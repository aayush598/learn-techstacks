# Function Selection Procedures — Answering Function Questions in 60 Seconds

> Section 3 · DBMS & SQL · Functions, Aggregates & CASE · _Estimated reading time: 7 min_
> **Prerequisite:** [Functions, aggregates and CASE](../01-concepts/01-functions-aggregates-and-case.md)

## In one sentence

**Read the question's verb — count, total, average, split, pad, rank, replace — and the answer is the
function name.**

## Why the pre-test tests this

- Function questions are pure recall, and the answer is always a name you either recognise or do
  not.
- The trick is that distractors are **real functions used in the wrong place**, e.g. `TRIM` offered
  where `LTRIM` is needed, or `RANK` where `ROW_NUMBER` is needed.

## Core concept

### Procedure 1 — the verb → function map

| The question asks for | Answer |
|---|---|
| "How many rows / how many non-NULL values?" | `COUNT(*)` / `COUNT(col)` |
| "How many **different** values?" | `COUNT(DISTINCT col)` |
| "The total / sum" | `SUM(col)` |
| "The average" | `AVG(col)` |
| "The highest / lowest" | `MAX(col)` / `MIN(col)` |
| "Remove leading spaces" | `LTRIM(s)` |
| "Remove trailing spaces" | `RTRIM(s)` |
| "Remove spaces from **both** ends" | `TRIM(s)` |
| "Convert to upper / lower case" | `UPPER(s)` / `LOWER(s)` |
| "A number of characters" | `LENGTH(s)` / `CHAR_LENGTH(s)` |
| "Part of a string" | `SUBSTRING(s, start, len)` / `SUBSTR` / `LEFT` / `RIGHT` |
| "Join two strings" | `CONCAT(a, b)` |
| "Join with a separator" | `CONCAT_WS(sep, a, b)` |
| "Replace text inside a string" | `REPLACE(s, from, to)` |
| "Pad with characters to a fixed length" | `LPAD(s, n, pad)` / `RPAD(s, n, pad)` |
| "Position of a substring" | `LOCATE(sub, s)` / `POSITION` / `INSTR` |
| "The first value that is not NULL" | `COALESCE(a, b, ...)` |
| "Return NULL if two values are equal" | `NULLIF(a, b)` |
| "A label based on a condition" | `CASE ... WHEN ... THEN ... END` |
| "Round to n decimals" | `ROUND(x, n)` |
| "Cut off at n decimals" | `TRUNC(x, n)` |
| "Round up / down" | `CEIL(x)` / `FLOOR(x)` |
| "The remainder of a division" | `MOD(a, b)` |
| "A rank with ties" | `RANK()` / `DENSE_RANK()` |
| "A number with no ties" | `ROW_NUMBER()` |
| "The previous row's value" | `LAG(col, n)` |
| "The next row's value" | `LEAD(col, n)` |

### Procedure 2 — the aggregate-selection table

| Question | Answer | Why |
|---|---|---|
| "Number of rows in the table" | `COUNT(*)` | Counts rows regardless of NULLs |
| "Number of rows where `col` has a value" | `COUNT(col)` | Skips NULLs |
| "Number of different values of `col`" | `COUNT(DISTINCT col)` | Distinct, non-NULL |
| "Total of `col`" | `SUM(col)` | Skips NULLs |
| "Mean of `col`" | `AVG(col)` | Divides by the **non-NULL** count |
| "Highest / lowest `col`" | `MAX` / `MIN` | Skips NULLs |

**Ask yourself two questions:** (1) Do I want **rows** or **values**? (2) Do I want **unique** values?

### Procedure 3 — the `WHERE` / `HAVING` decision

```
Is the condition about an AGGREGATE (COUNT, SUM, AVG, MIN, MAX)?
├─ YES → HAVING
└─ NO  → is it about a single row/column value?
          ├─ YES → WHERE
          └─ NO  → need a CASE expression in the SELECT list
```

**Never put an aggregate in `WHERE`.** The rows are not grouped yet when `WHERE` runs.

### Procedure 4 — evaluate a `CASE` expression

1. Read the `WHEN` conditions **top to bottom**.
2. Take the **first** one that is true.
3. Return that `THEN` value and **stop** — later conditions are not evaluated.
4. If **none** is true, return the `ELSE` value. If there is no `ELSE`, return `NULL`.

**The three exam traps**

| Trap | Fix |
|---|---|
| Reading the conditions out of order | Always top to bottom |
| Assuming `ELSE` is required | Without it the result is `NULL` |
| Assuming `CASE` is exhaustive | It is not — always handle the fall-through |

### Procedure 5 — evaluate a window function

1. **Is it a window function?** Look for `OVER (...)`.
2. **Does it have `PARTITION BY`?** If yes, the calculation restarts for each partition.
3. **Does it have `ORDER BY`?** If yes, the ordering inside the window is fixed — and for
   `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `LEAD` it is **required**.
4. **Does it have a frame?** If yes, the aggregate only sees the rows in the frame.
5. **How many rows come out?** The same number as went in. Window functions **never collapse**.

### Procedure 6 — the three ranking functions

| Situation | Use |
|---|---|
| You need a unique identifier per row | `ROW_NUMBER()` |
| You need a competition ranking, gaps allowed | `RANK()` |
| You need a dense ranking, no gaps | `DENSE_RANK()` |

**Worked difference on the values 100, 90, 90, 80:**

| Function | Output | Rule |
|---|---|---|
| `ROW_NUMBER()` | 1, 2, 3, 4 | Never ties |
| `RANK()` | 1, 2, 2, 4 | Ties share a rank; **skip** the next number |
| `DENSE_RANK()` | 1, 2, 2, 3 | Ties share a rank; **no skip** |

**The tell in the question:** "the second row should still be rank 3" → `DENSE_RANK`. "There should
be no ties" → `ROW_NUMBER`. "Top 2 *rows*" → `ROW_NUMBER` or `LIMIT`.

### Procedure 7 — `COALESCE` vs `CASE` vs `IFNULL` vs `NULLIF`

| Situation | Use |
|---|---|
| Replace NULL with a fallback value | `COALESCE(col, 0)` — or `IFNULL` in MySQL |
| Choose a label based on a condition | `CASE` |
| Return NULL when a value equals another (to avoid divide-by-zero) | `NULLIF(a, b)` |
| Choose between two values based on a boolean | `IIF(cond, a, b)` in SQL Server |

**The one-liner:** `COALESCE(a, b)` ≡ `CASE WHEN a IS NOT NULL THEN a ELSE b END`.

### Procedure 8 — string aggregation

| DBMS | Function |
|---|---|
| MySQL | `GROUP_CONCAT(col SEPARATOR ', ')` |
| PostgreSQL | `STRING_AGG(col, ', ')` |
| Oracle | `LISTAGG(col, ', ') WITHIN GROUP (ORDER BY col)` |
| SQL Server | `STRING_AGG(col, ', ') WITHIN GROUP (ORDER BY col)` |

The question usually asks which function **in MySQL** — answer `GROUP_CONCAT`.

### Procedure 9 — the 60-second split

| Seconds | Activity |
|---|---|
| 0–15 | Read the **verb** in the question |
| 15–30 | Find the matching row in the table |
| 30–45 | Check the distractors — are they real functions used in the wrong place? |
| 45–60 | Mark and move |

## Worked example

**Q. Which function returns a string with trailing spaces removed?**

- A. `TRIM`
- B. `LTRIM`
- C. `RTRIM`
- D. `SUBSTR`

**Solution**

The question says **trailing** spaces. `RTRIM` removes trailing spaces specifically. `TRIM` removes
spaces from **both** ends, and `LTRIM` removes **leading** spaces only.

**Answer: C (`RTRIM`).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | `TRIM` removes leading **and** trailing spaces. It works, but it is not the function that targets trailing spaces. The exam wants the precise one |
| B | `LTRIM` removes **leading** spaces — the opposite end |
| D | `SUBSTR` extracts a substring; it does not remove whitespace |

---

**Q2. Which clause should contain the condition `COUNT(*) > 2`?**

- A. `WHERE`
- B. `GROUP BY`
- C. `HAVING`
- D. `ORDER BY`

**Solution**

`COUNT(*)` is an aggregate, and aggregates are only available **after** grouping. `WHERE` runs
before grouping and cannot reference an aggregate. `HAVING` runs after grouping and can.

**Answer: C (`HAVING`).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | `WHERE` is evaluated **before** grouping. Referring to `COUNT(*)` there is an error |
| B | `GROUP BY` defines the groups. It does not filter them |
| D | `ORDER BY` sorts the result. It does not filter |

---

**Q3. Which window function assigns consecutive numbers with no gaps and never ties?**

- A. `RANK()`
- B. `DENSE_RANK()`
- C. `ROW_NUMBER()`
- D. `NTILE(4)`

**Solution**

`ROW_NUMBER()` numbers rows consecutively and never produces a tie — even when the ordering
columns are equal.

**Answer: C (`ROW_NUMBER()`).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | `RANK()` gives tied rows the same rank and **skips** the next number |
| B | `DENSE_RANK()` gives tied rows the same rank but does not skip. Ties are still possible |
| D | `NTILE(4)` distributes rows into 4 buckets. It is not a numbering function |

## Quick rules

- Verb → function: count, trim, pad, replace, round, rank, lag.
- `COUNT(*)` rows, `COUNT(col)` non-NULL, `COUNT(DISTINCT col)` distinct.
- No `GROUP BY` + aggregate = one row.
- Aggregates go in `HAVING`.
- `CASE` = first match wins; no `ELSE` → `NULL`.
- `ROW_NUMBER` no ties, `RANK` skips, `DENSE_RANK` does not.
- `COALESCE` = first non-NULL; `NULLIF` = NULL when equal.
- `CONCAT` propagates NULL; `CONCAT_WS` skips it.
- `ROUND` rounds, `TRUNC` truncates.
- Window functions never collapse rows; MySQL 8.0+.

## Common traps

| Trap | Why the option is wrong |
|---|---|
| `TRIM` offered for "trailing spaces" | Too broad — `RTRIM` is precise |
| `LTRIM` for trailing spaces | Wrong end |
| Aggregate in `WHERE` | `WHERE` runs before grouping |
| `CASE` branches read out of order | Top to bottom, first match |
| `RANK` and `DENSE_RANK` swapped | `RANK` skips |
| `CONCAT` with a NULL arg | Result is `NULL` |
| `AVG` over `COUNT(*)` | Wrong denominator |
| `GROUP_CONCAT` for PostgreSQL | PostgreSQL uses `STRING_AGG` |

## Checklist

- [ ] I can map a verb to a function name in 15 seconds.
- [ ] I know the three `COUNT` variants.
- [ ] I know `WHERE` vs `HAVING`.
- [ ] I can evaluate a `CASE` in order.
- [ ] I can tell `ROW_NUMBER`, `RANK` and `DENSE_RANK` apart.
- [ ] I know `COALESCE` vs `NULLIF` vs `IFNULL`.
- [ ] I know the MySQL string-aggregation function.

## Related

- [Functions, aggregates and CASE](../01-concepts/01-functions-aggregates-and-case.md)
- [Solved functions and aggregates set](../03-worked-examples/01-solved-functions-aggregates-set.md)
- [Functions and aggregates traps](../04-pitfalls/01-functions-aggregates-traps.md)
- [Functions and aggregates quick check](../05-reference/01-functions-aggregates-quick-check.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
