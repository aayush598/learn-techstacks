# Chapter 3: Classical Synchronization Problems

> **TL;DR**: The four canonical problems — bounded-buffer (producer-consumer), dining philosophers, readers-writers, and sleeping barber — encode the core synchronization traps: buffer capacity, deadlock via resource ordering, starvation between readers/writers, and correct wait-when-nobody-ready. Mastering them means mastering every locking pattern.

## Sections
| Section | Topic | Key Idea |
|---|---|---|
| 01 | Bounded Buffer (Producer-Consumer) | semaphores/CV; full/empty accounting |
| 02 | Dining Philosophers | deadlock + starvation; resource ordering |
| 03 | Readers-Writers | reader concurrency vs writer exclusion |
| 04 | Sleeping Barber | waiting customers; no-busy-wait |

## What You'll Learn
- The canonical semaphore and monitor solutions to each problem.
- Where each problem fails (deadlock, starvation, race) and how the fix works.
- How these patterns map to real systems (queues, thread pools, caches, workers).

## Prerequisites
- Part 04 Ch 1-2 (semaphores, mutexes, monitors, CVs, RW locks).
- Part 03 (scheduling interacts with waiting).
