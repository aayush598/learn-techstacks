# Paging Basics and Page Tables

> **TL;DR**: Paging splits both the virtual address space and physical RAM into fixed-size units (**pages** and **frames**, usually 4 KB), maps each page to any frame via a **page table**, and thereby eliminates external fragmentation while keeping hardware protection per page.

## 1. Why Does This Exist?
Contiguous allocation (Chapter 02) fails because processes need variable-size contiguous blocks: free memory fragments externally and large processes can't fit. Paging exists to make the *allocation unit fixed*. By dividing the virtual address space into **pages** and physical RAM into **frames** of identical size, a process's memory no longer needs to be contiguous — each page can live in any free frame. This one decision eliminates external fragmentation entirely (there's always a free 4 KB page if *any* 4 KB is free), enables sharing (two page tables can point at one frame), and makes growth trivial (add another page mapping). It's the mechanism every modern general-purpose OS (Linux, Windows, macOS, Android, iOS) is built on.

## 2. How Does It Work?
1. Choose page size, typically **4 KB** (4096 bytes). The virtual address is split:
   - `page number` = high bits (e.g., bits 31..12 on 32-bit).
   - `offset` = low 12 bits.
2. Physical address is `frame number | same offset`.
3. A **page table** — an array indexed by page number, with one entry (PTE) per page — holds the frame number plus protection bits (present, rw, user, accessed, dirty, NX).
4. Translation: `frame = page_table[page].frame; phys = (frame << 12) | offset`. On TLB miss, the MMU walks the table; on PTE not-present or permission violation, it raises a page fault.

Because page and frame sizes are equal, the **offset passes through unchanged** — the beauty of the design.

## 3. When Is It Used?
- **Every general-purpose OS**, all the time: Linux, Windows, macOS, Android, iOS, BSDs.
- **Virtualization**: guest page tables + EPT/NPT compose the same idea twice.
- **Huge pages**: 2 MB / 1 GB pages for databases, VMs, JVM heaps (fewer table entries, fewer TLB misses).
- **Embedded with MMUs**: Cortex-A systems, most Linux-on-ARM.
- **Memory protection units** (MPU) in MMU-less parts are paging's cousin but don't translate.

## 4. Why Wasn't Another Approach Chosen?
- **Contiguous allocation**: fails on external fragmentation, growth, sharing — paging fixes all three at the price of a page table + TLB. Chosen instead.
- **Segmentation**: matches program structure (code/data/stack as separate segments) but suffers external fragmentation again (variable sizes) — paging's fixed size is the key advantage. See Chapter 04.
- **Single-level page table**: needs one PTE per page of the *whole address space* (e.g., 2²⁰ entries = 4 MB per process on 32-bit; 2⁵² on 64-bit) — wasteful. Replaced by multilevel (Section 03).
- **Software translation (no MMU)**: too slow; must be hardware.
- **Protection keys only**: fast region checks but no translation — a supplement, not a replacement.

## 5. Intuition
Imagine a library with 4096 books. Instead of shelving a multi-volume encyclopedia contiguously, you put each volume on any free shelf. The catalog (page table) records "encyclopedia volume 5 → shelf 231." To read volume 5, you look up the catalog, go to shelf 231, and read the book. Since all volumes are the same size (fixed pages), any free shelf works — no more "need 40 consecutive shelves." The catalog is the page table; the shelves are frames; the lookup clerk is the MMU.

## 6. Real-World Analogy
A shipping company moves crates of fixed size. A shipment may consist of 100 crates; each crate can go on any truck, in any order, on any route — the manifest (page table) records which crate is on which truck. Fixed crate size means no truck is ever partially wasted in a way that blocks another shipment (only up to one crate's worth of slack at the end — internal fragmentation). The manifest is per-customer (per-process page table).

## 7. Formal Definition
**Paging** is a memory-management scheme that permits the physical address space of a process to be non-contiguous. Physical memory is divided into **frames** of size F; the logical address space into **pages** of size F. A **page table** maps logical page numbers to frame numbers; a **page-table entry (PTE)** stores the frame number and control/protection bits. The logical address is `(page number, offset)`; the physical address is `(frame number, offset)`. Because frames and pages are equal-sized, the offset is not translated.

## 8. Example
Page size 4 KB, a 32-bit address `0x2A1C` = binary `0010 1010 0001 1100`. 
- page = `0x2A1C >> 12` = `0x2`; offset = `0x2A1C & 0xFFF` = `0xA1C`.
- Process's page table: page 0→frame 7, page 1→frame 4, page 2→frame 12.
- Physical = `12 << 12 | 0xA1C` = `0xC000 | 0xA1C` = `0xCA1C`.

Second access `0x3000` (page 3): page table has no entry / present=0 → **page fault** → kernel either loads a frame (demand paging, Part 07) or kills the process (SIGSEGV).

Now, memory layout: the process's 3 pages live at frames 7, 4, 12 — scattered. Even with zero *contiguous* space available, the process runs, as long as 3 individual frames are free. That is the anti-fragmentation win.

## 9. Internal Working
1. **Page table allocation**: on `fork()`, the kernel allocates a root page-table structure for the child (copy-on-write page tables in Linux — the child shares until written).
2. **Walk on TLB miss**: MMU reads CR3 → PML4 base → indexes PML4E/PDPTE/PDE/PTE by address bits → gets frame.
3. **PTE check**: present bit set? rw/user bits permit this access? If not → #PF.
4. **Combine**: physical = (PTE.PFN << 12) | offset.
5. **Cache**: load the translation into the TLB.
6. **Fault handling**: kernel `do_page_fault` — validates the VMA, allocates a zeroed frame (or reads from disk/swap), installs the PTE, flushes nothing (page wasn't cached), returns to retry the instruction.
7. **On free**: `munmap`/exit tears down page tables, returns frames to the buddy allocator.

## 10. Time Complexity
- Translation with TLB hit: O(1) (~1 cycle).
- Translation with TLB miss: O(L) where L = number of levels (4 on x86-64) — plus memory latencies; ~30–80 cycles with page-walk caches.
- Page-table lookup structure: array index = O(1) per level.
- Page fault: O(page-table ops) + O(frame allocation) + O(I/O if backing store) — dominated by disk (ms).
- Page table memory: O(#mapped pages) with multilevel, not O(#possible pages).
- Memory for one level of page tables on 32-bit: 2²⁰ × 4 B = 4 MB per process (why multilevel matters).

## 11. Advantages
- **No external fragmentation** — any 4 KB frame fits any request.
- **Sharing**: two processes map the same frame (shared libraries, copy-on-write) by pointing at the same frame number.
- **Fine-grained protection**: per-page r/w/x, present, user/supervisor.
- **Easy growth/shrink**: `mmap`/`mprotect`/`munmap` add/remove page mappings.
- **Enables virtual memory** (Part 07): pages can be absent, demand-loaded, swapped.
- **Internal fragmentation is bounded** at ≤ page_size − 1 per mapping.

## 12. Disadvantages
- **Internal fragmentation**: the last page of each mapping is under-full (up to 4 KB−1 wasted).
- **Page-table overhead**: multilevel tables cost memory (a few KB to MBs per process) and time to walk.
- **TLB pressure**: small TLBs thrash under large working sets → huge pages mitigate.
- **Not "natural"**: paging ignores program structure (code vs data vs stack are treated the same) — segmentation had that advantage (Chapter 04).
- **Access time**: even with TLBs, cold mappings pay the walk cost.
- Complexity: fault handling, TLB invalidation, and copy-on-write logic.

## 13. Interview Questions
1. **Q: What is paging and why is it used?** A: Splitting virtual and physical memory into equal fixed-size pages/frames and mapping page→frame via a page table; it eliminates external fragmentation, enables sharing, per-page protection, and virtual memory.
2. **Q: How do you translate a logical address under paging?** A: Split into `page | offset`; look up `frame = page_table[page]`; physical = `(frame << 12) | offset`; offset passes unchanged.
3. **Q: What's the difference between a page, a frame, and an offset?** A: Page = unit of virtual memory; frame = unit of physical memory; offset = byte within the page/frame (identical low bits). Pages map to frames 1:1 by size.
4. **Q: What does a page table entry contain?** A: The frame number plus control bits: present, read/write, user/supervisor, accessed, dirty, NX (and, in some OSes, protection keys, software bits, or the physical frame address).
5. **Q: What happens if the page isn't present?** A: MMU raises a page fault (#PF); the kernel checks whether the address is in the process's VMA list — if yes, demand-loads/swap-in/zero-fills the page and resumes; if no, sends SIGSEGV.
6. **Q: Why does paging cause only internal, not external, fragmentation?** A: The unit is fixed (4 KB): any page fits any free frame, so free memory never becomes "too small to be useful"; only the last page of a mapping can be under-filled (≤ 4 KB−1).
7. **Q: How do two processes share a library? (Tricky)** A: Both page tables contain a PTE pointing to the *same frame number* for the library's pages; the pages are marked read-only/executable so neither can corrupt the shared copy (writes trigger copy-on-write or PROT_NONE semantics).
8. **Q: How is a page table allocated for a new process? (Scenario)** A: On `fork()`, Linux copies or marks copy-on-write the parent's page tables (child shares frames until writes); on `exec`, fresh empty tables are built lazily as segments map in.
9. **Q: What is the cost of a page table for a full 32-bit space?** A: 2²⁰ pages × 4 bytes = 4 MB — too much for most processes; multilevel tables allocate only used regions, shrinking the footprint dramatically.
10. **Q: Why is the offset not translated?** A: Because page and frame sizes are equal, the low-order bits index into the page/frame identically; translation only changes the high (page→frame) bits.
11. **Q: What's the worst-case internal fragmentation of paging?** A: For a mapping of size S, `page_size − 1` bytes (≈4 KB); the *average* is half a page. For many small `mmap`s, this is the main memory waste — which is why glibc uses larger `mmap` thresholds and why huge pages trade granularity for TLB efficiency.
12. **Q: When would you NOT want paging? (Production)** A: Hard real-time/safety-critical systems (page faults introduce unbounded latency), minimal microcontrollers (no MMU), and some high-performance DMA paths where physical contiguity is required.

## 14. Follow-Up Questions
1. **Q: What's the difference between hardware-walk and software-walk (TLB load) architectures?** A: On x86-64, the MMU walks page tables itself; on MIPS/SPARC, a TLB-miss exception hands control to the OS, which fills the TLB from its own structures. Software-walk is flexible, hardware-walk is faster.
2. **Q: What is copy-on-write at the page level?** A: `fork()` marks both processes' pages read-only and shared; the first write triggers a fault that copies the page privately. (Detailed in Part 07 Section 03.)
3. **Q: How do huge pages help?** A: A 2 MB page replaces 512 × 4 KB PTEs with one PTE and one TLB entry → fewer walks, fewer misses; Linux THP/hugetlbfs expose this.
4. **Q: What happens to page tables when a process forks?** A: The kernel clones the page-table structures (COW), so the child's tables are a private copy pointing at the same frames; first write by either process copies the page.

## 15. Coding Example
```c
// Simulated paging translation: page table + present-bit handling
#include <stdio.h>
#include <stdint.h>

#define PAGE_SHIFT 12
#define PAGE_SIZE  (1u << PAGE_SHIFT)

typedef struct {
    uint32_t present : 1;
    uint32_t rw      : 1;
    uint32_t frame   : 30;
} PTE;                       // 32-bit PTE (single-level, 32-bit addr)

PTE table[1 << 20];

int translate(uint32_t logical, uint32_t *phys) {
    uint32_t page  = logical >> PAGE_SHIFT;
    uint32_t offset = logical & (PAGE_SIZE - 1);
    PTE e = table[page];
    if (!e.present) return -1;                 // page fault
    *phys = (e.frame << PAGE_SHIFT) | offset;
    return 0;
}

int main(void) {
    table[2] = (PTE){ .present = 1, .rw = 1, .frame = 12 };
    uint32_t phys;
    if (translate(0x2A1C, &phys) == 0) printf("0x2A1C -> 0x%x\n", phys); // 0xCA1C
    if (translate(0x3000, &phys) != 0) printf("0x3000 -> page fault\n");  // page 3 not present
    return 0;
}
```

## 16. Industry Usage
- **Linux**: `arch/x86/include/asm/pgtable.h`, `mm/memory.c` (`handle_mm_fault`), THP in `mm/huge_memory.c`, hugetlbfs; `x86_64/mm.rst` documents the 4-level layout.
- **Windows**: 2-level for x86, 4-level for x64; large pages via `MEM_LARGE_PAGES`.
- **macOS/XNU**: 4 KB + 2 MB + 1 GB pages; `pmap`/`vm_map` structures.
- **Hypervisors**: KVM/Hyper-V use EPT/NPT — a second page table walked by hardware for guest→host translation.
- **Cloud**: AWS Nitro / QEMU use huge pages for VM performance; JVM `-XX:+UseLargePages`.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 8.5 "Paging".
- Tanenbaum, *Modern Operating Systems (4th ed.)*, Ch. 3.4 "Memory Management with Paging".
- Intel SDM Vol. 3A, Ch. 4 "Paging".
- Linux source: `mm/memory.c`, `arch/x86/include/asm/pgtable_types.h`.
- `man 5 proc` (`/proc/<pid>/pagemap`, `pagemap` PFN bit 63 present flag).

## 18. Cheat Sheet
- Pages (virtual) = frames (physical) = 4 KB; offset passes through unchanged.
- Address split: `page | offset`; translation: `frame | offset`.
- PTE = frame + present/rw/user/accessed/dirty/NX.
- Present=0 or permission violation ⇒ #PF ⇒ demand-load or SIGSEGV.
- Paging ⇒ no external fragmentation; internal ≤ page−1 per mapping.
- Page table = array indexed by page number; multilevel to stay small.
- Flat 32-bit table = 4 MB; x86-64 needs 4 levels (Section 03/04).
- Sharing = two PTEs pointing to one frame.

## 19. Quiz
1. Under 4 KB paging, address 0x2A1C has page ___, offset ___:
   a) 2, 0x1C b) 2, 0xA1C c) 0x2A, 0x1C d) 0xA1C, 2 → **b**
2. Paging eliminates:
   a) internal fragmentation b) external fragmentation c) TLB misses d) page faults → **b**
3. The offset is not translated because:
   a) it's unused b) page and frame sizes are equal c) the TLB caches it d) it's zero → **b**
4. A missing PTE causes:
   a) TLB miss only b) page fault c) deadlock d) swap-out → **b**
5. Two processes share a library by:
   a) copying frames b) pointing two PTEs at one frame c) using one page table d) static linking → **b**
6. Worst internal fragmentation of one 4 KB-page mapping is:
   a) 4 KB b) 4 KB − 1 c) 8 KB d) 0 → **b**

## 20. Flashcards
- **Q: What is paging?** → **A:** Equal-size pages/frames mapped via a page table; kills external fragmentation.
- **Q: How is a virtual address translated?** → **A:** `frame = PT[page]; phys = (frame<<12)|offset`.
- **Q: What's in a PTE?** → **A:** Frame number + present/rw/user/accessed/dirty/NX bits.
- **Q: What raises a page fault?** → **A:** present=0 or permission violation on a page-table entry.
- **Q: Why does paging only have internal fragmentation?** → **A:** Fixed units fit anywhere; only the last page of a mapping is under-filled (≤4 KB−1).
- **Q: How is sharing done?** → **A:** Two PTEs in different tables pointing at the same frame.

## 21. Revision
Paging turns memory management into fixed-size bookkeeping: 4 KB pages map to 4 KB frames via a page table; the address is `page|offset` → `frame|offset`, with the offset unchanged. External fragmentation disappears (any page fits any frame), per-page protection and sharing become natural, and virtual memory becomes possible. The costs are internal fragmentation (≤4 KB−1 per mapping), page-table memory, and TLB pressure — each addressed by multilevel tables and huge pages (Sections 02–04).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is paging and why?" | 1 Why / 7 Formal |
| "Translate this address." | 8 Example / 15 Coding |
| "What does a PTE contain?" | 9 Internal / 13 Q4 |
| "Why no external fragmentation?" | 11/13 Q6 |
| "What happens on a page fault?" | 9 Internal / 13 Q5 |
| "How do processes share memory?" | 13 Q7 / 9 Internal |
| "Cost of a flat page table?" | 10 Time / 13 Q9 |
