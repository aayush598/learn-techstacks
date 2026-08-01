# Section 02: SJF and SRTF

> **TL;DR**: Shortest-Job-First (SJF, non-preemptive) and Shortest-Remaining-Time-First (SRTF, its preemptive twin) minimize average waiting time — provably optimal — but require knowing future CPU burst lengths, which no one can, making them an ideal you approximate with aging, exponential averaging, or MLFQ.

## 1. Why Does This Exist?
SJF exists because FCFS is provably bad: average wait time can be unbounded with a long early job. SJF asks the natural question — *why wait for the longest job when a shorter one could finish first?* By running the shortest available job next, it minimizes average waiting/turnaround time (provable via exchange argument). It exists as the *theoretical optimum* that every practical scheduler tries to approximate, because guessing burst lengths is the real problem.

## 2. How Does It Work?
- **SJF (non-preemptive)**: when the CPU frees, pick the ready job with the shortest CPU burst.
- **SRTF (preemptive SJF)**: also preempt the running job whenever a newly-arriving job has a *shorter remaining* burst.
- Needs an estimate of each job's burst; usually a priority queue (min-heap) keyed on burst/remaining time.

## 3. When Is It Used?
- As a *concept* everywhere: Linux, Windows, and MLFQ all favor shorter/faster tasks at run time.
- In batch scheduling where run times are known (e.g., long-running jobs with known durations).
- In theory and interviews as the benchmark: "optimal average wait" baseline.
- In approximation: exponential averaging predicts next burst from past bursts → pseudo-SJF.

## 4. Why Wasn't Another Approach Chosen?
- **FCFS**: simpler but convoy-ridden; SJF strictly dominates on average TAT.
- **RR**: fair/respondive but average TAT is *worse* than SJF (quantum wastes time); SJF is better when you only care about completion, not response.
- **Priority**: SJF *is* priority scheduling where priority = 1/burst; but SJF's priority is data-driven, not policy-driven.
SJF's weakness — it needs the future and can starve long jobs — is exactly why MLFQ was invented: it *learns* burstiness without knowing the future.

## 5. Intuition
**Grocery checkout**: the cashier always picks the customer with the fewest items next. Each customer finishes fast, so the *total* waiting time is minimized — the few items don't block many-item carts... but the person with 100 items might wait a long time (starvation). If a new small cart arrives while you're scanning a big one, SRTF says *pause and take the small cart* (preempt).

## 6. Real-World Analogy
**A single escalator line**: everyone waits; SJF lets people with 1 floor hop on first. Mathematically, total time people spend waiting is minimized when you serve shortest-first (each short task removes its own small wait from everyone's total). But long-haul riders (long bursts) keep getting deferred → starvation, the reason SJF needs aging or isn't used literally.

## 7. Formal Definition
- **SJF**: non-preemptive; at each scheduling decision, choose the ready process with the minimum predicted CPU burst b_i. Provably minimizes average waiting time among non-preemptive policies.
- **SRTF**: preemptive version; at every arrival, if the new job's remaining burst < the current job's remaining burst, preempt. Provably minimizes average waiting time among all (preemptive) policies.
- Prediction: b̂_{n+1} = α·b_n + (1-α)·b̂_n (exponential averaging), α typically 0.5.

## 8. Example
Jobs (arrive 0): A(6), B(2), C(1), D(7).
- SJF: C(0-1), B(1-3), A(3-9), D(9-16). TAT: 1+3+9+16=29, avg 7.25. Wait avg: 0+1+3+9=13/4=3.25.
- FCFS order A,B,C,D: TAT avg (6+8+9+16)/4=9.75 → SJF wins.
- SRTF: add B(2) arrives t=3 (A running, remaining 4) → no preempt (2<4? no wait B arrives at 3: A remaining 3 at t=3, B burst 2 < 3 → preempt!). A:0-3, B:3-5, then A:5-8, D? etc. SRTF always beats or ties SJF on average wait when arrivals are staggered.

## 9. Internal Working
1. Maintain a min-heap keyed on predicted burst (SJF) or remaining time (SRTF).
2. SJF: dispatch the min; never interrupt; on completion remove from heap.
3. SRTF: on every arrival, compare new job's burst with current remaining; if smaller, set need_resched → preempt.
4. Predict bursts with exponential averaging from the job's history (or decay a runtime statistic, which is how Linux CFS actually approximates "short first" via vruntime).
5. Aging (optional): increase effective priority of a waiting job over time to prevent starvation.

## 10. Time Complexity
- Heap extract-min / insert: O(log n).
- SRTF: O(log n) per arrival + O(1) comparison for preemption check.
- Prediction update: O(1) per completion.
- Optimal average waiting time (the reason for the heap); but measuring "optimal" assumes perfect prediction.

## 11. Advantages
- **Provably optimal** average waiting time (SJF among non-preemptive; SRTF among all).
- Minimal average turnaround time for batch workloads.
- Quick turnaround for short jobs — great for the common case (most jobs are short).
- Foundation of practical schedulers (approximate "shortest first" via runtime decay).

## 12. Disadvantages
- **Requires future knowledge** — burst times aren't known in advance; prediction is guesswork.
- **Starvation**: long jobs can wait indefinitely as short ones keep arriving (no aging by default).
- Preemption (SRTF) adds context-switch overhead and complexity.
- Prediction errors (α tuning) cause variance; "short first" can under-prioritize latency-sensitive *interactive* work that happens to have long bursts.

## 13. Interview Questions
1. **Q: Why is SJF optimal?** A: Exchange argument — if a longer job precedes a shorter one, swapping them lowers total wait. Therefore shortest-first minimizes average waiting time (non-preemptive case).
2. **Q: What's SRTF?** A: Preemptive SJF — if a newly arrived job has shorter *remaining* time than the running job, it preempts. Optimal among preemptive policies.
3. **Q (TRICKY): Can SJF be implemented in practice?** A: No, exactly — bursts are unknown. You can approximate with exponential averaging or run a decayed-runtime scheduler (CFS does this: lower runtime → "shorter"). But exact SJF needs a crystal ball.
4. **Q: What is starvation in SJF?** A: A long job that keeps being beaten by a stream of short arrivals may never run. Fix: aging (boost priority of long waiters).
5. **Q: Which is better, SJF or SRTF?** A: SRTF ≤ SJF on average wait when arrivals are staggered (preemption exploits short new arrivals); but SRTF has more context switches and can over-preempt.
6. **Q (SCENARIO): Compute avg wait for SJF, bursts [6,2,1,7] arrival 0.** A: order 1,2,6,7 → waits 0,1,3,9 → avg 3.25. FCFS same set → 3.25 vs FCFS (0,6,8,9)/4=5.75.
7. **Q: How does exponential averaging work?** A: b̂_{n+1} = α·b_n + (1-α)·b̂_n. α near 1 → trust recent bursts; α near 0 → smooth. It's a moving average predictor for the next burst.
8. **Q: Why is "shortest first" good in the real world?** A: Most processes are short; finishing them quickly minimizes queue length and average latency. This is why MLFQ and Linux favor low-vruntime tasks.
9. **Q: What's SJF's role as priority?** A: SJF = priority scheduling with priority = 1/burst — a data-driven priority rather than policy-driven.
10. **Q: Does SJF work with I/O-bound jobs?** A: Poorly as stated — I/O-bound jobs need the CPU briefly and often (small bursts) which SJF serves well, but predicting *their* bursts is noisy; MLFQ handles them better.
11. **Q (TRICKY): If you had perfect burst prediction, is SJF always best?** A: For average wait/TAT in batch, yes. But it sacrifices response-time bounds and can starve; interactive/RT systems still need preemption and deadlines — "optimal wait" isn't the only goal.
12. **Q: Why does CFS approximate SJF but not equal it?** A: CFS orders by vruntime (runtime already consumed), so a freshly-woken task with low vruntime gets picked first — a rough "shortest remaining." It's not exact because it measures *used* time, not *future* time.

## 14. Follow-Up Questions
1. **Q: How is SJF implemented (data structure)?** A: Min-heap keyed on predicted burst: O(log n) insert/extract.
2. **Q: What is the exchange argument?** A: For two adjacent jobs X then Y with bursts x>y, swapping → X waits y instead of Y waiting x. Since y<x, swapping reduces total wait. Repeat → shortest-first optimal.
3. **Q: What's the difference between SJF and SRTF worst-case?** A: SRTF can preempt a nearly-done long job for a tiny new job → thrashing context switches; SJF never preempts.
4. **Q: How do you prevent starvation?** A: Aging — add a factor that grows with waiting time (e.g., priority += wait/age), so long jobs eventually get picked.
5. **Q: Where is SJF used in Linux?** A: Directly: nowhere. Conceptually: CFS picks lowest vruntime (least-used), MLQ/priority tiers favor short-running interactive tasks. The *ideal* behind EEVDF/CFS ordering.

## 15. Coding Example
```c
/* SRTF simulation using a min-heap on remaining burst */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define N 4
typedef struct { int id, burst, remain, arrive; } job;

/* simple array-based min-heap (see standard heap impl) */
job heap[64]; int hn = 0;

int min_rem(void) {
    int best = -1;
    for (int i = 0; i < hn; i++)
        if (best == -1 || heap[i].remain < heap[best].remain) best = i;
    return best;
}

int main(void) {
    job j[N] = {{0,6,6,0},{1,2,2,3},{2,1,1,2},{3,7,7,0}};
    int t = 0, done = 0, prev = -1;
    while (done < N) {
        /* enqueue arrivals at time t */
        for (int i = 0; i < N; i++)
            if (j[i].arrive == t) heap[hn++] = j[i];
        /* preempt: running job stays, but re-pick each step */
        int m = min_rem();
        if (m != -1) {
            heap[m].remain--;
            printf("t=%d job%d runs\n", t, heap[m].id);
            if (heap[m].remain == 0) {
                printf("  job%d done at %d (TAT %d)\n",
                       heap[m].id, t+1, t+1-j[m].id > 0 ? t+1 : 0);
                heap[m] = heap[--hn]; done++;
            }
        }
        t++;
    }
    return 0;
}
```

## 16. Industry Usage
- **Linux CFS/EEVDF**: picks lowest-vruntime task — an SJF-like bias (short/early tasks finish).
- **MLFQ** (macOS, Windows, many RTOS): short/fast tasks get high-priority queues = SJF approximation.
- **Batch schedulers** with known runtimes (some HPC/research clusters, CI with estimated durations).
- **Job-shop/queuing theory**: EDF and SRT variants studied; network scheduling approximates shortest-processing-time.
- **RTOS**: not SJF per se; deadline-based instead. But SJF is the baseline all practical "fast-first" policies imitate.

## 17. References
- Silberschatz, *OS Concepts*, 6.3.2 (SJF) & 6.3.3 (SRTF).
- Tanenbaum, *Modern OS*, 2.4.4-2.4.5.
- Kleinrock, *Queueing Systems* (SJF optimality).
- Linux: `kernel/sched/fair.c` (vruntime ordering), docs "EEVDF".
- Cormen *et al.*, *CLRS*, ch. 6 (heaps).

## 18. Cheat Sheet
- SJF = shortest burst next, non-preemptive, optimal avg wait.
- SRTF = preemptive SJF (shortest *remaining*), optimal among all.
- Needs burst prediction (exponential averaging); not implementable exactly.
- Starvation → aging fixes.
- Min-heap: O(log n) per op.
- Prediction: b̂ = α·b + (1-α)·b̂.
- SJF = priority with priority 1/burst.
- CFS/MLFQ approximate it via low-vruntime/fast-task bias.
- Exchange argument proves optimality.

## 19. Quiz
1. SJF minimizes: a) response b) average wait/TAT c) context switches d) utilization → **b**
2. SRTF preempts when: a) new job shorter remaining b) quantum expires c) priority low d) I/O → **a**
3. SJF requires: a) timers b) future knowledge c) aging always d) RR → **b**
4. Exchange argument proves: a) RR optimal b) SJF optimal c) FCFS optimal d) MLFQ optimal → **b**
5. Starvation in SJF fixed by: a) preemption b) aging c) quantum d) MLQ → **b**
6. Prediction formula is: a) b̂=αb+(1-α)b̂ b) b̂=b+1 c) b̂=2b d) none → **a**
7. CFS approximates SJF via: a) highest vruntime b) lowest vruntime c) FIFO d) priority → **b**
8. SRTF vs SJF average wait: a) SRTF ≥ b) SRTF ≤ c) equal d) unrelated → **b**
9. SJF data structure: a) stack b) min-heap c) FIFO d) list → **b**
10. A long job under SJF: a) always fast b) can starve c) preempts d) none → **b**

## 20. Flashcards
- **Q: SJF?** → **A:** Non-preemptive shortest burst first; optimal avg wait.
- **Q: SRTF?** → **A:** Preemptive SJF (shortest remaining).
- **Q: Why not implemented exactly?** → **A:** Bursts unknown; prediction only.
- **Q: Starvation fix?** → **A:** Aging.
- **Q: Heap cost?** → **A:** O(log n).
- **Q: Exponential averaging?** → **A:** b̂ = αb + (1-α)b̂.
- **Q: CFS approximates it how?** → **A:** Picks lowest vruntime task.
- **Q: Optimality proof?** → **A:** Exchange argument.

## 21. Revision
SJF runs the shortest ready job next (non-preemptive), SRTF preempts for shorter-remaining newcomers; both minimize average waiting time and are optimal in their classes via the exchange argument. In practice bursts are unknown, so you predict (exponential averaging) or approximate (CFS's low-vruntime bias, MLFQ's fast-task queues); aging prevents starvation. This is the theoretical floor every real scheduler is measured against.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Why is SJF optimal?" | 13 Q1 / 5 Intuition / 8 Example |
| "What is SRTF?" | 13 Q2 / 7 Formal Definition |
| "Can SJF be implemented?" | 13 Q3 / 12 Disadvantages |
| "What is starvation?" | 13 Q4 / 9 Internal Working |
| "SJF vs SRTF?" | 13 Q5 / 11 Advantages |
| "Compute avg wait" | 13 Q6 / 8 Example |
| "Exponential averaging?" | 13 Q7 / 9 Internal Working |
| "Why shortest-first in real world?" | 13 Q8 / 3 When Is It Used |
| "SJF as priority?" | 13 Q9 / 7 Formal Definition |
| "CFS approximates SJF?" | 13 Q12 / 3 When Is It Used |
