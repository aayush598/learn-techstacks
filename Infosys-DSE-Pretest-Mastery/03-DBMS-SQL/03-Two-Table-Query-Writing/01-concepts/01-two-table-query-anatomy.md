# Two-Table Query Writing — The Anatomy of a Two-Table Query

> Section 3 · DBMS & SQL · Two-Table Query Writing · _Estimated reading time: 8 min_
> **Prerequisite:** [Join decision table](../02-Joins/02-techniques/01-join-decision-table.md)

## In one sentence

**A two-table query is eight clauses in a fixed order** — and almost every wrong answer in the
pre-test is a clause in the wrong place.

## Why the pre-test tests this

- "Write a query for two tables" is 1–2 of the 10 DBMS questions, usually free-response or
  "which query is correct".
- The grader checks three things: the join type, the join condition, and the clause order. Get all
  three and the mark is yours.
- This is the archetype where Meera's DBMS strength should pay off — but only if she does not
  reorder the clauses under pressure.

## Core concept

### 1. The eight clauses, in typed order

```sql
SELECT  c.cust_name, o.amount          -- 6. output columns
FROM    customers c                     -- 1. base table (the LEFT table)
JOIN    orders o ON o.cust_id = c.cust_id  -- 2. join type + 3. join condition
WHERE   o.amount > 400                 -- 4. row filter
GROUP BY c.cust_id, c.cust_name        -- 5. grouping
HAVING  COUNT(*) > 1                   -- 5b. group filter
ORDER BY total DESC                    -- 7. sorting
LIMIT  5;                              -- 8. cut
```

### 2. The eight clauses, in executed order

```
1. FROM + JOIN      build the working set        ← rows can multiply here
2. WHERE            drop individual rows
3. GROUP BY         collapse rows into groups
4. HAVING           drop groups
5. SELECT           compute output columns
6. DISTINCT         remove duplicate output rows
7. ORDER BY         sort
8. LIMIT            cut
```

**Everything else in this topic follows from this list.** The three rules that get tested:

- An aggregate may appear in `SELECT`, `HAVING` and `ORDER BY` — **never in `WHERE`**.
- An alias defined in `SELECT` may be used in `ORDER BY`, but **not in `GROUP BY`** (standard SQL).
- `LIMIT` without `ORDER BY` has no defined order.

### 3. The join condition — the single most important line

```sql
JOIN orders o ON o.cust_id = c.cust_id
```

| Rule | Why |
|---|---|
| Use **qualified** column names | Both tables have `cust_id`; unqualified is ambiguous |
| Qualify on the **right** side with the right alias | `ON o.cust_id = c.cust_id` |
| Do not repeat the `ON` condition in `WHERE` | On a `LEFT JOIN` that kills the unmatched rows |
| Match on the key, not on a descriptive column | `ON c.city = o.city` creates a cartesian blow-up |

Always alias both tables. `FROM customers JOIN orders ON customers.cust_id = orders.cust_id` works,
but it is unreadable the moment a third table arrives.

### 4. `WHERE` vs `HAVING` — the two-filter rule

| Clause | Filters | Can use an aggregate | Can use a `SELECT` alias |
|---|---|---|---|
| `WHERE` | Individual **rows** | No | No |
| `HAVING` | **Groups** of rows | Yes | Yes (MySQL) |

The classic exam question: "filter customers who have placed more than one order".

```sql
-- Correct
SELECT c.cust_id, c.cust_name, COUNT(*) AS n
FROM   customers c JOIN orders o ON o.cust_id = c.cust_id
GROUP  BY c.cust_id, c.cust_name
HAVING COUNT(*) > 1;
```

**Why `WHERE c.cust_id IN (...)` is a different question:** it filters *customers* by a condition
computed in a subquery, then counts all their orders. Same result here, but a different plan and a
different meaning if the condition changes.

### 5. The three clauses you should almost never need

| Clause | When to skip it |
|---|---|
| `GROUP BY` | The question asks for row-level data, not aggregates |
| `HAVING` | There are no groups |
| `ORDER BY` / `LIMIT` | The question does not ask for an order or a top-N |

**Ananya's habit** is to add `GROUP BY` to every query because the answer looked "more
professional". An unnecessary `GROUP BY` changes the result: it collapses duplicate rows and makes
every non-aggregated column a grouping key.

### 6. `SELECT` list discipline

The question asks for specific columns. Selecting `*` on a two-table join gives you **both**
`cust_id` columns, which is usually not what is asked.

```sql
-- The exam answer
SELECT c.cust_name, o.amount

-- The lazy answer
SELECT * FROM customers c JOIN orders o ON o.cust_id = c.cust_id;
-- returns 7 columns: cust_id, cust_name, city, order_id, cust_id, order_date, amount
```

### 7. Aggregates and aliases

```sql
SELECT c.cust_name, SUM(o.amount) AS total_spend
FROM   customers c JOIN orders o ON o.cust_id = c.cust_id
GROUP  BY c.cust_id, c.cust_name
ORDER  BY total_spend DESC
LIMIT  3;
```

- `SUM(o.amount)` ignores NULLs — the same as `SUM` over the inner join.
- `total_spend` is an alias; `ORDER BY total_spend` is legal, `ORDER BY SUM(o.amount)` is also legal
  and sometimes safer (MySQL resolves both).
- `GROUP BY c.cust_id, c.cust_name` is the safe form. `GROUP BY c.cust_name` alone works here only
  because names happen to be unique.

### 8. "Include the zeros" — the pattern the exam loves

"List all customers with the number of orders, including those with none":

```sql
SELECT c.cust_name, COUNT(o.order_id) AS order_count
FROM   customers c
LEFT JOIN orders o ON o.cust_id = c.cust_id
GROUP  BY c.cust_id, c.cust_name;
```

| Expression | Vikram's count |
|---|---|
| `COUNT(*)` | **1** ❌ (counts the NULL-padded row) |
| `COUNT(o.order_id)` | **0** ✅ |

For sums, wrap in `COALESCE`:

```sql
SELECT c.cust_name, COALESCE(SUM(o.amount), 0) AS total
FROM   customers c LEFT JOIN orders o ON o.cust_id = c.cust_id
GROUP  BY c.cust_id, c.cust_name;
```

### 9. "Find the ones with none" — the anti-join pattern

```sql
SELECT c.cust_name
FROM   customers c
LEFT JOIN orders o ON o.cust_id = c.cust_id
WHERE  o.order_id IS NULL;
```

Or, NULL-safe without a join:

```sql
SELECT c.cust_name
FROM   customers c
WHERE  NOT EXISTS (SELECT 1 FROM orders o WHERE o.cust_id = c.cust_id);
```

Both return customer 105 on the shared fixture. `NOT IN (SELECT cust_id FROM orders)` does **not**,
because the `orders` table contains a NULL `cust_id` row.

### 10. "Top N per group" — the window function

MySQL note: **window functions require MySQL 8.0+.** On older MySQL the equivalent is a correlated
subquery or a `GROUP BY` with a self-join.

```sql
-- Top 3 orders per customer (MySQL 8+)
SELECT c.cust_name, o.order_id, o.amount,
       ROW_NUMBER() OVER (PARTITION BY c.cust_id ORDER BY o.amount DESC) AS rn
FROM   customers c JOIN orders o ON o.cust_id = c.cust_id
WHERE  rn <= 3;   -- MySQL does not allow a window function in WHERE — see the note below
```

Standard form (filter in an outer query, because `WHERE` runs before windows):

```sql
SELECT * FROM (
  SELECT c.cust_name, o.order_id, o.amount,
         ROW_NUMBER() OVER (PARTITION BY c.cust_id ORDER BY o.amount DESC) AS rn
  FROM   customers c JOIN orders o ON o.cust_id = c.cust_id
) t
WHERE t.rn <= 3;
```

| Window function | Use |
|---|---|
| `ROW_NUMBER()` | 1, 2, 3, … always distinct — the right one for "top N per group" |
| `RANK()` | 1, 1, 3, … ties share a rank and then skip |
| `DENSE_RANK()` | 1, 1, 2, … ties share a rank, no skipping |
| `SUM(...) OVER (ORDER BY ...)` | Running total |
| `LAG(col) / LEAD(col)` | Previous / next row |

### 11. Running total

```sql
SELECT o.order_date, o.amount,
       SUM(o.amount) OVER (ORDER BY o.order_date) AS running_total
FROM   orders o;
```

On the shared fixture:

| order_date | amount | running_total |
|---|---|---|
| 2026-01-05 | 500.00 | 500.00 |
| 2026-01-09 | 750.00 | 1250.00 |
| 2026-02-11 | 1200.00 | 2450.00 |
| 2026-02-14 | 300.00 | 2750.00 |
| 2026-03-02 | 950.00 | 3700.00 |
| 2026-03-03 | 1100.00 | 4800.00 |

For a deterministic order, add a tiebreaker to the `ORDER BY` inside the window:
`OVER (ORDER BY o.order_date, o.order_id)`.

### 12. "Find pairs" — the self-join

"Find all pairs of customers in the same city":

```sql
SELECT a.cust_name AS c1, b.cust_name AS c2
FROM   customers a
JOIN   customers b ON a.city = b.city AND a.cust_id < b.cust_id;
```

- `a.cust_id < b.cust_id` prevents each pair appearing twice (A,B and B,A).
- The result on the fixture: (Ananya, Meera) — the only two customers in Pune.

## Worked example

**Q. Write a query to list each customer with the total amount they have ordered, including
customers who have never ordered, ordered by total descending.**

**Reference answer**

```sql
SELECT c.cust_id,
       c.cust_name,
       COALESCE(SUM(o.amount), 0) AS total_ordered
FROM   customers c
LEFT JOIN orders o ON o.cust_id = c.cust_id
GROUP  BY c.cust_id, c.cust_name
ORDER  BY total_ordered DESC;
```

**Expected output**

| cust_id | cust_name | total_ordered |
|---|---|---|
| 104 | Karthik | 2050.00 |
| 101 | Ananya | 1250.00 |
| 102 | Rahul | 1200.00 |
| 103 | Meera | 300.00 |
| 105 | Vikram | 0 |

**Why each clause is there**

| Clause | Reason |
|---|---|
| `LEFT JOIN` | "including customers who have never ordered" |
| `COALESCE(SUM(...), 0)` | `SUM` over zero rows is `NULL`, not `0` |
| `GROUP BY c.cust_id, c.cust_name` | One row per customer, and both non-aggregated columns are legal grouping keys |
| `ORDER BY total_ordered DESC` | The question asks for descending total |

**Why the near-misses are wrong**

| Near-miss | What breaks |
|---|---|
| `JOIN` instead of `LEFT JOIN` | Vikram disappears — the question explicitly includes him |
| `SUM(o.amount)` without `COALESCE` | Vikram shows `NULL` instead of `0` |
| `COUNT(*)` instead of `SUM` | Counts orders, not money |
| `GROUP BY c.cust_name` only | Works on this data by luck; fails if two customers share a name |
| No `ORDER BY` | The ordering requirement is unmet |

## Quick rules

- Write `FROM` + `JOIN … ON` **first**. Nothing else until it is right.
- Use qualified names on both sides of the `ON` condition.
- `WHERE` filters rows; `HAVING` filters groups. Aggregates only in `SELECT`/`HAVING`/`ORDER BY`.
- `GROUP BY` every non-aggregated column in `SELECT`.
- `COUNT(right.col)` for "how many matches, including zero".
- `COALESCE(SUM(x), 0)` when zeros are required.
- `LIMIT` needs `ORDER BY`; add a tiebreaker.
- Window functions need MySQL 8+.

## Common traps

| Trap | What you get | What you should get |
|---|---|---|
| `WHERE` instead of `HAVING` for an aggregate filter | Error | `HAVING` |
| Unnecessary `GROUP BY` | Rows collapsed | Only group when aggregating |
| `SELECT *` on a join | Duplicate key columns | Named columns |
| `COUNT(*)` for "count of orders, including 0" | 1 for the zero case | `COUNT(o.order_id)` |
| `SUM` with no rows | `NULL` | `COALESCE(SUM(...), 0)` |
| `LIMIT` with no `ORDER BY` | Arbitrary | Add `ORDER BY` |
| Right-table condition in `WHERE` on a `LEFT JOIN` | Inner join behaviour | Move it to `ON` |
| Missing tiebreaker in a window `ORDER BY` | Non-deterministic | Add a unique key |

## Checklist

- [ ] I wrote `FROM` + `JOIN … ON` before anything else.
- [ ] Both join columns are qualified with the right alias.
- [ ] I checked whether the question needs `LEFT` or `INNER`.
- [ ] Every aggregate is in `SELECT`/`HAVING`/`ORDER BY`, never in `WHERE`.
- [ ] I grouped by every non-aggregated selected column.
- [ ] I used `COUNT(col)` and `COALESCE(SUM(...), 0)` where zeros are required.
- [ ] I added `ORDER BY` before `LIMIT`, with a tiebreaker if needed.

## Related

- [The eight-step recipe](../02-techniques/01-the-eight-step-recipe.md)
- [Task recipe cards](../02-techniques/02-task-recipe-cards.md)
- [Solved query writing set](../03-worked-examples/01-solved-query-writing-set.md)
- [Query writing traps](../04-pitfalls/01-query-writing-traps.md)
- [Pattern library](../05-reference/01-query-writing-pattern-library.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
