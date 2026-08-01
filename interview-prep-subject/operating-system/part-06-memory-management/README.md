# Part: Memory Management

> **TL;DR**: Memory management is the OS subsystem that decides *which process's code/data lives where in physical RAM*, translates every program's addresses safely, and recycles memory efficiently — the foundation for every other OS feature including virtual memory (Part 07).

## What this part covers
Part 06 explains the physical-memory layer of the OS before virtual memory: how address spaces are constructed, how programs get bound to physical addresses, how the CPU's MMU translates logical→physical addresses, and how the OS divides physical RAM among processes (contiguous allocation, paging, segmentation). By the end you can answer "how does a `load` instruction on a process's virtual address actually reach a physical DIMM?" — the single most-asked OS interview topic.

## Chapter map (chapter → sections → key skills)

| Chapter | Sections | Key skills you'll gain |
|---|---|---|
| **Chapter 01: Memory Architecture** | address spaces & address binding; logical vs physical addresses & MMU; base & limit registers | Explain compile-time/load-time/run-time binding; describe the MMU; describe memory protection via base/limit |
| **Chapter 02: Allocation Strategies** | contiguous allocation; fragmentation & compaction; partitioning & swapping | Solve allocation problems (first/best/worst fit); quantify internal vs external fragmentation; describe swap-in/swap-out |
| **Chapter 03: Paging** | paging basics & page tables; TLB; multilevel/hierarchical/hashed page tables; paging hardware & PTE | Translate virtual→physical by hand; design page tables (incl. inverted); analyze TLB hit/miss; read an x86-64 PTE |
| **Chapter 04: Segmentation** | segmentation in depth; segmentation + paging (x86 & modern OS) | Translate segmented addresses; explain why OSes abandoned pure segmentation; describe the 4-level paging used by Linux on x86-64 |

## Study order
1. **Chapter 01** — build the address-translation mental model (bind time, MMU, protection).
2. **Chapter 02** — see why the naïve "just give each process a big chunk" approach fails (fragmentation).
3. **Chapter 03** — learn the fix: paging (the dominant technique on every modern CPU).
4. **Chapter 04** — segmentation (what was tried, why it failed, and how it survives inside paging).

## Interview importance
★★★★★ — memory management is a top-3 OS interview topic at every FAANG/MAANG company. Google, Meta, Amazon, and Apple all ask about page tables, TLB, and fragmentation. Expected in every systems-design and OS round. Companies emphasizing it: Google (systems), Meta (product infra), Amazon (SDE), Apple (kernel teams), Microsoft (Windows), VMware, Nvidia (driver stacks), any company doing low-level work.

## How the parts connect (roadmap)
- **Part 01-05** (concurrency, processes, CPU scheduling) assume *multiple programs in RAM at once* — Part 06 shows how the OS actually arranges that safely.
- **Part 07 (Virtual Memory)** is the direct sequel: paging from Part 06 is what *enables* demand paging, page replacement, and copy-on-write. Master Part 06 first.
- **Part 09 (Linux internals)** shows the real `struct mm_struct`, page fault handlers, and `do_page_fault` that implement the tables you learn here.
- **Part 08 (File systems)** reuses these ideas (block allocation mirrors page allocation; memory-mapped files glue VM and FS together).
