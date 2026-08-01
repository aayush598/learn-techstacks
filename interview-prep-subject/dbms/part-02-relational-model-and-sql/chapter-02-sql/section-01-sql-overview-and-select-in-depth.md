# SQL Overview and SELECT in Depth

> **TL;DR**: SELECT is processed in a fixed logical order — FROM → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT — and NULL/three-valued logic decide everything else; internalize the order and every SQL question becomes deterministic.

## 1. Why Does This Exist?
SQL is the interface through which *all* relational data work happens, and `SELECT` is the statement people write thousands of times. This section exists because most SQL bugs are *order bugs*: writing a filter that must run after grouping (`HAVING`) in `WHERE`, expecting column aliases to be usable in `WHERE`, or assuming `LIMIT` runs before `ORDER BY`. The logical execution order is the single highest-leverage fact in SQL — it explains why every clause behaves the way it does, why aliases work only in certain clauses, and why two apparently identical queries can return different results. Know the order, and you stop "trying things" and start *predicting*.

## 2. How Does It Work?
Every SELECT (conceptually) runs in this order:
1. **FROM** — build the working set (tables + joins; CROSS then ON).
2. **WHERE** — filter rows (predicate per row).
3. **GROUP BY** — collapse rows into groups.
4. **HAVING** — filter groups (aggregate-friendly).
5. **SELECT** — compute expressions, aliases (aliases born here!).
6. **DISTINCT** — deduplicate result rows.
7. **ORDER BY** — sort (can use aliases; also `NULLS FIRST/LAST`).
8. **LIMIT/OFFSET** — cut rows (after ORDER BY).
This is *logical* order (what the result means), not physical — the engine reorders for speed, but must produce the same result. NULLs use **three-valued logic**: comparisons with NULL are UNKNOWN, `WHERE` keeps only TRUE, so NULLs silently disappear unless handled (`IS NULL`, `COALESCE`).

## 3. When Is It Used?
- **Every read query** — this is the anatomy all production SQL follows.
- **Debugging**: "why is my row missing?" is almost always a WHERE-vs-HAVING, join-vs-filter, or NULL-logic issue — the order explains each.
- **Writing correct analytics**: `LIMIT` after `ORDER BY` (top-N), `HAVING` after `GROUP BY` (min group size), aliases only in ORDER BY/SELECT.
- **Optimizing**: knowing the order tells you where filters bind (filter in WHERE runs before GROUP BY = cheaper) and guides index design.
- **Interview screens**: "write a query that returns ..." — everything hangs on this order.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: let clauses run in any order (no defined pipeline).** Rejected: results would be ambiguous and un-portable; a *fixed logical order* is the contract that makes SQL deterministic across engines.
- **Alternative: make `WHERE` able to reference aggregates (merge HAVING into WHERE).** Rejected: `WHERE` runs pre-grouping — it can't know aggregates. Keeping them separate is why `HAVING` exists; conflating them would create an inconsistent pipeline.
- **Alternative: make `SELECT` aliases available everywhere.** Rejected: aliases are *defined* in SELECT (step 5), so earlier clauses (WHERE, GROUP BY, HAVING) can't see them — referencing a column by a name that doesn't exist yet would be order-violating. (Postgres even allows `ORDER BY alias` and `GROUP BY alias` by design; MySQL is looser with HAVING aliases — vendor quirks.)
- **Why three-valued logic?** Missing data is real; `NULL` = unknown is the honest representation. Two-valued logic would force a lie ("does this NULL equal 5? → false"). 3VL is the cost of truthfully handling unknown values.

## 5. Intuition
Think of SELECT as a **factory assembly line**: parts (rows) come in FROM the warehouse; a quality gate (WHERE) discards defective parts; a packaging machine (GROUP BY) bundles them; an inspector (HAVING) rejects bad bundles; the label printer (SELECT) writes what's on the box; a duplicate-checker (DISTINCT) removes repeated boxes; a conveyor (ORDER BY) lines them up; and a take-away truck (LIMIT) picks only the first few. You cannot inspect bundles (HAVING) before they're bundled (GROUP BY), and you can't label (SELECT alias) before packaging. The line's order is the pipeline — follow it and every query makes sense.

## 6. Real-World Analogy
A **restaurant order process**: FROM = read the entire kitchen stock; WHERE = use only today's fresh ingredients; GROUP BY = sort dishes by course (starters/mains/desserts); HAVING = keep only courses with at least 3 dishes; SELECT = print just dish names and prices; ORDER BY = arrange the menu by price; LIMIT = show only the 5 cheapest dishes. The chef can't "keep only courses with 3+ dishes" (HAVING) before grouping dishes into courses (GROUP BY) — same constraint, same order. Following the steps in sequence yields the exact menu every time.

## 7. Formal Definition
The SQL `SELECT` statement's **logical processing order** (ISO/IEC 9075 semantics): (1) FROM clause — computes the cross product of table sources, then applies JOIN ON conditions; (2) WHERE clause — filters rows by predicate (true only; UNKNOWN rows removed); (3) GROUP BY clause — partitions surviving rows into groups; (4) HAVING clause — filters groups by predicate (may use aggregates); (5) SELECT clause — evaluates target list expressions, assigning aliases; (6) DISTINCT — eliminates duplicate output rows; (7) ORDER BY — sorts output (may reference aliases and non-selected expressions); (8) LIMIT/OFFSET — restricts the returned row count. NULL semantics follow **three-valued logic**: TRUE/FALSE/UNKNOWN, where comparisons with NULL yield UNKNOWN, and `WHERE`/`HAVING` accept only TRUE. (PostgreSQL docs, SQL standard.)

## 8. Example
Schema: `students(sid, name, dept, gpa)`. Data:
```
(1,Alice,CS,3.8),(2,Bob,EE,3.2),(3,Cara,CS,NULL),(4,Dan,EE,2.9)
```
Query: `SELECT dept, AVG(gpa) AS avg FROM students WHERE gpa IS NOT NULL GROUP BY dept HAVING COUNT(*) >= 1 ORDER BY avg DESC LIMIT 1;`
Step-by-step:
1. FROM: all 4 rows.
2. WHERE `gpa IS NOT NULL`: keep (1),(2),(4) — **Cara (NULL) dropped**.
3. GROUP BY dept: {CS: [3.8]}, {EE: [3.2, 2.9]}.
4. HAVING count≥1: both groups pass.
5. SELECT: CS→avg 3.80; EE→avg 3.05.
6. DISTINCT: nothing to dedupe.
7. ORDER BY avg DESC: [3.80, 3.05].
8. LIMIT 1: → `(CS, 3.80)`.
The result is deterministic *because the order is fixed* — and Cara's NULL never entered the aggregation.

## 9. Internal Working
1. **Parse** into a query tree; validate names/types against catalog.
2. **Rewrite**: flatten subqueries, expand views, push predicates.
3. **Plan**: the optimizer reorders *physical* execution (e.g., push WHERE into index scan, join reorder) while *guaranteeing* the logical order's result — the logical order is the contract; the plan is a faster way to meet it.
4. **Execute**: operators (SeqScan/IndexScan apply WHERE; HashAggregate implements GROUP BY+HAVING; Sort implements ORDER BY; Limit stops early).
5. **Efficiency note**: because WHERE runs before GROUP BY, a predicate like `WHERE dept='CS'` reduces the rows the aggregator sees — plan quality depends on filter placement, which the optimizer exploits (σ push-down).

## 10. Time Complexity
- **Full query**: dominated by the most expensive operator — scan O(n), index seek O(log n + k), hash aggregate O(n), sort O(n log n).
- **Ordering comparisons**: ORDER BY = O(n log n) (or O(k log k) with LIMIT via top-k heap → O(n log k)).
- **DISTINCT**: O(n) hash or O(n log n) sort.
- **GROUP BY**: O(n) hash aggregate (no sort needed) or O(n log n) sort aggregate.
- **HAVING**: O(#groups) after aggregation.
- **LIMIT**: O(k) truncation — but it runs *after* ORDER BY, so "top-K" still sorts first (unless an index provides order).

## 11. Advantages
- **Deterministic semantics**: the fixed order makes results predictable and portable across engines.
- **Declarative power**: express multi-stage logic (filter→group→filter→sort→limit) in one statement.
- **Optimization freedom**: the engine can reorder physically while honoring logical order — cost-free correctness.
- **Three-valued logic honesty**: NULLs are handled explicitly (`IS NULL`, `COALESCE`), avoiding silent wrongness.
- **Composable**: SELECTs nest (subqueries, CTEs) because the pipeline can be re-run on intermediate results.

## 12. Disadvantages
- **Logical order ≠ written order**: beginners read left-to-right and get confused (alias in WHERE, aggregate in WHERE).
- **NULLs are silent**: `WHERE gpa > 3.5` quietly drops NULL-GPA students; the "missing row" bug is endemic.
- **Bag vs set**: DISTINCT is manual; `LIMIT` before/after sort confusion.
- **Vendor quirks**: MySQL allows aliases in HAVING/GROUP BY, Postgres in GROUP BY/ORDER BY — portability traps.
- **No position logic**: without ORDER BY, LIMIT picks arbitrary rows — a classic "nondeterministic top-N" bug.

## 13. Interview Questions
1. **Q: What is the logical execution order of a SELECT?** A: FROM (joins) → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT/OFFSET. This is the semantic contract; the engine may reorder physically but must return the same result.
2. **Q: Why can't you use an alias from SELECT in WHERE?** A: WHERE runs *before* SELECT — the alias doesn't exist yet. You can use it in ORDER BY (and in GROUP BY/HAVING in some engines), because those run after SELECT (or allow re-reference).
3. **Q: Why does `WHERE COUNT(*) > 5` fail?** A: WHERE runs before grouping, so no aggregates exist yet. Filtering groups is HAVING's job: `HAVING COUNT(*) > 5`. WHERE filters *rows*; HAVING filters *groups*.
4. **Q: What is three-valued logic?** A: SQL predicates evaluate to TRUE, FALSE, or UNKNOWN. Any comparison with NULL is UNKNOWN; WHERE/HAVING keep only TRUE rows — so UNKNOWN rows (and FALSE) are dropped. That's why `gpa > 3.5` removes NULL-GPA rows.
5. **Q (tricky): `WHERE name <> 'Alice'` — does it return NULL names?** A: No. `NULL <> 'Alice'` is UNKNOWN, and WHERE keeps only TRUE — NULL names silently vanish. To include them: `WHERE name <> 'Alice' OR name IS NULL`.
6. **Q: Does LIMIT run before or after ORDER BY?** A: After. The order is ...ORDER BY → LIMIT. So `LIMIT 3` means "first 3 of the *sorted* result". Without ORDER BY, LIMIT picks arbitrary rows — never rely on it without ORDER BY.
7. **Q (production): "Top 5 products by revenue" — what's the optimal plan?** A: With an index on revenue it's an index scan in order + early stop (O(n log k)); otherwise a full sort O(n log n) then LIMIT. In either case the query text is `SELECT ... ORDER BY revenue DESC LIMIT 5`.
8. **Q: What's the difference between WHERE and HAVING?** A: WHERE filters rows *before* grouping (no aggregates allowed, cheap). HAVING filters groups *after* grouping (aggregates allowed). Same predicate can be expressed both ways when it's about columns — but the row-filter version is cheaper.
9. **Q (tricky): `SELECT DISTINCT a, b FROM t ORDER BY a` — legal?** A: Yes — DISTINCT applies to (a,b) pairs; ORDER BY may reference any selected expression (Postgres requires ORDER BY expressions to be in SELECT for DISTINCT queries). Ordering by a non-selected column with DISTINCT is illegal.
10. **Q: What does `COALESCE(a, b, 0)` do?** A: Returns the first non-NULL argument in order; `COALESCE(NULL, 5, 0)` = 5. It's the standard NULL-default idiom (vs `IFNULL`/`NVL`, vendor names).
11. **Q: How does GROUP BY interact with non-aggregated columns?** A: Every column in the SELECT list that isn't aggregated must appear in GROUP BY (strict standard; Postgres enforces, MySQL's ONLY_FULL_GROUP_BY too). Otherwise the value per group is ambiguous — the classic "pick an arbitrary row" bug.
12. **Q (scenario): Write a query for the department with the highest average GPA.** A: `SELECT dept, AVG(gpa) avg FROM students GROUP BY dept ORDER BY avg DESC LIMIT 1;` (order: group → order → limit). Edge case: ties — LIMIT picks one arbitrarily; use a window/RANK for ties.
13. **Q: What is `IS NULL` vs `= NULL`?** A: `= NULL` is always UNKNOWN (never TRUE) — it matches nothing. `IS NULL` is the correct null test. This is the single most common NULL bug.
14. **Q (tricky): Can ORDER BY reference an expression not in SELECT?** A: Yes — `ORDER BY gpa DESC` works even if SELECT lists only name. ORDER BY can use columns, expressions, and (in Postgres) output-column positions. Aliases are allowed because ORDER BY is step 7.
15. **Q: What's the difference between DISTINCT and GROUP BY?** A: Both dedupe, but GROUP BY also *aggregates* and produces one row per group (with aggregates you can compute per-group stats); DISTINCT only removes duplicate rows. `SELECT DISTINCT dept FROM t` ≡ `SELECT dept FROM t GROUP BY dept`.
16. **Q (production): Why does adding DISTINCT make a query slow?** A: Dedup requires a hash table or sort over the result (O(n) memory / O(n log n) sort). If your data has no duplicates, DISTINCT is pure waste — verify with a COUNT first.
17. **Q: What is the difference between `ORDER BY` and default table order?** A: Tables have *no guaranteed order* (sets). `ORDER BY` is the only way to get a deterministic order. Default order is whatever the scan produces — never assumed, always brittle.
18. **Q: What does `OFFSET` do and why is it risky?** A: It skips N rows after ORDER BY — used for pagination (`LIMIT 10 OFFSET 20`). Risky because (a) it rescans skipped rows each page (slow on big offsets) and (b) new rows during pagination shift pages. Prefer keyset pagination (`WHERE id > last_id ORDER BY id LIMIT 10`).
19. **Q (hard): `SELECT COUNT(*)` vs `COUNT(col)` vs `COUNT(DISTINCT col)`?** A: `COUNT(*)` counts all rows (including NULLs everywhere); `COUNT(col)` counts non-NULL values of col only; `COUNT(DISTINCT col)` counts distinct non-NULL values. NULL behavior differs — know it precisely.
20. **Q: When does the optimizer ignore your query's written order?** A: Always, physically — it reorders joins, pushes filters, and may use an index that reads in sorted order (satisfying ORDER BY free of cost). But the *result* must match the logical order — that's the guarantee.

## 14. Follow-Up Questions
1. **Q: Can you reference a column by position in ORDER BY?** A: Yes — `ORDER BY 2` sorts by the 2nd selected column (legacy SQL; frowned upon). Never use positions in production; aliases are clearer.
2. **Q: What is `NULLS FIRST/LAST`?** A: Control where NULLs sort: `ORDER BY gpa DESC NULLS LAST` (Postgres/Oracle/SQL Server 2019+; MySQL lacks it — NULLs sort first ascending). Vendor quirk worth naming.
3. **Q: Does GROUP BY sort output?** A: Not guaranteed — hash aggregation returns unsorted groups. If you need order, add ORDER BY. (Sort-based aggregate happens to sort, but it's not a contract.)
4. **Q: Why is `WHERE dept='CS'` faster than `HAVING dept='CS'`?** A: WHERE filters rows before grouping (fewer rows aggregated); HAVING filters after grouping (still aggregated everything). When the predicate is row-level, prefer WHERE.
5. **Q: What is a "deterministic" query?** A: One whose result doesn't change across runs given the same data — ensured by ORDER BY + deterministic functions. `now()`, `random()`, `uuid_generate` are non-deterministic; they break idempotent reasoning.

## 15. Coding Example
```sql
-- The execution order, clause by clause
SELECT   dept, COUNT(*) AS n, AVG(gpa) AS avg_gpa   -- 5: compute + alias
FROM     students                                    -- 1: sources
WHERE    gpa IS NOT NULL                             -- 2: filter rows
GROUP BY dept                                        -- 3: form groups
HAVING   COUNT(*) >= 2                               -- 4: filter groups
ORDER BY avg_gpa DESC                                -- 7: sort (alias OK!)
LIMIT    3;                                          -- 8: keep top 3

-- NULL traps in action
SELECT * FROM students WHERE gpa > 3.0;              -- Cara (NULL) NOT returned
SELECT * FROM students WHERE gpa > 3.0 OR gpa IS NULL; -- include NULLs explicitly

-- COALESCE default
SELECT name, COALESCE(gpa, 0.0) AS gpa_or_zero FROM students;

-- Deterministic top-N (never without ORDER BY)
SELECT name, gpa FROM students ORDER BY gpa DESC LIMIT 2;
```

## 16. Industry Usage
- **Every BI tool** (Looker, Tableau, Superset) generates SELECTs; understanding execution order is how you debug their generated SQL.
- **dbt models** are SELECT statements wrapped in CTEs — the entire modern analytics-engineering stack is this section's pipeline.
- **Production APIs** run `WHERE id = $1 LIMIT 1` with keyset pagination — the LIMIT-after-ORDER BY pattern in the wild.
- **Optimizer traces** (`EXPLAIN` in Postgres/MySQL) show the physical operators implementing each logical step — engineers read them to fix slow queries, which requires knowing the logical order first.
- **Query fuzzing/frameworks** (CockroachDB, DuckDB, Calcite) use the logical order to prove plan correctness — the pipeline is literally the spec.

## 17. References
- PostgreSQL Documentation, SELECT: https://www.postgresql.org/docs/current/sql-select.html
- PostgreSQL Documentation, Logical Processing: https://www.postgresql.org/docs/current/queries-select-lists.html
- MySQL Reference Manual, SELECT: https://dev.mysql.com/doc/refman/8.0/en/select.html
- ISO/IEC 9075-2:2016 (SQL — Foundation; SELECT semantics).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 4 (SQL).

## 18. Cheat Sheet
- Order: FROM → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT.
- WHERE = rows, before grouping; HAVING = groups, after (aggregates allowed).
- Aliases usable in ORDER BY; not in WHERE/GROUP BY (mostly).
- NULL: 3VL — any comparison is UNKNOWN; WHERE keeps TRUE only; use IS NULL.
- `= NULL` never matches; `IS NULL` matches.
- LIMIT runs after ORDER BY; never LIMIT without ORDER BY.
- COUNT(*) vs COUNT(col) vs COUNT(DISTINCT col) — NULL behavior differs.
- DISTINCT costs (hash/sort); only add when duplicates exist.

## 19. Quiz
1. Which runs first? a) GROUP BY b) WHERE c) SELECT d) ORDER BY → **b**
2. `WHERE COUNT(*) > 1` is: a) valid b) invalid — HAVING needed c) valid if aliased d) slow but valid → **b**
3. `gpa > 3.5` on a NULL gpa evaluates to: a) TRUE b) FALSE c) UNKNOWN d) error → **c**
4. `WHERE name = NULL` returns: a) NULL names b) all rows c) nothing d) error → **c**
5. LIMIT runs: a) before ORDER BY b) after ORDER BY c) before WHERE d) first → **b**
6. Aliases are usable in: a) WHERE b) GROUP BY (MySQL) c) ORDER BY d) FROM → **c**
7. COUNT(*) counts: a) non-NULL cols b) all rows c) distinct rows d) NULLs only → **b**
8. `COALESCE(NULL, 5, 0)` returns: a) NULL b) 5 c) 0 d) error → **b**
9. Filtering groups needs: a) WHERE b) HAVING c) LIMIT d) DISTINCT → **b**
10. GROUP BY output order is: a) guaranteed sorted b) not guaranteed c) always hash d) reversed → **b**

## 20. Flashcards
- **Q: Logical execution order?** → **A:** FROM → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT.
- **Q: WHERE vs HAVING?** → **A:** Rows pre-grouping (no aggregates) vs groups post-grouping.
- **Q: What is 3VL?** → **A:** TRUE/FALSE/UNKNOWN; NULL comparisons = UNKNOWN; WHERE keeps TRUE.
- **Q: `= NULL` vs `IS NULL`?** → **A:** Never matches vs correct null test.
- **Q: When is LIMIT safe?** → **A:** After ORDER BY (deterministic top-N).
- **Q: Why can't WHERE use aliases?** → **A:** Aliases born in SELECT (later in the order).
- **Q: COUNT(*) vs COUNT(col)?** → **A:** All rows vs non-NULL values of col.
- **Q: Why is DISTINCT expensive?** → **A:** Needs hash/sort to dedupe.

## 21. Revision
SELECT's pipeline: **FROM→WHERE→GROUP BY→HAVING→SELECT→DISTINCT→ORDER BY→LIMIT**. WHERE filters rows (no aggregates) → GROUP BY groups → HAVING filters groups (aggregates OK) → SELECT computes aliases → DISTINCT dedupes → ORDER BY sorts (alias OK) → LIMIT cuts. NULLs: **3VL** — comparisons are UNKNOWN, WHERE keeps only TRUE; use `IS NULL`, never `= NULL`. Traps to name: `WHERE COUNT(*)` invalid (HAVING), alias in WHERE invalid, LIMIT-before-ORDER-BY nondeterministic, `name <> 'x'` silently drops NULLs. Quick answers: COUNT(*) all rows, COUNT(col) non-null, COUNT(DISTINCT) distinct-non-null. Determinism requires ORDER BY. Physical plans may reorder; logical order is the contract.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the execution order of SELECT?" | 7 / 13 Q1 |
| "WHERE vs HAVING?" | 13 Q3, Q8 |
| "NULLs and three-valued logic?" | 13 Q4-5, Q13 |
| "LIMIT vs ORDER BY?" | 13 Q6-7 |
| "Aliases in which clauses?" | 13 Q2 |
| "COUNT variants?" | 13 Q19 |
| "Top-N query?" | 13 Q12 |
| "Why is DISTINCT slow?" | 13 Q16 |
