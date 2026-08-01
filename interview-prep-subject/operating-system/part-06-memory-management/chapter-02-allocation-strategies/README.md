# Chapter: Allocation Strategies

## What you'll learn
- How the OS divides physical RAM among processes when each needs a contiguous block: **contiguous memory allocation**.
- The two flavors of memory waste — **internal fragmentation** (allocated but unused space) vs **external fragmentation** (free holes too small/uselessly placed) — and how **compaction** and **swapping** try to fix them.
- **Partitioning** (fixed vs dynamic) and **swapping** (moving whole processes between RAM and disk), with real numbers for placement algorithms.

## Prerequisites (linked)
- [Part 06 README](../README.md) — where this fits in memory management.
- [Chapter 01 Memory Architecture](chapter-01-memory-architecture/README.md) — you must be fluent in logical vs physical addresses, base/limit, and binding before studying allocation.

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Contiguous Memory Allocation](section-01-contiguous-memory-allocation.md) | How does the OS carve one contiguous chunk out of RAM for each process, and which hole do I pick? |
| 02 | [Fragmentation and Compaction](section-02-fragmentation-and-compaction.md) | Where exactly does RAM get wasted, and what can we do about it without paging? |
| 03 | [Partitioning and Swapping](section-03-partitioning-and-swapping.md) | Fixed vs dynamic partitions; when does the OS swap entire processes out to disk, and at what cost? |

## One-paragraph narrative connecting all sections
Given base/limit protection, the natural way to place processes is to give each a contiguous window of RAM. Section 01 shows the two classic placement algorithms (fixed and dynamic partitions), the free-list data structure, and the hole-selection policies (first/best/worst-fit) with concrete byte math. Section 02 quantifies the two failure modes that arise: internal fragmentation (wasted space *inside* an allocated block) and external fragmentation (free space split into unusable holes), then examines compaction — shifting processes to merge holes — and explains why compaction is expensive and why it was abandoned for anything except specialty systems. Section 03 completes the picture with swapping (moving whole processes to disk to free RAM, the ancestor of virtual memory) and shows why swapping + contiguous allocation collapses under large processes — setting up paging (Chapter 03) as the real fix.

## Common interview trap in this chapter
**Trap:** Confusing internal and external fragmentation. Internal = inside an allocated block (e.g., process takes 13 KB but the OS gives it a 16 KB partition — 3 KB wasted, unusable by anyone). External = between blocks (free holes too small to satisfy a request, even though their sum is huge). Remember: **fixed partitions → internal; variable partitions → external** (paging's granularity also creates internal-only). Another trap: "best-fit is always optimal" — it minimizes wasted *space* per allocation but is slowest and creates many tiny holes; first-fit is usually the practical winner.

## Checklist before moving on
- [ ] I can explain the free-list and the O(1) idea behind fixed partitioning.
- [ ] I can compute first-fit / best-fit / worst-fit placements on a worked example.
- [ ] I can explain both fragmentation types and which scheme causes which.
- [ ] I understand why compaction is O(total memory) and can't be done safely on running systems.
- [ ] I can explain swap-in/swap-out cost and the double-swap inefficiency.
- [ ] I can articulate why contiguous allocation fails at scale → motivates paging.
