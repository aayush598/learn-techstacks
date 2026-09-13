# FAANG-Style Interview Round 2 (Advanced) — 100 SQL Q&A

---

## Q1: Sessionization — Group Events into Sessions

**Tables:** `events(user_id INT, event_type VARCHAR, event_time TIMESTAMP)`. Group events into sessions where a new session starts after 30 minutes of inactivity. Assign each event a session_id.

**Query:**
```sql
SELECT
  user_id,
  event_type,
  event_time,
  SUM(new_session) OVER (ORDER BY user_id, event_time) AS session_id
FROM (
  SELECT
    *,
    CASE
      WHEN event_time - LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time)
           > INTERVAL '30 minutes'
        THEN 1
      ELSE 0
    END AS new_session
  FROM events
) sub;
```

**Explanation:** The classic sessionization trick: compare each event time to the previous event's time per user. If the gap exceeds 30 minutes, flag a new session. The running sum of flags produces a unique session ID. **Interview trick:** Always handle NULL from LAG on the first event (implicitly handled here since SUM starts at 0).

---

## Q2: Sessionization — Compute Time Spent Per Session

**Tables:** `events(user_id INT, page VARCHAR, event_time TIMESTAMP)`. Compute the duration of each session (last event minus first event).

**Query:**
```sql
SELECT
  user_id,
  session_id,
  MIN(event_time) AS session_start,
  MAX(event_time) AS session_end,
  EXTRACT(EPOCH FROM MAX(event_time) - MIN(event_time)) / 60.0 AS minutes_spent
FROM (
  SELECT
    *,
    SUM(new_session) OVER (PARTITION BY user_id ORDER BY event_time) AS session_id
  FROM (
    SELECT
      *,
      CASE
        WHEN event_time - LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time)
             > INTERVAL '30 minutes'
          THEN 1
        ELSE 0
      END AS new_session
    FROM events
  ) s
) t
GROUP BY user_id, session_id;
```

**Explanation:** Build on Q1's sessionization, then aggregate with MIN/MAX to get duration. Convert to minutes with `EXTRACT(EPOCH)`. **Interview trick:** For single-event sessions, duration is 0 — confirm with interviewer whether that's acceptable.

---

## Q3: Sessionization — Page Views Per Session with Rankings

**Tables:** `page_views(user_id INT, page_url VARCHAR, view_time TIMESTAMP)`. Find the top 3 most-viewed pages per session.

**Query:**
```sql
WITH sessionized AS (
  SELECT
    *,
    SUM(new_session) OVER (PARTITION BY user_id ORDER BY view_time) AS session_id
  FROM (
    SELECT
      *,
      CASE
        WHEN view_time - LAG(view_time) OVER (PARTITION BY user_id ORDER BY view_time)
             > INTERVAL '30 minutes'
          THEN 1
        ELSE 0
      END AS new_session
    FROM page_views
  ) s
),
ranked AS (
  SELECT
    user_id,
    session_id,
    page_url,
    COUNT(*) AS page_views,
    ROW_NUMBER() OVER (
      PARTITION BY user_id, session_id
      ORDER BY COUNT(*) DESC
    ) AS rn
  FROM sessionized
  GROUP BY user_id, session_id, page_url
)
SELECT user_id, session_id, page_url, page_views
FROM ranked
WHERE rn <= 3;
```

**Explanation:** Sessionize, then count per page per session, and rank with ROW_NUMBER. **Interview trick:** Use ROW_NUMBER vs DENSE_RANK depending on whether ties should share a position.

---

## Q4: Funnel Conversion — Stepwise Drop-Off

**Tables:** `events(user_id INT, event_type VARCHAR, event_time TIMESTAMP)`. Event types are: 'page_view', 'add_to_cart', 'checkout', 'purchase'. Compute conversion rate at each step.

**Query:**
```sql
WITH funnel AS (
  SELECT
    user_id,
    MAX(CASE WHEN event_type = 'page_view'   THEN 1 ELSE 0 END) AS step1_view,
    MAX(CASE WHEN event_type = 'add_to_cart'  THEN 1 ELSE 0 END) AS step2_cart,
    MAX(CASE WHEN event_type = 'checkout'     THEN 1 ELSE 0 END) AS step3_checkout,
    MAX(CASE WHEN event_type = 'purchase'     THEN 1 ELSE 0 END) AS step4_purchase
  FROM events
  GROUP BY user_id
)
SELECT
  COUNT(*) AS total_users,
  SUM(step1_view)   AS reached_view,
  SUM(step2_cart)    AS reached_cart,
  SUM(step3_checkout) AS reached_checkout,
  SUM(step4_purchase) AS reached_purchase,
  ROUND(100.0 * SUM(step2_cart)    / NULLIF(SUM(step1_view), 0), 2) AS view_to_cart_pct,
  ROUND(100.0 * SUM(step3_checkout) / NULLIF(SUM(step2_cart), 0), 2) AS cart_to_checkout_pct,
  ROUND(100.0 * SUM(step4_purchase) / NULLIF(SUM(step3_checkout), 0), 2) AS checkout_to_purchase_pct
FROM funnel;
```

**Explanation:** Pivot each user's events into step flags, then count users who reached each step. **Interview trick:** `NULLIF(..., 0)` prevents division by zero. Use `MAX` because a user either reached the step (1) or didn't (0).

---

## Q5: Funnel Conversion — Time-to-Convert Per Step

**Tables:** `events(user_id INT, event_type VARCHAR, event_time TIMESTAMP)`. For users who complete the full funnel, compute the average time between each step.

**Query:**
```sql
WITH step_times AS (
  SELECT
    user_id,
    MIN(CASE WHEN event_type = 'page_view'  THEN event_time END) AS t_view,
    MIN(CASE WHEN event_type = 'add_to_cart' THEN event_time END) AS t_cart,
    MIN(CASE WHEN event_type = 'checkout'    THEN event_time END) AS t_checkout,
    MIN(CASE WHEN event_type = 'purchase'    THEN event_time END) AS t_purchase
  FROM events
  GROUP BY user_id
)
SELECT
  COUNT(*) AS completers,
  AVG(EXTRACT(EPOCH FROM t_cart - t_view))      / 60.0 AS avg_min_view_to_cart,
  AVG(EXTRACT(EPOCH FROM t_checkout - t_cart))   / 60.0 AS avg_min_cart_to_checkout,
  AVG(EXTRACT(EPOCH FROM t_purchase - t_checkout)) / 60.0 AS avg_min_checkout_to_purchase
FROM step_times
WHERE t_view IS NOT NULL
  AND t_cart IS NOT NULL
  AND t_checkout IS NOT NULL
  AND t_purchase IS NOT NULL;
```

**Explanation:** Take the earliest timestamp per step per user, then compute average deltas. **Interview trick:** Filter for users who completed all steps; otherwise averages include NULLs and skew low.

---

## Q6: Retention Curve — N-Day Retention Per Cohort

**Tables:** `signups(user_id INT, signup_date DATE)`, `logins(user_id INT, login_date DATE)`. Compute D1, D7, D14, D30 retention for each weekly signup cohort.

**Query:**
```sql
WITH cohort AS (
  SELECT
    user_id,
    DATE_TRUNC('week', signup_date)::DATE AS cohort_week,
    signup_date
  FROM signups
),
retention AS (
  SELECT
    c.cohort_week,
    c.user_id,
    MAX(CASE WHEN l.login_date = c.signup_date + INTERVAL '1 day'  THEN 1 ELSE 0 END) AS d1,
    MAX(CASE WHEN l.login_date = c.signup_date + INTERVAL '7 days' THEN 1 ELSE 0 END) AS d7,
    MAX(CASE WHEN l.login_date = c.signup_date + INTERVAL '14 days' THEN 1 ELSE 0 END) AS d14,
    MAX(CASE WHEN l.login_date = c.signup_date + INTERVAL '30 days' THEN 1 ELSE 0 END) AS d30
  FROM cohort c
  LEFT JOIN logins l ON c.user_id = l.user_id
  GROUP BY c.cohort_week, c.user_id
)
SELECT
  cohort_week,
  COUNT(*) AS cohort_size,
  ROUND(100.0 * SUM(d1)  / COUNT(*), 2) AS d1_retention,
  ROUND(100.0 * SUM(d7)  / COUNT(*), 2) AS d7_retention,
  ROUND(100.0 * SUM(d14) / COUNT(*), 2) AS d14_retention,
  ROUND(100.0 * SUM(d30) / COUNT(*), 2) AS d30_retention
FROM retention
GROUP BY cohort_week
ORDER BY cohort_week;
```

**Explanation:** Assign each user to a weekly cohort, then check if they logged in on specific days after signup. **Interview trick:** Use `DATE_TRUNC('week')` for consistent cohort buckets; LEFT JOIN ensures users with zero logins still appear.

---

## Q7: Retention — Rolling Retention Curve (Any Day)

**Tables:** `signups(user_id INT, signup_date DATE)`, `activity(user_id INT, activity_date DATE)`. For each cohort, compute the percentage of users active on each day from day 0 to day 30.

**Query:**
```sql
WITH cohort AS (
  SELECT user_id, signup_date
  FROM signups
),
days AS (
  SELECT
    c.user_id,
    c.signup_date,
    a.activity_date - c.signup_date AS day_n,
    MAX(CASE WHEN a.activity_date = c.signup_date + (a.activity_date - c.signup_date) THEN 1 ELSE 0 END) AS active
  FROM cohort c
  LEFT JOIN activity a ON c.user_id = a.user_id
    AND a.activity_date BETWEEN c.signup_date AND c.signup_date + INTERVAL '30 days'
  GROUP BY c.user_id, c.signup_date, a.activity_date
),
retention AS (
  SELECT
    signup_date AS cohort_date,
    day_n,
    COUNT(DISTINCT user_id) AS active_users
  FROM days
  WHERE active = 1
  GROUP BY signup_date, day_n
),
cohort_sizes AS (
  SELECT signup_date, COUNT(*) AS cohort_size
  FROM signups
  GROUP BY signup_date
)
SELECT
  r.cohort_date,
  r.day_n,
  r.active_users,
  cs.cohort_size,
  ROUND(100.0 * r.active_users / cs.cohort_size, 2) AS retention_pct
FROM retention r
JOIN cohort_sizes cs ON r.cohort_date = cs.signup_date
ORDER BY r.cohort_date, r.day_n;
```

**Explanation:** Join signups to activity within a 30-day window, compute day_n, then aggregate active users per day per cohort. **Interview trick:** The LEFT JOIN with date range bounds is more efficient than computing day_n in application code.

---

## Q8: Median Event Count Per Day (Percentile Approach)

**Tables:** `daily_events(day DATE, event_count INT)`. Find the median of event_count across all days.

**Query:**
```sql
-- PostgreSQL
SELECT
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY event_count) AS median_events
FROM daily_events;
```

**Alt1:** Manual median with ROW_NUMBER:
```sql
SELECT AVG(event_count) AS median_events
FROM (
  SELECT
    event_count,
    ROW_NUMBER() OVER (ORDER BY event_count) AS rn,
    COUNT(*) OVER () AS total
  FROM daily_events
) sub
WHERE rn IN (FLOOR((total + 1) / 2.0), CEIL((total + 1) / 2.0));
```

**Alt2:** MySQL 8+:
```sql
-- MySQL
SELECT
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY event_count) OVER () AS median_events
FROM daily_events
LIMIT 1;
```

**Explanation:** `PERCENTILE_CONT` interpolates between values for exact medians. **Interview trick:** MySQL doesn't support `PERCENTILE_CONT` as a standalone aggregate — use the window function form or the ROW_NUMBER method.

---

## Q9: Median Session Duration Per Day

**Tables:** `sessions(session_id INT, user_id INT, start_time TIMESTAMP, end_time TIMESTAMP)`. Compute the median session duration per day.

**Query:**
```sql
-- PostgreSQL
WITH durations AS (
  SELECT
    start_time::DATE AS day,
    session_id,
    EXTRACT(EPOCH FROM end_time - start_time) / 60.0 AS duration_min
  FROM sessions
),
ranked AS (
  SELECT
    day,
    duration_min,
    ROW_NUMBER() OVER (PARTITION BY day ORDER BY duration_min) AS rn,
    COUNT(*) OVER (PARTITION BY day) AS cnt
  FROM durations
)
SELECT
  day,
  AVG(duration_min) AS median_duration_min
FROM ranked
WHERE rn IN (FLOOR((cnt + 1) / 2.0), CEIL((cnt + 1) / 2.0))
GROUP BY day
ORDER BY day;
```

**Explanation:** Compute durations, rank within each day, and pick the middle value(s). **Interview trick:** The `FLOOR/CEIL` trick handles both odd and even counts correctly by averaging the two middle values when even.

---

## Q10: Rolling 7-Day Active Users (Distinct)

**Tables:** `events(user_id INT, event_date DATE)`. For each day, compute the number of distinct users active in the preceding 7 days (including the current day).

**Query:**
```sql
SELECT
  d.day,
  COUNT(DISTINCT e.user_id) AS rolling_7d_active
FROM (
  SELECT DISTINCT event_date AS day FROM events
) d
JOIN events e
  ON e.event_date BETWEEN d.day - INTERVAL '6 days' AND d.day
GROUP BY d.day
ORDER BY d.day;
```

**Alt1:** Window function approach (no self-join):
```sql
WITH daily_users AS (
  SELECT event_date, user_id
  FROM events
  GROUP BY event_date, user_id
)
SELECT
  event_date,
  COUNT(DISTINCT user_id) OVER (
    ORDER BY event_date
    RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW
  ) AS rolling_7d_active
FROM daily_users
ORDER BY event_date;
```

**Explanation:** Join each day to events in the 7-day window and count distinct users. **Interview trick:** The window function approach with `RANGE` is cleaner but PostgreSQL may not support `DISTINCT` in all window aggregates — test your dialect.

---

## Q11: Rolling 7-Day Active Users with New vs Returning

**Tables:** `events(user_id INT, event_date DATE)`, `signups(user_id INT, signup_date DATE)`. For each day, show rolling 7-day active users split into new (signed up within 7 days) and returning.

**Query:**
```sql
WITH daily_active AS (
  SELECT event_date, user_id
  FROM events
  GROUP BY event_date, user_id
),
classified AS (
  SELECT
    da.event_date,
    da.user_id,
    CASE
      WHEN s.signup_date BETWEEN da.event_date - INTERVAL '6 days' AND da.event_date
        THEN 'new'
      ELSE 'returning'
    END AS user_type
  FROM daily_active da
  LEFT JOIN signups s ON da.user_id = s.user_id
)
SELECT
  event_date,
  COUNT(DISTINCT user_id) AS rolling_7d_active,
  COUNT(DISTINCT CASE WHEN user_type = 'new' THEN user_id END) AS new_users,
  COUNT(DISTINCT CASE WHEN user_type = 'returning' THEN user_id END) AS returning_users
FROM classified
WHERE event_date >= (SELECT MIN(event_date) FROM events) + INTERVAL '6 days'
GROUP BY event_date
ORDER BY event_date;
```

**Explanation:** Classify each active user as new or returning based on signup recency, then aggregate. **Interview trick:** Only compute from day 7 onward so the rolling window is full; earlier days have incomplete windows.

---

## Q12: Gaps-and-Islands — Consecutive Active Days

**Tables:** `user_activity(user_id INT, activity_date DATE)`. Find all streaks of consecutive days each user was active.

**Query:**
```sql
WITH numbered AS (
  SELECT
    user_id,
    activity_date,
    activity_date - ROW_NUMBER() OVER (
      PARTITION BY user_id ORDER BY activity_date
    )::INT AS grp
  FROM user_activity
)
SELECT
  user_id,
  MIN(activity_date) AS streak_start,
  MAX(activity_date) AS streak_end,
  COUNT(*) AS streak_length
FROM numbered
GROUP BY user_id, grp
ORDER BY user_id, streak_start;
```

**Explanation:** The gaps-and-islands trick: subtract the row number from the date. Consecutive dates produce the same group value. **Interview trick:** Cast `ROW_NUMBER()` to INT for date subtraction to work in PostgreSQL.

---

## Q13: Gaps-and-Islands — Longest Streak

**Tables:** `user_activity(user_id INT, activity_date DATE)`. Find each user's longest consecutive activity streak.

**Query:**
```sql
WITH streaks AS (
  SELECT
    user_id,
    MIN(activity_date) AS streak_start,
    MAX(activity_date) AS streak_end,
    COUNT(*) AS streak_length,
    MAX(activity_date) - MIN(activity_date) + 1 AS span_days
  FROM (
    SELECT
      user_id,
      activity_date,
      activity_date - ROW_NUMBER() OVER (
        PARTITION BY user_id ORDER BY activity_date
      )::INT AS grp
    FROM user_activity
  ) s
  GROUP BY user_id, grp
),
ranked AS (
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY streak_length DESC) AS rn
  FROM streaks
)
SELECT user_id, streak_start, streak_end, streak_length
FROM ranked
WHERE rn = 1;
```

**Explanation:** Build streaks with gaps-and-islands, then rank by length per user. **Interview trick:** Use `span_days` (end - start + 1) as a sanity check against `COUNT(*)` — they should match for clean date data.

---

## Q14: Consecutive Wins/Losses in Game Results

**Tables:** `game_results(game_id INT, team VARCHAR, result VARCHAR, game_date DATE)`. Find the longest consecutive winning streak per team.

**Query:**
```sql
WITH wins AS (
  SELECT * FROM game_results WHERE result = 'W'
),
streaks AS (
  SELECT
    team,
    MIN(game_date) AS streak_start,
    MAX(game_date) AS streak_end,
    COUNT(*) AS streak_length
  FROM (
    SELECT
      team,
      game_date,
      game_date - ROW_NUMBER() OVER (
        PARTITION BY team ORDER BY game_date
      )::INT AS grp
    FROM wins
  ) s
  GROUP BY team, grp
),
ranked AS (
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY team ORDER BY streak_length DESC) AS rn
  FROM streaks
)
SELECT team, streak_start, streak_end, streak_length
FROM ranked
WHERE rn = 1;
```

**Explanation:** Filter to wins only, then apply gaps-and-islands. **Interview trick:** If the question asks for streaks including losses, remove the filter and use `CASE WHEN result = 'W' THEN 1 ELSE 0 END` with a different grouping strategy.

---

## Q15: Consecutive Wins — Current Streak Status

**Tables:** `game_results(game_id INT, team VARCHAR, result VARCHAR, game_date DATE)`. For each team, find their current streak (ongoing as of the most recent game) and whether it's a win or loss streak.

**Query:**
```sql
WITH ordered AS (
  SELECT
    team,
    result,
    game_date,
    ROW_NUMBER() OVER (PARTITION BY team ORDER BY game_date DESC) AS rn
  FROM game_results
),
streak_groups AS (
  SELECT
    team,
    result AS current_streak_result,
    COUNT(*) AS current_streak_length,
    MAX(game_date) AS last_game_date
  FROM ordered
  WHERE rn <= (
    SELECT COUNT(*) FROM ordered o2
    WHERE o2.team = ordered.team
      AND o2.result = ordered.result
      AND o2.rn >= ordered.rn
  )
  GROUP BY team, result
)
SELECT
  team,
  current_streak_result,
  current_streak_length,
  last_game_date
FROM (
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY team ORDER BY last_game_date DESC) AS final_rn
  FROM streak_groups
) f
WHERE final_rn = 1
ORDER BY team;
```

**Explanation:** Walk backward from the most recent game; count how many consecutive same results before the result changes. **Interview trick:** The correlated subquery counts consecutive same-result rows starting from the most recent.

---

## Q16: Weighted Moving Average (3-Day)

**Tables:** `daily_sales(day DATE, revenue DECIMAL)`. Compute a 3-day weighted moving average where the most recent day has weight 3, middle day weight 2, oldest day weight 1.

**Query:**
```sql
WITH lagged AS (
  SELECT
    day,
    revenue,
    LAG(revenue, 0) OVER (ORDER BY day) AS r0,
    LAG(revenue, 1) OVER (ORDER BY day) AS r1,
    LAG(revenue, 2) OVER (ORDER BY day) AS r2
  FROM daily_sales
)
SELECT
  day,
  revenue,
  ROUND(
    (r0 * 3 + r2 * 2 + r1 * 1) / 6.0,
    2
  ) AS wma_3day
FROM lagged
WHERE r1 IS NOT NULL AND r2 IS NOT NULL
ORDER BY day;
```

**Explanation:** Use LAG to fetch the current and previous two days' revenue, then apply weights. **Interview trick:** The denominator is the sum of weights (3+2+1=6). Ensure the weight assignment direction matches the interviewer's expectation (recent vs. older weighted more).

---

## Q17: Weighted Moving Average (7-Day, Custom Weights)

**Tables:** `stock_prices(trade_date DATE, ticker VARCHAR, close_price DECIMAL)`. Compute a 7-day weighted moving average for AAPL with exponentially decaying weights (most recent = 2^6, oldest = 2^0).

**Query:**
```sql
WITH lagged AS (
  SELECT
    trade_date,
    close_price,
    LAG(close_price, 0) OVER w AS p0,
    LAG(close_price, 1) OVER w AS p1,
    LAG(close_price, 2) OVER w AS p2,
    LAG(close_price, 3) OVER w AS p3,
    LAG(close_price, 4) OVER w AS p4,
    LAG(close_price, 5) OVER w AS p5,
    LAG(close_price, 6) OVER w AS p6
  FROM stock_prices
  WHERE ticker = 'AAPL'
  WINDOW w AS (ORDER BY trade_date)
)
SELECT
  trade_date,
  close_price,
  ROUND(
    (p0*64 + p1*32 + p2*16 + p3*8 + p4*4 + p5*2 + p6*1)
    / 127.0,
    2
  ) AS ema_weighted_7d
FROM lagged
WHERE p6 IS NOT NULL
ORDER BY trade_date;
```

**Explanation:** Exponential weights: 2^6=64, 2^5=32, ..., 2^0=1. Sum of weights = 127. **Interview trick:** This is a simple exponential weighted average; true EMA uses a recursive formula. Clarify with the interviewer which is expected.

---

## Q18: Product Affinity — Customers Who Bought A Also Bought B

**Tables:** `orders(order_id INT, customer_id INT, product_id INT, order_date DATE)`. For each product pair (A, B), count how many customers bought both.

**Query:**
```sql
WITH customer_products AS (
  SELECT DISTINCT customer_id, product_id
  FROM orders
)
SELECT
  a.product_id AS product_a,
  b.product_id AS product_b,
  COUNT(DISTINCT a.customer_id) AS customers_who_bought_both
FROM customer_products a
JOIN customer_products b
  ON a.customer_id = b.customer_id
  AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
HAVING COUNT(DISTINCT a.customer_id) >= 10
ORDER BY customers_who_bought_both DESC;
```

**Explanation:** Self-join on customer_id with `a.product_id < b.product_id` to avoid duplicates and self-pairs. **Interview trick:** The `<` condition ensures each pair appears once (A-B but not B-A). The HAVING clause filters for statistically meaningful pairs.

---

## Q19: Product Affinity — Support and Confidence

**Tables:** `orders(order_id INT, customer_id INT, product_id INT)`. Compute association rules: for each pair (A → B), calculate support, confidence, and lift.

**Query:**
```sql
WITH customer_products AS (
  SELECT DISTINCT customer_id, product_id FROM orders
),
total_customers AS (
  SELECT COUNT(DISTINCT customer_id) AS n FROM orders
),
pair_counts AS (
  SELECT
    a.product_id AS product_a,
    b.product_id AS product_b,
    COUNT(DISTINCT a.customer_id) AS pair_count
  FROM customer_products a
  JOIN customer_products b
    ON a.customer_id = b.customer_id AND a.product_id < b.product_id
  GROUP BY a.product_id, b.product_id
),
product_counts AS (
  SELECT product_id, COUNT(DISTINCT customer_id) AS prod_count
  FROM customer_products
  GROUP BY product_id
)
SELECT
  pc.product_a,
  pc.product_b,
  pc.pair_count,
  ROUND(pc.pair_count::DECIMAL / tc.n, 4) AS support,
  ROUND(pc.pair_count::DECIMAL / pa.prod_count, 4) AS confidence_a_to_b,
  ROUND(
    (pc.pair_count::DECIMAL / tc.n)
    / (pa.prod_count::DECIMAL / tc.n * pb.prod_count::DECIMAL / tc.n),
    4
  ) AS lift
FROM pair_counts pc
CROSS JOIN total_customers tc
JOIN product_counts pa ON pc.product_a = pa.product_id
JOIN product_counts pb ON pc.product_b = pb.product_id
ORDER BY lift DESC;
```

**Explanation:** Support = P(A∩B), Confidence = P(A∩B)/P(A), Lift = Confidence / P(B). **Interview trick:** Lift > 1 means A and B co-occur more than expected by chance — this is the key metric for affinity.

---

## Q20: Recommendation — Co-occurrence Matrix

**Tables:** `purchases(user_id INT, product_id INT)`. Build a co-occurrence matrix showing how often each product pair appears in the same user's purchases.

**Query:**
```sql
WITH user_products AS (
  SELECT DISTINCT user_id, product_id FROM purchases
)
SELECT
  a.product_id AS row_product,
  b.product_id AS col_product,
  COUNT(DISTINCT a.user_id) AS co_occurrence
FROM user_products a
JOIN user_products b
  ON a.user_id = b.user_id
GROUP BY a.product_id, b.product_id
ORDER BY a.product_id, b.product_id;
```

**Explanation:** Self-join on user_id to get all product pairs per user, then count. **Interview trick:** For a pivot/matrix output, use conditional aggregation: `SUM(CASE WHEN col_product = X THEN 1 ELSE 0 END)` per product X.

---

## Q21: Stock Price — Monthly High/Low/First/Last

**Tables:** `stock_prices(trade_date DATE, ticker VARCHAR, open_price DECIMAL, high_price DECIMAL, low_price DECIMAL, close_price DECIMAL, volume INT)`. For each ticker, compute monthly OHLC (open/high/low/close) and total volume.

**Query:**
```sql
-- PostgreSQL
SELECT
  ticker,
  DATE_TRUNC('month', trade_date)::DATE AS month,
  (ARRAY_AGG(close_price ORDER BY trade_date ASC))[1]  AS month_open,
  MAX(high_price)  AS month_high,
  MIN(low_price)   AS month_low,
  (ARRAY_AGG(close_price ORDER BY trade_date DESC))[1]  AS month_close,
  SUM(volume)      AS month_volume
FROM stock_prices
GROUP BY ticker, DATE_TRUNC('month', trade_date)
ORDER BY ticker, month;
```

**Alt1:** Using FIRST_VALUE/LAST_VALUE:
```sql
SELECT DISTINCT
  ticker,
  DATE_TRUNC('month', trade_date)::DATE AS month,
  FIRST_VALUE(close_price) OVER w AS month_open,
  LAST_VALUE(close_price)  OVER w AS month_close
FROM stock_prices
WINDOW w AS (
  PARTITION BY ticker, DATE_TRUNC('month', trade_date)
  ORDER BY trade_date
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
);
```

**Explanation:** `ARRAY_AGG` with ORDER BY lets you pick first/last elements. **Interview trick:** The `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` is required for LAST_VALUE to see beyond the current row.

---

## Q22: Stock Price — Monthly Return and Volatility

**Tables:** `stock_prices(trade_date DATE, ticker VARCHAR, close_price DECIMAL)`. Compute monthly return (% change from month start to month end) and daily return standard deviation (volatility) per month.

**Query:**
```sql
WITH monthly AS (
  SELECT
    ticker,
    DATE_TRUNC('month', trade_date)::DATE AS month,
    FIRST_VALUE(close_price) OVER w AS month_open,
    LAST_VALUE(close_price)  OVER w AS month_close
  FROM stock_prices
  WINDOW w AS (
    PARTITION BY ticker, DATE_TRUNC('month', trade_date)
    ORDER BY trade_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  )
),
returns AS (
  SELECT DISTINCT
    ticker, month, month_open, month_close,
    ROUND((month_close - month_open) / month_open * 100, 2) AS monthly_return_pct
  FROM monthly
),
daily_rets AS (
  SELECT
    ticker,
    DATE_TRUNC('month', trade_date)::DATE AS month,
    (close_price - LAG(close_price) OVER w) / LAG(close_price) OVER w AS daily_return
  FROM stock_prices
  WINDOW w AS (PARTITION BY ticker ORDER BY trade_date)
)
SELECT
  r.ticker,
  r.month,
  r.monthly_return_pct,
  ROUND(STDDEV(d.daily_return) * 100, 4) AS monthly_volatility_pct
FROM returns r
LEFT JOIN daily_rets d ON r.ticker = d.ticker AND r.month = d.month
GROUP BY r.ticker, r.month, r.monthly_return_pct
ORDER BY r.ticker, r.month;
```

**Explanation:** Monthly return is the percentage change from first to last close. Volatility is the standard deviation of daily returns within the month. **Interview trick:** Daily returns must be computed before aggregation; use `LAG` partitioned by ticker.

---

## Q23: Stock Price — Longest Consecutive Up Days

**Tables:** `stock_prices(trade_date DATE, ticker VARCHAR, close_price DECIMAL)`. For each ticker, find the longest streak of consecutive days where close > previous close.

**Query:**
```sql
WITH changes AS (
  SELECT
    ticker,
    trade_date,
    close_price,
    CASE WHEN close_price > LAG(close_price) OVER (PARTITION BY ticker ORDER BY trade_date)
         THEN 1 ELSE 0
    END AS is_up
  FROM stock_prices
),
streaks AS (
  SELECT
    ticker,
    trade_date,
    is_up,
    trade_date - ROW_NUMBER() OVER (
      PARTITION BY ticker, is_up ORDER BY trade_date
    )::INT AS grp
  FROM changes
  WHERE is_up = 1
),
streak_lengths AS (
  SELECT
    ticker,
    MIN(trade_date) AS streak_start,
    MAX(trade_date) AS streak_end,
    COUNT(*) AS streak_days
  FROM streaks
  GROUP BY ticker, grp
),
ranked AS (
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY streak_days DESC) AS rn
  FROM streak_lengths
)
SELECT ticker, streak_start, streak_end, streak_days
FROM ranked
WHERE rn = 1;
```

**Explanation:** Flag up days, filter to up days only, then apply gaps-and-islands. **Interview trick:** The partition includes `is_up` to restart grouping for non-up days.

---

## Q24: Transactions — Running Balance

**Tables:** `transactions(id INT, account_id INT, amount DECIMAL, txn_type VARCHAR, txn_time TIMESTAMP)`. `txn_type` is 'credit' or 'debit'. Compute the running balance per account ordered by time.

**Query:**
```sql
SELECT
  id,
  account_id,
  amount,
  txn_type,
  txn_time,
  SUM(CASE WHEN txn_type = 'credit' THEN amount ELSE -amount END)
    OVER (PARTITION BY account_id ORDER BY txn_time) AS running_balance
FROM transactions
ORDER BY account_id, txn_time;
```

**Explanation:** Convert credits to positive and debits to negative, then use a running SUM. **Interview trick:** Always clarify whether `amount` is stored as positive for both types — the CASE handles the sign conversion.

---

## Q25: Transactions — Detect Minimum Balance Violations (Negative)

**Tables:** `transactions(id INT, account_id INT, amount DECIMAL, txn_type VARCHAR, txn_time TIMESTAMP)`. Find accounts that ever had a negative running balance, and identify the first violating transaction.

**Query:**
```sql
WITH running AS (
  SELECT
    *,
    SUM(CASE WHEN txn_type = 'credit' THEN amount ELSE -amount END)
      OVER (PARTITION BY account_id ORDER BY txn_time) AS balance,
    ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY txn_time) AS txn_seq
  FROM transactions
),
violations AS (
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY txn_time) AS violation_rank
  FROM running
  WHERE balance < 0
)
SELECT account_id, id AS first_violating_txn, balance
FROM violations
WHERE violation_rank = 1;
```

**Explanation:** Compute running balance, filter for negative balances, then pick the first per account. **Interview trick:** Use `ROW_NUMBER` twice: once for ordering within the partition and once to isolate the first violation.

---

## Q26: Time Difference Between Consecutive Events

**Tables:** `clicks(user_id INT, page VARCHAR, click_time TIMESTAMP)`. For each user, compute the time gap (in seconds) between consecutive clicks.

**Query:**
```sql
SELECT
  user_id,
  page,
  click_time,
  EXTRACT(EPOCH FROM
    click_time - LAG(click_time) OVER (PARTITION BY user_id ORDER BY click_time)
  ) AS seconds_since_last_click
FROM clicks
ORDER BY user_id, click_time;
```

**Explanation:** `LAG` gets the previous click time; `EXTRACT(EPOCH)` gives the difference in seconds. **Interview trick:** The first event per user returns NULL — handle with `COALESCE(..., 0)` if the business logic requires it.

---

## Q27: Percentiles of Time Between Events

**Tables:** `page_views(user_id INT, view_time TIMESTAMP)`. Compute the 25th, 50th, 75th, and 95th percentiles of the time gap between consecutive page views per user.

**Query:**
```sql
-- PostgreSQL
WITH gaps AS (
  SELECT
    user_id,
    EXTRACT(EPOCH FROM
      view_time - LAG(view_time) OVER (PARTITION BY user_id ORDER BY view_time)
    ) AS gap_seconds
  FROM page_views
)
SELECT
  PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY gap_seconds) AS p25,
  PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY gap_seconds) AS p50,
  PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY gap_seconds) AS p75,
  PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY gap_seconds) AS p95
FROM gaps
WHERE gap_seconds IS NOT NULL;
```

**Alt1:** MySQL approach with NTILE:
```sql
-- MySQL
WITH gaps AS (
  SELECT
    EXTRACT(SECOND FROM
      view_time - LAG(view_time) OVER (PARTITION BY user_id ORDER BY view_time)
    ) AS gap_seconds,
    NTILE(4) OVER (ORDER BY
      EXTRACT(SECOND FROM view_time - LAG(view_time) OVER (
        PARTITION BY user_id ORDER BY view_time
      ))
    ) AS quartile
  FROM page_views
)
SELECT
  MAX(CASE WHEN quartile = 1 THEN gap_seconds END) AS p25,
  MAX(CASE WHEN quartile = 2 THEN gap_seconds END) AS p50,
  MAX(CASE WHEN quartile = 3 THEN gap_seconds END) AS p75
FROM gaps;
```

**Explanation:** Compute gaps with LAG, then use `PERCENTILE_CONT` for exact percentiles. **Interview trick:** `PERCENTILE_CONT` interpolates; `PERCENTILE_DISC` returns an actual value from the dataset. Choose based on requirements.

---

## Q28: Split Into Quarters and Analyze Revenue

**Tables:** `orders(order_id INT, order_date DATE, revenue DECIMAL, region VARCHAR)`. Split each year into quarters and compute total revenue, order count, and average order value per region per quarter.

**Query:**
```sql
SELECT
  EXTRACT(YEAR FROM order_date) AS order_year,
  EXTRACT(QUARTER FROM order_date) AS order_quarter,
  region,
  SUM(revenue) AS total_revenue,
  COUNT(*) AS order_count,
  ROUND(AVG(revenue), 2) AS avg_order_value,
  ROUND(
    100.0 * SUM(revenue) / SUM(SUM(revenue)) OVER (
      PARTITION BY EXTRACT(YEAR FROM order_date)
    ), 2
  ) AS pct_of_yearly_revenue
FROM orders
GROUP BY EXTRACT(YEAR FROM order_date), EXTRACT(QUARTER FROM order_date), region
ORDER BY order_year, order_quarter, region;
```

**Explanation:** Extract year and quarter, aggregate, then compute each region's share of yearly revenue. **Interview trick:** The `SUM(SUM(revenue)) OVER (PARTITION BY year)` is a window of an aggregate — a powerful pattern for percentages of totals.

---

## Q29: Decile Analysis of Customer Spend

**Tables:** `orders(customer_id INT, revenue DECIMAL)`. Split customers into 10 deciles based on total spend and show revenue distribution.

**Query:**
```sql
WITH customer_spend AS (
  SELECT customer_id, SUM(revenue) AS total_spend
  FROM orders
  GROUP BY customer_id
),
deciled AS (
  SELECT
    customer_id,
    total_spend,
    NTILE(10) OVER (ORDER BY total_spend) AS spend_decile
  FROM customer_spend
)
SELECT
  spend_decile,
  COUNT(*) AS customer_count,
  ROUND(MIN(total_spend), 2) AS min_spend,
  ROUND(AVG(total_spend), 2) AS avg_spend,
  ROUND(MAX(total_spend), 2) AS max_spend,
  ROUND(SUM(total_spend), 2) AS total_spend_in_decile,
  ROUND(100.0 * SUM(total_spend) / SUM(SUM(total_spend)) OVER (), 2) AS pct_of_total_revenue
FROM deciled
GROUP BY spend_decile
ORDER BY spend_decile;
```

**Explanation:** `NTILE(10)` splits rows into 10 equal-ish groups. **Interview trick:** Decile 1 = lowest spenders, decile 10 = highest. The Pareto principle often shows ~80% of revenue from the top 2 deciles.

---

## Q30: Symmetric Pair Finding (Friend Pairs A-B)

**Tables:** `friendships(user_id INT, friend_id INT)`. Each friendship is stored once (e.g., (1,2) exists but (2,1) may not). Find all unique friendship pairs.

**Query:**
```sql
SELECT
  LEAST(user_id, friend_id) AS person_a,
  GREATEST(user_id, friend_id) AS person_b
FROM friendships
GROUP BY LEAST(user_id, friend_id), GREATEST(user_id, friend_id)
HAVING COUNT(*) = 1
ORDER BY person_a, person_b;
```

**Explanation:** `LEAST/GREATEST` normalizes (1,2) and (2,1) into the same canonical form. **Interview trick:** `HAVING COUNT(*) = 1` ensures you only get one-sided friendships (the other direction is missing). For mutual friendships stored in both directions, use `HAVING COUNT(*) = 2`.

---

## Q31: Mutual Friends Count

**Tables:** `friendships(user_id INT, friend_id INT)`. Friendships are stored in both directions (A→B and B→A). For each pair of users, compute how many mutual friends they have.

**Query:**
```sql
SELECT
  a.user_id AS user_1,
  b.user_id AS user_2,
  COUNT(*) AS mutual_friends
FROM friendships a
JOIN friendships b
  ON a.friend_id = b.friend_id
  AND a.user_id < b.user_id
GROUP BY a.user_id, b.user_id
HAVING COUNT(*) >= 3
ORDER BY mutual_friends DESC, user_1, user_2;
```

**Explanation:** Two users share a friend if they both have the same `friend_id`. The `<` condition avoids duplicate pairs. **Interview trick:** The `HAVING COUNT(*) >= 3` threshold filters noise; adjust based on requirements.

---

## Q32: Followers Graph — Reach (Friends of Friends)

**Tables:** `follows(follower_id INT, followee_id INT)`. For each user, compute the size of their 2-hop network (friends of friends, excluding themselves and direct follows).

**Query:**
```sql
WITH fof AS (
  SELECT DISTINCT
    a.follower_id AS user_id,
    b.followee_id AS fof_user
  FROM follows a
  JOIN follows b ON a.followee_id = b.follower_id
  WHERE b.followee_id != a.follower_id
),
direct AS (
  SELECT DISTINCT follower_id, followee_id FROM follows
)
SELECT
  f.user_id,
  COUNT(DISTINCT f.fof_user) AS reach_count
FROM fof f
LEFT JOIN direct d
  ON f.user_id = d.follower_id AND f.fof_user = d.followee_id
WHERE d.followee_id IS NULL
GROUP BY f.user_id
ORDER BY reach_count DESC;
```

**Explanation:** Self-join follows to get 2-hop connections, then exclude direct follows. **Interview trick:** The LEFT JOIN ... WHERE IS NULL pattern is the classic anti-join to exclude existing direct connections.

---

## Q33: Leaderboard With Dense Rank and Position Ties

**Tables:** `scores(player_id INT, game_date DATE, score INT)`. Build a leaderboard using DENSE_RANK so tied scores share positions, and compute each player's movement from the previous day.

**Query:**
```sql
WITH daily_scores AS (
  SELECT player_id, game_date, SUM(score) AS total_score
  FROM scores
  GROUP BY player_id, game_date
),
ranked AS (
  SELECT
    player_id,
    game_date,
    total_score,
    DENSE_RANK() OVER (PARTITION BY game_date ORDER BY total_score DESC) AS position,
    LAG(DENSE_RANK() OVER (PARTITION BY game_date ORDER BY total_score DESC))
      OVER (PARTITION BY player_id ORDER BY game_date) AS prev_position
  FROM daily_scores
)
SELECT
  player_id,
  game_date,
  total_score,
  position,
  prev_position,
  CASE
    WHEN prev_position IS NULL THEN 'new'
    WHEN position < prev_position THEN 'up'
    WHEN position > prev_position THEN 'down'
    ELSE 'same'
  END AS movement
FROM ranked
ORDER BY game_date, position;
```

**Explanation:** `DENSE_RANK` gives positions without gaps (1,1,2 not 1,1,3). `LAG` on the rank shows movement. **Interview trick:** `DENSE_RANK` vs `RANK` vs `ROW_NUMBER` — interviewers will test if you know the difference. DENSE_RANK: ties share rank, no gaps.

---

## Q34: Rank Retention Over Time — User Moves Up/Down

**Tables:** `monthly_rankings(month DATE, user_id INT, revenue DECIMAL)`. Track each user's rank month over month and classify their trajectory.

**Query:**
```sql
WITH ranked AS (
  SELECT
    month,
    user_id,
    revenue,
    DENSE_RANK() OVER (PARTITION BY month ORDER BY revenue DESC) AS rank_pos
  FROM monthly_rankings
),
with_lag AS (
  SELECT
    month,
    user_id,
    revenue,
    rank_pos,
    LAG(rank_pos) OVER (PARTITION BY user_id ORDER BY month) AS prev_rank,
    LAG(rank_pos, 3) OVER (PARTITION BY user_id ORDER BY month) AS rank_3mo_ago
  FROM ranked
)
SELECT
  month,
  user_id,
  revenue,
  rank_pos,
  prev_rank,
  CASE
    WHEN prev_rank IS NULL THEN 'new entrant'
    WHEN rank_pos < prev_rank THEN 'improved'
    WHEN rank_pos > prev_rank THEN 'declined'
    ELSE 'stable'
  END AS trend,
  CASE
    WHEN rank_3mo_ago IS NOT NULL AND rank_pos < rank_3mo_ago THEN 'rising star'
    WHEN rank_3mo_ago IS NOT NULL AND rank_pos > rank_3mo_ago THEN 'fading'
  END AS long_term_trend
FROM with_lag
ORDER BY month, rank_pos;
```

**Explanation:** Compute rank per month, then use LAG to compare with previous and 3-month-ago ranks. **Interview trick:** The 3-month-ago comparison (LAG with offset 3) reveals longer-term trends vs short-term noise.

---

## Q35: Slow Signals — Forward-Fill NULLs (Compass)

**Tables:** `sensor_data(sensor_id INT, reading_time TIMESTAMP, temperature DECIMAL)`. Temperature has NULL gaps. Forward-fill NULLs with the last known non-NULL value.

**Query:**
```sql
-- PostgreSQL
WITH filled_groups AS (
  SELECT
    sensor_id,
    reading_time,
    temperature,
    COUNT(temperature) OVER (
      PARTITION BY sensor_id ORDER BY reading_time
    ) AS grp
  FROM sensor_data
)
SELECT
  sensor_id,
  reading_time,
  FIRST_VALUE(temperature) OVER (
    PARTITION BY sensor_id, grp ORDER BY reading_time
  ) AS temperature_filled
FROM filled_groups;
```

**Alt1:** Using a CTE with MAX:
```sql
WITH numbered AS (
  SELECT
    sensor_id,
    reading_time,
    temperature,
    SUM(CASE WHEN temperature IS NOT NULL THEN 1 ELSE 0 END)
      OVER (PARTITION BY sensor_id ORDER BY reading_time) AS grp
  FROM sensor_data
)
SELECT
  sensor_id,
  reading_time,
  MAX(temperature) OVER (
    PARTITION BY sensor_id, grp ORDER BY reading_time
  ) AS temperature_filled
FROM numbered;
```

**Explanation:** A running count of non-NULL values creates groups. Within each group, `FIRST_VALUE` or `MAX` (since only one non-NULL exists) fills the NULLs. **Interview trick:** This is the classic "forward fill" / "last observation carried forward" pattern — essential for time-series data with gaps.

---

## Q36: Rolling Max With Window Frame

**Tables:** `server_metrics(server_id INT, check_time TIMESTAMP, cpu_usage DECIMAL)`. For each check, compute the rolling maximum CPU usage over the last 10 checks per server.

**Query:**
```sql
SELECT
  server_id,
  check_time,
  cpu_usage,
  MAX(cpu_usage) OVER (
    PARTITION BY server_id
    ORDER BY check_time
    ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
  ) AS rolling_max_cpu
FROM server_metrics
ORDER BY server_id, check_time;
```

**Explanation:** `ROWS BETWEEN 9 PRECEDING AND CURRENT ROW` creates a window of exactly 10 rows. **Interview trick:** `ROWS` counts physical rows; `RANGE` counts logical values. Use ROWS for row-count windows, RANGE for value-based windows.

---

## Q37: Cumulative Distribution Function (CDF)

**Tables:** `orders(order_id INT, amount DECIMAL)`. Compute the cumulative distribution of order amounts — what fraction of orders are ≤ each amount.

**Query:**
```sql
-- PostgreSQL
SELECT
  amount,
  COUNT(*) AS orders_at_amount,
  SUM(COUNT(*)) OVER (ORDER BY amount) AS cumulative_orders,
  ROUND(
    CUME_DIST() OVER (ORDER BY amount),
    4
  ) AS cumulative_distribution
FROM orders
GROUP BY amount
ORDER BY amount;
```

**Alt1:** Manual CDF with window SUM:
```sql
WITH sorted AS (
  SELECT
    amount,
    COUNT(*) AS freq
  FROM orders
  GROUP BY amount
)
SELECT
  amount,
  freq,
  SUM(freq) OVER (ORDER BY amount) AS cumulative_count,
  ROUND(
    SUM(freq) OVER (ORDER BY amount)::DECIMAL
    / SUM(freq) OVER (),
    4
  ) AS cdf
FROM sorted
ORDER BY amount;
```

**Explanation:** `CUME_DIST()` returns the fraction of rows with values ≤ the current row. **Interview trick:** `CUME_DIST` includes the current row; `PERCENT_RANK` excludes it (uses rank-1 / total-1). Know the difference.

---

## Q38: Heat Tiers via NTILE

**Tables:** `page_views(page_url VARCHAR, view_count INT, day DATE)`. Classify pages into 4 heat tiers (hot/warm/cool/cold) based on daily view count using NTILE.

**Query:**
```sql
WITH tiered AS (
  SELECT
    page_url,
    day,
    view_count,
    NTILE(4) OVER (PARTITION BY day ORDER BY view_count DESC) AS heat_tier
  FROM page_views
)
SELECT
  page_url,
  day,
  view_count,
  CASE heat_tier
    WHEN 1 THEN 'hot'
    WHEN 2 THEN 'warm'
    WHEN 3 THEN 'cool'
    WHEN 4 THEN 'cold'
  END AS heat_label
FROM tiered
ORDER BY day, heat_tier;
```

**Explanation:** `NTILE(4)` splits each day's pages into 4 equal groups. **Interview trick:** NTILE distributes rows as evenly as possible; with 10 pages, groups are 3,3,2,2. The `PARTITION BY day` ensures tiers are recalculated daily.

---

## Q39: Top Page Per Session

**Tables:** `page_views(session_id INT, page_url VARCHAR, view_time TIMESTAMP, user_id INT)`. For each session, find the page that received the most views.

**Query:**
```sql
WITH page_counts AS (
  SELECT
    session_id,
    user_id,
    page_url,
    COUNT(*) AS views,
    ROW_NUMBER() OVER (
      PARTITION BY session_id
      ORDER BY COUNT(*) DESC
    ) AS rn
  FROM page_views
  GROUP BY session_id, user_id, page_url
)
SELECT session_id, user_id, page_url, views
FROM page_counts
WHERE rn = 1;
```

**Explanation:** Count views per page per session, rank within session, pick the top. **Interview trick:** Use ROW_NUMBER (picks one even with ties) vs DENSE_RANK (returns all ties) based on business requirements.

---

## Q40: Purchase Probability — Bayesian Approach

**Tables:** `product_views(user_id INT, product_id INT, view_time TIMESTAMP)`, `purchases(user_id INT, product_id INT, purchase_time TIMESTAMP)`. For each product, compute P(purchase | viewed).

**Query:**
```sql
WITH viewers AS (
  SELECT user_id, product_id, COUNT(*) AS view_count
  FROM product_views
  GROUP BY user_id, product_id
),
buyers AS (
  SELECT user_id, product_id, 1 AS purchased
  FROM purchases
  GROUP BY user_id, product_id
),
combined AS (
  SELECT
    v.user_id,
    v.product_id,
    v.view_count,
    COALESCE(b.purchased, 0) AS purchased
  FROM viewers v
  LEFT JOIN buyers b ON v.user_id = b.user_id AND v.product_id = b.product_id
)
SELECT
  product_id,
  COUNT(*) AS total_viewers,
  SUM(purchased) AS total_buyers,
  ROUND(
    SUM(purchased)::DECIMAL / COUNT(*),
    4
  ) AS purchase_probability,
  ROUND(
    AVG(view_count) FILTER (WHERE purchased = 1),
    2
  ) AS avg_views_before_purchase,
  ROUND(
    AVG(view_count) FILTER (WHERE purchased = 0),
    2
  ) AS avg_views_no_purchase
FROM combined
GROUP BY product_id
ORDER BY purchase_probability DESC;
```

**Explanation:** Join viewers with buyers, compute conversion rate per product. **Interview trick:** The `FILTER (WHERE ...)` clause is PostgreSQL-specific; in MySQL use `AVG(CASE WHEN purchased = 1 THEN view_count END)`.

---

## Q41: Business Days Difference Excluding Holidays

**Tables:** `projects(project_id INT, start_date DATE, end_date DATE)`, `holidays(holiday_date DATE)`. Compute the number of business days (weekdays excluding holidays) between start and end dates.

**Query:**
```sql
-- PostgreSQL
WITH date_range AS (
  SELECT
    project_id,
    start_date,
    end_date,
    GENERATE_SERIES(start_date, end_date, INTERVAL '1 day')::DATE AS dt
  FROM projects
)
SELECT
  dr.project_id,
  dr.start_date,
  dr.end_date,
  COUNT(*) AS business_days
FROM date_range dr
LEFT JOIN holidays h ON dr.dt = h.holiday_date
WHERE EXTRACT(DOW FROM dr.dt) NOT IN (0, 6)
  AND h.holiday_date IS NULL
GROUP BY dr.project_id, dr.start_date, dr.end_date;
```

**Alt1:** SQL Server approach:
```sql
-- SQL Server
SELECT
  project_id,
  start_date,
  end_date,
  DATEDIFF(day, start_date, end_date)
    - 2 * (DATEDIFF(week, start_date, end_date))
    - (
      SELECT COUNT(*)
      FROM holidays
      WHERE holiday_date BETWEEN start_date AND end_date
    ) AS business_days
FROM projects;
```

**Explanation:** Generate all dates in the range, exclude weekends (DOW 0=Sun, 6=Sat) and holidays. **Interview trick:** `GENERATE_SERIES` is PostgreSQL; for MySQL use a numbers table or recursive CTE. The SQL Server approach is O(1) per project.

---

## Q42: Ranked Percentile — Assign Percentile Rank to Rows

**Tables:** `salaries(employee_id INT, department VARCHAR, salary DECIMAL)`. Assign each employee a percentile rank within their department based on salary.

**Query:**
```sql
SELECT
  employee_id,
  department,
  salary,
  ROUND(PERCENT_RANK() OVER (
    PARTITION BY department ORDER BY salary
  ) * 100, 1) AS percentile_rank,
  ROUND(CUME_DIST() OVER (
    PARTITION BY department ORDER BY salary
  ) * 100, 1) AS cumulative_pct
FROM salaries
ORDER BY department, salary;
```

**Explanation:** `PERCENT_RANK` = (rank-1) / (total-1). `CUME_DIST` = rank / total. **Interview trick:** PERCENT_RANK gives 0 for the lowest value; CUME_DIST gives the fraction of values ≤ the current value. Use PERCENT_RANK for relative standing.

---

## Q43: Deltas vs Previous Period — Percentage Change

**Tables:** `monthly_sales(month DATE, region VARCHAR, revenue DECIMAL)`. Compute month-over-month and year-over-year percentage change in revenue per region.

**Query:**
```sql
WITH lagged AS (
  SELECT
    month,
    region,
    revenue,
    LAG(revenue, 1) OVER (PARTITION BY region ORDER BY month) AS prev_month_rev,
    LAG(revenue, 12) OVER (PARTITION BY region ORDER BY month) AS prev_year_rev
  FROM monthly_sales
)
SELECT
  month,
  region,
  revenue,
  prev_month_rev,
  ROUND(
    (revenue - prev_month_rev) / NULLIF(prev_month_rev, 0) * 100, 2
  ) AS mom_pct_change,
  prev_year_rev,
  ROUND(
    (revenue - prev_year_rev) / NULLIF(prev_year_rev, 0) * 100, 2
  ) AS yoy_pct_change
FROM lagged
ORDER BY region, month;
```

**Explanation:** `LAG(revenue, 1)` for MoM, `LAG(revenue, 12)` for YoY. **Interview trick:** `NULLIF(prev, 0)` prevents division by zero. Always clarify if the denominator should be the previous period or an average of both periods.

---

## Q44: Interpolation — Fill Missing Dates

**Tables:** `daily_metrics(metric_date DATE, metric_value DECIMAL)`. Some dates are missing. Fill gaps by linear interpolation between the nearest known values.

**Query:**
```sql
-- PostgreSQL
WITH all_dates AS (
  SELECT GENERATE_SERIES(
    (SELECT MIN(metric_date) FROM daily_metrics),
    (SELECT MAX(metric_date) FROM daily_metrics),
    INTERVAL '1 day'
  )::DATE AS metric_date
),
base AS (
  SELECT
    a.metric_date,
    m.metric_value,
    SUM(CASE WHEN m.metric_value IS NOT NULL THEN 1 ELSE 0 END)
      OVER (ORDER BY a.metric_date) AS grp
  FROM all_dates a
  LEFT JOIN daily_metrics m ON a.metric_date = m.metric_date
),
bounds AS (
  SELECT
    metric_date,
    grp,
    metric_value,
    FIRST_VALUE(metric_value) OVER w AS start_val,
    LAST_VALUE(metric_value)  OVER w AS end_val,
    FIRST_VALUE(metric_date)  OVER w AS start_date,
    LAST_VALUE(metric_date)   OVER w AS end_date
  FROM base
  WINDOW w AS (
    PARTITION BY grp ORDER BY metric_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  )
)
SELECT
  metric_date,
  ROUND(
    CASE
      WHEN metric_value IS NOT NULL THEN metric_value
      ELSE start_val + (end_val - start_val)
        * (metric_date - start_date)::DECIMAL
        / NULLIF(end_date - start_date, 0)
    END,
    2
  ) AS interpolated_value
FROM bounds
ORDER BY metric_date;
```

**Explanation:** Identify non-NULL segments with a running COUNT, then use FIRST_VALUE/LAST_VALUE to get segment bounds. Interpolate linearly within each segment. **Interview trick:** This is a critical data cleaning technique. Clarify whether to forward-fill, backward-fill, or interpolate.

---

## Q45: Percentile Buckets for A/B Test Analysis

**Tables:** `ab_tests(user_id INT, variant VARCHAR, metric_value DECIMAL)`. Split users into 20 percentile buckets by metric value, then compare distributions across variants.

**Query:**
```sql
WITH percentiled AS (
  SELECT
    user_id,
    variant,
    metric_value,
    NTILE(20) OVER (PARTITION BY variant ORDER BY metric_value) AS pct_bucket
  FROM ab_tests
)
SELECT
  variant,
  pct_bucket,
  COUNT(*) AS users,
  ROUND(MIN(metric_value), 2) AS bucket_min,
  ROUND(AVG(metric_value), 2) AS bucket_avg,
  ROUND(MAX(metric_value), 2) AS bucket_max
FROM percentiled
GROUP BY variant, pct_bucket
ORDER BY variant, pct_bucket;
```

**Explanation:** NTILE(20) splits each variant into 20 equal groups. **Interview trick:** Comparing bucket-level statistics across variants reveals distributional differences that a simple mean comparison would miss.

---

## Q46: Event Sequence Pattern Detection

**Tables:** `events(user_id INT, event_type VARCHAR, event_time TIMESTAMP)`. Find users who performed the sequence: 'signup' → 'view_product' → 'add_to_cart' → 'purchase' within 24 hours.

**Query:**
```sql
WITH ordered_events AS (
  SELECT
    user_id,
    event_type,
    event_time,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_time) AS seq
  FROM events
  WHERE event_type IN ('signup', 'view_product', 'add_to_cart', 'purchase')
),
sequences AS (
  SELECT
    a.user_id,
    a.event_time AS signup_time,
    d.event_time AS purchase_time,
    EXTRACT(EPOCH FROM d.event_time - a.event_time) / 3600.0 AS hours_to_purchase
  FROM ordered_events a
  JOIN ordered_events b
    ON a.user_id = b.user_id AND b.event_type = 'view_product' AND b.seq = a.seq + 1
  JOIN ordered_events c
    ON a.user_id = c.user_id AND c.event_type = 'add_to_cart' AND c.seq = a.seq + 2
  JOIN ordered_events d
    ON a.user_id = d.user_id AND d.event_type = 'purchase' AND d.seq = a.seq + 3
  WHERE a.event_type = 'signup'
)
SELECT user_id, signup_time, purchase_time, ROUND(hours_to_purchase, 2) AS hours
FROM sequences
WHERE hours_to_purchase <= 24
ORDER BY hours_to_purchase;
```

**Explanation:** Use ROW_NUMBER to assign sequence positions, then join on consecutive positions matching the expected event types. **Interview trick:** The join pattern (a.seq+1, a.seq+2, a.seq+3) enforces strict ordering. Relax to `b.seq > a.seq` for non-strict sequences.

---

## Q47: Time Between Consecutive Logins — User Engagement

**Tables:** `logins(user_id INT, login_time TIMESTAMP)`. Compute the average, median, and P90 time between consecutive logins per user.

**Query:**
```sql
-- PostgreSQL
WITH gaps AS (
  SELECT
    user_id,
    EXTRACT(EPOCH FROM
      login_time - LAG(login_time) OVER (PARTITION BY user_id ORDER BY login_time)
    ) / 3600.0 AS hours_between
  FROM logins
)
SELECT
  user_id,
  ROUND(AVG(hours_between), 2) AS avg_hours,
  ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY hours_between), 2) AS median_hours,
  ROUND(PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY hours_between), 2) AS p90_hours,
  COUNT(*) AS login_count
FROM gaps
WHERE hours_between IS NOT NULL
GROUP BY user_id
HAVING COUNT(*) >= 5
ORDER BY avg_hours;
```

**Explanation:** Compute gaps with LAG, then aggregate with multiple percentile functions. **Interview trick:** The HAVING clause ensures statistical significance — you need at least a few gaps to compute meaningful percentiles.

---

## Q48: Quarterly Ranking Changes — Migration Matrix

**Tables:** `quarterly_revenue(quarter VARCHAR, customer_id INT, revenue DECIMAL)`. Build a migration matrix showing how many customers moved between revenue deciles from one quarter to the next.

**Query:**
```sql
WITH ranked AS (
  SELECT
    quarter,
    customer_id,
    revenue,
    NTILE(10) OVER (PARTITION BY quarter ORDER BY revenue) AS decile
  FROM quarterly_revenue
),
paired AS (
  SELECT
    a.customer_id,
    a.quarter AS from_quarter,
    b.quarter AS to_quarter,
    a.decile AS from_decile,
    b.decile AS to_decile
  FROM ranked a
  JOIN ranked b
    ON a.customer_id = b.customer_id
    AND b.quarter = (
      SELECT MAX(quarter) FROM quarterly_revenue WHERE quarter > a.quarter
    )
)
SELECT
  from_decile,
  to_decile,
  COUNT(*) AS customers
FROM paired
GROUP BY from_decile, to_decile
ORDER BY from_decile, to_decile;
```

**Explanation:** Rank customers into deciles per quarter, then self-join to compare consecutive quarters. **Interview trick:** The correlated subquery for the next quarter is cleaner than hardcoding quarter values; for Oracle, use `LEAD(quarter)` in a window.

---

## Q49: Decile-Based Revenue Concentration (Pareto)

**Tables:** `sales(product_id INT, revenue DECIMAL)`. Show what percentage of total revenue comes from the top 10%, 20%, etc. of products (Pareto analysis).

**Query:**
```sql
WITH product_revenue AS (
  SELECT product_id, SUM(revenue) AS total_revenue
  FROM sales
  GROUP BY product_id
),
ranked AS (
  SELECT
    product_id,
    total_revenue,
    ROW_NUMBER() OVER (ORDER BY total_revenue DESC) AS rn,
    COUNT(*) OVER () AS total_products
  FROM product_revenue
),
cumulative AS (
  SELECT
    product_id,
    total_revenue,
    rn,
    total_products,
    ROUND(rn::DECIMAL / total_products * 100, 1) AS pct_products,
    SUM(total_revenue) OVER (ORDER BY total_revenue DESC) AS cum_revenue
  FROM ranked
)
SELECT
  product_id,
  total_revenue,
  pct_products,
  ROUND(cum_revenue / SUM(total_revenue) OVER () * 100, 2) AS cum_revenue_pct
FROM cumulative
WHERE pct_products <= 30
ORDER BY rn;
```

**Explanation:** Rank products by revenue, compute cumulative percentage. **Interview trick:** Classic Pareto: typically ~20% of products drive ~80% of revenue. The WHERE clause focuses on the top 30% for readability.

---

## Q50: Symmetric Pair Validation — Bidirectional Friendship Check

**Tables:** `friendships(user_id INT, friend_id INT)`. Find asymmetric friendships where A follows B but B does not follow A back.

**Query:**
```sql
SELECT
  a.user_id AS follower,
  a.friend_id AS followee
FROM friendships a
LEFT JOIN friendships b
  ON a.friend_id = b.user_id AND b.friend_id = a.user_id
WHERE b.user_id IS NULL
ORDER BY a.user_id, a.friend_id;
```

**Explanation:** Self-join where the reverse pair should exist; LEFT JOIN + WHERE NULL finds missing reversals. **Interview trick:** This anti-join pattern is fundamental for data integrity checks. For bidirectional systems, you'd enforce both rows exist or use a canonical form (Q30).

---

## Q51: Churn Detection — Idle Users Feature Set

**Tables:** `events(user_id INT, event_time TIMESTAMP)`, `signups(user_id INT, signup_date DATE)`. Build a feature set for churn prediction: for each user, compute their activity in the last 7/30/90 days versus their total activity.

**Query:**
```sql
WITH user_stats AS (
  SELECT
    user_id,
    COUNT(*) AS total_events,
    COUNT(DISTINCT event_time::DATE) AS active_days
  FROM events
  GROUP BY user_id
),
recent_stats AS (
  SELECT
    user_id,
    COUNT(*) FILTER (WHERE event_time >= CURRENT_DATE - INTERVAL '7 days') AS events_7d,
    COUNT(*) FILTER (WHERE event_time >= CURRENT_DATE - INTERVAL '30 days') AS events_30d,
    COUNT(DISTINCT event_time::DATE)
      FILTER (WHERE event_time >= CURRENT_DATE - INTERVAL '90 days') AS active_days_90d
  FROM events
  GROUP BY user_id
)
SELECT
  s.user_id,
  s.signup_date,
  u.total_events,
  u.active_days,
  r.events_7d,
  r.events_30d,
  r.active_days_90d,
  CASE
    WHEN r.events_30d = 0 THEN 'churned'
    WHEN r.events_7d = 0 THEN 'at_risk'
    ELSE 'active'
  END AS churn_risk
FROM signups s
LEFT JOIN user_stats u ON s.user_id = u.user_id
LEFT JOIN recent_stats r ON s.user_id = r.user_id;
```

**Explanation:** Compute activity aggregates over multiple windows, then bucket users by recency. **Interview trick:** This mirrors production churn models — recency (7d/30d activity) is usually the strongest predictor. The `FILTER (WHERE ...)` is PostgreSQL; for MySQL use `SUM(CASE WHEN ...)`.

---

## Q52: Friend Recommendations — Friends of Friends Not Yet Friends

**Tables:** `friendships(user_id INT, friend_id INT)`, bidirectional (both directions stored). Recommend friends: for user 1, list people who are 2 hops away but not already friends.

**Query:**
```sql
WITH my_friends AS (
  SELECT friend_id FROM friendships WHERE user_id = 1
),
friend_friends AS (
  SELECT DISTINCT f.friend_id AS candidate
  FROM friendships f
  JOIN my_friends m ON f.user_id = m.friend_id
  WHERE f.friend_id != 1
)
SELECT
  ff.candidate AS recommended_user,
  COUNT(*) AS mutual_friends_count,
  STRING_AGG(mf.friend_id::VARCHAR, ', ' ORDER BY mf.friend_id) AS mutual_friend_list
FROM friend_friends ff
JOIN friendships mf ON mf.user_id = ff.candidate
JOIN my_friends m ON mf.friend_id = m.friend_id
WHERE ff.candidate NOT IN (SELECT friend_id FROM my_friends)
GROUP BY ff.candidate
ORDER BY mutual_friends_count DESC;
```

**Explanation:** Compute my bag of friends, find people who are friends of my friends, then exclude people already in my friend set. **Interview trick:** The `STRING_AGG` shows the shared connection paths — interviewers love asking why not to recommend direct friends (duplicate/self filtering reasons).

---

## Q53: Follower Graph — Influence Score (Shortest Path Reach)

**Tables:** `follows(follower_id INT, followee_id INT)`. Compute the number of unique users reachable within 2 hops for each influencer.

**Query:**
```sql
WITH one_hop AS (
  SELECT followee_id AS influencer, follower_id AS follower
  FROM follows
),
two_hop AS (
  SELECT
    o1.influencer,
    o2.follower_id AS second_hop_user
  FROM one_hop o1
  JOIN follows o2 ON o1.follower = o2.followee_id
)
SELECT
  influencer,
  COUNT(DISTINCT follower) AS direct_followers,
  COUNT(DISTINCT
    CASE WHEN second_hop_user != influencer
         AND second_hop_user NOT IN (
           SELECT follower_id FROM follows WHERE followee_id = influencer
         )
    THEN second_hop_user END
  ) AS unique_2hop_reach
FROM one_hop
LEFT JOIN two_hop USING (influencer)
GROUP BY influencer
ORDER BY unique_2hop_reach DESC;
```

**Explanation:** Join the follow graph twice, exclude self-loops and direct followers. **Interview trick:** The anti-join for direct followers prevents double counting. For 3+ hops, use a recursive CTE instead of manual joins.

---

## Q54: Leaderboard With Percentile and Tie-Breaking

**Tables:** `player_scores(player_id INT, total_score INT)`. Create a leaderboard with DENSE_RANK, PERCENT_RANK, and a stable tiebreaker (fewer games played).

**Query:**
```sql
SELECT
  player_id,
  total_score,
  games_played,
  DENSE_RANK() OVER (
    ORDER BY total_score DESC, games_played ASC
  ) AS position,
  ROUND(PERCENT_RANK() OVER (
    ORDER BY total_score DESC
  ) * 100, 1) AS percentile_rank
FROM player_scores
ORDER BY position;
```

**Explanation:** Composite ORDER BY (score DESC, games ASC) breaks ties deterministically. **Interview trick:** PERCENT_RANK is computed on score alone; the tiebreaker only affects position. Clarify whether ties should share or all have distinct positions.

---

## Q55: Weekly Return Rate — User Engagement Prediction

**Tables:** `activity(user_id INT, activity_date DATE)`. For each user, compute their weekly return rate (fraction of active weeks in which they had activity the following week).

**Query:**
```sql
WITH weekly_active AS (
  SELECT DISTINCT
    user_id,
    DATE_TRUNC('week', activity_date) AS active_week
  FROM activity
),
next_week AS (
  SELECT
    user_id,
    active_week,
    LEAD(active_week) OVER (PARTITION BY user_id ORDER BY active_week) AS next_active_week
  FROM weekly_active
),
weeks AS (
  SELECT
    user_id,
    active_week,
    MIN(active_week) OVER () AS min_week,
    MAX(active_week) OVER () AS max_week
  FROM weekly_active
)
SELECT
  w.user_id,
  COUNT(DISTINCT w.active_week) AS active_weeks,
  ROUND(
    100.0 * COUNT(CASE WHEN n.next_active_week = w.active_week + INTERVAL '1 week' THEN 1 END)
    / COUNT(DISTINCT w.active_week),
    2
  ) AS week_over_week_return_pct
FROM weeks w
LEFT JOIN next_week n ON w.user_id = n.user_id AND w.active_week = n.active_week
WHERE w.active_week >= (SELECT MIN(active_week) FROM weekly_active) + INTERVAL '1 week'
GROUP BY w.user_id
ORDER BY week_over_week_return_pct DESC NULLS LAST;
```

**Explanation:** Mark each user's active weeks, use LEAD to find their next engagement, then compute return rate. **Interview trick:** There's a nuance — whether inactive weeks count in the denominator. The WHERE clause drops the final week since we can't observe its return.

---

## Q56: Concurrent Session Overlap Detection

**Tables:** `sessions(session_id INT, user_id INT, start_time TIMESTAMP, end_time TIMESTAMP)`. Find all pairs of sessions that overlap in time (potential multi-tab activity).

**Query:**
```sql
SELECT
  a.session_id AS session_a,
  b.session_id AS session_b,
  a.user_id,
  a.start_time AS a_start,
  a.end_time AS a_end,
  b.start_time AS b_start,
  b.end_time AS b_end
FROM sessions a
JOIN sessions b
  ON a.user_id = b.user_id
  AND a.session_id < b.session_id
  AND a.start_time < b.end_time
  AND b.start_time < a.end_time
ORDER BY a.session_id, b.session_id;
```

**Explanation:** Two intervals overlap if `A.start < B.end AND B.start < A.end`. The ID comparison deduplicates pairs. **Interview trick:** This is the interval-overlap join — a classic for session, hotel booking, and calendar systems alike.

---

## Q57: Funnel With Per-Step Time Limit

**Tables:** `events(user_id INT, event_type VARCHAR, event_time TIMESTAMP)`. Compute funnel conversion where each step must occur within 15 minutes of the previous step.

**Query:**
```sql
WITH step_events AS (
  SELECT
    user_id,
    event_type,
    event_time,
    ROW_NUMBER() OVER (
      PARTITION BY user_id, event_type ORDER BY event_time
    ) AS step_rn
  FROM events
  WHERE event_type IN ('view', 'cart', 'checkout', 'purchase')
),
view_only AS (
  SELECT user_id, event_time AS view_time, step_rn
  FROM step_events WHERE event_type = 'view'
),
cart_only AS (
  SELECT user_id, event_time AS cart_time, step_rn
  FROM step_events WHERE event_type = 'cart'
),
checkout_only AS (
  SELECT user_id, event_time AS checkout_time, step_rn
  FROM step_events WHERE event_type = 'checkout'
),
purchase_only AS (
  SELECT user_id, event_time AS purchase_time, step_rn
  FROM step_events WHERE event_type = 'purchase'
),
full_funnel AS (
  SELECT
    v.user_id,
    v.view_time,
    c.cart_time,
    k.checkout_time,
    p.purchase_time
  FROM view_only v
  JOIN cart_only c
    ON v.user_id = c.user_id
    AND c.cart_time BETWEEN v.view_time AND v.view_time + INTERVAL '15 minutes'
  JOIN checkout_only k
    ON v.user_id = k.user_id
    AND k.checkout_time BETWEEN c.cart_time AND c.cart_time + INTERVAL '15 minutes'
  JOIN purchase_only p
    ON v.user_id = p.user_id
    AND p.purchase_time BETWEEN k.checkout_time AND k.checkout_time + INTERVAL '15 minutes'
)
SELECT
  COUNT(*) AS full_funnel_users,
  ROUND(AVG(EXTRACT(EPOCH FROM purchase_time - view_time) / 60.0), 2) AS avg_total_minutes
FROM full_funnel;
```

**Explanation:** Each join enforces the 15-minute constraint between consecutive steps, chaining the time windows. **Interview trick:** This is a "path with timing constraints" problem — notice how each JOIN's range references the previous step's timestamp, not the original.

---

## Q58: Retention With Rolling Window (Approx)

**Tables:** `user_events(user_id INT, event_date DATE)`. For each active week cohort, compute the fraction of users still active in any later week (rolling retention), capped at 8 weeks forward.

**Query:**
```sql
WITH weekly AS (
  SELECT DISTINCT user_id, DATE_TRUNC('week', event_date) AS wk
  FROM user_events
),
cohort AS (
  SELECT
    user_id,
    MIN(wk) AS cohort_week
  FROM weekly
  GROUP BY user_id
),
joined AS (
  SELECT
    c.cohort_week,
    c.user_id,
    w.wk,
    (w.wk - c.cohort_week) / 7 AS week_offset
  FROM cohort c
  JOIN weekly w ON c.user_id = w.user_id
    AND w.wk BETWEEN c.cohort_week AND c.cohort_week + INTERVAL '8 weeks'
)
SELECT
  cohort_week,
  ROUND(100.0 * COUNT(DISTINCT user_id) FILTER (WHERE week_offset = 0), 0) AS wk0,
  ROUND(100.0 * COUNT(DISTINCT user_id) FILTER (WHERE week_offset = 1) / NULLIF(COUNT(DISTINCT user_id) FILTER (WHERE week_offset = 0), 0), 2) AS wk1_pct,
  ROUND(100.0 * COUNT(DISTINCT user_id) FILTER (WHERE week_offset = 4) / NULLIF(COUNT(DISTINCT user_id) FILTER (WHERE week_offset = 0), 0), 2) AS wk4_pct,
  ROUND(100.0 * COUNT(DISTINCT user_id) FILTER (WHERE week_offset = 8) / NULLIF(COUNT(DISTINCT user_id) FILTER (WHERE week_offset = 0), 0), 2) AS wk8_pct
FROM joined
GROUP BY cohort_week
ORDER BY cohort_week;
```

**Explanation:** Cohort = first active week. Week offset = (event week - cohort week)/7. Retention % = active in week N / cohort size. **Interview trick:** Rolling retention is "ever active by week N," different from classic "active exactly in week N" — the distinction often matters.

---

## Q59: LTV Prediction — Revenue Per Active Month

**Tables:** `orders(order_id INT, user_id INT, order_date DATE, revenue DECIMAL)`, `events(user_id INT, event_date DATE)`. Compute lifetime value (LTV) per user and their average revenue per active month (ARPU).

**Query:**
```sql
WITH user_metrics AS (
  SELECT
    u.user_id,
    SUM(o.revenue) AS total_revenue,
    COUNT(o.order_id) AS order_count,
    DATE_PART('year', AGE(MAX(o.order_date), MIN(o.order_date))) * 12
    + DATE_PART('month', AGE(MAX(o.order_date), MIN(o.order_date))) AS months_span,
    COUNT(DISTINCT DATE_TRUNC('month', o.order_date)) AS active_months
  FROM (SELECT DISTINCT user_id FROM orders) u
  LEFT JOIN orders o ON u.user_id = o.user_id
  GROUP BY u.user_id
)
SELECT
  user_id,
  ROUND(total_revenue, 2) AS ltv,
  order_count,
  active_months,
  ROUND(total_revenue / NULLIF(active_months, 0), 2) AS monthly_arpu,
  DENSE_RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank
FROM user_metrics
ORDER BY revenue_rank;
```

**Explanation:** LTV = total revenue. ARPU = LTV / active months. **Interview trick:** Use `active_months` (distinct months with orders) not total months spanned, so a user with only one month of orders has ARPU = LTV.

---

## Q60: Product Co-purchase Jaccard Similarity

**Tables:** `transactions_cart(txn_id INT, product_id INT)`. Compute Jaccard similarity between each product pair: J(A,B) = |A∩B| / |A∪B| (baskets containing both / baskets containing either).

**Query:**
```sql
WITH baskets AS (
  SELECT DISTINCT txn_id, product_id FROM transactions_cart
),
a AS (
  SELECT txn_id, product_id AS p FROM baskets
),
b AS (
  SELECT txn_id, product_id AS q FROM baskets
),
pair_counts AS (
  SELECT
    a.p,
    b.q,
    COUNT(*) AS intersection_count
  FROM a
  JOIN b
    ON a.txn_id = b.txn_id
    AND a.p < b.q
  GROUP BY a.p, b.q
),
single_counts AS (
  SELECT product_id, COUNT(*) AS basket_count
  FROM baskets
  GROUP BY product_id
)
SELECT
  pc.p AS product_a,
  pc.q AS product_b,
  pc.intersection_count,
  sc1.basket_count AS baskets_with_a,
  sc2.basket_count AS baskets_with_b,
  ROUND(
    pc.intersection_count::DECIMAL
    / NULLIF(sc1.basket_count + sc2.basket_count - pc.intersection_count, 0),
    4
  ) AS jaccard_similarity
FROM pair_counts pc
JOIN single_counts sc1 ON pc.p = sc1.product_id
JOIN single_counts sc2 ON pc.q = sc2.product_id
ORDER BY jaccard_similarity DESC;
```

**Explanation:** |A∩B| = baskets with both, |A∪B| = baskets(A) + baskets(B) - baskets(both). **Interview trick:** Jaccard is insensitive to product popularity scale, unlike lift. The `<` join keeps each pair once.

---

## Q61: Stock — 52-Week High/Low and Days Since

**Tables:** `stock_prices(ticker VARCHAR, trade_date DATE, close_price DECIMAL)`. For AAPL, compute the rolling 52-week high and low, and how many trading days since each was hit.

**Query:**
```sql
WITH daily AS (
  SELECT
    trade_date,
    close_price,
    MAX(close_price) OVER (
      ORDER BY trade_date
      RANGE BETWEEN INTERVAL '364 days' PRECEDING AND CURRENT ROW
    ) AS high_52w,
    MIN(close_price) OVER (
      ORDER BY trade_date
      RANGE BETWEEN INTERVAL '364 days' PRECEDING AND CURRENT ROW
    ) AS low_52w
  FROM stock_prices
  WHERE ticker = 'AAPL'
),
high_dates AS (
  SELECT trade_date, close_price
  FROM daily
  WHERE close_price = high_52w
),
low_dates AS (
  SELECT trade_date, close_price
  FROM daily
  WHERE close_price = low_52w
)
SELECT
  d.trade_date,
  ROUND(d.close_price, 2) AS close_price,
  ROUND(d.high_52w, 2) AS high_52w,
  ROUND(d.low_52w, 2) AS low_52w,
  EXTRACT(DAY FROM d.trade_date - MAX(hd.trade_date)) AS days_since_high,
  EXTRACT(DAY FROM d.trade_date - MAX(ld.trade_date)) AS days_since_low
FROM daily d
LEFT JOIN high_dates hd ON hd.trade_date <= d.trade_date
LEFT JOIN low_dates ld  ON ld.trade_date  <= d.trade_date
GROUP BY d.trade_date, d.close_price, d.high_52w, d.low_52w
ORDER BY d.trade_date;
```

**Explanation:** Rolling window `RANGE BETWEEN 364 days PRECEDING` gives the 52-week band. Days since hit = latest high-date ≤ current date. **Interview trick:** The self-correlated LEFT JOIN with MAX date is the "most recent occurrence" pattern.

---

## Q62: Stock — Moving Average Cross-Over Signals

**Tables:** `stock_prices(ticker VARCHAR, trade_date DATE, close_price DECIMAL)`. Generate buy/sell signals using the golden cross (50-day MA crosses above 200-day MA = buy signal).

**Query:**
```sql
WITH ma AS (
  SELECT
    trade_date,
    close_price,
    AVG(close_price) OVER (
      ORDER BY trade_date ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
    ) AS ma_50,
    AVG(close_price) OVER (
      ORDER BY trade_date ROWS BETWEEN 199 PRECEDING AND CURRENT ROW
    ) AS ma_200
  FROM stock_prices
  WHERE ticker = 'AAPL'
),
prev AS (
  SELECT
    *,
    LAG(ma_50 > ma_200) OVER (ORDER BY trade_date) AS was_above
  FROM ma
)
SELECT
  trade_date,
  ROUND(close_price, 2) AS close_price,
  ROUND(ma_50, 2) AS ma_50,
  ROUND(ma_200, 2) AS ma_200,
  CASE
    WHEN (ma_50 > ma_200) AND NOT was_above THEN 'BUY (golden cross)'
    WHEN (ma_50 < ma_200) AND was_above THEN 'SELL (death cross)'
    ELSE 'hold'
  END AS signal
FROM prev
WHERE trade_date >= (SELECT MIN(trade_date) + INTERVAL '199 days' FROM stock_prices WHERE ticker = 'AAPL')
ORDER BY trade_date;
```

**Explanation:** Two rolling averages; a cross-over is detected when the sign of (ma_50 - ma_200) flips versus the previous day. **Interview trick:** The LAG boolean `was_above` comparison is how cross-overs (not just positions) are detected.

---

## Q63: Weighted Median — Price-Volume Median

**Tables:** `order_book(price DECIMAL, volume INT)`. Compute the volume-weighted median price (the price at which 50% of cumulative volume traded above and below).

**Query:**
```sql
WITH sorted AS (
  SELECT
    price,
    volume,
    SUM(volume) OVER (ORDER BY price) AS cum_volume,
    SUM(volume) OVER () AS total_volume
  FROM order_book
)
SELECT
  price AS weighted_median_price
FROM sorted
WHERE cum_volume >= total_volume / 2.0
ORDER BY cum_volume
LIMIT 1;
```

**Explanation:** Sort by price, compute cumulative volume; the weighted median is the first price where cumulative volume reaches half the total. **Interview trick:** This generalizes to weighted percentiles: replace 0.5 with any fraction, also for `WHERE` on `(cum_volume - volume) / total <= x`.

---

## Q64: Multiple Orders Per Day — First and Last Order Analysis

**Tables:** `orders(order_id INT, user_id INT, order_time TIMESTAMP, amount DECIMAL)`. For each user and day, compute the number of orders and the amount of their first vs last order.

**Query:**
```sql
WITH tagged AS (
  SELECT
    order_id,
    user_id,
    order_time,
    amount,
    ROW_NUMBER() OVER (
      PARTITION BY user_id, order_time::DATE ORDER BY order_time
    ) AS order_seq
  FROM orders
)
SELECT
  user_id,
  order_time::DATE AS day,
  COUNT(*) AS daily_orders,
  SUM(amount) AS daily_revenue,
  MAX(CASE WHEN order_seq = 1 THEN amount END) AS first_order_amount,
  MAX(CASE WHEN order_seq = (SELECT MAX(order_seq) FROM tagged t2 WHERE t2.user_id = tagged.user_id AND t2.order_time::DATE = tagged.order_time::DATE) THEN amount END) AS last_order_amount
FROM tagged
GROUP BY user_id, order_time::DATE
ORDER BY user_id, day;
```

**Alt1:** Cleaner with a second window:
```sql
WITH tagged AS (
  SELECT
    order_id,
    user_id,
    order_time,
    amount,
    ROW_NUMBER() OVER (
      PARTITION BY user_id, order_time::DATE ORDER BY order_time
    ) AS first_seq,
    ROW_NUMBER() OVER (
      PARTITION BY user_id, order_time::DATE ORDER BY order_time DESC
    ) AS last_seq
  FROM orders
)
SELECT
  user_id,
  order_time::DATE AS day,
  COUNT(*) AS daily_orders,
  SUM(amount) AS daily_revenue,
  MAX(CASE WHEN first_seq = 1 THEN amount END) AS first_order_amount,
  MAX(CASE WHEN last_seq = 1 THEN amount END) AS last_order_amount
FROM tagged
GROUP BY user_id, order_time::DATE
ORDER BY user_id, day;
```

**Explanation:** Rank orders within each user-day both forward and backward, then pivot with MAX(CASE). **Interview trick:** The double ROW_NUMBER (asc + desc) is far cleaner than a correlated subquery — always prefer it.

---

## Q65: Time-Weighted Average (Money-Weighted Return)

**Tables:** `portfolio_balance(account_id INT, balance_date DATE, balance DECIMAL)`. Compute the time-weighted average balance per month (weighting by days held, not simple average of daily snapshots).

**Query:**
```sql
WITH snapshots AS (
  SELECT
    account_id,
    balance_date,
    balance,
    LEAD(balance_date) OVER (
      PARTITION BY account_id ORDER BY balance_date
    ) AS next_date
  FROM portfolio_balance
),
weighted AS (
  SELECT
    account_id,
    balance_date,
    balance,
    next_date,
    COALESCE(next_date, balance_date + INTERVAL '1 day') - balance_date AS days_held
  FROM snapshots
)
SELECT
  account_id,
  DATE_TRUNC('month', balance_date) AS month,
  ROUND(SUM(balance * days_held) / SUM(days_held), 2) AS time_weighted_avg_balance
FROM weighted
GROUP BY account_id, DATE_TRUNC('month', balance_date)
ORDER BY account_id, month;
```

**Explanation:** Each snapshot's balance counts for `days_held` days; time-weighted avg = Σ(balance × days) / Σ(days). **Interview trick:** The COALESCE for the last snapshot uses +1 day so it still contributes. This is the difference between -simple- and -time-weighted- averages.

---

## Q66: Z-Score Anomaly Detection — Daily Revenue

**Tables:** `daily_revenue(day DATE, revenue DECIMAL)`. Flag days where revenue deviates more than 2 standard deviations from the trailing 30-day mean.

**Query:**
```sql
WITH rolling_stats AS (
  SELECT
    day,
    revenue,
    AVG(revenue) OVER (
      ORDER BY day ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING
    ) AS prev_30_avg,
    STDDEV(revenue) OVER (
      ORDER BY day ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING
    ) AS prev_30_std
  FROM daily_revenue
)
SELECT
  day,
  ROUND(revenue, 2) AS revenue,
  ROUND(prev_30_avg, 2) AS trailing_avg,
  ROUND(prev_30_std, 3) AS trailing_std,
  ROUND((revenue - prev_30_avg) / NULLIF(prev_30_std, 0), 2) AS z_score,
  CASE
    WHEN ABS((revenue - prev_30_avg) / NULLIF(prev_30_std, 0)) > 2 THEN 'anomaly'
    ELSE 'normal'
  END AS flag
FROM rolling_stats
WHERE day >= (SELECT MIN(day) + INTERVAL '30 days' FROM daily_revenue)
ORDER BY day;
```

**Explanation:** Rolling mean/std computed over the PRIOR 30 rows (BETWEEN 30 PRECEDING AND 1 PRECEDING) so the current day isn't included. **Interview trick:** The window deliberately excludes the current row — a naive implementation includes it and under-reports anomalies.

---

## Q67: Hotel Booking Overlap — Double-Booked Rooms

**Tables:** `bookings(booking_id INT, room_id INT, check_in DATE, check_out DATE)`. Find all overlapping bookings per room.

**Query:**
```sql
SELECT
  a.booking_id AS booking_a,
  b.booking_id AS booking_b,
  a.room_id,
  a.check_in AS a_check_in,
  a.check_out AS a_check_out,
  b.check_in AS b_check_in,
  b.check_out AS b_check_out
FROM bookings a
JOIN bookings b
  ON a.room_id = b.room_id
  AND a.booking_id < b.booking_id
  AND a.check_in < b.check_out
  AND b.check_in < a.check_out
ORDER BY a.room_id, a.check_in;
```

**Explanation:** Same interval-overlap test as Q56 but on date ranges. **Interview trick:** Overlap requires `A.start < B.end AND B.start < A.end`. A stays that end exactly when another starts are adjacent, not overlapping.

---

## Q68: Candidate Hiring Funnel With Stage Durations

**Tables:** `candidate_moves(candidate_id INT, stage VARCHAR, moved_at TIMESTAMP)`. Stages: 'applied', 'phone_screen', 'onsite', 'offer'. Compute avg time in each stage.

**Query:**
```sql
WITH stages AS (
  SELECT
    candidate_id,
    stage,
    moved_at,
    LEAD(moved_at) OVER (
      PARTITION BY candidate_id ORDER BY moved_at
    ) AS next_stage_time
  FROM candidate_moves
)
SELECT
  stage,
  COUNT(*) AS candidates_reached,
  ROUND(
    AVG(EXTRACT(EPOCH FROM next_stage_time - moved_at) / 86400.0),
    2
  ) AS avg_days_in_stage,
  ROUND(
    PERCENTILE_CONT(0.5) WITHIN GROUP (
      ORDER BY EXTRACT(EPOCH FROM next_stage_time - moved_at) / 86400.0
    ),
    2
  ) AS median_days_in_stage
FROM stages
WHERE next_stage_time IS NOT NULL
GROUP BY stage
ORDER BY MIN(moved_at);
```

**Explanation:** LEAD gives the time of the next stage move; the diff is time-in-stage. **Interview trick:** Avg vs median matters here — a few stuck candidates blow up the average, so report both.

---

## Q69: Movie Co-Rating — Recommendations Without Purchases

**Tables:** `ratings(user_id INT, movie_id INT, rating INT)`. Find movie pairs rated 4+ by the same users.

**Query:**
```sql
WITH good_ratings AS (
  SELECT user_id, movie_id
  FROM ratings
  WHERE rating >= 4
)
SELECT
  a.movie_id AS movie_a,
  b.movie_id AS movie_b,
  COUNT(DISTINCT a.user_id) AS co_ratings,
  ROUND(AVG(a.rating * 1.0), 2) AS avg_a_rating,
  ROUND(AVG(b.rating * 1.0), 2) AS avg_b_rating
FROM good_ratings a
JOIN ratings b
  ON a.user_id = b.user_id
  AND a.movie_id != b.movie_id
WHERE b.rating >= 4
GROUP BY a.movie_id, b.movie_id
HAVING COUNT(DISTINCT a.user_id) >= 5
ORDER BY co_ratings DESC;
```

**Explanation:** Restrict to users who rate both movies highly, count overlaps. **Interview trick:** For recommendation quality, add popularity normalization — co-ratings between two globally popular movies are less informative.

---

## Q70: Pivot — User×Event-Type Matrix

**Tables:** `user_events(user_id INT, event_type VARCHAR, event_time TIMESTAMP)`. Build a pivot table showing counts of each event type per user.

**Query:**
```sql
SELECT
  user_id,
  COUNT(*) FILTER (WHERE event_type = 'view')   AS view_count,
  COUNT(*) FILTER (WHERE event_type = 'click')  AS click_count,
  COUNT(*) FILTER (WHERE event_type = 'cart')   AS cart_count,
  COUNT(*) FILTER (WHERE event_type = 'buy')    AS buy_count,
  COUNT(*) AS total_events
FROM user_events
GROUP BY user_id
ORDER BY total_events DESC;
```

**Alt1:** Standard SQL bridge (no FILTER):
```sql
SELECT
  user_id,
  SUM(CASE WHEN event_type = 'view'  THEN 1 ELSE 0 END) AS view_count,
  SUM(CASE WHEN event_type = 'click' THEN 1 ELSE 0 END) AS click_count,
  SUM(CASE WHEN event_type = 'cart'  THEN 1 ELSE 0 END) AS cart_count,
  SUM(CASE WHEN event_type = 'buy'   THEN 1 ELSE 0 END) AS buy_count
FROM user_events
GROUP BY user_id;
```

**Explanation:** One row per user with a column per event type. **Interview trick:** `FILTER` is cleaner but PostgreSQL-only; use SUM + CASE for portability. This is the "wide" version of the long/wide normalization question.

---

## Q71: Weekly Active vs Daily Active (Stickiness Ratio)

**Tables:** `events(user_id INT, event_date DATE)`. Compute the stickiness ratio (DAU/WAU) for each week.

**Query:**
```sql
WITH week_start AS (
  SELECT
    DATE_TRUNC('week', event_date) AS wk,
    COUNT(DISTINCT user_id) AS wau
  FROM events
  GROUP BY DATE_TRUNC('week', event_date)
),
daily_counts AS (
  SELECT
    event_date,
    DATE_TRUNC('week', event_date) AS wk,
    COUNT(DISTINCT user_id) AS dau
  FROM events
  GROUP BY event_date, DATE_TRUNC('week', event_date)
)
SELECT
  w.wk,
  w.wau,
  ROUND(AVG(d.dau), 2) AS avg_dau,
  ROUND(100.0 * AVG(d.dau) / w.wau, 2) AS stickiness_pct
FROM week_start w
JOIN daily_counts d ON w.wk = d.wk
GROUP BY w.wk, w.wau
ORDER BY w.wk;
```

**Explanation:** Stickiness = average DAU / WAU. **Interview trick:** Stickiness is a product-quality signal: >20% is strong for consumer apps, <10% suggests once-a-week usage. Attribution requires joins on the week key.

---

## Q72: Cohort Quartile Comparison — Engagement by Signup Quartile

**Tables:** `signups(user_id INT, signup_date DATE)`, `activity(user_id INT, activity_date DATE)`. Split users into quartiles by signup date and compare their lifetime activity.

**Query:**
```sql
WITH cohorts AS (
  SELECT
    user_id,
    signup_date,
    NTILE(4) OVER (ORDER BY signup_date) AS quartile
  FROM signups
),
activity_counts AS (
  SELECT
    c.quartile,
    c.user_id,
    COUNT(DISTINCT a.activity_date) AS active_days,
    COUNT(a.activity_date) AS total_actions
  FROM cohorts c
  LEFT JOIN activity a ON c.user_id = a.user_id
  GROUP BY c.quartile, c.user_id
)
SELECT
  quartile,
  COUNT(*) AS users,
  ROUND(AVG(active_days), 1) AS avg_active_days,
  ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY active_days), 1) AS median_active_days,
  ROUND(AVG(total_actions), 1) AS avg_actions
FROM activity_counts
GROUP BY quartile
ORDER BY quartile;
```

**Explanation:** NTILE(4) buckles users by signup date; compare engagement statistics across quarters. **Interview trick:** Median hides outlier power users; the avg-vs-median gap reveals engagement skew — mention it to score points.

---

## Q73: Cumulative Retention Curve — Weekly Cohorts, Max 8 Weeks

**Tables:** `user_events(user_id INT, event_date DATE)`. For each weekly cohort, compute the percentage of users who were active at least once by week N (cumulative retention, N = 1..8), handling NULL.

**Query:**
```sql
WITH cohorts AS (
  SELECT user_id, MIN(DATE_TRUNC('week', event_date)) AS cohort_week
  FROM user_events
  GROUP BY user_id
),
weeks AS (
  SELECT
    c.cohort_week,
    w.week_num,
    COUNT(DISTINCT ue.user_id) AS active_users
  FROM cohorts c
  JOIN user_events ue
    ON c.user_id = ue.user_id
  JOIN (
    SELECT GENERATE_SERIES(1, 8) AS week_num
  ) w
    ON DATE_TRUNC('week', ue.event_date) BETWEEN
      c.cohort_week AND c.cohort_week + (w.week_num - 1) * INTERVAL '1 week'
  GROUP BY c.cohort_week, w.week_num
)
SELECT
  cohort_week,
  week_num,
  active_users,
  ROUND(
    100.0 * active_users / NULLIF(MAX(active_users) OVER (PARTITION BY cohort_week), 0),
    2
  ) AS cumulative_retention_pct
FROM weeks
ORDER BY cohort_week, week_num;
```

**Explanation:** For each cohort, count distinct users seen within the first N weeks; divide by cohort size (taken as week 1 count). **Interview trick:** The `MAX(...) OVER (PARTITION BY cohort_week)` is a neat way to reference cohort size without a second join.

---

## Q74: Top Session Per User Per Day

**Tables:** `events(user_id INT, session_id INT, event_time TIMESTAMP)`. Compute each user's daily session count and find the session with the most events.

**Query:**
```sql
WITH session_events AS (
  SELECT
    user_id,
    session_id,
    event_time::DATE AS day,
    COUNT(*) OVER (
      PARTITION BY user_id, session_id
    ) AS events_in_session
  FROM events
),
ranked AS (
  SELECT
    user_id,
    day,
    session_id,
    events_in_session,
    ROW_NUMBER() OVER (
      PARTITION BY user_id, day ORDER BY events_in_session DESC, session_id
    ) AS rn
  FROM session_events
)
SELECT
  user_id,
  day,
  COUNT(DISTINCT session_id) AS total_sessions,
  MAX(CASE WHEN rn = 1 THEN session_id END) AS top_session_id,
  MAX(CASE WHEN rn = 1 THEN events_in_session END) AS top_session_events
FROM ranked
GROUP BY user_id, day
ORDER BY user_id, day;
```

**Explanation:** Count events per session via window, then pick the top session per user-day. **Interview trick:** The `row_number` tiebreaker (`session_id`) makes output deterministic — required in production reporting.

---

## Q75: Drop-Off Analysis — Users Who Viewed Product Page But Never Purchased

**Tables:** `events(user_id INT, event_type VARCHAR)`, `purchases(user_id INT, order_date DATE)`. For each product viewed (event 'view_product'), compute how many users viewed it, purchased it, and never came back.

**Query:**
```sql
SELECT
  v.product_id,
  COUNT(DISTINCT v.user_id) AS who_viewed,
  COUNT(DISTINCT p.user_id) AS who_purchased,
  COUNT(DISTINCT v.user_id) - COUNT(DISTINCT p.user_id) AS viewed_not_bought,
  ROUND(
    100.0 * (COUNT(DISTINCT v.user_id) - COUNT(DISTINCT p.user_id))
    / NULLIF(COUNT(DISTINCT v.user_id), 0), 2
  ) AS drop_off_pct
FROM (
  SELECT DISTINCT user_id, product_id
  FROM product_views v
) v
LEFT JOIN product_purchases p
  ON v.product_id = p.product_id AND v.user_id = p.user_id
GROUP BY v.product_id;
```

**Alt1:** Anti-join version (users in the LEFT JOIN and not in purchases):
```sql
SELECT
  v.product_id,
  COUNT(DISTINCT v.user_id) AS who_viewed,
  COUNT(DISTINCT CASE WHEN p.user_id IS NULL THEN v.user_id END) AS viewed_not_bought
FROM (SELECT DISTINCT user_id, product_id FROM product_views) v
LEFT JOIN product_purchases p
  ON v.product_id = p.product_id AND v.user_id = p.user_id
GROUP BY v.product_id;
```

**Explanation:** LEFT JOIN views to purchases; the difference in distinct user counts is the lost opportunity. **Interview trick:** This is the core of product analytics — funnel leakage between interest and conversion. Ask which product has the highest drop-off to spot conversion-blocking UX.

---

## Q76: First-Touch vs Last-Touch Attribution

**Tables:** `touchpoints(user_id INT, channel VARCHAR, touch_time TIMESTAMP)`, `conversions(user_id INT, converted_at TIMESTAMP)`. Assign each conversion to the channel of the first and last touchpoint.

**Query:**
```sql
WITH channel_ranks AS (
  SELECT
    user_id,
    channel,
    touch_time,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY touch_time) AS first_rank,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY touch_time DESC) AS last_rank
  FROM touchpoints
)
SELECT
  c.user_id,
  c.converted_at,
  MAX(CASE WHEN t1.first_rank = 1 THEN t1.channel END) AS first_touch_channel,
  MAX(CASE WHEN t2.last_rank = 1 THEN t2.channel END) AS last_touch_channel
FROM conversions c
LEFT JOIN channel_ranks t1
  ON c.user_id = t1.user_id AND t1.first_rank = 1 AND t1.touch_time <= c.converted_at
LEFT JOIN channel_ranks t2
  ON c.user_id = t2.user_id AND t2.last_rank = 1 AND t2.touch_time <= c.converted_at
GROUP BY c.user_id, c.converted_at;
```

**Explanation:** Rank touchpoints forward (first) and backward (last), join both to conversions. **Interview trick:** Credit-modeling questions test your ability to join derived identifiers. The `touch_time <= converted_at` guard ensures touchpoints after conversion don't count.

---

## Q77: Reactivation Rate — Users Returning After Churn

**Tables:** `user_activity(user_id INT, activity_date DATE)`. A user "churned" after 30 days of inactivity; "reactivated" when they return. Count reactivations per month.

**Query:**
```sql
WITH ranked_activity AS (
  SELECT
    user_id,
    activity_date,
    LAG(activity_date) OVER (PARTITION BY user_id ORDER BY activity_date) AS prev_active_date
  FROM (
    SELECT DISTINCT user_id, activity_date FROM user_activity
  ) d
),
reactivations AS (
  SELECT
    user_id,
    activity_date,
    prev_active_date,
    DATE_PART('day', activity_date - prev_active_date) AS days_gap
  FROM ranked_activity
  WHERE prev_active_date IS NOT NULL
    AND activity_date - prev_active_date > INTERVAL '30 days'
)
SELECT
  DATE_TRUNC('month', activity_date) AS reactivation_month,
  COUNT(*) AS reactivated_users
FROM reactivations
GROUP BY DATE_TRUNC('month', activity_date)
ORDER BY reactivation_month;
```

**Explanation:** LAG on distinct activity dates; a gap over 30 days marks a reactivation. **Interview trick:** Deduplicate dates first, otherwise repeated same-day activity creates 0-day "gaps." The DAYS_GAP value doubles as a churn intensity metric.

---

## Q78: Rolling 7-Day Revenue With Prior-Week Comparison

**Tables:** `order_transactions(transaction_id INT, order_date DATE, revenue DECIMAL)`. For each day, compute the trailing 7-day revenue and the previous 7-day revenue, plus % change.

**Query:**
```sql
WITH daily AS (
  SELECT order_date, SUM(revenue) AS revenue
  FROM order_transactions
  GROUP BY order_date
),
rolling AS (
  SELECT
    order_date,
    revenue,
    SUM(revenue) OVER (
      ORDER BY order_date
      ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS revenue_last_7d,
    LAG(SUM(revenue) OVER (
      ORDER BY order_date
      ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ), 7) OVER (ORDER BY order_date) AS revenue_prev_7d
  FROM daily
)
SELECT
  order_date,
  ROUND(revenue_last_7d, 2) AS revenue_last_7d,
  ROUND(revenue_prev_7d, 2) AS revenue_prev_7d,
  ROUND(
    (revenue_last_7d - revenue_prev_7d) / NULLIF(revenue_prev_7d, 0) * 100, 2
  ) AS wow_change_pct
FROM rolling
WHERE order_date >= (SELECT MIN(order_date) + INTERVAL '13 days' FROM order_transactions)
ORDER BY order_date;
```

**Explanation:** Rolling 7-day sum, then shift by 7 days to compare against the previous window. **Interview trick:** The WHERE ensures both windows are complete so WoW deltas aren't skewed by warm-up days.

---

## Q79: Timezone-Aware Event Day Bucketing

**Tables:** `events(event_id INT, user_id INT, event_time TIMESTAMP)`, `users(user_id INT, timezone VARCHAR)`. Aggregate events by the user's local calendar day, then a UTC day, for comparison.

**Query:**
```sql
SELECT
  u.timezone,
  event_time::DATE AS utc_day,
  (event_time AT TIME ZONE COALESCE(u.timezone, 'UTC'))::DATE AS local_day,
  COUNT(*) AS events
FROM events e
JOIN users u ON e.user_id = u.user_id
WHERE u.timezone IS NOT NULL
GROUP BY u.timezone, event_time::DATE, (event_time AT TIME ZONE COALESCE(u.timezone, 'UTC'))::DATE
ORDER BY u.timezone, local_day;
```

**Explanation:** `AT TIME ZONE` converts timestamps between zones; casting the result to DATE buckeby local day. **Interview trick:** ALWAYS confirm the expected timezone conventions up front — the difference between UTC-day and local-day reporting can change conclusions by hours of peak activity.

---

## Q80: Business Days With Oracle CONNECT BY and LISTAGG

**Tables:** `work_days(project_id INT, start_date DATE, end_date DATE)`. Oracle: expand a date range into business days and concatenate into a string.

**Query:**
```sql
-- Oracle
SELECT
  project_id,
  start_date,
  end_date,
  LISTAGG(TO_CHAR(dt, 'DD-MON'), ',') WITHIN GROUP (ORDER BY dt) AS business_days_list,
  COUNT(*) AS business_days
FROM (
  SELECT
    project_id,
    start_date,
    end_date,
    start_date + LEVEL - 1 AS dt
  FROM work_days
  CONNECT BY
    LEVEL <= end_date - start_date + 1
    AND PRIOR project_id = project_id
    AND PRIOR SYS_GUID() IS NOT NULL
)
WHERE TO_CHAR(dt, 'D') NOT IN ('7', '1')
GROUP BY project_id, start_date, end_date;
```

**Explanation:** `CONNECT BY LEVEL` with the range length generates each date. `LISTAGG` rolls the business-day dates into a CSV. **Interview trick:** The `PRIOR SYS_GUID() IS NOT NULL` guard is the standard trick to stop recursive row multiplication in CONNECT BY. 'D'=7 is Saturday, 1 is Sunday in an NLS-dependent calendar.

---

## Q81: Unpivot — Wide Table to Long Rows

**Tables:** `revenue_wide(year INT, q1 DECIMAL, q2 DECIMAL, q3 DECIMAL, q4 DECIMAL)`. Convert quarterly revenue columns into rows (long format) and rank quarters per year.

**Query:**
```sql
-- PostgreSQL: VALUES unpivot
WITH long_format AS (
  SELECT year, quarter, revenue
  FROM revenue_wide
  CROSS JOIN LATERAL (
    VALUES
      (1, q1),
      (2, q2),
      (3, q3),
      (4, q4)
  ) AS t(quarter, revenue)
)
SELECT
  year,
  quarter,
  revenue,
  RANK() OVER (PARTITION BY year ORDER BY revenue DESC) AS quarter_rank
FROM long_format
ORDER BY year, quarter;
```

**Alt1:** Oracle UNPIVOT operator:
```sql
-- Oracle
SELECT
  year,
  quarter,
  revenue,
  RANK() OVER (PARTITION BY year ORDER BY revenue DESC) AS quarter_rank
FROM revenue_wide
UNPIVOT (revenue FOR quarter IN (q1 AS 1, q2 AS 2, q3 AS 3, q4 AS 4));
```

**Explanation:** The VALUES/LATERAL pattern is the portable unpivot; Oracle has a dedicated UNPIVOT. **Interview trick:** The reverse (pivoting) uses `MAX(CASE WHEN ...)`; these questions rotate all the time — know both directions.

---

## Q82: SQL Server — LEAD/LAG With OFFSET Partitions

**Tables:** `sales_team(region VARCHAR, salesperson VARCHAR, month DATE, sales DECIMAL)`. SQL Server: for each salesperson, compare this month's sales to the same month last year.

**Query:**
```sql
-- SQL Server
SELECT
  region,
  salesperson,
  month,
  sales,
  LAG(sales, 12) OVER (
    PARTITION BY region, salesperson ORDER BY month
  ) AS sales_same_month_prev_year,
  (sales - LAG(sales, 12) OVER (
    PARTITION BY region, salesperson ORDER BY month
  )) / NULLIF(LAG(sales, 12) OVER (
    PARTITION BY region, salesperson ORDER BY month
  ), 0) * 100.0 AS yoy_change_pct
FROM sales_team
WHERE salesperson = 'Alice'
ORDER BY month;
```

**Explanation:** LAG with offset 12 reaches the same calendar month last year, provided the table has all 13 months. **Interview trick:** SQL Server's `/` does integer division for INTs — always multiply by 100.0 or CAST to DECIMAL, a classic SQL Server gotcha.

---

## Q83: Weighted Median Per Category

**Tables:** `inventory(item_id INT, category VARCHAR, price DECIMAL, units_sold INT)`. Compute the units-sold-weighted median price per category.

**Query:**
```sql
WITH sorted AS (
  SELECT
    category,
    price,
    units_sold,
    SUM(units_sold) OVER (
      PARTITION BY category ORDER BY price
    ) AS cum_units,
    SUM(units_sold) OVER (
      PARTITION BY category
    ) AS total_units
  FROM inventory
)
SELECT
  category,
  price AS weighted_median_price
FROM (
  SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY category ORDER BY cum_units
    ) AS rn
  FROM sorted
  WHERE cum_units >= total_units / 2.0
) r
WHERE rn = 1
ORDER BY category;
```

**Explanation:** Cumulative units by ascending price; the price where cumulative weight crosses half of the total is the weighted median. **Interview trick:** This is the E-commerce dashboard equivalent of "median order value weighted by units" — know exact syntax as percentile functions don't take weights.

---

## Q84: CAGR — Compound Annual Growth Rate

**Tables:** `company_revenue(year INT, revenue DECIMAL)`. Compute year-over-year growth and the CAGR for each trailing 3-year and 5-year window.

**Query:**
```sql
WITH revenue AS (
  SELECT
    year,
    revenue,
    LAG(revenue, 3) OVER (ORDER BY year) AS revenue_3y_ago,
    LAG(revenue, 5) OVER (ORDER BY year) AS revenue_5y_ago,
    LAG(revenue, 1) OVER (ORDER BY year) AS revenue_prev_year
  FROM company_revenue
)
SELECT
  year,
  ROUND(revenue, 2) AS revenue,
  ROUND(
    (revenue - revenue_prev_year) / NULLIF(revenue_prev_year, 0) * 100, 2
  ) AS yoy_growth_pct,
  ROUND(POWER(revenue / NULLIF(revenue_3y_ago, 0), 1.0 / 3.0) - 1, 4) * 100 AS cagr_3y_pct,
  ROUND(POWER(revenue / NULLIF(revenue_5y_ago, 0), 1.0 / 5.0) - 1, 4) * 100 AS cagr_5y_pct
FROM revenue
WHERE revenue_3y_ago IS NOT NULL
ORDER BY year;
```

**Explanation:** CAGR = (end/start)^(1/n) - 1. LAG with offsets fetches the start-of-window values. **Interview trick:** `POWER` type-casting matters — 1.0/3.0 instead of 1/3 avoids integer division returning 0.

---

## Q85: Top N Per Group With Ties (RANK Approach)

**Tables:** `student_scores(student_id INT, subject VARCHAR, score INT)`. Find all students who achieved the top 3 scores in each subject, including ties.

**Query:**
```sql
WITH ranked AS (
  SELECT
    student_id,
    subject,
    score,
    RANK() OVER (PARTITION BY subject ORDER BY score DESC) AS pos
  FROM student_scores
)
SELECT subject, pos, student_id, score
FROM ranked
WHERE pos <= 3
ORDER BY subject, pos;
```

**Explanation:** `RANK` leaves gaps after ties, so both students tying 2nd place get pos=2 and the next is 4 — this preserves "top N distinct score levels." **Interview trick:** RANK (ties share, gaps) vs DENSE_RANK (ties share, no gaps) vs ROW_NUMBER (unique). Each answers a different "top 3."

---

## Q86: Users Who Completed an Entire Required Action Set

**Tables:** `user_actions(user_id INT, action VARCHAR, action_time TIMESTAMP)`. Platform onboarding: list users who completed ALL of: `account_setup`*, `profile_complete`, `first_upload`, plus optional `invite_sent`.

**Query:**
```sql
SELECT
  user_id
FROM user_actions
WHERE action IN ('account_setup', 'profile_complete', 'first_upload')
GROUP BY user_id
HAVING COUNT(DISTINCT action) = 3
ORDER BY user_id;
```

**Alt1:** If optional actions can be ignored and every user may have incomplete set:
```sql
WITH required AS (
  SELECT
    user_id,
    SUM(CASE WHEN action = 'account_setup'   THEN 1 ELSE 0 END) AS done_1,
    SUM(CASE WHEN action = 'profile_complete' THEN 1 ELSE 0 END) AS done_2,
    SUM(CASE WHEN action = 'first_upload'     THEN 1 ELSE 0 END) AS done_3
  FROM user_actions
  GROUP BY user_id
)
SELECT user_id
FROM required
WHERE done_1 = 1 AND done_2 = 1 AND done_3 = 1;
```

**Explanation:** HAVING with a strict equality count is the set-completion test. **Interview trick:** Use `>=` not `=` if users can repeat actions; and `COUNT(DISTINCT action)` prevents a single duplicated action from satisfying the count.

---

## Q87: Gaps in Order IDs — Missing Sequence Detection

**Tables:** `orders(order_id INT, customer_id INT, order_date DATE)`. Find gaps in order_id sequences (skipped IDs).

**Query:**
```sql
WITH base AS (
  SELECT order_id, LAG(order_id) OVER (ORDER BY order_id) AS prev_id
  FROM orders
)
SELECT
  prev_id + 1 AS missing_start,
  order_id - 1 AS missing_end,
  order_id - prev_id - 1 AS missing_count
FROM base
WHERE prev_id IS NOT NULL
  AND order_id - prev_id > 1
ORDER BY prev_id;
```

**Explanation:** LAG over ascending IDs; a gap exists when the difference > 1. **Interview trick:** This reveals at a glance single-ID gaps (start=end) vs large hole ranges. Add `AND order_id - prev_id > 1` condition carefully to exclude the first row.

---

## Q88: Cumulative Sum That Resets on a Condition

**Tables:** `manufacturing(part_id INT, event_date DATE, defect_count INT, has_changeover DATE)`. Compute a running defect total that resets each time a production run indicator changes.

**Query:**
```sql
WITH changeover_flags AS (
  SELECT
    part_id,
    event_date,
    defect_count,
    changeover_flag,
    SUM(changeover_flag) OVER (PARTITION BY part_id ORDER BY event_date) AS run_group
  FROM manufacturing
)
SELECT
  part_id,
  event_date,
  defect_count,
  run_group,
  SUM(defect_count) OVER (
    PARTITION BY part_id, run_group ORDER BY event_date
  ) AS running_defects_per_run
FROM changeover_flags
ORDER BY part_id, event_date;
```

**Explanation:** A running SUM of the changeover flag × partitions creates reset buckets; then running SUM within each bucket. **Interview trick:** This two-level SUM (bucket id + running total) is the standard "running total with reset" pattern.

---

## Q89: Session Revenue With Multiple Payment Attempts

**Tables:** `payment_attempts(attempt_id INT, session_id INT, amount DECIMAL, status VARCHAR, attempt_time TIMESTAMP)`. For each session, compute total successfully collected revenue, attempts count, and time to first successful payment.

**Query:**
```sql
WITH attempts AS (
  SELECT
    session_id,
    attempt_id,
    amount,
    status,
    attempt_time,
    ROW_NUMBER() OVER (
      PARTITION BY session_id, status ORDER BY attempt_time
    ) AS rn,
    MIN(attempt_time) FILTER (WHERE status = 'success')
      OVER (PARTITION BY session_id) AS first_success_time
  FROM payment_attempts
)
SELECT
  session_id,
  SUM(CASE WHEN status = 'success' THEN amount ELSE 0 END) AS collected_revenue,
  COUNT(attempt_id) AS total_attempts,
  SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) AS successful_payments,
  MIN(
    EXTRACT(EPOCH FROM first_success_time - attempt_time) FILTER (WHERE rn = 1 AND status = 'success')
  ) / 60.0 AS min_to_first_success_attempt
FROM attempts
GROUP BY session_id
ORDER BY session_id;
```

**Alt1:** First-success time per session via a second CTE:
```sql
WITH success_times AS (
  SELECT session_id, MIN(attempt_time) AS first_success
  FROM payment_attempts
  WHERE status = 'success'
  GROUP BY session_id
),
joined AS (
  SELECT
    a.session_id,
    a.status,
    a.amount,
    EXTRACT(EPOCH FROM s.first_success - a.attempt_time) / 60.0 AS min_to_success
  FROM payment_attempts a
  LEFT JOIN success_times s ON a.session_id = s.session_id
  WHERE a.status <> 'failure'
)
SELECT
  session_id,
  SUM(CASE WHEN status = 'success' THEN amount ELSE 0 END) AS collected_revenue,
  AVG(min_to_success) AS avg_min_to_success
FROM joined
GROUP BY session_id;
```

**Explanation:** Status-aware sums and the earliest success timestamp tell a payment-friction story. **Interview trick:** Filtering non-failure attempts keeps the time-to-success metric clean; the first approach counts attempts but the second is simpler to read.

---

## Q90: Currency Conversion — As-Of Rate Join

**Tables:** `orders(order_id INT, amount_local DECIMAL, currency VARCHAR, order_date DATE)`, `exchange_rates(currency VARCHAR, effective_date DATE, rate DECIMAL)`. Convert every order to USD using the most recent exchange rate on or before the order date.

**Query:**
```sql
SELECT
  o.order_id,
  o.currency,
  o.amount_local,
  r.effective_date AS rate_date,
  r.rate,
  ROUND(o.amount_local / r.rate, 2) AS amount_usd
FROM orders o
JOIN exchange_rates r
  ON o.currency = r.currency
  AND r.effective_date = (
    SELECT MAX(r2.effective_date)
    FROM exchange_rates r2
    WHERE r2.currency = o.currency
      AND r2.effective_date <= o.order_date
  );
```

**Alt1:** Range join with a filter:
```sql
WITH rate_pairs AS (
  SELECT
    o.order_id,
    o.amount_local,
    r.rate,
    ROW_NUMBER() OVER (
      PARTITION BY o.order_id
      ORDER BY r.effective_date DESC
    ) AS rn
  FROM orders o
  JOIN exchange_rates r
    ON o.currency = r.currency
    AND r.effective_date <= o.order_date
)
SELECT order_id, amount_local, rate, ROUND(amount_local / rate, 2) AS amount_usd
FROM rate_pairs
WHERE rn = 1;
```

**Explanation:** The correlated-subquery version picks the latest rate on-or-before order date. **Interview trick:** The ROW_NUMBER variant scales better on big tables (single pass). Some interviews want "nearest date either direction" — interpolate or use `MIN(ABS(diff))` with ties handled.

---

## Q91: Funnel Conversion by Variant — A/B Test Comparison

**Tables:** `ab_events(user_id INT, variant VARCHAR, event_type VARCHAR, event_time TIMESTAMP)`. Compare the view→purchase conversion rate between the control ('A') and treatment ('B') variants.

**Query:**
```sql
WITH variant_users AS (
  SELECT
    variant,
    user_id,
    MAX(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) AS viewed,
    MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchased
  FROM ab_events
  GROUP BY variant, user_id
)
SELECT
  variant,
  COUNT(*) AS users,
  SUM(viewed) AS viewers,
  SUM(purchased) AS purchasers,
  ROUND(100.0 * SUM(purchased) / NULLIF(SUM(viewed), 0), 2) AS conversion_pct,
  ROUND(100.0 * COUNT(*) FILTER (WHERE viewed = 1) / COUNT(*), 2) AS view_rate_pct
FROM variant_users
GROUP BY variant
ORDER BY variant;
```

**Explanation:** Pivot each user into flags, then compute per-variant rates. **Interview trick:** Give the raw conversion delta, then mention you'd run a statistical test (e.g. chi-square) for significance — interviewers hear the extra step.

---

## Q92: Device-Segmented Funnel

**Tables:** `sessions_events(session_id INT, user_id INT, device VARCHAR, event_type VARCHAR, event_time TIMESTAMP)`. Segment the view→cart→purchase funnel by mobile vs desktop.

**Query:**
```sql
WITH funnel AS (
  SELECT
    user_id,
    device,
    MAX(CASE WHEN event_type = 'view'     THEN 1 ELSE 0 END) AS step_view,
    MAX(CASE WHEN event_type = 'cart'     THEN 1 ELSE 0 END) AS step_cart,
    MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS step_purchase
  FROM sessions_events
  GROUP BY user_id, device
)
SELECT
  device,
  COUNT(*) AS users,
  SUM(step_view) AS step_1_view,
  SUM(step_cart) AS step_2_cart,
  SUM(step_purchase) AS step_3_purchase,
  ROUND(100.0 * SUM(step_cart) / NULLIF(SUM(step_view), 0), 2) AS view_to_cart_pct,
  ROUND(100.0 * SUM(step_purchase) / NULLIF(SUM(step_cart), 0), 2) AS cart_to_purchase_pct,
  ROUND(100.0 * SUM(step_purchase) / NULLIF(SUM(step_view), 0), 2) AS overall_pct
FROM funnel
GROUP BY device
ORDER BY overall_pct DESC;
```

**Explanation:** Same funnel pattern as Q4 but grouped per device. **Interview trick:** Watch for the stepwise vs overall rate distinction — mobile usually wins on view-to-cart but loses on cart-to-purchase.

---

## Q93: Percentiles Per Category (Latency SLO)

**Tables:** `api_logs(api_name VARCHAR, latency_ms INT, request_time TIMESTAMP)`. Compute p50, p95, and p99 latency per API endpoint.

**Query:**
```sql
-- PostgreSQL
SELECT
  api_name,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY latency_ms) AS p50_ms,
  PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency_ms) AS p95_ms,
  PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY latency_ms) AS p99_ms,
  COUNT(*) AS request_count
FROM api_logs
GROUP BY api_name
ORDER BY p99_ms DESC;
```

**Alt1:** SQL Server:
```sql
-- SQL Server
SELECT DISTINCT
  api_name,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY latency_ms) OVER (PARTITION BY api_name) AS p50_ms,
  PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency_ms) OVER (PARTITION BY api_name) AS p95_ms,
  PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY latency_ms) OVER (PARTITION BY api_name) AS p99_ms
FROM api_logs;
```

**Explanation:** PERCENTILE_CONT per endpoint with no window = group-by percentile. **Interview trick:** SQL Server and PostgreSQL differ — the former requires WITHIN GROUP as a window function, PostgreSQL allows the concise aggregate form.

---

## Q94: Decile Analysis of API Latency — SLO Compliance

**Tables:** `request_logs(request_id INT, endpoint VARCHAR, latency_ms INT, status INT)`. Split requests into 10 latency deciles per endpoint, and compute SLO non-compliance (status != 200 OR latency > 500ms) per decile.

**Query:**
```sql
WITH deciled AS (
  SELECT
    request_id,
    endpoint,
    latency_ms,
    status,
    NTILE(10) OVER (PARTITION BY endpoint ORDER BY latency_ms) AS latency_decile
  FROM request_logs
)
SELECT
  endpoint,
  latency_decile,
  COUNT(*) AS requests,
  ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY latency_ms), 0) AS median_latency_ms,
  ROUND(PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY latency_ms), 0) AS p90_latency_ms,
  SUM(CASE WHEN status != 200 OR latency_ms > 500 THEN 1 ELSE 0 END) AS violations,
  ROUND(
    100.0 * SUM(CASE WHEN status != 200 OR latency_ms > 500 THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS violation_pct
FROM deciled
GROUP BY endpoint, latency_decile
ORDER BY endpoint, latency_decile;
```

**Explanation:** NTILE gives deciles; the CASE counts SLO violations per bucket. **Interview trick:** Present the ratio not the raw counts — multiplying by 100.0 avoids rank of magnitude confusion.

---

## Q95: Session Event Path Concatenation

**Tables:** `events(session_id INT, event_type VARCHAR, event_time TIMESTAMP)`. Reconstruct each session's ordered event path as a single string.

**Query:**
```sql
-- PostgreSQL
SELECT
  session_id,
  STRING_AGG(event_type, ' → ' ORDER BY event_time) AS event_path
FROM events
GROUP BY session_id
ORDER BY session_id;
```

**Alt1:** MySQL GROUP_CONCAT:
```sql
-- MySQL
SELECT
  session_id,
  GROUP_CONCAT(event_type ORDER BY event_time SEPARATOR ' → ') AS event_path
FROM events
GROUP BY session_id;
```

**Alt2:** SQL Server STRING_AGG:
```sql
-- SQL Server
SELECT
  session_id,
  STRING_AGG(event_type, ' → ') WITHIN GROUP (ORDER BY event_time) AS event_path
FROM events
GROUP BY session_id;
```

**Explanation:** String aggregation preserves the exact journey, useful for path-funnels. **Interview trick:** The ORDER BY clause inside STRING_AGG / GROUP_CONCAT differs by dialect (Postgres inline, SQL Server WITHIN GROUP). Knowing all three in a single answer is a differentiator.

---

## Q96: Session Duration vs Purchase — Hypothesis Query

**Tables:** `sessions(session_id INT, user_id INT, session_start TIMESTAMP, session_end TIMESTAMP)`, `session_purchases(session_id INT, amount DECIMAL)`. Compare the purchase rate of short (< 5 min) vs long (>= 5 min) sessions.

**Query:**
```sql
WITH session_bucket AS (
  SELECT
    s.session_id,
    s.user_id,
    EXTRACT(EPOCH FROM s.session_end - s.session_start) / 60.0 AS duration_min,
    COALESCE(sp.amount, 0) AS purchase_amount,
    CASE WHEN sp.session_id IS NOT NULL THEN 1 ELSE 0 END AS purchased
  FROM sessions s
  LEFT JOIN session_purchases sp ON s.session_id = sp.session_id
)
SELECT
  CASE
    WHEN duration_min < 5 THEN 'short (<5m)'
    WHEN duration_min < 15 THEN 'medium (5-15m)'
    ELSE 'long (>15m)'
  END AS session_length,
  COUNT(*) AS sessions,
  SUM(purchased) AS with_purchase,
  ROUND(100.0 * SUM(purchased) / COUNT(*), 2) AS purchase_rate_pct,
  ROUND(AVG(purchase_amount), 2) AS avg_purchase_amount,
  ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY duration_min), 1) AS median_duration_min
FROM session_bucket
GROUP BY 1
ORDER BY purchase_rate_pct DESC;
```

**Explanation:** Bucket sessions by duration, compute purchase metrics per bucket. **Interview trick:** The COALESCE in payment aggregation is important — a zero purchase must be counted, so NULL from the LEFT JOIN becomes an explicit 0.

---

## Q97: User 30-60-90 Day Behavior Vectors

**Tables:** `events(user_id INT, event_time TIMESTAMP)`, `orders(user_id INT, order_time TIMESTAMP, amount DECIMAL)`. Build a 30/60/90-day feature vector per user for modeling: events, orders, and amounts in each bucket relative to signup.

**Query:**
```sql
WITH users_base AS (
  SELECT DISTINCT user_id FROM events
),
days_vectors AS (
  SELECT
    u.user_id,
    COUNT(DISTINCT DATE_TRUNC('day', e.event_time)) AS active_days_90,
    COUNT(e.event_time) AS total_events_90,
    COUNT(e.event_time) FILTER (
      WHERE e.event_time < MIN(o.order_time) OVER (
        PARTITION BY u.user_id
      )
    ) AS pre_first_order_events,
    COALESCE(SUM(o.amount) FILTER (
      WHERE o.order_time - (SELECT MIN(o2.order_time) FROM orders o2 WHERE o2.user_id = u.user_id) < INTERVAL '30 days'
    ), 0) AS amount_30d
  FROM users_base u
  LEFT JOIN events e ON u.user_id = e.user_id
  LEFT JOIN orders o ON u.user_id = o.user_id
  GROUP BY u.user_id
)
SELECT
  user_id,
  active_days_90,
  total_events_90,
  pre_first_order_events,
  amount_30d,
  DENSE_RANK() OVER (ORDER BY amount_30d DESC, total_events_90 DESC) AS engagement_rank
FROM days_vectors
ORDER BY engagement_rank;
```

**Explanation:** Window-based MIN for first order time and FILTER-based date arithmetic build per-user time-boxed aggregates. **Interview trick:** This is the SQL side of feature engineering — interviewers grade on clarity of the time-bucket definitions more than the code.

---

## Q98: CAPSTONE PART 1 — Full Sessionization Pipeline

**Tables:** `raw_events(user_id INT, event_type VARCHAR, event_time TIMESTAMP)`. Stage one of the capstone: split events into sessions (>30 min gap), compute per-session metrics, and produce a pollution-free session ID.

**Query:**
```sql
WITH flags AS (
  SELECT
    user_id,
    event_type,
    event_time,
    CASE
      WHEN LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time) IS NULL
        THEN 1
      WHEN event_time - LAG(event_time) OVER (
        PARTITION BY user_id ORDER BY event_time
      ) > INTERVAL '30 minutes'
        THEN 1
      ELSE 0
    END AS session_flag
  FROM raw_events
),
sessionized AS (
  SELECT
    *,
    SUM(session_flag) OVER (
      PARTITION BY user_id ORDER BY event_time
    ) AS session_num
  FROM flags
),
session_metrics AS (
  SELECT
    user_id,
    session_num,
    MIN(event_time) AS session_start,
    MAX(event_time) AS session_end,
    COUNT(*) AS event_count,
    COUNT(*) FILTER (WHERE event_type = 'purchase') AS purchase_count
  FROM sessionized
  GROUP BY user_id, session_num
)
SELECT
  user_id,
  session_num,
  session_start,
  session_end,
  EXTRACT(EPOCH FROM session_end - session_start) / 60.0 AS duration_min,
  event_count,
  purchase_count,
  DENSE_RANK() OVER (
    PARTITION BY user_id ORDER BY session_start
  ) AS session_order
FROM session_metrics
ORDER BY user_id, session_start;
```

**Explanation:** Three CTE stages: flag → running-sum badge → aggregate. NULL LAG on the very first event is explicitly handled. **Interview trick:** Notice the explicit NULL guard — your first event per user must start a session, not rely on implicit behavior.

---

## Q99: CAPSTONE PART 2 — Funnel Across Sessions

**Tables:** Reuse `raw_events(user_id INT, event_type VARCHAR, event_time TIMESTAMP)` (from Part 1). For each user, compute the funnel view→cart→checkout→purchase, but only counting events in their FIRST session of the day.

**Query:**
```sql
WITH daily_first_session AS (
  SELECT
    user_id,
    DATE_TRUNC('day', MIN(event_time)) AS day,
    SUM(session_flag) OVER (
      PARTITION BY user_id ORDER BY event_time
    ) AS session_num
  FROM (
    SELECT
      user_id,
      event_type,
      event_time,
      CASE
        WHEN LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time) IS NULL
          OR event_time - LAG(event_time) OVER (
            PARTITION BY user_id ORDER BY event_time
          ) > INTERVAL '30 minutes'
          THEN 1
        ELSE 0
      END AS session_flag
    FROM raw_events
  ) s
  GROUP BY user_id, s.session_flag
),
first_session_flags AS (
  SELECT
    f.user_id,
    f.day,
    e.event_type,
    MAX(CASE WHEN e.event_type = 'view'     THEN 1 ELSE 0 END) AS saw_view,
    MAX(CASE WHEN e.event_type = 'cart'     THEN 1 ELSE 0 END) AS saw_cart,
    MAX(CASE WHEN e.event_type = 'checkout' THEN 1 ELSE 0 END) AS saw_checkout,
    MAX(CASE WHEN e.event_type = 'purchase' THEN 1 ELSE 0 END) AS saw_purchase
  FROM daily_first_session f
  JOIN raw_events e
    ON f.user_id = e.user_id
    AND DATE_TRUNC('day', e.event_time) = f.day
    AND e.event_time < f.day + INTERVAL '1 day'
  GROUP BY f.user_id, f.day, e.event_type
)
SELECT
  user_id,
  day,
  MAX(saw_view) AS step_view,
  MAX(saw_cart) AS step_cart,
  MAX(saw_checkout) AS step_checkout,
  MAX(saw_purchase) AS step_purchase
FROM first_session_flags
GROUP BY user_id, day
ORDER BY user_id, day;
```

**Explanation:** Normalize to the first session per day, then flag 4 step types. This shows a key constraint — "first session only" — which almost every real funnel has. **Interview trick:** The `first session of the day` requirement forces you to think about session boundaries; state your assumption about day thresholds early.

---

## Q100: CAPSTONE PART 3 — Retention Curve and Final Report

**Tables:** Reuse `raw_events(user_id INT, event_type VARCHAR, event_time TIMESTAMP)`. Compute cohort retention (D0/D1/D7/D30) per weekly cohort and final aggregated dashboard.

**Query:**
```sql
WITH cohorts AS (
  SELECT
    user_id,
    MIN(DATE_TRUNC('week', event_time)) AS cohort_week
  FROM raw_events
  GROUP BY user_id
),
days_active AS (
  SELECT
    c.user_id,
    c.cohort_week,
    e.event_time::DATE AS active_day,
    e.event_time::DATE - c.cohort_week AS day_offset
  FROM cohorts c
  LEFT JOIN raw_events e ON c.user_id = e.user_id
  WHERE e.event_time BETWEEN c.cohort_week AND c.cohort_week + INTERVAL '30 days'
),
cohort_retention AS (
  SELECT
    cohort_week,
    SUM(CASE WHEN day_offset = 0  THEN 1 ELSE 0 END) AS day0,
    SUM(CASE WHEN day_offset = 1  THEN 1 ELSE 0 END) AS day1,
    SUM(CASE WHEN day_offset = 7  THEN 1 ELSE 0 END) AS day7,
    SUM(CASE WHEN day_offset = 30 THEN 1 ELSE 0 END) AS day30
  FROM days_active
  GROUP BY cohort_week
)
SELECT
  cohort_week,
  ROUND(100.0 * day1  / NULLIF(day0, 0), 2) AS d1_retention,
  ROUND(100.0 * day7  / NULLIF(day0, 0), 2) AS d7_retention,
  ROUND(100.0 * day30 / NULLIF(day0, 0), 2) AS d30_retention,
  ROUND((day7 - day1) / NULLIF(day1, 0) * 100, 2) AS day1_to_day7_growth_pct,
  ROUND(
    (100.0 * day30 / NULLIF(day0, 0)) / (100.0 * day7 / NULLIF(day0, 0)) * 100 - 100, 2
  ) AS d7_to_d30_drop_pct
FROM cohort_retention
ORDER BY cohort_week;
```

**Explanation:** Weekly cohorts, day offsets from cohort start, and a retention waterfall table ready to be exported. **Interview trick:** In a live interview capstone, candidates are expected to explain why `d1_to_day7_growth_pct` can exceed 100% (users return on day 7 who didn't on day 1), and to comment on which window smoothing removes weekend noise.

---
