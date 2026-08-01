# Joins in Depth

> **TL;DR**: A join combines rows from two relations by a condition — INNER keeps only matches, LEFT/RIGHT OUTER keep one side's unmatched rows (with NULLs), FULL keeps both, CROSS pairs everything, and SELF joins a table to itself — with NULLs and duplicate keys as the two traps that break naive reasoning.

## 1. Why Does This Exist?
Relational data is normalized into separate tables, so *almost every real query needs to combine tables* — a join is the value-based link that puts a customer, her orders, and his items back together. This section exists because joins are the most-queried and most-misunderstood SQL construct: subtle semantic differences (inner vs outer, `ON` vs `WHERE`, `USING` vs `NATURAL`) produce wrong results silently, and NULL keys + duplicate keys break "obvious" expectations. Interviewers test joins because they test whether you understand *set semantics* — which rows survive, which don't, and why — not whether you memorized the syntax.

## 2. How Does It Work?
For tables R and S joined on condition θ:
- **INNER JOIN**: `R ⋈ S = σ_θ(R × S)` — rows where θ is TRUE. Unmatched rows dropped.
- **LEFT OUTER JOIN**: inner rows + R's unmatched rows padded with NULLs for S's columns.
- **RIGHT OUTER JOIN**: inner + S's unmatched (NULLs for R).
- **FULL OUTER JOIN**: inner + both sides' unmatched.
- **CROSS JOIN**: R × S (no condition) — every pair.
- **SELF JOIN**: any join type where R and S are the *same table* (aliased) — for rows-to-rows comparisons (employees vs managers).
- **ON vs USING vs NATURAL**: `ON` = arbitrary condition; `USING(col)` = equality on the named column (merged in output); `NATURAL` = equality on *all* common column names (auto, dangerous).
- **Semantically**, LEFT JOIN is "keep all left rows; fill gaps with NULL" — so any `WHERE` on right-table columns that rejects NULL *undoes* the outer-ness.

## 3. When Is It Used?
- **INNER**: "orders with their customer" where every order must have one; existence checks.
- **LEFT**: "all customers and their orders, including customers with zero orders" — the reporting/analytics workhorse.
- **RIGHT**: mirror of LEFT; rarely used directly (most people flip to LEFT) but appears in generated SQL.
- **FULL**: comparing two systems' data (rows in A not in B and vice versa) — reconciliation, diffs.
- **CROSS**: generating combinations (all products × all stores for a matrix), date range filling.
- **SELF**: hierarchy queries (manager-of), comparing rows within one table (find employees who out-earn their manager).
- **ANTI/SEMI** (via NOT EXISTS/EXISTS or LEFT JOIN ... WHERE IS NULL): find rows *without* a match.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: denormalize everything so joins aren't needed.** Rejected: redundancy, update anomalies, and no way to ask arbitrary questions (normalization is the point, Part 03).
- **Alternative: joins by manual programming (network model).** Rejected: navigational joins couple queries to storage; the relational *value-based* join is declarative and storage-independent.
- **Alternative: one universal join (always NATURAL).** Rejected: silently joins on unintended common columns; `ON`/`USING` give explicit control — `NATURAL` is retained as sugar, mostly avoided in production.
- **Why so many join types?** Each serves a distinct set-semantic need: inner (matches only), outer (preserve a side), full (preserve both), cross (all pairs), self (same table). Dropping any one type would force contorted workarounds.
- **Why `WHERE` and `ON` differ?** `ON` is part of the join (decides matching *before* outer-padding); `WHERE` filters the *joined result* — the difference is exactly what breaks LEFT JOINs when misused.

## 5. Intuition
Picture **two lists on two whiteboards**. INNER JOIN = "the overlapping names, written once." LEFT JOIN = "every name from the left board, and next to it the matching name from the right board — or a blank (NULL) if there's no match." FULL JOIN = "the union of both boards, blanks where a side has no match." CROSS JOIN = "every name on the left paired with every name on the right — multiplication." SELF JOIN = "the same board read twice: for each employee, find the row named as their boss." The key mental move: **joins answer "which rows go together?"** — and the join type decides what happens to the leftovers.

## 6. Real-World Analogy
A **wedding guest list + meal preferences list**. INNER JOIN = guests who returned their RSVP *and* chose a meal (only complete pairs). LEFT JOIN = every guest on the master list, with meal choice filled in or "—" (NULL) for those who didn't RSVP. FULL JOIN = all guests on either list — RSVPs with no master record are flagged too. CROSS JOIN = the (invitee × menu) pairing the chef uses to estimate quantities. SELF JOIN = matching each guest to the *plus-one* named on their own card — the list referenced against itself. The master list (LEFT) is what the venue needs; the NULL fill-in is exactly why `WHERE meal IS NOT NULL` would undo it.

## 7. Formal Definition
Let R, S be relations and θ a join condition.
- **Inner (theta) join**: R ⋈_θ S = { t : t ∈ R × S ∧ θ(t) }.
- **Equi-join**: θ is a conjunction of equalities.
- **Natural join**: R ⋈ S — equi-join on the intersection of attribute sets, with one copy of join attributes.
- **Left outer join**: R ⟕_θ S = (R ⋈_θ S) ∪ { (r, NULL, ..., NULL) : r ∈ R, no s with θ(r,s) }.
- **Right outer join**: S ⟖_θ R (symmetric).
- **Full outer join**: R ⟗_θ S = left ∪ right outer results.
- **Cross join (product)**: R × S.
- **Semi-join**: R ⋉ S = { r ∈ R : ∃s ∈ S, θ(r,s) }.
- **Anti-join**: R ⋊ S = { r ∈ R : ¬∃s ∈ S, θ(r,s) } — implemented as `NOT EXISTS` or `LEFT JOIN ... WHERE S.key IS NULL`.
(Elmasri & Navathe Ch. 5; ISO/IEC 9075.)

## 8. Example
```
customers:  (1,Alice), (2,Bob), (3,Cara)
orders:     (10,1,100), (11,1,50), (12,2,200)     -- customer_id → FK
```
- **INNER** `c JOIN o ON c.id = o.customer_id` → Alice(10,11), Bob(12). **Cara absent.**
- **LEFT** → Alice(10,11), Bob(12), **Cara with NULL order columns**.
- **RIGHT** (o LEFT c) → same rows here since every order has a customer.
- **FULL** → same as LEFT here (no orphan orders).
- **CROSS** c × o → 3 × 3 = 9 pairs (e.g., Alice-10, Alice-11, Alice-12, ...).
- **SELF**: `employees(id, name, manager_id)` → `SELECT e.name, m.name FROM employees e LEFT JOIN employees m ON e.manager_id = m.id` — employees with their boss (NULL for the CEO).
- **LEFT + WHERE trap**: `... LEFT JOIN orders o ON c.id = o.customer_id WHERE o.id IS NOT NULL` → behaves *exactly like INNER* (Cara dropped) — the classic silent bug.

## 9. Internal Working
1. **Parse** the join (`JOIN ... ON ...`) into an algebra join node.
2. **Optimizer chooses a physical join algorithm**:
   - **Nested-loop join**: for each R row, scan S — O(n·m); fine for small inputs or with index → O(n·log m) (index nested-loop).
   - **Hash join**: hash R's keys, probe S — O(n+m); best for large unsorted joins.
   - **Merge join**: sort both on key, merge — O(n log n + m log m); good for pre-sorted inputs, output is ordered.
3. **Outer joins** are implemented with the same algorithms plus a "preserved side" bookkeeping (emit unmatched left rows with NULL padding).
4. **Semi/anti joins** use `EXISTS`/`NOT EXISTS` plans or hash-semi/anti-join operators — they can stop at the first match (cheaper than a full join).
5. **`EXPLAIN`** shows the chosen algorithm (e.g., `Hash Join`, `Nested Loop Left Join`) — reading it is how you debug join performance.

## 10. Time Complexity
- **Nested-loop join**: O(n·m); index nested-loop O(n·log m) — best when one side is small and indexed.
- **Hash join**: O(n + m) build+probe — the default for big equi-joins (memory-bounded by `work_mem`).
- **Sort-merge join**: O(n log n + m log m) — preferred when inputs are already sorted or output order matters.
- **Cross join**: O(n·m) tuples — avoid unless deliberate.
- **Left/right/full outer joins**: same asymptotic cost as the underlying inner algorithm (padding adds no order-of-growth).
- **Semi/anti join via EXISTS**: stops at first match — often O(n + m) with a hash.

## 11. Advantages
- **Recomposition**: normalized data becomes queryable end-to-end (customer→orders→items).
- **Declarative**: `ON` describes *what* matches, not *how*; optimizer picks the algorithm.
- **Outer joins**: preserve unmatched data (reporting without data loss).
- **Performance options**: three algorithms + indexes let the optimizer match any data shape.
- **Composable**: joins nest with filters, aggregates, and window functions.
- **Correct by value**: joins on keys (PK↔FK) are index-accelerated and integrity-backed.

## 12. Disadvantages
- **Duplication explosion**: joins on duplicate keys multiply rows (1 order × 3 items × 2 shipments) — a classic "why are my numbers 6× too big" bug.
- **NULL traps**: outer-join NULL padding, then a `WHERE` filter that rejects NULLs, silently reverts to inner — the #1 join bug.
- **Cost**: naive nested loops are O(n·m); wrong join order/algorithm makes queries seconds → minutes.
- **Semantic fragility**: `NATURAL`/`USING` rely on column names; renaming a column changes join behavior silently.
- **Self-join aliasing errors**: forgetting `AS` aliases on self-joins → ambiguous column errors.

## 13. Interview Questions
1. **Q: Explain INNER vs LEFT OUTER JOIN.** A: INNER keeps only rows that match the condition (unmatched dropped). LEFT OUTER keeps all left rows, padding unmatched right columns with NULLs. RIGHT/FULL preserve the other/both sides.
2. **Q: What does a CROSS JOIN return?** A: The cartesian product — every row of R paired with every row of S, O(n·m) rows, no condition. Rarely intended; usually a bug (forgotten `ON`), but deliberate for generating combinations.
3. **Q: What is a self-join? When is it used?** A: Joining a table to itself using table aliases. Used for hierarchies (employee→manager), row-vs-row comparisons (pairs of products bought together), and dedup checks.
4. **Q (tricky): Does `WHERE o.id IS NOT NULL` change a LEFT JOIN?** A: Yes — that predicate rejects the NULL-padded unmatched rows, so the LEFT JOIN behaves exactly like an INNER JOIN (silently). Filtering the right table in WHERE undoes outer-join preservation; use the `ON` condition for such filters.
5. **Q: What is the difference between `ON`, `USING`, and `NATURAL JOIN`?** A: `ON` = arbitrary condition; `USING(col)` = equality on one named column (merged in output, usable unqualified); `NATURAL` = equality on *all* common columns automatically. NATURAL is dangerous (silent column-name coupling) — production code prefers explicit ON/USING.
6. **Q (production): A join returns more rows than the left table had. Why?** A: Duplicate keys on the right side — each right match multiplies. E.g., joining orders to items (1 order, 3 items) yields 3 rows per order. Use `DISTINCT`, aggregate, or fix the join granularity.
7. **Q: What is an anti-join? How do you write it?** A: Rows of R with no match in S. Standard: `NOT EXISTS (SELECT 1 FROM S WHERE ...)` or `LEFT JOIN S ON ... WHERE S.key IS NULL`. (Beware `NOT IN` with NULLs — see below.)
8. **Q (tricky): `NOT IN (SELECT ...)` vs `NOT EXISTS` — which is safe with NULLs?** A: `NOT IN` returns *no rows at all* if the subquery contains a NULL (because `x NOT IN (..., NULL)` is UNKNOWN). `NOT EXISTS` is NULL-safe. Production rule: prefer `NOT EXISTS` / anti-join.
9. **Q: When does the optimizer pick hash vs nested-loop vs merge join?** A: Hash: large unsorted equi-joins (O(n+m), memory-bounded). Nested-loop: small inputs or indexed right side (O(n·log m)). Merge: pre-sorted inputs / order-preserving / large ranges. Stats + `work_mem` drive the choice.
10. **Q: What is the difference between an equi-join and a theta join?** A: Equi-join: condition is equality (`a.x = b.y`). Theta join: any comparison condition (`>`, `<`, `<>`, or compound). Natural join is a specific equi-join (all common columns).
11. **Q (scenario): "All departments, even those with no employees" — which join?** A: LEFT JOIN departments to employees (`FROM departments d LEFT JOIN employees e ON e.dept_id = d.id`). Departments without employees appear with NULL employee columns.
12. **Q: What is a semi-join?** A: Rows of R that have at least one match in S — without returning S's columns (no duplication even if many matches). SQL: `EXISTS` or `IN`. Optimizers use a hash semi-join that stops at first match.
13. **Q (production): Why does joining three tables produce a huge result?** A: Join granularity multiplies: if order has 3 items and each item has 2 shipments, the 3-way join yields 6 rows per order. Always reason about the *multiplicative* semantics before writing multi-table joins.
14. **Q: What does a FULL OUTER JOIN return that LEFT+RIGHT don't separately?** A: Unmatched rows from *both* sides (left-orphans and right-orphans) in one result. Used for reconciliations: "rows in A but not B AND rows in B but not A".
15. **Q (tricky): Can you join on a non-key column?** A: Yes — any predicate is allowed (`ON a.start_date <= b.end_date` — a range/interval join, used for time-overlap queries). It's just slower and can multiply rows; keys make joins correct + fast.
16. **Q: What is the difference between a join and a subquery?** A: Both combine data, but joins combine *from multiple tables* producing side-by-side columns; subqueries compute values used in predicates (or inline views). Many correlated subqueries can be rewritten as joins — often faster.
17. **Q (production): "Find customers with no orders" — three ways to write it.** A: (1) `LEFT JOIN ... WHERE o.id IS NULL` (anti-join); (2) `NOT EXISTS`; (3) `id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL)`. Name the NULL caveat of (3).
18. **Q: How does join order affect performance?** A: The optimizer tries to join the smallest pairs first (reducing intermediate cardinality). Wrong join order = huge intermediate results. That's why join-count/selectivity stats matter and why `join_collapse_limit` exists (Postgres).
19. **Q (hard): What happens with duplicate keys in a FULL OUTER JOIN?** A: Cartesian-ish: each left dup pairs with each right dup (and vice versa). The result can grow multiplicatively; dedupe the sides first (GROUP BY/DISTINCT) or fix the source keys. Outer joins don't protect you from duplication.
20. **Q: When would you use a CROSS JOIN deliberately?** A: Generating a complete grid: every product × every store for a coverage report; calendar-date × dimension filling; testing combinatorial cases. Deliberate, bounded, and clearly commented.

## 14. Follow-Up Questions
1. **Q: What's the difference between a join condition in ON vs a filter in WHERE?** A: ON decides match *before* outer padding (right-side filters belong here); WHERE filters the *final* result (rejects NULL-padded rows). Same syntax, different semantic stage — the LEFT JOIN killer.
2. **Q: How does an optimizer handle a LEFT JOIN?** A: It can't freely reorder it with other joins (outer joins are not associative) — restricted join reordering. Postgres uses `Lateral`/specific join trees for outer joins.
3. **Q: What is a "lateral join" (Postgres)?** A: `LEFT JOIN LATERAL` lets the right side reference left columns per-row (like a correlated subquery in a join) — used for "top-N per group" and function calls. It's a join, not a filter.
4. **Q: How do you join a table with itself without alias collision?** A: `FROM employees AS e JOIN employees AS m ON e.manager_id = m.id` — aliases give each "copy" a distinct namespace; without them, column references are ambiguous.
5. **Q: When is a join "lossy" for aggregation?** A: When the join duplicates rows (1 order × 3 items), then `SUM(item_qty)` sums 3× per order — double counting. Aggregate before joining or join at the right granularity.

## 15. Coding Example
```sql
-- Sample tables
CREATE TABLE dept (did INT PRIMARY KEY, dname TEXT);
CREATE TABLE emp  (eid INT PRIMARY KEY, name TEXT, salary INT, did INT REFERENCES dept(did));
INSERT INTO dept VALUES (1,'Eng'),(2,'Sales'),(3,'Ops');       -- Ops has no employees
INSERT INTO emp  VALUES (10,'Alice',100,1),(11,'Bob',90,1),(12,'Cara',80,2);

-- INNER: only departments with staff
SELECT d.dname, e.name FROM dept d JOIN emp e ON e.did = d.did;
-- Eng:Alice, Eng:Bob, Sales:Cara     (Ops missing!)

-- LEFT: all departments (Ops appears with NULL)
SELECT d.dname, e.name FROM dept d LEFT JOIN emp e ON e.did = d.did;
-- Eng:Alice, Eng:Bob, Sales:Cara, Ops:NULL

-- The classic trap: WHERE on the right table undoes LEFT
SELECT d.dname, e.name FROM dept d LEFT JOIN emp e ON e.did = d.did WHERE e.salary > 80;
-- Eng:Alice, Eng:Bob   (Cara dropped by salary; Ops NULL dropped too) -> behaves INNER!

-- Self join: employees and their managers
CREATE TABLE org (eid INT PRIMARY KEY, name TEXT, mgr INT REFERENCES org(eid));
SELECT e.name AS emp, m.name AS boss
FROM   org e LEFT JOIN org m ON e.mgr = m.eid;

-- Anti-join: departments with no employees (two correct ways)
SELECT d.dname FROM dept d LEFT JOIN emp e ON e.did = d.did WHERE e.eid IS NULL;  -- Ops
SELECT d.dname FROM dept d WHERE NOT EXISTS (SELECT 1 FROM emp e WHERE e.did = d.did);  -- Ops
```

## 16. Industry Usage
- **Every analytics query** is a join network: dbt models chain CTE joins; Looker/Tableau generate join-heavy SQL from semantic layers.
- **Star-schema warehouses** (Snowflake, Redshift, BigQuery) are literally built on joins: fact tables ⋈ dimension tables — the join is the data model.
- **Streaming SQL** (Flink, Kafka Streams) joins streams and tables (event-time join, lookup join) — the same semantics on infinite data.
- **`EXPLAIN` join algorithms** are the first thing engineers read on slow queries: "hash vs nested loop vs merge" tells you memory, order, and index problems at a glance.
- **Data reconciliation** (FULL OUTER JOIN diffs between source and target) is a standard reliability/backfill pattern at every data platform.

## 17. References
- PostgreSQL Documentation, Queries (JOIN): https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN
- PostgreSQL Documentation, EXPLAIN / join types: https://www.postgresql.org/docs/current/using-explain.html
- MySQL Reference Manual, JOIN Syntax: https://dev.mysql.com/doc/refman/8.0/en/join.html
- ISO/IEC 9075-2:2016 (SQL — join semantics).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 3-4 (Join; query processing Ch. 12).
- Elmasri & Navathe, Ch. 5 (Joins).

## 18. Cheat Sheet
- INNER = matches only; LEFT = keep left + NULLs; RIGHT = keep right; FULL = both; CROSS = all pairs.
- ON = join condition (before padding); WHERE = filter (after — kills outer NULLs).
- Self-join: alias the same table twice.
- Duplicate keys multiply rows — check join granularity.
- `NOT IN` breaks with NULLs; use `NOT EXISTS`.
- Anti-join: `LEFT JOIN ... WHERE right.key IS NULL` or `NOT EXISTS`.
- Algorithms: nested-loop O(n·m), hash O(n+m), merge O(n log n + m log m).
- NATURAL JOIN is dangerous (name-coupled); prefer explicit ON/USING.

## 19. Quiz
1. Which join keeps unmatched left rows? a) INNER b) LEFT c) RIGHT d) CROSS → **b**
2. `WHERE right_col IS NOT NULL` on a LEFT JOIN turns it into: a) FULL b) INNER c) RIGHT d) CROSS → **b**
3. Self-joins need: a) subqueries b) table aliases c) window functions d) GROUP BY → **b**
4. CROSS JOIN of 3×4 rows yields: a) 7 b) 12 c) 1 d) 0 → **b**
5. `NOT IN` with a NULL subquery returns: a) some rows b) no rows c) all rows d) error → **b**
6. Hash join complexity (equi): a) O(n·m) b) O(n+m) c) O(log n) d) O(n!) → **b**
7. Anti-join finds: a) matches b) non-matches c) NULLs d) duplicates → **b**
8. Which is safest for the "no match" check? a) NOT IN b) NOT EXISTS c) IN d) = → **b**
9. Duplicate right keys cause: a) fewer rows b) row multiplication c) NULLs d) deadlock → **b**
10. NATURAL JOIN joins on: a) PK b) all common columns c) FK d) index → **b**

## 20. Flashcards
- **Q: 5 join types?** → **A:** INNER, LEFT, RIGHT, FULL OUTER, CROSS.
- **Q: What does LEFT JOIN do with unmatched left rows?** → **A:** Keeps them, pads right columns with NULL.
- **Q: ON vs WHERE in a join?** → **A:** ON decides matches (pre-padding); WHERE filters result (post).
- **Q: What is a self-join?** → **A:** Same table joined to itself via aliases (hierarchies).
- **Q: Why do duplicate keys multiply rows?** → **A:** Each right match pairs with each left row.
- **Q: NOT IN vs NOT EXISTS with NULLs?** → **A:** NOT IN can return nothing; NOT EXISTS is safe.
- **Q: Hash join complexity?** → **A:** O(n+m) — the big-join default.
- **Q: Anti-join query?** → **A:** `LEFT JOIN ... WHERE right.key IS NULL` / `NOT EXISTS`.

## 21. Revision
Joins: **INNER** (matches only), **LEFT/RIGHT** (preserve one side + NULLs), **FULL** (both), **CROSS** (all pairs), **SELF** (aliased same table). Critical rules: `ON` vs `WHERE` — filtering the right side in WHERE reverts LEFT→INNER; `NOT IN` breaks on NULL subqueries (use `NOT EXISTS`); duplicate keys multiply rows (granularity!); anti-join = `LEFT JOIN ... WHERE key IS NULL`. Algorithms: nested-loop O(n·m), hash O(n+m), merge O(n log n). Interview moves: state which join for "all X even with no Y"; demonstrate the WHERE-on-right-trap; write anti-join two ways; and read an `EXPLAIN` join line (hash vs nested). Prefer explicit ON/USING; avoid NATURAL.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "INNER vs LEFT vs FULL?" | 7 / 13 Q1 |
| "Which join for 'all depts even empty'?" | 13 Q11 |
| "WHERE on right table trap?" | 13 Q4 |
| "Anti-join patterns?" | 13 Q7-8 |
| "Why do rows multiply?" | 13 Q6, Q13 |
| "Join algorithms (hash/nested/merge)?" | 13 Q9 |
| "NOT IN vs NOT EXISTS?" | 13 Q8 |
| "Self-join use cases?" | 13 Q3 |
