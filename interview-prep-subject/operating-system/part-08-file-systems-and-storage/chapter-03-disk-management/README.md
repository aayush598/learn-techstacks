# Chapter: Disk Management

## What you'll learn
- **Disk structure**: platters, sectors/tracks/cylinders, seek + rotational latency, and how modern drives expose logical block addresses.
- **Disk scheduling algorithms**: FCFS, SSTF, SCAN (elevator), C-SCAN, LOOK/C-LOOK — which minimize seek time for which workloads.
- **RAID levels**: 0 (striping), 1 (mirroring), 5/6 (parity), 10 (striped mirrors) — the performance/reliability/capacity trade-off space, plus hot spares.
- **SSDs and hybrids**: NAND flash, wear leveling, TRIM, overprovisioning, and why scheduling on SSDs is different from HDDs.

## Prerequisites (linked)
- [Part 08 Chapter 01/02](chapter-01-files-and-directories/README.md) — file/block concepts.
- [Part 03 CPU Scheduling](part-03-cpu-scheduling/README.md) — the "elevator" analogy carries over from disk scheduling.

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Disk Structure and Disk Scheduling](section-01-disk-structure-and-disk-scheduling-algorithms.md) | What makes disk I/O slow (seek/rotation), and which order should requests be served? |
| 02 | [RAID Levels](section-02-raid-levels.md) | How do you combine disks for speed, redundancy, and capacity? |
| 03 | [Solid State Drives and Hybrid](section-03-solid-state-drives-and-hybrid.md) | How does NAND flash change everything (no seek, but wear + GC)? |

## One-paragraph narrative connecting all sections
Disks are mechanical (HDD) or flash (SSD), and their physics defines the I/O model. Section 01 dissects the HDD: seek time (moving the head) and rotational latency dominate random I/O, so the **scheduler** orders requests — from FCFS (fair, slow) to SSTF (greedy, starvation-prone) to SCAN/C-SCAN/C-LOOK (elevator algorithms that balance fairness and throughput) — while modern drives reorder internally via NCQ. Section 02 raises the abstraction: **RAID** stripes or mirrors data across many disks to increase bandwidth, add redundancy, or both (RAID 0/1/5/6/10), trading capacity and write cost for speed and safety. Section 03 accounts for the SSD revolution: no seek or rotation, so scheduling becomes about write amplification, wear leveling, TRIM, and garbage collection — and "hybrid" designs (Optane/NVMe tiers, HDD+SSD caching) combine the best of both. Together: how the OS + device manage the physical storage substrate Chapter 04's filesystems sit on.

## Common interview trap in this chapter
**Trap:** Treating disk scheduling as if it still mattered on SSDs — it doesn't (no seek); interviewers asking "why is disk scheduling obsolete on SSDs" want exactly that nuance. Also: mixing up RAID 5 vs RAID 6 (single vs double parity, tolerates 1 vs 2 failures) and thinking RAID 0 "mirrors" anything. And: "RAID = backup" — it's redundancy/performance, not backup (it doesn't protect against deletion/corruption).

## Checklist before moving on
- [ ] I can compute seek distance for FCFS/SSTF/SCAN/C-SCAN on a request queue.
- [ ] I can state each RAID level's usable capacity and failure tolerance.
- [ ] I can explain why SSD write amplification / wear leveling / TRIM exist.
- [ ] I can explain why disk scheduling is nearly irrelevant on SSDs.
- [ ] I can compare NCQ/native command queuing with elevator scheduling.
