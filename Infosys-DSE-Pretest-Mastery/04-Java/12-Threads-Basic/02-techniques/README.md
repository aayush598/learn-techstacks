# 02-techniques — Threads Basics

> Section 4 · Java · Threads Basics · _Estimated reading time: 9 min_

## What lives here

The **how**: six tables that turn any thread question into a lookup, and the 60-second procedure
that makes you **strike out** every order-dependent claim before you answer.

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-thread-interview-techniques.md](01-thread-interview-techniques.md) | 190 | Table 1 the 4 question types, Table 2 thread safety, Table 3 which method throws what, Table 4 `sleep()` vs `wait()`, Table 5 the guaranteed-statement checklist, Table 6 thread states, the 6-step 60-second procedure, a worked example |

## The 6 steps

1. Output question? → Table 5. Keep only the guaranteed statements.
2. "Which is thread-safe?" → Table 2.
3. "Which throws what?" → Table 3 (+ Table 4 for `sleep`/`wait`).
4. Thread state? → Table 6.
5. Lifecycle or interruption? → `start()` vs `run()`, daemon rules, the interrupt flag.
6. Sanity check: did you promise an ordering? Remove it.

## Related

- [Topic overview](../README.md)
- [Concepts: synchronization and race conditions](../01-concepts/02-synchronization-and-race-conditions.md)
