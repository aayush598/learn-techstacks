# Two-Table Query Writing — Topic Guide

> Section 3 · DBMS & SQL · Two-Table Query Writing · _Estimated reading time: 70 min for the full topic_

## What the pre-test asks in this topic

**"Write a query for two tables" is 1–2 of the 10 DBMS questions** and it comes in two formats:

1. **Free response** — "Write a query to display all customers with their order amounts, including
   customers who have never ordered." You produce the SQL.
2. **Multiple choice on SQL** — four candidate queries, three of them broken in a specific way.

Both are decided by the same three things: **the left table, the join type, and the clause order.**

This is the archetype where DBMS strength pays off directly. It is also the archetype where
candidates lose time, because writing a query from scratch under a 108-second box is slow.
Adapt a pattern instead.

## Learning objectives

After this topic you should be able to:

- Apply the **eight-step recipe** (`FROM` → `JOIN` → `ON` → `WHERE` → `GROUP BY` → `HAVING` →
  `SELECT` → `ORDER BY` → `LIMIT`) to any two-table question, in under 90 seconds.
- Pick the left table using the "which rows would be missing" test.
- Choose `INNER` vs `LEFT` from the stem's escape clause in under 10 seconds.
- Write "count per parent **including zeros**" with `COUNT(child.col)` — and know why `COUNT(*)`
  is wrong there.
- Write "find the ones with **none**" with the anti-join or `NOT EXISTS`, and know why `NOT IN`
  fails.
- Put row filters in `WHERE` and aggregate filters in `HAVING`, every time.
- Write top-N-per-group and running-total queries with window functions, and state that they need
  **MySQL 8+**.
- Write a many-to-many query through a junction table and a same-city pair query with a self-join.
- Spot all six common query mistakes before reading the option list.

## File index

| File | Lines | What it gives you |
|---|---|---|
| [01-concepts/01-two-table-query-anatomy.md](01-concepts/01-two-table-query-anatomy.md) | ~280 | The 8 clauses typed and executed, join conditions, `WHERE` vs `HAVING`, `SELECT` discipline, zero-inclusive counts, anti-joins, window functions, running totals, pairs |
| [02-techniques/01-the-eight-step-recipe.md](02-techniques/01-the-eight-step-recipe.md) | ~230 | The nine-step recipe with the question each step answers, MySQL vs standard differences, answer-format rules |
| [02-techniques/02-task-recipe-cards.md](02-techniques/02-task-recipe-cards.md) | ~250 | Seven task types, nine ready-made cards, a stem scanner, fixture-verified results for each card |
| [03-worked-examples/01-solved-query-writing-set.md](03-worked-examples/01-solved-query-writing-set.md) | ~300 | 8 fully solved write-the-query questions with the near-miss for each |
| [04-pitfalls/01-query-writing-traps.md](04-pitfalls/01-query-writing-traps.md) | ~190 | Six mistakes in query order + two more, each with the symptom and the fix |
| [05-reference/01-query-writing-pattern-library.md](05-reference/01-query-writing-pattern-library.md) | ~180 | Nine copy-and-adapt patterns, clause quick card, engine differences, style rules |

## Quick 5-step procedure

1. **Task type** — count / none / aggregate / filter-on-aggregate / top-N / pairs. Name it.
2. **Left table** — the table whose rows must survive goes first.
3. **Join type** — "including" → `LEFT`; "that have" → `INNER`.
4. **Clause order** — `WHERE` for rows, `GROUP BY`/`HAVING` only if aggregating, `ORDER BY`+`LIMIT`
   only if asked.
5. **Verify on the fixture** — run it against the shared tables and check the row count and the
   zero case before you move on.

## Key takeaways

- ✅ **Write `FROM` + `JOIN … ON` first.** Everything else is optional; that line is not.
- ✅ **"including those with none" → `LEFT JOIN`.** "who have" → `INNER JOIN`.
- ✅ **`WHERE` filters rows, `HAVING` filters groups.** An aggregate in a `WHERE` is an error.
- ✅ **`COUNT(child.col)` for zero-inclusive counts; `COALESCE(SUM(x), 0)` for zero-inclusive sums.**
- ✅ **`GROUP BY` every non-aggregated selected column** — and skip it entirely when you are not
  aggregating.
- ✅ **`ORDER BY` before `LIMIT`; add a tiebreaker** when the sort key can tie.
- ✅ **Window functions need MySQL 8+**, and cannot be filtered in the same `WHERE`.
- ⚠️ **Meera's warning:** she can write the SQL but re-derives the clause order every time. Use
  the recipe. Ananya's warning: she adds `GROUP BY` to everything — that changes the answer.

## Related

- [DBMS & SQL section index](../README.md)
- [Joins](../02-Joins/README.md) — pick the join type from here
- [Query Output Identification](../04-Query-Output-Identification/README.md) — the reverse skill: read a query you did not write
- [Functions, Aggregates & CASE](../08-Functions-Aggregates-Case/README.md) — `COUNT`, `SUM`, `COALESCE` in depth
- [Master README](../../README.md)
