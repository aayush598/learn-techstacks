# Section 01: Deadlocks in Databases

> **TL;DR**: Databases deadlock on row locks: two transactions each lock a row and then want the other's row. DBs handle it by building a wait-for graph on every lock wait, detecting the cycle, and rolling back a chosen victim transaction — the client simply retries.

## 1. Why Does This Exist?
Databases hold locks for the whole transaction (ACID isolation), so the classic lock-ordering deadlock appears naturally: T1 locks row A and wants B; T2 locks B and wants A. DBs can't easily enforce ordering (rows are dynamic), and they *can* roll back work — so the chosen strategy is detection + recovery. The whole machinery — wait-for graphs, victim selection, retries — exists so that concurrent transactions can run freely and a rare deadlock costs a single retry rather than a frozen database.

## 2. How Does It Work?
- **Locking**: `SELECT ... FOR UPDATE`, `INSERT`, `UPDATE` take exclusive row locks; reads under `REPEATABLE READ`/`SERIALIZABLE` may take shared locks.
- **Waits**: a transaction requesting a locked row blocks (wait-for edge).
- **Detection**: the DB (e.g., InnoDB) maintains a wait-for graph; on every lock wait it checks for a cycle. If found → choose a victim (the transaction with the least work / smallest undo).
- **Recovery**: roll back the victim's transaction (undo log), release its locks → the cycle breaks; the victim's client gets a deadlock error and retries.
- **Timeouts**: `innodb_lock_wait_timeout` (default 50s) aborts a transaction that waits too long — a coarse backstop.

## 3. When Is It Used?
- Every transaction that updates multiple rows in different orders (common in billing, inventories, order systems).
- Read-committed/repeatable-read isolation with row locking.
- MVCC databases: deadlocks still occur on *writes* (updates lock rows); MVCC helps readers, not writers.

## 4. Why Wasn't Another Approach Chosen?
- **Prevention by ordering**: rows aren't statically orderable; enforcing sort-by-key acquisition is possible but restrictive and rarely enforced by default. Rejected as primary.
- **Avoidance (Banker's)**: needs max claims (which rows will be touched) — unknowable in dynamic SQL. Rejected.
- **Global serialization**: one lock for all → no deadlock but no concurrency. Rejected.
- **Detection + rollback**: chosen because transactions are *naturally rollbackable* (undo logs) and deadlocks are rare — a retry costs little, concurrency is preserved.

## 5. Intuition
**Two customers at a bank transferring between accounts**: Customer A transfers from account 1 to 2; B transfers from 2 to 1. Each locks their "from" account first — A locks 1, B locks 2, then each needs the other's account. The teller (DB) spots the standoff (wait-for cycle), asks one customer to step aside and undo their work (rollback victim), so the other completes; the stepped-aside customer just retries.

## 6. Real-World Analogy
**A hotel booking system locking rooms**: two bookings each hold a room and need the other's adjacent room for a suite. The system watches who's waiting for whom (wait-for graph); when a loop forms, it cancels the cheaper booking (victim — smallest undo), frees its room, and the other completes. The canceled customer can rebook (retry). Locking one room at a time, in an unpredictable order, makes deadlocks inevitable — detection makes them survivable.

## 7. Formal Definition
- **Row lock**: exclusive/shared lock on a row, held to transaction end (2PL — two-phase locking).
- **Wait-for graph**: transactions as nodes; edge T1→T2 if T1 waits for a lock T2 holds.
- **Deadlock detection**: cycle in the wait-for graph. InnoDB checks on each wait (or periodically); a cycle ⇒ deadlock.
- **Victim selection**: rollback the transaction with the smallest undo size / least work (minimize redo cost); return error 1213/40001.
- **Timeout**: `innodb_lock_wait_timeout` aborts after T seconds — catches undetected stalls (e.g., distributed, or very rare cycles).
- **MVCC caveat**: reads via snapshots don't block (no shared-row locks under RC), so deadlocks are writer-vs-writer.

## 8. Example
```
T1: UPDATE accounts SET bal=bal-10 WHERE id=1;  -- locks row 1
T2: UPDATE accounts SET bal=bal-10 WHERE id=2;  -- locks row 2
T1: UPDATE accounts SET bal=bal+10 WHERE id=2;  -- waits on T2's row 2
T2: UPDATE accounts SET bal=bal+10 WHERE id=1;  -- waits on T1's row 1
=> cycle T1->T2->T1. InnoDB rolls back the victim (say T2).
T2's client: ERROR 1213 Deadlock found; retry.
```

## 9. Internal Working
1. Lock manager tracks lock ownership per row/table.
2. On a new lock request that conflicts: transaction blocks; wait-for graph gains an edge.
3. Detection triggers: InnoDB checks for cycles on every wait (depth-limited search). 
4. On cycle: pick the victim (smallest undo log / least recent), roll back via undo records (inverse operations), release locks, notify the client (SQLSTATE 40001).
5. Remaining transactions proceed; their locks are now satisfiable.
6. Timeouts catch stalls the graph search misses (e.g., lock-wait chains spanning many transactions, or disabled detection).

## 10. Time Complexity
- Per-wait cycle check: bounded DFS (InnoDB limits search depth) — effectively O(edges checked) per wait, amortized small.
- Rollback: O(victim's operations) via undo log.
- Timeout: O(1) check per wait.

## 11. Advantages
- **Concurrency preserved** — transactions run freely until a rare deadlock.
- **Recovery is cheap** — undo-log rollback + client retry.
- **Self-healing** — the DB resolves it automatically; no admin intervention.
- Client-facing: retry-on-40001 is a standard, well-understood pattern.

## 12. Disadvantages
- **Rollback cost**: victim's work is wasted (must be redone by the client).
- **Detection latency**: periodic/depth-limited checks may miss long chains briefly.
- **Retry storms**: under contention, repeated deadlock+retry thrashes.
- **Timeout aborts** can kill legitimately slow transactions (false positives).
- MVCC doesn't remove write-write deadlocks.

## 13. Interview Questions
1. **Q: How do databases deadlock?** A: Two transactions each lock a row and then want a row the other holds — the classic two-lock circular wait (T1 wants T2's row and vice versa).
2. **Q: How does a DB detect deadlock?** A: It builds a wait-for graph of transactions (who waits for whose lock) and searches for a cycle — InnoDB checks on every lock wait.
3. **Q: What happens on detection?** A: The DB selects a victim (smallest undo / least work), rolls it back via the undo log, releases its locks, and the client gets SQLSTATE 40001 to retry.
4. **Q: What is a wait-for graph in a DB?** A: Nodes = transactions; edge T1→T2 means T1 waits for a lock T2 holds. A cycle = deadlock.
5. **Q (TRICKY): Why doesn't MVCC eliminate deadlocks?** A: MVCC makes *reads* lock-free (snapshots), but *writers* still take exclusive row locks — so write-write conflicts deadlock exactly as before.
6. **Q: How is a victim chosen?** A: Minimize redo cost: smallest undo log, least work done, fewest rows. Rollback that transaction and let the rest proceed.
7. **Q: What's the role of `innodb_lock_wait_timeout`?** A: A backstop — a transaction waiting longer than T (default 50s) is aborted even if no cycle was found, catching stalls the graph search misses.
8. **Q (PRODUCTION): High deadlock rate — how do you fix it?** A: Reduce lock duration (shorter transactions), access rows in consistent order across transactions, use MVCC read snapshots instead of locking reads, index correctly, or increase granularity (partitioning).
9. **Q: Can a single statement deadlock?** A: Yes — an UPDATE affecting multiple rows locks them in a scan order that can conflict with another transaction's order (lock order differs between two scans).
10. **Q: What's the difference between DB deadlock handling and OS deadlock handling?** A: DBs use detection + rollback (transactions are rollbackable — cheap to abort). OSes mostly use prevention/ordering (kernel state isn't checkpointable) plus timeouts.
11. **Q: What is 2PL (two-phase locking)?** A: Transactions acquire all locks (growing phase) before releasing any (shrinking) — the source of hold-and-wait and, hence, of DB deadlocks under contention.
12. **Q (TRICKY): Deadlock error says "try restarting transaction." Why does the retry usually succeed?** A: After the victim rolls back, the lock it held is freed — the retry's contended rows are now available, so the second attempt usually completes (if the transaction ordering is stable).

## 14. Follow-Up Questions
1. **Q: What's the difference between InnoDB and MyISAM here?** A: MyISAM uses table-level locks (coarse → fewer deadlocks but no concurrency); InnoDB uses row locks (fine → deadlocks possible, high concurrency).
2. **Q: What is a "lock-wait chain"?** A: A long chain T1→T2→...→Tn of waits; detection depth-limited searches might miss very long chains — timeouts cover them.
3. **Q: How do isolation levels affect deadlocks?** A: `SERIALIZABLE` takes shared locks on reads (more blocking → more deadlock risk); `READ COMMITTED` reads don't lock (fewer conflicts).
4. **Q: What's "deadlock avoidance" in a DB?** A: Techniques like sorting lock acquisitions by key or acquiring in a global order (prevention-style) to reduce deadlock frequency.
5. **Q: How do you make a deadlock-safe transaction order?** A: Always access rows in a fixed order (e.g., sorted by primary key) across all transactions — eliminates the cycle.

## 15. Coding Example
```sql
-- The classic DB deadlock and the retry pattern
-- T1
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- locks row 1
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- waits on row 2 if T2 holds it
COMMIT;

-- T2 (concurrent)
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 2;  -- locks row 2
UPDATE accounts SET balance = balance + 100 WHERE id = 1;  -- waits on row 1 -> CYCLE
COMMIT;

-- Victim (say T2): ERROR 1213 (40001): Deadlock found; try restarting transaction
```
```java
// Standard retry-on-deadlock pattern
for (int attempt = 0; attempt < 3; attempt++) {
    try {
        doTransaction();  // commit or rollback internally
        break;
    } catch (DeadlockLoserDataAccessException e) {
        // victim: wait briefly and retry
        Thread.sleep(50 * (attempt + 1));
    }
}
```

## 16. Industry Usage
- **MySQL/InnoDB**: detects + rolls back victims; `SHOW ENGINE INNODB STATUS` exposes the wait-for graph.
- **PostgreSQL**: lock timeout + detection (aborts a deadlock victim automatically).
- **Oracle/SQL Server**: deadlock detection + victim selection, error codes for retry.
- **Microservices**: distributed transactions (Saga, 2PC) treat deadlocks as retryable.
- **Application pattern**: `retry on 40001` is a standard JDBC/Spring idiom.

## 17. References
- MySQL docs: InnoDB deadlock detection (`SHOW ENGINE INNODB STATUS`, `innodb_lock_wait_timeout`).
- PostgreSQL docs: deadlock detection, lock timeouts.
- Silberschatz, *OS Concepts*, 8.6 (deadlock detection) — DB application.
- Tanenbaum, *Modern OS* (deadlock chapter).
- 2PL: Bernstein et al., *Concurrency Control and Recovery in Database Systems*.

## 18. Cheat Sheet
- DB deadlock: two transactions lock rows in conflicting orders (2PL hold-and-wait).
- Detection: wait-for graph cycle (checked per lock wait in InnoDB).
- Victim: smallest undo → rollback → error 40001 → client retry.
- Timeout backstop: innodb_lock_wait_timeout (default 50s).
- MVCC helps reads only; writers still deadlock.
- Fix: shorter transactions, consistent row-access order, correct indexes.
- Single-statement UPDATEs can deadlock (scan lock order).
- MyISAM table locks (fewer deadlocks, less concurrency) vs InnoDB row locks.
- 2PL = acquire all before release — the root of DB hold-and-wait.
- Retry-on-40001 is the standard idiom.

## 19. Quiz
1. DB deadlock arises from: a) row locks in conflicting order b) memory c) I/O d) CPU → **a**
2. Detection uses: a) RAG only b) wait-for graph c) Banker's d) sort → **b**
3. On deadlock, DB: a) prevents b) rolls back victim c) ignores d) locks all → **b**
4. Victim chosen by: a) random b) smallest undo c) oldest d) newest → **b**
5. Client error for deadlock: a) 500 b) 40001 c) 404 d) 503 → **b**
6. MVCC helps: a) writers b) readers c) both d) none → **b**
7. innodb_lock_wait_timeout: a) detection b) backstop timeout c) prevention d) ordering → **b**
8. MyISAM uses: a) row locks b) table locks c) MVCC d) no locks → **b**
9. 2PL means: a) release early b) acquire all before release c) no locks d) read-only → **b**
10. Fix high deadlock rate: a) more locks b) consistent order c) bigger txns d) fewer rows → **b**

## 20. Flashcards
- **Q: DB deadlock?** → **A:** Row locks in conflicting order (2PL).
- **Q: Detection?** → **A:** Wait-for graph cycle per lock wait.
- **Q: Recovery?** → **A:** Roll back victim (smallest undo).
- **Q: Client error?** → **A:** 40001; retry.
- **Q: MVCC?** → **A:** Helps readers, not writers.
- **Q: Timeout?** → **A:** innodb_lock_wait_timeout backstop.
- **Q: Root cause?** → **A:** 2PL hold-and-wait.
- **Q: Fix?** → **A:** Consistent row-access order.

## 21. Revision
Databases deadlock when transactions lock rows in conflicting orders under 2PL. They handle it with detection + recovery: a wait-for graph is searched on each lock wait; on a cycle, the smallest-undo victim is rolled back and its client retries on error 40001; a timeout backstop covers undetected stalls. MVCC removes reader blocking but writers still deadlock. Prevention-style fixes (consistent row ordering, short transactions) reduce frequency. It's the textbook OS detection algorithm applied to real row locks.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "How do databases deadlock?" | 13 Q1 / 5 Intuition / 8 Example |
| "How detect?" | 13 Q2 / 2 How Does It Work |
| "What happens on detection?" | 13 Q3 / 9 Internal Working |
| "DB wait-for graph?" | 13 Q4 / 7 Formal Definition |
| "Why not MVCC fix writers?" | 13 Q5 / 7 Formal Definition |
| "Victim selection?" | 13 Q6 / 9 Internal Working |
| "innodb_lock_wait_timeout?" | 13 Q7 / 2 How Does It Work |
| "High deadlock rate fix?" | 13 Q8 / 12 Disadvantages |
| "Single statement deadlock?" | 13 Q9 / 8 Example |
| "DB vs OS handling?" | 13 Q10 / 4 Why Wasn't Another Approach Chosen |
