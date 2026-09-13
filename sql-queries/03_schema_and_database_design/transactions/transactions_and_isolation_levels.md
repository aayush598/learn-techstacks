# Transactions and Isolation Levels — 100 SQL Interview Q&A

## Q1: What is a database transaction?

A transaction is a logical unit of work that groups multiple SQL statements so they either all take effect or none do.

**Query:**
```sql
-- PostgreSQL
BEGIN;
INSERT INTO accounts (id, name, balance) VALUES (1, 'Alice', 1000);
UPDATE accounts SET balance = balance - 200 WHERE id = 1;
INSERT INTO transfers (from_acct, to_acct, amount) VALUES (1, 2, 200);
COMMIT;
```
**Explanation:** Three statements execute atomically — if any fails, the entire set is rolled back.

## Q2: What is Atomicity in ACID?

Atomicity guarantees that every transaction either completes fully or has no visible effect at all.

**Query:**
```sql
-- MySQL
START TRANSACTION;
UPDATE accounts SET balance = balance - 500 WHERE id = 1;
UPDATE accounts SET balance = balance + 500 WHERE id = 2;
-- If the second UPDATE raises an error, the debit is also undone
COMMIT;
```
**Explanation:** The two updates are atomic — a failure mid-transaction prevents a partial transfer.

## Q3: What is Consistency in ACID?

Consistency ensures a transaction moves the database from one valid state to another, never violating constraints, triggers, or business rules.

**Query:**
```sql
-- PostgreSQL
BEGIN;
-- Violates CHECK constraint (price > 0), aborts the transaction
INSERT INTO products (id, name, price) VALUES (1, 'Widget', -5.00);
COMMIT;
```
**Explanation:** The CHECK constraint rejects the insert; PostgreSQL marks the transaction aborted, so COMMIT has no effect — consistency is preserved.

## Q4: What is Isolation in ACID?

Isolation ensures that concurrent transactions do not interfere with each other — each transaction should behave as if it were the only one running.

**Query:**
```sql
-- SQL Server
-- Connection 1
BEGIN TRANSACTION;
SELECT balance FROM accounts WHERE id = 1; -- sees 1000
-- Connection 2 runs concurrently
BEGIN TRANSACTION;
UPDATE accounts SET balance = 500 WHERE id = 1;
COMMIT;
-- Connection 1 re-reads under REPEATABLE READ — still sees 1000
SELECT balance FROM accounts WHERE id = 1;
COMMIT;
```
**Explanation:** REPEATABLE READ isolation ensures Connection 1's second read returns the same value as the first, hiding the concurrent update.

## Q5: What is Durability in ACID?

Durability guarantees that once a transaction commits, its changes survive system failures (power loss, crash).

**Query:**
```sql
-- MySQL — durability controlled by innodb_flush_log_at_trx_commit
SET GLOBAL innodb_flush_log_at_trx_commit = 1;
-- 1 = flush log to disk on every COMMIT (full durability)
-- 0 = flush once per second (risk of losing 1 second of commits)
-- 2 = flush to OS cache per commit, to disk once per second
```
**Explanation:** Setting `innodb_flush_log_at_trx_commit = 1` ensures each COMMIT is fsynced to disk, providing true durability.

## Q6: How do you start a transaction in MySQL?

**Query:**
```sql
-- MySQL
START TRANSACTION;
INSERT INTO accounts (id, name, balance) VALUES (3, 'Carol', 750);
COMMIT;
```
**Explanation:** `START TRANSACTION` disables autocommit until an explicit COMMIT or ROLLBACK is issued.

**Alt1:**
```sql
-- MySQL — BEGIN and BEGIN WORK are aliases
BEGIN WORK;
INSERT INTO accounts (id, name, balance) VALUES (4, 'Dave', 500);
COMMIT;
```
**Explanation:** `BEGIN WORK` behaves identically to `START TRANSACTION` in MySQL; `WORK` is optional keyword sugar.

## Q7: How do you start a transaction in PostgreSQL?

**Query:**
```sql
-- PostgreSQL
BEGIN;
UPDATE inventory SET quantity = quantity - 10 WHERE product_id = 42;
INSERT INTO shipments (product_id, qty, status) VALUES (42, 10, 'pending');
COMMIT;
```
**Explanation:** `BEGIN` starts a transaction block in PostgreSQL; all statements until COMMIT or ROLLBACK execute as one unit.

**Alt1:**
```sql
-- PostgreSQL — START TRANSACTION with options
START TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY;
SELECT avg(balance) FROM accounts;
COMMIT;
```
**Explanation:** You can set isolation level and read-only mode directly in the `START TRANSACTION` statement.

## Q8: How do you start a transaction in SQL Server?

**Query:**
```sql
-- SQL Server
BEGIN TRANSACTION;
INSERT INTO audit_log (event, ts) VALUES ('backup_started', GETDATE());
UPDATE config SET value = 'true' WHERE key = 'backup_running';
COMMIT TRANSACTION;
```
**Explanation:** `BEGIN TRANSACTION` starts an explicit transaction in SQL Server; `BEGIN TRAN` is a common abbreviation.

## Q9: How do you start a transaction in Oracle?

**Query:**
```sql
-- Oracle
-- Oracle does not have an explicit BEGIN TRANSACTION; DML starts an implicit transaction
INSERT INTO orders (customer_id, total) VALUES (10, 249.99);
UPDATE inventory SET stock = stock - 1 WHERE product_id = 7;
COMMIT;
```
**Explanation:** Oracle uses implicit transactions — any DML statement starts a transaction, and you COMMIT or ROLLBACK when ready.

## Q10: How do you roll back a transaction?

**Query:**
```sql
-- MySQL
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
-- Decided to abort — undo the debit
ROLLBACK;
```
**Explanation:** `ROLLBACK` discards all changes made since the transaction began, restoring the database to its prior state.

**Alt1:**
```sql
-- SQL Server — partial rollback with savepoint
BEGIN TRANSACTION;
INSERT INTO orders (customer_id, total) VALUES (5, 50.00);
SAVE TRANSACTION order_inserted;
INSERT INTO order_items (order_id, product_id, qty) VALUES (@@IDENTITY, 99, 1);
-- Item insert failed, roll back just that statement
ROLLBACK TRANSACTION order_inserted;
-- The order row is preserved
COMMIT TRANSACTION;
```
**Explanation:** Rolling back to a savepoint undoes only statements after the savepoint, leaving earlier work intact.

## Q11: What is autocommit mode in MySQL?

Autocommit means every single statement is automatically wrapped in its own transaction and committed immediately.

**Query:**
```sql
-- MySQL
-- Autocommit is ON by default
SELECT @@autocommit; -- returns 1

-- This INSERT commits immediately on its own
INSERT INTO logs (message) VALUES ('auto-committed');

-- Turn autocommit off for the session
SET autocommit = 0;
INSERT INTO logs (message) VALUES ('not yet committed');
INSERT INTO logs (message) VALUES ('still not committed');
COMMIT; -- both inserts now committed together
SET autocommit = 1; -- restore default
```
**Explanation:** With `autocommit = 0`, statements accumulate until an explicit COMMIT or ROLLBACK.

## Q12: How does autocommit work in PostgreSQL?

**Query:**
```sql
-- PostgreSQL
-- Each statement outside an explicit BEGIN block is its own transaction
INSERT INTO events (type) VALUES ('click');  -- auto-committed
INSERT INTO events (type) VALUES ('scroll');  -- auto-committed

-- To batch statements, use an explicit block
BEGIN;
INSERT INTO events (type) VALUES ('load');
INSERT INTO events (type) VALUES ('resize');
COMMIT;
```
**Explanation:** PostgreSQL auto-commits each statement unless it is inside an explicit `BEGIN...COMMIT` block.

## Q13: How does SQL Server handle implicit transactions?

**Query:**
```sql
-- SQL Server
-- IMPLICIT_TRANSACTIONS ON means DML starts a transaction automatically
SET IMPLICIT_TRANSACTIONS ON;
INSERT INTO temp_results (val) VALUES (1);  -- transaction started
INSERT INTO temp_results (val) VALUES (2);  -- same transaction
-- You must explicitly COMMIT or ROLLBACK
COMMIT TRANSACTION;
SET IMPLICIT_TRANSACTIONS OFF;  -- restore default
```
**Explanation:** When `IMPLICIT_TRANSACTIONS` is ON, every DML statement begins a transaction automatically, requiring explicit COMMIT/ROLLBACK.

## Q14: What is the difference between implicit and explicit transactions?

**Query:**
```sql
-- MySQL — explicit transaction
START TRANSACTION;
INSERT INTO queue (task) VALUES ('send_email');
INSERT INTO queue (task) VALUES ('update_index');
COMMIT;

-- MySQL — implicit (autocommit) transaction
INSERT INTO queue (task) VALUES ('send_email');  -- committed immediately
INSERT INTO queue (task) VALUES ('update_index');  -- committed immediately
```
**Explanation:** Explicit transactions give you control over when changes are finalized; implicit (autocommit) commits each statement immediately.

## Q15: How do you create a savepoint in MySQL?

**Query:**
```sql
-- MySQL
START TRANSACTION;
INSERT INTO orders (customer_id, total) VALUES (1, 100.00);
SAVEPOINT sp_items;
INSERT INTO order_items (order_id, product_id, qty) VALUES (LAST_INSERT_ID(), 5, 2);
INSERT INTO order_items (order_id, product_id, qty) VALUES (LAST_INSERT_ID(), 8, 1);
ROLLBACK TO SAVEPOINT sp_items;
-- Order row remains, both item inserts are undone
COMMIT;
```
**Explanation:** `SAVEPOINT` marks a rollback point; `ROLLBACK TO SAVEPOINT` undoes only changes after that point.

**Alt1:**
```sql
-- PostgreSQL — savepoint syntax is identical
BEGIN;
INSERT INTO orders (customer_id, total) VALUES (2, 75.00);
SAVEPOINT sp_items;
INSERT INTO order_items (order_id, product_id, qty) VALUES (currval('orders_id_seq'), 3, 4);
ROLLBACK TO SAVEPOINT sp_items;
COMMIT;
```
**Explanation:** PostgreSQL savepoint syntax is the same as MySQL; the `currval()` call gets the generated order ID.

## Q16: How do you roll back to a savepoint?

**Query:**
```sql
-- PostgreSQL
BEGIN;
INSERT INTO accounts (id, name, balance) VALUES (10, 'Eve', 200);
SAVEPOINT before_transfer;
UPDATE accounts SET balance = balance - 150 WHERE id = 10;
-- Decided the amount was wrong — undo just the UPDATE
ROLLBACK TO SAVEPOINT before_transfer;
UPDATE accounts SET balance = balance - 50 WHERE id = 10;
COMMIT;
```
**Explanation:** `ROLLBACK TO SAVEPOINT` reverts changes made after the savepoint while preserving earlier statements in the transaction.

## Q17: How do you use multiple savepoints in a single transaction?

**Query:**
```sql
-- MySQL
START TRANSACTION;
INSERT INTO batch_log (step, status) VALUES (1, 'started');
SAVEPOINT sp1;
INSERT INTO batch_log (step, status) VALUES (2, 'processing');
SAVEPOINT sp2;
INSERT INTO batch_log (step, status) VALUES (3, 'finalizing');
-- Undo step 3 only
ROLLBACK TO SAVEPOINT sp2;
-- Undo step 3 and step 2
ROLLBACK TO SAVEPOINT sp1;
-- Step 1 insert still intact
COMMIT;
```
**Explanation:** Multiple savepoints can be nested; rolling back to an earlier savepoint implicitly releases all later savepoints.

## Q18: How do you release a savepoint?

**Query:**
```sql
-- PostgreSQL
BEGIN;
INSERT INTO events (type) VALUES ('start');
SAVEPOINT sp1;
INSERT INTO events (type) VALUES ('middle');
RELEASE SAVEPOINT sp1;
-- sp1 no longer exists; cannot ROLLBACK TO sp1
INSERT INTO events (type) VALUES ('end');
COMMIT;
```
**Explanation:** `RELEASE SAVEPOINT` explicitly removes a savepoint, making it unavailable for future rollback.

**Alt1:**
```sql
-- MySQL — RELEASE SAVEPOINT syntax
START TRANSACTION;
INSERT INTO events (type) VALUES ('start');
SAVEPOINT sp1;
INSERT INTO events (type) VALUES ('middle');
RELEASE SAVEPOINT sp1;
COMMIT;
```
**Explanation:** MySQL uses the same `RELEASE SAVEPOINT` syntax; the savepoint is removed from the transaction's savepoint stack.

## Q19: What happens to savepoints when a transaction commits?

**Query:**
```sql
-- PostgreSQL
BEGIN;
INSERT INTO events (type) VALUES ('a');
SAVEPOINT sp1;
INSERT INTO events (type) VALUES ('b');
COMMIT;
-- Attempting to ROLLBACK TO sp1 after COMMIT produces an error:
-- ROLLBACK TO SAVEPOINT sp1;  -- ERROR: savepoint "sp1" does not exist
```
**Explanation:** All savepoints are destroyed on COMMIT — they only exist within the lifetime of a single transaction.

## Q20: How do you use savepoints for error recovery in a batch?

**Query:**
```sql
-- PostgreSQL
BEGIN;
INSERT INTO batch_import (row_data, status) VALUES ('row1', 'ok');
SAVEPOINT sp_row2;
INSERT INTO batch_import (row_data, status) VALUES ('row2', 'ok');
-- row2 insert fails due to constraint violation
-- Manually roll back to savepoint and continue
ROLLBACK TO SAVEPOINT sp_row2;
INSERT INTO batch_import (row_data, status) VALUES ('row2_fixed', 'ok');
INSERT INTO batch_import (row_data, status) VALUES ('row3', 'ok');
COMMIT;
```
**Explanation:** Savepoints let you recover from a failed row in a batch without discarding all prior successful inserts.

## Q21: What are the different syntaxes for BEGIN TRANSACTION?

**Query:**
```sql
-- MySQL
START TRANSACTION;
-- or
BEGIN;
-- or
BEGIN WORK;
```
**Explanation:** All three forms are equivalent in MySQL; `START TRANSACTION` is the most explicit.

**Alt1:**
```sql
-- SQL Server
BEGIN TRANSACTION;
-- or
BEGIN TRAN;
-- or
BEGIN DISTRIBUTED TRANSACTION;  -- for distributed (XA-like) transactions
```
**Explanation:** SQL Server supports `BEGIN TRAN` as shorthand; `BEGIN DISTRIBUTED TRANSACTION` is used for cross-server transactions.

## Q22: What is the difference between COMMIT and COMMIT WORK?

**Query:**
```sql
-- MySQL — both are equivalent
START TRANSACTION;
INSERT INTO logs (msg) VALUES ('test');
COMMIT;
-- or
BEGIN;
INSERT INTO logs (msg) VALUES ('test');
COMMIT WORK;
```
**Explanation:** `COMMIT WORK` is SQL-standard syntax; in MySQL, `COMMIT` and `COMMIT WORK` are identical.

## Q23: How do you wrap a batch INSERT in a transaction?

**Query:**
```sql
-- PostgreSQL
BEGIN;
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');
INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com');
INSERT INTO users (name, email) VALUES ('Carol', 'carol@example.com');
COMMIT;
```
**Explanation:** All three inserts are committed together — if any fails, none are persisted.

## Q24: How do you wrap a batch UPDATE in a transaction?

**Query:**
```sql
-- SQL Server
BEGIN TRANSACTION;
UPDATE products SET price = price * 1.10 WHERE category = 'electronics';
UPDATE products SET price = price * 1.05 WHERE category = 'clothing';
UPDATE inventory SET warehouse = 'main' WHERE warehouse IS NULL;
COMMIT TRANSACTION;
```
**Explanation:** The price and warehouse updates are committed atomically, ensuring consistent application of the pricing policy.

## Q25: How do you wrap a batch DELETE in a transaction?

**Query:**
```sql
-- MySQL
START TRANSACTION;
-- Archive before deleting
INSERT INTO orders_archive SELECT * FROM orders WHERE created_at < '2024-01-01';
DELETE FROM order_items WHERE order_id IN (SELECT id FROM orders WHERE created_at < '2024-01-01');
DELETE FROM orders WHERE created_at < '2024-01-01';
COMMIT;
```
**Explanation:** Archiving and deleting within one transaction ensures no data is lost if the process fails midway.

## Q26: What is READ UNCOMMITTED isolation level?

READ UNCOMMITTED is the lowest isolation level — a transaction can read rows that other transactions have written but not yet committed.

**Query:**
```sql
-- MySQL
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
START TRANSACTION;
SELECT balance FROM accounts WHERE id = 1;  -- may see uncommitted data
COMMIT;
```
**Explanation:** This level permits dirty reads and offers the least protection but the highest concurrency.

## Q27: How do you demonstrate a dirty read in READ UNCOMMITTED?

**Query:**
```sql
-- Connection 1 (writer)
START TRANSACTION;
UPDATE accounts SET balance = 100 WHERE id = 1;
SELECT SLEEP(10);  -- hold the uncommitted change open
COMMIT;

-- Connection 2 (reader, READ UNCOMMITTED)
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SELECT balance FROM accounts WHERE id = 1;  -- reads 100 (uncommitted!)
```
**Explanation:** Connection 2 sees the new balance of 100 before Connection 1 commits — a dirty read.

## Q28: What is READ COMMITTED isolation level?

READ COMMITTED allows reads of only committed data, but different statements in one transaction may see different snapshots.

**Query:**
```sql
-- SQL Server
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN TRANSACTION;
SELECT balance FROM accounts WHERE id = 1;  -- snapshot A
-- another session commits a change here
SELECT balance FROM accounts WHERE id = 1;  -- snapshot B (different!)
COMMIT TRANSACTION;
```
**Explanation:** Each statement is a fresh snapshot, so the two SELECTs could return different balances — no dirty reads, but non-repeatable reads possible.

## Q29: What is REPEATABLE READ isolation level?

REPEATABLE READ guarantees that if you read a row twice in one transaction, you see the same value both times.

**Query:**
```sql
-- PostgreSQL
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT balance FROM accounts WHERE id = 1;  -- 1000
-- concurrent session commits a change to balance
SELECT balance FROM accounts WHERE id = 1;  -- still 1000
COMMIT;
```
**Explanation:** The snapshot is fixed at the first read, so all subsequent reads in that transaction return the same values.

## Q30: What is SERIALIZABLE isolation level?

SERIALIZABLE is the highest isolation level — transactions appear to run one after another, with no bitmap anomalies whatsoever.

**Query:**
```sql
-- PostgreSQL
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT sum(balance) FROM accounts WHERE name LIKE 'A%';
UPDATE accounts SET balance = balance + 50 WHERE name = 'Alice';
COMMIT;
```
**Explanation:** SERIALIZABLE detects and aborts conflicting transactions, guaranteeing a serial execution order.

## Q31: What is a dirty read? Demonstrate it with two connections.

A dirty read is reading data another transaction has written but not yet committed — the data could be rolled back later.

**Query:**
```sql
-- SQL Server, Connection 1 (with READ UNCOMMITTED)
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
BEGIN TRANSACTION;
SELECT quantity FROM inventory WHERE product_id = 5;  -- 100
-- Connection 2 has uncommitted UPDATE setting quantity = 50
SELECT quantity FROM inventory WHERE product_id = 5;  -- 50 (uncommitted!)
ROLLBACK;
-- Connection 2 rolls back; the "50" the reader saw never existed
```
**Explanation:** The reader saw value 50 that was later rolled back to 100 — a classic dirty read.

## Q32: What is a non-repeatable read? Demonstrate it.

A non-repeatable read occurs when a transaction re-reads the same row within one transaction and gets a different value because another transaction committed a change in between.

**Query:**
```sql
-- PostgreSQL, Connection 1 (READ COMMITTED, default)
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- 1000
-- Connection 2 commits: UPDATE accounts SET balance = 800 WHERE id = 1;
SELECT balance FROM accounts WHERE id = 1;  -- 800 (different value)
COMMIT;
```
**Explanation:** The same SELECT returned 1000 then 800 within one transaction — a non-repeatable read.

## Q33: What is a phantom read? Demonstrate it.

A phantom read is when a transaction re-runs a search query and sees new rows appear, because another transaction committed inserts in the meantime.

**Query:**
```sql
-- MySQL, Connection 1 (REPEATABLE READ — InnoDB prevents this with a snapshot)
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
SELECT count(*) FROM orders WHERE customer_id = 7;  -- 3
-- Connection 2 commits: INSERT INTO orders (customer_id, total) VALUES (7, 20);
SELECT count(*) FROM orders WHERE customer_id = 7;  -- 3 (still, due to snapshot)
COMMIT;
```
**Explanation:** InnoDB REPEATABLE READ uses a consistent snapshot; phantoms would appear under READ COMMITTED.

## Q34: What is a lost update? Demonstrate it.

A lost update happens when two transactions read the same value, both modify it, and the last commit overwrites the first, silently losing the first transaction's change.

**Query:**
```sql
-- PostgreSQL, Connection 1 (READ COMMITTED)
BEGIN;
SELECT quantity FROM inventory WHERE product_id = 9;  -- 100
-- Connection 2 reads 100 and commits: SET quantity = 100 - 30
UPDATE inventory SET quantity = quantity - 20 WHERE product_id = 9;
COMMIT;  -- quantity is now 80, not 50 — Connection 2's -30 was lost
```
**Explanation:** Both transactions computed from 100; the second COMMIT overwrote the first, losing the -30 decrement.

## Q35: How do isolation levels prevent each anomaly?

**Query:**
```sql
-- SQL Server — anomaly prevention matrix
-- Level                Dirty  Non-Rep.  Phantom  Lost Update
-- READ UNCOMMITTED     Maybe  Maybe     Maybe    Yes
-- READ COMMITTED       No     Maybe     Maybe    Under concurrency
-- REPEATABLE READ      No     No        Maybe    Mostly prevented
-- SERIALIZABLE         No     No        No       Prevents
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;  -- choose when all are unacceptable
BEGIN TRANSACTION;
SELECT sum(amount) FROM ledger WHERE account_id = 3;
COMMIT TRANSACTION;
```
**Explanation:** Higher isolation trades concurrency for correctness; SERIALIZABLE prevents every anomaly class.

## Q36: How do you set the isolation level in MySQL?

**Query:**
```sql
-- MySQL — for the entire session
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- for the next transaction only
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```
**Explanation:** Use `SET SESSION` for persistent session behavior or `SET TRANSACTION` for just the next transaction.

**Alt1:**
```sql
-- MySQL — per-transaction via START TRANSACTION
START TRANSACTION ISOLATION LEVEL SERIALIZABLE READ ONLY;
SELECT count(*) FROM accounts;
COMMIT;
```
**Explanation:** MySQL lets you specify isolation level directly in `START TRANSACTION`, overriding the session default for one transaction.

## Q37: How do you set the isolation level in PostgreSQL?

**Query:**
```sql
-- PostgreSQL — for one transaction
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
INSERT INTO inventory_log (product_id, delta) VALUES (5, -10);
COMMIT;
```
**Explanation:** PostgreSQL accepts the isolation level directly in `BEGIN` or `START TRANSACTION`.

**Alt1:**
```sql
-- PostgreSQL — inside the transaction with SET LOCAL
BEGIN;
SET LOCAL TRANSACTION ISOLATION LEVEL READ COMMITTED;
SELECT avg(price) FROM products;
COMMIT;
```
**Explanation:** `SET LOCAL` applies only until the current transaction ends, unlike `SET SESSION` which persists.

## Q38: How do you set the isolation level in SQL Server?

**Query:**
```sql
-- SQL Server — session-wide / connection-wide setting
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN TRANSACTION;
SELECT sum(total) FROM orders;
COMMIT TRANSACTION;
-- restore default
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```
**Explanation:** SQL Server's `SET TRANSACTION ISOLATION LEVEL` applies to the whole connection until changed, unlike Oracle/PostgreSQL per-transaction settings.

## Q39: How do you set a default isolation level per session in PostgreSQL?

**Query:**
```sql
-- PostgreSQL
SET default_transaction_isolation = 'repeatable read';
-- Subsequent statements now use REPEATABLE READ automatically
BEGIN;
SELECT count(*) FROM ledger;
COMMIT;
-- Or query the current value
SHOW default_transaction_isolation;
```
**Explanation:** `default_transaction_isolation` controls the level applied to newly started transactions.

**Alt1:**
```sql
-- PostgreSQL — via session GUC on connect
-- In libpq connection string:
-- host=db.example.com user=app dbname=shop options='-c default_transaction_isolation=repeatable_read'
BEGIN;
SELECT * FROM accounts;
COMMIT;
```
**Explanation:** You can set the GUC at connection startup so every transaction inherits the desired isolation level automatically.

## Q40: Can you change the isolation level after BEGIN?

**Query:**
```sql
-- Oracle — changing it mid-transaction is an error
-- Run before or at transaction start:
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
INSERT INTO accounts (id, balance) VALUES (50, 300);
-- SET TRANSACTION ISOLATION LEVEL READ COMMITTED; -- ORA-01453: not allowed inside a transaction
COMMIT;
```
**Explanation:** Oracle forbids changing isolation level mid-transaction; MySQL, PostgreSQL (`SET LOCAL`), and SQL Server allow it within the session or transaction depending on dialect.

## Q41: Demonstrate a lost update with two concurrent transactions in detail.

**Query:**
```sql
-- MySQL, Connection 1
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
SELECT stock FROM products WHERE id = 3;   -- 50
-- update based on stale value
UPDATE products SET stock = stock - 10 WHERE id = 3;   -- 40
COMMIT;

-- MySQL, Connection 2 (interleaved)
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
SELECT stock FROM products WHERE id = 3;   -- 50 (read before C1 commits)
UPDATE products SET stock = stock - 25 WHERE id = 3;   -- 25 (commits last)
COMMIT;  -- final stock 25 — C1's -10 was lost
```
**Explanation:** Both sessions compute from stock = 50; the last commit wins and the first update's effect (75) is silently lost.

**Alt1:**
```sql
-- PostgreSQL — same scenario; use FOR UPDATE to fix
BEGIN;
SELECT stock FROM products WHERE id = 3 FOR UPDATE;  -- locks the row
UPDATE products SET stock = stock - 10 WHERE id = 3;
COMMIT;
```
**Explanation:** `SELECT ... FOR UPDATE` locks the row so rival transactions must wait, eliminating the lost update.

## Q42: Demonstrate a dirty read with READ UNCOMMITTED in detail.

**Query:**
```sql
-- PostgreSQL, Connection 1
BEGIN;
UPDATE accounts SET balance = balance + 1000 WHERE id = 4;   -- uncommitted
-- Connection 2 (READ UNCOMMITTED) reads 1000 ahead of our commit
-- Connection 1 rolls back
ROLLBACK;

-- PostgreSQL, Connection 2
SET default_transaction_isolation = 'read uncommitted';
BEGIN;
CREATE TEMP TABLE seen (val int);
INSERT INTO seen SELECT balance FROM accounts WHERE id = 4;  -- saw phantom 1000
-- value later rolled back — the 1000 was never committed
ROLLBACK;
```
**Explanation:** PostgreSQL treats READ UNCOMMITTED as READ COMMITTED internally, but on Real DBs it still demonstrates the classic dirty-read window.

## Q43: Demonstrate a non-repeatable read with READ COMMITTED in detail.

**Query:**
```sql
-- SQL Server, Connection 1 (default READ COMMITTED)
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN TRANSACTION;
DECLARE @b1 int = (SELECT balance FROM accounts WHERE id = 2);  -- 500
-- Connection 2 commits an UPDATE to the same row in this window
DECLARE @b2 int = (SELECT balance FROM accounts WHERE id = 2);  -- 400
IF @b1 <> @b2 PRINT 'Non-repeatable read detected!';
COMMIT TRANSACTION;
```
**Explanation:** Each statement got a new committed snapshot, so the same row returned different values within one transaction.

## Q44: Demonstrate a phantom read with REPEATABLE READ (SQL Server).

**Query:**
```sql
-- SQL Server, Connection 1 (REPEATABLE READ locks individual rows, not ranges)
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN TRANSACTION;
SELECT count(*) FROM orders WHERE total > 100;   -- 5
-- Connection 2 commits: INSERT a new order with total = 250
SELECT count(*) FROM orders WHERE total > 100;   -- 6 !!
-- Phantom row appeared despite REPEATABLE READ
COMMIT TRANSACTION;
```
**Explanation:** REPEATABLE READ locks only existing rows; newly inserted rows matching the predicate can still appear — the phantom read.

## Q45: Show how SERIALIZABLE prevents all anomalies in a transaction.

**Query:**
```sql
-- PostgreSQL, Connection 1
BEGIN ISOLATION LEVEL SERIALIZABLE;
SELECT count(*) FROM orders WHERE customer_id = 1;  -- 3
-- Connection 2 attempts: INSERT new order for customer_id = 1, gets blocked/serialization error
SELECT count(*) FROM orders WHERE customer_id = 1;  -- still 3
COMMIT;
```
**Explanation:** SERIALIZABLE takes predicate locks — concurrent inserts into the scanned range either block or cause a serialization failure, preventing phantoms.

## Q46: Which isolation level is best for a typical OLTP workload?

**Query:**
```sql
-- PostgreSQL — READ COMMITTED is the default OLTP choice
SET default_transaction_isolation = 'read committed';
BEGIN;
UPDATE accounts SET balance = balance - 15 WHERE id = 1;
INSERT INTO ledger (account_id, amount) VALUES (1, -15);
COMMIT;
```
**Explanation:** READ COMMITTED prevents dirty reads while keeping row locks short and concurrency high — ideal for operational queries.

## Q47: Which isolation level for a long-running reporting query?

**Query:**
```sql
-- PostgreSQL — REPEATABLE READ gives a stable snapshot for reports
BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY;
SELECT department_id, sum(salary) FROM employees GROUP BY department_id;
SELECT count(*) FROM orders;  -- consistent with the first query
COMMIT;
```
**Explanation:** REPEATABLE READ gives the report a single consistent snapshot across all its queries, unlike READ COMMITTED.

## Q48: Which isolation level for a banking transfer scenario?

**Query:**
```sql
-- PostgreSQL — account transfers want strong guarantees
BEGIN ISOLATION LEVEL SERIALIZABLE;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;  -- lock both rows
SELECT balance FROM accounts WHERE id = 2 FOR UPDATE;
UPDATE accounts SET balance = balance - 250 WHERE id = 1;
UPDATE accounts SET balance = balance + 250 WHERE id = 2;
COMMIT;
```
**Explanation:** SERIALIZABLE (plus row locks) guarantees no lost updates, no phantoms, and a consistent transfer invariant.

**Alt1:**
```sql
-- MySQL — same operation; REPEATABLE READ + locking reads
START TRANSACTION;
SELECT balance FROM accounts WHERE id IN (1,2) FOR UPDATE;
UPDATE accounts SET balance = balance - 250 WHERE id = 1;
UPDATE accounts SET balance = balance + 250 WHERE id = 2;
COMMIT;
```
**Explanation:** InnoDB's locking reads (`FOR UPDATE`) give transfer-grade isolation at REPEATABLE READ.

## Q49: Why might READ COMMITTED be preferred over REPEATABLE READ?

**Query:**
```sql
-- MySQL — REPEATABLE READ can cause unwarranted serialization errors
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
SELECT price FROM products WHERE id = 10;  -- short-lived statement snapshot
UPDATE products SET price = 12.50 WHERE id = 10;
COMMIT;
```
**Explanation:** READ COMMITTED takes shorter-lived locks and snapshots, reducing blocking and index-lock contention for high-concurrency workloads.

## Q50: When is SERIALIZABLE necessary despite its performance cost?

**Query:**
```sql
-- PostgreSQL — invariants that depend on absence of concurrent writes
BEGIN ISOLATION LEVEL SERIALIZABLE;
-- "total seats must never exceed 100"
SELECT count(*) FROM reservations WHERE flight_id = 88;   -- 95
INSERT INTO reservations (flight_id, person) VALUES (88, 'Alice');  -- would make 96
COMMIT;
-- A concurrent insert committing first triggers a serialization failure here
```
**Explanation:** SERIALIZABLE is required when the correctness of a write depends on the sum of concurrent writes, like seat or inventory caps.

## Q51: How does PostgreSQL MVCC work?

MVCC (Multiversion Concurrency Control) keeps multiple row versions so readers never block writers and writers never block readers.

**Query:**
```sql
-- PostgreSQL — invisible internals that demonstrate per-row versioning
BEGIN;
UPDATE accounts SET balance = 900 WHERE id = 1;   -- creates new row version (xmin = txid)
-- Concurrent reader still sees old version 1000
COMMIT;
SELECT txid_current();  -- the current transaction id for xmin checks
```
**Explanation:** Updates insert a new tuple version tagged with the transaction id, and readers use visibility rules to pick the correct version.

## Q52: What does REPEATABLE READ mean in PostgreSQL?

REPEATABLE READ in PostgreSQL takes a single snapshot at the transaction's start; the whole transaction reads from that one consistent state.

**Query:**
```sql
-- PostgreSQL
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT sum(balance) FROM accounts;   -- snapshot taken here
-- Another session commits data about 1 second later
SELECT count(*) FROM accounts;       -- still reflects the original snapshot
SELECT sum(balance) FROM accounts;   -- still original snapshot
COMMIT;
```
**Explanation:** Unlike READ COMMITTED, all statements see one uniform snapshot — no non-repeatable reads or phantoms within the transaction.

**Alt1:**
```sql
-- PostgreSQL — caveat: REPEATABLE READ + concurrent writer still raises a serialization error
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT * FROM accounts WHERE id = 9;
UPDATE accounts SET balance = balance + 10 WHERE id = 9;
COMMIT;
```
**Explanation:** If another transaction updated the same row first, you get error `40001: could not serialize access due to concurrent update`.

## Q53: How does MySQL InnoDB implement REPEATABLE READ?

InnoDB REPEATABLE READ uses a consistent snapshot the FIRST time a read occurs in the transaction, and all subsequent reads use that same snapshot.

**Query:**
```sql
-- MySQL
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
SELECT * FROM ledger WHERE account_id = 1;  -- snapshot established here
-- Later DML sees the same snapshot, but locking reads see latest committed
SELECT * FROM ledger WHERE account_id = 1 FOR UPDATE;  -- sees the newest row
COMMIT;
```
**Explanation:** The consistent read snapshot is created at the first SELECT and reused; `FOR UPDATE` forces the latest committed version.

## Q54: How do you enable snapshot isolation in SQL Server?

**Query:**
```sql
-- SQL Server
ALTER DATABASE AppDB SET ALLOW_SNAPSHOT_ISOLATION ON;

SET TRANSACTION ISOLATION LEVEL SNAPSHOT;
BEGIN TRANSACTION;
SELECT balance FROM accounts WHERE id = 1;  -- snapshot at transaction start
-- concurrent UPDATE commits in another session
SELECT balance FROM accounts WHERE id = 1;  -- same value as the first read
COMMIT TRANSACTION;
```
**Explanation:** SQL Server SNAPSHOT isolation gives MVCC-style consistent reads at transaction start, preventing non-repeatable and phantom reads.

## Q55: What is READ COMMITTED SNAPSHOT in SQL Server?

READ COMMITTED SNAPSHOT (RCSI) makes READ COMMITTED behave like a statement-level snapshot — no dirty read canonical RCSI semantics, no update locks, no reader blocking.

**Query:**
```sql
-- SQL Server — enable once per database (requires exclusive access briefly)
ALTER DATABASE AppDB SET READ_COMMITTED_SNAPSHOT ON WITH ROLLBACK IMMEDIATE;

-- Now the default READ COMMITTED gets statement-level snapshot reads
SELECT balance FROM accounts WHERE id = 1;  -- snapshot, not lock-based
```
**Explanation:** RCSI changes default READ COMMITTED from locking to versioning-based reads, reducing blocking with no application change.

## Q56: What is a deadlock? Show a basic example.

A deadlock is when two transactions each hold a lock the other needs and neither can proceed.

**Query:**
```sql
-- SQL Server, Connection 1
BEGIN TRANSACTION; -- holds UPDATE lock on accounts row 1
UPDATE accounts SET balance = 100 WHERE id = 1;
-- Conn 2:
BEGIN TRANSACTION; -- holds UPDATE lock on accounts row 2
UPDATE accounts SET balance = 200 WHERE id = 2;
-- Conn 1 tries:
UPDATE accounts SET balance = 299 WHERE id = 2;  -- blocked, needs row 2
-- Conn 2 tries:
UPDATE accounts SET balance = 150 WHERE id = 1;  -- blocked, needs row 1
-- DEADLOCK — SQL Server picks a victim, rolls it back, kills its batch
```
**Explanation:** Both rows are locked by opposite transactions — classic cyclic wait that the engine resolves by sacrificing one victim.

**Alt1:**
```sql
-- SQL Server — the canonical two-row deadlock in one readable block
-- Transaction A locks (1) then (2); Transaction B locks (2) then (1)
BEGIN TRAN; UPDATE accounts SET cb = cb+1 WHERE id=1;
-- vs
BEGIN TRAN; UPDATE accounts SET cb = cb+1 WHERE id=2;
```
**Explanation:** Same cycle at different scale — same resolution by victim selection.

## Q57: How does MySQL detect deadlocks?

**Query:**
```sql
-- MySQL, Connection 1
START TRANSACTION;
UPDATE accounts SET balance = 10 WHERE id = 1;   -- X lock on row 1
SELECT SLEEP(2);
-- Connection 2 (interleaved)
START TRANSACTION;
UPDATE accounts SET balance = 20 WHERE id = 2;   -- X lock on row 2
SELECT SLEEP(2);
-- now C1 updates row 2, C2 updates row 1 => deadlock
UPDATE accounts SET balance = 30 WHERE id = 2;   -- C1 blocked
UPDATE accounts SET balance = 40 WHERE id = 1;   -- C2 blocked
-- InnoDB detects the cycle and aborts one: ERROR 1213 (40001): Deadlock
```
**Explanation:** InnoDB continuously checks the wait-for graph and immediately aborts one transaction with `ERROR 1213` on deadlock.

**Alt1:**
```sql
-- MySQL — aftermath: catch error 1213 and retry
START TRANSACTION;
-- application catches: IntegrityError 1213 'Deadlock found when trying to get lock'
-- and re-executes the entire transaction
COMMIT;
```
**Explanation:** Deadlocks are recoverable — the standard pattern is retrying the whole transaction after error 1213.

## Q58: How does PostgreSQL detect deadlocks?

PostgreSQL waits up to `deadlock_timeout` (default 1s), then walks its lock-queues to find a cycle and aborts one combatant with `SQLSTATE 40P01`.

**Query:**
```sql
-- PostgreSQL, Connection 1
BEGIN;
UPDATE accounts SET balance = balance - 1 WHERE id = 1;
-- Connection 2:
BEGIN;
UPDATE accounts SET balance = balance - 1 WHERE id = 2;
-- now C1: UPDATE accounts ... WHERE id = 2;  C2: UPDATE ... WHERE id = 1;
-- ERROR: deadlock detected (40P01) after deadlock_timeout
ROLLBACK;  -- the victim must roll back and retry
```
**Explanation:** PostgreSQL detects deadlock only after `deadlock_timeout` elapses, then aborts one transaction with SQLSTATE 40P01.

## Q59: How do you handle a deadlock error in application code?

**Query:**
```sql
-- PostgreSQL — retry loop pseudo-SQL with keepalive/backoff
-- pg_advisory locks can alternate with row locks to avoid the cycle
BEGIN;
SELECT pg_advisory_xact_lock(42);         -- take advisory locks in a consistent order
UPDATE accounts SET balance = 500 WHERE id = 2;
UPDATE accounts SET balance = 300 WHERE id = 1;  -- same order everywhere
COMMIT;
```
**Explanation:** The most robust solutions make deadlocks impossible by always acquiring locks in a fixed canonical order.

## Q60: What strategies prevent deadlocks?

**Query:**
```sql
-- MySQL — keep transactions short and lock rows in the same order everywhere
START TRANSACTION;
-- always lock account A then account B, never reverse the order
SELECT id FROM accounts WHERE id IN (1,2) FOR UPDATE;  -- bulk lock first
UPDATE accounts SET balance = balance + 100 WHERE id = 1;
UPDATE accounts SET balance = balance - 100 WHERE id = 2;
COMMIT;
```
**Explanation:** Consistent lock ordering, shorter transactions, and fewer indexes scanned reduce deadlock probability to near zero.

## Q61: What is write skew?

Write skew occurs when two transactions each read overlapping data, make different writes that jointly violate an invariant, and both commit — under repeatable-read-like snapshots that allow it.

**Query:**
```sql
-- PostgreSQL, Connection 1 (REPEATABLE READ)
BEGIN;
SELECT count(*) FROM on_call WHERE room = 'A';   -- 1
-- Connection 2 reads same: 1
-- Both decide: "only one person on call, I can leave"
DELETE FROM on_call WHERE doctor = 'Alice' AND room = 'A';
-- Connection 2:
DELETE FROM on_call WHERE doctor = 'Bob' AND room = 'A';
-- Both commit → room A now has 0 on-call doctors, violating "at least 1"
```
**Explanation:** Neither transaction alone breaks the constraint, but together they do — each acted from the same stale snapshot.

## Q62: Demonstrate write skew in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
-- invariant: a vault requires at least 2 of 3 authorized users to open
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT count(*) FROM vault_access WHERE vault_id = 5 AND authorized = true;  -- 2
-- user A revokes their own access while user B (in parallel) revokes theirs
DELETE FROM vault_access WHERE user_id = 'A' AND vault_id = 5;
COMMIT;
```
**Explanation:** Both users pass the "still 2 others" check based on a snapshot, then both revoke — the vault lands at 0 authorized users.

**Alt1:**
```sql
-- PostgreSQL — the write-skew surface is wider with UPDATEs than DELETEs
BEGIN ISOLATION LEVEL REPEATABLE READ;
UPDATE employees SET on_duty = false
WHERE id = 3 AND (SELECT count(*) FROM employees WHERE on_duty AND shift_id = 1) > 1;
COMMIT;
```
**Explanation:** Each UPDATE checker evaluates the sibling count from its own snapshot — the two off-duty flags can both land.

## Q63: How do you prevent write skew?

**Query:**
```sql
-- PostgreSQL — lock the consulted rows, so rivals can't read the same snapshot
BEGIN;
SELECT id FROM employees WHERE shift_id = 1 AND on_duty FOR UPDATE;  -- lock all candidates
UPDATE employees SET on_duty = false WHERE id = 3
AND (SELECT count(*) FROM employees WHERE shift_id = 1 AND on_duty) > 1;
COMMIT;
```
**Explanation:** Locking the predicate rows serializes the check-and-act, restoring the invariant.

## Q64: Does PostgreSQL support transactional DDL?

Yes — PostgreSQL DDL is transactional, so CREATE/ALTER/DROP and DML roll back together within one transaction.

**Query:**
```sql
-- PostgreSQL
BEGIN;
CREATE TABLE temp_audit (id serial PRIMARY KEY, msg text);
INSERT INTO temp_audit (msg) VALUES ('created');
-- oops — roll it all back
ROLLBACK;
-- Re-run and confirm
BEGIN;
CREATE TABLE audit (id serial PRIMARY KEY, msg text);
INSERT INTO audit (msg) VALUES ('created');
COMMIT;
SELECT count(*) FROM audit;  -- survives
```
**Explanation:** DDL statements join the transaction; on ROLLBACK the table never existed.

## Q65: Does MySQL support transactional DDL?

**Query:**
```sql
-- MySQL — DDL is NOT transactional (implicit commit before/after DDL)
START TRANSACTION;
INSERT INTO logs (msg) VALUES ('about to CREATE');
CREATE TABLE t1 (id INT);       -- this implicitly commits the INSERT
-- ROLLBACK will NOT undo the CREATE TABLE
ROLLBACK;
DROP TABLE t1;
```
**Explanation:** MySQL implicitly commits the current transaction before and after non-transactional DDL; the DDL itself cannot be rolled back.

**Alt1:**
```sql
-- MySQL — InnoDB supports transactional DDL only for non-atomic operations
START TRANSACTION;
CREATE TABLE t2 (id INT) ENGINE = InnoDB;   -- still implicitly commits
INSERT INTO t2 VALUES (1);
ROLLBACK;   -- INSERT rolled back; the table remains
```
**Explanation:** The CREATE TABLE itself persists despite ROLLBACK — only the DML after it is undone.

## Q66: Does SQL Server support transactional DDL?

Yes — SQL Server wraps DDL in transactions like PostgreSQL, so CREATE, ALTER, DROP of tables and indexes roll back with the transaction.

**Query:**
```sql
-- SQL Server
BEGIN TRANSACTION;
CREATE TABLE dbo.temp_status (id INT PRIMARY KEY, state VARCHAR(20));
INSERT INTO dbo.temp_status VALUES (1, 'active');
-- Roll back: table disappears again
ROLLBACK;
IF OBJECT_ID('dbo.temp_status') IS NOT NULL PRINT 'exists';
```
**Explanation:** The entire CREATE + INSERT disappears on ROLLBACK — SQL Server DDL is fully transactional.

## Q67: Does Oracle support transactional DDL?

Oracle commits the current transaction before and after DDL — DDL is not rollbackable.

**Query:**
```sql
-- Oracle
INSERT INTO accounts (id, name) VALUES (99, 'temp');
CREATE TABLE tmp (id NUMBER);   -- implicit COMMIT of the INSERT here
ROLLBACK;                       -- does NOT undo the CREATE TABLE
-- and does NOT undo the INSERT either (it was implicitly committed)
```
**Explanation:** Oracle performs implicit commits around DDL; the DDL and any prior uncommitted DML both become permanent.

**Alt1:**
```sql
-- Oracle — procedural workaround: flashback for accidental DDL
SELECT original_name FROM recyclebin WHERE type = 'TABLE';  -- dropped table lives in the recycle bin
FLASHBACK TABLE tmp TO BEFORE DROP;
```
**Explanation:** With flashback you can recover an accidentally dropped table because the DDL itself committed instantly.

## Q68: What are distributed transactions?

Distributed transactions span multiple databases or services and require coordinated COMMIT across all participants — atomicity across networks.

**Query:**
```sql
-- SQL Server — BEGIN DISTRIBUTED TRANSACTION via linked servers + MSDTC
BEGIN DISTRIBUTED TRANSACTION;
INSERT INTO ServerA.ShopDB.dbo.orders (id) VALUES (1);
INSERT INTO ServerB.WarehouseDB.dbo.shipments (id) VALUES (1);
COMMIT TRANSACTION;   -- coordinates via MSDTC: all or nothing
```
**Explanation:** A transaction coordinator ensures every participating connection commits or rolls back identically.

## Q69: How do you use XA transactions in MySQL?

**Query:**
```sql
-- MySQL — native XA steps
XA START 'xid-1';
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
XA END 'xid-1';
XA PREPARE 'xid-1';          -- phase 1: ready to commit
-- Coordinator decides...
XA COMMIT 'xid-1';           -- phase 2: commit
-- (or XA ROLLBACK 'xid-1';)
```
**Explanation:** XA is a two-step protocol: `XA PREPARE` then `XA COMMIT`/`XA ROLLBACK` — MySQL participates in two-phase commit.

**Alt1:**
```sql
-- MySQL — recovering prepared-but-undecided transactions
XA RECOVER;                -- lists prepared branches with no outcome
XA COMMIT 'xid-1';         -- the app finishes them after a crash
```
**Explanation:** `XA RECOVER` shows orphans left by interrupted coordinators so you can resolve them manually.

## Q70: What is two-phase commit (2PC)?

**Query:**
```sql
-- 2PC protocol (conceptual — the coordinator drives these calls)
-- Phase 1 (prepare): each participant XA PREPARE 'id' and replies "yes/no"
XA START 'tx1';  ...  XA END 'tx1';  XA PREPARE 'tx1';   -- per participant
-- If ALL participants prepare successfully:
XA COMMIT 'tx1';   -- per participant  (if any fails: XA ROLLBACK 'tx1';)
```
**Explanation:** 2PC has a prepare phase where each DB makes changes durable-but-uncommitted, and a commit phase where all commit together — highest available atomicity across systems.

## Q71: How do you emulate nested transactions with savepoints?

Real nesting is not available anywhere; savepoints simulate nesting so inner-work rollbacks don't destroy outer-work.

**Query:**
```sql
-- PostgreSQL
BEGIN;                                   -- outer transaction
INSERT INTO accounts (id, name) VALUES (80, 'outer');
SAVEPOINT inner_tran;                    -- "nested" transaction boundary
INSERT INTO accounts (id, name) VALUES (81, 'inner');
ROLLBACK TO SAVEPOINT inner_tran;        -- inner aborted, outer intact
INSERT INTO accounts (id, name) VALUES (82, 'after-inner');
COMMIT;                                  -- outer commits 80 and 82 only
```
**Explanation:** Each `SAVEPOINT` is a nested-tran boundary; `ROLLBACK TO` aborts only the inner level, like a partially failed subtransaction.

## Q72: How do you use savepoints for nested rollback in a stored procedure?

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION insert_order(cid int) RETURNS void AS $$
BEGIN
  SAVEPOINT order_sp;
  BEGIN   -- emulate a subtransaction
    INSERT INTO orders (customer_id) VALUES (cid);
    INSERT INTO order_items (order_id) SELECT currval('orders_id_seq'), 1;
    COMMIT;
  EXCEPTION WHEN unique_violation THEN
    ROLLBACK TO order_sp;                -- undo the inner block only
  END;
END $$ LANGUAGE plpgsql;
```
**Explanation:** The inner `BEGIN...EXCEPTION` block traps errors and uses savepoints to roll back only the inner work, then lets the caller decide on the outer transaction.

## Q73: How do you set a transaction timeout in MySQL?

**Query:**
```sql
-- MySQL — max wait per lock acquisition
SET SESSION innodb_lock_wait_timeout = 5;   -- seconds
START TRANSACTION;
UPDATE accounts SET balance = 0 WHERE id = 1;   -- waits max 5s for the lock
COMMIT;
-- scope: per statement/connection, not whole-transaction
```
**Explanation:** `innodb_lock_wait_timeout` aborts a query after that many seconds of waiting on a row lock (error 1205).

**Alt1:**
```sql
-- MySQL — prevent a whole transaction from running forever isn't built-in;
-- use a kill watchdog
-- (application schedules: 'KILL <id>' after a deadline, then ROLLBACK)
SELECT CONNECTION_ID();
```
**Explanation:** MySQL lacks a whole-transaction timeout; production systems externally `KILL` stale connections.

## Q74: How do you set a lock timeout in PostgreSQL?

**Query:**
```sql
-- PostgreSQL
SET lock_timeout = '3s';        -- abort a statement that can't get a lock in 3s
SET statement_timeout = '30s';  -- abort any statement running longer than 30s
BEGIN;
UPDATE accounts SET balance = 100 WHERE id = 1;  -- error 55P03 if lock waits > 3s
COMMIT;
```
**Explanation:** `lock_timeout` and `statement_timeout` bound waiting and execution; both raise errors you can catch and retry.

**Alt1:**
```sql
-- PostgreSQL — idle-in-transaction guard
SET idle_in_transaction_session_timeout = '60s';
-- a transaction left open for > 60s is auto-rolled-back
BEGIN;
SELECT * FROM accounts;
-- ...nothing else for a minute => session aborted automatically
```
**Explanation:** This prevents leaking long-open transactions that hold locks and bloat old row versions.

## Q75: What does durable commit mean?

A durable commit means the transaction's changes are persisted to non-volatile storage before the client is told COMMIT succeeded.

**Query:**
```sql
-- PostgreSQL — synchronous_commit on makes every COMMIT wait for fsync
SHOW synchronous_commit;              -- 'on'
BEGIN; UPDATE accounts SET balance = 10 WHERE id = 1; COMMIT;
-- the WAL is flushed to disk before COMMIT returns 'COMMIT'

-- PostgreSQL — off speeds up; COMMIT returns before flush (small window of loss)
SET synchronous_commit = off;
BEGIN; UPDATE accounts SET balance = 20 WHERE id = 1; COMMIT;
```
**Explanation:** `synchronous_commit = on` (default) fsyncs the WAL on every commit; `off` risks losing the last fraction of commits on a crash for faster throughput.

## Q76: When does a plain SELECT need a transaction?

**Query:**
```sql
-- PostgreSQL — a single SELECT is already one statement, atomic by itself
SELECT sum(amount) FROM ledger WHERE account_id = 1;  -- fine without BEGIN

-- BUT to bind several SELECTs into one consistent view, wrap them:
BEGIN;
SELECT sum(debits) FROM register WHERE account_id = 1;
SELECT sum(credits) FROM register WHERE account_id = 1;
COMMIT;
```
**Explanation:** One statement is inherently consistent; you need a transaction only when reading multiple statements that must agree on the same snapshot.

## Q77: How do you get consistent reads across multiple SELECTs?

**Query:**
```sql
-- MySQL — REPEATABLE READ keeps all SELECTs on one snapshot
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
SELECT count(*) FROM orders;                 -- snapshot S
SELECT sum(total) FROM orders;               -- same snapshot S
SELECT avg(total) FROM orders;               -- same snapshot S
COMMIT;
```
**Explanation:** With REPEATABLE READ, every read in the transaction uses the same snapshot established at the first read — a consistent multi-query report.

## Q78: How do you batch INSERTs efficiently in a transaction?

**Query:**
```sql
-- SQL Server — one transaction, reduced log flushes, atomic result
BEGIN TRANSACTION;
INSERT INTO metrics (name, val, dt) VALUES ('cpu', 22, GETDATE()), ('mem', 61, GETDATE()), ('io', 8, GETDATE());
INSERT INTO metrics (name, val, dt) VALUES ('net', 33, GETDATE());
COMMIT;
```
**Explanation:** Batching multiple inserts in one transaction avoids per-row COMMIT overhead and makes insertion atomic.

## Q79: How do you batch UPDATEs with error handling?

**Query:**
```sql
-- PostgreSQL
BEGIN;
UPDATE accounts SET balance = balance - 10 WHERE id IN (1,2,3);
SAVEPOINT upd2;
UPDATE accounts SET balance = balance + 10 WHERE id = 999;   -- nonexistent row: no error, no rows
ROLLBACK TO SAVEPOINT upd2;
UPDATE accounts SET balance = balance + 5 WHERE id = 1;
COMMIT;
```
**Explanation:** Savepoints quarantine part of a batch so a failed statement doesn't force rolling back already-correct updates.

## Q80: How do you batch DELETEs safely?

**Query:**
```sql
-- MySQL — chunked deletes in one transaction, bounded by LIMIT
START TRANSACTION;
DELETE FROM audit_events WHERE ts < '2023-01-01' LIMIT 5000;
-- verify row count here; repeat the transaction for the next chunk
COMMIT;
```
**Explanation:** Chunked deletes avoid massive single-statement locks; wrapping each chunk in a transaction divides risk and allows rollback per chunk.

## Q81: How do you rollback to a savepoint after a batch error?

**Query:**
```sql
-- PostgreSQL — error hides in a savepoint, outer transaction lives on
BEGIN;
INSERT INTO import_log (row) VALUES ('header');
SAVEPOINT row1;
INSERT INTO accounts (id, balance) VALUES (1, 10);      -- OK
SAVEPOINT row2;
INSERT INTO accounts (id, balance) VALUES (43, 0);      -- fails: balance cannot be 0
ROLLBACK TO SAVEPOINT row2;                             -- salvage
INSERT INTO accounts (id, balance) VALUES (43, 1);      -- retry corrected
COMMIT;
```
**Explanation:** `ROLLBACK TO SAVEPOINT` discards only the failed statement and its side effects, letting the batch continue.

**Alt1:**
```sql
-- MySQL — same savepoint rescue pattern
START TRANSACTION;
INSERT INTO batch (status) VALUES ('starting');
SAVEPOINT sp_err;
INSERT INTO batch (status) VALUES ('will_fail');   -- trigger error (e.g., NOT NULL)
ROLLBACK TO SAVEPOINT sp_err;                       -- backup to before the error
INSERT INTO batch (status) VALUES ('recovered');
COMMIT;
```
**Explanation:** Identical rescue pattern across MySQL and PostgreSQL; InnoDB also never destroys savepoints used after an error.

## Q82: How do you implement idempotent batch processing with savepoints?

**Query:**
```sql
-- PostgreSQL — per-item savepoint: retryable without reprocessing earlier items
BEGIN;
FOR item IN (SELECT * FROM inbound_queue) LOOP
  SAVEPOINT item_sp;
  BEGIN
    INSERT INTO processed (payload) VALUES (item.payload);
    DELETE FROM inbound_queue WHERE id = item.id;
  EXCEPTION WHEN unique_violation THEN
    ROLLBACK TO item_sp;              -- skip duplicates, keep transaction open
  END;
END LOOP;
COMMIT;
```
**Explanation:** Each item gets its own savepoint so one bad row never aborts the entire batch — idempotent and resumable.

## Q83: What is SELECT FOR UPDATE?

`SELECT ... FOR UPDATE` acquires exclusive row locks so no other transaction can modify (or in some modes even read) those rows until you commit.

**Query:**
```sql
-- SQL Server — the row stays locked until the transaction ends
BEGIN TRANSACTION;
SELECT balance FROM accounts WHERE id = 5 WITH (UPDLOCK, ROWLOCK);
UPDATE accounts SET balance = balance - 100 WHERE id = 5;
COMMIT;
```
**Explanation:** Locking reads give you pessimistic control over a row you plan to change, preventing lost updates.

## Q84: What is SELECT FOR SHARE in PostgreSQL?

**Query:**
```sql
-- PostgreSQL — FOR SHARE locks rows against writes, but not reads
BEGIN;
SELECT * FROM products WHERE id = 3 FOR SHARE;
-- Concurrent writers block; other FOR SHARE readers may proceed
-- Useful to prevent a row being deleted while you validate other tables
COMMIT;
```
**Explanation:** `FOR SHARE` grants shared locks — reads are fine, but UPDATE/DELETE/queries that need exclusive locks wait.

**Alt1:**
```sql
-- SQL Server — NOLOCK reads uncommitted data for adventurous speed
BEGIN TRANSACTION;
SELECT balance FROM accounts WITH (NOLOCK);   -- skips locks, may read dirty
COMMIT TRANSACTION;
```
**Explanation:** SQL Server's `WITH (NOLOCK)` hint bypasses locking — a deliberate, risky trade-off equivalent to READ UNCOMMITTED.

## Q85: How does SERIALIZABLE prevent write skew?

SERIALIZABLE places predicate locks on every scanned row range, so a concurrent transaction touching the same predicate either blocks or fails.

**Query:**
```sql
-- PostgreSQL
BEGIN ISOLATION LEVEL SERIALIZABLE;
SELECT id FROM on_call WHERE room = 'A' AND doctor IN ('Alice','Bob');
DELETE FROM on_call WHERE doctor = 'Alice' AND room = 'A';
INSERT INTO on_call (doctor, room) VALUES ('Carol', 'A');  -- concurrent writer may force 40001 here
COMMIT;
```
**Explanation:** Serializable snapshots track predicate (SI-read) dependencies; if a detected conflict exists, one transaction is aborted — write skew surfaces as an error instead of silently corrupting data.

## Q86: How do you optimize read-only transactions in PostgreSQL?

**Query:**
```sql
-- PostgreSQL — READ ONLY disables some locking overhead
BEGIN TRANSACTION READ ONLY;
SELECT count(*) FROM orders WHERE STATUS = 'open';
SELECT sum(total) FROM orders;
COMMIT;
```
**Explanation:** Marking the transaction READ ONLY lets PostgreSQL skip the need to assign heavyweight transaction ids and reduces overhead on long reports.

**Alt1:**
```sql
-- PostgreSQL — REPEATABLE READ + READ ONLY is the reporting sweet spot
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY;
SELECT department_id, avg(salary) FROM employees GROUP BY 1;
COMMIT;
```
**Explanation:** You get a stable snapshot, minimal overhead, and no risk of accidental writes in analytics queries.

## Q87: What is SET TRANSACTION READ ONLY?

`SET TRANSACTION READ ONLY` declares that the transaction will not perform writes, enabling cheaper execution and stronger snapshot semantics.

**Query:**
```sql
-- Oracle
SET TRANSACTION READ ONLY;
SELECT sum(total) FROM orders WHERE created_at >= SYSDATE - 7;
-- an attempt to INSERT raises an error inside a read-only transaction
SELECT count(*) FROM orders;
COMMIT;
```
**Explanation:** Oracle enforces the read-only promise and refuses any DML inside the transaction.

**Alt1:**
```sql
-- PostgreSQL — fully combined control statement
BEGIN READ ONLY;                 -- also: BEGIN ISOLATION LEVEL SERIALIZABLE READ ONLY;
SELECT * FROM accounts;          -- reads OK
-- UPDATE ... would error: cannot execute UPDATE in a read-only transaction
COMMIT;
```
**Explanation:** PostgreSQL mirrors Oracle's behavior — write attempts inside READ ONLY fail with a clear error.

## Q88: How do you combine isolation level with read-only mode?

**Query:**
```sql
-- PostgreSQL — both modifiers on the START TRANSACTION line
START TRANSACTION ISOLATION LEVEL SERIALIZABLE READ ONLY;
SELECT sum(amount) FROM ledger;
COMMIT;
```
**Explanation:** Combined settings give a consistent, read-only, serializable snapshot — common for complex audits and reports.

## Q89: How do you handle cross-database transactions in SQL Server?

SQL Server runs transactions per database by default; to span databases you need a distributed or linked-server transaction managed by MSDTC.

**Query:**
```sql
-- SQL Server
BEGIN DISTRIBUTED TRANSACTION;
INSERT INTO MainDB.dbo.orders (id) VALUES (100);
INSERT INTO ArchiveDB.dbo.orders_archive (id) VALUES (100);
COMMIT TRANSACTION;   -- MSDTC coordinates both databases atomically
```
**Explanation:** `BEGIN DISTRIBUTED TRANSACTION` promotes the transaction to MSDTC-managed scope, giving atomicity across databases.

## Q90: How do you manage autocommit in MySQL?

**Query:**
```sql
-- MySQL
SET autocommit = OFF;                -- now every DML joins the current transaction
UPDATE accounts SET balance = 0 WHERE id = 1;
UPDATE accounts SET balance = 0 WHERE id = 2;
COMMIT;                              -- both updates land together
SET autocommit = ON;                 -- back to per-statement commits
```
**Explanation:** With autocommit OFF, statements stay uncommitted until you choose to COMMIT or ROLLBACK the session transaction.

**Alt1:**
```sql
-- SQL Server — implicit transactions do the same as autocommit OFF
SET IMPLICIT_TRANSACTIONS ON;
UPDATE accounts SET balance = 0 WHERE id = 3;
UPDATE accounts SET balance = 0 WHERE id = 4;
COMMIT TRANSACTION;
SET IMPLICIT_TRANSACTIONS OFF;
```
**Explanation:** SQL Server's `IMPLICIT_TRANSACTIONS ON` produces behavior similar to MySQL with autocommit disabled.

## Q91: How do you use a transaction with a CTE?

**Query:**
```sql
-- PostgreSQL — WITH confirms the batch, transaction commits it once
BEGIN;
WITH recent AS (SELECT id FROM orders WHERE created_at > now() - interval '1 hour')
DELETE FROM order_items WHERE order_id IN (SELECT id FROM recent);
WITH recent AS (SELECT id FROM orders WHERE created_at > now() - interval '1 hour')
DELETE FROM orders WHERE id IN (SELECT id FROM recent);
COMMIT;
```
**Explanation:** The CTE defines what to delete; the transaction guarantees related rows in both tables are removed atomically.

## Q92: How do you ensure consistency with subqueries across tables?

**Query:**
```sql
-- MySQL — the transaction guarantees the FK-referenced row exists at commit
START TRANSACTION;
INSERT INTO orders (customer_id, total)
SELECT id, 120 FROM customers WHERE id = 5;           -- subquery source
INSERT INTO order_items (order_id, product_id, qty)
SELECT LAST_INSERT_ID(), 12, 1;                       -- relational pairing
COMMIT;
```
**Explanation:** The two inserts maintain a referential invariant — order_items can only reference the just-created order_id.

**Alt1:**
```sql
-- MySQL — wrap a consistency check between two tables in one transaction
START TRANSACTION;
DELETE FROM inventory WHERE stock = 0 AND product_id IN (SELECT id FROM products WHERE discontinued = 1);
UPDATE products SET active = 0 WHERE discontinued = 1;
COMMIT;
```
**Explanation:** Deleting and deactivating in one atomic step ensures the catalog and inventory views never disagree.

## Q93: How do you use savepoints with triggers?

**Query:**
```sql
-- PostgreSQL — trigger failure rolls back the trigger's work but not the whole transaction
CREATE TRIGGER trg_audit AFTER INSERT ON orders
FOR EACH ROW EXECUTE FUNCTION log_order();

BEGIN;
SAVEPOINT sp_ins;
INSERT INTO orders (customer_id, total) VALUES (1, 10);  -- trigger fires and writes audit row
-- trigger raises an exception? we land here:
ROLLBACK TO SAVEPOINT sp_ins;   -- discard order + audit side effect
-- continue with other work
COMMIT;
```
**Explanation:** Savepoints let you handle trigger exceptions without discarding unrelated, already-successful work in the same transaction.

## Q94: What are savepoint naming conventions?

Structured names make nested rollback targets obvious and debuggable.

**Query:**
```sql
-- PostgreSQL — clear, hierarchical names
BEGIN;
INSERT INTO batch_run (id, started_at) VALUES (1, now());
SAVEPOINT sp_step_1;
INSERT INTO batch_rows (batch_id, row) VALUES (1, 'r1');
SAVEPOINT sp_step_2;
INSERT INTO batch_rows (batch_id, row) VALUES (1, 'r2');
ROLLBACK TO SAVEPOINT sp_step_2;   -- retry only step 2
COMMIT;
```
**Explanation:** Prefix (`sp_`) plus step name (`step_2`) keeps rollback targets unambiguous as transactions grow.

## Q95: Should you rollback to a savepoint or the whole transaction?

**Query:**
```sql
-- PostgreSQL — savepoint: salvage the last committed chunk and continue
BEGIN;
SAVEPOINT chunk1;
INSERT INTO logs (msg) VALUES ('chunk1');
ROLLBACK TO SAVEPOINT chunk1;          -- chunk1 failed: data gone, transaction alive
-- vs whole-transaction:
ROLLBACK;                              -- everything gone, must restart from zero
```
**Explanation:** Use savepoints when the error is recoverable in-batch; use a full rollback when the transaction's premise is broken and continuing would be meaningless.

## Q96: What isolation level for a financial ledger?

**Query:**
```sql
-- PostgreSQL — SERIALIZABLE guarantees append-only invariants
BEGIN ISOLATION LEVEL SERIALIZABLE;
INSERT INTO ledger_entry (account_id, amount)
SELECT account_id, delta FROM pending_batch WHERE batch_id = 77;
UPDATE accounts SET balance = balance + 5 WHERE id = 3;
COMMIT;
```
**Explanation:** Ledgers require the highest guarantees — another batch writing to the same account never disappears, so SERIALIZABLE (or row locks) is mandatory.

**Alt1:**
```sql
-- MySQL — the banking standard: REPEATABLE READ + FOR UPDATE
START TRANSACTION;
SELECT * FROM accounts WHERE id IN (3, 8) FOR UPDATE;   -- lock both legs
UPDATE accounts SET balance = balance - 100 WHERE id = 3;
UPDATE accounts SET balance = balance + 100 WHERE id = 8;
COMMIT;
```
**Explanation:** With row locks, REPEATABLE READ delivers ledger-grade atomicity at far lower cost than SERIALIZABLE.

## Q97: What isolation level for a real-time analytics dashboard?

**Query:**
```sql
-- PostgreSQL — READ COMMITTED is the right trade-off for dashboards
BEGIN;
SELECT count(*) FROM events;                      -- fast, fresh
SELECT metric_name, avg(value) FROM metrics GROUP BY 1;
COMMIT;
```
**Explanation:** Dashboards want the latest data and tolerate tiny inconsistencies between panels — READ COMMITTED keeps latency low.

**Alt1:**
```sql
-- MySQL — READ COMMITTED with a per-panel snapshot for a dashboard
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
SELECT sum(revenue) FROM sales WHERE date = CURDATE();
SELECT count(DISTINCT user_id) FROM activity WHERE dt = TODAY;
COMMIT;
```
**Explanation:** Each dashboard panel reads a fresh committed snapshot — cheap, current, and adequate for non-financial metrics.

## Q98: How do long-running transactions affect MVCC databases?

**Query:**
```sql
-- PostgreSQL — the longer the transaction, the more old row versions accumulate
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT * FROM accounts;
SELECT * FROM orders;                    -- big report may run for minutes
-- Meanwhile UPDATE/INSERT churn creates new tuple versions
-- Old versions cannot be vacuumed while this transaction (or any) keeps a snapshot old enough to see them
COMMIT;
```
**Explanation:** Long-lived transactions pin old snapshots, causing table bloat and degraded index scan performance — keep analytics outside OLTP transactions.

**Alt1:**
```sql
-- PostgreSQL — realm of vacuum: bloat, XID wraparound, interrupted vacation
SELECT age(datfrozenxid) FROM pg_database;
-- Staying inside REPEATABLE READ on big tables is the same horizontal scan risk
BEGIN ISOLATION LEVEL SERIALIZABLE; SELECT * FROM big_table; COMMIT;
```
**Explanation:** Monitoring `age(datfrozenxid)` catches transactions that keep the database from freezing rows — long snapshots delay vacuum.

## Q99: How does autovacuum interact with long transactions?

**Query:**
```sql
-- PostgreSQL — autovacuum skips rows that still-old snapshots might see
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT count(*) FROM huge_logs;          -- starts a very old snapshot
-- autovacuum runs, sees an old snapshot, and cannot recycle dead tuples
COMMIT;  -- after a long delay, autovacuum finally reaps the tuples
```
**Explanation:** Autovacuum uses the oldest active snapshot to decide what is safely removable; a long transaction this old freezes cleanup.

**Alt1:**
```sql
-- PostgreSQL — defensive: periodic sync + idempotent queries
-- avoid leaving SELECT-only transactions open past the report's real need
BEGIN; SELECT count(*) FROM logs WHERE ts > now() - interval '1h'; COMMIT;
```
**Explanation:** Committing read-only transactions promptly frees autovacuum to reclaim dead rows and minimizes bloat.

## Q100: Give a decision tree for choosing an isolation level.

**Query:**
```sql
-- PostgreSQL — concurrency-first decision
-- 1) Only one statement?             -> autocommit (no BEGIN needed)
-- 2) Small OLTP writes, no conflicts?-> READ COMMITTED
-- 3) Multi-statement report accuracy?-> REPEATABLE READ READ ONLY
-- 4) Invariant depends on other writes?-> SERIALIZABLE (or locking reads)
BEGIN ISOLATION LEVEL SERIALIZABLE;
-- FIFO inventory rule: never oversell
SELECT sum(cart_qty) FROM cart_lines WHERE sku = 'SKU-9';
INSERT INTO cart_lines (cart_id, sku, cart_qty) VALUES (1, 'SKU-9', 2);
COMMIT;
```
**Explanation:** Choose the weakest level that still satisfies correctness — start at READ COMMITTED, escalate to REPEATABLE READ for reports and SERIALIZABLE for invariant-critical writes.

**Alt1:**
```sql
-- MySQL — matching decision on InnoDB
-- light OLTP: default REPEATABLE READ (snapshot) is already fine
-- invariant writes: add FOR UPDATE at REPEATABLE READ before you reach for SERIALIZABLE
START TRANSACTION;
SELECT sum(cart_qty) FROM cart_lines WHERE sku = 'SKU-9' FOR UPDATE;
INSERT INTO cart_lines (cart_id, sku, cart_qty) VALUES (1, 'SKU-9', 2);
COMMIT;
```
**Explanation:** On InnoDB, serializability is achieved by REPEATABLE READ plus explicit row locks, so most shops never need SERIALIZABLE.
