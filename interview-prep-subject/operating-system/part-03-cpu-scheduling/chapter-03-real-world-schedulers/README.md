# Chapter 3: Real-World Schedulers

> **TL;DR**: Real schedulers are hybrids of the textbook algorithms: Linux uses EEVDF (fair share) with RT/deadline classes, Windows NT uses 32-level priorities with dynamic boosts, and RTOSes use fixed-priority preemption or EDF. This chapter maps theory to production.

## Sections
| Section | Topic | Key Idea |
|---|---|---|
| 01 | Linux CFS & EEVDF | Fair share via vruntime / virtual deadline; rbtree |
| 02 | Windows NT Scheduler | Priority levels, dynamic boosts, dispatcher |
| 03 | Real-Time & RTOS Scheduling | Fixed-priority preemption, EDF, DEADLINE class |

## What You'll Learn
- What CFS/EEVDF actually compute and why the rbtree replaced the old O(n) scan.
- How Windows maps threads to 32 priority levels with interactive boosts.
- The difference between soft real-time (Linux SCHED_FIFO/DEADLINE) and hard real-time (RTOS).
- How each real scheduler relates to the classic algorithms from Chapter 2.

## Prerequisites
- Part 03 Ch 1 (criteria, preemption) and Ch 2 (all five algorithms).
- Part 01 Ch 2 (kernel, interrupts) for how ticks trigger scheduling.
- Part 02 Ch 4 (context switching) for switch costs.
