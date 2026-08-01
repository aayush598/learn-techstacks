# Fork and Exec in Depth

> **TL;DR**: Every process on Linux is created by `fork`/`clone` (copy the current task, copy-on-write) and optionally transformed by `exec` (replace the image) — the fork/exec pattern gives Unix its cheap, uniform process creation with the full isolation of a fresh address space.

## 1. Why Does This Exist?
The Unix designers needed a simple, uniform way to create processes. `fork` exists because it's the *cheapest primitive that reuses the current process's state*: the child starts as a byte-for-byte copy of the parent (inheriting files, environment, signals), so no complex "constructor arguments" are needed. `exec` exists because a copy alone is useless — you usually want a *different* program, so `exec` replaces the copied image with a new one. This two-step (copy-then-replace) design means: creation is trivial (no per-program creation logic), and the OS doesn't need to know anything about the program being run. Every process in Unix/Linux — shell commands, systemd services, containers — is created this way.

## 2. How Does It Work?
- **`fork()`**: clones the calling task. Returns: `0` in the child, the child's PID in the parent, `-1` on failure. Memory is **copy-on-write** (pages shared read-only; first write duplicates). The child inherits open fds, environment, signal handlers (dispositions, but pending signals are cleared), and more.
- **`execve(path, argv, envp)`**: replaces the current process's image with `path`'s. On success it *never returns*; on failure returns `-1`. The address space is rebuilt (text/data mapped from the new file), PID is kept, most attributes (open fds except those with `O_CLOEXEC`) are preserved.
- **`clone(flags, stack, ...)`**: the generalized primitive; flags decide sharing (`CLONE_VM`, `CLONE_FILES`, `CLONE_SIGHAND`, `CLONE_FS`, `CLONE_THREAD`...). `fork` = `clone(SIGCHLD)`; `pthread_create` = `clone(CLONE_VM|CLONE_FS|CLONE_FILES|CLONE_SIGHAND|CLONE_THREAD|...)`.
- **`vfork`**: child shares everything until `exec` (optimized, dangerous if it touches memory before exec).

## 3. When Is It Used?
- **Every shell command**: bash → `fork` + `exec`.
- **`system()`, `popen()`** in C; **`subprocess`** in Python; **`ProcessBuilder`** in Java.
- **Servers**: Apache prefork (fork per connection), Postgres (fork per connection), gunicorn (fork workers).
- **Daemonization**: a process forks, parent exits, child `setsid` and `exec`s.
- **Containers**: runc uses `clone` with namespace flags (`CLONE_NEWPID`, `CLONE_NEWNET`, ...) then `exec`s the container init.
- **Isolation**: browsers and sandboxes fork+exec with tightened permissions.

## 4. Why Wasn't Another Approach Chosen?
- **`spawn` with full arguments (Windows-style `CreateProcess`)**: rejects the "copy state" approach — it's a big API and requires encoding everything at creation. Unix's fork is simpler but has problems (in multi-threaded apps, fork copies one thread — risky). `posix_spawn()` provides a Windows-like wrapper over fork+exec when fork is undesirable.
- **Exec without fork (just load a new program into an existing process)**: that's exactly `exec` — but you'd lose the parent, so you can't have shells or process trees. Fork is needed to keep the parent alive.
- **Creating processes directly from files (no copy step)**: loses inherited environment/files/signals — fork's inheritance is what makes process setup trivial.
- **Hardware/VM-based process creation**: way too heavy; kernel bookkeeping + COW is the sweet spot.
The fork+exec design won on simplicity and uniformity; its thread-safety flaws are patched by `posix_spawn` and careful use.

## 5. Intuition
Fork is like **photocopying a document**: you get an exact copy (the child), then you edit the copy (exec) to become something else. Exec is like **erasing a whiteboard and drawing a new picture** on it: same board (process), brand-new content (program). The copy-first design means you never have to describe the child from scratch — it inherits everything, and you only change what you need.

## 6. Real-World Analogy
A **restaurant opening a new location**: `fork` = the owner makes a complete duplicate of the current restaurant (same menu, recipes, staff knowledge, suppliers). Then `exec` = they remodel the duplicate into a *different* restaurant — same building license (PID), new brand. If they don't remodel (no exec), they just have two identical restaurants. Copying is cheap because of COW: pages of the menu are *shared* until someone edits them.

## 7. Formal Definition
**`fork()`**: a system call that creates a new process (child) that is an almost exact copy of the calling process (parent); it returns `0` to the child, the child's PID to the parent, and `-1` on error, using copy-on-write so page frames are shared until written. **`exec()`** (family: `execve`, `execvp`, ...): a system call that replaces the calling process's memory image with a specified program; on success control transfers to the new program's entry and the call never returns. **`clone()`**: the Linux primitive generalizing creation via flags controlling shared resources.

## 8. Example
```c
pid_t pid = fork();
if (pid == 0) {                    /* child path */
    execlp("ls", "ls", "-l", NULL); /* replace image with ls */
    _exit(127);                     /* exec failed */
} else if (pid > 0) {              /* parent path */
    waitpid(pid, &status, 0);
    printf("ls finished\n");
} else {
    perror("fork");                 /* pid == -1 */
}
```
Behavior:
- Parent prints "ls finished" after the child's `ls -l` output.
- If `exec` fails (e.g., missing binary), the child prints an error and exits with 127.
- The parent never "runs" the child's code; the child never runs the parent's post-fork code. The magic is the **two return values** — one code, two paths.

## 9. Internal Working
1. `fork` → `sys_fork` → `_do_fork` → `copy_process`:
   - `dup_task_struct`: new `task_struct` + kernel stack (slab).
   - `copy_mm`: shares parent's `mm_struct` page tables read-only (COW) — sets PTE RO + marks pages; first write → page fault → copy.
   - `copy_files`, `copy_fs`, `copy_sighand`, `copy_creds`: increments reference counts or clones (per `CLONE_*` flags).
   - `alloc_pid` → new PID; `copy_thread` copies `pt_regs` so the child returns `0`.
   - `wake_up_new_task`: child enqueued; `SIGCHLD` not sent (parent already has the PID).
2. `execve` → `do_execve` → `exec_binprm`:
   - Read ELF header; `flush_old_exec` tears down old `mm`/files-with-CLOEXEC.
   - `do_mmap` maps the new text/data; loads interpreter (dynamic linker) if needed.
   - `start_thread`: sets new PC (entry point), clears most registers; returns `0` to userspace → the new image begins.
3. COW mechanics: both parent and child share frames mapped RO; either process writing triggers `handle_mm_fault` → `wp_page_copy` duplicates the frame and updates that process's PTE.

## 10. Time Complexity
- `fork`: O(1) amortized for task_struct (slab) + O(page-table setup) — COW keeps the heavy copy off the fast path.
- `exec`: O(binary size) + O(library loads + relocations) — I/O bound.
- `clone` thread: O(1) + O(new stack).
- Practical: fork+exec of `/bin/true` ≈ 100-500µs; pthread_create ≈ 5-20µs (order-of-magnitude difference).
- COW fault cost: O(1) per first-written page (a page copy + TLB update).

## 11. Advantages
- **Simple, uniform creation** — no constructor API; state inherited for free.
- **Cheap due to COW** — fork doesn't copy memory.
- **Isolation preserved** — the child is a full process with its own address space.
- **Flexible** — `clone` flags tune sharing (threads vs processes) with one primitive.
- **Composable** — fork+exec powers shells, daemons, containers, sandboxes.

## 12. Disadvantages
- **fork in multi-threaded apps is dangerous**: only the calling thread survives; locks held by other threads are stuck in the child → deadlock. Fixes: `posix_spawn`, `pthread_atfork`, fork-before-threads.
- **Overhead vs threads**: fork still copies page tables and bookkeeping; thread creation is cheaper.
- **vfork semantics are subtle** (child must not touch memory before exec) — a classic bug source.
- **COW has memory overhead**: shared read-only pages may pin frames; pathological write-heavy forks still copy.
- **`exec` failure handling** is easy to get wrong (forgetting `_exit` after failed exec → double-run).

## 13. Interview Questions
1. **Q: What does `fork()` return?** A: `0` in the child; the child's PID in the parent; `-1` on failure. One call, two returns — the copy makes both execution paths live.
2. **Q: What is copy-on-write and why is fork so fast?** A: Fork shares the parent's pages read-only; the first write by either process faults and duplicates only that page. So fork copies bookkeeping, not memory — O(page tables), not O(memory).
3. **Q (TRICKY): Does the child of fork inherit the parent's pending signals?** A: No — pending signals are cleared in the child; signal *dispositions* (handlers) are inherited. Async-safe operations are the only safe ones between fork and exec in a multithreaded program.
4. **Q: What is the difference between `fork`, `vfork`, and `clone`?** A: fork copies with COW; vfork shares everything until exec (faster, riskier); clone is the generalized primitive with `CLONE_*` flags — pthreads uses clone with CLONE_VM etc.
5. **Q: What happens on a successful `exec`?** A: The current image is replaced; on success exec never returns. Failure returns -1. PID and most attributes (fds without O_CLOEXEC, umask, cwd, signals) survive exec.
6. **Q (SCENARIO): You `fork` and forget to `_exit` after a failed `exec` in the child. What happens?** A: The child continues running the parent's code — double execution (classic fork bomb / duplicate logic bug). Always `_exit()` right after failed exec.
7. **Q: What does `O_CLOEXEC` do?** A: Marks an fd to be automatically closed on exec — preventing accidental fd leaks into exec'd programs (a security and correctness primitive).
8. **Q: What's wrong with `fork` in a multi-threaded process?** A: Only the calling thread is duplicated. Locks (mutexes) held by vanished threads remain locked in the child → deadlock. `pthread_atfork` or `posix_spawn` fixes it.
9. **Q: How does a shell run a command?** A: `fork` a child, child `exec`s the command, parent `waitpid`s. Builtins (cd, export) don't fork — they run in the shell itself.
10. **Q: What are the `clone` flags that make a thread?** A: `CLONE_VM` (share mm), `CLONE_FILES` (share fds), `CLONE_FS` (share cwd/umask), `CLONE_SIGHAND` + `CLONE_THREAD` (share signal handlers & thread group), plus `CLONE_SETTLS`, `CLONE_PARENT_SETTID`.
11. **Q (PRODUCTION): How does a container runtime create a container?** A: runc `clone`s with namespace flags (`CLONE_NEWPID`, `CLONE_NEWNS`, `CLONE_NEWNET`, `CLONE_NEWIPC`, `CLONE_NEWUTS`, `CLONE_NEWUSER`), sets up cgroups, then `exec`s the container's init — the container is just a specially-created process.
12. **Q: What is `posix_spawn`?** A: A library wrapper that does fork+exec in a safe way (Windows-style spawn), avoiding the multi-threaded-fork pitfalls; used by glibc for `system` where appropriate.
13. **Q: What is `pthread_atfork`?** A: Registers prepare/parent/child handlers run before/after fork to re-acquire/release locks, keeping the child consistent in multi-threaded apps.
14. **Q: What is the return-value contract for fork in terms of PID?** A: Parent gets the child's PID (to `wait` on it); child gets 0 (to know it's the child); the kernel guarantees the child's PID != 0. Negative = error (`EAGAIN` limit, `ENOMEM`).
15. **Q (TRICKY): If fork is COW, why is fork+exec sometimes still slow?** A: exec must load and map a new image (page table rebuild, libs, relocations) and the COW fault machinery may still fire during startup writes; also `fork` duplicates page tables and fd tables. posix_spawn/vfork skip most of that.
16. **Q: What is the relationship between fork and copy_process in the kernel?** A: `fork` → `sys_fork` → `kernel_clone` → `copy_process`, which does the deep copy (task_struct, mm, files, creds) then `wake_up_new_task`. The kernel has ONE creation path; fork/clone/vfork are thin wrappers.

## 14. Follow-Up Questions
1. **Q: What is `RLIMIT_NPROC` and how does it interact with fork?** A: A per-user cap on process/thread count; exceeding it makes fork return EAGAIN. It's the standard fork-bomb defense alongside cgroup `pids.max`.
2. **Q: What does `SIGCHLD` have to do with fork?** A: When a child exits or stops, the kernel sends SIGCHLD to the parent; with `SA_NOCLDWAIT` or handlers, parents can auto-reap or ignore.
3. **Q: What is `kernel.pid_max` and PID wraparound?** A: Max PID value (default 32768→4M); Linux allocates increasing PIDs then wraps, avoiding reuse while a PID is live.
4. **Q: Why do you `setvbuf`/`fflush` before fork in C?** A: stdio buffers in the parent are copied to the child; without flushing, both might write the same buffered output — duplicated output or lost data. This is the classic "fork + printf" interview gotcha.
5. **Q: What happens if exec loads a script (shebang)?** A: The kernel reads `#!interpreter args` and execs the interpreter with the script as its argument (e.g., `#!/bin/bash`).

## 15. Coding Example
```c
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    printf("before fork: pid=%d\n", getpid());
    pid_t pid = fork();

    if (pid == 0) {
        /* child: exec a new program */
        execl("/bin/echo", "echo", "child here, about to become /bin/echo", NULL);
        perror("exec");              /* only on failure */
        _exit(127);
    } else if (pid > 0) {
        int status;
        waitpid(pid, &status, 0);
        printf("parent (%d): child %d exited, status=%d\n",
               getpid(), pid, WEXITSTATUS(status));
    } else {
        perror("fork");
    }
    return 0;
}
```
```bash
# fork + exec in bash
( exec /bin/echo hello )           # subshell = fork; exec replaces it
# measure fork+exec cost
time for i in $(seq 1000); do /bin/true; done
# see PID churn / PPID relationships
bash -c 'echo "sh pid=$$"; sleep 5' &
ps -o pid,ppid,comm,args -p $! --ppid $$
```

## 16. Industry Usage
- **Linux**: `kernel/fork.c` (kernel_clone), `fs/exec.c` (do_execveat_common), `include/uapi/linux/sched.h` (clone flags). Every container (runc/crun), every server pre-forking, every shell uses it.
- **Windows**: `CreateProcess` (no fork) — the contrast question ("why doesn't Windows use fork?") is common; Windows copies via process creation with arguments.
- **Production**: Apache prefork & gunicorn (fork), Postgres (fork per backend), Go's `os/exec` (fork+exec), Python `multiprocessing` (fork by default on Linux), systemd units (exec).
- **Container security**: `CLONE_NEWUSER` unprivileged user namespaces are the basis of rootless containers and unprivileged sandboxing (Firecracker, gVisor).
- **Interview angle**: fork return values, COW, vfork/clone, posix_spawn, and the multithreaded-fork trap are the highest-frequency C/systems questions.

## 17. References
- Silberschatz, *OS Concepts*, Ch. 3.3 (Process Creation/Termination).
- Tanenbaum, *Modern OS*, Ch. 2.1.4 (Process creation in Unix).
- Linux man: `fork(2)`, `execve(2)`, `clone(2)`, `vfork(2)`, `posix_spawn(3)`, `pthread_atfork(3)`.
- Linux source: `kernel/fork.c`, `fs/exec.c`, `include/linux/sched.h`.
- Love, *Linux Kernel Development*, Ch. 3 (Process Management).
- Kerrisk, *The Linux Programming Interface* (Process creation).

## 18. Cheat Sheet
- fork returns 0 (child), child PID (parent), -1 (error).
- COW: fork shares pages RO; first write copies.
- exec never returns on success; replaces the image; keeps PID + fds (unless O_CLOEXEC).
- clone flags: CLONE_VM/FILES/SIGHAND/THREAD/NS* → threads/containers.
- vfork: share-till-exec, fast but fragile.
- Always `_exit()` after failed exec in the child.
- Multithreaded fork copies one thread; use posix_spawn/pthread_atfork.
- flush stdio before fork (buffer duplication).
- O_CLOEXEC prevents fd leaks into exec'd programs.
- fork+exec ≈ 100-500µs; pthread_create ≈ 5-20µs.

## 19. Quiz
1. In the child after fork, `fork()` returned: a) child PID b) 0 c) -1 d) parent PID → **b**
2. COW means fork copies: a) all memory b) only bookkeeping/page tables c) disk d) registers only → **b**
3. On successful exec: a) returns 0 b) never returns c) returns -1 d) forks → **b**
4. A thread created by pthreads uses clone flag: a) CLONE_VM b) CLONE_FORK c) CLONE_EXEC d) none → **a**
5. Which is NOT inherited by the child on fork? a) open fds b) pending signals c) env d) file offsets → **b**
6. Forking in a multithreaded process: a) copies all threads b) copies one thread c) deadlocks always d) crashes → **b**
7. `posix_spawn` is preferred because it: a) is faster than fork b) avoids multithreaded-fork traps c) uses exec only d) needs no libc → **b**
8. `O_CLOEXEC` closes an fd on: a) fork b) exec c) exit d) signal → **b**
9. runc creates containers via: a) exec only b) clone with NS flags + exec c) CreateProcess d) mmap → **b**
10. Forgetting `_exit` after failed exec causes: a) segfault b) double execution c) zombie d) no effect → **b**

## 20. Flashcards
- **Q: fork() return values?** → **A:** 0 child, child PID parent, -1 error.
- **Q: Why is fork fast?** → **A:** Copy-on-write — pages shared, copied on write.
- **Q: exec on success?** → **A:** Never returns; image replaced.
- **Q: Thread creation primitive?** → **A:** clone(CLONE_VM | CLONE_FILES | ...).
- **Q: Multithreaded fork danger?** → **A:** Copies one thread; stuck locks → deadlock.
- **Q: Fix for that?** → **A:** posix_spawn or pthread_atfork.
- **Q: O_CLOEXEC?** → **A:** Auto-close fd on exec.
- **Q: vfork?** → **A:** Share until exec; fast but dangerous.
- **Q: stdio before fork?** → **A:** Flush — buffers are duplicated.
- **Q: container creation?** → **A:** clone with CLONE_NEW* + exec.

## 21. Revision
Every process is born via fork/clone (copy-on-write copy) and reshaped via exec (image replace, never returns on success). fork returns 0 to child, PID to parent, -1 on error. clone flags (CLONE_VM, CLONE_NS*) make threads and containers. Traps: multithreaded fork copies one thread (deadlock risk → posix_spawn/pthread_atfork), unflushed stdio duplicates output, and missing `_exit` after failed exec double-runs code. O_CLOEXEC prevents fd leaks. fork+exec costs ~100-500µs; threads ~10µs.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What does fork return?" | 13 Q1 / 8 Example |
| "What is copy-on-write?" | 13 Q2 / 9 Internal Working |
| "fork vs vfork vs clone?" | 13 Q4 / 7 Formal Definition |
| "What happens on exec?" | 13 Q5 / 2 How It Works |
| "fork in multithreaded app?" | 13 Q8 / 14 Follow-Up |
| "How does a shell run a command?" | 13 Q9 / 16 Industry Usage |
| "How are containers created?" | 13 Q11 / 16 Industry Usage |
| "What is posix_spawn / pthread_atfork?" | 13 Q12-13 / 12 Disadvantages |
| "O_CLOEXEC purpose?" | 13 Q7 / 9 Internal Working |
| "Why is fork+exec slow sometimes?" | 13 Q15 / 10 Time Complexity |
