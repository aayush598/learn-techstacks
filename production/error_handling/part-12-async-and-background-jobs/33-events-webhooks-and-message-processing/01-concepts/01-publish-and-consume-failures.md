# Publish and Consume Failures, Ack/Reject, and Preventing Loss

> Part XII · Chapter 33 · Sections 33.1–33.3, 33.18 · _Estimated reading time: 18 min_
> **Prerequisite:** [Chapter 32 — Background Jobs](../../32-background-jobs-queues-and-scheduled-tasks/README.md)

## In one sentence

A message pipeline has **two failure surfaces** — the publisher (did the event leave?) and the
consumer (did the event land?) — and preventing loss means knowing which side you are on before
choosing to retry, ack, or reject.

## Why this matters in production

Teams debug message loss for days because they cannot tell whether the event was never published or
published and then dropped by the consumer. The two failures have different fixes: a publish failure
needs an **outbox or publisher retry**, a consume failure needs **ack/reject discipline and a DLQ**.
Conflating them produces "we'll just retry the consumer" for an event that never existed.

## 33.1 — Publish failures

Publishing can fail before the broker accepts the message:

| Failure | Cause | Handling |
| ------- | ----- | -------- |
| Connection refused / DNS | Broker unreachable | Retry with backoff |
| Timeout / no ack | Publish ambiguous | Retry with idempotency key |
| Auth failure | Bad credentials | Terminal; alert |
| Message too large | Payload exceeds limit | Split or use claim-check (S3 pointer) |
| Throttling (`429`) | Producer rate limit | Backoff, honor `Retry-After` |
| Serialization error | Unserializable payload | Terminal; fix producer |

The hard case is the **ambiguous publish**: the broker may have accepted the message but the ack was
lost. Retrying can duplicate. Solve it with a **deterministic message id** so the broker or consumer
can dedupe.

### Transactional outbox

Never write the database and publish in two separate steps without an outbox:

```text
❌  BEGIN; INSERT order; COMMIT; publish event;   ← crash between commit and publish = lost event

✅  BEGIN; INSERT order; INSERT outbox(event); COMMIT;
    relay: SELECT outbox → publish → mark sent   ← at-least-once, replayable
```

```sql
CREATE TABLE outbox (
  id           uuid PRIMARY KEY,
  topic        text NOT NULL,
  payload      jsonb NOT NULL,
  created_at   timestamptz NOT NULL DEFAULT now(),
  published_at timestamptz
);

-- Relay loop claims unpublished rows with SKIP LOCKED, publishes, then marks them.
SELECT * FROM outbox
WHERE published_at IS NULL
ORDER BY created_at
FOR UPDATE SKIP LOCKED
LIMIT 100;
```

The relay publishes at-least-once; the event id (`outbox.id`) becomes the consumer's dedupe key.

## 33.2 — Consume failures

Consume failures happen after the message is delivered:

| Failure | Example | Classification |
| ------- | ------- | -------------- |
| Transient dependency | DB down, provider `503` | Retry |
| Handler bug | `TypeError`, null deref | Terminal → DLQ + alert |
| Invalid payload | Schema mismatch | Terminal → DLQ |
| Unknown event type | New upstream type | Terminal (quarantine) or ignore |
| Poison combination | One tenant triggers an edge case | Terminal → DLQ |
| Batch partial | 2 of 10 records invalid | Per-record failure report |

The consumer must **classify before acking**. Acking a transient failure loses the event; rejecting a
terminal failure loops it forever.

## 33.3 — Ack / reject

Ack (commit, delete, settle) tells the broker "done, do not redeliver." Reject (nack, negative-ack,
`batchItemFailures`) tells it "not done, redeliver or dead-letter."

| Broker | Ack | Reject / retry | Dead-letter |
| ------ | --- | -------------- | ----------- |
| SQS | `DeleteMessage` | Do not delete (visibility expiry) | Redrive policy |
| Kafka | `commitSync` offset | Do not commit / seek back | App-level DLQ topic |
| RabbitMQ | `basic.ack` | `basic.nack(requeue=true)` | Dead-letter exchange |
| Pub/Sub | `ack()` | `nack()` | Dead-letter topic |
| HTTP webhook | `2xx` | Non-2xx | Sender's retry policy |

### The ack contract

1. **Ack only after the effect is durable.** Ack-before-write loses on crash.
2. **Ack-after-write can duplicate** on crash before ack — make the effect idempotent.
3. **Never ack a transient failure** to keep the queue clean.
4. **Never reject a permanent failure** without a DLQ; it will loop.
5. **Ack the batch only when all records succeed**, or report per-record failures (33.15).

```ts
async function consume(message: Message) {
  try {
    await projector.apply(message);   // durable effect
    await broker.ack(message);        // then ack
  } catch (err) {
    if (isTransient(err)) {
      await broker.nack(message, { requeue: true }); // redeliver
    } else {
      await dlq.publish(message, err);
      await broker.ack(message);                     // remove from main queue
    }
  }
}
```

> ⚠️ **Hazard.** `nack(requeue=true)` without a retry limit is an infinite loop. Use a receive count,
> a retry topic, or a dead-letter exchange.

## 33.18 — Preventing message loss

Loss happens at five seams. Close each one:

| Seam | Loss mode | Control |
| ---- | --------- | ------- |
| Producer → DB | Order saved, event not published | Transactional outbox |
| Producer → broker | Publish ambiguous, no retry | Publisher confirms + deterministic id |
| Broker retention | Consumer down longer than retention | Retention > max outage; alarms on lag |
| Consumer → DB | Ack before durable write | Ack-after-commit |
| Consumer → DLQ | Reject without DLQ | DLQ on every queue/topic |

Also guard against **silent filtering**: a consumer that ignores unknown event types without
recording them loses data invisibly. Either DLQ unknown types or emit a metric for each one.

```ts
const HANDLED = new Set(["invoice.paid", "invoice.failed", "subscription.updated"]);

if (!HANDLED.has(event.type)) {
  await unknownEvents.record(event);   // observable, replayable
  metrics.increment("event_unhandled", { type: event.type });
  return;                              // ack: deliberately ignored, not lost
}
```

## Worked example — Checkout order events

Checkout writes an order and publishes `order.created` for downstream fulfillment.

```ts
// ❌ Lost event if the process dies between commit and publish.
await db.orders.insert(order);
await bus.publish("order.created", order);

// ✅ Outbox: the event is committed with the order.
await db.transaction(async (tx) => {
  await tx.orders.insert(order);
  await tx.outbox.insert({ id: order.eventId, topic: "order.created", payload: order });
});

// Relay (separate process):
for (const row of await outbox.claimBatch()) {
  await bus.publish(row.topic, row.payload, { messageId: row.id }); // deterministic id
  await outbox.markPublished(row.id);
}
```

The consumer dedupes on `messageId = order.eventId`; a relay crash after publish but before
`markPublished` causes a redelivery that is safely ignored.

## Key data / numbers

- SQS maximum message size: **256 KiB**; larger payloads need the claim-check pattern (S3 pointer).
- SQS message retention: default **4 days**, max **14 days**.
- Kafka topic retention is time/size based; a consumer lagging past it loses data permanently.
- RabbitMQ publisher confirms should be enabled; without them, publish success is unverified.
- HTTP webhook success is **any 2xx**; Stripe treats non-2xx as a failed delivery and retries.
- Pub/Sub ack deadline default **10 s**, max **600 s**; extend for long handlers.

## Real-world use case — Acme SaaS

Acme published `tenant.deleted` after committing the delete. A deploy killed the process between
the commit and the publish; the tenant's S3 objects and search documents were never cleaned up.
Because there was no outbox and no publish confirmation, the event was simply gone. They moved to a
transactional outbox with a relay that publishes `tenant.deleted` at-least-once, and the cleanup
consumer became idempotent (deleting an already-deleted object is a no-op). No tenant deletion has
leaked resources since.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Publish after commit | Simple | Loses events on crash | Non-critical notifications |
| Outbox + relay | No loss, replayable | Extra table/process | Any state-changing event |
| Publish inside DB txn | Atomic in some DBs | Not portable | Rare, DB-specific |
| Ack before effect | Fast | Loses on crash | Never |
| Ack after effect | Durable | Duplicates | Default with idempotency |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use an outbox for state-changing events | Publish after commit with no recovery |
| Give every message a deterministic id | Let the broker generate a new id per retry |
| Ack after durable processing | Ack first and process later |
| Reject transient failures | Ack them to clear the queue |
| DLQ permanent failures | Requeue forever |
| Record unknown event types | Silently ignore them |

## Common mistakes

- **Missing outbox** — committed state without its event.
- **Publish retry with a new message id** — duplicates the consumer cannot detect.
- **Ack-before-write** — lost work on crash.
- **No DLQ on reject** — one bad event blocks the partition.
- **Ignoring unknown types without a metric** — invisible data loss.

## Checklist

- [ ] Are state-changing events written through an outbox?
- [ ] Does every message have a deterministic id?
- [ ] Is the consumer acking only after a durable effect?
- [ ] Are transient failures rejected and permanent ones dead-lettered?
- [ ] Does every queue/topic have a DLQ?
- [ ] Is retention longer than the longest expected consumer outage?
- [ ] Are unknown event types recorded and measured?

## Related

- [Delivery Guarantees, Duplicates, and Ordering](./02-delivery-guarantees-duplicates-and-ordering.md)
- [At-least-once and Idempotent Consumers — Mechanics](../02-deep-dive/02-at-least-once-and-idempotent-consumers.md)
- [Chapter 23 — Transaction and Rollback Error Handling](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
- [Chapter 33 Reference](../05-reference/README.md)
