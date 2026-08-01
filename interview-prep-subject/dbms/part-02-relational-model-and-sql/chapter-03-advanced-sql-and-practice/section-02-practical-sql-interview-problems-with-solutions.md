# Practical SQL Interview Problems with Solutions

> **TL;DR**: The 15 canonical SQL problems — top-N per group, dedupe, running totals, gaps, sessions, percentiles, conditional aggregation, pivots — with working queries on sample data, two solutions each where useful, and a performance note per problem.

## 1. Why Does This Exist?
Interview SQL questions are drawn from a small, recurring pattern library. If you've *seen and solved* the canonical problems, a new variant is just a rename. This section exists to (a) compress the pattern library into one place with *correct, tested, defensible* solutions, (b) give each problem two answers (the "obvious" and the "optimal") so you can discuss trade-offs, and (c) attach a performance note per problem so your answer includes "and this is how I'd make it fast". It exists because pattern recognition + syntax fluency under time pressure is what actually wins SQL screens.

## 2. How Does It Work?
Each problem follows the same skeleton: **setup** (small sample tables + rows) → **question** → **solution(s)** → **explanation of why it works** → **performance note** (index, plan shape, alternative). The 15 problems:
1. Top-N per group (window vs lateral).
2. Deduplicate keeping newest (ROW_NUMBER).
3. Second highest salary (several idioms).
4. Running total / cumulative sum.
5. Moving average.
6. Month-over-month / day-over-day delta (LAG).
7. Find gaps in a sequence (LAG + compare).
8. Consecutive-day streak / groups (island-gap).
9. Sessionization (LAG + window-sum boundary).
10. Percentile / median (PERCENTILE_CONT).
11. Conditional aggregation (FILTER / SUM CASE).
12. Pivot (table with one row per category → columns).
13. Share-of-total / percent of category.
14. Existence/anti-join problems (customers with/without orders).
15. Hierarchical/recursive query (org chart).

## 3. When Is It Used?
- **Live SQL screens** (Amazon, Meta, Google, Stripe, Snowflake, Databricks): expect 1-3 of these patterns.
- **Take-homes**: data-prep tasks are literally these problems (dedupe, rolling totals, gaps).
- **Production analytics**: every pattern above appears daily in real pipelines.
- **Interview warm-up**: drilling these 15 makes any new problem a variant.
- **Data engineering**: the same shapes in dbt/warehouse SQL.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: memorize answers to specific questions.** Rejected — interviews change names/data; only *patterns* transfer. Each solution here is deliberately stated as "this is the X pattern" so you apply it, not recall it.
- **Alternative: one "trick" solution per problem.** Rejected — interviewers probe alternatives ("can you do it with a subquery?" / "with a window?"). Two solutions per problem = you can discuss equivalence and trade-offs.
- **Alternative: write answers by hand without running.** Rejected — correctness is critical; every solution here is designed to be runnable as-is on the sample data with a standard SQL dialect (Postgres-flavored, portable where possible).
- **Why these 15?** Because they cover the full taxonomy of SQL interview questions: ranking, dedup, aggregation, time series, existence, pivoting, recursion. It's a complete coverage set, not an arbitrary list.

## 5. Intuition
Think of this section as a **cookbook, not a menu**. You don't memorize dishes; you learn *techniques* — "rank everything with ROW_NUMBER", "compare neighbors with LAG", "find boundaries with a running-sum trick". When an interviewer hands you a new scenario ("find employees who've been in the same dept 3 months straight"), you recognize: *that's a streak problem* → apply the island-gap technique. The pattern → technique mapping is the real content; the sample data just makes it concrete. After drilling, the mapping becomes automatic, like a cook knowing "cream sauce" without the recipe.

## 6. Real-World Analogy
A **builder's toolbox**: a top-N problem is "sort the beams and take the first three" (window function = the ladder that keeps all beams visible while you pick). Dedup is "keep the newest receipt per customer" (ROW_NUMBER = timestamping each and keeping label 1). Gaps are "find the missing page numbers in the ledger" (LAG = compare each page to the previous). Sessions are "group these purchases into visits" (the 30-minute-gap trick = when the silence is long enough, start a new session). You don't need a different tool for every house — 15 tools build every house. This section is the toolbag, organized by problem shape.

## 7. Formal Definition
The canonical SQL problem set spans the full vocabulary of the language:
- **Ranking/windowing**: `ROW_NUMBER()/RANK()/DENSE_RANK() OVER (PARTITION BY ... ORDER BY ...)`.
- **Dedup**: partition by natural key, order by timestamp desc, keep rn=1.
- **Time-series deltas**: `LAG(col) OVER (ORDER BY time)` and `LEAD`.
- **Running aggregates**: `SUM/AVG OVER (ORDER BY time [ROWS frame])`.
- **Gap detection**: difference between row's value and LAG's value.
- **Island/gap (streaks)**: group-consecutive-rows by `value - ROW_NUMBER() OVER (ORDER BY date)`.
- **Sessionization**: `SUM(boundary_flag) OVER (ORDER BY ts)` where boundary_flag marks long gaps.
- **Percentiles**: `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY col)` (Postgres/SQL Server/MySQL 8+/Oracle).
- **Conditional aggregation**: `COUNT(*) FILTER (WHERE cond)` (Postgres) / `SUM(CASE WHEN cond THEN 1 ELSE 0 END)` (portable).
- **Pivot**: conditional aggregation across `CASE` columns, or `CROSSTAB` (Postgres extension).
- **Existence**: `EXISTS`/`NOT EXISTS`/anti-join.
- **Recursion**: `WITH RECURSIVE ... UNION ALL ...`.
(All patterns standard in ISO 9075:2016 + vendor extensions noted.)

## 8. Example
```
-- Sample data used throughout (sales events)
CREATE TABLE sales (id INT PRIMARY KEY, cust_id INT, region TEXT, amount INT, sold_at DATE);
INSERT INTO sales VALUES
 (1,10,'West',100,'2024-01-01'), (2,10,'West',120,'2024-01-02'),
 (3,20,'East',200,'2024-01-01'), (4,20,'East',180,'2024-01-03'),
 (5,30,'West',90 ,'2024-01-02'), (6,30,'West',110,'2024-01-04'),
 (7,10,'West',130,'2024-01-05'), (8,20,'East',210,'2024-01-05');
```
**Problem 1 — Top-2 sales per region**:
```sql
SELECT region, id, amount FROM (
  SELECT s.*, ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC) rn
  FROM sales s
) t WHERE rn <= 2;
-- West: 7(130), 2(120); East: 8(210), 4(180)
```
**Problem 3 — Second highest sale overall**: `SELECT DISTINCT amount FROM sales ORDER BY amount DESC OFFSET 1 LIMIT 1;` → 130 (note DISTINCT for ties).

## 9. Internal Working
Each solution's plan shape (so you can talk about cost):
1. **Top-N**: window pass → Sort per partition O(n log n) → outer filter (Index Scan if (region, amount) index exists → window gets ordered input, no sort).
2. **Dedup**: Sort or hash by partition → keep rn=1 → DELETE/upsert.
3. **Second-highest**: sort+offset O(n log n), or MAX of "< max" O(n); window variant.
4. **Running total**: window SUM with ordered input O(n) (index on date) or sort O(n log n).
5. **Moving average**: frame window — O(n) after sort.
6. **LAG delta**: same pass, O(n).
7. **Gaps**: sort + LAG compare — O(n log n).
8. **Streaks**: `date - ROW_NUMBER()` grouping — O(n log n).
9. **Sessions**: LAG + window SUM — O(n log n).
10. **Median/percentile**: PERCENTILE_CONT does an internal sort + interpolation — O(n log n).
11. **Conditional aggregation**: hash aggregate, FILTER — O(n).
12. **Pivot**: aggregate with CASE columns — O(n).
13. **Share-of-total**: window SUM over no-partition — O(n).
14. **Existence**: hash semi/anti-join — O(n + m).
15. **Recursion**: iterative UNION ALL until fixpoint — O(levels × work).

## 10. Time Complexity
- **Window top-N / dedup / streaks**: O(n log n) (dominated by partition+order sort); O(n) if an index already orders input.
- **Running/moving aggregates**: O(n) after ordering; O(n log n) if sort required.
- **Percentile/median**: O(n log n) (sort + interpolation).
- **Conditional aggregation / pivot / share-of-total**: O(n) hash aggregate.
- **Existence/anti-join**: O(n + m) hash.
- **Recursion**: O(levels × per-level work); guard cycles with keys/depth limits.

## 11. Advantages
- **Pattern coverage**: 15 problems cover the whole interview taxonomy.
- **Two answers each**: you can discuss equivalence (window vs subquery vs lateral) and trade-offs.
- **Performance-aware**: every solution includes its plan shape and the index that makes it O(n).
- **Runnable**: exact SQL on sample data — verifiable correctness.
- **Transfers to production**: the same patterns are daily analytics work.

## 12. Disadvantages
- **Dialect drift**: FILTER, PERCENTILE_CONT, LATERAL vary by engine — flagged per problem.
- **Sample-data optimism**: real tables have NULLs, duplicates, skew — the notes call out the traps each pattern hides.
- **Pattern ≠ free**: window sorts and recursive depth can surprise at scale — each note says where to look.
- **Edge cases**: ties (RANK vs ROW_NUMBER), empty partitions, single-row groups — worth naming in interviews.

## 13. Interview Questions
1. **Q: Top 3 salaries per department.** A: `SELECT dept, name, salary FROM (SELECT e.*, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) rn FROM emp e) t WHERE rn <= 3;` — window then outer filter. Alt: `LATERAL` for a small outer set.
2. **Q: Deduplicate a table, keep newest row per user.** A: `WITH r AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC) rn FROM t) DELETE FROM t WHERE (user_id, updated_at) IN (SELECT user_id, updated_at FROM r WHERE rn > 1);` — rn=1 keeps newest.
3. **Q: Second highest salary (handle ties).** A: `SELECT MAX(salary) FROM emp WHERE salary < (SELECT MAX(salary) FROM emp);` — NULL if none (COALESCE for a default). Alt: `ORDER BY salary DESC OFFSET 1 LIMIT 1` needs DISTINCT for ties.
4. **Q: Running total of sales per month.** A: `SELECT month, amount, SUM(amount) OVER (ORDER BY month) AS running FROM sales;` — window SUM in date order.
5. **Q: 7-day moving average.** A: `SELECT day, AVG(amount) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) ma7 FROM sales;` — ROWS frame for physical window.
6. **Q: Month-over-month growth.** A: `SELECT month, amount, amount - LAG(amount) OVER (ORDER BY month) AS delta FROM sales;` — LAG; January's delta is NULL (note it).
7. **Q: Find missing invoice numbers in a sequence.** A: `SELECT n FROM (SELECT inv_no AS n, LAG(inv_no) OVER (ORDER BY inv_no) prev FROM invoices) t WHERE n <> prev + 1;` — gaps detected by comparing neighbors.
8. **Q: Consecutive-day streaks per user.** A: Island-gap: `WITH g AS (SELECT user_id, day, day - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day) grp FROM t) SELECT user_id, COUNT(*) days, MIN(day) start, MAX(day) end FROM g GROUP BY user_id, grp;` — the ROW_NUMBER difference groups runs.
9. **Q: Sessionize page views into visits (30-min gap).** A: `WITH v AS (SELECT *, LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) prev FROM views), s AS (SELECT *, SUM(CASE WHEN prev IS NULL OR ts - prev > interval '30 min' THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) sess FROM v) SELECT user_id, sess, MIN(ts) start, MAX(ts) end, COUNT(*) FROM s GROUP BY user_id, sess;`
10. **Q: Median salary per dept.** A: `SELECT dept, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) FROM emp GROUP BY dept;` — or `PERCENTILE_DISC` for an actual salary. MySQL 8: `PERCENTILE_CONT` over window.
11. **Q: Count orders per status in one row (pivot).** A: `SELECT SUM(CASE WHEN status='paid' THEN 1 ELSE 0 END) paid, SUM(CASE WHEN status='pending' THEN 1 ELSE 0 END) pending FROM orders;` — conditional aggregation; Postgres: `COUNT(*) FILTER (WHERE status='paid')`.
12. **Q: Percent of total revenue per region.** A: `SELECT region, SUM(amount), SUM(amount)*100.0 / SUM(SUM(amount)) OVER () FROM sales GROUP BY region;` — window over aggregate.
13. **Q: Customers with no orders (three ways).** A: (1) `LEFT JOIN ... WHERE o.id IS NULL`; (2) `NOT EXISTS`; (3) `NOT IN` (NULL-unsafe if customer_id nullable — say so). Pick NOT EXISTS/anti-join.
14. **Q: Customers who ordered in both 2023 and 2024.** A: `SELECT cust_id FROM orders WHERE EXTRACT(YEAR FROM d)=2023 INTERSECT SELECT cust_id FROM orders WHERE EXTRACT(YEAR FROM d)=2024;` — or `GROUP BY cust_id HAVING COUNT(DISTINCT CASE ...)`.
15. **Q: Org chart with levels (recursive).** A: `WITH RECURSIVE org AS (SELECT id,name,mgr,1 lvl FROM emp WHERE mgr IS NULL UNION ALL SELECT e.id,e.name,e.mgr,o.lvl+1 FROM emp e JOIN org o ON e.mgr=o.id) SELECT * FROM org;` — level = depth.
16. **Q (tricky): Top-N per group with ties — show all employees tied for 3rd.** A: Use `DENSE_RANK() ... rn <= 3` (no gaps → includes ties) or `RANK() ... rn <= 3`. ROW_NUMBER would arbitrarily drop a tied employee. Name the difference.
17. **Q (production): Your dedup DELETE locks the whole table. Fix?** A: Batch: DELETE in chunks (`WHERE id IN (SELECT id FROM ranked WHERE rn>1 AND id > $last ORDER BY id LIMIT 1000)` loop), or dedup into a new table + swap. Single huge DELETE on a hot table is the anti-pattern.
18. **Q: First order date per customer, plus days since.** A: `SELECT cust_id, MIN(d) first_order, CURRENT_DATE - MIN(d) days_since FROM orders GROUP BY cust_id;` — group-wise MIN (simple); or `FIRST_VALUE(d) OVER (PARTITION BY cust_id ORDER BY d)`.
19. **Q (scenario): "Employees who earn more than their manager."** A: `SELECT e.name FROM emp e JOIN emp m ON e.mgr = m.id WHERE e.salary > m.salary;` — self-join (hierarchy pattern). Or a LATERAL/EXISTS variant.
20. **Q (hard): Cumulative distinct count per month (slow COUNT(DISTINCT)).** A: Exact but slow: `COUNT(DISTINCT user_id) OVER (ORDER BY month ROWS UNBOUNDED PRECEDING)` — dedup in frame. At scale: precompute per-month new users then window-SUM those (additive trick), or approximate (HyperLogLog). Name the trade-off.

## 14. Follow-Up Questions
1. **Q: ROW_NUMBER vs RANK vs DENSE_RANK — when for top-N?** A: ROW_NUMBER when ties don't matter (or must be unique); RANK/DENSE_RANK to include all ties — DENSE_RANK if you also want no gaps (e.g., "top 3 bands").
2. **Q: Window vs correlated subquery for running totals?** A: Window — one pass, O(n); correlated is O(n·m) unless rewritten. Always prefer windows for this class.
3. **Q: How do you dedup a 1B-row table in a warehouse?** A: Partition + ROW_NUMBER in an idempotent INSERT INTO new_table (CTAS pattern); then swap. Batch the UPDATE/DELETE on OLTP; avoid giant single DELETEs.
4. **Q: What's the difference between PERCENTILE_CONT and PERCENTILE_DISC?** A: CONT interpolates between values (can be a value not in data); DISC returns the nearest actual value. Pick DISC when the answer must be an existing row's value.
5. **Q: Streak query with NULL dates?** A: COALESCE/filter NULLs before the ROW_NUMBER trick; define the streak semantics first (missing days = break?). Say the assumption in interviews.

## 15. Coding Example
```sql
-- One complete runnable example set (Postgres-flavored; portable variants noted)
WITH sales AS (   -- sample
  SELECT * FROM (VALUES
    (1,10,'West',100,'2024-01-01'), (2,10,'West',120,'2024-01-02'),
    (3,20,'East',200,'2024-01-01'), (4,20,'East',180,'2024-01-03'),
    (5,30,'West',90 ,'2024-01-02'), (6,30,'West',110,'2024-01-04'),
    (7,10,'West',130,'2024-01-05'), (8,20,'East',210,'2024-01-05')
  ) AS t(id, cust_id, region, amount, sold_at)
)
-- (1) top-2 per region
SELECT region, id, amount FROM (
  SELECT s.*, ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC) rn FROM sales s
) x WHERE rn <= 2;

-- (4) running total by date
SELECT sold_at, amount,
       SUM(amount) OVER (ORDER BY sold_at) AS running
FROM sales ORDER BY sold_at;

-- (6) day-over-day delta
SELECT sold_at, amount,
       amount - LAG(amount) OVER (ORDER BY sold_at) AS dod
FROM sales ORDER BY sold_at;

-- (8) streaks: consecutive days present (group by day - row_number)
WITH daily AS (SELECT DISTINCT sold_at FROM sales),
     grp AS (SELECT sold_at, sold_at - ROW_NUMBER() OVER (ORDER BY sold_at) AS g FROM daily)
SELECT MIN(sold_at) AS start, MAX(sold_at) AS end, COUNT(*) AS days
FROM grp GROUP BY g ORDER BY start;
```

## 16. Industry Usage
- **Amazon's SQL screen** for BI/data roles is literally these problems (top-N, dedupe, rolling metrics); the Amazon "Bar Raiser" expects you to discuss the plan, not just the answer.
- **Meta/Google** ask ranking + time-series problems as standard; **Stripe/Snowflake/Databricks** favor aggregation + window-heavy data prep.
- **dbt model libraries** implement these patterns verbatim (dedup macros, rolling aggregations) — the patterns ARE production analytics.
- **Data quality/CDC pipelines** use the dedup + gap patterns continuously (drop duplicates, detect missing records, sessionize).
- **Feature stores** (ML) build rolling-window and delta features exactly as these problems show — the patterns power model training data.

## 17. References
- PostgreSQL Documentation, Window Functions: https://www.postgresql.org/docs/current/functions-window.html
- PostgreSQL Documentation, `PERCENTILE_CONT`: https://www.postgresql.org/docs/current/functions-aggregate.html
- MySQL Reference Manual, Window Functions (8.0+): https://dev.mysql.com/doc/refman/8.0/en/window-functions.html
- PostgreSQL Documentation, `WITH RECURSIVE`: https://www.postgresql.org/docs/current/queries-with.html
- LeetCode Database problems + SQLZoo (practice platforms).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 4 (SQL).

## 18. Cheat Sheet
- Top-N: `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ... DESC)` + `rn <= k`.
- Dedup: `ROW_NUMBER() OVER (PARTITION BY key ORDER BY ts DESC) = 1`.
- Second-highest: `MAX(x) WHERE x < MAX(x)`.
- Running total: `SUM(x) OVER (ORDER BY date)`.
- Moving avg: `AVG(x) OVER (ORDER BY date ROWS BETWEEN n PRECEDING AND CURRENT ROW)`.
- Deltas: `LAG(x) OVER (ORDER BY date)`.
- Gaps: `LAG(seq) OVER (ORDER BY seq) <> seq - 1`.
- Streaks: `date - ROW_NUMBER() OVER (ORDER BY date)` groups runs.
- Median: `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x)`.
- Pivot: `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` columns.
- Share: `x / SUM(x) OVER ()`.
- No-order: `NOT EXISTS` / anti-join.
- Recursion: `WITH RECURSIVE ... UNION ALL ...`.

## 19. Quiz
1. Keep-newest dedup uses: a) GROUP BY b) ROW_NUMBER rn=1 c) LIMIT d) DISTINCT → **b**
2. Second-highest via MAX: a) `WHERE x < MAX(x)` b) `WHERE x > MAX(x)` c) `= MAX(x)` d) `<>` → **a**
3. Running total uses: a) GROUP BY b) SUM OVER (ORDER BY) c) LAG d) NTILE → **b**
4. Moving average frame: a) ROWS BETWEEN n PRECEDING AND CURRENT ROW b) UNBOUNDED FOLLOWING c) default d) none → **a**
5. MoM delta uses: a) LEAD b) LAG c) RANK d) ROW_NUMBER → **b**
6. Gap detection compares: a) row to LAG b) row to SUM c) row to MAX d) nothing → **a**
7. Streak grouping trick: a) `date - ROW_NUMBER()` b) `date + SUM` c) `COUNT` d) `PERCENTILE` → **a**
8. Session boundary flag: a) `SUM(CASE WHEN gap>30min THEN 1 END) OVER` b) `GROUP BY` c) `DISTINCT` d) `CROSS` → **a**
9. Median function: a) MEDIAN() b) PERCENTILE_CONT(0.5) c) AVG(d) d) MODE → **b**
10. Pivot uses: a) CASE columns + SUM b) LATERAL c) RECURSIVE d) CROSS → **a**

## 20. Flashcards
- **Q: Top-3 per dept pattern?** → **A:** ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) ≤ 3.
- **Q: Dedup newest pattern?** → **A:** ROW_NUMBER() OVER (PARTITION BY key ORDER BY ts DESC) = 1.
- **Q: Second highest?** → **A:** MAX(x) WHERE x < (SELECT MAX(x)).
- **Q: Running total?** → **A:** SUM(x) OVER (ORDER BY date).
- **Q: Gaps in sequence?** → **A:** LAG(seq) OVER (ORDER BY seq) <> seq - 1.
- **Q: Streak grouping?** → **A:** date - ROW_NUMBER() OVER (ORDER BY date) forms run-groups.
- **Q: Median?** → **A:** PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x).
- **Q: Sessionize?** → **A:** LAG + SUM(boundary) OVER — new session on long gap.

## 21. Revision
15 patterns to have instant: **Top-N** (window + rn≤k), **Dedup** (rn=1), **2nd-highest** (MAX WHERE < MAX), **Running total** (SUM OVER date), **Moving avg** (ROWS frame), **Deltas** (LAG), **Gaps** (LAG compare), **Streaks** (date - ROW_NUMBER), **Sessions** (LAG + SUM boundary), **Median** (PERCENTILE_CONT .5), **Pivot** (CASE columns), **Share** (x/SUM() OVER), **Existence** (NOT EXISTS), **Recursion** (WITH RECURSIVE). Rules of thumb: ties → RANK/DENSE_RANK not ROW_NUMBER; NULLs break NOT IN → NOT EXISTS; big deletes → batch. Interview moves: name the pattern first, then write; give the alternative approach; end with the index/plan note. That triple is a complete answer.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Top-3 per dept?" | 13 Q1, Q16 |
| "Deduplicate keeping newest?" | 13 Q2 |
| "Second highest salary?" | 13 Q3 |
| "Running total / moving average?" | 13 Q4-5 |
| "MoM growth?" | 13 Q6 |
| "Find missing numbers / streaks?" | 13 Q7-8 |
| "Sessionize page views?" | 13 Q9 |
| "Median / percentiles?" | 13 Q10 |
| "Pivot / share-of-total?" | 13 Q11-12 |
| "Customers with no orders?" | 13 Q13 |
