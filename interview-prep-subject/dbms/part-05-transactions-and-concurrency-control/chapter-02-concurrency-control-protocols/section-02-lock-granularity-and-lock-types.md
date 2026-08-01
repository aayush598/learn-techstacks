# Lock Granularity and Lock Types

> **TL;DR**: Lock granularity answers "how big is the thing I'm locking?" — from a single row up to a whole table — and multi-granularity locking with **intention locks** is how a DBMS lets fine- and coarse-grained locks coexist without deadlock or explosion.

## 1. Why Does This Exist?
2PL says "lock the data items you touch" but never says *what a data item is*. Lock everything (whole table): simple, no lock-table bloat, but abysmal concurrency — one `UPDATE` blocks the entire table. Lock nothing (each byte): great concurrency, but the lock table becomes huge (a lock per row is expensive) and range operations are impossible to lock atomically. Lock granularity exists because there's a spectrum between "too coarse" (table) and "too fine" (byte), and because different transactions need different granularities — a report scans a table, a hot row update touches one record. **Multi-granularity locking (MGL)** formalizes this with a lock hierarchy (table → page → row) plus intention locks so that a coarse lock (table) properly conflicts with fine locks (rows) held by others.

## 2. How Does It Work?
The hierarchy: a DB is a tree of granularities — database → table → page → row (→ field). A transaction locking at granularity G must first acquire *intention locks* on all ancestors. **Intention modes**: IS (intention shared — "I intend to take shared locks on descendants"), IX (intention exclusive), SIX (shared + intention exclusive — I hold S on this node and may take X on descendants). Compatibility is defined so that an exclusive lock at any ancestor conflicts with any *non-intention* or conflicting lock at descendants. **Lock escalation**: when a transaction holds many small locks (e.g., >5% of rows), the DBMS converts them into one table-level lock (with the same or stricter mode) to save memory — reducing concurrency but cutting bookkeeping. Lock types also vary by operation: **record lock**, **gap lock** (lock the space between index records), **next-key lock** (record + preceding gap — the MySQL phantom-prevention lock).

## 3. When Is It Used?
- When a transaction updates a *range* via a `WHERE` clause — the DBMS locks individual matching rows (or the whole table if the optimizer decides a scan is cheaper than many locks).
- `SELECT * FROM orders` for a nightly report → a table-level or large-range read; wants an IS/S lock on the table.
- `UPDATE orders SET status='x' WHERE status='pending'` scanning many rows → the engine may escalate row locks to a table X-lock.
- `INSERT` into a range being scanned by another transaction → needs gap/next-key locks (InnoDB) to prevent phantoms.
- Every production DBMS: Postgres locks tables (`LOCK TABLE`), rows, and index entries; InnoDB has record/gap/next-key; SQL Server escalates row→page→table.

## 4. Why Wasn't Another Approach Chosen?
- *Table-only locking*: simple, deadlock-free with care, but the concurrency of an entire e-commerce checkout becomes serialized on the orders table. Rejected for OLTP throughput.
- *Row-only locking*: maximum concurrency but (a) a lock entry per row is expensive (millions of rows = millions of lock structs), (b) you can't atomically lock a *range* you haven't enumerated yet (needed for phantoms), (c) a full-table scan acquires millions of locks. Rejected as the sole granularity.
- *No hierarchy (just "any lock anywhere")*: if T1 locks row 5 and T2 locks the table, the conflict isn't detectable without checking every row — O(n) conflict checks. Intention locks exist to make the conflict check O(1): T2 sees T1's IX-lock on the table and knows it conflicts.
- *Predicate locking (lock by WHERE predicate)*: the theoretically "correct" phantom prevention, but checking predicate overlap is expensive and rarely implemented (InnoDB's next-key locks are a pragmatic approximation).

## 5. Intuition
Think of a **building with floors, corridors, and rooms** (table → page → rows). Before you enter any room, you pin a sign on the building entrance: "I'm in room 7, intending to be inside." The sign (intention lock) tells other people *who might be inside* without them having to check every room. If someone wants to lock the *whole building* (table lock) they see your sign and wait until you're done. If someone else wants room 7 too, they check the room itself. The signs are cheap to check (one flag per floor) — that's why intention locks keep conflict detection O(1) instead of scanning every room.

## 6. Real-World Analogy
A **concert hall**: the "table lock" = booking the whole venue for the night (nobody else gets in). "Page lock" = booking one balcony. "Row lock" = booking individual seats. If you book individual seats, you must tell the box office *which section* (intention lock) so that someone booking the whole balcony knows you're in there. If the box office decides to convert your 50 seat-bookings into a whole-balcony booking (escalation), it's simpler for them but now the other 50 seats are blocked for everyone else — exactly the trade-off of lock escalation.

## 7. Formal Definition
**Multi-granularity locking**: a lock hierarchy is a rooted tree (DB → tables → pages → rows). A transaction that acquires a lock on node N in mode M must acquire a *compatible intention lock* on every ancestor of N. Intention modes: **IS** (intention shared — descendants will hold S locks), **IX** (intention exclusive — descendants will hold X locks), **SIX** (shared + intention exclusive — holds S here, will take X below). The lock-compatibility table (IS, IX, S, SIX, X):
- IS: compatible with IS, IX, S, SIX; conflicts with X.
- IX: compatible with IS, IX; conflicts with S, SIX, X.
- S: compatible with IS, S; conflicts with IX, SIX, X.
- SIX: compatible with IS; conflicts with IX, S, SIX, X.
- X: conflicts with everything.
**Lock escalation**: converting many low-granularity locks (rows) into one higher-granularity lock (page/table) with the same mode (S→S, X→X) when a threshold (e.g., percentage of rows or memory) is exceeded. **Lock types (InnoDB)**: **record lock** (on an index record), **gap lock** (on the gap *between* index records or before first/after last), **next-key lock** (record + gap, locking the range [prev, record]); in REPEATABLE READ InnoDB uses next-key locks to prevent phantoms; in READ COMMITTED only record locks (gaps disabled).

## 8. Example
Suppose table `orders` (1,000,000 rows), transaction T1 runs `UPDATE orders SET status='paid' WHERE order_id=123456`. Engine does an index lookup → acquires an X record lock on row 123456, plus IX lock on the table and IS/IX on the appropriate page and index. Concurrently T2 runs `LOCK TABLE orders IN SHARE MODE` (a report). T2 requests an S lock on the whole table: it checks compatibility — the table already has an IX lock from T1 → S conflicts with IX → T2 waits. Correct: a full-table read must not run while a row is being modified. When T1 commits, T2 proceeds. Without the IX marker, the engine couldn't know a row-level write is in progress without scanning all rows.

Phantom-prevention with next-key locks: `status='pending'` index has records at statuses (pending: rows 1,3,7; paid: row 5). T1 does `SELECT * FROM orders WHERE status='pending' FOR UPDATE` → next-key locks on index entries 1,3,7 and gaps (before 1, between 1-3, between 3-5, between 7-end). T2 tries `INSERT (status='pending', ...)` — the insert wants to place a record in a gap T1 has locked → **blocks** until T1 commits. That's how InnoDB REPEATABLE READ prevents phantoms.

## 9. Internal Working
1. A transaction's request `lock(mode, granularity)` walks from the root: acquire compatible intention locks on ancestors (if not held by this transaction in a stronger/equal mode), then acquire the requested lock at the target node.
2. The lock manager maintains per-node lock lists + wait queues; conflicts resolved via the compatibility matrix; deadlock detection runs on the wait-for graph (Chapter 05).
3. When a transaction holds S locks and requests X on the same node → **upgrade**; upgrade waits for other S-holders.
4. **Escalation trigger** (SQL Server / Postgres adaptive): when row-lock count crosses a threshold (e.g., 5,000 locks or 40% of table in SQL Server) or memory pressure hits, the manager asks to convert to table lock. Escalation can fail if a conflicting lock exists (then it retries later).
5. On commit/abort: release all locks, from leaves up (each release wakes waiters).

## 10. Time Complexity
- Lock acquisition with intention locks: O(depth of hierarchy) ≈ O(1) (3-4 levels) per request.
- Compatibility check: O(1) table lookup.
- Lock table memory: O(#locks held). Row-level locking of a big scan = O(#rows) lock entries — the cost that escalation tries to bound.
- Escalation decision: O(#locks held) to count, amortized O(1) per lock.

## 11. Advantages
- **Balances concurrency and overhead**: fine locks for hot rows, coarse for big scans.
- **O(1) conflict detection across granularities** via intention locks.
- **Phantom prevention** via gap/next-key locks (range stability for range queries).
- **Memory control** through lock escalation when the lock table grows too large.
- Matches real query shapes: single-row OLTP updates and full-table analytic scans both get reasonable locking.

## 12. Disadvantages
- **More complex**: the compatibility matrix and intention modes are hard to reason about — interviewers exploit this.
- **Escalation reduces concurrency** suddenly (a "report blocks everything" outage pattern).
- **Gap locks reduce insert concurrency** and can cause mysterious "deadlocks" between inserts into adjacent ranges.
- **Lock table memory**: fine-grained locking on huge scans is still memory-hungry; escalation is a blunt fix.
- **Deadlock surface grows** with more granularity (more lock combos can cycle).

## 13. Interview Questions
1. **Q: What is lock granularity?** A: The size of the data unit being locked: database, table, page, row (or field). Coarser = less concurrency but less overhead; finer = more concurrency but more bookkeeping.
2. **Q: What are intention locks and why do they exist?** A: IS/IX/SIX are ancestor locks signaling "I'll lock descendants." They exist so that a coarse lock (table) can detect a conflict with fine locks (rows) in O(1) — without them you'd scan every row to see if a table lock conflicts.
3. **Q: What is the compatibility rule for intention locks?** A: Intention locks are compatible with other intention locks (IS/IS, IX/IX, IS/IX all fine) but conflict with *actual* locks: S conflicts with IX, SIX, X; X conflicts with everything; SIX conflicts with IX, S, SIX, X. In short: "intention vs intention = fine; intention vs real = check."
4. **Q: What is lock escalation?** A: Converting many fine locks (rows) into one coarse lock (page/table) at the same mode to save lock-table memory when a threshold is crossed. Trade-off: reduces concurrency (the whole table is now locked) but prevents the lock manager from exhausting memory.
5. **Q: TRICKY: Why can escalation hurt you in production?** A: Because one big scan can escalate to a table X-lock, blocking *all* writes on the table — a classic "everything is slow after the ETL ran" outage. Tuning knobs (SQL Server `LOCK_ESCALATION=DISABLE/AUTO`, Postgres `max_locks_per_transaction`) exist to manage it.
6. **Q: What is a record lock vs gap lock vs next-key lock?** A: Record lock = a single index record. Gap lock = the space between index records (prevents inserts there). Next-key lock = record + the gap before it — it locks the *range*, preventing phantoms. InnoDB uses next-key locks at REPEATABLE READ and record locks at READ COMMITTED.
7. **Q: How does InnoDB prevent phantom reads?** A: With next-key locks during `SELECT ... FOR UPDATE`/`LOCK IN SHARE MODE` and DML: the range you scan is locked (records + gaps), so a concurrent `INSERT` into that range blocks until you commit. That's why InnoDB REPEATABLE READ is phantom-safe (stronger than the standard's minimal requirement).
8. **Q: What is the difference between IS and IX?** A: IS = "intention shared" (I'll read descendants, hold S locks); IX = "intention exclusive" (I'll write descendants, hold X locks). A table with IS can still allow table S-locks; a table with IX blocks table S/SIX/X locks.
9. **Q: What is an SIX lock and when would it be used?** A: SIX = shared + intention exclusive: hold S on this node AND intend X on descendants. Example: a transaction reads the whole table (S) but updates a subset (X) — holding S+SIX says "I'm reading everything and writing some of it." It blocks other writers (IX-compatible SIX? no — SIX conflicts with IX, S, SIX, X) while letting other readers through.
10. **Q: PRODUCTION: When would you `LOCK TABLE ... IN ACCESS EXCLUSIVE MODE` in Postgres?** A: For DDL that must not interleave (schema changes, `VACUUM FULL`, `CLUSTER`) or to force a full-table lock for a batch job. It's the coarse extreme — use sparingly.
11. **Q: TRICKY: Why doesn't pure row locking prevent phantoms?** A: Because a phantom is a row that *doesn't exist yet* — there's nothing to lock. To lock "the place where a new row might appear," you need to lock the *gap* (or the predicate). Row locks only cover existing rows.
12. **Q: What is a lock upgrade and why can it deadlock?** A: Upgrade = converting S(A) to X(A). If T1 and T2 both hold S(A) and both upgrade, each waits for the other to release S → deadlock. DBMSes handle it via detection or by forcing upgrades to wait for all S-holders to leave.
13. **Q: How does lock granularity relate to index locks?** A: Locks attach to *index records*, not table rows — so an update also locks the B-tree leaf entry (and gaps between entries). Deleting a row locks the index entry too; an index scan takes locks on leaf pages/records, enabling range locking.
14. **Q: What are the three standard multi-granularity lock modes' names?** A: Shared (S), exclusive (X), intention-shared (IS), intention-exclusive (IX), shared-intention-exclusive (SIX) — five modes; the three "intention" ones are IS, IX, SIX.

## 14. Follow-Up Questions
1. **Q: Why is predicate locking rarely implemented?** A: Two predicates ("status='pending'" and "id>100") can overlap in ways that are expensive to detect (range intersection); next-key/gap locking approximates it using the index order — cheaper and deadlock-tractable.
2. **Q: How does Postgres handle table vs row locking?** A: Postgres uses per-tuple locks in a shared-memory lock table, plus `LOCK TABLE` for explicit table locks (with levels ACCESS SHARE through ACCESS EXCLUSIVE — a 8-level hierarchy differing from the textbook 5-mode one).
3. **Q: What's the difference between Postgres's ACCESS EXCLUSIVE and ROW EXCLUSIVE?** A: ACCESS EXCLUSIVE conflicts with everything (even reads); ROW EXCLUSIVE conflicts with SHARE/EXCLUSIVE-family locks but allows ACCESS SHARE (readers). The lock-level table in Postgres docs maps each DDL/DML to its level.

## 15. Coding Example
```sql
-- InnoDB: see lock types in practice
START TRANSACTION;
SELECT * FROM orders WHERE status = 'pending' FOR UPDATE;   -- next-key locks on range

-- In another session, this INSERT blocks (gap lock on 'pending' range)
INSERT INTO orders (order_id, status) VALUES (999999, 'pending');

-- Inspect locks
SELECT * FROM performance_schema.data_locks\G   -- MySQL 8.0: LOCK_TYPE, LOCK_MODE, LOCK_DATA
```
```python
# Escalation simulation: fine-grained → coarse-grained
class LockTracker:
    def __init__(self, threshold=5_000):
        self.row_locks = {}      # row_id -> mode
        self.table_lock = None   # mode or None
        self.threshold = threshold
    def acquire_row(self, row_id, mode):
        if self.table_lock:
            return f"granted via table lock ({self.table_lock})"
        self.row_locks[row_id] = mode
        if len(self.row_locks) > self.threshold:
            self.table_lock = max(self.row_locks.values())  # escalate
            self.row_locks.clear()
            return f"ESCALATED to table {self.table_lock}"
        return f"row lock granted ({row_id}, {mode})"

t = LockTracker(threshold=3)
print(t.acquire_row(1, 'S')); print(t.acquire_row(2, 'S'))
print(t.acquire_row(3, 'X'))     # 3 > 3? no, == 3 not > 3... threshold met at 4
print(t.acquire_row(4, 'X'))     # ESCALATED to table X
```

## 16. Industry Usage
- **MySQL InnoDB**: record locks, gap locks, next-key locks; REPEATABLE READ uses next-key by default; `innodb_lock_wait_timeout` bounds waits. Documented in InnoDB Locking docs.
- **PostgreSQL**: multi-granularity table locks (`LOCK TABLE` modes: ACCESS SHARE … ACCESS EXCLUSIVE) + per-tuple locks; `max_locks_per_transaction` and `deadlock_timeout` (1s default).
- **SQL Server**: lock escalation row→page→table; hints `ROWLOCK, PAGLOCK, TABLOCK, UPDLOCK, HOLDLOCK, XLOCK`; `ALTER TABLE ... SET (LOCK_ESCALATION=...)`.
- **Oracle**: row + table (TM) locks; uses `SELECT ... FOR UPDATE` for app-level locks; Oracle historically used row-level locking with no gap locks (different phantom story).
- **CockroachDB**: per-row locks + "replicated" lock spans; uses the same theory but over a distributed key range.

## 17. References
- Gray, Lorie, Putzolu, Traiger, "Granularity of Locks and Degrees of Consistency in a Shared Data Base", IBM 1975 — the original multi-granularity paper.
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 16.3 (multiple granularity).
- Elmasri & Navathe, Ch. 21.
- MySQL 8.0 InnoDB Locking docs: https://dev.mysql.com/doc/refman/8.0/en/innodb-locking.html
- PostgreSQL docs, "Explicit Locking": https://www.postgresql.org/docs/current/explicit-locking.html
- SQL Server docs, "Lock Escalation": https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-guides/lock-escalation

## 18. Cheat Sheet
- Granularity ladder: database → table → page → row. Coarser = less concurrency, less memory.
- Intention locks (IS/IX/SIX) on ancestors make cross-granularity conflicts O(1).
- Compatibility: X conflicts with all; S conflicts with IX, SIX, X; SIX conflicts with S, SIX, IX, X; IX & IS conflict only with the "real" locks.
- Escalation: many row locks → one table lock (save memory, cut concurrency).
- Next-key lock = record + preceding gap → phantom prevention in InnoDB RR.
- Gap locks block inserts into the gap; only existing rows can have record locks.
- Lock upgrade S→X can self-deadlock between two upgraders.
- Lock waits: InnoDB `innodb_lock_wait_timeout`; Postgres `deadlock_timeout`.

## 19. Quiz
1. Which is the correct granularity order (coarse→fine)? a) row→page→table b) table→page→row c) page→table→row d) row→table→page → **b**
2. Why do intention locks exist? a) to lock more data b) to make cross-granularity conflict detection O(1) c) to escalate locks d) to detect deadlocks → **b**
3. IS is compatible with: a) X b) S c) SIX d) none → **b** (and IS/IX)
4. A table with an IX lock blocks a request for: a) IS b) IX c) S d) nothing → **c** (S conflicts with IX)
5. Phantom prevention needs: a) record locks b) gap/next-key locks c) escalation d) intention locks → **b**
6. Escalation converts row locks into a: a) byte lock b) table lock c) gap lock d) schema lock → **b**
7. InnoDB uses next-key locks at which isolation? a) READ COMMITTED b) REPEATABLE READ c) READ UNCOMMITTED d) only SERIALIZABLE → **b**
8. Which can self-deadlock between two transactions? a) read locks b) lock upgrade S→X c) gap locks d) intention locks → **b**

## 20. Flashcards
- **Q: Name the granularities from coarse to fine.** → **A:** Table → page → row (→ field).
- **Q: What are the three intention modes?** → **A:** IS, IX, SIX (signals about future descendant locks).
- **Q: Why intention locks?** → **A:** So a table lock can detect row-lock conflicts in O(1), not by scanning rows.
- **Q: What is lock escalation?** → **A:** Replacing many row locks with one table lock to save memory, at the cost of concurrency.
- **Q: Record vs gap vs next-key lock.** → **A:** One record; the space between records; record + preceding gap.
- **Q: Which lock type prevents phantoms in InnoDB?** → **A:** Next-key locks (at REPEATABLE READ).
- **Q: What's dangerous about lock upgrade?** → **A:** Two S-holders both upgrading → deadlock.
- **Q: Why can't row locks stop phantoms?** → **A:** A phantom row doesn't exist yet — nothing to lock; you must lock the gap.

## 21. Revision
Granularity is the size of the locked unit (table/page/row); MGL uses intention locks (IS/IX/SIX) on ancestors so a coarse lock can detect a fine-lock conflict in O(1). Compatibility: X beats all; S vs IX/SIX/X conflict; intentions conflict only with real locks. Escalation saves lock memory by going coarse (hurts concurrency). InnoDB's record/gap/next-key locks: next-key prevents phantoms at REPEATABLE READ; gap locks block range inserts. Interview: draw the compatibility matrix, explain intention locks' purpose, describe escalation's outage risk, and give the phantom-prevention example.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is lock granularity?" | 1, 7 |
| "What are intention locks and why?" | 2, 7, 13 |
| "Lock escalation: what and when?" | 2, 9, 13 |
| "Record vs gap vs next-key lock." | 7, 13 |
| "How does InnoDB prevent phantoms?" | 8, 13 |
| "Why can't row locks stop phantoms?" | 13, 14 |
| "Compatibility matrix / SIX?" | 7, 13 |
| "When to use LOCK TABLE?" | 13, 16 |
