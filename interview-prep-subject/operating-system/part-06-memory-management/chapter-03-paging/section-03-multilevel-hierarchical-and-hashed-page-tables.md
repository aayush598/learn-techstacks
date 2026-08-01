# Multilevel, Hierarchical and Hashed Page Tables

> **TL;DR**: A flat page table for a 64-bit address space would need 2⁵² entries per process, so real systems use **multilevel (hierarchical) tables** — allocating only the levels actually used — with **hashed** and **inverted** variants for special cases, trading a few extra memory accesses per walk for enormous memory savings.

## 1. Why Does This Exist?
A flat page table has one entry per page of the *entire address space*: on 32-bit that's 2²⁰ entries × 4 B = 4 MB per process; on 64-bit it's 2⁵² entries — completely impossible. Yet a process uses only a tiny fraction of its address space. Multilevel page tables exist to make page-table memory **proportional to usage, not to the address-space size**: allocate the top level, then only the subtables that correspond to actually-mapped regions. Hashed and inverted tables exist for the other extreme — very large sparse address spaces (inverted tables: one entry per physical frame, not per virtual page).

## 2. How Does It Work?
**Multilevel (hierarchical):** split the page number into several indices, each indexing a level:
- x86-64: 48-bit VA split into PML4 (9 bits) → PDPT (9) → PD (9) → PT (9) + 12-bit offset. CR3 → PML4 → ... → PTE.
- Each level holds 2⁹ = 512 entries × 8 B = 4 KB (one page — self-aligned).
- Unused upper entries point to "not present" — no subtable allocated → memory only for used regions.

**Hashed:** a hash table keyed by virtual page number; each bucket holds `(VPN, frame, chain)` — compact for sparse 64-bit spaces, but collisions chain and lookups are slower.

**Inverted:** a single table with one entry *per physical frame* in the whole system, storing `(pid, vpn) → frame`. Fixed-size (memory ∝ physical RAM), but lookup is a hash/scan over all frames — good for 64-bit spaces where page tables would explode.

## 3. When Is It Used?
- **Multilevel**: every mainstream 64-bit OS (Linux, Windows, macOS on x86-64/ARM64; ARM64 uses 4 KB pages with 4 levels or 64 KB pages with 2 levels).
- **Hashed**: some older 64-bit RISC designs (MIPS R4000-style, early Alpha used hashed inverted tables); still seen in SPARC/PA-RISC and in some MMU research designs.
- **Inverted**: IBM POWER/RS/6000, early PowerPC, MIPS, and PA-RISC used inverted/hashed tables; on 64-bit with huge address spaces and (historically) small RAM, it bounded table size.
- **5-level (LA57)**: x86-64 with 57-bit VAs adds a 5th level for >128 TB virtual spaces (databases with huge memory-mapped files).

## 4. Why Wasn't Another Approach Chosen?
- **Flat table**: 4 MB per process (32-bit), impossible on 64-bit → rejected for scale.
- **Two-level with equal splits**: works on 32-bit (page directory + page table = 4 MB max but often < 4 KB used) — the classic 386 design; on 64-bit it needs more levels because 48-bit space / 9 bits per level = 5+ levels (x86-64 uses 4: 48 bits → 4×9 + 12).
- **Segmented tables (Intel x86-32)**: Paging + segmentation overlay added complexity without benefit on 64-bit; x86-64 dropped segments for paging (Chapter 04).
- **Inverted table as the general solution**: bounded memory, but every lookup is a hash search — slow, needs special TLB-fill hardware/software; modern CPUs prefer multilevel because hardware walks are fast and 4 levels is affordable.
- **Radix tree of page tables (Linux)**: Linux stores page-table roots in `struct mm_struct` and uses a radix-tree-like `pgd/p4d/pud/pmd/pte` split, allowing lazy allocation and clean `mmap` semantics.

## 5. Intuition
A huge library uses a **card catalog in tiers**: a top drawer of index cards points to second-drawer cards, which point to the actual book. You only print index cards for subjects the library actually has. That's a multilevel table: create a second-level card *only when the first book under that subject is added*. An **inverted table** is the opposite: instead of a card per *book* (per virtual page), the library keeps a card per *shelf slot* (physical frame) saying which book is in it — fixed size, but finding a book requires searching the shelves.

## 6. Real-World Analogy
City streets vs. a phone directory: a flat table is a directory with an entry for every possible address (most unused — huge waste). A multilevel table is organized like a hierarchical directory: street → block → building → apartment. You only print the blocks that have buildings. An inverted table is like a hotel with one guest log per *room* (frame), not per *possible guest*: you always know who's in each room, but finding "which room is Mr. X in?" needs a search.

## 7. Formal Definition
A **multilevel (hierarchical) page table** divides the virtual page number into L indices, each selecting an entry in a level of the table; a translation walks from the root (pointed to by the page-table base register, e.g., CR3) through L levels to reach the PTE. A **hashed page table** uses a hash function on the virtual page number to index a bucket of entries, each containing the full VPN and its frame. An **inverted page table** has one entry per physical frame, storing the (process ID, virtual page number) that currently maps it, and is searched (via hashing) to translate an address.

## 8. Example
x86-64 translation of VA `0x0000_7F00_0000_1000` (48-bit):
- Offset = bits 11:0 = 0x000.
- VPN parts: PML4 index = bits 47:39 = 0x0; PDPT = 0x7F? (say 0x0), PD = 0x0, PT = 0x1.
- Walk: `CR3 → PML4[0] → PDPT[0] → PD[0] → PT[1] → PTE.frame`.
- Only 1 of 512 PDPT entries used (the user-space region) → 4 KB for PDPT+PD+PT instead of 512 × 4 KB.

**Memory comparison**: flat 48-bit table = 2³⁶ × 8 B = 512 GB (impossible). Multilevel = 4 KB (PML4) + 4 KB (PDPT) + 4 KB (PD) + 4 KB (PT) = 16 KB for one mapped region — 32 million × smaller.

**Inverted example**: system with 1 GB RAM = 262,144 frames → inverted table = 262,144 × ~16 B ≈ 4 MB *total for the entire machine*, independent of how many processes or how sparse.

## 9. Internal Working
1. **Walk (x86-64, 4-level)**:
   - `index1 = (VA >> 39) & 0x1FF; e1 = *(CR3 + index1*8);` if !present → #PF.
   - `index2 = (VA >> 30) & 0x1FF; e2 = *(e1.paddr + index2*8);` ...
   - `index3 = (VA >> 21) & 0x1FF; e3 = ...`
   - `index4 = (VA >> 12) & 0x1FF; pte = ...`
   - `phys = (pte.pfn << 12) | (VA & 0xFFF)`.
2. **Allocation on fault**: when a page is touched, `handle_mm_fault` walks and *allocates missing middle levels* (`pgd_alloc`/`p4d_alloc`/`pud_alloc`/`pmd_alloc`/`pte_alloc_map`), so the table grows lazily.
3. **Large pages**: a PDE (or PUD) entry with `PS=1` maps 2 MB (or 1 GB) directly, skipping lower levels — one walk level saved and one PTE.
4. **Hashed table**: `h = hash(vpn)`, probe bucket chain; on miss, allocate a new chain entry or wrap (MIPS used software fill).
5. **Inverted table**: `hash(pid, vpn) → frame`; hardware/software searches the bucket; on miss → page fault.

## 10. Time Complexity
- Multilevel walk: **O(L)** — L=4 (x86-64), L=5 (LA57), L=2 (ARM64 64 KB pages). With TLB hit: O(1).
- Page-table memory: **O(used virtual space / level)**, i.e., O(4 KB per top-level entry touched) — not O(address space).
- Hashed lookup: O(1) average, O(bucket chain length) worst.
- Inverted lookup: O(1) average via hash, O(frames) worst — table size O(physical RAM).
- `mmap` of a huge sparse file: O(number of mappings), no page-table preallocation.

## 11. Advantages
- **Memory proportional to usage** — sparse 64-bit spaces cost little.
- **Lazy allocation** — table levels created only when pages are touched.
- **Large pages** — 2 MB/1 GB reduce levels and TLB pressure.
- **Per-process root** (CR3) makes context switching cheap (just reload root).
- Inverted tables: bounded, global size independent of process count.

## 12. Disadvantages
- Extra memory access per level on a walk (mitigated by TLB + page-walk caches).
- Complexity: nested allocation, fragmentation of table pages, fault handling at each level.
- Inverted tables: slow, collision-prone lookups; no natural way to iterate a process's mappings.
- Hashed tables: chain overhead, non-deterministic lookup.
- Deep hierarchies (5 levels) add latency even with caches.

## 13. Interview Questions
1. **Q: Why can't we use a flat page table on 64-bit?** A: 2⁵² entries × 8 B = 2⁵⁵ bytes per process — impossible. Multilevel tables allocate only used levels.
2. **Q: How does a 4-level x86-64 table split a 48-bit address?** A: PML4(9) | PDPT(9) | PD(9) | PT(9) | offset(12) = 48 bits; CR3 points to PML4; each level is 512×8 B = 4 KB.
3. **Q: How much memory does one mapped 4 KB page cost in table overhead?** A: Up to 4 levels × 4 KB = 16 KB worst-case when all upper levels are new, but amortized: one PML4/PDPT/PD level covers 512 pages, so per-page overhead falls fast as a region fills.
4. **Q: What happens on a fault through a missing middle level?** A: The kernel walks `mm->pgd` and allocates the missing `p4d/pud/pmd/pte` page (zero-filled), then inserts the PTE — lazy table growth.
5. **Q: What is an inverted page table and its trade-off? (Tricky)** A: One entry per physical frame storing (pid, vpn); memory ∝ RAM not address space, but lookup is a hash search and you can't easily enumerate a process's pages. Used on POWER/MIPS/PA-RISC.
6. **Q: What is a hashed page table?** A: Hash table keyed by VPN with chaining; compact for sparse spaces but slower lookups and collision chains; historically used on some 64-bit RISC CPUs.
7. **Q: When would 5-level paging help? (Production)** A: 57-bit virtual spaces (>128 TB) — for databases/DBMS mapping enormous files, avoiding table overflow at 128 TB; Linux `CONFIG_X86_5LEVEL`.
8. **Q: How do large (huge) pages reduce the walk?** A: A PDE with PS=1 maps 2 MB directly (skips PT level) — one fewer level to walk and one fewer TLB entry needed. A PUD with PS=1 maps 1 GB.
9. **Q: How is the page table freed when a process exits?** A: The kernel tears down each level (`pgd_free` → `pud_free` → `pmd_free` → `pte_free`), returning pages to the buddy allocator; Linux does this in `exit_mmap`.
10. **Q: Why is a "present" check needed at each level? (Scenario)** A: An upper entry not present means the whole subtree is unmapped — the walk must fault *at that level* so the kernel can allocate it lazily (or SIGSEGV).
11. **Q: How does Linux organize its 4 levels?** A: `pgd/p4d/pud/pmd/pte` — a configurable 4-or-5-level hierarchy (5 on LA57); the mmap/VMA layer drives which ranges get table levels.
12. **Q: What's the memory overhead of page tables in practice?** A: Roughly 4 KB per 512 pages mapped at steady state plus top-level tables; a 1 GB process with 4 KB pages ≈ 2 MB of tables (0.2%) — negligible vs the flat-table explosion it replaces.
13. **Q: Can two processes share page-table *levels*?** A: Yes, in specialized cases (e.g., `clone(CLONE_VM)` shares `mm`, or KSM/transparent huge pages share frames, and hypervisor EPTs share host-level tables) — but each process normally owns its tables for isolation.

## 14. Follow-Up Questions
1. **Q: How do TLBs interact with multilevel tables?** A: The TLB caches the *result* of the walk, so deeper hierarchies only cost on misses; page-walk caches cache intermediate entries to make misses cheap.
2. **Q: What's the difference between a radix tree and a multilevel page table?** A: They're essentially the same idea; Linux's page tables are a fixed-depth radix/red-black tree with lazy nodes.
3. **Q: How do nested (EPT/NPT) tables add levels?** A: Each guest-virtual access can require walking guest tables *and* host tables — hardware caches this in a second TLB.
4. **Q: Why is a 2 MB huge page table only 3 levels?** A: The PD entry itself contains the frame (PS=1), so the PT level disappears — 3-level walk + offset (21 bits).

## 15. Coding Example
```c
// Simulate a 2-level page table (32-bit, 10+10+12) with lazy subtable allocation
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define DIR_ENTRIES 1024
#define TBL_ENTRIES 1024
#define PSHIFT 12

uint32_t *dir[DIR_ENTRIES];   // NULL => not allocated (lazy)

uint32_t *get_or_create_tbl(unsigned di) {
    if (!dir[di]) {
        dir[di] = calloc(TBL_ENTRIES, sizeof(uint32_t));
        printf("  allocated page-table level for dir index %u\n", di);
    }
    return dir[di];
}

int map(uint32_t vaddr, uint32_t frame) {
    unsigned di = vaddr >> 22, ti = (vaddr >> 12) & 0x3FF, off = vaddr & 0xFFF;
    get_or_create_tbl(di)[ti] = frame;       // store PFN (present implied)
    return off;
}

uint32_t translate(uint32_t vaddr, int *present) {
    unsigned di = vaddr >> 22, ti = (vaddr >> 12) & 0x3FF;
    if (!dir[di]) { *present = 0; return 0; } // fault: no table level
    uint32_t e = dir[di][ti];
    *present = e != 0;
    return (e << PSHIFT) | (vaddr & 0xFFF);
}

int main(void) {
    map(0x00400200, 7);                       // dir 1, tbl 0
    map(0x00C00ABC, 3);                       // dir 3, tbl 0
    int ok;
    printf("0x00400200 -> 0x%x\n", translate(0x00400200, &ok)); // 0x700200
    printf("0x0C000000 (never mapped): %s\n", ok ? "??" : "FAULT");
    (void)translate(0x0C000000, &ok);
    printf("  present=%d\n", ok);
    return 0;
}
```

## 16. Industry Usage
- **Linux on x86-64**: 4-level default; `CONFIG_X86_5LEVEL` for 5-level; THP uses PMD-level huge pages; hugetlbfs for explicit 2 MB/1 GB.
- **ARM64**: 4 KB/16 KB/64 KB pages with 4/2-level tables (ASID-tagged); stage-2 for VMs.
- **PowerPC**: multilevel with hashed inverted segments on older parts; modern uses 4 KB/64 KB/2 MB/1 GB.
- **Windows x64**: 4-level paging with PTE macros in `ntoskrnl`; large pages for SQL Server.
- **Databases**: Oracle/Postgres recommend huge pages; SAP uses 1 GB pages on POWER.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 8.5.4–8.5.5 "Hierarchical/Hashed/Inverted Page Tables".
- Intel SDM Vol. 3A, Ch. 4 "Paging" (4.3 "Details of the 4-level paging").
- Linux source: `arch/x86/include/asm/pgtable.h`, `arch/x86/include/asm/pgtable_64_types.h`, `mm/memory.c`.
- ARMv8-A Reference Manual, "Translation table formats".
- Tanenbaum, *Modern Operating Systems*, Ch. 3.4 (multilevel page tables).

## 18. Cheat Sheet
- Flat table = 2²⁰ entries (32-bit), impossible on 64-bit → multilevel.
- x86-64: PML4(9)|PDPT(9)|PD(9)|PT(9)|off(12); CR3 = root.
- Each level = 512×8 B = 4 KB; allocate levels lazily on fault.
- Inverted table: one entry per frame (pid,vpn); size ∝ RAM.
- Hashed table: hash(VPN) buckets with chains; compact for sparse spaces.
- Large pages: PDE PS=1 → 2 MB (skip PT), PUD PS=1 → 1 GB.
- 5-level (LA57) = 57-bit VAs; Linux CONFIG_X86_5LEVEL.
- Table overhead ∝ used virtual space, not address space.

## 19. Quiz
1. A flat 48-bit page table would have how many entries?
   a) 2³⁶ b) 2³⁷ c) 2⁵² d) 2⁴⁸ → **a**
2. On x86-64, how many bits select the PT level?
   a) 12 b) 9 c) 10 d) 21 → **b**
3. An inverted table's size is proportional to:
   a) virtual address space b) physical RAM c) process count d) TLB size → **b**
4. A PMD entry with PS=1 maps:
   a) 4 KB b) 2 MB c) 1 GB d) 512 KB → **b**
5. Missing middle levels are allocated:
   a) at boot b) lazily on page fault c) at fork d) never → **b**
6. 5-level paging provides how many virtual address bits?
   a) 48 b) 52 c) 57 d) 64 → **c**

## 20. Flashcards
- **Q: Why multilevel page tables?** → **A:** Flat tables explode on 64-bit; multilevel allocates only used levels, so memory ∝ usage.
- **Q: x86-64 level split?** → **A:** PML4(9)|PDPT(9)|PD(9)|PT(9)|offset(12).
- **Q: When are middle levels created?** → **A:** Lazily, when a page fault touches a new region.
- **Q: What is an inverted page table?** → **A:** One entry per physical frame (pid,vpn); bounded by RAM size.
- **Q: What is a hashed page table?** → **A:** VPN hash → bucket with chains; compact for sparse spaces.
- **Q: What do huge pages do to the walk?** → **A:** PS=1 skips lower levels (2 MB/1 GB), fewer TLB entries.
- **Q: What is 5-level paging?** → **A:** LA57, 57-bit VAs — for >128 TB address spaces.

## 21. Revision
Multilevel page tables make paging scale: the 48-bit x86-64 address splits into PML4|PDPT|PD|PT|offset (9 bits each, 4 KB per level, CR3 as root), and levels are allocated lazily, so table memory tracks *used* virtual space instead of the address-space size. Hashed tables (VPN hash + chains) and inverted tables (one entry per frame) trade lookup speed for bounded/compact size on very sparse or RAM-limited 64-bit designs. Huge pages skip levels (PS=1) and shrink the TLB footprint; 5-level paging (LA57) extends reach beyond 128 TB. The walk is hidden by the TLB, making all this nearly free on the hot path.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Why not a flat page table on 64-bit?" | 1 Why / 13 Q1 |
| "Walk me through an x86-64 translation." | 8 Example / 9 Internal |
| "What's an inverted page table?" | 13 Q5 / 2 How |
| "What's a hashed page table?" | 13 Q6 / 2 How |
| "When is 5-level paging useful?" | 13 Q7 / 4 Alternative |
| "How much do page tables cost in memory?" | 13 Q12 / 10 Time |
