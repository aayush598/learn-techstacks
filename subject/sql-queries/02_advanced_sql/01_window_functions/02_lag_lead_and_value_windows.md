# LAG, LEAD, FIRST_VALUE, LAST_VALUE Window Functions — 100 SQL Interview Q&A

## Q1: Write a query to show each day's sales and the previous day's sales using LAG.

**Query:**
```sql
SELECT sales_date,
       sales_amount,
       LAG(sales_amount) OVER (ORDER BY sales_date) AS prev_day_sales
FROM daily_sales
ORDER BY sales_date;
```

**Explanation:** LAG reads the value `sales_amount` from the row that precedes the current row when rows are ordered by `sales_date`, so each row shows the previous day's figure.

**Alt1:** LEAD instead — the same previous-value via a self-join on the prior date:
```sql
SELECT d.sales_date,
       d.sales_amount,
       p.sales_amount AS prev_day_sales
FROM daily_sales d
LEFT JOIN daily_sales p ON p.sales_date = d.sales_date - INTERVAL 1 DAY
ORDER BY d.sales_date;
```
The self-join produces the same column but fails when dates are non-consecutive; LAG is immune to sparse calendars.

## Q2: Write a query to show each day's sales and the next day's sales using LEAD.

**Query:**
```sql
SELECT sales_date,
       sales_amount,
       LEAD(sales_amount) OVER (ORDER BY sales_date) AS next_day_sales
FROM daily_sales
ORDER BY sales_date;
```

**Explanation:** LEAD reads the value from the row that follows the current row in `sales_date` order, giving the next day's number on each row.

**Alt1:** Rewritten as a self-join matching the following date:
```sql
SELECT d.sales_date,
       d.sales_amount,
       n.sales_amount AS next_day_sales
FROM daily_sales d
LEFT JOIN daily_sales n ON n.sales_date = d.sales_date + INTERVAL 1 DAY
ORDER BY d.sales_date;
```
Equivalent for back-to-back dates; LEAD handles calendar gaps without the join predicate.

## Q3: Write a query to show each employee's salary and the previous employee's salary, defaulting to 0 when there is no previous row.

**Query:**
```sql
SELECT employee_id,
       salary,
       LAG(salary, 1, 0) OVER (ORDER BY employee_id) AS prev_salary
FROM employees;
```

**Explanation:** The third argument `0` is the default returned when there is no lagging row (the first row in the window); without it you would get NULL.

**Alt1:** PostgreSQL — `LAG(salary) OVER (ORDER BY employee_id) OVER` self-join:
```sql
SELECT a.employee_id,
       a.salary,
       COALESCE(b.salary, 0) AS prev_salary
FROM employees a
LEFT JOIN employees b ON b.employee_id = a.employee_id - 1
ORDER BY a.employee_id;
```
The self-join relies on contiguous `employee_id` values; COALESCE supplies the 0 default.

## Q4: Write a query to show each employee's salary and the next employee's salary, returning the current salary when there is no next row.

**Query:**
```sql
SELECT employee_id,
       salary,
       LEAD(salary, 1, salary) OVER (ORDER BY employee_id) AS next_salary
FROM employees;
```

**Explanation:** The default value is evaluated and returned for the last row of the window, which here repeats the current salary instead of returning NULL.

## Q5: Write a query to compare today's sales with the sales from two days ago using LAG with an offset.

**Query:**
```sql
SELECT sales_date,
       sales_amount,
       LAG(sales_amount, 2) OVER (ORDER BY sales_date) AS sales_two_days_ago
FROM daily_sales;
```

**Explanation:** The second argument `2` instructs LAG to skip back two rows, so only rows with at least two preceding rows get a non-NULL value.

**Alt1:** Two-offset via ROW_NUMBER join:
```sql
WITH r AS (
    SELECT sales_date, sales_amount,
           ROW_NUMBER() OVER (ORDER BY sales_date) AS rn
    FROM daily_sales
)
SELECT a.sales_date, a.sales_amount, b.sales_amount AS sales_two_days_ago
FROM r a LEFT JOIN r b ON b.rn = a.rn - 2;
```
Positional numbering emulates a LAG offset of 2, trading a window call for a self-join.

## Q6: Write a query to compare today's sales with the sales from two days ahead using LEAD with an offset.

**Query:**
```sql
SELECT sales_date,
       sales_amount,
       LEAD(sales_amount, 2) OVER (ORDER BY sales_date) AS sales_in_two_days
FROM daily_sales;
```

**Explanation:** LEAD jumps two rows ahead in the ordered window; the final two rows of the result contain NULL for this column.

## Q7: Write a query to show each order and the customer's previous order amount using LAG with PARTITION BY.

**Query:**
```sql
SELECT customer_id,
       order_id,
       order_date,
       order_amount,
       LAG(order_amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order_amount
FROM orders;
```

**Explanation:** PARTITION BY customer_id resets the window per customer, so LAG always compares against that customer's own earlier order rather than arbitrary previous rows.

**Alt1:** Correlated subquery:
```sql
SELECT o.customer_id,
       o.order_id,
       o.order_date,
       o.order_amount,
       (SELECT MAX(o2.order_amount)
        FROM orders o2
        WHERE o2.customer_id = o.customer_id
          AND o2.order_date < o.order_date
       ) AS prev_order_amount
FROM orders o;
```
The subquery approximates LAG but only works for a single previous row and needs a tie-friendly predicate; LAG is simpler and faster at scale.

## Q8: Write a query to show each order and the customer's next order amount using LEAD with PARTITION BY.

**Query:**
```sql
SELECT customer_id,
       order_id,
       order_date,
       order_amount,
       LEAD(order_amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS next_order_amount
FROM orders;
```

**Explanation:** The window is partitioned per customer and ordered by date, so LEAD looks at that customer's next chronological order; the latest order per customer gets NULL.

## Q9: Write a query to list each department's employees along with the salary of the employee hired just before them.

**Query:**
```sql
SELECT department_id,
       employee_id,
       hire_date,
       LAG(salary) OVER (PARTITION BY department_id ORDER BY hire_date) AS prev_hire_salary
FROM employees;
```

**Explanation:** Ordering by `hire_date` inside each department partition makes LAG return the salary of the previously hired colleague in the same department.

## Q10: Write a query to compute the day-over-day change in sales using LAG.

**Query:**
```sql
SELECT sales_date,
       sales_amount,
       sales_amount - LAG(sales_amount) OVER (ORDER BY sales_date) AS day_over_day_change
FROM daily_sales;
```

**Explanation:** Subtracting the previous day's amount from the current amount gives the delta; the first row will be NULL because there is no prior day.

**Alt1:** Self-join on consecutive dates:
```sql
SELECT d.sales_date,
       d.sales_amount,
       d.sales_amount - COALESCE(p.sales_amount, 0) AS day_over_day_change
FROM daily_sales d
LEFT JOIN daily_sales p ON p.sales_date = d.sales_date - INTERVAL 1 DAY
ORDER BY d.sales_date;
```
Matching on `sales_date - 1 day` reproduces the LAG result, but only if dates are contiguous.

## Q11: Write a query to compute the percentage growth from the previous day's sales.

**Query:**
```sql
SELECT sales_date,
       sales_amount,
       ROUND((sales_amount - LAG(sales_amount) OVER (ORDER BY sales_date))
             * 100.0 / LAG(sales_amount) OVER (ORDER BY sales_date), 2) AS pct_growth
FROM daily_sales;
```

**Explanation:** The change is divided by the previous value and multiplied by 100 to produce a percentage; guard against a zero/negative previous value in real data.

## Q12: Write a query to flag each row as 'up' or 'down' depending on whether the price increased or decreased from the prior close.

**Query:**
```sql
SELECT trade_date,
       close_price,
       CASE WHEN close_price > LAG(close_price) OVER (ORDER BY trade_date) THEN 'up'
            WHEN close_price < LAG(close_price) OVER (ORDER BY trade_date) THEN 'down'
            ELSE 'flat' END AS direction
FROM stock_prices;
```

**Explanation:** LAG supplies the prior close and a CASE maps the comparison to a label; the first row is NULL comparing so falls to 'flat'.

**Alt1:** Comparison via LEAD against current on a reversed window:
```sql
SELECT trade_date,
       close_price,
       CASE WHEN LEAD(close_price) OVER (ORDER BY trade_date DESC) < close_price THEN 'up'
            WHEN LEAD(close_price) OVER (ORDER BY trade_date DESC) > close_price THEN 'down'
            ELSE 'flat' END AS direction
FROM stock_prices;
```
Ordering descending makes LEAD expose the *previous* close in natural time, mirroring LAG.

## Q13: Write a query to add an is_increase flag (1/0) showing whether each product's stock level went up compared with the previous recorded level.

**Query:**
```sql
SELECT product_id,
       recorded_at,
       stock_level,
       CASE WHEN stock_level > LAG(stock_level) OVER (PARTITION BY product_id ORDER BY recorded_at)
            THEN 1 ELSE 0 END AS is_increase
FROM inventory_snapshots;
```

**Explanation:** Partitioning by product and ordering by recording time makes LAG pick the previous snapshot for the same product, and the CASE reduces the comparison to a boolean flag.

## Q14: Write a query that shows each employee and their previous job title, printing 'N/A' instead of NULL for the first employee.

**Query:**
```sql
SELECT employee_id,
       job_title,
       LAG(job_title, 1, 'N/A') OVER (ORDER BY hire_date) AS prev_job_title
FROM employee_history;
```

**Explanation:** The third argument provides a string default for the opening rows, making the result display-friendly instead of showing NULL.

## Q15: Write a query to show each user's activity and the timestamp of their next login using LEAD.

**Query:**
```sql
SELECT user_id,
       login_ts,
       LEAD(login_ts) OVER (PARTITION BY user_id ORDER BY login_ts) AS next_login_ts
FROM user_logins;
```

**Explanation:** LEAD over the per-user partition ordered by time returns the very next login timestamp for the same user.

**Alt1:** MIN with a correlated subquery:
```sql
SELECT l.user_id,
       l.login_ts,
       (SELECT MIN(l2.login_ts)
        FROM user_logins l2
        WHERE l2.user_id = l.user_id
          AND l2.login_ts > l.login_ts) AS next_login_ts
FROM user_logins l;
```
The subquery finds the smallest timestamp greater than the current one — the analytic equivalent of LEAD(1).

## Q16: Write a query to compute the gap in minutes between consecutive events for each user.

**Query:**
```sql
SELECT user_id,
       event_ts,
       TIMESTAMPDIFF(MINUTE, event_ts,
                     LEAD(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts)) AS mins_to_next
FROM user_events;
```

**Explanation:** LEAD pulls the next event timestamp in the same partition and `TIMESTAMPDIFF` computes minutes between them; the final event per user has NULL.

**Alt1:** PostgreSQL version using EXTRACT:
```sql
SELECT user_id,
       event_ts,
       EXTRACT(EPOCH FROM (
           LEAD(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts) - event_ts
       )) / 60 AS mins_to_next
FROM user_events;
```
Subtracting two timestamps gives an interval, converted to seconds and then to minutes.

## Q17: Write a query to backfill NULL stage names with the last known value using LAG and COALESCE.

**Query:**
```sql
SELECT order_id,
       stage_ts,
       stage_name,
       COALESCE(stage_name,
                LAG(stage_name) OVER (ORDER BY stage_ts)) AS filled_stage
FROM order_stages;
```

**Explanation:** COALESCE returns the current stage name when present; otherwise LAG supplies the previous row's name — a simple one-row backfill (see Q55 for multi-row).

## Q18: Write a query using LAG to show each row along with both the previous and two-rows-back amounts in one result.

**Query:**
```sql
SELECT sales_date,
       sales_amount,
       LAG(sales_amount, 1) OVER (ORDER BY sales_date) AS prev_1,
       LAG(sales_amount, 2) OVER (ORDER BY sales_date) AS prev_2
FROM daily_sales;
```

**Explanation:** Two LAG calls with offsets 1 and 2 against the same window definition produce both neighbours in a single SELECT.

**Alt1:** Self-join producing the same two columns via ROW_NUMBER:
```sql
WITH r AS (
    SELECT sales_date, sales_amount,
           ROW_NUMBER() OVER (ORDER BY sales_date) AS rn
    FROM daily_sales
)
SELECT a.sales_date, a.sales_amount, b.sales_amount AS prev_1, c.sales_amount AS prev_2
FROM r a
LEFT JOIN r b ON b.rn = a.rn - 1
LEFT JOIN r c ON c.rn = a.rn - 2;
```
Two positional joins replace LAG(1) and LAG(2); heavier to write but valid in every dialect.

## Q19: Write a query to show each department's first hire date together with the name of the first hired employee using FIRST_VALUE.

**Query:**
```sql
SELECT department_id,
       employee_id,
       hire_date,
       FIRST_VALUE(employee_id) OVER (PARTITION BY department_id ORDER BY hire_date) AS first_emp_id
FROM employees;
```

**Explanation:** FIRST_VALUE returns the employee_id of the first row within each department partition ordered by hire date — the earliest hire.

**Alt1:** MIN over the window is equivalent for the value itself:
```sql
SELECT department_id,
       hire_date,
       MIN(employee_id) OVER (PARTITION BY department_id) AS first_emp_id
FROM employees;
```
Only valid when the smallest employee_id also belongs to the earliest hire; FIRST_VALUE is the correct general tool.

## Q20: Write a query to show each department's last hire date and last hire's name using LAST_VALUE, then explain why the result looks wrong.

**Query:**
```sql
SELECT department_id,
       employee_id,
       hire_date,
       LAST_VALUE(employee_id) OVER (PARTITION BY department_id ORDER BY hire_date) AS last_emp_id
FROM employees;
```

**Explanation:** Without an explicit frame, LAST_VALUE evaluates over `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, so it returns the *current* row's employee_id and makes the query appear broken — the classic LAST_VALUE pitfall.

## Q21: Write a corrected version of Q20 that returns the true last hired employee per department using LAST_VALUE.

**Query:**
```sql
SELECT department_id,
       employee_id,
       hire_date,
       LAST_VALUE(employee_id) OVER (
           PARTITION BY department_id ORDER BY hire_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS last_emp_id
FROM employees;
```

**Explanation:** `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` extends the frame to the whole partition so LAST_VALUE sees the final row.

## Q22: Write a query showing each employee with both the earliest and latest hire dates in their department, using FIRST_VALUE and LAST_VALUE together.

**Query:**
```sql
SELECT department_id,
       employee_id,
       hire_date,
       FIRST_VALUE(hire_date) OVER (
           PARTITION BY department_id ORDER BY hire_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS first_hire_date,
       LAST_VALUE(hire_date) OVER (
           PARTITION BY department_id ORDER BY hire_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS last_hire_date
FROM employees;
```

**Explanation:** Both functions share the full-partition frame, so they return the chronological boundaries of each department's hires.

## Q23: Write a query to compute how many days after the department's first hire each employee joined, using FIRST_VALUE.

**Query:**
```sql
SELECT department_id,
       employee_id,
       hire_date,
       DATEDIFF(hire_date,
                FIRST_VALUE(hire_date) OVER (PARTITION BY department_id ORDER BY hire_date)) AS days_after_first_hire
FROM employees;
```

**Explanation:** The first hire's date is anchored for every row in the partition and DATEDIFF measures how many days later the current employee arrived.

**Alt1:** MIN over the partition plays the anchor role when IDs are comparable:
```sql
SELECT department_id,
       employee_id,
       hire_date,
       DATEDIFF(hire_date, MIN(hire_date) OVER (PARTITION BY department_id)) AS days_after_first_hire
FROM employees;
```
MIN over a window reaches the earliest hire date without ordering the window; simpler but less flexible than FIRST_VALUE.

## Q24: Write a query to show each row's previous, current, and next sales amount in one row using LAG and LEAD together.

**Query:**
```sql
SELECT sales_date,
       sales_amount,
       LAG(sales_amount) OVER (ORDER BY sales_date)   AS prev_amount,
       LEAD(sales_amount) OVER (ORDER BY sales_date)  AS next_amount
FROM daily_sales;
```

**Explanation:** LAG and LEAD run over the same ordering; combined they give a sliding triple of previous/current/next on every row.

## Q25: Write a query to return the second-highest salary per department using NTH_VALUE.

**Query:**
```sql
SELECT department_id,
       employee_id,
       salary,
       NTH_VALUE(salary, 2) OVER (
           PARTITION BY department_id ORDER BY salary DESC
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS second_highest_salary
FROM employees;
```

**Explanation:** NTH_VALUE(salary, 2) grabs the second row of the partition ordered by salary descending; the full-partition frame is required so the second row is always in scope.

## Q26: Write a query to flag rows where a value resets back to a baseline, saying the previous value using LAG.

**Query:**
```sql
SELECT reading_id,
       device_id,
       counter_value,
       LAG(counter_value) OVER (PARTITION BY device_id ORDER BY reading_id) AS prev_counter,
       CASE WHEN counter_value < LAG(counter_value) OVER (PARTITION BY device_id ORDER BY reading_id)
            THEN 'reset' ELSE 'normal' END AS status
FROM meter_readings;
```

**Explanation:** If the current counter is smaller than the previous reading for the same device, the gauge must have reset; LAG provides the prior reading to compare against.

## Q27: Write a query to show each order and how it ranks by value against the customer's first ever order using FIRST_VALUE.

**Query:**
```sql
SELECT customer_id,
       order_id,
       order_amount,
       FIRST_VALUE(order_amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS first_order_amount,
       CASE WHEN order_amount > FIRST_VALUE(order_amount) OVER (PARTITION BY customer_id ORDER BY order_date)
            THEN 'exceeded_first' ELSE 'below_or_equal' END AS comparison
FROM orders;
```

**Explanation:** FIRST_VALUE anchors every row of the customer partition to that customer's first order amount, enabling an at-a-glance comparison.

## Q28: Write a query to calculate the percentage difference between each sale and the customer's first sale.

**Query:**
```sql
SELECT customer_id,
       order_id,
       order_amount,
       ROUND((order_amount - FIRST_VALUE(order_amount) OVER (PARTITION BY customer_id ORDER BY order_date))
             * 100.0 / FIRST_VALUE(order_amount) OVER (PARTITION BY customer_id ORDER BY order_date), 2) AS pct_vs_first
FROM orders;
```

**Explanation:** Each row's amount is relativised to the partition's opening amount, showing growth or shrinkage relative to the first purchase.

## Q29: Write a query to list users whose consecutive logins were more than 7 days apart using LEAD.

**Query:**
```sql
SELECT user_id,
       login_ts,
       next_login,
       DATEDIFF(DAY, login_ts, next_login) AS gap_days
FROM (
    SELECT user_id,
           login_ts,
           LEAD(login_ts) OVER (PARTITION BY user_id ORDER BY login_ts) AS next_login
    FROM user_logins
) t
WHERE DATEDIFF(DAY, login_ts, next_login) > 7;
```

**Explanation:** An inner query computes each user's next login with LEAD, and the outer filter keeps only gaps exceeding seven days.

## Q30: Write a query returning each customer's third purchase amount using NTH_VALUE.

**Query:**
```sql
SELECT customer_id,
       order_id,
       order_date,
       order_amount,
       NTH_VALUE(order_amount, 3) OVER (
           PARTITION BY customer_id ORDER BY order_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS third_order_amount
FROM orders;
```

**Explanation:** NTH_VALUE positions the window at the third row per partition and returns its amount; the unbounded frame makes rows 3+ all carry the same value.

**Alt1:** The same result via a self-join to the third order:
```sql
SELECT o.customer_id,
       o.order_id,
       o.order_date,
       o.order_amount,
       t3.order_amount AS third_order_amount
FROM orders o
LEFT JOIN LATERAL (
    SELECT o2.order_amount
    FROM orders o2
    WHERE o2.customer_id = o.customer_id
    ORDER BY o2.order_date
    LIMIT 1 OFFSET 2
) t3 ON true;
```
A lateral subquery pinned at offset 2 picks the third order per customer — an explicit alternative to NTH_VALUE.

## Q31: Write a query to compute month-over-month revenue change using LAG after truncating dates to months.

**Query:**
```sql
SELECT DATE_TRUNC('month', order_date) AS month,
       SUM(order_amount) AS monthly_revenue,
       SUM(order_amount) - LAG(SUM(order_amount)) OVER (ORDER BY DATE_TRUNC('month', order_date)) AS mom_change
FROM orders
GROUP BY DATE_TRUNC('month', order_date);
```

**Explanation:** Aggregate first with GROUP BY, then apply LAG to the grouped sums so consecutive months compare directly.

**Alt1:**
```sql
-- MySQL 8+
SELECT DATE_FORMAT(order_date, '%Y-%m-01') AS month,
       SUM(order_amount) AS monthly_revenue,
       SUM(order_amount) - LAG(SUM(order_amount)) OVER (ORDER BY DATE_FORMAT(order_date, '%Y-%m-01')) AS mom_change
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m-01');
```
MySQL accepts window functions on grouped expressions as long as the window ORDER BY matches the GROUP BY expression.

## Q32: Write a query to compute week-over-week sales change using LAG on weekly aggregates.

**Query:**
```sql
SELECT DATE_TRUNC('week', sales_date) AS week,
       SUM(sales_amount) AS weekly_sales,
       SUM(sales_amount) - LAG(SUM(sales_amount)) OVER (ORDER BY DATE_TRUNC('week', sales_date)) AS wow_change
FROM daily_sales
GROUP BY DATE_TRUNC('week', sales_date);
```

**Explanation:** Aggregating to weekly buckets first lets LAG line up adjacent weeks for the week-over-week delta.

## Q33: Write a query that compares each store's current monthly sales to that same store's previous monthly sales.

**Query:**
```sql
SELECT store_id,
       sales_month,
       monthly_sales,
       LAG(monthly_sales) OVER (PARTITION BY store_id ORDER BY sales_month) AS prev_month_sales
FROM (
    SELECT store_id,
           DATE_TRUNC('month', sales_date) AS sales_month,
           SUM(sales_amount) AS monthly_sales
    FROM sales
    GROUP BY store_id, DATE_TRUNC('month', sales_date)
) t;
```

**Explanation:** The subquery pre-aggregates per store per month; LAG then partitions by store so each row only sees that store's previous month.

## Q34: Write a query to find the last order date for each customer using FIRST_VALUE on a descending order.

**Query:**
```sql
SELECT customer_id,
       order_id,
       order_date,
       FIRST_VALUE(order_date) OVER (
           PARTITION BY customer_id ORDER BY order_date DESC
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS last_order_date
FROM orders;
```

**Explanation:** Ordering the window by date descending makes the newest order the first row, so FIRST_VALUE returns the latest purchase.

## Q35: Write a query to compute the difference in days between each purchase and the customer's most recent previous purchase using LAG.

**Query:**
```sql
SELECT customer_id,
       order_date,
       DATEDIFF(order_date,
                LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)) AS days_since_last_purchase
FROM orders;
```

**Explanation:** LAG provides the previous purchase date in the customer partition; DATEDIFF computes elapsed days. The first order per customer is NULL.

**Alt1:** LEAD instead of LAG to compute days *until* the next purchase:
```sql
SELECT customer_id,
       order_date,
       DATEDIFF(LEAD(order_date) OVER (PARTITION BY customer_id ORDER BY order_date), order_date) AS days_until_next_purchase
FROM orders;
```
Direction only changes which date is subtracted from which.

## Q36: Write a query using LAG to identify the start of a new streak when a dimension value changes.

**Query:**
```sql
SELECT event_id,
       user_id,
       category,
       LAG(category) OVER (PARTITION BY user_id ORDER BY event_ts) AS prev_category,
       CASE WHEN category <> LAG(category) OVER (PARTITION BY user_id ORDER BY event_ts)
            OR LAG(category) OVER (PARTITION BY user_id ORDER BY event_ts) IS NULL
            THEN 1 ELSE 0 END AS streak_start
FROM user_events;
```

**Explanation:** A streak starts when the category differs from the previous event (or when it is the user's first event); LAG produces the comparison value.

## Q37: Write a query to detect gaps in a transaction sequence using LAG.

**Query:**
```sql
SELECT tx_id,
       account_id,
       tx_time,
       tx_id - LAG(tx_id) OVER (PARTITION BY account_id ORDER BY tx_id) AS seq_gap
FROM transactions
HAVING seq_gap > 1;
```

**Explanation:** If consecutive IDs differ by more than one, rows are missing; the outer HAVING filters on the LAG-derived gap.

## Q38: Write a query to show the first and last event type in each user session partitioned by session_id.

**Query:**
```sql
SELECT session_id,
       user_id,
       event_ts,
       event_type,
       FIRST_VALUE(event_type) OVER (PARTITION BY session_id ORDER BY event_ts
                                     ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS first_event,
       LAST_VALUE(event_type)  OVER (PARTITION BY session_id ORDER BY event_ts
                                     ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_event
FROM session_events;
```

**Explanation:** Both window functions span the whole session partition, so every row reports the session's opening and closing event types.

## Q39: Write a query to compute the difference between each sale and the previous sale of the same product using LAG.

**Query:**
```sql
SELECT product_id,
       sale_date,
       quantity_sold,
       quantity_sold - LAG(quantity_sold) OVER (PARTITION BY product_id ORDER BY sale_date) AS qty_change
FROM product_sales;
```

**Explanation:** The partition restricts LAG to consecutive sales of one product, exposing the volume jump or drop on each row.

## Q40: Write a query to return the third most recent order amount per customer using NTH_VALUE with a descending order.

**Query:**
```sql
SELECT customer_id,
       order_id,
       order_date,
       order_amount,
       NTH_VALUE(order_amount, 3) OVER (
           PARTITION BY customer_id ORDER BY order_date DESC
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS third_most_recent_amount
FROM orders;
```

**Explanation:** Ordering the partition descending puts newest first, so NTH_VALUE(…, 3) yields the third most recent order amount.

## Q41: Write a query to compare each row to the maximum value in its partition using LAST_VALUE with an explicit frame.

**Query:**
```sql
SELECT product_id,
       price,
       LAST_VALUE(price) OVER (
           PARTITION BY product_id ORDER BY price
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS max_price,
       price - LAST_VALUE(price) OVER (
           PARTITION BY product_id ORDER BY price
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS diff_from_max
FROM product_price_snapshots;
```

**Explanation:** With an unbounded frame in both directions, LAST_VALUE reaches partition end — the highest price — and each row shows its gap to that maximum.

## Q42: Write a query to show each row with the minimum and maximum price in the partition, using FIRST_VALUE and LAST_VALUE.

**Query:**
```sql
SELECT product_id,
       price_date,
       price,
       FIRST_VALUE(price) OVER (
           PARTITION BY product_id ORDER BY price
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS min_price,
       LAST_VALUE(price) OVER (
           PARTITION BY product_id ORDER BY price
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS max_price
FROM product_prices;
```

**Explanation:** Ordering by price makes the partition's first row the minimum and last row the maximum; the shared unbounded frame lets both be reached.

**Alt1:** MIN/MAX aggregates over the same window:
```sql
SELECT product_id,
       price_date,
       price,
       MIN(price) OVER (PARTITION BY product_id) AS min_price,
       MAX(price) OVER (PARTITION BY product_id) AS max_price
FROM product_prices;
```
Order-independent MIN/MAX give the identical bounds in one pass, a compact substitute for the value-function pair.

## Q43: Write a query to compute year-over-year sales change using LAG on yearly aggregates.

**Query:**
```sql
SELECT YEAR(order_date) AS yr,
       SUM(order_amount) AS yearly_revenue,
       SUM(order_amount) - LAG(SUM(order_amount)) OVER (ORDER BY YEAR(order_date)) AS yoy_change
FROM orders
GROUP BY YEAR(order_date);
```

**Explanation:** GROUP BY year, then LAG over the ordered yearly sums to subtract the prior year's revenue from the current one.

## Q44: Write a query to find the next 30-day window date per user using LEAD on a daily partition.

**Query:**
```sql
SELECT user_id,
       activity_date,
       LEAD(activity_date) OVER (PARTITION BY user_id ORDER BY activity_date) AS next_activity,
       DATEDIFF(LEAD(activity_date) OVER (PARTITION BY user_id ORDER BY activity_date), activity_date) AS days_between
FROM user_activity
WHERE DATEDIFF(LEAD(activity_date) OVER (PARTITION BY user_id ORDER BY activity_date), activity_date) <= 30;
```

**Explanation:** LEAD gives each user's next activity date, and DATEDIFF measures the gap; only rows within 30 days of the next activity remain.

## Q45: Write a query to compute each customer's first purchase price alongside every purchase using a self-contained FIRST_VALUE.

**Query:**
```sql
SELECT customer_id,
       order_id,
       order_amount,
       FIRST_VALUE(order_amount) OVER (
           PARTITION BY customer_id ORDER BY order_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS first_purchase_amount
FROM orders;
```

**Explanation:** The first row of the customer partition ordered by date is the first purchase, so FIRST_VALUE propagates that amount to every row.

## Q46: Write a query to show each product's current price and the difference from the price at the partition's start using FIRST_VALUE.

**Query:**
```sql
SELECT product_id,
       snapshot_date,
       price,
       FIRST_VALUE(price) OVER (PARTITION BY product_id ORDER BY snapshot_date) AS opening_price,
       price - FIRST_VALUE(price) OVER (PARTITION BY product_id ORDER BY snapshot_date) AS change_since_opening
FROM price_history;
```

**Explanation:** FIRST_VALUE defaults to the frame `UNBOUNDED PRECEDING .. CURRENT ROW`, which for the opening price is identical to the full partition because ordering fixes row one — no explicit frame needed.

## Q47: Write a query to detect when a product's price changed from the previous recorded snapshot, flagging the changed rows.

**Query:**
```sql
SELECT product_id,
       snapshot_date,
       price,
       CASE WHEN price = LAG(price) OVER (PARTITION BY product_id ORDER BY snapshot_date)
            THEN 'unchanged' ELSE 'price_changed' END AS price_flag
FROM price_history;
```

**Explanation:** The first snapshot has no lagging row (NULL), so it is reported as changed — correct, since it establishes the initial price.

**Alt1:** Window-free self-join that compares only adjacent snapshots:
```sql
SELECT a.product_id,
       a.snapshot_date,
       a.price,
       CASE WHEN a.price <> b.price THEN 'price_changed' ELSE 'unchanged' END AS price_flag
FROM price_history a
JOIN price_history b
  ON b.product_id = a.product_id
 AND b.snapshot_date = (SELECT MAX(c.snapshot_date)
                        FROM price_history c
                        WHERE c.product_id = a.product_id
                          AND c.snapshot_date < a.snapshot_date);
```
Each row is paired with its exact predecessor via a maximum-date subquery, replicating LAG behaviour for one step back.

## Q48: Write a query to compute the minutes each support ticket spent in a status using LEAD on status timestamps.

**Query:**
```sql
SELECT ticket_id,
       status,
       status_ts,
       EXTRACT(EPOCH FROM (
           LEAD(status_ts) OVER (PARTITION BY ticket_id ORDER BY status_ts) - status_ts
       )) / 60 AS minutes_in_status
FROM ticket_status_history;
```

**Explanation:** LEAD returns the timestamp of the next status for the same ticket; subtracting gives how long the current status was held.

## Q49: Write a query to show the most recent price for each product, keeping every row in the output using LAST_VALUE with the right frame.

**Query:**
```sql
SELECT product_id,
       snapshot_date,
       price,
       LAST_VALUE(price) OVER (
           PARTITION BY product_id ORDER BY snapshot_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS latest_price
FROM price_history;
```

**Explanation:** Ordering by date ascending plus an unbounded-following frame means LAST_VALUE sees the newest snapshot and repeats it on every row.

## Q50: Write a query returning each employee's current salary along with the salary report's first and last recorded salaries, exhibiting the LAST_VALUE default-frame pitfall fix.

**Query:**
```sql
SELECT employee_id,
       salary,
       FIRST_VALUE(salary) OVER (ORDER BY salary_date) AS first_recorded,
       LAST_VALUE(salary) OVER (ORDER BY salary_date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_recorded
FROM salary_history;
```

**Explanation:** FIRST_VALUE uses its default frame safely here (first row is fixed by ordering), while LAST_VALUE needs the explicit full-partition frame to return the final recorded salary instead of the current row's.

## Q51: Write a query to show the first and last activity timestamp for each user session and the session length using value window functions.

**Query:**
```sql
SELECT session_id,
       user_id,
       FIRST_VALUE(event_ts) OVER (PARTITION BY session_id ORDER BY event_ts) AS session_start,
       LAST_VALUE(event_ts) OVER (PARTITION BY session_id ORDER BY event_ts
                                  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS session_end,
       EXTRACT(EPOCH FROM (
           LAST_VALUE(event_ts) OVER (PARTITION BY session_id ORDER BY event_ts
                                      ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
           - FIRST_VALUE(event_ts) OVER (PARTITION BY session_id ORDER BY event_ts))) / 60 AS session_minutes
FROM session_events;
```

**Explanation:** FIRST_VALUE fixes the opening timestamp and LAST_VALUE (with a full-partition frame) the closing one; the session length is their difference.

## Q52: Write a query to compute the difference between each employee's salary and the maximum salary in their department, anchored via LAST_VALUE.

**Query:**
```sql
SELECT department_id,
       employee_id,
       salary,
       LAST_VALUE(salary) OVER (
           PARTITION BY department_id ORDER BY salary
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS dept_max_salary,
       salary - LAST_VALUE(salary) OVER (
           PARTITION BY department_id ORDER BY salary
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS gap_to_max
FROM employees;
```

**Explanation:** Ordering by salary ascending makes the final partition row the maximum; the expanded frame lets LAST_VALUE reach it from any row.

## Q53: Write a query to rank months by revenue and show the previous month's rank using LAG over a computed ranking.

**Query:**
```sql
SELECT sales_month,
       monthly_revenue,
       RANK() OVER (ORDER BY monthly_revenue DESC) AS revenue_rank,
       LAG(RANK() OVER (ORDER BY monthly_revenue DESC)) OVER (ORDER BY sales_month) AS prev_month_rank
FROM monthly_sales;
```

**Explanation:** A rank is computed over aggregated revenue, then LAG retrieves the prior calendar month's rank to show rank momentum.

## Q54: Write a query that fills every NULL price with the most recent non-NULL price using LAG and a running-marker trick.

**Query:**
```sql
SELECT day,
       price,
       COALESCE(price,
                LAST_VALUE(valid_price) OVER (
                    ORDER BY day
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )) AS filled_price
FROM (
    SELECT day,
           price,
           CASE WHEN price IS NOT NULL THEN price ELSE NULL END AS valid_price
    FROM asset_prices
) t;
```

**Explanation:** The last-known value is carried forward because LAST_VALUE over the frame `UNBOUNDED PRECEDING .. CURRENT ROW` repeats the most recent row that has a valid price.

## Q55: Write a query to find the previous day's closing price for a stock, defaulting to the stock's own first-ever price when none exists.

**Query:**
```sql
SELECT ticker,
       trade_date,
       close_price,
       LAG(close_price) OVER (PARTITION BY ticker ORDER BY trade_date) AS prev_close,
       COALESCE(LAG(close_price) OVER (PARTITION BY ticker ORDER BY trade_date),
                FIRST_VALUE(close_price) OVER (PARTITION BY ticker ORDER BY trade_date)) AS prev_or_first_close
FROM market_data;
```

**Explanation:** When LAG returns NULL on the first trading day, COALESCE falls back to FIRST_VALUE — the ticker's inaugural price — avoiding NULLs.

**Alt1:** PostgreSQL: same fallback expressed with a windowed MIN over the partition:
```sql
SELECT ticker,
       trade_date,
       close_price,
       LAG(close_price) OVER (PARTITION BY ticker ORDER BY trade_date) AS prev_close,
       COALESCE(LAG(close_price) OVER (PARTITION BY ticker ORDER BY trade_date),
                MIN(close_price) OVER (PARTITION BY ticker)) AS prev_or_first_close
FROM market_data;
```
MIN over the partition returns the earliest close when LAG has no predecessor, swapping FIRST_VALUE for an aggregate anchor.

## Q56: Write a query to compute the number of days between consecutive order delivery dates using LEAD.

**Query:**
```sql
SELECT order_id,
       customer_id,
       delivered_at,
       LEAD(delivered_at) OVER (PARTITION BY customer_id ORDER BY delivered_at) AS next_delivery,
       DATEDIFF(LEAD(delivered_at) OVER (PARTITION BY customer_id ORDER BY delivered_at), delivered_at) AS days_until_next_delivery
FROM orders
WHERE delivered_at IS NOT NULL;
```

**Explanation:** LEAD exposes the customer's next delivery date; DATEDIFF converts it to days. Non-delivered orders are excluded up front.

## Q57: Write a query to display each order along with the first, last, and second order amounts in the customer's partition in one row.

**Query:**
```sql
SELECT customer_id,
       order_id,
       order_amount,
       FIRST_VALUE(order_amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS first_amount,
       NTH_VALUE(order_amount, 2)   OVER (PARTITION BY customer_id ORDER BY order_date
                                          ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS second_amount,
       LAST_VALUE(order_amount)     OVER (PARTITION BY customer_id ORDER BY order_date
                                          ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_amount
FROM orders;
```

**Explanation:** Three value functions — FIRST_VALUE, NTH_VALUE, LAST_VALUE — each read a specific ordinal position of the same partitioned, ordered window.

## Q58: Write a query to show the price 3 trading days before the current row for each stock using LAG.

**Query:**
```sql
SELECT ticker,
       trade_date,
       close_price,
       LAG(close_price, 3) OVER (PARTITION BY ticker ORDER BY trade_date) AS close_3_days_ago
FROM stock_daily
ORDER BY ticker, trade_date;
```

**Explanation:** Offset 3 skips back three ordered rows per stock partition; the first three rows per ticker are NULL.

## Q59: Write a query using LAG to identify every row where an order status downgraded (e.g. from 'shipped' to 'pending') compared with the previous status.

**Query:**
```sql
SELECT order_id,
       status_ts,
       status,
       prev_status,
       CASE WHEN status < prev_status THEN 'downgrade' ELSE 'ok' END AS status_move
FROM (
    SELECT order_id,
           status_ts,
           status,
           LAG(status) OVER (PARTITION BY order_id ORDER BY status_ts) AS prev_status
    FROM order_status_log
) t;
```

**Explanation:** A predefined status ordering makes the string comparison meaningful: a lower rank than the previous one signals a downgrade.

## Q60: Write a query to compute each user's next payment date and the interval until it, using LEAD inside a payment-subscription join.

**Query:**
```sql
SELECT s.user_id,
       p.payment_date,
       amount,
       LEAD(p.payment_date) OVER (PARTITION BY s.user_id ORDER BY p.payment_date) AS next_payment,
       DATEDIFF(LEAD(p.payment_date) OVER (PARTITION BY s.user_id ORDER BY p.payment_date), p.payment_date) AS days_to_next
FROM payments p
JOIN subscriptions s ON s.subscription_id = p.subscription_id;
```

**Explanation:** After joining payments to subscriptions, LEAD partitions by the user so each payment shows the gap until the next one on the same account.

## Q61: Write a query to show the first event and the last event per user ordered by time, demonstrating that LAST_VALUE needs an explicit frame while FIRST_VALUE does not.

**Query:**
```sql
SELECT user_id,
       event_ts,
       event_type,
       FIRST_VALUE(event_type) OVER (PARTITION BY user_id ORDER BY event_ts) AS first_event,
       LAST_VALUE(event_type) OVER (
           PARTITION BY user_id ORDER BY event_ts
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS last_event
FROM user_events;
```

**Explanation:** FIRST_VALUE's default frame already starts at the partition beginning, but LAST_VALUE must be explicitly extended to the partition end or it will mirror the current row.

**Alt1:** Using aggregate MIN/MAX with a frame instead of the value functions:
```sql
SELECT user_id,
       event_ts,
       event_type,
       MIN(event_type) KEEP (DENSE_RANK FIRST ORDER BY event_ts) OVER (PARTITION BY user_id) AS first_event,
       MAX(event_type) KEEP (DENSE_RANK LAST  ORDER BY event_ts) OVER (PARTITION BY user_id) AS last_event
FROM user_events;
```
Oracle's `KEEP (DENSE_RANK ...)` aggregates return the value of the first/last row without re-sorting.

## Q62: Write a query that flags rows where the running value decreased twice in a row using two LAG offsets.

**Query:**
```sql
SELECT reading_id,
       reading_value,
       LAG(reading_value, 1) OVER (ORDER BY reading_id) AS v_prev1,
       LAG(reading_value, 2) OVER (ORDER BY reading_id) AS v_prev2,
       CASE WHEN reading_value < v_prev1 AND v_prev1 < v_prev2 THEN 'double_drop' ELSE 'ok' END AS pattern
FROM sensor_readings;
```

**Explanation:** Two LAG calls capture the last two values; the pattern condition requires the latest reading to be smaller than both, in descending succession.

## Q63: Write a query to compute the difference between each row's value and the first row's value of its partition using a single FIRST_VALUE stored in a CTE.

**Query:**
```sql
WITH anchor AS (
    SELECT region,
           month,
           sales,
           FIRST_VALUE(sales) OVER (PARTITION BY region ORDER BY month) AS first_sales
    FROM regional_sales
)
SELECT region,
       month,
       sales,
       first_sales,
       sales - first_sales AS diff_from_first
FROM anchor;
```

**Explanation:** The CTE materialises the anchored first value once, keeping the outer SELECT readable and avoiding repeated window calls.

## Q64: Write a query to compute the time between each website pageview and the next pageview in the same session using LEAD.

**Query:**
```sql
SELECT session_id,
       page,
       viewed_at,
       LEAD(viewed_at) OVER (PARTITION BY session_id ORDER BY viewed_at) AS next_view,
       EXTRACT(EPOCH FROM (
           LEAD(viewed_at) OVER (PARTITION BY session_id ORDER BY viewed_at) - viewed_at
       )) AS seconds_to_next
FROM pageviews;
```

**Explanation:** LEAD lines up successive pageviews inside each session; subtracting the timestamps yields dwell time per page.

**Alt1:** Self-join for the same dwell figure:
```sql
SELECT p.session_id,
       p.page,
       p.viewed_at,
       n.viewed_at - p.viewed_at AS seconds_to_next
FROM pageviews p
LEFT JOIN LATERAL (
    SELECT v.viewed_at
    FROM pageviews v
    WHERE v.session_id = p.session_id
      AND v.viewed_at > p.viewed_at
    ORDER BY v.viewed_at
    LIMIT 1
) n ON true;
```
The lateral lookup fetches the next timestamp explicitly; LEAD compresses the same work into one clause.

## Q65: Write a query to mark the first occurrence of each product in the sales log using a LAG null-test.

**Query:**
```sql
SELECT product_id,
       sale_ts,
       CASE WHEN LAG(product_id) OVER (ORDER BY sale_ts) = product_id
            THEN 'repeat' ELSE 'first_seen' END AS occurrence
FROM sales_log;
```

**Explanation:** If the preceding row's product differs (or is NULL), this is the first time the product appears in temporal order.

## Q66: Write a query to mark the last occurrence of each value in a partitioned sequence using LEAD.

**Query:**
```sql
SELECT product_id,
       sale_ts,
       status,
       CASE WHEN LEAD(status) OVER (PARTITION BY product_id ORDER BY sale_ts) = status
            THEN 'continues' ELSE 'last_in_run' END AS run_end
FROM inventory_events;
```

**Explanation:** A run ends where the next event of the same product no longer carries the same status; LEAD supplies that look-ahead value.

## Q67: Write a query to find the minimum and maximum salary in each department without GROUP BY, using FIRST_VALUE and LAST_VALUE on every row.

**Query:**
```sql
SELECT department_id,
       employee_id,
       salary,
       FIRST_VALUE(salary) OVER (PARTITION BY department_id ORDER BY salary) AS min_salary,
       LAST_VALUE(salary) OVER (PARTITION BY department_id ORDER BY salary
                                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS max_salary
FROM employees;
```

**Explanation:** Ordering the partitioned window by salary puts the minimum first and maximum last; both are exposed per row via the value functions.

## Q68: Write a query to show each employee with their hire date and the hire date of the employee hired immediately after them in the same department.

**Query:**
```sql
SELECT department_id,
       employee_id,
       hire_date,
       LEAD(hire_date) OVER (PARTITION BY department_id ORDER BY hire_date) AS next_hire_date
FROM employees;
```

**Explanation:** LEAD reads one row ahead in department/hire order, so the newest hire in each department has a NULL next hire date.

## Q69: Write a query to compute how long each session lasted by comparing every row to the session's first timestamp with FIRST_VALUE.

**Query:**
```sql
SELECT session_id,
       event_ts,
       EXTRACT(EPOCH FROM (event_ts -
           FIRST_VALUE(event_ts) OVER (PARTITION BY session_id ORDER BY event_ts))) / 60 AS minutes_since_session_start
FROM session_events;
```

**Explanation:** FIRST_VALUE anchors every row to the session's start time; each event is expressed as an elapsed offset, not just first/last rows.

## Q70: Write a query to reset a running day-count when a user's streak breaks, using LAG to detect the break and a SUM to number the segments.

**Query:**
```sql
SELECT user_id,
       active_date,
       SUM(is_break) OVER (PARTITION BY user_id ORDER BY active_date ROWS UNBOUNDED PRECEDING) AS streak_group
FROM (
    SELECT user_id,
           active_date,
           CASE WHEN active_date - LAG(active_date) OVER (PARTITION BY user_id ORDER BY active_date) = 1
                THEN 0 ELSE 1 END AS is_break
    FROM activity
) t;
```

**Explanation:** LAG tests whether the previous activity day was consecutive; each break increments a running group id, clustering separated streaks.

## Q71: Write a query to get the sale amount from three rows ahead using LEAD with an offset of 3.

**Query:**
```sql
SELECT sales_date,
       sales_amount,
       LEAD(sales_amount, 3) OVER (ORDER BY sales_date) AS amount_3_ahead
FROM daily_sales;
```

**Explanation:** LEAD skips forward three rows in time order, so the final three rows are NULL; offset is a simple positional hop, not a value match.

## Q72: Write a query to combine LAG and LEAD to flag local extrema (peaks and troughs) in a price series.

**Query:**
```sql
SELECT trade_date,
       close_price,
       LAG(close_price) OVER (ORDER BY trade_date)  AS prev_close,
       LEAD(close_price) OVER (ORDER BY trade_date) AS next_close,
       CASE WHEN close_price > LAG(close_price) OVER (ORDER BY trade_date)
            AND close_price > LEAD(close_price) OVER (ORDER BY trade_date) THEN 'peak'
            WHEN close_price < LAG(close_price) OVER (ORDER BY trade_date)
            AND close_price < LEAD(close_price) OVER (ORDER BY trade_date) THEN 'trough'
            ELSE 'trend' END AS point_type
FROM stock_daily;
```

**Explanation:** A peak is higher than both neighbours and a trough lower than both; LAG (past) and LEAD (future) together supply the neighbours.

**Alt1:** All four neighbours rebuilt via a self-join:
```sql
SELECT c.trade_date,
       c.close_price,
       CASE WHEN p.close_price IS NULL OR n.close_price IS NULL THEN 'edge'
            WHEN c.close_price > p.close_price AND c.close_price > n.close_price THEN 'peak'
            WHEN c.close_price < p.close_price AND c.close_price < n.close_price THEN 'trough'
            ELSE 'trend' END AS point_type
FROM stock_daily c
LEFT JOIN stock_daily p ON p.trade_date = c.trade_date - INTERVAL 1 DAY
LEFT JOIN stock_daily n ON n.trade_date = c.trade_date + INTERVAL 1 DAY;
```
Adjacent-day joins reproduce the LAG/LEAD neighbours under a contiguous-dates assumption.

## Q73: Write a query to show the previous, current, and next status for a state machine using one window each.

**Query:**
```sql
SELECT order_id,
       status_ts,
       status,
       LAG(status)  OVER (PARTITION BY order_id ORDER BY status_ts) AS prev_status,
       LEAD(status) OVER (PARTITION BY order_id ORDER BY status_ts) AS next_status
FROM order_status_log;
```

**Explanation:** LAG and LEAD on the same partition and order reconstruct the state-transition context around every status change.

## Q74: Write a query to return the order amount of the previous order on the same day for each order, using LAG over a timestamp.

**Query:**
```sql
SELECT order_id,
       customer_id,
       placed_at,
       order_amount,
       LAG(order_amount) OVER (PARTITION BY DATE(placed_at) ORDER BY placed_at) AS prev_same_day_amount
FROM orders;
```

**Explanation:** Partitioning by the calendar date isolates same-day ordering; LAG inside that window compares to the order placed immediately before on the same day.

## Q75: Write a query to compute the average lead time between consecutive shipments per warehouse using LEAD.

**Query:**
```sql
SELECT warehouse_id,
       shipment_id,
       shipped_at,
       LEAD(shipped_at) OVER (PARTITION BY warehouse_id ORDER BY shipped_at) AS next_shipment,
       AVG(DATEDIFF(LEAD(shipped_at) OVER (PARTITION BY warehouse_id ORDER BY shipped_at), shipped_at))
           OVER (PARTITION BY warehouse_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_avg_gap
FROM shipments;
```

**Explanation:** LEAD yields each inter-shipment gap, and a running AVG window accumulates those gaps per warehouse to track average cadence.

## Q76: Write a query that shows each month's revenue along with the first month's revenue in the partition and the difference, using FIRST_VALUE and comparing per row.

**Query:**
```sql
SELECT sales_month,
       monthly_revenue,
       FIRST_VALUE(monthly_revenue) OVER (ORDER BY sales_month) AS baseline_revenue,
       monthly_revenue - FIRST_VALUE(monthly_revenue) OVER (ORDER BY sales_month) AS growth_vs_baseline
FROM monthly_revenue;
```

**Explanation:** The frame defaults to `UNBOUNDED PRECEDING .. CURRENT ROW`, so FIRST_VALUE repeatedly returns the earliest month — the baseline every month is measured against.

## Q77: Write a query to compute the inter-quartile-style spread using NTH_VALUE: 25th, 50th, and 75th percentiles of salary per department.

**Query:**
```sql
SELECT department_id,
       NTH_VALUE(salary, 1) OVER w  AS pct_small,
       NTH_VALUE(salary, 5) OVER w  AS pct_25,
       NTH_VALUE(salary, 9) OVER w  AS pct_50,
       NTH_VALUE(salary, 13) OVER w AS pct_75
FROM employees
WINDOW w AS (PARTITION BY department_id ORDER BY salary
             ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING);
```

**Explanation:** NTH_VALUE plucks salaries at fixed ordinal positions of the salary-sorted partition, approximating distribution points without true percentile functions.

## Q78: Write a query to show the first and second person who signed up in each cohort of the same month.

**Query:**
```sql
SELECT cohort_month,
       user_id,
       signed_up_at,
       FIRST_VALUE(user_id) OVER (PARTITION BY cohort_month ORDER BY signed_up_at)  AS first_signer,
       NTH_VALUE(user_id, 2)   OVER (PARTITION BY cohort_month ORDER BY signed_up_at
                                     ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS second_signer
FROM users_growth
WINDOW w AS (PARTITION BY cohort_month ORDER BY signed_up_at);
```

**Explanation:** FIRST_VALUE names the earliest signer in each month-cohort while NTH_VALUE(…,2) names the next — note the second needs the full-partition frame.

## Q79: Write a query that computes, for every row, the value of the partition row five positions earlier using LAG with the offset derived from a column.

**Query:**
```sql
WITH params AS (SELECT 5 AS lag_offset)
SELECT t.reading_id,
       t.reading_value,
       LAG(t.reading_value, p.lag_offset) OVER (ORDER BY t.reading_id) AS value_n_back
FROM sensor_readings t
CROSS JOIN params p;
```

**Explanation:** Offsets can come from a parameter table: the join injects the constant into the LAG call, giving a tunable look-back distance.

## Q80: Write a query to detect sessions where a user was inactive for more than one hour between events using LEAD.

**Query:**
```sql
SELECT user_id,
       event_ts,
       next_event,
       gap_minutes
FROM (
    SELECT user_id,
           event_ts,
           LEAD(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts) AS next_event,
           EXTRACT(EPOCH FROM (LEAD(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts) - event_ts)) / 60 AS gap_minutes
    FROM user_events
) t
WHERE gap_minutes > 60;
```

**Explanation:** LEAD computes each user's inter-event gap; the outer query filters for gaps larger than 60 minutes to spotlight idle stretches.

## Q81: Write a query to verify whether a series of readings is monotonically non-decreasing using LAG.

**Query:**
```sql
SELECT CASE WHEN COUNT(*) = SUM(ok) THEN 'monotonic' ELSE 'breached' END AS series_check
FROM (
    SELECT CASE WHEN value >= LAG(value) OVER (ORDER BY reading_id) OR
                     LAG(value) OVER (ORDER BY reading_id) IS NULL THEN 1 ELSE 0 END AS ok
    FROM sensor_readings
) t;
```

**Explanation:** Every interior row must satisfy `value >= previous`; the first row is exempted via the NULL test, and a full count of OK rows confirms monotonicity.

## Q82: Write a query comparing each row with both the row 2 before and 2 after it, and flagging rows that are the largest in that local window using LAG and LEAD.

**Query:**
```sql
SELECT day,
       value,
       value >= COALESCE(LAG(value,1) OVER (ORDER BY day), value)
       AND value >= COALESCE(LAG(value,2) OVER (ORDER BY day), value)
       AND value >= COALESCE(LEAD(value,1) OVER (ORDER BY day), value)
       AND value >= COALESCE(LEAD(value,2) OVER (ORDER BY day), value) AS is_local_max
FROM measurements;
```

**Explanation:** Four neighbour values (two behind, two ahead) are gathered and tested; COALESCE substitutes the row itself at the series boundaries.

## Q83: Write a query to compute the duration between the first and last event of each type per user using FIRST_VALUE and LAST_VALUE.

**Query:**
```sql
SELECT user_id,
       event_type,
       FIRST_VALUE(event_ts) OVER (PARTITION BY user_id, event_type ORDER BY event_ts) AS first_seen,
       LAST_VALUE(event_ts) OVER (PARTITION BY user_id, event_type ORDER BY event_ts
                                  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_seen,
       EXTRACT(EPOCH FROM (
           LAST_VALUE(event_ts) OVER (PARTITION BY user_id, event_type ORDER BY event_ts
                                      ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
           - FIRST_VALUE(event_ts) OVER (PARTITION BY user_id, event_type ORDER BY event_ts))) AS span_seconds
FROM user_events;
```

**Explanation:** Partitioning on both user and event type frames each value function to a specific behaviour; the span is the first-to-last difference.

## Q84: Write a query to show the current salary, the salary 1 change back, and salary 2 changes back for each employee using a CTE to avoid repeating LAG clauses.

**Query:**
```sql
WITH changes AS (
    SELECT employee_id,
           salary_date,
           salary,
           LAG(salary, 1) OVER (PARTITION BY employee_id ORDER BY salary_date) AS salary_prev1,
           LAG(salary, 2) OVER (PARTITION BY employee_id ORDER BY salary_date) AS salary_prev2
    FROM salary_history
)
SELECT employee_id,
       salary_date,
       salary,
       salary_prev1,
       salary_prev2,
       salary - COALESCE(salary_prev1, salary) AS change_vs_last
FROM changes
ORDER BY employee_id, salary_date;
```

**Explanation:** The CTE computes both LAG columns once; the outer query references them cleanly and derives the delta with a defensive COALESCE.

## Q85: Write a query that finds customers who placed two orders within 7 days, using LAG to inspect the prior order date.

**Query:**
```sql
SELECT DISTINCT customer_id
FROM (
    SELECT customer_id,
           order_date,
           LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order_date
    FROM orders
) t
WHERE DATEDIFF(order_date, prev_order_date) <= 7;
```

**Explanation:** LAG surfaces each order's predecessor; a DATEDIFF of seven days or less identifies fast-repeat buyers, deduplicated across all qualifying pairs.

## Q86: Write a query to keep the LAST_VALUE up to the current row (a monotonic maximum) versus reaching the partition end, demonstrating both frames in one query.

**Query:**
```sql
SELECT day,
       price,
       LAST_VALUE(price) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_last,
       LAST_VALUE(price) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS final_price
FROM commodity_prices;
```

**Explanation:** The `CURRENT ROW` frame freezes LAST_VALUE at each row in time (running value), while the unbounded-following frame reads the terminal price everywhere.

## Q87: Write a query to return, for every product, the price at the 10th recorded date using NTH_VALUE over an offset ordered by date.

**Query:**
```sql
SELECT product_id,
       record_date,
       price,
       NTH_VALUE(price, 10) OVER (
           PARTITION BY product_id ORDER BY record_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS price_10th_record
FROM product_records;
```

**Explanation:** The tenth row of the date-ordered product partition supplies the anchor price; products with fewer than 10 records yield NULL.

## Q88: Write a query to compute the difference between consecutive days' values normalized by the earlier value (percentage return), using LAG in a CTE.

**Query:**
```sql
WITH prices AS (
    SELECT trade_date,
           close_price,
           LAG(close_price) OVER (ORDER BY trade_date) AS prev_close
    FROM asset_daily
)
SELECT trade_date,
       close_price,
       ROUND((close_price - prev_close) * 100.0 / prev_close, 2) AS return_pct
FROM prices
ORDER BY trade_date;
```

**Explanation:** Materialising LAG in the CTE keeps the percentage formula readable and computed exactly once per row.

## Q89: Write a query to show the first and last day a product was available in each store partnership using FIRST/LAST_VALUE.

**Query:**
```sql
SELECT store_id,
       product_id,
       priced_at,
       FIRST_VALUE(priced_at) OVER (PARTITION BY store_id, product_id ORDER BY priced_at) AS first_available,
       LAST_VALUE(priced_at) OVER (PARTITION BY store_id, product_id ORDER BY priced_at
                                   ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_available
FROM store_product_prices;
```

**Explanation:** Each store–product pair becomes a partition; the value functions expose the listing's first and last pricing dates on every row.

## Q90: Write a query that labels each sale with how many days something was 'open' before the next sale in that category, using LEAD.

**Query:**
```sql
SELECT category_id,
       sale_date,
       sale_amount,
       LEAD(sale_date) OVER (PARTITION BY category_id ORDER BY sale_date) AS next_sale_date,
       DATEDIFF(LEAD(sale_date) OVER (PARTITION BY category_id ORDER BY sale_date), sale_date) AS days_until_next_sale
FROM promo_sales;
```

**Explanation:** LEAD looks up the next sale within the category; the DATEDIFF quantifies the quiet period each sale precedes.

## Q91: Write a query to compute a forward-looking sum of three future readings per sensor using LEAD three times.

**Query:**
```sql
SELECT sensor_id,
       reading_ts,
       reading_value,
       COALESCE(LEAD(reading_value,1) OVER (PARTITION BY sensor_id ORDER BY reading_ts), 0)
         + COALESCE(LEAD(reading_value,2) OVER (PARTITION BY sensor_id ORDER BY reading_ts), 0)
         + COALESCE(LEAD(reading_value,3) OVER (PARTITION BY sensor_id ORDER BY reading_ts), 0) AS next3_total
FROM sensor_log;
```

**Explanation:** Three LEAD calls with growing offsets gather the next three values; COALESCE(…0) keeps the trailing rows finite.

## Q92: Write a query that converts the LAST_VALUE column to a true "current value" reached so far, comparing first and last rows of the frame.

**Query:**
```sql
SELECT day,
       balance,
       FIRST_VALUE(balance) OVER (ORDER BY day) AS starting_balance,
       LAST_VALUE(balance) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance_to_date
FROM account_balances;
```

**Explanation:** `UNBOUNDED PRECEDING .. CURRENT ROW` makes LAST_VALUE report the updated balance as of each day — a running snapshot, not a partition-final static.

## Q93: Write a query to label each event as 'new' if it introduces a value never seen before among the previous rows, using LAG and a gap test.

**Query:**
```sql
SELECT value,
       seen_at,
       CASE WHEN value <> LAG(value) OVER (ORDER BY seen_at, value) THEN 'new_value' ELSE 'same' END AS first_appearance
FROM event_stream;
```

**Explanation:** When sorted by seen_at and value, an equal neighbour means no change; any difference (or NULL) flags a new value in temporal order.

## Q94: Write a query to show each order with its value, the customer's previous order value, and the delta, using LAG within a derived table to allow a WHERE filter on the delta.

**Query:**
```sql
SELECT *
FROM (
    SELECT order_id,
           customer_id,
           order_value,
           LAG(order_value) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_value
    FROM orders
) t
WHERE order_value - prev_value > 100;
```

**Explanation:** The inner LAG is unavoidable inside WHERE, so a derived table exposes it to the outer predicate that selects large jumps.

## Q95: Write a query to compute the previous distinct specialty per doctor from appointment history using LAG.

**Query:**
```sql
SELECT doctor_id,
       appointment_date,
       specialty,
       LAG(specialty) OVER (PARTITION BY doctor_id ORDER BY appointment_date) AS prior_specialty
FROM appointments;
```

**Explanation:** Partitioning by doctor and ordering by date returns the specialty from the immediately preceding appointment booked with the same doctor.

## Q96: Write a query to compare each product's weekly revenue against both the previous week and the same product's first week using LAG and FIRST_VALUE.

**Query:**
```sql
SELECT product_id,
       date_trunc('week', sale_date) AS sale_week,
       SUM(revenue) AS weekly_revenue,
       LAG(SUM(revenue)) OVER (PARTITION BY product_id ORDER BY date_trunc('week', sale_date)) AS prev_week_rev,
       FIRST_VALUE(SUM(revenue)) OVER (PARTITION BY product_id ORDER BY date_trunc('week', sale_date)) AS first_week_rev
FROM revenue
GROUP BY product_id, date_trunc('week', sale_date);
```

**Explanation:** The same grouped window supports LAG (last week) and FIRST_VALUE (launch week), letting you compare each product against both reference points.

## Q97: Write a query to show the daily price and the price from exactly one month earlier using LAG, on data aggregated at month level.

**Query:**
```sql
SELECT product_id,
       snapshot_month,
       avg_price,
       LAG(avg_price) OVER (PARTITION BY product_id ORDER BY snapshot_month) AS prev_month_price,
       avg_price - LAG(avg_price) OVER (PARTITION BY product_id ORDER BY snapshot_month) AS mom_diff
FROM monthly_prices;
```

**Explanation:** Monthly aggregation followed by a LAG over the ordered month partition reproduces a month-over-month price movement series.

## Q98: Write a query to find the highest and second-highest paying jobs using FIRST_VALUE and NTH_VALUE across all employees.

**Query:**
```sql
SELECT FIRST_VALUE(job_title) OVER (w ORDER BY salary DESC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS top_job,
       NTH_VALUE(job_title, 2) OVER (w ORDER BY salary DESC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS second_top_job
FROM employees_all
WINDOW w AS ();
```

**Explanation:** With no partition the whole table is one window; ordering by salary descending lets FIRST_VALUE and NTH_VALUE name the two best-paid jobs.

## Q99: Write a query combining LAG, LEAD, FIRST_VALUE and LAST_VALUE to build a deviation report showing current, prior, next, first, and last readings.

**Query:**
```sql
SELECT meter_id,
       reading_ts,
       reading_value,
       LAG(reading_value)  OVER (PARTITION BY meter_id ORDER BY reading_ts) AS prev_reading,
       LEAD(reading_value) OVER (PARTITION BY meter_id ORDER BY reading_ts) AS next_reading,
       FIRST_VALUE(reading_value) OVER (PARTITION BY meter_id ORDER BY reading_ts) AS first_reading,
       LAST_VALUE(reading_value) OVER (PARTITION BY meter_id ORDER BY reading_ts
                                      ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_reading,
       reading_value - FIRST_VALUE(reading_value) OVER (PARTITION BY meter_id ORDER BY reading_ts) AS deviation_from_first
FROM meter_log;
```

**Explanation:** All four value functions work over the same per-meter time window, giving a complete neighbourhood plus partition anchors on each row.

## Q100: Write a complex query that finds, for every sale, the previous sale of the same customer and the customer's very first sale, then returns only sales that beat both.

**Query:**
```sql
WITH enriched AS (
    SELECT o.order_id,
           o.customer_id,
           o.order_date,
           o.order_amount,
           LAG(o.order_amount) OVER (PARTITION BY o.customer_id ORDER BY o.order_date) AS prev_amount,
           FIRST_VALUE(o.order_amount) OVER (PARTITION BY o.customer_id ORDER BY o.order_date
                                             ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS first_amount
    FROM orders o
)
SELECT customer_id,
       order_id,
       order_date,
       order_amount,
       prev_amount,
       first_amount,
       ROUND((order_amount - prev_amount) * 100.0 / prev_amount, 2) AS pct_vs_prev
FROM enriched
WHERE order_amount > prev_amount
  AND order_amount > first_amount
  AND prev_amount IS NOT NULL
ORDER BY customer_id, order_date;
```

**Explanation:** LAG supplies the immediate predecessor, FIRST_VALUE the partition's inaugural sale; the record must outpace both. This combines the file's running patterns — offsets, partition anchoring, CTEs, flags, and deltas — into one decisive filter.

**Alt1:** The same answer in pure SQL Server over Oracle dialect highlights portability; only the FIRST_VALUE partition anchor and LAG offset live on the window clause:
```sql
-- SQL Server / Azure SQL
WITH enriched AS (
    SELECT o.order_id,
           o.customer_id,
           o.order_date,
           o.order_amount,
           LAG(o.order_amount) OVER (PARTITION BY o.customer_id ORDER BY o.order_date) AS prev_amount,
           FIRST_VALUE(o.order_amount) OVER (PARTITION BY o.customer_id ORDER BY o.order_date
                                             ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS first_amount
    FROM orders o
)
SELECT customer_id,
       order_id,
       order_amount
FROM enriched
WHERE order_amount > prev_amount
  AND order_amount > first_amount
  AND prev_amount IS NOT NULL;
```
The dialect differences collapse to type casting and casting of NULL ordering rules; the window logic itself is unchanged across MySQL 8+, PostgreSQL, SQL Server, and Oracle.
