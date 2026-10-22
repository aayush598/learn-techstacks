# Functions, Aggregates & CASE — Topic Guide

> Section 3 · DBMS & SQL · Functions, Aggregates & CASE · _Estimated reading time: 35 min for the full topic_

## What the pre-test asks in this topic

**Function questions are the most common archetype in DBMS sections** — a short question, four
function names, one correct answer. Typical forms:

- "Which function removes trailing spaces?" → `RTRIM`
- "What does `COUNT(DISTINCT cust_id)` return on this table?" → a number
- "What is the value of this `CASE` expression?" → a label or `NULL`
- "Which clause filters groups?" → `HAVING`
- "Which window function gives 1, 2, 2, 3?" → `DENSE_RANK`

There is no computation to get wrong. You either know the name or you do not.

## Learning objectives

After this topic you should be able to:

- Sort any SQL function into **scalar**, **aggregate**, **window** or **conditional**, and state what
  each does to the row count.
- Distinguish `COUNT(*)`, `COUNT(col)` and `COUNT(DISTINCT col)` and give the correct value on the
  shared fixture.
- Recall the **string, numeric and date** function sets at the level of "which one does this".
- Explain why an aggregate with **no `GROUP BY`** returns exactly one row.
- Say when `WHERE` and when `HAVING` applies, and why an aggregate can only go in `HAVING`.
- Evaluate a `CASE` expression **top to bottom**, knowing that the first match wins and that no
  `ELSE` means `NULL`.
- Use `COALESCE`, `NULLIF` and `IFNULL` correctly, and use `IS NULL` rather than `= NULL`.
- Tell `ROW_NUMBER`, `RANK` and `DENSE_RANK` apart, and state that window functions **never
  collapse** rows.
- Know that window functions require **MySQL 8.0+**.

## File index

| File | Lines | What it gives you |
|---|---|---|
| [01-concepts/01-functions-aggregates-and-case.md](01-concepts/01-functions-aggregates-and-case.md) | ~400 | Every function family with a full reference table, `CASE` rules, `WHERE`/`GROUP BY`/`HAVING`, `DISTINCT` vs `GROUP BY`, CTEs |
| [02-techniques/01-function-selection-procedures.md](02-techniques/01-function-selection-procedures.md) | ~300 | The verb → function map, aggregate selection, `HAVING` decision, `CASE` evaluation, window evaluation, ranking trio, NULL-handling, string aggregation per DBMS |
| [03-worked-examples/01-solved-functions-aggregates-set.md](03-worked-examples/01-solved-functions-aggregates-set.md) | ~340 | 9 solved questions with the fixture stated and distractors explained |
| [04-pitfalls/01-functions-aggregates-traps.md](04-pitfalls/01-functions-aggregates-traps.md) | ~200 | 9 traps + 4 bonus, each with the tell in the option |
| [05-reference/01-functions-aggregates-quick-check.md](05-reference/01-functions-aggregates-quick-check.md) | ~200 | Verb → function map, aggregates, window syntax, `CASE` rules, fixture numbers |

## Quick procedure

1. **Read the verb** in the question — count, total, average, strip, pad, replace, rank.
2. **Ask: rows, values, or distinct values?** Then pick `COUNT(*)`, `COUNT(col)` or
   `COUNT(DISTINCT col)`.
3. **Is the condition on an aggregate?** If yes → `HAVING`.
4. **Evaluating a `CASE`?** Top to bottom, first match wins, no `ELSE` → `NULL`.
5. **Evaluating a window function?** Check `PARTITION BY`, then `ORDER BY`, then the frame. Count the
   output rows — they equal the input rows.

## Key takeaways

- ✅ **Scalar** transforms, **aggregate** collapses, **window** computes without collapsing.
- ✅ **`COUNT(*)` = rows. `COUNT(col)` = non-NULL. `COUNT(DISTINCT col)` = distinct non-NULL.**
- ✅ **Aggregate + no `GROUP BY` = exactly one row.**
- ✅ **`WHERE` filters rows, `HAVING` filters groups.** Aggregates live in `HAVING`.
- ✅ **`CASE` takes the first matching `WHEN`. No `ELSE` → `NULL`.**
- ✅ **`IS NULL`, never `= NULL`.**
- ✅ **`ROW_NUMBER` never ties. `RANK` skips. `DENSE_RANK` does not.**
- ✅ **`CONCAT` propagates NULL; `CONCAT_WS` skips it; `GROUP_CONCAT` aggregates.**
- ✅ **`ROUND` rounds, `TRUNC` truncates, `CEIL` up, `FLOOR` down.**
- ✅ **Window functions need MySQL 8.0+.**
- ⚠️ **Ananya's note:** she recognises the function names but counts wrong under time pressure. Write
  the fixture numbers down: 6 orders, 4800 total, **4** distinct ordering customers, 5 customers.

## Related

- [DBMS & SQL section index](../README.md)
- [SQL Basics: DDL & DML](../01-SQL-Basics-DDL-DML/README.md) — `SELECT`, `WHERE`, `GROUP BY` clauses
- [Query Output Identification](../04-Query-Output-Identification/README.md) — where `COUNT` vs `COUNT(*)` decides the answer
- [DBMS Theory, Keys, Indexes & Views](../07-DBMS-Theory-Keys-Indexes-Views/README.md) — procedures, functions and triggers
- [Master README](../../README.md)
