# Part 5: Deadlocks

> **TL;DR**: A deadlock is a permanent state where every thread waits for a resource another thread holds — no progress possible. Deadlocks need 4 conditions (ME, hold-and-wait, no preemption, circular wait); systems prevent them (break a condition), avoid them (safe-state checks like Banker's), detect them (wait-for cycles) and recover (kill/rollback).

## What You'll Learn
- The four necessary conditions and how to recognize a deadlock on sight.
- Resource allocation graphs and how cycles = deadlock (for single-instance resources).
- The three strategies: prevention, avoidance (Banker's algorithm), detection + recovery.
- How real systems (Linux, databases, distributed systems) actually handle deadlocks.

## Prerequisites
- Part 04 (locks, semaphores, all the primitives deadlocks involve).
- Part 03 (scheduling/waiting interacts with lock acquisition).
