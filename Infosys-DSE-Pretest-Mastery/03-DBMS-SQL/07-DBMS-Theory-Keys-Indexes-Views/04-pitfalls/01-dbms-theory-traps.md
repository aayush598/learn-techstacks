# DBMS Theory Traps — Where Candidates Lose the Mark

> Section 3 · DBMS & SQL · DBMS Theory, Keys, Indexes & Views · _Estimated reading time: 5 min_
> **Prerequisite:** [Schema, keys and indexes](../01-concepts/01-schema-keys-and-indexes.md)

## In one sentence

Nine traps, each one a near-miss definition that the exam deliberately puts next to the right
answer.

## Why the pre-test tests this

- In theory questions the distractors are **not random** — they are the correct definition of a
  *different* concept.
- If you know the exact wording of each definition, these questions become trivial.

## Core concept

### Trap 1 — Superkey vs candidate key

| Term | Definition | Remember |
|---|---|---|
| Superkey | Any attribute set that determines all attributes | **Any** will do |
| Candidate key | A **minimal** superkey | **Smallest** that works |

The trap option is usually "an attribute set that determines all attributes" offered as the answer
to "candidate key". Check the word **minimal**.

### Trap 2 — Candidate key vs primary key vs alternate key

| Term | Definition |
|---|---|
| Candidate key | Every minimal superkey |
| Primary key | The candidate key **chosen** |
| Alternate key | A candidate key **not** chosen |

"Every column in the primary key is a prime attribute" is true. "Every prime attribute is in the
primary key" is **false** — prime attributes are those in *some* candidate key.

### Trap 3 — Logical vs physical data independence reversed

| Type | The level that changes | The level that does not |
|---|---|---|
| **Logical** | Conceptual | External |
| **Physical** | Internal | Conceptual |

The tell: **physical** questions mention indexes, files, storage, pages, partitioning. **Logical**
questions mention adding/splitting a table, changing a column, re-pointing a view.

### Trap 4 — DDL auto-commit / DML rollback

DDL statements are **auto-committed** in mainstream DBMS — you cannot `ROLLBACK` a `CREATE TABLE`.
DML is transactional. If an option says "a `CREATE TABLE` can be rolled back", it is wrong (except
in MySQL with certain safety modes).

### Trap 5 — Foreign key on the wrong side

For a **1:N** relationship the FK is on the **many** side (`orders.cust_id`). Putting it on the "one"
side creates a circular reference and breaks the constraint.

### Trap 6 — M:N resolved with a junction table, 1:N not

If the requirement says "each order has **exactly one** customer", a junction table is wrong — it
would allow an order to have several customers. Junction tables are for **M:N only**.

### Trap 7 — Composite index and the leftmost prefix rule

Index on `(a, b)`:
- `WHERE a = 1` → ✅ usable
- `WHERE a = 1 AND b = 2` → ✅ usable
- `WHERE b = 2` → ❌ **not usable**
- `WHERE a = 1 ORDER BY b` → ✅ usable

### Trap 8 — "Views improve performance"

Virtual views are **recomputed on every query** and **cannot be indexed**. A view usually makes
things *slower* and adds a layer of indirection. Only a **materialized view** stores the result and
can be indexed — and it can be **stale** between refreshes, which is its own trap.

### Trap 9 — "All views are updatable"

Only **simple, single-table** views with no `GROUP BY`, `HAVING`, `DISTINCT`, aggregate, `UNION` or
join are updatable. The trap option is "a view can be updated like a table".

### Bonus trap — Trigger vs procedure vs function

| Object | Called by | Returns | Modifies data | Automatic |
|---|---|---|---|---|
| Procedure | You | `OUT` params | ✅ | ❌ |
| Function | You, in an expression | One value | ❌ | ❌ |
| Trigger | The DBMS | Nothing | ✅ | ✅ |

### Bonus trap — 2-tier vs 3-tier

**2-tier** = client talks **directly** to the DBMS. If the question's diagram has an application
server between the client and the DB, it is **3-tier**. "Client → DBMS" with the business logic in
the client is 2-tier.

## Worked example

**Q. Which of the following statements about views is TRUE?**

- A. A view is physically stored, which makes queries against it fast
- B. Any view can be updated, provided the user has `UPDATE` permission on the base table
- C. A view can be used to enforce referential integrity between two tables
- D. A view can be used to restrict the rows and columns a user can access, without granting access
  to the base tables

**Solution**

**D** is true. A view is a security mechanism as well as a simplification tool — you grant
`SELECT` on the view and never touch the base table's privileges.

**Answer: D.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | A **virtual** view stores the *query*, not the data. It is recomputed on every use and cannot be indexed |
| B | Only **simple, single-table** views with no aggregation, `GROUP BY`, `DISTINCT` or join are updatable |
| C | Referential integrity is enforced by **foreign key constraints**, not by views |

## Quick rules

- Superkey = any determinant; candidate = minimal; primary = chosen; alternate = the rest.
- Prime = in *some* candidate key. Not the same as primary.
- Logical independence = conceptual changes; physical = internal changes.
- DDL auto-commits; DML does not.
- FK on the many side; junction table only for M:N.
- Composite index needs the leftmost column.
- Virtual views: not stored, not indexed, recomputed, often slower.
- Updatable views: single table, simple, no aggregates or joins.
- Trigger fires automatically; procedure must be called.

## Common traps

| Trap | The tell in the option |
|---|---|
| Superkey offered for candidate key | Missing the word *minimal* |
| Primary key offered for prime attribute | Missing the word *some* |
| Physical/logical independence reversed | Mention of *conceptual* where *internal* belongs |
| "Views are fast" | View is recomputed every time |
| "Any view is updatable" | Mentions *any* or *all* |
| "Trigger must be called manually" | Contradicts the definition |
| Junction table for 1:N | Requirement says "exactly one" |

## Checklist

- [ ] I can write the minimal-superkey definition.
- [ ] I know prime ≠ primary.
- [ ] I can map both independence types to the level that changes.
- [ ] I know the FK side rule.
- [ ] I can apply the leftmost prefix rule.
- [ ] I can list the updatable-view rules.
- [ ] I can tell a trigger from a procedure from a function.

## Related

- [Schema, keys and indexes](../01-concepts/01-schema-keys-and-indexes.md)
- [DBMS concept procedures](../02-techniques/01-dbms-concept-procedures.md)
- [Solved DBMS theory set](../03-worked-examples/01-solved-dbms-theory-set.md)
- [DBMS theory quick check](../05-reference/01-dbms-theory-quick-check.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
