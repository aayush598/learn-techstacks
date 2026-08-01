# What are Threads

> **TL;DR**: A thread is a single sequential execution stream within a process — it has its own stack, registers, and program counter but shares the process's address space and resources, making it the OS's cheap unit of concurrency.

## 1. Why Does This Exist?
Processes give isolation, but isolation is expensive: switching between them flushes TLB/caches, and sharing data between them requires IPC with copies. Modern services need *concurrency inside one logical unit* — handling many requests, parallelizing computation, keeping the UI responsive while computing. Threads exist to provide: (1) **shared-memory concurrency** — all threads can read/write the same data without IPC, (2) **cheap creation and context switching** — no new address space, no TLB flush, (3) **parallelism** — multiple cores working the same task, and (4) **responsiveness** — one thread blocks on I/O while others continue. Without threads you'd be forced to either process-per-task (expensive) or a single event loop (limited parallelism).

## 2. How Does It Work?
- The process owns the shared resources: `mm_struct` (address space), `files_struct` (fd table), `fs_struct`, `signal_struct`, credentials.
- Each thread owns: a `task_struct` (kernel-scheduled task), its own **stack** (user + kernel), its own **registers/PC** (saved on the kernel stack), its own **TID**, and its own scheduling state.
- On Linux, threads are created by `clone(CLONE_VM | CLONE_FILES | CLONE_SIGHAND | CLONE_THREAD | ...)` — the pthreads library wraps this in `pthread_create`.
- The scheduler treats each thread as an independent runnable task; `ps -T`/`/proc/<pid>/task/` lists them.

## 3. When Is It Used?
- **Server request handling**: Apache worker MPM, MySQL (thread per connection), Java servlet containers (thread per request).
- **Parallel computation**: matrix ops, image/video processing, MapReduce-style in-process (C++ std::thread, OpenMP).
- **UI + background work**: one thread for the UI event loop, worker threads for I/O/compute (mobile, desktop).
- **I/O concurrency without blocking**: read/parse in separate threads, or one thread per connection (vs. async event loops).
- **Language runtimes**: Java (1:1), Go (M:N goroutines over threads), Rust (std::thread), C++ (std::thread).

## 4. Why Wasn't Another Approach Chosen?
- **Process-per-task**: isolated but costly — switch flushes TLB, IPC copies data, creation is expensive. Rejected for fine-grained concurrency; still chosen when isolation matters.
- **Single-threaded event loop (async I/O)**: fast and simple (nginx, Redis, Node), but doesn't use multiple cores for CPU work and complicates CPU-bound parallelism. Threads complement it (many runtimes now mix: async + thread pool).
- **User-space coroutines/green threads**: cheap but invisible to the OS; a blocking syscall stalls the whole process (N:1 model). Threads as kernel tasks avoid that.
- **Hardware threads (SMT)**: CPU-level concurrency, not a programming model; threads exploit SMT cores.
The chosen model — kernel-scheduled threads sharing a process — balances cost, parallelism, and blocking semantics.

## 5. Intuition
A process is a **building**; threads are the **workers inside it**. The workers share the building: same rooms (address space), same supply closet (files), same front desk (fd table). But each worker has their own: notepad (stack), current task (PC), and name badge (TID). Hiring a new worker (creating a thread) is cheap — they just grab an empty desk (stack) and start. They can also pass papers to each other directly (shared memory) — no mailing (IPC) needed.

## 6. Real-World Analogy
A **kitchen crew in a restaurant**: the chef, sous-chef, and pastry cook all share the kitchen (process address space) — same pantry (heap), same recipes (code), same inventory sheet (files). Each has their own station (stack), knife roll (registers), and station checklist (PC). When the pastry cook waits for the oven (I/O), the chef keeps cooking (thread independence). If one cook burns something, the whole kitchen smells (shared fate) — but the restaurant next door (another process) doesn't.

## 7. Formal Definition
A **thread** (thread of execution) is the smallest unit of scheduling/execution: a sequence of instructions with its own program counter, register set, stack, and scheduling state, sharing the parent process's address space, file descriptors, signal handlers, and process-wide state. On Linux, threads are tasks (`task_struct`) created with `CLONE_VM|CLONE_FILES|CLONE_SIGHAND|CLONE_THREAD`; the POSIX API is `pthread_create`. The process is the unit of *resource ownership*; the thread is the unit of *execution*.

## 8. Example
```
$ ./multi_thread &      # a process with 3 threads
$ ps -T -p 1234
  PID  SPID  COMMAND
  1234 1234  multi_thread      # main thread
  1234 1235  multi_thread      # worker A
  1234 1236  multi_thread      # worker B
$ cat /proc/1234/status | grep Threads
Threads: 3
$ cat /proc/1234/task/1235/stack 2>/dev/null || true   # per-thread kernel stack
```
Threads 1235/1236 share 1234's address space (same `maps`) but have distinct stacks, registers, and TIDs.

## 9. Internal Working
1. **Creation**: `pthread_create` → `clone(CLONE_VM|CLONE_FILES|CLONE_SIGHAND|CLONE_THREAD|CLONE_SYSVSEM|CLONE_SETTLS|CLONE_PARENT_SETTID, ...)` → `kernel_clone` → new `task_struct` + kernel stack; user stack allocated by the runtime; TLS (thread-local storage) set up.
2. **Sharing**: the new task's `mm`/`files`/`fs`/`sighand` point to the *same* structs (refcounted) instead of copies — that's the whole difference from fork.
3. **Scheduling**: threads are ordinary tasks on runqueues; `switch_mm` is skipped when switching between threads of the same process (no TLB flush).
4. **Exit**: thread calls `pthread_exit`/returns → `do_exit` → thread's task_struct freed; the process stays until its last thread exits (or `exit_group`).
5. **Identity**: `gettid()` = TID; `getpid()` = TGID (thread group leader's PID). Signal delivery is per-thread or per-group.
6. **Observability**: `/proc/<pid>/task/<tid>/` per-thread state; `top -H`/`ps -T` show them.

## 10. Time Complexity
- Thread creation: O(1) amortized + O(new stack) — typically ~5-20µs vs fork+exec ~100-500µs.
- Thread context switch: O(1) — registers + stack pointer, no CR3/TLB work (same mm).
- Process switch: O(1) + TLB/cache warm-up (higher constant).
- Scheduling 1000s of threads: EEVDF O(log n) worst case; runqueue per-CPU.
- Memory: each thread = task_struct (~2-3KB) + kernel stack (16KB) + user stack (8MB virtual, small resident).

## 11. Advantages
- **Cheap concurrency**: low creation/switch cost vs processes.
- **Shared memory**: threads communicate by direct data access — no IPC copies.
- **Parallelism**: many cores on one task (thread-safe, synchronized).
- **Blocking independence**: one thread's I/O wait doesn't stall the others.
- **Resource economy**: one mm/files table shared — less duplication than processes.

## 12. Disadvantages
- **No isolation**: a thread segfault or wild pointer kills the whole process.
- **Race conditions**: shared data needs synchronization (mutexes) — bugs are subtle and hard to reproduce.
- **Blocking semantics**: a thread blocked in a syscall blocks only itself (good), but a *user-thread* in N:1 blocks its whole process (bad).
- **Debugging complexity**: multi-threaded stack traces, data races, TSan needed.
- **Scalability ceilings**: lock contention, false sharing, and cache thrash with many threads on shared data.

## 13. Interview Questions
1. **Q: What is a thread?** A: The smallest unit of scheduling/execution — a sequence of instructions with its own PC, registers, stack, and TID, sharing the process's address space, files, and signal handlers.
2. **Q: What does a thread share with its process and what does it own?** A: Shares: address space (code/data/heap), open fds, signal handlers, cwd, creds. Owns: stack, registers, PC, TID, scheduling state, thread-local storage.
3. **Q (TRICKY): Do two threads of one process have separate page tables?** A: No — they share one `mm_struct`/page tables. That's why switching between them doesn't require a CR3 change. (Their *kernel stacks* and TSS per-thread context are separate.)
4. **Q: How is a thread created on Linux?** A: `pthread_create` → `clone` with `CLONE_VM|CLONE_FILES|CLONE_SIGHAND|CLONE_THREAD|CLONE_SETTLS` → a new task sharing the process's resources.
5. **Q: What is the difference between a thread's TID and the process's PID?** A: TID = unique thread id (`gettid`); PID = TGID = the thread-group leader's ID (`getpid`). In a single-threaded process, TID == PID.
6. **Q: Why are threads cheaper to create than processes?** A: Threads skip address-space copy: no page-table duplication (COW not needed), no fd/fs copy — just a new task_struct + stacks. Order of magnitude cheaper.
7. **Q (SCENARIO): A thread calls `read()` on a slow socket. Do other threads stall?** A: No — each thread is a kernel task; the blocked thread goes to a wait queue while others run. (This is the 1:1 advantage; in N:1 user threads it WOULD stall the process.)
8. **Q: What happens to the process if one thread has a segfault?** A: The whole process dies (shared address space, shared signal handlers) — SIGSEGV kills the process, taking all threads with it.
9. **Q: What is thread-local storage (TLS)?** A: Per-thread variables (e.g., errno, thread caches) — implemented via the FS/GS segment or `__thread` keyword; `CLONE_SETTLS` sets the TLS base at thread creation.
10. **Q: How does the kernel schedule threads?** A: Each thread is a task on a runqueue (EEVDF); the scheduler picks per-CPU; switching within a process skips address-space switch (no TLB flush).
11. **Q: What is the difference between a thread and a coroutine/green thread?** A: Threads are scheduled by the OS (kernel tasks); coroutines/green threads are user-space scheduled (M:N or N:1) — cheaper but invisible to the OS (blocking syscalls stall unless carefully bridged).
12. **Q (PRODUCTION): Your Java/Node app has thousands of threads and a huge RSS. Why?** A: Each thread has a user stack (e.g., 8MB virtual default, or JVM 1MB) + task_struct + kernel stack — thousands × MBs = gigabytes. Use bounded thread pools or async models.
13. **Q: What is the thread group and who is the leader?** A: The thread group = all threads with the same TGID; the leader is the first (main) thread. `getpid()` returns the leader's TID; signals to the PID hit the group.
14. **Q: What does `pthread_join` do?** A: Blocks the calling thread until the target thread exits, then reaps its resources and retrieves its return value — the thread analog of `wait`.
15. **Q: How do you see threads in production?** A: `ps -T -p <pid>`, `ps -L`, `top -H`, `htop` (thread view), `/proc/<pid>/task/`, and `Threads:` in `/proc/<pid>/status`.
16. **Q (TRICKY): Can a process have threads from different "users" or is the process a single security context?** A: Threads share the process's credentials (uid/gid/caps) by default; per-thread credentials (capabilities/security contexts) are possible (e.g., for servers) but rare — the process is usually the security unit.

## 14. Follow-Up Questions
1. **Q: What is false sharing and how does it relate to threads?** A: Two threads on different cores writing adjacent cache lines cause cache-line ping-pong (invalidate/refetch) — the effect of sharing the same line though data differs. Padding/`cacheline_aligned` fixes it.
2. **Q: What is the cost of a thread context switch on modern CPUs?** A: ~1-5µs measured (register save/restore + scheduler), plus cache/TLB warm-up effects; process switches pay more (CR3 + potential TLB flush).
3. **Q: How many threads is too many?** A: Depends: ~1 thread per core for CPU-bound; many for I/O-bound; beyond a few thousand you hit memory/scheduler overhead — profile and use pools.
4. **Q: What is `pthread_setaffinity_np`/`sched_setaffinity`?** A: CPU affinity — pins a thread to specific cores to improve cache locality and reduce migration jitter.
5. **Q: How does errno work per thread?** A: errno is thread-local (via TLS); each thread's errno is independent — that's why errno must be TLS in a multithreaded libc.

## 15. Coding Example
```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/syscall.h>

#define N 4

void *worker(void *arg) {
    int id = *(int *)arg;
    /* thread-local view: own TID, shared memory (printf, globals) */
    printf("worker %d: tid=%ld in process %ld\n", id,
           syscall(SYS_gettid), (long)getpid());
    return NULL;
}

int main(void) {
    pthread_t tids[N];
    int ids[N];
    for (int i = 0; i < N; i++) {
        ids[i] = i;
        pthread_create(&tids[i], NULL, worker, &ids[i]);
    }
    for (int i = 0; i < N; i++)
        pthread_join(tids[i], NULL);
    printf("main done; process pid=%ld\n", (long)getpid());
    return 0;
}
```
```bash
# Compile & observe
gcc -pthread threads.c -o threads && ./threads
ps -T -p $(pgrep -n threads) | head
cat /proc/$(pgrep -n threads)/status | grep Threads
```

## 16. Industry Usage
- **Databases**: MySQL (thread per connection), Postgres (processes + parallel workers threads), Redis (single-threaded, but uses `bio` threads for fsync).
- **Web/app servers**: Tomcat (thread pool), gunicorn (processes + threads), nginx (event loop, optionally thread pools), Go services (goroutines over threads).
- **Runtimes**: JVM (1:1 native threads), Go (M:N GMP), Rust std::thread (1:1), C++ std::thread, Python (GIL + threads, multiprocessing for CPU).
- **Cloud/scale**: thread pools with bounded size, cgroup `pids.max` limits, `ulimit -u`; monitoring `Threads:` in status.
- **Embedded**: FreeRTOS tasks are threads (scheduled by the RTOS).
- **Interview angle**: thread definition/sharing/cost is the most-asked OS concurrency opening; being fluent here makes synchronization (Part 04) much easier.

## 17. References
- Silberschatz, *OS Concepts*, Ch. 4 (Threads).
- Tanenbaum, *Modern OS*, Ch. 2.2 (Threads).
- Linux man: `clone(2)`, `pthreads(7)`, `pthread_create(3)`, `gettid(2)`.
- Linux source: `kernel/fork.c` (kernel_clone), `include/linux/sched.h`.
- Love, *Linux Kernel Development*, Ch. 4 (Process Scheduling), threads.
- Kerrisk, *The Linux Programming Interface* (threads chapters).

## 18. Cheat Sheet
- Thread = execution stream; owns stack/registers/PC/TID; shares mm, files, signals.
- Created via clone(CLONE_VM | CLONE_FILES | ...); pthreads wraps it.
- Thread create ~5-20µs; fork+exec ~100-500µs.
- Thread switch: no CR3/TLB change (same mm) → cheaper.
- Thread segfault kills the process; process crash isolated.
- TID vs TGID; `ps -T`, `top -H`, `/proc/<pid>/task/`.
- TLS = thread-local storage (errno); CLONE_SETTLS.
- Blocked thread doesn't stall others (1:1).
- Thousands of threads = GBs RSS (stacks); use pools.
- False sharing = cache-line ping-pong; pad structs.

## 19. Quiz
1. Threads of a process share: a) stack b) address space c) registers d) TID → **b**
2. A thread owns: a) mm_struct b) page tables c) its stack & registers d) fd table → **c**
3. Thread creation uses: a) fork b) clone with CLONE_VM etc c) exec d) mmap → **b**
4. Thread switch within a process skips: a) register save b) CR3/TLB work c) stack change d) nothing → **b**
5. One thread's segfault: a) isolated b) kills the process c) kills the kernel d) nothing → **b**
6. `gettid` returns: a) process PID b) thread ID c) TGID d) uid → **b**
7. errno is: a) global b) thread-local c) per-process d) per-cpu → **b**
8. In a single-threaded process, TID: a) differs from PID b) equals PID c) is 0 d) is the uid → **b**
9. Blocked thread (1:1 model) stalls: a) the whole process b) only itself c) the kernel d) other cores → **b**
10. False sharing causes: a) deadlock b) cache-line ping-pong c) zombie threads d) TLB thrash → **b**

## 20. Flashcards
- **Q: Define thread.** → **A:** Execution stream with own stack/regs/PC, sharing process address space.
- **Q: What do threads share?** → **A:** Address space, files, signals; own stacks/TIDs.
- **Q: How are threads created on Linux?** → **A:** clone with CLONE_VM|CLONE_FILES|CLONE_SIGHAND|CLONE_THREAD.
- **Q: Why are threads cheap?** → **A:** No address space/page table duplication.
- **Q: Why is thread switch cheap?** → **A:** Same mm — no CR3/TLB flush.
- **Q: Thread crash effect?** → **A:** Kills its process.
- **Q: TID vs PID?** → **A:** gettid vs TGID/leader.
- **Q: TLS?** → **A:** Per-thread storage (errno); CLONE_SETTLS.
- **Q: False sharing?** → **A:** Adjacent cache lines ping-pong between cores.

## 21. Revision
A thread is the unit of execution within a process: own stack, registers, PC, TID; shared mm, files, signals. Created by `clone(CLONE_VM|...)`, ~10x cheaper than fork+exec; thread switches skip CR3/TLB. A thread crash kills its process. TID vs PID (TGID) matters for signals and `ps -T`. Threads give cheap shared-memory concurrency but bring races and shared fate; production uses bounded pools and watches RSS. This is the foundation for all of Part 04 (synchronization).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a thread?" | 7 Formal Definition / 5 Intuition |
| "What do threads share/own?" | 13 Q2 / 2 How It Works |
| "How is a thread created?" | 13 Q4 / 9 Internal Working |
| "Thread vs process creation/switch cost?" | 13 Q6-7 / 10 Time Complexity |
| "What happens when a thread crashes?" | 13 Q8 / 12 Disadvantages |
| "TID vs PID?" | 13 Q5 / 9 Internal Working |
| "What is TLS?" | 13 Q9 / 14 Follow-Up Q5 |
| "Why is my app's RSS huge with many threads?" | 13 Q12 / 16 Industry Usage |
| "Coroutine vs thread?" | 13 Q11 / 4 Why Not |
| "How to see threads in prod?" | 13 Q15 / 16 Industry Usage |
