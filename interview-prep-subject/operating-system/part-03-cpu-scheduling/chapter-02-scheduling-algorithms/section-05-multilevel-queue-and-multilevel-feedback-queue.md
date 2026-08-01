# Section 05: Multilevel Queue and Multilevel Feedback Queue

> **TL;DR**: MLQ partitions the ready queue by priority class (system/interactive/batch) with no movement between queues. MLFQ lets tasks move between queues based on behavior — short CPU bursts get boosted, CPU hogs get demoted — making it the practical scheduler behind modern interactive OSes.

## 1. Why Does This Exist?
A single global priority or a single RR queue can't serve mixed workloads: system tasks (0.1ms bursts), interactive tasks (10ms, latency-sensitive), and batch jobs (minutes). MLQ exists to *partition* priorities into classes. But MLQ's static partitioning mis-ranks: a batch task that happens to be short is stuck in the slow queue. **MLFQ** fixes that by letting tasks *prove* their nature — giving every task a chance to run fast and demoting those that abuse CPU. This self-learned behavior is why MLFQ needs no burst prediction and still beats static priority.

## 2. How Does It Work?
- **MLQ**: k queues, each with its own priority and scheduler (e.g., RR for system, RR for interactive, FCFS for batch). Tasks are *permanently* assigned to a queue by type. Higher queues always preempt lower.
- **MLFQ**: k queues with increasing quanta (Q0: RR q=8, Q1: q=16, Q2: q=32, ...). A new task starts in Q0. If it uses its whole quantum → demoted (CPU-bound). If it blocks early (I/O) → stays/boosts (interactive). Round-robin within each queue, higher queue always preempts.

## 3. When Is It Used?
- **MLQ**: systems with clearly separated task classes (system vs user vs batch) that don't change — real-time + timesharing hybrids.
- **MLFQ**: the classic model behind interactive general-purpose OSes (BSD, macOS QoS tiers, and conceptually the adaptive behavior in Windows/Linux).
- MLFQ is the theoretical answer to "scheduler for mixed interactive + batch without future knowledge."

## 4. Why Wasn't Another Approach Chosen?
- **Static priority/MLQ**: wrong for changing workloads — a task's classification is guessed at creation and never corrected. Rejected.
- **SJF/SRTF**: needs future knowledge. Rejected.
- **RR alone**: treats all equally, ignoring that interactive tasks need priority. Rejected.
- **EDF**: needs deadlines; not general-purpose. 
MLFQ chosen because it is **self-tuning**: it observes behavior (does the task use its whole quantum?) and adapts priority automatically — no user configuration, no burst prediction. Its problems (starvation of old tasks, gaming the scheduler) get classic fixes: boosting and accounting, which the textbook 3 rules encode.

## 5. Intuition
**A restaurant with moving tables**: new diners start at the fast counter (Q0, short quantum). If a diner takes too long (uses full quantum), they're moved to a slower table (longer quantum, Q1), then an even slower one (Q2). Quick diners (I/O) bounce back to the fast counter. Everyone starts equal; the restaurant learns who's a quick eater and who lingers.

## 6. Real-World Analogy
**Priority lanes on a highway with downgrades**: new cars enter the express lane (Q0) — if you're short-trip (interactive) you stay fast; if you're long-haul (CPU-bound) you get shunted to a slower lane with a bigger gap between exits (longer quantum) so the express lane serves quick trips. Periodic "refresh" (boosting) re-admits everyone to the express lane so nobody starves. It self-classifies drivers by behavior.

## 7. Formal Definition
- **MLQ**: queues Q0..Qk-1, each with a scheduler policy; assignment is fixed (system→Q0, interactive→Q1, batch→Q2, e.g.). Q0 preempts Q1 preempts Q2. Only one queue is serviced at a time (higher priority first).
- **MLFQ rules (Silberschatz)**: (1) New job → Q0. (2) Job A is served ahead of B if A's queue > B's (or same queue → RR). (3) When a job enters a queue, it gets one full time slice; if it doesn't finish, → next queue down. (4) If a job blocks (I/O) before quantum ends, it stays in (or is boosted to) a higher queue. (5) Periodic boost: all jobs move to Q0 to prevent starvation and handle priority inversion.

## 8. Example
Queues: Q0 (RR q=8), Q1 (RR q=16), Q2 (FCFS). Task X needs 25ms of CPU.
- X starts Q0: runs 8ms → demoted.
- Q1: runs 16ms → demoted.
- Q2: runs remaining 1ms to completion.
Task Y needs 4ms then I/O:
- Q0: runs 4ms, blocks early → stays Q0 (fast response next time).
Total: interactive Y always responds quickly; CPU-bound X is pushed down.

## 9. Internal Working
1. Data structures: k FIFO queues; a scheduler picks the highest non-empty queue; within it, RR with that queue's quantum.
2. On task wakeup: if it blocked (not quantum-exhausted), keep priority (or boost).
3. On quantum expiry: demote one queue; if at bottom, keep RR there (or FCFS).
4. Periodic boost timer: every T (e.g., 100ms), move all to Q0 — prevents starvation and "scheduler gaming" (a task could deliberately block just before quantum end to stay high — mitigated by accounting CPU usage even when blocked, or by boosting but also re-evaluating).
5. Interrupts/RT classes: RT tasks still preempt MLFQ at the very top.

## 10. Time Complexity
- Pick next queue: O(1) (scan k, k small — bitmap of non-empty queues).
- Enqueue/dequeue: O(1) per queue.
- Boost: O(n) over all tasks (periodic).
- Memory: O(n + k).
- Context switches: bounded by quanta; total overhead same tradeoff as RR.

## 11. Advantages
- **No burst prediction needed** — self-adaptive by observation.
- **Responsive to interactive tasks** (stay high), efficient for CPU hogs (demoted, long quanta).
- **No starvation** (with boosting).
- **Priorities emerge from behavior**, not user config.
- Bounded response (top queues RR), good throughput (bottom queues long quanta).

## 12. Disadvantages
- **Scheduler gaming**: a task can block just before quantum end to stay high (fixed by charging CPU time even while blocked — Linux charges vruntime for wait).
- **Configuration**: choosing number of queues, quanta, boost interval is fiddly.
- **I/O-intensive tasks can hog Q0** → boost storms.
- **Not deadline-aware** — no hard guarantees (RTOSes still use fixed-priority or EDF).
- Priority inversion still possible between queues (needs inheritance at the top).

## 13. Interview Questions
1. **Q: Difference between MLQ and MLFQ?** A: MLQ assigns each task to a fixed queue by type, never moving. MLFQ allows movement — tasks move down after using their quantum and up on blocking/boost — so behavior self-classifies.
2. **Q: What are the MLFQ rules?** A: New job → top queue; higher queues preempt lower; use full quantum → demote; block early → stay high; periodic boost to prevent starvation/gaming.
3. **Q: Why is MLFQ better than SJF in practice?** A: SJF needs future burst knowledge; MLFQ learns bursts from behavior (did it exhaust its quantum?) — practically optimal without a crystal ball.
4. **Q (TRICKY): What is scheduler gaming?** A: A task voluntarily blocks just before its quantum ends to avoid demotion, staying in the fast queue. Fix: account CPU time used even while blocked (Linux does this with vruntime) — or charge the full quantum.
5. **Q: How does MLFQ prevent starvation?** A: Periodic boosting: move all tasks to the top queue — guarantees even the most demoted task periodically runs at high priority.
6. **Q: What queues/quanta would you configure?** A: A few tiers: Q0 RR q=8ms, Q1 RR q=16ms, Q2 FCFS/SJF — enough to separate interactive from CPU-bound without excessive demotion churn.
7. **Q: How do RT tasks fit in?** A: Real-time/priority tasks sit above the MLFQ tiers (higher queues preempt); the MLFQ governs only the fair/timesharing classes.
8. **Q (SCENARIO): A batch job never blocks and a web server keeps blocking early. How do they interact?** A: Web server stays in Q0 (fast response, good); batch job demotes to Q2 (long quanta, low preemption) — the two don't fight; exactly MLFQ's point.
9. **Q: Why is MLFQ called "feedback"?** A: The scheduler uses *feedback* from past behavior (CPU usage) to change future priority — unlike open-loop priority.
10. **Q: What is the classic MLFQ implementation detail?** A: Within each queue, RR; only when a queue is empty do you service the next; a bitmap tracks non-empty queues for O(1) selection.
11. **Q: How does Linux relate to MLFQ?** A: Linux uses CFS/EEVDF (proportional share), not strict MLFQ — but the idea of adaptivity lives in latency targets (`sched_latency`, `sched_min_granularity`). macOS QoS is closer to MLFQ-style classes.
12. **Q: What's the downside of too many queues?** A: More configuration, more demotion latency, and more overhead; diminishing returns beyond ~3-5 tiers for typical workloads.

## 14. Follow-Up Questions
1. **Q: How does Windows NT relate to MLFQ?** A: It's priority-based with dynamic boosts (interactive threads boosted) — conceptually MLFQ-like adaptive priorities over 32 levels.
2. **Q: What's the relationship to aging?** A: Boosting IS a form of aging (periodic raise of priority); both prevent starvation.
3. **Q: How do you charge a blocked task that games the quantum?** A: Track CPU time consumed while runnable even if it didn't use the whole slice; if it repeatedly blocks just before the end, treat as used-up → demote anyway.
4. **Q: What's the boost interval tradeoff?** A: Too short → CPU hogs bounce back up (unfair); too long → low tasks starve longer. Typically ~100ms-1s.
5. **Q: Can MLFQ meet real-time deadlines?** A: No — soft at best. Hard deadlines need fixed-priority (RTOS) or EDF; MLFQ is for general-purpose latency.

## 15. Coding Example
```c
/* MLFQ simulation: 3 queues, quantum 8/16/32, demote on full quantum */
#include <stdio.h>

typedef struct { int id, need, queue, slice_used; } task;

#define QN 3
task q[QN][16]; int qn[QN] = {0};

void boost(void) {  /* rule: periodic boost to Q0 */
    for (int i = 1; i < QN; i++)
        for (int j = 0; j < qn[i]; j++) {
            q[0][qn[0]++] = q[i][j];
        }
    for (int i = 1; i < QN; i++) qn[i] = 0;
}

int main(void) {
    int quanta[QN] = {8, 16, 32};
    /* new tasks start at Q0 */
    task t1 = {0, 25, 0, 0};
    task t2 = {1, 4, 0, 0};
    q[0][qn[0]++] = t1; q[0][qn[0]++] = t2;

    for (int step = 0; step < 6; step++) {
        for (int i = 0; i < QN && qn[i] > 0; i++) {
            task *t = &q[i][0];
            int s = t->need > quanta[i] ? quanta[i] : t->need;
            printf("tick: task%d in Q%d runs %dms\n", t->id, i, s);
            t->need -= s;
            if (t->need > 0) {           /* didn't finish slice */
                q[i+1 < QN ? i+1 : QN-1][qn[i+1 < QN ? i+1 : QN-1]++] = *t;
            } else {
                printf("  task%d done\n", t->id);
            }
            /* remove head */
            for (int k = 1; k < qn[i]; k++) q[i][k-1] = q[i][k];
            qn[i]--;
        }
        if (step == 2) boost();  /* periodic boost */
    }
    return 0;
}
```

## 16. Industry Usage
- **macOS/iOS**: QoS classes (UI, interactive, utility, background) — MLQ-like static classes.
- **Windows**: adaptive priorities + boosts (MLFQ spirit).
- **BSD/older Unix**: multilevel feedback schedulers.
- **SCTP/network**: priority-based flow scheduling.
- **Linux**: not literal MLFQ — CFS uses vruntime decay, which approximates "short/runnable tasks run first" adaptively; EEVDF is its successor.
- MLFQ is the textbook answer for "interactive general-purpose scheduler" — expect it in OS interviews and in designing QoS tiers.

## 17. References
- Silberschatz, *OS Concepts*, 6.3.6 (MLQ) & 6.3.7 (MLFQ).
- Tanenbaum, *Modern OS*, 2.4.8 (MLQ/MLFQ).
- Ousterhout, "Scheduling Techniques for Concurrent Systems".
- Linux: `Documentation/scheduler/sched-design-CFS.rst`, EEVDF RFC.
- Windows Internals (priority model); macOS QoS docs.

## 18. Cheat Sheet
- MLQ: fixed class per task; no movement. MLFQ: adaptive, moving.
- MLFQ rules: Q0 start; higher preempts lower; full quantum → demote; early block → stay high; periodic boost.
- No burst prediction; self-learning.
- Scheduler gaming: block before quantum end → fix by charging full quantum / vruntime.
- Boosting = aging = starvation prevention.
- Pick queue: O(1) bitmap; per-queue ops O(1).
- Choose 3-5 queues with increasing quanta (8/16/32...).
- Not for hard real-time (no deadlines).
- Linux uses CFS/EEVDF, not literal MLFQ.

## 19. Quiz
1. MLFQ lets tasks: a) never move b) move between queues c) sleep only d) die → **b**
2. New MLFQ task starts at: a) lowest b) Q0 c) random d) batch → **b**
3. Using full quantum → a) boost b) demote c) stay d) exit → **b**
4. Blocking early → a) demote b) stay high c) kill d) no effect → **b**
5. Periodic boost prevents: a) inversion b) starvation c) overhead d) quantum → **b**
6. MLFQ needs burst prediction: a) yes b) no c) only RT d) always → **b**
7. Scheduler gaming fix: a) longer quantum b) charge full slice/vruntime c) boost d) FIFO → **b**
8. Pick next queue cost: a) O(n) b) O(1) c) O(log n) d) O(k²) → **b**
9. MLFQ suitable for: a) hard RT b) general-purpose interactive c) only batch d) GPU → **b**
10. Higher queues: a) run after lower b) preempt lower c) equal d) idle → **b**

## 20. Flashcards
- **Q: MLQ vs MLFQ?** → **A:** Fixed classes vs adaptive movement.
- **Q: New task starts?** → **A:** Q0.
- **Q: Full quantum?** → **A:** Demote.
- **Q: Early block?** → **A:** Stay high.
- **Q: Boost?** → **A:** Periodic → no starvation.
- **Q: Gaming?** → **A:** Block before quantum end; fix = charge full.
- **Q: Burst prediction?** → **A:** None — self-learning.
- **Q: Hard RT?** → **A:** No (use fixed-prio/EDF).

## 21. Revision
MLQ statically assigns tasks to priority classes; MLFQ adapts — new tasks enter Q0 and move down when they exhaust their quantum (CPU-bound) or stay up when they block early (interactive), with periodic boosting against starvation. No burst prediction needed; it self-classifies by behavior. Watch for scheduler gaming (block-before-quantum; fixed by charging full slice) and remember MLFQ is for general-purpose latency, not hard real-time. Linux uses CFS/EEVDF, but MLFQ is the classic interactive answer.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "MLQ vs MLFQ?" | 13 Q1 / 7 Formal Definition |
| "MLFQ rules?" | 13 Q2 / 7 Formal Definition |
| "Why better than SJF?" | 13 Q3 / 5 Intuition |
| "Scheduler gaming?" | 13 Q4 / 12 Disadvantages |
| "How prevent starvation?" | 13 Q5 / 9 Internal Working |
| "RT + MLFQ?" | 13 Q7 / 9 Internal Working |
| "Batch vs interactive interplay?" | 13 Q8 / 8 Example |
| "Why 'feedback'?" | 13 Q9 / 1 Why Does This Exist |
| "Linux vs MLFQ?" | 13 Q11 / 3 When Is It Used |
