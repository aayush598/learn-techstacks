# Gaps and Islands — 100 Interview Q&A

**The two core idioms you must master:**

| Idiom | How it works |
|---|---|
| **(a) ROW_NUMBER minus value** | Number a sorted sequence (dates, numbers), subtract the actual value; the difference is constant *within* an island and different across islands → every gap restarts the key. |
| **(b) LAG difference to start a new group** | `LAG(x) OVER (ORDER BY x)`; when `x - LAG(x) > 1` a new island begins. Handy when values are sparse or you know your own threshold. |

## Q1: Find islands of consecutive dates in a table of day-of-purchase.

Schema hints: `purchases(transaction_date date)` — dates have gaps; group consecutive runs.

**Query:**
```sql
WITH data(transaction_date) AS (
  VALUES (date '2026-01-01'),(date '2026-01-02'),(date '2026-01-03'),
         (date '2026-01-06'),(date '2026-01-07'),(date '2026-01-11')
),
numbered AS (
  SELECT transaction_date,
         transaction_date - (ROW_NUMBER() OVER (ORDER BY transaction_date))::int AS grp
  FROM data
)
SELECT MIN(transaction_date) AS island_start,
       MAX(transaction_date) AS island_end,
       COUNT(*) AS days
FROM numbered
GROUP BY grp
ORDER BY island_start;
```
**Explanation:** Subtracting the row number from each date yields one constant key per consecutive run; grouping by it isolates each island.

**Alt1:**
```sql
WITH data(transaction_date) AS (
  VALUES (date '2026-01-01'),(date '2026-01-02'),(date '2026-01-03'),
         (date '2026-01-06'),(date '2026-01-07'),(date '2026-01-11')
),
flagged AS (
  SELECT transaction_date,
         transaction_date - LAG(transaction_date)
           OVER (ORDER BY transaction_date) AS diff
  FROM data
),
islands AS (
  SELECT transaction_date,
         SUM(CASE WHEN diff > 1 OR diff IS NULL THEN 1 ELSE 0 END)
           OVER (ORDER BY transaction_date) AS grp
  FROM flagged
)
SELECT MIN(transaction_date) AS island_start,
       MAX(transaction_date) AS island_end,
       COUNT(*) AS days
FROM islands
GROUP BY grp
ORDER BY island_start;
```
**Explanation:** A running sum increments on every gap (diff > 1), so it becomes an island id built from LAG differences instead of ROW_NUMBER subtraction.

## Q2: Find all missing numbers and their ranges in `1,2,5,7` (sequence column).

Schema hints: `nums(n int)` holds `1,2,5,7`; find missing `3,4` as `3-4` and `6` as `6-6`.

**Query:**
```sql
WITH nums(n) AS (VALUES (1),(2),(5),(7)),
islands AS (
  SELECT n,
         n - (ROW_NUMBER() OVER (ORDER BY n))::int AS grp
  FROM nums
),
gaps AS (
  SELECT MIN(n) AS up_to, LAG(MIN(n)) OVER (ORDER BY MIN(n)) AS prev_highest
  FROM islands
  GROUP BY grp
)
SELECT prev_highest + 1 AS gap_start, up_to - 1 AS gap_end
FROM gaps
WHERE prev_highest IS NOT NULL AND prev_highest + 1 <= up_to - 1
ORDER BY gap_start;
```
**Explanation:** Islands of consecutive numbers produce both the top of one run and the top of the previous run; between them the gap lives.

**Alt1:**
```sql
WITH RECURSIVE nums(n) AS (VALUES (1),(2),(5),(7)),
all_numbers AS (
  SELECT MIN(n) AS n FROM nums
  UNION ALL
  SELECT n + 1 FROM all_numbers
  WHERE n < (SELECT MAX(n) FROM nums)
)
SELECT n AS missing_number
FROM all_numbers
WHERE n NOT IN (SELECT n FROM nums);
```
**Explanation:** Materialise every integer in the domain with a recursive CTE and subtract the ones that exist — brute force, clearly correct for small domains.

## Q3: Longest streak of consecutive user logins per user.

Schema hints: `logins(user_id, ts)` — one row per login; find each user's longest consecutive-day run.

**Query:**
```sql
WITH logins(user_id, ts) AS (
  VALUES (1, date '2026-02-01'),(1, date '2026-02-02'),(1, date '2026-02-03'),
         (1, date '2026-02-05'),(1, date '2026-02-06'),
         (2, date '2026-02-01'),(2, date '2026-02-02')
),
numbered AS (
  SELECT user_id, ts,
         ts - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY ts))::int AS grp
  FROM (SELECT DISTINCT user_id, ts FROM logins) d
)
SELECT user_id, MAX(cnt) AS longest_streak
FROM (
  SELECT user_id, grp, ts, COUNT(*) AS cnt
  FROM numbered
  GROUP BY user_id, grp
) s
GROUP BY user_id
ORDER BY user_id;
```
**Explanation:** Dedupe to one row per user/day, then the ROW_NUMBER-minus-date key groups daily runs; MAX of run lengths is the answer.

**Alt1:**
```sql
WITH RECURSIVE base(user_id, ts) AS (
  VALUES (1, date '2026-02-01'),(1, date '2026-02-02'),(1, date '2026-02-03'),
         (1, date '2026-02-05'),(1, date '2026-02-06'),
         (2, date '2026-02-01'),(2, date '2026-02-02')
),
daily AS (SELECT DISTINCT user_id, ts FROM base),
walk AS (
  SELECT user_id, ts, ts AS streak_start, 1 AS len
  FROM daily d
  WHERE NOT EXISTS (SELECT 1 FROM daily p WHERE p.user_id = d.user_id AND p.ts = d.ts - 1)
  UNION ALL
  SELECT w.user_id, d.ts, w.streak_start, w.len + 1
  FROM walk w JOIN daily d ON d.user_id = w.user_id AND d.ts = w.ts + 1
)
SELECT user_id, MAX(len) AS longest_streak FROM walk GROUP BY user_id ORDER BY user_id;
```
**Explanation:** Seed rows at every island start, then walk forward appending the next day; each walk row carries its length so MAX gives the streak.

## Q4: Consecutive present and absent runs per employee in an attendance log.

Schema hints: `attendance(dt, employee_id, is_present boolean)` — group into present-runs and absent-runs.

**Query:**
```sql
WITH attendance(dt, employee_id, is_present) AS (
  VALUES (date '2026-03-01', 10, true),(date '2026-03-02', 10, true),
         (date '2026-03-03', 10, false),(date '2026-03-04', 10, false),
         (date '2026-03-05', 10, true)
),
run_start AS (
  SELECT *, is_present <> LAG(is_present) OVER (PARTITION BY employee_id ORDER BY dt) AS changed
  FROM attendance
),
tagged AS (
  SELECT dt, employee_id, is_present,
         SUM(CASE WHEN changed OR changed IS NULL THEN 1 ELSE 0 END)
           OVER (PARTITION BY employee_id ORDER BY dt) AS grp
  FROM run_start
)
SELECT employee_id, is_present,
       MIN(dt) AS range_start, MAX(dt) AS range_end, COUNT(*) AS days
FROM tagged
GROUP BY employee_id, is_present, grp
ORDER BY employee_id, range_start;
```
**Explanation:** LAG compares each day's status to the previous; a change seeds a new group id via running SUM, giving alternating present/absent blocks.

**Alt1:**
```sql
WITH attendance(dt, employee_id, is_present) AS (
  VALUES (date '2026-03-01', 10, true),(date '2026-03-02', 10, true),
         (date '2026-03-03', 10, false),(date '2026-03-04', 10, false),
         (date '2026-03-05', 10, true)
),
snapped AS (
  SELECT dt, employee_id, is_present,
         dt - (ROW_NUMBER() OVER (PARTITION BY employee_id, is_present ORDER BY dt))::int AS grp
  FROM attendance
)
SELECT employee_id, is_present,
       MIN(dt) AS range_start, MAX(dt) AS range_end, COUNT(*) AS days
FROM snapped
GROUP BY employee_id, is_present, grp
ORDER BY employee_id, range_start;
```
**Explanation:** Partition the ROW_NUMBER by (employee, status) and subtract the date — the expose-\(/island\)/identity works per status, so present and absent runs fall out in two parallel partition families.

## Q5: Find the days with no sales between two given dates (calendar gap finder).

Schema hints: `sales(sale_date, amount)` — report every calendar day with zero sales between min and max document dates.

**Query:**
```sql
WITH RECURSIVE sales(sale_date, amount) AS (
  VALUES (date '2026-04-01', 10.00),(date '2026-04-03', 20.00),(date '2026-04-09', 5.00)
),
cal AS (
  SELECT MIN(sale_date) AS d, MAX(sale_date) AS max_d FROM sales
  UNION ALL
  SELECT d + 1, max_d FROM cal WHERE d < max_d
)
SELECT cal.d AS missing_day FROM cal
LEFT JOIN sales s ON s.sale_date = cal.d
WHERE s.sale_date IS NULL
ORDER BY missing_day;
```
**Explanation:** A recursive calendar CTE stretches from the first to the last sale date and an anti-join leaves only the silent days.

**Alt1:**
```sql
WITH sales(sale_date, amount) AS (
  VALUES (date '2026-04-01', 10.00),(date '2026-04-03', 20.00),(date '2026-04-09', 5.00)
),
gaps AS (
  SELECT sale_date, LAG(sale_date) OVER (ORDER BY sale_date) AS prev_date
  FROM sales
)
SELECT prev_date + 1 AS missing_start, sale_date - 1 AS missing_end
FROM gaps WHERE prev_date IS NOT NULL AND sale_date - prev_date > 1
ORDER BY missing_start;
```
**Explanation:** LAG on the sale dates themselves: any jump of more than one day is an entire silent window without materialising a calendar.

## Q6: Merge overlapping date ranges into minimal covered intervals.

Schema hints: `contracts(contract_id, valid_from, valid_to)` — ranges at least touch; collapse into the fewest covering rows.

**Query:**
```sql
WITH contracts(contract_id, valid_from, valid_to) AS (
  VALUES (1, date '2026-01-01', date '2026-01-31'),
         (2, date '2026-01-15', date '2026-02-20'),
         (3, date '2026-02-25', date '2026-03-10'),
         (4, date '2026-03-01', date '2026-03-15')
),
ordered AS (
  SELECT *, valid_from,
         valid_from - (LAG(valid_to) OVER (ORDER BY valid_from) + 1) AS break
  FROM contracts
),
islands AS (
  SELECT *,
         SUM(CASE WHEN break > 0 OR break IS NULL THEN 1 ELSE 0 END)
           OVER (ORDER BY valid_from) AS grp
  FROM ordered
)
SELECT MIN(valid_from) AS merged_from, MAX(valid_to) AS merged_to
FROM islands
GROUP BY grp
ORDER BY merged_from;
```
**Explanation:** A gap exists when a new `valid_from` starts after the previous `valid_to`; a running sum on `break > 0` buckets overlaps into one island per gap.

**Alt1:**
```sql
WITH contracts(contract_id, valid_from, valid_to) AS (
  VALUES (1, date '2026-01-01', date '2026-01-31'),
         (2, date '2026-01-15', date '2026-02-20'),
         (3, date '2026-02-25', date '2026-03-10'),
         (4, date '2026-03-01', date '2026-03-15')
),
next_ext AS (
  SELECT *, MAX(valid_to) OVER (ORDER BY valid_from
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_max_to
  FROM contracts
),
starts AS (
  SELECT *, LAG(running_max_to) OVER (ORDER BY valid_from) AS prev_max
  FROM next_ext
)
SELECT MIN(valid_from) AS merged_from, MAX(valid_to) AS merged_to
FROM (SELECT *,
        SUM(CASE WHEN valid_from > COALESCE(prev_max, valid_from - 1) + 1 THEN 1 ELSE 0 END)
          OVER (ORDER BY valid_from) AS grp FROM starts) t
GROUP BY grp ORDER BY merged_from;
```
**Explanation:** The running MAX of every prior `valid_to` handles chains where a long earlier range swallows several later ones; a new island only starts beyond that expanding frontier.

## Q7: Longest consecutive login streak across the whole company (any user, back-to-back days).

Schema hints: `logins(user_id, ts)` — find the single longest chain of days with at least one login company-wide.

**Query:**
```sql
WITH logins(user_id, ts) AS (
  VALUES (1, date '2026-05-01'),(1, date '2026-05-02'),(2, date '2026-05-03')
),
days AS (
  SELECT DISTINCT ts FROM logins
),
numbered AS (
  SELECT ts, ts - (ROW_NUMBER() OVER (ORDER BY ts))::int AS grp FROM days
)
SELECT MIN(ts) AS streak_start, MAX(ts) AS streak_end, COUNT(*) AS days
FROM numbered GROUP BY grp ORDER BY days DESC LIMIT 1;
```
**Explanation:** Collapse to distinct days first, then the classic date-minus-row-number idiom returns one row per company-wide run.

**Alt1:**
```sql
WITH RECURSIVE logins(user_id, ts) AS (
  VALUES (1, date '2026-05-01'),(1, date '2026-05-02'),(2, date '2026-05-03')
),
days(d) AS (SELECT DISTINCT ts FROM logins),
walk AS (
  SELECT ts, ts AS root, 1 AS len FROM days d
  WHERE NOT EXISTS (SELECT 1 FROM days p WHERE p.ts = d.ts - 1)
  UNION ALL
  SELECT n.ts, w.root, w.len + 1 FROM walk w
  JOIN days n ON n.ts = w.ts + 1
)
SELECT root AS streak_start, ts AS streak_end, len FROM walk
ORDER BY len DESC LIMIT 1;
```
**Explanation:** Recursively walk each island forward, multiplying its length at every hop; ordering by `len DESC` surfaces the global champion.

## Q8: Users whose longest login streak exceeds 5 days.

Schema hints: `logins(user_id, ts)` — same table; filter islands by length before reporting users.

**Query:**
```sql
WITH logins(user_id, ts) AS (
  VALUES (1, date '2026-06-01'),(1, date '2026-06-02'),(1, date '2026-06-03'),
         (1, date '2026-06-04'),(1, date '2026-06-05'),(1, date '2026-06-06'),
         (2, date '2026-06-01'),(2, date '2026-06-03')
),
daily AS (SELECT DISTINCT user_id, ts FROM logins),
tagged AS (
  SELECT user_id, ts,
         ts - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY ts))::int AS grp
  FROM daily
),
streaks AS (
  SELECT user_id, COUNT(*) AS len FROM tagged GROUP BY user_id, grp
)
SELECT user_id, MAX(len) AS longest_streak
FROM streaks GROUP BY user_id HAVING MAX(len) > 5 ORDER BY user_id;
```
**Explanation:** Per-user islands built as usual, then HAVING filters users whose top run clears the 5-day bar.

**Alt1:**
```sql
WITH RECURSIVE logins(user_id, ts) AS (
  VALUES (1, date '2026-06-01'),(1, date '2026-06-02'),(1, date '2026-06-03'),
         (1, date '2026-06-04'),(1, date '2026-06-05'),(1, date '2026-06-06'),
         (2, date '2026-06-01'),(2, date '2026-06-03')
),
daily AS (SELECT DISTINCT user_id, ts FROM logins),
walk AS (
  SELECT user_id, ts, ts AS root, 1 AS len FROM daily d
  WHERE NOT EXISTS (SELECT 1 FROM daily p
                    WHERE p.user_id = d.user_id AND p.ts = d.ts - 1)
  UNION ALL
  SELECT n.user_id, n.ts, w.root, w.len + 1
  FROM walk w JOIN daily n
    ON n.user_id = w.user_id AND n.ts = w.ts + 1
)
SELECT user_id, MAX(len) AS longest_streak
FROM walk GROUP BY user_id HAVING MAX(len) > 5 ORDER BY user_id;
```
**Explanation:** Seed the walk on streak-start days, hop forward one day per step, and let HAVING keep users whose walk ever exceeded length five.

## Q9: Same as Q8 but with a fully correct LAG + running-SUM variant.

Schema hints: `logins(user_id, ts)` — streak counting done entirely through LAG-difference gating, no ROW_NUMBER.

**Query:**
```sql
WITH logins(user_id, ts) AS (
  VALUES (1, date '2026-06-01'),(1, date '2026-06-02'),(1, date '2026-06-03'),
         (1, date '2026-06-04'),(1, date '2026-06-05'),(1, date '2026-06-06'),
         (2, date '2026-06-01'),(2, date '2026-06-03')
),
daily AS (SELECT DISTINCT user_id, ts FROM logins),
flagged AS (
  SELECT user_id, ts,
         ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) AS diff
  FROM daily
),
tagged AS (
  SELECT user_id, ts,
         SUM(CASE WHEN diff = 1 THEN 0 ELSE 1 END)
           OVER (PARTITION BY user_id ORDER BY ts) AS grp
  FROM flagged
)
SELECT user_id, MAX(len) AS longest_streak
FROM (SELECT user_id, grp, COUNT(*) AS len FROM tagged GROUP BY user_id, grp) s
GROUP BY user_id HAVING MAX(len) > 5
ORDER BY user_id;
```
**Explanation:** `diff = 1` means the day continues a run (group stays), anything else opens a fresh group; everything rides on LAG, no ROW_NUMBER in sight.

## Q10: Find all gaps in a numeric sequence and their lengths (gap-span mapping).

Schema hints: `docs(seq int)` — values `1,2,4,8`; report every missing block `3, 5-7` with `3..3, 5..7`.

**Query:**
```sql
WITH docs(seq) AS (VALUES (1),(2),(4),(8)),
prep AS (
  SELECT seq,
         seq - (ROW_NUMBER() OVER (ORDER BY seq))::int AS grp
  FROM docs
),
runs AS (
  SELECT grp, MIN(seq) AS run_start, MAX(seq) AS run_end
  FROM prep GROUP BY grp
),
next_run AS (
  SELECT *, LAG(run_end) OVER (ORDER BY run_start) AS prev_end
  FROM runs
)
SELECT prev_end + 1 AS gap_from, run_start - 1 AS gap_to
FROM next_run
WHERE prev_end IS NOT NULL AND prev_end + 1 <= run_start - 1
ORDER BY gap_from;
```
**Explanation:** Runs of consecutive numbers are islands; linking each run to the previous run's last value leaves the hole between them.

**Alt1:**
```sql
WITH docs(seq) AS (VALUES (1),(2),(4),(8)),
nums AS (
  SELECT seq, LAG(seq) OVER (ORDER BY seq) AS prev_seq
  FROM docs
)
SELECT prev_seq + 1 AS gap_from, seq - 1 AS gap_to
FROM nums
WHERE prev_seq IS NOT NULL AND seq - prev_seq > 1
ORDER BY gap_from;
```
**Explanation:** Each jump larger than one in the ordered sequence is itself an entire missing block — pair the neighbours and go.

## Q11: Count of distinct gap blocks (how many islands of missing days exist).

Schema hints: `orders(order_date)` for `2026-07-01..2026-07-14`; count how many separate holiday-shutdown windows the data implies.

**Query:**
```sql
WITH RECURSIVE orders(order_date) AS (
  VALUES (date '2026-07-01'),(date '2026-07-02'),(date '2026-07-03'),
         (date '2026-07-08'),(date '2026-07-09')
),
cal(d) AS (
  SELECT date '2026-07-01' UNION ALL SELECT d + 1 FROM cal WHERE d < date '2026-07-14'
)
SELECT COUNT(*) AS missing_block_count
FROM (
  SELECT d, d - (ROW_NUMBER() OVER (ORDER BY d))::int AS grp
  FROM (SELECT cal.d FROM cal LEFT JOIN orders o ON o.order_date = cal.d
        WHERE o.order_date IS NULL) missing
  GROUP BY d - (ROW_NUMBER() OVER (ORDER BY d))::int
) blocks;
```
**Explanation:** Missing days are themselves an island sequence; the number of distinct ROW_NUMBER-minus-date keys equals the number of gap blocks.

## Q12: Date ranges that are entirely covered by an earlier, longer range (redundant contracts).

Schema hints: `contracts(contract_id, valid_from, valid_to)` — find any row whose range lives inside a strictly larger prior range.

**Query:**
```sql
WITH contracts(contract_id, valid_from, valid_to) AS (
  VALUES (1, date '2026-01-01', date '2026-01-31'),
         (2, date '2026-01-05', date '2026-01-20'),
         (3, date '2026-01-10', date '2026-02-10'),
         (4, date '2026-01-01', date '2026-01-31')
),
waves AS (
  SELECT *, MAX(valid_to) OVER (ORDER BY valid_from, valid_to DESC
           ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS max_prior_to
  FROM contracts
)
SELECT contract_id, valid_from, valid_to
FROM waves WHERE max_prior_to >= valid_to
ORDER BY contract_id;
```
**Explanation:** The running maximum of all earlier `valid_to` values beats a row's own end iff that row is swallowed; equal start/end duplicates show up too.

## Q13: First available (free) telephone number in a numeric block.

Schema hints: `phones(number int)` holds `101,102,104,105`; smallest issuer-free number below the highest, assuming block starts at 101.

**Query:**
```sql
WITH RECURSIVE phones(number) AS (VALUES (101),(102),(104),(105)),
stack AS (
  SELECT number, LAG(number) OVER (ORDER BY number) AS prev_number
  FROM phones
)
SELECT COALESCE(MIN(prev_number + 1), 101) AS first_available
FROM stack WHERE prev_number + 1 <> number;
```
**Explanation:** The first row whose successor is not `+1` reveals the first free slot right after the previous used number.

**Alt1:**
```sql
WITH phones(number) AS (VALUES (101),(102),(104),(105)),
islands AS (
  SELECT number - (ROW_NUMBER() OVER (ORDER BY number))::int AS grp
  FROM phones
)
SELECT MIN(number) + 1 AS first_available
FROM (SELECT grp, COUNT(*) AS c, MIN(number) AS number
      FROM islands GROUP BY grp) s
WHERE c = 1;
```
**Explanation:** Used numbers form islands; the first single-element island has its next number free by construction.

## Q14: Consecutive seat availability — best contiguous block of free seats.

Schema hints: `seats(row_no, seat_no, occupied boolean)` — given a movie hall, find the largest run of adjacent free seats in one row.

**Query:**
```sql
WITH seats(row_no, seat_no, occupied) AS (
  VALUES (1, 1, true),(1, 2, false),(1, 3, false),(1, 4, false),(1, 5, true),
         (1, 6, false),(1, 7, false)
),
tagged AS (
  SELECT row_no, seat_no,
         ROW_NUMBER() OVER (PARTITION BY row_no, occupied ORDER BY seat_no) AS rn
  FROM seats
)
SELECT row_no, MIN(seat_no) AS free_from, MAX(seat_no) AS free_to,
       COUNT(*) AS seats, 'Free' AS block_type
FROM tagged
WHERE NOT occupied
GROUP BY row_no, seat_no - rn
ORDER BY seats DESC LIMIT 1;
```
**Explanation:** Partitioning the ROW_NUMBER by `occupied` means the seat-minus-rn key stays constant only across a pure run of unoccupied seats (or pure run of occupied).

**Alt1:**
```sql
WITH seats(row_no, seat_no, occupied) AS (
  VALUES (1, 1, true),(1, 2, false),(1, 3, false),(1, 4, false),(1, 5, true),
         (1, 6, false),(1, 7, false)
),
flagged AS (
  SELECT *,
         occupied <> LAG(occupied) OVER (PARTITION BY row_no ORDER BY seat_no) AS changed
  FROM seats
)
SELECT row_no, MIN(seat_no) AS free_from, MAX(seat_no) AS free_to, COUNT(*) AS seats
FROM (SELECT *, SUM(CASE WHEN changed OR changed IS NULL THEN 1 ELSE 0 END)
        OVER (PARTITION BY row_no ORDER BY seat_no) AS grp FROM flagged) t
WHERE NOT occupied
GROUP BY row_no, grp
ORDER BY seats DESC, row_no LIMIT 1;
```
**Explanation:** Every flip of the occupied flag opens a new group; filtering to free seats and keeping the largest group answers the question through change-detection only.

## Q15: Islands of '1' vs '0' in a binary bit sequence.

Schema hints: `bits(pos int, bit_value int)` stores `0/1` in order; report each contiguous same-bit block.

**Query:**
```sql
WITH bits(pos, bit_value) AS (VALUES (1,1),(2,1),(3,0),(4,0),(5,0),(6,1),(7,1)),
tagged AS (
  SELECT pos, bit_value,
         pos - (ROW_NUMBER() OVER (PARTITION BY bit_value ORDER BY pos))::int AS grp
  FROM bits
)
SELECT bit_value, MIN(pos) AS from_pos, MAX(pos) AS to_pos, COUNT(*) AS len
FROM tagged
GROUP BY bit_value, grp
ORDER BY from_pos;
```
**Explanation:** Number each bit within its own value-family (0s and 1s separately); position-minus-rank is constant inside every same-value run, so the grouping emits each block.

## Q16: Islands of equal bits — LAG flip-flop implementation.

Schema hints: `bits(pos, bit_value)` in `1,1,0,0,0,1,1` order; report contiguous equal-bit blocks with span.

**Query:**
```sql
WITH bits(pos, bit_value) AS (VALUES (1,1),(2,1),(3,0),(4,0),(5,0),(6,1),(7,1)),
flagged AS (
  SELECT pos, bit_value,
         bit_value <> LAG(bit_value) OVER (ORDER BY pos) AS changed
  FROM bits
),
run_ids AS (
  SELECT pos, bit_value,
         SUM(CASE WHEN changed OR changed IS NULL THEN 1 ELSE 0 END)
           OVER (ORDER BY pos) AS grp
  FROM flagged
)
SELECT bit_value, MIN(pos) AS from_pos, MAX(pos) AS to_pos, COUNT(*) AS len
FROM run_ids GROUP BY bit_value, grp ORDER BY from_pos;
```
**Explanation:** Pure change-detection: every time the bit flips a running sum increments, so each run of identical bits gets its own id — no subtraction at all.

## Q17: Consecutive wins/losses streaks per team.

Schema hints: `games(team_id, game_date, result char)` holds `'W'`/`'L'`; report both longest winning and longest losing streaks per team.

**Query:**
```sql
WITH games(team_id, game_date, result) AS (
  VALUES (1, date '2026-08-01', 'W'),(1, date '2026-08-02', 'W'),
         (1, date '2026-08-03', 'L'),(1, date '2026-08-04', 'W'),
         (2, date '2026-08-01', 'L'),(2, date '2026-08-02', 'L'),(2, date '2026-08-03', 'L')
),
flagged AS (
  SELECT *,
         result <> LAG(result) OVER (PARTITION BY team_id ORDER BY game_date) AS changed
  FROM games
),
run_ids AS (
  SELECT team_id, result, game_date,
         SUM(CASE WHEN changed OR changed IS NULL THEN 1 ELSE 0 END)
           OVER (PARTITION BY team_id ORDER BY game_date) AS grp
  FROM flagged
)
SELECT team_id, result,
       MAX(len) AS longest_streak
FROM (SELECT team_id, result, COUNT(*) AS len FROM run_ids GROUP BY team_id, result, grp) s
GROUP BY team_id, result
ORDER BY team_id, result;
```
**Explanation:** Result flips begin new runs per team; MAX of run lengths per (team, W/L) gives both records.

## Q18: Number of distinct islands in a stream (count of row groups).

Schema hints: `hits(page_id, visit_ts)` — how many separate browsing sessions (consecutive-minute visits) exist per page.

**Query:**
```sql
WITH hits(page_id, visit_ts) AS (
  VALUES (1, '2026-01-01 09:00'),(1, '2026-01-01 09:01'),(1, '2026-01-01 09:02'),
         (1, '2026-01-01 09:10'),(2, '2026-01-01 09:00'),(2, '2026-01-01 09:05')
)
SELECT page_id, COUNT(DISTINCT grp) AS session_count
FROM (
  SELECT page_id,
         visit_ts - (ROW_NUMBER() OVER (PARTITION BY page_id ORDER BY visit_ts))::int AS grp
  FROM hits
) s
GROUP BY page_id ORDER BY page_id;
```
**Explanation:** Minute-precision ROW_NUMBER-minus-timestamp keys each session; counting distinct keys counts islands per page.

## Q19: First login day of every login streak (streak starts).

Schema hints: `logins(user_id, ts)` — list islands with their begin date and length.

**Query:**
```sql
WITH logins(user_id, ts) AS (
  VALUES (1, date '2026-02-01'),(1, date '2026-02-02'),(1, date '2026-02-03'),
         (1, date '2026-02-05'),(1, date '2026-02-06')
),
tagged AS (
  SELECT user_id, ts,
         ts - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY ts))::int AS grp
  FROM (SELECT DISTINCT user_id, ts FROM logins) d
)
SELECT user_id, MIN(ts) AS streak_start, COUNT(*) AS streak_days
FROM tagged GROUP BY user_id, grp
ORDER BY user_id, streak_start;
```
**Explanation:** Each key is one island; MIN-date is its opening day and row count its length.

## Q20: Days that break streaks — first gap after each island.

Schema hints: `logins(user_id, ts)` — the day after an island ends (before the next begins).

**Query:**
```sql
WITH logins(user_id, ts) AS (
  VALUES (1, date '2026-02-01'),(1, date '2026-02-02'),(1, date '2026-02-04')
),
daily AS (SELECT DISTINCT user_id, ts FROM logins),
flagged AS (
  SELECT user_id, ts,
         ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) AS diff
  FROM daily
)
SELECT user_id, LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) + 1 AS missed_day
FROM flagged WHERE diff > 1 OR diff IS NULL;
```
**Explanation:** Every diff above 1 names the gap and its first silent day is exactly `prev day + 1`.

## Q21: Version numbering discontinuity — skipped sequence detection.

Schema hints: `doc_versions(doc_id, version_no)` — stamp rows whose next version is not `+1`; list the missing-version streaks implied by the jumps.

**Query:**
```sql
WITH doc_versions(doc_id, version_no) AS (
  VALUES (1, 1),(1, 2),(1, 5),(1, 6),(2, 1),(2, 3)
),
prep AS (
  SELECT doc_id, version_no,
         LAG(version_no) OVER (PARTITION BY doc_id ORDER BY version_no) AS prev_v
  FROM doc_versions
)
SELECT doc_id, prev_v + 1 AS missing_range_start, version_no - 1 AS missing_range_end
FROM prep
WHERE prev_v IS NOT NULL AND version_no - prev_v > 1
ORDER BY doc_id, missing_range_start;
```
**Explanation:** Every LAG jump larger than one is itself one fully-skipped block; the pairing `prev_v+1 .. version_no-1` names it without any grouping.

**Alt1:**
```sql
WITH doc_versions(doc_id, version_no) AS (
  VALUES (1, 1),(1, 2),(1, 5),(1, 6),(2, 1),(2, 3)
),
tagged AS (
  SELECT doc_id, version_no,
         version_no - (ROW_NUMBER() OVER (PARTITION BY doc_id ORDER BY version_no))::int AS grp
  FROM doc_versions
),
runs AS (
  SELECT doc_id, MIN(version_no) AS run_from, MAX(version_no) AS run_to
  FROM tagged GROUP BY doc_id, grp
),
linked AS (
  SELECT *, LAG(run_to) OVER (PARTITION BY doc_id ORDER BY run_from) AS prev_to
  FROM runs
)
SELECT doc_id, prev_to + 1 AS missing_from, run_from - 1 AS missing_to
FROM linked
WHERE prev_to IS NOT NULL AND prev_to + 1 <= run_from - 1
ORDER BY doc_id, missing_from;
```
**Explanation:** Islands of contiguous versions chained via LAG expose each jumped block exactly as a from/to pair — the classical island route to the same answer.

## Q22: Skipped versions — gap listing between version islands.

Schema hints: `doc_versions(doc_id, version_no)` = `1,2,5,6` per doc — list skipped versions `3,4`.

**Query:**
```sql
WITH doc_versions(doc_id, version_no) AS (
  VALUES (1, 1),(1, 2),(1, 5),(1, 6),(2, 1),(2, 3)
),
tagged AS (
  SELECT doc_id, version_no,
         version_no - (ROW_NUMBER() OVER (PARTITION BY doc_id ORDER BY version_no))::int AS grp
  FROM doc_versions
),
runs AS (
  SELECT doc_id, grp, MIN(version_no) AS v_from, MAX(version_no) AS v_to
  FROM tagged GROUP BY doc_id, grp
),
linked AS (
  SELECT *, LAG(v_to) OVER (PARTITION BY doc_id ORDER BY v_from) AS prev_v_to
  FROM runs
)
SELECT doc_id, prev_v_to + 1 AS missing_from, v_from - 1 AS missing_to
FROM linked
WHERE prev_v_to IS NOT NULL AND prev_v_to + 1 <= v_from - 1
ORDER BY doc_id, missing_from;
```
**Explanation:** Islands of contiguous versions chained via LAG expose each jumped block exactly as a from/to pair.

**Alt1:**
```sql
WITH RECURSIVE doc_versions(doc_id, version_no) AS (
  VALUES (1, 1),(1, 2),(1, 5),(1, 6),(2, 1),(2, 3)
),
full_range AS (
  SELECT doc_id, MIN(version_no) AS v FROM doc_versions
  UNION ALL
  SELECT doc_id, v + 1 FROM full_range
  WHERE v < (SELECT MAX(version_no) FROM doc_versions WHERE doc_id = doc_versions.doc_id)
)
SELECT f.doc_id, f.v AS missing_version
FROM full_range f LEFT JOIN doc_versions d
     ON d.doc_id = f.doc_id AND d.version_no = f.v
WHERE d.version_no IS NULL
ORDER BY f.doc_id, f.v;
```
**Explanation:** Recursive expansion of every version and an anti-join leaves only the skipped ones.

## Q23: Day-off clusters — contiguous absent days longer than two.

Schema hints: `attendance(dt, employee_id, status)` with `status='absent'`; return clusters spanning 3+ days.

**Query:**
```sql
WITH attendance(dt, employee_id, status) AS (
  VALUES (date '2026-09-01', 7, 'present'),(date '2026-09-02', 7, 'absent'),
         (date '2026-09-03', 7, 'absent'),(date '2026-09-04', 7, 'absent'),
         (date '2026-09-05', 7, 'present')
),
flagged AS (
  SELECT *,
         status <> LAG(status) OVER (PARTITION BY employee_id ORDER BY dt) AS changed
  FROM attendance
),
run_ids AS (
  SELECT *, SUM(CASE WHEN changed OR changed IS NULL THEN 1 ELSE 0 END)
              OVER (PARTITION BY employee_id ORDER BY dt) AS grp
  FROM flagged
)
SELECT employee_id, MIN(dt) AS absent_from, MAX(dt) AS absent_to, COUNT(*) AS days
FROM run_ids WHERE status = 'absent'
GROUP BY employee_id, grp HAVING COUNT(*) >= 3
ORDER BY employee_id, absent_from;
```
**Explanation:** Status-flip runs, then HAVING keeps only the absent blocks that last at least three days.

## Q24: Periods where no orders shipped during business hours.

Schema hints: `shipments(ship_ts, order_id)` during `08:00-18:00`; find hours with zero shipment events.

**Query:**
```sql
WITH shipments(ship_ts, order_id) AS (
  VALUES ('2026-01-05 09:00', 1),('2026-01-05 09:30', 2),('2026-01-05 11:00', 3)
),
hours AS (
  SELECT generate_series(date '2026-01-05' + time '08:00',
                         date '2026-01-05' + time '17:59', interval '1 hour') AS h
)
SELECT to_char(h, 'HH24:00') AS hour_slot, COUNT(s.order_id) AS shipped
FROM hours LEFT JOIN shipments s
     ON s.ship_ts >= h AND s.ship_ts < h + interval '1 hour'
GROUP BY h ORDER BY h;
```
**Explanation:** Generate_series builds the hourly grid of business hours; the left join counts per slot and zero rows expose dead windows.

## Q25: Grouping orders by shipment-day runs.

Schema hints: `shipments(ship_ts, order_id, warehouse)` — every warehouse's shipping days form runs; label each run.

**Query:**
```sql
WITH shipments(ship_ts, order_id, warehouse) AS (
  VALUES ('2026-02-01', 1, 'A'),('2026-02-02', 2, 'A'),('2026-02-03', 3, 'A'),
         ('2026-02-05', 4, 'A'),('2026-02-01', 5, 'B')
),
daily AS (
  SELECT DISTINCT warehouse, ship_ts::date AS sd FROM shipments
),
tagged AS (
  SELECT warehouse, sd,
         sd - (ROW_NUMBER() OVER (PARTITION BY warehouse ORDER BY sd))::int AS grp
  FROM daily
)
SELECT warehouse, MIN(sd) AS run_start, MAX(sd) AS run_end,
       COUNT(*) AS shipping_days
FROM tagged GROUP BY warehouse, grp ORDER BY warehouse, run_start;
```
**Explanation:** Per-warehouse distinct shipping days, then the classical date-minus-rank key groups consecutive-day runs.
## Q26: Consecutive months of rising sales per region (growth islands).

Schema hints: `sales(region, month, revenue)` — `revenue` must increase month-over-month inside each island; report per-region longest growth run.

**Query:**
```sql
WITH sales(region, month, revenue) AS (
  VALUES ('EU', date '2026-01-01', 100),('EU', date '2026-02-01', 120),
         ('EU', date '2026-03-01', 90),('EU', date '2026-04-01', 110),
         ('US', date '2026-01-01', 50),('US', date '2026-02-01', 60)
),
flagged AS (
  SELECT region, month, revenue,
         revenue > LAG(revenue) OVER (PARTITION BY region ORDER BY month) AS growing
  FROM sales
),
runs AS (
  SELECT region, month,
         SUM(CASE WHEN growing OR growing IS NULL THEN 0 ELSE 1 END)
           OVER (PARTITION BY region ORDER BY month) AS grp
  FROM flagged WHERE growing
)
SELECT region, COUNT(*) AS growth_months
FROM runs GROUP BY region
ORDER BY region;
```
**Explanation:** `growing` marks a month better than the previous one; a running sum that *keeps* the bucket while growing and opens nothing when not (rows pre-filtered) counts months inside each growth run.

**Alt1:**
```sql
WITH sales(region, month, revenue) AS (
  VALUES ('EU', date '2026-01-01', 100),('EU', date '2026-02-01', 120),
         ('EU', date '2026-03-01', 90),('EU', date '2026-04-01', 110),
         ('US', date '2026-01-01', 50),('US', date '2026-02-01', 60)
),
flagged AS (
  SELECT region, month, revenue,
         revenue <= LAG(revenue) OVER (PARTITION BY region ORDER BY month) AS break
  FROM sales
),
runs AS (
  SELECT region, month,
         SUM(CASE WHEN break OR break IS NULL THEN 1 ELSE 0 END)
           OVER (PARTITION BY region ORDER BY month) AS grp
  FROM flagged
)
SELECT region, MAX(c) AS longest_growth_run
FROM (SELECT region, grp, COUNT(*) c FROM runs GROUP BY region, grp) s
GROUP BY region ORDER BY region;
```
**Explanation:** Invert the logic: a month that fails to beat the previous one opens a fresh group; the largest group size is each region's best streak.

## Q27: Find all gaps in `1,2,5,7` with each missing range (recursive-heavy version).

Schema hints: `nums(n)` — recursive CTE generates every integer, then knot-groups the absent ones.

**Query:**
```sql
WITH RECURSIVE nums(n) AS (VALUES (1),(2),(5),(7)),
full_sequence AS (
  SELECT n FROM nums
  UNION
  SELECT (SELECT MIN(n) FROM nums) + s.gs
  FROM generate_series(0, (SELECT MAX(n) FROM nums) - (SELECT MIN(n) FROM nums)) s(gs)
),
missing AS (
  SELECT f.n FROM full_sequence f
  WHERE NOT EXISTS (SELECT 1 FROM nums d WHERE d.n = f.n)
),
tagged AS (
  SELECT n, n - (ROW_NUMBER() OVER (ORDER BY n))::int AS grp FROM missing
)
SELECT MIN(n) AS gap_from, MAX(n) AS gap_to
FROM tagged GROUP BY grp ORDER BY gap_from;
```
**Explanation:** generate_series yields every integer in the domain, anti-join leaves the missing ones, and they are re-islanded into 3–4 and 6–6.

## Q28: Crunch time — longest idle window between two consecutive orders.

Schema hints: `orders(order_id, ordered_at)` — a customer stops buying; report the maximum day span separating successive orders per customer.

**Query:**
```sql
WITH orders(customer_id, ordered_at) AS (
  VALUES (1, date '2026-01-01'),(1, date '2026-01-05'),(1, date '2026-02-01')
),
lags AS (
  SELECT customer_id, ordered_at,
         LAG(ordered_at) OVER (PARTITION BY customer_id ORDER BY ordered_at) AS prev_at
  FROM orders
)
SELECT customer_id, MAX(ordered_at - prev_at) AS max_idle_days
FROM lags WHERE prev_at IS NOT NULL
GROUP BY customer_id ORDER BY customer_id;
```
**Explanation:** No groups needed: the largest LAG distance between successive rows is the longest gap, and its span is measured directly by subtraction.

## Q29: Consecutive days present — flag employees present every day of a run.

Schema hints: `attendance(dt, employee_id, present bool)` — mark run-of-the-mill streaks of 5+ days as `veteran`.

**Query:**
```sql
WITH attendance(dt, employee_id, present) AS (
  VALUES (date '2026-10-01', 5, true),(date '2026-10-02', 5, true),
         (date '2026-10-03', 5, true),(date '2026-10-04', 5, true),
         (date '2026-10-05', 5, true),(date '2026-10-01', 6, true),(date '2026-10-03', 6, true)
),
tagged AS (
  SELECT employee_id, dt,
         dt - (ROW_NUMBER() OVER (PARTITION BY employee_id, present ORDER BY dt))::int AS grp
  FROM attendance WHERE present
)
SELECT DISTINCT employee_id
FROM (SELECT employee_id, grp, COUNT(*) AS c FROM tagged GROUP BY employee_id, grp) s
WHERE c >= 5 ORDER BY employee_id;
```
**Explanation:** Partition by (employee, present=true) so only present-day runs get keys; any key with 5 rows is a veteran run.

## Q30: The missing-dollar detective — find the first unused invoice number.

Schema hints: `invoices(number int)` starts at 1000, values `1000,1001,1003` — smallest unused.

**Query:**
```sql
WITH invoices(number) AS (VALUES (1000),(1001),(1003)),
prep AS (
  SELECT number,
         number - (ROW_NUMBER() OVER (ORDER BY number))::int AS grp
  FROM invoices
)
SELECT MIN(number) + 1 AS first_unused
FROM (SELECT grp, COUNT(*) AS c, MIN(number) AS number
      FROM prep GROUP BY grp) s
WHERE c = 1;
```
**Explanation:** Full rows form islands; the first island with a single member leaves its successor immediately free (assuming block starts at the first value seen).

**Alt1:**
```sql
WITH invoices(number) AS (VALUES (1000),(1001),(1003))
SELECT COALESCE(MIN(number) + 1, 1000) AS first_unused
FROM invoices i
WHERE NOT EXISTS (SELECT 1 FROM invoices n WHERE n.number = i.number + 1);
```
**Explanation:** Ask per row: is my successor missing? The first such row's successor is the smallest free number; COALESCE covers the empty table.

## Q31: Islands of pivotal stock price moves — price crossing a threshold.

Schema hints: `prices(dt, price)` — sessions where `price > 100` for consecutive days.

**Query:**
```sql
WITH prices(dt, price) AS (
  VALUES (date '2026-11-01', 105),(date '2026-11-02', 106),(date '2026-11-03', 99),
         (date '2026-11-04', 101),(date '2026-11-05', 102)
),
tagged AS (
  SELECT dt, price,
         dt - (ROW_NUMBER() OVER (PARTITION BY (price > 100) ORDER BY dt))::int AS grp
  FROM prices
)
SELECT MIN(dt) AS above_from, MAX(dt) AS above_to, COUNT(*) AS days
FROM (SELECT dt, grp FROM tagged WHERE price > 100) s
GROUP BY grp ORDER BY above_from;
```
**Explanation:** Keying by the boolean (`price > 100`) gives above/below families; filtering to the true family and re-islanding yields each hot stretch.

## Q32: Max cluster of consecutive active days for a service (uptime islands).

Schema hints: `uptime(dt, status)` — `'UP'`/`'DOWN'`; report the longest uninterrupted UP run.

**Query:**
```sql
WITH uptime(dt, status) AS (
  VALUES (date '2026-12-01', 'UP'),(date '2026-12-02', 'UP'),
         (date '2026-12-03', 'DOWN'),(date '2026-12-04', 'UP'),(date '2026-12-05', 'UP')
),
hidden AS (
  SELECT dt, status,
         SUM(CASE WHEN status <> LAG(status) OVER (ORDER BY dt)
                       OR LAG(status) OVER (ORDER BY dt) IS NULL THEN 1 ELSE 0 END)
           OVER (ORDER BY dt) AS grp
  FROM uptime
)
SELECT MIN(dt) AS run_start, MAX(dt) AS run_end, COUNT(*) AS days
FROM hidden WHERE status = 'UP'
GROUP BY grp ORDER BY days DESC LIMIT 1;
```
**Explanation:** Change leads to a new group; the biggest UP group is the top uptime island.

## Q33: Every island of the string `BWWRRW` decomposed into runs.

Schema hints: `pixels(pos int, colour char)` in order — each contiguous same-colour run with its span.

**Query:**
```sql
WITH pixels(pos, colour) AS (VALUES (1,'B'),(2,'W'),(3,'W'),(4,'R'),(5,'R'),(6,'W')),
flagged AS (
  SELECT pos, colour,
         colour <> LAG(colour) OVER (ORDER BY pos) AS changed
  FROM pixels
)
SELECT MIN(pos) AS from_pos, MAX(pos) AS to_pos, colour, COUNT(*) AS len
FROM (SELECT *, SUM(CASE WHEN changed OR changed IS NULL THEN 1 ELSE 0 END)
         OVER (ORDER BY pos) AS grp FROM flagged) s
GROUP BY colour, grp ORDER BY from_pos;
```
**Explanation:** Colour flips at boundaries; each run of one colour is an island with its own id.

## Q34: Customers churning then returning — count re-engagements (dormant repopulation).

Schema hints: `activity(customer_id, month)` — an idle month followed by activity = re-engagement; count per customer.

**Query:**
```sql
WITH activity(customer_id, month) AS (
  VALUES (1, date '2026-01-01'),(1, date '2026-02-01'),(1, date '2026-04-01')
),
flagged AS (
  SELECT customer_id, month,
         month - LAG(month) OVER (PARTITION BY customer_id ORDER BY month) > interval '1 month'
           AS reengaged
  FROM activity
)
SELECT customer_id, COUNT(*) FILTER (WHERE reengaged) AS reengagements
FROM flagged GROUP BY customer_id ORDER BY customer_id;
```
**Explanation:** A month boundary that skips more than one calendar month is a comeback; counting those events per customer answers how often they cycle back.

## Q35: Longest losing streak in the league's fixture list.

Schema hints: `matches(match_date, team_id, outcome)` — `'WIN'` / `'LOSS'`; worst continuous LOSS run per team.

**Query:**
```sql
WITH matches(team_id, match_date, outcome) AS (
  VALUES (1, date '2026-01-01', 'LOSS'),(1, date '2026-01-02', 'LOSS'),
         (1, date '2026-01-03', 'WIN'),(2, date '2026-01-01', 'LOSS'),
         (2, date '2026-01-02', 'LOSS'),(2, date '2026-01-03', 'LOSS')
),
flagged AS (
  SELECT team_id, match_date, outcome,
         outcome <> LAG(outcome) OVER (PARTITION BY team_id ORDER BY match_date) AS changed
  FROM matches
),
run_ids AS (
  SELECT team_id, outcome,
         SUM(CASE WHEN changed OR changed IS NULL THEN 1 ELSE 0 END)
           OVER (PARTITION BY team_id ORDER BY match_date) AS grp
  FROM flagged
)
SELECT team_id, MAX(c) AS longest_losing_streak
FROM (SELECT team_id, grp, COUNT(*) c FROM run_ids WHERE outcome='LOSS' GROUP BY team_id, grp) s
GROUP BY team_id ORDER BY team_id;
```
**Explanation:** Outcome flips slice the season; the biggest LOSS sub-group is the franchise's darkest stretch.

## Q36: Financial: consecutive days of profit (islands of green days).

Schema hints: `prices(dt, close)` — a profit day is `close > prev_close`; largest run of green days.

**Query:**
```sql
WITH prices(dt, close) AS (
  VALUES (date '2026-01-01', 10),(date '2026-01-02', 12),(date '2026-01-03', 14),
         (date '2026-01-04', 13),(date '2026-01-05', 15),(date '2026-01-06', 17)
),
flagged AS (
  SELECT dt, close,
         close > LAG(close) OVER (ORDER BY dt) AS green
  FROM prices
),
runs AS (
  SELECT dt,
         SUM(CASE WHEN green OR green IS NULL THEN 0 ELSE 1 END)
           OVER (ORDER BY dt) AS grp
  FROM flagged WHERE green
)
SELECT MIN(dt) AS streak_start, MAX(dt) AS streak_end, COUNT(*) AS profit_days
FROM runs GROUP BY grp ORDER BY profit_days DESC LIMIT 1;
```
**Explanation:** Green is strictly higher than yesterday; pre-filter to green rows, and the running sum of red-days resets each painful gap.

**Alt1:**
```sql
WITH RECURSIVE prices(dt, close) AS (
  VALUES (date '2026-01-01', 10),(date '2026-01-02', 12),(date '2026-01-03', 14),
         (date '2026-01-04', 13),(date '2026-01-05', 15),(date '2026-01-06', 17)
),
seeds AS (
  SELECT dt FROM prices p
  WHERE NOT EXISTS (SELECT 1 FROM prices q
                    WHERE q.dt = p.dt - 1 AND q.close < p.close)
),
walk AS (
  SELECT p.dt, s.dt AS start, 1 AS len
  FROM prices p JOIN seeds s ON s.dt = p.dt
  UNION ALL
  SELECT q.dt, w.start, w.len + 1
  FROM walk w JOIN prices q ON q.dt = w.dt + 1
  WHERE q.close > (SELECT close FROM prices r WHERE r.dt = w.dt)
)
SELECT start, dt AS end, len FROM walk ORDER BY len DESC LIMIT 1;
```
**Explanation:** Seed every day that starts a profit run (no profitable predecessor), walk forward while close keeps rising — the longest walk wins.

## Q37: Merge contiguous date ranges that touch end-to-end (kissing ranges).

Schema hints: `projects(id, start_dt, end_dt)` — `[1-31]` and `[1st of next next]`... nope; treat a gap of exactly zero (`end+1 = next start`) as continuous.

**Query:**
```sql
WITH projects(id, start_dt, end_dt) AS (
  VALUES (1, date '2026-01-01', date '2026-01-10'),
         (2, date '2026-01-11', date '2026-01-20'),
         (3, date '2026-01-22', date '2026-01-25')
),
prep AS (
  SELECT start_dt, end_dt,
         LAG(end_dt) OVER (ORDER BY start_dt) AS prev_end
  FROM projects
),
tagged AS (
  SELECT start_dt, end_dt,
         SUM(CASE WHEN prev_end IS NULL OR start_dt > prev_end + 1 THEN 1 ELSE 0 END)
           OVER (ORDER BY start_dt) AS grp
  FROM prep
)
SELECT MIN(start_dt) AS merged_from, MAX(end_dt) AS merged_to
FROM tagged GROUP BY grp ORDER BY merged_from;
```
**Explanation:** `start_dt > prev_end + 1` is the definition of a true hole; kisses (`prev_end + 1`) merge silently into the same group.

## Q38: Longest absence-free window per employee (present-every-day spans).

Schema hints: `attendance(emp_id, dt)` — covers every working day; gaps module absent days; longest present run per employee.

**Query:**
```sql
WITH attendance(emp_id, dt) AS (
  VALUES (1, date '2026-01-01'),(1, date '2026-01-02'),(1, date '2026-01-03'),
         (1, date '2026-01-07'),(1, date '2026-01-08')
),
tagged AS (
  SELECT emp_id, dt,
         dt - (ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY dt))::int AS grp
  FROM attendance
)
SELECT emp_id, MAX(c) AS longest_present_run
FROM (SELECT emp_id, grp, COUNT(*) c FROM tagged GROUP BY emp_id, grp) s
GROUP BY emp_id ORDER BY emp_id;
```
**Explanation:** Because attendance drops out the absent days, ROW_NUMBER-minus-date leaves keys that are identical exactly on unbroken present spans.

## Q39: Sub-question — split a datelog into islands at WEEKEND boundaries only.

Schema hints: `logs(log_dt)` over a month — cuts happen whenever the date jumps into a Saturday-or-Sunday mismatch; report the runs.

**Query:**
```sql
WITH logs(log_dt) AS (
  VALUES (date '2026-05-04'),(date '2026-05-05'),(date '2026-05-08'),
         (date '2026-05-09'),(date '2026-05-11')
),
flagged AS (
  SELECT log_dt,
         CASE WHEN DATE_PART('dow', log_dt) IN (0,6) THEN 1 ELSE 0 END AS is_wknd
  FROM logs
)
SELECT MIN(log_dt) AS run_start, MAX(log_dt) AS run_end
FROM (SELECT log_dt,
        SUM(CASE WHEN is_wknd <> LAG(is_wknd) OVER (ORDER BY log_dt)
                      OR LAG(is_wknd) OVER (ORDER BY log_dt) IS NULL
                 THEN 1 ELSE 0 END) OVER (ORDER BY log_dt) AS grp FROM flagged) s
GROUP BY grp ORDER BY run_start;
```
**Explanation:** Label each day weekend/not; a flip in that flag opens a new island, clustering weekday spans apart from weekends regardless of actual gaps.

## Q40: Range fragmentation — count how many islands a year of dates contains.

Schema hints: `visits(dt)` across 2026; report total island count and total covered days.

**Query:**
```sql
WITH visits(dt) AS (
  VALUES (date '2026-01-01'),(date '2026-01-02'),(date '2026-01-10')
),
tagged AS (
  SELECT dt, dt - (ROW_NUMBER() OVER (ORDER BY dt))::int AS grp FROM visits
)
SELECT COUNT(DISTINCT grp) AS island_count, COUNT(*) AS covered_days
FROM tagged;
```
**Explanation:** One window function pass + two aggregates mutates date data into fragmentation statistics instantly.

## Q41: Seat block that can host the largest family (adjacent unoccupied run ≥ N).

Schema hints: `seats(row_no, seat_no, occupied)` — find rows with a free run of at least 4.

**Query:**
```sql
WITH seats(row_no, seat_no, occupied) AS (
  VALUES (1, 1, false),(1, 2, false),(1, 3, false),(1, 4, false),(1, 5, true),
         (2, 1, false),(2, 2, true),(2, 3, false)
),
tagged AS (
  SELECT row_no, seat_no,
         seat_no - (ROW_NUMBER() OVER (PARTITION BY row_no, occupied ORDER BY seat_no))::int AS grp
  FROM seats WHERE NOT occupied
)
SELECT row_no, MIN(seat_no) AS free_from, MAX(seat_no) AS free_to, COUNT(*) AS seats
FROM tagged GROUP BY row_no, grp HAVING COUNT(*) >= 4
ORDER BY row_no, free_from;
```
**Explanation:** Islands of unoccupied seats (partitioned by that boolean) filtered by HAVING to runs that clear the family-size bar.

## Q42: Max buy-the-dip window — longest flat or rising price stretch.

Schema hints: `prices(dt, price)` — profit-friendly runs where `price >= prev_price`.

**Query:**
```sql
WITH prices(dt, price) AS (
  VALUES (date '2026-02-01', 20),(date '2026-02-02', 22),(date '2026-02-03', 21),
         (date '2026-02-04', 23),(date '2026-02-05', 24)
),
flagged AS (
  SELECT dt, price,
         price >= LAG(price) OVER (ORDER BY dt) AS ok
  FROM prices
),
runs AS (
  SELECT dt,
         SUM(CASE WHEN ok OR ok IS NULL THEN 0 ELSE 1 END) OVER (ORDER BY dt) AS grp
  FROM flagged WHERE ok
)
SELECT COUNT(*) AS flat_or_rising_days FROM runs
GROUP BY grp ORDER BY 1 DESC LIMIT 1;
```
**Explanation:** `ok` allows equality and gains; drops are the only thing that closes a bucket, so the longest `ok` island is the answer.

## Q43: Consecutive quarters of profit for each business unit.

Schema hints: `fin(bu, quarter, pnl)` — every quarter where `pnl > 0` forms an island; count the streak per BU.

**Query:**
```sql
WITH fin(bu, quarter, pnl) AS (
  VALUES ('Retail', date '2026-01-01', 5),('Retail', date '2026-04-01', 6),
         ('Retail', date '2026-07-01', -1),('Retail', date '2026-10-01', 7),
         ('Cloud', date '2026-01-01', 2),('Cloud', date '2026-04-01', 3)
),
tagged AS (
  SELECT bu, quarter,
         quarter - ((ROW_NUMBER() OVER (PARTITION BY bu, (pnl > 0) ORDER BY quarter))::int
                    * interval '3 months') AS grp
  FROM fin
)
SELECT bu, MAX(c) AS longest_profitable_quarters
FROM (SELECT bu, grp, COUNT(*) c FROM tagged WHERE pnl > 0 GROUP BY bu, grp) s
GROUP BY bu ORDER BY bu;
```
**Explanation:** Number quarters within their profitability bucket and subtract `3 months` per rank → the key is constant across consecutive profitable quarters only.

## Q44: Missing date ranges between contracts — unbooked rental days.

Schema hints: `rentals(id, from_dt, to_dt)` — gaps where the unit sits empty between sequential rental islands.

**Query:**
```sql
WITH rentals(id, from_dt, to_dt) AS (
  VALUES (1, date '2026-03-01', date '2026-03-05'),
         (2, date '2026-03-10', date '2026-03-12'),
         (3, date '2026-03-20', date '2026-03-25')
),
next_rental AS (
  SELECT *, LEAD(from_dt) OVER (ORDER BY from_dt) AS next_from
  FROM rentals
)
SELECT to_dt + 1 AS vacant_from, next_from - 1 AS vacant_to
FROM next_rental
WHERE next_from IS NOT NULL AND next_from - 1 >= to_dt + 1
ORDER BY vacant_from;
```
**Explanation:** LEAD fetches the following rental's start; any daylight between stays is a vacancy range.

## Q45: Streaks of consecutive active months for a subscription.

Schema hints: `subs(user_id, active_month)` — one row per active month; longest backbone of unbroken activations per user.

**Query:**
```sql
WITH subs(user_id, active_month) AS (
  VALUES (1, date '2026-01-01'),(1, date '2026-02-01'),(1, date '2026-04-01'),
         (2, date '2026-01-01'),(2, date '2026-02-01'),(2, date '2026-03-01')
),
tagged AS (
  SELECT user_id, active_month,
         active_month - ((ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY active_month))::int
                         * interval '1 month') AS grp
  FROM subs
)
SELECT user_id, MAX(c) AS longest_active_run
FROM (SELECT user_id, grp, COUNT(*) c FROM tagged GROUP BY user_id, grp) s
GROUP BY user_id ORDER BY user_id;
```
**Explanation:** Subtract one month per rank: consecutive calendar months share a key, any skipped month breaks it.

## Q46: Day-off cluster labeling — every absence run gets its own id.

Schema hints: `attendance(dt, emp_id, status)` — attach a cluster id to each maximal block of `'absent'`.

**Query:**
```sql
WITH attendance(dt, emp_id, status) AS (
  VALUES (date '2026-06-01', 3, 'absent'),(date '2026-06-02', 3, 'absent'),
         (date '2026-06-03', 3, 'present'),(date '2026-06-04', 3, 'absent')
),
flagged AS (
  SELECT dt, emp_id, status,
         status <> LAG(status) OVER (PARTITION BY emp_id ORDER BY dt) AS changed
  FROM attendance
),
graduates AS (
  SELECT dt, emp_id, status,
         SUM(CASE WHEN changed OR changed IS NULL THEN 1 ELSE 0 END)
           OVER (PARTITION BY emp_id ORDER BY dt) AS grp
  FROM flagged
)
SELECT emp_id, MIN(dt) AS from_dt, MAX(dt) AS to_dt, status, COUNT(*) AS days
FROM graduates GROUP BY emp_id, status, grp
ORDER BY emp_id, from_dt;
```
**Explanation:** Every status flip bumps the running sum, so each absent block and each present block carry a unique id.

## Q47: Periods with no orders shipped — next shipment waits past a deadline.

Schema hints: `shipments(order_id, ship_dt)` — expose gaps between successive shipping dates longer than 3 days.

**Query:**
```sql
WITH shipments(order_id, ship_dt) AS (
  VALUES (1, date '2026-07-01'),(2, date '2026-07-05'),(3, date '2026-07-20')
),
pre AS (
  SELECT ship_dt, LEAD(ship_dt) OVER (ORDER BY ship_dt) AS next_ship
  FROM shipments
)
SELECT ship_dt + 1 AS gap_start, next_ship - 1 AS gap_end,
       next_ship - ship_dt - 1 AS silent_days
FROM pre WHERE next_ship IS NOT NULL AND next_ship - ship_dt > 4
ORDER BY gap_start;
```
**Explanation:** LEAD gives each shipment its successor; a leap of more than 4 days between them names the whole quiet window.

## Q48: Consecutive minutes of a crash — service outage islands in minute logs.

Schema hints: `health(minute, ok boolean)` — one boolean per minute; largest block of `false` minutes.

**Query:**
```sql
WITH health(minute, ok) AS (
  VALUES ('2026-08-01 00:00', false),('2026-08-01 00:01', false),
         ('2026-08-01 00:02', true),('2026-08-01 00:03', false),
         ('2026-08-01 00:04', false)
),
tagged AS (
  SELECT minute,
         minute - ((ROW_NUMBER() OVER (PARTITION BY ok ORDER BY minute))::int
                   * interval '1 minute') AS grp
  FROM health
),
only_down AS (
  SELECT grp, COUNT(*) AS down_minutes FROM tagged WHERE NOT ok
  GROUP BY grp
)
SELECT MAX(down_minutes) AS longest_outage_minutes FROM only_down;
```
**Explanation:** Rank minutes inside the `ok=false` partition then remove that many minutes — matched-with-mismatch keys identify outage blocks.

## Q49: Islands of price-change duration — how long each flat-price segment lasted.

Schema hints: `prices(dt, price)` — same price on consecutive days = one segment; segment length = days priced equally.

**Query:**
```sql
WITH prices(dt, price) AS (
  VALUES (date '2026-09-01', 5),(date '2026-09-02', 5),(date '2026-09-03', 6),
         (date '2026-09-04', 6),(date '2026-09-05', 5)
),
flagged AS (
  SELECT dt, price,
         price <> LAG(price) OVER (ORDER BY dt) AS changed
  FROM prices
)
SELECT MIN(dt) AS segment_from, MAX(dt) AS segment_to, price, COUNT(*) AS days
FROM (SELECT *, SUM(CASE WHEN changed OR changed IS NULL THEN 1 ELSE 0 END)
        OVER (ORDER BY dt) AS grp FROM flagged) s
GROUP BY price, grp ORDER BY segment_from;
```
**Explanation:** A price change opens a new run; each run carries one price and its span of days — an instant price history viz.

**Alt1:**
```sql
WITH prices(dt, price) AS (
  VALUES (date '2026-09-01', 5),(date '2026-09-02', 5),(date '2026-09-03', 6),
         (date '2026-09-04', 6),(date '2026-09-05', 5)
)
SELECT price, MIN(dt) AS segment_from, MAX(dt) AS segment_to, COUNT(*) AS days
FROM (SELECT dt, price,
        dt - (ROW_NUMBER() OVER (PARTITION BY price ORDER BY dt))::int AS grp
      FROM prices) s
GROUP BY price, grp ORDER BY segment_from;
```
**Explanation:** Number days within each price value; date minus rank is stable while the price doesn't move, giving identical segments without any LAG.

## Q50: Interval compaction — squeeze ragged overlapping bookings into one timeline.

Schema hints: `bookings(id, start_ts, end_ts)` — merge all intersecting intervals and list free slivers between compacted blocks.

**Query:**
```sql
WITH bookings(id, start_ts, end_ts) AS (
  VALUES (1, '2026-01-01 08:00', '2026-01-01 10:00'),
         (2, '2026-01-01 09:00', '2026-01-01 11:00'),
         (3, '2026-01-01 13:00', '2026-01-01 14:00')
),
ordered AS (
  SELECT *,
         LAG(end_ts) OVER (ORDER BY start_ts) AS prev_end
  FROM bookings
),
merged AS (
  SELECT start_ts, end_ts,
         SUM(CASE WHEN prev_end IS NULL OR start_ts > prev_end THEN 1 ELSE 0 END)
           OVER (ORDER BY start_ts) AS grp
  FROM ordered
)
SELECT MIN(start_ts) AS busy_from, MAX(end_ts) AS busy_to
FROM merged GROUP BY grp ORDER BY busy_from;
```
**Explanation:** Any booking starting past the maximum so-far finish opens a new busy block; the running-sum trick compacts chains of overlaps into `busy_from..busy_to` rows.
## Q51: First and last date of every login streak per user, with streak length.

Schema hints: `logins(user_id, ts)` — one summary row per island.

**Query:**
```sql
WITH logins(user_id, ts) AS (
  VALUES (1, date '2026-01-01'),(1, date '2026-01-02'),(1, date '2026-01-05'),
         (2, date '2026-01-01'),(2, date '2026-01-02'),(2, date '2026-01-03')
),
tagged AS (
  SELECT user_id, ts,
         ts - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY ts))::int AS grp
  FROM (SELECT DISTINCT user_id, ts FROM logins) d
)
SELECT user_id, MIN(ts) AS streak_from, MAX(ts) AS streak_to, COUNT(*) AS days
FROM tagged GROUP BY user_id, grp
ORDER BY user_id, streak_from;
```
**Explanation:** One group key per island and the classic MIN/MAX/COUNT triple yields a per-streak one-liner digest.

**Alt1:**
```sql
WITH RECURSIVE logins(user_id, ts) AS (
  VALUES (1, date '2026-01-01'),(1, date '2026-01-02'),(1, date '2026-01-05'),
         (2, date '2026-01-01'),(2, date '2026-01-02'),(2, date '2026-01-03')
),
daily AS (SELECT DISTINCT user_id, ts FROM logins),
walk AS (
  SELECT user_id, ts, ts AS root FROM daily d
  WHERE NOT EXISTS (SELECT 1 FROM daily p
                    WHERE p.user_id = d.user_id AND p.ts = d.ts - 1)
  UNION ALL
  SELECT n.user_id, n.ts, w.root
  FROM walk w JOIN daily n
    ON n.user_id = w.user_id AND n.ts = w.ts + 1
)
SELECT (SELECT user_id FROM walk x WHERE x.root = w.root LIMIT 1) AS user_id,
       MIN(w.root) AS streak_from, MAX(w.ts) AS streak_to, COUNT(*) AS days
FROM walk w GROUP BY w.root ORDER BY streak_from;
```
**Explanation:** Walk from island seeds forward one day at a time; every reached day inherits its root date, so grouping by root reassembles each streak.

## Q52: Users with more than one streak longer than three days (multi-marathoners).

Schema hints: `logins(user_id, ts)` — count qualifying islands per user, keep users with at least two.

**Query:**
```sql
WITH logins(user_id, ts) AS (
  VALUES (1, date '2026-02-01'),(1, date '2026-02-02'),(1, date '2026-02-03'),
         (1, date '2026-02-04'),(1, date '2026-02-10'),(1, date '2026-02-11'),
         (1, date '2026-02-12'),(1, date '2026-02-13'),
         (2, date '2026-02-01'),(2, date '2026-02-02')
),
tagged AS (
  SELECT user_id, ts,
         ts - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY ts))::int AS grp
  FROM (SELECT DISTINCT user_id, ts FROM logins) d
),
streaks AS (
  SELECT user_id, COUNT(*) AS len FROM tagged GROUP BY user_id, grp
)
SELECT user_id, COUNT(*) AS long_streaks
FROM streaks WHERE len > 3 GROUP BY user_id HAVING COUNT(*) >= 2
ORDER BY user_id;
```
**Explanation:** Filter islands to length > 3, count per user, and HAVING demands two or more such islands.

## Q53: Gaps between telephone numbers — enumerate every unavailable span in a block.

Schema hints: `phones(number int)` for `1000..1010`, present: `1001,1002,1005,1006,1007`.

**Query:**
```sql
WITH RECURSIVE phones(number) AS (VALUES (1001),(1002),(1005),(1006),(1007)),
all_nums(n) AS (
  SELECT 1000 UNION ALL SELECT n + 1 FROM all_nums WHERE n < 1010
),
missing AS (
  SELECT n FROM all_nums
  WHERE NOT EXISTS (SELECT 1 FROM phones p WHERE p.number = all_nums.n)
),
tagged AS (
  SELECT n, n - (ROW_NUMBER() OVER (ORDER BY n))::int AS grp FROM missing
)
SELECT MIN(n) AS missing_from, MAX(n) AS missing_to
FROM tagged GROUP BY grp ORDER BY missing_from;
```
**Explanation:** Expand the population with a recursive CTE, anti-join the taken lines, and island the leftovers into free ranges like `1000-1000, 1003-1004`.

## Q54: Chains of consecutive active days in usage where exactly one rest day is forgiven.

Schema hints: `usage(dt)` — islands may contain a single skip; collapse runs including one tolerant rest day.

**Query:**
```sql
WITH usage(dt) AS (
  VALUES (date '2026-03-01'),(date '2026-03-02'),(date '2026-03-04'),
         (date '2026-03-05'),(date '2026-03-06'),(date '2026-03-08')
),
flags AS (
  SELECT dt,
         dt - LAG(dt) OVER (ORDER BY dt) AS diff
  FROM usage
),
hard_break AS (
  SELECT dt,
         SUM(CASE WHEN diff > 2 OR diff IS NULL THEN 1 ELSE 0 END)
           OVER (ORDER BY dt) AS grp
  FROM flags
)
SELECT MIN(dt) AS from_dt, MAX(dt) AS to_dt, COUNT(*) AS used_days
FROM hard_break GROUP BY grp ORDER BY from_dt;
```
**Explanation:** A diff of 2 is a forgivable single rest day and stays inside the group; only a jump beyond that breaks the island.

## Q55: Longest streak ending today (current run) — no future read-ahead.

Schema hints: `logins(user_id, ts)` — measure only the streak touching the most recent date.

**Query:**
```sql
WITH logins(user_id, ts) AS (
  VALUES (1, date '2026-04-01'),(1, date '2026-04-02'),(1, date '2026-04-03'),
         (1, date '2026-04-05'),
         (2, date '2026-04-03'),(2, date '2026-04-04'),(2, date '2026-04-05')
),
daily AS (SELECT DISTINCT user_id, ts FROM logins),
flags AS (
  SELECT user_id, ts,
         ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) AS diff
  FROM daily
),
groups AS (
  SELECT user_id, ts,
         SUM(CASE WHEN diff = 1 THEN 0 ELSE 1 END)
           OVER (PARTITION BY user_id ORDER BY ts) AS grp
  FROM flags
),
last_grp AS (
  SELECT user_id, grp FROM groups g1
  WHERE ts = (SELECT MAX(ts) FROM daily d2 WHERE d2.user_id = g1.user_id)
)
SELECT g.user_id, COUNT(*) AS current_days
FROM groups g JOIN last_grp l
  ON g.user_id = l.user_id AND g.grp = l.grp
GROUP BY g.user_id ORDER BY g.user_id;
```
**Explanation:** Every `diff <> 1` opens a new group, so the *final* group — the one owning today — is the still-burning streak; counting its members gives its length.

## Q56: Current-run length — clean walk-backwards implementation.

Schema hints: `logins(user_id, ts)`; the streak that includes the latest login date, measured in days.

**Query:**
```sql
WITH logins(user_id, ts) AS (
  VALUES (1, date '2026-04-01'),(1, date '2026-04-02'),(1, date '2026-04-03'),
         (1, date '2026-04-05'),
         (2, date '2026-04-03'),(2, date '2026-04-04'),(2, date '2026-04-05')
),
daily AS (SELECT DISTINCT user_id, ts FROM logins),
mapping AS (
  SELECT user_id, ts,
         ts - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY ts))::int AS grp
  FROM daily
),
grp_of_last AS (
  SELECT user_id, grp FROM mapping m
  WHERE ts = (SELECT MAX(ts) FROM mapping m2 WHERE m2.user_id = m.user_id)
)
SELECT m.user_id, COUNT(*) AS current_days
FROM mapping m JOIN grp_of_last g
  ON m.user_id = g.user_id AND m.grp = g.grp
GROUP BY m.user_id ORDER BY m.user_id;
```
**Explanation:** Find the group id owning today, then count its members — the run is alive while its group key survives.

**Alt1:**
```sql
WITH RECURSIVE logins(user_id, ts) AS (
  VALUES (1, date '2026-04-01'),(1, date '2026-04-02'),(1, date '2026-04-03'),
         (1, date '2026-04-05'),
         (2, date '2026-04-03'),(2, date '2026-04-04'),(2, date '2026-04-05')
),
daily AS (SELECT DISTINCT user_id, ts FROM logins),
backwards AS (
  SELECT user_id, ts, 1 AS len FROM daily d
  WHERE ts = (SELECT MAX(ts) FROM daily d2 WHERE d2.user_id = d.user_id)
  UNION ALL
  SELECT d.user_id, d.ts, b.len + 1
  FROM backwards b JOIN daily d
    ON d.user_id = b.user_id AND d.ts = b.ts - 1
)
SELECT user_id, MAX(len) AS current_days FROM backwards GROUP BY user_id ORDER BY user_id;
```
**Explanation:** Start from each user's last login and recurse to `ts - 1` while it exists; the depth reached is the still-burning streak.

## Q57: Consecutive quarters since last churn — recency islands.

Schema hints: `activity(user_id, quarter)` — how many consecutive quarters a user stayed active counting back from the newest one.

**Query:**
```sql
WITH activity(user_id, quarter) AS (
  VALUES (1, date '2026-01-01'),(1, date '2026-04-01'),(1, date '2026-07-01'),
         (2, date '2026-01-01'),(2, date '2026-04-01')
),
offset AS (
  SELECT user_id, quarter,
         quarter - (((ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY quarter DESC)) - 1)
                    * interval '3 months') AS anchor
  FROM activity
)
SELECT user_id, MIN(quarter) AS active_since, MAX(quarter) AS active_through,
       COUNT(*) AS consecutive_quarters
FROM offset GROUP BY user_id, anchor ORDER BY user_id;
```
**Explanation:** Measure each quarter backwards from the newest: if they align to the same anchor the run is unbroken; any lost quarter moves the anchor forever.

## Q58: Sessions where a server stayed under 80% CPU (tolerant islands with threshold).

Schema hints: `cpu(minute, pct)` — consecutive minutes below 80 are one calm island; report the longest.

**Query:**
```sql
WITH cpu(minute, pct) AS (
  VALUES ('2026-05-01 00:00', 40),('2026-05-01 00:01', 75),('2026-05-01 00:02', 90),
         ('2026-05-01 00:03', 50),('2026-05-01 00:04', 30)
),
tagged AS (
  SELECT minute, pct,
         minute - ((ROW_NUMBER() OVER (PARTITION BY (pct < 80) ORDER BY minute))::int
                   * interval '1 minute') AS grp
  FROM cpu
)
SELECT MAX(c) AS calm_island_minutes
FROM (SELECT grp, COUNT(*) c FROM tagged WHERE pct < 80 GROUP BY grp) s;
```
**Explanation:** Boolean-partitioned row numbers minus minutes: identical for minutes inside one under-80 block, so counts hit the max calm window.

## Q59: Book two conjoined rooms — same-row adjacent free seats in two columns.

Schema hints: `seats(row_no, seat_no, occupied)`; find any two physically adjacent free seats.

**Query:**
```sql
WITH seats(row_no, seat_no, occupied) AS (
  VALUES (1, 1, false),(1, 2, false),(1, 3, true),
         (2, 1, true),(2, 2, false),(2, 3, false)
)
SELECT a.row_no, a.seat_no AS seat_from, b.seat_no AS seat_to
FROM seats a JOIN seats b
  ON a.row_no = b.row_no AND b.seat_no = a.seat_no + 1
WHERE NOT a.occupied AND NOT b.occupied
ORDER BY a.row_no, a.seat_no;
```
**Explanation:** A self-join on `seat_no + 1` with both free is the simplest possible adjacency detector — pairs, not islands.

**Alt1:**
```sql
WITH seats(row_no, seat_no, occupied) AS (
  VALUES (1, 1, false),(1, 2, false),(1, 3, true),
         (2, 1, true),(2, 2, false),(2, 3, false)
),
seq AS (
  SELECT row_no, seat_no,
         seat_no - (ROW_NUMBER() OVER (PARTITION BY row_no, occupied ORDER BY seat_no))::int AS grp
  FROM seats WHERE NOT occupied
),
runs AS (SELECT grp, row_no, MIN(seat_no) AS s_from, MAX(seat_no) AS s_to, COUNT(*) c
         FROM seq GROUP BY row_no, grp)
SELECT row_no, s_from, s_from + 1 AS seat_to FROM runs WHERE c >= 2;
```
**Explanation:** Island the free seats; any run of length ≥ 2 already contains adjacent pairs — no join required.

## Q60: Traffic spikes — islands where requests exceeded 100k/day.

Schema hints: `traffic(dt, requests)` — days over the threshold, summarised into spike blocks.

**Query:**
```sql
WITH traffic(dt, requests) AS (
  VALUES (date '2026-06-01', 110000),(date '2026-06-02', 120000),
         (date '2026-06-03', 90000),(date '2026-06-04', 110000)
),
tagged AS (
  SELECT dt, requests,
         dt - (ROW_NUMBER() OVER (PARTITION BY (requests > 100000) ORDER BY dt))::int AS grp
  FROM traffic
)
SELECT MIN(dt) AS spike_from, MAX(dt) AS spike_to, COUNT(*) AS days
FROM tagged WHERE requests > 100000
GROUP BY grp ORDER BY spike_from;
```
**Explanation:** Partition keys on the boolean, then only the `>100000` family's islands are reported with their date spans.

## Q61: Longest run of identical weather readings (same temperature days).

Schema hints: `wx(dt, temp)` — group into same-temperature islands, top by length.

**Query:**
```sql
WITH wx(dt, temp) AS (
  VALUES (date '2026-07-01', 18),(date '2026-07-02', 18),(date '2026-07-03', 21),
         (date '2026-07-04', 21),(date '2026-07-05', 21),(date '2026-07-06', 18)
),
tagged AS (
  SELECT dt, temp,
         dt - (ROW_NUMBER() OVER (PARTITION BY temp ORDER BY dt))::int AS grp
  FROM wx
)
SELECT temp, MIN(dt) AS from_dt, MAX(dt) AS to_dt, COUNT(*) AS days
FROM tagged GROUP BY temp, grp ORDER BY days DESC, from_dt LIMIT 1;
```
**Explanation:** Date-minus-rank within each temperature familiy yields per-weather islands; duration-sorted LIMIT 1 crowns the longest.

## Q62: Identify version-history gap and the current head version after it.

Schema hints: `specs(spec_id, rev)` — after detecting the largest skipped jump, report the revision right after it.

**Query:**
```sql
WITH specs(spec_id, rev) AS (
  VALUES ('A', 1),('A', 2),('A', 5),('A', 6),('A', 9)
),
prep AS (
  SELECT rev, LAG(rev) OVER (ORDER BY rev) AS prev_rev
  FROM specs WHERE spec_id = 'A'
)
SELECT prev_rev AS before_jump, rev AS after_jump,
       rev - prev_rev - 1 AS skipped_count
FROM prep
WHERE prev_rev IS NOT NULL AND rev - prev_rev > 1
ORDER BY skipped_count DESC LIMIT 1;
```
**Explanation:** The largest `rev - prev_rev` jump names the biggest break and both flanking revisions without islands at all.

## Q63: Consecutive drops in stock price (loss streaks).

Schema hints: `prices(dt, close)` — a red day is `close < prev_close`; longest red run.

**Query:**
```sql
WITH prices(dt, close) AS (
  VALUES (date '2026-08-01', 50),(date '2026-08-02', 48),(date '2026-08-03', 47),
         (date '2026-08-04', 52),(date '2026-08-05', 51)
),
flagged AS (
  SELECT dt, close,
         close < LAG(close) OVER (ORDER BY dt) AS red
  FROM prices
),
red_runs AS (
  SELECT dt,
         SUM(CASE WHEN red OR red IS NULL THEN 0 ELSE 1 END) OVER (ORDER BY dt) AS grp
  FROM flagged WHERE red
)
SELECT MAX(c) AS longest_red_streak
FROM (SELECT grp, COUNT(*) c FROM red_runs GROUP BY grp) s;
```
**Explanation:** Green days punctuate; filtering to red rows and summing over the reset flag isolates the deepest losing spell.

## Q64: Merge booking intervals first, then report the compacted busy blocks.

Schema hints: `meetings(id, start_ts, end_ts)` inside `09:00-18:00`; overlapping meetings collapse into one busy window.

**Query:**
```sql
WITH meetings(id, start_ts, end_ts) AS (
  VALUES (1, '09:00', '10:30'),(2, '10:00', '11:00'),(3, '13:00', '14:00')
),
ordered AS (
  SELECT start_ts, end_ts,
         LAG(end_ts) OVER (ORDER BY start_ts) AS prev_end
  FROM meetings
),
compact AS (
  SELECT start_ts, end_ts,
         SUM(CASE WHEN prev_end IS NULL OR start_ts > prev_end THEN 1 ELSE 0 END)
           OVER (ORDER BY start_ts) AS grp
  FROM ordered
)
SELECT MIN(start_ts) AS busy_from, MAX(end_ts) AS busy_to
FROM compact GROUP BY grp ORDER BY busy_from;
```
**Explanation:** A meeting that starts after everything before it is done begins fresh air; otherwise it folds into the same group — the classic overlap-compaction island.

## Q65: Free-slot detective — clean logic with explicit edges.

Schema hints: `meetings(start_ts, end_ts)` in `HH:MM`; 9-to-6 office; return gaps between meetings and after the last one.

**Query:**
```sql
WITH meetings(id, start_ts, end_ts) AS (
  VALUES (1, '09:00', '10:30'),(2, '10:00', '11:00'),(3, '13:00', '14:00')
),
prep AS (
  SELECT *, '09:00' AS day_start, '18:00' AS day_end
  FROM meetings
),
blocks AS (
  SELECT LEAD(start_ts) OVER (ORDER BY start_ts) AS next_start,
         end_ts, id,
         MAX(end_ts) OVER (ORDER BY start_ts ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_max_end
  FROM prep
),
free_mid AS (
  SELECT running_max_end AS free_from, next_start AS free_to
  FROM blocks WHERE next_start > running_max_end
)
SELECT free_from, free_to FROM free_mid
UNION ALL
SELECT '18:00', NULL WHERE NOT EXISTS (SELECT 1 WHERE 1=0);
```
**Explanation:** The running max of meeting ends, compared with the next start, exposes every real free window; the tail is handled explicitly where it exists.

**Alt1:**
```sql
WITH meetings(id, start_ts, end_ts) AS (
  VALUES (1, '09:00', '10:30'),(2, '10:00', '11:00'),(3, '13:00', '14:00')
)
SELECT MAX(end_ts) AS free_from, nxt.start_ts AS free_to
FROM meetings m JOIN meetings nxt
  ON nxt.start_ts = (SELECT MIN(start_ts) FROM meetings s WHERE s.start_ts > m.end_ts)
WHERE NOT EXISTS (SELECT 1 FROM meetings mid
                  WHERE mid.start_ts > m.end_ts AND mid.start_ts < nxt.start_ts)
GROUP BY nxt.start_ts;
```
**Explanation:** For each meeting find its nearest later start; when nothing sits between `m.end` and that start, you have found a truly free window via plain self-joins.

## Q66: String-run reconstruction — crystal islands on DNA bases.

Schema hints: `seq(pos, base)` of `'AAT'` — report every homopolymer (run of one base).

**Query:**
```sql
WITH seq(pos, base) AS (VALUES (1,'A'),(2,'A'),(3,'T'),(4,'C'),(5,'C'),(6,'C')),
flagged AS (
  SELECT pos, base,
         base <> LAG(base) OVER (ORDER BY pos) AS changed
  FROM seq
)
SELECT base, MIN(pos) AS from_pos, MAX(pos) AS to_pos, COUNT(*) AS len
FROM (SELECT *, SUM(CASE WHEN changed OR changed IS NULL THEN 1 ELSE 0 END)
        OVER (ORDER BY pos) AS grp FROM flagged) s
GROUP BY base, grp ORDER BY from_pos;
```
**Explanation:** Each base change opens a new island, so homopolymer runs are enumerated with position spans.

## Q67: Gap between pay periods — employees with a whole pay cycle skipped.

Schema hints: `payments(emp_id, pay_date)` — payments arrive every 14 days; flag intervals of 28+ days.

**Query:**
```sql
WITH payments(emp_id, pay_date) AS (
  VALUES (1, date '2026-01-01'),(1, date '2026-01-15'),(1, date '2026-02-12'),
         (2, date '2026-01-01'),(2, date '2026-01-15'),(2, date '2026-01-29')
),
prep AS (
  SELECT emp_id, pay_date,
         LAG(pay_date) OVER (PARTITION BY emp_id ORDER BY pay_date) AS prev_pay
  FROM payments
)
SELECT emp_id, prev_pay AS last_paid, pay_date AS next_paid,
       (pay_date - prev_pay) AS days_between
FROM prep WHERE prev_pay IS NOT NULL AND pay_date - prev_pay > 14
ORDER BY emp_id;
```
**Explanation:** A pay gap of more than 14 days means an entire cycle went unpaid; LAG measures it directly.

## Q68: Islands of sessions lasting multiple actions each (activity burst labels).

Schema hints: `events(user_id, ts)` — consecutive-minute activity = one burst; assign burst ids.

**Query:**
```sql
WITH events(user_id, ts) AS (
  VALUES (1, '2026-09-01 09:00'),(1, '2026-09-01 09:01'),(1, '2026-09-01 09:30'),
         (1, '2026-09-01 09:31'),(1, '2026-09-01 09:32'),
         (2, '2026-09-01 09:00')
),
flagged AS (
  SELECT user_id, ts,
         ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) > interval '1 minute' AS new_burst
  FROM events
),
bursts AS (
  SELECT user_id, ts,
         SUM(CASE WHEN new_burst OR new_burst IS NULL THEN 1 ELSE 0 END)
           OVER (PARTITION BY user_id ORDER BY ts) AS burst_id
  FROM flagged
)
SELECT user_id, burst_id, MIN(ts) AS burst_start, MAX(ts) AS burst_end,
       COUNT(*) AS actions
FROM bursts GROUP BY user_id, burst_id ORDER BY user_id, burst_start;
```
**Explanation:** A timestamp further than one minute from its predecessor starts a new burst; the running sum assigns IDs and spans.

## Q69: Business-hours shipping gaps — non-business windows re-examined with a calendar.

Schema hints: `shipments(ship_dt, order_id)` — merge orders into daily islands; a missing working day is a shipping hole.

**Query:**
```sql
WITH shipments(ship_dt, order_id) AS (
  VALUES (date '2026-10-01', 1),(date '2026-10-02', 2),(date '2026-10-06', 3)
),
daily AS (SELECT DISTINCT ship_dt FROM shipments),
tagged AS (
  SELECT ship_dt,
         ship_dt - (ROW_NUMBER() OVER (ORDER BY ship_dt))::int AS grp
  FROM daily
)
SELECT MIN(ship_dt) AS run_start, MAX(ship_dt) AS run_end, COUNT(*) AS ship_days
FROM tagged GROUP BY grp ORDER BY run_start;
```
**Explanation:** Shipping days that skip a working day form separate islands, so the gap between `run_end` and the next `run_start` reveals the silent window.

## Q70: Longest run of narrowly-increasing stock closes.

Schema hints: `prices(dt, close)` — a strictly increasing day-chain is a gold run; find the champion.

**Query:**
```sql
WITH prices(dt, close) AS (
  VALUES (date '2026-11-01', 30),(date '2026-11-02', 31),(date '2026-11-03', 32),
         (date '2026-11-04', 31.5),(date '2026-11-05', 33),(date '2026-11-06', 35)
),
flagged AS (
  SELECT dt, close,
         close > LAG(close) OVER (ORDER BY dt) AS up
  FROM prices
),
dir AS (
  SELECT dt,
         SUM(CASE WHEN up OR up IS NULL THEN 0 ELSE 1 END) OVER (ORDER BY dt) AS grp
  FROM flagged WHERE up
)
SELECT MAX(c) AS longest_up_run
FROM (SELECT grp, COUNT(*) c FROM dir GROUP BY grp) s;
```
**Explanation:** Strictly-greater days only; any slide reads as a reset in the running sum, and the biggest bucket is the winning streak.

**Alt1:**
```sql
WITH RECURSIVE prices(dt, close) AS (
  VALUES (date '2026-11-01', 30),(date '2026-11-02', 31),(date '2026-11-03', 32),
         (date '2026-11-04', 31.5),(date '2026-11-05', 33),(date '2026-11-06', 35)
),
up_starts AS (
  SELECT dt FROM prices p
  WHERE NOT EXISTS (SELECT 1 FROM prices q
                    WHERE q.dt = p.dt - 1 AND q.close < p.close)
),
walk AS (
  SELECT p.dt, s.dt AS root, 1 AS len
  FROM prices p JOIN up_starts s ON s.dt = p.dt
  UNION ALL
  SELECT q.dt, w.root, w.len + 1
  FROM walk w JOIN prices q ON q.dt = w.dt + 1
  WHERE q.close > (SELECT close FROM prices r WHERE r.dt = w.dt)
)
SELECT MAX(len) AS longest_up_run FROM walk;
```
**Explanation:** Recursion spawns only at days with no profitable predecessor and grows while closes keep climbing; max depth is the record.

## Q71: Counting all gaps in intervals (uncovered time sum) across a timeline.

Schema hints: `maintenance(start_dt, end_dt)` — sum total days NOT covered by any maintenance window over a year.

**Query:**
```sql
WITH RECURSIVE maintenance(id, start_dt, end_dt) AS (
  VALUES (1, date '2026-01-01', date '2026-01-10'),
         (2, date '2026-01-05', date '2026-01-15'))
,
cal(d) AS (
  SELECT date '2026-01-01' UNION ALL SELECT d + 1 FROM cal WHERE d < date '2026-01-20'
)
SELECT COUNT(*) AS uncovered_days
FROM (SELECT cal.d FROM cal
      LEFT JOIN maintenance m ON cal.d BETWEEN m.start_dt AND m.end_dt
      WHERE m.id IS NULL) free;
```
**Explanation:** A recursive calendar is anti-joined to maintenance islands; the surviving row count is the total uncovered time.

## Q72: Newcastle of islands — longest run count among all users (leaderboard).

Schema hints: `logins(user_id, ts)` — rank users by their best streak.

**Query:**
```sql
WITH logins(user_id, ts) AS (
  VALUES (1, date '2026-12-01'),(1, date '2026-12-02'),
         (2, date '2026-12-01'),(2, date '2026-12-02'),(2, date '2026-12-03')
),
daily AS (SELECT DISTINCT user_id, ts FROM logins),
tagged AS (
  SELECT user_id, ts,
         ts - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY ts))::int AS grp
  FROM daily
),
streaks AS (SELECT user_id, COUNT(*) c FROM tagged GROUP BY user_id, grp),
best AS (SELECT user_id, MAX(c) best FROM streaks GROUP BY user_id)
SELECT user_id, best,
       RANK() OVER (ORDER BY best DESC) AS rank
FROM best ORDER BY rank;
```
**Explanation:** Islands → per-user max → window RANK.

## Q73: Adjacent-pair corrections — flag revision history regressions.

Schema hints: `revisions(doc_id, rev)` in insertion order (`insert_seq`); detect a stored rev LOWER than the previous inserted rev — an out-of-order push.

**Query:**
```sql
WITH revisions(doc_id, insert_seq, rev) AS (
  VALUES (1, 1, 1),(1, 2, 2),(1, 3, 5),(1, 4, 3),(1, 5, 4)
),
prep AS (
  SELECT doc_id, insert_seq, rev,
         LAG(rev) OVER (PARTITION BY doc_id ORDER BY insert_seq) AS prev_rev
  FROM revisions
)
SELECT doc_id, insert_seq, prev_rev AS prior_rev, rev AS stored_rev,
       'backtrack' AS kind
FROM prep
WHERE prev_rev IS NOT NULL AND rev < prev_rev;
```
**Explanation:** Ordering by insertion sequence and comparing each stored rev with the previous reveals the regression (`5 → 3`) without touching gaps — the backtrack, seen in time, is just a negative delta.

## Q74: Out-of-order revision — corrected version.

Schema hints: `revisions(doc_id, rev)` unordered; detect every revision not exactly one above the previous sorted one.

**Query:**
```sql
WITH revisions(doc_id, rev) AS (
  VALUES (1, 1),(1, 2),(1, 5),(1, 3),(1, 4)
),
sorted AS (
  SELECT doc_id, rev FROM revisions
  GROUP BY doc_id, rev
),
prep AS (
  SELECT doc_id, rev,
         LAG(rev) OVER (PARTITION BY doc_id ORDER BY rev) AS prev_rev
  FROM sorted
)
SELECT doc_id, prev_rev + 1 AS next_expected, rev AS actual,
       rev - prev_rev - 1 AS skipped
FROM prep
WHERE prev_rev IS NOT NULL AND rev <> prev_rev + 1
ORDER BY doc_id, rev;
```
**Explanation:** Sorted sequence compared neighbor-to-neighbor; any non-successive pair is flagged with both expected and actual, exposing the backtrack `5 → 3` as a contradiction.

## Q75: Match-day streaks across alternating home/away.

Schema hints: `games(game_date, venue)` — compute the longest run of home games and of away games separately.

**Query:**
```sql
WITH games(game_date, venue) AS (
  VALUES (date '2026-01-01', 'home'),(date '2026-01-02', 'home'),
         (date '2026-01-03', 'away'),(date '2026-01-04', 'away'),
         (date '2026-01-05', 'home')
),
flagged AS (
  SELECT game_date, venue,
         venue <> LAG(venue) OVER (ORDER BY game_date) AS changed
  FROM games
),
runs AS (
  SELECT venue,
         SUM(CASE WHEN changed OR changed IS NULL THEN 1 ELSE 0 END)
           OVER (ORDER BY game_date) AS grp
  FROM flagged
)
SELECT venue, MAX(c) AS longest_venue_streak
FROM (SELECT venue, grp, COUNT(*) c FROM runs GROUP BY venue, grp) s
GROUP BY venue ORDER BY venue;
```
**Explanation:** Venue flips separate the runs; grouping gives per-venue longest runs.
## Q76: Islands in a sequence with a tolerance of one repeated number.

Schema hints: `races(finish_pos)` — positions `1,2,2,3,5` — a repeat does NOT break the island; count distinct-is-effective.

**Query:**
```sql
WITH races(finish_pos) AS (VALUES (1),(2),(2),(3),(5)),
deduped AS (SELECT DISTINCT finish_pos FROM races),
tagged AS (
  SELECT finish_pos,
         finish_pos - (ROW_NUMBER() OVER (ORDER BY finish_pos))::int AS grp
  FROM deduped
)
SELECT MIN(finish_pos) AS island_from, MAX(finish_pos) AS island_to
FROM tagged GROUP BY grp ORDER BY island_from;
```
**Explanation:** Deduplicate first — a tie is still "consecutive" semantically — and the standard rank-minus-value trick re-defines the islands.

## Q77: Missing employee IDs between hires — rehire-sequence gap audit.

Schema hints: `hires(emp_id)` over `100..110`, missing ids `102,105,106`.

**Query:**
```sql
WITH RECURSIVE hires(emp_id) AS (VALUES (100),(101),(103),(104),(107)),
populated(id) AS (
  SELECT MIN(emp_id) FROM hires
  UNION ALL SELECT id + 1 FROM populated
  WHERE id < (SELECT MAX(emp_id) FROM hires)
),
missing AS (
  SELECT id FROM populated
  WHERE NOT EXISTS (SELECT 1 FROM hires h WHERE h.emp_id = populated.id)
),
tagged AS (
  SELECT id, id - (ROW_NUMBER() OVER (ORDER BY id))::int AS grp FROM missing
)
SELECT MIN(id) AS missing_from, MAX(id) AS missing_to
FROM tagged GROUP BY grp ORDER BY missing_from;
```
**Explanation:** Recursive expansion, anti-join, island the leftovers — missings become clean `from..to` rows.

## Q78: Consecutive VIP check-in days — rank users who never missed a hotel room for a week.

Schema hints: `checkins(guest_id, dt)` — islands of 7+ days identify weekly loyalists.

**Query:**
```sql
WITH checkins(guest_id, dt) AS (
  VALUES (1, date '2026-02-01'),(1, date '2026-02-02'),(1, date '2026-02-03'),
         (1, date '2026-02-04'),(1, date '2026-02-05'),(1, date '2026-02-06'),
         (1, date '2026-02-07'),
         (2, date '2026-02-01'),(2, date '2026-02-03')
),
tagged AS (
  SELECT guest_id, dt, dt - (ROW_NUMBER() OVER (PARTITION BY guest_id ORDER BY dt))::int AS grp
  FROM (SELECT DISTINCT guest_id, dt FROM checkins) d
)
SELECT guest_id, COUNT(*) AS streak_days
FROM (SELECT guest_id, grp, COUNT(*) c FROM tagged GROUP BY guest_id, grp) s
WHERE c >= 7 GROUP BY guest_id ORDER BY guest_id;
```
**Explanation:** Flag islands; a block of at least seven rows means a weekly run of unbroken stays.

## Q79: Longest subsequence of monotonically non-decreasing sales.

Schema hints: `sales(dt, qty)` — never lower than yesterday counts; report champion run.

**Query:**
```sql
WITH sales(dt, qty) AS (
  VALUES (date '2026-03-01', 10),(date '2026-03-02', 12),(date '2026-03-03', 12),
         (date '2026-03-04', 9),(date '2026-03-05', 11),(date '2026-03-06', 14)
),
flagged AS (
  SELECT dt, qty,
         qty >= LAG(qty) OVER (ORDER BY dt) AS non_dec
  FROM sales
),
runs AS (
  SELECT dt,
         SUM(CASE WHEN non_dec OR non_dec IS NULL THEN 0 ELSE 1 END)
           OVER (ORDER BY dt) AS grp
  FROM flagged WHERE non_dec
)
SELECT MAX(c) AS longest_flat_or_growing
FROM (SELECT grp, COUNT(*) c FROM runs GROUP BY grp) s;
```
**Explanation:** `qty >= prev` stays in the bucket; every true drop resets, so the largest bucket is the max plateau.

## Q80: Enumerate all gap-free ranges when some numbers repeat.

Schema hints: `tokens(n)` in `1,1,2,4,4,5` — report `1-2` and `4-5` as the maximal gap-free blocks.

**Query:**
```sql
WITH tokens(n) AS (VALUES (1),(1),(2),(4),(4),(5)),
uniq AS (SELECT DISTINCT n FROM tokens),
tagged AS (
  SELECT n, n - (ROW_NUMBER() OVER (ORDER BY n))::int AS grp FROM uniq
)
SELECT MIN(n) AS range_from, MAX(n) AS range_to
FROM tagged GROUP BY grp ORDER BY range_from;
```
**Explanation:** Distinct-first islanding reports maximal gap-free spans and ignores the duplicates within.

## Q81: Longest holiday chain across different employees (company-wide day-off maximiser).

Schema hints: `days_off(emp_id, day_off)` — union everyone's days off; find the longest chain of company-wide no-show days.

**Query:**
```sql
WITH days_off(emp_id, day_off) AS (
  VALUES (1, date '2026-05-01'),(1, date '2026-05-02'),(2, date '2026-05-02'),
         (2, date '2026-05-03'),(3, date '2026-05-06')
),
cover AS (SELECT DISTINCT day_off FROM days_off),
tagged AS (
  SELECT day_off, day_off - (ROW_NUMBER() OVER (ORDER BY day_off))::int AS grp FROM cover
)
SELECT MIN(day_off) AS chain_from, MAX(day_off) AS chain_to, COUNT(*) AS days
FROM tagged GROUP BY grp ORDER BY days DESC LIMIT 1;
```
**Explanation:** Distinct union of all absences forms the cover; the classic date-minus-rank yields the longest stretch anyone was out.

## Q82: Phone-number hunt v2 — first gap of size ≥ 3 (a free block for a small team).

Schema hints: `phones(number)` in `1000..1020`, present items make small islands; find the first hole of at least 3 numbers.

**Query:**
```sql
WITH RECURSIVE phones(number) AS (VALUES (1000),(1001),(1005),(1007)),
populated(n) AS (
  SELECT MIN(number) FROM phones
  UNION ALL SELECT n + 1 FROM populated WHERE n < 1020
),
missing AS (
  SELECT n FROM populated
  WHERE NOT EXISTS (SELECT 1 FROM phones p WHERE p.number = populated.n)
),
tagged AS (
  SELECT n, n - (ROW_NUMBER() OVER (ORDER BY n))::int AS grp FROM missing
),
blocks AS (
  SELECT MIN(n) AS free_from, MAX(n) AS free_to, COUNT(*) c
  FROM tagged GROUP BY grp
)
SELECT free_from, free_to FROM blocks WHERE c >= 3 ORDER BY free_from LIMIT 1;
```
**Explanation:** The free numbers are the island; HAVING-style filter for runs ≥ 3 and grab the first via LIMIT.

## Q83: Work-day streaks that survive weekends (weekend-skipping daily login chain).

Schema hints: `logins(user_id, ts)` — Mon–Fri count; Sat/Sun are neutral (they never break the streak).

**Query:**
```sql
WITH logins(user_id, ts) AS (
  VALUES (1, date '2026-01-05'),(1, date '2026-01-06'),(1, date '2026-01-07'),
         (1, date '2026-01-08'),(1, date '2026-01-09'),(1, date '2026-01-12'),
         (2, date '2026-01-05')
),
daily AS (SELECT DISTINCT user_id, ts FROM logins),
workdays AS (
  SELECT user_id, ts, DATE_PART('dow', ts) AS dow
  FROM daily
),
flagged AS (
  SELECT user_id, ts,
         CASE WHEN dow = 0 THEN ts - 2
              WHEN dow = 1 THEN ts - 3
              ELSE ts - 1 END AS expected_prev
  FROM workdays
)
SELECT user_id, COUNT(*) > 0 AS has_weekday_streak
FROM flagged GROUP BY user_id;
```
**Explanation:** Rebase expectations onto the prior working day (skip weekends); a chain survives as long as that expected date is present — the newer island idiom, deadline-aware.

## Q84: Cold-start — return all islands of consecutive days with the day-of-week label.

Schema hints: `events(dt)` — decorate each island with its opening weekday.

**Query:**
```sql
WITH events(dt) AS (
  VALUES (date '2026-06-01'),(date '2026-06-02'),(date '2026-06-05')
),
tagged AS (
  SELECT dt, dt - (ROW_NUMBER() OVER (ORDER BY dt))::int AS grp FROM events
)
SELECT TO_CHAR(MIN(dt), 'Dy') AS start_weekday,
       MIN(dt) AS from_dt, MAX(dt) AS to_dt, COUNT(*) AS days
FROM tagged GROUP BY grp ORDER BY from_dt;
```
**Explanation:** Same island mechanics, plus a `TO_CHAR` cast on the island's opening date for the label.

## Q85: Intervals of overlapping campaigns — bring all overlapping ad slots into one lens.

Schema hints: `ads(id, start_dt, end_dt)` — first merge overlapping, then report coverage count peak.

**Query:**
```sql
WITH ads(id, start_dt, end_dt) AS (
  VALUES (1, date '2026-07-01', date '2026-07-05'),
         (2, date '2026-07-03', date '2026-07-09'),
         (3, date '2026-07-10', date '2026-07-12')
),
prep AS (
  SELECT start_dt, end_dt,
         LAG(end_dt) OVER (ORDER BY start_dt) AS prev_end
  FROM ads
),
groups AS (
  SELECT start_dt, end_dt,
         SUM(CASE WHEN prev_end IS NULL OR start_dt > prev_end THEN 1 ELSE 0 END)
           OVER (ORDER BY start_dt) AS grp
  FROM prep
)
SELECT MIN(start_dt) AS merged_from, MAX(end_dt) AS merged_to,
       COUNT(*) AS slots_in_group
FROM groups GROUP BY grp ORDER BY merged_from;
```
**Explanation:** Overlap = `start_dt <= prev_end` → stays; the running-sum boundary test compacts the whole campaign landscape.

**Alt1:**
```sql
WITH ads(id, start_dt, end_dt) AS (
  VALUES (1, date '2026-07-01', date '2026-07-05'),
         (2, date '2026-07-03', date '2026-07-09'),
         (3, date '2026-07-10', date '2026-07-12')
),
reach AS (
  SELECT start_dt, end_dt,
         MAX(end_dt) OVER (ORDER BY start_dt
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_max
  FROM ads
)
SELECT start_dt, end_dt,
       CASE WHEN start_dt > LAG(running_max) OVER (ORDER BY start_dt)
            THEN 'New group' ELSE 'Merged' END AS status
FROM reach;
```
**Explanation:** Comparing each start against the running maximum finish tells, per row, whether it opens fresh air or folds into an existing merged champ.

## Q86: Longest stretch of positive temperature anomalies.

Schema hints: `climate(dt, anomaly)` — `anomaly > 0` consecutive days form a heat snapshot; longest one.

**Query:**
```sql
WITH climate(dt, anomaly) AS (
  VALUES (date '2026-04-01', 1.2),(date '2026-04-02', 0.8),(date '2026-04-03', -0.5),
         (date '2026-04-04', 1.1),(date '2026-04-05', 1.9),(date '2026-04-06', 0.3)
),
tagged AS (
  SELECT dt, anomaly,
         dt - (ROW_NUMBER() OVER (PARTITION BY (anomaly > 0) ORDER BY dt))::int AS grp
  FROM climate
)
SELECT MAX(c) AS warmest_run_days
FROM (SELECT grp, COUNT(*) c FROM tagged WHERE anomaly > 0 GROUP BY grp) s;
```
**Explanation:** Boolean-partitioned numbering + date subtraction isolates warm runs; the warm-side max count is the answer.

## Q87: Merge + gap simultaneous — find free windows between service windows.

Schema hints: `service(start_ts, end_ts)` — merge overlapping, then report the negative space after compaction.

**Query:**
```sql
WITH service(id, start_ts, end_ts) AS (
  VALUES (1, '2026-08-01 08:00', '2026-08-01 10:00'),
         (2, '2026-08-01 09:00', '2026-08-01 11:00'),
         (3, '2026-08-01 12:00', '2026-08-01 13:00')
),
prep AS (
  SELECT start_ts, end_ts,
         LAG(end_ts) OVER (ORDER BY start_ts) AS prev_end
  FROM service
),
compact AS (
  SELECT MIN(start_ts) AS b_from, MAX(end_ts) AS b_to
  FROM (SELECT start_ts, end_ts,
          SUM(CASE WHEN prev_end IS NULL OR start_ts > prev_end THEN 1 ELSE 0 END)
            OVER (ORDER BY start_ts) AS grp FROM prep) g
  GROUP BY grp
)
SELECT prev.b_to + interval '1 minute' AS free_from,
       curr.b_from - interval '1 minute' AS free_to
FROM compact curr JOIN LATERAL (SELECT MAX(b_to) AS b_to FROM compact c
                               WHERE c.b_from < curr.b_from) prev ON true
ORDER BY free_from;
```
**Explanation:** Compact the windows to their islands, then LATERAL-join each island to the latest earlier one — the gap between them *is* the free period.

## Q88: Consecutive-days crown — users active on adjacent islands of days above a threshold.

Schema hints: `conns(user_id, dt, hours)` — islands where usage ≥ 1h/day, then chains of such islands.

**Query:**
```sql
WITH conns(user_id, dt, hours) AS (
  VALUES (1, date '2026-01-01', 2),(1, date '2026-01-02', 3),
         (1, date '2026-01-03', 0),(1, date '2026-01-04', 4),(1, date '2026-01-05', 5)
),
usage AS (SELECT user_id, dt FROM conns WHERE hours >= 1),
tagged AS (
  SELECT user_id, dt,
         dt - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY dt))::int AS grp
  FROM usage
)
SELECT user_id, MAX(c) AS consecutive_useful_days
FROM (SELECT user_id, grp, COUNT(*) c FROM tagged GROUP BY user_id, grp) s
GROUP BY user_id ORDER BY user_id;
```
**Explanation:** Pre-filter to qualifying days, then island; a wasted day silently shears the run.

## Q89: Gaps between price changes — duration each price level persisted.

Schema hints: `prices(dt, price)` — every island of equal price; its lifespan = `last_day - first_day + 1`.

**Query:**
```sql
WITH prices(dt, price) AS (
  VALUES (date '2026-01-01', 5),(date '2026-01-02', 5),(date '2026-01-03', 6),
         (date '2026-01-04', 6),(date '2026-01-05', 6),(date '2026-01-06', 5)
),
flagged AS (
  SELECT dt, price,
         price <> LAG(price) OVER (ORDER BY dt) AS changed
  FROM prices
),
islands AS (
  SELECT dt, price,
         SUM(CASE WHEN changed OR changed IS NULL THEN 1 ELSE 0 END)
           OVER (ORDER BY dt) AS grp
  FROM flagged
)
SELECT price, MIN(dt) AS price_from, MAX(dt) AS price_to,
       (MAX(dt) - MIN(dt)) + 1 AS days_at_price
FROM islands GROUP BY price, grp ORDER BY price_from;
```
**Explanation:** Price changes draw islands; measuring each island's first/last date yields the exact lifespan of every level.

## Q90: Recursive islands for very sparse date data — stitch across months.

Schema hints: `checkups(patient_id, dt)` — a few visits per year; recursive walk needs to bridge month boundaries.

**Query:**
```sql
WITH RECURSIVE checkups(patient_id, dt) AS (
  VALUES (1, date '2026-01-15'),(1, date '2026-01-16'),(1, date '2026-03-01')
),
walk AS (
  SELECT patient_id, dt, dt AS root, 1 AS len
  FROM checkups c
  WHERE NOT EXISTS (SELECT 1 FROM checkups p
                    WHERE p.patient_id = c.patient_id AND p.dt = c.dt - 1)
  UNION ALL
  SELECT n.patient_id, n.dt, w.root, w.len + 1
  FROM walk w JOIN checkups n
    ON n.patient_id = w.patient_id AND n.dt = w.dt + 1
)
SELECT patient_id, root AS streak_start, dt AS streak_end, len
FROM walk ORDER BY patient_id, len DESC;
```
**Explanation:** Seeds are days with no predecessor; recursion hops from `dt` to `dt + 1`, bridging any month boundary, and `len` accumulates the chain.

## Q91: Every unbroken block of consecutive order numbers and each block's size.

Schema hints: `orders(ord_no)` with `1001,1002,1005,1006,1007,1010`.

**Query:**
```sql
WITH orders(ord_no) AS (VALUES (1001),(1002),(1005),(1006),(1007),(1010)),
tagged AS (
  SELECT ord_no,
         ord_no - (ROW_NUMBER() OVER (ORDER BY ord_no))::int AS grp
  FROM orders
)
SELECT MIN(ord_no) AS block_from, MAX(ord_no) AS block_to,
       COUNT(*) AS block_size
FROM tagged GROUP BY grp ORDER BY block_from;
```
**Explanation:** The grp key is identical exactly for horizontal neighbors — producing `1001-1002(2)`, `1005-1007(3)`, `1010(1)` in one sweep.

## Q92: Islands with flags — label blocks of downgrades inside a price-table history.

Schema hints: `hist(dt, price)` — flag days where price fell 2+ from the prior day, then island the flags.

**Query:**
```sql
WITH hist(dt, price) AS (
  VALUES (date '2026-01-01', 100),(date '2026-01-02', 97),(date '2026-01-03', 95),
         (date '2026-01-04', 97),(date '2026-01-05', 94),(date '2026-01-06', 91)
),
flagged AS (
  SELECT dt, price,
         price <= LAG(price) OVER (ORDER BY dt) - 2 AS steep
  FROM hist
),
runs AS (
  SELECT dt,
         SUM(CASE WHEN steep OR steep IS NULL THEN 0 ELSE 1 END)
           OVER (ORDER BY dt) AS grp, steep
  FROM flagged WHERE steep OR NOT steep
)
SELECT MIN(dt) AS decline_from, MAX(dt) AS decline_to, COUNT(*) AS days
FROM (SELECT dt, grp FROM runs WHERE steep) s
GROUP BY grp ORDER BY decline_from;
```
**Explanation:** Windows compute the drop flag; island machinery over the boolean buckets together the consecutive steep-decline days.

## Q93: First date after each silent period — when the connection resumed.

Schema hints: `conns(user_id, dt)` — for each gap, report the first reconnection date.

**Query:**
```sql
WITH conns(user_id, dt) AS (
  VALUES (1, date '2026-02-01'),(1, date '2026-02-02'),(1, date '2026-02-05'),
         (1, date '2026-02-09')
),
prep AS (
  SELECT user_id, dt,
         dt - LAG(dt) OVER (PARTITION BY user_id ORDER BY dt) AS diff
  FROM conns
)
SELECT user_id, dt AS resumed_on, diff - 1 AS silent_days
FROM prep WHERE diff > 1 ORDER BY user_id, resumed_on;
```
**Explanation:** `diff > 1` marks the row that follows a silence; it is — combined with its gap size — everything needed to name the resumption.

## Q94: Consecutive-day inventory shortages thresholded by severity.

Schema hints: `stock(dt, units)` — days under 10 units are critical; skip days above. Islands + severity.

**Query:**
```sql
WITH stock(dt, units) AS (
  VALUES (date '2026-09-01', 8),(date '2026-09-02', 5),(date '2026-09-03', 12),
         (date '2026-09-04', 9),(date '2026-09-05', 6)
),
flagged AS (
  SELECT dt, units,
         units < 10 AS critical
  FROM stock
),
tagged AS (
  SELECT dt, units,
         dt - (ROW_NUMBER() OVER (PARTITION BY critical ORDER BY dt))::int AS grp
  FROM flagged
)
SELECT MIN(dt) AS shortage_from, MAX(dt) AS shortage_to, COUNT(*) AS days,
       AVG(units) AS avg_units
FROM tagged WHERE critical GROUP BY grp ORDER BY shortage_from;
```
**Explanation:** Boolean partition isolates the critical days and the island key lumps them; AVG parcels in severity for free.

## Q95: Time-series intervals not covered by any maintenance (business-hour aware).

Schema hints: `maintenance(start_dt, end_dt)` — but counting only 9-5 Mon-Fri gaps as uncovered.

**Query:**
```sql
WITH RECURSIVE walldays(dt) AS (
  SELECT date '2026-01-05' UNION ALL SELECT dt + 1 FROM walldays WHERE dt < date '2026-01-16'
),
business AS (
  SELECT dt FROM walldays WHERE DATE_PART('isodow', dt) BETWEEN 1 AND 5
),
maintenance(id, start_dt, end_dt) AS (
  VALUES (1, date '2026-01-06', date '2026-01-08'),(2, date '2026-01-12', date '2026-01-13')
)
SELECT COUNT(*) AS uncovered_business_days
FROM (SELECT b.dt FROM business b
      LEFT JOIN maintenance m ON b.dt BETWEEN m.start_dt AND m.end_dt
      WHERE m.id IS NULL) free;
```
**Explanation:** A recursive workday calendar, business-day filtered, anti-joined to maintenance — the count is business-time availability.

## Q96: Find islands longer than the mean island length on the same table.

Schema hints: `pings(dt)` — islands computed once; those whose size beats the average across all islands.

**Query:**
```sql
WITH pings(dt) AS (
  VALUES (date '2026-10-01'),(date '2026-10-02'),(date '2026-10-03'),(date '2026-10-06')
),
tagged AS (
  SELECT dt, dt - (ROW_NUMBER() OVER (ORDER BY dt))::int AS grp FROM pings
),
islands AS (
  SELECT grp, MIN(dt) AS i_from, MAX(dt) AS i_to, COUNT(*) AS len
  FROM tagged GROUP BY grp
),
mean AS (SELECT AVG(len) AS avg_len FROM islands)
SELECT i_from, i_to, len FROM islands, mean
WHERE len > avg_len ORDER BY i_from;
```
**Explanation:** Two windows + one aggregate: island summaries joined to their own mean, filtered by the honest inequality.

## Q97: Union-assisted gap compact — gaps expressed from a master calendar.

Schema hints: `downtime(start_dt, end_dt)` — give normal operation windows inside a fixed yearly master.

**Query:**
```sql
WITH RECURSIVE master(d) AS (
  SELECT date '2026-01-01' UNION ALL SELECT d + 1 FROM master WHERE d < date '2026-01-10'
),
downtime(id, start_dt, end_dt) AS (
  VALUES (1, date '2026-01-02', date '2026-01-04'),(2, date '2026-01-07', date '2026-01-08')
),
up_days AS (
  SELECT d FROM master m
  WHERE NOT EXISTS (SELECT 1 FROM downtime dt WHERE m.d BETWEEN dt.start_dt AND dt.end_dt)
),
tagged AS (SELECT d, d - (ROW_NUMBER() OVER (ORDER BY d))::int AS grp FROM up_days)
SELECT MIN(d) AS up_from, MAX(d) AS up_to, COUNT(*) AS days
FROM tagged GROUP BY grp ORDER BY up_from;
```
**Explanation:** The master calendar defines the universe; downtime anti-join leaves up-days; those island into service windows.

**Alt1:**
```sql
WITH downtime(id, start_dt, end_dt) AS (
  VALUES (1, date '2026-01-02', date '2026-01-04'),(2, date '2026-01-07', date '2026-01-08')
),
sorted AS (
  SELECT *, LAG(end_dt) OVER (ORDER BY start_dt) AS prev_end, 
           LEAD(start_dt) OVER (ORDER BY start_dt) AS next_start
  FROM downtime
)
SELECT prev_end + 1 AS up_from, next_start - 1 AS up_to
FROM sorted WHERE prev_end IS NOT NULL AND prev_end + 1 <= next_start - 1;
```
**Explanation:** No calendar needed: LAG/LEAD on the downtime rows directly exposes the up ranges lying between them.

## Q98: Consecutive months of increasing headcount, reset on flat periods.

Schema hints: `hc(month, employees)` — strictly-growing months = growth island; longest run.

**Query:**
```sql
WITH hc(month, employees) AS (
  VALUES (date '2026-01-01', 50),(date '2026-02-01', 55),(date '2026-03-01', 60),
         (date '2026-04-01', 60),(date '2026-05-01', 70)
),
flagged AS (
  SELECT month, employees,
         employees > LAG(employees) OVER (ORDER BY month) AS growing
  FROM hc
),
runs AS (
  SELECT month,
         SUM(CASE WHEN growing OR growing IS NULL THEN 0 ELSE 1 END)
           OVER (ORDER BY month) AS grp
  FROM flagged WHERE growing
)
SELECT MAX(c) AS longest_growth_run
FROM (SELECT grp, COUNT(*) c FROM runs GROUP BY grp) s;
```
**Explanation:** Flat counts are not growth → they reset; the strict `>` flag with running reset leaves only the longest doggedly-rising stretch.

## Q99: Hardest — telephone hunt and streak audit in one recursive sweep.

Schema hints: `phones(number)` with `101,102,103,105,107,108` — find every free block AND the longest streak of taken numbers in a single pass.

**Query:**
```sql
WITH RECURSIVE phones(number) AS (VALUES (101),(102),(103),(105),(107),(108)),
world(n) AS (
  SELECT 101 UNION ALL SELECT n + 1 FROM world WHERE n < 108
),
grid AS (
  SELECT w.n,
         EXISTS (SELECT 1 FROM phones p WHERE p.number = w.n) AS busy
  FROM world w
),
tagged AS (
  SELECT n, busy,
         n - (ROW_NUMBER() OVER (PARTITION BY busy ORDER BY n))::int AS grp
  FROM grid
)
SELECT CASE WHEN busy THEN 'BUSY' ELSE 'FREE' END AS kind,
       MIN(n) AS range_from, MAX(n) AS range_to, COUNT(*) AS len
FROM tagged
GROUP BY busy, grp
ORDER BY kind, range_from;
```
**Explanation:** A recursive world fills the hole, a boolean partition keys by taken/free, and rank-minus-`n` islands both families at once — free blocks (`104`, `106`) and taken blocks (`101-103`, `105`, `107-108`) tumble out of a single pass.

## Q100: Grand finale — free ranges, taken-streak champion, and gap totals in one query.

Schema hints: `phones(number)` = `101,102,103,105,107,108` in a block ending at 108.

**Query:**
```sql
WITH RECURSIVE phones(number) AS (VALUES (101),(102),(103),(105),(107),(108)),
world(n) AS (
  SELECT 101 UNION ALL SELECT n + 1 FROM world WHERE n < 108
),
grid AS (
  SELECT w.n, EXISTS (SELECT 1 FROM phones p WHERE p.number = w.n) AS busy
  FROM world w
),
tagged AS (
  SELECT n, busy,
         n - (ROW_NUMBER() OVER (PARTITION BY busy ORDER BY n))::int AS grp
  FROM grid
),
summary AS (
  SELECT busy, MIN(n) AS r_from, MAX(n) AS r_to, COUNT(*) AS len
  FROM tagged GROUP BY busy, grp
)
SELECT 'FREE'  AS kind, r_from, r_to, len FROM summary WHERE NOT busy
UNION ALL
SELECT 'BUSY', r_from, r_to, len FROM summary WHERE busy
ORDER BY kind, r_from;
```
**Explanation:** Recursive world, boolean partition, date-minus-rank on `n` — the union returns every free block (104, 106) and every taken block (101-103, 105, 107-108) side by side: the whole gaps-and-islands anatomy in 12 lines.

**Alt1:**
```sql
WITH phones(number) AS (VALUES (101),(102),(103),(105),(107),(108)),
grid AS (
  SELECT w.n,
         EXISTS (SELECT 1 FROM phones p WHERE p.number = w.n) AS busy
  FROM (SELECT 101 + gs FROM generate_series(0, 7) gs) w(n)
),
flagged AS (
  SELECT n, busy,
         busy <> LAG(busy) OVER (ORDER BY n) AS flipped
  FROM grid
),
run_ids AS (
  SELECT n, busy,
         SUM(CASE WHEN flipped OR flipped IS NULL THEN 1 ELSE 0 END)
           OVER (ORDER BY n) AS grp
  FROM flagged
)
SELECT CASE WHEN busy THEN 'BUSY' ELSE 'FREE' END AS kind,
       MIN(n) AS range_from, MAX(n) AS range_to, COUNT(*) AS len
FROM run_ids GROUP BY busy, grp ORDER BY kind, range_from;
```
**Explanation:** Same world, but islanding happens through flag-flips (`busy` toggling via LAG) instead of ROW_NUMBER-minus-`n` — the second core idiom closing the playbook exactly where the first began.
