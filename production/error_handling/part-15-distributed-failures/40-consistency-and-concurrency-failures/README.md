# Chapter 40 — Consistency and Concurrency Failures

> Part XV · _Estimated reading time: 70–95 min_
> **Prerequisite:** [Chapter 22 — Database Error Classification](../../part-09-database-and-transactions/22-database-error-classification/README.md)

## One-sentence summary

Concurrency failures — races, **lost updates**, **version conflicts**, **deadlocks**, expired
leases, and stale replicas — are not anomalies to be prevented but *normal contention to be
detected and resolved*, and the only unforgivable outcome is **silent corruption**.

## Why this chapter matters

Every one of these failures looks like a small bug and lands like data loss: two editors save and
one overwrite is gone; two requests create the same subscription; a nightly job writes through a
stale read; a worker keeps writing after its lease expired and the next worker has already taken
over. The database will often *tell* you — `HTTP 409`, `SQLSTATE 40001`/`40P01` — and most
application code converts that truth into a `500` or, worse, ignores it and commits anyway. This
chapter is about hearing the signal and answering it correctly.

## Chapter map

The chapter has 15 sections grouped into nine files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-races-optimistic-control-and-version-conflicts.md`](./01-concepts/01-races-optimistic-control-and-version-conflicts.md) | 40.1–40.3 | What a race is, optimistic concurrency control, version conflicts |
| [`01-concepts/02-lock-contention-deadlocks-and-duplicate-requests.md`](./01-concepts/02-lock-contention-deadlocks-and-duplicate-requests.md) | 40.4–40.7 | Lock contention, deadlock detection and recovery, concurrent duplicates |
| [`01-concepts/03-lost-updates-stale-reads-and-conflicting-writes.md`](./01-concepts/03-lost-updates-stale-reads-and-conflicting-writes.md) | 40.8, 40.9 | Lost updates, stale reads, conflicting writes and how to prove them |
| [`01-concepts/04-distributed-locks-fencing-and-replicas.md`](./01-concepts/04-distributed-locks-fencing-and-replicas.md) | 40.10–40.12 | Leases, lease expiry, fencing tokens, replica consistency |
| [`01-concepts/05-conflict-resolution-retry-safety-and-corruption.md`](./01-concepts/05-conflict-resolution-retry-safety-and-corruption.md) | 40.13–40.15 | Conflict resolution strategies, retry safety, preventing corruption |
| [`02-deep-dive/01-optimistic-concurrency-vs-deadlock.md`](./02-deep-dive/01-optimistic-concurrency-vs-deadlock.md) | 40.2, 40.3, 40.5 (mechanics) | OCC vs pessimistic locking, wait-die/wound-wait, deadlock internals |
| [`03-practical-examples/01-optimistic-locking-with-version-column.md`](./03-practical-examples/01-optimistic-locking-with-version-column.md) | 40.2, 40.3, 40.8 | A version column end-to-end: SQL, repository, HTTP `409`, client retry |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Concurrency rules and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Conflict decision tables, SQLSTATE/status-code map, glossary |

## Learning objectives

By the end you can:

- Reproduce a **lost update** and a **race condition** and explain why the test that caught them
  must run two real sessions, not a mock.
- Choose **optimistic** vs **pessimistic** concurrency for a specific write path and defend it with
  the contention you observe.
- Detect deadlocks, classify them as **retryable** (`40001`/`40P01`, MySQL `1213`), and bound the
  retries safely.
- Answer **concurrent duplicate** requests with `409` + idempotency, not with hope.
- Design a **distributed lease** that survives expiry — including **fencing tokens**, the part
  everyone skips.
- Map every conflict to a client-actionable response (`409`, `412`, `202`) and never to a bare
  `500`.

## Key takeaways

1. **Conflicts are data, not defects.** `409`, `40001`, and `40P01` mean "you are not alone";
   the defect is committing over them.
2. **Optimistic control is a version number plus a guarded `UPDATE ... WHERE version = $1`.**
   Zero rows updated is a conflict — read the row count, always.
3. **Retry only what is safe.** Deadlock retries re-run the whole transaction with fresh reads;
   conflict retries require re-applying the user's intent on top of the new state.
4. **A lease without a fencing token is a rumor.** After expiry, the old holder can still write;
   only a monotonically increasing token checked by the storage layer stops it.
5. **Reads are writes' inputs.** A stale read feeding a write corrupts just as effectively as two
   writers racing — use read-your-writes and verify preconditions at commit time.

## Exercises

1. Take your hottest row (counter, quota, balance). Write down every code path that updates it and
   classify each as lost-update-prone.
2. Reproduce a deadlock with two real psql/`mysql` sessions; capture the victim's SQLSTATE and
   confirm your retry wrapper recovers.
3. Implement a `version` column on one table and deliberately send two concurrent `PUT`s. Verify
   the loser gets `409` and can retry safely.
4. Audit one distributed lock in your system: what happens if the holder pauses past the lease?
   Where would a fencing token be checked?
5. List every place your code writes based on a read from a replica. Which of those are unsafe?

## Related

- [Chapter 39 — Partial Failures and Multi-Step Operations](../39-partial-failures-and-multi-step-operations/README.md)
- [Chapter 41 — Process, Runtime, and Resource Failures](../41-process-runtime-and-resource-failures/README.md)
- [Chapter 23 — Transaction and Rollback Error Handling](../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
- [Chapter 28 — Idempotency and Duplicate-Operation Safety](../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Glossary: optimistic concurrency, fencing token](../../GLOSSARY.md)
