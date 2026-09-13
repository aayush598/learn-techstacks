# FAANG-Style Interview Round 1 — 100 SQL Q&A

## Q1: Write a query that returns every employee, highest salary first (tables: employees(id, name, dept_id, salary)).

**Query:**
```sql
-- MySQL 8+
SELECT id, name, dept_id, salary
FROM employees
ORDER BY salary DESC;
```

**Explanation:** Explicit column list plus a sorted scan; for large tables pair this with an index on (dept_id, salary) so the sort is served from the index.

**Alt1:**
```sql
-- MySQL 8+
SELECT id, name, dept_id, salary
FROM employees
ORDER BY 4 DESC;
```

Ordering by ordinal is equivalent but breaks if column order changes; name columns explicitly in shared code.

## Q2: Write a query to list all customers who have never placed an order (tables: customers(id, name), orders(id, customer_id)).

**Query:**
```sql
-- MySQL 8+
SELECT c.id, c.name
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.id IS NULL;
```

**Explanation:** Anti-join via LEFT JOIN + IS NULL; this is the FAANG-grade answer because it lets the optimizer hash-join on customer_id instead of rescanning per row.

**Alt1:**
```sql
-- PostgreSQL
SELECT id, name
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```

NOT EXISTS is the same anti-join but short-circuits on the first hit, which can beat the join when the hot customer set is small.

## Q3: How many orders has each customer placed? Ordered by most orders first (tables: customers(id, name), orders(id, customer_id)).

**Query:**
```sql
-- MySQL 8+
SELECT c.id, c.name, COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.id, c.name
ORDER BY order_count DESC;
```

**Explanation:** LEFT JOIN preserves customers with zero orders; GROUP BY on the customer key (not o.customer_id) keeps non-aggregated columns valid.

**Alt1:**
```sql
-- PostgreSQL
SELECT c.id, c.name,
       (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) AS order_count
FROM customers c
ORDER BY 3 DESC;
```

Correlated scalar subquery gives the same result and can be cheaper when there is an index on orders(customer_id).

## Q4: What is the average salary per department? Show the department name (tables: employees(id, name, dept_id, salary), departments(id, name)).

**Query:**
```sql
-- MySQL 8+
SELECT d.name, ROUND(AVG(e.salary), 2) AS avg_salary
FROM employees e
JOIN departments d ON d.id = e.dept_id
GROUP BY d.id, d.name
ORDER BY avg_salary DESC;
```

**Explanation:** Grouping by d.name alone is enough in MySQL but grouping by the key d.id too is the portable FAANG-grade habit that survives every dialect.

**Alt1:**
```sql
-- PostgreSQL
SELECT d.name,
       ROUND(AVG(salary) OVER (PARTITION BY e.dept_id), 2) AS avg_salary
FROM employees e JOIN departments d ON d.id = e.dept_id;
```

Window AVG returns the average on every row rather than one row per department; use it when downstream rows still need the per-row salary.

## Q5: Write a query to return the second highest salary in the entire company (tables: employees(id, name, salary)).

**Query:**
```sql
-- MySQL 8+
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```

**Explanation:** MAX under the global MAX is the classic two-pass answer; it avoids the DISTINCT-then-skip cost and is immune to ties at the top.

**Alt1:**
```sql
-- PostgreSQL
SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 1;
```

ORDER BY + OFFSET is the most readable answer on Postgres/MySQL, but on MySQL it needs the DISTINCT or tied top salaries collapse into one row.

## Q6: Which employees earn more than their own manager? (tables: employees(id, name, manager_id, salary)).

**Query:**
```sql
-- MySQL 8+
SELECT e.name AS employee, e.salary, m.name AS manager, m.salary AS mgr_salary
FROM employees e
JOIN employees m ON m.id = e.manager_id
WHERE e.salary > m.salary;
```

**Explanation:** A self-join turns the manager relationship into a row, then a simple filter; the JOIN (not LEFT JOIN) drops the CEO who has no manager row.

**Alt1:**
```sql
-- MySQL 8+
SELECT e.name
FROM employees e
WHERE e.salary > (SELECT salary FROM employees m WHERE m.id = e.manager_id);
```

The correlated subquery is the same logic without materializing the join, and is easier to read when the manager columns are not needed in the output.

## Q7: Write a query to find all duplicate email addresses (tables: users(id, email)).

**Query:**
```sql
-- MySQL 8+
SELECT email, COUNT(*) AS duplicates
FROM users
GROUP BY email
HAVING COUNT(*) > 1;
```

**Explanation:** GROUP BY + HAVING is the canonical duplicate detector; using COUNT(*) > 1 keeps each duplicated email once, not per-row.

**Alt1:**
```sql
-- SQL Server
SELECT DISTINCT email
FROM (
  SELECT email,
         COUNT(*) OVER (PARTITION BY email) AS cnt
  FROM users
) t
WHERE cnt > 1;
```

The windowed COUNT partitions without collapsing rows, which matters when you must later inspect individual duplicate rows.

## Q8: List employees hired within the last 12 months (tables: employees(id, name, hire_date)).

**Query:**
```sql
-- MySQL 8+
SELECT id, name, hire_date
FROM employees
WHERE hire_date >= CURRENT_DATE - INTERVAL 12 MONTH;
```

**Explanation:** The predicate on hire_date is sargable, so an index on hire_date serves the range scan; applying functions to hire_date would disable that index.

**Alt1:**
```sql
-- PostgreSQL
SELECT id, name, hire_date
FROM employees
WHERE hire_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE;
```

BETWEEN is the Postgres-friendly equivalent and reads like the requirement; both keep hire_date bare so indexes still apply.

## Q9: Which products cost more than the average price of all products? (tables: products(id, name, price)).

**Query:**
```sql
-- MySQL 8+
SELECT id, name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);
```

**Explanation:** The scalar subquery computes the average once; a bare WHERE with the average inline would be illegal SQL, which is the trap this question is designed to catch.

**Alt1:**
```sql
-- PostgreSQL
SELECT p.id, p.name, p.price
FROM products p
JOIN (SELECT AVG(price) AS avg_price FROM products) a ON TRUE
WHERE p.price > a.avg_price;
```

Materializing the average as a derived table makes the comparison explicit and lets you reuse it for multiple filters in one query.

## Q10: Count how many orders were placed in the last 30 days, grouped per product (tables: orders(id, product_id, order_date)).

**Query:**
```sql
-- MySQL 8+
SELECT product_id, COUNT(*) AS orders_last_30d
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL 30 DAY
GROUP BY product_id;
```

**Explanation:** The date filter runs before grouping, shrinking the aggregation input; keep order_date bare so the index on product_id + order_date is usable.

**Alt1:**
```sql
-- PostgreSQL
SELECT product_id, COUNT(*) FILTER (WHERE order_date >= CURRENT_DATE - INTERVAL '30 days')
FROM orders
GROUP BY product_id;
```

FILTER inside COUNT keeps all products in the result (even zero-order ones) while counting only recent rows; an anti-pattern lesson in itself.

## Q11: Write a query listing the top 3 salaried employees per department; ties must all be shown (tables: employees(id, name, dept_id, salary)).

**Query:**
```sql
-- MySQL 8+
SELECT name, dept_id, salary
FROM (
  SELECT name, dept_id, salary,
         DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
) t
WHERE rnk <= 3
ORDER BY dept_id, salary DESC;
```

**Explanation:** DENSE_RANK gives tied salaries the same rank, so every tie inside the top 3 bands survives; this is the FAANG-canonical top-N-with-ties answer.

**Alt1:**
```sql
-- MySQL 8+
SELECT e.name, e.dept_id, e.salary
FROM employees e
WHERE (SELECT COUNT(DISTINCT e2.salary) FROM employees e2
       WHERE e2.dept_id = e.dept_id AND e2.salary >= e.salary) <= 3
ORDER BY e.dept_id, e.salary DESC;
```

The correlated COUNT DISTINCT of strictly-higher salaries is the join-based equivalent and the only clean approach on MySQL 5.x without windows.

## Q12: Show employees whose salary is above their own department's average (tables: employees(id, name, dept_id, salary)).

**Query:**
```sql
-- MySQL 8+
SELECT id, name, dept_id, salary
FROM employees e
WHERE salary > (SELECT AVG(salary) FROM employees e2 WHERE e2.dept_id = e.dept_id);
```

**Explanation:** The correlated subquery recomputes the department average per row, which is correct on small tables and is the classic non-window answer.

**Alt1:**
```sql
-- MySQL 8+
SELECT e.id, e.name, e.dept_id, e.salary
FROM employees e
JOIN (SELECT dept_id, AVG(salary) AS avg_sal
      FROM employees GROUP BY dept_id) a ON a.dept_id = e.dept_id
WHERE e.salary > a.avg_sal;
```

Joining to a pre-aggregated dept average computes each average exactly once - the better plan when the company has many employees.

## Q13: Return the 5 most recent orders for each customer (tables: orders(id, customer_id, order_date)).

**Query:**
```sql
-- MySQL 8+
SELECT customer_id, id, order_date
FROM (
  SELECT id, customer_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, id DESC) AS rn
  FROM orders
) t
WHERE rn <= 5;
```

**Explanation:** ROW_NUMBER partitions per customer and orders within the window; adding id as tiebreaker makes the ranking deterministic, which interviews check for.

**Alt1:**
```sql
-- MySQL 8+
SELECT o.customer_id, o.id, o.order_date
FROM orders o
WHERE (SELECT COUNT(*) FROM orders o2
       WHERE o2.customer_id = o.customer_id
         AND (o2.order_date > o.order_date
           OR (o2.order_date = o.order_date AND o2.id > o.id))) < 5;
```

The correlated count of rows that rank above the current one is the derived-table/join alternative that works without window functions.

## Q14: Compute total sales amount per region, showing only regions with sales (tables: sales(id, region, amount)).

**Query:**
```sql
-- MySQL 8+
SELECT region, SUM(amount) AS total_sales
FROM sales
GROUP BY region
ORDER BY total_sales DESC;
```

**Explanation:** GROUP BY collapses each region from rows to one aggregate; an index on (region, amount) lets MySQL run this as a loose index scan.

**Alt1:**
```sql
-- PostgreSQL
SELECT DISTINCT region,
       SUM(amount) OVER (PARTITION BY region) AS total_sales
FROM sales
ORDER BY 2 DESC;
```

The window version keeps the raw rows around while attaching each region's total, useful when the detail rows are needed in the same result.

## Q15: How many orders were placed each month across all time? (tables: orders(id, order_date)).

**Query:**
```sql
-- MySQL 8+
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
       COUNT(*) AS orders
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;
```

**Explanation:** Truncating to month is done once per group; casting order_date instead of the group key keeps the month label clean and the ordering chronological.

**Alt1:**
```sql
-- PostgreSQL
SELECT to_char(order_date, 'YYYY-MM') AS month,
       COUNT(*) AS orders
FROM orders
GROUP BY 1
ORDER BY 1;
```

Postgres uses to_char for the same truncation, and grouping by the ordinal 1 avoids re-typing the expression - equivalent, but beware expression duplication in HAVING.

## Q16: Return the 4th highest distinct salary from the company (tables: employees(id, name, salary)).

**Query:**
```sql
-- MySQL 8+
SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 3;
```

**Explanation:** DISTINCT collapses ties so OFFSET counts *distinct* salary bands, and LIMIT+OFFSET turns it into a paged read; on MySQL 8 this is the whole answer.

**Alt1:**
```sql
-- SQL Server
SELECT TOP 1 salary
FROM (
  SELECT DISTINCT salary,
         ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn
  FROM employees
) t
WHERE rn = 4;
```

ROW_NUMBER ON DISTINCT salary is the SQL Server/Oracle portable variant when OFFSET/FETCH syntax differs.

## Q17: Which customers have placed more than 5 orders? (tables: customers(id, name), orders(id, customer_id)).

**Query:**
```sql
-- MySQL 8+
SELECT c.id, c.name, COUNT(o.id) AS order_count
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.id, c.name
HAVING COUNT(o.id) > 5;
```

**Explanation:** JOIN + HAVING filters after aggregation; HAVING on the aggregate count is the only place a COUNT comparison is legal.

**Alt1:**
```sql
-- MySQL 8+
SELECT id, name
FROM customers c
WHERE (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) > 5;
```

The correlated scalar count avoids building the full join when an index on orders(customer_id) exists, and skips GROUP BY entirely.

## Q18: Find all salary values shared by two or more employees (tables: employees(id, name, salary)).

**Query:**
```sql
-- MySQL 8+
SELECT salary, COUNT(*) AS employees
FROM employees
GROUP BY salary
HAVING COUNT(*) >= 2;
```

**Explanation:** GROUP BY salary surfaces shared values only after HAVING filters groups; count of rows, not distinct names, since (id, name) is unique.

**Alt1:**
```sql
-- PostgreSQL
SELECT DISTINCT salary
FROM (
  SELECT salary, COUNT(*) OVER (PARTITION BY salary) AS cnt
  FROM employees
) t
WHERE cnt >= 2;
```

The window COUNT keeps every row visible, which is the variant to use when audit rows - not just the salary - must be listed.

## Q19: List movies released after 2010 along with how many lead actors star in each (tables: movies(id, title, release_year), leads(movie_id, actor_name)).

**Query:**
```sql
-- MySQL 8+
SELECT m.title, m.release_year, COUNT(l.actor_name) AS lead_count
FROM movies m
LEFT JOIN leads l ON l.movie_id = m.id
WHERE m.release_year > 2010
GROUP BY m.id, m.title, m.release_year;
```

**Explanation:** LEFT JOIN keeps movies with zero listed leads; the WHERE on release_year runs before grouping so only recent movies are joined.

**Alt1:**
```sql
-- PostgreSQL
SELECT m.title, m.release_year,
       (SELECT COUNT(*) FROM leads l WHERE l.movie_id = m.id) AS lead_count
FROM movies m
WHERE m.release_year > 2010;
```

The correlated subquery is the clean read-aloud version when movies are few and leads are indexed by movie_id.

## Q20: List books that have more than 100 pages, alphabetically by title (tables: books(id, title, pages)).

**Query:**
```sql
-- MySQL 8+
SELECT id, title, pages
FROM books
WHERE pages > 100
ORDER BY title;
```

**Explanation:** A range predicate + a sort key; both are served by a covering index on (pages, title) so the DB never touches the table.

**Alt1:**
```sql
-- PostgreSQL
SELECT id, title, pages
FROM books
WHERE pages BETWEEN 101 AND 99999
ORDER BY title COLLATE "C";
```

BETWEEN is the explicit range form, and forcing a C collation on ORDER BY is the trick interviewers want for deterministically ASCII-sorted output.

## Q21: Which 2 products have sold the most units? (tables: products(id, name), order_items(id, product_id, qty)).

**Query:**
```sql
-- MySQL 8+
SELECT p.id, p.name, SUM(oi.qty) AS units_sold
FROM order_items oi
JOIN products p ON p.id = oi.product_id
GROUP BY p.id, p.name
ORDER BY units_sold DESC
LIMIT 2;
```

**Explanation:** Aggregating units per product then ORDER BY + LIMIT 2 is the top-K pattern; do the aggregate first, never ORDER BY a raw column that should be summed.

**Alt1:**
```sql
-- MySQL 8+
SELECT id, name, units_sold
FROM (
  SELECT p.id, p.name, SUM(oi.qty) AS units_sold,
         RANK() OVER (ORDER BY SUM(oi.qty) DESC) AS rnk
  FROM order_items oi JOIN products p ON p.id = oi.product_id
  GROUP BY p.id, p.name
) t
WHERE rnk <= 2;
```

RANK keeps the top 2 *ranks*, including every product tied for second - use it when a tie for the last slot should promote all, unlike LIMIT which truncates.

## Q22: List every employee next to their manager's name (tables: employees(id, name, manager_id)).

**Query:**
```sql
-- MySQL 8+
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON m.id = e.manager_id;
```

**Explanation:** LEFT JOIN keeps the CEO who has a NULL manager_id; JOIN would silently drop that row, which is the distinction this question exists to test.

**Alt1:**
```sql
-- MySQL 8+
SELECT name,
       (SELECT name FROM employees m WHERE m.id = e.manager_id) AS manager
FROM employees e;
```

The scalar subquery prints the manager name without a join and is how you'd phrase the intent when the self-join feels heavy.

## Q23: How many distinct users logged in during each month? (tables: logins(user_id, login_date)).

**Query:**
```sql
-- MySQL 8+
SELECT DATE_FORMAT(login_date, '%Y-%m') AS month,
       COUNT(DISTINCT user_id) AS active_users
FROM logins
GROUP BY DATE_FORMAT(login_date, '%Y-%m')
ORDER BY month;
```

**Explanation:** COUNT(DISTINCT user_id) dedupes the repeated daily logins inside the month; the case for splitting month from year before aggregating is exactly this.

**Alt1:**
```sql
-- PostgreSQL
SELECT DATE_TRUNC('month', login_date) AS month,
       COUNT(DISTINCT user_id) AS active_users
FROM logins
GROUP BY 1
ORDER BY 1;
```

DATE_TRUNC keeps a real date instead of a string, so any downstream month arithmetic (next month, joins) stays type-safe.

## Q24: Rank employees within each department by salary, and show the ranking numbers including the gaps caused by ties (tables: employees(id, name, dept_id, salary)).

**Query:**
```sql
-- MySQL 8+
SELECT name, dept_id, salary,
       RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
FROM employees
ORDER BY dept_id, rnk;
```

**Explanation:** RANK skips a number after ties (1,2,2,4), while DENSE_RANK would not (1,2,2,3); the question's "gaps" wording tells you RANK is the required function.

**Alt1:**
```sql
-- SQL Server
SELECT name, dept_id, salary,
       DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dense_rnk,
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, id) AS seq
FROM employees
ORDER BY dept_id;
```

Showing all three ranking functions side by side is the interview-grade answer when the interviewer probes the difference between RANK, DENSE_RANK and ROW_NUMBER.

## Q25: Delete duplicate emails from users, keeping only the row with the smallest id (tables: users(id, email)).

**Query:**
```sql
-- MySQL 8+
DELETE u1 FROM users u1
JOIN users u2
  ON u1.email = u2.email
 AND u1.id > u2.id;
```

**Explanation:** The self-join matches every duplicate with its lower-id sibling and deletes the higher side, so the minimum id of each email survives untouched.

**Alt1:**
```sql
-- PostgreSQL
WITH ranked AS (
  SELECT id,
         ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS rn
  FROM users
)
DELETE FROM users u
USING ranked r
WHERE u.id = r.id AND r.rn > 1;
```

Postgres authors deletions through a CTE + USING: ROW_NUMBER keeps the first row per email, and the DELETE fires only on rn > 1.

## Q26: Flag attendance gaps: for each login mark whether the user skipped a day versus their previous login (tables: attendance(user_id, login_date)).

**Query:**
```sql
-- PostgreSQL
SELECT user_id, login_date,
       LAG(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS prev_date,
       CASE WHEN LAG(login_date) OVER (PARTITION BY user_id ORDER BY login_date)
                 = login_date - 1 THEN 0 ELSE 1 END AS gap_flag
FROM attendance
ORDER BY user_id, login_date;
```

**Explanation:** LAG reports the prior login and a single subtraction detects skipped days; this is the standard gaps-primer that later feeds gaps-and-islands grouping.

**Alt1:**
```sql
-- MySQL 8+
SELECT a.user_id, a.login_date,
       a.login_date - INTERVAL 1 DAY AS expected_prev,
       CASE WHEN b.login_date IS NULL THEN 1 ELSE 0 END AS gap_flag
FROM attendance a
LEFT JOIN attendance b
  ON b.user_id = a.user_id
 AND b.login_date = a.login_date - INTERVAL 1 DAY
ORDER BY a.user_id, a.login_date;
```

A self-LOOKUP of yesterday's row replaces LAG and highlights the extra joins a pre-window solution would need.

## Q27: Find customers who ordered in the past but have not ordered in the last 30 days (tables: customers(id, name), orders(id, customer_id, order_date)).

**Query:**
```sql
-- MySQL 8+
SELECT c.id, c.name
FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id)
  AND NOT EXISTS (SELECT 1 FROM orders o
                  WHERE o.customer_id = c.id
                    AND o.order_date >= CURRENT_DATE - INTERVAL 30 DAY);
```

**Explanation:** Two EXISTS anti/semi-joins express "ever ordered" AND "not recently"; short-circuit semantics only scan orders until a match or proof-of-none is found.

**Alt1:**
```sql
-- PostgreSQL
SELECT c.id, c.name
FROM customers c
JOIN (
  SELECT customer_id, MAX(order_date) AS last_order
  FROM orders GROUP BY customer_id
) m ON m.customer_id = c.id
WHERE m.last_order < CURRENT_DATE - INTERVAL '30 days';
```

The derived MAX(order_date) per customer computes each customer's recency once and is the classic GROUP BY alternative to nested EXISTS.

## Q28: Give the second-highest salary in each department (tables: employees(id, name, dept_id, salary)).

**Query:**
```sql
-- MySQL 8+
SELECT name, dept_id, salary
FROM (
  SELECT name, dept_id, salary,
         DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
) t
WHERE rnk = 2;
```

**Explanation:** DENSE_RANK collapses ties so bands are 1,2,3 and "second-highest" means the second distinct value - the intended reading for top-N-per-group.

**Alt1:**
```sql
-- MySQL 8+
SELECT e.name, e.dept_id, e.salary
FROM employees e
WHERE e.salary = (
  SELECT MAX(salary) FROM employees e2
  WHERE e2.dept_id = e.dept_id AND e2.salary < (
    SELECT MAX(salary) FROM employees e3 WHERE e3.dept_id = e.dept_id
  )
);
```

The correlated double-MAX is the no-window classic: find the max, then the max strictly below it, per department.

## Q29: Find all managers who have at least 5 direct reports, with their name (tables: employees(id, name, manager_id)).

**Query:**
```sql
-- MySQL 8+
SELECT m.id, m.name, COUNT(e.id) AS report_count
FROM employees e
JOIN employees m ON m.id = e.manager_id
GROUP BY m.id, m.name
HAVING COUNT(e.id) >= 5;
```

**Explanation:** The self-join flattens manager->report, GROUP BY + HAVING keeps only managers crossing the threshold, and COUNT(e.id) never counts the NULL CEO row.

**Alt1:**
```sql
-- SQL Server
SELECT name
FROM employees
WHERE id IN (
  SELECT manager_id FROM employees
  GROUP BY manager_id HAVING COUNT(*) >= 5
);
```

Aggregating only the ids (HAVING) then IN-lookup of names avoids the join entirely - fewer rows flow when report sets are big.

## Q30: Total revenue contributed by each customer in the last 30 days (tables: customers(id, name), orders(id, customer_id, order_date), order_items(order_id, product_id, qty, price)).

**Query:**
```sql
-- MySQL 8+
SELECT c.id, c.name, SUM(oi.qty * oi.price) AS revenue_30d
FROM customers c
JOIN orders o ON o.customer_id = c.id
              AND o.order_date >= CURRENT_DATE - INTERVAL 30 DAY
JOIN order_items oi ON oi.order_id = o.id
GROUP BY c.id, c.name
ORDER BY revenue_30d DESC;
```

**Explanation:** Two joins multiply order quantities by their unit price, and pushing the date filter into the JOIN condition shrinks the pipeline before aggregation.

**Alt1:**
```sql
-- PostgreSQL
SELECT c.id, c.name,
       (SELECT SUM(oi.qty * oi.price)
        FROM orders o JOIN order_items oi ON oi.order_id = o.id
        WHERE o.customer_id = c.id
          AND o.order_date >= CURRENT_DATE - INTERVAL '30 days') AS revenue_30d
FROM customers c
ORDER BY 3 DESC;
```

The dependent scalar sum keeps customers without recent orders in the list (NULL/zero), which the INNER JOIN version suppresses.

## Q31: What is the average order value per month? (tables: orders(id, customer_id, amount, order_date)).

**Query:**
```sql
-- MySQL 8+
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
       ROUND(AVG(amount), 2) AS avg_order_value
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;
```

**Explanation:** AVG over amount per month-bucket is AOV; ROUND keeps analytics output clean, and alignment of GROUP BY to SELECT avoids expression drift.

**Alt1:**
```sql
-- PostgreSQL
SELECT to_char(order_date, 'YYYY-MM') AS month,
       ROUND(SUM(amount) * 1.0 / COUNT(*), 2) AS avg_order_value
FROM orders
GROUP BY 1
ORDER BY 1;
```

Writing AOV explicitly as SUM/COUNT makes the definition self-documenting and avoids any misunderstanding about what AVG did.

## Q32: Find players who logged in on two consecutive days at some point (tables: logins(user_id, login_date)).

**Query:**
```sql
-- PostgreSQL
WITH lg AS (
  SELECT user_id, login_date,
         LAG(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS prev_date
  FROM logins
)
SELECT DISTINCT user_id
FROM lg
WHERE login_date - prev_date = 1;
```

**Explanation:** LAG computes each day's predecessor and a one-day difference isolates consecutive pairs; DISTINCT collapses a user with several streaks into one hit.

**Alt1:**
```sql
-- MySQL 8+
SELECT DISTINCT a.user_id
FROM logins a
JOIN logins b
  ON a.user_id = b.user_id
 AND b.login_date = a.login_date + INTERVAL 1 DAY;
```

The self-join to the calendar-successor is the pre-window equivalent and reads almost literally like the requirement.

## Q33: For each department, list employees who earn the department's maximum salary (all ties included) (tables: employees(id, name, dept_id, salary)).

**Query:**
```sql
-- MySQL 8+
SELECT dept_id, name, salary
FROM (
  SELECT dept_id, name, salary,
         DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
) t
WHERE rnk = 1;
```

**Explanation:** DENSE_RANK = 1 keeps every co-max earner, which is the LeetCode 184 requirement; alternatives that take top-1 drop valid ties.

**Alt1:**
```sql
-- MySQL 8+
SELECT dept_id, name, salary
FROM employees
WHERE (dept_id, salary) IN (
  SELECT dept_id, MAX(salary) FROM employees GROUP BY dept_id
);
```

The row-constructor IN compares against a grouped max set - a completely self-contained and window-free answer on MySQL.

## Q34: A log table has no primary key; find the rows that are exact duplicates (tables: t_log(ts, user_id, action)).

**Query:**
```sql
-- MySQL 8+
SELECT ts, user_id, action, COUNT(*) AS dup_count
FROM t_log
GROUP BY ts, user_id, action
HAVING COUNT(*) > 1;
```

**Explanation:** Grouping by every column surface the repeated events; HAVING > 1 keeps only duplicated rows, and COUNT(*) doubles as the duplicate count.

**Alt1:**
```sql
-- PostgreSQL
SELECT ts, user_id, action, n
FROM (
  SELECT ts, user_id, action,
         COUNT(*) OVER (PARTITION BY ts, user_id, action) AS n
  FROM t_log
) t
WHERE n > 1;
```

The windowed COUNT annotates *every* duplicate row instead of collapsing them, so the raw duplicated events remain addressable for cleanup.

## Q35: Rank salaries per department two ways - with and without gaps for ties - side by side (tables: employees(id, name, dept_id, salary)).

**Query:**
```sql
-- SQL Server
SELECT name, dept_id, salary,
       RANK()       OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rank_with_gaps,
       DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dense_rank
FROM employees
ORDER BY dept_id, salary DESC;
```

**Explanation:** Payroll needs RANK (1,2,2,4) for precise position, dashboards want DENSE_RANK (1,2,2,3) for compact bands; showing both in one result is the click moment.

**Alt1:**
```sql
-- MySQL 8+
SELECT name, dept_id, salary,
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, id) AS seq
FROM employees;
```

ROW_NUMBER breaks every tie with the id tiebreaker - no gaps, no shared ranks - which is what materialized "position number" use-cases demand.

## Q36: What is the average runtime of movies in each genre? (tables: movies(id, title, runtime), genres(id, name), movie_genre(movie_id, genre_id)).

**Query:**
```sql
-- MySQL 8+
SELECT g.name AS genre, ROUND(AVG(m.runtime), 1) AS avg_runtime
FROM movies m
JOIN movie_genre mg ON mg.movie_id = m.id
JOIN genres g ON g.id = mg.genre_id
GROUP BY g.id, g.name
ORDER BY avg_runtime DESC;
```

**Explanation:** A many-to-many chain joins through the junction table; grouping by the genre key (not name only) is safe across all dialects.

**Alt1:**
```sql
-- PostgreSQL
SELECT g.name,
       ROUND(AVG(m.runtime) FILTER (WHERE m.runtime IS NOT NULL), 1) AS avg_runtime
FROM genres g
LEFT JOIN movie_genre mg ON mg.genre_id = g.id
LEFT JOIN movies m ON m.id = mg.movie_id
GROUP BY g.id, g.name;
```

Driving from genres with a LEFT JOIN keeps empty genres visible as NULL/zero instead of vanishing - the alternative to the inner-join route.

## Q37: Compute a rolling 7-day total of sales revenue ending on each date (tables: orders(order_date, amount), one row per day).

**Query:**
```sql
-- PostgreSQL
SELECT order_date,
       SUM(amount) OVER (ORDER BY order_date
                         RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW) AS revenue_7d
FROM orders
ORDER BY order_date;
```

**Explanation:** RANGE (not ROWS) counts the trailing 6 calendar days regardless of whether daily rows exist, which is the correct semantics for a 7-day rolling window.

**Alt1:**
```sql
-- MySQL 8+
SELECT o1.order_date,
       (SELECT SUM(o2.amount) FROM orders o2
         WHERE o2.order_date BETWEEN o1.order_date - INTERVAL 6 DAY AND o1.order_date) AS revenue_7d
FROM orders o1
ORDER BY o1.order_date;
```

The correlated BETWEEN subquery is the join trouble you would've handwritten; windows exist precisely because this was the pre-8.0 pattern.

## Q38: Compute month-over-month growth rate of new user signups (tables: users(id, created_at)).

**Query:**
```sql
-- PostgreSQL
WITH monthly AS (
  SELECT DATE_TRUNC('month', created_at) AS ym, COUNT(*) AS new_users
  FROM users GROUP BY 1
)
SELECT ym, new_users,
       LAG(new_users) OVER (ORDER BY ym) AS prev_users,
       ROUND(100.0 * (new_users - LAG(new_users) OVER (ORDER BY ym))
             / LAG(new_users) OVER (ORDER BY ym), 1) AS growth_pct
FROM monthly ORDER BY ym;
```

**Explanation:** Aggregate to a monthly series, then LAG pulls the prior month and one arithmetic expression yields the growth rate; dividing by NULL (first month) correctly yields NULL.

**Alt1:**
```sql
-- MySQL 8+
SELECT DATE_FORMAT(created_at, '%Y-%m') AS ym,
       COUNT(*) AS new_users
FROM users
GROUP BY DATE_FORMAT(created_at, '%Y-%m');
```

Without LAG, month-over-month in older MySQL required a self-join on `m1.ym = DATE_ADD(m2.ym, INTERVAL 1 MONTH)` - the derived-table alternative that windows replaced.

## Q39: Find the median salary for each department (tables: employees(id, dept_id, salary)).

**Query:**
```sql
-- PostgreSQL
SELECT dept_id,
       percentile_cont(0.5) WITHIN GROUP (ORDER BY salary) AS median_salary
FROM employees GROUP BY dept_id;
```

**Explanation:** PERCENTILE_CONT(0.5) computes a continuous median (interpolating between middles on even counts) in one expression - the idiomatic Postgres answer.

**Alt1:**
```sql
-- MySQL 8+
WITH idx AS (
  SELECT dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary) AS rn,
         COUNT(*) OVER (PARTITION BY dept_id) AS cnt
  FROM employees
)
SELECT dept_id, AVG(salary) AS median_salary
FROM idx
WHERE rn IN (FLOOR((cnt + 1) / 2), CEIL((cnt + 1) / 2))
GROUP BY dept_id;
```

The ROW_NUMBER + count window pair is the portable median: it takes the one or two middle positions and averages them, covering odd and even sizes.

## Q40: Can a meeting room host overlapping bookings? Show every pair that collides (tables: bookings(id, room_id, start_at, end_at)).

**Query:**
```sql
-- PostgreSQL
SELECT DISTINCT a.room_id, a.id AS booking_a, b.id AS booking_b,
       a.start_at, a.end_at, b.start_at, b.end_at
FROM bookings a
JOIN bookings b
  ON a.room_id = b.room_id
 AND a.id < b.id
 AND a.start_at < b.end_at
 AND b.start_at < a.end_at;
```

**Explanation:** Two ranges overlap iff each starts before the other ends; `a.id < b.id` dedupes each pair and starts the join only half the pairs.

**Alt1:**
```sql
-- SQL Server
SELECT room_id, id
FROM bookings x
WHERE EXISTS (
  SELECT 1 FROM bookings y
  WHERE y.room_id = x.room_id
    AND y.id <> x.id
    AND x.start_at < y.end_at
    AND y.start_at < x.end_at
);
```

EXISTS returns each colliding booking once regardless of how many partners it has - the correct shape for a "room is busy" flag.

## Q41: Which products sold more than 100 units in total? (tables: order_items(id, product_id, qty)).

**Query:**
```sql
-- MySQL 8+
SELECT product_id, SUM(qty) AS units_sold
FROM order_items
GROUP BY product_id
HAVING SUM(qty) > 100;
```

**Explanation:** The sum happens first, HAVING filters the aggregate output afterwards; a WHERE on qty here would silently count only large single orders.

**Alt1:**
```sql
-- PostgreSQL
SELECT product_id, units_sold
FROM (
  SELECT product_id, SUM(qty) AS units_sold
  FROM order_items GROUP BY product_id
) t
WHERE units_sold > 100;
```

Wrapping the grouped sum in a derived table and filtering outside is the explicit two-stage equivalent many find clearer to read.

## Q42: List the top 10 customers by lifetime spend (tables: customers(id, name), orders(id, customer_id, amount)).

**Query:**
```sql
-- MySQL 8+
SELECT c.id, c.name, SUM(o.amount) AS lifetime_value
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.id, c.name
ORDER BY lifetime_value DESC
LIMIT 10;
```

**Explanation:** Aggregate lifetime spend first, then ORDER BY + LIMIT 10; the JOIN uses the PK, and grouping by the customer key satisfies both select and group.

**Alt1:**
```sql
-- PostgreSQL
SELECT c.id, c.name, lv.spend
FROM (
  SELECT customer_id, SUM(amount) AS spend,
         RANK() OVER (ORDER BY SUM(amount) DESC) AS rnk
  FROM orders GROUP BY customer_id
) lv
JOIN customers c ON c.id = lv.customer_id
WHERE lv.rnk <= 10;
```

RANK-based top-K includes every customer tied at position 10; LIMIT would drop ties arbitrarily, which matters for fair LTV leaderboards.

## Q43: Find the 3 longest-running projects (tables: projects(id, name, start_date, end_date)).

**Query:**
```sql
-- MySQL 8+
SELECT id, name, start_date, end_date,
       DATEDIFF(end_date, start_date) AS days_run
FROM projects
ORDER BY days_run DESC
LIMIT 3;
```

**Explanation:** DATEDIFF produces the duration and a sort + LIMIT picks the longest; keep the computation in a SELECT alias so ORDER BY stays readable.

**Alt1:**
```sql
-- PostgreSQL
SELECT id, name, (end_date - start_date) AS days_run
FROM projects
ORDER BY 3 DESC
LIMIT 3;
```

Postgres subtracts dates natively returning days, and the ordinal ORDER BY 3 avoids recomputing the difference in the ORDER BY clause.

## Q44: Find the two nearest airports in a catalog by true surface distance (tables: airports(id, name, lat, lng)).

**Query:**
```sql
-- MySQL 8+
SELECT a1.name AS from_airport, a2.name AS to_airport,
       6371 * 2 * ASIN(SQRT(POWER(SIN(RADIANS(a2.lat - a1.lat) / 2), 2)
       + COS(RADIANS(a1.lat)) * COS(RADIANS(a2.lat))
       * POWER(SIN(RADIANS(a2.lng - a1.lng) / 2), 2))) AS distance_km
FROM airports a1
JOIN airports a2 ON a1.id < a2.id
ORDER BY distance_km
LIMIT 1;
```

**Explanation:** The clipped self-join on id < id pairs each airport with every *other* one exactly once, and the Haversine formula gives great-circle kilometers.

**Alt1:**
```sql
-- PostgreSQL
SELECT a1.name, a2.name,
       earth_distance(ll_to_earth(a1.lat, a1.lng),
                      ll_to_earth(a2.lat, a2.lng)) AS distance_m
FROM airports a1, airports a2
WHERE a1.id < a2.id
ORDER BY 3
LIMIT 1;
```

Using the earthdistance extension moves the geometry into the engine (a2.name kept; distance in meters) - the specialist tool when spatial accuracy is a frequent need.

## Q45: Which users signed up but have never performed any activity? (tables: users(id, name, signed_up_at), activity(user_id, at)).

**Query:**
```sql
-- MySQL 8+
SELECT u.id, u.name
FROM users u
WHERE NOT EXISTS (SELECT 1 FROM activity a WHERE a.user_id = u.id);
```

**Explanation:** The anti-join stops at the first activity row per user, so never-active users surface without counting all of their events.

**Alt1:**
```sql
-- PostgreSQL
SELECT u.id, u.name
FROM users u
LEFT JOIN activity a ON a.user_id = u.id
WHERE a.user_id IS NULL;
```

LEFT JOIN + IS NULL is the join-form anti-join; both plans are hash-based, but correlated NOT EXISTS shines when activity carries several indexes to probe.

## Q46: Pull the domain out of every customer's email address (tables: customers(id, name, email)).

**Query:**
```sql
-- MySQL 8+
SELECT id, email,
       SUBSTRING_INDEX(email, '@', -1) AS domain
FROM customers;
```

**Explanation:** SUBSTRING_INDEX splits on @ and the -1 takes the right-hand piece; scalar per row, index-free, matching the format column most event pipelines emit.

**Alt1:**
```sql
-- PostgreSQL
SELECT id, email,
       split_part(email, '@', 2) AS domain,
       left(email, strpos(email, '@') - 1) AS local_part
FROM customers;
```

split_part yields the domain on the second field, and strpos-based left() recovers the local part in the same pass - the richer parsing variant.

## Q47: Which pairs of cities are within 100 km of each other? (tables: cities(id, name, lat, lng)).

**Query:**
```sql
-- PostgreSQL
SELECT c1.name, c2.name
FROM cities c1 JOIN cities c2 ON c1.id < c2.id
WHERE 6371 * 2 * ASIN(SQRT(POWER(SIN(RADIANS(c2.lat - c1.lat) / 2), 2)
     + COS(RADIANS(c1.lat)) * COS(RADIANS(c2.lat))
     * POWER(SIN(RADIANS(c2.lng - c1.lng) / 2), 2))) <= 100
ORDER BY c1.name;
```

**Explanation:** Distance is computed once per candidate pair and filtered with the threshold; the id < id guard keeps each unordered pair exactly once.

**Alt1:**
```sql
-- MySQL 8+
SELECT c1.name, c2.name
FROM cities c1, cities c2
WHERE c1.id < c2.id
  AND ST_Distance_Sphere(POINT(c1.lng, c1.lat), POINT(c2.lng, c2.lat)) <= 100000
ORDER BY c1.name;
```

MySQL's ST_Distance_Sphere moves Haversine into an indexed spatial call - the best-in-class way once the city set outgrows a brute-force join.

## Q48: Rank products by how frequently they appear across orders (tables: order_items(id, order_id, product_id)).

**Query:**
```sql
-- MySQL 8+
SELECT product_id, COUNT(*) AS order_frequency
FROM order_items
GROUP BY product_id
ORDER BY order_frequency DESC;
```

**Explanation:** COUNT(*) per product counts order memberships, not units; this is item-frequency analysis and is the stepping-stone to market-basket counts.

**Alt1:**
```sql
-- MySQL 8+
SELECT DISTINCT product_id,
       COUNT(*) OVER (PARTITION BY product_id) AS order_frequency
FROM order_items
ORDER BY 2 DESC;
```

COUNT OVER keeps every order_item row alive while attaching each product's frequency - the shape that supports drilling into the contributing orders later.

## Q49: Compute each day's ride cancellation rate, counting only unbanned clients and drivers (tables: trips(id, client_id, driver_id, city_id, status, request_at), users(users_id, banned, role)).

**Query:**
```sql
-- MySQL 8+
SELECT t.request_at AS day,
       ROUND(SUM(CASE WHEN t.status IN ('cancelled_by_client', 'cancelled_by_driver')
                      THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancellation_rate
FROM trips t
JOIN users c ON c.users_id = t.client_id AND c.banned = 'No'
JOIN users d ON d.users_id = t.driver_id AND d.banned = 'No'
WHERE t.request_at BETWEEN '2024-10-01' AND '2024-10-03'
GROUP BY t.request_at;
```

**Explanation:** Both parties must be unbanned so the users table joins twice, and SUM(CASE)/COUNT turns a boolean into a rate - FAANG's favorite conditional-aggregation trick.

**Alt1:**
```sql
-- MySQL 8+
SELECT request_at,
       ROUND(AVG(status IN ('cancelled_by_client', 'cancelled_by_driver')), 2)
FROM trips
WHERE request_at BETWEEN '2024-10-01' AND '2024-10-03'
  AND client_id IN (SELECT users_id FROM users WHERE banned = 'No')
  AND driver_id IN (SELECT users_id FROM users WHERE banned = 'No')
GROUP BY request_at;
```

AVG over a boolean expression computes the same rate without CASE, and IN-subqueries filter banned users - fewer joins, same math.

## Q50: Report how many exams each student sat in each subject, even when never attempted (tables: students(student_id, student_name), subjects(subject_name), examinations(student_id, subject_name)).

**Query:**
```sql
-- MySQL 8+
SELECT s.student_id, s.student_name, su.subject_name,
       COUNT(e.subject_name) AS attended_exams
FROM students s
CROSS JOIN subjects su
LEFT JOIN examinations e
  ON e.student_id = s.student_id
 AND e.subject_name = su.subject_name
GROUP BY s.student_id, s.student_name, su.subject_name
ORDER BY s.student_id, su.subject_name;
```

**Explanation:** CROSS JOIN products every student with every subject, then the LEFT JOIN and COUNT(e.subject_name) count real attempts and report 0 otherwise - full Cartesian coverage.

**Alt1:**
```sql
-- PostgreSQL
SELECT s.student_id, s.student_name, su.subject_name,
       COUNT(e.*) AS attended_exams
FROM students s
CROSS JOIN subjects su
LEFT JOIN examinations e USING (student_id, subject_name)
GROUP BY s.student_id, s.student_name, su.subject_name
ORDER BY 1, 3;
```

USING condenses the equality join condition and COUNT(*) over the (possibly NULL) joined side mirrors the same outcome with less typing.

## Q51: In a cinema, swap the seat of each student with the adjacent student; the last odd seat stays put (tables: seat(id, student)).

**Query:**
```sql
-- MySQL 8+
SELECT CASE
         WHEN MOD(id, 2) = 1 AND id = (SELECT MAX(id) FROM seat) THEN id
         WHEN MOD(id, 2) = 1 THEN id + 1
         ELSE id - 1
       END AS id,
       student
FROM seat
ORDER BY id;
```

**Explanation:** Odd rows take the next id (pairing), even rows take the previous, and the last-row guard keeps the unpaired tail exchange-free - the classic self-defining CASE.

**Alt1:**
```sql
-- PostgreSQL
SELECT (id % 2) * LEAST(id + 1, (SELECT MAX(id) FROM seat))
       + (1 - id % 2) * (id - 1) AS id,
       student
FROM seat
ORDER BY id;
```

The fully-numeric variant shifts odds up and evens down with pure arithmetic, while LEAST pins the final odd seat to its own id - identical output, worse readability, which is why the CASE version dominates production.

## Q52: Find ids where the stadium recorded 100+ visitors on three consecutive days (tables: stadium(id, visit_date, people)).

**Query:**
```sql
-- MySQL 8+
WITH base AS (
  SELECT id, visit_date, people,
         LAG(people, 1)  OVER (ORDER BY id) AS p1,
         LAG(people, 2)  OVER (ORDER BY id) AS p2,
         LEAD(people, 1) OVER (ORDER BY id) AS n1,
         LEAD(people, 2) OVER (ORDER BY id) AS n2
  FROM stadium
)
SELECT id, visit_date, people FROM base
WHERE (people >= 100 AND p1 >= 100 AND p2 >= 100)
   OR (people >= 100 AND p1 >= 100 AND n1 >= 100)
   OR (people >= 100 AND n1 >= 100 AND n2 >= 100)
ORDER BY id;
```

**Explanation:** LAG/LEAD materialize the neighbors, and the three OR-branches cover "middle of a triple", "end of a triple", and "start of a triple" - all runs are caught.

**Alt1:**
```sql
-- MySQL 8+
SELECT DISTINCT a.id
FROM stadium a, stadium b, stadium c
WHERE a.people >= 100 AND b.people >= 100 AND c.people >= 100
  AND ((a.id = b.id + 1 AND b.id = c.id + 1)
    OR (b.id = a.id + 1 AND a.id = c.id + 1)
    OR (a.id = b.id + 1 AND c.id = b.id + 1))
ORDER BY a.id;
```

The triple self-join enumerates each window of three ids and is the LeetCode 601 answer for engines without window functions.

## Q53: Label each node of a tree as Root, Inner, or Leaf (tables: tree(id, p_id)).

**Query:**
```sql
-- MySQL 8+
SELECT id,
       CASE WHEN p_id IS NULL THEN 'Root'
            WHEN id NOT IN (SELECT p_id FROM tree WHERE p_id IS NOT NULL) THEN 'Leaf'
            ELSE 'Inner' END AS type
FROM tree
ORDER BY id;
```

**Explanation:** Root = no parent; Leaf = never a parent (guard against NULL inside the NOT IN list); everything else Inner - the three predicates, evaluated in order.

**Alt1:**
```sql
-- PostgreSQL
SELECT t.id,
       CASE WHEN t.p_id IS NULL THEN 'Root'
            WHEN EXISTS (SELECT 1 FROM tree c WHERE c.p_id = t.id) THEN 'Inner'
            ELSE 'Leaf' END AS type
FROM tree t
ORDER BY t.id;
```

EXISTS flips the leaf test into a positive "has children" check and sidesteps the classic NULL-in-NOT-IN pitfall entirely.

## Q54: Given an elevator that holds 1000 kg, who is the last person to board before it is full? (tables: queue(person_id, person_name, weight, turn)).

**Query:**
```sql
-- SQL Server
SELECT TOP 1 person_name
FROM (
  SELECT person_id, person_name, turn,
         SUM(weight) OVER (ORDER BY turn ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_weight
  FROM queue
) t
WHERE running_weight <= 1000
ORDER BY turn DESC;
```

**Explanation:** The running sum models boarding in turn order, then TOP 1 of the survivors by reverse turn - the person filling the elevator is the last eligible comma.

**Alt1:**
```sql
-- PostgreSQL
SELECT person_name
FROM queue
WHERE (SELECT SUM(weight) FROM queue q2 WHERE q2.turn <= queue.turn) <= 1000
ORDER BY turn DESC
LIMIT 1;
```

The correlated running sum is the window-free form; identical math, but it rescan queue per row, so Windows perform better at scale.

## Q55: Summarize each calendar month of transactions: totals and approved-only volumes per country (tables: transactions(id, country, state, amount, trans_date)).

**Query:**
```sql
-- MySQL 8+
SELECT DATE_FORMAT(trans_date, '%Y-%m') AS month,
       country,
       COUNT(*) AS trans_count,
       SUM(state = 'approved') AS approved_count,
       SUM(amount) AS trans_total_amount,
       SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END) AS approved_total_amount
FROM transactions
GROUP BY month, country;
```

**Explanation:** Grouping by month+country and doubling each column into (all | approved) is the FAANG conditional-aggregation staple - SUM(boolean) counts approvals, SUM(CASE) sums their amounts.

**Alt1:**
```sql
-- PostgreSQL
SELECT to_char(trans_date, 'YYYY-MM') AS month, country,
       COUNT(*) AS cnt,
       COUNT(*) FILTER (WHERE state = 'approved') AS approved,
       SUM(amount) FILTER (WHERE state = 'approved') AS approved_amount
FROM transactions
GROUP BY 1, 2;
```

Postgres FILTER makes conditional aggregates self-describing and is the preferred syntax over SUM(CASE) once the codebase is PG-only.

## Q56: Determine who wins an election where each vote records its candidate (tables: candidate(id, name), vote(id, candidate_id)).

**Query:**
```sql
-- MySQL 8+
SELECT c.name
FROM candidate c
JOIN vote v ON v.candidate_id = c.id
GROUP BY c.id, c.name
ORDER BY COUNT(*) DESC
LIMIT 1;
```

**Explanation:** Count votes per candidate, rank by that count descending, take the single leader; a GROUP BY + ORDER BY aggregate expression is the simplest winner algorithm.

**Alt1:**
```sql
-- SQL Server
SELECT name FROM candidate
WHERE id = (
  SELECT TOP 1 candidate_id FROM vote
  GROUP BY candidate_id ORDER BY COUNT(*) DESC
);
```

Resolving the winner id first inside a subquery then looking up the name keeps the candidate table scan tiny - a neat plan for huge vote tables.

## Q57: Which sales people never sold to the company named RED? (tables: salesperson(sales_id, name), company(com_id, name), orders(order_id, date, com_id, sales_id)).

**Query:**
```sql
-- MySQL 8+
SELECT name
FROM salesperson
WHERE sales_id NOT IN (
  SELECT o.sales_id
  FROM orders o
  JOIN company c ON c.com_id = o.com_id
  WHERE c.name = 'RED'
);
```

**Explanation:** Resolve RED's orders to salesperson ids, then NOT IN excludes them; an index on orders(com_id, sales_id) keeps the inner set tiny.

**Alt1:**
```sql
-- PostgreSQL
SELECT s.name
FROM salesperson s
WHERE NOT EXISTS (
  SELECT 1 FROM orders o JOIN company c ON c.com_id = o.com_id
  WHERE o.sales_id = s.sales_id AND c.name = 'RED'
);
```

NOT EXISTS re-checks per salesperson and leaves NULLs alone (NOT IN would silently drop a NULL sales_id), which makes it the safer form on dirty data.

## Q58: For each category list the single best-selling product; keep ties for first place (tables: products(id, name, category, units_sold)).

**Query:**
```sql
-- MySQL 8+
SELECT category, name, units_sold
FROM (
  SELECT category, name, units_sold,
         DENSE_RANK() OVER (PARTITION BY category ORDER BY units_sold DESC) AS rnk
  FROM products
) t
WHERE rnk = 1;
```

**Explanation:** The window partitions by category and ranks by sales; DENSE_RANK = 1 includes every product tied for the lead instead of arbitrarily cutting to one row.

**Alt1:**
```sql
-- MySQL 8+
SELECT category, name, units_sold
FROM products p
WHERE units_sold = (
  SELECT MAX(units_sold) FROM products p2 WHERE p2.category = p.category
);
```

The correlated MAX equals is the derived-table equivalent and handily demonstrates how a per-group max rewrites to a window-free query.

## Q59: Build a pivot report: revenue per product with one column for each of 2020, 2021, 2022 (tables: sales(id, product_id, yr, amount)).

**Query:**
```sql
-- MySQL 8+
SELECT product_id,
       SUM(CASE WHEN yr = 2020 THEN amount ELSE 0 END) AS y2020,
       SUM(CASE WHEN yr = 2021 THEN amount ELSE 0 END) AS y2021,
       SUM(CASE WHEN yr = 2022 THEN amount ELSE 0 END) AS y2022
FROM sales
GROUP BY product_id;
```

**Explanation:** Conditional aggregation rotates rows-to-columns with a fixed known member list - the standard long-to-wide pivot when each year is a hard-coded column.

**Alt1:**
```sql
-- Oracle
SELECT * FROM (
  SELECT product_id, yr, amount FROM sales
)
PIVOT (SUM(amount) FOR yr IN (2020 AS y2020, 2021 AS y2021, 2022 AS y2022));
```

Oracle's native PIVOT operator declares the rotation declaratively; it's the cleanest syntax when the column set is fixed but should not be hand-typed as CASE.

## Q60: How many people sit at each reporting depth below the CEO? (tables: employees(id, name, manager_id)).

**Query:**
```sql
-- PostgreSQL
WITH RECURSIVE org AS (
  SELECT id, name, manager_id, 1 AS depth
  FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.name, e.manager_id, o.depth + 1
  FROM employees e JOIN org o ON e.manager_id = o.id
)
SELECT depth, COUNT(*) AS employees_at_depth
FROM org GROUP BY depth ORDER BY depth;
```

**Explanation:** The anchor is the top of the tree, each iteration attaches one further level, and the UNION ALL guard terminates when no new managers remain - this is the recursive CTE pattern.

**Alt1:**
```sql
-- SQL Server
WITH e AS (SELECT id, manager_id FROM employees)
SELECT t.depth, COUNT(*) AS employees_at_depth
FROM (
  SELECT CASE
           WHEN m.id  IS NULL THEN 1
           WHEN m2.id IS NULL THEN 2
           WHEN m3.id IS NULL THEN 3
           ELSE 4 END AS depth
  FROM e lv0
  LEFT JOIN e m  ON m.id  = lv0.manager_id
  LEFT JOIN e m2 ON m2.id = m.manager_id
  LEFT JOIN e m3 ON m3.id = m2.manager_id
) t
GROUP BY t.depth ORDER BY t.depth;
```

Engines without recursive CTEs resolve depth by repeatedly self-joining one more level until a hop lands on NULL - a fixed-depth iteration that unrolls the recursion, capped here at 4 levels.

## Q61: Find numbers that appear three or more times consecutively in the log (tables: logs(id, num)).

**Query:**
```sql
-- MySQL 8+
SELECT DISTINCT l1.num AS consecutive_nums
FROM logs l1
JOIN logs l2 ON l1.id = l2.id - 1 AND l1.num = l2.num
JOIN logs l3 ON l1.id = l3.id - 2 AND l1.num = l3.num;
```

**Explanation:** Three self-joins anchor to an id and match its two successors by both id-stepping and value; DISTINCT collapses overlapping triples into one row.

**Alt1:**
```sql
-- MySQL 8+
SELECT DISTINCT num
FROM (
  SELECT num,
         LAG(num, 1) OVER (ORDER BY id) AS p1,
         LAG(num, 2) OVER (ORDER BY id) AS p2
  FROM logs
) t
WHERE num = p1 AND p1 = p2;
```

LAG turns the triple into a row-level predicate - the window rewrite that scales far past the triple self-join for long logs.

## Q62: Compute a 30-day rolling average of the daily sales amount (tables: daily_sales(order_date, amount), one row per day).

**Query:**
```sql
-- MySQL 8+
SELECT order_date,
       AVG(amount) OVER (ORDER BY order_date
                         RANGE INTERVAL 29 DAY PRECEDING) AS avg_30d
FROM daily_sales
ORDER BY order_date;
```

**Explanation:** RANGE INTERVAL counts calendar days, not rows, so a month with missing weekend rows still averages the true prior 30 days; ROWS 29 PRECEDING would skew it.

**Alt1:**
```sql
-- PostgreSQL
SELECT order_date,
       AVG(amount) OVER (ORDER BY order_date
                         RANGE BETWEEN INTERVAL '29 days' PRECEDING AND CURRENT ROW) AS avg_30d
FROM daily_sales;
```

The explicit RANGE BETWEEN spelling is Postgres' equivalent; both rely on ORDER BY over dates, which the engine indexes for the frame scan.

## Q63: For each salary record show the previous salary and the size of the raise (tables: salaries(employee_id, salary, from_date)).

**Query:**
```sql
-- SQL Server
SELECT employee_id, from_date, salary,
       LAG(salary) OVER (PARTITION BY employee_id ORDER BY from_date) AS prev_salary,
       salary - LAG(salary) OVER (PARTITION BY employee_id ORDER BY from_date) AS raise_amount
FROM salaries
ORDER BY employee_id, from_date;
```

**Explanation:** Partitioning by employee and ordering by effective date makes LAG read the prior raise row; the difference expresses the delta in the same projection.

**Alt1:**
```sql
-- PostgreSQL
SELECT s.employee_id, s.from_date, s.salary,
       (SELECT salary FROM salaries s2
         WHERE s2.employee_id = s.employee_id AND s2.from_date < s.from_date
         ORDER BY s2.from_date DESC LIMIT 1) AS prev_salary
FROM salaries s;
```

The correlated max-before subquery is the window-free previous-row lookup - the pattern everyone hand-coded before LAG existed.

## Q64: Turn a raw event stream into user sessions where 30 minutes of silence starts a new session (tables: events(user_id, event_time)).

**Query:**
```sql
-- PostgreSQL
WITH ev AS (
  SELECT user_id, event_time,
         LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time) AS prev_ts
  FROM events
),
flagged AS (
  SELECT user_id, event_time,
         CASE WHEN prev_ts IS NULL
               OR event_time - prev_ts > INTERVAL '30 minutes' THEN 1 ELSE 0 END AS new_session
  FROM ev
),
sess AS (
  SELECT user_id, event_time,
         SUM(new_session) OVER (PARTITION BY user_id ORDER BY event_time) AS session_id
  FROM flagged
)
SELECT user_id, session_id, MIN(event_time) AS started, MAX(event_time) AS ended,
       COUNT(*) AS event_count
FROM sess GROUP BY user_id, session_id;
```

**Explanation:** Flag each >30-min gap with 1, then SUM it as a running counter - every gap increment spawns a new session id; the canonical sessionization pattern at Intuit/Meta.

**Alt1:**
```sql
-- MySQL 8+
SELECT user_id, session_id, MIN(event_time), MAX(event_time), COUNT(*) 
FROM (
  SELECT user_id, event_time,
         SUM(gt30) OVER (PARTITION BY user_id ORDER BY event_time) AS session_id
  FROM (
    SELECT user_id, event_time,
           (event_time - LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time))
             > INTERVAL 30 MINUTE AS gt30
    FROM events
  ) x
) y GROUP BY user_id, session_id;
```

The same three-stage pipeline in MySQL 8 syntax; comparing the lag delta to an interval in a boolean keeps the flag stage inline.

## Q65: How many days passed between each customer's first and second order? (tables: orders(id, customer_id, order_date)).

**Query:**
```sql
-- MySQL 8+
WITH rn AS (
  SELECT customer_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS r
  FROM orders
)
SELECT a.customer_id,
       DATEDIFF(b.order_date, a.order_date) AS days_to_second_order
FROM rn a JOIN rn b
  ON a.customer_id = b.customer_id AND a.r = 1 AND b.r = 2;
```

**Explanation:** Numbering per customer and joining rank-1 to rank-2 of the same CTE isolates the first two purchases; a DATEDIFF then measures the gap.

**Alt1:**
```sql
-- PostgreSQL
WITH ordered AS (
  SELECT customer_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS r,
         COUNT(*) OVER (PARTITION BY customer_id) AS total
  FROM orders
)
SELECT customer_id,
       MAX(order_date ORDER BY r) - MIN(order_date) AS days_to_second
FROM ordered
WHERE r <= 2 AND total >= 2
GROUP BY customer_id;
```

Constraining to r<=2 and subtracting the min from the max order date yields the same span without a self-join; the WHERE total>=2 excludes single-order customers.

## Q66: Compare this month's sales to last month per region, showing the delta (tables: orders(region, order_date, amount)).

**Query:**
```sql
-- SQL Server
WITH m AS (
  SELECT region, FORMAT(order_date, 'yyyy-MM') AS ym, SUM(amount) AS amt
  FROM orders GROUP BY region, FORMAT(order_date, 'yyyy-MM')
)
SELECT region, ym, amt,
       LAG(amt) OVER (PARTITION BY region ORDER BY ym) AS prev_amt,
       amt - LAG(amt) OVER (PARTITION BY region ORDER BY ym) AS delta
FROM m ORDER BY region, ym;
```

**Explanation:** Roll sales into a monthly series per region, then LAG within each region pulls the prior month; the difference is the growth signal.

**Alt1:**
```sql
-- MySQL 8+
SELECT cur.region, cur.ym, cur.amt, prev.amt AS prev_amt, cur.amt - prev.amt AS delta
FROM (
  SELECT region, DATE_FORMAT(order_date, '%Y-%m') ym, SUM(amount) amt
  FROM orders GROUP BY 1, 2
) cur
LEFT JOIN (
  SELECT region, DATE_FORMAT(order_date, '%Y-%m') ym, SUM(amount) amt
  FROM orders GROUP BY 1, 2
) prev ON prev.region = cur.region
      AND prev.ym = DATE_FORMAT(DATE_ADD(STR_TO_DATE(CONCAT(cur.ym, '-01'), '%Y-%m-%d'),
                              INTERVAL -1 MONTH), '%Y-%m')
ORDER BY cur.region, cur.ym;
```

LEFT JOIN pins each month to its predecessor via date arithmetic - the pre-LAG comparison that window functions were invented to replace.

## Q67: Order numbers start at 1 with occasional holes; find the smallest missing number (tables: orders(order_num)).

**Query:**
```sql
-- MySQL 8+
WITH RECURSIVE seq AS (
  SELECT 1 AS n
  UNION ALL
  SELECT n + 1 FROM seq
  WHERE n < (SELECT MAX(order_num) FROM orders)
)
SELECT MIN(n) AS first_missing
FROM seq
WHERE n NOT IN (SELECT order_num FROM orders);
```

**Explanation:** Generate the complete 1..MAX range with a recursive CTE, then difference it against the existing numbers; the minimum of the leftover set is the answer.

**Alt1:**
```sql
-- PostgreSQL
SELECT MIN(n)
FROM generate_series(1, (SELECT MAX(order_num) FROM orders)) n
WHERE n NOT IN (SELECT order_num FROM orders);
```

generate_series is Postgres' one-liner source for the same range, keeping the anti-join identical while dropping the recursion.

## Q68: Which order amount is the mode - the most frequently occurring value? (tables: orders(id, amount)).

**Query:**
```sql
-- MySQL 8+
SELECT amount, COUNT(*) AS frequency
FROM orders
GROUP BY amount
HAVING COUNT(*) = (SELECT COUNT(*) FROM orders
                   GROUP BY amount ORDER BY COUNT(*) DESC LIMIT 1);
```

**Explanation:** The inner HAVING subquery returns the maximum group size, and the outer HAVING keeps every amount hitting that top count - so all modes when the distribution is tied.

**Alt1:**
```sql
-- PostgreSQL
SELECT amount, cnt FROM (
  SELECT amount, COUNT(*) AS cnt,
         RANK() OVER (ORDER BY COUNT(*) DESC) AS rnk
  FROM orders GROUP BY amount
) t WHERE rnk = 1;
```

RANK over the count assigns position 1 to all modes in one pass - cleaner than HAVING against a scalar LIMIT and trivially extendable to report the top N.

## Q69: Build a running balance per bank account in transaction order (tables: transactions(id, account_id, amount, created_at)).

**Query:**
```sql
-- PostgreSQL
SELECT account_id, created_at, amount,
       SUM(amount) OVER (PARTITION BY account_id ORDER BY created_at, id
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance
FROM transactions
ORDER BY account_id, created_at, id;
```

**Explanation:** The cumulative SUM window runs down the account's transaction history; tie-breaking on id keeps same-timestamp credits and debits deterministic.

**Alt1:**
```sql
-- MySQL 8+
SELECT t.account_id, t.created_at, t.amount,
       (SELECT SUM(t2.amount) FROM transactions t2
         WHERE t2.account_id = t.account_id
           AND (t2.created_at < t.created_at
             OR (t2.created_at = t.created_at AND t2.id <= t.id))) AS balance
FROM transactions t
ORDER BY t.account_id, t.created_at, t.id;
```

The correlated running-total subquery is the O(N^2) original that window functions replace - worth showing to justify engine-native frames.

## Q70: Compute first-month-to-second-month retention per signup cohort (tables: logins(user_id, login_date)).

**Query:**
```sql
-- PostgreSQL
WITH active AS (
  SELECT user_id, DATE_TRUNC('month', login_date) AS m
  FROM logins GROUP BY user_id, 2
)
SELECT a.m AS cohort_month,
       COUNT(DISTINCT a.user_id) AS cohort_size,
       COUNT(DISTINCT b.user_id) AS returned_next_month,
       ROUND(100.0 * COUNT(DISTINCT b.user_id) / COUNT(DISTINCT a.user_id), 1) AS retention_pct
FROM active a
LEFT JOIN active b
  ON a.user_id = b.user_id AND b.m = a.m + INTERVAL '1 month'
GROUP BY a.m;
```

**Explanation:** One active-month set, joined on user AND exactly one spent month later - retention is returned/cohort; the numerator and denominator stay distinct-counted.

**Alt1:**
```sql
-- SQL Server
SELECT a.m, COUNT(DISTINCT a.user_id) AS cohort,
       SUM(CASE WHEN b.user_id IS NOT NULL THEN 1 ELSE 0 END) AS returned
FROM (SELECT DISTINCT user_id, DATEADD(month, DATEDIFF(month, 0, login_date), 0) AS m
      FROM logins) a
LEFT JOIN (SELECT DISTINCT user_id, DATEADD(month, DATEDIFF(month, 0, login_date), 0) AS m
           FROM logins) b
  ON b.user_id = a.user_id AND b.m = DATEADD(month, 1, a.m)
GROUP BY a.m;
```

SQL Server normalizes months with DATEADD/DATEDIFF arithmetic and CASE-sums the survivors - the dialect-local pivot of the same cohort math.

## Q71: How many previously-active users churned last month, i.e., were active but not active anymore? (tables: logins(user_id, login_date)).

**Query:**
```sql
-- PostgreSQL
WITH m AS (
  SELECT user_id, DATE_TRUNC('month', login_date) AS mo
  FROM logins GROUP BY 1, 2
)
SELECT mo AS churned_month, COUNT(*) AS churned_users
FROM m
WHERE mo = (SELECT MAX(mo) FROM m) - INTERVAL '1 month'
  AND NOT EXISTS (SELECT 1 FROM m m2
                  WHERE m2.user_id = m.user_id AND m2.mo = (SELECT MAX(mo) FROM m))
GROUP BY mo;
```

**Explanation:** Split the activity stream into months, filter to last month, then NOT EXISTS removes anyone who reappeared this month - the residue is churned.

**Alt1:**
```sql
-- MySQL 8+
WITH base AS (
  SELECT user_id, DATE_FORMAT(login_date, '%Y-%m') AS ym
  FROM logins GROUP BY user_id, ym
)
SELECT b1.ym, COUNT(*) AS churn
FROM base b1
LEFT JOIN base b2
  ON b2.user_id = b1.user_id AND b2.ym = DATE_FORMAT(DATE_ADD(
       STR_TO_DATE(CONCAT(b1.ym, '-01'), '%Y-%m-%d'), INTERVAL 1 MONTH), '%Y-%m')
WHERE b2.ym IS NULL
GROUP BY b1.ym;
```

LEFT JOIN to the following month and keep rows without a successor - the join-based anti-join that computes churn for every month at once.

## Q72: A sales table has rows only on days something sold; fill in every calendar day with zero where no sales occurred (tables: sales(day, amount)).

**Query:**
```sql
-- PostgreSQL
WITH cal AS (
  SELECT generate_series('2024-01-01'::date, '2024-01-31'::date, '1 day')::date AS day
)
SELECT cal.day, COALESCE(s.amount, 0) AS amount
FROM cal
LEFT JOIN sales s ON s.day = cal.day
ORDER BY cal.day;
```

**Explanation:** generate_series is the free-standing calendar, and the LEFT JOIN + COALESCE(...,0) stamps every missing date with zero - the classic sparse-to-dense fix.

**Alt1:**
```sql
-- MySQL 8+
WITH RECURSIVE cal AS (
  SELECT CAST('2024-01-01' AS DATE) AS d
  UNION ALL
  SELECT d + INTERVAL 1 DAY FROM cal WHERE d < '2024-01-31'
)
SELECT cal.d, COALESCE(s.amount, 0) FROM cal
LEFT JOIN sales s ON s.day = cal.d;
```

MySQL reaches for the recursive CTE to synthesize the calendar, proving the same dense-series idea with engine-specific mechanics.

## Q73: Which customers have purchased every product the catalog carries? (tables: customers(id), orders(id, customer_id, product_id), products(id)).

**Query:**
```sql
-- MySQL 8+
SELECT o.customer_id
FROM orders o
GROUP BY o.customer_id
HAVING COUNT(DISTINCT o.product_id) = (SELECT COUNT(*) FROM products);
```

**Explanation:** Relational division done by cardinality: a customer who ordered as many distinct products as the catalog holds must have tried them all.

**Alt1:**
```sql
-- PostgreSQL
SELECT c.id
FROM customers c
WHERE NOT EXISTS (
  SELECT 1 FROM products p
  WHERE NOT EXISTS (
    SELECT 1 FROM orders o
    WHERE o.customer_id = c.id AND o.product_id = p.id
  )
);
```

Double negation - no product the customer skipped - is the division-theorem form, and it behaves correctly even when orders contain duplicate product rows.

## Q74: Compare each department's average salary ratio against the company average (tables: employees(id, dept_id, salary), departments(id, name)).

**Query:**
```sql
-- MySQL 8+
SELECT d.id, d.name,
       ROUND(AVG(e.salary), 2) AS dept_avg,
       ROUND((SELECT AVG(salary) FROM employees), 2) AS company_avg,
       ROUND(AVG(e.salary) / (SELECT AVG(salary) FROM employees), 2) AS ratio
FROM employees e JOIN departments d ON d.id = e.dept_id
GROUP BY d.id, d.name
ORDER BY ratio DESC;
```

**Explanation:** The company average is a constant scalar subquery evaluated once and reused in both output and the ratio; >1 means the department out-earns the firm.

**Alt1:**
```sql
-- SQL Server
SELECT d.name,
       AVG(e.salary) AS dept_avg,
       AVG(AVG(e.salary)) OVER () AS company_avg
FROM employees e JOIN departments d ON d.id = e.dept_id
GROUP BY d.name;
```

AVG-over-the-aggregates puts the firm average into a window over the department rows themselves - two aggregation passes in one query - no scalar needed.

## Q75: Show the most common basket amount per calendar month, all modes included (tables: orders(id, order_date, amount)).

**Query:**
```sql
-- MySQL 8+
WITH cnts AS (
  SELECT DATE_FORMAT(order_date, '%Y-%m') AS ym, amount, COUNT(*) AS cnt
  FROM orders GROUP BY ym, amount
)
SELECT ym, amount, cnt FROM (
  SELECT ym, amount, cnt,
         RANK() OVER (PARTITION BY ym ORDER BY cnt DESC) AS rnk
  FROM cnts
) t WHERE rnk = 1
ORDER BY ym;
```

**Explanation:** Aggregating amount-frequencies per month, then RANK within each month keeps every tied mode - per-group mode in two clean stages.

**Alt1:**
```sql
-- PostgreSQL
SELECT DISTINCT ON (ym) ym, amount, cnt
FROM (
  SELECT to_char(order_date, 'YYYY-MM') AS ym, amount, COUNT(*) AS cnt
  FROM orders GROUP BY 1, 2
) t
ORDER BY ym, cnt DESC;
```

Postgres DISTINCT ON takes the single top row per month directly; switching it for RANK keeps all ties - a two-line mutation of the same design.

## Q76: List every one-stop route between two cities and its total fare (tables: flights(id, origin, destination, cost)).

**Query:**
```sql
-- PostgreSQL
SELECT f1.origin, f1.destination AS stopover, f2.destination AS final_dest,
       f1.cost + f2.cost AS total_cost
FROM flights f1
JOIN flights f2 ON f1.destination = f2.origin
WHERE f1.origin <> f2.destination;
```

**Explanation:** One self-join chains any leg's destination to the next leg's origin; the WHERE blocks a B->A->B micro-loop, leaving clean one-hop planning rows.

**Alt1:**
```sql
-- MySQL 8+
SELECT f1.origin, f1.destination AS stopover, f2.destination AS final_dest,
       f1.cost + f2.cost AS total_cost
FROM flights f1
JOIN flights f2
  ON f1.destination = f2.origin
 AND f1.origin <> f2.destination;
```

Push the loop guard into the JOIN's ON clause so the optimizer prunes candidate leg-pairs before materializing them - prefer this when leg counts are high.

## Q77: Count the business days (Mon-Fri) in June 2024 (tables: none; pure date logic).

**Query:**
```sql
-- PostgreSQL
WITH days AS (
  SELECT generate_series('2024-06-01'::date, '2024-06-30'::date, '1 day')::date AS d
)
SELECT COUNT(*) AS business_days
FROM days
WHERE EXTRACT(dow FROM d) BETWEEN 1 AND 5;
```

**Explanation:** Generate every day in range and filter EXTRACT(dow) to 1-5 (Mon-Fri); the series does the enumeration so COUNT counts only working dates.

**Alt1:**
```sql
-- SQL Server
WITH nums AS (
  SELECT TOP (DATEDIFF(day, '2024-06-01', '2024-06-30') + 1) n = ROW_NUMBER() OVER (ORDER BY @@SPID) - 1
  FROM sys.all_columns a, sys.all_columns b
)
SELECT COUNT(*) AS business_days
FROM nums
WHERE DATEPART(dw, DATEADD(day, n, '2024-06-01')) BETWEEN 2 AND 6;
```

SQL Server fakes a number series from sys catalog and counts via DATEPART(dw) with US-centric (Sunday=1) mapping - the pragmatic pre-generate_series approach, localizable to any weekday convention.

## Q78: Normalize phone numbers stored with mixed punctuation and prefixes into plain 10-digit strings (tables: customers(id, name, phone)).

**Query:**
```sql
-- PostgreSQL
SELECT id, phone,
       REGEXP_REPLACE(phone, '[^0-9]', '', 'g') AS digits
FROM customers;
```

**Explanation:** The greedy character-class delete removes dashes, spaces and parens in one pass; 'g' makes it global, not just the first hit - the safest idempotent scrub.

**Alt1:**
```sql
-- MySQL 8+
SELECT id, phone,
       REGEXP_REPLACE(phone, '[^0-9]', '') AS digits
FROM customers;
```

MySQL 8 exposes the same global-replace default, so cross-engine the pattern is portable; keep phone bare on the left of REGEXP_REPLACE so nothing re-scans it.

## Q79: Compute the volume-weighted average price (VWAP) each stock traded at (tables: trades(id, symbol, shares, price)).

**Query:**
```sql
-- MySQL 8+
SELECT symbol,
       ROUND(SUM(shares * price) / SUM(shares), 4) AS vwap
FROM trades
GROUP BY symbol;
```

**Explanation:** Weighting each fill by its shares and dividing by total shares is the financial-standard VWAP; ROUND tames the float noise for equality joins downstream.

**Alt1:**
```sql
-- PostgreSQL
SELECT symbol,
       SUM(shares * price)::numeric / SUM(shares) AS vwap
FROM trades GROUP BY symbol;
```

Casting to numeric before dividing yields exact decimal arithmetic in Postgres where MySQL's double would drag in rounding artifacts.

## Q80: Bucket sessions by duration into 0-5m, 5-15m, and over 15m (tables: sessions(id, user_id, started_at, ended_at)).

**Query:**
```sql
-- MySQL 8+
SELECT CASE
         WHEN TIME_TO_SEC(TIMEDIFF(ended_at, started_at)) < 5 * 60 THEN '0-5m'
         WHEN TIME_TO_SEC(TIMEDIFF(ended_at, started_at)) < 15 * 60 THEN '5-15m'
         ELSE '15m+'
       END AS bucket,
       COUNT(*) AS sessions
FROM sessions
GROUP BY bucket
ORDER BY MIN(TIME_TO_SEC(TIMEDIFF(ended_at, started_at)));
```

**Explanation:** CASE buckets the duration into a label, GROUP BY on that label, then a MIN-duration ORDER BY reproduces the histogram order instead of alphabetical '0-5m', '15m+', '5-15m'.

**Alt1:**
```sql
-- PostgreSQL
SELECT CASE
         WHEN EXTRACT(EPOCH FROM (ended_at - started_at)) < 300 THEN '0-5m'
         WHEN EXTRACT(EPOCH FROM (ended_at - started_at)) < 900 THEN '5-15m'
         ELSE '15m+'
       END AS bucket,
       COUNT(*)
FROM sessions GROUP BY 1
ORDER BY MIN(EXTRACT(EPOCH FROM (ended_at - started_at)));
```

EXTRACT(EPOCH) yields seconds in PG versus TIMEDIFF in MySQL - same bucket math, engine-native time arithmetic.

## Q81: Find users who bought something within 24 hours after viewing it (tables: events(user_id, page, event, ts)).

**Query:**
```sql
-- PostgreSQL
SELECT DISTINCT e.user_id, e.page
FROM events e
JOIN events p
  ON p.user_id = e.user_id
 AND p.page = e.page
 AND p.ts < e.ts
WHERE e.event = 'purchase' AND p.event = 'view'
  AND e.ts - p.ts <= INTERVAL '24 hours';
```

**Explanation:** Self-join a view row to a later purchase of the same page, then constrain the lag to a day; DISTINCT collapses a user who bought the item many times.

**Alt1:**
```sql
-- MySQL 8+
SELECT DISTINCT v.user_id, v.page
FROM events v
WHERE v.event = 'view'
  AND EXISTS (
    SELECT 1 FROM events e
    WHERE e.user_id = v.user_id AND e.page = v.page
      AND e.event = 'purchase'
      AND e.ts BETWEEN v.ts AND v.ts + INTERVAL 24 HOUR
  );
```

EXISTS rephrases the join as a probe against the purchase table - identical semantics, often cheaper when purchases are rare relative to views.

## Q82: Sessionize login streaks: collapse consecutive-day logins into contiguous date ranges per user (tables: logins(user_id, login_date)).

**Query:**
```sql
-- PostgreSQL
WITH grp AS (
  SELECT user_id, login_date,
         login_date - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end,
       COUNT(*) AS days
FROM grp
GROUP BY user_id, grp
ORDER BY user_id, streak_start;
```

**Explanation:** Subtracting the row number from the date drops each island to a constant key - consecutive days share one grp value, anything non-consecutive shifts it; the gaps-and-islands cornerstone technique every interviewer circles back to.

**Alt1:**
```sql
-- MySQL 8+
WITH grp AS (
  SELECT user_id, login_date,
         login_date - INTERVAL rn DAY AS grp
  FROM (
    SELECT user_id, login_date,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM logins
  ) x
)
SELECT user_id, MIN(login_date), MAX(login_date), COUNT(*)
FROM grp GROUP BY user_id, grp ORDER BY user_id;
```

MySQL shifts the timeline with INTERVAL rather than date-minus-integer - same constant-key trick, dialect-aware arithmetic.

## Q83: What share of total revenue comes from the top 10% of customers? (tables: orders(id, customer_id, amount)).

**Query:**
```sql
-- PostgreSQL
WITH spent AS (
  SELECT customer_id, SUM(amount) AS total,
         PERCENT_RANK() OVER (ORDER BY SUM(amount) DESC) AS p
  FROM orders GROUP BY customer_id
)
SELECT ROUND(100.0 * SUM(total) / (SELECT SUM(amount) FROM orders), 1) AS top10_share_pct
FROM spent WHERE p <= 0.10;
```

**Explanation:** PERCENT_RANK pins each customer at their spending percentile; the WHERE p<=0.10 slices the top decile and their SUM over the company total is the concentration ratio - the revenue-concentration question Meta actually ships.

**Alt1:**
```sql
-- MySQL 8+
WITH spent AS (
  SELECT customer_id, SUM(amount) AS total,
         ROW_NUMBER() OVER (ORDER BY SUM(amount) DESC) AS rn,
         COUNT(*) OVER () AS cnt
  FROM orders GROUP BY customer_id
)
SELECT ROUND(100.0 * SUM(total) / (SELECT SUM(amount) FROM orders), 1) AS top10_share_pct
FROM spent WHERE rn <= CEIL(cnt * 0.1);
```

ROW_NUMBER + CEIL(cnt*0.1) approximates the decile cut as the top ten percent of *headcount* - MySQL's version when PERCENT_RANK gives little control over tie membership.

## Q84: Rotate employees into a wide row per employee that shows their salary recorded under each department they belong to, without hardcoding department names (tables: employees(id, name, dept_id), departments(id, name)).

**Query:**
```sql
-- PostgreSQL
SELECT e.id, e.name,
       jsonb_object_agg(d.name, e.salary) FILTER (WHERE d.name IS NOT NULL) AS salaries_by_dept
FROM employees e
LEFT JOIN departments d ON d.id = e.dept_id
GROUP BY e.id, e.name;
```

**Explanation:** jsonb_object_agg transplants a name-to-value map onto each row, so departments need never be known at query-write time - the schema-agnostic pivot.

**Alt1:**
```sql
-- MySQL 8+
SELECT e.id, e.name,
       GROUP_CONCAT(CONCAT(d.name, ':', e.salary) ORDER BY d.name) AS salary_map
FROM employees e JOIN departments d ON d.id = e.dept_id
GROUP BY e.id, e.name;
```

GROUP_CONCAT serializes dept:salary pairs into one string field - the lightest possible "wide" output when the consumer just needs a blob, not typed columns.

## Q85: Build a signup → profile → purchase funnel and report the conversion at each hop (tables: events(user_id, ts, event)).

**Query:**
```sql
-- PostgreSQL
SELECT
  COUNT(*) FILTER (WHERE event = 'signup')   AS signups,
  COUNT(*) FILTER (WHERE event = 'profile')  AS profiles,
  COUNT(*) FILTER (WHERE event = 'purchase') AS purchases,
  ROUND(100.0 * COUNT(*) FILTER (WHERE event = 'profile')
        / NULLIF(COUNT(*) FILTER (WHERE event = 'signup'), 0), 1) AS signup_to_profile_pct,
  ROUND(100.0 * COUNT(*) FILTER (WHERE event = 'purchase')
        / NULLIF(COUNT(*) FILTER (WHERE event = 'profile'), 0), 1) AS profile_to_purchase_pct
FROM events WHERE event IN ('signup', 'profile', 'purchase');
```

**Explanation:** FILTER counts each cohort and NULLIF guards the divide-by-zero on an empty signup month; the ratios chain the funnel's stages on one scan.

**Alt1:**
```sql
-- MySQL 8+
SELECT COUNT(*) AS signups,
       SUM(event = 'profile') AS profiles,
       SUM(event = 'purchase') AS purchases,
       ROUND(100 * SUM(event = 'profile') / NULLIF(SUM(event = 'signup'), 0), 1)
FROM events WHERE event IN ('signup','profile','purchase');
```

MySQL subbing SUM(boolean) for FILTER achieves identical counts - a renovation any linter turns FILTER into when ports are expected between engines.

## Q86: Split revenue between a customer's first-ever purchase and all repeat purchases (tables: orders(id, customer_id, order_date, amount)).

**Query:**
```sql
-- MySQL 8+
WITH rnk AS (
  SELECT customer_id, order_date, amount,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS n
  FROM orders
)
SELECT CASE WHEN n = 1 THEN 'first' ELSE 'repeat' END AS buyer_type,
       SUM(amount) AS revenue
FROM rnk
GROUP BY 1;
```

**Explanation:** ROW_NUMBER marks each order's birth rank inside the customer; rank 1 is first-buyer money and the rest aggregates to repeat revenue - the LTV split.

**Alt1:**
```sql
-- MySQL 8+
WITH flag AS (
  SELECT customer_id, amount,
         order_date = MIN(order_date) OVER (PARTITION BY customer_id) AS is_first
  FROM orders
)
SELECT CASE WHEN is_first THEN 'first' ELSE 'repeat' END AS buyer_type,
       SUM(amount) AS revenue
FROM flag
GROUP BY 1;
```

The window-MIN boolean flags the earliest order per customer without ranking, then one aggregate splits the money - the tie-safe rewrite that survives same-date race conditions.

## Q87: Find the median salary across the whole company, handling tied salaries (tables: employees(id, name, salary)).

**Query:**
```sql
-- MySQL 8+
WITH idx AS (
  SELECT salary,
         ROW_NUMBER() OVER (ORDER BY salary) AS rn,
         COUNT(*) OVER () AS cnt
  FROM employees
)
SELECT AVG(salary) AS median_salary
FROM idx
WHERE rn IN (FLOOR((cnt + 1) / 2), CEIL((cnt + 1) / 2));
```

**Explanation:** The two middle positions plug straight into AVG, which correctly interpolates even-count datasets and averages identical middle salaries without skewing - tie-safe by construction.

**Alt1:**
```sql
-- Oracle
SELECT DISTINCT MEDIAN(salary) OVER () AS median_salary
FROM employees;
```

Oracle's analytic MEDIAN does the same interpolation natively; MEDIAN ignores ties by definition, matching the continuous-median contract with a one-liner.

## Q88: Return the top 3 salaries per department using no window functions at all (tables: employees(id, name, dept_id, salary)).

**Query:**
```sql
-- MySQL 8+
SELECT e.id, e.name, e.dept_id, e.salary
FROM employees e
WHERE (SELECT COUNT(DISTINCT e2.salary) FROM employees e2
       WHERE e2.dept_id = e.dept_id AND e2.salary >= e.salary) <= 3
ORDER BY e.dept_id, e.salary DESC;
```

**Explanation:** The correlated COUNT of distinct higher-or-equal salaries gives each employee its band number; bands 1-3 survive - the pre-window top-N trick that still grades well.

**Alt1:**
```sql
-- SQL Server
SELECT e.id, e.name, e.dept_id, e.salary
FROM employees e
INNER JOIN employees e2 ON e2.dept_id = e.dept_id AND e2.salary >= e.salary
GROUP BY e.id, e.name, e.dept_id, e.salary
HAVING COUNT(DISTINCT e2.salary) <= 3
ORDER BY e.dept_id, e.salary DESC;
```

The same count via JOIN + GROUP BY + HAVING keeps the comparison relational rather than correlated - a straight port to engines that frown on scalar subqueries in WHERE.

## Q89: What is the longest streak of consecutive days any user logged in? (tables: logins(user_id, login_date)).

**Query:**
```sql
-- PostgreSQL
WITH grp AS (
  SELECT user_id, login_date,
         login_date - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
)
SELECT user_id, COUNT(*) AS streak_days
FROM grp
GROUP BY user_id, grp
ORDER BY streak_days DESC
LIMIT 1;
```

**Explanation:** Gap-and-island grouping converts streaks into sizes, then a single ORDER BY + LIMIT 1 picks the longest - the direct question this family of questions optimizes for.

**Alt1:**
```sql
-- MySQL 8+
SELECT user_id, COUNT(*) AS streak_days
FROM (
  SELECT user_id, login_date,
         login_date - INTERVAL rn DAY AS grp
  FROM (
    SELECT user_id, login_date,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM logins
  ) x
) g
GROUP BY user_id, grp
ORDER BY streak_days DESC
LIMIT 1;
```

The engine-local INTERVAL variant - identical islands, and returning rows per user if you drop the LIMIT is the bonus the interviewer is fishing for.

## Q90: Report active and newly-signed-up users side by side per month (tables: users(id, created_at), logins(user_id, login_date)).

**Query:**
```sql
-- MySQL 8+
WITH new_users AS (
  SELECT DATE_FORMAT(created_at, '%Y-%m') AS ym, COUNT(*) AS new_cnt
  FROM users GROUP BY DATE_FORMAT(created_at, '%Y-%m')
),
active_users AS (
  SELECT DATE_FORMAT(login_date, '%Y-%m') AS ym, COUNT(DISTINCT user_id) AS active_cnt
  FROM logins GROUP BY DATE_FORMAT(login_date, '%Y-%m')
)
SELECT a.ym, a.active_cnt, COALESCE(n.new_cnt, 0) AS new_users
FROM active_users a
LEFT JOIN new_users n ON n.ym = a.ym
ORDER BY a.ym;
```

**Explanation:** Two independent aggregates - one on signups, one on distinct logins - merge on the month key; LEFT JOIN keeps months with activity but zero signups, an easy-to-miss requirement.

**Alt1:**
```sql
-- PostgreSQL
SELECT ym,
       COUNT(DISTINCT CASE WHEN src = 'login' THEN user_id END) AS active,
       COUNT(*) FILTER (WHERE src = 'signup') AS new_users
FROM (
  SELECT user_id, DATE_TRUNC('month', login_date) AS ym, 'login' AS src FROM logins
  UNION ALL
  SELECT id, DATE_TRUNC('month', created_at), 'signup' FROM users
) t
GROUP BY ym;
```

UNION ALL over both sources then conditional-counts in one aggregate - a single grouped scan instead of two CTEs.

## Q91: For each date, how many distinct users logged in within the trailing 7-day window? (tables: logins(user_id, login_date)).

**Query:**
```sql
-- MySQL 8+
SELECT ds.day,
       (SELECT COUNT(DISTINCT l2.user_id) FROM logins l2
         WHERE l2.login_date BETWEEN ds.day - INTERVAL 6 DAY AND ds.day) AS active_7d
FROM (SELECT DISTINCT login_date AS day FROM logins) ds
ORDER BY ds.day;
```

**Explanation:** The correlated subquery bounds a distinct-count to a 7-day frame per date - a rolling distinct that no single frame can express, which is precisely why it tests window fluency.

**Alt1:**
```sql
-- MySQL 8+
SELECT ds.day,
       COUNT(DISTINCT l.user_id) AS active_7d
FROM (SELECT DISTINCT login_date AS day FROM logins) ds
JOIN logins l
  ON l.login_date BETWEEN ds.day - INTERVAL 6 DAY AND ds.day
GROUP BY ds.day
ORDER BY ds.day;
```

The join-form equivalent pairs each calendar day with every login inside its trailing 7 days and COUNT(DISTINCT user_id) dedupes - correct, but the ENGINE cannot skip stragglers per day the way the correlated version can.

## Q92: Sample 10 employees from each department at random (tables: employees(id, name, dept_id)).

**Query:**
```sql
-- PostgreSQL
WITH r AS (
  SELECT id, name, dept_id,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY random()) AS rn
  FROM employees
)
SELECT id, name, dept_id FROM r WHERE rn <= 10;
```

**Explanation:** random() inside the ordering makes every tie-break nondeterministic, and ROW_NUMBER per department truncates to ten - stratified random sampling in one window.

**Alt1:**
```sql
-- MySQL 8+
WITH r AS (
  SELECT id, name, dept_id,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY RAND()) AS rn
  FROM employees
)
SELECT id, name, dept_id FROM r WHERE rn <= 10;
```

MySQL spells it RAND() - identical stratified sampling, and both engines resolve the window ordering before the WHERE trims down to the sample.

## Q93: Show each employee together with the boss five reporting levels above them (tables: employees(id, name, manager_id)).

**Query:**
```sql
-- PostgreSQL
WITH RECURSIVE chain(emp_id, anc_id, dist) AS (
  SELECT id, id, 0 FROM employees
  UNION ALL
  SELECT c.emp_id, e.manager_id, c.dist + 1
  FROM chain c JOIN employees e ON c.anc_id = e.id
  WHERE e.manager_id IS NOT NULL
)
SELECT emp_id, MAX(anc_id) FILTER (WHERE dist = 5) AS boss_5_up
FROM chain
GROUP BY emp_id;
```

**Explanation:** The recursion walks every ancestor chain storing distance; a FILTER selects the exactly-five-levels-ancestor and MAX squeezes the group - clean org-chart navigation to arbitrary depth.

**Alt1:**
```sql
-- MySQL 8+
WITH RECURSIVE chain(emp_id, anc_id, dist) AS (
  SELECT id, id, 0 FROM employees
  UNION ALL
  SELECT c.emp_id, p.manager_id, c.dist + 1
  FROM chain c JOIN employees p ON c.anc_id = p.id
  WHERE p.manager_id IS NOT NULL
)
SELECT emp_id, anc_id AS boss_5_up FROM chain WHERE dist = 5;
```

Filtering for dist = 5 before collapsing keeps the ancestor id visible directly - MySQL shortens the GROUP BY that PostgreSQL needed for its FILTER-qualified MAX.

## Q94: Compute view → cart → purchase conversion rates per product line (tables: events(product_id, event, ts), products(id, name)).

**Query:**
```sql
-- MySQL 8+
SELECT p.name,
       SUM(e.event = 'view') AS views,
       SUM(e.event = 'cart') AS carts,
       SUM(e.event = 'purchase') AS purchases,
       ROUND(100 * SUM(e.event = 'purchase') / NULLIF(SUM(e.event = 'view'), 0), 1) AS view_to_buy_pct
FROM events e JOIN products p ON p.id = e.product_id
GROUP BY p.id, p.name;
```

**Explanation:** SUM over boolean predicates counts each stage with no subqueries, and NULLIF protects the ratio from divide-by-zero on a product nobody viewed.

**Alt1:**
```sql
-- PostgreSQL
SELECT p.name,
       COUNT(*) FILTER (WHERE e.event = 'view') AS views,
       COUNT(*) FILTER (WHERE e.event = 'cart') AS carts,
       COUNT(*) FILTER (WHERE e.event = 'purchase') AS purchases,
       ROUND(100.0 * COUNT(*) FILTER (WHERE e.event = 'purchase')
             / NULLIF(COUNT(*) FILTER (WHERE e.event = 'view'), 0), 1) AS view_to_buy_pct
FROM events e JOIN products p ON p.id = e.product_id
GROUP BY p.id, p.name;
```

FILTER reads as the intent for every stage, and Postgres builds one aggregate pass; the numeric 100.0 preserves decimal division instead of integer truncation.

## Q95: Which users visited page A then navigated to page B within 30 minutes? (tables: visits(user_id, page, ts)).

**Query:**
```sql
-- MySQL 8+
SELECT DISTINCT v1.user_id
FROM visits v1
JOIN visits v2
  ON v2.user_id = v1.user_id
 AND v2.page = 'B'
 AND v2.ts > v1.ts
WHERE v1.page = 'A'
  AND v2.ts <= v1.ts + INTERVAL 30 MINUTE;
```

**Explanation:** Self-join pairs an A-hit to any later B-hit, and the 30-minute cap on the timestamp difference expresses the behavioral window; DISTINCT reports the user once.

**Alt1:**
```sql
-- SQL Server
SELECT DISTINCT user_id
FROM visits v
WHERE page = 'B'
  AND EXISTS (
    SELECT 1 FROM visits a
    WHERE a.user_id = v.user_id AND a.page = 'A'
      AND v.ts BETWEEN a.ts AND DATEADD(minute, 30, a.ts)
  );
```

The EXISTS probe flips the join around so visits to B are scanned once and checked against prior A hits - the shape that wins when B-pages are rare.

## Q96: Generate a full year of calendar days and left join sparse traffic data onto it (tables: daily_data(day, value)).

**Query:**
```sql
-- MySQL 8+
WITH RECURSIVE cal AS (
  SELECT CAST('2024-01-01' AS DATE) AS d
  UNION ALL
  SELECT d + INTERVAL 1 DAY FROM cal WHERE d < '2024-12-31'
)
SELECT cal.d, COALESCE(dd.value, 0) AS value
FROM cal
LEFT JOIN daily_data dd ON dd.day = cal.d
ORDER BY cal.d;
```

**Explanation:** The recursive CTE is the driver and the LEFT JOIN fills gaps with COALESCE(...) - the dense calendar pattern that powers every "missing days" dashboard.

**Alt1:**
```sql
-- PostgreSQL
SELECT c.d, COALESCE(dd.value, 0) AS value
FROM generate_series('2024-01-01'::date, '2024-12-31'::date, '1 day') AS c(d)
LEFT JOIN daily_data dd ON dd.day = c.d
ORDER BY c.d;
```

generate_series produces the same calendar natively in Postgres - no recursion syntax, identical sparse-to-dense result.

## Q97: How many orders arrive on each day of the week? (tables: orders(id, order_date)).

**Query:**
```sql
-- PostgreSQL
SELECT to_char(order_date, 'Dy') AS weekday,
       EXTRACT(dow FROM order_date) AS dow_num,
       COUNT(*) AS orders
FROM orders
GROUP BY 1, 2
ORDER BY 2;
```

**Explanation:** EXTRACT(dow) sorts the week naturally (Sunday 0 through Saturday 6) while to_char labels it; grouping on both keeps the sort meaningful across years.

**Alt1:**
```sql
-- MySQL 8+
SELECT DAYNAME(order_date) AS weekday,
       DAYOFWEEK(order_date) AS dow_num,
       COUNT(*) AS orders
FROM orders
GROUP BY 1, 2
ORDER BY 2;
```

MySQL spells the pair DAYNAME/DAYOFWEEK - same contract, and including dow_num in GROUP BY preserves the chronological order the label alone cannot express.

## Q98: Which budget line items push their team over the annual allocation as they are approved in sequence? (tables: budgets(team, annual_limit), budget_items(id, team, amount)).

**Query:**
```sql
-- PostgreSQL
WITH running AS (
  SELECT bi.id, bi.team, bi.amount,
         SUM(bi.amount) OVER (PARTITION BY bi.team ORDER BY bi.id
                              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative
  FROM budget_items bi
)
SELECT r.id, r.team, r.amount, r.cumulative,
       b.annual_limit,
       r.cumulative - b.annual_limit AS overshoot
FROM running r
JOIN budgets b ON b.team = r.team
WHERE r.cumulative > b.annual_limit
ORDER BY r.team, r.id;
```

**Explanation:** The running total simulates approval order, and the join to each team's cap flags every item whose cumulative crosses it - cumulative-flagging against a reference table.

**Alt1:**
```sql
-- SQL Server
SELECT bi.id, bi.team, bi.amount,
       SUM(bi.amount) OVER (PARTITION BY bi.team ORDER BY bi.id
                            ROWS UNBOUNDED PRECEDING) AS cumulative
FROM budget_items bi;
```

A simpler frame spelling yields the same running total; joining it to budgets for the overshoot comparison is the step candidates most often forget to take.

## Q99: What is the highest number of conference calls simultaneously active in any room? (tables: calls(id, room_id, started_at, ended_at)).

**Query:**
```sql
-- PostgreSQL
WITH events AS (
  SELECT room_id, started_at AS ts, 1 AS delta FROM calls
  UNION ALL
  SELECT room_id, ended_at, -1 FROM calls
)
SELECT MAX(concurrent) AS max_concurrent
FROM (
  SELECT SUM(delta) OVER (PARTITION BY room_id ORDER BY ts, delta DESC) AS concurrent
  FROM events
) t;
```

**Explanation:** Every start adds 1 and every end removes 1; the cumulative sum over the event stream is the active count at each instant, and MAX is the peak - the sweep-line algorithm in SQL.

**Alt1:**
```sql
-- MySQL 8+
SELECT MAX(cnt) FROM (
  SELECT c1.id,
         (SELECT COUNT(*) FROM calls c2
          WHERE c2.room_id = c1.room_id
            AND c2.started_at < c1.ended_at
            AND c1.started_at < c2.ended_at) AS cnt
  FROM calls c1
) t;
```

Correlated overlap-count per call, maxed outside - the O(N^2) pre-window proof every interviewer accepts when the event-delta version is unknown.

## Q100: HR promotes up to 3 distinct salary bands per department; if several employees tie on the third band, promote all of them - but never touch band 4+. Show exactly that list (tables: employees(id, name, dept_id, salary)).

**Query:**
```sql
-- MySQL 8+
WITH ranked AS (
  SELECT id, name, dept_id, salary,
         DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS band
  FROM employees
)
SELECT id, name, dept_id, salary, band
FROM ranked
WHERE band <= 3
ORDER BY dept_id, band, name;
```

**Explanation:** DENSE_RANK collapses salaries into distinct bands, so band <= 3 keeps the whole third band including every tie, while RANK would misplace tied teammates into band 4 and silently demote them - DENSE_RANK is the whole point of the question.

**Alt1:**
```sql
-- MySQL 8+
SELECT e.id, e.name, e.dept_id, e.salary,
       (SELECT COUNT(DISTINCT e2.salary) FROM employees e2
        WHERE e2.dept_id = e.dept_id AND e2.salary >= e.salary) AS band
FROM employees e
HAVING band <= 3
ORDER BY e.dept_id, band, e.name;
```

The tally of strictly-higher-or-equal distinct salaries reproduces the band number without windows; the HAVING without GROUP BY is valid MySQL aliasing at the SELECT layer.
