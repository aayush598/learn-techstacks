# What is a Process

> **TL;DR**: A process is a program in execution — a dynamic entity with its own address space (text, data, heap, stack), program counter, registers, and kernel bookkeeping; the process is *what the OS schedules*, while the program is merely the *instructions on disk*.

## 1. Why Does This Exist?
A program on disk is inert — it's just bytes. For it to do anything, the OS must give it a *living instance*: memory for its code and data, a stack, a program counter, registers, file descriptors, and an identity. The process concept exists to bundle all of that into one schedulable, protectable unit. It's what lets the OS run *many* instances of the *same* program (two terminals running `bash`), pause and resume them, isolate them from each other, and account for their resource use. Without processes there is no multitasking, no isolation, no concurrency.

## 2. How Does It Work?
- When you run a program, the OS (via `execve`) builds a new **address space** with four regions: **text** (code), **data** (globals), **heap** (dynamic memory), **stack** (function frames).
- The kernel creates a **PCB** (`task_struct` on Linux) recording: PID, state, PC, registers, scheduling priority, memory maps (VMAs), open files, signal handlers, credentials.
- The process's virtual address space is mapped through page tables to physical memory; on x86-64 the layout has user space low (0x0000000000000000–0x00007fffffffffff) and the kernel mapped high.
- The CPU executes the process's instruction stream, advancing the PC; the scheduler later can preempt it, save its context, and run another process.

## 3. When Is It Used?
- **Every program run**: shell → `fork`/`exec` → process.
- **Servers**: each incoming connection may be handled by a process (Apache prefork), a thread (MySQL threads), or async events (nginx/Redis epoll) — the process is still the container.
- **Isolation**: containers (Docker) are processes (plus namespaces/cgroups); cloud functions (AWS Lambda) run as processes in microVMs.
- **Daemons**: sshd, cron, systemd — long-lived background processes.
- **Every tool you use**: `ps`, `top`, `htop` read process table (`/proc`); `kill` signals processes.

## 4. Why Wasn't Another Approach Chosen?
- **No process concept (one big program)**: everything in one address space — impossible to isolate or protect; rejected for general-purpose OSes.
- **Processes with no virtual memory**: each process physically contiguous memory — fragmentation, no protection, no sharing; rejected in favor of paging + virtual address spaces.
- **One process per program file instance, fixed at load**: too rigid; the same binary must run many times with independent state — hence *instance* not *file*.
- **Threads-only model (process is just a thread)**: threads share everything, so isolation is lost — that's why the process (with its own address space) *is* the unit of isolation, and threads are the unit of execution *within* it.
The chosen approach — schedulable, protected, memory-isolated instances of programs — is the Unix model every modern OS follows.

## 5. Intuition
A **program is a recipe book**; a process is a **chef following the recipe right now**. The recipe (text) is static and identical for everyone. But each chef has their own: current page (PC), ingredients on their counter (data/heap), their pan stack (call stack), and their name tag (PID). Two chefs can cook from the same book simultaneously without touching each other's counters — that's two processes from one program. If the OS must freeze one chef and let another cook (context switch), it records every detail of the first chef's station first.

## 6. Real-World Analogy
A **flight booking**: the program is the flight schedule (a document, static). A process is a *specific flight in the air right now* — it has a flight number (PID), a route (memory map), a manifest (files), and a position (PC). Two flights use the same schedule but are completely independent; one crashing (process crash) doesn't affect the other. The air traffic controller (OS) tracks each flight's state (flying, holding, landed) and its position — that's the process's life-cycle and PCB.

## 7. Formal Definition
A **process** is an instance of a program in execution: the context (address space, program counter, registers, open files, signal state, resource accounting) maintained by the OS for one schedulable entity. It consists of (a) an address space (text, data, heap, stack), (b) CPU context (PC, SP, registers), and (c) kernel-managed metadata (PCB). On Linux, a process is represented by `struct task_struct`, with its memory by `struct mm_struct`, open files by `struct files_struct`, and credentials by `struct cred`.

## 8. Example
Run `bash -c "sleep 30"` twice, then observe:
```
$ ps -eo pid,ppid,stat,comm,args | grep -E "sleep|bash -c"
  1234  1200  S   bash     bash -c sleep 30
  1235  1234  S   sleep    sleep 30
  1236  1200  S   bash     bash -c sleep 30
  1237  1236  S   sleep    sleep 30
```
- Two `bash` processes (PIDs 1234, 1236) — two *instances* of the same `/bin/bash` program.
- Each spawned its own `sleep` child (1235, 1237). Each has a distinct PID, state (S = sleeping), and own address space, though they execute the *same* binary text.
- Killing `sleep 1235` (`kill -9 1235`) affects only that process; the other sleep and both shells continue.

## 9. Internal Working
1. **Creation**: `fork()` clones `task_struct` (copy-on-write memory); `execve()` loads a new image into the address space.
2. **Address space**: `mm_struct` → list of `vm_area_struct` (VMAs) describing text/data/heap/stack regions; page tables map VMA → frames.
3. **Execution**: CPU fetches instructions at the PC mapped from the text VMA; heap grows via `brk`/`mmap`; stack grows on demand (page faults).
4. **Scheduling**: the task is on a runqueue; on preemption the scheduler saves `pt_regs` (registers) into `task_struct` and switches `mm` (CR3) and kernel stacks.
5. **Termination**: `exit()` → resources released (memory, files) → PCB stays as **zombie** until parent `wait()` reaps it.
6. **Observation**: `/proc/<pid>/` exposes status (state, pid, ppid), maps, fd, stat, etc., generated on demand by the kernel.

## 10. Time Complexity
- Process creation (`fork`): O(1) amortized for `task_struct` (slab cache) + O(page tables) with COW (usually cheap).
- `exec`: O(image size) — read + map the new binary.
- Address-space switch (context switch between processes): O(1) registers + CR3 reload + TLB/cache warm-up costs.
- `wait`/`exit`: O(1) + O(children) notification.
- Memory: `task_struct` ~ few KB; full process memory = VMA-sum (each process costs pages).

## 11. Advantages
- **Isolation**: each process has a private address space — a crash or bug can't read/corrupt others.
- **Protection**: page-table-level permissions (kernel vs user, read/write/exec) per process.
- **Portability/multitasking**: many programs run concurrently, independent life cycles.
- **Observability & control**: signal, kill, resource-limit, and account per process.
- **Deterministic debugging**: each process is self-contained (gdb attaches per process).

## 12. Disadvantages
- **Creation cost**: fork/exec + page tables is heavier than thread creation.
- **Context-switch cost**: switching address spaces flushes TLB/caches.
- **IPC complexity**: processes can't share memory directly — need pipes/shared memory/sockets (slower than in-process calls).
- **Memory overhead**: per-process page tables and metadata add up under many processes (thousands of containers).
- **Signals/daemon complexity**: managing many processes adds lifecycle complexity (init, reaping, orphan adoption).

## 13. Interview Questions
1. **Q: What is a process?** A: A program in execution — an instance with its own address space (text/data/heap/stack), CPU context, and kernel bookkeeping (PCB); the unit the OS schedules and isolates.
2. **Q: What's in a process's address space?** A: Text (executable code), data (initialized/uninitialized globals), heap (dynamic allocation), stack (call frames); mapped through page tables to physical frames; kernel high-half on x86-64.
3. **Q (TRICKY): If two processes run the same binary, do they share memory?** A: The *text* pages are shared (read-only, mapped by both page tables), but each has its own data/heap/stack; writes are copy-on-write or private. So: shared code, private state.
4. **Q: What's the difference between a process and a program?** A: A program is static bytes on disk (instructions); a process is a dynamic executing instance with state (PC, memory, files). Many processes can run one program.
5. **Q: What is the PCB?** A: The kernel's per-process record: PID/PPID, state, PC, registers, scheduling info, memory maps, file table, credentials, accounting. On Linux: `task_struct`.
6. **Q (PRODUCTION): How do you check how many processes a host has and their states?** A: `ps -eo pid,stat,comm`, `top`, `htop`; `/proc/loadavg`; count via `/proc` (there's a process per directory). State letters: R running, S sleeping, D uninterruptible, Z zombie, T stopped.
7. **Q: What is a PID and how is it allocated?** A: Process identifier — a unique integer; Linux allocates from a bitmap (increasing until wrap), then reuses. PID 1 is `systemd`; PID 2 is `kthreadd`.
8. **Q (SCENARIO): Your service has 10,000 processes and is slow. What's wrong?** A: Likely context-switch overhead + memory overhead (page tables) at that scale; consider threads or an event-driven model (single process, epoll) — the classic process-vs-thread scale question.
9. **Q: What is copy-on-write?** A: `fork` shares pages read-only; the first write page-faults and copies only that page — so fork doesn't copy the whole address space upfront. This is why fork is cheap and fork+exec works well.
10. **Q: What is the relationship between a process and the shell?** A: The shell is itself a process that creates other processes via fork/exec; it's not special — any process can spawn others.
11. **Q (TRICKY): Can a process run without an address space?** A: Kernel threads run without user address space (`mm = NULL`); user processes always have an `mm_struct`. That's a clean way to distinguish kernel threads from normal processes.
12. **Q: What happens to a process's resources at exit?** A: The kernel reclaims memory, closes files, releases locks; the PCB lingers as a zombie until the parent `wait()`s — without reaping, zombies accumulate.
13. **Q: How does the OS keep processes isolated?** A: Virtual memory: each process's page tables map only its own frames; CPU enforces U/S bits; syscalls validate pointers (`copy_from_user`); file access checked by perms/credentials.
14. **Q: What is `/proc/<pid>/`?** A: A virtual directory exposing a process's kernel state: `status` (state/pid/ppid/uid), `maps` (memory regions), `fd/` (open files), `stat`, `cmdline`, `environ`. `ps` and `htop` read exactly this.
15. **Q (PRODUCTION): A process is in `D` (uninterruptible sleep). What does that mean?** A: It's blocked in kernel I/O (e.g., NFS, disk, some device drivers) and can't be killed until the I/O completes — a D-state pileup usually indicates a stuck filesystem/network mount.
16. **Q: What is a process's "executable" vs "process image"?** A: The executable is the ELF file on disk; the process image is the loaded, mapped, linked state in memory (with relocations resolved, dynamic libs mapped) ready to execute.

## 14. Follow-Up Questions
1. **Q: What is a VMA?** A: A virtual memory area — a `vm_area_struct` describing one region of a process's address space (start/end/permissions/backing). The VMA list = the process's memory map (`/proc/<pid>/maps`).
2. **Q: Why does a stack grow down and heap grow up?** A: Convention that lets them share one address space and grow toward each other (guard pages detect overflow); compilers and ABI assume the downward stack.
3. **Q: What is `brk` vs `mmap`?** A: `brk` grows the heap contiguously (fast for small allocs); `mmap` maps arbitrary regions (used for large allocations and shared memory). glibc uses both in `malloc`.
4. **Q: What is the difference between a daemon and a normal process?** A: A daemon is a background process, typically detached from the controlling terminal (setsid, chdir /, umask, closes fds) — started at boot or by systemd.
5. **Q: How do processes share memory on Linux?** A: `mmap(MAP_SHARED)`, SysV `shmget`/`shmat`, or POSIX `shm_open` — mapping the same physical frames into multiple processes' page tables.

## 15. Coding Example
```c
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    printf("I am PID %d, my parent is %d\n", getpid(), getppid());
    pid_t pid = fork();           /* create a new process */
    if (pid < 0) { perror("fork"); return 1; }

    if (pid == 0) {               /* child */
        printf("child:  my PID = %d, parent PID = %d\n", getpid(), getppid());
        return 0;                 /* child exits */
    }

    /* parent */
    int status;
    waitpid(pid, &status, 0);     /* reap the child (avoid zombie) */
    printf("parent: child %d exited with status %d\n", pid, WEXITSTATUS(status));
    return 0;
}
```
```bash
# Observe processes and their address spaces
sleep 100 &
echo "pid: $!"
ls -l /proc/$!/exe /proc/$!/fd/          # the executable and open files
cat /proc/$!/status | grep -E "State|Pid|PPid|VmSize|VmRSS"
head -20 /proc/$!/maps                   # the address space layout (VMAs)
kill $!
```

## 16. Industry Usage
- **Linux**: `kernel/fork.c` (fork), `fs/exec.c` (execve), `include/linux/sched.h` (task_struct), `fs/proc/` (procfs). All cloud workloads, containers (runc = clone + exec), Android (Zygote forks apps).
- **Windows NT**: `nt!PspCreateProcess`, `EPROCESS`/`KPROCESS`; process = object with token, handles, address space.
- **macOS/XNU**: `proc` structures; launchd (PID 1).
- **Production patterns**: pre-forking web servers (Apache prefork, gunicorn) use many processes; Postgres forks a backend per connection; systemd manages processes as units with cgroups.
- **Distributed/runtimes**: Go runtime uses OS *processes* for the toolchain but goroutines in-process; Kubernetes pods = process groups with shared namespaces.
- **Interview angle**: process concepts underpin fork-based concurrency, process-per-request scalability, and the "why threads not processes" debate — asked everywhere.

## 17. References
- Silberschatz, *OS Concepts*, Ch. 3 (Processes).
- Tanenbaum, *Modern OS*, Ch. 2 (Processes and Threads).
- Linux man: `fork(2)`, `execve(2)`, `proc(5)`.
- Linux source: `include/linux/sched.h`, `kernel/fork.c`, `fs/exec.c`, `fs/proc/base.c`.
- Love, *Linux Kernel Development*, Ch. 3 (Process Management).

## 18. Cheat Sheet
- Process = program in execution: address space + CPU context + PCB.
- 4 segments: text, data, heap, stack.
- Program is static; process is dynamic; two processes can run one binary.
- PCB = task_struct on Linux; contains PID, state, PC, regs, mm, files, cred.
- COW: fork shares pages, copies on write — fork is cheap.
- Kernel threads have no user address space (mm == NULL).
- `/proc/<pid>/` exposes status, maps, fd.
- D-state = uninterruptible kernel I/O sleep.
- Stack grows down; heap up; guard pages between.
- Isolation via page tables + U/S bits + syscall pointer validation.

## 19. Quiz
1. A process is: a) a file b) a program in execution c) a thread d) a PCB → **b**
2. Which is NOT a process segment? a) text b) data c) heap d) inode → **d**
3. Two processes running the same binary share: a) heap b) stack c) text pages (read-only) d) files → **c**
4. Kernel threads have: a) a full mm_struct b) no user address space c) a stack only d) a TTY → **b**
5. Copy-on-write makes fork: a) impossible b) cheap c) slow d) recursive → **b**
6. `/proc/<pid>/maps` shows: a) open files b) memory regions (VMAs) c) signals d) CPU time → **b**
7. A D-state process is: a) dead b) in uninterruptible kernel I/O c) stopped d) running → **b**
8. The kernel process bookkeeping struct on Linux: a) PCB b) task_struct c) cred d) fs_struct → **b**
9. A program is: a) dynamic b) static bytes c) always running d) a thread → **b**
10. The shell creating a process uses: a) mmap b) fork+exec c) pthread_create d) io_uring → **b**

## 20. Flashcards
- **Q: Define process.** → **A:** Program in execution with own address space, CPU context, and PCB.
- **Q: Process segments?** → **A:** Text, data, heap, stack.
- **Q: Program vs process?** → **A:** Static file vs dynamic executing instance.
- **Q: Linux PCB struct?** → **A:** task_struct (mm_struct, files_struct, cred).
- **Q: Why is fork cheap?** → **A:** Copy-on-write — pages shared, copied on first write.
- **Q: Kernel threads' memory?** → **A:** No user address space (mm == NULL).
- **Q: `/proc/<pid>/status`?** → **A:** Process state, PID, PPID, memory, creds.
- **Q: D-state?** → **A:** Uninterruptible kernel I/O sleep; not killable.
- **Q: Isolation mechanisms?** → **A:** Page tables, U/S bits, syscall validation.

## 21. Revision
A process is a program in execution: its own address space (text/data/heap/stack), CPU context, and PCB (Linux `task_struct`). Programs are static; processes are dynamic instances — many processes may run one binary (shared text, private state). `fork` uses copy-on-write so creation is cheap; kernel threads have no user address space; isolation comes from page tables, U/S bits, and validated syscalls. `/proc/<pid>/` exposes the whole picture. Process vs program vs thread is the opening distinction of most OS interviews.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a process?" | 7 Formal Definition / 5 Intuition |
| "What's in the address space?" | 13 Q2 / 9 Internal Working |
| "Do two processes share memory?" | 13 Q3 / 4 Why Not |
| "Process vs program?" | 13 Q4 / 8 Example |
| "What is the PCB?" | 13 Q5 / 2 How It Works |
| "How do you inspect processes in prod?" | 13 Q6 / 16 Industry Usage |
| "What is copy-on-write?" | 13 Q9 / 4 Why Not |
| "Kernel threads vs processes?" | 13 Q11 / 9 Internal Working |
| "Why is my 10k-process host slow?" | 13 Q8 / 12 Disadvantages |
| "What is D-state?" | 13 Q15 / 16 Industry Usage |
