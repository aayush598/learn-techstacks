# Chapter: Query Processing

## What you'll learn
- The **query processing pipeline**: parsing → rewriting → planning → execution, and where each step can go wrong (syntax, permissions, plan choice, runtime).
- **Join algorithms**: Nested Loop (with index), Merge Join, and Hash Join — when each is right, their cost formulas, and how to pick by eye from an EXPLAIN plan.
- **Query cost estimation**: cardinality and selectivity, statistics (histograms, `pg_stats`), and why bad estimates are the #1 cause of slow queries.

## Prerequisites (linked)
- [Part 07 README](../README.md) — the roadmap.
- [Part 04](../part-04-indexing-and-file-organization/README.md) — B-trees, index seek vs scan, pages/disk I/O (join costs are I/O costs).

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Query Processing Pipeline and Steps](section-01-query-processing-pipeline-and-steps.md) | What happens between "SELECT" and "rows returned"? |
| 02 | [Join Algorithms: Nested Loop, Merge, Hash](section-02-join-algorithms-nested-loop-merge-hash.md) | How are joins physically executed, and at what cost? |
| 03 | [Query Cost Estimation](section-03-query-cost-estimation.md) | How does the optimizer guess which plan is cheapest — and when is it wrong? |

## One-paragraph narrative connecting all sections
A SQL statement doesn't magically touch tables — it passes through a pipeline. Section 01 walks the stages: the parser builds an abstract syntax tree, the rewriter applies views/rules, the planner (optimizer) generates candidate *plans* and estimates costs, and the executor runs the chosen plan node-by-node, streaming rows. The heart of that pipeline is how data is physically combined: Section 02 covers the three join strategies — **nested loop** (O(n·m), ideal when one side is tiny and indexed), **merge join** (O(n+m) on sorted inputs), and **hash join** (O(n+m) with a build side and probe side, ideal for big unindexed sets) — with their cost formulas and real-world selection rules. But plans are only as good as their *guesses*: Section 03 explains the cost model — selectivity, cardinality, statistics, histograms — and the failure mode that breaks every optimizer (stale or missing statistics, correlated columns), because "why is my query slow?" almost always traces back to a bad estimate, not a bad algorithm.

## Common interview trap in this chapter
**Trap:** Thinking the optimizer "runs the query" to decide — it doesn't; it *estimates* from statistics and chooses the cheapest *estimated* plan, so estimates can be wrong (and often are). Also: assuming nested loop is always the worst join — with an index and a tiny outer relation, it beats hash join. And confusing **logical** operations (SELECT, JOIN — what you wrote) with **physical** operators (Nested Loop, Hash Join, Seq Scan — how it runs): the optimizer can implement one logical join as several physical join variants and picks the cheapest.

## Checklist before moving on
- [ ] I can name the pipeline stages and what each produces.
- [ ] I can derive the cost formulas for nested-loop, merge, and hash joins.
- [ ] I can pick the likely join strategy from table sizes and index availability.
- [ ] I can explain selectivity, cardinality, and histograms, and why bad estimates cause slow queries.
- [ ] I can read a minimal EXPLAIN plan and spot a Seq Scan vs Index Scan.
