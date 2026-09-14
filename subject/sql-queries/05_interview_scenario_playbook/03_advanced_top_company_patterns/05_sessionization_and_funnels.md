# Sessionization and Funnel Analysis — 100 Interview Q&A

## Q1: Scenario: Given a table of page-view events, split the raw stream into per-user sessions where a gap of more than 30 minutes opens a new session. Assign each event a session number.

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
SELECT user_id, ts, event,
       SUM(new_session) OVER w AS session_id
FROM (
  SELECT user_id, ts, event,
         CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
              THEN 1 ELSE 0 END AS new_session
  FROM events
) t
WINDOW w AS (PARTITION BY user_id ORDER BY ts ROWS UNBOUNDED PRECEDING);
```
**Explanation:** A LAG flag marks each event that is more than 30 minutes after its predecessor, then a running SUM converts those 0/1 flags into a 1-based session id per user.

**Alt1:** Use `EXTRACT(EPOCH FROM (ts - LAG(ts) OVER ...)) > 1800` instead of `INTERVAL '30 minutes'` if the engine stores ts differences as numeric seconds (e.g. MySQL/BigQuery UNIX_SECONDS).

**Alt2:** `COUNT(CASE WHEN ts - LAG(ts) OVER (...) > INTERVAL '30 minutes' THEN 1 END) OVER w` — using COUNT of flags yields the same session id while being portable across Postgres/MySQL dialects.

## Q2: Scenario: Assign each event a global session id that encodes both the user and session (e.g. `u123-s1`) so downstream tables can join on a single key.

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
SELECT user_id, ts, event,
       user_id || '-s' ||
       SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS session_key
FROM events;
```
**Explanation:** The running SUM of gap flags gives the per-user session number, and string concatenation builds a globally unique `user-session` key.

## Q3: Scenario: Events arrive out of order within the same user. Recompute session boundaries after first sorting by timestamp, and note why order keeps changing the answer.

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR, ingestion_ts TIMESTAMP)

**Query:**
```sql
WITH sorted AS (
  SELECT user_id, ts, event
  FROM events
  ORDER BY user_id, ts
)
SELECT *,
  SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
           THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS session_id
FROM sorted;
```
**Explanation:** Session membership depends entirely on the sorted `ts` sequence, so out-of-order inserts can shift boundaries; a stable sort or a dedupe-by-(user,ts) step is required before computing flags.

**Alt1:** Replace the CTE sort with `ORDER BY user_id, ts, ingestion_ts` inside each window so ties resolve deterministically.

## Q4: Scenario: Instead of computing a session number with window functions, build sessions with a recursive CTE that walks a user's event sequence and cuts a new session only when the 30-minute gap is exceeded.

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH RECURSIVE seq AS (
  SELECT user_id, ts, event,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY ts) AS rn
  FROM events
),
walk AS (
  SELECT user_id, ts, event, rn, 1 AS session_id,
         ts AS session_start
  FROM seq WHERE rn = 1
  UNION ALL
  SELECT s.user_id, s.ts, s.event, s.rn,
         CASE WHEN s.ts - w.session_start > INTERVAL '30 minutes'
              THEN w.session_id + 1 ELSE w.session_id END,
         CASE WHEN s.ts - w.session_start > INTERVAL '30 minutes'
              THEN s.ts ELSE w.session_start END
  FROM seq s JOIN walk w ON s.user_id = w.user_id AND s.rn = w.rn + 1
)
SELECT * FROM walk ORDER BY user_id, ts;
```
**Explanation:** The recursion carries the last session start forward and bumps the session id whenever the current event is more than 30 minutes past it, giving the same result as the LAG/SUM approach using only procedural comparison.

**Alt1:** The window-function SUM-of-flags is preferred on big data (single pass, parallel-safe); the recursive version is a good correctness check but slow on millions of events.

## Q5: Scenario: For each session produced by the gap method, compute its start time, end time, and duration in minutes.

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH flagged AS (
  SELECT user_id, ts,
         SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS session_id
  FROM events
)
SELECT user_id, session_id,
       MIN(ts) AS session_start,
       MAX(ts) AS session_end,
       EXTRACT(EPOCH FROM (MAX(ts) - MIN(ts))) / 60.0 AS duration_minutes
FROM flagged
GROUP BY user_id, session_id;
```
**Explanation:** Once events are grouped by (user, session_id), MIN/MAX timestamps are the session bounds and their difference is the total active duration, ignoring idle gaps inside the session.

**Alt1:** Derive duration from `SUM(LEAD(ts) - ts)` over the raw stream and skip the grouping entirely if you need precise per-gap dwell rather than wall-clock bounds.

## Q6: Scenario: Count the number of events per session and use it to classify sessions as a single event vs. multi-event sessions.

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH sessions AS (
  SELECT user_id,
         SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS session_id,
         event
  FROM events
)
SELECT session_id, user_id, COUNT(*) AS event_count,
       CASE WHEN COUNT(*) = 1 THEN 'single' ELSE 'multi' END AS session_type
FROM sessions
GROUP BY user_id, session_id;
```
**Explanation:** Grouping the flagged stream by session and counting rows shows which sessions contain one event vs. many, a common proxy for bounce vs. engaged behavior.

**Alt1:** Compare against a pre-joined sessions table (`sessions.event_count`) when the session log already carries the aggregate, avoiding a second pass over raw events.

## Q7: Scenario: Compute the number of sessions each user had per calendar day.

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH sessions AS (
  SELECT user_id, ts,
         SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS session_id
  FROM events
)
SELECT user_id, ts::date AS day, COUNT(DISTINCT session_id) AS sessions
FROM sessions
GROUP BY user_id, ts::date
ORDER BY day, user_id;
```
**Explanation:** A session that straddles midnight still belongs to the day of its first event because timestamp-to-date cast happens on the event time before grouping by session id.

**Alt1:** Use `LAST_DAY`/`DATE_TRUNC('day', ts)` if the engine doesn't support `::date` casts, keeping the same grouping logic.

## Q8: Scenario: Find each user's average session length and rank users by it to spot the heaviest purchasers' activity.

Schema hint: sessions(user_id INT, session_id INT, session_start TIMESTAMP, session_end TIMESTAMP), events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH sess AS (
  SELECT user_id, session_id,
         EXTRACT(EPOCH FROM (session_end - session_start)) / 60.0 AS len_minutes
  FROM sessions
)
SELECT user_id,
       ROUND(AVG(len_minutes), 2) AS avg_session_minutes,
       COUNT(*) AS num_sessions
FROM sess
GROUP BY user_id
ORDER BY avg_session_minutes DESC;
```
**Explanation:** Averaging bounded session durations per user gives engagement depth, and ordering surfaces power users for closer analysis.

**Alt1:** Replace the sessions join with `MAX(ts) - MIN(ts)` per (user, session) computed inline from events if the sessions table hasn't been materialized yet.

## Q9: Scenario: Build a session-duration histogram to understand whether most sessions are short bounces or long engagements.

Schema hint: sessions(user_id INT, session_id INT, session_start TIMESTAMP, session_end TIMESTAMP)

**Query:**
```sql
SELECT bucket,
       COUNT(*) AS sessions
FROM (
  SELECT CASE WHEN len_minutes < 1 THEN '< 1m'
              WHEN len_minutes < 5 THEN '1-5m'
              WHEN len_minutes < 15 THEN '5-15m'
              WHEN len_minutes < 30 THEN '15-30m'
              ELSE '30m+' END AS bucket
  FROM sessions
  CROSS JOIN LATERAL (SELECT EXTRACT(EPOCH FROM (session_end - session_start)) / 60.0 AS len_minutes) x
) t
GROUP BY bucket
ORDER BY MIN(session_start::timestamp) NULLS FIRST;
```
**Explanation:** Bucketing durations into coarse bins produces a distribution; a realistic web log is strongly right-skewed toward sub-5-minute sessions.

**Alt1:** Rebuild the histogram with `WIDTH_BUCKET(len_minutes, 0, 60, 12)` for fixed integer bins, or `CASE` ranges for arbitrary labels.

## Q10: Scenario: Identify the entry (first) page and exit (last) page of every session.

Schema hint: events(user_id INT, ts TIMESTAMP, page VARCHAR, event VARCHAR)

**Query:**
```sql
WITH s AS (
  SELECT user_id, page,
         SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS session_id,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY ts) AS rn
  FROM events
),
bounds AS (
  SELECT user_id, session_id,
         MIN(ts) AS start_ts, MAX(ts) AS end_ts
  FROM s GROUP BY user_id, session_id
)
SELECT b.user_id, b.session_id,
       (SELECT page FROM s WHERE user_id = b.user_id AND ts = b.start_ts LIMIT 1) AS entry_page,
       (SELECT page FROM s WHERE user_id = b.user_id AND ts = b.end_ts LIMIT 1) AS exit_page
FROM bounds b;
```
**Explanation:** Sessioning the page stream, then taking the page at the min and max event time, yields entry and exit pages; empty pages indicate inaccessible exit tracking (e.g. no `pageleave` payload).

**Alt1:** Use `FIRST_VALUE(page) OVER (PARTITION BY user_id, session_id ORDER BY ts)` with alternative `LAST_VALUE` sorting by ts DESC in one pass, avoiding correlated subqueries.

## Q11: Scenario: Produce a complete ordered page sequence (the click path) inside a single session.

Schema hint: events(user_id INT, ts TIMESTAMP, page VARCHAR)

**Query:**
```sql
WITH s AS (
  SELECT user_id, page,
         SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS session_id
  FROM events
),
numbered AS (
  SELECT user_id, session_id, page,
         ROW_NUMBER() OVER (PARTITION BY user_id, session_id ORDER BY ts) AS step
  FROM s
)
SELECT user_id, session_id,
       ARRAY_AGG(page ORDER BY step) AS clickpath
FROM numbered
GROUP BY user_id, session_id;
```
**Explanation:** Numbering events inside each session and aggregating pages in order reconstructs the full clickpath, suitable for analyzing navigation loops and drop-off patterns.

## Q12: Scenario: Convert the sessioned event stream into a full session log: session window, event count, entry and exit pages, in a single query.

Schema hint: events(user_id INT, ts TIMESTAMP, page VARCHAR)

**Query:**
```sql
WITH s AS (
  SELECT user_id, ts, page,
         SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS session_id
  FROM events
)
SELECT user_id, session_id,
       MIN(ts) AS started_at,
       MAX(ts) AS ended_at,
       COUNT(*) AS events,
       (ARRAY_AGG(page ORDER BY ts))[1] AS entry_page,
       (ARRAY_AGG(page ORDER BY ts))[cardinality(ARRAY_AGG(page ORDER BY ts))] AS exit_page
FROM s
GROUP BY user_id, session_id;
```
**Explanation:** A single GROUP BY over the flagged stream aggregates window bounds, event count and first/last page; the `[1]` and `[cardinality(...)]` subscripting extracts ordered array ends.

**Alt1:** Extract entry/exit with `MIN(page) FILTER (WHERE rn = 1)` per group where rn comes from a precomputed ROW_NUMBER column, avoiding repeated ARRAY_AGG.

## Q13: Scenario: Define a product funnel from ordered page events: view → cart → checkout → purchase. Count users reaching each step.

Schema hint: events(user_id INT, ts TIMESTAMP, step VARCHAR)

**Query:**
```sql
SELECT 'view'    AS step, COUNT(DISTINCT user_id) AS users FROM events WHERE step = 'view'
UNION ALL
SELECT 'cart',    COUNT(DISTINCT user_id) FROM events WHERE step = 'cart'
UNION ALL
SELECT 'checkout', COUNT(DISTINCT user_id) FROM events WHERE step = 'checkout'
UNION ALL
SELECT 'purchase', COUNT(DISTINCT user_id) FROM events WHERE step = 'purchase';
```
**Explanation:** Funnels start as per-step user counts; without ordering guarantee this is a loose "reached" funnel that answers depth-of-pipeline, not true path purity.

**Alt1:** Use `COUNT(DISTINCT user_id) FILTER (WHERE step = 'view')` in one filtered aggregate chain instead of four UNIONed scans for engines that prefer single-pass FILTER clauses.

## Q14: Scenario: Count distinct users who performed view → cart → checkout → purchase strictly in that order, ensuring earlier steps happen before later steps.

Schema hint: events(user_id INT, ts TIMESTAMP, step VARCHAR)

**Query:**
```sql
WITH ordered AS (
  SELECT user_id,
         MAX(ts) FILTER (WHERE step = 'view')     AS t_view,
         MAX(ts) FILTER (WHERE step = 'cart')     AS t_cart,
         MAX(ts) FILTER (WHERE step = 'checkout') AS t_checkout,
         MAX(ts) FILTER (WHERE step = 'purchase') AS t_purchase
  FROM events
  GROUP BY user_id
)
SELECT COUNT(*) AS users
FROM ordered
WHERE t_view < t_cart AND t_cart < t_checkout AND t_checkout < t_purchase;
```
**Explanation:** Taking the latest occurrence of each step per user and demanding strict timestamp inequality enforces order; users who skip or reorder steps are excluded, which is the first pass at a real funnel.

**Alt1:** For multi-attempt journeys, select the FIRST occurrence per step (`MIN(ts)`) so a user who buys after retrying still counts if first-view < first-cart < first-checkout < first-purchase.

## Q15: Scenario: Compute funnel conversion rates step-over-step and overall from the ordered definition in Q14.

Schema hint: events(user_id INT, ts TIMESTAMP, step VARCHAR)

**Query:**
```sql
WITH ordered AS (
  SELECT user_id,
         MAX(ts) FILTER (WHERE step = 'view')     AS t_view,
         MAX(ts) FILTER (WHERE step = 'cart')     AS t_cart,
         MAX(ts) FILTER (WHERE step = 'checkout') AS t_checkout,
         MAX(ts) FILTER (WHERE step = 'purchase') AS t_purchase
  FROM events GROUP BY user_id
),
funnel AS (
  SELECT COUNT(*) FILTER (WHERE t_cart IS NOT NULL)     AS at_cart,
         COUNT(*) FILTER (WHERE t_checkout IS NOT NULL) AS at_checkout,
         COUNT(*) FILTER (WHERE t_purchase IS NOT NULL) AS at_purchase
  FROM ordered WHERE t_view IS NOT NULL
)
SELECT at_cart AS reached_cart,
       at_checkout AS reached_checkout,
       at_purchase AS reached_purchase,
       ROUND(100.0 * at_cart / NULLIF(at_cart,0), 1)  AS pct_view_to_cart,
       ROUND(100.0 * at_checkout / NULLIF(at_cart,0), 1)  AS pct_cart_to_checkout,
       ROUND(100.0 * at_purchase / NULLIF(at_checkout,0), 1) AS pct_checkout_to_purchase
FROM funnel;
```
**Explanation:** Rows of strictly ordered step users drive cascading ratios; NULLIF guards division-by-zero when a step has zero users.

## Q16: Scenario: Find the biggest drop-off step in the funnel per day so the product team knows which day's UX broke.

Schema hint: events(user_id INT, ts TIMESTAMP, step VARCHAR)

**Query:**
```sql
WITH ordered AS (
  SELECT user_id, ts::date AS day,
         MAX(ts) FILTER (WHERE step = 'view') AS t_view,
         MAX(ts) FILTER (WHERE step = 'cart') AS t_cart,
         MAX(ts) FILTER (WHERE step = 'checkout') AS t_checkout,
         MAX(ts) FILTER (WHERE step = 'purchase') AS t_purchase
  FROM events GROUP BY user_id, ts::date
),
per_day AS (
  SELECT day,
         COUNT(*) FILTER (WHERE t_view IS NOT NULL) AS v,
         COUNT(*) FILTER (WHERE t_cart IS NOT NULL) AS c,
         COUNT(*) FILTER (WHERE t_checkout IS NOT NULL) AS k,
         COUNT(*) FILTER (WHERE t_purchase IS NOT NULL) AS p
  FROM ordered GROUP BY day
)
SELECT day,
       ROUND(100.0 * (v - c) / NULLIF(v,0), 1) AS drop_view_to_cart_pct,
       ROUND(100.0 * (c - k) / NULLIF(c,0), 1) AS drop_cart_to_checkout_pct,
       ROUND(100.0 * (k - p) / NULLIF(k,0), 1) AS drop_checkout_to_purchase_pct
FROM per_day
ORDER BY day;
```
**Explanation:** Per-day step counts produce per-step drop percentages; a sudden spike identifies which step and day to investigate.

## Q17: Scenario: Count users who skip a step (e.g. view → checkout without cart) to measure funnel shortcut adoption.

Schema hint: events(user_id INT, ts TIMESTAMP, step VARCHAR)

**Query:**
```sql
WITH ordered AS (
  SELECT user_id,
         MAX(ts) FILTER (WHERE step = 'view')     AS t_view,
         MAX(ts) FILTER (WHERE step = 'cart')     AS t_cart,
         MAX(ts) FILTER (WHERE step = 'checkout') AS t_checkout,
         MAX(ts) FILTER (WHERE step = 'purchase') AS t_purchase
  FROM events GROUP BY user_id
)
SELECT 'skip_cart' AS pattern, COUNT(*) AS users
FROM ordered
WHERE t_view < t_checkout AND t_cart IS NULL
UNION ALL
SELECT 'no_view_start', COUNT(*) FROM ordered
WHERE t_purchase IS NOT NULL AND t_view IS NULL;
```
**Explanation:** Users reaching checkout with no cart step reveal the path a feature like express-buy creates; filtering for missing middle steps quantifies how often the linear funnel is bypassed.

## Q18: Scenario: Measure time-to-convert between the view and purchase events per user, and report the median conversion time.

Schema hint: events(user_id INT, ts TIMESTAMP, step VARCHAR)

**Query:**
```sql
WITH ordered AS (
  SELECT user_id,
         MIN(ts) FILTER (WHERE step = 'view')     AS t_view,
         MIN(ts) FILTER (WHERE step = 'purchase') AS t_purchase
  FROM events GROUP BY user_id
  HAVING MIN(ts) FILTER (WHERE step = 'purchase') IS NOT NULL
)
SELECT ROUND(AVG(EXTRACT(EPOCH FROM (t_purchase - t_view)) / 60.0), 1) AS avg_minutes,
       ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (t_purchase - t_view)) / 60.0), 1) AS median_minutes
FROM ordered;
```
**Explanation:** First-step to purchase-timestamp differences per user give velocity; median is robust to the long tail of users who come back days later.

## Q19: Scenario: Report time-between-steps (cart→checkout, checkout→purchase) to find where users dawdle most.

Schema hint: events(user_id INT, ts TIMESTAMP, step VARCHAR)

**Query:**
```sql
WITH firsts AS (
  SELECT user_id,
         MIN(ts) FILTER (WHERE step = 'cart')     AS t_cart,
         MIN(ts) FILTER (WHERE step = 'checkout') AS t_checkout,
         MIN(ts) FILTER (WHERE step = 'purchase') AS t_purchase
  FROM events GROUP BY user_id
)
SELECT ROUND(AVG(EXTRACT(EPOCH FROM (t_checkout - t_cart)) / 60.0), 1)   AS cart_to_checkout_min,
       ROUND(AVG(EXTRACT(EPOCH FROM (t_purchase - t_checkout)) / 60.0), 1) AS checkout_to_purchase_min
FROM firsts
WHERE t_checkout IS NOT NULL AND t_purchase IS NOT NULL AND t_cart IS NOT NULL;
```
**Explanation:** Differencing consecutive first-step timestamps isolates where users pause; the largest average signals the friction or ambivalence point in the flow.

## Q20: Scenario: Build a session-scoped funnel where every step must occur inside the same 30-minute session.

Schema hint: events(user_id INT, ts TIMESTAMP, step VARCHAR)

**Query:**
```sql
WITH flagged AS (
  SELECT user_id, ts, step,
         SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS session_id
  FROM events
),
sess_funnel AS (
  SELECT user_id, session_id,
         MAX(ts) FILTER (WHERE step = 'view') AS t_view,
         MAX(ts) FILTER (WHERE step = 'cart') AS t_cart,
         MAX(ts) FILTER (WHERE step = 'checkout') AS t_checkout,
         MAX(ts) FILTER (WHERE step = 'purchase') AS t_purchase
  FROM flagged GROUP BY user_id, session_id
)
SELECT COUNT(*) AS sessions, COUNT(*) FILTER (WHERE t_purchase IS NOT NULL) AS completed_sessions,
       ROUND(100.0 * COUNT(*) FILTER (WHERE t_purchase IS NOT NULL) / NULLIF(COUNT(*),0), 1) AS completion_rate_pct
FROM sess_funnel
WHERE t_view IS NOT NULL;
```
**Explanation:** Sessioning first, then funneling within each (user, session), excludes journeys spread over multiple visits and measures single-session conversion — the classic "same-session purchase" metric.

**Alt1:** Grou peer sessions with `GROUP BY user_id, session_id` using an inline session id computed from LAG, or pre-materialize a sessions table and join events to it for hybrid queries.

## Q21: Scenario: Same-session funnel but users may visit two purchase paths; keep the FIRST ordered occurrence of each step within the session.

Schema hint: events(user_id INT, ts TIMESTAMP, step VARCHAR)

**Query:**
```sql
WITH flagged AS (
  SELECT user_id, ts, step,
         SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS session_id
  FROM events
),
firsts AS (
  SELECT DISTINCT ON (user_id, session_id, step) user_id, session_id, ts, step
  FROM flagged
  ORDER BY user_id, session_id, step, ts
)
SELECT user_id, session_id, step, ts
FROM firsts
ORDER BY user_id, session_id, ts;
```
**Explanation:** `DISTINCT ON` collapses repeated steps to their first time per session, so later re-loops of the funnel don't create phantom conversions.

## Q22: Scenario: Compute conversion rate per cohort, where a cohort is users who first appeared in the funnel on a given day.

Schema hint: events(user_id INT, ts TIMESTAMP, step VARCHAR)

**Query:**
```sql
WITH first_seen AS (
  SELECT user_id, MIN(ts)::date AS cohort_day
  FROM events GROUP BY user_id
),
ordered AS (
  SELECT e.user_id, f.cohort_day,
         MAX(e.ts) FILTER (WHERE step = 'view') AS t_view,
         MAX(e.ts) FILTER (WHERE step = 'purchase') AS t_purchase
  FROM events e JOIN first_seen f USING (user_id)
  GROUP BY e.user_id, f.cohort_day
)
SELECT cohort_day,
       COUNT(*) AS cohort_size,
       COUNT(*) FILTER (WHERE t_purchase IS NOT NULL) AS buyers,
       ROUND(100.0 * COUNT(*) FILTER (WHERE t_purchase IS NOT NULL) / NULLIF(COUNT(*),0), 1) AS conversion_pct
FROM ordered
GROUP BY cohort_day
ORDER BY cohort_day;
```
**Explanation:** Tagging each user with the day of their first funnel event defines a cohort; comparing conversion across cohort days reveals whether newer onboarding is improving.

**Alt1:** Use `COUNT(DISTINCT user_id) FILTER (WHERE t_purchase IS NOT NULL) OVER (PARTITION BY cohort_day)` for a windowed single-scan variant, then dedupe to one row per cohort_day.

## Q23: Scenario: Report daily funnel counts (users entering the funnel each day) alongside daily active users so you can normalize conversion by traffic quality.

Schema hint: events(user_id INT, ts TIMESTAMP, step VARCHAR OBJECT), daus(user_id INT, day DATE)

**Query:**
```sql
WITH daily AS (
  SELECT ts::date AS day,
         COUNT(DISTINCT user_id) FILTER (WHERE step = 'view') AS funnel_entered,
         COUNT(DISTINCT user_id) FILTER (WHERE step = 'purchase') AS purchased
  FROM events GROUP BY ts::date
)
SELECT d.day, d.funnel_entered, d.purchased,
       d.dau,
       ROUND(100.0 * d.dau / NULLIF(day1.funnel_entered,0), 1) AS dau_to_entry_pct
FROM (
  SELECT day,
         COUNT(DISTINCT user_id) AS dau
  FROM daus GROUP BY day
) d
JOIN daily day1 USING (day)
ORDER BY day;
```
**Explanation:** Funnel entries sourced from the events table are joined against the DAU table per day; the ratio separates "fewer users" from "worse conversion" explanations for a revenue dip.

## Q24: Scenario: Identify multi-step funnels with multiple valid entry points (e.g. either a 'view' or a deep-link 'cart' counts as entering), and count conversion for each entry type.

Schema hint: events(user_id INT, ts TIMESTAMP, step VARCHAR, entry_point VARCHAR)

**Query:**
```sql
WITH entries AS (
  SELECT user_id, entry_point,
         MAX(ts) FILTER (WHERE step = 'purchase') AS t_purchase,
         MAX(ts) FILTER (WHERE step = 'checkout') AS t_checkout
  FROM events
  GROUP BY user_id, entry_point
)
SELECT entry_point,
       COUNT(*) AS entered,
       COUNT(*) FILTER (WHERE t_checkout IS NOT NULL) AS reached_checkout,
       COUNT(*) FILTER (WHERE t_purchase IS NOT NULL) AS purchased,
       ROUND(100.0 * COUNT(*) FILTER (WHERE t_purchase IS NOT NULL) / NULLIF(COUNT(*),0), 1) AS conversion_pct
FROM entries
GROUP BY entry_point
ORDER BY entered DESC;
```
**Explanation:** Capping the fan-in of the funnel by entry point lets you see which acquisition surface (search, ad, deep link) converts best, since the linear path now branches at the beginning.

## Q25: Scenario: Classify every session's dwell as quick, standard, or engaged based on duration thresholds, then report the mix by day.

Schema hint: sessions(user_id INT, session_id INT, session_start TIMESTAMP, session_end TIMESTAMP)

**Query:**
```sql
WITH classified AS (
  SELECT session_id,
         EXTRACT(EPOCH FROM (session_end - session_start)) / 60.0 AS mins,
         CASE WHEN EXTRACT(EPOCH FROM (session_end - session_start)) / 60.0 < 1 THEN 'quick'
              WHEN EXTRACT(EPOCH FROM (session_end - session_start)) / 60.0 < 10 THEN 'standard'
              ELSE 'engaged' END AS dwell
  FROM sessions
)
SELECT dwell,
       COUNT(*) AS sessions,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM classified
GROUP BY dwell
ORDER BY sessions DESC;
```
**Explanation:** Duration-based thresholds bucket sessions and the windowed SUM over the whole mix gives percentage share per dwell class in one group-by.
## Q26: Scenario: Convert the classified session dwell labels into an ordered severest-first table so you can top-N the worst sessions (shorter dwell, more events).

Schema hint: sessions(user_id INT, session_id INT, session_start TIMESTAMP, session_end TIMESTAMP), events(user_id INT, session_id INT, event VARCHAR)

**Query:**
```sql
WITH m AS (
  SELECT s.user_id, s.session_id,
         EXTRACT(EPOCH FROM (s.session_end - s.session_start)) / 60.0 AS mins,
         COUNT(e.user_id) AS events
  FROM sessions s JOIN events e USING (user_id, session_id)
  GROUP BY s.user_id, s.session_id, s.session_start, s.session_end
)
SELECT user_id, session_id, mins, events,
       CASE WHEN mins < 1 THEN 'quick' WHEN mins < 10 THEN 'standard' ELSE 'engaged' END AS dwell
FROM m
ORDER BY mins ASC, events DESC
LIMIT 10;
```
**Explanation:** Ordering by duration ascending and event count descending surfaces the "quick but busy" sessions that are candidates for bot or scraping behavior follow-up.

## Q27: Scenario: Compute daily active sessions vs. daily active users to understand whether traffic growth is breadth (users) or depth (repeat sessions).

Schema hint: events(user_id INT, ts TIMESTAMP)

**Query:**
```sql
WITH flagged AS (
  SELECT user_id, ts,
         SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS session_id
  FROM events
)
SELECT ts::date AS day,
       COUNT(DISTINCT user_id) AS dau,
       COUNT(DISTINCT (user_id, session_id)) AS das,
       ROUND(100.0 * COUNT(DISTINCT user_id) / NULLIF(COUNT(DISTINCT (user_id, session_id)),0), 2) AS users_per_session_pct
FROM flagged
GROUP BY ts::date
ORDER BY day;
```
**Explanation:** DAS is driven by distinct (user, session) pairs; when DAS grows faster than DAU, the same users are coming back within the day rather than new users arriving.

## Q28: Scenario: Report the average number of sessions per active user per day, bucketed into power-user vs. casual.

Schema hint: events(user_id INT, ts TIMESTAMP)

**Query:**
```sql
WITH flagged AS (
  SELECT user_id, ts,
         SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS session_id
  FROM events
),
per_user AS (
  SELECT ts::date AS day, user_id, COUNT(DISTINCT session_id) AS sessions
  FROM flagged GROUP BY ts::date, user_id
)
SELECT day,
       ROUND(AVG(sessions), 2) AS avg_sessions_per_user,
       COUNT(*) FILTER (WHERE sessions >= 5) AS power_users,
       COUNT(*) FILTER (WHERE sessions = 1) AS casual_users
FROM per_user
GROUP BY day
ORDER BY day;
```
**Explanation:** Summarizing sessions per user per day, then averaging and classifying thresholds, shows the daily distribution of repeat engagement vs. one-and-done usage.

## Q29: Scenario: Build a users table mapping each user to their first and last session dates and total sessions; use it as the base for retention queries.

Schema hint: sessions(user_id INT, session_id INT, session_start TIMESTAMP)

**Query:**
```sql
SELECT user_id,
       COUNT(*) AS total_sessions,
       MIN(session_start) AS first_session,
       MAX(session_start) AS last_session,
       MAX(session_start)::date - MIN(session_start)::date AS days_between_first_and_last
FROM sessions
GROUP BY user_id;
```
**Explanation:** Per-user MIN/MAX over the sessions table establishes the relationship window; retention is then just whether a subsequent session exists within a day offset.

## Q30: Scenario: For every session, find whether the user had a session in the preceding 7 days (returning vs. new-to-period visitor).

Schema hint: sessions(user_id INT, session_id INT, session_start TIMESTAMP)

**Query:**
```sql
WITH ordered AS (
  SELECT user_id, session_id, session_start,
         LAG(session_start) OVER (PARTITION BY user_id ORDER BY session_start) AS prev_start
  FROM sessions
)
SELECT session_id,
       CASE WHEN prev_start IS NOT NULL AND session_start - prev_start <= INTERVAL '7 days'
            THEN 'returning' ELSE 'new' END AS visitor_type
FROM ordered;
```
**Explanation:** Comparing each session to the user's previous session gains the 7-day lookback; sessions with no earlier session, or one older than 7 days, count as new.

**Alt1:** Use `DATE_DIFF(prev_start, session_start, DAY) <= 7` on BigQuery/MySQL for engines that don't support `INTERVAL` on date subtraction.

## Q31: Scenario: Compute 7-day session retention: for users with a baseline session on day D, what fraction have a session on D+7?

Schema hint: sessions(user_id INT, session_id INT, session_start TIMESTAMP)

**Query:**
```sql
WITH base AS (
  SELECT user_id, MIN(session_start)::date AS day0
  FROM sessions GROUP BY user_id
)
SELECT COUNT(DISTINCT b.user_id) AS cohort_size,
       COUNT(DISTINCT CASE WHEN s.session_start::date = b.day0 + 7 THEN s.user_id END) AS retained,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN s.session_start::date = b.day0 + 7 THEN s.user_id END)
                  / NULLIF(COUNT(DISTINCT b.user_id),0), 1) AS retention_pct
FROM base b
LEFT JOIN sessions s ON s.user_id = b.user_id;
```
**Explanation:** Cohorting by first-session day and left-joining all later sessions, the flag for an exact D+7 session yields day-7 retention; the LEFT JOIN keeps non-returners counted in the denominator.

## Q32: Scenario: Detect sessions that might be bots because a single user has an implausibly high number of sessions per day.

Schema hint: sessions(user_id INT, session_id INT, session_start TIMESTAMP)

**Query:**
```sql
WITH per_day AS (
  SELECT user_id, session_start::date AS day, COUNT(*) AS session_count
  FROM sessions GROUP BY user_id, session_start::date
)
SELECT user_id,
       MAX(session_count) AS max_sessions_in_day,
       GREATEST(MAX(session_count), 60) AS threshold
FROM per_day
GROUP BY user_id
HAVING MAX(session_count) >= 60
ORDER BY max_sessions_in_day DESC;
```
**Explanation:** Grouping sessions by user-day surfaces tails of hundreds of sessions; a threshold (≥60/day) flags automation, assuming a human can't legitimately spawn that many 30-min windows.

**Alt1:** Flag by event rate instead: count events per minute per user and bolt on a check like `events/min > 30` for micro-interval scraping bots.

## Q33: Scenario: A user's many short consecutive sessions have the same device and IP. Detect cross-session device anomalies that hint at shared/abusive accounts.

Schema hint: sessions(user_id INT, session_id INT, session_start TIMESTAMP, device VARCHAR, ip VARCHAR)

**Query:**
```sql
SELECT user_id,
       COUNT(DISTINCT device) AS devices,
       COUNT(DISTINCT ip) AS ips,
       COUNT(DISTINCT session_id) AS sessions
FROM sessions
GROUP BY user_id
HAVING COUNT(DISTINCT device) >= 3 OR COUNT(DISTINCT ip) >= 5
ORDER BY sessions DESC;
```
**Explanation:** Aggregating distinct devices/IPs per user and filtering on multi-device or multi-IP use surfaces accounts behaving unlike typical single-person usage, warranting manual review.

## Q34: Scenario: Count unique events vs. unique sessions to show the difference between expandable event counts and session counts (the "expanded counting" pitfall).

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH flagged AS (
  SELECT user_id, ts,
         SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS session_id
  FROM events
)
SELECT COUNT(*) AS raw_events,
       COUNT(DISTINCT (user_id, session_id)) AS distinct_sessions,
       ROUND(100.0 * COUNT(DISTINCT (user_id, session_id)) / NULLIF(COUNT(*),0), 1) AS session_to_event_pct
FROM flagged;
```
**Explanation:** Counting raw rows over-counts (duplicate heartbeats inflate), while distinct (user, session) pairs give the true session count; the ratio quantifies how much a single event uniqueness mistake distorts DAU.

**Alt1:** Validate with `COUNT(DISTINCT CONCAT(user_id, '-', session_id))` where string keys are the only way to express pair-uniqueness in engines without composite DISTINCT support.

## Q35: Scenario: Map every event to a running global session number that continues numbering across users (sessions ordered globally, not per user).

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH flagged AS (
  SELECT user_id, ts, event,
         SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS sess
  FROM events
),
pairs AS (
  SELECT DISTINCT user_id, sess FROM flagged
)
SELECT f.*, ROW_NUMBER() OVER (ORDER BY MIN_PAIR_TS) AS global_session_no
FROM flagged f
JOIN (
  SELECT user_id, sess, MIN(ts) AS pair_start
  FROM flagged GROUP BY user_id, sess
) x USING (user_id, sess)
ORDER BY f.ts;
```
**Explanation:** Unique (user, session) pairs get globally ordered by their earliest event time; a join then stamps every row with the ranking number, giving a monotonically rising session id across the whole system instead of per-user numbering.

## Q36: Scenario: Compute session count in a rolling 7-day window per user so you can spot a ramp-up right before suspicious activity.

Schema hint: sessions(user_id INT, session_start TIMESTAMP)

**Query:**
```sql
SELECT user_id, session_start::date AS day,
       COUNT(*) OVER (PARTITION BY user_id ORDER BY session_start::date
                      RANGE BETWEEN INTERVAL '7 days' PRECEDING AND CURRENT ROW) AS sessions_last_7d
FROM sessions;
```
**Explanation:** A windowed COUNT with a RANGE interval tracks trailing session volume per day; crossing a threshold becomes a trigger for anomaly review.

## Q37: Scenario: Identify sessions whose duration exceeds 6 hours as likely background tab leakage, and exclude them from average duration metrics.

Schema hint: sessions(user_id INT, session_start TIMESTAMP, session_end TIMESTAMP)

**Query:**
```sql
WITH dur AS (
  SELECT *,
         EXTRACT(EPOCH FROM (session_end - session_start)) / 3600.0 AS hours
  FROM sessions
)
SELECT 'all_inclusive' AS bucket, ROUND(AVG(hours),2) AS avg_hours FROM dur
UNION ALL
SELECT 'clean', ROUND(AVG(hours),2)
FROM dur WHERE hours < 6;
```
**Explanation:** Comparisons between the inclusive and truncated averages show how much background-tab leakage would skew engagement reporting; the <6h filter is the sanitized metric.

**Alt1:** Cap instead of truncate using `LEAST(hours, 6)` so leaking sessions stay in the denominator but their inflated tail is clamped at 6h.

## Q38: Scenario: Given heartbeats from an audio player (a pulse every ~10s while playing), sessionize with a 60-second gap rule rather than 30 minutes.

Schema hint: play_heartbeats(user_id INT, ts TIMESTAMP, track_id INT)

**Query:**
```sql
SELECT user_id,
       SUM(CASE WHEN EXTRACT(EPOCH FROM (ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts))) > 60
                THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS listening_session,
       MIN(ts) OVER (PARTITION BY user_id ORDER BY ts ROWS UNBOUNDED PRECEDING) AS session_start
FROM play_heartbeats;
```
**Explanation:** Switching the gap constant from 1800s to 60s makes heartbeat pauses >60s split a listening session, matching media behavior where a radio silence means a real stop.

**Alt1:** Parameterize the gap via a per-row column `gap_seconds` in the ORDER BY clause window so the same query serves audio (60s) and web (1800s) with one code path.

## Q39: Scenario: Video watching sessions: compute the view duration by integrating timestamp gaps between heartbeats, capped at the 60s heartbeat interval.

Schema hint: play_heartbeats(user_id INT, ts TIMESTAMP, position_sec INT)

**Query:**
```sql
WITH gaps AS (
  SELECT user_id,
         ts - LAG(ts) OVER (PARTITION BY user_id, streaming_session ORDER BY ts) AS gap
  FROM play_heartbeats
  -- streaming_session derived by the 30-min gap rule before this CTE
)
SELECT user_id, SUM(gap) AS watched_duration
FROM gaps WHERE gap < INTERVAL '60 seconds'
GROUP BY user_id;
```
**Explanation:** Summing only gaps whose length is under one heartbeat interval (60s) excludes long pauses — like pausing the video — giving a good approximation of wall-clock watching time.

## Q40: Scenario: Build a capstone: retailers' funnel over 3 steps (browse → add_cart → purchase) with per-step raw counts, then daily conversion splits. Part 1 of a coachable capstone.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR, product_id INT)

**Query:**
```sql
WITH ordered AS (
  SELECT user_id, ts::date AS day,
         MAX(ts) FILTER (WHERE event = 'browse')   AS t_browse,
         MAX(ts) FILTER (WHERE event = 'add_cart') AS t_cart,
         MAX(ts) FILTER (WHERE event = 'purchase') AS t_purchase
  FROM web_events GROUP BY user_id, ts::date
)
SELECT day,
       COUNT(*) FILTER (WHERE t_browse IS NOT NULL)  AS browse,
       COUNT(*) FILTER (WHERE t_cart IS NOT NULL)    AS add_cart,
       COUNT(*) FILTER (WHERE t_purchase IS NOT NULL) AS purchase,
       ROUND(100.0 * COUNT(*) FILTER (WHERE t_cart IS NOT NULL) / NULLIF(COUNT(*) FILTER (WHERE t_browse IS NOT NULL),0), 1) AS browse_to_cart_pct,
       ROUND(100.0 * COUNT(*) FILTER (WHERE t_purchase IS NOT NULL) / NULLIF(COUNT(*) FILTER (WHERE t_cart IS NOT NULL),0), 1) AS cart_to_purchase_pct
FROM ordered GROUP BY day ORDER BY day;
```
**Explanation:** Part 1 establishes the funnel skeleton and per-day conversion; later parts layer churn and cohort context on top.

## Q41: Scenario: Capstone part 2 — chain the three-step funnel but require the steps to be in strict chronological order within the same session.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR), sessions(user_id INT, session_id INT, session_start TIMESTAMP)

**Query:**
```sql
WITH flagged AS (
  SELECT w.user_id, w.ts, w.event,
         SUM(CASE WHEN w.ts - s.session_start > INTERVAL '30 minutes' OR s.session_id IS NULL
                  THEN 1 ELSE 0 END) OVER (PARTITION BY w.user_id ORDER BY w.ts) AS session_id
  FROM web_events w LEFT JOIN sessions s USING (user_id)
),
ordered AS (
  SELECT user_id, session_id,
         MIN(ts) FILTER (WHERE event = 'browse')   AS t_browse,
         MIN(ts) FILTER (WHERE event = 'add_cart') AS t_cart,
         MIN(ts) FILTER (WHERE event = 'purchase') AS t_purchase
  FROM flagged GROUP BY user_id, session_id
)
SELECT COUNT(*) FILTER (WHERE t_browse < t_cart AND t_cart < t_purchase) AS strict_funnel_sessions,
       COUNT(*) AS browse_sessions
FROM ordered WHERE t_browse IS NOT NULL;
```
**Explanation:** Part 2 keeps only sessions where browse < add_cart < purchase strictly, collapsing multi-session journeys and showing the strict same-session win rate.

## Q42: Scenario: Capstone part 3 — compute the churn context: of users who entered the funnel this week, how many came back for a session next week (session retention)?

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR), sessions(user_id INT, session_start TIMESTAMP)

**Query:**
```sql
WITH entrants AS (
  SELECT DISTINCT user_id
  FROM web_events
  WHERE event = 'browse'
    AND ts >= date_trunc('week', CURRENT_DATE)
),
next_week AS (
  SELECT DISTINCT s.user_id
  FROM sessions s
  JOIN entrants e USING (user_id)
  WHERE s.session_start >= date_trunc('week', CURRENT_DATE) + INTERVAL '7 days'
)
SELECT (SELECT COUNT(*) FROM entrants) AS funnel_entrants,
       (SELECT COUNT(*) FROM next_week) AS returned_next_week,
       ROUND(100.0 * (SELECT COUNT(*) FROM next_week) / NULLIF((SELECT COUNT(*) FROM entrants),0), 1) AS session_retention_pct;
```
**Explanation:** Entrants defined by a browse event in the current week, then a join to sessions in the following week measures session-level churn, tying funnel performance to retention.

## Q43: Scenario: Users often reorder funnel steps (buy directly from a shared cart link without adding to cart). Quantify how many purchases had a reordered or missing-prefix path.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH ordered AS (
  SELECT user_id,
         ARRAY_AGG(event ORDER BY ts) AS path
  FROM web_events GROUP BY user_id
)
SELECT 'purchase_without_cart' AS pattern, COUNT(*) AS users
FROM ordered WHERE 'purchase' = ANY(path) AND NOT ('add_cart' = ANY(path))
UNION ALL
SELECT 'reordered_purchase', COUNT(*)
FROM ordered WHERE 'purchase' = ANY(path) AND 'add_cart' = ANY(path)
         AND array_position(path, 'purchase') < array_position(path, 'add_cart');
```
**Explanation:** Materializing each user's event path as an ordered array makes step checks trivial: missing prefixes, or purchasing before the canonical cart step, identify the non-linear purchase paths.

## Q44: Scenario: For a funnel with 4 steps, compute the exact % of users who complete step N having completed all earlier steps, i.e. the conditional per-step completion.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH h AS (
  SELECT user_id,
         MAX(ts) FILTER (WHERE event = 'step1') AS t1,
         MAX(ts) FILTER (WHERE event = 'step2') AS t2,
         MAX(ts) FILTER (WHERE event = 'step3') AS t3,
         MAX(ts) FILTER (WHERE event = 'step4') AS t4
  FROM web_events GROUP BY user_id
)
SELECT ROUND(100.0 * COUNT(*) FILTER (WHERE t1 < t2 AND t2 < t3 AND t3 < t4) / NULLIF(COUNT(*) FILTER (WHERE t1 IS NOT NULL),0), 1) AS pct_all_4,
       ROUND(100.0 * COUNT(*) FILTER (WHERE t1 < t2 AND t2 < t3) / NULLIF(COUNT(*) FILTER (WHERE t1 IS NOT NULL AND t2 IS NOT NULL),0), 1) AS pct_2_of_4
FROM h;
```
**Explanation:** Both whole-funnel completion and stage-2-of-4 are computed from timestamp-ordered flags in one pass; a denominator of 'has t1' keeps drop semantics consistent.

## Q45: Scenario: Predict step-one-to-step-two conversion with a fallback: if the user is on mobile, step order may differ. Compute mobile-only funnel metrics separately.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR, platform VARCHAR)

**Query:**
```sql
WITH mobile AS (
  SELECT user_id,
         MAX(ts) FILTER (WHERE event = 'step1') AS t1,
         MAX(ts) FILTER (WHERE event = 'step2') AS t2
  FROM web_events WHERE platform = 'mobile'
  GROUP BY user_id
)
SELECT COUNT(*) AS mobile_users,
       COUNT(*) FILTER (WHERE t2 > t1) AS completed_in_order,
       ROUND(100.0 * COUNT(*) FILTER (WHERE t2 > t1) / NULLIF(COUNT(*),0), 1) AS mobile_conversion_pct
FROM mobile WHERE t1 IS NOT NULL;
```
**Explanation:** Filtering the funnel to the mobile cohort before ordering keeps platform-specific flows (e.g. no cart page) from contaminating the shared metric.

## Q46: Scenario: Compute the max streak of consecutive days with at least one session per user (session-based activity streak).

Schema hint: sessions(user_id INT, session_start TIMESTAMP)

**Query:**
```sql
WITH days AS (
  SELECT DISTINCT user_id, session_start::date AS day
  FROM sessions
),
grp AS (
  SELECT user_id, day,
         day - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day) AS grp
  FROM days
)
SELECT user_id, MAX(day_count) AS max_streak
FROM (
  SELECT user_id, grp, COUNT(*) AS day_count
  FROM grp GROUP BY user_id, grp
) s GROUP BY user_id ORDER BY max_streak DESC;
```
**Explanation:** Subtracting a row number (dense day sequence) from the calendar date groups contiguous runs into a constant; the max run length per user is their longest streak.

**Alt1:** Replace with an `EXTRACT(EPOCH) / 86400` numeric-day comparison for engines without native date arithmetic.

## Q47: Scenario: Return from a session-null perspective: compute the average gap between consecutive sessions per user to model churn risk from inactivity.

Schema hint: sessions(user_id INT, session_start TIMESTAMP)

**Query:**
```sql
WITH gaps AS (
  SELECT user_id, session_start,
         session_start - LAG(session_start) OVER (PARTITION BY user_id ORDER BY session_start) AS gap
  FROM sessions
)
SELECT user_id,
       ROUND(AVG(EXTRACT(EPOCH FROM gap) / 86400.0), 1) AS avg_days_between_sessions,
       MAX(EXTRACT(EPOCH FROM gap) / 86400.0) AS max_gap_days
FROM gaps WHERE gap IS NOT NULL
GROUP BY user_id ORDER BY avg_days_between_sessions DESC;
```
**Explanation:** Gaps between consecutive sessions give a churn-risk signal; large average or maximum gaps flag users about to lapse into inactivity.

**Alt1:** Express the same with `DATEDIFF(day, LAG(session_start)...)` on MySQL/BigQuery where date subtraction yields an integer rather than an interval.

## Q48: Scenario: Assigned a session to events but two adjacent sessions resolve to the same session id because timestamps tied. Make the split deterministic by ingesting a monotonic run counter.

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR, seq INT)

**Query:**
```sql
SELECT user_id, ts, event,
       SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts, seq) > INTERVAL '30 minutes'
                THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts, seq) AS session_id
FROM events;
```
**Explanation:** Adding a sequence column to both ORDER BY clauses breaks timestamp ties deterministically so session assignment no longer depends on physical row order.

## Q49: Scenario: Split by an explicit inactivity marker instead of a time gap: some apps emit a `pause` event. Build sessions cut on pause rather than 30-minute silence.

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
SELECT user_id, ts, event,
       SUM(CASE WHEN event = 'pause' THEN 1 ELSE 0 END)
            OVER (PARTITION BY user_id ORDER BY ts ROWS UNBOUNDED PRECEDING) AS session_id
FROM events
WHERE event <> 'pause';
```
**Explanation:** Using the pause event itself as the boundary flag gives an app-defined session, and filtering pauses out of the output keeps the stream clean.

## Q50: Scenario: Two users share the same underlying visit but a single-page app emits a burst of 200 synthetic 'view' events per second. Aggregate them into one representative event per second before sessionizing.

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH dedup AS (
  SELECT user_id, DATE_TRUNC('second', ts) AS ts_m, MAX(event) AS event
  FROM events GROUP BY user_id, DATE_TRUNC('second', ts)
)
SELECT user_id, ts_m AS ts, event,
       SUM(CASE WHEN ts_m - LAG(ts_m) OVER (PARTITION BY user_id ORDER BY ts_m) > INTERVAL '30 minutes'
                THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts_m) AS session_id
FROM dedup;
```
**Explanation:** Down-sampling the event stream to one row per user-second tames instrumentation spam and makes the 30-minute gap operator behave like a human-speed clickstream would.
## Q51: Scenario: Compute the cohort × step funnel: for each acquisition cohort, list which funnel step generates the biggest absolute drop.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR), users(user_id INT, acquired_at TIMESTAMP)

**Query:**
```sql
WITH firsts AS (
  SELECT u.user_id, DATE_TRUNC('month', u.acquired_at) AS cohort,
         MAX(e.ts) FILTER (WHERE e.event = 'browse')   AS t_browse,
         MAX(e.ts) FILTER (WHERE e.event = 'add_cart') AS t_cart,
         MAX(e.ts) FILTER (WHERE e.event = 'purchase') AS t_purchase
  FROM users u JOIN web_events e USING (user_id)
  GROUP BY u.user_id, DATE_TRUNC('month', u.acquired_at)
),
agg AS (
  SELECT cohort,
         COUNT(*) FILTER (WHERE t_browse IS NOT NULL)  AS c1,
         COUNT(*) FILTER (WHERE t_cart IS NOT NULL)    AS c2,
         COUNT(*) FILTER (WHERE t_purchase IS NOT NULL) AS c3
  FROM firsts GROUP BY cohort
)
SELECT cohort, c1, c2, c3,
       CASE WHEN (c1 - c2) >= (c2 - c3) THEN 'browse->cart' ELSE 'cart->purchase' END AS biggest_drop_step
FROM agg ORDER BY cohort;
```
**Explanation:** Comparing consecutive step deltas names the funnel's largest leak per cohort; if the drop flips between cohorts you know where to focus onboarding vs. checkout fixes.

## Q52: Scenario: Funnel for users who hit step 2 but not step 1 (skip-view arrivals). Classify them as 'deep-link entry' vs 'reordered' and report both counts.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH ordered AS (
  SELECT user_id,
         ARRAY_AGG(event ORDER BY ts) AS path
  FROM web_events GROUP BY user_id
)
SELECT CASE WHEN 'add_cart' = ANY(path) AND NOT ('browse' = ANY(path)) THEN 'deep_link_entry'
            WHEN 'purchase' = ANY(path) AND 'add_cart' = ANY(path)
                 AND array_position(path,'add_cart') > array_position(path,'purchase') THEN 'purchase_reorder'
            ELSE 'normal' END AS path_type,
       COUNT(*) AS users
FROM ordered
WHERE ('add_cart' = ANY(path) AND NOT ('browse' = ANY(path)))
   OR (array_position(path,'add_cart') > array_position(path,'purchase'))
GROUP BY 1;
```
**Explanation:** Array predicates isolate non-canonical entries: users who skip browse entirely (deep links) versus users who buy before adding to cart (sharing flows), giving two levers for funnel rework.

## Q53: Scenario: Every session gets a funnel_attempt flag: did it contain a complete ordered browse→add_cart→purchase run? Compare attempted vs. completed within each session.

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR), sessions(user_id INT, session_id INT)

**Query:**
```sql
WITH flagged AS (
  SELECT e.*,
         SUM(CASE WHEN e.ts - s.session_start > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY e.user_id ORDER BY e.ts) AS s_id
  FROM events e JOIN sessions s USING (user_id)
),
runs AS (
  SELECT user_id, s_id,
         COUNT(*) FILTER (WHERE event = 'browse')   AS browsed,
         COUNT(*) FILTER (WHERE event = 'add_cart') AS carted,
         COUNT(*) FILTER (WHERE event = 'purchase') AS purchased
  FROM flagged GROUP BY user_id, s_id
)
SELECT COUNT(*) AS sessions,
       COUNT(*) FILTER (WHERE browsed > 0 AND carted > 0) AS had_attempt,
       COUNT(*) FILTER (WHERE browsed > 0 AND carted > 0 AND purchased > 0) AS completed
FROM runs;
```
**Explanation:** Presence of each step defines an attempted vs completed funnel session; the gap between had_attempt and completed is the abandonment rate of sessions that seriously started shopping.

## Q54: Scenario: Compute the funnel using sessions as the unit (session-level steps) and separately as user-level, then diff to show session vs user interpretation.

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH flagged AS (
  SELECT user_id, ts, event,
         SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS s_id
  FROM events
),
sess AS (SELECT user_id, s_id, COUNT(DISTINCT event) FILTER (WHERE event LIKE '%pury%') AS p FROM flagged GROUP BY user_id, s_id)
SELECT COUNT(DISTINCT user_id) AS users_made_purchase,
       (SELECT COUNT(*) FROM sess) AS sessions_total
FROM sess WHERE p > 0;
```
**Explanation:** Unit choice changes the metric meaning: user-level counts buyers, session-level counts buying occasions; comparing both frames prevents interpreting one as the other in reporting.

## Q55: Scenario: Model the funnel as a chain that can restart after an abandonment: count users who abandoned (reached cart, no purchase in 2 days) but later converted in a later session.

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR), sessions(user_id INT, session_id INT, session_start TIMESTAMP)

**Query:**
```sql
WITH ordered AS (
  SELECT user_id, ts, event,
         SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS s_id
  FROM events
),
firsts AS (
  SELECT user_id, s_id,
         MAX(ts) FILTER (WHERE event = 'add_cart') AS t_cart,
         MAX(ts) FILTER (WHERE event = 'purchase') AS t_purchase
  FROM ordered GROUP BY user_id, s_id
)
SELECT COUNT(DISTINCT a.user_id) AS cart_abandoners,
       COUNT(DISTINCT CASE WHEN b.t_purchase > a.t_cart THEN b.user_id END) AS later_converted,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN b.t_purchase > a.t_cart THEN b.user_id END) / NULLIF(COUNT(DISTINCT a.user_id),0), 1) AS recovery_pct
FROM firsts a
LEFT JOIN firsts b ON b.user_id = a.user_id AND b.s_id > a.s_id;
```
**Explanation:** Joining a later session that contains a purchase to an earlier session with cart-but-no-purchase measures cart-abandonment recovery — a funnel that technically "failed" but redeemed later.

## Q56: Scenario: Compute time-between-step velocity bucketed by hour of day to find when fast checkout happens vs. slow.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH ordered AS (
  SELECT user_id,
         MIN(ts) FILTER (WHERE event = 'add_cart') AS t_cart,
         MIN(ts) FILTER (WHERE event = 'purchase') AS t_purchase
  FROM web_events GROUP BY user_id
)
SELECT EXTRACT(HOUR FROM t_cart) AS hour_of_day,
       ROUND(AVG(EXTRACT(EPOCH FROM (t_purchase - t_cart)) / 60.0), 1) AS avg_cart_to_buy_minutes
FROM ordered
WHERE t_purchase > t_cart
GROUP BY 1 ORDER BY hour_of_day;
```
**Explanation:** Bucketing conversion latency by the hour of the cart step reveals when users race through checkout (fast, 9-5 traffic) and when they linger (evenings), informing staffing and UX experiments.

## Q57: Scenario: Compute the 90th percentile session length and count the bumps that exceed it, as the anomaly threshold for your session log.

Schema hint: sessions(user_id INT, session_start TIMESTAMP, session_end TIMESTAMP)

**Query:**
```sql
WITH d AS (
  SELECT *, EXTRACT(EPOCH FROM (session_end - session_start)) AS secs
  FROM sessions
)
SELECT PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY secs) AS p90_seconds,
       COUNT(*) FILTER (WHERE secs > (SELECT PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY secs) FROM d)) AS sessions_over_p90
FROM d;
```
**Explanation:** The p90 duration defines a statistical outlier band; the count of sessions above it is the tail that troubleshooting tickets should inspect first.

## Q58: Scenario: Report sessions per server node per hour and spot session storming (a node handling 10x its median) as an infrastructure red flag.

Schema hint: sessions(node VARCHAR, session_id INT, session_start TIMESTAMP)

**Query:**
```sql
WITH per_node AS (
  SELECT node, DATE_TRUNC('hour', session_start) AS hour, COUNT(*) AS sessions
  FROM sessions GROUP BY node, DATE_TRUNC('hour', session_start)
),
median_band AS (
  SELECT node, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY sessions) AS median_sessions
  FROM per_node GROUP BY node
)
SELECT p.node, p.hour, p.sessions, m.median_sessions,
       ROUND(p.sessions * 1.0 / NULLIF(m.median_sessions,0), 1) AS times_median
FROM per_node p JOIN median_band m USING (node)
WHERE p.sessions > 10 * m.median_sessions
ORDER BY times_median DESC;
```
**Explanation:** Comparing each node-hour volume to that node's own median flags 10x spikes — classic session-storm signatures pointing to a cache miss bug or a health-check bot loop.

## Q59: Scenario: Distributed-consistency check: sessions that start on one device and end on another (device switching mid-session) — count how often that happens.

Schema hint: sessions(user_id INT, session_id INT, session_start TIMESTAMP, session_end TIMESTAMP, device VARCHAR)

**Query:**
```sql
SELECT COUNT(*) AS sessions,
       COUNT(*) FILTER (WHERE start_dev = end_dev) AS same_device,
       COUNT(*) FILTER (WHERE start_dev <> end_dev) AS cross_device
FROM (
  SELECT session_id,
         (ARRAY_AGG(device ORDER BY session_start))[1]  AS start_dev,
         (ARRAY_AGG(device ORDER BY session_end DESC))[1] AS end_dev
  FROM sessions GROUP BY session_id
) t;
```
**Explanation:** Sessions are attached to a single device ID in practice, so a start/end device mismatch is either instrumentation crossover or a bug, both worth counting before trusting multi-device analytics.

## Q60: Scenario: Detect improbable multi-touch attribution inside a session: a session that toggles IPs more than 3 times is flagged for review.

Schema hint: sessions(user_id INT, session_id INT, ip VARCHAR, ts TIMESTAMP)

**Query:**
```sql
WITH toggles AS (
  SELECT user_id, session_id,
         COUNT(*) FILTER (WHERE LAG(ip) OVER (PARTITION BY user_id, session_id ORDER BY ts) <> ip) AS ip_switches
  FROM sessions GROUP BY user_id, session_id
)
SELECT user_id, session_id, ip_switches
FROM toggles WHERE ip_switches >= 3
ORDER BY ip_switches DESC;
```
**Explanation:** Counting IP transitions within one session using LAG (excluding the first row's always-NULL comparison) flags sessions that hop networks — a VPN or a co-used account.

## Q61: Scenario: Rolling-session window engagement: what fraction of users had some session in each of the last 7 rolling windows of 24h?

Schema hint: sessions(user_id INT, session_start TIMESTAMP)

**Query:**
```sql
WITH hours AS (
  SELECT DISTINCT user_id,
         DATE_TRUNC('hour', session_start) AS hour
  FROM sessions
  WHERE session_start >= CURRENT_TIMESTAMP - INTERVAL '7 days'
)
SELECT hour,
       COUNT(DISTINCT user_id) AS active_users,
       (SELECT COUNT(DISTINCT user_id) FROM hours) AS uniques_7d
FROM hours GROUP BY hour ORDER BY hour;
```
**Explanation:** Per-hour distinct users joined against the rolling 7-day unique base shows whether daily engagement is growing or shrinking relative to the pool, equivalent to a naive rolling-active panel.

## Q62: Scenario: Users who come back after a 7-day absence: they had session today but prior session was >7 days ago. Count reset-session users.

Schema hint: sessions(user_id INT, session_start TIMESTAMP)

**Query:**
```sql
WITH seq AS (
  SELECT user_id, session_start,
         LAG(session_start) OVER (PARTITION BY user_id ORDER BY session_start) AS prev_start
  FROM sessions
)
SELECT COUNT(*) AS reactivations
FROM seq
WHERE session_start::date = CURRENT_DATE - 1
  AND (prev_start IS NULL OR session_start - prev_start > INTERVAL '7 days');
```
**Explanation:** Filtering yesterday's sessions whose previous session is more than 7 days old (or absent) counts lapsed users returning — the sleepers re-engaging cohort.

## Q63: Scenario: Recompute sessions with an asymmetric rule: gap of 15 min ends a session but a 5-second 'heartbeat' inside a session extends it (media-style pacing).

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
SELECT user_id, ts, event,
       SUM(CASE WHEN COALESCE(EXTRACT(EPOCH FROM (ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts))), 0) > 900
                THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS session_id
FROM events;
```
**Explanation:** Relaxing the cut to 15 minutes (900s) is a single constant change; modeling heartbeat-extension is equivalent because a heartbeat that stays under 900s simply never triggers a split.

## Q64: Scenario: Compare two sessionization strategies side by side: 30-min gap vs user-level 15-min gap, and output both session ids in one row set.

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH g AS (
  SELECT user_id, ts, event,
         LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) AS prev
  FROM events
)
SELECT user_id, ts, event,
       SUM(CASE WHEN prev IS NULL OR EXTRACT(EPOCH FROM (ts - prev)) > 1800 THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS sess_30m,
       SUM(CASE WHEN prev IS NULL OR EXTRACT(EPOCH FROM (ts - prev)) > 900 THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS sess_15m
FROM g;
```
**Explanation:** A single pass over precomputed lag values yields both session ids; diffs between the two columns identify events re-bucketed by the stricter rule and drive sensitivity analysis of the cutoff.

## Q65: Scenario: Some products define a session by focusing on a single page type. Keep only 'watch' events and sessionize those, discarding navigation noise.

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR, page VARCHAR)

**Query:**
```sql
SELECT user_id, ts, event,
       SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS session_id
FROM events
WHERE page = 'watch';
```
**Explanation:** Pre-filtering to the watch page before the gap window means only watch dwells define a session — navigation across other pages no longer resets the clock.

## Q66: Scenario: Build the funnel counting events, not users, to demonstrate the double-count bias: the same user completing the funnel twice inflates 'purchases'.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
SELECT 'raw pull all purchases' AS metric,
       COUNT(*) FILTER (WHERE event = 'purchase') AS naive_count
FROM web_events
UNION ALL
SELECT 'distinct user purchases', COUNT(DISTINCT user_id)
FROM web_events WHERE event = 'purchase';
```
**Explanation:** The naive count includes repeat purchasers multiple times; distinct-user counting is the funnel-correct denominator and the two numbers' ratio reveals repeat-purchase rate.

## Q67: Scenario: Return session start time and the session's first event type in one query without a correlated subquery.

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH flagged AS (
  SELECT user_id, ts, event,
         SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS session_id,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY ts) AS rn
  FROM events
),
starts AS (
  SELECT user_id, session_id, MIN(ts) AS s_start
  FROM flagged GROUP BY user_id, session_id
)
SELECT s.user_id, s.session_id, s.s_start,
       FIRST_VALUE(f.event) OVER (PARTITION BY f.user_id, f.session_id ORDER BY f.ts) AS first_event
FROM starts s JOIN flagged f USING (user_id, session_id)
GROUP BY s.user_id, s.session_id, s.s_start, f.event, f.ts
ORDER BY s.user_id, s.session_id;
```
**Explanation:** FIRST_VALUE over the session partition labels the leading event; combining it with the MIN start gives a complete session-opening summary without correlated lookups.

## Q68: Scenario: Produce a per-session page-view sequence that skips intra-page duplicate views (repeat clicks on the same link collapse to one).

Schema hint: events(user_id INT, ts TIMESTAMP, url VARCHAR)

**Query:**
```sql
WITH flagged AS (
  SELECT user_id, ts, url,
         SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS session_id
  FROM events
),
deduped AS (
  SELECT DISTINCT ON (user_id, session_id, url)
         user_id, session_id, url
  FROM flagged ORDER BY user_id, session_id, url, ts
)
SELECT user_id, session_id, ARRAY_AGG(url) AS cleaned_clickpath
FROM deduped GROUP BY user_id, session_id;
```
**Explanation:** DISTINCT ON per (session, url) keeps one row per page, so repeated visits to the same URL inside a session read as one step rather than inflating the clickpath.

## Q69: Scenario: Given a funnel where some users do step2 without step1, compute the skip-measure as a ratio and name the dominant skip pattern.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH path AS (
  SELECT user_id, ARRAY_AGG(event ORDER BY ts) AS p
  FROM web_events GROUP BY user_id
)
SELECT CASE WHEN array_length(p,1) = 1 THEN 'single_step'
            WHEN 'step2' = ANY(p) AND NOT ('step1' = ANY(p)) THEN 'skip_step1'
            ELSE 'normal' END AS pattern,
       COUNT(*) AS users
FROM path GROUP BY 1 ORDER BY users DESC;
```
**Explanation:** Classifying paths by skip presence produces a labeled breakdown; the top pattern is the funnel change that would recover the most conversions.

## Q70: Scenario: Track `conversion date` vs `first session date` to measure time-from-first-session to purchase in days (conversion latency), bucketed.

Schema hint: sessions(user_id INT, session_start TIMESTAMP), purchases(user_id INT, purchased_at TIMESTAMP)

**Query:**
```sql
WITH f AS (
  SELECT s.user_id, MIN(s.session_start) AS first_visit,
         MIN(p.purchased_at) AS first_purchase
  FROM sessions s LEFT JOIN purchases p USING (user_id)
  GROUP BY s.user_id
)
SELECT CASE WHEN EXTRACT(days FROM (first_purchase - first_visit)) > 30 THEN '30d+'
            WHEN EXTRACT(days FROM (first_purchase - first_visit)) > 7 THEN '8-30d'
            WHEN EXTRACT(days FROM (first_purchase - first_visit)) > 1 THEN '2-7d'
            ELSE 'same-day' END AS latency_bucket,
       COUNT(*) AS buyers
FROM f WHERE first_purchase IS NOT NULL
GROUP BY 1 ORDER BY 1;
```
**Explanation:** Diffing each buyer's first purchase against first session and bucketing days reveals purchase latency — critical for whether same-day funnel or multi-touch nurture deserves the budget.

## Q71: Scenario: A/B test the funnel: two variants, compute conversion per variant and a simple relative uplift.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR, variant VARCHAR)

**Query:**
```sql
WITH v AS (
  SELECT variant,
         COUNT(DISTINCT user_id) FILTER (WHERE event = 'step1') AS reached,
         COUNT(DISTINCT user_id) FILTER (WHERE event = 'step3') AS converted
  FROM web_events GROUP BY variant
)
SELECT variant, ROUND(100.0 * converted / NULLIF(reached,0), 2) AS conv_rate,
       ROUND(100.0 * (converted * 1.0 / reached) / NULLIF(MAX(converted * 1.0 / reached) OVER (),0), 1) AS relative_to_best
FROM v ORDER BY conv_rate DESC;
```
**Explanation:** Normalizing conversions by reached-per-variant yields unbiased-rates, and the windowed ratio of the best variant reports relative uplift in one query.

## Q72: Scenario: Detect a funnel leak caused by a failed dependency: purchases that bounced because the payment step errored before checkout.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR, error VARCHAR)

**Query:**
```sql
WITH err AS (
  SELECT DISTINCT user_id
  FROM web_events
  WHERE event = 'payment_error' AND error = '3ds_failed'
)
SELECT COUNT(*) AS error_users,
       (SELECT COUNT(DISTINCT user_id) FROM web_events WHERE event = 'purchase') AS purchasers,
       ROUND(100.0 * COUNT(*) / NULLIF((SELECT COUNT(DISTINCT user_id) FROM web_events WHERE event = 'purchase'),0), 1) AS error_to_purchase_pct
FROM err;
```
**Explanation:** Linking payment-3DS failures to purchases shows how much of the funnel leak is technical rather than intent; removing that failure class is a mechanical fix with a measurable ceiling.

## Q73: Scenario: Rolling 3-day average of completed funnels to smooth volatility and identify dips vs. structural change.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH daily AS (
  SELECT ts::date AS day,
         COUNT(DISTINCT user_id) FILTER (WHERE event = 'step3') AS completed
  FROM web_events GROUP BY ts::date
)
SELECT day, completed,
       ROUND(AVG(completed) OVER (ORDER BY day ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 1) AS rolling_3d
FROM daily ORDER BY day;
```
**Explanation:** A 3-day centered rolling average single-windowed in the SELECT flattens weekday noise, exposing a real dive from a config bug rather than a Monday artifact.

**Alt1:** Use `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` for a weekly smoothing that absorbs day-of-week seasonality entirely.

## Q74: Scenario: Surface user journeys that go backwards in the funnel (purchase, then add_cart) — path-order anomalies worth flagging.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH p AS (
  SELECT user_id, ARRAY_AGG(event ORDER BY ts) AS path
  FROM web_events GROUP BY user_id
)
SELECT user_id, path
FROM p
WHERE array_position(path, 'purchase') < array_position(path, 'add_cart');
```
**Explanation:** Any user whose purchase timestamp precedes the add_cart one has a non-linear journey; listing them isolates instrumentation errors, gift flows, or backfilled orders.

## Q75: Scenario: Compute the expected-funnel completion assuming steps are independent (product of step probabilities) vs. the observed, to quantify dependency between steps.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH probs AS (
  SELECT ROUND(COUNT(DISTINCT user_id) FILTER (WHERE event = 'step2') * 1.0 / COUNT(DISTINCT user_id), 3) AS p2,
         ROUND(COUNT(DISTINCT user_id) FILTER (WHERE event = 'step3') * 1.0 / COUNT(DISTINCT user_id), 3) AS p3
  FROM web_events
),
observed AS (
  SELECT user_id FROM web_events WHERE event = 'step3'
)
SELECT p.p2 * p.p3 AS expected_independent,
       ROUND(COUNT(DISTINCT o.user_id) * 1.0 / (SELECT COUNT(DISTINCT user_id) FROM web_events), 3) AS observed
FROM probs p, observed o
GROUP BY p.p2, p.p3;
```
**Explanation:** If steps were independent, expected = product of each step's marginal rate; the gap to observed quantifies how correlated step completion is, guiding whether to optimize the leaky step or the path between steps.
## Q76: Scenario: Aggregate a full funnel with wedge measures: users, sessions, and events at each step, all in one table for a dashboard.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR, session_id INT)

**Query:**
```sql
SELECT step,
       COUNT(*) AS events,
       COUNT(DISTINCT session_id) AS sessions,
       COUNT(DISTINCT user_id) AS users
FROM web_events
GROUP BY step
ORDER BY MIN(CASE step WHEN 'step1' THEN 1 WHEN 'step2' THEN 2 WHEN 'step3' THEN 3 END);
```
**Explanation:** One GROUP BY over event type yields events/sessions/users per step; the CASE ordering pins display order so dashboard tiles line up with the funnel shape.

## Q77: Scenario: A marketing promotion sends users directly to checkout. Compare funnel for promo vs organic cohorts using the user's acquisition flag.

Schema hint: users(user_id INT, channel VARCHAR), web_events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
SELECT u.channel,
       COUNT(DISTINCT u.user_id) FILTER (WHERE e.event = 'step1') AS entered,
       COUNT(DISTINCT u.user_id) FILTER (WHERE e.event = 'step3') AS converted,
       ROUND(100.0 * COUNT(DISTINCT u.user_id) FILTER (WHERE e.event = 'step3')
            / NULLIF(COUNT(DISTINCT u.user_id) FILTER (WHERE e.event = 'step1'),0), 1) AS conv_rate
FROM users u JOIN web_events e USING (user_id)
GROUP BY u.channel ORDER BY conv_rate DESC NULLS LAST;
```
**Explanation:** Cohort-funnel cross-tab by acquisition channel exposes which channels pipeline high-intent shoppers straight to conversion and which enter as window-shoppers.

## Q78: Scenario: Compute step-time-normed funnel: average seconds spent at each step before advancing, to find the "slowest" step.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR, session_id INT)

**Query:**
```sql
WITH seq AS (
  SELECT user_id, session_id, event, ts,
         LAG(event) OVER (PARTITION BY user_id, session_id ORDER BY ts) AS prev_event,
         LAG(ts)    OVER (PARTITION BY user_id, session_id ORDER BY ts) AS prev_ts
  FROM web_events
)
SELECT prev_event, ROUND(AVG(EXTRACT(EPOCH FROM (ts - prev_ts))),1) AS avg_seconds_on_step
FROM seq WHERE prev_event IS NOT NULL
GROUP BY prev_event ORDER BY avg_seconds_on_step DESC;
```
**Explanation:** Pairing each event with its predecessor inside a session measures time spent on a step; the step with the longest dwell is where users reconsider, an optimization target.

## Q79: Scenario: Sessions that both entered and completed the funnel are 'converting sessions'; pair them with their dwell to check whether faster sessions convert better.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR, session_id INT)

**Query:**
```sql
WITH s AS (
  SELECT session_id,
         COUNT(*) FILTER (WHERE event = 'step1') AS has_step1,
         COUNT(*) FILTER (WHERE event = 'step3') AS has_step3,
         MAX(ts) - MIN(ts) AS length
  FROM web_events GROUP BY session_id
)
SELECT CASE WHEN EXTRACT(EPOCH FROM length) < 120 THEN 'fast'
            WHEN EXTRACT(EPOCH FROM length) < 900 THEN 'avg' ELSE 'slow' END AS session_speed,
       COUNT(*) FILTER (WHERE has_step1 > 0 AND has_step3 > 0) AS converting_sessions,
       COUNT(*) FILTER (WHERE has_step1 > 0) AS entered_sessions,
       ROUND(100.0 * COUNT(*) FILTER (WHERE has_step1 > 0 AND has_step3 > 0) / NULLIF(COUNT(*) FILTER (WHERE has_step1 > 0),0),1) AS conversion_pct
FROM s GROUP BY 1 ORDER BY 1;
```
**Explanation:** Bucketing sessions by total length and painting conversion rates onto those buckets shows whether speedy sessions signal decisive shoppers or accidental hits.

## Q80: Scenario: Emit per-user max funnel depth reached (1, 2, or 3) as a distribution: how many users stop at each stage.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH depth AS (
  SELECT user_id,
         MAX(CASE event WHEN 'step1' THEN 1 WHEN 'step2' THEN 2 WHEN 'step3' THEN 3 END) AS max_depth
  FROM web_events GROUP BY user_id
)
SELECT max_depth, COUNT(*) AS users,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM depth GROUP BY max_depth ORDER BY max_depth;
```
**Explanation:** Mapping events to step ranks and taking the per-user max yields cumulative depth; the plateau in the distribution is exactly the drop-off at that stage.

**Alt1:** Use `CARDINALITY(ARRAY_AGG(DISTINCT step))` over the ranked steps per user for the same depth measure without a MAX-CASE mapping.

## Q81: Scenario: Return all events of a single key session with a flag marking whether the session converted, to enable mixed-model funnel+forecast features.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR, session_id INT)

**Query:**
```sql
WITH conv AS (
  SELECT DISTINCT session_id
  FROM web_events
  WHERE event = 'step3'
)
SELECT e.user_id, e.session_id, e.ts, e.event,
       CASE WHEN c.session_id IS NOT NULL THEN 'converted' ELSE 'abandoned' END AS outcome
FROM web_events e
LEFT JOIN conv c USING (session_id)
ORDER BY e.session_id, e.ts;
```
**Explanation:** A LEFT JOIN against the set of converting session ids stamps every event with its session outcome, ready for model features like counts-before-step3.

## Q82: Scenario: Simulate a funnel of first-time events only (each step needs to be the user's first of that kind) to mirror UX demos rather than repeat visits.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH firsts AS (
  SELECT user_id, event, MIN(ts) AS t
  FROM web_events GROUP BY user_id, event
)
SELECT COUNT(DISTINCT user_id) AS users_with_step,
       COUNT(DISTINCT user_id) FILTER (WHERE t BETWEEN first_t AND first_t + INTERVAL '1 hour') AS one_hour
FROM (
  SELECT user_id, event, t,
         MIN(t) OVER (PARTITION BY user_id) AS first_t
  FROM firsts
) x GROUP BY 1;
```
**Explanation:** Collapsing each (user, step) to its earliest time simulates a virgin-journey funnel; the one-hour window variant measures how much of the flow happens on the very first touch.

## Q83: Scenario: Compute the funnel of sessions that bounce (single event) separately from engagers, to show how much conversion is carried by the engaged minority.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR, session_id INT)

**Query:**
```sql
WITH sess AS (
  SELECT session_id, COUNT(*) AS n
  FROM web_events GROUP BY session_id
)
SELECT 'bounce' AS kind, COUNT(DISTINCT w.user_id) AS converted
FROM web_events w JOIN sess s USING (session_id)
WHERE s.n = 1 AND w.event = 'step3'
UNION ALL
SELECT 'engaged', COUNT(DISTINCT w.user_id)
FROM web_events w JOIN sess s USING (session_id)
WHERE s.n > 1 AND w.event = 'step3';
```
**Explanation:** Splitting converting users by session size shows the engaged chunk virtually owns conversion; bounce-single-event purchases are near-impossible, a sanity validation of the funnel.

## Q84: Scenario: Compute sessions where the user went back-and-forth between step1 and step2 three or more times (hover-looping) as UX friction.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR, session_id INT)

**Query:**
```sql
WITH toggles AS (
  SELECT session_id,
         COUNT(*) FILTER (WHERE LAG(event) OVER (PARTITION BY session_id ORDER BY ts) <> event) AS switches
  FROM web_events GROUP BY session_id
)
SELECT COUNT(*) FILTER (WHERE switches >= 3) AS looping_sessions,
       COUNT(*) AS total_sessions
FROM toggles;
```
**Explanation:** Counting event-type changes via LAG-neq each session, sessions with 3+ switches are hover-loopers; their share is the UX-friction metric for the funnel.

## Q85: Scenario: Build the time-damped funnel: weight conversions by how quickly they happen (e.g. same-session conversion counts 1.0, next-day 0.5).

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR), sessions(user_id INT, session_id INT, session_start TIMESTAMP)

**Query:**
```sql
WITH conv AS (
  SELECT DISTINCT w.user_id, s.session_start
  FROM web_events w JOIN sessions s USING (user_id)
  WHERE w.event = 'step3'
)
SELECT SUM(CASE WHEN session_start::date = conv.session_start::date THEN 1.0
                WHEN session_start > conv.session_start THEN 0.5 ELSE 0 END) AS damped_conversions
FROM web_events
JOIN sessions USING (user_id)
JOIN conv USING (user_id)
WHERE event = 'step1';
```
**Explanation:** Multiplying same-day conversions by 1.0 and later ones by 0.5 discounts latency-weighted success, so instantaneous funnels contribute more to the product score.

## Q86: Scenario: Emit session-first and session-last timestamps in an event-level table so downstream joins never re-derive session bounds.

Schema hint: events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH flagged AS (
  SELECT user_id, ts, event,
         SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts) AS session_id
  FROM events
)
SELECT user_id, session_id, ts, event,
       MIN(ts) OVER (PARTITION BY user_id, session_id) AS s_start,
       MAX(ts) OVER (PARTITION BY user_id, session_id) AS s_end
FROM flagged;
```
**Explanation:** Broadcast windowed MIN/MAX per (user, session) denormalizes bounds onto every row in one pass — the standard presentation layer for sessionized streams.

## Q87: Scenario: Recompute a user's session count over 30 days and compare against their purchase count to find the conversion-per-session ratio.

Schema hint: sessions(user_id INT, session_start TIMESTAMP), purchases(user_id INT, purchased_at TIMESTAMP)

**Query:**
```sql
SELECT s.user_id,
       COUNT(DISTINCT s.session_id) AS sessions_30d,
       COUNT(DISTINCT p.purchase_id) AS purchases_30d,
       ROUND(COUNT(DISTINCT p.purchase_id) * 100.0 / NULLIF(COUNT(DISTINCT s.session_id),0), 2) AS purchase_per_session_pct
FROM sessions s
LEFT JOIN purchases p ON p.user_id = s.user_id
  AND p.purchased_at > '2026-01-01' AND p.purchased_at < CURRENT_DATE
WHERE s.session_start > '2026-01-01'
GROUP BY s.user_id;
```
**Explanation:** Dividing rolling 30-day purchases by sessions normalizes buyer behavior across users; very low ratios indicate browsing-users who never transact.

## Q88: Scenario: The funnel is dynamic (steps can be added mid-quarter). Recompute Q-over-Q by labeling events with the step-map version they were collected under.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR), step_map(version VARCHAR, event VARCHAR, step_key INT)

**Query:**
```sql
WITH labeled AS (
  SELECT e.user_id, m.step_key,
         MAX(e.ts) FILTER (WHERE m.step_key = 1) AS t1,
         MAX(e.ts) FILTER (WHERE m.step_key = 2) AS t2,
         MAX(e.ts) FILTER (WHERE m.step_key = 3) AS t3
  FROM web_events e
  JOIN step_map m ON m.event = e.event AND m.version = 'v2'
  GROUP BY e.user_id, m.step_key
)
SELECT COUNT(*) FILTER (WHERE t1 IS NOT NULL AND t2 IS NOT NULL AND t3 IS NOT NULL) AS full_path
FROM labeled;
```
**Explanation:** Joining a versioned step map re-buckets historical events under current definitions, so Q-over-Q comparisons stay apples-to-apples when the funnel changes.

## Q89: Scenario: Compute the 'step-area' metric: total time users collectively spent between step1 and step2, bucketed by day, as a load signal.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR, session_id INT)

**Query:**
```sql
WITH step_times AS (
  SELECT user_id,
         MIN(ts) FILTER (WHERE event = 'step1') AS t1,
         MIN(ts) FILTER (WHERE event = 'step2') AS t2
  FROM web_events GROUP BY user_id
)
SELECT t1::date AS day,
       SUM(EXTRACT(EPOCH FROM (t2 - t1)) / 3600.0) AS person_hours_between_1_and_2
FROM step_times
WHERE t2 > t1 GROUP BY 1 ORDER BY day;
```
**Explanation:** Integrating dwell between consecutive steps per user-day yields a person-hour load; a spike here shows extra friction (or a stuck form) costing support time.

## Q90: Scenario: Pinpoint the exact step pair with the largest conversion gap so you can spend redesign effort where it moves the needle most.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR), sessions(user_id INT, session_id INT, session_start TIMESTAMP)

**Query:**
```sql
WITH ordered AS (
  SELECT w.user_id, w.session_id,
         MAX(w.ts) FILTER (WHERE w.event = 'step1') AS t1,
         MAX(w.ts) FILTER (WHERE w.event = 'step2') AS t2,
         MAX(w.ts) FILTER (WHERE w.event = 'step3') AS t3,
         MAX(w.ts) FILTER (WHERE w.event = 'step4') AS t4
  FROM web_events w JOIN sessions s USING (session_id)
  GROUP BY w.user_id, w.session_id
)
SELECT 'step1->step2' AS pair, COUNT(*) FILTER (WHERE t1 IS NOT NULL AND t2 > t1) AS progressed,
       COUNT(*) FILTER (WHERE t1 IS NOT NULL) AS base FROM ordered
UNION ALL SELECT 'step2->step3', COUNT(*) FILTER (WHERE t2 IS NOT NULL AND t3 > t2), COUNT(*) FILTER (WHERE t2 IS NOT NULL) FROM ordered
UNION ALL SELECT 'step3->step4', COUNT(*) FILTER (WHERE t3 IS NOT NULL AND t4 > t3), COUNT(*) FILTER (WHERE t3 IS NOT NULL) FROM ordered;
```
**Explanation:** A UNION of progression/base pairs at each transition ranks which step-pair loses the most users; the largest loss is where the product team should ship next. Note: `progressed <= base` invariant holds by construction.

## Q91: Scenario: Compute per-session conversion-attempt rate when a user attempted the funnel (hit step1) multiple times in one session — attempt count vs. one attempt.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR, session_id INT)

**Query:**
```sql
WITH attempts AS (
  SELECT session_id,
         COUNT(*) FILTER (WHERE event = 'step1') AS step1_count,
         COUNT(*) FILTER (WHERE event = 'step3') AS step3_count
  FROM web_events GROUP BY session_id
)
SELECT CASE WHEN step1_count = 1 THEN 'one_attempt' ELSE 'repeat_attempts' END AS attempt_style,
       COUNT(*) FILTER (WHERE step3_count > 0) AS converted_sessions,
       COUNT(*) AS sessions
FROM attempts GROUP BY 1;
```
**Explanation:** Sessions with a single step1 vs. repeated step1 reveal whether users convert on first try or need several run-throughs; persistent restarters are a UX or trust issue.

## Q92: Scenario: Compute session-start-hour bias of the funnel: does conversion rate depend on when the session began (graveyard vs peak)?

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR, session_id INT)

**Query:**
```sql
WITH sess AS (
  SELECT session_id, MIN(ts) AS s_start,
         COUNT(*) FILTER (WHERE event = 'step1') AS s1,
         COUNT(*) FILTER (WHERE event = 'step3') AS s3
  FROM web_events GROUP BY session_id
)
SELECT EXTRACT(HOUR FROM s_start) AS start_hour,
       COUNT(*) FILTER (WHERE s1 > 0) AS entered,
       COUNT(*) FILTER (WHERE s1 > 0 AND s3 > 0) AS converted,
       ROUND(100.0 * COUNT(*) FILTER (WHERE s1 > 0 AND s3 > 0) / NULLIF(COUNT(*) FILTER (WHERE s1 > 0),0), 1) AS conv_pct
FROM sess GROUP BY 1 ORDER BY start_hour;
```
**Explanation:** Grouping sessions by their opening hour and comparing entered-vs-converted reveals whether late-night sessions convert better (motivated) or worse (bot traffic), steering support staffing.

## Q93: Scenario: Detect the 'checkout hang': sessions that reach step2 but generate no step3 within 5 minutes; compute the rate and whether they resume later.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR, session_id INT), sessions(user_id INT, session_id INT)

**Query:**
```sql
WITH hang AS (
  SELECT session_id,
         COUNT(*) FILTER (WHERE event = 'step2') > 0 AND COUNT(*) FILTER (WHERE event = 'step3') = 0 AS step2_no_step3_5min
  FROM web_events GROUP BY session_id
)
SELECT COUNT(*) FILTER (WHERE step2_no_step3_5min) AS hung_sessions,
       COUNT(*) AS try_sessions,
       ROUND(100.0 * COUNT(*) FILTER (WHERE step2_no_step3_5min) / NULLIF(COUNT(*),0), 1) AS hang_rate_pct
FROM hang;
```
**Explanation:** Presence of step2 without step3 marks a checkout hang; its rate is the abandonment floor that call-center tickets confirm.

## Q94: Scenario: For every step-1-to-step-2 gap, classify the gap as 'instant' (<15s), 'normal', or 'long' and output the distribution.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR, session_id INT)

**Query:**
```sql
WITH spans AS (
  SELECT session_id,
         EXTRACT(EPOCH FROM (MIN(ts) FILTER (WHERE event = 'step2') - MIN(ts) FILTER (WHERE event = 'step1'))) AS gap_s
  FROM web_events GROUP BY session_id
)
SELECT CASE WHEN gap_s < 15 THEN 'instant' WHEN gap_s < 300 THEN 'normal' ELSE 'long' END AS bucket,
       COUNT(*) AS sessions
FROM spans WHERE gap_s IS NOT NULL
GROUP BY 1 ORDER BY 2 DESC;
```
**Explanation:** Sub-second step1→step2 gaps cluster in the 'instant' bucket — the signature of scripted automation — while long gaps are humans reading content.

## Q95: Scenario: Efficient chunking for big data: split the funnel computation by date partition and merge in one CTE (the map-reduce pattern interviewers love).

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR) PARTITIONED BY DAY

**Query:**
```sql
WITH partial AS (
  SELECT ts::date AS day, partition_epoch,
         COUNT(DISTINCT user_id) FILTER (WHERE event = 'step1') AS c1,
         COUNT(DISTINCT user_id) FILTER (WHERE event = 'step3') AS c3
  FROM web_events
  CROSS JOIN LATERAL (SELECT (EXTRACT(EPOCH FROM ts) / 86400)::int AS partition_epoch) x
  GROUP BY 1, 2
)
SELECT day, MAX(c1) AS entered, MAX(c3) AS converted,
       ROUND(100.0 * MAX(c3) / NULLIF(MAX(c1),0), 1) AS conv_pct
FROM partial GROUP BY day ORDER BY day;
```
**Explanation:** Pre-aggregating per partition-epoch (a day shard) then folding to a daily max keeps the heavy DISTINCT work distributed and the merge light — the pattern behind partitioned funnel pipelines.

## Q96: Scenario: Merge heartbeats and click events into one sessionized stream with an explicit event_priority tie-breaker for equal timestamps.

Schema hint: heartbeats(user_id INT, ts TIMESTAMP), clicks(user_id INT, ts TIMESTAMP, page VARCHAR)

**Query:**
```sql
WITH merged AS (
  SELECT user_id, ts, 'click' AS kind, 1 AS priority
  FROM clicks
  UNION ALL
  SELECT user_id, ts, 'hb', 0 FROM heartbeats
)
SELECT user_id, ts, kind,
       SUM(CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts, priority) > INTERVAL '30 minutes'
                THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY ts, priority) AS session_id
FROM merged;
```
**Explanation:** Unioning both sources and ordering by (ts, priority) keeps clicks ahead of heartbeats on the same instant, so session ids don't flip unpredictably at collision moments.

## Q97: Scenario: The product defines a session as at most 4 hours even if active. Enforce a strict cap so a bot that never stops generates multiple sessions.

Schema hint: events(user_id INT, ts TIMESTAMP, event)

**Query:**
```sql
WITH flagged AS (
  SELECT user_id, ts,
         CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL '30 minutes'
               OR EXTRACT(EPOCH FROM (ts - MIN(ts) OVER (PARTITION BY user_id ORDER BY ts ROWS UNBOUNDED PRECEDING))) > 4*3600
              THEN 1 ELSE 0 END AS cut
  FROM events
)
SELECT user_id, ts,
       SUM(cut) OVER (PARTITION BY user_id ORDER BY ts ROWS UNBOUNDED PRECEDING) AS session_id
FROM flagged;
```
**Explanation:** Adding an OR-condition — the 30-min gap OR exceeding 4 hours since the session's running start — caps session length, so a continuous bot gets split into capped 4h pieces that are easier to reason about.

**Alt1:** Carry a per-session running start with MAX(ts) FILTER in a second pass and compare the same way if the window engine doesn't allow OR on two windows.

## Q98: Scenario: Compute each user's funnel depth as a sequence vector (e.g. '1,2,3', '1,2', '1') and count users per vector.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR)

**Query:**
```sql
WITH depth AS (
  SELECT user_id, ARRAY_AGG(DISTINCT step ORDER BY step) AS seq
  FROM (
    SELECT user_id, CASE event WHEN 'step1' THEN 1 WHEN 'step2' THEN 2 WHEN 'step3' THEN 3 END AS step
    FROM web_events
  ) t GROUP BY user_id
)
SELECT seq, COUNT(*) AS users
FROM depth GROUP BY seq ORDER BY seq;
```
**Explanation:** A per-user ordered DISTINCT array of reached step numbers is the funnel depth signature; grouping by it counts exactly how many users peak at each depth.

## Q99: Scenario: Return, per session, whether the funnel happened, plus the time-to-first-completion, to feed a churn model.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR, session_id INT)

**Query:**
```sql
WITH s AS (
  SELECT session_id,
         COUNT(*) FILTER (WHERE event = 'step1') > 0 AS entered,
         COUNT(*) FILTER (WHERE event = 'step3') > 0 AS converted,
         MIN(ts) FILTER (WHERE event = 'step1') AS first_step1,
         MIN(ts) FILTER (WHERE event = 'step3') AS first_step3
  FROM web_events GROUP BY session_id
)
SELECT session_id, entered, converted,
       EXTRACT(EPOCH FROM (first_step3 - first_step1)) AS seconds_to_complete
FROM s;
```
**Explanation:** Boolean entered/converted flags plus the step1→step3 latency give a model-ready feature row per session; NULL seconds to complete encode non-converters naturally.

## Q100: Scenario: Full capstone — one query producing the end-to-end report: sessions per user, sharing the funnel stages within a 30-min session, plus the churn-resurrection day-7 flag, for the analytics team.

Schema hint: web_events(user_id INT, ts TIMESTAMP, event VARCHAR), sessions(user_id INT, session_id INT, session_start TIMESTAMP, session_end TIMESTAMP)

**Query:**
```sql
WITH flagged AS (
  SELECT e.user_id, e.ts, e.event,
         SUM(CASE WHEN e.ts - LAG(e.ts) OVER (PARTITION BY e.user_id ORDER BY e.ts) > INTERVAL '30 minutes'
                  THEN 1 ELSE 0 END) OVER (PARTITION BY e.user_id ORDER BY e.ts) AS s_id
  FROM web_events e
),
funnel AS (
  SELECT user_id, s_id,
         COUNT(*) FILTER (WHERE event = 'step1') > 0 AS entered,
         COUNT(*) FILTER (WHERE event = 'step2') > 0 AS carted,
         COUNT(*) FILTER (WHERE event = 'step3') > 0 AS purchased
  FROM flagged GROUP BY user_id, s_id
),
resurrect AS (
  SELECT user_id,
         MAX(s.session_start) OVER (PARTITION BY s.user_id ORDER BY s.session_start
                                    ROWS BETWEEN 1 FOLLOWING AND 1 FOLLOWING) AS next_session
  FROM sessions s
)
SELECT f.user_id, f.s_id, f.entered, f.carted, f.purchased,
       CASE WHEN r.next_session IS NOT NULL
                 AND r.next_session - s.session_start <= INTERVAL '7 days'
            THEN 'returned_7d' ELSE 'lapsed' END AS resurrection_flag,
       ROUND(100.0 * COUNT(*) FILTER (WHERE f.purchased) OVER (PARTITION BY f.user_id)
            / NULLIF(COUNT(*) FILTER (WHERE f.entered) OVER (PARTITION BY f.user_id), 0), 1) AS user_funnel_conv_pct
FROM funnel f
JOIN (SELECT user_id, s_id, MIN(session_start) AS session_start
      FROM sessions GROUP BY user_id, s_id) s USING (user_id, s_id)
LEFT JOIN resurrect r USING (user_id)
ORDER BY f.user_id, f.s_id;
```
**Explanation:** This capstone fuses sessionization, the 3-step same-session funnel, a 7-day return (churn) flag, and a per-user conversion rate into one row-per-flagged-session output — everything the analytics team needs for the weekly funnel+retention review.

**Alt1:** Swap the LAG-based sessioning for a `NTH_VALUE` or recursive-CTE session build if the engine lacks stable window ORDER BY over large event streams, keeping the funnel section identical.
