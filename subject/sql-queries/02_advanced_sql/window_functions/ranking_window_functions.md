# Ranking Window Functions (ROW_NUMBER RANK DENSE_RANK NTILE) — 100 SQL Interview Q&A

## Q1: Rank all employees by salary in descending order across the entire company.

**Query:**
```sql
SELECT
  employee_id,
  first_name,
  last_name,
  salary,
  ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn,
  RANK()       OVER (ORDER BY salary DESC) AS rnk,
  DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rnk
FROM employees;
```
**Explanation:** ROW_NUMBER always assigns unique sequential numbers. RANK leaves gaps after ties. DENSE_RANK leaves no gaps.

---

## Q2: Rank employees by salary within each department, highest salary first.

**Query:**
```sql
SELECT
  department_id,
  employee_id,
  salary,
  ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rn
FROM employees;
```
**Explanation:** PARTITION BY restarts the ranking at 1 for each department.

**Alt1:** Using DENSE_RANK if multiple employees share the top salary per department:
```sql
SELECT department_id, employee_id, salary,
  DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dr
FROM employees;
```

---

## Q3: Show the top 3 highest-paid employees per department.

**Query:**
```sql
WITH ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rn
  FROM employees
)
SELECT department_id, employee_id, first_name, salary
FROM ranked
WHERE rn <= 3;
```
**Explanation:** A CTE computes the row number inside each partition; the outer query filters for the top 3.

**Alt1:** Use a correlated subquery instead of a window function:
```sql
SELECT e1.department_id, e1.employee_id, e1.salary
FROM employees e1
WHERE (
  SELECT COUNT(*)
  FROM employees e2
  WHERE e2.department_id = e1.department_id
    AND e2.salary > e1.salary
) < 3
ORDER BY e1.department_id, e1.salary DESC;
```

---

## Q4: Show all employees who share the top salary in their department (handles ties).

**Query:**
```sql
WITH ranked AS (
  SELECT *,
    RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rnk
  FROM employees
)
SELECT department_id, employee_id, first_name, salary
FROM ranked
WHERE rnk = 1;
```
**Explanation:** RANK returns 1 for all rows tied at the maximum salary, so no tied winner is missed.

---

## Q5: Difference between ROW_NUMBER, RANK, and DENSE_RANK on a sample with ties.

**Query:**
```sql
SELECT
  id,
  score,
  ROW_NUMBER() OVER (ORDER BY score DESC) AS row_num,
  RANK()       OVER (ORDER BY score DESC) AS rank_val,
  DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank_val
FROM test_scores;
```
**Explanation:** For scores 100, 100, 90: ROW_NUMBER gives 1,2,3; RANK gives 1,1,3; DENSE_RANK gives 1,1,2.

**Alt1:** PostgreSQL's `percent_rank` to express the same data as relative fractions:
```sql
SELECT id, score,
  percent_rank() OVER (ORDER BY score DESC) AS pct_rank
FROM test_scores;
```

---

## Q6: Find the second-highest salary in the entire company without using LIMIT.

**Query:**
```sql
WITH ranked AS (
  SELECT salary,
    DENSE_RANK() OVER (ORDER BY salary DESC) AS dr
  FROM employees
)
SELECT DISTINCT salary AS second_highest_salary
FROM ranked
WHERE dr = 2;
```
**Explanation:** DENSE_RANK ensures "second distinct salary" even if multiple employees share it.

**Alt1:** Using a subquery with COUNT(DISTINCT):
```sql
SELECT MAX(salary) AS second_highest_salary
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```

---

## Q7: Find the third-highest salary per department.

**Query:**
```sql
WITH ranked AS (
  SELECT *,
    DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dr
  FROM employees
)
SELECT department_id, salary AS third_highest_salary
FROM ranked
WHERE dr = 3;
```
**Explanation:** DENSE_RANK per partition gives the third distinct salary in each department.

**Alt1:** With ROW_NUMBER combined with DISTINCT you get the same output for tie-free data:
```sql
WITH distinct_salaries AS (
  SELECT DISTINCT department_id, salary
  FROM employees
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rn
  FROM distinct_salaries
)
SELECT department_id, salary AS third_highest_salary
FROM ranked WHERE rn = 3;
```

---

## Q8: Assign row numbers to orders globally ordered by order_date, then order_id.

**Query:**
```sql
SELECT
  order_id,
  customer_id,
  order_date,
  ROW_NUMBER() OVER (ORDER BY order_date, order_id) AS global_row_num
FROM orders;
```
**Explanation:** ORDER BY with multiple keys ensures deterministic, reproducible row numbering.

**Alt1:** Use ROW_NUMBER with an explicit tiebreaker when order_date is nullable:
```sql
SELECT order_id, customer_id, order_date,
  ROW_NUMBER() OVER (ORDER BY COALESCE(order_date, '9999-12-31'), order_id) AS global_row_num
FROM orders;
```

---

## Q9: Rank products by total revenue within each category; return only the #1 product per category.

**Query:**
```sql
WITH product_revenue AS (
  SELECT
    category_id,
    product_id,
    SUM(quantity * unit_price) AS total_revenue
  FROM order_items
  JOIN products USING (product_id)
  GROUP BY category_id, product_id
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY total_revenue DESC) AS rn
  FROM product_revenue
)
SELECT category_id, product_id, total_revenue
FROM ranked
WHERE rn = 1;
```
**Explanation:** Aggregate first, then use ROW_NUMBER in a second pass to pick the top product per category.

---

## Q10: Delete all duplicate rows from a table keeping the row with the lowest id.

**Query:**
```sql
-- MySQL 8+
WITH cte AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY email ORDER BY id ASC) AS rn
  FROM users
)
DELETE FROM users WHERE id IN (SELECT id FROM cte WHERE rn > 1);
```
**Explanation:** ROW_NUMBER partitions by the business key and orders by id; duplicates get rn > 1 and are deleted.

**Alt1:** PostgreSQL approach using ctid:
```sql
DELETE FROM users
WHERE ctid NOT IN (
  SELECT MIN(ctid)
  FROM users
  GROUP BY email
);
```

---

## Q11: Use NTILE to split employees into 4 salary quartiles.

**Query:**
```sql
SELECT
  employee_id,
  first_name,
  salary,
  NTILE(4) OVER (ORDER BY salary DESC) AS salary_quartile
FROM employees;
```
**Explanation:** NTILE(4) divides the result set into 4 roughly equal buckets (1 = top quartile).

**Alt1:** Use PERCENT_RANK + a CASE expression to label quartiles explicitly:
```sql
SELECT employee_id, salary,
  CASE
    WHEN PERCENT_RANK() OVER (ORDER BY salary DESC) < 0.25 THEN 'Q1'
    WHEN PERCENT_RANK() OVER (ORDER BY salary DESC) < 0.50 THEN 'Q2'
    WHEN PERCENT_RANK() OVER (ORDER BY salary DESC) < 0.75 THEN 'Q3'
    ELSE 'Q4'
  END AS salary_quartile
FROM employees;
```

---

## Q12: Use NTILE to divide 1000 rows into deciles (10 groups).

**Query:**
```sql
SELECT
  id,
  value,
  NTILE(10) OVER (ORDER BY value DESC) AS decile
FROM measurements;
```
**Explanation:** NTILE(10) assigns each row a decile from 1 (top 10%) to 10 (bottom 10%).

---

## Q13: Compute percentile_rank and cume_dist for employees ordered by salary.

**Query:**
```sql
SELECT
  employee_id,
  salary,
  PERCENT_RANK() OVER (ORDER BY salary) AS pct_rank,
  CUME_DIST()    OVER (ORDER BY salary) AS cumulative_dist
FROM employees;
```
**Explanation:** PERCENT_RANK = (rank-1)/(rows-1); CUME_DIST = cumulative distribution (fraction of rows <= current).

**Alt1:** NTILE(100) as a rough percentile bucket approximation:
```sql
SELECT employee_id, salary,
  NTILE(100) OVER (ORDER BY salary) AS percentile_bucket
FROM employees;
```

---

## Q14: Use NTILE to create 3 equal-sized test/control groups for an A/B experiment.

**Query:**
```sql
SELECT
  user_id,
  NTILE(3) OVER (ORDER BY RANDOM()) AS experiment_group   -- PostgreSQL
FROM users;
```
**Explanation:** Random ordering before NTILE produces a roughly random assignment into 3 groups.

**Alt1:** MySQL equivalent:
```sql
SELECT user_id,
  NTILE(3) OVER (ORDER BY RAND()) AS experiment_group
FROM users;
```

---

## Q15: Find employees whose salary rank is between 5 and 10 in the company.

**Query:**
```sql
WITH ranked AS (
  SELECT *,
    DENSE_RANK() OVER (ORDER BY salary DESC) AS dr
  FROM employees
)
SELECT employee_id, first_name, salary, dr
FROM ranked
WHERE dr BETWEEN 5 AND 10;
```
**Explanation:** Window function aliases can't be used in WHERE, so a CTE wraps the ranking.

---

## Q16: Rank employees by hire_date ascending to find the most recently hired per department.

**Query:**
```sql
WITH ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY hire_date DESC) AS rn
  FROM employees
)
SELECT department_id, employee_id, first_name, hire_date
FROM ranked
WHERE rn = 1;
```
**Explanation:** ORDER BY hire_date DESC with ROW_NUMBER gives the most recent hire in each department.

**Alt1:** Same result via a NOT EXISTS correlated subquery:
```sql
SELECT e.department_id, e.employee_id, e.first_name, e.hire_date
FROM employees e
WHERE NOT EXISTS (
  SELECT 1 FROM employees e2
  WHERE e2.department_id = e.department_id
    AND e2.hire_date > e.hire_date
);
```

---

## Q17: Rank rows with ORDER BY multiple columns: salary DESC, then last_name ASC.

**Query:**
```sql
SELECT
  employee_id,
  last_name,
  salary,
  ROW_NUMBER() OVER (ORDER BY salary DESC, last_name ASC) AS rn
FROM employees;
```
**Explanation:** Multiple ORDER BY keys break ties deterministically; ROW_NUMBER still produces unique numbers.

---

## Q18: Show the second-highest order per customer using ROW_NUMBER with an offset pattern.

**Query:**
```sql
WITH ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn
  FROM orders
)
SELECT customer_id, order_id, order_date
FROM ranked
WHERE rn = 2;
```
**Explanation:** rn = 2 isolates the second-most-recent order per customer.

**Alt1:** For ties (e.g., two orders on the same date), use RANK instead:
```sql
WITH ranked AS (
  SELECT *,
    RANK() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rnk
  FROM orders
)
SELECT customer_id, order_id, order_date
FROM ranked
WHERE rnk = 2;
```

---

## Q19: Find all employees who have the same salary rank as at least one other employee in their department.

**Query:**
```sql
WITH ranked AS (
  SELECT *,
    DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dr
  FROM employees
)
SELECT r1.*
FROM ranked r1
JOIN ranked r2
  ON r1.department_id = r2.department_id
 AND r1.dr = r2.dr
 AND r1.employee_id <> r2.employee_id;
```
**Explanation:** Self-join on (department, rank) finds every employee whose salary rank is shared.

---

## Q20: Compute the average of ROW_NUMBER values within each department.

**Query:**
```sql
WITH numbered AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rn
  FROM employees
)
SELECT department_id, AVG(rn) AS avg_row_position
FROM numbered
GROUP BY department_id;
```
**Explanation:** Wrapping ROW_NUMBER in a CTE lets you aggregate over its results in a subsequent step.

---

## Q21: Rank employees by salary, then use the rank to compute what fraction of the department each employee represents.

**Query:**
```sql
WITH ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rn,
    COUNT(*) OVER (PARTITION BY department_id) AS dept_size
  FROM employees
)
SELECT department_id, employee_id, salary, rn, dept_size,
  ROUND(rn * 100.0 / dept_size, 1) AS pct_position
FROM ranked;
```
**Explanation:** Combining ROW_NUMBER with COUNT window over the same partition gives a positional percentage.

---

## Q22: Find the top 5 customers by total spending per year using ranking inside a derived table.

**Query:**
```sql
WITH yearly AS (
  SELECT
    customer_id,
    YEAR(order_date) AS order_year,
    SUM(amount) AS total_spent
  FROM orders
  GROUP BY customer_id, YEAR(order_date)
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY order_year ORDER BY total_spent DESC) AS rn
  FROM yearly
)
SELECT order_year, customer_id, total_spent
FROM ranked
WHERE rn <= 5
ORDER BY order_year, rn;
```
**Explanation:** Aggregate → rank → filter. The ranking derived table is joined back to get full details.

---

## Q23: Reverse ranking: rank employees from lowest to highest salary.

**Query:**
```sql
SELECT
  employee_id,
  salary,
  RANK() OVER (ORDER BY salary ASC) AS reverse_rank
FROM employees;
```
**Explanation:** Changing ORDER BY from DESC to ASC reverses the ranking direction.

**Alt1:** Reverse ranking can also be produced from a DESC rank by subtracting:
```sql
WITH counts AS (SELECT COUNT(*) AS n FROM employees)
SELECT employee_id, salary,
  COUNT(*) OVER () - RANK() OVER (ORDER BY salary DESC) + 1 AS reverse_rank
FROM employees CROSS JOIN counts;
```

---

## Q24: Rank from bottom: find the bottom 3 earners in each department.

**Query:**
```sql
WITH ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary ASC) AS rn_asc
  FROM employees
)
SELECT department_id, employee_id, salary
FROM ranked
WHERE rn_asc <= 3;
```
**Explanation:** ORDER BY salary ASC puts the lowest salaries first; ROW_NUMBER then picks the bottom 3.

---

## Q25: Show each department's salary bands using NTILE over the department's own rows.

**Query:**
```sql
SELECT
  department_id,
  employee_id,
  salary,
  NTILE(5) OVER (PARTITION BY department_id ORDER BY salary DESC) AS dept_salary_band
FROM employees;
```
**Explanation:** NTILE inside a PARTITION creates per-department quintile bands.

---

## Q26: Identify ties in a competition: return all contestants tied for positions 1–3 using RANK.

**Query:**
```sql
WITH ranked AS (
  SELECT *,
    RANK() OVER (ORDER BY score DESC) AS rnk
  FROM contestants
)
SELECT contestant_id, score, rnk
FROM ranked
WHERE rnk <= 3
ORDER BY rnk;
```
**Explanation:** RANK allows multiple contestants per position, so all tied for 1st, 2nd, or 3rd appear.

---

## Q27: Use DENSE_RANK to list every distinct salary level in the company from highest to lowest.

**Query:**
```sql
SELECT DISTINCT
  salary,
  DENSE_RANK() OVER (ORDER BY salary DESC) AS salary_level
FROM employees
ORDER BY salary_level;
```
**Explanation:** DISTINCT combined with DENSE_RANK produces one row per unique salary, numbered without gaps.

---

## Q28: Paginate through a large result set using ROW_NUMBER with a page size of 25.

**Query:**
```sql
-- Page 3 (rows 51-75)
WITH numbered AS (
  SELECT *,
    ROW_NUMBER() OVER (ORDER BY employee_id) AS rn
  FROM employees
)
SELECT *
FROM numbered
WHERE rn BETWEEN 51 AND 75;
```
**Explanation:** ROW_NUMBER without PARTITION BY creates a global sequence for keyset-like pagination.

**Alt1:** SQL Server syntax with OFFSET-FETCH (simpler):
```sql
SELECT *
FROM employees
ORDER BY employee_id
OFFSET 50 ROWS FETCH NEXT 25 ROWS ONLY;
```

---

## Q29: Rank customers by their order count, breaking ties by earliest signup date.

**Query:**
```sql
WITH counts AS (
  SELECT customer_id, COUNT(*) AS order_count, MIN(signup_date) AS earliest_signup
  FROM orders
  JOIN customers USING (customer_id)
  GROUP BY customer_id
)
SELECT customer_id, order_count, earliest_signup,
  RANK() OVER (ORDER BY order_count DESC, earliest_signup ASC) AS rnk
FROM counts;
```
**Explanation:** Multiple ORDER BY keys in the window define a deterministic tiebreaker.

---

## Q30: Find employees who are the sole member of their department (count = 1) using COUNT OVER.

**Query:**
```sql
SELECT employee_id, department_id, salary
FROM (
  SELECT *,
    COUNT(*) OVER (PARTITION BY department_id) AS dept_count
  FROM employees
) sub
WHERE dept_count = 1;
```
**Explanation:** COUNT OVER partitions by department; only singleton departments have dept_count = 1.

---

## Q31: Show the running position of each transaction within its account ordered by transaction date.

**Query:**
```sql
SELECT
  account_id,
  transaction_id,
  transaction_date,
  amount,
  ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY transaction_date, transaction_id) AS txn_sequence
FROM transactions;
```
**Explanation:** ROW_NUMBER with PARTITION BY gives each account a sequential transaction counter.

---

## Q32: Find departments where the highest-paid employee ranks in the top 10 company-wide.

**Query:**
```sql
WITH dept_max AS (
  SELECT department_id, MAX(salary) AS max_salary
  FROM employees
  GROUP BY department_id
),
ranked AS (
  SELECT *,
    DENSE_RANK() OVER (ORDER BY max_salary DESC) AS company_rank
  FROM dept_max
)
SELECT department_id, max_salary, company_rank
FROM ranked
WHERE company_rank <= 10;
```
**Explanation:** Aggregate per department, then rank those aggregates across the company.

---

## Q33: Use NTILE(100) to assign percentile buckets to test scores.

**Query:**
```sql
SELECT
  student_id,
  score,
  NTILE(100) OVER (ORDER BY score) AS percentile
FROM test_scores;
```
**Explanation:** NTILE(100) creates 100 buckets; each row gets a percentile from 1 (lowest) to 100 (highest).

---

## Q34: Flag duplicate entries in an orders table by ranking within (customer_id, product_id, order_date).

**Query:**
```sql
SELECT *,
  ROW_NUMBER() OVER (
    PARTITION BY customer_id, product_id, order_date
    ORDER BY order_id
  ) AS dup_rank
FROM orders;
```
**Explanation:** Rows with dup_rank > 1 are duplicates; the row with the lowest order_id is dup_rank = 1.

---

## Q35: Find the median salary per department using NTILE(2) as a median approximation.

**Query:**
```sql
-- Oracle / PostgreSQL with PERCENTILE_CONT
SELECT DISTINCT
  department_id,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary)
    OVER (PARTITION BY department_id) AS median_salary
FROM employees;
```
**Explanation:** PERCENTILE_CONT(0.5) is the true median; NTILE(2) only gives upper/lower halves, not the exact median.

**Alt1:** NTILE(2) for a rough median split:
```sql
SELECT department_id, employee_id, salary,
  NTILE(2) OVER (PARTITION BY department_id ORDER BY salary) AS half
FROM employees;
```

---

## Q36: Rank employees by salary, then compute the average salary of all employees ranked above them.

**Query:**
```sql
WITH ranked AS (
  SELECT *,
    RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employees
)
SELECT r1.employee_id, r1.salary, r1.rnk,
  (SELECT AVG(r2.salary) FROM ranked r2 WHERE r2.rnk < r1.rnk) AS avg_above
FROM ranked r1;
```
**Explanation:** A correlated subquery over the ranked CTE computes the average of higher-ranked salaries.

---

## Q37: Show each order's revenue rank among all orders on the same day.

**Query:**
```sql
SELECT
  order_id,
  order_date,
  revenue,
  DENSE_RANK() OVER (
    PARTITION BY order_date
    ORDER BY revenue DESC
  ) AS daily_rank
FROM orders;
```
**Explanation:** PARTITION BY order_date resets the ranking each day.

---

## Q38: Identify the highest-scoring employee per department, including ties, using a derived table joined back.

**Query:**
```sql
WITH ranked AS (
  SELECT department_id, employee_id, score,
    MAX(score) OVER (PARTITION BY department_id) AS max_dept_score
  FROM employees
)
SELECT department_id, employee_id, score
FROM ranked
WHERE score = max_dept_score;
```
**Explanation:** MAX OVER compares each row to its department's maximum; ties all appear.

**Alt1:** Traditional approach with RANK:
```sql
WITH ranked AS (
  SELECT *, RANK() OVER (PARTITION BY department_id ORDER BY score DESC) AS rnk
  FROM employees
)
SELECT department_id, employee_id, score
FROM ranked WHERE rnk = 1;
```

---

## Q39: Assign sequential IDs to gaps in a non-contiguous id column using ROW_NUMBER.

**Query:**
```sql
SELECT
  original_id,
  value,
  ROW_NUMBER() OVER (ORDER BY original_id) AS sequential_id
FROM sparse_table;
```
**Explanation:** ROW_NUMBER over ORDER BY produces 1,2,3... regardless of gaps in the original id column.

---

## Q40: Rank employees by salary within gender groups.

**Query:**
```sql
SELECT
  employee_id,
  gender,
  salary,
  DENSE_RANK() OVER (PARTITION BY gender ORDER BY salary DESC) AS rank_in_gender
FROM employees;
```
**Explanation:** PARTITION BY gender creates separate ranking streams for each gender.

---

## Q41: For each product, rank its monthly sales and find the month with peak sales. Return only the peak month.

**Query:**
```sql
WITH monthly AS (
  SELECT product_id, DATE_FORMAT(order_date, '%Y-%m') AS sale_month,
    SUM(amount) AS monthly_sales
  FROM order_items
  JOIN orders USING (order_id)
  GROUP BY product_id, DATE_FORMAT(order_date, '%Y-%m')
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY monthly_sales DESC) AS rn
  FROM monthly
)
SELECT product_id, sale_month, monthly_sales
FROM ranked
WHERE rn = 1;
```
**Explanation:** Aggregate monthly, rank per product, keep only the top month.

---

## Q42: Use NTILE(5) to bucket employees into salary quintiles and show average performance score per quintile.

**Query:**
```sql
WITH bucketed AS (
  SELECT *, NTILE(5) OVER (ORDER BY salary) AS quintile
  FROM employees
)
SELECT quintile,
  AVG(performance_score) AS avg_perf_score,
  COUNT(*) AS employee_count
FROM bucketed
GROUP BY quintile
ORDER BY quintile;
```
**Explanation:** NTILE creates quintiles, then aggregation computes stats per quintile.

---

## Q43: Show the dense rank of each city by population, within each state.

**Query:**
```sql
SELECT
  city_id,
  state,
  population,
  DENSE_RANK() OVER (PARTITION BY state ORDER BY population DESC) AS city_rank_in_state
FROM cities;
```
**Explanation:** DENSE_RANK ensures no gaps in ranking within each state partition.

---

## Q44: Find all students who share the same exam rank as another student in the same class.

**Query:**
```sql
WITH ranked AS (
  SELECT class_id, student_id, exam_score,
    DENSE_RANK() OVER (PARTITION BY class_id ORDER BY exam_score DESC) AS exam_rank
  FROM exams
)
SELECT r1.*
FROM ranked r1
INNER JOIN ranked r2
  ON r1.class_id = r2.class_id
 AND r1.exam_rank = r2.exam_rank
 AND r1.student_id <> r2.student_id;
```
**Explanation:** Self-join on the same rank within a class surfaces all students who are tied.

---

## Q45: Rank customer support tickets by resolution time and identify the fastest 10% using CUME_DIST.

**Query:**
```sql
WITH ranked AS (
  SELECT ticket_id, agent_id, resolution_minutes,
    CUME_DIST() OVER (ORDER BY resolution_minutes ASC) AS cum_dist
  FROM support_tickets
)
SELECT ticket_id, agent_id, resolution_minutes
FROM ranked
WHERE cum_dist <= 0.10;
```
**Explanation:** CUME_DIST <= 0.10 captures the fastest-resolving 10% of tickets.

---

## Q46: Assign a global row number to a UNION ALL of two tables and select every 10th row for sampling.

**Query:**
```sql
WITH combined AS (
  SELECT id, 'source_a' AS src FROM table_a
  UNION ALL
  SELECT id, 'source_b' AS src FROM table_b
),
numbered AS (
  SELECT *, ROW_NUMBER() OVER (ORDER BY id) AS rn
  FROM combined
)
SELECT *
FROM numbered
WHERE rn % 10 = 0;
```
**Explanation:** ROW_NUMBER over the union enables modulo-based sampling.

---

## Q47: Rank departments by average salary, then find departments ranked in the top quartile.

**Query:**
```sql
WITH dept_stats AS (
  SELECT department_id, AVG(salary) AS avg_salary
  FROM employees
  GROUP BY department_id
),
ranked AS (
  SELECT *,
    NTILE(4) OVER (ORDER BY avg_salary DESC) AS quartile
  FROM dept_stats
)
SELECT department_id, avg_salary, quartile
FROM ranked
WHERE quartile = 1;
```
**Explanation:** NTILE(4) on aggregated department stats isolates the top-quartile departments.

---

## Q48: Rank transactions within each customer by amount, and compute a cumulative count of high-value transactions (amount > 1000).

**Query:**
```sql
SELECT
  transaction_id,
  customer_id,
  amount,
  ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY amount DESC) AS amt_rank,
  SUM(CASE WHEN amount > 1000 THEN 1 ELSE 0 END)
    OVER (PARTITION BY customer_id ORDER BY amount DESC
          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_high_value_count
FROM transactions;
```
**Explanation:** A conditional sum windowed over the ranked rows gives a running count of high-value transactions.

---

## Q49: Find the salary gap (difference from the next-highest salary) using ROW_NUMBER and LAG.

**Query:**
```sql
WITH ranked AS (
  SELECT salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn
  FROM employees
)
SELECT r1.salary AS current_salary,
  r2.salary AS next_salary,
  r1.salary - r2.salary AS gap
FROM ranked r1
LEFT JOIN ranked r2 ON r1.rn = r2.rn - 1
WHERE r2.salary IS NOT NULL
ORDER BY r1.rn;
```
**Explanation:** A self-join offset by one row_number computes salary gaps between consecutive ranks.

**Alt1:** Using LAG (if permitted alongside ranking):
```sql
SELECT salary,
  salary - LAG(salary) OVER (ORDER BY salary DESC) AS gap
FROM employees;
```

---

## Q50: Rank job postings by application count and show the distribution of application counts across ranks.

**Query:**
```sql
WITH counts AS (
  SELECT job_id, COUNT(*) AS app_count
  FROM applications
  GROUP BY job_id
),
ranked AS (
  SELECT *,
    DENSE_RANK() OVER (ORDER BY app_count DESC) AS popularity_rank
  FROM counts
)
SELECT popularity_rank, COUNT(*) AS num_jobs_at_rank
FROM ranked
GROUP BY popularity_rank
ORDER BY popularity_rank;
```
**Explanation:** Ranking jobs by popularity, then aggregating over the ranks shows the distribution.

---

## Q51: Find employees who are the Nth hire in their department (N = 5).

**Query:**
```sql
WITH ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY hire_date ASC, employee_id) AS hire_order
  FROM employees
)
SELECT department_id, employee_id, first_name, hire_date
FROM ranked
WHERE hire_order = 5;
```
**Explanation:** ROW_NUMBER by hire_date within each department gives the sequential hire order.

---

## Q52: For each employee, show their salary, the company-wide dense rank, and the department-wide dense rank.

**Query:**
```sql
SELECT
  employee_id,
  department_id,
  salary,
  DENSE_RANK() OVER (ORDER BY salary DESC)            AS company_rank,
  DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dept_rank
FROM employees;
```
**Explanation:** Two OVER clauses with different partitioning provide both global and local rankings in one pass.

---

## Q53: Assign 20% random samples from a table using NTILE(5) over randomized ordering.

**Query:**
```sql
WITH bucketed AS (
  SELECT *,
    NTILE(5) OVER (ORDER BY RANDOM()) AS sample_bucket   -- PostgreSQL
  FROM large_table
)
SELECT * FROM bucketed WHERE sample_bucket = 1;
```
**Explanation:** RANDOM() + NTILE(5) creates 5 random groups; selecting bucket 1 yields a ~20% sample.

**Alt1:** MySQL:
```sql
SELECT * FROM (
  SELECT *, NTILE(5) OVER (ORDER BY RAND()) AS sample_bucket
  FROM large_table
) sub
WHERE sample_bucket = 1;
```

---

## Q54: Rank regions by revenue and show a running cumulative revenue total up to and including each rank.

**Query:**
```sql
WITH region_rev AS (
  SELECT region_id, SUM(revenue) AS total_revenue
  FROM sales
  GROUP BY region_id
),
ranked AS (
  SELECT *,
    RANK() OVER (ORDER BY total_revenue DESC) AS rnk
  FROM region_rev
)
SELECT region_id, total_revenue, rnk,
  SUM(total_revenue) OVER (ORDER BY rnk) AS cumulative_revenue
FROM ranked
ORDER BY rnk;
```
**Explanation:** Rank first, then apply a cumulative sum over the ranked order.

---

## Q55: Find the second-most-active user per category by post count.

**Query:**
```sql
WITH post_counts AS (
  SELECT category_id, user_id, COUNT(*) AS post_count
  FROM posts
  GROUP BY category_id, user_id
),
ranked AS (
  SELECT *,
    DENSE_RANK() OVER (PARTITION BY category_id ORDER BY post_count DESC) AS rnk
  FROM post_counts
)
SELECT category_id, user_id, post_count
FROM ranked
WHERE rnk = 2;
```
**Explanation:** DENSE_RANK captures ties at the second position; no active user is excluded.

---

## Q56: Rank employees within their salary band (e.g., 0-50k, 50k-100k, 100k+) by hire date.

**Query:**
```sql
WITH banded AS (
  SELECT *,
    CASE
      WHEN salary < 50000  THEN 'Band A'
      WHEN salary < 100000 THEN 'Band B'
      ELSE 'Band C'
    END AS salary_band
  FROM employees
)
SELECT employee_id, salary_band, hire_date,
  ROW_NUMBER() OVER (PARTITION BY salary_band ORDER BY hire_date) AS hire_order_in_band
FROM banded;
```
**Explanation:** A CASE expression creates the band, then ROW_NUMBER sequences hires within each band.

---

## Q57: Rank posts by comment count and find the median commenter's post using NTILE(2).

**Query:**
```sql
WITH comment_counts AS (
  SELECT post_id, COUNT(*) AS comment_count
  FROM comments
  GROUP BY post_id
),
halved AS (
  SELECT post_id, comment_count,
    NTILE(2) OVER (ORDER BY comment_count) AS half
  FROM comment_counts
)
SELECT post_id, comment_count
FROM halved
WHERE half = 1
ORDER BY comment_count DESC
LIMIT 1;
```
**Explanation:** NTILE(2) splits posts into two halves; the top of the lower half approximates the median.

---

## Q58: Show each employee's salary as a percentage of their department's maximum salary.

**Query:**
```sql
SELECT
  employee_id,
  department_id,
  salary,
  ROUND(salary * 100.0 / MAX(salary) OVER (PARTITION BY department_id), 2) AS pct_of_dept_max
FROM employees;
```
**Explanation:** MAX() OVER provides the department maximum on every row, enabling a simple division.

---

## Q59: Rank movies by box office revenue, then list movies that rank in the top 3 for every genre they appear in.

**Query:**
```sql
WITH genre_rank AS (
  SELECT m.movie_id, m.title, g.genre_name, m.revenue,
    RANK() OVER (PARTITION BY g.genre_name ORDER BY m.revenue DESC) AS genre_rank
  FROM movies m
  JOIN movie_genres g USING (movie_id)
)
SELECT movie_id, title, genre_name, revenue, genre_rank
FROM genre_rank
WHERE genre_rank <= 3;
```
**Explanation:** A movie can appear in multiple genres; each genre partition ranks independently.

---

## Q60: Rank orders by total value per customer, then count how many customers have exactly one order.

**Query:**
```sql
WITH order_totals AS (
  SELECT order_id, customer_id, SUM(amount) AS order_total
  FROM order_items
  GROUP BY order_id, customer_id
),
ranked AS (
  SELECT customer_id, order_id, order_total,
    COUNT(*) OVER (PARTITION BY customer_id) AS order_count
  FROM order_totals
)
SELECT COUNT(DISTINCT customer_id) AS single_order_customers
FROM ranked
WHERE order_count = 1;
```
**Explanation:** COUNT OVER flags customers with exactly one order; a subsequent count provides the metric.

---

## Q61: Rank employees by salary within a salary grade (computed from a grades table) and return the top 2 per grade.

**Query:**
```sql
WITH graded AS (
  SELECT e.employee_id, e.salary, g.grade_level,
    ROW_NUMBER() OVER (PARTITION BY g.grade_level ORDER BY e.salary DESC) AS rn
  FROM employees e
  JOIN salary_grades g
    ON e.salary BETWEEN g.low_salary AND g.high_salary
)
SELECT employee_id, salary, grade_level
FROM graded
WHERE rn <= 2;
```
**Explanation:** JOIN defines salary grades, then ROW_NUMBER picks the top 2 earners per grade.

---

## Q62: Find the gap in a sequence of invoice numbers using ROW_NUMBER over a generated series.

**Query:**
```sql
-- PostgreSQL
WITH seq AS (
  SELECT generate_series(1, (SELECT MAX(invoice_no) FROM invoices)) AS expected_no
),
existing AS (
  SELECT DISTINCT invoice_no FROM invoices
)
SELECT s.expected_no AS missing_invoice_no
FROM seq s
LEFT JOIN existing e ON s.expected_no = e.invoice_no
WHERE e.invoice_no IS NULL;
```
**Explanation:** ROW_NUMBER isn't directly needed here, but comparing against a generated sequence exposes gaps.

**Alt1:** Using ROW_NUMBER to detect gaps in sparse data:
```sql
WITH numbered AS (
  SELECT invoice_no,
    invoice_no - ROW_NUMBER() OVER (ORDER BY invoice_no) AS grp
  FROM invoices
)
SELECT MIN(invoice_no) - 1 AS gap_before, MAX(invoice_no) + 1 AS gap_after
FROM numbered
GROUP BY grp
HAVING MAX(invoice_no) - MIN(invoice_no) > 0;
```

---

## Q63: Rank employees by salary, then find the salary of the employee immediately above and below each employee.

**Query:**
```sql
WITH ranked AS (
  SELECT employee_id, salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC, employee_id) AS rn
  FROM employees
)
SELECT r1.employee_id, r1.salary,
  r2.salary AS salary_above,
  r3.salary AS salary_below
FROM ranked r1
LEFT JOIN ranked r2 ON r2.rn = r1.rn - 1
LEFT JOIN ranked r3 ON r3.rn = r1.rn + 1;
```
**Explanation:** Self-joins at rn-1 and rn+1 retrieve neighboring salaries from the ranked list.

---

## Q64: Assign each sale to a "sales bucket" of 100 transactions each using ROW_NUMBER and integer division.

**Query:**
```sql
SELECT
  sale_id,
  sale_amount,
  FLOOR((ROW_NUMBER() OVER (ORDER BY sale_id) - 1) / 100) + 1 AS bucket_number
FROM sales;
```
**Explanation:** ROW_NUMBER divided by bucket size creates sequential batch numbers for processing.

---

## Q65: Rank students by GPA within each major, breaking ties alphabetically by name.

**Query:**
```sql
SELECT
  student_id,
  major,
  gpa,
  name,
  RANK() OVER (PARTITION BY major ORDER BY gpa DESC, name ASC) AS gpa_rank
FROM students;
```
**Explanation:** The second ORDER BY key (name ASC) ensures a deterministic tiebreaker.

---

## Q66: Find all departments where the employee with the median hire date was hired in 2023.

**Query:**
```sql
-- SQL Server / PostgreSQL
WITH numbered AS (
  SELECT department_id, hire_date,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY hire_date) AS rn,
    COUNT(*) OVER (PARTITION BY department_id) AS cnt
  FROM employees
)
SELECT department_id
FROM numbered
WHERE rn = FLOOR((cnt + 1) / 2.0)
  AND hire_date >= '2023-01-01'
  AND hire_date < '2024-01-01';
```
**Explanation:** The middle row_number (computed from COUNT) identifies the median; filtering on hire_date answers the question.

---

## Q67: Rank songs by play count per playlist, and show the play count of the song ranked exactly above each song.

**Query:**
```sql
WITH ranked AS (
  SELECT playlist_id, song_id, play_count,
    ROW_NUMBER() OVER (PARTITION BY playlist_id ORDER BY play_count DESC) AS rn
  FROM playlist_plays
)
SELECT r1.playlist_id, r1.song_id, r1.play_count,
  r2.play_count AS play_count_above
FROM ranked r1
LEFT JOIN ranked r2
  ON r1.playlist_id = r2.playlist_id
 AND r2.rn = r1.rn - 1;
```
**Explanation:** Self-join on rn-1 retrieves the next-higher play count for comparison.

---

## Q68: Find the top 1% of earners using PERCENT_RANK.

**Query:**
```sql
WITH ranked AS (
  SELECT employee_id, salary,
    PERCENT_RANK() OVER (ORDER BY salary DESC) AS pct
  FROM employees
)
SELECT employee_id, salary
FROM ranked
WHERE pct <= 0.01;
```
**Explanation:** PERCENT_RANK <= 0.01 selects the top 1% of earners in the distribution.

---

## Q69: Rank warehouses by inventory value and calculate what percentage of total inventory each warehouse holds.

**Query:**
```sql
WITH warehouse_values AS (
  SELECT warehouse_id, SUM(quantity * unit_cost) AS inventory_value
  FROM inventory
  GROUP BY warehouse_id
)
SELECT warehouse_id, inventory_value,
  ROUND(inventory_value * 100.0 / SUM(inventory_value) OVER(), 2) AS pct_of_total,
  RANK() OVER (ORDER BY inventory_value DESC) AS value_rank
FROM warehouse_values;
```
**Explanation:** SUM() OVER () gives the grand total; division yields each warehouse's share.

---

## Q70: Rank transactions per account and find accounts where the 2nd transaction was more than double the 1st.

**Query:**
```sql
WITH ranked AS (
  SELECT account_id, transaction_id, amount,
    ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY transaction_date, transaction_id) AS txn_seq
  FROM transactions
)
SELECT r1.account_id
FROM ranked r1
JOIN ranked r2
  ON r1.account_id = r2.account_id
 AND r1.txn_seq = 1
 AND r2.txn_seq = 2
WHERE r2.amount > 2 * r1.amount;
```
**Explanation:** Joining txn_seq 1 and 2 per account allows a direct comparison.

---

## Q71: Show a dense rank of countries by number of customers, skipping ranks where count = 0.

**Query:**
```sql
WITH counts AS (
  SELECT country, COUNT(*) AS customer_count
  FROM customers
  GROUP BY country
)
SELECT country, customer_count,
  DENSE_RANK() OVER (ORDER BY customer_count DESC) AS popularity_rank
FROM counts
ORDER BY popularity_rank;
```
**Explanation:** DENSE_RANK avoids gaps; countries with equal counts share the same rank.

---

## Q72: Find employees whose ROW_NUMBER within department equals their DENSE_RANK across the company.

**Query:**
```sql
WITH dual_ranked AS (
  SELECT employee_id, department_id, salary,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dept_rn,
    DENSE_RANK() OVER (ORDER BY salary DESC) AS company_dr
  FROM employees
)
SELECT employee_id, department_id, salary, dept_rn, company_dr
FROM dual_ranked
WHERE dept_rn = company_dr;
```
**Explanation:** Matching department row number to company dense rank highlights structural coincidences.

---

## Q73: Assign a rank to each product's daily sales position and compute the average daily rank per product over a month.

**Query:**
```sql
WITH daily AS (
  SELECT product_id, order_date, SUM(amount) AS daily_sales
  FROM order_items oi JOIN orders o USING (order_id)
  GROUP BY product_id, order_date
),
ranked AS (
  SELECT product_id, order_date, daily_sales,
    RANK() OVER (PARTITION BY order_date ORDER BY daily_sales DESC) AS daily_rank
  FROM daily
)
SELECT product_id,
  ROUND(AVG(daily_rank), 2) AS avg_daily_rank,
  MIN(daily_rank) AS best_daily_rank,
  MAX(daily_rank) AS worst_daily_rank
FROM ranked
WHERE order_date >= '2025-01-01' AND order_date < '2025-02-01'
GROUP BY product_id
ORDER BY avg_daily_rank;
```
**Explanation:** Ranking per day then averaging across days provides a robust monthly performance metric.

---

## Q74: For each customer, rank their payments from most to least recent, then compute the running average payment amount.

**Query:**
```sql
SELECT
  customer_id,
  payment_id,
  payment_date,
  amount,
  ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY payment_date DESC) AS payment_seq,
  AVG(amount) OVER (
    PARTITION BY customer_id
    ORDER BY payment_date DESC
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_avg_amount
FROM payments;
```
**Explanation:** A cumulative average window over the ROW_NUMBER-ordered sequence smooths payment trends.

---

## Q75: Rank U.S. states by population using DENSE_RANK, then list only ranks where at least 3 states share the same population range.

**Query:**
```sql
WITH state_pop AS (
  SELECT state, population,
    DENSE_RANK() OVER (ORDER BY population DESC) AS pop_rank
  FROM states
),
rank_counts AS (
  SELECT pop_rank, COUNT(*) AS states_at_rank
  FROM state_pop
  GROUP BY pop_rank
)
SELECT s.state, s.population, s.pop_rank
FROM state_pop s
JOIN rank_counts rc USING (pop_rank)
WHERE rc.states_at_rank >= 3
ORDER BY s.pop_rank;
```
**Explanation:** Counting states per rank then filtering ensures only broadly shared ranks appear.

---

## Q76: Find the exact row that is the median of a table using ROW_NUMBER and COUNT.

**Query:**
```sql
-- SQL Server
WITH numbered AS (
  SELECT *,
    ROW_NUMBER() OVER (ORDER BY id) AS rn,
    COUNT(*) OVER () AS total
  FROM my_table
)
SELECT *
FROM numbered
WHERE rn IN ((total + 1) / 2, (total + 2) / 2);
```
**Explanation:** For even counts, two middle rows are returned; for odd counts, one row. This is a classic median CTE.

---

## Q77: Rank movie ratings by a user and identify the user's most controversial movie (smallest gap between any two ratings for the same user).

**Query:**
```sql
WITH ranked AS (
  SELECT user_id, movie_id, rating,
    LAG(rating)  OVER (PARTITION BY user_id ORDER BY rating) AS prev_rating,
    LEAD(rating) OVER (PARTITION BY user_id ORDER BY rating) AS next_rating
  FROM ratings
)
-- Simplified: find the range of ratings per user
SELECT user_id,
  MAX(rating) - MIN(rating) AS rating_range
FROM ratings
GROUP BY user_id
HAVING MAX(rating) - MIN(rating) = (
  SELECT MAX(r2.rating) - MIN(r2.rating)
  FROM ratings r2
)
ORDER BY user_id;
```
**Explanation:** The user with the smallest range has the most consistent (least controversial) taste; largest range is most controversial.

---

## Q78: Rank nodes in a tree table by depth (level) using ROW_NUMBER within each level.

**Query:**
```sql
WITH RECURSIVE tree AS (
  SELECT node_id, parent_id, 0 AS depth
  FROM nodes WHERE parent_id IS NULL
  UNION ALL
  SELECT n.node_id, n.parent_id, t.depth + 1
  FROM nodes n JOIN tree t ON n.parent_id = t.node_id
)
SELECT node_id, parent_id, depth,
  ROW_NUMBER() OVER (PARTITION BY depth ORDER BY node_id) AS position_in_level
FROM tree;
```
**Explanation:** A recursive CTE computes depth; ROW_NUMBER within each depth gives breadth-first ordering.

---

## Q79: Rank departments by the number of distinct projects each has, and show cumulative count up to each rank.

**Query:**
```sql
WITH dept_projects AS (
  SELECT department_id, COUNT(DISTINCT project_id) AS project_count
  FROM employee_projects ep
  JOIN employees e USING (employee_id)
  GROUP BY department_id
),
ranked AS (
  SELECT *,
    RANK() OVER (ORDER BY project_count DESC) AS rnk
  FROM dept_projects
)
SELECT department_id, project_count, rnk,
  SUM(project_count) OVER (ORDER BY rnk) AS cumulative_projects
FROM ranked;
```
**Explanation:** Aggregate first, rank the aggregates, then sum cumulatively over the ranks.

---

## Q80: Assign each customer a loyalty tier (Gold/Silver/Bronze) using NTILE(3) over total spend.

**Query:**
```sql
WITH spend AS (
  SELECT customer_id, SUM(amount) AS total_spend
  FROM orders
  GROUP BY customer_id
),
tiers AS (
  SELECT customer_id, total_spend,
    NTILE(3) OVER (ORDER BY total_spend DESC) AS tier_num
  FROM spend
)
SELECT customer_id, total_spend,
  CASE tier_num
    WHEN 1 THEN 'Gold'
    WHEN 2 THEN 'Silver'
    WHEN 3 THEN 'Bronze'
  END AS loyalty_tier
FROM tiers;
```
**Explanation:** NTILE(3) splits customers into three equal tiers by spend; CASE maps numbers to names.

---

## Q81: Rank each employee's performance rating against others in the same job title.

**Query:**
```sql
SELECT
  employee_id,
  job_title,
  performance_rating,
  DENSE_RANK() OVER (PARTITION BY job_title ORDER BY performance_rating DESC) AS rating_rank_in_role
FROM employees;
```
**Explanation:** Partitioning by job title ensures fair comparison among peers.

---

## Q82: Find the most common order quantity per product using RANK on frequency.

**Query:**
```sql
WITH qty_freq AS (
  SELECT product_id, quantity, COUNT(*) AS freq
  FROM order_items
  GROUP BY product_id, quantity
),
ranked AS (
  SELECT *,
    RANK() OVER (PARTITION BY product_id ORDER BY freq DESC) AS freq_rank
  FROM qty_freq
)
SELECT product_id, quantity, freq
FROM ranked
WHERE freq_rank = 1;
```
**Explanation:** Ranking quantities by frequency per product isolates the most commonly ordered quantity.

---

## Q83: Show each order's revenue rank among all orders by the same customer, and compute the revenue difference from the customer's top order.

**Query:**
```sql
WITH ranked AS (
  SELECT order_id, customer_id, revenue,
    RANK() OVER (PARTITION BY customer_id ORDER BY revenue DESC) AS rnk,
    MAX(revenue) OVER (PARTITION BY customer_id) AS max_rev
  FROM orders
)
SELECT order_id, customer_id, revenue, rnk,
  max_rev - revenue AS gap_from_top
FROM ranked
WHERE rnk <= 5;
```
**Explanation:** MAX OVER provides each customer's top order on every row, enabling a direct gap calculation.

---

## Q84: Assign row numbers to a JSON array's elements unpacked into rows.

**Query:**
```sql
-- PostgreSQL
SELECT
  item->>'id' AS item_id,
  item->>'name' AS item_name,
  ROW_NUMBER() OVER (ORDER BY (item->>'id')::int) AS position
FROM json_array_elements('[{"id":1,"name":"a"},{"id":2,"name":"b"}]') AS item;
```
**Explanation:** ROW_NUMBER assigns a position to each element extracted from the JSON array.

---

## Q85: Rank salespeople by deal count, then find the average deal size for each rank position.

**Query:**
```sql
WITH deal_counts AS (
  SELECT salesperson_id, COUNT(*) AS deal_count
  FROM deals
  WHERE status = 'closed_won'
  GROUP BY salesperson_id
),
ranked AS (
  SELECT *,
    RANK() OVER (ORDER BY deal_count DESC) AS deal_rank
  FROM deal_counts
)
SELECT deal_rank, AVG(deal_count) AS avg_deals_at_rank
FROM ranked
GROUP BY deal_rank
ORDER BY deal_rank;
```
**Explanation:** Ranking salespeople then averaging within each rank reveals how many deals per rank tier.

---

## Q86: Use ROW_NUMBER to detect the first occurrence of each event type per user and flag it.

**Query:**
```sql
SELECT *,
  CASE WHEN ROW_NUMBER() OVER (PARTITION BY user_id, event_type ORDER BY event_time) = 1
    THEN 'first_occurrence' ELSE 'repeat'
  END AS occurrence_flag
FROM events;
```
**Explanation:** ROW_NUMBER = 1 within each (user, event_type) partition identifies first occurrences.

**Alt1:** Using a correlated subquery:
```sql
SELECT e.*,
  CASE WHEN e.event_time = (
    SELECT MIN(e2.event_time) FROM events e2
    WHERE e2.user_id = e.user_id AND e2.event_type = e.event_type
  ) THEN 'first_occurrence' ELSE 'repeat'
  END AS occurrence_flag
FROM events e;
```

---

## Q87: Rank products by the number of 5-star reviews they received, then show products ranked exactly 10th.

**Query:**
```sql
WITH five_star AS (
  SELECT product_id, COUNT(*) AS five_star_count
  FROM reviews
  WHERE rating = 5
  GROUP BY product_id
),
ranked AS (
  SELECT *,
    DENSE_RANK() OVER (ORDER BY five_star_count DESC) AS rnk
  FROM five_star
)
SELECT product_id, five_star_count, rnk
FROM ranked
WHERE rnk = 10;
```
**Explanation:** DENSE_RANK ensures products with equal review counts share the same rank.

---

## Q88: Rank each employee's salary relative to their salary band midpoint, showing who is furthest above midpoint.

**Query:**
```sql
WITH midpoints AS (
  SELECT employee_id, salary, salary_band,
    (low_bound + high_bound) / 2.0 AS midpoint
  FROM employees e
  JOIN salary_bands sb ON e.salary_band = sb.band_name
)
SELECT employee_id, salary, salary_band, midpoint,
  ROUND((salary - midpoint) / midpoint * 100, 2) AS pct_above_midpoint,
  RANK() OVER (ORDER BY (salary - midpoint) / midpoint DESC) AS above_midpoint_rank
FROM midpoints;
```
**Explanation:** Computing the distance from midpoint then ranking surfaces outliers above band expectations.

---

## Q89: Find employees who changed departments, and rank their salary progression within each department they've been in.

**Query:**
```sql
SELECT
  employee_id,
  department_id,
  effective_date,
  salary,
  ROW_NUMBER() OVER (PARTITION BY employee_id, department_id ORDER BY effective_date) AS dept_salary_seq
FROM salary_history
WHERE department_id IS NOT NULL;
```
**Explanation:** Partitioning by both employee and department gives the sequential salary change order within each department.

---

## Q90: Assign groups of 50 employees each to an "on-call rotation" using NTILE with explicit count.

**Query:**
```sql
SELECT
  employee_id,
  first_name,
  NTILE((SELECT CEIL(COUNT(*) / 50.0) FROM employees) )
    OVER (ORDER BY employee_id) AS rotation_group
FROM employees;
```
**Explanation:** NTILE with a computed number of buckets distributes employees into ~50-person groups.

**Alt1:** Manual bucketing using ROW_NUMBER and arithmetic:
```sql
WITH numbered AS (
  SELECT *, ROW_NUMBER() OVER (ORDER BY employee_id) AS rn
  FROM employees
)
SELECT employee_id, first_name,
  CEIL(rn / 50.0) AS rotation_group
FROM numbered;
```

---

## Q91: Rank bank transactions by amount within each account and identify which transaction broke the 3-consecutive-deposit streak.

**Query:**
```sql
WITH ranked AS (
  SELECT account_id, transaction_id, amount, transaction_date,
    ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY transaction_date) AS txn_seq
  FROM bank_transactions
  WHERE type = 'deposit'
)
SELECT r1.account_id, r1.transaction_id AS streak_breaker
FROM ranked r1
LEFT JOIN ranked r2
  ON r1.account_id = r2.account_id
 AND r2.txn_seq = r1.txn_seq - 1
LEFT JOIN ranked r3
  ON r1.account_id = r3.account_id
 AND r3.txn_seq = r1.txn_seq - 2
WHERE r2.transaction_id IS NULL OR r3.transaction_id IS NULL;
```
**Explanation:** Self-joins check for consecutive predecessors; missing predecessors mark streak breaks.

---

## Q92: Rank employees by performance score, then show a percentile bucket (quartile) alongside the rank.

**Query:**
```sql
SELECT
  employee_id,
  performance_score,
  RANK() OVER (ORDER BY performance_score DESC) AS score_rank,
  NTILE(4) OVER (ORDER BY performance_score DESC) AS quartile
FROM employees;
```
**Explanation:** Running both RANK and NTILE in the same SELECT provides both precise position and bucket.

---

## Q93: For each date, rank products by units sold and find the product that held the #1 spot for the most days.

**Query:**
```sql
WITH daily_sales AS (
  SELECT order_date, product_id, SUM(units) AS daily_units
  FROM sales
  GROUP BY order_date, product_id
),
ranked AS (
  SELECT order_date, product_id,
    RANK() OVER (PARTITION BY order_date ORDER BY daily_units DESC) AS daily_rank
  FROM daily_sales
)
SELECT product_id, COUNT(*) AS days_at_top
FROM ranked
WHERE daily_rank = 1
GROUP BY product_id
ORDER BY days_at_top DESC
LIMIT 1;
```
**Explanation:** Rank per day, filter #1 spots, then count days per product.

---

## Q94: Rank items in a shopping cart by price (highest first) and assign a display_order for the UI.

**Query:**
```sql
SELECT
  cart_id,
  product_id,
  product_name,
  price,
  ROW_NUMBER() OVER (PARTITION BY cart_id ORDER BY price DESC) AS display_order
FROM cart_items;
```
**Explanation:** ROW_NUMBER within each cart creates a deterministic display sequence by price.

---

## Q95: Rank cities by temperature change year-over-year and identify the top 5 cities with the largest swings.

**Query:**
```sql
WITH yearly_temps AS (
  SELECT city_id, YEAR(recorded_date) AS yr, AVG(temperature) AS avg_temp
  FROM weather_records
  GROUP BY city_id, YEAR(recorded_date)
),
pivoted AS (
  SELECT a.city_id,
    a.avg_temp - b.avg_temp AS temp_change
  FROM yearly_temps a
  JOIN yearly_temps b
    ON a.city_id = b.city_id
   AND a.yr = b.yr + 1
)
SELECT city_id, temp_change,
  RANK() OVER (ORDER BY ABS(temp_change) DESC) AS swing_rank
FROM pivoted
WHERE RANK() OVER (ORDER BY ABS(temp_change) DESC) <= 5;
```
**Explanation:** Year-over-year temperature difference ranked by absolute swing identifies volatile climates.

---

## Q96: Rank transactions and compute a running total, then find the transaction where the running total first exceeds 10,000.

**Query:**
```sql
WITH ranked AS (
  SELECT transaction_id, amount,
    SUM(amount) OVER (ORDER BY transaction_date, transaction_id
                      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
    ROW_NUMBER() OVER (ORDER BY transaction_date, transaction_id) AS rn
  FROM transactions
)
SELECT transaction_id, amount, running_total
FROM ranked
WHERE running_total >= 10000
ORDER BY rn
LIMIT 1;
```
**Explanation:** A cumulative sum window identifies when the threshold is crossed; LIMIT 1 gets the first occurrence.

---

## Q97: Rank suppliers by defect rate per product category and identify the worst supplier in each category.

**Query:**
```sql
WITH defect_rates AS (
  SELECT supplier_id, category_id,
    SUM(CASE WHEN defect = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS defect_rate
  FROM shipments
  GROUP BY supplier_id, category_id
),
ranked AS (
  SELECT *,
    RANK() OVER (PARTITION BY category_id ORDER BY defect_rate DESC) AS worst_rank
  FROM defect_rates
)
SELECT supplier_id, category_id, defect_rate
FROM ranked
WHERE worst_rank = 1;
```
**Explanation:** Aggregating defect rate then ranking per category isolates the worst supplier in each.

---

## Q98: Rank employees by the number of projects completed and find the dense rank of their project count.

**Query:**
```sql
WITH project_counts AS (
  SELECT employee_id, COUNT(*) AS completed_projects
  FROM projects
  WHERE status = 'completed'
  GROUP BY employee_id
)
SELECT employee_id, completed_projects,
  DENSE_RANK() OVER (ORDER BY completed_projects DESC) AS productivity_rank
FROM project_counts;
```
**Explanation:** DENSE_RANK gives a gapless ranking of productivity tiers.

---

## Q99: Find all ties in an exam results table: students who share the same rank for the top 3 positions.

**Query:**
```sql
WITH ranked AS (
  SELECT student_id, score,
    RANK() OVER (ORDER BY score DESC) AS rnk
  FROM exam_results
),
tied AS (
  SELECT rnk, COUNT(*) AS tie_count
  FROM ranked
  WHERE rnk <= 3
  GROUP BY rnk
  HAVING COUNT(*) > 1
)
SELECT r1.student_id, r1.score, r1.rnk
FROM ranked r1
JOIN tied t ON r1.rnk = t.rnk;
```
**Explanation:** First find which top-3 ranks have ties (count > 1), then join back to get the actual students.

---

## Q100: Combine NTILE, DENSE_RANK, and ROW_NUMBER in one query to fully describe each employee's salary position: global percentile, dense rank, and sequential row.

**Query:**
```sql
SELECT
  employee_id,
  department_id,
  salary,
  NTILE(100)       OVER (ORDER BY salary DESC) AS percentile_bucket,
  DENSE_RANK()      OVER (ORDER BY salary DESC) AS global_dense_rank,
  ROW_NUMBER()      OVER (ORDER BY salary DESC) AS global_row_number,
  NTILE(4)          OVER (PARTITION BY department_id ORDER BY salary DESC) AS dept_quartile,
  DENSE_RANK()      OVER (PARTITION BY department_id ORDER BY salary DESC) AS dept_dense_rank
FROM employees;
```
**Explanation:** This single query produces five complementary views of each employee's salary position: global percentile, gapless rank, unique sequence, department quartile, and department dense rank.
