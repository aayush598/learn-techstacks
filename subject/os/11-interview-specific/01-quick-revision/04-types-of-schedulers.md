# Types of Schedulers

## Comparison Table

| Property | Long-Term (Job Scheduler) | Short-Term (CPU Scheduler) | Medium-Term (Swapper) |
|----------|--------------------------|---------------------------|----------------------|
| **Also called** | Admission Scheduler | CPU Scheduler | Swapper |
| **Frequency** | Low (seconds/minutes) | Very high (ms) | Medium |
| **Function** | Selects processes from disk → memory (ready queue) | Selects ready process → CPU | Moves processes memory ↔ disk |
| **Controls** | Degree of multiprogramming | CPU utilization + response time | Degree of multiprogramming |
| **Duration** | Long-lived decisions | Milliseconds | Milliseconds to seconds |
| **Invoked when** | Process created / enters system | Every clock interrupt / I/O / syscall | Memory pressure |

## Long-Term Scheduler (Job Scheduler)
- **Controls admission:** which processes enter the ready queue
- **Decides multiprogramming degree** (how many processes in memory)
- **Balances I/O-bound vs CPU-bound processes**
  - Too many CPU-bound → poor response time for interactive
  - Too many I/O-bound → poor CPU utilization
- Rare in modern OS (time-sharing systems admit all; batch systems still use it)

## Short-Term Scheduler (CPU Scheduler)
- **Selects next process** from ready queue to run on CPU
- Invoked frequently: every **timer interrupt** (~1–10ms), I/O wait, syscall, yield
- **Must be fast** — overhead of scheduling decision matters (1% of CPU time rule)
- Implements scheduling algorithm: FCFS, SJF, RR, Priority, MLFQ

## Medium-Term Scheduler (Swapper)
- **Swaps out** processes from memory to disk (suspend)
- **Swaps in** suspended processes back to memory
- Triggered by **memory pressure** (high demand, low free pages)
- Reduces degree of multiprogramming to free memory
- Used by **virtual memory systems** (paging/segmentation)

## Process State Transitions
```
New → [Long-term] → Ready → [Short-term] → Running → [Medium-term] → Suspended Ready
                       ↑                                ↓
                      [Preempt]                   Suspended Blocked
```

## Modern OS (Linux)
- **No explicit long-term scheduler** — processes admitted on exec()
- **CFS (Completely Fair Scheduler)** is the short-term scheduler
- **kswapd** + **OOM killer** serve medium-term roles (swap + process killing)
- **cgroup limits** implicitly control multiprogramming

## Interview Tips
- *"Short-term scheduler picks which process gets the CPU RIGHT NOW — must be fast (< 1ms)"*
- *"Long-term scheduler controls how many processes are in memory (batch systems)"*
- *"Medium-term scheduler handles swapping — modern systems use demand paging instead"*
