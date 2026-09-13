# Aggregate Functions (COUNT SUM AVG MIN MAX) — 100 SQL Interview Q&A

## Q1: Write a query to count the total number of employees in the employees table.
**Query:**
```sql
SELECT COUNT(*) AS total_employees FROM employees;
```
**Explanation:** `COUNT(*)` counts every row in the table, including rows where every column is NULL.

## Q2: Write a query to count the number of employees in each department.
**Query:**
```sql
SELECT dept_id, COUNT(*) AS headcount
FROM employees
GROUP BY dept_id;
```
**Explanation:** Group rows by `dept_id`, then `COUNT(*)` runs once per group.
**Alt1:** Keep only departments with at least 5 staff using `HAVING`:
```sql
SELECT dept_id, COUNT(*) AS headcount
FROM employees
GROUP BY dept_id
HAVING COUNT(*) >= 5;
```
**Alt2:** Zero-safe counts (include empty departments) via `LEFT JOIN` + counting a non-NULL column:
```sql
SELECT d.dept_id, COUNT(e.employee_id) AS headcount
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.dept_id
GROUP BY d.dept_id;
```

## Q3: Write a query to count the distinct job titles held by employees.
**Query:**
```sql
SELECT COUNT(DISTINCT job_title) AS unique_titles FROM employees;
```
**Explanation:** `COUNT(DISTINCT col)` ignores duplicate values and NULLs, so each title is counted once.

## Q4: Write a query to compute the total salary paid to all employees.
**Query:**
```sql
SELECT SUM(salary) AS total_payroll FROM employees;
```
**Explanation:** `SUM` adds up non-NULL values only; any NULL salaries are skipped.

## Q5: Write a query to find the average salary of the whole company.
**Query:**
```sql
SELECT AVG(salary) AS avg_salary FROM employees;
```
**Explanation:** `AVG` is `SUM / COUNT` over non-NULL rows; it never includes NULLs in the denominator.

## Q6: Write a query to find the highest and lowest salary in one pass.
**Query:**
```sql
SELECT MIN(salary) AS min_salary, MAX(salary) AS max_salary FROM employees;
```
**Explanation:** `MIN`/`MAX` scan once and return extremes; several of them can coexist in a single SELECT.

## Q7: Write a query to get the name of the highest-paid employee.
**Query:**
```sql
SELECT name FROM employees ORDER BY salary DESC LIMIT 1;
```
**Explanation:** Sort by salary descending and keep the top row — the classic "first/last value" pattern.
**Alt1:** Subquery with MAX — ties all qualify, so the DB returns the first matching row:
```sql
SELECT name FROM employees WHERE salary = (SELECT MAX(salary) FROM employees);
```

## Q8: Write a query to count how many employees have a non-NULL commission.
**Query:**
```sql
SELECT COUNT(commission) AS with_commission FROM employees;
```
**Explanation:** `COUNT(col)` counts only non-NULL cells, so NULL commissions are silently excluded.

## Q9: Write a query to count employees earning above the company average.
**Query:**
```sql
SELECT COUNT(*) AS above_avg
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```
**Explanation:** The scalar subquery is evaluated once, then the WHERE filter is applied per row before COUNT runs.

## Q10: Write a query showing total sales per salesperson.
**Query:**
```sql
SELECT salesperson_id, SUM(amount) AS total_sales
FROM sales
GROUP BY salesperson_id
ORDER BY total_sales DESC;
```
**Explanation:** Rows are grouped per salesperson and `SUM(amount)` runs once per group.

## Q11: Write a query to find the average order amount across all orders.
**Query:**
```sql
SELECT AVG(amount) AS avg_order_amount FROM orders;
```
**Explanation:** One aggregate over the whole table — no GROUP BY needed when you want a single scalar.

## Q12: Write a query to find the earliest and latest order date in the table.
**Query:**
```sql
SELECT MIN(order_date) AS earliest, MAX(order_date) AS latest FROM orders;
```
**Explanation:** MIN/MAX work on dates because dates have a natural ordering (chronological).

## Q13: Write a query to compute total revenue per product.
**Query:**
```sql
SELECT product_id, SUM(price * quantity) AS revenue
FROM order_items
GROUP BY product_id;
```
**Explanation:** The expression `price * quantity` is evaluated per row, then SUM aggregates those row values per product.

## Q14: Write a query to find the total quantity sold per product category.
**Query:**
```sql
SELECT p.category, SUM(oi.quantity) AS total_qty
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
GROUP BY p.category;
```
**Explanation:** Join first to attach the category, then group by the joined column and aggregate quantity.

## Q15: Write a query to count orders per status.
**Query:**
```sql
SELECT status, COUNT(*) AS order_count
FROM orders
GROUP BY status;
```
**Explanation:** Every distinct status becomes one group and `COUNT(*)` reports its size.

## Q16: Write a query that returns count, average, minimum and maximum salary per department.
**Query:**
```sql
SELECT dept_id,
       COUNT(*)    AS emp_count,
       AVG(salary) AS avg_salary,
       MIN(salary) AS min_salary,
       MAX(salary) AS max_salary
FROM employees
GROUP BY dept_id;
```
**Explanation:** Four different aggregates over the same groups in one scan.
**Alt1:** Same, with a rounded average:
```sql
SELECT dept_id, ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY dept_id;
```

## Q17: Write a query to get total salary grouped by department and job title.
**Query:**
```sql
SELECT dept_id, job_title, SUM(salary) AS total
FROM employees
GROUP BY dept_id, job_title;
```
**Explanation:** Grouping by two columns makes one group per (dept, job) combination.

## Q18: Write a query to count how many employees were hired in each year.
**Query:**
```sql
-- Postgres
SELECT EXTRACT(YEAR FROM hire_date) AS hire_year, COUNT(*) AS hires
FROM employees
GROUP BY hire_year;
```
**Explanation:** Derive a scalar (the year) from the date column, then group by the derived value.
**Alt1:** MySQL:
```sql
-- MySQL
SELECT YEAR(hire_date) AS hire_year, COUNT(*) AS hires
FROM employees
GROUP BY YEAR(hire_date);
```

## Q19: Write a query to find the highest salary by department and job title.
**Query:**
```sql
SELECT dept_id, job_title, MAX(salary) AS top_salary
FROM employees
GROUP BY dept_id, job_title;
```
**Explanation:** MAX collapses each (dept, job) group down to its best-paid tuple.

## Q20: Write a query to find the department with the largest total payroll.
**Query:**
```sql
SELECT dept_id, SUM(salary) AS payroll
FROM employees
GROUP BY dept_id
ORDER BY payroll DESC
LIMIT 1;
```
**Explanation:** Aggregate, sort by the aggregate, keep one row.
**Alt1:** Constrain with HAVING and still order by the aggregate:
```sql
SELECT dept_id, SUM(salary) AS payroll
FROM employees
GROUP BY dept_id
HAVING SUM(salary) > 1000000
ORDER BY payroll DESC;
```

## Q21: Write a query to find customers who placed more than one order.
**Query:**
```sql
SELECT customer_id, COUNT(*) AS orders
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 1;
```
**Explanation:** HAVING filters groups by their aggregate after grouping — WHERE cannot do this.

## Q22: Write a query to identify the product with the most units sold.
**Query:**
```sql
SELECT product_id, SUM(quantity) AS units
FROM order_items
GROUP BY product_id
ORDER BY units DESC
LIMIT 1;
```
**Explanation:** Sum quantity per product, sort by that sum, take the leader.

## Q23: Write a query showing the number of distinct products in each order.
**Query:**
```sql
SELECT order_id, COUNT(DISTINCT product_id) AS product_count
FROM order_items
GROUP BY order_id;
```
**Explanation:** `COUNT(DISTINCT ...)` dedupes within each group, so repeated products count once per order.

## Q24: Write a query to compute average order value per customer.
**Query:**
```sql
SELECT customer_id, AVG(total) AS avg_order_value
FROM orders
GROUP BY customer_id;
```
**Explanation:** Group per customer and average the order totals within each group.

## Q25: Write a query returning three scalar counts in a single row: total employees, distinct departments, distinct job titles.
**Query:**
```sql
SELECT COUNT(*)                AS employees,
       COUNT(DISTINCT dept_id)  AS departments,
       COUNT(DISTINCT job_title) AS titles
FROM employees;
```
**Explanation:** Three aggregates with no GROUP BY — the whole table is a single implicit group.
## Q26: Write a query that demonstrates COUNT(*), COUNT(col) and COUNT(DISTINCT col) side by side.
**Query:**
```sql
SELECT COUNT(*)                 AS all_rows,
       COUNT(manager_id)        AS has_manager,
       COUNT(DISTINCT manager_id) AS distinct_managers
FROM employees;
```
**Explanation:** `COUNT(*)` counts all rows, `COUNT(col)` counts non-NULL cells, and `COUNT(DISTINCT col)` counts unique non-NULL values — three different answers from one table.

## Q27: Write a query to count employees who report to nobody (manager_id is NULL).
**Query:**
```sql
SELECT COUNT(*) - COUNT(manager_id) AS no_manager
FROM employees;
```
**Explanation:** Total rows minus rows with a manager equals rows whose `manager_id` is NULL — a classic NULL-counting trick.

## Q28: Write a query to find the average salary and prove that AVG ignores NULLs by computing it manually.
**Query:**
```sql
SELECT AVG(salary)                  AS avg_sql,
       SUM(salary) / COUNT(salary)  AS avg_manual
FROM employees;
```
**Explanation:** Both expressions skip NULL salaries, so the columns match; dividing by `COUNT(*)` instead would wrongly treat NULLs as zeros.

## Q29: Write a query that sums a column that may be entirely NULL, showing both the NULL trap and the COALESCE fix.
**Query:**
```sql
-- Postgres / MySQL / SQL Server
SELECT SUM(bonus) AS sum_bonus,
       COALESCE(SUM(bonus), 0) AS sum_bonus_coalesced
FROM employees
WHERE dept_id = 999;  -- no matching rows
```
**Explanation:** Aggregates over an empty set return NULL (not 0); `COALESCE` turns that into a displayable zero.

## Q30: Write a query to compute the percentage share of employees in each department.
**Query:**
```sql
SELECT dept_id,
       COUNT(*) * 100.0 / (SELECT COUNT(*) FROM employees) AS pct
FROM employees
GROUP BY dept_id;
```
**Explanation:** Each group's count is divided by a scalar total; the `* 100.0` forces floating-point division.
**Alt1:** Cross-join version — computes the total once into every group:
```sql
SELECT e.dept_id, COUNT(*) * 100.0 / t.total AS pct
FROM employees e
CROSS JOIN (SELECT COUNT(*) AS total FROM employees) t
GROUP BY e.dept_id;
```

## Q31: Write a query counting employees who earn above 100k per department using SUM with CASE.
**Query:**
```sql
SELECT dept_id,
       SUM(CASE WHEN salary > 100000 THEN 1 ELSE 0 END) AS high_earners
FROM employees
GROUP BY dept_id;
```
**Explanation:** The CASE emits 1/0 per row and SUM adds them; the explicit ELSE 0 stops NULLs leaking into the total.
**Alt1:** Shorter boolean-boolean form:
```sql
-- MySQL (and MariaDB)
SELECT dept_id, SUM(salary > 100000) AS high_earners
FROM employees
GROUP BY dept_id;
```

## Q32: Write the same count again, this time using COUNT(CASE WHEN ...).
**Query:**
```sql
SELECT dept_id, COUNT(CASE WHEN salary > 100000 THEN 1 END) AS high_earners
FROM employees
GROUP BY dept_id;
```
**Explanation:** The implicit ELSE is NULL, and COUNT skips NULLs — so only matching rows contribute. Same result as the SUM version.
**Alt1:** Postgres FILTER — the most readable form:
```sql
-- Postgres
SELECT dept_id, COUNT(*) FILTER (WHERE salary > 100000) AS high_earners
FROM employees
GROUP BY dept_id;
```

## Q33: Write a query that sums three columns across a row: budget + actual + forecast.
**Query:**
```sql
SELECT project_id, budget + actual + forecast AS total_spend
FROM projects;
```
**Explanation:** `+` adds across columns on one row. Beware the trap: any NULL column poisons the whole total — guard with COALESCE.
**Alt1:**
```sql
SELECT project_id,
       COALESCE(budget, 0) + COALESCE(actual, 0) + COALESCE(forecast, 0) AS total_spend
FROM projects;
```

## Q34: Write a query that returns per-department counts, totals and averages in a single statement.
**Query:**
```sql
SELECT dept_id,
       COUNT(*)    AS cnt,
       SUM(salary) AS total,
       AVG(salary) AS mean,
       MAX(salary) AS top
FROM employees
GROUP BY dept_id;
```
**Explanation:** Multiple aggregates run over the same group in a single scan, producing several summary columns.

## Q35: Write a query computing the average selling price per unit for each product.
**Query:**
```sql
SELECT product_id, SUM(line_total) / SUM(quantity) AS avg_unit_price
FROM order_items
GROUP BY product_id;
```
**Explanation:** A ratio of two sums — the correct "weighted" average unit price regardless of line sizes.
**Alt1:** AVG of per-line ratios — deliberately unweighted and mathematically different:
```sql
SELECT product_id, AVG(line_total / quantity) AS avg_line_ratio
FROM order_items
GROUP BY product_id;
```

## Q36: Write a query showing each employee's salary and what percentage it represents of their department's total.
**Query:**
```sql
SELECT e.name, e.salary,
       e.salary * 100.0 / d.dept_total AS pct_of_dept
FROM employees e
JOIN (SELECT dept_id, SUM(salary) AS dept_total
      FROM employees
      GROUP BY dept_id) d ON d.dept_id = e.dept_id;
```
**Explanation:** A derived table pre-computes each department total once, then the join compares row-to-total — no window functions required.

## Q37: Write a query to find the alphabetically first and last employee names.
**Query:**
```sql
SELECT MIN(name) AS first_name, MAX(name) AS last_name FROM employees;
```
**Explanation:** MIN/MAX use string (dictionary) ordering, so they pick the A–Z extremes.

## Q38: Write a query to find the earliest and latest hire date in each department.
**Query:**
```sql
SELECT dept_id,
       MIN(hire_date) AS first_hire,
       MAX(hire_date) AS latest_hire
FROM employees
GROUP BY dept_id;
```

## Q39: Write a query that lists employee names per department as one comma-separated string.
**Query:**
```sql
-- Postgres
SELECT dept_id, STRING_AGG(name, ', ' ORDER BY name) AS team
FROM employees
GROUP BY dept_id;
```
**Alt1:** MySQL:
```sql
-- MySQL
SELECT dept_id, GROUP_CONCAT(name ORDER BY name SEPARATOR ', ') AS team
FROM employees
GROUP BY dept_id;
```
**Alt2:** Oracle:
```sql
-- Oracle
SELECT dept_id, LISTAGG(name, ', ') WITHIN GROUP (ORDER BY name) AS team
FROM employees
GROUP BY dept_id;
```
**Alt3:** SQL Server:
```sql
-- SQL Server
SELECT dept_id, STRING_AGG(name, ', ') WITHIN GROUP (ORDER BY name) AS team
FROM employees
GROUP BY dept_id;
```
**Explanation:** All four dialects concatenate group rows; ordering inside the aggregate makes the list deterministic.

## Q40: Write a query to count employees whose salary exceeds their own department's average.
**Query:**
```sql
SELECT COUNT(*)
FROM employees e
WHERE e.salary > (SELECT AVG(salary) FROM employees d WHERE d.dept_id = e.dept_id);
```
**Explanation:** The correlated subquery recomputes the department average per outer row.
**Alt1:** Derived-table version — the average is computed once per department:
```sql
SELECT e.name, e.salary
FROM employees e
JOIN (SELECT dept_id, AVG(salary) AS avg_sal
      FROM employees GROUP BY dept_id) d
  ON d.dept_id = e.dept_id AND e.salary > d.avg_sal;
```

## Q41: Write a query counting orders per month and year.
**Query:**
```sql
-- Postgres
SELECT EXTRACT(YEAR FROM order_date)  AS yr,
       EXTRACT(MONTH FROM order_date) AS mon,
       COUNT(*) AS orders
FROM orders
GROUP BY yr, mon
ORDER BY yr, mon;
```
**Alt1:** MySQL:
```sql
-- MySQL
SELECT YEAR(order_date) AS yr, MONTH(order_date) AS mon, COUNT(*) AS orders
FROM orders
GROUP BY YEAR(order_date), MONTH(order_date);
```

## Q42: Write a query using Postgres FILTER to count high-value orders per customer.
**Query:**
```sql
-- Postgres
SELECT customer_id,
       COUNT(*)                              AS all_orders,
       COUNT(*) FILTER (WHERE amount > 1000) AS big_orders
FROM orders
GROUP BY customer_id;
```
**Explanation:** `FILTER` restricts which rows feed one aggregate without touching its neighbors — clean multi-condition aggregation.

## Q43: Write a query counting cancelled vs completed orders in one SELECT.
**Query:**
```sql
-- Postgres
SELECT COUNT(*) FILTER (WHERE status = 'cancelled') AS cancelled,
       COUNT(*) FILTER (WHERE status = 'completed') AS completed
FROM orders;
```
**Alt1:** Dialect-neutral SUM(CASE):
```sql
SELECT SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled,
       SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed
FROM orders;
```
**Explanation:** Both return identical integers; FILTER is idiomatic Postgres, SUM(CASE) works everywhere.

## Q44: Write a query computing the average amount of only the orders worth at least 100.
**Query:**
```sql
-- Postgres
SELECT AVG(amount) FILTER (WHERE amount >= 100) AS avg_big
FROM orders;
```
**Alt1:** Conditional version:
```sql
SELECT AVG(CASE WHEN amount >= 100 THEN amount END) AS avg_big
FROM orders;
```
**Explanation:** Non-matching rows become NULL and AVG skips NULLs — no ELSE 0, so the denominator counts only qualifying rows.

## Q45: Write a query showing, per customer, the share of their orders that exceed $500.
**Query:**
```sql
-- Postgres
SELECT customer_id,
       COUNT(*) FILTER (WHERE amount > 500) * 100.0 / COUNT(*) AS pct_big
FROM orders
GROUP BY customer_id;
```
**Explanation:** FILTER supplies the numerator, a plain COUNT the denominator — two aggregates, one group.
**Alt1:** SUM(CASE) equivalent:
```sql
-- MySQL
SELECT customer_id,
       SUM(amount > 500) * 100.0 / COUNT(*) AS pct_big
FROM orders
GROUP BY customer_id;
```

## Q46: Write a query counting distinct VIP customers — those with at least one order above $1000.
**Query:**
```sql
SELECT COUNT(DISTINCT customer_id) AS vip_customers
FROM orders
WHERE amount > 1000;
```
**Explanation:** Filter first, then count unique customers that survive — simplest and fastest.
**Alt1:** Per-customer view with FILTER — answers "who, and how many each":
```sql
-- Postgres
SELECT customer_id,
       COUNT(*) FILTER (WHERE amount > 1000) AS big_orders
FROM orders
GROUP BY customer_id
HAVING COUNT(*) FILTER (WHERE amount > 1000) > 0;
```

## Q47: Write a query counting, per supplier, the distinct expensive products (price > 500) they supply using COUNT(DISTINCT CASE WHEN ...).
**Query:**
```sql
SELECT supplier_id,
       COUNT(DISTINCT CASE WHEN price > 500 THEN product_id END) AS premium_products
FROM products
GROUP BY supplier_id;
```
**Explanation:** The CASE maps non-qualifying rows to NULL; `COUNT(DISTINCT ...)` ignores NULLs and dedupes product_id across rows.
**Alt1:** Pre-filtered derived table, same result:
```sql
SELECT supplier_id, COUNT(*) AS premium_products
FROM (SELECT DISTINCT supplier_id, product_id
      FROM products WHERE price > 500) p
GROUP BY supplier_id;
```

## Q48: Write a query counting active (is_active = true) users per country using a boolean-cast trick.
**Query:**
```sql
-- Postgres
SELECT country,
       SUM(is_active::int) AS active_users,
       COUNT(*)            AS total_users
FROM users
GROUP BY country;
```
**Explanation:** Casting boolean to int turns true→1/false→0, so SUM counts activations.
**Alt1:** MySQL (booleans are tinyints there):
```sql
-- MySQL
SELECT country, SUM(is_active) AS active_users
FROM users
GROUP BY country;
```
**Alt2:** Dialect-neutral CASE:
```sql
SELECT country, SUM(CASE WHEN is_active THEN 1 ELSE 0 END) AS active_users
FROM users
GROUP BY country;
```

## Q49: Write a query finding departments whose average salary is below the company average, and count them.
**Query:**
```sql
SELECT COUNT(*) AS below_company_avg
FROM (SELECT dept_id, AVG(salary) AS avg_sal
      FROM employees GROUP BY dept_id) d
WHERE d.avg_sal < (SELECT AVG(salary) FROM employees);
```
**Explanation:** Aggregates can't live in WHERE, so group first in a derived table, then filter against the scalar company average.
**Alt1:** HAVING inside, count outside:
```sql
SELECT COUNT(*) FROM (
  SELECT dept_id
  FROM employees
  GROUP BY dept_id
  HAVING AVG(salary) < (SELECT AVG(salary) FROM employees)
) t;
```

## Q50: Write a query that shows every department's max salary alongside the company-wide min and max in the same row.
**Query:**
```sql
SELECT e.dept_id,
       MAX(e.salary) AS dept_max,
       c.max_sal     AS company_max,
       c.min_sal     AS company_min
FROM employees e
CROSS JOIN (SELECT MIN(salary) AS min_sal, MAX(salary) AS max_sal FROM employees) c
GROUP BY e.dept_id, c.max_sal, c.min_sal;
```
**Explanation:** The derived table produces exactly one row; CROSS JOIN replicates it to every group, giving per-group and global extremes without window functions.
## Q51: Write a query computing variance and standard deviation of salaries per department.
**Query:**
```sql
-- Postgres / MySQL
SELECT dept_id, VARIANCE(salary) AS var_sal, STDDEV(salary) AS sd_sal
FROM employees
GROUP BY dept_id;
```
**Alt1:** SQL Server uses the older aliases:
```sql
-- SQL Server
SELECT dept_id, VAR(salary) AS var_sal, STDEV(salary) AS sd_sal
FROM employees
GROUP BY dept_id;
```
**Explanation:** Variance and standard deviation measure spread around the mean; the two dialects simply name them differently.

## Q52: Write a query showing both population and sample variance/stddev.
**Query:**
```sql
-- Postgres
SELECT VAR_POP(salary)    AS var_pop,
       VAR_SAMP(salary)   AS var_samp,
       STDDEV_POP(salary) AS sd_pop,
       STDDEV_SAMP(salary) AS sd_samp
FROM employees;
```
**Explanation:** *_POP divides by n, *_SAMP divides by n−1; the unqualified VARIANCE/STDDEV are the sample versions in most engines.

## Q53: Write a query measuring the linear correlation between years of service and salary.
**Query:**
```sql
-- Postgres
SELECT CORR(years_of_service, salary) AS service_salary_corr
FROM employees;
```
**Explanation:** `CORR` returns Pearson's r in [−1, 1]. MySQL has no CORR aggregate, so compute it manually from five sums.
**Alt1:** Manual Pearson correlation (portable to any engine):
```sql
-- MySQL
SELECT (SUM(x*y) - SUM(x)*SUM(y)/COUNT(*)) /
       SQRT((SUM(x*x) - SUM(x)*SUM(x)/COUNT(*)) *
            (SUM(y*y) - SUM(y)*SUM(y)/COUNT(*))) AS corr
FROM (SELECT years_of_service AS x, salary AS y FROM employees) t;
```

## Q54: Write a query to find the most common salary (the mode).
**Query:**
```sql
SELECT salary, COUNT(*) AS freq
FROM employees
GROUP BY salary
ORDER BY freq DESC
LIMIT 1;
```
**Explanation:** Group, count, sort by frequency, keep the top row; ties arbitrarily pick one value.
**Alt1:** Oracle has no LIMIT — wrap in a subquery:
```sql
-- Oracle
SELECT * FROM (
  SELECT salary, COUNT(*) AS freq
  FROM employees GROUP BY salary ORDER BY COUNT(*) DESC
) WHERE ROWNUM = 1;
```

## Q55: Write a query to find the mode salary per department.
**Query:**
```sql
SELECT f.dept_id, f.salary
FROM (
  SELECT dept_id, salary, COUNT(*) AS freq
  FROM employees GROUP BY dept_id, salary
) f
JOIN (
  SELECT dept_id, MAX(freq) AS max_freq
  FROM (SELECT dept_id, salary, COUNT(*) AS freq
        FROM employees GROUP BY dept_id, salary) s
  GROUP BY dept_id
) m ON m.dept_id = f.dept_id AND m.max_freq = f.freq;
```
**Explanation:** Two groupings: first get every (dept, salary, freq), then join back to each department's max frequency — no window functions needed.
**Alt1:** Postgres `DISTINCT ON` shortcut:
```sql
-- Postgres
SELECT DISTINCT ON (dept_id) dept_id, salary, COUNT(*) AS freq
FROM employees
GROUP BY dept_id, salary
ORDER BY dept_id, COUNT(*) DESC;
```

## Q56: Write a query computing a weighted average — average price weighted by quantity sold per product.
**Query:**
```sql
SELECT product_id,
       SUM(price * quantity) / NULLIF(SUM(quantity), 0) AS weighted_avg
FROM order_items
GROUP BY product_id;
```
**Explanation:** Total spend divided by total units. `NULLIF` turns a zero denominator into NULL to dodge divide-by-zero errors.

## Q57: Write a query to get each customer's first and last purchase — dates and amounts together.
**Query:**
```sql
SELECT f.customer_id,
       f.order_date AS first_date, of_.amount AS first_amount,
       l.order_date AS last_date,  ol.amount  AS last_amount
FROM (SELECT customer_id, MIN(order_date) AS order_date FROM orders GROUP BY customer_id) f
JOIN orders of_ ON of_.customer_id = f.customer_id AND of_.order_date = f.order_date
JOIN (SELECT customer_id, MAX(order_date) AS order_date FROM orders GROUP BY customer_id) l
  ON l.customer_id = f.customer_id
JOIN orders ol  ON ol.customer_id  = l.customer_id AND ol.order_date  = l.order_date;
```
**Explanation:** MIN/MAX find the boundary dates, then joins attach the full rows carrying the amounts.
**Alt1:** Scalar subqueries skip the joins entirely:
```sql
SELECT DISTINCT o.customer_id,
  (SELECT amount FROM orders o2 WHERE o2.customer_id = o.customer_id
    ORDER BY o2.order_date LIMIT 1) AS first_amount,
  (SELECT amount FROM orders o2 WHERE o2.customer_id = o.customer_id
    ORDER BY o2.order_date DESC LIMIT 1) AS last_amount
FROM orders o;
```

## Q58: Write a query returning the cheapest and the priciest product in a single row.
**Query:**
```sql
SELECT (SELECT name FROM products ORDER BY price ASC  LIMIT 1)  AS cheapest,
       (SELECT name FROM products ORDER BY price DESC LIMIT 1) AS priciest;
```
**Explanation:** Two scalar subqueries collapse "first/last value by key" into one row — a MIN/MAX-adjacent trick for fetching whole rows.
**Alt1:** MIN/MAX + membership test:
```sql
SELECT name, price
FROM products
WHERE price = (SELECT MIN(price) FROM products)
   OR price = (SELECT MAX(price) FROM products);
```

## Q59: Show the classic NULL trap with NOT IN — a query intending "employees in no big department" that silently returns nothing.
**Query:**
```sql
SELECT name FROM employees
WHERE dept_id NOT IN (SELECT dept_id FROM departments WHERE headcount > 5000);
```
**Explanation:** If the subquery returns any NULL, `dept_id NOT IN (...)` evaluates to NULL (never TRUE) for every row and the query returns 0 rows — a famous trap.
**Alt1:** Fix by excluding NULLs up front:
```sql
SELECT name FROM employees
WHERE dept_id NOT IN (SELECT dept_id FROM departments
                      WHERE headcount > 5000 AND dept_id IS NOT NULL);
```
**Alt2:** The bulletproof rewrite with NOT EXISTS:
```sql
SELECT name FROM employees e
WHERE NOT EXISTS (SELECT 1 FROM departments d
                  WHERE d.dept_id = e.dept_id AND d.headcount > 5000);
```

## Q60: Write a query showing, per customer, how many days elapsed between their first and latest order.
**Query:**
```sql
-- Postgres
SELECT customer_id,
       MAX(order_date) - MIN(order_date) AS days_between
FROM orders
GROUP BY customer_id;
```
**Alt1:** SQL Server / MySQL:
```sql
SELECT customer_id,
       DATEDIFF(day, MIN(order_date), MAX(order_date)) AS days_between
FROM orders
GROUP BY customer_id;
```
**Explanation:** Reach the extremes with MIN/MAX first, then diff the two dates.

## Q61: Write a query that concatenates, per department, the job titles ranked by descending frequency.
**Query:**
```sql
-- Postgres
SELECT dept_id,
       STRING_AGG(job_title, ', ' ORDER BY cnt DESC, job_title) AS ranked_titles
FROM (SELECT dept_id, job_title, COUNT(*) AS cnt
      FROM employees GROUP BY dept_id, job_title) t
GROUP BY dept_id;
```
**Explanation:** Group first to obtain frequencies, then the ordering inside STRING_AGG sorts the list deterministically.
**Alt1:** MySQL:
```sql
-- MySQL
SELECT dept_id,
       GROUP_CONCAT(job_title ORDER BY cnt DESC, job_title SEPARATOR ', ') AS ranked_titles
FROM (SELECT dept_id, job_title, COUNT(*) AS cnt
      FROM employees GROUP BY dept_id, job_title) t
GROUP BY dept_id;
```

## Q62: Write a query listing the distinct set of product categories each customer has bought, concatenated.
**Query:**
```sql
-- MySQL
SELECT o.customer_id,
       GROUP_CONCAT(DISTINCT p.category ORDER BY p.category SEPARATOR ' | ') AS categories
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
GROUP BY o.customer_id;
```
**Explanation:** `GROUP_CONCAT(DISTINCT ...)` dedupes inside the string, so categories bought many times still appear once.
**Alt1:** Postgres — dedupe in a derived set, then STRING_AGG:
```sql
-- Postgres
SELECT customer_id,
       STRING_AGG(category, ' | ' ORDER BY category) AS categories
FROM (SELECT DISTINCT o.customer_id, p.category
      FROM orders o
      JOIN order_items oi ON oi.order_id = o.order_id
      JOIN products p ON p.product_id = oi.product_id) t
GROUP BY customer_id;
```

## Q63: Write a query that, per department, reports both the count of distinct tags and the accumulated tag list.
**Query:**
```sql
-- Postgres
SELECT dept_id,
       COUNT(DISTINCT tag) AS distinct_tags,
       STRING_AGG(DISTINCT tag, ', ' ORDER BY tag) AS tag_list
FROM article_tags
GROUP BY dept_id;
```
**Explanation:** The distinct count and the concatenated grouping ride the same GROUP BY — two ways to summarize one dimension.

## Q64: Write a query counting orders per weekday.
**Query:**
```sql
-- Postgres
SELECT EXTRACT(ISODOW FROM order_date) AS dow, COUNT(*) AS orders
FROM orders
GROUP BY dow
ORDER BY dow;
```
**Alt1:** MySQL:
```sql
-- MySQL
SELECT DAYOFWEEK(order_date) AS dow, COUNT(*) AS orders
FROM orders
GROUP BY DAYOFWEEK(order_date) ORDER BY 1;
```
**Alt2:** SQL Server:
```sql
-- SQL Server
SELECT DATEPART(weekday, order_date) AS dow, COUNT(*) AS orders
FROM orders
GROUP BY DATEPART(weekday, order_date) ORDER BY 1;
```
**Explanation:** Extract a date component and group by it; Postgres and MySQL accept an alias in GROUP BY, SQL Server needs the raw expression.

## Q65: Write a query returning the department with the highest average salary, with its count and total payroll.
**Query:**
```sql
SELECT dept_id,
       COUNT(*) AS cnt,
       SUM(salary) AS total,
       AVG(salary) AS avg_sal
FROM employees
GROUP BY dept_id
ORDER BY avg_sal DESC
LIMIT 1;
```
**Explanation:** Compute every aggregate, order by the average, keep the winning group.

## Q66: Write a query summing the salaries of the company's five highest-paid employees.
**Query:**
```sql
SELECT SUM(salary) AS top5_payroll
FROM (SELECT salary FROM employees ORDER BY salary DESC LIMIT 5) t;
```
**Explanation:** A derived table caps the set with LIMIT, then SUM runs over just those rows — "top-N aggregate" without window functions.
**Alt1:** SQL Server with TOP:
```sql
-- SQL Server
SELECT SUM(salary) AS top5_payroll
FROM (SELECT TOP 5 salary FROM employees ORDER BY salary DESC) t;
```

## Q67: Write a query comparing the average salary of the top 5 earners with the company average, in one row.
**Query:**
```sql
SELECT (SELECT AVG(salary)
        FROM (SELECT salary FROM employees ORDER BY salary DESC LIMIT 5) t) AS avg_top5,
       AVG(salary) AS avg_all
FROM employees;
```
**Explanation:** A scalar subquery computes the top-5 average; the outer AVG covers everyone.

## Q68: Write a query counting, per department, salaried staff located in NY, using FILTER with multiple conditions.
**Query:**
```sql
-- Postgres
SELECT dept_id,
       COUNT(*) FILTER (WHERE salary > 0 AND location = 'NY') AS ny_staff
FROM employees
GROUP BY dept_id;
```
**Explanation:** FILTER accepts any boolean expression; several predicates simply AND together inside the parentheses.

## Q69: Write a query that pivots order counts per status into three separate columns.
**Query:**
```sql
SELECT SUM(CASE WHEN status = 'pending'   THEN 1 ELSE 0 END) AS pending_orders,
       SUM(CASE WHEN status = 'shipped'   THEN 1 ELSE 0 END) AS shipped_orders,
       SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders
FROM orders
WHERE dept_id = 42;
```
**Explanation:** Conditional aggregation turns row-values (status) into column-values — a mini pivot table with no PIVOT syntax.

## Q70: Write a query finding the median salary using Postgres percentile_cont.
**Query:**
```sql
-- Postgres
SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY salary) AS median_salary
FROM employees;
```
**Explanation:** Percentile-based medians interpolate between the middle values for even counts — used here in its aggregate form, no window clause required. `percentile_disc(0.5)` returns an actual member value instead.

## Q71: Write a query finding the median order value using SQL Server PERCENTILE_CONT.
**Query:**
```sql
-- SQL Server
SELECT DISTINCT
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total) OVER () AS median_total
FROM orders;
```
**Explanation:** SQL Server forces an OVER clause; `OVER ()` with `DISTINCT` collapses the repeated analytic result into one row.

## Q72: Write a query finding the median salary with Oracle's MEDIAN function.
**Query:**
```sql
-- Oracle
SELECT MEDIAN(salary) AS median_salary FROM employees;
```
**Explanation:** `MEDIAN` is Oracle's built-in shortcut for the 50th percentile — equivalent to `PERCENTILE_CONT(0.5)`.

## Q73: Write a query computing the median salary in MySQL without percentile or window functions.
**Query:**
```sql
-- MySQL (variable-rownumber trick)
SELECT AVG(salary) AS median_salary
FROM (
  SELECT salary,
         @rownum := @rownum + 1 AS rn,
         @n := (SELECT COUNT(*) FROM employees) AS n
  FROM employees, (SELECT @rownum := 0) r
  ORDER BY salary
) t
WHERE rn IN (FLOOR((n + 1) / 2), CEIL((n + 1) / 2));
```
**Explanation:** Number the sorted rows with a session variable, then average the middle row (odd set) or the two middle rows (even set).
**Alt1:** The elegant LIMIT/OFFSET trick — pick exactly the middle row(s):
```sql
-- MySQL
SELECT AVG(salary) AS median_salary
FROM (
  SELECT salary
  FROM employees
  ORDER BY salary
  LIMIT 2 - ((SELECT COUNT(*) FROM employees) MOD 2)
  OFFSET (SELECT (COUNT(*) - 1) / 2 FROM employees)
) t;
```

## Q74: Write a query computing the median salary per department in MySQL.
**Query:**
```sql
-- MySQL
SELECT dept_id, AVG(salary) AS median_salary
FROM (
  SELECT e.dept_id, e.salary,
         @rn := IF(@d = e.dept_id, @rn + 1, 1) AS rn,
         @d := e.dept_id,
         @cnt := (SELECT COUNT(*) FROM employees d WHERE d.dept_id = e.dept_id) AS cnt
  FROM employees e, (SELECT @rn := 0, @d := NULL) init
  ORDER BY dept_id, salary
) t
WHERE rn IN (FLOOR((cnt + 1) / 2), CEIL((cnt + 1) / 2))
GROUP BY dept_id;
```
**Explanation:** The counter resets whenever the department changes, so each group gets its own row numbers; averaging the middle row(s) per department yields the group median.
**Alt1:** Postgres makes the same problem trivial with an ordered-set aggregate:
```sql
-- Postgres
SELECT dept_id,
       percentile_cont(0.5) WITHIN GROUP (ORDER BY salary) AS median_salary
FROM employees
GROUP BY dept_id;
```

## Q75: Write a query demonstrating the difference between percentile_disc and percentile_cont on the same data.
**Query:**
```sql
-- Postgres
SELECT percentile_disc(0.5) WITHIN GROUP (ORDER BY salary) AS disc_median,
       percentile_cont(0.5) WITHIN GROUP (ORDER BY salary) AS cont_median
FROM employees;
```
**Explanation:** `percentile_disc` returns an actual value present in the data; `percentile_cont` interpolates and can output a value that lies between two rows.
## Q76: Write a query computing the median of DISTINCT salaries only.
**Query:**
```sql
-- Postgres
SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY salary) AS median_distinct_salary
FROM (SELECT DISTINCT salary FROM employees) t;
```
**Explanation:** Deduplicate in a derived table first, then run the percentile — the median of unique values differs from the median of all rows when duplicates exist.
**Alt1:** MySQL variable version over the distinct set:
```sql
-- MySQL
SELECT AVG(salary)
FROM (
  SELECT salary,
         @r := @r + 1 AS rn,
         @n := (SELECT COUNT(DISTINCT salary) FROM employees) AS n
  FROM (SELECT DISTINCT salary FROM employees ORDER BY salary) d,
       (SELECT @r := 0) init
) t
WHERE rn IN (FLOOR((n + 1) / 2), CEIL((n + 1) / 2));
```

## Q77: Write a query showing the 25th and 75th percentiles of order amounts and the interquartile range in one row.
**Query:**
```sql
-- Postgres
SELECT percentile_cont(0.25) WITHIN GROUP (ORDER BY amount) AS p25,
       percentile_cont(0.75) WITHIN GROUP (ORDER BY amount) AS p75,
       percentile_cont(0.75) WITHIN GROUP (ORDER BY amount) -
       percentile_cont(0.25) WITHIN GROUP (ORDER BY amount) AS iqr
FROM orders;
```
**Explanation:** Percentiles quantify spread; their difference is the interquartile range — computed here purely with ordered-set aggregates.

## Q78: Write a query computing the average of only positive amounts and counting the non-positive ones, using FILTER.
**Query:**
```sql
-- Postgres
SELECT AVG(amount)     FILTER (WHERE amount > 0)  AS avg_positive,
       COUNT(*)        FILTER (WHERE amount <= 0) AS non_positive_count
FROM transactions;
```
**Explanation:** Two different aggregates over two different subsets, both computed in a single pass.

## Q79: Write a query that splits sums into inflow and outflow per account.
**Query:**
```sql
SELECT account_id,
       SUM(CASE WHEN amount > 0 THEN amount  ELSE 0 END) AS inflow,
       SUM(CASE WHEN amount < 0 THEN -amount ELSE 0 END) AS outflow
FROM transactions
GROUP BY account_id;
```
**Explanation:** Conditional aggregation buckets by sign and flips negatives positive for the outflow figure.

## Q80: Write a query rounding the average salary per department to two decimals, in each major dialect.
**Query:**
```sql
-- Postgres / MySQL
SELECT dept_id, ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY dept_id;
```
**Alt1:** SQL Server prefers an explicit decimal cast:
```sql
-- SQL Server
SELECT dept_id, CAST(AVG(salary) AS DECIMAL(12, 2)) AS avg_salary
FROM employees
GROUP BY dept_id;
```
**Explanation:** ROUND with a scale is the portable idiom; SQL Server has no ROUND-with-scale-on-aggregate, so the cast does the formatting.

## Q81: Write a query showing, per product line, total units and the units coming from big batches (> 1000 in one line).
**Query:**
```sql
-- Postgres
SELECT product_line,
       SUM(quantity) AS total_units,
       SUM(quantity) FILTER (WHERE quantity > 1000) AS big_batch_units
FROM order_items
GROUP BY product_line;
```
**Explanation:** Two SUMs, one liberal and one gated by FILTER — a partitioning of the same measure inside one query.

## Q82: Write a query finding the department with the most uneven salaries (largest variance).
**Query:**
```sql
-- Postgres / MySQL
SELECT dept_id, VARIANCE(salary) AS var_salary
FROM employees
GROUP BY dept_id
ORDER BY var_salary DESC
LIMIT 1;
```
**Explanation:** Aggregate the spread metric, sort by it, keep the top group.

## Q83: Write a query computing, per employee, (a) the sum of three score columns and (b) the average of those three columns.
**Query:**
```sql
SELECT employee_id,
       score1 + score2 + score3 AS total_score,
       (score1 + score2 + score3) / 3.0 AS avg_score
FROM reviews;
```
**Explanation:** Row-wise "aggregates" are plain arithmetic — but a single NULL in any score NULLs the whole row, so COALESCE each column if that matters.

## Q84: Write a query to find every city that more than one employee lives in, and how many live there.
**Query:**
```sql
SELECT city, COUNT(*) AS employees
FROM employees
GROUP BY city
HAVING COUNT(*) > 1;
```
**Explanation:** GROUP BY collapses to cities and HAVING keeps only duplicated ones — the minimal answer to "who is not alone".

## Q85: Write a query demonstrating what each aggregate returns over an empty result set.
**Query:**
```sql
SELECT COUNT(*) AS rows_,
       SUM(x) AS sum_x,
       AVG(x) AS avg_x,
       MAX(x) AS max_x
FROM (SELECT 1 AS x WHERE 1 = 0) t;
```
**Explanation:** COUNT returns 0; SUM/AVG/MIN/MAX return NULL. Production code typically wraps the latter in COALESCE.

## Q86: Write a query reporting each category's revenue with a grand-total footer row added by ROLLUP.
**Query:**
```sql
-- Postgres
SELECT COALESCE(category, 'TOTAL') AS category,
       SUM(revenue) AS revenue
FROM products
GROUP BY ROLLUP(category);
```
**Explanation:** ROLLUP appends a grand-total row (category becomes NULL) — one statement replaces a UNION of two aggregates.
**Alt1:** MySQL:
```sql
-- MySQL
SELECT category, SUM(revenue) AS revenue
FROM products
GROUP BY category WITH ROLLUP;
```

## Q87: Write a query returning per-year salary totals, the grand total, and each year's share of it.
**Query:**
```sql
-- Postgres
SELECT EXTRACT(YEAR FROM hire_date) AS yr,
       SUM(e.salary) AS total,
       ROUND(SUM(e.salary) * 100.0 / t.overall, 2) AS pct
FROM employees e
CROSS JOIN (SELECT SUM(salary) AS overall FROM employees) t
GROUP BY yr, t.overall
ORDER BY yr;
```
**Explanation:** The scalar total replicates onto every group via CROSS JOIN, so each group can compare against the whole — window-free percentages.

## Q88: Write a query finding the most common first letter of employee first names.
**Query:**
```sql
SELECT LEFT(name, 1) AS first_letter, COUNT(*) AS freq
FROM employees
GROUP BY LEFT(name, 1)
ORDER BY freq DESC
LIMIT 1;
```
**Explanation:** Bucket rows with a scalar function, group by the derived key, sort by frequency — the mode recipe applied to a computed key.
**Alt1:** Postgres SUBSTRING variant:
```sql
-- Postgres
SELECT SUBSTRING(name FROM 1 FOR 1) AS first_letter, COUNT(*) AS freq
FROM employees
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1;
```

## Q89: Write a query computing three distinct counts over overlapping subsets in one statement.
**Query:**
```sql
SELECT COUNT(DISTINCT o.customer_id) AS customers,
       COUNT(DISTINCT oi.product_id)  AS products,
       COUNT(*)                       AS rows
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id;
```
**Explanation:** Three different granularities summarized in a single scan of the joined rows.

## Q90: Write a query that filters groups by their aggregate — and explain the error you get if the aggregate goes in WHERE.
**Query:**
```sql
-- This is WRONG and errors out in most engines:
-- SELECT dept_id FROM employees WHERE COUNT(*) > 3 GROUP BY dept_id;
SELECT dept_id
FROM employees
GROUP BY dept_id
HAVING COUNT(*) > 3;
```
**Explanation:** WHERE runs row-by-row before grouping and can't see aggregates; HAVING runs after grouping and can. Put group filters in HAVING (or wrap in a derived table).
**Alt1:** Derived-table filtering:
```sql
SELECT dept_id FROM (
  SELECT dept_id FROM employees GROUP BY dept_id HAVING COUNT(*) > 3
) t;
```

## Q91: Write a query keeping only regions whose revenue share exceeds 10% of the total.
**Query:**
```sql
SELECT region, SUM(revenue) AS rev
FROM sales
GROUP BY region
HAVING SUM(revenue) > (SELECT 0.10 * SUM(revenue) FROM sales);
```
**Explanation:** HAVING compares each group's SUM against a scalar subquery — a share filter with no window functions.

## Q92: Write a query counting new and returning customers per month in one pass with FILTER.
**Query:**
```sql
-- Postgres
SELECT DATE_TRUNC('month', order_date) AS mon,
       COUNT(*) FILTER (WHERE signup_date = order_date) AS new_customers,
       COUNT(*) FILTER (WHERE signup_date < order_date) AS returning_customers
FROM orders
GROUP BY mon
ORDER BY mon;
```
**Explanation:** Two FILTERed COUNTs partition each group by a predicate — one scan produces two analytical buckets.

## Q93: Write a query to find the customer with the most large (> $500) orders, using SUM(CASE ...).
**Query:**
```sql
SELECT customer_id,
       SUM(CASE WHEN amount > 500 THEN 1 ELSE 0 END) AS big_orders
FROM orders
GROUP BY customer_id
ORDER BY big_orders DESC
LIMIT 1;
```
**Explanation:** Conditional SUM counts qualifying rows per group, then ordering + LIMIT picks the winner.

## Q94: Write a query computing per-department 25th and 75th salary percentiles.
**Query:**
```sql
-- Postgres
SELECT dept_id,
       percentile_cont(0.25) WITHIN GROUP (ORDER BY salary) AS q1,
       percentile_cont(0.75) WITHIN GROUP (ORDER BY salary) AS q3
FROM employees
GROUP BY dept_id;
```
**Explanation:** Ordered-set percentiles are just aggregates, so they slot naturally into a GROUP BY to describe each department's spread.

## Q95: Write a query counting active vs inactive users per signup source.
**Query:**
```sql
-- Postgres
SELECT source,
       COUNT(*) FILTER (WHERE is_active)    AS active_users,
       COUNT(*) FILTER (WHERE NOT is_active) AS inactive_users
FROM users
GROUP BY source;
```
**Alt1:** Universal CASE version:
```sql
SELECT source,
       SUM(CASE WHEN is_active THEN 1 ELSE 0 END) AS active_users,
       SUM(CASE WHEN NOT is_active THEN 1 ELSE 0 END) AS inactive_users
FROM users
GROUP BY source;
```
**Explanation:** Two identical recipes for a two-way breakdown — FILTER (Postgres) and SUM(CASE) (everywhere) yield the same numbers.

## Q96: Write a query counting employees hired per calendar quarter.
**Query:**
```sql
-- Postgres
SELECT EXTRACT(YEAR FROM hire_date) AS yr,
       EXTRACT(QUARTER FROM hire_date) AS qrt,
       COUNT(*) AS hires
FROM employees
GROUP BY yr, qrt
ORDER BY yr, qrt;
```
**Alt1:** MySQL:
```sql
-- MySQL
SELECT YEAR(hire_date) AS yr, QUARTER(hire_date) AS qrt, COUNT(*) AS hires
FROM employees
GROUP BY YEAR(hire_date), QUARTER(hire_date);
```

## Q97: Write a query bucketing employees into salary bands and counting each band.
**Query:**
```sql
SELECT CASE
         WHEN salary < 50000    THEN 'low'
         WHEN salary < 100000   THEN 'mid'
         WHEN salary < 200000   THEN 'high'
         ELSE 'executive'
       END AS band,
       COUNT(*) AS headcount
FROM employees
GROUP BY 1
ORDER BY MIN(salary);
```
**Explanation:** Bucket with a CASE key, group by it, and order by MIN(salary) so bands naturally print in ascending order.

## Q98: Write a query computing the average age and the oldest/newest hire per team.
**Query:**
```sql
-- Postgres
SELECT team_id,
       AVG(EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM birth_date)) AS avg_age,
       MIN(hire_date) AS oldest_hire,
       MAX(hire_date) AS newest_hire
FROM employees
GROUP BY team_id;
```
**Alt1:** SQL Server:
```sql
-- SQL Server
SELECT team_id,
       AVG(DATEDIFF(year, birth_date, GETDATE())) AS avg_age,
       MIN(hire_date) AS oldest_hire,
       MAX(hire_date) AS newest_hire
FROM employees
GROUP BY team_id;
```
**Explanation:** AVG of an age expression plus MIN/MAX on dates — three summary metrics over identical groups.

## Q99: Write a single department-dashboard query: headcount, payroll, average, top salary, name list, and median salary per department.
**Query:**
```sql
-- Postgres
SELECT e.dept_id,
       COUNT(*) AS headcount,
       SUM(e.salary) AS payroll,
       ROUND(AVG(e.salary), 2) AS avg_salary,
       MAX(e.salary) AS top_salary,
       STRING_AGG(e.name, ', ' ORDER BY e.salary DESC) AS by_salary,
       percentile_cont(0.5) WITHIN GROUP (ORDER BY e.salary) AS median_salary
FROM employees e
GROUP BY e.dept_id
ORDER BY payroll DESC;
```
**Explanation:** Six different aggregates — count, sum, average, extreme, concatenation and an ordered-set percentile — over the same groups in one statement.
**Alt1:** MySQL version (no percentile, swaps in GROUP_CONCAT):
```sql
-- MySQL
SELECT dept_id,
       COUNT(*) AS headcount,
       SUM(salary) AS payroll,
       ROUND(AVG(salary), 2) AS avg_salary,
       MAX(salary) AS top_salary,
       GROUP_CONCAT(name ORDER BY salary DESC SEPARATOR ', ') AS by_salary
FROM employees
GROUP BY dept_id
ORDER BY payroll DESC;
```

## Q100: Final challenge — one query computing, per employee, department headcount, the department's share of company headcount and payroll, the gap to the department's top earner, and the employee's share of department payroll, all NULL-safe.
**Query:**
```sql
SELECT e.name,
       e.dept_id,
       d.cnt,
       ROUND(d.cnt * 100.0 / t.headcount, 2) AS pct_of_headcount,
       ROUND(d.payroll * 100.0 / t.payroll, 2) AS pct_of_payroll,
       d.max_salary - e.salary AS gap_to_top,
       COALESCE(ROUND(e.salary * 100.0 / NULLIF(d.payroll, 0), 2), 0) AS pct_of_dept
FROM employees e
JOIN (SELECT dept_id, COUNT(*) AS cnt, SUM(salary) AS payroll, MAX(salary) AS max_salary
      FROM employees GROUP BY dept_id) d ON d.dept_id = e.dept_id
CROSS JOIN (SELECT COUNT(*) AS headcount, SUM(salary) AS payroll FROM employees) t
ORDER BY d.payroll DESC, gap_to_top;
```
**Explanation:** Every figure is built from basic aggregates plus derived joins — shares, percentages, gaps. `NULLIF` guards division by zero and `COALESCE` tames NULLs, the two constant companions of aggregation.
