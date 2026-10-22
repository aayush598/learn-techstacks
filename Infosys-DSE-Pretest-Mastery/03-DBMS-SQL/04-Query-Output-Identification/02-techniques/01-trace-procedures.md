# Trace Procedures — Read a Query in 60 Seconds

> Section 3 · DBMS & SQL · Query Output Identification · _Estimated reading time: 7 min_
> **Prerequisite:** [The five-step execution model](../01-concepts/01-five-step-execution-model.md)

## In one sentence

**Four scratch lines on paper — join, filter, group, output** — is all it takes to answer any
output-identification question in the pre-test.

## Why the pre-test tests this

- This archetype is 2 of the 10 questions. At 60 seconds each, it is 2 minutes of the 18.
- The technique is not about SQL knowledge; it is about **discipline on paper**. Meera's problem is
  that she reads the query and guesses. Four lines of scratch paper end the guessing.
- The procedures below fit in the corner of the question paper.

## Core concept

### The scratch pad

Draw this at the bottom of the question paper and fill it in:

```
STAGE 1  FROM+JOIN  →  rows: ____   (list them if ≤ 8)
STAGE 2  WHERE      →  rows: ____
STAGE 3  GROUP BY   →  groups: ____
STAGE 4  HAVING     →  groups: ____
STAGE 5  SELECT     →  output rows: ____
```

### Procedure 1 — the 60-second trace

1. **Read the `FROM` line. Name the join type.** Write `INNER` / `LEFT` / `RIGHT` / `CROSS`.
2. **Count the join rows.** Match each right row to a left row. If a left row has no match and the
   join is `LEFT`, it still produces a row with NULLs. Write the row count.
3. **Read the `WHERE`.** Cross out every row that fails. Remember: a NULL comparison fails.
4. **Read the `GROUP BY`.** Write the groups and the number of rows in each.
5. **Read the `HAVING`.** Cross out whole groups.
6. **Read the `SELECT` and apply the aggregate.** One output row per surviving group.
7. **Apply `DISTINCT`, `ORDER BY`, `LIMIT` last.**

### Procedure 2 — "which row count?" shortcut

You do not always need the full row list. For a question that only asks for a count, this is
faster:

```
Final count = (rows surviving WHERE) grouped by GROUP BY key, then filtered by HAVING
```

| Query shape | Count |
|---|---|
| No `GROUP BY`, no aggregate | Number of rows after `WHERE` |
| No `GROUP BY`, with an aggregate | **1** |
| `GROUP BY`, with an aggregate | Number of **distinct group keys** after `HAVING` |
| `GROUP BY`, no aggregate | Number of distinct group keys (rows are deduped) |
| `GROUP BY`, `DISTINCT` in the select | Number of distinct **output rows**, not groups |

### Procedure 3 — the aggregate cheat sheet

| Expression | What it returns |
|---|---|
| `COUNT(*)` | Number of rows in the group |
| `COUNT(col)` | Number of non-NULL values of `col` in the group |
| `COUNT(DISTINCT col)` | Number of distinct non-NULL values of `col` |
| `SUM(col)` | Sum of non-NULL values; `NULL` if the group has no non-NULL values |
| `AVG(col)` | Mean of the **non-NULL** values |
| `MIN(col)` / `MAX(col)` | Smallest / largest non-NULL value |

**`SUM` and `AVG` over an empty group:** `SUM` → `NULL`; `AVG` → `NULL`; `COUNT` → 0; `MIN`/`MAX`
→ `NULL`.

### Procedure 4 — NULL hunting

Whenever a column can be NULL, walk the rows and mark them:

| Expression | Result for a NULL column value |
|---|---|
| `col = 5` | `UNKNOWN` → row dropped by `WHERE` |
| `col <> 5` | `UNKNOWN` → row dropped |
| `col > 5` | `UNKNOWN` → row dropped |
| `col IS NULL` | `TRUE` → row kept |
| `col IS NOT NULL` | `FALSE` → row dropped |
| `SUM(col)` | NULL is skipped |
| `COUNT(col)` | NULL is skipped |
| `GROUP BY col` | NULLs form one group |
| `ORDER BY col ASC` | NULLs first in MySQL, last in PostgreSQL/Oracle |

### Procedure 5 — the "answer type" check

Before you look at the options, predict the **shape** of the answer:

| The query contains | The answer is |
|---|---|
| `COUNT(*)` alone | A single number |
| `COUNT(col), COUNT(col)` | One row, two numbers |
| `GROUP BY` + aggregate | One row per group |
| Plain column list | One row per surviving source row |
| `DISTINCT` | One row per distinct combination |
| `LIMIT n` | At most n rows |

If the options do not contain the shape you predicted, you have mis-read the query. Go back.

### Procedure 6 — the sanity checks

Run these three before you commit to an answer:

| Check | If it fails |
|---|---|
| Does my row count exceed the source table's row count? | A join fanned out — that is legal, but confirm |
| Is the row count a multiple of something suspicious? | Check for a missing `GROUP BY` (1 row) |
| Do my totals match a hand-computed total? | Recompute the `SUM` by hand from the source rows |

### The 90-second time split

| Time | Activity |
|---|---|
| 0–15 s | Read the whole query once. Name the archetype: count / group / list / top-N |
| 15–40 s | Stage 1: write the join rows |
| 40–55 s | Stage 2: cross out the `WHERE` failures |
| 55–75 s | Stage 3–4: form the groups, apply `HAVING` |
| 75–90 s | Stage 5: write the output, match the option, mark and move |

If you are at 70 seconds and the trace is still unclear, **guess and move**. One guess is 1 point;
two extra minutes is often 2 points lost.

## Worked example

**Q. Given the fixture, what does
`SELECT c.cust_name, COUNT(o.order_id) FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_name;` return?**

- A. 4 rows
- B. 5 rows
- C. 6 rows
- D. 7 rows

**Procedure 5 first — predict the shape:** `GROUP BY` + an aggregate → one row per group. So the
answer is a row count, and the number of groups is the number of distinct customer names among the
surviving rows.

**Trace**

| Stage | Result |
|---|---|
| 1 `FROM` + `LEFT JOIN` | 7 rows: Ananya×2, Rahul, Meera, Karthik×2, Vikram (NULLs) |
| 2 `WHERE` | None → 7 rows |
| 3 `GROUP BY c.cust_name` | 5 groups: Ananya(2), Rahul(1), Meera(1), Karthik(2), Vikram(1) |
| 4 `HAVING` | None → 5 groups |
| 5 `SELECT` | 5 output rows |

**Answer: B (5 rows).**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| A | 4 = the number of customers who **have** orders — the inner-join count. The `LEFT JOIN` keeps Vikram, so there are 5 groups |
| C | 6 = the number of **orders**. `GROUP BY cust_name` collapses the two Ananya orders into one row |
| D | 7 = the number of **join rows** before grouping. The `GROUP BY` collapses 7 rows into 5 groups |

**The value of each row**

| cust_name | COUNT(o.order_id) |
|---|---|
| Ananya | 2 |
| Rahul | 1 |
| Meera | 1 |
| Karthik | 2 |
| Vikram | **0** |

Note that Vikram's count is **0**, not 1 — `COUNT(o.order_id)` skips the NULL. If the query had
said `COUNT(*)`, Vikram would show 1 and the trap would move.

## Quick rules

- Predict the **shape** of the answer before reading the options.
- Write the stage-1 rows; everything else is arithmetic on paper.
- After a join, count rows.
- NULL rows die in a `WHERE` unless the test is `IS NULL`.
- `COUNT(*)` = rows, `COUNT(col)` = non-NULL, `COUNT(DISTINCT col)` = distinct.
- No `GROUP BY` + an aggregate = exactly one output row.
- `GROUP BY` + `DISTINCT` → distinct output rows, which may be fewer than the groups.
- At 70 seconds with an unclear trace: guess and move.

## Common traps

| Trap | Fix |
|---|---|
| Counting entities instead of join rows | Trace stage 1 |
| Forgetting `WHERE` kills the `LEFT JOIN`'s NULL row | Cross out the NULL row explicitly |
| `COUNT(*)` after a `LEFT JOIN` | `COUNT(col)` |
| No `GROUP BY` but expecting many rows | One group, one row |
| `DISTINCT` applied to one column only | It applies to the whole row |
| Forgetting `NULL` in a `WHERE` comparison | Mark the NULL rows first |
| `LIMIT` before `ORDER BY` | Sort, then cut |

## Checklist

- [ ] I predicted the answer shape first.
- [ ] I wrote the stage-1 rows on paper.
- [ ] I marked the NULL rows before applying the `WHERE`.
- [ ] I counted rows after the join, not entities.
- [ ] I checked `COUNT(*)` vs `COUNT(col)`.
- [ ] I applied `HAVING` before computing the final aggregates.
- [ ] I marked and moved if I passed 70 seconds.

## Related

- [The five-step execution model](../01-concepts/01-five-step-execution-model.md)
- [Solved output identification set](../03-worked-examples/01-solved-output-identification-set.md)
- [Output identification traps](../04-pitfalls/01-output-identification-traps.md)
- [Output identification reference](../05-reference/01-output-identification-reference.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
