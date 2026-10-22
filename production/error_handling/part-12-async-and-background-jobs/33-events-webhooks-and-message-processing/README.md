# Chapter 33 — Events, Webhooks, and Message Processing

> Part XII · _Estimated reading time: 60–80 min_
> **Prerequisite:** [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../32-background-jobs-queues-and-scheduled-tasks/README.md)

## One-sentence summary

Events and webhooks are **messages from someone else's failure domain**: they arrive late, twice,
out of order, unsigned, or not at all — so consumers must verify, deduplicate, ack explicitly, and
converge on the correct state despite the transport, not because of it.

## Why this chapter matters

Inbound events are the integration surface where correctness is hardest to see. Stripe retries a
webhook three times; your handler runs three times. Kafka redelivers a batch after a rebalance; half
your projections are already written. A schema changes upstream; your consumer throws on every
message and the partition stalls. Every one of these is normal operation, not an edge case. This
chapter teaches the consumer contracts that make "normal operation" safe: **signature verification,
idempotency, ack/reject, ordering, schema versioning, and dead-letter replay**.

## Chapter map

The chapter has 18 sections grouped into twelve files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-publish-and-consume-failures.md`](./01-concepts/01-publish-and-consume-failures.md) | 33.1–33.3, 33.18 | Publish vs consume failures, ack/reject, preventing message loss |
| [`01-concepts/02-delivery-guarantees-duplicates-and-ordering.md`](./01-concepts/02-delivery-guarantees-duplicates-and-ordering.md) | 33.4, 33.5, 33.7 | At-most/at-least-once, duplicates, out-of-order events |
| [`01-concepts/03-schema-validation-and-versioning.md`](./01-concepts/03-schema-validation-and-versioning.md) | 33.8, 33.9 | Schema validation, version incompatibility |
| [`01-concepts/04-webhook-signatures-retries-timeouts.md`](./01-concepts/04-webhook-signatures-retries-timeouts.md) | 33.10–33.12 | Signature errors, sender retries, webhook timeouts |
| [`01-concepts/05-consumer-isolation-and-eventual-consistency.md`](./01-concepts/05-consumer-isolation-and-eventual-consistency.md) | 33.6, 33.13–33.17 | Poison events, isolation, DLQ, partial batch, eventual consistency, compensation |
| [`02-deep-dive/01-webhook-signature-verification.md`](./02-deep-dive/01-webhook-signature-verification.md) | 33.10 (mechanics) | HMAC, timestamp tolerance, raw body, constant-time compare |
| [`02-deep-dive/02-at-least-once-and-idempotent-consumers.md`](./02-deep-dive/02-at-least-once-and-idempotent-consumers.md) | 33.4–33.5 (mechanics) | Delivery guarantees and consumer dedupe |
| [`02-deep-dive/03-out-of-order-events-and-versioning.md`](./02-deep-dive/03-out-of-order-events-and-versioning.md) | 33.7–33.9 (mechanics) | Sequence numbers, version negotiation, upcasting |
| [`03-practical-examples/01-webhookingest-dedupe-and-signature.md`](./03-practical-examples/01-webhookingest-dedupe-and-signature.md) | 33.5, 33.10–33.12 | A complete webhook endpoint |
| [`03-practical-examples/02-event-consumer-partial-batch-and-dlq.md`](./03-practical-examples/02-event-consumer-partial-batch-and-dlq.md) | 33.13–33.15 | Batch consumer with per-record failure reporting |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Consumer rules and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Event/webhook contracts, ack matrix, glossary |

## Learning objectives

By the end you can:

- Distinguish a **publish** failure from a **consume** failure and place the boundary correctly.
- Explain at-most-once, at-least-once, and effectively-once for messages and webhooks.
- Verify a **Stripe-style signature** with timestamp tolerance and constant-time comparison.
- Deduplicate events durably and design idempotent consumers.
- Handle **out-of-order** delivery with sequence/version checks.
- Validate schemas and tolerate **version incompatibility**.
- Report **partial batch failures** so only failed records are retried.
- Design for **eventual consistency** and downstream compensation.

## Key takeaways

1. **The sender's retry is your duplicate.** Every consumer needs a durable dedupe key derived from
   the event, not the delivery.
2. **Ack semantics are a contract.** Ack only after durable processing; reject to retry; never ack a
   transient failure to "clear the queue."
3. **A 2xx webhook response is a promise.** Return it after the event is durably recorded, not after
   the business logic finishes.
4. **Ordering is not guaranteed** unless you explicitly partition and sequence; design consumers to
   be order-tolerant or order-enforcing.
5. **Schema versioning is part of the error contract**, not an afterthought. Unknown versions must
   fail predictably, not crash the partition.
6. **Eventual consistency is the default**, so every user-visible read must tolerate a lagging
   projection.

## Exercises

1. Take one inbound webhook and write down its signature header, timestamp tolerance, and dedupe key.
2. Send the same event twice and prove the second is a no-op at the database level.
3. Reorder two events for the same entity and verify the consumer does not regress state.
4. Add a `v2` schema with a new required field and define the consumer's behavior for `v1` and
   unknown versions.
5. Configure a partial-batch response for a 10-record batch with 2 failures and verify only those 2
   are retried.
6. Write the compensation action for an event that has already been projected downstream.

## Related

- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../32-background-jobs-queues-and-scheduled-tasks/README.md)
- [Chapter 28 — Idempotency](../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Chapter 31 — Detached Failures and Async Cleanup](../31-asynchronous-error-handling/01-concepts/05-async-cleanup-and-detached-failures.md)
- [Webhook Signature Verification — Mechanics](./02-deep-dive/01-webhook-signature-verification.md)
- [Glossary](../../GLOSSARY.md)
