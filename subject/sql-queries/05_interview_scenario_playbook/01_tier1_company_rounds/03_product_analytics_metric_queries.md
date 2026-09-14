# Product Analytics and Metric Queries — 100 SQL Interview Q&A

## Q1: Compute DAU (daily active users) per day.

Tables: `events(event_id, user_id, event_time TIMESTAMP, event_type)`; a user is active on a day if they fired any event that day.

**Query:**
```sql
-- PostgreSQL
SELECT event_time::date            AS day
     , COUNT(DISTINCT user_id)     AS dau
FROM   events
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** DAU is distinct users active per calendar day; the DISTINCT is what turns raw event volume into an active-user metric.

**Alt1:**
```sql
-- MySQL 8+
SELECT DATE(event_time)        AS day
     , COUNT(DISTINCT user_id) AS dau
FROM   events
GROUP  BY DATE(event_time)
ORDER  BY day;
```

## Q2: Compute WAU (weekly active users) for each ISO week.

Tables: `events(event_id, user_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL
SELECT date_trunc('week', event_time)              AS week_start
     , COUNT(DISTINCT user_id)                     AS wau
FROM   events
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** WAU is distinct users active within a Monday-starting week; `date_trunc('week', ts)` buckets timestamps into calendar weeks.

**Alt1:**
```sql
-- MySQL (ISO week, mode 3)
SELECT YEAR(event_time)                       AS yr
     , WEEK(event_time, 3)                    AS week_no
     , COUNT(DISTINCT user_id)                AS wau
FROM   events
GROUP  BY 1, 2
ORDER  BY 1, 2;
```

## Q3: Compute MAU (monthly active users) for each calendar month.

Tables: `events(event_id, user_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL
SELECT date_trunc('month', event_time)          AS month
     , COUNT(DISTINCT user_id)                  AS mau
FROM   events
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** MAU is distinct users active within a calendar month; truncation normalizes all timestamps to the first of the month so GROUP BY collapses cleanly.

**Alt1:**
```sql
-- SQL Server
SELECT DATEFROMPARTS(YEAR(event_time), MONTH(event_time), 1) AS month
     , COUNT(DISTINCT user_id)                               AS mau
FROM   events
GROUP  BY DATEFROMPARTS(YEAR(event_time), MONTH(event_time), 1)
ORDER  BY month;
```

## Q4: DAU trend with day-over-day growth percentage.

Tables: `events(event_id, user_id, event_time TIMESTAMP)`; `users(user_id, signup_date)`.

**Query:**
```sql
-- PostgreSQL
WITH daily AS (
  SELECT event_time::date AS day
       , COUNT(DISTINCT user_id) AS dau
  FROM   events
  GROUP  BY 1
)
SELECT day
     , dau
     , LAG(dau) OVER (ORDER BY day)                                     AS prev_dau
     , ROUND(100.0 * (dau - LAG(dau) OVER (ORDER BY day))
                     / NULLIF(LAG(dau) OVER (ORDER BY day), 0), 2)      AS dod_growth_pct
FROM   daily
ORDER  BY day;
```
**Explanation:** Dod growth = `(DAU − prior DAU) / prior DAU`; `LAG` reads the previous row and `NULLIF` avoids a divide-by-zero on the first day.

**Alt1:**
```sql
-- MySQL 8+
WITH daily AS (
  SELECT DATE(event_time) AS day, COUNT(DISTINCT user_id) AS dau
  FROM   events
  GROUP  BY 1
)
SELECT day, dau,
       (dau / NULLIF(LAG(dau) OVER (ORDER BY day), 0) - 1) * 100 AS dod_growth_pct
FROM   daily
ORDER  BY day;
```

## Q5: Count active users on a rolling trailing 7-day window (overlapping, not calendar weeks).

Tables: `events(event_id, user_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL
WITH daily AS (
  SELECT event_time::date AS day, user_id
  FROM   events
  GROUP  BY 1, 2
)
SELECT day,
       (SELECT COUNT(DISTINCT user_id)
        FROM   daily d2
        WHERE  d2.day > d1.day - 7 AND d2.day <= d1.day) AS rolling_7day_active
FROM   (SELECT DISTINCT day FROM daily) d1
ORDER  BY day;
```
**Explanation:** The trailing window looks back 7 days ending at each day, so consecutive days share overlapping user pools — the point of "overlapping" growth metrics vs non-overlapping calendar buckets.

## Q6: Active users on a rolling trailing 28-day window (overlapping MAU proxy).

Tables: `events(event_id, user_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL
SELECT DISTINCT day,
       COUNT(DISTINCT user_id) OVER (ORDER BY day RANGE BETWEEN 27 PRECEDING AND CURRENT ROW) AS rolling_28day_active
FROM   (SELECT event_time::date AS day, user_id FROM events GROUP BY 1, 2) d;
```
**Explanation:** A window function with `RANGE BETWEEN 27 PRECEDING AND CURRENT ROW` counts distinct users whose active day falls inside the trailing 28-day frame for each day.

**Alt1:**
```sql
-- MySQL 8+: frame can't hold DISTINCT, so use a correlated subquery
SELECT d1.day,
       (SELECT COUNT(DISTINCT user_id)
        FROM   events e
        WHERE  DATE(e.event_time) <= d1.day
          AND  DATE(e.event_time) > d1.day - 28) AS rolling_28day_active
FROM   (SELECT DISTINCT DATE(event_time) AS day FROM events) d1
ORDER  BY d1.day;
```

## Q7: Compare calendar-week WAU against trailing 7-day activity on each day.

Tables: `events(event_id, user_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL
WITH daily AS (
  SELECT event_time::date AS day, user_id FROM events GROUP BY 1, 2
)
SELECT day
     , COUNT(DISTINCT user_id) AS dau
     , (SELECT COUNT(DISTINCT user_id) FROM daily d2
        WHERE d2.day > d1.day - 7 AND d2.day <= d1.day)                       AS trailing7
     , (SELECT COUNT(DISTINCT user_id) FROM daily d3
        WHERE date_trunc('week', d3.day) = date_trunc('week', d1.day))        AS cal_week
FROM   (SELECT DISTINCT day FROM daily) d1
ORDER  BY day;
```
**Explanation:** trailing7 slides forward day by day (overlapping pool) while cal_week is a fixed Monday–Sunday bucket; the gap between the two reveals intra-week onboarding spikes.

## Q8: Monthly stickiness ratio — DAU/MAU averaged per month.

Tables: `events(event_id, user_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL
WITH daily AS (
  SELECT event_time::date AS day, COUNT(DISTINCT user_id) AS dau
  FROM   events GROUP BY 1
)
SELECT date_trunc('month', day)                                 AS month
     , AVG(dau)                                                 AS avg_dau
     , (SELECT COUNT(DISTINCT user_id) FROM events e
        WHERE date_trunc('month', e.event_time) = date_trunc('month', dd.day)) AS mau
     , ROUND(100.0 * AVG(dau) / NULLIF(
         (SELECT COUNT(DISTINCT user_id) FROM events e
          WHERE date_trunc('month', e.event_time) = date_trunc('month', dd.day)), 0), 2) AS stickiness_pct
FROM   daily dd
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** Stickiness = average daily actives ÷ monthly actives for the month; values above ~25% indicate users are returning roughly weekly, below ~10% indicates shallow engagement.

**Alt1:**
```sql
-- SQL Server: single pass, stickiness via two subqueries
SELECT date_trunc_month.m                              AS month
     , ROUND(100.0 * avg_dau / NULLIF(mau, 0), 2)      AS stickiness_pct
FROM   (SELECT DATEFROMPARTS(YEAR(event_time), MONTH(event_time), 1) AS m,
               AVG(1.0 * cnt) AS avg_dau
        FROM   (SELECT CAST(event_time AS date) AS d,
                       COUNT(DISTINCT user_id) AS cnt
                FROM   events GROUP BY CAST(event_time AS date)) t
        GROUP  BY DATEFROMPARTS(YEAR(event_time), MONTH(event_time), 1)) date_trunc_month
JOIN   (SELECT DATEFROMPARTS(YEAR(event_time), MONTH(event_time), 1) AS m,
               COUNT(DISTINCT user_id) AS mau
        FROM   events
        GROUP  BY DATEFROMPARTS(YEAR(event_time), MONTH(event_time), 1)) monthly ON monthly.m = date_trunc_month.m
ORDER  BY month;
```

## Q9: Longest streak of consecutive active days per user.

Tables: `events(event_id, user_id, event_time DATE)`.

**Query:**
```sql
-- PostgreSQL
WITH alive AS (
  SELECT user_id, event_time AS day
  FROM   events
  GROUP  BY 1, 2
),
grpd AS (
  SELECT user_id, day
       , day - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day)::int) AS grp
  FROM   alive
)
SELECT user_id, MAX(streak) AS longest_streak
FROM (
  SELECT user_id, grp, COUNT(*) AS streak
  FROM   grpd
  GROUP  BY user_id, grp
) s
GROUP  BY user_id
ORDER  BY longest_streak DESC;
```
**Explanation:** The classic "gaps-and-islands" trick: subtracting a per-user row number from the date leaves a constant `grp` for consecutive dates, so each island of contiguous days becomes one group to count.

**Alt1:**
```sql
-- MySQL 8+ (identical technique)
WITH alive AS (
  SELECT user_id, event_time AS day FROM events GROUP BY 1, 2
),
grpd AS (
  SELECT user_id, day,
         DATE_SUB(day, INTERVAL ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day) DAY) AS grp
  FROM   alive
)
SELECT user_id, MAX(cnt) AS longest_streak
FROM   (SELECT user_id, grp, COUNT(*) AS cnt FROM grpd GROUP BY 1, 2) s
GROUP  BY user_id
ORDER  BY longest_streak DESC;
```

## Q10: Users active today who were also active in each of the two prior days (3-day engagement win).

Tables: `events(event_id, user_id, event_time DATE)`.

**Query:**
```sql
-- PostgreSQL
WITH act AS (SELECT DISTINCT user_id, event_time AS day FROM events)
SELECT act.day
     , COUNT(DISTINCT act.user_id) AS active_3_consecutive
FROM   act
WHERE  EXISTS (SELECT 1 FROM act a1 WHERE a1.user_id = act.user_id AND a1.day = act.day - 1)
  AND  EXISTS (SELECT 1 FROM act a2 WHERE a2.user_id = act.user_id AND a2.day = act.day - 2)
GROUP  BY act.day
ORDER  BY act.day;
```
**Explanation:** An EXISTS clause per lag day verifies presence on each of the previous two dates, giving the cohort of high-frequency users active three days running.

## Q11: Weekly cohort retention — fraction of week-0 actives still active in weeks 1..6.

Tables: `events(event_id, user_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL
WITH w AS (
  SELECT user_id, date_trunc('week', event_time) AS wk
  FROM   events
  GROUP  BY 1, 2
),
cohort AS (
  SELECT user_id, MIN(wk) AS birth_wk FROM w GROUP BY 1
)
SELECT birth_wk,
       COUNT(DISTINCT c.user_id) AS cohort_size,
       COUNT(DISTINCT CASE WHEN w.wk = birth_wk + INTERVAL '1 week'  THEN c.user_id END) AS w1,
       COUNT(DISTINCT CASE WHEN w.wk = birth_wk + INTERVAL '2 weeks' THEN c.user_id END) AS w2,
       COUNT(DISTINCT CASE WHEN w.wk = birth_wk + INTERVAL '4 weeks' THEN c.user_id END) AS w4
FROM   cohort c
LEFT   JOIN w ON w.user_id = c.user_id AND w.wk >= c.birth_wk
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** Retention cohort = distinct users from the birth week who appear in each later week, divided by the birth-week cohort size; weeks are ISO weeks via `date_trunc`.

**Alt1:**
```sql
-- MySQL 8+ (birth week from a users table; events are weekly visits)
SELECT birth_wk,
       COUNT(DISTINCT u.user_id) AS cohort_size,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN v.wk = DATE_ADD(birth_wk, INTERVAL 1 WEEK) THEN u.user_id END)
              / NULLIF(COUNT(DISTINCT u.user_id), 0), 1) AS retention_w1_pct
FROM   (SELECT user_id, DATE_FORMAT(signup_date, '%x-%v-1') AS birth_wk
        FROM   users) u
LEFT   JOIN (SELECT DISTINCT user_id, DATE_FORMAT(event_time, '%x-%v-1') AS wk
             FROM events) v ON v.user_id = u.user_id
GROUP  BY birth_wk;
```

## Q12: Monthly retention matrix — % of each signup month's users active in later months.

Tables: `users(user_id, signup_date DATE)`, `events(event_id, user_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL (pivoted)
WITH months AS (
  SELECT DISTINCT user_id, date_trunc('month', event_time) AS m FROM events
),
birth AS (
  SELECT user_id, date_trunc('month', signup_date) AS bm FROM users
)
SELECT b.bm,
       COUNT(DISTINCT b.user_id) AS cohort_size,
       COUNT(DISTINCT CASE WHEN m.m = b.bm + INTERVAL '1 month'  THEN b.user_id END) AS m1,
       COUNT(DISTINCT CASE WHEN m.m = b.bm + INTERVAL '3 months' THEN b.user_id END) AS m3,
       COUNT(DISTINCT CASE WHEN m.m = b.bm + INTERVAL '6 months' THEN b.user_id END) AS m6
FROM   birth b
LEFT   JOIN months m ON m.user_id = b.user_id AND m.m >= b.bm
GROUP  BY b.bm
ORDER  BY b.bm;
```
**Explanation:** Each column is a fixed offset (month 1, 3, 6) after signup; dividing each count by cohort_size yields the classic retention matrix reading left-to-right across time.

**Alt1:**
```sql
-- Unpivoted long form is easier to chart (justified_interval handles >1yr offsets)
SELECT b.bm,
       EXTRACT(YEAR  FROM (m.m - b.bm)) * 12
     + EXTRACT(MONTH FROM (m.m - b.bm))           AS month_offset,
       COUNT(DISTINCT b.user_id)                  AS active_users
FROM   birth b
JOIN   months m ON m.user_id = b.user_id AND m.m >= b.bm
GROUP  BY b.bm, 2;
```

## Q13: New vs returning users per day.

Tables: `users(user_id, signup_date DATE)`, `events(event_id, user_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL
SELECT e.event_time::date AS day,
       COUNT(DISTINCT u.user_id) AS new_users,
       COUNT(DISTINCT e.user_id) - COUNT(DISTINCT u.user_id) AS returning_users
FROM   events e
LEFT   JOIN users u ON u.user_id = e.user_id AND u.signup_date = e.event_time::date
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** A user counts as "new" on the exact day of signup; everyone else active that day is "returning" = distinct active users minus distinct new users.

**Alt1:**
```sql
-- MySQL 8+ using LEFT JOIN + FIRST decarbonized (same logic)
SELECT DATE(e.event_time) AS day,
       SUM(CASE WHEN DATE(u.signup_date) = DATE(e.event_time) THEN 1 ELSE 0 END) AS new_users
FROM   events e
LEFT   JOIN users u ON u.user_id = e.user_id
GROUP  BY 1
ORDER  BY 1;
```

## Q14: Daily active users who visited at least 3 distinct pages (engaged DAU).

Tables: `events(event_id, user_id, event_time TIMESTAMP, event_type, url)`.

**Query:**
```sql
-- PostgreSQL
SELECT event_time::date AS day,
       COUNT(DISTINCT CASE WHEN page_views >= 3 THEN user_id END) AS engaged_dau
FROM   (
  SELECT user_id, event_time::date,
         COUNT(DISTINCT url) AS page_views
  FROM   events
  WHERE  event_type = 'page_view'
  GROUP  BY 1, 2
) t
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** Engaged DAU applies a depth threshold (≥3 distinct pages) on top of raw DAU, separating casual one-hit visits from meaningful sessions.

## Q15: Distribution of daily visits per user for the last 30 days.

Tables: `events(event_id, user_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL
SELECT visits_per_day, COUNT(*) AS num_users
FROM   (
  SELECT user_id, event_time::date, COUNT(*) AS visits_per_day
  FROM   events
  WHERE  event_time >= CURRENT_DATE - 30
  GROUP  BY 1, 2
) t
GROUP  BY visits_per_day
ORDER  BY visits_per_day;
```
**Explanation:** A histogram built from a GROUP BY user+day — counts the number of (user, day) pairs at each visit level, revealing whether usage is power-law or bimodal.

## Q16: Weekly retention of users who completed onboarding, vs. those who did not.

Tables: `users(user_id, signup_date)`, `user_milestones(user_id, milestone, achieved_at)`, `events(...)`.

**Query:**
```sql
-- PostgreSQL
WITH onboarded AS (
  SELECT DISTINCT user_id FROM user_milestones WHERE milestone = 'onboarding_complete'
)
SELECT date_trunc('week', u.signup_date) AS signup_wk,
       (o.user_id IS NOT NULL) AS completed_onboarding,
       COUNT(DISTINCT u.user_id) AS cohort,
       COUNT(DISTINCT CASE WHEN date_trunc('week', e.event_time) = date_trunc('week', u.signup_date) + INTERVAL '1 week'
                           THEN u.user_id END) AS retained_w1
FROM   users u
LEFT   JOIN onboarded o ON o.user_id = u.user_id
LEFT   JOIN events e    ON e.user_id = u.user_id
GROUP  BY 1, 2
ORDER  BY 1, 2;
```
**Explanation:** Comparing week-1 retention split by an onboarding flag isolates whether the activation milestone is what drives return use.

## Q17: Time between signup and first key action (e.g., first purchase), truncated at 7 days.

Tables: `users(user_id, signup_date TIMESTAMP)`, `orders(order_id, user_id, created_at TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL
SELECT user_id,
       MIN(created_at) - signup_date  AS days_to_first_order,
       LEAST(EXTRACT(EPOCH FROM (MIN(created_at) - signup_date)) / 86400, 7) AS days_capped
FROM   users u
LEFT   JOIN orders o ON o.user_id = u.user_id
GROUP  BY u.user_id, u.signup_date;
```
**Explanation:** Time-to-first-action is a simple MIN on the event table minus signup; capping at 7 days keeps the metric readable for the long-tail of never-converting users.

**Alt1:**
```sql
-- MySQL 8+
SELECT u.user_id,
       TIMESTAMPDIFF(DAY, u.signup_date, MIN(o.created_at)) AS days_to_first_order
FROM   users u
LEFT   JOIN orders o ON o.user_id = u.user_id
GROUP  BY u.user_id, u.signup_date;
```

## Q18: Average time-to-first-purchase, plus distribution buckets.

Tables: `users(user_id, signup_date TIMESTAMP)`, `orders(order_id, user_id, created_at TIMESTAMP)`.

**Query:**
```sql
-- SQL Server
WITH first_orders AS (
  SELECT u.user_id,
         DATEDIFF(DAY, u.signup_date, MIN(o.created_at)) AS ttf
  FROM   users u
  LEFT   JOIN orders o ON o.user_id = u.user_id
  GROUP  BY u.user_id, u.signup_date
)
SELECT CASE
         WHEN ttf IS NULL          THEN 'never'
         WHEN ttf = 0              THEN 'same_day'
         WHEN ttf BETWEEN 1 AND 3  THEN '1-3d'
         WHEN ttf BETWEEN 4 AND 7  THEN '4-7d'
         ELSE 'after_week'
       END AS bucket,
       COUNT(*) AS users
FROM   first_orders
GROUP  BY CASE
         WHEN ttf IS NULL          THEN 'never'
         WHEN ttf = 0              THEN 'same_day'
         WHEN ttf BETWEEN 1 AND 3  THEN '1-3d'
         WHEN ttf BETWEEN 4 AND 7  THEN '4-7d'
         ELSE 'after_week'
       END
ORDER  BY MIN(ttf);
```
**Explanation:** Bucketing a continuous TTF distribution lets product answer "how fast do users convert" and spot drop-dead windows where momentum is lost.

## Q19: Bounce rate per landing page (sessions with exactly one pageview / all sessions).

Tables: `sessions(session_id, user_id, entry_url, started_at, ended_at)`, `events(event_id, session_id, event_type)`.

**Query:**
```sql
-- PostgreSQL
WITH pv AS (
  SELECT session_id, COUNT(*) AS pageviews
  FROM   events
  WHERE  event_type = 'page_view'
  GROUP  BY session_id
)
SELECT s.entry_url,
       COUNT(*) AS sessions,
       COUNT(*) FILTER (WHERE pv.pageviews = 1) AS bounced,
       ROUND(100.0 * COUNT(*) FILTER (WHERE pv.pageviews = 1) / COUNT(*), 1) AS bounce_rate_pct
FROM   sessions s
LEFT   JOIN pv ON pv.session_id = s.session_id
GROUP  BY s.entry_url
ORDER  BY bounce_rate_pct DESC;
```
**Explanation:** Bounce rate = sessions with a single pageview ÷ all sessions for each entry URL; high bounce signals a landing page that fails to engage.

**Alt1:**
```sql
-- MySQL 8+
SELECT s.entry_url,
       ROUND(100.0 * SUM(pv.pageviews = 1) / COUNT(*), 1) AS bounce_rate_pct
FROM   sessions s
LEFT   JOIN (SELECT session_id, COUNT(*) AS pageviews
             FROM   events WHERE event_type = 'page_view' GROUP BY session_id) pv
       ON pv.session_id = s.session_id
GROUP  BY s.entry_url;
```

## Q20: Conversion funnel — view → add-to-cart → checkout → purchase per day.

Tables: `events(event_id, user_id, event_time TIMESTAMP, event_type)`; event types in ('page_view','add_to_cart','begin_checkout','purchase').

**Query:**
```sql
-- PostgreSQL
SELECT event_time::date AS day,
       COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'page_view')      AS views,
       COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'add_to_cart')    AS carted,
       COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'begin_checkout') AS checked_out,
       COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'purchase')       AS purchased
FROM   events
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** Each step counts distinct users, so funnel drop-off is comparable across rows; absolute steps are the input, and step-to-step conversion is ratio of consecutive columns.

**Alt1:**
```sql
-- SQL Server
SELECT CAST(event_time AS date) AS day,
       COUNT(DISTINCT CASE WHEN event_type = 'page_view'      THEN user_id END) AS views,
       COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart'    THEN user_id END) AS carted,
       COUNT(DISTINCT CASE WHEN event_type = 'begin_checkout' THEN user_id END) AS checked_out,
       COUNT(DISTINCT CASE WHEN event_type = 'purchase'       THEN user_id END) AS purchased
FROM   events
GROUP  BY CAST(event_time AS date);
```

## Q21: Step-to-step funnel conversion percentages across the whole date range.

Tables: `events(event_id, user_id, event_time TIMESTAMP, event_type)`.

**Query:**
```sql
-- MySQL 8+
WITH steps AS (
  SELECT COUNT(DISTINCT user_id) AS views,
         COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart'    THEN user_id END) AS carted,
         COUNT(DISTINCT CASE WHEN event_type = 'begin_checkout' THEN user_id END) AS checked_out,
         COUNT(DISTINCT CASE WHEN event_type = 'purchase'       THEN user_id END) AS purchased
  FROM   events
),
prev AS (
  SELECT carted AS a, checked_out AS b, purchased AS c, views AS v FROM steps
)
SELECT 100.0 AS view_rate_pct,
       ROUND(100.0 * carted      / views, 1) AS view_to_cart_pct,
       ROUND(100.0 * checked_out / carted, 1) AS cart_to_checkout_pct,
       ROUND(100.0 * purchased   / checked_out, 1) AS checkout_to_purchase_pct,
       ROUND(100.0 * purchased   / views, 1) AS overall_pct
FROM   steps;
```
**Explanation:** Consecutive-step ratios (cart/views, checkout/carted, purchase/checkout) localize where the funnel bleeds; overall (purchase/views) is the end-to-end conversion.

## Q22: Revenue per user and average order value (AOV) per day.

Tables: `orders(order_id, user_id, created_at TIMESTAMP, total_amount DECIMAL)`, `order_items(order_id, product_id, quantity, unit_price)`.

**Query:**
```sql
-- PostgreSQL
SELECT created_at::date AS day,
       SUM(total_amount)                                            AS revenue,
       COUNT(DISTINCT order_id)                                     AS orders,
       COUNT(DISTINCT user_id)                                      AS buyers,
       ROUND(SUM(total_amount) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS aov
FROM   orders
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** AOV = revenue ÷ order count (distinct orders, not order lines); revenue ÷ buyers would instead be revenue-per-customer, a different metric.

## Q23: Basket size — average number of items (order lines) per order.

Tables: `order_items(order_id, product_id, quantity, unit_price)`.

**Query:**
```sql
-- MySQL 8+
SELECT ROUND(AVG(items), 2) AS avg_items_per_order
FROM   (
  SELECT order_id, SUM(quantity) AS items
  FROM   order_items
  GROUP  BY order_id
) t;
```
**Explanation:** Basket size averages `SUM(quantity)` across orders — items combines quantity, unlike a simple line count.

## Q24: Repeat purchase rate — buyers with >1 order as % of all buyers.

Tables: `orders(order_id, user_id, created_at TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL
WITH buyer_counts AS (
  SELECT user_id, COUNT(*) AS order_cnt
  FROM   orders
  GROUP  BY user_id
)
SELECT COUNT(*) AS total_buyers,
       COUNT(*) FILTER (WHERE order_cnt >= 2) AS repeat_buyers,
       ROUND(100.0 * COUNT(*) FILTER (WHERE order_cnt >= 2) / COUNT(*), 1) AS repeat_purchase_rate_pct
FROM   buyer_counts;
```
**Explanation:** Repeat purchase rate = customers with ≥2 orders ÷ total customers; it answers "is the product a one-time buy or a habit?"

**Alt1:**
```sql
-- SQL Server
SELECT ROUND(100.0 * COUNT(CASE WHEN order_cnt >= 2 THEN 1 END) / COUNT(*), 1) AS repeat_rate_pct
FROM   (SELECT user_id, COUNT(*) AS order_cnt FROM orders GROUP BY user_id) t;
```

## Q25: Daily new signups vs daily first-time buyers vs daily churned-first-time projections.

Tables: `users(user_id, signup_date)`, `orders(order_id, user_id, created_at)`, `cancellations(cancellation_id, user_id, cancelled_at)`.

**Query:**
```sql
-- PostgreSQL
WITH signups AS (
  SELECT signup_date::date AS d, COUNT(*) AS signups
  FROM   users GROUP BY 1
),
first_orders AS (
  SELECT MIN(created_at)::date AS d, COUNT(*) AS first_buyers
  FROM   orders GROUP BY 1
),
churned AS (
  SELECT cancelled_at::date AS d, COUNT(*) AS cancellations
  FROM   cancellations GROUP BY 1
)
SELECT COALESCE(s.d, f.d, c.d) AS day,
       COALESCE(s.signups, 0)       AS signups,
       COALESCE(f.first_buyers, 0)  AS first_buyers,
       COALESCE(c.cancellations, 0) AS cancellations
FROM   signups s
FULL   OUTER JOIN first_orders f ON f.d = s.d
FULL   OUTER JOIN churned      c ON c.d = f.d
ORDER  BY 1;
```
**Explanation:** A three-way FULL OUTER JOIN unions each metric on the same day axis so the funnel's top (signups), activation (first buy), and leak (cancellations) sit in one table.

## Q26: Hour-of-day activity distribution — which hours have the most events.

Tables: `events(event_id, user_id, event_time TIMESTAMP, event_type)`.

**Query:**
```sql
-- PostgreSQL
SELECT EXTRACT(HOUR FROM event_time)      AS hour_of_day
     , COUNT(*)                           AS events
     , COUNT(DISTINCT user_id)            AS distinct_users
FROM   events
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** Bucketing events into 24 hour slots shows peak usage windows; distinct_users guards against one crawler inflating an hour.

## Q27: Engagement by day-of-week AND hour — find the single busiest block.

Tables: `events(event_id, user_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- MySQL 8+
WITH blocks AS (
  SELECT DAYOFWEEK(event_time)                               AS dow
       , HOUR(event_time)                                    AS hr
       , COUNT(DISTINCT user_id)                             AS dau
  FROM   events
  GROUP  BY 1, 2
)
SELECT dow, hr, dau
     , RANK() OVER (ORDER BY dau DESC)                       AS rnk
FROM   blocks
ORDER  BY rnk;
```
**Explanation:** A day×hour grid ranked by actives identifies the single most crowded engagement block, the anchor for feature-flag rollouts and maintenance windows.

## Q28: Daily new signups vs daily churned users on one chart.

Tables: `users(user_id, signup_date DATE)`, `subscription_cancellations(cancellation_id, user_id, cancelled_at DATE)`.

**Query:**
```sql
-- PostgreSQL
WITH signups AS (
  SELECT signup_date AS day, COUNT(*) AS new_signups
  FROM   users GROUP BY 1
),
losses AS (
  SELECT cancelled_at AS day, COUNT(*) AS churned_users
  FROM   subscription_cancellations GROUP BY 1
)
SELECT COALESCE(s.day, l.day) AS day,
       COALESCE(s.new_signups, 0) AS new_signups,
       COALESCE(l.churned_users, 0) AS churned_users,
       COALESCE(s.new_signups, 0) - COALESCE(l.churned_users, 0) AS net_added
FROM   signups s
FULL   OUTER JOIN losses l ON l.day = s.day
ORDER  BY 1;
```
**Explanation:** Stacking gross additions against gross losses yields net growth per day; when the line crosses zero the business has a leak that signups no longer cover.

## Q29: Monthly churn rate from a subscription table.

Tables: `subscriptions(subscription_id, user_id, plan, started_at DATE, ended_at DATE)`; a row's `ended_at` is NULL while active, set on cancellation.

**Query:**
```sql
-- PostgreSQL
WITH months AS (
  SELECT generate_series('2024-01-01'::date, '2024-12-01'::date, '1 month') AS m
)
SELECT to_char(m.m, 'YYYY-MM') AS month,
       COUNT(DISTINCT s.subscription_id)                                AS churned,
       COUNT(DISTINCT a.subscription_id)                                AS active_at_start,
       ROUND(100.0 * COUNT(DISTINCT s.subscription_id)
             / NULLIF(COUNT(DISTINCT a.subscription_id), 0), 2)         AS churn_rate_pct
FROM   months m
LEFT   JOIN subscriptions a
       ON  a.started_at < (m.m + INTERVAL '1 month')
       AND (a.ended_at IS NULL OR a.ended_at >= m.m)
LEFT   JOIN subscriptions s
       ON  s.started_at < (m.m + INTERVAL '1 month')
       AND s.ended_at >= m.m
       AND s.ended_at <  (m.m + INTERVAL '1 month')
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** Churn rate = subscriptions terminated in the month ÷ subscriptions active at the month's start; the join boundary conditions (`started_at` before month end, `ended_at` inside the month) define both numerator and denominator precisely.

## Q30: Reactivation rate — churned users who resubscribed later.

Tables: `subscriptions(subscription_id, user_id, plan, started_at DATE, ended_at DATE)`.

**Query:**
```sql
-- SQL Server
;WITH churns AS (
  SELECT user_id, ended_at, started_at
  FROM   subscriptions
  WHERE  ended_at IS NOT NULL
)
SELECT YEAR(ch.ended_at) AS churn_year,
       MONTH(ch.ended_at) AS churn_month,
       COUNT(DISTINCT ch.user_id) AS total_churned,
       COUNT(DISTINCT nxt.user_id) AS reactivated,
       ROUND(100.0 * COUNT(DISTINCT nxt.user_id) / NULLIF(COUNT(DISTINCT ch.user_id), 0), 2) AS reactivation_rate_pct
FROM   churns ch
LEFT   JOIN subscriptions nxt
       ON  nxt.user_id = ch.user_id
       AND nxt.started_at > ch.ended_at
       AND nxt.started_at <= DATEADD(DAY, 90, ch.ended_at)
GROUP  BY YEAR(ch.ended_at), MONTH(ch.ended_at);
```
**Explanation:** Reactivation counts a separate subscription starting after the churn endpoint (window 90d); the metric tells you whether churn is permanent or a break users come back from.

## Q31: Gross revenue retention (GRR) vs net revenue retention (NRR).

Tables: `subscriptions(subscription_id, user_id, plan_start DATE, plan_end DATE, mrr DECIMAL)`.

**Query:**
```sql
-- PostgreSQL
WITH mrr_at_start AS (
  SELECT '2024-01-01'::date AS start_dt
       , SUM(mrr) AS starting_mrr
  FROM   subscriptions
  WHERE  plan_start < '2024-02-01'::date
     AND (plan_end IS NULL OR plan_end >= '2024-01-01'::date)
),
mrr_now AS (
  SELECT COUNT(*) AS survivors
       , COALESCE(SUM(mrr), 0) AS surviving_mrr
  FROM   subscriptions
  WHERE  plan_start < '2024-02-01'::date
     AND (plan_end IS NULL OR plan_end >= '2024-02-01'::date)
)
SELECT ROUND(100.0 * surviving_mrr / starting_mrr, 2) AS grr_pct,
       surviving_mrr
FROM   mrr_at_start, mrr_now;
```
**Explanation:** GRR keeps only surviving customers' MRR (drops cap at 100%); NRR adds expansion back on top. Computing NRR requires expansion tables, covered later.

**Alt1:**
```sql
-- NRR needs upsell events; compute against a price-movement log
SELECT ROUND(100.0 * SUM(CURRENT_MRR) / NULLIF((SELECT SUM(mrr) FROM mrr_at_start), 0), 2)
FROM   price_movements;
```

## Q32: Feature adoption % — share of active users who used a given feature.

Tables: `feature_events(feature_id, user_id, event_time)`, `events(event_id, user_id, event_time)`.

**Query:**
```sql
-- MySQL 8+
SELECT DATE(fe.event_time) AS day,
       COUNT(DISTINCT fe.user_id)                     AS feature_users,
       COUNT(DISTINCT e.user_id)                      AS active_users,
       ROUND(100.0 * COUNT(DISTINCT fe.user_id)
             / NULLIF(COUNT(DISTINCT e.user_id), 0), 1) AS adoption_pct
FROM   events e
LEFT   JOIN feature_events fe
       ON  fe.user_id = e.user_id
       AND DATE(fe.event_time) = DATE(e.event_time)
       AND fe.feature_id = 'dark_mode'
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** Adoption = distinct users touching the feature ÷ all distinct active users the same day; LEFT JOIN preserves the full denominator.

## Q33: Cumulative feature adoption over time per signup cohort.

Tables: `users(user_id, signup_date DATE)`, `feature_events(user_id, feature_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- Oracle
WITH feat AS (
  SELECT DISTINCT user_id, TRUNC(event_time, 'MM') AS use_month
  FROM   feature_events
  WHERE  feature_id = 'reports'
)
SELECT SUBSTR(TO_CHAR(u.signup_date, 'YYYY-MM'), 1, 7)                       AS cohort
     , COUNT(DISTINCT u.user_id)                                             AS cohort_size
     , COUNT(DISTINCT CASE WHEN F.use_month <= ADD_MONTHS(TRUNC(u.signup_date, 'MM'), 0) THEN u.user_id END) AS adopted_m0
     , COUNT(DISTINCT CASE WHEN F.use_month <= ADD_MONTHS(TRUNC(u.signup_date, 'MM'), 1) THEN u.user_id END) AS adopted_m1
     , COUNT(DISTINCT CASE WHEN F.use_month <= ADD_MONTHS(TRUNC(u.signup_date, 'MM'), 3) THEN u.user_id END) AS adopted_m3
FROM   users u
LEFT   JOIN feat F ON F.user_id = u.user_id
GROUP  BY SUBSTR(TO_CHAR(u.signup_date, 'YYYY-MM'), 1, 7)
ORDER  BY 1;
```
**Explanation:** Each column is the cumulative count of cohort users who adopted the feature by month 0/1/3 since signup; dividing by cohort_size gives the adoption curve's speed per vintage, not just its ceiling.

## Q34: Sessionize events and compute average session length.

Tables: `sessions(session_id, user_id, started_at TIMESTAMP, ended_at TIMESTAMP, device)`.

**Query:**
```sql
-- PostgreSQL
SELECT device,
       AVG(EXTRACT(EPOCH FROM (ended_at - started_at)) / 60.0)          AS avg_session_min
     , PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (ended_at - started_at)) / 60.0) AS median_session_min
FROM   sessions
GROUP  BY device
ORDER  BY avg_session_min DESC;
```
**Explanation:** Session length is `ended_at − started_at` per session; averaging in minutes gives mean, percentile gives median, and splitting by device surfaces hardware differences.

**Alt1:**
```sql
-- Without a sessions table, reconstruct: gap > 30 min = new session
WITH marked AS (
  SELECT user_id, event_time,
         CASE WHEN event_time - LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time) > INTERVAL '30 minutes'
              THEN 1 ELSE 0 END AS new_session
  FROM   events
)
SELECT COUNT(*) FILTER (WHERE new_session = 1) + COUNT(DISTINCT user_id) AS estimated_sessions
FROM   marked;
```
**Explanation:** Each gap marker starts a new session, and per user the very first event is one extra session — so `SUM(new markers) + distinct users` is the sessionization estimate from raw events.

## Q35: Session count per user distribution (histogram).

Tables: `sessions(session_id, user_id, started_at)`.

**Query:**
```sql
-- PostgreSQL
WITH per_user AS (
  SELECT user_id, COUNT(*) AS session_cnt
  FROM   sessions
  WHERE  started_at >= CURRENT_DATE - 30
  GROUP  BY user_id
)
SELECT session_cnt, COUNT(*) AS users
FROM   per_user
GROUP  BY session_cnt
ORDER  BY session_cnt;
```
**Explanation:** Counting users at each session-count level builds a power-law histogram; the long tail of heavy users is where monetization ROI concentrates.

## Q36: Average sessions per active user per day.

Tables: `sessions(session_id, user_id, started_at TIMESTAMP)`.

**Query:**
```sql
-- MySQL 8+
SELECT DATE(started_at) AS day,
       COUNT(*) / NULLIF(COUNT(DISTINCT user_id), 0) AS sessions_per_active_user
FROM   sessions
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** Sessions ÷ distinct users is the daily frequency measure; >1 means users average multiple sessions, a stickiness lever above DAU.

## Q37: LTV approximation — ARPU × average active lifetime.

Tables: `users(user_id, signup_date)`, `orders(order_id, user_id, created_at, total_amount)`, `sessions(session_id, user_id, started_at)`.

**Query:**
```sql
-- PostgreSQL
WITH arpu AS (
  SELECT COALESCE(SUM(o.total_amount) / NULLIF(COUNT(DISTINCT u.user_id), 0), 0) AS avg_revenue_per_user
  FROM   users u
  LEFT   JOIN orders o ON o.user_id = u.user_id
),
life AS (
  SELECT AVG(EXTRACT(EPOCH FROM (last_seen - signup_date)) / 86400.0 / 30.44) AS avg_lifetime_months
  FROM   (
    SELECT u.user_id, u.signup_date, MAX(s.started_at) AS last_seen
    FROM   users u
    LEFT   JOIN sessions s ON s.user_id = u.user_id
    GROUP  BY u.user_id, u.signup_date
  ) t
  WHERE  last_seen IS NOT NULL
)
SELECT ROUND(a.avg_revenue_per_user * l.avg_lifetime_months, 2) AS ltv_estimate
FROM   arpu a, life l;
```
**Explanation:** LTV approximation = ARPU × average lifetime (last event minus signup, in months); cheap and directionally correct for cohorts, though it ignores discounting and future revenue.

**Alt1:**
```sql
-- Cohort-based LTV is more stable
WITH c AS (
  SELECT date_trunc('month', signup_date) AS cohort
       , COUNT(DISTINCT u.user_id) AS users
       , COALESCE(SUM(o.total_amount), 0) AS revenue
  FROM   users u LEFT JOIN orders o ON o.user_id = u.user_id
  GROUP  BY 1
)
SELECT cohort, revenue / users AS ltv_per_user FROM c ORDER BY cohort;
```

## Q38: CAC proxy — marketing spend divided by new customers acquired.

Tables: `marketing_spend(date, channel, spend)`, `customers(user_id, acquired_at)`.

**Query:**
```sql
-- SQL Server
SELECT MONTH(m.spend_date) AS spend_month,
       SUM(m.spend)                                                        AS spend,
       COUNT(DISTINCT c.user_id)                                           AS new_customers,
       ROUND(SUM(m.spend) / NULLIF(COUNT(DISTINCT c.user_id), 0), 2)       AS cac
FROM   marketing_spend m
LEFT   JOIN customers c
       ON  YEAR(c.acquired_at) = YEAR(m.spend_date)
       AND MONTH(c.acquired_at) = MONTH(m.spend_date)
GROUP  BY MONTH(m.spend_date), YEAR(m.spend_date)
ORDER  BY YEAR(m.spend_date), MONTH(m.spend_date);
```
**Explanation:** CAC proxy = total marketing spend ÷ new customers in the same month; a coin-month lag join makes it tractable when attribution is unavailable.

## Q39: Refund rate — refunded order value as a % of total order value.

Tables: `orders(order_id, user_id, created_at, total_amount)`, `refunds(refund_id, order_id, amount, refunded_at)`.

**Query:**
```sql
-- PostgreSQL
SELECT to_char(date_trunc('month', o.created_at), 'YYYY-MM') AS month,
       COUNT(DISTINCT o.order_id)                                    AS orders,
       COUNT(DISTINCT r.order_id)                                   AS refunded_orders,
       ROUND(100.0 * COUNT(DISTINCT r.order_id) / COUNT(DISTINCT o.order_id), 2)       AS order_refund_rate_pct,
       ROUND(100.0 * COALESCE(SUM(r.amount), 0) / NULLIF(SUM(o.total_amount), 0), 2)    AS value_refund_rate_pct
FROM   orders o
LEFT   JOIN refunds r ON r.order_id = o.order_id
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** Two flavors: order-level refund rate (share of orders refunded) and value-level (refunded dollars ÷ gross dollars); the latter is the true revenue leak.

## Q40: NPS-style score buckets (promoters/passives/detractors) from a surveys table.

Tables: `surveys(survey_id, user_id, score INT, submitted_at)`; score scale 0–10: 9–10 promoter, 7–8 passive, 0–6 detractor.

**Query:**
```sql
-- MySQL 8+
SELECT DATE_FORMAT(submitted_at, '%Y-%m')                                      AS month,
       SUM(score BETWEEN 9 AND 10)                                             AS promoters,
       SUM(score BETWEEN 7 AND 8)                                              AS passives,
       SUM(score BETWEEN 0 AND 6)                                              AS detractors,
       ROUND(100.0 * (SUM(score BETWEEN 9 AND 10) - SUM(score BETWEEN 0 AND 6))
             / COUNT(*), 2)                                                    AS nps
FROM   surveys
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** NPS = (promoters − detractors) ÷ responses × 100; the boolean SUM trick buckets in one pass.

**Alt1:**
```sql
-- PostgreSQL FILTER clause
SELECT date_trunc('month', submitted_at) AS month,
       ROUND(100.0 * (COUNT(*) FILTER (WHERE score BETWEEN 9 AND 10)
                     - COUNT(*) FILTER (WHERE score BETWEEN 0 AND 6))
             / COUNT(*), 2) AS nps
FROM   surveys
GROUP  BY 1
ORDER  BY 1;
```

## Q41: Pageview heat — event counts per URL, ranked.

Tables: `events(event_id, user_id, event_time, event_type, url)`.

**Query:**
```sql
-- SQL Server
SELECT Top 20
       url,
       COUNT(*)                                                AS pageviews,
       COUNT(DISTINCT user_id)                                 AS viewers,
       AVG(DATEDIFF(SECOND, event_time, LEAD(event_time) OVER (PARTITION BY session_id ORDER BY event_time))) AS avg_dwell_sec
FROM   events
WHERE  event_type = 'page_view'
GROUP  BY url
ORDER  BY pageviews DESC;
```
**Explanation:** Ranked counts per URL identify the hottest surfaces; dwell-time derived from the next event approximates attention, not just views.

## Q42: 3-sigma spike detection — a day's DAU far above its 30-day rolling baseline.

Tables: `events(event_id, user_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL
WITH daily AS (
  SELECT event_time::date AS day, COUNT(DISTINCT user_id) AS dau
  FROM   events GROUP BY 1
),
stats AS (
  SELECT day, dau,
         AVG(dau)  OVER (ORDER BY day ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING) AS mean_prior,
         STDDEV(dau) OVER (ORDER BY day ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING) AS sd_prior
  FROM   daily
)
SELECT day, dau,
       ROUND(mean_prior, 1) AS baseline,
       ROUND((dau - mean_prior) / NULLIF(sd_prior, 0), 2) AS z_score
FROM   stats
WHERE  sd_prior IS NOT NULL
  AND  (dau - mean_prior) / NULLIF(sd_prior, 0) > 3
ORDER  BY z_score DESC;
```
**Explanation:** Each day's DAU is compared against the mean/std of the 30 preceding days; days exceeding +3σ are flagged as anomalies worth investigating (launch? outage of a competitor? bot wave?).

## Q43: Week-over-week growth — this week's MAU vs last week's MAU.

Tables: `events(event_id, user_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL
WITH wau AS (
  SELECT date_trunc('week', event_time)          AS wk
       , COUNT(DISTINCT user_id)                 AS wau
  FROM   events
  GROUP  BY 1
)
SELECT wk
     , wau
     , LAG(wau) OVER (ORDER BY wk)                              AS prev_wau
     , ROUND(100.0 * (wau - LAG(wau) OVER (ORDER BY wk)) / NULLIF(LAG(wau) OVER (ORDER BY wk), 0), 2) AS wow_growth_pct
FROM   wau
ORDER  BY wk;
```
**Explanation:** WoW = (current WAU − prior WAU) / prior WAU; same LAG pattern as DoD/MoM, applied at the week granularity.

## Q44: Year-over-year growth — each month vs the same month last year.

Tables: `events(event_id, user_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- MySQL 8+
WITH mau AS (
  SELECT DATE_FORMAT(event_time, '%Y-%m-01') AS month
       , COUNT(DISTINCT user_id) AS mau
  FROM   events
  GROUP  BY 1
)
SELECT a.month
     , a.mau
     , b.mau AS yoy_prev
     , ROUND(100.0 * (a.mau - b.mau) / NULLIF(b.mau, 0), 2) AS yoy_growth_pct
FROM   mau a
LEFT   JOIN mau b ON b.month = DATE_SUB(a.month, INTERVAL 1 YEAR)
ORDER  BY a.month;
```
**Explanation:** YoY joins each month to its counterpart 12 months earlier, canceling seasonality like holiday spikes and summer drops.

## Q45: Cohort revenue curves — total revenue generated in each month since signup.

Tables: `users(user_id, signup_date)`, `orders(order_id, user_id, created_at, total_amount)`.

**Query:**
```sql
-- PostgreSQL
WITH birth AS (
  SELECT user_id, date_trunc('month', signup_date) AS cohort FROM users
),
rev AS (
  SELECT o.user_id,
         date_trunc('month', o.created_at) AS order_month,
         SUM(o.total_amount)               AS rev
  FROM   orders o GROUP  BY 1, 2
)
SELECT b.cohort
     , COUNT(DISTINCT b.user_id) AS cohort_size
     , SUM(CASE WHEN r.order_month = b.cohort THEN r.rev END)                                                              AS m0_rev
     , SUM(CASE WHEN r.order_month = b.cohort + INTERVAL '1 month' THEN r.rev END)                                          AS m1_rev
     , SUM(CASE WHEN r.order_month = b.cohort + INTERVAL '3 months' THEN r.rev END)                                         AS m3_rev
     , ROUND(SUM(CASE WHEN r.order_month = b.cohort THEN r.rev END) * 1.0 / COUNT(DISTINCT b.user_id), 2)                  AS rev_per_user_m0
FROM   birth b
LEFT   JOIN rev r ON r.user_id = b.user_id AND r.order_month >= b.cohort
GROUP  BY b.cohort
ORDER  BY b.cohort;
```
**Explanation:** Each cohort row is a column of revenue at fixed month-offsets since join (m0, m1, m3); dividing by cohort_size produces revenue-per-user curves that are comparable across vintages.

## Q46: Median revenue per user.

Tables: `orders(order_id, user_id, total_amount)`.

**Query:**
```sql
-- PostgreSQL: user-level revenue, then a true median across those totals
WITH per_user AS (
  SELECT user_id, SUM(total_amount) AS user_total
  FROM   orders
  GROUP  BY user_id
)
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY user_total) AS median_user_revenue,
       ROUND(AVG(user_total), 2)                          AS mean_user_revenue,
       COUNT(*)                                           AS paying_users
FROM   per_user;
```
**Explanation:** `PERCENTILE_CONT(0.5)` is the continuous median across the per-user revenue distribution, robust to a few whales skewing the mean; the mean alongside it exposes the gap.

**Alt1:**
```sql
-- SQL Server / PostgreSQL: median of per-user revenue in one pass
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY user_rev) AS median_rev
FROM   (SELECT SUM(total_amount) AS user_rev FROM orders GROUP BY user_id) t;
```

## Q47: Top-paying users segment — top decile of customers and their revenue share.

Tables: `orders(order_id, user_id, created_at, total_amount)`.

**Query:**
```sql
-- MySQL 8+
WITH per_user AS (
  SELECT user_id, SUM(total_amount) AS rev
  FROM   orders GROUP BY user_id
),
ranked AS (
  SELECT user_id, rev,
         NTILE(10) OVER (ORDER BY rev DESC) AS decile
  FROM   per_user
)
SELECT decile,
       COUNT(*)                                        AS users,
       SUM(rev)                                        AS revenue,
       ROUND(100.0 * SUM(rev) / SUM(SUM(rev)) OVER (), 2) AS share_pct
FROM   ranked
GROUP  BY decile
ORDER  BY decile;
```
**Explanation:** `NTILE(10)` cuts customers into deciles by revenue; decile 1 is the top 10% and its `share_pct` quantifies whale-concentration risk.

## Q48: Cohort table pivot — retention from a pre-aggregated cohort table.

Tables: `cohort_rollup(cohort_month DATE, month_offset INT, users INT, revenue DECIMAL)`.

**Query:**
```sql
-- PostgreSQL (offset → column pivot)
SELECT cohort_month,
       MAX(CASE WHEN month_offset = 0 THEN users END) AS m0_users,
       MAX(CASE WHEN month_offset = 1 THEN users END) AS m1_users,
       MAX(CASE WHEN month_offset = 2 THEN users END) AS m2_users,
       MAX(CASE WHEN month_offset = 3 THEN users END) AS m3_users
FROM   cohort_rollup
GROUP  BY cohort_month
ORDER  BY cohort_month;
```
**Explanation:** When a warehouse pre-aggregates cohorts into a `(cohort, offset)` long table, a conditional MAX pivot reproduces the classic matrix without touching raw events.

**Alt1:**
```sql
-- Long-form retention is chart-ready without pivoting
SELECT cohort_month, month_offset,
       ROUND(100.0 * users / MAX(users) FILTER (WHERE month_offset = 0) OVER (PARTITION BY cohort_month), 1) AS retention_pct
FROM   cohort_rollup
ORDER  BY cohort_month, month_offset;
```

## Q49: Onboarding funnel — users who reach each activation step.

Tables: `user_flow_events(user_id, step, step_ts)`, `users(user_id, signup_date)`; steps: install → signup → profile → first_content → watchlisted.

**Query:**
```sql
-- PostgreSQL
WITH base AS (
  SELECT u.user_id
       , MAX(CASE WHEN f.step = 'install'      THEN 1 END) AS s_install
       , MAX(CASE WHEN f.step = 'signup'       THEN 1 END) AS s_signup
       , MAX(CASE WHEN f.step = 'profile'      THEN 1 END) AS s_profile
       , MAX(CASE WHEN f.step = 'first_content' THEN 1 END) AS s_content
       , MAX(CASE WHEN f.step = 'watchlisted'  THEN 1 END) AS s_watchlist
  FROM   users u
  LEFT   JOIN user_flow_events f ON f.user_id = u.user_id
  GROUP  BY u.user_id
)
SELECT COUNT(*) AS signed_up
     , SUM(s_profile)                            AS reached_profile
     , SUM(s_content)                            AS created_first_content
     , SUM(s_watchlist)                          AS used_watchlist
     , ROUND(100.0 * SUM(s_watchlist) / COUNT(*), 1) AS end_to_end_pct
FROM   base;
```
**Explanation:** Pivoting per-user "ever reached step" flags then summing gives the cumulative staircase that shows where activation leaks, independent of row order.

## Q50: Daily revenue by acquisition channel.

Tables: `users(user_id, signup_date, channel)`, `orders(order_id, user_id, created_at, total_amount)`.

**Query:**
```sql
-- MySQL 8+
SELECT DATE(o.created_at)            AS day
     , u.channel                     AS channel
     , SUM(o.total_amount)           AS revenue
FROM   orders o
JOIN   users u ON u.user_id = o.user_id
GROUP  BY 1, 2
ORDER  BY 1, 2;
```
**Explanation:** Revenue credited to a user's signup channel; the JOIN carries `channel` alongside every order so GROUP BY channel totals cleanly.

## Q51: Time-series fill — backfill missing days with zero DAU.

Tables: `events(event_id, user_id, event_time TIMESTAMP)` covering only active days.

**Query:**
```sql
-- PostgreSQL
WITH days AS (
  SELECT generate_series(MIN(start_dt), MAX(end_dt), INTERVAL '1 day')::date AS day
  FROM   (SELECT MIN(event_time)::date AS start_dt, MAX(event_time)::date AS end_dt FROM events) r
),
dau AS (
  SELECT event_time::date AS day, COUNT(DISTINCT user_id) AS dau FROM events GROUP BY 1
)
SELECT d.day, COALESCE(x.dau, 0) AS dau
FROM   days d
LEFT   JOIN dau x ON x.day = d.day
ORDER  BY d.day;
```
**Explanation:** `generate_series` materializes every calendar day, and LEFT JOIN + COALESCE turns gaps into explicit zeros so the chart line is continuous.

**Alt1:**
```sql
-- MySQL 8+ without generate_series: recursive CTE builds the day list
WITH RECURSIVE days AS (
  SELECT MIN(DATE(event_time)) AS day FROM events
  UNION ALL
  SELECT day + INTERVAL 1 DAY FROM days
  WHERE  day < (SELECT MAX(DATE(event_time)) FROM events)
),
dau AS (
  SELECT DATE(event_time) AS day, COUNT(DISTINCT user_id) AS dau FROM events GROUP BY 1
)
SELECT d.day, COALESCE(x.dau, 0) AS dau
FROM   days d
LEFT   JOIN dau x ON x.day = d.day
ORDER  BY d.day;
```
**Explanation:** MySQL emulates the series with a recursive CTE: anchor = first event day, recursion = `day + INTERVAL 1 DAY`, terminator = `<= last event day`; a LEFT JOIN then fills every blank day with a zero DAU.

## Q52: 30/60/90-day milestones — % of each cohort still active at each age.

Tables: `users(user_id, signup_date)`, `sessions(session_id, user_id, started_at)`.

**Query:**
```sql
-- PostgreSQL
WITH birth AS (
  SELECT user_id, signup_date::date FROM users
),
seen AS (
  SELECT DISTINCT user_id, started_at::date AS day FROM sessions
)
SELECT date_trunc('month', b.signup_date) AS cohort,
       COUNT(DISTINCT b.user_id) AS cohort_size,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN s.day > b.signup_date AND s.day <= b.signup_date + 30 THEN b.user_id ELSE NULL END) / COUNT(DISTINCT b.user_id), 1) AS active_d30_pct,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN s.day > b.signup_date AND s.day <= b.signup_date + 60 THEN b.user_id ELSE NULL END) / COUNT(DISTINCT b.user_id), 1) AS active_d60_pct,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN s.day > b.signup_date AND s.day <= b.signup_date + 90 THEN b.user_id ELSE NULL END) / COUNT(DISTINCT b.user_id), 1) AS active_d90_pct
FROM   birth b
LEFT   JOIN seen s ON s.user_id = b.user_id
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** Each column is a cumulative "active at least once by day N" window; the D30→D60→D90 decay curve per cohort is the milestone view of churn.

**Alt1:**
```sql
-- Oracle
SELECT TO_CHAR(TRUNC(u.signup_date, 'MM'), 'YYYY-MM')                    AS cohort,
       COUNT(DISTINCT u.user_id)                                         AS cohort_size,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN s.day > u.signup_date
                                         AND  s.day <= u.signup_date + 30 THEN u.user_id END)
             / COUNT(DISTINCT u.user_id), 1)                             AS active_d30_pct,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN s.day > u.signup_date
                                         AND  s.day <= u.signup_date + 90 THEN u.user_id END)
             / COUNT(DISTINCT u.user_id), 1)                             AS active_d90_pct
FROM   users u
LEFT   JOIN (SELECT DISTINCT user_id, TRUNC(started_at) AS day FROM sessions) s
       ON s.user_id = u.user_id
GROUP  BY TO_CHAR(TRUNC(u.signup_date, 'MM'), 'YYYY-MM')
ORDER  BY 1;
```
**Explanation:** Oracle uses `TRUNC(date, 'MM')` to bucket months and `date + 30` for day arithmetic; the milestone windows (`signup_date + 30/90`) define the retention ladder with no special interval syntax needed.

## Q53: Expansion revenue — MRR gained from upgrades and add-ons by month.

Tables: `plan_changes(change_id, subscription_id, user_id, plan, plan_start, new_mrr, old_mrr)`.

**Query:**
```sql
-- PostgreSQL
SELECT to_char(date_trunc('month', plan_start), 'YYYY-MM') AS month,
       COUNT(*)                                       AS changes,
       SUM(CASE WHEN new_mrr > old_mrr THEN new_mrr - old_mrr ELSE 0 END) AS expansion_mrr,
       SUM(CASE WHEN new_mrr < old_mrr THEN new_mrr - old_mrr ELSE 0 END) AS contraction_mrr
FROM   plan_changes
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** Expansion = positive MRR deltas from plan moves (upgrades/add-ons); the negative deltas go to contraction. The two sums are the guts of an NRR bridge.

## Q54: Contraction vs churn — MRR lost to downgrades vs cancelled subscriptions.

Tables: `plan_changes(change_id, user_id, plan_start, new_mrr, old_mrr)`, `subscriptions(subscription_id, user_id, plan_end, mrr)`.

**Query:**
```sql
-- SQL Server
SELECT YEAR(change_month) AS yr, MONTH(change_month) AS mo,
       SUM(contraction) AS contraction_mrr,
       SUM(churn)       AS churn_mrr
FROM (
  SELECT plan_start AS change_month,
         CASE WHEN new_mrr < old_mrr THEN old_mrr - new_mrr ELSE 0 END AS contraction,
         0 AS churn
  FROM   plan_changes
  UNION ALL
  SELECT plan_end,
         0 AS contraction,
         mrr AS churn
  FROM   subscriptions
  WHERE  plan_end IS NOT NULL
) t
GROUP  BY YEAR(change_month), MONTH(change_month);
```
**Explanation:** Downgrades shrink a still-captive account (contraction), cancellations remove it entirely (churn); a UNION ALL stack of both deltas builds a single MRR-loss ledger.

## Q55: S2S payment declines — decline rate and top decline reason per day.

Tables: `payment_events(event_id, order_id, user_id, event_time, event_type, decline_reason)`; event_type in ('auth_attempt','decline','authorization').

**Query:**
```sql
-- MySQL 8+
SELECT DATE(event_time) AS day,
       COUNT(*)                                  AS attempts,
       SUM(event_type = 'decline')               AS declines,
       ROUND(100.0 * SUM(event_type = 'decline')
             / NULLIF(COUNT(*), 0), 2)           AS decline_rate_pct
FROM   payment_events
WHERE  event_type IN ('auth_attempt', 'decline')
GROUP  BY DATE(event_time)
ORDER  BY 1;
```
**Explanation:** Decline rate = declines ÷ auth attempts per day; the denominator is scoped to attempts + declines so it cannot be inflated by unrelated payment-event types.

**Alt1:**
```sql
-- PostgreSQL: rank decline reasons per day and keep top-3 in one row
WITH d AS (
  SELECT DATE(event_time) AS day, COUNT(*) AS attempts,
         SUM(CASE WHEN event_type = 'decline' THEN 1 ELSE 0 END) AS declines
  FROM   payment_events GROUP BY 1
),
reasons AS (
  SELECT DATE(event_time) AS day, decline_reason, COUNT(*) AS cnt,
         ROW_NUMBER() OVER (PARTITION BY DATE(event_time) ORDER BY COUNT(*) DESC) AS rnk
  FROM   payment_events
  WHERE  event_type = 'decline'
  GROUP  BY 1, 2
)
SELECT d.day, d.attempts, d.declines,
       ROUND(100.0 * d.declines / NULLIF(d.attempts, 0), 2) AS decline_rate_pct,
       MAX(CASE WHEN r.rnk = 1 THEN r.decline_reason END) AS reason_1,
       MAX(CASE WHEN r.rnk = 2 THEN r.decline_reason END) AS reason_2
FROM   d
LEFT   JOIN reasons r ON r.day = d.day
GROUP  BY d.day, d.attempts, d.declines
ORDER  BY d.day;
```

## Q56: Anomaly — users with a signup-to-first-order span under one second (data bug or fraud).

Tables: `users(user_id, signup_date TIMESTAMP)`, `orders(order_id, user_id, created_at TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL
WITH fo AS (
  SELECT user_id, MIN(created_at) AS first_order_ts
  FROM   orders GROUP BY 1
)
SELECT u.user_id, u.signup_date, fo.first_order_ts,
       (fo.first_order_ts - u.signup_date) AS elapsed,
       EXTRACT(EPOCH FROM (fo.first_order_ts - u.signup_date)) AS elapsed_seconds
FROM   users u
JOIN   fo ON fo.user_id = u.user_id
WHERE  fo.first_order_ts < u.signup_date + INTERVAL '1 second'
ORDER  BY elapsed_seconds;
```
**Explanation:** A real human cannot register and complete checkout in under a second; sub-second spans flag test accounts, seeded data, or timestamp tz-conversion bugs.

**Alt1:**
```sql
-- Same idea but flag "impossibly early": order before signup (clock skew)
SELECT u.user_id, u.signup_date, MIN(o.created_at) AS first_order,
       (MIN(o.created_at) < u.signup_date) AS ordered_before_signup
FROM   users u JOIN orders o ON o.user_id = u.user_id
GROUP  BY u.user_id, u.signup_date
HAVING MIN(o.created_at) < u.signup_date - INTERVAL '1 day';
```

## Q57: Payment-fraud velocity — users with many declined attempts in a short window.

Tables: `payment_events(event_id, card_id, user_id, event_time, event_type)`.

**Query:**
```sql
-- MySQL 8+
WITH decl AS (
  SELECT user_id,
         COUNT(*) AS decline_count,
         COUNT(DISTINCT card_id) AS cards_used,
         TIMESTAMPDIFF(MINUTE, MIN(event_time), MAX(event_time)) AS minutes_span
  FROM   payment_events
  WHERE  event_type = 'decline'
  GROUP  BY user_id
)
SELECT user_id, decline_count, cards_used, minutes_span
FROM   decl
WHERE  decline_count >= 5
  AND  minutes_span <= 60
ORDER  BY decline_count DESC;
```
**Explanation:** Rule-based fraud score: ≥5 declines across multiple cards inside 60 minutes is implausible human behavior and matches card-testing patterns.

## Q58: Referrals count distribution — how many invites each user sends.

Tables: `referrals(inviter_id, invitee_id, invited_at)`.

**Query:**
```sql
-- SQL Server
SELECT inv_count, COUNT(DISTINCT inviter_id) AS inviters
FROM   (SELECT inviter_id, COUNT(*) AS inv_count
        FROM   referrals
        GROUP  BY inviter_id) t
GROUP  BY inv_count
ORDER  BY inv_count;
```
**Explanation:** A count-on-count histogram of invites-per-inviter; heavy right tails indicate a super-spreader cohort worth a dedicated growth loop.

## Q59: Referral funnel — invites sent, invites accepted, and accepted-referral signups.

Tables: `referrals(inviter_id, invitee_id, invited_at, accepted_at)`, `users(user_id, signup_date)`.

**Query:**
```sql
-- PostgreSQL
SELECT COUNT(*)                                          AS invites_sent,
       COUNT(accepted_at)                                AS invites_accepted,
       ROUND(100.0 * COUNT(accepted_at) / COUNT(*), 1)   AS acceptance_pct,
       COUNT(u.user_id)                                  AS invited_signups,
       ROUND(100.0 * COUNT(u.user_id) / COUNT(*), 1)     AS end_to_end_pct
FROM   referrals r
LEFT   JOIN users u ON u.user_id = r.invitee_id AND u.signup_date <= r.accepted_at;
```
**Explanation:** Each stage counts a different obligation: sent rows, accepted rows, and invitees who are now real users; ratios localize where viral loops break.

## Q60: Users active on all 7 days of the week (ultra-sticky cohort).

Tables: `events(event_id, user_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL
WITH wk AS (
  SELECT user_id,
         date_trunc('week', event_time) AS wk,
         COUNT(DISTINCT event_time::date) AS active_days
  FROM   events
  GROUP  BY 1, 2
)
SELECT wk,
       COUNT(DISTINCT user_id) AS daily_any_active,
       COUNT(DISTINCT CASE WHEN active_days = 7 THEN user_id END) AS active_all_7,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN active_days = 7 THEN user_id END) / NULLIF(COUNT(DISTINCT user_id), 0), 2) AS ultra_sticky_pct
FROM   wk
GROUP  BY wk
ORDER  BY wk;
```
**Explanation:** Counting distinct active days within each week and thresholding at 7 identifies the habit-forming core that drives retention benchmarks.

## Q61: WAU/MAU overlap — weekly actives who are also monthly actives.

Tables: `events(event_id, user_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- MySQL 8+
SELECT DATE_FORMAT(event_time, '%Y-%m') AS month,
       COUNT(DISTINCT CASE WHEN event_time >= DATE_SUB(DATE_ADD(LAST_DAY(event_time), INTERVAL 1 DAY), INTERVAL 7 DAY)
                        THEN user_id END)                            AS wau_last7,
       COUNT(DISTINCT user_id)                                       AS mau,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN event_time >= DATE_SUB(DATE_ADD(LAST_DAY(event_time), INTERVAL 1 DAY), INTERVAL 7 DAY)
                        THEN user_id END) / COUNT(DISTINCT user_id), 2) AS wau_to_mau_pct
FROM   events
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** Overlap = users active in the month's final 7 days ÷ all month actives; high values mean usage is concentrated and current rather than stale-accumulated.

## Q62: Revenue split — first-purchase revenue vs repeat-purchase revenue.

Tables: `orders(order_id, user_id, created_at, total_amount)`.

**Query:**
```sql
-- SQL Server
WITH order_rank AS (
  SELECT order_id, user_id, created_at, total_amount,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) AS order_rn
  FROM   orders
)
SELECT DATEPART(month, created_at) AS mth,
       SUM(CASE WHEN order_rn = 1 THEN total_amount ELSE 0 END) AS first_order_revenue,
       SUM(CASE WHEN order_rn > 1 THEN total_amount ELSE 0 END) AS repeat_revenue
FROM   order_rank
GROUP  BY DATEPART(month, created_at);
```
**Explanation:** `ROW_NUMBER` per user tags each customer's very first order; revenue splits into acquisition-fueled (rn=1) versus retention-backed (rn>1).

## Q63: Median pageviews before a user's first purchase.

Tables: `events(event_id, user_id, event_time, event_type, url)`, `orders(order_id, user_id, created_at)`.

**Query:**
```sql
-- PostgreSQL
WITH first_order AS (
  SELECT user_id, MIN(created_at) AS fo_ts FROM orders GROUP BY 1
),
pvs_before AS (
  SELECT e.user_id, COUNT(*) AS pvs
  FROM   events e
  JOIN   first_order fo ON fo.user_id = e.user_id
  WHERE  e.event_type = 'page_view'
     AND e.event_time < fo.fo_ts
  GROUP  BY e.user_id
)
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY pvs) AS median_pvs_to_purchase,
       AVG(pvs) AS avg_pvs_to_purchase
FROM   pvs_before;
```
**Explanation:** Counting pageviews strictly before the first order and taking the median gives the "research depth" before commitment, robust to whale sessions.

## Q64: Browse-only users — active for 30+ days who never made a purchase.

Tables: `events(event_id, user_id, event_time)`, `orders(order_id, user_id, created_at)`.

**Query:**
```sql
-- PostgreSQL
WITH ever_buyer AS (
  SELECT DISTINCT user_id FROM orders
)
SELECT COUNT(DISTINCT e.user_id)                                AS active_never_bought,
       ROUND(100.0 * COUNT(DISTINCT e.user_id)
             / NULLIF((SELECT COUNT(DISTINCT user_id) FROM events), 0), 2) AS browse_only_pct
FROM   events e
LEFT   JOIN ever_buyer b ON b.user_id = e.user_id
WHERE  b.user_id IS NULL
  AND  e.event_time >= CURRENT_DATE - 30;
```
**Explanation:** Active-but-never-converted users = actives minus buyers; a large browse-only slice is a monetization opportunity, not merely lost users.

## Q65: Cart abandonment rate per day.

Tables: `cart_events(event_id, user_id, session_id, event_type, event_time)`; event_type in ('add_to_cart','checkout_started','purchase_completed').

**Query:**
```sql
-- MySQL 8+
SELECT DATE(event_time) AS day,
       COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart' THEN session_id END) AS carts,
       COUNT(DISTINCT CASE WHEN event_type = 'checkout_started' THEN session_id END) AS checkouts,
       COUNT(DISTINCT CASE WHEN event_type = 'purchase_completed' THEN session_id END) AS purchases,
       ROUND(100.0 * (COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart' THEN session_id END)
                     - COUNT(DISTINCT CASE WHEN event_type = 'purchase_completed' THEN session_id END))
             / COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart' THEN session_id END), 2) AS cart_abandonment_rate_pct
FROM   cart_events
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** Cart abandonment = (carts − completed purchases) ÷ carts at the session level; counting sessions, not events, avoids double-counting within a session.

## Q66: Do weekend signups retain better than weekday signups? Compare week-1 retention.

Tables: `users(user_id, signup_date)`, `events(event_id, user_id, event_time)`.

**Query:**
```sql
-- SQL Server
WITH birth AS (
  SELECT user_id,
         CASE WHEN DATEPART(weekday, signup_date) IN (1, 7) THEN 'weekend' ELSE 'weekday' END AS signup_day_type,
         signup_date
  FROM   users
),
wk AS (
  SELECT user_id, DATEDIFF(DAY, birth.signup_date, event_time) AS day_offset
  FROM   events e
  JOIN   birth ON birth.user_id = e.user_id
  WHERE  DATEDIFF(DAY, birth.signup_date, event_time) BETWEEN 0 AND 7
)
SELECT b.signup_day_type,
       COUNT(DISTINCT b.user_id) AS cohort,
       COUNT(DISTINCT CASE WHEN w.day_offset = 7 THEN b.user_id END) AS retained_d7,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN w.day_offset = 7 THEN b.user_id END)
             / COUNT(DISTINCT b.user_id), 1) AS d7_retention_pct
FROM   birth b
LEFT   JOIN wk w ON w.user_id = b.user_id
GROUP  BY b.signup_day_type;
```
**Explanation:** Wrapping signup date by weekday and testing the user's day-7 appearance compares acquisition quality (intent) across weekdays vs weekends.

## Q67: DAU by acquisition channel — which channel drives today's actives.

Tables: `users(user_id, signup_date, channel)`, `events(event_id, user_id, event_time)`.

**Query:**
```sql
-- PostgreSQL
SELECT u.channel,
       COUNT(DISTINCT e.user_id) AS active_users_today
FROM   users u
JOIN   events e ON e.user_id = u.user_id AND e.event_time::date = CURRENT_DATE
GROUP  BY u.channel
ORDER  BY active_users_today DESC;
```
**Explanation:** Active users joined back to the channel that acquired them — the raw material for CAC-weighted channel ROI versus Q38's spend view.

## Q68: Power users — top 1% by session count and their revenue contribution.

Tables: `sessions(session_id, user_id, started_at)`, `orders(order_id, user_id, total_amount)`.

**Query:**
```sql
-- MySQL 8+
WITH usage_cnt AS (
  SELECT user_id, COUNT(*) AS sessions,
         PERCENT_RANK() OVER (ORDER BY COUNT(*) DESC) AS pctl
  FROM   sessions
  GROUP  BY user_id
),
power AS (
  SELECT user_id FROM usage_cnt WHERE pctl <= 0.01
)
SELECT (p.user_id IS NOT NULL) AS is_power_user,
       COUNT(DISTINCT o.user_id)                  AS buyers,
       COALESCE(SUM(o.total_amount), 0)           AS revenue,
       ROUND(100.0 * COALESCE(SUM(o.total_amount), 0) / SUM(SUM(o.total_amount)) OVER (), 2) AS revenue_share_pct
FROM   orders o
LEFT   JOIN power p ON p.user_id = o.user_id
GROUP  BY 1;
```
**Explanation:** `PERCENT_RANK` labels the heaviest 1% of users; their revenue share quantifies dependence on the power-user tail.

## Q69: Session gap distribution — hours between consecutive sessions per user.

Tables: `sessions(session_id, user_id, started_at)`.

**Query:**
```sql
-- PostgreSQL
WITH gapped AS (
  SELECT user_id, started_at,
         LAG(started_at) OVER (PARTITION BY user_id ORDER BY started_at) AS prev_start
  FROM   sessions
)
SELECT width_bucket(EXTRACT(EPOCH FROM (started_at - prev_start)) / 3600.0, 0, 168, 12) AS gap_bucket,
       COUNT(*) AS gaps
FROM   gapped
WHERE  prev_start IS NOT NULL
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** Time since a user's own previous session reveals natural cadence (daily weekly); `width_bucket` turns hour gaps into 12 weekly-spanning bins.

## Q70: Same-day return — % of users who come back within 24 hours of their first visit.

Tables: `events(event_id, user_id, event_time)`.

**Query:**
```sql
-- SQL Server
WITH first_seen AS (
  SELECT user_id, MIN(event_time) AS first_ts FROM events GROUP BY user_id
)
SELECT COUNT(*) AS users,
       COUNT(CASE WHEN EXISTS (
         SELECT 1 FROM events e WHERE e.user_id = f.user_id
           AND e.event_time > f.first_ts
           AND e.event_time <= DATEADD(HOUR, 24, f.first_ts)
       ) THEN 1 END) AS returned_24h,
       ROUND(100.0 * COUNT(CASE WHEN EXISTS (
         SELECT 1 FROM events e WHERE e.user_id = f.user_id
           AND e.event_time > f.first_ts
           AND e.event_time <= DATEADD(HOUR, 24, f.first_ts)
       ) THEN 1 END) / COUNT(*), 1) AS return_24h_pct
FROM   first_seen f;
```
**Explanation:** An EXISTS probe for any event in the 24h after first-seen measures the "got them to come back once" hook; the strongest single-day retention predictor.

## Q71: User lifecycle migration — how segment memberships move month over month.

Tables: `events(event_id, user_id, event_time)` aggregated to monthly lifecycles via classifications: New (<30d), Rising (active 2 of last 3 mo), Declining, At-risk (no activity this month, active last mo), Churned (no activity in 60d+).

**Query:**
```sql
-- PostgreSQL
WITH mo AS (
  SELECT user_id, date_trunc('month', event_time) AS m FROM events GROUP BY 1, 2
),
span AS (
  SELECT user_id,
         COUNT(*) FILTER (WHERE m = date_trunc('month', CURRENT_DATE))      AS this_mo,
         COUNT(*) FILTER (WHERE m = date_trunc('month', CURRENT_DATE - INTERVAL '1 month')) AS last_mo,
         COUNT(*) FILTER (WHERE m BETWEEN date_trunc('month', CURRENT_DATE - INTERVAL '2 months') AND date_trunc('month', CURRENT_DATE)) AS last_3_mo
  FROM   mo
  GROUP  BY user_id
)
SELECT CASE
         WHEN this_mo > 0 AND last_mo = 0 THEN 'new_or_returning'
         WHEN this_mo > 0 AND last_3_mo >= 2 THEN 'rising'
         WHEN this_mo = 0 AND last_mo > 0 THEN 'at_risk'
         WHEN this_mo = 0 AND last_mo = 0 THEN 'churned'
         ELSE 'declining'
       END AS lifecycle,
       COUNT(*) AS users
FROM   span
GROUP  BY 1
ORDER  BY users DESC;
```
**Explanation:** Classifying each user against a month-span of activity flags builds a lifecycle cohort you can re-run each month to watch segments migrate.

## Q72: At-risk scoring — users whose last activity is past their median gap.

Tables: `events(event_id, user_id, event_time)`.

**Query:**
```sql
-- PostgreSQL
WITH gaps AS (
  SELECT user_id,
         event_time,
         LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time) AS prev
  FROM   events
  GROUP  BY user_id, event_time
),
stats AS (
  SELECT user_id,
         AVG(EXTRACT(EPOCH FROM (event_time - prev)) / 86400.0) AS avg_gap_days,
         MAX(event_time) AS last_seen
  FROM   gaps WHERE prev IS NOT NULL
  GROUP  BY user_id
)
SELECT user_id,
       ROUND(avg_gap_days, 1) AS avg_gap_days,
       last_seen,
       (CURRENT_DATE - last_seen::date) AS days_since_last,
       ((CURRENT_DATE - last_seen::date) > avg_gap_days * 1.5) AS at_risk
FROM   stats
ORDER  BY at_risk DESC, days_since_last DESC;
```
**Explanation:** If today's silence exceeds 1.5× the user's own average inter-session gap, they're deviating from personal cadence — the first warning before churn.

## Q73: Does using a feature improve retention? Compare 7-day return by feature use.

Tables: `feature_events(feature_id, user_id, event_time)`, `events(event_id, user_id, event_time)`.

**Query:**
```sql
-- MySQL 8+
WITH first_use AS (
  SELECT user_id, MIN(event_time) AS fu_ts
  FROM   feature_events WHERE feature_id = 'collab' GROUP BY user_id
)
SELECT COUNT(DISTINCT CASE WHEN e.event_time BETWEEN fu.fu_ts AND DATE_ADD(fu.fu_ts, INTERVAL 7 DAY)
                        THEN fu.user_id END) AS returned_within_7d
     , COUNT(DISTINCT CASE WHEN e.event_time > DATE_ADD(fu.fu_ts, INTERVAL 7 DAY)
                        THEN fu.user_id END) AS active_after_d7
     , COUNT(DISTINCT fu.user_id)            AS feature_users
FROM   first_use fu
LEFT   JOIN events e ON e.user_id = fu.user_id;
```
**Explanation:** Restricting to feature users and measuring their return rate within/beyond 7 days tests activation lift — a restricted gate, not a whole-base stat.

## Q74: Cohort stickiness — DAU/MAU per cohort over time.

Tables: `events(event_id, user_id, event_time)`, `users(user_id, signup_date)`.

**Query:**
```sql
-- PostgreSQL: for each cohort-month, stickiness = active days ÷ monthly distinct users
WITH cohort AS (
  SELECT u.user_id, date_trunc('month', u.signup_date) AS cohort
  FROM   users u
),
em AS (
  SELECT e.user_id, date_trunc('month', e.event_time) AS m, e.event_time::date AS d
  FROM   events e
  GROUP  BY 1, 2, 3
)
SELECT c.cohort,
       em.m,
       COUNT(DISTINCT em.d)                  AS distinct_active_days,
       COUNT(DISTINCT em.user_id)            AS mau,
       ROUND(COUNT(DISTINCT em.d) * 1.0
             / NULLIF(COUNT(DISTINCT em.user_id), 0), 3) AS stickiness_days_per_mau
FROM   cohort c
JOIN   em ON em.user_id = c.user_id AND em.m >= c.cohort AND em.m < c.cohort + INTERVAL '6 months'
GROUP  BY c.cohort, em.m
ORDER  BY c.cohort, em.m;
```
**Explanation:** Stickiness per cohort-month = distinct active days (a day-level DAU proxy) ÷ distinct monthly actives inside that cohort's month; ratios sliding downward flag engagement dilution even when cohort counts hold.

**Alt1:**
```sql
-- SQL Server: same metric via EOMONTH bucketing
WITH cohort AS (
  SELECT user_id, EOMONTH(signup_date) AS cohort FROM users
),
em AS (
  SELECT EOMONTH(event_time) AS m, CAST(event_time AS date) AS d, user_id
  FROM   events
  GROUP  BY EOMONTH(event_time), CAST(event_time AS date), user_id
)
SELECT c.cohort, em.m,
       COUNT(DISTINCT em.d)                       AS distinct_active_days,
       COUNT(DISTINCT em.user_id)                 AS mau,
       ROUND(1.0 * COUNT(DISTINCT em.d) / NULLIF(COUNT(DISTINCT em.user_id), 0), 3) AS stickiness_days_per_mau
FROM   cohort c
JOIN   em ON em.user_id = c.user_id AND em.m >= c.cohort
         AND em.m <= DATEADD(MONTH, 5, c.cohort)
GROUP  BY c.cohort, em.m
ORDER  BY c.cohort, em.m;
```

## Q75: Overlapping windows compared — trailing 7-day vs 28-day actives as a ratio.

Tables: `events(event_id, user_id, event_time)`.

**Query:**
```sql
-- PostgreSQL
WITH daily AS (
  SELECT event_time::date AS day, user_id FROM events GROUP BY 1, 2
)
SELECT day,
       (SELECT COUNT(DISTINCT user_id) FROM daily a
        WHERE a.day > d.day - 7  AND a.day <= d.day)  AS trailing_7d,
       (SELECT COUNT(DISTINCT user_id) FROM daily b
        WHERE b.day > d.day - 28 AND b.day <= d.day) AS trailing_28d,
       ROUND(100.0 * (SELECT COUNT(DISTINCT user_id) FROM daily a
        WHERE a.day > d.day - 7  AND a.day <= d.day)
       / NULLIF((SELECT COUNT(DISTINCT user_id) FROM daily b
        WHERE b.day > d.day - 28 AND b.day <= d.day), 0), 1) AS freq_ratio_pct
FROM   (SELECT DISTINCT day FROM daily) d
ORDER  BY day;
```
**Explanation:** trailing_7d ÷ trailing_28d is an overlap ratio expressing how "recent" the accumulated audience is; it rises after campaigns and falls as stale users accumulate.

## Q76: Median session length by day of week.

Tables: `sessions(session_id, user_id, started_at TIMESTAMP, ended_at TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL
SELECT TO_CHAR(started_at, 'Dy')                        AS weekday
     , EXTRACT(ISODOW FROM started_at)                  AS iso_dow
     , ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (ended_at - started_at)) / 60.0), 1) AS median_session_min
FROM   sessions
GROUP  BY 1, 2
ORDER  BY 2;
```
**Explanation:** Median session minutes per weekday highlights engagement rhythm (weekday work-lunch vs weekend binge blocks) without average-skew noise.

## Q77: Timezone-aware activity — DAU per hour using each user's regional offset.

Tables: `users(user_id, tz_offset_hours SMALLINT)`, `events(event_id, user_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL
SELECT ((EXTRACT(HOUR FROM event_time) + u.tz_offset_hours) % 24)::int AS local_hour,
       COUNT(DISTINCT e.user_id) AS users
FROM   events e
JOIN   users u ON u.user_id = e.user_id
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** Adding the user's stored UTC offset to the event hour yields their *local* clock time, so peak-hours reflect real-world behavior not UTC geography.

## Q78: Downward anomaly — days whose DAU is 2σ below the 30-day window.

Tables: `events(event_id, user_id, event_time)`.

**Query:**
```sql
-- SQL Server
WITH daily AS (
  SELECT CAST(event_time AS date) AS day, COUNT(DISTINCT user_id) AS dau
  FROM   events
  GROUP  BY CAST(event_time AS date)
),
stats AS (
  SELECT day, dau,
         AVG(dau)  OVER (ORDER BY day ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING) AS base,
         STDEV(dau) OVER (ORDER BY day ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING) AS sd
  FROM   daily
)
SELECT day, dau, base, sd
FROM   stats
WHERE  sd IS NOT NULL AND base IS NOT NULL
  AND  dau < base - 2 * sd
ORDER  BY day;
```
**Explanation:** The mirrored condition `dau < base − 2σ` flags outages, tracking-pixel failures, or platform issues — the crash twin of Q42's spike check.

## Q79: Monitoring band — 7-day moving average DAU with upper/lower control limits.

Tables: `events(event_id, user_id, event_time)`.

**Query:**
```sql
-- PostgreSQL
WITH daily AS (
  SELECT event_time::date AS day, COUNT(DISTINCT user_id) AS dau
  FROM   events GROUP BY 1
)
SELECT day, dau,
       ROUND(AVG(dau) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 1)             AS ma7,
       ROUND(AVG(dau) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
             - 2 * STDDEV(dau) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 1)      AS lower_band,
       ROUND(AVG(dau) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
             + 2 * STDDEV(dau) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 1)      AS upper_band
FROM   daily
ORDER  BY day;
```
**Explanation:** A moving average with ±2σ bands yields an automated monitoring sheet; any DAU outside the band triggers investigation.

## Q80: Paid vs organic LTV comparison.

Tables: `users(user_id, signup_date, channel)`, `orders(order_id, user_id, created_at, total_amount)`, `sessions(session_id, user_id, started_at)`.

**Query:**
```sql
-- MySQL 8+
WITH arpu AS (
  SELECT u.channel,
         COUNT(DISTINCT u.user_id) AS users,
         COALESCE(SUM(o.total_amount), 0) AS revenue
  FROM   users u
  LEFT   JOIN orders o ON o.user_id = u.user_id
  GROUP  BY u.channel
),
life AS (
  SELECT u.channel,
         AVG(TIMESTAMPDIFF(DAY, u.signup_date, s.last_seen)) / 30.44 AS lifetime_months
  FROM   users u
  LEFT   JOIN (SELECT user_id, MAX(started_at) AS last_seen FROM sessions GROUP BY user_id) s
         ON s.user_id = u.user_id
  GROUP  BY u.channel
)
SELECT a.channel,
       (a.revenue / a.users) * IFNULL(l.lifetime_months, 1) AS ltv,
       (a.revenue / a.users)                                AS arpu
FROM   arpu a
JOIN   life l ON l.channel = a.channel;
```
**Explanation:** LTV = ARPU × lifetime for paid vs organic slices; comparing the two tells you whether the paid dollar buys habituated or one-shot users.

## Q81: CAC payback period — months for a cohort's margin to repay its CAC.

Tables: `marketing_spend(date, channel, spend)`, `customers(user_id, acquired_at)`, `order_ledger(order_id, user_id, month, gross_margin)`.

**Query:**
```sql
-- SQL Server
DECLARE @month DATE = '2024-06-01';
;WITH cac AS (
  SELECT SUM(m.spend) / NULLIF(COUNT(DISTINCT c.user_id), 0) AS cac_per_user
  FROM   marketing_spend m
  LEFT   JOIN customers c
         ON DATEFROMPARTS(YEAR(c.acquired_at), MONTH(c.acquired_at), 1)
          = DATEFROMPARTS(YEAR(m.spend_date), MONTH(m.spend_date), 1)
  WHERE  DATEFROMPARTS(YEAR(m.spend_date), MONTH(m.spend_date), 1) = @month
),
margin AS (
  SELECT SUM(o.gross_margin) / NULLIF(COUNT(DISTINCT c.user_id), 0) AS avg_margin_per_user
  FROM   order_ledger o
  JOIN   customers c ON c.user_id = o.user_id
  WHERE  DATEFROMPARTS(YEAR(c.acquired_at), MONTH(c.acquired_at), 1) = @month
)
SELECT @month AS cohort,
       cac.cac_per_user,
       m.avg_margin_per_user,
       ROUND(cac.cac_per_user / NULLIF(m.avg_margin_per_user, 0), 1) AS payback_months
FROM   cac, margin;
```
**Explanation:** Payback = CAC ÷ average monthly gross margin per customer in the same cohort; below ~12 months is healthy for SaaS, above and the funnel is a money pit.

## Q82: Single vs multi-product adoption — users of one product vs two or more.

Tables: `product_usage(user_id, product, used_on)`.

**Query:**
```sql
-- PostgreSQL
WITH per_user AS (
  SELECT user_id, COUNT(DISTINCT product) AS products_used
  FROM   product_usage
  GROUP  BY user_id
)
SELECT CASE
         WHEN products_used = 1 THEN 'single_product'
         WHEN products_used = 2 THEN 'two_products'
         ELSE 'multi_product'
       END AS segment,
       COUNT(*) AS users
FROM   per_user
GROUP  BY 1
ORDER  BY users DESC;
```
**Explanation:** Segmenting users by distinct product count measures suite expansion; multi-product share is the leading indicator of retention and upmarket revenue.

## Q83: Upgrade velocity — median days between signup and first paid plan.

Tables: `users(user_id, signup_date)`, `subscriptions(subscription_id, user_id, plan_start, plan)`.

**Query:**
```sql
-- MySQL 8+ (median via ROW_NUMBER — MySQL has no PERCENTILE_CONT)
WITH first_paid AS (
  SELECT user_id, MIN(plan_start) AS paid_at
  FROM   subscriptions
  WHERE  plan <> 'free'
  GROUP  BY user_id
),
days AS (
  SELECT TIMESTAMPDIFF(DAY, u.signup_date, fp.paid_at) AS ttf_days
  FROM   first_paid fp
  JOIN   users u ON u.user_id = fp.user_id
),
ranked AS (
  SELECT ttf_days,
         ROW_NUMBER() OVER (ORDER BY ttf_days) AS rn,
         COUNT(*) OVER ()                      AS n
  FROM   days
)
SELECT ROUND(AVG(ttf_days), 1) AS avg_days,
       (SELECT ttf_days FROM ranked WHERE rn = FLOOR((n + 1) / 2))                     AS p50_days,
       (SELECT MIN(ttf_days) FROM ranked WHERE rn >= 0.9 * n)                          AS p90_days,
       (SELECT ttf_days FROM (SELECT ttf_days, rn, n FROM ranked ORDER BY rn DESC LIMIT 1) x) AS slowest_upgrade_days
FROM   days;
```
**Explanation:** The distribution of signup→paid days (p50/p90) marks the paywall-assist window; p50 is the ROW_NUMBER median, p90 is the first row crossing the 90th percentile, and a far-right p90 means the trial nudge arrives too late for many.

**Alt1:**
```sql
-- PostgreSQL (native percentile support, same output)
WITH first_paid AS (
  SELECT user_id, MIN(plan_start) AS paid_at
  FROM   subscriptions WHERE plan <> 'free' GROUP  BY user_id
),
days AS (
  SELECT (fp.paid_at::date - u.signup_date::date) AS ttf_days
  FROM   first_paid fp JOIN users u ON u.user_id = fp.user_id
)
SELECT ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY ttf_days), 1) AS p50_days,
       ROUND(PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY ttf_days), 1) AS p90_days,
       ROUND(AVG(ttf_days), 1)                                         AS avg_days
FROM   days;
```

## Q84: Cross-sell rate — buyers of product A who also bought product B.

Tables: `order_items(order_id, product_id, quantity)`, `orders(order_id, user_id)`.

**Query:**
```sql
-- PostgreSQL
WITH a AS (SELECT DISTINCT o.user_id
           FROM   orders o JOIN order_items i ON i.order_id = o.order_id
           WHERE  i.product_id = 'A')
SELECT COUNT(DISTINCT a.user_id)                              AS buyers_of_A,
       COUNT(DISTINCT CASE WHEN b.user_id IS NOT NULL THEN a.user_id END) AS also_bought_B,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN b.user_id IS NOT NULL THEN a.user_id END)
             / COUNT(DISTINCT a.user_id), 1) AS cross_sell_rate_pct
FROM   a
LEFT   JOIN (SELECT DISTINCT o.user_id
             FROM   orders o JOIN order_items i ON i.order_id = o.order_id
             WHERE  i.product_id = 'B') b ON b.user_id = a.user_id;
```
**Explanation:** Cross-sell = A-buyers who ever bought B ÷ all A-buyers; a second join on the same order_items via orders makes item-pair affinity constant.

## Q85: Guarantee-window returns — items returned within the 30-day policy.

Tables: `returns(return_id, order_id, item_id, returned_at)`, `orders(order_id, user_id, created_at)`, `order_items(order_id, item_id, unit_price)`.

**Query:**
```sql
-- SQL Server
SELECT YEAR(o.created_at) AS yr, MONTH(o.created_at) AS mo,
       SUM(i.unit_price * i.quantity)                                          AS gross,
       SUM(CASE WHEN r.return_id IS NOT NULL AND DATEDIFF(DAY, o.created_at, r.returned_at) <= 30
                THEN i.unit_price * i.quantity ELSE 0 END)                     AS returned_value,
       ROUND(100.0 * SUM(CASE WHEN r.return_id IS NOT NULL AND DATEDIFF(DAY, o.created_at, r.returned_at) <= 30
                THEN i.unit_price * i.quantity ELSE 0 END) / NULLIF(SUM(i.unit_price * i.quantity), 0), 2) AS guarantee_returns_pct
FROM   order_items i
JOIN   orders o ON o.order_id = i.order_id
LEFT   JOIN returns r ON r.order_id = i.order_id AND r.item_id = i.item_id
GROUP  BY YEAR(o.created_at), MONTH(o.created_at);
```
**Explanation:** Value-weighted returns inside the 30-day guarantee window ÷ gross item value measures product-fit risk and the revenue that refunds claw back.

## Q86: Survey response bias — response rate by customer segment.

Tables: `surveys(survey_id, user_id, score, submitted_at)`, `users(user_id, plan, subscriber_since)`.

**Query:**
```sql
-- PostgreSQL
WITH sent AS (
  SELECT user_id, plan FROM users
)
SELECT u.plan,
       COUNT(DISTINCT u.user_id) AS users,
       COUNT(DISTINCT s.user_id) AS respondents,
       ROUND(100.0 * COUNT(DISTINCT s.user_id) / NULLIF(COUNT(DISTINCT u.user_id), 0), 1) AS response_rate_pct,
       ROUND(AVG(s.score) FILTER (WHERE s.user_id IS NOT NULL), 2)                        AS avg_score
FROM   sent u
LEFT   JOIN surveys s ON s.user_id = u.user_id
GROUP  BY u.plan
ORDER  BY response_rate_pct DESC;
```
**Explanation:** Comparing response rate by plan exposes NPS bias — if free users answer 2× more, raw NPS is skewed and needs weighting before action.

**Alt1:**
```sql
-- PostgreSQL: weighted NPS — re-weight each bucket by inverse response rate per plan
WITH rates AS (
  SELECT plan, COUNT(DISTINCT u.user_id)::numeric / NULLIF(COUNT(DISTINCT s.user_id), 0) AS w
  FROM   users u LEFT JOIN surveys s ON s.user_id = u.user_id
  GROUP  BY plan
)
SELECT ROUND(SUM((CASE WHEN x.score BETWEEN 9 AND 10 THEN 1
                       WHEN x.score BETWEEN 0 AND 6 THEN -1 ELSE 0 END) * r.w)
             / NULLIF(SUM(r.w), 0), 2) AS weighted_nps
FROM   surveys x
JOIN   users u ON u.user_id = x.user_id
JOIN   rates r ON r.plan = u.plan;
```

## Q87: Bounce rate by device.

Tables: `sessions(session_id, user_id, device, entry_url, started_at)`, `events(event_id, session_id, event_type)`.

**Query:**
```sql
-- PostgreSQL
WITH pv AS (
  SELECT session_id, COUNT(*) AS pvs
  FROM   events WHERE event_type = 'page_view' GROUP BY session_id
)
SELECT s.device,
       COUNT(*) AS sessions,
       COUNT(*) FILTER (WHERE COALESCE(pv.pvs, 0) <= 1) AS bounced,
       ROUND(100.0 * COUNT(*) FILTER (WHERE COALESCE(pv.pvs, 0) <= 1) / COUNT(*), 1) AS bounce_rate_pct
FROM   sessions s
LEFT   JOIN pv ON pv.session_id = s.session_id
GROUP  BY s.device
ORDER  BY bounce_rate_pct DESC;
```
**Explanation:** Same bounce definition as Q19 but sliced by device; mobile bouncing far above desktop usually implicates page weight or the signup wall, not intent.

## Q88: Funnel conversion by device with step ratios.

Tables: `events(event_id, user_id, device, event_time, event_type)`; event_type in ('view','add_to_cart','purchase').

**Query:**
```sql
-- MySQL 8+
WITH steps AS (
  SELECT device,
         COUNT(DISTINCT CASE WHEN event_type = 'view'        THEN user_id END) AS v,
         COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart' THEN user_id END) AS c,
         COUNT(DISTINCT CASE WHEN event_type = 'purchase'    THEN user_id END) AS p
  FROM   events
  GROUP  BY device
)
SELECT device,
       ROUND(100.0 * c / NULLIF(v, 0), 1) AS view_to_cart_pct,
       ROUND(100.0 * p / NULLIF(c, 0), 1) AS cart_to_purchase_pct,
       ROUND(100.0 * p / NULLIF(v, 0), 1) AS end_to_end_pct
FROM   steps
ORDER  BY end_to_end_pct DESC;
```
**Explanation:** A device-sliced funnel shows where each platform diverges — e.g., mobile converting cart→purchase worse flags checkout UX, worse view→cart flags discovery.

## Q89: MAU by region plus market-penetration density.

Tables: `users(user_id, region, signup_date)`, `events(event_id, user_id, event_time)`, `regional_population(region, population)`.

**Query:**
```sql
-- PostgreSQL
SELECT u.region,
       COUNT(DISTINCT e.user_id)                    AS mau,
       COUNT(DISTINCT u.user_id)                    AS total_users,
       ROUND(1000.0 * COUNT(DISTINCT e.user_id)
             / NULLIF(MAX(rp.population), 0), 2)    AS da
FROM   users u
LEFT   JOIN events e ON e.user_id = u.user_id
    AND e.event_time >= CURRENT_TIMESTAMP - INTERVAL '30 days'
LEFT   JOIN regional_population rp ON rp.region = u.region
GROUP  BY u.region
ORDER  BY mau DESC;
```
**Explanation:** MAU joined to region and population density (users per 1000 residents) separates big-market raw MAU from small-market saturation — the two metrics rarely rank the same.

## Q90: Cohort convergence — does a new cohort reach the same month-3 retention as a mature one?

Tables: `users(user_id, signup_date)`, `events(event_id, user_id, event_time)`.

**Query:**
```sql
-- MySQL 8+
WITH birth AS (
  SELECT user_id, DATE_FORMAT(signup_date, '%Y-%m-01') AS cohort
  FROM   users
),
seen AS (
  SELECT DISTINCT user_id, DATE_FORMAT(event_time, '%Y-%m-01') AS m FROM events
),
joined AS (
  SELECT b.cohort,
         b.user_id,
         MAX(CASE WHEN s.m = DATE_ADD(b.cohort, INTERVAL 3 MONTH) THEN 1 ELSE 0 END) AS retained_m3
  FROM   birth b
  LEFT   JOIN seen s ON s.user_id = b.user_id
  GROUP  BY b.cohort, b.user_id
),
agg AS (
  SELECT cohort,
         COUNT(*)                                             AS cohort_size,
         SUM(retained_m3)                                     AS retained_m3,
         ROUND(100.0 * SUM(retained_m3) / COUNT(*), 1)        AS retention_m3_pct
  FROM   joined
  GROUP  BY cohort
)
SELECT cohort, cohort_size, retained_m3, retention_m3_pct,
       LAG(retention_m3_pct) OVER (ORDER BY cohort)           AS prev_cohort_m3_pct,
       ROUND(retention_m3_pct - LAG(retention_m3_pct) OVER (ORDER BY cohort), 1) AS convergence_delta
FROM   agg
ORDER  BY cohort;
```
**Explanation:** Each cohort's month-3 retention is computed, then `LAG` reads the prior cohort's rate — `convergence_delta ≈ 0` means new vintages retain like the last one (steady product-market fit), while a widening gap means quality or fit is decaying.

## Q91: Average order value weighted across markets via FX-normalized totals.

Tables: `orders(order_id, user_id, created_at, total_amount, currency)`, `fx_rates(currency, usd_rate, effective_date)`.

**Query:**
```sql
-- SQL Server
SELECT o.currency,
       COUNT(DISTINCT o.order_id)                                    AS orders,
       SUM(o.total_amount)                                           AS local_amount,
       SUM(o.total_amount * fx.usd_rate)                             AS usd_amount,
       ROUND(SUM(o.total_amount * fx.usd_rate) / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS aov_usd
FROM   orders o
JOIN   fx_rates fx ON fx.currency = o.currency
                  AND fx.effective_date = (SELECT MAX(effective_date) FROM fx_rates f2
                                           WHERE f2.currency = o.currency AND f2.effective_date <= o.created_at)
GROUP  BY o.currency;
```
**Explanation:** Joining each order to the latest FX rate on its creation date normalizes to USD; AOV in USD is then apples-to-apples across markets.

## Q92: Cumulative revenue split — new-customer revenue vs existing-customer revenue over time.

Tables: `orders(order_id, user_id, created_at, total_amount)`.

**Query:**
```sql
-- PostgreSQL
WITH first_order AS (
  SELECT user_id, MIN(created_at)::date AS first_day FROM orders GROUP BY 1
),
daily AS (
  SELECT o.created_at::date AS day,
         SUM(CASE WHEN o.created_at::date = fo.first_day THEN o.total_amount ELSE 0 END) AS new_cust_rev,
         SUM(CASE WHEN o.created_at::date > fo.first_day THEN o.total_amount ELSE 0 END) AS existing_cust_rev
  FROM   orders o
  JOIN   first_order fo ON fo.user_id = o.user_id
  GROUP  BY 1
)
SELECT day,
       new_cust_rev, existing_cust_rev,
       ROUND(100.0 * existing_cust_rev / NULLIF(new_cust_rev + existing_cust_rev, 0), 1) AS repeat_share_pct,
       SUM(new_cust_rev + existing_cust_rev) OVER (ORDER BY day) AS cumulative_revenue
FROM   daily
ORDER  BY day;
```
**Explanation:** Routing each order to new vs existing by comparing to the user's first order day, then a running total — the slope of `repeat_share_pct` rising is the healthiest growth sign in the report.

## Q93: MRR waterfall — new + expansion − contraction − churn per month.

Tables: `mrr_movements(month DATE, account_id, movement_type TEXT, amount DECIMAL)`; movement_type in ('new','expansion','contraction','churn').

**Query:**
```sql
-- PostgreSQL
SELECT to_char(date_trunc('month', month), 'YYYY-MM') AS month,
       COALESCE(SUM(amount) FILTER (WHERE movement_type = 'new'), 0)         AS new_mrr,
       COALESCE(SUM(amount) FILTER (WHERE movement_type = 'expansion'), 0)   AS expansion_mrr,
       COALESCE(SUM(amount) FILTER (WHERE movement_type = 'contraction'), 0) AS contraction_mrr,
       COALESCE(SUM(amount) FILTER (WHERE movement_type = 'churn'), 0)       AS churn_mrr,
       COALESCE(SUM(amount) FILTER (WHERE movement_type = 'new'), 0)
       + COALESCE(SUM(amount) FILTER (WHERE movement_type = 'expansion'), 0)
       - COALESCE(SUM(amount) FILTER (WHERE movement_type = 'contraction'), 0)
       - COALESCE(SUM(amount) FILTER (WHERE movement_type = 'churn'), 0)     AS net_mrr_change
FROM   mrr_movements
GROUP  BY 1
ORDER  BY 1;
```
**Explanation:** The waterfall sums each movement type separately before combining — the ledger behind "why did MRR move this month" and the input to NRR.

## Q94: Reconciliation — DAU computed from events vs from the sessions table disagree.

Tables: `events(event_id, user_id, event_time)`, `sessions(session_id, user_id, day DATE)`.

**Query:**
```sql
-- PostgreSQL
WITH a AS (
  SELECT event_time::date AS day, COUNT(DISTINCT user_id) AS dau FROM events GROUP BY 1
),
b AS (
  SELECT day, COUNT(DISTINCT user_id) AS dau FROM sessions GROUP BY 1
)
SELECT full.day, a.dau AS dau_events, b.dau AS dau_sessions, a.dau - b.dau AS delta
FROM   (SELECT DISTINCT day FROM (SELECT event_time::date AS day FROM events
                                  UNION SELECT day FROM sessions) u) full
LEFT   JOIN a ON a.day = full.day
LEFT   JOIN b ON b.day = full.day
WHERE  a.dau IS DISTINCT FROM b.dau
ORDER  BY full.day;
```
**Explanation:** A row per mismatch day quantifies definition drift (spider traffic, deduping errors, or session drops); a healthy pipeline shows zero rows and the CI check stays green.

## Q95: CAPSTONE A — Part 1/3: Build the daily growth-metrics table (DAU, new users, returning users).

Tables: `events(event_id, user_id, event_time TIMESTAMP, event_type)`, `users(user_id, signup_date DATE)`.

**Query:**
```sql
-- PostgreSQL
WITH dau AS (
  SELECT event_time::date AS day, COUNT(DISTINCT user_id) AS dau
  FROM   events GROUP BY 1
),
new_users AS (
  SELECT signup_date AS day, COUNT(*) AS new_users
  FROM   users GROUP BY 1
)
SELECT COALESCE(d.day, n.day)                       AS day
     , COALESCE(d.dau, 0)                           AS dau
     , COALESCE(n.new_users, 0)                     AS new_users
     , COALESCE(d.dau, 0) - COALESCE(n.new_users, 0) AS returning_users
FROM   dau d
FULL   OUTER JOIN new_users n ON n.day = d.day
ORDER  BY 1;
```
**Explanation:** Stage 1 materializes the three raw inputs of the growth dashboard — top-of-funnel additions (new), total pulse (DAU), and their reconciliation (returning = DAU − new). Rendering: daily line chart.

## Q96: CAPSTONE A — Part 2/3: Bolt growth rates and overlapping windows onto the daily table.

Tables: `events(event_id, user_id, event_time TIMESTAMP)`, `users(user_id, signup_date)`.

**Query:**
```sql
-- PostgreSQL
WITH daily AS (
  SELECT event_time::date AS day, COUNT(DISTINCT user_id) AS dau
  FROM   events GROUP BY 1
),
new_users AS (
  SELECT signup_date AS day, COUNT(*) AS new_users FROM users GROUP BY 1
),
combined AS (
  SELECT COALESCE(d.day, n.day) AS day, COALESCE(d.dau, 0) AS dau, COALESCE(n.new_users, 0) AS new_users
  FROM   daily d FULL OUTER JOIN new_users n ON n.day = d.day
)
SELECT day, dau, new_users,
       LAG(dau) OVER (ORDER BY day)                                                       AS prev_dau,
       ROUND(100.0 * (dau - LAG(dau) OVER (ORDER BY day)) / NULLIF(LAG(dau) OVER (ORDER BY day), 0), 2) AS dod_growth_pct,
       (SELECT COUNT(DISTINCT user_id) FROM events e
        WHERE  e.event_time::date > c.day - 7 AND e.event_time::date <= c.day)            AS rolling_7d,
       (SELECT COUNT(DISTINCT user_id) FROM events e
        WHERE  e.event_time::date > c.day - 28 AND e.event_time::date <= c.day)           AS rolling_28d
FROM   combined c
ORDER  BY day;
```
**Explanation:** Stage 2 enriches the base table with DoD growth and overlapping 7/28-day actives — a single daily snapshot that answers "are we growing and is the pulse recent."

## Q97: CAPSTONE A — Part 3/3: Final dashboard join — daily growth KPIs with week-1 cohort retention of that day's signups.

Tables: `users(user_id, signup_date DATE)`, `events(event_id, user_id, event_time TIMESTAMP)`.

**Query:**
```sql
-- PostgreSQL
WITH daily AS (
  SELECT event_time::date AS day, COUNT(DISTINCT user_id) AS dau FROM events GROUP BY 1
),
signup_cohort AS (
  SELECT signup_date AS day, COUNT(*) AS signups FROM users GROUP BY 1
),
w1_retention AS (
  SELECT u.signup_date AS day,
         COUNT(DISTINCT CASE WHEN e.event_time::date BETWEEN u.signup_date + 1 AND u.signup_date + 7
                          THEN u.user_id END) AS active_w1
  FROM   users u
  JOIN   events e ON e.user_id = u.user_id
  GROUP  BY u.signup_date
)
SELECT d.day, d.dau,
       COALESCE(s.signups, 0) AS signups,
       COALESCE(r.active_w1, 0) AS active_w1,
       ROUND(100.0 * COALESCE(r.active_w1, 0) / NULLIF(COALESCE(s.signups, 0), 0), 1) AS w1_retention_pct
FROM   daily d
LEFT   JOIN signup_cohort s  ON s.day = d.day
LEFT   JOIN w1_retention r   ON r.day = d.day
ORDER  BY d.day;
```
**Explanation:** Stage 3 lands the cohort lens on the same daily axis — for each day you see acquisition (signups), keeping (w1 retention), and total activity (DAU), completing the end-to-end growth pipeline.

## Q98: CAPSTONE B — Part 1/3: Monetization health — MRR waterfall plus account counts and churn %.

Tables: `accounts(account_id, plan, plan_start)`, `mrr_movements(month DATE, account_id, movement_type, amount)`, `churn_log(account_id, churned_at, mrr)`.

**Query:**
```sql
-- PostgreSQL
WITH movements AS (
  SELECT date_trunc('month', month) AS m,
         COALESCE(SUM(amount) FILTER (WHERE movement_type = 'new'), 0)         AS new_mrr,
         COALESCE(SUM(amount) FILTER (WHERE movement_type = 'expansion'), 0)   AS exp_mrr,
         COALESCE(SUM(amount) FILTER (WHERE movement_type = 'contraction'), 0) AS con_mrr,
         COALESCE(SUM(amount) FILTER (WHERE movement_type = 'churn'), 0)       AS churn_mrr
  FROM   mrr_movements
  GROUP  BY 1
),
accounts AS (
  SELECT date_trunc('month', plan_start) AS m, COUNT(*) AS accounts FROM accounts GROUP BY 1
),
churn_cnt AS (
  SELECT date_trunc('month', churned_at) AS m, COUNT(*) AS churned_accounts
  FROM   churn_log GROUP BY 1
)
SELECT to_char(M.m, 'YYYY-MM') AS month,
       M.new_mrr, M.exp_mrr, M.con_mrr, M.churn_mrr,
       ROUND(M.new_mrr + M.exp_mrr - M.con_mrr - M.churn_mrr, 2) AS net_mrr_change,
       A.accounts,
       C.churned_accounts,
       ROUND(100.0 * C.churned_accounts / NULLIF(A.accounts, 0), 2) AS logo_churn_pct
FROM   movements M
LEFT   JOIN accounts A   ON A.m = M.m
LEFT   JOIN churn_cnt C  ON C.m = M.m
ORDER  BY M.m;
```
**Explanation:** One table holds every MRR movement type, account base size, and churn count — the accounting-age view that answers "are we growing revenue through expansion or disguising churn with new logo sales."

## Q99: CAPSTONE B — Part 2/3: Cohort net revenue retention (NRR) — revenue surviving per month offset.

Tables: `accounts(account_id, plan, plan_start DATE)`, `mrr_movements(month DATE, account_id, movement_type, amount)`.

**Query:**
```sql
-- PostgreSQL
WITH cohort AS (
  SELECT account_id, date_trunc('month', plan_start) AS cohort FROM accounts
)
SELECT to_char(c.cohort, 'YYYY-MM')                                                   AS cohort,
       COUNT(DISTINCT c.account_id)                                                   AS accounts,
       COALESCE(SUM(CASE WHEN M.m = c.cohort THEN M.amount END), 0)                    AS m0_rev,
       COALESCE(SUM(CASE WHEN M.m = c.cohort + INTERVAL '3 months' THEN M.amount END), 0) AS m3_rev,
       COALESCE(SUM(CASE WHEN M.m = c.cohort + INTERVAL '6 months' THEN M.amount END), 0) AS m6_rev,
       ROUND(100.0 * COALESCE(SUM(CASE WHEN M.m = c.cohort + INTERVAL '6 months' THEN M.amount END), 0)
             / NULLIF(COALESCE(SUM(CASE WHEN M.m = c.cohort THEN M.amount END), 0), 0), 1) AS nrr_6mo_pct
FROM   cohort c
LEFT   JOIN mrr_movements M ON M.account_id = c.account_id AND M.m >= c.cohort
GROUP  BY c.cohort
ORDER  BY c.cohort;
```
**Explanation:** NRR tracks the same cohort's *current* MRR (minus churn but plus expansion) at fixed offsets — values above 100% mean expansions out-earn losses, the upmarket metric VCs grade on.

## Q100: CAPSTONE B — Part 3/3: Executive summary — ARR, logos, NRR, churn, and reconciliation check in one query.

Tables: `accounts(account_id, plan, plan_start DATE, mrr DECIMAL)`, `mrr_movements(month DATE, account_id, movement_type, amount)`, `churn_log(account_id, churned_at, mrr)`.

**Query:**
```sql
-- PostgreSQL
WITH active AS (
  SELECT account_id, mrr
  FROM   accounts
  WHERE  plan_start <= CURRENT_DATE
),
curr AS (
  SELECT date_trunc('month', CURRENT_DATE) AS m, account_id, mrr FROM active
),
arr AS (
  SELECT SUM(mrr) * 12 AS arr, COUNT(DISTINCT account_id) AS logos FROM active
),
churn_30d AS (
  SELECT COALESCE(SUM(mrr), 0) AS churned_value, COUNT(*) AS churned_logos
  FROM   churn_log
  WHERE  churned_at > CURRENT_DATE - 30
),
exp_30d AS (
  SELECT COALESCE(SUM(amount), 0) AS expansion_value
  FROM   mrr_movements
  WHERE  movement_type IN ('expansion','new')
    AND  month > CURRENT_DATE - 30
),
base AS (
  SELECT COALESCE(SUM(mrr), 0) AS starting_mrr
  FROM   accounts
  WHERE  plan_start < CURRENT_DATE - 30
)
SELECT ROUND(A.arr / 1000, 1)                       AS arr_k
     , A.logos                                       AS active_accounts
     , ROUND(100.0 * E.expansion_value / NULLIF(B.starting_mrr, 0), 2)                         AS gross_expansion_rate_pct
     , ROUND(100.0 * C.churned_value / NULLIF(B.starting_mrr, 0), 2)                           AS churn_rate_pct
     , ROUND(100.0 * (B.starting_mrr + E.expansion_value - C.churned_value) / NULLIF(B.starting_mrr, 0), 2) AS nrr_pct
FROM   arr A, base B, churn_30d C, exp_30d E;
```
**Explanation:** Final output compresses the whole pipeline into four board-room numbers (ARR, logos, churn %, NRR) and self-reconciles by construction: `starting + expansion − churn = ending`, so any accountant can validate the run.
