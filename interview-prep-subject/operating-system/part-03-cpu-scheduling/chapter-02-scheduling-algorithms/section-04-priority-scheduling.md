# Section 04: Priority Scheduling

> **TL;DR**: Priority scheduling runs the highest-priority ready task; priorities express importance. Preemptive version switches to a higher-priority newcomer immediately. Its fatal flaw — starvation and priority inversion — is why aging and priority inheritance exist.

## 1. Why Does This Exist?
FCFS, SJF, and RR treat all tasks as equal. Real systems need *hierarchy*: a network packet handler, a heartbeat thread, or an audio DMA must beat a background batch job. Priority scheduling exists to encode importance — a number that says "this task matters more." It's the backbone of real-time OSes (fixed-priority preemptive) and is layered under every production scheduler (Windows priority classes, Linux `nice`/RT classes, macOS QoS).

## 2. How Does It Work?
- Each process has a priority (static or dynamic). Ready queue ordered by priority.
- Non-preemptive: when CPU frees, pick highest priority. Preemptive: if a newly-ready task has higher priority than the running one, preempt immediately.
- Priorities are usually *ranges* (Linux: -20..19 `nice`, RT 1..99; Windows: 0-31; FreeRTOS: 0..configMAX_PRIORITIES-1).
- Dynamic priorities: I/O-bound tasks boosted, CPU-bound decayed (e.g., Windows foreground boost).

## 3. When Is It Used?
- **Real-time OSes**: fixed-priority preemptive scheduling (FreeRTOS, QNX, VxWorks) — the standard.
- **Windows NT**: priority classes × levels; interactive threads get boosts.
- **Linux**: RT classes (`SCHED_FIFO/RR` 1-99) sit above CFS fair class; `nice` maps to CFS weight.
- **Networking/GPUs**: priority queues for traffic/flows.
- **Every production OS** uses some priority dimension, even if the base policy is fair.

## 4. Why Wasn't Another Approach Chosen?
- **FCFS/RR/SJF**: no notion of importance — you can't tell the scheduler "this must run first." Rejected for anything with deadlines/importance.
- **EDF**: better for real-time but needs deadlines, is fragile under overload (domino effect), and complicates priority inheritance.
- **Proportional share (CFS)**: weights exist but you *can't* express hard "run this now" requirements.
Priority scheduling chose the *simple, expressive, deterministic* model: a scalar per task. Its defects (starvation, inversion) are handled by **aging** and **priority inheritance** — small add-ons that keep the model.

## 5. Intuition
**An emergency room triage**: patients are prioritized (critical first) rather than served in arrival order. The ER always treats the most severe case. But a stream of "critical" patients can starve the walking-wounded forever (starvation), and a doctor stuck with a low-priority patient holding the only tool while a critical patient needs it is priority inversion in the flesh.

## 6. Real-World Analogy
**Airport check-in with priority lanes**: first-class (high priority) always goes ahead; coach (low priority) waits — and if first-class keeps arriving, coach never moves (starvation → fix with aging, "max wait time → force serve"). And if a first-class passenger is stuck behind a coach passenger at a broken kiosk (low-priority task holds a resource a high-priority task needs), that's priority inversion — resolved by letting the coach passenger "inherit" priority temporarily.

## 7. Formal Definition
- A priority p_i ∈ ℕ per process; ready queue ordered by p (ties → FCFS).
- **Preemptive version**: running task preempted iff ∃ ready j with p_j > p_current.
- **Aging**: priority boosted over waiting time: p_i(t) = p_i + f(wait_i) — guarantees progress.
- **Priority inversion**: high-priority task H blocked on a resource held by low-priority L, while medium M (p_L < p_M < p_H) runs and prevents L → H is effectively blocked by M.
- **Priority inheritance**: L temporarily takes p_H while holding the resource → M can't run → H proceeds.

## 8. Example
Priorities: A(1, CPU-bound), B(3), C(2), all ready, preemptive.
- Runs B (3) to completion, then C (2), then A (1). Deterministic order.
- Starvation demo: A(1) ready forever while higher-priority jobs keep arriving — A starves without aging.
- Inversion demo: H(5) needs lock held by L(1); M(3) runs → H blocked by M, not L. Fix: L inherits 5.

## 9. Internal Working
1. Ready queue = priority queue (array of FIFOs per priority level, or rbtree — Linux RT uses bitmap + FIFO per level).
2. Dispatch: O(1) bitmap find-highest-set-bit → head of that level.
3. Preemptive: on wakeup (`try_to_wake_up`), if new priority > running's, `resched_curr()`.
4. Linux: RT prios 1-99 bitmap; `sched_find_first_bit()` finds highest; FIFO within same prio. CFS `nice` (nice = 20 - prio) maps to weight via `sched_prio_to_weight[]`.
5. Inversion handled by priority inheritance (PI): `rt_mutex_setprio()` on lock acquisition.

## 10. Time Complexity
- Pick highest priority: O(1) with bitmap (Linux RT).
- Insert: O(1) (append to level's FIFO).
- Preemption check on wakeup: O(1).
- Aging (if dynamic): O(1) periodic or O(log n) if using heaps.
- Windows: 32 levels → O(1) bitmap-ish.

## 11. Advantages
- **Express importance** — essential for real-time and interactive responsiveness.
- **Deterministic** (fixed priority, preemptive) — provable response bounds for RT.
- Simple, O(1) implementation with bitmaps/FIFO-per-level.
- Priority inheritance gives clean synchronization (RT mutexes).
- Layered cleanly: RT above fair in Linux, classes in Windows.

## 12. Disadvantages
- **Starvation**: low-priority tasks can wait indefinitely (needs aging).
- **Priority inversion**: requires inheritance/deadlock-avoidance machinery.
- Static priority doesn't adapt to changing importance (dynamic policies add complexity).
- Choosing priorities is policy guesswork; wrong choices mis-schedule.
- Inversion/preemption storms: high-priority burst can starve everything else.

## 13. Interview Questions
1. **Q: What is priority scheduling?** A: Ready queue ordered by priority; highest-priority ready task runs; preemptive version switches to a newly-ready higher-priority task immediately.
2. **Q: What is aging?** A: Boost a waiting task's priority with time — guarantees low-priority tasks eventually run (starvation prevention).
3. **Q: What is priority inversion?** A: High-priority H blocked on a resource held by low-priority L; a medium-priority M runs and delays L, so H is effectively blocked by M.
4. **Q: What is priority inheritance?** A: While L holds the resource H needs, L temporarily inherits H's priority — M can't preempt L, so L finishes and H proceeds. Standard fix for inversion.
5. **Q (SCENARIO): Give a real inversion example.** A: Mars Pathfinder — a sensor mutex held by a low-priority task was blocked by medium-priority tasks; high-priority data collection starved → watchdog resets. Fixed by enabling priority inheritance in VxWorks.
6. **Q (TRICKY): Does Linux CFS have priorities?** A: Sort of — `nice` (-20..19) maps to a *weight* affecting share, not a hard rank. True hard priorities are the RT classes (1-99) which preempt the fair class entirely.
7. **Q: What's the priority range in Linux?** A: `nice` -20 (highest fair weight) to +19; RT 1 (lowest RT) to 99 (highest); SCHED_DEADLINE above all RT. Windows: 0-31.
8. **Q: How does priority scheduling cause starvation?** A: Continuous arrival of higher-priority jobs means low-priority ones never run; aging or share-based policies prevent it.
9. **Q: What's the difference between static and dynamic priorities?** A: Static = fixed at creation (RT). Dynamic = adjusted at runtime (Windows boosts interactive threads; aging boosts waiters).
10. **Q: Why does FreeRTOS use fixed-priority preemptive?** A: Determinism — the highest-priority ready task always runs, giving bounded response for critical tasks; priorities are the RT model.
11. **Q (TRICKY): Priority inversion can't happen with spinlocks — why?** A: Spinlocks disable preemption while held, so a medium task can't run while L spins (single CPU). On SMP it can still invert between CPUs, but RT mutexes (PI) are preferred. True statement for uniprocessor.
12. **Q: How are ties broken in priority scheduling?** A: Usually FCFS within the same priority level (Linux RT: FIFO within a prio; SCHED_RR adds a quantum).

## 14. Follow-Up Questions
1. **Q: What's the difference between priority and nice in Linux?** A: RT priority = hard rank (preemption). `nice` = weight within the fair scheduler — influences share, not exclusivity.
2. **Q: How is priority inversion solved in Windows?** A: Priority boosting + balance set manager + critical-section waiter boosting.
3. **Q: What is an unbounded priority inversion?** A: Inversion where H's wait grows unboundedly with M's runtime (no inheritance) — the Mars Pathfinder bug.
4. **Q: How do you implement aging?** A: Periodic boost: priority += wait/age_factor, or re-evaluate on a timer; ensure it converges so every task gets CPU.
5. **Q: What is the relationship to MLFQ?** A: MLFQ *is* dynamic priority scheduling with multiple queues — priority changes based on behavior (short CPU bursts get boosted).

## 15. Coding Example
```c
/* Priority scheduling simulation + aging */
#include <stdio.h>
#include <stdlib.h>

typedef struct { int id, prio, burst, wait; } job;

job q[16]; int n = 0;

int pick(void) {  /* highest priority; ties FCFS */
    int b = 0;
    for (int i = 1; i < n; i++)
        if (q[i].prio > q[b].prio) b = i;
    return b;
}

void age(void) {  /* aging: boost waiters */
    for (int i = 0; i < n; i++) q[i].prio += q[i].wait / 10;
}

int main(void) {
    job jobs[] = {{0,1,5,0},{1,3,2,0},{2,2,3,0}};
    n = 3; for (int i = 0; i < n; i++) q[i] = jobs[i];
    int t = 0;
    while (n > 0) {
        int b = pick();
        printf("job%d (prio %d) runs %d..%d\n", q[b].id, q[b].prio,
               t, t + q[b].burst);
        t += q[b].burst;
        q[b] = q[--n];   /* remove */
        for (int i = 0; i < n; i++) q[i].wait += q[b].burst;
        age();
    }
    return 0;
}
```
```bash
# Linux priorities
nice -n -5 ./server &      # boost fair weight of server
chrt -f -p 80 $$           # RT FIFO priority 80
ps -e -o pid,ni,rtprio,comm
```

## 16. Industry Usage
- **FreeRTOS / QNX / VxWorks**: fixed-priority preemptive — the dominant RTOS model.
- **Windows**: priority classes (IDLE..REALTIME) × 0-31 levels; foreground boosts; critical sections boost waiters.
- **Linux**: RT classes above CFS; `nice`; `SCHED_DEADLINE`. PI mutexes in `rtmutex`.
- **macOS/iOS**: QoS classes (user-interactive → background) — priority per service class.
- **Networking**: priority queues in NICs/switches for QoS.
- Every RTOS interview question eventually touches priority + inversion.

## 17. References
- Silberschatz, *OS Concepts*, 6.3.5 (Priority) & Ch 8 (inversion/PI).
- Tanenbaum, *Modern OS*, 2.4.7 (priority), 2.3.6 (inversion).
- Mars Pathfinder bug: JPL "What really happened on Mars?" (Mike Jones, 1997).
- Linux: `kernel/sched/rt.c`, `rtmutex.c`, man `sched(7)`, `chrt(1)`, `nice(1)`.
- FreeRTOS docs: priority/preemption; Windows Internals (priority model).

## 18. Cheat Sheet
- Priority = importance rank; preemptive version = higher-prio preempts.
- Tie → FCFS within priority level.
- Aging fixes starvation (boost waiters).
- Priority inversion: H blocked on L's resource, M (middle) preempts L → H effectively blocked by M.
- Fix: priority inheritance (L takes H's prio while holding).
- Mars Pathfinder: real inversion → watchdog reset.
- Linux: nice = weight (fair); RT 1-99 = hard rank; DEADLINE above.
- Windows: 0-31 levels, classes; boosts for interactivity.
- Pick-highest: O(1) bitmap (Linux RT).

## 19. Quiz
1. Preemptive priority scheduling switches when: a) quantum expires b) higher-prio ready c) FCFS tie d) never → **b**
2. Aging prevents: a) inversion b) starvation c) preemption d) fragmentation → **b**
3. Priority inheritance: a) boosts H b) boosts L while holding c) boosts M d) nothing → **b**
4. Mars Pathfinder bug was: a) deadlock b) inversion c) starvation d) quantum → **b**
5. Linux RT priority range: a) 0-19 b) 1-99 c) -20-19 d) 0-31 → **b**
6. Windows levels: a) 1-99 b) 0-31 c) -20-19 d) 0-7 → **b**
7. `nice` affects: a) RT order b) fair share weight c) quantum d) memory → **b**
8. Linux picks RT highest via: a) linear scan b) bitmap c) heap d) rbtree → **b**
9. Tie within priority: a) SJF b) FCFS c) RR always d) random → **b**
10. Priority inversion fix: a) aging b) inheritance c) RR d) preemption → **b**

## 20. Flashcards
- **Q: Priority scheduling?** → **A:** Highest-priority ready runs; preemptive variant.
- **Q: Aging?** → **A:** Boost waiters' priority → no starvation.
- **Q: Inversion?** → **A:** H blocked on L's resource; M delays L.
- **Q: Inheritance?** → **A:** L takes H's prio while holding resource.
- **Q: Mars bug?** → **A:** Unbounded inversion → watchdog reset; fixed by PI.
- **Q: Linux nice?** → **A:** Fair weight, not hard rank.
- **Q: RT range?** → **A:** 1-99, above CFS.
- **Q: Pick cost?** → **A:** O(1) bitmap.

## 21. Revision
Priority scheduling ranks tasks by importance and runs the highest-priority ready task, preempting on higher-priority wakeups — the model behind FreeRTOS/QNX and layered under Windows and Linux. Two defects define the interview: starvation (fixed by aging) and priority inversion (fixed by priority inheritance — H blocked on L's resource while M runs). Linux encodes priorities two ways: hard RT ranks (1-99, bitmap O(1)) and `nice` weights in the fair class.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is priority scheduling?" | 13 Q1 / 7 Formal Definition |
| "What is aging?" | 13 Q2 / 9 Internal Working |
| "What is priority inversion?" | 13 Q3 / 7 Formal Definition |
| "What is priority inheritance?" | 13 Q4 / 8 Example |
| "Real inversion example?" | 13 Q5 / 16 Industry Usage |
| "Linux priorities?" | 13 Q6 / 7 Formal Definition |
| "Priority ranges?" | 13 Q7 / 9 Internal Working |
| "How does it starve?" | 13 Q8 / 12 Disadvantages |
| "Spinlocks vs inversion?" | 13 Q11 / 9 Internal Working |
