# Chapter: Query Optimization

## What you'll learn
- **Optimizer heuristics and transformations**: how the optimizer searches plan space — dynamic programming, greedy/branch-and-bound, heuristics (join order, predicate pushdown, subquery unnesting) — and the transformation rules that reshuffle queries without changing results.
- **EXPLAIN plans in Postgres and MySQL**: how to read a plan end-to-end, verify a plan with `EXPLAIN ANALYZE`, spot the failure modes (Seq Scan vs Index, bad join order, spilled sorts), and fix them.
- **Database performance tuning and monitoring**: indexing strategy, statistics/autovacuum, `work_mem`/buffer tuning, slow-query detection (`auto_explain`, `pg_stat_statements`), and the operational loop that keeps queries fast.

## Prerequisites (linked)
- [Chapter 01 README](chapter-01-query-processing/README.md) — pipeline, join algorithms, cost estimation.
- [Part 04](../part-04-indexing-and-file-organization/README.md) — indexes, B-trees, covering indexes.

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Query Optimizer: Heuristics and Transformations](section-01-query-optimizer-heuristics-and-transformational.md) | How does the optimizer actually search for the best plan? |
| 02 | [EXPLAIN Plans in Postgres and MySQL](section-02-explain-plans-in-postgres-and-mysql.md) | How do you read — and verify — the plan an engine chose? |
| 03 | [Database Performance Tuning and Monitoring](section-03-database-performance-tuning-and-monitoring.md) | What knobs and dashboards keep production queries fast? |

## One-paragraph narrative connecting all sections
Chapter 01 explained *how* queries run and *how costs are guessed*. Chapter 02 is the optimizer's black box and its operations. Section 01 opens the box: the optimizer explores a huge space of equivalent plans — join orders, access paths, algorithms — using dynamic programming for small queries, heuristics (and `from_collapse_limit`/`join_collapse_limit`) to bound the search beyond that, and algebraic transformation rules (join reordering, predicate pushdown, subquery unnesting, `DISTINCT`/`GROUP BY` pushdown) that preserve semantics while reshaping the tree. Section 02 makes the outcome legible: a complete reading guide for `EXPLAIN` and `EXPLAIN ANALYZE` in Postgres and MySQL — operators, cost/rows, loops, buffers, and the three classic plan pathologies (a Seq Scan the optimizer shouldn't have chosen, a bad join order, a spill). Section 03 closes the loop operationally: how to keep the optimizer happy in production — indexing strategy, keeping statistics fresh, tuning `work_mem`/buffer pools and cost parameters, and the monitoring stack (`auto_explain`, `pg_stat_statements`, slow-query logs, `VACUUM`/bloat) that turns "my query is slow" into "here's the plan, here's the fix, here's the verification."

## Common interview trap in this chapter
**Trap:** Believing the optimizer's plan is "what runs" forever — it's an *estimate-driven choice* that changes with statistics, parameters, and settings; `EXPLAIN` without `ANALYZE` is a guess, not a measurement. Also: using `SET enable_* = off` as a "fix" — those are debugging switches, not tuning; the right fix is better statistics/indexes. And treating `work_mem` as a global setting — it's *per-operation* (per sort/hash/aggregate), so raising it globally can explode memory under many concurrent operations.

## Checklist before moving on
- [ ] I can name the plan-search techniques and the heuristics that bound them.
- [ ] I can list the major transformation rules and give an example of each.
- [ ] I can read a Postgres `EXPLAIN ANALYZE` and a MySQL `EXPLAIN` top to bottom.
- [ ] I can diagnose the three classic plan pathologies and prescribe fixes.
- [ ] I can design the monitoring/tuning loop (stats, indexes, work_mem, slow-query detection).
