# Disk Structure and Disk Scheduling Algorithms

> **TL;DR**: HDDs serve requests with a moving head, so **seek time** and **rotational latency** dominate; the disk scheduler orders the request queue — FCFS (fair, slow), SSTF (fast, starvation-prone), SCAN/elevator, C-SCAN, and C-LOOK — to minimize total head movement and maximize throughput.

## 1. Why Does This Exist?
A spinning disk's head must physically move to a cylinder (seek), wait for the platter to rotate under it (rotational latency), then transfer. A random-access workload can spend 90%+ of its time seeking. Disk scheduling exists to reduce that waste: by reordering the pending request queue, the scheduler minimizes total head travel and exploits locality — the difference between a disk that serves 200 IOPS and one that serves 2000 IOPS on the same hardware. It also exists to provide fairness (don't let one far request starve everyone) and to be *correct* (never lose or reorder dependent I/O).

## 2. How Does It Work?
The OS/controller keeps a queue of pending requests `(cylinder, sector, direction)`. On each decision it picks the next request per policy:
- **FCFS**: serve in arrival order — fair, no starvation, but head bounces = worst throughput.
- **SSTF (Shortest Seek Time First)**: serve the request closest to the current head — great total movement, but *starvation*: a steady stream of nearby requests can postpone far ones forever.
- **SCAN (elevator)**: head sweeps from one end to the other, serving everything in its path, then reverses. Fair-ish, bounded wait, good throughput.
- **C-SCAN (circular)**: sweep in one direction only, then jump back to the start (the "wrap"). More uniform wait times; the return sweep serves nothing.
- **LOOK / C-LOOK**: like SCAN but only sweeps as far as the outermost/innermost *requests* (no empty travel). Best practical variants.
Modern HDDs add **NCQ** (Native Command Queuing): the drive itself reorders commands (SATA/AHCI), so the OS scheduler's job is mostly done at higher levels; NVMe queues push further.

## 3. When Is It Used?
- **Classic OS schedulers**: Linux has `deadline`, `cfq` (CFQ — fairness), and `mq-deadline`/`none` for SSDs; macOS/Windows have variants. HDDs use elevator-like policies.
- **Databases**: know your scheduler — deadline/NOOP choices affect random-vs-sequential mix.
- **Legacy/embedded**: RTOS disk schedulers with real-time ordering (EDF variants for deadline guarantees).
- **NCQ**: hardware-side reordering on SATA drives; the OS only feeds a well-ordered-ish queue.
- **Filesystems**: `noatime`, sequential readahead, and journal placement all reduce seek load *before* the scheduler sees requests.

## 4. Why Wasn't Another Approach Chosen?
- **FCFS (rejected as default)**: no starvation but terrible throughput; fine for tiny queues.
- **SSTF (rejected)**: near-optimal seek but unbounded starvation (no fairness guarantee).
- **SCAN family (chosen for HDDs)**: bounded waiting (each request served within ~2 sweeps), no starvation, near-SSTF movement — the best practical trade.
- **EDF/priority**: needed for real-time; overkill for general I/O.
- **Random order**: unpredictable latency — rejected.
- **"No scheduling" on SSDs (chosen)**: SSDs have no seek — the OS uses `none`/`noop` and lets NVMe queue management + FTL handle ordering (Section 03).

## 5. Intuition
An **elevator** in a building: to serve every floor efficiently, it doesn't go to the closest floor each time (SSTF — would ping-pong forever) — it goes up, stopping at every requested floor, then down (SCAN). Requests "in the direction of travel" get served; a request one floor up is delayed only until the elevator reaches it. That's why SCAN is called the *elevator algorithm*: it's literally the real-world optimal policy for a moving head.

## 6. Real-World Analogy
A **letter carrier** on a street: FCFS = deliver each letter as it arrives, running back and forth across town (exhausting). SSTF = always deliver to the nearest house (fast now, but the far houses never get mail — starvation). SCAN = walk the street end-to-end, delivering to every house in order, then turn around — everyone gets served within one or two passes.

## 7. Formal Definition
Disk scheduling orders a queue of pending requests to minimize head-movement cost (seek time) subject to fairness and latency constraints. **FCFS** preserves arrival order. **SSTF** selects the request minimizing |current − target| cylinder distance. **SCAN** moves the head monotonically across the cylinder range, servicing requests encountered, reversing at the boundary; **C-SCAN** serves only one direction and wraps, equalizing response times; **LOOK/C-LOOK** reverse at the last request rather than the physical boundary. Seek time is the dominant cost (plus rotational latency), approximated by a linear function of distance (modern drives: piecewise).

## 8. Example
Disk 200 cylinders (0–199). Head starts at 53. Queue: `98, 183, 37, 122, 14, 124, 65, 67`. Compute total seek distance (the standard Silberschatz example):

**FCFS** (in order): |53−98|+|98−183|+|183−37|+|37−122|+|122−14|+|14−124|+|124−65|+|65−67|
= 45+85+146+85+108+110+59+2 = **640 cylinders**.

**SSTF** (closest first): 53→65(12)→67(2)→37(30)→14(23)→98(84)→122(24)→124(2)→183(59) = **236 cylinders**. (Much less movement — but note 183 was served last; a continuous stream near 100 would starve 183.)

**SCAN** (to 199 then reverse, serving in path): 53→65→67→98→122→124→183→199 → reverse → 37→14. Distance = (199−53) + (199−14) = 146 + 185 = **331 cylinders** (196 for the outbound sweep + 162 inbound... compute: 53→199 = 146; 199→14 = 185; total **331**).

**C-SCAN** (one direction + wrap): 53→...→199 (146), wrap to 0 (199), 0→14→37 = 14+37=51; total 146+199+51 = **396**.

**C-LOOK** (C-SCAN but only between requests): 53→...→183 (130), wrap to 14 (169), 14→37 (23) = 130+169+23 = **322**.

Note: SCAN/C-SCAN assume sweep to the boundary; LOOK variants stop at the last request — in practice the numbers differ per implementation. The lesson: SSTF minimizes movement; SCAN guarantees fairness; FCFS is the worst.

## 9. Internal Working
1. Requests arrive → elevator queue (per-disk `struct request_queue`).
2. Scheduler classifies (read/write, priority, deadline) and merges adjacent requests (plugging/merging — Linux `blk_plug` batches).
3. `__blk_mq_run_hw_queue` issues the next request per policy.
4. NCQ/AHCI lets the drive reorder within its command queue; the OS can submit multiple.
5. On completion, DMA delivers data to the page cache; the FS I/O completes.
6. Modern Linux: `mq-deadline` (fifo batches + writes-starve-reads protection) for HDDs, `none` for NVMe.

## 10. Time Complexity
- FCFS: O(1) per request (queue order).
- SSTF: O(n) per request (scan for min distance), or O(log n) with a sorted tree.
- SCAN/C-SCAN/LOOK: O(n) worst per request with a linear queue; O(log n) with a balanced tree (Linux uses rbtrees).
- Total seek distance: FCFS O(n²)-ish worst over n requests; SSTF near-O(n log n); SCAN O(C) per sweep (bounded by cylinders).
- NCQ reordering: hardware, bounded by queue depth (typically 32).

## 11. Advantages
- **SSTF**: minimal total head movement — best raw throughput.
- **SCAN/C-SCAN**: bounded wait (≤ ~2 sweeps) → no starvation; good fairness.
- **LOOK/C-LOOK**: avoids empty travel — the practical production choice.
- **NCQ**: adds hardware-level reordering for free.
- **Plugging/merging**: reduces queue depth and seeks (Linux `blk_plug`).

## 12. Disadvantages
- **FCFS**: poor throughput on random workloads.
- **SSTF**: unbounded starvation (fairness).
- **SCAN**: long tail waits for requests behind the head's turn point; C-SCAN's wrap adds a large empty seek.
- All: assume seek cost dominates — **irrelevant on SSDs** (Section 03).
- Software scheduling can't know about hidden reordering inside the drive (NCQ/FTL), so "optimal" OS order isn't what the drive actually does.

## 13. Interview Questions
1. **Q: Why does disk scheduling exist?** A: HDD access is dominated by seek (moving the head) + rotational latency; reordering the request queue minimizes head movement → dramatically higher throughput with the same hardware.
2. **Q: Compare FCFS, SSTF, SCAN, C-SCAN.** A: FCFS fair but slow (640 cylinders in the classic example); SSTF minimal movement (236) but starves far requests; SCAN sweeps both ways (331, bounded wait); C-SCAN sweeps one way + wrap (396, uniform waits); LOOK variants skip empty travel.
3. **Q: What is the elevator algorithm?** A: SCAN: move the head monotonically, serving requests in the path, reverse at the boundary — literally how a building elevator serves floors; bounded wait, no starvation.
4. **Q: What's the difference between SCAN and LOOK?** A: SCAN sweeps to the physical cylinder boundary; LOOK reverses at the last pending request — skipping empty travel (C-LOOK = circular version).
5. **Q: What is starvation and which algorithm suffers it?** A: SSTF — a continuous stream of nearby requests can indefinitely postpone a far request; SCAN/LOOK bound the wait to ~one sweep.
6. **Q: What is NCQ? (Tricky)** A: Native Command Queuing: the drive itself reorders commands (SATA/AHCI, queue depth ~32); the OS scheduler's ordering is advisory at the hardware level — the real order is the drive's choice.
7. **Q: Why is disk scheduling largely obsolete on SSDs?** A: No head, no seek, no rotation — access time is uniform; the OS uses `none`/`noop`/`mq-deadline` and NVMe queue management handles ordering (Section 03).
8. **Q: How does the OS combine scheduling with merging/plugging?** A: Linux batches requests (`blk_plug`), merges adjacent sectors, and lets the scheduler (deadline/cfq/none) order them — reducing both seeks and interrupts.
9. **Q: Which scheduler for a database on HDDs?** A: `deadline`/`mq-deadline` — it batches reads and gives writes a deadline, protecting reads (latency-sensitive) from write floods. For NVMe: `none`.
10. **Q: What's the difference between rotational latency and seek time?** A: Seek = head movement to the cylinder (ms, dominant); rotational latency = time for the target sector to reach the head after seek (half a rotation on average: ~4 ms at 7200 RPM).
11. **Q: How does the elevator algorithm relate to CPU scheduling?** A: Conceptually the same "serve the queue in one direction, then reverse" fairness idea — SCAN is taught as the I/O cousin of fair CPU scheduling.
12. **Q: What is the "access time" formula?** A: Access = seek + rotational latency + transfer. For a 7200 RPM drive: ~8 ms seek + ~4 ms rotation + ~0.2 ms transfer ≈ 12 ms per random I/O → ~80 IOPS; SSDs: ~0.1 ms (µs latency).

## 14. Follow-Up Questions
1. **Q: What is the `cfq` scheduler?** A: Complete Fairness Queuing — per-process I/O fairness (round-robin time slices); the old Linux default, replaced by mq-deadline for simplicity.
2. **Q: What is I/O scheduling on NVMe?** A: NVMe has deep hardware queues (up to 64K) and no seek — the OS mostly forwards; `none`/`noop` is the default; `blk-mq` multipath matters more.
3. **Q: What's the difference between a "seek" and a "short seek"?** A: Drives have a piecewise seek profile: short seeks are cheaper per cylinder; long seeks (many cylinders) can take several ms — why SCAN helps more on scattered workloads.
4. **Q: How do filesystems reduce seek load pre-scheduler?** A: Block-group locality, sequential allocation, readahead, `noatime` — fewer and more localized requests reach the scheduler.

## 15. Coding Example
```c
// Simulate FCFS, SSTF, and SCAN seek distances
#include <stdio.h>
#include <stdlib.h>

#define N 8
int fcfs(int *r, int n, int start) {
    int dist = 0, cur = start;
    for (int i = 0; i < n; i++) { dist += abs(cur - r[i]); cur = r[i]; }
    return dist;
}

int sstf(int *r, int n, int start) {
    int done[8] = {0}, cur = start, dist = 0;
    for (int k = 0; k < n; k++) {
        int best = -1, bd = 1 << 30;
        for (int i = 0; i < n; i++)
            if (!done[i] && abs(cur - r[i]) < bd) { bd = abs(cur - r[i]); best = i; }
        dist += bd; cur = r[best]; done[best] = 1;
    }
    return dist;
}

int scan(int *r, int n, int start, int maxcyl) {
    // sweep to max, then to min, serving in path (simplified: serve all in one direction pass)
    int dist = (maxcyl - start) + (maxcyl - 0);   // outbound + return to 0
    return dist;
}

int main(void) {
    int req[] = {98, 183, 37, 122, 14, 124, 65, 67};
    printf("FCFS: %d\n", fcfs(req, N, 53));    // 640
    printf("SSTF: %d\n", sstf(req, N, 53));    // 236
    printf("SCAN(0..199): %d\n", scan(req, N, 53, 199)); // 146+199=345 (simplified)
    return 0;
}
```

## 16. Industry Usage
- **Linux**: `block/mq-deadline.c`, `block/bfq.c`, `block/blk-mq.c`, `block/blk-merge.c`; NVMe `nvme` driver queue management.
- **Windows**: Storport/port miniport scheduling; `disk` sysclass.
- **Databases**: PostgreSQL/MySQL workload tuning (deadline vs none; `random_page_cost` reflects HDD vs SSD).
- **Storage arrays**: controller-level elevator + NCQ across many spindles (EMC/NetApp-era).
- **HDD vendors**: firmware-level scheduling + NCQ + SMR shingling optimization.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 10.2 "Disk Scheduling".
- Tanenbaum, *Modern Operating Systems*, Ch. 5.5 (disk scheduling).
- Linux source: `block/mq-deadline.c`, `block/blk-mq.c`, `Documentation/block/`.
- `man 8 ionice`; `Documentation/block/queue-sysfs.rst`.
- Oracle: "Disk I/O tuning" (deadline/cfq guidelines).

## 18. Cheat Sheet
- HDD access = seek + rotation + transfer (~12 ms random).
- FCFS: arrival order, worst movement (640 on classic example).
- SSTF: nearest-first (236), but starvation.
- SCAN/elevator: sweep + reverse; C-SCAN: one direction + wrap.
- LOOK/C-LOOK: reverse at last request — production HDD choice.
- NCQ = drive-side reordering (hardware).
- SSDs: no seek → `none`/noop; scheduling obsolete.
- Linux: mq-deadline for HDDs, none for NVMe.
- Read-before-write protection and merging matter as much as ordering.

## 19. Quiz
1. The dominant HDD cost is:
   a) transfer b) seek + rotation c) cache d) DMA → **b**
2. SSTF's flaw:
   a) slow b) starvation c) complexity d) merge → **b**
3. SCAN is also called:
   a) shortest b) elevator c) circular d) batch → **b**
4. C-SCAN improves over SCAN by:
   a) less movement b) uniform wait times c) no seek d) read priority → **b**
5. LOOK vs SCAN:
   a) LOOK goes to boundary b) LOOK reverses at last request c) same d) LOOK is SSTF → **b**
6. On an SSD, the OS scheduler is usually:
   a) SCAN b) deadline c) none d) SSTF → **c**

## 20. Flashcards
- **Q: Why disk scheduling?** → **A:** Seek dominates; reordering minimizes head movement.
- **Q: FCFS vs SSTF?** → **A:** Fair but slow vs minimal movement but starves.
- **Q: What is SCAN?** → **A:** Elevator: sweep + reverse; bounded wait.
- **Q: C-SCAN?** → **A:** One direction + wrap; uniform waits.
- **Q: What is NCQ?** → **A:** Drive-side command reordering (hardware).
- **Q: Why obsolete on SSDs?** → **A:** No seek; uniform access time.

## 21. Revision
HDD I/O cost is seek + rotational latency, so the OS reorders the request queue: FCFS (fair, 640 movement), SSTF (236, starvation), SCAN/elevator (sweep + reverse, 331), C-SCAN (one-way + wrap), and LOOK/C-LOOK (reverse at last request) balance throughput and fairness; NCQ adds hardware reordering. SSDs remove seek entirely, making software scheduling mostly obsolete (`none`/noop) and shifting the story to wear leveling, TRIM, and garbage collection (Section 03). Linux uses mq-deadline for HDDs and none for NVMe — know both worlds for the "what changed?" questions.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Why does disk scheduling exist?" | 1 Why / 13 Q1 |
| "Compare FCFS/SSTF/SCAN/C-SCAN." | 8 Example / 13 Q2 |
| "What is the elevator algorithm?" | 13 Q3 / 5 Intuition |
| "SCAN vs LOOK?" | 13 Q4 / 2 How |
| "What is NCQ?" | 13 Q6 / 9 Internal |
| "Why is scheduling obsolete on SSDs?" | 13 Q7 / 12 Disadvantages |
