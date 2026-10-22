# Chapter 23 — Transaction and Rollback Error Handling

> Part IX · _Estimated reading time: 85–110 min_
> **Prerequisite:** [Chapter 22 — Database Error Classification](../22-database-error-classification/README.md)

## One-sentence summary

A transaction is a **promise about what can be undone**, and transaction error handling exists to
keep that promise when `COMMIT` fails, `ROLLBACK` fails, the connection dies mid-commit, or an
effect outside the database already happened.

## Why this chapter matters

The hardest database bugs are not failed queries — they are **uncertain commits**. A `23505` is
easy: don't retry. But if the connection drops after you send `COMMIT`, did the payment apply?
Retrying blindly double-charges; not retrying may lose the order. Add rollback failures,
savepoints, an external Stripe call, and a queue publish, and "just wrap it in a transaction"
stops being a strategy. This chapter gives you explicit policies for every outcome, including
the one where you genuinely cannot know.

## Chapter map

The chapter has 20 sections. They are grouped into these files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-transaction-boundaries-and-atomicity.md`](./01-concepts/01-transaction-boundaries-and-atomicity.md) | 23.1, 23.2 | Where a transaction starts/ends and what atomicity actually guarantees |
| [`01-concepts/02-commit-rollback-and-savepoints.md`](./01-concepts/02-commit-rollback-and-savepoints.md) | 23.3–23.6 | Commit failures, rollback failures, savepoints, partial completion |
| [`01-concepts/03-retry-eligibility-and-locking-strategies.md`](./01-concepts/03-retry-eligibility-and-locking-strategies.md) | 23.7–23.10 | What is retryable; deadlock retry; optimistic vs pessimistic locking |
| [`01-concepts/04-ambiguous-commits-and-idempotent-retries.md`](./01-concepts/04-ambiguous-commits-and-idempotent-retries.md) | 23.11–23.14 | Lost connection during commit, unknown outcomes, idempotency, duplicate side effects |
| [`01-concepts/05-after-commit-failures-outbox-and-cross-store.md`](./01-concepts/05-after-commit-failures-outbox-and-cross-store.md) | 23.15–23.20 | Post-commit failures, compensation, outbox, cross-store consistency, standards |
| [`02-deep-dive/01-ambiguous-commit-outcomes.md`](./02-deep-dive/01-ambiguous-commit-outcomes.md) | 23.11, 23.12, 23.19 | The mechanics of "did it commit?" and how to resolve it safely |
| [`02-deep-dive/02-outbox-mechanics-and-cross-store-consistency.md`](./02-deep-dive/02-outbox-mechanics-and-cross-store-consistency.md) | 23.16–23.18, 23.20 | Outbox table design, relay loop, `SKIP LOCKED`, compensation boundaries |
| [`03-practical-examples/01-retrying-40001-and-40p01.md`](./03-practical-examples/01-retrying-40001-and-40p01.md) | 23.7–23.9, 23.13 | Retry wrappers in TypeScript, Go, and Python for serialization/deadlock |
| [`03-practical-examples/02-outbox-and-compensation-in-code.md`](./03-practical-examples/02-outbox-and-compensation-in-code.md) | 23.15–23.17 | Checkout: commit + outbox, post-commit publish, compensation |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Transaction rules, anti-patterns, review checks |
| [`05-reference/README.md`](./05-reference/README.md) | all | Transaction failure guide, retry decision table, outbox checklist |

## Learning objectives

By the end you can:

- Place transaction boundaries so every unit of work is **atomic or explicitly compensated**.
- Explain what a **commit failure**, **rollback failure**, and **lost connection during commit**
  each mean — and which ones are safe to retry.
- Write a retry wrapper that retries the **whole transaction** on `40001`/`40P01`, re-reads
  state, and is safe for non-idempotent side effects.
- Design a **transactional outbox** and explain why it beats "commit then publish".
- Resolve an **ambiguous commit** by reading back a unique marker instead of guessing.

## Key takeaways

1. **Atomicity stops at the database.** Stripe, S3, email, and queue publishes are outside it.
2. **`COMMIT` can succeed and still look like a failure.** Treat "unknown" as a distinct state.
3. **Retry is per transaction, not per statement.** `40001`/`40P01` poison the whole unit of work.
4. **Never retry a non-idempotent write blindly** — make it idempotent first (key, unique marker,
   or read-back).
5. **The outbox is the default** for "change data + tell the world" in one atomic step.
6. **Compensation is business logic**, not rollback: it must be idempotent and observable.

## Exercises

1. List every effect your checkout performs and mark which are inside the DB transaction.
2. Simulate a dropped connection after `COMMIT` is sent (kill the socket) and see what your code
   reports. Fix it to a defined outcome.
3. Add an `outbox` table to one flow; publish from a relay; verify no event is lost when the
   relay crashes between read and publish.
4. Write a test that forces a `40001` (two concurrent `SERIALIZABLE` transactions) and asserts
   exactly one retry succeeds and no duplicate row exists.

## Related

- [Chapter 22 — Database Error Classification](../22-database-error-classification/README.md)
- [Chapter 24 — Repository and Data Access Error Handling](../24-repository-and-data-access-error-handling/README.md)
- [Partial Failures and Multi-Step Operations (Ch. 39)](../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
- [Idempotency and Duplicate-Operation Safety (Ch. 28)](../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
