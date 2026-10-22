# Schema, Keys and Indexes — The DBMS Theory Core

> Section 3 · DBMS & SQL · DBMS Theory, Keys, Indexes & Views · _Estimated reading time: 12 min_
> **Prerequisite:** [SQL Basics: DDL & DML](../01-SQL-Basics-DDL-DML/01-concepts/01-ddl-dml-anatomy.md)

## In one sentence

**Three-level schema = how the DBMS is layered; keys = how rows are identified and related;
indexes = how rows are found; views = how rows are presented.**

## Why the pre-test tests this

- "DBMS theory" is 1–2 of the 10 DBMS questions and it is the broadest archetype: schema levels,
  keys, cardinality, indexes, views, and the DBMS-vs-file-system comparison.
- The questions are recall, not computation. If you have read the list once, you get them right.
- Rahul's gap here is **vocabulary in English** — the definitions are hard to read cold.

## Core concept

### 1. The three-level schema (ANSI/SPARC)

```
┌─────────────────────────────────────────────┐
│  EXTERNAL level  (view level)               │  ← what each user sees
│  Views, external schemas, user programs     │
├─────────────────────────────────────────────┤
│  CONCEPTUAL level (logical level)            │  ← what the whole community sees
│  Tables, keys, constraints, relationships    │
├─────────────────────────────────────────────┤
│  INTERNAL level (physical level)             │  ← how it is stored
│  Files, pages, indexes, access paths        │
└─────────────────────────────────────────────┘
```

| Level | Describes | Users |
|---|---|---|
| **External** | A view of the data for a specific user or application | End users |
| **Conceptual** | The global logical structure — all tables, keys, constraints, relationships | The whole organisation |
| **Internal** | Physical storage — files, blocks, indexes, access paths, compression | The DBMS itself |

**Data independence** = you can change one level without changing the level above it.

| Type | What changes | What stays the same | Level affected |
|---|---|---|---|
| **Logical data independence** | The **conceptual** schema (add a table, split a table, add a column) | The external schema — user programs and views | Conceptual |
| **Physical data independence** | The **internal** schema (new index, file layout, partitioning) | The conceptual schema | Internal |

**How they are achieved**

| Technique | Enables |
|---|---|
| **Views** | Logical data independence — a view hides the restructure |
| **Logical data independence** | Views + the mapping between external and conceptual |
| **Physical data independence** | The mapping between conceptual and internal; indexes and access paths |

**The data dictionary / catalogue** sits beside the three levels and stores the metadata: schema
definitions, indexes, constraints, statistics, permissions.

### 2. The data languages

| Category | Full name | Commands | Purpose |
|---|---|---|---|
| **DDL** | Data Definition Language | `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME` | Define and change structure |
| **DML** | Data Manipulation Language | `INSERT`, `UPDATE`, `DELETE`, `MERGE` | Change data |
| **DQL** | Data Query Language | `SELECT` | Read data |
| **DCL** | Data Control Language | `GRANT`, `REVOKE` | Permissions |
| **TCL** | Transaction Control Language | `COMMIT`, `ROLLBACK`, `SAVEPOINT` | Transaction control |

| Category | Changes schema? | Changes data? |
|---|---|---|
| DDL | ✅ Yes | ❌ No |
| DML | ❌ No | ✅ Yes |
| DQL | ❌ No | ❌ No |
| DCL | ❌ No | ❌ No |
| TCL | ❌ No | ❌ No (but controls data changes) |

**DDL is auto-committed in every mainstream DBMS** — a `CREATE TABLE` cannot be rolled back
(though `DROP TABLE` can be protected by a safety mode in MySQL).

### 3. Keys — the whole family

| Key | Definition | In the fixture |
|---|---|---|
| **Superkey** | Any attribute set that determines all attributes | `{cust_id}`, `{cust_id, cust_name}` |
| **Candidate key** | A **minimal** superkey | `cust_id` |
| **Primary key** | The candidate key you chose | `cust_id` |
| **Alternate key** | A candidate key you did **not** choose as primary | `email` (if unique) |
| **Composite key** | A key made of **two or more** attributes | `(student_id, course_id)` in enrollments |
| **Foreign key** | An attribute that references another table's primary key | `orders.cust_id` → `customers.cust_id` |
| **Natural key** | A real-world attribute with business meaning, used as a key | `email`, `aadhaar_no` |
| **Surrogate key** | A system-generated key with no business meaning | `cust_id` when it is just a number |
| **Partial key** | Part of a composite key, not a key by itself | `student_id` in `(student_id, course_id)` |
| **Unique key** | Enforces uniqueness but allows `NULL`s (in MySQL) | — |

**Natural vs surrogate**

| | Natural key | Surrogate key |
|---|---|---|
| Meaning | Business meaning (`email`) | No meaning (`cust_id`) |
| Changes | Can change (people change emails) | Never changes |
| Size | Often wide | Always narrow |
| Joins | Wide | Fast |
| Use | Reference tables, external data | Transaction tables |

### 4. Referential integrity

A **foreign key** must either match an existing primary key value in the parent table, or be `NULL`.

| `ON DELETE` action | Effect |
|---|---|
| `CASCADE` | Delete the matching parent rows too |
| `SET NULL` | Set the child's FK to `NULL` |
| `RESTRICT` | Refuse the delete immediately (checked before) |
| `NO ACTION` | Refuse the delete (checked at end of statement) |
| `SET DEFAULT` | Set the child's FK to its default value |

```sql
ALTER TABLE orders
  ADD CONSTRAINT fk_orders_cust
  FOREIGN KEY (cust_id) REFERENCES customers(cust_id)
  ON DELETE CASCADE
  ON UPDATE CASCADE;
```

**Orphan rows** are rows whose FK points at a parent that no longer exists. FK constraints prevent
them.

**Self-referencing FK:** `employees.manager_id → employees.emp_id`. On the fixture, employees 4 and
5 have `manager_id = NULL` (they are top-level) and employees 1, 2 report to 4 and 3, 6 report to
5.

### 5. ER model and cardinality

| Term | Meaning |
|---|---|
| **Entity** | A real-world thing worth storing (`Customer`, `Order`) |
| **Strong entity** | Has its own key |
| **Weak entity** | **No key of its own** — identified only through its owner (`Order_Line` via `Order`) |
| **Attribute** | A property of an entity |
| **Relationship** | A meaningful association between entities |
| **Identifying relationship** | The relationship that gives a weak entity its identity |
| **Recursive relationship** | An entity related to itself (`Employee` manages `Employee`) |

**Attribute types**

| Type | Meaning | Example |
|---|---|---|
| **Simple / atomic** | One value | `cust_name` |
| **Composite** | Made of parts | `cust_name` = first + last |
| **Derived** | Computed from other data | `age` from `dob`; `order_total` from line items |
| **Multivalued** | Many values | `cust_phone` |
| **Key attribute** | Identifies the entity | `cust_id` |

**Cardinality**

| Relationship | Meaning | Fixture example |
|---|---|---|
| **1:1** | One entity to one entity | `Employee` ↔ `ParkingSpot` |
| **1:N** | One entity to many entities | `Customer` 1 → N `Order`; `Department` 1 → N `Employee` |
| **M:N** | Many to many | `Student` M ↔ N `Course` |

**Participation**

| Type | Meaning | Fixture example |
|---|---|---|
| **Total** | Every entity **must** participate | Every `Order` must have a `Customer` |
| **Partial** | Entities **may** participate | A `Customer` may have zero orders (Vikram, 105) |

**M:N must be resolved** by introducing a junction/associative table with a composite key:
`ENROLLMENT(student_id, course_id, enrolled_on)`.

### 6. Indexes

An index is a **separate lookup structure** that maps key values to row locations, so the DBMS can
find matching rows without scanning the whole table.

| Type | Structure | Best for |
|---|---|---|
| **B-tree** | Balanced tree | Range scans, `=`, `<`, `>`, `BETWEEN`, `ORDER BY`, prefix search |
| **Hash** | Hash table | Exact `=` matches only, very large tables, high-cardinality columns |
| **Bitmap** | Bit array per key value | Low-cardinality columns, very large tables, data warehouse bitmaps |
| **Full-text** | Inverted index | Natural-language text search |
| **Clustered** | Stores the **rows** in index order | Range scans, one clustered index per table (InnoDB: the PK) |
| **Non-clustered** | Stores **pointers** to rows | Additional lookup paths, covering indexes |

**Primary vs secondary index**

| | Primary index | Secondary index |
|---|---|---|
| Built on | The primary key | Any other column |
| In InnoDB | It **is** the clustered index | Separate structure with row pointers |
| Uniqueness | Unique | May or may not be |

**Dense vs sparse**

| | Dense | Sparse |
|---|---|---|
| Entry per record | ✅ Every record has an entry | Only some records |
| Lookup | Direct | Must search then scan |
| Space | More | Less |

**Key concepts**

| Concept | Meaning |
|---|---|
| **Selectivity** | `distinct values / total rows` — how many rows an index narrows to. Higher is better |
| **Composite index** | Index on `(a, b)` — usable with `a`, or `a` AND `b`, but **not** `b` alone (**leftmost prefix rule**) |
| **Covering index** | The index contains every column the query needs → no table lookup |
| **Index selectivity** | Low selectivity (few distinct values) → the index may not be used |
| **Write cost** | Every `INSERT`/`UPDATE`/`DELETE` must also update every index on that row |

**When to index**

| Good candidate | Poor candidate |
|---|---|
| Primary and foreign key columns | Columns with very low selectivity (a `status` with 3 values) |
| Columns used in `WHERE`, `JOIN`, `ORDER BY`, `GROUP BY` | Columns used only in the `SELECT` list |
| Sort/join columns in large tables | A table with fewer than ~1000 rows |
| High-cardinality columns | Wide `TEXT`/`BLOB` columns without a prefix index |

**When NOT to index:** small tables, frequently-updated columns, low-selectivity columns, and
columns with many `NULL`s.

### 7. Views

A **view** is a named, stored `SELECT` query that behaves like a table.

| Type | What it does |
|---|---|
| **Virtual view** | Stored as the query text; recomputed every time it is queried; costs nothing to store |
| **Materialized view** | The **result** is physically stored and refreshed on a schedule or on demand |

**Advantages of views**

| Advantage | Why |
|---|---|
| Simplicity | Hide complex joins, filters and aggregations behind a simple name |
| Security | Grant access to a view without granting access to the base tables |
| Logical data independence | Restructure the base tables and re-point the view |
| Consistency | One definition of a business rule, reused everywhere |
| Reusability | A single definition reused by many queries |

**Disadvantages of views**

| Disadvantage | Why |
|---|---|
| Performance | A complex view expands into its full query every time — no automatic optimisation |
| No index | You cannot index a virtual view; the base tables must be indexed |
| Update restrictions | Only **simple, single-table, no aggregates/DISTINCT/GROUP BY/JOIN** views are updatable |
| Maintenance | Changing the base table may break the view |

**Updatable view rules (typical)**

| Requirement | Why |
|---|---|
| Single base table | A join makes "which row do I update?" ambiguous |
| No `GROUP BY`, `HAVING`, `DISTINCT`, aggregate | Aggregation has no single target row |
| All required columns of the base table present | You cannot update a column the view does not expose |
| No `UNION`, `UNION ALL`, `GROUP BY` | Same reason |

### 8. Stored procedures, functions and triggers

| Object | Returns | Can modify data? | Fires |
|---|---|---|---|
| **Stored procedure** | Optional `OUT` parameters | ✅ Yes | When called |
| **Function** | Exactly one value | ❌ No (in MySQL/PostgreSQL) | When called, from an expression |
| **Trigger** | None | ✅ Yes | **Automatically** on an event |

**Trigger events:** `BEFORE INSERT`, `AFTER INSERT`, `BEFORE UPDATE`, `AFTER UPDATE`, `BEFORE
DELETE`, `AFTER DELETE`.

**Use cases**

| Object | Use case |
|---|---|
| Procedure | A multi-step business operation called from the application |
| Function | A computed value used inside a `SELECT` (`fn_full_name(a, b)`) |
| Trigger | Audit logging, maintaining a summary table, enforcing a cross-table rule |

### 9. DBMS vs RDBMS vs flat files

| Feature | Flat files | DBMS | RDBMS |
|---|---|---|---|
| Data redundancy | High | Controlled | Controlled by normalisation |
| Integrity constraints | None | Some | Full (PK, FK, CHECK) |
| Concurrent access | Poor | Managed | Managed with isolation levels |
| Queries | Write code | Query language | SQL |
| Recovery | Manual | Automatic | Automatic via WAL |

**DBMS advantages over file systems**

| Advantage | Explanation |
|---|---|
| Redundancy control | A fact is stored once, in one place |
| Consistency | Constraints prevent invalid states |
| Sharing | Many users, many programs, one copy of the data |
| Security | Permissions per table, column, or view |
| Backup & recovery | Automatic, consistent |
| Standards | One language (SQL) instead of per-application code |

**Architecture tiers**

| Tier | What it is | Typical user |
|---|---|---|
| **1-tier** | The app and the DB on the same machine, no network | A local tool |
| **2-tier** | Client → DBMS over the network; the client does the presentation and business logic | A desktop app |
| **3-tier** | Client → application server → DBMS; the middle tier holds the business logic | A web app |

### 10. Database users and the DBA

| Role | What they do |
|---|---|
| **Database Administrator (DBA)** | Schema definition, storage, security, backup, recovery, performance tuning, granting privileges |
| **Database designer** | Logical and physical schema design, normalisation, tuning |
| **Application programmer** | Writes the programs that use the database |
| **End user** | Runs the application; may write their own ad-hoc queries |
| **Specialist user** | Writes complex SQL and scripts |

**DBA tasks**

| Task | Tool |
|---|---|
| Define the schema | DDL |
| Grant and revoke access | DCL |
| Manage storage and indexes | DDL, `OPTIMIZE`/`REINDEX` |
| Backup and recovery | `BACKUP`, log shipping, PITR |
| Monitor and tune | Execution plans, statistics, `EXPLAIN` |

## Worked example

**Q. A `customers` table and an `orders` table are related such that each order belongs to exactly
one customer and a customer may place many orders. What is the relationship's cardinality, and
which foreign key is correct?**

- A. M:N — `orders.cust_id REFERENCES customers(cust_id)`
- B. 1:N — `customers.cust_id REFERENCES orders.cust_id)`
- C. 1:N — `orders.cust_id REFERENCES customers(cust_id)`
- D. 1:1 — `orders.cust_id REFERENCES customers(cust_id)`

**Solution**

"Each order belongs to exactly one customer" and "a customer may place many orders" is the
definition of a **one-to-many** relationship from `customers` to `orders`. The foreign key lives on
the **many** side — `orders.cust_id` — and references the **one** side's primary key
`customers.cust_id`.

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | M:N would mean an order can have several customers. It cannot — one order has one customer |
| B | The FK is on the wrong table. `customers.cust_id` is the primary key of `customers`; you cannot reference `orders.cust_id` from `customers` — that would create a circular dependency |
| D | 1:1 would mean each customer places at most one order. On the fixture Ananya has two orders (1001, 1002) |

**Note on participation:** the relationship is **total** on the `orders` side (every order must have
a customer) and **partial** on the `customers` side (Vikram, `cust_id` 105, has no orders). That is
why the fixture uses `LEFT JOIN` when you need to keep Vikram.

## Quick rules

- **Three levels:** external (view) → conceptual (logical) → internal (physical).
- **Logical data independence** = conceptual changes, external does not. **Physical** = internal
  changes, conceptual does not.
- **DDL** changes schema, **DML** changes data, **DQL** reads, **DCL** grants, **TCL** commits.
- **Candidate key** = minimal superkey. **Primary key** = the one you chose. **Alternate** = the
  others.
- **FK lives on the many side.** `ON DELETE CASCADE` deletes children too.
- **M:N needs a junction table** with a composite key.
- **B-tree** for ranges and sorts, **hash** for exact matches, **clustered** stores the rows.
- **Leftmost prefix rule**: index on `(a, b)` does not help a query on `b` alone.
- **Views** hide complexity and secure data, but cannot be indexed and only simple single-table
  views are updatable.

## Common traps

| Trap | What you get | What you should get |
|---|---|---|
| Logical vs physical data independence reversed | — | Logical = conceptual changes; physical = internal changes |
| DML said to change the schema | — | Only DDL changes schema |
| Foreign key on the wrong side | B in the example | FK on the many side |
| Composite index used for a non-leftmost column | — | Only with the leftmost prefix present |
| "Views improve performance" | — | Virtual views usually slow queries down |
| All views are updatable | — | Only simple single-table views |
| `COUNT(*)` vs `COUNT(col)` in an index discussion | — | Unrelated |

## Checklist

- [ ] I can draw the three-level schema and name both data-independence types.
- [ ] I can sort DDL / DML / DQL / DCL / TCL into two buckets.
- [ ] I can name all ten key types and give one example of each.
- [ ] I know the five `ON DELETE` actions.
- [ ] I can read cardinality and participation off a scenario.
- [ ] I know when an index helps and when it does not.
- [ ] I can list the updatable-view rules.
- [ ] I know the 1-tier / 2-tier / 3-tier architecture difference.

## Related

- [DBMS concept procedures](../02-techniques/01-dbms-concept-procedures.md)
- [Solved DBMS theory set](../03-worked-examples/01-solved-dbms-theory-set.md)
- [DBMS theory traps](../04-pitfalls/01-dbms-theory-traps.md)
- [DBMS theory quick check](../05-reference/01-dbms-theory-quick-check.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
