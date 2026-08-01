# Section 01: Linux CFS and EEVDF

> **TL;DR**: Linux replaced the O(n) priority-array scheduler with CFS (Completely Fair Scheduler) in 2.6.23, and EEVDF (Earliest Eligible Virtual Deadline First) in 6.6 — both keep tasks in a red-black tree keyed by *virtual runtime* (actual runtime weighted by `nice`), always picking the leftmost (least-run) task, so CPU is shared proportionally to weight rather than by arbitrary priority.

## 1. Why Does This Exist?
Before 2.6.23, Linux's O(1) scheduler used static priorities and interactivity heuristics that misbehaved: interactive tasks got starved by subtle bugs, and balancing across CPUs was ad hoc. CFS exists to answer "what is *fair*?" precisely: give each task CPU proportional to its weight (from `nice`), measured by actual runtime — no hard-coded interactivity guesswork. EEVDF (6.6) refines CFS to also guarantee *latency*: it adds an eligibility condition + virtual deadline so the scheduler meets a target latency while keeping fairness. Both exist to deliver low latency for interactive tasks and proportional share for everyone, in one simple tree structure.

## 2. How Does It Work?
- **CFS**: each task has `vruntime` = normalized actual CPU time (divided by weight factor). Tasks live in a red-black tree keyed on vruntime. Pick = leftmost (smallest vruntime = least-run). After running, vruntime increases; it re-inserts. Latency target `sched_latency` (default 6ms) splits time: `slice = sched_latency * weight/total_weight`. `sched_min_granularity` floors a slice (default 0.75ms) to limit switch frequency.
- **EEVDF**: like CFS but each task has a *virtual deadline* = vruntime + lag-corrected virtual slice. Only *eligible* tasks (with `lag` ≤ 0, i.e., already received ≤ fair share) are pickable; pick the eligible task with the earliest virtual deadline. This preserves both fairness (lag → 0 over time) and latency (deadlines).
- `nice` (-20..19) → weight via `sched_prio_to_weight[]`; weight ratio = CPU share ratio.
- Group scheduling: cgroups give fair share *across groups*, not just tasks (container isolation).

## 3. When Is It Used?
- Default for all normal (fair class) tasks on Linux — desktop, server, cloud, containers.
- When you need proportional-share fairness, low latency for interactive work, and tunability (`sysctl kernel.sched_latency`, `sched_min_granularity`, `nice`, cgroups CPU limits).
- Not for hard real-time (that's RT/deadline classes above it).

## 4. Why Wasn't Another Approach Chosen?
- **O(1) priority array (pre-2.6.23)**: static 140-level arrays with interactivity heuristics — complex, misbehaved, unfair. Rejected.
- **MLFQ**: qualitative priority tiers, hard to reason about proportional share; gaming-prone. CFS chose *quantitative* fair share instead.
- **Pure RR**: no priority/weight, poor latency for short tasks. Rejected.
- **EDF**: great for deadlines but requires known execution times; not general-purpose. EEVDF adapts deadline ideas *without* needing WCET — that's the key innovation.
CFS/EEVDF won because a single, simple, provably-fair structure (rbtree) with a latency knob gives both fairness and responsiveness.

## 5. Intuition
**A pie being shared fairly**: everyone has a "deficit counter" (lag). The hungriest (most-under-served, smallest vruntime) always eats next. EEVDF adds a *ticket*: you can only eat once your counter catches up (eligible), and among eligible, the earliest-expiring coupon (earliest virtual deadline) goes first — so no one waits too long. Weight (nice) just means bigger slices per turn.

## 6. Real-World Analogy
**A kitchen with a fair-serving rule**: each diner has a "consumed" tally. The chef always serves the diner who has consumed the least (leftmost vruntime) — a huge diner gets the next dish, then their tally rises, and someone else is served. EEVDF = the chef checks a *coupon* (eligibility: you must have waited your fair share) then serves the coupon expiring soonest (deadline) — guaranteeing every diner is served within a target window even while fairness holds.

## 7. Formal Definition
- **Weight**: w_i from nice via `sched_prio_to_weight` (nice -20 → 88761, 0 → 1024, +19 → 15).
- **vruntime**: vr = vruntime + (delta_exec * 1024 / w_i) — normalized to nice 0.
- **CFS slice**: slice_i = sched_latency * w_i / Σw (capped by sched_min_granularity).
- **EEVDF**: virtual deadline d_i = vruntime_i + slice_i; eligible when lag_i ≤ 0 (received ≤ fair share); pick min d_i among eligible. (Simplified; lag computed against a "fair clock" V(t).)
- **Pick**: O(log n) — rbtree leftmost; O(1) amortized with caching.

## 8. Example
Two tasks: A (nice 0, w=1024), B (nice -5 → w ≈ 3355; ~3.3× weight). Total weight ≈ 4379.
- Slice: sched_latency 6ms → A ≈ 1.4ms, B ≈ 4.6ms per round. B runs 3.3× more CPU — proportional share.
- vruntime after 6ms: A consumed 1.4ms → vr += 1.4ms; B consumed 4.6ms → vr += 4.6*1024/3355 ≈ 1.4ms. Equal vruntime → "fair" measured in normalized time. Tree always picks whichever has lower vr (here both equal → FCFS tie).

## 9. Internal Working
1. **Enqueue**: insert task into rbtree keyed by vruntime (`__enqueue_entity`).
2. **Pick-next**: leftmost node = least-run task (`__pick_first_entity`), O(1) via cached leftmost.
3. **Tick**: `scheduler_tick` → `task_tick_fair` → update vruntime of current; if it used its slice or EEVDF deadline passed and others eligible, `resched_curr()`.
4. **Preempt by wakeup**: `wakeup_preempt_eevdf` compares current vs new task's virtual deadline/eligibility.
5. **Placement on wake**: woken task is placed at its *last* vruntime (to preserve history) unless it slept long (> sched_idle-ish thresholds → given min vruntime so it runs soon → boost for interactive).
6. **Cgroups**: `sched_entity` tree per group; `cfs_rq` per CPU; pick lowest vruntime within the whole hierarchy.
7. **NO_HZ**: idle CPUs skip ticks (energy); wakeups still resched.

## 10. Time Complexity
- Enqueue/dequeue/pick: O(log n) worst; O(1) amortized for pick (cached leftmost).
- Tick: O(1) per task.
- Wakeup preemption check: O(1).
- Group hierarchy: O(log n + depth) — depth ≤ cgroup nesting.
- Compare old O(1) scheduler: O(1) enqueue with bitmaps but *unfair*; EEVDF trades strict O(1) for O(log n) fairness/latency — well worth it.

## 11. Advantages
- **Fair proportional share** with clear math (weights → shares).
- **Low latency**: leftmost is the least-run task → interactive tasks respond; EEVDF guarantees target latency via deadlines.
- **No burst prediction** — purely reactive to actual runtime.
- **Tunable**: `nice`, `sched_latency`, `sched_min_granularity`, cgroups.
- **Good worst case** O(log n); robust across thousands of threads.
- Simple, well-understood model (vs heuristics of O(1) scheduler).

## 12. Disadvantages
- O(log n) vs old O(1) enqueue (practically negligible).
- **Throughput at tiny latency**: small sched_latency → more context switches.
- **Wakeup placement heuristics** are still fiddly (interactive detection).
- Not for hard real-time — no worst-case execution-time guarantees.
- vruntime can overflow eventually (handled by lag normalization in EEVDF).
- Fair share doesn't equal isolation: a CPU hog still delays others unless cgroup-limited.

## 13. Interview Questions
1. **Q: What does CFS stand for and how does it pick tasks?** A: Completely Fair Scheduler — keeps tasks in an rbtree keyed on vruntime (normalized actual runtime); always runs the leftmost (least-run) task.
2. **Q: What is vruntime?** A: Each task's CPU time normalized by weight: vr += delta_exec × 1024 / weight. Fairness = equal vruntime across tasks, not equal wall-clock.
3. **Q (TRICKY): Two tasks, nice 0 and nice -5. Who runs more and why?** A: nice -5 has ~3.3× the weight, so it gets ~3.3× the CPU share — proportional share, not equal time.
4. **Q: How does `nice` affect CFS?** A: nice maps to weight; the slice each task gets is proportional to weight/total-weight — no hard priority ranking, only share ratios.
5. **Q: What changed in EEVDF (Linux 6.6)?** A: Adds eligibility (lag ≤ 0) + a virtual deadline per task; picks earliest-deadline among eligible — guarantees latency while preserving CFS fairness.
6. **Q: How does CFS handle an interactive task waking up?** A: It's placed by its historical vruntime (or given a minimum vruntime if slept long) so it lands near the left of the tree → runs quickly → low latency.
7. **Q: What is sched_latency / sched_min_granularity?** A: sched_latency = target round time (default ~6ms) that slices are carved from; sched_min_granularity = floor on a slice (default ~0.75ms) to avoid thrashing on tiny slices.
8. **Q: How do cgroups fit into CFS?** A: Each cgroup is a subtree in the sched_entity hierarchy; CFS guarantees fair share *across groups* first (container isolation), then within groups.
9. **Q (PRODUCTION): A container hogs CPU. How to cap it?** A: cgroup cpu.max (quota/period) or cpu.weight — CFS enforces proportional weight among groups, quota caps absolute usage.
10. **Q: Is CFS real-time?** A: No — it's soft real-time at best (no WCET guarantees). Hard priorities need SCHED_FIFO/RR (1-99) or SCHED_DEADLINE above the fair class.
11. **Q: What's the time complexity of picking next in CFS?** A: O(log n) for the rbtree; effectively O(1) amortized via cached leftmost node.
12. **Q (TRICKY): Can a task be CPU-starved under CFS?** A: No permanent starvation — its vruntime stays low so it climbs to the left and gets CPU. But it *can* be delayed by many other runnable tasks; cgroup limits and RT classes control that.

## 14. Follow-Up Questions
1. **Q: What's the difference between CFS and MLFQ?** A: MLFQ = discrete priority tiers (qualitative); CFS = continuous weighted share (quantitative). Both aim for "interactive fast, batch slow" but CFS is provable fair.
2. **Q: What is "lag"?** A: Difference between a task's actual runtime and its fair share over time (V(t) − vruntime). Eligibility in EEVDF requires lag ≤ 0.
3. **Q: How does CFS avoid vruntime overflow?** A: EEVDF normalizes lag and maintains bounded vruntime differences; also the tree only needs relative ordering.
4. **Q: What is wakeup preemption in EEVDF?** A: When a task wakes and is eligible with an earlier virtual deadline than the current task, it preempts — `wakeup_preempt_eevdf`.
5. **Q: Why was the O(1) scheduler replaced?** A: Unfair interactive heuristics and hard-to-tune behavior; CFS is simpler, fairer, and one data structure does everything.

## 15. Coding Example
```c
/* rbtree ordering is what CFS does internally; here's the pick logic */
#include <stdio.h>

typedef struct { int pid; double vruntime, weight; } sched_entity;

/* pick least-run task (leftmost in CFS's rbtree) */
sched_entity *pick_leftmost(sched_entity *t, int n) {
    int best = 0;
    for (int i = 1; i < n; i++)
        if (t[i].vruntime < t[best].vruntime) best = i;
    return &t[best];
}

int main(void) {
    /* nice 0 => weight 1024; nice -5 => weight ~3355 */
    sched_entity tasks[] = {
        {1, 0.0, 1024},
        {2, 0.0, 3355}
    };
    sched_entity *run = pick_leftmost(tasks, 2);
    /* normalize runtime by weight, like CFS's update_curr */
    double delta = 1.0; /* ms of real CPU */
    run->vruntime += delta * 1024.0 / run->weight;
    printf("picked pid %d; new vruntime %.3f (tie broken FCFS)\n",
           run->pid, run->vruntime);
    return 0;
}
```
```bash
# Observe CFS
cat /sys/kernel/debug/sched/debug | head -40   # rq/rbtree state
cat /proc/self/sched                             # per-task scheduling stats
sysctl kernel.sched_latency kernel.sched_min_granularity_ns
```

## 16. Industry Usage
- **Every Linux workload** — servers, containers (cgroup CPU), desktops, mobile (Android uses CFS).
- **Google/cloud**: CPU isolation via cgroups + CFS; autoscaling relies on fair share.
- **Android**: CFS with custom group weights for app/foreground priorities.
- **Kubernetes**: cpu limits/requests map to CFS quota/weight.
- **Preempt-RT**: CFS stays for fair tasks; RT classes for audio/industrial.
- Interview: "how does Linux schedule?" — CFS/EEVDF answer expected.

## 17. References
- Linux: `kernel/sched/fair.c`, `Documentation/scheduler/sched-design-CFS.rst`.
- EEVDF: "Earliest Eligible Virtual Deadline First" — Li & Yao (IEEE RTSS 2022); Linux 6.6 merge notes (LWN "Completely fair scheduling with EEVDF").
- CFS: Ingo Molnár, "CFS scheduler" (2.6.23) — LWN 2007.
- man: `sched(7)`, `nice(1)`, `chrt(1)`, `cgroups` docs.

## 18. Cheat Sheet
- CFS: rbtree by vruntime; run leftmost (least-run).
- vruntime = runtime × 1024/weight.
- nice → weight (1024 base; ±→×).
- Slice = sched_latency × weight/Σweight, floored by sched_min_granularity.
- EEVDF (6.6): eligibility (lag≤0) + virtual deadline; pick earliest deadline among eligible.
- Wakeup: place by history (or min vruntime if long-slept) → fast interactive.
- Cgroups: per-group fair share; quota caps.
- O(log n) pick; O(1) amortized.
- Not hard RT — use RT/DEADLINE classes.

## 19. Quiz
1. CFS data structure: a) array b) rbtree c) heap d) bitmap → **b**
2. CFS runs: a) highest priority b) leftmost c) shortest burst d) FCFS → **b**
3. vruntime normalizes: a) IO b) runtime by weight c) memory d) priority → **b**
4. nice -5 vs 0: a) less share b) ~3.3× share c) equal d) none → **b**
5. sched_latency default: a) 1s b) ~6ms c) 100ms d) 0 → **b**
6. EEVDF adds: a) RR b) eligibility+deadline c) priority d) quantum → **b**
7. CFS pick cost: a) O(1) always b) O(log n) c) O(n) d) O(n²) → **b**
8. CFS hard RT? a) yes b) no c) with RT class yes d) always → **b**
9. cgroups provide: a) priority b) group fair share c) quantum d) budget only → **b**
10. CFS replaced: a) MLFQ b) O(1) scheduler c) EDF d) FCFS → **b**

## 20. Flashcards
- **Q: CFS?** → **A:** Fair share via vruntime rbtree, run leftmost.
- **Q: vruntime?** → **A:** runtime × 1024/weight.
- **Q: nice?** → **A:** Weight ratio, not hard rank.
- **Q: EEVDF?** → **A:** Eligibility + virtual deadline, earliest first.
- **Q: Pick cost?** → **A:** O(log n), O(1) amortized.
- **Q: sched_latency?** → **A:** Target round time (~6ms).
- **Q: Interactive wakeup?** → **A:** Place by history → runs fast.
- **Q: Hard RT?** → **A:** No; use RT/DEADLINE classes.

## 21. Revision
CFS is Linux's fair scheduler: tasks in an rbtree keyed by vruntime (normalized actual time), always running the least-run (leftmost) task, with slices carved from sched_latency by weight (nice). EEVDF (6.6) adds per-task virtual deadlines plus an eligibility condition so latency is bounded while fairness holds. It's O(log n), tunable via sysctl/cgroups, but soft real-time only — RT (SCHED_FIFO/RR) and SCHED_DEADLINE sit above it for hard guarantees.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is CFS and how does it pick?" | 13 Q1 / 2 How It Works |
| "What is vruntime?" | 13 Q2 / 7 Formal Definition |
| "nice 0 vs -5?" | 13 Q3 / 8 Example |
| "How does nice affect CFS?" | 13 Q4 / 7 Formal Definition |
| "What changed in EEVDF?" | 13 Q5 / 2 How It Works |
| "Interactive wakeup handling?" | 13 Q6 / 9 Internal Working |
| "sched_latency/min_granularity?" | 13 Q7 / 7 Formal Definition |
| "Cgroups + CFS?" | 13 Q8 / 9 Internal Working |
| "Cap a CPU hog?" | 13 Q9 / 3 When Is It Used |
| "Is CFS real-time?" | 13 Q10 / 12 Disadvantages |
