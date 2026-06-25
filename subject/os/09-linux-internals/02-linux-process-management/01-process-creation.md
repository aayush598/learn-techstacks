# Process Creation in Linux

## fork()
- Creates child as **copy of parent** (PCB, file descriptors, memory)
- Returns: **PID of child** to parent, **0** to child, **-1** on error
- After `fork()`, both processes execute next instruction
- **Copy-on-Write (COW)**: pages not copied immediately
  - Both share same physical pages until one writes
  - On write, kernel copies page → each has own copy
  - Saves memory, avoids copy overhead when exec follows

## exec()
- Replaces process image: loads new program, resets address space
- `execl`, `execv`, `execle`, `execve`, `execlp`, `execvp`
- `execve()`: actual syscall; others are libc wrappers
- PID remains same after exec
- If exec fails (e.g., file not found), original process continues

## wait() / waitpid()
- Parent blocks until child terminates
- `waitpid(pid, &status, options)`: wait for specific child
- `WNOHANG`: return immediately if no child has exited
- Status macros: `WIFEXITED`, `WEXITSTATUS`, `WIFSIGNALED`, `WTERMSIG`

## Zombie vs Orphan
| State | Cause | Reaping |
|-------|-------|---------|
| **Zombie** | Child terminated, parent hasn't called `wait()` | Parent calls `wait()` → PCB freed |
| **Orphan** | Parent dies before child | **init** (PID 1) adopts and calls `wait()` |

## Process States
- **TASK_RUNNING**: running or runnable
- **TASK_INTERRUPTIBLE**: waiting (can be woken by signal)
- **TASK_UNINTERRUPTIBLE**: waiting (cannot be woken by signal, e.g., disk I/O)
- **TASK_STOPPED**: stopped (SIGSTOP/SIGTSTP)
- **TASK_ZOMBIE**: terminated, waiting for parent to reap

## Process Hierarchy
- **init** (PID 1): ancestor of all processes (systemd on modern systems)
- `pstree` shows process tree
- Every process has parent (except init and kernel threads)
