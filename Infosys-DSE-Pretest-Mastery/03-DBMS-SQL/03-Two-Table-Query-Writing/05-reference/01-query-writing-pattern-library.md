# Query Writing Pattern Library — The Nine Patterns, Ready to Adapt

> Section 3 · DBMS & SQL · Two-Table Query Writing · _Estimated reading time: 5 min_
> **Prerequisite:** [Task recipe cards](../02-techniques/02-task-recipe-cards.md)

## In one sentence

Nine copy-and-adapt query patterns covering every "write a query for two tables" question the
pre-test asks.

## Why the pre-test tests this

- The archetype is free-response. A pattern you can adapt in 30 seconds is worth more than SQL you
  have to re-derive.
- Print this. On exam day you replace the table names and the column list, and you are done.

## Core concept

### Pattern 1 — list parent + child rows

```sql
SELECT p.name, c.value
FROM   parent p
LEFT JOIN child c ON c.parent_id = p.id;
```

### Pattern 2 — count per parent, including zeros

```sql
SELECT p.name, COUNT(c.id) AS child_count
FROM   parent p
LEFT JOIN child c ON c.parent_id = p.id
GROUP BY p.id, p.name;
```

### Pattern 3 — find parents with no children (anti-join)

```sql
SELECT p.name
FROM   parent p
LEFT JOIN child c ON c.parent_id = p.id
WHERE  c.id IS NULL;
```

```sql
-- NULL-safe, no join
SELECT p.name
FROM   parent p
WHERE  NOT EXISTS (SELECT 1 FROM child c WHERE c.parent_id = p.id);
```

### Pattern 4 — aggregate per parent

```sql
SELECT p.name, SUM(c.amount) AS total
FROM   parent p
JOIN   child c ON c.parent_id = p.id
GROUP BY p.id, p.name;
```

With zeros: `LEFT JOIN` + `COALESCE(SUM(c.amount), 0)`.

### Pattern 5 — filter on an aggregate

```sql
SELECT p.name, COUNT(c.id) AS child_count
FROM   parent p
LEFT JOIN child c ON c.parent_id = p.id
GROUP BY p.id, p.name
HAVING COUNT(c.id) > 1;
```

### Pattern 6 — top N overall

```sql
SELECT p.name, SUM(c.amount) AS total
FROM   parent p
JOIN   child c ON c.parent_id = p.id
GROUP BY p.id, p.name
ORDER BY total DESC
LIMIT 3;
```

### Pattern 7 — top N per group (MySQL 8+)

```sql
SELECT * FROM (
  SELECT c.cust_name, o.order_id, o.amount,
         ROW_NUMBER() OVER (PARTITION BY c.cust_id ORDER BY o.amount DESC) AS rn
  FROM   customers c JOIN orders o ON o.cust_id = c.cust_id
) t
WHERE t.rn <= 3;
```

### Pattern 8 — running total (MySQL 8+)

```sql
SELECT o.order_date, o.amount,
       SUM(o.amount) OVER (ORDER BY o.order_date, o.order_id) AS running_total
FROM   orders o;
```

### Pattern 9 — pairs (self-join)

```sql
SELECT a.name AS p1, b.name AS p2
FROM   people a
JOIN   people b ON a.city = b.city AND a.id < b.id;
```

### Clause quick card

| Clause | Position | Filters | Aggregate allowed | Alias allowed |
|---|---|---|---|---|
| `FROM` | 1 | — | — | — |
| `JOIN` | 2 | — | — | — |
| `ON` | 3 | Match condition | — | — |
| `WHERE` | 4 | Rows | **No** | No |
| `GROUP BY` | 5 | — | — | No |
| `HAVING` | 6 | Groups | Yes | Yes |
| `SELECT` | 7 | — | Yes | Defines aliases |
| `DISTINCT` | 8 | — | — | — |
| `ORDER BY` | 9 | — | Yes | Yes |
| `LIMIT` | 10 | — | — | — |

### Engine differences

| Feature | MySQL | Standard SQL / others |
|---|---|---|
| `LIMIT n OFFSET m` | ✅ | PostgreSQL ✅, Oracle needs `OFFSET m ROWS FETCH NEXT n ROWS ONLY` |
| Window functions | **8.0+ only** | SQL:2003+ |
| `FULL OUTER JOIN` | ❌ | ✅ |
| `INTERSECT` / `EXCEPT` | 8.0.31+ only | ✅ |
| `CONCAT(a, b)` | ✅ | MySQL-specific; standard is `a \|\| b` |
| `IFNULL(a, b)` | ✅ | Standard is `COALESCE(a, b)` — use `COALESCE` everywhere |

### Style rules that cost nothing and gain marks

1. Alias both tables (`c`, `o`) and qualify every join column.
2. Name every output column with `AS`.
3. One statement, one indentation style.
4. No `SELECT *` on a join.
5. No clause the question did not ask for.

## Worked example

**Q. "Show the top 2 orders by amount for each customer, with the customer name." (MySQL 8+)**

```sql
SELECT * FROM (
  SELECT c.cust_name,
         o.order_id,
         o.amount,
         ROW_NUMBER() OVER (PARTITION BY c.cust_id ORDER BY o.amount DESC) AS rn
  FROM   customers c
  JOIN   orders o ON o.cust_id = c.cust_id
) t
WHERE t.rn <= 2;
```

**Output on the shared fixture**

| cust_name | order_id | amount | rn |
|---|---|---|---|
| Ananya | 1002 | 750.00 | 1 |
| Ananya | 1001 | 500.00 | 2 |
| Rahul | 1003 | 1200.00 | 1 |
| Meera | 1004 | 300.00 | 1 |
| Karthik | 1006 | 1100.00 | 1 |
| Karthik | 1005 | 950.00 | 2 |

**Why the outer wrapper:** `WHERE` runs before window functions, so `rn` does not exist yet when
`WHERE` is evaluated. The subquery computes the window, and the outer query filters on it.

## Quick rules

- Nine patterns cover the whole archetype.
- Pattern 2 uses `COUNT(c.id)`, Pattern 4 uses `COALESCE` when zeros are needed.
- Pattern 3 is the anti-join; never `NOT IN` on a nullable foreign key.
- Pattern 6: `ORDER BY` then `LIMIT`.
- Pattern 7 needs MySQL 8+ and an outer wrapper.
- Use `COALESCE`, not `IFNULL` — it is standard SQL.

## Common traps

| Trap | Fix |
|---|---|
| `COUNT(*)` in Pattern 2 | `COUNT(c.id)` |
| `NOT IN` in Pattern 3 | `NOT EXISTS` |
| `WHERE` on an aggregate in Pattern 5 | `HAVING` |
| `LIMIT` without `ORDER BY` in Pattern 6 | Add both |
| Window function filtered in the same `WHERE` in Pattern 7 | Wrap it |

## Checklist

- [ ] I can name the pattern from the stem in 10 seconds.
- [ ] I adapted the pattern rather than writing from scratch.
- [ ] I qualified every join column.
- [ ] I used `COALESCE` rather than `IFNULL`.
- [ ] I checked the MySQL version before using a window function.
- [ ] I removed any clause the question did not ask for.

## Related

- [Two-table query anatomy](../01-concepts/01-two-table-query-anatomy.md)
- [The eight-step recipe](../02-techniques/01-the-eight-step-recipe.md)
- [Task recipe cards](../02-techniques/02-task-recipe-cards.md)
- [Solved query writing set](../03-worked-examples/01-solved-query-writing-set.md)
- [Query writing traps](../04-pitfalls/01-query-writing-traps.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
