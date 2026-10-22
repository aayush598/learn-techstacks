# DBMS Concept Procedures — Answering Theory Questions in 60 Seconds

> Section 3 · DBMS & SQL · DBMS Theory, Keys, Indexes & Views · _Estimated reading time: 7 min_
> **Prerequisite:** [Schema, keys and indexes](../01-concepts/01-schema-keys-and-indexes.md)

## In one sentence

**Name the concept, find the tell in the question, and pick the option that uses the concept's own
words.**

## Why the pre-test tests this

- 1–2 questions. The exam reuses the same twenty or so definitions across question banks.
- The options are near-identical sentences, so the only way to pick correctly is to know the exact
  distinction.

## Core concept

### Procedure 1 — the twenty-second classifier

Read the question stem, find the concept noun, then apply the matching table.

| The stem mentions | The concept | Go to |
|---|---|---|
| "schema levels", "external/conceptual/internal" | Three-level schema | Table A |
| "data independence" | Independence | Table B |
| "which language", "DDL/DML", "command categories" | Data languages | Table C |
| "key", "candidate", "primary", "foreign", "composite" | Keys | Table D |
| "referential integrity", "ON DELETE", "orphan" | Referential integrity | Table E |
| "cardinality", "one-to-many", "participation" | ER model | Table F |
| "index", "B-tree", "clustered", "selectivity" | Indexes | Table G |
| "view", "updatable", "materialized" | Views | Table H |
| "procedure vs function vs trigger" | Programmable objects | Table I |
| "DBMS vs files", "2-tier vs 3-tier", "DBA" | Architecture | Table J |

### Table A — three-level schema

| Level | Contains | Answers to |
|---|---|---|
| **External** | Views, user-specific schemas | "What does this user see?" |
| **Conceptual** | All tables, keys, constraints, relationships | "What does the whole database contain?" |
| **Internal** | Files, pages, indexes, access paths | "How is it physically stored?" |

### Table B — data independence

| Question | Answer | Which level changes |
|---|---|---|
| "Change the **conceptual** schema without changing the **external** schema" | **Logical** data independence | Conceptual |
| "Change the **internal** schema without changing the **conceptual** schema" | **Physical** data independence | Internal |
| "How is logical data independence achieved?" | **Views** | — |

**Tie-breaker:** if the word *physical* or *index* or *file* appears → physical. If the word
*schema restructure*, *add a table* or *view* appears → logical.

### Table C — data languages

| Command | Category |
|---|---|
| `CREATE`, `ALTER`, `DROP`, `TRUNCATE` | **DDL** |
| `INSERT`, `UPDATE`, `DELETE` | **DML** |
| `SELECT` | **DQL** |
| `GRANT`, `REVOKE` | **DCL** |
| `COMMIT`, `ROLLBACK`, `SAVEPOINT` | **TCL** |

### Table D — keys

| The stem says | The key is |
|---|---|
| "Determines all attributes, not necessarily minimal" | **Superkey** |
| "Minimal attribute set that determines all attributes" | **Candidate key** |
| "The candidate key actually used" | **Primary key** |
| "A candidate key not chosen as primary" | **Alternate key** |
| "Made of two or more attributes" | **Composite key** |
| "References another table's primary key" | **Foreign key** |
| "Has business meaning" | **Natural key** |
| "System-generated, no business meaning" | **Surrogate key** |
| "Part of a composite key but not a key alone" | **Partial key** |

### Table E — referential integrity

| The stem says | The answer |
|---|---|
| "What happens to children when the parent is deleted?" | Depends on the `ON DELETE` action — read it from the question |
| "Child rows pointing at a deleted parent" | **Orphan rows** — prevented by the FK constraint |
| "FK on a table that references itself" | **Self-referencing FK** (`employees.manager_id`) |

### Table F — ER model

| The stem describes | Cardinality |
|---|---|
| "Each A has exactly one B, and each B has at most one A" | **1:1** |
| "Each A has many B, each B has exactly one A" | **1:N** |
| "Each A has many B, each B has many A" | **M:N** — needs a junction table |

| The stem says | Participation |
|---|---|
| "Every A **must** have a B" | **Total** |
| "An A **may** have no B" | **Partial** |

**Reading the direction:** "Each order belongs to exactly one customer and a customer may place many
orders" → **1:N** from customer to order, **FK on `orders`**.

### Table G — indexes

| The stem says | The answer |
|---|---|
| "Supports `=`, `<`, `>`, `BETWEEN`, `ORDER BY`" | **B-tree** |
| "Exact match only, very large table" | **Hash** |
| "Stores the rows in index order" | **Clustered** |
| "Stores pointers to rows" | **Non-clustered** |
| "Entry for every record" | **Dense** |
| "Entry for some records, then scan" | **Sparse** |
| "Index on `(a, b)`, query filters on `b` only" | **Index not used** — leftmost prefix rule |
| "Index contains every column the query needs" | **Covering index** |
| "Few distinct values, huge table" | **Bitmap index** |

### Table H — views

| The stem says | The answer |
|---|---|
| "Stored as SQL text, recomputed each time" | **Virtual view** |
| "Result physically stored and refreshed" | **Materialized view** |
| "Can it be updated?" | Only **simple, single-table, no aggregate/join/group by/distinct** views |
| "Main advantages" | Simplicity, security, logical data independence, consistency, reusability |
| "Main disadvantage" | **Performance** — no index on a virtual view |

### Table I — programmable objects

| Returns a value? | Can modify data? | Fires automatically? | Object |
|---|---|---|---|
| Optional `OUT` params | ✅ | ❌ | **Stored procedure** |
| Exactly one value | ❌ | ❌ | **Function** |
| Nothing | ✅ | ✅ | **Trigger** |

### Table J — architecture

| The stem says | The answer |
|---|---|
| "App and DB on the same machine" | **1-tier** |
| "Client talks directly to the DBMS" | **2-tier** |
| "Client → app server → DBMS" | **3-tier** |
| "Why use a DBMS instead of files?" | Redundancy control, integrity, sharing, security, backup, standards |
| "Who grants privileges and manages storage?" | **DBA** |

### Procedure 2 — the "definition wording" rule

In a definition question, the correct option usually **reuses the vocabulary of the concept**:

| Question | Correct option wording | Wrong option wording |
|---|---|---|
| "What is a superkey?" | "Any attribute set that determines all attributes" | "The minimal attribute set that determines all attributes" (that is a candidate key) |
| "What is a candidate key?" | "A minimal superkey" | "The key chosen by the DBA" (that is the primary key) |
| "What is logical data independence?" | "Change the conceptual schema without changing the external schema" | "Change the internal schema without changing the conceptual schema" (that is physical) |

**Read the options as definitions.** Two options will be near-identical — one of them is a different
concept's definition.

### Procedure 3 — the "which is NOT" trap

Roughly one in four theory questions asks **"which is NOT true"** or **"which does NOT apply"**.
Three options are true and one is false — the hard way round.

| Technique | What to do |
|---|---|
| Verify each option against your definition | Do not look for the "most correct" option |
| Find the one that **contradicts** a rule | "Views can be indexed" is false |
| Watch for absolutes | "always", "never", "all", "only" — these are where the false option hides |
| Cross-check pairs | If options A and B are near-identical, one of them is the false one |

### Procedure 4 — the fixture facts for theory questions

| Fact | Value |
|---|---|
| Customers | 5 |
| Orders | 6 |
| Departments | 3 |
| Employees | 6 |
| Students / Courses / Enrollments | 3 / 3 / 5 |
| Customer with no order | 105 Vikram (→ **partial participation**) |
| Employee with no manager | 4 and 5 (`manager_id` NULL → **total participation** on `employees`) |
| `orders.cust_id` | FK → `customers.cust_id` (1:N) |
| `employees.dept_id` | FK → `departments.dept_id` (1:N) |
| `employees.manager_id` | **Self-referencing** FK |
| `enrollments(student_id, course_id)` | Junction table, **composite key** (M:N resolved) |

## Worked example

**Q. A DBA adds a new index on `orders(cust_id)` and reorganises the physical storage of the
`orders` table, without changing any table definition or any view. Which type of data independence
is this?**

- A. Logical data independence
- B. Physical data independence
- C. Both logical and physical
- D. Neither

**Solution**

Both changes are at the **internal (physical)** level: the index and the file layout. The
**conceptual** schema — the table definitions and constraints — is untouched, and so is the
external level.

**Answer: B (Physical data independence).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Logical data independence is about changing the **conceptual** schema (adding a table, splitting one) while the external schema stays fixed |
| C | No conceptual change was made, so no logical independence was exercised |
| D | Physical data independence is exactly this situation |

---

**Q2. Which of the following is TRUE about views?**

- A. A view can have an index created on it, which speeds up all queries that use it
- B. Every view is updatable
- C. A materialized view stores the query, not the result
- D. A view can hide the underlying table structure, providing logical data independence

**Solution**

**D** is true. Views decouple the external level from the conceptual level.

**Answer: D.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Only **materialized** views can be indexed. A virtual view is recomputed every time |
| B | Only simple single-table views with no aggregates, `GROUP BY`, `DISTINCT` or joins are updatable |
| C | Backwards. A materialized view stores the **result**. A virtual view stores the **query** |

## Quick rules

- External = view, conceptual = logical, internal = physical.
- Logical independence = conceptual changes; physical = internal changes.
- DDL = schema, DML = data, DQL = read, DCL = rights, TCL = transactions.
- Superkey = any determinant; candidate = minimal; primary = chosen; alternate = not chosen.
- FK on the many side; M:N needs a junction table.
- B-tree for ranges, hash for equality, clustered stores rows.
- Leftmost prefix rule; covering index; low selectivity = weak index.
- Only simple single-table views are updatable; virtual views cannot be indexed.

## Common traps

| Trap | Why the option is wrong |
|---|---|
| Logical vs physical independence | Check **which level** the question says changes |
| Superkey vs candidate key | Minimal or not |
| Foreign key on the wrong side | FK lives on the many side |
| Composite index used out of order | Leftmost prefix rule |
| "Views are indexed" / "views improve performance" | Only materialized views |
| "All views are updatable" | Only simple ones |
| Missing a "NOT" in the stem | Verify each option, do not hunt for the best one |

## Checklist

- [ ] I can place any concept in one of the ten tables above.
- [ ] I can state both data-independence types in one line.
- [ ] I can sort the key types without hesitating.
- [ ] I can read cardinality and participation off a scenario.
- [ ] I know the index types and when each wins.
- [ ] I can list the updatable-view rules.
- [ ] I check whether the stem says "NOT".

## Related

- [Schema, keys and indexes](../01-concepts/01-schema-keys-and-indexes.md)
- [Solved DBMS theory set](../03-worked-examples/01-solved-dbms-theory-set.md)
- [DBMS theory traps](../04-pitfalls/01-dbms-theory-traps.md)
- [DBMS theory quick check](../05-reference/01-dbms-theory-quick-check.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
