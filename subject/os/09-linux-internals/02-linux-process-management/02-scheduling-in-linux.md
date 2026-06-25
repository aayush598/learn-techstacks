# Linux Scheduling (CFS)

## CFS (Completely Fair Scheduler)
- Introduced in **Linux 2.6.23** (replaced O(1) scheduler)
- Goal: give each process a **fair share** of CPU
- Uses **red-black tree** to track runnable processes
- Scheduling complexity: **O(log N)** (tree insertion/lookup)
- **Virtual runtime (vruntime)**: actual runtime weighted by priority

## Virtual Runtime
- `vruntime` = actual runtime × (NICE_LOAD / weight)
- Higher priority (lower nice) → smaller weight divisor → slower vruntime growth
- CFS always picks process with **smallest vruntime** (leftmost in RB-tree)
- When process runs, vruntime increases; when blocked, vruntime stays

## Nice Values
| Nice | Priority Level |
|------|---------------|
| **-20** | Highest priority |
| **0** | Default |
| **+19** | Lowest priority |
- `nice()` and `setpriority()` syscalls
- Lower nice = more CPU time vs other processes (not absolute)

## Scheduling Classes
| Class | Policy | Description |
|-------|--------|-------------|
| **SCHED_NORMAL** | CFS | Standard time-sharing |
| **SCHED_FIFO** | RT | First-in-first-out (preempted by higher RT) |
| **SCHED_RR** | RT | Round-robin within same priority |
| **SCHED_BATCH** | CFS | Batch (wakeup penalty, fewer preemptions) |
| **SCHED_IDLE** | CFS | Only runs when CPU is idle |
| **SCHED_DEADLINE** | EDF | Earliest deadline first (real-time) |
- RT policies: priority 1 (low) to 99 (high)

## CFS Parameters
- `sched_latency`: target latency (default 20ms)
- `sched_min_granularity`: minimum preemption granularity (default 4ms)
- `sched_wakeup_granularity`: wakeup preemption threshold
- `/proc/sys/kernel/sched_*` for tuning
