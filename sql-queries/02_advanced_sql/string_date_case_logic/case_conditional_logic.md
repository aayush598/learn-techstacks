# CASE and Conditional Logic in SQL — 100 Interview Q&A

## Q1: Write a query to label salaries as low, medium, or high using CASE.

**Query:**
```sql
SELECT employee_name, salary,
  CASE
    WHEN salary < 50000 THEN 'Low'
    WHEN salary < 100000 THEN 'Medium'
    ELSE 'High'
  END AS salary_band
FROM employees;
```

**Explanation:** Searched CASE evaluates WHEN clauses top-down; the first true branch wins and ELSE catches everything else.

## Q2: Write a query to map department codes to readable names using simple CASE.

**Query:**
```sql
SELECT employee_name,
  CASE department_code
    WHEN 'HR' THEN 'Human Resources'
    WHEN 'ENG' THEN 'Engineering'
    WHEN 'FIN' THEN 'Finance'
    ELSE 'Other'
  END AS department
FROM employees;
```

**Explanation:** Simple CASE compares one expression against each WHEN value using equality only.

**Alt1:** The same logic rewritten as a searched CASE for readable booleans:

```sql
SELECT employee_name,
  CASE
    WHEN department_code = 'HR' THEN 'Human Resources'
    WHEN department_code = 'ENG' THEN 'Engineering'
    ELSE 'Other'
  END AS department
FROM employees;
```

## Q3: Write a query that filters employees to 'Senior' earners using CASE in the WHERE clause.

**Query:**
```sql
SELECT employee_name, salary
FROM employees
WHERE CASE WHEN salary >= 100000 THEN 'Senior' ELSE 'Junior' END = 'Senior';
```

**Explanation:** CASE is just an expression, so it can be compared in WHERE and is evaluated once per row.

**Alt1:** Most engines let you skip CASE with a plain predicate, which is cheaper:

```sql
SELECT employee_name, salary
FROM employees
WHERE salary >= 100000;
```

## Q4: Write a query to bucket order amounts into size bands using BETWEEN inside CASE.

**Query:**
```sql
SELECT order_id, amount,
  CASE
    WHEN amount BETWEEN 1 AND 100 THEN 'Small'
    WHEN amount BETWEEN 101 AND 1000 THEN 'Medium'
    ELSE 'Large'
  END AS size_band
FROM orders;
```

**Explanation:** BETWEEN is inclusive and plugs directly into a WHEN condition.

## Q5: Write a query to group product categories with IN inside a CASE.

**Query:**
```sql
SELECT product_name, category,
  CASE
    WHEN category IN ('Laptops', 'Phones') THEN 'Devices'
    WHEN category IN ('Shirts', 'Shoes') THEN 'Apparel'
    ELSE 'Other'
  END AS aisle
FROM products;
```

**Explanation:** IN collapses several equality checks into one condition per WHEN branch.

## Q6: Write a query to classify email providers using LIKE inside CASE.

**Query:**
```sql
SELECT customer_name, email,
  CASE
    WHEN email LIKE '%@gmail.com' THEN 'Gmail'
    WHEN email LIKE '%@outlook.com' THEN 'Outlook'
    WHEN email LIKE '%@protonmail.com' THEN 'ProtonMail'
    ELSE 'Other'
  END AS provider
FROM customers;
```

**Explanation:** LIKE patterns let CASE work on partial string matches.

## Q7: Write a query to flag orders with missing delivery timestamps using IS NULL in CASE.

**Query:**
```sql
SELECT order_id, delivered_at,
  CASE
    WHEN delivered_at IS NULL THEN 'Pending'
    ELSE 'Delivered'
  END AS delivery_status
FROM orders;
```

**Explanation:** NULL never equals anything, so IS NULL is the correct condition to detect a missing timestamp.

**Alt1:** COALESCE can substitute a default label when NULL itself is the signal:

```sql
SELECT order_id, COALESCE(CAST(delivered_at AS VARCHAR(10)), 'Pending') AS delivery_status
FROM orders;
```

## Q8: Write a query that nests CASE to combine salary band with tenure.

**Query:**
```sql
SELECT employee_name, salary, tenure_years,
  CASE
    WHEN salary >= 100000 THEN
      CASE WHEN tenure_years >= 5 THEN 'Senior - tenured' ELSE 'Senior - new' END
    WHEN salary >= 50000 THEN 'Mid'
    ELSE 'Junior'
  END AS profile
FROM employees;
```

**Explanation:** The inner CASE is evaluated only when the outer branch matches, keeping deep logic readable.

## Q9: Write a query with multiple conditions and explicit precedence in CASE (AND/OR).

**Query:**
```sql
SELECT customer_name, region, is_active,
  CASE
    WHEN region = 'North' AND is_active = TRUE THEN 'Key account'
    WHEN region = 'North' OR is_active = TRUE THEN 'Watch'
    ELSE 'Standard'
  END AS tier
FROM customers;
```

**Explanation:** AND binds tighter than OR, and the first matching WHEN wins, so the narrow 'Key account' rule is checked before the broader OR rule.

## Q10: Write a query that produces boolean flags in CASE for later summing.

**Query:**
```sql
SELECT
  SUM(CASE WHEN is_vip THEN 1 ELSE 0 END) AS vip_count,
  SUM(CASE WHEN NOT is_vip THEN 1 ELSE 0 END) AS non_vip_count
FROM customers;
```

**Explanation:** Each row contributes 1 or 0, so SUM collapses the flags into counts.

## Q11: Write a query to pivot order counts by status into a single row.

**Query:**
```sql
SELECT
  SUM(CASE WHEN status = 'shipped'   THEN 1 ELSE 0 END) AS shipped_orders,
  SUM(CASE WHEN status = 'pending'   THEN 1 ELSE 0 END) AS pending_orders,
  SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders
FROM orders;
```

**Explanation:** Conditional aggregation turns rows into columns without a PIVOT clause.

## Q12: Write a query that buckets rows in GROUP BY using CASE.

**Query:**
```sql
SELECT
  CASE
    WHEN amount < 100  THEN 'small'
    WHEN amount < 1000 THEN 'medium'
    ELSE 'large'
  END AS order_bucket,
  COUNT(*) AS order_count,
  SUM(amount) AS bucket_revenue
FROM orders
GROUP BY order_bucket;
```

**Explanation:** GROUP BY order_bucket reuses the SELECT alias — accepted in MySQL and PostgreSQL; SQL Server needs the full expression (see Alt1).

**Alt1:** Portable: repeat the CASE expression in GROUP BY so every engine groups on the computed column:

```sql
SELECT
  CASE
    WHEN amount < 100  THEN 'small'
    WHEN amount < 1000 THEN 'medium'
    ELSE 'large'
  END AS order_bucket,
  COUNT(*) AS order_count
FROM orders
GROUP BY
  CASE
    WHEN amount < 100  THEN 'small'
    WHEN amount < 1000 THEN 'medium'
    ELSE 'large'
  END;
```

## Q13: Write a query to sort statuses in a custom, non-alphabetical order using CASE in ORDER BY.

**Query:**
```sql
SELECT status, COUNT(*) AS total
FROM orders
GROUP BY status
ORDER BY
  CASE status
    WHEN 'pending'   THEN 1
    WHEN 'shipped'   THEN 2
    WHEN 'delivered' THEN 3
    WHEN 'cancelled' THEN 4
    ELSE 5
  END;
```

**Explanation:** CASE turns each status into a numeric sort key; rows sort by that key order.

## Q14: Write a query to convert order status codes to human labels.

**Query:**
```sql
SELECT order_id,
  CASE status_code
    WHEN 'P' THEN 'Processing'
    WHEN 'S' THEN 'Shipped'
    WHEN 'D' THEN 'Delivered'
    WHEN 'X' THEN 'Cancelled'
    ELSE 'Unknown'
  END AS status_label
FROM orders;
```

**Explanation:** Simple CASE maps each code to its label; ELSE covers unknown codes.

**Alt1:** Oracle: DECODE is the terse equivalent of a simple CASE:

```sql
-- Oracle
SELECT order_id,
  DECODE(status_code, 'P', 'Processing', 'S', 'Shipped', 'D', 'Delivered',
         'X', 'Cancelled', 'Unknown') AS status_label
FROM orders;
```

## Q15: Write a CFO-style query applying discount tiers by order size.

**Query:**
```sql
SELECT order_id, amount,
  CASE
    WHEN amount >= 1000 THEN 0.20
    WHEN amount >= 500  THEN 0.10
    ELSE 0.00
  END AS discount_rate,
  amount * (1 -
    CASE
      WHEN amount >= 1000 THEN 0.20
      WHEN amount >= 500  THEN 0.10
      ELSE 0.00
    END) AS final_amount
FROM orders;
```

**Explanation:** CASE computes the tiered rate and the same CASE computes the discounted total.

## Q16: Write a query to compute progressive tax using CASE brackets.

**Query:**
```sql
-- PostgreSQL
SELECT employee_name, taxable_income,
  CASE
    WHEN taxable_income <= 100000 THEN taxable_income * 0.10
    WHEN taxable_income <= 200000 THEN 10000 + (taxable_income - 100000) * 0.20
    ELSE 30000 + (taxable_income - 200000) * 0.30
  END AS tax_due
FROM employees;
```

**Explanation:** Each upper bracket adds the flat tax of lower brackets plus its own marginal rate.

**Alt1:** SQL Server: nested IIF compresses the ladder into one expression:

```sql
-- SQL Server
SELECT employee_name, taxable_income,
  IIF(taxable_income <= 100000, taxable_income * 0.10,
    IIF(taxable_income <= 200000, 10000 + (taxable_income - 100000) * 0.20,
      30000 + (taxable_income - 200000) * 0.30)) AS tax_due
FROM employees;
```

## Q17: Write a query that computes shipping cost from weight rules.

**Query:**
```sql
SELECT order_id, weight_kg,
  CASE
    WHEN weight_kg <= 1  THEN 5.00
    WHEN weight_kg <= 5  THEN 10.00
    WHEN weight_kg <= 10 THEN 15.00
    ELSE 15.00 + (weight_kg - 10) * 1.50
  END AS shipping_cost
FROM orders;
```

**Explanation:** Fixed buckets set a base price and the ELSE adds an overage fee per extra kilogram.

## Q18: Write a query that protects a division by zero using CASE.

**Query:**
```sql
SELECT product_id, revenue, units_sold,
  CASE WHEN units_sold > 0 THEN revenue / units_sold ELSE 0 END AS avg_price
FROM sales;
```

**Explanation:** The division only runs when the denominator is positive; otherwise we return 0.

**Alt1:** NULLIF guard: convert a 0 denominator to NULL so the division yields NULL instead of erroring:

```sql
SELECT product_id, revenue / NULLIF(units_sold, 0) AS avg_price
FROM sales;
```

## Q19: Write a query to return a default contact value when the phone is missing, using COALESCE.

**Query:**
```sql
SELECT customer_name, COALESCE(phone, 'No phone on file') AS contact
FROM customers;
```

**Explanation:** COALESCE returns the first non-NULL argument.

**Alt1:** CASE is the verbose equivalent:

```sql
SELECT customer_name,
  CASE WHEN phone IS NULL THEN 'No phone on file' ELSE phone END AS contact
FROM customers;
```

## Q20: Write a query using MySQL's IF() to show availability as a label.

**Query:**
```sql
-- MySQL
SELECT product_name, stock,
  IF(stock > 0, 'In stock', 'Sold out') AS availability
FROM inventory;
```

**Explanation:** IF(condition, then, else) works like a two-branch CASE — a MySQL-only scalar function.

**Alt1:** Portable CASE:

```sql
SELECT product_name, stock,
  CASE WHEN stock > 0 THEN 'In stock' ELSE 'Sold out' END AS availability
FROM inventory;
```

## Q21: Write a query using SQL Server's IIF() to mark active products.

**Query:**
```sql
-- SQL Server
SELECT product_id, discontinued,
  IIF(discontinued = 0, 'Active', 'Discontinued') AS product_status
FROM products;
```

**Explanation:** IIF is a scalar function equivalent to a two-way CASE, available since SQL Server 2012.

**Alt1:** CASE keeps the same job portable:

```sql
SELECT product_id, discontinued,
  CASE WHEN discontinued = 0 THEN 'Active' ELSE 'Discontinued' END AS product_status
FROM products;
```

## Q22: Write a PostgreSQL query that marks stock levels — note PostgreSQL has no IF() in SELECT.

**Query:**
```sql
-- PostgreSQL
SELECT product_name, stock,
  CASE WHEN stock > 0 THEN 'In stock' ELSE 'Sold out' END AS availability
FROM inventory;
```

**Explanation:** IF exists only in PL/pgSQL procedures; inside a query PostgreSQL uses CASE and returns booleans.

**Alt1:** PostgreSQL's FILTER clause does conditional aggregation without any CASE:

```sql
-- PostgreSQL
SELECT COUNT(*) FILTER (WHERE stock = 0) AS out_of_stock,
       COUNT(*) FILTER (WHERE stock > 0) AS in_stock
FROM inventory;
```

## Q23: Write a query that computes a total which conditionally includes tax.

**Query:**
```sql
SELECT order_id, subtotal, tax, is_taxable,
  subtotal + CASE WHEN is_taxable THEN tax ELSE 0 END AS total
FROM orders;
```

**Explanation:** The tax term is added only when the flag is true — a conditionally computed column.

## Q24: Write a query to classify inventory health relative to the reorder level.

**Query:**
```sql
SELECT product_id, stock, reorder_level,
  CASE
    WHEN stock = 0 THEN 'Out'
    WHEN stock < reorder_level THEN 'Low'
    WHEN stock < 2 * reorder_level THEN 'OK'
    ELSE 'Healthy'
  END AS stock_status
FROM inventory;
```

**Explanation:** CASE can compare against other columns, not just literals, so thresholds vary per row.

## Q25: Write a query that converts empty strings into NULL using NULLIF.

**Query:**
```sql
SELECT employee_name, NULLIF(nickname, '') AS nickname
FROM employees;
```

**Explanation:** NULLIF(a, b) returns NULL when a equals b, cleaning empty strings into query-friendly NULLs.

**Alt1:** The CASE spelling of the same rule:

```sql
SELECT employee_name,
  CASE WHEN nickname = '' THEN NULL ELSE nickname END AS nickname
FROM employees;
```

## Q26: Write a query using CASE inside HAVING to find departments with many overdue invoices.

**Query:**
```sql
SELECT department_id,
  SUM(CASE WHEN status = 'overdue' THEN 1 ELSE 0 END) AS overdue_count
FROM invoices
GROUP BY department_id
HAVING SUM(CASE WHEN status = 'overdue' THEN 1 ELSE 0 END) > 10;
```

**Explanation:** The CASE flag is summed per group and HAVING re-evaluates the same aggregate to keep only groups above the threshold.

## Q27: Write a query that takes a conditional MIN() of due dates for overdue invoices.

**Query:**
```sql
SELECT MIN(CASE WHEN status = 'overdue' THEN due_date END) AS first_overdue
FROM invoices;
```

**Explanation:** When a branch returns NULL the aggregate MIN ignores it, so only overdue dates participate.

## Q28: Write a query to compute the cancellation rate as a percentage.

**Query:**
```sql
SELECT
  100.0 * SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*) AS cancel_rate_pct
FROM orders;
```

**Explanation:** Conditional count divided by the total; multiplying by 100.0 forces decimal division instead of integer truncation.

## Q29: Write a query counting high-value customers with DISTINCT inside a conditional aggregate.

**Query:**
```sql
SELECT
  COUNT(DISTINCT customer_id) AS all_customers,
  COUNT(DISTINCT CASE WHEN total_spent >= 5000 THEN customer_id END) AS vip_customers
FROM customer_totals;
```

**Explanation:** Aggregates skip NULLs, so the CASE returns NULL for non-VIP rows and they are never counted.

## Q30: Write a query that buckets age groups in SELECT and aggregates per bucket.

**Query:**
```sql
SELECT
  CASE
    WHEN age < 18 THEN 'Minor'
    WHEN age < 65 THEN 'Adult'
    ELSE 'Senior'
  END AS age_group,
  COUNT(*) AS people
FROM population
GROUP BY 1
ORDER BY people DESC;
```

**Explanation:** GROUP BY 1 references the first select item — accepted in MySQL and PostgreSQL; repeat the CASE in GROUP BY for SQL Server.

## Q31: Write a query to sort regions in a business-defined priority order.

**Query:**
```sql
SELECT region, SUM(sales) AS total_sales
FROM sales
GROUP BY region
ORDER BY
  CASE region
    WHEN 'EMEA' THEN 1
    WHEN 'AMER' THEN 2
    WHEN 'APAC' THEN 3
    ELSE 4
  END, total_sales DESC;
```

**Explanation:** CASE turns a priority list into numeric sort keys; total_sales then breaks ties within each priority.

**Alt1:** MySQL: FIELD() builds that ordering in one call and missing values sort last:

```sql
-- MySQL
SELECT region, SUM(sales) AS total_sales
FROM sales
GROUP BY region
ORDER BY FIELD(region, 'EMEA', 'AMER', 'APAC'), total_sales DESC;
```

## Q32: Write a query that controls where NULL rows appear in the sort.

**Query:**
```sql
-- PostgreSQL
SELECT employee_name, manager_id
FROM employees
ORDER BY
  CASE WHEN manager_id IS NULL THEN 0 ELSE 1 END,
  manager_id;
```

**Explanation:** The first sort key pushes NULL managers to the top (0) and the second key orders the rest.

**Alt1:** PostgreSQL and SQL Server have dedicated NULLS FIRST/LAST syntax:

```sql
-- PostgreSQL
SELECT employee_name, manager_id
FROM employees
ORDER BY manager_id NULLS FIRST;
```

## Q33: Write a query to flag transactions for fraud review using two conditions.

**Query:**
```sql
SELECT transaction_id, amount, customer_tenure_days,
  CASE
    WHEN amount > 10000 AND customer_tenure_days < 30 THEN 'Review'
    WHEN amount > 10000 THEN 'Flagged'
    ELSE 'Normal'
  END AS risk_level
FROM transactions;
```

**Explanation:** The narrowest rule comes first; fall-through handles the broader cases.

## Q34: Write a query that grants a senior discount when either rule passes (OR precedence).

**Query:**
```sql
SELECT customer_id, age, membership_years,
  CASE
    WHEN age >= 65 OR membership_years >= 10 THEN 'Eligible'
    ELSE 'Not eligible'
  END AS discount_eligibility
FROM customers;
```

**Explanation:** A single OR condition is enough — CASE simply tests the resulting boolean.

## Q35: Write a query to convert numeric scores into letter grades.

**Query:**
```sql
SELECT student_name, score,
  CASE
    WHEN score >= 90 THEN 'A'
    WHEN score >= 80 THEN 'B'
    WHEN score >= 70 THEN 'C'
    ELSE 'F'
  END AS grade
FROM grades;
```

**Explanation:** Ordered thresholds narrow downwards; the ELSE catches everything below 70.

**Alt1:** MySQL: nested IF() mimics the same ladder:

```sql
-- MySQL
SELECT student_name,
  IF(score >= 90, 'A', IF(score >= 80, 'B', IF(score >= 70, 'C', 'F'))) AS grade
FROM grades;
```

## Q36: Write a query that pivots counts of completed vs refunded orders per year.

**Query:**
```sql
SELECT EXTRACT(YEAR FROM order_date) AS year,
  SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_orders,
  SUM(CASE WHEN status = 'refunded'  THEN 1 ELSE 0 END) AS refunded_orders
FROM orders
GROUP BY EXTRACT(YEAR FROM order_date)
ORDER BY year;
```

**Explanation:** Each status gets its own SUM(CASE...) column while rows group by year.

## Q37: Write a query to sum positive revenue and refunds separately from one column.

**Query:**
```sql
SELECT product_id,
  SUM(CASE WHEN units >= 0 THEN revenue ELSE 0 END) AS sales_amount,
  SUM(CASE WHEN units < 0 THEN ABS(revenue) ELSE 0 END) AS refund_amount
FROM transactions
GROUP BY product_id;
```

**Explanation:** The sign of units routes each row into exactly one of the two conditional sums.

**Alt1:** SIGN() makes the routing branch explicit in a simple CASE:

```sql
SELECT product_id,
  SUM(CASE WHEN SIGN(units) >= 0 THEN revenue ELSE 0 END) AS sales_amount,
  SUM(CASE WHEN SIGN(units) < 0 THEN ABS(revenue) ELSE 0 END) AS refund_amount
FROM transactions
GROUP BY product_id;
```

## Q38: Write an Oracle query mapping status numbers to labels using DECODE.

**Query:**
```sql
-- Oracle
SELECT order_id,
  DECODE(status, 1, 'New', 2, 'Open', 3, 'Closed', 'Unknown') AS status_label
FROM orders;
```

**Explanation:** DECODE is Oracle's compact simple-CASE: value, search, result pairs, with an optional default at the end.

## Q39: Write a query computing a safe average price per category, guarding a zero aggregate denominator.

**Query:**
```sql
SELECT category_id,
  CASE WHEN SUM(units_sold) > 0
       THEN SUM(revenue) / SUM(units_sold)
       ELSE 0
  END AS avg_unit_price
FROM sales
GROUP BY category_id;
```

**Explanation:** The division only executes when the grouped denominator is positive.

## Q40: Write a PostgreSQL query counting active employees per department using FILTER.

**Query:**
```sql
-- PostgreSQL
SELECT department_id,
  COUNT(*) FILTER (WHERE status = 'active') AS active_employees,
  COUNT(*) AS total_employees
FROM employees
GROUP BY department_id;
```

**Explanation:** FILTER applies the predicate before counting — no CASE required.

**Alt1:** The same count as a portable conditional aggregation:

```sql
SELECT department_id,
  SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS active_employees
FROM employees
GROUP BY department_id;
```

## Q41: Write a query building a reporting line that handles missing managers.

**Query:**
```sql
-- PostgreSQL
SELECT employee_name || ' reports to ' ||
  CASE WHEN manager_name IS NULL THEN 'no one' ELSE manager_name END AS line
FROM employees;
```

**Explanation:** The CASE returns a string that concatenation can safely include without NULL poisoning the result.

## Q42: Write a query to label fiscal quarters from an order date.

**Query:**
```sql
SELECT order_id, order_date,
  CASE
    WHEN EXTRACT(MONTH FROM order_date) BETWEEN 1 AND 3 THEN 'Q1'
    WHEN EXTRACT(MONTH FROM order_date) BETWEEN 4 AND 6 THEN 'Q2'
    WHEN EXTRACT(MONTH FROM order_date) BETWEEN 7 AND 9 THEN 'Q3'
    ELSE 'Q4'
  END AS quarter
FROM orders;
```

**Explanation:** Calendar-month bands map to quarter labels; only the month part of the date is used.

## Q43: Write a query to label weekdays vs weekends.

**Query:**
```sql
-- PostgreSQL
SELECT order_id, order_date,
  CASE
    WHEN EXTRACT(DOW FROM order_date) IN (0, 6) THEN 'Weekend'
    ELSE 'Weekday'
  END AS day_type
FROM orders;
```

**Explanation:** DOW is 0=Sunday to 6=Saturday in PostgreSQL; other engines number days differently, hence the dialect comment.

## Q44: Write a query that builds reusable boolean flags from summary columns.

**Query:**
```sql
SELECT customer_id,
  CASE WHEN total_spend  > 5000 THEN 1 ELSE 0 END AS is_high_spender,
  CASE WHEN order_count > 3   THEN 1 ELSE 0 END AS is_repeat_buyer
FROM customer_summary;
```

**Explanation:** Flags persist per row and downstream queries can SUM() or filter on them.

## Q45: Write a query to build an employee band-per-department matrix.

**Query:**
```sql
SELECT department_id,
  SUM(CASE WHEN band = 'Junior' THEN 1 ELSE 0 END) AS juniors,
  SUM(CASE WHEN band = 'Senior' THEN 1 ELSE 0 END) AS seniors
FROM employees
GROUP BY department_id;
```

**Explanation:** One CASE-column per band; each row increments exactly one column.

## Q46: Write a query that computes a raise from a performance rating with CASE.

**Query:**
```sql
SELECT employee_name, salary, rating,
  CASE
    WHEN rating = 5 THEN salary * 1.10
    WHEN rating = 4 THEN salary * 1.05
    ELSE salary * 1.00
  END AS new_salary
FROM employees;
```

**Explanation:** Rating buckets map to multipliers, and the ELSE keeps everyone else moving too.

## Q47: Write a query computing a completion percentage safely.

**Query:**
```sql
SELECT department_id,
  SUM(CASE WHEN task_completed THEN 1 ELSE 0 END) * 100.0 /
    NULLIF(COUNT(*), 0) AS completion_pct
FROM tasks
GROUP BY department_id;
```

**Explanation:** NULLIF(COUNT(*), 0) turns an empty group into NULL so the division cannot error.

## Q48: Write a query to label the time of day from an order time.

**Query:**
```sql
SELECT order_time,
  CASE
    WHEN order_time < '12:00:00' THEN 'Morning'
    WHEN order_time < '18:00:00' THEN 'Afternoon'
    ELSE 'Evening'
  END AS time_of_day
FROM orders;
```

**Explanation:** Ordered time comparisons bucket each hour into a label.

## Q49: Write a decision-table query that approves applications from multiple rules.

**Query:**
```sql
SELECT applicant_id, credit_score, income, existing_debt,
  CASE
    WHEN credit_score >= 700 AND income >= 50000 THEN 'Approved'
    WHEN credit_score >= 650 AND existing_debt < 20000 THEN 'Manual review'
    ELSE 'Denied'
  END AS decision
FROM applications;
```

**Explanation:** Policy reads best as ordered WHEN rules and the first match wins.

## Q50: Write a query to classify ledger amounts as debit, credit, or zero.

**Query:**
```sql
SELECT transaction_id, amount,
  CASE
    WHEN amount < 0 THEN 'credit'
    WHEN amount > 0 THEN 'debit'
    ELSE 'zero'
  END AS txn_type
FROM ledger;
```

**Explanation:** Three exhaustive comparisons cover every possible sign of the amount.

**Alt1:** SIGN() drives a simple CASE with three outcomes:

```sql
SELECT transaction_id,
  CASE SIGN(amount)
    WHEN 1  THEN 'debit'
    WHEN -1 THEN 'credit'
    ELSE 'zero'
  END AS txn_type
FROM ledger;
```

## Q51: Write a tier-and-price query that reuses a CASE via a subquery (no repetition).

**Query:**
```sql
SELECT order_id, amount, tier, rate,
  ROUND(amount * (1 - rate), 2) AS final_amount
FROM (
  SELECT order_id, amount,
    CASE WHEN amount >= 1000 THEN 'Platinum'
         WHEN amount >= 500  THEN 'Gold'
         ELSE 'Silver'
    END AS tier,
    CASE WHEN amount >= 1000 THEN 0.20
         WHEN amount >= 500  THEN 0.10
         ELSE 0.00
    END AS rate
  FROM orders
) t;
```

**Explanation:** The subquery computes tier and rate once; the outer query consumes both, avoiding repeated CASE blobs.

## Q52: Write a query applying eligibility rules with IN, IS NULL and a blacklist flag.

**Query:**
```sql
SELECT customer_id,
  CASE
    WHEN country_code IN ('US', 'CA') AND blacklist_flag = 0 THEN 'Eligible'
    WHEN country_code IS NULL THEN 'Data issue'
    ELSE 'Ineligible'
  END AS eligibility
FROM customers;
```

**Explanation:** Each WHEN encodes one policy and the IS NULL branch isolates bad data.

## Q53: Write a query summing refunds that occurred in the last 90 days.

**Query:**
```sql
SELECT product_id,
  SUM(
    CASE
      WHEN status = 'refunded' AND return_date >= CURRENT_DATE - 90
      THEN refund_amount ELSE 0
    END
  ) AS recent_refunds
FROM returns
GROUP BY product_id;
```

**Explanation:** The CASE filters rows inside the aggregate, summing only qualifying amounts.

## Q54: Write a query that compares December vs November sales using CASE in HAVING.

**Query:**
```sql
SELECT region
FROM sales
GROUP BY region
HAVING SUM(CASE WHEN month = 'Dec' THEN sales ELSE 0 END)
     > SUM(CASE WHEN month = 'Nov' THEN sales ELSE 0 END);
```

**Explanation:** Each conditional sum builds a per-group comparison without adding new columns.

## Q55: Write a KPI dashboard query with one row of totals using conditional aggregates.

**Query:**
```sql
SELECT
  COUNT(*) AS total_orders,
  SUM(CASE WHEN status = 'shipped' THEN 1 ELSE 0 END) AS shipped,
  SUM(CASE WHEN status IN ('cancelled', 'refunded') THEN 1 ELSE 0 END) AS lost
FROM orders;
```

**Explanation:** Aggregates with no GROUP BY collapse the table into a single summary row.

## Q56: Write an Oracle query pivoting quarterly sales using DECODE.

**Query:**
```sql
-- Oracle
SELECT 2019 AS year,
  SUM(DECODE(quarter, 1, sales, 0)) AS q1,
  SUM(DECODE(quarter, 2, sales, 0)) AS q2,
  SUM(DECODE(quarter, 3, sales, 0)) AS q3,
  SUM(DECODE(quarter, 4, sales, 0)) AS q4
FROM sales_q
WHERE year = 2019;
```

**Explanation:** DECODE inside SUM routes each row's sales into the matching quarter column.

**Alt1:** The CASE spelling keeps the pivot portable across engines:

```sql
SELECT
  SUM(CASE WHEN quarter = 1 THEN sales ELSE 0 END) AS q1,
  SUM(CASE WHEN quarter = 2 THEN sales ELSE 0 END) AS q2,
  SUM(CASE WHEN quarter = 3 THEN sales ELSE 0 END) AS q3,
  SUM(CASE WHEN quarter = 4 THEN sales ELSE 0 END) AS q4
FROM sales_q
WHERE year = 2019;
```

## Q57: Write a query sorting product types in the business's specified order using MySQL FIELD().

**Query:**
```sql
-- MySQL
SELECT product_type, COUNT(*) AS cnt
FROM listings
GROUP BY product_type
ORDER BY FIELD(product_type, 'flagship', 'featured', 'standard'), cnt DESC;
```

**Explanation:** FIELD returns the 1-based position of the value in the list; unnamed values get 0 and sort last.

**Alt1:** The portable CASE version:

```sql
SELECT product_type, COUNT(*) AS cnt
FROM listings
GROUP BY product_type
ORDER BY
  CASE product_type
    WHEN 'flagship' THEN 1
    WHEN 'featured' THEN 2
    WHEN 'standard' THEN 3
    ELSE 4
  END, cnt DESC;
```

## Q58: Write a warehouse reorder query using several business rules.

**Query:**
```sql
SELECT sku, stock, safety_stock, lead_time_days,
  CASE
    WHEN stock = 0 THEN 'EMERGENCY'
    WHEN stock < safety_stock AND lead_time_days > 7 THEN 'URGENT'
    WHEN stock < safety_stock THEN 'REORDER'
    ELSE 'OK'
  END AS action
FROM inventory;
```

**Explanation:** Rules are ordered most severe first; the first matching branch wins.

## Q59: Write a query that finds customers with 5+ large orders using a flag summed in HAVING.

**Query:**
```sql
SELECT customer_id, COUNT(*) AS total_orders,
  SUM(CASE WHEN amount > 500 THEN 1 ELSE 0 END) AS big_orders
FROM orders
GROUP BY customer_id
HAVING SUM(CASE WHEN amount > 500 THEN 1 ELSE 0 END) >= 5;
```

**Explanation:** The same conditional expression appears in SELECT and HAVING; HAVING filters the resulting groups.

## Q60: Write a query comparing the average age of active vs churned customers.

**Query:**
```sql
SELECT
  AVG(CASE WHEN status = 'active'  THEN age END) AS active_avg_age,
  AVG(CASE WHEN status = 'churned' THEN age END) AS churned_avg_age
FROM customers;
```

**Explanation:** AVG skips NULLs, so a CASE without an ELSE branch only feeds matching rows.

## Q61: Write a query that finds the max salary of 2019 hires per department.

**Query:**
```sql
SELECT department_id,
  MAX(CASE WHEN EXTRACT(YEAR FROM hire_date) = 2019 THEN salary END) AS best_2019_salary
FROM employees
GROUP BY department_id;
```

**Explanation:** Non-2019 rows become NULL inside the branch and are ignored by MAX.

## Q62: Write a query that buckets ZIP codes into regional labels using LIKE.

**Query:**
```sql
SELECT customer_name, postal_code,
  CASE
    WHEN postal_code LIKE '1%' OR postal_code LIKE '2%' THEN 'North'
    WHEN postal_code LIKE '9%' THEN 'West'
    ELSE 'Other'
  END AS region
FROM customers;
```

**Explanation:** Prefix matching on postal codes groups them into coarse regions.

## Q63: Write an insurance premium decision using several applicant columns.

**Query:**
```sql
SELECT policy_id, age, bmi, smoker,
  CASE
    WHEN age < 30 AND bmi < 25 AND smoker = 0 THEN 'Low'
    WHEN age >= 60 OR smoker = 1 THEN 'High'
    WHEN bmi >= 30 THEN 'Medium-high'
    ELSE 'Medium'
  END AS risk_class
FROM policies;
```

**Explanation:** Ordered WHENs encode the rating manual; narrow rules are checked before broad ones.

**Alt1:** Derive the class from a summed points score instead:

```sql
SELECT policy_id,
  CASE
    WHEN (CASE WHEN age < 30 THEN 0 ELSE 1 END) +
         (CASE WHEN bmi >= 30 THEN 2 ELSE 1 END) +
         (CASE WHEN smoker = 1 THEN 3 ELSE 0 END) >= 6 THEN 'High'
    ELSE 'Medium'
  END AS risk_class
FROM policies;
```

## Q64: Write a query that clamps interest rates into a min/max band.

**Query:**
```sql
SELECT loan_id, rate,
  CASE
    WHEN rate > 0.25 THEN 0.25
    WHEN rate < 0.05 THEN 0.05
    ELSE rate
  END AS capped_rate
FROM loans;
```

**Explanation:** Threshold clamping keeps every rate inside the allowed band.

**Alt1:** GREATEST/LEAST nest into one portable expression:

```sql
SELECT loan_id, LEAST(0.25, GREATEST(rate, 0.05)) AS capped_rate
FROM loans;
```

## Q65: Write a query that distinguishes NULL, zero, and positive price distinctly.

**Query:**
```sql
SELECT product_id, price,
  CASE
    WHEN price IS NULL THEN 'not published'
    WHEN price = 0 THEN 'free'
    WHEN price > 0 THEN 'paid'
  END AS price_band
FROM products;
```

**Explanation:** Three mutually exclusive branches cover IS NULL, zero, and positive values.

## Q66: Write a query that shows what happens when CASE branches mix data types.

**Query:**
```sql
SELECT employee_name,
  CASE WHEN employee_type = 'contractor' THEN 0 ELSE 'Salaried' END AS type_code
FROM employees;
```

**Explanation:** Types must be reconciled: MySQL coerces to string, SQL Server converts to the higher-precedence type, and PostgreSQL raises an error unless you CAST.

**Alt1:** Fix it portably by keeping every branch the same type:

```sql
SELECT employee_name,
  CASE WHEN employee_type = 'contractor' THEN '0' ELSE 'Salaried' END AS type_code
FROM employees;
```

## Q67: Write a SQL Server query showing that IIF handles only two outcomes and needs nesting for more.

**Query:**
```sql
-- SQL Server
SELECT student_name, score,
  IIF(score >= 90, 'A',
    IIF(score >= 80, 'B', IIF(score >= 70, 'C', 'F'))) AS grade
FROM grades;
```

**Explanation:** IIF is a two-way branch; deeper ladders require nesting, which hurts readability versus CASE.

## Q68: Write a MySQL query comparing IF() and CASE for a three-way outcome.

**Query:**
```sql
-- MySQL
SELECT id, qty,
  IF(qty > 100, 'plenty', IF(qty > 0, 'some', 'none')) AS stock_label_if,
  CASE
    WHEN qty > 100 THEN 'plenty'
    WHEN qty > 0   THEN 'some'
    ELSE 'none'
  END AS stock_label_case
FROM inventory;
```

**Explanation:** Both columns compute the same label, but CASE scales better than nested IF.

## Q69: Write PostgreSQL queries translating an IF-style need into CASE and FILTER.

**Query:**
```sql
-- PostgreSQL
SELECT
  COUNT(*) FILTER (WHERE is_vip) AS vip,
  COUNT(*) FILTER (WHERE NOT is_vip) AS regular
FROM customers;
```

**Explanation:** FILTER is PostgreSQL's native conditional-aggregate idiom.

**Alt1:** CASE produces the same counts portably:

```sql
SELECT
  SUM(CASE WHEN is_vip THEN 1 ELSE 0 END) AS vip,
  SUM(CASE WHEN NOT is_vip THEN 1 ELSE 0 END) AS regular
FROM customers;
```

## Q70: Write a query computing a safe conversion rate with NULLIF and COALESCE.

**Query:**
```sql
SELECT product_id, units_sold, views,
  COALESCE(100.0 * units_sold / NULLIF(views, 0), 0) AS conversion_rate
FROM analytics;
```

**Explanation:** NULLIF prevents the zero-division and COALESCE turns the resulting NULL into 0.

## Q71: Write a query mapping abbreviated department codes to full titles.

**Query:**
```sql
SELECT team_id,
  CASE department_code
    WHEN 'ACCT' THEN 'Accounting'
    WHEN 'OPS'  THEN 'Operations'
    WHEN 'IT'   THEN 'Information Technology'
    ELSE 'Unknown'
  END AS department
FROM teams;
```

**Explanation:** Simple CASE is the ideal tool for code-to-label dictionaries.

## Q72: Write a query that labels customers by age band computed from birth_date.

**Query:**
```sql
SELECT customer_name, birth_date,
  CASE
    WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM birth_date) < 18 THEN 'Minor'
    WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM birth_date) < 65 THEN 'Adult'
    ELSE 'Senior'
  END AS age_band
FROM customers;
```

**Explanation:** Age is derived from the date before the CASE buckets it.

## Q73: Write a deeply nested CASE for a three-level claim risk score.

**Query:**
```sql
SELECT claim_id, incident_severity, amount,
  CASE
    WHEN incident_severity = 'severe' THEN
      CASE
        WHEN amount > 100000 THEN 'High-risk'
        WHEN amount > 10000 THEN 'Review'
        ELSE 'Medium'
      END
    WHEN incident_severity = 'minor' THEN 'Low'
    ELSE 'Undefined'
  END AS claim_risk
FROM claims;
```

**Explanation:** The inner CASE refines only the outer 'severe' branch.

## Q74: Write a query grouping by a labeled bucket and ordering by a custom label order.

**Query:**
```sql
SELECT
  CASE
    WHEN total < 1000 THEN 'small'
    WHEN total < 10000 THEN 'medium'
    ELSE 'large'
  END AS segment,
  COUNT(*) AS accounts
FROM customers
GROUP BY 1
ORDER BY
  CASE segment
    WHEN 'small' THEN 1
    WHEN 'medium' THEN 2
    WHEN 'large' THEN 3
  END;
```

**Explanation:** GROUP BY 1 groups on the label, and ORDER BY CASE restores the business order afterwards.

## Q75: Write a query where the ELSE branch of a CASE supplies an aggregation fallback.

**Query:**
```sql
SELECT product_id,
  SUM(CASE WHEN status = 'sold' THEN quantity
           ELSE CEIL(quantity * 0.5) END) AS adjusted_qty
FROM stock_moves
GROUP BY product_id;
```

**Explanation:** Non-sold rows fall into the ELSE expression inside SUM, so they still contribute to the total.

## Q76: Write both a CASE-based mapping and a join-to-lookup-table mapping for statuses.

**Query:**
```sql
SELECT o.order_id,
  CASE o.status_code
    WHEN 'A' THEN 'Active'
    WHEN 'P' THEN 'Pending'
    ELSE 'Closed'
  END AS status_label
FROM orders o;
```

**Explanation:** CASE stays inline with zero joins — perfect when only a handful of codes exist.

**Alt1:** A label-dictionary table is cleaner and reusable:

```sql
SELECT o.order_id, s.status_label
FROM orders o
LEFT JOIN status_codes s ON o.status_code = s.code;
```

**Explanation:** With many codes the join wins on maintainability and can use indexes; CASE only beats it for tiny or per-row ad hoc mappings.

## Q77: Write a query computing on-time vs late delivery counts per courier.

**Query:**
```sql
SELECT courier_id,
  SUM(CASE WHEN delivered_at <= promised_date THEN 1 ELSE 0 END) AS on_time,
  SUM(CASE WHEN delivered_at >  promised_date THEN 1 ELSE 0 END) AS late
FROM shipments
GROUP BY courier_id;
```

**Explanation:** Two CASE flags divide every row into exactly one of the two outcomes.

## Q78: Write a query that filters groups in HAVING using a CASE you never select.

**Query:**
```sql
SELECT region
FROM sales
GROUP BY region
HAVING SUM(CASE WHEN quarter = 4 THEN revenue ELSE 0 END) >
       SUM(CASE WHEN quarter = 1 THEN revenue ELSE 0 END);
```

**Explanation:** HAVING may reference CASE aggregates that are absent from the SELECT list.

## Q79: Write a query filtering on a computed flag placed inside a subquery.

**Query:**
```sql
SELECT customer_id, big_order_count
FROM (
  SELECT customer_id,
    SUM(CASE WHEN amount >= 1000 THEN 1 ELSE 0 END) AS big_order_count
  FROM orders
  GROUP BY customer_id
) t
WHERE big_order_count >= 3;
```

**Explanation:** SELECT aliases are invisible in WHERE at the same level, so the flag is computed in a subquery first.

## Q80: Write a query handling negative quantities in an inventory report.

**Query:**
```sql
SELECT sku,
  SUM(CASE WHEN movement_type = 'in'  THEN qty ELSE 0 END) AS units_in,
  SUM(CASE WHEN movement_type = 'out' THEN -qty ELSE 0 END) AS units_out
FROM stock_movements
GROUP BY sku;
```

**Explanation:** 'out' movements flip sign inside CASE so the totals net out cleanly.

## Q81: Write a query with a multi-source fallback using CASE inside COALESCE.

**Query:**
```sql
SELECT employee_id,
  COALESCE(
    CASE WHEN manager_override IS NOT NULL THEN manager_override END,
    department_head_id,
    NULL) AS effective_manager
FROM employees;
```

**Explanation:** CASE narrows to a source only when populated; COALESCE then picks the first non-NULL source.

## Q82: Write a query that compares two price columns and labels the change.

**Query:**
```sql
SELECT product_id, price, msrp,
  CASE
    WHEN price = msrp THEN 'at list'
    WHEN price < msrp THEN 'discounted'
    ELSE 'above list'
  END AS price_position
FROM products;
```

**Explanation:** Peer-column comparison yields a business label without any aggregate.

## Q83: Write an Oracle query showing that DECODE treats NULL as equal to NULL (unlike simple CASE).

**Query:**
```sql
-- Oracle
SELECT employee_id,
  DECODE(manager_id, NULL, 'No manager', 'Has manager') AS mgr_status
FROM employees;
```

**Explanation:** DECODE uses NULL-safe equality, whereas Oracle simple CASE with `WHEN NULL` uses `=` semantics and would NOT match NULL — a classic trap.

## Q84: Write a query turning booleans into counts per region.

**Query:**
```sql
SELECT region,
  SUM(CASE WHEN opted_in THEN 1 ELSE 0 END) AS opted_in,
  SUM(CASE WHEN NOT opted_in THEN 1 ELSE 0 END) AS opted_out
FROM users
GROUP BY region;
```

**Explanation:** Each boolean row counts into exactly one of the two flag columns.

## Q85: Write a query that labels shipment lateness against a promised date.

**Query:**
```sql
SELECT shipment_id, promised_date, delivered_at,
  CASE
    WHEN delivered_at IS NULL THEN 'in transit'
    WHEN delivered_at <= promised_date THEN 'on time'
    ELSE 'late'
  END AS status
FROM shipments;
```

**Explanation:** Order matters: the unshipped check runs first, then the date comparisons.

## Q86: Write a query that sorts by a CASE key and then breaks ties with a second column.

**Query:**
```sql
SELECT product_id, discount_pct
FROM products
ORDER BY
  CASE WHEN discount_pct IS NULL THEN 1 ELSE 0 END,
  discount_pct DESC;
```

**Explanation:** The CASE key pushes NULL discounts to the end; discount_pct then orders the rest descending.

## Q87: Write a query computing free-shipping thresholds with CASE.

**Query:**
```sql
SELECT order_id, amount,
  CASE
    WHEN amount >= 75 THEN 0.00
    WHEN amount >= 50 THEN 4.99
    ELSE 9.99
  END AS shipping_fee
FROM orders;
```

**Explanation:** Descending thresholds set the fee; only the top tier ships free.

## Q88: Write an UPDATE that adjusts prices conditionally per row with CASE.

**Query:**
```sql
UPDATE products
SET price = CASE
    WHEN category = 'clearance' THEN price * 0.50
    WHEN category IN ('premium', 'luxury') THEN price * 1.10
    ELSE price
  END
WHERE discontinued = 0;
```

**Explanation:** CASE in SET computes a per-row value inside a single UPDATE.

**Alt1:** Drive the multiplier from a price-rules table with a join:

```sql
-- SQL Server / PostgreSQL
UPDATE p
SET price = p.price * pr.multiplier
FROM products p
JOIN price_rules pr ON p.category = pr.category;
```

## Q89: Write a query tagging customers who have any large order using EXISTS inside CASE.

**Query:**
```sql
SELECT c.customer_id,
  CASE WHEN EXISTS (
        SELECT 1 FROM orders o
        WHERE o.customer_id = c.customer_id AND o.amount > 2000)
       THEN 'premium' ELSE 'standard' END AS tier
FROM customers c;
```

**Explanation:** EXISTS yields the boolean that CASE maps into a label.

## Q90: Write a query that places out-of-stock SKUs first while keeping the rest sorted.

**Query:**
```sql
SELECT sku, stock
FROM inventory
ORDER BY
  CASE WHEN stock = 0 THEN 0 ELSE 1 END,
  sku;
```

**Explanation:** Zero-stock SKUs surface first; the remaining rows sort by SKU.

## Q91: Write a query computing a weighted points risk score from several CASE inputs.

**Query:**
```sql
SELECT applicant_id,
  CASE WHEN income < 30000 THEN 3 ELSE 0 END +
  CASE WHEN debt_ratio > 0.4 THEN 3 ELSE 0 END +
  CASE WHEN credit_score < 600 THEN 4 ELSE 0 END AS risk_points
FROM applications;
```

**Explanation:** Each CASE contributes 0 or points; summing the flags yields a score.

## Q92: Write a query that buckets overdue invoices into aging bands using DATEDIFF.

**Query:**
```sql
-- SQL Server
SELECT invoice_id, due_date,
  DATEDIFF(day, due_date, GETDATE()) AS days_overdue,
  CASE
    WHEN DATEDIFF(day, due_date, GETDATE()) > 90 THEN '> 90 days'
    WHEN DATEDIFF(day, due_date, GETDATE()) > 60 THEN '61-90 days'
    WHEN DATEDIFF(day, due_date, GETDATE()) > 30 THEN '31-60 days'
    ELSE '<= 30 days'
  END AS aging_bucket
FROM invoices
WHERE due_date < GETDATE();
```

**Explanation:** DATEDIFF feeds the dedicated function and the descending thresholds keep the ranges clean.

## Q93: Write a query summing status flags in one pass and compare ELSE 0 vs ELSE omitted.

**Query:**
```sql
SELECT
  SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS count_visible,
  SUM(CASE WHEN status = 'active' THEN 1 END)        AS count_null_missing
FROM users;
```

**Explanation:** For SUM both give the same total, but the ELSE-less pattern feeds NULL; for AVG or COUNT the two forms differ sharply.

## Q94: Write a query showing numeric coercion between integer and decimal CASE branches.

**Query:**
```sql
-- MySQL
SELECT order_id, amount,
  CASE
    WHEN amount >= 100 THEN amount * 1.0
    ELSE 0
  END AS mixed_precision
FROM orders;
```

**Explanation:** MySQL returns a decimal because the decimal branch wins promotion; other engines may upcast differently, so know your engine's coercion rules.

## Q95: Write a SQL Server query with a three-level nested IIF for order sizing.

**Query:**
```sql
-- SQL Server
SELECT sale_id, amount,
  IIF(amount > 900, 'large',
    IIF(amount > 400, 'medium', 'small')) AS size
FROM sales
WHERE amount > 0;
```

**Explanation:** Nested IIF simulates an ELSE ladder; CASE remains the clearer choice for chains.

## Q96: Write a MySQL query using ELT to pick a label by 1-based position.

**Query:**
```sql
-- MySQL
SELECT customer_id, tier_code,
  ELT(tier_code, 'Bronze', 'Silver', 'Gold', 'Platinum') AS tier_name
FROM customers;
```

**Explanation:** ELT returns the n-th string, so tier_code must be within 1..4; it maps numeric codes positionally rather than conditionally.

## Q97: Write a query computing a repeat-customer share with a boolean CASE, and note the ELSE-less AVG form.

**Query:**
```sql
-- PostgreSQL
SELECT
  AVG(CASE WHEN status = 'repeat' THEN 1 END) AS repeat_share,
  AVG(CASE WHEN status = 'repeat' THEN 1 ELSE 0 END) AS repeat_share_safe
FROM customers;
```

**Explanation:** Both give the same average, but with ELSE omitted non-matching rows become NULL; keep ELSE constants explicit when COUNT is involved.

**Alt1:** The portable percentage spelling:

```sql
SELECT
  100.0 * SUM(CASE WHEN status = 'repeat' THEN 1 ELSE 0 END) / COUNT(*) AS repeat_pct
FROM customers;
```

## Q98: Write a query returning a date from a CASE with a fallback date.

**Query:**
```sql
SELECT order_id,
  CASE
    WHEN delivered_at IS NOT NULL THEN delivered_at
    ELSE approved_at
  END AS effective_date
FROM orders
WHERE approved_at IS NOT NULL;
```

**Explanation:** All branches return dates, so no conversion issues arise.

## Q99: Write a decision-table CASE for ticket routing and note the performance consideration.

**Query:**
```sql
SELECT ticket_id, affected_users, severity,
  CASE
    WHEN severity = 'critical' AND affected_users > 1000 THEN 'S1 - P0'
    WHEN severity = 'critical' THEN 'S1 - P1'
    WHEN affected_users > 500 THEN 'S2'
    ELSE 'S3'
  END AS routing_priority
FROM incidents;
```

**Explanation:** The ordered WHENs are the decision table itself; CASE scales fine for few rules, but a lookup/rules join wins for thousands of rows of policy.

**Alt1:** The table-driven alternative keeps policy data out of the query:

```sql
SELECT i.ticket_id, r.priority
FROM incidents i
JOIN routing_rules r
  ON r.severity = i.severity
 AND r.max_users >= i.affected_users
 AND (r.min_users <= i.affected_users OR r.min_users IS NULL);
```

## Q100: Write a fully portable conditional-logic query that avoids dialect-specific functions.

**Query:**
```sql
SELECT order_id, amount, status_code,
  CASE
    WHEN status_code = 'X' THEN 0
    ELSE amount
  END AS gross_amount,
  COALESCE(NULLIF(discount_code, ''), 'none') AS effective_discount
FROM orders;
```

**Explanation:** Standard CASE/NULLIF/COALESCE runs unchanged on MySQL, PostgreSQL, SQL Server and Oracle — prefer it whenever code crosses dialects; IF/IIF/DECODE stay handy one-engine shorthands.

**Alt1:** The same status check as a MySQL IF for comparison:

```sql
-- MySQL
SELECT order_id,
  IF(status_code = 'X', 0, amount) AS gross_amount
FROM orders;
```
