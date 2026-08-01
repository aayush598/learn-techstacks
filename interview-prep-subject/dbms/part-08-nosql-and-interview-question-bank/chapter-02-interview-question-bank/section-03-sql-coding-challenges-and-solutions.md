# SQL Coding Challenges and Solutions

> **TL;DR**: The live/take-home SQL round distilled into its recurring patterns — window functions, recursive CTEs, gaps-and-islands, deduplication, top-N per group, cumulative sums, date bucketing, and index-aware queries — each with a problem, a trap, and an optimized, commented solution in standard SQL (Postgres-flavored, MySQL-annotated).

## 1. Why Does This Exist?
Live SQL interviews and take-home SQL screens are *pattern-matching* tests: interviewers use a small set of query shapes (rank within a group, running totals, consecutive-day streaks, duplicate detection, date range overlap, self-joins, aggregation with pivoting) and vary the business dressing. This file exists because SQL proficiency in interviews is not about knowing every function — it's about instantly *recognizing* which pattern a problem is and executing the canonical solution, correctly handling the traps (NULLs, off-by-one in date ranges, duplicate rows, the difference between ROW_NUMBER and RANK, WHERE vs HAVING placement). Each challenge here encodes the canonical pattern, the trap interviewers plant, and the optimized solution — so a candidate walks into any SQL round with the full repertoire pre-loaded.

## 2. How Does It Work?
Each challenge is structured as: **Problem** (the prompt), **Schema** (tables), **Trap** (the common failure), **Solution** (SQL, commented), and **Complexity** (what the query does). The patterns are the transferable unit — you learn 15 patterns, not 15 problems:
1. Window functions: `ROW_NUMBER`/`RANK`/`DENSE_RANK`, `LAG`/`LEAD`, `SUM() OVER (...)`, `NTILE`.
2. Top-N per group.
3. Running totals / moving averages.
4. Recursive CTEs (hierarchies, number series, date range expansion).
5. Gaps-and-islands (consecutive days, streaks).
6. Deduplication / keep-one-row-per-key.
7. Pivoting with conditional aggregation.
8. Date arithmetic and bucketing.
9. Self-joins (employee-manager, matching pairs).
10. Correlated subqueries vs JOINs.
11. NULL-handling traps (`NOT IN` with NULLs, `COALESCE`, `NULLS FIRST/LAST`).
12. `EXISTS` vs `IN` vs `JOIN` for anti/semi joins.

## 3. When Is It Used?
- Live SQL interview rounds (shared editor, often LeetCode-style or a company schema).
- Take-home SQL screens (submitted query files; judged on correctness, clarity, index-awareness).
- Hiring-team coding screens where SQL is a must-have skill (data engineering, analytics, backend).
- Rehearsal before the round: run the patterns against a local Postgres/MySQL or an online playground until the syntax is automatic.
- Interviews: "rank employees by salary per department", "find employees who earn more than their manager", "consecutive days logged in", "duplicate emails", "department top-3", "cumulative sales", "streak detection", "pivot by month".

## 4. Why Wasn't Another Approach Chosen?
- *Memorizing 100 bespoke solutions*: the surface area is unbounded; the *patterns* are bounded (~15). Pattern-first training transfers to unseen prompts.
- *Only reading theory*: window-function syntax is easy to know and hard to *execute* under pressure; this file is executable practice, not prose.
- *Avoiding window functions (old-school GROUP BY gymnastics)*: modern interviews expect window functions; the GROUP BY workarounds are longer, error-prone, and a signal of dated skills.
- *Ignoring the traps*: most candidates write correct-looking SQL that fails on one edge (NULLs in `NOT IN`, duplicate rows inflating counts, `<> NULL`); every challenge flags the trap because that's where interviews are won/lost.
- *Focusing on exotic vendors*: the file sticks to standard SQL (portable), with Postgres/MySQL notes — interviews are vendor-agnostic at the pattern level.

## 5. Intuition
Think of the SQL patterns as **knitting stitches**: a sweater isn't memorized row-by-row; it's a small set of stitches (knit, purl, increase, decrease) combined. Each challenge here is a *stitch* — "rank within a group" is one motion; "cumulative sum" is another; "gaps-and-islands" is two stitches combined (a running flag + a running sum). When the interviewer gives you a novel prompt, your job is to *decompose it into stitches*, not to recall a whole garment. "Find the top 2 products by revenue per region" = rank-within-group stitch + a filter on the rank. "Find streaks of logged-in days" = gaps-and-islands (flag + sum). "Compare sales to last year same month" = LAG with date bucketing. The traps are the moments you'd drop a stitch: forgetting `DENSE_RANK` (ties), forgetting to `GROUP BY` after the window, or letting NULLs break `NOT IN`. Practice the stitches until each is automatic — then any prompt is just a combination.

## 6. Real-World Analogy
A **data analyst's swiss army knife**. When a business asks "what were the top 3 stores this quarter?" the analyst doesn't start from scratch — she reaches for the *rank-within-group* blade. "How many customers came back within 30 days?" → the *date-difference + self-join* blade. "Which weeks had zero sales?" → the *series generation* blade (generate the expected weeks, LEFT JOIN, filter NULL). Each blade is a known, tested motion; a novel question is recognized as "this is really the *running-total* blade with a different dressing." A skilled analyst isn't faster because she's memorized a thousand queries — she's faster because her *blade set* is small and sharp, and recognizing which blade fits is instant. This file is that blade set, sharpened and labeled, plus the warning of each blade's blunt edge (the trap).

## 7. Formal Definition
Canonical SQL patterns (standard SQL:2023, with engine notes):
- **Window functions**: `f(x) OVER (PARTITION BY cols ORDER BY cols [ROWS/RANGE frame])` — compute a function over a sliding/partitioned window *without* collapsing rows (unlike GROUP BY).
- **Ranking family**: `ROW_NUMBER()` (unique sequential), `RANK()` (ties share, gaps), `DENSE_RANK()` (ties share, no gaps), `NTILE(n)` (buckets).
- **Offset/lag**: `LAG(x, k, default) OVER (...)` — previous row's value; `LEAD` — next.
- **Aggregate over window**: `SUM(x) OVER (PARTITION BY ... ORDER BY ...)` — running total (default frame RANGE UNBOUNDED PRECEDING to CURRENT ROW).
- **Recursive CTE**: `WITH RECURSIVE t AS (anchor UNION ALL recursive_term)` — for hierarchies and series.
- **Gaps-and-islands**: assign a group id via `SUM(flag) OVER (ORDER BY ...)` where flag=1 when the gap breaks (e.g., `date - LAG(date)` ≠ 1 day).
- **Pivot**: `SUM(CASE WHEN ... THEN val END) AS col` conditional aggregation.

## 8. Example
**Problem**: Find the top-2 best-selling products per region for 2026 Q1.
**Schema**: `sales(region, product, qty, sale_date)`.
**Trap**: Forgetting ties (two products tie for #2) → use `DENSE_RANK`, not `ROW_NUMBER`; or forgetting the outer filter can't reference the window alias in the same SELECT → wrap in a subquery.
**Solution**:
```sql
WITH ranked AS (
  SELECT region, product,
         SUM(qty) AS total,
         DENSE_RANK() OVER (PARTITION BY region ORDER BY SUM(qty) DESC) AS rnk
  FROM sales
  WHERE sale_date BETWEEN '2026-01-01' AND '2026-03-31'
  GROUP BY region, product
)
SELECT region, product, total
FROM ranked
WHERE rnk <= 2
ORDER BY region, rnk;
```
**Complexity**: one scan + one window sort per region partition — index on `(sale_date)` or `(region, sale_date)` helps the WHERE; the window sort is unavoidable for the ranking.

## 9. Internal Working
Each pattern compiles to a known execution shape:
- **Window functions** add a *window aggregate* step after the WHERE/JOIN/GROUP BY, sorting by the `ORDER BY` per partition — plan shows a `Sort` or uses an index order when available (Part 07).
- **Recursive CTEs** run as iterative *WorkTableScan* loops (bounded by a `UNION ALL` terminator) — the engine materializes each level.
- **Gaps-and-islands** = two passes: (1) compute `lag`/difference flag; (2) running `SUM` over the flag → group id; (3) GROUP BY the group id. Execution: two window sorts (or one with a compound order).
- **Pivot via CASE** = conditional aggregate; plan shows a hash/grouped aggregate on the CASE expressions.
- **Anti/semi joins** (`NOT IN` vs `NOT EXISTS` vs LEFT JOIN ... WHERE NULL): optimizers rewrite equivalent forms, but *NULL semantics differ* — `NOT IN (subquery)` returns *no rows* if the subquery contains any NULL; `NOT EXISTS` is NULL-safe. That trap alone decides correctness, not speed.
- **Index-awareness**: a WHERE on an indexed column turns the scan into an index scan (Part 04/07); window sorts benefit from indexes matching the PARTITION/ORDER keys; `WHERE sale_date BETWEEN` benefits from a date index + partition pruning on date-partitioned tables.

## 10. Time Complexity
- Window sort: O(n log n) worst per partition (or O(n) if the order matches an index), memory-bound (`work_mem`/`sort_buffer_size` — Part 07 §3; spills when exceeded).
- Recursive CTE: O(sum of per-level rows) — depth × breadth; exponential in pathological trees (guard with `LEVEL` limits).
- Gaps-and-islands: O(n) for the flag pass + O(n log n) for the running sum sort → O(n log n) dominant.
- Pivot: O(n) aggregate over CASE columns.
- The *interview* time complexity is really about *correctness* first: a query that "runs" is worse than a query that's right; then optimize the hot filter with an index (Part 04).

## 11. Advantages
- **Transfers to any prompt**: 15 patterns cover the overwhelming majority of live-SQL questions.
- **Traps called out**: the exact spots candidates fail are named per challenge — rehearsing the traps is rehearsing the win.
- **Optimized, not just correct**: solutions are index-aware and mention `EXPLAIN` verification (Part 07).
- **Vendor-portable core** with Postgres/MySQL notes.
- **Executable**: each solution can be run on a local DB or playground for drill.
- **Interview-relevant**: these are the shapes companies actually use.

## 12. Disadvantages
- **Window-sort cost** can blow up on huge partitions (memory/disk spill) — the "correct" query may need a different design at scale (pre-aggregation).
- **Recursive CTEs** are elegant but can be slow/loopy on deep trees; some engines have iteration limits.
- **Vendor quirks** still bite: `ROW_NUMBER` over `NULL` handling, `FILTER (WHERE ...)` (Postgres) vs `CASE` (portable), `DISTINCT ON` (Postgres-only).
- **Over-focusing on syntax** risks missing the interviewer's real intent (e.g., asking for the *slowest* store, ties included).
- **No production schema context**: a correct pattern still needs the actual data shape (indexes, duplicates) — the file can't know the schema you'll face.

## 13. Interview Questions
1. **Q: Top-N per group (per department top-3 salaries).** A: `DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC)`, filter rnk≤3 in an outer query. Use `DENSE_RANK` to include ties; `ROW_NUMBER` if exactly N rows needed. → §2/8
2. **Q: Running total (cumulative sales by date).** A: `SUM(qty) OVER (PARTITION BY product ORDER BY sale_date)` — the default frame runs to current row. Trap: without `ORDER BY` inside OVER, the frame is the whole partition (not a running total). → §2
3. **Q: TRICKY: Employees who earn more than their manager.** A: Self-join `employee e JOIN employee m ON e.manager_id = m.id WHERE e.salary > m.salary` — no window needed. Trap: NULL manager_id (the CEO) — INNER JOIN naturally excludes them. → §2
4. **Q: Deduplicate rows keeping the latest per key.** A: `ROW_NUMBER() OVER (PARTITION BY key ORDER BY updated_at DESC) = 1` (or `DISTINCT ON (key) ORDER BY key, updated_at DESC` in Postgres). Trap: forget which version is "latest" (timestamp vs id). → §2
5. **Q: Consecutive-day login streaks.** A: Gaps-and-islands: flag `(day - LAG(day)) > 1` per user, `SUM(flag) OVER (PARTITION BY user ORDER BY day)` → group id, then `COUNT(*)` per (user, group). Trap: duplicate logins per day must be deduped first (`SELECT DISTINCT`), else a "gap" appears. → §2
6. **Q: TRICKY: Find all dates with no sales in a range.** A: Generate the series (`generate_series` in Postgres / recursive CTE elsewhere), LEFT JOIN sales, filter WHERE NULL. Trap: never scan "missing" — you must generate the expected universe. → §2
7. **Q: Duplicate emails in a users table.** A: `GROUP BY email HAVING COUNT(*) > 1` — the classic; HAVING filters groups (Part 02 §26). → §2
8. **Q: Moving 30-day average of revenue.** A: `AVG(revenue) OVER (PARTITION BY product ORDER BY day ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)` — the explicit frame is the pattern. Trap: default frames differ between RANGE (ties included) and ROWS. → §2
9. **Q: Second-highest salary overall.** A: `DISTINCT salary ORDER BY salary DESC OFFSET 1 LIMIT 1` (or `FETCH FIRST 1 ROW ONLY`), or `MAX(salary) WHERE salary < (SELECT MAX(salary)...)`. Trap: ties and "second distinct vs second row". → §2
10. **Q: TRICKY: `NOT IN` with a subquery returns nothing — why?** A: If the subquery contains any NULL, `NOT IN` (which is `<> ALL`) evaluates NULL → no rows. Fix: `NOT EXISTS` (NULL-safe) or exclude NULLs in the subquery. Classic NULL trap. → §2/9
11. **Q: Pivot: monthly sales by region (rows=region, cols=month).** A: Conditional aggregation: `SUM(CASE WHEN month=1 THEN amount END) AS jan, ...` — portable; Postgres can also use `FILTER (WHERE month=1)`. → §2
12. **Q: Compare each month's sales to the previous month.** A: `LAG(amount, 1) OVER (ORDER BY month)` then compute `amount - lag`. Trap: the first row's LAG is NULL — `COALESCE` or exclude it. → §2
13. **Q: TRICKY: Find pairs of orders from the same customer within 7 days (at-least-once ordering).** A: Self-join `o1.user_id = o2.user_id AND o1.id < o2.id AND o2.created_at - o1.created_at BETWEEN 0 AND 7` (dedupe with `o1.id < o2.id`). Trap: missing the `id < id` guard → duplicate pairs. → §2
14. **Q: Number of users active every day for the last 7 days.** A: `GROUP BY user HAVING COUNT(DISTINCT day) = 7` with `WHERE day >= CURRENT_DATE - 7` — but ensure the 7 days *exist* in data (missing days ≠ inactive). → §2
15. **Q: TRICKY: "Which products are in the top 10 by revenue AND have > 100 reviews?"** A: Two filters that operate at different stages: rank within a window over revenue, then a *separate* aggregate on reviews — combine in one subquery with `HAVING COUNT(*) > 100` per product before ranking, or filter reviews in the outer query. The trap is mixing row-level (reviews) and group-level (revenue rank) conditions in one SELECT. → §2
16. **Q: Retrieve the most recent order per customer with order details.** A: `DISTINCT ON (customer_id) ... ORDER BY customer_id, created_at DESC` (Postgres) or ROW_NUMBER = 1. Trap: "most recent" must tie-break deterministically (id desc). → §2
17. **Q: Percentage contribution of each product to total revenue.** A: `SUM(amount) / SUM(SUM(amount)) OVER () * 100` — window aggregate over the grouped sum (double aggregate pattern). Trap: missing the inner GROUP BY → sums rows twice. → §2
18. **Q: Employees whose salary is above their department average.** A: Correlated subquery or window: `AVG(salary) OVER (PARTITION BY dept)` compared per row. Prefer the window (single scan). → §2
19. **Q: TRICKY: Delete duplicate rows keeping the lowest id.** A: `DELETE FROM t WHERE id NOT IN (SELECT MIN(id) FROM t GROUP BY (key1, key2))` — or with a window `ROW_NUMBER() OVER (PARTITION BY key ORDER BY id) > 1`. Trap: the self-reference during DELETE (Postgres requires a subquery/CTE materialization; use `DELETE FROM t USING t2 ...` or wrap). → §2
20. **Q: Fill missing months with zeros for a reporting series.** A: Generate months (`generate_series`), LEFT JOIN data, `COALESCE(amount, 0)`. The "generate + left join + coalesce" trio. → §2

## 14. Follow-Up Questions
1. **Q: "How would you make this faster on 100M rows?"** → Index the WHERE filter, consider a covering index for the SELECT columns, use date partitioning for the range, and check `EXPLAIN` (Part 07).
2. **Q: "Does your answer change if ties matter?"** → RANK/DENSE_RANK vs ROW_NUMBER — name the semantic difference explicitly.
3. **Q: "What if the data has NULLs in the key/salary column?"** → State the behavior: NULLs in window `PARTITION BY` form their own partition; `ORDER BY ... NULLS FIRST/LAST`; NULL-safe anti-joins (`NOT EXISTS`).
4. **Q: "Write it without a window function."** → Provide the GROUP BY/correlated-subquery equivalent (the interviewer is probing understanding, not just syntax).

## 15. Coding Example
```sql
-- Gaps-and-islands: longest consecutive login streak per user
WITH daily AS (                       -- dedupe first (trap!)
  SELECT DISTINCT user_id, login_date
  FROM logins
),
flagged AS (
  SELECT user_id, login_date,
         login_date - LAG(login_date) OVER (PARTITION BY user_id ORDER BY login_date)
           AS gap
  FROM daily
),
groups AS (
  SELECT user_id, login_date,
         SUM(CASE WHEN gap > 1 OR gap IS NULL THEN 1 ELSE 0 END)
           OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM flagged
)
SELECT user_id, MIN(login_date) AS start, MAX(login_date) AS end,
       COUNT(*) AS streak_days
FROM groups
GROUP BY user_id, grp
ORDER BY streak_days DESC;
```
```sql
-- Top-N per group + running total, in one query (combined patterns)
WITH per_region AS (
  SELECT region, product, SUM(qty) AS total
  FROM sales WHERE sale_date BETWEEN '2026-01-01' AND '2026-03-31'
  GROUP BY region, product
),
ranked AS (
  SELECT region, product, total,
         DENSE_RANK() OVER (PARTITION BY region ORDER BY total DESC) AS rnk,
         SUM(total) OVER (PARTITION BY region ORDER BY total DESC
                          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
           AS running_total
  FROM per_region
)
SELECT region, product, total, running_total
FROM ranked WHERE rnk <= 3;
```
```sql
-- NULL-safe anti-join: customers with no orders (NOT IN trap avoided)
SELECT c.id, c.name
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
-- vs the trap:
-- WHERE c.id NOT IN (SELECT customer_id FROM orders)  -- WRONG if customer_id can be NULL
```

## 16. Industry Usage
- **Live SQL rounds** (LeetCode-style, company editors) test exactly these patterns; the top-LC database problems map 1:1 (rank scores, second-highest, department top-3, consecutive days, duplicate emails, customer orders).
- **Data engineering/analytics hires** (Stripe, Shopify, Airbnb tracks, FAANG data roles) use these as the screening floor; take-home SQL screens judge readability + index-awareness + trap-avoidance.
- **Backend engineers** are expected to write window/aggregate SQL for reports and ETL snippets.
- **DBA/DBRE roles** extend it to `EXPLAIN` verification and partitioning (Parts 04/07).

## 17. References
- LeetCode Database problems (select patterns: https://leetcode.com/problemset/database/).
- Use The Index, Luke — practical SQL + indexing: https://use-the-index-luke.com/
- PostgreSQL docs, "Window Functions": https://www.postgresql.org/docs/current/tutorial-window.html
- MySQL docs, "Window Functions": https://dev.mysql.com/doc/refman/8.0/en/window-functions.html
- DataLemur (Nick Singh) and StrataScratch SQL practice libraries.

## 18. Cheat Sheet
- Window function anatomy: `f() OVER (PARTITION BY ... ORDER BY ... [frame])`.
- ROW_NUMBER (unique) / RANK (ties+gap) / DENSE_RANK (ties, no gap) — choose by ties semantics.
- LAG/LEAD: previous/next row; default = NULL (COALESCE it).
- Running total: `SUM(x) OVER (PARTITION BY k ORDER BY d)` (default frame to current row).
- Explicit frame: `ROWS BETWEEN N PRECEDING AND CURRENT ROW` for moving windows; RANGE includes ties.
- Gaps-and-islands: dedupe → flag gap → running SUM = group id → COUNT per group.
- Top-N: window rank + outer filter (can't reference window alias in same SELECT).
- Series/missing data: generate_series / recursive CTE + LEFT JOIN + COALESCE.
- Anti-join: prefer NOT EXISTS (NULL-safe); NOT IN dies on any NULL.
- Pivot: `SUM(CASE WHEN ... END)`; Postgres `FILTER (WHERE ...)`.
- NULL traps: `<> NULL` never true; `NULLS FIRST/LAST`; NULL forms its own window partition.
- Index-aware: WHERE/join filters → index; window ORDER → matching index avoids sort; date range → date index/partition.
- Double aggregate: `SUM(SUM(x) OVER ())` or wrap grouping first.

## 19. Quiz
1. Include ties in top-N? a) ROW_NUMBER b) DENSE_RANK c) LIMIT d) OFFSET → **b**
2. Running total needs: a) GROUP BY b) ORDER BY inside OVER c) WHERE d) HAVING → **b**
3. `NOT IN` with NULL subquery returns: a) rows b) nothing c) error d) NULLs → **b**
4. Moving 30-day average uses: a) ROWS frame b) default frame c) LAG d) PARTITION → **a**
5. Missing dates in range requires: a) HAVING b) generate series + LEFT JOIN c) self-join d) pivot → **b**
6. Gap flag → running sum produces: a) rank b) group id c) running total d) pivot → **b**
7. LAG's first-row value is: a) 0 b) NULL c) itself d) next → **b**
8. Pivot = : a) window b) conditional aggregation c) recursion d) LAG → **b**

## 20. Flashcards
- **Q: RANK vs DENSE_RANK?** → **A:** Both share ties; RANK gaps, DENSE_RANK doesn't.
- **Q: Running total?** → **A:** SUM(x) OVER (PARTITION BY k ORDER BY d).
- **Q: Top-N per group?** → **A:** Window rank + outer WHERE rnk<=N.
- **Q: NOT IN with NULLs?** → **A:** Returns nothing — use NOT EXISTS.
- **Q: Streak detection?** → **A:** Gaps-and-islands (flag + running sum + count).
- **Q: Missing dates?** → **A:** generate_series + LEFT JOIN + COALESCE.
- **Q: Moving average frame?** → **A:** ROWS BETWEEN N PRECEDING AND CURRENT ROW.
- **Q: Previous row value?** → **A:** LAG(x, 1) — first row NULL.

## 21. Revision
SQL rounds are pattern-matching: window functions (rank families, LAG/LEAD, running totals, explicit frames), recursive CTEs, gaps-and-islands, dedup (keep latest), top-N per group, series generation for missing data, NULL-safe anti-joins (NOT EXISTS), and conditional-aggregation pivots. Every prompt → decompose into stitches; every solution → check the trap (ties, NULLs, duplicate rows, frame defaults). Make it index-aware and verify with EXPLAIN. Practice until the syntax is automatic — the patterns are bounded, the problems are infinite.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Top-N per group" | 8, 13 |
| "Running total / moving average" | 2, 8, 13 |
| "Consecutive-day streaks" | 8, 13 |
| "Deduplicate keeping latest" | 2, 13 |
| "NOT IN NULL trap" | 9, 13 |
| "Missing dates / series" | 8, 13 |
| "Second-highest / ranks" | 8, 13 |
| "Employees earning more than manager" | 8, 13 |
| "Pivot by month" | 8, 13 |
| "Delete duplicates keeping lowest id" | 13 |
