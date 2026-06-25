# FCFS & SJF Scheduling

## FCFS (First-Come, First-Served)

- Non-preemptive — CPU allocated in order of arrival
- **Implemented with FIFO queue** (enqueue arrivals, dequeue dispatch)
- **Convoy Effect**: Short processes wait behind long ones → poor avg waiting time

### Example
Processes: P1=24, P2=3, P3=3 (arrival order: P1, P2, P3)

```
Gantt: ┌────── P1 (24) ──────┬── P2 ──┬── P3 ──┐
       0                     24      27       30
```

| Process | Waiting Time |
|---------|-------------|
| P1 | 0 |
| P2 | 24 |
| P3 | 27 |
| **Avg** | **(0+24+27)/3 = 17** |

## SJF (Shortest-Job-First / Non-Preemptive)

- Choose process with **smallest next CPU burst**
- **Optimal** for minimizing avg waiting time (if all bursts known)
- Problem: **Starvation** — long processes may never execute if short ones keep arriving

### Example
Processes: P1=6, P2=8, P3=7, P4=3

```
Arrival order: P1, P2, P3, P4
SJF order: P4(3) → P1(6) → P3(7) → P2(8)

Gantt: ┌─P4─┬── P1 ──┬─── P3 ───┬──── P2 ────┐
       0    3        9          16           24
```

| Process | Waiting Time |
|---------|-------------|
| P4 | 0 |
| P1 | 3 |
| P3 | 9 |
| P2 | 16 |
| **Avg** | **(0+3+9+16)/4 = 7** |

Compare with FCFS on same set: avg = `(0+6+14+21)/4 = 10.25` ⟶ SJF is better

## SRTF (Shortest Remaining Time First / Preemptive SJF)

- Preemptive version of SJF
- When a new process arrives, compare its **remaining time** with current running process
- Preempt if new process has **shorter remaining time**

### Example
| Process | Arrival | Burst |
|---------|---------|-------|
| P1 | 0 | 8 |
| P2 | 1 | 4 |
| P3 | 2 | 9 |

```
Gantt: ┌─P1─┬── P2 ──┬── P1 ──┬────── P3 ──────┐
       0    1        5        9                 17
```

- At t=1: P2 arrives (burst=4) < P1 remaining (7) → preempt P1
- At t=5: P2 done → resume P1 (remaining 7) → runs to completion
- Avg waiting time: P1=1, P2=0, P3=6 → **avg = 2.33** (better than SJF non-preemptive)

## Predicting Next CPU Burst (Exponential Averaging)

Since future burst lengths are unknown, predict using **exponential moving average**:

```
τₙ₊₁ = α · tₙ + (1 - α) · τₙ
```

Where:
- `tₙ` = actual burst length of `n`th occurrence
- `τₙ` = predicted burst for `n`th occurrence
- `α` = smoothing factor (0 ≤ α ≤ 1)
  - **α = 0**: Ignore recent history (always predict τ₀)
  - **α = 1**: Only use most recent burst
  - **α = 0.5**: Equal weight to history and recent

```c
// Typical implementation
static int predict_burst(int prev_actual, int prev_predicted, double alpha) {
    return (int)(alpha * prev_actual + (1 - alpha) * prev_predicted);
}
```
