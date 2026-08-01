# Scheduling Criteria and Goals

> **TL;DR**: Scheduling is judged by measurable criteria — CPU utilization, throughput, turnaround time, waiting time, and response time — which trade off against each other, so every scheduler is a policy choice over which goals matter for its workload.

## 1. Why Does This Exist?
"Scheduling" without goals is just guessing. Criteria exist to make the scheduler's job testable and improvable: they define the *objective function* the OS optimizes (throughput for batch, latency for interactive, determinism for real-time). They also expose the fundamental tensions — you can't maximize both throughput and response time — which is why there are many algorithms instead of one. Every "which scheduling algorithm?" interview question is really "which criteria do you care about, and what does the algorithm optimize?"

## 2. How Does It Work?
The classic metrics (Silberschatz):
- **CPU utilization**: % of time the CPU is doing useful work (`busy / total`). Goal: high for expensive hardware.
- **Throughput**: processes completed per unit time (`n / T`). Goal: maximize.
- **Turnaround time (TAT)**: `completion − arrival` — the full interval from submission to finish. Goal: minimize.
- **Waiting time**: `TAT − burst (CPU time)` — time spent in the ready queue. Goal: minimize.
- **Response time**: `first CPU allocation − arrival` — time until the process *starts* responding (key for interactivity). Goal: minimize.
- **Fairness** (modern): each process gets a fair share (proportional to weight/priority) — the goal Linux's EEVDF formalizes.
Schedulers optimize a weighted combination; preemption, quantum, and priority encode the weights.

## 3. When Is It Used?
- **Batch/HPC**: maximize throughput & utilization (Slurm, big iron).
- **Interactive/desktop**: minimize response time (Linux CFS/EEVDF on desktop).
- **Real-time**: deterministic deadlines (RMS, EDF, SCHED_DEADLINE).
- **Cloud/containers**: fairness + latency isolation (cgroup shares, EEVDF weighted vruntime; CPU bandwidth controls).
- **Interview computations**: given bursts + arrival times, compute TAT/wait/response for each algorithm — the universal question format.

## 4. Why Wasn't Another Approach Chosen?
- **Single metric (only throughput)**: kills interactivity — a batch-only scheduler makes the GUI unusable. Rejected; real systems blend.
- **Single metric (only response)**: fairness/throughput collapse; compute jobs starve. Rejected.
- **No metrics (ad-hoc)**: untestable, unreproducible. Rejected.
- **Fairness as the sole goal (strict round-robin)**: ignores priority and I/O behavior — throughput suffers, priorities break. Rejected; fairness is *weighted* (EEVDF).
- **Hardware-only scheduling (SMT)**: not a policy — the OS still decides which thread on which core.
The chosen approach: a *set* of criteria with weights that vary by workload, encoded in the scheduling policy.

## 5. Intuition
Think of a **single cashier at a store** (the CPU). Metrics answer different questions:
- Utilization: is the cashier ever idle? (Underuse = wasted.)
- Throughput: how many customers are served per hour?
- Turnaround: how long from a customer joining the line until they leave with their bags?
- Waiting: how long just *in line* (not scanning)?
- Response: how soon does the cashier *first* acknowledge you? (Acknowledge fast = interactive; even if scanning takes a while.)
Optimizing one metric can hurt another — the cashier can't acknowledge everyone instantly *and* process long orders fastest.

## 6. Real-World Analogy
An **emergency room triage**: criteria = how many patients seen/hour (throughput), how long until discharge (turnaround), how long in the waiting room (waiting), how quickly a patient is *first* seen by a nurse (response). Triage (priority scheduling) sacrifices "average turnaround" to get critical patients seen quickly (response) — exactly the priority-vs-fairness trade in OS scheduling. The ER is scored on all five, never one.

## 7. Formal Definition
Given jobs with arrival time `a`, CPU burst `b`, completion `c`, and first-CPU time `f`:
- **Utilization** = Σbusy / total_time.
- **Throughput** = completed_jobs / elapsed_time.
- **Turnaround** = `c − a`.
- **Waiting** = `c − a − b` (Σ time in ready queue).
- **Response** = `f − a`.
A scheduler is *good* if it minimizes the chosen latencies for its workload class; fairness (proportional to weight) is the modern distributional goal.

## 8. Example
Three jobs, all arrive at t=0, bursts: A=5, B=3, C=2. Under **FCFS (A,B,C)**:
- A: c=5, TAT=5, wait=0
- B: c=8, TAT=8, wait=5
- C: c=10, TAT=10, wait=8
- Avg TAT = (5+8+10)/3 = 7.67; avg wait = (0+5+8)/3 = 4.33.
Under **SJF (C,B,A)**:
- C: c=2 (TAT 2, wait 0); B: c=5 (TAT 5, wait 2); A: c=10 (TAT 10, wait 5)
- Avg TAT = (2+5+10)/3 = 5.67; avg wait = (0+2+5)/3 = 2.33.
Same jobs, same CPU — SJF's shorter average TAT is *exactly* why it's optimal for average waiting/turnaround (though it starves long jobs).

## 9. Internal Working
1. The scheduler computes per-task values from PCB fields: `vruntime` (Linux) accumulates CPU time; priority/weight derives from `nice` or cgroup share.
2. **EEVDF (Linux fair scheduler)**: each task has a virtual runtime; the scheduler picks the *lagging* task (largest "eligibility"), keeping weighted fairness. Metrics like TAT are derived from these virtual times, not tracked explicitly.
3. **Accounting**: `schedule()`/timer tick updates vruntime; `getrusage`/`/proc/<pid>/stat` expose utime/stime (for turnaround/wait analysis).
4. **cgroup bandwidth**: `cpu.max` throttles a group after its share quota — a fairness/throughput enforcement at the container level.
5. **Metrics in practice**: latency via `latencyTop`/perf sched; throughput via throughput tests; utilization via `mpstat`.

## 10. Time Complexity
- Computing metrics for n jobs (analysis): O(n log n) (sort bursts) to compute all TATs/wait.
- EEVDF pick-next: O(1) amortized (cached leftmost); O(log n) worst for rbtree updates.
- vruntime update per tick: O(1).
- cgroup bandwidth accounting: O(1) per task tick.

## 11. Advantages
- **Objective, measurable**: you can A/B schedulers by metrics.
- **Design language**: criteria map cleanly to algorithms (SJF→wait, RR→response, EDF→deadlines).
- **Workload-matched**: batch vs interactive vs RT each get the right objective.
- **Explainable**: "this scheduler optimizes X" is a precise statement.

## 12. Disadvantages
- **Metrics conflict**: optimizing one degrades others (throughput ↔ response).
- **Burst estimation is hard**: SJF etc. need burst lengths you don't know in advance.
- **Average-based metrics hide worst cases**: p99 latency can be terrible with good averages.
- **Fairness vs efficiency**: strict fairness can leave resources unused (prefer small jobs).

## 13. Interview Questions
1. **Q: What are the scheduling criteria?** A: CPU utilization, throughput, turnaround time, waiting time, response time (and fairness). Each is a measurable goal the scheduler optimizes for its workload class.
2. **Q: Define turnaround, waiting, and response time with formulas.** A: TAT = completion − arrival; Waiting = TAT − burst (ready-queue time); Response = first-CPU − arrival.
3. **Q (TRICKY): If a process never waits, are TAT and burst equal?** A: Yes — TAT = wait + burst; wait=0 → TAT = burst. That only happens when it's first in line with no preemption (FCFS first job).
4. **Q: Which criterion does a batch system optimize?** A: Throughput and CPU utilization (maximum work); interactivity is not a concern. HPC schedulers (Slurm) do exactly this.
5. **Q: Which criterion does a time-sharing OS prioritize?** A: Response time (interactivity) and fairness — hence preemptive quantum-based scheduling (RR-like) over pure throughput.
6. **Q: What's the trade-off between utilization and response time?** A: High utilization = long queues = high latency; low queues = idle CPU = low utilization. OSes accept some idle to bound response (e.g., idle-wakeup in EEVDF, load balancing).
7. **Q (SCENARIO): Design a scheduler for an interactive terminal with occasional heavy compiles.** A: Prioritize short tasks and I/O-bound tasks (high response); give compute jobs lower dynamic priority (aging to avoid starvation) — the classic MLFQ design. Metrics to watch: response + p99 TAT.
8. **Q: Why is average waiting time a better "goodness" metric than average TAT?** A: Waiting isolates the scheduler's contribution (ready-queue delay), removing the job's own burst from the score — comparing schedulers fairly.
9. **Q: What does "fairness" mean in scheduling, and how is it measured?** A: Each task gets CPU proportional to its weight (not necessarily equal). Measured by lag (deviation from ideal share); EEVDF bounds lag — the modern formalization.
10. **Q (PRODUCTION): Your container is latency-spiky. Which criterion is the kernel optimizing and what do you check?** A: CFS/EEVDF optimizes *fairness* (weighted vruntime), not your container's latency. Check cgroup `cpu.max`/shares, runqueue pressure (`runqlat`), and whether neighbors are hogging share.
11. **Q: What is the difference between response time and turnaround time?** A: Response = time until *first* CPU service (interactive feel); Turnaround = total time to *completion* (includes the whole execution).
12. **Q: Can one scheduler be optimal for all five criteria?** A: No — proven tensions: SJF/SRTF minimizes avg wait/TAT but poor worst-case response (starvation); RR bounds response but raises avg TAT. Optimality is per-criterion.
13. **Q: What is "dispatch latency"?** A: The time from the scheduler deciding to switch to the next task actually running (schedule → context switch → resume) — part of response time and a real-time concern.
14. **Q (TRICKY): If two processes have equal TAT but different waits, what do we infer?** A: Their bursts differ — wait = TAT − burst, so equal TAT with different waits means different CPU bursts (the longer-burst job waited less, relatively).
15. **Q: How does Linux account CPU time per process?** A: `task_struct`'s utime/stime (updated on ticks and exit) + `cputime` in cgroup; `vruntime` (weighted virtual time) drives fairness, not raw metrics.

## 14. Follow-Up Questions
1. **Q: What is p99 latency and why do averages mislead in scheduling?** A: p99 = the 99th-percentile latency; a few starved tasks wreck p99 even when averages look fine — why modern systems report tail latencies.
2. **Q: What is "CPU-bound vs I/O-bound" and how does it interact with criteria?** A: CPU-bound tasks use full slices (throughput); I/O-bound tasks need quick response (they block frequently) — priority schemas favor I/O-bound to keep devices busy.
3. **Q: How does nice/priority map to fairness?** A: `nice` adjusts weight (Linux: nice 0 = weight 1024; each ±1 ≈ ±1.25× share). EEVDF converts weight to virtual-time slope.
4. **Q: What is a "Gantt chart"?** A: A time-line diagram of which process runs when — the standard visual for scheduling problems and the format for computing metrics.
5. **Q: What is the relationship between utilization and response under Little's Law?** A: `L = λW` — average jobs in system = arrival rate × response time; as utilization → 1, queues (and response) blow up nonlinearly.

## 15. Coding Example
```c
/* Compute scheduling metrics given completion times (numpy-style in C) */
#include <stdio.h>
int main(void) {
    /* jobs: (burst, arrival) — schedule chosen by hand for the example */
    int burst[] = {5, 3, 2};
    int arrival[] = {0, 0, 0};
    int n = 3;
    /* FCFS order A,B,C */
    int completion[3], t = 0;
    for (int i = 0; i < n; i++) {
        t += burst[i];
        completion[i] = t;
        printf("job %c: completion %d, TAT %d, wait %d\n",
               'A'+i, completion[i],
               completion[i] - arrival[i],
               completion[i] - arrival[i] - burst[i]);
    }
    return 0;
}
```
```bash
# Measure a process's CPU usage (utime/stime) and scheduler behavior
sleep 1000 &
P=$(pgrep -n sleep)
grep -E "^utime|^stime" /proc/$P/stat
cat /proc/$P/sched   # vruntime, nr_switches, se.statistics
kill $P
```

## 16. Industry Usage
- **Linux EEVDF**: fairness metric = lag (weighted); used by every cloud workload; cgroup CPU shares implement per-tenant fairness.
- **Slurm/Grid**: HPC batch — optimizes utilization/throughput for large jobs.
- **Windows NT**: priority-based with quantum; foreground boost optimizes interactive response.
- **FreeRTOS/QNX**: hard real-time — deadline/priority metrics, not averages.
- **Kubernetes/cgroups**: CPU requests/limits encode fairness and bandwidth guarantees; SREs watch runqueue latency.
- **Interview angle**: "compute TAT/wait" and "pick the algorithm" questions are universal; knowing criteria first makes all algorithms easy to derive.

## 17. References
- Silberschatz, *OS Concepts*, Ch. 6.1-6.2 (CPU Scheduling: Basic Concepts, Criteria).
- Tanenbaum, *Modern OS*, Ch. 2.4.1 (Scheduling).
- Linux: `kernel/sched/fair.c` (EEVDF), `include/linux/sched.h` (vruntime), cgroup docs (cpu controller).
- man: `sched(7)`, `proc(5)` (stat).
- LWN: "The EEVDF scheduler" (2023).
- Kleinrock, *Queueing Systems* (Little's Law).

## 18. Cheat Sheet
- Criteria: utilization, throughput, turnaround, waiting, response, fairness.
- TAT = completion − arrival; Wait = TAT − burst; Response = first-CPU − arrival.
- Batch: throughput/utilization; interactive: response; RT: deadlines; cloud: fairness.
- Metrics conflict — no universal optimum.
- Dispatch latency = schedule→switch→resume.
- Fairness = proportional to weight (lag-bounded, EEVDF).
- nice ↔ weight (Linux weight 1024 @ nice 0).
- Little's Law: L = λW; utilization → 1 ⇒ queues blow up.
- Averages hide p99/tail latency.

## 19. Quiz
1. Turnaround time = a) wait + burst b) burst only c) arrival only d) completion − burst → **a** (completion − arrival = wait + burst)
2. Response time measures: a) completion b) first CPU service c) I/O d) total wait → **b**
3. Waiting time excludes: a) ready queue b) execution c) I/O d) memory → **b**
4. Batch systems optimize: a) response b) throughput/utilization c) deadlines d) fairness only → **b**
5. A conflict pair is: a) TAT/wait b) utilization/response c) response/TAT d) all are unrelated → **b**
6. Fairness in EEVDF is: a) equal CPU b) proportional to weight c) lottery d) random → **b**
7. Dispatch latency is part of: a) TAT only b) response time c) throughput d) utilization → **b**
8. Under SJF with bursts 5,3,2 arriving at 0, avg TAT is: a) 7.67 b) 5.67 c) 4.33 d) 10 → **b**
9. p99 latency matters because: a) averages lie b) throughput high c) utilization low d) dispatch free → **a**
10. Little's Law relates: a) queue to cores b) L=λW c) TAT to burst d) weight to nice → **b**

## 20. Flashcards
- **Q: 6 scheduling criteria?** → **A:** Utilization, throughput, TAT, waiting, response, fairness.
- **Q: TAT formula?** → **A:** completion − arrival.
- **Q: Waiting formula?** → **A:** TAT − burst.
- **Q: Response formula?** → **A:** first-CPU − arrival.
- **Q: What does batch optimize?** → **A:** Throughput/utilization.
- **Q: What does interactive optimize?** → **A:** Response time/fairness.
- **Q: EEVDF fairness?** → **A:** Weighted virtual time; bounded lag.
- **Q: Dispatch latency?** → **A:** Decision → context switch → resume.
- **Q: Little's Law?** → **A:** L = λW; high utilization ⇒ long queues.

## 21. Revision
Scheduling is judged by criteria: utilization, throughput, turnaround (completion−arrival), waiting (TAT−burst), response (first-CPU−arrival), and fairness. Batch optimizes throughput/utilization; interactive optimizes response/fairness; RT optimizes deadlines. Metrics conflict, so algorithms encode policy choices. Linux EEVDF enforces weighted fairness via vruntime/lag; dispatch latency matters for response. Compute TAT/wait from Gantt charts — the universal interview skill.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What are the scheduling criteria?" | 13 Q1 / 7 Formal Definition |
| "Define turnaround/waiting/response" | 13 Q2 / 8 Example |
| "Batch vs interactive criteria?" | 13 Q4-5 / 3 When Is It Used |
| "Utilization vs response trade-off?" | 13 Q6 / 4 Why Not |
| "Why is avg wait a good metric?" | 13 Q8 / 8 Example |
| "What is fairness in scheduling?" | 13 Q9 / 9 Internal Working |
| "Design a scheduler for interactive + compiles?" | 13 Q7 / 16 Industry Usage |
| "What is dispatch latency?" | 13 Q13 / 2 How It Works |
| "Container latency spikes?" | 13 Q10 / 16 Industry Usage |
| "p99 vs average?" | 14 Follow-Up Q1 / 12 Disadvantages |
