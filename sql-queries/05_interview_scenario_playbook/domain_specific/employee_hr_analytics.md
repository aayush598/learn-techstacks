# Employee and HR Analytics SQL Scenarios — 100 Interview Q&A

> **Schema Reference**
> - `employees(emp_id, name, dept_id, salary, manager_id, hire_date, gender, county, left_date)`
> - `departments(dept_id, dept_name, location)`
> - `attendance(emp_id, date, status)` — status ∈ {present, absent, leave, work_from_home}
> - `leave_records(emp_id, leave_type, start_date, end_date)`
> - `promotions(emp_id, old_title, new_title, promo_date, old_salary, new_salary)`
> - `performance_reviews(emp_id, review_date, score, reviewer_id)`
> - `payroll(emp_id, pay_period, base_salary, bonus, deduction, net_pay)`
> - `department_transfers(emp_id, from_dept_id, to_dept_id, transfer_date)`

---

## Q1: Total employee count per department

**Schema hint:** `employees(dept_id)`, `departments(dept_id, dept_name)`

```sql
SELECT d.dept_name,
       COUNT(e.emp_id) AS employee_count
  FROM departments d
  LEFT JOIN employees e ON e.dept_id = d.dept_id
 GROUP BY d.dept_name
 ORDER BY employee_count DESC;
```

**Explanation:** A LEFT JOIN ensures departments with zero employees still appear. GROUP BY aggregates per department.

**Alt1:**
```sql
-- MySQL
SELECT d.dept_name,
       COUNT(e.emp_id) AS employee_count
  FROM employees e
  RIGHT JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name
 ORDER BY employee_count DESC;
```
**Explanation:** RIGHT JOIN is the mirror of the LEFT JOIN spell — both preserve zero-headcount departments.

---

## Q2: Average salary per department, sorted descending

**Schema hint:** `employees(dept_id, salary)`, `departments(dept_name)`

```sql
SELECT d.dept_name,
       ROUND(AVG(e.salary), 2) AS avg_salary
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name
 ORDER BY avg_salary DESC;
```

**Explanation:** INNER JOIN excludes orphan dept_ids. AVG with ROUND provides a clean monetary figure.

**Alt1:**
```sql
-- SQL Server
SELECT d.dept_name,
       CAST(AVG(e.salary) AS DECIMAL(10,2)) AS avg_salary
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name
 ORDER BY avg_salary DESC;
```
**Explanation:** CAST to DECIMAL(10,2) rounds the average in SQL Server and keeps the sort key numeric.

---

## Q3: Min, Max, and Avg salary per department in one pass

**Schema hint:** `employees(dept_id, salary)`

```sql
SELECT d.dept_name,
       MIN(e.salary)  AS min_salary,
       MAX(e.salary)  AS max_salary,
       ROUND(AVG(e.salary), 2) AS avg_salary
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name;
```

**Explanation:** Multiple aggregate functions in a single GROUP BY avoid redundant table scans.

---

## Q4: Median salary per department — MySQL 8+

**Schema hint:** `employees(dept_id, salary)`

```sql
-- MySQL
SELECT d.dept_name,
       ROUND(AVG(e.salary), 2) AS median_salary
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
  JOIN (
    SELECT dept_id, salary,
           ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary) AS rn,
           COUNT(*) OVER (PARTITION BY dept_id) AS cnt
      FROM employees
  ) ranked ON ranked.dept_id = e.dept_id
 WHERE ranked.rn IN (FLOOR((cnt + 1) / 2), CEIL((cnt + 1) / 2))
 GROUP BY d.dept_name;
```

**Explanation:** Window functions ROW_NUMBER and COUNT partition by department. We pick the middle row(s) and average them for an even-count median.

**Alt1:**
```sql
-- PostgreSQL
SELECT d.dept_name,
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY e.salary) AS median_salary
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name;
```
**Explanation:** PERCENTILE_CONT computes the median natively — no manual row counting or window bookkeeping.

---

## Q5: Median salary per department — PostgreSQL

**Schema hint:** `employees(dept_id, salary)`

```sql
-- PostgreSQL
SELECT d.dept_name,
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY e.salary) AS median_salary
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name;
```

**Explanation:** PERCENTILE_CONT is a built-in ordered-set aggregate that computes the continuous median in PostgreSQL natively.

**Alt1:**
```sql
-- Oracle
SELECT d.dept_name,
       MEDIAN(e.salary) AS median_salary
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name;
```
**Explanation:** Oracle ships a dedicated MEDIAN aggregate — the shortest possible median spell.

---

## Q6: Employees earning above their department average

**Schema hint:** `employees(dept_id, salary, name)`

```sql
SELECT e.name, e.salary, d.dept_name
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
 WHERE e.salary > (
       SELECT AVG(e2.salary)
         FROM employees e2
        WHERE e2.dept_id = e.dept_id
       );
```

**Explanation:** A correlated subquery computes the per-department average for each row, filtering those above it.

**Alt1:**
```sql
-- PostgreSQL
WITH dept_avg AS (
  SELECT emp_id, dept_id, salary,
         AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg_salary
    FROM employees
)
SELECT e.name, e.salary, d.dept_name
  FROM dept_avg e
  JOIN departments d ON d.dept_id = e.dept_id
 WHERE e.salary > e.dept_avg_salary;
```
**Explanation:** AVG OVER (PARTITION BY) computes the department mean in a single scan, avoiding the correlated subquery.

---

## Q7: Employees who earn more than their own manager

**Schema hint:** `employees(emp_id, name, salary, manager_id)`

```sql
SELECT e.name    AS employee_name,
       e.salary  AS employee_salary,
       m.name    AS manager_name,
       m.salary  AS manager_salary
  FROM employees e
  JOIN employees m ON m.emp_id = e.manager_id
 WHERE e.salary > m.salary;
```

**Explanation:** A self-join links each employee to their manager. The WHERE clause filters salary inversions.

**Alt1:**
```sql
SELECT e.name AS employee_name, e.salary,
       m.name AS manager_name, m.salary AS manager_salary,
       ROUND(e.salary * 100.0 / m.salary, 2) AS comp_ratio_pct
  FROM employees e
  JOIN employees m ON m.emp_id = e.manager_id
 WHERE e.salary > m.salary;
```
**Explanation:** Extending with a comp-ratio column quantifies exactly how far the inversion extends above 100%.

---

## Q8: Manager-to-reportee ratio per department

**Schema hint:** `employees(emp_id, dept_id, manager_id)`

```sql
SELECT d.dept_name,
       COUNT(CASE WHEN m.emp_id IS NOT NULL THEN 1 END) AS manager_count,
       COUNT(CASE WHEN e.manager_id IS NOT NULL THEN 1 END) AS reportee_count,
       ROUND(
         COUNT(CASE WHEN e.manager_id IS NOT NULL THEN 1 END) * 1.0
         / NULLIF(COUNT(CASE WHEN m.emp_id IS NOT NULL THEN 1 END), 0),
       2) AS reports_per_manager
  FROM departments d
  LEFT JOIN employees e ON e.dept_id = d.dept_id
  LEFT JOIN employees m ON m.emp_id = e.manager_id AND m.dept_id = d.dept_id
 GROUP BY d.dept_name;
```

**Explanation:** Conditional COUNTs separate managers from reportees. NULLIF prevents division by zero.

---

## Q9: Tenure in years for each employee (hire date to today)

**Schema hint:** `employees(hire_date)`

```sql
-- MySQL
SELECT name,
       hire_date,
       TIMESTAMPDIFF(YEAR, hire_date, CURDATE()) AS tenure_years
  FROM employees
 ORDER BY tenure_years DESC;
```

**Explanation:** TIMESTAMPDIFF computes the difference in calendar years between hire_date and today in MySQL.

**Alt1:**
```sql
-- PostgreSQL
SELECT name, hire_date,
       EXTRACT(YEAR FROM AGE(CURRENT_DATE, hire_date)) AS tenure_years
  FROM employees
 ORDER BY tenure_years DESC;
```
**Explanation:** AGE() yields an interval; EXTRACT(YEAR) pulls whole years — identical result to TIMESTAMPDIFF.

---

## Q10: Tenure distribution bucketed into ranges

**Schema hint:** `employees(hire_date)`

```sql
-- PostgreSQL
SELECT CASE
         WHEN AGE(CURRENT_DATE, hire_date) < INTERVAL '1 year'  THEN '0-1 yrs'
         WHEN AGE(CURRENT_DATE, hire_date) < INTERVAL '3 years' THEN '1-3 yrs'
         WHEN AGE(CURRENT_DATE, hire_date) < INTERVAL '5 years' THEN '3-5 yrs'
         WHEN AGE(CURRENT_DATE, hire_date) < INTERVAL '10 years' THEN '5-10 yrs'
         ELSE '10+ yrs'
       END AS tenure_bucket,
       COUNT(*) AS headcount
  FROM employees
 GROUP BY tenure_bucket
 ORDER BY MIN(AGE(CURRENT_DATE, hire_date));
```

**Explanation:** AGE() in PostgreSQL computes an interval; CASE buckets it into human-readable ranges.

---

## Q11: Number of employees hired each year

**Schema hint:** `employees(hire_date)`

```sql
SELECT YEAR(hire_date)  AS hire_year,
       COUNT(*)          AS hires
  FROM employees
 GROUP BY hire_year
 ORDER BY hire_year;
```

**Explanation:** YEAR() extracts the calendar year. GROUP BY produces one row per year.

**Alt1:**
```sql
-- SQL Server
SELECT YEAR(hire_date) AS hire_year,
       COUNT(*) AS hires
  FROM employees
 GROUP BY YEAR(hire_date)
 ORDER BY hire_year;
```
**Explanation:** YEAR() behaves identically in MySQL and SQL Server; the only adjustment is grouping on the expression itself.

---

## Q12: Employees hired each month within a specific year

**Schema hint:** `employees(hire_date)`

```sql
-- SQL Server
SELECT MONTH(e.hire_date)  AS hire_month,
       DATENAME(MONTH, e.hire_date) AS month_name,
       COUNT(*) AS hires
  FROM employees e
 WHERE YEAR(e.hire_date) = 2024
 GROUP BY MONTH(e.hire_date), DATENAME(MONTH, e.hire_date)
 ORDER BY hire_month;
```

**Explanation:** DATENAME returns the month name for readability. Filter on a specific year first.

---

## Q13: Monthly headcount change trend (running total of hires minus exits)

**Schema hint:** `employees(hire_date, left_date)`

```sql
-- PostgreSQL
WITH monthly_events AS (
  SELECT DATE_TRUNC('month', hire_date) AS event_month,
         1 AS delta
    FROM employees
   UNION ALL
  SELECT DATE_TRUNC('month', left_date) AS event_month,
         -1 AS delta
    FROM employees
   WHERE left_date IS NOT NULL
)
SELECT event_month,
       SUM(delta) OVER (ORDER BY event_month
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_headcount
  FROM monthly_events
 ORDER BY event_month;
```

**Explanation:** Hires (+1) and exits (−1) are unioned. A cumulative SUM window function tracks headcount over time.

---

## Q14: Attrition — employees who have left (left_date IS NOT NULL)

**Schema hint:** `employees(left_date)`

```sql
SELECT name, hire_date, left_date,
       DATEDIFF(left_date, hire_date) AS days_employed
  FROM employees
 WHERE left_date IS NOT NULL
 ORDER BY days_employed;
```

**Explanation:** A non-null left_date signals the employee has separated from the company.

**Alt1:**
```sql
-- SQL Server
SELECT name, hire_date, left_date,
       DATEDIFF(DAY, hire_date, left_date) AS days_employed
  FROM employees
 WHERE left_date IS NOT NULL
 ORDER BY days_employed;
```
**Explanation:** SQL Server requires the datepart unit — DAY — as the first DATEDIFF argument.

---

## Q15: Attrition rate per department

**Schema hint:** `employees(dept_id, left_date)`

```sql
-- MySQL
SELECT d.dept_name,
       COUNT(CASE WHEN e.left_date IS NOT NULL THEN 1 END) AS departed,
       COUNT(*) AS total,
       ROUND(
         COUNT(CASE WHEN e.left_date IS NOT NULL THEN 1 END) * 100.0 / COUNT(*),
       2) AS attrition_pct
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name
 ORDER BY attrition_pct DESC;
```

**Explanation:** Conditional COUNT counts only departed employees; dividing by total gives the rate.

**Alt1:**
```sql
-- PostgreSQL
SELECT dept_name,
       COUNT(*) FILTER (WHERE left_date IS NOT NULL) AS departed,
       COUNT(*) AS total,
       ROUND(COUNT(*) FILTER (WHERE left_date IS NOT NULL) * 100.0 / COUNT(*), 2) AS attrition_pct
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY dept_name
 ORDER BY attrition_pct DESC;
```
**Explanation:** PostgreSQL's FILTER clause keeps the conditional count inline and readable instead of a CASE.

---

## Q16: Attrition rate bucketed by tenure range

**Schema hint:** `employees(hire_date, left_date)`

```sql
-- PostgreSQL
WITH tenure_buckets AS (
  SELECT *,
       CASE
         WHEN AGE(COALESCE(left_date, CURRENT_DATE), hire_date) < INTERVAL '1 year'  THEN '0-1'
         WHEN AGE(COALESCE(left_date, CURRENT_DATE), hire_date) < INTERVAL '3 years' THEN '1-3'
         WHEN AGE(COALESCE(left_date, CURRENT_DATE), hire_date) < INTERVAL '5 years' THEN '3-5'
         ELSE '5+'
       END AS tenure_bucket,
       CASE WHEN left_date IS NOT NULL THEN 1 ELSE 0 END AS has_left
    FROM employees
)
SELECT tenure_bucket,
       SUM(has_left) AS departed,
       COUNT(*)      AS total,
       ROUND(SUM(has_left) * 100.0 / COUNT(*), 2) AS attrition_pct
  FROM tenure_buckets
 GROUP BY tenure_bucket
 ORDER BY MIN(AGE(COALESCE(left_date, CURRENT_DATE), hire_date));
```

**Explanation:** Employees are bucketed by tenure; within each bucket the departure ratio is calculated.

**Alt1:**
```sql
-- PostgreSQL
SELECT CASE
         WHEN DATE_PART('year', COALESCE(left_date, CURRENT_DATE)) - DATE_PART('year', hire_date) < 1 THEN '0-1'
         WHEN DATE_PART('year', COALESCE(left_date, CURRENT_DATE)) - DATE_PART('year', hire_date) < 3 THEN '1-3'
         WHEN DATE_PART('year', COALESCE(left_date, CURRENT_DATE)) - DATE_PART('year', hire_date) < 5 THEN '3-5'
         ELSE '5+'
       END AS tenure_bucket,
       COUNT(*) FILTER (WHERE left_date IS NOT NULL) AS departed,
       COUNT(*) AS total,
       ROUND(COUNT(*) FILTER (WHERE left_date IS NOT NULL) * 100.0 / COUNT(*), 2) AS attrition_pct
  FROM employees
 GROUP BY tenure_bucket
 ORDER BY MIN(DATE_PART('year', COALESCE(left_date, CURRENT_DATE)) - DATE_PART('year', hire_date));
```
**Explanation:** DATE_PART year subtraction avoids interval math entirely and orders buckets chronologically.

---

## Q17: Employees hired in the last 30 days

**Schema hint:** `employees(hire_date)`

```sql
SELECT emp_id, name, hire_date
  FROM employees
 WHERE hire_date >= CURRENT_DATE - INTERVAL '30 days';
```

**Explanation:** Date arithmetic filters recent hires. Interval syntax is PostgreSQL-standard; adjust for other dialects.

---

## Q18: Salary statistics (avg, min, max, stddev) per department

**Schema hint:** `employees(dept_id, salary)`

```sql
SELECT d.dept_name,
       COUNT(*) AS headcount,
       ROUND(AVG(e.salary), 2)    AS avg_sal,
       MIN(e.salary)              AS min_sal,
       MAX(e.salary)              AS max_sal,
       ROUND(STDDEV(e.salary), 2) AS stddev_sal
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name;
```

**Explanation:** STDDEV reveals salary spread; departments with high stddev may have pay equity concerns.

**Alt1:**
```sql
-- SQL Server
SELECT d.dept_name,
       COUNT(*) AS headcount,
       AVG(e.salary) AS avg_sal,
       MIN(e.salary) AS min_sal,
       MAX(e.salary) AS max_sal,
       STDEV(e.salary) AS salary_stddev
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name;
```
**Explanation:** STDEV is SQL Server's sample standard deviation, the exact analogue of PostgreSQL's STDDEV.

---

## Q19: Top 3 highest-paid employees per department

**Schema hint:** `employees(dept_id, salary, name)`

```sql
SELECT dept_name, name, salary
  FROM (
    SELECT d.dept_name, e.name, e.salary,
           ROW_NUMBER() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS rn
      FROM employees e
      JOIN departments d ON d.dept_id = e.dept_id
  ) ranked
 WHERE rn <= 3
 ORDER BY dept_name, rn;
```

**Explanation:** ROW_NUMBER assigns a rank within each department. Filtering rn <= 3 yields the top three.

---

## Q20: Employees with no direct reports (leaf nodes in org chart)

**Schema hint:** `employees(emp_id, manager_id)`

```sql
SELECT e.emp_id, e.name
  FROM employees e
 WHERE NOT EXISTS (
       SELECT 1
         FROM employees sub
        WHERE sub.manager_id = e.emp_id
       );
```

**Explanation:** NOT EXISTS checks that no other employee references this emp_id as their manager.

**Alt1:**
```sql
SELECT e.emp_id, e.name
  FROM employees e
  LEFT JOIN employees r ON r.manager_id = e.emp_id
 WHERE r.emp_id IS NULL;
```
**Explanation:** A LEFT JOIN that yields only NULL right-side rows is the classic anti-join — same result as NOT EXISTS.

---

## Q21: Department with the highest average salary

**Schema hint:** `employees(dept_id, salary)`, `departments(dept_name)`

```sql
SELECT d.dept_name,
       ROUND(AVG(e.salary), 2) AS avg_salary
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name
 ORDER BY avg_salary DESC
 LIMIT 1;
```

**Explanation:** ORDER BY DESC with LIMIT 1 picks the single highest average.

---

## Q22: Salary bands (Low / Mid / High) based on global percentiles

**Schema hint:** `employees(salary, name)`

```sql
-- Oracle
SELECT name, salary,
       CASE
         WHEN salary <= NTILE(4) OVER (ORDER BY salary) THEN 'Low'
         WHEN salary <= NTILE(4) OVER (ORDER BY salary) * 2 THEN 'Mid'
         ELSE 'High'
       END AS salary_band
  FROM employees;
```

**Explanation:** This simplified version is shown for reference. The proper Oracle approach uses PERCENTILE_CONT:

```sql
-- Oracle (correct)
WITH percentiles AS (
  SELECT emp_id, name, salary,
         PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY salary) OVER () AS p25,
         PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY salary) OVER () AS p75
    FROM employees
)
SELECT name, salary,
       CASE
         WHEN salary <= p25 THEN 'Low'
         WHEN salary <= p75 THEN 'Mid'
         ELSE 'High'
       END AS salary_band
  FROM percentiles;
```

**Explanation:** PERCENTILE_CONT computes the 25th and 75th percentiles; CASE assigns each employee a band.

---

## Q23: Employees who joined in the same month as their manager

**Schema hint:** `employees(hire_date, manager_id)`

```sql
SELECT e.name AS employee, m.name AS manager,
       e.hire_date AS emp_hire, m.hire_date AS mgr_hire
  FROM employees e
  JOIN employees m ON m.emp_id = e.manager_id
 WHERE YEAR(e.hire_date)  = YEAR(m.hire_date)
   AND MONTH(e.hire_date) = MONTH(m.hire_date);
```

**Explanation:** Comparing year and month of both hire dates identifies coincidental co-hiring.

---

## Q24: Count of employees per gender per department

**Schema hint:** `employees(dept_id, gender)`

```sql
SELECT d.dept_name,
       SUM(CASE WHEN e.gender = 'M' THEN 1 ELSE 0 END) AS male_count,
       SUM(CASE WHEN e.gender = 'F' THEN 1 ELSE 0 END) AS female_count,
       SUM(CASE WHEN e.gender NOT IN ('M','F') THEN 1 ELSE 0 END) AS other_count
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name;
```

**Explanation:** Conditional SUM acts as a manual pivot to produce gender columns per department.

---

## Q25: Duplicate employee records (same name and hire_date)

**Schema hint:** `employees(name, hire_date)`

```sql
SELECT name, hire_date, COUNT(*) AS occurrence
  FROM employees
 GROUP BY name, hire_date
HAVING COUNT(*) > 1
 ORDER BY occurrence DESC;
```

**Explanation:** GROUP BY with HAVING COUNT > 1 identifies exact duplicates — a common data-quality check.

---

## Q26: Manager with the most direct reports

**Schema hint:** `employees(emp_id, manager_id)`

```sql
SELECT m.name AS manager_name,
       COUNT(e.emp_id) AS direct_reports
  FROM employees m
  JOIN employees e ON e.manager_id = m.emp_id
 GROUP BY m.emp_id, m.name
 ORDER BY direct_reports DESC
 LIMIT 1;
```

**Explanation:** Joining employees to themselves on manager_id and counting yields the span of control per manager.

**Alt1:**
```sql
WITH report_counts AS (
  SELECT manager_id, COUNT(*) AS direct_reports
    FROM employees
   WHERE manager_id IS NOT NULL
   GROUP BY manager_id
)
SELECT e.name AS manager_name, rc.direct_reports
  FROM report_counts rc
  JOIN employees e ON e.emp_id = rc.manager_id
 ORDER BY rc.direct_reports DESC
 LIMIT 1;
```
**Explanation:** Pre-aggregating counts then joining the manager table avoids the double self-join.

---

## Q27: Full org-chart ancestry path (recursive CTE) — MySQL 8+

**Schema hint:** `employees(emp_id, name, manager_id)`

```sql
-- MySQL
WITH RECURSIVE org_path AS (
  SELECT emp_id, name, manager_id,
         CAST(name AS CHAR(1000)) AS path
    FROM employees
   WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, e.name, e.manager_id,
         CONCAT(op.path, ' > ', e.name)
    FROM employees e
    JOIN org_path op ON op.emp_id = e.manager_id
)
SELECT emp_id, name, path
  FROM org_path
 ORDER BY path;
```

**Explanation:** The anchor selects top-of-tree (null manager); the recursive leg concatenates the path downward.

**Alt1:**
```sql
-- SQL Server
WITH org_path AS (
  SELECT emp_id, name, manager_id,
         CAST(name AS VARCHAR(MAX)) AS path
    FROM employees
   WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, e.name, e.manager_id,
         CAST(op.path + ' > ' + e.name AS VARCHAR(MAX))
    FROM employees e
    JOIN org_path op ON op.emp_id = e.manager_id
)
SELECT emp_id, name, path
  FROM org_path
 ORDER BY path;
```
**Explanation:** SQL Server concatenates the path with the + operator and VARCHAR(MAX) instead of CONCAT.

---

## Q28: Descendant count per manager (recursive)

**Schema hint:** `employees(emp_id, name, manager_id)`

```sql
-- PostgreSQL
WITH RECURSIVE descendants AS (
  SELECT emp_id AS manager_id, emp_id, 1 AS depth
    FROM employees
  UNION ALL
  SELECT d.manager_id, e.emp_id, d.depth + 1
    FROM descendants d
    JOIN employees e ON e.manager_id = d.emp_id
   WHERE d.emp_id != d.manager_id
)
SELECT manager_id,
       COUNT(*) - 1 AS descendant_count
  FROM descendants
 GROUP BY manager_id
HAVING COUNT(*) - 1 > 0
 ORDER BY descendant_count DESC;
```

**Explanation:** The recursive CTE walks from each employee downward. Grouping by manager_id and subtracting 1 (self) gives the total sub-tree size.

---

## Q29: Depth of each employee in the org tree

**Schema hint:** `employees(emp_id, name, manager_id)`

```sql
-- SQL Server
WITH RECURSIVE org_depth AS (
  SELECT emp_id, name, manager_id, 0 AS depth
    FROM employees
   WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, e.name, e.manager_id, od.depth + 1
    FROM employees e
    JOIN org_depth od ON od.emp_id = e.manager_id
)
SELECT emp_id, name, depth
  FROM org_depth
 ORDER BY depth, name;
```

**Explanation:** The depth counter increments at each recursive level, showing how far each person sits from the CEO.

---

## Q30: Employees at depth 2 (skip-level reporting)

**Schema hint:** `employees(emp_id, manager_id)`

```sql
WITH RECURSIVE org_depth AS (
  SELECT emp_id, name, manager_id, 0 AS depth
    FROM employees
   WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, e.name, e.manager_id, od.depth + 1
    FROM employees e
    JOIN org_depth od ON od.emp_id = e.manager_id
)
SELECT emp_id, name
  FROM org_depth
 WHERE depth = 2;
```

**Explanation:** Depth 2 means two levels below the root — useful for skip-level meeting planning.

---

## Q31: Promotion chain — current title level per employee

**Schema hint:** `promotions(emp_id, new_title, promo_date)`

```sql
-- PostgreSQL
WITH latest_promo AS (
  SELECT DISTINCT ON (emp_id)
         emp_id, new_title, promo_date
    FROM promotions
   ORDER BY emp_id, promo_date DESC
)
SELECT e.emp_id, e.name, COALESCE(lp.new_title, 'Junior') AS current_title
  FROM employees e
  LEFT JOIN latest_promo lp ON lp.emp_id = e.emp_id;
```

**Explanation:** DISTINCT ON (PostgreSQL) picks the most recent promotion per employee. LEFT JOIN covers employees with no promotions.

**Alt1:**
```sql
WITH latest_promo AS (
  SELECT emp_id, new_title, promo_date,
         ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY promo_date DESC) AS rn
    FROM promotions
)
SELECT e.emp_id, e.name,
       COALESCE(lp.new_title, 'Junior') AS current_title
  FROM employees e
  LEFT JOIN latest_promo lp ON lp.emp_id = e.emp_id AND lp.rn = 1;
```
**Explanation:** ROW_NUMBER = 1 per employee reproduces DISTINCT ON and works in every major dialect.

---

## Q32: Average days to first promotion

**Schema hint:** `employees(hire_date)`, `promotions(emp_id, promo_date)`

```sql
-- MySQL
SELECT ROUND(AVG(DATEDIFF(p.promo_date, e.hire_date)), 0) AS avg_days_to_first_promo
  FROM employees e
  JOIN (
    SELECT emp_id, MIN(promo_date) AS promo_date
      FROM promotions
     GROUP BY emp_id
  ) p ON p.emp_id = e.emp_id;
```

**Explanation:** MIN(promo_date) identifies the first promotion; DATEDIFF computes days from hire.

---

## Q33: Employees promoted more than once

**Schema hint:** `promotions(emp_id)`

```sql
SELECT e.emp_id, e.name, COUNT(*) AS promo_count
  FROM promotions p
  JOIN employees e ON e.emp_id = p.emp_id
 GROUP BY e.emp_id, e.name
HAVING COUNT(*) > 1
 ORDER BY promo_count DESC;
```

**Explanation:** COUNT of promotion records per employee, filtered by HAVING, surfaces repeat promotees.

---

## Q34: Salary progression per employee year-over-year

**Schema hint:** `payroll(emp_id, pay_period, base_salary)`

```sql
-- PostgreSQL
WITH yearly_salary AS (
  SELECT emp_id,
         EXTRACT(YEAR FROM pay_period::date) AS pay_year,
         AVG(base_salary) AS avg_salary
    FROM payroll
   GROUP BY emp_id, EXTRACT(YEAR FROM pay_period::date)
)
SELECT emp_id, pay_year, avg_salary,
       LAG(avg_salary) OVER (PARTITION BY emp_id ORDER BY pay_year) AS prev_year_salary,
       ROUND(
         (avg_salary - LAG(avg_salary) OVER (PARTITION BY emp_id ORDER BY pay_year))
         / NULLIF(LAG(avg_salary) OVER (PARTITION BY emp_id ORDER BY pay_year), 0) * 100,
       2) AS yoy_change_pct
  FROM yearly_salary
 ORDER BY emp_id, pay_year;
```

**Explanation:** LAG accesses the previous year's salary; dividing the difference gives the year-over-year percentage change.

**Alt1:**
```sql
-- MySQL
WITH yearly_salary AS (
  SELECT emp_id,
         YEAR(pay_period) AS pay_year,
         AVG(base_salary) AS avg_salary
    FROM payroll
   GROUP BY emp_id, YEAR(pay_period)
)
SELECT emp_id, pay_year, avg_salary,
       LAG(avg_salary) OVER (PARTITION BY emp_id ORDER BY pay_year) AS prev_year_salary,
       ROUND(
         (avg_salary - LAG(avg_salary) OVER (PARTITION BY emp_id ORDER BY pay_year))
         / NULLIF(LAG(avg_salary) OVER (PARTITION BY emp_id ORDER BY pay_year), 0) * 100,
       2) AS yoy_change_pct
  FROM yearly_salary
 ORDER BY emp_id, pay_year;
```
**Explanation:** YEAR() over the pay_period feeds the identical LAG-based YoY math in MySQL 8+.

---

## Q35: Monthly total salary bill (sum of net_pay)

**Schema hint:** `payroll(pay_period, net_pay)`

```sql
-- SQL Server
SELECT FORMAT(pay_period, 'yyyy-MM') AS pay_month,
       SUM(net_pay) AS total_salary_bill
  FROM payroll
 GROUP BY FORMAT(pay_period, 'yyyy-MM')
 ORDER BY pay_month;
```

**Explanation:** FORMAT standardizes the pay period to year-month; SUM rolls up all net pays.

---

## Q36: Bonus as percentage of base salary per employee

**Schema hint:** `payroll(emp_id, base_salary, bonus)`

```sql
SELECT emp_id,
       SUM(base_salary) AS total_base,
       SUM(bonus)       AS total_bonus,
       ROUND(SUM(bonus) * 100.0 / NULLIF(SUM(base_salary), 0), 2) AS bonus_pct
  FROM payroll
 GROUP BY emp_id
HAVING SUM(bonus) > 0
 ORDER BY bonus_pct DESC;
```

**Explanation:** NULLIF prevents division by zero for employees with no base salary record.

---

## Q37: Employees with zero bonus in any pay period

**Schema hint:** `payroll(emp_id, bonus, pay_period)`

```sql
SELECT DISTINCT emp_id
  FROM payroll
 WHERE bonus = 0
   AND emp_id NOT IN (
       SELECT emp_id
         FROM payroll
        WHERE bonus > 0
       );
```

**Explanation:** The NOT IN subquery excludes anyone who ever received a bonus, leaving only perpetually zero-bonus employees.

---

## Q38: Total leave days per employee (current year)

**Schema hint:** `leave_records(emp_id, start_date, end_date)`

```sql
-- MySQL
SELECT lr.emp_id, e.name,
       SUM(DATEDIFF(lr.end_date, lr.start_date) + 1) AS total_leave_days
  FROM leave_records lr
  JOIN employees e ON e.emp_id = lr.emp_id
 WHERE YEAR(lr.start_date) = YEAR(CURDATE())
 GROUP BY lr.emp_id, e.name
 ORDER BY total_leave_days DESC;
```

**Explanation:** DATEDIFF + 1 accounts for inclusive start/end dates; filtering by year restricts to the current period.

**Alt1:**
```sql
-- PostgreSQL
SELECT lr.emp_id, e.name,
       SUM((lr.end_date - lr.start_date)::int + 1) AS total_leave_days
  FROM leave_records lr
  JOIN employees e ON e.emp_id = lr.emp_id
 WHERE EXTRACT(YEAR FROM lr.start_date) = EXTRACT(YEAR FROM CURRENT_DATE)
 GROUP BY lr.emp_id, e.name
 ORDER BY total_leave_days DESC;
```
**Explanation:** PostgreSQL date subtraction returns integer days directly; +1 keeps the range inclusive.

---

## Q39: Sick leave frequency per employee (top 10)

**Schema hint:** `leave_records(emp_id, leave_type)`

```sql
-- PostgreSQL
SELECT lr.emp_id, e.name,
       COUNT(*) AS sick_leave_count
  FROM leave_records lr
  JOIN employees e ON e.emp_id = lr.emp_id
 WHERE lr.leave_type = 'sick'
 GROUP BY lr.emp_id, e.name
 ORDER BY sick_leave_count DESC
 LIMIT 10;
```

**Explanation:** Filtering on leave_type = 'sick' isolates sick leave; LIMIT 10 surfaces the top consumers.

---

## Q40: Overtime hours per employee from attendance records

**Schema hint:** `attendance(emp_id, date, status)`

```sql
SELECT emp_id,
       COUNT(CASE WHEN status = 'overtime' THEN 1 END) AS overtime_days
  FROM attendance
 WHERE EXTRACT(MONTH FROM date) = EXTRACT(MONTH FROM CURRENT_DATE)
 GROUP BY emp_id
HAVING COUNT(CASE WHEN status = 'overtime' THEN 1 END) > 0
 ORDER BY overtime_days DESC;
```

**Explanation:** Conditional COUNT tallies overtime-marked days in the current month.

---

## Q41: Average performance review score per department

**Schema hint:** `performance_reviews(emp_id, score)`, `employees(dept_id)`

```sql
SELECT d.dept_name,
       ROUND(AVG(pr.score), 2) AS avg_score,
       COUNT(pr.emp_id) AS reviews_count
  FROM performance_reviews pr
  JOIN employees e ON e.emp_id = pr.emp_id
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name
 ORDER BY avg_score DESC;
```

**Explanation:** JOINing reviews to employees to departments links scores to their department context.

**Alt1:**
```sql
WITH dept_avgs AS (
  SELECT d.dept_name,
         AVG(pr.score) OVER (PARTITION BY e.dept_id) AS avg_score,
         COUNT(pr.emp_id) OVER (PARTITION BY e.dept_id) AS reviews_count
    FROM performance_reviews pr
    JOIN employees e ON e.emp_id = pr.emp_id
    JOIN departments d ON d.dept_id = e.dept_id
)
SELECT DISTINCT dept_name, ROUND(avg_score, 2) AS avg_score, reviews_count
  FROM dept_avgs
 ORDER BY avg_score DESC;
```
**Explanation:** Window aggregates compute department means without GROUP BY; DISTINCT collapses the repeated per-row values.

---

## Q42: Top performer (highest avg score) per department

**Schema hint:** `performance_reviews(emp_id, score)`, `employees(dept_id)`

```sql
WITH emp_scores AS (
  SELECT e.emp_id, e.name, e.dept_id,
         AVG(pr.score) AS avg_score,
         ROW_NUMBER() OVER (PARTITION BY e.dept_id ORDER BY AVG(pr.score) DESC) AS rn
    FROM performance_reviews pr
    JOIN employees e ON e.emp_id = pr.emp_id
   GROUP BY e.emp_id, e.name, e.dept_id
)
SELECT es.name AS top_performer, d.dept_name, ROUND(es.avg_score, 2) AS avg_score
  FROM emp_scores es
  JOIN departments d ON d.dept_id = es.dept_id
 WHERE es.rn = 1;
```

**Explanation:** ROW_NUMBER ranks employees within each department by average score; rn = 1 is the winner.

---

## Q43: Correlation between salary band and review score

**Schema hint:** `employees(salary)`, `performance_reviews(score)`

```sql
-- PostgreSQL
WITH salary_bands AS (
  SELECT emp_id,
         NTILE(5) OVER (ORDER BY salary) AS salary_quintile
    FROM employees
)
SELECT sb.salary_quintile,
       ROUND(AVG(pr.score), 2) AS avg_review_score,
       COUNT(*) AS sample_size
  FROM salary_bands sb
  JOIN performance_reviews pr ON pr.emp_id = sb.emp_id
 GROUP BY sb.salary_quintile
 ORDER BY sb.salary_quintile;
```

**Explanation:** NTILE(5) splits employees into five salary quintiles; averaging review scores per quintile reveals pay-performance correlation.

**Alt1:**
```sql
-- PostgreSQL
SELECT ROUND(CORR(e.salary, pr.score)::numeric, 3) AS salary_score_correlation,
       ROUND(REGR_SLOPE(pr.score, e.salary)::numeric, 4) AS score_per_dollar
  FROM employees e
  JOIN performance_reviews pr ON pr.emp_id = e.emp_id;
```
**Explanation:** CORR yields the Pearson correlation; REGR_SLOPE quantifies how many score points each dollar of salary buys.

---

## Q44: Employees with above-average salary AND above-average review score

**Schema hint:** `employees(salary)`, `performance_reviews(score)`

```sql
WITH emp_metrics AS (
  SELECT e.emp_id, e.name, e.salary,
         AVG(pr.score) AS avg_score,
         AVG(e.salary) OVER () AS global_avg_sal,
         AVG(AVG(pr.score)) OVER () AS global_avg_score
    FROM employees e
    JOIN performance_reviews pr ON pr.emp_id = e.emp_id
   GROUP BY e.emp_id, e.name, e.salary
)
SELECT name, salary, ROUND(avg_score, 2) AS avg_score
  FROM emp_metrics
 WHERE salary > global_avg_sal
   AND avg_score > global_avg_score;
```

**Explanation:** Window functions compute global averages; the WHERE clause keeps only high-performing, high-earning employees.

---

## Q45: Gender composition across the company

**Schema hint:** `employees(gender)`

```sql
SELECT gender,
       COUNT(*) AS headcount,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct
  FROM employees
 GROUP BY gender
 ORDER BY headcount DESC;
```

**Explanation:** A window SUM of COUNT(*) over the entire result gives the total for percentage calculation.

---

## Q46: Department transfer history for an employee

**Schema hint:** `department_transfers(emp_id, from_dept_id, to_dept_id, transfer_date)`

```sql
SELECT dt.emp_id, e.name,
       d1.dept_name AS from_dept,
       d2.dept_name AS to_dept,
       dt.transfer_date
  FROM department_transfers dt
  JOIN employees e    ON e.emp_id    = dt.emp_id
  JOIN departments d1 ON d1.dept_id  = dt.from_dept_id
  JOIN departments d2 ON d2.dept_id  = dt.to_dept_id
 WHERE dt.emp_id = 1042
 ORDER BY dt.transfer_date;
```

**Explanation:** Double-joining the departments table decodes both the source and destination department names.

---

## Q47: Employees who have never changed departments

**Schema hint:** `employees(emp_id)`, `department_transfers(emp_id)`

```sql
SELECT e.emp_id, e.name
  FROM employees e
 WHERE NOT EXISTS (
       SELECT 1
         FROM department_transfers dt
        WHERE dt.emp_id = e.emp_id
       );
```

**Explanation:** NOT EXISTS filters employees absent from the transfer table — indicating a single-department career.

---

## Q48: Average number of transfers per employee

**Schema hint:** `department_transfers(emp_id)`

```sql
SELECT ROUND(AVG(transfer_count), 2) AS avg_transfers_per_employee
  FROM (
    SELECT emp_id, COUNT(*) AS transfer_count
      FROM department_transfers
     GROUP BY emp_id
  ) sub
 UNION ALL
 SELECT 0.00
  WHERE NOT EXISTS (SELECT 1 FROM department_transfers);
```

**Explanation:** The subquery counts transfers per employee; the outer query averages them. UNION ALL handles the empty-table edge case.

---

## Q49: Employees with salary below the median for their department and gender

**Schema hint:** `employees(dept_id, gender, salary)`

```sql
-- PostgreSQL
WITH gender_dept_median AS (
  SELECT dept_id, gender,
         PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median_salary
    FROM employees
   GROUP BY dept_id, gender
)
SELECT e.name, e.salary, d.dept_name, e.gender, gdm.median_salary
  FROM employees e
  JOIN departments d          ON d.dept_id     = e.dept_id
  JOIN gender_dept_median gdm ON gdm.dept_id   = e.dept_id
                             AND gdm.gender    = e.gender
 WHERE e.salary < gdm.median_salary;
```

**Explanation:** PERCENTILE_CONT computes median within each dept-gender partition; employees below that median are flagged.

**Alt1:**
```sql
-- PostgreSQL
WITH ranked AS (
  SELECT emp_id, name, dept_id, gender, salary,
         PERCENTILE_CONT(0.5) OVER (PARTITION BY dept_id, gender ORDER BY salary) AS median_salary
    FROM employees
)
SELECT r.name, r.salary, d.dept_name, r.gender, ROUND(r.median_salary, 2) AS median_salary
  FROM ranked r
  JOIN departments d ON d.dept_id = r.dept_id
 WHERE r.salary < r.median_salary;
```
**Explanation:** PERCENTILE_CONT as a window function delivers the same dept-gender median without a GROUP BY join.

---

## Q50: Hire date gaps — months with zero new hires

**Schema hint:** `employees(hire_date)`

```sql
-- PostgreSQL
WITH month_series AS (
  SELECT generate_series(
           DATE_TRUNC('month', MIN(hire_date)),
           DATE_TRUNC('month', CURRENT_DATE),
           INTERVAL '1 month'
         ) AS month
    FROM employees
),
hires_per_month AS (
  SELECT DATE_TRUNC('month', hire_date) AS month, COUNT(*) AS hires
    FROM employees
   GROUP BY DATE_TRUNC('month', hire_date)
)
SELECT ms.month
  FROM month_series ms
  LEFT JOIN hires_per_month hpm ON hpm.month = ms.month
 WHERE hpm.hires IS NULL OR hpm.hires = 0
 ORDER BY ms.month;
```

**Explanation:** generate_series creates a continuous month range; LEFT JOIN + NULL check reveals gaps with no hiring activity.

---

## Q51: Exit interview categories with employee count

**Schema hint:** `exit_interviews(emp_id, category)`, `employees(name)`

```sql
SELECT ei.category,
       COUNT(*) AS exit_count,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct
  FROM exit_interviews ei
 GROUP BY ei.category
 ORDER BY exit_count DESC;
```

**Explanation:** Aggregating exit interview reasons highlights the primary drivers of attrition.

---

## Q52: Employees who took the longest single leave

**Schema hint:** `leave_records(emp_id, start_date, end_date)`

```sql
-- MySQL
SELECT lr.emp_id, e.name, lr.leave_type,
       lr.start_date, lr.end_date,
       DATEDIFF(lr.end_date, lr.start_date) + 1 AS leave_days
  FROM leave_records lr
  JOIN employees e ON e.emp_id = lr.emp_id
 ORDER BY leave_days DESC
 LIMIT 5;
```

**Explanation:** DATEDIFF + 1 counts inclusive days; ORDER BY DESC with LIMIT surfaces the longest leaves.

---

## Q53: Salary freeze — employees with no raise in 2+ years

**Schema hint:** `employees(emp_id, hire_date)`, `promotions(emp_id, promo_date, new_salary, old_salary)`

```sql
WITH last_promo AS (
  SELECT emp_id, MAX(promo_date) AS last_promo_date
    FROM promotions
   GROUP BY emp_id
)
SELECT e.emp_id, e.name, e.salary,
       lp.last_promo_date,
       DATEDIFF(CURDATE(), lp.last_promo_date) AS days_since_last_raise
  FROM employees e
  LEFT JOIN last_promo lp ON lp.emp_id = e.emp_id
 WHERE lp.last_promo_date IS NULL
    OR DATEDIFF(CURDATE(), lp.last_promo_date) > 730
 ORDER BY days_since_last_raise DESC;
```

**Explanation:** Employees without a promotion in 730+ days (≈2 years) are salary-frozen candidates.

**Alt1:**
```sql
-- PostgreSQL
WITH last_promo AS (
  SELECT emp_id, MAX(promo_date) AS last_promo_date
    FROM promotions
   GROUP BY emp_id
)
SELECT e.emp_id, e.name, e.salary,
       lp.last_promo_date,
       (CURRENT_DATE - COALESCE(lp.last_promo_date, e.hire_date)) AS days_since_last_raise
  FROM employees e
  LEFT JOIN last_promo lp ON lp.emp_id = e.emp_id
 WHERE lp.last_promo_date IS NULL
    OR (CURRENT_DATE - lp.last_promo_date) > 730
 ORDER BY days_since_last_raise DESC;
```
**Explanation:** PostgreSQL subtracts dates natively; COALESCE falls back to hire_date so never-promoted staff are included.

---

## Q54: Span of control — managers with the widest reach

**Schema hint:** `employees(emp_id, manager_id)`

```sql
-- SQL Server
SELECT TOP 10
       m.name AS manager,
       COUNT(e.emp_id) AS span
  FROM employees m
  JOIN employees e ON e.manager_id = m.emp_id
 GROUP BY m.name
 ORDER BY span DESC;
```

**Explanation:** TOP 10 limits the result to the ten managers with the most direct reports.

---

## Q55: Employees due for promotion (time-in-grade > 3 years)

**Schema hint:** `employees(hire_date)`, `promotions(emp_id, promo_date)`

```sql
WITH last_promo AS (
  SELECT emp_id, MAX(promo_date) AS last_promo_date
    FROM promotions
   GROUP BY emp_id
)
SELECT e.emp_id, e.name,
       COALESCE(lp.last_promo_date, e.hire_date) AS reference_date,
       DATEDIFF(CURDATE(), COALESCE(lp.last_promo_date, e.hire_date)) AS days_in_grade
  FROM employees e
  LEFT JOIN last_promo lp ON lp.emp_id = e.emp_id
 WHERE DATEDIFF(CURDATE(), COALESCE(lp.last_promo_date, e.hire_date)) > 1095
 ORDER BY days_in_grade DESC;
```

**Explanation:** 1095 days ≈ 3 years. COALESCE falls back to hire_date for employees never promoted.

---

## Q56: Payroll deduction analysis — average deduction percentage per department

**Schema hint:** `payroll(emp_id, base_salary, deduction)`, `employees(dept_id)`

```sql
SELECT d.dept_name,
       ROUND(AVG(p.deduction), 2) AS avg_deduction,
       ROUND(AVG(p.deduction * 100.0 / NULLIF(p.base_salary, 0)), 2) AS avg_deduction_pct
  FROM payroll p
  JOIN employees e ON e.emp_id = p.emp_id
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name
 ORDER BY avg_deduction_pct DESC;
```

**Explanation:** Both absolute and percentage deductions are computed to account for salary scale differences.

---

## Q57: Performance review trend — improving vs declining per employee

**Schema hint:** `performance_reviews(emp_id, review_date, score)`

```sql
WITH scored AS (
  SELECT emp_id, score,
         LAG(score) OVER (PARTITION BY emp_id ORDER BY review_date) AS prev_score
    FROM performance_reviews
)
SELECT emp_id,
       SUM(CASE WHEN score > prev_score THEN 1 ELSE 0 END) AS improvements,
       SUM(CASE WHEN score < prev_score THEN 1 ELSE 0 END) AS declines,
       CASE
         WHEN SUM(CASE WHEN score > prev_score THEN 1 ELSE 0 END) >
              SUM(CASE WHEN score < prev_score THEN 1 ELSE 0 END) THEN 'Improving'
         WHEN SUM(CASE WHEN score < prev_score THEN 1 ELSE 0 END) >
              SUM(CASE WHEN score > prev_score THEN 1 ELSE 0 END) THEN 'Declining'
         ELSE 'Stable'
       END AS trend
  FROM scored
 WHERE prev_score IS NOT NULL
 GROUP BY emp_id;
```

**Explanation:** LAG compares each score to the previous one; counting improvements vs declines classifies the overall trend.

**Alt1:**
```sql
-- SQL Server
WITH scored AS (
  SELECT emp_id, score,
         LAG(score) OVER (PARTITION BY emp_id ORDER BY review_date) AS prev_score
    FROM performance_reviews
)
SELECT emp_id,
       SUM(CASE WHEN score > prev_score THEN 1 ELSE 0 END) AS improvements,
       SUM(CASE WHEN score < prev_score THEN 1 ELSE 0 END) AS declines
  FROM scored
 WHERE prev_score IS NOT NULL
 GROUP BY emp_id
 ORDER BY improvements DESC;
```
**Explanation:** SQL Server shares the identical LAG syntax; ordering by improvement count surfaces growth trends directly.

---

## Q58: Employees with consecutive absences (>= 3 days)

**Schema hint:** `attendance(emp_id, date, status)`

```sql
-- PostgreSQL
WITH absent_runs AS (
  SELECT emp_id, date, status,
         date - ROW_NUMBER() OVER (PARTITION BY emp_id, status ORDER BY date) AS grp
    FROM attendance
   WHERE status = 'absent'
),
consecutive AS (
  SELECT emp_id, MIN(date) AS absence_start, MAX(date) AS absence_end,
         COUNT(*) AS consecutive_days
    FROM absent_runs
   GROUP BY emp_id, grp
  HAVING COUNT(*) >= 3
)
SELECT c.emp_id, e.name, c.absence_start, c.absence_end, c.consecutive_days
  FROM consecutive c
  JOIN employees e ON e.emp_id = c.emp_id
 ORDER BY c.consecutive_days DESC;
```

**Explanation:** The classic "islands" technique: ROW_NUMBER subtracted from the date creates a group identifier for consecutive sequences.

---

## Q59: Cost per hire (payroll spend since hire date)

**Schema hint:** `payroll(emp_id, net_pay)`, `employees(hire_date)`

```sql
SELECT e.emp_id, e.name, e.hire_date,
       SUM(p.net_pay) AS total_cost
  FROM employees e
  JOIN payroll p ON p.emp_id = e.emp_id
 GROUP BY e.emp_id, e.name, e.hire_date
 ORDER BY total_cost DESC
 LIMIT 10;
```

**Explanation:** SUM of all net pays per employee represents the total cost the company has incurred for that hire.

---

## Q60: Department headcount as a percentage of total company headcount

**Schema hint:** `employees(dept_id)`, `departments(dept_name)`

```sql
SELECT d.dept_name,
       COUNT(e.emp_id) AS dept_headcount,
       SUM(COUNT(e.emp_id)) OVER () AS total_headcount,
       ROUND(COUNT(e.emp_id) * 100.0 / SUM(COUNT(e.emp_id)) OVER (), 2) AS pct_of_total
  FROM departments d
  LEFT JOIN employees e ON e.dept_id = d.dept_id
 GROUP BY d.dept_name
 ORDER BY pct_of_total DESC;
```

**Explanation:** A window SUM of COUNT gives the total in a single pass, enabling percentage calculation without a subquery.

---

## Q61: Employees who were promoted within 1 year of hire

**Schema hint:** `employees(hire_date)`, `promotions(emp_id, promo_date)`

```sql
-- MySQL
SELECT e.emp_id, e.name, e.hire_date, p.promo_date, p.new_title,
       DATEDIFF(p.promo_date, e.hire_date) AS days_to_first_promo
  FROM employees e
  JOIN promotions p ON p.emp_id = e.emp_id
 WHERE DATEDIFF(p.promo_date, e.hire_date) <= 365
 ORDER BY days_to_first_promo;
```

**Explanation:** DATEDIFF measures days from hire to the promotion date; 365-day threshold identifies fast-track employees.

---

## Q62: Running total of salary expenditure by department over time

**Schema hint:** `payroll(emp_id, pay_period, net_pay)`, `employees(dept_id)`

```sql
-- Oracle
SELECT d.dept_name,
       TO_CHAR(p.pay_period, 'YYYY-MM') AS pay_month,
       SUM(p.net_pay) AS monthly_spend,
       SUM(SUM(p.net_pay)) OVER (PARTITION BY d.dept_id
                                  ORDER BY TO_CHAR(p.pay_period, 'YYYY-MM'))
         AS cumulative_spend
  FROM payroll p
  JOIN employees e ON e.emp_id = p.emp_id
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name, d.dept_id, TO_CHAR(p.pay_period, 'YYYY-MM')
 ORDER BY d.dept_name, pay_month;
```

**Explanation:** SUM OVER (PARTITION ... ORDER ...) creates a running total of salary expenditure within each department.

**Alt1:**
```sql
-- SQL Server
SELECT d.dept_name,
       FORMAT(p.pay_period, 'yyyy-MM') AS pay_month,
       SUM(p.net_pay) AS monthly_spend,
       SUM(SUM(p.net_pay)) OVER (PARTITION BY d.dept_id
                                  ORDER BY FORMAT(p.pay_period, 'yyyy-MM'))
         AS cumulative_spend
  FROM payroll p
  JOIN employees e ON e.emp_id = p.emp_id
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name, d.dept_id, FORMAT(p.pay_period, 'yyyy-MM')
 ORDER BY d.dept_name, pay_month;
```
**Explanation:** FORMAT renders a zero-padded year-month key that sorts lexicographically, mirroring the Oracle TO_CHAR variant.

---

## Q63: Payroll net-pay ranking across all employees per period

**Schema hint:** `payroll(emp_id, pay_period, net_pay)`

```sql
-- SQL Server
SELECT emp_id,
       FORMAT(pay_period, 'yyyy-MM') AS period,
       net_pay,
       RANK() OVER (PARTITION BY pay_period ORDER BY net_pay DESC) AS pay_rank
  FROM payroll
 WHERE FORMAT(pay_period, 'yyyy-MM') = '2025-01';
```

**Explanation:** RANK assigns a dense rank to employees ordered by net pay within a specific month.

---

## Q64: Sick leave vs total leave ratio per employee

**Schema hint:** `leave_records(emp_id, leave_type)`

```sql
WITH totals AS (
  SELECT emp_id,
         SUM(CASE WHEN leave_type = 'sick' THEN 1 ELSE 0 END) AS sick_days,
         COUNT(*) AS total_leave
    FROM leave_records
   WHERE EXTRACT(YEAR FROM start_date) = EXTRACT(YEAR FROM CURRENT_DATE)
   GROUP BY emp_id
)
SELECT t.emp_id, e.name, t.sick_days, t.total_leave,
       ROUND(t.sick_days * 100.0 / NULLIF(t.total_leave, 0), 2) AS sick_pct
  FROM totals t
  JOIN employees e ON e.emp_id = t.emp_id
 WHERE t.total_leave > 0
 ORDER BY sick_pct DESC;
```

**Explanation:** The ratio reveals whether an employee's absences are predominantly illness-related.

---

## Q65: Employees with attendance below 80% in a month

**Schema hint:** `attendance(emp_id, date, status)`

```sql
WITH monthly_stats AS (
  SELECT emp_id,
         EXTRACT(MONTH FROM date) AS mth,
         COUNT(CASE WHEN status = 'present' THEN 1 END) AS present_days,
         COUNT(*) AS total_days
    FROM attendance
   WHERE EXTRACT(YEAR FROM date) = 2025
     AND EXTRACT(MONTH FROM date) = 6
   GROUP BY emp_id, EXTRACT(MONTH FROM date)
)
SELECT ms.emp_id, e.name,
       ms.present_days, ms.total_days,
       ROUND(ms.present_days * 100.0 / ms.total_days, 2) AS attendance_pct
  FROM monthly_stats ms
  JOIN employees e ON e.emp_id = ms.emp_id
 WHERE ms.present_days * 100.0 / ms.total_days < 80
 ORDER BY attendance_pct;
```

**Explanation:** Computing the attendance percentage and filtering < 80% surfaces chronic absentees.

---

## Q66: Cross-department salary comparison — each department vs company average

**Schema hint:** `employees(dept_id, salary)`

```sql
SELECT d.dept_name,
       ROUND(AVG(e.salary), 2) AS dept_avg,
       ROUND((SELECT AVG(salary) FROM employees), 2) AS company_avg,
       ROUND(AVG(e.salary) - (SELECT AVG(salary) FROM employees), 2) AS diff_from_avg
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name
 ORDER BY diff_from_avg DESC;
```

**Explanation:** A scalar subquery provides the company-wide average; subtraction reveals which departments are above/below.

**Alt1:**
```sql
WITH dept_stats AS (
  SELECT d.dept_name,
         AVG(e.salary) AS dept_avg
    FROM employees e
    JOIN departments d ON d.dept_id = e.dept_id
   GROUP BY d.dept_name
)
SELECT dept_name,
       ROUND(dept_avg, 2) AS dept_avg,
       ROUND(AVG(dept_avg) OVER (), 2) AS overall_avg,
       ROUND(dept_avg - AVG(dept_avg) OVER (), 2) AS diff_from_avg
  FROM dept_stats
 ORDER BY diff_from_avg DESC;
```
**Explanation:** AVG OVER () over the department rows yields the average of department averages without a scalar subquery.

---

## Q67: Cohort analysis — employees grouped by hire year, tracked by tenure

**Schema hint:** `employees(hire_date)`

```sql
-- PostgreSQL
SELECT EXTRACT(YEAR FROM hire_date)::INT AS cohort_year,
       COUNT(*) AS cohort_size,
       ROUND(AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, hire_date))), 1) AS avg_tenure_yrs
  FROM employees
 GROUP BY cohort_year
 ORDER BY cohort_year;
```

**Explanation:** Each hire-year cohort is tracked; average tenure validates that older cohorts are still present.

---

## Q68: Employees whose salary is more than 2x the department average

**Schema hint:** `employees(dept_id, salary, name)`

```sql
SELECT e.name, e.salary, d.dept_name
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
 WHERE e.salary > 2 * (
       SELECT AVG(e2.salary)
         FROM employees e2
        WHERE e2.dept_id = e.dept_id
       )
 ORDER BY e.salary DESC;
```

**Explanation:** The correlated subquery computes the department average; the 2x multiplier flags outliers.

---

## Q69: Monthly attrition rate (departures / beginning headcount)

**Schema hint:** `employees(hire_date, left_date)`

```sql
-- PostgreSQL
WITH months AS (
  SELECT generate_series(
           DATE_TRUNC('month', MIN(hire_date)),
           DATE_TRUNC('month', CURRENT_DATE),
           INTERVAL '1 month'
         ) AS month
    FROM employees
),
beginning AS (
  SELECT m.month,
         COUNT(*) AS headcount_begin
    FROM employees e
    JOIN months m ON DATE_TRUNC('month', e.hire_date) <= m.month
                 AND (e.left_date IS NULL OR DATE_TRUNC('month', e.left_date) > m.month)
   GROUP BY m.month
),
departures AS (
  SELECT DATE_TRUNC('month', left_date) AS month,
         COUNT(*) AS exits
    FROM employees
   WHERE left_date IS NOT NULL
   GROUP BY DATE_TRUNC('month', left_date)
)
SELECT b.month, b.headcount_begin,
       COALESCE(d.exits, 0) AS exits,
       ROUND(COALESCE(d.exits, 0) * 100.0 / NULLIF(b.headcount_begin, 0), 2) AS attrition_rate_pct
  FROM beginning b
  LEFT JOIN departures d ON d.month = b.month
 ORDER BY b.month;
```

**Explanation:** Beginning headcount is computed by counting active employees; departures are overlayed to compute a monthly rate.

---

## Q70: Gender pay gap per department

**Schema hint:** `employees(dept_id, gender, salary)`

```sql
-- PostgreSQL
WITH dept_gender_avg AS (
  SELECT dept_id, gender, AVG(salary) AS avg_salary
    FROM employees
   GROUP BY dept_id, gender
)
SELECT d.dept_name,
       MAX(CASE WHEN dga.gender = 'M' THEN ROUND(dga.avg_salary, 2) END) AS male_avg,
       MAX(CASE WHEN dga.gender = 'F' THEN ROUND(dga.avg_salary, 2) END) AS female_avg,
       ROUND(
         ABS(
           MAX(CASE WHEN dga.gender = 'M' THEN dga.avg_salary END) -
           MAX(CASE WHEN dga.gender = 'F' THEN dga.avg_salary END)
         ) * 100.0 /
         NULLIF(MAX(CASE WHEN dga.gender = 'M' THEN dga.avg_salary END), 0),
       2) AS gap_pct
  FROM dept_gender_avg dga
  JOIN departments d ON d.dept_id = dga.dept_id
 GROUP BY d.dept_name;
```

**Explanation:** Conditional MAX pivots gender averages into columns; the percentage gap is computed between male and female averages.

---

## Q71: Review score standard deviation per department (quality consistency)

**Schema hint:** `performance_reviews(emp_id, score)`, `employees(dept_id)`

```sql
SELECT d.dept_name,
       ROUND(AVG(pr.score), 2) AS avg_score,
       ROUND(STDDEV(pr.score), 2) AS score_stddev,
       COUNT(*) AS review_count
  FROM performance_reviews pr
  JOIN employees e ON e.emp_id = pr.emp_id
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name
 ORDER BY score_stddev DESC;
```

**Explanation:** High stddev suggests inconsistent performance within a department — a signal for management review.

---

## Q72: Employees with no performance review on record

**Schema hint:** `employees(emp_id)`, `performance_reviews(emp_id)`

```sql
SELECT e.emp_id, e.name, e.dept_id
  FROM employees e
 WHERE NOT EXISTS (
       SELECT 1
         FROM performance_reviews pr
        WHERE pr.emp_id = e.emp_id
       );
```

**Explanation:** NOT EXISTS cleanly identifies employees absent from the review process.

---

## Q73: Department with the highest total payroll spend

**Schema hint:** `payroll(emp_id, net_pay)`, `employees(dept_id)`

```sql
SELECT d.dept_name,
       SUM(p.net_pay) AS total_spend,
       COUNT(DISTINCT p.emp_id) AS paying_headcount
  FROM payroll p
  JOIN employees e ON e.emp_id = p.emp_id
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name
 ORDER BY total_spend DESC
 LIMIT 1;
```

**Explanation:** SUM of net_pay per department reveals which unit carries the largest payroll burden.

---

## Q74: Pay period anomalies — negative net_pay

**Schema hint:** `payroll(emp_id, pay_period, net_pay)`

```sql
SELECT emp_id, pay_period, base_salary, bonus, deduction, net_pay
  FROM payroll
 WHERE net_pay < 0
 ORDER BY pay_period, emp_id;
```

**Explanation:** Negative net_pay indicates over-recovery or payroll errors that need investigation.

---

## Q75: Employee retention cohort (hire-year vs still-active count)

**Schema hint:** `employees(hire_date, left_date)`

```sql
SELECT EXTRACT(YEAR FROM hire_date)::INT AS hire_year,
       COUNT(*) AS total_hired,
       COUNT(CASE WHEN left_date IS NULL THEN 1 END) AS still_active,
       ROUND(COUNT(CASE WHEN left_date IS NULL THEN 1 END) * 100.0 / COUNT(*), 2) AS retention_pct
  FROM employees
 GROUP BY hire_year
 ORDER BY hire_year;
```

**Explanation:** Per hire-year, the ratio of active to total hired shows long-term retention by cohort.

---

## Q76: Managers whose direct reports all earn less (strict hierarchy)

**Schema hint:** `employees(emp_id, salary, manager_id)`

```sql
SELECT m.emp_id AS manager_id, m.name AS manager_name
  FROM employees m
 WHERE NOT EXISTS (
       SELECT 1
         FROM employees e
        WHERE e.manager_id = m.emp_id
          AND e.salary >= m.salary
       );
```

**Explanation:** NOT EXISTS with a salary check ensures every reportee earns strictly less — a strict org-chart invariant.

---

## Q77: Salary compression detection — reports earning within 5% of manager

**Schema hint:** `employees(emp_id, salary, manager_id)`

```sql
SELECT e.name AS employee, e.salary AS emp_salary,
       m.name AS manager, m.salary AS mgr_salary,
       ROUND((m.salary - e.salary) * 100.0 / m.salary, 2) AS gap_pct
  FROM employees e
  JOIN employees m ON m.emp_id = e.manager_id
 WHERE (m.salary - e.salary) * 100.0 / m.salary < 5
   AND e.salary < m.salary
 ORDER BY gap_pct;
```

**Explanation:** A gap under 5% signals salary compression — employees clustered too close to their manager's pay.

**Alt1:**
```sql
SELECT e.name AS employee, e.salary AS emp_salary,
       m.name AS manager, m.salary AS mgr_salary,
       CASE WHEN e.salary >= m.salary * 0.95 THEN 'Within 5% of manager' ELSE 'OK' END AS flag
  FROM employees e
  JOIN employees m ON m.emp_id = e.manager_id
 WHERE e.salary BETWEEN m.salary * 0.95 AND m.salary
 ORDER BY flag, m.salary;
```
**Explanation:** A BETWEEN window isolates staff sitting exactly 5% under their manager's pay — compression without the pre-computed ratio.

---

## Q78: Compensation vs review score — salary quartile by score quartile

**Schema hint:** `employees(salary)`, `performance_reviews(score)`

```sql
-- PostgreSQL
WITH emp_quartiles AS (
  SELECT e.emp_id,
         NTILE(4) OVER (ORDER BY e.salary)   AS salary_q,
         NTILE(4) OVER (ORDER BY pr.score)    AS score_q
    FROM employees e
    JOIN performance_reviews pr ON pr.emp_id = e.emp_id
)
SELECT salary_q, score_q, COUNT(*) AS employee_count
  FROM emp_quartiles
 GROUP BY salary_q, score_q
 ORDER BY salary_q, score_q;
```

**Explanation:** Dual NTILE partitioning creates a cross-tab of salary quartile vs review-score quartile.

---

## Q79: Employees who changed departments AND received a promotion

**Schema hint:** `department_transfers(emp_id)`, `promotions(emp_id)`

```sql
SELECT DISTINCT e.emp_id, e.name
  FROM employees e
 WHERE e.emp_id IN (SELECT emp_id FROM department_transfers)
   AND e.emp_id IN (SELECT emp_id FROM promotions);
```

**Explanation:** IN-list intersection identifies employees present in both the transfer and promotion tables.

---

## Q80: Year-over-year headcount growth rate

**Schema hint:** `employees(hire_date)`

```sql
WITH yearly AS (
  SELECT EXTRACT(YEAR FROM hire_date)::INT AS yr,
         COUNT(*) AS hires
    FROM employees
   GROUP BY yr
)
SELECT y1.yr,
       y1.hires,
       y2.hires AS prev_year_hires,
       ROUND((y1.hires - y2.hires) * 100.0 / NULLIF(y2.hires, 0), 2) AS yoy_growth_pct
  FROM yearly y1
  LEFT JOIN yearly y2 ON y2.yr = y1.yr - 1
 ORDER BY y1.yr;
```

**Explanation:** A self-join on adjacent years computes the percentage change in hiring volume.

---

## Q81: Average time between promotions for employees with 2+ promos

**Schema hint:** `promotions(emp_id, promo_date)`

```sql
WITH promo_gaps AS (
  SELECT emp_id, promo_date,
         LAG(promo_date) OVER (PARTITION BY emp_id ORDER BY promo_date) AS prev_promo
    FROM promotions
)
SELECT ROUND(AVG(DATEDIFF(promo_date, prev_promo)), 0) AS avg_days_between_promos
  FROM promo_gaps
 WHERE prev_promo IS NOT NULL;
```

**Explanation:** LAG provides the previous promotion date; AVG of the gaps gives the average cadence.

---

## Q82: Salary percentile rank per employee globally

**Schema hint:** `employees(salary, name)`

```sql
-- PostgreSQL
SELECT name, salary,
       PERCENT_RANK() OVER (ORDER BY salary) AS pct_rank,
       CUME_DIST()    OVER (ORDER BY salary) AS cumulative_dist
  FROM employees
 ORDER BY salary DESC;
```

**Explanation:** PERCENT_RANK gives relative standing (0 to 1); CUME_DIST gives the cumulative distribution value.

---

## Q83: Employees who got a pay cut (promotion with lower salary)

**Schema hint:** `promotions(emp_id, old_salary, new_salary, new_title)`

```sql
SELECT p.emp_id, e.name, p.old_salary, p.new_salary, p.new_title, p.promo_date
  FROM promotions p
  JOIN employees e ON e.emp_id = p.emp_id
 WHERE p.new_salary < p.old_salary
 ORDER BY p.promo_date;
```

**Explanation:** A promotion with a salary decrease is unusual and may indicate a demotion in disguise.

---

## Q84: Department with the highest standard deviation of review scores

**Schema hint:** `performance_reviews(score)`, `employees(dept_id)`

```sql
SELECT d.dept_name,
       ROUND(STDDEV(pr.score), 2) AS score_stddev
  FROM performance_reviews pr
  JOIN employees e ON e.emp_id = pr.emp_id
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name
 ORDER BY score_stddev DESC
 LIMIT 1;
```

**Explanation:** The department with the widest score spread may have inconsistent management or evaluation criteria.

---

## Q85: Employees with attendance gaps (no record for a weekday)

**Schema hint:** `attendance(emp_id, date)`, `employees(emp_id)`

```sql
-- PostgreSQL
WITH workdays AS (
  SELECT day
    FROM generate_series(
           (SELECT MIN(date) FROM attendance),
           (SELECT MAX(date) FROM attendance),
           INTERVAL '1 day'
         ) AS g(day)
   WHERE EXTRACT(DOW FROM g.day) BETWEEN 1 AND 5
),
emp_workdays AS (
  SELECT e.emp_id, w.day
    FROM employees e
    CROSS JOIN workdays w
)
SELECT ew.emp_id, ew.day
  FROM emp_workdays ew
  LEFT JOIN attendance a ON a.emp_id = ew.emp_id AND a.date = ew.day
 WHERE a.emp_id IS NULL
 ORDER BY ew.emp_id, ew.day
 LIMIT 100;
```

**Explanation:** A generated series of workdays is cross-joined with employees; LEFT JOIN + NULL detects missing attendance records.

---

## Q86: Consecutive performance review scores (3+ reviews at same level)

**Schema hint:** `performance_reviews(emp_id, score, review_date)`

```sql
WITH consecutive_scores AS (
  SELECT emp_id, score, review_date,
         score - ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY review_date) AS grp
    FROM performance_reviews
)
SELECT emp_id, score, COUNT(*) AS consecutive_count
  FROM consecutive_scores
 GROUP BY emp_id, score, grp
HAVING COUNT(*) >= 3;
```

**Explanation:** The ROW_NUMBER subtraction trick identifies consecutive identical scores — a stagnation signal.

---

## Q87: Employees with the most varied leave types

**Schema hint:** `leave_records(emp_id, leave_type)`

```sql
SELECT lr.emp_id, e.name,
       COUNT(DISTINCT lr.leave_type) AS distinct_leave_types,
       STRING_AGG(DISTINCT lr.leave_type, ', ') AS leave_types_used
  FROM leave_records lr
  JOIN employees e ON e.emp_id = lr.emp_id
 GROUP BY lr.emp_id, e.name
 ORDER BY distinct_leave_types DESC
 LIMIT 10;
```

**Explanation:** COUNT(DISTINCT) measures variety; STRING_AGG lists the types for context.

---

## Q88: Salary progression — largest single raise ever received

**Schema hint:** `promotions(emp_id, old_salary, new_salary)`

```sql
SELECT p.emp_id, e.name, p.old_salary, p.new_salary,
       p.new_salary - p.old_salary AS raise_amount,
       ROUND((p.new_salary - p.old_salary) * 100.0 / p.old_salary, 2) AS raise_pct,
       p.promo_date
  FROM promotions p
  JOIN employees e ON e.emp_id = p.emp_id
 ORDER BY raise_pct DESC
 LIMIT 5;
```

**Explanation:** Percentage raise is computed; ORDER BY DESC with LIMIT surfaces the top 5 largest raises.

---

## Q89: Employees who left within 1 year of hire (early attrition)

**Schema hint:** `employees(hire_date, left_date)`

```sql
SELECT emp_id, name, hire_date, left_date,
       DATEDIFF(left_date, hire_date) AS days_employed
  FROM employees
 WHERE left_date IS NOT NULL
   AND DATEDIFF(left_date, hire_date) <= 365
 ORDER BY days_employed;
```

**Explanation:** Early attrition within 365 days signals onboarding or cultural fit issues.

**Alt1:**
```sql
-- PostgreSQL
SELECT emp_id, name, hire_date, left_date,
       (left_date - hire_date) AS days_employed
  FROM employees
 WHERE left_date IS NOT NULL
   AND (left_date - hire_date) <= 365
 ORDER BY days_employed;
```
**Explanation:** PostgreSQL returns integer days from date subtraction directly, with no DATEDIFF call.

---

## Q90: Department salary bands using WIDTH_BUCKET (Oracle)

**Schema hint:** `employees(dept_id, salary)`

```sql
-- Oracle
SELECT d.dept_name,
       WIDTH_BUCKET(e.salary, 30000, 200000, 5) AS salary_band,
       COUNT(*) AS employees_in_band
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name, WIDTH_BUCKET(e.salary, 30000, 200000, 5)
 ORDER BY d.dept_name, salary_band;
```

**Explanation:** WIDTH_BUCKET evenly distributes a numeric range into N buckets, ideal for histogram-style reporting.

---

## Q91: Employees who received the highest single bonus

**Schema hint:** `payroll(emp_id, bonus, pay_period)`

```sql
SELECT emp_id, bonus, pay_period
  FROM payroll
 WHERE bonus = (SELECT MAX(bonus) FROM payroll);
```

**Explanation:** A scalar subquery finds the max bonus; the outer query retrieves the recipient(s).

---

## Q92: Promotion velocity — average months between promotions per dept

**Schema hint:** `promotions(emp_id, promo_date)`, `employees(dept_id)`

```sql
-- MySQL
WITH promo_gaps AS (
  SELECT p.emp_id,
         TIMESTAMPDIFF(MONTH,
           LAG(p.promo_date) OVER (PARTITION BY p.emp_id ORDER BY p.promo_date),
           p.promo_date
         ) AS months_between
    FROM promotions p
)
SELECT d.dept_name,
       ROUND(AVG(pg.months_between), 1) AS avg_months_between_promos
  FROM promo_gaps pg
  JOIN employees e ON e.emp_id = pg.emp_id
  JOIN departments d ON d.dept_id = e.dept_id
 WHERE pg.months_between IS NOT NULL
 GROUP BY d.dept_name
 ORDER BY avg_months_between_promos;
```

**Explanation:** TIMESTAMPDIFF in months measures the gap between consecutive promotions; AVG per dept reveals typical velocity.

---

## Q93: Employees in departments where everyone earns above the company median

**Schema hint:** `employees(dept_id, salary)`

```sql
WITH company_median AS (
  SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median_sal
    FROM employees
),
dept_min_salary AS (
  SELECT dept_id, MIN(salary) AS min_dept_salary
    FROM employees
   GROUP BY dept_id
)
SELECT d.dept_name
  FROM dept_min_salary dms
  JOIN company_median cm ON dms.min_dept_salary > cm.median_sal
  JOIN departments d ON d.dept_id = dms.dept_id;
```

**Explanation:** If a department's minimum salary exceeds the company median, every member earns above-median.

---

## Q94: Hire date day-of-week distribution (are Monday hires more common?)

**Schema hint:** `employees(hire_date)`

```sql
-- PostgreSQL
SELECT TO_CHAR(hire_date, 'Day') AS day_of_week,
       EXTRACT(DOW FROM hire_date)::INT AS dow_num,
       COUNT(*) AS hires
  FROM employees
 GROUP BY day_of_week, dow_num
 ORDER BY dow_num;
```

**Explanation:** TO_CHAR + EXTRACT(DOW) reveals whether hiring clusters on specific days — useful for operational planning.

---

## Q95: Cross-tab: department x leave_type leave days

**Schema hint:** `leave_records(emp_id, leave_type)`, `employees(dept_id)`

```sql
SELECT d.dept_name,
       SUM(CASE WHEN lr.leave_type = 'sick'    THEN DATEDIFF(lr.end_date, lr.start_date) + 1 ELSE 0 END) AS sick_days,
       SUM(CASE WHEN lr.leave_type = 'casual'  THEN DATEDIFF(lr.end_date, lr.start_date) + 1 ELSE 0 END) AS casual_days,
       SUM(CASE WHEN lr.leave_type = 'earned'  THEN DATEDIFF(lr.end_date, lr.start_date) + 1 ELSE 0 END) AS earned_days,
       SUM(CASE WHEN lr.leave_type = 'maternity' THEN DATEDIFF(lr.end_date, lr.start_date) + 1 ELSE 0 END) AS maternity_days
  FROM leave_records lr
  JOIN employees e ON e.emp_id = lr.emp_id
  JOIN departments d ON d.dept_id = e.dept_id
 GROUP BY d.dept_name;
```

**Explanation:** Conditional sums pivot leave types into columns per department — a common HR report layout.

---

## Q96: Employees whose last review score dropped from their first

**Schema hint:** `performance_reviews(emp_id, score, review_date)`

```sql
WITH first_last AS (
  SELECT emp_id,
         FIRST_VALUE(score) OVER (PARTITION BY emp_id ORDER BY review_date) AS first_score,
         FIRST_VALUE(score) OVER (PARTITION BY emp_id ORDER BY review_date DESC) AS last_score
    FROM performance_reviews
)
SELECT DISTINCT fl.emp_id, e.name, fl.first_score, fl.last_score
  FROM first_last fl
  JOIN employees e ON e.emp_id = fl.emp_id
 WHERE fl.last_score < fl.first_score;
```

**Explanation:** FIRST_VALUE with opposite ORDER BY clauses extracts the first and last scores; filtering on decline surfaces at-risk employees.

**Alt1:**
```sql
WITH ordered AS (
  SELECT emp_id, score,
         ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY review_date) AS rn_first,
         ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY review_date DESC) AS rn_last
    FROM performance_reviews
)
SELECT o1.emp_id, e.name,
       o1.score AS first_score, o2.score AS last_score
  FROM ordered o1
  JOIN ordered o2 ON o2.emp_id = o1.emp_id AND o2.rn_last = 1
  JOIN employees e ON e.emp_id = o1.emp_id
 WHERE o1.rn_first = 1
   AND o2.score < o1.score;
```
**Explanation:** Pairing the earliest (rn_first=1) and latest (rn_last=1) reviews makes score erosion detectable in any dialect.

---

## Q97: Employees with identical salaries (salary clusters)

**Schema hint:** `employees(salary, name)`

```sql
SELECT salary, COUNT(*) AS cluster_size,
       STRING_AGG(name, ', ') AS employees
  FROM employees
 GROUP BY salary
HAVING COUNT(*) > 1
 ORDER BY cluster_size DESC;
```

**Explanation:** GROUP BY salary with HAVING COUNT > 1 finds pay-equity clusters — identical salaries across multiple employees.

---

## Q98: Effective salary change audit — payroll vs promotion records mismatch

**Schema hint:** `payroll(emp_id, pay_period, base_salary)`, `promotions(emp_id, promo_date, new_salary)`

```sql
WITH payroll_latest AS (
  SELECT emp_id,
         MAX(pay_period) AS latest_period,
         MAX(base_salary) AS latest_payroll_salary
    FROM payroll
   GROUP BY emp_id
),
promo_latest AS (
  SELECT emp_id,
         MAX(new_salary) AS latest_promo_salary
    FROM promotions
   GROUP BY emp_id
)
SELECT pl.emp_id, e.name,
       pl.latest_payroll_salary,
       pl.latest_period,
       COALESCE(prl.latest_promo_salary, 0) AS latest_promo_salary,
       CASE
         WHEN pl.latest_payroll_salary != COALESCE(prl.latest_promo_salary, 0)
         THEN 'MISMATCH'
         ELSE 'OK'
       END AS status
  FROM payroll_latest pl
  JOIN employees e ON e.emp_id = pl.emp_id
  LEFT JOIN promo_latest prl ON prl.emp_id = pl.emp_id
 WHERE pl.latest_payroll_salary != COALESCE(prl.latest_promo_salary, 0)
 ORDER BY pl.emp_id;
```

**Explanation:** Comparing the latest payroll salary to the latest promotion salary catches data-entry mismatches between systems.

---

## Q99: Tenure-adjusted performance — review score per tenure bucket

**Schema hint:** `employees(hire_date)`, `performance_reviews(score)`

```sql
-- PostgreSQL
WITH emp_tenure AS (
  SELECT e.emp_id,
         EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date))::INT AS tenure_yrs
    FROM employees e
)
SELECT CASE
         WHEN et.tenure_yrs < 1  THEN '0-1 yrs'
         WHEN et.tenure_yrs < 3  THEN '1-3 yrs'
         WHEN et.tenure_yrs < 5  THEN '3-5 yrs'
         WHEN et.tenure_yrs < 10 THEN '5-10 yrs'
         ELSE '10+ yrs'
       END AS tenure_bucket,
       ROUND(AVG(pr.score), 2) AS avg_review_score,
       COUNT(*) AS reviews_count
  FROM performance_reviews pr
  JOIN emp_tenure et ON et.emp_id = pr.emp_id
 GROUP BY tenure_bucket
 ORDER BY MIN(et.tenure_yrs);
```

**Explanation:** Binning by tenure then averaging review scores shows whether experience correlates with higher performance.

---

## Q100: Capstone — Attrition risk pipeline combining tenure, review, leave, and promotion gaps

**Schema hint:** `employees(hire_date, left_date)`, `performance_reviews(score)`, `leave_records(start_date)`, `promotions(promo_date)`

```sql
-- PostgreSQL
WITH emp_tenure AS (
  SELECT emp_id,
         EXTRACT(YEAR FROM AGE(CURRENT_DATE, hire_date)) AS tenure_yrs,
         CASE WHEN left_date IS NOT NULL THEN 1 ELSE 0 END AS has_left
    FROM employees
),
latest_review AS (
  SELECT DISTINCT ON (emp_id)
         emp_id, score AS last_review_score
    FROM performance_reviews
   ORDER BY emp_id, review_date DESC
),
leave_count AS (
  SELECT emp_id,
         COUNT(*) AS leave_days_current_year
    FROM leave_records
   WHERE EXTRACT(YEAR FROM start_date) = EXTRACT(YEAR FROM CURRENT_DATE)
   GROUP BY emp_id
),
last_promo AS (
  SELECT emp_id,
         MAX(promo_date) AS last_promo_date
    FROM promotions
   GROUP BY emp_id
),
risk_scores AS (
  SELECT e.emp_id, e.name,
         et.tenure_yrs,
         lr.last_review_score,
         COALESCE(lc.leave_days_current_year, 0) AS leave_days,
         lp.last_promo_date,
         COALESCE(
           EXTRACT(YEAR FROM AGE(CURRENT_DATE, lp.last_promo_date)),
           EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date))
         ) AS years_since_promo,
         CASE
           WHEN et.tenure_yrs < 1 THEN 1
           WHEN et.tenure_yrs BETWEEN 1 AND 3 THEN 2
           WHEN et.tenure_yrs BETWEEN 3 AND 5 THEN 3
           ELSE 4
         END AS tenure_risk,
         CASE
           WHEN lr.last_review_score IS NULL THEN 4
           WHEN lr.last_review_score < 3 THEN 4
           WHEN lr.last_review_score < 4 THEN 3
           ELSE 1
         END AS review_risk,
         CASE
           WHEN COALESCE(lc.leave_days_current_year, 0) > 20 THEN 4
           WHEN COALESCE(lc.leave_days_current_year, 0) > 12 THEN 3
           WHEN COALESCE(lc.leave_days_current_year, 0) > 5 THEN 2
           ELSE 1
         END AS leave_risk,
         CASE
           WHEN COALESCE(
                  EXTRACT(YEAR FROM AGE(CURRENT_DATE, lp.last_promo_date)),
                  EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date))
                ) > 5 THEN 4
           WHEN COALESCE(
                  EXTRACT(YEAR FROM AGE(CURRENT_DATE, lp.last_promo_date)),
                  EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date))
                ) > 3 THEN 3
           ELSE 1
         END AS promo_risk
    FROM employees e
    JOIN emp_tenure et ON et.emp_id = e.emp_id
    LEFT JOIN latest_review lr ON lr.emp_id = e.emp_id
    LEFT JOIN leave_count lc ON lc.emp_id = e.emp_id
    LEFT JOIN last_promo lp ON lp.emp_id = e.emp_id
   WHERE et.has_left = 0
)
SELECT emp_id, name, tenure_yrs, last_review_score, leave_days,
       years_since_promo,
       (tenure_risk + review_risk + leave_risk + promo_risk) AS composite_risk_score,
       CASE
         WHEN (tenure_risk + review_risk + leave_risk + promo_risk) >= 14 THEN 'Critical'
         WHEN (tenure_risk + review_risk + leave_risk + promo_risk) >= 10 THEN 'High'
         WHEN (tenure_risk + review_risk + leave_risk + promo_risk) >= 6  THEN 'Medium'
         ELSE 'Low'
       END AS risk_tier
  FROM risk_scores
 ORDER BY composite_risk_score DESC, name;
```

**Explanation:** This capstone pipeline combines four risk dimensions — tenure, review performance, leave usage, and promotion stagnation — into a single composite score. Each dimension is scored 1–4; the sum determines the overall risk tier (Critical / High / Medium / Low). HR can use this to prioritize retention interventions for the most at-risk active employees.

**Alt1:**
```sql
-- PostgreSQL
SELECT d.dept_name,
       ROUND(AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date))), 1) AS avg_tenure_yrs,
       ROUND(AVG(pr.score), 2) AS avg_review_score,
       ROUND(AVG(COALESCE(lc.leave_days, 0)), 1) AS avg_leave_days,
       COUNT(*) FILTER (WHERE lp.last_promo_date IS NULL
                        OR lp.last_promo_date < CURRENT_DATE - INTERVAL '3 years') AS promo_starved
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
  LEFT JOIN performance_reviews pr ON pr.emp_id = e.emp_id
  LEFT JOIN (
    SELECT emp_id, COUNT(*) AS leave_days
      FROM leave_records
     WHERE EXTRACT(YEAR FROM start_date) = EXTRACT(YEAR FROM CURRENT_DATE)
     GROUP BY emp_id
  ) lc ON lc.emp_id = e.emp_id
  LEFT JOIN (
    SELECT emp_id, MAX(promo_date) AS last_promo_date
      FROM promotions GROUP BY emp_id
  ) lp ON lp.emp_id = e.emp_id
 WHERE e.left_date IS NULL
 GROUP BY d.dept_name;
```
**Explanation:** A department roll-up lens on the same four signals — tenure, reviews, leave load, promotion starvation — ranks entire teams instead of individuals.

---
