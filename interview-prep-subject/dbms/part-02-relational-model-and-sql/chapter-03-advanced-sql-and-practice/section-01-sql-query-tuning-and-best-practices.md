# SQL Query Tuning and Best Practices

> **TL;DR**: Fast SQL comes from making the optimizer's job easy — filters on indexed columns in index-friendly form, joins on keys, minimal columns/pages touched, and batching — and the way you verify it is reading `EXPLAIN`, not guessing.

## 1. Why Does This Exist?
A query can return the right answer in 5 ms or 5 minutes depending on how it's written — not because the data differs but because the plan differs. Query tuning exists because (a) the optimizer can only use indexes when the SQL is written in *index-friendly* forms (`col = x` yes, `func(col) = x` no), (b) the difference between a scan and a seek is 100-1000×, and (c) every production team hits the "it worked in dev, crawls in prod" wall. This section exists to make you *predict* and *verify* performance — reading `EXPLAIN` is the skill that converts "SQL writer" into "engineer". Interviewers test tuning because it exposes whether you understand the physical layer, not just syntax.

## 2. How Does It Work?
The tuning loop: **measure → read plan → fix → verify**.
- `EXPLAIN` (no execution) shows the plan + estimated costs; `EXPLAIN ANALYZE` runs it and shows actual times/rows.
- Plan nodes tell the story: `Seq Scan` (whole table), `Index Scan` (seek+fetch), `Index Only Scan` (index covers all needed columns), `Bitmap Heap Scan` (bitmap from index), `Hash Join`/`Nested Loop`/`Merge Join` (join algorithms), `Sort`, `Aggregate`.
- The optimizer's decisions hinge on **statistics** (row estimates, selectivity) — stale stats → bad plans → `ANALYZE`.
- Index-friendly SQL: `WHERE col = ...`, `WHERE col BETWEEN ...`, `WHERE col IN (...)`, `WHERE col LIKE 'prefix%'` (B-tree range); **not** `WHERE func(col) = ...`, `WHERE col LIKE '%suffix'`, or non-sargable rewrites.
- Cost levers: rows touched, pages read, `work_mem` spills, sort size, join cardinality.

## 3. When Is It Used?
- **Production incidents**: "orders query got slow" → read the plan, find the Seq Scan on a big table, add/reshape the index.
- **Code review**: reject/accept queries based on predicted plan shape; require `EXPLAIN` for hot paths.
- **Schema/index design**: indexes are *designed from queries* — knowing the query mix determines which (composite/covering/partial) indexes to build.
- **Migration performance**: adding a column, changing a predicate — verify nothing regresses.
- **Interview screens**: "why is this query slow?" and "what index would you add?" — the standard tuning probes.
- **Data engineering**: dbt model performance, warehouse query tuning (same skills, warehouse plans).

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: just "add indexes everywhere".** Rejected: each index slows writes and costs storage; the *right* indexes (matched to the query mix) beat a pile of indexes. Tuning is query-first, not index-first.
- **Alternative: hint-based optimization (force join order / index).** Rejected as the default: hints freeze plans (brittle when data changes) and bypass the optimizer; Postgres deliberately *has no hints* — it forces you to fix statistics/schema. Hints are a last resort.
- **Alternative: denormalize everything for speed.** Rejected as the default: redundancy + update anomalies; tuning first, denormalization only when the read profile demands it (Part 03 §06).
- **Alternative: guess and test (random rewrite until fast).** Rejected: unverifiable; `EXPLAIN` gives *evidence*. The measurement-based loop is the only systematic method.
- **Why EXPLAIN (cost model)?** Because it lets the optimizer and the human share a language — plans, estimated costs, and row counts are comparable, explainable, and diffable.

## 5. Intuition
Tuning is like **choosing the route for a delivery** — you don't guess; you look at the map. `EXPLAIN` is the GPS route preview: it shows "you're planning to drive through every street (Seq Scan)" versus "highway + exit (Index Scan)". `EXPLAIN ANALYZE` is the same route *after driving*, with actual timestamps. A non-sargable predicate (`WHERE YEAR(created)=2024`) is like asking the GPS to visit every house to check the year — the index (the address book) is useless because you force the DB to compute before comparing. Writing index-friendly SQL is handing the optimizer an address book instead of making it knock on every door.

## 6. Real-World Analogy
A **library's card catalog vs walking the shelves**. `WHERE author = 'Tolkien'` uses the card catalog (index) — O(log n) to find, then grab the exact shelves. `WHERE UPPER(author) = 'TOLKIEN'` forces the librarian to check every book's spine one by one (function on the column defeats the catalog). `EXPLAIN` is the librarian's report: "I looked in the catalog (Index Scan), found 40 titles, visited 12 shelves (Heap fetch)". A `Hash Join` is "I wrote a lookup list of all customers in one pass, then checked orders against it" — vs a `Nested Loop` of "for every customer, re-scan all orders". Reading the report tells you exactly which part of the trip wasted time.

## 7. Formal Definition
**Query tuning**: the process of adjusting a query's structure and the underlying schema (indexes, statistics, schema design) so the optimizer selects a lower-cost execution plan, verified via the optimizer's output.
- **EXPLAIN**: shows the plan tree: each node = operator + estimated cost (startup, total), row estimate, width; `ANALYZE` adds actual times, rows, and (with buffers) page reads.
- **Selectivity**: the fraction of rows a predicate passes; low selectivity → index seek; high selectivity → seq scan (index overhead unjustified).
- **Sargable predicate**: one where an index can be used directly (`col OP constant`); non-sargable wraps the column in an expression.
- **Covering index**: an index containing *all* columns the query needs → `Index Only Scan` (no heap fetch).
- **N+1**: executing N queries instead of one combined query (typically ORM loop per parent row).
- **Keyset (seek) pagination**: `WHERE id > $last ORDER BY id LIMIT 10` vs `OFFSET`.
(PostgreSQL EXPLAIN docs; SQL performance canon.)

## 8. Example
```
orders(id, customer_id, region, total, created_at), 1M rows, 50K per region
```
- **Bad**: `SELECT * FROM orders WHERE UPPER(region) = 'WEST';` → **Seq Scan** (1M rows), because UPPER(region) can't use an index on region.
- **Good**: `SELECT * FROM orders WHERE region = 'West';` → **Index Scan** (with index on region), ~50K rows.
- **Covering**: `SELECT region, COUNT(*) FROM orders WHERE region='West' GROUP BY region` with index on (region) → **Index Only Scan** (no heap fetches).
- **Date trap**: `WHERE EXTRACT(YEAR FROM created_at) = 2024` → Seq Scan. Fix: `WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'` → index range scan.
- **ANALYZE evidence**: `EXPLAIN ANALYZE` shows "Seq Scan on orders (cost=0.00..20834.00 rows=1000000)" vs "Index Scan (cost=0.42..152.00 rows=50000)" — the plan is the proof.

## 9. Internal Working
1. **Parse** the query; optimizer reads **statistics** (`reltuples`, histograms, distinct counts) from the catalog.
2. **Generate plans** (join orders, access methods); estimate cost = I/O + CPU per node, summed bottom-up.
3. **EXPLAIN prints the tree**; `ANALYZE` adds actual runtime + row counts (detects mis-estimates → stale stats).
4. **Index usage requires**: (a) the predicate be sargable, (b) selectivity low enough that index seeks beat scans, (c) index covers/points to the needed rows.
5. **Plan types seen**: Seq Scan (scan), Index Scan (seek + heap), Index Only Scan (cover), Bitmap Index/Heap Scan (many matches → bitmap), Hash Join (large equi-join), Nested Loop (small/right-indexed), Merge Join (sorted), Sort (ORDER BY/GROUP BY), Aggregate, CTE materialization.
6. **Batching**: bulk operations (multi-row inserts, batched UPDATE/DELETE) amortize lock+log overhead vs row-at-a-time.

## 10. Time Complexity
- **Seq Scan**: O(n) — reads every page.
- **Index Scan (point)**: O(log_f n + k) (k = matching rows).
- **Index Only Scan**: O(log_f n + k) with *no heap fetches* — the cheapest read.
- **Hash Join**: O(n + m) build+probe; **Nested Loop**: O(n·m) or O(n·log m) with right index; **Merge Join**: O(n log n + m log m).
- **Sort**: O(n log n) — the reason ORDER BY/GROUP BY on indexed order is free.
- **OFFSET pagination**: O(n + page·k) — rescans skipped rows; **keyset**: O(log n + k) per page.
- **N+1**: O(n) queries × O(log m) each vs one join O(n + m) — up to n× worse.

## 11. Advantages
- **100-1000× wins**: index seeks vs scans is the biggest free speedup in databases.
- **Evidence-based**: plans + `ANALYZE` numbers replace guessing.
- **Predictable**: you can predict cost from the plan before running on production.
- **Reversible**: mostly schema/query changes; easy to review and roll back.
- **Compound**: fixing one predicate can unlock a whole class of queries via one index.
- **Interview gold**: tuning questions prove understanding of the physical layer.

## 12. Disadvantages
- **Stale statistics** produce wrong plans — tuning is only as good as `ANALYZE` freshness.
- **Over-indexing** costs writes/storage; "index everything" is a trap.
- **Plan instability**: data distribution changes flip plans (parameterized queries help).
- **EXPLAIN literacy is non-trivial**: misreading costs (e.g., a "fast-looking" plan with huge row-count mis-estimates) misleads.
- **No universal answers**: what's optimal depends on data size, distribution, hardware, and query mix — the tuning advice is conditional.
- **Non-sargable rewrites can hurt readability**: `created_at >= '2024-01-01'` is less obvious than `YEAR(created_at) = 2024` though it's what makes the index work.

## 13. Interview Questions
1. **Q: What is a Seq Scan vs an Index Scan?** A: Seq Scan reads every page of the table (O(n)) — the baseline. Index Scan uses a B+ tree to locate matching rows (O(log n + k)) then fetches them from the heap. Index Only Scan skips the heap entirely when the index covers all needed columns.
2. **Q: What does `EXPLAIN` vs `EXPLAIN ANALYZE` show?** A: EXPLAIN shows the plan and *estimated* costs without running; EXPLAIN ANALYZE executes and adds *actual* times and row counts. The actual vs estimated comparison reveals stale statistics or bad estimates.
3. **Q (production): Your query got slow overnight. First steps?** A: (1) `EXPLAIN ANALYZE` the query; (2) look for a new Seq Scan / a plan change (stale stats, changed data distribution); (3) check `ANALYZE` recency and the index; (4) compare the old vs new plan. Statistics or index regression is the usual cause.
4. **Q: Why does `WHERE UPPER(region)='WEST'` ignore the index?** A: Non-sargable — the function must be computed on every column value before comparison, so the B+ tree's ordering is useless. Fix: store normalized values or use a functional index (Postgres supports indexes on expressions).
5. **Q: What is selectivity and how does it drive index choice?** A: Selectivity = fraction of rows a predicate passes. Low selectivity (few rows) → index seek wins. High selectivity (many rows, e.g., 90%) → seq scan wins (index adds per-row random I/O). The optimizer estimates selectivity from statistics.
6. **Q: What is a covering index / Index Only Scan?** A: An index whose entries contain every column the query needs — no heap fetch. E.g., index on (region, total) serves `SELECT total FROM orders WHERE region='West'`. The fastest read form.
7. **Q (tricky): `WHERE year = 2024` on a date column — index friendly or not?** A: Depends: `EXTRACT(YEAR FROM created_at) = 2024` is not; `created_at BETWEEN '2024-01-01' AND '2024-12-31'` is. The range form is sargable and uses the index.
8. **Q: What is the N+1 problem?** A: One query for the parents + one per child (N queries) — e.g., ORM loops: 100 orders → 100 customer queries. Fix: one JOIN (or one IN) — single query, single plan, order-of-magnitude fewer round trips.
9. **Q (production): Why is OFFSET pagination slow at deep pages?** A: OFFSET must scan and discard all preceding rows each time (O(n) per page). Fix: keyset pagination `WHERE id > $last ORDER BY id LIMIT 10` (index seek per page, O(log n + k)), plus stable order.
10. **Q: Hash join vs nested loop — when does each win?** A: Hash join: large equi-joins, both sides scanned once (O(n+m)); uses `work_mem` (spills if exceeded). Nested loop: small outer × indexed inner (O(n·log m)); no build memory; works for non-equality predicates (range joins).
11. **Q: When does the optimizer choose a Seq Scan over an available index?** A: When the estimated selectivity is high (most rows qualify) or the table is small — index I/O + random page fetches exceeds sequential read cost. Example: `WHERE active = true` on a 95%-active table.
12. **Q (scenario): A report does `GROUP BY region` on 10M rows every 5 minutes. How do you speed it up?** A: (a) Ensure stats are fresh (ANALYZE); (b) a composite index on (region) gives a covering/ordered aggregate; (c) columnar pre-aggregation/mart (if warehouse) or materialized view; (d) parallel workers. Start with the plan: a Sort-free hash aggregate on fewer columns.
13. **Q: What is a Bitmap Index Scan?** A: An index scan that produces a bitmap of matching pages, then fetches heap pages (possibly in order) — chosen when many rows match (low-mid selectivity). Avoids per-row random I/O by clustering page fetches.
14. **Q (tricky): Why does adding an index sometimes slow a query?** A: The optimizer may choose a different plan that's estimated-cheaper but actually worse, or the write side slows (index maintenance). Always measure with EXPLAIN ANALYZE before/after.
15. **Q: What does `work_mem` (Postgres) do?** A: It bounds memory for sorts/hash joins/aggregates. When exceeded, operators spill to disk → 10-100× slowdown. `EXPLAIN ANALYZE` shows "Disk:" when spilling — the fix is raising work_mem (or better indexes).
16. **Q (production): How do you fix a plan regression after a data change?** A: (1) `ANALYZE` the table (refresh stats); (2) compare plans before/after; (3) reindex if bloat; (4) if the optimizer is stubborn, rewrite the query (or use `pg_hint_plan` as a last resort — Postgres has no native hints).
17. **Q: What is "index-only scan" and when is it impossible?** A: Impossible when the query needs a column *not* in the index, or when visibility info requires a heap check (Postgres: an older index version needs heap visit for MVCC visibility — the "visibility map" reduces this).
18. **Q: How do you tune a query that scans a 100M-row table for a needle?** A: Find the selective predicate and index it; if the predicate is non-sargable, rewrite it; if no predicate exists, the query is genuinely a scan — consider a covering aggregate, partitioning, or a precomputed table (mart).
19. **Q (hard): A JOIN between two 10M tables returns 5M rows — which join algorithm and why?** A: Hash join (O(n+m)) on the equi-keys — both sides hashed, probed in memory; nested loop would be 10M×10M. If output must be ordered or inputs are pre-sorted, merge join. Check the plan for `Hash Join` + whether it spilled.
20. **Q: What is the difference between an index and a statistics object for tuning?** A: An index speeds *access* (B+ tree). Statistics (histograms, distinct counts) inform the *optimizer's estimates* that choose which access/join. Both matter: right index + stale stats = wrong plan; fresh stats + no index = scan. Tuning is the pair working together.

## 14. Follow-Up Questions
1. **Q: What is a functional index?** A: `CREATE INDEX ON t (UPPER(col))` — an index on an expression; makes `WHERE UPPER(col)=...` an index seek. Postgres-specific (also MySQL: expression indexes in 8.0.13+).
2. **Q: What is `pg_stat_statements`?** A: A Postgres extension tracking normalized query performance (calls, total/mean time, buffers) — the production tool to find the slowest queries to tune. Every Postgres shop uses it.
3. **Q: What are parameterized/prepared statements and why do they matter?** A: `PREPARE`/driver-prepared SQL parse+plan once, reuse per value — both injection-safe and plan-cached. Generic vs custom plans matter for parameterized queries (Postgres picks based on parameter frequency).
4. **Q: What is a materialized view's role in tuning?** A: Precomputed, indexed results refreshed on schedule — the classic "query too expensive to run live" fix (reporting marts). Staleness is the trade-off.
5. **Q: What is parallel query execution?** A: The planner splits scans/aggregates/joins across workers (`parallel workers`); small queries stay serial (setup cost). Warehouse performance is largely this + columnar storage.

## 15. Coding Example
```sql
-- Diagnose: run this to see the plan
EXPLAIN ANALYZE
SELECT region, COUNT(*), SUM(total)
FROM   orders
WHERE  created_at >= '2024-01-01' AND created_at < '2025-01-01'
GROUP  BY region;
-- Look for: Index Scan vs Seq Scan; Hash Aggregate vs GroupAggregate; actual vs estimated rows

-- The index that serves the above (covering for the aggregate)
CREATE INDEX idx_orders_region_created_total
  ON orders (region, created_at, total);

-- Fixing N+1 (app loop) with one query
SELECT c.name, o.id, o.total
FROM   customers c
LEFT JOIN orders o ON o.customer_id = c.id   -- one query, not 1+N
WHERE  c.active = true;

-- Keyset pagination (stable, index-friendly)
-- page 1:
SELECT * FROM orders WHERE id > 0    ORDER BY id LIMIT 10;
-- page 2 (using last id from page 1):
SELECT * FROM orders WHERE id > 1234 ORDER BY id LIMIT 10;  -- index seek, no OFFSET

-- Non-sargable → sargable rewrite
SELECT * FROM orders WHERE EXTRACT(YEAR FROM created_at) = 2024;        -- scan
SELECT * FROM orders WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';  -- seek
```

## 16. Industry Usage
- **Every backend team's slow-query workflow** starts with `EXPLAIN ANALYZE` + `pg_stat_statements`/MySQL slow log — this section is the shared playbook.
- **Amazon/Google/Meta SQL screens** include "what index would you add?" and "why is this query slow?" — directly this section.
- **dbt/warehouse tuning** uses the same plans (Snowflake `EXPLAIN`, BigQuery `EXPLAIN ANALYZE`); models are performance-reviewed with cost + bytes scanned.
- **Index design services** (PgHero, pg_stat_plans, DTA for SQL Server, EXPLAIN tools) automate exactly this loop — prove the methodology is standard, not exotic.
- **Plan regressions** are the #1 production performance incident: monitoring plan changes (e.g., auto_explain sampling) is standard SRE practice at scale.

## 17. References
- PostgreSQL Documentation, `EXPLAIN`: https://www.postgresql.org/docs/current/using-explain.html
- PostgreSQL Documentation, `pg_stat_statements`: https://www.postgresql.org/docs/current/pgstatstatements.html
- PostgreSQL Documentation, Indexes (Chapter 11): https://www.postgresql.org/docs/current/indexes.html
- MySQL Reference Manual, EXPLAIN: https://dev.mysql.com/doc/refman/8.0/en/explain-output.html
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 12-13 (Query Processing & Optimization).
- Use the Index, Luke! (SQL performance guide): https://use-the-index-luke.com/

## 18. Cheat Sheet
- Measure first: `EXPLAIN ANALYZE` before changing anything.
- Node types: SeqScan, IndexScan, IndexOnlyScan, BitmapScan, Hash/Nested/Merge Join, Sort.
- Sargable predicates use indexes; wrap-free column comparisons only.
- Low selectivity → index; high selectivity → scan.
- Covering index (all columns) → Index Only Scan (fastest).
- N+1: one JOIN, not N queries.
- OFFSET rescans → keyset `WHERE id > $last LIMIT 10`.
- Stale stats → wrong plans → `ANALYZE`.

## 19. Quiz
1. Which shows actual runtimes? a) EXPLAIN b) EXPLAIN ANALYZE c) SELECT d) DESCRIBE → **b**
2. `WHERE UPPER(region)='WEST'` → a) Index Scan b) Seq Scan c) Hash d) Sort → **b**
3. A covering index gives: a) Seq Scan b) Index Only Scan c) Merge Join d) Sort → **b**
4. N+1 is: a) 1 query per parent b) a loop of queries c) a pagination trick d) an index → **b**
5. OFFSET pagination is slow because: a) sorts b) rescans skipped rows c) locks d) NULLs → **b**
6. High-selectivity predicates favor: a) index seek b) seq scan c) hash d) merge → **b**
7. Hash join complexity: a) O(n·m) b) O(n+m) c) O(log n) d) O(n!) → **b**
8. Postgres has: a) rich hints b) no native hints c) mandatory hints d) only MySQL hints → **b**
9. Stale statistics cause: a) wrong plans b) data loss c) deadlocks d) index drops → **a**
10. Date-range rewrite `created_at BETWEEN` is: a) non-sargable b) sargable c) an error d) a join → **b**

## 20. Flashcards
- **Q: What does EXPLAIN show?** → **A:** The plan tree with estimated costs; ANALYZE adds actual times/rows.
- **Q: Seq vs Index Scan?** → **A:** All pages (O(n)) vs index seek + heap fetch (O(log n + k)).
- **Q: What is sargable?** → **A:** A predicate the index can use directly (`col = x`, not `f(col)=x`).
- **Q: Covering index?** → **A:** Index containing all needed columns → Index Only Scan.
- **Q: N+1 problem?** → **A:** Loop of per-parent queries; fix with one JOIN.
- **Q: Why OFFSET is slow?** → **A:** Rescans skipped rows; use keyset pagination.
- **Q: Hash join complexity?** → **A:** O(n+m) — the big equi-join default.
- **Q: Plan regression fix?** → **A:** ANALYZE (stats), compare plans, reindex, rewrite.

## 21. Revision
Tuning loop: **EXPLAIN ANALYZE → find the bad node → fix → verify**. Read nodes: SeqScan (bad on big tables), IndexScan/IndexOnlyScan (good), HashJoin (big joins), Sort (expensive), bitmap for mid-selectivity. Sargable predicates only: `col = x`, `col BETWEEN`, `col LIKE 'pre%'`; rewrite `YEAR(col)=x` as a range. Covering indexes → Index Only Scan. High selectivity → scan (don't force index). Kill N+1 with one JOIN; replace OFFSET with keyset `WHERE id > $last LIMIT 10`; keep stats fresh (`ANALYZE`) — stale stats = wrong plans. Interview moves: diagnose a slow query out loud with the checklist; state "no native hints in Postgres, fix stats/schema instead"; and always propose the index *from the query's predicates*.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Seq vs Index scan?" | 13 Q1 |
| "EXPLAIN vs ANALYZE?" | 13 Q2 |
| "Why is a query slow?" | 13 Q3 |
| "Non-sargable predicates?" | 13 Q5, Q7 |
| "What is a covering index?" | 13 Q6 |
| "N+1 problem?" | 13 Q8 |
| "OFTSET vs keyset pagination?" | 13 Q9 |
| "Hash vs nested loop?" | 13 Q10 |
