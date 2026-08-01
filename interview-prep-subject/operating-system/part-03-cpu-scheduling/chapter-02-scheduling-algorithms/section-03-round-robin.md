# Section 03: Round Robin (RR)

> **TL;DR**: Round Robin gives every ready process a fixed CPU time slice (quantum) in a circular FIFO — preemption by timer. It delivers the best worst-case response time of the simple algorithms, at the cost of average turnaround (quantum size tunes the tradeoff).

## 1. Why Does This Exist?
FCFS and SJF both let a long job monopolize the CPU, destroying response time — the killer metric for interactive systems. Round Robin exists to answer: *how do we give every process a fair, bounded chance to use the CPU?* By time-slicing in a circle, RR bounds how long any process waits before its next quantum — guaranteed responsiveness. It's the preemptive foundation of time-sharing, and it's why your terminal still responds while a heavy build runs.

## 2. How Does It Work?
- A FIFO ready queue of processes.
- The head runs for at most one *quantum* q (e.g., 10-100ms).
- On timer expiry, preempt, push it to the tail, dispatch the next head.
- If a process blocks (I/O) before q expires, it leaves the queue and rejoins at the tail when ready.
- Repeat forever — a rotating circle.

## 3. When Is It Used?
- Default choice for **interactive/time-sharing** systems where response time matters.
- Inside MLFQ as the base policy at the highest-priority queues.
- Embedded/RTOS with time-slicing (FreeRTOS round-robin among equal priorities).
- Anywhere you want fairness among equal-priority peers.

## 4. Why Wasn't Another Approach Chosen?
- **FCFS/SJF**: no response bound — rejected for interactivity.
- **Priority**: unfair to low-priority tasks; RR is fair *by construction* (no priorities needed).
- **MLFQ**: the right answer for production, but needs the complexity of multiple queues; RR is the minimal fair preemptive policy.
RR is chosen for its **simplicity + guaranteed response bound**. The price (extra context switches, worse average TAT) is the reason MLFQ layers RR on top rather than using it alone.

## 5. Intuition
**A round of sharing a single slice of pizza**: everyone gets a bite (quantum), then the plate passes to the next person in a circle. Nobody waits long for the plate, but the pizza takes longer overall (many passes). If bites are tiny, everyone gets frequent tiny tastes (great response, tons of passes/overhead); if bites are huge, it's basically FCFS.

## 6. Real-World Analogy
**A shared conference room on a strict schedule**: each team books 15 minutes (quantum), then hands the room to the next team regardless of where they are (timer preemption). Teams get predictable access — a team arriving at the top of the hour always gets its slot within ~15 min (bounded response). But a project that needs 2 hours straight is forced to split it into 8 sessions (TAT suffers, plus setup overhead).

## 7. Formal Definition
- Preemptive scheduling: ready queue = FIFO; each process runs ≤ q; on expiry it moves to tail; block → leaves and rejoins at tail.
- **Response time bound**: worst-case time until a task's first quantum ≈ (number of ready tasks) × q.
- Given n tasks and quantum q: maximum wait for next CPU ≈ (n-1)·q + q = n·q.
- **TAT tradeoff**: average turnaround grows with n and q; small q → better response, worse throughput (more switches); large q → FCFS-like.

## 8. Example
Jobs: A(5), B(3), C(1), arrival 0, q=2.
- A:0-2, B:2-4, C:4-5 (done), A:5-7, B:7-8 (done), A:8-10.
- TAT: A=10, B=8, C=5 → avg 7.67. (Compare SJF: order C,B,A → TAT 1,4,9 avg 4.67 — RR trades TAT for response.)
- Response: A gets CPU at 0 (0), B at 2, C at 4 → avg 2.0 — much better than FCFS's worst case.

## 9. Internal Working
1. Timer configured for q (e.g., `hrtimer`/local APIC); ticks fire.
2. On expiry: `scheduler_tick()` → mark current need_resched → `__schedule()`.
3. Current task's context saved; pushed to tail of runqueue; next head loaded — a **context switch** (Part 02 Ch 4).
4. If a task blocks: it exits the runqueue; on wakeup it's appended to the tail (Fair: in CFS there's no literal round-robin of the queue — RR is used in MLQ/priority tiers; but conceptually identical).
5. Overhead: each quantum boundary = 1+ context switches (switch out + switch in next).

## 10. Time Complexity
- Enqueue/dequeue: O(1) (FIFO).
- Timer tick handling: O(1).
- Context switches per quantum: 2 (out + in) per preemption.
- **Average wait ≈ (n-1)·q/2** (uniform arrivals) — grows linearly with quantum and n.
- Total overhead ∝ (total CPU time / q) × context-switch-cost — smaller q = more overhead.

## 11. Advantages
- **Bounded response time** — worst case ≈ n·q — the key metric for interactivity.
- **Fairness**: every process gets equal CPU share; no starvation.
- Simple O(1) implementation; no burst prediction.
- Predictable behavior; the base for MLFQ's top tiers.

## 12. Disadvantages
- **Worse average TAT than SJF** — quantum slicing fragments long jobs.
- Context-switch overhead scales inversely with q.
- q too small → thrashing (switching overhead dominates); q too large → FCFS-like response loss.
- Not optimal by any single objective (suboptimal TAT, suboptimal response for longest).
- No priority support alone (needs layering).

## 13. Interview Questions
1. **Q: What is Round Robin?** A: Preemptive, FIFO, fixed quantum q; a process runs ≤ q, then preempts to the tail; every process gets a fair slice.
2. **Q: Why does RR exist?** A: To bound worst-case response time for interactive systems — FCFS/SJF let long jobs monopolize the CPU.
3. **Q (TRICKY): What happens if quantum → ∞?** A: RR degenerates to FCFS (run to completion). Quantum → 0: pure context-switch overhead, zero work — so q must balance overhead vs response.
4. **Q: How does quantum size affect performance?** A: Small q → better response, more switches, worse throughput; large q → worse response, less overhead, FCFS-like. Typical: 10-100ms (Linux tick ~4ms, but CFS doesn't use fixed ticks).
5. **Q: What's the worst-case response time for n processes, quantum q?** A: ≈ n·q — a process can wait at most for all others to finish their slices.
6. **Q: Why is average TAT worse than SJF?** A: SJF finishes short jobs early; RR forces even the shortest job to wait up to n·q and fragments long jobs into slices.
7. **Q: Does RR starve a process?** A: No — every process periodically returns to the head; no starvation by construction.
8. **Q (SCENARIO): A has burst 10, B burst 2, C burst 2, q=4, arrival 0. Compute avg TAT.** A: A:0-4, B:4-6(done), C:6-8(done), A:8-14. TAT: 14, 6, 8 → avg 9.33. SJF (2,2,10): 2+4+14=20/3=6.67.
9. **Q: How does RR handle I/O-bound tasks?** A: They block quickly and return to the tail; their frequent short CPU needs get served each round — good interaction, but they add switching overhead.
10. **Q: What is a "preemptive" in RR?** A: The timer interrupt firing mid-quantum forces the switch — the only preemption source; block/exit also release but voluntarily.
11. **Q: Why use RR inside MLFQ?** A: At the highest-priority queues, RR gives fair, responsive service to the short/interactive tasks that dominate real workloads; deeper queues use RR too but with bigger quanta.
12. **Q (TRICKY): Is RR optimal for response time?** A: For *max-min* response among equal-priority tasks with zero context-switch cost, RR is near-optimal; with switching overhead, larger quanta win. No single q is optimal across workloads — hence adaptive policies.

## 14. Follow-Up Questions
1. **Q: What's the relationship between RR and context switches?** A: Each quantum boundary costs ~2 switches; overhead ∝ (total runtime)/q × switch cost.
2. **Q: How do you choose q?** A: q ≫ context-switch time (else overhead); q ≤ target response time / n. Many systems use 20-50ms.
3. **Q: What's the difference between RR and time-slicing?** A: Same thing — time-slicing is RR with a quantum; "time slice" = quantum.
4. **Q: Does CFS use RR?** A: No — CFS is fair-share (vruntime), not fixed-slice. But MLQ/priority kernels (macOS) and equal-priority FreeRTOS tiers use RR. SCHED_RR in Linux *is* classic RR among equal RT priorities.
5. **Q: What is Linux's SCHED_RR?** A: A real-time scheduling class: tasks of equal RT priority share the CPU round-robin with a time slice (default ~100ms); higher-priority RT preempts immediately.

## 15. Coding Example
```c
/* Round Robin scheduler simulation with a circular FIFO */
#include <stdio.h>

#define Q 2 /* quantum */
typedef struct { int id, burst, remain; } job;

void round_robin(job *j, int n) {
    int t = 0, done = 0, cur = 0;
    while (done < n) {
        if (j[cur].remain > 0) {
            int slice = j[cur].remain > Q ? Q : j[cur].remain;
            printf("t=%d job%d runs %d..%d (slice %d)\n", t, j[cur].id,
                   t, t+slice, slice);
            j[cur].remain -= slice; t += slice;
            if (j[cur].remain == 0) {
                printf("  job%d done (TAT %d)\n", j[cur].id, t);
                done++;
            }
        }
        cur = (cur + 1) % n; /* circular FIFO */
    }
}

int main(void) {
    job jobs[] = {{0,5,5},{1,3,3},{2,1,1}};
    round_robin(jobs, 3);
    return 0;
}
```
```bash
# Linux SCHED_RR (round-robin among equal RT priorities)
chrt -r -p 50 $$        # SCHED_RR priority 50
cat /proc/$$/sched      # shows rr_interval (~100ms default)
```

## 16. Industry Usage
- **Linux SCHED_RR**: round-robin for equal-priority real-time threads (`sched_setscheduler(2)`).
- **Windows NT**: dispatcher uses priority + time slice (~2 quanta); interactive threads get boost — a priority+RR hybrid.
- **macOS**: MLQ with RR at the top priorities.
- **FreeRTOS**: round-robin time-slicing among equal-priority tasks (config).
- **Network scheduling**: DRR (Deficit Round Robin) — weighted RR for fair bandwidth.
- Every interactive OS effectively implements RR at some tier — it's the response-time safety net.

## 17. References
- Silberschatz, *OS Concepts*, 6.3.4 (RR).
- Tanenbaum, *Modern OS*, 2.4.6 (RR).
- Linux: `include/linux/sched.h` (SCHED_RR), `kernel/sched/rt.c`, man `sched(7)`, `chrt(1)`.
- FreeRTOS docs: time slicing.
- Cormen, *CLRS* (queues); queuing theory texts for M/M/1 RR results.

## 18. Cheat Sheet
- RR = FIFO + quantum q + timer preemption; every process gets q.
- Worst-case response ≈ n·q; avg wait ≈ (n-1)q/2.
- q→∞ : FCFS. q→0 : thrash. Sweet spot: q ≫ switch cost.
- Costs: ~2 context switches per quantum.
- No starvation; no burst prediction needed.
- Better response than FCFS/SJF; worse TAT than SJF.
- In Linux: SCHED_RR (RT class); CFS is not RR.
- Used as the base policy in MLFQ top queues and FreeRTOS.

## 19. Quiz
1. RR guarantees: a) optimal TAT b) bounded response c) priorities d) deadlines → **b**
2. q→∞ makes RR: a) SJF b) FCFS c) MLFQ d) EDF → **b**
3. Worst-case response for n procs: a) n+q b) n·q c) q/n d) 2n → **b**
4. RR average wait approx: a) n·q b) (n-1)q/2 c) 0 d) q → **b**
5. RR vs SJF avg TAT: a) RR better b) SJF better c) equal d) depends only on q → **b**
6. Per quantum context switches: a) 0 b) 1 c) ~2 d) n → **c**
7. RR starvation: a) possible b) impossible c) priority-based d) aging → **b**
8. I/O-bound task under RR: a) waits forever b) returns to tail quickly c) preempts all d) dies → **b**
9. Linux's SCHED_RR is: a) CFS b) RT round-robin c) MLFQ d) EDF → **b**
10. Small q downside: a) response b) switching overhead c) fairness d) none → **b**

## 20. Flashcards
- **Q: RR?** → **A:** FIFO + fixed quantum, timer-preemptive.
- **Q: Worst-case response?** → **A:** ≈ n·q.
- **Q: q→∞ ?** → **A:** FCFS.
- **Q: q→0 ?** → **A:** Thrashing.
- **Q: avg wait?** → **A:** ≈ (n-1)q/2.
- **Q: Main tradeoff?** → **A:** Response vs throughput/overhead.
- **Q: Starvation?** → **A:** None.
- **Q: Used where?** → **A:** MLFQ top tiers, SCHED_RR, FreeRTOS.

## 21. Revision
Round Robin is the preemptive FIFO: a fixed quantum q with timer-driven switching gives every process a fair slice and a worst-case response bound of ≈n·q — ideal for interactive workloads. The tradeoff: average turnaround worsens (SJF is better), and context-switch overhead grows as q shrinks (q→∞ = FCFS, q→0 = thrash). It's the base policy of MLFQ's high-priority queues, Linux's SCHED_RR, and FreeRTOS time-slicing.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is Round Robin?" | 13 Q1 / 7 Formal Definition |
| "Why does RR exist?" | 13 Q2 / 1 Why Does This Exist |
| "Quantum → ∞?" | 13 Q3 / 8 Example |
| "Quantum size effect?" | 13 Q4 / 10 Time Complexity |
| "Worst-case response?" | 13 Q5 / 7 Formal Definition |
| "Why worse TAT than SJF?" | 13 Q6 / 12 Disadvantages |
| "RR + I/O-bound?" | 13 Q9 / 3 When Is It Used |
| "RR in MLFQ?" | 13 Q11 / 3 When Is It Used |
| "Is RR optimal for response?" | 13 Q12 / 11 Advantages |
