# Chapter 2: Scheduling Algorithms

> **TL;DR**: The classic scheduling algorithms — FCFS, SJF/SRTF, Round Robin, Priority, and MLFQ — trade off throughput, turnaround time, waiting time, and response time. No single algorithm is optimal for everything; production schedulers (Linux EEVDF, Windows NT) are hybrids of these ideas.

## Sections
| Section | Topic | Key Idea |
|---|---|---|
| 01 | FCFS | Run-to-completion in arrival order; convoy effect |
| 02 | SJF & SRTF | Minimize average TAT; optimal but impractical (needs future) |
| 03 | Round Robin | Time slicing for fairness and response |
| 04 | Priority Scheduling | Ranks tasks; starvation needs aging |
| 05 | MLQ & MLFQ | Layered queues; MLFQ learns behavior |
| 06 | Comparison & Selection | When to use which algorithm |

## What You'll Learn
- The math (Gantt charts, TAT/response/waiting) behind each classic algorithm.
- Why SJF is provably optimal but unimplementable as stated.
- How the quantum choice drives Round Robin's tradeoffs.
- Why MLFQ is the practical winner (and the ancestor of Linux's fair schedulers).
- The interview formula: computing TAT/waiting/response for a given schedule.

## Prerequisites
- Part 01 (CPU, kernel, interrupts) — preemption requires timers.
- Part 02 (processes, context switching) — scheduling happens on every switch.
- Part 03 Ch 1 (criteria, preemption, three schedulers).
