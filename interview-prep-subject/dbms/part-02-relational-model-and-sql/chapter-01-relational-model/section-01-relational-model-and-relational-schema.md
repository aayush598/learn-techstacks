# Part: Relational Model & SQL

> **TL;DR**: The relational model (Codd 1970) organizes data into relations (tables) with set semantics — order doesn't matter, rows are unique, links are by value — and SQL is the standard declarative language for expressing relational algebra queries over them.

## 1. Why Does This Exist?
This chapter exists because the relational model is the *foundation of SQL*, and SQL is the foundation of almost every database interview. It answers three things you must be able to state precisely: (1) **What is a relation?** — a set of tuples over a schema, with domains, where order is irrelevant and duplicates are impossible. (2) **What are keys?** — the minimal identifiers (candidate keys), the chosen one (primary key), and the linking mechanism (foreign key). (3) **What are the rules?** — integrity constraints (entity, referential, domain, user-defined) that keep data truthful. Get these right and every SQL question becomes easy; get them wrong and even simple joins produce nonsense answers. The model exists to give data *precise, provable semantics* — the reason you can reason about queries at all.

## 2. How Does It Work?
A database is a set of relations. Each relation has a **schema** (name + ordered attribute list with domains) and an **instance** (a set of tuples). Relations satisfy: (1) every tuple is unique (set semantics), (2) tuples are unordered, (3) attribute values are atomic *per domain* (at least in the normalized core), (4) each attribute has a domain of allowed values. **Keys**: a *superkey* is any set of attributes uniquely identifying tuples; a *candidate key* is a minimal superkey; the *primary key* is the chosen candidate key; a *foreign key* references another relation's primary key. **Constraints**: entity integrity (PK not null, unique), referential integrity (FK values must exist or be null), domain/check constraints, and user-defined business rules. Queries (relational algebra) combine relations via select, project, join, rename, union, set-difference, cartesian product.

## 3. When Is It Used?
- **Schema design**: deciding tables, columns, keys, and constraints for any new feature — the universal starting point of DB work.
- **SQL correctness**: knowing tuple/order semantics explains why `ORDER BY` is needed, why `DISTINCT` exists, why `NULL` behaves specially, and how joins produce results.
- **Interview screens**: "design the schema for a social network / e-commerce / ride-sharing" — keys + constraints are the core.
- **Normalization** (Part 03) is literally *defined* in terms of functional dependencies and keys from this chapter.
- **In production**: every `CREATE TABLE ... PRIMARY KEY (..) REFERENCES ..` is this chapter's theory made concrete; ORMs generate exactly these DDLs.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: records with pointers (network/hierarchical).** Rejected — navigational querying, no data independence (see Part 01 Section 03). Relational uses *value-based* links (FK) so joins are declarative and storage can change freely.
- **Alternative: sets without ordering rules.** Sets were chosen over ordered sequences *deliberately*: ordering is a presentation concern, not a data concern. If rows had a defined order, every storage change (adding an index, moving a page) would change query results. Set semantics = storage independence.
- **Alternative: allowing duplicate rows.** Rejected — a "bag" breaks identity: how would you update *one* of two identical rows? Sets force uniqueness via keys, giving every tuple identity.
- **Alternative: one big universal relation (no decomposition).** Rejected — redundancy + update anomalies; the model *prescribes* decomposition into relations joined by keys (which Part 03 formalizes as normalization).
- **Why NULLs at all?** Real data has missing values; the model admits "unknown" via NULL with three-valued logic — an imperfect but necessary compromise (debated endlessly; the alternative — no missing values — is unrealistic).

## 5. Intuition
Think of a relation as a **spreadsheet that remembers its own rules**: every row is a unique record (no two identical rows), rows have no inherent order (sorting is a *view*, not stored), every column has a type (you can't put text in a number column), and the first column(s) act as the row's ID. The key insight: **connections between spreadsheets are made by sharing a value** (the foreign key), not by drawing arrows. That single idea — "link by value, not by pointer" — is what makes relational data re-combinable in infinite ways without redesigning storage.

## 6. Real-World Analogy
A **library catalogue**: each card (tuple) has fixed fields (attributes) — title, author, ISBN, shelf. Every card is unique because of the ISBN (primary key). Cards sit in no particular order (set semantics); the catalogue staff sort them only for display. The "author" index is a *separate* relation linking author names to ISBNs — connected by the shared ISBN value, not by arrows on paper. When you search "all books by Salinger," the DBMS finds every ISBN matching the author, then looks those up in the catalogue — a join by value. Remove the "unique card" rule and you can't tell which copy to update. That's the relational model in physical form.

## 7. Formal Definition
(Elmasri & Navathe Ch. 3; Silberschatz Ch. 2; Codd 1970.)
- **Relation schema**: R(A₁, A₂, ..., Aₙ) where Aᵢ are attributes over domains Dᵢ.
- **Relation instance**: r(R) is a *set* of n-tuples, r ⊆ D₁ × D₂ × ... × Dₙ. Being a set: no duplicate tuples, no ordering.
- **Domain**: a set of atomic values with a data type (int, char, etc.). Atomic = indivisible in the basic model.
- **Degree**: number of attributes; **cardinality**: number of tuples.
- **Superkey**: a set of attributes whose values uniquely determine a tuple.
- **Candidate key**: a minimal superkey (no proper subset is a superkey).
- **Primary key**: the candidate key chosen to identify tuples; PK values must be non-null (entity integrity).
- **Foreign key**: a set of attributes whose values must either be NULL or match a primary/unique key value of the referenced relation (referential integrity).
- **Integrity constraints**: entity, referential, domain (check/type), and user-defined (assertions, triggers).
- **Relational algebra**: a set of closed operations over relations — σ (select), π (project), ⋈ (join), ρ (rename), ∪, −, ×, ∩, and aggregates.

## 8. Example
Schema:
```
STUDENT(sid INT PK, name TEXT, dept TEXT, gpa NUMERIC)
COURSE(cno TEXT PK, cname TEXT, credits INT)
ENROLL(sid INT FK→STUDENT, cno TEXT FK→COURSE, grade TEXT, PK(sid,cno))
```
Instances:
```
STUDENT = { (1,'Alice','CS',3.8), (2,'Bob','EE',3.2), (3,'Cara','CS',3.9) }
COURSE  = { ('CS101','Databases',4), ('EE200','Circuits',3) }
ENROLL  = { (1,'CS101','A'), (2,'CS101','B'), (3,'EE200','A') }
```
- `(1,2,3)` — superkey candidate; `{sid}` is the only candidate key; chosen PK = `sid`.
- `ENROLL.sid = 1` refers to STUDENT(1); inserting `(99,'CS101','A')` violates referential integrity (no student 99).
- `UPDATE ENROLL SET sid=1 WHERE sid=2` — allowed? Only if student 1 still exists; the FK enforces it.
- Query: "names of CS students in CS101": σ_CS(STUDENT) ⋈ ENROLL ⋈ σ_CS101(COURSE), then π_name.

## 9. Internal Working
1. **Design time**: analysts derive relations from requirements (entities → relations, relationships → FK/PK), choose candidate keys from functional dependencies, apply normalization (Part 03).
2. **DDL**: `CREATE TABLE` materializes the schema + constraints in the catalog; PK/UNIQUE constraints create unique indexes; FK constraints register the referential rule.
3. **Write time**: INSERT validates domain types, entity integrity (PK not null/unique), referential integrity (FK exists); enforcement is a catalog lookup + index probe (O(log n)).
4. **Read time**: SQL is translated to relational algebra operators; the optimizer plans joins using keys (PK↔FK index lookups); the executor applies select/project/join over rows.
5. **Semantics guarantee**: because relations are *sets*, operations are deterministic and storage-independent — the DBMS can reorder scans and joins freely (this is what makes optimization safe).

## 10. Time Complexity
- **Key lookup**: PK/FK with unique index — O(log_f n) (B+ tree) or O(1) (hash).
- **Unique check on insert**: O(log_f n) index probe.
- **Referential check on insert**: O(log_f n) on referenced table's index.
- **Join on PK=FK**: hash join O(n+m); index nested-loop O(n·log m); merge join O(n log n + m log m).
- **Set operations (union/diff)**: O(n+m) with hashing, O(n log n) with sort.
- **Cartesian product**: O(n·m) — the reason joins exist.

## 11. Advantages
- **Simple, uniform model**: one concept (relation) for all data; easy to learn and teach.
- **Declarative queries**: relational algebra gives SQL its what-not-how semantics; optimizers are provably safe because of set semantics.
- **Data independence**: no pointers/order assumptions → storage can change freely.
- **Strong integrity**: keys + constraints make invalid data hard to insert.
- **Set-based reasoning**: results are sets → combinable, optimizable, predictable.
- **Standard SQL**: one language across all relational DBMSs.

## 12. Disadvantages
- **NULL semantics**: three-valued logic makes `WHERE` and joins confusing; NULLs complicate keys and optimization.
- **Set-bag mismatch**: real SQL (and engines) actually allow duplicate rows (bag semantics) unless `DISTINCT`/PK forces a set — a leak between theory and practice.
- **No natural ordering/position**: "first row" is meaningless without `ORDER BY`; rank-by-position needs extra machinery.
- **Object impedance mismatch**: nested/recursive data doesn't map cleanly to flat tables (ORM pain).
- **Atomic-attribute assumption**: composite values need decomposition; very nested data is awkward (hence JSONB extensions).

## 13. Interview Questions
1. **Q: What is a relation?** A: A set of tuples over a schema of attributes with domains. Properties: no duplicate tuples, unordered rows, atomic attribute values per domain, each attribute typed. A relation ≈ a table, but with strict set semantics.
2. **Q: What is the difference between a relation schema and a relation instance?** A: Schema = the structure (name + attributes + domains + constraints), stable; instance = the current set of tuples, volatile. (Same schema/state distinction as the database as a whole.)
3. **Q: Why must a relation have no duplicate rows?** A: Because it's a *set*. Duplicates would break identity — you couldn't update or delete one specific copy, and results would lose the set-based properties that make optimization safe. (Real SQL is bag-based; `DISTINCT` and PK restore set behavior.)
4. **Q: Why is row order irrelevant in a relation?** A: Ordering is a presentation concern, not data. If order were meaningful, storage changes (indexes, page layout) could change results — destroying data independence. You need `ORDER BY` to see a deterministic order.
5. **Q: What is a superkey vs a candidate key vs a primary key?** A: Superkey = any attribute set that uniquely identifies tuples. Candidate key = a *minimal* superkey (no proper subset is a superkey). Primary key = the candidate key the designer picks as the tuple identifier.
6. **Q: Can a relation have more than one candidate key? Give an example.** A: Yes — e.g., an Employee relation with UNIQUE(emp_id) and UNIQUE(pan_no) (national tax id): both are candidate keys; the designer chooses one as PK, the other stays as a UNIQUE key.
7. **Q: What is a foreign key?** A: An attribute set in relation R referencing the primary key (or unique key) of relation S; each FK value must be NULL or exist in S. It's how relationships are represented — by value, not pointer.
8. **Q (tricky): Can a foreign key reference a non-primary key?** A: Yes — it must reference a *unique* key (a candidate key), not necessarily the PK. Most engines require a UNIQUE constraint on the referenced columns. Common gotcha: it must be a key, not just any column.
9. **Q: What is entity integrity?** A: The primary key's attributes cannot be NULL (they must identify a tuple) and must be unique. Violating it means a row has no identity — you couldn't reference or update it reliably.
10. **Q: What is referential integrity?** A: A foreign key value must either be NULL or match an existing primary/unique key value in the referenced relation. Prevents "orphan" references to non-existent rows.
11. **Q (scenario): What happens if you delete a referenced STUDENT row?** A: With FK constraints, the engine blocks deletion (RESTRICT/NO ACTION), cascades the delete (ON DELETE CASCADE), nulls the FK (SET NULL), or sets a default (SET DEFAULT) — configured when the FK is declared. Default in most DBs is to refuse.
12. **Q: What is a domain constraint vs a CHECK constraint?** A: Domain = the legal value *type/set* for an attribute (INT, VARCHAR(50)); CHECK is a general Boolean predicate (`gpa BETWEEN 0 AND 4`, `balance >= 0`). Domain is a special case of the broader CHECK idea.
13. **Q (tricky): Does a PRIMARY KEY constraint create an index?** A: Yes — the DBMS creates a unique index (B+ tree) to enforce uniqueness and speed lookups. Similarly UNIQUE creates a unique index; FK often creates a supporting index (though you usually add it manually).
14. **Q: What is the difference between a key and an index?** A: A key is a *logical* constraint (uniqueness/identity semantics); an index is a *physical* structure to speed access. A PK key forces a unique index; but you can index non-key columns. Keys define integrity; indexes define speed.
15. **Q: What is a candidate key and how do you find it from FDs?** A: Candidate key = minimal set of attributes whose closure covers all attributes. From FDs, start with attributes never on the RHS, add attributes and test closures until the whole relation is covered. (Full algorithm in Part 03.)
16. **Q (production): Why does the ENROLL table use a composite PK (sid, cno)?** A: Because the relationship is many-to-many — a student takes many courses, a course has many students. The pair (sid,cno) is the minimal unique identifier of one enrollment; also prevents duplicate enrollments.
17. **Q: What is the difference between a relation and a table in SQL practice?** A: In theory identical; in practice tables are bags (duplicates allowed) unless a key/UNIQUE/DISTINCT is present, and tables may have order-affecting storage. The model is the ideal; SQL is a slightly loose implementation.
18. **Q (scenario): You see duplicate rows in `SELECT` output from a table with no PK. Why?** A: The table is a bag (no PK → duplicates allowed). Add `DISTINCT` for the query, or add a PK/unique constraint if duplicates are *data* and must be prevented. This is the set-vs-bag distinction in action.
19. **Q: What is the degree and cardinality of a relation?** A: Degree = number of attributes (columns); cardinality = number of tuples (rows). A relation STUDENT with 4 columns, 100 rows has degree 4, cardinality 100.
20. **Q (hard): Can NULL be part of a primary key?** A: No — entity integrity forbids it: PK attributes must be non-null. NULL in a key would mean "row with unknown identity." UNIQUE constraints in most engines *do* allow multiple NULLs (each NULL distinct) — a classic trap.

## 14. Follow-Up Questions
1. **Q: What is the difference between a relation and a relationship?** A: A relation = the data structure (table); a relationship = the association between entities, represented by FKs between relations (or an associative table for many-to-many). Don't conflate the terms.
2. **Q: Why is SQL "bag-based" rather than set-based?** A: Practicality + performance: sets require deduplication (expensive sort/hash) on every operation; bags don't. `DISTINCT`, `UNION` (not `UNION ALL`) restore set semantics on demand. Engines optimized for bags.
3. **Q: What is a natural key vs a surrogate key?** A: Natural = real-world value (PAN/email/ISBN); surrogate = artificial (auto-increment `BIGSERIAL`/UUID). Surrogates are stable when natural keys change; natural keys avoid extra columns. Production schemas commonly use surrogate PKs + unique constraint on the natural key.
4. **Q: What is `ON DELETE CASCADE` and when is it dangerous?** A: It propagates deletes to referencing rows. Dangerous when referenced rows are valuable (orders of a customer) — accidental cascade can wipe history. Prefer RESTRICT/SET NULL for financial/history data.
5. **Q: Can two rows in a bag-behavior table be "equal"?** A: In SQL, row equality is defined by the query's output — without DISTINCT, "equal" rows coexist. That's exactly why `SELECT DISTINCT` and grouping exist. State it in terms of set-vs-bag semantics.

## 15. Coding Example
```sql
-- Full relational model in DDL
CREATE TABLE student (
  sid   INT PRIMARY KEY,                -- candidate key 1, chosen PK
  pan   VARCHAR(10) UNIQUE NOT NULL,    -- candidate key 2 (unique)
  name  TEXT NOT NULL,
  dept  TEXT CHECK (dept IN ('CS','EE','ME')),
  gpa   NUMERIC(3,2) CHECK (gpa BETWEEN 0 AND 4)
);

CREATE TABLE course (
  cno     TEXT PRIMARY KEY,
  cname   TEXT NOT NULL,
  credits INT CHECK (credits > 0)
);

CREATE TABLE enroll (
  sid   INT REFERENCES student(sid) ON DELETE CASCADE,
  cno   TEXT REFERENCES course(cno),
  grade TEXT,
  PRIMARY KEY (sid, cno)               -- composite key; dedupes enrollments
);

-- Set semantics in action
SELECT DISTINCT dept FROM student;      -- set: no duplicate depts
SELECT dept FROM student;               -- bag: depts repeat per row
INSERT INTO student VALUES (1,'P1','Alice','CS',3.8);   -- OK
INSERT INTO student VALUES (1,'P2','Bob','CS',3.5);     -- violates PK (duplicate sid)
INSERT INTO enroll VALUES (99,'CS101','A');             -- violates FK (no student 99)
```

## 16. Industry Usage
- **Every RDBMS schema** — Postgres, MySQL, Oracle, SQL Server — is this chapter's model in DDL: PKs, FKs, UNIQUE, CHECK constraints are the backbone of every production database.
- **Data modeling tools** (dbdiagram, dbt docs, SchemaSpy) render ER diagrams from exactly these key/constraint definitions.
- **ORM frameworks** (Hibernate, Prisma, Django) map classes → relations, with `@Id`, `@ManyToOne` = FK, `@JoinTable` = associative table — the model encodes the relational design.
- **Interview standard**: "design an e-commerce schema" = identify entities, choose keys, wire FKs — the exact skills of this chapter; companies (Amazon, Google, Stripe) screen on it.
- **Consistency guarantees** in microservices rely on DB-enforced FK/PK — because the DB is the only place integrity can be *enforced*, not just declared.

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 3 (Relational Model) & Ch. 5 (Relational Algebra).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 2 (Introduction to the Relational Model).
- Codd, E. F., "A Relational Model of Data for Large Shared Data Banks", CACM 13(6), 1970.
- Date, C. J., *An Introduction to Database Systems*, 8th ed.
- ISO/IEC 9075:2016 (SQL Standard, relational foundations).

## 18. Cheat Sheet
- Relation = set of tuples: no duplicates, no order, atomic values, typed domains.
- Schema (structure) vs instance (current rows).
- Superkey → candidate key (minimal) → PK (chosen); FK links by value.
- Entity integrity: PK non-null + unique. Referential integrity: FK = NULL or existing.
- Degree = #columns; cardinality = #rows.
- Relational algebra: σ select, π project, ⋈ join, ρ rename, ∪ − × ∩.
- SQL is bag-based; DISTINCT/PK/UNION restore set semantics.
- PK creates a unique index; key = logical constraint, index = physical structure.

## 19. Quiz
1. A relation is a: a) bag of rows b) set of tuples c) list of records d) tree → **b**
2. Which can be NULL? a) PK part b) FK (if nullable) c) superkey d) none → **b**
3. A candidate key is: a) any unique column b) minimal superkey c) the biggest index d) a FK → **b**
4. Degree of STUDENT(id,name,gpa) is: a) 3 b) rows c) 0 d) 1 → **a**
5. Referential integrity prevents: a) duplicate PKs b) orphan FKs c) NULLs d) slow joins → **b**
6. `SELECT dept FROM student` without DISTINCT returns: a) set b) bag c) tree d) sorted list → **b**
7. Entity integrity demands PK: a) indexed b) non-null c) small d) foreign → **b**
8. Links between relations are by: a) pointers b) shared values (FK) c) OIDs d) offsets → **b**
9. Deleting a referenced row with `RESTRICT` will: a) delete children b) refuse c) set NULL d) ignore → **b**
10. A PK constraint in the engine: a) creates a unique index b) adds memory c) compresses data d) changes disks → **a**

## 20. Flashcards
- **Q: What is a relation?** → **A:** A set of tuples over a schema — no duplicates, no order.
- **Q: Superkey vs candidate vs primary key?** → **A:** Unique set → minimal unique set → chosen one.
- **Q: What is a foreign key?** → **A:** Attribute set referencing another relation's unique key; NULL or must exist.
- **Q: Entity integrity?** → **A:** PK attributes are non-null and unique.
- **Q: Referential integrity?** → **A:** FK value is NULL or matches an existing referenced key.
- **Q: Why no order in a relation?** → **A:** Order is presentation; storage independence requires sets.
- **Q: Set vs bag?** → **A:** Sets forbid duplicates; SQL bags allow them (DISTINCT restores).
- **Q: Degree vs cardinality?** → **A:** #attributes vs #tuples.

## 21. Revision
The relational model: relations = *sets* of tuples (no dups, no order, atomic typed values). Keys: superkey (unique) → candidate (minimal superkey) → PK (chosen, non-null, creates unique index); FK links by *value*. Constraints: entity (PK non-null+unique), referential (FK exists or NULL), domain/CHECK. Algebra ops: σ π ⋈ ρ ∪ − ×. SQL is *bag* semantics (DISTINCT/PK/UNION restore set behavior). Interview moves: define relation precisely with the 4 properties; walk superkey→candidate→PK; answer "can FK reference non-PK?" (yes, any unique key); explain composite PK for many-to-many; state the bag-vs-set trap with `SELECT dept` vs `SELECT DISTINCT dept`. Always tie keys to constraints to indexes.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a relation / table?" | 7 / 13 Q1 |
| "Schema vs instance?" | 13 Q2 |
| "Superkey/candidate/PK?" | 13 Q5-6 |
| "What is a foreign key?" | 13 Q7-8 |
| "Entity vs referential integrity?" | 13 Q9-10 |
| "Why no duplicates / no order?" | 13 Q3-4 |
| "Set vs bag semantics?" | 13 Q17-18 |
| "Design a many-to-many schema" | 13 Q16 |
