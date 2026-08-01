# LRU and Approximations

> **TL;DR**: **LRU (Least Recently Used)** evicts the page unused for the longest time — the practical stand-in for Optimal, with the stack property — but exact implementation is too expensive, so systems use **approximations** (reference-bit/aging) that capture recency cheaply.

## 1. Why Does This Exist?
Optimal (Section 02) tells us the best eviction is "farthest future use," but we can't see the future. LRU exists because **recency approximates future use**: a page not touched recently is likely to stay untouched. It's the natural, implementable version of Optimal's insight, and its stack property means adding memory can never hurt. It exists as the *reference algorithm* — every OS, database, and cache either uses LRU or an approximation of it, because it captures the locality principle (Part 07 Sec 01) almost perfectly.

## 2. How Does It Work?
**Exact LRU:**
- Maintain recency order of all resident pages (a doubly-linked list; most-recently-used at front, LRU at back), or a hardware-use-counter on each page.
- Hit → move the page to the front (O(1) list move).
- Miss, free frame → add at front.
- Miss, no frame → evict the back of the list.
- Needs per-reference update → a fault on every hit if software; hardware use-counts help but are expensive to scan.

**Approximations (what systems actually do):**
- **Reference bit**: hardware sets a bit on access; OS samples it periodically.
- **Aging**: keep an 8-bit counter per page; each period shift right and OR in the reference bit; victim = smallest counter. Captures *recency-weighted frequency*.
- **Enhanced/second-chance**: reference + dirty bits → 4 classes (0,0 clean-not-referenced best victim … 1,1 referenced+dirty worst).

## 3. When Is It Used?
- **Every modern OS**: Linux's multi-list LRU (active/inactive lists with refault detection), Windows working-set manager, macOS vm_pageout.
- **Database buffer pools**: InnoDB uses a variant of LRU with an "old block" zone; Postgres clock sweep.
- **CPU caches**: hardware cache replacement is literally LRU (or pseudo-LRU) for set-associative caches.
- **Web/CDN caches, key-value stores** (Redis `allkeys-lru`).

## 4. Why Wasn't Another Approach Chosen?
- **Exact LRU via per-reference list updates (rejected)**: on every memory access you'd touch kernel lists → catastrophically slow. Hardware timestamps need a scan per eviction → O(m) or O(n).
- **FIFO (rejected)**: no recency (Section 02).
- **LFU (Section 04)**: frequency without recency — can pin "once-hot, now-dead" pages forever (cache pollution).
- **Clock/aging (chosen)**: reference-bit sampling gives LRU-ish quality at O(1) amortized — the accepted compromise.
- **Pseudo-LRU (hardware)**: a cheap binary-tree approximation used in CPU caches.

## 5. Intuition
LRU is the "last person to use the copy machine" rule: the person who used it longest ago is least likely to use it again soon, so their printouts go to the recycling bin first. The stack of recent usage is the mental model — but tracking every single use is expensive, so real systems just ask each page "have you been touched recently?" (reference bit) every now and then, and treat "no" repeatedly as "cold."

## 6. Real-World Analogy
A restaurant pantry: LRU = the chef throws away the ingredient that hasn't been used for the longest (most likely expired/not needed). The perfect version records every pinch of every ingredient (expensive); the practical version just checks the "use-by" marks (reference bit) periodically and bins anything untouched for two checks (aging).

## 7. Formal Definition
**LRU replacement** evicts the page whose most recent reference is earliest. Implemented with a recency-ordered list, LRU is O(1) per reference (list move) and has the stack property (the set for m frames is a subset of that for m+1), hence it never exhibits Belady's anomaly. Because exact LRU requires updating a global order on every access, practical systems approximate it: the **reference bit** (set by the MMU) is sampled; **aging** maintains a per-page saturating counter, shifted and OR'd with the reference bit each window, so the smallest counter approximates "least recently/frequently used."

## 8. Example
Reference string: `7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1`, m = 3.
LRU simulation (MRU → LRU):
| Ref | Set before | Hit? | Set after | Fault? |
|---|---|---|---|---|
| 7 | — | – | 7 | F |
| 0 | 7 | – | 7,0 | F |
| 1 | 7,0 | – | 7,0,1 | F |
| 2 | 7,0,1 | – | 0,1,2 (evict 7) | F |
| 0 | 0,1,2 | hit | 1,2,0 | – |
| 3 | 1,2,0 | – | 2,0,3 (evict 1) | F |
| 0 | 2,0,3 | hit | 2,3,0 | – |
| 4 | 2,3,0 | – | 3,0,4 (evict 2) | F |
| 2 | 3,0,4 | – | 0,4,2 (evict 3) | F |
| 3 | 0,4,2 | – | 4,2,3 (evict 0) | F |
| 0 | 4,2,3 | – | 2,3,0 (evict 4) | F |
| 3 | 2,3,0 | hit | 2,0,3 | – |
| 2 | 2,0,3 | hit | 0,3,2 | – |
| 1 | 0,3,2 | – | 3,2,1 (evict 0) | F |
| 2 | 3,2,1 | hit | 3,1,2 | – |
| 0 | 3,1,2 | – | 1,2,0 (evict 3) | F |
| 1 | 1,2,0 | hit | 2,0,1 | – |
| 7 | 2,0,1 | – | 0,1,7 (evict 2) | F |
| 0 | 0,1,7 | hit | 1,7,0 | – |
| 1 | 1,7,0 | hit | 7,0,1 | – |

Total faults = **12** (vs FIFO 15, OPT 9).

**Aging example:** page X: counter 0110 0000, this window's ref bit = 1 → shift → 0011 0000 | 1 = 0011 0001. A page never touched keeps shifting right toward 0 → cold → evict.

## 9. Internal Working
**Exact LRU (list):**
1. Each resident page has a doubly-linked node.
2. Hit: unlink + push to MRU end.
3. Eviction: pop LRU end; writeback if dirty; clear PTE/TLB; reuse frame.

**Approximation (Linux-style active/inactive lists):**
1. Two lists: **active** (recently touched, "hot") and **inactive** (candidate victims).
2. Fault inserts into inactive; a hit on an inactive page promotes it to active.
3. Reclaim walks the inactive list; pages with the reference bit set get another chance (moved back), un-referenced ones are evicted.
4. Periodically, active pages with the ref bit clear demote to inactive.
5. Refault-distance detection (Linux `workingset.c`) distinguishes "page thrashing" from "page gone" to tune list sizes.

## 10. Time Complexity
- Exact LRU: O(1) per reference (list move) — but the move happens in software on *every access* → too slow for general memory.
- Aging sample: O(m) per sampling window (scan counters); O(1) amortized per access (bit set by hardware).
- Clock (Section 04): O(1) amortized — the practical champion.
- Refault-distance (Linux): O(1) per page with xa_tree/shadow entries; O(k) on reclaim for sampled decisions.

## 11. Advantages
- **Near-optimal quality**: matches Optimal within a small constant on most workloads (12 vs 9 on the textbook string).
- **Stack property** ⇒ no Belady's anomaly.
- Captures **temporal locality** precisely.
- Cheap approximations (aging/Clock) preserve most of the benefit at O(1).
- Used identically for CPU caches, page cache, DB buffers — one idea, many domains.

## 12. Disadvantages
- **Exact implementation is too expensive** in software (per-access updates).
- **Sequential-scan pollution**: reading a huge array once fills LRU with soon-unneeded pages (mitigated by list separation/Clock variants).
- Needs the **reference bit** in hardware; OSes without it approximate via dirty/page-cache lists.
- Aging counters saturate; long-running pages need care.
- Recency ≠ frequency: a page touched twice an hour ago beats a page touched once a second ago in pure LRU — hence LFU hybrids.

## 13. Interview Questions
1. **Q: What is LRU and why is it used?** A: Evicts the least recently used page — recency as a proxy for "next use" (locality); it's the practical stand-in for Optimal with the stack property.
2. **Q: Why can't we implement exact LRU in an OS? (Tricky)** A: Every reference would require a software list move (or timestamp scan) — a per-access kernel operation that's catastrophically slow; systems approximate with the reference bit.
3. **Q: What's the reference bit and how is it used?** A: Hardware sets it whenever the page is accessed; the OS samples it periodically (aging: shift counter right, OR in bit) to rank recency cheaply.
4. **Q: How does LRU compare to FIFO and OPT on the textbook string?** A: 12 faults (LRU) vs 15 (FIFO) vs 9 (OPT) at m=3 — LRU beats FIFO, approaches OPT.
5. **Q: Does LRU have Belady's anomaly?** A: No — it has the stack property (resident set for m frames ⊆ m+1 frames), so more frames never hurt.
6. **Q: What is aging?** A: A per-page saturating counter shifted right each window and OR'd with the current reference bit — small counter ⇒ cold; a cheap recency-weighted approximation of LRU.
7. **Q: What is the "sequential scan" problem with LRU?** A: A full-file scan marks every page recently-used, evicting hot pages that will be needed again — Linux mitigates with separate active/inactive lists and fault-around.
8. **Q: What are Linux's active and inactive lists?** A: Two LRU lists: inactive holds fault-in candidates; hits promote pages to active; reclaim scans inactive, giving referenced pages a second chance. A two-speed LRU approximation.
9. **Q: When does LRU fail vs LFU? (Scenario)** A: A page accessed once per second but "cold between accesses" looks LRU-warm; a page hot for one minute then dead looks LFU-hot forever. Hybrids (LRU-K, W-TinyLFU) fix both.
10. **Q: How does the refault-distance mechanism work? (Production)** A: When an evicted page is refaulted, Linux compares the time between eviction and refault to decide if the page cache is too small — dynamically balancing file vs anon memory without per-reference LRU.
11. **Q: How is LRU implemented in a database buffer pool?** A: InnoDB keeps an LRU list but with a 37%-tail "old" region: new pages land there and must survive to enter the hot region — protecting the hot set from scans.
12. **Q: What's pseudo-LRU?** A: A binary-tree approximation (each internal node stores which subtree was touched) — O(1) updates without a full stack, used in CPU caches.

## 14. Follow-Up Questions
1. **Q: What's the difference between aging and Clock?** A: Aging = counters sampled periodically (LRU-by-counter); Clock = a sweep hand with second-chance reference-bit checks (Section 04). Both O(1)-ish approximations.
2. **Q: How do you handle dirty pages under LRU?** A: Write back before eviction; algorithms may prefer clean victims (tie-break by dirty bit) to avoid writeback latency.
3. **Q: What is LRU-K?** A: Track the time of the *K-th most recent* reference, not just the last — better at separating transient scans from long-term hot pages.
4. **Q: How does the OS know when a ref bit changed?** A: It clears bits (e.g., via `ptep_clear_and_test_young`) at sampling windows and watches for sets; some architectures have a `young` bit hook.

## 15. Coding Example
```c
// Aging (LRU approximation) simulator with reference bits
#include <stdio.h>
#include <string.h>

#define NP 8
unsigned char age[NP];        // 8-bit aging counters
int present[NP];
int refs[] = {0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1};
int n = sizeof refs / sizeof *refs;

void tick(unsigned touched) {
    for (int p = 0; p < NP; p++) {
        if (!present[p]) continue;
        age[p] >>= 1;                          // decay
        if (p == touched) age[p] |= 0x80;      // reference bit -> high bit
    }
}

int evict(void) {
    int best = -1; unsigned bestv = 0xFF;
    for (int p = 0; p < NP; p++)
        if (present[p] && age[p] < bestv) { bestv = age[p]; best = p; }
    return best;
}

int main(void) {
    int frames = 3, filled = 0, faults = 0;
    for (int i = 0; i < n; i++) {
        int r = refs[i];
        if (present[r]) { tick(r); continue; }
        faults++;
        if (filled < frames) { present[r] = 1; filled++; tick(r); }
        else {
            int v = evict();
            present[v] = 0;
            present[r] = 1;
            tick(r);
            printf("evicted %d for %d\n", v, r);
        }
    }
    printf("aging faults: %d (LRU exact would be 12)\n", faults);
    return 0;
}
```

## 16. Industry Usage
- **Linux**: `mm/vmscan.c` (active/inactive LRU), `mm/workingset.c` (refault distance), `mm/swap_state.c`; sysctl knobs `vm.swappiness`, `vm.vfs_cache_pressure`.
- **Windows**: working-set manager (MRU/LRU list, clock-like trimmer).
- **macOS/XNU**: `vm_pageout` with LRU + compression.
- **CPU caches**: Intel/AMD set-associative caches use LRU/pseudo-LRU replacement.
- **Databases**: InnoDB buffer pool LRU with old-block zone; Postgres `clock sweep`; RocksDB `LRUCache`.
- **Caches**: Redis `maxmemory-policy allkeys-lru`; CDNs (Varnish, nginx proxy_cache) LRU variants.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 9.4.3 "LRU Replacement", 9.4.4 "LRU Approximation".
- Tanenbaum, *Modern Operating Systems*, Ch. 3.7.
- Intel SDM: paging (reference bit behavior).
- Linux: `mm/vmscan.c`, `mm/workingset.c`, `Documentation/admin-guide/sysctl/vm.rst`.
- O'Neil et al., "The LRU-K Page Replacement Algorithm" (1993).

## 18. Cheat Sheet
- LRU evicts least-recently-used; stack property; no anomaly.
- Textbook m=3: LRU 12 vs FIFO 15 vs OPT 9.
- Exact LRU = O(1) per ref but per-access software → too slow.
- Reference bit (hardware) + aging counters = cheap LRU.
- Aging: shift right, OR ref bit; smallest counter evicted.
- Active/inactive lists = Linux's two-speed LRU.
- Scan pollution problem → old-block zones (InnoDB) / list separation.
- Refault distance (Linux) tunes cache vs anon balance.
- LRU-K, W-TinyLFU = hybrids with frequency.

## 19. Quiz
1. LRU evicts:
   a) oldest arrival b) least recently used c) least frequent d) random → **b**
2. LRU on the textbook string (m=3):
   a) 9 b) 12 c) 15 d) 16 → **b**
3. Does LRU have Belady's anomaly?
   a) yes b) no (stack property) c) sometimes d) only with dirty pages → **b**
4. Aging uses ___ to approximate LRU:
   a) FIFO queues b) reference bit counters c) TLB d) swap files → **b**
5. A per-access list move makes exact LRU:
   a) fast b) too slow in software c) impossible d) hardware-only → **b**
6. Linux's two-speed LRU uses:
   a) active/inactive lists b) FIFO only c) OPT d) no lists → **a**

## 20. Flashcards
- **Q: LRU victim?** → **A:** The page whose most recent reference is earliest.
- **Q: LRU vs FIFO/OPT faults (m=3)?** → **A:** 12 vs 15 vs 9.
- **Q: Why approximate LRU?** → **A:** Exact needs per-access updates — too slow in software.
- **Q: What is aging?** → **A:** Shift per-page counter right, OR reference bit; smallest = evict.
- **Q: What are Linux active/inactive lists?** → **A:** Two-speed LRU: hot pages promoted, reclaim scans inactive.
- **Q: Stack property?** → **A:** LRU/OPT sets are nested by m; no anomaly.

## 21. Revision
LRU replaces "future use" with "recent use," matching Optimal's intuition with the stack property (12 faults vs 15 FIFO/9 OPT on the classic string). Exact LRU is too expensive (per-access software updates), so real systems approximate: hardware reference bits sampled periodically (aging counters), or Clock-style second-chance sweeps, or Linux's active/inactive lists plus refault-distance tuning. LRU is the workhorse of OS page reclaim, database buffer pools, and CPU caches — and the starting point for hybrid algorithms (LRU-K, W-TinyLFU) that also count frequency (Section 04).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is LRU and why?" | 1 Why / 13 Q1 |
| "Why can't exact LRU be implemented?" | 13 Q2 / 4 Alternative |
| "What is aging?" | 13 Q6 / 2 How |
| "Compare LRU to FIFO/OPT." | 8 Example / 13 Q4 |
| "Does LRU have Belady's anomaly?" | 13 Q5 / 7 Formal |
| "How does Linux implement LRU?" | 13 Q8 / 16 Industry |
