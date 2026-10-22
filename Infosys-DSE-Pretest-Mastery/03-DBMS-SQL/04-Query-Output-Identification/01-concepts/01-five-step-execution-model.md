# The Five-Step Execution Model — How to Read a Query You Did Not Write

> Section 3 · DBMS & SQL · Query Output Identification · _Estimated reading time: 8 min_
> **Prerequisite:** [SQL basics: SELECT, filter, sort and subqueries](../01-SQL-Basics-DDL-DML/01-concepts/02-select-filter-sort-and-subqueries.md)

## In one sentence

**A `SELECT` runs in five logical stages — `FROM`+`JOIN` → `WHERE` → `GROUP BY` → `HAVING` →
`SELECT`+`ORDER BY`** — and you can only read the output correctly if you walk them in that order.

## Why the pre-test tests this

- "Identify the output of the given SQL query" is 2 of the 10 DBMS questions — the joint-largest
  archetype.
- These questions are not hard, they are **slow**: candidates try to hold six rows in their head and
  lose track of which ones the join duplicated.
- The entire skill is discipline: write the intermediate row set at every stage, on paper.

## Core concept

### The five stages

```
Stage 1   FROM + JOIN      →  build the working set          (rows multiply here)
Stage 2   WHERE            →  drop individual rows
Stage 3   GROUP BY         →  collapse rows into groups
Stage 4   HAVING           →  drop groups
Stage 5   SELECT + DISTINCT + ORDER BY + LIMIT  →  shape, sort, cut
```

Each stage's output is the next stage's input. **You must write down the output of stages 1, 2 and
3** to answer the question. That is the whole technique.

### Stage 1 — `FROM` + `JOIN`

The working set starts as the cartesian product of every table in the `FROM`, then `ON` keeps the
matching pairs.

| Statement | Working set on the fixture |
|---|---|
| `FROM customers` | 5 rows |
| `FROM orders` | 6 rows |
| `FROM customers c JOIN orders o ON c.cust_id = o.cust_id` | **6 rows** |
| `FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id` | **7 rows** |
| `FROM customers c CROSS JOIN orders o` | **30 rows** |

**The three questions to ask at stage 1:**

1. **Which join type?** `INNER` drops unmatched rows on both sides; `LEFT` keeps unmatched left rows
   (right side NULL); `RIGHT` keeps unmatched right rows.
2. **How many rows does each side produce?** A one-to-many join **fans out** the "one" side.
3. **What happens to NULLs on the join key?** `NULL = NULL` is `UNKNOWN`, so a row with a NULL
   foreign key never matches anything.

### Stage 2 — `WHERE`

Filters individual rows. Three things to check:

| Check | Consequence |
|---|---|
| Does the condition reference the **right** table of a `LEFT JOIN`? | If yes, the NULL-padded rows are dropped — the join behaves like an inner join |
| Does it use `=` with a possibly-NULL column? | `NULL = x` is `UNKNOWN` → the row is dropped |
| Does it reference an aggregate? | **Error** — aggregates are not available yet |

### Stage 3 — `GROUP BY`

Collapses rows into groups. Three things to check:

| Check | Consequence |
|---|---|
| Which columns form the grouping key? | One output row per **distinct combination** |
| Are there NULLs in the grouping column? | All NULLs form **one** group |
| Is there no `GROUP BY` at all? | The entire working set is **one** group (one output row) |

### Stage 4 — `HAVING`

Filters groups. Only matters if the query has a `GROUP BY` or an aggregate.

### Stage 5 — `SELECT`, `DISTINCT`, `ORDER BY`, `LIMIT`

| Feature | What to check |
|---|---|
| `SELECT` list | Only the selected columns appear; aggregates are computed here |
| `DISTINCT` | Applied to the **whole output row**, not one column |
| `ORDER BY` | Sort key may be a column not in the `SELECT` list; NULL placement is engine-specific |
| `LIMIT` | Cuts after sorting; with ties the result is non-deterministic |

### The four rules that decide most output questions

1. **A join can multiply rows.** After a join, count rows — do not count entities.
2. **`NULL` never matches.** `NULL = NULL`, `NULL > x`, `NULL <> x` are all `UNKNOWN`, so those rows
   disappear from a `WHERE`.
3. **`COUNT(*)` counts rows; `COUNT(col)` counts non-NULL values.** After a `LEFT JOIN`, the
   difference is exactly the number of unmatched left rows.
4. **`WHERE` filters before grouping; `HAVING` filters after.** A `HAVING` on a column that is not
   in the `GROUP BY` (and not aggregated) is an error in strict mode and a semantic change otherwise.

### Worked example — a full trace

**Query**

```sql
SELECT c.city, COUNT(*) AS n
FROM   customers c
LEFT JOIN orders o ON c.cust_id = o.cust_id
WHERE  o.amount >= 500
GROUP BY c.city
ORDER BY n DESC;
```

**Stage 1 — the working set (7 rows)**

| cust_name | city | order_id | amount |
|---|---|---|---|
| Ananya | Pune | 1001 | 500.00 |
| Ananya | Pune | 1002 | 750.00 |
| Rahul | Chennai | 1003 | 1200.00 |
| Meera | Pune | 1004 | 300.00 |
| Karthik | Delhi | 1005 | 950.00 |
| Karthik | Delhi | 1006 | 1100.00 |
| Vikram | Bengaluru | NULL | NULL |

**Stage 2 — after `WHERE o.amount >= 500` (5 rows)**

| cust_name | city | order_id | amount |
|---|---|---|---|
| Ananya | Pune | 1001 | 500.00 |
| Ananya | Pune | 1002 | 750.00 |
| Rahul | Chennai | 1003 | 1200.00 |
| Karthik | Delhi | 1005 | 950.00 |
| Karthik | Delhi | 1006 | 1100.00 |

Meera's 300.00 is out. **Vikram is out too** — his `amount` is NULL and `NULL >= 500` is `UNKNOWN`.
The `LEFT JOIN` added him; the `WHERE` deleted him again. This is the trap.

**Stage 3 — after `GROUP BY c.city` (3 groups)**

| city | rows in group |
|---|---|
| Pune | 2 (Ananya ×2) |
| Chennai | 1 (Rahul) |
| Delhi | 2 (Karthik ×2) |

**Stage 4 — no `HAVING`, so all 3 groups survive.**

**Stage 5 — `SELECT` + `ORDER BY n DESC`**

| city | n |
|---|---|
| Pune | 2 |
| Delhi | 2 |
| Chennai | 1 |

The order between Pune and Delhi is a **tie** (both 2), so the DBMS may return them in either
order. If the exam wants a deterministic answer, the query needs a tiebreaker.

**Output rows: 3.**

## Quick rules

- Five stages, always in that order: `FROM`+`JOIN` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT`.
- Write the stage-1 row set on paper. Everything else follows from it.
- After a join, count **rows**, not entities.
- `NULL` rows disappear from any `WHERE` comparison except `IS NULL`.
- `COUNT(*)` vs `COUNT(col)` after a `LEFT JOIN` differ by the unmatched-row count.
- `DISTINCT` applies to the whole output row.
- `ORDER BY` ties → non-deterministic output order.

## Common traps

| Trap | What you get | What you should get |
|---|---|---|
| Counting entities instead of join rows | 5 | 6 or 7 depending on the join |
| Forgetting that `WHERE` on the right table kills a `LEFT JOIN` | 6 | 5 |
| Thinking `NULL > 400` is false-but-kept | Keeps the row | Drops the row |
| `COUNT(*)` = `COUNT(col)` | Same numbers | They differ by the NULL count |
| `GROUP BY` on a column with NULLs | One group per value | All NULLs in **one** group |
| No `GROUP BY` but an aggregate | Many rows | Exactly **one** row |
| `DISTINCT` on one column | Rows deduped on that column only | Dedup on the whole row |
| `LIMIT` before sorting | Arbitrary rows | Sort, then cut |

## Checklist

- [ ] I identified the join type before counting anything.
- [ ] I wrote the stage-1 row set on paper.
- [ ] I applied the `WHERE` and noted which rows died (including the NULL ones).
- [ ] I formed the groups and counted the rows in each.
- [ ] I applied `HAVING` before computing the final counts.
- [ ] I checked `COUNT(*)` vs `COUNT(col)` and `DISTINCT` semantics.
- [ ] I checked whether `ORDER BY` ties make the order undefined.

## Related

- [Trace procedures](../02-techniques/01-trace-procedures.md)
- [Solved output identification set](../03-worked-examples/01-solved-output-identification-set.md)
- [Output identification traps](../04-pitfalls/01-output-identification-traps.md)
- [Output identification reference](../05-reference/01-output-identification-reference.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
