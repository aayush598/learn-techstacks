# Section 03: Deadlock Detection and Recovery

> **TL;DR**: When prevention/avoidance are too costly, detect the deadlock at runtime and recover: build the wait-for graph and search for cycles (or use timeouts). Recovery aborts a victim process or preempts/rolls back a resource. This is what databases actually do — detect and abort a transaction.

## 1. Why Does This Exist?
Prevention restricts; avoidance needs max claims; sometimes you can't do either — resources are dynamic, claims unknown, and the system must just keep running. Detection + recovery exists as the pragmatic safety net: let the system proceed freely, and when a deadlock is *detected*, fix it (abort a victim, free resources, let others proceed). Databases run this every day (deadlock victim rollback); it's the answer for environments where the deadlock's cost (a retry) is less than prevention's restrictions.

## 2. How Does It Work?
- **Detection**:
  - Single-instance resources: maintain the wait-for graph; run cycle detection (DFS) periodically or on request.
  - Multi-instance: an algorithm similar to Banker's safety check that finds whether *any* process can finish with current Available + freed resources; if none can, deadlock.
- **Recovery**:
  - **Abort victim**: pick one deadlocked process (cheapest/youngest/least important) and abort it → its resources free → cycle breaks.
  - **Rollback**: abort-and-restart the victim (transactions) rather than full kill.
  - **Preemption**: forcibly take a resource from a holder (with rollback), give it to the victim, restore later.
  - **Timeout**: a process that waits too long is assumed deadlocked and aborts (cheap heuristic detection).

## 3. When Is It Used?
- **Databases**: `innodb_lock_wait_timeout`, deadlock detection on every lock wait — abort the victim transaction.
- **Distributed systems**: lock leases + timeout → evict a stalled holder.
- **General OSes**: rarely run full detection (overhead); rely on prevention + timeouts.
- **Embedded/telecom**: watchdog + restart on detected stalls.

## 4. Why Wasn't Another Approach Chosen?
- **Prevention**: too restrictive for dynamic workloads (ordering breaks, claims unknown). Rejected as the sole strategy.
- **Avoidance (Banker's)**: needs max claims, O(n²·m) per grant. Rejected for production.
- **Do nothing**: deadlock = frozen system. Rejected.
- **Detection + recovery**: chosen where deadlocks are *rare but possible* and a retry is cheap — the database model. The cost: aborting a victim loses its work (acceptable for transactions).

## 5. Intuition
**A construction site gridlock on a narrow road**: instead of redesigning traffic (prevention) or pre-checking every truck's route (avoidance), you watch for the jam (detection) and — when it forms — tow away one truck (abort victim) so the rest can move. It's reactive: you accept that jams happen, but you guarantee they don't last forever.

## 6. Real-World Analogy
**A reservation system with a timeout**: if a customer's booking session stalls (holds a table) and another customer can't proceed, the system detects the stall (wait-for cycle or timeout) and releases the first session (abort + rollback), letting the second one complete. The first customer just retries — a small cost compared to a permanently frozen lobby.

## 7. Formal Definition
- **Detection (single-instance)**: build wait-for graph; if a cycle exists → deadlock. Periodically (or on each wait) run DFS.
- **Detection (multi-instance)**: algorithm resembling Banker's safety: Work = Available; repeatedly find unfinished P with Request_i ≤ Work; Work += Allocation_i; if any remain unfinished → deadlock exists (all remaining are deadlocked).
- **Recovery options**:
  - **Process termination**: abort all deadlocked processes (harsh) or one at a time until the cycle clears (cheaper).
  - **Resource preemption**: select a victim, preempt its resource (rollback to a safe checkpoint), restart it; the victim may be re-selected (starvation — prefer avoiding re-victimization).
- **Timeout heuristic**: a request waiting longer than T is treated as deadlocked → abort. Not exact, but cheap and simple.

## 8. Example
Wait-for graph cycle: T0→T1 (T0 waits on T1's resource), T1→T2, T2→T0. Cycle = deadlock (single-instance). Recovery: choose victim T1 (cheapest), abort it → releases its resources → T2 proceeds → T0 proceeds.
DB equivalent: `ERROR 1213 (40001): Deadlock found when trying to get lock; try restarting transaction` — the victim transaction is rolled back.

## 9. Internal Working
1. On each resource request, add a request edge; on grant, move to assignment; on release, remove.
2. Detection trigger: periodic (every k seconds — but deadlocks persist between runs) or on-demand (every request — high overhead).
3. Cycle search: DFS with a recursion stack (O(V+E)); a back edge = cycle.
4. Multi-instance detection reuses the safety simulation; leftover unfinished processes = deadlocked.
5. Victim selection: cost-based (least CPU used, youngest, fewest locks, most retryable) — minimize redo cost.
6. Preemption/rollback: save checkpoint state; on preempt, restore; re-victimization risk → starvation (track victim count, prefer others).

## 10. Time Complexity
- Cycle detection (single-instance): O(V+E) per run.
- Multi-instance detection: O(n²·m) (like Banker's safety).
- Detection frequency tradeoff: every request → high overhead; periodic → deadlock lingers between runs.
- Timeout: O(1) per waiter (heuristic).

## 11. Advantages
- **No prior knowledge needed** — no max claims, no ordering rules.
- Works with dynamic resource types.
- Cheap when deadlocks are rare (detection overhead amortized).
- Rollback/abort is well-understood (transactions).
- The database industry standard.

## 12. Disadvantages
- **Abort cost**: victim's work is lost (may need redo).
- **Detection overhead**: periodic scans can't catch deadlocks instantly; per-request scans are expensive.
- **Timeout is imprecise**: false positives (aborts a merely-slow process) and misses.
- Victim selection/starvation: the same process can be repeatedly chosen.
- Not suitable where work can't be rolled back (kernel locks).

## 13. Interview Questions
1. **Q: How do you detect a deadlock?** A: Build the wait-for graph and search for a cycle (DFS); with multi-instance resources, run the safety-like simulation to find processes that can't finish.
2. **Q: When do you run detection?** A: Periodically (deadlock persists until detected) or on each request (high overhead but immediate). Timeouts are a cheap heuristic.
3. **Q: What's the detection complexity?** A: O(V+E) for single-instance cycle search; O(n²·m) for the multi-instance simulation.
4. **Q (TRICKY): Why not detect on every request in production?** A: The O(V+E)/O(n²·m) scan on every lock acquire is too expensive; periodic scans or timeouts trade immediacy for cost.
5. **Q: What recovery options exist?** A: Abort all deadlocked processes, abort one victim at a time until the cycle breaks, or preempt/rollback a resource from a holder.
6. **Q: How do you choose a victim?** A: Cost-based — least CPU, youngest, fewest locks, most easily retried. Goal: minimize lost work.
7. **Q: What is rollback?** A: Return the victim to a safe checkpoint and restart, rather than killing it outright — requires checkpointed/saveable state (transactions).
8. **Q: What does MySQL do on a deadlock?** A: Detects the cycle (InnoDB builds a wait-for graph on each lock wait), selects a victim transaction, rolls it back, and returns an error the client can retry.
9. **Q (PRODUCTION): A process keeps getting chosen as the deadlock victim. Problem?** A: Victim starvation — recovery is re-selecting the same process. Fix: track victim counts and prefer others (or prioritize by cost/age).
10. **Q: What's a timeout-based detector?** A: A request waiting longer than T is assumed deadlocked and aborts — simple, but can false-positive on slow-but-progressing processes.
11. **Q: Why is detection+recovery bad for kernel locks?** A: Kernel critical sections aren't checkpointable; aborting a kernel thread mid-lock corrupts state. Kernels use prevention/ordering instead.
12. **Q (TRICKY): Periodic detection every 30s — what's the worst-case deadlock duration?** A: Up to 30s + recovery time — the deadlock persists until the next scan. This latency is why on-request detection exists in DBs.

## 14. Follow-Up Questions
1. **Q: What's the difference between aborting all vs one?** A: Aborting all is simpler but destroys all progress; aborting one at a time is cheaper (re-check the graph after each) but slower.
2. **Q: How do you implement a wait-for graph efficiently?** A: Maintain per-thread held/requested resources; on request, add an edge; DFS with a recursion stack finds cycles on demand.
3. **Q: What's the relationship to Banker's safety check?** A: The multi-instance detector *is* the safety algorithm run on the current state — if some processes can't finish, they're deadlocked.
4. **Q: What is a "checkpoint"?** A: A saved, consistent state that a preempted/aborted process can restart from — the basis of rollback.
5. **Q: How do distributed systems detect deadlocks?** A: Distributed wait-for graphs (message-passing cycle detection) or leases/timeouts — simpler and more common (evict stale holders).

## 15. Coding Example
```c
/* Wait-for graph cycle detection via DFS (single-instance) */
#include <stdio.h>
#include <stdbool.h>

#define N 4
/* wait[i][j] = 1 means thread i waits for a resource held by thread j */
int wait[N][N] = {
    {0,1,0,0},
    {0,0,1,0},
    {0,0,0,1},
    {1,0,0,0},   /* 3 waits for 0: cycle 0->1->2->3->0 */
};
bool visited[N], on_stack[N];

bool dfs(int v) {
    if (on_stack[v]) return true;              /* back edge = cycle */
    if (visited[v]) return false;
    visited[v] = on_stack[v] = true;
    for (int j = 0; j < N; j++)
        if (wait[v][j] && dfs(j)) return true;
    on_stack[v] = false;
    return false;
}

bool deadlock_detected(void) {
    for (int i = 0; i < N; i++)
        if (dfs(i)) return true;
    return false;
}

int main(void) {
    printf("deadlock: %s\n", deadlock_detected() ? "yes" : "no");
    return 0;
}
```
```sql
-- MySQL: InnoDB reports and rolls back a victim on deadlock
SHOW ENGINE INNODB STATUS;   -- shows the wait-for graph (LATEST DETECTED DEADLOCK)
```

## 16. Industry Usage
- **Databases**: MySQL (InnoDB), Postgres (timeout + on-wait detection), Oracle — the flagship users; clients retry on deadlock error.
- **Distributed systems**: etcd/ZooKeeper leases + timeouts; kubernetes controller retries.
- **Telecom/embedded**: watchdog timers restart stalled subsystems.
- **Windows/Linux**: mostly avoid via ordering + timeouts (e.g., mutex timeouts); full detection too costly.

## 17. References
- Silberschatz, *OS Concepts*, 8.6-8.7 (Detection, Recovery).
- Holt (1972) — wait-for graph detection.
- MySQL docs: deadlock detection in InnoDB (`innodb_lock_wait_timeout`, `SHOW ENGINE INNODB STATUS`).
- Postgres docs: lock timeout/deadlock detection.

## 18. Cheat Sheet
- Detect: wait-for graph cycle (single-instance) O(V+E); safety simulation (multi-instance) O(n²·m).
- Triggers: periodic (latency) vs per-request (overhead) vs timeout (heuristic).
- Recover: abort all, abort one victim, preempt+rollback.
- Victim choice: cost-based (least work lost).
- Rollback = checkpoint + restart (transactions).
- Starvation risk: re-selecting the same victim.
- MySQL: detects + rolls back victim; client retries.
- Bad for kernel locks (no checkpoint); use prevention there.
- Timeouts: simple but false-positive prone.

## 19. Quiz
1. Single-instance detection: a) matrices b) wait-for cycle c) timeouts only d) none → **b**
2. Multi-instance detection complexity: a) O(V+E) b) O(n²·m) c) O(n) d) O(1) → **b**
3. Cycle search uses: a) BFS only b) DFS with stack c) sorting d) hashing → **b**
4. Recovery options: a) abort only b) abort/preempt c) nothing d) share → **b**
5. Victim choice is: a) random b) cost-based c) order d) always first → **b**
6. Rollback needs: a) max claims b) checkpoint c) ordering d) timeout → **b**
7. MySQL deadlock handling: a) prevention b) detect+rollback victim c) ignore d) Banker's → **b**
8. Kernel locks use: a) detection b) prevention/ordering c) abort d) timeouts → **b**
9. Timeout detection: a) exact b) heuristic c) optimal d) free → **b**
10. Periodic detection latency: a) zero b) up to period c) infinite d) one tick → **b**

## 20. Flashcards
- **Q: Detect?** → **A:** Wait-for cycle (single); safety sim (multi).
- **Q: Complexity?** → **A:** O(V+E) / O(n²·m).
- **Q: Recovery?** → **A:** Abort victim / preempt+rollback.
- **Q: Victim?** → **A:** Cost-based.
- **Q: Rollback?** → **A:** Checkpoint + restart.
- **Q: MySQL?** → **A:** Detect + rollback victim.
- **Q: Kernel?** → **A:** Prevention, not detection.
- **Q: Timeout?** → **A:** Cheap heuristic, false positives.

## 21. Revision
When prevention/avoidance are impractical, detect and recover: find cycles in the wait-for graph (single-instance, O(V+E)) or run the safety simulation (multi-instance, O(n²·m)), then abort a cost-chosen victim or preempt with rollback to a checkpoint. Databases do exactly this — MySQL detects cycles and rolls back the victim transaction; clients retry. Timeouts are the cheap heuristic. It's reactive and loses victim work, which is why kernels (non-checkpointable) prefer prevention/ordering instead.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "How do you detect a deadlock?" | 13 Q1 / 2 How Does It Work |
| "When to run detection?" | 13 Q2 / 9 Internal Working |
| "Detection complexity?" | 13 Q3 / 10 Time Complexity |
| "Why not per-request in production?" | 13 Q4 / 10 Time Complexity |
| "Recovery options?" | 13 Q5 / 7 Formal Definition |
| "How choose a victim?" | 13 Q6 / 9 Internal Working |
| "What is rollback?" | 13 Q7 / 7 Formal Definition |
| "MySQL deadlock behavior?" | 13 Q8 / 16 Industry Usage |
| "Same process repeatedly victim?" | 13 Q9 / 12 Disadvantages |
| "Why bad for kernel locks?" | 13 Q11 / 12 Disadvantages |
