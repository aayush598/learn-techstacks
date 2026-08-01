# Aggregation and GROUP BY

> **TL;DR**: GROUP BY collapses many rows into one summary row per group, and HAVING filters those groups — while WHERE filters rows *before* grouping, SELECT can only reference grouped/aggregated columns, and NULLs are excluded from aggregates (except COUNT(*)).

## 1. Why Does This Exist?
Raw tables hold millions of event rows; almost every question is answered *in summary*: "revenue per region", "avg GPA per dept", "count of orders per status". Aggregation exists to reduce rows to meaningful summaries *inside the database* (avoid shipping millions of rows to the app). This section exists because aggregation has the strictest semantics in SQL: what may appear in SELECT (only grouped or aggregated columns), when HAVING applies (after grouping), how NULLs count (mostly they don't), and how DISTINCT modifies aggregates. Getting these wrong produces silently wrong dashboards — the highest-cost bug class in analytics.

## 2. How Does It Work?
Pipeline: FROM → WHERE (row filter) → **GROUP BY** (partition rows into groups by the listed columns) → per-group **aggregate functions** (`SUM`, `AVG`, `COUNT`, `MIN`, `MAX`, `STDDEV`, `ARRAY_AGG`, ...) → **HAVING** (filter groups) → SELECT → ORDER BY → LIMIT. Rules: (1) every non-aggregated column in SELECT must be in GROUP BY (else ambiguous); (2) WHERE cannot use aggregates (pre-grouping); (3) HAVING may use aggregates; (4) aggregates ignore NULLs (`SUM` of {1,NULL,2} = 3; `AVG` = 1.5) except `COUNT(*)`; (5) `COUNT(DISTINCT col)` counts distinct non-NULL; (6) `GROUP BY` with no groups = one group over all rows.

## 3. When Is It Used?
- **Reporting/dashboards**: revenue by month, active users by region, order counts by status.
- **Analytics** (every warehouse query): fact tables grouped by dimensions.
- **Deduplication**: `SELECT col, COUNT(*) FROM t GROUP BY col` finds duplicates.
- **HAVING patterns**: "departments with > 100 employees", "customers spending > $10k".
- **Rollups**: `GROUP BY ROLLUP/CUBE/GROUPING SETS` (multi-level subtotals) — the OLAP extension.
- **Performance**: pushing aggregation into the DB (single pass) beats pulling raw rows to the app.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: aggregate in application code.** Rejected: ships millions of rows over the network, re-implements the logic per app, and loses the engine's single-pass aggregation + parallelism.
- **Alternative: let WHERE see aggregates (merge HAVING into WHERE).** Rejected: WHERE runs pre-grouping; aggregates don't exist yet. HAVING is the post-grouping filter — one clause per pipeline stage (matches the logical order).
- **Alternative: allow arbitrary non-grouped columns in SELECT (pick one per group).** Rejected (by the standard; MySQL 5.7 allowed it with random results!): results would be nondeterministic. Strict `ONLY_FULL_GROUP_BY` makes the ambiguity an error.
- **Alternative: aggregates include NULLs as zeros.** Rejected: NULL = missing, not zero — `AVG(1, NULL, 2)` should be 1.5 (mean of present values), not 1.0. The NULL-ignoring rule matches the semantics of missing data.
- **Why GROUP BY for grouping?** It's the algebra's γ generalized projection — set-theoretic, composable with joins and window functions.

## 5. Intuition
Imagine sorting a deck of cards **by suit**, then **counting** each pile. WHERE is "throw out the jokers first." GROUP BY is "make piles by suit." The count/avg per pile is the aggregate. HAVING is "keep only piles with more than 5 cards." And here's the rule: once you've made piles, you may only talk about *pile-level* facts (how many, the average card value) or the pile's *defining* feature (the suit) — you can't point at "the third card" of a pile, because the cards' order inside a pile isn't stored. That's exactly why SELECT may only use grouped columns and aggregates.

## 6. Real-World Analogy
A **store's monthly sales meeting**: the manager groups all receipts by salesperson (GROUP BY salesperson). For each stack: total sales (SUM), average ticket (AVG), number of receipts (COUNT). The meeting keeps only salespeople with more than 100 receipts (HAVING COUNT(*) > 100). Now, the manager can state "Ravi's total" but cannot say "Ravi's 5th receipt" — receipts within a stack have no order (that's the no-non-grouped-columns rule). WHERE would have been "discard returns before grouping" (filter rows), HAVING is "decide which stacks to discuss" (filter groups) — two different decisions, two different clauses.

## 7. Formal Definition
Given relation R and grouping attributes G = {g₁,...,gk}, the **generalized projection** γ_G,_{f1(A1),...,fm(Am)}(R) partitions R into groups, each group = { tuples sharing identical values on G }, and produces one tuple per group with the G values plus the results fⱼ(Aⱼ) of the aggregate functions. A **group** is a maximal set of tuples agreeing on G. **HAVING** is a predicate evaluated per group after aggregation. Aggregates: `COUNT(*)` counts tuples; `COUNT(A)`, `SUM`, `AVG`, `MIN`, `MAX` ignore NULL inputs; `COUNT(DISTINCT A)` counts distinct non-NULL values. `ROLLUP(G)` computes subtotals at each prefix of G; `CUBE` at all combinations; `GROUPING SETS` selects arbitrary subsets. (Elmasri & Navathe Ch. 5; ISO/IEC 9075.)

## 8. Example
```
orders: (id, customer, region, amount)
(1,A,West,100),(2,B,West,50),(3,C,East,200),(4,A,East,75),(5,D,West,NULL)
```
- **Count by region**: `SELECT region, COUNT(*) FROM orders GROUP BY region;` → West:3, East:2.
- **Sum by region (NULL-ignoring)**: `SUM(amount)` → West:150 (100+50+0), East:275.
- **Region total with HAVING**: `SELECT region, COUNT(*) n, SUM(amount) total FROM orders GROUP BY region HAVING COUNT(*) >= 2;` → West(3,150), East(2,275).
- **WHERE vs HAVING**: `WHERE amount >= 75` first → West:100, East:200,75 → grouped West:1, East:2. Different result than HAVING on the same predicate — know which you mean.
- **COUNT vs COUNT(DISTINCT)**: customers per region: `COUNT(customer)` = 3 (West, with dup A counted twice); `COUNT(DISTINCT customer)` = 2 (A,B) — dedup matters.

## 9. Internal Working
1. **Parse**: `SELECT region, SUM(amount) FROM orders WHERE ... GROUP BY region HAVING ...` → plan: filter → hash aggregate → filter groups.
2. **Hash aggregation**: build a hash table keyed by group keys; for each input row, find/insert the group entry and update running aggregates (single pass, O(n) memory-bounded by `work_mem`; spills to disk if too big).
3. **Sort aggregation**: if ORDER BY the group key is needed or hash is unhelpful, sort by group keys (O(n log n)) then scan runs, finalizing each group.
4. **Grouping sets/rollup**: multiple aggregations share one scan; engines use specialized multi-pass or extend the hash table with sentinel group keys.
5. **HAVING**: evaluated per group after aggregation (like a second filter at the group level).
6. **NULL group keys**: all-NULL group key forms its own group (NULLs group together in GROUP BY — unlike WHERE comparisons).

## 10. Time Complexity
- **Hash aggregate**: O(n) time, O(#groups) memory (single pass; spills if memory exceeded).
- **Sort aggregate**: O(n log n) (no hash memory, ordered output).
- **HAVING**: O(#groups) after aggregation.
- **COUNT(DISTINCT)**: O(n) hash / O(n log n) sort (expensive — dedup cost).
- **ROLLUP/CUBE/GROUPING SETS**: O(n · #sets) with shared scans (engines amortize).
- **Aggregate pushdown with index**: MIN/MAX can use B+ tree ends O(log n) (or O(1) per side) if no GROUP BY; COUNT(*) with MVCC needs scans (no cheap trick in Postgres).

## 11. Advantages
- **In-database reduction**: summaries computed once, in one pass — no row shipping.
- **Parallelism**: engines parallelize aggregation across workers (partial → final).
- **Expressiveness**: HAVING + DISTINCT + ROLLUP/CUBE cover most reporting needs.
- **NULL honesty**: aggregates ignore NULLs (or count them via COUNT(*)) — semantics match "missing."
- **Composable**: GROUP BY works over joins, subqueries, and window functions.
- **Deterministic**: strict ONLY_FULL_GROUP_BY makes ambiguous output an error, not a guess.

## 12. Disadvantages
- **Ambiguity trap**: non-grouped columns in SELECT → nondeterministic/wrong rows (MySQL 5.7 legacy) or errors.
- **NULL surprises**: `AVG` ignoring NULLs is correct but surprises people; `SUM` of all-NULL = NULL, not 0 (use COALESCE).
- **COUNT(DISTINCT) is expensive**: per-group dedup requires memory/sort; big-cardinality distinct is slow.
- **Memory spills**: huge group counts or `work_mem` exhaustion → disk spill, big slowdowns.
- **Not lossless**: aggregates destroy row-level detail — you can't recover rows after grouping (window functions exist for that).
- **HAVING misplacement**: putting row filters in HAVING runs them post-aggregation (slower + semantically wrong).

## 13. Interview Questions
1. **Q: Explain GROUP BY semantics.** A: It partitions rows into groups of equal values on the grouped columns; one output row per group, with aggregate functions computed within each group. Non-grouped, non-aggregated columns aren't allowed in SELECT.
2. **Q: What's the difference between WHERE and HAVING?** A: WHERE filters rows *before* grouping (no aggregates); HAVING filters groups *after* aggregation (aggregates allowed). Same predicate on a column works in both, but WHERE is cheaper and semantics differ.
3. **Q (tricky): Why does `SELECT dept, name FROM t GROUP BY dept` fail?** A: `name` is neither grouped nor aggregated — within a dept group there are many names; which one to show is ambiguous. Postgres errors; MySQL 5.7 silently picked an arbitrary one (removed in 8.0 `ONLY_FULL_GROUP_BY` default).
4. **Q: How do aggregates handle NULLs?** A: `SUM/AVG/MIN/MAX/COUNT(col)` ignore NULLs (AVG(1,NULL,2)=1.5). `COUNT(*)` counts all rows including all-NULL ones. `COUNT(DISTINCT col)` counts distinct non-NULL. `SUM` of all-NULL input = NULL (not 0) — use `COALESCE(SUM(x),0)`.
5. **Q (production): "Total revenue per region for regions with > 100 orders."** A: `SELECT region, SUM(amount) revenue, COUNT(*) n FROM orders GROUP BY region HAVING COUNT(*) > 100;` — grouping first, then the group filter.
6. **Q: What does `COUNT(*)` vs `COUNT(amount)` return when amount has 3 NULLs out of 10 rows?** A: `COUNT(*)`=10; `COUNT(amount)`=7 (NULLs excluded); `COUNT(DISTINCT amount)` = distinct non-NULL count. The NULL rule is the whole difference.
7. **Q (scenario): Find duplicate emails.** A: `SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;` — the canonical dedup detector.
8. **Q: What are ROLLUP, CUBE, GROUPING SETS?** A: ROLLUP(a,b) = subtotals at (a,b), (a), and grand total; CUBE = all combinations; GROUPING SETS = arbitrary chosen groupings. They produce multi-level summaries in one statement (OLAP).
9. **Q (tricky): Does GROUP BY sort the output?** A: Not guaranteed — hash aggregation returns groups in arbitrary order. Add ORDER BY for determinism. (Sort-aggregate happens to produce sorted output but it's not a contract.)
10. **Q: Can you use an aggregate in WHERE?** A: No — WHERE runs before grouping; aggregates don't exist yet. `WHERE SUM(x) > 5` is a syntax/semantic error. Use HAVING (post-group) or a subquery/CTE.
11. **Q (production): How do you compute the percentage of total revenue per region?** A: `SELECT region, SUM(amount) revenue, SUM(amount) * 100.0 / SUM(SUM(amount)) OVER () pct FROM orders GROUP BY region;` — window functions over aggregates (or a subquery computing the grand total).
12. **Q: What is the difference between `GROUP BY` and `DISTINCT`?** A: GROUP BY also aggregates (can compute per-group stats) and produces one row per group; DISTINCT only dedupes full rows. `SELECT DISTINCT dept FROM t` ≡ `SELECT dept FROM t GROUP BY dept`.
13. **Q: Can GROUP BY use an alias?** A: Postgres and MySQL allow `GROUP BY alias` (alias resolved); SQL Server historically not; standard says it must be the expression. Prefer writing the full expression for portability.
14. **Q (tricky): `SELECT dept, AVG(gpa) FROM students GROUP BY dept` — what about NULL gpas?** A: They're excluded from AVG (mean of non-NULL). If you want them treated as 0, `AVG(COALESCE(gpa, 0))`. Also, a dept with only-NULL gpas → AVG = NULL (no rows counted) — another COALESCE case.
15. **Q: What is "aggregate pushdown" in optimization?** A: Pushing aggregation below a join so fewer rows flow through the join (e.g., pre-aggregate orders per customer before joining). Requires the aggregate to be semantically valid at the lower level (e.g., partial aggregates with COUNT/SUM).
16. **Q (production): Why is `COUNT(DISTINCT user_id)` slow on a big table?** A: Dedup requires a hash table or sort over the whole column (O(n) memory or O(n log n)); no cheap approximation. For huge datasets, use approximate distinct (HyperLogLog in Postgres via extensions, or `APPROX_COUNT_DISTINCT` in BigQuery/Redshift).
17. **Q: What happens if you GROUP BY on a column with all NULLs?** A: All-NULL rows form a single group (NULLs group together in GROUP BY) — one group with those rows. This differs from WHERE semantics (NULL never matches), a classic gotcha.
18. **Q (scenario): "Average order value per customer, keep customers above the global average AOV."** A: `WITH aov AS (SELECT customer_id, AVG(amount) av FROM orders GROUP BY customer_id), g AS (SELECT AVG(amount) gv FROM orders) SELECT customer_id FROM aov, g WHERE av > gv;` — or use a window: `HAVING AVG(amount) > (SELECT AVG(amount) FROM orders)`. Name both approaches.
19. **Q: What is the difference between `GROUP BY ()` and no GROUP BY?** A: `GROUP BY ()` explicitly creates one group (grand total); no GROUP BY with aggregates also computes a single row but treats the whole query as one aggregate. Both give a one-row total; `GROUP BY ()` composes better with ROLLUP/UNION.
20. **Q (hard): Why might a HAVING filter be slower than the same filter in a subquery?** A: HAVING runs after full aggregation — the engine must aggregate *all* rows first (or push the filter into the aggregate if it's deterministic). A WHERE on the same predicate pre-aggregation reduces the aggregation input. Always prefer WHERE for row-level predicates.

## 14. Follow-Up Questions
1. **Q: What is the difference between `FILTER (WHERE ...)` in Postgres and HAVING?** A: `FILTER` conditions *which rows feed one aggregate* (per-aggregate selective aggregation) — `COUNT(*) FILTER (WHERE amount > 100)` counts only qualifying rows within the group. HAVING filters whole groups afterward. Different granularity.
2. **Q: Can you aggregate inside a window function?** A: Yes — `SUM(...) OVER (PARTITION BY ...)` is the row-preserving version of GROUP BY's SUM. The classic "running total" pattern; Section 06 covers it.
3. **Q: What are "partial aggregates"?** A: In parallel aggregation, each worker aggregates its share (partial), then a final aggregate merges (final). That's why COUNT/SUM are mergeable but AVG is computed as SUM/COUNT under the hood.
4. **Q: When is GROUP BY the wrong tool?** A: When you need per-row results alongside summaries, or rankings within groups (top-N) — those need window functions, not GROUP BY, which destroys rows.
5. **Q: How does a columnar warehouse aggregate faster than Postgres?** A: Columnar storage scans only the aggregated columns (compressed, vectorized), not whole rows — a huge I/O win for `SELECT region, SUM(amount)`. The SQL is identical; storage differs.

## 15. Coding Example
```sql
-- Sample: orders
SELECT region, COUNT(*) AS n, SUM(amount) AS total,
       AVG(amount) AS avg, COUNT(DISTINCT customer_id) AS customers
FROM   orders
WHERE  status = 'paid'                    -- rows filtered pre-grouping
GROUP  BY region                          -- group by dimension
HAVING COUNT(*) >= 2                      -- groups filtered post-aggregation
ORDER  BY total DESC;

-- Aggregate with FILTER (Postgres): conditional aggregation
SELECT region,
       COUNT(*) AS all_orders,
       COUNT(*) FILTER (WHERE amount >= 100) AS big_orders
FROM   orders
GROUP  BY region;

-- ROLLUP: subtotal per region + grand total
SELECT region, COUNT(*) AS n, SUM(amount) AS total
FROM   orders
GROUP  BY ROLLUP (region);                -- adds a NULL-region grand-total row

-- Grand total as a column (window over aggregate)
SELECT region, SUM(amount) AS total,
       SUM(SUM(amount)) OVER () AS grand_total
FROM   orders GROUP BY region;
```

## 16. Industry Usage
- **Every dashboard** is GROUP BY under the hood: Looker/Tableau generate `GROUP BY` queries from semantic models; dbt models aggregate event tables into marts.
- **Warehouses** (Snowflake, BigQuery, Redshift) specialize in GROUP BY performance: columnar scans + vectorized aggregation + result caching — "revenue by region" in a second over billions of rows.
- **Postgres/MySQL** use hash aggregates for OLTP reporting; `pg_stat_statements` + `EXPLAIN` show `HashAggregate`/`GroupAggregate` nodes when debugging.
- **Streaming engines** (Flink, Kafka Streams) implement *stateful* GROUP BY over windows — tumbling/hopping windows are aggregation over time partitions.
- **HyperLogLog** (approximate distinct) is the standard at scale (Druid, BigQuery, Postgres `hll` extension) because exact COUNT(DISTINCT) doesn't scale to exabyte event streams.

## 17. References
- PostgreSQL Documentation, Aggregates: https://www.postgresql.org/docs/current/functions-aggregate.html
- PostgreSQL Documentation, GROUP BY / HAVING: https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUP
- MySQL Reference Manual, GROUP BY: https://dev.mysql.com/doc/refman/8.0/en/group-by-handling.html
- ISO/IEC 9075-2:2016 (SQL — aggregate functions, grouping).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 4 (Aggregation).

## 18. Cheat Sheet
- WHERE → (rows) → GROUP BY → (groups) → HAVING → (groups) → SELECT.
- SELECT may contain only grouped columns + aggregates.
- Aggregates ignore NULLs; COUNT(*) counts all; SUM of all-NULL = NULL.
- HAVING can use aggregates; WHERE cannot.
- `GROUP BY x HAVING COUNT(*) > n` = the reporting backbone.
- DISTINCT ≠ GROUP BY; COUNT(DISTINCT) is expensive.
- ROLLUP / CUBE / GROUPING SETS = subtotals.
- Use COALESCE(SUM(x),0) to avoid NULL totals.

## 19. Quiz
1. Which filters groups? a) WHERE b) HAVING c) LIMIT d) FROM → **b**
2. `SELECT dept, name FROM t GROUP BY dept` is: a) valid b) invalid (name ambiguous) c) returns first name d) drops rows → **b**
3. AVG(1, NULL, 2) = a) 1 b) 1.5 c) NULL d) 3 → **b**
4. COUNT(*) with 3 NULLs in a 10-row table: a) 7 b) 10 c) 3 d) 0 → **b**
5. SUM of all-NULL input: a) 0 b) NULL c) error d) -1 → **b**
6. Aggregate in WHERE: a) valid b) invalid — HAVING c) slow but ok d) synonym → **b**
7. ROLLUP(region) adds: a) more rows b) subtotal/grand-total rows c) indexes d) NULLs only → **b**
8. Which finds duplicates? a) `GROUP BY email HAVING COUNT(*)>1` b) `WHERE COUNT(*)>1` c) `DISTINCT email` d) `ORDER BY` → **a**
9. COUNT(DISTINCT col) counts: a) all values b) distinct non-NULL c) NULLs d) rows → **b**
10. GROUP BY output order: a) guaranteed b) arbitrary without ORDER BY c) reversed d) PK-based → **b**

## 20. Flashcards
- **Q: WHERE vs HAVING?** → **A:** Rows pre-grouping vs groups post-aggregation.
- **Q: Rule for SELECT with GROUP BY?** → **A:** Only grouped columns + aggregates allowed.
- **Q: How do aggregates treat NULLs?** → **A:** Ignored (except COUNT(*)); SUM of all-NULL = NULL.
- **Q: What is ROLLUP?** → **A:** Subtotals across group hierarchies + grand total.
- **Q: Find duplicates?** → **A:** `GROUP BY email HAVING COUNT(*)>1`.
- **Q: COUNT vs COUNT(DISTINCT)?** → **A:** Non-NULL count vs distinct non-NULL count.
- **Q: Why is COUNT(DISTINCT) slow?** → **A:** Dedup needs hash/sort (use HLL at scale).
- **Q: FILTER (WHERE...) vs HAVING?** → **A:** Per-aggregate row filter vs whole-group filter.

## 21. Revision
Aggregation pipeline: WHERE (rows) → GROUP BY (groups) → aggregates → HAVING (groups) → SELECT → ORDER BY. Rules: SELECT = grouped columns + aggregates only; HAVING may use aggregates, WHERE may not; aggregates ignore NULLs (COUNT(*) counts all, SUM of all-NULL = NULL → COALESCE); COUNT(DISTINCT) is the expensive dedup. Tools: ROLLUP/CUBE/GROUPING SETS for subtotals; FILTER for conditional aggregation; window-over-aggregate for grand-total columns. Interview moves: write "revenue per region HAVING > 100"; explain the `SELECT dept, name` error; state the AVG-NULL semantics; and answer "duplicates?" with `GROUP BY ... HAVING COUNT(*)>1`. Prefer WHERE for row predicates (cheaper).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "WHERE vs HAVING?" | 7 / 13 Q2 |
| "Why can't SELECT use non-grouped columns?" | 13 Q3 |
| "NULL behavior of aggregates?" | 13 Q4-6 |
| "Revenue by region with HAVING?" | 13 Q5 |
| "Find duplicates?" | 13 Q7 |
| "ROLLUP/CUBE?" | 13 Q8 |
| "COUNT(DISTINCT) cost?" | 13 Q16 |
| "Grouped percentage / grand total?" | 13 Q11 |
