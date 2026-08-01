# Contiguous Memory Allocation

> **TL;DR**: Contiguous memory allocation gives each process one unbroken block of physical RAM and tracks free space with a free-list; the OS picks a hole using first/best/worst-fit — simple and fast, but external fragmentation eventually kills it, pushing the world toward paging.

## 1. Why Does This Exist?
The simplest way to multiprogram RAM is to hand each process a single contiguous window, protected by base/limit registers. Contiguous allocation exists because (a) it matches the base/limit protection model exactly — one window, one add, one compare; (b) it needs almost no OS bookkeeping (a list of free ranges); and (c) it has historically minimal hardware requirements (any MMU or even a pure load-time-binding system). It's the baseline every OS textbook derives paging *from*: you understand its failures, then you see why paging must exist.

## 2. How Does It Work?
The OS maintains a **free-list**: a linked list of `[base, size)` intervals of unallocated physical memory (sometimes merged into a buddy/tree for speed). When a process of size S arrives:
1. Pick a free hole of size ≥ S using a placement policy (first-fit / best-fit / worst-fit).
2. Allocate `[hole_base, hole_base + S)`; set the process's base/limit registers.
3. Trim the hole (split it into the allocated block + a smaller remainder hole), or remove it if it exactly fits.
4. On process exit, return the block and **merge adjacent holes** to prevent the free-list from fragmenting further.

The mapping is pure offset translation — identical to base/limit.

## 3. When Is It Used?
- **OS kernels themselves** for early boot and small fixed allocations (before the slab/buddy allocators take over): e.g., the kernel's linear mapping is contiguous-ish, `memblock` on Linux uses ranges.
- **RTOS / bare-metal** (FreeRTOS heap_1/heap_2/heap_4 use free-list contiguous allocation): deterministic, no MMU needed.
- **Real-time & safety-critical** systems where a process's memory must be one physical block (no page faults, predictable timing).
- **Swapping systems** (see Chapter 02 Section 03) — a process's swap image is one contiguous region.
- Historically: all general-purpose OSes (DOS, classic Unix, early Windows) until paging hardware became universal.

## 4. Why Wasn't Another Approach Chosen?
- **One big partition / no allocation (monoprogramming)**: trivial but no multiprogramming → CPU idle during I/O. Rejected for utilization.
- **Overlays**: program itself manages a fixed window. Rejected: programmer burden.
- **Fixed partitions (multiple static sizes)**: O(1) allocation, but internal fragmentation (a 10 KB process in a 16 KB partition wastes 6 KB) and partition-size guessing. Rejected for wasting RAM.
- **Non-contiguous / paging**: solves external fragmentation and enables sharing and VM — but needs an MMU with page tables and a TLB. Chosen on all modern hardware.
- **Free-list + first/best/worst fit**: chosen for the contiguous world because it balances speed and fragmentation; buddy allocator is the modern refinement (Linux kernel's `mm/page_alloc.c` uses buddy).

## 5. Intuition
Think of RAM as a strip of rental parking. Each process rents a contiguous run of spots. When renters leave, the strip gets holes. To park a new car (process) you scan for a run of free spots long enough. Where you start scanning decides whether you fill the first hole (first-fit), the tightest hole (best-fit), or the largest hole (worst-fit). The holes are the free-list; merging adjacent holes is repainting the dividing lines when two neighbors both leave.

## 6. Real-World Analogy
A bookcase shelf of contiguous books. Adding a book of size S means finding a gap of ≥ S slots. You can insert at the first gap (first-fit — fast, but might've been better for a bigger book later), the tightest gap (best-fit — leaves the least unused space but leaves a bookcase of many tiny useless gaps), or the biggest gap (worst-fit — keeps big gaps for future big books). When a book is removed, merge the two adjacent gaps into one larger gap (coalescing).

## 7. Formal Definition
Contiguous memory allocation is a memory-management scheme in which each process is allocated a single contiguous region of physical memory. Free memory is maintained as a list of holes. Given a request for size S, a hole of size ≥ S is selected by a placement policy, the process is assigned the first S bytes of the hole, and the remainder becomes a new hole. Upon deallocation, adjacent holes are merged (coalesced) to maximize the largest available contiguous free size. The scheme guarantees internal efficiency O(1) per access via base/limit translation but is subject to external fragmentation.

## 8. Example
Free holes: `[0, 10 KB]`, `[20, 30 KB]`, `[40, 60 KB]`. Requests arrive for 8 KB, 12 KB, 10 KB (in that order).

**First-fit** (scan from start):
- 8 KB → hole [0,10] → use [0,8], remainder [8,10].
- 12 KB → hole [20,30] (size 10 < 12, skip) → hole [40,60] (size 20) → use [40,52], remainder [52,60].
- 10 KB → hole [20,30] (size 10) → use [20,30], no remainder.

**Best-fit** (smallest hole ≥ request):
- 8 KB → holes 10,10,20 → use the 10 KB hole [0,10] → remainder [8,10].
- 12 KB → holes 10,20 → use [40,60] → remainder [52,60].
- 10 KB → hole [20,30] exactly → use fully.

**Worst-fit** (largest hole):
- 8 KB → [40,60] (20 KB) → remainder [48,60].
- 12 KB → [20,30]? size 10 <12 no; [0,10] no; [48,60] (12) → use fully.
- 10 KB → [20,30] (10) → use fully.

Observe how each policy produces different fragmentation: best-fit left a 2 KB sliver [8,10] and a 8 KB tail; first-fit left [8,10] and [52,60].

## 9. Internal Working
1. **Request**: `alloc(S)` → walk the free-list.
2. **Placement** (per policy):
   - first-fit: return the first hole with size ≥ S.
   - best-fit: return the smallest hole ≥ S (requires full scan).
   - worst-fit: return the largest hole (full scan).
3. **Split**: if `hole.size > S`, replace hole with `[hole.base + S, hole.size − S)`.
4. **Bind**: set process base/limit; PCB records the region.
5. **Free**: on exit, insert `[base, S)` back; check neighbors and coalesce adjacent free blocks (keeps the free-list's max-block large).
6. **Oversubscription handling**: if no hole ≥ S, options are (a) compact (Chapter 02 Sec 02), (b) swap out a process (Sec 03), or (c) fail the request.
7. **Growth**: growing a process may require finding a bigger hole and relocating — expensive, so systems reserve slack (the classic "over-allocate on growth" trick).

## 10. Time Complexity
- Allocation:
  - first-fit: O(n) worst-case (n = number of free-list entries); average O(1)–O(n) depending on list layout.
  - best-fit / worst-fit: O(n) always (full scan).
- Deallocation + coalescing: O(1) with doubly-linked free-list (check prev/next neighbors).
- Buddy allocator refinement: O(log M) for power-of-two sizes (M = memory size in smallest units) — Linux kernel uses this.
- Placement analysis shows first-fit ≥ best-fit ≥ worst-fit in fragmentation terms, but first-fit is fastest in practice.

## 11. Advantages
- **Trivial translation**: base + offset, no page tables, no TLB.
- **Low overhead**: a free-list + base/limit registers is all the bookkeeping.
- **Good locality**: a process's code/data/stack in one contiguous run → excellent cache and prefetch behavior.
- **Simple sharing of I/O buffers** and zero-copy paths (contiguous DMA windows).
- **Deterministic latency** — no page-fault path — ideal for RTOS.

## 12. Disadvantages
- **External fragmentation**: free memory exists but not as one big enough hole.
- No **sharing** of pages between processes; no memory-mapped files.
- **No virtual memory** — entire process resident; large processes impossible.
- **Growth is hard**: may require full-process relocation.
- Holes management cost grows with fragmentation; compaction (if used) is O(total memory).

## 13. Interview Questions
1. **Q: What is contiguous memory allocation?** A: Giving each process a single unbroken block of physical RAM, tracked via a free-list of holes, with base/limit translation.
2. **Q: Explain first-fit, best-fit, worst-fit and their trade-offs.** A: First-fit: first hole ≥ size (fast, tends to leave big tail holes). Best-fit: smallest adequate hole (least per-request waste, but slow, creates tiny slivers). Worst-fit: largest hole (keeps big holes, but fragments large blocks fast). No policy is globally optimal; first-fit usually wins in practice.
3. **Q: How does the OS keep track of free memory?** A: A free-list (linked list of `[base,size]` intervals); on free, coalesce adjacent holes; optionally a bitmap or buddy tree for speed.
4. **Q: Why coalesce adjacent free blocks?** A: Otherwise a single freed 100 KB run split by an in-between allocation later freed as 60 KB + 40 KB might fail to serve a 90 KB request though 100 KB is free — merging restores large holes.
5. **Q: What happens if no single hole fits? (Tricky)** A: The OS can compact (merge holes by moving processes — O(total memory), dangerous while running), swap out a process to disk (O(size) I/O), or fail the allocation.
6. **Q: Why is internal fragmentation caused by fixed partitions but external by dynamic?** A: Fixed partitions round a request up to a partition size (waste inside the block); dynamic partitions fit exactly but leave irregular holes between blocks that may be too small for any future request.
7. **Q: What does a process do when it needs to grow? (Scenario)** A: It must find a larger hole and be *relocated* — the entire image is copied to a bigger window and the base register updated. This is slow and risks failing if no hole exists; modern OSes avoid it via paging (grow by adding pages).
8. **Q: Why is compaction dangerous on a live system?** A: It moves processes while they run — for that to be safe every pointer/address must be re-resolved through base/limit at *load time* (compile-time/linked addresses break), and the copy is O(total RAM) with a window where memory is in flux. Systems almost always choose paging instead.
9. **Q: Where is contiguous allocation still used in production?** A: Kernel early-boot allocators (Linux `memblock`), RTOS heaps, safety-critical systems, DMA buffer pools, and the *buddy* allocator (a power-of-two form of it) inside the Linux kernel's `mm/page_alloc.c`.
10. **Q: What is the buddy allocator and why is it better than a plain free-list?** A: It splits memory into power-of-two blocks and merges buddies on free — allocation and merge are O(log n), fragmentation is bounded, and it supports quick page lookups. It's the contiguous allocator that actually scales; it's how Linux allocates physical pages.
11. **Q: Why did general-purpose OSes abandon contiguous allocation?** A: External fragmentation, no sharing, no growth, no virtual memory — paging (Chapter 03) fixes all four at the cost of a TLB and page-table walks.
12. **Q: If first-fit usually wins, why do textbooks still teach best-fit?** A: Because best-fit optimizes a clear metric (minimal wasted space per allocation) and reveals the scan-vs-fragment trade-off; but its tiny-hole production is why practice prefers first-fit or buddy.

## 14. Follow-Up Questions
1. **Q: How does memory get "moved" during compaction in a base/limit world?** A: The kernel suspends the process, copies the image to the new window, updates the base register (and any load-time-relocated pointers), and resumes — the reason run-time binding matters (Chapter 01).
2. **Q: What's the relationship between the free-list and memory maps in `/proc`?** A: `/proc/<pid>/maps` shows a process's *virtual* regions; a free-list describes physical holes. In contiguous systems the two are directly related; with paging they're decoupled.
3. **Q: Can external fragmentation occur under paging?** A: No — that's the point of paging. Paging only has internal fragmentation (up to `page_size − 1` bytes per page). This is a favorite one-liner in interviews.
4. **Q: How does Linux's physical page allocator avoid fragmentation?** A: The buddy allocator + `CMA` (contiguous memory allocation) reservations + `movable` page types — it reclaims/compacts at the *page* level instead of moving whole processes.

## 15. Coding Example
```c
// Free-list contiguous allocator with first-fit + coalescing
#include <stdio.h>
#include <stdlib.h>

typedef struct Hole { unsigned base, size; struct Hole *next; } Hole;

Hole *new_hole(unsigned b, unsigned s, Hole *n) {
    Hole *h = malloc(sizeof *h); h->base = b; h->size = s; h->next = n; return h;
}

// returns base or -1
long first_fit(Hole **head, unsigned size, unsigned *base_out) {
    Hole *p = *head, **prev = head;
    while (p) {
        if (p->size >= size) {
            unsigned base = p->base;
            p->base += size; p->size -= size;
            if (p->size == 0) { *prev = p->next; free(p); }
            *base_out = base; return base;
        }
        prev = &p->next; p = p->next;
    }
    return -1;
}

void free_block(Hole **head, unsigned base, unsigned size) {
    Hole *n = new_hole(base, size, NULL), *p = *head, **prev = head;
    while (p && p->base < base) { prev = &p->next; p = p->next; }
    n->next = p; *prev = n;
    // coalesce with next, then previous
    if (n->next && n->base + n->size == n->next->base) {
        n->size += n->next->size; n->next = n->next->next;
    }
    if (prev != head && (*prev) && (*prev)->base + (*prev)->size == n->base) {
        (*prev)->size += n->size; (*prev)->next = n->next;
    }
}

int main(void) {
    Hole *list = new_hole(0, 64, NULL);
    unsigned b;
    first_fit(&list, 20, &b); printf("alloc 20 at %u\n", b);
    first_fit(&list, 16, &b); printf("alloc 16 at %u\n", b);
    free_block(&list, 20, 20); printf("freed 20 @ 20 (coalesced with @0 rem)\n");
    first_fit(&list, 25, &b); printf("alloc 25 at %u (uses coalesced 36-byte hole)\n", b);
    return 0;
}
```

## 16. Industry Usage
- **Linux kernel**: `mm/memblock.c` (early boot contiguous ranges), `mm/page_alloc.c` (buddy), `mm/cma.c` (contiguous for DMA), `mm/slab.c`/`slub.c` (small-object contiguous-ish caches).
- **FreeRTOS**: `heap_1.c`/`heap_2.c`/`heap_4.c` implement first-fit-style free-list allocators over a static buffer (no MMU).
- **Safety-critical**: ARINC 653 partition memory managers allocate fixed contiguous partitions to avionics apps.
- **DMA**: `dma_alloc_coherent` returns physically contiguous memory because devices can't walk page tables.
- **Historical**: DOS memory blocks (EBDA/MCB chains), classic Unix on PDP-11 (later used a form of swapping + paging).

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 8.2 "Contiguous Allocation", Ch. 8.3 "Segmentation".
- Tanenbaum, *Modern Operating Systems (4th ed.)*, Ch. 3.2–3.3.
- Linux source: `mm/memblock.c`, `mm/page_alloc.c`, `include/linux/gfp.h`.
- FreeRTOS memory management docs: `heap_1.c`..`heap_5.c`.
- Knuth, *The Art of Computer Programming*, Vol. 1 (first/best/worst-fit analysis, buddy systems).

## 18. Cheat Sheet
- Free-list of `[base, size]` holes; coalesce on free.
- first-fit: first hole ≥ size (fast, practical winner).
- best-fit: smallest adequate hole (min waste, slow, slivers).
- worst-fit: largest hole (keeps big windows, fragments fast).
- Fixed partitions → internal fragmentation; dynamic → external.
- No hole? Compaction (O(total RAM)) / swapping (O(size)) / fail.
- Buddy allocator = power-of-two contiguous, O(log n) — Linux's choice.
- Contiguous → no sharing, no growth, no VM → replaced by paging.

## 19. Quiz
1. Which policy minimizes wasted space per request but is slowest?
   a) first-fit b) best-fit c) worst-fit d) buddy → **b**
2. Coalescing merges:
   a) allocated blocks b) adjacent free holes c) page tables d) TLB entries → **b**
3. External fragmentation happens with:
   a) fixed partitions b) dynamic partitions c) neither d) both → **b**
4. The Linux kernel's physical allocator is a:
   a) best-fit list b) buddy allocator c) slab only d) freelist only → **b**
5. A process that cannot be placed because no hole fits can be:
   a) swapped b) compacted c) failed d) all of the above → **d**
6. Which is O(log n) for power-of-two sizes?
   a) first-fit b) best-fit c) buddy allocator d) worst-fit → **c**

## 20. Flashcards
- **Q: What is contiguous allocation?** → **A:** Each process gets one unbroken physical block, tracked by a free-list of holes.
- **Q: first-fit vs best-fit?** → **A:** first-fit = first hole ≥ size (fast); best-fit = smallest hole ≥ size (min waste, slow).
- **Q: External vs internal fragmentation?** → **A:** External = unusable holes between blocks (dynamic partitions); internal = waste inside an allocated block (fixed partitions/paging).
- **Q: Why coalesce?** → **A:** Adjacent freed holes merge into one large hole so big requests can be served.
- **Q: What is the buddy allocator?** → **A:** Power-of-two split/merge, O(log n), used by the Linux kernel.
- **Q: Why was contiguous allocation replaced?** → **A:** External fragmentation, no sharing, no growth, no virtual memory.

## 21. Revision
Contiguous allocation hands each process one window of RAM, tracked via a free-list; requests pick holes by first/best/worst-fit, and frees coalesce neighbors. It's O(1) per access, needs no page tables, and is still used by kernels (buddy/memblock), RTOS heaps, and DMA pools. Its fatal flaws are external fragmentation (dynamic partitions), no sharing, painful growth (relocation), and no virtual memory — each of which pushes toward paging, where a page is just a 4 KB contiguous unit that can live anywhere.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Explain first/best/worst-fit." | 8 Example / 13 Q2 |
| "What is a free-list and how is it maintained?" | 9 Internal Working / 13 Q3 |
| "Why is coalescing important?" | 9 Internal Working / 13 Q4 |
| "What do you do if no hole fits?" | 9 Internal Working / 13 Q5 |
| "Internal vs external fragmentation?" | 12/13 Q6 |
| "How does Linux allocate physical pages?" | 13 Q9-10 / 16 Industry |
