# Retention and Cohort Analytics — 100 Interview Q&A

## Q1: Build a cohort definition query. A cohort is all users who signed up in the same calendar month.
**Schema:** `users(id, signup_date)` — `signup_date` is a `DATE`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', signup_date)::date AS cohort_month,
  COUNT(*) AS cohort_size
FROM users
GROUP BY 1
ORDER BY 1;
```
**Explanation:** Truncates each `signup_date` to month start and counts users per bucket; the `::date` cast keeps output a clean `DATE`.

## Q2: Compute the classic retention table — cohort month x age month (0-11) — using a monthly activity table.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_month, num_activity_days)` — `active_month` is month-start `DATE`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date        AS cohort_month,
  DATE_PART('month', AGE(a.active_month, DATE_TRUNC('month', u.signup_date)))::int AS age_month,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT u.id) AS retention_pct
FROM users u
LEFT JOIN activity a
  ON a.user_id = u.id
 AND a.active_month >= DATE_TRUNC('month', u.signup_date)
 AND a.active_month <  DATE_TRUNC('month', u.signup_date) + INTERVAL '12 months'
GROUP BY 1, 2
ORDER BY 1, 2;
```
**Explanation:** Left-joins so users with zero activity appear as age months with NULL (dropped by `COUNT(DISTINCT ...)`) while they count in the denominator; `AGE()` gives whole-month offsets.

## Q3: Same retention table, but compute age month with a datediff instead of `AGE()` (PostgreSQL/Redshift).
**Schema:** `users(id, signup_date)`; `activity(user_id, active_month)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  (EXTRACT(YEAR FROM a.active_month) - EXTRACT(YEAR FROM DATE_TRUNC('month', u.signup_date))) * 12
    + (EXTRACT(MONTH FROM a.active_month) - EXTRACT(MONTH FROM DATE_TRUNC('month', u.signup_date))) AS age_month,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT u.id) AS retention_pct
FROM users u
LEFT JOIN activity a ON a.user_id = u.id
GROUP BY 1, 2
ORDER BY 1, 2;
```
**Explanation:** YYYY delta multiplied by 12 plus the month delta produces the calendar-month age; this is the classic datediff pattern before `DATE_DIFF` existed.

## Q4: DateDiff month-age pattern for MySQL/BigQuery to reproduce the retention age column.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_month)`.
**Query:**
```sql
SELECT
  DATE_FORMAT(u.signup_date, '%Y-%m-01') AS cohort_month,
  TIMESTAMPDIFF(MONTH, DATE_FORMAT(u.signup_date, '%Y-%m-01'), a.active_month) AS age_month,
  COUNT(DISTINCT a.user_id) / COUNT(DISTINCT u.id) AS retention_pct
FROM users u
LEFT JOIN activity a ON a.user_id = u.id
GROUP BY 1, 2
ORDER BY 1, 2;
```
**Explanation:** `TIMESTAMPDIFF(MONTH,...)` trims to whole elapsed months; truncating to month-01 first keeps fractional days from leaking into the age.

## Q5: DATEDIFF month-age pattern for Snowflake/Databricks (Spark SQL dialect).
**Schema:** `users(id, signup_date)`; `activity(user_id, active_month)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)                        AS cohort_month,
  MONTHS_BETWEEN(a.active_month, DATE_TRUNC('month', u.signup_date)) AS age_month,
  COUNT(DISTINCT a.user_id) / COUNT(DISTINCT u.id) AS retention_pct
FROM users u
LEFT JOIN activity a ON a.user_id = u.id
GROUP BY 1, 2
ORDER BY 1, 2;
```
**Explanation:** `MONTHS_BETWEEN` returns fractional months, so cast to int only in a dialect where you accept the floor; this is the canonical Spark/BigQuery-safe datediff trick.

## Q6: Day-0 (same day) returners — % of committed users who returned on the same day they signed up (PostgreSQL).
**Schema:** `users(id, signup_date)`; `sessions(user_id, occurred_at)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  100.0 * COUNT(DISTINCT s.user_id) / COUNT(DISTINCT u.id) AS day0_return_pct
FROM users u
LEFT JOIN sessions s
  ON s.user_id = u.id
 AND s.occurred_at::date = u.signup_date
GROUP BY 1
ORDER BY 1;
```
**Explanation:** The equality `occurred_at::date = signup_date` isolates same-day activity; counting distinct session users over distinct signups yields a same-day returner rate.

**Alt1:** Day-0 returners by event count vs distinct user count — swap `COUNT(DISTINCT s.user_id)` for `COUNT(s.session_id)` to get event-per-user ratio; the former normalizes by users, the latter measures engagement depth, and they answer different questions (did they come back vs how much did they do).

## Q7: Same day-0 query in MySQL flavor (DATEDIFF to zero).
**Schema:** `users(id, signup_date)`; `sessions(user_id, occurred_at)`.
**Query:**
```sql
SELECT
  DATE_FORMAT(u.signup_date, '%Y-%m-01')                   AS cohort_month,
  COUNT(DISTINCT s.user_id) / COUNT(DISTINCT u.id)         AS day0_return_pct
FROM users u
LEFT JOIN sessions s
  ON s.user_id = u.id
 AND DATEDIFF(DATE(s.occurred_at), u.signup_date) = 0
GROUP BY 1
ORDER BY 1;
```
**Explanation:** `DATEDIFF(DATE(occurred_at), signup_date) = 0` pins the window exactly to the signup day, independent of timezone drift in the timestamp.

## Q8: Day-1 retention — % of each monthly cohort active exactly one day after signup.
**Schema:** `users(id, signup_date)`; `sessions(user_id, session_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT s.user_id) * 1.0 / COUNT(DISTINCT u.id) AS day1_retention
FROM users u
LEFT JOIN sessions s
  ON s.user_id = u.id
 AND s.session_date = u.signup_date + INTERVAL '1 day'
GROUP BY 1
ORDER BY 1;
```
**Explanation:** A single `session_date` column keeps the join predicate readable; only users with an activity dated exactly `signup + 1` count as retained.

## Q9: Day-7 and Day-28 retention in one pass — same cohort, two windows.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT s7.user_id)  * 1.0 / COUNT(DISTINCT u.id) AS day7_retention,
  COUNT(DISTINCT s28.user_id) * 1.0 / COUNT(DISTINCT u.id) AS day28_retention
FROM users u
LEFT JOIN activity s7
  ON s7.user_id = u.id AND s7.active_date = u.signup_date + INTERVAL '7 days'
LEFT JOIN activity s28
  ON s28.user_id = u.id AND s28.active_date = u.signup_date + INTERVAL '28 days'
GROUP BY 1
ORDER BY 1;
```
**Explanation:** Two left joins with different fixed offsets let you compute both classic gut-check retention numbers in a single GROUP BY with zero pre-aggregation.

**Alt1:** Day-30 instead of day-28 — change only the second literal to `INTERVAL '30 days'`; the same join skeleton handles any exact-day N, and prepackaged analytics tools (e.g. Mixpanel) often report day-30 while product teams quote day-28, so pick the window that matches your funnel meetings.

## Q10: Exact N-day retention parameterized — one query that handles any N via a `CASE` (BigQuery).
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC(u.signup_date, MONTH)          AS cohort_month,
  7                                          AS window_days,
  COUNT(DISTINCT a.user_id) / COUNT(DISTINCT u.id) AS retention_pct
FROM `project.users` u
LEFT JOIN `project.activity` a
  ON a.user_id = u.id
 AND DATE_DIFF(a.active_date, u.signup_date, DAY) = 7
GROUP BY 1
```
**Explanation:** Straightforward exact-day join; to swaption the window just change the literal and the `window_days` constant in lockstep.

**Alt1:** Window-fixed N via a VALUES table — build `SELECT * FROM UNNEST([7,14,28,30]) AS n` and `CROSS JOIN` it so one pass emits all four columns; the join predicate becomes `DATE_DIFF(...) = n`. This is the "parameterized retention" interview favorite because a single scan answers the whole board.

## Q11: Rolling N-day retention — active within any of the last N days (i.e., >= day-N window).
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT u.id) AS rolling_7d_retention
FROM users u
LEFT JOIN activity a
  ON a.user_id = u.id
 AND a.active_date BETWEEN u.signup_date AND u.signup_date + INTERVAL '7 days'
GROUP BY 1
ORDER BY 1;
```
**Explanation:** A `BETWEEN` window (inclusive of day 0) counts a user if they touched the product any time in the first 8 calendar days, not just on a single exact day — smother numbers, common in weekly dashboards.

**Alt1:** Rolling 7-day active in the *following* week — swap the window to `BETWEEN signup + INTERVAL '8 days' AND signup + INTERVAL '14 days'` to measure week-2 rolling retention; the rolling window definition changes the answer far more than the exact-day definition, and teams rarely agree on inclusive vs exclusive.

## Q12: Measure "active within last 7 days" (rolling window ending today) vs exact day-N — show both in one table.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT u.id)  AS active_last7,
  COUNT(DISTINCT a7.user_id) * 1.0 / COUNT(DISTINCT u.id) AS day7_retention
FROM users u
LEFT JOIN activity a
  ON a.user_id = u.id
 AND a.active_date BETWEEN CURRENT_DATE - INTERVAL '6 days' AND CURRENT_DATE
LEFT JOIN activity a7
  ON a7.user_id = u.id
 AND a7.active_date = u.signup_date + INTERVAL '7 days'
GROUP BY 1
ORDER BY 1;
```
**Explanation:** The `active_last7` column counts users active in the now-relative window `[today-6, today]`, while `day7_retention` counts users active exactly 7 days after *their own signup* — two different clocks in one table, and mixing them is one of the most common ways cohort dashboards silently corrupt percentages.

**Alt1:** Now-relative rolling variant — anchor on a fixed `today = CURRENT_DATE`: `a.active_date BETWEEN u.signup_date + INTERVAL '8 days' AND CURRENT_DATE` measures "still active this week", turning the now-relative window into a signup-relative milestone while keeping the join predicate explicit and single-scan.

## Q13: Weekly retention matrix — pivot cohorts (weeks) by age weeks.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('week', u.signup_date)::date AS cohort_week,
  COUNT(DISTINCT CASE WHEN a.active_date BETWEEN u.signup_date AND u.signup_date + INTERVAL '6 days'   THEN a.user_id END) * 1.0 / COUNT(*) AS w0,
  COUNT(DISTINCT CASE WHEN a.active_date BETWEEN u.signup_date + INTERVAL '7 days' AND u.signup_date + INTERVAL '13 days' THEN a.user_id END) * 1.0 / COUNT(*) AS w1
FROM users u
LEFT JOIN activity a ON a.user_id = u.id
GROUP BY 1
ORDER BY 1;
```
**Explanation:** Each `CASE` collapses a non-overlapping 7-day window into a column, giving a running weekly matrix; the pivot is done with conditional aggregates, so no true `PIVOT` syntax is required.

**Alt1:** Use conditional aggregation over a `GENERATE_SERIES` of age weeks instead of hand-writing w0..wN: `CROSS JOIN LATERAL generate_series(0, 7) g(w)` and compare `(a.active_date - u.signup_date) / 7 = g.w`; the matrix then scales to any N columns automatically.

## Q14: Monthly retention matrix pivoted with FILTER (PostgreSQL).
**Schema:** `users(id, signup_date)`; `activity(user_id, active_month)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT u.id)                                AS size,
  COUNT(DISTINCT a.user_id) FILTER (WHERE age_month = 0) * 1.0 / COUNT(DISTINCT u.id) AS m0,
  COUNT(DISTINCT a.user_id) FILTER (WHERE age_month = 1) * 1.0 / COUNT(DISTINCT u.id) AS m1
FROM users u
LEFT JOIN LATERAL (
  SELECT a2.user_id,
         (EXTRACT(YEAR FROM a2.active_month) - EXTRACT(YEAR FROM DATE_TRUNC('month', u.signup_date))) * 12
           + (EXTRACT(MONTH FROM a2.active_month) - EXTRACT(MONTH FROM DATE_TRUNC('month', u.signup_date))) AS age_month
  FROM activity a2 WHERE a2.user_id = u.id
) a ON TRUE
GROUP BY 1
ORDER BY 1;
```
**Explanation:** `FILTER` clauses isolate each age bucket cleanly; the `LATERAL` precomputes `age_month` once per user so the denominator and the four filters agree.

**Alt1:** True `PIVOT` in Snowflake — `PIVOT(COUNT(DISTINCT user_id) FOR age_month IN (0,1,2,3))` over a precomputed CTE; equals the FILTER version but note Snowflake's PIVOT cannot pivot on a plain aggregate with DISTINCT in all versions — the CTE must enforce distinctness first.

## Q15: Output the retention matrix as rows (cohort_month, age_month, retention) — the non-pivoted canonical form.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_month)`.
**Query:**
```sql
WITH monthly AS (
  SELECT user_id, DATE_TRUNC('month', active_month)::date AS m
  FROM activity GROUP BY 1, 2
)
SELECT
  left_join_base.cohort_month,
  COALESCE(m.age_month, 0) AS age_month,
  COUNT(DISTINCT m.user_id) * 1.0 / left_join_base.cohort_size AS retention_pct
FROM (
  SELECT DATE_TRUNC('month', signup_date)::date AS cohort_month, COUNT(*) AS cohort_size
  FROM users GROUP BY 1
) left_join_base
LEFT JOIN LATERAL (
  SELECT mp.user_id,
         (EXTRACT(YEAR FROM mp.m) - EXTRACT(YEAR FROM left_join_base.cohort_month)) * 12
           + (EXTRACT(MONTH FROM mp.m) - EXTRACT(MONTH FROM left_join_base.cohort_month)) AS age_month
  FROM monthly mp WHERE mp.user_id IN (SELECT id FROM users
    WHERE DATE_TRUNC('month', signup_date) = left_join_base.cohort_month)
) m ON TRUE
GROUP BY 1, 2
ORDER BY 1, 2;
```
**Explanation:** Pre-aggregating to monthly user-activity tuples trims the join fan-out, then the age is computed from month-start deltas; row-oriented output is what BI tools pivot on the client side.

## Q16: Churn rate per period — % of prior-period actives who did NOT return this period.
**Schema:** `activity(user_id, active_month)` — `active_month` is month-start `DATE`.
**Query:**
```sql
WITH cur AS (SELECT DISTINCT user_id, active_month FROM activity),
     prev AS (SELECT DISTINCT user_id, active_month FROM activity)
SELECT
  p.active_month AS period,
  COUNT(DISTINCT p.user_id) AS actives_prior,
  COUNT(DISTINCT c.user_id) AS actives_current,
  1.0 - COUNT(DISTINCT c.user_id) / COUNT(DISTINCT p.user_id) AS churn_rate
FROM prev p
LEFT JOIN cur c
  ON c.user_id = p.user_id
 AND c.active_month = p.active_month + INTERVAL '1 month'
GROUP BY 1
ORDER BY 1;
```
**Explanation:** Users present in the prior month only are churned; the self-join maps consecutive `active_month` values, and churn rate = `1 - period-over-period retention`.

**Alt1:** Event-count vs distinct-user flavored churn — if `activity` stores rows per event, run `COUNT(*) vs COUNT(DISTINCT user_id)`; distinct-user churn is the product metric, event-count churn answers volume questions, and they diverge when power users quietly return.

## Q17: Monthly churn computed with a window function instead of a self-join.
**Schema:** `activity(user_id, active_month)`.
**Query:**
```sql
WITH base AS (
  SELECT user_id, active_month,
         LAG(active_month) OVER (PARTITION BY user_id ORDER BY active_month) AS prev_month
  FROM (SELECT DISTINCT user_id, active_month FROM activity) t
)
SELECT
  active_month AS period,
  COUNT(*) FILTER (WHERE prev_month IS NULL) AS new_actives,
  COUNT(*) FILTER (WHERE prev_month = active_month - INTERVAL '1 month') AS retained,
  COUNT(*) FILTER (WHERE prev_month IS NOT NULL)
    - COUNT(*) FILTER (WHERE prev_month = active_month - INTERVAL '1 month') AS churned
FROM base
GROUP BY 1 ORDER BY 1;
```
**Explanation:** `LAG` over distinct `(user_id, month)` marks re-entries, then churned = previous actives minus retained; windowing avoids the self join’s fan-out.

## Q18: Churn vs reactivation split — users who left and came back vs stayed.
**Schema:** `activity(user_id, active_month)`.
**Query:**
```sql
WITH base AS (
  SELECT user_id, active_month,
         LAG(active_month) OVER (PARTITION BY user_id ORDER BY active_month) AS prev_month
  FROM (SELECT DISTINCT user_id, active_month FROM activity) t
)
SELECT
  active_month AS period,
  COUNT(*) FILTER (WHERE prev_month IS NULL) AS new,
  COUNT(*) FILTER (WHERE prev_month = active_month - INTERVAL '1 month') AS continuing,
  COUNT(*) FILTER (WHERE prev_month <> active_month - INTERVAL '1 month') AS reactivated
FROM base
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Three mutually-exclusive states: brand-new, continuing (present last month), and reactivated (gap since last activity); continuing vs reactivated is where a churn metric begins to describe the product lifecycle.

**Alt1:** Recompute churn rate as `continuing/churned` ratio by swapping in `SUM(CASE WHEN ...)`, and add an `is_new` flag per user via `FIRST_VALUE(active_month) OVER (PARTITION BY user_id)`, keeping reactivation numbers stable across both variants.

## Q19: Survival-style query — for each cohort, the % still alive (never churned) vs retained-in-period.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_month)`.
**Query:**
```sql
WITH monthly AS (
  SELECT user_id, DATE_TRUNC('month', active_month)::date AS m
  FROM activity GROUP BY 1, 2
),
ages AS (
  SELECT
    u.id,
    DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
    mm.m,
    (EXTRACT(YEAR FROM mm.m) - EXTRACT(YEAR FROM DATE_TRUNC('month', u.signup_date))) * 12
      + (EXTRACT(MONTH FROM mm.m) - EXTRACT(MONTH FROM DATE_TRUNC('month', u.signup_date))) AS age_month
  FROM users u LEFT JOIN monthly mm ON mm.user_id = u.id
)
SELECT cohort_month, age_month,
       COUNT(*) FILTER (WHERE m IS NOT NULL) * 1.0 / COUNT(*) AS alive_pct
FROM ages
WHERE age_month BETWEEN 0 AND 11
GROUP BY 1, 2
ORDER BY 1, 2;
```
**Explanation:** Survival is the milestone count: anybody with activity in a later month is counted alive at every earlier month; the row-level left join keeps every user in the denominator.

**Alt1:** First-exit survival (time-to-first-churn) — replace the aggregate with `MIN(age_month)` per user for the exit event, then cumulative-count exits up to each age; this measures how fast users stop, complementing the alive curve above.

## Q20: First and last activity date per user — the backbone of every lifetime-churn query.
**Schema:** `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  user_id,
  MIN(active_date) AS first_active,
  MAX(active_date) AS last_active,
  DATE_PART('day', MAX(active_date) - MIN(active_date)) AS span_days
FROM activity
GROUP BY 1;
```
**Explanation:** Two aggregates on the same column give the full activity lifespan in one scan; `span_days` is the naive lifetime before accounting for gaps.

## Q21: Days since last active — the raw material for a dead-user flag.
**Schema:** `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  user_id,
  MAX(active_date)                                             AS last_active,
  CURRENT_DATE - MAX(active_date)                              AS days_since_last_active
FROM activity
GROUP BY 1;
```
**Explanation:** Subtracting dates in Postgres yields integers; rows here correspond one-to-one to users with any activity, so this becomes the join key for the dead-user flag.

## Q22: Dead-user flag — inactive for 90 days out of the last 180.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  u.id,
  CASE
    WHEN MAX(a.active_date) IS NULL THEN 1
    WHEN CURRENT_DATE - MAX(a.active_date) > 90 THEN 1
    ELSE 0
  END AS dead_user          -- 180-day guard in WHERE below
FROM users u
LEFT JOIN activity a
  ON a.user_id = u.id
 AND a.active_date >= CURRENT_DATE - INTERVAL '180 days'
GROUP BY 1;
```
**Explanation:** The 180-day window scopes the scan to recent activity, the 90-day threshold then separates dead (flag=1) from alive; users with zero rows inherit flag=1 by definition.

**Alt1:** Dead-user vs dormant-user where-flag variants — dead = `> 90 days`; dormant = `> 30 AND <= 90`; both computed from the same `days_since_last_active` CASE ladder, but the 180-day guard must be widened to infinity for dormant users so they aren’t misclassified as dead.

## Q23: User lifetime — date of first-to-last active, both in months and days, with a cohort join.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  AVG(DATE_PART('day', a.last_active - a.first_active))          AS avg_lifetime_days,
  AVG(CURRENT_DATE - a.last_active)                              AS avg_days_since_last
FROM users u
JOIN (
  SELECT user_id, MIN(active_date) first_active, MAX(active_date) last_active
  FROM activity GROUP BY 1
) a ON a.user_id = u.id
GROUP BY 1
ORDER BY 1;
```
**Explanation:** Lifetime is first–last; `JOIN` (inner) excludes never-actives so the averages describe engaged users — an intentional scoping decision worth stating in interviews.

**Alt1:** Include never-active in lifetime via `LEFT JOIN` and `COALESCE(first_active, signup_date, CURRENT_DATE)`: swaps the denominator from “engaged users” to “all signups”, changing LTV math materially.

## Q24: Average cohort age in months — how long remains the typical user's active window?
**Schema:** `activity(user_id, active_date)`.
**Query:**
```sql
WITH user_life AS (
  SELECT user_id,
         DATE_PART('year', AGE(MAX(active_date), MIN(active_date))) * 12
           + DATE_PART('month', AGE(MAX(active_date), MIN(active_date))) AS months_alive
  FROM activity GROUP BY 1
)
SELECT
  AVG(months_alive) AS avg_months_alive,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY months_alive) AS median_months_alive
FROM user_life;
```
**Explanation:** `AGE()` yields interval components; averaging and median over the same distribution gives the central tendency of the lifespan, robust to the classic long-tail of actives.

## Q25: Cohort size vs regression line — does cohort size explain retention? Show sizes next to each cohort's day-30 rate.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT u.id) AS cohort_size,
  100.0 * COUNT(DISTINCT a.user_id) / COUNT(DISTINCT u.id) AS day30_ret_pct
FROM users u
LEFT JOIN activity a
  ON a.user_id = u.id
 AND a.active_date = u.signup_date + INTERVAL '30 days'
GROUP BY 1
ORDER BY 1;
```
**Explanation:** Cohort size and its day-30 rate side by side makes the size/quality tradeoff visible — classic acquisition-quality question — before any regression tooling.

## Q26: Rolling (unbounded) retention — has the user EVER returned after signup, flag per user.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  u.id,
  CASE WHEN MAX(a.active_date) > u.signup_date THEN 1 ELSE 0 END AS ever_returned
FROM users u
LEFT JOIN activity a ON a.user_id = u.id
GROUP BY 1;
```
**Explanation:** One aggregate distinguishes "came back after signup" from "only signed up"; almost every dashboard's "rolling retention" is this flag averaged over the cohort.

## Q27: Rolling 3-day, 7-day and 30-day retention in one query using three windows.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT a3.user_id)  / COUNT(DISTINCT u.id) AS ret_3d,
  COUNT(DISTINCT a7.user_id)  / COUNT(DISTINCT u.id) AS ret_7d,
  COUNT(DISTINCT a30.user_id) / COUNT(DISTINCT u.id) AS ret_30d
FROM users u
LEFT JOIN activity a3  ON a3.user_id = u.id  AND a3.active_date  BETWEEN u.signup_date + INTERVAL '1 day'  AND u.signup_date + INTERVAL '3 days'
LEFT JOIN activity a7  ON a7.user_id = u.id  AND a7.active_date  BETWEEN u.signup_date + INTERVAL '1 day'  AND u.signup_date + INTERVAL '7 days'
LEFT JOIN activity a30 ON a30.user_id = u.id AND a30.active_date BETWEEN u.signup_date + INTERVAL '1 day'  AND u.signup_date + INTERVAL '30 days'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Three differently-scoped self-joins share the user join key; each window is subsumed by the next so `3d ⊆ 7d ⊆ 30d` as expected, and one scan of `activity` feeds all three.

**Alt1:** Distinct-user vs distinct-event denominator — swap the numerators to `COUNT(DISTINCT ...)` on `(user_id, active_date)` pairs or keep raw event counts; the event-based numerator reports how active retained users are, the user-based one reports how many returned, and they answer respectively "velocity" and "breadth".

## Q28: Rolling retention where the window start is *not* day 1 — e.g., first 14 days after the 7-day mark.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT a.user_id) / COUNT(DISTINCT u.id) AS rolling_14d_in_week2
FROM users u
LEFT JOIN activity a
  ON a.user_id = u.id
 AND a.active_date BETWEEN u.signup_date + INTERVAL '8 days' AND u.signup_date + INTERVAL '21 days'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Offsetting the `BETWEEN` start opens later life-stage windows; this is the "did a weekly user become engaged in week 2" question, harder than the trivial signup-following window.

## Q29: Time-to-second-session as a retention predictor — median hours between session #1 and #2 per cohort.
**Schema:** `sessions(user_id, session_start)`.
**Query:**
```sql
WITH numbered AS (
  SELECT user_id, session_start,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY session_start) AS session_no
  FROM sessions
)
SELECT
  DATE_TRUNC('month', n1.session_start)::date AS cohort_month,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY n2.session_start - n1.session_start) AS median_time_to_2nd
FROM numbered n1
JOIN numbered n2 ON n2.user_id = n1.user_id AND n2.session_no = 2
WHERE n1.session_no = 1
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Numbered sessions make first and second session addressable; the interval between them correlates with long-term retention and is a favorite growth-lead diagnostics output.

## Q30: Users who never had a second session — return percentage as a "graveyard" KPI.
**Schema:** `sessions(user_id, session_start)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', first_sess)::date AS cohort_month,
  COUNT(*) FILTER (WHERE session_count = 1) * 1.0 / COUNT(*) AS one_session_rate
FROM (
  SELECT user_id, MIN(session_start) AS first_sess, COUNT(*) AS session_count
  FROM sessions GROUP BY 1
) t
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Counting users whose `session_count = 1` over all users reveals the drop-off at session two; the subquery prefilters before the cohort month is derived, keeping it cheap.

## Q31: Same-age cohort comparison — compare March cohort at age 3 with April cohort at age 3, not March vs April absolute.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_month)`.
**Query:**
```sql
WITH ages AS (
  SELECT u.id,
         DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
         (EXTRACT(YEAR FROM a.active_month) - EXTRACT(YEAR FROM DATE_TRUNC('month', u.signup_date))) * 12
           + (EXTRACT(MONTH FROM a.active_month) - EXTRACT(MONTH FROM DATE_TRUNC('month', u.signup_date))) AS age_month
  FROM users u LEFT JOIN activity a ON a.user_id = u.id
)
SELECT cohort_month, age_month,
       COUNT(DISTINCT id) FILTER (WHERE a.active_month IS NOT NULL) * 1.0 / COUNT(DISTINCT id) AS ret_pct
FROM ages a
WHERE age_month = 3
GROUP BY 1, 2 ORDER BY 1;
```
**Explanation:** Filtering to a fixed `age_month` before comparing cohorts neutralizes the calendar aging that sabotages naive month-over-month charts.

**Alt1:** Compare multiple same-age slices at once — `WHERE age_month IN (1,3,6)` turns the single column into a 3-column row per cohort; each cohort then has a full same-age profile, and the interview subtly checks you understand that newer cohorts have no older data.

## Q32: Exclude signup-day activity from day-1 retention to avoid inflating returner rates.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT u.id) AS strict_day1
FROM users u
LEFT JOIN activity a
  ON a.user_id = u.id
 AND a.active_date > u.signup_date
 AND a.active_date <= u.signup_date + INTERVAL '1 day'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Strict inequality keeps signup-day sessions out of day-1; alternately keep `signup <= x <= signup+1` and your day-1 quietly reports ~100% for any product that records a session at signup.

## Q33: Retention by acquisition channel — same matrix, three channels.
**Schema:** `users(id, signup_date, channel)`; `activity(user_id, active_month)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  u.channel,
  COUNT(DISTINCT u.id)                                                        AS size,
  COUNT(DISTINCT CASE WHEN age_month = 0 THEN a.user_id END) * 1.0 / COUNT(DISTINCT u.id) AS m0,
  COUNT(DISTINCT CASE WHEN age_month = 1 THEN a.user_id END) * 1.0 / COUNT(DISTINCT u.id) AS m1
FROM users u
LEFT JOIN LATERAL (
  SELECT a2.user_id,
    ((EXTRACT(YEAR FROM a2.active_month) - EXTRACT(YEAR FROM DATE_TRUNC('month', u.signup_date))) * 12
     + (EXTRACT(MONTH FROM a2.active_month) - EXTRACT(MONTH FROM DATE_TRUNC('month', u.signup_date)))) AS age_month
  FROM activity a2 WHERE a2.user_id = u.id
) a ON TRUE
GROUP BY 1, 2 ORDER BY 1, 2;
```
**Explanation:** The lateral join computes `age_month` per user; grouping by channel splits the matrix and immediately reveals acquisition-quality differences.

**Alt1:** Roll up channel into paid/organic via a `CASE` on `channel IN ('ads','sponsored','partnership')`, and cast channel to a `TYPE`-safe table so typos don't silently create ghost channels.

## Q34: Cohort revenue per active user per month — ARPU matrix.
**Schema:** `users(id, signup_date)`; `payments(user_id, paid_at, amount)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date              AS cohort_month,
  DATE_TRUNC('month', p.paid_at)::date                  AS revenue_month,
  COALESCE(SUM(p.amount), 0) * 1.0
    / NULLIF(COUNT(DISTINCT u.id), 0)                   AS arpu
FROM users u
LEFT JOIN payments p ON p.user_id = u.id
GROUP BY 1, 2 ORDER BY 1, 2;
```
**Explanation:** Splits revenue by both cohort month and revenue month so you can see revenue growing with user age; `NULLIF` guards the division.

## Q35: LTV curve — cumulative cohort revenue per user by age month (revenue attributable to each month of life).
**Schema:** `users(id, signup_date)`; `payments(user_id, paid_at, amount)`.
**Query:**
```sql
WITH monthly AS (
  SELECT
    DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
    DATE_TRUNC('month', p.paid_at)::date     AS rev_month,
    (EXTRACT(YEAR FROM DATE_TRUNC('month', p.paid_at)) - EXTRACT(YEAR FROM DATE_TRUNC('month', u.signup_date))) * 12
      + (EXTRACT(MONTH FROM DATE_TRUNC('month', p.paid_at)) - EXTRACT(MONTH FROM DATE_TRUNC('month', u.signup_date))) AS age_month,
    SUM(p.amount) AS month_rev
  FROM users u LEFT JOIN payments p ON p.user_id = u.id
  GROUP BY 1, 2, 3
)
SELECT cohort_month, age_month,
  SUM(month_rev) OVER (PARTITION BY cohort_month ORDER BY age_month) / cohort_size AS cumulative_ltv_per_user
FROM monthly
JOIN (SELECT DATE_TRUNC('month', signup_date)::date AS cohort_month, COUNT(*) AS cohort_size FROM users GROUP BY 1) c
  USING (cohort_month)
ORDER BY 1, 2;
```
**Explanation:** Running-sum revenue normalized by cohort size produces the LTV curve; age months without revenue simply inherit the prior total thanks to the window ordering.

**Alt1:** Current-LTV variant — restrict `rev_month <= CURRENT_DATE` and change the window frame to `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`; the interview point is that "LTV" claims need an explicit time horizon or they are unbounded and meaningless.

## Q36: Revenue per returning user (RPU) vs new-user revenue split by age.
**Schema:** `users(id, signup_date)`; `payments(user_id, paid_at, amount)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', p.paid_at)::date AS rev_month,
  SUM(CASE WHEN DATE_PART('month', AGE(CURRENT_DATE, u.signup_date)) < 1 THEN p.amount END) AS new_user_rev,
  SUM(CASE WHEN DATE_PART('month', AGE(CURRENT_DATE, u.signup_date)) >= 1 THEN p.amount END) AS returning_rev
FROM payments p JOIN users u ON u.id = p.user_id
GROUP BY 1 ORDER BY 1;
```
**Explanation:** `AGE` in months decides new vs returning at payment time; revenue splits reveal whether monetization comes from acquisition or retention loops.

## Q37: Retention by feature usage — users who used feature X in their first week vs those who didn't.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`, `events(user_id, event_ts, feature)`.
**Query:**
```sql
WITH early_x AS (
  SELECT DISTINCT e.user_id
  FROM events e
  JOIN users u ON u.id = e.user_id
  WHERE e.feature = 'X'
    AND e.event_ts::date BETWEEN u.signup_date AND u.signup_date + INTERVAL '7 days'
)
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  CASE WHEN ex.user_id IS NOT NULL THEN 'used_X_week1' ELSE 'did_not' END AS feature_use,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT u.id) AS day30_ret
FROM users u
LEFT JOIN early_x ex ON ex.user_id = u.id
LEFT JOIN activity a ON a.user_id = u.id AND a.active_date = u.signup_date + INTERVAL '30 days'
GROUP BY 1, 2 ORDER BY 1, 2;
```
**Explanation:** Two flags, two cohorts, same retention funnel; the `early_x` CTE touches only events in the first week so the join stays small.

**Alt1:** Feature used ≥N times instead of ≥1 — replace `DISTINCT` with `COUNT(*) >= 3` inside the CTE; single-use vs power-use feature cohorts diverge in retention and this alternative is the standard "feature quality" interview follow-up.

## Q38: Resurrection detection — users who churned (>90 days inactive) and then returned.
**Schema:** `activity(user_id, active_date)`.
**Query:**
```sql
WITH ordered AS (
  SELECT user_id, active_date,
         LAG(active_date) OVER (PARTITION BY user_id ORDER BY active_date) AS prev_date
  FROM (SELECT DISTINCT user_id, active_date FROM activity) t
)
SELECT
  DATE_TRUNC('month', active_date)::date AS return_month,
  COUNT(*) FILTER (WHERE prev_date IS NOT NULL
                  AND extended_gap >= 90) AS resurrections
FROM (
  SELECT user_id, active_date, prev_date,
         DATE_PART('day', active_date - prev_date) AS extended_gap
  FROM ordered
) g
GROUP BY 1 ORDER BY 1;
```
**Explanation:** A gap ≥90 days between consecutive activities is the resurrect event; the subquery materializes the gap so the `FILTER` can reference it.

## Q39: Resurrection rate for a single cohort — % of users who left and later came back.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
WITH gap AS (
  SELECT user_id,
         DATE_PART('day', active_date - LAG(active_date) OVER (PARTITION BY user_id ORDER BY active_date)) AS gap_days
  FROM (SELECT DISTINCT user_id, active_date FROM activity) t
)
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT u.id) FILTER (WHERE g.gap_days IS NOT NULL AND g.gap_days >= 90) * 1.0
    / COUNT(DISTINCT u.id) AS resurrection_rate
FROM users u LEFT JOIN gap g ON g.user_id = u.id
GROUP BY 1 ORDER BY 1;
```
**Explanation:** One `FILTER` counts users whose activity history contains a 90-day gap; the join handles never-active and single-activity users identically (NULL gap).

## Q40: Survival table construction — cumulative-probability-of-being-active so far, without assuming the cohort.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
WITH monthly AS (
  SELECT user_id, DATE_TRUNC('month', active_date)::date AS m
  FROM activity GROUP BY 1, 2
),
surv AS (
  SELECT
    DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
    (EXTRACT(YEAR FROM a.m) - EXTRACT(YEAR FROM DATE_TRUNC('month', u.signup_date))) * 12
      + (EXTRACT(MONTH FROM a.m) - EXTRACT(MONTH FROM DATE_TRUNC('month', u.signup_date))) AS age_month
  FROM users u LEFT JOIN monthly a ON a.user_id = u.id
)
SELECT cohort_month, age_month,
       COUNT(DISTINCT user_id) FILTER (WHERE age_month IS NOT NULL) * 1.0
         / COUNT(DISTINCT user_id) AS observed_alive_so_far
FROM surv
GROUP BY 1, 2
ORDER BY 1, 2;
```
**Explanation:** Survival is cohort age aligned: for every age month we count how many distinct users appear in any month up to it; dying users stop contributing to later ages, so the curve monotonically decays even though per-age retention jumps around between cohorts.

**Alt1:** True Kaplan-Meier via survival table — sort ages ascending per cohort, apply `product of (1 - deaths_at_age / at_risk_at_age)` using `EXP(SUM(LN(1 - d/r)) OVER (PARTITION BY cohort_month ORDER BY age_month))`, which is the correct at-risk aligned survival curve for engineers who must not hand-wave the "at-risk" set.

## Q41: Construct a retention query from raw events with no users table — derive signups via MIN(event_ts).
**Schema:** `events(user_id, event_ts)` — no separate users table.
**Query:**
```sql
WITH signups AS (
  SELECT user_id, MIN(event_ts)::date AS signup_date
  FROM events GROUP BY 1
)
SELECT
  DATE_TRUNC('month', s.signup_date)::date AS cohort_month,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT s.user_id) AS day30_ret
FROM signups s
LEFT JOIN events a
  ON a.user_id = s.user_id
 AND a.event_ts::date = s.signup_date + INTERVAL '30 days'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** `MIN(event_ts)` per user substitutes for the missing signup column; the join then reuses the same event table, so the query is fully self-contained.

**Alt1:** First-event vs user-metadata signups — when a users table does exist, `COALESCE(u.signup_date, MIN(e.event_ts)::date)` attaches metadata users who never fired an event; distinct-user vs event-count numerators both derive from the same join, but the first requires `DISTINCT`, the second just `COUNT(*)`.

## Q42: Same construction but define "signup" as the first event of a *specific type* (e.g. 'welcome_viewed').
**Schema:** `events(user_id, event_ts, event_name)`.
**Query:**
```sql
WITH signups AS (
  SELECT user_id, MIN(event_ts)::date AS signup_date
  FROM events WHERE event_name = 'welcome_viewed'
  GROUP BY 1
)
SELECT
  DATE_TRUNC('month', s.signup_date)::date AS cohort_month,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT s.user_id) AS day7_ret
FROM signups s
LEFT JOIN events a
  ON a.user_id = s.user_id AND a.event_name = 'page_view'
 AND a.event_ts::date = s.signup_date + INTERVAL '7 days'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** The cohort anchor and the activity definition become independent event filters; renaming the anchor event reshapes the entire cohort identity without touching the retention math.

## Q43: Event-count vs distinct-user retention — numerator swaps on identical joins.
**Schema:** `events(user_id, event_ts)`; `users(id, signup_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT u.id) AS user_based_ret,
  COUNT(*)                      / COUNT(DISTINCT u.id) AS event_based_ret -- events per user per cohort
FROM users u
LEFT JOIN events a
  ON a.user_id = u.id
 AND a.event_ts::date = u.signup_date + INTERVAL '7 days'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Same shape, two metrics: distinct users measure breadth of return, counted events measure depth; `event_based_ret` is strictly ≥ user-based and overstates when one heavy user floods events.

**Alt1:** Distinct `(user_id, event_date)` count as the middle ground — `COUNT(DISTINCT (a.user_id, a.event_ts::date))` counts active user-days, giving a workloads-insensitive depth proxy that is the industry-standard "active days" metric.

## Q44: Percentile of activity — daily active-user percentiles across all users (P50/P90/P99).
**Schema:** `activity(user_id, active_date)`.
**Query:**
```sql
WITH daily AS (
  SELECT user_id, active_date, COUNT(*) AS events_that_day
  FROM activity GROUP BY 1, 2
),
per_user AS (
  SELECT user_id, AVG(events_that_day) AS avg_daily_events
  FROM daily GROUP BY 1
)
SELECT
  PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY avg_daily_events) AS p50,
  PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY avg_daily_events) AS p90,
  PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY avg_daily_events) AS p99
FROM per_user;
```
**Explanation:** Two-step preaggregation avoids percentile-of-raw-events distortion; heavy tail users push P99 far above P50, which is the whole point of examining the distribution.

## Q45: Recency-frequency alignment — percentile rank of users by recency and frequency in one query.
**Schema:** `activity(user_id, active_date)`.
**Query:**
```sql
WITH user_stats AS (
  SELECT user_id,
         COUNT(DISTINCT active_date)           AS active_days,
         CURRENT_DATE - MAX(active_date)       AS days_since_last,
         PERCENT_RANK() OVER (ORDER BY COUNT(DISTINCT active_date))          AS freq_rank,
         PERCENT_RANK() OVER (ORDER BY CURRENT_DATE - MAX(active_date) DESC) AS recency_rank
  FROM activity
  GROUP BY 1
)
SELECT
  user_id, active_days, days_since_last, freq_rank, recency_rank,
  CASE WHEN days_since_last <= 7  AND freq_rank >= 0.8 THEN 'hot'
       WHEN days_since_last <= 30 THEN 'warm'
       ELSE 'cold' END AS segment
FROM user_stats;
```
**Explanation:** Percentile ranks computed in the same scan replace arbitrary thresholds; `PERCENT_RANK` is dialect-proof while `NTILE(4)` is the banded alternative.

**Alt1:** Recency-frequency banding with `NTILE` — `NTILE(4) OVER (ORDER BY days_since_last DESC)` and `NTILE(4) OVER (ORDER BY active_days)`, then label `(RF01, RF11, ...)`; same intent, but NTILE guarantees equal-size bins whereas PERCENT_RANK keeps raw fractions.

## Q46: Monthly retention where a user counts if they have ANY activity in the month (bordered monthly matrix).
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT u.id) AS periodic_monthly_ret
FROM users u
LEFT JOIN activity a
  ON a.user_id = u.id
 AND a.active_date >= DATE_TRUNC('month', u.signup_date)
 AND a.active_date  < DATE_TRUNC('month', u.signup_date) + INTERVAL '1 month'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** An open-ended `[month start, next month)` bracket is a bounded monthly window; unlike exact-day retention, a user active any day of the month counts — the "monthly active" reading of cohort retention.

**Alt1:** Window-cut on the calendar month vs fixed-day chunk — `BETWEEN '2025-03-01' AND '2025-03-31'` is calendar-truncated and drifts by weekday; the signup-relative window above keeps each user's own month anchored, a subtle but interview-relevant distinction.

## Q47: Daily retention at cohort-day resolution when the event table is huge — bucket first, then join.
**Schema:** `users(id, signup_date)`; `events(user_id, event_ts)`.
**Query:**
```sql
WITH days AS (
  SELECT user_id, event_ts::date AS d
  FROM events
  GROUP BY 1, 2
)
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  d.d - u.signup_date                      AS day_number,
  COUNT(DISTINCT d.user_id) * 1.0 / COUNT(DISTINCT u.id) AS ret
FROM users u
LEFT JOIN days d ON d.user_id = u.id
WHERE d.d - u.signup_date BETWEEN 0 AND 30
GROUP BY 1, 2 ORDER BY 1, 2;
```
**Explanation:** Pre-distincting `(user_id, day)` shrinks the join; `d.d - u.signup_date` divides exact-day ages, and the WHERE window caps the explosion to 31 rows per user.

## Q48: Exact-day vs rolling-7-day retention compared in one query to show how the definition shifts numbers.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT e.user_id) * 1.0 / COUNT(DISTINCT u.id) AS exact_day7,
  COUNT(DISTINCT r.user_id) * 1.0 / COUNT(DISTINCT u.id) AS rolling_7d
FROM users u
LEFT JOIN activity e ON e.user_id = u.id AND e.active_date = u.signup_date + INTERVAL '7 days'
LEFT JOIN activity r ON r.user_id = u.id AND r.active_date BETWEEN u.signup_date AND u.signup_date + INTERVAL '7 days'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Side-by-side numbers expose definitional sensitivity; exact-day counts a user only on the mark, rolling accepts any arrival in the window — a bigger, often double-or-more number.

**Alt1:** Rolling window anchor variants — anchor at day 0 (0-7), day 1 (1-8), or day 8 (8-15) each shift the count; state the anchor explicitly in every meeting because "rolling 7-day" alone is ambiguous by up to an entire window width.

## Q49: Retention hint that excludes current partial month from cohort sizes/AU (data-quality trap).
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT u.id)                     AS cohort_size,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT u.id) AS m0_ret
FROM users u
LEFT JOIN activity a ON a.user_id = u.id
WHERE DATE_TRUNC('month', u.signup_date)::date < DATE_TRUNC('month', CURRENT_DATE)::date
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Filtering out the current, incomplete month keeps "m0" cohorts whole; otherwise today’s partially-elapsed cohort drags the first column down and every downstream chart bends.

**Alt1:** Data-sufficiency filter counting full calendar months of life — `WHERE DATE_PART('month', AGE(CURRENT_DATE, signup_date)) >= 1` admits only cohorts that have completed month 0, plus an explicit `signup_date < CURRENT_DATE` guard for clock skew.

## Q50: Average active days per user per cohort in the first 28 days — engagement depth.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT a.active_date) * 1.0 / COUNT(DISTINCT u.id) AS avg_active_days_28
FROM users u
LEFT JOIN activity a
  ON a.user_id = u.id
 AND a.active_date BETWEEN u.signup_date AND u.signup_date + INTERVAL '27 days'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** `COUNT(DISTINCT active_date)` counts user-days, and dividing by user count yields an engagement-depth metric complementary to headcount retention.

**Alt1:** Normalize by cohort size *only* for engaged users — `COUNT(DISTINCT a.active_date) / NULLIF(COUNT(DISTINCT a.user_id), 0)` gives active-days-per-active-user, stripping never-active users from the denominator so the metric measures intensity, not breadth.

## Q51: Retention from a fact table keyed by (user_id, date) instead of an events stream — same math, cleaner scans.
**Schema:** `daily_activity(user_id, active_date)` — one row per user-date; `users(id, signup_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT d.user_id) * 1.0 / COUNT(DISTINCT u.id) AS day1_ret
FROM users u
LEFT JOIN daily_activity d
  ON d.user_id = u.id
 AND d.active_date = u.signup_date + INTERVAL '1 day'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Pre-bucketed user-days make the join trivially one-to-one; the retention math is identical to the events version but the scan is dramatically smaller.

## Q52: Weekly retention cohorts built from daily activity, with week bucketing.
**Schema:** `daily_activity(user_id, active_date)`; `users(id, signup_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('week', u.signup_date)::date AS cohort_week,
  (DATE_PART('day', (DATE_TRUNC('week', d.active_date) - DATE_TRUNC('week', u.signup_date)))::int / 7) AS age_week,
  COUNT(DISTINCT d.user_id) * 1.0 / COUNT(DISTINCT u.id) AS ret
FROM users u
LEFT JOIN daily_activity d ON d.user_id = u.id
GROUP BY 1, 2 ORDER BY 1, 2;
```
**Explanation:** Truncating both dates to week start then dividing the day delta by 7 yields the week age; identical cohort math, week-granular output.

**Alt1:** ISO vs Sunday week truncation — `DATE_TRUNC('week', ...)` respects the server's start-of-week convention while `EXTRACT(ISODOW FROM ...)` normalizes to Monday; state which you mean or weekly cohorts drift by a day across environments.

## Q53: Cohort retention where the definition of "active" is "opened the app" — a WHERE on an event name.
**Schema:** `users(id, signup_date)`; `events(user_id, event_ts, event_name)`.
**Query:**
```sql
WITH opens AS (
  SELECT user_id, event_ts::date AS d
  FROM events WHERE event_name = 'app_open'
  GROUP BY 1, 2
)
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT o.user_id) * 1.0 / COUNT(DISTINCT u.id) AS open_based_day1
FROM users u LEFT JOIN opens o
  ON o.user_id = u.id AND o.d = u.signup_date + INTERVAL '1 day'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Filtering the CTE to `app_open` before the join turns a generic activity table into an opens-only stream; changing one literal redefines the entire KPI.

**Alt1:** Multi-event active definition — `WHERE event_name IN ('app_open','page_view','action_tap')` and dedupe user-days; combining events inflates headcounts but avoids dropping users whose only telemetry isn't an open.

## Q54: Push-notification-influenced retention — compare opt-in vs opt-out cohorts.
**Schema:** `users(id, signup_date, push_opt_in)`; `events(user_id, event_ts)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  u.push_opt_in,
  COUNT(DISTINCT e.user_id) * 1.0 / COUNT(DISTINCT u.id) AS day7_ret
FROM users u LEFT JOIN events e
  ON e.user_id = u.id AND e.event_ts::date = u.signup_date + INTERVAL '7 days'
GROUP BY 1, 2 ORDER BY 1, 2;
```
**Explanation:** Grouping on the boolean attribute forces two retention rows per cohort; an important caveat for the interview: opt-in users are self-selected, so any lift is correlation, not causation.

## Q55: Retention by plan tier at signup — free vs paid cohorts.
**Schema:** `users(id, signup_date, plan)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  u.plan,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT u.id) AS day30_ret
FROM users u LEFT JOIN activity a
  ON a.user_id = u.id AND a.active_date = u.signup_date + INTERVAL '30 days'
WHERE u.plan IN ('free', 'paid')
GROUP BY 1, 2 ORDER BY 1, 2;
```
**Explanation:** Attributes on the user dimension split the cohort cleanly; if `plan` can upgrade later, snapshot at signup or you'll measure post-hoc attribution.

**Alt1:** Latest-plan vs signup-plan retention — join to the newest `plan` via `JOIN LATERAL ... ORDER BY changed_at DESC LIMIT 1`; reported retention differs because paid-upgraders count under their current tier, and the interview buries the difference in the join.

## Q56: Cohort-by-cohort first-week feature adoption — did the user's first-week features predict day-30?
**Schema:** `users(id, signup_date)`; `events(user_id, event_ts, feature)`.
**Query:**
```sql
WITH wk1 AS (
  SELECT e.user_id,
         COUNT(DISTINCT e.feature) AS features_used_wk1
  FROM events e JOIN users u ON u.id = e.user_id
  WHERE e.event_ts::date BETWEEN u.signup_date AND u.signup_date + INTERVAL '7 days'
  GROUP BY 1
)
SELECT
  (CASE WHEN w.features_used_wk1 = 0 THEN '0'
        WHEN w.features_used_wk1 = 1 THEN '1'
        WHEN w.features_used_wk1 = 2 THEN '2'
        ELSE '3+' END) AS features_in_week1,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT w.user_id) AS day30_ret_pct
FROM wk1 w LEFT JOIN activity a
  ON a.user_id = w.user_id AND a.active_date = w.signup_date + INTERVAL '30 days'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** `COUNT(DISTINCT feature)` in the first week is the adoption-shape variable; binning to 0/1/2/3+ turns a raw cardinality into an interpretable curve.

**Alt1:** Feature *set* matched ("used A at least once, B at least 3 times") via `FILTER` clauses; set-cohorts have sharper retention deltas than cardinality bins and are what product managers actually reason about.

## Q57: Denominator discipline — cohort retention must include users with NO activity at all.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT u.id) AS all_users,
  COUNT(DISTINCT a.user_id) AS active_users,
  COUNT(DISTINCT u.id) - COUNT(DISTINCT a.user_id) AS inactive_users
FROM users u
LEFT JOIN activity a
  ON a.user_id = u.id AND a.active_date = u.signup_date + INTERVAL '1 day'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** The left join keeps never-active users out of the numerator automatically; swapping to `INNER JOIN` silently inflates every retention figure and is the classic interview follow-up trap.

**Alt1:** Explicit `COUNT(u.id) FILTER (WHERE a.user_id IS NULL)` for inactive users; the FILTER form is portable to engines without full outer-markers and makes the exclusion visible in the query text.

## Q58: Time-zone normalization — retention joins must book events to the user's local day.
**Schema:** `users(id, signup_date, tz)`; `events(user_id, event_ts)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT e.user_id) * 1.0 / COUNT(DISTINCT u.id) AS day1_ret
FROM users u LEFT JOIN events e
  ON e.user_id = u.id
 AND (e.event_ts AT TIME ZONE 'UTC' AT TIME ZONE u.tz)::date = u.signup_date + INTERVAL '1 day'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Shifting events into `u.tz` before extracting the date aligns cohorts across the globe; UTC-raw dates will mis-classify midnight-adjacent sessions and bend day-0/day-1 retention.

**Alt1:** Store a user-local `date` column at ingest instead — `e.event_ts at user_tz::date` denormalized as `active_date`; the join degrades to `e.active_date = u.signup_date + 1`, sacrificing some purity for large-scale scan speed.

## Q59: Cohort revenue with refunds — net vs gross retention by age.
**Schema:** `users(id, signup_date)`; `payments(user_id, paid_at, amount, refund_amount)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  DATE_PART('month', AGE(p.paid_at, u.signup_date))::int AS age_month,
  SUM(p.amount)                               AS gross,
  SUM(p.amount - COALESCE(p.refund_amount,0)) AS net
FROM users u JOIN payments p ON p.user_id = u.id
GROUP BY 1, 2 ORDER BY 1, 2;
```
**Explanation:** Netting refunds at the row level before summing yields refund-adjusted revenue that matches finance GL; gross-only numbers overstate, and cohort-age buckets reveal refund hot-spots.

## Q60: LTV by acquisition channel with a 180-day window normalization.
**Schema:** `users(id, signup_date, channel)`; `payments(user_id, paid_at, amount)`.
**Query:**
```sql
WITH ltv AS (
  SELECT u.id, u.channel,
         SUM(p.amount) FILTER (WHERE p.paid_at::date <= u.signup_date + INTERVAL '180 days') AS rev_180d
  FROM users u LEFT JOIN payments p ON p.user_id = u.id
  GROUP BY 1, 2
)
SELECT
  channel,
  COUNT(*)                         AS size,
  AVG(COALESCE(rev_180d, 0))       AS avg_ltv_180
FROM ltv GROUP BY 1 ORDER BY 1;
```
**Explanation:** Revenue is summed per user over a 180-day horizon inside the `ltv` CTE, then `AVG` over all cohort users (with `COALESCE` so never-payers count as zero); the bounded horizon keeps channels comparable despite different signup ages.

**Alt1:** Unbounded LTV vs 180-day — unbounded rewards older cohorts (they've had more time to pay); to compare old and new cohorts fairly, cap at the youngest cohort's elapsed days, or report per-month-of-age LTV curves side by side.

## Q61: Retention comparison of two cohorts of equal age with a custom aggregate — portability trap (no FILTER).
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT CASE WHEN a.active_date = u.signup_date + INTERVAL '30 days' THEN a.user_id END)
    * 1.0 / COUNT(DISTINCT u.id) AS day30_ret
FROM users u LEFT JOIN activity a ON a.user_id = u.id
GROUP BY 1 ORDER BY 1;
```
**Explanation:** `CASE`-inside-`COUNT(DISTINCT)` is the most portable conditional-count idiom, identical in meaning to `FILTER` but valid on every engine from SQLite to Oracle.

**Alt1:** `FILTER (WHERE ...)` vs `COUNT(DISTINCT CASE WHEN ...)` — one is cleaner, the other portable; knowing both is the difference between "writes Postgres-only SQL" and "writes SQL someone else can run".

## Q62: Resurrection cohort — users who returned after ≥90 days of inactivity, bucketed by return month.
**Schema:** `activity(user_id, active_date)`.
**Query:**
```sql
WITH gaps AS (
  SELECT
    user_id,
    active_date,
    LAG(active_date) OVER w AS prev_date
  FROM (SELECT DISTINCT user_id, active_date FROM activity) t
  WINDOW w AS (PARTITION BY user_id ORDER BY active_date)
)
SELECT
  DATE_TRUNC('month', g.active_date)::date AS return_month,
  COUNT(DISTINCT g.user_id) FILTER (WHERE DATE_PART('day', g.active_date - g.prev_date) >= 90) AS resurrections
FROM gaps g GROUP BY 1 ORDER BY 1;
```
**Explanation:** Gap ≥90 days between consecutive actives marks a resurrection; aliasing the window (`WINDOW w AS`) makes the intent explicit and the query reusable.

**Alt1:** Time since first ever active as the baseline instead of consecutive gap — `active_date - MIN(active_date) OVER (PARTITION BY user_id)` reclassifies slow-burn users who return after months of absence but were never "active then churned".

## Q63: First and last event per user plus time-to-first-purchase funnel (signup→first payment latency).
**Schema:** `users(id, signup_date)`; `payments(user_id, paid_at, amount)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  AVG(DATE_PART('day', p.first_pay - u.signup_date)) AS avg_days_to_first_payment,
  COUNT(p.user_id) * 1.0 / COUNT(u.id)               AS conversion_to_paid
FROM users u
LEFT JOIN (SELECT user_id, MIN(paid_at) AS first_pay FROM payments GROUP BY 1) p
  ON p.user_id = u.id
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Pre-aggregating the first payment per user keeps the join one-to-one; `conversion_to_paid` + latency describes the revenue funnel far better than either alone.

## Q64: Monthly retention with a 12-month horizon and a CAST to numeric to avoid integer division (the precision trap).
**Schema:** `users(id, signup_date)`; `activity(user_id, active_month)`.
**Query:**
```sql
WITH base AS (
  SELECT u.id,
         DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
         a2.user_id  AS active_user,
         (EXTRACT(YEAR FROM a2.active_month) - EXTRACT(YEAR FROM DATE_TRUNC('month', u.signup_date))) * 12
           + (EXTRACT(MONTH FROM a2.active_month) - EXTRACT(MONTH FROM DATE_TRUNC('month', u.signup_date))) AS age_month
  FROM users u
  LEFT JOIN LATERAL (
    SELECT user_id, DATE_TRUNC('month', active_month)::date AS active_month
    FROM activity WHERE user_id = u.id GROUP BY 1, 2
  ) a2 ON TRUE
)
SELECT cohort_month,
       age_month,
       ROUND(COUNT(DISTINCT active_user)::numeric / NULLIF(COUNT(DISTINCT id)::numeric, 0), 2) AS retention_pct
FROM base
WHERE age_month BETWEEN 0 AND 11
GROUP BY 1, 2 ORDER BY 1, 2;
```
**Explanation:** `age_month` is a derived column in the CTE so the WHERE can reference it; the lateral join keeps activity-user pairs per user, and casting numerator and denominator to `NUMERIC` before dividing prevents integer truncation. `ROUND(..., 2)` fixes presentation and `NULLIF` guards a zero denominator. (Note: `DATE_PART('month', interval)` reads the interval's month component, NOT the count of months — that pitfall is why the age formula recomputes from year/month deltas.)

**Alt1:** Multiply-by-100 + float instead of numeric — `100.0 * COUNT(...) / COUNT(...)`: the `100.0` literal coerces the whole expression to float, which is the standard MySQL-readable trick; numeric is more precise, float is more portable.

## Q65: Rolling retention computed with a window `MIN(active_date)` per user and current-large window.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
WITH first_rets AS (
  SELECT u.id, MIN(a.active_date) AS first_ret
  FROM users u JOIN activity a ON a.user_id = u.id
  WHERE a.active_date > u.signup_date
  GROUP BY 1
)
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(fr.id) * 1.0 / COUNT(u.id) AS ever_returned_rate
FROM users u LEFT JOIN first_rets fr ON fr.id = u.id
GROUP BY 1 ORDER BY 1;
```
**Explanation:** `MIN(active_date)` after signup is the one-number rolling retention — "has the user EVER come back" — and because it is a bare MIN the query survives any event volume.

## Q66: Cross-dialect monthly retention — same query in BigQuery, Snowflake and Postgres conventions.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
-- BigQuery (ANSI DATE_DIFF is direct)
SELECT DATE_TRUNC(signup_date, MONTH) AS cohort_month,
       COUNT(DISTINCT a.user_id) / COUNT(DISTINCT u.id) AS ret
FROM `proj.users` u
LEFT JOIN `proj.activity` a
  ON a.user_id = u.id
 AND DATE_DIFF(a.active_date, u.signup_date, MONTH) BETWEEN 1 AND 2
GROUP BY 1;

-- Postgres (EXTRACT-based age)
SELECT DATE_TRUNC('month', u.signup_date)::date,
       COUNT(DISTINCT a.user_id) / COUNT(DISTINCT u.id) AS ret
FROM users u LEFT JOIN activity a
  ON a.user_id = u.id
 AND (EXTRACT(YEAR FROM a.active_date) - EXTRACT(YEAR FROM u.signup_date)) * 12
   + (EXTRACT(MONTH FROM a.active_date) - EXTRACT(MONTH FROM u.signup_date)) BETWEEN 1 AND 2
GROUP BY 1;

-- Snowflake (MONTHS_BETWEEN)
SELECT DATE_TRUNC('month', u.signup_date) AS cohort_month,
       COUNT(DISTINCT a.user_id) / COUNT(DISTINCT u.id) AS ret
FROM users u LEFT JOIN activity a
  ON a.user_id = u.id
 AND MONTHS_BETWEEN(a.active_date, u.signup_date) BETWEEN 1 AND 2
GROUP BY 1;
```
**Explanation:** Three dialects, one age definition: BigQuery's `DATE_DIFF(..., MONTH)`, Postgres's EXTRACT year*12+month arithmetic, Snowflake's `MONTHS_BETWEEN`; the join filter `BETWEEN 1 AND 2` series is retained retention (age-months 1–2), a fine-grained definition per dialect.

## Q67: Full-cohort age-0 row materialization — rows for users with zero activity in month 0.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  u.id                                     AS user_id,
  EXISTS (SELECT 1 FROM activity a WHERE a.user_id = u.id
          AND a.active_date < DATE_TRUNC('month', u.signup_date) + INTERVAL '1 month') AS active_m0
FROM users u;
```
**Explanation:** `EXISTS` yields a row per user including zero-activity users; coercing the boolean to `1`/`0` (`active_m0::int`) gives numeric materialization ready for a downstream AVG per cohort.

**Alt1:** `EXISTS` vs left-join-`COUNT(DISTINCT ...)` materialization — EXISTS stops at the first matching row (faster on event tables), while join-count scans all matches; both equal for users, not for events.

## Q68: First-event-scanned cohorts vs genuine signups mismatch — retention % where "cohort" = first ever event date, flagged for data-quality.
**Schema:** `events(user_id, event_ts)` only (no users table).
**Query:**
```sql
WITH firsts AS (
  SELECT user_id, MIN(event_ts)::date AS first_event
  FROM events GROUP BY 1
)
SELECT
  DATE_TRUNC('month', f.first_event)::date AS inferred_cohort,
  COUNT(DISTINCT f.user_id)                AS inferred_size,
  COUNT(DISTINCT e.user_id)                AS active_day30
FROM firsts f LEFT JOIN events e
  ON e.user_id = f.user_id
 AND e.event_ts::date = f.first_event + INTERVAL '30 days'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Without a users table the cohort anchor is inferred; any pre-existing users who had silent events inflate `inferred_size` and depress retention — flag the inference in the KPI name so the numbers aren't compared with signup-based cohorts.

**Alt1:** Cross-check inferred vs real: `LEFT JOIN users u ON u.id = f.user_id` and `WHERE u.signup_date IS NULL` isolates phantom users; the row count from that subset tells you trust the inferred cohorts or not.

## Q69: Cumulative retention at month N — % of cohort active in at least one of the first N months.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT u.id) AS ret_in_first_3
FROM users u LEFT JOIN activity a
  ON a.user_id = u.id
 AND a.active_date >  u.signup_date
 AND a.active_date <= u.signup_date + INTERVAL '3 months'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Cumulative never-been-inactive-in-first-N is computed by expanding the window, not by summing exact-day columns — a monotonic curve like this is the classic "have they engaged at least once by month 3".

**Alt1:** Exact-day vs cumulative definition — switch the window to `= signup + N days` and the number collapses to single-day hits; comparing both curves reveals whether "retention" in the report is hit-by-hit or milestone-based.

## Q70: Rolling 28-day retention with the window KEYED to fixed offsets against today (dashboard metric).
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT u.id) AS rolling_28_as_of_today
FROM users u LEFT JOIN activity a
  ON a.user_id = u.id
 AND a.active_date <= CURRENT_DATE
 AND a.active_date >= CURRENT_DATE - INTERVAL '28 days'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** The window anchors on `CURRENT_DATE`, not signup; each progression of cohort_month therefore corresponds to "how sticky is this cohort right now" — a live-monitoring metric, not a life-cycle curve.

## Q71: Cumulative-active-per-day curve — one row per (cohort, age-day) with running unique count.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
WITH base AS (
  SELECT u.id,
         DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
         a.active_date - u.signup_date            AS age_days,
         COUNT(*) FILTER (WHERE a.active_date IS NOT NULL)
            OVER (PARTITION BY u.id ORDER BY a.active_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS first_seen_flag
  FROM users u LEFT JOIN activity a ON a.user_id = u.id
)
SELECT cohort_month, age_days,
       COUNT(DISTINCT id) FILTER (WHERE first_seen_flag = 1) * 1.0 / COUNT(DISTINCT id) AS cum_users_alive
FROM base GROUP BY 1, 2 ORDER BY 1, 2;
```
**Explanation:** A windowed-running row number per user marks their first activity day, and the FILTER counts exactly one per user — the cumulative-active curve — while `COUNT(DISTINCT id)` keeps each cohort sized correctly on every row.

**Alt1:** Running `MAX`-style existing flag instead — `MAX(active_date) OVER (PARTITION BY user_id ORDER BY a.active_date)` marks whether *any* activity happened ≤ today per user; identical curve, more obvious reading for juniors.

## Q72: Percentile of first-return latency — median days to first re-engagement by cohort.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
WITH rets AS (
  SELECT u.id,
         a.active_date - u.signup_date AS days_to_first_return
  FROM users u
  JOIN (SELECT user_id, MIN(active_date) AS active_date
        FROM activity WHERE active_date > (SELECT MIN(signup_date) FROM users)
        GROUP BY 1) a
    ON a.user_id = u.id
 WHERE a.active_date > u.signup_date
)
SELECT DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY r.days_to_first_return) AS median_days_to_return
FROM users u LEFT JOIN rets r ON r.id = u.id
GROUP BY 1 ORDER BY 1;
```
**Explanation:** First post-signup activity minus signup is the return latency; the median per cohort quantifies "how quickly does retention kick in", and the `LEFT JOIN` keeps never-returning users visible as NULLs.

## Q73: Rolling 30-day with string-typed dates (common ingestion flaw) — cast before comparing.
**Schema:** `users(id, signup_date CHAR(10))`; `activity(user_id, active_date CHAR(10))` — dates stored as text.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date::date)::date AS cohort_month,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT u.id) AS day30_ret
FROM users u LEFT JOIN activity a
  ON a.user_id = u.id
 AND a.active_date::date = u.signup_date::date + INTERVAL '30 days'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** `::date` on both sides normalizes string dates before arithmetic; skipping the casts makes the join compare text and quietly fail to match on formats like `YYYY-MM-DD` vs `MM/DD/YYYY`.

**Alt1:** Same fix via `TO_DATE(a.active_date, 'YYYY-MM-DD')` for PostgreSQL and `CAST(active_date AS DATE)` for BigQuery — the explicit format string survives when the column contains mixed layouts, but it's slower; prefer a typed `DATE` column upstream.

## Q74: Decay-curve curve for daily actives — N-day retention for each N in 1..30 in a single pass.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
WITH n_days AS (SELECT generate_series(0, 30) AS n)
SELECT
  n.n                                                        AS day_n,
  COUNT(DISTINCT a.user_id) * 1.0
    / NULLIF(COUNT(DISTINCT u.id), 0)                        AS exact_day_retention
FROM users u
CROSS JOIN n_days n
LEFT JOIN activity a
  ON a.user_id = u.id
 AND a.active_date = u.signup_date + n.n * INTERVAL '1 day'
GROUP BY 1
ORDER BY 1;
```
**Explanation:** `CROSS JOIN generate_series(0,30)` gives one row per user per candidate day-N and the join predicate compares each activity date against `signup + n`; a single scan of activity yields all 31 exact-day retention points, avoiding 31 separate queries.

**Alt1:** Materialized decay curve — run once per day into a table `retention_decay(cohort_month, day_n, retention)` and incrementally refresh only today's cohort; dashboards then read 31 integers instead of rescanning all events, at the cost of staleness by one ingestion lag.

## Q75: Retention attributed to revenue — cohort revenue per retained user (RPU-retention blend).
**Schema:** `users(id, signup_date)`; `payments(user_id, paid_at, amount)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  SUM(p.amount) * 1.0
    / NULLIF(COUNT(DISTINCT a.user_id), 0)  AS revenue_per_active_user,
  SUM(p.amount) * 1.0
    / NULLIF(COUNT(DISTINCT u.id), 0)       AS revenue_per_signup
FROM users u
LEFT JOIN activity a ON a.user_id = u.id AND a.active_date = u.signup_date + INTERVAL '30 days'
LEFT JOIN payments p ON p.user_id = u.id
GROUP BY 1 ORDER BY 1;
```
**Explanation:** The two denominators -- retained users vs all signups -- answer different questions: monetization of the engaged core vs monetization per acquired lead; consistent use distinguishes an RPU dashboard from a CAC dashboard.

**Alt1:** Revenue tied to the retention window — restrict `p.paid_at` to the same 30-day window as retention (`p.paid_at <= u.signup_date + 30d`) to make revenue properly cohort-attributed instead of lifetime-summed.

## Q76: Month-over-month retention for a single cohort in long format with LAG comparison.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_month)`.
**Query:**
```sql
WITH single AS (
  SELECT active_month,
         COUNT(DISTINCT user_id) AS actives
  FROM activity
  WHERE active_month >= '2025-03-01'::date AND active_month < '2025-12-01'::date
  GROUP BY 1
)
SELECT active_month,
       actives,
       LAG(actives) OVER (ORDER BY active_month) AS prev_month,
       actives * 1.0 / NULLIF(LAG(actives) OVER (ORDER BY active_month), 0) AS pct_of_prior
FROM single ORDER BY 1;
```
**Explanation:** A single cohort (mandated by the WHERE window) plus a `LAG` positionally aligns months; the ratio `actives/prev_month` is retention within the cohort, and the `NULLIF` handles the first month's NULL.

## Q77: Exact 30-day cohort lookback that respects month boundaries — "first month complete" guard.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
WITH eligible AS (
  SELECT u.id
  FROM users u
  WHERE u.signup_date < CURRENT_DATE - INTERVAL '30 days'
)
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT u.id) AS day30_ret
FROM eligible u LEFT JOIN activity a
  ON a.user_id = u.id AND a.active_date = u.signup_date + INTERVAL '30 days'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Excluding users younger than the window (ineligible) means every day-30 return has had time to happen; this is the same guard applied to day-N where N=30, extended to any window in a function.

**Alt1:** Guard on the *entire cohort*, not per user — `WHERE DATE_TRUNC('month', u.signup_date) <= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '2 months'`; the per-user guard is more precise, the cohort guard simpler and usually sufficient.

## Q78: Multi-window retention output as one wide row (6 columns: 1d 3d 7d 14d 30d 60d).
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(*)                                    AS size,
  COUNT(f1.user_id) * 1.0 / COUNT(*) AS d1,
  COUNT(f3.user_id) * 1.0 / COUNT(*) AS d3,
  COUNT(f7.user_id) * 1.0 / COUNT(*) AS d7,
  COUNT(f14.user_id) * 1.0 / COUNT(*) AS d14,
  COUNT(f30.user_id) * 1.0 / COUNT(*) AS d30,
  COUNT(f60.user_id) * 1.0 / COUNT(*) AS d60
FROM users u
LEFT JOIN activity f1  ON f1.user_id  = u.id AND f1.active_date  = u.signup_date + INTERVAL '1 day'
LEFT JOIN activity f3  ON f3.user_id  = u.id AND f3.active_date  = u.signup_date + INTERVAL '3 days'
LEFT JOIN activity f7  ON f7.user_id  = u.id AND f7.active_date  = u.signup_date + INTERVAL '7 days'
LEFT JOIN activity f14 ON f14.user_id = u.id AND f14.active_date = u.signup_date + INTERVAL '14 days'
LEFT JOIN activity f30 ON f30.user_id = u.id AND f30.active_date = u.signup_date + INTERVAL '30 days'
LEFT JOIN activity f60 ON f60.user_id = u.id AND f60.active_date = u.signup_date + INTERVAL '60 days'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Six joins, one scan of `activity` each, and one wide row per cohort — the product-team format. Every column follows the honest `retained-users / cohort-size` formula; note that each extra join multiplies scanning cost, so this wide form is benchmarked against the single-pass FILTER variant below.

**Alt1:** Genuine wide pivots via `FILTER` over a precomputed age-days CTE (`COUNT(DISTINCT user_id) FILTER (WHERE d = 1)`) — the filter version scans activity once and is the recommended production variant; the join version above demonstrates why wide tables are both tempting and dangerous.

## Q79: Month-boundary retention with timezone in the definition (age defined by calendar month, not elapsed days).
**Schema:** `users(id, signup_date)`; `events(user_id, event_ts, tz_user)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date            AS cohort_month,
  DATE_TRUNC('month', e.event_ts AT TIME ZONE u.tz_user)::date AS event_month,
  COUNT(DISTINCT e.user_id) * 1.0
    / NULLIF(COUNT(DISTINCT u.id), 0) AS ret
FROM users u LEFT JOIN events e ON e.user_id = u.id
GROUP BY 1, 2 ORDER BY 1, 2;
```
**Explanation:** Truncating events to calendar month in *user* timezones keeps the definition "used this calendar month"; elapsed-days age (`MONTHS_BETWEEN`) would diverge from this by up to ±1 month near boundaries.

**Alt1:** Calendar-month vs rolling-30d for age — the calendar framing is the retention always shown in pitch decks; the rolling-30d is what engineers ship in ETL; state explicitly which resonates with your audience, both are computed side by side in prod.

## Q80: Cohort-acquisition-quality index — cohort size vs day-30 retention combined.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT u.id) AS size,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT u.id) AS day30_ret
FROM users u LEFT JOIN activity a
  ON a.user_id = u.id AND a.active_date = u.signup_date + INTERVAL '30 days'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Size and retention on the same axis — growing size with flat retention signals scaling spend; falling retention at rising size signals acquisition dilution; two numbers, one conversation.

**Alt1:** Normalize retention by cohort size with `(COUNT(DISTINCT a.user_id))::decimal / NULLIF(COUNT(DISTINCT u.id), 0)` cast before division — the explicit `::decimal` kills integer truncation on engines where `100` literals are missing in a codebase.

## Q81: Survival-table construction without LAG — count users still present per age via subqueries.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
WITH ages AS (SELECT DISTINCT u.id, a.active_date::date - u.signup_date AS age_days
              FROM users u JOIN activity a ON a.user_id = u.id)
SELECT age_days,
       (SELECT COUNT(DISTINCT id) FROM ages x WHERE x.age_days <= a.age_days) AS active_since_any_day,
       COUNT(DISTINCT id)                                                     AS active_on_day
FROM ages a GROUP BY 1 ORDER BY 1;
```
**Explanation:** Two correlated subqueries end the reliance on window functions; the left number is monotone (cumulative), the right is the exact-day count — together they demonstrate survival without `LAG`.

**Alt1:** Compare the same numbers with LAG-based window — `MAX(...) OVER (ORDER BY age_days)` gives the running count; window functions be more compact, correlated subqueries more portable, and the interview wants to see you can reason in both.

## Q82: Retention query with a join order trap — big fact table first vs users first.
**Schema:** `users(id, signup_date)` (2M rows); `events(user_id, event_ts)` (2B rows).
**Query:**
```sql
-- Users-first left join (recommended): keeps selectivity hints, scans events once for matching ids.
EXPLAIN SELECT COUNT(DISTINCT e.user_id) * 1.0 / COUNT(DISTINCT u.id) AS ret
FROM users u LEFT JOIN events e
  ON e.user_id = u.id AND e.event_ts::date = u.signup_date + INTERVAL '30 days'
GROUP BY 1;

-- Events-first (trap): filters on signup-derived date before joining users, disables broadcast.
SELECT COUNT(DISTINCT e.user_id) * 1.0 / COUNT(DISTINCT u.id) AS ret
FROM events e LEFT JOIN users u ON u.id = e.user_id
WHERE DATE_PART('year', e.event_ts) = 2025
GROUP BY 1;
```
**Explanation:** The `EXPLAIN` annotated users-first is typically 10x faster because the signup-relative date predicate pushes into an index; the events-first variant scans everything, and the `WHERE year=2025` leaks a calendar dependency into a "cohort-relative" query.

**Alt1:** Pre-filter events per user with a `LATERAL` — `CROSS JOIN LATERAL (SELECT 1 FROM events e WHERE e.user_id = u.id AND ... LIMIT 1)` yields an existence precheck that stops at one row per user instead of joining full fans.

## Q83: Precision of the retention %. Fixed decimal 2 vs float — show the CAST and avoid bank-pack truncation.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  ROUND((COUNT(DISTINCT a.user_id)::numeric / NULLIF(COUNT(DISTINCT u.id), 0)) * 100, 2) AS ret_pct_fixed,
  (COUNT(DISTINCT a.user_id) * 100.0 / NULLIF(COUNT(DISTINCT u.id), 0))                  AS ret_pct_float
FROM users u LEFT JOIN activity a
  ON a.user_id = u.id AND a.active_date = u.signup_date + INTERVAL '30 days'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** `NUMERIC` division is exact decimal arithmetic; `* 100.0` promotes to double, which renders identically for retention but diverges in extreme-tail LTV computations — always CAST denominators in finance-adjacent pipelines.

**Alt1:** Postgres `::decimal(5,2)` cast on the final ratio instead of `ROUND`; both format at publish-time, the difference is client rendering vs server rounding — the rounding must match the consumer's expectation of the KPI.

## Q84: Cohort age definition locked to *full* calendar months for a daily grain retention.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  u.id,
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  a.active_date,
  (EXTRACT(YEAR FROM a.active_date::date) - EXTRACT(YEAR FROM DATE_TRUNC('month', u.signup_date)))
    * 12 + (EXTRACT(MONTH FROM a.active_date::date) - EXTRACT(MONTH FROM DATE_TRUNC('month', u.signup_date))) AS age_month,
  a.active_date - u.signup_date AS age_days
FROM users u LEFT JOIN activity a ON a.user_id = u.id;
```
**Explanation:** Both `age_month` (calendar) and `age_days` (exact) in one row let downstream pipelines choose the grain; locking age-month against the truncated signup month means Jan-31 signups age to Feb-1, not Feb-28, keeping calendar retention internally consistent.

**Alt1:** Age in whole days via `(EXTRACT(EPOCH FROM (a.active_date - u.signup_date)) / 86400)::int` — identical for continuous datasets but explicit about leap seconds and DST in systems that record `timestamptz`; prefer date subtraction on DATE columns for simplicity.

## Q85: Rolling-90-day retention with quarterly seed — a writer's trap with a broken GROUP BY.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
WITH needs_fixing AS (
  SELECT u.id, DATE_TRUNC('quarter', u.signup_date)::date AS cohort_quarter,
         r.active_date AS ret_date
  FROM users u LEFT JOIN activity r
    ON r.user_id = u.id
GROUP BY 1, 2, 3
)
SELECT cohort_quarter,
       COUNT(DISTINCT ret_date) * 1.0 / COUNT(DISTINCT id) AS rolled_90
FROM needs_fixing WHERE ret_date IS NOT NULL GROUP BY 1;
```
**Explanation:** This runs but mis-scopes rolling-90 — the WHERE drops NULL ret_dates so the denominator collapses to active users only; the fix is to drop the WHERE and pinch `ret_date` via join predicate `r.active_date BETWEEN u.signup_date AND u.signup_date + INTERVAL '90 days'`.

**Alt1:** Corrected version — `LEFT JOIN activity r ON r.user_id = u.id AND r.active_date BETWEEN u.signup_date AND u.signup_date + INTERVAL '90 days'` then `COUNT(DISTINCT r.user_id)/COUNT(DISTINCT u.id)`; active-only vs all-users denominators are two different retention lines in any dashboard.

## Q86: Reactivation vs net-retention — monthly re-engagement percentage with a calendar definition.
**Schema:** `activity(user_id, active_month)`.
**Query:**
```sql
WITH base AS (
  SELECT user_id, active_month,
         LAG(active_month) OVER (PARTITION BY user_id ORDER BY active_month) AS prev
  FROM (SELECT DISTINCT user_id, active_month FROM activity) t
)
SELECT active_month,
       COUNT(*) FILTER (WHERE prev IS NULL)                                          AS new_users,
       COUNT(*) FILTER (WHERE AGE(active_month, prev) = INTERVAL '1 month')           AS continuing,
       COUNT(*) FILTER (WHERE prev IS NOT NULL AND AGE(active_month, prev) > INTERVAL '1 month') AS reactivated
FROM base GROUP BY 1 ORDER BY 1;
```
**Explanation:** `AGE(active_month, prev) = INTERVAL '1 month'` is calendar-shipped reactivation logic; skipping a calendar month triggers `AGE > 1 month` and marks a reactivation, exactly mirroring the product month the business ossifies.

**Alt1:** GREATER gap → resurrect vs reactivate split — `AGE > INTERVAL '3 months'` reclassified from reactivated to resurrected; the threshold defines the product's churn definition, two different charts may differ by one `>`.

## Q87: Retention with a "Session-3+ achieves" definition — users with ≥3 sessions in the window.
**Schema:** `users(id, signup_date)`; `sessions(user_id, session_start)`.
**Query:**
```sql
WITH per_user AS (
  SELECT s.user_id,
         COUNT(DISTINCT s.session_start::date) AS sessions_30d
  FROM sessions s
  JOIN users u ON u.id = s.user_id
  WHERE s.session_start::date BETWEEN u.signup_date AND u.signup_date + INTERVAL '30 days'
  GROUP BY 1
)
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT p.user_id) * 1.0 / COUNT(DISTINCT u.id) AS pct_with_3plus_sessions_30d
FROM users u
LEFT JOIN per_user p
  ON p.user_id = u.id
 AND p.sessions_30d >= 3
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Each user's 30-day session count is computed against their own signup-relative window in the `per_user` CTE; the outer join keeps every user in the denominator while `sessions_30d >= 3` marks the "3+ sessions" achievers.

**Alt1:** Threshold variants — `sessions_30d >= 10` instead of `>= 3` re-flags heavy users; counting raw sessions vs distinct session-dates changes the definition from "3 engagements" to "3 distinct days of engagement", a spec-line change that meaningfully moves the KPI.

## Q88: Retention in daily granularity with 30-day lookback but "active" defined the NEXT DAY 00:00-06:00 (night-owl bias).
**Schema:** `activity(user_id, active_date, active_hour)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT a.user_id) * 1.0 / COUNT(DISTINCT u.id) AS late_night_ret_adj
FROM users u LEFT JOIN activity a
  ON a.user_id = u.id
 AND a.active_hour BETWEEN 0 AND 5
 AND a.active_date = u.signup_date + INTERVAL '30 days'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Restricting the window's hours exposes the night-owl bias in day-N retention; a user active 03:00 counts, a user active at 15:00 does not — the interviewer wants to see you scope "active" to an hour basket deliberately instead of assuming.

**Alt1:** Broadcast-safe adjustment `SET TIME ZONE 'UTC'` on the hour extraction so that 00-05 UTC is equal for all users instead of audience-local; the metric's outlier quality losses (bias toward night-shift users) become a documented property, not a hidden bug.

## Q89: Cohort-based LTV with a supply of discounters separated — paid vs discounted revenue per age.
**Schema:** `users(id, signup_date)`; `payments(user_id, paid_at, amount, discount)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  (EXTRACT(YEAR FROM p.paid_at) - EXTRACT(YEAR FROM DATE_TRUNC('month', u.signup_date))) * 12
    + (EXTRACT(MONTH FROM p.paid_at) - EXTRACT(MONTH FROM DATE_TRUNC('month', u.signup_date))) AS age_month,
  SUM(CASE WHEN p.discount = 0 THEN p.amount ELSE 0 END) AS gross_ltv,
  SUM(p.amount - COALESCE(p.discount, 0))                AS net_ltv
FROM users u LEFT JOIN payments p
  ON p.user_id = u.id AND p.paid_at >= DATE_TRUNC('month', u.signup_date)
GROUP BY 1, 2 ORDER BY 1, 2;
```
**Explanation:** Splitting paid vs discounted LTV per age month reveals whether growth comes from price power or promos; the age formula reuses the cross-dialect EXTRACT pattern from earlier, staying consistent across the whole workbook.

**Alt1:** Discount removed from revenue entirely — `SUM(p.amount * (1 - COALESCE(p.discount_rate, 0)))` for rate-coded promos; gross/net definitions are product policy, so surface the exact formula in the column name to head off finance disputes.

## Q90: Median and percentiles of active days by cohort — the right-skew awareness check.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
WITH per_user AS (
  SELECT u.id,
         DATE_TRUNC('month', u.signup_date)::date              AS cohort_month,
         COUNT(DISTINCT a.active_date)                         AS active_days
  FROM users u LEFT JOIN activity a ON a.user_id = u.id
  GROUP BY 1, 2
)
SELECT
  cohort_month,
  COUNT(*)                                                        AS cohort_size,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY active_days)        AS p50_active_days,
  PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY active_days)        AS p90_active_days
FROM per_user
GROUP BY 1
ORDER BY 1;
```
**Explanation:** One `per_user` CTE holds each user's active-day count, then percentile aggregates run per cohort; the mean would be quoted by a naive analyst while P50/P90 reveal the handful of power users inflating averages — the standard engagement-distribution sanity check.

**Alt1:** `MODE()` vs median — some systems expose `APPROX_QUANTILES(active_days, 100)[OFFSET(95)]` (BigQuery); big data benefits from quantile sketches; small postgres cohorts can afford exact `PERCENTILE_CONT`. Prefer the approximate for dashboard tiers.

## Q91: Cohort revenue per retained user with a lookback that separates "existing" from "new" money.
**Schema:** `users(id, signup_date)`; `payments(user_id, paid_at, amount)`.
**Query:**
```sql
WITH p AS (
  SELECT user_id, paid_at, amount,
         SUM(amount) OVER (PARTITION BY user_id ORDER BY paid_at ROWS UNBOUNDED PRECEDING) AS cumulative_rev
  FROM payments
)
SELECT user_id,
       MAX(cumulative_rev) AS lifetime_rev
FROM p GROUP BY 1 HAVING COUNT(*) >= 2;
```
**Explanation:** The windowed cumulative sum with `ROWS UNBOUNDED PRECEDING` tracks how much a user has ever paid, and `HAVING COUNT(*) >= 2` selects payers with repeat purchases — separating existing money from new-money users is precisely this cumulative total.

**Alt1:** First-vs-repeat revenue via `ROW_NUMBER() = 1` running per user — first-payment subset vs repeat subset over the same cumulative; the split arms the cohort analysis with acquisition vs expansion series.

## Q92: Weekly cohort retention matrix (pivot) via FILTER in a clean fashion.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
WITH ages AS (
  SELECT u.id,
         DATE_TRUNC('week', u.signup_date)::date AS cohort_week,
         ((DATE_TRUNC('week', a.active_date)::date - DATE_TRUNC('week', u.signup_date)::date) / 7) AS age_week
  FROM users u LEFT JOIN activity a ON a.user_id = u.id
)
SELECT cohort_week,
       COUNT(DISTINCT id)                                  AS size,
       COUNT(DISTINCT id) FILTER (WHERE age_week = 0) * 1.0 / COUNT(DISTINCT id) AS w0,
       COUNT(DISTINCT id) FILTER (WHERE age_week = 1) * 1.0 / COUNT(DISTINCT id) AS w1,
       COUNT(DISTINCT id) FILTER (WHERE age_week = 2) * 1.0 / COUNT(DISTINCT id) AS w2
FROM ages GROUP BY 1 ORDER BY 1;
```
**Explanation:** `FILTER` over the week-age CTE yields three pivot columns without any PIVOT keyword; the age is `(week-truncated delta / 7)`, so Monday-to-Sunday buckets line up grid-clean.

**Alt1:** Pivot with explicit `CASE`-based conditional aggregates keeps MySQL compatibility — `COUNT(DISTINCT CASE WHEN age_week = 0 THEN id END)` — identical output, and the interviewer sees you balance portability against ergonomics.

## Q93: Retention at month-M from a raw event stream where each row is a session start.
**Schema:** `sessions(user_id, started_at)`; `users(id, signup_date)`.
**Query:**
```sql
WITH sess AS (
  SELECT user_id, DATE_TRUNC('month', started_at)::date AS m
  FROM sessions GROUP BY 1, 2
)
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT s.user_id) * 1.0 / COUNT(DISTINCT u.id) AS m1_ret
FROM users u LEFT JOIN sess s
  ON s.user_id = u.id
 AND s.m = DATE_TRUNC('month', u.signup_date) + INTERVAL '1 month'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Pre-bucketing sessions into monthly user-rows makes the month-1 join a set membership test — cheap even on billions of session rows — and keeps the age arithmetic only on month-starts.

## Q94: Churn-rate calculation where the denominator is "active in the PRIOR period" explicitly.
**Schema:** `activity(user_id, active_month)`.
**Query:**
```sql
WITH prior AS (SELECT DISTINCT user_id, active_month FROM activity),
     current AS (SELECT DISTINCT user_id, active_month FROM activity)
SELECT
  p.active_month AS period,
  COUNT(DISTINCT p.user_id) AS base_prior,
  COUNT(DISTINCT c.user_id) AS returned,
  ROUND(1.0 - COUNT(DISTINCT c.user_id) / NULLIF(COUNT(DISTINCT p.user_id), 0), 4) AS churn
FROM prior p
LEFT JOIN current c
  ON c.user_id = p.user_id
 AND c.active_month = p.active_month + INTERVAL '1 month'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Churn denominator = actives in the prior period, NOT all signups; the LEFT JOIN re-finds them in next period and `1 - returned/prior` yields the loss rate — this is the definition CS and PM teams fight over in every QBR.

**Alt1:** Constant-churn-period assumption — if some months report 35-day periods, churn is being understated; document `period_length_days` on every row or the trending curve drifts.

## Q95: Resurrection after 90-day churn with a cohort-grouped return percentage.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
WITH periods AS (
  SELECT u.id, DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
         MAX(CASE WHEN a.active_date > u.signup_date + INTERVAL '90 days' THEN a.active_date END) AS revived_date
  FROM users u LEFT JOIN activity a ON a.user_id = u.id
  GROUP BY 1, 2
)
SELECT cohort_month,
       COUNT(revived_date) * 1.0 / COUNT(*) AS resurrect_pct
FROM periods GROUP BY 1 ORDER BY 1;
```
**Explanation:** `revived_date` is any activity past the 90-day mark; `COUNT(revived_date)` counts users with such activity, and dividing by the full cohort gives resurrection share — differentiating sales (return after churn) from acquisition (new).

**Alt1:** Resurrection vs new-user split by age — `MIN(CASE WHEN active_date > signup+90d THEN active_date END)` per user taged as resurrection vs `MIN(active_date) = signup` as new; both computed from the same activity join in a single pass.

## Q96: Activity events first-seen-per-user scan — retention from raw events without users dimension.
**Schema:** `events(user_id, event_ts)` only (no users table, no defined signup event).
**Query:**
```sql
WITH first_seen AS (
  SELECT user_id, MIN(event_ts)::date AS signup_date
  FROM events GROUP BY 1
)
SELECT
  DATE_TRUNC('month', f.signup_date)::date AS cohort_month,
  COUNT(DISTINCT e.user_id) * 1.0
    / NULLIF(COUNT(DISTINCT f.user_id), 0)  AS day_1_ret
FROM first_seen f
LEFT JOIN events e
  ON e.user_id = f.user_id
 AND e.event_ts::date = f.signup_date + INTERVAL '1 day'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** The events-table-only construction: `MIN(event_ts)` becomes signup, and the very same table re-joins as activity; note the caveat — a user's first event may predate their signup event, so `MIN` over all event types is a proxy, not a fact.

**Alt1:** First-seen restricted to key event (`WHERE event_name IN ('signup_complete')`) to reconstruct actual signup dates from a firehose; looser definitions inflate cohorts with pre-signup activity and depress day-1 retention.

## Q97: Cohort-size rollup to overall LTV risk — the aggregation nuance on the denominator.
**Schema:** `users(id, signup_date)`; `payments(user_id, paid_at, amount)`; `activity(user_id, active_date)`.
**Query:**
```sql
SELECT
  DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
  COUNT(DISTINCT u.id)                      AS cohort_size,
  SUM(COALESCE(p.amount, 0))                AS total_rev,
  SUM(COALESCE(p.amount, 0))
    / NULLIF(COUNT(DISTINCT u.id), 0)       AS avg_rev_per_user,
  SUM(COALESCE(p.amount, 0))
    / NULLIF(COUNT(DISTINCT CASE WHEN a.active_date IS NOT NULL THEN u.id END), 0) AS avg_rev_per_active
FROM users u
LEFT JOIN payments p ON p.user_id = u.id
LEFT JOIN activity a ON a.user_id = u.id AND a.active_date = u.signup_date + INTERVAL '30 days'
GROUP BY 1 ORDER BY 1;
```
**Explanation:** The denominator choice — all users vs retained users — transforms avg revenue per user into avg revenue per retained user; both belong in one table because executives quote one and product quotes the other, and the rollup's concentration risk lives in the difference.

**Alt1:** Add a cohort-size rollup warning flag — `CASE WHEN cohort_size < 100 THEN 'noise' ELSE 'reliable' END`; small-cohort retention is unit-meaningless, and flagging it in SQL beats discovering it in a slide.

## Q98: Median lifetime (first-to-last) per cohort — the classic right-skew trap again, in monthly terms.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`.
**Query:**
```sql
WITH lives AS (
  SELECT u.id,
         DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
         (EXTRACT(YEAR FROM MAX(a.active_date)) - EXTRACT(YEAR FROM MIN(a.active_date))) * 12
           + (EXTRACT(MONTH FROM MAX(a.active_date)) - EXTRACT(MONTH FROM MIN(a.active_date))) AS lifetime_months
  FROM users u LEFT JOIN activity a ON a.user_id = u.id
  GROUP BY 1, 2
)
SELECT cohort_month,
       AVG(lifetime_months)                                AS avg_lifetime_months,
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY lifetime_months) AS median_lifetime_months
FROM lives GROUP BY 1 ORDER BY 1;
```
**Explanation:** Mean lifetime is skewed by a few long-lived power users; the median describes the typical user, and the gap between the two is itself a product insight (how concentration-dependent is retention?).

**Alt1:** Cap lifetime at cohort age (`min(lifetime, months_since_cohort)`) — unbounded lifetimes for young cohorts create phantom LTV projections; capping prevents mean-vs-median drama from becoming forecast error.

## Q99: Full retention-dashboard SQL — one script that produces cohort table + churn + LTV in one execution for a BI tool.
**Schema:** `users(id, signup_date, channel)`; `activity(user_id, active_date)`; `payments(user_id, paid_at, amount)`.
**Query:**
```sql
WITH cohorts AS (
  SELECT id, DATE_TRUNC('month', signup_date)::date AS cohort_month, channel
  FROM users
),
ret AS (
  SELECT c.cohort_month, c.channel,
         COUNT(DISTINCT a.user_id) * 1.0 / NULLIF(COUNT(DISTINCT c.id), 0) AS day30_ret
  FROM cohorts c
  LEFT JOIN activity a ON a.user_id = c.id AND a.active_date = DATE_TRUNC('month', c.cohort_month) + INTERVAL '30 days'
  GROUP BY 1, 2
),
rev AS (
  SELECT c.cohort_month, c.channel,
         COALESCE(SUM(p.amount) FILTER (WHERE p.paid_at::date <= c.cohort_month + INTERVAL '90 days'), 0) AS rev_90d
  FROM cohorts c LEFT JOIN payments p ON p.user_id = c.id
  GROUP BY 1, 2
)
SELECT r.cohort_month, r.channel,
       COUNT(DISTINCT c.id) AS size,
       r.day30_ret,
       rv.rev_90d,
       rv.rev_90d / NULLIF(COUNT(DISTINCT c.id), 0) AS ltv_90d
FROM ret r
JOIN rev rv USING (cohort_month, channel)
JOIN cohorts c ON c.cohort_month = r.cohort_month AND c.channel = r.channel
GROUP BY 1, 2, 3, 4, 5, 6 ORDER BY 1, 2;
```
**Explanation:** Three CTEs compute cohort size, retention, and bounded LTV; capping revenue at 90 days — and retention at day-30 for uniform pricing — keeps every old and new cohort comparable on the same dashboard axis.

**Alt1:** Dashboard-parameterized — wrap in a `WITH p AS (SELECT current_date - INTERVAL '365 days' AS lookback)` and filter cohorts; onboarding "last 12 months of cohorts" is the standard BI ask, and a one-line CTE addition turns research SQL into a served dashboard.

## Q100: The Master Retention Audit — a single query that surfaces every denominator/definition inconsistency in one pass.
**Schema:** `users(id, signup_date)`; `activity(user_id, active_date)`; `payments(user_id, paid_at)`.
**Query:**
```sql
WITH coverage AS (
  SELECT
    COUNT(*)                                        AS registered_users,
    COUNT(a.user_id)                               AS active_w_users,
    COUNT(*) - COUNT(a.user_id)                    AS zero_activity_users
  FROM users u
  LEFT JOIN (SELECT DISTINCT user_id FROM activity) a ON a.user_id = u.id
),
dupes AS (
  SELECT COUNT(*) AS dupe_pairs
  FROM (SELECT user_id, active_date, COUNT(*) AS c
        FROM activity GROUP BY 1, 2 HAVING COUNT(*) > 1) z
),
recency AS (SELECT MAX(active_date) AS max_active FROM activity)
SELECT
  CASE
    WHEN c.zero_activity_users > 0 THEN 'users-without-activity'
    WHEN r.max_active < CURRENT_DATE - 365 THEN 'stale-data'
    WHEN d.dupe_pairs > 0 THEN 'duplicate-user-days'
    ELSE 'clean'
  END AS data_warning,
  c.registered_users,
  c.active_w_users,
  c.zero_activity_users,
  d.dupe_pairs,
  r.max_active
FROM coverage c CROSS JOIN dupes d CROSS JOIN recency r;
```
**Explanation:** A single aggregate pass checks the four classic retention killers: users with zero activity (dead weight in the denominator), duplicate user-days (inflated numerators), and stale data (whole table predates expectations); each check reads the same fact table once via pre-aggregated CTEs.

**Alt1:** Definition-hygiene cross-check — verify `active_date IS NOT NULL AND signup_date IS NOT NULL` reach zero missing before trusting any chart; the audit query (built above) is the first artifact to run after any ETL change, precisely because retention percentages silently absorb bad denominators.
