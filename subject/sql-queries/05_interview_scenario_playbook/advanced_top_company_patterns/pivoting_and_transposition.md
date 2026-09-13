# Pivoting and Transposition — 100 Interview Q&A

## Q1: Basic Conditional Aggregation — Sales by Quarter

**Scenario:** You have quarterly sales figures per employee. Pivot rows into columns so each row shows one employee with Q1–Q4 as separate columns.

**Schema:** `employee_sales (emp_id INT, emp_name VARCHAR, quarter VARCHAR, sales DECIMAL)`

**Query:**
```sql
SELECT
  emp_id,
  emp_name,
  SUM(CASE WHEN quarter = 'Q1' THEN sales ELSE 0 END) AS Q1,
  SUM(CASE WHEN quarter = 'Q2' THEN sales ELSE 0 END) AS Q2,
  SUM(CASE WHEN quarter = 'Q3' THEN sales ELSE 0 END) AS Q3,
  SUM(CASE WHEN quarter = 'Q4' THEN sales ELSE 0 END) AS Q4
FROM employee_sales
GROUP BY emp_id, emp_name;
```
**Explanation:** Conditional aggregation with `SUM(CASE WHEN ...)` is the most portable pivot technique — works on every SQL dialect. NULLs default to 0 via the ELSE clause.

**Alt1 (SQL Server PIVOT + MySQL conditional agg rewrite):**
```sql
-- SQL Server PIVOT
SELECT emp_id, emp_name, Q1, Q2, Q3, Q4
FROM (
  SELECT emp_id, emp_name, quarter, sales
  FROM employee_sales
) src
PIVOT (
  SUM(sales) FOR quarter IN (Q1, Q2, Q3, Q4)
) pvt;

-- MySQL conditional aggregation (same as primary)
SELECT
  emp_id,
  emp_name,
  IFNULL(SUM(CASE WHEN quarter = 'Q1' THEN sales END), 0) AS Q1,
  IFNULL(SUM(CASE WHEN quarter = 'Q2' THEN sales END), 0) AS Q2,
  IFNULL(SUM(CASE WHEN quarter = 'Q3' THEN sales END), 0) AS Q3,
  IFNULL(SUM(CASE WHEN quarter = 'Q4' THEN sales END), 0) AS Q4
FROM employee_sales
GROUP BY emp_id, emp_name;
```

---

## Q2: PIVOT with Aggregated Values — Product Revenue by Region

**Scenario:** Flatten a `product_revenue` table so each row is a product and each column is a region's total revenue.

**Schema:** `product_revenue (product VARCHAR, region VARCHAR, revenue DECIMAL)`

**Query:**
```sql
SELECT
  product,
  SUM(CASE WHEN region = 'East'  THEN revenue ELSE 0 END) AS East,
  SUM(CASE WHEN region = 'West'  THEN revenue ELSE 0 END) AS West,
  SUM(CASE WHEN region = 'North' THEN revenue ELSE 0 END) AS North,
  SUM(CASE WHEN region = 'South' THEN revenue ELSE 0 END) AS South
FROM product_revenue
GROUP BY product;
```
**Explanation:** Classic matrix pivot — products as rows, regions as columns. The ELSE 0 ensures no NULLs appear in the output.

**Alt1 (SQL Server PIVOT):**
```sql
SELECT product, [East], [West], [North], [South]
FROM (
  SELECT product, region, revenue FROM product_revenue
) src
PIVOT (
  SUM(revenue) FOR region IN ([East], [West], [North], [South])
) pvt;
```

---

## Q3: Count Pivot — Users per Status per Month

**Scenario:** Count how many users have each status (active, inactive, banned) per month. Months become columns.

**Schema:** `user_status_log (user_id INT, status VARCHAR, recorded_on DATE)`

**Query:**
```sql
SELECT
  DATE_TRUNC('month', recorded_on)::DATE AS month,
  COUNT(*) FILTER (WHERE status = 'active')   AS active,
  COUNT(*) FILTER (WHERE status = 'inactive') AS inactive,
  COUNT(*) FILTER (WHERE status = 'banned')   AS banned
FROM user_status_log
GROUP BY DATE_TRUNC('month', recorded_on)
ORDER BY month;
```
**Explanation:** PostgreSQL's `FILTER (WHERE ...)` clause on aggregate functions is a concise alternative to CASE-based pivoting for counts.

**Alt1 (PostgreSQL CROSSTAB):**
```sql
-- Requires: CREATE EXTENSION IF NOT EXISTS tablefunc;
SELECT * FROM crosstab(
  $$
  SELECT DATE_TRUNC('month', recorded_on)::DATE, status, COUNT(*)::INT
  FROM user_status_log
  GROUP BY 1, 2
  ORDER BY 1, 2
  $$,
  $$ VALUES ('active'), ('inactive'), ('banned') $$
) AS ct(month DATE, active INT, inactive INT, banned INT);
```

---

## Q4: Oracle PIVOT — Monthly Sales Pivot

**Scenario:** Pivot `monthly_sales` so each department becomes a column with total sales.

**Schema:** `monthly_sales (dept VARCHAR, sale_month VARCHAR, amount NUMBER)`

**Query:**
```sql
SELECT *
FROM monthly_sales
PIVOT (
  SUM(amount)
  FOR sale_month IN ('2024-01' AS jan, '2024-02' AS feb, '2024-03' AS mar)
);
```
**Explanation:** Oracle's PIVOT operator directly aggregates and transposes. Column aliases are assigned in the IN list.

**Alt1 (Oracle conditional aggregation):**
```sql
SELECT
  dept,
  SUM(CASE WHEN sale_month = '2024-01' THEN amount ELSE 0 END) AS jan,
  SUM(CASE WHEN sale_month = '2024-02' THEN amount ELSE 0 END) AS feb,
  SUM(CASE WHEN sale_month = '2024-03' THEN amount ELSE 0 END) AS mar
FROM monthly_sales
GROUP BY dept;
```

---

## Q5: Conditional Aggregation with AVG — Average Scores by Category

**Scenario:** Pivot average test scores by category (math, science, english) per student.

**Schema:** `test_scores (student_id INT, student_name VARCHAR, category VARCHAR, score DECIMAL)`

**Query:**
```sql
SELECT
  student_id,
  student_name,
  ROUND(AVG(CASE WHEN category = 'math'    THEN score END), 2) AS avg_math,
  ROUND(AVG(CASE WHEN category = 'science' THEN score END), 2) AS avg_science,
  ROUND(AVG(CASE WHEN category = 'english' THEN score END), 2) AS avg_english
FROM test_scores
GROUP BY student_id, student_name;
```
**Explanation:** Using AVG inside CASE with no ELSE returns NULL for non-matching rows, which AVG correctly ignores — only averaging actual scores per category.

**Alt1 (MySQL conditional agg):**
```sql
SELECT
  student_id,
  student_name,
  ROUND(AVG(CASE WHEN category = 'math'    THEN score END), 2) AS avg_math,
  ROUND(AVG(CASE WHEN category = 'science' THEN score END), 2) AS avg_science,
  ROUND(AVG(CASE WHEN category = 'english' THEN score END), 2) AS avg_english
FROM test_scores
GROUP BY student_id, student_name;
```

---

## Q6: Pivot with Multiple Aggregates — Revenue and Orders by Channel

**Scenario:** Show both total revenue and order count per sales channel, pivoted into columns per product category.

**Schema:** `orders (order_id INT, category VARCHAR, channel VARCHAR, revenue DECIMAL)`

**Query:**
```sql
SELECT
  category,
  SUM(CASE WHEN channel = 'online'  THEN revenue ELSE 0 END)  AS online_revenue,
  COUNT(CASE WHEN channel = 'online'  THEN 1 END)              AS online_orders,
  SUM(CASE WHEN channel = 'offline' THEN revenue ELSE 0 END)  AS offline_revenue,
  COUNT(CASE WHEN channel = 'offline' THEN 1 END)              AS offline_orders
FROM orders
GROUP BY category;
```
**Explanation:** Pivoting multiple aggregates requires placing each aggregate inside its own CASE expression. SQL Server PIVOT only supports one aggregate per pivot, making conditional aggregation more flexible here.

---

## Q7: PostgreSQL CROSSTAB — Employee Department History

**Scenario:** Show each employee's department assignment across quarters using CROSSTAB.

**Schema:** `dept_history (emp_id INT, quarter VARCHAR, dept VARCHAR)`

**Query:**
```sql
SELECT * FROM crosstab(
  $$
  SELECT emp_id, quarter, dept
  FROM dept_history
  ORDER BY 1, 2
  $$,
  $$ VALUES ('Q1'), ('Q2'), ('Q3'), ('Q4') $$
) AS ct(emp_id INT, q1_dept VARCHAR, q2_dept VARCHAR, q3_dept VARCHAR, q4_dept VARCHAR);
```
**Explanation:** CROSSTAB requires a category SQL (second parameter) defining the fixed column order. The source query must be sorted by row_category, column_category.

**Alt1 (Conditional aggregation):**
```sql
SELECT
  emp_id,
  MAX(CASE WHEN quarter = 'Q1' THEN dept END) AS q1_dept,
  MAX(CASE WHEN quarter = 'Q2' THEN dept END) AS q2_dept,
  MAX(CASE WHEN quarter = 'Q3' THEN dept END) AS q3_dept,
  MAX(CASE WHEN quarter = 'Q4' THEN dept END) AS q4_dept
FROM dept_history
GROUP BY emp_id;
```

---

## Q8: Pivot on MAX Value — Latest Status per Device

**Scenario:** Each device reports multiple status checks. Pivot to show the latest status check time for each status type per device.

**Schema:** `device_logs (device_id INT, status VARCHAR, checked_at TIMESTAMP)`

**Query:**
```sql
SELECT
  device_id,
  MAX(CASE WHEN status = 'online'  THEN checked_at END) AS last_online,
  MAX(CASE WHEN status = 'offline' THEN checked_at END) AS last_offline,
  MAX(CASE WHEN status = 'error'   THEN checked_at END) AS last_error
FROM device_logs
GROUP BY device_id;
```
**Explanation:** Pivoting with MAX picks the most recent timestamp per status category. NULL appears when a device never had that status.

---

## Q9: Month-over-Month Spread — Monthly Revenue Columns

**Scenario:** Transform a long `monthly_revenue` table into a wide table with months as columns for easy period-over-period comparison.

**Schema:** `monthly_revenue (product_id INT, rev_month DATE, revenue DECIMAL)`

**Query:**
```sql
SELECT
  product_id,
  SUM(CASE WHEN rev_month = '2024-01-01' THEN revenue ELSE 0 END) AS jan_2024,
  SUM(CASE WHEN rev_month = '2024-02-01' THEN revenue ELSE 0 END) AS feb_2024,
  SUM(CASE WHEN rev_month = '2024-03-01' THEN revenue ELSE 0 END) AS mar_2024,
  SUM(CASE WHEN rev_month = '2024-04-01' THEN revenue ELSE 0 END) AS apr_2024,
  SUM(CASE WHEN rev_month = '2024-05-01' THEN revenue ELSE 0 END) AS may_2024,
  SUM(CASE WHEN rev_month = '2024-06-01' THEN revenue ELSE 0 END) AS jun_2024
FROM monthly_revenue
GROUP BY product_id;
```
**Explanation:** Fixed-pivot with known date values. Each month gets its own CASE expression to produce a spread table suitable for trend analysis.

**Alt1 (PostgreSQL CROSSTAB):**
```sql
SELECT * FROM crosstab(
  $$
  SELECT product_id, rev_month::TEXT, revenue
  FROM monthly_revenue
  ORDER BY 1, 2
  $$,
  $$ SELECT generate_series('2024-01-01'::date, '2024-06-01'::date, '1 month')::TEXT $$
) AS ct(product_id INT, jan_2024 DECIMAL, feb_2024 DECIMAL, mar_2024 DECIMAL,
        apr_2024 DECIMAL, may_2024 DECIMAL, jun_2024 DECIMAL);
```

---

## Q10: UNPIVOT — Wide to Long (SQL Server)

**Scenario:** You have a wide `quarterly_targets` table with columns Q1–Q4. Unpivot into rows showing each quarter's target per employee.

**Schema:** `quarterly_targets (emp_id INT, emp_name VARCHAR, Q1 DECIMAL, Q2 DECIMAL, Q3 DECIMAL, Q4 DECIMAL)`

**Query:**
```sql
SELECT emp_id, emp_name, quarter, target
FROM quarterly_targets
UNPIVOT (
  target FOR quarter IN (Q1, Q2, Q3, Q4)
) unpvt;
```
**Explanation:** UNPIVOT is the reverse of PIVOT — it transforms columns into rows. SQL Server provides a dedicated UNPIVOT operator.

**Alt1 (MySQL manual unpivot with UNION ALL):**
```sql
SELECT emp_id, emp_name, 'Q1' AS quarter, Q1 AS target FROM quarterly_targets
UNION ALL
SELECT emp_id, emp_name, 'Q2', Q2 FROM quarterly_targets
UNION ALL
SELECT emp_id, emp_name, 'Q3', Q3 FROM quarterly_targets
UNION ALL
SELECT emp_id, emp_name, 'Q4', Q4 FROM quarterly_targets;
```

---

## Q11: Oracle UNPIVOT — Wide Sensor Readings to Long

**Scenario:** Sensor data is stored with columns `temp_morning`, `temp_afternoon`, `temp_evening`. Unpivot to get one row per reading.

**Schema:** `sensor_readings (sensor_id INT, reading_date DATE, temp_morning NUMBER, temp_afternoon NUMBER, temp_evening NUMBER)`

**Query:**
```sql
SELECT sensor_id, reading_date, time_of_day, temperature
FROM sensor_readings
UNPIVOT (
  temperature FOR time_of_day IN (
    temp_morning   AS 'morning',
    temp_afternoon AS 'afternoon',
    temp_evening   AS 'evening'
  )
);
```
**Explanation:** Oracle UNPIVOT maps column names to string labels. The AS keyword in the IN list assigns readable aliases to each unpivoted column.

**Alt1 (PostgreSQL UNION ALL approach):**
```sql
SELECT sensor_id, reading_date, 'morning'   AS time_of_day, temp_morning   AS temperature FROM sensor_readings
UNION ALL
SELECT sensor_id, reading_date, 'afternoon', temp_afternoon FROM sensor_readings
UNION ALL
SELECT sensor_id, reading_date, 'evening',   temp_evening   FROM sensor_readings;
```

---

## Q12: Dynamic Pivot — Unknown Category Values

**Scenario:** Categories in `order_categories` change over time. Build a dynamic pivot that automatically creates columns for all distinct categories.

**Schema:** `order_categories (order_id INT, category VARCHAR, amount DECIMAL)`

**Query:**
```sql
-- MySQL dynamic pivot
SET @sql = NULL;

SELECT GROUP_CONCAT(
  DISTINCT CONCAT(
    'SUM(CASE WHEN category = ''', category, ''' THEN amount ELSE 0 END) AS `', category, '`'
  )
) INTO @sql
FROM order_categories;

SET @sql = CONCAT('SELECT order_id, ', @sql, ' FROM order_categories GROUP BY order_id');

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```
**Explanation:** Dynamic pivot builds the SQL string at runtime using `GROUP_CONCAT` (MySQL) to generate CASE expressions for every discovered category value. This is essential when category values are not known at write time.

**Alt1 (PostgreSQL dynamic with STRING_AGG and regexp):**
```sql
-- PostgreSQL dynamic pivot
DO $$
DECLARE
  cols TEXT;
  sql  TEXT;
BEGIN
  SELECT STRING_AGG(
    DISTINCT format(
      'SUM(CASE WHEN category = %L THEN amount ELSE 0 END) AS %I',
      category, category
    ),
    ', '
  ) INTO cols
  FROM order_categories;

  sql := format('SELECT order_id, %s FROM order_categories GROUP BY order_id', cols);
  RAISE NOTICE '%', sql;
  -- Execute: EXECUTE sql; (wrapped in a function or used dynamically)
END $$;
```

---

## Q13: Dynamic Pivot with GROUP_CONCAT — MySQL Sales Pivot

**Scenario:** Build a dynamic pivot for `regional_sales` where region names are unknown and discovered at runtime.

**Schema:** `regional_sales (product VARCHAR, region VARCHAR, sales DECIMAL)`

**Query:**
```sql
-- MySQL
SET @cols = NULL;
SET @query = NULL;

SELECT GROUP_CONCAT(DISTINCT region ORDER BY region SEPARATOR ', ') INTO @cols
FROM regional_sales;

SET @query = CONCAT(
  'SELECT product, ',
  (SELECT GROUP_CONCAT(
    CONCAT('SUM(CASE WHEN region = ''', region, ''' THEN sales ELSE 0 END) AS `', region, '`')
   )
   FROM (SELECT DISTINCT region FROM regional_sales) t),
  ' FROM regional_sales GROUP BY product'
);

PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```
**Explanation:** Uses GROUP_CONCAT to build both the column list and the CASE expressions dynamically. DISTINCT ensures each region appears once regardless of row count.

**Alt1 (SQL Server dynamic pivot using STRING_AGG):**
```sql
DECLARE @cols NVARCHAR(MAX), @sql NVARCHAR(MAX);

SELECT @cols = STRING_AGG(QUOTENAME(region), ', ') WITHIN GROUP (ORDER BY region)
FROM (SELECT DISTINCT region FROM regional_sales) t;

SET @sql = N'SELECT product, ' + @cols + N'
             FROM (SELECT product, region, sales FROM regional_sales) src
             PIVOT (SUM(sales) FOR region IN (' + @cols + N')) pvt';

EXEC sp_executesql @sql;
```

---

## Q14: Pivot with COALESCE — Handling NULLs in Output

**Scenario:** Pivot `inventory_counts` to show stock per warehouse per product. Replace NULLs with 0 for clean reporting.

**Schema:** `inventory_counts (product VARCHAR, warehouse VARCHAR, qty INT)`

**Query:**
```sql
SELECT
  product,
  COALESCE(SUM(CASE WHEN warehouse = 'WH-East'  THEN qty END), 0) AS wh_east,
  COALESCE(SUM(CASE WHEN warehouse = 'WH-West'  THEN qty END), 0) AS wh_west,
  COALESCE(SUM(CASE WHEN warehouse = 'WH-North' THEN qty END), 0) AS wh_north,
  COALESCE(SUM(CASE WHEN warehouse = 'WH-South' THEN qty END), 0) AS wh_south
FROM inventory_counts
GROUP BY product;
```
**Explanation:** COALESCE wraps the CASE-SUM to replace NULL (product not present in that warehouse) with 0. Alternatively, use `ELSE 0` inside the CASE.

---

## Q15: Conditional Aggregation — One-Hot Style Flags

**Scenario:** For each customer, produce a binary flag column for each product they have purchased (one-hot encoding style).

**Schema:** `purchases (customer_id INT, product VARCHAR)`

**Query:**
```sql
SELECT
  customer_id,
  MAX(CASE WHEN product = 'Widget'  THEN 1 ELSE 0 END) AS has_widget,
  MAX(CASE WHEN product = 'Gadget'  THEN 1 ELSE 0 END) AS has_gadget,
  MAX(CASE WHEN product = 'Doohickey' THEN 1 ELSE 0 END) AS has_doohickey
FROM purchases
GROUP BY customer_id;
```
**Explanation:** Using MAX with CASE produces 1/0 flags — a one-hot encoding pattern common in feature engineering for ML pipelines fed from SQL.

---

## Q16: Pivot with Multiple Dimensions — Nested Pivot

**Scenario:** Pivot `sales_data` by product (rows) and region (columns), nested under a year dimension.

**Schema:** `sales_data (year INT, product VARCHAR, region VARCHAR, revenue DECIMAL)`

**Query:**
```sql
SELECT
  year,
  product,
  SUM(CASE WHEN region = 'East'  THEN revenue ELSE 0 END) AS east,
  SUM(CASE WHEN region = 'West'  THEN revenue ELSE 0 END) AS west,
  SUM(CASE WHEN region = 'North' THEN revenue ELSE 0 END) AS north,
  SUM(CASE WHEN region = 'South' THEN revenue ELSE 0 END) AS south
FROM sales_data
GROUP BY year, product
ORDER BY year, product;
```
**Explanation:** Multi-dimension pivot includes the year in GROUP BY to produce separate rows per year-product combination with regional columns. Each group is independently pivoted.

---

## Q17: PIVOT with Subquery — SQL Server Aggregated Pivot

**Scenario:** Pivot the result of a subquery that computes average order value per payment method per day-of-week.

**Schema:** `orders (order_id INT, payment_method VARCHAR, order_date DATE, amount DECIMAL)`

**Query:**
```sql
SELECT day_of_week, [Credit Card], [Cash], [Bank Transfer]
FROM (
  SELECT
    DATENAME(WEEKDAY, order_date) AS day_of_week,
    payment_method,
    amount
  FROM orders
) src
PIVOT (
  AVG(amount) FOR payment_method IN ([Credit Card], [Cash], [Bank Transfer])
) pvt;
```
**Explanation:** The PIVOT operator works on any derived table or subquery. The source must contain the row identifier, the pivot column, and the value column.

---

## Q18: PostgreSQL CROSSTAB — Pivot Without Fixed Categories

**Scenario:** Use CROSSTAB to show each student's grade per subject. The category SQL explicitly defines the column order.

**Schema:** `grades (student_id INT, subject VARCHAR, grade CHAR(2))`

**Query:**
```sql
SELECT * FROM crosstab(
  $$SELECT student_id, subject, grade FROM grades ORDER BY 1, 2$$,
  $$VALUES ('Math'), ('Science'), ('English'), ('History')$$
) AS ct(student_id INT, math CHAR(2), science CHAR(2), english CHAR(2), history CHAR(2));
```
**Explanation:** CROSSTAB's second argument provides the fixed set of column values. This guarantees consistent columns even when some students lack a grade in a subject (NULL fills gaps).

**Alt1 (Conditional aggregation — portable):**
```sql
SELECT
  student_id,
  MAX(CASE WHEN subject = 'Math'    THEN grade END) AS math,
  MAX(CASE WHEN subject = 'Science' THEN grade END) AS science,
  MAX(CASE WHEN subject = 'English' THEN grade END) AS english,
  MAX(CASE WHEN subject = 'History' THEN grade END) AS history
FROM grades
GROUP BY student_id;
```

---

## Q19: LAG as Virtual Pivot — Previous Value in Same Row

**Scenario:** Show each order's revenue alongside the previous order's revenue for the same customer, using LAG to simulate a pivot of current vs. previous.

**Schema:** `orders (order_id INT, customer_id INT, order_date DATE, revenue DECIMAL)`

**Query:**
```sql
SELECT
  customer_id,
  order_id,
  order_date,
  revenue AS current_revenue,
  LAG(revenue) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_revenue,
  revenue - LAG(revenue) OVER (PARTITION BY customer_id ORDER BY order_date) AS delta
FROM orders;
```
**Explanation:** LAG places the previous row's value into the current row — a different pattern from pivot. Pivot transposes across categories; LAG accesses an adjacent row in the same direction.

---

## Q20: UNPIVOT Laptops — Wide Laptop Specs to Long

**Scenario:** A `laptops` table stores specs as columns (cpu, ram, storage, screen). Unpivot to get one row per specification per laptop.

**Schema:** `laptops (laptop_id INT, model VARCHAR, cpu VARCHAR, ram VARCHAR, storage VARCHAR, screen VARCHAR)`

**Query:**
```sql
SELECT laptop_id, model, spec_name, spec_value
FROM laptops
UNPIVOT (
  spec_value FOR spec_name IN (cpu, ram, storage, screen)
) unpvt;
```
**Explanation:** SQL Server UNPIVOT converts column headers into row values. Each laptop now has four rows — one per spec — enabling easier filtering and aggregation by spec type.

**Alt1 (MySQL UNION ALL unpivot):**
```sql
SELECT laptop_id, model, 'cpu'     AS spec_name, cpu     AS spec_value FROM laptops
UNION ALL
SELECT laptop_id, model, 'ram'     AS spec_name, ram     AS spec_value FROM laptops
UNION ALL
SELECT laptop_id, model, 'storage' AS spec_name, storage AS spec_value FROM laptops
UNION ALL
SELECT laptop_id, model, 'screen'  AS spec_name, screen  AS spec_value FROM laptops;
```

---

## Q21: Dynamic Pivot — Categories Discovered at Runtime (SQL Server)

**Scenario:** The `survey_responses` table has dynamically added question columns. Pivot responses so each question becomes a column.

**Schema:** `survey_responses (respondent_id INT, question VARCHAR, answer VARCHAR)`

**Query:**
```sql
DECLARE @cols NVARCHAR(MAX), @sql NVARCHAR(MAX);

SELECT @cols = STRING_AGG(QUOTENAME(question), ', ') WITHIN GROUP (ORDER BY question)
FROM (SELECT DISTINCT question FROM survey_responses) t;

SET @sql = N'SELECT respondent_id, ' + @cols + N'
             FROM survey_responses
             PIVOT (MAX(answer) FOR question IN (' + @cols + N')) pvt';

EXEC sp_executesql @sql;
```
**Explanation:** Dynamic SQL builds the PIVOT operator's IN list at runtime. `QUOTENAME` prevents SQL injection from question text. `STRING_AGG` (SQL Server 2017+) replaces FOR XML PATH.

**Alt1 (MySQL dynamic with GROUP_CONCAT):**
```sql
SET @sql = NULL;
SELECT GROUP_CONCAT(
  DISTINCT CONCAT('MAX(CASE WHEN question = ''', question, ''' THEN answer END) AS `', question, '`')
) INTO @sql
FROM survey_responses;

SET @sql = CONCAT('SELECT respondent_id, ', @sql, ' FROM survey_responses GROUP BY respondent_id');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```

---

## Q22: Pivot with SUM and NULL Fill — Regional Quarterly Pivot

**Scenario:** Pivot `quarterly_revenue` to show revenue per region per quarter. Fill missing combinations with 0.

**Schema:** `quarterly_revenue (region VARCHAR, quarter VARCHAR, revenue DECIMAL)`

**Query:**
```sql
SELECT
  region,
  COALESCE(SUM(CASE WHEN quarter = 'Q1' THEN revenue END), 0) AS q1,
  COALESCE(SUM(CASE WHEN quarter = 'Q2' THEN revenue END), 0) AS q2,
  COALESCE(SUM(CASE WHEN quarter = 'Q3' THEN revenue END), 0) AS q3,
  COALESCE(SUM(CASE WHEN quarter = 'Q4' THEN revenue END), 0) AS q4
FROM quarterly_revenue
GROUP BY region;
```
**Explanation:** COALESCE replaces NULL (no data for a region-quarter combination) with 0, producing a clean numerical matrix.

---

## Q23: Pivot Employee Salary Bands — Frequency Matrix

**Scenario:** Count employees in each salary band per department. Departments as rows, bands as columns.

**Schema:** `employees (emp_id INT, dept VARCHAR, salary DECIMAL)`

**Query:**
```sql
SELECT
  dept,
  COUNT(*) FILTER (WHERE salary < 50000)  AS band_low,
  COUNT(*) FILTER (WHERE salary BETWEEN 50000 AND 99999)  AS band_mid,
  COUNT(*) FILTER (WHERE salary BETWEEN 100000 AND 149999) AS band_high,
  COUNT(*) FILTER (WHERE salary >= 150000) AS band_exec
FROM employees
GROUP BY dept;
```
**Explanation:** PostgreSQL FILTER clause provides a clean alternative to SUM(CASE WHEN ... THEN 1 ELSE 0 END) for frequency pivots.

**Alt1 (MySQL conditional aggregation):**
```sql
SELECT
  dept,
  SUM(CASE WHEN salary < 50000 THEN 1 ELSE 0 END)       AS band_low,
  SUM(CASE WHEN salary BETWEEN 50000 AND 99999 THEN 1 ELSE 0 END) AS band_mid,
  SUM(CASE WHEN salary BETWEEN 100000 AND 149999 THEN 1 ELSE 0 END) AS band_high,
  SUM(CASE WHEN salary >= 150000 THEN 1 ELSE 0 END)     AS band_exec
FROM employees
GROUP BY dept;
```

---

## Q24: Confusion Matrix Pivot — Predictions vs Actuals

**Scenario:** Build a confusion matrix from `model_predictions` where each row is a prediction. Rows = actual labels, columns = predicted labels, values = counts.

**Schema:** `model_predictions (prediction_id INT, actual_label VARCHAR, predicted_label VARCHAR)`

**Query:**
```sql
SELECT
  actual_label,
  SUM(CASE WHEN predicted_label = 'positive' THEN 1 ELSE 0 END) AS pred_positive,
  SUM(CASE WHEN predicted_label = 'negative' THEN 1 ELSE 0 END) AS pred_negative
FROM model_predictions
GROUP BY actual_label;
```
**Explanation:** A confusion matrix is a two-dimensional pivot: actual values as rows, predicted values as columns, with COUNT as the aggregate. This is a classic interview scenario for ML-adjacent roles.

**Alt1 (PostgreSQL CROSSTAB):**
```sql
SELECT * FROM crosstab(
  $$SELECT actual_label, predicted_label, COUNT(*)::INT
    FROM model_predictions GROUP BY 1, 2 ORDER BY 1, 2$$,
  $$VALUES ('positive'), ('negative')$$
) AS cm(actual_label VARCHAR, pred_positive INT, pred_negative INT);
```

---

## Q25: Pivot — Sparse to Dense Matrix with COALESCE

**Scenario:** Pivot `user_permissions` to produce a dense permission matrix where rows are users and columns are permissions, with 1/0 flags.

**Schema:** `user_permissions (user_id INT, permission VARCHAR)`

**Query:**
```sql
SELECT
  user_id,
  COALESCE(MAX(CASE WHEN permission = 'read'    THEN 1 END), 0) AS can_read,
  COALESCE(MAX(CASE WHEN permission = 'write'   THEN 1 END), 0) AS can_write,
  COALESCE(MAX(CASE WHEN permission = 'delete'  THEN 1 END), 0) AS can_delete,
  COALESCE(MAX(CASE WHEN permission = 'admin'   THEN 1 END), 0) AS can_admin
FROM user_permissions
GROUP BY user_id;
```
**Explanation:** COALESCE with MAX(CASE WHEN ... THEN 1 END) produces a clean binary matrix. Without COALESCE, users missing a permission would show NULL instead of 0.

---

## Q26: PIVOT with Aliases — SQL Server Sales by Store

**Scenario:** Pivot `store_sales` so each store becomes a column showing total sales for January 2024.

**Schema:** `store_sales (store_id INT, store_name VARCHAR, sale_month VARCHAR, total_sales DECIMAL)`

**Query:**
```sql
SELECT [North], [South], [East], [West]
FROM (
  SELECT store_name, total_sales FROM store_sales WHERE sale_month = '2024-01'
) src
PIVOT (
  SUM(total_sales) FOR store_name IN ([North], [South], [East], [West])
) pvt;
```
**Explanation:** The PIVOT operator's FOR clause specifies the column whose values become new column headers. The IN list maps original values to output column names.

---

## Q27: Count Matrix Pivot — Votes per Candidate per State

**Scenario:** Aggregate votes into a matrix: states as rows, candidates as columns, vote counts as values.

**Schema:** `votes (vote_id INT, state VARCHAR, candidate VARCHAR)`

**Query:**
```sql
SELECT
  state,
  SUM(CASE WHEN candidate = 'Alice'   THEN 1 ELSE 0 END) AS alice,
  SUM(CASE WHEN candidate = 'Bob'     THEN 1 ELSE 0 END) AS bob,
  SUM(CASE WHEN candidate = 'Charlie' THEN 1 ELSE 0 END) AS charlie
FROM votes
GROUP BY state
ORDER BY state;
```
**Explanation:** Converting vote rows into a candidate-by-state count matrix is a standard pivoting exercise. The aggregate COUNT inside CASE produces tallies per cell.

---

## Q28: Transpose Two-Column Key-Value to Columns

**Scenario:** A `settings` table stores configuration as key-value pairs. Pivot so each key becomes a column with its value.

**Schema:** `settings (config_key VARCHAR, config_value VARCHAR)`

**Query:**
```sql
SELECT
  MAX(CASE WHEN config_key = 'theme'       THEN config_value END) AS theme,
  MAX(CASE WHEN config_key = 'language'    THEN config_value END) AS language,
  MAX(CASE WHEN config_key = 'timezone'    THEN config_value END) AS timezone,
  MAX(CASE WHEN config_key = 'notifications' THEN config_value END) AS notifications
FROM settings;
```
**Explanation:** Key-value to columnar transposition uses MAX (or MIN) with CASE. Since each key has one value, MAX collapses the single non-NULL result. No GROUP BY needed when pivoting a single row set.

---

## Q29: Oracle PIVOT with Multiple Aggregates

**Scenario:** Pivot `inventory_log` to show both SUM of quantities and MAX of last_updated per warehouse per product.

**Schema:** `inventory_log (product VARCHAR, warehouse VARCHAR, qty INT, last_updated TIMESTAMP)`

**Query:**
```sql
SELECT product, warehouse_qty, warehouse_max_date
FROM (
  SELECT product, warehouse, qty, last_updated FROM inventory_log
)
PIVOT (
  SUM(qty) AS warehouse_qty,
  MAX(last_updated) AS warehouse_max_date
  FOR warehouse IN ('A' AS wh_a, 'B' AS wh_b, 'C' AS wh_c)
);
```
**Explanation:** Oracle PIVOT supports multiple comma-separated aggregates, each producing suffixed columns (e.g., `wh_a_warehouse_qty`).

**Alt1 (Conditional aggregation — portable):**
```sql
SELECT
  product,
  SUM(CASE WHEN warehouse = 'A' THEN qty ELSE 0 END)       AS wh_a_qty,
  MAX(CASE WHEN warehouse = 'A' THEN last_updated END)      AS wh_a_max_date,
  SUM(CASE WHEN warehouse = 'B' THEN qty ELSE 0 END)       AS wh_b_qty,
  MAX(CASE WHEN warehouse = 'B' THEN last_updated END)      AS wh_b_max_date,
  SUM(CASE WHEN warehouse = 'C' THEN qty ELSE 0 END)       AS wh_c_qty,
  MAX(CASE WHEN warehouse = 'C' THEN last_updated END)      AS wh_c_max_date
FROM inventory_log
GROUP BY product;
```

---

## Q30: UNPIVOT Lateral Join — Wide Survey to Long (PostgreSQL)

**Scenario:** A survey table stores Q1–Q5 as columns. Unpivot using a lateral join with VALUES to produce one row per question per respondent.

**Schema:** `survey (respondent_id INT, q1 INT, q2 INT, q3 INT, q4 INT, q5 INT)`

**Query:**
```sql
SELECT s.respondent_id, v.question, v.score
FROM survey s
CROSS JOIN LATERAL (VALUES
  ('Q1', s.q1),
  ('Q2', s.q2),
  ('Q3', s.q3),
  ('Q4', s.q4),
  ('Q5', s.q5)
) AS v(question, score);
```
**Explanation:** PostgreSQL's LATERAL with VALUES is the idiomatic unpivot pattern — no UNION ALL needed. The LATERAL join references the outer row's columns directly.

**Alt1 (UNION ALL — MySQL/SQL Server):**
```sql
SELECT respondent_id, 'Q1' AS question, q1 AS score FROM survey
UNION ALL SELECT respondent_id, 'Q2', q2 FROM survey
UNION ALL SELECT respondent_id, 'Q3', q3 FROM survey
UNION ALL SELECT respondent_id, 'Q4', q4 FROM survey
UNION ALL SELECT respondent_id, 'Q5', q5 FROM survey;
```

---

## Q31: Dynamic Pivot with STRING_AGG — SQL Server Unknown Categories

**Scenario:** The `event_types` table has unpredictable category names. Dynamically pivot event counts per category.

**Schema:** `events (event_date DATE, event_type VARCHAR, event_count INT)`

**Query:**
```sql
DECLARE @cols NVARCHAR(MAX), @sql NVARCHAR(MAX);

SELECT @cols = STRING_AGG(QUOTENAME(event_type), ', ') WITHIN GROUP (ORDER BY event_type)
FROM (SELECT DISTINCT event_type FROM events) AS t;

SET @sql = N'SELECT event_date, ' + @cols + N'
             FROM (SELECT event_date, event_type, event_count FROM events) src
             PIVOT (SUM(event_count) FOR event_type IN (' + @cols + N')) pvt
             ORDER BY event_date';

EXEC sp_executesql @sql;
```
**Explanation:** Dynamic PIVOT via `STRING_AGG` + `QUOTENAME` ensures safe, ordered column generation. The subquery is wrapped to avoid PIVOT restrictions on direct table references.

---

## Q32: Pivot — User Pair Matrix (Self-Join Aggregation)

**Scenario:** From a `messages` table, build a user-pair interaction matrix where rows and columns are user IDs and values are message counts.

**Schema:** `messages (sender_id INT, receiver_id INT)`

**Query:**
```sql
WITH users AS (
  SELECT DISTINCT user_id FROM (
    SELECT sender_id AS user_id FROM messages
    UNION
    SELECT receiver_id AS user_id FROM messages
  ) t
)
SELECT
  u1.user_id AS row_user,
  u2.user_id AS col_user,
  COUNT(m.sender_id) AS msg_count
FROM users u1
CROSS JOIN users u2
LEFT JOIN messages m ON m.sender_id = u1.user_id AND m.receiver_id = u2.user_id
GROUP BY u1.user_id, u2.user_id
ORDER BY u1.user_id, u2.user_id;
```
**Explanation:** A cross join of users with itself creates the full matrix skeleton. LEFT JOIN ensures all pairs appear, even those with zero messages.

---

## Q33: Pivot Rows to Multiple Columns per Group — Top 3 Scores

**Scenario:** For each student, pivot their top 3 test scores into columns score_1, score_2, score_3.

**Schema:** `test_scores (student_id INT, student_name VARCHAR, test_name VARCHAR, score DECIMAL)`

**Query:**
```sql
WITH ranked AS (
  SELECT
    student_id, student_name, score,
    ROW_NUMBER() OVER (PARTITION BY student_id ORDER BY score DESC) AS rn
  FROM test_scores
)
SELECT
  student_id,
  student_name,
  MAX(CASE WHEN rn = 1 THEN score END) AS score_1,
  MAX(CASE WHEN rn = 2 THEN score END) AS score_2,
  MAX(CASE WHEN rn = 3 THEN score END) AS score_3
FROM ranked
WHERE rn <= 3
GROUP BY student_id, student_name;
```
**Explanation:** ROW_NUMBER generates a positional index per group. Conditional aggregation then pivots these positions into named columns, producing a fixed-width output per student.

---

## Q34: Pivot with Percentage — Market Share by Product

**Scenario:** Calculate each product's share of total revenue per quarter, pivoted into columns.

**Schema:** `quarterly_sales (quarter VARCHAR, product VARCHAR, revenue DECIMAL)`

**Query:**
```sql
WITH totals AS (
  SELECT quarter, SUM(revenue) AS total FROM quarterly_sales GROUP BY quarter
)
SELECT
  qs.quarter,
  ROUND(SUM(CASE WHEN qs.product = 'A' THEN qs.revenue ELSE 0 END) / t.total * 100, 2) AS product_a_pct,
  ROUND(SUM(CASE WHEN qs.product = 'B' THEN qs.revenue ELSE 0 END) / t.total * 100, 2) AS product_b_pct,
  ROUND(SUM(CASE WHEN qs.product = 'C' THEN qs.revenue ELSE 0 END) / t.total * 100, 2) AS product_c_pct
FROM quarterly_sales qs
JOIN totals t ON qs.quarter = t.quarter
GROUP BY qs.quarter, t.total;
```
**Explanation:** Combining a totals CTE with pivoted CASE expressions produces percentage-of-total columns — a common follow-up twist on basic pivoting questions.

---

## Q35: Oracle UNPIVOT — Wide Metrics to Long

**Scenario:** A `server_metrics` table stores CPU, memory, and disk as columns. Unpivot for normalized monitoring.

**Schema:** `server_metrics (server_id INT, check_time TIMESTAMP, cpu_pct NUMBER, mem_pct NUMBER, disk_pct NUMBER)`

**Query:**
```sql
SELECT server_id, check_time, metric_name, metric_value
FROM server_metrics
UNPIVOT (
  metric_value FOR metric_name IN (cpu_pct AS 'CPU', mem_pct AS 'Memory', disk_pct AS 'Disk')
);
```
**Explanation:** Oracle UNPIVOT converts wide-format metrics into long format. The AS keyword assigns readable aliases to each unpivoted column name.

---

## Q36: PIVOT Multiple Aggregates — Order Counts and Revenue by Channel

**Scenario:** For each product category, pivot to show order count and total revenue per sales channel.

**Schema:** `orders (category VARCHAR, channel VARCHAR, amount DECIMAL)`

**Query:**
```sql
SELECT
  category,
  SUM(CASE WHEN channel = 'web'     THEN 1 ELSE 0 END) AS web_orders,
  SUM(CASE WHEN channel = 'web'     THEN amount ELSE 0 END) AS web_revenue,
  SUM(CASE WHEN channel = 'mobile'  THEN 1 ELSE 0 END) AS mobile_orders,
  SUM(CASE WHEN channel = 'mobile'  THEN amount ELSE 0 END) AS mobile_revenue,
  SUM(CASE WHEN channel = 'store'   THEN 1 ELSE 0 END) AS store_orders,
  SUM(CASE WHEN channel = 'store'   THEN amount ELSE 0 END) AS store_revenue
FROM orders
GROUP BY category;
```
**Explanation:** Multiple aggregates per pivot cell require separate CASE expressions for each metric-channel combination. This pattern is extremely common in business reporting.

---

## Q37: Dynamic Pivot with GROUP_CONCAT and regexp — MySQL Robust Column Building

**Scenario:** Dynamically pivot `tag_counts` where tag names may contain spaces or special characters, requiring careful quoting.

**Schema:** `tag_counts (post_id INT, tag VARCHAR, count INT)`

**Query:**
```sql
SET @sql = NULL;

SELECT GROUP_CONCAT(
  DISTINCT CONCAT(
    'SUM(CASE WHEN tag = ''',
    REPLACE(tag, '''', ''''''),
    ''' THEN count ELSE 0 END) AS `',
    REPLACE(tag, '`', '``'),
    '`'
  )
  ORDER BY tag
) INTO @sql
FROM tag_counts;

SET @sql = CONCAT('SELECT post_id, ', @sql, ' FROM tag_counts GROUP BY post_id');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```
**Explanation:** Escaping single quotes and backticks in dynamic SQL prevents injection and syntax errors. `REPLACE(tag, '''', ''''')` doubles single quotes for safe embedding.

---

## Q38: Pivot Rows into Columns with LAG — Running Comparison

**Scenario:** For each product, show current month's sales alongside previous month's sales using LAG, then pivot the comparison into a single row.

**Schema:** `monthly_sales (product_id INT, sale_month DATE, revenue DECIMAL)`

**Query:**
```sql
WITH lagged AS (
  SELECT
    product_id,
    sale_month,
    revenue AS current_rev,
    LAG(revenue) OVER (PARTITION BY product_id ORDER BY sale_month) AS prev_rev
  FROM monthly_sales
)
SELECT
  product_id,
  sale_month,
  current_rev,
  prev_rev,
  current_rev - prev_rev AS change,
  ROUND((current_rev - prev_rev) / NULLIF(prev_rev, 0) * 100, 2) AS pct_change
FROM lagged;
```
**Explanation:** LAG brings the previous row's value into the current row — semantically different from pivot. Pivot transposes categories into columns; LAG accesses sequential rows. Both can achieve "side-by-side" comparisons but through different mechanisms.

---

## Q39: Pivot — Heat Map Data Preparation

**Scenario:** Prepare data for a heat map by pivoting `hourly_visits` so rows are hours (0–23) and columns are days of the week.

**Schema:** `hourly_visits (visit_time TIMESTAMP, visitor_count INT)`

**Query:**
```sql
SELECT
  EXTRACT(HOUR FROM visit_time)::INT AS hour_of_day,
  SUM(CASE WHEN EXTRACT(DOW FROM visit_time) = 0 THEN visitor_count ELSE 0 END) AS sun,
  SUM(CASE WHEN EXTRACT(DOW FROM visit_time) = 1 THEN visitor_count ELSE 0 END) AS mon,
  SUM(CASE WHEN EXTRACT(DOW FROM visit_time) = 2 THEN visitor_count ELSE 0 END) AS tue,
  SUM(CASE WHEN EXTRACT(DOW FROM visit_time) = 3 THEN visitor_count ELSE 0 END) AS wed,
  SUM(CASE WHEN EXTRACT(DOW FROM visit_time) = 4 THEN visitor_count ELSE 0 END) AS thu,
  SUM(CASE WHEN EXTRACT(DOW FROM visit_time) = 5 THEN visitor_count ELSE 0 END) AS fri,
  SUM(CASE WHEN EXTRACT(DOW FROM visit_time) = 6 THEN visitor_count ELSE 0 END) AS sat
FROM hourly_visits
GROUP BY EXTRACT(HOUR FROM visit_time)
ORDER BY hour_of_day;
```
**Explanation:** Heat map data requires a two-dimensional pivot: one dimension for rows (hours), another for columns (days). The aggregate SUM builds cell values for visualization.

---

## Q40: UNPIVOT with LATERAL — PostgreSQL Wide Inventory to Long

**Scenario:** Unpivot an `inventory` table with columns for each warehouse's stock into normalized rows.

**Schema:** `inventory (product_id INT, wh_a_qty INT, wh_b_qty INT, wh_c_qty INT, wh_d_qty INT)`

**Query:**
```sql
SELECT i.product_id, v.warehouse, v.quantity
FROM inventory i
CROSS JOIN LATERAL (VALUES
  ('WH-A', i.wh_a_qty),
  ('WH-B', i.wh_b_qty),
  ('WH-C', i.wh_c_qty),
  ('WH-D', i.wh_d_qty)
) AS v(warehouse, quantity)
WHERE v.quantity > 0;
```
**Explanation:** LATERAL VALUES is the cleanest PostgreSQL unpivot. The optional WHERE clause filters out zero-stock combinations, producing a sparse long-form result.

---

## Q41: Conditional Aggregation — Pivot with HAVING Filter

**Scenario:** Pivot `support_tickets` to show ticket counts by priority per team. Only show teams with more than 10 total tickets.

**Schema:** `support_tickets (team VARCHAR, priority VARCHAR, ticket_id INT)`

**Query:**
```sql
SELECT
  team,
  SUM(CASE WHEN priority = 'critical' THEN 1 ELSE 0 END) AS critical,
  SUM(CASE WHEN priority = 'high'     THEN 1 ELSE 0 END) AS high,
  SUM(CASE WHEN priority = 'medium'   THEN 1 ELSE 0 END) AS medium,
  SUM(CASE WHEN priority = 'low'      THEN 1 ELSE 0 END) AS low
FROM support_tickets
GROUP BY team
HAVING COUNT(*) > 10;
```
**Explanation:** The HAVING clause filters after aggregation, ensuring only teams with sufficient ticket volume appear in the pivoted output.

---

## Q42: PIVOT with SUM and AVG — Financial Summary Pivot

**Scenario:** For each account, show total credits and average debit per transaction type, pivoted by type.

**Schema:** `transactions (account_id INT, txn_type VARCHAR, amount DECIMAL)`

**Query:**
```sql
SELECT
  account_id,
  SUM(CASE WHEN txn_type = 'credit' THEN amount ELSE 0 END)  AS total_credits,
  AVG(CASE WHEN txn_type = 'debit'  THEN amount END)          AS avg_debits
FROM transactions
GROUP BY account_id;
```
**Explanation:** Mixing different aggregate functions (SUM for credits, AVG for debits) in a single pivot is trivial with conditional aggregation — each aggregate lives in its own CASE expression.

---

## Q43: Pivot Long Table to Wide — Monthly Expenses

**Scenario:** Pivot `expenses` so each expense category becomes a column with total spent per month.

**Schema:** `expenses (expense_date DATE, category VARCHAR, amount DECIMAL)`

**Query:**
```sql
SELECT
  DATE_TRUNC('month', expense_date)::DATE AS month,
  SUM(CASE WHEN category = 'rent'       THEN amount ELSE 0 END) AS rent,
  SUM(CASE WHEN category = 'utilities'  THEN amount ELSE 0 END) AS utilities,
  SUM(CASE WHEN category = 'salaries'   THEN amount ELSE 0 END) AS salaries,
  SUM(CASE WHEN category = 'marketing'  THEN amount ELSE 0 END) AS marketing
FROM expenses
GROUP BY DATE_TRUNC('month', expense_date)
ORDER BY month;
```
**Explanation:** Monthly expense pivots are common in financial reporting. The DATE_TRUNC groups by month, and CASE expressions spread categories into columns.

---

## Q44: Dynamic Pivot with CONCAT and GROUP_CONCAT — MySQL Unknown Columns

**Scenario:** Build a dynamic pivot for `feature_usage` where feature names are user-generated and unknown at query time.

**Schema:** `feature_usage (user_id INT, feature_name VARCHAR, usage_count INT)`

**Query:**
```sql
SET @sql = NULL;

SELECT GROUP_CONCAT(
  DISTINCT CONCAT(
    'SUM(CASE WHEN feature_name = ''', feature_name,
    ''' THEN usage_count ELSE 0 END) AS `', feature_name, '`'
  )
  ORDER BY feature_name SEPARATOR ', '
) INTO @sql
FROM feature_usage;

SET @sql = CONCAT('SELECT user_id, ', @sql, ' FROM feature_usage GROUP BY user_id');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```
**Explanation:** Dynamic SQL with GROUP_CONCAT generates a CASE expression per discovered feature. This pattern scales to any number of unknown categories.

---

## Q45: PIVOT — Daily Login Counts per Platform

**Scenario:** Pivot `login_events` to show daily login counts per platform (web, mobile, desktop) as separate columns.

**Schema:** `login_events (user_id INT, login_date DATE, platform VARCHAR)`

**Query:**
```sql
SELECT
  login_date,
  COUNT(CASE WHEN platform = 'web'     THEN 1 END) AS web_logins,
  COUNT(CASE WHEN platform = 'mobile'  THEN 1 END) AS mobile_logins,
  COUNT(CASE WHEN platform = 'desktop' THEN 1 END) AS desktop_logins
FROM login_events
GROUP BY login_date
ORDER BY login_date;
```
**Explanation:** COUNT with CASE counts only non-NULL values matching the condition. This produces a platform-by-date login matrix.

---

## Q46: UNPIVOT — Wide Product Attributes to Long (SQL Server)

**Scenario:** A `product_catalog` table stores attributes as columns (color, size, weight, material). Unpivot to normalize.

**Schema:** `product_catalog (product_id INT, product_name VARCHAR, color VARCHAR, size VARCHAR, weight VARCHAR, material VARCHAR)`

**Query:**
```sql
SELECT product_id, product_name, attribute, value
FROM product_catalog
UNPIVOT (
  value FOR attribute IN (color, size, weight, material)
) unpvt;
```
**Explanation:** UNPIVOT transforms a wide table with fixed columns into a long table where attribute names become row values, enabling flexible filtering and joins.

**Alt1 (PostgreSQL LATERAL VALUES):**
```sql
SELECT p.product_id, p.product_name, v.attribute, v.value
FROM product_catalog p
CROSS JOIN LATERAL (VALUES
  ('color', p.color),
  ('size', p.size),
  ('weight', p.weight),
  ('material', p.material)
) AS v(attribute, value);
```

---

## Q47: Pivot — User Activity Heatmap Matrix

**Scenario:** Pivot `page_views` into a matrix of user activity by hour-of-day and day-of-week for heatmap visualization.

**Schema:** `page_views (view_id INT, user_id INT, viewed_at TIMESTAMP)`

**Query:**
```sql
SELECT
  EXTRACT(DOW FROM viewed_at)::INT AS day_of_week,
  EXTRACT(HOUR FROM viewed_at)::INT AS hour_of_day,
  COUNT(*) AS view_count
FROM page_views
GROUP BY EXTRACT(DOW FROM viewed_at), EXTRACT(HOUR FROM viewed_at)
ORDER BY day_of_week, hour_of_day;
```
**Explanation:** While not a traditional columnar pivot, this two-dimensional GROUP BY produces heatmap-ready data. A full columnar pivot would require dynamic SQL since hours span 0–23.

---

## Q48: Pivot with COALESCE and SUM — Regional Sales Dashboard

**Scenario:** Build a regional sales dashboard with products as rows, regions as columns, and revenue totals. Fill NULLs with 0.

**Schema:** `regional_sales (product VARCHAR, region VARCHAR, revenue DECIMAL)`

**Query:**
```sql
SELECT
  product,
  COALESCE(SUM(CASE WHEN region = 'APAC'     THEN revenue END), 0) AS apac,
  COALESCE(SUM(CASE WHEN region = 'EMEA'     THEN revenue END), 0) AS emea,
  COALESCE(SUM(CASE WHEN region = 'Americas' THEN revenue END), 0) AS americas,
  COALESCE(SUM(CASE WHEN region = 'LATAM'    THEN revenue END), 0) AS latam
FROM regional_sales
GROUP BY product
ORDER BY product;
```
**Explanation:** COALESCE with CASE-SUM produces a complete matrix with no NULL gaps, suitable for downstream charting and reporting tools.

---

## Q49: Conditional Aggregation — Pivoting Aggregates for Reporting

**Scenario:** For each department, show total salary, headcount, and average salary per employment type (full-time, part-time, contractor).

**Schema:** `employees (dept VARCHAR, emp_type VARCHAR, salary DECIMAL)`

**Query:**
```sql
SELECT
  dept,
  SUM(CASE WHEN emp_type = 'full-time'  THEN salary ELSE 0 END) AS ft_total_salary,
  COUNT(CASE WHEN emp_type = 'full-time' THEN 1 END)             AS ft_headcount,
  AVG(CASE WHEN emp_type = 'full-time'  THEN salary END)         AS ft_avg_salary,
  SUM(CASE WHEN emp_type = 'part-time'  THEN salary ELSE 0 END) AS pt_total_salary,
  COUNT(CASE WHEN emp_type = 'part-time' THEN 1 END)             AS pt_headcount,
  AVG(CASE WHEN emp_type = 'part-time'  THEN salary END)         AS pt_avg_salary
FROM employees
GROUP BY dept;
```
**Explanation:** Multi-aggregate pivoting across categories is essential for management reporting. Each metric-category combination needs its own CASE expression.

---

## Q50: Dynamic Pivot — SQL Server STRING_AGG with QUOTENAME

**Scenario:** Dynamically pivot `product_ratings` where product names change over time.

**Schema:** `product_ratings (reviewer_id INT, product_name VARCHAR, rating INT)`

**Query:**
```sql
DECLARE @cols NVARCHAR(MAX), @sql NVARCHAR(MAX);

SELECT @cols = STRING_AGG(QUOTENAME(product_name), ', ') WITHIN GROUP (ORDER BY product_name)
FROM (SELECT DISTINCT product_name FROM product_ratings) AS t;

SET @sql = N'SELECT reviewer_id, ' + @cols + N'
             FROM product_ratings
             PIVOT (AVG(rating) FOR product_name IN (' + @cols + N')) pvt';

EXEC sp_executesql @sql;
```
**Explanation:** `QUOTENAME` wraps product names in square brackets, protecting against names with spaces or reserved words. `STRING_AGG` with `WITHIN GROUP (ORDER BY ...)` ensures deterministic column order.

---

## Q51: Pivot with RANK and Conditional Aggregation — Top Products per Region

**Scenario:** For each region, pivot to show the top 3 products by revenue as separate columns.

**Schema:** `product_revenue (product VARCHAR, region VARCHAR, revenue DECIMAL)`

**Query:**
```sql
WITH ranked AS (
  SELECT
    product, region, revenue,
    RANK() OVER (PARTITION BY region ORDER BY revenue DESC) AS rnk
  FROM product_revenue
)
SELECT
  region,
  MAX(CASE WHEN rnk = 1 THEN product END) AS top_1_product,
  MAX(CASE WHEN rnk = 1 THEN revenue END) AS top_1_revenue,
  MAX(CASE WHEN rnk = 2 THEN product END) AS top_2_product,
  MAX(CASE WHEN rnk = 2 THEN revenue END) AS top_2_revenue,
  MAX(CASE WHEN rnk = 3 THEN product END) AS top_3_product,
  MAX(CASE WHEN rnk = 3 THEN revenue END) AS top_3_revenue
FROM ranked
WHERE rnk <= 3
GROUP BY region;
```
**Explanation:** Combining window functions (RANK) with conditional aggregation produces a "top-N per group" pivot — a frequent interview pattern for business analytics.

---

## Q52: PIVOT with Subquery — SQL Server Month Pivot

**Scenario:** Pivot monthly order counts so each month becomes a column, using a subquery to pre-aggregate.

**Schema:** `orders (order_id INT, order_date DATE)`

**Query:**
```sql
SELECT [Jan], [Feb], [Mar], [Apr], [May], [Jun]
FROM (
  SELECT FORMAT(order_date, 'MMM') AS month_name
  FROM orders
  WHERE order_date >= '2024-01-01' AND order_date < '2024-07-01'
) src
PIVOT (
  COUNT(*) FOR month_name IN ([Jan], [Feb], [Mar], [Apr], [May], [Jun])
) pvt;
```
**Explanation:** The PIVOT operator works on pre-aggregated or raw data. Here COUNT(*) in the PIVOT does the aggregation directly.

---

## Q53: UNPIVOT — Wide Feature Flags to Normalized Rows

**Scenario:** A `feature_flags` table has boolean columns for each feature. Unpivot to get one row per feature per user.

**Schema:** `feature_flags (user_id INT, dark_mode BOOLEAN, beta_access BOOLEAN, notifications BOOLEAN, analytics BOOLEAN)`

**Query:**
```sql
SELECT user_id, feature, enabled
FROM feature_flags
UNPIVOT (
  enabled FOR feature IN (dark_mode, beta_access, notifications, analytics)
) unpvt;
```
**Explanation:** UNPIVOT converts boolean columns into a normalized feature-enabled pairs structure, useful for permission checks and auditing.

**Alt1 (PostgreSQL LATERAL VALUES):**
```sql
SELECT f.user_id, v.feature, v.enabled
FROM feature_flags f
CROSS JOIN LATERAL (VALUES
  ('dark_mode', f.dark_mode),
  ('beta_access', f.beta_access),
  ('notifications', f.notifications),
  ('analytics', f.analytics)
) AS v(feature, enabled);
```

---

## Q54: Pivot — Wide to Long for Charts (MySQL)

**Scenario:** A charting library requires long-format data. Unpivot `chart_data` from wide (Jan–Jun columns) to long rows.

**Schema:** `chart_data (series_name VARCHAR, jan DECIMAL, feb DECIMAL, mar DECIMAL, apr DECIMAL, may DECIMAL, jun DECIMAL)`

**Query:**
```sql
SELECT series_name, 'Jan' AS month, jan AS value FROM chart_data
UNION ALL SELECT series_name, 'Feb', feb FROM chart_data
UNION ALL SELECT series_name, 'Mar', mar FROM chart_data
UNION ALL SELECT series_name, 'Apr', apr FROM chart_data
UNION ALL SELECT series_name, 'May', may FROM chart_data
UNION ALL SELECT series_name, 'Jun', jun FROM chart_data
ORDER BY series_name, month;
```
**Explanation:** Chart libraries (D3, Chart.js, Plotly) typically require long-format data. UNION ALL unpivots wide columns into the standard series-value-month format.

---

## Q55: Pivot with Multiple GROUP BY Columns — Multi-Dimensional Pivot

**Scenario:** Pivot `sales_by_channel` by product category AND year, producing a matrix for each year-category pair.

**Schema:** `sales_by_channel (year INT, category VARCHAR, channel VARCHAR, revenue DECIMAL)`

**Query:**
```sql
SELECT
  year,
  category,
  SUM(CASE WHEN channel = 'online'  THEN revenue ELSE 0 END) AS online,
  SUM(CASE WHEN channel = 'retail'  THEN revenue ELSE 0 END) AS retail,
  SUM(CASE WHEN channel = 'wholesale' THEN revenue ELSE 0 END) AS wholesale
FROM sales_by_channel
GROUP BY year, category
ORDER BY year, category;
```
**Explanation:** Multiple GROUP BY columns create a multi-dimensional pivot. Each unique year-category combination gets its own row with pivoted channel columns.

---

## Q56: Dynamic Pivot with IFNULL — MySQL Null-Safe Pivot

**Scenario:** Build a dynamic pivot for `student_marks` where some students may have no marks in certain subjects.

**Schema:** `student_marks (student_id INT, subject VARCHAR, marks INT)`

**Query:**
```sql
SET @sql = NULL;

SELECT GROUP_CONCAT(
  DISTINCT CONCAT(
    'IFNULL(SUM(CASE WHEN subject = ''', subject,
    ''' THEN marks END), 0) AS `', subject, '`'
  )
  ORDER BY subject
) INTO @sql
FROM student_marks;

SET @sql = CONCAT('SELECT student_id, ', @sql, ' FROM student_marks GROUP BY student_id');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```
**Explanation:** IFNULL wraps the CASE-SUM to convert NULL results (no marks in a subject) to 0, ensuring clean numerical output.

---

## Q57: PIVOT with Aggregated Subquery — SQL Server Summary

**Scenario:** Pivot a subquery that computes total sales per salesperson per quarter.

**Schema:** `sales (salesperson_id INT, sale_date DATE, amount DECIMAL)`

**Query:**
```sql
SELECT salesperson_id, Q1, Q2, Q3, Q4
FROM (
  SELECT
    salesperson_id,
    'Q' + CAST(DATEPART(QUARTER, sale_date) AS VARCHAR) AS quarter,
    amount
  FROM sales
) src
PIVOT (
  SUM(amount) FOR quarter IN (Q1, Q2, Q3, Q4)
) pvt;
```
**Explanation:** DATEPART extracts the quarter, and the PIVOT aggregates the amounts. The subquery pre-formats the quarter label for the PIVOT operator.

---

## Q58: Conditional Aggregation — Pivot with Window Function

**Scenario:** Pivot monthly revenue for each store, then use a window function to compute each store's share of total revenue across all stores.

**Schema:** `store_monthly (store_id INT, month DATE, revenue DECIMAL)`

**Query:**
```sql
WITH pivoted AS (
  SELECT
    store_id,
    SUM(CASE WHEN month = '2024-01-01' THEN revenue ELSE 0 END) AS jan,
    SUM(CASE WHEN month = '2024-02-01' THEN revenue ELSE 0 END) AS feb,
    SUM(CASE WHEN month = '2024-03-01' THEN revenue ELSE 0 END) AS mar
  FROM store_monthly
  GROUP BY store_id
)
SELECT
  store_id, jan, feb, mar,
  jan + feb + mar AS q1_total,
  ROUND((jan + feb + mar) / SUM(jan + feb + mar) OVER () * 100, 2) AS pct_of_total
FROM pivoted;
```
**Explanation:** Combining a pivot with a window function SUM(...) OVER () enables computing each row's contribution to the grand total — a common analytical extension.

---

## Q59: UNPIVOT — Wide Temperature Data to Long (Oracle)

**Scenario:** Unpivot a `city_temperatures` table where each column represents a month's average temperature.

**Schema:** `city_temperatures (city VARCHAR, jan_temp NUMBER, feb_temp NUMBER, mar_temp NUMBER)`

**Query:**
```sql
SELECT city, month, temperature
FROM city_temperatures
UNPIVOT (
  temperature FOR month IN (jan_temp AS 'Jan', feb_temp AS 'Feb', mar_temp AS 'Mar')
);
```
**Explanation:** Oracle UNPIVOT maps column names to label strings. The AS keyword in the IN list provides human-readable month names in the output.

---

## Q60: Pivot — Cross-Tabulation of Gender vs. Department

**Scenario:** Cross-tabulate employee count by gender (rows) and department (columns).

**Schema:** `employees (emp_id INT, gender VARCHAR, dept VARCHAR)`

**Query:**
```sql
SELECT
  gender,
  COUNT(CASE WHEN dept = 'Engineering' THEN 1 END) AS engineering,
  COUNT(CASE WHEN dept = 'Marketing'   THEN 1 END) AS marketing,
  COUNT(CASE WHEN dept = 'Finance'     THEN 1 END) AS finance,
  COUNT(CASE WHEN dept = 'HR'          THEN 1 END) AS hr
FROM employees
GROUP BY gender;
```
**Explanation:** A cross-tabulation (contingency table) is a specialized pivot that counts occurrences across two categorical dimensions.

---

## Q61: Dynamic Pivot with CONCAT_WS — MySQL Cleaner Output

**Scenario:** Dynamically pivot `web_analytics` where metric names are unknown, using CONCAT_WS for cleaner column list generation.

**Schema:** `web_analytics (page_url VARCHAR, metric_name VARCHAR, metric_value DECIMAL)`

**Query:**
```sql
SET @sql = NULL;

SELECT CONCAT_WS(', ',
  GROUP_CONCAT(
    CONCAT('MAX(CASE WHEN metric_name = ''', metric_name,
           ''' THEN metric_value END) AS `', metric_name, '`')
    ORDER BY metric_name
  )
) INTO @sql
FROM (SELECT DISTINCT metric_name FROM web_analytics) t;

SET @sql = CONCAT('SELECT page_url, ', @sql, ' FROM web_analytics GROUP BY page_url');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```
**Explanation:** CONCAT_WS adds commas between expressions cleanly. The subquery with DISTINCT ensures each metric appears exactly once.

---

## Q62: PIVOT with DATE-Based Columns — Year Pivot

**Scenario:** Pivot `yearly_budget` so each year becomes a column showing department budgets.

**Schema:** `yearly_budget (dept VARCHAR, budget_year INT, budget DECIMAL)`

**Query:**
```sql
SELECT
  dept,
  SUM(CASE WHEN budget_year = 2022 THEN budget ELSE 0 END) AS y2022,
  SUM(CASE WHEN budget_year = 2023 THEN budget ELSE 0 END) AS y2023,
  SUM(CASE WHEN budget_year = 2024 THEN budget ELSE 0 END) AS y2024
FROM yearly_budget
GROUP BY dept;
```
**Explanation:** Pivoting on year values is common for budget and financial trend analysis. Each year gets its own CASE expression.

---

## Q63: Unpivot with Lateral Join — PostgreSQL Flexible Unpivot

**Scenario:** Unpivot an `eav_staging` table that stores entity-attribute-value data in a wide format, using lateral join for maximum flexibility.

**Schema:** `eav_staging (entity_id INT, attr_a VARCHAR, attr_b VARCHAR, attr_c VARCHAR, attr_d VARCHAR)`

**Query:**
```sql
SELECT e.entity_id, v.attr_name, v.attr_value
FROM eav_staging e
CROSS JOIN LATERAL (VALUES
  ('attr_a', e.attr_a),
  ('attr_b', e.attr_b),
  ('attr_c', e.attr_c),
  ('attr_d', e.attr_d)
) AS v(attr_name, attr_value)
WHERE v.attr_value IS NOT NULL;
```
**Explanation:** LATERAL VALUES in PostgreSQL unpivots without UNION ALL overhead. The WHERE clause filters NULLs for sparse data.

---

## Q64: Pivot — Product Availability Matrix

**Scenario:** Pivot `store_inventory` to show product availability (in-stock = 1, out = 0) per store.

**Schema:** `store_inventory (product VARCHAR, store VARCHAR, in_stock BOOLEAN)`

**Query:**
```sql
SELECT
  product,
  MAX(CASE WHEN store = 'Store-A' THEN CASE WHEN in_stock THEN 1 ELSE 0 END END) AS store_a,
  MAX(CASE WHEN store = 'Store-B' THEN CASE WHEN in_stock THEN 1 ELSE 0 END END) AS store_b,
  MAX(CASE WHEN store = 'Store-C' THEN CASE WHEN in_stock THEN 1 ELSE 0 END END) AS store_c
FROM store_inventory
GROUP BY product;
```
**Explanation:** Boolean-to-integer conversion within CASE produces a binary availability matrix. MAX collapses to a single row per product.

---

## Q65: Conditional Aggregation with FILTER — PostgreSQL Login Matrix

**Scenario:** Produce a weekly login matrix: users as rows, days of week as columns, with login counts.

**Schema:** `logins (user_id INT, login_time TIMESTAMP)`

**Query:**
```sql
SELECT
  user_id,
  COUNT(*) FILTER (WHERE EXTRACT(DOW FROM login_time) = 0) AS sun,
  COUNT(*) FILTER (WHERE EXTRACT(DOW FROM login_time) = 1) AS mon,
  COUNT(*) FILTER (WHERE EXTRACT(DOW FROM login_time) = 2) AS tue,
  COUNT(*) FILTER (WHERE EXTRACT(DOW FROM login_time) = 3) AS wed,
  COUNT(*) FILTER (WHERE EXTRACT(DOW FROM login_time) = 4) AS thu,
  COUNT(*) FILTER (WHERE EXTRACT(DOW FROM login_time) = 5) AS fri,
  COUNT(*) FILTER (WHERE EXTRACT(DOW FROM login_time) = 6) AS sat
FROM logins
GROUP BY user_id;
```
**Explanation:** PostgreSQL FILTER clause is a clean alternative to CASE for conditional counts. It's more readable and semantically explicit.

**Alt1 (MySQL conditional aggregation):**
```sql
SELECT
  user_id,
  SUM(CASE WHEN DAYOFWEEK(login_time) = 1 THEN 1 ELSE 0 END) AS sun,
  SUM(CASE WHEN DAYOFWEEK(login_time) = 2 THEN 1 ELSE 0 END) AS mon,
  SUM(CASE WHEN DAYOFWEEK(login_time) = 3 THEN 1 ELSE 0 END) AS tue,
  SUM(CASE WHEN DAYOFWEEK(login_time) = 4 THEN 1 ELSE 0 END) AS wed,
  SUM(CASE WHEN DAYOFWEEK(login_time) = 5 THEN 1 ELSE 0 END) AS thu,
  SUM(CASE WHEN DAYOFWEEK(login_time) = 6 THEN 1 ELSE 0 END) AS fri,
  SUM(CASE WHEN DAYOFWEEK(login_time) = 7 THEN 1 ELSE 0 END) AS sat
FROM logins
GROUP BY user_id;
```

---

## Q66: PIVOT — Matrix of User Pairs with Interaction Counts

**Scenario:** Build a user interaction matrix from `chat_messages` — rows and columns are user IDs, values are message counts between pairs.

**Schema:** `chat_messages (sender_id INT, receiver_id INT)`

**Query:**
```sql
WITH all_users AS (
  SELECT DISTINCT user_id FROM (
    SELECT sender_id AS user_id FROM chat_messages
    UNION
    SELECT receiver_id AS user_id FROM chat_messages
  ) t
),
counts AS (
  SELECT sender_id, receiver_id, COUNT(*) AS msg_count
  FROM chat_messages
  GROUP BY sender_id, receiver_id
)
SELECT
  u1.user_id AS from_user,
  u2.user_id AS to_user,
  COALESCE(c.msg_count, 0) AS messages
FROM all_users u1
CROSS JOIN all_users u2
LEFT JOIN counts c ON c.sender_id = u1.user_id AND c.receiver_id = u2.user_id
ORDER BY u1.user_id, u2.user_id;
```
**Explanation:** Cross join of users creates the full matrix skeleton; LEFT JOIN populates values; COALESCE fills zeros for non-existent pairs.

---

## Q67: UNPIVOT — Wide Audit Log to Long Format

**Scenario:** An audit log has columns `old_value` and `new_value`. Unpivot to get separate rows for before/after states.

**Schema:** `audit_log (record_id INT, changed_at TIMESTAMP, field_name VARCHAR, old_value VARCHAR, new_value VARCHAR)`

**Query:**
```sql
SELECT record_id, changed_at, field_name, 'before' AS state, old_value AS value
FROM audit_log
UNION ALL
SELECT record_id, changed_at, field_name, 'after', new_value
FROM audit_log;
```
**Explanation:** Self-referencing UNION ALL unpivots paired columns into rows with a state discriminator. This is the standard audit-trail normalization pattern.

**Alt1 (SQL Server UNPIVOT):**
```sql
SELECT record_id, changed_at, field_name, state, value
FROM (
  SELECT record_id, changed_at, field_name,
    CAST(old_value AS VARCHAR(MAX)) AS old_value,
    CAST(new_value AS VARCHAR(MAX)) AS new_value
  FROM audit_log
) src
UNPIVOT (
  value FOR state IN (old_value, new_value)
) unpvt;
```

---

## Q68: Pivot with Running Total — Cumulative Monthly Pivot

**Scenario:** Pivot monthly revenue into columns, then compute running totals across months.

**Schema:** `monthly_revenue (dept VARCHAR, rev_month DATE, revenue DECIMAL)`

**Query:**
```sql
WITH pivoted AS (
  SELECT
    dept,
    SUM(CASE WHEN rev_month = '2024-01-01' THEN revenue ELSE 0 END) AS jan,
    SUM(CASE WHEN rev_month = '2024-02-01' THEN revenue ELSE 0 END) AS feb,
    SUM(CASE WHEN rev_month = '2024-03-01' THEN revenue ELSE 0 END) AS mar
  FROM monthly_revenue
  GROUP BY dept
)
SELECT
  dept, jan, feb, mar,
  jan AS jan_cum,
  jan + feb AS feb_cum,
  jan + feb + mar AS mar_cum
FROM pivoted;
```
**Explanation:** Post-pivot computation of running totals is straightforward in SQL — just accumulate columns with addition.

---

## Q69: Dynamic Pivot — PostgreSQL regexp Pattern Matching

**Scenario:** Pivot `metrics_log` where metric names follow a pattern (e.g., `cpu_avg`, `cpu_max`, `mem_avg`). Use regexp to identify columns dynamically.

**Schema:** `metrics_log (server_id INT, metric_name VARCHAR, metric_value DECIMAL)`

**Query:**
```sql
DO $$
DECLARE
  cols TEXT;
  sql  TEXT;
BEGIN
  SELECT STRING_AGG(
    format('MAX(CASE WHEN metric_name = %L THEN metric_value END) AS %I', metric_name, metric_name),
    ', '
  ) INTO cols
  FROM (SELECT DISTINCT metric_name FROM metrics_log ORDER BY metric_name) t;

  sql := format('SELECT server_id, %s FROM metrics_log GROUP BY server_id', cols);
  EXECUTE sql;
END $$;
```
**Explanation:** The anonymous DO block dynamically builds a pivot query using STRING_AGG. This is PostgreSQL's equivalent of MySQL's prepared statement approach.

---

## Q70: Pivot — Contact Preferences Matrix

**Scenario:** Pivot `contact_preferences` to show each customer's preferred contact method as a boolean flag.

**Schema:** `contact_preferences (customer_id INT, method VARCHAR)`

**Query:**
```sql
SELECT
  customer_id,
  MAX(CASE WHEN method = 'email'   THEN 1 ELSE 0 END) AS prefers_email,
  MAX(CASE WHEN method = 'sms'     THEN 1 ELSE 0 END) AS prefers_sms,
  MAX(CASE WHEN method = 'phone'   THEN 1 ELSE 0 END) AS prefers_phone,
  MAX(CASE WHEN method = 'mail'    THEN 1 ELSE 0 END) AS prefers_mail
FROM contact_preferences
GROUP BY customer_id;
```
**Explanation:** One-hot encoding with MAX(CASE WHEN ... THEN 1 ELSE 0 END) produces clean binary flags for each contact method.

---

## Q71: UNPIVOT + Lateral — PostgreSQL Wide to Long with Calculations

**Scenario:** Unpivot `budget_allocation` and compute percentage of total budget per department after unpivoting.

**Schema:** `budget_allocation (dept VARCHAR, q1 DECIMAL, q2 DECIMAL, q3 DECIMAL, q4 DECIMAL)`

**Query:**
```sql
WITH unpivoted AS (
  SELECT d.dept, v.quarter, v.amount
  FROM budget_allocation d
  CROSS JOIN LATERAL (VALUES
    ('Q1', d.q1), ('Q2', d.q2), ('Q3', d.q3), ('Q4', d.q4)
  ) AS v(quarter, amount)
)
SELECT
  dept, quarter, amount,
  ROUND(amount / SUM(amount) OVER (PARTITION BY dept) * 100, 2) AS pct_of_annual
FROM unpivoted
ORDER BY dept, quarter;
```
**Explanation:** After unpivoting, window functions compute each quarter's percentage of the annual total per department — demonstrating post-unpivot analytics.

---

## Q72: Pivot — Server Health Dashboard

**Scenario:** Pivot `health_checks` to produce a dashboard showing last check status per service per server.

**Schema:** `health_checks (server_id INT, service_name VARCHAR, status VARCHAR, checked_at TIMESTAMP)`

**Query:**
```sql
WITH latest AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY server_id, service_name ORDER BY checked_at DESC) AS rn
  FROM health_checks
)
SELECT
  server_id,
  MAX(CASE WHEN service_name = 'api'      AND rn = 1 THEN status END) AS api_status,
  MAX(CASE WHEN service_name = 'database' AND rn = 1 THEN status END) AS db_status,
  MAX(CASE WHEN service_name = 'cache'    AND rn = 1 THEN status END) AS cache_status,
  MAX(CASE WHEN service_name = 'queue'    AND rn = 1 THEN status END) AS queue_status
FROM latest
GROUP BY server_id;
```
**Explanation:** ROW_NUMBER filters to the most recent check per service, then conditional aggregation pivots service names into columns.

---

## Q73: PIVOT with LIKE — SQL Server Pattern-Based Pivot

**Scenario:** Pivot `server_metrics` where metric names follow a pattern. Use LIKE to pre-filter before pivoting.

**Schema:** `server_metrics (server_id INT, metric_name VARCHAR, metric_value DECIMAL)`

**Query:**
```sql
SELECT server_id, [cpu_avg], [cpu_max], [mem_avg], [mem_max]
FROM (
  SELECT server_id, metric_name, metric_value
  FROM server_metrics
  WHERE metric_name LIKE 'cpu_%' OR metric_name LIKE 'mem_%'
) src
PIVOT (
  AVG(metric_value) FOR metric_name IN ([cpu_avg], [cpu_max], [mem_avg], [mem_max])
) pvt;
```
**Explanation:** Pre-filtering with LIKE in the subquery reduces the dataset before PIVOT, improving performance and clarity.

---

## Q74: Conditional Aggregation — Pivot with Complex Expressions

**Scenario:** For each product, pivot to show the ratio of online to offline sales and the total, with complex derived metrics.

**Schema:** `sales_data (product VARCHAR, channel VARCHAR, revenue DECIMAL)`

**Query:**
```sql
SELECT
  product,
  SUM(CASE WHEN channel = 'online'  THEN revenue ELSE 0 END) AS online_rev,
  SUM(CASE WHEN channel = 'offline' THEN revenue ELSE 0 END) AS offline_rev,
  SUM(CASE WHEN channel = 'online'  THEN revenue ELSE 0 END) +
  SUM(CASE WHEN channel = 'offline' THEN revenue ELSE 0 END) AS total_rev,
  ROUND(
    SUM(CASE WHEN channel = 'online' THEN revenue ELSE 0 END) * 100.0 /
    NULLIF(
      SUM(CASE WHEN channel = 'online'  THEN revenue ELSE 0 END) +
      SUM(CASE WHEN channel = 'offline' THEN revenue ELSE 0 END), 0
    ), 2
  ) AS online_pct
FROM sales_data
GROUP BY product;
```
**Explanation:** Pivot values can be combined in derived expressions for ratio, percentage, and variance calculations — extending the basic pivot into analytical territory.

---

## Q75: UNPIVOT — Wide Log Table to Long Format (MySQL)

**Scenario:** A `service_logs` table stores error counts per service as columns. Unpivot for time-series analysis.

**Schema:** `service_logs (log_date DATE, auth_errors INT, db_errors INT, api_errors INT, cache_errors INT)`

**Query:**
```sql
SELECT log_date, service, error_count
FROM service_logs
CROSS JOIN (SELECT 'auth' AS service UNION ALL SELECT 'db' UNION ALL SELECT 'api' UNION ALL SELECT 'cache') services
WHERE (service = 'auth'  AND auth_errors  IS NOT NULL)
   OR (service = 'db'    AND db_errors    IS NOT NULL)
   OR (service = 'api'   AND api_errors   IS NOT NULL)
   OR (service = 'cache' AND cache_errors IS NOT NULL);
```
**Explanation:** MySQL lacks UNPIVOT, so a cross join with a derived table of service names simulates it. The WHERE clause filters NULLs for sparse data.

**Alt1 (PostgreSQL LATERAL VALUES):**
```sql
SELECT s.log_date, v.service, v.error_count
FROM service_logs s
CROSS JOIN LATERAL (VALUES
  ('auth',  s.auth_errors),
  ('db',    s.db_errors),
  ('api',   s.api_errors),
  ('cache', s.cache_errors)
) AS v(service, error_count)
WHERE v.error_count IS NOT NULL;
```

---

## Q76: Pivot — Confusion Matrix with Normalized Percentages

**Scenario:** Build a confusion matrix from `ml_predictions` and normalize each row to show percentages alongside counts.

**Schema:** `ml_predictions (sample_id INT, actual VARCHAR, predicted VARCHAR)`

**Query:**
```sql
WITH counts AS (
  SELECT
    actual,
    SUM(CASE WHEN predicted = 'spam'    THEN 1 ELSE 0 END) AS pred_spam,
    SUM(CASE WHEN predicted = 'ham'     THEN 1 ELSE 0 END) AS pred_ham,
    COUNT(*) AS total
  FROM ml_predictions
  GROUP BY actual
)
SELECT
  actual,
  pred_spam, pred_ham,
  ROUND(pred_spam * 100.0 / total, 2) AS spam_pct,
  ROUND(pred_ham  * 100.0 / total, 2) AS ham_pct
FROM counts;
```
**Explanation:** A confusion matrix pivot combined with percentage normalization gives both absolute and relative performance metrics, essential for ML model evaluation interviews.

---

## Q77: PIVOT with GROUPING SETS — Summary Rows

**Scenario:** Pivot `quarterly_sales` and include subtotal rows using GROUPING SETS for region and overall totals.

**Schema:** `quarterly_sales (region VARCHAR, product VARCHAR, quarter VARCHAR, revenue DECIMAL)`

**Query:**
```sql
SELECT
  COALESCE(region, 'ALL REGIONS') AS region,
  SUM(CASE WHEN quarter = 'Q1' THEN revenue ELSE 0 END) AS q1,
  SUM(CASE WHEN quarter = 'Q2' THEN revenue ELSE 0 END) AS q2,
  SUM(CASE WHEN quarter = 'Q3' THEN revenue ELSE 0 END) AS q3,
  SUM(CASE WHEN quarter = 'Q4' THEN revenue ELSE 0 END) AS q4
FROM quarterly_sales
GROUP BY GROUPING SETS ((region), ())
ORDER BY GROUPING(region), region;
```
**Explanation:** GROUPING SETS adds aggregate rows (subtotals) alongside detail rows. The pivot columns remain the same; the grouping dimension expands.

---

## Q78: Dynamic Pivot — SQL Server with QUOTENAME and STRING_AGG

**Scenario:** Dynamically pivot `event_metrics` where metric names contain spaces and special characters.

**Schema:** `event_metrics (event_id INT, metric_name VARCHAR, metric_value DECIMAL)`

**Query:**
```sql
DECLARE @cols NVARCHAR(MAX), @sql NVARCHAR(MAX);

SELECT @cols = STRING_AGG(QUOTENAME(metric_name), ', ') WITHIN GROUP (ORDER BY metric_name)
FROM (SELECT DISTINCT metric_name FROM event_metrics) AS t;

SET @sql = N'SELECT event_id, ' + @cols + N'
             FROM event_metrics
             PIVOT (MAX(metric_value) FOR metric_name IN (' + @cols + N')) pvt';

EXEC sp_executesql @sql;
```
**Explanation:** QUOTENAME automatically handles special characters by wrapping names in brackets. This is essential for production dynamic pivots with user-generated category names.

---

## Q79: UNPIVOT with Cast — Oracle Wide to Long with Type Conversion

**Scenario:** Unpivot `financial_summary` where monetary values are stored as VARCHAR, requiring CAST during unpivot.

**Schema:** `financial_summary (account_id INT, revenue_str VARCHAR, cost_str VARCHAR, profit_str VARCHAR)`

**Query:**
```sql
SELECT
  account_id,
  metric,
  CAST(value AS NUMBER(12,2)) AS numeric_value
FROM financial_summary
UNPIVOT (
  value FOR metric IN (revenue_str AS 'REVENUE', cost_str AS 'COST', profit_str AS 'PROFIT')
);
```
**Explanation:** Oracle UNPIVOT can accept VARCHAR columns and CAST converts them to numeric types. The AS labels provide readable metric names.

**Alt1 (PostgreSQL LATERAL VALUES with CAST):**
```sql
SELECT f.account_id, v.metric, v.value::NUMERIC(12,2) AS numeric_value
FROM financial_summary f
CROSS JOIN LATERAL (VALUES
  ('REVENUE', f.revenue_str),
  ('COST',    f.cost_str),
  ('PROFIT',  f.profit_str)
) AS v(metric, value);
```

---

## Q80: Pivot — Daily Active Users by Feature

**Scenario:** Pivot `feature_activations` to show daily active users per feature as columns.

**Schema:** `feature_activations (user_id INT, feature_name VARCHAR, activated_on DATE)`

**Query:**
```sql
SELECT
  activated_on,
  COUNT(DISTINCT CASE WHEN feature_name = 'search'    THEN user_id END) AS search_dau,
  COUNT(DISTINCT CASE WHEN feature_name = 'upload'    THEN user_id END) AS upload_dau,
  COUNT(DISTINCT CASE WHEN feature_name = 'messaging' THEN user_id END) AS messaging_dau,
  COUNT(DISTINCT CASE WHEN feature_name = 'analytics' THEN user_id END) AS analytics_dau
FROM feature_activations
GROUP BY activated_on
ORDER BY activated_on;
```
**Explanation:** COUNT(DISTINCT CASE WHEN ...) counts unique users per feature per day — critical for DAU metrics where a user may activate a feature multiple times.

---

## Q81: Conditional Aggregation — Pivot with NULL Handling

**Scenario:** Pivot `sensor_data` to show average, min, and max temperature per sensor per month. Handle NULL readings gracefully.

**Schema:** `sensor_data (sensor_id INT, reading_month DATE, temperature DECIMAL)`

**Query:**
```sql
SELECT
  sensor_id,
  reading_month,
  ROUND(AVG(CASE WHEN EXTRACT(MONTH FROM reading_month) = 1  THEN temperature END), 2) AS jan_avg,
  ROUND(AVG(CASE WHEN EXTRACT(MONTH FROM reading_month) = 6  THEN temperature END), 2) AS jun_avg,
  ROUND(AVG(CASE WHEN EXTRACT(MONTH FROM reading_month) = 12 THEN temperature END), 2) AS dec_avg
FROM sensor_data
WHERE EXTRACT(MONTH FROM reading_month) IN (1, 6, 12)
GROUP BY sensor_id, reading_month;
```
**Explanation:** AVG ignores NULL values automatically, so non-matching CASE branches don't corrupt the average. The WHERE clause pre-filters to target months.

---

## Q82: PIVOT — Multiple Aggregates with GROUPING SETS

**Scenario:** For each region and quarter, pivot to show both SUM of revenue and COUNT of transactions. Include grand totals.

**Schema:** `transactions (txn_id INT, region VARCHAR, quarter VARCHAR, revenue DECIMAL)`

**Query:**
```sql
SELECT
  COALESCE(region, 'TOTAL') AS region,
  SUM(CASE WHEN quarter = 'Q1' THEN revenue ELSE 0 END) AS q1_rev,
  SUM(CASE WHEN quarter = 'Q2' THEN revenue ELSE 0 END) AS q2_rev,
  COUNT(CASE WHEN quarter = 'Q1' THEN 1 END) AS q1_count,
  COUNT(CASE WHEN quarter = 'Q2' THEN 1 END) AS q2_count
FROM transactions
GROUP BY GROUPING SETS ((region), ());
```
**Explanation:** Combining multiple aggregates with GROUPING SETS in a pivot produces both detail and summary rows — useful for executive dashboards.

---

## Q83: UNPIVOT — Wide Configuration Table to Key-Value Pairs

**Scenario:** Unpivot `app_config` where each column is a configuration key.

**Schema:** `app_config (app_name VARCHAR, theme VARCHAR, language VARCHAR, max_connections VARCHAR, timeout VARCHAR)`

**Query:**
```sql
SELECT app_name, config_key, config_value
FROM app_config
UNPIVOT (
  config_value FOR config_key IN (theme, language, max_connections, timeout)
) unpvt;
```
**Explanation:** Converting a configuration table from wide to key-value format enables generic configuration readers that iterate over rows instead of hardcoding column names.

**Alt1 (MySQL UNION ALL):**
```sql
SELECT app_name, 'theme'           AS config_key, theme           AS config_value FROM app_config
UNION ALL SELECT app_name, 'language',         language         FROM app_config
UNION ALL SELECT app_name, 'max_connections', max_connections  FROM app_config
UNION ALL SELECT app_name, 'timeout',         timeout          FROM app_config;
```

---

## Q84: Pivot — Employee Skills Matrix

**Scenario:** Pivot `employee_skills` to produce a skill-proficiency matrix: employees as rows, skills as columns, proficiency ratings as values.

**Schema:** `employee_skills (emp_id INT, skill VARCHAR, proficiency INT)`

**Query:**
```sql
SELECT
  emp_id,
  MAX(CASE WHEN skill = 'SQL'       THEN proficiency END) AS sql_rating,
  MAX(CASE WHEN skill = 'Python'    THEN proficiency END) AS python_rating,
  MAX(CASE WHEN skill = 'Java'      THEN proficiency END) AS java_rating,
  MAX(CASE WHEN skill = 'AWS'       THEN proficiency END) AS aws_rating,
  MAX(CASE WHEN skill = 'Docker'    THEN proficiency END) AS docker_rating
FROM employee_skills
GROUP BY emp_id;
```
**Explanation:** MAX with CASE preserves the actual rating value (not just presence/absence), producing a skill proficiency matrix for HR analytics.

---

## Q85: Dynamic Pivot — Oracle with XML-aggregated Column List

**Scenario:** Dynamically pivot `audit_events` in Oracle where event types are unknown, using XMLAGG to build the column list.

**Schema:** `audit_events (event_date DATE, event_type VARCHAR, event_count NUMBER)`

**Query:**
```sql
DECLARE
  cols VARCHAR2(4000);
  sql_stmt VARCHAR2(8000);
BEGIN
  SELECT LISTAGG(event_type, ', ') WITHIN GROUP (ORDER BY event_type)
  INTO cols
  FROM (SELECT DISTINCT event_type FROM audit_events);

  sql_stmt := 'SELECT event_date, ' || cols || '
               FROM audit_events
               PIVOT (SUM(event_count) FOR event_type IN (' || cols || '))
               ORDER BY event_date';

  EXECUTE IMMEDIATE sql_stmt;
END;
```
**Explanation:** Oracle's LISTAGG is equivalent to STRING_AGG/STRING_CONCAT. EXECUTE IMMEDIATE runs the dynamically built PIVOT statement.

**Alt1 (Oracle conditional aggregation):**
```sql
SELECT
  event_date,
  SUM(CASE WHEN event_type = 'login'  THEN event_count ELSE 0 END) AS login,
  SUM(CASE WHEN event_type = 'logout' THEN event_count ELSE 0 END) AS logout,
  SUM(CASE WHEN event_type = 'error'  THEN event_count ELSE 0 END) AS error
FROM audit_events
GROUP BY event_date;
```

---

## Q86: Pivot — Cross-Tab with SUM and COUNT on Different Columns

**Scenario:** Pivot `customer_orders` to show total revenue (SUM) and order count (COUNT) per product category per quarter.

**Schema:** `customer_orders (order_id INT, category VARCHAR, quarter VARCHAR, revenue DECIMAL)`

**Query:**
```sql
SELECT
  category,
  SUM(CASE WHEN quarter = 'Q1' THEN revenue ELSE 0 END) AS q1_revenue,
  COUNT(CASE WHEN quarter = 'Q1' THEN 1 END)             AS q1_orders,
  SUM(CASE WHEN quarter = 'Q2' THEN revenue ELSE 0 END) AS q2_revenue,
  COUNT(CASE WHEN quarter = 'Q2' THEN 1 END)             AS q2_orders
FROM customer_orders
GROUP BY category;
```
**Explanation:** Different aggregate functions per pivot cell (SUM for revenue, COUNT for orders) demonstrate the flexibility of conditional aggregation over PIVOT operator limitations.

---

## Q87: PIVOT — Weekly Sales Heatmap Data

**Scenario:** Pivot `daily_sales` to produce week-by-day-of-week sales matrix for heatmap visualization.

**Schema:** `daily_sales (sale_date DATE, revenue DECIMAL)`

**Query:**
```sql
SELECT
  EXTRACT(WEEK FROM sale_date)::INT AS week_num,
  SUM(CASE WHEN EXTRACT(DOW FROM sale_date) = 0 THEN revenue ELSE 0 END) AS sun,
  SUM(CASE WHEN EXTRACT(DOW FROM sale_date) = 1 THEN revenue ELSE 0 END) AS mon,
  SUM(CASE WHEN EXTRACT(DOW FROM sale_date) = 2 THEN revenue ELSE 0 END) AS tue,
  SUM(CASE WHEN EXTRACT(DOW FROM sale_date) = 3 THEN revenue ELSE 0 END) AS wed,
  SUM(CASE WHEN EXTRACT(DOW FROM sale_date) = 4 THEN revenue ELSE 0 END) AS thu,
  SUM(CASE WHEN EXTRACT(DOW FROM sale_date) = 5 THEN revenue ELSE 0 END) AS fri,
  SUM(CASE WHEN EXTRACT(DOW FROM sale_date) = 6 THEN revenue ELSE 0 END) AS sat
FROM daily_sales
GROUP BY EXTRACT(WEEK FROM sale_date)
ORDER BY week_num;
```
**Explanation:** Weekly heatmap data uses two dimensions: week number (rows) and day-of-week (columns). This pattern feeds directly into visualization libraries.

---

## Q88: UNPIVOT with Filter — Sparse Matrix to Dense Long

**Scenario:** Unpivot `sparse_matrix` and filter to only non-zero entries for efficient storage or visualization.

**Schema:** `sparse_matrix (row_id INT, col_a INT, col_b INT, col_c INT, col_d INT, col_e INT)`

**Query:**
```sql
SELECT row_id, column_name, value
FROM sparse_matrix
UNPIVOT (
  value FOR column_name IN (col_a, col_b, col_c, col_d, col_e)
) unpvt
WHERE value != 0;
```
**Explanation:** Filtering after unpivot removes zero entries, producing a sparse representation ideal for matrix visualization libraries and storage optimization.

---

## Q89: Pivot — Login Frequency Matrix

**Scenario:** Pivot `user_logins` to show login counts per hour of day for each user, producing a 24-column matrix.

**Schema:** `user_logins (user_id INT, login_hour INT)`

**Query:**
```sql
SELECT
  user_id,
  SUM(CASE WHEN login_hour = 0  THEN 1 ELSE 0 END) AS h00,
  SUM(CASE WHEN login_hour = 1  THEN 1 ELSE 0 END) AS h01,
  SUM(CASE WHEN login_hour = 2  THEN 1 ELSE 0 END) AS h02,
  SUM(CASE WHEN login_hour = 3  THEN 1 ELSE 0 END) AS h03,
  SUM(CASE WHEN login_hour = 4  THEN 1 ELSE 0 END) AS h04,
  SUM(CASE WHEN login_hour = 5  THEN 1 ELSE 0 END) AS h05,
  SUM(CASE WHEN login_hour = 6  THEN 1 ELSE 0 END) AS h06,
  SUM(CASE WHEN login_hour = 7  THEN 1 ELSE 0 END) AS h07,
  SUM(CASE WHEN login_hour = 8  THEN 1 ELSE 0 END) AS h08,
  SUM(CASE WHEN login_hour = 9  THEN 1 ELSE 0 END) AS h09,
  SUM(CASE WHEN login_hour = 10 THEN 1 ELSE 0 END) AS h10,
  SUM(CASE WHEN login_hour = 11 THEN 1 ELSE 0 END) AS h11,
  SUM(CASE WHEN login_hour = 12 THEN 1 ELSE 0 END) AS h12,
  SUM(CASE WHEN login_hour = 13 THEN 1 ELSE 0 END) AS h13,
  SUM(CASE WHEN login_hour = 14 THEN 1 ELSE 0 END) AS h14,
  SUM(CASE WHEN login_hour = 15 THEN 1 ELSE 0 END) AS h15,
  SUM(CASE WHEN login_hour = 16 THEN 1 ELSE 0 END) AS h16,
  SUM(CASE WHEN login_hour = 17 THEN 1 ELSE 0 END) AS h17,
  SUM(CASE WHEN login_hour = 18 THEN 1 ELSE 0 END) AS h18,
  SUM(CASE WHEN login_hour = 19 THEN 1 ELSE 0 END) AS h19,
  SUM(CASE WHEN login_hour = 20 THEN 1 ELSE 0 END) AS h20,
  SUM(CASE WHEN login_hour = 21 THEN 1 ELSE 0 END) AS h21,
  SUM(CASE WHEN login_hour = 22 THEN 1 ELSE 0 END) AS h22,
  SUM(CASE WHEN login_hour = 23 THEN 1 ELSE 0 END) AS h23
FROM user_logins
GROUP BY user_id;
```
**Explanation:** A 24-column pivot for hour-of-day analysis is a common pattern in behavioral analytics. Each CASE expression handles one hour.

---

## Q90: PIVOT with MAX and MIN — Sensor Range Pivot

**Scenario:** Pivot `temperature_readings` to show min and max temperature per sensor per month.

**Schema:** `temperature_readings (sensor_id INT, reading_month DATE, temperature DECIMAL)`

**Query:**
```sql
SELECT
  sensor_id,
  MIN(CASE WHEN EXTRACT(MONTH FROM reading_month) = 1  THEN temperature END) AS jan_min,
  MAX(CASE WHEN EXTRACT(MONTH FROM reading_month) = 1  THEN temperature END) AS jan_max,
  MIN(CASE WHEN EXTRACT(MONTH FROM reading_month) = 7  THEN temperature END) AS jul_min,
  MAX(CASE WHEN EXTRACT(MONTH FROM reading_month) = 7  THEN temperature END) AS jul_max
FROM temperature_readings
WHERE EXTRACT(MONTH FROM reading_month) IN (1, 7)
GROUP BY sensor_id;
```
**Explanation:** Multiple aggregate functions (MIN, MAX) per pivot cell produce range data — each cell shows a different statistic for the same category.

---

## Q91: UNPIVOT — Wide Comparison Table to Long

**Scenario:** A `benchmark_results` table stores performance metrics for different configurations as columns. Unpivot for comparison charts.

**Schema:** `benchmark_results (test_id INT, config_a_time DECIMAL, config_b_time DECIMAL, config_c_time DECIMAL)`

**Query:**
```sql
SELECT test_id, configuration, execution_time
FROM benchmark_results
UNPIVOT (
  execution_time FOR configuration IN (config_a_time, config_b_time, config_c_time)
) unpvt
ORDER BY test_id, configuration;
```
**Explanation:** Unpivoting benchmark results into long format enables grouped bar charts and box plots for performance comparison across configurations.

---

## Q92: Pivot — Cross-Tab with COALESCE and ORDER BY Expression

**Scenario:** Pivot `budget_data` and order results by total budget across all quarters.

**Schema:** `budget_data (dept VARCHAR, quarter VARCHAR, amount DECIMAL)`

**Query:**
```sql
SELECT
  dept,
  COALESCE(SUM(CASE WHEN quarter = 'Q1' THEN amount END), 0) AS q1,
  COALESCE(SUM(CASE WHEN quarter = 'Q2' THEN amount END), 0) AS q2,
  COALESCE(SUM(CASE WHEN quarter = 'Q3' THEN amount END), 0) AS q3,
  COALESCE(SUM(CASE WHEN quarter = 'Q4' THEN amount END), 0) AS q4,
  COALESCE(SUM(CASE WHEN quarter = 'Q1' THEN amount END), 0) +
  COALESCE(SUM(CASE WHEN quarter = 'Q2' THEN amount END), 0) +
  COALESCE(SUM(CASE WHEN quarter = 'Q3' THEN amount END), 0) +
  COALESCE(SUM(CASE WHEN quarter = 'Q4' THEN amount END), 0) AS total
FROM budget_data
GROUP BY dept
ORDER BY total DESC;
```
**Explanation:** Adding a computed total column and ordering by it produces a ranked pivot table — a common interview requirement.

---

## Q93: Dynamic Pivot — PostgreSQL with DO Block and EXECUTE

**Scenario:** Build a dynamic pivot for `performance_metrics` where metric names are stored in the database itself.

**Schema:** `performance_metrics (service_id INT, metric_name VARCHAR, metric_value NUMERIC)`

**Query:**
```sql
DO $$
DECLARE
  col_list TEXT;
  query    TEXT;
BEGIN
  SELECT STRING_AGG(
    format('MAX(CASE WHEN metric_name = %L THEN metric_value END) AS %I', metric_name, metric_name),
    ', ' ORDER BY metric_name
  ) INTO col_list
  FROM (SELECT DISTINCT metric_name FROM performance_metrics) sub;

  query := format(
    'SELECT service_id, %s FROM performance_metrics GROUP BY service_id ORDER BY service_id',
    col_list
  );

  RAISE NOTICE '%', query;
  -- In a function context: EXECUTE query; RETURN QUERY EXECUTE query;
END $$;
```
**Explanation:** The DO block dynamically constructs and optionally executes a pivot query. In production, this would be a function returning a table type.

---

## Q94: Pivot — Order Status Fulfillment Matrix

**Scenario:** Pivot `order_status` to show order counts per status per fulfillment center.

**Schema:** `order_status (order_id INT, fulfillment_center VARCHAR, status VARCHAR)`

**Query:**
```sql
SELECT
  fulfillment_center,
  COUNT(CASE WHEN status = 'pending'    THEN 1 END) AS pending,
  COUNT(CASE WHEN status = 'processing' THEN 1 END) AS processing,
  COUNT(CASE WHEN status = 'shipped'    THEN 1 END) AS shipped,
  COUNT(CASE WHEN status = 'delivered'  THEN 1 END) AS delivered,
  COUNT(CASE WHEN status = 'returned'   THEN 1 END) AS returned
FROM order_status
GROUP BY fulfillment_center;
```
**Explanation:** A fulfillment matrix shows operational status distribution across centers — a standard logistics analytics pattern.

---

## Q95: UNPIVOT — Wide API Response Times to Long

**Scenario:** Unpivot `api_performance` where response times per endpoint are stored as columns.

**Schema:** `api_performance (date DATE, auth_ms DECIMAL, search_ms DECIMAL, checkout_ms DECIMAL, admin_ms DECIMAL)`

**Query:**
```sql
SELECT date, endpoint, response_time_ms
FROM api_performance
UNPIVOT (
  response_time_ms FOR endpoint IN (auth_ms, search_ms, checkout_ms, admin_ms)
) unpvt
ORDER BY date, endpoint;
```
**Explanation:** Unpivoting API response times enables time-series analysis, percentile calculations, and alerting per endpoint in long format.

---

## Q96: Pivot — Matrix of Prerequisite Dependencies

**Scenario:** Build a course dependency matrix from `prerequisites` where rows are courses and columns indicate which courses are prerequisites.

**Schema:** `prerequisites (course_id INT, course_name VARCHAR, prerequisite_name VARCHAR)`

**Query:**
```sql
SELECT
  course_name,
  MAX(CASE WHEN prerequisite_name = 'Intro to CS'     THEN 1 ELSE 0 END) AS needs_intro_cs,
  MAX(CASE WHEN prerequisite_name = 'Data Structures' THEN 1 ELSE 0 END) AS needs_data_structures,
  MAX(CASE WHEN prerequisite_name = 'Algorithms'      THEN 1 ELSE 0 END) AS needs_algorithms,
  MAX(CASE WHEN prerequisite_name = 'Databases'       THEN 1 ELSE 0 END) AS needs_databases
FROM prerequisites
GROUP BY course_name;
```
**Explanation:** Binary prerequisite matrix is a classic pivot use case in educational data systems.

---

## Q97: Pivot with SUM and Running Aggregation — Quarterly Cumulative

**Scenario:** Pivot quarterly revenue and compute cumulative totals across quarters.

**Schema:** `quarterly_revenue (product VARCHAR, quarter VARCHAR, revenue DECIMAL)`

**Query:**
```sql
WITH pivoted AS (
  SELECT
    product,
    SUM(CASE WHEN quarter = 'Q1' THEN revenue ELSE 0 END) AS q1,
    SUM(CASE WHEN quarter = 'Q2' THEN revenue ELSE 0 END) AS q2,
    SUM(CASE WHEN quarter = 'Q3' THEN revenue ELSE 0 END) AS q3,
    SUM(CASE WHEN quarter = 'Q4' THEN revenue ELSE 0 END) AS q4
  FROM quarterly_revenue
  GROUP BY product
)
SELECT
  product, q1, q2, q3, q4,
  q1 AS q1_cum,
  q1 + q2 AS q2_cum,
  q1 + q2 + q3 AS q3_cum,
  q1 + q2 + q3 + q4 AS q4_cum
FROM pivoted;
```
**Explanation:** Post-pivot cumulative calculations are simple column additions — but interviewers often ask this to test whether you can combine pivoting with window-like logic.

---

## Q98: UNPIVOT with NULL Filtering — Clean Long Format

**Scenario:** Unpivot `user_preferences` and filter out NULL values to produce a clean long-format result.

**Schema:** `user_preferences (user_id INT, color_pref VARCHAR, font_pref VARCHAR, layout_pref VARCHAR, notification_pref VARCHAR)`

**Query:**
```sql
SELECT user_id, preference_type, preference_value
FROM user_preferences
UNPIVOT (
  preference_value FOR preference_type IN (color_pref, font_pref, layout_pref, notification_pref)
) unpvt
WHERE preference_value IS NOT NULL;
```
**Explanation:** Filtering NULLs after unpivot produces a clean long format. SQL Server UNPIVOT automatically excludes NULLs; Oracle UNPIVOT keeps them by default — the WHERE clause ensures consistency.

---

## Q99: Pivot — Dynamic Column Generation with STRING_AGG and FORMAT

**Scenario:** Dynamically pivot `quarterly_kpi` in SQL Server, formatting column names with year-quarter labels.

**Schema:** `quarterly_kpi (department VARCHAR, year_quarter VARCHAR, kpi_value DECIMAL)`

**Query:**
```sql
DECLARE @cols NVARCHAR(MAX), @sql NVARCHAR(MAX);

SELECT @cols = STRING_AGG(
  QUOTENAME(year_quarter), ', '
) WITHIN GROUP (ORDER BY year_quarter)
FROM (SELECT DISTINCT year_quarter FROM quarterly_kpi) AS t;

SET @sql = N'SELECT department, ' + @cols + N'
             FROM quarterly_kpi
             PIVOT (AVG(kpi_value) FOR year_quarter IN (' + @cols + N')) pvt
             ORDER BY department';

EXEC sp_executesql @sql;
```
**Explanation:** Dynamic PIVOT with STRING_AGG produces a spreadsheet-style layout where each column represents a year-quarter combination, ideal for executive KPI dashboards.

---

## Q100: Comprehensive Pivot — Wide Salary Report with Multiple Aggregates

**Scenario:** Build a comprehensive salary report pivoting `employee_compensation` to show base salary, bonus, and total compensation per grade level. Include overall averages.

**Schema:** `employee_compensation (emp_id INT, grade_level INT, base_salary DECIMAL, bonus DECIMAL, stock_options INT)`

**Query:**
```sql
WITH aggregated AS (
  SELECT
    grade_level,
    SUM(base_salary) AS total_base,
    SUM(bonus)       AS total_bonus,
    SUM(base_salary + bonus) AS total_comp,
    COUNT(*)         AS headcount,
    AVG(base_salary) AS avg_base,
    AVG(bonus)       AS avg_bonus
  FROM employee_compensation
  GROUP BY grade_level
)
SELECT
  grade_level,
  total_base,
  total_bonus,
  total_comp,
  headcount,
  ROUND(avg_base, 2)  AS avg_base,
  ROUND(avg_bonus, 2) AS avg_bonus,
  ROUND(total_comp * 100.0 / SUM(total_comp) OVER (), 2) AS pct_of_total
FROM aggregated
ORDER BY grade_level;
```
**Explanation:** This comprehensive pivot combines multiple aggregates (SUM, COUNT, AVG) with a window function (SUM OVER) to produce a complete compensation analysis report — a capstone pattern for pivot interviews.
