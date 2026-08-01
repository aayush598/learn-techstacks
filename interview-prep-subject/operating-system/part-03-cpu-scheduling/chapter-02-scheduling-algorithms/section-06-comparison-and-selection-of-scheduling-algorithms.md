# Section 06: Comparison and Selection of Scheduling Algorithms

> **TL;DR**: No single algorithm wins. FCFS is simple but convoys; SJF/SRTF optimize TAT but need the future; RR optimizes response but hurts TAT; priority expresses importance but starves; MLFQ adapts. Real systems hybridize — Linux uses fair-share (EEVDF) + RT classes; the interview win is knowing the metric each algorithm optimizes.

## 1. Why Does This Exist?
Every algorithm trades off the scheduling criteria from Ch 1: throughput, turnaround, waiting, response, fairness, predictability. This section exists to give you the *decision framework*: given a workload and a metric, which algorithm wins? It's the synthesis question interviewers ask ("your web server has 2ms interactive requests and 10s batch jobs — what scheduler?"). Understanding the trade space is what separates "knows the definitions" from "can design a scheduler."

## 2. How Does It Work?
Compare algorithms along axes:
- **Metric optimized**: SJF/SRTF → avg wait/TAT; RR → max response; priority → importance; MLFQ → adaptive balance.
- **Preemption**: none (FCFS/SJF) vs timer (RR) vs wakeup (priority/MLFQ).
- **Knowledge required**: none (FCFS/RR) vs future (SJF/SRTF) vs observation (MLFQ).
- **Starvation**: FCFS/RR no; SJF/SRTF/priority/MLQ possible; MLFQ with boost no.
- **Overhead**: FCFS minimal; RR/MLFQ per-quantum context switches.

## 3. When Is It Used?
- Choosing a policy for a specific system: batch farm → SJF/FCFS; interactive desktop → MLFQ/RR+priority; hard RT → fixed-priority/EDF; fairness → CFS/weighted share.
- Interview questions: "which algorithm for X workload?" — the framework here is the answer.
- Real production: hybrid (Linux RT over CFS; Windows priority+boost; macOS QoS).

## 4. Why Wasn't Another Approach Chosen?
This isn't about one "right" algorithm — the question is *which tradeoff matters for your workload*. The alternatives aren't rejected; they're *specialized*. The unifying insight: production schedulers compose algorithms (MLFQ = priority + RR + aging; Linux = EDF-ish fair + RT priority). The "one true scheduler" doesn't exist because metrics conflict — you can't maximize both TAT and response simultaneously in general.

## 5. Intuition
**Choosing a queue at a stadium with multiple lines**: FCFS = one line, first-come. SJF = one line, shortest ticket first. RR = rotating lanes (fair, everyone moves). Priority = VIP/regular/GA lanes. MLFQ = lanes that change based on how fast you move through the gate. Which is "best"? Depends on whether you value total time, worst-case wait, or fairness.

## 6. Real-World Analogy
**A restaurant kitchen**: FCFS = tickets in order (orders pile up if one big ticket). SJF = quick dishes first (optimal total time, big tables wait). RR = cook cycles through tickets 2 min each (everyone gets served regularly, big dishes take long). Priority = VIP tickets jump the line (VIP fast, others starve). MLFQ = tickets start fast, slow-dishes demoted, quick dishes stay fast — self-adapting to the kitchen's mix.

## 7. Formal Definition
Decision matrix (Silberschatz Table-style):
| Algo | Preempt | Avg TAT | Response | Starvation | Future needed | Overhead |
|---|---|---|---|---|---|---|
| FCFS | No | Worst | Worst | No | No | Minimal |
| SJF | No | Near-opt | Bad | Yes | Yes | Low |
| SRTF | Yes | Optimal | Good | Yes | Yes | Medium |
| RR | Yes | Bad | Best | No | No | Medium |
| Priority | Yes* | Varies | Good | Yes | No | Low |
| MLFQ | Yes | Good | Good | No (boost) | No | Medium |
\* Priority can be non-preemptive too.

## 8. Example
Workload: interactive web requests (burst 1ms), a 30s batch job, a 5ms periodic telemetry task.
- FCFS: batch hog delays everything → bad.
- SJF: web (1ms) always first → good TAT, but batch starves without aging.
- RR q=10ms: web tasks wait up to n·10ms → meh for 1ms tasks.
- MLFQ: web stays Q0, telemetry Q0/Q1, batch demotes to Q2 → all happy.
- RT (fixed-prio): telemetry gets RT prio 50 → deterministic 5ms periodic.
Best: MLFQ for the interactive mix + RT class for telemetry = Linux's actual model.

## 9. Internal Working
1. Define the workload: burst distribution, arrival pattern, I/O ratio, deadlines.
2. Define metrics & weights: is response or throughput the goal?
3. Match algorithm to (workload, metric): use the matrix in section 7.
4. Consider overhead: preemptive algorithms cost context switches; verify q vs switch cost.
5. Add mechanisms: aging (starvation), priority inheritance (inversion), boosting (MLFQ), weight (fair share).
6. Validate: measure TAT/response/fairness; tune quantum/tiers.
7. Hybridize: compose classes (RT over fair) for mixed systems.

## 10. Time Complexity
- FCFS: O(1) ops; zero preemption overhead.
- SJF/SRTF: O(log n) heap ops; SRTF adds per-arrival preemption check O(1).
- RR: O(1) queue ops + 2 context switches per quantum.
- Priority: O(1) bitmap pick (Linux RT); ties FCFS.
- MLFQ: O(1) queue pick (bitmap of k queues) + per-quantum switches + periodic boost O(n).
- Selection cost is secondary to metric fit — the framework is about *which metric*, not raw speed.

## 11. Advantages
- **Framework thinking**: match algorithm to workload — better than memorizing.
- **Hybridization**: combining classes (RT over fair) gets multiple metrics at once.
- **Bounded tradeoffs**: know exactly what you sacrifice (TAT for response, etc.).
- **Predictable engineering**: pick deterministic algorithms (fixed-priority) where deadlines matter.

## 12. Disadvantages
- **No universal optimum** — every choice sacrifices something.
- Metric conflicts: minimizing TAT (SJF) harms worst-case response (RR wins).
- Real workloads are heterogeneous — a single algorithm always mis-fits some tasks.
- Configuration (quanta, priorities, tiers) is fragile and workload-dependent.
- Theory metrics (TAT) ≠ production reality (latency, fairness, energy, isolation).

## 13. Interview Questions
1. **Q: Which algorithm minimizes average waiting time?** A: SJF (non-preemptive) / SRTF (preemptive) — optimal in their classes; but both need future burst knowledge.
2. **Q: Which is best for response time?** A: RR (with suitable quantum) or MLFQ — bounded worst-case response; FCFS/SJF are worst.
3. **Q (TRICKY): Your workload: many 1ms interactive tasks + one 60s batch job. Which scheduler?** A: MLFQ — interactive stays high (fast response), batch demotes (efficient); or priority with aging. Not FCFS (convoy), not pure RR (wasteful quanta).
4. **Q: Why does Linux use CFS/EEVDF instead of MLFQ?** A: MLFQ gives qualitative priorities; CFS gives *proportional share* (weighted fairness, low latency) — better isolation and tunability for general-purpose Linux; RT classes on top for hard priorities.
5. **Q: When would you pick FCFS in 2026?** A: Where ordering/monotonicity beats latency: print/spool queues, serial batch pipelines, or as a tiebreaker — never for interactive.
6. **Q: SJF vs SRTF which to implement?** A: SRTF if you can preempt and want best avg wait with staggered arrivals; SJF if you want no preemption overhead and can accept longer waits.
7. **Q (SCENARIO): A real-time system needs 1ms-periodic task response under 1ms. Which?** A: Fixed-priority preemptive (RTOS) — MLFQ/RR can't give hard bounds. EDF if schedulability allows.
8. **Q: How do you pick a quantum for RR/MLFQ?** A: q ≫ context-switch time (avoid thrash); q ≤ target response time / n (keep worst-case response bounded). Common: 10-100ms.
9. **Q: What's the difference between optimizing TAT and response?** A: TAT = completion − arrival (throughput feel); response = first CPU − arrival (interactivity). SJF optimizes TAT, RR optimizes response — they conflict.
10. **Q: Why is MLFQ "self-adaptive"?** A: It needs no a-priori burst knowledge; behavior (did it exhaust its quantum?) drives queue placement — the feedback loop.
11. **Q (PRODUCTION): A noisy neighbor batch job kills your latency. Mitigation?** A: Fair-share (CFS weight/cgroups) or RT class for the latency-sensitive service; MLFQ-style would demote the batch — all valid, choose by need for hard isolation vs simple priority.
12. **Q: What metrics do production schedulers actually optimize?** A: p99 latency, utilization, fairness, isolation, energy — not textbook avg TAT. This gap is why CFS/EEVDF (fair share) replaced pure MLFQ/priority designs.

## 14. Follow-Up Questions
1. **Q: What is the "LPT rule"?** A: Longest Processing Time first — good for minimizing *makespan* (finish time of all jobs) on parallel machines, opposite of SJF; used in load balancing.
2. **Q: What's the relation between scheduling and utilization?** A: More context switches (small q) → more overhead → lower utilization; batch (no preemption) → high utilization, low response.
3. **Q: How does energy factor in?** A: Idle-waiting vs busy-waiting; NO_HZ and low-latency preemption conflict with power — DVFS-aware schedulers balance both.
4. **Q: What is the difference between preemptive SJF and EDF?** A: SRTF = preempt on shorter *remaining time*; EDF = preempt on *earlier deadline* (or when new job has earlier deadline). EDF is optimal for meeting deadlines; SRTF for avg wait.
5. **Q: Why do real OSes never use textbook SJF?** A: Bursts are unknowable, and the kernel doesn't predict user behavior reliably; MLFQ/CFS approximate without prediction.

## 15. Coding Example
```c
/* Choosing a scheduler: workload-driven selection simulation */
#include <stdio.h>

typedef struct { double burst, arrive, io_ratio; } workload;

/* pretend burst predictor from history */
double predict(double prev, double avg) { return 0.5*prev + 0.5*avg; }

const char *recommend(workload w) {
    if (w.io_ratio > 0.7) return "MLFQ (interactive, block-early stays high)";
    if (w.burst < 5.0)    return "RR or MLFQ with small quantum";
    if (w.arrive < 0)     return "FCFS batch pipeline (ordering matters)";
    return "Priority + aging (mixed importance)";
}

int main(void) {
    workload web   = {0.001, 0, 0.95};
    workload batch = {30.0, 0, 0.02};
    printf("web:   %s\n", recommend(web));
    printf("batch: %s\n", recommend(batch));
    printf("predicted next burst: %.2f\n", predict(0.8, 0.4));
    return 0;
}
```

## 16. Industry Usage
- **Linux**: EEVDF/CFS (fair share) + RT/deadline classes — the hybrid answer.
- **Windows**: priority classes + dynamic boosts — MLFQ spirit over 32 levels.
- **macOS/iOS**: QoS classes (UI → background) — MLQ-like.
- **FreeRTOS/QNX**: fixed-priority preemptive — the RT answer.
- **HPC**: FCFS + backfill; SJF-ish (short jobs scheduled in gaps).
- **GPU**: work stealing / priority batches.
- The interview lesson: real schedulers are *compositions* — know which primitive each class uses.

## 17. References
- Silberschatz, *OS Concepts*, 6.3.8 (algorithm comparison) & Ch 6 summary.
- Tanenbaum, *Modern OS*, 2.4 (comparison).
- Kleinrock, *Queueing Systems* (SJF optimality, M/M/1).
- Linux docs: EEVDF, cgroup CPU controller.
- Windows Internals (dispatcher priorities).

## 18. Cheat Sheet
- SJF/SRTF → avg wait/TAT optimal (future needed).
- RR → best bounded response (quantum tunes).
- FCFS → simplest, convoy, batch-only.
- Priority → importance; starves (aging); inverts (inheritance).
- MLFQ → adaptive, no prediction, best interactive general purpose.
- Tradeoff: TAT (SJF) vs response (RR) conflict.
- Real systems compose: Linux = fair + RT; Windows = priority+boost.
- Pick q: ≫ switch cost, ≤ response_target/n.
- Hard RT → fixed-priority or EDF, not MLFQ/RR.
- LPT minimizes makespan (parallel) — opposite of SJF.

## 19. Quiz
1. Minimizes avg waiting time: a) FCFS b) SRTF c) RR d) MLQ → **b**
2. Best response bound: a) SJF b) RR c) FCFS d) batch → **b**
3. No burst knowledge needed: a) SJF b) SRTF c) MLFQ d) both a+b → **c**
4. Starvation-free by construction: a) SJF b) RR c) priority d) SRTF → **b**
5. Convoy effect: a) RR b) FCFS c) MLFQ d) SRTF → **b**
6. Hard RT scheduling: a) MLFQ b) RR c) fixed-prio/EDF d) FCFS → **c**
7. Linux base scheduler: a) MLFQ b) EEVDF/CFS c) FCFS d) priority → **b**
8. Quantum tradeoff: q big → a) better response b) FCFS-like c) thrash d) faster → **b**
9. LPT minimizes: a) TAT b) makespan c) response d) fairness → **b**
10. Best interactive general purpose: a) MLFQ b) FCFS c) SRTF d) batch → **a**

## 20. Flashcards
- **Q: Min avg wait?** → **A:** SRTF (needs future).
- **Q: Best response?** → **A:** RR (tuned q).
- **Q: No prediction?** → **A:** MLFQ self-adapts.
- **Q: Starvation-free?** → **A:** FCFS/RR/MLFQ(+boost).
- **Q: Convoy?** → **A:** FCFS.
- **Q: Hard RT?** → **A:** Fixed-prio / EDF.
- **Q: Linux?** → **A:** EEVDF + RT classes.
- **Q: q choice?** → **A:** ≫ switch cost, ≤ target/n.
- **Q: LPT?** → **A:** Min makespan on parallel.

## 21. Revision
Each classic algorithm optimizes one metric: SRTF minimizes average wait (but needs the future), RR bounds response (at TAT cost), FCFS is the simple convoy-prone baseline, priority encodes importance (starvation/inversion fixable), and MLFQ self-adapts without prediction — the practical interactive winner. Real production schedulers compose these: Linux stacks RT classes over EEVDF fair-share; Windows uses priority + boosts. Match the algorithm to the workload and metric; never apply one everywhere.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Which minimizes avg wait?" | 13 Q1 / 7 Formal Definition |
| "Best for response?" | 13 Q2 / 5 Intuition |
| "Workload: interactive + batch?" | 13 Q3 / 8 Example |
| "Why CFS over MLFQ?" | 13 Q4 / 16 Industry Usage |
| "When pick FCFS?" | 13 Q5 / 3 When Is It Used |
| "SJF vs SRTF?" | 13 Q6 / 12 Disadvantages |
| "RT needs 1ms response?" | 13 Q7 / 4 Why Not |
| "Pick a quantum?" | 13 Q8 / 10 Time Complexity |
| "TAT vs response?" | 13 Q9 / 7 Formal Definition |
| "Noisy neighbor mitigation?" | 13 Q11 / 16 Industry Usage |
