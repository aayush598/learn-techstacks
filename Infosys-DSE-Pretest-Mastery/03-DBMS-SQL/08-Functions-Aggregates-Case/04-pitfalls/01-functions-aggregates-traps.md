# Functions and Aggregates Traps — Where Candidates Lose the Mark

> Section 3 · DBMS & SQL · Functions, Aggregates & CASE · _Estimated reading time: 5 min_
> **Prerequisite:** [Functions, aggregates and CASE](../01-concepts/01-functions-aggregates-and-case.md)

## In one sentence

Nine traps, each one a real function offered in the wrong place, or a wrong count on the fixture.

## Why the pre-test tests this

- The function archetype is the most frequent question type in DBMS sections.
- The wrong options are always **plausible function names** — precision is the entire skill.

## Core concept

### Trap 1 — `COUNT(*)` vs `COUNT(col)` vs `COUNT(DISTINCT col)`

| You want | Use |
|---|---|
| Number of **rows** | `COUNT(*)` |
| Number of rows where `col` **has a value** | `COUNT(col)` |
| Number of **different** values | `COUNT(DISTINCT col)` |

On the fixture, `orders` has 6 rows, 6 non-NULL `cust_id` values and 4 distinct `cust_id` values.
The three answers are **6, 6 and 4** — and the exam's option set usually contains 5 and 7 as the
near-misses.

### Trap 2 — Counting the wrong table

"Customers who have placed at least one order" — the count must come from **`orders`**. Counting
`cust_id` over `customers` gives 5 and includes Vikram, who has none.

### Trap 3 — Row count vs group count

`GROUP BY cust_id` over `orders` gives **4** groups, not 6 rows and not 5 customers. The moment
`GROUP BY` appears, switch from "rows" to "groups".

### Trap 4 — An aggregate with no `GROUP BY` returns one row

`SELECT COUNT(*) FROM orders;` returns **one row** with the value 6. It does not return 6 rows. The
option "6 rows" is a trap.

### Trap 5 — `WHERE` vs `HAVING`

`WHERE` runs **before** grouping. An aggregate condition belongs in `HAVING`. If the question's
condition mentions `COUNT`, `SUM`, `AVG`, `MIN` or `MAX`, it goes in `HAVING` — always.

### Trap 6 — `= NULL` vs `IS NULL`

`city = NULL` is **never true** — not even for a NULL city. The only correct test is
`city IS NULL`. Any option using `= NULL` is wrong, and any `CASE` using `= NULL` will always take
its `ELSE` branch.

### Trap 7 — `CASE` branches read in the wrong order

`CASE` takes the **first** matching `WHEN`. For `order_amt = 1200` with
`WHEN >= 1000 THEN 'High' WHEN >= 750 THEN 'Medium'`, the answer is `'High'` — the second branch is
never evaluated. Candidates who scan for the "best match" instead of the "first match" get
`'Medium'`.

### Trap 8 — `CASE` without `ELSE`

The result is `NULL`, not `''` and not a default label. If the question asks what a `CASE` returns
when nothing matches, the answer is `NULL` unless the `CASE` has an `ELSE`.

### Trap 9 — `ROW_NUMBER` vs `RANK` vs `DENSE_RANK`

| Requirement | Function |
|---|---|
| Unique numbers, never a tie | `ROW_NUMBER()` |
| Ties share a rank, gaps appear (1, 2, 2, 4) | `RANK()` |
| Ties share a rank, no gaps (1, 2, 2, 3) | `DENSE_RANK()` |

### Bonus trap 1 — `CONCAT` vs `CONCAT_WS` with NULL

`CONCAT('a', NULL, 'b')` → **`NULL`**. `CONCAT_WS('-', 'a', NULL, 'b')` → `'a-b'` — `CONCAT_WS`
skips the NULL. If the question is about NULLs in string joins, this is the answer.

### Bonus trap 2 — `ROUND` vs `TRUNC` vs `CEIL` vs `FLOOR`

| Input | `ROUND` | `TRUNC` | `CEIL` | `FLOOR` |
|---|---|---|---|---|
| 2.7 | 3 | 2 | 3 | 2 |
| -2.7 | -3 | -2 | -2 | -3 |

`TRUNC` truncates **toward zero**; `FLOOR` rounds down. They agree on positives and differ on
negatives. `ROUND` rounds half away from zero.

### Bonus trap 3 — `AVG` denominator

`AVG(col)` divides by the number of **non-NULL** values. `SUM(col) / COUNT(*)` divides by all rows.
When `col` has NULLs the two differ — and this is the classic exam pair.

### Bonus trap 4 — `GROUP_CONCAT` is not `CONCAT_WS`

`GROUP_CONCAT` is an **aggregate** — it gathers values across the rows of a group. `CONCAT_WS` is
**scalar** — it joins arguments within one row. Offering `CONCAT_WS` for a "list of values in a
group" question is the standard wrong option.

## Worked example

**Q. Which expression returns the average order amount, treating rows where `order_amt` is NULL as
excluded?**

- A. `SUM(order_amt) / COUNT(*)`
- B. `AVG(order_amt)`
- C. `SUM(order_amt) / NULLIF(COUNT(*), 0)`
- D. `COUNT(order_amt) / COUNT(*)`

**Solution**

`AVG(col)` **ignores NULLs** in both the numerator and the denominator, which is exactly "treat
NULL rows as excluded".

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | `SUM` skips NULLs but `COUNT(*)` counts **all** rows including NULL rows, so the denominator is too large and the average comes out too low |
| C | Same denominator problem as A |
| D | This is a **ratio of counts**, not an average amount |

## Quick rules

- `COUNT(*)` rows, `COUNT(col)` non-NULL, `COUNT(DISTINCT col)` distinct.
- Count from the table that holds the qualifying rows.
- `GROUP BY` → count groups.
- Aggregate with no `GROUP BY` → 1 row.
- Aggregate filter → `HAVING`.
- `IS NULL`, never `= NULL`.
- `CASE`: first match wins; no `ELSE` → `NULL`.
- `ROW_NUMBER` no ties, `RANK` skips, `DENSE_RANK` does not.
- `CONCAT` propagates NULL; `CONCAT_WS` skips it.
- `AVG` uses the non-NULL count as the denominator.
- `GROUP_CONCAT` = aggregate; `CONCAT_WS` = scalar.

## Common traps

| Trap | The tell in the option |
|---|---|
| `COUNT(*)` offered for "distinct values" | No `DISTINCT` |
| Counting over the wrong table | Includes a customer with no orders |
| Row count offered for a `GROUP BY` result | Same number as the table |
| "6 rows" for an aggregate with no `GROUP BY` | Should be 1 row |
| `WHERE` offered for an aggregate filter | — |
| `= NULL` in a `CASE` or `WHERE` | Never true |
| `CONCAT` offered where NULLs must be skipped | `CONCAT_WS` is the answer |
| `CONCAT_WS` offered for a group list | `GROUP_CONCAT` is the answer |
| `RANK` and `DENSE_RANK` swapped | Check the gap behaviour |

## Checklist

- [ ] I can name the three `COUNT` variants and their values on the fixture.
- [ ] I can tell a row count from a group count.
- [ ] I always put aggregate filters in `HAVING`.
- [ ] I use `IS NULL`.
- [ ] I read `CASE` top to bottom, first match wins.
- [ ] I know the `ROW_NUMBER` / `RANK` / `DENSE_RANK` gap rules.
- [ ] I know `CONCAT` vs `CONCAT_WS` vs `GROUP_CONCAT`.
- [ ] I know the `ROUND` / `TRUNC` / `CEIL` / `FLOOR` differences.

## Related

- [Functions, aggregates and CASE](../01-concepts/01-functions-aggregates-and-case.md)
- [Function selection procedures](../02-techniques/01-function-selection-procedures.md)
- [Solved functions and aggregates set](../03-worked-examples/01-solved-functions-aggregates-set.md)
- [Functions and aggregates quick check](../05-reference/01-functions-aggregates-quick-check.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
