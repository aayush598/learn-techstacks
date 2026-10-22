# The Eight-Step Recipe for Writing a Two-Table Query

> Section 3 · DBMS & SQL · Two-Table Query Writing · _Estimated reading time: 7 min_
> **Prerequisite:** [Two-table query anatomy](../01-concepts/01-two-table-query-anatomy.md)

## In one sentence

**Eight steps, always in this order: `FROM` → `JOIN` → `ON` → `WHERE` → `GROUP BY` → `HAVING` →
`SELECT` → `ORDER BY` → `LIMIT`** — and step 1 is "which table goes on the left?".

## Why the pre-test tests this

- The archetype asks for a *free-response* query. There is no option list to lean on — you must
  produce the clause order yourself, under time pressure.
- The recipe exists so that you never have to remember the order; you just walk the list.
- Every clause you skip is a clause you cannot get wrong.

## Core concept

### The recipe, with the question each step answers

| Step | Clause | The question it answers | If the answer is "no", skip it |
|---|---|---|---|
| 1 | `FROM table1 alias1` | Which table must keep all its rows? | — |
| 2 | `[INNER\|LEFT\|RIGHT] JOIN table2 alias2` | Must the other table's rows survive too? | Use `INNER JOIN` |
| 3 | `ON alias2.key = alias1.key` | How do the two tables match? | — |
| 4 | `WHERE condition` | Which individual rows are wanted? | No row filter |
| 5 | `GROUP BY cols` | Do we need counts/totals/averages? | No aggregate → no group |
| 6 | `HAVING condition` | Which groups qualify? | No group filter |
| 7 | `SELECT cols` | Which columns are asked for? | — |
| 8 | `ORDER BY cols [DESC]` | In what order? | No order asked |
| 9 | `LIMIT n` | How many rows? | No top-N asked |

### Step 1 — choose the left table (15 seconds)

| The question says | Left table |
|---|---|
| "all customers and their orders" | `customers` |
| "all orders and the customer" | `orders` |
| "all employees and their manager" | `employees` |
| "all departments and their employees" | `departments` |

Test: *which rows would make the answer incomplete if they disappeared?* Those must be the left
table's rows.

### Step 2 — choose the join type (10 seconds)

| Signal in the stem | Join |
|---|---|
| "including those with no / never / even if" | `LEFT JOIN` |
| "that have / with a matching" | `INNER JOIN` |
| Both sides must appear in full | `FULL OUTER JOIN` |
| Every combination | `CROSS JOIN` |

### Step 3 — write the `ON` condition (15 seconds)

```
ON alias2.<fk> = alias1.<pk>
```

Rules:
- Both sides qualified.
- The right side's foreign key first, the left side's primary key second (a convention, not a
  rule — the exam accepts either order).
- Never put the join condition in `WHERE` on a `LEFT JOIN`.

### Step 4 — `WHERE` (15 seconds)

Only if the question names a row-level condition: a city, a date range, an amount threshold, a
status.

```sql
WHERE c.city = 'Pune' AND o.amount > 400
```

### Steps 5 and 6 — `GROUP BY` and `HAVING` (20 seconds)

Ask: "does the question mention **how many**, **total**, **average**, **maximum**, or **more than
n**?"

- **Yes** → add `GROUP BY` (step 5). Add `HAVING` only if the filter is on the aggregate itself
  ("more than one order", "total above 1000").
- **No** → add neither.

`GROUP BY` must list **every** non-aggregated column in the `SELECT` list.

### Step 7 — `SELECT` (10 seconds)

List exactly the columns asked for, plus the aggregate if one is needed.

```sql
SELECT c.cust_name, COUNT(o.order_id) AS order_count
```

### Steps 8 and 9 — `ORDER BY` and `LIMIT` (10 seconds)

- Add `ORDER BY` only when the question says "ordered by", "highest", "top", "ascending".
- Add `LIMIT` only when the question says "top N", "first N", "limited to N".
- If you add `LIMIT`, add `ORDER BY` first, and add a tiebreaker if the sort key can tie.

### The whole recipe in 90 seconds

```
Step 1  FROM customers c
Step 2  LEFT JOIN
Step 3  ON o.cust_id = c.cust_id
Step 4  WHERE c.city = 'Pune'
Step 5  GROUP BY c.cust_id, c.cust_name
Step 6  HAVING COUNT(*) > 1
Step 7  SELECT c.cust_name, COUNT(o.order_id) AS n
Step 8  ORDER BY n DESC
Step 9  LIMIT 5
```

### MySQL vs standard SQL — the differences that matter

| Feature | Standard SQL | MySQL | MySQL note |
|---|---|---|---|
| Window functions | SQL:2003+ | **8.0+ only** | `ROW_NUMBER() OVER (PARTITION BY …)` fails on 5.7 |
| `LIMIT` | Not standard | `LIMIT n OFFSET m` | Also `LIMIT m, n` (MySQL only) |
| `FULL OUTER JOIN` | Yes | **No** | Emulate with `LEFT JOIN UNION RIGHT JOIN` |
| `INTERSECT` / `EXCEPT` | Yes | 8.0.31+ only | Use `IN`/`EXISTS` instead |
| `TOP n` | No | No | That is T-SQL (SQL Server) |
| `ROWNUM` | No | No | That is Oracle, and it behaves differently |
| String concatenation | `||` | `CONCAT()` | `||` means logical OR in MySQL by default |
| `LIMIT` without `ORDER BY` | Undefined | Undefined | Always add `ORDER BY` |

### The answer-format rules for free-response questions

1. **One statement.** No semicolon-separated pile.
2. **Use `JOIN` explicitly** rather than a comma-join with `WHERE`, so the grader can see the join
   type.
3. **Alias both tables** and qualify every join column.
4. **Do not add clauses the question did not ask for.** An unnecessary `GROUP BY` changes the
   result.
5. **Indent consistently.** It costs nothing and makes the query readable to a human grader.

## Worked example

**Q. Write a query to find each customer in Chennai with the total amount they have ordered, only
if that total exceeds 1000, ordered by total descending.**

**Reference answer**

```sql
SELECT c.cust_name,
       SUM(o.amount) AS total_ordered
FROM   customers c
JOIN   orders o ON o.cust_id = c.cust_id
WHERE  c.city = 'Chennai'
GROUP  BY c.cust_id, c.cust_name
HAVING SUM(o.amount) > 1000
ORDER  BY total_ordered DESC;
```

**Step-by-step**

| Step | Decision | Reason |
|---|---|---|
| 1 | `FROM customers c` | "each customer" — customers keep their rows. A customer with no order would have no total, so an inner join is acceptable here |
| 2 | `JOIN` (inner) | The question asks about totals; customers with no orders cannot have a total over 1000 |
| 3 | `ON o.cust_id = c.cust_id` | The foreign key to primary key |
| 4 | `WHERE c.city = 'Chennai'` | Row-level filter — it belongs in `WHERE`, not `HAVING` |
| 5 | `GROUP BY c.cust_id, c.cust_name` | "each customer" + a total → one row per customer |
| 6 | `HAVING SUM(o.amount) > 1000` | The filter is on the aggregate → `HAVING` |
| 7 | `SELECT c.cust_name, SUM(o.amount) AS total_ordered` | The columns asked for |
| 8 | `ORDER BY total_ordered DESC` | "ordered by total descending" |
| 9 | No `LIMIT` | Not asked |

**Expected output**

| cust_name | total_ordered |
|---|---|
| Rahul | 1200.00 |

**Why the near-misses are wrong**

| Near-miss | What breaks |
|---|---|
| `WHERE SUM(o.amount) > 1000` | Invalid — an aggregate cannot appear in `WHERE` |
| `HAVING c.city = 'Chennai'` | Legal but wrong order of work: it filters **groups** by a city that is not in the `GROUP BY`, and it drops the row-level filter before grouping |
| `GROUP BY c.cust_name` only | Works here by luck; fails if two customers share a name |
| Missing `HAVING` | Rahul's total (1200) is over 1000, but any Chennai customer under 1000 would wrongly appear |
| `ORDER BY SUM(o.amount)` vs `ORDER BY total_ordered` | Both work; the alias is shorter |

## Quick rules

- Left table first, and it is the table whose rows must survive.
- `ON` matches, `WHERE` filters rows, `GROUP BY` collapses, `HAVING` filters groups.
- Aggregates appear only in `SELECT`, `HAVING` and `ORDER BY`.
- `GROUP BY` lists every non-aggregated selected column.
- `COUNT(col)` and `COALESCE(SUM(...), 0)` when zeros matter.
- `ORDER BY` before `LIMIT`; add a tiebreaker.
- Window functions need MySQL 8+.
- Skip any clause the question did not ask for.

## Common traps

| Trap | Fix |
|---|---|
| Aggregate in `WHERE` | `HAVING` |
| `WHERE` for a right-table filter on a `LEFT JOIN` | `ON` |
| Unnecessary `GROUP BY` | Only group when aggregating |
| Missing `GROUP BY` column | Add every non-aggregated selected column |
| `COUNT(*)` for a zero-inclusive count | `COUNT(child.col)` |
| `LIMIT` without `ORDER BY` | Add both |
| `SELECT *` | Name the columns |
| Window function on MySQL 5.7 | Use a correlated subquery |

## Checklist

- [ ] I can write the eight-step order from memory.
- [ ] I identified the left table in 15 seconds using the "which rows would be missing" test.
- [ ] I put the row filter in `WHERE` and the aggregate filter in `HAVING`.
- [ ] I grouped by every non-aggregated selected column.
- [ ] I skipped every clause the question did not ask for.
- [ ] I added a tiebreaker to any `ORDER BY … LIMIT`.
- [ ] I checked the MySQL version for window functions.

## Related

- [Two-table query anatomy](../01-concepts/01-two-table-query-anatomy.md)
- [Task recipe cards](02-task-recipe-cards.md)
- [Solved query writing set](../03-worked-examples/01-solved-query-writing-set.md)
- [Query writing traps](../04-pitfalls/01-query-writing-traps.md)
- [Pattern library](../05-reference/01-query-writing-pattern-library.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
