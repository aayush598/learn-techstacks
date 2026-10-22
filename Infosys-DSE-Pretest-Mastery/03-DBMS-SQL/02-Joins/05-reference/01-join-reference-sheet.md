# Join Reference Sheet — Every Join, Every Row Count

> Section 3 · DBMS & SQL · Joins · _Estimated reading time: 5 min_
> **Prerequisite:** [The six joins](../01-concepts/01-the-six-joins.md)

## In one sentence

One page: the six join types, what each keeps, the row count on the shared fixture, and the
sentence to use when the exam asks "which join".

## Why the pre-test tests this

- Joins are 2–3 of the 10 DBMS questions. This sheet answers every "which join" question in 20
  seconds.
- The row counts on the fixture let you verify a join answer in 5 seconds instead of tracing.

## Core concept

### The six joins at a glance

| Join | Keeps | Unmatched left | Unmatched right | Fixture rows |
|---|---|---|---|---|
| `INNER JOIN` / `JOIN` | Matches only | Dropped | Dropped | 6 |
| `LEFT OUTER JOIN` | All left rows | **Kept, NULLs** | Dropped | 7 |
| `RIGHT OUTER JOIN` | All right rows | Dropped | **Kept, NULLs** | 7 (when right = customers) |
| `FULL OUTER JOIN` | Everything | Kept, NULLs | Kept, NULLs | 7 |
| `CROSS JOIN` | Everything | Kept | Kept | 30 |
| `SELF JOIN` | Per inner/left type | per type | per type | 6 (employees: 6 rows) |

### Row counts on the shared fixture

| Query shape | Rows |
|---|---|
| `customers JOIN orders` | 6 |
| `customers LEFT JOIN orders` | 7 |
| `orders JOIN customers` | 6 |
| `orders LEFT JOIN customers` | 6 |
| `orders RIGHT JOIN customers` | 7 |
| `customers CROSS JOIN orders` | 30 |
| `employees e LEFT JOIN employees m` (manager) | 6 |
| `customers NATURAL JOIN orders` | 6 rows, **6 columns** |
| `customers JOIN orders` with `SELECT *` | 6 rows, **7 columns** |

### The "which join" one-liner

| The stem says | Write |
|---|---|
| only those that have / that match | `INNER JOIN` |
| all X, including those with no Y | `X LEFT JOIN Y` |
| X that have never had Y | `X LEFT JOIN Y ... WHERE Y.id IS NULL` |
| all X **and** all Y | `FULL OUTER JOIN` |
| every combination | `CROSS JOIN` |
| X with its parent / manager / category | `LEFT JOIN` on the parent |
| two mentions of the same table | `SELF JOIN` with two aliases |
| students and courses | join through the junction table |

### Join type → row survival rule

```
INNER   = A ∩ B
LEFT    = A ∪ (A \ B with NULLs)
RIGHT   = B ∪ (B \ A with NULLs)
FULL    = A ∪ B with NULLs
CROSS   = A × B
```

### Where the condition goes

| Clause | Purpose | Trap |
|---|---|---|
| `ON` | Match condition | — |
| `WHERE` | Filter the joined rows | On a `LEFT JOIN`, filters away the NULL-padded rows |

```sql
-- 7 rows: keeps Vikram
LEFT JOIN orders o ON c.cust_id = o.cust_id

-- 5 rows: Vikram gone
LEFT JOIN orders o ON c.cust_id = o.cust_id WHERE o.amount > 400

-- 7 rows: Vikram kept, only big orders matched
LEFT JOIN orders o ON c.cust_id = o.cust_id AND o.amount > 400
```

### Count cheat

| Question | Expression |
|---|---|
| How many rows in the result? | `COUNT(*)` |
| How many matched rows? | `COUNT(right.col)` |
| How many distinct left entities? | `COUNT(DISTINCT left.id)` |
| How many left entities, including zeros? | `COUNT(right.col)` with `GROUP BY left.id` |
| How many left entities with at least one match? | `COUNT(DISTINCT left.id)` on the inner join |

### Join syntax forms

| Form | Meaning |
|---|---|
| `JOIN t2 ON a.id = b.a_id` | Explicit condition (use this) |
| `JOIN t2 USING (id)` | Join on named columns; the column appears once |
| `NATURAL JOIN t2` | Join on all same-named columns; **avoid** |
| `JOIN t2 ON a.id = b.a_id AND a.x > 5` | Extra right-side filter stays in `ON` for a `LEFT JOIN` |
| `FROM t1, t2 WHERE t1.id = t2.id` | Old-style join; equivalent to an inner join |
| `FROM t1, t2` | Old-style **cross** join |

### MySQL notes

| Feature | MySQL status |
|---|---|
| `INNER`, `LEFT`, `RIGHT`, `CROSS` | Supported |
| `FULL OUTER JOIN` | **Not supported** — emulate with `LEFT JOIN UNION RIGHT JOIN` |
| `INTERSECT` / `EXCEPT` | 8.0.31+ only |
| Window functions | 8.0+ only |
| `LIMIT` / `OFFSET` | Supported (also `LIMIT m, n`) |

## Worked example

**Q. Which query returns one row per customer, showing the customer name and their order count,
including customers with zero orders?**

- A. `SELECT c.cust_name, COUNT(o.order_id) FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id, c.cust_name;`
- B. `SELECT c.cust_name, COUNT(*) FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id;`
- C. `SELECT c.cust_name, COUNT(o.order_id) FROM customers c JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id;`
- D. `SELECT c.cust_name, COUNT(*) FROM customers c, orders o WHERE c.cust_id = o.cust_id GROUP BY c.cust_id;`

**Solution**

| Requirement | Must be |
|---|---|
| One row per customer, including zero-order customers | `LEFT JOIN` + `GROUP BY` the customer |
| Correct count, 0 for Vikram | `COUNT(o.order_id)`, not `COUNT(*)` |
| Group by the right columns | `GROUP BY c.cust_id, c.cust_name` |

**Answer: A.** Output: Ananya 2, Rahul 1, Meera 1, Karthik 2, Vikram **0**.

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | `COUNT(*)` counts the NULL-padded row → Vikram shows **1** instead of 0 |
| C | `JOIN` drops Vikram entirely — only 4 rows |
| D | Old-style inner join; Vikram is dropped, and `COUNT(*)` is wrong anyway |

## Quick rules

- The join type decides which side's unmatched rows survive.
- `ON` matches; `WHERE` filters. A right-table `WHERE` erases the `LEFT JOIN`.
- `COUNT(*)`, `COUNT(col)`, `COUNT(DISTINCT col)` — pick by what you are counting.
- `NATURAL JOIN` = all same-named columns, joined column shown once.
- `RIGHT JOIN` keeps the right table's rows.
- `FULL OUTER JOIN` is not in MySQL.
- Self-join → two aliases.

## Common traps

| Trap | Correct |
|---|---|
| `WHERE` on the right of a `LEFT JOIN` | Move it to `ON` |
| `COUNT(*)` for "count of children" | `COUNT(child.id)` |
| `NATURAL JOIN` shows shared columns twice | It shows them once |
| `RIGHT JOIN` keeps the left table | It keeps the right table |
| `FULL OUTER JOIN` in MySQL | Not supported |

## Checklist

- [ ] I can state the fixture row count for all six join types.
- [ ] I know what `ON` vs `WHERE` does on a `LEFT JOIN`.
- [ ] I can pick the right `COUNT` expression for the question.
- [ ] I know `FULL OUTER JOIN` is not in MySQL.
- [ ] I can answer any "which join" question in 20 seconds.

## Related

- [The six joins](../01-concepts/01-the-six-joins.md)
- [Join decision table](../02-techniques/01-join-decision-table.md)
- [Solved join set](../03-worked-examples/01-solved-join-set.md)
- [Join traps](../04-pitfalls/01-join-traps.md)
- [Join cheat sheet](02-join-cheat-sheet.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
