# TLB (Translation Lookaside Buffer)

> **TL;DR**: The **TLB** is a tiny, extremely fast hardware cache inside the MMU that remembers recent page→frame translations so most memory accesses cost ~1 cycle instead of a 4-level page-table walk — making paging affordable.

## 1. Why Does This Exist?
A page-table lookup isn't free: on x86-64, a TLB miss forces a **4-level walk** — four dependent memory reads (PML4E, PDPTE, PDE, PTE) that can cost 30–80+ cycles *per memory access*. Since almost every instruction touches memory, doing a walk on every access would make paging several times slower than the CPU. The TLB exists to make translation nearly free by exploiting **temporal and spatial locality**: programs keep hitting the same handful of pages (the working set), so caching the last N translations makes the common case a single parallel compare.

## 2. How Does It Work?
The TLB is an associative cache: entries `(ASID/PCID, virtual page number) → (frame number, permissions)`. On each access:
1. The MMU compares the page number (and address-space tag) against all TLB entries in parallel (CAM).
2. **Hit**: get the frame + check permissions → emit physical address. ~1 cycle.
3. **Miss**: walk the page table (hardware on x86-64, software TLB-fill on MIPS/SPARC), insert the entry (evicting one, often LRU/random), then retry.
On a context switch, entries tagged with the old process are invalidated (or kept with PCID/ASID tags).

## 3. When Is It Used?
- **Every memory access on every paged CPU**: desktop, server, mobile, embedded (Cortex-A). 
- **Huge-page workloads** (DBs, VMs, JVMs): explicitly to increase TLB reach.
- **Hypervisors**: second-level TLBs (EPT/NPT) cached separately to speed guest translation.
- **I/O**: IOMMU TLBs cache device address translations for DMA.
- **Address-space tagging**: ASIDs/PCIDs avoid wholesale flushes on context switch.

## 4. Why Wasn't Another Approach Chosen?
- **No cache (walk every time)**: correct but unaffordable — 4 dependent loads per access.
- **Fully-associative software cache**: flexible but slow; hardware CAM is faster.
- **Bigger page tables instead (single-level)**: doesn't remove the walk cost; just removes one level.
- **Always use huge pages**: reduces entries needed but can't cover everything; 2 MB granularity wastes memory for fine-grained sharing.
- **Virtually-indexed/virtually-tagged caches**: could bypass translation for L1, but breaks coherence and requires ASID tags on every line — not worth it. Physically-tagged caches + TLB won.

## 5. Intuition
You're a librarian (MMU) who must find every book. Looking up the catalog (page table) takes 4 trips across the library (4-level walk). So you keep a small notepad by your desk (TLB) listing the last books you retrieved: "encyclopedia vol 5 → shelf 231." Most requests are for books you just fetched, so you glance at the notepad (1 second) instead of making 4 trips. The notepad has limited lines — when full, you erase an old entry (eviction).

## 6. Real-World Analogy
A receptionist with a rolodex of the 50 most-called extensions. Calling an extension you dial often is instant (hit). Dialing one not in the rolodex means walking to the company directory (page table) — slow. When the rolodex fills, the least-used card is removed. Now imagine every phone call (memory access) forced a directory lookup; the rolodex is the only reason the company functions at all.

## 7. Formal Definition
A **Translation Lookaside Buffer (TLB)** is a content-addressable (associative) cache in the memory-management unit that stores recent mappings from virtual page numbers to physical frame numbers, along with permission/access bits. On a virtual address lookup, the TLB is searched in parallel; a hit supplies the frame immediately, while a miss requires a page-table walk (hardware or software) after which the mapping is cached. Because it caches *translations* (not data), it must be invalidated when mappings change (unmap/mprotect/context switch), selectively via `invlpg` or wholesale via CR3 reload/PCID.

## 8. Example
TLB with 4 entries for process P (PCID 0):
| VPN | PFN | Perm |
|---|---|---|
| 0x0 | 0x7 | R-X |
| 0x1 | 0x4 | R-- |
| 0x2 | 0xC | RW- |
| 0x3 | 0x2 | R-- |

Access to `0x21A0` → VPN 0x2 → TLB **hit** → PFN 0xC → physical 0xCA1C. Cost: ~1 cycle.
Access to `0x4000` → VPN 0x4 → TLB **miss** → hardware walks 4 levels → finds page 4 unmapped → page fault. Cost: fault path (µs–ms if disk I/O).
Access to `0x3000` → VPN 0x3 → TLB hit → PFN 0x2 → 0x2A1C.
Now the OS calls `munmap(0x2000, 0x1000)`: it issues `invlpg` for VPN 0x2 (or flushes TLB) so stale frame 0xC can't be reused after the page is freed.

## 9. Internal Working
1. CPU emits logical address → MMU extracts VPN + offset.
2. TLB CAM compare: does an entry match `(PCID, VPN)` and satisfy permission?
3. **Hit** → physical address emitted; hardware may also update the accessed/dirty bits lazily.
4. **Miss** → the page-table walker (x86-64) reads CR3, fetches 4 levels, checks present/permissions:
   - If present → insert into TLB (evict victim), retry the access.
   - If not present → #PF to the kernel.
5. **Context switch** (Linux): writes CR3 → with PCID, the TLB keeps old-process entries tagged and only new process's entries are used (no flush); without PCID, the whole TLB is flushed.
6. **Invalidation**: `mprotect`/`munmap`/`mmap` change PTEs → kernel flushes affected entries (`invlpg`) to avoid stale translations (a stale TLB entry is a security/perf bug — stale frames may be reallocated).
7. **Thrash**: if the working set exceeds TLB capacity, every access misses → "TLB thrashing," mitigated by huge pages and better locality.

## 10. Time Complexity
- TLB hit: **O(1)** — single parallel CAM lookup (~1 cycle).
- TLB miss: **O(L)** hardware walk, L = 4 on x86-64 (plus memory latency); software-filled TLBs add kernel trap cost.
- Amortized access cost ≈ `hit% × 1 + miss% × walk_cost`.
- TLB invalidation: O(1) full flush; O(#entries) selective (`invlpg` per page).
- Working set > TLB capacity ⇒ effective miss rate spikes (TLB thrashing), dominated by walk cost.

## 11. Advantages
- Makes paging affordable: hot mappings cost ~1 cycle, not ~50.
- Small (typically 64–2,048 entries for 4 KB pages; larger for huge pages), cheap, high-speed.
- Handles permissions in hardware (rwx, NX) — no kernel call on the hot path.
- PCID/ASID support reduces context-switch cost.
- Second-level TLB (EPT/NPT) keeps virtualization fast.

## 12. Disadvantages
- **Limited capacity**: large working sets overflow it → thrashing.
- **Coherence burden**: software must invalidate on every mapping change; bugs cause stale-translation crashes.
- Context switches historically flushed it (now mitigated by PCID).
- Only caches *recent* translations — cold but large regions are always slow.
- Uses power/silicon; bigger TLBs are costly.

## 13. Interview Questions
1. **Q: What is the TLB?** A: A small hardware cache in the MMU that caches recent virtual-page→physical-frame mappings (plus permissions) so most accesses skip the page-table walk.
2. **Q: Why is a TLB needed at all?** A: A page-table walk on x86-64 is 4 dependent memory loads (~30-80+ cycles); with a TLB hit costing ~1 cycle, the cache amortizes translation to near-zero on programs with locality.
3. **Q: TLB hit vs miss — what happens?** A: Hit: frame + permission check → physical address, ~1 cycle. Miss: hardware walk (or software TLB-fill) → insert entry → retry; if PTE not present → page fault to kernel.
4. **Q: When must the TLB be invalidated? (Tricky)** A: Whenever mappings change: `munmap`, `mprotect` (permission change), page deallocation, context switch without PCID, and after the kernel maps new pages. Linux uses `invlpg`/flush-tlb ranges.
5. **Q: Why is a stale TLB entry dangerous?** A: The page may be freed and reallocated to another process; the stale entry maps the new owner's frame into the old process — a memory-safety/security bug. That's why unmaps always flush.
6. **Q: What is TLB thrashing and how do you fix it?** A: Working set > TLB capacity → misses dominate. Fixes: huge pages (2 MB/1 GB map more per entry), better data locality, PCID to avoid flushes, or workload redesign.
7. **Q: How do huge pages help the TLB specifically?** A: One 2 MB page = one TLB entry covering 512 × 4 KB pages → 512× more reach for the same TLB; databases/JVMs/cloud VMs use THP/hugetlbfs for exactly this.
8. **Q: What are PCIDs/ASIDs and what problem do they solve?** A: Process-Context Identifiers tag TLB entries with their owning process; on context switch the CPU keeps old entries and only matches new PCID, avoiding a full flush — faster switches.
9. **Q: Who invalidates the TLB — hardware or OS?** A: The OS, via privileged instructions (`invlpg`, full flush on CR3 write) because only the OS knows when mappings changed; the hardware merely obeys.
10. **Q: How does the x86-64 walk happen on a miss?** A: Hardware reads CR3 (PML4 base), indexes PML4E/PDPTE/PDE/PTE using address bits 47:39/38:30/29:21/20:12, checks present/permissions, and fills the TLB. No kernel involvement on the hit/miss path.
11. **Q: Can the TLB be a correctness issue in multiprocessing? (Production)** A: Yes — on some architectures the OS must broadcast TLB flushes to all CPUs (`tlb shootdown`) after unmap; Linux sends IPIs (flush_tlb_mm) when a page is unmapped while other CPUs may have it cached.
12. **Q: How does an IOMMU's TLB differ from the CPU's?** A: It caches *device* I/O address translations (DMA); the OS invalidates it via `iommu_unmap` paths, protecting DMA from stale mappings.
13. **Q: What's a "TLB reach"?** A: TLB size × page size = total addressable by cached entries, e.g., 1024 entries × 4 KB = 4 MB reach. Databases exceeding reach → misses.

## 14. Follow-Up Questions
1. **Q: What's the difference between fully-associative and set-associative TLBs?** A: Fully-associative searches all entries in parallel (flexible, power-hungry); set-associative hashes VPN to a set (cheaper, occasional conflicts). Most TLBs are set-associative.
2. **Q: How do superpages interact with the TLB?** A: TLB entries can match on larger sizes (2 MB/1 GB), so fewer entries cover the same region; MMU checks page size per entry.
3. **Q: What is a "page walk cache"?** A: Hardware caches for the upper levels of the walk (PML4E/PDPTE/PDE), so a miss costs ~1-2 loads, not 4.
4. **Q: Why does the kernel sometimes flush TLB on *all* CPUs?** A: Because page tables are shared across CPUs; on `munmap` every CPU that might hold the mapping must invalidate → IPI-based shootdown, an occasional scalability bottleneck.

## 15. Coding Example
```c
// Simulate a small set-associative TLB with LRU eviction
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define WAYS 4
#define SETS 8
typedef struct { uint32_t vpn; uint32_t pfn; uint8_t valid; uint8_t age; } TlbEntry;

static TlbEntry tlb[SETS][WAYS];
static uint32_t ticks = 0;

int tlb_lookup(uint32_t vpn, uint32_t *pfn) {
    unsigned set = vpn % SETS;
    int victim = 0;
    for (int w = 0; w < WAYS; w++) {
        if (tlb[set][w].valid && tlb[set][w].vpn == vpn) {
            tlb[set][w].age = ++ticks;
            *pfn = tlb[set][w].pfn;
            return 1;                       // hit
        }
        if (!tlb[set][w].valid) victim = w;
        else if (tlb[set][w].age < tlb[set][victim].age) victim = w; // LRU
    }
    tlb[set][victim] = (TlbEntry){ vpn, vpn * 4, 1, ++ticks }; // fill on miss
    return 0;
}

int main(void) {
    uint32_t pfn;
    printf("0x1: %s\n", tlb_lookup(1, &pfn) ? "hit" : "miss");
    printf("0x1: %s\n", tlb_lookup(1, &pfn) ? "hit" : "miss"); // now cached
    return 0;
}
```

## 16. Industry Usage
- **Intel**: 4-level walks, PCID, paging-structure caches, 1.5K+ TLB entries on recent CPUs for 4 KB + huge pages.
- **AMD**: NPT (nested page tables) with its own TLBs for VMs.
- **ARM64**: stage-1/stage-2 TLBs, ASIDs, and `TLBI` instructions; used in every Android/iOS SoC.
- **Linux**: `arch/x86/include/asm/tlbflush.h`, `mm/tlb.c`, PCID support (`CONFIG_PCID`), THP tuning.
- **Cloud/DB**: MySQL/Postgres/Cassandra recommend huge pages to reduce TLB misses; KVM recommends `-mem-path` huge pages.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 8.5.3 "Translation Lookaside Buffer".
- Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*, Ch. on virtual memory/TLB.
- Intel SDM Vol. 3A, Ch. 4.10 "Caching Translation Information".
- Linux source: `arch/x86/mm/tlb.c`, `arch/x86/include/asm/tlbflush.h`.
- ARMv8 Architecture Reference Manual, "TLB maintenance operations".

## 18. Cheat Sheet
- TLB = associative cache of VPN→PFN + permissions; hit ≈ 1 cycle.
- Miss = 4-level walk (x86-64) → insert → retry; absent PTE = page fault.
- Invalidate on: unmap, mprotect, page free, context switch (no PCID).
- PCID/ASID: tag entries per process → no full flush on switch.
- TLB reach = entries × page size; huge pages multiply reach.
- Thrashing = working set > TLB; fix with huge pages/locality.
- Multi-CPU unmaps need TLB shootdown (IPIs).
- IOMMU TLB caches device DMA translations.

## 19. Quiz
1. A TLB hit costs approximately:
   a) 50 cycles b) 1 cycle c) 100 cycles d) 0 cycles → **b**
2. An x86-64 TLB miss walks how many levels?
   a) 1 b) 2 c) 4 d) 6 → **c**
3. Which event requires TLB invalidation?
   a) TLB hit b) munmap c) TLB miss d) page fault → **b**
4. PCIDs let a context switch avoid:
   a) page faults b) TLB flushes c) cache flushes d) IPIs → **b**
5. A 1024-entry TLB with 4 KB pages has reach:
   a) 4 MB b) 1 MB c) 16 MB d) 4 GB → **a**
6. TLB thrashing happens when:
   a) TLB too big b) working set exceeds TLB capacity c) too few pages d) PCID missing → **b**

## 20. Flashcards
- **Q: What does the TLB cache?** → **A:** Recent VPN→PFN translations + permissions.
- **Q: Cost of a hit vs a miss?** → **A:** ~1 cycle vs a 4-level hardware walk (~tens of cycles).
- **Q: When must TLB be flushed?** → **A:** On unmap/mprotect/free and context switch without PCID.
- **Q: How do huge pages help the TLB?** → **A:** One entry covers 2 MB/1 GB instead of 4 KB.
- **Q: What are PCIDs/ASIDs for?** → **A:** Tag TLB entries per process, avoiding full flushes on context switch.
- **Q: What is a TLB shootdown?** → **A:** IPIs forcing all CPUs to invalidate stale mappings after an unmap.

## 21. Revision
The TLB is a small associative cache in the MMU mapping VPN→PFN with permissions. Hits cost ~1 cycle; misses trigger the x86-64 4-level hardware walk (or a software fill), and absent PTEs become page faults. The OS must invalidate TLB entries whenever mappings change (unmap/mprotect/free) — per-CPU with `invlpg`, or full flush on CR3/context switch unless PCIDs tag entries per process. TLB reach (entries × page size) dictates thrashing; huge pages, ASIDs, and page-walk caches keep translation cheap enough for paging to be the universal scheme.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the TLB and why is it needed?" | 1 Why / 7 Formal |
| "What happens on hit vs miss?" | 9 Internal / 13 Q3 |
| "When do you invalidate the TLB?" | 13 Q4-5 / 9 Internal |
| "What is TLB thrashing and fixes?" | 13 Q6-7 |
| "What are PCIDs/ASIDs?" | 13 Q8 / 2 How |
| "How do multi-core unmaps work?" | 13 Q11 / 14 Q4 |
| "What is TLB reach?" | 13 Q13 |
