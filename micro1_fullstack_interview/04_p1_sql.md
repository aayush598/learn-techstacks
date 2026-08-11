# Priority 1 — SQL (Q121–Q175)

**Why these matter for micro1:** the role requires "writing and debugging SQL queries" and "data modeling for reliable data operations." Expect live query-writing, query tuning (EXPLAIN), and design questions. The AI recruiter stores candidates/jobs/interviews in PostgreSQL.

**Schema used throughout these examples:**
```sql
users(id, name, email, created_at)
orders(id, user_id FK, amount, status, created_at)
```

---

## Q121: How comfortable are you with SQL?

**Answer with evidence + range:**
- "I'm very comfortable — I write SQL daily for backend features, reporting, and debugging: complex joins, aggregations, window functions, CTEs, and query tuning with EXPLAIN."
- Name real work: pagination queries, dashboard aggregations, dedup, N+1 fixes, index tuning in PostgreSQL.
- Mention tooling: SQLAlchemy (ORM + core), Alembic migrations, psycopg2/asyncpg, EXPLAIN ANALYZE, pg_stat statements.
- Close: "I also know when to reach for the ORM vs raw SQL and how to keep both correct and fast."

> Follow-up prep: they'll likely ask you to *write* a query next (joins, group by, window functions). Be ready to write on the spot.

---

## Q122: Write a query to retrieve users from a database.

```sql
SELECT id, name, email FROM users;

SELECT * FROM users WHERE email LIKE '%@company.com' ORDER BY created_at DESC LIMIT 50;
```

- Always list columns explicitly (readability, index friendliness, avoids surprises).
- Filter with `WHERE`, order with `ORDER BY`, limit with `LIMIT`.

---

## Q123: What is the difference between `WHERE` and `HAVING`?

- **WHERE** filters **rows** *before* grouping.
- **HAVING** filters **groups** *after* aggregation.

```sql
-- users with >2 orders (groups)
SELECT user_id, COUNT(*) AS cnt
FROM orders
WHERE status != 'cancelled'        -- filters rows first
GROUP BY user_id
HAVING COUNT(*) > 2;               -- filters groups after

-- Note: aggregate functions are NOT allowed in WHERE
-- WHERE COUNT(*) > 2  →  error
```

Order of operations: `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`.

---

## Q124: What does `GROUP BY` do?

Collapses rows with equal values in the grouped columns into one row per group, so you can run **aggregate functions** per group.

```sql
SELECT user_id, COUNT(*) AS order_count, SUM(amount) AS total
FROM orders
GROUP BY user_id;
```

- Every non-aggregated column in `SELECT` must appear in `GROUP BY` (or be functionally dependent on it).
- Aggregates: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `ARRAY_AGG`, `STRING_AGG`.
- `GROUP BY` can use positional references (`GROUP BY 1`) but that's fragile — use names.
- Add `GROUP BY ROLLUP/CUBE/GROUPING SETS` (PostgreSQL) for subtotals.

---

## Q125: What is the difference between `COUNT(*)` and `COUNT(column)`?

- `COUNT(*)` — counts **all rows** in the group, including NULLs.
- `COUNT(column)` — counts **non-NULL values** of that column.

```sql
SELECT COUNT(*) AS all_rows, COUNT(email) AS with_email FROM users;
-- 1000 rows, but only 950 have email → 1000 / 950
```

- Related: `COUNT(DISTINCT column)` counts distinct non-null values.

---

## Q126: What is an INNER JOIN?

Returns rows that have **matching values in both tables** — unmatched rows are excluded from both sides.

```sql
SELECT u.name, o.id AS order_id
FROM users u
INNER JOIN orders o ON o.user_id = u.id;
-- only users who have at least one order appear
```

- If one user has many orders, rows multiply (one user row per matching order) — this is the join's cardinality behavior.
- `JOIN` == `INNER JOIN`.

---

## Q127: What is a LEFT JOIN?

Returns **all rows from the left table**, plus matching rows from the right; where there's no match, right-side columns are `NULL`.

```sql
SELECT u.name, o.id
FROM users u
LEFT JOIN orders o ON o.user_id = u.id;
-- every user appears; users without orders get NULL for o.id
```

- Use for: "all X, with their Y if any" (e.g., all users and their orders).
- Check for NULL to find rows without matches: `WHERE o.id IS NULL`.

---

## Q128: What is the difference between INNER JOIN and LEFT JOIN?

| | INNER JOIN | LEFT JOIN |
|---|---|---|
| Left rows without match | Excluded | Kept (right cols NULL) |
| Right rows without match | Excluded | Excluded |
| Typical use | Only pairs that exist | "All X plus optional Y" |

```sql
INNER → only users who have orders
LEFT  → all users, orders optional
```

Also related: `RIGHT JOIN` (mirror of LEFT), `FULL OUTER JOIN` (keep both sides), `CROSS JOIN` (Cartesian).

---

## Q129: When would you use a RIGHT JOIN?

A `RIGHT JOIN` returns all rows from the **right** table with matches from the left. In practice you almost never write one — **rewrite as LEFT JOIN** (swap tables) for readability, since LEFT is the convention.

```sql
-- same result:
SELECT * FROM orders o RIGHT JOIN users u ON o.user_id = u.id;
SELECT * FROM users u LEFT JOIN orders o ON o.user_id = u.id;
```

---

## Q130: What is a FULL OUTER JOIN?

Returns **all rows from both tables**, matched where possible, `NULL` elsewhere — the union of LEFT and RIGHT joins.

```sql
SELECT u.name, o.id
FROM users u
FULL OUTER JOIN orders o ON o.user_id = u.id;
-- users without orders AND orders without matching user both appear
```

- Use: reconciling two lists (e.g., candidates vs interviews) where either side may lack matches.
- Find unmatched from both sides: `WHERE u.id IS NULL OR o.user_id IS NULL`.

---

## Q131: What is a CROSS JOIN?

Every row of table A paired with **every row** of table B — the **Cartesian product**. No `ON` clause.

```sql
SELECT * FROM colors CROSS JOIN sizes;   -- red×S, red×M, ..., blue×S ...
```

- Result rows = `len(A) × len(B)` — can explode; use deliberately (combinations, permutations, calendar × symbols) and guard with filters.

---

## Q132: What is a SELF JOIN?

Joining a table **to itself** (using aliases) — useful when relationships live inside one table (hierarchy, adjacency, comparisons within the same table).

```sql
-- employees with their manager
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;

-- pairs of users in the same city
SELECT a.name, b.name FROM users a JOIN users b ON a.city = b.city AND a.id < b.id;
```

- Always use aliases; decide `INNER` vs `LEFT` (manager may be null).

---

## Q133: How do you join three tables?

Chain joins; each `ON` clause ties two tables.

```sql
SELECT u.name, o.id AS order_id, p.name AS product
FROM users u
JOIN orders o ON o.user_id = u.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id;
```

- Order of joins doesn't change the result (optimizer reorders), only readability.
- Keep ON conditions precise; beware unintentional row multiplication (fan-out) when both order_items and products join.

---

## Q134: How do you find duplicate records?

```sql
SELECT email, COUNT(*)
FROM users
GROUP BY email
HAVING COUNT(*) > 1;
```

To list the actual duplicate rows (PostgreSQL):

```sql
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS rn
  FROM users
) t WHERE rn > 1;
```

- Define the dedup key (what makes a row "duplicate") first.

---

## Q135: How do you remove duplicate records?

Keep the lowest id per email, delete the rest (PostgreSQL):

```sql
DELETE FROM users
WHERE id NOT IN (
  SELECT MIN(id) FROM users GROUP BY email
);
```

Or with a window function (more explicit):

```sql
DELETE FROM users
WHERE id IN (
  SELECT id FROM (
    SELECT id, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS rn
    FROM users
  ) t WHERE rn > 1
);
```

- **Backup first!** Delete inside a transaction; test the `SELECT` before running `DELETE`.
- In production, prefer soft-dedupe (mark) + unique index for prevention: `CREATE UNIQUE INDEX ... ON users(lower(email))`.

---

## Q136: How do you find the second-highest salary?

```sql
-- Method 1: OFFSET (simple; no ties)
SELECT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 1;

-- Method 2: DENSE_RANK (handles ties — the "2nd distinct value")
SELECT salary FROM (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employees
) t WHERE rnk = 2;

-- Method 3: scalar subquery
SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);
```

- **Interview nuance:** ask whether ties count. `LIMIT 1 OFFSET 1` fails on ties; `DENSE_RANK` gives the 2nd distinct salary.

---

## Q137: How do you find the top N records?

```sql
SELECT * FROM employees ORDER BY salary DESC LIMIT 10;

-- per group (top 3 per department):
SELECT * FROM (
  SELECT e.*, ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rn
  FROM employees e
) t WHERE rn <= 3;
```

- Plain top-N: `ORDER BY ... LIMIT N`.
- Top-N-per-group: window function with `PARTITION BY` + `ROW_NUMBER`.

---

## Q138: How do you find users who have never placed an order?

```sql
-- LEFT JOIN + NULL check
SELECT u.id, u.name
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE o.id IS NULL;

-- NOT EXISTS (often clearer + efficient, especially large tables)
SELECT id, name FROM users u
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);
```

- `NOT EXISTS` short-circuits per row and is usually the preferred form.

---

## Q139: How do you count orders for each user?

```sql
SELECT u.id, u.name, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.name
ORDER BY order_count DESC;
```

- `LEFT JOIN` so users with zero orders show `0` (COUNT ignores NULLs → 0).
- `COUNT(o.id)` not `COUNT(*)` — `COUNT(*)` would count the NULL row too (giving 1 for no-order users).
- Always group by all non-aggregate selected columns (PostgreSQL can infer by PK but be explicit).

---

## Q140: How do you find the highest-value customer?

```sql
SELECT u.id, u.name, SUM(o.amount) AS total_spent
FROM users u
JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.name
ORDER BY total_spent DESC
LIMIT 1;
```

- For "highest total," order by the aggregate and `LIMIT 1`.
- Per-period version: add a `WHERE o.created_at >= ...` or group by date.

---

## Q141: How do you find records created within a specific date range?

```sql
SELECT * FROM orders
WHERE created_at >= '2026-01-01' AND created_at < '2026-02-01';

-- PostgreSQL date range operators
WHERE created_at BETWEEN '2026-01-01' AND '2026-01-31 23:59:59';
WHERE created_at::date = CURRENT_DATE;               -- today (all day)
WHERE created_at >= NOW() - INTERVAL '7 days';
```

- Prefer **half-open ranges** (`>= start AND < end`) for correctness with timestamps.
- Function on the column (`DATE(created_at)`) kills index usage — use a range on the raw column instead.

---

## Q142: What is a subquery?

A `SELECT` nested inside another query (in `SELECT`, `WHERE`, `FROM`, `JOIN`).

```sql
-- scalar subquery in SELECT
SELECT name, (SELECT MAX(amount) FROM orders WHERE user_id = u.id) AS max_order
FROM users u;

-- subquery in WHERE (IN)
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE amount > 500);

-- derived table in FROM
SELECT dept, AVG(salary) FROM (SELECT * FROM employees WHERE active) t GROUP BY dept;
```

- Types: scalar (one value), row, table (derived), correlated (references outer query, Q143).
- Optimizer often flattens subqueries into joins; correctness first, then tune.

---

## Q143: What is a correlated subquery?

A subquery that **references a column from the outer query** — evaluated **per outer row** (like a nested loop).

```sql
SELECT u.name
FROM users u
WHERE (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) > 3;
-- inner query re-runs for each user u
```

- **vs uncorrelated:** uncorrelated subquery runs once; correlated runs once per outer row → potentially slow without good indexing.
- Often rewritten as `GROUP BY`/`HAVING` or `JOIN` + `EXISTS`.

---

## Q144: What is a CTE?

**Common Table Expression** — a named, temporary result set defined with `WITH` before the main query; it reads like a variable/subquery, scoped to that statement.

```sql
WITH high_value_users AS (
  SELECT user_id, SUM(amount) AS total
  FROM orders
  GROUP BY user_id
  HAVING SUM(amount) > 1000
)
SELECT u.name, hv.total
FROM users u JOIN high_value_users hv ON hv.user_id = u.id;
```

- **Recursive CTEs** allow hierarchical queries (org trees, graph traversal): `WITH RECURSIVE ... UNION ALL ...`.
- Multiple CTEs: `WITH a AS (...), b AS (...) SELECT ...`.
- CTEs are often **materialization/optimization fences** in PostgreSQL (executed once, or inlined depending on version) — don't assume; check EXPLAIN.

---

## Q145: Why would you use a CTE?

1. **Readability** — name a complex subquery, reuse it several times in one statement.
2. **Modularity** — break a big query into logical steps.
3. **Recursion** — `WITH RECURSIVE` for trees/graphs (org hierarchy, BOM).
4. **Avoid repetition** — reference the same intermediate result multiple times.
5. **Testability** — build and check each CTE independently.
- **Caveat:** PostgreSQL historically materializes CTEs (no push-down); PG12+ inlines non-recursive ones when safe. Use CTEs for clarity; if slow, check EXPLAIN and consider rewriting as a subquery/join.

---

## Q146: What are window functions?

Functions that compute a value across a **set of rows related to the current row** *without collapsing them into a group*. They keep all rows and add a computed column.

```sql
SELECT
  user_id, amount,
  SUM(amount) OVER (PARTITION BY user_id) AS user_total,     -- running/group total
  ROW_NUMBER() OVER (ORDER BY amount DESC) AS rank_no,       -- ranking
  LAG(amount) OVER (PARTITION BY user_id ORDER BY created_at) AS prev_amount
FROM orders;
```

Parts: `function() OVER ([PARTITION BY ...] [ORDER BY ...] [ROWS/RANGE frame])`.
- Partition = "group by" for the window (default: whole set).
- ORDER BY inside OVER controls ordering/ranking and running frames.
- Aggregates (`SUM`, `AVG`, `COUNT`), ranking (`ROW_NUMBER`, `RANK`, `DENSE_RANK`), offsets (`LAG`, `LEAD`), distribution (`NTILE`, `PERCENT_RANK`).
- **vs GROUP BY:** GROUP BY reduces rows; window functions don't.

---

## Q147: What is `ROW_NUMBER()`?

Assigns a **sequential number (1,2,3...) to each row within a partition**, ordered by the `ORDER BY`. Ties are broken arbitrarily — no two rows share a number.

```sql
SELECT user_id, amount,
       ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn
FROM orders;
-- rn=1 is the user's most recent order
```

- Workhorse for "top N per group" and dedup.

---

## Q148: What is `RANK()`?

Like ROW_NUMBER but ties share the same rank; **gaps** appear after ties.

```sql
-- salaries 100, 90, 90, 80
RANK()       → 1, 2, 2, 4
```

---

## Q149: What is `DENSE_RANK()`?

Ties share the same rank but **no gaps**:

```sql
-- salaries 100, 90, 90, 80
DENSE_RANK() → 1, 2, 2, 3
```

---

## Q150: What is the difference between ROW_NUMBER, RANK, and DENSE_RANK?

| Function | Ties share rank? | Gaps after ties? | Numbers unique? |
|---|---|---|---|
| `ROW_NUMBER` | No (arbitrary order) | n/a | Yes (1..N) |
| `RANK` | Yes | Yes (gaps) | No |
| `DENSE_RANK` | Yes | No | No |

```sql
-- scores 10, 10, 8, 7
ROW_NUMBER  → 1, 2, 3, 4
RANK        → 1, 1, 3, 4
DENSE_RANK  → 1, 1, 2, 3
```

- Use `DENSE_RANK` when you want "2nd best distinct value"; `RANK` for competition standings with gaps; `ROW_NUMBER` for pagination/dedup.

---

## Q151: What are `LAG()` and `LEAD()`?

Access a value from a **previous (`LAG`) or next (`LEAD`)** row within the partition/order — for comparing with neighbors (time-series diffs, deltas).

```sql
SELECT
  created_at, amount,
  LAG(amount)  OVER (ORDER BY created_at) AS prev_amount,
  amount - LAG(amount) OVER (ORDER BY created_at) AS delta,
  LEAD(amount) OVER (ORDER BY created_at) AS next_amount
FROM orders;
```

- Optional offset/`default`: `LAG(amount, 2, 0)` — look 2 rows back, default 0.
- Use: day-over-day changes, session boundaries, gaps detection.

---

## Q152: What is a transaction?

A sequence of SQL operations executed **as one atomic unit** — all succeed or all are rolled back.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;   -- or ROLLBACK on error
```

- Guarantees: ACID (Q153).
- Multi-statement business operations (transfer, order + stock decrement) must be transactional to avoid partial state.
- Keep transactions short; never hold them across user interaction/network calls.

---

## Q153: What is ACID?

- **Atomicity** — all or nothing: partial failures roll back the whole transaction.
- **Consistency** — a transaction moves the DB from one valid state to another (constraints/invariants hold).
- **Isolation** — concurrent transactions don't see each other's partial work (levels: READ UNCOMMITTED → SERIALIZABLE; PostgreSQL default READ COMMITTED; PostgreSQL has no READ UNCOMMITTED).
- **Durability** — committed data survives crashes (WAL + fsync).

PostgreSQL notes: uses **MVCC** (Q335) for isolation; durability via the **WAL** (write-ahead log).

---

## Q154: What is a primary key?

A column (or column set) that **uniquely identifies each row**; not null + unique, and typically indexed.

```sql
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,   -- auto-incrementing
  email TEXT UNIQUE NOT NULL
);
```

- One per table; the DB enforces uniqueness; other tables reference it via foreign keys.
- Prefer **surrogate keys** (auto-increment `id` / UUID) for stability; natural keys (email) often change.

---

## Q155: What is a foreign key?

A column referencing a **primary key in another table**, enforcing referential integrity — you can't reference a row that doesn't exist.

```sql
CREATE TABLE orders (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
  amount NUMERIC
);
```

- `ON DELETE`: `CASCADE`, `SET NULL`, `RESTRICT`, `NO ACTION`.
- Requires an index on the FK column for fast joins (PostgreSQL doesn't auto-index FKs).
- Enables the relational model: users → orders → items.

---

## Q156: What is a unique constraint?

Guarantees **no duplicate values** in a column/column-set across the table (NULLs are allowed to repeat in PostgreSQL — NULL ≠ NULL).

```sql
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email TEXT UNIQUE,               -- unique constraint (creates index)
  UNIQUE (tenant_id, email)        -- composite unique
);
```

- Enforces business rules (email uniqueness, one active session per user) at the DB level.
- Creates a unique index automatically — also serves lookups.

---

## Q157: What is normalization?

Designing schemas to **reduce redundancy and anomalies** by organizing columns into related tables and applying normal forms:

- **1NF:** atomic values, no repeating groups.
- **2NF:** 1NF + every non-key column depends on the whole key (no partial dependency).
- **3NF:** 2NF + no transitive dependency (non-key depends only on the key).
- **BCNF:** every determinant is a candidate key.

**Example:** instead of repeating `user_name` on every order row, store users once and reference `user_id` (FK) from orders. Benefits: no duplication, single source of truth, updates/inserts/deletes don't create anomalies.

---

## Q158: What is denormalization?

**Deliberately reintroducing redundancy** (duplicated or pre-aggregated data) to **gain query performance** at the cost of storage and write complexity.

Examples:
- Store `order_count` / `total_spent` on the user row.
- Materialize a flattened `user_orders` table for reporting.
- Pre-join fields into a wide table for reads.

Tradeoff: faster reads, simpler queries vs. consistency risk, larger writes, invalidation logic.

---

## Q159: When would you denormalize a database?

1. **Read-heavy analytics/reporting** — precomputed aggregates for dashboards (or use materialized views, Q556).
2. **Hot paths with heavy joins** — flatten to avoid 4-table joins on every request.
3. **Caching** at the schema level when cache invalidation is simpler than joins.
4. **High-scale OLTP read patterns** — fan-out snapshots (event-sourcing projections).
5. **Latency-critical reads** where join cost dominates.
- Rules: denormalize **only after** profiling shows a real join/index bottleneck; keep writes correct (or accept eventual consistency); document the invariants.

---

## Q160: What are database indexes?

Structures that **speed up lookups/filters/sorts/joins** at the cost of **write overhead and storage**. An index is a sorted copy of the indexed columns + pointers to the table rows.

```sql
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_created ON orders(created_at DESC);
```

- PostgreSQL types: **B-tree** (default; equality + range), **GIN** (arrays, JSONB), **GiST**, **BRIN** (huge sequential data), **hash**.
- Indexes make `WHERE`, `JOIN`, `ORDER BY`, `GROUP BY`, unique constraints fast by scanning the index tree instead of the whole table.

---

## Q161: Why do indexes improve query performance?

- Without an index, a `WHERE` on a non-key column requires a **full table scan** (O(n), every row read).
- With a **B-tree index**, lookup is **O(log n)** — it finds the relevant page directly.
- For ranges/orderings, the index returns rows **already sorted** (skip a sort step).
- For lookups covering only indexed columns, PostgreSQL can do an **index-only scan** (never touch the heap).
- `JOIN` keys indexed → nested-loop/hash joins stay cheap.

**Caveat:** index benefits assume *selectivity*; returning a large % of rows is faster with a scan.

---

## Q162: When can an index hurt performance?

1. **Write slowdown** — every `INSERT/UPDATE/DELETE` must update every index on the table.
2. **Storage + memory cost** — indexes eat disk/RAM (cache pressure).
3. **Unused/redundant indexes** — overhead with no query benefit (find via `pg_stat_user_indexes`).
4. **Wrong type** — e.g., a regular index on a column queried with `ILIKE '%x%'` (can't use B-tree) or on JSONB (needs GIN).
5. **Low selectivity** — index on `gender` (2 values) rarely helps; planner may ignore it anyway.
6. **Ordering mismatch** — `INDEX(a, b)` vs query `ORDER BY b` can't be served efficiently.
7. **Write-heavy tables** — many indexes on hot insert tables add latency.
- Rule: index what the *queries* need, drop duplicates/unused, and measure.

---

## Q163: What is a composite index?

An index on **multiple columns**: `CREATE INDEX idx ON orders(user_id, created_at)`.

- **Leftmost prefix rule:** the index serves queries using the leading columns — `(user_id)` and `(user_id, created_at)` work; `(created_at)` alone does NOT use it.
- Column order matters: put **equality-filtered** columns first, then **range/sort** columns.
- `(user_id, created_at)` covers "all orders of user X, sorted by date" in one index — great for pagination.

```sql
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);
-- serves: WHERE user_id = ? ORDER BY created_at DESC  (index-only)
```

---

## Q164: How do you decide which columns to index?

1. **Look at the queries** (logs / slow-query log / `pg_stat_statements`): what `WHERE`/`JOIN`/`ORDER BY`/`GROUP BY` columns appear.
2. **High-cardinality, selective** columns → good index candidates.
3. **Order** composite indexes: equality cols first, then range/sort.
4. **Covering indexes** (`INCLUDE`) add payload columns for index-only scans.
5. **Foreign keys** — index them (joins + FK enforcement).
6. **Avoid** columns mutated constantly, low selectivity, and duplicated prefixes.
7. **Measure** with EXPLAIN + `pg_stat_user_indexes` (idx_scan) — remove unused.

---

## Q165: What is index selectivity?

The fraction of rows an indexed value matches: **selectivity = matching_rows / total_rows**. High selectivity = a value matches few rows (unique-like) → index is very effective; low selectivity = matches many rows → index may be ignored.

- Indexing a column with values that match most rows (e.g., `status='active'` when 99% active) is wasteful.
- Partial indexes (Q332) exist for exactly this — index only the interesting subset.
- The planner uses statistics to estimate selectivity and decide scan vs index.

---

## Q166: What is a database query plan?

The optimizer's **execution strategy** for a query: which tables scanned, which indexes used, join order/algorithm (nested loop / hash join / merge join), sorts, and estimated costs per step.

```sql
EXPLAIN SELECT * FROM users u JOIN orders o ON o.user_id = u.id WHERE u.id = 5;
-- Hash Join  (cost=... rows=... width=...)
--   Hash on u.id
--   -> Seq Scan on users
--   ...
```

- Reading it tells you **why** a query is slow (Seq Scan on big table, missing index, bad join order, huge sort).
- Each node shows: access method, estimated rows, actual rows (with ANALYZE), cost units, filters.

---

## Q167: What does `EXPLAIN` do?

Prints the **query plan** without executing the query — the optimizer's estimates.

```sql
EXPLAIN SELECT ...;
```

- Cost estimates (relative units), row estimates, access paths.
- Use it first to see if the plan is sensible (index chosen? joins reasonable?).
- **Limitation:** estimates can be wrong (stale stats) — that's why you use `EXPLAIN ANALYZE` for actuals.

---

## Q168: What does `EXPLAIN ANALYZE` do?

**Executes the query** and shows the plan with **actual timings and row counts** per node — the ground truth for "is this query actually fast?"

```sql
EXPLAIN ANALYZE SELECT ...;
-- Seq Scan on users (cost=0.00..1837.00 rows=1000 actual time=0.04..12.5 rows=1000)
```

- Compare **actual vs estimated rows** — a big mismatch = stale statistics → `ANALYZE` the table.
- Watch for: `Seq Scan` on large tables, high `actual time` nodes, sorts without index, "rows removed by filter".
- `EXPLAIN (ANALYZE, BUFFERS)` adds I/O numbers; `(ANALYZE, TIMING OFF)` in CI (timing variance).

---

## Q169: How would you debug a slow SQL query?

1. **Reproduce it** — run the exact query (same params), time it.
2. **`EXPLAIN (ANALYZE, BUFFERS)`** — find the expensive node(s): full scans, sorts, hash joins on big sets, high row estimates mismatch.
3. **Check statistics** — `ANALYZE table;` if estimates are off.
4. **Missing index?** — index the filtered/joined/ordered columns; verify with EXPLAIN.
5. **Rewrites:**
   - Avoid functions on columns in `WHERE` (`WHERE date(created_at)=...` → range on `created_at`).
   - `LIKE '%x%'` → trigram index; `ILIKE` → `pg_trgm`.
   - Replace OR with `UNION ALL` or `IN`.
   - Avoid `SELECT *`; limit columns.
   - Subqueries → joins/CTEs when cheaper (check plan).
6. **Check concurrency** — locks/blocking (Q551), slow due to bloat → VACUUM (Q336).
7. **pg_stat_statements** — find the most expensive queries overall; slow-query log threshold.
8. **Test on realistic data volume** — plans change with data size.

---

## Q170: What is an N+1 query problem?

When you fetch N records, then make **one extra query per record** — 1 + N queries total. Classic ORM anti-pattern:

```python
users = session.query(User).all()        # 1 query (N users)
for u in users:
    print(u.orders)                      # N more queries — one per user!
# total: 1 + N queries
```

- Extremely common with lazy-loaded relationships (SQLAlchemy, Django ORM).
- At scale (1000 users) = 1001 round trips → huge latency + DB load.

---

## Q171: How would you solve an N+1 query problem?

1. **Eager loading:** `SELECT ... JOIN orders` in one query.
   - SQLAlchemy: `session.query(User).options(joinedload(User.orders))` (JOIN) or `selectinload(...)` (2 queries — better for one-to-many).
   - Django: `.select_related()` (FK/1-to-1), `.prefetch_related()` (many).
2. **Batch loading** — one `IN (...)` query per relationship instead of per row.
3. **Denormalize/aggregate** — precompute counts/aggregates for lists.
4. **Avoid lazy access in loops**; design serializers to batch.
5. **Use `selectin`** for collections to avoid cartesian fan-out.

Also see Q348–Q350 (SQLAlchemy specifics) — this exact question is a micro1 favorite.

---

## Q172: What is connection pooling?

Pre-established, reusable DB connections managed by a pool (see Q108–110 for detail). In SQLAlchemy: `create_engine` maintains `pool_size` + `max_overflow` connections; sessions check out a connection and return it on close.

```python
engine = create_engine(url, pool_size=10, max_overflow=5, pool_pre_ping=True, pool_recycle=3600)
```

- Same concepts as the async chapter (Q108–110): amortize handshake cost, bound DB connections, prevent "too many connections".
- PostgreSQL-specific: consider **PgBouncer** for many short-lived connections.

---

## Q173: What are database isolation levels?

The degree to which concurrent transactions' changes are visible to each other — the "I" in ACID.

- **READ UNCOMMITTED** — dirty reads possible (PostgreSQL doesn't implement it; maps to READ COMMITTED).
- **READ COMMITTED** (PostgreSQL default) — only committed data visible; non-repeatable reads possible.
- **REPEATABLE READ** — a transaction sees a stable snapshot (no non-repeatable reads); PG: no phantom reads either (true snapshot isolation).
- **SERIALIZABLE** — transactions behave as if run one-by-one; serialization failures abort → retry.

```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN ISOLATION LEVEL SERIALIZABLE;
```

**Phenomena:** dirty read (uncommitted), non-repeatable read (value changes on re-read), phantom read (new rows appear).
Higher isolation = more correctness, more contention/locks/retries.

---

## Q174: What is a database deadlock?

Two transactions each holding locks the other needs → the DB detects it and **aborts one** ("deadlock detected"), so the application must **retry** the aborted one.

```sql
-- T1: UPDATE accounts SET bal=bal-10 WHERE id=1;  (locks row 1)
-- T1: UPDATE accounts SET bal=bal+10 WHERE id=2;  ← waits for T2
-- T2: UPDATE accounts SET bal=bal-10 WHERE id=2;  (locks row 2)
-- T2: UPDATE accounts SET bal=bal+10 WHERE id=1;  ← waits for T1 → deadlock
```

- **Prevention:** consistent lock ordering (always update by id), keep transactions short, avoid locking too many rows, index FKs.
- **Handling:** catch the deadlock error (SQLSTATE 40P01), retry the transaction with backoff, alert if frequent.
- PostgreSQL detects deadlocks via the **deadlock detector** (background process scans lock graph) — one victim is rolled back, others continue.

---

## Q175: How would you design a database for a recruitment platform?

**Walk through entities, relationships, and choices out loud:**

```sql
candidates (id PK, name, email UNIQUE, resume_s3_key, status, created_at)
jobs      (id PK, title, company_id FK, description, requirements JSONB, status)
applications (id PK, candidate_id FK, job_id FK, status, applied_at,
              UNIQUE(candidate_id, job_id))
interviews (id PK, application_id FK, round, interviewer_id, mode, status, started_at)
messages   (id PK, conversation_id FK, role, content, token_count, created_at)   -- AI chat
evaluations (id PK, interview_id FK, criteria JSONB, score NUMERIC, model, created_at)
```

**Design decisions to mention:**
1. **Normalized core** (candidates/jobs/applications) + **JSONB for flexible fields** (requirements, criteria) — schema evolution without migrations.
2. **Indexes:** FK columns, `(candidate_id, job_id)` unique (prevents dup applications), status filters (partial index), `created_at` for recency lists, full-text search via `tsvector`/`pg_trgm` for resume search (or vector store for embeddings).
3. **Concurrency:** avoid duplicate applications (unique constraint), lock-free evaluation inserts, `SELECT FOR UPDATE` only where truly needed.
4. **Message/history:** append-only `messages` table, paginated with keyset; consider partitioning by date for growth.
5. **Scaling:** read replicas for reports; PgBouncer for connection concurrency; partitioning for the big append-only tables (Q558–560).
6. **Audit:** append-only tables + `updated_at` triggers (audit trail for AI decisions — Q738).
7. **JSONB vs relational tradeoff** (Q327–329) — explain when each wins.
8. **Backups/monitoring** — WAL, PITR, pg_stat monitoring (Q339, Q630).
