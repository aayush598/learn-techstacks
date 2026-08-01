# Threads vs Processes

> **TL;DR**: Threads give cheap shared-memory concurrency inside one process; processes give isolated fault/security domains — the choice is a cost/isolation trade-off, and production systems often use both (threads for parallelism, processes for isolation).

## 1. Why Does This Exist?
The question "threads or processes?" exists because the two models optimize different things. Processes were the original unit (isolation-first, expensive); threads were invented (1980s, then mainstreamed) because sharing memory cheaply and switching fast is essential for interactive and parallel systems. Understanding the difference isn't academic — every server architecture, language runtime, and container model is a decision about this axis. The comparison exists to help engineers pick correctly: you want processes when a crash or compromise must be contained, threads when you need low-cost parallelism on shared data.

## 2. How Does It Work?
Comparison matrix (the full answer to the interview question):
| Axis | Process | Thread |
|---|---|---|
| Address space | private (`mm_struct`) | shared (same mm) |
| Creation cost | fork: ~100-500µs | clone: ~5-20µs |
| Context switch | + CR3/TLB flush | no address-space switch |
| Sharing | via IPC (copies) | direct shared memory |
| Crash semantics | isolated | kills the whole process |
| Security | per-process creds | shared creds |
| Debugging | per-process | multi-threaded traces |
| Number limits | pid_max | thread limits + stack memory |
On Linux, both are `task_struct`s; the difference is what `clone` flags share.

## 3. When Is It Used?
- **Threads**: in-process parallelism (compute), thread-per-connection servers (Java, MySQL), request pools, apps with UI+background work, language runtimes.
- **Processes**: isolation boundaries — browsers (per-tab), containers (per-app), daemons (per-service), multi-tenant services, servers that must survive child crashes (Postgres backends).
- **Both together**: nginx (master process + workers, each worker event-driven), Apache prefork (processes) + worker MPM (threads), Go (process + goroutines), browsers (process per site + threads per process).
- **Decision rule**: isolate untrusted/failure-prone work in processes; parallelize trusted in-process work with threads.

## 4. Why Wasn't Another Approach Chosen?
- **Processes only**: no cheap sharing or fine-grained parallelism; IPC latency dominates high-frequency coordination. Rejected for modern workloads (still correct for isolation).
- **Threads only**: no isolation — one wild pointer kills everything; no protection between apps/users; security domains impossible. Rejected.
- **Coroutines-only (no OS threads)**: cheap but blocking syscalls stall the process unless bridged; limited to cooperative concurrency. Used for I/O-heavy single-threaded apps, not general parallelism.
- **Unikernel/VEE (processes as VMs)**: heavyweight; used only for strong isolation.
The industry converged on "process for isolation, threads for concurrency" with hybrid architectures everywhere.

## 5. Intuition
Think of **two construction sites vs one site with many workers**. One site with many workers (threads): they share the site, tools, and materials (memory), communicate by shouting (shared variables), and hire more workers cheaply — but one worker's fire (segfault) burns the whole site. Two sites (processes): complete isolation — a fire at site A doesn't touch site B — but sharing materials means trucking them between sites (IPC), and setting up a new site is expensive.

## 6. Real-World Analogy
A **hospital**: threads are nurses on one ward sharing the same floor, charts (memory), and supplies — efficient, but an infection (bug) spreads across the ward. Processes are *different hospitals* (or isolation wings) — a lockdown in one hospital never affects another, but transferring a patient requires an ambulance (IPC). Modern care (hybrid) has isolation wings for infectious cases (processes) and shared teams within each ward (threads).

## 7. Formal Definition
**Process**: a unit of resource ownership — an isolated address space, file table, credentials, and signals; the unit for protection and fault containment. **Thread**: a unit of execution within a process — shares the process's resources; the unit for scheduling and parallelism. The **thread-vs-process decision** is the engineering choice between isolation (process) and efficiency/simplicity of sharing (thread).

## 8. Example
Two servers, same workload (10k connections, 4 cores):
- **Process-per-connection** (Apache prefork): 10k processes — 10k page tables, GBs of overhead, heavy context switches with TLB flushes; but a crash kills one connection only.
- **Thread-per-connection** (Java NIO + thread, or MySQL): 10k threads in a few processes — shared memory, cheap switching, moderate overhead (thread stacks); but one wild pointer in any thread kills all 10k connections.
- **Event loop + thread pool** (nginx/Go): few processes/threads, async I/O — best of both: cheap concurrency and controlled parallelism, with process isolation at the worker level.
The concrete numbers (10k processes vs 10k threads vs 100 event-loop workers) demonstrate the trade-off.

## 9. Internal Working
1. **Process creation**: `fork` → `copy_process` with COW memory, duplicated fd/fs/creds → new page tables, new `mm_struct`.
2. **Thread creation**: `clone(CLONE_VM|...)` → new `task_struct`, *shares* `mm_struct`/`files_struct` (refcount++), new kernel stack + user stack.
3. **Context switch**:
   - Thread→thread (same process): `switch_to` swaps registers + kernel stacks only; `mm` unchanged; no TLB flush.
   - Process→process: additionally `switch_mm` (CR3), possible TLB flush (with PCID, selective); cache cold.
4. **Exit**: a process exits when its last thread exits (or `exit_group`); each thread exit frees its task_struct.
5. **Isolation enforcement**: process boundary = page tables + U/S bits; thread boundary = nothing (shared mm) — which is why threads can't be "isolated" from each other.

## 10. Time Complexity
- Thread create: O(1) + O(stack) ≈ 5-20µs; process create: O(1) + O(page tables) ≈ 100-500µs (COW).
- Thread switch: O(1) ~ 1-5µs (no TLB); process switch: O(1) + TLB/cache refill ~ 2-10µs+.
- IPC (process) per message: O(size) copy + syscalls; thread shared access: O(1) + lock.
- Memory: thread ≈ task_struct + 16KB kernel stack + user stack (mostly virtual); process ≈ + page tables + duplicated resource tables.

## 11. Advantages
**Threads**: cheap create/switch; zero-copy sharing; natural parallelism on shared data; per-thread blocking independence; low memory overhead.
**Processes**: crash isolation; security (creds, capabilities, namespaces); independent life cycles (restartable); portable across hosts; cleaner failure models.

## 12. Disadvantages
**Threads**: no isolation (one crash kills all); data races require locks (complexity + contention); debugging harder; stack memory scales linearly; signal semantics messy.
**Processes**: expensive create/switch; IPC copy/latency; memory duplication (page tables, fd tables); harder to coordinate shared state; more processes = more kernel objects.

## 13. Interview Questions
1. **Q: What's the difference between a process and a thread?** A: A process is a unit of resource ownership (own address space, files, creds) — isolation; a thread is a unit of execution within a process (shares those) — concurrency. Linux represents both as tasks; `clone` flags decide sharing.
2. **Q: Why is a thread faster to create than a process?** A: No address space to build — no page-table/COW setup, no fd/fs/cred duplication; just a new task_struct + stacks. ~10x cheaper.
3. **Q: Why is switching between threads faster than between processes?** A: Threads share page tables, so no `switch_mm`/CR3 reload and no TLB flush — only registers + stack pointer + scheduling.
4. **Q (TRICKY): Can a thread be "isolated" like a process?** A: No — by definition threads share the address space; isolation requires separate address spaces (processes, or VMs). You can get *crash* isolation with subprocesses/isolates, but not within one thread pool.
5. **Q: When would you prefer processes over threads?** A: When you need fault isolation (browser tabs, multi-tenant services, containers), security boundaries (untrusted code), or independent life cycles (restart a crashed child without losing others). Also when the unit must migrate across hosts.
6. **Q: When threads over processes?** A: When sharing is the point (in-memory caches, shared indexes), you need low-latency parallelism, creation cost matters (per-request), or IPC overhead would dominate.
7. **Q (SCENARIO): Build a web server. Process, thread, or event loop?** A: Classic answer: event loop for I/O-heavy (nginx/Node/Redis) + thread pool for blocking work; processes/threads per connection trade isolation vs overhead. Modern: Go/async + bounded thread pools. Justify by workload (I/O vs CPU-bound) and isolation needs.
8. **Q: How does crash semantics differ?** A: A thread fault (SIGSEGV) kills its process — all threads die. A process crash is isolated; other processes continue. That's why browsers use process-per-tab.
9. **Q (PRODUCTION): 10k threads vs 10k processes — what breaks first?** A: Processes exhaust PIDs (pid_max), page-table memory, and scheduler/TLB overhead; threads exhaust stack memory (RSS) and lock/scheduler contention. Measure; both need pooling.
10. **Q: What does `clone` share for threads vs processes?** A: Threads: `CLONE_VM|CLONE_FILES|CLONE_SIGHAND|CLONE_THREAD|CLONE_FS`. Processes (fork): none of those (COW memory, dup fd/fs). Containers add `CLONE_NEW*` namespace flags.
11. **Q: Can you have both threads and processes?** A: Yes — nginx (master/worker processes), Apache worker MPM (processes each with threads), Java (processes per JVM, threads inside), Go (process per program, goroutines inside). Hybrid is the norm.
12. **Q: How does memory accounting differ?** A: Process memory = its RSS (page tables + pages); thread memory is counted under the process's RSS (shared pages) + thread stacks. `VmRSS` includes all threads' resident stacks.
13. **Q: What is a thread pool and why?** A: A fixed set of worker threads processing a queue — avoids per-task creation cost, bounds resources, amortizes stack memory. Every server uses one.
14. **Q (TRICKY): If threads share memory, why is passing data between threads still slow sometimes?** A: Synchronization (locks) + cache coherence — writing shared data invalidates other cores' caches; false sharing multiplies it. Sharing *avoids copies* but not *coherence*.
15. **Q: How do signals interact with threads?** A: Signal *dispositions* are process-wide; delivery targets a specific thread (the one not blocking it) or the whole group depending on the signal; `pthread_kill` sends to one thread. This is a common source of bugs.

## 14. Follow-Up Questions
1. **Q: What is a goroutine vs an OS thread?** A: A goroutine is a user-space coroutine scheduled by the Go runtime (M:N) — thousands of them on a few OS threads; stacks grow dynamically; not visible to the kernel as separate threads.
2. **Q: What is the "thread per connection" anti-pattern?** A: At high concurrency, each blocked connection pins a stack (MBs) and scheduler entry — memory/latency blowup; the fix is event-driven I/O with a small thread pool.
3. **Q: What is process migration and why can't threads migrate as easily?** A: Processes have full state (can checkpoint/restart across hosts); threads are tied to a process's memory in one host — distributed systems replicate *processes*, not threads.
4. **Q: How do containers relate to processes/threads?** A: A container is a set of processes (PID namespace) sharing namespaces + cgroups — it's a *process-group* construct, not a thread construct.
5. **Q: What is the cost of `clone` vs `fork` measured on a real system?** A: Rough: fork+exec of /bin/true ~ 100-500µs; pthread_create ~ 5-20µs; measured thread switch ~ 1-5µs, process switch ~ 2-10µs (TLB/cache dependent).

## 15. Coding Example
```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/wait.h>

/* Thread variant: shares memory */
long shared_counter = 0;
void *thread_incr(void *arg) {
    for (int i = 0; i < 100000; i++) shared_counter++;   /* racy without lock */
    return NULL;
}

int main(void) {
    /* threads: one process, N threads */
    pthread_t t[4];
    for (int i = 0; i < 4; i++) pthread_create(&t[i], NULL, thread_incr, NULL);
    for (int i = 0; i < 4; i++) pthread_join(t[i], NULL);
    printf("threads shared_counter = %ld (expect 400000)\n", shared_counter);

    /* processes: each has its OWN copy -> no sharing */
    long proc_counter = 0;
    pid_t pids[4];
    for (int i = 0; i < 4; i++) {
        if ((pids[i] = fork()) == 0) {
            for (int j = 0; j < 100000; j++) proc_counter++;
            _exit(proc_counter);
        }
    }
    for (int i = 0; i < 4; i++) { int st; waitpid(pids[i], &st, 0); }
    printf("processes: each child had its own counter (isolated)\n");
    return 0;
}
```
```bash
# Observe process vs thread count
./demo &
PID=$(pgrep -n demo)
echo "processes: $(pgrep -P $PID | wc -l)"
echo "threads: $(cat /proc/$PID/status | grep Threads)"
```

## 16. Industry Usage
- **Processes**: browser tabs (Chrome), containers (Docker/runc), Postgres backends, systemd services, multi-tenant cloud apps, language runtimes that isolate (Firefox sandbox).
- **Threads**: MySQL, Tomcat, JVM, OpenMP/C++ std::thread, Go (goroutines over threads), UI frameworks.
- **Hybrid**: nginx (process workers), Apache worker MPM, gunicorn (processes, some threads), Kubernetes (pods = process groups; workloads use threads inside).
- **SRE practice**: `pid_max`/`threads-max` tuning, cgroup `pids.max`, thread-pool sizing, and "process vs thread vs event loop" architecture decisions on every backend.
- **Interview angle**: this is the single most-asked OS design question; the sharing/cost/isolation matrix is the complete answer.

## 17. References
- Silberschatz, *OS Concepts*, Ch. 3-4 (Processes and Threads).
- Tanenbaum, *Modern OS*, Ch. 2.1-2.2.
- Linux man: `clone(2)`, `fork(2)`, `pthreads(7)`.
- Love, *Linux Kernel Development*, Ch. 3-4.
- Kerrisk, *The Linux Programming Interface* (process vs thread chapters).
- Go docs: effective Go (goroutines) — M:N scheduling.

## 18. Cheat Sheet
- Process = resource unit (isolation); Thread = execution unit (concurrency).
- Threads: share mm/files/signals; own stack/regs/TID.
- Thread create ~10x cheaper; switch skips CR3/TLB.
- Thread crash kills process; process crash isolated.
- Both are task_struct; clone flags decide sharing.
- Use threads: shared data, low-latency parallelism, per-request work.
- Use processes: isolation, security, independent life cycles, cross-host.
- Hybrid everywhere: nginx, Apache MPM, Go, browsers.
- 10k processes → PID/memory exhaustion; 10k threads → stack/scheduler pressure.
- Thread pool = bounded workers; the universal pattern.

## 19. Quiz
1. Which is a unit of resource ownership? a) thread b) process c) coroutine d) goroutine → **b**
2. Threads of a process share: a) kernel stack b) address space c) registers d) user stack → **b**
3. Cheaper to create: a) process b) thread c) same d) container → **b**
4. Switching between processes requires: a) only registers b) CR3/TLB handling c) nothing d) a reboot → **b**
5. A thread segfault: a) isolated b) kills its process c) kills the kernel d) nothing → **b**
6. Hybrid architecture example: a) nginx b) MySQL only c) Redis only d) Postgres only → **a**
7. 10k processes first exhaust: a) memory b) PIDs/page tables c) sockets d) disk → **b**
8. Threads communicate via: a) IPC copies b) shared memory c) network d) files → **b**
9. `clone(CLONE_VM)` creates: a) process b) thread-like task c) container d) VM → **b**
10. Goroutines are scheduled by: a) the kernel b) the Go runtime c) systemd d) the JVM → **b**

## 20. Flashcards
- **Q: Process vs thread (one line)?** → **A:** Resource/isolation unit vs execution/concurrency unit.
- **Q: What do threads share?** → **A:** Address space, files, signals; own stacks/regs.
- **Q: Why cheaper to create?** → **A:** No address-space/page-table build.
- **Q: Why cheaper to switch?** → **A:** Same page tables — no CR3/TLB flush.
- **Q: Crash semantics?** → **A:** Thread kills process; process is isolated.
- **Q: When processes?** → **A:** Isolation, security, independent life, cross-host.
- **Q: When threads?** → **A:** Shared data, low-latency parallelism, per-request.
- **Q: Hybrid examples?** → **A:** nginx, Apache MPM, Go, browsers.
- **Q: Thread pool?** → **A:** Bounded worker set over a queue.

## 21. Revision
Processes = units of resource ownership (own address space, files, creds) — the isolation boundary. Threads = units of execution within a process (share those) — the concurrency unit. Threads are ~10x cheaper to create and switch (no CR3/TLB work) but share fate (one crash kills the process). Choose processes for isolation/security/life-cycle independence; threads for shared-data parallelism and per-request concurrency. Real systems are hybrid (nginx, Apache, Go, browsers). Both are `task_struct`s; `clone` flags decide sharing.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Process vs thread?" | 7 Formal Definition / 2 How It Works |
| "Why are threads cheaper to create/switch?" | 13 Q2-3 / 10 Time Complexity |
| "Can threads be isolated?" | 13 Q4 / 12 Disadvantages |
| "When processes vs threads?" | 13 Q5-6 / 3 When Is It Used |
| "Design a web server (process/thread/event)?" | 13 Q7 / 16 Industry Usage |
| "Crash semantics?" | 13 Q8 / 9 Internal Working |
| "10k threads vs 10k processes?" | 13 Q9 / 16 Industry Usage |
| "clone flags for threads?" | 13 Q10 / 9 Internal Working |
| "Why is shared access slow despite sharing?" | 13 Q14 / 14 Follow-Up Q1 |
| "Goroutines vs OS threads?" | 14 Follow-Up Q1 / 16 Industry Usage |
