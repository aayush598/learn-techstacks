# User Threads vs Kernel Threads

> **TL;DR**: User threads are scheduled by a user-space runtime library and invisible to the kernel; kernel threads are scheduled by the OS as real tasks — the distinction determines whether a blocking call stalls the whole process and whether the OS can parallelize your threads across cores.

## 1. Why Does This Exist?
Threads must be implemented *somewhere* — and there are two candidates: the kernel (which sees and schedules them) or a user-space library (which multiplexes them onto fewer kernel schedulable entities). The distinction exists because of a fundamental tension: user threads are **cheap** (no syscalls, no kernel objects — switching is a function call) but **invisible to the OS** (the OS doesn't know they exist, can't parallelize them across cores, and a blocking syscall blocks all of them). Kernel threads are **powerful** (the OS schedules and parallelizes them, and blocking one doesn't block the process) but **costly** (each needs kernel structures and syscalls). Understanding where threads are scheduled explains why some programs parallelize and others stall.

## 2. How Does It Work?
- **User threads (library-level, e.g., old green threads, early Java, or goroutines' user-level coroutines)**: a runtime library (`user thread library`) maintains TCBs, runs its own scheduler in user space, and maps many user threads onto fewer **kernel-level entities** (LWPs/OS threads). Thread switches are context switches *within the library* — just saving/restoring user contexts, no kernel involvement.
- **Kernel threads**: each thread is a kernel task (Linux `task_struct`); creation via `clone`, scheduling via the kernel scheduler (EEVDF), switching via the kernel context switch. The kernel sees and manages each one.
- Modern systems are usually a **hybrid**: the library creates a pool of kernel threads (LWPs) and multiplexes user threads (goroutines/coroutines) onto them — this is the M:N model.

## 3. When Is It Used?
- **User threads**: coroutines/green threads (Go goroutines, Python `asyncio` tasks, old Java green threads, Erlang processes) — used when you want thousands/millions of cheap units and control scheduling yourself.
- **Kernel threads**: classic pthreads (1:1 on Linux), Java native threads, C++ std::thread, kernel-internal tasks (ksoftirqd, kworker — "kernel threads" in the *kernel-internal* sense).
- **Hybrid (M:N)**: Go's GMP scheduler, Java's virtual threads (Project Loom), old Solaris 2 threading, Ruby fibers + threads.

## 4. Why Wasn't Another Approach Chosen?
- **User threads only (N:1)**: cheap but fatal flaw — if *any* user thread blocks in a syscall (e.g., `read`), the OS blocks the whole process (the LWP), stalling *all* user threads. Also can't use multiple cores. This is why early Java green threads were abandoned.
- **Kernel threads only (1:1)**: robust but heavier — each thread is a kernel object (task_struct, stacks), creation is a syscall, and context switches go through the kernel. Fine for moderate thread counts; expensive for millions.
- **Hybrid (M:N)**: best of both but complex — must handle blocking calls (either block an LWP and migrate others, or use async syscalls) and keep scheduler state consistent. Go/JVM virtual threads implement this carefully.
- **No threads (processes only)**: isolation-heavy, no cheap concurrency — rejected (see threads chapter).
The industry chose: **kernel threads as the base (1:1 for pthreads/Java), with user-level multiplexing on top (goroutines, virtual threads)** — you get OS visibility plus cheap units.

## 5. Intuition
User threads are like **gym members sharing one treadmill lane rotation** — the gym staff (OS) only knows about the lane (LWP), and the members (user threads) rotate among themselves. If one member faints and the lane stops (blocking syscall), everyone waits. Kernel threads are like **each member renting their own treadmill** — the staff sees each one, can let them run on different machines (cores), and one fainting doesn't stop the others — but renting costs more.

## 6. Real-World Analogy
A **taxi company**: kernel threads are each *driver with their own cab* — the dispatcher (OS) tracks every cab, can send them to different neighborhoods (cores), and one cab's breakdown doesn't stop the fleet. User threads are *riders sharing a van* (one LWP per van) — cheap and flexible among themselves, but if the van breaks down (blocking syscall), all riders in that van wait; and you can't send riders to different neighborhoods at once.

## 7. Formal Definition
- **User thread**: a thread whose scheduling context is managed by a user-space thread library, multiplexed onto one or more **kernel threads (LWPs)**; invisible to the OS scheduler.
- **Kernel thread**: a thread that the OS kernel schedules as an independent task (Linux `task_struct`, Windows `KTHREAD`), with kernel-visible state and preemption.
- **LWP (lightweight process)**: the kernel-level schedulable entity that carries one or more user threads.
- **N:1**: many user threads on one LWP. **1:1**: each user thread is one kernel thread. **M:N**: M user threads multiplexed onto N LWPs.

## 8. Example
Go program with 10,000 goroutines on a 4-core machine:
- The Go runtime (M:N) creates a few OS threads (GOMAXPROCS, default = #cores = 4) — the kernel sees **4** threads.
- 10,000 goroutines are user threads scheduled by the Go runtime across those 4 threads.
- `ps -L` shows ~4-5 threads (plus runtime helpers), not 10,000 — because goroutines are *user threads*, invisible to the kernel.
- Contrast: Java with 10,000 `new Thread()` = 10,000 kernel threads (1:1) — `ps -L` shows 10,000; creation/switch is heavier; blocking one doesn't block others.

## 9. Internal Working
1. **User-thread switching (N:1 / within one LWP)**: the library saves the current user thread's registers into its TCB and restores the next user thread's — pure user space, ~100ns-1µs, no syscalls, no kernel involvement.
2. **Blocking problem (N:1)**: a user thread calling `read()` issues a syscall that blocks *the whole process/LWP* → all user threads stall until the read returns. Workarounds: async I/O, non-blocking syscalls with a poll loop, or 1:1 mapping.
3. **Kernel-thread creation**: `pthread_create` → `clone(CLONE_VM|...)` syscall → new `task_struct`, scheduled by EEVDF; switching is the kernel context switch (~1-5µs).
4. **M:N multiplexing (Go)**: goroutine blocked → Go scheduler parks it and runs another goroutine on the same OS thread; if all goroutines block in a syscall, the runtime grows an OS thread (thread-splitting) so the process can still progress.
5. **Java virtual threads (Loom)**: virtual threads are user threads on a ForkJoinPool of carrier OS threads; a blocking `synchronized`/I/O parks the virtual thread, not the carrier.
6. **Kernel-internal "kernel threads"**: distinct concept — tasks like `ksoftirqd` run *kernel* code (not user threads at all); don't confuse them with user-thread mapping.

## 10. Time Complexity
- User-thread switch (in-library): ~100ns-1µs — no syscalls.
- Kernel-thread switch: ~1-5µs (kernel context switch, scheduler).
- Kernel-thread create: ~5-20µs (clone syscall).
- User-thread create (goroutine): ~100-300ns (runtime allocation, growable stack).
- N:1 blocking cost: O(blocking syscall duration) for the *whole process*.
- M:N scheduling overhead: O(1) per runnable goroutine (work-stealing queues).

## 11. Advantages
**User threads**: extremely cheap create/switch; can run 100k-1M threads on limited resources; full scheduling control in user space; portable (work without kernel changes).
**Kernel threads**: OS schedules/parallelizes across cores; blocking one doesn't stall the process; kernel-level preemption and priority; debugging/`ps`/cgroup visibility.

## 12. Disadvantages
**User threads**: invisible to OS — no multicore parallelization in N:1; blocking syscall stalls all mapped threads; no preemption if library is cooperative; debugging is harder (OS sees only LWPs).
**Kernel threads**: per-thread kernel overhead (task_struct + stacks + syscalls); context switches via kernel cost more; OS limits (threads-max, stack RSS) at scale; less control over scheduling policy.

## 13. Interview Questions
1. **Q: Difference between user threads and kernel threads?** A: User threads are scheduled by a user-space library and invisible to the OS (multiplexed onto LWPs); kernel threads are OS-scheduled tasks with kernel state. The choice trades cost for visibility/parallelism.
2. **Q: What is an LWP?** A: A lightweight process — the kernel-scheduled entity that carries user threads; in 1:1 it's the thread itself; in N:1 it's the single carrier for all user threads.
3. **Q (TRICKY): Why do user threads have a blocking problem?** A: In N:1, all user threads share one LWP; if any thread issues a blocking syscall (read/write/sleep), the OS blocks the LWP — the whole process's user threads stall. Fix: async I/O, non-blocking + poll, or 1:1/M:N.
4. **Q: What are the three mapping models?** A: Many-to-one (N:1, cheap, blocking stalls process), one-to-one (1:1, OS-scheduled, heavier), many-to-many (M:N, pool of LWPs, complex). Real systems: pthreads=1:1, Go=M:N, old green threads=N:1.
5. **Q: Why did Java abandon green threads?** A: Green threads were N:1 — one blocking syscall stalled the JVM, and multicore CPUs made lack of OS-scheduled parallelism fatal. Java went 1:1 native threads (and is now adding virtual threads = M:N).
6. **Q: Are goroutines kernel threads?** A: No — they're user threads scheduled by the Go runtime over a pool of OS threads (GOMAXPROCS default = #cores). The kernel sees only the OS threads; `ps -L` won't show goroutines.
7. **Q: What is GOMAXPROCS?** A: The number of OS threads Go's scheduler will use simultaneously for running goroutines (default = number of logical CPUs) — the "N" in Go's M:N model.
8. **Q (SCENARIO): Your Go app blocks on a syscall for 100ms. Do all goroutines stall?** A: No — the runtime parks that goroutine and runs others on the same OS thread; if all goroutines are blocked in syscalls, Go grows an OS thread. That's the M:N blocking-handling advantage over N:1.
9. **Q: What's the cost difference between switching user vs kernel threads?** A: User-thread switch ≈ 100ns-1µs (function-call-like, no syscall); kernel-thread switch ≈ 1-5µs (kernel context switch). That's why 1M goroutines is feasible but 1M pthreads is not.
10. **Q: What are "kernel threads" like ksoftirqd?** A: Kernel-internal tasks running kernel code (softirq processing, workqueues) in process-like contexts — different from user threads mapped 1:1. They're scheduled by the kernel and can't be killed.
11. **Q: How do Java virtual threads (Loom) work?** A: Virtual threads are user threads scheduled on a ForkJoinPool of carrier (kernel) threads; a blocking op parks the virtual thread without blocking the carrier — an M:N model giving cheap threads with OS parallelization.
12. **Q (PRODUCTION): When would you prefer kernel threads over user threads?** A: When threads block frequently (real I/O) and you rely on OS scheduling, need core parallelization with preemption, need per-thread OS visibility (debugging, cgroups, affinity), or must interop with C/native code.
13. **Q: What does "cooperative vs preemptive" have to do with user threads?** A: User-space schedulers are often cooperative (yield explicitly) because the library can't preempt an in-flight user thread without a timer signal; kernel threads are preemptive (OS timer interrupt). Cooperative = a stuck thread hangs the whole process.
14. **Q: Can user threads use multiple cores?** A: Only if mapped to multiple LWPs (M:N or 1:1). Pure N:1 user threads use one core. That's the core parallelization argument for kernel threads.
15. **Q (TRICKY): Is Python's threading model user or kernel threads?** A: Python threads are *kernel threads* (1:1, via pthreads), but the **GIL** serializes bytecode execution, so they behave like user threads for CPU work — only one runs at a time. True parallelism needs `multiprocessing` or subinterpreters.

## 14. Follow-Up Questions
1. **Q: What is a thread-splitting / syscall escaping in Go?** A: When a goroutine blocks in a syscall, the runtime may hand that OS thread to a *new* thread and continue other goroutines elsewhere — so the process doesn't stall. The netpoller handles net I/O without splitting.
2. **Q: What is stack growth in goroutines vs fixed pthread stacks?** A: Goroutine stacks start at 2KB and grow dynamically; pthread stacks are fixed (8MB virtual default) — one reason goroutines scale to millions.
3. **Q: What is a fiber?** A: A user-space cooperative thread with manual scheduling (Windows fibers, Boost.Fiber) — N:1-style; the basis of Loom's virtual threads conceptually.
4. **Q: Why do some languages mix (e.g., Ruby, Erlang)?** A: Erlang processes are user-space schedulable entities with their own heaps (M:N); Ruby fibers are N:1; each language chose based on isolation vs cost.
5. **Q: What happens to user threads when the LWP is preempted?** A: The kernel context-switches the LWP away (saving its user registers); the library's user-thread state stays in memory — resumption restores the library's context, not each user thread (they're "frozen" within the LWP).

## 15. Coding Example
```go
// Go: goroutines = user threads over OS threads (M:N)
package main

import (
	"fmt"
	"runtime"
	"sync"
	"time"
)

func work(wg *sync.WaitGroup, id int) {
	defer wg.Done()
	time.Sleep(10 * time.Millisecond) // blocks only this goroutine
	fmt.Printf("goroutine %d on thread %d\n", id, runtime.GOMAXPROCS(0))
}

func main() {
	fmt.Println("OS threads used (GOMAXPROCS):", runtime.GOMAXPROCS(0))
	var wg sync.WaitGroup
	for i := 0; i < 10000; i++ { // 10k user threads, only a few OS threads
		wg.Add(1)
		go work(&wg, i)
	}
	wg.Wait()
}
```
```bash
# The kernel sees a handful of threads, not 10,000 goroutines
./demo &
ps -L -p $(pgrep -n demo) -o pid,tid,comm | wc -l   # ~ 4-6 threads
```
```c
/* pthreads: 1:1 kernel threads — each is an OS task */
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/syscall.h>

void *t(void *a) {
    printf("kernel thread tid=%ld (os task)\n", syscall(SYS_gettid));
    return NULL;
}
int main(void) {
    pthread_t th[4];
    for (int i = 0; i < 4; i++) pthread_create(&th[i], NULL, t, NULL);
    for (int i = 0; i < 4; i++) pthread_join(th[i], NULL);
    return 0;
}
```

## 16. Industry Usage
- **1:1 (kernel threads)**: pthreads (C/C++), Java (classic), Rust std::thread, Windows threads — the default for systems where OS scheduling/blocking semantics matter.
- **M:N (user threads on LWPs)**: Go goroutines, Java virtual threads (Loom, in production since Java 21), Erlang/Elixir processes, Haskell green threads.
- **N:1 (pure user threads)**: legacy green threads (old Java), some fibers; mostly superseded but conceptually instructive.
- **Kernel-internal kernel threads**: Linux ksoftirqd/kworker/migration — scheduled by the kernel, unkillable.
- **Production**: Go services routinely host millions of goroutines on dozens of OS threads; JVM apps use thread pools of kernel threads (or virtual threads); C++ servers use pthread pools.
- **Interview angle**: knowing which model each runtime uses — and why — is a differentiator in backend and systems interviews.

## 17. References
- Silberschatz, *OS Concepts*, Ch. 4.3 (Multithreading Models), Ch. 4.4 (Thread Libraries).
- Tanenbaum, *Modern OS*, Ch. 2.2.2-2.2.3 (User and Kernel threads).
- Linux man: `clone(2)`, `pthreads(7)`.
- Go runtime docs: `runtime` package (GOMAXPROCS), effective Go.
- JEP 425 (Java virtual threads) / JEP 444.
- Love, *Linux Kernel Development* (kernel threads).

## 18. Cheat Sheet
- User threads: library-scheduled, invisible to OS, cheap (100ns switch).
- Kernel threads: OS-scheduled tasks, visible, ~1-5µs switch.
- LWP = kernel entity carrying user threads.
- Models: N:1 (cheap, blocking stalls process), 1:1 (pthreads/Java), M:N (Go/Loom).
- Green threads = N:1; abandoned due to blocking + no multicore.
- Go: M:N, GOMAXPROCS OS threads, growable stacks.
- Java: 1:1 classic; virtual threads (Loom) = M:N.
- ksoftirqd/kworker = kernel-internal threads (different meaning).
- Python: kernel threads + GIL ≈ user-thread behavior for CPU.
- Cooperative user threads can't preempt; a stuck thread hangs the process.

## 19. Quiz
1. User threads are scheduled by: a) the kernel b) a user-space library c) the hardware d) systemd → **b**
2. N:1 means: a) one user thread per LWP b) many user threads on one LWP c) one per core d) none → **b**
3. A blocking syscall in N:1 stalls: a) one thread b) the whole process c) the kernel d) the LWP only → **b**
4. pthreads on Linux are: a) user threads b) 1:1 kernel threads c) N:1 d) M:N → **b**
5. Goroutines are: a) kernel threads b) user threads on OS threads (M:N) c) processes d) fibers only → **b**
6. GOMAXPROCS controls: a) goroutine count b) OS threads Go uses c) memory d) CPU speed → **b**
7. Green threads were abandoned because: a) too slow b) blocking + no multicore c) syntax d) licenses → **b**
8. A user-thread switch costs about: a) 1-5µs b) 100ns-1µs c) 1ms d) 100ms → **b**
9. ksoftirqd is a: a) user thread b) kernel-internal kernel thread c) goroutine d) process → **b**
10. Java virtual threads (Loom): a) 1:1 b) M:N on a ForkJoinPool c) N:1 d) processes → **b**

## 20. Flashcards
- **Q: User vs kernel threads?** → **A:** Library-scheduled invisible tasks vs OS-scheduled visible tasks.
- **Q: LWP?** → **A:** Kernel entity carrying user threads.
- **Q: N:1 blocking problem?** → **A:** A blocking syscall stalls the whole process.
- **Q: Which model is pthreads?** → **A:** 1:1 kernel threads.
- **Q: Go's model?** → **A:** M:N; goroutines on GOMAXPROCS OS threads.
- **Q: Why did green threads fail?** → **A:** N:1 blocking + no multicore parallelism.
- **Q: Loom?** → **A:** M:N virtual threads on carrier threads.
- **Q: Cooperative user threads?** → **A:** Can't preempt; stuck thread hangs process.
- **Q: Python's GIL effect?** → **A:** Kernel threads serialized → user-thread-like for CPU.

## 21. Revision
User threads are scheduled by a library (invisible to the OS, ~100ns switches, cheap); kernel threads are OS tasks (~1-5µs switches, parallelizable, visible). N:1 user threads have the fatal blocking flaw (one blocking syscall stalls the whole process) and can't use multiple cores — why green threads died and pthreads went 1:1. M:N (Go goroutines, Java Loom) gives cheap user threads *and* OS parallelization by multiplexing onto a pool of kernel threads. Know each runtime's model — the kernel sees goroutines as only GOMAXPROCS threads.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "User vs kernel threads?" | 7 Formal Definition / 2 How It Works |
| "What is an LWP?" | 13 Q2 / 7 Formal Definition |
| "Why is the N:1 blocking problem bad?" | 13 Q3 / 12 Disadvantages |
| "The three threading models?" | 13 Q4 / 8 Example |
| "Why did Java drop green threads?" | 13 Q5 / 4 Why Not |
| "Are goroutines kernel threads?" | 13 Q6 / 8 Example |
| "What is GOMAXPROCS?" | 13 Q7 / 9 Internal Working |
| "What are ksoftirqd-type threads?" | 13 Q10 / 9 Internal Working |
| "How do Java virtual threads work?" | 13 Q11 / 9 Internal Working |
| "Python threads + GIL?" | 13 Q15 / 16 Industry Usage |
