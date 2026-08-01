# Chapter 3: Real-World Deadlocks

> **TL;DR**: Deadlock theory meets practice: databases detect and roll back transactions, distributed systems use leases/timeouts, Linux enforces lock ordering with lockdep, and a classic case — the Mars Pathfinder priority-inversion incident — shows how subtle synchronization bugs present as "deadlock-like" freezes.

## Sections
| Section | Topic | Key Idea |
|---|---|---|
| 01 | Deadlocks in Databases | Row locks, transactions, detect + rollback |
| 02 | Distributed & Linux Deadlocks | Leases/timeouts; lockdep; the Pathfinder story |

## What You'll Learn
- How row-level locking and transactions create deadlocks in real databases.
- How distributed systems avoid them with leases and timeouts.
- How Linux uses lock ordering + lockdep to make deadlocks impossible.
- The Mars Pathfinder case and what it teaches.

## Prerequisites
- Part 05 Ch 1-2 (conditions, RAG, prevention/avoidance/detection).
- Part 04 (locks, transactions use the same primitives).
