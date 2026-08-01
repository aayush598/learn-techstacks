# Frame Allocation Strategies

> **TL;DR**: Frame allocation decides **how many physical frames each process gets** — equal, proportional, or priority-weighted — and interacts with replacement (global vs local) to either protect processes from each other or maximize utilization; getting it wrong on the low side causes **thrashing** (Chapter 03).

## 1. Why Does This Exist?
Page replacement answers "which page to evict," but first we must decide *whose* pages can be evicted and *how many frames a process may hold*. Frame allocation exists because allocation determines isolation: with **local** replacement a process's faults depend only on its own allocation (a runaway process can't hurt others); with **global** replacement any process may be a victim (fair utilization, but one hog can displace others). And the *amount* allocated matters: too few frames → a process faults constantly (and with too few to even run — some instructions reference multiple pages, the **minimum frame count** problem); too many → wasteful. Allocation is the control knob between utilization and isolation, and it's the direct lever on thrashing.

## 2. How Does It Work?
- **Equal allocation**: m frames / n processes — simple, but wrong for mixed sizes.
- **Proportional allocation**: allocate proportional to process size (e.g., `frames_i = (size_i / Σ size) × m`). Better fit, still static.
- **Priority allocation**: scale by priority — high-priority processes get more frames (they fault less).
- **Local replacement**: each process has its own fixed allocation; a fault evicts only from its own pages. Predictable isolation; may underuse idle processes' frames.
- **Global replacement**: one shared pool; any fault can evict any process's page. Higher utilization; no per-process guarantee — can lead to unfairness/thrashing of a victim process.
- **Minimum frames**: at least enough for the maximum number of pages an instruction can touch concurrently (e.g., on x86, an instruction can reference base+index+displacement + copy ops; realistically ~2–3 pages; plus the stack page).

## 3. When Is It Used?
- **Every OS** implicitly: Linux uses mostly **global** replacement (reclaim scans all processes' pages via per-process lists, but decisions are global), Windows uses per-process working sets with trim (semi-local), macOS similar.
- **Database buffer pools**: fixed shared pool (global within the DB); per-tenant caches can be "local."
- **VMs/cloud**: KVM ballooning + cgroup limits act as per-process frame caps — allocation as a policy tool.
- **Real-time/safety**: fixed local allocations (ARINC 653 partitions) guarantee worst-case fault behavior.

## 4. Why Wasn't Another Approach Chosen?
- **No allocation (all pages share one pool, global)**: maximal utilization but no isolation — a faulty or hostile process can evict everyone. Linux's compromise: global reclaim but per-process LRU lists so the kernel *can* be fairer.
- **Pure local (rejected as sole policy)**: underutilizes idle processes; can't adapt to changing working sets without complex reallocation.
- **Pure proportional-static (rejected)**: working sets change over time (a process may become huge); static splits are wrong.
- **Dynamic/adaptive (chosen in hybrids)**: working-set model (Chapter 03) adjusts allocations to measured need; priority scaling; cgroup memory limits — the modern answer is *policy-layered*: mostly global with local guarantees via cgroups/priority.

## 5. Intuition
A shared apartment: how many rooms (frames) does each tenant get? Give everyone the same (equal — fair but wasteful if some tenants own nothing), split by belongings (proportional — fair-ish), or favor the tenant who pays more rent (priority). And who may be evicted: only your own stuff (local — safe but the fridge might be empty) or anyone's (global — full fridge but your milk can vanish). Too few rooms for a tenant → they keep packing/unpacking every hour (thrashing).

## 6. Real-World Analogy
An airport's luggage carousels: carousels = frames, airlines = processes. Equal = one carousel per airline (simple; a tiny airline wastes one). Proportional = carousels ∝ passenger count (better). Global = all airlines share all carousels (fast for everyone until one airline floods the hall, delaying all others). Minimum frames = the one carousel a flight needs to even start unloading.

## 7. Formal Definition
**Frame allocation** is the policy determining how many physical frames each process may use. Schemes include **equal** (m/n per process), **proportional** (`frames_i ∝ size_i`), and **priority-weighted** allocation. Replacement is **local** if the victim must belong to the faulting process (each process's allocation fixed) and **global** if the victim may be any process's page. A process requires a **minimum number of frames** — enough that no single instruction can fault more pages than it has, e.g., the maximum concurrently-referenced pages (typically a few) — otherwise it cannot complete even one instruction.

## 8. Example
m = 93 frames, 5 processes with sizes {10 KB, 127 KB, 64 KB, 127 KB, 10 KB} = Σ 338 KB.
- **Equal**: 93/5 ≈ 18.6 → 18 each (5 wasted).
- **Proportional**: 
  - P1: (10/338)×93 ≈ 2.7 → 3
  - P2: (127/338)×93 ≈ 34.9 → 35
  - P3: (64/338)×93 ≈ 17.6 → 18
  - P4: 35, P5: 3.
  - Sum ≈ 94 → trim one. P2/P4 (biggest) get ~35 — proportional to need.
- **Minimum-frames example**: an x86 instruction `MOV [base + index×4], reg` can touch the instruction page, a data page, and the stack page → a process needs ≥ 3 frames (in practice, Linux sizes `RLIMIT`-free but kernel logic ensures a working set floor; on some architectures the minimum is ~2–6).

Scenario: P1's working set is 40 pages but it's allocated 3 → it faults constantly (thrash within its quota); with global replacement it could still use 40 if others are idle — showing the utilization/isolation trade-off.

## 9. Internal Working
1. **Boot/limits**: the OS computes free frames after kernel/buffers; remaining = allocatable pool.
2. **Admission**: on `exec`, allocate per policy (Linux: no explicit per-process cap — the cgroup/memcg sets limits; scheduler + reclaim adapt).
3. **Reclaim (Linux)**: `kswapd` (background) or direct reclaim scans LRU lists *per process/memcg*; victims chosen by global scanning — effectively global but grouped.
4. **Working-set adjustment**: if a process is frequently faulting (thrashing), the working-set model (Chapter 03) raises or lowers its frames; priority adjustment scales.
5. **Minimum frames**: handled by reserving frames for kernel/user critical paths; the kernel never lets a runnable process fall below a usable floor (e.g., `NR_UNRECLAIMABLE` accounting).
6. **cgroups**: `memory.limit_in_bytes` caps a group's frames; the OOM killer triggers if a group exceeds and can't reclaim — allocation becomes an explicit policy API.

## 10. Time Complexity
- Equal allocation: O(1).
- Proportional: O(n) (sum + distribute).
- Global reclaim decision: O(pages scanned) per pass — amortized O(1) per page; batching (Linux sweeps K pages).
- Local replacement: O(1) amortized (per-process list).
- Working-set estimation: O(pages) per window with the reference bit; O(1) amortized.

## 11. Advantages
- **Isolation** with local allocation: one process's faults don't evict another's pages.
- **Utilization** with global allocation: idle processes' frames serve busy ones.
- **Proportional/priority** match heterogeneous workloads and QoS.
- **cgroup limits** give operators explicit control (containers).
- Minimum-frame guarantees prevent *per-instruction* livelock.

## 12. Disadvantages
- Local can **underutilize** (idle processes hold frames); global can **starve** a process (someone else always wins).
- Static schemes misjudge **changing working sets**.
- Minimum frames: hard to bound precisely for all instruction sets.
- Allocation + replacement interplay is subtle — the classic cause of **thrashing** (Chapter 03).
- More policy knobs = more tuning mistakes in production (swappiness, limits).

## 13. Interview Questions
1. **Q: What is frame allocation and why does it matter?** A: How many physical frames each process gets; it determines isolation vs utilization and sets the floor below which a process cannot run (minimum frames) — the lever on thrashing.
2. **Q: Equal vs proportional allocation?** A: Equal: m/n per process — fair but wasteful for mixed sizes. Proportional: ∝ size (or priority) — better fit to need, static but not adaptive.
3. **Q: What is the minimum number of frames and why?** A: Enough pages for any instruction's concurrent references (e.g., instruction + operand + stack pages, typically 2–6); with fewer, an instruction can fault on every page and never complete.
4. **Q: Local vs global replacement — trade-offs? (Tricky)** A: Local: faults only evict the process's own pages → isolation, predictable, but idle processes' frames are wasted. Global: any page can be evicted → higher utilization, but a big process can displace everyone (fairness/thrashing).
5. **Q: Which does Linux use? (Production)** A: Mostly global with per-process/per-memcg LRU lists — reclaim scans globally but groups work, so the kernel can be fair; cgroup memory limits make allocation explicit.
6. **Q: What's the thrashing boundary?** A: When the sum of processes' working sets exceeds the frames available, replacement can't keep up — allocation must shrink working sets (suspend/swap) or the system thrashes (Chapter 03).
7. **Q: How do you adapt allocation to a changing working set?** A: The working-set model measures recent page use (reference bits) and adjusts frames dynamically; priority scaling biases toward important processes.
8. **Q: What happens if a process is allocated too few frames?** A: It faults on nearly every access (its own working set doesn't fit) — it thrashes *locally*; with global replacement it may instead steal others' frames.
9. **Q: How do containers/limits interact with allocation?** A: cgroups cap memory (`memory.limit`), the kernel enforces by reclaiming inside the group, and the OOM killer fires if unreclaimable — operators control allocation policy at the group level.
10. **Q: Can a process use more than its allocation? (Scenario)** A: Only under global replacement, at the expense of others; under strict local, a fault with no free frame in its pool must wait (no eviction) — the design chooses which.
11. **Q: What's the relationship between allocation and Belady's anomaly?** A: Allocation changes a process's frame count m; stack algorithms (LRU) never hurt with larger m, but FIFO can — so allocation interacts with algorithm choice for guaranteed monotonicity.
12. **Q: What's "priority" allocation in practice?** A: Real-time or foreground processes get more frames so their fault rate is low and latency bounded; background processes get fewer. (E.g., Windows priority classes adjust working sets.)

## 14. Follow-Up Questions
1. **Q: How does the working-set model allocate frames?** A: Estimate each process's working set size W from recent references (sampling window Δ); allocate enough frames to hold W; adjust dynamically (Chapter 03).
2. **Q: What is "denial of service" by a frame hog?** A: Under global replacement, a process touching many distinct pages evicts others' pages constantly — their working sets collapse — a fairness DoS; cgroup limits prevent it.
3. **Q: How do large-page systems change allocation?** A: A 2 MB page consumes 512 4 KB frames at once — allocation granularity coarsens; limits and counters must count bytes, not pages.
4. **Q: What is "ballooning" in VMs?** A: The hypervisor inflates a fake device that reclaims guest frames (reducing guest allocation) so the host can serve other VMs — allocation at the VM layer.

## 15. Coding Example
```c
// Compute equal and proportional frame allocation
#include <stdio.h>

void allocate_equal(int m, int n) {
    int per = m / n, rem = m % n;
    printf("equal: %d frames each (+%d spare)\n", per, rem);
}

void allocate_proportional(int m, long *sizes, int n) {
    long total = 0;
    for (int i = 0; i < n; i++) total += sizes[i];
    long sum = 0;
    for (int i = 0; i < n; i++) {
        long f = (long)(m * (double)sizes[i] / total);
        sum += f;
        printf("proc %d (size %ld) -> ~%ld frames\n", i, sizes[i], f);
    }
    printf("distributed %ld of %d frames\n", sum, m);
}

int main(void) {
    long sizes[] = {10, 127, 64, 127, 10};
    allocate_equal(93, 5);
    allocate_proportional(93, sizes, 5);
    return 0;
}
```

## 16. Industry Usage
- **Linux**: cgroup v2 `memory.max`, `vm.min_free_kbytes`, `vm.swappiness`; reclaim in `mm/vmscan.c`; THP/cma interplay.
- **Windows**: working-set management (`NtSetInformationProcess`), `MiChooseVirtualAddressForAllocation`.
- **macOS**: per-task memory limits (`task_set_limit`), compressed memory.
- **Containers**: Kubernetes `memory` requests/limits → cgroup allocation + OOM scoring.
- **VMs**: KVM balloon, `memory.limit` per VM, cloud oversubscription policies.
- **Databases**: shared_buffers as a fixed pool; per-connection working-set tools.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 9.5.1 "Minimum Number of Frames", 9.5.2 "Allocation Algorithms", 9.5.3 "Global vs Local Allocation".
- Tanenbaum, *Modern Operating Systems*, Ch. 3.7.5 "Allocation Algorithms".
- Denning, "The Working Set Model for Program Behavior" (CACM 1968).
- Linux: `Documentation/admin-guide/cgroup-v2.rst`, `mm/vmscan.c`.
- KVM docs on ballooning and memory hotplug.

## 18. Cheat Sheet
- Allocation: equal (m/n), proportional (∝ size), priority-weighted.
- Replacement: local (own pages) vs global (any page) — isolation vs utilization.
- Minimum frames: enough for one instruction's concurrent pages (~2–6).
- Linux ≈ global reclaim grouped by memcg with per-process lists.
- Too few frames → local thrashing; too many → waste.
- Working-set model adjusts allocation dynamically.
- cgroups/K8s = operator-controlled allocation policy.
- Thrashing boundary = Σ working sets > frames (Chapter 03).

## 19. Quiz
1. Equal allocation gives:
   a) ∝ size b) m/n each c) by priority d) random → **b**
2. Local replacement evicts:
   a) any page b) only the faulting process's pages c) file pages d) kernel pages → **b**
3. Global replacement's downside:
   a) isolation loss/fairness b) low utilization c) complexity only d) none → **a**
4. Minimum frames exist because:
   a) TLB size b) an instruction may touch several pages c) disk block size d) cache lines → **b**
5. Linux's default is closest to:
   a) pure local b) pure global with grouped lists c) OPT d) FIFO → **b**
6. cgroups limit allocation via:
   a) swappiness b) memory.max c) swappiness+vm.dirty d) priorities → **b**

## 20. Flashcards
- **Q: Frame allocation policies?** → **A:** Equal (m/n), proportional (∝size), priority-weighted.
- **Q: Local vs global replacement?** → **A:** Local = own pages only (isolation); global = any page (utilization).
- **Q: Why a minimum frame count?** → **A:** An instruction can reference several pages at once; below the floor it can never complete.
- **Q: What does Linux do?** → **A:** Global-ish reclaim grouped per memcg with per-process LRU lists.
- **Q: How is allocation controlled in containers?** → **A:** cgroup memory limits (`memory.max`) + OOM scoring.
- **Q: Thrashing boundary?** → **A:** Sum of working sets > available frames.

## 21. Revision
Frame allocation decides per-process frame counts: equal (simple), proportional (∝ size), or priority-weighted; each needs a minimum floor (an instruction may touch multiple pages). Replacement scope is local (evict own pages — isolation, but idle frames wasted) vs global (evict anyone — utilization, but fairness risk). Linux is effectively global-with-grouping: reclaim scans per-memcg/per-process lists, and cgroup limits turn allocation into an operator policy. The failure mode — total working sets exceeding available frames — is thrashing, addressed next via the working-set model (Chapter 03).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is frame allocation?" | 1 Why / 7 Formal |
| "Equal vs proportional?" | 8 Example / 13 Q2 |
| "Why minimum frames?" | 13 Q3 / 7 Formal |
| "Local vs global replacement?" | 13 Q4 / 2 How |
| "How does Linux handle it?" | 13 Q5 / 16 Industry |
| "How do containers control it?" | 13 Q9 / 16 Industry |
