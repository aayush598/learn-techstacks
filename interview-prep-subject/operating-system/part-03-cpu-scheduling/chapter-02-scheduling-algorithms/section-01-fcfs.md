# Section 01: First-Come, First-Served (FCFS)

> **TL;DR**: FCFS runs processes in arrival order to completion — dead simple and starvation-free, but a long early job creates the convoy effect that kills average turnaround and response time.

## 1. Why Does This Exist?
FCFS is the *default scheduling strategy* humans use: "first come, first served." For batch systems it needs zero machinery — no timers, no priorities, no data structures beyond a FIFO queue. It exists because it is trivially fair in one sense (arrival order is respected, nobody "jumps the line") and trivially cheap to implement. Understanding FCFS matters because every scheduler must at least match its simplicity, and FCFS exposes the fundamental problem — the convoy effect — that motivates every fancier algorithm.

## 2. How Does It Work?
- A FIFO queue holds ready processes in arrival order.
- The CPU picks the head; the process runs to completion (non-preemptive).
- When it blocks (I/O) or exits, the next FIFO entry is dispatched.
- No time quantum, no priority, no preemption. Arrival order = execution order.

## 3. When Is It Used?
- Batch systems where jobs are uniform and interaction is irrelevant.
- As a tiebreaker inside other schedulers (equal priority → FCFS).
- Line/queue processing at a single resource (printers, single-issue hardware queues).
- Baseline in analysis: other algorithms are compared against FCFS's TAT.

## 4. Why Wasn't Another Approach Chosen?
- **SJF**: better TAT but needs future knowledge and starves long jobs — rejected for simplicity.
- **RR**: needs a timer and creates switching overhead — overkill for pure batch.
- **Priority**: needs a notion of importance and starves low-priority tasks.
FCFS's whole point is *simplicity and non-starvation in arrival order*; where interactivity or variance exists, the convoy effect forces you to abandon it. That's exactly why the other algorithms were invented.

## 5. Intuition
A **single supermarket checkout**. Customers arrive and line up; the cashier serves each person fully before the next. If a customer with a huge cart (long burst) arrives first, everyone behind them waits for the entire cart — the convoy effect. Fair in "who's next" but awful in "how long do I wait on average."

## 6. Real-World Analogy
**Airport security with one lane**: passengers arrive in order and are each fully screened. One traveler with a suspicious bag (long processing) delays every person behind them. The lane keeps order (FCFS) but the average wait explodes with variance. Non-preemptive: you can't "park" someone mid-screening to process others faster.

## 7. Formal Definition
- A scheduling algorithm in which the process that arrives first is dispatched first and, once running, is never preempted — it holds the CPU until it terminates or blocks.
- Implemented as a FIFO queue. Picking next = O(1) dequeue.
- Given arrival times a_i and bursts b_i, completion time c_i satisfies c_i = max(a_i, c_prev) + b_i.

## 8. Example
Jobs: A(5), B(2), C(3), all arrive t=0.
- Order A→B→C. Gantt: A:0-5, B:5-7, C:7-10.
- TAT: A=5, B=7, C=10 → avg 7.33.
- Wait: A=0, B=5, C=7 → avg 4.0.
- Now with variance: A(10) arrives t=0, B(1) t=0. B waits 10 → convoy. SRTF would give B instantly.

## 9. Internal Working
1. New processes are appended to the FIFO tail (O(1)).
2. Dispatcher dequeues the head, saves its context, loads the new context.
3. The running process is *never* interrupted by the scheduler — no timer involvement.
4. On exit/block, the dispatcher repeats; blocked processes return to the tail when done (their *own* position, not strictly arrival order, if they re-queue — FCFS is about first *use*).
5. I/O-heavy vs CPU-heavy interplay: a CPU-bound job can hold the CPU while I/O devices sit idle → poor utilization.

## 10. Time Complexity
- Enqueue/dequeue: O(1).
- Pick-next: O(1) (head of FIFO).
- Preemption: none (no timer path).
- Total scheduler overhead: minimal — the cheapest of all algorithms.

## 11. Advantages
- Simple to implement (a FIFO is enough).
- No starvation — every job eventually runs.
- Deterministic, predictable execution order.
- No preemption overhead (no ticks, no context-switch-forced interruptions).
- Excellent when all jobs are short and uniform (batch).

## 12. Disadvantages
- **Convoy effect**: one long CPU-bound job delays many short jobs → bad average TAT/wait.
- Terrible response time for interactive jobs behind a CPU hog.
- Poor CPU+I/O utilization (device idle while one job computes).
- No fairness by priority or runtime; a short job waits for a long one.

## 13. Interview Questions
1. **Q: Describe FCFS.** A: Run processes to completion in arrival order using a FIFO queue; non-preemptive.
2. **Q: What is the convoy effect?** A: A single long (CPU-bound) job at the head delays all shorter jobs behind it — the "convoy" of short jobs. Both wait time and I/O utilization suffer.
3. **Q (TRICKY): Is FCFS fair?** A: Fair in "arrival order is preserved" (no line-jumping) but not fair in outcomes — a job arriving slightly later than a 100s job waits ~100s. Fairness is about bounds; FCFS has none on wait time.
4. **Q: What is the average waiting time for equal-length jobs under FCFS?** A: With n jobs of length L, arrival 0: waits are 0, L, 2L…(n-1)L → avg (n-1)L/2 — grows linearly with the queue.
5. **Q: When would you choose FCFS in production?** A: Where ordering matters more than efficiency: batch pipelines, print queues, single-resource serialization, or as a fair tiebreaker among equal priorities.
6. **Q: How does FCFS perform with a mix of CPU-bound and I/O-bound jobs?** A: Poorly — CPU-bound jobs hog the CPU while I/O devices sit idle; utilization drops. RR/SJF interleave them better.
7. **Q: Is FCFS preemptive?** A: No — it runs to completion (or block). Blocking (I/O) releases the CPU, but that's voluntary, not preemption.
8. **Q: Can FCFS starve a process?** A: No — arrival order guarantees every process eventually reaches the head. It's starvation-free (but convoy-ridden).
9. **Q (SCENARIO): All jobs arrive at t=0 with bursts [4,1,2]. What's avg TAT under FCFS?** A: Order 4,1,2: completions 4,5,7 → TAT avg (4+5+7)/3 = 5.33. SJF would give (1,3,7)/3 = 3.67 — showing why SJF wins.
10. **Q: Why is FCFS a "convoy" for I/O?** A: CPU-bound job runs continuously; I/O devices idle; when it finally blocks, all queued I/O hits the device at once → device bursts. Alternating (RR/SJF) keeps both busy.

## 14. Follow-Up Questions
1. **Q: How does FCFS relate to SJF?** A: FCFS = SJF when bursts are in ascending arrival order; otherwise SJF (shortest first) usually beats FCFS on average TAT.
2. **Q: What's the difference between FCFS and FIFO?** A: Same thing — a FIFO queue discipline defines FCFS. The term is used interchangeably.
3. **Q: How do you fix the convoy effect?** A: Preempt (RR), or shortest-first (SJF/SRTF), or MLFQ — anything that breaks run-to-completion.
4. **Q: Why does FCFS hurt CPU utilization?** A: A single CPU-bound process underutilizes I/O devices; utilization requires mixing I/O-bound jobs in, which FCFS doesn't enable.
5. **Q: What's FCFS's role in Linux?** A: CFS isn't FCFS; but on equal vruntime, ordering degenerates to FIFO-like behavior. FCFS also appears as the base for `SCHED_BATCH`-style low-priority semantics (though those differ).

## 15. Coding Example
```c
/* FCFS scheduler simulation (arrival order = FIFO) */
#include <stdio.h>
#include <stdlib.h>

typedef struct { int id, burst, arrive; } job;

int cmp(const void *a, const void *b) {
    return ((job*)a)->arrive - ((job*)b)->arrive; /* arrival order */
}

int main(void) {
    job jobs[] = {{0,5,0},{1,2,0},{2,3,0}};
    int n = 3, t = 0, tat = 0, wait = 0;
    qsort(jobs, n, sizeof(job), cmp);
    for (int i = 0; i < n; i++) {
        if (t < jobs[i].arrive) t = jobs[i].arrive; /* idle */
        wait += t - jobs[i].arrive;
        t += jobs[i].burst;
        tat += t - jobs[i].arrive;
        printf("job %d runs %d..%d\n", jobs[i].id, t-jobs[i].burst, t);
    }
    printf("avg TAT %.2f, avg wait %.2f\n", (float)tat/n, (float)wait/n);
    return 0;
}
```

## 16. Industry Usage
- Batch/offline pipelines (render farms, MapReduce task queues).
- Print/spooler queues, job queues in CI systems (often FCFS within a priority tier).
- Hardware queues (network transmit rings, single-lane resource arbitration).
- Benchmark baseline in scheduling literature and in OS theory.
- Where preemption is unavailable (very simple embedded/cooperative systems).

## 17. References
- Silberschatz, *OS Concepts*, 6.3.1 (FCFS).
- Tanenbaum, *Modern OS*, 2.4.3 (FCFS).
- Stallings, *Operating Systems*, scheduling chapter.
- man: `at`, `batch`, `cron` job ordering docs.

## 18. Cheat Sheet
- FCFS = FIFO queue, run to completion, non-preemptive.
- Pick-next O(1); zero preemption cost.
- Convoy effect: long job → many short jobs wait → bad avg TAT.
- No starvation but unbounded wait-time variance.
- Best for uniform, batch, ordering-critical work.
- Formulas: c_i = max(a_i, c_prev) + b_i; TAT = c - a; wait = TAT - b.
- I/O + CPU mixed workloads: FCFS underutilizes devices.
- Fix: preemption (RR) or shortest-first (SJF/SRTF/MLFQ).

## 19. Quiz
1. FCFS is: a) preemptive b) non-preemptive c) both d) neither → **b**
2. The convoy effect: a) helps I/O b) delays short jobs c) removes starvation d) speeds TAT → **b**
3. Pick-next in FCFS is: a) O(n) b) O(log n) c) O(1) d) O(n²) → **c**
4. FCFS starvation: a) common b) impossible c) priority-based d) tick-based → **b**
5. FCFS is best for: a) interactive b) batch-uniform c) real-time d) GPU → **b**
6. Wait formula: a) TAT-b b) b-TAT c) completion b) a+b → **a**
7. FCFS respects: a) priority b) arrival order c) burst d) deadline → **b**
8. To fix convoy use: a) longer quantum b) preemption c) FCFS d) polling → **b**
9. A CPU-bound job first under FCFS: a) improves utilization b) starves I/O c) speeds short jobs d) no effect → **b**
10. FCFS data structure: a) heap b) FIFO c) stack d) rbtree → **b**

## 20. Flashcards
- **Q: FCFS?** → **A:** FIFO, run to completion, non-preemptive.
- **Q: Convoy effect?** → **A:** Long job delays all short jobs behind it.
- **Q: Pick-next cost?** → **A:** O(1) — FIFO head.
- **Q: Does FCFS starve?** → **A:** No — arrival order guarantees progress.
- **Q: Best use?** → **A:** Uniform batch work, ordering matters.
- **Q: Worst weakness?** → **A:** Unbounded wait variance / convoy.
- **Q: Fix?** → **A:** Preemption (RR) or shortest-first.

## 21. Revision
FCFS dispatches in arrival order and runs to completion — the simplest, cheapest, starvation-free scheduler. Its fatal flaw is the convoy effect: one long job at the head delays everyone behind it, exploding average TAT/wait and idling I/O. It's ideal only for uniform batch work or as a fair tiebreaker; anywhere jobs vary in length or need response time, move to SJF/SRTF, RR, or MLFQ.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Describe FCFS" | 13 Q1 / 7 Formal Definition |
| "What is the convoy effect?" | 13 Q2 / 5 Intuition / 8 Example |
| "Is FCFS fair?" | 13 Q3 / 11 Advantages |
| "When choose FCFS in production?" | 13 Q5 / 3 When Is It Used |
| "FCFS with CPU+I/O mix?" | 13 Q6 / 9 Internal Working |
| "Can FCFS starve?" | 13 Q8 / 12 Disadvantages |
| "Compute avg TAT for [4,1,2]" | 13 Q9 / 8 Example |
| "Why does FCFS underutilize I/O?" | 13 Q10 / 9 Internal Working |
