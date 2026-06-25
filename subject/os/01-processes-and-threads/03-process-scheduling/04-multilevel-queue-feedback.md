# Multilevel Queue & Feedback Scheduling

## Multilevel Queue

- Ready queue **partitioned into separate queues** (each with its own scheduling algorithm)
- Processes permanently assigned to a queue based on **type** (foreground/background, system/interactive/batch)
- **Fixed priority**: Process stays in same queue forever

### Example
```
High priority  ┌──────────────────────┐
               │ Queue 1 (Foreground) │  Round Robin (q = 8)
               │   Interactive apps   │
               └──────────┬───────────┘
                          │ Must empty Q1
Low priority   ┌──────────┴───────────┐
               │ Queue 2 (Background) │  FCFS
               │   Batch jobs         │
               └──────────────────────┘
```

### Scheduling between queues
- **Strict priority**: Run all Q1 tasks first; only if Q1 empty → Q2 (starvation risk!)
- **Time slice**: 80% CPU to Q1, 20% to Q2 (fair share)

## Multilevel Feedback Queue (MLFQ)

- Process can **move between queues** based on behavior
- **Goal**: Optimize response for interactive (I/O-bound) processes + throughput for CPU-bound

### MLFQ Rules (Classic — from OSTEP)

```
Q0: q = 8ms    (highest priority)
Q1: q = 16ms
Q2: FCFS       (lowest priority)
```

1. If **Priority(A) > Priority(B)** → A runs
2. If **Priority(A) == Priority(B)** → RR with queue's quantum
3. When process **enters system**, it goes to **highest priority** queue (Q0)
4. If process **uses whole quantum** → demoted one level (CPU-bound detected)
5. If process **yields CPU** before quantum ends → stays at same priority (I/O-bound)

### MLFQ Parameters (Design Decisions)
| Parameter | Options | Trade-off |
|-----------|---------|-----------|
| **Number of queues** | Fixed vs variable | More = finer control but complex |
| **Quantum per queue** | Same vs increasing | Increasing favors short bursts |
| **Promotion** | Periodic vs never | Prevents starvation (aging) |
| **Priority boost** | Every N ms | Resets demoted processes to top |

### Starvation Prevention
- **Aging**: Periodically boost all processes to top queue
- Without it, CPU-bound processes could stay at lowest level forever

## Linux CFS (Completely Fair Scheduler)

- **Goal**: Give each process a **fair share** of CPU
- Uses **virtual runtime** (`vruntime`) instead of priorities + fixed quanta
- Picks process with **smallest vruntime** (red-black tree for O(log n) selection)
- **sched_latency** (~6–48 ms): Time window over which CPU is divided fairly
- **Targeted latency**: Each process gets at least `sched_latency / n` time per cycle
- **`nice` value**: weight adjustment (lower nice = more CPU share)

```c
// CFS simplified: pick next task
struct sched_entity *pick_next_entity(struct cfs_rq *cfs_rq) {
    return rb_entry(rb_first(&cfs_rq->tasks_timeline), struct sched_entity, run_node);
}
// Process with smallest vruntime is leftmost in tree
```

### CFS vs MLFQ
| Aspect | MLFQ | CFS |
|--------|------|-----|
| Approach | Explicit priority queues | Proportional fairness (vruntime) |
| Prioritization | Queue level determines priority | Weighted by `nice` value |
| I/O vs CPU | Demotes CPU-hog, favors I/O | Naturally favors I/O (sleep accumulates vruntime credit) |
| Latency | Configurable per queue | Controlled by `sched_latency` |
