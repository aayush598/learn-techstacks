# SQL Basics: DDL & DML — Topic Guide

> Section 3 · DBMS & SQL · SQL Basics, DDL & DML · _Estimated reading time: 70 min for the full topic_

## What the pre-test asks in this topic

Roughly **1–2 of the 10 DBMS/SQL questions** are straight SQL-foundation questions. They never ask
you to write a long query. They ask you to:

1. **Name a command** — "which statement removes a table?" → `DROP TABLE`, not `DELETE`.
2. **Compare three similar things** — `TRUNCATE` vs `DELETE` vs `DROP`; `WHERE` vs `HAVING`;
   `UNION` vs `UNION ALL`; `IN` vs `BETWEEN` vs `LIKE`.
3. **Judge a piece of SQL** — "is this query valid?", "what does `NULL` do here?".
4. **Fill a blank** — "write the statement to insert a row", "write the statement to update all rows
   where `city = 'Pune'`".

The archetype looks easy and is where most candidates leak marks, because the options are *all*
plausible SQL. You need the differences cold, not the syntax.

## Learning objectives

After this topic you should be able to:

- Separate **DDL, DML, DQL, TCL and DCL** by what each statement does, and give one example of each.
- Explain the four differences between `DELETE`, `TRUNCATE` and `DROP` (rows, structure, rollback,
  identity counter) and pick the right one in a question.
- State how `NULL` behaves in comparisons, arithmetic, `COUNT`, `AVG`, `DISTINCT`, `LIKE` and
  `ORDER BY` — and know that `NULL = NULL` is not `TRUE`.
- Write correct `SELECT` statements with `WHERE`, `DISTINCT`, `ORDER BY`, `LIMIT` and column
  aliases, in the right logical order.
- Distinguish `WHERE` (row filter, before grouping) from `HAVING` (group filter, after grouping),
  and know why `WHERE` cannot reference an aggregate.
- Use `IN`, `BETWEEN`, `LIKE` and `EXISTS` correctly, including the `NOT IN` + `NULL` trap.
- Write scalar, `IN` and `EXISTS` subqueries, and know which one is NULL-safe.
- Choose correctly between `UNION`, `UNION ALL`, `INTERSECT` and `EXCEPT`.
- Know what `ALTER TABLE` can and cannot do, and what `DROP` does to the data definition.

## File index

| File | Lines | What it gives you |
|---|---|---|
| [01-concepts/01-ddl-dml-anatomy.md](01-concepts/01-ddl-dml-anatomy.md) | ~230 | Statement families, `CREATE TABLE`, data types, `INSERT`/`UPDATE`/`DELETE`, `ALTER`/`DROP`/`TRUNCATE`, NULL semantics |
| [01-concepts/02-select-filter-sort-and-subqueries.md](01-concepts/02-select-filter-sort-and-subqueries.md) | ~250 | `SELECT`, `DISTINCT`, `ORDER BY`, `LIMIT`, `WHERE` vs `HAVING`, subqueries, set operations |
| [02-techniques/01-statement-decision-procedures.md](02-techniques/01-statement-decision-procedures.md) | ~190 | 9 numbered procedures: pick the command, place the clause, choose the predicate, choose the set operation |
| [03-worked-examples/01-solved-sql-basics-set.md](03-worked-examples/01-solved-sql-basics-set.md) | ~280 | 8 fully solved questions, each built around one specific error |
| [04-pitfalls/01-sql-basics-traps.md](04-pitfalls/01-sql-basics-traps.md) | ~170 | 9 traps with the wrong answer, the right answer, and the signature option |
| [05-reference/01-sql-basics-cheat-sheet.md](05-reference/01-sql-basics-cheat-sheet.md) | ~160 | One-page syntax sheet: clause order, NULL table, operator chooser |
| [05-reference/02-command-family-table.md](05-reference/02-command-family-table.md) | ~120 | Every command, its family, and what it touches |

## Quick 5-step procedure for any SQL question

1. **Name the job.** Is the stem asking you to *change data*, *change structure*, *read data*, or
   *control a transaction*? That single sentence picks the statement family.
2. **Circle the verbs.** `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `INSERT`, `UPDATE`, `DELETE`, `SELECT`,
   `COMMIT`, `ROLLBACK`, `GRANT`, `REVOKE`. The verb is the answer to "which statement…".
3. **Check the scope.** Does it need `WHERE`? `WHERE` on `UPDATE`/`DELETE` without `WHERE` hits every
   row — that is the classic trap.
4. **Check the NULL edge.** Any comparison, any `COUNT`, any `NOT IN` — ask "what does NULL do here?"
5. **Read the option list backwards.** If one option is the "delete everything" version and the stem
   says "delete rows where…", the `DELETE … WHERE` option is right and the `TRUNCATE` option is the
   trap.

## Key takeaways

- ✅ **Verb first.** The command family is decided by what the statement *does*, not what it touches.
- ✅ **`DELETE` removes rows, `TRUNCATE` empties a table and resets identity, `DROP` removes the
  table itself.** Structure vs data is the cleanest split.
- ✅ **`WHERE` filters rows; `HAVING` filters groups.** `WHERE` runs first, `GROUP BY` next,
  `HAVING` after.
- ✅ **`NULL` is not a value.** `= NULL` is never true; `NULL > 5` is unknown; `COUNT(col)` skips
  NULLs; `ORDER BY` puts NULLs first ascending in MySQL.
- ✅ **`NOT IN` with a NULL in the list returns nothing.** Use `NOT EXISTS` instead.
- ✅ **`UNION` removes duplicates and costs a sort; `UNION ALL` keeps them and is faster.**
- ✅ **`ORDER BY` uses the alias or the ordinal (`ORDER BY 2`); `GROUP BY` uses real column names.**
- ⚠️ **Meera's warning:** she answers "which statement deletes a table" with `DELETE`. Re-read the
  stem: "deletes a table" is `DROP`.

## Related

- [DBMS & SQL section index](../README.md)
- [Joins](../02-Joins/README.md) — the next topic, and the highest-yield one
- [Two-Table Query Writing](../03-Two-Table-Query-Writing/README.md) — where the clauses above get used
- [Functions, Aggregates & CASE](../08-Functions-Aggregates-Case/README.md) — `COUNT`, `AVG` and `CASE`
- [Master README](../../README.md)
