# At-least-once and Idempotent Consumers — Mechanics

> Part XII · Chapter 33 · Sections 33.4–33.5 (mechanics) · _Estimated reading time: 16 min_
> **Prerequisite:** [Delivery Guarantees, Duplicates, and Ordering](../01-concepts/02-delivery-guarantees-duplicates-and-ordering.md)

## In one sentence

Every event transport you will use delivers **at least once**, so the consumer's job is to translate
that into **exactly-once effects** using a durable, atomic dedupe key tied to the event identity.

## Why this matters in production

The duplicate window is not theoretical: it is the time between "the effect committed" and "the
offset/ack committed." Any crash, rebalance, timeout, or deploy in that window causes redelivery.
If the consumer is not idempotent, that window becomes a duplicate charge, a duplicate email, or a
double-counted usage record. The size of the window is irrelevant; the existence of it is what
matters.

## The delivery/processing distinction

```text
delivery:    broker → consumer      (at-least-once: duplicates possible)
processing:  consumer → effect      (make it idempotent: duplicates become no-ops)
result:      effectively-once
```

"Naming it exactly-once" without an idempotent effect is wishful thinking. Name the delivery
guarantee and the processing guarantee separately in your docs.

## Consumer dedupe patterns

### Pattern 1 — Inbox table (recommended)

```sql
CREATE TABLE consumer_inbox (
  consumer     text NOT NULL,
  event_id     text NOT NULL,
  received_at  timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (consumer, event_id)
);
```

```ts
await db.transaction(async (tx) => {
  const claimed = await tx.inbox.insertIfAbsent({ consumer: "BillingProjector", eventId: event.id });
  if (!claimed) return;                 // duplicate: no-op
  await applyProjection(tx, event);     // same transaction
});
```

The dedupe row and the effect commit together. If the effect fails, the transaction rolls back and
the event can be retried.

### Pattern 2 — Effect key with unique constraint

```sql
INSERT INTO ledger_entries (event_id, tenant_id, amount_cents)
VALUES ($1, $2, $3)
ON CONFLICT (event_id) DO NOTHING;
```

Use when the effect itself has a natural event id. Simpler than a separate inbox, but not every effect
maps to one row.

### Pattern 3 — Offset/checkpoint (stream consumers)

For Kafka-style consumers, the offset commit **is** the dedupe cursor:

```text
process record → write effect → commit offset
```

If you commit before the effect, a crash loses the record. If you commit after, a crash duplicates the
effect. Therefore the effect must be idempotent (Patterns 1/2) or the sink must be transactional.

## Where dedupe must live

| Store | Durability | Atomic with effect | Verdict |
| ----- | ---------- | ------------------ | ------- |
| In-memory `Set` | Process lifetime | No | ❌ Never for effects |
| Redis `SETNX` + TTL | Until TTL/eviction | No | ⚠️ Best-effort only |
| DB unique constraint | Durable | Yes (same txn) | ✅ Default |
| Provider idempotency key | Provider-defined | At provider | ✅ For external effects |
| Kafka offset | Durable per partition | Only with transactions | ✅ With idempotent sink |

## The ordering that makes it safe

```text
1. BEGIN
2. INSERT INTO consumer_inbox (consumer, event_id) ON CONFLICT DO NOTHING
3. if 0 rows -> COMMIT (duplicate) and return
4. apply the effect
5. COMMIT
6. ack/commit offset
```

If the crash happens:

| Crash point | Inbox row | Effect | Retry behavior |
| ----------- | --------- | ------ | -------------- |
| After 2 | ✅ | ❌ | Transaction rolls back; retry applies |
| After 4 | ✅ | ✅ | Transaction rolls back; retry applies |
| After 5, before ack | ✅ | ✅ | Retry sees duplicate → no-op |
| After ack | ✅ | ✅ | No retry |

The only safe rows require the inbox insert and effect to be in **one transaction**.

## Idempotency for external effects

You cannot put Stripe inside your DB transaction. Use the provider's idempotency key derived from the
event:

```ts
await stripe.refunds.create(
  { payment_intent: pi, amount },
  { idempotencyKey: `refund:${event.id}` },
);
```

The provider stores the result for its retention window (Stripe: 24 h) and returns the same response
for the same key. Outside that window, rely on a durable local record of the provider id.

## Rebalance and batch semantics

Kafka can redeliver an entire batch after a rebalance, even records you already processed. SQS can
redeliver a subset. Lambda's partial-batch response narrows the retry set, but it is not a guarantee
of no duplicates. Design every handler as if it will see the same event again.

```ts
async function onBatch(records: Record[]) {
  const failures: BatchItemFailure[] = [];
  for (const r of records) {
    try {
      await handleIdempotent(r);          // inbox + effect
    } catch (err) {
      if (isRetryable(err)) failures.push({ itemIdentifier: r.id });
      else await dlq.publish(r, err);
    }
  }
  return { batchItemFailures: failures };
}
```

## Worked example — BillingProjector double credit

Acme processed `usage.recorded` events and incremented a counter:

```ts
// ❌ Not idempotent: a redelivery increments twice.
await usage.increment(tenantId, units);
```

A consumer rebalance redelivered 40 events; tenants were over-billed by 40× the batch size. The fix:

```ts
await db.transaction(async (tx) => {
  const claimed = await tx.inbox.insertIfAbsent({ consumer: "Usage", eventId: event.id });
  if (!claimed) return;
  await tx.usage.incrementForEvent({ eventId: event.id, tenantId, units });
});
```

`incrementForEvent` writes a `(event_id, units)` row and updates the aggregate; the unique constraint
on `event_id` makes the increment idempotent even if the inbox check races.

## Key data / numbers

- Kafka `enable.auto.commit=true` can commit **before** processing; prefer manual commits.
- Kafka default `max.poll.records`: **500**; a rebalance may replay the uncommitted batch.
- SQS at-least-once: duplicates are possible even without failures.
- Stripe idempotency key retention: **24 hours**.
- Redis `SETNX` + TTL is best-effort; eviction can re-enable duplicates.
- Dedupe retention recommendation: longer than the maximum replay window (often 7–30 days).

## Real-world use case — WebhookIngest

`WebhookIngest` deduped on a Redis key with a 1-hour TTL. Stripe retried a failed `invoice.paid`
delivery 26 hours later after an outage; the key had expired, the handler ran again, and the tenant
received a second credit. The fix moved dedupe into the `consumer_inbox` table with no TTL and a
unique `(consumer, event_id)` constraint, committing with the credit in one transaction. A later
48-hour outage produced zero duplicate credits.

## Trade-offs

| Dedupe store | Pros | Cons | When to use |
| ------------ | ---- | ---- | ----------- |
| DB inbox | Durable, atomic | Write per event | Default |
| Redis SETNX | Fast | Eviction/TTL risk | Non-financial, short window |
| Provider idempotency | No local state | Provider window | External side effects |
| Offset commit | Native to stream | Not atomic with sink | Idempotent sinks |
| Natural unique key | No extra table | Only some effects | Ledger rows |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Dedupe on the event's stable id | Dedupe on payload content |
| Commit dedupe with the effect | Separate check and write |
| Make external effects idempotent | Generate a new key per attempt |
| Retain keys past the replay window | Rely on a 1-hour TTL |
| Assume batch redelivery | Assume a clean offset |

## Common mistakes

- **Check-then-write race** — two consumers both pass the check.
- **Dedupe transaction separate from effect** — crash between them.
- **TTL shorter than provider retry window** — duplicates after expiry.
- **Provider key including attempt number** — defeats provider dedupe.
- **Auto-commit before processing** — data loss on crash.

## Checklist

- [ ] Is there a durable dedupe key per event?
- [ ] Is the dedupe insert in the same transaction as the effect?
- [ ] Is the dedupe retention longer than the max retry/replay window?
- [ ] Are external effects keyed by a stable event id?
- [ ] Are batch redeliveries assumed?
- [ ] Is auto-commit disabled or safe?
- [ ] Are duplicates measured as a metric, not logged as errors?

## Related

- [Delivery Guarantees, Duplicates, and Ordering](../01-concepts/02-delivery-guarantees-duplicates-and-ordering.md)
- [At-least-once vs Exactly-once (Chapter 32)](../../32-background-jobs-queues-and-scheduled-tasks/02-deep-dive/02-at-least-once-vs-exactly-once.md)
- [Event Consumer Partial Batch and DLQ](../03-practical-examples/02-event-consumer-partial-batch-and-dlq.md)
- [Chapter 28 — Idempotency](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
