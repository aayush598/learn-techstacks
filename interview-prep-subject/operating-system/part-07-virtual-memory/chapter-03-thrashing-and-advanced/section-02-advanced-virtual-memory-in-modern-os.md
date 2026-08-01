# Advanced Virtual Memory in Modern OS

> **TL;DR**: Modern OSes industrialize the textbook VM: **kswapd** reclaims proactively, the **OOM killer** is the last resort, **THP/hugetlbfs** use huge pages, **KSM** dedups, **zswap/zram** compress evicted pages, and **madvise/mincore/PSI** give apps and operators the observability and control that make all of Part 07 actually run.

## 1. Why Does This Exist?
The textbook algorithms (Chapters 01–02) are correct but naive: they don't survive production. Modern VM exists because real systems need *predictive* reclaim (don't wait for faults), *scalable* structures (thousands of processes, cgroups), *compression* as a stopgap between RAM and disk, *deduplication* to reclaim identical pages, and *observability* (PSI) so operators can act before collapse. Each feature answers a specific production failure: kswapd answers "direct reclaim stalls user processes"; the OOM killer answers "unreclaimable memory"; THP answers "TLB misses on big heaps"; zswap answers "swap is too slow on SSD-latency budgets"; KSM answers "a fleet of VMs runs the same kernel/libc pages."

## 2. How Does It Work?
- **kswapd**: a kernel thread that wakes when free memory drops below a **watermark** (`low`), reclaims pages until it reaches `high`, sleeping otherwise — proactive, amortized, off the fault path.
- **Direct reclaim**: when kswapd can't keep up, the *faulting process* reclaims synchronously (`alloc_pages` → `try_to_free_pages`) — slow, but guarantees progress.
- **OOM killer**: when reclaim yields nothing, `oom_kill()` scores processes (`oom_score` ∝ memory, priority, runtime) and SIGKILLs the worst — the last resort.
- **THP/hugetlbfs**: `khugepaged` scans for mappable 2 MB regions (`THP`), or apps reserve `hugetlbfs` explicitly — fewer PTEs, fewer TLB misses.
- **KSM**: scans anonymous pages, finds identical ones (via content hashing), merges them via COW → one frame shared by many processes (VMs).
- **zswap/zram**: compressed pages held in RAM before/without hitting disk — CPU for I/O trade.
- **madvise/mincore/PSI**: hints (MADV_DONTNEED/FREE/RANDOM/SEQUENTIAL), occupancy queries (mincore), and pressure metrics (PSI) for apps/operators.

## 3. When Is It Used?
- **Always** on Linux/Windows/macOS: the reclaim paths run constantly; kswapd ticks every few seconds.
- **VMs/cloud**: KSM in multi-VM hosts; THP for JVM/database workloads; cgroup limits for containers; PSI for autoscalers.
- **Databases**: THP off or on depending on workload; huge pages for large buffer pools; `madvise` for sequential/random file access.
- **Embedded/mobile**: zram instead of disk swap (flash wear, latency); low-memory killer (Android's LMKD) as the OOM equivalent.
- **Research/memory profiling**: mincore/pagemap/smaps to understand RSS and page placement.

## 4. Why Wasn't Another Approach Chosen?
- **Wait-for-fault reclaim (direct-only, rejected)**: fault-time stalls — kswapd's proactivity exists precisely to avoid this.
- **Never kill (rejected)**: without OOM, the kernel livelocks reclaiming; killing (or `cgroup` OOM) is the sane worst case.
- **4 KB pages only (rejected)**: TLB pressure at scale → huge pages; THP's downside (more memory, COW costs) is why it's optional/tunable.
- **Disk swap only (rejected)**: SSD wear + ms-latency → zswap/zram compression first.
- **No dedup (rejected for VMs)**: identical guest pages waste RAM; KSM reclaims it cheaply enough.
- **Black-box (rejected)**: without PSI/mincore, nobody could tune — observability became a feature.

## 5. Intuition
A well-run hotel: a **concierge (kswapd)** keeps a few rooms always free by quietly cleaning early, so guests never wait at the desk. When a rush hits, guests help clean (direct reclaim — slow but functional). If a guest refuses to check out (unreclaimable), security physically removes the worst offender (OOM killer). Meanwhile, the hotel compresses luggage storage (zswap), shares identical room layouts (KSM), and posts live occupancy telemetry (PSI) so the manager can act before the lobby floods.

## 6. Real-World Analogy
- **kswapd =** a supermarket restocking shelves before they're empty so customers never hit an empty aisle mid-shopping.
- **OOM killer =** the bouncer who removes the biggest problem at closing time because you can't just let the club exceed capacity.
- **THP =** serving large platters instead of hundreds of small plates (fewer trips/TLB entries) — but wasteful if each table eats little.
- **zswap =** a compressible vacuum-storage closet: squeeze what you can't keep out before renting expensive off-site storage (disk).
- **KSM =** a chain restaurant using one shared kitchen recipe book instead of printing identical copies per location.

## 7. Formal Definition
Modern virtual-memory management augments demand paging with: **background reclaim** (kswapd, watermark-triggered) and **direct reclaim** (synchronous, in the fault path); **out-of-memory handling** (score-based victim selection and termination) when reclaim is impossible; **large pages** (transparent huge pages, hugetlbfs) to reduce page-table depth and TLB misses; **page deduplication** (KSM) for identical anonymous pages; **compressed swap** (zswap/zram) to defer disk I/O; and **pressure-stall information (PSI)** quantifying time lost to memory pressure. Together they implement the working-set/thrashing controls (Chapter 03 Sec 01) in a production-safe, observable, tunable form.

## 8. Example
A server running 20 containers, 128 GB RAM, cgroup limits:
- Free memory crosses `low` watermark → **kswapd** wakes, reclaims ~1 GB of cold file pages (drop clean file cache — free); anon pages are compressed via **zswap** when swap is configured.
- A JVM allocates a 64 GB heap → THP merges 4 KB pages into 2 MB pages → TLB misses drop (heap access is dense).
- Two identical containers run the same JVM classes → **KSM** merges their shared class pages → 40% anon dedup.
- A container exceeds `memory.max` → the kernel reclaims inside it; on failure, the *container's* OOM killer fires, killing its worst process (not a global one) — the host survives.
- Operator sees `/proc/pressure/memory` climbing → raises memory limits or scales out before any user impact.

Concrete reclaim numbers: 128 GB RAM, cold file cache ~60 GB. kswapd at `low` watermark reclaims to `high`: typically hundreds of MB to a few GB per pass, amortized — the fault path almost never pays.

## 9. Internal Working
1. **Watermark machinery**: `min`/`low`/`high` per zone; `wakeup_kswapd` on allocation when free < low.
2. **Reclaim**: `shrink_node` walks per-memcg LRU lists (anon+file), `shrink_slab` for kernel caches; writeback via `flusher` threads; batch of k pages, throttle via `balance_dirty_pages`.
3. **OOM**: `out_of_memory()` computes scores (`oom_badness`), selects worst, `oom_kill_process` → SIGKILL, memory freed.
4. **THP**: `khugepaged` scans VMAs for regions to collapse into 2 MB PMD mappings; allocation on fault for `THP=madvise` targets.
5. **KSM**: `ksmd` scans candidate anonymous pages, hashes content, matches identical, `merge_across_nodes` → COW share.
6. **zswap**: on swap-out, compress; store compressed page in RAM; write through to disk only under pressure; decompress on swap-in.
7. **PSI**: tracks average memory-pressure stalls per time window; exports `/proc/pressure/memory`.
8. **cgroup v2**: per-group watermarks/limits; `memory.high` throttles, `memory.max` hard-caps → group-local OOM.

## 10. Time Complexity
- kswapd reclaim pass: O(pages scanned) — bounded by batch/watermark; amortized O(1) per allocation.
- Direct reclaim: O(pages scanned) synchronous — the cost users pay when kswapd lags.
- THP collapse: O(region pages) per scan, background (khugepaged) — doesn't stall the fault path.
- KSM: O(unique page contents) per scan with hashing — CPU-hungry, tuned via `pages_to_scan`/`sleep_millisecs`.
- zswap: O(page) compress (hardware LZO/zstd possible) — CPU cost traded for I/O; swap-in decompress O(page).
- PSI: O(1) per tick with exponential moving averages.

## 11. Advantages
- **Proactive** (kswapd) keeps the fault path fast; no user-process stalls for routine reclaim.
- **OOM management** bounds failures; cgroup-local OOM isolates blast radius.
- **Huge pages** cut TLB misses and page-table depth for large heaps (5–20% perf wins reported for DBs/JVMs).
- **Dedup** reclaims identical VM/container pages (significant in fleets).
- **Compression** makes swap survivable (zram on Android = no disk swap).
- **Observability** (PSI, smaps, mincore, pagemap) makes tuning scientific.

## 12. Disadvantages
- **Complexity/tuning**: watermarks, swappiness, THP policies, KSM CPU cost — each a foot-gun.
- **THP costs**: COW on huge pages copies 2 MB; memory waste for sparse heaps; some apps turn it off.
- **KSM CPU overhead** (hashing, scanning) — not free; tuned conservatively.
- **zswap CPU** for compression/decompression; compressed pages still occupy RAM.
- **OOM is destructive**: cgroup-local is safer, but global OOM can kill innocent services without limits.
- **Observability overhead**: PSI accounting and smaps scans cost some CPU.

## 13. Interview Questions
1. **Q: What is kswapd and why does it exist?** A: A background kernel thread that reclaims pages when free memory falls below the `low` watermark, returning it to `high` — so the fault path rarely pays for reclaim (proactive vs direct).
2. **Q: What's the difference between direct and background reclaim?** A: Direct reclaim runs in the faulting process (synchronous, stalls the app); kswapd runs in a thread (asynchronous, amortized). Direct happens when kswapd can't keep up.
3. **Q: When does the OOM killer fire and how does it choose victims?** A: When reclaim can't free enough for an allocation; it scores processes (`oom_score` — memory use, priority, runtime, cgroup) and SIGKILLs the worst. cgroup limits make it group-local.
4. **Q: What are transparent huge pages and their trade-off? (Tricky)** A: THP auto-promotes 4 KB to 2 MB mappings (`khugepaged`); fewer TLB misses and page-table entries, but COW copies 2 MB, memory waste for sparse heaps, and fragmentation pressure — hence `always/madvise/never` policies.
5. **Q: What is KSM?** A: Kernel Samepage Merging — scans anonymous pages, merges identical ones via COW so many processes/VMs share one frame; saves RAM in homogeneous fleets at the cost of CPU.
6. **Q: What is zswap vs zram?** A: zswap compresses evicted pages in RAM *before* writing to disk swap (defers I/O); zram is a compressed RAM block device *used as* swap — both trade CPU for I/O/latency.
7. **Q: What is swappiness and when do you tune it?** A: Bias between reclaiming anonymous (swap) vs file pages, 0–200 (Linux default 60); set low for workloads that want anon memory (databases), high when file cache matters more.
8. **Q: What is PSI?** A: Pressure Stall Information — `/proc/pressure/memory` (and cpu/io) reports the percentage of time tasks were stalled on memory — the production metric for detecting incipient thrashing.
9. **Q: How do cgroups change the OOM story? (Production)** A: `memory.high` throttles, `memory.max` hard-caps; the kernel OOM-kills *within* the group, so a misbehaving container can't kill the host — this is how containers and Kubernetes work.
10. **Q: What's the difference between RSS, PSS, and VSS?** A: VSS = virtual size (address space); RSS = resident (including shared, counted per-process); PSS = proportional share (shared pages split across users) — `smaps` exposes all; useful for capacity planning.
11. **Q: How do I make a process's memory not get swapped? (Scenario)** A: `mlock`/`mlockall` (lock pages in RAM), `MADV_DONTNEED` to drop them, set `vm.swappiness=0`/cgroup limits, or use `MADV_LOCKED`. Kernel threads and real-time need this.
12. **Q: What does `madvise(MADV_DONTNEED)` actually do?** A: Tells the kernel to drop the range's pages (unmap them) — RSS drops immediately; the next access refaults (zero-fill or file read). A programmatic "free to OS" — commonly used by allocators (jemalloc `madvise(MADV_DONTNEED)` on decommit).
13. **Q: Why might THP hurt a database? (Tricky)** A: 2 MB granularity means a large allocation with a small hot region keeps 2 MB resident (fragmentation), and COW on fork copies 2 MB per page — many DBs set `never` or `madvise`.
14. **Q: What is the `lowmemorykiller` on Android?** A: A userspace/legacy policy daemon that preemptively kills background apps based on importance + memory pressure — Android's product-specific OOM management (LMKD with PSI today).

## 14. Follow-Up Questions
1. **Q: How does `madvise(MADV_FREE)` differ from MADV_DONTNEED?** A: DONTNEED drops pages immediately (RSS drops, refault later); FREE marks pages free *lazily* (dropped only under pressure) — cheaper, better for allocators returning memory.
2. **Q: What is `mincore`?** A: Tells you which pages of a mapping are resident — used to probe fault behavior and by tools like `pcstat` (page cache status).
3. **Q: What's the relationship between THP and the TLB?** A: A 2 MB mapping uses one PTE/TLB entry instead of 512 — huge reach gains for dense heaps; the reverse (fragmentation) is why it's optional.
4. **Q: What's `memory.high` throttling vs `memory.max`?** A: high = soft limit (reclaim but don't kill; throttle allocations); max = hard (block allocation until reclaim; then OOM-kill inside the group).

## 15. Coding Example
```c
// Use madvise to drop a large temporary buffer, then observe RSS drop
#define _GNU_SOURCE
#include <stdio.h>
#include <sys/mman.h>
#include <unistd.h>
#include <string.h>

static long rss_kb(void) {
    FILE *f = fopen("/proc/self/status", "r");
    char line[128]; long kb = -1;
    while (fgets(line, sizeof line, f))
        if (sscanf(line, "VmRSS: %ld", &kb) == 1) break;
    fclose(f);
    return kb;
}

int main(void) {
    size_t n = 256UL * 1024 * 1024;                      // 256 MB
    char *p = mmap(NULL, n, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    memset(p, 'x', n);                                   // touch all pages
    printf("after touch : RSS=%ld kB\n", rss_kb());      // ~262144
    if (madvise(p, n, MADV_DONTNEED) != 0) perror("madvise");
    printf("after madvise: RSS=%ld kB\n", rss_kb());     // ~near 0
    munmap(p, n);
    return 0;
}
```

## 16. Industry Usage
- **Linux**: `mm/vmscan.c`, `mm/oom_kill.c`, `mm/huge_memory.c`, `mm/ksm.c`, `mm/zswap.c`, `drivers/block/zram/zram_drv.c`, `mm/workingset.c`, `Documentation/admin-guide/sysctl/vm.rst`, cgroup v2 (`Documentation/admin-guide/cgroup-v2.rst`).
- **Windows**: working-set manager, `MmAccessFault`, large pages, memory compression (same spirit as zram).
- **macOS**: XNU `vm_pageout`, compressed memory (`vm_compressor`).
- **Android**: LMKD + PSI; zram everywhere; `lmkd` kill thresholds.
- **Cloud/DB**: K8s memory limits + eviction thresholds; MySQL/Postgres THP guidance (`never` or `madvise`); Redis `maxmemory` policies; JVM `-XX:+UseTransparentHugePages`.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 9.6–9.7.
- Linux source: paths listed in §16; docs `Documentation/admin-guide/sysctl/vm.rst`, `Documentation/admin-guide/cgroup-v2.rst`, `Documentation/accounting/psi.rst`.
- `man 2 mmap`, `man 2 madvise`, `man 2 mincore`, `man 2 mlock`.
- Gorman, *Understanding the Linux Virtual Memory Manager*.
- lwn.net: "kswapd and the lowmem watermarks", "Transparent Huge Pages", "Zswap".

## 18. Cheat Sheet
- kswapd = proactive reclaim at watermarks; direct reclaim = in-fault last resort.
- OOM killer: score + SIGKILL; cgroup-local with limits.
- THP: 2 MB pages for TLB/PTE savings; `always/madvise/never`.
- KSM: dedup identical anon pages (VMs); CPU cost.
- zswap/zram: compressed in-RAM swap; CPU for I/O.
- swappiness: anon-vs-file reclaim bias (default 60).
- PSI: `/proc/pressure/memory` — production thrash gauge.
- RSS/PSS/VSS; smaps; mincore; MADV_DONTNEED/FREE.
- Android LMKD kills by importance + pressure.

## 19. Quiz
1. kswapd is:
   a) user thread b) background kernel reclaim thread c) OOM daemon d) swap device → **b**
2. Direct reclaim runs:
   a) in kswapd b) synchronously in the faulting process c) never d) in userspace → **b**
3. THP maps pages of size:
   a) 4 KB b) 2 MB c) 1 GB d) both b & c → **d**
4. KSM is for:
   a) file cache b) dedup identical anonymous pages c) swap d) TLB → **b**
5. zram provides:
   a) disk swap b) compressed RAM block device as swap c) page cache d) huge pages → **b**
6. PSI lives in:
   a) /proc/pressure/memory b) /proc/swaps c) /sys/fs cgroup d) both a & c → **d**

## 20. Flashcards
- **Q: kswapd vs direct reclaim?** → **A:** Background proactive thread vs synchronous in-fault reclaim.
- **Q: When does OOM fire?** → **A:** Reclaim can't satisfy an allocation; score-based SIGKILL.
- **Q: What do THP/hugetlbfs give?** → **A:** Fewer PTEs/TLB misses for dense memory (2 MB/1 GB).
- **Q: What does KSM dedup?** → **A:** Identical anonymous pages across processes/VMs (COW merge).
- **Q: zswap vs zram?** → **A:** Compress-then-defer-disk vs compressed-RAM-as-swap.
- **Q: How do you detect pressure in production?** → **A:** PSI `/proc/pressure/memory` (and cgroup memory limits).

## 21. Revision
Production VM is textbook demand paging plus industrial machinery: kswapd reclaims proactively at watermarks so faults stay cheap, direct reclaim is the synchronous fallback, and the OOM killer (cgroup-local with limits) is the bounded worst case. THP/hugetlbfs use huge pages to cut TLB misses, KSM dedups identical VM pages, zswap/zram compress evicted pages to dodge disk latency, and swappiness biases anon-vs-file reclaim. PSI (`/proc/pressure/memory`), smaps/mincore, and madvise hints give operators and apps the observability and control that turn Chapter 01–02 theory into a tunable, observable, production-grade memory system — and are the exact features interviewers probe for "senior" signal.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is kswapd and why?" | 2 How / 13 Q1-2 |
| "How does the OOM killer work?" | 13 Q3 / 9 Internal |
| "THP trade-offs?" | 13 Q4 / 13 Q13 |
| "What is KSM?" | 13 Q5 / 2 How |
| "zswap vs zram?" | 13 Q6 / 4 Alternative |
| "How do containers control memory?" | 13 Q9 / 16 Industry |
| "What is PSI?" | 13 Q8 / 18 Cheat Sheet |
