# Process Control Block (PCB)

> **TL;DR**: The PCB is the kernel's per-process data structure that stores everything the OS needs to manage one process (state, registers, memory, files, priority) — it's the process's "identity card" and the anchor for context switching.

## 1. Why Does This Exist?
Without a PCB, the OS would have nowhere to store a process's saved registers and memory info, so it could never pause and resume a process (context switching would be impossible). It exists because a process is a *dynamic, changing* entity that must be suspended and resumed. The PCB also centralizes: identity (PID/PPID), credentials (who owns it), resources (files, memory), and accounting (CPU time) — one record the scheduler, signal subsystem, debugger, and `/proc` all consult.

## 2. How Does It Work?
Every process has exactly one PCB, created at process creation (`fork`/`clone`) and freed at termination (after reaping). On every context switch, the OS saves the outgoing process's state into its PCB and loads the incoming process's state from its PCB. The PCB is linked into multiple structures simultaneously: the global process list (all tasks), runqueues (ready tasks), wait queues (blocked tasks), and per-parent child lists.

## 3. When Is It Used?
- On `fork()`/`exec()` in Linux (PCB = `task_struct`).
- On every timer interrupt (scheduler tick → look up runqueue).
- On I/O waits (block → enqueue PCB in a wait queue).
- On signals, `kill`, ptrace, seccomp, resource accounting.
- On process exit (zombie PCB kept until reaped).
- In debugging: `ps`, `/proc/<pid>/` reads PCB-derived data.

## 4. Why Wasn't Another Approach Chosen?
Alternative: store process state inline in the process's own memory. Rejected because the process may be suspended, swapped out, or not resident — the OS needs *its own* protected, always-available structure. Alternative: one giant global process table (early Unix). Rejected for cache locality and scalability — per-process PCBs linked into per-CPU structures scale better and localize hot data. Alternative: fully separate structs with no "one object" (Linux partially does this — `task_struct` plus `mm_struct`, `files_struct`, `cred`, `signal_struct` — but they're all anchored from `task_struct`, giving one identity record). The chosen approach: a compact per-process control block owned by the kernel.

## 5. Intuition
Think of a passenger who keeps getting on and off a train. The station master's clipboard (PCB) records exactly where each passenger is, their seat, destination, and ticket — so they can be resumed perfectly when the next train arrives. The process is the passenger; the CPU is the train; the clipboard is the PCB. Every time the passenger leaves the train, the clipboard is updated; every time they board, it's consulted.

## 6. Real-World Analogy
A **bookmark / save-game slot**: a PCB is like a "save game" in a video game — it stores the full state (position, health, inventory = registers, stack, files) so the game can be paused and resumed exactly where it left off. Without the save slot, the game must be restarted from scratch after every pause — the OS equivalent of no context switching.

## 7. Formal Definition
A **process control block (PCB)**, also called task control block (TCB) in RTOSes, is a kernel-maintained data structure that contains the complete context of a process: process ID (PID), process state, program counter, CPU registers, scheduling information (priority, accounting), memory-management information (page tables, VMAs), file-table information (open files), and accounting/I-O status information. On Linux it is `struct task_struct` (with `mm_struct`, `files_struct`, `fs_struct`, `cred`, `signal_struct` anchored from it); on Windows, `EPROCESS`/`KPROCESS`; on FreeRTOS, `TCB_t`.

## 8. Example
`fork()` producing PID 2345 (child of 2344):
1. Parent calls `fork()` → kernel `_do_fork()` → `copy_process()`.
2. `dup_task_struct()` allocates a fresh `task_struct` from the slab cache.
3. Fields copied from parent; new PID assigned (`alloc_pid`); state set to ready/running; `mm` copied via COW (shares pages); `files`/`fs`/`cred` duplicated (reference-counted).
4. New task linked into the global list and runqueue; `wake_up_new_task`.
5. Returns PID 2345 to parent, 0 to child.
`/proc/2345/status` now shows State, Pid, PPid, Uid, VmSize, etc., all read from the PCB.

## 9. Internal Working
1. **Allocation**: `dup_task_struct` → `kmem_cache_alloc(task_struct_cachep)`; also `alloc_thread_info` for kernel stack; PID from `pid.c`'s bitmap.
2. **Initialization**: copy parent's `pt_regs` (registers), set `state = TASK_RUNNING`, `stack = new kernel stack`, `mm` via `copy_mm` (COW), `files`/`fs`/`cred`/`signal` via `copy_files`/`copy_fs`/`copy_creds` (shared or cloned per flags), `sched` fields from parent.
3. **Linking**: `list_add` into global task list; `enqueue_task` into runqueue; `SET_LINKS` into parent's children list.
4. **Use during scheduling**: `pick_next_task` → `context_switch()`: `switch_to()` saves callee-saved regs + SP into old task's `thread` struct, loads new task's; `switch_mm` updates CR3; TLB may flush.
5. **Use during wait**: block → `__schedule` with `state = TASK_INTERRUPTIBLE`; on wake, `wake_up` → `try_to_wake_up` → `enqueue_task`.
6. **Exit**: `do_exit` → `exit_mm`/`exit_files` free resources → `state = EXIT_ZOMBIE` → parent `wait()` → `release_task` → `task_struct` freed.

## 10. Time Complexity
- Create: O(1) amortized (slab cache for `task_struct`).
- Context switch: O(1) — fixed number of register save/loads (no per-size scan).
- Scheduler lookup: O(1) amortized pick-next with EEVDF; O(log n) worst case (rbtree).
- PID allocation: O(1) amortized (bitmap).
- Exit/reap: O(1) per task.
- Memory: `task_struct` ≈ 2-3 KB on x86-64 Linux; kernel stack ≈ 16 KB.

## 11. Advantages
- Enables preemptive multitasking and context switching.
- Centralizes state → decouples process execution from any one CPU (migration).
- Provides isolation bookkeeping: each process's resources are tracked from one object.
- Observable: `/proc`, `ps`, and debuggers all read it.
- Foundation for RTOS determinism (TCB is the only per-task state).

## 12. Disadvantages
- Overhead: PCB allocate/free + context-switch cost (register saves, TLB flush, cache misses).
- Memory: a few KB per process × many processes adds up (10k containers → ~hundreds of MB).
- Fixed-size fields waste memory; huge structs (`task_struct` ~hundreds of fields) hurt cache locality.
- Sharing between CPU cores requires synchronization (runqueue locking, RCU) — contention under many threads.

## 13. Interview Questions
1. **Q: What is a PCB and what does it store?** A: The kernel's per-process control block — PID/PPID, state, program counter, registers, scheduling priority, memory info (page tables/VMAs), open files, credentials, signal handlers, accounting. Linux: `task_struct`.
2. **Q: When is a PCB created and destroyed?** A: Created at `fork`/`clone` (new process), destroyed after `exit` + `wait` (reap). A zombie keeps its PCB until reaped.
3. **Q (TRICKY): Does a thread have its own PCB?** A: A thread is a task in Linux — each thread has its own `task_struct` (a "task"), but threads *share* `mm_struct` (address space) and `files_struct` with their process. So: separate PCB, shared resources.
4. **Q: What does a context switch do to the PCB?** A: Saves the outgoing task's registers/PC/SP into its PCB (via `thread` struct), loads the incoming task's, and updates `mm` (CR3). The PCB is the source/target of every switch.
5. **Q: Where is the PCB stored?** A: In kernel memory, not process memory (the process may be swapped). Allocated from the kernel slab cache; linked into global list + runqueue/wait queues.
6. **Q (PRODUCTION): How do you inspect a process's PCB from user space?** A: Via `/proc/<pid>/` — `status`, `stat`, `maps`, `fd/`, `sched`, `cgroup` — the kernel formats PCB fields into these virtual files. `ps`, `top`, `htop` do exactly this.
7. **Q: What's the difference between `task_struct` and `mm_struct`?** A: `task_struct` = the whole PCB (identity, state, regs, scheduling, refs). `mm_struct` = only the memory-management part (page tables, VMAs). One `mm_struct` can be shared by many threads.
8. **Q (SCENARIO): You fork 100k times and get EAGAIN. What limit was hit?** A: Either `pid_max` (PID space), `kernel.threads-max`, `RLIMIT_NPROC`, or memory (slab + kernel stacks). Each `task_struct`+stack costs KBs — the PCB is why process counts are bounded.
9. **Q: What is stored in the PCB vs the kernel stack?** A: PCB = long-term identity/state/resources; kernel stack = the *active* call stack while executing in kernel mode (syscall frames, pt_regs at the top). They're separate; the kernel stack can be found from `task_struct.stack`.
10. **Q: How does the scheduler find the next process's PCB?** A: The runqueue stores pointers to `task_struct`s (EEVDF rbtree keyed by vruntime); `pick_next_task` returns one; the context switch then uses it.
11. **Q (TRICKY): Is the PCB shared between CPUs?** A: The same PCB object moves between per-CPU runqueues as tasks migrate; hot fields are read by whichever CPU runs the task. Per-CPU data (`current` via `current_thread_info`) makes lookup O(1) — that's why `current` works on any CPU.
12. **Q: What is `current` on Linux?** A: A macro resolving the running task's `task_struct` — historically from the kernel stack pointer (`current_thread_info`), now from a `percpu` variable. It's how kernel code answers "who am I?"
13. **Q: What happens to the PCB when a process is swapped out?** A: The `mm_struct`'s pages may move to swap (the task keeps its PCB in memory — the PCB itself isn't swapped; only user memory is). That's why the OS can resume it.
14. **Q: What does `wait()` do with a zombie's PCB?** A: `wait` collects the exit status, then `release_task` frees the `task_struct`, `mm_struct`, and related structures — the PID becomes reusable.
15. **Q (PRODUCTION): Why would `/proc/<pid>/status` show huge VmSize for a small program?** A: `VmSize` is the *virtual* size (all mapped regions, including shared libs and reservations); `VmRSS` is resident. Both are read from the PCB's mm info — a common source of "why is my process using so much memory" confusion.
16. **Q: How does a debugger (gdb) use the PCB?** A: `ptrace` lets gdb read/write the child's registers and memory through the kernel, which accesses the PCB (`pt_regs`, `mm`). The PCB is the interface for process inspection.

## 14. Follow-Up Questions
1. **Q: What is `thread_info` vs `task_struct`?** A: Historically `thread_info` held flags + the pointer to `task_struct` and lived at the bottom of the kernel stack (fast `current` lookup); modern Linux stores it in `task_struct` itself on many arches, with `current` via `percpu`.
2. **Q: What is `pt_regs`?** A: A struct holding the saved user registers at syscall/exception entry, stored at the top of the kernel stack frame; the PCB's register "image" during syscalls.
3. **Q: Why is the kernel stack per-task and small (16KB)?** A: It's allocated per task (so we can preempt without touching user stack); kept small to save memory (16KB × 100k tasks = 1.6GB) — deep recursion/`-fstack-protector` bugs overflow it.
4. **Q: How do RTOS TCBs differ from Linux task_struct?** A: FreeRTOS `TCB_t` is tiny (stack ptr, state, priority, timers, ~100 bytes) — no VM, no files; determinism comes from its small fixed size.
5. **Q: What is `copy_process` vs `copy_mm`?** A: `copy_process` is the whole PCB-copying pipeline in `kernel/fork.c`; `copy_mm` is the sub-step that clones (COW) or shares the address space depending on `CLONE_VM`.

## 15. Coding Example
```c
/* Minimal PCB-like structure (conceptual C) */
struct my_pcb {
    pid_t pid;
    pid_t ppid;
    int   state;              /* 0=ready 1=running 2=waiting 3=zombie */
    uint64_t pc;              /* program counter */
    uint64_t regs[32];        /* saved registers (context) */
    uint64_t *stack;          /* saved stack pointer */
    int      priority;
    uint64_t vruntime;        /* scheduler key */
    struct page *pgd;         /* page table pointer */
    struct file **fds;        /* open file table */
    uid_t    uid, euid;       /* credentials */
    uint64_t utime, stime;    /* accounting */
};
```
```c
/* Linux: reading a process's PCB fields via /proc (userspace) */
#include <stdio.h>
int main(int argc, char **argv) {
    if (argc < 2) return 1;
    char path[64];
    snprintf(path, sizeof path, "/proc/%s/status", argv[1]);
    FILE *f = fopen(path, "r");
    char line[128];
    while (fgets(line, sizeof line, f))
        if (strncmp(line, "State", 5) == 0 || strncmp(line, "Pid", 3) == 0 ||
            strncmp(line, "PPid", 4) == 0 || strncmp(line, "VmRSS", 5) == 0)
            printf("%s", line);
    fclose(f);
    return 0;
}
```

## 16. Industry Usage
- **Linux**: `include/linux/sched.h` (`task_struct`), `kernel/fork.c` (`copy_process`), `kernel/sched/core.c`, `kernel/exit.c`, `fs/proc/base.c`. Every cloud/container host uses it.
- **Windows**: `EPROCESS` (executive) + `KPROCESS` (kernel) + `ETHREAD`/`KTHREAD`; Process Explorer reads them.
- **macOS/XNU**: `proc` + `uthread` structs.
- **FreeRTOS**: `TCB_t` — the TCB is the heart of every task API.
- **Production patterns**: `/proc`-based monitoring (node_exporter), thread-per-request servers, `RLIMIT_NPROC` tuning, OOM accounting — all PCB-driven.
- **Interview angle**: PCB/task_struct is the concrete answer to "what happens in fork" and "what does a context switch save."

## 17. References
- Silberschatz, *OS Concepts*, Ch. 3.1.3 (Process Control Block).
- Tanenbaum, *Modern OS*, Ch. 2.1.2 (Process Control Blocks).
- Linux source: `include/linux/sched.h`, `kernel/fork.c`, `arch/x86/include/asm/thread_info.h`.
- Love, *Linux Kernel Development*, Ch. 3 (Process Management).
- `proc(5)` man page.
- Russinovich, *Windows Internals* (EPROCESS/KPROCESS).

## 18. Cheat Sheet
- PCB = process identity card / save-game slot; Linux = `task_struct`.
- Created on fork, freed on exit+reap; zombie keeps PCB.
- Contents: PID, state, PC, registers, scheduler info, mm info, files, cred, accounting.
- Stored in kernel memory (slab), NOT process memory.
- Thread = own task_struct but shared mm/files.
- Context switch = save to PCB, load from PCB, switch CR3.
- `current` macro = the running task's task_struct.
- `VmSize` (virtual) vs `VmRSS` (resident) from PCB mm info.
- `task_struct` ≈ 2-3KB; kernel stack 16KB.
- RTOS: TCB_t; Windows: EPROCESS/KPROCESS.

## 19. Quiz
1. Which is NOT stored in the PCB? a) PC b) heap data c) registers d) PID → **b**
2. Linux's PCB struct is: a) mm_struct b) task_struct c) cred d) pt_regs → **b**
3. A zombie's PCB: a) is freed b) is kept until reap c) is swapped d) is shared → **b**
4. Threads sharing a process share: a) task_struct b) mm_struct c) PID d) stack → **b**
5. The PCB lives in: a) user heap b) kernel memory c) disk d) the process's stack → **b**
6. `current` gives you: a) PID b) the running task's task_struct c) the CPU d) time → **b**
7. Context switch saves into: a) kernel stack only b) the PCB c) user memory d) swap → **b**
8. Creating a PCB is O(1) amortized thanks to: a) buddy b) slab cache c) rbtree d) memcpy → **b**
9. `VmRSS` shows: a) virtual size b) resident memory c) file size d) swap → **b**
10. FreeRTOS calls its PCB: a) TCB_t b) task_struct c) EPROCESS d) proc → **a**

## 20. Flashcards
- **Q: What is a PCB?** → **A:** Kernel per-process struct (Linux task_struct) with full context.
- **Q: Where does the PCB live?** → **A:** Kernel memory (slab), not process memory.
- **Q: When freed?** → **A:** After exit + wait (reap); zombie keeps it.
- **Q: Threads' PCBs?** → **A:** Own task_struct, shared mm_struct/files_struct.
- **Q: What does context switch touch?** → **A:** PCB regs, kernel stack, CR3/page tables.
- **Q: `current`?** → **A:** Macro for the running task's task_struct (percpu).
- **Q: How to read a PCB in prod?** → **A:** /proc/<pid>/ (status, stat, maps, fd).
- **Q: task_struct size?** → **A:** ~2-3KB; kernel stack 16KB.

## 21. Revision
The PCB (Linux `task_struct`) is the kernel's per-process record: identity, state, registers, scheduler info, memory, files, credentials, accounting. Created on fork (slab cache, O(1) amortized), freed on exit+reap; zombies keep it. Threads each get a `task_struct` but share `mm_struct` and `files_struct`. Context switching saves/loads the PCB and switches CR3. It lives in kernel memory, is observable via `/proc/<pid>/`, and `current` resolves the running task's PCB. This is the data structure behind fork, scheduling, signals, and debugging.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a PCB?" | 7 Formal Definition / 8 Example |
| "What does a context switch save?" | 13 Q4 / 9 Internal Working |
| "Do threads have PCBs?" | 13 Q3 / 4 Why Not |
| "Where is the PCB stored?" | 13 Q5 / 9 Internal Working |
| "How to inspect a PCB in production?" | 13 Q6 / 16 Industry Usage |
| "Why EAGAIN on many forks?" | 13 Q8 / 10 Time Complexity |
| "task_struct vs mm_struct?" | 13 Q7 / 2 How It Works |
| "What is `current`?" | 13 Q12 / 14 Follow-Up Q1 |
| "What does wait() do to the PCB?" | 13 Q14 / 9 Internal Working |
| "VmSize vs VmRSS?" | 13 Q15 / 16 Industry Usage |
