# DBMS Theory Quick Check — One Page

> Section 3 · DBMS & SQL · DBMS Theory, Keys, Indexes & Views · _Estimated reading time: 3 min_
> **Prerequisite:** [DBMS concept procedures](../02-techniques/01-dbms-concept-procedures.md)

## In one sentence

The three schema levels, the five languages, ten key types, the cardinality rules, the index types
and the view rules — the whole archetype on one page.

## Why the pre-test tests this

- 1–2 marks, and this page is 3 minutes of reading. Best marks-per-minute in Section 3.
- Every distractor in this archetype appears as a wrong row in one of these tables.

## Core concept

### Three-level schema

| Level | Also called | Holds |
|---|---|---|
| External | View level | Views, user programs |
| Conceptual | Logical level | All tables, keys, constraints, relationships |
| Internal | Physical level | Files, pages, indexes, access paths |

| Independence | Level that changes | Level that does not |
|---|---|---|
| **Logical** | Conceptual | External |
| **Physical** | Internal | Conceptual |

### Data languages

| Category | Commands |
|---|---|
| **DDL** | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` |
| **DML** | `INSERT`, `UPDATE`, `DELETE` |
| **DQL** | `SELECT` |
| **DCL** | `GRANT`, `REVOKE` |
| **TCL** | `COMMIT`, `ROLLBACK`, `SAVEPOINT` |

### Keys

| Key | Definition |
|---|---|
| Superkey | Any attribute set determining all attributes |
| Candidate key | **Minimal** superkey |
| Primary key | The candidate key chosen |
| Alternate key | A candidate key not chosen |
| Composite key | Two or more attributes |
| Partial key | Part of a composite key, not a key alone |
| Foreign key | References another table's PK |
| Natural key | Has business meaning |
| Surrogate key | System-generated, no meaning |
| Unique key | Unique but nullable (MySQL) |

**Prime attribute** = in **some** candidate key. **Non-prime** = in none.

### Referential integrity

| `ON DELETE` | Effect |
|---|---|
| `CASCADE` | Delete children too |
| `SET NULL` | Null the child's FK |
| `RESTRICT` | Refuse immediately |
| `NO ACTION` | Refuse at end of statement |
| `SET DEFAULT` | Use the child's default |

### ER model

| Cardinality | Shape | Fixture |
|---|---|---|
| 1:1 | one ↔ one | Employee ↔ ParkingSpot |
| 1:N | one → many | Customer → Order; Department → Employee |
| M:N | many ↔ many | Student ↔ Course (via `enrollments`) |

| Participation | Meaning |
|---|---|
| **Total** | Every entity must participate (every order has a customer) |
| **Partial** | May not participate (Vikram, cust_id 105, has no orders) |

| Attribute type | Example |
|---|---|
| Simple / composite | `cust_name` / first + last |
| Derived | `order_total`, `age` |
| Multivalued | `cust_phone` |
| Key | `cust_id` |

### Indexes

| Type | Use for |
|---|---|
| B-tree | Ranges, `BETWEEN`, `ORDER BY`, prefix |
| Hash | Exact `=` only |
| Bitmap | Low-cardinality columns, huge tables |
| Full-text | Natural language search |
| Clustered | Stores the rows; one per table (InnoDB = the PK) |
| Non-clustered | Stores pointers; covering indexes |

| Concept | Rule |
|---|---|
| Selectivity | `distinct / total` — higher is better |
| Composite | Leftmost prefix rule |
| Covering | Index holds every column the query needs |
| Write cost | Every write also updates every index |

### Views

| Type | Stored | Refreshed | Indexable |
|---|---|---|---|
| Virtual | The query | Every query | ❌ |
| Materialized | The result | On schedule / on demand | ✅ |

| Advantages | Disadvantages |
|---|---|
| Simplicity, security, logical data independence, consistency, reusability | Performance, no index, update restrictions, maintenance |

**Updatable view** = single base table, no aggregate/`GROUP BY`/`DISTINCT`/join/`UNION`, all needed
columns present.

### Programmable objects

| Object | Returns | Modifies data | Fires automatically |
|---|---|---|---|
| Procedure | `OUT` params | ✅ | ❌ |
| Function | One value | ❌ | ❌ |
| Trigger | Nothing | ✅ | ✅ |

### Architecture

| Tier | Shape |
|---|---|
| 1-tier | App + DB, same machine |
| 2-tier | Client → DBMS |
| 3-tier | Client → app server → DBMS |

### DBMS over flat files

Redundancy control · integrity · concurrency · sharing · security · backup and recovery ·
standards.

### Fixture facts

| Fact | Value |
|---|---|
| Customers / Orders / Departments / Employees | 5 / 6 / 3 / 6 |
| Customer with no order | 105 (partial participation) |
| Employees with no manager | 4, 5 (`manager_id` NULL) |
| Self-referencing FK | `employees.manager_id` |
| Composite key | `enrollments(student_id, course_id)` |
| M:N junction table | `enrollments` |

## Worked example

**Q. Which level of the three-level schema changes when a DBA adds an index on `orders(cust_id)`?**

- A. External
- B. Conceptual
- C. Internal
- D. All three

**Answer: C.** An index is a physical storage structure. The conceptual schema (tables, keys,
constraints) is unchanged and the external schema is untouched. This is **physical data
independence**.

## Quick rules

- Conceptual = logical, internal = physical.
- Logical independence = conceptual changes; physical = internal changes.
- Superkey any, candidate minimal, primary chosen.
- FK on the many side; junction table only for M:N.
- Composite index needs the leftmost column.
- Virtual views are not stored, not indexed, recomputed.
- Trigger fires automatically.

## Common traps

| Trap | Fix |
|---|---|
| Candidate key = "any determinant" | Minimal |
| Logical/physical reversed | Check which level the question names |
| "Views improve performance" | Usually the opposite |
| "All views are updatable" | Simple single-table only |
| Junction table for 1:N | FK only |

## Checklist

- [ ] I can name the three levels and their contents.
- [ ] I can sort the five language categories.
- [ ] I can define all ten key types.
- [ ] I can read cardinality and participation off a scenario.
- [ ] I know the index types and the leftmost prefix rule.
- [ ] I can list the updatable-view rules.
- [ ] I can tell a trigger from a procedure from a function.

## Related

- [Schema, keys and indexes](../01-concepts/01-schema-keys-and-indexes.md)
- [DBMS concept procedures](../02-techniques/01-dbms-concept-procedures.md)
- [Solved DBMS theory set](../03-worked-examples/01-solved-dbms-theory-set.md)
- [DBMS theory traps](../04-pitfalls/01-dbms-theory-traps.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
