# Thrashing

## Definition

- **Thrashing:** process spends **more time paging than executing**
- Throughput drops to near zero
- CPU utilization plummets, system appears frozen

## Cause

- **Insufficient frames** allocated to a process (smaller than its working set)
- Triggers continuous page faults
- System tries to increase multiprogramming → makes it worse

## Thrashing Cycle (Feedback Loop)

```
High page fault rate
        ↓
Process waits for disk I/O (page in)
        ↓
CPU utilization decreases (idle waiting)
        ↓
OS thinks CPU is underutilized
        ↓
OS adds more processes (increase multiprogramming)
        ↓
Each process gets fewer frames
        ↓
Even more page faults
        ↓
THRASHING (collapse)
```

## Why It Happens

- Each process needs a **minimum number of frames** to execute efficiently
- **Working set:** set of pages actively referenced
- If `total working set size > available physical frames` → thrashing
- OS with CPU utilization based scheduling makes wrong decisions

## Detection

| Symptom | Indicator |
|---|---|
| Very high page fault rate | `p` approaches 0.1 or worse |
| Low CPU utilization | < 20% despite runnable processes |
| High disk I/O | Disk constantly swapping |
| Long run queue | Many processes waiting for CPU |

## Solution Strategies

### 1. Reduce Degree of Multiprogramming

- Swap out one or more processes entirely
- Let remaining processes get enough frames
- Also called **mid-term scheduling**

### 2. Working Set Model (prevention)

- Track each process's working set
- Only allocate if `sum(WSS_i) ≤ available frames`
- Deny new process admission if insufficient frames

### 3. Page Fault Frequency (PFF) Control

- Monitor page fault rate per process
- **Too high:** allocate more frames (process needs more)
- **Too low:** reclaim some frames (process has more than needed)
- Keep each process in its "sweet spot"

## Locality Model

- **Locality:** a set of pages actively used together
- Processes move between **localities** over time
- When locality shifts: working set changes, may trigger faults
- Thrashing occurs when locality size > available frames
- Working set ≈ current locality
