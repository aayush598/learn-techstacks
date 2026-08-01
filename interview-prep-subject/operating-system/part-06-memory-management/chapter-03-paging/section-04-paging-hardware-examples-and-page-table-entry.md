# Paging Hardware Examples and Page Table Entry

> **TL;DR**: This section dissects the real x86-64 **page-table entry (PTE)** bit by bit and shows the exact hardware walk — the `present/rw/user/accessed/dirty/NX` bits, the PFN, CR3/PCID mechanics, and how Linux programs them — so you can answer any "read this PTE" or "how does a walk work" question cold.

## 1. Why Does This Exist?
Textbook paging shows abstract `page_table[page].frame`. Production systems need the *actual* hardware contract: which bits mean what, where the PFN lives, and how the CPU behaves on each condition. This exists because every interview about paging eventually becomes a question about real PTEs and the walk — and because real bugs (stale PTEs, missing NX, wrong user bit) come from misreading these bits. Knowing the x86-64 PTE layout and the walk makes you dangerous on any low-level team.

## 2. How Does It Work?
The x86-64 **4-level walk** consumes a 48-bit virtual address:
- `CR3` → base of **PML4** (page-map level-4).
- Bits 47:39 → index PML4E (8 bytes each).
- Bits 38:30 → index **PDPTE**.
- Bits 29:21 → index **PDE**.
- Bits 20:12 → index **PTE**.
- Bits 11:0 → physical offset.
- Large pages: PDE `PS=1` → 2 MB (bits 20:21 map frame, offset = bits 20:0); PUD `PS=1` → 1 GB.

Each level entry is 8 bytes. The **PTE** (4 KB page) layout (canonical bit positions, x86-64):
```
63   62  61 ... 52  51     32   31                   13  12  11   9   8   7   6   5   4   3   2   1   0
NX   —   —      PAT/…  reserved…  PFN(physical frame)    PAT soft A  D  A  PCD PWT U/S R/W P
(bit63: no-execute; bit5: accessed; bit6: dirty; bit2: user; bit1: rw; bit0: present)
```
Key bits: **0=Present**, **1=R/W**, **2=U/S**, **5=Accessed**, **6=Dirty**, **7=PAT**, **63=NX**, plus reserved bits that must be zero (a violation → #PF with reserved-bit error code).

## 3. When Is It Used?
- **Every instruction fetch & data access** on x86-64 Linux/Windows — the walk is the address path.
- **Kernel uses it too**: user/kernel split at bit 47 (`_PAGE_BIT_NX` on the top-half). The kernel half is mapped in every process's tables (global, PCID-aware).
- **Security**: NX + W^X, and the `user` bit prevent ring-0 code from being addressable by ring-3.
- **Diagnostics**: `pagemap`, `mincore`, `pagemap`-based tools read PTE state from `/proc/<pid>/pagemap`.

## 4. Why Wasn't Another Approach Chosen?
- **Segment-based protection only**: x86-16/32 had segment descriptors; x86-64 removed segmentation from the canonical path — paging became the sole translation mechanism (fewer moving parts, one walk).
- **Different PTE formats**: ARM64 differs (10-bit ASID, contiguous hints, hardware access/dirty optional); but the *concepts* are identical — bits for present/permissions/dirty/accessed, plus PFN. x86-64 is the interview default because it's ubiquitous.
- **OS-updated accessed/dirty vs hardware**: some CPUs let the OS manage them (software) to save writes; x86 hardware sets them, Linux periodically clears/uses them.
- **Single-level / software walk**: rejected for speed (Section 03) — hardware walk with caching won.

## 5. Intuition
The PTE is a tiny spec sheet for one 4 KB page: "Does this page exist? (present) Can it be written? (rw) Can users touch it? (user) Has it been read lately? (accessed) Written? (dirty) Can it be executed? (NX)." The walk is the MMU reading four nested index cards (PML4→PDPT→PD→PT) to find that spec sheet, then combining the frame number from it with the offset to produce the physical address.

## 6. Real-World Analogy
An apartment building directory: floor index (PML4) → wing index (PDPT) → corridor index (PD) → apartment door (PT). The door's nameplate (PTE) tells you the room's real location (PFN) and its rules: "visitors may ring only (user), no deliveries between 10pm (NX), front desk tracks when anyone visits (accessed) and when packages are left (dirty)." The walk is the doorman tracing the path floor→wing→corridor→door every time you visit a new door.

## 7. Formal Definition
A **page-table entry (PTE)** is a machine word that maps one virtual page to one physical frame: it encodes the **physical frame number (PFN)** in its upper address bits and a set of control bits, canonically **present (P)**, **read/write (R/W)**, **user/supervisor (U/S)**, **page-level writethrough (PWT)**, **page-level cache disable (PCD)**, **accessed (A)**, **dirty (D)**, **page attribute table (PAT)**, **global (G)**, and **no-execute (NX)**. A **page-table walk** is the sequence of memory reads, rooted at CR3 (PML4), used by the MMU to locate the PTE for a virtual address on a TLB miss.

## 8. Example
Two PTEs (physical frames given in decimal):
- `PTE_A = 0x8000000000007005`:
  - NX=1 (bit63) → non-executable (data page).
  - PFN = bits 51:12 = 0x700 → frame 0x700 (1792).
  - bits 2,1,0 set (U/S, R/W, P) → user, writable, present. A=0, D=0 → never touched.
- `PTE_B = 0x0000000000002011`:
  - NX=0 → executable. PFN = 0x2 → frame 2.
  - bits 4,0 set (PCD?, present) → present, cache-disabled. Not user, not writable → supervisor-only, read-only.

A user-mode `LOAD [0x1234]` with page = 0x1 (PTE_B): user bit clear → **#PF (protection violation)** — user can't access supervisor page.
`LOAD [0x7005...]` with NX page: allowed (data). `CALL 0x7005...`: NX set → #PF (can't execute).

## 9. Internal Working
1. **Access**: TLB miss → walker reads CR3.
2. **Level 1 (PML4)**: `addr1 = CR3 + idx1*8`; load; check present; check reserved bits; if `!present` → #PF (page-not-present) unless the error code says otherwise.
3. **Level 2 (PDPT)**: `addr2 = pml4e.pfn<<12 + idx2*8`; check present; if `PS=1` here → 1 GB page.
4. **Level 3 (PD)**: similar; `PS=1` → 2 MB page.
5. **Level 4 (PT)**: load PTE; check present + rw/user against the access's error code; read PFN; set Accessed (and Dirty for writes) — hardware or OS.
6. **Result**: `phys = (pte.pfn << 12) | offset`; insert into TLB; retry instruction.
7. **Kernel bookkeeping**: Linux marks PTEs via `set_pte`/`pte_modify`; the accessed bit drives the LRU/clock page-replacement heuristics (Part 07 Ch 02), and the dirty bit drives writeback. `mprotect` toggles rw/user; `mmap(MAP_SHARED)` uses `_PAGE_SOFT_DIRTY` in unused software bits.

## 10. Time Complexity
- TLB-hit translation: O(1) (~1 cycle).
- Hardware walk: O(4) memory reads (with page-walk caches usually 1–2 loads); each read ~4–15 ns.
- Per PTE changes: O(1) (`invlpg`) — but multi-page operations batch (`flush_tlb_range`).
- Linux building/tearing tables: O(pages touched) for `munmap` (page-by-page PTE zeroing + shootdowns).
- `fork()` cloning page tables: O(PTE count), historically the fork cost; mitigated by COW + lazy `mm` cloning.

## 11. Advantages
- **One uniform mechanism** (paging) for protection + translation on x86-64 (no segments to reconcile).
- **Fine-grained control**: rw/user/NX per page → strong W^X and ASLR-friendly layouts.
- **Hardware-managed accessed/dirty** remove per-access OS writes.
- **Large pages** (2 MB/1 GB) shrink walks and TLB pressure.
- Well-documented, stable ABI (Intel SDM Vol 3A) — the interview-standard model.

## 12. Disadvantages
- 8-byte entries × 4 levels = expensive walk without caches.
- Reserved-bit strictness: any stray bit causes #PF — table layout is rigid.
- PCID/global-bit interactions complicate flushing.
- Nested virtualization: guest walks + host walks = up to 8 levels of reads (mitigated by EPT TLB).
- Linux's software view (`pmd/pud/...`) is a config-dependent alias of hardware — can confuse.

## 13. Interview Questions
1. **Q: Lay out the x86-64 PTE bits.** A: bit0 Present, bit1 R/W, bit2 U/S, bit3 PWT, bit4 PCD, bit5 Accessed, bit6 Dirty, bit7 PAT, bit8 Global, bits 11:9 ignored/software, bits 51:12 PFN, bits 62:52 (reserved/PAT/keys), bit63 NX.
2. **Q: How does the CPU know where the page table is?** A: CR3 holds the physical base of PML4; on context switch the kernel loads the new process's CR3 (or uses PCID-tagged entries to avoid a full flush).
3. **Q: What error does a reserved bit cause?** A: A #PF with error code indicating "reserved bit violation" — the CPU validates reserved bits during the walk and faults before translation completes.
4. **Q: Walk me through translating 0x00007F00_00001234 (48-bit).** A: idx1=(VA>>39)&0x1FF, idx2=(VA>>30)&0x1FF, idx3=(VA>>21)&0x1FF, idx4=(VA>>12)&0x1FF; walk CR3→PML4→PDPT→PD→PT; phys=(PFN<<12)|0x234.
5. **Q: What happens on a write to a read-only page?** A: The R/W bit is clear → the walk's permission check fails → #PF with protection error → kernel either makes it writable (COW: copy-on-write) or SIGSEGVs (writing to `.text`).
6. **Q: How do accessed and dirty bits get set?** A: The MMU sets them (hardware) on reads/writes to that page; the OS periodically scans/clears them for LRU/clock page replacement (Part 07 Ch 02) and writeback decisions. On ARM64 they're sometimes managed by the OS.
7. **Q: What is the NX bit and why does it exist?** A: No-Execute (bit 63) marks pages non-executable; combined with W^X it prevents injecting/executing shellcode in writable memory — the foundation of modern exploit mitigation.
8. **Q: How does the user/kernel split work at the PTE level? (Tricky)** A: x86-64 Linux maps the kernel in the *high half* (bit47=1 → above 0xFFFF800000000000) of *every* process's tables; those PTEs have U/S=0 (supervisor), so user accesses fault but the kernel can switch without reloading CR3.
9. **Q: What's the "global" (G) bit for?** A: Marks kernel/user-shared PTEs that survive TLB flushes on context switch (with PCID), so kernel mappings don't need re-walking constantly.
10. **Q: Why would you set PWT/PCD?** A: To control caching of MMIO and device memory — e.g., framebuffers and PCIe BARs use uncached/mem-mapped semantics; wrong bits cause bizarre data corruption.
11. **Q: How does the kernel protect itself from user `mprotect` tampering? (Production)** A: `mprotect` only affects the calling process's PTEs and cannot set U/S=0 (supervisor) from user mode; the kernel validates new bits against allowed combos (`can_change_prot`).
12. **Q: What happens to PTEs on fork?** A: Linux clones page-table *levels* (COW), sharing frames read-only; first write by either process triggers a fault that copies the page (Part 07 Sec 03).
13. **Q: How do you read the PFN of a page from userspace?** A: `pagemap` (`/proc/<pid>/pagemap`) exposes each PTE; bit 63 = present, bits 54:0 = PFN — root-only. Useful for debugging page placement/huge pages.
14. **Q: What's a "software" PTE bit and why do OSes use them? (Tricky)** A: x86 reserves some low bits (e.g., 11:9) or uses PAT-bit space for OS-defined meanings — Linux uses `_PAGE_SOFT_DIRTY` and `_PAGE_SPECIAL` to track COW/file mappings without extra structure.

## 14. Follow-Up Questions
1. **Q: What's the difference between hardware-walk and software-loaded TLB on ARM64?** A: ARM64 has hardware-walk but also explicit `TLBI` maintenance; MIPS relied on software TLB fill. Either way, the PTE semantics (present/permissions/dirty) are similar.
2. **Q: How does PAT vs PCD/PWT work?** A: PAT is an extended cache-policy mechanism (a small table indexed by the PAT bit + PCD + PWT) giving more memory types than PCD/PWT alone.
3. **Q: What's the MKTME/memory-encryption bit?** A: Newer Intel PTEs can encode encryption keys (TME/MKTME); the concept: PFN + policy + encryption key all live in the same 8 bytes.
4. **Q: How do 5-level tables change the PTE?** A: An extra level (PML5) eats bits 56:48; PTE layout unchanged; address space grows to 57 bits.

## 15. Coding Example
```c
// Print and decode x86-64 style PTE bits
#include <stdio.h>
#include <stdint.h>

void dump_pte(uint64_t pte) {
    printf("PTE 0x%016lx\n", pte);
    printf("  present=%d rw=%d user=%d pwt=%d pcd=%d accessed=%d dirty=%d pat=%d global=%d nx=%d\n",
        (int)(pte & 1), (int)((pte>>1)&1), (int)((pte>>2)&1), (int)((pte>>3)&1),
        (int)((pte>>4)&1), (int)((pte>>5)&1), (int)((pte>>6)&1), (int)((pte>>7)&1),
        (int)((pte>>8)&1), (int)((pte>>63)&1));
    printf("  PFN=0x%lx (frame %lu)\n", (pte >> 12) & 0xFFFFFFFFF, (pte >> 12) & 0xFFFFFFFFF);
}

int main(void) {
    dump_pte(0x8000000000007005ULL);   // NX, PFN 0x700, user+rw+present
    dump_pte(0x0000000000002011ULL);   // supervisor, exec, present, pcd
    return 0;
}
```

## 16. Industry Usage
- **Linux**: `arch/x86/include/asm/pgtable_types.h` (`_PAGE_PRESENT`, `_PAGE_RW`, ...), `mm/pgtable-generic.c`, `mm/memory.c` (`do_wp_page` for COW), `mm/rmap.c`.
- **Windows**: `ntoskrnl`/`mm` PTE macros (`PTE_BASE`, `MI_PTE`), huge-page pools for SQL Server.
- **KVM/QEMU**: programs guest PTEs under EPT; `kvm_mmu` caches shadow/nested tables.
- **Browsers/security**: Chrome's V8 uses `mprotect(PROT_NONE)` (present=0 trick) to trap JIT regions — "guard page" pattern from PTE semantics.
- **Databases**: Postgres recommends `huge_pages=try`; the PTE for a 2 MB page is a single entry.

## 17. References
- Intel SDM Vol. 3A, Ch. 4.3 "Details of the 4-level Paging", Table 4-11 (PTE fields).
- AMD64 Architecture Programmer's Manual, Vol. 2, Ch. 5.
- Silberschatz, *OS Concepts (10th ed.)*, Ch. 8.5.2 "Implementation of Page Tables".
- Linux source: `arch/x86/include/asm/pgtable_types.h`, `arch/x86/include/asm/pgtable.h`, `mm/memory.c`.
- ARMv8-A Reference Manual, Ch. D5 "The AArch64 Virtual Memory System Architecture".

## 18. Cheat Sheet
- PTE (x86-64): P=0, RW=1, US=2, PWT=3, PCD=4, A=5, D=6, PAT=7, G=8, PFN=51:12, NX=63.
- Walk: CR3→PML4(47:39)→PDPT(38:30)→PD(29:21)→PT(20:12)+offset(11:0).
- PS=1 in PDE → 2 MB; in PUD → 1 GB (skip lower levels).
- Reserved bit violation → #PF (error code marks it).
- User accesses supervisor (U/S=0) pages → #PF.
- W^X: writable pages set NX; prevents shellcode execution.
- Accessed/Dirty set by hardware; drive LRU + writeback.
- Kernel mapped high-half in every process's tables, U/S=0.
- Linux software bits: `_PAGE_SOFT_DIRTY`, `_PAGE_SPECIAL`.

## 19. Quiz
1. Which PTE bit makes a page non-executable?
   a) bit 5 b) bit 6 c) bit 63 d) bit 0 → **c**
2. The PFN occupies bits:
   a) 63:52 b) 51:12 c) 11:0 d) 47:39 → **b**
3. A user-mode write to a supervisor read-only page causes:
   a) TLB hit b) #PF protection violation c) dirty-bit set d) no-op → **b**
4. In a PDE, PS=1 maps:
   a) 4 KB b) 2 MB c) 1 GB d) 512 B → **b**
5. Which bits are set by hardware during a walk?
   a) present, rw b) accessed, dirty c) user, nx d) PAT, PCD → **b**
6. The kernel half of a 48-bit address has bit 47:
   a) 0 b) 1 c) undefined d) toggled → **b**

## 20. Flashcards
- **Q: PTE present/RW/US/A/D/NX bit numbers?** → **A:** 0/1/2/5/6/63.
- **Q: How does the walk proceed?** → **A:** CR3→PML4(47:39)→PDPT(38:30)→PD(29:21)→PT(20:12), +offset(11:0).
- **Q: What does a reserved-bit violation do?** → **A:** #PF with a reserved-bit error code.
- **Q: How is COW implemented at the PTE level?** → **A:** fork marks frames read-only/shared; write → #PF → `do_wp_page` copies page, sets RW.
- **Q: Why is the kernel mapped into every process?** → **A:** High-half, U/S=0 → user can't touch it, and no CR3 reload on syscalls.
- **Q: What are accessed/dirty for?** → **A:** LRU/clock replacement and writeback decisions (Part 07).

## 21. Revision
The x86-64 PTE is an 8-byte contract: bit0 present, bit1 rw, bit2 user, bit5 accessed, bit6 dirty, bit7 PAT, bit8 global, bits 51:12 the physical frame number, bit63 NX. Translation walks CR3→PML4→PDPT→PD→PT using 9-bit indices (48-bit VA), folding in the 12-bit offset; PS=1 skips a level for 2 MB/1 GB pages. Hardware validates reserved bits and permissions during the walk, raising #PF on violations — the mechanism behind COW (write to shared read-only page), W^X (NX on writable pages), and the user/kernel split (kernel PTEs are supervisor, high-half). Accessed/dirty bits power page-replacement and writeback heuristics in Part 07.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Lay out the x86-64 PTE bits." | 2 How / 13 Q1 |
| "Walk me through a translation." | 8 Example / 13 Q4 |
| "How does COW work at the PTE level?" | 13 Q5 / 14 Q1 |
| "What does NX enable?" | 13 Q7 / 2 How |
| "Why can't user processes read kernel memory?" | 13 Q8 / 18 Cheat Sheet |
| "What drives page replacement?" | 13 Q6 / 9 Internal |
| "How does fork clone page tables?" | 13 Q12 / 9 Internal |
