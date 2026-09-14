# Common Table Expressions (CTEs) — 100 SQL Interview Q&A

## Q1: Write a query using a simple CTE to list the names and hire dates of all employees in the Sales department.

**Query:**
```sql
WITH sales_team AS (
    SELECT employee_id, first_name, last_name, hire_date
    FROM employees
    WHERE department = 'Sales'
)
SELECT first_name, last_name, hire_date
FROM sales_team
ORDER BY hire_date;
```
**Explanation:** The CTE `sales_team` isolates the filtering logic so the outer query is easy to read; it behaves like a temporary named result set valid for the lifetime of the single statement.

**Alt1:** Same logic as a derived table (subquery in FROM):
```sql
SELECT first_name, last_name, hire_date
FROM (
    SELECT employee_id, first_name, last_name, hire_date
    FROM employees
    WHERE department = 'Sales'
) AS sales_team
ORDER BY hire_date;
```
**Explanation:** A derived table lives inline in the FROM clause; a CTE reads from the top, can be referenced more than once, and makes the query read in the order you think about it.

## Q2: Write a query that defines two CTEs separated by commas — one for high-value orders and one for VIP customers — then list orders together with customer names.

**Query:**
```sql
WITH high_value_orders AS (
    SELECT order_id, customer_id, total
    FROM orders
    WHERE total > 1000
),
vip_customers AS (
    SELECT customer_id, first_name, last_name
    FROM customers
    WHERE loyalty_rank = 'VIP'
)
SELECT v.first_name, v.last_name, h.order_id, h.total
FROM high_value_orders h
JOIN vip_customers v ON v.customer_id = h.customer_id
ORDER BY h.total DESC;
```
**Explanation:** CTEs are declared between `WITH` and the main `SELECT`, one after another, separated by commas. Each acts like a named table for the whole statement.

**Alt1:** Same output via a single derived table join (harder to read as complexity grows):
```sql
SELECT v.first_name, v.last_name, h.order_id, h.total
FROM (SELECT order_id, customer_id, total FROM orders WHERE total > 1000) h
JOIN (SELECT customer_id, first_name, last_name FROM customers WHERE loyalty_rank = 'VIP') v
  ON v.customer_id = h.customer_id
ORDER BY h.total DESC;
```
**Explanation:** Both produce the same rows, but nesting subqueries scalably becomes unreadable; the CTE version reads top-down.

## Q3: Write a query that uses a one-row CTE as a readable way to hold a business threshold, then list orders above that threshold.

**Query:**
```sql
WITH threshold AS (
    SELECT 5000 AS min_total
)
SELECT o.order_id, o.customer_id, o.total
FROM orders o
CROSS JOIN threshold t
WHERE o.total >= t.min_total
ORDER BY o.total DESC;
```
**Explanation:** A singleton CTE acts like a named "variable": one query feeds the magic number into the predicate, and changing it later only requires editing the CTE.

**Alt1:** Oracle needs a `FROM`, so the same idea reads:
```sql
-- Oracle
WITH threshold AS (
    SELECT 5000 AS min_total FROM dual
)
SELECT o.order_id, o.customer_id, o.total
FROM orders o, threshold t
WHERE o.total >= t.min_total;
```
**Explanation:** Oracle 12c+ supports CTEs but requires `dual` for a value-only SELECT; the approach is otherwise identical.

## Q4: Write a CTE that computes the company-wide average salary, then list every employee who earns more than that average.

**Query:**
```sql
WITH company_avg AS (
    SELECT AVG(salary) AS avg_salary
    FROM employees
)
SELECT e.employee_id, e.first_name, e.last_name, e.salary
FROM employees e
CROSS JOIN company_avg c
WHERE e.salary > c.avg_salary
ORDER BY e.salary DESC;
```
**Explanation:** Compute the scalar aggregate once in a CTE, then compare every row against it. Because the CTE is a single row, a `CROSS JOIN` is safe and portable.

**Alt1:** Scalar subquery in the WHERE clause:
```sql
SELECT employee_id, first_name, last_name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY salary DESC;
```
**Explanation:** This works and is concise, but the subquery is a second, unnamed pass over the table; the CTE name documents intent and is reusable if you need the average again later.

## Q5: Write a query using a CTE to compute department averages and then list each employee who earns above their own department's average.

**Query:**
```sql
WITH department_avg AS (
    SELECT department, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
)
SELECT e.employee_id, e.first_name, e.salary, da.avg_salary
FROM employees e
JOIN department_avg da ON da.department = e.department
WHERE e.salary > da.avg_salary
ORDER BY e.department, e.salary DESC;
```
**Explanation:** The CTE materializes one average per department, then a join matches each employee to their group's average, and the WHERE keeps only above-average earners.

**Alt1:** Window-function approach (ANSI/Postgres/MySQL 8+):
```sql
SELECT employee_id, first_name, salary
FROM (
    SELECT employee_id, first_name, salary,
           AVG(salary) OVER (PARTITION BY department) AS dept_avg
    FROM employees
) t
WHERE salary > dept_avg;
```
**Explanation:** Shorter, but a window function computes the aggregate per row; the CTE version is more approachable and reuses one sub-result if needed elsewhere in the statement.

## Q6: Write chained CTEs: first total sales per region, then identify the region with the highest total.

**Query:**
```sql
WITH region_total AS (
    SELECT region, SUM(amount) AS total_sales
    FROM sales
    GROUP BY region
),
top_region AS (
    SELECT region, total_sales
    FROM region_total
    ORDER BY total_sales DESC
    LIMIT 1
)
SELECT * FROM top_region;
```
**Explanation:** The second CTE references the first — chaining — so each stage of the analysis is a clearly labelled step instead of one giant query.

**Alt1:** Delete the second CTE and find the max with a subquery:
```sql
WITH region_total AS (
    SELECT region, SUM(amount) AS total_sales
    FROM sales
    GROUP BY region
)
SELECT region, total_sales
FROM region_total
WHERE total_sales = (SELECT MAX(total_sales) FROM region_total);
```
**Explanation:** Same result, and note the CTE `region_total` is now referenced twice — which is exactly what chaining into a second CTE avoided doing visually.

## Q7: Write a query that reuses one CTE in two different places of the same statement.

**Query:**
```sql
WITH region_total AS (
    SELECT region, SUM(amount) AS total_sales
    FROM sales
    GROUP BY region
)
SELECT r.region, r.total_sales,
       ROUND(100.0 * r.total_sales / g.grand_total, 2) AS pct_of_company
FROM region_total r
CROSS JOIN (SELECT SUM(total_sales) AS grand_total FROM region_total) g
ORDER BY r.total_sales DESC;
```
**Explanation:** `region_total` appears twice — once per region row, once to sum the total across all regions — without re-typing the aggregation logic.

## Q8: Write a CTE-based query that prepares a deduplicated copy of a staging table by keeping the earliest record per email address.

**Query:**
```sql
WITH keep_one AS (
    SELECT email, MIN(user_id) AS keep_id
    FROM staging_users
    GROUP BY email
)
SELECT s.*
FROM staging_users s
JOIN keep_one k ON k.keep_id = s.user_id;
```
**Explanation:** The CTE computes the "survivor" id per group, and the main query keeps exactly one row per email — a preparation step often used before loading a clean table.

**Alt1:** ROW_NUMBER ranking approach:
```sql
SELECT user_id, email, first_name
FROM (
    SELECT user_id, email, first_name,
           ROW_NUMBER() OVER (PARTITION BY email ORDER BY created_at) AS rn
    FROM staging_users
) ranked
WHERE rn = 1;
```
**Explanation:** Both are valid "row per group" patterns; GROUP BY + MIN works anywhere, while ROW_NUMBER gives you more control when the "winner" rule is more elaborate.

## Q9: Write an INSERT ... SELECT that moves rows through a CTE into an archive table.

**Query:**
```sql
WITH recent_orders AS (
    SELECT order_id, customer_id, total, order_date
    FROM orders
    WHERE order_date < CURRENT_DATE - INTERVAL 365 DAY
)
INSERT INTO orders_archive (order_id, customer_id, total, order_date)
SELECT order_id, customer_id, total, order_date
FROM recent_orders;
```
**Explanation:** The CTE is used inside the FROM of an INSERT ... SELECT, so you can archive a computed, filtered dataset without a separate staging table (works in Postgres/SQL Server/MySQL 8+).

**Alt1:** Same data flow as a plain subquery:
```sql
INSERT INTO orders_archive (order_id, customer_id, total, order_date)
SELECT order_id, customer_id, total, order_date
FROM orders
WHERE order_date < CURRENT_DATE - INTERVAL 365 DAY;
```
**Explanation:** When you only select from the CTE once, a subquery is equivalent; the CTE earns its pay when the same set is referenced multiple times.

## Q10: Write a SQL Server UPDATE that uses a CTE to update only the top-flagged employees, and show the Postgres style alternative.

**Query:**
```sql
-- SQL Server / Postgres
WITH flagged AS (
    SELECT employee_id, performance_rating
    FROM employees
    WHERE performance_rating >= 4
)
UPDATE flagged
SET performance_rating = 5;
```
**Explanation:** Both SQL Server and Postgres let you target a CTE directly for UPDATE — the CTE behaves like the target of the UPDATE statement, so predicate and target live in exactly one place.

**Alt1:** Postgres update-with-join form (identical effect):
```sql
-- Postgres
WITH flagged AS (
    SELECT employee_id FROM employees WHERE performance_rating >= 4
)
UPDATE employees e
SET performance_rating = 5
FROM flagged f
WHERE e.employee_id = f.employee_id;
```
**Explanation:** This spelling separates the target table from the source CTE and is the form most people generalize when the UPDATE must be driven by an aggregation.

## Q11: Write a DELETE that removes rows using a CTE in Postgres and show the MySQL multi-table equivalent.

**Query:**
```sql
-- Postgres
WITH stale_inventory AS (
    SELECT product_id FROM inventory WHERE last_sold_date < CURRENT_DATE - INTERVAL 730 DAY
)
DELETE FROM inventory i
USING stale_inventory s
WHERE i.product_id = s.product_id;
```
**Explanation:** Postgres deletes via `USING`, with the CTE naming exactly which rows are eligible — clearer than a bare `WHERE EXISTS` when the rule is built from an aggregation.

**Alt1:** MySQL multi-table DELETE with a derived-table join:
```sql
-- MySQL
DELETE i
FROM inventory i
JOIN (
    SELECT product_id FROM inventory WHERE last_sold_date < CURRENT_DATE - INTERVAL 730 DAY
) s ON i.product_id = s.product_id;
```
**Explanation:** MySQL 8 traditionally performs DML against joins rather than `WITH ... DELETE`; the derived table plays the same "compute the victims" role as the Postgres CTE.

## Q12: Build a chained multi-stage pipeline that rolls daily sales up to monthly totals, then compares each month with the same month a year earlier (YoY delta).

**Query:**
```sql
WITH monthly AS (
    SELECT EXTRACT(YEAR FROM order_date)  AS yr,
           EXTRACT(MONTH FROM order_date) AS mo,
           SUM(total) AS rev
    FROM orders
    GROUP BY 1, 2
),
prev_year AS (
    SELECT * FROM monthly
)
SELECT a.yr, a.mo, a.rev,
       b.rev AS prev_year_rev,
       a.rev - b.rev AS yoy_delta
FROM monthly a
LEFT JOIN prev_year b
  ON b.mo = a.mo AND b.yr = a.yr - 1
ORDER BY a.yr, a.mo;
```
**Explanation:** Stage one aggregates to month, then a self-join of the pipeline aligns each month with its year-ago counterpart — no window function needed, and each stage stays readable.

## Q13: Write a Postgres CTE that builds a date spine — every day in January 2024 — and counts sales per day, including days with no sales.

**Query:**
```sql
WITH days AS (
    SELECT d::date AS day
    FROM generate_series('2024-01-01', '2024-01-31', INTERVAL '1 day') AS d
)
SELECT days.day, COUNT(s.sale_id) AS sales_count
FROM days
LEFT JOIN sales s ON s.sale_date = days.day
GROUP BY days.day
ORDER BY days.day;
```
**Explanation:** `generate_series` produces the full range of dates, and the LEFT JOIN guarantees every calendar day appears — missing days surface as zeros instead of silently vanishing.

**Alt1:** SQL Server equivalent using a numbers helper (no recursive CTE, no generate_series):
```sql
-- SQL Server
WITH n AS (
    SELECT ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) - 1 AS n
    FROM sys.all_objects a CROSS JOIN sys.all_objects b
)
SELECT DATEADD(day, n.n, '2024-01-01') AS day,
       COUNT(s.sale_id) AS sales_count
FROM n
LEFT JOIN sales s ON s.sale_date = DATEADD(day, n.n, '2024-01-01')
WHERE n.n BETWEEN 0 AND 30
GROUP BY DATEADD(day, n.n, '2024-01-01');
```
**Explanation:** A number table replaces generate_series; DATEADD maps each integer to a date. ROW_NUMBER is used purely to create a sequence, not for analytics.

## Q14: Write a CTE that produces the integers 1 through 100 without recursion.

**Query:**
```sql
SELECT g AS n
FROM generate_series(1, 100) AS g;
```
**Explanation:** Postgres's `generate_series` is the simplest recursive-free number table; it is routinely chained into date spines, split logic and sampling.

**Alt1:** Dialect-idiomatic generators:
```sql
-- SQL Server
WITH numbers AS (
    SELECT ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n
    FROM sys.all_objects a CROSS JOIN sys.all_objects b
)
SELECT TOP (100) n FROM numbers;

-- MySQL 8
WITH RECURSIVE seq AS (SELECT 1 AS n UNION ALL SELECT n + 1 FROM seq WHERE n < 100)
SELECT n FROM seq;
```
**Explanation:** SQL Server builds one from catalog objects; MySQL needs its recursive form since it lacks generate_series — a sibling file covers recursion in depth, this trick is only for tables.

## Q15: Write a query that needs the employee table twice — employees joined to their managers — using CTEs.

**Query:**
```sql
WITH emps AS (
    SELECT employee_id, first_name, manager_id
    FROM employees
)
SELECT e.first_name AS employee, m.first_name AS manager
FROM emps e
LEFT JOIN emps m ON m.employee_id = e.manager_id
ORDER BY m.first_name, e.first_name;
```
**Explanation:** A self-join reads much better when the same table is aliased once in a CTE and then joined under two distinct names.

**Alt1:** Two inline derived tables:
```sql
SELECT e.first_name AS employee, m.first_name AS manager
FROM (SELECT employee_id, first_name, manager_id FROM employees) e
LEFT JOIN (SELECT employee_id, first_name FROM employees) m
  ON m.employee_id = e.manager_id;
```
**Explanation:** Functionally identical; the CTE version avoids repeating the source table name and keeps column intention closer to the top.

## Q16: Write three chained CTEs in one statement: roll orders to customer totals, then to region totals, then pick the customer-level detail for the best region.

**Query:**
```sql
WITH customer_total AS (
    SELECT customer_id, region, SUM(total) AS spent
    FROM orders
    GROUP BY customer_id, region
),
region_total AS (
    SELECT region, SUM(spent) AS total_spent
    FROM customer_total
    GROUP BY region
),
best_region AS (
    SELECT region FROM region_total ORDER BY total_spent DESC LIMIT 1
)
SELECT c.customer_id, c.spent
FROM customer_total c
JOIN best_region b ON b.region = c.region
ORDER BY c.spent DESC;
```
**Explanation:** Three stages, each one consuming the previous one's output — a poster child for turning a multi-step business question into a readable down-the-page pipeline.

## Q17: Write a query that references the same CTE twice, and contrast what Postgres does with that CTE.

**Query:**
```sql
WITH region_total AS (
    SELECT region, SUM(amount) AS total_sales
    FROM sales
    GROUP BY region
)
SELECT region,
       total_sales,
       total_sales - (SELECT AVG(total_sales) FROM region_total) AS diff_from_company_avg
FROM region_total;
```
**Explanation:** In Postgres, a CTE referenced more than once is materialized to a temp result unless it is trivially inlined, so the expensive `sales` scan runs once; SQL Server behaves similarly by default.

**Alt1:** Breaking the reference into a derived table (Postgres will inline rather than materialize):
```sql
SELECT r.region, r.total_sales,
       r.total_sales - (SELECT AVG(total_sales) FROM (SELECT region, SUM(amount) AS total_sales FROM sales GROUP BY region) x) AS diff
FROM (SELECT region, SUM(amount) AS total_sales FROM sales GROUP BY region) r;
```
**Explanation:** Bidirectional inlining means Postgres recomputes the aggregate — fine on small data, slower on big tables; a clearly-materialized CTE often wins on repeated references.

## Q18: Break a complicated report into three named CTEs (orders -> outstanding balances -> delinquent list) to modularize the logic.

**Query:**
```sql
WITH orders AS (
    SELECT customer_id, order_id, total, paid
    FROM orders_table
),
balances AS (
    SELECT customer_id, order_id, total - paid AS outstanding
    FROM orders
    WHERE paid < total
),
delinquent AS (
    SELECT customer_id, SUM(outstanding) AS owing
    FROM balances
    GROUP BY customer_id
    HAVING SUM(outstanding) > 1000
)
SELECT * FROM delinquent ORDER BY owing DESC;
```
**Explanation:** Each CTE answers one sentence of the requirement, so the final SELECT is trivial and each step is testable in isolation.

## Q19: Rewrite a report that must run in several statements so the heavy aggregation is computed once in a temp table instead of a CTE.

**Query:**
```sql
-- Postgres / SQL Server
CREATE TEMP TABLE region_totals AS
SELECT region, SUM(amount) AS total_sales
FROM sales
GROUP BY region;

SELECT * FROM region_totals ORDER BY total_sales DESC;   -- statement 1
SELECT region, total_sales FROM region_totals WHERE total_sales > 50000;  -- statement 2
DROP TABLE region_totals;
```
**Explanation:** A CTE dies at the end of its statement; a temp table survives for the session, so when you genuinely need the dataset across many statements, a temp table is the right tool.

**Alt1:** The CTE equivalent (single statement only — the key difference):
```sql
WITH region_totals AS (
    SELECT region, SUM(amount) AS total_sales FROM sales GROUP BY region
)
SELECT * FROM region_totals ORDER BY total_sales DESC;
```
**Explanation:** Same shape, single use. The tradeoff to state in an interview: CTE = per-statement, temp table = cross-statement, always weigh in both the lifecycle and the cost.

## Q20: Write a CTE that counts orders per day for the last 30 days, then lists only days that beat the daily average.

**Query:**
```sql
WITH daily AS (
    SELECT order_date, COUNT(*) AS orders_count
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL 30 DAY
    GROUP BY order_date
)
SELECT order_date, orders_count
FROM daily
WHERE orders_count > (SELECT AVG(orders_count) FROM daily)
ORDER BY order_date;
```
**Explanation:** `daily` is computed once and then reused — once row-by-row for the comparison and once to compute the average — a neat demo of CTE reuse in a small statement.

## Q21: Write a CTE-based query listing customers who have never placed an order (anti-join).

**Query:**
```sql
WITH ordering_customers AS (
    SELECT DISTINCT customer_id FROM orders
)
SELECT c.customer_id, c.first_name, c.last_name
FROM customers c
LEFT JOIN ordering_customers o ON o.customer_id = c.customer_id
WHERE o.customer_id IS NULL
ORDER BY c.customer_id;
```
**Explanation:** The LEFT JOIN + NULL check filters out everyone who appears in the CTE, i.e. exactly the customers with zero orders — no NOT IN edge cases with NULLs.

**Alt1:** NOT EXISTS form:
```sql
SELECT customer_id, first_name, last_name
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```
**Explanation:** For a one-shot check NOT EXISTS is equally correct and often fast; the CTE version shines when `ordering_customers` is reused elsewhere in the same statement.

## Q22: Write a query that counts orders per customer in a CTE and then keeps only customers with more than five orders.

**Query:**
```sql
WITH order_counts AS (
    SELECT customer_id, COUNT(*) AS num_orders
    FROM orders
    GROUP BY customer_id
)
SELECT customer_id, num_orders
FROM order_counts
WHERE num_orders > 5
ORDER BY num_orders DESC;
```
**Explanation:** Aggregation happens in the CTE; the outer WHERE filters on the alias — you cannot filter an aggregate inside the GROUP BY, so a CTE is the natural place to do it.

## Q23: Write a query that computes a running total over a week using only CTEs and joins (no window function in the main query).

**Query:**
```sql
WITH days AS (
    SELECT order_date, SUM(total) AS revenue
    FROM orders
    WHERE order_date BETWEEN '2024-01-01' AND '2024-01-07'
    GROUP BY order_date
)
SELECT a.order_date,
       SUM(b.revenue) AS running_total
FROM days a
JOIN days b ON b.order_date <= a.order_date
GROUP BY a.order_date
ORDER BY a.order_date;
```
**Explanation:** A self-join accumulates every prior-or-equal revenue to the current day; O(n^2)-ish work, but a valid join-only strategy when the data is small.

**Alt1:** The idiomatic window-function version:
```sql
SELECT order_date, SUM(revenue) OVER (ORDER BY order_date) AS running_total
FROM (
    SELECT order_date, SUM(total) AS revenue FROM orders
    WHERE order_date BETWEEN '2024-01-01' AND '2024-01-07'
    GROUP BY order_date
) d
ORDER BY order_date;
```
**Explanation:** The window version is the production answer for running totals; the join-CTE version is the "how it works under the hood" answer and is covered here because this file's siblings own window functions.

## Q24: Build a fiscal-calendar helper CTE that maps dates to a fiscal year label, then group orders by it.

**Query:**
```sql
WITH fiscal AS (
    SELECT order_id,
           CASE WHEN EXTRACT(MONTH FROM order_date) >= 4
                THEN TO_CHAR(order_date, 'YYYY') || '-' || (EXTRACT(YEAR FROM order_date) + 1)
                ELSE (EXTRACT(YEAR FROM order_date) - 1) || '-' || TO_CHAR(order_date, 'YYYY')
           END AS fiscal_year
    FROM orders
)
SELECT fiscal_year, COUNT(*) AS orders_count
FROM fiscal
GROUP BY fiscal_year
ORDER BY fiscal_year;
```
**Explanation:** One CTE centralizes the fiddly fiscal-year rule; the reporting query never sees the CASE expression and cannot get it subtly wrong per call site (works on Postgres/Oracle).

## Q25: Write chained CTEs that find the highest-totaled product category, then return every category that ties with it.

**Query:**
```sql
WITH category_total AS (
    SELECT category_id, SUM(amount) AS cat_sales
    FROM sales
    GROUP BY category_id
),
best_total AS (
    SELECT MAX(cat_sales) AS best FROM category_total
)
SELECT c.category_id, c.cat_sales
FROM category_total c
JOIN best_total b ON b.best = c.cat_sales
ORDER BY c.category_id;
```
**Explanation:** `best_total` holds a single scalar that any number of categories can equal, so ties are preserved naturally by the join instead of being chopped by an arbitrary ORDER BY + LIMIT.

## Q26: Write chained CTEs that build a marketing funnel: page views -> sign-ups -> purchases, then compute conversion rates between stages.

**Query:**
```sql
WITH pageviews AS (
    SELECT COUNT(*) AS views FROM events WHERE event_type = 'page_view'
),
signups AS (
    SELECT COUNT(*) AS signups FROM events WHERE event_type = 'sign_up'
),
purchases AS (
    SELECT COUNT(*) AS purchases FROM events WHERE event_type = 'purchase'
)
SELECT views, signups, purchases,
       ROUND(100.0 * signups / NULLIF(views, 0), 2) AS view_to_signup_pct,
       ROUND(100.0 * purchases / NULLIF(signups, 0), 2) AS signup_to_purchase_pct
FROM pageviews, signups, purchases;
```
**Explanation:** Three independent CTEs each own one stage, and the final SELECT reads like the metric definition — NULLIF keeps division-by-zero from crashing the report.

## Q27: Write a data-quality CTE that flags products with missing or clearly invalid prices.

**Query:**
```sql
WITH flagged AS (
    SELECT product_id, product_name, price,
           CASE WHEN price IS NULL THEN 'missing price'
                WHEN price <= 0 THEN 'non-positive price'
                ELSE 'ok'
           END AS status
    FROM products
)
SELECT product_id, product_name, price, status
FROM flagged
WHERE status <> 'ok'
ORDER BY status, product_id;
```
**Explanation:** All the messy validation rules live in one CTE; the outer query simply "keeps what isn't ok", and adding a new rule means touching one CASE.

## Q28: Write a CTE that gives every date a friendly weekday label and then counts orders grouped by that label.

**Query:**
```sql
WITH labeled AS (
    SELECT order_id,
           TO_CHAR(order_date, 'Dy') AS weekday
    FROM orders
)
SELECT weekday, COUNT(*) AS order_count
FROM labeled
GROUP BY weekday
ORDER BY MIN(order_date);
```
**Explanation:** The enrichment (date -> weekday) is computed once in the CTE and the GROUP BY works on the label. `TO_CHAR` works on Postgres/Oracle; MySQL uses `DATE_FORMAT`.

**Alt1:** MySQL dialect:
```sql
SELECT order_date, DAYNAME(order_date) AS weekday, COUNT(*) AS order_count
FROM orders
GROUP BY order_date, DAYNAME(order_date)
ORDER BY order_date;
```
**Explanation:** Same spirit; the CTE variant keeps the label logic above the aggregation so the GROUP BY reads cleanly instead of repeating the expression.

## Q29: Write a query that defines a "VIP customer" CTE and joins it back to the orders table to list their recent orders.

**Query:**
```sql
WITH vip AS (
    SELECT customer_id FROM customers WHERE lifetime_value >= 100000
)
SELECT o.order_id, o.customer_id, o.order_date, o.total
FROM orders o
JOIN vip v ON v.customer_id = o.customer_id
WHERE o.order_date >= CURRENT_DATE - INTERVAL 90 DAY
ORDER BY o.total DESC;
```
**Explanation:** Membership logic sits in `vip`; the main query composes it with time filtering, showing how a named business concept reduces the join predicate to one line.

## Q30: Write CTEs that count male and female customers separately, then compute the ratio in the final SELECT.

**Query:**
```sql
WITH counts AS (
    SELECT gender, COUNT(*) AS n
    FROM customers
    GROUP BY gender
)
SELECT gender, n,
       ROUND(100.0 * n / SUM(n) OVER (), 1) AS pct_of_all
FROM counts;
```
**Explanation:** One CTE computes the per-group counts; the outer query adds the overall denominator — here with a window aggregate, which this file's sibling owns but is a legal alternative.

**Alt1:** No window function — a second CTE for the grand total:
```sql
WITH counts AS (
    SELECT gender, COUNT(*) AS n FROM customers GROUP BY gender
),
total AS (
    SELECT SUM(n) AS all_customers FROM counts
)
SELECT c.gender, c.n,
       ROUND(100.0 * c.n / t.all_customers, 1) AS pct_of_all
FROM counts c CROSS JOIN total t;
```
**Explanation:** Purely CTE mechanics — reuse `counts` to derive `total`, then cross join the scalar back. Both answers are acceptable; this one stays window-function-free.

## Q31: Write chained CTEs that roll products up to their top-selling category, then average the category totals.

**Query:**
```sql
WITH product_sales AS (
    SELECT product_id, category_id, SUM(amount) AS revenue
    FROM sales
    GROUP BY product_id, category_id
),
category_sales AS (
    SELECT category_id, SUM(revenue) AS cat_revenue
    FROM product_sales
    GROUP BY category_id
)
SELECT AVG(cat_revenue) AS avg_category_revenue,
       MAX(cat_revenue) AS max_category_revenue
FROM category_sales;
```
**Explanation:** Each roll-up consumes the previous stage; the final query is an aggregate on aggregates, which only works because `category_sales` already materialized the per-category totals.

## Q32: Write a query that references the same employees table twice via CTEs to compare each employee's own department and the whole-company average salary.

**Query:**
```sql
WITH dept_avg AS (
    SELECT department, AVG(salary) AS avg_salary FROM employees GROUP BY department
),
co_avg AS (
    SELECT AVG(salary) AS avg_salary FROM employees
)
SELECT e.first_name, e.department, e.salary,
       d.avg_salary AS dept_avg, c.avg_salary AS company_avg,
       e.salary - d.avg_salary AS vs_dept,
       e.salary - c.avg_salary AS vs_company
FROM employees e
JOIN dept_avg d ON d.department = e.department
CROSS JOIN co_avg c;
```
**Explanation:** Two read-only CTEs both target `employees` but with different granularities; joining both on makes the comparison one clean, self-describing statement.

## Q33: Write CTEs that compute per-category revenue and a grand total, then return each category with its share (no window functions).

**Query:**
```sql
WITH category_total AS (
    SELECT category_id, SUM(amount) AS cat_rev
    FROM sales
    GROUP BY category_id
),
grand_total AS (
    SELECT SUM(cat_rev) AS all_rev FROM category_total
)
SELECT c.category_id, c.cat_rev,
       ROUND(100.0 * c.cat_rev / g.all_rev, 2) AS share_pct
FROM category_total c
CROSS JOIN grand_total g
ORDER BY share_pct DESC;
```
**Explanation:** The grand total is derived from the same `category_total` CTE (not the raw table), so the two stages share one source of truth and cannot disagree.

## Q34: Write a Postgres UPDATE that raises salaries using a CTE that holds the department averages.

**Query:**
```sql
-- Postgres
WITH dept_avg AS (
    SELECT department, AVG(salary) AS avg_dept
    FROM employees
    GROUP BY department
)
UPDATE employees e
SET salary = salary + 1000
FROM dept_avg d
WHERE d.department = e.department
  AND e.salary < d.avg_dept;
```
**Explanation:** The CTE computes each department's average once, then the UPDATE ... FROM applies a raise only to below-average earners — a single transactional statement.

**Alt1:** SQL Server CTE-targeted syntax:
```sql
-- SQL Server
WITH below_avg AS (
    SELECT e.employee_id, d.avg_dept
    FROM employees e
    JOIN (SELECT department, AVG(salary) AS avg_dept FROM employees GROUP BY department) d
      ON d.department = e.department
    WHERE e.salary < d.avg_dept
)
UPDATE below_avg
SET avg_dept = avg_dept  -- placeholder; see explanation
```
**Explanation:** SQL Server allows an updatable CTE, but the constraint is that only the CTE's own columns (and thus one table) are updatable — for multi-source updates the Postgres FROM form is the cleaner pattern.

## Q35: Write a DELETE that purges rows using a CTE in SQL Server, and give the MySQL equivalent.

**Query:**
```sql
-- SQL Server
WITH doomed AS (
    SELECT invoice_id FROM invoices WHERE total < paid * 0.5   -- deeply discounted
)
DELETE d
FROM doomed d
JOIN invoices i ON i.invoice_id = d.invoice_id;
```
**Explanation:** The CTE isolates which rows die; SQL Server then deletes through the join. Postgres got the USING form earlier; this is the SQL Server spelling.

**Alt1:** MySQL multi-table DELETE:
```sql
-- MySQL
DELETE i
FROM invoices i
JOIN (SELECT invoice_id FROM invoices WHERE total < paid * 0.5) d
  ON i.invoice_id = d.invoice_id;
```
**Explanation:** MySQL 8 relies on the multi-table DELETE shape; the derived table mirrors the CTE's purpose even though the keyword isn't used at the statement's top level.

## Q36: Write a CTE prepared step that deduplicates a log table on (session_id, event) keeping the first event, then inserts the clean set.

**Query:**
```sql
WITH clean_events AS (
    SELECT session_id, event, MIN(occurred_at) AS first_at
    FROM raw_events
    GROUP BY session_id, event
)
INSERT INTO events (session_id, event, first_occurred_at)
SELECT session_id, event, first_at
FROM clean_events;
```
**Explanation:** GROUP BY + MIN collapses duplicates before the INSERT runs, so the destination table only ever sees one row per (session_id, event) — dedup as a preparation stage.

**Alt1:** ROW_NUMBER dedup (clearer when the "first" rule has a tie-breaker):
```sql
INSERT INTO events (session_id, event, first_occurred_at)
SELECT session_id, event, occurred_at
FROM (
    SELECT session_id, event, occurred_at,
           ROW_NUMBER() OVER (PARTITION BY session_id, event ORDER BY occurred_at) AS rn
    FROM raw_events
) t
WHERE rn = 1;
```
**Explanation:** Equivalent outcome; ROW_NUMBER scales better when the dedup key or ordering is more complex than a bare MIN.

## Q37: Write a CTE-based query that turns rows into columns using conditional aggregation (a mini pivot).

**Query:**
```sql
WITH source AS (
    SELECT product_id,
           CASE WHEN channel = 'web' THEN total ELSE 0 END AS web,
           CASE WHEN channel = 'mobile' THEN total ELSE 0 END AS mobile
    FROM sales
)
SELECT product_id,
       SUM(web)   AS web_total,
       SUM(mobile) AS mobile_total
FROM source
GROUP BY product_id;
```
**Explanation:** A CTE spreads each channel into its own column, and the outer SUM collapses them back into a product-per-row, channel-per-column mini pivot — no PIVOT operator needed.

## Q38: Write a query that fills zero days using a date-spine CTE left-joined to sales.

**Query:**
```sql
WITH days AS (
    SELECT d::date AS day
    FROM generate_series('2024-06-01', '2024-06-30', INTERVAL '1 day') d
)
SELECT days.day, COALESCE(SUM(s.amount), 0) AS daily_sales
FROM days
LEFT JOIN sales s ON s.sale_date = days.day
GROUP BY days.day
ORDER BY days.day;
```
**Explanation:** The spine guarantees all 30 rows; COALESCE turns NULL (no sale on that date) into a visible zero instead of a missing row.

## Q39: Write a query using a numbers CTE to report which weekday numbers fall in the data and which are entirely empty.

**Query:**
```sql
WITH weekdays AS (
    SELECT g AS dow FROM generate_series(0, 6) AS g
)
SELECT w.dow, COUNT(o.order_id) AS orders
FROM weekdays w
LEFT JOIN orders o ON EXTRACT(DOW FROM o.order_date) = w.dow
GROUP BY w.dow
ORDER BY w.dow;
```
**Explanation:** The spine is 0..6 (Sunday=0 in Postgres); the left join reveals weekday gaps. In MySQL use `DAYOFWEEK()` (1..7) and adjust the spine accordingly.

**Alt1:** SQL Server numbers helper:
```sql
-- SQL Server
WITH weekdays AS (
    SELECT ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) - 1 AS dow
    FROM sys.all_objects
)
SELECT w.dow, COUNT(o.order_id) AS orders
FROM weekdays w
LEFT JOIN orders o ON DATEPART(WEEKDAY, o.order_date) = w.dow
WHERE w.dow BETWEEN 0 AND 6
GROUP BY w.dow
ORDER BY w.dow;
```
**Explanation:** Same shape with a catalog-built sequence; the WHERE trims the helper to the window you actually need.

## Q40: Write a CTE that finds the five most frequent product categories and then labels them with a browse rank.

**Query:**
```sql
WITH frequency AS (
    SELECT category_id, COUNT(*) AS views
    FROM page_views
    GROUP BY category_id
)
SELECT category_id, views
FROM frequency
ORDER BY views DESC
LIMIT 5;
```
**Explanation:** The COUNT happens in the CTE; the outer query applies the top-N rule. Ordering inside a subquery trick like `ORDER BY ... LIMIT` inside a CTE is fine because the CTE's output is then used in FROM.

**Alt1:** Window rank version (for numbered output):
```sql
SELECT category_id, views
FROM (
    SELECT category_id, COUNT(*) AS views,
           ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS rn
    FROM page_views
    GROUP BY category_id
) t
WHERE rn <= 5;
```
**Explanation:** Production-quality top-N with explicit ranking; the plain LIMIT version is simpler and portable when you don't need to walk the rank values.

## Q41: Write chained CTEs that count new users per month and then roll those counts up to quarterly totals.

**Query:**
```sql
WITH monthly AS (
    SELECT DATE_TRUNC('month', signup_date) AS month, COUNT(*) AS new_users
    FROM users
    GROUP BY 1
),
quarterly AS (
    SELECT DATE_TRUNC('quarter', month) AS quarter, SUM(new_users) AS users
    FROM monthly
    GROUP BY 1
)
SELECT quarter, users FROM quarterly ORDER BY quarter;
```
**Explanation:** One stage groups raw rows to months, the next groups those months to quarters — an aggregation pipeline where each level trusts the previous one's precision. (MySQL: use `DATE_FORMAT(signup_date, '%Y-%m-01')` and quarters via `QUARTER()`.)

## Q42: Write a CTE that computes a safe reorder point per product and then lists everything currently below it.

**Query:**
```sql
WITH reorder_point AS (
    SELECT product_id,
           3 * AVG(weekly_sold) AS reorder_at
    FROM sales_history
    GROUP BY product_id
)
SELECT p.product_id, p.product_name, p.stock_qty, r.reorder_at
FROM products p
JOIN reorder_point r ON r.product_id = p.product_id
WHERE p.stock_qty <= r.reorder_at
ORDER BY p.stock_qty;
```
**Explanation:** The business rule (3 weeks of average sales) is computed exactly once in a CTE and then compared to live stock — the kind of helper dataset CTEs excel at.

## Q43: Write a query that centres a business rule (recent orders window) in one CTE and reuses it across several counter query branches.

**Query:**
```sql
WITH recent AS (
    SELECT *
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL 30 DAY
)
SELECT 'total' AS metric, COUNT(*) AS value FROM recent
UNION ALL
SELECT 'high_value', COUNT(*) FROM recent WHERE total > 1000
UNION ALL
SELECT 'from_vip', COUNT(*) FROM recent WHERE customer_rank = 'VIP';
```
**Explanation:** A single `recent` CTE feeds three different filters in one statement — the window rule is written once, and all branches can never go out of sync.

## Q44: Rewrite a deep nested-subquery report using CTEs solely for readability, keeping identical results.

**Query:**
```sql
WITH regional AS (
    SELECT region, SUM(amount) AS rev FROM sales GROUP BY region
),
above_avg AS (
    SELECT region, rev FROM regional
    WHERE rev > (SELECT AVG(rev) FROM regional)
)
SELECT region, rev, rev - (SELECT AVG(rev) FROM regional) AS beats_avg_by
FROM above_avg
ORDER BY rev DESC;
```
**Explanation:** Two CTEs replace two nesting levels, and the final SELECT is nearly English. Readability is CTE value proposition number one — results are provably identical.

## Q45: Write a statement that uses one CTE as a self-join target AND joins it to the base table — three references in total.

**Query:**
```sql
WITH region_total AS (
    SELECT region, SUM(amount) AS rev FROM sales GROUP BY region
)
SELECT r.region,
       r.rev,
       r.rev - b.best_region_rev AS gap_to_leader
FROM region_total r
CROSS JOIN (SELECT MAX(rev) AS best_region_rev FROM region_total) b
ORDER BY r.rev DESC;
```
**Explanation:** `region_total` is referenced twice (per-row read and scalar max) while the base `sales` table only appears inside the CTE — three logical touches, one physical definition.

## Q46: Write a CTE that finds each customer's most recent purchase date and then the count of their purchases since then.

**Query:**
```sql
WITH last_purchase AS (
    SELECT customer_id, MAX(order_date) AS last_date
    FROM orders
    GROUP BY customer_id
)
SELECT o.customer_id, l.last_date,
       COUNT(o.order_id) FILTER (WHERE o.order_date = l.last_date) AS purchases_on_last_day
FROM orders o
JOIN last_purchase l ON l.customer_id = o.customer_id
GROUP BY o.customer_id, l.last_date;
```
**Explanation:** MAX in the CTE identifies the anchor date; the outer query answers follow-up questions about it. (FILTER is Postgres; MySQL could use SUM(CASE WHEN ...).)

## Q47: Write chained CTEs that convert revenue in many currencies through a rate table into a single reporting currency.

**Query:**
```sql
WITH usd_rates AS (
    SELECT currency, rate_to_usd
    FROM exchange_rates
    WHERE effective_date = (SELECT MAX(effective_date) FROM exchange_rates)
),
local_rev AS (
    SELECT currency_code, SUM(amount) AS amount
    FROM transactions
    GROUP BY currency_code
)
SELECT r.currency_code, r.amount, u.rate_to_usd,
       ROUND(r.amount * u.rate_to_usd, 2) AS usd_amount
FROM local_rev r
JOIN usd_rates u ON u.currency = r.currency_code
ORDER BY usd_amount DESC;
```
**Explanation:** `usd_rates` snapshots the current conversion map; `local_rev` aggregates sales; the final join applies the FX. Each stage answers one question: "what rate", "how much", "in USD".

## Q48: Write a CTE query that reports average session length per feature from raw event logs.

**Query:**
```sql
WITH session_lengths AS (
    SELECT session_id,
           MAX(event_time) - MIN(event_time) AS length
    FROM events
    GROUP BY session_id
),
feature_sessions AS (
    SELECT DISTINCT session_id, feature
    FROM events
)
SELECT f.feature, AVG(s.length) AS avg_session_len
FROM feature_sessions f
JOIN session_lengths s ON s.session_id = f.session_id
GROUP BY f.feature
ORDER BY avg_session_len DESC;
```
**Explanation:** Session durations and feature membership are two distinct facts derived from the same log table via separate CTEs, then composed — reusing the base table twice cleanly.

## Q49: Write a helper CTE that assigns fiscal quarters to dates and enumerates them in order.

**Query:**
```sql
WITH fy_quarters AS (
    SELECT order_id,
           TO_CHAR(order_date, 'YYYY') || '-Q' ||
           CEIL(EXTRACT(MONTH FROM order_date) / 3.0) AS quarter_label,
           EXTRACT(YEAR FROM order_date) * 4 + CEIL(EXTRACT(MONTH FROM order_date) / 3.0) AS quarter_seq
    FROM orders
)
SELECT quarter_label, COUNT(*) AS orders
FROM fy_quarters
GROUP BY quarter_label, quarter_seq
ORDER BY quarter_seq;
```
**Explanation:** A pure-number secondary key (`quarter_seq`) keeps the label column human-readable while the sort stays correct across year boundaries.

## Q50: Write a Postgres UPDATE ... FROM that applies a stage-two price adjustment using a computed CTE.

**Query:**
```sql
-- Postgres
WITH sale_stats AS (
    SELECT product_id, AVG(unit_price) AS historical_avg
    FROM order_items
    GROUP BY product_id
)
UPDATE products p
SET list_price = ROUND(s.historical_avg * 1.05, 2),
    updated_at = CURRENT_TIMESTAMP
FROM sale_stats s
WHERE s.product_id = p.product_id
  AND p.list_price < s.historical_avg;
```
**Explanation:** The FROM + CTE supplies context to the UPDATE, letting a single statement reprice products based on their own sales history without a second query round-trip.

## Q51: Show the same analytic as both a session-scoped CTE and a temporary table, and say when each wins.

**Query:**
```sql
CREATE TEMP TABLE monthly_rev AS
SELECT DATE_TRUNC('month', order_date) AS month, SUM(total) AS revenue
FROM orders
GROUP BY 1;

SELECT month, revenue,
       revenue - LAG(revenue) OVER (ORDER BY month) AS mom_change
FROM monthly_rev;                                          -- first report

SELECT month, revenue FROM monthly_rev WHERE revenue > 100000;  -- second report
DROP TABLE monthly_rev;
```
**Explanation:** The temp table persists across statements, so two reports share one computation. A CTE can only serve one statement — use a temp table for real reuse, a CTE for one-shot pipelines.

**Alt1:** The CTE one-statement version:
```sql
WITH monthly_rev AS (
    SELECT DATE_TRUNC('month', order_date) AS month, SUM(total) AS revenue
    FROM orders GROUP BY 1
)
SELECT month, revenue FROM monthly_rev ORDER BY month;
```
**Explanation:** Same aggregation, single use; the mental tradeoff is lifecycle (statement vs session) and visibility (CTE is scoped and self-documenting; the temp table is shared state a colleague must remember to drop).

## Q52: Write a pageable query that returns the 21st–30th highest-value orders using a CTE and LIMIT/OFFSET.

**Query:**
```sql
WITH ranked_orders AS (
    SELECT order_id, total FROM orders
)
SELECT order_id, total
FROM ranked_orders
ORDER BY total DESC
OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;
```
**Explanation:** The CTE is a staging area between the raw table and the page-clipping rules; OFFSET/FETCH works on Postgres, Oracle, and SQL Server (MySQL uses `LIMIT 20, 10`).

**Alt1:** MySQL syntax and an Oracle ROWNUM naming twist:
```sql
-- MySQL
SELECT order_id, total FROM orders
ORDER BY total DESC
LIMIT 10 OFFSET 20;

-- Oracle 11g and earlier
SELECT * FROM (
    SELECT order_id, total FROM orders ORDER BY total DESC
) WHERE rownum <= 30
MINUS
SELECT * FROM (
    SELECT order_id, total FROM orders ORDER BY total DESC
) WHERE rownum <= 20;
```
**Explanation:** Page clipping differs by dialect; the takeaway for an interview is: ANSI OFFSET/FETCH is the modern portable spelling, and older Oracle needs the rownum trick.

## Q53: Write chained CTEs that compute month-over-month retention by joining users to their subsequent signups.

**Query:**
```sql
WITH cohort_months AS (
    SELECT user_id, DATE_TRUNC('month', signup_date) AS cohort
    FROM users
),
activity_months AS (
    SELECT user_id, DATE_TRUNC('month', activity_date) AS act_month
    FROM user_activity
    GROUP BY user_id, DATE_TRUNC('month', activity_date)
),
cohort_size AS (
    SELECT cohort, COUNT(*) AS size FROM cohort_months GROUP BY cohort
)
SELECT c.cohort, a.act_month,
       COUNT(DISTINCT a.user_id) AS active,
       ROUND(100.0 * COUNT(DISTINCT a.user_id) / cs.size, 1) AS retention_pct
FROM cohort_months c
LEFT JOIN activity_months a
  ON a.user_id = c.user_id AND a.act_month >= c.cohort
LEFT JOIN cohort_size cs ON cs.cohort = c.cohort
GROUP BY c.cohort, a.act_month, cs.size
ORDER BY c.cohort, a.act_month;
```
**Explanation:** Three CTEs encode the three facts — cohort membership, activity months, cohort size — and the chained joins answer retention without any window trick. Grandma's cohort table stays readable one stage at a time.

## Q54: Write chained CTEs that transform daily sales to weekly totals, then apply an average.

**Query:**
```sql
WITH daily AS (
    SELECT sale_date, SUM(amount) AS revenue
    FROM sales GROUP BY sale_date
),
weekly AS (
    SELECT DATE_TRUNC('week', sale_date) AS week, SUM(revenue) AS revenue
    FROM daily GROUP BY 1
)
SELECT week, revenue,
       revenue - AVG(revenue) OVER (ORDER BY week ROWS BETWEEN 3 PRECEDING AND CURRENT ROW) AS vs_4wk_avg
FROM weekly
ORDER BY week;
```
**Explanation:** Aggregation at a finer grain (day) rolls up into a coarser grain (week) via chained CTEs; the window call is the live comparison layer on top. MySQL uses `DATE_FORMAT(sale_date, '%X-%V')` for ISO weeks.

## Q55: Write a query that finds missing invoice numbers in 10000–10999 using a number-table CTE.

**Query:**
```sql
WITH all_nums AS (
    SELECT g AS n FROM generate_series(10000, 10999) g
),
issued AS (
    SELECT DISTINCT invoice_number FROM invoices
)
SELECT a.n AS missing_invoice
FROM all_nums a
LEFT JOIN issued i ON i.invoice_number = a.n
WHERE i.invoice_number IS NULL
ORDER BY a.n;
```
**Explanation:** The number spine guarantees the full range exists; the LEFT JOIN + NULL test exposes every gap. Gap analysis is a classic helper-dataset application.

**Alt1:** NOT IN spelling:
```sql
WITH all_nums AS (
    SELECT g AS n FROM generate_series(10000, 10999) g
)
SELECT n AS missing_invoice
FROM all_nums
WHERE n NOT IN (SELECT invoice_number FROM invoices WHERE invoice_number IS NOT NULL)
ORDER BY n;
```
**Explanation:** Equivalent output — this version relies on the subquery returning no NULLs, which is why the guard `WHERE invoice_number IS NOT NULL` matters.

## Q56: Write a CTE that averages teacher-given grades per student and lists students whose average is below the pass mark.

**Query:**
```sql
WITH grade_averages AS (
    SELECT student_id, AVG(grade) AS avg_grade
    FROM grades
    GROUP BY student_id
)
SELECT s.student_id, s.full_name, g.avg_grade
FROM students s
JOIN grade_averages g ON g.student_id = s.student_id
WHERE g.avg_grade < 60
ORDER BY g.avg_grade;
```
**Explanation:** The pass rule lives in the outer WHERE and the computation in the CTE — exactly the division of labour (calculate, then decide) a reviewer wants to see.

## Q57: Write CTEs for budget and actual spend, then join them into a variance report.

**Query:**
```sql
WITH budget AS (
    SELECT department, fiscal_month, SUM(budget_amount) AS budget_amt
    FROM budgets GROUP BY department, fiscal_month
),
actual AS (
    SELECT department, fiscal_month, SUM(spent) AS spent_amt
    FROM expenses GROUP BY department, fiscal_month
)
SELECT COALESCE(b.department, a.department) AS department,
       COALESCE(b.fiscal_month, a.fiscal_month) AS month,
       COALESCE(b.budget_amt, 0) AS budgeted,
       COALESCE(a.spent_amt, 0) AS spent,
       COALESCE(b.budget_amt, 0) - COALESCE(a.spent_amt, 0) AS variance
FROM budget b
FULL OUTER JOIN actual a
  ON a.department = b.department AND a.fiscal_month = b.fiscal_month
ORDER BY department, month;
```
**Explanation:** Each fact source gets its own CTE; the FULL OUTER JOIN keeps months where only one side has data, and COALESCE turns gaps into zeros. (MySQL 8 lacks FULL OUTER JOIN — swap in a LEFT/RIGHT UNION.)

## Q58: Write a CTE that detects probable duplicate bank transactions within a day and same amount.

**Query:**
```sql
WITH dup_candidates AS (
    SELECT amount, EXTRACT(DAY FROM tx_date) AS day_of_month,
           COUNT(*) AS occurrences
    FROM transactions
    GROUP BY amount, EXTRACT(DAY FROM tx_date)
    HAVING COUNT(*) > 1
)
SELECT t.*, d.occurrences
FROM transactions t
JOIN dup_candidates d
  ON d.amount = t.amount
 AND d.day_of_month = EXTRACT(DAY FROM t.tx_date);
```
**Explanation:** The CTE identifies the suspicious groups with HAVING, and the join pulls back every member row so a human can eyeball whether they are genuine double-posts.

## Q59: Write chained CTEs computing a campaign funnel across email-opened, link-clicked and purchased, with drop-off percentages.

**Query:**
```sql
WITH opened AS (
    SELECT COUNT(DISTINCT user_id) AS n FROM campaign_events WHERE event = 'open'
),
clicked AS (
    SELECT COUNT(DISTINCT user_id) AS n FROM campaign_events WHERE event = 'click'
),
purchased AS (
    SELECT COUNT(DISTINCT user_id) AS n FROM campaign_events WHERE event = 'purchase'
)
SELECT o.n AS opened, c.n AS clicked, p.n AS purchased,
       ROUND(100.0 * (o.n - c.n) / NULLIF(o.n, 0), 1) AS open_to_click_dropoff_pct,
       ROUND(100.0 * (c.n - p.n) / NULLIF(c.n, 0), 1) AS click_to_buy_dropoff_pct
FROM opened o, clicked c, purchased p;
```
**Explanation:** Each stage is a single-card CTE and the final SELECT is the funnel math itself — the classic "one CTE per metric" pipeline.

## Q60: Write a statement that computes daily totals in a CTE and then both groups further AND filters in the outer query.

**Query:**
```sql
WITH daily AS (
    SELECT order_date, SUM(total) AS revenue
    FROM orders GROUP BY order_date
)
SELECT EXTRACT(DOW FROM order_date) AS weekday, AVG(revenue) AS avg_revenue
FROM daily
WHERE revenue > 500
GROUP BY EXTRACT(DOW FROM order_date)
ORDER BY weekday;
```
**Explanation:** The row-level aggregation happens once in `daily`; the outer query decides what counts (filter) and how to regroup (weekday) — two concerns cleanly separated.

## Q61: Write a CTE that finds the highest salary per department, then list employees holding those salaries.

**Query:**
```sql
WITH dept_max AS (
    SELECT department, MAX(salary) AS max_salary
    FROM employees GROUP BY department
)
SELECT e.first_name, e.last_name, e.department, e.salary
FROM employees e
JOIN dept_max d ON d.department = e.department AND d.max_salary = e.salary
ORDER BY e.department;
```
**Explanation:** The peak is computed once per department; joining on both department and salary keeps every co-leader instead of only an arbitrary one.

**Alt1:** Corelated subquery alternative:
```sql
SELECT first_name, last_name, department, salary
FROM employees e
WHERE salary = (
    SELECT MAX(salary) FROM employees m WHERE m.department = e.department
);
```
**Explanation:** Same output; the correlated form repeats its aggregate per row (can be slower on big groups), while the CTE computes each department maximum once.

## Q62: Write a statement that uses a CTE in conjunction with EXISTS to find regions that had any sales last month.

**Query:**
```sql
WITH last_month AS (
    SELECT region
    FROM sales
    WHERE sale_date >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 month'
      AND sale_date <  DATE_TRUNC('month', CURRENT_DATE)
)
SELECT r.region_name
FROM regions r
WHERE EXISTS (SELECT 1 FROM last_month lm WHERE lm.region = r.region_id);
```
**Explanation:** The CTE computes the touching rows; EXISTS short-circuits and just needs "at least one match", which is honest about the question being asked.

## Q63: Write a Postgres CTE that snapshots hourly buckets for a 24-hour report, left-joined to pageviews.

**Query:**
```sql
WITH hours AS (
    SELECT g::time AS slot
    FROM generate_series('2024-09-04 00:00', '2024-09-04 23:00', INTERVAL '1 hour') AS g
)
SELECT hours.slot, COUNT(pv.id) AS views
FROM hours
LEFT JOIN pageviews pv ON DATE_TRUNC('hour', pv.viewed_at) = hours.slot
GROUP BY hours.slot
ORDER BY hours.slot;
```
**Explanation:** The spine is a full day of hourly slots; the join lands each view on its bucket and empty hours still appear with zero — a time-axis CTE that guarantees an unbroken x-axis.

**Alt1:** SQL Server with a numbers-built hour list:
```sql
-- SQL Server
WITH n AS (SELECT ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) - 1 AS n FROM sys.all_objects)
SELECT DATEADD(hour, n.n, CAST('2024-09-04' AS datetime)) AS slot, COUNT(pv.id) AS views
FROM n
LEFT JOIN pageviews pv ON CAST(pv.viewed_at AS date) = DATEADD(day, n.n / 24, CAST('2024-09-04' AS date))
                       AND DATEPART(hour, pv.viewed_at) = n.n % 24
WHERE n.n BETWEEN 0 AND 23
GROUP BY DATEADD(hour, n.n, CAST('2024-09-04' AS datetime));
```
**Explanation:** The number table reproduces the hour spine; the join key is decomposed to (day, hour) so the on-paper equals holds.

## Q64: Write a CTE report that shows each day plus a company-wide daily average alongside (grand totals via CTE + join).

**Query:**
```sql
WITH daily AS (
    SELECT order_date, SUM(total) AS revenue FROM orders GROUP BY order_date
),
overall AS (
    SELECT AVG(revenue) AS day_avg FROM daily
)
SELECT d.order_date, d.revenue, o.day_avg,
       ROUND(100.0 * d.revenue / o.day_avg, 1) AS pct_of_typical
FROM daily d
CROSS JOIN overall o
ORDER BY d.order_date;
```
**Explanation:** A scalar CTE carries the global benchmark and every day rows up against it — the "sparkline vs company average" pattern in three clean blocks.

## Q65: Write an INSERT that back-fills missing dates into a calendar table using a date-spine CTE.

**Query:**
```sql
WITH all_days AS (
    SELECT d::date AS day
    FROM generate_series('2024-01-01', '2024-12-31', INTERVAL '1 day') d
    WHERE d::date NOT IN (SELECT day FROM calendar)
)
INSERT INTO calendar (day)
SELECT day FROM all_days;
```
**Explanation:** Two facts — the full spine and what already exists — meet in one CTE, and the INSERT surfaces only the difference. Great demo of "CTE in FROM inside INSERT ... SELECT".

**Alt1:** LEFT JOIN anti-join instead of NOT IN:
```sql
INSERT INTO calendar (day)
SELECT d::date
FROM generate_series('2024-01-01', '2024-12-31', INTERVAL '1 day') d
LEFT JOIN calendar c ON c.day = d::date
WHERE c.day IS NULL;
```
**Explanation:** Identical result, NULL-safe; prefer the anti-join when the existing key column could ever hold NULL.

## Q66: Write a SQL Server UPDATE through a CTE that caps stock quantities at a configured maximum.

**Query:**
```sql
-- SQL Server
WITH caps AS (
    SELECT product_id, 200 AS max_qty FROM products WHERE category = 'perishable'
)
UPDATE p
SET stock_qty = CASE WHEN stock_qty > 200 THEN 200 ELSE stock_qty END
FROM products p
JOIN caps c ON c.product_id = p.product_id;
```
**Explanation:** The caps CTE marks the targets; SQL Server's UPDATE ... FROM applies the clamp. The rule reads top-down: "these products, cap them".

## Q67: Write a DELETE through a CTE + join in MySQL 8 style alternative and contrast with direct syntax.

**Query:**
```sql
-- MySQL 8 (derived-table join form)
DELETE p
FROM price_history p
JOIN (
    SELECT product_id
    FROM price_history
    GROUP BY product_id
    HAVING COUNT(*) < 3
) thin ON thin.product_id = p.product_id;
```
**Explanation:** MySQL's CTE-with-DELETE support is limited, so the derived table carries the "which rows" decision and a multi-table DELETE removes them.

**Alt1:** ANSI-friendly WHERE ... IN over a CTE (works in Postgres/SQL Server):
```sql
-- Postgres / SQL Server
WITH thin AS (
    SELECT product_id FROM price_history GROUP BY product_id HAVING COUNT(*) < 3
)
DELETE FROM price_history
WHERE product_id IN (SELECT product_id FROM thin);
```
**Explanation:** Clean and portable when the victim set is just a key list; the IN version cannot see row-level nuance, so keep it for set-based deletes.

## Q68: Refactor a monster WHERE clause into labelled CTEs without changing the result.

**Query:**
```sql
WITH eligible_age AS (
    SELECT * FROM applicants WHERE age BETWEEN 21 AND 60
),
has_income AS (
    SELECT * FROM eligible_age WHERE monthly_income >= 3000
),
no_criminal AS (
    SELECT a.*
    FROM has_income a
    WHERE NOT EXISTS (SELECT 1 FROM criminal_records cr WHERE cr.applicant_id = a.applicant_id)
)
SELECT * FROM no_criminal;
```
**Explanation:** Each acceptance rule becomes a chained named stage so a policy reviewer reads intent instead of reverse-engineering a 20-line AND-chain.

**Alt1:** The one-block equivalent everyone starts with:
```sql
SELECT *
FROM applicants a
WHERE age BETWEEN 21 AND 60
  AND monthly_income >= 3000
  AND NOT EXISTS (SELECT 1 FROM criminal_records cr WHERE cr.applicant_id = a.applicant_id);
```
**Explanation:** Functionally identical and fine at this size; the CTE cascade earns its keep when rules number into dozens or each stage grows subqueries.

## Q69: Write a CTE that flags suppliers below their minimum order quantity and alerts on reorder.

**Query:**
```sql
WITH min_qty AS (
    SELECT supplier_id, MIN(minimum_order_qty) AS floor
    FROM supplier_contracts GROUP BY supplier_id
),
below_floor AS (
    SELECT s.supplier_id, s.stock_qty, m.floor
    FROM suppliers s
    JOIN min_qty m ON m.supplier_id = s.supplier_id
    WHERE s.stock_qty < m.floor
)
SELECT supplier_id, stock_qty, floor, floor - stock_qty AS to_order
FROM below_floor
ORDER BY to_order DESC;
```
**Explanation:** Two chained CTEs (contract floor, then comparison) turn a three-way business relationship into an ordered shopping list.

## Q70: Write CTEs reporting email-campaign open rate and click rate segmented by segment.

**Query:**
```sql
WITH per_campaign AS (
    SELECT campaign_id, segment,
           COUNT(*) AS sent,
           COUNT(*) FILTER (WHERE opened_at IS NOT NULL) AS opened,
           COUNT(*) FILTER (WHERE clicked_at IS NOT NULL) AS clicked
    FROM campaign_recipients
    GROUP BY campaign_id, segment
)
SELECT campaign_id, segment, sent,
       ROUND(100.0 * opened  / NULLIF(sent, 0), 1) AS open_pct,
       ROUND(100.0 * clicked / NULLIF(sent, 0), 1) AS click_pct
FROM per_campaign
ORDER BY open_pct DESC, click_pct DESC;
```
**Explanation:** One CTE tallies the three event counts per slice (FILTER is Postgres; MySQL swaps in SUM(CASE WHEN ...)), one report statement consumes it — modular, testable metrics.

## Q71: Write a CTE that prepares first and last names split out of a single full_name column, then greets users by first name.

**Query:**
```sql
WITH split_names AS (
    SELECT user_id,
           SPLIT_PART(full_name, ' ', 1) AS first_name,
           SPLIT_PART(full_name, ' ', 2) AS last_name
    FROM users
)
SELECT user_id, first_name,
       CONCAT('Welcome back, ', first_name) AS greeting
FROM split_names;
```
**Explanation:** Every downstream piece reads only the clean columns; the parsing lives in one place. (MySQL uses SUBSTRING_INDEX; Oracle uses SUBSTR/INSTR.)

## Q72: Write a statement where a CTE value is compared inside a SELECT-list scalar subquery.

**Query:**
```sql
WITH max_salary AS (
    SELECT MAX(salary) AS top FROM employees
)
SELECT e.employee_id, e.salary,
       (SELECT top FROM max_salary) AS company_top,
       (SELECT top - e.salary FROM max_salary) AS gap_to_top
FROM employees e
ORDER BY e.salary DESC;
```
**Explanation:** The scalar `max_salary` CTE is pulled into the SELECT list through subqueries, so top and gap columns sit beside every row without repeating the MAX call.

## Q73: Write chained CTEs computing the average of the department averages (an average-of-averages).

**Query:**
```sql
WITH dept_avg AS (
    SELECT department, AVG(salary) AS avg_salary
    FROM employees GROUP BY department
)
SELECT ROUND(AVG(avg_salary), 2) AS mean_of_dept_means
FROM dept_avg;
```
**Explanation:** Averaging an already-aggregated CTE is only possible because the CTE materialized the group means; the outer AVG treats each department equally regardless of headcount.

## Q74: Write a CTE report that builds a full matrix of regions x product categories via CROSS JOIN of two helper sets.

**Query:**
```sql
WITH regions AS (
    SELECT DISTINCT region FROM sales
),
categories AS (
    SELECT DISTINCT category_id FROM sales
)
SELECT r.region, c.category_id,
       COUNT(s.sale_id) AS sales_count
FROM regions r
CROSS JOIN categories c
LEFT JOIN sales s
  ON s.region = r.region AND s.category_id = c.category_id
GROUP BY r.region, c.category_id
ORDER BY r.region, c.category_id;
```
**Explanation:** Two helper CTEs define the axes; a CROSS JOIN creates every cell and a LEFT JOIN fills those that have data — the classic zero-filled crosstab.

## Q75: Write CTEs that compute low-stock alerts by joining current stock to a safety-stock policy.

**Query:**
```sql
WITH policy AS (
    SELECT product_id, safety_stock FROM stock_policy WHERE active = true
),
stock AS (
    SELECT product_id, SUM(quantity_on_hand) AS total_qty
    FROM inventory_bins GROUP BY product_id
)
SELECT p.product_id, s.total_qty, p.safety_stock,
       p.safety_stock - s.total_qty AS shortfall
FROM policy p
JOIN stock s ON s.product_id = p.product_id
WHERE s.total_qty <= p.safety_stock
ORDER BY shortfall ASC;
```
**Explanation:** Procedural-looking logic (sum bins, compare to policy) becomes declarative: two facts joined under one business rule, output ready for an alert feed.

## Q76: Explain Postgres CTE materialization and write a query that forces the difference to matter.

**Query:**
```sql
WITH repeated AS (
    SELECT customer_id, COUNT(*) AS orders
    FROM orders WHERE status = 'shipped'
    GROUP BY customer_id
)
SELECT r.customer_id,
       r.orders,
       (SELECT COUNT(*) FROM repeated x WHERE x.customer_id = r.customer_id) AS sanity_check
FROM repeated r
LIMIT 100;
```
**Explanation:** `repeated` is referenced twice, so Postgres executes it once into an intermediate buffer; since it only reads plain tables it may be inlined on 12+, but this two-reference pattern is precisely when the planner prefers materializing.

**Alt1:** Forcing materialization when the CTE is referenced once but must not fuse:
```sql
WITH snapshot AS (
    SELECT * FROM orders WHERE status = 'shipped'
    OFFSET 0            -- Postgres: blocks inlining, guarantees materialization
)
UPDATE orders o
SET updated_at = CURRENT_TIMESTAMP
FROM snapshot s
WHERE o.order_id = s.order_id;
```
**Explanation:** A no-op `OFFSET 0` is the classic hint to force a one-shot CTE to be materialized (e.g. to snapshot a volatile table); it documents intent better than planner heroics.

## Q77: Write a CTE query that detects reversal pairs — a charge and its exact negative twin.

**Query:**
```sql
WITH amounts AS (
    SELECT tx_id, account_id, amount, EXTRACT(DAY FROM tx_date) AS day
    FROM ledger
)
SELECT a.tx_id AS charge_id, b.tx_id AS reversal_id, a.amount
FROM amounts a
JOIN amounts b
  ON b.account_id = a.account_id
 AND b.amount      = -a.amount
 AND b.day         = a.day
 AND a.tx_id < b.tx_id
WHERE a.amount > 0;
```
**Explanation:** One CTE aliased twice lets charge rows pair with their negative twins on (account, day) while `a.tx_id < b.tx_id` kills the duplicate ordering.

## Q78: Write chained CTEs that compute per-day active-user counts and then the 7-day trailing average core logic with a date spine.

**Query:**
```sql
WITH daily_active AS (
    SELECT DATE_TRUNC('day', activity_date) AS day, COUNT(DISTINCT user_id) AS dau
    FROM user_activity GROUP BY 1
),
spine AS (
    SELECT g::date AS day
    FROM generate_series('2024-06-01', '2024-06-30', INTERVAL '1 day') AS g
)
SELECT s.day, COALESCE(d.dau, 0) AS dau
FROM spine s
LEFT JOIN daily_active d ON d.day = s.day
ORDER BY s.day;
```
**Explanation:** Active-user math and the calendar are separate CTEs; the spine is what keeps the time axis unbroken for the chart that follows.

**Alt1:** Same shape with a window trailing average on top (alternative approach only — the window sibling file owns these):
```sql
WITH daily_active AS (
    SELECT DATE_TRUNC('day', activity_date) AS day, COUNT(DISTINCT user_id) AS dau
    FROM user_activity GROUP BY 1
)
SELECT day, dau,
       ROUND(AVG(dau) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 1) AS dau_7d
FROM daily_active ORDER BY day;
```
**Explanation:** Once the daily counts exist, the moving average is a one-line window; the spine remains unnecessary only if you do not need zero-filled days.

## Q79: Write a CTE that reports distinct customer counts per region and per country in one statement.

**Query:**
```sql
WITH region_counts AS (
    SELECT region, COUNT(DISTINCT customer_id) AS customers
    FROM customers GROUP BY region
),
country_counts AS (
    SELECT country, COUNT(DISTINCT customer_id) AS customers
    FROM customers GROUP BY country
)
SELECT 'region' AS level, region AS label, customers FROM region_counts
UNION ALL
SELECT 'country', country, customers FROM country_counts
ORDER BY level, label;
```
**Explanation:** Two CTEs compute two granularities; UNION ALL stitches them into a single report — the differ-by-dimension pattern, solved by keeping each dimension its own CTE.

## Q80: Write a CTE mini-pivot that produces one row per store with a column per year's revenue.

**Query:**
```sql
WITH yearly AS (
    SELECT store_id,
           EXTRACT(YEAR FROM sale_date) AS yr,
           SUM(amount) AS sales
    FROM sales GROUP BY store_id, EXTRACT(YEAR FROM sale_date)
)
SELECT store_id,
       SUM(CASE WHEN yr = 2023 THEN sales END) AS y2023,
       SUM(CASE WHEN yr = 2024 THEN sales END) AS y2024,
       SUM(CASE WHEN yr = 2025 THEN sales END) AS y2025
FROM yearly GROUP BY store_id
ORDER BY store_id;
```
**Explanation:** The CTE normalizes (store, year, sales); the outer query pivots by conditional aggregation — the readable, dialect-free pivot.

## Q81: Write a CTE that flags sequential gaps in shipping week numbers.

**Query:**
```sql
WITH weeks AS (
    SELECT DISTINCT g AS week_num
    FROM generate_series(1, 52) g
),
shipped AS (
    SELECT DISTINCT week_num FROM tracking WHERE week_num BETWEEN 1 AND 52
)
SELECT w.week_num AS missing_shipping_week
FROM weeks w
LEFT JOIN shipped s ON s.week_num = w.week_num
WHERE s.week_num IS NULL
ORDER BY w.week_num;
```
**Explanation:** The full year's weeks form the spine; anything the tracking table can't fill is genuinely missing — useful for supply-chain reporting where "no data" means "no shipments".

## Q82: Write a statement that reads the same source table once inside a CTE and derives several metrics from it.

**Query:**
```sql
WITH base_metrics AS (
    SELECT s.sale_id, s.region, s.amount,
           s.amount - AVG(s.amount) OVER (PARTITION BY s.region) AS diff_from_region,
           MAX(s.amount) OVER () AS global_max
    FROM sales s
)
SELECT region, COUNT(*) AS sales, MAX(diff_from_region) AS biggest_beat,
       MAX(global_max) AS top_sale_anywhere
FROM base_metrics GROUP BY region;
```
**Explanation:** Even though the window calls live here, the point is architectural: `sales` is scanned once and every downstream metric consumes `base_metrics` — the reuse pattern your interviewer wants you to articulate.

## Q83: Write CTEs that UNION consolidated data from several source tables into one reporting set.

**Query:**
```sql
WITH in_store AS (
    SELECT sale_id, 'store' AS channel, amount FROM store_sales
),
online AS (
    SELECT sale_id, 'online' AS channel, amount FROM ecommerce_sales
)
SELECT channel, SUM(amount) AS revenue, COUNT(*) AS orders
FROM (
    SELECT * FROM in_store
    UNION ALL
    SELECT * FROM online
) all_sales
GROUP BY channel;
```
**Explanation:** Two CTEs standardize different source schemas; a UNION ALL melts them together, and aggregation runs over the consolidated view — a pattern that also anchors ETL landing queries.

## Q84: Write a CTE membership-tier setup that classifies each customer using a range table.

**Query:**
```sql
WITH tiers AS (
    SELECT 'bronze' AS tier, 0 AS low, 999 AS high
    UNION ALL SELECT 'silver', 1000, 4999
    UNION ALL SELECT 'gold', 5000, NULL
)
SELECT c.customer_id, t.tier
FROM customers c
JOIN tiers t ON c.lifetime_value BETWEEN t.low AND COALESCE(t.high, c.lifetime_value)
ORDER BY c.customer_id;
```
**Explanation:** The tier boundaries are a stand-alone helper CTE; the join with range predicates classifies everyone, and gold's open-ended bucket is handled by COALESCE — all logic in one view.

**Alt1:** Merge boundaries into a plain subquery materialized the same way:
```sql
SELECT c.customer_id, t.tier
FROM customers c
JOIN (SELECT 'bronze' tier, 0 low, 999 high
      UNION ALL SELECT 'silver', 1000, 4999
      UNION ALL SELECT 'gold', 5000, NULL) t
  ON c.lifetime_value BETWEEN t.low AND COALESCE(t.high, c.lifetime_value);
```
**Explanation:** Identical output; only the location of the rule changes. Prefer the CTE when the tier list is long or will be referenced again in the same statement.

## Q85: Write chained CTEs computing revenue, cost of goods, gross margin, and margin rate.

**Query:**
```sql
WITH revenue AS (
    SELECT product_id, SUM(quantity * unit_price) AS rev
    FROM order_items GROUP BY product_id
),
cogs AS (
    SELECT product_id, SUM(quantity * unit_cost) AS cost
    FROM inventory_moves WHERE move_type = 'sold' GROUP BY product_id
),
margin AS (
    SELECT r.product_id, r.rev, c.cost, r.rev - c.cost AS gross_margin
    FROM revenue r LEFT JOIN cogs c ON c.product_id = r.product_id
)
SELECT product_id, rev, COALESCE(cost, 0) AS cost, gross_margin,
       ROUND(100.0 * gross_margin / NULLIF(rev, 0), 1) AS margin_pct
FROM margin ORDER BY margin_pct DESC;
```
**Explanation:** Four stages — each asks one financial question; the final SELECT adds the ratio. Chaining here mirrors the natural reading order of a P&L line.

## Q86: Write CTEs finding each user's best-selling month by revenue without window functions.

**Query:**
```sql
WITH user_month AS (
    SELECT user_id, DATE_TRUNC('month', sale_date) AS month, SUM(amount) AS m_rev
    FROM sales GROUP BY user_id, DATE_TRUNC('month', sale_date)
),
user_best AS (
    SELECT user_id, MAX(m_rev) AS best
    FROM user_month GROUP BY user_id
)
SELECT um.user_id, um.month, um.m_rev AS best_month_rev
FROM user_month um
JOIN user_best ub ON ub.user_id = um.user_id AND ub.best = um.m_rev;
```
**Explanation:** The MAX per user is computed in a second CTE, then raw months are joined back — preserving ties for the "argmax month" per user without ever calling a rank function.

## Q87: Write a CTE-based query that finds users active on at least three distinct days last week.

**Query:**
```sql
WITH last_week AS (
    SELECT DISTINCT user_id, DATE_TRUNC('day', activity_date) AS day
    FROM activity
    WHERE activity_date >= CURRENT_DATE - INTERVAL 7 DAY
)
SELECT user_id, COUNT(*) AS active_days
FROM last_week
GROUP BY user_id
HAVING COUNT(*) >= 3
ORDER BY active_days DESC;
```
**Explanation:** Dedup to (user, day) in the CTE first, then HAVING enforces the threshold — the "distinct-day" wording maps directly onto DISTINCT + HAVING.

## Q88: Write a statement that reads one stats CTE in two roles: full detail and company-wide compares.

**Query:**
```sql
WITH product_stats AS (
    SELECT product_id, SUM(amount) AS rev, AVG(amount) AS avg_sale
    FROM sales GROUP BY product_id
),
overall AS (
    SELECT AVG(avg_sale) AS company_avg_sale FROM product_stats
)
SELECT ps.product_id,
       ps.avg_sale,
       o.company_avg_sale,
       ps.avg_sale - o.company_avg_sale AS vs_company
FROM product_stats ps
CROSS JOIN overall o
ORDER BY vs_company DESC;
```
**Explanation:** `product_stats` is the workhorse CTE referenced both row-by-row and as input to `overall` — the two-references-worthy use case that justifies a CTE over a subquery.

## Q89: Write a non-recursive helper that produces a 0–99 sequence usable across dialects.

**Query:**
```sql
-- PostgreSQL
SELECT g AS n FROM generate_series(0, 99) g;
```
**Explanation:** One line in Postgres. The interview lesson: know your dialect's sequence source before reaching for recursion.

**Alt1:** Cross-dialect sequence sources:
```sql
-- SQL Server
SELECT ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) - 1 AS n
FROM sys.all_objects a CROSS JOIN sys.all_objects b;

-- MySQL 8
SELECT @row := @row + 1 AS n
FROM (SELECT @row := -1) r, information_schema.tables t
LIMIT 100;

-- Oracle
SELECT LEVEL - 1 AS n FROM dual CONNECT BY LEVEL <= 100;
```
**Explanation:** Each dialect has a terse generator — catalog rows (SQL Server), a session variable over the dictionary (MySQL), and Oracle's CONNECT BY LEVEL (a sibling file's recursion topic, used here purely as sequence). Knowing one per dialect beats misusing recursive CTEs for counts.

## Q90: Write CTEs that flag orders an unusual distance above the order-size norm using mean and standard deviation.

**Query:**
```sql
WITH stats AS (
    SELECT AVG(total) AS mean_total, STDDEV(total) AS sd_total
    FROM orders
),
deviant AS (
    SELECT o.order_id, o.total, s.mean_total, s.sd_total
    FROM orders o
    CROSS JOIN stats s
    WHERE o.total > s.mean_total + 2 * s.sd_total
)
SELECT order_id, total,
       ROUND((total - mean_total) / sd_total, 2) AS z_score
FROM deviant ORDER BY z_score DESC;
```
**Explanation:** Aggregate statistics materialize once in a CTE; the anomaly rule (mean + 2σ) reads like the business spec. STDDEV is portable enough (STDDEV in Postgres/Oracle, STDEV in SQL Server, STD in MySQL).

## Q91: Write the same "top product per category" as a temp table then as a CTE and contrast the lifecycle.

**Query:**
```sql
-- Postgres
CREATE TEMP TABLE cat_rank AS
SELECT category_id, product_id, SUM(amount) AS sales
FROM sales GROUP BY category_id, product_id;

SELECT * FROM cat_rank ORDER BY sales DESC;        -- statement A reuses it
SELECT category_id, COUNT(*) FROM cat_rank GROUP BY category_id;  -- statement B reuses it
DROP TABLE cat_rank;
```
**Explanation:** Two later statements reuse the aggregation — the textbook "no temp table would mean re-aggregating per statement" argument for session-persistent helpers.

**Alt1:** One-shot CTE twin:
```sql
WITH cat_rank AS (
    SELECT category_id, product_id, SUM(amount) AS sales
    FROM sales GROUP BY category_id, product_id
)
SELECT * FROM cat_rank ORDER BY sales DESC;
```
**Explanation:** Same computation, one statement of life. The interview tradeoff: CTE = self-contained/repeatable-as-needed, temp table = once-and-reuse but adds lifecycle hygiene (drop, permissions, drift).

## Q92: Write CTEs that produce a budget-approval matrix: department spends that exceed manager authority levels.

**Query:**
```sql
WITH authority AS (
    SELECT manager_id, dept, max_approval FROM mgr_limits
),
department_spend AS (
    SELECT dept, SUM(amount) AS total
    FROM purchase_requests WHERE status = 'pending' GROUP BY dept
)
SELECT a.manager_id, a.dept, d.total,
       CASE WHEN d.total > a.max_approval THEN 'ESCALATE' ELSE 'APPROVE' END AS action
FROM authority a
LEFT JOIN department_spend d ON d.dept = a.dept
ORDER BY a.manager_id;
```
**Explanation:** Two helper CTEs — the approval ceilings and the pending commitments — drive a pure CASE decision rule in the outer query: policy data in, workflow action out.

## Q93: Write a deduplicated staging-to-prod load where the CTE also sums duplicated rows before inserting.

**Query:**
```sql
WITH aggregated AS (
    SELECT sku, warehouse_id, SUM(qty) AS total_qty
    FROM staging_inventory
    GROUP BY sku, warehouse_id
)
INSERT INTO inventory (sku, warehouse_id, qty, loaded_at)
SELECT sku, warehouse_id, total_qty, CURRENT_TIMESTAMP
FROM aggregated;
```
**Explanation:** The CTE both collapses duplicate staging rows AND aggregates quantities, so the load is automatically normalized — no separate clean-up step and no data loss.

**Alt1:** Row-numbered variant keeping an explicit winner per (sku, warehouse):
```sql
INSERT INTO inventory (sku, warehouse_id, qty, loaded_at)
SELECT sku, warehouse_id, qty, CURRENT_TIMESTAMP
FROM (
    SELECT sku, warehouse_id, qty,
           ROW_NUMBER() OVER (PARTITION BY sku, warehouse_id ORDER BY updated_at DESC) rn
    FROM staging_inventory
) latest
WHERE rn = 1;
```
**Explanation:** Two philosophies: sum the duplicates (when counts must be merged) versus keep the latest (when edits overwrite). Each is the right call under a different business rule.

## Q94: Write chained CTEs that roll up sales team -> region -> national levels.

**Query:**
```sql
WITH team AS (
    SELECT rep_id, team, SUM(amount) AS team_rev FROM sales GROUP BY rep_id, team
),
region AS (
    SELECT team, region, SUM(team_rev) AS region_rev FROM team GROUP BY team, region
),
national AS (
    SELECT SUM(region_rev) AS total_rev FROM region
)
SELECT team, region, team_rev, region_rev, total_rev
FROM team t
JOIN region r ON r.team = t.team
CROSS JOIN national n
ORDER BY team, region;
```
**Explanation:** Three roll-up stages let one statement expose team, region and national totals together — each later stage feeding on the earlier one enough to keep the report's arithmetic auditable.

## Q95: Write a CTE that centralizes shipping-cost logic (fragile weight bands) and then recomputes order totals.

**Query:**
```sql
WITH shipping AS (
    SELECT order_id,
           CASE WHEN total_weight < 5   THEN 4.99
                WHEN total_weight < 20  THEN 9.99
                WHEN total_weight < 50  THEN 19.99
                ELSE 39.99 END AS shipping_fee
    FROM orders
)
SELECT o.order_id, o.total, s.shipping_fee,
       o.total + s.shipping_fee AS grand_total
FROM orders o
JOIN shipping s USING (order_id);
```
**Explanation:** The pricing bands are an isolated CASE in a CTE; accounting changes touch exactly one block, and any query joining `shipping` inherits the new rules automatically.

## Q96: Write a helper CTE that emits month names in chronological order for a report axis.

**Query:**
```sql
WITH months AS (
    SELECT g AS month_num
    FROM generate_series(1, 12) g
)
SELECT m.month_num,
       TO_CHAR(MAKE_DATE(2024, m.month_num, 1), 'Month') AS month_name,
       COUNT(o.order_id) AS orders
FROM months m
LEFT JOIN orders o ON EXTRACT(MONTH FROM o.order_date) = m.month_num
GROUP BY m.month_num
ORDER BY m.month_num;
```
**Explanation:** A twelve-row helper drives the axis; the join guarantees every month appears even with zero orders. (MAKE_DATE/TO_CHAR are Postgres; MySQL substitutes `MONTHNAME` after a date-builder.)

## Q97: Write CTEs that first prove duplicates by email with HAVING, then keep the senior record per email.

**Query:**
```sql
WITH dup_emails AS (
    SELECT email FROM users GROUP BY email HAVING COUNT(*) > 1
),
seniors AS (
    SELECT email, MIN(user_id) AS survivor_id
    FROM users WHERE email IN (SELECT email FROM dup_emails)
    GROUP BY email
)
SELECT u.*
FROM users u
JOIN seniors s ON s.survivor_id = u.user_id;
```
**Explanation:** Stage one proves the problem exists (HAVING), stage two selects who survives, and the outer join returns full rows — diagnostic thinking encoded in CTE names.

## Q98: Write CTEs comparing this period vs the previous period fully with joins.

**Query:**
```sql
WITH this_period AS (
    SELECT region, SUM(amount) AS rev
    FROM sales WHERE sale_date >= DATE '2024-07-01'
    GROUP BY region
),
prev_period AS (
    SELECT region, SUM(amount) AS rev
    FROM sales WHERE sale_date >= DATE '2024-04-01' AND sale_date < DATE '2024-07-01'
    GROUP BY region
)
SELECT COALESCE(t.region, p.region) AS region,
       COALESCE(p.rev, 0) AS prev_rev, COALESCE(t.rev, 0) AS this_rev,
       COALESCE(t.rev, 0) - COALESCE(p.rev, 0) AS change,
       CASE WHEN COALESCE(p.rev, 0) = 0 THEN NULL
            ELSE ROUND(100.0 * (COALESCE(t.rev,0) - COALESCE(p.rev,0)) / p.rev, 1)
       END AS change_pct
FROM this_period t
FULL OUTER JOIN prev_period p ON p.region = t.region
ORDER BY region;
```
**Explanation:** Two windowed CTEs (period definitions kept isolated), one FULL JOIN, and every NULL is turned into a real number — a calendar-period compare with no window function on the line.

## Q99: Write CTEs that split the workforce into full-time and part-time from raw timesheet hours.

**Query:**
```sql
WITH weekly_hours AS (
    SELECT employee_id, SUM(hours) AS hrs
    FROM timesheets
    WHERE week_date >= DATE_TRUNC('month', CURRENT_DATE)
    GROUP BY employee_id
),
classified AS (
    SELECT employee_id,
           CASE WHEN hrs >= 150 THEN 'full-time' ELSE 'part-time' END AS employment
    FROM weekly_hours
)
SELECT employment, COUNT(*) AS headcount
FROM classified
GROUP BY employment;
```
**Explanation:** Hours are totalled once, the rule is applied in a second CTE, and the headcount report reads cleanly — a three-stage split that captures the "compute, classify, report" staircase.

## Q100: Write the capstone: a full multi-CTE monthly revenue report pipeline — daily totals, monthly totals, best month, and share of best — in one readable statement.

**Query:**
```sql
WITH daily AS (
    SELECT sale_date, SUM(amount) AS day_rev FROM sales GROUP BY sale_date
),
monthly AS (
    SELECT DATE_TRUNC('month', sale_date) AS month, SUM(day_rev) AS month_rev
    FROM daily GROUP BY 1
),
best_month AS (
    SELECT MAX(month_rev) AS best FROM monthly
)
SELECT m.month,
       m.month_rev,
       b.best,
       ROUND(100.0 * m.month_rev / NULLIF(b.best, 0), 1) AS pct_of_best_month
FROM monthly m
CROSS JOIN best_month b
ORDER BY m.month;
```
**Explanation:** Daily -> monthly -> best-month scalar -> share — four CTEs that each stand alone, terminate in one tiny SELECT, and together answer four questions at once. This is the shape of a senior-level "build me a report" answer: named stages, zero repeated logic, everything inspectable.
