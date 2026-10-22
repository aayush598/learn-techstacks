# 03-worked-examples — Threads Basics

> Section 4 · Java · Threads Basics · _Estimated reading time: 22 min_

## What lives here

10 fully solved thread questions. Wherever the output order is not deterministic, the answer is the
**guaranteed** statement, and the breakdown says so explicitly.

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-solved-threads-set.md](01-solved-threads-set.md) | 436 | 10 questions: `start()` vs `run()`, the guaranteed-statement pattern, `join()` semantics, `volatile` vs `synchronized` vs `AtomicInteger`, `sleep()` vs `wait()`, `wait()` without the lock, daemon threads, thread states, interruption, race conditions |

## The questions at a glance

| Q | Archetype | Answer |
|---|---|---|
| Q1 | `start()` vs `run()` | `main` then `Thread-0` |
| Q2 | the guaranteed-statement pattern | `A`/`B` in either order; `C` always last |
| Q3 | `join()` semantics | `child` then `parent`, always |
| Q4 | what is not enough for a thread-safe counter | `volatile` alone |
| Q5 | `sleep()` vs `wait()` | `sleep()` keeps the lock; `wait()` releases it |
| Q6 | `wait()` without the lock | `IMSE` |
| Q7 | daemon threads | the program exits immediately |
| Q8 | thread states | `NEW` then `TERMINATED` |
| Q9 | interruption | `interrupted` is printed |
| Q10 | race condition | at most `2000`, possibly less |

## Related

- [Topic overview](../README.md)
- [Thread traps](../04-pitfalls/01-thread-traps.md)
