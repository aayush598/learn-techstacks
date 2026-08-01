# Fragmentation and Compaction

> **TL;DR**: **Internal fragmentation** wastes space *inside* an allocated block (unusable by anyone); **external fragmentation** chops free RAM into holes too small to use; **compaction** fixes external fragmentation by shifting all processes together — an O(total memory) operation that is why modern OSes prefer paging.

## 1. Why Does This Exist?
Fragmentation is the unavoidable tax of memory allocation: because processes come and go at arbitrary sizes and times, the set of allocated blocks and free holes becomes messy. Understanding fragmentation matters because it directly decides *how much usable RAM a system really has* — a system can show 40% free yet fail to load a 20% process. Compaction exists as the brute-force remedy: periodically or on-demand, *move every process so all free memory is contiguous*, then a large hole appears. It's the last resort of the contiguous-allocation world and the precise reason that world was abandoned.

## 2. How Does It Work?
- **Internal fragmentation**: an allocated block is bigger than the request (e.g., fixed partition of 16 KB, process needs 10 KB → 6 KB wasted *inside*, unavailable to any other process). With paging: the last page of a process is under-full (process of 10,001 bytes in 4 KB pages → 4 pages = 16 KB → 4,095 bytes wasted per *under-full* last page, worst case 4 KB−1).
- **External fragmentation**: total free space is enough, but it's split among holes, each too small for the next request. Caused by variable-size (dynamic) allocation and by allocation policies that leave tiny residuals.
- **Compaction**: stop all processes (or one at a time, cooperative), copy each process's image to a new location so that all free memory is merged into one hole at one end, update base registers (run-time binding makes this safe), then resume.

## 3. When Is It Used?
- **Classic contiguous-memory OSes** (early Unix, OS/360, MFT/MVT): compaction invoked when a request can't be placed.
- **In-kernel**: Linux's buddy allocator performs *page-level* compaction (`mm/compaction.c`) to create contiguous *pages* for huge pages and CMA, using movable pages — this is the modern descendant of compaction.
- **JVM/Go collectors**: *compacting GC* (moving/copying collectors, e.g., G1, ZGC, Go's GC) relocate live objects to eliminate heap fragmentation — the concept reused for heaps, not physical RAM.
- **Databases**: space-reclaim passes and *rewrite/rebuild* operations compact fragmented index pages.

## 4. Why Wasn't Another Approach Chosen?
- **Paging (chosen instead)**: eliminates external fragmentation by using fixed-size pages scattered anywhere — no compaction ever needed for user processes. The 4 KB granularity only causes small internal fragmentation (≤4 KB−1 per segment). This is the decisive alternative that won.
- **Segmentation without compaction**: pure segmentation suffers both internal (segment padding) and external (variable segment sizes) fragmentation — worse than paging alone.
- **Never compacting (choose to fail)**: simplest, but unusable — memory becomes unusable over time.
- **Copying compaction is unsafe while running** unless addresses are resolvable at run time (base/limit) — so compaction needs MMU support; on MMU-less systems it's effectively impossible.
- **Best-fit with aggressive coalescing**: reduces but never eliminates fragmentation; pathological orders still defeat it.

## 5. Intuition
A parking lot: cars (processes) park one after another; when cars leave, empty spots are scattered everywhere. Total free spots may be 100, but no *contiguous* run of 40 spots exists for the next bus. That's external fragmentation. Compaction = tow every car to one side, so all empty space is one big lot. But you must move every car (slow), and you can't move cars that have passengers inside mid-journey (running processes) without special permission (run-time binding).

## 6. Real-World Analogy
A hard-drive defragmenter: files scattered in fragments are physically rearranged so free space becomes one contiguous region. Windows' `defrag` and the old DOS `DEFRAG` are literally compaction for the file system. Just as defragging a disk takes a long time (you move everything), memory compaction is O(total memory).

## 7. Formal Definition
- **Internal fragmentation** is the difference between the memory allocated to a process and the memory it actually needs (the allocated block size minus the used size), occurring when allocation granularity exceeds request granularity.
- **External fragmentation** is the condition where total free memory exceeds the requested amount, but no single contiguous free region is large enough to satisfy it; it results from a variable-size (dynamic) allocation scheme.
- **Compaction** is the relocation of all allocated blocks to contiguous addresses (typically one end of memory) to consolidate free memory into a single region; it is feasible only when addressing is relocatable (run-time binding).

## 8. Example
256 KB RAM. Processes: A=50 KB @0, B=30 KB @50, C=70 KB @80. Then C exits.
- Free: [0,50]? no — A there. Actually free regions: `[50,80)=30 KB` and `[150,256)=106 KB` (since C occupied [80,150)). Total free = 136 KB.
- A request for 90 KB arrives. No single hole ≥ 90 KB → **request fails though 136 KB is free** (external fragmentation).
- **Compaction**: move B from [50,80) to [0,50) (after moving A... order matters). Suppose final layout: A@0(50), B@50(30), free = [80,256) = 176 KB contiguous. Now the 90 KB request succeeds.
- **Internal fragmentation example**: with fixed 64 KB partitions, a 50 KB process uses 64 KB → 14 KB internal waste; a 10 KB process uses 64 KB → 54 KB waste.

## 9. Internal Working
1. **Detection**: `alloc(S)` scans the free-list; no hole ≥ S → fragmentation detected.
2. **Selection**: choose whether to compact (cost: O(total RAM)) or swap out (cost: O(image size) I/O); OS heuristics compare sizes.
3. **Suspend**: for compaction, processes must be quiescent — the OS typically stops them at the scheduler boundary (or uses per-process relocation windows).
4. **Relocate**: copy each process's image to its new base; because translation is via base/limit (run-time binding), only the base register changes — no code patching.
5. **Merge**: the entire free space is now one hole.
6. **Resume** and serve the request.
Modern kernels do the page-level equivalent: `compact_zone()` migrates movable pages into contiguous runs (e.g., to form a 2 MB huge page or CMA region).

## 10. Time Complexity
- Detect external fragmentation: O(n) scan of free-list.
- Compaction: **O(total physical memory in use)** — copy every live byte; worst case O(M) for M bytes of allocated RAM.
- Page-level compaction (Linux): O(pages moved), bounded by migration cost per page (copy + page-table update + TLB flush).
- Internal fragmentation overhead under paging: ≤ `page_size − 1` bytes per mapping (amortized negligible: (2⁴⁰⁹⁶−1)/n for a large n-byte segment).
- No compaction under pure paging (for user processes): O(0) — the structural win.

## 11. Advantages
- Restores the ability to place large requests in a contiguous scheme (avoids failing despite free memory).
- Simple conceptually; a pure software operation (needs only base/limit relocation).
- Improves *cache/TLB locality*: after compaction, a process's pages are adjacent.
- Page-level compaction (Linux) enables **huge pages** and **CMA** without rebooting.

## 12. Disadvantages
- **O(total memory)** — cost scales with everything allocated, not with the request.
- **Stops processes** (liveness/real-time hazard); long unpredictable pauses.
- **Unsafe with fixed/absolute addressing** (compile-time binding) — cannot be used without an MMU or load-time re-patching.
- Rapidly repeated compaction under churn → poor throughput.
- Doesn't fix **internal** fragmentation (fixed partitions still waste inside blocks).
- Complexity: relocation tracking, interrupt/syscall windows, cache invalidation.

## 13. Interview Questions
1. **Q: Internal vs external fragmentation — define precisely.** A: Internal = unused space *inside* an allocated block (allocation granularity > need; e.g., fixed partition or last page). External = free memory split into holes, none large enough for a request, though total free suffices.
2. **Q: Which scheme causes internal and which causes external?** A: Fixed partitions and paging cause internal; dynamic/contiguous allocation causes external (variable sizes). Segmentation causes both.
3. **Q: How much internal fragmentation can paging create?** A: At most `page_size − 1` bytes per mapping (up to 4 KB−1 for 4 KB pages); the *average* is half a page per segment. Statistically negligible on 64-bit systems with many segments.
4. **Q: What is compaction and when is it done?** A: Relocating all processes so free memory becomes one contiguous region; done on-demand when a request can't be placed, at O(total memory) cost.
5. **Q: Why is compaction safe only with run-time binding? (Tricky)** A: Relocation means changing where processes live; only if every address is re-resolved by the MMU each access (base/limit or page tables) can images be copied safely without patching pointers. Compile-time/load-time addressing breaks.
6. **Q: Could you compact while processes run?** A: Not safely mid-instruction; you suspend at scheduler boundaries or copy + wait for quiescence. Real-time systems can't tolerate the pause — another reason they avoid it.
7. **Q: Does paging eliminate external fragmentation entirely?** A: Yes, for user processes — any set of pages fits anywhere. Page *allocation* still sees fragmentation at huge-page/CMA granularity, which is what kernel compaction addresses.
8. **Q: What is Linux's page compaction? (Production)** A: `mm/compaction.c` migrates movable pages to create contiguous runs for huge pages (THP) and CMA; it works at 4 KB page granularity, moving pages to free frames, updating PTEs and flushing TLBs — far cheaper than whole-process compaction.
9. **Q: What's the compaction cost in the worst case?** A: O(M) where M is total allocated memory — every live page must be copied once; plus per-page TLB/cache invalidation.
10. **Q: How do JVMs deal with heap fragmentation?** A: Moving/copying GCs (G1, ZGC) compact the *heap* by copying live objects to contiguous addresses and updating references — the same "compaction" idea applied to the object heap instead of physical RAM.
11. **Q: When is fragmentation actually *good*? (Tricky)** A: Fragmentation of the *page tables* is fine and even desirable: sparse mappings waste no RAM. Also, external fragmentation protects against a single process hogging one huge contiguous region — paging's scattering is a feature, not a bug.
12. **Q: A request fails though free space is ample — what do you do?** A: Compaction (if contiguous), swapping (move a whole process out), or — with paging — this situation never arises for user memory; it can arise for huge pages, where THP falls back to 4 KB pages.

## 14. Follow-Up Questions
1. **Q: Why do file systems defragment?** A: Exactly the same external-fragmentation problem for contiguous file allocation; journaling/extents minimize but don't eliminate it; `fstrim`/`defrag` periodically compacts.
2. **Q: What's the difference between compaction and swapping?** A: Compaction moves processes *within* RAM (no I/O, O(memory)); swapping moves whole processes to disk (I/O, O(size), frees RAM).
3. **Q: How does a copying garbage collector avoid the pause?** A: Concurrent/parallel collectors (ZGC, Shenandoah) copy live objects incrementally using read/load barriers, so the compaction work overlaps with program execution.
4. **Q: Can external fragmentation affect the kernel heap?** A: Yes — the buddy allocator is power-of-two so it has bounded internal (≤50%) and limited external fragmentation; slab caches avoid it for fixed-size objects.

## 15. Coding Example
```c
// Simulate compaction: pack all live blocks to the left, return new free base
#include <stdio.h>
#include <stdbool.h>

typedef struct { unsigned base, size; bool live; } Block;

// blocks[0..n-1] are live or free; compaction moves all live blocks left.
unsigned compact(Block *b, int n) {
    unsigned cursor = 0;
    for (int i = 0; i < n; i++) {
        if (!b[i].live) continue;
        if (b[i].base != cursor) {           // relocate: only base changes (run-time binding)
            b[i].base = cursor;
        }
        cursor += b[i].size;
    }
    return cursor;                            // start of the single merged free hole
}

int main(void) {
    // 256 KB memory: A@0(50), free@50(30), B@80(30), free@110(146)
    Block mem[4] = {
        { 0,   50, true  },
        { 50,  30, false },
        { 80,  30, true  },
        { 110, 146, false},
    };
    unsigned freeBase = compact(mem, 4);
    printf("A now at %u (size %u)\n", mem[0].base, mem[0].size);
    printf("B now at %u (size %u)\n", mem[2].base, mem[2].size);
    printf("single free hole: base=%u size=%u\n", freeBase, 256 - freeBase);
    return 0;
}
```

## 16. Industry Usage
- **Linux kernel**: `mm/compaction.c` for huge-page/CMA formation; `CONFIG_COMPACTION`.
- **JVM**: G1, ZGC, Shenandoah compact the Java heap; Go's GC compacts via copying; .NET and V8 use moving GCs too.
- **Filesystems**: ext4 `e2fsck`/`fsck` and online defrag; XFS `xfs_fsr`; Windows `defrag.exe` — all compaction for storage.
- **Databases**: Postgres's `VACUUM FULL`, SQL Server `ALTER INDEX ... REBUILD`, and page-compact operations reduce fragmentation on disk.
- **Legacy**: OS/360 MVT, MVS storage manager compaction; classic Unix swap-compaction routines.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 8.2.1 "Dynamic Storage-Allocation Problem", 8.2.2 "Fragmentation".
- Tanenbaum, *Modern Operating Systems*, Ch. 3.3 "Memory Management with Bitmaps and Linked Lists".
- Linux source: `mm/compaction.c`, `include/linux/compaction.h`.
- G1/ZGC papers: Oracle "Garbage-First Garbage Collector" (Detlefs et al.), "ZGC" (Tene et al.).
- Knuth, TAOCP Vol. 1, "Fragmentation".

## 18. Cheat Sheet
- Internal = waste inside a block (fixed partitions, paging's last page).
- External = free holes too small (variable/contiguous allocation, segmentation).
- Compaction = shift all live blocks together → one big free hole; O(total RAM).
- Needs run-time binding (base/limit) to be safe.
- Paging eliminates external fragmentation structurally; internal ≤ page−1.
- Linux page-compaction creates huge pages/CMA by migrating pages.
- Compacting GC = compaction applied to a managed heap.
- Swapping ≠ compaction: disk I/O vs in-RAM moves.

## 19. Quiz
1. Paging causes which fragmentation?
   a) external b) internal c) both d) neither → **b**
2. Compaction is O(___):
   a) request size b) total allocated memory c) page count d) n → **b**
3. Compaction requires ___ to be safe:
   a) compile-time binding b) run-time binding c) fixed partitions d) an IOMMU → **b**
4. A 10,001-byte process on 4 KB pages wastes at most:
   a) 0 bytes b) 3,072 bytes c) 4,095 bytes d) 4,096 bytes → **c**
5. External fragmentation is caused by:
   a) fixed partitions b) variable-size allocation c) paging d) TLB misses → **b**
6. Linux page compaction mainly serves:
   a) user malloc b) huge pages & CMA c) swap d) TLB flushing → **b**

## 20. Flashcards
- **Q: Internal vs external fragmentation?** → **A:** Inside allocated blocks vs free holes too small to use.
- **Q: What does compaction do?** → **A:** Moves all live blocks together to make one large free hole; O(total RAM).
- **Q: Why is compaction safe only under run-time binding?** → **A:** Only the MMU base changes; pointers in code don't need patching.
- **Q: Does paging have external fragmentation?** → **A:** No — pages fit anywhere; only internal (≤ page−1 per mapping).
- **Q: What's Linux page compaction for?** → **A:** Huge pages (THP) and CMA contiguous regions.
- **Q: Compacting GC?** → **A:** JVM/Go collectors copy live objects to eliminate heap fragmentation.

## 21. Revision
Fragmentation is where memory allocation loses usable RAM. Internal fragmentation (waste inside a block) comes from fixed partitions and paging's under-filled last page (≤ 4 KB−1). External fragmentation (free space split into unusable holes) comes from variable-size allocation and causes "free space exists but the request fails." Compaction — moving every live block to one end — fixes it but costs O(total memory) and needs run-time binding; that cost is why systems chose paging instead, which eliminates external fragmentation structurally. The concept survives as Linux page compaction for huge pages/CMA and as compacting garbage collectors for managed heaps.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Internal vs external fragmentation?" | 7 Formal / 13 Q1 |
| "Which scheme causes which fragmentation?" | 8 Example / 13 Q2 |
| "Why is compaction expensive?" | 10 Time / 13 Q9 |
| "Why does compaction need run-time binding?" | 13 Q5 / 9 Internal |
| "How does Linux do compaction?" | 13 Q8 / 16 Industry |
| "How do JVMs handle fragmentation?" | 13 Q10 / 14 Follow-Up Q3 |
