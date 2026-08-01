# Chapter: Virtual Memory Basics

## What you'll learn
- The **virtual memory** concept: a process's address space is larger than RAM; only the **working set** is resident.
- **Demand paging** and the full **page-fault path** (from PTE not-present to resumed instruction).
- **Copy-on-write** (how `fork()` gets cheap) and **memory-mapped files** (how files become memory via `mmap`).

## Prerequisites (linked)
- [Part 06 README](../README.md) — paging, page tables, PTEs, TLB (Chapters 03-04) are mandatory prerequisites.
- [Part 06 Chapter 01](part-06-memory-management/chapter-01-memory-architecture/README.md) — logical vs physical address.

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Virtual Memory Concept](section-01-virtual-memory-concept.md) | How can a process reference more memory than exists in RAM? |
| 02 | [Demand Paging and Page Faults](section-02-demand-paging-and-page-faults.md) | What exactly happens, step by step, when an instruction touches a missing page? |
| 03 | [Copy-on-Write and Memory-Mapped Files](section-03-copy-on-write-and-memory-mapped-files.md) | How does Linux make `fork()` and `mmap()` so cheap? |

## One-paragraph narrative connecting all sections
Virtual memory is the payoff of Part 06's paging: since translation is per-page, the OS can mark pages "not present" and load them only when touched. Section 01 establishes the concept — the process's logical space is a fiction backed by a fraction of RAM, justified by locality. Section 02 dives into the exact mechanism: the #PF trap, `do_page_fault`'s decisions (valid access → demand-load; invalid → SIGSEGV), and the cost model (a fault costs ~1M cycles if it hits disk). Section 03 shows the two features that make this practical in production: copy-on-write (fork becomes O(page tables), not O(memory)) and memory-mapped files (`mmap` unifies files and memory, the basis of executable loading, shared libraries, and databases).

## Common interview trap in this chapter
**Trap:** Believing a page fault is always an error. Most faults are *demand paging* — valid, expected, and required for a program to even start. Only faults on invalid addresses (outside any VMA, or permission violations) are bugs. Also, students confuse "virtual memory" with "swap": VM is the *abstraction*; swapping pages is just one *implementation* of eviction.

## Checklist before moving on
- [ ] I can state the locality argument for why VM works.
- [ ] I can trace a page fault end-to-end (hardware + kernel steps).
- [ ] I can explain why `fork()` uses copy-on-write and how the first write after fork behaves.
- [ ] I can explain what `mmap` does vs `read`, and where the file data lives.
- [ ] I can estimate the cost of a fault vs a TLB hit.
