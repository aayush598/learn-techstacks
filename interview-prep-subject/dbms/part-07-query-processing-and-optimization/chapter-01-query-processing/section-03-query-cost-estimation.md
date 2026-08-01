# Query Cost Estimation

> **TL;DR**: The optimizer doesn't run queries — it *estimates* their cost from statistics (cardinality, selectivity, histograms) — and when those estimates are wrong, you get slow queries, which is why "why is this query slow?" usually means "why is the estimate wrong?"

## 1. Why Does This Exist?
The optimizer must choose among exponentially many plans (join orders × algorithms × access paths) without executing them. It needs a *scoring function*: an estimate of the plan's cost (I/O reads, CPU work, memory). Cost estimation exists to (a) rank plans so the cheapest *estimated* plan can be chosen, (b) make the choice deterministic and explainable, and (c) turn data statistics (table sizes, distributions, index stats) into a decision. It's the "brain" that makes a cost-based optimizer intelligent — and it's also its achilles heel: estimates are approximations, and when reality diverges from them, the chosen plan is wrong.

## 2. How Does It Work?
Core quantities:
- **Cardinality**: estimated number of rows an operator outputs (the big driver of cost).
- **Selectivity**: the fraction of rows satisfying a predicate (`WHERE amount > 1000` matching 0.1% ⇒ selectivity 0.001).
- **Statistics**: per-table (reltuples, pages), per-column (null fraction, distinct count `n_distinct`, min/max), and **histograms** (column value distribution, e.g., 100 equal-frequency buckets) — collected by `ANALYZE`/`autovacuum`; extended stats for correlated columns.
- **Cost model**: a weighted sum of I/O and CPU (`seq_page_cost`, `random_page_cost`, `cpu_tuple_cost`, `cpu_index_tuple_cost`, etc.) — per-operator estimates combine children costs bottom-up.
- The optimizer computes candidate plans' costs; joins/sorts/scans each contribute; the cheapest wins.

## 3. When Is It Used?
- Every plan choice: scan (seq vs index vs bitmap), join method/order, aggregation (hash vs sort), sort strategy.
- **`ANALYZE` / `VACUUM ANALYZE`** — refresh statistics; autovacuum/`autovacuum_analyze_threshold` keeps them current.
- **`EXPLAIN`** — shows the *estimates*; `EXPLAIN ANALYZE` reveals estimate-vs-actual divergence (the diagnostic).
- **Parameterized queries** — `n_distinct`, histogram positions, and (Postgres) extended statistics for multi-column correlation.
- In interviews: "what is selectivity?", "why is my estimate wrong?", "how does the optimizer choose between scan types?", "how do histograms help?"

## 4. Why Wasn't Another Approach Chosen?
- *Rule-based optimization (no stats — "always use an index")*: predictable but blind — a rule can't know the index is useless for a 90%-selective predicate. Cost-based optimization is the modern standard (Postgres, MySQL 8, Oracle, SQL Server).
- *Execute-then-decide*: you can't try all plans at runtime; estimation is the only tractable approach. (Some systems use *adaptive* plans — switching at runtime — as a partial answer.)
- *Exact statistics (maintain full distributions)*: storage and update costs are prohibitive; *sampled* statistics + histograms are the accepted approximation.
- *Treat all predicates independently*: cheap but wrong for correlated columns (`city` × `age`); Postgres added **extended statistics** (`CREATE STATISTICS`) to fix exactly this — showing the model is a hierarchy of approximations.
- *Zero statistics (assume uniform/independence)*: uniform assumptions crash on skewed data (a "Mozilla" column with one mega-city); histograms + `most common values` capture skew.

## 5. Intuition
Cost estimation is a **restaurant manager planning the night** before seeing the actual crowd: they estimate how many customers (cardinality), how many want the fish (selectivity), and the kitchen's capacity (I/O costs) to decide how many cooks and which menu. The plan is only as good as the *guesses*. If the manager assumed a quiet Tuesday but a busload arrives, the kitchen collapses — the "plan" was right in principle, wrong in estimate. `EXPLAIN ANALYZE` is the manager comparing the reservation list (estimate) against the actual door count (actual) at the end of the night.

## 6. Real-World Analogy
**A taxi dispatcher estimating routes**: the driver asks "fastest way to the airport?" The dispatcher estimates traffic (histogram of typical delays), road closures (statistics freshness), and distance (cost per mile). The recommendation (plan) is the cheapest *estimated* route. If the traffic data is stale (roads changed since the last map update = statistics not analyzed), the chosen route is slow. A dispatcher who "just always takes the highway" (rule-based) is predictable but wrong when the highway is gridlocked. The dispatcher's only honest tool is: keep the map fresh, measure actual travel time (EXPLAIN ANALYZE), and re-route (ANALYZE / plan tuning).

## 7. Formal Definition
For a predicate P on column C with histogram buckets and `n_distinct` estimate, the **selectivity** s(P) is estimated as the fraction of tuples satisfying P (e.g., via histogram bucket fractions for ranges; via `most_common_values` frequencies for =). The **cardinality** of an operator is `selectivity × input cardinality`. A plan's **cost** is a weighted sum: `Σ (page accesses × page_cost) + Σ (tuples × cpu_tuple_cost) + index/function/sort overheads`, with configurable weights (`random_page_cost`, `seq_page_cost`, `cpu_tuple_cost`, `cpu_index_tuple_cost`, `cpu_operator_cost`). The optimizer chooses the plan minimizing total estimated cost; actual execution may differ (shown by `EXPLAIN ANALYZE`'s "actual rows/time").

## 8. Example
Table `orders` (10M rows). Query `SELECT * FROM orders WHERE status = 'paid' AND amount > 1000;`
- Stats: `status` has 4 values with frequencies; `amount` has a histogram; assume `status='paid'` → 25% (2.5M rows), `amount>1000` → 10%.
- Independent assumption → selectivity 0.25 × 0.10 = 0.025 → estimated 250K rows. (If `paid` orders are also high-amount, the true number may be 500K — the *correlation* error.)
- Indexes: `idx_status (status)` — a scan would return ~2.5M rows then filter → optimizer may prefer **Seq Scan** (a bitmap index scan's random I/O at 25% selectivity loses to a full scan). `idx_status_amount (status, amount)` — a covering composite index returns ~250K rows → optimizer picks **Index Scan**.
- Cost: seq scan ≈ 10M pages-ish reads + CPU over 10M rows; index scan ≈ index reads + 250K random page fetches. The crossover point (about 5-10% selectivity for a typical `random_page_cost=4` setup) decides.

## 9. Internal Working
1. `ANALYZE` samples rows (default `default_statistics_target`=100 buckets), computes per-column stats: null fraction, `n_distinct`, min/max, `most_common_values` (with frequencies), and histogram buckets.
2. `autovacuum` triggers `ANALYZE` based on `autovacuum_analyze_threshold`/`scale_factor` (default 0.05 → ~5% changed rows).
3. At plan time, the planner (a) gets base relations' cardinalities, (b) applies predicate selectivities (via histograms/MCVs), (c) computes join cardinalities (using `n_distinct` and join selectivity), (d) assembles operator trees, and (e) computes each node's cost bottom-up; the cheapest complete plan wins.
4. **Inaccuracy sources**: independent-predicate assumption, uniform distribution assumption (fixed by histograms), `LIMIT`/`OFFSET` estimation, correlation across columns (fixed by extended stats), and **staleness** (data changed since `ANALYZE`).
5. `EXPLAIN ANALYZE` runs the plan and prints estimated vs actual rows/time per node — the primary diagnostic loop: spot the mismatch, fix stats (ANALYZE), fix the query shape, or add indexes.

## 10. Time Complexity
- Collecting statistics: O(sample) per table at `ANALYZE`; autovacuum keeps it amortized.
- Selectivity lookups: O(1) per predicate (histogram binary search O(log buckets)).
- Plan-space search: exponential in joins in theory, pruned in practice (dynamic programming for ≤ ~12 relations).
- Cost computation per candidate: O(plan size).
- The *payoff*: a good estimate can make a plan 100-1000x faster than a bad one — estimation cost is trivial next to execution cost.

## 11. Advantages
- **Data-adaptive**: plans reflect the actual distribution (skew, distinctness) via histograms/MCVs — not rules.
- **Explainable & tunable**: cost weights are configurable; `EXPLAIN` makes choices transparent.
- **Diagnosable**: estimate-vs-actual comparison is the core debugging loop.
- **Cheap**: sampling-based stats are O(sample), not O(data).
- **Extensible**: extended statistics, `n_distinct` tuning, and custom cost settings cover real-world corner cases.

## 12. Disadvantages
- **Estimates can be wrong** — the #1 cause of slow queries (independent/ uniform/ staleness assumptions).
- **Statistics staleness** — without `ANALYZE`, plans drift as data grows (the classic "query was fast, now slow").
- **Skew and correlation** break the model — a histogram fixes single-column skew but not multi-column correlation (needs extended stats).
- **Cost model ≠ reality** — `random_page_cost` on SSDs differs; underestimated costs mis-rank plans.
- **Parameterized queries** — `$1` in a prepared statement hides the value from estimates (Postgres uses generic plans).

## 13. Interview Questions
1. **Q: What is cost-based optimization?** A: The optimizer assigns each candidate plan an *estimated cost* (weighted I/O + CPU using data statistics) and picks the minimum. It contrasts with rule-based optimization (heuristics without data).
2. **Q: What are cardinality and selectivity?** A: Cardinality = estimated rows output by an operator. Selectivity = the fraction of input rows a predicate keeps (e.g., `amount>1000` keeping 10% ⇒ selectivity 0.1). Cardinality = selectivity × input rows; cost estimates flow from it.
3. **Q: What statistics does the optimizer use?** A: Per-table (row count, page count), per-column (null fraction, `n_distinct`, min/max, most-common-values with frequencies, and a histogram of value distribution), plus extended stats for correlated columns. Collected by `ANALYZE`.
4. **Q: How does a histogram help the optimizer?** A: It estimates *range* predicate selectivity by computing the fraction of values in the relevant buckets — far more accurate than assuming a uniform distribution. (Uniform assumption on a skewed column is how estimates go wrong.)
5. **Q: TRICKY: Why is my EXPLAIN estimate 10x off from actual rows?** A: Likely: stale statistics (run `ANALYZE`), correlated columns treated as independent, skew in a column without MCVs, or a `LIMIT`/parameterized query hiding values. The fix path: `ANALYZE` → check extended stats need → inspect actual vs estimated per node.
6. **Q: What are the main cost weights and what do they model?** A: `seq_page_cost` (sequential page read), `random_page_cost` (random page read — historically 4x, ~1.1-1.5 on SSD), `cpu_tuple_cost`, `cpu_index_tuple_cost`, `cpu_operator_cost`. They encode "disk I/O dominates; random I/O is pricier than sequential."
7. **Q: How does the optimizer choose between a Seq Scan and an Index Scan?** A: It estimates rows returned (selectivity) and compares: index scan = log-depth index reads + per-row random fetches; seq scan = read whole table sequentially. High selectivity (few rows) → index; low selectivity (many rows) → seq. Crossover ≈ ~5-10% for typical settings.
8. **Q: What is `random_page_cost` and why does it matter on SSDs?** A: The assumed cost of a random page read relative to sequential. Historically 4.0 (spinning disks); on SSD, random reads are nearly free, so lowering it (1.1-1.5) makes the optimizer more index-happy — a classic SSD-tuning move.
9. **Q: What is a bitmap index scan?** A: A hybrid for predicates matching many rows across an index: build a bitmap of candidate heap pages (index scan), merge bitmaps for OR conditions, then fetch heap pages in order — less random I/O than many single-row fetches. Chosen for moderate-selectivity predicates.
10. **Q: TRICKY: What's the independence assumption and when does it fail?** A: Estimating `P(A AND B) = P(A)·P(B)`. Fails when columns correlate (e.g., `city='NYC'` and `population>10M`). Postgres extended statistics (`CREATE STATISTICS ... WITH (dependencies)`) fix it — a great "advanced" answer.
11. **Q: PR: A query was fast last week, slow today. What changed?** A: Data volume (row count, distribution) changed and statistics went stale, or a `VACUUM`/`ANALYZE` changed the plan. Diagnose with `EXPLAIN ANALYZE` (estimate vs actual), then `ANALYZE`, and consider extended stats or index changes.
12. **Q: What does `work_mem` have to do with estimates?** A: The optimizer *estimates* memory for sorts/hash joins; if a hash join's estimated size exceeds `work_mem`, it plans for a spill (slower); underestimating the build side also causes real spills. Raising `work_mem` (for the query/session) can make the optimizer pick an in-memory plan.
13. **Q: What is the difference between estimated and actual cost in `EXPLAIN ANALYZE`?** A: Estimated = optimizer's model (rows, cost). Actual = measured execution (time, actual rows). Big divergence = estimation failure; matching = healthy plan. Always compare rows first — time follows.
14. **Q: How do prepared statements affect estimates?** A: The optimizer must plan without concrete parameter values → generic estimates (uniform assumptions), possibly worse than custom plans. Postgres: first 5 executions use custom plans, then generic if stable (`plan_cache_mode` controls it). MySQL's optimizer has similar trade-offs.
15. **Q: PRODUCTION: How would you tune a data warehouse join that always spills?** A: Increase `work_mem` for that workload, ensure the smaller relation is the build side (hash join), refresh statistics, add a covering index, or rewrite as a more selective query. Measure before/after with `EXPLAIN ANALYZE`.

## 14. Follow-Up Questions
1. **Q: What are extended statistics and when do you create them?** A: `CREATE STATISTICS` on column sets adds `ndistinct` (multi-column distinct count), `dependencies` (functional dependence), and `mcv` (multi-column MCVs) — fixing independence and correlation estimation. Use when you *know* columns correlate and plans are wrong.
2. **Q: What is `n_distinct` and why does it matter?** A: The estimated number of distinct values per column — drives join cardinality (`|R ⋈ S| ≈ |R|·|S|/max(n_distinct_R, n_distinct_S)`). A wrong `n_distinct` (or NULL-inclusive counts) mis-estimates join sizes badly.
3. **Q: How does `LIMIT` interact with cost estimation?** A: A `LIMIT` can stop early (incremental sort / index ordering), but estimating how many rows to scan before hitting the limit is hard — plans may still sort the whole input. `OFFSET` is a hidden cost (rows must be skipped).

## 15. Coding Example
```sql
-- Inspect statistics: what the optimizer actually sees
SELECT relname, reltuples, relpages FROM pg_class WHERE relname='orders';
SELECT attname, n_distinct, null_frac, most_common_vals, histogram_bounds
  FROM pg_stats WHERE tablename='orders' AND attname IN ('status','amount');
```
```sql
-- Find estimate-vs-actual divergence (the diagnostic loop)
EXPLAIN ANALYZE
SELECT * FROM orders WHERE status='paid' AND amount > 1000;
-- Compare "rows" (estimate) vs "actual rows" per node.
-- If diverging: refresh stats or add extended stats.
ANALYZE orders;
CREATE STATISTICS orders_status_amount (dependencies, mcv) ON status, amount FROM orders;
```
```bash
# SSD tuning that changes the cost model
psql -c "ALTER SYSTEM SET random_page_cost = 1.1;"   # SSDs: random ≈ sequential
psql -c "SELECT pg_reload_conf();"
```
```pseudocode
// Selectivity via histogram (conceptual)
function range_selectivity(hist, low, high):
    frac = 0
    for bucket in buckets_overlapping(low, high):
        frac += overlap_fraction(bucket) / total_frequency
    return frac
```

## 16. Industry Usage
- **PostgreSQL**: `pg_stats`/`pg_class` stats, `ANALYZE`, extended statistics, `random_page_cost`, `work_mem`, `EXPLAIN` — the reference for "stats-driven" planning.
- **MySQL 8.0**: histogram support (8.0.3+), `ANALYZE TABLE`, cost constants in `mysql.engine_cost`/`server_cost` tables, index statistics from `SHOW INDEX`.
- **SQL Server**: auto-update statistics (thresholds), `UPDATE STATISTICS`, histogram inspection, `FORCESEEK`/`FORCESCAN` hints.
- **Oracle**: `DBMS_STATS.GATHER_TABLE_STATS`, histograms, `OPTIMIZER_*` parameters.
- **Snowflake/BigQuery/Redshift**: statistics from metadata + auto-analyze; columnar engines estimate bytes-scanned rather than pages — same ideas, different cost units.
- Any "query planner tuning" work is, at its core, this cost model.

## 17. References
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 14 (query optimization) — selectivity & cost estimation.
- Elmasri & Navathe, Ch. 19.
- PostgreSQL docs, "Planner/Optimizer": https://www.postgresql.org/docs/current/planner-optimizer.html, "Row Estimation Examples": https://www.postgresql.org/docs/current/row-estimation-examples.html, "Extended Statistics": https://www.postgresql.org/docs/current/functions-statistics.html
- MySQL 8.0 docs, "Cost-Based Optimizer": https://dev.mysql.com/doc/refman/8.0/en/cost-model.html
- Selinger et al., "Access Path Selection in a Relational Database Management System" (1979) — the original cost-based optimizer paper.

## 18. Cheat Sheet
- Cardinality = est. rows out; Selectivity = fraction kept by a predicate.
- Selectivity → cardinality → cost; cost = weighted I/O + CPU.
- Weights: `seq_page_cost`=1, `random_page_cost`=4 (lower on SSD), `cpu_tuple_cost` etc.
- Stats come from `ANALYZE`: rows/pages, `n_distinct`, null_frac, MCVs, histograms.
- Seq vs Index crossover ≈ 5-10% selectivity (typical).
- Bitmap scan = merge index hits, fetch pages in order (moderate selectivity).
- Failures: stale stats, independence assumption, correlation, uniform-skew, parameterized queries.
- Fixes: `ANALYZE`, extended statistics, `random_page_cost`, `work_mem`, index design.
- Diagnostic: `EXPLAIN ANALYZE` estimate-vs-actual, rows first.

## 19. Quiz
1. Selectivity of a predicate keeping 5% of rows: a) 0.05 b) 5 c) 0.5 d) 95 → **a**
2. Cardinality = a) rows in table b) selectivity × input rows c) cost d) pages → **b**
3. Which fix handles stale statistics? a) VACUUM b) ANALYZE c) REINDEX d) EXPLAIN → **b**
4. `random_page_cost` on SSD should usually be: a) raised b) lowered c) unchanged d) zero → **b**
5. The independence assumption fails on: a) uniform data b) correlated columns c) NULLs d) indexes → **b**
6. Index scan wins over seq scan when: a) selectivity high b) selectivity low c) table small always d) never → **a**
7. Which fixes correlated-column estimation? a) histograms b) extended statistics c) work_mem d) seq_page_cost → **b**
8. EXPLAIN ANALYZE "rows" vs "actual rows" mismatch means: a) bad index b) estimation error c) slow disk d) nothing → **b**

## 20. Flashcards
- **Q: What is selectivity?** → **A:** Fraction of rows a predicate keeps; drives cardinality → cost.
- **Q: What stats does the optimizer use?** → **A:** reltuples/pages, n_distinct, null_frac, MCVs, histograms (from ANALYZE).
- **Q: Seq vs Index scan decision?** → **A:** Estimated selectivity/cardinality vs scan costs; crossover ≈ 5-10%.
- **Q: Why is my estimate wrong?** → **A:** Stale stats, independence/correlation, skew, parameterized queries.
- **Q: How do you fix bad estimates?** → **A:** ANALYZE, extended statistics, cost-parameter tuning, indexes.
- **Q: What does random_page_cost model?** → **A:** Cost of random page reads relative to sequential (4.0 HDD, ~1.1 SSD).
- **Q: What is a bitmap index scan?** → **A:** Build a bitmap from index hits, fetch heap pages in order — for moderate selectivity.
- **Q: What is the diagnostic loop?** → **A:** EXPLAIN ANALYZE → compare estimated vs actual rows → fix stats/query/indexes.

## 21. Revision
Cost-based optimization: from `ANALYZE` stats (rows, n_distinct, MCVs, histograms), estimate selectivity → cardinality → cost (I/O + CPU weighted). Pick cheapest plan. Estimation failures (stale stats, correlation, skew, params) are the #1 cause of slow queries. Fixes: `ANALYZE`, extended statistics, `random_page_cost` (SSD), `work_mem`, indexes. Always verify with `EXPLAIN ANALYZE` estimate-vs-actual — rows first. This cost model is what selects the join algorithms of Section 02.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is cost-based optimization?" | 1, 2, 7 |
| "Cardinality vs selectivity?" | 2, 7, 13 |
| "What statistics does the optimizer use?" | 2, 9, 13 |
| "Why are my estimates wrong?" | 9, 13 |
| "Seq vs Index scan decision?" | 8, 13 |
| "What does random_page_cost do?" | 7, 13 |
| "What is the independence assumption?" | 4, 13 |
| "How do you fix a slow query?" | 9, 13, 16 |
