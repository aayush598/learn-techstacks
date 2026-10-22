# Output Identification Traps — Where the Trace Goes Wrong

> Section 3 · DBMS & SQL · Query Output Identification · _Estimated reading time: 6 min_
> **Prerequisite:** [The five-step execution model](../01-concepts/01-five-step-execution-model.md)

## In one sentence

**Eight ways to get an output question wrong, and every one of them is a skipped step** — you
stopped tracing after stage 1 or stage 2.

## Why the pre-test tests this

- Output questions are 2 of the 10 DBMS questions, and the distractors are built precisely from
  the intermediate results of the trace.
- The option that equals your stage-2 row count, or your stage-1 row count, is almost always a
  trap option.
- Learning to *check which stage* an option belongs to turns a guess into a 20-second decision.

## Core concept

### Trap 1 — you stopped after stage 1

The option list contains the row count **after the join**, **after the `WHERE`**, **after the
`GROUP BY`**, and **after `HAVING`**. Each is a trap for a candidate who stopped tracing too early.

**Guard:** identify which stage each option corresponds to before choosing.

| Option value | Stage it represents |
|---|---|
| 30 | Stage 1 with a cartesian product (no `ON` match) |
| 7 | Stage 1 with a `LEFT JOIN` from `customers` |
| 6 | Stage 1 with an inner join |
| 5 | Stage 2, after `WHERE o.amount > 400` |
| 4 | Stage 3, after `GROUP BY c.cust_name` on an inner join |
| 2 | Stage 4, after `HAVING COUNT(*) > 1` |

### Trap 2 — you counted entities, not rows

`COUNT(*)` after a join counts **join rows**. Customers 101 and 104 each have 2 orders, so the
inner join gives 6 rows for 4 customers and 7 rows for 5 customers with a left join.

**Guard:** after a join, always list the rows before counting.

### Trap 3 — the `WHERE` deleted the NULL-padded row

On a `LEFT JOIN`, `WHERE right.col > x` drops the unmatched left rows because `NULL > x` is
`UNKNOWN`. The join silently becomes an inner join.

**Guard:** cross out the NULL row explicitly and note it in the margin.

### Trap 4 — you thought `NULL` comparisons are "false but kept"

`NULL = 5`, `NULL > 400`, `NULL <> 5` are all `UNKNOWN`. `WHERE` keeps only rows where the
predicate is `TRUE`, so `UNKNOWN` rows are dropped — the same as `FALSE`.

**Guard:** treat a NULL row as **dead** unless the predicate is `IS NULL`.

### Trap 5 — `COUNT(*)` vs `COUNT(col)`

After a `LEFT JOIN`, `COUNT(*)` counts the NULL-padded row and `COUNT(col)` does not. The
difference is exactly the number of unmatched left rows (1 on this fixture).

**Guard:** read the exact expression in the `SELECT` list.

### Trap 6 — you forgot that `GROUP BY` collapses

7 join rows → 5 groups → 2 groups after `HAVING`. Three different numbers, and the options usually
contain all three.

**Guard:** write the group count, not the row count, once you reach stage 3.

### Trap 7 — `DISTINCT` applies to the whole row

`SELECT DISTINCT c.city, c.cust_name` only removes rows where **both** columns repeat. It is not a
per-column filter.

**Guard:** count the distinct **combinations**, not the distinct values of one column.

### Trap 8 — `LIMIT` before sorting

`LIMIT 2` with no `ORDER BY` gives an arbitrary 2 rows. And with a tie at the cut line, even
`ORDER BY` is non-deterministic.

**Guard:** if the query has `LIMIT`, find the `ORDER BY` first, then check whether the cut line is
a tie.

### Trap 9 — no `GROUP BY` but an aggregate

`SELECT COUNT(*) FROM customers;` returns **one row**, not five. Without a `GROUP BY`, the whole
table is one group.

**Guard:** predict the answer shape before counting.

### Trap 10 — `HAVING` vs `WHERE` swapped in your head

`WHERE` filters the **orders**, `HAVING` filters the **customers**. Swapping them changes which
customers survive. Read which table each condition touches.

## Worked example

**Q. What does
`SELECT c.cust_name, COUNT(*) AS n FROM customers c JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_name HAVING COUNT(*) > 1;`
return?**

- A. 2 rows
- B. 4 rows
- C. 6 rows
- D. 7 rows

**The traps, mapped to stages**

| Option | Stage | Meaning | Verdict |
|---|---|---|---|
| A | Stage 4 | After `HAVING COUNT(*) > 1` → Ananya, Karthik | ✅ **Correct** |
| B | Stage 3 | After `GROUP BY` → Ananya, Rahul, Meera, Karthik | Trap: forgot `HAVING` |
| C | Stage 1–2 | The inner-join row count | Trap: forgot `GROUP BY` |
| D | Stage 1 with a `LEFT JOIN` | The left-join row count | Trap: used the wrong join |

**Answer: A (2 rows).**

**Second example — the NULL trap.**

**Q. What does
`SELECT c.cust_name FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id WHERE o.amount IS NOT NULL;`
return?**

| Option | Answer |
|---|---|
| A | 5 rows (Ananya×2, Rahul, Meera, Karthik×2) |
| B | 6 rows |
| C | 7 rows |

**Answer: B (6 rows).** The `LEFT JOIN` produced 7 rows; the `WHERE o.amount IS NOT NULL` removed
exactly the one NULL-padded row (Vikram). If you answered 7, you forgot the `WHERE`; if you
answered 5, you also forgot that Ananya and Karthik each appear twice.

## Quick rules

- Every option in an output question corresponds to a **stage**. Name the stage, then pick.
- After a join, list the rows before counting them.
- Treat a NULL row as dead unless the test is `IS NULL`.
- `COUNT(*)` ≠ `COUNT(col)` after a `LEFT JOIN`.
- `GROUP BY` collapses; count groups from stage 3 onwards.
- `DISTINCT` applies to the whole output row.
- `LIMIT` needs `ORDER BY`, and ties are non-deterministic.
- No `GROUP BY` + an aggregate = one output row.

## Common traps

| Trap | Wrong option | Right answer |
|---|---|---|
| Stopped after stage 1 | 6 or 7 when the answer is smaller | Trace to stage 4/5 |
| Counted entities | 5 | 6 or 7 |
| `WHERE` killed the NULL row | 7 | 5 |
| Treated NULL as kept | 6 | 5 |
| `COUNT(*)` vs `COUNT(col)` | 7 | 6 |
| Forgot `GROUP BY` collapses | 6 | 4 |
| `DISTINCT` on one column | 4 | 3 |
| `LIMIT` without sorting | wrong pair | sorted pair |
| No `GROUP BY` + aggregate | many rows | 1 row |

## Checklist

- [ ] I identified which stage each option corresponds to.
- [ ] I listed the join rows before counting.
- [ ] I marked the NULL rows and killed them in the `WHERE`.
- [ ] I checked the exact `COUNT` expression.
- [ ] I counted groups from stage 3 onwards.
- [ ] I verified `DISTINCT` applies to the whole row.
- [ ] I checked for ties at a `LIMIT` cut line.

## Related

- [The five-step execution model](../01-concepts/01-five-step-execution-model.md)
- [Trace procedures](../02-techniques/01-trace-procedures.md)
- [Solved output identification set](../03-worked-examples/01-solved-output-identification-set.md)
- [Output identification reference](../05-reference/01-output-identification-reference.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
