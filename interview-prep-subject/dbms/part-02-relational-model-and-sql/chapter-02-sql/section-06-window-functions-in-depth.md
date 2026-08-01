# Window Functions in Depth

> **TL;DR**: Window functions compute a value over a *sliding partition of related rows* — `OVER (PARTITION BY ... ORDER BY ...)` — without collapsing rows like GROUP BY, powering rankings, running totals, moving averages, and delta-from-previous analytics in one pass.

## 1. Why Does This Exist?
GROUP BY is lossy — it collapses rows into one summary per group, and you can't get "the rank of *this* row within its group" or "a running total that includes this row's value while keeping the row itself." Window functions exist precisely for that gap: compute an aggregate-like value **per row**, over a window of *neighboring* rows defined by partitioning and ordering — while keeping every original row in the result. They exist because the most common analytics (rankings, percentiles, running totals, period-over-period deltas, top-N per group) are fundamentally "per-row-with-context" computations that GROUP BY cannot express. Interviewers love them because they compress a huge class of problems into one clean clause.

## 2. How Does It Work?
Syntax: `function(...) OVER ( [PARTITION BY cols] [ORDER BY cols] [frame] )`.
- **PARTITION BY** — split rows into independent groups (like GROUP BY but *not* collapsing).
- **ORDER BY** — order rows within each partition; required for ranking/window-order functions.
- **frame** — `ROWS/RANGE BETWEEN ... AND ...` defines which rows are in each row's window (default: `RANGE UNBOUNDED PRECEDING TO CURRENT ROW`).
- **Classes**:
  - **Ranking**: `ROW_NUMBER()` (unique sequential), `RANK()` (gaps on ties), `DENSE_RANK()` (no gaps), `NTILE(n)` (buckets), `CUME_DIST`, `PERCENT_RANK`.
  - **Value**: `LAG(col, n)` / `LEAD(col, n)` — previous/next row (delta comparisons), `FIRST_VALUE`, `LAST_VALUE`, `NTH_VALUE`.
  - **Aggregates**: `SUM/AVG/COUNT/MIN/MAX` as window functions → running totals, moving averages.
  - **Distribution**: `PERCENTILE_CONT/DISC` (Postgres), `RATIO_TO_REPORT` (Oracle).
Window functions run *after* WHERE/GROUP BY/HAVING, *before* DISTINCT/ORDER BY — hence the legality rules below.

## 3. When Is It Used?
- **Top-N per group**: "top 3 salaries per department" (`ROW_NUMBER` + filter).
- **Rankings/percentiles**: leaderboards, percentile scores, `NTILE` quartiles.
- **Running totals & moving averages**: revenue-to-date, 7-day rolling MA.
- **Deltas**: LAG for MoM/QoQ growth, "change from previous month", session gaps.
- **Dedup**: `ROW_NUMBER() OVER (PARTITION BY key ORDER BY updated_at DESC) = 1` — the canonical dedup pattern.
- **Share of total**: `value / SUM(value) OVER (PARTITION BY ...)`.
- **Any analytics where the row must survive**: dashboards, cohort analysis, sessionization.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: GROUP BY + self-join.** Rejected: to get "rank within group" you'd join the table to an aggregated version — verbose, duplicates rows, and loses row context (you can't select non-grouped columns). Window functions are one clause.
- **Alternative: correlated subqueries.** Rejected: "count of rows before this one" is a per-row correlated subquery → O(n·m) unless rewritten; window functions are a single optimized pass.
- **Alternative: application code (sort + loop).** Rejected: ships all rows to the app and re-implements partitioning; the DB can do it in one parallelized pass.
- **Alternative: make GROUP BY preserve rows (like `GROUPING SETS` or lateral).** Rejected: semantics get muddy; keeping GROUP BY *collapsing* and adding *window functions* preserves both simple grouping and row-preserving analytics — a cleaner language design.
- **Why did SQL add this late (SQL:1999)?** Because ranking/percentile needs (reporting, data warehousing) grew large enough that engines (Oracle, DB2) pioneered the syntax, and the standard formalized it. Postgres added it in 8.4 (2009); MySQL only in 8.0 (2018) — a historical lag interviewers sometimes probe.

## 5. Intuition
Imagine **handing out medals after a race, while keeping every runner's row**. You don't delete runners — you add a "rank" column computed by ordering the runners (ORDER BY time) within their category (PARTITION BY gender). LAG/LEAD are "who finished just before/after me" (compare this lap to the last). SUM(...) OVER (ORDER BY date) is the "bank balance after each deposit" — running total; the balance at row 5 includes rows 1-5 but the row stays. GROUP BY would be "only the winner per category" (rows lost); a window function is "everyone + their category rank" (rows kept). The window is the "peek left/right within your partition" — nothing else in SQL does that.

## 6. Real-World Analogy
A **cricket scorecard**: the table shows every batsman's runs (rows kept). RANK OVER the whole innings = each batsman's position by runs. PARTITION BY team = rank within each team. LAG = "runs scored by the previous batsman" (compare partnerships). SUM OVER (ORDER BY innings) = the running total after each player — the scoreboard's progressive total, row by row. GROUP BY team would give only team totals (rows lost); the window version gives *both* each player's row *and* the team/global context beside it. That's the scorecard the TV shows — window functions are the scorecard, not the summary table.

## 7. Formal Definition
A window function f applied to a relation with window specification `OVER (PARTITION BY P ORDER BY O frame)` computes, for each tuple t, the value f over the **window frame** of t: the set of tuples in t's partition whose position satisfies the frame bounds relative to t (default `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`). Partitioning splits tuples into independent groups; ordering within partition defines frame positions (with ties in RANGE mode forming peer groups). Window functions are evaluated in the query pipeline **after** FROM/WHERE/GROUP BY/HAVING and **before** DISTINCT/ORDER BY/LIMIT — hence they can't appear in WHERE or GROUP BY, and a window-filter needs an outer query. Key functions: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `NTILE(n)`, `LAG(e, k)`, `LEAD(e, k)`, `FIRST_VALUE(e)`, `LAST_VALUE(e)`, and aggregate functions used as window functions. (ISO/IEC 9075-2:2016, "windowed functions"; Postgres docs.)

## 8. Example
```
sales: (region, month, amount)
(West,  Jan, 100),(West, Feb, 120),(West, Mar, 90)
(East,  Jan, 200),(East, Feb, 180),(East, Mar, 210)
```
- **ROW_NUMBER over all, ordered by amount DESC**: unique rank 1..6.
- **RANK / DENSE_RANK with a tie** (add West,Feb=120 duplicate): RANK: two rows get 2, next gets 4; DENSE_RANK: next gets 3. Gap vs no-gap.
- **Running total per region**: `SUM(amount) OVER (PARTITION BY region ORDER BY month)` → West: 100, 220, 310; East: 200, 380, 590.
- **Moving average (3-month frame)**: `AVG(amount) OVER (PARTITION BY region ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`.
- **MoM growth**: `amount - LAG(amount) OVER (PARTITION BY region ORDER BY month)` → West Feb: 20, Mar: -30.
- **Share of region total**: `amount * 100.0 / SUM(amount) OVER (PARTITION BY region)` → West Mar: 90/310 ≈ 29%.

## 9. Internal Working
1. **Pipeline position**: window functions execute after aggregation, before DISTINCT — the row set is final except dedup/sort.
2. **Partitioning**: rows are hashed/sorted by PARTITION BY into groups; within a partition, ORDER BY establishes the sequence (with NULLs first/last and peer handling in RANGE mode).
3. **Frame computation**: for each row, the engine slides the frame window (ROWS = physical offsets; RANGE = value-based peer groups) — implemented via sorted scans and running accumulators.
4. **Evaluation strategies**: engines use a single sort when possible; two sorts for partition+order; specialized accumulators for running aggregates (add left edge, remove right edge as the frame slides) → O(n) per partition.
5. **Filtering window results**: since window functions can't be in WHERE, a filter becomes `SELECT * FROM (SELECT ..., ROW_NUMBER() OVER (...) rn FROM t) x WHERE rn = 1` — the subquery materializes the window, then the outer filter applies.
6. **Dedup pattern**: `ROW_NUMBER() OVER (PARTITION BY key ORDER BY updated_at DESC) = 1` keeps the newest row per key — the #1 production use.

## 10. Time Complexity
- **Window function pass**: O(n log n) when sorting by partition+order keys; O(n) if rows already arrive sorted (index order); each window aggregate is O(n) amortized over sliding frames.
- **Memory**: window evaluation may buffer the partition (Postgres) — large partitions consume memory; spills for very large windows.
- **Multiple window functions with different ORDER BY**: multiple sorts — combine into shared windows to reuse.
- **Ranking**: ROW_NUMBER/RANK/DENSE_RANK all O(n log n) (sort) or O(n) (sorted input).
- **Vs GROUP BY**: window pass is comparable cost but keeps all rows (more output).

## 11. Advantages
- **Row-preserving**: keeps every row + adds context columns — no lossy collapse.
- **One-pass analytics**: running totals, ranks, deltas without self-joins or correlated subqueries.
- **Declarative**: the optimizer chooses sort/window strategy; parallelism applies.
- **Composable**: window functions combine with GROUP BY and CTEs; results feed outer queries.
- **Dedup & top-N**: the canonical patterns are one query, no temp tables.
- **Standardized**: SQL:1999+; available in Postgres, MySQL 8, Oracle, SQL Server, Snowflake, BigQuery.

## 12. Disadvantages
- **Not allowed in WHERE/GROUP BY/HAVING** — the #1 syntax error; filters need a subquery wrapper.
- **Frame semantics subtlety**: default frame is `RANGE` (peers), so LAST_VALUE needs an explicit frame — a classic "wrong answer that looks right".
- **Sort cost**: each distinct ORDER BY partition can cost a sort; over-indexed window use slows big queries.
- **Memory**: buffering partitions for LAG/LEAD/aggregates can blow `work_mem`.
- **Tie handling differences**: RANK vs DENSE_RANK vs ROW_NUMBER — wrong choice gives off-by-gap ranks.
- **MySQL lag**: window functions only from 8.0 (2018) — legacy systems lack them (correlated subqueries or variables).

## 13. Interview Questions
1. **Q: What is a window function?** A: A function computed over a window of related rows (PARTITION BY + ORDER BY + frame) that returns a value *per row* without collapsing rows — unlike GROUP BY. Powers rankings, running totals, and per-row context.
2. **Q: Window function vs GROUP BY?** A: GROUP BY collapses each group into one row (lossy). Window functions keep every row and attach a value computed over a partition (row-preserving). GROUP BY answers "what's the summary?", window answers "what's *this* row's context?"
3. **Q: What is PARTITION BY vs ORDER BY in a window?** A: PARTITION BY splits rows into independent groups (window scope); ORDER BY sequences rows within each partition (defines frame order + ranking). You can have PARTITION BY without ORDER BY (e.g., share-of-total) and ORDER BY without PARTITION (e.g., global running total).
4. **Q: Difference between ROW_NUMBER, RANK, DENSE_RANK?** A: ROW_NUMBER = unique sequential 1,2,3 (ties broken arbitrarily). RANK = ties share rank, next rank has gaps (1,2,2,4). DENSE_RANK = ties share rank, no gaps (1,2,2,3). Pick by business semantics.
5. **Q (production): Write "top 3 salaries per department".** A: `SELECT dept, name, salary FROM (SELECT e.*, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) rn FROM emp e) t WHERE rn <= 3;` — window then outer filter (can't put rn in WHERE directly).
6. **Q: What does LAG / LEAD do?** A: LAG(col, n) = the value n rows *before* the current row (per partition/order); LEAD = n rows after. Used for MoM/QoQ deltas: `amount - LAG(amount) OVER (... ORDER BY month)`. NULL on missing rows (guard with COALESCE or IGNORE NULLS in Postgres 14+).
7. **Q (scenario): Month-over-month revenue growth per region.** A: `SELECT region, month, amount, amount - LAG(amount) OVER (PARTITION BY region ORDER BY month) AS mom_delta, round((amount - LAG(amount) OVER (PARTITION BY region ORDER BY month))*100.0/LAG(amount) OVER (PARTITION BY region ORDER BY month), 2) AS mom_pct FROM sales;` — name the NULL on January (no prior) and the COALESCE/LAG handling.
8. **Q: What is the default frame?** A: `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` — "everything up to and including the current row, with peers". For running totals this is right; for LAST_VALUE or precise windows you must specify an explicit `ROWS` frame.
9. **Q (tricky): Why does LAST_VALUE sometimes return the current row's value unexpectedly?** A: The default frame ends at CURRENT ROW, so LAST_VALUE only sees rows up to the current row — it returns the current value unless you set `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`. Classic "correct-looking, wrong-answer" bug.
10. **Q: Where can't window functions appear?** A: In WHERE, GROUP BY, HAVING (they're evaluated after those stages) — also not directly in aggregate arguments. You can use them in SELECT and ORDER BY; to filter on them, wrap in a subquery/CTE.
11. **Q (production): Deduplicate a table keeping the newest row per key.** A: `WITH ranked AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC) rn FROM events) DELETE FROM events WHERE (user_id, updated_at) IN (SELECT user_id, updated_at FROM ranked WHERE rn > 1);` (or a CTE+join). The single most common window-function production pattern.
12. **Q: What is NTILE?** A: `NTILE(n)` divides each partition into n roughly-equal buckets and returns the bucket number — for quartiles/deciles and cohort bucketing. `NTILE(4)` → 1-4.
13. **Q (scenario): Running total of sales by region.** A: `SELECT region, month, amount, SUM(amount) OVER (PARTITION BY region ORDER BY month) AS running_total FROM sales;` — each row gets cumulative sum up to it.
14. **Q: What is a moving average and how do you frame it?** A: `AVG(amount) OVER (PARTITION BY region ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` — 3-row trailing average. Explicit ROWS frame for window arithmetic.
15. **Q: Can you combine window functions with GROUP BY?** A: Yes — aggregate first (GROUP BY), then window over the aggregated result (e.g., percent of grand total: `SUM(amount)/SUM(SUM(amount)) OVER ()`). The window sees the post-aggregation rows.
16. **Q (tricky): What is the difference between a window aggregate and a GROUP BY aggregate with the same SUM?** A: The GROUP BY version produces one row per group (lossy); the window version repeats the group total on *every* row of the group (row-preserving) — same number, different shape. Choose by whether you keep rows.
17. **Q: How do window functions perform?** A: Sorting dominates — O(n log n) per distinct PARTITION/ORDER combination; memory buffers the partition. With an index matching the partition+order, no sort is needed (O(n)). Multiple window functions with different orderings = multiple sorts.
18. **Q (production): Why is a big `ROW_NUMBER` dedup slow on a 100M-row table?** A: Full sort of the partition keys (O(n log n)) + memory for large partitions. Optimize: index on (partition_key, order_key), reduce scanned columns, or use incremental/streaming dedup. Always check `EXPLAIN` for the Sort node.
19. **Q: What does `PERCENT_RANK` / `CUME_DIST` do?** A: Percentile-style ranks: PERCENT_RANK = (rank-1)/(n-1) within partition; CUME_DIST = fraction of rows <= current. Used for relative-position analytics (what percentile is this sale?).
20. **Q (hard): Explain the three-part window clause interaction with RANGE vs ROWS.** A: ROWS frames count *physical* rows (offsets); RANGE frames group *peer* rows with equal ORDER BY values (includes all peers at the boundary). With ties, RANGE can pull in extra rows the ROWS frame wouldn't — a subtle difference that changes running totals when ORDER BY values repeat.

## 14. Follow-Up Questions
1. **Q: When would you pick RANK over ROW_NUMBER for top-N?** A: When ties must all appear (give all 2nd-place medalists rank 2, and then a gap) — ROW_NUMBER breaks ties arbitrarily and gives one row per slot.
2. **Q: How do you get the previous *non-null* value?** A: Postgres 14+: `LAG(col IGNORE NULLS)`; older engines: a lateral self-join or a filtered frame — an interview-adjacent edge case.
3. **Q: Can window functions use indexes to avoid sorting?** A: Yes — an index on (partition, order) provides rows already in window order, so the planner skips the Sort node; that's the main window-function optimization.
4. **Q: What is `EXCLUDE` in frames (SQL:2011)?** A: Frame exclusion clauses (`EXCLUDE CURRENT ROW`, `EXCLUDE TIES`) refine the window contents — used for "sum of all others" and peer-aware analytics.
5. **Q: Window functions in streaming (Flink)?** A: Flink/Kafka Streams implement windowed aggregation natively (tumbling/sliding windows) — the streaming analog; the SQL `OVER` syntax is partly supported for special windows. Conceptual continuity, not full parity.

## 15. Coding Example
```sql
-- Setup
CREATE TABLE sales (region TEXT, month TEXT, amount INT);
INSERT INTO sales VALUES
 ('West','Jan',100),('West','Feb',120),('West','Mar',90),
 ('East','Jan',200),('East','Feb',180),('East','Mar',210);

-- Rankings
SELECT region, month, amount,
       ROW_NUMBER() OVER (ORDER BY amount DESC) AS row_num,
       RANK()        OVER (ORDER BY amount DESC) AS rnk,
       DENSE_RANK()  OVER (ORDER BY amount DESC) AS dense_rnk,
       NTILE(2)      OVER (ORDER BY amount DESC) AS half
FROM sales;

-- Running total + moving avg + delta (per region)
SELECT region, month, amount,
       SUM(amount) OVER (PARTITION BY region ORDER BY month)          AS running_total,
       AVG(amount) OVER (PARTITION BY region ORDER BY month
                         ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)   AS ma3,
       amount - LAG(amount) OVER (PARTITION BY region ORDER BY month) AS mom_delta
FROM sales;

-- Top 2 sales per region (window + outer filter)
SELECT region, month, amount FROM (
  SELECT s.*, ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC) rn
  FROM sales s
) t WHERE rn <= 2;

-- Dedup (keep newest per user)
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC) rn
  FROM events
)
DELETE FROM events WHERE (user_id, updated_at) IN (SELECT user_id, updated_at FROM ranked WHERE rn > 1);
```

## 16. Industry Usage
- **dbt/analytics engineering** uses window functions in every second model: dedup with `ROW_NUMBER`, `LAG` for growth, running totals for funnel analytics.
- **Snowflake/BigQuery/Redshift** optimize window functions with massive parallelism; window queries are core to their dashboard workloads.
- **Amazon/Google/Meta SQL screens** literally ask for "top-3 per group" and "running total" — the two canonical window questions — because they test both syntax and pipeline semantics.
- **Sessionization**: `LAG(timestamp)` to compute session gaps, then `SUM(CASE WHEN gap>30min THEN 1 END) OVER (...)` to number sessions — a window-only technique.
- **Feature engineering for ML**: window features (rolling averages, delta, percentile ranks) are computed exactly this way on feature pipelines (Vertex AI, SageMaker feature stores).

## 17. References
- PostgreSQL Documentation, Window Functions: https://www.postgresql.org/docs/current/functions-window.html
- PostgreSQL Documentation, Window Function Processing: https://www.postgresql.org/docs/current/queries-window.html
- MySQL Reference Manual, Window Functions: https://dev.mysql.com/doc/refman/8.0/en/window-functions.html
- ISO/IEC 9075-2:2016 (SQL — windowed table functions).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 4 (Window functions).

## 18. Cheat Sheet
- `f() OVER (PARTITION BY p ORDER BY o frame)` — per-row, row-preserving.
- ROW_NUMBER unique; RANK gaps on ties; DENSE_RANK no gaps.
- Default frame: `RANGE UNBOUNDED PRECEDING TO CURRENT ROW` (peers!).
- LAST_VALUE needs explicit frame (`ROWS ... UNBOUNDED FOLLOWING`).
- LAG/LEAD for deltas; NULL on missing — guard/IGNORE NULLS.
- Illegal in WHERE/GROUP BY/HAVING — wrap in subquery.
- Top-N: ROW_NUMBER + outer `WHERE rn <= k`.
- Dedup: `ROW_NUMBER() OVER (PARTITION BY key ORDER BY updated_at DESC) = 1`.

## 19. Quiz
1. Window functions: a) collapse rows b) keep every row c) create tables d) sort only → **b**
2. `PARTITION BY` does: a) global sort b) splits rows into groups c) dedup d) index → **b**
3. RANK with 2 ties at rank 2, next rank is: a) 3 b) 4 c) 2 d) 5 → **b**
4. DENSE_RANK with 2 ties at 2, next rank: a) 3 b) 4 c) 1 d) 2 → **a**
5. Default frame ends at: a) UNBOUNDED FOLLOWING b) CURRENT ROW c) 2 PRECEDING d) first row → **b**
6. Window functions can appear in: a) WHERE b) SELECT/ORDER BY c) GROUP BY d) HAVING → **b**
7. MoM growth uses: a) LAG b) NTILE c) CUME_DIST d) ROW_NUMBER → **a**
8. `NTILE(4)` produces: a) ranks b) quartile buckets c) deltas d) totals → **b**
9. Dedup newest-per-key uses: a) RANK b) ROW_NUMBER + rn=1 c) SUM d) LEAD → **b**
10. Top-3 per group needs: a) GROUP BY b) window + outer filter c) DISTINCT d) CROSS JOIN → **b**

## 20. Flashcards
- **Q: Window function vs GROUP BY?** → **A:** GROUP BY collapses rows; windows keep rows + add context.
- **Q: ROW_NUMBER vs RANK vs DENSE_RANK?** → **A:** Unique / gaps on ties / no gaps.
- **Q: What is PARTITION BY?** → **A:** Independent row groups within which the window computes.
- **Q: Default frame?** → **A:** RANGE UNBOUNDED PRECEDING TO CURRENT ROW (includes peers).
- **Q: LAG/LEAD?** → **A:** Previous/next row value (per partition+order) — deltas.
- **Q: Where are windows illegal?** → **A:** WHERE, GROUP BY, HAVING — wrap in a subquery.
- **Q: Top-N per group?** → **A:** ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ... DESC) ≤ k.
- **Q: Dedup pattern?** → **A:** ROW_NUMBER over (key, updated_at DESC) = 1.

## 21. Revision
Window functions: `f() OVER (PARTITION BY p ORDER BY o frame)` — per-row, row-preserving analytics after WHERE/GROUP BY. Ranking: ROW_NUMBER (unique), RANK (gaps), DENSE_RANK (no gaps); NTILE for buckets. Value: LAG/LEAD (deltas), FIRST/LAST_VALUE (LAST needs explicit frame!). Aggregates as windows: running totals, moving averages (`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`). Illegal in WHERE/GROUP BY/HAVING → subquery wrapper. Top-N: ROW_NUMBER + outer `rn <= k`. Dedup: ROW_NUMBER over (key, updated_at DESC) = 1. Cost: O(n log n) sort unless index matches. Interview moves: recite the two canonical patterns (top-N, running total); explain the default-frame LAST_VALUE bug; and always state where windows are illegal.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Window vs GROUP BY?" | 13 Q2 |
| "ROW_NUMBER vs RANK vs DENSE_RANK?" | 13 Q4 |
| "Top-3 per dept?" | 13 Q5 |
| "LAG/LEAD for MoM growth?" | 13 Q7 |
| "Default frame / LAST_VALUE bug?" | 13 Q9 |
| "Where illegal?" | 13 Q10 |
| "Dedup pattern?" | 13 Q11 |
| "Running total / moving average?" | 13 Q13-14 |
