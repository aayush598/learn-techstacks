# Part: CPU Scheduling

## What this part covers
The OS's central question — "which process gets the CPU, and for how long?" — answered from first principles to production schedulers. You'll learn the scheduling criteria (throughput, latency, fairness), the three scheduler types (long/short/medium term), preemption semantics, the classic algorithms (FCFS, SJF/SRTF, Round Robin, Priority, MLQ/MLFQ), and how real kernels actually schedule today: Linux's CFS/EEVDF, the Windows NT scheduler, and real-time schedulers (FreeRTOS, SCHED_DEADLINE, RMS).

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| ch-01 Scheduling Fundamentals | criteria & goals, long/short/medium schedulers, preemptive vs non-preemptive | Quantify scheduling goals; classify schedulers; define preemption |
| ch-02 Scheduling Algorithms | FCFS, SJF/SRTF, Round Robin, Priority, MLQ/MLFQ, Comparison | Compute turnaround/wait/response; analyze starvation & overhead; pick per workload |
| ch-03 Real-World Schedulers | Linux CFS/EEVDF, Windows NT, RTOS & real-time scheduling | Explain EEVDF/vruntime & O(1)/O(log n) claims; NT dispatcher/quantum; RMS/EDF, SCHED_DEADLINE |

## Study order
1. **ch-01** — the criteria (why scheduling exists) and vocabulary.
2. **ch-02** — the algorithms, because every interview question computes Gantt charts and turnaround/wait times.
3. **ch-03** — real schedulers, because production questions ("how does Linux schedule?") live here.
Read sections in numbered order within each chapter; Chapter 03 assumes Chapters 01-02.

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ⭐⭐⭐⭐ (4/5)** — near-universal: every FAANG/MAANG OS round has at least one scheduling computation (Gantt/turnaround) or a "which algorithm would you use?" design question.
- **Emphasized by**: Amazon/Google/Meta (compute Gantt, compare algorithms), OS/systems teams (Linux scheduler internals), embedded (Tesla, Apple: RTOS scheduling), SRE (why is my container slow — CFS bandwidth cgroups).
- **Coding angle**: scheduling questions appear as priority-queue/heap problems (e.g., "process tasks by deadline") — the algorithms transfer directly.

## How the parts connect (roadmap)
- Builds on **Part 02** (Processes/Threads): the scheduler picks among the tasks you learned there; context switching is what the scheduler *executes*.
- Feeds **Part 04 (Synchronization)** and **Part 05 (Deadlocks)**: preemption and priority are what make sync (which relies on the scheduler not swapping threads mid-critical-section in some designs) and priority-inversion deadlocks real problems.
- Later parts (memory, I/O) also have "scheduling" (page replacement, disk scheduling) — the same criteria/intuition generalize.
