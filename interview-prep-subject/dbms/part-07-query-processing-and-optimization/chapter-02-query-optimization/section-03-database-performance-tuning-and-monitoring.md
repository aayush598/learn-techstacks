# Database Performance Tuning and Monitoring

> **TL;DR**: Production performance is a feedback loop — index the hot access paths, keep statistics fresh (autovacuum/analyze), size per-operation memory (work_mem, shared_buffers, buffer pool), and monitor slow queries (pg_stat_statements, auto_explain, slow-query logs) so every regression becomes an EXPLAIN-diagnosable, verifiable fix.

## 1. Why Does This Exist?
Even with a great optimizer (Section 01) and the ability to read plans (Section 02), production queries degrade: data grows, workloads shift, statistics go stale, memory pressure builds, and indexes go unused or bloated. Tuning & monitoring exists to (a) *keep* the optimizer's inputs correct (fresh stats, right indexes, enough memory) and (b) *detect* regressions fast (slow-query instrumentation) so that "the app is slow" becomes "this query's plan is bad, here's why, here's the verified fix." Without this loop, databases are a black box that slows down silently until an outage.

## 2. How Does It Work?
- **Indexing strategy**: identify hot predicates and joins (from slow queries + workload analysis), create covering/composite/partial indexes, and verify with EXPLAIN before/after. Remove unused indexes (write amplification).
- **Statistics hygiene**: `VACUUM ANALYZE`/`ANALYZE` keeps `pg_statistic`/`pg_class.reltuples` current; autovacuum does this automatically (thresholds + scale factors); targeted `ANALYZE` after bulk loads.
- **Memory sizing**: `shared_buffers` (Postgres) / `innodb_buffer_pool_size` (MySQL) hold hot pages; `work_mem`/`sort_buffer_size`/`join_buffer_size` are per-operation memory. Correct sizing eliminates disk spills.
- **Monitoring loop**: `pg_stat_statements` (normalized query stats: calls, total/max time, rows), `auto_explain` (logs plans over a duration threshold), slow-query logs (MySQL `slow_query_log`, `long_query_time`), and `VACUUM`/bloat tracking. Each slow entry → EXPLAIN → fix → re-measure.

## 3. When Is It Used?
- Onboarding a new app: set base memory/autovacuum/stat-statements config, add indexes for known queries.
- Incident response: "API latency spiked" → pull slowest statements → EXPLAIN → fix (index, work_mem, rewritten query).
- Capacity planning: growth → re-evaluate buffer pool, autovacuum, index bloat.
- After upgrades/migrations: confirm plans and latencies are stable.
- Recurring hygiene: weekly/monthly bloat checks, unused-index reports, autovacuum lag monitoring.
- Interviews: "how do you tune a slow database?", "what's the monitoring loop?", "buffer pool vs work_mem".

## 4. Why Wasn't Another Approach Chosen?
- *"Just add indexes" shotgun*: indexes aren't free (write amplification, storage); the EXPLAIN-first loop targets the actual plan defect. The plan is the ground truth; guessing wastes I/O and time.
- *Raise memory blindly*: `shared_buffers` beyond ~30-40% of RAM causes cache thrash; `work_mem` is *per operation* — scaling it globally explodes memory under many concurrent sessions. Sizing must be data-aware (physical RAM, workload, EXPLAIN spills).
- *Rewrite all queries by hand*: usually unnecessary — most regressions are stats/indexes/memory; rewriting is the last resort after EXPLAIN proves the shape is wrong.
- *Monitoring without tuning / tuning without monitoring*: either is blind — metrics without EXPLAIN can't localize the node; EXPLAIN without metrics can't detect regressions. The two halves make the loop.
- *Hardware-scale-out first*: adding RAM/CPU is a hammer; it can mask (not fix) bad plans and is expensive. Tune before buying, buy after proving you've exhausted software fixes.

## 5. Intuition
Think of the database as a **kitchen that cooks every dish per a menu (plans)**. Tuning = keeping the *menu accurate*: the recipe book's page-count estimates (statistics) are current, the right tools are on the counter (indexes), and the pantry has room (buffer pool) so you don't run to the store (disk) for every ingredient. Monitoring = the *head-chef's clipboard*: it records which dishes take longest (`pg_stat_statements`), and when a dish suddenly slows, it flags the recipe (auto_explain prints the plan) so you can see exactly which step drifted. The fix is never "cook everything twice as fast" (raise memory) — it's "this dish's recipe assumed 10 carrots but the market now delivers 10,000 (stale stats), so the cook is peeling 10,000." Fix the assumption; the dish speeds up.

## 6. Real-World Analogy
A **supply-chain team and their ERP**. Order history shows order lines 40x larger than last month; the MRP (optimizer) keeps picking the same batching plan that assumed small orders, so pickers (scans) handle far more units than planned. Monitoring (a dashboard of slow batches) flags it; EXPLAIN (the batch plan) shows the forecast assumed old order volumes — i.e., *statistics are stale* (orders table not re-analyzed after a bulk load). Fix: re-run the forecast (`ANALYZE`), and re-layout the warehouse for big orders (index on order size; add pickers near the hot zone). Then the dashboard shows the batch back to target. Same inventory, same people — the *planning inputs* were stale, and the fix was to refresh them, not to hire more pickers.

## 7. Formal Definition
Tuning = adjusting configuration and schema so the optimizer's *cost model inputs* (statistics: cardinalities, histograms, distinct counts) and *execution resources* (memory: buffer pool for page cache; work_mem for sorts/hashes/aggregates; I/O: index structures) produce the intended physical plans at acceptable latency. Monitoring = continuously recording per-statement metrics (normalized SQL → calls, mean/max/p99 latency, rows, plans) and emitting plans for statements above a latency threshold. The loop: metric flags query → plan identifies node → fix input (stats/index/memory/rewrite) → re-measure.

## 8. Example
Symptom: API endpoint slowed 10x. Monitoring:
```
pg_stat_statements:
 query | calls | total_time_ms | mean_time_ms | max_time_ms | rows
 'SELECT * FROM orders WHERE amount > $1' | 5000 | 900000 | 180 | 2000 | 45000
```
ACTION 1 — read the plan:
```
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE amount > $1;  -- with a typical $1
Seq Scan on orders (actual rows=6000000 ...) Filter: (amount > 1000)
-- estimates say 6000 rows, actual is 6M → stats stale on amount
```
ACTION 2 — refresh stats:
```
ANALYZE orders;  -- or wait for autovacuum; or set higher autovacuum_analyze_scale_factor
```
ACTION 3 — re-EXPLAIN: the optimizer now sees the true histogram, adds an index if the predicate is still selective:
```
CREATE INDEX idx_orders_amount ON orders(amount) WHERE amount > 1000;  -- maybe partial
EXPLAIN (ANALYZE, BUFFERS) ... -- now Index Scan, 5ms
```
ACTION 4 — verify in monitoring: `pg_stat_statements` shows the mean time back to ~5ms. That's the full loop in one example.

## 9. Internal Working
1. **Statistics refresh**: `ANALYZE` scans a sample of a table, builds `pg_statistic` (histogram bounds, `n_distinct`, most-common-values, null fraction) and updates `pg_class.reltuples`. Autovacuum triggers `analyze` based on `autovacuum_analyze_threshold` (default 50) + `autovacuum_analyze_scale_factor` (0.1 — analyze after 10% of tuples changed).
2. **Index management**: the planner picks indexes from `pg_class`; bloat (dead tuples, fragmentation from updates) makes scans read extra pages; `VACUUM`/`REINDEX`/`pg_repack` reclaim. `pg_stat_user_indexes` shows idx_scan counts → unused-index candidates.
3. **Memory**: `shared_buffers` (page cache, default 128MB) and MySQL `innodb_buffer_pool_size` (default 128MB, 8.0 auto-sizes); `work_mem` (default 4MB) allocated per sort/hash/agg operation, capped by total concurrent operations; spills visible in `EXPLAIN BUFFERS` temp writes / `pg_stat_database.temp_files`.
4. **Monitoring**: `pg_stat_statements` aggregates by queryid (normalized SQL), rolling the data in memory + `pg_stat_statements.max`; `auto_explain` hooks the executor, logging `EXPLAIN ANALYZE` for statements over `log_min_duration`; MySQL's slow log writes rows > `long_query_time` with optional plan capture; all feed dashboards (Datadog, Grafana, pgbadger).
5. **Query rewrite as last resort**: after stats/index/memory proven, restructure the SQL (avoid functions on indexed columns, decompose monster joins, use covering/partial indexes) — each change re-enters the loop with a before/after EXPLAIN.

## 10. Time Complexity
- `ANALYZE` on a sample: O(sample size), configurable via `default_statistics_target` (default 100 histogram buckets — more = better estimates, costlier analyze).
- Index lookup: O(log N) B-tree probes + heap fetches; covering indexes avoid heap fetches entirely.
- Buffer pool hit: ~ns-µs (memory); miss: ms (disk) — the gap the cache exists to bridge.
- `pg_stat_statements` overhead: negligible (µs per statement); `auto_explain` adds plan cost only above the threshold.
- The loop's complexity: linear in the number of slow statements; each iteration is EXPLAIN (fast) → fix (small) → verify (fast).

## 11. Advantages
- **Targeted**: fixes the actual plan defect instead of guessing.
- **Verifiable**: every change has a before/after EXPLAIN + metric delta.
- **Data-driven**: monitoring turns intuition into a prioritized backlog (top-N slowest).
- **Proactive**: thresholds (auto_explain, autovacuum) catch regressions before users do.
- **Low risk**: stats refresh, index adds, and memory raises are reversible/gradual.
- **Portable**: the loop (monitor → plan → fix → verify) is the same in Postgres, MySQL, SQL Server, Oracle.

## 12. Disadvantages
- **No silver bullet**: correlated columns, functions on indexed columns, and skewed data defeat simple fixes — need advanced stats (extended statistics), expression indexes, or rewrites.
- **Bloat grows quietly**: unfixed bloat (failed autovacuum, long-running txns, heavy updates) degrades scans; requires vigilance.
- **Memory trade-offs**: shared_buffers vs OS page cache; too large = cache thrash; work_mem per-operation explosion risk.
- **Monitoring has its own cost/ops**: pg_stat_statements storage, log volume, dashboard maintenance.
- **Autovacuum can lag or miss**: scale-factor heuristics are blunt for sudden bulk loads (needs manual `ANALYZE`).
- **Tuning knowledge is deep**: many knobs interact (autovacuum vs lock contention; work_mem vs parallel workers); wrong tuning makes things worse.

## 13. Interview Questions
1. **Q: What's your process for a slow query in production?** A: (1) Find the query (pg_stat_statements / slow log); (2) read the plan (`EXPLAIN (ANALYZE, BUFFERS)`); (3) compare estimates vs actuals; (4) fix the *input* (stats, index, memory) — not the symptom; (5) verify with a before/after plan + metrics. Never "just add an index."
2. **Q: What is pg_stat_statements?** A: A Postgres extension that aggregates statistics per normalized query (calls, total/mean/max time, rows, shared-blocks-read) — the primary tool for finding the slowest/hot queries and detecting regressions.
3. **Q: TRICKY: Why did adding an index not speed up my query?** A: Either the predicate isn't selective (index returns most rows — seq scan wins), the query does a sort/aggregate the index doesn't help (need different index / covering), the optimizer's stats are stale so it didn't choose it (ANALYZE), or the index isn't indexable (function/expression without an expression index). The EXPLAIN before/after tells you which.
4. **Q: What is the difference between shared_buffers and work_mem?** A: shared_buffers (Postgres) is the shared page cache for all sessions/table data; work_mem is *per-operation* memory for a sort/hash/aggregate in a single query. Raising shared_buffers caches more pages; raising work_mem prevents spills but multiplies by concurrent operations.
5. **Q: What is autovacuum and why does it matter?** A: Postgres background processes that (a) VACUUM dead tuples/bloat and (b) ANALYZE statistics, triggered by tuple-change thresholds. It keeps bloat low and stats current — the two things that silently degrade plans.
6. **Q: PR: Bulk-loaded a table; queries are suddenly slow. What happened?** A: `reltuples`/statistics are stale after a bulk load (autovacuum hasn't caught up), so the optimizer mis-estimates selectivity → wrong plans. Fix: `ANALYZE <table>` (and optionally `VACUUM`), then re-check plans. Consider `autovacuum_analyze_scale_factor` tuning for such workloads.
7. **Q: How do you find unused indexes?** A: Postgres: `pg_stat_user_indexes.idx_scan` ~0 over a representative period → candidates; MySQL: `performance_schema.table_io_waits_summary_by_index_usage`. Verify impact (write overhead, bloat) before dropping. Dropping unused indexes reduces write amplification and vacuum work.
8. **Q: What is index bloat and how do you fix it?** A: Repeated updates/delete leave dead entries and fragmentation inside B-trees — scans read extra pages. Fix: `VACUUM (FULL)` / `REINDEX` / `pg_repack`; prevent via adequate `fillfactor` for update-heavy tables.
9. **Q: TRICKY: `work_mem=64MB` but my hash join still spilled. Why?** A: work_mem is per operation — a plan with several sorts/hashes each gets its own 64MB, and the *total* can exceed expectations; also parallel workers each allocate their own. Check `EXPLAIN BUFFERS` for "temp file writes"; raise the relevant setting via `SET LOCAL` for the specific query first.
10. **Q: What is a covering index?** A: An index containing all columns a query needs (INCLUDE columns), so the planner can use "Index Only Scan" and skip heap fetches entirely — often the cheapest read.
11. **Q: How do you detect a plan regression?** A: Track mean/p99 latency per normalized query (pg_stat_statements); when it jumps, pull the current `EXPLAIN` and diff it against the historical plan (capture plans into a repo / `EXPLAIN (FORMAT JSON)` snapshots). Roll back the change (stats, schema, version) if it's a regression.
12. **Q: PR: The optimizer ignores my brand-new index.** A: (1) `ANALYZE` the table so the planner knows about it/cardinality; (2) check the predicate is indexable (no function unless expression index); (3) check selectivity — the optimizer may correctly prefer a seq scan; (4) verify with `EXPLAIN ANALYZE`, don't force with hints.
13. **Q: What is a partial index?** A: An index on a subset of rows (`CREATE INDEX ... WHERE ...`) — smaller, faster for that predicate, and useful for hot, selective predicates over mostly-old data. Example: index only active orders.
14. **Q: What is a slow-query log?** A: MySQL logs statements exceeding `long_query_time` (with plans via `log_queries_not_using_indexes`/`EXPLAIN` capture); Postgres has `log_min_duration_statement` and `auto_explain` for plans. Both feed pgbadger/pt-query-digest analysis.
15. **Q: TRICKY: Everything is cached (hit=100%) but the query is still slow. Why?** A: The bottleneck moved to CPU: expensive sorts/hashes/aggregates, a bad join order generating huge intermediates, or a function-heavy filter — plan shows the dominant node; fix by reducing work (index to avoid sort, covering index, better join order), not more cache.

## 14. Follow-Up Questions
1. **Q: What are extended statistics and when are they needed?** A: Postgres 12+ `CREATE STATISTICS` captures correlations and n-distinct for multiple columns — when single-column histograms badly mis-estimate (e.g., `WHERE city='X' AND age>50` correlated), the optimizer under/over-estimates join sizes.
2. **Q: What is `fillfactor` and how does it fight bloat?** A: Percentage of each B-tree page to fill on insert (default 100); leaving headroom (e.g., 70) lets in-place updates stay on-page, reducing page splits and dead tuples for update-heavy tables.
3. **Q: How do parallel query settings interact with memory?** A: Parallel workers each allocate per-operation memory (work_mem × workers), so enabling parallelism raises memory pressure; balance `max_parallel_workers_per_gather` with work_mem.

## 15. Coding Example
```sql
-- 1. Find the slowest queries (the monitoring loop's start)
SELECT queryid, calls, mean_exec_time, max_exec_time, rows,
       shared_blks_hit, shared_blks_read
  FROM pg_stat_statements
 ORDER BY mean_exec_time DESC LIMIT 10;
```
```sql
-- 2. Capture the plan of a slow query (use the queryid's template)
EXPLAIN (ANALYZE, BUFFERS, TIMING)
SELECT * FROM orders WHERE amount > 1000;
```
```sql
-- 3. Fix inputs, verify each step
ANALYZE orders;                              -- refresh stats
CREATE INDEX IF NOT EXISTS idx_orders_amount ON orders(amount);
EXPLAIN (ANALYZE, BUFFERS)                   -- confirm Index Scan now
SELECT * FROM orders WHERE amount > 1000;
```
```sql
-- 4. Memory settings (compare before/after; spills gone?)
SHOW shared_buffers;      -- e.g., 128MB (too small for big OLTP)
SHOW work_mem;            -- 4MB default
SET LOCAL work_mem = '64MB';   -- only for this session/query
EXPLAIN (ANALYZE, BUFFERS) SELECT customer_id, count(*) FROM orders GROUP BY customer_id;
-- "Sort Method: quicksort Memory: 12kB" (in-memory) vs "external merge Disk"
```
```sql
-- 5. Unused-index hunt
SELECT s.relname, s.indexrelname, s.idx_scan
  FROM pg_stat_user_indexes s
 WHERE s.idx_scan = 0
 ORDER BY s.relname;
```
```sql
-- 6. Production tripwire (auto_explain on slow statements)
-- config (postgresql.conf):
-- shared_preload_libraries = 'auto_explain,pg_stat_statements'
-- auto_explain.log_min_duration = '500ms'
-- auto_explain.log_analyze = on
-- auto_explain.log_buffers = on
```

## 16. Industry Usage
- **PostgreSQL**: the loop above is standard practice (pg_stat_statements + auto_explain + autovacuum + EXPLAIN). Cloud (RDS/Aurora) exposes these via Performance Insights.
- **MySQL 8.0**: `innodb_buffer_pool_size`, slow-query log + `pt-query-digest`, `performance_schema` for index/IO wait stats; `EXPLAIN ANALYZE` for verification.
- **SQL Server**: Query Store (plan history + regression alerts), missing-index DMVs, `sys.dm_exec_query_stats`.
- **Oracle**: AWR/ADDM reports, `DBMS_AUTO_TUNING`, SQL tuning advisor — the same monitor→plan→fix loop, enterprise-grade.
- **Warehouses (BigQuery/Snowflake)**: monitoring via query profile UI, slot utilization; "tuning" = partitioning/clustering and query shape rather than buffer pools.

## 17. References
- PostgreSQL docs, "Tuning Your PostgreSQL Server": https://www.postgresql.org/docs/current/runtime-config-resource.html
- PostgreSQL docs, `pg_stat_statements`: https://www.postgresql.org/docs/current/pgstatstatements.html
- PostgreSQL docs, "VACUUM" & autovacuum: https://www.postgresql.org/docs/current/routine-vacuuming.html
- MySQL docs, "Optimizing Server Settings": https://dev.mysql.com/doc/refman/8.0/en/optimizing-server-parameters.html
- PostgreSQL Wiki, "Indexes / Performance": https://wiki.postgresql.org/wiki/Performance_Optimization
- Use The Index, Luke (Markus Winand): https://use-the-index-luke.com/

## 18. Cheat Sheet
- Loop: monitor → EXPLAIN → fix input (stats/index/memory) → verify → repeat.
- pg_stat_statements: top-N slow queries, regressions, rows.
- auto_explain: auto-log plans for slow statements (threshold).
- ANALYZE after bulk loads; check `reltuples`/stale stats first when plans look wrong.
- Autovacuum: bloat + stats — keep it healthy; watch lag.
- Index: only for selective, indexable predicates; prefer covering/partial; drop unused (idx_scan≈0).
- Memory: shared_buffers = page cache; work_mem = per-operation; buffer pool (MySQL) = cache; watch spills in EXPLAIN BUFFERS.
- Spill ("external merge"/"temp files") → raise work_mem for that query (SET LOCAL).
- Bloat fixes: VACUUM (FULL)/REINDEX/pg_repack, fillfactor for hot-update tables.
- Only rewrite SQL after stats/index/memory are proven; verify each step with EXPLAIN before/after.

## 19. Quiz
1. First step of a slow-query investigation? a) add index b) EXPLAIN c) increase RAM d) restart → **b**
2. pg_stat_statements aggregates by: a) session b) normalized query c) table d) index → **b**
3. Stale stats cause: a) correct plans b) wrong estimates → bad plans c) crashes d) nothing → **b**
4. work_mem is: a) global b) per-operation c) per-database d) per-index → **b**
5. An index with idx_scan=0 is: a) essential b) a drop candidate c) broken d) hidden → **b**
6. Bloat from updates is fixed by: a) ANALYZE b) VACUUM/REINDEX c) work_mem d) indexes → **b**
7. After a bulk load you should: a) ANALYZE b) SET work_mem c) drop indexes d) restart → **a**
8. auto_explain triggers on: a) all queries b) duration threshold c) errors d) first run → **b**

## 20. Flashcards
- **Q: The tuning loop?** → **A:** Monitor → EXPLAIN → fix input (stats/index/memory) → verify.
- **Q: Tool to find slowest queries?** → **A:** pg_stat_statements / slow-query log.
- **Q: Why are stale stats bad?** → **A:** Wrong estimates → wrong plan choices → slow queries.
- **Q: work_mem vs shared_buffers?** → **A:** Per-operation memory vs shared page cache.
- **Q: Fix for disk spill?** → **A:** Raise work_mem (per query: SET LOCAL).
- **Q: Unused index signal?** → **A:** idx_scan ≈ 0 in pg_stat_user_indexes.
- **Q: After bulk load?** → **A:** ANALYZE the table.
- **Q: Auto capture plans in prod?** → **A:** auto_explain.log_min_duration.

## 21. Revision
Performance = keeping optimizer inputs correct. Three levers: statistics (ANALYZE/autovacuum), schema (indexes: covering/partial, drop unused), memory (buffer pool + work_mem, per-operation). Monitoring (pg_stat_statements + auto_explain) closes the loop: every regression → EXPLAIN → fix → verify. Stats first, then indexes, then memory, rewrite SQL last. This loop is portable across engines and is the operational half of the query-processing story.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Your process for a slow query?" | 2, 8, 13 |
| "What is pg_stat_statements?" | 2, 13 |
| "Why didn't the index help?" | 9, 13 |
| "shared_buffers vs work_mem?" | 4, 13 |
| "Why is autovacuum important?" | 9, 13 |
| "How do you find unused indexes?" | 9, 13 |
| "Bulk load made queries slow?" | 8, 13 |
| "How do you fix index bloat?" | 9, 13 |
