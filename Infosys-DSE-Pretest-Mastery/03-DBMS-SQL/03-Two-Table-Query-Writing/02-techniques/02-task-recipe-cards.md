# Task Recipe Cards — Seven Queries You Will Be Asked to Write

> Section 3 · DBMS & SQL · Two-Table Query Writing · _Estimated reading time: 8 min_
> **Prerequisite:** [The eight-step recipe](01-the-eight-step-recipe.md)

## In one sentence

**Seven task types cover almost every "write a query for two tables" question** — recognise the
task type, paste the card, change the table names.

## Why the pre-test tests this

- Free-response questions are drawn from a small set of task types. Recognising the type is worth
  30 seconds.
- Each card below is a template you can adapt in under a minute.
- Meera knows the SQL but loses time re-deriving the shape. The cards remove that step.

## Core concept

### The seven task types

| # | Task type | The stem sounds like | Card |
|---|---|---|---|
| 1 | List parent + child rows | "show all X with their Y" | A |
| 2 | Count per parent, including zeros | "how many Y does each X have" | B |
| 3 | Find parents with none | "X that have no Y" | C |
| 4 | Aggregate per parent | "total/average/max amount per X" | D |
| 5 | Filter on an aggregate | "X with more than N Y" | E |
| 6 | Top N | "top 3 X by Y" | F |
| 7 | Top N per group / running total | "top 2 orders per customer", "running balance" | G |

### Card A — list parent and child rows

```sql
SELECT p.name, c.value
FROM   parent p
LEFT JOIN child c ON c.parent_id = p.id;
```

Use `INNER JOIN` if the stem says "that have", "with a matching", "for each Y".

### Card B — count per parent, including zeros

```sql
SELECT p.name, COUNT(c.id) AS child_count
FROM   parent p
LEFT JOIN child c ON c.parent_id = p.id
GROUP BY p.id, p.name;
```

- `COUNT(c.id)` — **not** `COUNT(*)` — so the zero case is reported as 0.
- `GROUP BY p.id, p.name` — every non-aggregated selected column.

### Card C — find parents with none (anti-join)

```sql
SELECT p.name
FROM   parent p
LEFT JOIN child c ON c.parent_id = p.id
WHERE  c.id IS NULL;
```

NULL-safe alternative without a join:

```sql
SELECT p.name
FROM   parent p
WHERE  NOT EXISTS (SELECT 1 FROM child c WHERE c.parent_id = p.id);
```

Never `NOT IN (SELECT parent_id FROM child)` when the child table can contain a NULL foreign key.

### Card D — aggregate per parent

```sql
SELECT p.name, SUM(c.amount) AS total
FROM   parent p
JOIN   child c ON c.parent_id = p.id
GROUP BY p.id, p.name;
```

Use `LEFT JOIN` + `COALESCE(SUM(c.amount), 0)` when zeros are required.

### Card E — filter on an aggregate

```sql
SELECT p.name, COUNT(c.id) AS child_count
FROM   parent p
LEFT JOIN child c ON c.parent_id = p.id
GROUP BY p.id, p.name
HAVING COUNT(c.id) > 1;
```

The filter is on the aggregate → `HAVING`. The `WHERE` clause cannot hold `COUNT(...)`.

### Card F — top N overall

```sql
SELECT p.name, SUM(c.amount) AS total
FROM   parent p
JOIN   child c ON c.parent_id = p.id
GROUP BY p.id, p.name
ORDER BY total DESC
LIMIT 3;
```

Always `ORDER BY` before `LIMIT`. Add `, p.id` as a tiebreaker when the sort key can tie.

### Card G — top N per group (window function, MySQL 8+)

```sql
SELECT * FROM (
  SELECT c.cust_name,
         o.order_id,
         o.amount,
         ROW_NUMBER() OVER (PARTITION BY c.cust_id ORDER BY o.amount DESC) AS rn
  FROM   customers c
  JOIN   orders o ON o.cust_id = c.cust_id
) t
WHERE t.rn <= 3;
```

- `ROW_NUMBER()` for a strict top-N; `RANK()` if ties should all appear; `DENSE_RANK()` if ties
  should appear without gaps.
- The window function cannot be filtered in the same `WHERE` — wrap it in a subquery.
- **MySQL 5.7 fallback** (correlated subquery):

```sql
SELECT c.cust_name, o.order_id, o.amount
FROM   customers c JOIN orders o ON o.cust_id = c.cust_id
WHERE  (SELECT COUNT(*) FROM orders o2
        WHERE o2.cust_id = o.cust_id AND o2.amount > o.amount) < 3
ORDER BY c.cust_id, o.amount DESC;
```

### Card H — running total (window function, MySQL 8+)

```sql
SELECT o.order_date,
       o.amount,
       SUM(o.amount) OVER (ORDER BY o.order_date, o.order_id) AS running_total
FROM   orders o;
```

### Card I — "find pairs" (self-join)

```sql
SELECT a.name AS person_1, b.name AS person_2
FROM   people a
JOIN   people b ON a.city = b.city AND a.id < b.id;
```

The `a.id < b.id` guard stops each pair appearing twice.

### The card-selection scanner

| The stem contains | Use |
|---|---|
| "including", "even if", "never" | Card A or B with `LEFT JOIN` |
| "how many" | Card B or E |
| "no", "never", "none" | Card C |
| "total", "average", "maximum", "sum" | Card D |
| "more than", "at least", "fewer than" | Card E |
| "top", "highest", "first", "lowest" | Card F (add `ORDER BY` + `LIMIT`) |
| "per", "for each", "each" | `GROUP BY` is required |
| "running", "cumulative" | Card H (MySQL 8+) |
| "pairs", "together with each other" | Card I |
| "with the count of" | `COUNT(child.col)`, not `COUNT(*)` |

### Running the cards on the shared fixture

| Card | Query result on the fixture |
|---|---|
| A (`LEFT JOIN`) | 7 rows: Ananya ×2, Rahul, Meera, Karthik ×2, Vikram (NULLs) |
| B (`COUNT(o.order_id)`) | Ananya 2, Rahul 1, Meera 1, Karthik 2, Vikram 0 |
| C (anti-join) | 1 row: Vikram |
| D (`SUM(o.amount)`) | Ananya 1250, Rahul 1200, Meera 300, Karthik 2050 |
| E (`HAVING COUNT(*) > 1`) | Ananya 2, Karthik 2 |
| F (top 2 by total) | Karthik 2050, Ananya 1250 |
| G (top 1 order per customer) | 4 rows: Ananya 750, Rahul 1200, Meera 300, Karthik 1100 |
| I (same-city pairs) | 1 pair: Ananya, Meera |

## Worked example

**Q. "Write a query to list each customer in Pune together with the number of orders they have
placed, including customers who have placed none."**

**Card B + a `WHERE` filter.**

```sql
SELECT c.cust_name,
       COUNT(o.order_id) AS order_count
FROM   customers c
LEFT JOIN orders o ON o.cust_id = c.cust_id
WHERE  c.city = 'Pune'
GROUP BY c.cust_id, c.cust_name;
```

**Expected output**

| cust_name | order_count |
|---|---|
| Ananya | 2 |
| Meera | 1 |

**Step-by-step**

| Step | Decision |
|---|---|
| Left table | `customers` — "each customer", and "including none" |
| Join type | `LEFT JOIN` — the escape clause |
| `ON` | `o.cust_id = c.cust_id` |
| `WHERE` | `c.city = 'Pune'` — row-level filter, before grouping |
| `GROUP BY` | `c.cust_id, c.cust_name` — "each customer" |
| `HAVING` | None — no aggregate filter asked for |
| `SELECT` | `c.cust_name, COUNT(o.order_id)` |
| `ORDER BY` / `LIMIT` | None |

**Near-misses**

| Near-miss | What breaks |
|---|---|
| `COUNT(*)` | The NULL-padded row counts as 1 — Vikram would show 1, not 0 |
| `JOIN` instead of `LEFT JOIN` | Vikram disappears |
| `WHERE` after `GROUP BY` | Syntax error in standard SQL |
| `GROUP BY c.cust_name` | Works by luck; the id is the real key |

**Note:** on this data Vikram is in Bengaluru, so the "including none" clause does not change the
answer. A good examiner would put the zero case inside the filter. Do not rely on the data saving
you — write the query the stem asks for.

## Quick rules

- Recognise the task type first; the rest is a template.
- `LEFT JOIN` when "including" appears; `INNER JOIN` when "that have" appears.
- `COUNT(child.col)` for zero-inclusive counts.
- `HAVING` for aggregate filters, `WHERE` for row filters.
- `COALESCE(SUM(x), 0)` when zeros are required.
- `ORDER BY` then `LIMIT`; add a tiebreaker.
- Window functions: MySQL 8+, and wrap them to filter on the window result.

## Common traps

| Trap | Fix |
|---|---|
| `COUNT(*)` in Card B | `COUNT(child.col)` |
| `WHERE` instead of `HAVING` in Card E | `HAVING` |
| `NOT IN` in Card C | `NOT EXISTS` or the anti-join |
| Missing `ORDER BY` in Card F | Add it before `LIMIT` |
| Window function filtered in the same `WHERE` | Wrap in a subquery |
| `SUM` over zero rows returns `NULL` | `COALESCE(..., 0)` |
| Pair duplication in Card I | Add `a.id < b.id` |

## Checklist

- [ ] I can name the task type from the stem in 10 seconds.
- [ ] I chose the card, then adapted it.
- [ ] I used `COUNT(child.col)` and `COALESCE` where zeros matter.
- [ ] I put the aggregate filter in `HAVING`.
- [ ] I added `ORDER BY` before `LIMIT` with a tiebreaker.
- [ ] I checked the MySQL version before using a window function.
- [ ] I verified the expected output on the fixture before moving on.

## Related

- [Two-table query anatomy](../01-concepts/01-two-table-query-anatomy.md)
- [The eight-step recipe](01-the-eight-step-recipe.md)
- [Solved query writing set](../03-worked-examples/01-solved-query-writing-set.md)
- [Query writing traps](../04-pitfalls/01-query-writing-traps.md)
- [Pattern library](../05-reference/01-query-writing-pattern-library.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
