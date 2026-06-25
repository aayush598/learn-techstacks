# Disk Scheduling — LOOK & C-LOOK

## LOOK (Elevator with Early Turnaround)
- Like SCAN, but **arm reverses at the last request** in that direction
- Does NOT go all the way to cylinder 0 or max
- Example (queue: `[98, 183, 37, 122, 14, 124, 65, 67]`, head = 53)
  - Direction: toward 0 → serve 37, 14 → reverse → serve 65, 67, 98, 122, 124, 183
  - Total: |53-37| + |37-14| + |14-65| + |65-67| + |67-98| + |98-122| + |122-124| + |124-183|
  - = **208 cylinders**
- **Improvement over SCAN**: saves unnecessary travel to cylinder edges

## C-LOOK (Circular LOOK)
- Like C-SCAN, but **arm goes only to last request** in that direction, then jumps back
- Example (same queue, head = 53, direction toward 199):
  - Serve 65, 67, 98, 122, 124, 183 → **jump back** to 14 → serve 37
  - Total: |53-65| + |65-67| + |67-98| + |98-122| + |122-124| + |124-183| + |183-14| + |14-37|
  - = **322 cylinders**
- **Improvement over C-SCAN**: less unnecessary travel

## Comparison: SCAN vs LOOK vs C-SCAN vs C-LOOK

| Algorithm | Total Movement | Arm Travel | Wait Var | Complexity |
|-----------|---------------|------------|----------|------------|
| **SCAN** | 236 | Goes to 0 & 199 | High | Simple |
| **C-SCAN** | 382 | Goes to 0 & 199 | Low | Simple |
| **LOOK** | **208** | Reverses at min/max request | High | Moderate |
| **C-LOOK** | **322** | Jumps from max to min request | Low | Moderate |

## Which Algorithm to Choose?

| Workload | Recommended | Reason |
|----------|-------------|--------|
| **Database (OLTP)** | LOOK / C-LOOK | Random I/O; minimal seek |
| **Web server** | C-LOOK | Uniform latency across disk |
| **File server** | LOOK | Good throughput for large files |
| **Time-sharing** | C-LOOK | Fairness across users |
| **Batch system** | LOOK | Maximum throughput |

## Modern Disks & SSDs
- **HDDs**: disk scheduling matters — 5-10ms seek times
- **NCQ** (Native Command Queuing): drive-internal scheduling; reorders more efficiently than OS
- **SSDs**: **no seek time** (3μs access); disk scheduling algorithm makes **no difference**
- For SSDs, focus on **I/O merging** and **queue depth** (NVMe supports 64K queues)

## Key Interview Questions
- Why is LOOK better than SCAN? → Eliminates unnecessary empty travel to cylinder edges
- Can LOOK still starve requests? → If they arrive at the end the arm just left, they wait a full cycle
- Do we even need disk scheduling for SSDs? → **No** — uniform access time; but **I/O merging** (combine adjacent requests) still helps
- What about deadline I/O schedulers? → Linux **CFQ**, **Deadline**, **BFQ** enforce fairness; **NOOP** (no-op, pass-through) best for SSDs
