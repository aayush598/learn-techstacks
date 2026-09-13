# Locking and Concurrency Control — 100 SQL Interview Q&A

## Q1: What is a database lock?
A lock is a concurrency-control primitive that lets a transaction acquire exclusive or shared access to a resource (row, page, table, index range) so that conflicting operations serialize instead of corrupting data.

**Query:**
```sql
-- PostgreSQL: lock a row so the later UPDATE has no race
BEGIN;
SELECT * FROM accounts WHERE id = 7 FOR UPDATE;
-- ... compute new balance ...
COMMIT;
```
**Explanation:** The lock is held until end of transaction; any concurrent incompatible lock on row 7 waits.

## Q2: Shared lock vs exclusive lock?
Shared (S) locks are compatible with each other (many readers), while exclusive (X) locks are compatible with nothing. Writers need X locks; plain readers take S locks (or no lock under MVCC).

**Query:**
```sql
-- MySQL: take an explicit shared lock
BEGIN;
SELECT balance FROM accounts WHERE id = 1 LOCK IN SHARE MODE;  -- S lock
COMMIT;
```
**Explanation:** A second `LOCK IN SHARE MODE` succeeds in parallel, but an `UPDATE ... WHERE id = 1` (X lock) must wait.

**Alt1:**
```sql
-- PostgreSQL: equivalent shared-lock read
SELECT * FROM accounts WHERE id = 1 FOR SHARE;
```
**Explanation:** Same S-lock semantics; combine with `NOWAIT` if you want an immediate error instead of a wait.

## Q3: What is lock granularity?
Granularity is the size of the resource a lock covers: row, page, table, schema, or index range. Finer granularity (row) maximizes concurrency but costs more memory and metadata; coarser granularity is cheaper but blocks more.

**Query:**
```sql
-- SQL Server: force row granularity for one statement
SELECT * FROM inventory WITH (ROWLOCK) WHERE sku = 'A1';
```
**Explanation:** ROWLOCK is a hint that tells the engine to use row locks for this operation instead of escalating to page/table locks.

## Q4: What is a happy-path lock for a SELECT that will be followed by an UPDATE?
Use a locking read: `SELECT ... FOR UPDATE` takes exclusive row locks held until commit, so no other transaction can change those rows in the meantime.

**Query:**
```sql
-- PostgreSQL / MySQL / Oracle
BEGIN;
SELECT balance, version FROM accounts WHERE id = 10 FOR UPDATE;
UPDATE accounts SET balance = balance - 100 WHERE id = 10;
COMMIT;
```
**Explanation:** Concurrent writers on row 10 block behind the FOR UPDATE until the transaction commits or rolls back.

## Q5: What does SELECT ... FOR SHARE do in PostgreSQL?
It takes a shared lock on the selected rows: other transactions can still lock them FOR SHARE or read them, but cannot `UPDATE`, `DELETE`, or `FOR UPDATE` them until the lock is released.

**Query:**
```sql
-- PostgreSQL
BEGIN;
SELECT id FROM promo_codes WHERE code = 'SAVE10' FOR SHARE;
COMMIT;
```
**Explanation:** FOR SHARE is a cheap "prevent mutation" read; it differs from FOR UPDATE in that other SHARE readers do not wait.

## Q6: Why doesn't a plain SELECT block on a FOR UPDATE locked row?
Because MVCC reads do not need locks: a normal SELECT reads a consistent snapshot of committed data and never contends with writers.

**Query:**
```sql
-- PostgreSQL: tx A has the row locked FOR UPDATE; this read still returns instantly
SELECT balance FROM accounts WHERE id = 5;
```
**Explanation:** Plain reads are lock-free under MVCC; only locking reads (`FOR UPDATE`/`FOR SHARE`/`LOCK IN SHARE MODE`) or writes actually block.

## Q7: When is a row lock released?
Row locks are held until the transaction ends (COMMIT or ROLLBACK). In autocommit mode each statement is its own transaction, so its locks release at the end of the statement.

**Query:**
```sql
-- MySQL: locks persist until COMMIT, not until the UPDATE finishes
SET autocommit = 0;
UPDATE accounts SET balance = balance - 5 WHERE id = 3;  -- lock held
COMMIT;                                                  -- lock released
```
**Explanation:** This is why long transactions hold locks long: the lock duration is "until transaction end", not "until statement end".

## Q8: What are the core lock modes in SQL Server?
Shared (S), Exclusive (X), Update (U), Intent (IS/IX/SIU/SIX), Schema (Sch-S/Sch-M), and Bulk Update locks.

**Query:**
```sql
-- SQL Server: U lock avoids the classic read-then-upgrade deadlock
BEGIN TRAN;
SELECT * FROM stock WITH (UPDLOCK) WHERE sku = 'A1';
UPDATE stock SET qty = qty - 1 WHERE sku = 'A1';
COMMIT;
```
**Explanation:** U locks are compatible with S but not other U/X; they prevent two readers from deadlocking when both try to upgrade S→X at once.

## Q9: Which row locking modes does MySQL InnoDB have?
InnoDB implements S (shared) and X (exclusive) record locks, plus gap locks and next-key locks for range protection.

**Query:**
```sql
-- MySQL: S and X expressed through statements, not lock names
SELECT * FROM t WHERE id = 1 LOCK IN SHARE MODE;         -- S record lock
SELECT * FROM t WHERE id = 1 FOR UPDATE;                -- X record lock
```
**Explanation:** `LOCK IN SHARE MODE` = shared; `FOR UPDATE` = exclusive. Both are locking reads held until transaction end.

## Q10: What is MVCC?
Multiversion concurrency control keeps multiple physical versions of a row so readers see a consistent snapshot without blocking writers and vice versa.

**Query:**
```sql
-- PostgreSQL: reader and writer do not block each other
-- tx A: UPDATE accounts SET balance = 999 WHERE id = 1;        (uncommitted)
-- tx B: SELECT balance FROM accounts WHERE id = 1;  -- old committed version
SELECT balance FROM accounts WHERE id = 1;
```
**Explanation:** B reads the pre-change version from the snapshot; no lock conflict occurs, which is why concurrent reads scale well.

## Q11: MVCC versus pessimistic locking: how do they coexist?
MVCC liberates plain reads, but writes are still protected by row locks; pessimistic locking deliberately takes locks up front (FOR UPDATE) to serialize critical sections.

**Query:**
```sql
-- MySQL: snapshot read (no locks) vs locking read used inside an update
SELECT * FROM accounts WHERE id = 1;              -- MVCC snapshot read
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;   -- pessimistic lock
```
**Explanation:** Use MVCC reads for reporting; switch to FOR UPDATE only where a value is read then re-written based on it.

## Q12: What lock does an UPDATE statement take?
An UPDATE takes exclusive (X) locks on every row it modifies, plus shared/relevant gap or next-key locks on the scanned range in REPEATABLE READ, and holds them to end of transaction.

**Query:**
```sql
-- SQL Server: default locking of an UPDATE
UPDATE accounts SET balance = balance + 10 WHERE id = 5;
```
**Explanation:** The engine first reads (often under a U lock) then converts to X for each row written; all rows matching the predicate get X locks.

## Q13: What locks does a DELETE statement take?
DELETE takes exclusive locks on each row it removes, and under REPEATABLE READ/SERIALIZABLE also takes gap locks so concurrent inserts cannot create phantoms in the deleted range.

**Query:**
```sql
-- MySQL: delete acquires X record locks on matched rows
DELETE FROM orders WHERE status = 'cancelled' AND created_at < '2024-01-01';
```
**Explanation:** Each matched row is X-locked until COMMIT; other transactions that try to touch those rows block.

## Q14: What locks does an INSERT take?
An INSERT takes an exclusive lock on the new row plus an insert-intention gap lock on the index gap into which the row is placed.

**Query:**
```sql
-- MySQL: inserting into a gap blocked by another transaction's gap lock is an insert-intention lock
INSERT INTO orders (id, customer_id) VALUES (500, 900);
```
**Explanation:** Insert-intention locks signal "I want to insert here" and coordinate with gap locks so two inserts into the same gap do not double-violate uniqueness.

## Q15: Read COMMITTED vs REPEATABLE READ: difference in locking?
Read Committed releases locks after each statement and allows phantom rows; Repeatable Read (MySQL default) holds locks to transaction end and uses next-key locks to prevent phantoms.

**Query:**
```sql
-- PostgreSQL: RC releases locks per-statement; set it per transaction
BEGIN ISOLATION LEVEL READ COMMITTED;
UPDATE accounts SET balance = balance - 1 WHERE id = 2;
COMMIT;
```
**Explanation:** Under RC, the row holds an X lock only until the statement completes (still until commit in postgres for the row) — snapshot reads never block; RR additionally locks ranges (MySQL).

**Alt1:**
```sql
-- MySQL: RR is default; gap+next-key locks are applied automatically
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT * FROM orders WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31' FOR UPDATE;
```
**Explanation:** In MySQL RR, the range is guarded by next-key locks that also stop inserts of matching rows.

## Q16: What is a dirty read and which isolation level permits it?
A dirty read is reading data a transaction has written but not yet committed; only READ UNCOMMITTED allows it (and MVCC engines usually still avoid it via snapshots).

**Query:**
```sql
-- SQL Server: explicitly allow uncommitted reads (dirty reads)
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SELECT balance FROM accounts WHERE id = 1;
```
**Explanation:** No shared locks are taken, so data can be read mid-mutation; usable for rough reporting, dangerous for money.

## Q17: What is the lost update problem?
When two readers read the same value and each writes back a value derived from the stale read, the last writer wins and the first writer's update is lost.

**Query:**
```sql
-- PostgreSQL / MySQL: both tx read 100, both set balance = 100 - 20 = 80
-- expected 60, got 80  ← lost update
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- 100
UPDATE accounts SET balance = 80 WHERE id = 1;
COMMIT;
```
**Explanation:** Neither read sees the other's change; the final value reflects only one of the two updates. Prevention requires locking or optimistic versioning.

## Q18: Prevent a lost update with SELECT ... FOR UPDATE?
Lock the row before deriving the new value so the second transaction must wait and re-read the updated value.

**Query:**
```sql
-- PostgreSQL: serialized read-modify-write
BEGIN;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;   -- tx B waits here
UPDATE accounts SET balance = balance - 20 WHERE id = 1; -- read-modify-write atomic
COMMIT;                                                  -- tx B now proceeds with 80
```
**Explanation:** Tx B blocks at the FOR UPDATE and, after A commits, still sees the latest value, so no update is lost. This is pessimistic locking.

## Q19: Prevent a lost update with an optimistic version column?
Read the row without locking, carry a version, and make the UPDATE conditional on the version still matching; check rowcount to retry if it changed.

**Query:**
```sql
-- PostgreSQL: optimistic concurrency
BEGIN;
SELECT id, balance, version FROM accounts WHERE id = 1;   -- version = 5
UPDATE accounts
   SET balance = balance - 20, version = version + 1
 WHERE id = 1 AND version = 5;                            -- fails if version moved
-- if 0 rows updated → someone else won, retry the whole read-modify-write
COMMIT;
```
**Explanation:** No locks are held during the read; contention produces a failed UPDATE (0 rows) instead of a wait, so the client retries. Works well for low-contention data.

## Q20: How do you atomically increment a counter without a lost update?
Do the increment inside the UPDATE itself (`counter = counter + 1`) so the database applies it under an exclusive lock, never read-then-write in client code.

**Query:**
```sql
-- PostgreSQL / MySQL / SQL Server
UPDATE visit_stats SET count = count + 1 WHERE page_id = 42;
```
**Explanation:** The expression `count + 1` is evaluated under the row's X lock, so concurrent increments serialize cleanly and no increment is lost.

**Alt1:**
```sql
-- PostgreSQL: atomic read of the resulting value in the same statement
UPDATE visit_stats SET count = count + 1
 WHERE page_id = 42
RETURNING count;
```
**Explanation:** RETURNING returns the new value under the same lock, avoiding a second racy read.

## Q21: Why is `UPDATE counter = counter + 1` race-free but `SELECT; UPDATE;` is not?
Because the UPDATE form locks the row, evaluates the expression, and writes back in one atomic step inside the engine, whereas a separate SELECT loses the lock between the two statements.

**Query:**
```sql
-- Race-prone pattern (PostgreSQL)
BEGIN;
SELECT count FROM stats WHERE id = 1;         -- stale value
UPDATE stats SET count = 77 WHERE id = 1;     -- may overwrite a newer value
COMMIT;
```
**Explanation:** Between the SELECT and UPDATE another transaction may commit; the single-statement `count = count + 1` eliminates that hole.

## Q22: Row locks vs page locks vs table locks: when does each apply?
The engine picks granularity from lock count and contention; SQL Server may start on rows then escalate to pages then to the table when a statement touches many rows.

**Query:**
```sql
-- SQL Server: see locking behavior; a large update tends to escalate
UPDATE orders SET status = 'archived' WHERE created_at < '2020-01-01';
```
**Explanation:** Touching thousands of rows usually triggers lock escalation to table-level, blocking the whole table even though only a few rows were needed.

## Q23: What are intent locks for?
Intent locks (IS/IX) announce at a coarse level (table) that a transaction holds finer locks (rows/pages) underneath, allowing compatible coarse locks to coexist and letting conflicts be decided cheaply.

**Query:**
```sql
-- SQL Server / MySQL show intent locks internally during a transaction
BEGIN TRAN;
SELECT * FROM accounts WITH (TABLOCKX) WHERE id = 1;  -- explicit exclusive table lock
```
**Explanation:** With TABLOCKX the table is X-locked; concurrent operations must wait even on unrelated rows because intent/table lock conflicts are checked first.

## Q24: What is lock escalation?
Lock escalation converts many fine-grained locks (rows/pages) into one coarse-grained table lock to reduce lock-manager overhead, at the cost of drastically reduced concurrency.

**Query:**
```sql
-- SQL Server: escalation can be disabled/triggered per table via ALTER
ALTER TABLE orders SET (LOCK_ESCALATION = DISABLE);   -- keep row locks only
-- ALTERNATIVELY: SET (LOCK_ESCALATION = TABLE) is the default
```
**Explanation:** Default escalation occurs once a threshold of locks is exceeded; disabling it trades memory for concurrency and can cause OOM under heavy writes.

**Alt1:**
```sql
-- SQL Server limits locks before escalation by adding a fast filter
UPDATE orders SET status = 'archived'
 WHERE created_at < '2020-01-01' AND id % 10 = 0;   -- fewer rows → no escalation
```
**Explanation:** Shrinking the working set avoids crossing the escalation threshold, keeping concurrency high.

## Q25: How do you avoid or defer lock escalation in SQL Server?
Partition the table (escalation can go to partition or heap/B-tree), keep statements small, use ROWLOCK hints selectively, or set `LOCK_ESCALATION = AUTO`.

**Query:**
```sql
-- SQL Server: escalation to a partition instead of the whole table
ALTER TABLE orders SET (LOCK_ESCALATION = AUTO);
-- batches: update rows in small keyset windows
UPDATE orders SET status = 'archived'
WHERE id BETWEEN 1 AND 500 AND status = 'open';
```
**Explanation:** AUTO plus small batches keeps locks at row/partition level, so unrelated partitions and pagination ranges stay available to other transactions.


## Q26: PostgreSQL FOR UPDATE vs FOR NO KEY UPDATE: what is the difference?
FOR NO KEY UPDATE locks rows against UPDATE/DELETE but still permits concurrent FOR SHARE/KEY SHARE and foreign-key checks, whereas FOR UPDATE blocks all four.

**Query:**
```sql
-- PostgreSQL: KEY SHARE is enough when you only reference the key
BEGIN;
SELECT id FROM parent WHERE id = 5 FOR NO KEY UPDATE;
COMMIT;
```
**Explanation:** Choosing a weaker lock (FOR NO KEY UPDATE / FOR KEY SHARE) reduces blocking when you only set non-key columns or merely reference the parent key.

## Q27: What does FOR UPDATE OF <table> restrict in PostgreSQL?
It restricts the lock to rows of the named table(s) in a multi-table SELECT, so joins touched with `FOR UPDATE` only lock listed relations.

**Query:**
```sql
-- PostgreSQL: lock only the users row, not the joined orders row
SELECT u.id, o.id
  FROM users u
  JOIN orders o ON o.user_id = u.id
 WHERE u.id = 5
   FOR UPDATE OF u;
```
**Explanation:** Without `OF u`, every participating table's rows would be locked; with it, only `users` rows that actually get selected are locked.

## Q28: What does FOR UPDATE OF do in Oracle?
Oracle's `FOR UPDATE OF col` indicates which table(s) to lock; the named columns are only markers (any column of the target table works), and `NOWAIT` makes it fail fast instead of waiting.

**Query:**
```sql
-- Oracle: lock employees rows, fail fast if already locked
SELECT empno, sal
  FROM emp
 WHERE deptno = 10
   FOR UPDATE OF sal NOWAIT;
```
**Explanation:** The column list tells the optimizer which joined table to lock; `NOWAIT` returns ORA-00054 (locked) immediately rather than blocking.

## Q29: What does SKIP LOCKED do?
SKIP LOCKED skips rows locked by other transactions and returns only immediately available rows, making it perfect for parallel worker queues.

**Query:**
```sql
-- PostgreSQL: claim one unclaimed job, skipping work in progress
SELECT * FROM jobs
 WHERE status = 'pending'
 ORDER BY priority
 LIMIT 1
 FOR UPDATE SKIP LOCKED;
```
**Explanation:** Two workers running this concurrently get different rows instead of one waiting on the other — no lost work, no lock contention.

## Q30: What does NOWAIT do?
NOWAIT attempts a lock and errors out immediately instead of waiting for the lock timeout; if the row is locked you get an error telling you to retry.

**Query:**
```sql
-- PostgreSQL: fail fast if the row is locked
SELECT * FROM accounts WHERE id = 1 FOR UPDATE NOWAIT;
-- error: could not obtain lock on row in relation "accounts"
```
**Explanation:** NOWAIT converts a wait into an immediate exception, letting the application decide to retry or abandon. Available in PostgreSQL, MySQL 8.0+, Oracle.

## Q31: How do you build a job queue poll with SKIP LOCKED in MySQL?
MySQL 8.0 added `FOR UPDATE SKIP LOCKED`, allowing several workers to claim distinct rows concurrently from a queue table.

**Query:**
```sql
-- MySQL 8.0+ (also works in PostgreSQL)
BEGIN;
SELECT * FROM jobs
 WHERE status = 'queued'
 ORDER BY id
 LIMIT 5
 FOR UPDATE SKIP LOCKED;
---- claim by setting status inside the same transaction
UPDATE jobs SET status = 'running', claimed_by = CONNECTION_ID()
 WHERE id IN (...selected ids...);
COMMIT;
```
**Explanation:** SKIP LOCKED skips rows already locked for processing, so N workers each grab an exclusive slice with zero wait and no double-claim.

**Alt1:**
```sql
-- PostgreSQL equivalent with claim timestamp
SELECT * FROM jobs
 WHERE status = 'queued' AND claimed_at IS NULL
 ORDER BY priority DESC
 LIMIT 10
 FOR UPDATE SKIP LOCKED;
```
**Explanation:** Add a `claimed_at` column and only claim rows older than a heartbeat window to give workers crash-recovery semantics.

## Q32: What goes wrong polling a queue WITHOUT SKIP LOCKED?
Workers serialize on the same top row: each SELECT FOR UPDATE blocks on the previous worker's lock, so throughput collapses and you can get lock waits and deadlocks.

**Query:**
```sql
-- PostgreSQL: BAD pattern — all workers block on the same first row
SELECT * FROM jobs WHERE status = 'queued'
 ORDER BY priority
 LIMIT 1 FOR UPDATE;   -- worker 2 waits on worker 1's lock
```
**Explanation:** Only the first worker proceeds; the rest idle-wait on locks even though thousands of unclaimed jobs exist — effectively single-threaded consumption.

**Alt1:**
```sql
-- MySQL: the old workaround was a random offset, which is not concurrency-safe
SELECT * FROM jobs WHERE status = 'queued' ORDER BY RAND() LIMIT 1 FOR UPDATE;
```
**Explanation:** RAND() spreads contention statistically but wastes scans and can still collide; SKIP LOCKED is the correct primitive.

## Q33: What is the canonical use case for NOWAIT?
NOWAIT suits fast-fail cases: a user clicking "edit" when someone else is editing should get "already in use" immediately, not a hang.

**Query:**
```sql
-- Oracle: prevent double-editing of a document
SELECT * FROM documents WHERE id = 42 FOR UPDATE NOWAIT;
-- ORA-00054 → show "document is being edited by another user"
```
**Explanation:** The application turns the immediate lock error into friendly UX instead of letting the user wait indefinitely behind a peer's long transaction.

## Q34: What does the SQL Server UPDLOCK hint do?
UPDLOCK takes update (U) locks instead of shared locks for the read, which prevents conversion deadlocks and lets you reserve the row for modification.

**Query:**
```sql
-- SQL Server: lock the row as "mine to update"
BEGIN TRAN;
SELECT * FROM stock WITH (UPDLOCK) WHERE sku = 'A1';
UPDATE stock SET qty = qty - 1 WHERE sku = 'A1';
COMMIT;
```
**Explanation:** Later UPDATEs upgrade the U lock to X without waiting, and no other transaction can take U/X in between, giving serialized read-modify-write.

## Q35: What does the SQL Server ROWLOCK hint do?
ROWLOCK requests row-level locks for the statement, orphaning page/table locks, which increases concurrency but increases memory usage.

**Query:**
```sql
-- SQL Server: keep locks at row granularity during a bulk-ish update
UPDATE orders WITH (ROWLOCK) SET status = 'shipped'
 WHERE order_id BETWEEN 1000 AND 5000;
```
**Explanation:** Without the hint the engine may escalate to page/table locks; ROWLOCK tells it not to, prudent for online tables with mixed traffic.

**Alt1:**
```sql
-- SQL Server: ROWLOCK combined with READPAST to skip locked rows instead of waiting
SELECT * FROM jobs WITH (ROWLOCK, READPAST) WHERE status = 'queued';
```
**Explanation:** READPAST behaves like SKIP LOCKED — locked rows are silently skipped — letting multiple workers drain a queue in parallel.

## Q36: What does the SQL Server HOLDLOCK hint do?
HOLDLOCK extends a shared/update lock to the end of the transaction (like SERIALIZABLE), preventing other transactions from modifying or inserting rows in the read range.

**Query:**
```sql
-- SQL Server: hold the range lock until COMMIT to prevent phantom inserts
BEGIN TRAN;
SELECT * FROM stock WITH (HOLDLOCK) WHERE sku = 'A1';
COMMIT;
```
**Explanation:** HOLDLOCK makes the SELECT behave as a serializable read for the predicate range, so a concurrent INSERT into the same range blocks.

## Q37: SQL Server WITH (UPDLOCK, ROWLOCK, HOLDLOCK) combined: what do you get?
A row-level update lock held to end of transaction — a pessimistic "lock this row for my later update" idiom without range escalation.

**Query:**
```sql
-- SQL Server: classic row-level pessimistic lock
BEGIN TRAN;
SELECT * FROM accounts WITH (UPDLOCK, ROWLOCK) WHERE id = 10;
-- ... business logic ...
UPDATE accounts SET balance = balance - 50 WHERE id = 10;
COMMIT;
```
**Explanation:** UPDLOCK reserves upgrade headroom, ROWLOCK prevents escalation, and the lock persists until COMMIT because of the open transaction.

**Alt1:**
```sql
-- SQL Server: adding HOLDLOCK extends it to a serializable range lock
SELECT * FROM accounts WITH (UPDLOCK, ROWLOCK, HOLDLOCK) WHERE status = 'open';
```
**Explanation:** Now the whole qualifying range is U-locked until commit, guarding against phantoms as well, at the cost of broader blocking.

## Q38: INSERT/UPDATE with triggers and cascades: how do locks spread?
Triggers and foreign-key cascades run in the same statement and take locks on every row they touch, so a small UPDATE can lock large dependency subtrees.

**Query:**
```sql
-- PostgreSQL: cascading DELETE acquires locks on child rows too
DELETE FROM parents WHERE id = 1;   -- triggers ON DELETE CASCADE on children
```
**Explanation:** The cascade's child-row operations are transactional and X-locked until commit; long cascades hold locks broadly and can deadlock with concurrent child updates.

## Q39: What is optimistic concurrency control (OCC)?
Optimistic CC validates conflicts at commit time instead of locking upfront: read data, do work, then check no one changed it (`WHERE version = ?`) and retry on failure.

**Query:**
```sql
-- PostgreSQL / MySQL: version-column check in the UPDATE
UPDATE documents
   SET body = 'v2', version = version + 1
 WHERE id = 7 AND version = 1;
-- 0 rows updated → conflict detected, retry from scratch
```
**Explanation:** OCC shines at low contention where waits are waste; it converts contention from blocking into a commit-time retry loop.

**Alt1:**
```sql
-- SQL Server: use ROWVERSION (rowversion) as a built-in version column
UPDATE documents SET body = 'v2'
 WHERE id = 7 AND rowver = 0x00000000000007D1;   -- compare stored rowver
```
**Explanation:** SQL Server's ROWVERSION auto-increments on every update, giving you a free optimistic check without manual versioning.

## Q40: What is pessimistic concurrency control?
Pessimistic CC locks resources before using them (SELECT FOR UPDATE) so no other transaction can interfere while you hold the lock; conflicts are prevented, not detected.

**Query:**
```sql
-- PostgreSQL / MySQL / Oracle
BEGIN;
SELECT seat FROM seats WHERE id = 12 FOR UPDATE;   -- lock now
UPDATE seats SET booked_by = 99, status = 'taken' WHERE id = 12;
COMMIT;
```
**Explanation:** The booking is serialized at lock acquisition; the only cost is waiting. Pessimistic fits high-contention, correctness-sensitive resources.

## Q41: Pessimistic vs optimistic: how do you choose?
Choose pessimistic when contention is high or the cost of a failed retry is high (money, seats); choose optimistic when reads dominate and retries are cheap.

**Query:**
```sql
-- PostgreSQL: pessimistic for a hot seat-booking write ...
SELECT * FROM seats WHERE id = 12 FOR UPDATE;
-- ... optimistic for a rarely-touched profile update
UPDATE profiles SET display_name = 'n'
 WHERE user_id = 3 AND version = 4;
```
**Explanation:** A blocking FOR UPDATE prevents retries/lost work under high write contention; the version check avoids needless locking where collisions are rare.

## Q42: What is a deadlock?
A deadlock is a cycle where each transaction holds a lock the other wants, so neither can proceed; the DBMS resolves it by aborting one victim.

**Query:**
```sql
-- MySQL: two concurrent transactions deadlocking on swapped lock order
-- T1: UPDATE a ...;  UPDATE b ...;
-- T2: UPDATE b ...;  UPDATE a ...;
-- ERROR 1213 (40001): Deadlock found when trying to get lock; try restarting transaction
```
**Explanation:** Database detects the cycle, rolls back the lighter victim, and reports which statement caused it; the app must retry.

## Q43: What are the common causes of deadlocks?
Swapped lock order across transactions, escalating shared→exclusive at different times, gap-lock interactions, range scans vs inserts, triggers/cascades, and missing indexes that cause table scans to lock broad ranges.

**Query:**
```sql
-- SQL Server: classic cause — different acquisition order in two stored procs
-- spA: UPDATE A then B      spB: UPDATE B then A   → cycle
-- Fix: standardize on the same order A-then-B everywhere
BEGIN TRAN;
UPDATE accounts SET bal = bal - 10 WHERE id = 1;
UPDATE accounts SET bal = bal + 10 WHERE id = 2;
COMMIT;
```
**Explanation:** If all transactions acquire account locks in ascending id order (1 then 2), no two transactions can hold each other's target and cycle.

## Q44: How do databases detect deadlocks?
Engines build a waits-for graph (who is blocked by whom) and detect a cycle; MySQL (InnoDB) uses a background detector plus lock-wait timeout heuristic, PostgreSQL uses a timeout and prints a deadlock detail.

**Query:**
```sql
-- PostgreSQL: deadlock detection is after deadlock_timeout (default 1s)
SET deadlock_timeout = '200ms';   -- detect deadlocks faster
-- then run the two crossed transactions to trigger:
-- ERROR: deadlock detected, Process 123 waits for ShareLock...Process 456 waits for ShareLock...
```
**Explanation:** After detecting the cycle, the DB aborts the transaction that caused the least work (victim) and notifies the client to retry.

## Q45: What is a waits-for (deadlock detection) graph?
A directed graph where nodes are transactions and edges point from a waiting transaction to the lock-holder it needs; a cycle in the graph proves a deadlock.

**Query:**
```sql
-- MySQL: SHOW ENGINE INNODB STATUS prints the LATEST DETECTED DEADLOCK graph
SHOW ENGINE INNODB STATUS\G
-- *** (1) TRANSACTION: ... holds lock ... waits for lock ...
-- *** (2) TRANSACTION: ... holds lock ... waits for lock ...
```
**Explanation:** The output shows the two transactions, which locks each holds, and which each waits on — the graph's cycle you must eliminate by lock ordering.

## Q46: How should you resolve a deadlock in application code?
Catch the deadlock error (MySQL 1213, PostgreSQL 40P01, SQL Server 1205), retry the whole transaction idempotently (careful with side effects/stored-proc output), and bound the retry count.

**Query:**
```sql
-- SQL Server: catch error 1205 and retry the transaction
WHILE @tries < 3
BEGIN TRY
    BEGIN TRAN;
    UPDATE t SET ...; UPDATE u SET ...;
    COMMIT; BREAK;
END TRY
BEGIN CATCH
    IF ERROR_NUMBER() = 1205 AND @tries < 3
        ROLLBACK; SET @tries = @tries + 1;   -- retry with backoff
    ELSE THROW;
END CATCH
```
**Explanation:** Since the victim transaction is fully rolled back, retrying the same logical operation is safe; keep the pattern short to avoid compounding contention.

**Alt1:**
```sql
-- MySQL: retry loop in application pseudocode
-- for attempt in 1..3:
--    try: BEGIN; ...work...; COMMIT; break
--    except MySQLdb.OperationalError(e) if e.args[0] == 1213: continue
```
**Explanation:** A small capped retry with random backoff turns a detected deadlock into a successful commit for most workloads.

## Q47: What is lock ordering and why does it matter?
Lock ordering is the discipline of always acquiring locks in the same global sequence; it makes waits-for graphs acyclic, eliminating deadlock cycles.

**Query:**
```sql
-- PostgreSQL: always lock lower id first regardless of direction of transfer
BEGIN;
SELECT * FROM accounts WHERE id = LEAST(:from_id, :to_id) FOR UPDATE;
SELECT * FROM accounts WHERE id = GREATEST(:from_id, :to_id) FOR UPDATE;
COMMIT;
```
**Explanation:** With a monotonic order (1 then 2), two money transfers between the same accounts cannot cross-lock, so deadlock is structurally impossible.

## Q48: What is the single-writer-per-key pattern?
One key (e.g., an account or user) may be written by only one transaction at a time, enforced with a dedicated lock row or FOR UPDATE on the parent record.

**Query:**
```sql
-- PostgreSQL: serialize all work for account 7 through one lock row
BEGIN;
SELECT * FROM account_lock WHERE account_id = 7 FOR UPDATE;  -- all writers take this
UPDATE accounts SET balance = balance + 100 WHERE id = 7;
COMMIT;
```
**Explanation:** Everyone who mutates account 7 first locks its sentinel row, so writers serialize per key without a table-wide lock or complex coordination.

## Q49: What is two-phase / phased locking?
Two-Phase Locking (2PL) grows locks during the transaction and never acquires new locks after the first release; the standard history ensures serializability and is the basis for read-uncommitted-free engines.

**Query:**
```sql
-- SQL Server/PostgreSQL: a lock order that respects 2PL
BEGIN;                  -- phase 1: acquire
SELECT * FROM a WHERE id = 1 FOR UPDATE;
SELECT * FROM b WHERE id = 1 FOR UPDATE;
COMMIT;                 -- phase 2: release everything
```
**Explanation:** As long as the second acquisition never happens after any release within the transaction, the execution is serializable per 2PL.

## Q50: What is innodb_lock_wait_timeout?
MySQL's variable (default 50s) controlling how long a lock request waits before returning `ERROR 1205 Lock wait timeout exceeded`; deadlock is separate (1213).

**Query:**
```sql
-- MySQL: tune globally, or measure current value
SET GLOBAL innodb_lock_wait_timeout = 10;
SHOW VARIABLES LIKE 'innodb_lock_wait_timeout';
-- 1205 is a timeout, 1213 is a deadlock
```
**Explanation:** A 1205 error means the requesting transaction never got the lock within the window; the SQL statement is rolled back and should be retried after checking the blocker.


## Q51: What is lock_timeout in PostgreSQL and how is it different from deadlock_timeout?
`lock_timeout` (default 0 = infinity) aborts a statement that waits too long for any lock; `deadlock_timeout` only controls how quickly a deadlock is detected. Both are per-session settings.

**Query:**
```sql
-- PostgreSQL
SET lock_timeout = '2s';
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;   -- ERROR: canceling statement due to lock timeout
```
**Explanation:** A lock timeout rolls back the statement (not the whole transaction necessarily); a deadlock timeout is detection latency and rolls back the victim transaction.

## Q52: What is a gap lock?
A gap lock locks the space between index records (and before first / after last) so no other transaction can insert a row into that gap — it does not lock the records themselves.

**Query:**
```sql
-- MySQL: the following FOR UPDATE under RR takes gap+next-key locks
BEGIN;
SELECT * FROM products WHERE price BETWEEN 100 AND 200 FOR UPDATE;
-- concurrent INSERT of a row with price=150 now blocks
COMMIT;
```
**Explanation:** The gap between existing index entries gets locked, blocking phantom inserts; note gap locks only guard inserts, not updates of existing rows.

## Q53: What is a next-key lock?
A next-key lock = record lock + gap lock on the gap immediately after the record; it locks the record and prevents inserts into the adjacent gap, which is how MySQL InnoDB stops phantoms at REPEATABLE READ.

**Query:**
```sql
-- MySQL (RR): scanning index rows acquires record+gap "next-key" locks
BEGIN;
SELECT * FROM products WHERE id BETWEEN 10 AND 20 FOR UPDATE;
COMMIT;
```
**Explanation:** A concurrent INSERT with id in (10,20] waits because the next-key lock covers that gap; this is the mechanism behind InnoDB's phantom prevention.

## Q54: What is a phantom read?
A phantom read is re-executing a query within a transaction and seeing newly inserted rows that appear/disappear, i.e., the result set is not stable under an isolation level without range locks.

**Query:**
```sql
-- PostgreSQL READ COMMITTED: a range may grow mid-transaction
BEGIN ISOLATION LEVEL READ COMMITTED;
SELECT count(*) FROM orders WHERE total > 1000;      -- 3
-- another tx commits an INSERT matching the predicate
SELECT count(*) FROM orders WHERE total > 1000;      -- 4 (phantom!)
COMMIT;
```
**Explanation:** No gap locks exist at READ COMMITTED, so concurrent inserts change later reads; REPEATABLE READ (MySQL) or SERIALIZABLE eliminate this.

## Q55: How do next-key locks prevent phantoms?
Under REPEATABLE READ, InnoDB locks the scanned index range with record+gap locks, so a concurrent insert into that range blocks until the locking transaction commits/rolls back, keeping the read set stable.

**Query:**
```sql
-- MySQL: range locking that blocks the phantom
-- tx A: SELECT * FROM orders WHERE id BETWEEN 100 AND 200 FOR UPDATE;  (next-key locked)
-- tx B: INSERT INTO orders (id, ...) VALUES (150, ...);   -- blocked until A commits
COMMIT;  -- A releases → B proceeds, but the phantom is gone for A's snapshot
```
**Explanation:** The gap between id 100 and 200 is closed to inserts, so A re-running the query always sees the same set at RR.

## Q56: Do gap locks exist at READ COMMITTED in MySQL?
No. At READ COMMITTED, InnoDB uses only record locks (next-key locks are downgraded), trading phantom prevention for higher concurrency.

**Query:**
```sql
-- MySQL: force READ COMMITTED to avoid gap-lock blocking for single-row work
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
SELECT * FROM orders WHERE id = 100 FOR UPDATE;   -- record lock only
```
**Explanation:** With only record locks, concurrent inserts into nearby gaps succeed; the cost is that phantoms are possible within such transactions.

**Alt1:**
```sql
-- MySQL: READ COMMITTED still keeps binlog row-based required
-- (set binlog_format = ROW when demoting to RC globally)
SET GLOBAL binlog_format = 'ROW';
SET GLOBAL transaction_isolation = 'READ-COMMITTED';
```
**Explanation:** MySQL requires row-based binlog for repeatability-of-guarded-statements safety at RC; statement-based binlog + RC gaps can be unsafe.

## Q57: How do you disable or reduce gap locking when you need it gone?
Use READ COMMITTED isolation, lock only primary-key single rows, and keep predicates index-searching (no full scans), since gap locks only materialize where indexes exist.

**Query:**
```sql
-- MySQL: single-row primary-key lock → record lock, no gap involved
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN;
SELECT * FROM accounts WHERE id = 7 FOR UPDATE;   -- record lock only
COMMIT;
```
**Explanation:** Unique-index exact matches cannot have phantom gaps, and RC drops gap locks; combining both minimizes range blocking.

## Q58: When does an UPDATE take gap locks in InnoDB?
Whenever the UPDATE's search (scan) under REPEATABLE READ covers index ranges and the engine uses next-key locks; it also gap-locks if the WHERE cannot use a unique index or matches multiple rows.

**Query:**
```sql
-- MySQL: range UPDATE obtains next-key locks across the covered index
BEGIN;
UPDATE inventory SET qty = qty - 1
 WHERE sku_id BETWEEN 100 AND 200 AND warehouse = 1;
COMMIT;
```
**Explanation:** The two-part predicate scans an index range, so records plus the following gaps are locked; a concurrent INSERT into that sku range blocks.

## Q59: Give a deadlock scenario caused purely by gap locks.
Two transactions gap-lock overlapping-but-different gaps and then insert into each other's gaps, creating a lock cycle.

**Query:**
```sql
-- MySQL (RR): classic gap deadlock
-- T1: SELECT * FROM t WHERE id BETWEEN 10 AND 20 FOR UPDATE;   (locks gap 10-20)
-- T2: SELECT * FROM t WHERE id BETWEEN 15 AND 25 FOR UPDATE;   (locks gap 15-25)
-- T1: INSERT INTO t (id) VALUES (18);  -- waits on T2's gap (15-25)
-- T2: INSERT INTO t (id) VALUES (16);  -- waits on T1's gap (10-20) → deadlock
SELECT * FROM t WHERE id BETWEEN 10 AND 20 FOR UPDATE;
```
**Explanation:** The two insert-intention locks target each other's gaps; InnoDB aborts one insert with 1213 to break the cycle.

## Q60: How do you inspect current locks in MySQL?
Use SHOW ENGINE INNODB STATUS for the lock/transaction dump or the performance_schema.data_locks / data_lock_waits tables for live, queryable data.

**Query:**
```sql
-- MySQL: live lock inspection
SELECT * FROM performance_schema.data_locks;
SELECT * FROM performance_schema.data_lock_waits;
SHOW ENGINE INNODB STATUS\G
```
**Explanation:** performance_schema shows what each transaction holds and which waits exist; the STATUS dump also includes recent deadlock details and lock wait sections.

**Alt1:**
```sql
-- MySQL: reject the dump and use the sys schema for a human-readable wait summary
SELECT * FROM sys.innodb_lock_waits;
```
**Explanation:** sys.innodb_lock_waits joins blocked ↔ blocking transactions, their SQL, and ages — the fastest way to find "who is the blocker?"

## Q61: What is pg_locks and what does it tell you?
pg_locks is PostgreSQL's system view listing every lock the backend processes hold or request, with lock types (relation, tuple, transactionid, advisory) and grant status.

**Query:**
```sql
-- PostgreSQL: find which query holds the blocking lock
SELECT blocked.pid AS blocked_pid,
       blocker.pid AS blocker_pid,
       blocker.query AS blocking_query
  FROM pg_stat_activity blocked
  JOIN pg_locks bl ON bl.pid = blocked.pid AND NOT bl.granted
  JOIN pg_locks bk ON bk.pid <> blocked.pid
   AND bk.locktype = bl.locktype AND bk.relation = bl.relation AND bk.granted
  JOIN pg_stat_activity blocker ON blocker.pid = bk.pid
 WHERE blocked.query <> '<IDLE>';
```
**Explanation:** Matching not-granted locks against granted locks on the same relation reveals the blocker chain; add pg_blocking_pids(pid) for a direct helper.

**Alt1:**
```sql
-- PostgreSQL: simpler built-in blocker list
SELECT pid, pg_blocking_pids(pid) AS blocked_by, state, query
  FROM pg_stat_activity
 WHERE pid <> pg_backend_pid();
```
**Explanation:** pg_blocking_pids() returns, per backend, the PIDs blocking it — the quickest way to identify lock holders in a hung system.

## Q62: How do you inspect locks with sys.dm_tran_locks in SQL Server?
sys.dm_tran_locks lists active lock resources with their modes (S/X/U/IX), request status (GRANT/WAIT), and owning session/transaction; pair it with sys.dm_exec_requests for the waiting queries.

**Query:**
```sql
-- SQL Server: find blockers and waiters
SELECT r.session_id AS waiting_session,
       w.blocking_session_id AS blocker,
       r.wait_type,
       l.resource_type, l.request_mode, l.request_status
FROM sys.dm_exec_requests r
JOIN sys.dm_tran_locks l ON r.session_id = l.request_session_id
LEFT JOIN sys.dm_os_waiting_tasks w ON r.session_id = w.session_id
WHERE r.blocking_session_id > 0;
```
**Explanation:** dm_exec_requests shows which request waits on which session via blocking_session_id; dm_tran_locks fills in type, mode, and grant status.

## Q63: How does Oracle expose locks (V$LOCK)? Key differences?
Oracle uses enqueues (V$LOCK) with modes like RX (row S), SX (row X); lock waits surface as wait_event 'enq: TX - row lock contention', and block/waiter tracking uses V$SESSION + V$LOCK.

**Query:**
```sql
-- Oracle: who is blocking whom
SELECT blocked.sid AS waiter, blocker.sid AS blocker, blocker.serial# 
  FROM v$session blocked
  JOIN v$session blocker ON blocked.blocking_session = blocker.sid
 WHERE blocked.blocking_session IS NOT NULL;
```
**Explanation:** blocking_session gives the blocker directly; convert sids to SQL text via v$sql/v$session.prev_sql_id to find the offending statement.

## Q64: How do you find the blocking chain's query text?
Join the waiting session to its blocking sessions and pull SQL text; MySQL can use sys.innodb_lock_waits, PostgreSQL pg_stat_activity, SQL Server dm_exec_sql_text.

**Query:**
```sql
-- SQL Server: blocking query text
SELECT blocking.blocking_session_id,
       q.text AS blocker_query
FROM sys.dm_exec_requests blocking
CROSS APPLY sys.dm_exec_sql_text(blocking.sql_handle) q
WHERE blocking.blocking_session_id > 0;
```
**Explanation:** The blocking request's sql_handle maps to the exact statement holding the lock; address the statement (add an index, shrink its range, or commit earlier).

## Q65: How do you kill a blocker safely?
Terminate only after confirming it is a stale/runaway transaction, since killing loses its work; use native kill with the session id, plus a transaction-only kill (Oracle/sysadmin) where available.

**Query:**
```sql
-- MySQL: kill a specific session (or connection)
SELECT id FROM sys.innodb_lock_waits;       -- or: SHOW PROCESSLIST;
KILL 12345;
```
**Explanation:** KILL aborts the backend and rolls that transaction back, releasing all its locks — the blockers immediately unblock afterwards.

**Alt1:**
```sql
-- PostgreSQL: terminate a backend
SELECT pg_terminate_backend(4567);
-- SQL Server version:
-- KILL 4567;    (optionally WITH STATUSONLY to preview)
```
**Explanation:** All three engines support a session-level kill with rollback; prefer terminating only genuinely orphaned sessions, not long legitimate ones.

## Q66: Lock wait timeout vs deadlock — same thing?
No. A lock-wait timeout (MySQL 1205, Postgres lock_timeout) is a slow request never granted; a deadlock (MySQL 1213, Postgres 40P01, SQL Server 1205) is a cycle already detected and broken by aborting a victim.

**Query:**
```sql
-- MySQL: 1205 vs 1213 side by side
-- 1205: Lock wait timeout exceeded; try restarting transaction        (never got the lock)
-- 1213: Deadlock found when trying to get lock; try restarting transaction (cycle, victim aborted)
SHOW VARIABLES LIKE 'innodb_lock_wait_timeout';
```
**Explanation:** 1205 means "another transaction held it too long"; 1213 means "two transactions deadlocked and one was sacrificed". Both need retries; 1213 needs lock-order fixes.

## Q67: What is a hot row / hot-spot contention?
A highly contended row written by many transactions (e.g., a global counter or the latest-ticket ID) that serializes all writers and becomes a throughput bottleneck.

**Query:**
```sql
-- PostgreSQL/MySQL: a hot counter row that serializes every request
UPDATE counters SET n = n + 1 WHERE name = 'global_visits';
```
**Explanation:** Every increment takes the row's X lock for the transaction duration, so write throughput is capped at one row-update at a time.

## Q68: How do you reduce hot-row contention?
Shard the counter into N sub-rows and sum them on read; also shorten transaction time, or switch to idempotent atomics and read on replica.

**Query:**
```sql
-- PostgreSQL: sharded counter update
UPDATE counters SET n = n + 1
 WHERE name = 'visits' AND shard = (random() * 100)::int % 100;
-- read total: SELECT sum(n) FROM counters WHERE name = 'visits';
```
**Explanation:** 100 separate rows spread the X-lock contention across 100 distinct locks; the sum aggregates on read — order-of-magnitude wins for counters.

**Alt1:**
```sql
-- SQL Server: separate table per shard to avoid a per-row arms race
UPDATE counters_07 SET n = n + 1 WHERE counter_key = 'visits';
-- shard chosen by round-robin in the app: counters_00 .. counters_99
```
**Explanation:** Picking the shard key in the application layer spreads contention with near-zero per-row overhead; aggregating reads sums the shard tables.

## Q69: What is a locking read used for inside a transaction?
A locking read (FOR UPDATE / FOR SHARE / LOCK IN SHARE MODE / WITH (UPDLOCK)) turns a normal read into a lock-acquiring read so the read-to-write gap is serialized.

**Query:**
```sql
-- PostgreSQL: read-then-write protected for the whole transaction
BEGIN;
SELECT stock FROM skus WHERE id = 9 FOR UPDATE;    -- locks the row
UPDATE skus SET stock = stock - 1 WHERE id = 9;
COMMIT;
```
**Explanation:** Without FOR UPDATE, two transactions could both read stock=1 and each minus 1 → stock ends at 0 instead of -1; the locking read fixes it.

## Q70: SELECT ... FOR UPDATE across a JOIN: what gets locked?
All rows of all joined tables that survive the join are locked (PostgreSQL), while `FOR UPDATE OF t` (with OF) restricts it to named tables.

**Query:**
```sql
-- PostgreSQL: locks carts + cart_items rows for the user's cart
BEGIN;
SELECT c.id, ci.product_id
  FROM carts c
  JOIN cart_items ci ON ci.cart_id = c.id
 WHERE c.user_id = 55
   FOR UPDATE OF c;               -- only c (carts) rows locked here
COMMIT;
```
**Explanation:** Use OF to keep the lock footprint small; without OF, items rows lock too, increasing deadlock surface with concurrent item updates.

## Q71: How do you lock multiple rows/tables without deadlocking?
Acquire locks in a deterministic global order (e.g., sorted keys), keep the locked set minimal, and hold it for as short a transaction as possible.

**Query:**
```sql
-- PostgreSQL: lock all involved accounts in ascending id order
BEGIN;
SELECT * FROM accounts
 WHERE id IN (200, 1, 55)
 ORDER BY id                       -- 1, 55, 200
 FOR UPDATE;                       -- take them in that order
COMMIT;
```
**Explanation:** If every transaction sorts account ids before locking, no transaction can wait on one it would later be asked to release — cycles become impossible.

## Q72: What is a write skew and how is it different from a lost update?
Write skew is two transactions each update different rows using a constraint dependent on each other's row, leaving the invariant violated — neither reads stale data, but their individual writes are inconsistent together.

**Query:**
```sql
-- PostgreSQL: doctor on-call invariant (≥1 doctor must remain)
-- T1: SELECT count(*) FROM doctors WHERE on_call;       -- 2
-- T2: SELECT count(*) FROM doctors WHERE on_call;       -- 2
-- T1: UPDATE doctors SET on_call = false WHERE id = 1;  -- ok individually
-- T2: UPDATE doctors SET on_call = false WHERE id = 2;  -- ok individually
-- result: 0 on call ← invariant broken, and no single row was "lost"
SELECT count(*) FROM doctors WHERE on_call;
```
**Explanation:** Both based their decision on the same old count; neither overwrote the other's row, yet the aggregate constraint broke. Needs predicate/table lock or SERIALIZABLE.

## Q73: How do you prevent write skew?
Lock the predicate range (`SELECT ... FOR UPDATE` over the check's domain), lock a sentinel row, or use SERIALIZABLE + explicit conflict checks at serialization point.

**Query:**
```sql
-- PostgreSQL: lock ALL rows that the invariant reads over
BEGIN;
SELECT id FROM doctors FOR UPDATE;              -- freezes the on-call set
--- now recompute count and decide
UPDATE doctors SET on_call = false WHERE id = 1;
COMMIT;
```
**Explanation:** Locking the whole checked range serializes the "count then update" steps so the second transaction sees the first's committed change before computing its count.

## Q74: What are predicate locks in SERIALIZABLE?
Predicate locks claim a condition (e.g., "WHERE price > 100") rather than specific rows; any insert/update matching the predicate conflicts, blocking matches regardless of where they are inserted.

**Query:**
```sql
-- PostgreSQL: SSI uses predicate locks behind the scenes
BEGIN ISOLATION LEVEL SERIALIZABLE;
SELECT * FROM products WHERE price > 100;      -- predicate locked
COMMIT;  -- a concurrent matching insert would serialize/abort instead
```
**Explanation:** True predicate locks cover not-yet-existing rows, which record/gap locks cannot; PostgreSQL implements them implicitly in SSI (serializable snapshot isolation).

## Q75: What is SSI (serializable snapshot isolation)?
PostgreSQL's SERIALIZABLE mode: snapshot reads plus automatic predicate-based conflict detection whose serialization-point checks detect anomalies (write skew) and abort one transaction with `40001 serialization_failure`.

**Query:**
```sql
-- PostgreSQL: allow automatic retries when SERIALIZABLE aborts
BEGIN ISOLATION LEVEL SERIALIZABLE;
-- ... any read-modify-write ...
COMMIT;
-- application loop: on ERROR 40001 SERIALIZATION FAILURE, re-run the whole transaction
```
**Explanation:** SSI preserves consistent snapshots yet serializes by aborting one side of an actual conflict (including write skew), relying on bounded application retries.

**Alt1:**
```sql
-- PostgreSQL: you can also push the retry into SQL with a savepoint+loop
-- (most dialects just catch 40001 / 1213 / 1205 in the app)
DO $$
BEGIN
  LOOP
    BEGIN
      BEGIN ISOLATION LEVEL SERIALIZABLE;
      -- critical section
      COMMIT;
      EXIT;
    EXCEPTION WHEN serialization_failure THEN
      NULL;  -- sleep & retry
    END;
  END LOOP;
END $$;
```
**Explanation:** For simple cases an in-SQL retry loop works; for real apps, keep the retry in the service layer where you control boundary, timeout, and side effects.


## Q76: Walk through the classic two-account transfer deadlock.
Two transfers move money in opposite directions on the same two accounts; each locks one account, then waits for the other's lock, forming a cycle.

**Query:**
```sql
-- PostgreSQL: transfer A→B (T1) and B→A (T2) run concurrently
-- T1: UPDATE accounts SET bal=bal-100 WHERE id=1;  -- locks 1
--     UPDATE accounts SET bal=bal+100 WHERE id=2;  -- waits: 2 locked by T2
-- T2: UPDATE accounts SET bal=bal-100 WHERE id=2;  -- locks 2
--     UPDATE accounts SET bal=bal+100 WHERE id=1;  -- waits: 1 locked by T1
-- → ERROR: deadlock detected
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
```
**Explanation:** T1 holds 1 and wants 2; T2 holds 2 and wants 1. The engine aborts one victim; the transfer logic must then be retried — or, better, never acquire locks in cross-order.

## Q77: How do you fix the transfer deadlock structurally?
Always lock both accounts in the same deterministic order (e.g., ascending id) regardless of transfer direction, making a cross-order cycle impossible.

**Query:**
```sql
-- PostgreSQL: order-insensitive by id
BEGIN;
SELECT * FROM accounts
 WHERE id IN (:from_id, :to_id)
 ORDER BY id FOR UPDATE;                  -- sorted: id 1 then id 2
UPDATE accounts SET balance = balance - :amt WHERE id = :from_id;
UPDATE accounts SET balance = balance + :amt WHERE id = :to_id;
COMMIT;
```
**Explanation:** Both T1 and T2 now take id 1's lock then id 2's, so no transaction waits on the other's held lock — the deadlock is impossible by construction.

**Alt1:**
```sql
-- PostgreSQL: keep server-side ordering even if ids arrive reversed
SELECT * FROM accounts
 WHERE id IN (:from_id, :to_id)
 ORDER BY (id = :from_id)::int, id FOR UPDATE;
```
**Explanation:** A stable secondary sort guarantees identical acquisition order across call sites, which is the crucial property (never "lock whichever id was passed first").

## Q78: What does FOR UPDATE look like in a full, safe financial transfer?
Lock both rows, check the balance, then apply both deltas in one transaction; the single-writer-per-key guarantee comes from the row locks.

**Query:**
```sql
-- PostgreSQL: end-to-end transfer
BEGIN;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;   -- debit side locked
SELECT balance FROM accounts WHERE id = 2 FOR UPDATE;   -- credit side locked
UPDATE accounts SET balance = balance - 100, updated_at = now() WHERE id = 1
  AND balance >= 100;                                   -- guarded check
-- if 0 rows: insufficient funds → ROLLBACK
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```
**Explanation:** Locks serialize per account, the WHERE balance >= 100 guard makes the check atomic with the write, and the transaction ensures debits and credits move together.

## Q79: What are advisory locks?
Named, application-meaningful locks that don't guard rows at all; they coordinate code-level resources (processes, jobs, k8s leader election) with the same transaction-scoped or session-scoped lifecycle.

**Query:**
```sql
-- PostgreSQL: session-level advisory lock for a "only one worker per queue"
SELECT pg_advisory_lock(hashtext('queue:checkout'));
-- ... exclusive critical section ...
SELECT pg_advisory_unlock(hashtext('queue:checkout'));
```
**Explanation:** Advisory locks are pure namespaces — no table, row, of overhead — so two variants: transaction-scoped (pg_advisory_xact_lock) and session-scoped (pg_advisory_lock).

**Alt1:**
```sql
-- PostgreSQL: transaction-scoped advisory lock auto-releases at COMMIT
BEGIN;
SELECT pg_advisory_xact_lock(12345);
-- critical section
COMMIT;  -- lock released automatically
```
**Explanation:** xact variant never needs an explicit unlock; pair with pg_try_advisory_xact_lock for non-blocking acquisition in workers.

## Q80: What is pg_try_advisory_lock and when do you use it?
The non-blocking variant returns true/false immediately instead of waiting; it is the basis for "claim a slot or fail fast" patterns such as multi-instance schedulers.

**Query:**
```sql
-- PostgreSQL: only one app instance becomes "leader"
SELECT pg_try_advisory_lock(42) AS got_it;
-- got_it=true → this instance is the leader; false → another holds it, stand by
```
**Explanation:** Combined with a heartbeat loop and unlock, this implements distributed locking with zero special infrastructure, no row, and no deadlock wait.

## Q81: How does MySQL's GET_LOCK compare to an advisory lock?
GET_LOCK/RELEASE_LOCK provide named locks similar to PostgreSQL advisory locks, but deprecated; the supported alternative is a service (e.g., OS, ZooKeeper) or a dedicated lock table.

**Query:**
```sql
-- MySQL: named lock with timeout (seconds)
SELECT GET_LOCK('leader_election', 5);      -- 1 if acquired, 0 if busy
-- critical section
SELECT RELEASE_LOCK('leader_election');
```
**Explanation:** Same idea as advisories; for production, consider a lock table or a dedicated coordination service because named locks die with the connection and can surprise.

## Q82: How do locking and indexes interact?
Locks are taken on indexed structures — a unique index lookup locks exactly the found record, while a full scan or non-covering index search locks many records/pages, expanding the lock footprint massively.

**Query:**
```sql
-- MySQL: index-driven lock granularity difference
UPDATE orders SET status='shipped' WHERE order_id = 7;      -- 1 record lock
UPDATE orders SET status='shipped' WHERE customer_note = 'x';  -- needs table-ish locks
ALTER TABLE orders ADD INDEX idx_status (status);           -- shrink future footprint
```
**Explanation:** A unique-key lookup touches one record; a non-indexed filter scans (and locks) whole ranges — adding targeted indexes is the highest-leverage deadlock fix.

## Q83: What is index-based lock ordering?
Ordering lock acquisition by index values (e.g., always ascending keys) so row/range locks are granted in a monotonic sequence — the engine's pagination then rarely trips over itself.

**Query:**
```sql
-- MySQL/PostgreSQL: process ids in ascending order to guarantee 2PL order
DECLARE cur CURSOR FOR
  SELECT id FROM orders
   WHERE status = 'pending'
   ORDER BY id           -- stable ascending iteration
   FOR UPDATE;
```
**Explanation:** Stable ORDER BY makes multiple workers' lock sequence predictable, and consistent ordering is a proven way to eliminate most lock-cycle deadlocks.

## Q84: Triggers and cascades: how do they affect locking?
Triggers, ON UPDATE/DELETE cascades, and generated columns re-enter DML within the same statement and acquire their own locks; one statement can therefore lock many unrelated subtrees.

**Query:**
```sql
-- PostgreSQL: auditing trigger inserts under the same transaction's locks
CREATE TRIGGER audit_account
AFTER UPDATE ON accounts
FOR EACH ROW
EXECUTE FUNCTION log_account_change();  -- this INSERT locks audit rows too
UPDATE accounts SET balance = balance - 1 WHERE id = 9;
```
**Explanation:** The trigger's write to `audit_log` takes row locks held to COMMIT; heavy concurrent updates + a slow trigger multiply lock holders and deadlock chances.

## Q85: What is autocommit and how does it affect locks?
With autocommit ON, every statement is its own transaction, so its locks release immediately at statement end — the source of many "why is this row unlocked?" surprises.

**Query:**
```sql
-- MySQL: OFF keeps locks alive across statements
SET autocommit = 0;                 -- or start a BEGIN
UPDATE accounts SET balance = 0 WHERE id = 1;
-- lock held...
COMMIT;
```
**Explanation:** Latent lock retention between statements is exactly what recommends turning autocommit OFF (or BEGIN) for multi-statement read-modify-write flows.

## Q86: Explain the transaction lifecycle for locks: BEGIN → work → COMMIT/ROLLBACK.
Locks accumulate during the transaction and are released only at the end; statement-level autocommit releases them per statement, while explicit transactions batch them.

**Query:**
```sql
-- SQL Server: explicit transaction lifecycle
BEGIN TRAN;
INSERT INTO orders (...) VALUES (...);          -- insert X-lock
UPDATE inventory SET qty = qty - 1 WHERE sku='A';  -- U→X upgrade lock
COMMIT TRAN;                                      -- every lock released here
-- ROLLBACK TRAN would undo everything and release too
```
**Explanation:** The longer the open transaction, the longer every lock it ever touched stays held — keep writes close to COMMIT and commit eagerly.

## Q87: Do nested transactions exist?
Emulated. Engines support `BEGIN ... COMMIT` nesting syntactically (SQL Server, MySQL), but internally there is a single transaction; `ROLLBACK` from any depth rolls back everything.

**Query:**
```sql
-- SQL Server: @@TRANCOUNT tracks nesting; inner savepoints are the real tool
BEGIN TRAN;            -- @@TRANCOUNT = 1
  BEGIN TRAN;          -- @@TRANCOUNT = 2   (no real second transaction)
COMMIT;                -- @@TRANCOUNT = 1
ROLLBACK;              -- rolls back BOTH levels at once
```
**Explanation:** There is exactly one transaction and one lock set; use SAVEPOINT (below) to create rollback subtrees inside that single transaction.

## Q88: What are savepoints and how do they help with locks?
Savepoints partition a single transaction: you can roll back to a marker, undoing only that patch of work, while locks acquired earlier stay intact until the real COMMIT/ROLLBACK.

**Query:**
```sql
-- PostgreSQL: retry a conflicting row inside a transaction via savepoint
BEGIN;
UPDATE accounts SET balance = balance - 10 WHERE id = 4;
SAVEPOINT attempt;
UPDATE accounts SET balance = balance - 10 WHERE id = 4
  AND balance >= 10;
ROLLBACK TO attempt;       -- undo only the failed attempt; outer work kept
COMMIT;
```
**Explanation:** Savepoints keep a long transaction alive after a sub-error, avoiding a full aborted transaction, though the held locks from before the savepoint remain.

## Q89: Map the four isolation levels to their locking behavior.
READ UNCOMMITTED locks nothing (dirty reads); READ COMMITTED locks only rows written, releasing read locks immediately; REPEATABLE READ (Postgres) adds blocking on modified rows and (MySQL) gap locks; SERIALIZABLE (SQL Server, MySQL) adds range/predicate locks or aborts conflicts (PG SSI).

**Query:**
```sql
-- SQL Server: serially-step down isolation for a long batch that must not block
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- better: replace sticky default with one-off NOLOCK where reporting tolerates it
SELECT * FROM analytics WITH (READUNCOMMITTED) WHERE region = 'us';
```
**Explanation:** Choosing the loosest level whose anomalies you accept is the real trade: durability of locks, work, and snapshot consistency all climb with the level.

## Q90: What is snapshot isolation and how do its locks differ?
Under snapshot isolation (Postgres REPEATABLE READ/SERIALIZABLE, SQL Server SNAPSHOT) reads take no locks at all and block for no writer; only writes lock rows, and conflicts surface as serialization failures.

**Query:**
```sql
-- SQL Server: enable and use SNAPSHOT isolation for read/write concurrency
ALTER DATABASE app SET ALLOW_SNAPSHOT_ISOLATION ON;
SET TRANSACTION ISOLATION LEVEL SNAPSHOT;
SELECT * FROM accounts WHERE id = 1;      -- lock-free consistent read
UPDATE accounts SET balance = balance - 5 WHERE id = 1;  -- only this blocks
```
**Explanation:** Readers never wait on writers; writers can still collide, detected at UPDATE commit as error 3960 — retry the write, not the read.

## Q91: What are DDL locks and why does ALTER TABLE block heavily?
DDL takes schema/metadata locks (SQL Server Sch-M, MySQL MDL) that exclude almost everything; any concurrent query on the table can block the ALTER and vice versa.

**Query:**
```sql
-- MySQL: invisible DDL gate — no online option by default
-- Standard: ALTER TABLE orders ADD COLUMN promo_code VARCHAR(32);
-- Rebuild: ALTER TABLE orders ADD COLUMN promo_code VARCHAR(32), ALGORITHM=INPLACE;
```
**Explanation:** While the metadata lock is held (or being requested), other queries/transactions touching orders wait; MySQL 8 online DDL with ALGORITHM=INPLACE and plugins (pt-osc, gh-ost) shrink that window.

## Q92: What are MySQL metadata locks (MDL)?
MySQL serializes DDL vs DML on a table with metadata locks: a long-running SELECT/transaction holds MDL now, blocking an ALTER; conversely an ALTER blocks new DML while switching tables.

**Query:**
```sql
-- MySQL: diagnose MDL waits
SELECT * FROM performance_schema.metadata_locks;
-- a transaction that opened an old statement keeps MDL → ALTER fails with
-- "Waiting for table metadata lock" / "Lock wait timeout exceeded"
```
**Explanation:** MDLs are per-table name-based locks with SHARED (queries), SHARED_WRITE (DML), and EXCLUSIVE (ALTER) modes — a forgotten open transaction is the classic MDL blocker.

## Q93: How do online DDL tools avoid taking exclusive locks?
They copy the table into a shadow with a trigger, flip traffic in micro-swaps, or use rapid row-copy + catch-up, holding only a brief moment of EXCLUSIVE MDL.

**Query:**
```sql
-- MySQL: gh-ost / pt-online-schema-change style command
-- gh-ost --alter="ADD COLUMN promo_code VARCHAR(32) NULL" --table=orders --execute
--   … copies rows in the background, then swaps at the end
```
**Explanation:** The switcheroo means no long Sch-M/EX; the brief final swap is a tiny exclusive window, so production writes keep flowing during the migration.

## Q94: How do you monitor lock waits in MySQL live?
Use performance_schema.data_lock_waits joined to sys.innodb_lock_waits and information_schema.INNODB_TRX for the blocking statement and the blocker's query.

**Query:**
```sql
-- MySQL: the whole picture in one query
SELECT trx.trx_id AS waiter,
       trx.trx_mysql_thread_id AS waiter_conn,
       CONNECTION_ID()                                  AS blocker_conn
  FROM sys.innodb_lock_waits;
-- piece together with information_schema.INNODB_TRX for SQL_TEXT on both sides
```
**Explanation:** sys.innodb_lock_waits (blocked <-> blocking ids + wait age) plus INNODB_TRX exposes the exact query; samples on a cron catch periodic lock storms before they page you.

**Alt1:**
```sql
-- MySQL: quickly increase wait timeout before hunting the culprit
SET GLOBAL innodb_lock_wait_timeout = 30;
SHOW STATUS LIKE 'Innodb_row_lock_current_waits';
```
**Explanation:** A status counter gives the aggregate wait count; keep reports enabled to alert when current_waits climbs above a threshold.

## Q95: What are SQL Server's sys.dm_os_waiting_tasks for lock waits, and the LATCH picture?
dm_os_waiting_tasks exposes wait_type — LCK_M_* are lock waits, LATCH_* are in-memory internal structure waits — with the waiting session and lock resource.

**Query:**
```sql
-- SQL Server: classify wait types
SELECT session_id, wait_type, wait_time_ms, blocking_session_id
  FROM sys.dm_os_waiting_tasks
 WHERE wait_type LIKE 'LCK%' OR wait_type LIKE 'LATCH%';
```
**Explanation:** LCK waits mean the app holds row locks (fix ordering/indexing/transactions); LATCH waits are short internal page-protection spins — signal of CPU-heavy buffered contention, not SQL logic.

## Q96: Lock vs latch: what is the difference?
Locks are logical, app-visible, transaction-managed protections (undo-able, held to commit); latches are low-level, microsecond CPU spin/mutexes guarding internal structures (buffer pages, index nodes) with no transaction semantics.

**Query:**
```sql
-- SQL Server: latch waits on shared pages are visible as LATCH_SH, not LCK
SELECT wait_type, wait_time_ms
  FROM sys.dm_os_wait_stats
 WHERE wait_type IN ('LATCH_EX','LATCH_SH','PAGEIOLATCH_SH')
 ORDER BY wait_time_ms DESC;
```
**Explanation:** A SQL query never "sees" latches; latches only show up in wait statistics as contention on shared pages — the DB's internal equivalent of parallelism bottlenecks.

## Q97: What is buffer-pool page latching in InnoDB?
Before touching a page in the buffer pool, a thread takes an S or X latch on that page frame for microseconds; long XOR holding turns into LOCK_WAIT and stall symptoms despite no row locks.

**Query:**
```sql
-- MySQL: observed as performance_schema wait events, not lock tables
SELECT * FROM performance_schema.events_waits_current
 WHERE event_name LIKE '%latch%' OR event_name LIKE '%io/table%';
```
**Explanation:** Two threads needing the same hot page serialize on its latch; if a thread holds it during a slow IO, everyone behind it stalls — page-latch churn, not deadlock.

## Q98: What happens to row locks at READ COMMITTED when the statement ends?
Under READ COMMITTED, most engines (SQL Server, MySQL RC, Oracle) release the read/update lock after each statement; only the transaction's own writes keep X locks until COMMIT/ROLLBACK.

**Query:**
```sql
-- SQL Server: at READ COMMITTED, locks released per-statement
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN TRAN;
UPDATE accounts SET balance = 0 WHERE id = 1;   -- X lock freed AFTER this line
-- rows the UPDATE touched are free again before later statements run
COMMIT;
```
**Explanation:** The contrast — READ COMMITTED frees locks between statements vs REPEATABLE READ holding to the end — directly changes how long readers take locks and hence blocking spans.

## Q99: Why ORDER BY before FOR UPDATE, and what can go wrong otherwise?
Because the engine applies FOR UPDATE as rows are scanned; without ordering, an index order can vary between plans (or between transactions), letting two workers lock row sets in opposite sequences.

**Query:**
```sql
-- PostgreSQL: iterate in a fixed key order to keep lock order stable
BEGIN;
SELECT * FROM orders
 WHERE status = 'pending'
 ORDER BY id
 FOR UPDATE;
 -- per-row processing...
COMMIT;
```
**Explanation:** Deterministic ordering turns a scan-based lock pattern into an ordered acquisition, which preserves 2PL and avoids the swapped-order deadlock class entirely.

## Q100: Design the locking for an inventory-deduct API (concurrency-safe).
Combine a unique-key locking read, SKIP LOCKED for claim-style work, and a guarded UPDATE with an atomic expression, all inside one short transaction with bounded retry.

**Query:**
```sql
-- PostgreSQL: deduction endpoint
BEGIN;
SELECT id, stock FROM inventory
 WHERE sku = 'SKU-123'
   FOR UPDATE;                          -- serialize writers on the row
UPDATE inventory
   SET stock   = stock - :qty,
       version = version + 1
 WHERE sku = 'SKU-123'
   AND stock >= :qty;                   -- atomic availability guard
-- rows_affected == 0 → 409 "insufficient stock", ROLLBACK
COMMIT;
-- deadlock/serialization error → retry ≤3 times with backoff
```
**Explanation:** FOR UPDATE serializes concurrent deductors, the guarded expression checks stock atomically with the decrement, and the short transaction minimizes the lock window.

**Alt1:**
```sql
-- MySQL 8: same pattern but reading claimed-appointment rows without waiting
SELECT * FROM inventory WHERE sku = 'SKU-123' FOR UPDATE NOWAIT;
-- 1205 → return 409 quickly instead of finishing inside a long wait
```
**Explanation:** NOWAIT turns "someone else is mid-deduct" into an immediate, well-defined error the API can surface — better UX than a 50-second black hole at scale.

