# Chapter: SQL

## What you'll learn
- **SELECT, in depth**: the logical execution order (FROM→WHERE→GROUP BY→HAVING→SELECT→DISTINCT→ORDER BY→LIMIT), how NULL and three-valued logic behave, and column aliasing.
- **DDL/DML/DCL/TCL in SQL**: `CREATE/ALTER/DROP`, `INSERT/UPDATE/DELETE/MERGE`, `GRANT/REVOKE`, and constraints declared in SQL.
- **Joins, in depth**: INNER vs OUTER vs CROSS vs SELF, natural vs USING vs ON, and where joins silently mislead (NULLs, duplicates).
- **Aggregation & GROUP BY**: aggregate functions, `GROUP BY` semantics, `HAVING` vs `WHERE`, and the "group by everything not aggregated" rule.
- **Subqueries & CTEs**: correlated vs uncorrelated, `IN/EXISTS/ANY/ALL`, recursive CTEs, and when to prefer a JOIN.
- **Window functions**: `ROW_NUMBER/RANK/DENSE_RANK`, `LAG/LEAD`, running totals, partitioning/ordering/windowing frames, and where window functions are *illegal*.

## Prerequisites (linked)
- [Part 01 (DBMS Fundamentals)](../../part-01-dbms-fundamentals/README.md) — the relational model vocabulary (keys, constraints) from Part 02's own [Chapter 01](../chapter-01-relational-model/README.md).
- Feeds into [Chapter 03 (Advanced SQL & Practice)](../chapter-03-advanced-sql-and-practice/README.md) for tuning + solved problems, and into all later parts (normalization assumes SQL fluency).

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — SQL Overview and SELECT in Depth](section-01-sql-overview-and-select-in-depth.md) | Logical execution order; NULL/3VL; DISTINCT; aliases; the anatomy of a SELECT |
| [Section 02 — DDL, DML, DCL, and Constraints in SQL](section-02-ddl-dml-dcl-and-constraints-in-sql.md) | Real DDL/DML/DCL statements; constraints in CREATE/ALTER; MERGE/upsert |
| [Section 03 — Joins in Depth](section-03-joins-in-depth.md) | INNER/OUTER/CROSS/SELF; ON vs USING vs NATURAL; NULL & duplicate traps |
| [Section 04 — Aggregation and GROUP BY](section-04-aggregation-and-group-by.md) | Aggregate functions; GROUP BY rules; HAVING vs WHERE; distinct aggregates |
| [Section 05 — Subqueries and CTEs](section-05-subqueries-and-ctes.md) | Correlated/uncorrelated; IN/EXISTS/ANY/ALL; recursive CTEs; flattening |
| [Section 06 — Window Functions in Depth](section-06-window-functions-in-depth.md) | ROW_NUMBER/RANK/DENSE_RANK; LAG/LEAD; frames; NTILE; where illegal |

## One-paragraph narrative connecting all sections
SQL is one language with a strict mental model: every statement is processed in a fixed **logical order**, and knowing that order (Section 01) makes every other section mechanical. Structure and data mutations come from **DDL/DML/DCL/TCL** (Section 02), while the relational *queries* are dominated by **joins** (Section 03) — combining tables by keys — and **aggregation** (Section 04) — collapsing many rows into summaries, where `GROUP BY` and `HAVING` live. When a single query isn't enough, **subqueries and CTEs** (Section 05) let you build intermediate results and even recurse. And the highest-leverage tool for analytics, **window functions** (Section 06), compute per-group rankings and running totals without collapsing rows. Master this chapter and you can write 90% of all interview SQL; Chapter 03 adds tuning and a pattern library on top.

## Common interview trap in this chapter
Candidates write `WHERE` conditions on aggregated columns ("`WHERE COUNT(*) > 5`") — that's **`HAVING`'s** job, because `WHERE` runs *before* grouping. Second trap: using `WHERE` on a join-filter (filtering the right side of a `LEFT JOIN`), which silently converts the outer join back to an inner join. Third: forgetting that `NULL` breaks equality — `col <> 'x'` drops NULLs, and `NOT IN (subquery)` misbehaves when the subquery contains NULLs. If you catch yourself doing any of these three in an interview, you've hit this chapter's classic traps.

## Checklist before moving on
- [ ] I can recite the full logical execution order of SELECT with a one-line example for each clause.
- [ ] I can explain why `WHERE COUNT(*)` fails and give the `HAVING` fix.
- [ ] I can predict the output of LEFT vs INNER join on a table with NULL keys.
- [ ] I can write "top 2 per group" with a window function and with a subquery, and know when each works.
- [ ] I can convert a correlated subquery to a JOIN and explain when NOT to.
- [ ] I can write a recursive CTE (org chart / tree) from memory.
- [ ] I can state exactly where window functions are illegal (WHERE, GROUP BY, HAVING).
