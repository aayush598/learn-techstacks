# DBMS Languages: DDL, DML, DCL, TCL

> **TL;DR**: SQL is split into four language families by concern — DDL defines structure, DML manipulates data, DCL grants/revokes permissions, and TCL manages transactions — so that each operation type can be scoped, secured, and audited independently.

## 1. Why Does This Exist?
If SQL were one undifferentiated blob of commands, the DBMS couldn't cleanly separate *who may change structure* from *who may change data* from *who may change permissions*. The division into DDL/DML/DCL/TCL exists for **separation of concerns**: structure (schema) and data (rows) are different beasts that require different privileges, different audit trails, and different transaction semantics. DDL must be tightly controlled (one bad `DROP TABLE` destroys a schema); DML must be granted per-table; DCL is the *most* privileged (granting power is power); TCL groups operations into atomic units. The partition lets a DBA give analysts `SELECT` but not `DROP`, and lets the DBMS apply different locking/undo rules to each class.

## 2. How Does It Work?
Four families, each with a fixed set of core commands:
- **DDL (Data Definition Language)**: `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME`, `COMMENT` — modify the *schema* (catalog). Auto-commits in MySQL; transactional in Postgres/Oracle.
- **DML (Data Manipulation Language)**: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `MERGE` — operate on *rows*. DML is the only family you can wrap in transactions for user data.
- **DCL (Data Control Language)**: `GRANT`, `REVOKE`, `DENY` (SQL Server) — manage privileges. Grants are catalog rows the authorization manager enforces on every statement.
- **TCL (Transaction Control Language)**: `BEGIN`/`START TRANSACTION`, `COMMIT`, `ROLLBACK`, `SAVEPOINT` — delimit atomic units, control the transaction manager.
Each command routes to a different subsystem: DDL→catalog manager, DML→optimizer/executor, DCL→authorization manager, TCL→transaction manager.

## 3. When Is It Used?
- **DDL**: initial schema design, migrations, index creation (`CREATE INDEX`), adding columns — the domain of developers and DBAs.
- **DML**: the *entire* application workload — every read (`SELECT`) and write (`INSERT/UPDATE/DELETE`) your app issues.
- **DCL**: onboarding/offboarding users, granting analysts read-only access, revoking a departed employee — a DBA/security duty.
- **TCL**: every multi-statement operation that must be atomic (money transfer, order+inventory update), batch jobs, ETL loads.
- **Combined**: a deployment script typically runs DDL (schema), then DML (seed data), within TCL wrappers, after DCL ensures the service account can act.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: one language, no privilege classes.** Rejected: then a user with `UPDATE` could also `DROP TABLE`; you'd need per-command ACLs anyway, which is just DCL unstated. Partitioning makes *privilege granularity* expressible ("GRANT SELECT, UPDATE ON orders").
- **Alternative: DDL and DML in separate proprietary languages (pre-SQL history).** Some early DBMSs separated schema language from data language; rejected because one integrated language is easier to learn/script, and the families share syntax and engine.
- **Alternative: TCL as part of DML.** Rejected: `COMMIT`/`ROLLBACK` are *meta*-operations about a group of DML — lumping them in would conflate "what data changes" with "when it's made permanent". Keeping TCL separate lets the transaction manager own atomicity explicitly.
- **Why this 4-way split?** It mirrors the four distinct subsystems (catalog, executor, authorization, transaction manager) and the four distinct privilege domains — it's the minimal clean partition that maps onto the architecture.

## 5. Intuition
Think of a **company's office rules**. DDL is the **blueprint/construction permit** — who may build new rooms, knock down walls, or renumber rooms (structure). DML is **day-to-day operations** — moving boxes, editing files, taking inventory (the actual work). DCL is the **key-cabinet** — who gets keys to which rooms (access control); giving away keys is the most sensitive act. TCL is the **camera+ledger** — "start recording, this shift's actions are one batch; if anything goes wrong, scrub the whole shift" (atomicity). You wouldn't give the intern the construction permit just because they can edit files — so the language is split so the *keys* can be split.

## 6. Real-World Analogy
A **restaurant kitchen** again: DDL is the **architect who designs the kitchen** — adding ovens, rearranging stations, installing the pass. DML is the **line cooks** — chopping, plating, serving (the daily data operations). DCL is the **manager with the key card system** — deciding who may enter the storeroom and who may only see the menu. TCL is the **shift coordinator** — "tonight's service is one unit: every order logged, and if the POS crashes, we can roll tonight back to the last confirmed close-out." The architect doesn't plate dishes and the cooks don't grant keys — separation keeps each role controllable.

## 7. Formal Definition
SQL (ISO/IEC 9075) is partitioned into:
- **DDL**: statements that define, alter, or drop the database structure (schema) — `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME`. Effects are recorded in the catalog.
- **DML**: statements that retrieve and modify data — `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `MERGE` (and `VALUES`/`TABLE`).
- **DCL**: statements that control access rights — `GRANT`, `REVOKE` (plus `DENY` in SQL Server).
- **TCL**: statements that manage transactions — `START TRANSACTION`/`BEGIN`, `COMMIT`, `ROLLBACK`, `SAVEPOINT`, `SET TRANSACTION`.
(Elmasri & Navathe Ch. 4; Silberschatz Ch. 1.3.)

## 8. Example
Building a university DB with all four families:
```sql
-- DDL: define structure
CREATE TABLE students (id INT PRIMARY KEY, name TEXT, gpa NUMERIC(3,2));
ALTER TABLE students ADD COLUMN dept TEXT;      -- structure change
CREATE INDEX idx_students_dept ON students(dept);

-- DML: manipulate data
INSERT INTO students VALUES (1, 'Alice', 3.8, 'CS');
UPDATE students SET gpa = 3.9 WHERE id = 1;
DELETE FROM students WHERE gpa < 1.0;

-- DCL: control access
GRANT SELECT ON students TO analyst_role;
REVOKE DELETE ON students FROM analyst_role;

-- TCL: wrap multi-step work atomically
BEGIN;
  INSERT INTO enroll VALUES (1, 'CS101');
  UPDATE seats SET count = count - 1 WHERE course = 'CS101';
COMMIT;
```

## 9. Internal Working
1. **DDL** → catalog manager: validates statement, inserts/updates/deletes catalog rows, allocates storage for new relations, builds indexes. In transactional engines, catalog changes are journaled (WAL) and roll back with the transaction.
2. **DML** → query processor: parse → optimize → execute. Writes additionally go through the transaction manager (locks + WAL). `SELECT` is the only DML that never writes.
3. **DCL** → authorization manager: `GRANT` inserts privilege rows (e.g., `pg_class.relacl`, `mysql.tables_priv`); enforcement happens on *every* later statement (per-statement check, cached).
4. **TCL** → transaction manager: `BEGIN` opens a transaction (assigns snapshot/lock ownership); `COMMIT` fsyncs WAL, releases locks, makes changes visible; `ROLLBACK` undoes via WAL/undo log; `SAVEPOINT` marks a rollback point within the transaction.
5. **All families** run under the same parsing pipeline; the *target subsystem* differs — that's the elegance of one language, four concerns.

## 10. Time Complexity
- **DDL**: `CREATE INDEX` O(n log n); `DROP TABLE` O(catalog cleanup + space release); `ALTER ADD COLUMN` O(1) in most engines (metadata-only in Postgres ≥11, no table rewrite); adding NOT NULL with DEFAULT may rewrite O(n).
- **DML**: `SELECT`/`UPDATE`/`DELETE` with index O(log n + affected); without index O(n); `INSERT` O(log n) on clustered PK, O(1) heap append + index maintenance.
- **DCL**: `GRANT` O(1) catalog update; per-statement check O(1) cached.
- **TCL**: `COMMIT` O(WAL fsync) — dominated by disk latency (~ms); `ROLLBACK` O(undo size).

## 11. Advantages
- **Privilege granularity**: grant structure vs data vs control rights separately; least-privilege is expressible.
- **Auditability**: each family can be logged/audited independently (who ran DDL vs DML vs DCL).
- **Clear semantics**: structure vs rows vs permissions vs atomicity each have their own verbs and rules.
- **Transactional DDL** (in engines that support it): schema + data changes in one atomic migration.
- **Portability**: the families and their core verbs are standardized across vendors.
- **Scoped locking/undo**: `TRUNCATE` (DDL) can skip per-row undo; `DELETE` (DML) needs undo — the split lets engines optimize each.

## 12. Disadvantages
- **Blurred edges**: MySQL's `TRUNCATE` is DDL but behaves like a fast DELETE; `MERGE` is DML but mixes INSERT+UPDATE+DELETE — classification questions trip people up.
- **Non-transactional DDL in some engines** (MySQL): a failed multi-DDL migration leaves partial structure — a real production hazard.
- **Over-granting risk**: coarse `GRANT ALL` patterns defeat the whole purpose; enforcement is per-statement so *correct* grants are a discipline.
- **Auto-commit traps**: forgetting `BEGIN` means every DML auto-commits — developers can't get atomicity by accident.
- **Vendor divergences**: `DENY` (SQL Server), `MERGE` availability, `TRUNCATE` semantics vary — standard ≠ identical.

## 13. Interview Questions
1. **Q: What are the four SQL language families?** A: DDL (structure: CREATE/ALTER/DROP/TRUNCATE), DML (data: SELECT/INSERT/UPDATE/DELETE/MERGE), DCL (privileges: GRANT/REVOKE), TCL (transactions: BEGIN/COMMIT/ROLLBACK/SAVEPOINT).
2. **Q: Why separate DDL from DML?** A: Separation of concerns + privilege granularity: structure changes are catastrophic and rare (tightly controlled, DBA-only), data changes are routine (per-table grants). Different subsystems, different audit trails, different transaction semantics.
3. **Q: Is `SELECT` a DML statement?** A: Yes — DML includes data retrieval (SELECT) plus modification (INSERT/UPDATE/DELETE/MERGE). It's the read-only member of the family.
4. **Q: What does `TRUNCATE` do and why is it DDL?** A: It removes all rows instantly by deallocating table pages (fast, non-logged per-row) — the whole table is dropped of data, structure remains. It's classified DDL because it resets the table (like dropping/recreating) and typically can't be rolled back per-row; MySQL treats it as implicit commit.
5. **Q (tricky): `DELETE` vs `TRUNCATE`?** A: `DELETE` is DML — per-row, fires triggers, can use WHERE, is transactional/undoable. `TRUNCATE` is DDL — drops all pages, no triggers, no WHERE, faster, usually not transactional. Choose TRUNCATE only when you're wiping a table and can accept non-undoable behavior.
6. **Q: What does `GRANT` do? Give the syntax.** A: Grants privileges on objects to roles/users: `GRANT SELECT, INSERT ON students TO analyst;`. It writes privilege rows that the authorization manager enforces on every subsequent statement.
7. **Q: What does `REVOKE` do?** A: Removes previously granted privileges: `REVOKE DELETE ON students FROM analyst;`. The inverse of GRANT; also enforced per-statement.
8. **Q (production): What is least privilege and how does DCL enable it?** A: Grant only the minimum privileges a role needs: analysts get `SELECT`, service accounts get the DML they perform, only DBAs get `GRANT`/DDL. DCL's per-object, per-operation grants make this policy expressible and auditable.
9. **Q: What does `COMMIT` do at the engine level?** A: Tells the transaction manager the transaction is complete: WAL is fsynced (durability point), locks released, and all changes become visible to other transactions atomically.
10. **Q: What does `ROLLBACK` do?** A: Aborts the transaction and undoes all its changes via the WAL/undo log, releasing locks and restoring the previous committed state. It's the "all or nothing" in atomicity.
11. **Q: What is a `SAVEPOINT`?** A: A marker inside a transaction that lets you roll back to a point *without* aborting the whole transaction: `ROLLBACK TO SAVEPOINT s1;` then continue. Useful in long batch transactions.
12. **Q (tricky): Is DDL transactional in Postgres vs MySQL?** A: Postgres/Oracle/SQL Server: yes — DDL participates in transactions and rolls back. MySQL: mostly no — DDL causes implicit commit and cannot be rolled back. This asymmetry is a classic interview favorite and a real migration-planning concern.
13. **Q: What happens if you forget `BEGIN` before two `UPDATE`s?** A: Each statement auto-commits individually — no atomicity. A crash between them leaves a partial result (e.g., debit applied, credit not). Wrapping in `BEGIN...COMMIT` fixes it.
14. **Q (scenario): An analyst should read but never modify `orders`. Write the DCL.** A: `REVOKE INSERT, UPDATE, DELETE ON orders FROM analyst_role; GRANT SELECT ON orders TO analyst_role;` (or just grant SELECT in the first place).
15. **Q: What is `MERGE`?** A: A single DML statement that conditionally INSERTs, UPDATEs, or DELETEs based on a source (upsert). It's DML because it manipulates rows; useful for ETL syncs.
16. **Q (production): What does `ALTER TABLE ADD COLUMN` cost?** A: In modern engines (Postgres 11+), adding a nullable column is O(1) — metadata-only, no table rewrite. Adding a column with a DEFAULT/constraint may rewrite O(n); MySQL 8.0.12+ optimizes many cases (instant add). Size the risk by engine and version.
17. **Q: `CREATE INDEX` — DDL and how expensive?** A: Yes, DDL. It builds the index structure, cost O(n log n) on the table, taking locks (share-lock, non-blocking reads in many engines). DDL that scans your biggest table is why migrations are scheduled.
18. **Q (tricky): Can you use DML inside a DDL statement?** A: No — they're separate families. But DDL/DML can be *mixed inside one transaction* (Postgres): `BEGIN; ALTER TABLE...; INSERT...; COMMIT;` — both roll back together. That's the power of transactional DDL.
19. **Q: Who should have DCL privileges?** A: DBAs and security roles only. GRANT grants power — a user with `GRANT` can delegate privileges. Least-privilege says: very few humans hold the key cabinet.
20. **Q: What is autocommit and why does it bite?** A: Autocommit = every statement commits immediately. It bites because multi-statement operations lose atomicity and because *read* transactions get inconsistent snapshots across statements. Explicit `BEGIN` is the fix.

## 14. Follow-Up Questions
1. **Q: Why is `TRUNCATE` faster than `DELETE`?** A: DELETE logs each row for undo; TRUNCATE just deallocates pages and resets metadata — no per-row undo, no triggers, fewer locks. Speed vs undoability is the trade.
2. **Q: What is the difference between `REVOKE` and `DENY` (SQL Server)?** A: REVOKE removes a grant (neutral); DENY explicitly forbids and wins over GRANT. Postgres/MySQL lack DENY — SQL Server's superset is a differentiator.
3. **Q: Can DCL be rolled back?** A: In transactional engines, GRANT/REVOKE participate in transactions (roll back). In MySQL, they auto-commit like DDL. Same engine asymmetry as DDL.
4. **Q: What is `SET TRANSACTION ISOLATION LEVEL`?** A: TCL-adjacent DML control — sets the isolation level (READ COMMITTED, REPEATABLE READ, etc.) for the transaction, changing locking/snapshot behavior. Often asked alongside TCL.
5. **Q: What is an "upsert"?** A: INSERT ... ON CONFLICT (Postgres) / ON DUPLICATE KEY UPDATE (MySQL) / MERGE — atomic insert-or-update. It's DML, and it's one of the most-asked practical DML patterns.

## 15. Coding Example
```sql
-- DDL: schema lifecycle
CREATE TABLE accounts (id BIGSERIAL PRIMARY KEY, owner TEXT, balance NUMERIC);
ALTER TABLE accounts ADD COLUMN currency TEXT DEFAULT 'INR';
CREATE INDEX idx_accounts_owner ON accounts(owner);
-- DROP TABLE accounts;  -- catastrophic; gated behind DBA privileges

-- DML: data lifecycle
INSERT INTO accounts (owner, balance) VALUES ('Alice', 500), ('Bob', 100);
UPDATE accounts SET balance = balance + 50 WHERE owner = 'Alice';
DELETE FROM accounts WHERE balance <= 0;

-- DCL: access control
CREATE ROLE analyst;
GRANT SELECT ON accounts TO analyst;
REVOKE UPDATE ON accounts FROM analyst;

-- TCL: atomic unit
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE owner = 'Alice';
  UPDATE accounts SET balance = balance + 100 WHERE owner = 'Bob';
SAVEPOINT before_verify;
  UPDATE accounts SET balance = balance - 999999 WHERE owner = 'Alice';  -- fails CHECK
ROLLBACK TO SAVEPOINT before_verify;   -- keep going, undo only this bit
COMMIT;
```
```python
# Practical: forcing transactionality in app code (autocommit off)
conn.autocommit = False
try:
    cur = conn.cursor()
    cur.execute("UPDATE accounts SET balance = balance - 100 WHERE id=1")
    cur.execute("UPDATE accounts SET balance = balance + 100 WHERE id=2")
    conn.commit()
except Exception:
    conn.rollback()
```

## 16. Industry Usage
- **Migrations** (Flyway, Liquibase, Prisma) are DDL orchestration pipelines; their safety *depends* on the engine's transactional-DDL support (a core reason Postgres is favored for critical migrations).
- **Service accounts & least privilege** are audited requirements in SOC2/PCI environments: DCL statements (`GRANT`/`REVOKE`) are logged and reviewed — the four-family split makes such audit trails clean.
- **Postgres** famously runs `CREATE INDEX CONCURRENTLY` (DDL without blocking reads) for zero-downtime schema changes; **MySQL**'s `pt-online-schema-change` exists to emulate what transactional DDL gives for free.
- **ETL/ELT** (dbt, Airflow) wrap DML batch jobs in TCL so a failed load rolls back cleanly — atomicity is how warehouses avoid half-loaded days.
- **Every ORM** issues DML per query and DDL via migrations; the TCL/DCL layers stay in DBA hands — the split is how real organizations separate developer power from production risk.

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 4 (Relational Model & SQL — DDL/DML/DCL/TCL).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 1.3 & Ch. 4 (Data Languages; SQL).
- ISO/IEC 9075:2016 (SQL Standard, parts 1-11).
- PostgreSQL Documentation: https://www.postgresql.org/docs/current/sql-commands.html (SQL Commands).
- MySQL Reference Manual: https://dev.mysql.com/doc/refman/8.0/en/sql-statements.html (SQL Statements).

## 18. Cheat Sheet
- DDL = structure: CREATE / ALTER / DROP / TRUNCATE (schema, rare, dangerous).
- DML = data: SELECT / INSERT / UPDATE / DELETE / MERGE (daily work).
- DCL = privileges: GRANT / REVOKE (the key cabinet).
- TCL = transactions: BEGIN / COMMIT / ROLLBACK / SAVEPOINT (atomicity).
- SELECT is DML (the read-only one). TRUNCATE is DDL (faster, non-undoable).
- Postgres DDL is transactional; MySQL DDL auto-commits.
- DELETE = per-row, triggers, undoable; TRUNCATE = deallocates pages, no triggers.
- Never grant more than least privilege; only DBAs hold DCL.

## 19. Quiz
1. `ALTER TABLE` belongs to: a) DML b) DDL c) DCL d) TCL → **b**
2. `SELECT` is: a) DDL b) DML c) DCL d) TCL → **b**
3. `GRANT` belongs to: a) DML b) DDL c) DCL d) TCL → **c**
4. `COMMIT` belongs to: a) DML b) DDL c) DCL d) TCL → **d**
5. Which is faster and non-undoable? a) DELETE b) TRUNCATE c) UPDATE d) MERGE → **b**
6. In MySQL, DDL is: a) transactional b) auto-committed c) disallowed d) asynchronous → **b**
7. `ROLLBACK TO SAVEPOINT s1` — what is this? a) DCL b) partial rollback within a transaction c) DDL d) index rebuild → **b**
8. Which gives an analyst read access? a) GRANT SELECT b) CREATE VIEW c) BEGIN d) COMMIT → **a**
9. `MERGE` is classified as: a) DDL b) DML c) DCL d) TCL → **b**
10. Forgetting BEGIN before two UPDATEs causes: a) deadlock b) no atomicity c) faster writes d) data types error → **b**

## 20. Flashcards
- **Q: 4 SQL families?** → **A:** DDL (structure), DML (data), DCL (privileges), TCL (transactions).
- **Q: Is SELECT DML?** → **A:** Yes — the read-only DML statement.
- **Q: TRUNCATE vs DELETE?** → **A:** TRUNCATE = DDL, deallocates pages, fast, no triggers/undo; DELETE = DML, per-row, undoable.
- **Q: GRANT syntax?** → **A:** GRANT SELECT, INSERT ON table TO role;
- **Q: Is DDL transactional in Postgres?** → **A:** Yes; MySQL mostly no (implicit commit).
- **Q: What does COMMIT do?** → **A:** Fsync WAL, release locks, make changes visible atomically.
- **Q: What is a SAVEPOINT?** → **A:** A rollback point within a transaction.
- **Q: Least privilege?** → **A:** Grant only the minimum needed; only DBAs hold DCL.

## 21. Revision
Four families, one language: **DDL** builds the blueprint (CREATE/ALTER/DROP/TRUNCATE — structure, DBA-gated, Postgres-transactional vs MySQL auto-commit), **DML** does the daily work (SELECT/INSERT/UPDATE/DELETE/MERGE — rows), **DCL** controls the keys (GRANT/REVOKE — privileges, only DBAs), **TCL** wraps atomic units (BEGIN/COMMIT/ROLLBACK/SAVEPOINT). Interview moves: classify 10 commands fast (SELECT = DML, TRUNCATE = DDL); compare TRUNCATE vs DELETE (speed vs undo); state the MySQL-vs-Postgres DDL asymmetry; write GRANT/REVOKE for an analyst; explain why forgetting BEGIN loses atomicity. The split exists for privilege granularity + subsystem mapping — say that, not just the names.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Name and classify the SQL families" | 7 / 13 Q1 |
| "DELETE vs TRUNCATE?" | 13 Q5 |
| "What is DCL / GRANT / REVOKE?" | 13 Q6-7 |
| "Is DDL transactional (Postgres vs MySQL)?" | 13 Q12 |
| "What is a SAVEPOINT?" | 13 Q11 |
| "What happens without BEGIN?" | 13 Q13 |
| "What does COMMIT do at the engine level?" | 13 Q9 |
| "How do migrations use DDL?" | 13 Q16-17 |
