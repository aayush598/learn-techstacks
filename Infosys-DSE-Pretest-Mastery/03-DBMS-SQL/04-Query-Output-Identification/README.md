# Query Output Identification — Topic Guide

> Section 3 · DBMS & SQL · Query Output Identification · _Estimated reading time: 60 min for the full topic_

## What the pre-test asks in this topic

**"Identify the output of the given SQL query" is 2 of the 10 DBMS questions.** The exam shows
you two small tables and a query, and asks either:

- "How many rows does this query return?" → the option set contains 5, 6, 7 and 30.
- "Which rows appear in the result?" → the option set contains four row sets.
- "What value does this aggregate return?" → the option set contains four numbers.

The archetype is **not** hard. It is slow, and it is slow because candidates try to read the SQL in
their head. Four lines of scratch paper ends it.

## Learning objectives

After this topic you should be able to:

- Walk a `SELECT` through the five stages — `FROM`+`JOIN` → `WHERE` → `GROUP BY` → `HAVING` →
  `SELECT`+`ORDER BY` — in that order, every time.
- Compute the join row count for any join on a small fixture, and know that a one-to-many join
  **fans out** the "one" side.
- Explain why a `WHERE` on the right table of a `LEFT JOIN` removes the NULL-padded rows, and why
  `NULL > 400` drops a row rather than keeping it.
- State the difference between `COUNT(*)`, `COUNT(col)`, `COUNT(DISTINCT col)`, `SUM(col)`,
  `AVG(col)`, `MIN/MAX(col)` on a group containing NULLs.
- Predict the **shape** of the output (1 row, 1 row per group, 1 row per source row, ≤ n rows)
  before you read the options.
- Know that an aggregate with no `GROUP BY` returns exactly **one** row.
- Know that `DISTINCT` applies to the whole output row, not to one column.
- Identify which execution stage each option in the list corresponds to, and use that to pick in 20
  seconds.

## File index

| File | Lines | What it gives you |
|---|---|---|
| [01-concepts/01-five-step-execution-model.md](01-concepts/01-five-step-execution-model.md) | ~250 | The five stages, what to check at each one, the four deciding rules, a full worked trace |
| [02-techniques/01-trace-procedures.md](02-techniques/01-trace-procedures.md) | ~230 | The scratch pad, 6 procedures, the aggregate cheat sheet, NULL hunting, the 90-second time split |
| [03-worked-examples/01-solved-output-identification-set.md](03-worked-examples/01-solved-output-identification-set.md) | ~330 | 9 solved output questions on a stated fixture, each traced stage by stage |
| [04-pitfalls/01-output-identification-traps.md](04-pitfalls/01-output-identification-traps.md) | ~190 | 10 traps, each mapped to the stage where the trace went wrong |
| [05-reference/01-output-identification-reference.md](05-reference/01-output-identification-reference.md) | ~150 | The trace card, fixture numbers, join row counts, aggregate table, NULL table, shape predictor |

## Quick 5-step procedure

1. **Predict the shape.** Aggregate without `GROUP BY` → 1 row. With `GROUP BY` → 1 row per group.
   Plain list → 1 row per source row.
2. **Stage 1: list the join rows.** Write them out. Count them.
3. **Stage 2: kill the `WHERE` failures.** Mark NULL rows first — they die on any comparison except
   `IS NULL`.
4. **Stage 3 and 4: groups, then `HAVING`.** Count groups, not rows, from here on.
5. **Stage 5: apply `DISTINCT`, `ORDER BY`, `LIMIT`.** Check for ties at a `LIMIT` cut line.

## Key takeaways

- ✅ **The five stages always run in the same order.** Write the intermediate set at each one.
- ✅ **After a join, count rows — not entities.** On the fixture: 6 inner, 7 left, 30 cross.
- ✅ **NULL comparisons are `UNKNOWN`, so the row is dropped**, not kept.
- ✅ **`COUNT(*)` counts rows including NULL-padded ones; `COUNT(col)` does not.**
- ✅ **No `GROUP BY` + an aggregate = exactly one output row.**
- ✅ **`DISTINCT` applies to the whole output row.**
- ✅ **Every option in the list corresponds to a stage.** Name the stage, then pick.
- ⚠️ **Meera's warning:** she knows the SQL and loses the mark anyway because she traced it in her
  head. Paper, every time.

## Related

- [DBMS & SQL section index](../README.md)
- [SQL Basics: DDL & DML](../01-SQL-Basics-DDL-DML/README.md) — clause order and NULL semantics
- [Joins](../02-Joins/README.md) — the row counts that stage 1 depends on
- [Functions, Aggregates & CASE](../08-Functions-Aggregates-Case/README.md) — `COUNT`, `SUM`, `AVG` in depth
- [Master README](../../README.md)
