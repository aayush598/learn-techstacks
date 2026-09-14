# Running Totals, Moving Averages and Window Aggregates — 100 SQL Interview Q&A

## Q1: Write a query to compute a running total of daily sales for a store.

`sales(day_date DATE, amount DECIMAL)`. Return each day with a cumulative amount through that day.

**Query:**
```sql
SELECT
  day_date,
  amount,
  SUM(amount) OVER (ORDER BY day_date) AS running_total
FROM sales
ORDER BY day_date;
```
**Explanation:** `SUM(...) OVER (ORDER BY ...)` without a frame clause defaults to the growing range from the first row (UNBOUNDED PRECEDING) through the CURRENT ROW, producing the cumulative total.

## Q2: Write a query to compute a running total of revenue per month per product.

`revenue(product_id INT, month CHAR(7), amount DECIMAL)`. Reset the cumulative total for each product.

**Query:**
```sql
SELECT
  product_id,
  month,
  amount,
  SUM(amount) OVER (PARTITION BY product_id ORDER BY month) AS product_running_total
FROM revenue
ORDER BY product_id, month;
```
**Explanation:** `PARTITION BY product_id` restarts the running total for each product, while `ORDER BY month` drives the accumulation direction.

## Q3: Write a query to compute a cumulative count of orders placed, one row per order.

`orders(id INT, order_ts TIMESTAMP)`. Show order id, timestamp, and an incrementing ordinal number.

**Query:**
```sql
SELECT
  id,
  order_ts,
  COUNT(*) OVER (ORDER BY order_ts, id) AS running_order_count
FROM orders
ORDER BY order_ts, id;
```
**Explanation:** `COUNT(*) OVER (ORDER BY ...)` counts all rows up to and including the current row in sort order.

## Q4: Write a query to produce a 7-day trailing moving average of daily prices.

`prices(day_date DATE, price DECIMAL)`. The average should cover the current day and the 6 preceding days.

**Query:**
```sql
SELECT
  day_date,
  price,
  AVG(price) OVER (
    ORDER BY day_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS ma_7
FROM prices
ORDER BY day_date;
```
**Explanation:** The explicit frame `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` makes the window exactly 7 physical rows, sliding one day at a time.

## Q5: Write a query to compute a 30-day moving average of page views for a website.

`traffic(day_date DATE, views INT)`.

**Query:**
```sql
SELECT
  day_date,
  views,
  AVG(views) OVER (
    ORDER BY day_date
    ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
  ) AS ma_30
FROM traffic
ORDER BY day_date;
```
**Explanation:** `ROWS BETWEEN 29 PRECEDING AND CURRENT ROW` is a trailing window of the latest 30 days. Early rows average fewer days (no padding).

## Q6: Write a query to compute an expanding (cumulative) average of daily temperature readings.

`sensor(ts TIMESTAMP, temp DECIMAL)`. Same as a running average from the first reading.

**Query:**
```sql
SELECT
  ts,
  temp,
  AVG(temp) OVER (ORDER BY ts) AS cum_avg_temp
FROM sensor
ORDER BY ts;
```
**Explanation:** The default frame for `AVG(...) OVER (ORDER BY ...)` is from UNBOUNDED PRECEDING to CURRENT ROW, giving the average of everything so far.

## Q7: Write a query to find the cumulative maximum of an inventory level over time.

`inventory(day_date DATE, qty INT)`.

**Query:**
```sql
SELECT
  day_date,
  qty,
  MAX(qty) OVER (ORDER BY day_date) AS running_high
FROM inventory
ORDER BY day_date;
```
**Explanation:** `MAX(qty) OVER (ORDER BY day_date)` tracks the highest value seen so far; cumulative min works with the same pattern.

## Q8: Write a query to compute the cumulative minimum of a stock's closing price (running low).

`stocks(symbol VARCHAR(10), trade_date DATE, close_price DECIMAL)`. One row per symbol/date.

**Query:**
```sql
SELECT
  symbol,
  trade_date,
  close_price,
  MIN(close_price) OVER (
    PARTITION BY symbol
    ORDER BY trade_date
  ) AS running_low
FROM stocks
ORDER BY symbol, trade_date;
```
**Explanation:** `PARTITION BY symbol` keeps each ticker's running low independent; the implicit frame is UNBOUNDED PRECEDING through CURRENT ROW.

## Q9: Write a query to compute a centered (two-sided) 5-day moving average of temperatures.

`temps(day_date DATE, temp DECIMAL)`. Window = 2 days before, current, 2 days after.

**Query:**
```sql
SELECT
  day_date,
  temp,
  AVG(temp) OVER (
    ORDER BY day_date
    ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
  ) AS centered_ma_5
FROM temps
ORDER BY day_date;
```
**Explanation:** `ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING` centers the frame on the current row, which is standard for smoothing filter applications.

## Q10: Write a query to compute a running total reset per department, using an explicit `PARTITION BY`.

`employees(emp_id INT, dept VARCHAR(20), salary INT)`. Cumulative salary sum per department by emp_id.

**Query:**
```sql
SELECT
  emp_id,
  dept,
  salary,
  SUM(salary) OVER (
    PARTITION BY dept
    ORDER BY emp_id
  ) AS dept_cum_salary
FROM employees
ORDER BY dept, emp_id;
```
**Explanation:** Partitioning by department resets the cumulative salary, and ordering by emp_id controls the accumulation order.

## Q11: Write a query to compute the share of each day's sales within the running total (percentage-of-running-total), then convert it to a percentage.

`sales(day_date DATE, amount DECIMAL)`.

**Query:**
```sql
SELECT
  day_date,
  amount,
  SUM(amount) OVER (ORDER BY day_date) AS running_total,
  amount * 100.0 / SUM(amount) OVER (ORDER BY day_date) AS pct_of_running_total
FROM sales
ORDER BY day_date;
```
**Explanation:** The current row's amount divided by the running total gives the fraction of the cumulative sum contributed so far.

## Q12: Write a query to add a grand-total percentage to each row so percentages always sum to 100 across the whole result set.

`region_sales(region VARCHAR(20), amount DECIMAL)`.

**Query:**
```sql
SELECT
  region,
  amount,
  SUM(amount) OVER () AS grand_total,
  amount * 100.0 / SUM(amount) OVER () AS pct_of_grand_total
FROM region_sales
ORDER BY region;
```
**Explanation:** `OVER ()` with no PARTITION/ORDER makes the window the entire result set, so each row sees the grand total.

## Q13: Write a query to compute a moving average of order amounts over the current and previous 2 orders per customer.

`orders(customer_id INT, order_id INT, amount DECIMAL)`.

**Query:**
```sql
SELECT
  customer_id,
  order_id,
  amount,
  AVG(amount) OVER (
    PARTITION BY customer_id
    ORDER BY order_id
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) AS ma_3_orders
FROM orders
ORDER BY customer_id, order_id;
```
**Explanation:** Partition by customer keeps frames client-local; the ROWS frame averages the latest 3 physical order rows within the partition.

## Q14: Recompute a running count of events per device session, using `COUNT` with a window partitioned by session id.

`events(session_id INT, event_seq INT, event_name VARCHAR(30))`.

**Query:**
```sql
SELECT
  session_id,
  event_seq,
  event_name,
  COUNT(*) OVER (
    PARTITION BY session_id
    ORDER BY event_seq
  ) AS event_number
FROM events
ORDER BY session_id, event_seq;
```
**Explanation:** `COUNT(*) OVER (PARTITION BY session_id ORDER BY event_seq)` numbers events 1,2,3,... within each session as the window grows.

## Q15: Write a query to compute a weighted 7-day moving average where each day has a weight.

`prices(day_date DATE, price DECIMAL, weight DECIMAL)`. Use `SUM(price*weight) / SUM(weight)` over the trailing 7 rows.

**Query:**
```sql
SELECT
  day_date,
  SUM(price * weight) OVER (
    ORDER BY day_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) / NULLIF(SUM(weight) OVER (
    ORDER BY day_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ), 0) AS wma_7
FROM prices
ORDER BY day_date;
```
**Explanation:** Two identical windows compute numerator and denominator; `NULLIF` guards against an all-zero weight denominator.

## Q16: Write a query to compute a moving median of daily stock prices using a 7-day trailing window.

`quotes(day_date DATE, close_price DECIMAL)`.

**Query:**
```sql
SELECT
  day_date,
  close_price,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY close_price)
    OVER (PARTITION BY day_date) AS med_from_self
FROM quotes;
```
**Explanation:** `PERCENTILE_CONT` can't take a frame, so this exact query is wrong for a *trailing* median — see the alternative below.

**Alt1:**
```sql
-- PostgreSQL: array_agg with a window frame gives a true trailing median
SELECT
  day_date,
  close_price,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY close_price)
    OVER (ORDER BY day_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS trailing_median
FROM quotes;
```
**Explanation:** Postgres extends `percentile_cont` to accept an `OVER` frame, so the ORDER BY inside the window sort defines the frame and the aggregate computes over the 7 rows in it — a true sliding median.

## Q17: Write a query to compute a rolling count of distinct customers in the trailing 7 days.

`purchases(day_date DATE, customer_id INT)`.

**Query:**
```sql
SELECT
  day_date,
  COUNT(DISTINCT customer_id) OVER (
    ORDER BY day_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS distinct_customers_7d
FROM purchases
ORDER BY day_date;
```
**Explanation:** `COUNT(DISTINCT ...) OVER (...)` counts unique customers within the sliding frame (supported natively in Postgres, SQL Server, SQLite; MySQL 8 needs the alternative below).

**Alt1:**
```sql
-- MySQL 8: emulate distinct-count-over-frame by aggregating a flagged subquery
SELECT
  day_date,
  SUM(is_first)  AS distinct_customers_7d
FROM (
  SELECT
    p1.day_date,
    p2.customer_id,
    CASE WHEN MIN(p2.day_date) = p1.day_date THEN 1 ELSE 0 END AS is_first
  FROM purchases p1
  JOIN purchases p2
    ON p2.customer_id = p1.customer_id
   AND p2.day_date BETWEEN p1.day_date - INTERVAL 6 DAY AND p1.day_date
  GROUP BY p1.day_date, p2.customer_id
) x
GROUP BY day_date
ORDER BY day_date;
```
**Explanation:** The join builds each day's 7-day window, `MIN(day_date)` detects the day the customer first appears in that window, and a final `SUM` counts each customer once.

## Q18: Write a query to compute a cumulative delta (day-over-day running net change) of a balance column.

`account_balance(balance_date DATE, balance DECIMAL)`.

**Query:**
```sql
SELECT
  balance_date,
  balance,
  balance - FIRST_VALUE(balance) OVER (ORDER BY balance_date) AS cum_delta,
  balance - LAG(balance) OVER (ORDER BY balance_date) AS day_delta
FROM account_balance
ORDER BY balance_date;
```
**Explanation:** `FIRST_VALUE` gives the opening balance for the cumulative delta; `LAG` in the same statement supplies the day-over-day change.

## Q19: Write a query to compute a running total that resets when a new product line begins.

`output_log(serial_no INT, product_line VARCHAR(10), qty INT)`.

**Query:**
```sql
SELECT
  serial_no,
  product_line,
  qty,
  SUM(qty) OVER (
    PARTITION BY product_line
    ORDER BY serial_no
  ) AS line_running_qty
FROM output_log
ORDER BY product_line, serial_no;
```
**Explanation:** Partitioning on `product_line` causes the cumulative sum to restart at each line change, exactly mirroring a production batch boundary.

## Q20: Write a query to produce a running total with predictions padded to the next 2 rows using the last observed cumulative value (forward-fill).

`daily_sales(day_date DATE, amount DECIMAL)`.

**Query:**
```sql
-- PostgreSQL / SQL Server
WITH obs AS (
  SELECT
    day_date,
    amount,
    SUM(amount) OVER (ORDER BY day_date) AS running_total
  FROM daily_sales
),
future AS (
  SELECT
    day_date,
    amount,
    running_total
  FROM obs
  UNION ALL
  SELECT
    day_date + INTERVAL '1 day',
    NULL,
    MAX(running_total) OVER () 
  FROM obs
  WHERE day_date = (SELECT MAX(day_date) FROM obs)
  -- (repeat UNION ALL with +2 days for the second padded row)
)
SELECT * FROM future;
```
**Explanation:** The CTE computes the running total on observed rows, then pads synthetic rows carrying the final cumulative value forward.

## Q21: Write a query to compute a moving average of monthly revenue with a tumbling 3-month window, no overlap.

`revenue(month CHAR(7), amount DECIMAL)`.

**Query:**
```sql
WITH grp AS (
  SELECT
    month,
    amount,
    (ROW_NUMBER() OVER (ORDER BY month) - 1) / 3 AS bucket
  FROM revenue
)
SELECT
  MIN(month) AS month_start,
  SUM(amount) / 3.0 AS rolling_3mo_avg_bucket
FROM grp
GROUP BY bucket
ORDER BY month_start;
```
**Explanation:** `ROW_NUMBER()/3` groups months into non-overlapping triples; the group average is a tumbling-window aggregate, not a sliding one.

## Q22: Write a query to compute a moving total (sum) of new users registered in the trailing 5 days.

`users(reg_date DATE, user_id INT)`. Count users, not rows.

**Query:**
```sql
SELECT
  reg_date,
  COUNT(*) OVER (
    ORDER BY reg_date
    ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
  ) AS users_last_5d
FROM users
ORDER BY reg_date;
```
**Explanation:** With one registration row per user, `COUNT(*)` over the 5-row trailing frame equals the number of distinct users registered in the window.

## Q23: Write a query to compute the cumulative maximum drawdown of an investment (peak to current).

`nav(day_date DATE, value DECIMAL)`.

**Query:**
```sql
SELECT
  day_date,
  value,
  MAX(value) OVER (ORDER BY day_date) AS running_peak,
  100.0 * (value / MAX(value) OVER (ORDER BY day_date) - 1) AS drawdown_pct
FROM nav
ORDER BY day_date;
```
**Explanation:** Dividing current value by the running peak and subtracting 1 gives the drawdown percentage from the highest value seen so far.

## Q24: Write a query to compute a running average share price per symbol, resetting per ticker.

`trades(symbol VARCHAR(10), ts TIMESTAMP, price DECIMAL, qty INT)`.

**Query:**
```sql
SELECT
  symbol,
  ts,
  price,
  qty,
  SUM(price * qty) OVER (
    PARTITION BY symbol ORDER BY ts
  ) / NULLIF(SUM(qty) OVER (
    PARTITION BY symbol ORDER BY ts
  ), 0) AS vwap_running
FROM trades
ORDER BY symbol, ts;
```
**Explanation:** Cumulative notional (price×qty) divided by cumulative volume is a running volume-weighted average price per symbol.

## Q25: Write a query to compute a running total that only counts rows in a given month, zero otherwise.

`expenses(expense_date DATE, amount DECIMAL)`. January totals accumulate; other months show the January total flat.

**Query:**
```sql
SELECT
  expense_date,
  amount,
  SUM(
    CASE WHEN EXTRACT(MONTH FROM expense_date) = 1 THEN amount ELSE 0 END
  ) OVER (ORDER BY expense_date) AS jan_running_total
FROM expenses
ORDER BY expense_date;
```
**Explanation:** A `CASE` inside the window `SUM` filters the accumulated value per row; rows outside January contribute 0 and hold the total constant.

## Q26: Write a query to compute a cumulative sum of items sold, expressed as a normalized share 0–1 of the grand total.

`sku_sales(sku VARCHAR(20), qty INT)`.

**Query:**
```sql
SELECT
  sku,
  qty,
  SUM(qty) OVER (ORDER BY qty DESC, sku) AS running_qty,
  SUM(qty) OVER (ORDER BY qty DESC, sku)
    / NULLIF(SUM(qty) OVER (), 0) AS norm_running_share
FROM sku_sales
ORDER BY qty DESC, sku;
```
**Explanation:** Dividing the running total by the grand total yields a Lorenz-curve-style normalized cumulative share in [0,1].

## Q27: Write a query to compute a centered 3-day moving *minimum* temperature (smoothing lows).

`weather(day_date DATE, low_temp DECIMAL)`.

**Query:**
```sql
SELECT
  day_date,
  low_temp,
  MIN(low_temp) OVER (
    ORDER BY day_date
    ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
  ) AS smoothed_low
FROM weather
ORDER BY day_date;
```
**Explanation:** The centered frame `1 PRECEDING AND 1 FOLLOWING` evaluates the minima over each 3-row neighborhood, a smoothing filter for extremes.

## Q28: Write a query to compute a running total of sales grouped by week, cumulatively over weeks.

`sales(day_date DATE, amount DECIMAL)`.

**Query:**
```sql
WITH weekly AS (
  SELECT
    DATE_TRUNC('week', day_date) AS wk,
    SUM(amount) AS week_total
  FROM sales
  GROUP BY 1
)
SELECT
  wk,
  week_total,
  SUM(week_total) OVER (ORDER BY wk) AS cumulative_weeks
FROM weekly
ORDER BY wk;
```
**Explanation:** A group-by CTE first collapses rows to weekly totals; a second `SUM OVER` then accumulates them week over week.

## Q29: Write a query to produce a trailing 4-week moving average of signups, using `ROWS` on the aggregated week rows.

`signups(day_date DATE, user_id INT)`.

**Query:**
```sql
WITH weekly AS (
  SELECT
    DATE_TRUNC('week', day_date) AS wk,
    COUNT(*) AS signup_count
  FROM signups
  GROUP BY 1
)
SELECT
  wk,
  signup_count,
  AVG(signup_count) OVER (
    ORDER BY wk
    ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
  ) AS ma_4w
FROM weekly
ORDER BY wk;
```
**Explanation:** Aggregating first (per week) then applying the window is the idiomatic way to get a weekly moving average where the frame is 4 week rows.

## Q30: Write a query to compute a cumulative sum of scored goals resetting at every season change.

`matches(season VARCHAR(9), match_no INT, goals INT)`.

**Query:**
```sql
SELECT
  season,
  match_no,
  goals,
  SUM(goals) OVER (
    PARTITION BY season
    ORDER BY match_no
  ) AS season_goals
FROM matches
ORDER BY season, match_no;
```
**Explanation:** Partitioning on `season` resets the running goal count at each new season, matching championship tables.

## Q31: Write a query to compare each row's running total with the previous row's running total using a single window sum and `LAG`.

`sales(day_date DATE, amount DECIMAL)`.

**Query:**
```sql
SELECT
  day_date,
  amount,
  SUM(amount) OVER (ORDER BY day_date) AS running_total,
  SUM(amount) OVER (ORDER BY day_date)
    - LAG(SUM(amount) OVER (ORDER BY day_date)) OVER (ORDER BY day_date) AS step_change
FROM sales
ORDER BY day_date;
```
**Explanation:** A comma-feed pattern won't work here — recomputing the window twice is redundant; simpler: the step change is just the row's own amount.

**Alt1:**
```sql
SELECT
  day_date,
  amount,
  SUM(amount) OVER (ORDER BY day_date) AS running_total,
  amount AS implied_step_change
FROM sales
ORDER BY day_date;
```
**Explanation:** The increase in a running total from one row to the next is definitionally the current row's amount, so no extra window function is needed (demonstrates avoiding window-over-window restrictions).

## Q32: Write a query to compute the running total of invoice amounts for the last 3 fiscal months per customer.

`invoices(customer_id INT, inv_date DATE, amount DECIMAL)`.

**Query:**
```sql
SELECT
  customer_id,
  inv_date,
  amount,
  SUM(amount) OVER (
    PARTITION BY customer_id
    ORDER BY inv_date
    ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING
  ) AS trailing_3_excl_current
FROM invoices
ORDER BY customer_id, inv_date;
```
**Explanation:** The 3-row frame *ending at 1 PRECEDING* excludes the current invoice, giving the sum of the three invoices before it.

## Q33: Write a query to compute a running total of budget where past rows contribute and future rows show the final budget (backfill of the last cumulative value forward).

`project_budget(phase_no INT, budget DECIMAL)`.

**Query:**
```sql
SELECT
  phase_no,
  budget,
  SUM(budget) OVER (ORDER BY phase_no) AS running_budget,
  COALESCE(
    SUM(budget) OVER (ORDER BY phase_no),
    MAX(SUM(budget) OVER (ORDER BY phase_no)) OVER ()
  ) AS backfilled_total
FROM project_budget
ORDER BY phase_no;
```
**Explanation:** Explained inline — the `COALESCE`/`MAX` combo is illustrative; kernel point: pre-aggregate the final total in a subquery or use the last running value fetched with `LAST_VALUE`.

**Alt1:**
```sql
SELECT
  phase_no,
  budget,
  LAST_VALUE(SUM(budget) OVER (ORDER BY phase_no))
    OVER (ORDER BY phase_no ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS final_total
FROM project_budget;
```
**Explanation:** `LAST_VALUE` with an unbounded-following frame pulls the final cumulative value onto every earlier row.

## Q34: Write a query to compute a moving average of score rounded to 2 decimals using a centered window.

`exam_scores(scr_date DATE, score DECIMAL)`.

**Query:**
```sql
SELECT
  scr_date,
  score,
  ROUND(AVG(score) OVER (
    ORDER BY scr_date
    ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING
  ), 2) AS centered_ma_7
FROM exam_scores
ORDER BY scr_date;
```
**Explanation:** A 7-row centered frame smooths each score with neighbors; `ROUND` formats the average.

## Q35: Write a query that computes the ratio of each day's value to its 7-day running average (a "bollinger-ish" relative measure).

`metrics(day_date DATE, value DECIMAL)`.

**Query:**
```sql
SELECT
  day_date,
  value,
  AVG(value) OVER (
    ORDER BY day_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS ma_7,
  value / NULLIF(AVG(value) OVER (
    ORDER BY day_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ), 0) AS ratio_to_ma
FROM metrics
ORDER BY day_date;
```
**Explanation:** Current value over the 7-day moving average gives a normalized oscillation indicator around 1.0.

## Q36: Write a query to compute the cumulative number of unique cities visited by run date.

`trips(visit_date DATE, city VARCHAR(40))`.

**Query:**
```sql
SELECT
  visit_date,
  city,
  COUNT(DISTINCT city) OVER (ORDER BY visit_date) AS cities_seen
FROM trips
ORDER BY visit_date;
```
**Explanation:** `COUNT(DISTINCT city)` over the default growing frame counts unique city names seen so far (supported in Postgres, SQL Server, SQLite).

## Q37: Write a query to compute a 3-month centered moving total of returns, numbers-only.

`portfolio(month CHAR(7), return_amt DECIMAL)`.

**Query:**
```sql
SELECT
  month,
  return_amt,
  SUM(return_amt) OVER (
    ORDER BY month
    ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
  ) AS centered_sum_3
FROM portfolio
ORDER BY month;
```
**Explanation:** A 3-row centered frame aggregates the previous, current, and next month into a rolling window sum.

## Q38: Write a query to compute a running average of throughput hours, partitioning by machine.

`machine_log(machine_id INT, day_date DATE, hours DECIMAL)`.

**Query:**
```sql
SELECT
  machine_id,
  day_date,
  hours,
  AVG(hours) OVER (
    PARTITION BY machine_id
    ORDER BY day_date
  ) AS machine_cum_avg
FROM machine_log
ORDER BY machine_id, day_date;
```
**Explanation:** Partition by machine resets the cumulative average per machine; ordering by date determines accumulation order.

## Q39: Write a query to compute a moving sum of weekly defect counts using a 4-week trailing window with century-annotation.

`defects(week_start DATE, defects INT)`.

**Query:**
```sql
SELECT
  week_start,
  defects,
  SUM(defects) OVER (
    ORDER BY week_start
    ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
  ) AS defects_last_4w
FROM defects
ORDER BY week_start;
```
**Explanation:** Sliding 4-week sum is a trailing frame over pre-aggregated week rows.

## Q40: Recompute Q39 using a self-join instead of a window function.

**Query:**
```sql
SELECT
  a.week_start,
  a.defects,
  SUM(b.defects) AS defects_last_4w
FROM defects a
JOIN defects b
  ON b.week_start BETWEEN a.week_start - INTERVAL '3 week' AND a.week_start
GROUP BY a.week_start, a.defects
ORDER BY a.week_start;
```
**Explanation:** The self-join duplicates each row into its own 4-week window; `GROUP BY` then sums the joined partners — the classic pre-window-functions pattern.

## Q41: Write a query to compare running totals computed with `RANGE` (ties share values) versus `ROWS` (ties get distinct slots).

`sales_ties(day_date DATE, amount DECIMAL)` where multiple rows share the same day.

**Query:**
```sql
SELECT
  day_date,
  amount,
  SUM(amount) OVER (ORDER BY day_date)        AS rt_range,
  SUM(amount) OVER (ORDER BY day_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS rt_rows
FROM sales_ties
ORDER BY day_date;
```
**Explanation:** With tied sort keys, `RANGE` grants every tied row the *same* cumulative value (all peers included); `ROWS` counts physical rows, so ties produce differing running totals.

## Q42: Write a query to compute additional totals per row where each row also carries the grand total, group total, and running total at once.

`orders_wide(region VARCHAR(20), product VARCHAR(20), amount DECIMAL)`.

**Query:**
```sql
SELECT
  region,
  product,
  amount,
  SUM(amount) OVER ()                                       AS grand_total,
  SUM(amount) OVER (PARTITION BY region)                    AS region_total,
  SUM(amount) OVER (PARTITION BY region, product
    ORDER BY product)                                       AS product_running
FROM orders_wide
ORDER BY region, product;
```
**Explanation:** Multiple window calls with different PARTITION/ORDER specifications coexist in one `SELECT`, each producing a distinct aggregation level.

## Q43: Write a query to compute a moving average that ignores the current row (average of the previous 7 rows only).

`server_load(ts TIMESTAMP, load REAL)`.

**Query:**
```sql
SELECT
  ts,
  load,
  AVG(load) OVER (
    ORDER BY ts
    ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
  ) AS prev_7_avg
FROM server_load
ORDER BY ts;
```
**Explanation:** Ending the frame at `1 PRECEDING` excludes the current row, so the window is the 7 rows before it — useful for anomaly detection.

## Q44: Write a query to compute a 2-row-leading (forward) moving average using a frame that starts ahead of the current row, and note the caveat for the last rows.

`temps_daily(day_date DATE, temp DECIMAL)`.

**Query:**
```sql
SELECT
  day_date,
  temp,
  AVG(temp) OVER (
    ORDER BY day_date
    ROWS BETWEEN 1 FOLLOWING AND 2 FOLLOWING
  ) AS forward_ma_2
FROM temps_daily
ORDER BY day_date;
```
**Explanation:** A frame composed only of following rows yields a look-ahead average; the final rows naturally have fewer/empty frames.

## Q45: Write a query to accumulate a session-duration counter with `SUM` over a `CASE` that flags session starts.

`clicks(ts TIMESTAMP, session_bool INT)` where a 1 marks a new session boundary.

**Query:**
```sql
SELECT
  ts,
  session_bool,
  SUM(CASE WHEN session_bool = 1 THEN 1 ELSE 0 END)
    OVER (ORDER BY ts) AS session_no
FROM clicks
ORDER BY ts;
```
**Explanation:** Folding a `CASE` into a window sum counts boundary flags cumulatively, assigning every click its session number — the classic sessionization trick.

## Q46: Write a query that aggregates `EXCLUDE CURRENT ROW` to compute the sum of all other rows in the same partition.

`team_scores(team VARCHAR(20), player VARCHAR(20), score INT)`.

**Query:**
```sql
SELECT
  team,
  player,
  score,
  SUM(score) OVER (
    PARTITION BY team
    EXCLUDE CURRENT ROW
  ) AS teammates_total
FROM team_scores
ORDER BY team, player;
```
**Explanation:** `EXCLUDE CURRENT ROW` drops the current row from the frame (ORDER BY is absent so the frame is the whole partition) — SQLite/SQL Server 2022 support this.

## Q47: Write a query to compute the running average time between successive page views, framed per session.

`pageviews(session_id INT, view_ts TIMESTAMP)`.

**Query:**
```sql
SELECT
  session_id,
  view_ts,
  AVG(view_ts - LAG(view_ts) OVER (
    PARTITION BY session_id ORDER BY view_ts
  )) OVER (
    PARTITION BY session_id
    ORDER BY view_ts
  ) AS avg_gap_so_far
FROM pageviews
ORDER BY session_id, view_ts;
```
**Explanation:** A nested LAG computes each adjacent gap; the outer AVG window takes the cumulative average of those gaps within the session.

## Q48: Write a query to compute a cumulative minimum reset per stock split, using a partition on the split boundary flag.

`price_history(symbol VARCHAR(10), trade_date DATE, close DECIMAL, split_flag INT)`.

**Query:**
```sql
SELECT
  symbol,
  trade_date,
  split_flag,
  MIN(close) OVER (
    PARTITION BY symbol, split_flag
    ORDER BY trade_date
  ) AS cum_min_since_split
FROM price_history
ORDER BY symbol, trade_date;
```
**Explanation:** Partitioning by the split flag makes the running low restart at each split event, so old pre-split prices never leak into the new price scale.

## Q49: Write a query to compute a centered 5-day *maximum* of server cpu, and identify days that are local peaks.

`servers(day_date DATE, cpu REAL)`.

**Query:**
```sql
SELECT
  day_date,
  cpu,
  MAX(cpu) OVER (
    ORDER BY day_date
    ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
  ) AS centered_max_5,
  CASE
    WHEN cpu = MAX(cpu) OVER (
      ORDER BY day_date
      ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
    ) AND cpu > LAG(cpu) OVER (ORDER BY day_date)
    THEN 'local_peak' ELSE ''
  END AS tag
FROM servers
ORDER BY day_date;
```
**Explanation:** The centered max exposes the local neighborhood ceiling; a CASE flags days whose cpu equals it (compared against the prior day to avoid plateau ambiguity).

## Q50: Write a query to recompute a running total using only a correlated subquery, no window functions.

`sales(data_date DATE, amount DECIMAL)`.

**Query:**
```sql
SELECT
  s1.data_date,
  s1.amount,
  (SELECT SUM(s2.amount)
   FROM sales s2
   WHERE s2.data_date <= s1.data_date) AS running_total
FROM sales s1
ORDER BY s1.data_date;
```
**Explanation:** The correlated subquery re-sums all rows up to the current date for every row — an O(n²) alternative that window functions make O(n).

## Q51: Write a query to compute a running total of salary contributions for the top 5 earning employees per department.

`workers(dept VARCHAR(20), emp_id INT, salary INT)`.

**Query:**
```sql
WITH ranked AS (
  SELECT
    dept,
    emp_id,
    salary,
    ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
  FROM workers
)
SELECT
  dept,
  emp_id,
  salary,
  SUM(salary) OVER (
    PARTITION BY dept
    ORDER BY salary DESC, emp_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS top5_running
FROM ranked
WHERE rn <= 5
ORDER BY dept, salary DESC;
```
**Explanation:** A CTE ranks employees per department, the filter keeps the top 5, and the window sum runs along that reduced set.

## Q52: Write a query to compute, for each row, the count of rows *strictly before* and *strictly after* it in sort order (group-level context without ties).

`pts(ts TIMESTAMP, val INT)`.

**Query:**
```sql
SELECT
  ts,
  val,
  COUNT(*) OVER (
    ORDER BY ts
    ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
  ) AS rows_before,
  COUNT(*) OVER (
    ORDER BY ts
    ROWS BETWEEN 1 FOLLOWING AND UNBOUNDED FOLLOWING
  ) AS rows_after
FROM pts
ORDER BY ts;
```
**Explanation:** Two asymmetric frames count preceding and following rows; together with the current row they sum to the total row count.

## Q53: Write a query to compute a cumulative sum per quarter, then a quarterly-to-date percentage of the year total.

`sales(sale_date DATE, amount DECIMAL)`.

**Query:**
```sql
WITH qtot AS (
  SELECT
    DATE_TRUNC('quarter', sale_date) AS q,
    SUM(amount) OVER (ORDER BY sale_date) AS rt
  FROM sales
)
SELECT
  q,
  rt,
  rt / NULLIF(MAX(rt) OVER (), 0) AS pct
FROM qtot;
```
**Explanation:** The CTE holds the running total, and the `MAX` over the whole result retrieves the final (year-end) running total for the percentage.

## Q54: Write a query to compute a moving standard-deviation (volatility proxy) over a 20-day window.

`fx(day_date DATE, rate DECIMAL)`.

**Query:**
```sql
SELECT
  day_date,
  rate,
  STDDEV(rate) OVER (
    ORDER BY day_date
    ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
  ) AS volatility_20d
FROM fx
ORDER BY day_date;
```
**Explanation:** `STDDEV` over a 20-row trailing frame measures dispersion in the window; note it's the sample SD — a standard volatility proxy.

## Q55: Write a query to compute a running count of *positive* values and a running count of *negative* values in one pass.

`movements(d DATE, qty INT)`.

**Query:**
```sql
SELECT
  d,
  qty,
  SUM(CASE WHEN qty > 0 THEN 1 ELSE 0 END) OVER (ORDER BY d) AS cum_positives,
  SUM(CASE WHEN qty < 0 THEN 1 ELSE 0 END) OVER (ORDER BY d) AS cum_negatives
FROM movements
ORDER BY d;
```
**Explanation:** Two CASE-inside-SUM window aggregates count each sign class cumulatively with a single scan.

## Q56: Write a query that restates a running total as a *centralized* running total: cumulative minus grand total (deviation from final).

`clicks_by_day(day_date DATE, clicks INT)`.

**Query:**
```sql
SELECT
  day_date,
  clicks,
  SUM(clicks) OVER (ORDER BY day_date) AS running_clicks,
  SUM(clicks) OVER (ORDER BY day_date) - SUM(clicks) OVER () AS remaining_from_total
FROM clicks_by_day
ORDER BY day_date;
```
**Explanation:** Subtracting the grand-total window from the running window yields the amount still to come — a "remaining workload" indicator.

## Q57: Write a query to compute a 7-day moving average via a self-join, matching Q4 without window functions.

`prices(day_date DATE, price DECIMAL)`.

**Query:**
```sql
SELECT
  a.day_date,
  AVG(b.price) AS ma_7
FROM prices a
JOIN prices b
  ON b.day_date BETWEEN a.day_date - INTERVAL '6 day' AND a.day_date
GROUP BY a.day_date
ORDER BY a.day_date;
```
**Explanation:** The join fans out each day to its 6 predecessors plus itself; `AVG` over the group is the 7-day moving average.

## Q58: Write a query to compute a centered median (5-row median) for a sensor stream, using a frame and an ordered-set aggregate where supported.

`streams(ts TIMESTAMP, reading DECIMAL)`.

**Query:**
```sql
-- PostgreSQL: only the frame variant is a true sliding median
SELECT
  ts,
  reading,
  ROUND(
    percentile_cont(0.5) WITHIN GROUP (ORDER BY reading)
      OVER (ORDER BY ts ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING),
    3
  ) AS median_5
FROM streams
ORDER BY ts;
```
**Explanation:** Postgres `percentile_cont` accepts a `ROWS` frame, so each row's median comes from its 5-row centered neighborhood.

## Q59: Write a query to compute cumulative page views by weekday, resetting each new weekday partition.

`analytics(day_date DATE, views INT)`.

**Query:**
```sql
SELECT
  day_date,
  TO_CHAR(day_date, 'Dy') AS weekday,
  views,
  SUM(views) OVER (
    PARTITION BY EXTRACT(ISODOW FROM day_date)
    ORDER BY day_date
  ) AS weekday_cumulative
FROM analytics
ORDER BY day_date;
```
**Explanation:** Partitioning on the ISO weekday extracts each weekday's own series; ordering by date cumulates within that partition.

## Q60: Write a query to compute a running total of transactions where a `CASE` inside `SUM` drops return-transactions from accumulation.

`txns(txn_date DATE, txn_type VARCHAR(10), amount DECIMAL)`.

**Query:**
```sql
SELECT
  txn_date,
  txn_type,
  amount,
  SUM(
    CASE WHEN txn_type = 'SALE' THEN amount ELSE 0 END
  ) OVER (ORDER BY txn_date) AS net_sales_running
FROM txns
ORDER BY txn_date;
```
**Explanation:** The CASE filters which amounts enter the accumulation, so returns contribute zero while still advancing the frame.

## Q61: Write a query to compute a centered 3-month moving total of revenue with a full outer alignment that never shrinks frames mid-series.

`quarterly(q_start DATE, rev DECIMAL)`. Markets behave best when the frame always has all 3 rows.

**Query:**
```sql
-- PostgreSQL
WITH q AS (
  SELECT q_start, rev FROM quarterly
),
fullq AS (
  SELECT generate_series(MIN(q_start), MAX(q_start), '1 month')::date AS m
  FROM quarterly
)
SELECT
  f.m,
  COALESCE(q.rev, 0) AS rev,
  COALESCE(SUM(q.rev) OVER (
    ORDER BY f.m
    ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
  ), 0) AS centered_3mo
FROM fullq f
LEFT JOIN q ON q.q_start = f.m
ORDER BY f.m;
```
**Explanation:** `generate_series` materializes every month so missing months are filled with zeros, keeping the centered frame complete (avoids month-skew).

## Q62: Write a query to compute a running total per currency pair, ordering by trade time.

`trades(pair VARCHAR(10), ts TIMESTAMP, usd_vol DECIMAL)`.

**Query:**
```sql
SELECT
  pair,
  ts,
  usd_vol,
  SUM(usd_vol) OVER (
    PARTITION BY pair
    ORDER BY ts
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS pair_running_usd
FROM trades
ORDER BY pair, ts;
```
**Explanation:** Explicit `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` restates the default frame for clarity and forces physical-row semantics.

## Q63: Write a query that computes, per row, the average of the *excluding-self* group total: `(group_total - own_value) / (count - 1)`.

`grades(stu_id INT, subject VARCHAR(20), score INT)`.

**Query:**
```sql
SELECT
  stu_id,
  subject,
  score,
  (SUM(score) OVER (PARTITION BY subject) - score)
    / NULLIF(COUNT(*) OVER (PARTITION BY subject) - 1, 0) AS subject_avg_excl_self
FROM grades
ORDER BY subject, stu_id;
```
**Explanation:** Combines a partition-wide SUM and COUNT window with the row's own value to derive the leave-one-out average in one pass.

## Q64: Write a query to compute a *centered-sum forward fill*: carry the last available value over gaps with an ordering key.

`telemetry(tick INT, value DECIMAL)` where some ticks are missing.

**Query:**
```sql
SELECT
  tick,
  value,
  SUM(COALESCE(value, 0)) OVER (
    ORDER BY tick
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS forward_filled_total
FROM telemetry
ORDER BY tick;
```
**Explanation:** `COALESCE` converts missing values to zeros so the cumulative sum stays constant across gaps — effectively forward-filling the total.

## Q65: Write a query to compute a 10-row trailing moving sum of order weights on a delivery route.

`deliveries(stop_no INT, weight DECIMAL)`.

**Query:**
```sql
SELECT
  stop_no,
  weight,
  SUM(weight) OVER (
    ORDER BY stop_no
    ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
  ) AS trailing_10_stops
FROM deliveries
ORDER BY stop_no;
```
**Explanation:** The frame covers the current stop and 9 before it, giving the rolling 10-stop load constraint window.

## Q66: Write a query to produce a running total of *distinct* SKU counts using `COUNT(DISTINCT)` over a growing window for MySQL 8.

`orders_by_date(day_date DATE, sku VARCHAR(20))`. MySQL limitation is real.

**Query:**
```sql
SELECT
  day_date,
  COUNT(DISTINCT sku) OVER (ORDER BY day_date) AS distinct_skus
FROM orders_by_date
ORDER BY day_date;
```
**Explanation:** MySQL 8 *does* support `COUNT(DISTINCT ...) OVER` on this frame type; the fallback below documents the workaround for older engines.

**Alt1:**
```sql
SELECT
  day_date,
  (SELECT COUNT(DISTINCT o2.sku)
   FROM orders_by_date o2
   WHERE o2.day_date <= o1.day_date) AS distinct_skus
FROM orders_by_date o1
ORDER BY day_date;
```
**Explanation:** A correlated subquery recounts distinct SKUs across all rows up to the current date — correct, slow, but portable everywhere.

## Q67: Write a query to compute a centered 3-row running total that excludes the corner rows of the table (trim edges).

`points(serial INT, val INT)`.

**Query:**
```sql
SELECT
  serial,
  val,
  SUM(val) OVER (
    ORDER BY serial
    ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
  ) AS center_sum,
  CASE WHEN
    serial = MIN(serial) OVER () OR serial = MAX(serial) OVER ()
  THEN 'trim' ELSE 'keep' END AS edge_flag
FROM points
ORDER BY serial;
```
**Explanation:** MIN/MAX windows identify the first and last rows; the centered frame itself still calculates on them, and the flag lets you trim later.

## Q68: Write a query to compute a cumulative percentage **within groups** (each partition's own running total turns into a 0–100 share).

`regional_sales(region VARCHAR(20), day_date DATE, amount DECIMAL)`.

**Query:**
```sql
SELECT
  region,
  day_date,
  amount,
  SUM(amount) OVER (
    PARTITION BY region ORDER BY day_date
  ) * 100.0 / NULLIF(SUM(amount) OVER (PARTITION BY region), 0) AS pct_of_region
FROM regional_sales
ORDER BY region, day_date;
```
**Explanation:** The running (partition+order) window divided by the partition-wide sum yields each row's share of its region's total as it accumulates.

## Q69: Write a query to compute a cumulative sum of minutes parked, per vehicle, per garage.

`parking(garage_id INT, vehicle_id INT, entry_ts TIMESTAMP, minutes INT)`.

**Query:**
```sql
SELECT
  garage_id,
  vehicle_id,
  entry_ts,
  minutes,
  SUM(minutes) OVER (
    PARTITION BY garage_id, vehicle_id
    ORDER BY entry_ts
  ) AS billed_cumulative
FROM parking
ORDER BY garage_id, vehicle_id, entry_ts;
```
**Explanation:** Nested partitions (garage, vehicle) reset the running minute-total at every combination boundary.

## Q70: Write a query to compute a trailing 7-day average of sensor temperature using `RANGE` and explain why dates (not timestamps) matter.

`sensors(sample_date DATE, temp DECIMAL)`.

**Query:**
```sql
SELECT
  sample_date,
  AVG(temp) OVER (
    ORDER BY sample_date
    RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW
  ) AS ma_7d
FROM sensors
ORDER BY sample_date;
```
**Explanation:** `RANGE` with an interval offsets by *value* not row-count, so a 7-day window is 7 calendar days — exact only when frames operate on dates.

## Q71: Write a query that computes the ratio-moving-average: current 10-day MA divided by the running 50-day MA, comparing two frames in one select.

`index_vals(day_date DATE, price DECIMAL)`.

**Query:**
```sql
SELECT
  day_date,
  AVG(price) OVER (
    ORDER BY day_date ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
  ) / NULLIF(AVG(price) OVER (
    ORDER BY day_date ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
  ), 0) AS golden_ratio
FROM index_vals
ORDER BY day_date;
```
**Explanation:** Both MAs use the same ordering but different frame sizes; their quotient is a fast/slow-ratio oscillator.

## Q72: Write a query to compute a cumulative sum reset **mid-partition** using a change flag from a column.

`route_log(step_id INT, direction CHAR(1), qty INT)` where direction='R' starts a new route segment.

**Query:**
```sql
SELECT
  step_id,
  direction,
  qty,
  SUM(CASE WHEN direction = 'R' THEN 1 ELSE 0 END)
    OVER (ORDER BY step_id) AS segment,
  SUM(qty) OVER (
    PARTITION BY SUM(CASE WHEN direction = 'R' THEN 1 ELSE 0 END)
      OVER (ORDER BY step_id)
    ORDER BY step_id
  ) AS segment_running_qty
FROM route_log
ORDER BY step_id;
```
**Explanation:** A CASE-based cumulative flag computes a segment number, and partitioning the outer SUM by that computed flag makes the running total reset at every 'R'.

## Q73: Write a query that mirrors a running total twice — once by date, once by id — and show when ROWS vs RANGE diverge on duplicate dates.

`registrations(reg_date DATE, reg_id INT)` with duplicate reg_dates.

**Query:**
```sql
SELECT
  reg_id,
  reg_date,
  SUM(reg_id) OVER (ORDER BY reg_date) AS by_date_range,
  SUM(reg_id) OVER (
    ORDER BY reg_date, reg_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS by_date_id_rows
FROM registrations
ORDER BY reg_date, reg_id;
```
**Explanation:** On duplicates, `RANGE` folds ties into one frame value while `ROWS` respects row identity — ordering by `(reg_date, reg_id)` removes the ambiguity.

## Q74: Write a query to compute a cumulative sum of stock-option grants split by vesting cohort.

`grants(symbol VARCHAR(10), grant_date DATE, shares INT, cohort VARCHAR(10))`.

**Query:**
```sql
SELECT
  symbol,
  cohort,
  grant_date,
  shares,
  SUM(shares) OVER (
    PARTITION BY symbol, cohort
    ORDER BY grant_date
  ) AS cohort_vest_rt
FROM grants
ORDER BY symbol, cohort, grant_date;
```
**Explanation:** The (symbol, cohort) partition tracks each vesting tranche's own cumulative grant count.

## Q75: Write a query to compute a *moving coefficient of variation*: running SD divided by running mean over a 30-day frame.

`yields(day_date DATE, y REAL)`.

**Query:**
```sql
SELECT
  day_date,
  STDDEV(y) OVER (ORDER BY day_date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)
    / NULLIF(AVG(y) OVER (ORDER BY day_date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW), 0)
    AS cv_30
FROM yields
ORDER BY day_date;
```
**Explanation:** Dividing the framed STDDEV by the framed AVG yields a normalized dispersion index that is scale-free.

## Q76: Write a query showing why a *window over a window* fails, and restructure it using a derived table to compute the average of a moving average.

`daily_sensor(day_date DATE, reading DECIMAL)`.

**Query:**
```sql
-- The illegal version (fails: "window functions not allowed in the window frame")
-- SELECT AVG(AVG(reading) OVER (ORDER BY day_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW))
--        OVER (ORDER BY day_date) FROM daily_sensor;

WITH ma7 AS (
  SELECT
    day_date,
    AVG(reading) OVER (
      ORDER BY day_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS ma_7
  FROM daily_sensor
)
SELECT
  day_date,
  ma_7,
  AVG(ma_7) OVER (
    ORDER BY day_date ROWS BETWEEN 13 PRECEDING AND CURRENT ROW
  ) AS ma_of_ma
FROM ma7
ORDER BY day_date;
```
**Explanation:** Nested window calls are prohibited; lane-splitting into a CTE turns the "moving average of the moving average" into two legal sequential window layers.

## Q77: Write a query to compute a running total per *session* identified by aggregate flags — a cumulative-total-then-repartition.

`events_raw(ev_ts TIMESTAMP, session_id INT, value INT)`.

**Query:**
```sql
SELECT
  session_id,
  ev_ts,
  value,
  SUM(value) OVER (
    PARTITION BY session_id
    ORDER BY ev_ts
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS session_running
FROM events_raw
ORDER BY session_id, ev_ts;
```
**Explanation:** The session_id already partitions cleanly; because sessions never interleave, this is the canonical running-total-per-session pattern.

## Q78: Write a query to compute a cumulative sum that *ignores the current row* — good for "prior-period totals" in trend reports.

`expiry(month CHAR(7), qty INT)`.

**Query:**
```sql
SELECT
  month,
  qty,
  SUM(qty) OVER (
    ORDER BY month
    ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
  ) AS prior_months_cum
FROM expiry
ORDER BY month;
```
**Explanation:** Ending the frame at `1 PRECEDING` yields cumulative-without-self; the first row legitimately shows NULL.

## Q79: Write a query that produces an expanding-window count *including empty days* built from a date spine.

`campaigns(start_date DATE, end_date DATE, clicks INT)`.

**Query:**
```sql
-- PostgreSQL
WITH spine AS (
  SELECT generate_series(MIN(start_date), MAX(end_date), '1 day')::date AS d
  FROM campaigns
),
left_join AS (
  SELECT spine.d, campaigns.clicks
  FROM spine
  LEFT JOIN campaigns ON campaigns.start_date = spine.d
)
SELECT
  d,
  COALESCE(clicks, 0) AS clicks,
  SUM(COALESCE(clicks, 0)) OVER (
    ORDER BY d ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS campaigns_cumulative
FROM left_join
ORDER BY d;
```
**Explanation:** A `generate_series` spine guarantees one row per day; zeros for gaps keep the expanding sum continuous across the campaign window.

## Q80: Write a query to compute a *weighted cumulative total* where the weight itself comes from the next available value (inner join trick).

`streams(tick INT, z DECIMAL, w DECIMAL)`.

**Query:**
```sql
SELECT
  tick,
  z,
  w,
  SUM(z * w) OVER (
    ORDER BY tick ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) / NULLIF(SUM(w) OVER (
    ORDER BY tick ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ), 0) AS wcum_avg
FROM streams
ORDER BY tick;
```
**Explanation:** Numerator and denominator windows share the frame, so the quotient is a running weighted average using each row's own weight.

## Q81: Write a query using `ROWS` explicitly to guarantee integer semantics on a cumulative sum where floating-point drift is a concern.

`apportion(id INT, resourced DECIMAL(30,10))`.

**Query:**
```sql
SELECT
  id,
  resourced,
  SUM(resourced) OVER (
    ORDER BY id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS exact_cumulative
FROM apportion
ORDER BY id;
```
**Explanation:** Numeric(30,10) minimizes drift; `ROWS` avoids RANGE's tie-jumping, keeping the cumulative exactly per physical row.

## Q82: Write a query that computes a running total *as-of* sequence numbers but resets at a NULL boundary marker.

`build_orders(step INT, milestone INT, hours INT)` where milestone is NULL at segment starts.

**Query:**
```sql
SELECT
  step,
  milestone,
  hours,
  SUM(CASE WHEN milestone IS NULL THEN 1 ELSE 0 END)
    OVER (ORDER BY step) AS seg,
  SUM(hours) OVER (
    PARTITION BY SUM(CASE WHEN milestone IS NULL THEN 1 ELSE 0 END)
      OVER (ORDER BY step)
    ORDER BY step
  ) AS seg_hours
FROM build_orders
ORDER BY step;
```
**Explanation:** NULL flags mark each segment start; a cumulative sum counts segments, and the hours-sum partititions by that count — a NULL-driven restart.

## Q83: Write a query to compute a trailing 3-row *sum of absolute deltas* (volatility in absolute terms).

`flow(tick INT, amount DECIMAL)`.

**Query:**
```sql
SELECT
  tick,
  SUM(ABS(amount - LAG(amount) OVER (ORDER BY tick)))
    OVER (ORDER BY tick ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS abs_vol_3
FROM flow
ORDER BY tick;
```
**Explanation:** LAG computes each step's signed change; ABS makes it non-negative, and the outer 3-row window sums recent absolute move sizes.

## Q84: Write a query to compute a *running total of distinct assets held* per portfolio with a strict ordering that keeps duplicates from double-counting.

`holdings(acc VARCHAR(10), asset VARCHAR(10), amt DECIMAL)`.

**Query:**
```sql
SELECT
  acc,
  asset,
  amt,
  SUM(CASE WHEN rn = 1 THEN amt ELSE 0 END) OVER (
    PARTITION BY acc
    ORDER BY asset
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS distinct_asset_rt
FROM (
  SELECT
    acc, asset, amt,
    ROW_NUMBER() OVER (PARTITION BY acc, asset ORDER BY amt DESC) AS rn
  FROM holdings
) h
ORDER BY acc, asset;
```
**Explanation:** `ROW_NUMBER` marks the first occurrence of each asset; the window SUM adds only those rows, skipping duplicates like a running DISTINCT.

## Q85: Write a query to compute a running effective exchange rate as a weighted average over rolling positions.

`fx_positions(day_date DATE, ccy CHAR(3), notional DECIMAL)`.

**Query:**
```sql
SELECT
  day_date,
  ccy,
  SUM(notional) OVER (
    PARTITION BY ccy ORDER BY day_date
  ) AS pos_cum,
  AVG(1.0 * notional) OVER (
    PARTITION BY ccy ORDER BY day_date
  ) AS simple_avg_rate_proxy
FROM fx_positions
ORDER BY ccy, day_date;
```
**Explanation:** A demo of mixing cumulative notional with a running average — proper FX averages need notional weights (see Q24's VWAP pattern).

## Q86: Write a query to compute the *maximum cumulative sum so far* per group and flag rows at the record high.

`team_scores(team VARCHAR(20), match_no INT, pts INT)`.

**Query:**
```sql
SELECT
  team,
  match_no,
  pts,
  SUM(pts) OVER (PARTITION BY team ORDER BY match_no) AS cum_pts,
  MAX(SUM(pts) OVER (PARTITION BY team ORDER BY match_no))
    OVER (PARTITION BY team ORDER BY match_no) AS best_so_far,
  CASE WHEN
    SUM(pts) OVER (PARTITION BY team ORDER BY match_no)
    = MAX(SUM(pts) OVER (PARTITION BY team ORDER BY match_no))
       OVER (PARTITION BY team ORDER BY match_no)
  THEN 'record' ELSE '' END AS is_record
FROM team_scores
ORDER BY team, match_no;
```
**Explanation:** `MAX` over the running sum tracks a running record; the CASE marks rows tying the all-time highest cumulative total in the partition.

## Q87: Write a query to emulate a *centered* moving average when the engine lacks `ROWS BETWEEN n PRECEDING AND n FOLLOWING`.

`samples(seq INT, val DECIMAL)`.

**Query:**
```sql
-- Works on engines that only support basic frames: split into LEAD/LAG
-- (PostgreSQL/MySQL 8/SQL Server all have ROWS, so this is a legacy fallback)
SELECT
  seq,
  val,
  (val
   + COALESCE(LAG(val, 1) OVER (ORDER BY seq), 0)
   + COALESCE(LAG(val, 2) OVER (ORDER BY seq), 0)
   + COALESCE(LEAD(val, 1) OVER (ORDER BY seq), 0)
   + COALESCE(LEAD(val, 2) OVER (ORDER BY seq), 0)
  ) / 5.0 AS centered_5_manual
FROM samples
ORDER BY seq;
```
**Explanation:** LAG/LEAD pulls the ±2 neighbors explicitly and COALESCE turns edge rows into zeros — a manual centered window with no ROWS support required.

## Q88: Write a query to compute a moving average of a *percentage column* without bias from differing denominator lengths.

`shift_metrics(shift DATE, prod INT, planned INT)`.

**Query:**
```sql
SELECT
  shift,
  prod,
  planned,
  SUM(prod) OVER (ORDER BY shift ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
    / NULLIF(SUM(planned) OVER (ORDER BY shift ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 0)
    * 100 AS ma_uptime_pct_7d
FROM shift_metrics
ORDER BY shift;
```
**Explanation:** Averaging already-computed percentages is wrong; instead sum both numerators and denominators over the same frame, then divide.

## Q89: Write a query to compute a cumulative total of returns *after filtering* the top 10% of rows out using an inner window.

`trades(id INT, amount DECIMAL)` — drop the top 10% by amount before cumulating.

**Query:**
```sql
WITH pct AS (
  SELECT
    id,
    amount,
    NTILE(10) OVER (ORDER BY amount DESC) AS decile
  FROM trades
)
SELECT
  id,
  amount,
  SUM(amount) OVER (
    ORDER BY id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS filtered_running
FROM pct
WHERE decile > 1
ORDER BY id;
```
**Explanation:** NTILE buckets rows into deciles; the `WHERE` discards the top decile and the remaining rows get their running total cleanly.

## Q90: Write a query to compute a weighted moving average using an *inline kernel* (weight column) with the frame sized by kernel length.

`energetics(day_date DATE, e DECIMAL, w DECIMAL)`.

**Query:**
```sql
SELECT
  day_date,
  e,
  SUM(e * w) OVER (
    ORDER BY day_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) / NULLIF(SUM(w) OVER (
    ORDER BY day_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ), 0) AS ewma7
FROM energetics
ORDER BY day_date;
```
**Explanation:** The kernel weight column multiplies each reading; identical 7-row frames on numerator and denominator yield a proper 7-point weighted MA.

## Q91: Write a query to compute a *trailing* cumulative sum with a cutting `EXCLUDE GROUP` — hand-rolled group-level sums per row.

`flat(team VARCHAR(10), pts INT)` with duplicate teams.

**Query:**
```sql
SELECT
  team,
  pts,
  SUM(pts) OVER (PARTITION BY team
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    EXCLUDE GROUP) AS group_sum_excl
FROM flat
ORDER BY team, pts;
```
**Explanation:** `EXCLUDE GROUP` removes all peer rows with the same ORDER BY value; with no ORDER BY the frame is the full partition, so this yields per-row peer-excluded sums.

## Q92: Write a query to compute cumulative counts and sums on a *multi-key* ordering with stable tie-breaking.

`sales_events(day_date DATE, event_no INT, amount DECIMAL)`.

**Query:**
```sql
SELECT
  day_date,
  event_no,
  amount,
  SUM(amount) OVER (
    ORDER BY day_date, event_no
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS stable_running
FROM sales_events
ORDER BY day_date, event_no;
```
**Explanation:** Ordering by `(day_date, event_no)` makes the running total deterministic even when dates collide.

## Q93: Write a query to compute a centered-3 *maximum of running total* — a two-window composition reflecting the peak cumulative so far in a window.

`players(ord INT, score INT)`.

**Query:**
```sql
WITH rt AS (
  SELECT
    ord,
    score,
    SUM(score) OVER (ORDER BY ord) AS running_score
  FROM players
)
SELECT
  ord,
  score,
  running_score,
  MAX(running_score) OVER (
    ORDER BY ord ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
  ) AS centered_peak
FROM rt
ORDER BY ord;
```
**Explanation:** First compute the running total in a CTE, then apply a centered MAX over it — cleanly demonstrating two sequential window layers.

## Q94: Write a query that converts a running total into a **density-formatted** cumulative percentage (100% at the end).

`effort(day_date DATE, pts INT)`.

**Query:**
```sql
WITH rt AS (
  SELECT
    day_date,
    pts,
    SUM(pts) OVER (ORDER BY day_date) AS running_pts,
    SUM(pts) OVER () AS total_pts
  FROM effort
)
SELECT
  day_date,
  pts,
  100.0 * running_pts / NULLIF(total_pts, 0) AS pct_done
FROM rt
ORDER BY day_date;
```
**Explanation:** The final value of a running total equals the grand total, so dividing running by grand gives a monotonically-growing completion percentage.

## Q95: Write a query that shows a *moving bucket-count*: how many distinct sessions fall inside each trailing 5-day frame.

`web_sessions(day_date DATE, session_id INT)`.

**Query:**
```sql
SELECT
  day_date,
  COUNT(DISTINCT session_id) OVER (
    ORDER BY day_date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
  ) AS active_sessions_5d
FROM web_sessions
ORDER BY day_date;
```
**Explanation:** Approximating distinct sessions per rolling frame with `COUNT(DISTINCT ...) OVER (ROWS ...)` — deterministic but heavier than a HyperLogLog approximation.

**Alt1:**
```sql
-- PostgreSQL: exact same result, cheaper if frames are large, using generate_series
WITH per_day AS (
  SELECT day_date, COUNT(DISTINCT session_id) AS sess FROM web_sessions GROUP BY 1
)
SELECT
  day_date,
  (SELECT COUNT(DISTINCT session_id) FROM web_sessions w
    WHERE w.day_date BETWEEN p.day_date - INTERVAL '4 day' AND p.day_date) AS active_5d
FROM per_day p
ORDER BY day_date;
```
**Explanation:** A correlated subquery per day recomputes the rolling distinct count — exact but O(rows×days), contrasting with the single-pass window above.

## Q96: Write a query to compute the *moving total of events per template*, resetting the count when the template id changes.

`template_events(tid INT, seq INT, weight INT)`.

**Query:**
```sql
SELECT
  tid,
  seq,
  weight,
  SUM(weight) OVER (
    PARTITION BY tid
    ORDER BY seq
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS tid_running
FROM template_events
ORDER BY tid, seq;
```
**Explanation:** Partitioning by template id is exactly the "reset at template change" requirement, since templates never interleave in the data.

## Q97: Write a query with a *mixed* frame — count(*) from unbounded preceding to 2 following, plus current-row average — in one select for a "backward-looking total, forward-looking count".

`waves(pos INT, h DECIMAL)`.

**Query:**
```sql
SELECT
  pos,
  h,
  SUM(1) OVER (ORDER BY pos ROWS BETWEEN 3 PRECEDING AND CURRENT ROW) AS back_count,
  AVG(h) OVER (ORDER BY pos ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING) AS fwd_avg,
  MAX(h) OVER (ORDER BY pos ROWS BETWEEN 3 PRECEDING AND 2 FOLLOWING) AS swing_high
FROM waves
ORDER BY pos;
```
**Explanation:** Three framed windows in one SELECT: a trailing span count, a forward-looking average, and an asymmetric min-max span — all legal and independent.

## Q98: Write a query showing an *optimization hint*: single-pass frame reuse by naming the frame in a window clause to avoid repeating `ROWS ...` text.

`sales_audit(day_date DATE, rev DECIMAL)`.

**Query:**
```sql
SELECT
  day_date,
  rev,
  SUM(rev) OVER w   AS rt_7,
  AVG(rev) OVER w   AS ma_7,
  MIN(rev) OVER w   AS lo_7,
  MAX(rev) OVER w   AS hi_7,
  COUNT(*) OVER w   AS n_7
FROM sales_audit
WINDOW w AS (
  ORDER BY day_date
  ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
)
ORDER BY day_date;
```
**Explanation:** The `WINDOW` clause reuses one 7-row frame for five aggregates, making the intent clear and the plan single-pass (MySQL, Postgres, SQL Server).

## Q99: Write a query to compute a *reversed* running total (cumulative from the end) by negating the sort key.

`lifespan(days_used INT, units INT)` — cumulative units remaining.

**Query:**
```sql
SELECT
  days_used,
  units,
  SUM(units) OVER (
    ORDER BY (days_used * -1)
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS remaining_from_end
FROM lifespan
ORDER BY days_used;
```
**Explanation:** Ordering by the negated key makes the window grow from the last row backwards, producing cumulative-total-from-the-end with a standard frame.

## Q100: Write a query computing plan-vs-actual: a running total of "budget minus actual per day", alias the cumulative deviation budget-drift.

`budget_actual(day_date DATE, budget DECIMAL, actual DECIMAL)`.

**Query:**
```sql
SELECT
  day_date,
  budget,
  actual,
  SUM(budget - actual) OVER (
    ORDER BY day_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS drift_cumulative
FROM budget_actual
ORDER BY day_date;
```
**Explanation:** Algebraic sign is folded into the window SUM — each row adds its daily gap to the drift, the running deviation from plan.

**Alt1:**
```sql
-- Self-join equivalent: same outcome, quadratic cost, no window function
SELECT
  b1.day_date,
  b1.budget,
  b1.actual,
  SUM(b2.budget - b2.actual) AS drift_cumulative
FROM budget_actual b1
JOIN budget_actual b2 ON b2.day_date <= b1.day_date
GROUP BY b1.day_date, b1.budget, b1.actual
ORDER BY b1.day_date;
```
**Explanation:** The self-join sums all earlier daily gaps per row — the instructive, pre-window rewrite of the same cumulative deviation.
