# Chapter 14 — Resource Cleanup and Failure-Safe Execution

> Part V · _Estimated reading time: 55–75 min_
> **Prerequisite:** [Chapter 13 — Catch Blocks and Recovery Logic](../13-catch-blocks-and-recovery-logic/README.md)

## One-sentence summary

Every resource you **acquire** — connection, transaction, file, stream, lock, temp file — must be
**released on every path**, including the failure path, and when cleanup itself fails you must
**preserve the primary error** rather than let the cleanup error replace it.

## Why this chapter matters

Leaks are the slowest, most insidious production failure. A connection not returned exhausts a
pool hours later; a lock not released deadlocks a system; a temp file not deleted fills a disk
days later. None of these happen on the happy path — they happen *because something failed*, and
the cleanup code assumed success. Failure-safe execution means the cleanup is **structural**, not
dependent on reaching the end of the function.

## Chapter map

The chapter has 18 sections, grouped into 11 files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-acquire-release-and-guaranteed-cleanup.md`](./01-concepts/01-acquire-release-and-guaranteed-cleanup.md) | 14.1, 14.2, 14.3, 14.4 | Acquire/release, guaranteed cleanup, `finally`, scoped management |
| [`01-concepts/02-cleanup-for-common-resources.md`](./01-concepts/02-cleanup-for-common-resources.md) | 14.5, 14.6, 14.7, 14.8, 14.9 | DB connections, transactions, files, streams, network |
| [`01-concepts/03-locks-semaphores-and-temporary-resources.md`](./01-concepts/03-locks-semaphores-and-temporary-resources.md) | 14.10, 14.11 | Locks/semaphores and temporary resources |
| [`01-concepts/04-multiple-errors-and-primary-preservation.md`](./01-concepts/04-multiple-errors-and-primary-preservation.md) | 14.12, 14.13 | Multiple simultaneous errors; preserving the primary |
| [`01-concepts/05-cleanup-timeouts-cancellation-and-idempotency.md`](./01-concepts/05-cleanup-timeouts-cancellation-and-idempotency.md) | 14.14, 14.15, 14.16, 14.17, 14.18 | Cleanup timeouts, cancellation-safe, idempotent cleanup, preventing leaks, universal policy |
| [`02-deep-dive/01-scoped-cleanup-mechanics.md`](./02-deep-dive/01-scoped-cleanup-mechanics.md) | mechanics | `try/finally`, `using`, `defer`, context managers, RAII |
| [`02-deep-dive/02-primary-vs-secondary-errors.md`](./02-deep-dive/02-primary-vs-secondary-errors.md) | mechanics | Suppressed errors, before/after traces, Java `addSuppressed` |
| [`03-practical-examples/01-try-finally-and-using-patterns.md`](./03-practical-examples/01-try-finally-and-using-patterns.md) | 14.1–14.9 | try/finally, try-with-resources, `using` patterns |
| [`03-practical-examples/02-defer-context-managers-and-cancellation-safe.md`](./03-practical-examples/02-defer-context-managers-and-cancellation-safe.md) | 14.10–14.18 | Go `defer`, Python `with`, cancellation-safe cleanup |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules of thumb and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Cleanup decision table, resource checklist, glossary |

## Learning objectives

By the end you can:

- Structure code so release happens on success, failure, cancellation, and timeout.
- Use `finally`, `using` / try-with-resources, `defer`, and context managers correctly.
- Preserve the primary error when cleanup fails, attaching the cleanup error as suppressed.
- List and eliminate the leak paths in a service.

## Key takeaways

1. **Acquire and release in the same scope.** The frame that acquires owns the release (14.1–14.4).
2. **Cleanup is structural, not habitual.** Use the language's scope mechanism; never rely on
   reaching the last line (14.3–14.4).
3. **Cleanup runs on the failure path too** — and can fail there. Preserve the primary error
   (14.12–14.13).
4. **Cleanup must be fast, cancellation-safe, and idempotent.** A slow or fragile cleanup is a new
   outage (14.14–14.16).
5. **One universal policy.** Same rules for every resource type (14.18).

## Exercises

1. List every resource acquired in one service and its release site; find paths with no release.
2. Introduce a failure mid-function and confirm cleanup still runs.
3. Make a cleanup that throws; verify the primary error is not lost.

## Related

- [Chapter 13 — Catch Blocks and Recovery Logic](../13-catch-blocks-and-recovery-logic/README.md)
- [Chapter 12 — Exception Propagation and Control Flow](../12-exception-propagation-and-control-flow/README.md)
- [Transaction and Rollback Error Handling (Part IX)](../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
- [Glossary: cleanup, leak, suppressed error](../../GLOSSARY.md)
