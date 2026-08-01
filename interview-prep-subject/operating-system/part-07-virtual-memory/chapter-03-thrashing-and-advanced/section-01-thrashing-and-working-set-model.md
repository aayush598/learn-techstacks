# Thrashing and Working Set Model

> **TL;DR**: **Thrashing** is the collapse where total working sets exceed RAM, so every fault evicts a page that's needed again immediately — CPU utilization plummets while the disk thrashes; the **working-set model** measures each process's true resident need so the OS can stop the spiral.

## 1. Why Does This Exist?
Replacement algorithms minimize faults *given enough frames*. But if the combined **working sets** of all processes exceed physical RAM, no algorithm can help: any page loaded is immediately needed again, so each fault forces an eviction that causes the next fault — a self-reinforcing loop. Thrashing exists as a concept because it's the *failure mode* of everything in Chapter 02: the OS must detect it (working-set model) and act (suspend/swap processes, or admit fewer). Understanding thrashing is also the interview litmus test for whether you understand that memory is a *system-wide* resource with *workload* dynamics, not just a per-process cache.

## 2. How Does It Work?
The **working set WS(t, Δ)** of a process = the pages it referenced during the last Δ references (or time window). Its size, |WS|, is the process's resident need.
- Summing |WS| over all processes gives **D = total demand**. If D > available frames → thrashing.
- **Detection**: monitor page-fault rate per process. High fault rate + low CPU utilization = thrash.
- **Cure**: 
  1. **Reduce D**: suspend/swap out a process (freeing its frames and shrinking D), or 
  2. **Increase frames**: add RAM (or reduce the resident set requirements via prefetching/locality improvements).
- The model also gives **allocation policy**: give each process exactly enough frames for its working set; adjust as the set changes.

## 3. When Is It Used?
- **Every memory-limited system**: cloud VMs, containers with cgroup limits, laptops with little RAM, mobile.
- **Operationally**: `sar -B`/`vmstat` fault counters, `mpstat` low %user + high %sy, `iostat` disk 100% — classic thrash diagnosis.
- **Admission control**: batch schedulers use working-set estimates to decide which jobs to run concurrently.
- **Databases/OLTP**: buffer pool sizing avoids DB-level "thrashing" of the buffer cache.

## 4. Why Wasn't Another Approach Chosen?
- **Ignore it (let LRU "just work")**: LRU prevents per-process anomaly but cannot prevent global thrash — the demand simply exceeds supply. Rejected.
- **Kill a process (OOM)**: works but brutal; used only as a last resort (Linux OOM killer). Working-set/suspend is gentler.
- **Suspend & swap (chosen)**: the classic cure — roll out a process whose working set doesn't fit. That's the medium-term scheduler + working-set model in action.
- **Global allocation without feedback (rejected)**: Chapter 02's global replacement gives utilization but no protection from one process's expanding working set — the model adds the *control loop*.
- **Prefetch everything (rejected)**: reading all pages removes faults but kills memory; the working set is the sweet spot between eager and demand.

## 5. Intuition
An office with a single phone line shared by N teams. Each team needs the line a certain fraction of the time (working set). If total demand > 100%, teams grab the line, get cut off, and immediately redial — nobody completes a call (thrashing). The fix: limit concurrent teams (suspend/swap) or add lines (more RAM). The "working set" is each team's real need; summing them tells you if you're over-subscribed.

## 6. Real-World Analogy
A checkout line at a supermarket with one cashier: every customer steps up, the cashier starts scanning (page in), but the customer remembers something and leaves to get it (evicted), then returns (refault) — the line moves nowhere. The store's cure: either stop letting certain customers in (suspend a process) or open another register (more RAM). The "working set" of customers = those actually mid-checkout at once.

## 7. Formal Definition
**Thrashing** is the state in which the total demand for frames (the sum of working-set sizes, D = Σ|WS_i|) exceeds the number of available frames, causing the page-fault rate to rise to the point where most of the system's time is spent servicing faults rather than executing instructions; CPU utilization collapses while paging I/O saturates. The **working set** WS(t, Δ) of a process is the set of pages referenced in the window [t−Δ, t]; the **working-set model** controls multiprogramming by tracking each process's working set and suspending/swapping processes (or adjusting their frame allocation) to keep Σ|WS| ≤ available frames, restoring useful CPU utilization.

## 8. Example
Reference string (window Δ = 10): `1 2 3 4 5 6 7 8 9 1 2 3 4 5` — pages 1..9 referenced sequentially.
- At t=10 (just referenced 1): WS = pages referenced in the last 10 references = {1,2,3,4,5,6,7,8,9} → |WS|=9.
- The working set is *growing* as the scan continues: a sequential scan has a huge working set → its working set exceeds any small frame budget → it thrashes.
- Contrast: a loop `for i: A[i] = A[i] * 2` has WS = a few pages → fits easily.

Scenario: 3 processes, |WS| = {20, 15, 25} = 60 pages total; system has 50 frames → **thrashing**. Cure: suspend process 3 (frees its working set's evictable pages, D drops to 35 ≤ 50); CPU utilization recovers. Alternatively, cgroup limit process 2 to 10 frames (forcing its working set to shrink or its owner to swap internally).

## 9. Internal Working
1. **Measure**: sample the reference bit every Δ; pages with the bit set during the window belong to WS (use a "working-set clock" or `pte_young` checks).
2. **Estimate demand D** = Σ|WS| over processes (Linux approximates via "reclaim activity" + workingset shadows).
3. **Compare to available frames**; compute the *page fault rate* (minor + major per second).
4. **Trigger**: if fault rate is high *and* CPU is starved, enter thrash management:
   - Medium-term scheduler chooses a victim process (idle, low priority, big working set).
   - Suspend it → swap out → frames return to the pool → D drops.
5. **Recovery**: fault rate falls, utilization rises; the suspended process may be resumed when D allows (or never, at operator's discretion).
6. Modern Linux equivalents: `kswapd` wakes proactively at `watermark` thresholds (reclaim *before* faulting), direct reclaim handles bursts, and the OOM killer fires only when reclaim yields nothing — the control loop industrial-grade.

## 10. Time Complexity
- Working-set window tracking: O(1) per reference (update a counter/interval); O(m) per sampling pass.
- Fault-rate monitoring: O(1) amortized (counters).
- Working-set size computation from a reference string: O(n) for the whole trace (window slides).
- Thrash cure (suspend one process): O(frames freed) + O(working set) swap I/O.
- kswapd proactive reclaim: O(k) pages per pass, k ~ watermark — bounded, amortized O(1).

## 11. Advantages
- **Detects and cures** the fundamental VM failure — turns memory into a controlled, adaptive resource.
- Working-set allocation is **proven near-optimal**: frame allocation ∝ real need beats static proportional.
- Clean **admission control**: batch schedulers use it to avoid oversubscription.
- Cheap to implement (reference bits + counters).
- Translates directly to **cloud/container policy** (limits, priorities, ballooning).

## 12. Disadvantages
- **Working-set measurement is approximate** (window Δ tuning; sampling error).
- **Suspend/swap is disruptive** — latency spikes, possible deadlock-ish waits if resumed prematurely (double-thrashing).
- Requires **global knowledge** (all processes' working sets) — coordination across cgroups/hosts is hard.
- Doesn't fix *pathological workloads* (sequential scans that genuinely need huge memory).
- On oversubscribed clouds, the "cure" may be *evicting your VM* (the OOM killer / spot reclaim) — no soft landing.

## 13. Interview Questions
1. **Q: What is thrashing?** A: The state where Σ working sets > available frames: every fault evicts a page needed immediately, so the system spends almost all its time paging and CPU utilization collapses.
2. **Q: How do you detect thrashing?** A: High page-fault rate + falling CPU utilization + saturated paging I/O (e.g., vmstat: high `si`/`so`, `%wa` up, `%user` down).
3. **Q: What is the working set model?** A: WS(t,Δ) = pages referenced in the last Δ references; its size is the process's resident need; the model keeps Σ|WS| ≤ frames and suspends processes to enforce it.
4. **Q: What's the relationship between working set and locality?** A: Locality means |WS| ≪ address space — the working set is the *observable* locality; without locality, |WS| ≈ all pages and VM fails (thrashing).
5. **Q: How do you fix thrashing? (Tricky)** A: Reduce demand (suspend/swap a process, shrink via cgroup limits) or increase supply (more RAM); then let fault rates re-equilibrate. Killing is the last resort (OOM).
6. **Q: Why does LRU not prevent thrashing?** A: LRU is a *local* policy; when global demand exceeds supply, every eviction is a bad eviction — no algorithm survives D > frames. Only admission/allocation control helps.
7. **Q: What's the difference between local thrash and system thrash?** A: A single process with |WS| > its allocation thrashes locally (its faults, others fine); system thrash is all processes (D > total) — cgroup limits convert the latter into the former, which is why containers "thrash inside their limit."
8. **Q: How does the OS measure a working set cheaply?** A: Sample the hardware reference bit each Δ window; pages referenced during the window are in WS. Linux uses `pte_young`/aging and workingset shadows instead of a full window.
9. **Q: What does the "medium-term scheduler" do?** A: It *suspends* processes (swaps them out) to reduce D when memory is tight — the operative cure for thrashing between the long-term (admission) and short-term (CPU) schedulers.
10. **Q: How do containers experience thrashing? (Production)** A: A cgroup with `memory.max` too small forces the kernel to reclaim inside the group constantly; the app's fault rate spikes — from the app's view it's "slow," from the operator's view `memory.failcnt` climbs.
11. **Q: What is the working set page fault rate model (Denning)?** A: Working-set theory connects fault rate to allocation: too few frames → high fault rate; the "working-set clock" tracks recent references to size allocations dynamically.
12. **Q: What's the difference between thrashing and simply being out of memory?** A: Out-of-memory = allocation *fails* (OOM). Thrashing = allocation succeeds but pages are immediately evicted, so the system spins faulting. Both are bad, differently diagnosable.

## 14. Follow-Up Questions
1. **Q: What is "prepaging" and how does it help?** A: Predicting and loading pages before faults (e.g., readahead) reduces fault count — helps streaming workloads, not thrash, since thrash is demand > supply.
2. **Q: How do cgroups/memory limits implement the working-set control?** A: `memory.high` throttles by reclaiming beyond a soft target; `memory.max` hard-caps and triggers OOM; fault counters let the kernel bias reclaim toward cold memcg groups.
3. **Q: What is "memory pressure" as Linux defines it?** A: A psi (Pressure Stall Information) metric quantifying time tasks waited on memory — `/proc/pressure/memory` — the production-friendly replacement for eyeballing vmstat.
4. **Q: What's the role of `vm.swappiness`?** A: It biases the kernel between reclaiming anonymous (swap) pages vs file pages — a tuning knob for the thrash boundary on particular workloads.

## 15. Coding Example
```c
// Compute working set sizes from a reference string with a sliding window Δ
#include <stdio.h>
#include <string.h>

#define NP 16
int seen[NP];

int wssize(int *refs, int n, int from, int delta) {
    memset(seen, 0, sizeof seen);
    int count = 0;
    for (int t = from; t >= 0 && t > from - delta; t--)
        if (!seen[refs[t]]) { seen[refs[t]] = 1; count++; }
    return count;
}

int main(void) {
    int refs[] = {1,2,3,4,5,6,7,8,9,1,2,3,4,5};
    int n = sizeof refs / sizeof *refs;
    for (int t = 0; t < n; t++)
        printf("t=%d ref=%d WS(Δ=5)=%d\n", t, refs[t], wssize(refs, n, t, 5));
    return 0;
}
```

## 16. Industry Usage
- **Linux**: `mm/vmscan.c` (reclaim), `mm/workingset.c` (refault distance, workingset shadows), PSI (`/proc/pressure/memory`), OOM killer (`mm/oom_kill.c`), cgroup v2 memory controllers.
- **Windows**: working-set manager + `SysMain` (SuperFetch) — prediction to avoid thrash.
- **macOS/XNU**: `vm_pageout` + memory compressor.
- **Cloud**: AWS/GCP/OVH memory oversubscription, spot instances reclaimed via pressure signals; Kubernetes `memory` requests/limits + node-level eviction thresholds.
- **Databases**: Postgres `shared_buffers` sizing vs OS cache — DB-level "thrashing" of buffers is tuned the same way.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 9.6 "Thrashing" (working-set model, working-set & page-fault rate, page-fault frequency).
- Denning, P. "The Working Set Model for Program Behavior" (CACM 1968); "Working Sets Past and Present" (1980).
- Tanenbaum, *Modern Operating Systems*, Ch. 3.8 "Thrashing".
- Linux: `Documentation/admin-guide/sysctl/vm.rst`, `Documentation/admin-guide/cgroup-v2.rst`, `Documentation/accounting/psi.rst`.
- `man 5 proc` (`/proc/pressure/memory`).

## 18. Cheat Sheet
- Thrashing: Σ|WS| > frames → fault-rate explosion, CPU collapse.
- Detect: high faults + low CPU + saturated swap I/O.
- WS(t,Δ) = pages referenced in last Δ references.
- Cure: suspend/swap a process (reduce D) or add RAM; cgroup limits localize it.
- LRU can't fix thrash (global demand > supply).
- kswapd reclaims proactively before faults; OOM kills as last resort.
- PSI `/proc/pressure/memory` = modern thrash gauge.
- swappiness biases anon-vs-file reclaim.

## 19. Quiz
1. Thrashing is:
   a) high CPU usage b) working sets exceed frames c) disk full d) TLB miss → **b**
2. Best indicator of thrashing:
   a) high free memory b) high fault rate + low CPU c) high CPU d) high disk space → **b**
3. Working set = :
   a) all pages b) pages in last Δ references c) dirty pages d) file pages → **b**
4. LRU prevents thrashing?
   a) yes b) no — global demand exceeds supply c) only local thrash d) always → **b**
5. First-line thrash cure:
   a) OOM kill b) suspend/swap a process c) reboot d) disable swap → **b**
6. Linux proactive reclaim runs in:
   a) kswapd b) OOM killer c) scheduler d) TLB → **a**

## 20. Flashcards
- **Q: What is thrashing?** → **A:** Σ working sets > frames → faults dominate, CPU collapses.
- **Q: How to detect?** → **A:** High fault rate + low CPU + saturated paging I/O.
- **Q: Working set?** → **A:** Pages referenced in the last Δ references (resident need).
- **Q: Why can't LRU fix it?** → **A:** It's local; global demand exceeding supply defeats any algorithm.
- **Q: The cures?** → **A:** Suspend/swap a process (reduce D) or add RAM; OOM as last resort.
- **Q: What's PSI?** → **A:** `/proc/pressure/memory` — production memory-pressure metric.

## 21. Revision
Thrashing is the VM failure mode: when Σ working sets exceeds RAM, every fault evicts a needed page — fault rates explode, CPU utilization collapses, and the disk spins. The working-set model (pages referenced in window Δ) measures per-process demand; the OS cures thrash by suspending/swapping a process (reducing D) or growing memory, and modern systems push the control loop into the kernel: kswapd reclaims proactively, cgroup limits localize pressure, PSI exposes pressure, and the OOM killer is the last resort. Diagnose via fault-rate + CPU, not by `free` — and remember LRU cannot rescue a globally over-subscribed system.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is thrashing and how do you detect it?" | 2 How / 13 Q1-2 |
| "What is the working-set model?" | 7 Formal / 13 Q3 |
| "Why doesn't LRU prevent thrashing?" | 13 Q6 / 4 Alternative |
| "How do you cure thrashing?" | 13 Q5 / 9 Internal |
| "How do containers experience it?" | 13 Q10 / 16 Industry |
| "What is PSI?" | 14 Q3 / 16 Industry |
