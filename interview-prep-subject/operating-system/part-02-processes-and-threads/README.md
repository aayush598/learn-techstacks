# Part: Processes and Threads

## What this part covers
The heart of OS concurrency: what a process is (and its identity card, the PCB), the full life cycle from creation (`fork`/`exec`) through termination (zombie/orphan/daemon), how processes relate into trees (`ps`), what threads are and the three threading models, and the mechanism that makes it all possible — the context switch — including its hidden costs and the production tricks used to reduce them.

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| ch-01 Process Concept | what-is-a-process, process-states & life-cycle, PCB, process-vs-program-vs-thread | Define process, enumerate states, describe PCB contents, distinguish program/process/thread |
| ch-02 Process Creation & Termination | fork & exec, zombie/orphan/daemon, hierarchies & ps tree | Trace fork/exec, explain zombies (reaping), design daemons, read `ps` trees |
| ch-03 Threads | what-are-threads, threads-vs-processes, user-vs-kernel threads, threading models, thread libraries | Compare thread/process, explain user vs kernel threads, models (N:1, 1:1, M:N), use pthreads/Java/Go |
| ch-04 Context Switching | internals, cost & mitigation | Describe save/restore, quantify cost, mitigation (cache-friendly, threading) |

## Study order
1. **ch-01** — the vocabulary (process, PCB, states) everything else depends on.
2. **ch-02** — processes are born and die; fork/exec is the single most-tested OS syscall pair.
3. **ch-03** — threads are the modern unit of concurrency; you need the models and libraries cold.
4. **ch-04** — context switching ties process *and* thread switching together and is where "performance" questions live.
Read chapters in order; within a chapter, sections in numbered order.

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ⭐⭐⭐⭐⭐ (5/5)** — this is the most-tested OS topic at FAANG/MAANG. "What happens on fork?", "process vs thread?", "zombie processes?", "why is context switching expensive?" appear in nearly every OS round.
- **Emphasized by**: backend/SRE roles everywhere (Amazon, Meta, Google, Netflix); systems roles (Databases: Snowflake, CockroachDB, Redis Labs); embedded (Tesla, NVIDIA).
- Expect **coding problems** built on these ideas: implement a thread pool, fork-based server, or explain `fork` in a multi-threaded program (a classic Google/Amazon trap).

## How the parts connect (roadmap)
- Builds on **Part 01** (syscalls, kernel mode, Linux architecture) — fork/exec and PCBs are the concrete syscall/kernel mechanisms introduced there.
- **Part 03 (CPU Scheduling)** assumes you know what a runnable task is; the scheduler picks among the processes/threads from Part 02.
- **Part 04 (Synchronization)** and **Part 05 (Deadlocks)** address the *dangers* of the concurrency Part 02 creates — race conditions and deadlock between the very processes/threads you just learned to create.
- Together, Parts 02-05 form the "concurrency core" that interviewers probe hardest.
