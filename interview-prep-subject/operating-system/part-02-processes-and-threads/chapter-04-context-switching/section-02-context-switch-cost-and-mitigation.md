# Context Switch Cost and Mitigation

> **TL;DR**: Context switches are costly mostly because of cache/TLB misses and kernel entry/exit, not the register saves — so production systems mitigate with CPU affinity, PCID/ASID, runqueue locality, bounded thread pools, and (at the extreme) kernel-bypass and busy-polling to avoid switching altogether.

## 1. Why Does This Exist?
If context switches were truly free, oversubscription would be harmless. They're not: every switch risks flushing or missing caches (the new task's data isn't resident), reloading page-table state, and paying kernel entry/exit. The "cost and mitigation" topic exists because context-switch overhead is a *real, measurable* production problem — web servers, databases, and HFT systems are all sensitive to switch frequency. Understanding the cost model (what actually hurts) and the mitigations (what you can do about it) is how engineers tune latency and throughput, and a favorite interview probe after "what is a context switch?"

## 2. How Does It Work?
The cost decomposes into:
1. **Software path**: scheduler decision + register save/load + kernel stack switch — O(1), tens of cycles.
2. **TLB reload**: switching CR3 invalidates (or re-tags) translations; the new process's pages may not be cached → page-table walks → **TLB misses**.
3. **Cache coldness**: the new task's working set (code/data/stack) is not in L1/L2/L3 → **cache misses** dominate the cost (hundreds to thousands of cycles).
4. **Kernel entry/exit**: every switch passes through interrupt/syscall paths; with **KPTI**, a page-table switch per entry/exit adds more.
5. **Pipeline/speculation loss**: branch predictors and µop caches reset for the new code.

Mitigations, layered:
- **PCID/ASID**: tag TLB entries per address space; reloads don't flush everything.
- **CPU affinity (`sched_setaffinity`) / per-CPU runqueues**: keep a task on one CPU so its data stays warm.
- **Lazy FPU**: avoid saving FPU/vector state unless needed.
- **Thread-per-core / pinning**: dedicate a core to a task — zero switching.
- **Batching / reduced switch frequency**: coalesce wakeups, use worker pools, async I/O (fewer blocking switches).
- **Kernel-bypass** (DPDK, XDP, RDMA) and **busy-polling** (NAPI busy-poll): remove kernel-mode switches from the hot path entirely.

## 3. When Is It Used?
- **Tuning web servers**: `pidstat -w`/`vmstat cs` reveal switch storms; NGINX/Go choose epoll + worker pools to keep switches low.
- **Database tuning**: Postgres `max_connections` and thread pools control switches; MySQL thread pool; latency-sensitive OLTP pins workers.
- **HFT/real-time**: thread-per-core, isolated CPUs (`isolcpus`), no preemption — eliminate switches on the hot path.
- **Virtualization**: KVM balances vCPU switches vs host overhead; VMENTER/EXIT costs are a first-class concern.
- **Embedded/RTOS**: deterministic context-switch latency is a design goal (O(1) switches).

## 4. Why Wasn't Another Approach Chosen?
- **Avoid switching entirely (process per core)**: maximal locality, but cores are shared and finite — can't dedicate cores to every task; used selectively (isolcpus, HFT).
- **Hardware context switch (TSS)**: tried, rejected — slower and inflexible vs software save/restore.
- **Cooperative scheduling (only yield)**: fewer switches but no preemption guarantees; rejected for general purpose.
- **Bigger time slices (fewer switches)**: reduces count but increases latency — the classic throughput-vs-latency trade; schedulers (EEVDF) already balance.
- **Ignoring TLB/cache (assuming PCID makes it free)**: PCID removes *full* flushes but the *miss* cost on a cold context remains — mitigations are layered, not a silver bullet.
The chosen approach: cheap software switches + hardware assist (PCID) + kernel/user scheduling policy + application-level avoidance (pinning, batching, bypass).

## 5. Intuition
Context switching is like **changing workstations in a shared office**. Physically moving (register save) is quick — the real cost is that the *documents you need aren't on your new desk* (cache miss) and you must re-read the filing cabinet (TLB miss/page walk). If you always use the same desk (CPU affinity), your papers stay put. If you never leave your desk (thread-per-core), there's no cost at all. Switching often (many threads) is like bouncing between desks constantly — most of your time is re-finding documents.

## 6. Real-World Analogy
An **airport gate change**: swapping a flight from gate A to gate B (register save/load) is minutes. The real cost is passengers, luggage, and ground crew having to *re-arrive* at the new gate (cache/TLB misses). Keeping a flight at its original gate (affinity) is cheap; giving each flight its own permanent gate (thread-per-core) has no change cost at all. Frequent gate changes (switch storms) create chaos out of proportion to the move itself.

## 7. Formal Definition
**Context-switch cost** = software overhead (O(1) register save/restore + scheduler) **plus** microarchitectural recovery (TLB reload misses, cache cold misses, branch/pipeline refills, and kernel entry/exit with KPTI), typically ~1-5µs for thread switches and ~2-10µs+ for process switches. **Mitigations** reduce the frequency or the microarchitectural penalty: PCID/ASID, CPU affinity, per-CPU runqueues, lazy FPU, bounded concurrency, and kernel-bypass/busy-polling.

## 8. Example
Two workloads on an 8-core box:
- **Workload A**: 8 threads pinned 1-per-core, each doing CPU work with no blocking → ~0 context switches per second on the hot path; 100% useful throughput.
- **Workload B**: 400 threads (8 cores), each thread does 10µs work then blocks on I/O → each switch costs ~2-5µs + cache miss storms; `vmstat` shows 50k+ `cs/sec`; effective throughput drops sharply; latency jitter grows.
Numbers: if each switch effectively "wastes" ~5µs of core time (including miss recovery), 50k switches/sec costs ~250ms/sec of core time — a 25% overhead on one core equivalent.

## 9. Internal Working
1. **Scheduler path**: timer tick → `schedule()` → `pick_next_task` → `context_switch` (as in Section 01).
2. **TLB handling**: with PCID, `load_new_mm_cr3` writes CR3 with the new PCID so only that tag's entries are used; the old context's entries are preserved (no flush). Without PCID, `flush_tlb_mm_range` or full CR3 write invalidates.
3. **Cache behavior**: the new task's hot pages (its text, stack, data) are evicted/missing → L1/L2/L3 misses → memory latency (100+ cycles) per miss; multiple misses per switch → the dominant cost.
4. **KPTI interplay**: `arch/x86/entry/entry_64.S` switches between user and kernel page tables on entry/exit — every syscall/interrupt (and therefore every switch) pays an extra CR3 switch (mitigated by PCID but still a cost).
5. **Affinity/migration**: `sched_setaffinity` marks `cpumask`; the scheduler keeps tasks local; `sched_migrate` moves tasks only when load imbalance is significant (wakeup balance vs idle balance heuristics) — because migration *itself* causes cold caches.
6. **Application-level**: thread pools bound the number of runnable tasks; epoll/io_uring avoid per-operation blocking; busy-poll keeps the CPU in user space checking rings instead of switching to the kernel.

## 10. Time Complexity
- Register save/restore: O(1).
- Full TLB flush (no PCID): O(TLB capacity) on some archs; with PCID: O(1) tag switch.
- Page-table walk after miss: O(depth) (4 levels) per missing translation.
- Cache miss recovery: O(memory latency) per miss — the dominant variable cost.
- Scheduler pick: O(log n) worst (EEVDF rbtree), O(1) amortized.
- Switch frequency: bounded by runnable-task churn — the actual throughput lever.

## 11. Advantages
- **Quantifiable**: switch costs are measurable (`perf sched`, `vmstat cs`), so tuning is data-driven.
- **Many levers**: from kernel config (PCID, KPTI choice) to API (affinity) to architecture (bypass) — mitigation is layered.
- **Cheap in the common case**: uncontended systems switch rarely; the cost only bites under oversubscription.
- **Thread switches nearly free**: intra-process concurrency is affordable.

## 12. Disadvantages
- **Cost is workload-dependent**: cache-miss costs are hard to predict; tuning is empirical.
- **Mitigations conflict**: pinning hurts load balancing; busy-poll burns CPU; affinity can strand idle cores.
- **Kernel entry/exit tax** (KPTI) is paid even by low-switch workloads.
- **Determinism**: switch latency is microarchitecturally noisy — painful for real-time.
- **Over-tuning risk**: aggressive pinning/batching complicates operations and can make systems rigid.

## 13. Interview Questions
1. **Q: What makes a context switch expensive?** A: Not the register save (O(1)) — the microarchitectural recovery: TLB reload misses, cache cold misses for the new task's working set, branch/pipeline refills, and kernel entry/exit (with KPTI, a page-table switch per transition). Typically 1-10µs.
2. **Q: Why are process switches more expensive than thread switches?** A: Process switches reload CR3 (new page tables) and risk TLB/cache misses for a different address space; thread switches keep the same mm so TLB/caches stay mostly warm.
3. **Q (TRICKY): If PCID avoids TLB flushes, is a process switch now free?** A: No — PCID avoids *full flushes*, but the new context's translations aren't in the TLB (misses → page walks) and its data isn't in the caches. The miss cost remains; PCID removes only the flush part.
4. **Q: How do you measure context switches?** A: `vmstat 1` (`cs` column), `sar -w`, `pidstat -w`, `perf sched`, `/proc/<pid>/status` (`voluntary_ctxt_switches`/`nonvoluntary_ctxt_switches`).
5. **Q (PRODUCTION): Your app shows 100k cs/sec and 60% CPU in kernel. What's happening and how do you fix it?** A: Thread churn — many runnable threads switching constantly (lock convoying, yielding loops, oversubscription). Fix: bound thread pools, batch work, use async I/O (epoll/io_uring), align threads to cores, reduce lock contention.
6. **Q: What does CPU affinity do?** A: `sched_setaffinity` pins a task to a subset of CPUs — its caches stay warm (no migration cold-start), TLB reuse improves, and NUMA locality improves. Downside: hurts load balancing when pinned cores are oversubscribed.
7. **Q: What is thread-per-core and when would you use it?** A: Running exactly one busy task per core with no preemption (often with `isolcpus`/`SCHED_FIFO`) — zero context switches on the hot path. Used in HFT, packet processing (DPDK), and some databases. Wasteful if work is bursty.
8. **Q: How does a thread pool reduce context switches?** A: A bounded pool keeps runnable-thread count low (fewer scheduler churn), amortizes creation, and blocks workers efficiently — versus thread-per-task where threads constantly wake/sleep/switch.
9. **Q: What is busy-polling and why is it a mitigation?** A: The application (or driver, e.g., NAPI busy-poll, DPDK) spins checking for work instead of sleeping and being woken — trading CPU for latency, eliminating wakeup+switch overhead. Right when I/O rate is high and latency is critical.
10. **Q (TRICKY): Does a bigger time slice reduce total switch cost?** A: It reduces the *number* of switches (more work per slice) but increases *latency* for others waiting — the throughput-vs-latency trade. EEVDF dynamically balances vruntime so slices adapt.
11. **Q: What is kernel-bypass and why does it avoid switches?** A: DPDK/XDP/RDMA move packets/data between user space and NIC/memory without the kernel's syscall/interrupt path — no mode switches, no per-packet kernel scheduling. Extreme but effective for packet forwarding/storage latency.
12. **Q: What is KPTI's role in switch cost?** A: With KPTI, user and kernel use different page tables — every syscall/interrupt (thus every switch) reloads CR3, adding cost. PCID mitigates, but the syscall-heavy penalty was historically 5-30%.
13. **Q (SCENARIO): Design a low-latency trading/telemetry service. How do you minimize switching?** A: Pin threads to cores (`isolcpus`+affinity), use thread-per-core with busy-polling, batch with io_uring/DPDK, avoid blocking locks (lock-free structures), and let the scheduler run long slices (`SCHED_FIFO`). Measure with `perf sched` until cs/sec ≈ 0 on the hot path.
14. **Q: What's the difference between voluntary and involuntary switches?** A: Voluntary = the task blocks/yields (I/O, sleep, mutex). Involuntary = the timer preempts it (timeslice expiry, higher-priority wake). `pidstat -w` shows both; involuntary spikes indicate oversubscription.
15. **Q: How do NUMA nodes affect switching?** A: Migrating a task across NUMA nodes moves its data to far memory (higher latency); the scheduler's NUMA balancing weighs memory-access costs against load balance — another reason affinity and locality matter.

## 14. Follow-Up Questions
1. **Q: What is `isolcpus` / CPU isolation?** A: A kernel cmdline option removing CPUs from the general scheduler — dedicated cores for RT/latency tasks (no interference, no migrations).
2. **Q: What is the "wakeup migration" trade-off?** A: Waking a task on the CPU that last ran it keeps caches warm but may overload that CPU; the scheduler (EEVDF wakeup preemption, `select_task_rq`) balances warmth vs load.
3. **Q: What is lazy FPU and how much does it save?** A: Skipping FPU/AVX state save unless a conflict occurs — avoids copying up to ~1-2KB of vector state per switch; typical saving: 50-200 cycles per switch.
4. **Q: What is an "expensive" vs "cheap" context switch in RTOS terms?** A: FreeRTOS measures fixed worst-case switch latency (µs) — determinism, not average cost, is the design goal; they precompute and bound every path.
5. **Q: How does io_uring help switching?** A: It batches I/O (fewer syscalls/wakeups), supports multishot/ring completions, and lets you avoid per-operation blocking — cutting both mode switches and context switches in I/O-heavy workloads.

## 15. Coding Example
```c
/* pin a thread to CPU 0 to improve cache locality (reduce switching cost) */
#include <stdio.h>
#include <pthread.h>
#include <sched.h>

void pin_to_cpu(int cpu) {
    cpu_set_t set;
    CPU_ZERO(&set);
    CPU_SET(cpu, &set);
    if (pthread_setaffinity_np(pthread_self(), sizeof(set), &set) != 0)
        perror("pthread_setaffinity_np");
    printf("thread %ld pinned to cpu %d\n", pthread_self(), cpu);
}

void *worker(void *a) {
    pin_to_cpu(0);
    for (volatile long i = 0; i < 1e8; i++) /* busy work, no switching */
        ;
    return NULL;
}
int main(void) {
    pthread_t t;
    pthread_create(&t, NULL, worker, NULL);
    pthread_join(t, NULL);
    return 0;
}
```
```bash
# Measure context switches
vmstat 1 5 | awk 'NR>3{print "ctx/s:",$12}'
pidstat -w 1 3
perf sched record -- sleep 1 && perf sched latency | head -20
grep ctxt /proc/self/status    # voluntary vs nonvoluntary counters
```
```pseudocode
# Conceptual cost model
switch_cost = register_save_load (O(1), ~50 cyc)
            + tlb_reload (CR3 write; PCID tag or flush)
            + cache_miss_recovery (working-set misses, 100s-1000s cyc)
            + kernel_entry_exit (syscall/IRQ; +KPTI CR3 swap)
Effective throughput ~= useful_work / (useful_work + switch_cost * switches)
```

## 16. Industry Usage
- **Databases**: Postgres/MySQL tune worker counts; RocksDB/Scylla use io_uring; latency-sensitive OLTP pins workers (Percona, Amazon Aurora tuning guides).
- **Networking**: DPDK/XDP/AF_XDP eliminate kernel-mode switching in high-rate packet processing (Cloudflare, Meta load balancers); RDMA for storage.
- **HFT/fintech**: thread-per-core + isolated CPUs + busy-poll; no context switches on the hot path.
- **Cloud/containers**: cgroup CPU limits and scheduler tuning; Kubernetes CPU manager pins pods to cores for consistent latency.
- **Runtimes**: Go netpoller + goroutines (few OS threads, few switches); JVM NIO; Node libuv.
- **Kernel**: EEVDF, PCID, KPTI, per-CPU runqueues, `sched_setaffinity`, `isolcpus` — the kernel is constantly reducing switch cost.
- **Interview angle**: "why is context switching expensive" + "how do you reduce it" is a top-3 systems-performance question.

## 17. References
- Silberschatz, *OS Concepts*, Ch. 3.2 (Context Switch), Ch. 6 (scheduling).
- Tanenbaum, *Modern OS*, Ch. 2.1.3.
- Linux source: `kernel/sched/core.c`, `kernel/sched/fair.c`, `arch/x86/mm/tlb.c`, `kernel/sched/cpupri.c`.
- man: `sched_setaffinity(2)`, `perf-sched(1)`, `pidstat(1)`, `vmstat(8)`.
- Intel SDM: PCID, KPTI/Meltdown mitigations.
- LWN: "Context switching" analyses; DPDK docs (dpdk.org).

## 18. Cheat Sheet
- Cost = regs (O(1)) + TLB reload + cache misses + kernel entry/exit (+KPTI).
- ~1-5µs thread switch; ~2-10µs+ process switch.
- TLB/cache miss recovery dominates, not register saves.
- PCID/ASID avoid full flushes but not cold misses.
- Mitigations: affinity, per-CPU runqueues, thread pools, batching, busy-poll, kernel-bypass.
- Thread-per-core + isolcpus = zero hot-path switches (HFT).
- Measure: vmstat cs, pidstat -w, perf sched, /proc/<pid>/status.
- Voluntary vs involuntary switches (blocking vs preemption).
- Too many switches = kernel CPU burn; fix with pools + async I/O.
- io_uring/DPDK cut both mode and context switches.

## 19. Quiz
1. The dominant context-switch cost is: a) register saves b) cache/TLB misses c) scheduler code d) memory bandwidth → **b**
2. PCID does NOT eliminate: a) full flushes b) cold-cache misses c) CR3 writes d) all → **b**
3. Which mitigation skips the kernel on the hot path? a) affinity b) DPDK busy-poll c) PCID d) pools → **b**
4. Affinity improves: a) load balance b) cache locality c) fairness d) memory → **b**
5. `vmstat`'s `cs` column shows: a) cache size b) context switches/sec c) cores d) syscalls → **b**
6. Thread-per-core eliminates: a) work b) hot-path context switches c) syscalls d) interrupts → **b**
7. Involuntary switches come from: a) blocking b) timer preemption c) sleep d) yield → **b**
8. Bigger time slices trade: a) latency for throughput b) memory for CPU c) correctness d) nothing → **a**
9. KPTI adds cost because it: a) flushes every switch b) switches page tables per entry/exit c) disables PCID d) slower disk → **b**
10. io_uring reduces switches by: a) more threads b) batching I/O c) no syscalls at all d) spin forever → **b**

## 20. Flashcards
- **Q: What dominates switch cost?** → **A:** TLB/cache misses, not register saves.
- **Q: Thread vs process switch cost?** → **A:** ~1-5µs vs ~2-10µs+ (CR3 + misses).
- **Q: PCID?** → **A:** TLB tagging; avoids full flushes, not cold misses.
- **Q: Best mitigations?** → **A:** Affinity, pools, batching, busy-poll, bypass.
- **Q: How to measure?** → **A:** vmstat cs, pidstat -w, perf sched.
- **Q: Thread-per-core?** → **A:** Pin one task per core; zero hot-path switches.
- **Q: Voluntary vs involuntary?** → **A:** Blocking vs timer preemption.
- **Q: KPTI effect?** → **A:** Extra page-table switch per kernel entry/exit.
- **Q: io_uring/DPDK?** → **A:** Batch/bypass to cut mode+context switches.

## 21. Revision
Context switches cost ~1-10µs and the cost is dominated by TLB/cache misses, not register saves. Process switches (CR3 + new working set) cost more than thread switches. Mitigations: PCID (no full TLB flush), CPU affinity (warm caches), bounded thread pools (fewer runnable tasks), batching/io_uring, busy-polling, kernel-bypass (DPDK), and thread-per-core + isolcpus for extreme latency. Measure with vmstat/pidstat/perf sched. The goal in production is fewer, cheaper switches — and on the hottest paths, none at all.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Why is context switching expensive?" | 13 Q1 / 2 How It Works |
| "PCID → are switches free now?" | 13 Q3 / 9 Internal Working |
| "How do you measure switches?" | 13 Q4 / 15 Coding |
| "100k cs/sec in production?" | 13 Q5 / 16 Industry Usage |
| "What does CPU affinity do?" | 13 Q6 / 3 When Is It Used |
| "Thread-per-core use cases?" | 13 Q7 / 16 Industry Usage |
| "How do thread pools help?" | 13 Q8 / 4 Why Not |
| "Design a low-latency service?" | 13 Q13 / 16 Industry Usage |
| "Voluntary vs involuntary?" | 13 Q14 / 7 Formal Definition |
| "How does io_uring/DPDK help?" | 14 Follow-Up Q5 / 12 Disadvantages |
