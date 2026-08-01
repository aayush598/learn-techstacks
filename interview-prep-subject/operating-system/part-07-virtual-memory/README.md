# Part: Virtual Memory

> **TL;DR**: Virtual memory lets a program run when only *part* of it is in RAM — pages are loaded on demand, evicted by page-replacement algorithms, and shared via copy-on-write and `mmap` — so systems run far more memory than physical RAM.

## What this part covers
Part 07 explains how the OS goes from "all of a process must be resident" (Part 06) to "only the working set needs RAM." You'll learn the demand-paging mechanism and page-fault path, the page-replacement algorithms (FIFO, Optimal, LRU, Clock, LFU) with their correctness/thrashing implications, frame allocation, the working-set model, and how modern kernels (Linux) actually implement all of it — including copy-on-write, memory-mapped files, KSM, zswap, and huge pages.

## Chapter map (chapter → sections → key skills)

| Chapter | Sections | Key skills you'll gain |
|---|---|---|
| **Chapter 01: Virtual Memory Basics** | the concept; demand paging & page faults; copy-on-write & mmap | Explain why VM works (locality); trace the fault path; implement/describe `mmap` and COW |
| **Chapter 02: Page Replacement Algorithms** | fundamentals; FIFO & Optimal; LRU & approximations; Clock & LFU; frame allocation | Simulate each algorithm by hand; analyze Belady's anomaly; compute hit ratios; choose frames per process |
| **Chapter 03: Thrashing & Advanced** | thrashing & working set; advanced modern VM | Diagnose and fix thrashing; describe Linux's VM internals (kswapd, OOM killer, THP, zswap) |

## Study order
1. **Chapter 01** — the concept + mechanism (how a missing page becomes a resident page).
2. **Chapter 02** — once pages are missing, decide *which* to evict (the algorithmic core).
3. **Chapter 03** — when eviction spirals (thrashing) and how production kernels cope.

## Interview importance
★★★★★ — virtual memory is the single most-tested memory topic. Every FAANG OS round includes "how does a page fault work," "compare LRU vs FIFO vs Clock," "what is thrashing," and "explain mmap." Google and Apple (kernel teams), Meta (infra), Amazon, Microsoft, Nvidia, VMware, and all systems-focused startups probe it deeply.

## How the parts connect (roadmap)
- **Part 06 (Memory Management)** gave you paging/page tables/TLB — VM is literally "what the OS does when the PTE says *not present*."
- **Part 08 (File Systems)** pairs with `mmap` (files as memory) and swap storage.
- **Part 09 (Linux Internals)** shows `do_page_fault`, `kswapd`, and the real allocation paths that implement this part.
