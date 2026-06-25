# Disk Scheduling — FCFS, SSTF, SCAN, C-SCAN

## Disk Scheduling Problem
- Goal: minimize **seek time** (head movement)
- Access time = **seek time** + **rotational latency** + **transfer time**
- Seek dominates (~10ms), so we reorder the request queue

## Example (standard interview problem)
**Request queue**: `[98, 183, 37, 122, 14, 124, 65, 67]`
**Head starts at**: `53`

## FCFS (First-Come, First-Served)
- Serve requests in arrival order
- **Pros**: fair, no starvation
- **Cons**: poor performance (zig-zag head movement)
- Total movement: |53-98| + |98-183| + |183-37| + |37-122| + |122-14| + |14-124| + |124-65| + |65-67|
- = **640 cylinders**

## SSTF (Shortest Seek Time First)
- Select request with minimum seek distance from current head
- **Pros**: better throughput than FCFS
- **Cons**: **starvation possible** (far-away requests may never be served)
- Order: 53 → 65 (12) → 67 (2) → 37 (30) → 14 (23) → 98 (84) → 122 (24) → 124 (2) → 183 (59)
- Total: **236 cylinders**

## SCAN (Elevator Algorithm)
- Head moves **one direction** (toward 0 or toward max), serving all requests
- Reverses at **end of disk** (cylinder 0 or 199)
- **Assumption**: disk has 200 cylinders (0-199)
- Direction: toward 0 → serve 37, 14 → at 0 → reverse → serve 65, 67, 98, 122, 124, 183
- Order: 53 → 37 (16) → 14 (23) → 0 (14) → 65 (65) → 67 (2) → 98 (31) → 122 (24) → 124 (2) → 183 (59)
- Total: **236 cylinders**

## C-SCAN (Circular SCAN)
- Head moves **one direction only**, serving requests
- When reaching end, **jump back** to start (no service on return)
- **Uniform wait time**: treats all cylinders equally
- Order: 53 → 65 (12) → 67 (2) → 98 (31) → 122 (24) → 124 (2) → 183 (59) → **199** (16) → **0** (199) → 14 (14) → 37 (23)
- Total: **382 cylinders**

## Algorithm Comparison

| Algorithm | Total Movement | Starvation | Direction Changes | Wait Time Variance |
|-----------|---------------|------------|-------------------|-------------------|
| **FCFS** | 640 | ❌ No | Many | High |
| **SSTF** | 236 | ✅ Yes | Many | Moderate |
| **SCAN** | 236 | ❌ No | 1 (per cycle) | High (ends wait longer) |
| **C-SCAN** | 382 | ❌ No | 0 (jumps back) | Low (uniform) |

## Key Interview Questions
- Which is fastest? → SSTF gives lowest total movement but can starve
- When to use C-SCAN? → Heavy load; want **variance-free wait times** (time-sharing systems)
- Real-world behavior: modern drives use **internal scheduling** (TCQ/NCQ); OS issues are less impactful for a single disk
