# 01-concepts — Threads Basics

> Section 4 · Java · Threads Basics · _Estimated reading time: 25 min_

## What lives here

The **what**: how a thread is created and run, the six lifecycle states, and what each
synchronisation tool actually guarantees.

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-thread-lifecycle-and-creation.md](01-thread-lifecycle-and-creation.md) | 272 | `extends Thread` vs `implements Runnable`, `start()` vs `run()`, the 6 `Thread.State` values, the `Thread` method table, daemon threads, interruption and the interrupt flag, priorities, `Callable` and `Future`, `ExecutorService` |
| [02-synchronization-and-race-conditions.md](02-synchronization-and-race-conditions.md) | 285 | The race condition, the 3 `synchronized` forms and which monitor each locks, what `synchronized` guarantees, `volatile` vs `synchronized` vs `AtomicInteger`, the `wait()`/`notify()`/`notifyAll()` rules, deadlock and how to avoid it, thread-safe collections, `ThreadLocal`, `ExecutorService` factories |

## Read in this order

1. `01-thread-lifecycle-and-creation.md` — the thread half.
2. `02-synchronization-and-race-conditions.md` — the correctness half.

## Related

- [Topic overview](../README.md)
- [Techniques: thread interview techniques](../02-techniques/01-thread-interview-techniques.md)
