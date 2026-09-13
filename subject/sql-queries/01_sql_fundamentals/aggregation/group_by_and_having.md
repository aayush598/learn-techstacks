# GROUP BY and HAVING — 100 SQL Interview Q&A

## Q1: Write a query to count the number of orders placed by each customer.
**Query:**
```sql
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id;
```
**Explanation:** `GROUP BY customer_id` collapses rows into one group per customer, and `COUNT(*)` returns the number of rows in each group.
**Alt1:** Count with an alias before grouping for readability:
```sql
SELECT customer_id AS cust, COUNT(*) AS order_count
FROM orders
GROUP BY cust;
```
**Explanation:** MySQL allows reusing the alias `cust` as the GROUP BY key — portable engines require `customer_id` spelled out again.


## Q2: Count the total units sold per product, summing the quantity column.
**Query:**
```sql
SELECT product_id, SUM(quantity) AS total_quantity
FROM order_items
GROUP BY product_id;
```
**Explanation:** Each group (one per `product_id`) is reduced by `SUM(quantity)`, producing the total sold per product.

## Q3: Write a query to compute the average product price per category.
**Query:**
```sql
SELECT category_id, AVG(price) AS avg_price
FROM products
GROUP BY category_id;
```
**Explanation:** `GROUP BY category_id` forms a group per category and `AVG(price)` ignores NULL prices, returning the mean price per category.

## Q4: Find the earliest order date and the latest order date for each customer.
**Query:**
```sql
SELECT customer_id,
       MIN(order_date) AS first_order_date,
       MAX(order_date) AS last_order_date
FROM orders
GROUP BY customer_id;
```
**Explanation:** `MIN(order_date)` and `MAX(order_date)` reduce each customer's group to its earliest and latest dates respectively.

## Q5: Count how many distinct products were purchased in each order.
**Query:**
```sql
SELECT order_id, COUNT(DISTINCT product_id) AS distinct_products
FROM order_items
GROUP BY order_id;
```
**Explanation:** `COUNT(DISTINCT product_id)` only counts unique product ids in each order group, so duplicate lines for one product aren't double-counted.

## Q6: Write a query that shows the total revenue per customer, and then explain why `customer_name` alone cannot appear in the SELECT list of a MySQL query that groups only by `customer_id` when `ONLY_FULL_GROUP_BY` is on.
**Query:**
```sql
SELECT customer_id, SUM(amount) AS total_revenue
FROM orders
GROUP BY customer_id;
```
**Explanation:** With `ONLY_FULL_GROUP_BY` on, any non-aggregated column must be functionally dependent on the grouped columns; `customer_name` is not dependent on `customer_id` alone (two ids could share a name), so it is rejected — either group by it too or wrap it in an aggregate such as `MAX(customer_name)` / `ANY_VALUE(customer_name)`.

## Q7: Use `SUM` to compute the total for each region, then add a `WHERE` clause that only includes rows from 2025.
**Query:**
```sql
SELECT region, SUM(revenue) AS total_revenue
FROM sales
WHERE sale_year = 2025
GROUP BY region;
```
**Explanation:** `WHERE` filters rows before grouping, so only 2025 sales contribute to each region's `SUM(revenue)`.

## Q8: Count orders per status, but only for customers in state 'CA'.
**Query:**
```sql
SELECT status, COUNT(*) AS order_count
FROM orders
WHERE customer_state = 'CA'
GROUP BY status;
```
**Explanation:** `WHERE customer_state = 'CA'` runs first, shrinking the rows that `GROUP BY status` then aggregates, so each count reflects only California orders.

## Q9: Show customers who have placed more than 5 orders, using HAVING on the aggregate count.
**Query:**
```sql
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 5;
```
**Explanation:** `HAVING` filters groups after aggregation, keeping only customer groups whose `COUNT(*)` is greater than 5.
**Alt1:** Same result via a derived-table wrapper (fully portable):
```sql
SELECT customer_id, order_count
FROM (SELECT customer_id, COUNT(*) AS order_count FROM orders GROUP BY customer_id) t
WHERE order_count > 5;
```
**Explanation:** Filtering the already-computed count outside the grouping gives identical output and sidesteps HAVING alias rules entirely.


## Q10: Find product categories whose average price exceeds 100 dollars.
**Query:**
```sql
SELECT category_id, AVG(price) AS avg_price
FROM products
GROUP BY category_id
HAVING AVG(price) > 100;
```
**Explanation:** `AVG(price)` is computed per group and `HAVING` keeps only categories whose mean price is above 100; `WHERE` can't do this because it runs before aggregation.

## Q11: List departments that have more than 30 employees.
**Query:**
```sql
SELECT department_id, COUNT(*) AS employee_count
FROM employees
GROUP BY department_id
HAVING COUNT(*) > 30;
```
**Explanation:** Each department is grouped, `COUNT(*)` tallies its employees, and `HAVING COUNT(*) > 30` keeps only the large departments.

## Q12: Show suppliers with total stock of their products greater than 500 units.
**Query:**
```sql
SELECT supplier_id, SUM(stock) AS total_stock
FROM products
GROUP BY supplier_id
HAVING SUM(stock) > 500;
```
**Explanation:** `SUM(stock)` aggregates each supplier's products, and `HAVING` filters out suppliers whose combined stock is 500 or less.

## Q13: Write a query to group sales by region and month, computing the total amount for each combination.
**Query:**
```sql
SELECT region, sale_month, SUM(amount) AS total_amount
FROM sales
GROUP BY region, sale_month;
```
**Explanation:** Grouping by two columns creates one group per (region, month) pair — subgrouping explained by the composite group key.

## Q14: Show the count of orders per year, using EXTRACT to group by year from a DATE column.
**Query:**
```sql
SELECT EXTRACT(YEAR FROM order_date) AS order_year, COUNT(*) AS order_count
FROM orders
GROUP BY EXTRACT(YEAR FROM order_date);
```
**Explanation:** The group key is an expression over the base column; each distinct year forms one group. A column alias can't be reused in the `GROUP BY` in most dialects, so the expression is repeated.

## Q15: Count orders grouped by month from a string column formatted 'YYYY-MM'.
**Query:**
```sql
SELECT SUBSTRING(order_month, 1, 7) AS month_key, COUNT(*) AS order_count
FROM orders
GROUP BY SUBSTRING(order_month, 1, 7);
```
**Explanation:** Grouping by a string expression produces one group per distinct 'YYYY-MM' prefix, effectively bucketing by month.

## Q16: Write a query using CASE to bucket employees into age bands ('Under 30', '30-39', '40-49', '50+') and count how many employees fall into each band.
**Query:**
```sql
SELECT CASE
           WHEN age < 30 THEN 'Under 30'
           WHEN age < 40 THEN '30-39'
           WHEN age < 50 THEN '40-49'
           ELSE '50+'
       END AS age_band,
       COUNT(*) AS employee_count
FROM employees
GROUP BY CASE
           WHEN age < 30 THEN 'Under 30'
           WHEN age < 40 THEN '30-39'
           WHEN age < 50 THEN '40-49'
           ELSE '50+'
         END;
```
**Explanation:** Both SELECT and GROUP BY repeat the same CASE expression so each computed bucket is exactly one group; MySQL also allows reusing the SELECT alias in `GROUP BY`.
**Alt1:** Define the band once in a derived table so SELECT and GROUP BY stay DRY:
```sql
SELECT age_band, COUNT(*) AS employee_count
FROM (SELECT CASE WHEN age < 30 THEN 'Under 30'
                  WHEN age < 40 THEN '30-39'
                  WHEN age < 50 THEN '40-49'
                  ELSE '50+' END AS age_band
      FROM employees) e
GROUP BY age_band;
```
**Explanation:** Comput-CASE in the inner SELECT and then GROUP BY its alias in the outer — portable everywhere and easier to maintain.


## Q17: Bucket orders into price bands ('Low', 'Medium', 'High') and sum the order values per band.
**Query:**
```sql
SELECT CASE
           WHEN total < 50 THEN 'Low'
           WHEN total < 200 THEN 'Medium'
           ELSE 'High'
       END AS price_band,
       SUM(total) AS band_total
FROM orders
GROUP BY price_band;  -- MySQL only: aliases are allowed in GROUP BY
```
**Explanation:** The CASE expression defines the bucket; the alias `price_band` is reusable inside `GROUP BY` in MySQL, while other dialects repeat the full expression or use an inline view/subquery.

## Q18: Use GROUP BY with the ROLLUP modifier to get sales totals per region and a grand total for all regions.
**Query:**
```sql
SELECT region, SUM(amount) AS total_amount
FROM sales
GROUP BY region WITH ROLLUP;  -- MySQL
```
**Explanation:** `WITH ROLLUP` adds a summary row where `region` is NULL holding the grand total; in PostgreSQL that's `GROUP BY ROLLUP (region)` and in SQL Server `GROUP BY ROLLUP (region)` as well.

## Q19: Produce monthly sales totals plus an overall total for the year using ROLLUP in PostgreSQL.
**Query:**
```sql
SELECT EXTRACT(MONTH FROM sale_date) AS m, EXTRACT(YEAR FROM sale_date) AS y,
       SUM(amount) AS total_amount
FROM sales
GROUP BY ROLLUP (EXTRACT(YEAR FROM sale_date), EXTRACT(MONTH FROM sale_date));
```
**Explanation:** `GROUP BY ROLLUP(a, b)` generates subtotal groups for `a`, `(a, b)`, and the grand total — one row with both NULL.

## Q20: Write a query using GROUPING SETS to produce totals both per region and per product in a single statement.
**Query:
```sql
SELECT region, product_id, SUM(amount) AS total_amount
FROM sales
GROUP BY GROUPING SETS ((region), (product_id));
```
**Explanation:** `GROUPING SETS` lists group keys explicitly, so one statement returns both regional totals (product_id NULL) and per-product totals (region NULL) without a UNION.

## Q21: Show the average sale amount per salesperson, only for those with at least 10 recorded sales.
**Query:**
```sql
SELECT salesperson_id, AVG(amount) AS avg_amount
FROM sales
GROUP BY salesperson_id
HAVING COUNT(*) >= 10;
```
**Explanation:** `HAVING COUNT(*) >= 10` filters on the group's row count after `AVG` groups, ensuring averages come from a meaningful sample size.

## Q22: Find stores where the total revenue exceeds 1,000,000 but the number of transactions is below 500.
**Query:**
```sql
SELECT store_id, SUM(revenue) AS total_revenue, COUNT(*) AS transaction_count
FROM transactions
GROUP BY store_id
HAVING SUM(revenue) > 1000000 AND COUNT(*) < 500;
```
**Explanation:** Multiple aggregate conditions can be combined in one `HAVING` with `AND`; both are evaluated per group after aggregation.
**Alt1:** Outer-query filtering with aliases instead of HAVING:
```sql
SELECT store_id, total_revenue, transaction_count
FROM (SELECT store_id, SUM(revenue) AS total_revenue, COUNT(*) AS transaction_count
      FROM transactions GROUP BY store_id) s
WHERE total_revenue > 1000000 AND transaction_count < 500;
```
**Explanation:** Equivalent thresholds, but the gate moves to WHERE over the derived table — handy when a dialect or style guide dislikes compound HAVING clauses.


## Q23: Write a query to list customers who have ordered in multiple distinct months.
**Query:**
```sql
SELECT customer_id
FROM orders
GROUP BY customer_id
HAVING COUNT(DISTINCT EXTRACT(MONTH FROM order_date)) > 1;
```
**Explanation:** `COUNT(DISTINCT ...)` counts unique months per customer group, and `HAVING` keeps only customers active in more than one month.

## Q24: Group orders by year and quarter, computing total amount and order count for each (year, quarter) pair.
**Query:**
```sql
SELECT EXTRACT(YEAR FROM order_date) AS yr,
       EXTRACT(QUARTER FROM order_date) AS qtr,
       SUM(amount) AS total_amount,
       COUNT(*) AS order_count
FROM orders
GROUP BY EXTRACT(YEAR FROM order_date), EXTRACT(QUARTER FROM order_date);
```
**Explanation:** Two expression-level group keys create subgroups per (year, quarter), and both aggregates are computed within each subgroup.

## Q25: Count orders per customer, ordering the result by the number of orders in descending order.
**Query:**
```sql
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
ORDER BY order_count DESC;
```
**Explanation:** `ORDER BY` runs after grouping, so the aggregate alias `order_count` can be used to sort the grouped results from most to fewest orders.
**Alt1:** Order by ordinal position instead of alias:
```sql
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
ORDER BY 2 DESC;
```
**Explanation:** `2` names the second SELECT column; equivalent to the alias form and useful in compact drill-downs.


## Q26: Show the total and average amount per region, and combine multiple aggregates of different types (COUNT, SUM, AVG, MIN, MAX) in one grouped query per customer.
**Query:**
```sql
SELECT customer_id,
       COUNT(*)                        AS order_count,
       SUM(amount)                     AS total_spent,
       AVG(amount)                     AS avg_spent,
       MIN(amount)                     AS smallest_order,
       MAX(amount)                     AS biggest_order
FROM orders
GROUP BY customer_id;
```
**Explanation:** A single `GROUP BY` can feed any number of aggregates — each one reduces the same groups independently.

## Q27: Explain why you cannot write `WHERE COUNT(*) > 1` and then write the correct query using HAVING instead.
**Query:**
```sql
-- Wrong: WHERE COUNT(*) > 1  -- aggregate in WHERE is invalid
SELECT customer_id, COUNT(*) AS cnt
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 1;
```
**Explanation:** `WHERE` filters raw rows before grouping exists, so aggregates aren't available there; `HAVING` filters after grouping, which is where aggregate conditions belong.

## Q28: Filter groups by a ratio threshold — show suppliers whose returned units are more than 10% of their shipped units.
**Query:**
```sql
SELECT supplier_id,
       SUM(shipped_units) AS shipped,
       SUM(returned_units) AS returned
FROM shipments
GROUP BY supplier_id
HAVING SUM(returned_units) * 1.0 / NULLIF(SUM(shipped_units), 0) > 0.10;
```
**Explanation:** The HAVING condition is an aggregate expression — a ratio of two `SUM`s — compared against 0.10; `NULLIF` guards against dividing by a zero-total group.

## Q29: List products where the average quantity per order line is less than 2 but the product has more than 5 lines.
**Query:**
```sql
SELECT product_id, AVG(quantity) AS avg_qty, COUNT(*) AS line_count
FROM order_items
GROUP BY product_id
HAVING AVG(quantity) < 2 AND COUNT(*) > 5;
```
**Explanation:** Two different aggregates (AVG and COUNT) can both restrict the same group with `AND` in one `HAVING`.

## Q30: Use MIN() on a date or string column to pick the earliest order date within each group, grouping by something else entirely.
**Query:**
```sql
SELECT customer_id, MIN(order_date) AS first_order
FROM orders
GROUP BY customer_id;
```
**Explanation:** Because `MIN()` aggregates every non-grouped column, you can attach descriptive values (like the earliest date) to each group without adding them to the group key.
**Alt1:** Attach the earliest date together with a companion aggregate in the same group:
```sql
SELECT customer_id, MIN(order_date) AS first_order, MAX(order_date) AS last_order
FROM orders
GROUP BY customer_id;
```
**Explanation:** Both endpoints come from the same rows' order_date column, so they are consistent — unlike pairing MAX(amount) with MIN(order_date), which can pull from different rows.


## Q31: Write a single query using GROUPING SETS to compute per-region, per-product, and total sums in one pass.
**Query:**
```sql
SELECT region, product_id, SUM(amount) AS total_amount
FROM sales
GROUP BY GROUPING SETS ((region), (product_id), ());
```
**Explanation:** The empty `()` set yields the grand total; combined with `(region)` and `(product_id)` this replaces three queries or a UNION — one statement, one scan phase.

## Q32: Show the maximum order amount per customer and also the date of that largest order using MAX and a bit of cleverness, explaining the limitation.
**Query:**
```sql
SELECT customer_id, MAX(order_date) AS recent_date, MAX(amount) AS max_amount
FROM orders
GROUP BY customer_id;
```
**Explanation:** `MAX(order_date)` and `MAX(amount)` come from possibly different rows — SQL doesn't guarantee they co-exist in one row; truly pairing amount-with-date needs a window function or join, a sibling topic.

## Q33: Count orders per region where the amount exceeds 100, and also count all orders per region in the same query using a conditional aggregate.
**Query:**
```sql
SELECT region,
       COUNT(*) AS all_orders,
       COUNT(CASE WHEN amount > 100 THEN 1 END) AS big_orders
FROM orders
GROUP BY region;
```
**Explanation:** `COUNT(CASE ... END)` counts only rows matching the condition (non-NULL results), letting you bucket-count within one group without a second pass.
**Alt1:** SUM over a 1/0 CASE flag instead of COUNT over a NULL-returning CASE:
```sql
SELECT region,
       COUNT(*) AS all_orders,
       SUM(CASE WHEN amount > 100 THEN 1 ELSE 0 END) AS big_orders
FROM orders
GROUP BY region;
```
**Explanation:** Both count the matching subset; the SUM-of-flag style is idiomatic in SQL Server and sometimes clearer with complex predicates.


## Q34: Find customers whose total spend is in the top range by comparing their SUM against an absolute threshold in HAVING, then comment on why relative top-N needs a different tool.
**Query:**
```sql
SELECT customer_id, SUM(amount) AS total_spent
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 10000;
```
**Explanation:** `HAVING` handles fixed thresholds; a "top 10 by rank" needs ordering over all groups (window functions/ORDER BY LIMIT) since no single group can know its global rank in a plain GROUP BY.

## Q35: Group by a boolean expression to compare average order value on discount days vs full-price days.
**Query:**
```sql
SELECT (is_discount_day = TRUE) AS discounted,
       AVG(amount) AS avg_amount,
       COUNT(*) AS order_count
FROM orders
GROUP BY (is_discount_day = TRUE);
```
**Explanation:** The group key is a boolean expression, so two groups (true, false) form; each shows its own average and count.

## Q36: Write a query to deduplicate a table by keeping one row per (email, first_name) pair using 'group by everything except one column'.
**Query:**
```sql
SELECT email, first_name, MAX(id) AS keep_id
FROM users
GROUP BY email, first_name;
```
**Explanation:** Grouping by the columns that define a duplicate leaves `id` outside the group key; aggregating it with `MAX(id)` yields a single representative id per group — the classic group-by-dedup shape.

## Q37: Show, per category, the number of products and the percentage of products priced above 50.
**Query:**
```sql
SELECT category_id,
       COUNT(*) AS total_products,
       COUNT(CASE WHEN price > 50 THEN 1 END) * 100.0 / COUNT(*) AS pct_above_50
FROM products
GROUP BY category_id;
```
**Explanation:** The ratio is computed entirely from aggregates defined in the same `GROUP BY`; `100.0` forces an integer-safe division into a percentage.
**Alt1:** Percent as AVG over a weighted CASE — no explicit division:
```sql
SELECT category_id, COUNT(*) AS total_products,
       AVG(CASE WHEN price > 50 THEN 100.0 ELSE 0 END) AS pct_above_50
FROM products
GROUP BY category_id;
```
**Explanation:** AVG of values set to 100/0 yields the percentage directly, condensing the ratio into one aggregate.


## Q38: Find regions where the highest single sale is at least 10 times the average sale of that region.
**Query:**
```sql
SELECT region, MAX(amount) AS max_sale, AVG(amount) AS avg_sale
FROM sales
GROUP BY region
HAVING MAX(amount) >= 10 * AVG(amount);
```
**Explanation:** `HAVING` can compare two aggregates from the same group (MAX vs AVG), flagging regions with an extreme outlier in one step.

## Q39: Group sales by custom bins defined by width — amounts in buckets of 0-99, 100-199, 200-299, etc. — and count each bucket.
**Query:**
```sql
SELECT FLOOR(amount / 100) * 100 AS lower_bound, COUNT(*) AS sales_in_bucket
FROM sales
GROUP BY FLOOR(amount / 100) * 100;
```
**Explanation:** `FLOOR(amount/100)*100` maps every amount to the start of its 100-wide bucket, and GROUP BY turns each distinct bucket boundary into one group.

## Q40: Count users per signup year who have a verified email, only where the count exceeds 50, using GROUP BY on an EXTRACT expression plus HAVING.
**Query:**
```sql
SELECT EXTRACT(YEAR FROM signup_date) AS signup_year, COUNT(*) AS verified_count
FROM users
WHERE email_verified = TRUE
GROUP BY EXTRACT(YEAR FROM signup_date)
HAVING COUNT(*) > 50;
```
**Explanation:** WHERE drops unverified users before grouping; EXTRACT forms year groups; HAVING keeps only years with more than 50 verified signups.

## Q41: Write a query that groups by two columns and filters by the combined count — pairs of (region, product) appearing in more than 3 orders.
**Query:**
```sql
SELECT region, product_id, COUNT(*) AS freq
FROM orders
GROUP BY region, product_id
HAVING COUNT(*) > 3;
```
**Explanation:** The group key is the composite (region, product); the COUNT aggregates whole pairs, and HAVING filters which pairs survive as "frequent combos".

## Q42: Show the total amount grouped by year, but with NULL and zero-sum rows handled explicitly using COALESCE in the SELECT.
**Query:**
```sql
SELECT EXTRACT(YEAR FROM sale_date) AS yr,
       COALESCE(SUM(amount), 0) AS total_amount
FROM sales
GROUP BY EXTRACT(YEAR FROM sale_date);
```
**Explanation:** `SUM` returns NULL only when a group contains no rows (impossible here) or all values are NULL; `COALESCE` turns that into `0` for display. NULLs inside values are ignored by SUM.

## Q43: Compute the average donation per donor, ignoring NULL donation values, and explain what AVG does with NULLs.
**Query:**
```sql
SELECT donor_id, AVG(donation_amount) AS avg_donation
FROM donations
GROUP BY donor_id;
```
**Explanation:** `AVG(col)` ignores NULLs entirely — it sums non-NULL values and divides by their count, not by the row count — so NULL donations neither drag down nor inflate the mean.

## Q44: Count rows versus count distinct values to prove a difference — total lines vs distinct products per order.
**Query:**
```sql
SELECT order_id,
       COUNT(*) AS total_lines,
       COUNT(product_id) AS non_null_lines,
       COUNT(DISTINCT product_id) AS distinct_products
FROM order_items
GROUP BY order_id;
```
**Explanation:** `COUNT(*)` counts rows, `COUNT(product)` ignores NULL product ids, and `COUNT(DISTINCT product)` counts unique values — the three COUNT variants compared side by side per group.

## Q45: Use GROUP BY with CUBE in PostgreSQL to get totals across all combinations of region and product.
**Query:**
```sql
SELECT region, product_id, SUM(amount) AS total_amount
FROM sales
GROUP BY CUBE (region, product_id);
```
**Explanation:** `CUBE` expands to every subset of the listed keys: region totals, product totals, pairs, and the grand total — more than ROLLUP, which only walks one direction.

## Q46: Show the count of employees per manager, but only managers supervising between 5 and 15 people (inclusive).
**Query:**
```sql
SELECT manager_id, COUNT(*) AS team_size
FROM employees
WHERE manager_id IS NOT NULL
GROUP BY manager_id
HAVING COUNT(*) BETWEEN 5 AND 15;
```
**Explanation:** WHERE removes rows with no manager before grouping; `BETWEEN 5 AND 15` filters group sizes afterward — the inclusive range HAVING.

## Q47: Group orders by weekday or day-of-week to find which weekdays have above-average order counts.
**Query:**
```sql
SELECT DAYOFWEEK(order_date) AS dow, COUNT(*) AS order_count
FROM orders
GROUP BY DAYOFWEEK(order_date)
HAVING COUNT(*) > (SELECT AVG(cnt) FROM (SELECT COUNT(*) AS cnt FROM orders GROUP BY DAYOFWEEK(order_date)) t);
```
**Explanation:** The HAVING condition compares each weekday's count against a scalar subquery that computes the average count across all weekday groups — aggregates inside aggregates via a subquery.

## Q48: Write the same grouped query for both MySQL and PostgreSQL where the group key is a date truncated to the day.
**Query:**
```sql
-- MySQL
SELECT DATE(order_date) AS day, SUM(amount) AS total FROM orders GROUP BY DATE(order_date);

-- PostgreSQL
SELECT order_date::date AS day, SUM(amount) AS total FROM orders GROUP BY order_date::date;
```
**Explanation:** Timestamps collapse into date groups with `DATE()` (MySQL) or `::date` cast (PostgreSQL); both compute one total per calendar day.

## Q49: Filter grouped results by SUM with a signed column — show teams with a positive net balance, using HAVING on SUM of a column that can be negative.
**Query:**
```sql
SELECT team_id, SUM(balance_delta) AS net_balance
FROM ledger
GROUP BY team_id
HAVING SUM(balance_delta) > 0;
```
**Explanation:** `SUM` naturally handles negative values, and HAVING keeps only groups whose net balance comes out positive.

## Q50: Write a query that groups by two levels and counts subgroups in a single pass — number of products per (category, subcategory) pair.
**Query:**
```sql
SELECT category_id, subcategory_id, COUNT(*) AS products_in_subcategory
FROM products
GROUP BY category_id, subcategory_id;
```
**Explanation:** The composite group key produces one group per (category, subcategory), so `COUNT(*)` tallies the subcategory size while higher-level category totals remain available from a second, coarser `GROUP BY category_id` query.

## Q51: Group transactions by type and month, then order by type and month to get a tidy summary.
**Query:**
```sql
SELECT tx_type, EXTRACT(MONTH FROM tx_date) AS m, SUM(amount) AS total
FROM transactions
GROUP BY tx_type, EXTRACT(MONTH FROM tx_date)
ORDER BY tx_type, m;
```
**Explanation:** ORDER BY applies after grouping, so grouped rows can be sorted by the group keys and/or aggregate aliases computed in the SELECT.

**Alt1:** Order with an ASC default on the second key omitted, same rows:
```sql
SELECT tx_type, EXTRACT(MONTH FROM tx_date) AS m, SUM(amount) AS total
FROM transactions
GROUP BY tx_type, EXTRACT(MONTH FROM tx_date)
ORDER BY 1, 2;
```
**Explanation:** Ordinal positions 1 and 2 reference the first two SELECT columns, handy for concise sorts.

## Q52: Find each customer's first-ever order id using MIN on a grouping trick, given rows have no order_date (only an incrementing id).
**Query:**
```sql
SELECT customer_id, MIN(order_id) AS first_order_id
FROM orders
GROUP BY customer_id;
```
**Explanation:** Because order ids are assigned in chronological sequence, the minimum id per customer group is the earliest order — MIN over a surrogate key substitutes for a date.

## Q53: Count orders per day only for the last 30 days, grouped by date, using a WHERE date filter plus GROUP BY.
**Query:**
```sql
SELECT order_date, COUNT(*) AS order_count
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY order_date;
```
**Explanation:** WHERE filters to the rolling window before grouping; each distinct date becomes a group and is counted. (Use `DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)` in MySQL.)

## Q54: Produce per-region subtotals AND per-region-per-year subtotals plus a grand total using ROLLUP in SQL Server, then say which modifier SQL Server uses.
**Query:**
```sql
SELECT region, sale_year, SUM(amount) AS total_amount
FROM sales
GROUP BY ROLLUP (sale_year, region);
```
**Explanation:** SQL Server accepts the `GROUP BY ROLLUP (...)` syntax; it emits subtotals for each prefix of the listed columns plus a grand-total row.

**Alt1:** Same output via GROUPING SETS (works in SQL Server, PostgreSQL, MySQL 8.0):
```sql
SELECT region, sale_year, SUM(amount) AS total_amount
FROM sales
GROUP BY GROUPING SETS ((sale_year, region), (sale_year), ());
```
**Explanation:** The empty set is the grand total, `(sale_year)` is the yearly subtotal, and `(sale_year, region)` is the per-region-per-year detail — ROLLUP is just a shorthand for the prefix sets.

## Q55: Write a query using GROUPING() to label ROLLUP subtotal rows as 'TOTAL' in a clean way.
**Query:**
```sql
SELECT CASE WHEN GROUPING(region) = 1 THEN 'ALL REGIONS' ELSE region END AS region,
       SUM(amount) AS total_amount
FROM sales
GROUP BY ROLLUP (region);
```
**Explanation:** `GROUPING(region)` returns 1 on the rollup summary row, so the CASE substitutes a label instead of showing NULL for the grouped-out dimension.

## Q56: Show the total sales per representative, but restrict the HAVING condition to representatives whose SUM is over 5000 AND who had at least one sale above 1000.
**Query:**
```sql
SELECT rep_id, SUM(amount) AS total_sales
FROM sales
GROUP BY rep_id
HAVING SUM(amount) > 5000 AND MAX(amount) > 1000;
```
**Explanation:** The two conditions combine per-group aggregates — total must exceed 5000 and the group's largest single sale must exceed 1000.

## Q57: Group employees by department, and within the same query show the count of each gender per department as separate aggregated columns.
**Query:**
```sql
SELECT department_id,
       COUNT(*) AS total,
       COUNT(CASE WHEN gender = 'F' THEN 1 END) AS females,
       COUNT(CASE WHEN gender = 'M' THEN 1 END) AS males
FROM employees
GROUP BY department_id;
```
**Explanation:** Conditional aggregates turn one group per department into a mini crosstab: three COUNTs, each zeroing non-matching rows with NULL.

## Q58: Write the same query in Oracle, where DUAL-style grouped queries differ, and add a GROUP BY on an expression with ROUND.
**Query:**
```sql
SELECT ROUND(price, -1) AS price_bucket, COUNT(*) AS cnt
FROM products
GROUP BY ROUND(price, -1);
```
**Explanation:** `ROUND(price, -1)` rounds to the nearest ten, creating de facto price buckets; Oracle requires the exact expression be repeated in GROUP BY.

## Q59: Show average quantity per order per product via grouping by both order and product, then order by the average descending.
**Query:**
```sql
SELECT order_id, product_id, AVG(quantity) AS avg_quantity
FROM order_items
GROUP BY order_id, product_id
ORDER BY avg_quantity DESC;
```
**Explanation:** The composite key makes each (order, product) pair one group; sorting by the AVG alias surfaces the densest line items first.

## Q60: Use HAVING with a string aggregate to find groups whose alphabetically first product name starts with 'A'.
**Query:**
```sql
SELECT category_id
FROM products
GROUP BY category_id
HAVING MIN(product_name) LIKE 'A%';
```
**Explanation:** `MIN()` over strings returns the alphabetically smallest name in the group; the HAVING condition tests that value, letting a string aggregate act as a per-group filter.

## Q61: Find the average order value per customer, showing only customers whose name also appears eligible via a non-aggregated predicate in HAVING combined with aggregate ones.
**Query:**
```sql
SELECT customer_id, AVG(amount) AS avg_order
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 3 AND MIN(order_date) > '2025-01-01';
```
**Explanation:** HAVING mixes aggregate conditions only — plain column predicates belong in WHERE that runs before grouping, while `MIN(order_date)` is a legitimate per-group aggregate.
**Alt1:** Move the date predicate into WHERE and keep HAVING purely aggregate:
```sql
SELECT customer_id, AVG(amount) AS avg_order
FROM orders
WHERE order_date > '2025-01-01'
GROUP BY customer_id
HAVING COUNT(*) > 3;
```
**Explanation:** Contrast: WHERE removes old rows first so COUNT(*) counts only new ones, whereas the main answer's MIN(order_date) gate keeps all rows and checks the earliest date — distinct semantics, choose by intent.


## Q62: Write a query that returns one row per customer per year (a 2-column group) with the year being the biggest spender, without using window functions.
**Query:**
```sql
SELECT customer_id, EXTRACT(YEAR FROM order_date) AS yr, SUM(amount) AS yearly_spend
FROM orders
GROUP BY customer_id, EXTRACT(YEAR FROM order_date);
```
**Explanation:** Grouping by customer and year jointly yields a time series row per pair; identifying the single biggest year per customer is a top-per-group problem that normally needs a window function, outside this file's scope.

## Q63: Count products per brand where stock and price conditions are applied in the right clauses, and explain which clause does what.
**Query:**
```sql
SELECT brand_id, COUNT(*) AS live_products
FROM products
WHERE stock > 0 AND price > 10        -- WHERE: prune rows pre-group
GROUP BY brand_id
HAVING COUNT(*) >= 3;                  -- HAVING: prune groups post-group
```
**Explanation:** WHERE rejects unqualified products before grouping, so counts reflect only live products; HAVING then drops brands with fewer than three qualifying products.

## Q64: Group leads by source and stage, and count how many leads fall into each funnel stage per source.
**Query:**
```sql
SELECT source, stage, COUNT(*) AS lead_count
FROM leads
GROUP BY source, stage;
```
**Explanation:** Two group keys cross-tab every source-stage combination; sources missing a stage get no row (the group simply doesn't exist).
**Alt1:** Pivot stages into columns per source using conditional counts:
```sql
SELECT source,
       COUNT(CASE WHEN stage = 'new' THEN 1 END) AS new_leads,
       COUNT(CASE WHEN stage = 'contacted' THEN 1 END) AS contacted_leads,
       COUNT(CASE WHEN stage = 'won' THEN 1 END) AS won_leads
FROM leads
GROUP BY source;
```
**Explanation:** The crosstab variant returns one row per source with columns per stage instead of one row per (source, stage) — same data, easier for side-by-side comparison.


## Q65: Compute the total revenue and the max single order per region, ordering by total revenue, and note why you can't reference a HAVING alias in WHERE.
**Query:**
```sql
SELECT region, SUM(revenue) AS total_revenue, MAX(revenue) AS max_order
FROM orders
GROUP BY region
ORDER BY total_revenue DESC;
```
**Explanation:** `ORDER BY` may use aliases, but WHERE runs before aliases exist — hence aggregates live in HAVING/ORDER BY only.

## Q66: Filter grouped results by multiple independent aggregate conditions using OR — regions that have either many orders OR huge total revenue.
**Query:**
```sql
SELECT region
FROM orders
GROUP BY region
HAVING COUNT(*) > 1000 OR SUM(amount) > 500000;
```
**Explanation:** OR inside HAVING keeps a group if either aggregate threshold is met, so high-frequency and high-value regions both qualify.
**Alt1:** Contrast the AND form, which requires both thresholds:
```sql
SELECT region
FROM orders
GROUP BY region
HAVING COUNT(*) > 1000 AND SUM(amount) > 500000;
```
**Explanation:** Flipping OR to AND narrows acceptance to heavy-volume AND heavy-value regions — the pairing shows how a one-word HAVING change reshapes results.


## Q67: Write a dedup-style query that keeps the most recently updated row per entity by group-by-everything-else with MAX.
**Query:**
```sql
SELECT entity_id, MAX(updated_at) AS latest_update
FROM entities
GROUP BY entity_id;
```
**Explanation:** Grouping by the identity column and applying MAX over the timestamp yields the newest value per entity — analogous to taking the top row without ranking.

## Q68: Group student grades by letter grade using a CASE mapping, and report count and percentage per grade using a subquery-free aggregate ratio.
**Query:**
```sql
SELECT CASE WHEN score >= 90 THEN 'A' WHEN score >= 80 THEN 'B'
            WHEN score >= 70 THEN 'C' ELSE 'F' END AS grade,
       COUNT(*) AS students,
       COUNT(*) * 100.0 / (SELECT COUNT(*) FROM grades) AS pct
FROM grades
GROUP BY CASE WHEN score >= 90 THEN 'A' WHEN score >= 80 THEN 'B'
            WHEN score >= 70 THEN 'C' ELSE 'F' END;
```
**Explanation:** The CASE defines grade buckets in both SELECT and GROUP BY, and the percentage divides each group's count by a scalar subquery total across all groups.

## Q69: Write an Oracle query grouping by TRUNC(hire_date, 'MM') to count hires per calendar month.
**Query:**
```sql
SELECT TRUNC(hire_date, 'MM') AS hire_month, COUNT(*) AS hires
FROM employees
GROUP BY TRUNC(hire_date, 'MM');
```
**Explanation:** `TRUNC(date,'MM')` truncates to day one of the month, so every date in the same month lands in one group; the expression must be repeated in GROUP BY.

## Q70: Show total time spent per user per project by SUM of duration minutes, filtering to projects exceeding 1000 minutes in HAVING.
**Query:**
```sql
SELECT user_id, project_id, SUM(duration_minutes) AS total_minutes
FROM time_entries
GROUP BY user_id, project_id
HAVING SUM(duration_minutes) > 1000;
```
**Explanation:** Composite grouping aggregates each user-project pair, and HAVING keeps only those over the 1000-minute threshold.

## Q71: Group sessions by device type and count average session length, then remove devices with NULL in the aggregated length from the final result using HAVING.
**Query:**
```sql
SELECT device_type, AVG(session_seconds) AS avg_length
FROM sessions
GROUP BY device_type
HAVING AVG(session_seconds) IS NOT NULL;
```
**Explanation:** `AVG` returns NULL only for groups with no non-NULL lengths; this HAVING drops exactly those degenerate groups from the result.

## Q72: Compare COUNT(*) versus COUNT(col) on a column with many NULLs and pick which better answers "how many fully completed forms per region".
**Query:**
```sql
SELECT region,
       COUNT(*)                    AS submitted,
       COUNT(completion_date)      AS completed,
       COUNT(*) - COUNT(completion_date) AS incomplete
FROM forms
GROUP BY region;
```
**Explanation:** `COUNT(completion_date)` skips rows where completion_date is NULL, revealing completed forms per region and letting arithmetic expose the incomplete count.

## Q73: Write a query grouping rows by a fixed number of groups using a modulo expression, e.g. partition ids into 4 buckets and count rows per bucket.
**Query:**
```sql
SELECT id % 4 AS bucket, COUNT(*) AS items
FROM records
GROUP BY id % 4;
```
**Explanation:** `id % 4` yields residues 0-3, forming exactly four groups; GROUP BY on the expression distributes rows evenly across buckets for sampling or sharding analysis.

## Q74: Find categories whose product count is 1-4 or 10+ (non-contiguous HAVING with logical nesting), and rank them by count.
**Query:**
```sql
SELECT category_id, COUNT(*) AS product_count
FROM products
GROUP BY category_id
HAVING COUNT(*) BETWEEN 1 AND 4 OR COUNT(*) >= 10
ORDER BY product_count DESC;
```
**Explanation:** Parenthesized OR conditions in HAVING express non-contiguous ranges on group sizes, and ORDER BY uses the count alias to sort.
**Alt1:** Explicit parentheses for the OR'd ranges:
```sql
SELECT category_id, COUNT(*) AS product_count
FROM products
GROUP BY category_id
HAVING (COUNT(*) BETWEEN 1 AND 4) OR (COUNT(*) >= 10)
ORDER BY product_count DESC;
```
**Explanation:** Parenthesizing each range keeps operator precedence obvious — no functional difference, only readability.


## Q75: Use GROUPING SETS in PostgreSQL to summarize sales by year and by quarter in one query, but avoid double-counting the quarterly rows.
**Query:**
```sql
SELECT EXTRACT(YEAR FROM sale_date) AS yr, EXTRACT(QUARTER FROM sale_date) AS qtr,
       SUM(amount) AS total
FROM sales
GROUP BY GROUPING SETS (
    (EXTRACT(YEAR FROM sale_date)),
    (EXTRACT(YEAR FROM sale_date), EXTRACT(QUARTER FROM sale_date))
);
```
**Explanation:** Because each set lists its own full key — quarter rows carry year too — and the plain-year set is separate, no row is aggregated twice; GROUPING SETS unions disjoint groupings.

## Q76: Write the canonical "count occurrences then keep the frequent ones" query for log events per hour.
**Query:**
```sql
SELECT HOUR(event_ts) AS event_hour, COUNT(*) AS event_count
FROM event_log
GROUP BY HOUR(event_ts)
HAVING event_count > 500;  -- alias reuse needs HAVING-era dialect support
```
**Explanation:** MySQL and many engines let aliases appear in HAVING; portable SQL repeats `COUNT(*) > 500` since HAVING is evaluated after the SELECT list is formed.

**Alt1:** Portable form repeating the aggregate:
```sql
SELECT HOUR(event_ts) AS event_hour, COUNT(*) AS event_count
FROM event_log
GROUP BY HOUR(event_ts)
HAVING COUNT(*) > 500;
```
**Explanation:** Works identically in MySQL, PostgreSQL, SQL Server, and Oracle — a safe default when portability matters.

## Q77: Group by a CASE that returns a label and a number at once? No — separate the dimension into two groups: band label and country.
**Query:**
```sql
SELECT country, CASE WHEN amount > 100 THEN 'high' ELSE 'low' END AS band,
       COUNT(*) AS order_count
FROM orders
GROUP BY country, CASE WHEN amount > 100 THEN 'high' ELSE 'low' END;
```
**Explanation:** Two independent group keys can live in one GROUP BY — one categorical (country) and one computed (band) — giving a simple 2D contingency table.

## Q78: Compute sum of positive amounts and sum of negative amounts separately per account, grouped by account.
**Query:**
```sql
SELECT account_id,
       SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS credits,
       SUM(CASE WHEN amount < 0 THEN -amount ELSE 0 END) AS debits
FROM account_moves
GROUP BY account_id;
```
**Explanation:** Conditional SUM lets two aggregates run over the same group from disjoint row subsets, splitting credits from debits in one pass.

## Q79: Show, per region, the count of orders and the average number of distinct products per order, using a nested aggregate, and explain the result semantics.
**Query:**
```sql
SELECT region,
       COUNT(DISTINCT order_id) AS orders,
       AVG(distinct_products) AS avg_distinct_products
FROM (SELECT region, order_id, COUNT(DISTINCT product_id) AS distinct_products
      FROM order_items
      GROUP BY region, order_id) t
GROUP BY region;
```
**Explanation:** The inner query counts distinct products per order (grouped by region+order), and the outer query averages those counts per region — grouping at two levels stacked through a subquery.

## Q80: Write a query that answers "which months since launch had no sales" and prove HAVING alone can't produce missing groups, suggesting a workaround.
**Query:**
```sql
SELECT EXTRACT(MONTH FROM sale_date) AS m, COUNT(*) AS cnt
FROM sales
GROUP BY EXTRACT(MONTH FROM sale_date);
```
**Explanation:** GROUP BY only emits groups that exist in the data; empty months simply vanish. Filling gaps requires a calendar table or generate_series cross join — a UNION-driven shape, not a HAVING trick.

## Q81: Group logins per user over a trailing window using GROUP BY on the bucket derived from an expression, and filter by HAVING on the count.
**Query:**
```sql
SELECT user_id,
       FLOOR(UNIX_TIMESTAMP(login_ts) / 86400) AS day_bucket,
       COUNT(*) AS logins
FROM logins
WHERE login_ts >= NOW() - INTERVAL 30 DAY
GROUP BY user_id, FLOOR(UNIX_TIMESTAMP(login_ts) / 86400)
HAVING COUNT(*) >= 5;
```
**Explanation:** Dividing epoch seconds by seconds-per-day collapses timestamps into day buckets (MySQL flavor), and HAVING isolates power users logging in at least 5 times that day.
**Alt1:** PostgreSQL flavor with date arithmetic for the same day buckets:
```sql
SELECT user_id,
       (login_ts AT TIME ZONE 'UTC')::date AS day_bucket,
       COUNT(*) AS logins
FROM logins
WHERE login_ts >= now() - interval '30 days'
GROUP BY user_id, (login_ts AT TIME ZONE 'UTC')::date
HAVING COUNT(*) >= 5;
```
**Explanation:** Casting a timestamp to date truncates it to the day boundary; the HAVING threshold is unchanged across dialects.


## Q82: Write the ROLLUP query in MySQL that produces per-year and grand totals, then locate the total row via GROUPING().
**Query:**
```sql
SELECT YEAR(sale_date) AS yr,
       SUM(amount) AS total,
       GROUPING(YEAR(sale_date)) AS is_total
FROM sales
GROUP BY YEAR(sale_date) WITH ROLLUP;
```
**Explanation:** `WITH ROLLUP` adds a grand-total row where `YEAR(sale_date)` is NULL and `GROUPING()` returns 1, so consumers can programmatically isolate the total.

## Q83: Show total spend per customer only for customers whose last order was after a cutoff, combining MIN/MAX-of-subgroup logic with HAVING.
**Query:**
```sql
SELECT customer_id, SUM(amount) AS total_spend
FROM orders
GROUP BY customer_id
HAVING MAX(order_date) > '2025-06-01';
```
**Explanation:** `MAX(order_date)` per group is the customer's latest order; the HAVING keeps only shoppers active after the cutoff while SUM reports their lifetime spend.

## Q84: Deduplicate a table keeping the earliest row per (user, type) pair by grouping on the pair and taking MIN of the tie-breaking id.
**Query:**
```sql
SELECT user_id, event_type, MIN(event_id) AS keep_row
FROM events
GROUP BY user_id, event_type;
```
**Explanation:** The duplicate key (user, type) is the full group key, and the monotonically increasing event_id is aggregated with MIN to retain exactly one canonical row.
**Alt1:** Latest-wins variant by swapping MIN for MAX:
```sql
SELECT user_id, event_type, MAX(event_id) AS keep_row
FROM events
GROUP BY user_id, event_type;
```
**Explanation:** One aggregate swap flips earliest-wins into latest-wins dedup without touching the group key.


## Q85: Bucket salaries into hand-written ranges with CASE, and compute average salary plus headcount per band, for bands that hold at least 2 people (HAVING on the band count).
**Query:**
```sql
SELECT CASE WHEN salary < 50000 THEN '48k'
            WHEN salary < 80000 THEN '50-79k'
            ELSE '80k+' END AS band,
       COUNT(*) AS headcount,
       AVG(salary) AS avg_salary
FROM employees
GROUP BY CASE WHEN salary < 50000 THEN '48k'
            WHEN salary < 80000 THEN '50-79k'
            ELSE '80k+' END
HAVING COUNT(*) >= 2;
```
**Explanation:** The CASE expression creates the buckets, AVG summarizes the group, and HAVING drops single-person bands for anonymity — a common reporting constraint.

## Q86: Write a query that applies WHERE and HAVING together where both reference the same column but semantically differ, and explain the difference with an example.
**Query:**
```sql
SELECT category, SUM(amount) AS total
FROM orders
WHERE amount > 50                 -- rows under 50 dropped before grouping
GROUP BY category
HAVING SUM(amount) > 500;         -- groups whose surviving total is small dropped after
```
**Explanation:** WHERE permanently removes cheap rows, then totals are computed from survivors; HAVING filters whole groups next — same column, two different points in the pipeline.

## Q87: Find, per month, the count of first-time customers by grouping on month of first order, then HAVING to keep only growing months.
**Query:**
```sql
SELECT EXTRACT(MONTH FROM first_order_date) AS m, COUNT(*) AS new_customers
FROM customers
GROUP BY EXTRACT(MONTH FROM first_order_date)
HAVING COUNT(*) >= (SELECT AVG(cnt) FROM (SELECT COUNT(*) AS cnt FROM customers GROUP BY EXTRACT(MONTH FROM first_order_date)) x);
```
**Explanation:** Each month's new-customer count is compared inside HAVING to the scalar subquery average of all months — months meeting or beating the average survive.

## Q88: Write a GROUPING SETS query producing per-status, per-priority, and per-(status, priority) workload sums from a ticket table.
**Query:**
```sql
SELECT status, priority, SUM(tickets) AS open_tickets
FROM ticket_counts
GROUP BY GROUPING SETS ((status), (priority), (status, priority));
```
**Explanation:** Each set is its own summary — singles give marginal totals, the pair gives the joint detail; NULL flags which dimension was rolled up in each row.

## Q89: Aggregate revenue by quarter using DATE_TRUNC in PostgreSQL, and filter quarters below a threshold with HAVING.
**Query:**
```sql
SELECT DATE_TRUNC('quarter', sale_date) AS qtr_start,
       SUM(revenue) AS quarterly_revenue
FROM sales
GROUP BY DATE_TRUNC('quarter', sale_date)
HAVING SUM(revenue) > 250000;
```
**Explanation:** `DATE_TRUNC('quarter', ...)` groups every timestamp into its quarter boundary; HAVING keeps only quarters clearing 250k of revenue.

## Q90: Show the max-stock product quantity per category plus the count of products that are out of stock, in one grouped query per category.
**Query:**
```sql
SELECT category_id,
       MAX(stock) AS max_stock,
       SUM(CASE WHEN stock = 0 THEN 1 ELSE 0 END) AS out_of_stock_count
FROM products
GROUP BY category_id;
```
**Explanation:** MAX summarizes the category while a conditional SUM counts the zero-stock subset, multi-aggregating one group per category.

## Q91: Use COUNT(DISTINCT ...) in HAVING to find teams that touched more than 3 distinct repositories.
**Query:**
```sql
SELECT team_id
FROM commits
GROUP BY team_id
HAVING COUNT(DISTINCT repo_id) > 3;
```
**Explanation:** Distinct counting inside the group, then thresholding on it in HAVING, identifies teams working across more than three repos.

**Alt1:** Add the number itself instead of returning bare team ids:
```sql
SELECT team_id, COUNT(DISTINCT repo_id) AS repos_touched
FROM commits
GROUP BY team_id
HAVING COUNT(DISTINCT repo_id) > 3;
```
**Explanation:** The distinction: Alt1 repeats the distinct-count in both SELECT and HAVING (portable), whereas omitting it from SELECT only drops the display value.

## Q92: Write one query per dialect note that computes a grouped median-free check: flag regions with above-average average order value using purely GROUP BY/HAVING with a subquery.
**Query:**
```sql
SELECT region, AVG(amount) AS avg_value
FROM orders
GROUP BY region
HAVING AVG(amount) > (SELECT AVG(amount) FROM orders);
```
**Explanation:** The scalar subquery in HAVING is a global average; each region's own AVG is kept only if it beats the overall mean — no window functions involved.

**Alt1:** PostgreSQL-equivalent using a lateral-style scalar only (identical syntax works):
```sql
SELECT region, AVG(amount) AS avg_value
FROM orders
GROUP BY region
HAVING AVG(amount) > AVG(amount) OVER ();  -- NOT portable; contrast only
```
**Explanation:** Shown solely to contrast: a global window average cannot be referenced in HAVING without an additional nesting layer, so the scalar subquery form is the correct portable approach.

## Q93: Group campaign responses by channel and day, computing conversion count and rate, ordered by best conversion rate first.
**Query:**
```sql
SELECT channel,
       day,
       COUNT(*) AS responses,
       ROUND(SUM(CASE WHEN converted THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS conv_pct
FROM campaign_events
GROUP BY channel, day
ORDER BY conv_pct DESC;
```
**Explanation:** The conversion rate is derived purely from grouped aggregates (ratio of conditional SUM to COUNT), and ordering by that computed alias ranks the best channels.
**Alt1:** Guard the ratio with NULLIF for empty-group safety:
```sql
SELECT channel, day, COUNT(*) AS responses,
       ROUND(SUM(CASE WHEN converted THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 2) AS conv_pct
FROM campaign_events
GROUP BY channel, day
ORDER BY conv_pct DESC;
```
**Explanation:** `NULLIF(COUNT(*), 0)` avoids a divide-by-zero if a degenerate group ever appears; identical results for normal rows.


## Q94: Deduplicate subscriptions keeping the most expensive plan per user by grouping user_id and applying MAX on price plus a companion MIN dance, then explain the pairing limitation.
**Query:**
```sql
SELECT user_id, MAX(price) AS max_price, MIN(subscription_id) AS a_plan_id
FROM subscriptions
GROUP BY user_id;
```
**Explanation:** MAX(price) gives the top price per user, but the plan id comes from a different row unless price ties are unique — a classic GROUP BY pairing hazard solved properly with window functions in the sibling file.

## Q95: Write an Oracle/CUBE-style query flagging natural language vs NULL dimension rows with GROUPING so dashboards don't misread totals as real regions.
**Query:**
```sql
SELECT region, product_id,
       GROUPING_ID(region, product_id) AS rollup_level,
       SUM(amount) AS total
FROM sales
GROUP BY CUBE (region, product_id);
```
**Explanation:** `GROUPING_ID` encodes which dimensions are rolled up into a bitmask — 3 for the grand total, 2/1 for single-dimension subtotals, 0 for detail rows — letting dashboards label every level unambiguously.

## Q96: Bucket transactions by their amount into two-part bands (0-100, 100-200, ...) with computed labels, and count each band, ordering by the lower bound.
**Query:**
```sql
SELECT CONCAT(FLOOR(amount/100)*100, '-', FLOOR(amount/100)*100 + 99) AS bucket,
       COUNT(*) AS tx_count
FROM transactions
GROUP BY CONCAT(FLOOR(amount/100)*100, '-', FLOOR(amount/100)*100 + 99);
```
**Explanation:** The label is built entirely from other GROUP BY-eligible expressions, so grouping by the same concatenation is valid; ordering by the numeric floor would need the expression in ORDER BY or a subquery.

**Alt1:** Cleaner numeric-bound approach sorting correctly:
```sql
SELECT FLOOR(amount/100)*100 AS lb, COUNT(*) AS tx_count
FROM transactions
GROUP BY FLOOR(amount/100)*100
ORDER BY lb;
```
**Explanation:** Keeping the bucket as a number makes ordering natural and the group key reusable — labels can be added in a final projection layer.

## Q97: Write a query that proves HAVING can reference only grouped/aggregated things by erroneously trying a plain column, then correcting it.
**Query:**
```sql
-- Broken: SELECT store_id, net FROM sales GROUP BY store_id HAVING net > 0;
-- net is neither grouped nor aggregated -> error in strict engines.

SELECT store_id, SUM(net) AS net_total
FROM sales
GROUP BY store_id
HAVING SUM(net) > 0;
```
**Explanation:** The commented attempt is invalid because `net` isn't in the GROUP BY and isn't aggregated; the fix wraps it in `SUM` so HAVING compares group-level values.

## Q98: Find pairs (region, year) whose revenue grew by comparing two banded groups in one query using conditional SUM over amounts with sign.
**Query:**
```sql
SELECT region, EXTRACT(YEAR FROM sale_date) AS yr,
       SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS gains,
       SUM(CASE WHEN amount <= 0 THEN ABS(amount) ELSE 0 END) AS losses
FROM sales
GROUP BY region, EXTRACT(YEAR FROM sale_date)
HAVING SUM(amount) > 0;
```
**Explanation:** Conditional SUMs split each region-year group into gains and losses while HAVING keeps only net-positive pairs — a compact P&L per combination.

## Q99: Write the dedup-by-latest pattern that keeps the row with the greatest id per (customer, campaign) using the group-by-everything-else shape.
**Query:**
```sql
SELECT customer_id, campaign_id, MAX(row_id) AS latest_row
FROM clicks
GROUP BY customer_id, campaign_id;
```
**Explanation:** All identifying columns are group keys; the surrogate `row_id` is aggregated with MAX to retain exactly one "latest" row per pair, ready to drive a self-join back to the original table.

## Q100: Combine grouping, multiple aggregates, HAVING on ratio, and ordering into one master query, and contrast against what a window function would change.
**Query:**
```sql
SELECT category,
       COUNT(*) AS sku_count,
       SUM(stock) AS total_stock,
       AVG(price) AS avg_price,
       SUM(CASE WHEN stock = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS stockout_pct
FROM products
GROUP BY category
HAVING COUNT(*) >= 5
   AND SUM(CASE WHEN stock = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) > 30
ORDER BY stockout_pct DESC;
```
**Explanation:** WHERE-like filters happen on rows, aggregates on groups, HAVING on aggregates (including a percentage ratio), and ORDER BY on the final aliases — the full GROUP BY/HAVING stack in one statement. Replacing HAVING's ratio check with a ranked RANK()/OVER() top-N would shift the problem into the window-functions sibling file.
**Alt1:** Two-pass shape — compute the ratio once, gate it in an outer WHERE:
```sql
SELECT category, sku_count, total_stock, avg_price, stockout_pct
FROM (SELECT category, COUNT(*) AS sku_count, SUM(stock) AS total_stock,
             AVG(price) AS avg_price,
             SUM(CASE WHEN stock = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS stockout_pct
      FROM products GROUP BY category) t
WHERE sku_count >= 5 AND stockout_pct > 30
ORDER BY stockout_pct DESC;
```
**Explanation:** Derived-table wrappers let you reuse aggregate aliases in WHERE — HAVING and this shape produce identical output, differing only in pipeline organization.

