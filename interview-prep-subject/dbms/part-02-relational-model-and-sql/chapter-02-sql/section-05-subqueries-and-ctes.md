# Subqueries and CTEs

> **TL;DR**: Subqueries are queries nested inside another query (IN/EXISTS/ANY/ALL, scalar, and inline views); CTEs name intermediate result sets for readability and recursion — knowing when to flatten one into a JOIN or CTE is the difference between working SQL and fast SQL.

## 1. Why Does This Exist?
Real queries rarely fit one flat SELECT — they need comparisons against computed values ("orders above the average"), existence tests ("customers with no orders"), and multi-stage logic. Subqueries exist so a query can *reference the result of another query*, composing complex logic without staging tables or app code. CTEs exist because deep nesting is unreadable and unreusable: a named, inline result set (`WITH x AS (...)`) turns a 50-line subquery labyrinth into step-by-step logic — and enables **recursion** (org charts, tree traversal), which a single SELECT cannot express. Interviewers test this because it separates people who pattern-match from people who reason about query structure.

## 2. How Does It Work?
Three subquery kinds + CTEs:
- **Scalar subquery**: returns exactly one value (one row, one column) → usable as a value (`SELECT name, (SELECT MAX(price) FROM p) ...`).
- **Row/column subquery (IN/ANY/ALL)**: `x IN (SELECT ...)`, `x = ANY(...)`, `x > ALL(...)`, `x > ANY(...)`.
- **Table subquery (inline view / derived table)**: `FROM (SELECT ...) AS t` — used like a table.
- **Correlated subquery**: references the *outer* query's column — re-evaluated per outer row (`WHERE e.salary > (SELECT AVG(salary) FROM emp m WHERE m.dept = e.dept)`).
- **EXISTS/NOT EXISTS**: tests existence (correlated, semi/anti-join semantics, stops at first match).
- **CTE**: `WITH cte AS (SELECT ...) SELECT ... FROM cte ...` — a named, reusable block; **recursive CTE**: `WITH RECURSIVE x(n) AS (base UNION ALL step) SELECT ...` for trees/sequences.

## 3. When Is It Used?
- **IN**: "customers in these regions" (with a static or subquery list).
- **EXISTS/NOT EXISTS**: "has/hasn't a matching row" — the NULL-safe existence idiom.
- **Scalar**: "each row plus the global average/MAX" (also done via window functions).
- **Inline views**: "FROM (aggregate first) JOIN ..." — precomputed summaries.
- **ANY/ALL**: "sales greater than any/all other regions".
- **CTEs**: multi-stage analytics (dbt models are almost entirely CTE chains), recursion (org trees, bill-of-materials), and readability + one-place maintenance.
- **Flattening**: many subqueries are optimizable to JOINs or CTEs — used when the plan shows unnecessary re-evaluation.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: only JOINs (no subqueries).** Rejected: some logic is naturally *predicate-oriented* (existence, membership, scalar comparison) — forcing it into joins produces convoluted queries and duplicates rows (semi-joins need dedup). Subqueries express intent directly.
- **Alternative: only subqueries (no CTEs).** Rejected: deep nesting is unreadable, and subqueries can't recurse or be reused; CTEs are the readability/maintenance layer, and `WITH RECURSIVE` expresses tree traversal that SQL otherwise cannot.
- **Alternative: temp tables for every intermediate result.** Rejected: temp tables need DDL, sessions, and cleanup — CTEs keep intermediates in-query (and many are inlined by the optimizer).
- **Why correlated subqueries despite the cost?** Expressiveness first; the optimizer *can* rewrite many correlated subqueries into joins/semi-joins automatically. When it can't, you unnest manually.
- **Why `IN` vs `EXISTS`?** Historical: `IN` was once universally optimized; `EXISTS` is semi-join-friendly and NULL-safe. Both survive because each is clearer in context.

## 5. Intuition
A subquery is a **question inside a question** — like asking "who among these people is taller than the average?" (the average is itself a question). A CTE is **writing intermediate answers on a whiteboard** before solving the main problem: "first: compute each team's average (call it A). Then: who is above A?" The whiteboard version (CTE) is readable, testable in steps, and — with RECURSIVE — can loop "keep expanding the org chart until no more levels" which plain SQL can't do. EXISTS is a **flashlight check**: "does any such row exist? — yes/no", often faster than a full subquery.

## 6. Real-World Analogy
A **job interview funnel**: "which candidates passed the average score?" — first you compute the average (inner question), then filter (outer question): a scalar/WHERE subquery. "Which candidates are in the referral program?" — a membership check (IN). "Which candidates have *no* interviews booked?" — an anti-existence check (NOT EXISTS). The CTE version: the recruiter writes on the whiteboard "1) compute average → 72. 2) list candidates above 72." And the recursive CTE is the **org-chart crawl**: "list me, then my reports, then their reports..." until the tree is exhausted — the single query shape that no plain SELECT expresses.

## 7. Formal Definition
(Elmasri & Navathe Ch. 4; ISO/IEC 9075-2.)
- **Subquery**: a `SELECT` embedded in another query's FROM/WHERE/HAVING/SELECT. Scalar (one value), row (one tuple), or table (set of tuples).
- **Correlated subquery**: a subquery containing a reference to an outer query's column; its value depends on the outer row; logically re-evaluated per outer tuple (optimizer may rewrite).
- **EXISTS(S)**: TRUE if S non-empty (stops at first row); **NOT EXISTS**: TRUE if empty.
- **IN(S)** ≡ `= ANY(S)`; **NOT IN(S)** ≡ `<> ALL(S)` — note: NOT IN is false/unknown if S contains NULL.
- **CTE**: `WITH [RECURSIVE] name [(cols)] AS (query) main_query` — names a query expression usable in the main query; RECURSIVE form has a base term `UNION [ALL]` a recursive term that references the CTE's own name.
- **Semantics**: conceptually, CTEs are like derived tables; the optimizer may inline them (Postgres inlines non-recursive, non-materialized CTEs).

## 8. Example
```
emp(id, name, dept, salary): (1,A,Sales,50),(2,B,Sales,90),(3,C,Eng,60),(4,D,Eng,120)
```
- **Scalar + WHERE subquery**: `SELECT name FROM emp WHERE salary > (SELECT AVG(salary) FROM emp);` → avg=80 → A?50 no, B?90 yes, C?60 no, D?120 yes → {B,D}.
- **Correlated**: "above their dept average": `SELECT e.name, e.dept FROM emp e WHERE e.salary > (SELECT AVG(s.salary) FROM emp s WHERE s.dept = e.dept);` → Sales avg 70 → B(90); Eng avg 90 → D(120) → {B,D}.
- **IN**: `SELECT name FROM emp WHERE dept IN ('Sales','Eng');` (membership).
- **EXISTS**: depts with a high earner: `SELECT DISTINCT dept FROM emp e WHERE EXISTS (SELECT 1 FROM emp m WHERE m.dept = e.dept AND m.salary > 100);` → {Eng}.
- **NOT IN trap**: `WHERE dept NOT IN (SELECT dept FROM emp WHERE salary > 100)` — if that subquery has NULLs, everything breaks (NULL → UNKNOWN). Use NOT EXISTS.
- **CTE**: `WITH dept_avg AS (SELECT dept, AVG(salary) a FROM emp GROUP BY dept) SELECT e.name FROM emp e JOIN dept_avg d ON d.dept = e.dept WHERE e.salary > d.a;`
- **Recursive CTE**: org tree — see Section 15.

## 9. Internal Working
1. **Parse**: subqueries become algebra expressions; correlated references become outer-column bindings.
2. **Optimizer rewrites**:
   - **Unnesting/flattening**: many IN/EXISTS subqueries become semi/anti-joins (hash) — the classic rewrite; correlated scalar subqueries may become joins or left-join-with-aggregate.
   - **CTE inlining**: non-recursive, single-use CTEs are inlined into the main query (Postgres default) — so a "CTE" often costs nothing; `MATERIALIZED` forces a temp table.
   - **Subquery pushdown**: predicates pushed into the subquery.
3. **Execution**:
   - Uncorrelated subquery: evaluated once (or once per plan — e.g., `InitPlan`), result cached.
   - Correlated: evaluated per outer row (or rewritten to a join); `EXISTS` short-circuits at first match.
   - Recursive CTE: iterative evaluation (working table + next table) until no new rows.
4. **The NULL trap in NOT IN**: `x NOT IN (1, 2, NULL)` = `x<>1 AND x<>2 AND x<>NULL` → the last is UNKNOWN → whole is UNKNOWN → row excluded. Hence NOT EXISTS for safety.

## 10. Time Complexity
- **Uncorrelated subquery (IN/EXISTS/scalar)**: O(n) once (indexed: O(log m)); then filter O(n).
- **Correlated subquery, naive**: O(n·m) (re-run per row) — the optimizer's unnest to join makes it O(n+m) (hash) or O(n·log m) (index).
- **IN** as semi-join: O(n + m) hash.
- **NOT EXISTS** as anti-join: O(n + m) hash (early exit on matches).
- **NOT IN** without index: O(n·m) with NULL risk — always prefer NOT EXISTS.
- **Recursive CTE**: O(levels × work-per-level); worst case exponential if not bounded by keys.
- **CTE inlined**: same cost as the inline query (no materialization overhead).

## 11. Advantages
- **Expressiveness**: existence, membership, scalar comparisons, and per-row context (correlated).
- **Readability**: CTEs turn nested subqueries into named, linear steps; recursion is expressible.
- **NULL-safe idioms**: EXISTS/ANY avoid the NOT IN NULL trap.
- **Optimization hooks**: subqueries are unnestable into joins/semi-joins — often free.
- **Reusability**: CTEs can be referenced multiple times in one statement (and in some engines, stacked).
- **Testability**: you can run a CTE's body alone to debug.

## 12. Disadvantages
- **Correlated subquery cost**: naive per-row evaluation O(n·m) if the optimizer can't unnest.
- **CTE inlining vs materialization**: relying on a CTE to "cache" work can backfire (inlined → recomputed); `MATERIALIZED` needed for side-effect/window-dependent CTEs.
- **NOT IN NULL trap**: silent wrong results — a top-3 production bug.
- **Recursion limits**: unbounded/cyclic data → runaway recursion (depth limit needed); performance is engine-dependent.
- **Readability cliffs**: deeply nested (not CTE'd) subqueries become unreadable; also CTE chains can hide performance.
- **No side effects**: subqueries can't share state across the outer query; some engines restrict what they can reference.

## 13. Interview Questions
1. **Q: What is a subquery? Name the kinds.** A: A query nested in another query: scalar (single value), row/column (used with IN/ANY/ALL), table (inline view in FROM), and correlated (references the outer query).
2. **Q: What is a correlated subquery?** A: A subquery that references a column of the outer query — logically re-evaluated per outer row. Example: "employees above their *department's* average". Optimizers often rewrite it into a join.
3. **Q: IN vs EXISTS — when do you use each?** A: Both test membership; EXISTS is a semi-join that stops at the first match and is NULL-safe; IN can be less safe with NULLs and historically less optimized. Use EXISTS/NOT EXISTS for existence semantics; use IN for simple membership lists.
4. **Q (tricky): Why is `NOT IN` dangerous with NULLs?** A: `x NOT IN (1, NULL)` ≡ `x<>1 AND x<>NULL` → the NULL comparison is UNKNOWN → whole predicate UNKNOWN → row excluded. So `NOT IN` with a NULL-containing subquery returns *no rows*. Use `NOT EXISTS` (anti-join) — NULL-safe.
5. **Q: What is a CTE?** A: `WITH name AS (query) SELECT ...` — a named, in-query intermediate result for readability, reuse, and recursion. Many are inlined by the optimizer (no cost); `MATERIALIZED` forces a temp table.
6. **Q: What is a recursive CTE and how does it work?** A: `WITH RECURSIVE x AS (base UNION ALL recursive-term-referencing-x) SELECT ...` — the base seed, then iterative expansion until no new rows. Used for org charts, tree traversal, and sequence generation.
7. **Q (scenario): Find employees who out-earn their department average — subquery and CTE versions.** A: Correlated: `WHERE salary > (SELECT AVG(s) FROM emp m WHERE m.dept=e.dept)`. CTE: `WITH da AS (SELECT dept, AVG(salary) a FROM emp GROUP BY dept) SELECT ... JOIN da ... WHERE salary > a`. Both correct; the CTE is more readable.
8. **Q: What does `ANY` / `ALL` do?** A: `x = ANY(array/subquery)` → true if x equals any element (≡ IN); `x > ALL(subquery)` → true if greater than every returned value. Careful: ALL over an empty subquery is TRUE; ANY over empty is FALSE.
9. **Q (production): "All departments with no employees" — subquery vs join.** A: `SELECT d.dname FROM dept d WHERE NOT EXISTS (SELECT 1 FROM emp e WHERE e.did=d.did);` or the anti-join `LEFT JOIN ... WHERE e.id IS NULL`. Both fine; prefer EXISTS for clarity, the join is also fine. Avoid `NOT IN` (NULL risk on emp.did if nullable).
10. **Q: When does the optimizer unnest a subquery?** A: When it's a semi/anti-join candidate (IN/EXISTS) or a correlated scalar that a join can express. Unnesting converts O(n·m) re-evaluation into a hash join O(n+m). `EXPLAIN` shows `Subquery Scan`/semi-join nodes.
11. **Q (tricky): A CTE used twice — inlined or materialized?** A: Depends: Postgres inlines non-recursive CTEs referenced once; with multiple references it may materialize automatically (or you force it with `MATERIALIZED`). Materialization = temp table (avoids recompute, costs I/O). Check the plan.
12. **Q: What is an inline view / derived table?** A: A subquery in the FROM clause used as a table: `FROM (SELECT dept, AVG(salary) a FROM emp GROUP BY dept) AS d`. It's a table-valued subquery — the historical name for what CTEs now do more readably.
13. **Q (production): When would you choose a CTE over a subquery?** A: Readability and reuse (referenced multiple times, stacked CTEs for stepwise logic), recursion, and when the optimizer would otherwise duplicate a complex subquery. Subqueries win when they're trivial and the optimizer inlines them anyway.
14. **Q: What is the difference between `EXISTS` and `IN` in terms of optimization?** A: EXISTS maps to a semi-join that can stop at the first matching row (no full result, no dedup); IN on a subquery may be rewritten to a semi-join too, but historically materialized the subquery. Modern optimizers often treat them identically.
15. **Q (scenario): Write the recursive CTE for an org chart.** A: `WITH RECURSIVE org AS (SELECT id, name, mgr, 1 lvl FROM emp WHERE mgr IS NULL UNION ALL SELECT e.id, e.name, e.mgr, o.lvl+1 FROM emp e JOIN org o ON e.mgr = o.id) SELECT name, lvl FROM org ORDER BY lvl;`
16. **Q: What is the "ANY/ALL with empty set" gotcha?** A: `x > ALL(empty)` = TRUE (vacuously true); `x > ANY(empty)` = FALSE. Business queries must handle empty subqueries deliberately (e.g., guard with EXISTS).
17. **Q (tricky): Can you reference an outer column in a CTE?** A: CTEs can't be correlated in the same way as subqueries (a CTE is defined once, outside the outer query's per-row context). That's a key structural difference — use a correlated subquery or LATERAL for per-row subqueries.
18. **Q: What is `LATERAL`?** A: `FROM ... , LATERAL (SELECT ... WHERE inner.col = outer.col)` — a correlated *derived table* that can reference preceding FROM items per row. Used for per-row top-N and function expansion. It's the "join version of a correlated subquery".
19. **Q (production): A query with a big correlated subquery is slow. What do you check?** A: (1) Is it unnestable? Add index on the subquery's join column; (2) rewrite as a JOIN/CTE; (3) check `EXPLAIN` for per-row re-execution (`SubPlan` re-evaluated per row); (4) consider materializing the inner result. Unnesting + indexes usually fix it.
20. **Q (hard): Explain how Postgres decides to inline or materialize a CTE.** A: Non-recursive CTEs referenced once are inlined (default) — zero overhead. CTEs referenced multiple times, with side effects (volatile functions), or marked `MATERIALIZED` are executed once into a temp store. This affects both correctness (volatile functions) and performance (recompute vs temp I/O).

## 14. Follow-Up Questions
1. **Q: What is query flattening/unnesting?** A: The optimizer rewrite that converts a subquery into a join or semi/anti-join — the single most important subquery optimization; it's why `EXISTS` usually becomes a hash semi-join.
2. **Q: How does `EXISTS` differ from `IN` with respect to column projection?** A: EXISTS doesn't care what the subquery selects (`SELECT 1` convention) — it only tests emptiness; IN must produce a single column. That's why `SELECT 1` is idiomatic in EXISTS.
3. **Q: Can a CTE be recursive and reference another CTE?** A: Yes — recursive CTEs can reference earlier CTEs in their base/recursive terms (with engine constraints), enabling layered recursive logic.
4. **Q: What are "common table expression" vs "temporary table" trade-offs?** A: CTE: in-query, optimizer-controlled (inlined or materialized), no DDL/session, gone after statement. Temp table: persistent for session, re-usable across statements, has stats + indexes. Use temp tables when a result is needed across many queries.
5. **Q: Why do warehouses love CTEs (dbt)?** A: dbt models are CTE chains — readability, modularity, and the warehouse's optimizer handles inlining; CTEs also enable `GROUP BY`-heavy stepwise logic without staging tables.

## 15. Coding Example
```sql
-- Scalar subquery
SELECT name, salary,
       (SELECT AVG(salary) FROM emp) AS company_avg
FROM   emp;

-- Correlated subquery (per-dept avg)
SELECT e.name, e.dept, e.salary
FROM   emp e
WHERE  e.salary > (SELECT AVG(s.salary) FROM emp s WHERE s.dept = e.dept);

-- EXISTS (semi-join)
SELECT d.dname FROM dept d
WHERE  EXISTS (SELECT 1 FROM emp e WHERE e.did = d.did);

-- NOT EXISTS (anti-join, NULL-safe)
SELECT d.dname FROM dept d
WHERE  NOT EXISTS (SELECT 1 FROM emp e WHERE e.did = d.did);

-- CTE chain (readable, stepwise)
WITH dept_avg AS (
  SELECT dept, AVG(salary) AS avg_sal FROM emp GROUP BY dept
),
above AS (
  SELECT e.name FROM emp e JOIN dept_avg d ON d.dept = e.dept
  WHERE  e.salary > d.avg_sal
)
SELECT * FROM above;

-- Recursive CTE: org chart
WITH RECURSIVE org AS (
  SELECT id, name, mgr, 1 AS lvl FROM emp WHERE mgr IS NULL
  UNION ALL
  SELECT e.id, e.name, e.mgr, o.lvl + 1
  FROM   emp e JOIN org o ON e.mgr = o.id
)
SELECT lvl, name FROM org ORDER BY lvl;

-- LATERAL: per-row top-N
SELECT d.dname, top.name
FROM   dept d
LEFT JOIN LATERAL (
  SELECT name FROM emp e WHERE e.did = d.did ORDER BY e.salary DESC LIMIT 2
) top ON true;
```

## 16. Industry Usage
- **dbt models** are CTE chains by convention — every modern analytics-engineering repo is built on this section's `WITH` patterns.
- **`NOT EXISTS`/anti-join** is the standard dedup/exclusion idiom in CDC and reconciliation pipelines (find missing records).
- **Recursive CTEs** power org charts, bill-of-materials, and graph-lite queries in Postgres/Oracle/SQL Server — even the "infinite" hierarchy cases.
- **LATERAL joins** appear in Postgres-heavy shops for per-row top-N and function expansion (PostGIS, jsonb).
- **Optimizers unnesting subqueries** is why `EXISTS` is rarely slower than joins in production — semi-joins are a first-class operator in every engine's planner.

## 17. References
- PostgreSQL Documentation, Subqueries: https://www.postgresql.org/docs/current/functions-subquery.html
- PostgreSQL Documentation, WITH (CTEs): https://www.postgresql.org/docs/current/queries-with.html
- PostgreSQL Documentation, LATERAL: https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-LATERAL
- MySQL Reference Manual, Subqueries: https://dev.mysql.com/doc/refman/8.0/en/subqueries.html
- ISO/IEC 9075-2:2016 (SQL — subqueries, WITH).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 4 (Nested Subqueries).

## 18. Cheat Sheet
- Kinds: scalar (1 value), IN/ANY/ALL (membership), table/inline view (FROM), correlated (references outer), EXISTS.
- Correlated = re-evaluated per row → optimizer unnests to joins.
- NOT IN breaks with NULLs → use NOT EXISTS (anti-join).
- CTE: `WITH x AS (...) SELECT ...` — readable, reusable, recursive.
- Recursive: `WITH RECURSIVE x AS (base UNION ALL step)` for trees.
- ANY(empty)=FALSE; ALL(empty)=TRUE.
- EXISTS stops at first match (`SELECT 1` idiomatic).
- LATERAL = correlated derived table (per-row top-N).

## 19. Quiz
1. Which is NULL-safe for "not present"? a) NOT IN b) NOT EXISTS c) <> d) != → **b**
2. A correlated subquery references: a) a constant b) the outer query's columns c) a CTE d) an index → **b**
3. `x > ALL(empty)` = a) FALSE b) TRUE c) NULL d) error → **b**
4. CTE syntax: a) SELECT ... WITH b) WITH x AS (...) SELECT c) BEGIN d) MERGE → **b**
5. Recursive CTEs need: a) GROUP BY b) UNION ALL c) ORDER BY d) JOIN → **b**
6. EXISTS is optimized as: a) full join b) semi-join c) cross join d) product → **b**
7. `SELECT 1` in EXISTS is: a) output b) a convention (only emptiness matters) c) error d) filter → **b**
8. NOT IN with a NULL in the subquery returns: a) some rows b) nothing c) all rows d) error → **b**
9. LATERAL is like: a) a correlated derived table b) a window function c) an index d) a trigger → **a**
10. Inlined CTEs cost: a) temp table I/O b) nothing extra c) a lock d) a scan → **b**

## 20. Flashcards
- **Q: 4 subquery kinds?** → **A:** Scalar, IN/ANY/ALL, table/inline view, correlated.
- **Q: Correlated subquery?** → **A:** References outer column; re-evaluated per row; unnestable to join.
- **Q: NOT IN NULL trap?** → **A:** NULL → UNKNOWN → no rows; use NOT EXISTS.
- **Q: What is a CTE?** → **A:** Named in-query result (`WITH x AS ...`) — readable, reusable, recursive.
- **Q: Recursive CTE structure?** → **A:** Base `UNION ALL` recursive-term-using-itself.
- **Q: ANY vs ALL on empty?** → **A:** ANY=FALSE; ALL=TRUE.
- **Q: EXISTS plan shape?** → **A:** Semi-join, stops at first match.
- **Q: What is LATERAL?** → **A:** Correlated derived table — per-row subqueries as joins.

## 21. Revision
Subqueries: **scalar** (single value), **IN/ANY/ALL** (membership), **table/inline view** (FROM), **correlated** (references outer row → re-evaluated per row → optimizer unnests to join), **EXISTS/NOT EXISTS** (semi/anti-join, NULL-safe, stops at first match). **CTEs** (`WITH x AS (...)`) add readability, reuse, and **recursion** (`WITH RECURSIVE ... UNION ALL`). Traps: `NOT IN` + NULL subquery → zero rows (use NOT EXISTS); ANY(empty)=FALSE vs ALL(empty)=TRUE; CTE inlining vs MATERIALIZED. Interview moves: write "above dept avg" in correlated and CTE forms; write the recursive org-chart CTE; explain the NOT IN bug; mention LATERAL for per-row top-N; and state that EXISTS becomes a hash semi-join in the plan.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a correlated subquery?" | 13 Q2 |
| "IN vs EXISTS?" | 13 Q3 |
| "NOT IN NULL trap?" | 13 Q4 |
| "What is a CTE / when use it?" | 13 Q5, Q13 |
| "Recursive CTE for org chart?" | 13 Q6, Q15 |
| "Subquery vs join?" | 13 Q9, Q19 |
| "ANY/ALL empty semantics?" | 13 Q8, Q16 |
| "LATERAL joins?" | 13 Q18 |
