# Page Replacement Fundamentals

> **TL;DR**: When demand paging fills every frame, the next fault forces an **eviction** — a page-replacement algorithm picks the victim to minimize future faults; algorithms are judged by fault rate, optimality (vs the unreachable Optimal), and overhead.

## 1. Why Does This Exist?
Demand paging (Part 07 Sec 02) has an implicit limit: physical frames are finite. The first time a process needs a page with no free frames, the OS must *evict* a resident page to make room. Page replacement exists to answer "which page should go?" — because that choice determines performance. Evicting a page that's needed again soon causes an immediate refault (double cost); evicting a page never needed again is free. Since the OS can't know the future, algorithms approximate "least likely to be needed soon" using recency, frequency, or position. Replacement quality is the difference between a fast system and one that thrashes.

## 2. How Does It Work?
On a page fault when free frames = 0:
1. Pick a victim page V using the algorithm (FIFO, Optimal, LRU, Clock, LFU…).
2. If V is **dirty** (modified), write it back (to swap or its file) before reuse.
3. Clear V's PTE (present=0), record its backing-store location if it's anonymous.
4. Load the faulting page into V's frame, install the PTE.
5. Update the algorithm's bookkeeping (queue/timestamps/counters).

Metrics: **fault rate** = faults / references; **hit ratio** = 1 − fault rate. A good algorithm minimizes future faults cheaply.

## 3. When Is It Used?
- **Every page fault with memory pressure** on Linux/Windows/macOS/Android/iOS.
- **Kernel memory** too: the kernel's own reclaim paths (shrinker) decide which file/anon pages to evict.
- **Caches**: file caches, DB buffer pools, and even CPU cache policies apply the same recency/frequency logic (this is a universal design pattern).
- **Huge pages / THP** reclaim uses the same machinery at 2 MB granularity.

## 4. Why Wasn't Another Approach Chosen?
- **Never evict (reject faults / just fail)**: unusable — programs would fail instead of slow down; oversubscription impossible.
- **Evict the page at the *front* (FIFO)**: simple but ignores recency/frequency — can evict a hot page (the "second-chance" idea fixes this).
- **Evict randomly**: uniform cost, unpredictable quality — worse than recency-based.
- **Ask the process (user hints)**: `madvise` exists but can't be relied on; OS must be self-sufficient.
- **More RAM instead**: still need replacement for oversubscription and cache; doesn't remove the problem.
- **Optimal (future knowledge)**: theoretically best, impossible to implement — used only as the evaluation ceiling.

## 5. Intuition
A hotel with N rooms (frames) and unlimited guests (pages). When a guest needs a room and all are occupied, the manager evicts someone. The ideal: evict the guest who'll return latest (Optimal). Without a crystal ball, the manager guesses by rules: "evict the first guest to check in" (FIFO), "evict the guest who checked in longest ago and hasn't been seen recently" (LRU-ish), or "evict a guest who rarely comes down to breakfast" (LFU). Every choice risks evicting someone who comes back immediately — a refault.

## 6. Real-World Analogy
A parking garage that's always full. When a new car arrives, the attendant decides which car to remove. FIFO = tow the first car that parked (even if its owner is about to return). LRU = tow the car that was last used longest ago (probably the owner isn't coming soon). Optimal = somehow know the future and tow the car whose owner will return latest. Refaulting = towing a car whose owner returns 2 minutes later.

## 7. Formal Definition
Given a fixed number of frames m and a **reference string** (sequence of page references), a **page-replacement algorithm** selects, on each page fault with no free frame, a victim page to remove from the resident set. The goal is to minimize the number of page faults over the reference string. An algorithm has the **stack property** if the set of resident pages for m frames is a subset of those for m+1 frames (all optimal, LRU); algorithms without it (FIFO) can exhibit **Belady's anomaly** (increasing frames increases faults). The **fault rate** is the ratio of faults to total references.

## 8. Example
Reference string: `7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1`, m = 3 frames.

Count faults for FIFO vs LRU (quick walk — full tables in Sections 02/03):
- FIFO: faults = 15.
- LRU: faults = 12.
- Optimal: faults = 9.

Observations: Optimal is a lower bound; LRU beats FIFO because it keeps `7` out longer only when recency suggests; the gap grows with workload. This reference string is the textbook example (Silberschatz) — memorize it.

## 9. Internal Working
1. **Fault path**: `handle_mm_fault` → frame allocator returns no free page → enter reclaim.
2. **Scan candidates**: iterate frames/pages (LRU list, Clock hand, shrinker lists).
3. **Choose victim** per algorithm.
4. **Writeback**: if dirty → `writeback` (swap/file); the eviction is not complete until the data is safe.
5. **Unmap/clear**: TLB flush the victim's PTE; mark page free.
6. **Load new page** into the freed frame; install PTE; update stats.
7. Modern Linux batches: reclaim works on page lists, throttles via `kswapd` wakeups, and uses heuristics (refault distance) rather than a pure textbook algorithm.

## 10. Time Complexity
- FIFO: O(1) — queue push/pop.
- Optimal: O(n) to *evaluate* (needs future) — hence unreachable.
- LRU exact: O(1) per ref but O(m) state per ref (or a hardware counter) — costly.
- Clock: O(1) amortized — one hand sweep, each pass clears a bit.
- LFU: O(1) with a counter, O(m) or O(log m) to find min-frequency; aging variants cheaper.
- Linux's multi-list LRU: O(1) per page with deferred writeback.

## 11. Advantages
- Enables **oversubscription** — run more than fits.
- Turns RAM into an **adaptive cache** (files, anonymous, mmap all share).
- Cheap algorithms (Clock) deliver near-LRU quality at O(1).
- Recency/frequency heuristics exploit locality (why they work).
- Clean integration with dirty-bit writeback for correctness.

## 12. Disadvantages
- **Fault latency** inherent to eviction+load.
- **Writeback I/O** before reuse (dirty victims stall).
- **Algorithm tuning**: no single algorithm is optimal for all workloads.
- **Thrashing** when total working set > frames (Chapter 03) — algorithms can't fix allocation failure.
- Bookkeeping overhead (lists, counters, scans) at scale.
- Interference: file cache vs anon pages compete (Linux balances).

## 13. Interview Questions
1. **Q: Why does an OS need page replacement?** A: Physical frames are finite; on a fault with no free frame, the OS must evict a resident page, and the choice (victim selection) determines future fault rate.
2. **Q: What metric evaluates replacement algorithms?** A: Number of page faults (or fault rate = faults/references) over a reference string; lower is better. Hit ratio = 1 − fault rate.
3. **Q: What is a reference string?** A: The sequence of page numbers referenced (e.g., `7 0 1 2 0 3 0 4 …`), abstracting address streams for algorithm comparison.
4. **Q: What is the Optimal algorithm?** A: Evict the page whose next use is farthest in the future; provably minimizes faults (Belady's algorithm) but requires future knowledge — it's the theoretical ceiling for evaluation only.
5. **Q: What is Belady's anomaly?** A: For some algorithms (FIFO), increasing the frame count can *increase* the fault count; stack-property algorithms (Optimal, LRU) never suffer it.
6. **Q: What is the stack property?** A: The resident set for m frames is a subset of the resident set for m+1 frames, so more frames can't hurt. LRU/Optimal have it; FIFO doesn't.
7. **Q: How does the OS know a victim page is dirty?** A: The hardware **dirty bit** in the PTE; a dirty page must be written back before eviction, a clean page can be dropped instantly (file) or merely unlinked (anon→swap).
8. **Q: What's the cost of evicting a dirty page? (Production)** A: A writeback I/O (SSD ~50 µs, HDD ~ms) plus the fault's load I/O — a dirty victim costs roughly 2× a clean one, so algorithms prefer clean victims (secondary criteria).
9. **Q: What is the "second chance" concept?** A: Give a page a reprieve if its reference bit is set: don't evict it; clear the bit and move on — the basis of Clock.
10. **Q: Can replacement algorithms be applied to non-memory caches? (Scenario)** A: Yes — web caches, CPU cache, database buffer pools, CDN edge caches all use LRU/LFU variants; the same theory (and its flaws) applies everywhere.
11. **Q: What happens during eviction of a memory-mapped (file) page?** A: If clean, drop the frame (file still has data); if dirty, write back via the page cache. The PTE is cleared; the VMA still references the file, so refault reloads from the cache/file.
12. **Q: How do algorithms interact with TLB?** A: On eviction the kernel flushes the victim's TLB entries (`invlpg`); the new page's first access walks and refills the TLB.

## 14. Follow-Up Questions
1. **Q: What's the difference between global and local replacement?** A: Global picks victims from all processes' pages (fair, adaptive); local restricts to the faulting process (isolation, prevents one process harming others). Linux uses mostly global with heuristics.
2. **Q: What is "refault distance" in Linux?** A: How far back an evicted page was, used to decide cache vs reclaim balance — Linux's file-cache self-tuning (Workingset Detection).
3. **Q: How does the dirty bit interact with read-only (COW) pages?** A: COW pages are read-only but not dirty; on eviction they're dropped cleanly; on write they become dirty and go to swap.
4. **Q: What is "thrashing" vs "high fault rate"?** A: Thrashing is the runaway case where working sets exceed frames and most cycles go to fault handling — Chapter 03.

## 15. Coding Example
```c
// A generic page-fault simulator shell; plug in a victim policy
#include <stdio.h>
#include <string.h>

#define FRAMES 3
int frames[FRAMES]; int resident[FRAMES]; int count = 0;

// Returns index to evict; policy plug-in (FIFO here)
int pick_victim(void) { return count++ % FRAMES; }

int main(void) {
    int refs[] = {7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1};
    int n = (int)(sizeof refs / sizeof *refs), faults = 0;
    memset(resident, 0, sizeof resident);
    for (int i = 0; i < n; i++) {
        int found = 0;
        for (int f = 0; f < FRAMES; f++)
            if (resident[f] && frames[f] == refs[i]) { found = 1; break; }
        if (found) continue;
        faults++;
        int v = pick_victim();
        frames[v] = refs[i]; resident[v] = 1;
        printf("fault: ref %d -> frame %d\n", refs[i], v);
    }
    printf("total faults (FIFO-ish): %d\n", faults);
    return 0;
}
```

## 16. Industry Usage
- **Linux**: multi-list LRU (`mm/vmscan.c`), Clock/aging (`struct lruvec`, refault detection), reclaim for file/anon via `shrinkers`; `kswapd`/direct reclaim.
- **Windows**: working-set manager + clock-like `MmWorkingSetList`.
- **macOS/XNU**: `vm_pageout` with LRU + compression.
- **Databases**: InnoDB `LRU_list` with an "old block" 37% zone; Postgres clock sweep; Oracle LRU.
- **CDNs/browsers**: HTTP cache uses LRU/LFU hybrid (e.g., Cloudflare's LRU shards).

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 9.4 "Page Replacement" (+ 9.4.1–9.4.5 for FIFO/OPT/LRU/LRU-aprox/Counting).
- Tanenbaum, *Modern Operating Systems*, Ch. 3.7.
- Belady, *A Study of Replacement Algorithms for a Virtual-Storage Computer* (IBM 1966).
- Linux source: `mm/vmscan.c`, `mm/workingset.c`, `Documentation/admin-guide/sysctl/vm.rst`.
- Corbett: "How does the Linux page cache work?" / lwn.net articles on workingset.

## 18. Cheat Sheet
- Replacement = pick victim when no free frame on fault.
- Fault rate = faults / references; hit ratio = 1 − fault rate.
- Optimal = evict farthest-future use — theoretical floor.
- Stack property ⇒ no Belady anomaly (LRU, Optimal; not FIFO).
- Dirty victim ⇒ writeback cost before reuse.
- FIFO O(1); LRU exact O(1) ref but costly; Clock O(1) amortized.
- Global vs local replacement; Linux mostly global + heuristics.
- Thrashing = working sets > frames (Ch 03).
- Eviction clears PTE + flushes TLB; refault reloads.

## 19. Quiz
1. Replacement runs on:
   a) every access b) a fault with no free frame c) TLB miss d) fork → **b**
2. The Optimal algorithm:
   a) is used in production b) needs future knowledge c) is O(1) d) beats LRU rarely → **b**
3. Belady's anomaly affects:
   a) LRU b) Optimal c) FIFO d) stack algorithms → **c**
4. The stack property guarantees:
   a) min faults b) no anomaly c) O(1) d) dirty-free → **b**
5. A dirty victim page must be:
   a) dropped b) written back c) zeroed d) copied → **b**
6. Fault rate = :
   a) faults/refs b) refs/faults c) frames/pages d) hits/refs → **a**

## 20. Flashcards
- **Q: When does replacement happen?** → **A:** On a fault when free frames = 0.
- **Q: Best metric?** → **A:** Fault rate over a reference string; lower = better.
- **Q: What is Optimal?** → **A:** Evict the farthest-future page; theoretical floor, not implementable.
- **Q: What is Belady's anomaly?** → **A:** FIFO can fault more with more frames.
- **Q: Which algorithms are safe (stack property)?** → **A:** LRU and Optimal; FIFO is not.
- **Q: Why prefer clean victims?** → **A:** No writeback I/O before reuse.

## 21. Revision
Page replacement picks a victim page whenever a fault has no free frame, balancing future-fault avoidance against cost. Algorithms: FIFO (O(1), but Belady's anomaly — not a stack algorithm), Optimal (provably minimal, needs the future — evaluation only), LRU (stack property, beats FIFO, but exact implementation is costly → approximated), Clock (O(1), reference-bit driven, production standard), LFU (frequency-based). Dirty pages need writeback before eviction, clean file pages are dropped free. Global vs local allocation decides scope; when total working sets exceed frames, no algorithm saves you — that's thrashing (Chapter 03).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Why is page replacement needed?" | 1 Why / 13 Q1 |
| "What is the Optimal algorithm?" | 13 Q4 / 2 How |
| "What is Belady's anomaly?" | 13 Q5 / 8 Example |
| "What is the stack property?" | 13 Q6 / 7 Formal |
| "How does dirty-bit affect eviction?" | 13 Q7-8 / 9 Internal |
| "Can replacement apply to caches?" | 13 Q10 / 16 Industry |
