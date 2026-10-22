# Chapter 28 — Idempotency and Duplicate-Operation Safety

> Part XI · _Estimated reading time: 80–100 min_
> **Prerequisite:** [Chapter 27 — Retry Policies](../27-retry-policies/README.md)

## One-sentence summary

An operation is **idempotent** when performing it N times has the same effect as performing it once;
an **idempotency key** is the client-supplied token that lets a server detect duplicates, replay the
original result, and make retries safe even when the first attempt already succeeded.

## Why this chapter matters

Retries are mandatory (Chapter 27), and every retry is a duplicate waiting to happen. Networks lose
responses after the server succeeded; queues redeliver; users double-click; webhooks arrive twice.
Without idempotency, each of those becomes a double charge, a duplicated project, or a second export.
With it, retrying becomes boring — which is exactly what you want. The cost is a small amount of
state and a very precise lifecycle for the key.

## Chapter map

The chapter has 16 sections. They are grouped into these files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-what-idempotency-means.md`](./01-concepts/01-what-idempotency-means.md) | 28.1–28.3 | Definition, why retries need it, idempotent vs not, the ambiguous-success problem |
| [`01-concepts/02-idempotency-keys-and-duplicate-detection.md`](./01-concepts/02-idempotency-keys-and-duplicate-detection.md) | 28.4–28.9 | Keys, detection, storage/TTL, concurrent same-key requests, replay, reused key with a different payload |
| [`01-concepts/03-failure-contracts-and-uncertain-outcomes.md`](./01-concepts/03-failure-contracts-and-uncertain-outcomes.md) | 28.10, 28.15, 28.16 | What a failed attempt records, unknown outcomes, preventing duplicate billing/creation |
| [`01-concepts/04-idempotency-in-payments-jobs-and-webhooks.md`](./01-concepts/04-idempotency-in-payments-jobs-and-webhooks.md) | 28.11–28.14 | Payments, jobs, webhooks, and distributed idempotency |
| [`02-deep-dive/01-idempotency-key-lifecycle.md`](./02-deep-dive/01-idempotency-key-lifecycle.md) | 28.4–28.10 | The full key state machine: acquired → in-progress → completed/failed → expired |
| [`02-deep-dive/02-distributed-idempotency-and-storage.md`](./02-deep-dive/02-distributed-idempotency-and-storage.md) | 28.6, 28.14, 28.15 | Storage choices, races, TTL, and cross-service keys |
| [`03-practical-examples/01-idempotency-key-store.md`](./03-practical-examples/01-idempotency-key-store.md) | 28.4–28.9 | A Postgres-backed key store with concurrency and 24h TTL |
| [`03-practical-examples/02-checkout-and-webhook-idempotency.md`](./03-practical-examples/02-checkout-and-webhook-idempotency.md) | 28.11–28.13, 28.16 | Checkout charges, `ExportJob`, and `WebhookIngest` in practice |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Key, storage, and replay rules; anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Key lifecycle table, TTL defaults, status mapping, decision guide |

## Learning objectives

By the end you can:

- Distinguish idempotent operations from merely "safe to call twice by luck."
- Design an idempotency key contract: who generates it, its scope, its TTL, and its payload hash.
- Handle concurrent requests with the same key without double-writing.
- Replay a stored success, including the original status and body.
- Define what a failed attempt records and how an unknown outcome is resolved.
- Apply idempotency to payments, jobs, webhooks, and multi-service workflows.

## Key takeaways

1. **Exactly-once delivery is a myth; exactly-once *effect* is achievable** with at-least-once
   delivery plus idempotency.
2. **The key must be stable across retries.** Generating a new key per attempt defeats the purpose.
3. **Store the result, not just a lock.** A duplicate request must receive the original response.
4. **Concurrency needs a unique constraint**, not a read-then-write check.
5. **Hash the payload.** A reused key with different content is a client bug and must be rejected.
6. **A key TTL is a business decision** (commonly 24h); retention must cover the retry window.
7. **Unknown outcomes require reconciliation**, not a blind retry.

## Exercises

1. List every write endpoint in your API and mark which ones need an idempotency key.
2. Write the state machine for a key: what happens on a second request while the first is in flight?
3. Choose a TTL for a payment key and justify it against your retry and reconciliation windows.
4. Simulate two concurrent requests with the same key and verify only one side effect occurs.
5. Take a webhook handler and make it idempotent by event id.

## Related

- [Chapter 27 — Retry Policies](../27-retry-policies/README.md)
- [Chapter 23 — Transaction and Rollback Error Handling](../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
- [Chapter 33 — Events, Webhooks, and Message Processing](../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
- [Glossary](../../GLOSSARY.md)
