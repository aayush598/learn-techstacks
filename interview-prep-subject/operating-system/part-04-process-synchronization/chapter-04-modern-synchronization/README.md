# Chapter 4: Modern Synchronization

> **TL;DR**: Modern systems avoid heavyweight kernel calls: futexes keep the fast path in userspace (kernel only on contention); lock-free programming uses CAS and memory ordering for progress without locks; and high-level languages (Java, Go) offer structured, safer concurrency models.

## Sections
| Section | Topic | Key Idea |
|---|---|---|
| 01 | Futexes & Linux Synchronization | Userspace fast path + kernel wait/wake |
| 02 | Lock-Free Programming & CAS | Optimistic progress; ABA; memory order |
| 03 | Synchronization in Java & Go | synchronized/atomics; channels/goroutines |

## What You'll Learn
- How futexes make mutexes cheap (no syscall on the uncontended path).
- What lock-free/wait-free mean and the hazards (ABA, memory ordering).
- How Java and Go structure concurrency differently (shared-memory locks vs message passing).

## Prerequisites
- Part 04 Ch 1-2 (atomics, mutexes, semaphores).
- Part 03 (scheduling interacts with blocking).
