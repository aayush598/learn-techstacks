# Views and Materialized Views — 100 SQL Interview Q&A

## Q1: Write a view that shows only active customers plus their email.

**Query:**
```sql
CREATE VIEW active_customers AS
SELECT customer_id, first_name, last_name, email
FROM customers
WHERE status = 'active';
```
**Explanation:** A simple view is a named, saved query: every select against it runs the underlying query, so `active_customers` always returns current data.

**Alt1:** Postgres shorthand to drop and recreate in one statement:
```sql
CREATE OR REPLACE VIEW active_customers AS
SELECT customer_id, first_name, last_name, email
FROM customers
WHERE status = 'active';
```
**Explanation:** `CREATE OR REPLACE VIEW` updates the view definition without erroring if it already exists; the old column list must have a compatible shape.

## Q2: Create a view that shows only active customers plus their total order value.

**Query:**
```sql
CREATE VIEW customer_order_value AS
SELECT c.customer_id, c.first_name, c.last_name,
       COALESCE(SUM(o.total), 0) AS total_order_value
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE c.status = 'active'
GROUP BY c.customer_id, c.first_name, c.last_name;
```
**Explanation:** The view hides the join-and-aggregate logic from reporting queries and shows `0` for customers who have never ordered thanks to `COALESCE`.

## Q3: Write a view that exposes only the first and last name plus a masked email for each employee (column masking).

**Query:**
```sql
CREATE VIEW employee_public AS
SELECT employee_id,
       first_name,
       last_name,
       CONCAT(LEFT(email, 2), '****', RIGHT(email, LOCATE('@', email) = 0)) AS masked_email
FROM employees;
```
**Explanation:** The view exposes rows without salaries or raw emails; consumers get the view instead of the base table, so sensitive columns never leave the table.

**Alt1:** String masking in Postgres:
```sql
CREATE VIEW employee_public AS
SELECT employee_id,
       first_name,
       last_name,
       left(email, 2) || '***' || split_part(email, '@', 2) AS masked_email
FROM employees;
```
**Explanation:** Dialects differ in string functions — Postgres uses `||`, `left()` and `split_part()` — but the security intent (mask before giving access) is the same.

## Q4: Create a view that joins customers and orders to build a reporting feed of order lines.

**Query:**
```sql
CREATE VIEW order_report AS
SELECT o.order_id, c.customer_id, c.first_name || ' ' || c.last_name AS customer_name,
       o.order_date, od.product_id, od.quantity * od.unit_price AS line_total
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN order_details od ON od.order_id = o.order_id;
```
**Explanation:** A join view packages the joins so the report query is a simple `SELECT * FROM order_report`.

## Q5: Change an existing view so it also returns the customer country, without dropping it first.

**Query:**
```sql
CREATE OR REPLACE VIEW order_report AS
SELECT o.order_id, c.customer_id, c.first_name || ' ' || c.last_name AS customer_name,
       c.country, o.order_date, od.product_id, od.quantity * od.unit_price AS line_total
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN order_details od ON od.order_id = o.order_id;
```
**Explanation:** `CREATE OR REPLACE VIEW` edits the definition in place; the new column is appended so existing query plans that only select the old columns keep working.

## Q6: Drop the view `old_deprecated_view` safely so an error is not raised if it is already gone.

**Query:**
```sql
DROP VIEW IF EXISTS old_deprecated_view;
```
**Explanation:** `IF EXISTS` makes the drop idempotent, which is handy in migration scripts that may run more than once.

## Q7: Write a view that aggregates monthly revenue by department using a GROUP BY.

**Query:**
```sql
CREATE VIEW monthly_revenue AS
SELECT department, DATE_TRUNC('month', order_date) AS order_month, SUM(total) AS revenue
FROM orders
GROUP BY department, DATE_TRUNC('month', order_date);
```
**Explanation:** Grouped views move aggregation into the saved object; the consumer just filters, e.g. `SELECT * FROM monthly_revenue WHERE order_month = date '2026-01-01'`.

**Alt1:** Microsoft SQL Server / MySQL variant without `DATE_TRUNC`:
```sql
-- SQL Server, MySQL
CREATE VIEW monthly_revenue AS
SELECT department, DATEADD(month, DATEDIFF(month, 0, order_date), 0) AS order_month, SUM(total) AS revenue
FROM orders
GROUP BY department, DATEADD(month, DATEDIFF(month, 0, order_date), 0);
```
**Explanation:** `DATEADD/DATEDIFF` rounds each order date to the first of its month; grouping by the same expression keeps the query valid in engines without `DATE_TRUNC`.

## Q8: Add HAVING to a grouped view and list only departments whose average order total exceeds $500.

**Query:**
```sql
CREATE VIEW top_departments AS
SELECT department, AVG(total) AS avg_order_value, COUNT(*) AS order_count
FROM orders
GROUP BY department
HAVING AVG(total) > 500;
```
**Explanation:** `HAVING` filters groups after aggregation, and it can live inside a view just like any SELECT.

## Q9: Build a view for internal HR that contains full contact data, and one for external auditors that hides salary and phone.

**Query:**
```sql
CREATE VIEW hr_employee_record AS
SELECT employee_id, first_name, last_name, email, phone, salary, department
FROM employees;

CREATE VIEW auditor_employee_record AS
SELECT employee_id, first_name, last_name,
       CASE WHEN salary IS NULL THEN 0 ELSE salary END AS compensation
FROM employees
WHERE department <> 'Payroll';
```
**Explanation:** Two views over one table grant different exposures: HR sees everything, auditors see a sanitized, salary-shaped column for testing without raw payroll access.

## Q10: Write a view that renames ugly legacy columns into clean, business-facing names for a reporting tool.

**Query:**
```sql
CREATE VIEW current_ledger AS
SELECT id AS ledger_id,
       cst_id AS customer_id,
       amt AS amount,
       created_dt AS created_at
FROM ledger_2020_tmp;
```
**Explanation:** The view is a translation layer: applications reference `current_ledger` with clean names while the messy legacy table can be replaced later without breaking them.

## Q11: Create a view that combines two sources with UNION so reporting sees one unified customer list.

**Query:**
```sql
CREATE VIEW unified_customers AS
SELECT customer_id, email, 'web' AS source
FROM web_customers
UNION
SELECT customer_id, email, 'store' AS source
FROM store_customers;
```
**Explanation:** `UNION` de-duplicates the two result sets with identical column counts and types, producing a single logical source.

**Alt1:** Keep every row from both sides with UNION ALL:
```sql
CREATE VIEW unified_customers AS
SELECT customer_id, email, 'web' AS source
FROM web_customers
UNION ALL
SELECT customer_id, email, 'store' AS source
FROM store_customers;
```
**Explanation:** `UNION ALL` keeps duplicates and is faster because no sorting/dedup happens; choose it when the two sources are guaranteed disjoint.

## Q12: Build a view on top of another view to derive a further-filtered (but still live) report.

**Query:**
```sql
CREATE VIEW high_value_customers AS
SELECT customer_id, customer_name, total_order_value
FROM customer_order_value
WHERE total_order_value > 10000;
```
**Explanation:** A view over a view just nests the queries — `high_value_customers` expands to `customer_order_value`'s full join-aggregate text, so data stays current but the plan is only as good as the optimizer's flattening.

## Q13: Write a view that categorizes orders with CASE into segments like 'small', 'medium', 'large'.

**Query:**
```sql
CREATE VIEW order_segments AS
SELECT order_id, total,
       CASE
           WHEN total < 100       THEN 'small'
           WHEN total < 1000      THEN 'medium'
           ELSE                        'large'
       END AS segment
FROM orders;
```
**Explanation:** Derived/business columns computed in a view keep segmentation rules in one place instead of scattered across reports.

## Q14: Create a view that shows each order over its customer average (view using a correlated subquery).

**Query:**
```sql
CREATE VIEW orders_above_customer_avg AS
SELECT o.order_id, o.customer_id, o.total
FROM orders o
WHERE o.total > (
    SELECT AVG(total)
    FROM orders o2
    WHERE o2.customer_id = o.customer_id
);
```
**Explanation:** The view contains a correlated subquery evaluated per row; complex predicates are fine in a view as long as the optimizer can handle them.

## Q15: Write a view that computes each product's stock status with a scalar subquery for total quantity sold.

**Query:**
```sql
CREATE VIEW product_stock_status AS
SELECT p.product_id, p.product_name, p.stock,
       (SELECT COALESCE(SUM(od.quantity), 0)
        FROM order_details od
        WHERE od.product_id = p.product_id) AS units_sold,
       CASE WHEN p.stock <= 10 THEN 'reorder' ELSE 'ok' END AS stock_status
FROM products p;
```
**Explanation:** Scalar subqueries in the SELECT list are allowed in views; this shape turns frequently repeated "how much is left" logic into a reusable object.

## Q16: Explain with a query the difference between a simple view and a complex view.

**Query:**
```sql
-- Simple view: single table, no functions, no joins
CREATE VIEW simple_customer_view AS
SELECT customer_id, email FROM customers;

-- Complex view: joins, aggregation, expressions
CREATE VIEW complex_sales_summary AS
SELECT c.country,
       DATE_TRUNC('month', o.order_date) AS month,
       SUM(o.total) AS revenue
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.country, DATE_TRUNC('month', o.order_date);
```
**Explanation:** Simple views select plain columns from one table and are updatable; complex views use joins/aggregation and are read-only but still hide heavy logic.

## Q17: Create a temporary view (session-scoped) that only your session can see.

**Query:**
```sql
-- PostgreSQL
CREATE TEMP VIEW tmp_session_report AS
SELECT customer_id, COUNT(*) AS order_count, SUM(total) AS revenue
FROM orders
GROUP BY customer_id;
```
**Explanation:** A `CREATE TEMP VIEW` is confined to the session, dropped automatically on disconnect, and is ideal for experimental staging before promoting it to a permanent view.

## Q18: Write a view that shows only orders from the last 7 days (rolling window).

**Query:**
```sql
CREATE VIEW recent_orders AS
SELECT order_id, customer_id, total, order_date
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '7 days';
```
**Explanation:** The view is evaluated at query time, so the WHERE clause re-checks the current date on every access — the view always shows the last 7 days from "now".

**Alt1:** SQL Server version of the same rolling window:
```sql
-- SQL Server
CREATE VIEW recent_orders AS
SELECT order_id, customer_id, total, order_date
FROM orders
WHERE order_date >= DATEADD(day, -7, CAST(GETDATE() AS date));
```
**Explanation:** `GETDATE()` is SQL Server's now-function and `DATEADD` shifts it back seven days; the view stays live either way.

## Q19: Create a view that reports order count and total revenue per customer, per month, through a view with GROUP BY and a date filter.

**Query:**
```sql
CREATE VIEW customer_monthly_totals AS
SELECT customer_id,
       TO_CHAR(order_date, 'YYYY-MM') AS month,        -- Oracle / Postgres
       COUNT(*) AS orders,
       SUM(total) AS revenue
FROM orders
GROUP BY customer_id, TO_CHAR(order_date, 'YYYY-MM');
```
**Explanation:** Formatting the date in the SELECT list and grouping by the same expression yields a clean monthly bucket key stored inside the view.

## Q20: Write a view for a support dashboard that shows each ticket's age in days and its priority label.

**Query:**
```sql
CREATE VIEW ticket_dashboard AS
SELECT ticket_id, subject, priority,
       CURRENT_DATE - created_date AS age_days,
       CASE
           WHEN priority = 'urgent' AND status = 'open' THEN 'escalate'
           ELSE 'normal'
       END AS action
FROM tickets
WHERE status IN ('open', 'in_progress');
```
**Explanation:** Date arithmetic and CASE labels make operational dashboards trivial to `SELECT * FROM` without duplicating business rules.

**Alt1:** MySQL version using `DATEDIFF`:
```sql
-- MySQL
CREATE VIEW ticket_dashboard AS
SELECT ticket_id, subject, priority,
       DATEDIFF(CURDATE(), created_date) AS age_days,
       CASE
           WHEN priority = 'urgent' AND status = 'open' THEN 'escalate'
           ELSE 'normal'
       END AS action
FROM tickets
WHERE status IN ('open', 'in_progress');
```
**Explanation:** MySQL subtracts dates with `DATEDIFF` instead of the `date - date` operator, but the view-based dashboard pattern is unchanged.

## Q21: Write a view that performs row-level filtering so each branch manager only sees their branch's rows.

**Query:**
```sql
CREATE VIEW branch_sales AS
SELECT *
FROM sales
WHERE branch_id IN (SELECT branch_id FROM branch_managers bm WHERE bm.manager = CURRENT_USER);
```
**Explanation:** The view hard-codes a predicate tied to `CURRENT_USER`, so granting the view (not the table) means each caller automatically sees only rows for branches they manage.

**Alt1:** PostgreSQL form using `session_user` and a lookup:
```sql
-- PostgreSQL
CREATE VIEW branch_sales AS
SELECT s.*
FROM sales s
JOIN branch_managers bm ON bm.branch_id = s.branch_id
WHERE bm.manager = current_user;
```
**Explanation:** A JOIN version of the same row-level filter is easier for the planner to optimize and reads more naturally.

## Q22: Grant a read-only analyst access to a view but explicitly not to the underlying table.

**Query:**
```sql
GRANT SELECT ON active_customers TO analyst_role;
REVOKE SELECT ON customers FROM analyst_role;
```
**Explanation:** Because the view is a separate object, privileges on it can be granted independently; the analyst reaches data only through the view, so filters and masking always apply.

## Q23: Create an updatable view that only lets INSERTs that satisfy its WHERE clause through (WITH CHECK OPTION).

**Query:**
```sql
CREATE VIEW active_customers AS
SELECT customer_id, first_name, last_name, email, status
FROM customers
WHERE status = 'active'
WITH CHECK OPTION;
```
**Explanation:** `WITH CHECK OPTION` blocks INSERT/UPDATE that would leave a row outside the view's WHERE predicate — you cannot insert a `'disabled'` customer through this view.

## Q24: Write a view that normalizes NULLs and blank strings into a single 'Unknown' label.

**Query:**
```sql
CREATE VIEW customer_clean AS
SELECT customer_id,
       COALESCE(NULLIF(TRIM(country), ''), 'Unknown') AS country
FROM customers;
```
**Explanation:** `NULLIF` maps blank/whitespace to NULL, then `COALESCE` supplies a fallback — data cleaning baked into a view so downstream code assumes one shape.

**Alt1:** Oracle variant with `NVL` and a check on whitespace:
```sql
-- Oracle
CREATE VIEW customer_clean AS
SELECT customer_id,
       NVL(NULLIF(TRIM(country), ''), 'Unknown') AS country
FROM customers;
```
**Explanation:** Oracle's single-argument-default `NVL(a, b)` plays the same role as `COALESCE` here; the `NULLIF(...)` trick is identical because it is ANSI SQL.

## Q25: Build a multi-join reporting view that joins four tables for a full order pipeline.

**Query:**
```sql
CREATE VIEW order_pipeline AS
SELECT o.order_id, o.order_date, c.customer_id,
       c.first_name || ' ' || c.last_name AS customer_name,
       e.employee_id AS sales_rep,
       d.department_name,
       SUM(od.quantity * od.unit_price) AS order_value
FROM orders o
JOIN customers c   ON c.customer_id  = o.customer_id
JOIN employees e   ON e.employee_id  = o.sales_rep_id
JOIN departments d ON d.department_id = e.department_id
JOIN order_details od ON od.order_id = o.order_id
GROUP BY o.order_id, o.order_date, c.customer_id, c.first_name, c.last_name,
         e.employee_id, d.department_name;
```
**Explanation:** A join-reporting view gives business users a tidy row-per-order grain without them writing (or mistyping) four joins and a GROUP BY.


## Q26: Show what happens when someone tries to INSERT a row through a view with WITH CHECK OPTION that violates its predicate.

**Query:**
```sql
CREATE VIEW active_customers AS
SELECT customer_id, first_name, last_name, status
FROM customers
WHERE status = 'active'
WITH CHECK OPTION;

-- This INSERT is rejected because status = 'disabled' fails the view predicate
INSERT INTO active_customers (customer_id, first_name, last_name, status)
VALUES (999, 'Jane', 'Doe', 'disabled');
```
**Explanation:** The check fires on the final row: since the row would not be visible through the view, the INSERT errors ("new row violates check option") and nothing is written.

## Q27: Insert a new order through an updatable view.

**Query:**
```sql
CREATE VIEW open_orders AS
SELECT order_id, customer_id, order_date, total, status
FROM orders
WHERE status = 'open';

INSERT INTO open_orders (order_id, customer_id, order_date, total, status)
VALUES (5001, 42, CURRENT_DATE, 199.99, 'open');
```
**Explanation:** The view maps directly onto one table with no derived columns, so the INSERT rewrites into the base table `orders`; the inserted status must match `open` for the row to show up later.

## Q28: Update customer email addresses through a plain view.

**Query:**
```sql
UPDATE active_customers
SET email = 'new.address@example.com'
WHERE customer_id = 1001;
```
**Explanation:** The UPDATE is pushed down to `customers`; because it uses a simple view (one table, key-preserved identity), the change is allowed and visible through the view.

## Q29: List the constructs that make a view read-only and demonstrate one.

**Query:**
```sql
-- Not updatable: a view with GROUP BY, DISTINCT, or aggregation
CREATE VIEW revenue_by_month AS
SELECT DATE_TRUNC('month', order_date) AS month, SUM(total) AS revenue
FROM orders
GROUP BY 1;

-- INSERT through it fails in every dialect
INSERT INTO revenue_by_month (month, revenue) VALUES ('2026-01-01', 5000);
```
**Explanation:** Aggregates, GROUP BY, DISTINCT, set operations, and window functions have no unambiguous base row to write to, so the engine refuses the write.

## Q30: Demonstrate a WITH CHECK OPTION UPDATE quirk where an update would silently re-hide the row without the option.

**Query:**
```sql
-- View WITHOUT the option
CREATE VIEW active_customers AS
SELECT customer_id, first_name, last_name, status
FROM customers
WHERE status = 'active';

-- This runs! The row just disappears from the view afterwards (no error)
UPDATE active_customers
SET status = 'disabled'
WHERE customer_id = 1001;
```
**Explanation:** Without `WITH CHECK OPTION` the engine allows the UPDATE and the row silently vanishes from the view — the classic silent-no-row-result trap during debugging.

**Alt1:** Now add the option and the same UPDATE fails loudly:
```sql
CREATE OR REPLACE VIEW active_customers AS
SELECT customer_id, first_name, last_name, status
FROM customers
WHERE status = 'active'
WITH CHECK OPTION;

UPDATE active_customers
SET status = 'disabled'
WHERE customer_id = 1001;  -- ERROR: violates WITH CHECK OPTION
```
**Explanation:** The explicit check converts a silent data-hiding bug into a hard error, which is almost always what you want.

## Q31: Resize/alter a view's column list in SQL Server and Oracle.

**Query:**
```sql
-- SQL Server
ALTER VIEW order_report AS
SELECT order_id, customer_id, total FROM orders WHERE total > 0;

-- Oracle
CREATE OR REPLACE VIEW order_report AS
SELECT order_id, customer_id, total FROM orders WHERE total > 0;
```
**Explanation:** SQL Server uses `ALTER VIEW` to replace a definition; Oracle (and Postgres/MySQL) use `CREATE OR REPLACE VIEW`. Both preserve the object so dependent grants survive.

## Q32: Drop a view that other views depend on (Postgres CASCADE).

**Query:**
```sql
DROP VIEW IF EXISTS customer_order_value CASCADE;
```
**Explanation:** `CASCADE` also drops any dependent views (e.g. `high_value_customers`) that reference it; without CASCADE Postgres refuses because objects depend on the view.

## Q33: Drop a view whose dependents must be preserved, and show how the engine protects them.

**Query:**
```sql
-- PostgreSQL: fails with a dependency error
DROP VIEW customer_order_value;

-- SQL Server: also blocks with a warning
DROP VIEW customer_order_value;  -- blocked while dependent objects exist

-- Oracle: succeeds but its dependents become INVALID
DROP VIEW customer_order_value;  -- dependent views go to status INVALID
```
**Explanation:** Postgres/SQL Server refuse DROP when dependents exist (RESTRICT is the default); Oracle allows it and invalidates dependents, which you must recompile.

## Q34: Revoke a user's table privileges after giving them a view, and confirm the view still works while the table is blocked.

**Query:**
```sql
GRANT SELECT ON active_customers TO analyst;
REVOKE SELECT ON customers FROM analyst;

-- analyst can now run this
SELECT * FROM active_customers;

-- and is blocked from this
SELECT * FROM customers;  -- permission denied
```
**Explanation:** Permissions are evaluated per object: the view grant is separate from the table grant, so revoking the table leaves the mediated path through the view open (and controlled).

## Q35: Create a PostgreSQL materialized view that precomputes revenue by month and store.

**Query:**
```sql
-- PostgreSQL
CREATE MATERIALIZED VIEW mv_monthly_revenue AS
SELECT DATE_TRUNC('month', order_date) AS month, store_id, SUM(total) AS revenue
FROM orders
GROUP BY 1, 2;
```
**Explanation:** Unlike a plain view, the data is actually computed and stored on disk at creation time; the query plan hits a persisted table, so repeated reads skip the aggregation entirely.

## Q36: Create an indexed view (SQL Server's materialized view) for a daily revenue summary.

**Query:**
```sql
-- SQL Server
CREATE VIEW dbo.daily_revenue WITH SCHEMABINDING AS
SELECT DATEADD(day, DATEDIFF(day, 0, order_date), 0) AS order_day,
       store_id,
       SUM(total) AS revenue,
       COUNT_BIG(*) AS line_count
FROM dbo.orders
GROUP BY DATEADD(day, DATEDIFF(day, 0, order_date), 0), store_id;

CREATE UNIQUE CLUSTERED INDEX ux_daily_revenue
    ON dbo.daily_revenue (order_day, store_id);
```
**Explanation:** In SQL Server a view becomes "materialized" when you build a unique clustered index on it; it is then auto-maintained and can serve query plans directly.

## Q37: Create an Oracle materialized view that refreshes automatically every night.

**Query:**
```sql
-- Oracle
CREATE MATERIALIZED VIEW mv_daily_sales
REFRESH COMPLETE ON DEMAND
START WITH SYSDATE NEXT TRUNC(SYSDATE + 1)
AS
SELECT TRUNC(order_date) AS order_day, store_id, SUM(total) AS revenue
FROM orders
GROUP BY TRUNC(order_date), store_id;
```
**Explanation:** Oracle materialized views carry a refresh policy (`ON DEMAND`/`ON COMMIT`, `COMPLETE`/`FAST`) and can self-schedule with a `START WITH ... NEXT` interval.

## Q38: Simulate a materialized view in MySQL, which has no native support.

**Query:**
```sql
-- MySQL: no CREATE MATERIALIZED VIEW; use a summary table + scheduled refresh
CREATE TABLE monthly_revenue_mv AS
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, store_id, SUM(total) AS revenue
FROM orders
GROUP BY 1, 2;

-- Refresh by event scheduler
CREATE EVENT refresh_monthly_revenue_mv
ON SCHEDULE EVERY 1 DAY
DO
  TRUNCATE TABLE monthly_revenue_mv;
  INSERT INTO monthly_revenue_mv
  SELECT DATE_FORMAT(order_date, '%Y-%m'), store_id, SUM(total)
  FROM orders GROUP BY 1, 2;
```
**Explanation:** MySQL lacks native materialized views, so the standard pattern is a `CREATE TABLE ... AS SELECT` snapshot refreshed on a schedule via an event or cron job.

## Q39: Refresh a PostgreSQL materialized view manually and verify new data appears.

**Query:**
```sql
-- PostgreSQL
REFRESH MATERIALIZED VIEW mv_monthly_revenue;
```
**Explanation:** `REFRESH MATERIALIZED VIEW` rebuilds the stored result from the source query; until it runs, the view shows the snapshot from the last refresh.

## Q40: Refresh a large materialized view without blocking concurrent SELECTs (CONCURRENTLY).

**Query:**
```sql
-- PostgreSQL: requires a UNIQUE index on the view first
CREATE UNIQUE INDEX ux_mv_monthly_revenue ON mv_monthly_revenue (month, store_id);

REFRESH MATERIALIZED VIEW CONCURRENTLY mv_monthly_revenue;
```
**Explanation:** `CONCURRENTLY` builds the new snapshot and swaps it in without taking an exclusive lock, so readers never block — but it demands at least one unique index on the materialized view.

## Q41: Show the performance win of a materialized view with an EXPLAIN comparison.

**Query:**
```sql
-- PostgreSQL
CREATE MATERIALIZED VIEW mv_customer_totals AS
SELECT customer_id, COUNT(*) AS orders, SUM(total) AS revenue
FROM orders
GROUP BY 1;

EXPLAIN ANALYZE SELECT * FROM mv_customer_totals WHERE customer_id = 10;   -- seq scan of cached table
EXPLAIN ANALYZE SELECT customer_id, COUNT(*), SUM(total)
                 FROM orders WHERE customer_id = 10 GROUP BY 1;             -- full scan + aggregate
```
**Explanation:** The materialized view serves reads straight from its persisted table, while the equivalent query rescans and re-aggregates `orders` every time — huge win on heavy reporting workloads.

## Q42: Decide between a view and a CTE for a one-off analysis and show both.

**Query:**
```sql
-- Reusable object (view): saved for many consumers
CREATE VIEW top_customers AS
SELECT customer_id, SUM(total) AS revenue
FROM orders GROUP BY customer_id ORDER BY revenue DESC LIMIT 10;

-- One-off (CTE): scoped to a single statement
WITH top AS (
    SELECT customer_id, SUM(total) AS revenue
    FROM orders GROUP BY customer_id ORDER BY revenue DESC LIMIT 10
)
SELECT * FROM top;
```
**Explanation:** A view persists the definition for reuse; a CTE lives and dies with its statement — use CTEs for ad-hoc queries, views for shared business logic.

## Q43: Compare a view with a temp table and show when the temp table wins.

**Query:**
```sql
-- Temp table: materialize once, then index and reuse in many statements
CREATE TEMP TABLE tmp_big_report AS
SELECT ... FROM orders GROUP BY ...;

CREATE INDEX ON tmp_big_report (customer_id);
SELECT * FROM tmp_big_report WHERE customer_id = 10;
SELECT * FROM tmp_big_report WHERE customer_id = 20;

-- View: always re-runs the query text on each access
CREATE VIEW v_big_report AS
SELECT ... FROM orders GROUP BY ...;
```
**Explanation:** If you query the same expensive result N times in one session, a temp table with an index reuses the materialized rows; a view recomputes every time unless the optimizer can cache it.

## Q44: Create a view that ranks customers by revenue inside itself using a window function.

**Query:**
```sql
CREATE VIEW ranked_customers AS
SELECT customer_id, SUM(total) AS revenue,
       RANK() OVER (ORDER BY SUM(total) DESC) AS revenue_rank
FROM orders
GROUP BY customer_id;
```
**Explanation:** Window functions over aggregates are fine inside views (read-only), giving downstream queries a pre-computed rank column.

**Alt1:** MySQL 8 form — window calls cannot reference an aggregate directly, so wrap the aggregate in a subquery first:
```sql
-- MySQL 8
CREATE VIEW ranked_customers AS
SELECT customer_id, revenue,
       RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM (
    SELECT customer_id, SUM(total) AS revenue
    FROM orders
    GROUP BY customer_id
) agg;
```
**Explanation:** MySQL requires the aggregate to be computed in a derived table before `RANK OVER` can use it; the view still hides both layers from the caller.

## Q45: Build a complex view that joins three tables and filters with a subquery, for an "unfulfilled high-value" report.

**Query:**
```sql
CREATE VIEW pending_high_value AS
SELECT o.order_id, c.customer_name, o.total, p.product_name
FROM orders o
JOIN customers c  ON c.customer_id = o.customer_id
JOIN order_details od ON od.order_id = o.order_id
JOIN products p   ON p.product_id = od.product_id
WHERE o.status = 'pending'
  AND o.total > 5000;
```
**Explanation:** Complex views hide multi-table joins and business thresholds; consumers just `SELECT *` and the view renders the pending, high-value line items.

## Q46: Write a view that finds customers who have ever ordered using EXISTS.

**Query:**
```sql
CREATE VIEW customers_with_orders AS
SELECT c.customer_id, c.first_name, c.last_name
FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```
**Explanation:** `EXISTS` short-circuits on the first match and returns customers at most once, unlike a DISTINCT JOIN.

**Alt1:** Same result with an inner JOIN plus DISTINCT:
```sql
CREATE VIEW customers_with_orders AS
SELECT DISTINCT c.customer_id, c.first_name, c.last_name
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id;
```
**Explanation:** Distinct join membership and `EXISTS` answer the same question; `EXISTS` stops at the first row while `DISTINCT` may sort, so the subquery form usually wins on large data.

## Q47: Write a view that exports orders belonging to a specific set of countries passed as a list in IN.

**Query:**
```sql
CREATE VIEW international_orders AS
SELECT o.order_id, c.country, o.total
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE c.country IN ('India', 'Germany', 'Brazil');
```
**Explanation:** `IN` is a shorthand membership test that compiles to the same plan as an OR-chain; the list is static inside the view but easy to revisit.

## Q48: Build a view of orders due for fulfillment today (dynamic date predicate).

**Query:**
```sql
CREATE VIEW due_today AS
SELECT order_id, customer_id, shipping_date, total
FROM orders
WHERE shipping_date = CURRENT_DATE;      -- Postgres / MySQL / Oracle
```
**Explanation:** `CURRENT_DATE` is evaluated when the query runs, so the view's boundary moves with real time rather than freezing at creation.

## Q49: Write a view that masks part of the customer phone number for support staff.

**Query:**
```sql
-- MySQL: (123) 456-7890 -> (123) ***-7890
CREATE VIEW support_customer AS
SELECT customer_id, first_name, last_name,
       CONCAT(LEFT(phone, 5), '***', RIGHT(phone, 5)) AS masked_phone
FROM customers;
```
**Explanation:** The final four digits plus the area-code prefix survive, but the middle digits are scrubbed before support ever sees them.

**Alt1:** PostgreSQL version using the same prefix/suffix approach:
```sql
-- PostgreSQL
CREATE VIEW support_customer AS
SELECT customer_id, first_name, last_name,
       concat(substr(phone, 1, 5), '***', substr(phone, -4)) AS masked_phone
FROM customers;
```
**Explanation:** `substr` + `concat` hide the same middle block as the MySQL example; the masking rule stays identical, only the string helpers differ by dialect.

## Q50: Create a view that reports NULL revenue as 0 and blanks store names as 'Online'.

**Query:**
```sql
CREATE VIEW clean_sales AS
SELECT store_id,
       COALESCE(NULLIF(store_name, ''), 'Online') AS store_name,
       COALESCE(revenue, 0) AS revenue
FROM sales_snapshot;
```
**Explanation:** `NULLIF` converts empty strings to NULL and `COALESCE` fills both NULLs and blanks with stable defaults — one clean view for all consumers.


## Q51: Design a maintenance strategy for a large materialized view that must stay fresh while staying fast.

**Query:**
```sql
-- PostgreSQL: index the view, refresh concurrently on a schedule
CREATE UNIQUE INDEX ux_mv_revenue ON mv_revenue (month, store_id);
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_revenue;

-- Schedule it: pg_cron
SELECT cron.schedule('refresh-revenue', '0 3 * * *',
  $$REFRESH MATERIALIZED VIEW CONCURRENTLY mv_revenue$$);
```
**Explanation:** Concurrent refresh + an off-peak schedule keeps the view near-real-time without ever blocking reads; the unique index is the mandatory piece for `CONCURRENTLY`.

## Q52: Explain why REFRESH ... CONCURRENTLY needs a unique index, and demonstrate the failure without one.

**Query:**
```sql
CREATE MATERIALIZED VIEW mv_sales AS SELECT store_id, SUM(total) AS revenue
FROM orders GROUP BY store_id;

-- No unique index on the view -> this errors
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_sales;
-- ERROR: cannot refresh materialized view "mv_sales" concurrently
--        without a unique index

-- Fix
CREATE UNIQUE INDEX ux_mv_sales ON mv_sales (store_id);
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_sales;
```
**Explanation:** Concurrent refresh runs both the old and new snapshots to compute row diffs; without a unique key it cannot match rows between versions, so Postgres refuses.

## Q53: Show why refreshing a materialized view inside a transaction can block or roll back everything.

**Query:**
```sql
-- PostgreSQL
BEGIN;
UPDATE orders SET total = total * 1.05 WHERE store_id = 5;
REFRESH MATERIALIZED VIEW mv_revenue;   -- takes an ACCESS EXCLUSIVE lock
-- ... more work
COMMIT;
```
**Explanation:** A non-concurrent refresh takes an exclusive lock until commit; long transactions hold it longer, and if you roll back, the refresh (and any concurrent reads) also went away with it.

**Alt1:** Avoid the trap with a concurrent refresh at statement end:
```sql
BEGIN;
UPDATE orders SET total = total * 1.05 WHERE store_id = 5;
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_revenue;   -- no exclusive lock
COMMIT;
```
**Explanation:** `CONCURRENTLY` avoids taking the long exclusive lock, so the transaction stays non-blocking; readers and the refresh coexist.

## Q54: Show the rules under which SQL Server auto-maintains an indexed view.

**Query:**
```sql
-- SQL Server: indexed views are automatically maintained by the engine
CREATE VIEW dbo.customer_totals WITH SCHEMABINDING AS
SELECT customer_id, SUM(total) AS revenue, COUNT_BIG(*) AS cnt
FROM dbo.orders
GROUP BY customer_id;

CREATE UNIQUE CLUSTERED INDEX ux ON dbo.customer_totals (customer_id);

INSERT INTO dbo.orders (order_id, customer_id, total) VALUES (1, 99, 50.00);
-- When query optimizer's chosen plan touches the view, the index is updated
SELECT * FROM dbo.customer_totals WHERE customer_id = 99;
```
**Explanation:** The optimizer decides whether to use the indexed view; SQL Server keeps it in sync with base-table DML automatically, so no manual REFRESH is required (this is also why it must be deterministic and schemabound).

## Q55: Create a recursive view in PostgreSQL for an employee org chart.

**Query:**
```sql
-- PostgreSQL
CREATE RECURSIVE VIEW org_chart AS
SELECT employee_id, manager_id, first_name, 1 AS depth
FROM employees
WHERE manager_id IS NULL
UNION ALL
SELECT e.employee_id, e.manager_id, e.first_name, oc.depth + 1
FROM employees e
JOIN org_chart oc ON oc.employee_id = e.manager_id;

SELECT first_name, depth FROM org_chart ORDER BY depth;
```
**Explanation:** `CREATE RECURSIVE VIEW` wraps a recursive CTE; the base term seeds the top of the tree and the recursive term walks down until no more managers are found.

## Q56: Explain (with a query) when a plain view gets inlined instead of materialized by the optimizer.

**Query:**
```sql
CREATE VIEW cheap_join AS
SELECT o.order_id, c.country FROM orders o JOIN customers c USING (customer_id);

-- Optimizer likely inlines the view into this query ...
EXPLAIN SELECT * FROM cheap_join WHERE country = 'India';

-- ... but with a window function the view is materialized as a barricade
CREATE VIEW ranked AS
SELECT order_id, total, RANK() OVER (ORDER BY total DESC) AS r FROM orders;
EXPLAIN SELECT * FROM ranked WHERE r < 5;  -- "WindowAgg" = materialization boundary
```
**Explanation:** Simple views are usually flattened ("inlined") into the outer query so predicates push down; views containing window functions, aggregates, or set operations often force a materialization barrier that blocks pushdown.

## Q57: Demonstrate WITH CHECK OPTION failing on a multi-table view.

**Query:**
```sql
CREATE VIEW brand_orders AS
SELECT o.order_id, o.customer_id, o.total, o.brand
FROM orders o
WHERE o.brand = 'acme'
WITH CHECK OPTION;

INSERT INTO brand_orders (order_id, customer_id, total, brand)
VALUES (777, 1, 100, 'other');   -- ERROR: violates check option
```
**Explanation:** The check applies to rows visible *through the view*, regardless of how many tables the view references — inserting a non-`acme` row is rejected because the view can't show it.

**Alt1:** Pass the predicate by inserting a compliant row:
```sql
INSERT INTO brand_orders (order_id, customer_id, total, brand)
VALUES (778, 1, 100, 'acme');   -- OK: row satisfies the WITH CHECK OPTION
```
**Explanation:** Because `brand = 'acme'` matches the view predicate, the insert through the view succeeds and the row is visible afterward.

## Q58: Write a view that uses LATERAL to attach the latest order per customer.

**Query:**
```sql
-- PostgreSQL
CREATE VIEW latest_orders AS
SELECT c.customer_id, c.first_name, lo.order_id, lo.order_date, lo.total
FROM customers c
CROSS JOIN LATERAL (
    SELECT order_id, order_date, total
    FROM orders o
    WHERE o.customer_id = c.customer_id
    ORDER BY o.order_date DESC
    LIMIT 1
) lo;
```
**Explanation:** `LATERAL` lets the subquery reference columns from the joined customers row (like a correlated subquery), returning exactly one newest order per customer.

**Alt1:** The SQL Server equivalent using `CROSS APPLY`:
```sql
-- SQL Server
CREATE VIEW latest_orders AS
SELECT c.customer_id, c.first_name, lo.order_id, lo.order_date, lo.total
FROM customers c
CROSS APPLY (
    SELECT TOP (1) order_id, order_date, total
    FROM orders o
    WHERE o.customer_id = c.customer_id
    ORDER BY o.order_date DESC
) lo;
```
**Explanation:** `CROSS APPLY` is SQL Server's implementation of LATERAL and `TOP (1)` replaces `LIMIT` — same correlated-lookup semantics, T-SQL syntax.

## Q59: Create a view that reports revenue at multiple granularities using GROUPING SETS.

**Query:**
```sql
-- PostgreSQL / SQL Server / Oracle (syntax-wise)
CREATE VIEW revenue_groupings AS
SELECT store_id, product_category, SUM(total) AS revenue
FROM sales
GROUP BY GROUPING SETS ((store_id), (product_category), ());
```
**Explanation:** One query produces store-level, category-level, and grand-total rows; NULL marks the rolled-up dimension, and the view lets analysts drill up and down.

## Q60: Index a PostgreSQL materialized view for fast lookups and show the query that benefits.

**Query:**
```sql
-- PostgreSQL
CREATE MATERIALIZED VIEW mv_customer_totals AS
SELECT customer_id, COUNT(*) AS orders, SUM(total) AS revenue
FROM orders GROUP BY customer_id;

CREATE INDEX idx_mv_customer_totals_revenue ON mv_customer_totals (revenue DESC);

SELECT first_name FROM mv_customer_totals
ORDER BY revenue DESC LIMIT 10;   -- uses the index, instant top-10
```
**Explanation:** Materialized views are storage objects, so you can index them like tables — that index survives refreshes (non-concurrent ones rebuild the heap but keep the index definitions).

## Q61: Enforce column-level security by hiding a single sensitive column behind a view.

**Query:**
```sql
CREATE VIEW public_employees AS
SELECT employee_id, first_name, last_name, email, department
FROM employees;                     -- note: no salary, no ssn

GRANT SELECT ON public_employees TO hr_viewer;
-- No grant on employees itself, so salary stays read-proof
```
**Explanation:** Column masking via views is the classic "drop the column, keep the table" trick — the sensitive columns exist on the table but no granted object exposes them.

## Q62: Create a materialized view in Postgres that precomputes an audit rollup for security review.

**Query:**
```sql
-- PostgreSQL
CREATE MATERIALIZED VIEW mv_audit_summary AS
SELECT action, actor, DATE_TRUNC('day', occurred_at) AS day, COUNT(*) AS events
FROM audit_log
GROUP BY 1, 2, 3;

REFRESH MATERIALIZED VIEW CONCURRENTLY mv_audit_summary;
```
**Explanation:** Login/action counts by actor-day are cheap to serve from the snapshot, so compliance queries never scan the full audit_log for a recurring report.

## Q63: Write a view that uses a volatile function now() and warn about read-your-writes confusion.

**Query:**
```sql
CREATE VIEW session_cutoff AS
SELECT NOW() AS captured_at, COUNT(*) AS open_orders
FROM orders
WHERE status = 'open';
```
**Explanation:** `NOW()` is re-evaluated per query, so two reads in the same second can report different `captured_at` values — a view with volatile functions is not a snapshot, unlike a materialized view.

## Q64: Set up a recurring refresh for a materialized view using pg_cron on a schedule.

**Query:**
```sql
-- PostgreSQL + pg_cron
SELECT cron.schedule('hourly-revenue', '15 * * * *',
  'REFRESH MATERIALIZED VIEW CONCURRENTLY mv_hourly_revenue');
```
**Explanation:** A cron job issues the refresh; choosing an odd minute (e.g. `:15`) spreads load and keeps `CONCURRENTLY` refreshes from contending with ad-hoc report traffic.

## Q65: Write a view that uses a correlated EXISTS subquery to list departments with at least one high-value order.

**Query:**
```sql
CREATE VIEW active_departments AS
SELECT d.department_id, d.department_name
FROM departments d
WHERE EXISTS (
    SELECT 1 FROM orders o
    JOIN employees e ON e.employee_id = o.sales_rep_id
    WHERE e.department_id = d.department_id AND o.total > 5000
);
```
**Explanation:** The outer row (a department) controls the subquery; `EXISTS` stops at the first qualifying order, keeping the view efficient.

## Q66: Create a view that concatenates customer data from five regional tables with UNION ALL, then add a source column.

**Query:**
```sql
CREATE VIEW all_regions AS
SELECT customer_id, name, region FROM eur_customers
UNION ALL SELECT customer_id, name, 'APAC' FROM apac_customers
UNION ALL SELECT customer_id, name, 'AMER' FROM amer_customers
UNION ALL SELECT customer_id, name, 'MEA'  FROM mea_customers
UNION ALL SELECT customer_id, name, 'OCE'  FROM oce_customers;
```
**Explanation:** `UNION ALL` merges same-shape result sets with no de-duplication cost; a hard-coded region literal on each branch makes the merged source self-describing.

## Q67: Write a view that shows customers present in the web list but not in the store list (EXCEPT).

**Query:**
```sql
-- PostgreSQL / SQL Server
CREATE VIEW web_only_customers AS
SELECT email FROM web_customers
EXCEPT
SELECT email FROM store_customers;
```
**Explanation:** `EXCEPT` returns rows in the first set that are absent from the second — exactly a "web-only" (or store-only) membership report.

**Alt1:** Oracle ranks the same operation using MINUS:
```sql
-- Oracle
CREATE VIEW web_only_customers AS
SELECT email FROM web_customers
MINUS
SELECT email FROM store_customers;
```
**Explanation:** Oracle calls the set-difference operator `MINUS`; SQL semantics are identical to `EXCEPT`.

## Q68: Build a view that uses a window frame to show each order against a rolling 3-order average.

**Query:**
```sql
CREATE VIEW rolling_avg_orders AS
SELECT order_id, customer_id, total,
       AVG(total) OVER (
           ORDER BY order_date
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS rolling_avg_3
FROM orders;
```
**Explanation:** The frame — the sliding window of the previous two rows plus the current — gives a moving average; the view preserves it for charting tools that can't write `OVER`.

**Alt1:** Same rolling average in MySQL 8+, which supports window frames:
```sql
-- MySQL 8
CREATE VIEW rolling_avg_orders AS
SELECT order_id, customer_id, total,
       AVG(total) OVER (
           ORDER BY order_date
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS rolling_avg_3
FROM orders;
```
**Explanation:** MySQL added `OVER` frames in 8.0, so an identical view definition works; the older 5.7 branch has no window functions and cannot express it in a view.

## Q69: Design an incremental refresh for a materialized view using a delta (log) table.

**Query:**
```sql
-- PostgreSQL: refresh only the delta, merge into the snapshot
CREATE TABLE order_changes_log (
    order_id int, customer_id int, total numeric, changed_at timestamptz
);

-- Instead of full REFRESH, merge new rows into the summary
INSERT INTO mv_daily_totals (order_day, revenue)
SELECT order_day, revenue FROM (
    SELECT DATE_TRUNC('day', o.order_date) AS order_day, SUM(o.total) AS revenue
    FROM orders o JOIN order_changes_log l ON l.order_id = o.order_id
    GROUP BY 1
) new_rows
ON CONFLICT (order_day) DO UPDATE SET revenue = EXCLUDED.revenue;
```
**Explanation:** For high-velocity data, a log table + `INSERT ... ON CONFLICT` only touches changed days instead of rebuilding the whole materialized view (the manual "fast refresh").

## Q70: Create an Oracle view of an employee hierarchy using CONNECT BY.

**Query:**
```sql
-- Oracle
CREATE VIEW emp_tree AS
SELECT employee_id, first_name, manager_id, LEVEL AS depth,
       SYS_CONNECT_BY_PATH(first_name, ' / ') AS chain
FROM employees
START WITH manager_id IS NULL
CONNECT BY PRIOR employee_id = manager_id;
```
**Explanation:** Oracle's hierarchical query builds the org tree in one pass; `LEVEL` and `SYS_CONNECT_BY_PATH` are exported as ordinary view columns for reporting.

## Q71: Write a view that uses ROLLUP to produce subtotals per store and a grand total.

**Query:**
```sql
-- PostgreSQL / MySQL / SQL Server
CREATE VIEW sales_rollup AS
SELECT store_id, SUM(total) AS revenue, GROUPING(store_id) AS is_grand_total
FROM sales
GROUP BY ROLLUP (store_id);
```
**Explanation:** `GROUPING()` labels the rolled-up rows so analysts can filter out (or keep) the grand-total row with a plain WHERE on the view.

## Q72: Show WITH CHECK OPTION restricting an UPDATE through a constrained complex view.

**Query:**
```sql
CREATE VIEW big_orders AS
SELECT order_id, customer_id, total, status
FROM orders
WHERE total > 1000
WITH CHECK OPTION;

UPDATE big_orders
SET total = 100
WHERE order_id = 101;              -- ERROR: new total < 1000 violates the check
```
**Explanation:** The option watches the *new* row too: shrinking an order below the view's threshold is rejected exactly like an out-of-bounds INSERT.

## Q73: Create a Postgres view that aggregates with FILTER to count open vs closed tickets in one pass.

**Query:**
```sql
-- PostgreSQL
CREATE VIEW ticket_health AS
SELECT DATE(created_date) AS day,
       COUNT(*) FILTER (WHERE status = 'closed') AS closed,
       COUNT(*) FILTER (WHERE status = 'open')   AS open_count
FROM tickets
GROUP BY 1;
```
**Explanation:** The `FILTER` clause yields per-condition counts inside one scan of the table, avoiding three separate aggregate queries glued together.

## Q74: Distinguish a temporary (session) view from a permanent view in PostgreSQL and show scoping.

**Query:**
```sql
-- PostgreSQL
CREATE TEMP VIEW tmp_scope_q2_report AS
SELECT customer_id, SUM(total) AS revenue FROM orders_2026_q2 GROUP BY 1;

-- Visible only to THIS session; vanishes on disconnect.
-- A permanent view is visible to everyone with privileges and survives.
SELECT * FROM tmp_scope_q2_report;
```
**Explanation:** Temp views shadow same-named permanent ones for the session and are dropped at session end — perfect for scratch analysis that must not leak into shared schema.

## Q75: Build a view that pivots ticket counts by status using STRING_AGG / LISTAGG into rows.

**Query:**
```sql
-- PostgreSQL
CREATE VIEW ticket_composition AS
SELECT DATE(created_date) AS day,
       STRING_AGG(status || '=' || cnt, ', ' ORDER BY status) AS status_line
FROM (
    SELECT created_date, status, COUNT(*) AS cnt
    FROM tickets GROUP BY 1, 2
) t
GROUP BY DATE(created_date);
```
**Explanation:** `STRING_AGG` (Postgres) / `LISTAGG` (Oracle) collapses grouped counts into one delimited string, a classic materialized-in-a-view trick for dense dashboard cells.

**Alt1:** Oracle renders the same pivot line with `LISTAGG` and the `WITHIN GROUP` ordering syntax:
```sql
-- Oracle
CREATE VIEW ticket_composition AS
SELECT created_date AS day,
       LISTAGG(status || '=' || cnt, ', ')
         WITHIN GROUP (ORDER BY status) AS status_line
FROM (
    SELECT created_date, status, COUNT(*) AS cnt
    FROM tickets GROUP BY created_date, status
) t
GROUP BY created_date;
```
**Explanation:** Oracle's `LISTAGG` places the ordering inside `WITHIN GROUP` instead of an argument clause, but the grouped-to-delimited-string result is identical.

## Q76: Give a decision framework: view vs CTE vs temp table vs materialized view — with one runnable pattern for each.

**Query:**
```sql
-- 1. View: shared, always-current business logic
CREATE VIEW active_users AS SELECT * FROM users WHERE status = 'active';

-- 2. CTE: single-statement readability
WITH active_users AS (SELECT * FROM users WHERE status = 'active')
SELECT * FROM active_users;

-- 3. Temp table: reuse across many statements in one session
CREATE TEMP TABLE tmp_active AS SELECT * FROM users WHERE status = 'active';

-- 4. Materialized view: precomputed, refreshed on schedule
CREATE MATERIALIZED VIEW mv_active_users AS
SELECT * FROM users WHERE status = 'active';
```
**Explanation:** Choose by lifetime and freshness: view = permanent & live, CTE = one statement, temp table = one session & reusable, materialized view = permanent & deliberately stale for speed.

## Q77: Write a recursive view that computes each employee's report count (Postgres), including retries through the tree.

**Query:**
```sql
-- PostgreSQL
CREATE RECURSIVE VIEW direct_reports AS (
    SELECT employee_id, 0 AS depth, '' AS path
    FROM employees
    UNION ALL
    SELECT e.employee_id, dr.depth + 1,
           dr.path || e.employee_id::text || '/' -- placeholder aggregation
    FROM employees e
    JOIN direct_reports dr ON dr.employee_id = e.manager_id
);
-- Fully populated report count:
SELECT manager_id, COUNT(*) AS direct_reports FROM employees GROUP BY 1 ORDER BY 2 DESC;
```
**Explanation:** The recursive view walks the reporting tree with a base case and a recursive term; guards (via depth limit or cycle detection) prevent infinite loops on cyclic org data.

## Q78: Show the full prerequisites and pattern for a safe concurrent refresh in production.

**Query:**
```sql
-- PostgreSQL
CREATE MATERIALIZED VIEW mv_sales AS
SELECT store_id, DATE_TRUNC('month', order_date) AS month, SUM(total) AS revenue
FROM orders GROUP BY 1, 2;

CREATE UNIQUE INDEX ux_mv_sales ON mv_sales (store_id, month);   -- REQUIRED for CONCURRENTLY

REFRESH MATERIALIZED VIEW CONCURRENTLY mv_sales;                 -- non-blocking, two snapshots
```
**Explanation:** Concurrent refresh needs (1) a unique index covering the view's key columns and (2) enough shared_buffers/disk headroom to build the second snapshot before the atomic swap.

## Q79: Show how a materialized view can enable partition-style row elimination by pre-aggregating the hot partition.

**Query:**
```sql
-- PostgreSQL
CREATE MATERIALIZED VIEW mv_current_month AS
SELECT store_id, product_id, SUM(total) AS revenue
FROM orders
WHERE order_date >= DATE_TRUNC('month', CURRENT_DATE)   -- only this month's data
GROUP BY 1, 2;

REFRESH MATERIALIZED VIEW CONCURRENTLY mv_current_month;
```
**Explanation:** The view physically contains only the current month's aggregates, so every report over "this month" scans a tiny snapshot instead of the whole order history.

## Q80: Compare materialized-view implementations across PostgreSQL, SQL Server, MySQL, and Oracle in one answer.

**Query:**
```sql
-- PostgreSQL: native, manual refresh
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_sales;

-- SQL Server: indexed view, auto-maintained once indexed
CREATE VIEW dbo.sales_mv WITH SCHEMABINDING AS
SELECT store_id, SUM(total) AS revenue, COUNT_BIG(*) AS cnt
FROM dbo.orders GROUP BY store_id;
CREATE UNIQUE CLUSTERED INDEX ux ON dbo.sales_mv (store_id);

-- Oracle: refresh policy + options
CREATE MATERIALIZED VIEW mv_sales
REFRESH FAST ON COMMIT ENABLE QUERY REWRITE AS
SELECT store_id, SUM(total) AS revenue FROM orders GROUP BY store_id;

-- MySQL: no native support -> summary table + event
CREATE TABLE mv_sales AS SELECT store_id, SUM(total) AS revenue FROM orders GROUP BY 1;
```
**Explanation:** PostgreSQL = manual `REFRESH`, SQL Server = auto-maintained indexed view, Oracle = refresh policies + query rewrite, MySQL = manual summary table. Same idea, four very different operators.

## Q81: Write a view that exposes a JSON summary of a customer's latest activity (PostgreSQL JSON functions).

**Query:**
```sql
-- PostgreSQL
CREATE VIEW customer_json_summary AS
SELECT customer_id,
       jsonb_build_object(
           'name', first_name || ' ' || last_name,
           'last_order', last_order_date,
           'total_revenue', total_revenue
       ) AS profile
FROM customer_totals;
```
**Explanation:** The view centralizes the JSON shaping so apps consume one stable document contract without embedding shape logic.

## Q82: Show how to rename a materialized view and keep its dependent indexes valid.

**Query:**
```sql
-- PostgreSQL
ALTER MATERIALIZED VIEW mv_sales RENAME TO mv_sales_daily;
REFRESH MATERIALIZED VIEW mv_sales_daily;
```
**Explanation:** Renaming updates the catalog and dependent index/rows references follow automatically; a refresh afterwards confirms the snapshot reflects the new identity.

## Q83: Create a view that uses FULL OUTER JOIN to surface mismatches between two systems' customer lists.

**Query:**
```sql
CREATE VIEW customer_reconcile AS
SELECT COALESCE(crm.customer_id, erp.customer_id)    AS customer_id,
       crm.name   AS crm_name,
       erp.name   AS erp_name,
       CASE WHEN crm.customer_id IS NULL THEN 'missing in CRM'
            WHEN erp.customer_id IS NULL THEN 'missing in ERP'
            ELSE 'present in both' END              AS reconciliation_status
FROM crm_customers crm
FULL OUTER JOIN erp_customers erp
  ON erp.customer_id = crm.customer_id;
```
**Explanation:** `FULL OUTER JOIN` keeps orphans from both sides; the status column turns every discrepancy into a queryable row for the reconciliation report.

**Alt1:** MySQL has no `FULL OUTER JOIN`, so emulate it with LEFT + RIGHT UNION ALL and a source tag:
```sql
-- MySQL
CREATE VIEW customer_reconcile AS
SELECT customer_id, name, 'crm' AS source FROM crm_customers
UNION ALL
SELECT customer_id, name, 'erp' AS source FROM erp_customers
LEFT JOIN crm_customers c USING (customer_id)
WHERE c.customer_id IS NULL;
```
**Explanation:** The LEFT branch lists every CRM customer and the RIGHT branch adds only ERP customers missing from CRM — a manual full-outer join when the dialect lacks the operator.

## Q84: Build a view with LEAD/LAG to show an order total alongside prior and next order totals per customer.

**Query:**
```sql
CREATE VIEW order_context AS
SELECT order_id, customer_id, total,
       LAG(total)  OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_total,
       LEAD(total) OVER (PARTITION BY customer_id ORDER BY order_date) AS next_total
FROM orders;
```
**Explanation:** `LAG`/`LEAD` peek at neighboring rows within each customer's ordered set — a normalized view that feeds growth or anomaly reports.

## Q85: Explain Oracle materialized view invalidation and query rewrite, and demonstrate ENABLE QUERY REWRITE.

**Query:**
```sql
-- Oracle
CREATE MATERIALIZED VIEW mv_sales
REFRESH FAST ON COMMIT
ENABLE QUERY REWRITE
AS SELECT store_id, TRUNC(order_date) AS day, SUM(total) AS revenue
   FROM orders GROUP BY store_id, TRUNC(order_date);

-- When someone writes a compatible aggregate, Oracle may answer from the MV:
SELECT TRUNC(order_date), SUM(total) FROM orders GROUP BY TRUNC(order_date);
```
**Explanation:** On base-table DDL, the MV can go INVALID until refreshed; with query rewrite enabled, the optimizer transparently substitutes the pre-aggregated data for equivalent user queries.

## Q86: Differentiate security definer vs invoker behavior for views (PostgreSQL).

**Query:**
```sql
-- PostgreSQL: views default to security_invoker = false -> run with CREATOR's rights
CREATE VIEW profitable_orders AS
SELECT * FROM orders WHERE revenue > cost;

-- Force invoker semantics so the caller needs table access too
-- ALTER VIEW profitable_orders SET (security_invoker = true);
SELECT * FROM profitable_orders;
```
**Explanation:** By default a view executes with the ownership privileges of its creator, letting you grant the view without granting the table; `security_invoker = true` removes that guard and requires caller table privileges.

## Q87: Name the classic performance anti-patterns with views and fix one nesting trap.

**Query:**
```sql
-- Anti-pattern: view-in-view-in-view exploding into a monster plan
CREATE VIEW v1 AS SELECT *, SUM(total) OVER () s FROM orders;      -- window
CREATE VIEW v2 AS SELECT * FROM v1 WHERE s > 100;                   -- filter on window
CREATE VIEW v3 AS SELECT * FROM v2 JOIN customers c USING (customer_id);

-- Fix: collapse into one view so the planner can push predicates down
CREATE OR REPLACE VIEW v3 AS
SELECT * FROM orders o JOIN customers c USING (customer_id)
WHERE SUM(o.total) OVER () > 100;
```
**Explanation:** Nesting views that each contain window functions or aggregates creates materialization barriers and duplicated scans; flattening restores predicate pushdown and index use.

## Q88: List the restrictions for creating an indexed view in SQL Server and prove one.

**Query:**
```sql
-- SQL Server: must be SCHEMABINDING, deterministic, no subqueries/window/nondeterministic funcs
CREATE VIEW dbo.sales_mv WITH SCHEMABINDING AS
SELECT customer_id, SUM(total) AS revenue, COUNT_BIG(*) AS cnt
FROM dbo.orders
GROUP BY customer_id;

CREATE UNIQUE CLUSTERED INDEX ux ON dbo.sales_mv (customer_id);  -- OK

-- This fails: nondeterministic GETDATE() is not allowed in an indexed view
CREATE VIEW dbo.bad_mv WITH SCHEMABINDING AS
SELECT customer_id, GETDATE() AS seen_at FROM dbo.orders GROUP BY customer_id;
```
**Explanation:** Indexed views must be schemabound, deterministic, and restricted to a narrow grammar; `COUNT_BIG` is mandatory for aggregate indexed views, bare `COUNT` is rejected.

## Q89: Use a Postgres view over generate_series to materialize a complete calendar skeleton.

**Query:**
```sql
-- PostgreSQL
CREATE VIEW calendar_days AS
SELECT d::date AS day,
       EXTRACT(DOW FROM d)::int    AS dow,
       EXTRACT(ISOYEAR FROM d)::int AS iso_year
FROM generate_series(date '2026-01-01', date '2026-12-31', interval '1 day') AS d;

-- LEFT JOIN sales to it and missing days appear as 0
SELECT cal.day, COALESCE(SUM(s.total), 0) AS daily_revenue
FROM calendar_days cal
LEFT JOIN sales s ON s.order_date = cal.day
GROUP BY cal.day;
```
**Explanation:** A dense calendar from a set-returning function plugged into a view makes time-series gaps explicit — join it and missing dates surface as zeros instead of disappearing.

**Alt1:** SQL Server builds the same dense calendar with a recursive CTE inside the view:
```sql
-- SQL Server
CREATE VIEW calendar_days AS
WITH cte AS (
    SELECT CAST('2026-01-01' AS date) AS day
    UNION ALL
    SELECT DATEADD(day, 1, day) FROM cte WHERE day < '2026-12-31'
)
SELECT day, DATEPART(weekday, day) AS dow FROM cte
OPTION (MAXRECURSION 366);
```
**Explanation:** T-SQL has no `generate_series`, so the calendar is seeded recursively — one row per day up to the end date — and `OPTION (MAXRECURSION)` lifts the default 100-level cap.

## Q90: Compare a materialized view to a prebuilt summary table and justify one over the other.

**Query:**
```sql
-- Materialized view: declarative, single source of truth for the mapping
CREATE MATERIALIZED VIEW mv_daily_revenue AS
SELECT DATE(order_date) AS day, SUM(total) AS revenue FROM orders GROUP BY 1;

-- Hand-rolled summary table: manual DDL + trigger/ETL ownership
CREATE TABLE daily_revenue_summary (day date PRIMARY KEY, revenue numeric);
-- (ETL job or trigger populates it — you own correctness)
```
**Explanation:** MVs own freshness semantics and keep the SQL definition between query and data; app-maintained summary tables are flexible but put the logic (and the bugs) in app or trigger code.

## Q91: Write a view that adds percentile ranks per product category.

**Query:**
```sql
-- PostgreSQL
CREATE VIEW product_percentiles AS
SELECT product_id, category,
       PERCENT_RANK() OVER (PARTITION BY category ORDER BY price) AS price_pctile
FROM products;
```
**Explanation:** `PERCENT_RANK` positions each product inside its category's price distribution; the window computation is preserved as a column for BI tooling that can't express it.

## Q92: Drop several dependent views in one statement and confirm the dependency chain.

**Query:**
```sql
-- PostgreSQL
DROP VIEW IF EXISTS high_value_customers, customer_order_value, active_customers CASCADE;
```
**Explanation:** Multiple views in one DROP is allowed when listed together; `CASCADE` (or explicit listing) guarantees no orphaned dependent objects are left invalid.

## Q93: Show REVOKE ALL on a table AFTER granting a view, and prove the attacker only sees view-shaped rows.

**Query:**
```sql
REVOKE ALL ON customers, orders FROM analyst;
GRANT SELECT ON active_customers TO analyst;    -- view grants are independent

-- Once only the view is granted, analyst's query:
SELECT * FROM active_customers;      -- OK, but only 'active' rows reachable
```
**Explanation:** Because SQL privileges are per-object, the analyst can query the view while the tables stay locked; row-level filters in the view act as an extra security boundary.

## Q94: Build a view on top of a materialized view to add presentation columns without copying the data.

**Query:**
```sql
-- PostgreSQL
CREATE MATERIALIZED VIEW mv_daily_revenue AS
SELECT DATE(order_date) AS day, SUM(total) AS revenue FROM orders GROUP BY 1;

CREATE VIEW v_daily_revenue AS
SELECT day, revenue,
       revenue - LAG(revenue) OVER (ORDER BY day) AS day_over_day_delta,
       ROUND(revenue / NULLIF(LAG(revenue) OVER (ORDER BY day), 0), 3) AS growth
FROM mv_daily_revenue;
```
**Explanation:** The view reads the *materialized* snapshot, so the added window columns are cheap to compute and the view stays fast even though it recomputes its delta columns on access.

## Q95: Combine multiple window functions — total share, running total, and rank — in one complex view.

**Query:**
```sql
CREATE VIEW sales_portfolio AS
SELECT store_id,
       SUM(total) OVER ()                                   AS grand_total,
       SUM(total) / NULLIF(SUM(total) OVER (), 0)           AS share_of_total,
       SUM(total) OVER (ORDER BY store_id)                  AS running_total,
       RANK() OVER (ORDER BY SUM(total) DESC)               AS revenue_rank
FROM sales
GROUP BY store_id;
```
**Explanation:** Window functions layered over one GROUP BY compute percentages, cumulative sums, and ranks in a single scan — a maxed-out reporting view.

## Q96: Prevent a refresh from blocking long-running report queries (lock analysis and fix).

**Query:**
```sql
-- PostgreSQL: observe blocking
SELECT pid, state, wait_event_type, wait_event, query
FROM pg_stat_activity WHERE wait_event_type = 'Lock';

-- Fix: swap the blocking full refresh for a concurrent one
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_revenue;   -- advisory lock instead
```
**Explanation:** Non-concurrent refresh sets `ACCESS EXCLUSIVE`, which blocks everything; `CONCURRENTLY` uses the lighter `SHARE UPDATE EXCLUSIVE` so readers proceed while the snapshot swaps.

## Q97: Combine three result sets — current, last year, and forecast — using UNION ALL in one reporting view.

**Query:**
```sql
CREATE VIEW revenue_comparison AS
SELECT 'current' AS period, DATE(order_date) AS day, SUM(total) AS revenue
FROM orders WHERE order_date >= date '2026-01-01' GROUP BY 1
UNION ALL
SELECT 'previous' AS period, DATE(order_date) AS day, SUM(total) AS revenue
FROM orders WHERE order_date BETWEEN date '2025-01-01' AND date '2025-12-31' GROUP BY 1
UNION ALL
SELECT 'forecast', day, revenue FROM forecast_2026;
```
**Explanation:** Tagged branches plus `UNION ALL` build a single, self-labeling series; the `period` column lets one chart compare current vs last-year vs forecast row by row.

## Q98: Write the full production materialized-view pattern: definition, unique index, concurrent refresh, and read path.

**Query:**
```sql
-- PostgreSQL
CREATE MATERIALIZED VIEW mv_store_revenue AS
SELECT store_id, DATE_TRUNC('month', order_date) AS month, SUM(total) AS revenue
FROM orders GROUP BY 1, 2;

CREATE UNIQUE INDEX ux_mv_store_revenue ON mv_store_revenue (store_id, month);
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_store_revenue;

-- Business read path (never hits orders directly)
SELECT store_id, revenue FROM mv_store_revenue WHERE month = date_trunc('month', now());
```
**Explanation:** Definition + unique key + concurrent refresh + scheduled job = a self-consistent, non-blocking snapshot; dashboards read the MV and never aggregate the base table.

## Q99: Build a role-aware masking view that shows full data to admins and masked data to everyone else.

**Query:**
```sql
-- PostgreSQL
CREATE VIEW employee_masked AS
SELECT employee_id, first_name, last_name,
       CASE WHEN current_user IN ('admin1', 'admin2') THEN email
            ELSE left(email, 2) || '***@' || split_part(email, '@', 2) END AS email,
       CASE WHEN current_user IN ('admin1', 'admin2') THEN salary
            ELSE NULL END AS salary
FROM employees;

GRANT SELECT ON employee_masked TO hr_role, bi_role;
```
**Explanation:** Masking is decided dynamically per `current_user` inside the view, so one object gives admins plaintext and other roles scrubbed data — no row-level policies needed.

## Q100: Capstone: lay out a three-layer reporting architecture — base views, aggregate materialized views, and final presentation views — that stays secure and fast.

**Query:**
```sql
-- LAYER 1: base, security-filtered views (grant these, not tables)
CREATE VIEW v_orders AS
SELECT * FROM orders
WHERE store_id IN (SELECT store_id FROM allowed_stores WHERE db_user = current_user);

CREATE VIEW v_customers AS
SELECT customer_id, first_name, last_name,
       left(email, 2) || '***@' || split_part(email, '@', 2) AS masked_email
FROM customers;

-- LAYER 2: materialized aggregate snapshot (refresh off-peak, concurrently)
CREATE MATERIALIZED VIEW mv_store_daily AS
SELECT DATE(o.order_date) AS day, o.store_id, c.country,
       COUNT(*) AS orders, SUM(o.total) AS revenue
FROM v_orders o JOIN v_customers c USING (customer_id)
GROUP BY 1, 2, 3;

CREATE UNIQUE INDEX ux_mv_store_daily ON mv_store_daily (day, store_id, country);
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_store_daily;
SELECT cron.schedule('mv-store-daily', '0 2 * * *',
  'REFRESH MATERIALIZED VIEW CONCURRENTLY mv_store_daily');

-- LAYER 3: presentation views on the snapshot (fast, cheap to run)
CREATE VIEW exec_dashboard AS
SELECT day, SUM(revenue) AS revenue,
       SUM(revenue) - LAG(SUM(revenue)) OVER (ORDER BY day) AS delta
FROM mv_store_daily
WHERE country = 'India'
GROUP BY day;

-- Consumers only ever see exec_dashboard / mv_store_daily.
SELECT * FROM exec_dashboard ORDER BY day DESC LIMIT 7;
```
**Explanation:** Layer 1 encapsulates security and masking; layer 2 materializes the heavy aggregation once; layer 3 adds presentation logic on top of the snapshot. The pipeline stays fast, secure (views, not tables), and fresh (concurrent scheduled refresh).

