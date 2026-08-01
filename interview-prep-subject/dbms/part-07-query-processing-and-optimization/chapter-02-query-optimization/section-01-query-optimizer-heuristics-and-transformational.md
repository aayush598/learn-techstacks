# Query Optimizer: Heuristics and Transformations

> **TL;DR**: The optimizer searches a huge space of semantically-equivalent plans using dynamic programming (for small queries) plus heuristics (to bound the search), applying algebraic transformation rules — join reordering, predicate pushdown, subquery unnesting — to reshape the logical query before costing physical plans.

## 1. Why Does This Exist?
The number of logically-equivalent plans for a join of N tables is enormous: N! join orders × algorithm choices × access paths. Evaluating every plan by cost is impossible for large N. The optimizer exists to make a *good-enough, near-optimal* choice quickly: it (a) *transforms* the logical query into better shapes via proven algebraic rules (transformational optimization), and (b) *searches* the remaining plan space using cost estimation with pruning (heuristic optimization). It exists because naive execution (the written join order, naive scans) is often orders of magnitude slower than what a good optimizer finds — so the optimizer is the difference between a usable SQL database and a toy.

## 2. How Does It Work?
Two complementary layers:
- **Transformational (rewrite-based) optimization**: apply equivalence-preserving rules to the logical tree *before* costing — e.g., `SELECT` projection pushdown, predicate (WHERE/JOIN) pushdown, subquery unnesting (`EXISTS`→semi-join, `IN`→join), view merging, `DISTINCT`/`GROUP BY`/`ORDER BY` simplification, outer-join to inner-join when NULLs provably don't matter, constant folding.
- **Cost-based search**: for the transformed query, enumerate candidate physical plans — join orders (via dynamic programming on the join graph for small N, heuristic orders beyond), access paths (seq/index/bitmap), join algorithms (NLJ/merge/hash), aggregation strategies (hash vs sort) — and pick the minimum estimated cost. Search-space controls: `from_collapse_limit`/`join_collapse_limit` (Postgres) bound the reordering search; `geqo` (genetic optimizer) kicks in above ~12 relations.

## 3. When Is It Used?
- Every query at plan time; the transformation layer runs even before costing (so `EXPLAIN` output reflects the *transformed* query, not the written one).
- **Prepared statements**: the same transformation/search runs once per plan; generic vs custom plans matter (Postgres).
- **View/materialized views**: view expansion is a transformation; `GROUP BY` pushdown through views can be a huge win.
- **Partition pruning**: predicates pushed to partitioned tables prune partitions at plan time — a transformation with big I/O effects.
- In interviews: "what transformations does the optimizer apply?", "how does the optimizer search plan space?", "why would the optimizer rewrite my query?", "what is `join_collapse_limit`?"

## 4. Why Wasn't Another Approach Chosen?
- *Exhaustive search of all plans*: provably optimal but factorial — infeasible above ~10-12 joins. Dynamic programming bounds it (optimal for a subset size, reuse), and `geqo` handles the extreme.
- *Pure rule-based (no costing)*: fast but blind — can't adapt to data; the industry moved to cost-based for a reason (Section 03 of Chapter 01).
- *Only local rules, no cross-query search*: transformation without costing misses the physical choice (join algorithm, index); search without transformation misses the logical reshaping. Real optimizers combine both.
- *Push all optimization to the developer (explicit hints/order)*: fragile, non-portable, and error-prone — that's what `JOIN ... ` written order would mean. Hints exist but as *controls*, not the primary mechanism.
- *Optimize at execution (adaptive)*: some engines add runtime adaptation, but it can't replace planning — plan-level decisions (sorts, builds) must be made before data flows.

## 5. Intuition
Think of the optimizer as a **chef planning a dinner from one pantry**. The "transformations" are rearranging the recipe for efficiency without changing the dish: sear the mushrooms first (predicate pushdown — reduce what you handle later), merge two steps (join reordering — the smaller pan first), substitute pre-chopped ingredients (index on the go). The "search" is trying out a few credible sequences (dynamic programming remembers the best prefix; heuristics cut the search when the pantry is huge) and picking the one with the least total effort (cost). You never taste-test every possible ordering of 20 dishes — you use expertise (rules) plus a few smart comparisons (cost) and ship.

## 6. Real-World Analogy
A **delivery dispatcher consolidating a day's routes**: the naive plan (written order) might be "drive to A, then B, then C, then back" — the *transformation* step notices you can reorder (visit C before B) and drop unneeded stops (predicate pushdown: skip orders already cancelled). The *search* step then compares "one big loop" vs "two smaller loops" vs "one driver with a truck (hash join)" and picks the cheapest *estimated* route. If there are only 8 stops, it can enumerate most orderings (dynamic programming); with 30 stops, it uses heuristics (closest-next). The dispatcher's rules guarantee the *delivered parcels* are identical either way — only efficiency changes.

## 7. Formal Definition
**Transformational optimization**: the set of equivalence-preserving algebraic rewrites applied to a relational-algebra/logical plan. Canonical rules include: predicate pushdown (σ onto the smallest input as early as possible), projection pushdown (reduce columns earlier), join reordering (commutativity/associativity of ⋈), subquery unnesting (turn `r WHERE EXISTS(SELECT...)` into a semi-join), view merging, `GROUP BY`/`DISTINCT` pushdown, and outer-to-inner join conversion when outer-join null-extension can't be observed.
**Cost-based (heuristic) search**: given the transformed logical plan, enumerate physical plans (join orders, algorithms, access paths); compute estimated cost (Ch. 1 §3); choose minimum. Bounded by: dynamic programming over the join graph with subset enumeration (optimal for the enumerated subspace), `from_collapse_limit`/`join_collapse_limit` limiting how many relations are reordered, and (Postgres) `geqo` genetic search beyond that threshold.

## 8. Example
Written query:
```sql
SELECT c.name FROM orders o
  JOIN customers c ON c.id = o.customer_id
  JOIN items i ON i.id = o.item_id
 WHERE i.category = 'electronics' AND o.amount > 1000;
```
Transformations:
1. **Predicate pushdown**: `i.category='electronics'` is pushed to the `items` scan; `o.amount>1000` pushed to `orders` — the joins then see far fewer rows.
2. **Join reordering**: the planner may join `items` and `orders` first (if `category` is selective, making that pair small) rather than the written order (`orders ⋈ customers` first).
3. **Projection pushdown**: only `c.name`, `o.amount`, `i.id`/keys are needed — scans fetch fewer columns (or use covering indexes).
4. **Subquery unnesting** (if the query used `EXISTS`): converted to a semi-join, allowing hash/merge semi-join execution.
Then the cost-based search picks join algorithms (hash vs NLJ) and access paths (seq vs index on `i.category`, `o.customer_id`), minimizing estimated cost. `EXPLAIN` shows the *final* physical plan — you can see the pushdowns happened (filters at the scans).

## 9. Internal Working
1. **Parse/rewrite** → logical plan.
2. **Transformation pass**: apply equivalence rules in a fixed/priority order (Postgres: `planner.c` handles `preprocess_expression` — flattening, subquery pull-up, `placeholders`, `simplify`; `query_planner` considers join orders).
3. **Search**: 
   - Build a join graph; enumerate subsets via dynamic programming (Postgres: `join_search_one_level`, memoization of cheapest plan per relation subset) up to `join_collapse_limit` (default 8) / `from_collapse_limit` (default 8).
   - Beyond the limit: `geqo` (genetic algorithm) or a simpler greedy order.
   - For each join node, add candidate paths (hash/merge/NLJ, inner/outer swapped) and each base relation gets access paths (seq, index, bitmap).
   - Cost each; prune dominated paths (a path that is slower *and* returns no extra useful ordering is discarded — "cheapest path with useful ordering" bookkeeping).
4. **Output**: the cheapest complete tree → executor plan. Cost parameters (`enable_seqscan`, etc.) act as *filters* (debug) not weights.

## 10. Time Complexity
- Transformations: O(plan size) per rule; typically small.
- Dynamic-programming join search: O(2^N) subsets in the worst case for N relations — fine for N ≤ 10-12, hence `join_collapse_limit`; `geqo` treats larger N with a genetic search (bounded population/iterations).
- Path generation per node: O(access paths × algorithms) — small constants.
- Result: near-optimal plans in milliseconds for typical queries; the *value* is that execution cost dominates planning by orders of magnitude.

## 11. Advantages
- **Near-optimal plans automatically**: transforms + costing find plans humans rarely write by hand.
- **Semantic safety**: rules are equivalence-preserving (with documented caveats), so optimization never changes results.
- **Adaptive to data**: the same query optimizes differently as statistics change.
- **Bounded search**: limits (`join_collapse_limit`, geqo) keep planning fast even for pathological queries.
- **Observable/tunable**: `EXPLAIN` + flags/hints give operators control.

## 12. Disadvantages
- **Search heuristics can miss the global optimum** (especially >12 joins, or geqo).
- **Transformation assumptions** (e.g., outer-join conversion, subquery equivalence) occasionally *fail* or change behavior (NULL semantics) — subtle bugs historically.
- **`from_collapse_limit` trade-off**: raising it can slow planning; lowering it can miss good orders.
- **Opaque to users**: "why this order?" needs deep knowledge; hints are engine-specific.
- **Cost-estimation errors** undermine the search (Ch. 1 §3) — the optimizer can *correctly* pick a plan that's wrong because the input estimates are wrong.

## 13. Interview Questions
1. **Q: What is transformational optimization?** A: Rewriting the logical query with equivalence-preserving rules — predicate/projection pushdown, join reordering, subquery unnesting, view merging — to produce a better-shaped tree *before* costing. It changes the plan shape but never the result.
2. **Q: Give examples of transformation rules.** A: Predicate pushdown (filters earlier), projection pushdown (fewer columns), join commutativity/associativity (reorder), subquery unnesting (`EXISTS`→semi-join), outer→inner join conversion (when safe), `DISTINCT`/`GROUP BY` pushdown, constant folding.
3. **Q: What is predicate pushdown and why is it so valuable?** A: Moving `WHERE`/`JOIN` filters down to the base scans so each operator processes fewer rows — it can reduce a join's input by orders of magnitude and enable index selection at the scan.
4. **Q: How does the optimizer search join orders?** A: It models joins as a graph and uses dynamic programming (enumerate relation subsets, keep the cheapest plan per subset) — optimal within the search space. Limits: `join_collapse_limit` (default 8) bounds reordering; beyond it, `geqo` (genetic) or a greedy order.
5. **Q: What is `join_collapse_limit`?** A: The maximum number of `JOIN` items the optimizer will reorder (Postgres default 8). Above it, join order is left as written (or via geqo). Raising it explores more plans (slower planning, possibly better plans); lowering it cuts planning time.
6. **Q: TRICKY: Why does the optimizer rewrite `EXISTS` into a semi-join?** A: Because semi-join has dedicated physical algorithms (hash/merge semi-join) and can stop after the first match per outer row — far cheaper than a correlated subquery scan per row. The rewrite is a *logical* equivalence; execution reaps the win.
7. **Q: What is subquery unnesting (flattening)?** A: Converting a subquery in `WHERE`/`FROM` into a join — e.g., `WHERE EXISTS(SELECT 1 FROM o WHERE o.c=... )` becomes a semi-join; `WHERE x IN (SELECT ...)` becomes a join. This unlocks join algorithms. `FROM` subqueries are merged when safe (`subquery_planner`).
8. **Q: When would the optimizer NOT flatten a subquery?** A: When flattening changes semantics (LIMIT/OFFSET inside, aggregates/`DISTINCT` that change cardinality, set operations) — the cost model must keep correctness. Postgres materializes such subqueries instead.
9. **Q: What is outer-join to inner-join conversion?** A: Rewriting `LEFT JOIN` into `INNER JOIN` when the optimizer can prove the right side can't add NULL rows (e.g., a `WHERE` predicate on the right side rejects NULLs, or a PK/FK constraint guarantees a match). It unlocks more join orders and algorithms.
10. **Q: What is the difference between heuristics and cost-based optimization?** A: Heuristics = fixed rules that always apply (pushdown, unnest) regardless of data. Cost-based = choose among alternatives by estimated cost from statistics. Real optimizers use both: heuristics to reshape, cost to pick among physical alternatives.
11. **Q: PR: Why would my query run better if I reorder the joins myself?** A: Usually it won't matter — the optimizer reorders for you (within limits). If it *does* matter, either the query exceeds `join_collapse_limit` (so reordering is disabled), or estimates are wrong (fix stats), or you're hitting a geqo plan. Write clean SQL; let the optimizer work; intervene only with evidence.
12. **Q: What is the genetic query optimizer (geqo)?** A: Postgres's heuristic search for large join sets (≥ `geqo_threshold`, default 12): a genetic algorithm explores join orders without enumerating all subsets. It produces good (not guaranteed-optimal) plans quickly — for the few pathological >12-table queries.
13. **Q: TRICKY: Can transformation rules change query results?** A: Only if a rule's equivalence *assumption* is violated (e.g., converting outer to inner when NULLs could leak, or flattening a subquery whose `LIMIT` changes semantics). Optimizers are conservative: they only apply rules whose preconditions (constraints, NULL-ability, cardinality) they can prove — which is why some rewrites are conditional.
14. **Q: What is "projection pushdown"?** A: Reducing the set of columns each operator carries (only what the query needs) as early as possible — smaller tuples, better page locality, and the enabler of *covering indexes*. Visible when EXPLAIN shows "Output" columns filtered at scans.
15. **Q: PRODUCTION: How do you know the optimizer did a good job?** A: `EXPLAIN ANALYZE`: estimated rows ≈ actual rows at every node, sensible algorithm choices, no unexpected Seq Scans on big tables, no spills. If actuals diverge from estimates, the *inputs* to the search (statistics) are wrong — fix those before touching hints.

## 14. Follow-Up Questions
1. **Q: What is a "path" in Postgres?** A: A candidate physical access method (seq scan, index scan, parameterized path, etc.) with its cost and ordering; the planner keeps the cheapest path (and cheapest with each useful ordering) per relation, then builds joins from paths. "Cheapest path" bookkeeping is the DP core.
2. **Q: What does `ORDER BY` pushdown / "useful ordering" mean?** A: If a path already provides the needed sort order (index on the ORDER BY key), no explicit Sort node is needed — the optimizer tracks "useful orderings" per path and prefers them.
3. **Q: How does partition pruning interact with transformations?** A: Predicates pushed to a partitioned table's scans let the planner *prune* whole partitions at plan time (a form of predicate pushdown + constraint exclusion) — only the relevant partitions are scanned.

## 15. Coding Example
```sql
-- See the transformed plan: note filters at scans (pushdown) and join order
EXPLAIN (ANALYZE, VERBOSE)
SELECT c.name FROM orders o
  JOIN customers c ON c.id = o.customer_id
  JOIN items i ON i.id = o.item_id
 WHERE i.category = 'electronics' AND o.amount > 1000;
-- Note: "Filter: (i.category='electronics')" near the items scan
--       "Filter: (o.amount>1000)" near the orders scan → pushdown happened

-- Bounding the search space
SHOW join_collapse_limit;   -- 8
SHOW geqo_threshold;        -- 12
SET join_collapse_limit = 16;  -- let the optimizer reorder more (slower planning)
```
```sql
-- Subquery unnesting visible: EXISTS → Hash Semi Join
EXPLAIN
SELECT c.id FROM customers c
 WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id AND o.amount > 100);
-- Output: "Hash Semi Join" (not a correlated scan) — the rewrite happened
```

## 16. Industry Usage
- **PostgreSQL**: transformations in `planner.c`/`subselect.c`; dynamic programming join search with `join_collapse_limit`; `geqo`; `pg_hint_plan` for explicit control.
- **MySQL 8.0**: cost-based optimizer with subquery-to-semi-join transformations, `range`/`ref` access, `optimizer_switch` knobs, `EXPLAIN FORMAT=JSON` (the optimizer trace).
- **SQL Server**: cost-based + query hints; dynamic management views show the chosen plan; `OPTION (RECOMPILE)` avoids stale generic plans.
- **Oracle**: rule→cost-based history; `DBMS_XPLAN`; join method/order hints (a rich hinting culture).
- **BigQuery/Snowflake**: columnar engines with their own transformation/search (often query *compile* + DAG execution), e.g., predicate pushdown into storage/partition pruning — same principles at warehouse scale.

## 17. References
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 14 (optimization: transformations, join ordering, heuristics).
- Elmasri & Navathe, Ch. 19.
- Selinger et al., "Access Path Selection in a Relational Database Management System" (1979) — the foundational cost/search paper.
- PostgreSQL docs, "Planner/Optimizer": https://www.postgresql.org/docs/current/planner-optimizer.html and "When To Use Custom Settings" / `geqo`: https://www.postgresql.org/docs/current/runtime-config-query.html
- PostgreSQL source: `src/backend/optimizer/plan/planner.c`, `joinpath.c`.

## 18. Cheat Sheet
- Two layers: transformations (logical reshapes, semantics-preserving) + cost-based search (physical choice).
- Key transforms: predicate/projection pushdown, join reordering, subquery unnesting (→ semi-join), outer→inner conversion, view merging, constant folding.
- Search: DP over join subsets (optimal in subspace), `join_collapse_limit`=8 bounds reordering; `geqo` above 12 relations.
- `EXISTS`/`IN` → semi-join → hash/merge semi-join (stop at first match).
- Keep clean SQL; the optimizer reorders. Fix *statistics*, not hints, when plans are wrong.
- `enable_*` flags are debug switches, not tuning.
- "Useful ordering" tracking avoids explicit Sort nodes.
- Partition pruning = constraint exclusion at plan time.

## 19. Quiz
1. Which is a transformation rule? a) hash join b) predicate pushdown c) seq scan d) work_mem → **b**
2. The DP join search enumerates: a) all tables b) relation subsets c) columns d) rows → **b**
3. `EXISTS` is typically rewritten into: a) a cartesian product b) a semi-join c) a union d) a view → **b**
4. `join_collapse_limit` bounds: a) join algorithms b) reordering search c) memory d) statistics → **b**
5. Outer→inner conversion requires proving: a) no duplicates b) no NULLs can leak c) sorted keys d) equality → **b**
6. geqo is used for: a) small queries b) >12 relations c) INSERT d) DDL → **b**
7. Which could change results if misapplied? a) pushdown b) outer→inner without proof c) projection d) folding → **b**
8. A "path" in Postgres is: a) a query plan b) a candidate access method with cost c) a file path d) an index → **b**

## 20. Flashcards
- **Q: Two optimizer layers?** → **A:** Transformations (logical reshapes) + cost-based search (physical choices).
- **Q: Name 4 transformation rules.** → **A:** Predicate pushdown, projection pushdown, join reordering, subquery unnesting.
- **Q: What is `EXISTS` rewritten to?** → **A:** A semi-join (hash/merge semi-join, stops at first match).
- **Q: What bounds the search?** → **A:** `join_collapse_limit` (8) and geqo above 12 relations.
- **Q: When is outer→inner safe?** → **A:** When the optimizer proves NULLs can't leak (constraints/predicates).
- **Q: What is a semi-join?** → **A:** Returns outer rows that have a match, without duplicating on multiple matches.
- **Q: How do you verify the optimizer's work?** → **A:** EXPLAIN ANALYZE — estimated vs actual rows.
- **Q: enable_* flags are for?** → **A:** Debugging (forcing/forbidding operators), not production tuning.

## 21. Revision
Optimizer = transformations (pushdown, unnest, reorder, outer→inner) that reshape the logical tree safely + cost-based search (DP over join subsets, `join_collapse_limit`=8, geqo >12) that picks physical plans. `EXISTS`→semi-join is the canonical rewrite. Keep SQL clean; when plans look wrong, suspect statistics, not the optimizer — verify with EXPLAIN ANALYZE. This is the "why" behind every EXPLAIN plan you'll read in Section 02.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is transformational optimization?" | 1, 2, 7 |
| "Give transformation rule examples." | 2, 8, 13 |
| "How does the optimizer search join orders?" | 2, 9, 13 |
| "What is join_collapse_limit / geqo?" | 9, 13 |
| "Why does EXISTS become a semi-join?" | 8, 13 |
| "When is outer→inner conversion safe?" | 13, 14 |
| "Can transformations change results?" | 13 |
| "How do you know the plan is good?" | 13, 15 |
