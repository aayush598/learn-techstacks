# EXPLAIN Plans in Postgres and MySQL

> **TL;DR**: `EXPLAIN` shows the optimizer's plan (operators, estimated rows/cost) without running it; `EXPLAIN ANALYZE` runs it and reports actuals — the whole skill is comparing the two to spot when estimates are wrong, when access paths are bad, and which node dominates the runtime.

## 1. Why Does This Exist?
`EXPLAIN` exists because the optimizer's *choice* is invisible otherwise: after Section 01, we know the optimizer applies transformations and cost-based search — but users need a window into *which* plan it chose and *why* it might be slow. It answers the three questions that matter: (a) What operators run, in what order? (b) How many rows does the optimizer *think* each step produces (estimates)? (c) How many rows/cost did it *actually* produce (with ANALYZE)? The whole art is the gap between (b) and (c) — that gap is where slow queries hide. Without EXPLAIN, production debugging would be guesswork: blind `CREATE INDEX` scatter-shooting.

## 2. How Does It Work?
- `EXPLAIN <stmt>`: builds the plan via the optimizer, prints the operator tree (indented = nesting; each node shows operator, estimated rows, estimated width, estimated cost range), and *does not execute*.
- `EXPLAIN ANALYZE <stmt>`: executes the query, and each node reports actual rows, actual time (ms), and (Postgres) actual loops; top node's "Execution Time" is the total; "Planning Time" is separate.
- `EXPLAIN (ANALYZE, BUFFERS)` (Postgres): adds buffer usage (shared read/hit/dirtied/written) — the key to diagnosing I/O. MySQL 8.0: `EXPLAIN ANALYZE` (executes, shows actuals), `EXPLAIN FORMAT=JSON` (structured detail), and `SHOW PROFILE`/optimizer trace for internals.
- The tree is read **inside-out / bottom-up**: leaf nodes (scans) feed parents (joins), and each node's cost/rows include its children. The dominant cost node = the bottleneck.

## 3. When Is It Used?
- Any time a query is slow in dev or production (before adding indexes!).
- After an optimizer change (stats refresh, `VACUUM ANALYZE`, version upgrade) to confirm plans are still good.
- In post-mortems: capture `EXPLAIN (ANALYZE, BUFFERS, TIMING)` of the offending query.
- Schema migrations: verify new indexes are actually used (or better: verify via plan).
- Interviews: "read this EXPLAIN and find the problem" is a staple — the three pathologies below are the classic answers.

## 4. Why Wasn't Another Approach Chosen?
- *Timing the query (`\timing` / `duration`)*: measures the *outcome* (total runtime) but not *where* time goes — you can't tell a bad join order from a huge sort without a plan. EXPLAIN's per-node breakdown localizes the bottleneck.
- *Statement statistics / logs*: show latency but not the operators; they tell you *that* it's slow, not *why*.
- *Tracing (e.g., `auto_explain.log_analyze`)*: exactly EXPLAIN's data, but automated for every slow query — the production wrapper of EXPLAIN, not a replacement.
- *Profiler/trace (MySQL `optimizer_trace`, Postgres `pg_hint_plan` trace)*: deeper internals, but noisy and hard to parse — EXPLAIN is the stable, human-grade summary everyone agrees on.

## 5. Intuition
Read the plan like a **recipe's prep-list written as a tree**. The leaves are "wash the vegetables" (scans); each parent is "mix the bowls" (joins), and every line shows "how many carrots you *expect* (rows) and how long you *think* it'll take (cost)". `ANALYZE` is the kitchen timer: after cooking, every step shows "actually took X ms, actually made Y carrots". A perfect recipe has expectations ≈ actuals. When they diverge wildly — you expected 10 carrots but got 10,000,000 — *that* step is where the meal goes wrong, and fixing *that* step (an index, a rewritten join) fixes the whole meal. You never need to time the entire meal; the mislabeled step is the culprit.

## 6. Real-World Analogy
A **freight-forwarder auditing a shipping plan**. The plan (EXPLAIN) says: "truck A: 10 pallets, 2 hours; transfer at warehouse B; truck C: 5 pallets, 1 hour." The manifest counters (ANALYZE) report after the run: "truck A actually carried 40 pallets and took 9 hours." The discrepancy — the plan expected 10 pallets because a forecast (statistics) was wrong — is the exact node to fix. Without the plan, you'd just know "shipment was slow." With it, you know the *forecast for truck A* was broken (stale stats) or truck A took the wrong route (bad access path) or a driver was waiting (buffer/cache issue). The plan + actuals pair turns "shipment slow" into "truck A's forecast is wrong — refresh the forecast."

## 7. Formal Definition
`EXPLAIN <stmt>` returns the physical plan produced by the optimizer: a tree of operator nodes, each annotated with estimated rows, estimated tuple width, and an estimated cost interval (`cost=start..end`) measured in arbitrary cost units (I/O + CPU). `EXPLAIN ANALYZE` additionally executes and annotates each node with measured rows, average/actual time, and loops. Cost units differ by engine and are only comparable *within* a plan for *ranking* operators, not as wall-clock time. Node examples: Seq Scan, Index Scan, Index Only Scan, Bitmap Heap Scan, Nested Loop, Hash Join, Merge Join, Sort, Hash Aggregate, Gather/Parallel. Read order: bottom-up; each node's totals include its children.

## 8. Example
```sql
EXPLAIN ANALYZE
SELECT c.name FROM orders o
  JOIN customers c ON c.id = o.customer_id
 WHERE o.amount > 1000;
```
Output (simplified Postgres):
```
Hash Join  (cost=1234.56..5678.90 rows=54321 width=20) (actual time=10.2..420.5 rows=45000 loops=1)
  Hash Cond: (o.customer_id = c.id)
  ->  Seq Scan on orders o (cost=0.00..1000.00 rows=60000 width=4)
        (actual time=0.1..30.0 rows=60000 loops=1)
        Filter: (amount > 1000)
  ->  Hash (cost=1200.00..1200.00 rows=50000 width=20) (actual time=9.5..9.5 rows=50000 loops=1)
        ->  Seq Scan on customers c (cost=0.00..1100.00 rows=50000 width=20)
              (actual time=0.1..15.0 rows=50000 loops=1)
```
Reading it: estimates ≈ actuals everywhere (good stats), the Filter is at the scan (pushdown worked), Hash Join with a full customers hash build — 45000 output rows at ~420ms. If the `orders` filter had estimated 60000 but actual was 6,000,000, the *statistics* on `amount` would be the problem (bloat/stale `ANALYZE`), and a better index might not even be the fix — stats are.

## 9. Internal Working
1. **Plan capture**: the optimizer's search (Section 01) produces the final tree; `EXPLAIN` serializes it with per-node annotations (estimates from `relcache` statistics: `pg_statistic`, histogram/`n_distinct`, table cardinality from `pg_class.reltuples`).
2. **Without ANALYZE**: print & return; no execution (safe on huge data).
3. **With ANALYZE**: wrap the executor; each node instruments its own `start_time`/`rows`/`loops`; on completion, print the measured values beside the estimates. `BUFFERS` adds `Instrumentation` counters for shared/local buffer hits and reads.
4. **Numeric details**: "actual time" is per-*loop* (divide by `loops`); "rows" is per loop; cost is cumulative-from-left edge. For parallel plans, each worker gets a `Workers` line.
5. **MySQL 8.0**: `EXPLAIN` (rows = estimate, Extra = access info: "Using index", "Using where", "Using temporary/filesort"); `EXPLAIN ANALYZE` gives actuals; `FORMAT=JSON` gives per-node cost/rows; `EXPLAIN FORMAT=TREE` gives the readable tree.

## 10. Time Complexity
- `EXPLAIN` alone: O(plan construction) — microseconds-to-milliseconds, independent of data size; safe on any table.
- `EXPLAIN ANALYZE`: executes the query — O(runtime of the query); *never* run it on a query you can't afford to run (DDL-wrapped EXPLAIN, huge queries, writes — use `EXPLAIN ANALYZE` carefully or wrap in `BEGIN ... ROLLBACK`).
- Cost units are cumulative and additive; per-node cost ≈ work unit estimate, ranked against siblings.
- The *value* is diagnostic speed: localizing the bottleneck costs one run instead of dozens of index experiments.

## 11. Advantages
- **Non-destructive diagnosis**: `EXPLAIN` reads nothing — free and safe.
- **Per-node granularity**: pinpoint the exact operator and its estimates-vs-actuals.
- **Statistics divergence visible**: the estimated-vs-actual gap is a direct, actionable signal (stale stats, correlated columns).
- **Engine-standard**: the same skill transfers to Postgres, MySQL, SQL Server (estimated/actual plans), Oracle (`DBMS_XPLAN`).
- **Tunable detail**: `BUFFERS`, `TIMING`, `VERBOSE`, `COSTS`, JSON formats let you zoom.
- **Teaching tool**: reading plans is how engineers learn optimizer behavior for real.

## 12. Disadvantages
- **Not wall-clock time**: cost units are relative; beginners misread "cost" as latency.
- **`ANALYZE` runs the query**: dangerous for writes / huge datasets without a transaction wrapper.
- **Sampling/parallel variance**: actual times fluctuate run-to-run; need `ANALYZE` loops or averaging to judge.
- **No guidance**: EXPLAIN shows *what*, not *why* (why a seq scan won) — requires optimizer/trace knowledge to explain choices.
- **Opaque for parameterized/`PREPARE`d queries**: the generic plan may differ from the runtime one (`EXPLAIN EXECUTE` needed).
- **Verbose for large trees**: dozens of nodes make humans miss the bottleneck; requires filtering skill.

## 13. Interview Questions
1. **Q: Difference between EXPLAIN and EXPLAIN ANALYZE?** A: EXPLAIN shows the estimated plan (doesn't run); EXPLAIN ANALYZE executes and shows actuals per node. Comparing the two reveals estimation errors — the source of bad plans.
2. **Q: TRICKY: What does "actual time=10.2..420.5 rows=45000 loops=1" mean?** A: Per-*loop* averages for this node's subtree: startup (first row) 10.2ms, total 420.5ms, 45000 rows returned per loop, executed once. If `loops`>1, divide totals by loops to get per-iteration cost.
3. **Q: What is a "rows" estimate vs "actual rows"?** A: Estimate comes from statistics (histograms, `reltuples`, `n_distinct`, selectivity functions) before execution; actual is measured at runtime. Big divergence = bad stats → bad plan choice.
4. **Q: What are the three classic plan pathologies?** A: (1) A Seq Scan on a large table when an index would serve (missing index, or selectivity underestimated); (2) a bad join order (large join early) — often from bad cardinality estimates; (3) a Sort or Hash that spills to disk (work_mem too small) — visible via buffers/memory in the plan.
5. **Q: PR: When would you see "Seq Scan" yet it's actually optimal?** A: When the table is small (few pages), when the predicate is not selective (returns most rows), or when it's a scanning whole table for a bulk load — index scans have per-row I/O overhead and aren't free. Seq Scan isn't a bug by itself; it's context-dependent.
6. **Q: What does "Index Only Scan" mean?** A: All needed columns are in the index (covering index), so the heap is never touched — typically the fastest scan. PostgreSQL can also use `visibility map` to avoid heap checks for all-visible pages.
7. **Q: TRICKY: What is a "Bitmap Heap Scan"?** A: Postgres's middle ground: Bitmap Index Scan builds a bitmap of matching pages from the index, then Bitmap Heap Scan fetches those pages once — effective when the predicate matches many rows (index would cause lots of random I/O) but not all rows.
8. **Q: How do you know a query needs an index?** A: From the plan: a Seq Scan on a large table whose Filter returns few rows is the classic signal — an index on the filter column(s) would change the plan. Verify before AND after by comparing `EXPLAIN` plans.
9. **Q: What does "rows=60000" on a scan with a Filter tell you?** A: That the estimate says 60000 rows pass the filter after scanning — if actual is wildly different, the column statistics (histogram) are stale or the predicate uses a correlated/volatile expression (functions, `LOWER()`, OR-clauses) the optimizer can't estimate.
10. **Q: What is `work_mem` and how does it show in EXPLAIN?** A: Per-operation memory for sorts/hashes/aggregates. If a Sort/Hash node "spills to disk" (Postgres: "External Sort", `EXPLAIN (ANALYZE, BUFFERS)` temp file writes; MySQL: "Using filesort" with temp table), raising `work_mem` per-query can eliminate the spill — but it's *per operation*, not global.
11. **Q: PR: A slow query got faster after `ANALYZE` without any schema change. Why?** A: Stale statistics were causing the optimizer to pick a bad plan (wrong join order / seq scan); refreshing stats updated the cardinality estimates, and the optimizer chose the right plan. This is why autovacuum/autoanalyze matter.
12. **Q: What is the "Filter" vs "Index Cond" distinction?** A: Index Cond is applied during the index scan (B-tree range); Filter is applied after (rechecking rows, e.g., non-indexable predicates like `LOWER(col)=...`). Pushdown means filters sit as low as possible.
13. **Q: How do you read a Hash Join node?** A: Inner side (right, under "Hash") is scanned once and built into a hash table; outer side (left) is probed. Build side is scanned fully once — pick the *smaller* relation as the build side (the optimizer does this; the plan shows which).
14. **Q: TRICKY: `EXPLAIN ANALYZE` on an UPDATE/DELETE?** A: It executes the write. Wrap in `BEGIN; EXPLAIN ANALYZE UPDATE ...; ROLLBACK;` to see the plan without committing — though the executor still modifies rows during the run (WAL/undo), so it's not free.
15. **Q: What is a "Nested Loop" and when is it preferred?** A: For each row of the outer, scan the inner — good when outer is small and inner has an index (indexed nested loop join). It's preferred when hash/merge would be overkill (tiny input) or when outer is very selective.

## 14. Follow-Up Questions
1. **Q: What does "Rows Removed by Filter" tell you?** A: The number of rows scanned that the filter rejected — huge values mean a broad scan is happening (pushdown not useful / no index) and the filter is applied after reading pages.
2. **Q: What is a "Sort Method: quicksort / external merge"?** A: In-memory (quicksort) vs disk (external merge with temp files) sort. "External" = spill = `work_mem` tuning candidate. Also "presorted input" when an index already provides order (no sort needed).
3. **Q: How do parallel plans look?** A: "Gather"/"Gather Merge" nodes split work across workers; each worker's scan has a "Workers Planned/Launched" line, and "Worker 0/1" subtrees show per-worker actuals. Watch for skewed per-worker times (bad distribution).
4. **Q: What is a "Materialize" node?** A: Caches a subtree's output (spool) to be reused — helps when the same input is probed repeatedly (e.g., in nested-loop outer). Appears automatically; rarely a tuning target.

## 15. Coding Example
```sql
-- 1. Pure estimate (safe on huge tables)
EXPLAIN SELECT * FROM customers WHERE country = 'IN';

-- 2. Execute and compare (careful: runs the query)
EXPLAIN ANALYZE SELECT * FROM customers WHERE country = 'IN';

-- 3. Add buffers to diagnose I/O vs CPU
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM customers WHERE country = 'IN';
-- shared hit=1200, shared read=0   → fully cached
-- shared read=400000              → reading from disk (bloat / no cache)

-- 4. Check for sort spill
SET work_mem = '4MB';
EXPLAIN (ANALYZE, BUFFERS) SELECT country, count(*) FROM customers
  GROUP BY country ORDER BY country;
-- Look for "external merge Disk" / temp files under Buffers → raise work_mem

-- 5. MySQL 8.0
EXPLAIN FORMAT=TREE SELECT * FROM customers WHERE country = 'IN';
EXPLAIN ANALYZE SELECT * FROM customers WHERE country = 'IN';
```
```sql
-- 6. Parameterized queries: the plan for the prepared statement
PREPARE q(int) AS SELECT * FROM orders WHERE amount > $1;
EXPLAIN EXECUTE q(1000);
```
```sql
-- 7. Auto-capture every slow query (production diagnostic)
ALTER SYSTEM SET auto_explain.log_min_duration = '500ms';   -- log plans > 500ms
ALTER SYSTEM SET auto_explain.log_analyze = on;
ALTER SYSTEM SET auto_explain.log_buffers = on;
-- requires: shared_preload_libraries = 'auto_explain'
```

## 16. Industry Usage
- **PostgreSQL**: `EXPLAIN (ANALYZE, BUFFERS, TIMING)` is the community standard; `auto_explain` logs slow-query plans in production; `pg_stat_statements` pairs latency with plan fingerprints.
- **MySQL 8.0**: `EXPLAIN ANALYZE` (8.0.18+), `EXPLAIN FORMAT=TREE/JSON`, `optimizer_trace` for why; the `EXPLAIN` "Extra" column (`Using index`, `Using filesort`, `Using temporary`) is the diagnostic vocabulary.
- **SQL Server**: "Actual Execution Plan" in SSMS (runtime), "Estimated Execution Plan" (cost-only); `SET STATISTICS IO, TIME` for counters.
- **Oracle**: `EXPLAIN PLAN` + `DBMS_XPLAN` (including `+COST`, `+BUFFERS`); the diagnostic skill transfers 1:1.
- **Warehouses (BigQuery, Snowflake, Redshift)**: the same operator trees (scan→join→aggregate→sort) exposed via their EXPLAIN — the reading skill scales to distributed engines.

## 17. References
- PostgreSQL docs, "EXPLAIN": https://www.postgresql.org/docs/current/sql-explain.html and "Using EXPLAIN": https://www.postgresql.org/docs/current/using-explain.html
- PostgreSQL docs, `auto_explain`: https://www.postgresql.org/docs/current/auto-explain.html
- MySQL docs, "EXPLAIN Statement": https://dev.mysql.com/doc/refman/8.0/en/explain.html
- Silberschatz, *Database System Concepts*, Ch. 14-15 (plan reading).
- depesz.com, "explain.depesz.com" — plan visualizer used industry-wide.

## 18. Cheat Sheet
- Read bottom-up, inside-out; each node's totals include children.
- Estimates (EXPLAIN) vs actuals (ANALYZE) — divergence = stats/estimation bug.
- "actual time" and "rows" are per *loop*; multiply/divide by `loops`.
- Three pathologies: bad Seq Scan (missing index/low selectivity), bad join order (wrong cardinality), spill to disk (work_mem).
- Add `BUFFERS`: `shared read` = disk I/O, `shared hit` = cached.
- Index Only Scan < Index Scan < Bitmap < Seq Scan (roughly, data-dependent).
- "External Sort"/"Filesort" = work_mem spill.
- Never `EXPLAIN ANALYZE` a write without `BEGIN ... ROLLBACK`.
- `auto_explain.log_min_duration` captures production plans automatically.
- "Filter" = post-scan recheck; "Index Cond" = applied during index scan.

## 19. Quiz
1. Which runs the query? a) EXPLAIN b) EXPLAIN ANALYZE c) both d) neither → **b**
2. Cost units in Postgres are: a) ms b) arbitrary units, relative c) bytes d) loops → **b**
3. A Seq Scan is always wrong: a) true b) false → **b** (context/data-dependent)
4. Estimated-vs-actual divergence signals: a) slow disk b) bad stats c) broken index d) corrupt data → **b**
5. "External Sort" means: a) no sort b) spill to disk c) fast path d) index sort → **b**
6. Index Only Scan avoids: a) the index b) the heap c) the filter d) the sort → **b**
7. Which wraps a write safely for ANALYZE? a) COMMIT b) BEGIN/ROLLBACK c) autocommit d) EXPLAIN-only → **b**
8. `shared read` high + `shared hit` low means: a) cached b) disk-heavy c) parallel d) sorted → **b**

## 20. Flashcards
- **Q: EXPLAIN vs EXPLAIN ANALYZE?** → **A:** Plan-only vs execute-and-measure; compare estimates vs actuals.
- **Q: Read direction?** → **A:** Bottom-up / inside-out; children feed parents.
- **Q: 3 plan pathologies?** → **A:** Bad seq scan, bad join order, disk spill.
- **Q: "actual time" is per?** → **A:** Per loop (divide by loops).
- **Q: What flag adds I/O counters?** → **A:** `BUFFERS` (shared hit/read).
- **Q: Seq scan is optimal when?** → **A:** Small table / non-selective predicate / bulk.
- **Q: Estimated rows come from?** → **A:** Statistics (histogram, reltuples, selectivity).
- **Q: What catches slow-query plans in prod?** → **A:** `auto_explain.log_min_duration`.

## 21. Revision
EXPLAIN = the optimizer's chosen plan with estimates; EXPLAIN ANALYZE adds measured actuals. Read bottom-up, mind per-loop values, add BUFFERS to separate I/O from CPU. Diagnose the three pathologies (seq scan, join order, spill). Fix statistics first — the plan is a symptom of the estimates. Verify any index/schema change by comparing before/after plans.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "EXPLAIN vs EXPLAIN ANALYZE?" | 2, 8, 13 |
| "How do you read this plan?" | 8, 9, 13 |
| "Three classic plan problems?" | 13 |
| "When is a Seq Scan optimal?" | 13 |
| "Index Only / Bitmap scans?" | 13 |
| "How do stats affect plans?" | 9, 13 |
| "Why did ANALYZE fix a slow query?" | 13 |
| "How do you check for spills?" | 13, 15 |
