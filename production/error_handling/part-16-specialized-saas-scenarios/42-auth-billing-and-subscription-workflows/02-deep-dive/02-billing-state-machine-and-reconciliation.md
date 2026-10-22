# Billing State Machine and Reconciliation — Mechanics

> Part XVI · Chapter 42 · Sections 42.10, 42.14, 42.15 · _Estimated reading time: 22 min_
> **Prerequisite:** [Invoices, Webhook-Driven State, and Billing Consistency](../01-concepts/04-invoice-webhooks-and-billing-consistency.md)

## In one sentence

Local billing state is a **versioned projection** updated only by an **idempotent, monotonic
applier**, and a **reconciliation job** that compares it against provider objects is what
converts "silent drift" into a detected, repairable condition.

## Why this matters in production

The applier is the single write-path for billing. If it is last-write-wins, out-of-order
webhooks regress state — a `canceled` subscription resurrected to `active`, an upgraded plan
downgraded by a late `invoice.paid`. If there is no ledger, duplicates double-apply. If there
is no reconciliation, the one event Stripe gave up retrying becomes a permanent lie in your
database that a customer will eventually find. This file is the mechanics behind the concepts.

## The state machine, formally

States (adopt the processor vocabulary even if you rename internals):

```text
incomplete ──▶ trialing ──▶ active ──▶ past_due ──▶ unpaid ──▶ canceled
     │            │            │           │           │
     └────────────┴────────────┴───────────┴───────────┴──▶ incomplete_expired (terminal)
active ──▶ paused ──▶ active
active ──▶ canceled   (terminal for this subscription id)
```

Every transition is a triple `(from_set, event, to)` with a guard. Encode the table, don't
scatter `if (status === ...)` through services:

```yaml
# transitions.yaml — single source of truth, loaded by the applier and the API layer
transitions:
  - to: active
    from: [trialing, past_due, paused]
    events: [invoice.paid, subscription.updated_active]
  - to: past_due
    from: [active, trialing]
    events: [invoice.payment_failed, subscription.updated_past_due]
  - to: unpaid
    from: [past_due]
    events: [dunning_exhausted]            # provider-driven or local dunning policy
  - to: canceled
    from: [active, past_due, unpaid, paused, trialing]
    events: [subscription.deleted, tenant_cancel]
  - to: paused
    from: [active]
    events: [subscription.paused]
terminal: [canceled, incomplete_expired]
```

Guards the applier enforces at write time:

1. `from ∈ transition.from` — else `SUBSCRIPTION_INVALID_TRANSITION` (dropped-event
   metric, not an exception storm).
2. `event_time > row.provider_updated_at` — **monotonicity**; stale events are counted and
   ignored.
3. Terminal states accept **no** transitions — a late `invoice.paid` for a canceled sub
   updates the invoice projection, never the subscription.
4. The whole apply runs in one DB transaction with the ledger insert (same tx), so "recorded"
   and "applied" cannot diverge.

## The applier, end to end

```ts
async function apply(event: StripeEvent, tx: Tx): Promise<ApplyResult> {
  const led = await tx.insert("billing_event_ledger", { id: event.id, type: event.type,
    provider_created: event.created, payload: event },
    { onConflict: "id", doNothing: true });          // idempotent by primary key
  if (!led.inserted) return ApplyResult.duplicate(event.id);

  const change = project(event);                     // event → SubscriptionChange | null
  if (!change) return ApplyResult.ignored(event.type);

  const row = await tx.selectForUpdate("subscriptions", change.providerId);
  if (!row) {
    // Webhook can beat our own insert. Upsert a shell row; the checkout flow fills it.
    await tx.insert("subscriptions", { ...change, version: 1 }, { onConflict: "provider_id" });
    return ApplyResult.created(change.providerId);
  }
  if (TERMINAL.has(row.status)) return ApplyResult.terminalSkipped(row.status);
  if (change.providerUpdatedAt <= row.provider_updated_at) return ApplyResult.stale(change);
  if (!isLegal(row.status, change.status)) return ApplyResult.illegalTransition(row.status, change.status);

  await tx.update("subscriptions", change.providerId, {
    status: change.status,
    provider_updated_at: change.providerUpdatedAt,
    version: row.version + 1,
  });
  await tx.insert("outbox", { topic: "subscription.changed", payload: { ...change } });
  return ApplyResult.applied(row.status, change.status);
}
```

**Key data:** dedupe = `billing_event_ledger.id` = provider `event.id`; monotonic guard =
provider object timestamp (Stripe exposes `created` on the object; for period-sensitive
facts use `current_period_end`); optimistic version column lets entitlement readers detect
mid-read changes; outbox event fires entitlement-cache invalidation in the same transaction.

## Reconciliation: the backstop

Webhooks are at-least-once **until they are at-most-zero** — after the provider's retry
window (Stripe: up to **~3 days**) an unacked event is simply gone. Reconciliation is a
**periodic full-state comparison**, not another event consumer:

```text
for each active local subscription (paged):
    fetch provider object (batched, respecting rate limits)
    if fetch 404 → mark canceled_via_reconciliation, alert if local was active/paid
    if status/period/plan differ beyond tolerance → classify drift → apply or alert
nightly: full sweep;  hourly: high-value / past_due cohorts
```

Drift classes and their handling:

| Drift | Example | Action |
| ----- | ------- | ------ |
| Provider ahead, monotonic | local `past_due`, provider `active` | Auto-apply (provider wins) |
| Provider ahead, money-sensitive | local `active`, provider `canceled` | Auto-apply **and** flag refund/grace review |
| Local ahead (impossible?) | local `active`, provider `incomplete` | Alert — projection bug or write outside applier |
| Missing locally | provider has sub, no row | Insert shell row, alert if invoices exist |
| Orphaned locally | local row, provider 404 | Auto-apply terminal `canceled` after grace |

**Key data:** reconciliation cadence recommendation — **hourly** for `past_due`/high-value
cohorts, **nightly** for everything active; run it as a regular background job
(Chapter 32's retry/DLQ rules apply: a flaky provider API must not fail the whole sweep —
per-item results, partial success, checkpointed paging).

## Invariants to test

Property tests that catch the whole bug class:

1. **Idempotence:** applying the same event twice ⇒ identical row (version unchanged the
   second time).
2. **Monotonicity:** for any permutation of a shuffled event set, the final projected status
   equals the status after applying in provider-timestamp order.
3. **Terminality:** after `canceled`, no event sequence changes the status.
4. **Ledger-apply atomicity:** kill the process between ledger insert and update; the retry
   must not double-apply, and must complete the apply.

```ts
// Property 2 in a nutshell — shuffle and converge.
it("converges regardless of delivery order", async () => {
  const events = await fixture.subscriptionEventSet("sub_1");
  for (const perm of permutations(shuffle(events, seed))) {
    await resetProjection();
    for (const e of perm) await apply(e);
    expect(await projectedStatus("sub_1")).toBe("active");
  }
});
```

## Real-world use case — the resurrected subscription

Acme's applier was last-write-wins. A tenant canceled; the `customer.subscription.deleted`
event applied. Hours later a delayed `invoice.paid` for the final prorated invoice arrived
and set the row back to `active` with a fresh period — the canceled tenant kept Pro
entitlements for a quarter and only stopped when their card expired. The fixes were exactly
the three mechanics above: ledger (no double-apply), terminal-state guard (a late event can
never resurrect), monotonic timestamps (an older event can never overwrite). The regression
test that now guards it: shuffle the full event set of a cancel-then-final-invoice scenario a
thousand times and assert convergence to `canceled`.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Last-write-wins applier | Simple | Silent regressions | Never for billing |
| Guarded + ledger | Correct under reordering/dupes | More code | ✅ Default |
| Full event replay rebuild | Rebuildable history | Expensive, needs retention | Audit / disaster recovery |
| Reconcile only | No webhook complexity | Slow detection, API load | Low volume only |
| Webhooks + reconciliation | Fast + self-healing | Two paths to maintain | ✅ Default |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep transitions in one table (code or config) | Scatter status writes across services |
| Insert the ledger row in the same tx as the apply | Dedupe with a separate "processed?" check |
| Ignore and count stale events | Let them overwrite newer state |
| Make reconciliation auto-apply the safe class | Only alert on drift |
| Test with shuffled event order | Test only the happy order |

## Common mistakes

- **Status writes from feature code** — bypasses every guard; enforce with permissions or a
  single repository.
- **Comparing status strings without timestamps** — order-dependence hides until production.
- **Reconciliation without rate-limit awareness** — the sweep itself gets 429'd and gives up;
  page and checkpoint instead.
- **Ledger without payload** — you cannot replay/rebuild without the original event.

## Checklist

- [ ] Transition table exists and the applier is table-driven.
- [ ] Ledger insert and projection update share one transaction.
- [ ] Stale events are detected, counted, and dropped.
- [ ] Terminal states reject all transitions.
- [ ] Reconciliation sweeps at least nightly, auto-applies safe drift, alerts on the rest.
- [ ] Shuffled-order property test passes in CI.

## Related

- [Invoices, Webhook-Driven State, and Billing Consistency](../01-concepts/04-invoice-webhooks-and-billing-consistency.md)
- [Webhook Reconciliation and Safe Financial Retries](../03-practical-examples/02-webhook-reconciliation-and-safe-financial-retries.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- [Chapter 33 — Events, Webhooks, and Message Processing](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
