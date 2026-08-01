# Part 4: Process Synchronization

> **TL;DR**: When threads/processes share data, they can race — so we need atomic operations, locks, semaphores, condition variables, and monitors. This part covers the critical-section problem, the primitives that solve it, the classic synchronization problems (producer-consumer, philosophers, readers-writers, barber), and modern tools (futexes, CAS/lock-free, Java/Go).

## What You'll Learn
- Why shared data needs synchronization and what a race condition is.
- The critical-section problem and its four requirements (ME, progress, bounded waiting, plus atomicity).
- Mutexes, semaphores, condition variables, monitors, spinlocks, read-write locks — how each works and when to use which.
- The four classic problems and their canonical solutions.
- Modern kernel/userspace primitives: futexes, CAS and lock-free structures, and the language-level models (Java synchronized, Go channels, Python GIL).

## Prerequisites
- Part 02 (threads share memory — the reason races exist).
- Part 03 (preemption can interrupt a thread mid-critical-section; scheduling decides who runs).
- Part 01 (kernel mode, system calls, interrupts).
