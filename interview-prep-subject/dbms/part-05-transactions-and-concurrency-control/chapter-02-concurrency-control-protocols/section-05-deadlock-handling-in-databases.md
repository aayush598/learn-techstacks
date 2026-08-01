# Deadlock Handling in Databases

> **TL;DR**: Deadlock is the circular-wait failure mode of locking protocols — nobody gets their lock, everybody waits — and databases handle it with timeouts or wait-for-graph detection plus victim selection, because 2PL can't prevent it and true prevention is too costly.

## 1. Why Does This Exist?
2PL guarantees serializability but *allows* deadlock: T1 holds lock on A and waits for B, while T2 holds B and waits for A. If nothing intervenes, both wait forever — the system hangs. Deadlock handling exists because (a) deadlocks are an *inevitable* consequence of lock-based concurrency (any protocol that lets a transaction hold a lock while requesting another can deadlock), and (b) the cost of *preventing* them up front (pre-declaring all locks, or globally ordering all lock acquisitions) is usually higher than the cost of *detecting and recovering* from the rare ones. Real DBMSes therefore accept deadlock as a fact of life and provide mechanisms to break the cycle.

## 2. How Does It Work?
Three strategies:
- **Deadlock prevention**: ensure circular wait can't form — e.g., **wait-die** (older waits, younger dies) and **wound-wait** (older wounds, i.e., aborts the younger) based on timestamps; or **lock ordering** (every transaction acquires locks in a fixed global order so cycles can't form); or acquire all locks up front.
- **Deadlock avoidance**: use the *knowledge* of what each transaction *will* need (before it requests) to never grant a request that creates a cycle (banker's algorithm) — rare in DBMSes because future needs are unknown.
- **Deadlock detection**: build a **wait-for graph** (nodes = transactions; edge T→U if T waits for a lock held by U) and periodically check for a cycle; when a cycle is found, **roll back a victim** (the transaction with the least cost — fewest locks, oldest, or one the app marked abortable), possibly after the cycle is broken, and let the others proceed. **Timeouts** (`innodb_lock_wait_timeout`, `lock_timeout`) are a cheap pragmatic proxy: a waiter that exceeds the timeout is aborted.
- **Livelock** (starvation): a transaction is never blocked but never granted (constantly overtaken). Prevented by FIFO lock queues / fairness.

## 3. When Is It Used?
- Every lock-based DBMS: MySQL InnoDB (timeout + `innodb_deadlock_detect` — detects immediately, aborts the smallest rollback-size transaction), Postgres (`deadlock_timeout` default 1s, then detects and aborts a victim), SQL Server (`DEADLOCK_PRIORITY`), Oracle (detection).
- App-level optimistic locking (version columns) *avoids* DB deadlocks by construction (no lock waiting).
- Distributed systems: deadlock detection is harder (no single wait-for graph) — distributed lock managers use timeouts and wound-wait.
- In interviews: "what is a deadlock?", "deadlock vs livelock", "wait-die vs wound-wait", "how does InnoDB detect deadlocks?", "how would you design a deadlock-free counter?"

## 4. Why Wasn't Another Approach Chosen?
- *Pure prevention (lock ordering)*: works only if all code acquires locks in the same global order — hard to guarantee across thousands of queries and schema; some queries can't know their full lock set in advance. DBMSes *recommend* it but don't enforce it.
- *Wait-die/wound-wait*: prevent deadlock but cause *unnecessary* aborts (a young transaction dies even when no deadlock would occur) and re-introduce timestamp pitfalls. Their use is justified only where detection is too expensive (distributed).
- *Banker's-algorithm avoidance*: requires perfect knowledge of future requests — impractical for SQL — so it's a textbook concept, not a DBMS feature.
- *Timeout-only*: simplest, but (a) a false timeout aborts a transaction that would have succeeded seconds later, wasting work; (b) a truly deadlocked pair must wait out the full timeout — sluggish. Modern engines combine: detect (instant, precise) + timeout (backstop).
- *Ignore deadlocks*: a hung database. Not an option. Even "no-lock" systems (MVCC readers, OCC) hit deadlock equivalents (write-write conflicts, lock upgrade conflicts) needing handling.

## 5. Intuition
A **four-way intersection with no traffic lights**: each car (transaction) has stopped in the middle and is waiting for another car to move first. No one will move because everyone waits for someone else — deadlock. Detection = a traffic officer (the DBMS) notices the gridlock and *tows one car* (aborts a victim) so the rest can flow; the towed driver returns later (retry). Prevention = rule "whoever arrived earlier always goes first" (wait-die/wound-wait) — but that sometimes sends cars back to the start even when there was no gridlock. And a *timeout* = "if you've been waiting more than 5 minutes, assume gridlock and turn back" — safe but occasionally turns back a car that would've moved in 6 minutes.

## 6. Real-World Analogy
**Two developers refactoring the same codebase**: Dev1 checked out (locked) `payment.go` and needs `auth.go`; Dev2 checked out `auth.go` and needs `payment.go`. Each is waiting for the other to finish — deadlock. The team's fix: a "repo lock" (global order — all devs take locks alphabetically), or a watcher that notices both are stuck and force-reverts the dev with the smaller diff (victim). Without any mechanism, both sit forever. This is exactly why teams add "always acquire locks in the same order" rules to their tooling.

## 7. Formal Definition
**Deadlock**: a state where a set of transactions {T₁,...,Tₙ} each holds a lock that another member needs and each is waiting for a lock held by another member — a cycle in the **wait-for graph** (W∅FG): an edge Tᵢ→Tⱼ exists iff Tᵢ is waiting for a lock currently held by Tⱼ. A cycle in the WFG ⇒ deadlock.
- **Wait-die (non-preemptive)**: if Tᵢ (older) requests a lock held by Tⱼ (younger), Tᵢ *waits*; if Tᵢ is younger, it *dies* (aborts). Only older transactions wait — deadlock-free.
- **Wound-wait (preemptive)**: if Tᵢ (older) requests a lock held by Tⱼ, Tᵢ *wounds* Tⱼ (aborts the younger holder); if Tᵢ is younger, it waits. Also deadlock-free.
- **Timeouts**: a waiter aborts after waiting longer than a threshold — heuristic, not guaranteed to break all deadlocks.
- **Livelock**: a transaction is not blocked by any single lock but never makes progress because it keeps losing the race (e.g., always restarted). Not a deadlock — a starvation condition.

## 8. Example
Transactions T1 and T2, items A and B.
- T1: `LOCK A; ... LOCK B; ...` 
- T2: `LOCK B; ... LOCK A; ...`
Sequence: T1 acquires X(A). T2 acquires X(B). T1 requests X(B) → blocked (held by T2). T2 requests X(A) → blocked (held by T1). **Wait-for graph: T1→T2 (T1 waits on B held by T2), T2→T1 (T2 waits on A held by T1)** — cycle → deadlock.
InnoDB behavior: `innodb_deadlock_detect=ON` → as soon as the second block happens, InnoDB scans for the cycle, picks the victim (the transaction with the smaller amount of rollback work, i.e., fewer records modified), aborts it with `ERROR 1213 (40001): Deadlock found ...`, and T2 (the survivor) proceeds. The app must retry T1.
Under wait-die: T1(older) requests B held by T2(younger) → T1 waits (older waits). Then T2 requests A held by T1 → T2 is younger → T2 *dies*. No cycle ever forms. One transaction aborted proactively.
Under wound-wait: T2 holds B, T1(older) requests → T1 wounds T2 → T2 aborts. If instead T1 were younger, T1 waits.

## 9. Internal Working
1. **Detection trigger**: InnoDB detects at lock-wait time (each time a transaction blocks, a graph scan checks cycles — O(transactions waiting)). Postgres waits `deadlock_timeout` (1s), then runs the cycle check; it does this lazily because the graph scan is periodic/on-demand.
2. **Wait-for graph construction**: maintained in the lock manager — on a block, add edge requester→holder; on grant/abort, remove edges.
3. **Cycle detection**: DFS/BFS over the WFG; if a cycle is found, pick a victim — heuristics: fewest undo/redo records (InnoDB), transaction with least total lock count / longest in system / most recently started.
4. **Victim rollback**: abort the victim (rollback its changes via undo log — possibly *partial* rollback only to the point needed to break the cycle in advanced systems; InnoDB rolls back the whole transaction), release its locks, wake its waiters, notify the app (error code 40001/1213).
5. **Retry**: the application must retry the aborted transaction — engines don't auto-retry (they'd need to know the app's side effects).
6. **Timeouts as backstop**: even if detection misses (or is disabled), `innodb_lock_wait_timeout` (50s default) / `lock_timeout` aborts long waiters, bounding worst-case stall.

## 10. Time Complexity
- Detection via WFG scan: O(V + E) per check (V = waiting transactions, E = edges); InnoDB amortizes by scanning at block-time; Postgres pays it after the timeout.
- Wait-die/wound-wait: O(1) per request — cheaper than detection but causes more aborts.
- Victim selection: O(transactions) to score.
- Abort cost: O(work done by victim) — the real price of deadlock.
- Timeout approach: no graph work, but worst-case detection latency = timeout value.

## 11. Advantages
- **Availability**: deadlocks are broken, not hung — the DB keeps working.
- **Precise (detection)**: aborts *only* when a real cycle exists; no wasted work like proactive prevention.
- **Simple to reason about**: the WFG is a clean model; cycle = deadlock.
- **Retry-friendly**: aborts are reported clearly (standard SQLSTATE 40001), so apps can retry safely.
- **Tunable**: detection on/off (InnoDB), timeouts, priorities (SQL Server) let ops balance precision and cost.

## 12. Disadvantages
- **Abort cost**: the victim's entire transaction work is wasted — under high contention, deadlock-retry storms can cascade throughput collapse.
- **Timeouts can be wrong**: false-positive aborts (transaction would have proceeded) waste work; false-negatives (waiting out the full timeout) stall.
- **Detection overhead**: graph scans under load add CPU; Postgres's 1s delay means deadlocked transactions *sit* for a second before detection.
- **Distributed deadlock detection is hard**: no global WFG; detectors must cooperate or use timeouts/wound-wait — often leading to spurious aborts.
- **Starvation/livelock** if victim selection is unfair (one transaction repeatedly chosen as victim).

## 13. Interview Questions
1. **Q: What is a deadlock?** A: A set of transactions where each holds a lock the other needs and each waits for the other — a cycle in the wait-for graph. No transaction can proceed, so the system would hang without intervention.
2. **Q: What are the four Coffman conditions and how do they map to DBMS?** A: Mutual exclusion (locks are exclusive), hold-and-wait (a transaction holds locks while requesting more), no preemption (locks can't be yanked away), circular wait (the wait-for cycle). DBMSes attack circular wait (detection/prevention) and hold-and-wait (pre-acquire all).
3. **Q: Deadlock vs livelock?** A: Deadlock = permanent block (a cycle — nobody moves). Livelock = never blocked but never makes progress (constantly restarted or overtaken) — a starvation condition. Both are "no progress"; deadlock is a waiting cycle, livelock is a losing race.
4. **Q: What are the approaches to handling deadlock?** A: Prevention (make circular wait impossible: wait-die, wound-wait, global lock ordering, acquire-all-up-front), avoidance (banker's algorithm — requires knowing future requests), detection + recovery (WFG cycle check, abort a victim), and timeouts (abort waiters exceeding a threshold). DBMSes use detection + timeouts; distributed systems often use prevention.
5. **Q: Explain wait-die and wound-wait.** A: Both use timestamps. Wait-die (non-preemptive): an *older* transaction waits for a younger; a *younger* dies when it would wait on an older. Wound-wait (preemptive): an *older* transaction *wounds* (aborts) a younger holder; a *younger* just waits. Both guarantee no deadlock; wound-wait aborts fewer transactions (the younger holder is already "committed" to less work usually).
6. **Q: TRICKY: Why does a deadlock victim get SQLSTATE 40001 / MySQL error 1213?** A: It's the standard "serialization failure" — the app must retry the whole transaction. Using a consistent error code makes retry logic portable and unambiguous (the transaction was aborted, not failed semantically).
7. **Q: How does InnoDB detect deadlocks?** A: With `innodb_deadlock_detect=ON` (default), the moment a transaction blocks waiting for a lock, InnoDB scans the wait-for graph for cycles and immediately aborts the victim (the transaction with the least rollback work). The error returns instantly — no timeout wait.
8. **Q: How does Postgres detect deadlocks?** A: It waits `deadlock_timeout` (default 1s) after a lock wait begins, then runs the cycle detection on the wait-for graph; if a cycle is found, one transaction is aborted with `ERROR: deadlock detected`. The delay means Postgres trades a small stall for cheaper detection.
9. **Q: What makes a good deadlock victim?** A: A victim whose abort is cheapest and least disruptive: fewest modified rows (InnoDB uses rollback work), lowest priority (SQL Server `DEADLOCK_PRIORITY`), least total lock count, or oldest — plus "don't victimize the same transaction twice" to avoid starvation.
10. **Q: PRODUCTION: What are the best practices to avoid deadlocks in application SQL?** A: (1) Access tables/rows in a consistent global order across all transactions; (2) keep transactions short (fewer locks held); (3) use indexes so UPDATE/DELETE lock few rows deterministically; (4) avoid user interaction inside a transaction; (5) prefer idempotent retry logic on 40001; (6) for read-modify-write races use `SELECT FOR UPDATE` *consistently*.
11. **Q: TRICKY: Can MVCC databases still deadlock?** A: Yes — writers deadlock on write-write conflicts and lock upgrades, even though readers never lock. Also FK checks, gap locks (InnoDB), and index inserts create lock waits. MVCC removes *reader* deadlocks, not *writer* deadlocks.
12. **Q: What is a lock upgrade deadlock?** A: T1 and T2 both hold S-lock on row X; both request X (upgrade). Each waits for the other to release S — a deadlock that pure record ordering wouldn't cause. DBMSes detect it; apps can avoid by using X-locks (FOR UPDATE) from the start.
13. **Q: When would you *disable* deadlock detection?** A: InnoDB: on tiny or highly-cyclic workloads where the graph scan costs more than timeouts (`innodb_deadlock_detect=OFF` with a low `innodb_lock_wait_timeout`). Generally not recommended — it trades precision for CPU.
14. **Q: PRODUCTION: A deadlock storm after deploying a new query — what do you check?** A: The new query's lock acquisition order vs existing ones (gap locks on overlapping ranges, FK locks), table/index scan vs seek (scan locks many rows), and whether transactions are longer than before. Fix: add indexes, standardize access order, shorten transactions, split the work.

## 14. Follow-Up Questions
1. **Q: Why is deadlock avoidance (banker's algorithm) not used in real DBMSes?** A: It requires knowing each transaction's *future* lock requests in advance. SQL transactions don't declare them; the engine can't predict which rows a WHERE clause will touch before execution. So avoidance stays theoretical.
2. **Q: How do distributed databases handle deadlock?** A: With per-node detectors that exchange info, or timeouts/wound-wait (CockroachDB aborts on lock timeout; Spanner uses wait queues + lock tables with a timeout). A global WFG is too expensive to maintain.
3. **Q: What is the relationship between lock ordering and deadlock?** A: If *every* transaction acquires locks in a fixed global order (e.g., always table A then B), a cycle is impossible — a cheap, *practical* prevention that apps can adopt even though engines don't enforce it.

## 15. Coding Example
```sql
-- Postgres: set a lock timeout to convert deadlock-prone waits into errors
SET lock_timeout = '5s';
BEGIN;
SELECT ... FROM accounts WHERE id=1 FOR UPDATE;
-- ... work ...
COMMIT;

-- MySQL: check the timeout & detection settings
SHOW VARIABLES LIKE 'innodb_lock_wait_timeout';   -- 50 (seconds)
SHOW VARIABLES LIKE 'innodb_deadlock_detect';     -- ON
```
```python
# Retry loop — the production pattern for handling deadlocks (SQLSTATE 40001)
import psycopg, time

def retry_deadlocks(fn, max_attempts=5):
    for attempt in range(max_attempts):
        try:
            with psycopg.connect("dbname=bank") as conn:
                with conn.transaction():
                    return fn(conn)                     # success
        except psycopg.errors.SerializationFailure as e:
            if attempt == max_attempts - 1:
                raise
            time.sleep(min(0.1 * 2 ** attempt, 2))      # exponential backoff
```
```pseudocode
// Wait-die rule (deadlock prevention)
function request_lock(T, L):
    if holder(H) exists:
        if TS(T) < TS(H):        # T older → T waits
            queue(T)
        else:                    # T younger → T dies (aborts & restarts)
            abort(T)
    else:
        grant(T, L)
```

## 16. Industry Usage
- **MySQL InnoDB**: `innodb_deadlock_detect`, `innodb_lock_wait_timeout`; auto-victim selection by rollback size; errors 1213/1205. `SHOW ENGINE INNODB STATUS` prints the last detected deadlock with the WFG.
- **PostgreSQL**: `deadlock_timeout` (1s) then graph detection; `lock_timeout`; aborted txn returns `40001`. `pg_stat_activity.wait_event_type='Lock'` shows live lock waits.
- **SQL Server**: `DEADLOCK_PRIORITY` (LOW/MEDIUM/HIGH + numeric) picks victims; deadlock graphs in Extended Events/error log.
- **Oracle**: detects via distributed/global wait-for info; `SELECT ... FOR UPDATE` apps see `ORA-00060` deadlock.
- **Distributed**: CockroachDB (lock wait + timeout → aborts, "transaction retry" errors), Spanner (wait-queue timeouts), FoundationDB (conflict-based, no blocking → no classic deadlock but optimistic abort).

## 17. References
- Coffman, Elphick, Shoshani, "System Deadlocks" (1971) — the four conditions.
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 16.7 (deadlock handling).
- Elmasri & Navathe, Ch. 21.
- MySQL 8.0 InnoDB deadlock docs: https://dev.mysql.com/doc/refman/8.0/en/innodb-deadlock-detection.html
- PostgreSQL docs, "Locking": https://www.postgresql.org/docs/current/locking-indexes.html and `deadlock_timeout` at https://www.postgresql.org/docs/current/runtime-config-locks.html
- Bernstein, Hadzilacos, Goodman, *Concurrency Control and Recovery in Database Systems* (1987) — wait-die/wound-wait origins.

## 18. Cheat Sheet
- Deadlock = cycle in the wait-for graph (hold-and-wait + circular wait).
- 4 conditions: mutual exclusion, hold-and-wait, no preemption, circular wait.
- Detection: WFG cycle check → abort victim → app retries (SQLSTATE 40001).
- Prevention: wait-die (older waits), wound-wait (older wounds younger), global lock order.
- Avoidance (banker's): impractical (needs future lock knowledge).
- Timeout: simple backstop; `innodb_lock_wait_timeout` 50s, `lock_timeout` in PG.
- MVCC kills *reader* deadlocks, not writer/gap/upgrade deadlocks.
- Lock upgrade S→X is a classic self-deadlock trap.
- Best practice: consistent access order, short transactions, indexes, retry on 40001.

## 19. Quiz
1. A deadlock is a: a) cycle in the wait-for graph b) timeout c) livelock d) dirty read → **a**
2. Wait-die: an older transaction that wants a younger's lock will: a) die b) wait c) wound d) commit → **b**
3. Wound-wait: an older transaction that wants a younger's lock will: a) die b) wait c) wound the younger d) restart → **c**
4. Which is NOT a deadlock handling approach? a) detection b) prevention c) avoidance d) serializability → **d**
5. MVCC eliminates deadlocks for: a) writers b) readers c) both d) neither → **b**
6. A lock upgrade (S→X) can cause: a) phantoms b) deadlock c) dirty reads d) none → **b**
7. InnoDB picks a deadlock victim by: a) age b) rollback work size c) priority d) random → **b**
8. Postgres detects deadlocks after: a) instant b) deadlock_timeout (1s) c) never d) 50s → **b**

## 20. Flashcards
- **Q: What is a deadlock?** → **A:** A cycle of transactions each waiting for a lock the other holds — permanent no-progress.
- **Q: Coffman conditions?** → **A:** Mutual exclusion, hold-and-wait, no preemption, circular wait.
- **Q: Wait-die vs wound-wait?** → **A:** Wait-die: older waits, younger dies. Wound-wait: older wounds (aborts) younger, younger waits.
- **Q: How does InnoDB detect deadlock?** → **A:** Wait-for graph scan at block time; aborts the smallest-rollback transaction (error 1213).
- **Q: How does Postgres detect?** → **A:** After deadlock_timeout (1s), runs the cycle check, aborts a victim (error 40001).
- **Q: Deadlock vs livelock?** → **A:** Deadlock = cycle of waits; livelock = never blocked but never progresses (starvation).
- **Q: Best practical deadlock avoidance?** → **A:** Consistent global lock-acquisition order + short transactions + retries on 40001.
- **Q: Can MVCC still deadlock?** → **A:** Yes — writers, gap locks, and lock upgrades can still deadlock.

## 21. Revision
Deadlock = circular wait (WFG cycle); caused by hold-and-wait + non-preemptive locks. Handling: detection (WFG cycle → abort cheapest victim → app retries 40001), prevention (wait-die/wound-wait by timestamp, global lock order), timeouts (backstop). Avoidance is impractical (unknown future locks). MVCC removes reader deadlocks only. InnoDB: instant detection, victim = smallest rollback; Postgres: 1s timeout then detect. Interview gold: state the 4 Coffman conditions, contrast wait-die/wound-wait, explain why 2PL doesn't prevent deadlock, and give the "consistent ordering + short transactions + retry" production recipe.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a deadlock and its conditions?" | 1, 7, 13 |
| "Deadlock vs livelock?" | 13, 18 |
| "Wait-die vs wound-wait?" | 2, 7, 13 |
| "How do InnoDB/Postgres detect deadlock?" | 9, 13, 16 |
| "How do you avoid deadlocks in SQL?" | 13, 15, 16 |
| "Why can't 2PL prevent deadlock?" | 4, 13 |
| "What is a lock upgrade deadlock?" | 13, 14 |
| "When disable deadlock detection?" | 13, 16 |
