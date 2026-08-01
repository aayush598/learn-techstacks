# Section 03: Real-Time and RTOS Scheduling

> **TL;DR**: Real-time scheduling must guarantee deadlines: fixed-priority preemptive (the RTOS standard) and EDF (optimal but fragile under overload). Linux offers soft real-time via SCHED_FIFO/RR and hard-ish via SCHED_DEADLINE (EDF); hard real-time systems use dedicated RTOSes (FreeRTOS, QNX, VxWorks) with schedulability analysis.

## 1. Why Does This Exist?
A web server that's 50ms late is annoying; a missile-guidance loop, a pacemaker, or an ABS controller that's late is *catastrophic*. Real-time scheduling exists to give *guarantees*: the scheduler must prove a task will meet its deadline before the system is trusted. This requires different math than "fairness" — it needs worst-case execution time (WCET) models, fixed priorities (or deadlines), and schedulability tests that decide *before runtime* whether the workload fits the CPU.

## 2. How Does It Work?
- **Fixed-priority preemptive (FPP)**: tasks get static priorities; the highest-priority ready task always runs (preemption). Priorities encode deadlines/importance. Schedulability test: **RMS** — for n tasks with periods, if utilization U ≤ n·(2^(1/n) − 1), all tasks meet deadlines (for rate-monotonic priorities).
- **EDF (Earliest Deadline First)**: run the task with the earliest deadline; **optimal** for meeting deadlines (if any schedule exists, EDF meets it) while U ≤ 1 (under full preemption).
- **SCHED_DEADLINE** (Linux): EDF with a guaranteed bandwidth (runtime/period budget) via CBS (Constant Bandwidth Server).
- **Analysis**: worst-case response time (WCRT) — sum of preemption/interference; checks feasibility a priori.

## 3. When Is It Used?
- **Hard RT**: automotive ECU (CAN, ABS), aerospace (flight control), medical devices, robotics control loops, industrial PLCs — dedicated RTOS.
- **Soft RT**: audio/video streaming, games, telecom — Linux SCHED_FIFO/RR/DEADLINE acceptable (missing a deadline degrades quality, not safety).
- **Mixed**: Linux with PREEMPT_RT + RT classes for industrial Linux (CODESYS, ROS2 realtime).

## 4. Why Wasn't Another Approach Chosen?
- **Round Robin / CFS**: no deadline guarantees — a task's deadline can always be missed. Rejected for RT.
- **SJF**: burst-driven, not deadline-driven; may miss deadlines with high utilization. Rejected.
- **FIFO/fair share**: no worst-case guarantee. Rejected.
- **EDF**: optimal but fragile under overload (domino of missed deadlines) and hard with non-preemptible sections — this is why FPP (RMS) is the RTOS default: deterministic, analyzable, and overload degrades predictably (low-priority tasks miss, high ones don't).
The two chosen: **FPP for determinism** (most RTOS), **EDF for utilization** (SCHED_DEADLINE).

## 5. Intuition
**A hospital with deadlines, not fairness**: FPP = surgeons by rank — highest-rank (highest priority) surgery always happens first; you can prove, if the OR schedule fits, every surgery finishes on time (RMS schedulability). EDF = treat whoever's deadline is *soonest* first — provably optimal, but if you overbook (overload), *everyone* gets delayed, like dominoes. RTOSes pick FPP because when overloaded, they'd rather the low-priority task be the one that dies, not the critical one.

## 6. Real-World Analogy
**An airline's check-in with flight deadlines**: EDF = serve the passenger whose flight departs soonest (optimal for on-time boarding). FPP = serve by class (first-class always first) with a boarding-time analysis showing everyone makes it if the counter load is low enough. If a crowd storms in (overload), EDF delays *every* flight (domino), while FPP delays coach (first-class always boards) — predictable degradation.

## 7. Formal Definition
- **Hard RT**: deadline miss = system failure. **Soft RT**: miss = degraded quality.
- **WCET**: worst-case execution time (measured/analyzed).
- **Periodic task**: (period T, deadline D ≤ T, WCET C). Utilization U = Σ C_i/T_i.
- **RMS schedulability** (rate-monotonic, priorities by period): U ≤ n·(2^(1/n) − 1); n=1 → 1.0; n→∞ → ln 2 ≈ 0.693 (sufficient, not necessary).
- **EDF schedulability**: U ≤ 1 (necessary and sufficient for fully preemptive, independent periodic tasks).
- **WCRT**: R_i = C_i + Σ_{j ∈ hp(i)} ⌈R_i/T_j⌉ · C_j — fixed-point iteration.
- **CBS/SCHED_DEADLINE**: each task a budget (runtime) refilled every period; server is EDF among servers.

## 8. Example
Two tasks: T1 (C=2, T=4, U=0.5), T2 (C=1, T=8, U=0.125). U_total = 0.625.
- RMS bound n=2: 2·(√2 − 1) ≈ 0.828. 0.625 < 0.828 → RMS guarantees schedulability. Priorities: T1 (shorter period) higher.
- EDF: U=0.625 ≤ 1 → schedulable, EDF optimal.
- Trace (RMS): T1 runs 0-2, T2 runs 2-3, T1 runs 4-6, T2 6-7, ... all deadlines met.

## 9. Internal Working
1. **Fixed-priority**: ready queue ordered by static priority; preemptive dispatcher; timer ticks + wakeup preemption (same as priority scheduling — Part 03 Ch 2 Sec 4).
2. **EDF**: ready queue = earliest deadline first (min-heap by deadline); on each arrival, compare deadlines → possibly preempt.
3. **Linux SCHED_DEADLINE**: CBS server — each task has runtime/period/deadline; the server is EDF among servers, with throttling when budget expires (`dl_throttled`).
4. **Interrupt handling**: hard RT requires bounded interrupt latency + fast ISR (top half) + deferred task (bottom half) with priority.
5. **Analysis step**: WCET from timing analysis; WCRT per task; acceptance test at admission (Linux rejects a SCHED_DEADLINE task if U would exceed 100%).

## 10. Time Complexity
- FPP pick-highest: O(1) (bitmap, Linux RT / RTOS).
- EDF: O(log n) heap insert/extract; admission test O(1) utilization check.
- WCRT analysis: iterative, converges in O(n) iterations typically.
- RMS bound check: O(n).
- CBS budget management: O(1) per arrival/refill.

## 11. Advantages
- **Hard guarantees** (with analysis) — provable deadlines.
- **FPP deterministic**: predictable overload behavior (low-priority tasks miss first).
- **EDF optimal**: maximum utilization (U → 1) while meeting deadlines.
- **Linux**: SCHED_DEADLINE gives EDF + bandwidth isolation in the general kernel.
- **Predictable degradation** — key for safety-critical systems.

## 12. Disadvantages
- Requires **WCET** knowledge (hard to measure; over-approximation wastes CPU).
- **EDF overload** → domino: even high-priority tasks miss deadlines.
- **FPP** is not optimal utilization-wise (bound 0.693 as n→∞).
- Blocking (locks) breaks the model → needs priority inheritance/ceiling protocols.
- Analysis assumes independence, preemption, no interrupts — reality is messier.
- Scheduling overhead + admission tests cost; non-preemptible sections add release jitter.

## 13. Interview Questions
1. **Q: What is a real-time system?** A: One whose correctness depends on *when* results are produced — deadlines must be met. Hard RT: miss = failure; soft RT: miss = degraded quality.
2. **Q: What's the difference between hard and soft real-time?** A: Hard = deadline miss is catastrophic (flight control); soft = deadline miss just degrades quality (video call). Guarantees vs best-effort.
3. **Q: What is Rate Monotonic Scheduling (RMS)?** A: Fixed-priority scheduling where priority is inversely proportional to period (shorter period = higher priority); schedulable if U ≤ n(2^(1/n)−1).
4. **Q: What is EDF?** A: Earliest Deadline First — run the task with the earliest deadline; optimal for meeting deadlines (if any schedule works, EDF works) up to U ≤ 1.
5. **Q (TRICKY): Why is EDF optimal but rarely used in hard RTOS?** A: EDF is utilization-optimal, but under overload it degrades catastrophically (all deadlines missed — no priority hierarchy), and it needs exact deadlines/WCET. Fixed-priority gives predictable degradation — low-priority misses first — so most safety-critical systems choose FPP.
6. **Q: What's WCET?** A: Worst-case execution time — the guaranteed upper bound a task needs (analysis/measurement); it's the input to all schedulability math.
7. **Q: What's SCHED_DEADLINE in Linux?** A: The EDF class (deadline-based) with a CBS server per task (runtime/period budget) — hard-ish real-time guarantees in the general kernel.
8. **Q: What is schedulability analysis?** A: A priori proof that all tasks meet deadlines: utilization tests (RMS/EDF) or worst-case response time (WCRT) fixed-point iteration.
9. **Q: How do locks affect RT scheduling?** A: A high-priority task blocked on a low-priority task's lock causes priority inversion — RTOS uses priority inheritance or priority ceiling protocols to bound blocking.
10. **Q (PRODUCTION): You have a 1ms-period sensor task, 5ms CPU task, 2ms RTOS overhead. Is it schedulable?** A: Depends on WCETs. If U = ΣC/T ≤ bound (RMS) or ≤ 1 (EDF) AND overhead accounted, yes. E.g., C=0.3/0.5: U=0.4 ≤ 0.828 → RMS schedulable.
11. **Q: What is jitter?** A: Variation in task release/response times. Hard RT needs bounded jitter (timer resolution, interrupt latency, preemption overhead all contribute).
12. **Q: Why do RTOSes prefer fixed priority over time-slicing?** A: Time-slicing (RR) gives no deadline guarantee; fixed priority + preemption gives deterministic, analyzable response — the only model with provable deadlines.

## 14. Follow-Up Questions
1. **Q: What is priority ceiling protocol (PCP)?** A: A task's effective priority is raised to the ceiling of the resources it might lock → prevents deadlock and bounds blocking, stronger than inheritance.
2. **Q: What's the difference between aperiodic and periodic tasks?** A: Periodic: fixed period, deadline each period. Aperiodic/sporadic: arrival times unknown; served by servers (sporadic server, CBS) to keep budget isolation.
3. **Q: What is the "domino effect"?** A: In EDF overload, missing one deadline cascades — the scheduler chases overdue deadlines and misses more.
4. **Q: How does PREEMPT_RT make Linux real-time?** A: Makes the kernel preemptible (spinlocks → rtmutexes with PI), bounded kernel latency → usable for soft and some hard RT.
5. **Q: What's a "tickless" RTOS?** A: NO_HZ-style — no periodic tick; wakeup-timer-driven (hrtimers) → lower jitter, less overhead, better energy.

## 15. Coding Example
```c
/* RMS schedulability test + EDF admission test */
#include <stdio.h>

typedef struct { double c, t; } task;  /* WCET, period */

double rms_bound(int n) {              /* n(2^(1/n) - 1) */
    double p = 1.0 / n;
    double two = 1.0;
    for (int i = 0; i < n; i++) two *= 2.0;
    /* approx: use pow */
    return n * (__builtin_pow(2.0, p) - 1.0);
}

int main(void) {
    task tasks[] = {{2,4},{1,8}};
    int n = 2;
    double u = 0;
    for (int i = 0; i < n; i++) u += tasks[i].c / tasks[i].t;
    printf("U = %.3f, RMS bound = %.3f -> %s\n", u, rms_bound(n),
           u <= rms_bound(n) ? "SCHEDULABLE" : "NOT guaranteed by RMS");
    printf("EDF: U <= 1 -> %s\n", u <= 1.0 ? "SCHEDULABLE" : "OVERLOAD");
    return 0;
}
```
```bash
# Linux SCHED_DEADLINE (EDF with CBS) via sched_setattr
# runtime/period in ns: e.g. 2ms in 10ms period = 20% bandwidth
python3 - <<'EOF'
import os, ctypes
sched_attr = ctypes.c_ubyte * 56  # simplified; use real struct on system
EOF
# chrt -d --sched-runtime 2000000 --sched-deadline 3000000 --sched-period 10000000 ./task
```

## 16. Industry Usage
- **Automotive**: AUTOSAR OS (fixed-priority), ECU control loops.
- **Aerospace**: ARINC 653 partitions + fixed-priority/RMS.
- **Industrial**: IEC 61131-3 PLC runtimes (fixed-priority cyclic).
- **Robotics**: ROS2 + Linux RT / QNX — control loops with deadlines.
- **Networking/telecom**: soft RT packet processing (DPDK, RT classes).
- **Audio/video**: soft RT audio threads (SCHED_FIFO on Linux, REALTIME on Windows).
- **Linux SCHED_DEADLINE**: live migration, video decode, cloud networking.

## 17. References
- Liu & Layland, "Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment" (JACM 1973) — RMS/EDF origin.
- Burns & Wellings, *Real-Time Systems and Programming Languages*.
- Silberschatz, *OS Concepts*, Ch. 6.7 (real-time).
- Linux: `Documentation/scheduler/sched-deadline.rst`, `kernel/sched/deadline.c`.
- FreeRTOS/QNX/VxWorks RTOS documentation.

## 18. Cheat Sheet
- Hard RT: miss = fail. Soft RT: miss = degraded.
- FPP (fixed-priority preemptive): RTOS default; RMS priority by period.
- RMS bound: U ≤ n(2^(1/n)−1) → → ln 2 ≈ 0.693.
- EDF: earliest deadline; optimal; U ≤ 1; domino under overload.
- WCRT: R = C + Σ ⌈R/T⌉·C (fixed point).
- WCET: input to all analysis; must be known/bounded.
- Linux SCHED_DEADLINE = EDF + CBS budget.
- Locks → priority inheritance/ceiling (bound blocking).
- Jitter = variation in release/response — bound it.
- Predictable degradation: FPP loses low-priority first; EDF loses all.

## 19. Quiz
1. Hard RT deadline miss: a) warning b) system failure c) retry d) demote → **b**
2. RMS priority by: a) importance b) period c) burst d) arrival → **b**
3. RMS bound n→∞: a) 1.0 b) ln2 ≈ 0.693 c) 0.5 d) 2 → **b**
4. EDF optimal for: a) avg TAT b) meeting deadlines c) fairness d) overhead → **b**
5. EDF schedulability: a) U ≤ 0.693 b) U ≤ 1 c) U ≤ 2 d) none → **b**
6. EDF overload causes: a) low-prio misses b) domino c) no effect d) boost → **b**
7. WCET is: a) average b) worst-case bound c) best case d) quantum → **b**
8. SCHED_DEADLINE is: a) FPP b) EDF+CBS c) RR d) CFS → **b**
9. Jitter means: a) latency b) variation in timing c) overhead d) priority → **b**
10. RTOS locks use: a) aging b) priority inheritance/ceiling c) boosting d) quantum → **b**

## 20. Flashcards
- **Q: Hard vs soft RT?** → **A:** Miss=fail vs miss=degraded.
- **Q: RMS?** → **A:** Priority by period; bound n(2^(1/n)−1).
- **Q: EDF?** → **A:** Earliest deadline; optimal; U≤1.
- **Q: Domino?** → **A:** EDF overload cascades.
- **Q: WCET?** → **A:** Worst-case exec time (analysis input).
- **Q: SCHED_DEADLINE?** → **A:** EDF + CBS budget in Linux.
- **Q: Locks in RT?** → **A:** Priority inheritance/ceiling.
- **Q: Why FPP over RR?** → **A:** Analyzable, predictable degradation.

## 21. Revision
Real-time scheduling trades fairness for *guarantees*: fixed-priority preemptive (RMS — priority by period, bound n(2^(1/n)−1)) is the deterministic RTOS default, EDF is utilization-optimal (U≤1) but domino-prone under overload. Everything hinges on known WCET and schedulability analysis (utilization or WCRT). Linux provides SCHED_FIFO/RR (soft) and SCHED_DEADLINE (EDF+CBS, harder); locks require priority inheritance/ceiling; jitter must be bounded.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a real-time system?" | 13 Q1 / 7 Formal Definition |
| "Hard vs soft?" | 13 Q2 / 3 When Is It Used |
| "What is RMS?" | 13 Q3 / 7 Formal Definition |
| "What is EDF?" | 13 Q4 / 7 Formal Definition |
| "Why EDF rare in RTOS?" | 13 Q5 / 4 Why Wasn't Another Approach Chosen |
| "What is WCET?" | 13 Q6 / 2 How Does It Work |
| "SCHED_DEADLINE?" | 13 Q7 / 16 Industry Usage |
| "Schedulability analysis?" | 13 Q8 / 9 Internal Working |
| "Locks in RT?" | 13 Q9 / 12 Disadvantages |
| "Is my workload schedulable?" | 13 Q10 / 8 Example |
