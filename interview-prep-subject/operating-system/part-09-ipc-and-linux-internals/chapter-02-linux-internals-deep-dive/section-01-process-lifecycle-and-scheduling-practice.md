# Process Lifecycle and Scheduling Practice

> **TL;DR**: In Linux a "process" is a `struct task_struct`. `fork`/`clone` copy the parent copy-on-write (sharing mm/files until written), `exec` builds a fresh address space and loads a program, `exit` turns the process into a **zombie** reaped by `wait`. The **CFS** scheduler picks the next `sched_entity` via a red-black tree keyed by `vruntime` to give fair CPU share.

## 1. Why Does This Exist?
The OS must (a) represent every running program (state: regs, memory, fds, credentials), (b) create processes efficiently — copying an entire address space on `fork` would be impossibly slow, so **copy-on-write** defers copying until a page is actually written, (c) replace a process's image cleanly via `exec`, (d) clean up on exit without leaking resources (hence zombies + `wait`), and (e) schedule all runnable tasks fairly and responsively. `task_struct` + COW fork + CFS is Linux's concrete answer to Parts 02–03's abstractions.

## 2. How Does It Work?
**`struct task_struct`** (`include/linux/sched.h`) — the process/thread descriptor:
- Thread-local state: `thread_info`/kernel stack, pt_regs (saved regs), `pid`/`tgid`, state.
- Scheduling: `sched_entity` (vruntime), `prio`, `static_prio`, `sched_class` (fair/rt/deadline/idle), `cpus_allowed`.
- Memory: `mm` (address space), `active_mm`.
- Files: `fs` (root/cwd), `files` (fd table).
- Signals: `signal`, `sighand`, `pending`.
- Credentials: `cred` (uid/gid/caps). Tree: `parent`, `children`, `sibling`, `thread_group`.

**`fork`/`clone`** (`kernel/fork.c`):
1. `copy_process` → `dup_task_struct` (copy task_struct, new kernel stack) → copy each subsystem per `CLONE_*` flag:
   - `CLONE_VM` → share `mm` (threads); else `copy_mm` → new mm with **copy-on-write** page tables (`dup_mmap` — pages shared, `VM_WRITE` becomes CoW) via `copy_page_range` → PTEs marked read-only for writable pages.
   - `CLONE_FILES` → share `files` (fd table); `CLONE_FS` → share cwd/root; `CLONE_SIGHAND`/`CLONE_THREAD` → share sighand/thread group.
2. `wake_up_new_task` → put on run queue. Child returns 0; parent returns child's pid.

**`exec`** (`fs/exec.c`): `do_execve` → load ELF (`load_elf_binary`): flush old mm (`flush_old_exec`), map PT_LOAD segments (text/data, with page permissions), set stack, push argv/envp, `elf_entry` → starts at `_start`/dynamic loader → `main`.

**`exit`** (`kernel/exit.c`): `do_exit` → `exit_mm`/`exit_files`/`exit_fs`, send SIGCHLD, set state to `EXIT_ZOMBIE`, parent `wait4` reads exit status → `release_task` frees task_struct. If parent died first → reparented to init/subreaper (PID 1). Orphaned-but-zombie → init reaps.

**CFS scheduling** (`kernel/sched/fair.c`): run queue = red-black tree of `sched_entity`s keyed by `vruntime`. `vruntime += delta_exec * NICE_0_LOAD / weight`. Pick the leftmost (smallest vruntime) node → fair share. `wakeup_preempt` (EEVDF/earliest-deadline evolution) preempts when needed. `sched_class` hierarchy: deadline > RT > CFS (fair) > idle.

## 3. When Is It Used?
- **Any program run**: shell `fork`+`exec`; daemons; containers use clone with `CLONE_NEWNS/...` (namespaces).
- **Threads**: `pthread_create` = `clone` with `CLONE_VM|CLONE_FILES|CLONE_SIGHAND|CLONE_THREAD`.
- **CoW**: `fork` followed by `exec` (the common case) is cheap — no copying before exec.
- **Zombies**: a parent that doesn't `wait` leaves zombies; PID 1 (or a subreaper) reaps orphans.
- **Scheduling**: every context switch goes through CFS/RT/deadline classes; `nice`, `taskset`, `chrt` tune it.

## 4. Why Wasn't Another Approach Chosen?
- **Eager fork copy (rejected)**: `fork`+`exec` in shells would copy gigabytes for nothing — COW makes fork O(1)-ish.
- **vfork (historical)**: shares parent's mm entirely (no CoW) — child must not write; fast for exec-only, but dangerous and now rare (still used in early exec paths).
- **Posix_spawn (chosen for some)**: a library call that does fork+exec efficiently in-process — used by glibc for `system`, golang, and others to avoid fork overhead in multi-threaded programs.
- **Single priority queue (rejected)**: CFS's rbtree gives O(log n) insertion and true fair share vs O(n) scans.
- **O(1) scheduler (previous)**: was complexity-bound, poor fairness; CFS (fair scheduler) replaced it in 2.6.23.

## 5. Intuition
**fork = cloning a document with a "write → make your own copy" rule**: the child initially shares every page with the parent; the first time either writes a page, the OS duplicates just that page. So `fork` is nearly free. **exec = tearing up the old document and writing a completely new one** — no point copying pages that will be discarded. **exit = handing the paper in and getting a receipt (zombie) until the grader (parent) records the grade (wait)**. **CFS = a fair cafeteria** where everyone's "time served" (vruntime) is tracked and the least-served person goes next — the person who ate the least gets priority.

## 6. Real-World Analogy
**A busy print shop**:
- **fork**: you photocopy your master sheet — but the copier is lazy: it stamps "shared — copy on first edit" and only actually photocopies a page when someone writes on it (COW). Starting a second run from the same master is nearly instant.
- **exec**: the boss hands you a brand-new master to work on — you throw out the old sheets and load the new one.
- **exit/zombie**: when a worker finishes, they don't vanish instantly — they stay at the desk as a "finished" marker until the supervisor (parent) records the outcome and lets them go (wait/reap). If the supervisor leaves, the front-desk person (init) clears them.
- **CFS**: the scheduling board ranks everyone by "least time worked" and always sends the least-worked person to the next machine — fair to all, and nobody starves.

## 7. Formal Definition
**task_struct**: the process descriptor containing identity (pid/tgid/ppid), state (TASK_RUNNING/INTERRUPTIBLE/UNINTERRUPTIBLE/STOPPED/TRACED/DEAD/ZOMBIE), scheduling (sched_entity, prio, sched_class, policy), mm/files/fs/signal/cred references, and linkage. **fork** = `copy_process` (duplicate task_struct + per-flag subsystem copies) + `wake_up_new_task`. **COW**: `dup_mmap`→`copy_page_range` marks writable PTEs read-only and installs a page fault handler that duplicates on write (`handle_mm_fault`/`do_wp_page`). **exec** = `do_execve`→`load_elf_binary` (new mm from PT_LOAD segments, entry point). **exit** = `do_exit` (release resources, SIGCHLD, zombie) → `wait` (read exit code) → `release_task`. **CFS**: run queue is an rbtree keyed by `vruntime` (`entity_key`), min-vruntime = leftmost; `update_curr` accumulates `vruntime += (delta_exec * NICE_0_LOAD) / se->load.weight`; fairness ≈ each task's CPU proportion matches its weight.

## 8. Example
`bash` runs `ls`:
1. `bash` calls `fork` → `copy_process`: new task_struct, `copy_mm` (COW page tables — bash's ~10 MB of pages shared), `CLONE_FILES` off → copied fd table (fds point to the same open files). Child pid 1234.
2. Child calls `execve("/bin/ls", ...)` → `load_elf_binary`: `flush_old_exec` drops the COW'd bash mm; maps ls's text/data; sets stack with argv; jumps to loader/`_start`; COW'd bash pages now unreferenced → freed. Parent's pages untouched (no copy happened!).
3. `ls` runs, writes to stdout (fd 1), calls `_exit(status)` → `do_exit` → zombie 1234.
4. `bash` calls `wait4(1234)` → reads status → `release_task` → zombie reaped.
Threads: `pthread_create` → `clone(CLONE_VM|CLONE_FILES|CLONE_SIGHAND|CLONE_THREAD)` → shares mm/files/signal; `getpid` returns same tgid; `gettid` distinct.

## 9. Internal Working
1. `fork`: `sys_fork`/`kernel_clone` → `copy_process`: `dup_task_struct` (new kernel stack, thread_info), then `copy_sighand`, `copy_signal`, `copy_mm` (fork COW), `copy_fs`, `copy_files`, `copy_namespaces`, `copy_creds` (if requested). Add to pidhash, link to parent's children. Return via `set_child_tid` (pid in child).
2. COW page fault: a write to a shared page → `do_wp_page` → allocate a new page, copy contents, update PTE to read-write → retry. (Parent/child each get their own copy — that's the "copy on write".)
3. `exec`: `do_execve` → `bprm` setup → `exec_binprm` → `search_binary_handler` → `load_elf_binary`: `elf_map` PT_LOAD, `set_brk` for bss, setup_auxv, `start_thread` → new entry.
4. `exit`: `do_exit` → `exit_signals`, `exit_mm` (last reference frees), `exit_files`/`exit_fs`, notify parent (SIGCHLD + wake), `EXIT_ZOMBIE`. `wait4` in parent → `wait_task_zombie` collects status → `release_task` (`free_task`).
5. CFS: `enqueue_task_fair`/`dequeue_task_fair` → rb_insert/rb_erase; `pick_next_task_fair` → `__pick_first_entity` (leftmost). `scheduler_tick` → `task_tick_fair` updates vruntime, maybe `resched_curr`. Context switch → `__schedule` → `context_switch` (switch mm via `switch_mm`, switch regs via `switch_to`).

## 10. Time Complexity
- `fork`: O(size of page tables) for `dup_mmap` (copy page table hierarchy) — pages themselves shared (COW) — so O(PTEs) not O(pages); in practice fast (µs–tens of µs).
- COW fault: O(1) per faulted page (allocate + copy one page).
- `exec`: O(binary size) page mapping (lazy) + O(segments) setup; actual page reads fault in lazily.
- `exit`: O(resources being released).
- CFS enqueue/dequeue: O(log n) rbtree; pick_next: O(log n) or O(1) cached leftmost.
- Context switch: O(1) register save/restore + `switch_mm` (TLB flush on mm change — optimized with ASIDs/PCID).

## 11. Advantages
- **fork COW**: nearly-free process creation; `fork`+`exec` shell pattern is cheap.
- **task_struct**: unified descriptor for processes *and* threads; all kernel paths touch one struct.
- **CFS**: fair, no starvation, O(log n), tunable (`nice`, weights, cgroups share CPU via weights).
- **Zombie model**: reliable resource cleanup + parent visibility of exit status.
- **sched_class**: pluggable policies (deadline/RT/CFS/idle) — real-time and fair coexist.

## 12. Disadvantages
- **fork's COW** can still page-fault heavily for a process that writes a lot before exec (rare).
- **task_struct** is large (~a few KB + kernel stack); thousands of threads consume memory.
- **Zombies** accumulate if parents don't `wait` (leak until parent exit/reparent to init).
- **CFS** isn't ideal for all workloads (e.g., RT needs the RT class; NUMA needs balancing) — hence multiple classes.
- **fork in multi-threaded processes** is problematic (child only has the calling thread; locks can be held) → `posix_spawn`/`vfork`/exec tricks needed.

## 13. Interview Questions
1. **Q: What is a `task_struct`?** A: Linux's process descriptor — everything about a process (pid, state, mm, files, fs, signal, cred, sched_entity); threads are tasks too (sharing mm/files/signal).
2. **Q: What happens in `fork`?** A: `copy_process` duplicates the task_struct and copies subsystems per `CLONE_*`; the address space is **copy-on-write** (PTEs shared read-only until written); child returns 0, parent returns the child's pid.
3. **Q: What is copy-on-write fork?** A: The child's page tables reference the parent's pages as read-only; the first write by either faults and duplicates just that page — `fork`+`exec` avoids copying at all.
4. **Q: fork vs vfork vs posix_spawn?** A: `fork` = full COW copy; `vfork` = shares mm entirely (child must exec without writing) — fast but dangerous; `posix_spawn` = library-level efficient spawn (fork+exec with child optimizations), safer in multithreaded programs.
5. **Q: Threads vs processes in Linux?** A: Both are `task_struct`s; threads are created with `CLONE_VM|CLONE_FILES|CLONE_SIGHAND|CLONE_THREAD` (share mm/files/signal); processes with plain `fork`. `getpid` = tgid; `gettid` = pid.
6. **Q: What is a zombie and when do they appear?** A: A task in `EXIT_ZOMBIE` after `do_exit` — resources freed but the task_struct kept so the parent can read the exit status via `wait`; reaped by `release_task`. Unreaped zombies accumulate if parents never `wait`.
7. **Q: What is an orphan?** A: A process whose parent died — reparented to PID 1 (init) or a subreaper, which reaps it (prevents permanent orphans).
8. **Q: What happens in `exec`?** A: `do_execve` → loads the ELF: `flush_old_exec` (new mm), maps PT_LOAD segments, sets up stack/argv/envp, jumps to the loader/entry — replaces the process image without creating a new task.
9. **Q: How does CFS work?** A: Run queue = red-black tree keyed by `vruntime`; `vruntime` grows by run time scaled by weight; always run the leftmost (least-served) task → fair share, O(log n).
10. **Q: What is `nice` and how does it affect CFS?** A: Nice (priority −20..19) sets the task weight: lower nice → higher weight → vruntime grows slower → more CPU share. It's a *relative* share adjustment, not a fixed quantum.
11. **Q: What is the difference between TASK_INTERRUPTIBLE and TASK_UNINTERRUPTIBLE?** A: Both sleep; INTERRUPTIBLE wakes on signals (can be interrupted by a signal); UNINTERRUPTIBLE doesn't (e.g., waiting on I/O in old kernels) — the source of "uninterruptible sleep" (D state) tasks.
12. **Q: What does `wait` do and why is it required?** A: `wait4`/`waitpid` blocks (or polls) until a child exits, collects the exit status, and triggers `release_task` — required for the child to be reaped (not stay a zombie) and for the parent to know the result.

## 14. Follow-Up Questions
1. **Q: What are sched classes?** A: SCHED_DEADLINE > SCHED_FIFO/RR (RT) > SCHED_NORMAL (CFS) > SCHED_IDLE — priority tiers; a task's `sched_class` determines which run queue it uses; the scheduler picks the highest-priority non-empty class.
2. **Q: What is the difference between `execve` and `posix_spawn`?** A: `execve` is the raw syscall; `posix_spawn` is a library function combining fork+exec efficiently (or optimized paths) — used by Go, glibc `system`, etc.
3. **Q: What is `CLONE_NEWNS` etc.?** A: Namespace clone flags — create isolated views (mount, pid, net, uts, ipc, user, cgroup) → the basis of containers.
4. **Q: What happens to fd tables on fork?** A: `CLONE_FILES` unset → copied fd table (both point at the same `struct file`s, with refcounts); set → shared (threads see the same fds; `dup` shares the underlying open file).

## 15. Coding Example
```c
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>

int main(void) {
    pid_t pid = fork();              // create a child (COW)
    if (pid == 0) {
        // child — exec replaces this image
        char *args[] = {"/bin/echo", "hello from child", NULL};
        execve(args[0], args, NULL); // if exec fails:
        perror("execve");
        _exit(1);
    } else if (pid > 0) {
        int status;
        waitpid(pid, &status, 0);    // reap the child (no zombie)
        if (WIFEXITED(status))
            printf("parent: child exited with %d\n", WEXITSTATUS(status));
    }
    return 0;
}
```
Run: child prints "hello from child"; parent prints the exit status 0. Try removing `waitpid` and adding a sleep to observe the zombie (`ps` shows `Z`).

## 16. Industry Usage
- **Kernel**: `kernel/fork.c`, `fs/exec.c`, `kernel/exit.c`, `kernel/sched/fair.c`, `kernel/sched/core.c`, `include/linux/sched.h`.
- **Runtimes**: glibc `fork`/`posix_spawn`; Go runtime (clone-based), Java/JVM (NPTL threads), systemd (`Type=forking`, `KillMode`).
- **Schedulers**: CFS (Linux default since 2.6.23); EEVDF (6.6) refinement; RT/deadline for audio/real-time.
- **Containers**: runc/containerd use clone namespaces; cgroups shape CPU shares.
- **Ops**: `ps`, `top`, `htop`, `strace -f`, `perf sched`, `taskset`, `chrt`, `nice`.

## 17. References
- Love, *Linux Kernel Development*, Ch. 3 (task_struct, fork, exec, exit) and Ch. 4 (process scheduling).
- Silberschatz, *Operating System Concepts*, Ch. 3 (processes) + Linux chapter.
- Tanenbaum, *Modern Operating Systems*, Ch. 2 (processes and threads).
- Kernel docs: `Documentation/scheduler/sched-design-CFS.rst`.
- `man 2 fork`, `man 2 execve`, `man 2 wait`, `man 2 clone`, `man 1 nice`, `man 1 taskset`.

## 18. Cheat Sheet
- task_struct = process descriptor; threads = tasks with shared mm/files/signal.
- fork = COW copy (share pages, fault-copy on write); child returns 0.
- exec = replace image (new mm, ELF segments, entry).
- exit → zombie → wait reaps → release_task.
- Orphans → reparented to init/subreaper.
- clone flags: CLONE_VM (share mm), CLONE_FILES, CLONE_SIGHAND, CLONE_THREAD.
- CFS: rbtree by vruntime; leftmost runs; nice → weight.
- sched_class: deadline > RT > CFS > idle.
- vfork shares mm (exec-only child); posix_spawn = safe fork+exec.

## 19. Quiz
1. fork copies the address space? a) eagerly b) COW c) never d) swap → **b**
2. Threads share which? a) mm b) PID namespace c) stack d) task_struct → **a** (and files/signal)
3. A zombie is? a) running b) exited, unreaped c) stopped d) orphan → **b**
4. exec creates a new process? a) yes b) no, new image c) thread d) vfork → **b**
5. CFS schedules by? a) priority queue b) vruntime rbtree c) FIFO d) random → **b**
6. `CLONE_VM` makes? a) process b) thread c) zombie d) exec → **b**

## 20. Flashcards
- **Q: task_struct?** → **A:** Process descriptor (pid, mm, files, sched, signal).
- **Q: COW fork?** → **A:** Share pages read-only; duplicate on first write.
- **Q: exec?** → **A:** Replace image in place; new mm + entry.
- **Q: Zombie vs orphan?** → **A:** Exited-unreaped vs parent died (→ init).
- **Q: CFS core?** → **A:** rbtree by vruntime; leftmost = next.
- **Q: Threads in Linux?** → **A:** clone with CLONE_VM/CLONE_FILES/CLONE_THREAD.

## 21. Revision
Linux processes are `task_struct`s; creation is `fork`/`clone` with copy-on-write (pages shared until written — that's why `fork`+`exec` is cheap), threads are tasks created with `CLONE_VM|CLONE_FILES|CLONE_SIGHAND|CLONE_THREAD`, `exec` replaces the image in place, and `exit` produces a zombie reaped by `wait`. The CFS scheduler runs the rbtree-leftmost (smallest vruntime) task for fair CPU share, with `nice`/weights shaping proportions and sched classes (deadline/RT/CFS/idle) layering priorities. This is the concrete realization of Parts 02–03: process states, creation, scheduling, and cleanup — the foundation the next sections' address space and syscall machinery live in.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a task_struct?" | 13 Q1 / 2 How |
| "What happens in fork?" | 13 Q2 / 8 Example |
| "What is COW fork?" | 13 Q3 / 2 How |
| "fork vs vfork vs posix_spawn?" | 13 Q4 / 4 Why not |
| "Threads vs processes?" | 13 Q5 / 8 Example |
| "What is a zombie?" | 13 Q6 / 8 Example |
| "How does CFS work?" | 13 Q9 / 7 Formal |
| "What does wait do?" | 13 Q12 / 2 How |
