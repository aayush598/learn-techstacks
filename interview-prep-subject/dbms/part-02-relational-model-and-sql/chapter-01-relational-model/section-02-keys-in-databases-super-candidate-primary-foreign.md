# Keys in Databases: Super, Candidate, Primary, Foreign

> **TL;DR**: Keys are the mechanism that gives every row an identity (superkey → candidate → primary) and connects relations together (foreign key) — without keys, tuples can't be identified, referenced, or checked for integrity.

## 1. Why Does This Exist?
In a *set*, every tuple must be identifiable — but nothing in raw data says "these two rows are the same person" unless some attribute combination does. Keys exist to answer four needs: (1) **Identity** — a minimal attribute set that uniquely pins a row, so updates/deletes know exactly which tuple they hit. (2) **Integrity** — preventing duplicate rows (entity integrity) and orphan references (referential integrity). (3) **Navigation** — foreign keys turn *relationships* into queryable values, replacing the pointers of pre-relational models. (4) **Optimization** — key constraints create indexes, giving O(log n) lookups. In interviews, keys are where "design a schema" questions begin: no candidate-key reasoning, no correct design.

## 2. How Does It Work?
From the attribute set of a relation, some subsets are **superkeys** (they uniquely determine tuples). Among superkeys, the ones where *no attribute can be removed* are **candidate keys** (minimal superkeys). The designer picks one candidate key as the **primary key** (usually the smallest/stable one); the rest stay as UNIQUE keys. A **foreign key** in relation R is a set of attributes matching a unique key of relation S — it links each R-tuple to a specific S-tuple. The DBMS enforces all of this: PK/UNIQUE → unique index + non-null rule; FK → referential checks on insert/update/delete. Keys are declared in DDL (`PRIMARY KEY`, `UNIQUE`, `REFERENCES`) and become the spine of indexes, joins, and constraint enforcement.

## 3. When Is It Used?
- **Schema design**: picking PKs and FKs for every table is the first step of any modeling exercise (interview or production).
- **Many-to-many relationships**: associative tables use a *composite PK* of the two FKs.
- **Deduplication**: a natural unique key (email, PAN) prevents duplicate customers even if the surrogate PK would allow them.
- **Joins**: `ON a.id = b.emp_id` works fast precisely because key constraints back them with indexes.
- **Data quality**: FK constraints stop orphaned rows; CHECK + UNIQUE stop nonsense duplicates.
- **Referential actions**: `ON DELETE CASCADE / SET NULL / RESTRICT` decide what happens to children when a parent is deleted.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: "everything is a key" (treat whole row as identifier).** Rejected: two identical rows would be indistinguishable (can't update one), and identity wouldn't survive adding/removing columns. Minimal keys keep identity stable.
- **Alternative: physical rowids/pointers (network model).** Rejected: breaks data independence and joins by value (the relational advantage). Keys let you reference by *meaningful value*, and they survive storage reorganization.
- **Alternative: allow NULLs in keys.** Rejected for PK: a NULL key is "no identity," and uniqueness with NULL is ill-defined (engines treat NULLs as distinct) — hence entity integrity forbids it.
- **Alternative: no keys, enforce uniqueness app-side.** Rejected: two app servers would race; the DB is the only place integrity is *atomically enforceable* (constraints + unique indexes).
- **Why multiple key types (super/candidate/primary)?** Because design needs the vocabulary to reason about *alternatives*: find all minimal identifiers, then pick one as PK. It's a design methodology, not ceremony.

## 5. Intuition
A key is a **national ID for a row**. A superkey is *any* set of identifiers that could work ("email + phone + SSN" — unique but bloated). A candidate key is the *smallest* set that works ("SSN" alone — you can't drop anything). The primary key is the one ID you decide is official. The foreign key is "the other table's ID written into my table" — a reference, like your colleague writing your employee number on a form. And the rules are simple: nobody may have the same official ID (entity integrity), and any employee number you cite must belong to someone real (referential integrity).

## 6. Real-World Analogy
A **driver's license + vehicle registry**: every driver has a unique license number (primary key). A license number is also printed on their vehicle registration, insurance, and traffic tickets (foreign keys) — each agency can look up the driver by that shared number (join by value). The registry can't issue two licenses with the same number (entity integrity), and a registration that cites a license number must correspond to a real license (referential integrity). If an officer copies your *name alone* (a superkey that's not minimal — duplicate names exist), it fails to identify you uniquely — so the system insists on the minimal identifier, the license number.

## 7. Formal Definition
Let R(A₁,...,Aₙ) be a relation. (Elmasri & Navathe Ch. 3; Silberschatz Ch. 2.3.)
- **Superkey**: K ⊆ {A₁,...,Aₙ} such that in any legal instance, no two tuples have the same value on K. (K "determines" the tuple.)
- **Candidate key**: a superkey K such that no *proper subset* of K is a superkey (minimality).
- **Primary key**: the candidate key selected to identify tuples; must be non-null and unique (entity integrity).
- **Unique key**: a candidate key not chosen as PK; enforced as UNIQUE (nullable or not).
- **Foreign key**: FK ⊆ R such that values of FK must be NULL or match a candidate key value in some referenced relation S (referential integrity). (Note: FK references a *unique* key, which may be the PK or another candidate key.)
- **Composite key**: a key with more than one attribute (e.g., (sid, cno) in an enrollment).
- **Surrogate vs natural key**: artificial (auto-increment/UUID) vs meaningful (email/ISBN) identifier.

## 8. Example
```
EMPLOYEE(emp_id INT PK, pan_no VARCHAR(10) UNIQUE, email VARCHAR UNIQUE, name TEXT, dept_id INT FK→DEPT)
DEPT(dept_id INT PK, dept_name TEXT)
```
- Superkeys of EMPLOYEE: {emp_id}, {pan_no}, {email}, {emp_id, pan_no}, {pan_no, email}, {emp_id, name, ...} etc.
- Candidate keys: {emp_id}, {pan_no}, {email} — each minimal.
- PK chosen: {emp_id}; the other two remain UNIQUE constraints.
- FK: dept_id must be a value present in DEPT.dept_id (or NULL if the employee has no department yet).
- Enforcing: `INSERT (100,'PAN1','a@x','Alice',99)` → FK check fails (dept 99 missing) → rejected.

## 9. Internal Working
1. **DDL**: `PRIMARY KEY (emp_id)` → catalog records the key; engine creates a *unique B+ tree index* on `emp_id`; the PK columns get NOT NULL.
2. **UNIQUE (pan_no)** → a second unique index (NULLs allowed, multiple).
3. **FOREIGN KEY (dept_id) REFERENCES DEPT(dept_id)** → catalog stores the rule; the referenced column must itself have a unique index (its PK).
4. **On INSERT/UPDATE of EMPLOYEE**: entity check (emp_id unique via index probe, O(log n)); FK check (probe DEPT's unique index for dept_id, O(log n)).
5. **On DELETE/UPDATE of DEPT**: engine applies the referential action (RESTRICT → block if children exist; CASCADE → delete children; SET NULL → null the FKs) — each child operation is an indexed lookup.
6. **Join**: `EMPLOYEE ⋈ DEPT` on dept_id uses the two unique indexes (index nested-loop) or hash — keys make the join both semantically correct and fast.

## 10. Time Complexity
- **Key uniqueness check** (insert/update): O(log_f n) via unique index.
- **PK lookup**: O(log_f n) (B+ tree) or O(1) (hash) — the reason `WHERE pk = ?` is the fastest access path.
- **FK existence check**: O(log_f m) on the referenced table's unique index.
- **Referential action on parent delete**: O(k·log m) for k children (each child found by index).
- **Join on key**: hash join O(n+m); index nested-loop O(n·log m).
- **Key derivation from FDs** (design-time, Part 03): closure computation is polynomial in attributes.

## 11. Advantages
- **Unambiguous identity**: updates/deletes always target exactly one tuple.
- **Integrity by construction**: duplicates and orphans are impossible to insert.
- **Fast joins & lookups**: key constraints automatically create indexes.
- **Data independence**: identity is by *value*, so storage can be reorganized freely.
- **Design clarity**: candidate-key analysis reveals all viable identifiers before committing to a PK.
- **Referential actions**: parent/child lifecycles controlled declaratively.

## 12. Disadvantages
- **Key selection is hard**: choosing the wrong PK (volatile or too wide) causes migration pain.
- **Composite keys are verbose**: every child must repeat all columns; joins grow; surrogate keys often simpler.
- **Natural keys leak/change**: an email-based PK breaks when the email changes (with cascading consequences).
- **NULL semantics**: UNIQUE allows multiple NULLs (each distinct), which surprises people; partial indexes exist to fix it.
- **Index overhead**: each key = one index; many keys = write slowdown + storage cost.

## 13. Interview Questions
1. **Q: Define superkey, candidate key, primary key.** A: Superkey = any attribute set that uniquely identifies tuples. Candidate key = a minimal superkey (no proper subset is unique). Primary key = the chosen candidate key — non-null, unique, and backed by a unique index.
2. **Q: How do you find all candidate keys of a relation given its FDs?** A: Compute attribute closures; a candidate key is a minimal set whose closure covers all attributes. (Given FDs, this is Part 03's algorithm — attributes never on any RHS are mandatory in every key.)
3. **Q: What is a foreign key?** A: An attribute set referencing a unique key (usually the PK) of another relation; values must be NULL or match an existing referenced value. It represents a relationship by value.
4. **Q (tricky): Can a foreign key reference a non-primary, non-unique column?** A: No — it must reference a column set with a UNIQUE constraint (a candidate key). Standard engines reject FK references to columns without a unique index. Common interview trap.
5. **Q: What is the difference between PRIMARY KEY and UNIQUE?** A: Both enforce uniqueness and create unique indexes; PK also forbids NULLs and there's exactly one per table; UNIQUE allows NULLs (multiple) and you can have many. (Some engines treat the PK as the clustered key too.)
6. **Q: What is a composite key? When would you use one?** A: A key of multiple attributes. Classic case: the many-to-many associative table ENROLL(sid, cno) — (sid, cno) is the minimal unique identifier of one enrollment; it also deduplicates.
7. **Q (scenario): Design keys for Orders and OrderItems.** A: Order(order_id PK, customer_id FK, total); OrderItem(order_id FK, item_no, product_id FK, qty, PK(order_id, item_no)). Composite PK identifies one line; order_id FK gives the parent; referential action ON DELETE CASCADE for lines.
8. **Q: What is entity integrity and which key enforces it?** A: PK attributes cannot be NULL and must be unique — every tuple has identity. Enforced by the PK constraint (NOT NULL + unique index).
9. **Q: What is referential integrity and which key enforces it?** A: FK values must be NULL or exist in the referenced unique key — no orphan references. Enforced by the FK constraint on insert/update/delete.
10. **Q (production): Why use a surrogate key (auto-increment/UUID) over a natural key?** A: Stability — natural keys change (email, phone) and cascade; surrogates never change, are compact, and simplify FKs. Keep the natural value as a UNIQUE key. UUIDs help distributed inserts; BIGSERIAL is compact for single-node.
11. **Q (tricky): Two tables have the same column `id` as PK. Does that make them related?** A: No — sharing a *name* means nothing; a relationship requires a *foreign key constraint* or join by value. Identical names are coincidence unless a FK declares the dependency.
12. **Q: What does `ON DELETE CASCADE` vs `SET NULL` do?** A: CASCADE deletes referencing rows too; SET NULL sets the FK to NULL (requires nullable FK). Choose per semantics: cascade for line items (owned), SET NULL for optional references (manager).
13. **Q: Can a table have two primary keys?** A: No — at most one primary key. But it can have many UNIQUE (candidate) keys. People say "composite PK" for multi-column PK; that's one key with multiple columns, not two keys.
14. **Q (scenario): You accidentally allowed duplicate customers. Which key would have prevented it?** A: A UNIQUE constraint on the natural key (e.g., UNIQUE(email)) or a natural-key-based PK. Surrogate PKs alone never dedupe on business attributes — the classic production miss.
15. **Q: What is the relationship between a key and an index?** A: A key is a logical constraint (identity/uniqueness); an index is a physical structure for speed. Every PK/UNIQUE key *creates* an index; but you can index non-key columns. Keys are semantics, indexes are performance.
16. **Q (hard): Is the set {emp_id, pan_no} a candidate key of EMPLOYEE?** A: No — it's a superkey but *not minimal*: you can remove emp_id and pan_no alone still uniquely identifies (it's a candidate key). Minimality is the test; a candidate key must have no proper subset that's a superkey.
17. **Q: What is a weak entity and what does it mean for keys?** A: A weak entity has no key of its own — it's identified by a partial key plus the owner's PK (e.g., OrderItem is identified by (order_id, item_no)). In relational terms its PK includes the parent FK.
18. **Q (production): Should FK columns be indexed?** A: Usually yes — FKs are join/delete paths; without an index, cascades and joins become scans. Many engines don't auto-create FK indexes; add them deliberately (Postgres doesn't auto-index FK columns).
19. **Q: What happens when you update a PK value referenced by FKs?** A: By default (NO ACTION/RESTRICT) the update is refused if children reference it. ON UPDATE CASCADE propagates the change to children. In practice, surrogate PKs make PK updates vanishingly rare.
20. **Q: Can a foreign key be NULL and what does it mean?** A: Yes — NULL FK = "no reference yet" (e.g., employee not yet assigned a dept). It's semantically different from an invalid value. Note NULLs aren't checked against the referenced table (they skip the check).

## 14. Follow-Up Questions
1. **Q: What is a "candidate key" from a functional-dependency perspective?** A: A set X whose closure X⁺ = all attributes, with no proper subset also covering all attributes. The definition is FD-driven; Part 03 makes it computational.
2. **Q: When should you use a UUID vs an auto-increment PK?** A: UUID for distributed/multi-node inserts (no coordination, no leaks) at the cost of 16 bytes + random index insert pattern; BIGSERIAL for compact, ordered, single-node ids. DBs now have UUIDv7 for time-ordered UUIDs.
3. **Q: Can you join on a non-key column?** A: Yes, SQL allows any join predicate — but without a key/index backing it, it's a hash/merge over scans, and semantically it may not identify a unique parent. Keys make joins *both* correct and fast.
4. **Q: What is the difference between a key and a constraint?** A: A key is a specific *kind* of constraint (uniqueness/identity); constraints also include CHECK, NOT NULL, and domain rules. Keys are the identity-focused subset.
5. **Q: What is an "alternate key"?** A: A candidate key not chosen as the PK (e.g., pan_no, email above). Enforced as UNIQUE. Older textbooks use this term; interviewers may too — recognize it.

## 15. Coding Example
```sql
CREATE TABLE dept (
  dept_id   INT PRIMARY KEY,
  dept_name TEXT UNIQUE NOT NULL          -- alternate key (candidate)
);

CREATE TABLE employee (
  emp_id   BIGSERIAL PRIMARY KEY,          -- surrogate PK
  pan_no   VARCHAR(10) UNIQUE NOT NULL,    -- natural candidate key
  email    VARCHAR(255) UNIQUE,            -- another candidate key
  name     TEXT NOT NULL,
  dept_id  INT REFERENCES dept(dept_id) ON DELETE SET NULL,  -- FK
  manager_id INT REFERENCES employee(emp_id)                 -- self-referencing FK
);

-- Composite key: many-to-many via associative table
CREATE TABLE project (
  pno INT PRIMARY KEY, pname TEXT
);
CREATE TABLE assignment (
  emp_id INT REFERENCES employee(emp_id) ON DELETE CASCADE,
  pno    INT REFERENCES project(pno)      ON DELETE CASCADE,
  hours  NUMERIC,
  PRIMARY KEY (emp_id, pno)                -- composite PK = dedupe
);

-- Enforcement demos
INSERT INTO dept VALUES (1, 'Engineering'), (2, 'Sales');
INSERT INTO employee (emp_id, pan_no, email, name, dept_id)
  VALUES (1, 'PAN1', 'a@x', 'Alice', 1);
INSERT INTO employee (emp_id, pan_no, email, name, dept_id)
  VALUES (2, 'PAN2', 'b@x', 'Bob', 99);     -- ERROR: FK violation (dept 99)
INSERT INTO employee (emp_id, pan_no, email, name, dept_id)
  VALUES (3, 'PAN1', 'c@x', 'Cara', 1);     -- ERROR: unique violation (PAN1)
DELETE FROM dept WHERE dept_id = 1;          -- OK? sets Alice's dept_id NULL
```

## 16. Industry Usage
- **Every production schema** is key-driven: Shopify's orders/lines, Stripe's customers/invoices, Uber's trips — composite PKs for line items, FK cascades for ownership trees.
- **Postgres** enforces keys with unique B+ tree indexes (`pg_constraint` records them); `ON CONFLICT DO UPDATE` (upsert) keys off PK/UNIQUE — key choice determines what "conflict" means.
- **MySQL InnoDB** treats the PK as the clustered index (rows physically ordered by PK) — PK choice *is* the physical layout decision.
- **dbt/data warehouses** use surrogate keys (`dbt_utils.surrogate_key`) to dedupe event streams — natural-key dedup without leaking PII.
- **Distributed systems** (Cassandra, DynamoDB) replaced the PK with the *partition key* — the single most important design choice in NoSQL — proving key thinking is universal, not just relational.

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 3 (Relational Model & Constraints).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 2 (Keys, Integrity Constraints).
- Date, C. J., *An Introduction to Database Systems*, 8th ed., Ch. on Keys.
- PostgreSQL Documentation, Constraints: https://www.postgresql.org/docs/current/ddl-constraints.html
- MySQL Reference Manual, Constraint FK: https://dev.mysql.com/doc/refman/8.0/en/create-table-foreign-keys.html

## 18. Cheat Sheet
- Superkey = uniquely identifies; candidate = minimal superkey; PK = chosen candidate; FK = reference by value.
- Entity integrity: PK non-null + unique. Referential integrity: FK = NULL or exists.
- PK/UNIQUE each create a unique index; PK = NOT NULL, one per table.
- Composite key: multi-column key — canonical for many-to-many associative tables.
- FK must reference a UNIQUE key (PK or candidate); it can be NULL.
- Surrogate (auto-inc/UUID) vs natural key (email/PAN); both valid, keep natural as UNIQUE.
- ON DELETE: RESTRICT/NO ACTION, CASCADE, SET NULL, SET DEFAULT.
- Key = logical constraint; index = physical structure.

## 19. Quiz
1. A minimal superkey is a: a) PK b) candidate key c) FK d) index → **b**
2. Which is a candidate key of Employee(emp_id, pan_no, email)? a) {emp_id,pan_no} b) {emp_id} c) {name} d) {pan_no,email} → **b**
3. {emp_id, pan_no} is: a) candidate key b) superkey but not candidate c) FK d) not a key → **b**
4. A foreign key must reference: a) any column b) a UNIQUE key c) a text column d) an index → **b**
5. Entity integrity says PK: a) may be NULL b) non-null + unique c) auto-increment d) indexed only → **b**
6. Multiple NULLs are allowed in: a) PK b) UNIQUE (in most engines) c) neither d) FK only → **b**
7. Deleting a parent row with CASCADE: a) blocks b) deletes children c) sets NULL d) ignores → **b**
8. Surrogate key is best when: a) natural key changes b) data is tiny c) no index d) read-only → **a**
9. A composite PK on (sid,cno) prevents: a) slow queries b) duplicate enrollments c) NULLs d) joins → **b**
10. Keys create: a) WAL files b) indexes c) tables d) triggers → **b**

## 20. Flashcards
- **Q: Superkey vs candidate key?** → **A:** Any unique set vs a *minimal* unique set.
- **Q: PK vs UNIQUE?** → **A:** PK = non-null, one per table; UNIQUE allows NULLs, many allowed.
- **Q: What is a FK?** → **A:** Attribute set referencing another table's UNIQUE key; NULL or must exist.
- **Q: Can FK reference a non-unique column?** → **A:** No — must reference a candidate/UNIQUE key.
- **Q: When a composite PK?** → **A:** Many-to-many associative tables — (sid, cno).
- **Q: ON DELETE CASCADE vs SET NULL?** → **A:** Delete children vs null the FK (nullable only).
- **Q: Surrogate vs natural key?** → **A:** Artificial (auto-inc/UUID) vs meaningful (email/ISBN).
- **Q: Key vs index?** → **A:** Logical constraint vs physical structure; keys create indexes.

## 21. Revision
Keys = identity + integrity + navigation. **Superkey** (any unique set) → **candidate key** (minimal) → **PK** (chosen, non-null, unique, creates index). **FK** references a UNIQUE key, may be NULL, enforces no-orphans. Constraints: entity (PK non-null+unique), referential (FK exists/NULL). Actions: RESTRICT/CASCADE/SET NULL. Practical: surrogate PK + natural key as UNIQUE; composite PK for M:N; FK indexes added manually (Postgres). Interview moves: find candidate keys from FDs (closure); answer "can FK reference non-PK?" (yes, any unique key); explain composite key dedup; state MySQL clusters on PK (physical) vs Postgres doesn't; and always convert key choice → index existence → join speed.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Superkey/candidate/PK definitions" | 7 / 13 Q1 |
| "Find candidate keys from FDs" | 13 Q2 |
| "Can FK reference non-PK?" | 13 Q4 |
| "PK vs UNIQUE?" | 13 Q5 |
| "Composite key for M:N?" | 13 Q6 / 9 |
| "ON DELETE CASCADE vs SET NULL?" | 13 Q12 |
| "Surrogate vs natural key?" | 13 Q10 |
| "Key vs index?" | 13 Q15 |
