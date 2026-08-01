# Chapter: Threads

## What you'll learn
- What threads are, why they exist (shared-memory concurrency), and what they share vs own.
- The precise thread-vs-process comparison: creation cost, context-switch cost, sharing, crash semantics.
- User threads vs kernel threads — where they run and why the distinction matters.
- The three threading models (many-to-one, one-to-one, many-to-many) and which real systems use which.
- The thread libraries that matter in interviews: POSIX pthreads, Java threads, Go goroutines (M:N).

## Prerequisites (linked)
- [Ch-01 Process Concept](../chapter-01-process-concept/README.md) and [Ch-02 Creation & Termination](../chapter-02-process-creation-and-termination/README.md) — `clone` flags, task_struct, process vs thread.
- [Part 01 Ch-03 Linux Architecture](../../part-01-os-fundamentals/chapter-03-linux-architecture/README.md) — how the kernel schedules tasks.
- Feeds into [Ch-04 Context Switching](../chapter-04-context-switching/README.md) and [Part 04 (Synchronization)](../../part-04-process-synchronization/README.md).

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — What are Threads](section-01-what-are-threads.md) | Definition, sharing matrix, thread structures |
| [Section 02 — Threads vs Processes](section-02-threads-vs-processes.md) | Cost, sharing, isolation, and when to use which |
| [Section 03 — User Threads vs Kernel Threads](section-03-user-threads-vs-kernel-threads.md) | Scheduler sees user threads (no) vs kernel threads (yes) |
| [Section 04 — Threading Models](section-04-threading-models-many-to-one-one-to-one-many-to-many.md) | N:1, 1:1, M:N mapping and their trade-offs |
| [Section 05 — Thread Libraries: pthreads, Java, Go](section-05-thread-libraries-pthreads-java-and-go.md) | The APIs and runtimes interviewers expect |

## One-paragraph narrative connecting all sections
Threads exist to give you concurrency with *shared memory* and cheap switching — the alternative to process isolation when you need parallelism inside one service (Section 01). Deciding between threads and processes is a cost/isolation trade-off: threads are cheaper but share fate (Section 02). Whether the OS knows about your threads depends on whether they're user threads (scheduled in user space, invisible to the kernel) or kernel threads (each a schedulable task) — and the historical mappings (N:1, 1:1, M:N) were the industry's answer to that tension (Sections 03-04). Finally, the libraries you'll actually use — pthreads, Java's java.lang.Thread, Go's goroutines — are these models made concrete (Section 05).

## Common interview trap in this chapter
Confusing **user threads** with **user-mode code**. Both run user code, but "user threads" specifically means *threads the kernel doesn't schedule* (N:1, e.g., old green threads); "kernel threads" can mean *kernel-internal tasks* (ksoftirqd) OR *threads scheduled by the kernel* (1:1, most pthreads). Also: Go's goroutines are NOT 1:1 OS threads — they're an M:N model where the Go scheduler multiplexes goroutines over OS threads.

## Checklist before moving on
- [ ] I can list exactly what threads share and what they own.
- [ ] I can compare thread vs process on 5 axes (cost, switch, sharing, crash, isolation).
- [ ] I can explain user threads vs kernel threads and why blocking a user thread can block its whole process (in N:1).
- [ ] I can draw all three threading models with real examples (pthreads=1:1, Go=M:N, old green threads=N:1).
- [ ] I can write a correct pthread program (create/join) and explain `clone` flags.
- [ ] I know Java's thread model and Go's GMP scheduler at a high level.
