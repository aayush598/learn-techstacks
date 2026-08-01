# Query Processing Pipeline and Steps

> **TL;DR**: A SQL statement becomes results through four stages — parse → rewrite → plan (optimize) → execute — and understanding where each stage happens (and where it can fail) is the foundation for every query-tuning discussion.

## 1. Why Does This Exist?
SQL is a *declarative* language: you say *what* you want, not *how* to get it. That's its power — but someone must translate "join orders and customers" into concrete steps (which table first? index or scan? which join algorithm?). The query processing pipeline exists to convert declarative SQL into an executable *plan* and run it efficiently. Without it, every query would be hand-written in procedural code. The pipeline also creates the separation that makes optimization possible: the *logical* query (what the user wrote) is decoupled from the *physical* plan (how the engine executes), so the optimizer can choose among many equivalent physical implementations.

## 2. How Does It Work?
Four stages:
1. **Parsing**: the SQL text is tokenized and parsed into an **AST** (abstract syntax tree), then bound to catalog objects (tables, columns, types). Syntax errors and missing objects surface here.
2. **Rewriting**: the parser's tree is transformed by rules — expanding **views**, applying security views (RLS), simplifying subqueries (`UNNEST`), constant folding, and standardizing the query (Postgres: rewrite system; MySQL: optimizer performs some rewrites).
3. **Planning/Optimization**: the planner produces a logical plan, generates *physical* alternatives (join orders, join algorithms, scan strategies), estimates costs from statistics, and picks the cheapest. (Deep dive in Chapter 02.)
4. **Execution**: the executor runs the plan top-down (or bottom-up), streaming rows from scans through operators (joins, filters, aggregates) to the client. Sort/memory/hash resources are managed here (e.g., `work_mem`, spill to disk).

## 3. When Is It Used?
- Every single query, from `SELECT 1` to a 20-table report.
- **Prepared statements / plan caching**: parsing+planning done once, execution repeated (Postgres caches per-session, MySQL per-connection).
- **Statement-level vs plan-level features**: `EXPLAIN` runs the planner but not the executor; `EXPLAIN ANALYZE` runs both; `VACUUM ANALYZE` refreshes the statistics the planner reads.
- **Query rewriting** for optimization: view expansion, subquery flattening, predicate pushdown.
- In interviews: "what are the stages of query processing?", "what does EXPLAIN show vs EXPLAIN ANALYZE?", "where do prepared statements help?"

## 4. Why Wasn't Another Approach Chosen?
- *Procedural access paths (pre-SQL, e.g., navigate manually)*: fast to optimize for one query shape but no abstraction; every new query needs hand-tuning. SQL's declarativeness + a *cost-based* optimizer is the accepted trade — you lose control but gain portability.
- *Interpret SQL directly (no plan generation)*: you'd re-parse and re-decide per row — catastrophic performance; the plan *materializes* decisions once.
- *No optimizer (run the logical plan as-is, e.g., always left-deep join in written order)*: correct but often 1000x slower than an optimized plan; cost-based planning is the industry standard.
- *Full search of all plans*: exponential (join orderings, algorithms); optimizers use pruning (dynamic programming for small N, heuristics beyond) to stay fast — correctness is preserved (all plans are equivalent *logically*), only the physical choice varies.
- *Push everything to the client*: the DB is where data + statistics live; optimizing there is the only sane choice.

## 5. Intuition
Query processing is like a **translator + strategist + field team**: the translator (parser) turns your request into an unambiguous script (AST); the strategist (planner) studies a map of the terrain (statistics) and picks a route (plan) — "take the expressway (index) rather than the scenic route (scan)"; the field team (executor) drives the route and streams passengers (rows) back. You never tell them which route — you just say "get me the customers from Amsterdam" and they pick the best one. `EXPLAIN` is asking for a copy of the route before you leave.

## 6. Real-World Analogy
**Ordering a custom PC**: the order form (SQL) lists components (tables/columns) declaratively. The shop's system (parser) reads the form and flags anything invalid (syntax/unknown part). A configurator (rewriter) applies standard packages (views, defaults). A build planner (optimizer) checks stock and compat (statistics) and assembles a *parts list + assembly order* (physical plan) — which parts to pull (scans), how to combine (joins), where to upgrade (indexes). The technicians (executor) follow the plan and hand you the machine (result set). If the planner's stock counts (statistics) are stale, the build is slow or wrong — exactly like a bad cardinality estimate.

## 7. Formal Definition
The **query processor** comprises:
- **Parser**: produces a syntax tree and a bound/annotated tree (validated against the catalog). Detects syntax and name resolution errors.
- **Rewriter/Transformer**: applies semantic transformations that preserve the query's meaning — view expansion, subquery unnesting/flattening, predicate/limit pushdown, constant folding, join reordering candidates.
- **Optimizer/Planner**: enumerates physical plans over the logical query graph, assigning a *cost* (estimated I/O + CPU, weighted) to each using catalog statistics (cardinality, selectivity, histograms), and selects the minimum-cost plan.
- **Executor**: interprets the plan tree — a composition of physical operators (Seq Scan, Index Scan, Nested Loop, Hash Join, Sort, Aggregate, etc.) — pulling tuples through the tree and returning them to the client, managing memory (work buffers), disk spill, and parallelism.

## 8. Example
Query: `SELECT c.name FROM customers c JOIN orders o ON o.customer_id = c.id WHERE o.total > 1000;`
Pipeline:
1. **Parse** → AST for SELECT with join and WHERE. Errors if `customers` doesn't exist or `o.total` isn't a column.
2. **Rewrite** → no views here; optimizer may *push the predicate* `o.total > 1000` down toward the orders scan (fewer rows join).
3. **Plan** → statistics: orders has 10M rows, customers 100K, index on orders(customer_id) and orders(total). Candidate plans: (a) Hash Join (hash customers, probe orders), (b) Merge Join (both sorted by customer_id), (c) Nested Loop (customers outer, index on orders.customer_id inner). The planner estimates: predicate selectivity ≈ 0.1% → ~10K orders; picks plan (c) or (a) — and you see the winner in `EXPLAIN`.
4. **Execute** → run the plan, stream matching rows to the client.

## 9. Internal Working
1. **Parse**: tokenize → grammar → syntax tree → *analyze* (resolve identifiers against catalogs, check types) → annotated tree.
2. **Rewrite**: apply rewrite rules recursively (views → subqueries → flatten; security policies injected; constraint exclusion can drop whole partitions).
3. **Plan**: 
   - Compute base-table access paths (seq scan, index scan, bitmap scan) with costs.
   - Generate join orders (usually left-deep for joins ≤ ~12 relations; `join_collapse_limit`/`from_collapse_limit` control search).
   - For each join, choose physical algorithm (nested loop/merge/hash) by estimated cost.
   - Handle aggregates (hash vs sort-based), sorts, window functions, `DISTINCT`, `UNION` (hash vs sort).
   - Parallel plan selection when estimated cost exceeds `parallel_setup_cost`/`parallel_tuple_cost`.
4. **Execute**: operators pull tuples (volcano model); each node buffers (hash table, sort run), and returns rows to the parent; `LIMIT` can stop early (short-circuit).
5. Resources: `work_mem` (per-operation memory; overflow → temp files), `temp_buffers`, `max_parallel_workers_per_gather`.

## 10. Time Complexity
- Parser/rewriter: O(query text / tree size) — negligible for typical queries.
- Planner: exponential in join count *in theory* (join-order enumeration); in practice bounded by pruning + limits (`join_collapse_limit`, dynamic programming for ≤ 12ish relations). Bad plans can cost *orders of magnitude* more than good ones at execution — the interesting cost is at execution, not planning.
- Executor: dominated by scan/join/sort costs (Section 02/03); a well-indexed query is O(log n) per row; a seq-scan join is O(n·m).

## 11. Advantages
- **Declarative SQL with automatic optimization**: developers write the *what*, the optimizer finds the *how*.
- **Statistics-driven**: plans adapt to data distributions (histograms) — better than static hand-tuning.
- **Portable**: the same query runs on Postgres, MySQL, Oracle — each produces its own plan.
- **Instrumentable**: `EXPLAIN`, `EXPLAIN ANALYZE`, auto-explain, `pg_stat_statements` let you inspect and correct the optimizer.
- **Safe equivalence**: rewrites preserve meaning; only the physical choice changes.

## 12. Disadvantages
- **Cost model is a model**: estimates (selectivity, cardinality) can be wildly wrong → terrible plans.
- **Planner is opaque-ish**: "why did it choose this plan?" often needs deep stats debugging.
- **Rewrite limits**: complex subqueries, CTEs (`MATERIALIZED` defaults), window functions can defeat optimization.
- **Planning cost**: very complex queries take visible planning time (mitigated by prepared statements).
- **Statistics staleness**: without `ANALYZE`/autovacuum, plans drift as data changes.

## 13. Interview Questions
1. **Q: What are the stages of query processing?** A: Parsing (SQL → AST, validated against the catalog), rewriting (views, subquery flattening, predicate pushdown, constant folding), planning/optimization (generate physical plans, estimate costs from statistics, pick the cheapest), and execution (run the plan, stream rows). `EXPLAIN` shows the plan stage; `EXPLAIN ANALYZE` runs it.
2. **Q: What's the difference between a logical and a physical query plan?** A: Logical = the relational algebra expression of what's requested (joins, selects, projections) independent of implementation. Physical = operators actually executed (Seq Scan, Index Scan, Hash Join, Sort) with an access path and ordering. The optimizer maps logical → physical, choosing among many.
3. **Q: What does the parser do vs the rewriter?** A: The parser checks syntax and resolves names/types into an annotated tree. The rewriter applies *semantic* transformations that preserve meaning: expanding views, unnesting subqueries, pushing predicates down, folding constants.
4. **Q: TRICKY: Why is parsing/planning so cheap but execution so expensive?** A: Planning is over the *query structure* (a few operators), executed once; execution is over the *data* (millions of rows), executed per row. The interesting costs — I/O, joins, sorts — are all at execution, which is why optimizer choices matter so much.
5. **Q: What is predicate pushdown?** A: Moving a `WHERE`/`JOIN` filter as close as possible to the base-table scan, so fewer rows are read and joined — e.g., `o.total > 1000` filtered at the orders scan, not after the join. It's a rewrite that dramatically cuts I/O.
6. **Q: What is a left-deep join tree?** A: A join order where each join takes the previous result and joins one more table — `((A ⋈ B) ⋈ C) ⋈ D`. It allows pipelining and simple cost evaluation; optimizers explore orders but usually stay left-deep for efficiency.
7. **Q: What does `EXPLAIN` show that `EXPLAIN ANALYZE` doesn't?** A: `EXPLAIN` shows the *estimated* plan (costs, row estimates, operators). `EXPLAIN ANALYZE` *executes* the query and shows actual timings and rows (plus buffers/loops). Compare estimate vs actual to find bad estimates.
8. **Q: PR: Why does a query run fast sometimes and slow other times with the same EXPLAIN?** A: Because the *plan* is static but the *data* (buffer cache hits, contention, locks, vacuum, parallel workers, and changed statistics) changes. Also prepared statements reuse old plans — replanning (`plan_cache_mode`) can fix it.
9. **Q: What are prepared statements and why do they help?** A: Parse+plan once, execute many times with different parameters — lower per-call overhead and more stable planning. Trade-off: parameters hide values from the planner, sometimes hurting estimates (Postgres plans with generic estimates by default for prepared statements).
10. **Q: TRICKY: Can the optimizer change the *result* of a query?** A: No — every rewrite and physical plan must be semantically equivalent for the *given* database state (including NULLs, duplicate handling, join commutativity caveats like `FULL JOIN`/`SEMI JOIN`). The risk is that equivalence depends on properties (e.g., `DISTINCT`, functional dependencies) the optimizer *assumes* — hence some rewrites are conditional.
11. **Q: What is a "Seq Scan" and when would the optimizer still choose it?** A: A sequential scan reads the whole table in order — usually bad on big tables, but chosen when (a) the table is small, (b) the query needs a large fraction of rows (selectivity high — the index would be slower), (c) no useful index exists, or (d) statistics suggest the index isn't worth it. Cost comparison, not dogma, decides.
12. **Q: What does an Index Scan buy you?** A: O(log n) lookup via the B-tree + random-access row fetch — great for selective predicates (few matching rows). The crossover vs seq scan depends on selectivity (roughly: seek+fetch wins under ~5-10% of rows for Postgres's planner).
13. **Q: PR: A complex report query takes 5 seconds to *plan*. What do you do?** A: Check `join_collapse_limit`/`from_collapse_limit` (search space), use a prepared statement or `PREPARE`, materialize expensive subqueries with CTEs deliberately, or cache the result. Planning cost is proportional to the search space the optimizer explores.
14. **Q: What is `auto_explain` / `pg_stat_statements`?** A: `auto_explain` logs plans above a duration threshold (auto_explain.log_min_duration) — the production way to find slow plans; `pg_stat_statements` aggregates query timing/plans — the first dashboard for "which queries are slow and how often."
15. **Q: TRICKY: Why does the same query produce a different plan on Postgres vs MySQL?** A: Different statistics, cost models, and algorithm choices (MySQL's optimizer vs Postgres's; different index types, `work_mem` semantics, join algorithms available). The logical result is the same; the physical plan is engine-specific — which is why "read the plan" is always engine-specific.

## 14. Follow-Up Questions
1. **Q: What is the "volcano"/"iterator" execution model?** A: Each operator exposes `open/next/close`; the parent pulls one tuple at a time from children (lazy streaming) — memory-efficient and composable. Downside: per-tuple function-call overhead (why Postgres added JIT).
2. **Q: What is parameterized/correlated plan for `IN`-subqueries?** A: The inner subquery can be planned with the outer value known (parameterized), turning a scan into a seek — a huge win the optimizer does automatically.
3. **Q: What does JIT (Postgres) do?** A: Just-in-time compilation of hot executor functions (LLVM) to cut per-tuple overhead — helps CPU-bound analytical queries, costs compilation time (so it's enabled only above `jit_above_cost`).

## 15. Coding Example
```sql
-- The four-stage pipeline, made visible
EXPLAIN (FORMAT TEXT, VERBOSE)
SELECT c.name, o.total
  FROM customers c JOIN orders o ON o.customer_id = c.id
 WHERE o.total > 1000;
-- shows: plan tree with operators, cost, rows (estimate), output columns (VERBOSE)

EXPLAIN ANALYZE
SELECT c.name, o.total
  FROM customers c JOIN orders o ON o.customer_id = c.id
 WHERE o.total > 1000;
-- executes; shows actual time, rows, loops — compare "rows" vs "actual rows"
```
```python
# Prepared statements: parse/plan once, execute many
import psycopg
with psycopg.connect("dbname=shop") as conn:
    with conn.cursor() as cur:
        cur.execute("PREPARE find_cust (int) AS SELECT name FROM customers WHERE id=$1")
        cur.execute("EXECUTE find_cust (42)")
        cur.execute("EXECUTE find_cust (7)")
        cur.execute("DEALLOCATE find_cust")
```

## 16. Industry Usage
- **PostgreSQL**: `EXPLAIN (ANALYZE, BUFFERS)`, `auto_explain`, `pg_stat_statements`, `pg_hint_plan` (plan hints), JIT. Cost params in `postgresql.conf`.
- **MySQL**: `EXPLAIN` + `EXPLAIN ANALYZE` (8.0.18+), optimizer trace (`SET optimizer_trace='enabled=on'`), `slow_query_log`.
- **Oracle/SQL Server**: `EXPLAIN PLAN`, plan guides, hinting (a mature hinting culture).
- **BigQuery/Snowflake**: serverless engines that *always* scan + columnar execution — the pipeline is the same but the cost model (bytes scanned) differs.
- Every DBA interview exercise — "explain this EXPLAIN" — exercises this pipeline.

## 17. References
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 13 (query processing) & 14 (query optimization).
- Elmasri & Navathe, Ch. 18-19.
- PostgreSQL docs, "EXPLAIN": https://www.postgresql.org/docs/current/sql-explain.html and "Performance Tips": https://www.postgresql.org/docs/current/performance-tips.html
- MySQL 8.0 docs, "EXPLAIN": https://dev.mysql.com/doc/refman/8.0/en/explain.html
- Graefe, "Query Evaluation Techniques for Large Databases" (1993) — the classic executor survey.

## 18. Cheat Sheet
- Pipeline: Parse → Rewrite → Plan (cost-based) → Execute.
- Logical plan = what; physical plan = how (operators).
- Rewrites: view expansion, subquery flattening, predicate pushdown, constant folding.
- EXPLAIN = estimates; EXPLAIN ANALYZE = actuals; compare rows vs actual rows.
- Left-deep join trees; `join_collapse_limit` bounds search.
- Seq Scan vs Index Scan: selectivity + table size decide (not dogma).
- Prepared statements: plan once, execute many (but generic estimates).
- `auto_explain` + `pg_stat_statements` = production slow-query discovery.
- Same SQL → different physical plans per engine.

## 19. Quiz
1. Correct pipeline order: a) Plan, Parse, Execute, Rewrite b) Parse, Rewrite, Plan, Execute c) Parse, Plan, Rewrite, Execute d) Rewrite, Parse, Execute → **b**
2. The optimizer's goal: a) parse faster b) cheapest estimated plan c) fewest rows d) no scans → **b**
3. Predicate pushdown moves filters: a) up b) down to scans c) to the client d) nowhere → **b**
4. EXPLAIN shows: a) actual times b) estimated costs/rows c) executed plan d) raw text → **b**
5. EXPLAIN ANALYZE: a) only plans b) executes + shows actuals c) faster d) caches → **b**
6. A left-deep join tree is: a) the only plan b) a common shape ((A⋈B)⋈C) c) illegal d) a rewrite → **b**
7. Which can make a query slow despite a good plan? a) stale stats b) contention c) buffer misses d) all of these → **d**
8. Seq Scan is chosen when: a) table huge, always b) selectivity low c) table small / high selectivity d) never → **c**

## 20. Flashcards
- **Q: Pipeline stages?** → **A:** Parse → Rewrite → Plan (optimize) → Execute.
- **Q: Logical vs physical plan?** → **A:** What you wrote (relational algebra) vs how it runs (operators + access paths).
- **Q: What is predicate pushdown?** → **A:** Pushing WHERE/JOIN filters down to base scans to cut I/O.
- **Q: EXPLAIN vs EXPLAIN ANALYZE?** → **A:** Estimated plan vs executed plan with actuals.
- **Q: Why is planning cheap but execution expensive?** → **A:** Planning is over query structure (once); execution is over data (per row).
- **Q: When does the optimizer choose a Seq Scan?** → **A:** Small table, high selectivity, or no useful index.
- **Q: What are prepared statements?** → **A:** Parse+plan once, execute with params — lower overhead, sometimes stale estimates.
- **Q: How do you find slow queries in production?** → **A:** auto_explain + pg_stat_statements + slow query log.

## 21. Revision
SQL → AST (parse) → semantic tree (rewrite: views, pushdown, flatten) → physical plan (optimize: generate + cost from stats + pick cheapest) → execute (stream rows). Cost model is *estimates* — compare EXPLAIN (estimated) vs EXPLAIN ANALYZE (actual). Left-deep joins, `join_collapse_limit`. Seq Scan vs Index Scan = selectivity + size decision. Prepared statements, auto_explain, pg_stat_statements are the ops tools. Every "why slow?" answer starts at the pipeline and its estimates.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Stages of query processing?" | 1, 2, 8 |
| "Logical vs physical plan?" | 7, 13 |
| "What is predicate pushdown?" | 2, 8, 13 |
| "EXPLAIN vs EXPLAIN ANALYZE?" | 9, 13 |
| "When is a Seq Scan chosen?" | 13, 18 |
| "Why do prepared statements help?" | 3, 13 |
| "Why is this query slow?" | 9, 13, 14 |
| "How do you find slow queries in prod?" | 13, 16 |
