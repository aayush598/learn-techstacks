# FIFO and Optimal Replacement

> **TL;DR**: **FIFO** evicts the page that's been resident longest (O(1), but suffers Belady's anomaly); **Optimal** evicts the page whose next use is farthest away — provably minimal faults but impossible to implement, serving only as the theoretical yardstick for every other algorithm.

## 1. Why Does This Exist?
- **FIFO exists** as the cheapest possible policy: a simple queue. It's the baseline every algorithm is compared against and the canonical example of "cheap but flawed" — showing *why* we need recency/frequency information.
- **Optimal exists** because you cannot improve what you cannot measure: by computing the minimum possible faults for a reference string, we get an upper bound on *any* algorithm's quality. Every paper/interview benchmark reports how close a real algorithm comes to Optimal. It also sharpens intuition: the best policy is "evict the page needed latest," which recency-based schemes approximate.

## 2. How Does It Work?
**FIFO:** maintain a FIFO queue of resident pages.
- Hit → nothing (queue unchanged).
- Miss + free frame → push page to tail.
- Miss + no frame → dequeue the head (oldest), evict it, push the new page.
- No hardware support needed — pure bookkeeping.

**Optimal (MIN/Belady's):** 
- Miss + no frame → scan the reference string *from the current point onward*; evict the page whose *next reference is farthest in the future* (or never again — those go first).
- Requires full future knowledge → implementationally impossible; used offline for evaluation.

## 3. When Is It Used?
- **FIFO**: as a component, not the OS's main policy — used in queue-based caches (network buffers, some hardware FIFO structures), and as a *candidate set* within more complex schemes (e.g., Linux's file cache uses an "inactive" FIFO-like list feeding an active LRU list). FIFO-style "oldest first" also approximates `MADV_SEQUENTIAL` streaming.
- **Optimal**: purely analytic — benchmark studies, cache-design simulations, and as the upper-bound in comparing web-cache and DB-buffer algorithms.

## 4. Why Wasn't Another Approach Chosen?
- **FIFO as the sole policy (rejected)**: it ignores recency — a hot page sitting in the queue longest gets evicted right before its next use → refault storms. The second-chance/Clock fix exists because of this.
- **Random (rejected)**: no worse than FIFO asymptotically in some analyses, but unpredictable and no better on locality workloads.
- **Optimal (not implementable)**: requires oracle knowledge; used as a benchmark instead.
- **LRU (chosen as reference)**: recency approximates "next use" far better than arrival order with O(1) amortized approximations (Clock) — hence FIFO is superseded but Optimal remains the benchmark.

## 5. Intuition
**FIFO** is a conveyor belt: the first box in is the first out, whether it's needed again immediately or not. **Optimal** is a fortune-teller: it knows the entire future schedule and always moves out the item needed latest — no rework ever.

## 6. Real-World Analogy
- **FIFO**: a grocery store with one shelf of "featured" products; every new product pushes out the oldest, even if customers buy it constantly.
- **Optimal**: a chef who knows tonight's entire order sheet and preps only what will be plated next — never wastes a dish, but impossible without the future menu.

## 7. Formal Definition
**FIFO (First-In-First-Out) replacement** evicts the page that entered the resident set earliest; it is implementable in O(1) with a queue but lacks the stack property, so it exhibits **Belady's anomaly** — page-fault count can rise when the frame count rises. **Optimal (MIN, Belady) replacement** evicts the resident page whose next reference is farthest in the future; it minimizes the number of page faults for any reference string and frame count, and has the stack property, but it requires complete advance knowledge of the reference stream.

## 8. Example
Reference string: `7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1`, m = 3.

**FIFO simulation:**
| Ref | 7 | 0 | 1 | 2 | 0 | 3 | 0 | 4 | 2 | 3 | 0 | 3 | 2 | 1 | 2 | 0 | 1 | 7 | 0 | 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Queue | 7 | 7,0 | 7,0,1 | 0,1,2 | hit | 1,2,3 | hit | 2,3,4 | hit | 3,4,2 | 4,2,0 | hit | hit | 2,0,1 | hit | 0,1,7 | hit | 1,7,0 | hit |
| Fault? | F | F | F | F | – | F | – | F | – | F | F | – | – | F | – | F | – | F | – | – |

Faults: refs 1,2,3,4,6,8,10,11,14,16,18 = **15 faults**. (Standard result for this string.)

**Optimal simulation (m=3):**
- Track next-use distances; evict farthest.
- Result: **9 faults** (Silberschatz). Note page `7` (next used at position 18) and `0` (used often) survive; `2` at position 8 is the farthest → evicted etc.

Also test m=4 for FIFO: fault count rises to 16 for the same string → **Belady's anomaly demonstrated** (15 → 16 when adding a frame).

## 9. Internal Working
**FIFO:**
1. Process start → resident set empty.
2. On miss with free frame: enqueue; set PTE present.
3. On miss, full: `victim = dequeue()`; if victim dirty → writeback; clear PTE, TLB flush; enqueue new page; install PTE.
4. Hits: no queue changes.

**Optimal (offline):**
1. Pre-scan the reference string, building, for each page, the ordered list of its future reference positions.
2. At each full miss, choose the resident page with the *max* next-position; ties → any.
3. Count faults; the total is the minimum for that string and m.

## 10. Time Complexity
- FIFO: **O(1)** per reference (queue ops). Space O(m).
- Optimal: O(n·m) offline (scan per eviction decision), or O(n + m·k) with precomputed next-use lists; must read the whole future — not implementable online.
- Fault-count computation for evaluation: O(n) with a table of next uses.
- Memory of FIFO: O(m); Optimal evaluation: O(n) future table.

## 11. Advantages
- **FIFO**: O(1), zero hardware support, trivially correct, predictable ordering; useful as a building block (e.g., the "oldest entry" candidate in multi-list designs).
- **Optimal**: provably minimal faults — the gold standard for evaluation; its analysis reveals *why* recency matters (the farthest-next-use page is usually a recently-referenced-but-not-recent page).

## 12. Disadvantages
- **FIFO**: Belady's anomaly (more memory can hurt); evicts hot pages; poor for locality-heavy workloads.
- **Optimal**: impossible to implement (needs the future); offline only; evaluation cost high for huge strings.

## 13. Interview Questions
1. **Q: Explain FIFO replacement.** A: Evict the page that's been in the resident set longest — a queue; O(1), no hardware needed, but recency-blind.
2. **Q: What is Belady's anomaly?** A: Increasing the number of frames can *increase* page faults for FIFO (and any non-stack algorithm); the classic counterexample is the `7 0 1 2 0 3 0 4 …` string where m=3 → 15 faults and m=4 → 16 faults.
3. **Q: Why does Belady's anomaly happen?** A: FIFO's victim depends only on arrival time; a page evicted with 3 frames might have been a "safe early victim" that gets pulled into the set at a bad moment with 4 frames, displacing a page that's needed immediately.
4. **Q: What is the Optimal (MIN) algorithm?** A: Evict the page whose next use is farthest in the future; it minimizes faults for any string/frame count but requires oracle knowledge — evaluation-only.
5. **Q: How do we use Optimal in practice? (Tricky)** A: As the benchmark: run any algorithm on a reference string and compare its fault count to Optimal's minimum — e.g., LRU on the textbook string gives 12 vs Optimal 9, so LRU is within 33% of optimal there.
6. **Q: Which of FIFO/LRU/Optimal have the stack property?** A: Optimal and LRU (more frames never hurts); FIFO does not (Belady's anomaly is the proof).
7. **Q: Can a real OS use Optimal for a *known* access pattern? (Scenario)** A: Sometimes approximated — e.g., databases with query plans may know future page access (buffer preload); Linux readahead predicts sequential patterns (a form of lookahead), but general-purpose Optimal is impossible.
8. **Q: What's the memory overhead of FIFO?** A: O(m) queue plus per-page position — minimal; that's its appeal for hardware/network caches.
9. **Q: Why is Optimal still taught if it's unusable?** A: It defines the achievable lower bound, forces rigor in algorithm evaluation, and its "farthest-next-use" principle motivates LRU/Clock designs.
10. **Q: When might FIFO actually beat LRU? (Tricky)** A: For purely sequential/streaming access (scan a large array once), FIFO's behavior ≈ LRU and it's simpler; or when the access pattern is "FIFO itself" (queue-like workloads). In general LRU/Clock win on locality.

## 14. Follow-Up Questions
1. **Q: What's a "stack algorithm" formally?** A: One where the resident set for m frames is always a subset of that for m+1 frames — implies no Belady anomaly; LRU, OPT, LFU-stack variants qualify.
2. **Q: How does Clock improve on FIFO?** A: Clock gives each page a "second chance" via the reference bit — a FIFO hand plus a recency check — effectively a cheap LRU approximation (Section 04).
3. **Q: What is the refault-distance framework?** A: Linux's way to tell how "cold" an evicted page was; used to decide whether to grow the file cache — a modern successor to the Optimal's future-distance intuition.
4. **Q: How do you compute the minimum faults (OPT) for a string efficiently?** A: Precompute each page's next-use index; at each eviction pick the max next-use among residents — O(n·m) or O(n) with a next-use heap.

## 15. Coding Example
```c
// FIFO simulator that prints Belady's anomaly (faults for m=3 and m=4)
#include <stdio.h>

int fifo_faults(int *refs, int n, int m) {
    int queue[64], head = 0, tail = 0, present[16] = {0}, faults = 0;
    for (int i = 0; i < n; i++) {
        if (present[refs[i]]) continue;
        faults++;
        if (tail - head < m) {            // free frame
            queue[tail++] = refs[i]; present[refs[i]] = 1;
        } else {                          // evict head
            int victim = queue[head++];
            present[victim] = 0;
            queue[tail++] = refs[i]; present[refs[i]] = 1;
        }
    }
    return faults;
}

int main(void) {
    int refs[] = {7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1};
    int n = sizeof refs / sizeof *refs;
    printf("FIFO m=3: %d faults\n", fifo_faults(refs, n, 3));   // 15
    printf("FIFO m=4: %d faults\n", fifo_faults(refs, n, 4));   // 16 -> Belady's anomaly
    return 0;
}
```

## 16. Industry Usage
- **Linux**: FIFO-ish "inactive list" feeding the LRU active list (mm/vmscan.c) — arrival-order staging with recency promotion; readahead queues are FIFO.
- **Networking**: TCP small buffers, NIC ring buffers, and hardware FIFO caches use FIFO (cheap, bounded).
- **Databases**: SQL Server's "LRU-K" / InnoDB read-ahead; FIFO appears in prefetch queues.
- **Research/eval**: OPT is the universal benchmark in OS/cache papers; CDN providers quote hit-ratio vs OPT in their literature.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 9.4.1 (FIFO), 9.4.2 (Optimal), Figure 9.16 (Belady's anomaly).
- Belady, L. "A Study of Replacement Algorithms for a Virtual-Storage Computer", IBM Systems Journal, 1966.
- Tanenbaum, *Modern Operating Systems*, Ch. 3.7.
- Linux: `mm/vmscan.c`, `Documentation/admin-guide/sysctl/vm.rst`.
- Denning, "Working Sets Past and Present" (IEEE TSE 1980).

## 18. Cheat Sheet
- FIFO = evict oldest-arrived page; queue; O(1); recency-blind.
- Belady's anomaly: FIFO m=3→15, m=4→16 faults on the textbook string.
- Optimal/MIN = evict farthest-next-use; minimal faults; oracle required.
- Stack property ⇒ no anomaly: LRU & OPT; FIFO lacks it.
- Textbook string faults: FIFO 15, LRU 12, OPT 9 (m=3).
- Optimal is the benchmark, never a production policy.
- FIFO survives as a building block (inactive list, NIC queues).
- Refault-distance (Linux) is a modern cousin of future-distance intuition.

## 19. Quiz
1. FIFO evicts:
   a) least-recently-used b) oldest-arrived c) least-frequent d) random → **b**
2. Belady's anomaly means:
   a) more frames always help b) more frames can hurt (FIFO) c) LRU fails d) OPT fails → **b**
3. Which has the stack property?
   a) FIFO b) Optimal c) neither d) both FIFO & OPT → **b**
4. OPT evicts the page whose next use is:
   a) nearest b) farthest c) unknown d) zero → **b**
5. Textbook string m=3: OPT gives ___ faults.
   a) 9 b) 12 c) 15 d) 16 → **a**
6. FIFO is O(___):
   a) n b) m c) 1 d) log m → **c**

## 20. Flashcards
- **Q: FIFO victim?** → **A:** Oldest page in the resident set (arrival order).
- **Q: Belady's anomaly?** → **A:** FIFO fault count can rise with more frames.
- **Q: OPT victim?** → **A:** Page whose next use is farthest in the future.
- **Q: Can OPT be implemented?** → **A:** No — needs the future; it's the evaluation benchmark.
- **Q: Stack-property algorithms?** → **A:** LRU and OPT; FIFO is not.
- **Q: Textbook string (m=3) fault counts?** → **A:** FIFO 15, LRU 12, OPT 9.

## 21. Revision
FIFO is the O(1) arrival-order policy: evict the oldest page. It's simple but recency-blind — the classic Belady's anomaly (m=3→15, m=4→16 faults on `7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1`) proves more frames can hurt non-stack algorithms. Optimal (MIN) evicts the page whose next use is farthest — minimal faults by definition (9 on that string) but requires oracle knowledge, so it's the benchmark every algorithm is measured against. LRU splits the difference: recency approximates future use with the stack property, which is why systems approximate LRU with Clock/aging (Section 04).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Explain FIFO replacement." | 2 How / 13 Q1 |
| "What is Belady's anomaly?" | 8 Example / 13 Q2-3 |
| "What is Optimal replacement?" | 7 Formal / 13 Q4 |
| "How do we use Optimal in evaluation?" | 13 Q5 / 3 When |
| "Which algorithms avoid the anomaly?" | 13 Q6 / 7 Formal |
| "When does FIFO beat LRU?" | 13 Q10 / 4 Alternative |
