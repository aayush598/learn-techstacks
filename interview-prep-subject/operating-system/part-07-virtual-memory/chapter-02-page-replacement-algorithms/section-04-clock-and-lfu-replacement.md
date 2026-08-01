# Clock and LFU Replacement

> **TL;DR**: The **Clock (second-chance)** algorithm sweeps a circular list of pages, clearing reference bits and only evicting un-referenced pages — an O(1) LRU approximation that every real OS uses; **LFU** counts access frequency and evicts the least-frequently-used page — better for stable hot sets, worse for scan/recency, and usually combined with aging.

## 1. Why Does This Exist?
Exact LRU (Section 03) is too expensive; pure FIFO (Section 02) is too dumb. Clock exists as the practical middle: it needs only the hardware **reference bit**, sweeps in O(1) amortized, and gives LRU-like quality — which is why it (and its variants) became the default in production kernels. LFU exists because *frequency* is sometimes the better predictor: a page touched 100 times is more valuable than one touched once "recently." LFU is the workhorse of caches (CDN, key-value stores) where hot data is stable; the OS mostly needs LFU's *complement* — resisting cache pollution — which is why it appears as aging/hybrids rather than pure LFU.

## 2. How Does It Work?
**Clock (second-chance):**
1. Arrange resident pages in a circular list with a **hand** pointer.
2. On eviction: inspect the page under the hand:
   - reference bit **1** → clear it, advance hand (second chance).
   - reference bit **0** → evict it (replace with the new page), advance hand.
3. A full pass clears all bits; the second pass evicts — worst case O(m) per eviction, amortized O(1).
4. **Enhanced Clock**: 4 classes from (ref, dirty): (0,0) best victim → (0,1) → (1,0) → (1,1) worst. Prefer clean unreferenced victims (avoid writeback).

**LFU:**
1. Per-page counter incremented on each reference.
2. Evict the page with the smallest count (with aging: decay all counters periodically so old hot pages fade).
3. Variants: LFU with aging window; LRU-K / W-TinyLFU (recency + frequency).

## 3. When Is It Used?
- **Clock**: Linux (active/inactive lists are clock-flavored; `pagevec` reclaim), Windows working-set trimmer, macOS/XNU vm_pageout, Postgres buffer manager ("clock sweep"), InnoDB's older sweep.
- **LFU**: web caches (Varnish, CDNs), Redis (`allkeys-lfu`), database buffer managers (Oracle's early LFU-K), general cache eviction in KV stores and browser caches.

## 4. Why Wasn't Another Approach Chosen?
- **Exact LRU**: too expensive (Section 03). Clock gives ~LRU quality at O(1) — chosen.
- **FIFO**: no recency (Section 02) — evicts hot pages; Clock's reference-bit check fixes exactly this.
- **Pure LFU**: pins once-hot pages forever (a page hot yesterday evicts nothing today); and does nothing about recency — needs aging, making it expensive and tuning-heavy. Used in *user-space caches* where frequency matters more than the OS's ephemeral pages.
- **Hybrids (LRU-K, W-TinyLFU, ARC)**: best quality, but more complexity/state — used where replacement quality directly affects revenue (cache hit ratio), not in the kernel's hot path.

## 5. Intuition
**Clock** is a janitor walking a circular corridor (the clock) of rooms; each room's door shows a "cleaned recently" sign (reference bit). He walks room to room; if a sign is up, he wipes it and moves on (second chance); if no sign, he empties the room (evict). People who just used the room get their sign wiped — so recently-used rooms survive a sweep.

**LFU** is a bouncer tracking how many times each patron visited (frequency counter); at capacity, the patron with the fewest visits leaves — unless you "decay" counts over time so yesterday's regulars can leave today.

## 6. Real-World Analogy
- **Clock**: a parking lot valet with a rotating clipboard. Each car gets a chalk mark when driven. On a full lot, he walks the list; marked cars get erased (another chance), unmarked cars get towed. He always circles the same list — O(1) average.
- **LFU**: a coffee shop's loyalty program: the person with the fewest stamps leaves the waiting list when it's full. Pure LFU lets someone with 100 old stamps block newcomers forever — so the shop expires stamps monthly (aging).

## 7. Formal Definition
The **Clock (second-chance) algorithm** maintains resident pages on a circular list; a hand pointer cycles through pages, clearing the reference bit of referenced pages and evicting the first page found with the reference bit clear (or, in enhanced form, choosing victims by (reference, dirty) class with clean-unreferenced preferred). Its amortized cost is O(1) per eviction; it is an LRU approximation that requires only the hardware reference bit. **LFU (Least Frequently Used)** evicts the page with the lowest access count, where counts are typically decayed (aged) to handle changing workloads; it models *stable frequency* better than recency, at the cost of more state and a susceptibility to cache pollution from historical hits.

## 8. Example
**Clock** with 4 frames, reference bits shown as (page, refbit). Hand at position 0:
Current set: `[(1,1),(2,0),(3,1),(4,0)]`, hand→0.
- Evict triggered:
  - pos0: page1 ref=1 → clear → (1,0), hand→1.
  - pos1: page2 ref=0 → **evict page 2**. Insert new page 5 with ref=1 at pos1: `[(1,0),(5,1),(3,1),(4,0)]`, hand→2.
- Notice page 1 got a second chance because it was *recently referenced*; page 2 (unreferenced since last sweep) was evicted. LRU would also evict the least-recently-used; Clock approximates it using bits.

**LFU** with counters: pages A(count 50), B(45), C(3), D(100). Eviction → C (fewest). After aging (×½): A=25, B=22, D=50 — a long-idle D stays hot; a page E used 2× recently may outrank B. Tuning matters.

## 9. Internal Working
**Clock implementation:**
1. `struct page` has `PG_referenced`/`PG_active` flags; a reclaim list of pages is traversed.
2. Reclaim triggered (kswapd or direct): walk the list from `lru` hand.
3. For each page: `pte_young()`? → clear (via `ptep_test_and_clear_young`), promote; else candidate. Dirty → writeback deferred.
4. After evicting K pages (batch), hand stops; kernel retries the fault with a free frame.
5. Linux's actual design: active + inactive lists each with a hand, plus per-memcg lists — a two-speed Clock.

**LFU implementation (cache level):**
1. `freq` map page→count; increment on access (O(1) with a hash or a frequency buckets list).
2. On eviction: scan for min count (O(m)) or maintain a min-heap / frequency-of-frequency counts (O(1) amortized — the LFU "frequency counters" optimization).
3. Aging: every T window, multiply counts by a decay factor.

## 10. Time Complexity
- Clock: amortized **O(1)** per eviction (hand sweeps, each page checked ≤ twice per full cycle); worst case O(m) for a full sweep.
- Enhanced Clock: same asymptotics; adds a dirty-bit class check.
- LFU (naive min-scan): O(m) per eviction.
- LFU (frequency-list / heap): **O(1)** amortized per access and per eviction (like the "LFU cache" data-structure).
- Aging (LFU decay): O(m) per window, O(1) amortized.
- Linux reclaim batching: O(k) pages per pass with per-page O(1) work.

## 11. Advantages
- **Clock**: O(1) amortized, requires only the reference bit, LRU-approximate quality, easy to batch; no global per-access updates.
- **Clock** handles scan pollution reasonably (referenced pages survive a pass).
- **LFU**: matches workloads with stable hot sets (CDN, KV, DB hot pages); with aging, adapts to drift; its "frequency-of-frequency" structure is provably O(1).
- Both are simple to implement and tune.

## 12. Disadvantages
- **Clock**: still can evict a page right before use if its bit was cleared at the wrong moment; two-pass worst case; less precise than LRU for very hot pages.
- **LFU**: pure LFU pins historical hits (cache pollution); needs aging (tuning); more state (counters per page); not a stack algorithm in the LRU sense (counter order isn't nested by m).
- Both: dirty-page writeback still costs I/O; global policies can starve a process (allocation coupling, Section 05).

## 13. Interview Questions
1. **Q: How does the Clock algorithm work?** A: Circular list + hand pointer; on eviction, if a page's reference bit is set, clear it and move on (second chance); evict the first page with the bit clear. Amortized O(1).
2. **Q: Why is Clock preferred over exact LRU?** A: It needs only the hardware reference bit and one hand sweep — no per-access kernel bookkeeping — while approximating LRU quality.
3. **Q: What is the enhanced Clock and its 4 classes?** A: Considers (referenced, dirty): (0,0) clean-cold best victim, (0,1) clean-writeback, (1,0) referenced-cold, (1,1) referenced+dirty worst — preferring clean victims avoids writeback.
4. **Q: What is LFU and its problem? (Tricky)** A: Evict the least-frequently-used page. Problem: cache pollution — a once-hot page keeps a huge count and blocks eviction forever; fix with aging (decay) or recency hybrids.
5. **Q: How do you implement LFU in O(1)?** A: Frequency-list structure: buckets indexed by count, an array of lists, and a min-count pointer — increment moves the page to the next bucket; eviction pops the min bucket. (The classic "LFU cache" data structure.)
6. **Q: When is LFU better than LRU? (Scenario)** A: Stable, long-lived hot sets (CDN content, DB index pages, KV values): frequency is a better predictor than recency. For ephemeral/anonymous pages, recency (LRU/Clock) wins.
7. **Q: How does Linux's reclaim relate to Clock?** A: Linux uses active/inactive lists — essentially a two-speed Clock: inactive pages get a referenced-bit second chance; hits promote to active; reclaim scans inactive. No single global clock in the textbook sense.
8. **Q: What's the difference between Clock and aging?** A: Clock = one reference bit and a sweep hand; aging = per-page counters shifted periodically. Aging is finer-grained (multiple levels of recency) but costs counters; Clock is cheaper.
9. **Q: Why prefer a clean victim in Clock? (Production)** A: Evicting a dirty page requires writeback I/O before reuse (2× the stall); the (ref, dirty) classes let Clock pick clean pages when possible.
10. **Q: Can Clock suffer Belady's anomaly?** A: Clock is not a strict stack algorithm, so it can, in principle, exhibit anomaly-like behavior in degenerate cases — in practice it behaves close to LRU, which is safe.
11. **Q: How does the hand pointer get positioned?** A: It stays where the last eviction stopped and continues from there — the invariant is that pages behind the hand have been checked (bits cleared) recently, giving fairness and O(1) amortized.
12. **Q: Why do key-value stores prefer LFU/LRU-hybrids?** A: Cache hit ratio is revenue; W-TinyLFU (used by Caffeine) keeps a frequency sketch (count-min sketch) + recency to reject "one-hit wonders" — a production-grade hybrid of LFU and LRU.

## 14. Follow-Up Questions
1. **Q: What's the difference between Clock and the "second-chance" algorithm?** A: Second-chance is FIFO with a reference-bit re-queue; Clock is the circular-list implementation — the same idea, Clock removes the queue re-linking cost.
2. **Q: How does the dirty bit interact with Clock's eviction?** A: Enhanced Clock classifies (ref, dirty); dirty pages defer writeback or are written before reuse; Linux also uses the "dirty_expire_centisecs" timer to age writes.
3. **Q: What's W-TinyLFU?** A: Caffeine's policy: a count-min sketch tracks frequency cheaply, a small admission window lets new pages prove themselves, and eviction combines frequency+recency — the state of the art for user-space caches.
4. **Q: What is ARC (Adaptive Replacement Cache)?** A: ZFS/IBM's self-tuning hybrid that adaptively splits capacity between recency (LRU-like) and frequency (LFU-like) segments — no kernel uses it, but ZFS does at the block level.

## 15. Coding Example
```c
// Clock (second-chance) replacement simulator
#include <stdio.h>
#include <string.h>

#define M 4
typedef struct { int page; int ref; } Slot;
static Slot clock_slots[M];
static int hand = 0;

int find_slot(int page) { for (int i = 0; i < M; i++) if (clock_slots[i].page == page) return i; return -1; }
int free_slot(void)     { for (int i = 0; i < M; i++) if (clock_slots[i].page == -1) return i; return -1; }

void touch(int page) {
    int i = find_slot(page);
    if (i >= 0) { clock_slots[i].ref = 1; return; }     // hit -> set ref bit
    // miss
    int victim = free_slot();
    if (victim < 0) {                                     // full: clock sweep
        for (;;) {
            if (!clock_slots[hand].ref) { victim = hand; break; }
            clock_slots[hand].ref = 0;                     // second chance
            hand = (hand + 1) % M;
        }
    }
    clock_slots[victim].page = page; clock_slots[victim].ref = 1;
    hand = (victim + 1) % M;
    printf("evicted slot %d for page %d\n", victim, page);
}

int main(void) {
    for (int i = 0; i < M; i++) clock_slots[i].page = -1;
    int refs[] = {7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1};
    for (unsigned i = 0; i < sizeof refs / sizeof *refs; i++) touch(refs[i]);
    return 0;
}
```

## 16. Industry Usage
- **Linux**: `mm/vmscan.c` (active/inactive lists — clock-flavored), `mm/swap.c`, `shrinkers`; `Documentation/admin-guide/sysctl/vm.rst`.
- **Windows**: `MiClockSweep` — literally the Clock algorithm in the working-set trimmer.
- **macOS/XNU**: `vm_pageout` sweep + compression.
- **Postgres**: `clock sweep` in the buffer manager (`bufmgr.c`).
- **InnoDB**: LRU with old-block zone; older MariaDB clock sweep.
- **Caches**: Redis `allkeys-lfu`/`volatile-lfu`; Caffeine (Java) W-TinyLFU; Varnish LFU; browser cache policies.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 9.4.4.1 "Enhanced Second-Chance Algorithm", 9.4.5 "Counting-Based Page Replacement".
- Tanenbaum, *Modern Operating Systems*, Ch. 3.7 (clock).
- Corbet, "How to think about the Linux page cache" (lwn.net).
- Linux source: `mm/vmscan.c`, `mm/workingset.c`.
- `Redis` docs (eviction policies), Caffeine W-TinyLFU paper.

## 18. Cheat Sheet
- Clock = circular list + hand; clear ref bit (second chance); evict clear page; O(1) amortized.
- Enhanced Clock classes (ref,dirty): (0,0)>(0,1)>(1,0)>(1,1) — prefer clean.
- LFU = evict lowest frequency; needs aging to avoid pollution.
- O(1) LFU = frequency-list structure (buckets + min pointer).
- Linux reclaim = two-speed clock (active/inactive lists).
- Windows trimmer is literally "MiClockSweep".
- Clock ≈ LRU quality; LFU ≈ stable hot sets.
- Hybrids (ARC, W-TinyLFU) = recency + frequency, for user-space caches.

## 19. Quiz
1. Clock evicts a page whose reference bit is:
   a) 1 b) 0 c) dirty d) either → **b**
2. A page with ref bit set gets:
   a) evicted b) second chance (bit cleared) c) promoted d) swapped → **b**
3. Clock is O(___):
   a) m b) 1 amortized c) n d) log m → **b**
4. LFU's main flaw is:
   a) recency blindness b) cache pollution from history c) O(m) scan d) both b & dirty → **b**
5. Enhanced Clock's best victim class is:
   a) (0,0) b) (1,1) c) (0,1) d) (1,0) → **a**
6. Windows' working-set trimmer uses:
   a) OPT b) Clock (MiClockSweep) c) LFU d) FIFO → **b**

## 20. Flashcards
- **Q: Clock algorithm?** → **A:** Circular list + hand; second chance via reference bit; evict first clear page.
- **Q: Why Clock over LRU?** → **A:** Only needs reference bit + sweep; O(1) amortized; LRU-approximate.
- **Q: Enhanced Clock classes?** → **A:** (ref,dirty): (0,0)>(0,1)>(1,0)>(1,1), prefer clean.
- **Q: LFU's problem?** → **A:** Historical hits pin pages (pollution); fix with aging/hybrids.
- **Q: O(1) LFU structure?** → **A:** Frequency buckets + min-count pointer.
- **Q: Where's Clock used?** → **A:** Linux lists, Windows MiClockSweep, Postgres bufmgr.

## 21. Revision
Clock is the production answer: a circular list with a hand pointer; referenced pages get their bit cleared (second chance) and the first un-referenced page is evicted — LRU-approximate at O(1) amortized using only the hardware reference bit, refined by (ref, dirty) classes that prefer clean victims. Linux's active/inactive lists are a two-speed clock; Windows uses MiClockSweep; Postgres clocks its buffer pool. LFU counts frequency and evicts the least-used, but historical hits cause pollution — so production LFU decays counters (aging) or hybridizes with recency (ARC, W-TinyLFU). Together they span the spectrum from "cheap LRU-ish" (kernel) to "precise hot-set tracking" (caches).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Explain Clock/second-chance." | 2 How / 13 Q1-2 |
| "Enhanced Clock classes?" | 13 Q3 / 8 Example |
| "What is LFU and its flaw?" | 13 Q4 / 12 Disadvantages |
| "O(1) LFU data structure?" | 13 Q5 / 9 Internal |
| "When is LFU better than LRU?" | 13 Q6 / 3 When |
| "How does Linux do it?" | 13 Q7 / 16 Industry |
