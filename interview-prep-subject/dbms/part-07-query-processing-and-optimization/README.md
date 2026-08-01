# Part: Query Processing and Optimization

> **TL;DR**: Query processing turns SQL into an efficient execution plan — parsing, rewriting, planning (with cost-based optimization), executing joins/aggregations, and tuning with `EXPLAIN` — the part that answers "why is this query slow?"

## What this part covers
Part 07 is about **performance**: how a SQL statement goes from text to a plan, how the optimizer chooses among billions of possible plans, how joins are actually executed (nested loop, merge, hash), how costs are estimated, and how you read an `EXPLAIN ANALYZE` to fix a slow query. It's the most "practical" part of DBMS: interviewers ask "how would you speed up this query?", "explain this plan", and system-design questions revolve around indexes, joins, and avoiding full scans. You'll learn the pipeline (parse → rewrite → plan → execute), the cost model (I/O-bound, selectivity, cardinality), join algorithms with their cost formulas, optimizer heuristics and transformation rules, and the operational side (EXPLAIN in Postgres and MySQL, performance monitoring, `VACUUM`/statistics, query tuning).

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| **Chapter 01: Query Processing** | query processing pipeline & steps; join algorithms; query cost estimation | Describe the full pipeline; pick the right join algorithm from stats; compute costs of nested-loop/merge/hash joins by hand |
| **Chapter 02: Query Optimization** | optimizer heuristics & transformation; EXPLAIN plans in Postgres & MySQL; performance tuning & monitoring | Explain why the optimizer chose a plan; read/verify an `EXPLAIN ANALYZE`; diagnose and fix slow queries; monitor DB performance |

## Study order
1. **Chapter 01** — understand how queries execute and cost (joins, scans, aggregation).
2. **Chapter 02** — how the optimizer decides, how to read the plan it chose, and how to make queries fast.

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ★★★★★ (5/5)** — tied with transactions as the most-asked DBMS interview area. "How would you optimize this query?", "what's the difference between Nested Loop and Hash Join?", "read this EXPLAIN plan" appear in nearly every DB round.
- **Emphasized by**: all data/platform roles — Meta (MySQL at scale), Amazon (Aurora/Redshift), Google (Spanner/BigQuery), Databricks (SQL engine), Snowflake, and every backend/infra position at any company running a database.
- Typical asked: "explain join algorithms", "cost of a B-tree index lookup", "why is this query slow?", "hash join vs merge join", "cardinality/selectivity", "how does EXPLAIN work".

## How the parts connect (roadmap)
- **Part 04 (Indexing/File Organization)** is the foundation: join/scan costs are literally index-vs-scan decisions; B-trees are why `SELECT ... WHERE id=5` is fast.
- **Part 05 (Transactions)** provides the concurrency context in which queries run (isolation affects locking reads); **Part 06 (Recovery)** explains why checkpointing/vacuum I/O can show up as query slowness.
- **Part 08 (NoSQL)** contrasts: query *processing* in NoSQL is pre-optimized access patterns (partition keys, secondary indexes) instead of cost-based optimization — the "why SQL has an optimizer" contrast.
- Together with Part 04-06, this part completes the "how databases actually work" story interviewers expect you to tell end-to-end.
