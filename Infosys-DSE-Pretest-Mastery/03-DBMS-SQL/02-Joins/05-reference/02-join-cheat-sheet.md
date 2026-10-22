# Join Cheat Sheet — The One Page to Print

> Section 3 · DBMS & SQL · Joins · _Estimated reading time: 3 min_
> **Prerequisite:** [The six joins](../01-concepts/01-the-six-joins.md)

## In one sentence

The smallest possible revision sheet: six join types, three sentences, four numbers.

## Why the pre-test tests this

- If you are out of time the night before, this is the file to read. It covers archetype (a) —
  "SQL up to JOINs" — which is 2–3 of the 10 questions.
- Three minutes of reading, three questions saved.

## Core concept

### The six joins

```
INNER JOIN  →  keep rows that match on both sides
LEFT  JOIN  →  keep EVERY left row; unmatched right side is NULL
RIGHT JOIN  →  keep EVERY right row; unmatched left side is NULL
FULL  JOIN  →  keep every row from both sides          (not in MySQL)
CROSS JOIN  →  every row × every row                   (no ON clause)
SELF  JOIN  →  a table joined to itself                (two aliases)
```

### Three sentences that answer most questions

1. **"including those with none" → `LEFT JOIN`.**
2. **"who have never" → `LEFT JOIN` + `WHERE right.id IS NULL`.**
3. **"only those that have" → `INNER JOIN`.**

### Four numbers to memorise (shared fixture)

| Number | What it is |
|---|---|
| 5 | customers |
| 6 | orders, and the row count of `customers JOIN orders` |
| 7 | row count of `customers LEFT JOIN orders` |
| 30 | row count of `customers CROSS JOIN orders` (5 × 6) |

### The three traps in one line each

- `WHERE right.col = x` on a `LEFT JOIN` = an `INNER JOIN`. Move it to `ON`.
- `COUNT(*)` after a fan-out counts join rows, not entities. Use `COUNT(DISTINCT id)`.
- `NATURAL JOIN` matches **every** same-named column; `SELECT *` shows the joined column once.

## Worked example

**Q. "List all customers with their order counts, including customers who have never ordered."**

```sql
SELECT c.cust_name, COUNT(o.order_id) AS order_count
FROM   customers c
LEFT JOIN orders o ON c.cust_id = o.cust_id
GROUP  BY c.cust_id, c.cust_name;
```

`LEFT JOIN` (escape clause) + `COUNT(o.order_id)` (skips the NULL row) → Ananya 2, Rahul 1, Meera 1,
Karthik 2, Vikram 0.

## Quick rules

- Escape clause → `LEFT`. Restriction clause → `INNER`. Combination → `CROSS`.
- Left table = the one whose rows must survive.
- `ON` matches, `WHERE` filters.
- `COUNT(*)` vs `COUNT(col)` vs `COUNT(DISTINCT col)`.
- `NATURAL JOIN` = all same-named columns.
- `RIGHT JOIN` keeps the right table.

## Common traps

| Trap | Fix |
|---|---|
| `WHERE` kills a `LEFT JOIN` | Move to `ON` |
| `COUNT(*)` overcounts | `COUNT(DISTINCT id)` |
| `NATURAL JOIN` unexpected column | Use explicit `ON` |
| `RIGHT JOIN` direction | Rewrite as `LEFT` with tables swapped |

## Checklist

- [ ] I can write all six join types from memory.
- [ ] I can quote the three sentence-rules.
- [ ] I know 5, 6, 7 and 30 for the fixture.
- [ ] I would answer any "which join" question in 20 seconds.

## Related

- [The six joins](../01-concepts/01-the-six-joins.md)
- [Join decision table](../02-techniques/01-join-decision-table.md)
- [Solved join set](../03-worked-examples/01-solved-join-set.md)
- [Join traps](../04-pitfalls/01-join-traps.md)
- [Join reference sheet](01-join-reference-sheet.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
