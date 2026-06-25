# I/O Scheduling

## Purpose
- Reorder I/O requests to **minimize seek time** and **maximize throughput**
- Need arises from **mechanical nature of HDDs** (seek + rotation delays)

## Scheduling at Different Levels

### OS-Level I/O Scheduling (Linux)
| Scheduler | Approach | Use Case |
|-----------|----------|----------|
| **CFQ** (Completely Fair Queuing) | Per-process time-sliced I/O | General-purpose, fairness |
| **Deadline** | Per-request deadlines (read = 500ms, write = 5s) | Databases, latency-sensitive |
| **NOOP** | No reordering; simple FIFO + merging | SSDs, NVMe (no seek) |
| **BFQ** (Budget Fair Queuing) | Weight-based I/O allocation | Interactive desktop |
| **Kyber** | Queue depth control | Low latency, consistent |

### Device-Level Scheduling (NCQ)
- **Native Command Queuing** (SATA) / **NVMe queues**: drive-internal scheduling
- Drive knows its **physical geometry** better than OS
- Supports **up to 32 commands** (SATA) or **64K queues × 64K commands** (NVMe)

## I/O Request Merging
- **Adjacent requests**: combine `read block 4` + `read block 5` → single `read blocks 4-5`
- Reduces number of I/O operations (more efficient for device)
- Linux block layer automatically merges

## Linux Block Layer Architecture
```
Application (read/write syscall)
    ↓
VFS + Page Cache
    ↓ (submits bio to block layer)
Block Layer (I/O scheduler + merge + sort)
    ↓ (scsi/cmd -> device driver)
Device Driver → Hardware
```

## Key Interview Questions
- Why does Linux have multiple I/O schedulers? → Different workloads need different trade-offs (fairness vs latency vs throughput)
- Which scheduler for SSDs? → **NOOP** or **Kyber** or **none** (NVMe): no seek time, so reordering adds overhead without benefit
- What is **write starvation**? → Reads blocked by many writes; Deadline scheduler helps by giving reads priority (reads are synchronous)
- How does **merged request** improve performance? → Fewer I/O operations, better sequential access pattern
- What is **I/O priority** (ionice)? → CFQ/BFQ supports `ionice -c 2 -n 0` (best-effort, high priority)
