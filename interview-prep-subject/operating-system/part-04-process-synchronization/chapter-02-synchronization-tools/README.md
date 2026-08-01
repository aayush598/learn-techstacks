# Chapter 2: Synchronization Tools (Primitives)

> **TL;DR**: The practical synchronization toolbox: mutexes (exclusive ownership), semaphores (counting/down-up), condition variables (wait/signal for state), monitors (language-level encapsulation), and spinlocks/read-write locks (specialized fast paths). Choosing the right primitive is as important as knowing how they work.

## Sections
| Section | Topic | Key Idea |
|---|---|---|
| 01 | Mutexes & Locks | Exclusive ownership; fast path + sleep; PI |
| 02 | Semaphores | Counting/down-up; sync + mutual exclusion |
| 03 | Condition Variables | Wait/signal for state predicates |
| 04 | Monitors | Encapsulated methods with implicit lock |
| 05 | Spinlocks & RW Locks | Spin vs sleep; many-reader/single-writer |

## What You'll Learn
- The semantics, implementation, and pitfalls of each primitive.
- Mutex vs semaphore vs spinlock — when to use which.
- How condition variables must be used with a predicate and a mutex.
- How monitor semantics map to Java/C#.

## Prerequisites
- Part 04 Ch 1 (critical section, TAS/CAS).
- Part 02 (threads sharing memory).
- Part 03 (scheduling interacts with lock waiting).
