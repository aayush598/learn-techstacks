# DDL, DML, DCL, and Constraints in SQL

> **TL;DR**: Real production SQL splits into four families — DDL (structure: CREATE/ALTER/DROP), DML (data: INSERT/UPDATE/DELETE/MERGE), DCL (privileges: GRANT/REVOKE), TCL (transactions: BEGIN/COMMIT/ROLLBACK) — with constraints declared inline so the engine enforces data rules for every writer.

## 1. Why Does This Exist?
Part 01 introduced the four SQL families conceptually; this section makes them *executable* — the exact statements, syntax, and pitfalls you type in production. It exists because interviewers (and jobs) test *syntax and behavior*: "write a CREATE TABLE with a FK and CHECK", "update a column and explain what happens to the index", "write an upsert". Knowing the verbs cold — including which are DDL (schema, DBA-gated, sometimes non-transactional) vs DML (data, transactional), and how constraints are declared — is the difference between describing SQL and *doing* SQL. The families exist so privileges, locking, and undo rules can differ per operation type.

## 2. How Does It Work?
**DDL**: `CREATE TABLE/INDEX/VIEW`, `ALTER TABLE ... ADD/DROP/ALTER COLUMN`, `DROP`, `TRUNCATE`, `RENAME` — modify the catalog; in Postgres they're transactional, in MySQL they auto-commit.
**DML**: `INSERT INTO ... VALUES/SELECT`, `UPDATE ... SET ... WHERE`, `DELETE FROM ... WHERE`, `MERGE`/upsert — modify rows under transaction control, update indexes, fire triggers.
**DCL**: `GRANT priv ON obj TO role`, `REVOKE ...` — write privilege rows enforced per statement.
**TCL**: `BEGIN`, `COMMIT`, `ROLLBACK`, `SAVEPOINT`, `SET TRANSACTION`.
**Constraints** (in DDL): `NOT NULL`, `UNIQUE`, `PRIMARY KEY`, `FOREIGN KEY ... REFERENCES ... ON DELETE ...`, `CHECK (...)` — declared at column or table level, stored in catalog, enforced on every DML write.

## 3. When Is It Used?
- **Every migration** is DDL orchestration: Flyway/Liquibase/Prisma run `CREATE/ALTER TABLE` scripts.
- **Every app write** is DML: ORMs generate INSERT/UPDATE/DELETE; bulk loads use INSERT...SELECT or COPY.
- **Every access change** is DCL: onboarding analysts (`GRANT SELECT`), removing access (`REVOKE`).
- **Every multi-step operation** needs TCL: order+inventory, transfer, batch load wrapped in BEGIN/COMMIT.
- **Constraints** are declared at schema creation to protect every subsequent write — the "spell-checker" of data quality.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: no DDL/DML distinction (one permission for everything).** Rejected: you couldn't give "edit data but not structure" to analysts; the split enables least-privilege (Part 01 §03).
- **Alternative: mutate schema by editing catalog rows directly.** Rejected: DDL is the *safe* interface — it validates, builds indexes, takes correct locks, and is transactional where supported. Hand-editing the catalog corrupts the DB.
- **Alternative: only `INSERT`, force updates via delete+insert.** Rejected: `UPDATE` is atomic (row locks, one statement, no delete/insert window) and preserves unchanged columns; DELETE+INSERT breaks FKs and is slower.
- **Alternative: `TRUNCATE` everything instead of `DELETE`.** Rejected: TRUNCATE is non-undoable and skips triggers — reserved for whole-table wipes, not targeted deletes.
- **Why constraints in DDL, not app code?** Because only the engine can enforce them atomically for *all* writers (Part 02 §03) — declaring them at schema time makes them part of the schema's contract.

## 5. Intuition
Think of the four families as four **employee badges** in a company. DDL = the **construction team**: they draw and change the building plans (tables) — blueprints, rare, tightly controlled. DML = the **daily staff**: they move inventory and edit records every hour — routine, granular, transactional. DCL = the **security team**: they issue and revoke access badges. TCL = the **shift supervisor**: "this shift's whole ledger is one batch — if any entry fails, tear up the whole batch." Constraints are the **building code**: the moment anyone tries to store a room without a door or a negative inventory count, the building system refuses. Each badge lets its holder do one kind of work — never someone else's.

## 6. Real-World Analogy
A **hotel booking system**: DDL = the manager reconfiguring room types (add a suite, rename a floor) — done by authorized staff in maintenance windows. DML = front-desk clerks booking/canceling rooms daily. DCL = IT deciding which staff may see guest credit cards. TCL = the night audit: "tonight's 200 bookings are one batch — if any fails to post, roll back the batch." Constraints = the rule "a room can't have double bookings" (UNIQUE on (room,date)) and "a booking must reference a real room" (FK) — enforced by the system regardless of which clerk is typing. The four badges keep housekeeping, booking, access, and auditing cleanly separated.

## 7. Formal Definition
- **DDL**: statements defining/modifying schema objects: `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME`, `COMMENT`. Effects are catalog changes.
- **DML**: statements accessing/modifying data: `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `SELECT` (read), `VALUES`, `TABLE`.
- **DCL**: `GRANT`, `REVOKE` (and SQL Server `DENY`) — access-control statements.
- **TCL**: `START TRANSACTION`/`BEGIN`, `COMMIT`, `ROLLBACK`, `SAVEPOINT`, `SET TRANSACTION`/`SET SESSION CHARACTERISTICS`.
- **Constraint declarations**: `{NOT NULL | UNIQUE | PRIMARY KEY | FOREIGN KEY(col) REFERENCES t(col) [ON DELETE {RESTRICT|CASCADE|SET NULL|SET DEFAULT} | ON UPDATE ...] | CHECK (predicate)}` at column or table level.
(ISO/IEC 9075; PostgreSQL and MySQL docs.)

## 8. Example
```sql
-- DDL with inline constraints
CREATE TABLE customers (
  id         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email      TEXT UNIQUE NOT NULL,
  balance    NUMERIC NOT NULL DEFAULT 0 CHECK (balance >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE orders (
  order_id    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
  total       NUMERIC NOT NULL CHECK (total > 0),
  status      TEXT NOT NULL DEFAULT 'pending'
               CHECK (status IN ('pending','paid','shipped','cancelled'))
);
-- ALTER: add / drop columns & constraints
ALTER TABLE orders ADD COLUMN shipped_at TIMESTAMPTZ;
ALTER TABLE orders ALTER COLUMN status SET DEFAULT 'pending';
ALTER TABLE customers ADD CONSTRAINT balance_nonneg CHECK (balance >= 0);
-- DML
INSERT INTO customers (email, balance) VALUES ('a@x', 100);
UPDATE customers SET balance = balance - 30 WHERE email = 'a@x';
DELETE FROM customers WHERE balance = 0;
-- Upsert (Postgres)
INSERT INTO customers (email, balance) VALUES ('b@x', 50)
ON CONFLICT (email) DO UPDATE SET balance = customers.balance + 50;
-- DCL
GRANT SELECT ON customers TO analyst;
REVOKE UPDATE ON customers FROM analyst;
-- TCL
BEGIN;
  UPDATE customers SET balance = balance - 100 WHERE id = 1;
  INSERT INTO orders (customer_id, total) VALUES (1, 100);
COMMIT;
```
All violation attempts (duplicate email, negative balance, FK to missing customer) are rejected by the engine.

## 9. Internal Working
1. **DDL** → catalog manager: validate → insert catalog rows → create supporting objects (PK/UNIQUE → unique index) → allocate storage. Postgres: transactional (rolls back); MySQL: implicit commit per statement.
2. **DML** → query processor + transaction manager: `INSERT` (heap append + index updates + FK probe), `UPDATE` (find rows via scan/index, lock them, write new versions — MVCC), `DELETE` (mark/remove, cascade/set-null via FK). Indexes updated in the same transaction.
3. **Upsert** (`ON CONFLICT`): attempts INSERT; on unique-violation, executes the DO UPDATE branch atomically — the unique index is both the conflict detector and the lock holder.
4. **DCL** → authorization manager: GRANT/REVOKE update privilege rows (e.g., `pg_class.relacl`); enforcement is per-statement on every later query.
5. **TCL** → transaction manager: BEGIN opens snapshot/locks; COMMIT fsyncs WAL + releases locks; ROLLBACK undoes via WAL/undo; SAVEPOINT marks a rollback point.

## 10. Time Complexity
- **INSERT**: heap append O(1) + index maintenance O(log n) per index (+ FK probes O(log m)).
- **UPDATE/DELETE**: locate O(log n) (indexed) or O(n) (scan); MVCC new-tuple O(1) + index updates O(log n) per index.
- **TRUNCATE**: O(1) amortized (deallocate pages; reset metadata) vs DELETE O(n).
- **ALTER ADD COLUMN (nullable)**: O(1) metadata-only (Postgres 11+, MySQL 8.0+ instant); with DEFAULT/rewrite O(n).
- **CREATE INDEX**: O(n log n) build; may block (use CONCURRENTLY).
- **GRANT/REVOKE**: O(1) catalog update; check O(1) cached.
- **COMMIT**: O(WAL fsync) ≈ disk latency.

## 11. Advantages
- **Safety by construction**: DDL validates + builds indexes; constraints enforced for all writers.
- **Atomic data ops**: single-statement UPDATE/DELETE with locking and MVCC — no read-modify-write races.
- **Least privilege**: GRANT/REVOKE per object per role; auditors can review.
- **Upserts**: one atomic insert-or-update (no SELECT-then-INSERT race).
- **Transactional DDL** (Postgres/Oracle/SQL Server): migrations can roll back cleanly.
- **Standardized verbs**: the same DDL/DML/DCL/TCL works across Postgres/MySQL/Oracle/SQL Server.

## 12. Disadvantages
- **DDL locking/blocking**: ALTER on big tables can block or rewrite (Postgres SHARE locks; MySQL table rebuilds) — needs careful scheduling.
- **Non-transactional DDL in MySQL**: a failed multi-DDL script leaves partial schema — no rollback.
- **Index write overhead**: each index doubles write cost on INSERT/UPDATE — many indexes = slower writes.
- **Upsert complexity**: `ON CONFLICT` vs `ON DUPLICATE KEY UPDATE` vs `MERGE` differ across engines; concurrency edge cases exist.
- **GRANT complexity**: role hierarchies, `WITH GRANT OPTION`, and revoke semantics can surprise; audit drift is real.

## 13. Interview Questions
1. **Q: Write a CREATE TABLE for orders with a FK, a CHECK, and a DEFAULT.** A: `CREATE TABLE orders (order_id BIGINT PRIMARY KEY, customer_id BIGINT NOT NULL REFERENCES customers(id) ON DELETE CASCADE, total NUMERIC CHECK (total > 0), status TEXT DEFAULT 'pending' CHECK (status IN ('pending','paid')));`
2. **Q: DDL vs DML — give 3 commands each.** A: DDL: CREATE, ALTER, DROP, TRUNCATE, RENAME. DML: INSERT, UPDATE, DELETE, MERGE, SELECT. (DCL: GRANT/REVOKE; TCL: BEGIN/COMMIT/ROLLBACK/SAVEPOINT.)
3. **Q: How do you add a NOT NULL column to an existing table with rows?** A: `ALTER TABLE t ADD COLUMN c TEXT NOT NULL DEFAULT 'x';` — engines backfill (may rewrite; Postgres 11+ does metadata-only if default is constant, applying it logically). Adding without DEFAULT to a non-empty table fails (can't satisfy NOT NULL).
4. **Q (tricky): `TRUNCATE` vs `DELETE` — which can you roll back?** A: DELETE is transactional (rollback-able, fires triggers, WHERE-able). TRUNCATE in Postgres *is* transactional but not per-row undoable and skips triggers; in MySQL it's implicit commit. For targeted rows, always DELETE.
5. **Q: What does `INSERT ... ON CONFLICT DO UPDATE` do?** A: Postgres upsert: try INSERT; if a UNIQUE/PK constraint is violated, execute the `DO UPDATE` branch instead — atomically. Conflicts are identified by the specific unique index you name (`ON CONFLICT (email)` or `ON CONFLICT ON CONSTRAINT`).
6. **Q: Write an upsert for MySQL.** A: `INSERT INTO customers (email, balance) VALUES ('a@x', 50) ON DUPLICATE KEY UPDATE balance = balance + 50;` (MySQL's version — keyed by any unique index automatically).
7. **Q: What's the difference between `DELETE` and `DROP TABLE`?** A: DELETE removes rows (data), keeps the table structure; DROP removes the whole table (structure + data + constraints + indexes). DELETE can be partial (WHERE); DROP is all-or-nothing.
8. **Q (scenario): An UPDATE sets `status='paid'` on 1M rows but must not block the app.** A: Batch it: `UPDATE ... WHERE status='pending' AND id IN (SELECT id ... ORDER BY id LIMIT 10000) RETURNING ...` loop until done — each batch is small, respects MVCC, avoids one giant lock/hold. Never one giant UPDATE on a hot table.
9. **Q: How does UPDATE interact with indexes?** A: Each changed index key is updated in the same transaction (delete old entry + insert new); with MVCC the old tuple version remains until vacuumed. An UPDATE on a key column = delete+insert in the index. More indexes = slower UPDATEs.
10. **Q: What is `GENERATED ALWAYS AS IDENTITY`?** A: The modern standard auto-increment (Postgres/Oracle/SQL Server); `SERIAL`/`AUTO_INCREMENT` are legacy alternatives. It prevents manual overriding; gives surrogate PKs without natural-key coupling.
11. **Q (production): What's the correct way to bulk-load millions of rows?** A: `COPY` (Postgres) / `LOAD DATA INFILE` (MySQL) — bypasses row-by-row parsing; batch within transactions; disable non-essential indexes during load or use `ON CONFLICT`; monitor FK checks. INSERT-per-row loops are the anti-pattern.
12. **Q: How do you rename a column?** A: `ALTER TABLE t RENAME COLUMN old TO new;` (Postgres); MySQL 8.0: `ALTER TABLE t RENAME COLUMN old TO new;` (older: `CHANGE old new TYPE`). Note: the catalog updates; apps must follow (or use views for backward compat).
13. **Q (tricky): Does `GRANT SELECT` let the grantee read all columns?** A: Yes, all columns of the table (SELECT grants are column-less). For column-level hiding, create a *view* exposing only allowed columns and grant SELECT on the view — the classic security pattern.
14. **Q: What is `WITH GRANT OPTION`?** A: It lets the grantee further grant the same privilege to others (delegation). Dangerous (privilege escalation chains) — restricted to trusted roles; revoke cascades can surprise.
15. **Q: What does `REVOKE` do to already-running statements?** A: Nothing retroactive — enforcement is per-statement at parse/execute time; in-flight transactions keep running (Postgres checks per statement). Revoking prevents *future* access.
16. **Q (scenario): Write TCL for a money transfer with a validation step.** A: `BEGIN; UPDATE a SET bal=bal-100; UPDATE b SET bal=bal+100; SAVEPOINT s; UPDATE a SET bal=-999999; /* fails CHECK */ ROLLBACK TO s; COMMIT;` — the SAVEPOINT keeps the valid work, undoing only the bad step.
17. **Q: How do you add a CHECK constraint to existing data safely?** A: Postgres: `ALTER TABLE t ADD CONSTRAINT c CHECK (...) NOT VALID;` then `VALIDATE CONSTRAINT c;` — the NOT VALID add skips the scan (no lock), validation checks old rows in the background. Standard zero-downtime pattern.
18. **Q (hard): `UPDATE` on a table with 2M rows and 6 indexes — where's the cost?** A: Row lookup (scan or index) + MVCC new version + up to 6 index entry updates + WAL logging + vacuuming later. Writes are *index-bound* — that's why write-heavy tables keep indexes minimal.
19. **Q: What is `RETURNING` for?** A: `INSERT/UPDATE/DELETE ... RETURNING col` returns the affected rows — Postgres' way to get the new PK/id/generated values in one round trip (avoiding a second SELECT). Also used in batching patterns.
20. **Q (tricky): Is `CREATE INDEX` DDL? Does it block?** A: Yes, DDL. In Postgres, `CREATE INDEX` takes a SHARE lock (blocks writes, allows reads) while `CREATE INDEX CONCURRENTLY` builds without blocking (longer, more I/O). MySQL 8 uses in-place ALGORITHM=INPLACE with some allowance. Name the CONCURRENTLY option for production.

## 14. Follow-Up Questions
1. **Q: What's the difference between `SERIAL` and `IDENTITY`?** A: IDENTITY is standard, NOT NULL by default, and you can't accidentally insert explicit values (unless OVERRIDING); SERIAL is a shorthand (default nextval) with quirks (allows NULL inserts historically). New schemas: use IDENTITY.
2. **Q: What is a DDL trigger / event trigger?** A: Postgres event triggers run on DDL events (`CREATE/DROP/ALTER`) — used for governance (log DDL, block destructive statements). MySQL lacks DDL triggers; a MySQL-vs-Postgres differentiator.
3. **Q: Can DML statements be prepared and reused?** A: Yes — PREPARE/EXECUTE (or driver-level prepared statements) parse+plan once, re-run with parameters: faster and injection-safe. The basis of every ORM's `execute(sql, params)`.
4. **Q: Why is `UPDATE ... SET balance = balance - 100` atomic while read-modify-write in app code isn't?** A: The SET form is a single statement — the engine locks the row, reads, computes, writes under the lock; app-level read-then-write has a gap two transactions can race through. Always push the arithmetic into SQL.
5. **Q: What happens to FKs when you `TRUNCATE` a referenced table?** A: Postgres refuses (TRUNCATE on a table referenced by FK RESTRICT) unless you TRUNCATE both `CASCADE` (dangerous). MySQL may allow with `FOREIGN_KEY_CHECKS=0` (orphan risk). Never truncate referenced tables casually.

## 15. Coding Example
```sql
-- Complete DDL+DML+DCL+TCL with constraints (Postgres-flavored, portable ideas)
BEGIN;

CREATE TABLE products (
  sku      TEXT PRIMARY KEY,
  name     TEXT NOT NULL,
  price    NUMERIC NOT NULL CHECK (price >= 0),
  qty      INT NOT NULL DEFAULT 0 CHECK (qty >= 0)
);

CREATE TABLE cart_items (
  cart_id   INT NOT NULL,
  sku       TEXT NOT NULL REFERENCES products(sku) ON DELETE CASCADE,
  qty       INT NOT NULL CHECK (qty > 0),
  PRIMARY KEY (cart_id, sku)
);
COMMIT;   -- transactional DDL: both tables or neither

-- DML with RETURNING (get IDs in one round trip)
INSERT INTO products (sku, name, price, qty)
VALUES ('SKU-1', 'Keyboard', 49.99, 100)
ON CONFLICT (sku) DO UPDATE SET qty = products.qty + EXCLUDED.qty
RETURNING sku, qty;

-- Atomic decrement inside a transaction with a guard
BEGIN;
UPDATE products SET qty = qty - 1 WHERE sku = 'SKU-1' AND qty > 0;
INSERT INTO cart_items (cart_id, sku, qty) VALUES (1, 'SKU-1', 1);
COMMIT;  -- if qty was 0, UPDATE affected 0 rows -> app can detect & rollback

-- DCL
GRANT SELECT, INSERT ON cart_items TO web_app;
REVOKE DELETE ON cart_items FROM web_app;
```

## 16. Industry Usage
- **Migration frameworks** (Flyway, Liquibase, Prisma) run DDL in ordered, versioned scripts; Postgres's transactional DDL is a headline reason migrations are safer there than MySQL's auto-commit DDL.
- **Upserts power sync pipelines**: `ON CONFLICT` (Postgres), `ON DUPLICATE KEY UPDATE` (MySQL), `MERGE` (SQL Server/Oracle) are how CDC/event systems reconcile targets.
- **Zero-downtime schema change**: `ALTER TABLE ... ADD COLUMN` metadata-only (Postgres 11+, MySQL 8 instant), `CREATE INDEX CONCURRENTLY`, `NOT VALID` constraints — the modern deployment playbook.
- **Least-privilege DCL** is a compliance requirement (SOC2/PCI): service accounts get only the DML they need; analysts get SELECT on views; DDL/DCL reserved for CI/CD migration roles.
- **`COPY` / `\copy`** (Postgres) is how warehouses load terabytes; **dbt** wraps DML models in transactions and runs `CREATE TABLE AS`/`INSERT` under the hood — DML/DDL patterns at analytics scale.

## 17. References
- PostgreSQL Documentation, SQL Commands (DDL/DML/DCL/TCL): https://www.postgresql.org/docs/current/sql-commands.html
- PostgreSQL Documentation, `INSERT ... ON CONFLICT`: https://www.postgresql.org/docs/current/sql-insert.html
- MySQL Reference Manual, SQL Statements: https://dev.mysql.com/doc/refman/8.0/en/sql-statements.html
- MySQL Reference Manual, `ON DUPLICATE KEY UPDATE`: https://dev.mysql.com/doc/refman/8.0/en/insert-on-duplicate.html
- ISO/IEC 9075-2:2016 (SQL — Foundation).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 4 (SQL: DDL/DML).

## 18. Cheat Sheet
- DDL: CREATE / ALTER / DROP / TRUNCATE / RENAME (schema; Postgres-transactional).
- DML: INSERT / UPDATE / DELETE / MERGE / SELECT (rows; transactional).
- DCL: GRANT / REVOKE. TCL: BEGIN / COMMIT / ROLLBACK / SAVEPOINT.
- Constraints: NOT NULL, UNIQUE, PK, FK (ON DELETE actions), CHECK.
- Upsert: `ON CONFLICT ... DO UPDATE` (Postgres) / `ON DUPLICATE KEY UPDATE` (MySQL).
- DELETE = row-wise, undoable; TRUNCATE = page-level, faster, no triggers.
- Zero-downtime DDL: ADD COLUMN metadata-only, CREATE INDEX CONCURRENTLY, NOT VALID.
- Bulk load: COPY / LOAD DATA INFILE, batched, inside transactions.

## 19. Quiz
1. Which is DDL? a) UPDATE b) ALTER c) GRANT d) COMMIT → **b**
2. Postgres upsert keyword: a) ON DUPLICATE KEY b) ON CONFLICT DO UPDATE c) MERGE INTO d) REPLACE → **b**
3. `ALTER TABLE t ADD COLUMN c TEXT NOT NULL DEFAULT 'x'` on 1M rows: a) always rewrites b) metadata-only in modern Postgres c) impossible d) drops table → **b**
4. TRUNCATE vs DELETE: a) same b) TRUNCATE skips triggers c) DELETE skips triggers d) TRUNCATE per-row → **b**
5. Which auto-commits in MySQL? a) INSERT b) DDL c) SELECT d) UPDATE → **b**
6. `CREATE INDEX CONCURRENTLY` (Postgres): a) blocks writes b) builds without blocking c) is DML d) drops indexes → **b**
7. `RETURNING` lets you: a) get affected rows in one trip b) revert c) grant d) truncate → **a**
8. GRANT SELECT on a table grants: a) all columns b) only PK c) only non-null d) indexes → **a**
9. To add a CHECK without scanning existing rows: a) `NOT VALID` b) `CONCURRENTLY` c) `DEFERRABLE` d) `CASCADE` → **a**
10. Bulk-load best practice: a) INSERT loop b) COPY/LOAD DATA in batches c) TRUNCATE d) upsert-less raw → **b**

## 20. Flashcards
- **Q: 4 DML verbs?** → **A:** INSERT, UPDATE, DELETE, MERGE (+SELECT read).
- **Q: Upsert in Postgres?** → **A:** `INSERT ... ON CONFLICT (col) DO UPDATE SET ...`.
- **Q: DELETE vs TRUNCATE?** → **A:** Row-wise/undoable/triggers vs page-level/fast/no triggers.
- **Q: Why batch big UPDATEs?** → **A:** Avoid one giant lock; small batches respect MVCC/concurrency.
- **Q: Zero-downtime index?** → **A:** `CREATE INDEX CONCURRENTLY` (Postgres).
- **Q: What is RETURNING?** → **A:** Returns affected rows — one round trip.
- **Q: Column-level security?** → **A:** View exposing allowed columns + GRANT SELECT on it.
- **Q: Is MySQL DDL transactional?** → **A:** No — implicit commit per statement.

## 21. Revision
DDL = schema (CREATE/ALTER/DROP/TRUNCATE — Postgres-transactional, MySQL auto-commits; zero-downtime tricks: metadata-only ADD COLUMN, CREATE INDEX CONCURRENTLY, NOT VALID). DML = rows (INSERT/UPDATE/DELETE/MERGE — transactional; upsert via ON CONFLICT / ON DUPLICATE KEY; always push arithmetic into the statement for atomicity). DCL = GRANT/REVOKE (least privilege; column security via views). TCL = BEGIN/COMMIT/ROLLBACK/SAVEPOINT. Constraints declared inline (NOT NULL/UNIQUE/PK/FK/CHECK). Interview moves: write the orders table from memory; compare TRUNCATE vs DELETE; explain upsert semantics; state the batching rule for big writes; and name COPY for bulk loads. Always tie DDL to locking/zero-downtime and DML to atomicity/index cost.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Write a CREATE TABLE with constraints" | 8 / 13 Q1 |
| "DELETE vs TRUNCATE?" | 13 Q4 |
| "How to write an upsert?" | 13 Q5-6 |
| "Batch big UPDATEs?" | 13 Q8 |
| "Zero-downtime DDL?" | 13 Q17, Q20 |
| "GRANT/REVOKE patterns?" | 13 Q13-14 |
| "What is RETURNING?" | 13 Q19 |
| "Bulk loading best practice?" | 13 Q11 |
