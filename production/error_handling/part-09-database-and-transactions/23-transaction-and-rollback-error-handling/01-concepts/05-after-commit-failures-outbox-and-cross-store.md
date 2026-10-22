# After-Commit Failures, Outbox, and Cross-Store Consistency (23.15–23.20)

> Part IX · Chapter 23 · Sections 23.15–23.20 · _Estimated reading time: 24 min_
> **Prerequisite:** [Ambiguous Commits and Idempotent Retries](./04-ambiguous-commits-and-idempotent-retries.md)

## In one sentence

Once a transaction commits you **cannot roll it back**, so every effect after that point must be
**idempotent, retriable, or compensatable** — and "write the row and publish the event" belongs in
one transaction via the **transactional outbox**.

## Why this matters in production

The commit is the point of no return. A post-commit failure — the response write fails, the queue
publish times out, the Stripe call is rejected, the process crashes — leaves durable state that
the rest of the system does not know about. If you publish inline after commit, an event can be
**lost** (publish fails, no retry) or **invented** (publish succeeds, then the transaction is
rolled back by a later bug). The outbox removes both. Cross-store writes (Postgres + Redis +
S3 + Stripe) need the same discipline: one store is the source of truth, the others converge.

## Core concept

### 23.15 Failure after successful commit

| Failure | State | Response |
| ------- | ----- | -------- |
| Commit OK, HTTP response write fails | committed, client unsure | client retries with idempotency key |
| Commit OK, queue publish fails | committed, event missing | **outbox relay** retries |
| Commit OK, Stripe charge fails | order pending, no payment | retry charge / mark failed / reconcile |
| Commit OK, process OOMs | committed, nothing else ran | startup reconciliation scans `pending` |
| Commit OK, then a compensating step fails | partially applied workflow | retry compensation (idempotent) |

The rule: **the committed row is the source of truth; everything else converges toward it.**

### 23.16 Compensation

Compensation is a **new business action** that undoes the *effect* of a completed step. It is not
`ROLLBACK`:

| Rollback | Compensation |
| -------- | ------------ |
| Database-only | Cross-service / external |
| Automatic, immediate | Explicit, asynchronous |
| Restores prior state exactly | Produces a new state (refund, release, cancel) |
| Cannot fail meaningfully | Can fail, must be retried and idempotent |

`Checkout`: reserve inventory → charge → confirm. If confirm fails, compensate with **refund**
and **release reservation**, each keyed by the order id so a retry cannot double-refund.

### 23.17 Transactional outbox

Write the business change **and** an outbox row in the same transaction; a relay publishes rows
afterward. This turns "exactly once" into "at least once + consumer dedupe".

```sql
BEGIN;
  UPDATE orders SET status = 'paid' WHERE id = $1;
  INSERT INTO outbox (id, topic, payload, created_at)
  VALUES (gen_random_uuid(), 'order.paid', $2, now());
COMMIT;   -- business change and event are now atomic
```

### 23.18 Cross-store consistency

| Store pair | Consistency model | Mechanism |
| ---------- | ----------------- | --------- |
| Postgres + queue | eventual | outbox + relay + consumer dedupe |
| Postgres + Redis cache | eventual, TTL-bound | invalidate after commit; cache-aside |
| Postgres + S3 | eventual | write object, then commit pointer; orphan cleanup |
| Postgres + Stripe | **saga** | local intent row + provider idempotency key + reconciliation |

Never write two stores in one "logical transaction" unless one participates in the other's
protocol (e.g. transactional messaging). Choose an **owner** and make the other converge.

### 23.19 Uncertain persistence

Different from an ambiguous *commit*: you may be unsure whether an **external** effect applied
(Stripe timeout). Resolve with the provider's idempotency key or a query-by-reference, exactly as
with `08007`. Record the uncertainty (`payment_state='unknown'`) instead of guessing.

### 23.20 Transactional standards

Codify the decisions so every service behaves the same:

1. One transaction per aggregate; no network calls inside.
2. Events via outbox, never inline publish.
3. Retry only `40001`/`40P01`/class `08`, whole transaction, ≤3 attempts.
4. Non-idempotent writes require a key; keys are committed with the effect.
5. Unknown outcomes are a named state with a resolution procedure.
6. Compensation actions are idempotent and audited.
7. `idle_in_transaction_session_timeout` and `lock_timeout` are set.
8. Integration events carry `event_id`, `occurred_at`, `aggregate_id`, `version`.

## How it works (mechanics)

### The outbox relay

```text
                 ┌─────────────── Postgres ───────────────┐
 business txn ──▶│ orders row  +  outbox row (same txn)   │
                 └───────────────────┬────────────────────┘
                                     │ poll
                          ┌──────────▼───────────┐
                          │ relay worker          │
                          │ SELECT ... FOR UPDATE │
                          │   SKIP LOCKED         │
                          │ publish to queue      │
                          │ mark published_at     │
                          └──────────┬───────────┘
                                     ▼
                              broker / consumers
                              (dedupe on event_id)
```

1. Relay selects unpublished rows with `FOR UPDATE SKIP LOCKED` so multiple workers do not
   collide.
2. It publishes, then marks the row `published_at` (or deletes it after a retention window).
3. **Crash between publish and mark** → the event is published twice. Consumers must dedupe on
   `event_id`. This is why the outbox gives *at-least-once*, not exactly-once.
4. Poison rows (publish permanently failing) are retried with backoff and surfaced as a metric.

## Worked example

```sql
-- Outbox table (Postgres)
CREATE TABLE outbox (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  topic       text NOT NULL,
  payload     jsonb NOT NULL,
  created_at  timestamptz NOT NULL DEFAULT now(),
  published_at timestamptz,
  attempts    int NOT NULL DEFAULT 0
);
CREATE INDEX outbox_unpublished_idx ON outbox (created_at) WHERE published_at IS NULL;
```

```ts
// Relay — at-least-once, safe with multiple workers
async function relay(batch = 100) {
  await db.transaction(async (tx) => {
    const rows = await tx.any(
      `SELECT id, topic, payload FROM outbox
        WHERE published_at IS NULL
        ORDER BY created_at
        LIMIT $1
        FOR UPDATE SKIP LOCKED`,
      [batch],
    );
    for (const row of rows) {
      try {
        await broker.publish(row.topic, row.payload);       // may duplicate on crash
        await tx.query(`UPDATE outbox SET published_at = now() WHERE id = $1`, [row.id]);
      } catch (err) {
        await tx.query(`UPDATE outbox SET attempts = attempts + 1 WHERE id = $1`, [row.id]);
        throw err;                                          // retry the batch with backoff
      }
    }
  });
}
```

```text
Checkout flow with outbox:
  BEGIN → order(pending) + inventory reserve + outbox('order.created') → COMMIT
  relay → publish order.created → consumer initiates charge (idempotencyKey=order:{id})
  charge OK → consumer calls back → order(pending→paid) → outbox('order.paid')
  charge fails → compensation: release reservation, order(cancelled)
```

## Key data / numbers

- Outbox relay uses **`FOR UPDATE SKIP LOCKED`** (Postgres 9.5+, MySQL 8.0+) to parallelize.
- Poll interval commonly **100 ms–1 s**; batch **100–1,000**; publish latency is the trade-off.
- Outbox retention: keep published rows **24 h–7 days** for audit/replay, then purge.
- Stripe idempotency keys replay for **24 hours**; store your own record longer if you reconcile
  later.
- `event_id` + consumer dedupe is what makes **at-least-once** behave like exactly-once.
- Compensation must be **idempotent**: refund keyed by `order_id`, reservation release keyed by
  `reservation_id`.

## Real-world use case — Acme SaaS

Acme published `order.created` **after** committing the order. When the broker had a 30 s
outage, 412 orders committed with no event; inventory was reserved forever and customers never
got confirmation emails. A second bug published events for transactions that later rolled back,
producing phantom orders in the fulfillment service. Moving to an **outbox** fixed both: events
exist iff the order exists, the relay retries during outages, and consumers dedupe on
`event_id`. Reconciliation now scans `outbox` and `orders`, not a best-effort log.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Inline publish after commit | simple, low latency | loses/invents events | never for critical events |
| Transactional outbox | atomic, retriable | relay lag, table growth | default |
| CDC (log-based) | no app table | infra complexity, opaqueness | mature platforms |
| Two-phase commit | strong | brittle, slow, rarely supported | almost never |
| Saga + compensation | works across services | eventual, complex | multi-service workflows |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Write event + change in one transaction | Publish before commit |
| Dedupe consumers on `event_id` | Assume exactly-once delivery |
| Mark relay progress after publish | Delete the outbox row before publishing |
| Make compensation idempotent and audited | Refund twice on retry |
| Choose one owner per datum | Dual-write Postgres and Redis "atomically" |
| Record `unknown` external outcomes | Guess success or failure |

## Common mistakes

- **Publish-then-commit** — consumers see events for rolled-back work.
- **Commit-then-publish** — events are lost on broker failure.
- **No consumer dedupe** — outbox retries become duplicate emails/charges.
- **Deleting outbox rows before publish succeeds** — permanent event loss.
- **Compensation without idempotency** — retry double-refunds.
- **Reading a replica to resolve an unknown commit** — lag produces false negatives.

## Checklist

- [ ] Every integration event is written to an outbox in the same transaction.
- [ ] The relay uses `SKIP LOCKED`, marks after publish, and retries with backoff.
- [ ] Consumers dedupe on a stable `event_id`.
- [ ] Every cross-store flow names an owner and a convergence mechanism.
- [ ] Compensation actions are idempotent, audited, and retryable.
- [ ] `unknown` outcomes have a reconciliation job.

## Related

- [Ambiguous Commit Outcomes](../02-deep-dive/01-ambiguous-commit-outcomes.md)
- [Outbox Mechanics and Cross-Store Consistency](../02-deep-dive/02-outbox-mechanics-and-cross-store-consistency.md)
- [Outbox and Compensation in Code](../03-practical-examples/02-outbox-and-compensation-in-code.md)
- [Partial Failures and Multi-Step Operations (Ch. 39)](../../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
