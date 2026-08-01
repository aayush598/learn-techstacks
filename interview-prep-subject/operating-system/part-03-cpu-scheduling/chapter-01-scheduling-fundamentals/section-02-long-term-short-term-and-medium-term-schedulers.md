# Long-Term, Short-Term, and Medium-Term Schedulers

> **TL;DR**: Scheduling is split into three levels — the long-term (admission) scheduler decides which jobs *enter* the ready pool, the short-term (dispatcher) scheduler decides which task runs *next* on the CPU, and the medium-term scheduler decides which processes are *swapped in/out* of memory — each with different frequency and goals.

## 1. Why Does This Exist?
"Who runs next?" isn't one decision — it's a pipeline of decisions at different timescales. The **long-term scheduler** controls *degree of multiprogramming* (how many jobs are admitted to fight for the CPU), the **short-term scheduler** makes the *per-millisecond* choice of the next task to dispatch, and the **medium-term scheduler** reacts to *memory pressure* by moving processes to/from disk (swap). The split exists because optimizing each timescale separately is simpler and more correct: admission control protects system stability, dispatching keeps the CPU busy, and swapping protects memory. On modern OSes the roles changed (Linux has no classical long-term scheduler — admission is implicit via limits/cgroups) but the three-way model remains the interview framework.

## 2. How Does It Work?
- **Long-term (job/ admission) scheduler**: selects processes from the *job pool* and admits them to memory (New → Ready). Controls multiprogramming degree. Frequency: infrequent (seconds/minutes). Historically in batch systems it chose job order.
- **Short-term (CPU) scheduler / dispatcher**: selects a ready process and *dispatches* it (Ready → Running). Frequency: very high (every tick, every block/wakeup). This is what most people mean by "the scheduler."
- **Medium-term scheduler**: moves processes between memory and disk (Ready↔Suspended-Ready, Blocked↔Suspended-Blocked) under memory pressure — swap in/out. Frequency: on demand (memory pressure events).
- On Linux: no explicit long-term scheduler (admission ≈ cgroup CPU limits, RLIMIT_NPROC, and the trivial case of a fork not exceeding limits); the short-term scheduler is EEVDF in `kernel/sched/fair.c`; the medium-term role is played by kswapd + direct reclaim + swap.

## 3. When Is It Used?
- **Long-term**: batch systems (admit jobs up to a multiprogramming limit), cgroup/limit enforcement ("admit only if resources allow"), Kubernetes pod admission (a real admission controller!).
- **Short-term**: every process switch — timer tick, I/O completion, wakeup, yield, exit.
- **Medium-term**: memory pressure (swap out idle/blocked processes), low-memory killers (Android LMK = medium-term-ish reclaim of processes), and process suspension in VM overcommit.
- **Hybrid**: RTOS with fixed tasks (no long-term); cloud VMs (admission = placement decisions by the orchestrator).

## 4. Why Wasn't Another Approach Chosen?
- **One monolithic scheduler (no levels)**: can't tune admission vs dispatch independently; multiprogramming degree becomes implicit and uncontrolled. Rejected.
- **No long-term scheduler**: process creation would flood memory with runnable tasks → thrashing; admission control exists precisely to avoid overcommit of *ready* work. Modern Linux approximates with limits (cgroup CPU/memory) because fork doesn't require "admission."
- **No medium-term scheduler**: when RAM is exhausted with a single in-memory model, the OS must kill or fail; swapping (medium-term) is more graceful — processes can continue later.
- **Moving all scheduling to hardware**: no — policies need software (see criteria).
The three-level model survives because each level addresses a different resource constraint (CPU, memory) at a different timescale.

## 5. Intuition
Think of a **venue with a bouncer, a floor manager, and a coat-check**:
- **Bouncer (long-term)**: controls how many people enter the club (multiprogramming degree) — too many and it's chaos.
- **Floor manager (short-term)**: decides, second by second, which guest gets the bartender's attention next (dispatch).
- **Coat-check / storage (medium-term)**: when the club is overcrowded, moves some guests to the outdoor smoking area (swap out) and brings them back later (swap in).
Three decisions, three timescales, one goal: keep the club running smoothly without exceeding capacity.

## 6. Real-World Analogy
A **hospital ER**: the triage nurse at the front desk (long-term) decides who gets admitted into the ER beds (multiprogramming). The ER doctor (short-term) decides which admitted patient to treat next — every few minutes. When beds run out, some stable patients get moved to the observation ward (swap out) and return when space frees (medium-term). Each level protects a different resource (beds, doctor time, space).

## 7. Formal Definition
- **Long-term scheduler (job scheduler)**: selects processes from the new/job queue for admission to memory, controlling the degree of multiprogramming; runs infrequently.
- **Short-term scheduler (CPU scheduler / dispatcher)**: selects the next ready process to execute on the CPU and dispatches it; runs very frequently (per scheduling decision).
- **Medium-term scheduler**: swaps processes between memory and disk to manage memory pressure and degree of multiprogramming; runs on demand.
- Linux correspondence: long-term ≈ admission limits/cgroups; short-term = EEVDF dispatcher; medium-term ≈ kswapd/reclaim + swap.

## 8. Example
Batch system with 100 jobs in the job pool, memory fits 4:
1. **Long-term**: admits 4 jobs (multiprogramming = 4), the rest wait in the pool.
2. **Short-term**: dispatches among the 4 every tick (e.g., RR, quantum 10ms).
3. **Medium-term**: memory pressure → one admitted job is blocked on I/O and gets swapped out; the long-term scheduler admits a 5th job to keep 4 in memory.
4. When the swapped job's I/O completes, the medium-term scheduler swaps it back in (if space) — it rejoins the ready/blocked queue.
Counts: 1 admission decision (seconds), ~4 dispatch decisions/ms, swap events (rare, on pressure).

## 9. Internal Working
1. **Long-term (classical)**: job queue → select by policy (SJF, priority) → `load` into memory → new→ready. Frequency and policy chosen to keep a target multiprogramming level.
2. **Linux modern equivalent**: `fork` succeeds unless `RLIMIT_NPROC`, `pid_max`, cgroup `pids.max`, or `cpu.max` quotas are hit — "admission" is *negative* (limits), not *positive* (selection). There's no job pool.
3. **Short-term**: `schedule()` called from tick, block, wakeup, exit, yield → `pick_next_task` (EEVDF rbtree) → `context_switch`.
4. **Medium-term (swap)**: kswapd scans pages under `watermark` pressure → reclaims clean pages / moves dirty to swap → processes whose resident set shrinks are effectively suspended; `vm.swappiness` tunes aggressiveness; swap in happens on access (page fault) or resume.
5. **Interaction**: blocked+swapped processes don't consume CPU (medium-term frees both memory *and* CPU for others).

## 10. Time Complexity
- Long-term decision: O(n) job-pool scan or O(1) limit checks (classical batch: O(n) per admission; Linux: O(1) checks).
- Short-term (dispatcher): O(1) amortized pick-next (EEVDF cached leftmost), O(log n) worst for rbtree updates.
- Medium-term (swap): O(pages) for swap in/out; kswapd O(scan window) per pass.
- Frequency dominates: short-term runs 1000s×/sec; long-term maybe once/sec; medium-term on pressure.

## 11. Advantages
- **Layered control**: admission, dispatch, and memory each tuned independently.
- **Stability**: admission caps prevent overload collapse; swap prevents hard OOM.
- **Determinism**: each level's criteria are simple at its own timescale.
- **Observability**: `mpstat`, `/proc`, `kswapd` stats, cgroup counters map to each level.

## 12. Disadvantages
- **Complexity**: three interacting policies; swap + admission can thrash.
- **Overhead**: swapping (medium-term) is I/O-expensive — pages must round-trip to disk.
- **Latency surprises**: a swapped-in process resumes slowly (page faults); admission delays job start.
- **Modern ambiguity**: Linux's lack of a true long-term scheduler means "admission" is implicit and easy to misjudge (OOM under load).

## 13. Interview Questions
1. **Q: What are the three types of schedulers?** A: Long-term (admission into memory, controls multiprogramming), short-term (dispatch next ready task to CPU), medium-term (swap in/out under memory pressure).
2. **Q: Which scheduler runs most frequently?** A: The short-term (CPU) scheduler — on every tick/block/wakeup (1000s/sec). The long-term runs rarely; medium-term on memory pressure.
3. **Q: What does the long-term scheduler control?** A: The degree of multiprogramming — how many processes are admitted into memory/ready at once. In batch systems it selects from the job queue.
4. **Q (TRICKY): Does Linux have a long-term scheduler?** A: Not classically — there's no job pool/admission selection. Its role is approximated by limits: `RLIMIT_NPROC`, cgroup `pids.max`, `cpu.max`/`memory.max` quotas — admission is enforced negatively, not chosen.
5. **Q: What is the medium-term scheduler's job?** A: Swap processes between memory and disk under memory pressure — moving ready/blocked processes to "suspended" states to free RAM; swap-in restores them (page faults).
6. **Q (SCENARIO): The system is thrashing (endless swap I/O). Which scheduler is failing and what's the fix?** A: Medium-term — swap in/out frequency is too high (multiprogramming too high, swappiness too high). Fix: reduce multiprogramming (admission/limits), lower swappiness, add RAM, or kill with OOM.
7. **Q: What's the difference between the short-term scheduler and the dispatcher?** A: Roughly the same thing in most texts — the dispatcher is the part of the short-term scheduler that performs the actual context switch (selecting = scheduling; switching = dispatching). Dispatch latency = the dispatcher's cost.
8. **Q: How does Android's low-memory killer relate to the medium-term scheduler?** A: It's an aggressive medium-term-like policy: under pressure it *kills* low-importance processes rather than swapping (phones lack swap) — trading process survival for memory.
9. **Q: Why can't the short-term scheduler control memory usage?** A: It only picks the next task; memory allocation is the memory manager's job. That's why a *separate* medium-term scheduler (or reclaim path) exists.
10. **Q: What happens to a swapped-out process when its I/O completes?** A: It's still in the suspended-blocked state; completion moves it to suspended-ready; the medium-term scheduler swaps it back in when memory is available — a resume (swap-in) then re-enables scheduling.
11. **Q (PRODUCTION): A container's cgroup CPU quota is exhausted. Which "scheduler" blocked it?** A: Admission/bandwidth enforcement (the long-term role via `cpu.max`) throttled it — the group exceeded its share; it's not the short-term dispatcher choosing badly.
12. **Q: What does `vm.swappiness` control?** A: The kernel's tendency to swap anonymous pages vs reclaim file cache (medium-term aggressiveness); high swappiness = more aggressive swap, can cause the thrash in Q6.
13. **Q: In a pure batch system, why is the long-term scheduler the right place for SJF?** A: Batch jobs are known upfront with estimated runtimes; SJF at admission minimizes average turnaround across the job pool — the short-term scheduler then just runs admitted jobs.
14. **Q: What is the "job pool"?** A: In batch systems, the queue of submitted-but-not-admitted jobs (on disk) — the long-term scheduler's input. Desktop/mobile OSes have no such pool (all processes are admitted on creation, subject to limits).
15. **Q: How do the three schedulers interact for a single process's life cycle?** A: Admitted (long-term) → dispatched (short-term, repeatedly) → maybe swapped out (medium-term) → swapped in → dispatched again → exits (short-term re-selects).

## 14. Follow-Up Questions
1. **Q: What is kswapd?** A: A kernel thread that proactively reclaims memory (scan + free pages) when watermarks drop — the practical incarnation of medium-term memory management on Linux.
2. **Q: What is "direct reclaim" vs kswapd?** A: kswapd = background; direct reclaim = a process's own page-fault path reclaims pages synchronously (latency spike) when kswapd can't keep up.
3. **Q: What is the relationship between multiprogramming degree and thrashing?** A: Too high a degree → resident sets don't fit → constant fault/swap → utilization collapses (thrashing); admission control exists to keep the degree in the "knee" of the curve.
4. **Q: What is CPU capacity / bandwidth in cgroup terms?** A: `cpu.max = quota period` (e.g., `50000 100000` = 50ms per 100ms) — a hard admission-style cap; `cpu.weight` = proportional share (soft).
5. **Q: Does FreeRTOS have all three schedulers?** A: No — it's a short-term scheduler only (fixed task set, no admission/swap). The three-scheduler model fits general-purpose/batch systems.

## 15. Coding Example
```c
/* Simulate the three scheduler levels (conceptual) */
#include <stdio.h>
#include <string.h>

#define MAX_MEM 4          /* multiprogramming limit */

typedef struct { char name; int burst; int swapped; } Job;

void long_term_admit(Job *pool, int n, Job *mem, int *in_mem) {
    /* admit until memory limit reached (simple FCFS admission) */
    while (*in_mem < MAX_MEM) {
        int i;
        for (i = 0; i < n && !pool[i].burst; i++);   /* find pending job */
        if (i == n) break;
        mem[(*in_mem)++] = pool[i];
        pool[i].burst = 0;                            /* mark admitted */
        printf("long-term: admitted %c (multiprogramming=%d)\n", mem[*in_mem-1].name, *in_mem);
    }
}

void short_term_dispatch(Job *mem, int in_mem) {
    /* round-robin: show each job getting one quantum */
    for (int i = 0; i < in_mem; i++)
        printf("short-term: dispatch %c\n", mem[i].name);
}

void medium_term_swap(Job *mem, int *in_mem, int idx) {
    printf("medium-term: swap out %c (memory pressure)\n", mem[idx].name);
    mem[idx] = mem[--(*in_mem)];      /* remove from memory (to disk) */
}

int main(void) {
    Job pool[] = {{'A',10,0},{'B',5,0},{'C',3,0},{'D',7,0},{'E',2,0},{'F',9,0}};
    Job mem[6]; int in_mem = 0;
    long_term_admit(pool, 6, mem, &in_mem);   /* admits 4 */
    short_term_dispatch(mem, in_mem);
    medium_term_swap(mem, &in_mem, 0);        /* pressure: free a slot */
    long_term_admit(pool, 6, mem, &in_mem);   /* admits 1 more */
    return 0;
}
```
```bash
# Observe the "medium-term" level on Linux
watch -n1 'grep -E "pgsteal|pswpin|pswpout" /proc/vmstat'
# Admission limits
cat /proc/sys/kernel/threads-max
cat /sys/fs/cgroup/cpu.max 2>/dev/null || echo "cgroup v2 cpu.max"
```

## 16. Industry Usage
- **Linux**: `kernel/sched/core.c` (dispatch), `kernel/sched/fair.c` (EEVDF pick), `mm/vmscan.c` + `mm/kswapd.c` (reclaim/swap), cgroup v2 (`cpu.max`, `pids.max`) as admission/limits.
- **Batch/HPC**: Slurm/LSF implement *real* long-term scheduling (job admission) with priorities/backfill.
- **Cloud/orchestrators**: Kubernetes admission controllers (long-term analog) + cgroup CPU/memory limits (enforcement).
- **Mobile**: Android LMK (medium-term-ish), iOS jetsam — memory-based process management.
- **Real-time/embedded**: short-term only (fixed task sets).
- **Interview angle**: the three-scheduler framework is asked directly, and "thrashing" questions hook into the medium-term role.

## 17. References
- Silberschatz, *OS Concepts*, Ch. 6.1-6.2 (Scheduling; dispatcher), Ch. 3.2 (queues).
- Tanenbaum, *Modern OS*, Ch. 2.4.1 (Scheduling).
- Linux source: `kernel/sched/core.c`, `kernel/sched/fair.c`, `mm/vmscan.c`, `kernel/cgroup/cgroup.c`.
- Linux docs: "cgroup v2" (kernel.org), `proc/vmstat`.
- Slurm docs (slurm.schedmd.com) — job scheduling/admission.

## 18. Cheat Sheet
- Long-term = admission (multiprogramming degree); infrequent.
- Short-term = dispatcher (next ready task); per tick/block/wakeup.
- Medium-term = swap in/out (memory pressure).
- Linux: no classic long-term; limits/cgroups fill the role.
- Dispatcher = scheduling decision + context switch (dispatch latency).
- kswapd + direct reclaim = Linux medium-term (reclaim/swap).
- Thrashing = multiprogramming too high → constant swap.
- swappiness = swap aggressiveness (medium-term knob).
- Android LMK ≈ aggressive medium-term (kills instead of swap).
- Batch (Slurm) has a true long-term scheduler; FreeRTOS has only short-term.

## 19. Quiz
1. Which scheduler controls multiprogramming degree? a) short b) long c) medium d) none → **b**
2. Most frequent: a) long-term b) short-term c) medium-term d) all equal → **b**
3. Medium-term scheduler deals with: a) CPU b) memory pressure/swap c) I/O d) files → **b**
4. Linux's "long-term" role is filled by: a) Slurm b) limits/cgroups c) kswapd d) OOM → **b**
5. kswapd is the Linux incarnation of: a) long-term b) short-term c) medium-term d) none → **c**
6. Thrashing is caused by: a) too few jobs b) too high multiprogramming c) slow CPU d) small quantum → **b**
7. The dispatcher: a) selects jobs b) performs the context switch c) swaps d) admits → **b**
8. Android LMK: a) swaps b) kills low-importance processes c) admits d) dispatches → **b**
9. FreeRTOS has: a) all three b) only short-term c) only long-term d) medium only → **b**
10. Slurm implements a real: a) short-term b) long-term (job) scheduler c) swap d) none → **b**

## 20. Flashcards
- **Q: Three scheduler types?** → **A:** Long (admission), short (dispatch), medium (swap).
- **Q: Most frequent?** → **A:** Short-term (per tick/block/wakeup).
- **Q: Long-term controls?** → **A:** Multiprogramming degree.
- **Q: Linux long-term equivalent?** → **A:** Limits/cgroups (negative admission).
- **Q: Medium-term job?** → **A:** Swap in/out under memory pressure.
- **Q: kswapd?** → **A:** Background reclaim thread (medium-term).
- **Q: Thrashing?** → **A:** Too many resident → constant swap → utilization collapse.
- **Q: Dispatcher?** → **A:** Context-switch performer (dispatch latency).
- **Q: Slurm vs FreeRTOS?** → **A:** True long-term job scheduling vs short-term only.

## 21. Revision
Scheduling has three levels: long-term (admission, controls multiprogramming), short-term (dispatcher, runs every tick/block/wakeup), medium-term (swap in/out under memory pressure). Linux has no classic long-term scheduler — limits/cgroups enforce admission; kswapd/reclaim is the medium-term role; EEVDF is the short-term dispatcher. Thrashing = too-high multiprogramming causing swap storms. Batch systems (Slurm) implement true job admission; FreeRTOS has only the short-term level.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What are the three schedulers?" | 13 Q1 / 7 Formal Definition |
| "Which runs most often?" | 13 Q2 / 2 How It Works |
| "Does Linux have a long-term scheduler?" | 13 Q4 / 9 Internal Working |
| "What does medium-term do?" | 13 Q5 / 2 How It Works |
| "System is thrashing — what's wrong?" | 13 Q6 / 12 Disadvantages |
| "Dispatcher vs scheduler?" | 13 Q7 / 7 Formal Definition |
| "Android LMK?" | 13 Q8 / 16 Industry Usage |
| "Container CPU quota throttled?" | 13 Q11 / 9 Internal Working |
| "What is swappiness?" | 13 Q12 / 3 When Is It Used |
| "How do schedulers interact in a life cycle?" | 13 Q15 / 9 Internal Working |
