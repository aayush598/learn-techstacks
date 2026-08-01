# Process vs Program vs Thread

> **TL;DR**: A program is static code on disk, a process is an executing instance of a program with its own address space, and a thread is a single execution stream *within* a process — the trio differs by what is shared (nothing / everything / address space + files).

## 1. Why Does This Exist?
Interviewers and OS designers need a precise vocabulary because the three terms solve different problems: **programs** are the persistent, portable units of code you ship; **processes** are the isolated units of resource ownership and protection you run; **threads** are the units of execution and scheduling *inside* a process. The distinctions exist because: (1) one program file must run as many independent instances, (2) isolation (process) and concurrency (thread) are separate concerns that shouldn't be conflated, and (3) context-switch cost, sharing, and fault containment all depend on which of the three you mean.

## 2. How Does It Work?
- **Program**: a file (ELF/PE/Mach-O) containing text, data, symbols, and load instructions. It's inert — no PID, no state, no resources.
- **Process**: created by `exec`'ing a program → gets a PCB, an address space (`mm_struct`), file descriptors, credentials. It's the *container*: own page tables, own files, own signals.
- **Thread**: created by `clone` with sharing flags → each thread gets its own stack, registers, PC, and `task_struct`, but *shares* the process's address space, open files, signal handlers, and working directory. Threads are scheduled independently (Linux: each is a task).

## 3. When Is It Used?
- **Program**: when you build/install software (`gcc` produces a program), run `which`, or inspect ELF files.
- **Process**: when you need isolation — a web server child, a container, a sandboxed app, a background daemon; when you `kill`, `ps`, or apply `RLIMIT`s.
- **Thread**: when you need concurrency within a service — thread pools (Java, C pthreads, Go's M:N), parallel request handling (Apache worker), per-core work (MySQL threads), UI + worker threads.
- **All three in production**: Postgres = 1 process per backend + threads; nginx = processes (workers) + each uses epoll (not threads); Go = 1 process, goroutines (user threads) multiplexed on OS threads.

## 4. Why Wasn't Another Approach Chosen?
- **Process-per-task only (no threads)**: maximum isolation but expensive — context switches flush TLB, IPC between parts is slow, and shared-memory coordination is painful. Rejected for fine-grained concurrency.
- **Thread-only model (no process isolation)**: fast and shared, but a crash in one thread takes the whole process, and no isolation boundary for untrusted code. Rejected — containers/VMs need process-level isolation.
- **Program-as-process (no distinction)**: confuses static vs dynamic; can't run two instances of one binary independently. Rejected.
- **User threads without kernel threads (N:1)**: cheap but a blocking syscall blocks the whole process (see threading models chapter). Rejected for modern concurrency.
The chosen model — process for isolation, threads for concurrency, program as the loadable unit — is the Unix/Windows standard and the basis of how every production system is architected.

## 5. Intuition
A **program** is the blueprints of a building. A **process** is the building itself — walls, rooms, own address. A **thread** is a person working inside the building — they share the building but have their own office (stack), their own movements (registers), and their own current task (PC). Many people (threads) work in one building (process) using the same kitchen and files (shared resources); two buildings (processes) share nothing.

## 6. Real-World Analogy
A **restaurant**: the *menu/recipes* are the program (static, reusable). A *restaurant location* is the process (has its own lease, kitchen, stock, staff = resources). A *chef working at the stove* is a thread: they share the kitchen and pantry (address space) with the other chefs, but each has their own knife block (stack) and their own current dish (PC). If one chef burns the food, the whole restaurant suffers (thread crash = process crash) — but a *different* restaurant location (another process) is unaffected.

## 7. Formal Definition
- **Program**: a passive, persistent executable file containing machine code, data, and metadata (ELF/PE), with no execution state.
- **Process**: an executing program instance — the OS's unit of *resource ownership and protection*: independent address space (via `mm_struct`/page tables), file table, credentials, signal disposition, and a PCB.
- **Thread**: the OS's unit of *scheduling/execution* — a lightweight task with its own stack, registers, PC, and scheduling context, sharing the parent process's address space, files, and signals. On Linux, threads and processes are both `task_struct`s; sharing is governed by `clone()` flags (`CLONE_VM`, `CLONE_FILES`, ...).

## 8. Example
```
$ gcc hello.c -o hello        # produces PROGRAM "hello" on disk
$ ./hello &                   # PROCESS "hello" PID 1234, own address space
$ ps -T -p 1234               # threads of that process
  PID  SPID  COMMAND
  1234 1234  hello            # main thread (TID == PID)
  1234 1235  hello            # extra threads from pthread_create
$ ./hello &                   # PROCESS 5678 — independent instance
```
Two processes (1234, 5678) from one program; thread 1235 shares 1234's address space but has its own TID, stack, and registers.

## 9. Internal Working
1. **Program→Process**: `execve` reads the ELF; the kernel maps text/data into a fresh `mm_struct`, sets up `entry`, loads dynamic linker, transfers control. The process now owns page tables, fd table (`files_struct`), creds.
2. **Process→Thread**: `clone(CLONE_VM|CLONE_FILES|CLONE_SIGHAND|...)` allocates a new `task_struct` + kernel stack, copies only the thread's `pt_regs`/stack pointer, *shares* `mm_struct`, `files_struct`, `signal_struct`, `fs_struct` (reference-counted).
3. **Scheduling**: both are tasks on runqueues; a thread switch within a process skips `switch_mm` (same page tables) — cheaper than a process switch.
4. **Failure semantics**: a thread segfault kills the whole process (shared address space); a process crash only kills itself. A program file can be replaced while processes run (the running images persist in memory).

## 10. Time Complexity
- Program load (`exec`): O(image size) + O(relocations).
- Process creation (`fork`): O(1) + O(page tables), COW makes it cheap.
- Thread creation (`clone`): O(1) + O(new stack) — typically 10-100x cheaper than fork+exec.
- Context switch (thread, same process): O(1) — no CR3 switch, no TLB flush.
- Context switch (process): O(1) + TLB/cache warm-up cost.
- Many threads sharing `mm`: memory lock contention grows with thread count (Linux mitigates with per-page locks + RCU).

## 11. Advantages
**Process** (isolation model): fault containment, protection, easy to kill/replace, portable across hosts.
**Thread** (concurrency model): cheap creation/switch, shared memory with no IPC copy, natural for parallel work on shared data, single-process debugging/monitoring.

## 12. Disadvantages
**Process**: expensive creation/switch, no direct memory sharing (IPC overhead), memory duplication (page tables).
**Thread**: no isolation (one thread's bug crashes the process), race conditions on shared data (needs synchronization), harder debugging/stack tracing, signal semantics get complex, can't use processes' isolation guarantees.

## 13. Interview Questions
1. **Q: Difference between program, process, and thread?** A: Program = static code file. Process = executing instance with own address space and resources (unit of isolation). Thread = execution stream within a process, sharing its address space (unit of scheduling).
2. **Q (TRICKY): How many threads does a process have by default?** A: Exactly one (the main thread) unless it creates more. On Linux, a single-threaded process's TID == its PID.
3. **Q: What does a thread share with its process?** A: Address space (code, data, heap), open file descriptors, signal handlers, working directory, user/group IDs. It does NOT share the stack, registers, or PC.
4. **Q: What is the cost difference between creating a process and a thread?** A: Fork duplicates page tables + bookkeeping (COW makes it cheap-ish); thread creation just allocates a new task_struct + kernel stack + user stack, then shares mm — typically an order of magnitude cheaper.
5. **Q: Why is switching between threads cheaper than between processes?** A: Threads share page tables, so `switch_mm`/CR3 reload and TLB flush are skipped — only registers + stack pointer change. Process switch reloads CR3 and pays TLB/cache miss costs.
6. **Q (SCENARIO): A thread crashes (segfault). What happens to the process?** A: The whole process dies (shared address space) — all threads die too. That's the isolation downside of threads; if you want isolation, use processes (or goroutines with recover, or isolate in separate processes).
7. **Q: When would you choose processes over threads?** A: When isolation matters (untrusted input, crash-resilience, security domains — browsers, sandboxes, containers), or you need to survive a child crash. Processes also work across hosts (distributed).
8. **Q: When threads over processes?** A: For fine-grained concurrency on shared data, low-latency creation/context switch, and when IPC copy overhead is unacceptable (in-memory caches, parallel algorithms, request handling).
9. **Q: What is a "lightweight process" (LWP)?** A: Historical term for kernel-scheduled threads; on Linux, all tasks are "threads" in the kernel — the distinction is only in how much they share (`clone` flags).
10. **Q (TRICKY): Can a thread outlive its process?** A: No — when the process exits, its address space is reclaimed and all threads die. (Daemons that "continue after exit" are new processes, not surviving threads.)
11. **Q: How does the kernel represent a thread on Linux?** A: As a `task_struct` (a task) with `CLONE_VM` sharing — pthreads is a library over `clone()`. `gettid()` gives a thread's unique TID; `getpid()` returns the thread-group leader's PID.
12. **Q: What is the thread group and TGID?** A: All threads of one process share a TGID (the PID shown in `ps`); each has a unique TID. Signals are delivered per-thread or per-group depending on the signal.
13. **Q: How do languages map threads?** A: pthreads (C) → 1:1 OS threads; Java → 1:1 (native threads) on Linux; Go → M:N (goroutines on a pool of OS threads); Python → GIL + 1 OS thread per Python thread.
14. **Q (PRODUCTION): Why would you set `ulimit -u`?** A: To cap the number of processes/threads a user can create — prevents fork bombs and runaway thread pools from exhausting PIDs/stack memory.
15. **Q: What does `ps -L` vs `ps -T` show?** A: `ps -L` lists threads with LWP (SPID); `ps -T` the same via SPID — both show the thread-per-process relationship vs plain `ps` (processes only).

## 14. Follow-Up Questions
1. **Q: What is copy-on-write and how does it relate to process vs thread?** A: Fork uses COW so it *appears* to copy everything but shares pages until written — process creation is cheaper than you'd think; threads skip even that by sharing mm directly.
2. **Q: What is a fork bomb and how do you prevent it?** A: A process recursively forking until PIDs/process table exhaust. Prevent with `RLIMIT_NPROC`, cgroup pids.max, and process accounting.
3. **Q: Why do some servers use a thread per connection and others a process per connection?** A: Thread-per-connection = low cost, shared state (but crash-risky); process-per-connection = isolation (Apache prefork) at higher overhead; event-driven (nginx) avoids both.
4. **Q: What is the "fork in a multi-threaded program" problem?** A: Fork duplicates only the calling thread (others vanish); locks held by other threads stay locked in the child → deadlock. Solution: `posix_spawn` or reinitialize locks (pthread_atfork).
5. **Q: What is `vfork`?** A: An older optimized fork that shares memory until exec (dangerous); Linux now implements fork with COW, so vfork is mostly a niche optimization (still faster in some fork+exec loops).

## 15. Coding Example
```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/syscall.h>

void *worker(void *arg) {
    /* thread: shares address space, own TID */
    printf("thread tid=%ld in process pid=%ld\n",
           syscall(SYS_gettid), (long)getpid());
    return NULL;
}

int main(void) {
    pthread_t t;
    pthread_create(&t, NULL, worker, NULL);   /* create a thread (clone CLONE_VM) */
    pthread_join(t, NULL);
    printf("main: process pid=%ld, main-thread tid=%ld\n",
           (long)getpid(), (long)syscall(SYS_gettid));
    return 0;
}
```
```bash
# See the three-way distinction live
ls -l /bin/sleep              # a PROGRAM (file)
sleep 100 &                   # a PROCESS (PID)
ps -o pid,tid,stat,comm -p $! # main thread: pid == tid
echo $! > /proc/sys/kernel/pid_max 2>/dev/null || true
# threads of a process:
ps -T -p $!
kill $!
```

## 16. Industry Usage
- **Production servers**: Postgres = 1 process/connection (isolation) with threads for parallel queries; MySQL = threads; nginx = processes + epoll; Redis = single process/thread event loop.
- **Languages**: Java (1:1 native threads), Go (goroutines, M:N), Node.js (single-threaded event loop + worker threads), Rust (std::thread → pthreads), Python (GIL).
- **Sandboxes**: Chrome = processes per tab (isolation); Android = process per app + Zygote; Docker = process + namespaces/cgroups.
- **Cloud/container orchestration**: Kubernetes pods = process groups with shared namespaces; cgroups limit threads/processes per pod (`pids.max`).
- **Interview angle**: process vs thread is *the* first concurrency question; knowing the sharing matrix (own/shared), cost model, and crash semantics wins the round.

## 17. References
- Silberschatz, *OS Concepts*, Ch. 3.1 (Process Concept), Ch. 4.1 (Threads).
- Tanenbaum, *Modern OS*, Ch. 2.1, 2.2 (Processes, Threads).
- Linux man: `clone(2)`, `fork(2)`, `pthreads(7)`, `gettid(2)`, `ps(1)`.
- Linux source: `kernel/fork.c` (clone flags), `include/linux/sched.h`.
- Love, *Linux Kernel Development*, Ch. 3-4 (Process/Thread Management).

## 18. Cheat Sheet
- Program = static file; Process = executing instance (own address space); Thread = execution stream (shares address space).
- Thread shares: mm (code/data/heap), files, signals, cwd. Owns: stack, regs, PC, TID.
- Thread crash → process crash; process crash → isolated.
- Thread create ~10-100x cheaper than fork+exec.
- Thread switch: no CR3/TLB flush (same mm) → cheaper.
- Linux: thread = task_struct with CLONE_VM; TID vs TGID.
- Chrome = process per tab; MySQL = threads; Postgres = processes.
- `ps -T` / `ps -L` show threads; `/proc/<pid>/task/` lists them.
- ulimit -u / pids.max prevent fork bombs.

## 19. Quiz
1. A thread shares with its process: a) stack b) address space c) PC d) registers → **b**
2. Which is static? a) process b) thread c) program d) PCB → **c**
3. A thread's crash: a) isolated b) kills the process c) kills the kernel d) nothing → **b**
4. Thread context switch skips: a) register save b) TLB/CR3 switch c) stack change d) nothing → **b**
5. On Linux, a thread is: a) a separate process b) a task_struct sharing mm c) a kernel thread d) a signal → **b**
6. TGID is: a) thread id b) process/group leader id c) group of users d) GPU id → **b**
7. `ps -T` shows: a) processes b) threads (SPID) c) kernel modules d) sockets → **b**
8. Process-per-connection wins on: a) speed b) isolation c) memory d) threads → **b**
9. Which is typically cheapest to create? a) process b) thread c) program load d) container → **b**
10. A fork in a multithreaded program: a) clones all threads b) clones only the calling thread → **b**

## 20. Flashcards
- **Q: Program vs process vs thread?** → **A:** Static file / executing instance w/ own address space / execution stream sharing address space.
- **Q: What do threads share?** → **A:** Address space, files, signals; NOT stack/registers/PC.
- **Q: Crash semantics?** → **A:** Thread crash kills its process; process crash is isolated.
- **Q: Why are thread switches cheaper?** → **A:** Same page tables — no CR3/TLB flush.
- **Q: Linux thread representation?** → **A:** task_struct with CLONE_VM; TID vs TGID.
- **Q: Chrome vs MySQL model?** → **A:** Process per tab (isolation) vs threads (concurrency).
- **Q: fork in multithreaded app?** → **A:** Duplicates only calling thread; beware deadlocks (pthread_atfork).
- **Q: How to see threads?** → **A:** ps -T / ps -L; /proc/<pid>/task/.

## 21. Revision
Program = static file; process = executing instance with own address space (unit of isolation); thread = execution stream within a process sharing its address space (unit of scheduling). Threads share code/data/heap, files, and signals but keep their own stack/registers/PC. Thread creation and switching are cheaper (no CR3/TLB churn), but a thread bug kills its whole process. On Linux both are `task_struct`s distinguished by `clone` flags; TID (own) vs TGID (process). Production picks: processes for isolation, threads for shared-memory concurrency.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Program vs process vs thread?" | 7 Formal Definition / 8 Example |
| "What does a thread share?" | 13 Q3 / 9 Internal Working |
| "Thread vs process creation/switch cost?" | 13 Q4-5 / 10 Time Complexity |
| "What happens when a thread crashes?" | 13 Q6 / 12 Disadvantages |
| "Processes or threads for this workload?" | 13 Q7-8 / 16 Industry Usage |
| "What is an LWP?" | 13 Q9 / 4 Why Not |
| "How does the kernel represent threads?" | 13 Q11 / 9 Internal Working |
| "TGID vs TID?" | 13 Q12 / 8 Example |
| "fork in a multithreaded program?" | 14 Follow-Up Q4 / 15 Coding |
| "How to prevent fork bombs?" | 14 Follow-Up Q2 / 16 Industry Usage |
