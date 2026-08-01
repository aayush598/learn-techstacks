# Relational Integrity Constraints

> **TL;DR**: Integrity constraints are declarative rules the DBMS enforces on every write so that invalid data (orphan references, duplicate identities, out-of-range values) is *impossible to insert*, not merely discouraged by application code.

## 1. Why Does This Exist?
Data enters a database through applications — and applications have bugs, race conditions, and malicious inputs. Integrity constraints exist so that *the database itself* rejects invalid data, rather than trusting every writer to be correct. They exist because: (1) **single enforcement point** — the DB is the only place all writers pass through, so one constraint covers every app, script, and manual query; (2) **atomic enforcement** — a constraint check and the write happen atomically under the engine's control, so no window of invalid state exists; (3) **data quality guarantees** — consumers can *assume* invariants (FK exists, balance ≥ 0) instead of checking defensively. In short: constraints move data-validation authority from fallible code into the engine where it's enforced for everyone, always.

## 2. How Does It Work?
Constraints are declared in DDL (`CREATE TABLE`/`ALTER TABLE`) and recorded in the catalog. On every INSERT/UPDATE/DELETE, the engine runs the applicable checks *inside the same transaction*:
- **NOT NULL**: rejects NULL in the column.
- **UNIQUE**: unique index probe rejects duplicate values (multiple NULLs allowed).
- **PRIMARY KEY**: NOT NULL + UNIQUE (one per table).
- **FOREIGN KEY**: value must be NULL or present in the referenced unique key; triggers referential actions (RESTRICT/CASCADE/SET NULL/DEFAULT).
- **CHECK**: evaluates a Boolean predicate; fails the row if false.
- **Domain/type**: type coercion/enforcement via the column's type.
Each violation raises an error and rolls back the *statement* (or transaction, per engine). Constraints live in the catalog, so they're applied identically to every session.

## 3. When Is It Used?
- **Schema design**: declaring PK/FK/CHECK/UNIQUE/NOT NULL for every table — the norm for all production schemas.
- **Data quality**: preventing negative balances (CHECK), impossible dates (CHECK), duplicate customers (UNIQUE on email), empty strings (CHECK length).
- **Referential integrity**: cascade/set-null behaviors for parent-child data (orders → order items).
- **Data migrations**: `ADD CONSTRAINT` to backfill-validate existing rows (`NOT VALID` in Postgres to validate without locking).
- **ETL/imports**: constraints are the "spell-checker" that catches dirty source data during loads.
- **App-level safety net**: even when apps validate, constraints are the final gate — defense in depth.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: validate only in application code.** Rejected: apps multiply (web, mobile, scripts, cron, analysts), each must re-implement the rules, and races let invalid data slip between validation and write. The DB is the one choke point all writes share — constraints there are atomic and universal.
- **Alternative: triggers for everything.** Rejected: triggers are procedural, harder to reason about, expensive, and not introspectable like constraints; constraints are declarative, optimizer-known, and cheap (index probes vs row-by-row code). Triggers remain for *business* logic constraints can't express.
- **Alternative: check on read (scrub queries).** Rejected: too late — invalid data is already stored, and consumers see garbage. Prevention-at-write beats correction-after-the-fact.
- **Why declarative?** Because declarative constraints (a) are self-describing (the schema documents its own invariants), (b) are enforceable by any engine in any session, (c) can be used by the optimizer to prune/cache (e.g., NOT NULL → skip null checks), and (d) cost far less than hand-rolled code.

## 5. Intuition
Constraints are the **form's built-in validation**, the difference between a paper form (where a clerk checks after you fill it) and a web form that *won't submit* until every field is right. With paper, someone always slips through with an empty "required" field. With the DBMS's declarative validation, the write simply cannot happen: "phone must be 10 digits" → type/CHECK; "no duplicate emails" → UNIQUE; "order must belong to a real customer" → FK. The rule lives in the form itself (the schema), not in whoever happens to be typing. That's the whole idea — invariants attached to the data, enforced by the engine, every time.

## 6. Real-World Analogy
A **bank's teller handbook**: every transaction must follow rules — "cannot withdraw more than the balance" (CHECK), "one account number per customer" (UNIQUE), "a transaction must reference an existing account" (FK), "every transaction has an amount" (NOT NULL). If rules lived only in each teller's head (application code), a new teller, a remote branch, or a rushed ATM could break them. But when the *ledger software* (the DBMS) refuses to record an invalid transaction no matter who enters it, the rules hold everywhere. Constraints are the handbook enforced by the machine.

## 7. Formal Definition
Integrity constraints are predicates that every legal database instance must satisfy. The DBMS guarantees they hold by checking each write. (Elmasri & Navathe Ch. 3; Silberschatz Ch. 2.4.)
- **Domain constraints**: attribute values must belong to their domain (type, CHECK, enum, range) — also called domain integrity.
- **Entity integrity**: primary key attributes are non-null and unique.
- **Referential integrity**: a foreign key value must be NULL or match a candidate-key value in the referenced relation; actions on delete/update: CASCADE, SET NULL, SET DEFAULT, RESTRICT, NO ACTION.
- **Key integrity**: uniqueness of PK and all UNIQUE constraints.
- **User-defined / business constraints**: CHECK predicates and general assertions (`CREATE ASSERTION`), enforceable also via triggers.
- SQL declarations: `NOT NULL`, `UNIQUE`, `PRIMARY KEY`, `FOREIGN KEY ... REFERENCES ... [ON DELETE ...]`, `CHECK (expr)`, and column types themselves.

## 8. Example
```
CREATE TABLE customers (
  id       INT PRIMARY KEY,               -- entity integrity
  email    TEXT UNIQUE NOT NULL,          -- key + null constraints
  balance  NUMERIC CHECK (balance >= 0),  -- domain/business constraint
  join_date DATE CHECK (join_date <= CURRENT_DATE)  -- CHECK
);
CREATE TABLE orders (
  order_id  INT PRIMARY KEY,
  customer_id INT REFERENCES customers(id) ON DELETE CASCADE,  -- referential
  total     NUMERIC CHECK (total > 0)
);
```
Attempts:
- `INSERT customers (id, email) VALUES (1, NULL)` → violates NOT NULL.
- `INSERT customers (id, email, balance) VALUES (1,'a@x',-5)` → violates CHECK.
- `INSERT orders (order_id, customer_id, total) VALUES (10, 999, 50)` → FK violation (no customer 999).
- `DELETE FROM customers WHERE id=1` (has orders) → ON DELETE CASCADE deletes their orders.
Each is rejected atomically; no half-applied row ever exists.

## 9. Internal Working
1. **Declare**: DDL writes the constraint into the catalog (`pg_constraint`/`information_schema.table_constraints`) and creates supporting indexes (unique for PK/UNIQUE).
2. **Insert path**: for each new tuple, the engine: checks NOT NULL (O(1)); probes the unique/PK index for duplicates (O(log n)); evaluates CHECK predicates (O(1)); probes the referenced table's unique index for the FK value (O(log m)).
3. **Delete/update of parent**: FK machinery checks whether referencing rows exist (index on FK if present, else scan); applies the action (block/cascade/null) within the same transaction.
4. **Atomicity**: constraint violations raise an error that aborts the statement (Postgres aborts the whole transaction unless a savepoint); no partial writes.
5. **Deferred constraints** (some engines): FK checks can be deferred to `COMMIT` (e.g., `DEFERRABLE INITIALLY DEFERRED` in Postgres) for operations that temporarily violate mid-transaction (e.g., re-parenting trees).
6. **Validation of existing data**: `ADD CONSTRAINT ... NOT VALID` (Postgres) skips scanning old rows; a later `VALIDATE CONSTRAINT` checks them — used for zero-downtime migration.

## 10. Time Complexity
- **NOT NULL / CHECK**: O(1) per row (predicate evaluation).
- **UNIQUE / PK check**: O(log_f n) per insert (index probe); bulk unique-build O(n log n).
- **FK check on child write**: O(log_f m) on the referenced unique index.
- **FK check on parent delete**: O(k) if an index exists on the FK column; O(m) full scan if not (why you index FKs).
- **Cascade delete**: O(k log m) total (each child found by index).
- **Deferred constraints**: same cost, shifted to commit time.

## 11. Advantages
- **Universal enforcement**: one rule covers every writer — apps, scripts, imports, ad-hoc SQL.
- **Atomic**: invalid state can never even exist transiently.
- **Self-documenting**: the schema states its own invariants; tools and humans read them.
- **Optimizer-friendly**: NOT NULL / UNIQUE knowledge lets the planner simplify (skip checks, prove uniqueness).
- **Cheap**: index probes vs procedural trigger code.
- **Declarative & portable**: `information_schema` exposes them; SQL standardizes them.

## 12. Disadvantages
- **Check cost on hot writes**: each unique/FK check is an index probe; write-heavy tables pay per row.
- **Missing FK indexes**: FK checks/cascades without an index degrade to scans (a silent performance trap).
- **Migration friction**: adding a NOT NULL/CHECK to a huge table can lock or require table rewrites (mitigated by NOT VALID + rewrite techniques).
- **Inflexibility**: strict constraints can block legitimate patterns (e.g., UNIQUE with NULLs behaving oddly — partial indexes needed).
- **Not a substitute for business logic**: complex invariants still need triggers/app code; constraints are the base layer, not the whole answer.

## 13. Interview Questions
1. **Q: What are integrity constraints?** A: Declarative rules stored in the schema that the DBMS enforces on every write: NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK, and domain/type. They guarantee legal data without relying on application code.
2. **Q: Why enforce constraints in the DB instead of the app?** A: Single choke point — all writers (web, mobile, cron, scripts, imports) pass through the DB, so one constraint covers them all; enforcement is atomic and races can't slip invalid data between check and write. Apps can't be trusted to validate consistently.
3. **Q: Name the constraint types with examples.** A: NOT NULL (name required), UNIQUE (email), PRIMARY KEY (id), FOREIGN KEY (customer_id → customers.id), CHECK (balance ≥ 0, gpa ≤ 4), domain/type (INT, VARCHAR(10)).
4. **Q: What is entity integrity vs referential integrity?** A: Entity: PK is non-null and unique (every tuple has identity). Referential: every FK value is NULL or exists in the referenced unique key (no orphans).
5. **Q: What is a CHECK constraint and what can it do?** A: A Boolean predicate on one row's values: `CHECK (balance >= 0)`, `CHECK (start_date < end_date)`, `CHECK (dept IN ('CS','EE'))`. It runs on insert/update; false → row rejected.
6. **Q (tricky): Can a CHECK constraint reference another table?** A: Not portably/cheaply — CHECK is single-row. Cross-table rules need FKs, triggers, or assertions. Postgres ignores `CREATE ASSERTION` (not implemented); use triggers for complex cross-row rules.
7. **Q: What are the ON DELETE actions?** A: RESTRICT/NO ACTION (block if children exist), CASCADE (delete children), SET NULL (null the FK, needs nullable), SET DEFAULT (set a default FK). Default is NO ACTION in most engines.
8. **Q (scenario): Orders should be deleted with their customer, but payments preserved. Design it.** A: Orders: `FOREIGN KEY (customer_id) REFERENCES customers ON DELETE CASCADE`; payments: `ON DELETE SET NULL` (or SET DEFAULT / keep customer_id nullable) so financial history survives. Choose actions per ownership semantics.
9. **Q: What is a deferred constraint?** A: A FK/unique check postponed to commit time (Postgres `DEFERRABLE INITIALLY DEFERRED`). Needed when a transaction temporarily violates a rule mid-way (e.g., deleting and re-creating a parent) but is consistent at commit.
10. **Q (tricky): Does `UNIQUE` allow NULLs?** A: Yes, in most engines UNIQUE allows multiple NULLs (each NULL treated as distinct). Postgres/MySQL/SQLite: yes; Oracle historically: NULLs are distinct too. If you need "one NULL max," use a partial index (`CREATE UNIQUE INDEX ... WHERE col IS NOT NULL`) or exclude NULLs.
11. **Q: What is `NOT VALID` in Postgres and why use it?** A: `ALTER TABLE ... ADD CONSTRAINT ... NOT VALID` adds the constraint without scanning existing rows (fast, no big lock), then `VALIDATE CONSTRAINT` checks old data later. Enables zero-downtime constraint addition on large tables.
12. **Q (production): Adding `NOT NULL` to a 100M-row table — what's the cost?** A: In Postgres, adding a NOT NULL with a default still rewrites the table (O(n)) unless the column is already filled with the value (metadata-only in newer versions when no default needed). MySQL 8.0.12+ does many `ADD COLUMN` instantly. Check engine + version; schedule rewrites.
13. **Q: What is the difference between a constraint and a trigger?** A: Constraints are declarative, engine-optimized, and enforced per-write automatically; triggers are procedural code on events, used when logic can't be expressed as a constraint. Constraint violations abort automatically; triggers can be more flexible (and slower/more dangerous).
14. **Q (scenario): Duplicate customers keep appearing despite the app checking emails. Why?** A: A race — two requests both saw "email free," both inserted. The app check isn't atomic. Fix: `UNIQUE(email)` constraint; the second insert fails with a unique violation (then upsert with `ON CONFLICT`).
15. **Q: Why should FK columns be indexed?** A: FK checks on child writes probe the *referenced* unique index; but deleting/updating a parent requires finding *children* — without an index on the FK column that's a full scan (O(n)). Postgres doesn't auto-index FKs; add them for cascade/delete-heavy paths.
16. **Q (hard): Can a CHECK constraint call a function?** A: In Postgres yes (must be IMMUTABLE, deterministic — e.g., `CHECK (btrim(name) <> '')`); in general, keep CHECKs simple and single-row. Volatile functions can't be used (would break consistency).
17. **Q: What is the difference between `RESTRICT` and `NO ACTION`?** A: Practically identical — both refuse the operation if children exist; NO ACTION checks at end of statement (deferrable), RESTRICT immediately. Most engines treat them the same; choose one and be consistent.
18. **Q: What happens to constraints during `ALTER TABLE`?** A: Existing constraints stay enforced; new ones validated (immediately or NOT VALID). Constraint additions may take locks (SHARE ROW EXCLUSIVE in Postgres) — that's why heavy migrations use NOT VALID + background validation.
19. **Q: Can you disable constraints?** A: Some engines allow `SET CONSTRAINTS ALL DEFERRED` (Postgres), or dropping/readding in MySQL (which also has `FOREIGN_KEY_CHECKS=0` for imports). Disabling trades integrity for speed — use only in controlled maintenance, revalidate after.
20. **Q (hard): How do constraints interact with transactions?** A: Violations normally abort the statement/transaction; deferred constraints only fail at commit. Because checks run inside the transaction, concurrent transactions can't observe invalid state — the constraint + transaction manager together guarantee atomic validity.

## 14. Follow-Up Questions
1. **Q: Why does MySQL `FOREIGN_KEY_CHECKS=0` speed up imports?** A: It skips FK verification (and often cascades), avoiding per-row probe overhead. Dangerous: silent orphans possible. Re-enable and validate afterward.
2. **Q: What is a `DEFERRABLE` constraint really for?** A: Cases where an intermediate state is illegal but the end state is fine — e.g., renumbering a self-referencing tree or swapping PKs. It moves the check to commit.
3. **Q: Can a CHECK constraint be used for lookup-style validation (country codes)?** A: Yes for small fixed sets (`IN ('US','IN','GB')`); for dynamic reference data use a FK to a lookup table instead — constraints can't read changing tables.
4. **Q: Do constraints slow down writes meaningfully?** A: Each unique/FK check is an index probe (~O(log n)); for normal OLTP it's small, but bulk-loading millions of rows benefits from deferral or staged validation.
5. **Q: What's the interaction between constraints and partition tables?** A: PK/unique constraints on partitioned tables must include the partition key in many engines; FK constraints on partitioned parents are limited — a known constraint-vs-partitioning tension.

## 15. Coding Example
```sql
CREATE TABLE accounts (
  account_id BIGSERIAL PRIMARY KEY,
  email      TEXT UNIQUE NOT NULL CHECK (email ~ '@'),
  balance    NUMERIC NOT NULL DEFAULT 0 CHECK (balance >= 0),
  currency   CHAR(3) NOT NULL DEFAULT 'INR' CHECK (currency IN ('INR','USD','EUR'))
);

CREATE TABLE txns (
  txn_id    BIGSERIAL PRIMARY KEY,
  account_id BIGINT NOT NULL REFERENCES accounts(account_id) ON DELETE RESTRICT,
  amount    NUMERIC NOT NULL CHECK (amount <> 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_txns_account ON txns(account_id);   -- support the FK path

-- Violations all rejected:
INSERT INTO accounts (email, balance) VALUES ('bad', -1);
-- ERROR: new row for relation "accounts" violates check constraint

INSERT INTO txns (account_id, amount) VALUES (9999, 50);
-- ERROR: foreign key constraint (no account 9999)

-- Deferred FK for a re-parenting transaction (Postgres):
ALTER TABLE txns ALTER CONSTRAINT txns_account_id_fkey DEFERRABLE INITIALLY DEFERRED;
BEGIN;
  INSERT INTO txns (account_id, amount) VALUES (1, -10);  -- allowed now
  UPDATE accounts SET account_id = 2 WHERE account_id = 1; -- fix at commit
COMMIT;  -- FK verified at commit; consistent
```

## 16. Industry Usage
- **Finance**: `CHECK (balance >= 0)`, NOT NULL amounts, FK to accounts — PCI/SOX auditors verify constraints exist in the schema, not the app.
- **E-commerce**: order lines `ON DELETE CASCADE`, SKUs `UNIQUE`, inventory `CHECK (qty >= 0)` — the DB, not the microservice, is the integrity backstop.
- **SaaS identity**: `UNIQUE(email)` per tenant (composite unique) prevents account-takeover-by-duplicate; partial unique indexes enforce "one active subscription per user."
- **Postgres & MySQL** both implement the standard constraint set; **DynamoDB/Cassandra** largely *dropped* constraints for write scalability — a trade-off you'll be asked to justify ("how do you keep integrity without FK constraints?" — app-level + partition keys).
- **Data engineering** (dbt tests, Great Expectations) now *reimplements* constraint-style checks at the warehouse layer — because warehouses enforce few constraints, pipelines add tests as a substitute. Knowing the original DBMS constraints makes these substitutes obvious.

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 3 (Integrity Constraints).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 2.4 (Integrity Constraints).
- PostgreSQL Documentation, Constraints: https://www.postgresql.org/docs/current/ddl-constraints.html
- PostgreSQL Documentation, `ALTER TABLE ... NOT VALID`: https://www.postgresql.org/docs/current/sql-altertable.html
- MySQL Reference Manual, `FOREIGN_KEY_CHECKS`: https://dev.mysql.com/doc/refman/8.0/en/create-table-foreign-keys.html

## 18. Cheat Sheet
- 6 types: NOT NULL, UNIQUE, PK, FK, CHECK, domain/type.
- Entity integrity: PK non-null + unique. Referential integrity: FK = NULL or exists.
- ON DELETE: RESTRICT / CASCADE / SET NULL / SET DEFAULT.
- UNIQUE allows multiple NULLs; PK doesn't.
- Constraints are atomic, DB-enforced, app-independent.
- Index FK columns (Postgres doesn't auto-index) for deletes/cascades.
- `NOT VALID` + `VALIDATE` = zero-downtime constraint addition (Postgres).
- Deferred constraints: check at COMMIT for re-parenting transactions.

## 19. Quiz
1. Which constraint prevents orphan rows? a) CHECK b) FK c) NOT NULL d) DEFAULT → **b**
2. UNIQUE in Postgres allows: a) one NULL b) multiple NULLs c) no NULLs d) duplicates → **b**
3. ON DELETE CASCADE deletes: a) the parent only b) referencing children c) nothing d) the index → **b**
4. A CHECK constraint is: a) single-row Boolean b) cross-table c) procedural d) always deferred → **a**
5. `ADD CONSTRAINT ... NOT VALID` is for: a) faster writes b) zero-downtime constraint add c) dropping keys d) indexes → **b**
6. Violating a constraint in Postgres: a) ignored b) aborts the statement/transaction c) warns d) logs → **b**
7. Which action nulls the child's FK? a) CASCADE b) SET NULL c) RESTRICT d) NO ACTION → **b**
8. Constraints live in: a) app config b) the catalog c) WAL d) client cache → **b**
9. FK checks on child INSERT probe: a) the child table's PK b) the referenced unique index c) WAL d) OS → **b**
10. Constraint checks are: a) procedural b) declarative + engine-enforced c) manual d) app-level → **b**

## 20. Flashcards
- **Q: 6 constraint types?** → **A:** NOT NULL, UNIQUE, PK, FK, CHECK, domain/type.
- **Q: Why DB-enforced not app-enforced?** → **A:** DB is the single atomic choke point all writers share.
- **Q: ON DELETE actions?** → **A:** RESTRICT / CASCADE / SET NULL / SET DEFAULT.
- **Q: UNIQUE and NULLs?** → **A:** Multiple NULLs allowed (each distinct).
- **Q: What is a deferred constraint?** → **A:** FK/unique check postponed to COMMIT (re-parenting).
- **Q: NOT VALID constraint?** → **A:** Add without scanning old rows; validate later — zero downtime.
- **Q: Should FK columns be indexed?** → **A:** Yes — for parent deletes/cascades (Postgres doesn't auto-index).
- **Q: Constraint vs trigger?** → **A:** Declarative engine rule vs procedural event code.

## 21. Revision
Integrity constraints = declarative rules the DB enforces on every write: **NOT NULL, UNIQUE, PK (entity), FK (referential), CHECK, domain**. Entity integrity: PK non-null + unique. Referential: FK NULL or exists, with actions RESTRICT/CASCADE/SET NULL. KEY traps: UNIQUE allows multiple NULLs; FK must reference a unique key; index FK columns (Postgres won't); `NOT VALID` + `VALIDATE` for zero-downtime adds; deferred constraints for re-parenting. Interview moves: answer "why DB not app?" (single atomic choke point); design actions for ownership vs history (CASCADE for owned, SET NULL for history); explain the duplicate-email race (app check non-atomic → UNIQUE constraint + upsert); and state that MySQL `FOREIGN_KEY_CHECKS=0` speeds imports but risks orphans.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What are integrity constraints?" | 7 / 13 Q1 |
| "Why enforce in DB not app?" | 13 Q2 |
| "Entity vs referential integrity?" | 13 Q4 |
| "ON DELETE actions?" | 13 Q7-8 |
| "UNIQUE and NULLs?" | 13 Q10 |
| "Zero-downtime constraint add?" | 13 Q11 |
| "Index FK columns?" | 13 Q15 |
| "Constraint vs trigger?" | 13 Q13 |
