# Priority & Round Robin Scheduling

## Priority Scheduling

- Each process has a **priority** (lower number = higher priority, typically)
- Scheduler picks process with highest priority from ready queue
- **Preemptive**: Lower-priority preempted when higher-priority arrives
- **Non-preemptive**: New higher-priority waits for running process to yield

### Problems
| Problem | Description | Solution |
|---------|-------------|----------|
| **Starvation** | Low-priority processes may never execute | **Aging** — gradually increase priority of waiting processes |
| **Indefinite Blocking** | Process never gets CPU | Same — aging guarantees eventual execution |

### Example (Preemptive)
| Process | Burst | Priority |
|---------|-------|----------|
| P1 | 8 | 3 (low) |
| P2 | 4 | 1 (high) |
| P3 | 2 | 2 |

```
Gantt: ┌─P2─┬── P3 ──┬────────── P1 ──────────┐
       0    4        6                        14
```

## Round Robin (RR)

- **Time-sharing** — each process gets a fixed **time quantum** (q)
- Processes **preempted** when quantum expires → placed at end of ready queue
- **FCFS within each quantum** — essentially preemptive FCFS with time limit

### Performance vs Quantum Size

| Quantum Size | Effect | Analogy |
|-------------|--------|---------|
| **Very large** (q → ∞) | Degrades to FCFS | No benefit |
| **Very small** (q → 0) | Too many context switches | CPU wasted on overhead |
| **Optimal** | q slightly > typical CPU burst | Most processes complete in one quantum |

### Example (q = 4)
| Process | Burst |
|---------|-------|
| P1 | 10 |
| P2 | 4 |
| P3 | 5 |

```
Gantt: ┌P1─┬P2─┬P3─┬P1─┬P3─┬─P1─┐
       0   4   8   12  16  18   21
```

| Process | Wait Time |
|---------|-----------|
| P1 | (0+8) = 8 |
| P2 | 4 |
| P3 | (4+4) = 8 |
| **Avg** | **(8+4+8)/3 = 6.67** |

### Context Switch Overhead Calculation

If q = 10ms, context switch time = 1ms:
- **Useful CPU**: 10/11 = ~**91%**
- **Overhead**: 1/11 = ~**9%**

```
overhead_pct = context_switch_time / (quantum + context_switch_time)
```

**Rule**: Quantum should be **>> context switch time** (typically 10–100 ms vs ~1–10 µs)

### Turnaround Time vs Quantum
- For **n** processes with total CPU time **T**, worst-case turnaround time = **n × q** (each process runs once per round)
- Larger q reduces context switches but increases response time
- Typical Linux default: **100 ms** (CFS uses variable time slices based on priority)
