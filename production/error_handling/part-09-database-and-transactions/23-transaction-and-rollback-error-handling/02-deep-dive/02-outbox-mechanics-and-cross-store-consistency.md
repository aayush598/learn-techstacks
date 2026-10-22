# Outbox Mechanics and Cross-Store Consistency

> Part IX · Chapter 23 · Sections 23.16–23.18, 23.20 · _Estimated reading time: 24 min_
> **Prerequisite:** [After-Commit Failures, Outbox, and Cross-Store (23.15–23.20)](../01-concepts/05-after-commit-failures-outbox-and-cross-store.md)

## In one sentence

The outbox turns a **dual write** (database + broker) into a **single write plus a relay**, and
cross-store consistency is the same idea generalized: pick an owner, make everyone else
**converge idempotently**.

## Why this matters in production

"Commit then publish" looks fine until the broker is unavailable for 30 seconds: committed orders
have no events, downstream services never see them, and nothing retries. "Publish then commit"
looks fine until the transaction rolls back: downstream sees orders that do not exist. The outbox
eliminates both classes of bug, at the cost of **at-least-once delivery**, which you must handle
with consumer dedupe. Everything else in this file is detail that decides whether the relay
scales, stalls, or duplicates forever.

## Outbox table design

```sql
CREATE TABLE outbox (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  aggregate_id text        NOT NULL,
  topic        text        NOT NULL,
  payload      jsonb       NOT NULL,
  headers      jsonb       NOT NULL DEFAULT '{}'::jsonb,
  created_at   timestamptz NOT NULL DEFAULT now(),
  available_at timestamptz NOT NULL DEFAULT now(),   -- delayed delivery
  published_at timestamptz,
  attempts     int         NOT NULL DEFAULT 0,
  last_error   text
);

-- The relay's hot path: only unpublished rows, oldest first.
CREATE INDEX outbox_pending_idx
  ON outbox (available_at, created_at)
  WHERE published_at IS NULL;
```

| Column | Purpose |
| ------ | ------- |
| `id` | event identity → consumers dedupe on it |
| `aggregate_id` | ordering/partition key (per aggregate, order matters) |
| `topic` | routing |
| `available_at` | delayed retries without a separate scheduler |
| `published_at` | completion marker; `NULL` means pending |
| `attempts` / `last_error` | poison-message detection and observability |

## Relay mechanics

```ts
// Polling relay. Multiple workers are safe because of SKIP LOCKED.
async function relayOnce(batch = 200) {
  await db.transaction(async (tx) => {
    const rows = await tx.any(
      `SELECT id, topic, payload, headers, attempts
         FROM outbox
        WHERE published_at IS NULL AND available_at <= now()
        ORDER BY created_at
        LIMIT $1
        FOR UPDATE SKIP LOCKED`,
      [batch],
    );
    for (const row of rows) {
      try {
        await broker.publish(row.topic, row.payload, {
          eventId: row.id,
          headers: row.headers,
        });
        await tx.query(`UPDATE outbox SET published_at = now() WHERE id = $1`, [row.id]);
      } catch (err) {
        await tx.query(
          `UPDATE outbox
              SET attempts = attempts + 1,
                  last_error = $2,
                  available_at = now() + make_interval(secs => LEAST(300, power(2, attempts)))
            WHERE id = $1`,
          [row.id, String(err)],
        );
      }
    }
  });
}
```

Key properties:

1. **Ordering is per aggregate, not global.** Publishing in parallel reorders across aggregates;
   consumers that need per-aggregate order must partition by `aggregate_id`.
2. **Crash between publish and mark** → duplicate publish. Consumers **must** dedupe on `id`.
3. **One bad row does not block the batch** — catch per row and schedule `available_at`.
4. **`SKIP LOCKED`** lets N workers share the table without contention (Postgres 9.5+, MySQL 8+).
5. **Delete or archive** published rows after a retention window; do not let the table grow
   unbounded.

## Delivery semantics

| Guarantee | How achieved | Cost |
| --------- | ------------ | ---- |
| At-most-once | publish, then mark (crash → lost) | **lost events** |
| At-least-once | mark, then publish? no — publish, mark may duplicate | consumer dedupe required |
| Exactly-once | at-least-once + idempotent consumer | needs dedupe store |

The outbox is **at-least-once**. "Exactly-once" is a property of the *consumer*, not the broker.

## Cross-store patterns

### Database + cache (Redis)

```text
1. Commit DB change.
2. Delete cache key (invalidate, don't write-through).
3. Next read repopulates from DB.
```

Deleting **after** commit is correct; deleting **before** commit lets a concurrent read
repopulate stale data. Cache TTL is the backstop for a missed invalidation.

### Database + object storage (S3)

```text
1. Write object to S3 with a deterministic key (tenant/export/id).
2. Commit the pointer/metadata row in Postgres.
3. A failure after (1) leaves an orphan → cleanup job deletes unreferenced objects.
   A failure before (2) means the export is not visible → safe retry with the same key.
```

Never commit the pointer **before** the object exists, or readers will 404.

### Database + payment provider (Stripe)

```text
saga:
  1. local: order(pending) + outbox('order.created')       [atomic]
  2. charge: provider idempotencyKey = order:{id}
  3. local: order(pending→paid)
  failure at 2 → retry with the SAME key; at 3 → reconciliation job
  abandonment → compensate: refund (idempotent) + release reservation
```

### Compensation boundaries

| Step | Compensating action | Idempotency key |
| ---- | ------------------- | --------------- |
| Reserve inventory | Release reservation | `reservation:{orderId}` |
| Charge card | Refund | `refund:{paymentId}` |
| Create S3 export | Delete object | deterministic object key |
| Send email | Not compensatable (accept) | `email:{orderId}` |

Compensation is **forward-only** — it produces new facts (`refunded`, `released`) and is audited.
Never "un-send" an email; never rely on deleting history.

## Worked example — `Checkout` end to end

```text
1. API: POST /checkout  Idempotency-Key: ord_9f2
2. TX:  insert order(pending)          → id=9001
        reserve inventory
        insert outbox('order.created', aggregate=9001)
        upsert idempotency_keys('ord_9f2', completed, response)
   COMMIT
3. Relay: publish order.created(eventId=…)
4. Consumer: charge with Idempotency-Key=order:9001
5. Consumer: TX update order 9001 → paid
             insert outbox('order.paid')
6. Relay: publish order.paid → email, fulfillment
7. If charge fails permanently:
             TX update order 9001 → cancelled
             release reservation (idempotent)
             insert outbox('order.cancelled')
```

Every step is retriable; every retry reuses a key; every event is deduped by `eventId`.

## Key data / numbers

- `SKIP LOCKED`: Postgres **9.5+**, MySQL **8.0+**.
- Relay poll: **100 ms–1 s**; batch **100–1,000**; publish latency target **< 2 s p99**.
- Retry backoff for poison rows: exponential capped at **5 minutes**; after N attempts
  (commonly **10–20**) move to a **dead-letter table/topic** and alert.
- Outbox retention: **24 h–7 days** published rows; index only pending rows.
- `pg_prepared_xacts`: keep empty; any long-lived row blocks vacuum and locks.
- At-least-once means **consumer dedupe is mandatory** — a unique `(consumer, event_id)` table or
  an idempotent upsert.

## Real-world use case — Acme SaaS

Acme used "commit then publish" for `ExportJob` completions. During a broker upgrade, 1,100
exports completed with no event; the UI never showed the download link, and support regenerated
them manually. After moving to an outbox with a `SKIP LOCKED` relay, a repeat outage produced
**zero** lost events: the relay drained the backlog in under a minute. Consumers dedupe on
`eventId`, so the crash-during-publish duplicates were harmless. The same table now backs
`order.created`, `order.paid`, and `export.completed`.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Outbox + polling relay | atomic, simple infra | poll latency, table growth | default |
| Outbox + CDC (Debezium) | low latency, no poller | infra, schema coupling | mature platforms |
| Inline publish | lowest latency | lost/invented events | never for critical |
| Transactional messaging (broker txn) | native atomicity | broker-specific, limited | when supported end-to-end |
| Two-phase commit | strong atomicity | slow, brittle, ops burden | almost never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Insert the outbox row in the business transaction | Publish before `COMMIT` |
| Dedupe consumers on `event_id` | Assume exactly-once |
| Partition by `aggregate_id` when order matters | Publish one aggregate's events in parallel |
| Move poison rows to a DLQ and alert | Retry forever with no visibility |
| Invalidate cache after commit | Write stale values into the cache |
| Use deterministic S3 keys | Generate a new key per retry |

## Common mistakes

- **Deleting the outbox row before publish** — event loss on crash.
- **No consumer dedupe** — retries become duplicate emails and charges.
- **Global ordering assumptions** — parallel relays reorder across aggregates.
- **Unbounded outbox growth** — table bloat and slow relays.
- **Pointer-before-object in S3** — readers see missing files.
- **Compensation without idempotency** — double refunds on retry.

## Checklist

- [ ] Business change and outbox row commit atomically.
- [ ] Relay uses `SKIP LOCKED`, marks after publish, and backs off on failure.
- [ ] Consumers dedupe on a stable `event_id`.
- [ ] Published rows are archived/purged on a schedule.
- [ ] Each cross-store flow names an owner and a convergence mechanism.
- [ ] Compensation is idempotent, audited, and retried from the outbox.

## Related

- [After-Commit Failures, Outbox, and Cross-Store (23.15–23.20)](../01-concepts/05-after-commit-failures-outbox-and-cross-store.md)
- [Ambiguous Commit Outcomes](./01-ambiguous-commit-outcomes.md)
- [Outbox and Compensation in Code](../03-practical-examples/02-outbox-and-compensation-in-code.md)
- [Events, Webhooks, and Message Processing (Ch. 33)](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
