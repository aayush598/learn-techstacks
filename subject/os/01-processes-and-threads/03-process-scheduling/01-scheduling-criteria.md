# Scheduling Criteria

## CPU Burst & I/O Burst Cycles
- Process execution alternates between **CPU bursts** (computing) and **I/O bursts** (waiting for I/O)
- **CPU-bound processes**: Long CPU bursts, few I/O waits (e.g., matrix multiplication, video encoding)
- **I/O-bound processes**: Short CPU bursts, frequent I/O waits (e.g., text editor, web server)

```
      CPU burst    I/O burst    CPU burst    I/O burst
    ────────┐     ┌────────┐     ┌──────┐     ┌────────
            ↓     │        ↓     │      ↓     │
            ┌─────┐        ┌─────┐      ┌─────┐
            │ CPU │        │ I/O │      │ CPU │
            └─────┘        └─────┘      └─────┘
```

## Preemptive vs Non-Preemptive Scheduling

| | Non-Preemptive | Preemptive |
|---|----------------|------------|
| **Process releases CPU by** | Voluntarily (waiting, terminating) | Involuntarily (timer interrupt) |
| **Kernel involvement** | Minimal | Higher (context switch overhead) |
| **Starvation risk** | Higher (long process hogs CPU) | Lower |
| **Data integrity** | Easier (no race on kernel data) | Must use synchronization |
| **Examples** | FCFS, SJF (non-preemptive) | SRTF, Round Robin, Priority (preemptive) |

## Scheduling Criteria (Metrics)

| Metric | Definition | Formula |
|--------|------------|---------|
| **CPU Utilization** | % time CPU is busy doing useful work | `busy_time / total_time × 100` |
| **Throughput** | # processes completed per time unit | `processes / time` |
| **Turnaround Time** | Total time from submission to completion | `completion - arrival` |
| **Waiting Time** | Total time spent in ready queue (not running) | `turnaround - CPU_burst_sum` |
| **Response Time** | Time from submission to **first** CPU response | `first_run - arrival` |

### Optimization Goals
- **Interactive systems** (desktop, phone): Minimize **response time** + **variance** (predictability)
- **Batch systems** (servers, data centers): Maximize **throughput**, minimize **turnaround time**
- **Real-time systems**: Meet **deadlines** above all else

## Scheduler Types

| Scheduler | Frequency | Function | Decision |
|-----------|-----------|----------|----------|
| **Long-term** (job scheduler) | Low (seconds/minutes) | Controls degree of multiprogramming | Which processes admitted to ready queue |
| **Short-term** (CPU scheduler) | High (milliseconds) | Picks next process to run on CPU | Which ready process gets CPU |
| **Medium-term** (swapper) | Moderate | Swaps processes in/out of memory | Which process to suspend/swap |

```
                      Medium-term
                         │
                    ┌────┴────┐
                    │  Swap   │
                    │  in/out │
                    └─────────┘
                         │
  Long-term ──→ Ready Q ──→ Short-term ──→ CPU ──→ Exit
                         │
                    ┌────┴────┐
                    │  Wait Q │
                    └─────────┘
```

- **Long-term**: Limits multiprogramming to prevent thrashing
- **Short-term**: Called on every timer interrupt, I/O completion, system call
- **Medium-term**: Reduces memory pressure by suspending processes
