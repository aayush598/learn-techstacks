# Query Writing Traps — Where the Marks Leak

> Section 3 · DBMS & SQL · Two-Table Query Writing · _Estimated reading time: 6 min_
> **Prerequisite:** [Two-table query anatomy](../01-concepts/01-two-table-query-anatomy.md)

## In one sentence

**Almost every wrong query is one of six mistakes** — and all six are visible if you check the
clause order before you read the SQL.

## Why the pre-test tests this

- A free-response query gives the grader no option list to anchor on. It compares your query to a
  reference, and one misplaced clause costs the whole mark.
- These six mistakes cover the vast majority of "wrong query" distractors the exam uses.
- Check the order first and you will catch four of the six without reading the SQL semantics.

## Core concept

### The six mistakes, in the order they appear in a query

| # | Mistake | Symptom | Fix |
|---|---|---|---|
| 1 | **Wrong join type** | The "including none" case loses its zero rows | `LEFT JOIN` when the stem says "including" |
| 2 | **Unqualified join column** | `cust_id` is ambiguous with two tables | `ON o.cust_id = c.cust_id` |
| 3 | **Right-table condition in `WHERE`** | The `LEFT JOIN` silently becomes an inner join | Move it into `ON` |
| 4 | **Aggregate in `WHERE`** | Query error | `HAVING` |
| 5 | **Unnecessary / incomplete `GROUP BY`** | Rows collapse, or the query errors | Group every non-aggregated column; skip `GROUP BY` entirely if not aggregating |
| 6 | **`LIMIT` without `ORDER BY`** | Arbitrary rows | Add `ORDER BY` first, plus a tiebreaker |

### Mistake 1 — wrong join type

| Stem | Correct | The trap |
|---|---|---|
| "all customers **including** those with no orders" | `LEFT JOIN` | `JOIN` |
| "customers **that have** placed an order" | `JOIN` | `LEFT JOIN` (over-inclusive) |
| "each X with the number of Y, **including** zero" | `LEFT JOIN` + `COUNT(y.col)` | `JOIN`, or `COUNT(*)` |

### Mistake 2 — unqualified join columns

```sql
-- Ambiguous: both tables have cust_id
SELECT cust_name, amount FROM customers JOIN orders ON cust_id = cust_id;

-- Correct
SELECT c.cust_name, o.amount FROM customers c JOIN orders o ON o.cust_id = c.cust_id;
```

`ON cust_id = cust_id` is also a **logical** bug even where it parses: it compares a column to
itself and is always true for non-NULL values.

### Mistake 3 — right-table condition in `WHERE`

```sql
-- 5 rows: the LEFT JOIN is destroyed
LEFT JOIN orders o ON c.cust_id = o.cust_id WHERE o.amount > 400

-- 7 rows: the LEFT JOIN survives
LEFT JOIN orders o ON c.cust_id = o.cust_id AND o.amount > 400
```

Rule: **on a `LEFT JOIN`, every predicate on the right table belongs in `ON`.**

### Mistake 4 — aggregate in `WHERE`

```sql
WHERE COUNT(*) > 1     -- error: aggregate evaluated before grouping
HAVING COUNT(*) > 1    -- correct
```

The only aggregates allowed in a `WHERE` are in a **subquery**:
`WHERE c.cust_id IN (SELECT cust_id FROM orders GROUP BY cust_id HAVING COUNT(*) > 1)`.

### Mistake 5 — the `GROUP BY` mistakes

| Mistake | Effect |
|---|---|
| No `GROUP BY` with an aggregate | One row for the whole table |
| `GROUP BY` on a column not in the `SELECT` | Legal but changes the grouping grain |
| `GROUP BY` missing a selected non-aggregated column | Error under `ONLY_FULL_GROUP_BY` (MySQL default since 5.7) |
| `GROUP BY` when no aggregate is used | Rows collapse; the result changes |

### Mistake 6 — `LIMIT` without `ORDER BY`

`LIMIT 3` with no `ORDER BY` returns **three arbitrary rows**. The exam's correct option always
has `ORDER BY` before `LIMIT`. And if the sort key can tie, the answer is non-deterministic — add a
tiebreaker (`ORDER BY total DESC, c.cust_id ASC`).

### Two more that show up in "which query is correct" questions

| Mistake | Why it fails |
|---|---|
| `SELECT *` on a two-table join | Returns both `cust_id` columns — usually not what was asked |
| `WHERE` after `GROUP BY` | Syntax error in standard SQL and in MySQL |

## Worked example

**Q. Which query correctly lists each customer with the number of orders they placed, including
customers with zero orders?**

- A. `SELECT c.cust_name, COUNT(o.order_id) AS n FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id, c.cust_name;`
- B. `SELECT c.cust_name, COUNT(*) AS n FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id, c.cust_name;`
- C. `SELECT c.cust_name, COUNT(o.order_id) AS n FROM customers c JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id, c.cust_name;`
- D. `SELECT c.cust_name, COUNT(o.order_id) AS n FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id WHERE c.cust_id > 0 GROUP BY c.cust_id, c.cust_name;`

**Solution**

| Requirement | Clause needed | A | B | C | D |
|---|---|---|---|---|---|
| Keep zero-order customers | `LEFT JOIN` | ✅ | ✅ | ❌ | ✅ |
| Report 0 as 0 | `COUNT(o.order_id)` | ✅ | ❌ `COUNT(*)` | ✅ | ✅ |
| No extra row filter | no `WHERE` | ✅ | ✅ | ✅ | ❌ filters `cust_id > 0` |

**Answer: A.** Output: Ananya 2, Rahul 1, Meera 1, Karthik 2, Vikram 0.

**The traps in this question**

| Trap | Where it shows up |
|---|---|
| `COUNT(*)` counts the NULL-padded row | B reports Vikram as **1** |
| Inner join drops the zero case | C has only 4 rows |
| An unnecessary `WHERE` changes the set | D would drop any customer with `cust_id <= 0` — the exam's point is that an extra predicate is a red flag even when it looks harmless |

**Second example — the `WHERE` that eats the `LEFT JOIN`.**

**Q. Which query returns all 5 customers, but only their orders above 400?**

| Option | Query | Rows | Verdict |
|---|---|---|---|
| A | `... LEFT JOIN orders o ON c.cust_id = o.cust_id WHERE o.amount > 400` | 5 | ❌ |
| B | `... LEFT JOIN orders o ON c.cust_id = o.cust_id AND o.amount > 400` | 7 | ✅ |
| C | `... JOIN orders o ON c.cust_id = o.cust_id WHERE o.amount > 400` | 5 | ❌ |
| D | `... LEFT JOIN orders o ON c.cust_id = o.cust_id WHERE o.amount >= 400` | 5 | ❌ |

**Answer: B.** Only B keeps Vikram. A and C both drop the NULL-padded row (and return the *same*
5 rows, which is why the trap is so effective). D is A with a different threshold — it still drops
Vikram, and it also drops nothing else because no order is exactly 400.

## Quick rules

- Check the join type first, then the join columns, then the clause order.
- "including" → `LEFT JOIN`; "that have" → `JOIN`.
- Qualify every join column with its table alias.
- Right-table predicates go in `ON` on a `LEFT JOIN`.
- Aggregates in `SELECT`/`HAVING`/`ORDER BY` only.
- Group by every non-aggregated selected column; skip `GROUP BY` if there is no aggregate.
- `ORDER BY` before `LIMIT`; add a tiebreaker.
- Never `SELECT *` on a join.

## Common traps

| Trap | Fix |
|---|---|
| Wrong join type | Read the escape clause |
| `ON cust_id = cust_id` | Qualify both sides |
| Right predicate in `WHERE` | Move to `ON` |
| Aggregate in `WHERE` | `HAVING` |
| Missing `GROUP BY` column | List every non-aggregated column |
| `GROUP BY` with no aggregate | Remove it |
| `LIMIT` without `ORDER BY` | Add both |
| `SELECT *` | Name the columns |

## Checklist

- [ ] I read the escape clause before choosing the join type.
- [ ] Both join columns are qualified.
- [ ] Every right-table predicate is inside `ON` on a `LEFT JOIN`.
- [ ] No aggregate sits in a `WHERE`.
- [ ] My `GROUP BY` matches the `SELECT` list exactly.
- [ ] `LIMIT` is preceded by `ORDER BY` with a tiebreaker.
- [ ] I named the mistake behind every query I got wrong.

## Related

- [Two-table query anatomy](../01-concepts/01-two-table-query-anatomy.md)
- [The eight-step recipe](../02-techniques/01-the-eight-step-recipe.md)
- [Task recipe cards](../02-techniques/02-task-recipe-cards.md)
- [Solved query writing set](../03-worked-examples/01-solved-query-writing-set.md)
- [Pattern library](../05-reference/01-query-writing-pattern-library.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
