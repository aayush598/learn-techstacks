# Delivery Guarantees, Duplicates, and Ordering

> Part XII · Chapter 33 · Sections 33.4, 33.5, 33.7 · _Estimated reading time: 17 min_
> **Prerequisite:** [Publish and Consume Failures](./01-publish-and-consume-failures.md)

## In one sentence

Assume **at-least-once delivery, duplicates, and no global ordering**; make the consumer idempotent
and either partition for order or tolerate disorder — never rely on the transport for either.

## Why this matters in production

The most damaging event bug is the **duplicate side effect**: a `invoice.paid` event processed twice
marks a subscription paid twice, credits a balance twice, or sends two receipts. The second most
damaging is **out-of-order state**: a `subscription.canceled` arriving before `subscription.created`
leaves the customer canceled, or a stale `updated` overwrites a newer one. Both are normal transport
behavior, not anomalies.

## 33.4 — At-most-once, at-least-once, exactly-once

| Guarantee | Duplicates | Loss | How it happens |
| --------- | ---------- | ---- | -------------- |
| At-most-once | None | Possible | Ack before processing; no retry |
| At-least-once | Possible | None if retention holds | Ack after processing; retry on failure |
| Exactly-once | None | None | Only within a transactional boundary |

For events and webhooks, **at-least-once is the practical default**. Senders retry on non-2xx (Stripe,
GitHub), brokers redeliver unacked messages (SQS, Kafka, RabbitMQ), and any crash between the effect
and the ack causes a duplicate.

"Exactly-once" for the consumer means **exactly-once processing**, achieved with a durable dedupe
key. It does not mean the event is delivered once.

## 33.5 — Duplicates

### Sources

- Sender retry after a timeout (webhook).
- Broker redelivery after an unacked message.
- Consumer rebalance / batch retry.
- DLQ replay.
- At-least-once producer (outbox relay).
- Manual operations (backfill, replay).

### Dedupe key

Choose a key that is **stable across deliveries** and **scoped to the effect**:

| Event source | Good key | Bad key |
| ------------ | -------- | ------- |
| Stripe webhook | `event.id` (`evt_...`) | `Date.now()` |
| Kafka record | `topic-partition-offset` or event `id` | Payload hash (changes with metadata) |
| Outbox | `outbox.id` | Random UUID at publish |
| Domain event | `aggregateId + version` | `aggregateId` alone (drops distinct versions) |

```ts
const key = `stripe:${event.id}`;

const inserted = await db.query(
  `INSERT INTO processed_events (key, type, received_at)
   VALUES ($1, $2, now())
   ON CONFLICT (key) DO NOTHING
   RETURNING key`,
  [key, event.type],
);

if (inserted.rowCount === 0) {
  metrics.increment("event_duplicate", { type: event.type });
  return; // already processed
}
```

### Dedupe must be durable and atomic with the effect

An in-memory `Set` or Redis key with a short TTL is **best-effort**. For money and entitlements, use
a unique constraint in the same database transaction as the effect:

```sql
BEGIN;
INSERT INTO processed_events (event_id) VALUES ($1) ON CONFLICT DO NOTHING;
-- if 0 rows, ROLLBACK and return
UPDATE subscriptions SET status = 'paid' WHERE id = $2;
COMMIT;
```

If the dedupe insert succeeds but the effect fails, the transaction rolls back and the event can be
retried. If the effect succeeds, the dedupe row is committed with it.

### Dedupe TTL

Events are not deduped forever in most systems:

- Stripe event ids are unique; you can retain them as long as your audit policy allows.
- Kafka offsets are unique per partition but a topic reset changes them.
- A 7–30 day TTL is common for non-financial events; financial events should be retained longer.

## 33.7 — Out-of-order events

Ordering guarantees are weaker than most people assume:

| System | Ordering guarantee |
| ------ | ------------------ |
| SQS standard | None |
| SQS FIFO | Per `MessageGroupId`, within a dedupe window |
| Kafka | Per partition only |
| RabbitMQ | Per queue with a single consumer; not across queues |
| Webhooks (Stripe) | **Not guaranteed**; retries can reorder |
| Pub/Sub | Per ordering key, if enabled |

### Two strategies

**A. Enforce order** by partitioning on an entity key and checking versions:

```ts
type Versioned = { aggregateId: string; version: number; type: string };

async function apply(event: Versioned) {
  const current = await projections.get(event.aggregateId);

  if (current && event.version <= current.version) {
    metrics.increment("event_stale", { type: event.type });
    return; // already applied or older
  }

  if (current && event.version > current.version + 1) {
    throw new TransientError("EVENT_GAP"); // reorder buffer / retry later
  }

  await projections.apply(event);          // idempotent upsert with version guard
}
```

**B. Tolerate disorder** by making events describe **facts with timestamps**, not incremental
mutations:

```text
❌ increment balance by 10      (order-dependent)
✅ set balance snapshot at t    (last-write-wins with timestamp/version)
```

Use an `updatedAt`/`version` guard so a late, older event cannot overwrite newer state:

```sql
UPDATE subscriptions
SET status = $2, version = $3
WHERE id = $1 AND version < $3;   -- ignore stale writes
```

### Gap detection

If versions arrive `1, 2, 4`, either:

- **buffer** event 4 until 3 arrives (with a timeout), or
- **refetch** the aggregate from the source of truth, or
- **fail transiently** and let redelivery fill the gap.

Choose based on how long the gap is likely to last and whether the projection can tolerate it.

## Worked example — WebhookIngest subscription state

Stripe sends `customer.subscription.created`, `.updated`, and `.deleted`, possibly out of order.
The old handler applied each event as it arrived; a delayed `.created` after `.deleted` reactivated a
canceled subscription.

```ts
async function applySubscriptionEvent(event: StripeEvent) {
  const sub = event.data.object as Stripe.Subscription;

  await db.transaction(async (tx) => {
    const seen = await tx.processedEvents.insertIfAbsent(event.id);
    if (!seen) return;                                  // duplicate

    const current = await tx.subscriptions.findByProviderId(sub.id);
    const incomingVersion = event.created;              // Stripe event timestamp

    if (current && current.providerVersion >= incomingVersion) return; // stale

    await tx.subscriptions.upsert({
      providerId: sub.id,
      status: mapStatus(sub.status),
      providerVersion: incomingVersion,
    });
  });
}
```

Now a duplicate is a no-op, and an older event cannot overwrite a newer one, regardless of arrival
order.

## Key data / numbers

- SQS standard: at-least-once, **no ordering**.
- SQS FIFO: ordering per `MessageGroupId`; dedupe window **5 minutes**.
- Kafka: ordering **per partition** only; `max.in.flight.requests.per.connection` can reorder on retry
  unless idempotence is enabled.
- Stripe webhook delivery order is **not guaranteed**; retries can arrive after newer events.
- Stripe event `created` is a Unix timestamp in seconds — useful as a coarse version.
- Common dedupe retention: **7–30 days** for non-financial, longer for payments.

## Real-world use case — Checkout

Checkout processed `payment_intent.succeeded` and `charge.refunded` in the same consumer. A refund
arrived before the success event due to a retry, so the order was marked refunded and then flipped
back to paid. They added a version guard using the Stripe event `created` timestamp and a per-order
state machine that rejected backward transitions. Late/out-of-order events became no-ops instead of
state corruption.

## Trade-offs

| Strategy | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| At-most-once | No duplicates | Loss | Telemetry only |
| At-least-once + dedupe | No loss, effectively once | Dedupe store | Default |
| Partition for order | Strong ordering | Hot partitions | Per-entity workflows |
| Version guard | Tolerates disorder | Requires versioning | Shared topics |
| Reorder buffer | Preserves order | Latency, memory | Strictly ordered streams |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Dedupe on the event's stable id | Dedupe on payload hash |
| Store dedupe durably | Use an in-memory set |
| Apply dedupe and effect atomically | Check then write in separate steps |
| Version-guard projections | Blindly upsert on every event |
| Treat stale events as no-ops | Apply them and regress state |
| Partition when order matters | Assume global order |

## Common mistakes

- **Dedupe TTL shorter than the retry window** — duplicates after expiry.
- **Dedupe by payload** — identical payloads with different ids are distinct facts.
- **Effect and dedupe in separate transactions** — crash between them either loses or duplicates.
- **Using event arrival time as version** — arrival order is exactly what is unreliable.
- **Assuming Stripe delivers in order** — it explicitly does not.

## Checklist

- [ ] Is the dedupe key stable and scoped to the effect?
- [ ] Is dedupe durable and committed with the effect?
- [ ] Is the dedupe TTL longer than the retry/replay window?
- [ ] Do projections carry a version/timestamp guard?
- [ ] Are stale/duplicate events recorded as metrics, not errors?
- [ ] Is ordering enforced by partition key where required?
- [ ] Are gaps detected and handled (buffer/refetch/retry)?

## Related

- [At-least-once and Idempotent Consumers — Mechanics](../02-deep-dive/02-at-least-once-and-idempotent-consumers.md)
- [Out-of-order Events and Versioning — Mechanics](../02-deep-dive/03-out-of-order-events-and-versioning.md)
- [WebhookIngest Dedupe and Signature](../03-practical-examples/01-webhookingest-dedupe-and-signature.md)
- [Chapter 28 — Idempotency](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
