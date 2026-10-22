# Property Tests for `WebhookIngest` (51.2, 51.9, 51.13, 51.14)

> Part XX · Chapter 51 · Practical example · _Estimated reading time: 20 min_
> **Prerequisite:** [Verifying Properties with Failure Injection](../02-deep-dive/01-verifying-properties-with-failure-injection.md)

## In one sentence

`WebhookIngest` is the ideal subject for property-based testing: it is **at-least-once**, so
duplicates, reordering, and concurrent delivery are the normal case — not the exception.

## Why this matters in production

Stripe delivers webhooks **at least once** and does not guarantee ordering. Two deliveries of the
same event can arrive concurrently, seconds apart, or after a 3-day outage. Everything your handler
assumes about "once, in order" is false in production.

That makes `WebhookIngest` a testing problem with a clean formulation: **for any N ≥ 1 deliveries of
the same event, exactly one effect occurs.** Property-based testing states that once, and the
generator explores the interleavings you would never think to write by hand.

## The properties under test

| Property | Statement | Oracle |
| -------- | --------- | ------ |
| 51.9 | N deliveries of the same `event_id` ⇒ exactly one subscription activation | `count(subscriptions) == 1` |
| 51.2 | Every rejected delivery is recorded with a reason | `count(error_events) == rejections` |
| 51.13 | Concurrent deliveries of the same event ⇒ one effect, no interleaved partial writes | unique constraint holds; no `23505` escapes |
| 51.14 | A batch of N events ⇒ successes + failures == N, per-event | `results.length == N` |
| 51.3 | The same invalid payload always yields the same code | `code` stable across 100 runs |
| 51.10 | Every response body validates against the published schema | schema check on every path |

## The generator

```ts
// A generator that produces *delivery schedules*, not just payloads.
type Delivery = { eventId: string; payload: unknown; delayMs: number };

function* deliverySchedules(events: WebhookEvent[], seed: number) {
  const rand = mulberry32(seed);
  for (const event of events) {
    // Duplicates: 0..3 extra copies of the same event.
    const copies = 1 + Math.floor(rand() * 3);
    for (let i = 0; i < copies; i++) {
      // Deliveries may overlap in time (concurrent) and may be reordered.
      yield {
        eventId: event.eventId,
        payload: event.payload,
        delayMs: Math.floor(rand() * 50),
      };
    }
  }
}
```

The important detail: the generator produces **overlapping deliveries**, so the test actually
exercises the race instead of politely serializing it.

## The tests

### 51.9 — exactly one effect per event

```ts
it("N deliveries of the same event produce exactly one subscription", async () => {
  for (const seed of [1, 7, 42, 1337, 90210]) {
    const h = await harness.start();
    const event = validEvent({ type: "invoice.paid" });

    // Deliver the same event 5 times, concurrently.
    await Promise.all(
      Array.from({ length: 5 }, () => h.deliver(event, { delayMs: 0 })),
    );

    expect(await h.countActivations(event.id)).toBe(1);      // the oracle
    expect(await h.countErrorEvents(event.id)).toBe(4);      // the 4 losers were recorded
  }
});
```

The second assertion matters as much as the first: the losing duplicates must be **recorded as
handled duplicates**, not thrown as errors. An unhandled `23505` would page someone at 3 a.m.

### 51.13 — concurrency safety of the dedupe

```ts
it("concurrent deliveries never produce a partial write", async () => {
  const h = await harness.start();
  const event = validEvent({ type: "invoice.paid" });

  const results = await Promise.allSettled(
    Array.from({ length: 20 }, () => h.deliver(event, { delayMs: Math.random() * 10 })),
  );

  // 51.2: every rejection is a *recorded* outcome, not a lost one.
  expect(results.filter((r) => r.status === "rejected")).toHaveLength(0);

  // 51.13: exactly one activation, and the invariant holds afterwards.
  expect(await h.countActivations(event.id)).toBe(1);
  expect(await h.orphanedEntitlementCount()).toBe(0);
});
```

### 51.14 — per-event reporting on a batch

```ts
it("a batch of 10 events reports 10 outcomes", async () => {
  const h = await harness.start();
  const events = [
    ...Array.from({ length: 8 }, (_, i) => validEvent({ type: "invoice.paid", id: `e${i}` })),
    invalidEvent({ type: "invoice.paid" }),                  // bad signature
    unknownTypeEvent({ type: "wallet.updated" }),           // unknown event type
  ];

  const results = await h.deliverBatch(events);

  expect(results.length).toBe(10);                            // completeness
  expect(results.filter((r) => r.outcome === "succeeded").length).toBe(8);
  expect(results.filter((r) => r.outcome === "rejected").length).toBe(1);   // bad signature
  expect(results.filter((r) => r.outcome === "acknowledged_unknown").length).toBe(1);
  // 51.14: successes + failures == attempted, and the outcome is per-event.
  expect(results.filter((r) => r.outcome === "succeeded").length +
         results.filter((r) => r.outcome === "rejected").length +
         results.filter((r) => r.outcome === "acknowledged_unknown").length).toBe(10);
});
```

### 51.3 — deterministic classification

```ts
it("the same invalid payload always produces the same code", () => {
  const codes = new Set<string>();
  for (let i = 0; i < 100; i++) {
    codes.add(classify(garbledPayload(seeded(i))).code);
  }
  expect(codes.size).toBe(1);
  expect([...codes][0]).toBe("WEBHOOK_PAYLOAD_INVALID");
});
```

### 51.10 — contract conformance on every path

```ts
it("every delivery path returns a schema-valid body", async () => {
  const h = await harness.start();
  const paths = await h.allDeliveryPaths();     // success, bad signature, unknown type, duplicate, timeout

  for (const path of paths) {
    const res = await h.deliver(path.event);
    expect(() => errorEnvelopeSchema.parse(res.body)).not.toThrow();   // 51.10
    expect(res.status).toBe(path.expectedStatus);
  }
});
```

## The implementation that makes the tests pass

```ts
// The dedupe record is inserted in the SAME transaction as the effect.
// Check-then-act (get, then insert) loses the race under concurrency (51.13).
export async function applyInvoicePaid(event: StripeEvent, ctx: OpContext): Promise<void> {
  await ctx.db.transaction(async (tx) => {
    const inserted = await tx.query(
      `INSERT INTO webhook_events (provider, event_id, type, payload, received_at)
       VALUES ('stripe', $1, $2, $3, now())
       ON CONFLICT (provider, event_id) DO NOTHING
       RETURNING id`,
      [event.id, event.type, JSON.stringify(event.data)],
    );

    if (inserted.length === 0) {
      // 51.9: duplicate detected. This is a SUCCESS, recorded as such.
      await tx.query(
        `INSERT INTO webhook_duplicates (provider, event_id, observed_at) VALUES ('stripe', $1, now())`,
        [event.id],
      );
      return;
    }

    await tx.query(
      `INSERT INTO subscriptions (tenant_id, plan_id, status) VALUES ($1, $2, 'active')
       ON CONFLICT (tenant_id, source_event_id) DO NOTHING`,
      [event.tenantId, event.planId, event.id],
    );
    await tx.query(
      `INSERT INTO entitlements (tenant_id, feature) VALUES ($1, 'reporting')`,
      [event.tenantId],
    );
  });
}
```

Note the `ON CONFLICT DO NOTHING` on `subscriptions` as well: even if the dedupe table is somehow
bypassed, the effect is still at-most-once.

## Key data / numbers

- **Duplicates per event: 0–3** in the generator; production reality is 1–2 for most providers and
  higher during provider incidents.
- **Stripe webhook replay window: 3 days**; Stripe retries non-2xx responses for up to **3 days**.
- **Signature tolerance: 300 seconds** — a delivery older than that must be rejected as permanent,
  not retried.
- **Concurrency in tests: 5–20 concurrent deliveries** of the same event; 20 is enough to expose a
  check-then-act race on a CI machine.
- **Seeds per property: 5 fixed + 1 random.** The random seed is printed on failure.
- **Oracles per property test: exactly 1 primary** (plus optional invariants). Multiple oracles
  make failures ambiguous.
- **Batch reporting: per-event outcomes**, never a single aggregate boolean.

## Real-world use case — Acme SaaS `WebhookIngest`

Acme's webhook handler was idempotent "in practice" because Stripe usually delivered events once.
The property test found the race on the **first run**, with seed `1`:

```text
  seed=1 → 5 concurrent deliveries of invoice.paid
  → countActivations = 2     ← expected 1
  → countErrorEvents = 0     ← the duplicate was NOT recorded
```

The cause was a `SELECT` followed by an `INSERT` in two transactions, plus a `catch` that swallowed
the unique-violation error. Two properties were broken at once: **51.9** (duplicate effect) and
**51.2** (the swallowed `23505` — the duplicate was invisible to everyone).

The fix was the single-transaction insert shown above, plus an explicit duplicate branch that
records the observation. After the fix, the same test passed for all seeds, and the production
duplicate-activation count went from ~2/week to 0 over the following month.

A second property test paid for itself immediately: the "unknown event type" path had been
returning `500`, which made Stripe redeliver the same event for three days. The property test
asserted `acknowledged_unknown` with `2xx`; the fix was one line and removed roughly 8 000
redeliveries per month from the queue.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Property-based testing | Explores interleavings you would not write | Seed debugging cost | At-least-once consumers, schedulers, classifiers |
| Example-based tests | Easy to read, fast to write | Misses the race | Every specific bug found |
| Load testing | Realistic timing | Expensive, flaky, hard to assert | Capacity questions, not correctness |
| Idempotency by construction | Removes the problem class | Requires schema + discipline | Always — belt *and* braces with tests |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Generate overlapping delivery schedules | Test duplicates sequentially only |
| Assert the losing duplicates are recorded | Only assert the effect count |
| Keep exactly one primary oracle per test | Assert five things and debug all five |
| Print the seed on failure | Hide the seed in CI logs |
| Use `ON CONFLICT DO NOTHING` in the same transaction as the effect | Check-then-act across two transactions |
| Treat a duplicate detection as a success | Throw the unique-violation error upward |

## Common mistakes

- **Serializing the test.** `await h.deliver(...)` in a loop removes the race you are trying to
  find.
- **Asserting only the happy path.** "5 deliveries → 1 activation" without "4 recorded duplicates"
  passes while the duplicates are being swallowed.
- **Trusting provider at-least-once semantics to be rare.** Providers duplicate more during their
  own incidents, exactly when your system is least healthy.
- **Testing the handler in isolation.** The real duplicate happens between the dedupe write and the
  effect write, which only exists in the transactional version.

## Checklist

- [ ] Every at-least-once consumer has a property test asserting at-most-once effects.
- [ ] The generator produces overlapping, reordered, duplicated deliveries.
- [ ] The losing duplicates are asserted to be *recorded*, not just counted.
- [ ] Batch results are asserted per event, and the counts sum to the batch size.
- [ ] Classification determinism is tested with at least 5 fixed seeds.
- [ ] Every delivery path is asserted against the response schema.
- [ ] The failing seed is printed and replayable from CI.

## Related

- [Verifying Properties with Failure Injection](../02-deep-dive/01-verifying-properties-with-failure-injection.md)
- [Determinism and Completeness (51.1–51.4)](../01-concepts/01-determinism-and-completeness.md)
- [Chapter 33 — Events, Webhooks, and Message Processing](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
- [Chapter 28 — Idempotency and Duplicate-Operation Safety](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
