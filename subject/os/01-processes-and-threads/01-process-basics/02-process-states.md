# Process States

## 5-State Model

```
         ┌──────────┐
         │   NEW    │  process created (PCB allocated)
         └────┬─────┘
              │ admit
              ▼
      ┌───────────────┐
      │    READY      │ ◄─────────────┐
      │ (in ready Q)  │               │
      └───────┬───────┘               │
              │ scheduler dispatch    │
              ▼                       │
      ┌───────────────┐   I/O/event   │
      │   RUNNING     │───────────────┤
      │ (on CPU)      │               │
      └───────┬───────┘               │
              │ I/O or event wait     │
              ▼                       │
      ┌───────────────┐              │
      │   WAITING     │───────────────┘
      │ (blocked)     │  I/O complete
      └───────────────┘
              │ exit
              ▼
      ┌───────────────┐
      │  TERMINATED   │  PCB eventually deallocated
      └───────────────┘
```

| State | Description |
|-------|-------------|
| **New** | Process being created; OS allocates PID, PCB, initial resources |
| **Ready** | In main memory, waiting for CPU (placed in **ready queue**) |
| **Running** | CPU actively executing instructions |
| **Waiting/Blocked** | Waiting for I/O or event (disk read, keyboard input, signal) |
| **Terminated** | Finished execution; PCB retained briefly for status collection |

## State Transitions (Key Pairs)
- **Ready → Running**: Scheduler dispatches the process
- **Running → Ready**: Timer interrupt (quantum expired), higher-priority process preempts
- **Running → Waiting**: Process issues I/O request or `wait()` system call
- **Waiting → Ready**: I/O completion, event occurs
- **Running → Terminated**: Process exits (`exit()`, or killed)

## Suspended States (Swapped)
When memory is full, OS moves processes to **swap space** (disk):

| State | Meaning |
|-------|---------|
| **Ready-Suspend** | Process ready to run but swapped out; must be swapped in first |
| **Blocked-Suspend** | Process waiting for I/O AND swapped out |

- **Swapping** ⟶ process moves between memory and disk
- OS swaps out a blocked process (not making progress anyway) to free memory
- If I/O completes for a swapped-out process, it moves to **ready-suspend** (still on disk)

## Zombie vs Orphan Processes

| | Zombie | Orphan |
|---|--------|--------|
| **Def** | Child terminated but **parent hasn't called `wait()`** | **Parent terminated** before child |
| **PCB?** | PCB retained (no memory, just status info) | Becomes child of `init` (PID 1) |
| **Problem** | Accumulates wasted PIDs (zombie flood) | None — `init` reaps it |
| **Fix** | Parent calls `wait()` / `waitpid()`; or kill parent | OS automatically handles |

```c
// Zombie creation
pid_t pid = fork();
if (pid == 0) exit(0);    // child exits
else sleep(60);            // parent doesn't wait — child is zombie
```

- **`wait()`**: Parent blocks until child terminates, collects exit status
- **`waitpid()`**: More control (specific PID, options like `WNOHANG`)
