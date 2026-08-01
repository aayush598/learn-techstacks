# Chapter: Paging

## What you'll learn
- How **paging** chops both the virtual address space and physical RAM into fixed-size **pages/frames** so a process's memory can be scattered anywhere — eliminating external fragmentation.
- How **page tables** map virtual page → physical frame, and exactly what a **PTE** (page-table entry) contains.
- How the **TLB** (Translation Lookaside Buffer) makes per-access translation fast, and the price of misses.
- The **multilevel / hierarchical / hashed / inverted** page-table designs that keep page tables small in 64-bit address spaces.

## Prerequisites (linked)
- [Part 06 README](../README.md) and [Chapter 01 Memory Architecture](chapter-01-memory-architecture/README.md) — logical/physical addresses, MMU, base/limit.
- [Chapter 02 Allocation Strategies](chapter-02-allocation-strategies/README.md) — know why fragmentation and contiguity forced this change.

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Paging Basics and Page Tables](section-01-paging-basics-and-page-tables.md) | How does splitting memory into 4 KB units let a process's RAM be scattered and free of external fragmentation? |
| 02 | [TLB (Translation Lookaside Buffer)](section-02-tlb-translation-lookaside-buffer.md) | Why is a naive page-table lookup too slow, and how does the TLB fix it? |
| 03 | [Multilevel, Hierarchical and Hashed Page Tables](section-03-multilevel-hierarchical-and-hashed-page-tables.md) | How do we store page tables for 2⁶⁴ addresses without 2⁵² entries per process? |
| 04 | [Paging Hardware Examples and Page Table Entry](section-04-paging-hardware-examples-and-page-table-entry.md) | What does a real x86-64 PTE and page-table walk look like, bit by bit? |

## One-paragraph narrative connecting all sections
Paging answers Chapter 02's failures with one idea: make the allocation unit a fixed 4 KB **page** and let pages live in any physical **frame**. Section 01 defines the mechanism — splitting virtual and physical addresses into `page | offset` and `frame | offset`, with a **page table** holding the mapping and protection bits per page. Section 02 confronts the performance problem: a page-table lookup on every access is too slow, so the **TLB** caches recent translations in hardware, making the common case O(1). Section 03 handles the scale problem: a flat table for 2⁶⁴ addresses would need 2⁵² entries, so real systems use **multilevel tables** (allocate only what's used), **hashed tables** (compact but slower), and **inverted tables** (one entry per frame, for very large address spaces). Section 04 grounds all of it in real hardware: the x86-64 **4-level walk** and the exact PTE bits (present, rw, user, accessed, dirty, NX) that Linux programs every day. After this chapter, Part 07 (virtual memory) is just "what happens when the PTE says the page isn't in RAM."

## Common interview trap in this chapter
**Trap:** Saying "the page table is indexed by page number" without noting *who walks it*. On x86-64 the **hardware MMU** walks the table on a TLB miss (driven by CR3); on some architectures (e.g., early MIPS) the *OS* handles misses in software. Also, `page_table[page]` with a flat array is *never* used on 64-bit — always multilevel; and the TLB is **not** the page table (they're often conflated in answers). Finally: internal fragmentation under paging is ≤ 4 KB−1 **per mapping**, not per process.

## Checklist before moving on
- [ ] I can translate a virtual address to physical by hand given a page table.
- [ ] I can explain the TLB hit/miss path and why it's needed.
- [ ] I can design a 2-level/4-level page table and compute its memory footprint.
- [ ] I can read a real x86-64 PTE and identify present/rw/user/accessed/dirty/NX bits.
- [ ] I can explain why paging kills external fragmentation but keeps internal.
- [ ] I understand hardware-walk vs software-walk (software-loaded TLB) differences.
