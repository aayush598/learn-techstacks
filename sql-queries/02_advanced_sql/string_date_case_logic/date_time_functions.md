# Date and Time Functions in SQL — 100 Interview Q&A

## Q1: Write a query to get the current date and time in MySQL.

**Query:**
```sql
-- MySQL
SELECT NOW() AS current_datetime;
```

**Explanation:** `NOW()` returns the current date and time in the session time zone. Use `CURRENT_TIMESTAMP` for the SQL-standard equivalent.
**Alt1:**
```sql
-- SQL Server
SELECT CURRENT_TIMESTAMP AS current_datetime;
```
**Alt1:**
```sql
-- PostgreSQL
SELECT NOW() AS current_datetime;
```
## Q2: Write a query to get only today's date (no time component) in MySQL.

**Query:**
```sql
-- MySQL
SELECT CURDATE() AS today;
```

**Explanation:** `CURDATE()` returns the current date with the time set to `00:00:00`. `CURRENT_DATE` is the ANSI SQL alias.
**Alt1:**
```sql
-- PostgreSQL
SELECT CURRENT_DATE AS today;
```
## Q3: Write a query to return the current system date in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT GETDATE() AS current_datetime;
```

**Explanation:** `GETDATE()` returns the server's current date and time. Use `SYSDATETIME()` for higher precision (datetime2).

## Q4: Write a query to return the current date and time in Oracle.

**Query:**
```sql
-- Oracle
SELECT SYSDATE FROM dual;
```

**Explanation:** `SYSDATE` returns the database server's current date and time. `SYSTIMESTAMP` additionally includes fractional seconds and time zone info.
**Alt1:**
```sql
-- MySQL
SELECT SYSDATE() FROM dual;
```
## Q5: Write a query to find orders placed in the last 7 days based on the order_date column.

**Query:**
```sql
-- MySQL
SELECT *
FROM orders
WHERE order_date >= NOW() - INTERVAL 7 DAY;
```

**Explanation:** `NOW() - INTERVAL 7 DAY` subtracts 7 days from the current moment; the comparison keeps the index on `order_date` usable.
**Alt1:**
```sql
-- PostgreSQL
SELECT * FROM orders WHERE order_date >= CURRENT_DATE - 7;
```
## Q6: Same as Q5 but additive syntax using DATE_ADD.

**Query:**
```sql
-- MySQL
SELECT *
FROM orders
WHERE order_date >= DATE_SUB(NOW(), INTERVAL 7 DAY);
```

**Explanation:** `DATE_SUB` is the explicit subtract form of `DATE_ADD`. Both accept `DAY`, `MONTH`, `YEAR`, `HOUR`, etc.

## Q7: Write a query to find orders created in the last 7 days in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT *
FROM orders
WHERE order_date >= NOW() - INTERVAL '7 days';
```

**Explanation:** Postgres uses a quoted `INTERVAL '7 days'` literal with `+`/`-` operators. `CURRENT_DATE - 7` also works when you only need whole days.
**Alt1:**
```sql
-- MySQL
SELECT * FROM orders WHERE order_date >= NOW() - INTERVAL 7 DAY;
```
## Q8: Write a query to find orders created in the last 7 days in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT *
FROM orders
WHERE order_date >= DATEADD(DAY, -7, GETDATE());
```

**Explanation:** `DATEADD(part, number, date)` adds a negative number to go back in time — here `-7` days from `GETDATE()`.

## Q9: Write a query to add 3 months to a hire_date in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT hire_date, hire_date + INTERVAL '3 months' AS plus_3_months
FROM employees;
```

**Explanation:** `INTERVAL '3 months'` added to a date yields a timestamp. Overflow from month-end is normalized (e.g. Jan 31 + 1 month becomes Feb 28).
**Alt1:**
```sql
-- Oracle
SELECT hire_date, ADD_MONTHS(hire_date, 3) FROM employees;
```
## Q10: Write a query to add 3 months to a hire_date in Oracle.

**Query:**
```sql
-- Oracle
SELECT hire_date, ADD_MONTHS(hire_date, 3) AS plus_3_months
FROM employees;
```

**Explanation:** `ADD_MONTHS(date, n)` is Oracle's dedicated month arithmetic function and correctly clamps the last day of the month.

## Q11: Write a query to add 3 months to a join_date in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT join_date, DATEADD(MONTH, 3, join_date) AS plus_3_months
FROM employees;
```

**Explanation:** `DATEADD(MONTH, 3, ...)` adds calendar months. Be aware that adding months into a shorter month returns the clamped last day.

## Q12: Write a query to compute the age (in years) of each employee from their birth_date in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT name, AGE(birth_date) AS age
FROM employees;
```

**Explanation:** `AGE(date)` returns an interval from that date to today. `AGE(date1, date2)` returns the interval between two dates.
**Alt1:**
```sql
-- SQL Server
SELECT name, DATEDIFF(YEAR, birth_date, GETDATE()) FROM employees;
```
## Q13: Write a query to get the exact age in years, months and days of a person born on 2000-06-15.

**Query:**
```sql
-- PostgreSQL
SELECT AGE(CURRENT_DATE, DATE '2000-06-15') AS exact_age;
```

**Explanation:** `AGE(today, birthdate)` produces an interval like `26 years 2 mons 28 days`, which is friendlier than a decimal count of years.

## Q14: Write a query to get the difference in days between order_date and ship_date in MySQL.

**Query:**
```sql
-- MySQL
SELECT order_id, DATEDIFF(ship_date, order_date) AS days_to_ship
FROM orders;
```

**Explanation:** MySQL's `DATEDIFF(date1, date2)` returns whole days. Note the argument order — it is `date1 - date2`.

## Q15: Write a query to get the days between two timestamps including fractional time in MySQL.

**Query:**
```sql
-- MySQL
SELECT order_id, TIMESTAMPDIFF(HOUR, order_date, ship_date) AS hours_between
FROM orders;
```

**Explanation:** `TIMESTAMPDIFF(unit, start, end)` returns the count in any unit (SECOND, MINUTE, HOUR, DAY, MONTH). For fractions, subtract the timestamps directly: `ship_date - order_date`.
**Alt1:**
```sql
-- PostgreSQL
SELECT EXTRACT(EPOCH FROM (ship_date - order_date)) / 3600 FROM orders;
```
## Q16: Write a query to compute the difference between two dates in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT ship_date - order_date AS days_to_ship
FROM orders;
```

**Explanation:** Subtracting one `DATE` from another yields an integer in Postgres. Subtracting timestamps yields an interval instead.

## Q17: Write a query to find how many days each subscription covers in PostgreSQL using timestamps.

**Query:**
```sql
-- PostgreSQL
SELECT subscription_id,
       EXTRACT(EPOCH FROM (end_ts - start_ts)) / 86400 AS days_covered
FROM subscriptions;
```

**Explanation:** Timestamp subtraction returns an interval; `EXTRACT(EPOCH FROM ...)` converts it to seconds, which is then divided by `86400` for days.

## Q18: Write a query to compute the difference in days between two dates in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT order_id, DATEDIFF(DAY, order_date, ship_date) AS days_to_ship
FROM orders;
```

**Explanation:** `DATEDIFF(unit, start, end)` counts boundaries crossed. For days this is intuitive, but for months it counts month-start boundaries, not full spans.

## Q19: Write a query to get the difference in whole months between two dates in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT order_id, DATEDIFF(MONTH, signup_date, churn_date) AS months_served
FROM accounts;
```

**Explanation:** `DATEDIFF(MONTH, ...)` counts month-boundaries crossed. If you need exact elapsed months, compute days first or divide a day count.

## Q20: Write a query to compute the difference in days between two dates in Oracle.

**Query:**
```sql
-- Oracle
SELECT order_id, ship_date - order_date AS days_to_ship
FROM orders;
```

**Explanation:** In Oracle, `DATE - DATE` directly returns a decimal number of days. Multiply by 24 for hours or 1440 for minutes.
**Alt1:**
```sql
-- MySQL
SELECT DATEDIFF(ship_date, order_date) FROM orders;
```
## Q21: Write a query to get the date 90 days from now in Oracle.

**Query:**
```sql
-- Oracle
SELECT SYSDATE + 90 AS ninety_days_from_now FROM dual;
```

**Explanation:** Adding an integer to an Oracle date adds that many days. Fractional values add fractional days (e.g. `+ 0.5` adds 12 hours).

## Q22: Write a query to add 5 business days' worth of simple interval on top of a date in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT ship_date, ship_date + INTERVAL '5 days' AS plus_5_days
FROM orders;
```

**Explanation:** This is calendar-day math, not business-day logic. True business days (skipping weekends) generally require a calendar table or a weekday-based CASE.

## Q23: Write a query to return the year, month and day components of order_date using MySQL.

**Query:**
```sql
-- MySQL
SELECT YEAR(order_date) AS yr, MONTH(order_date) AS mo, DAY(order_date) AS dy,
       DAYOFMONTH(order_date) AS dom
FROM orders;
```

**Explanation:** `YEAR()`, `MONTH()`, `DAY()`/`DAYOFMONTH()` directly extract components. These are MySQL-specific convenience functions.
**Alt1:**
```sql
-- SQL Server
SELECT DATEPART(YEAR, order_date), DATEPART(MONTH, order_date), DATEPART(DAY, order_date) FROM orders;
```
## Q24: Write a query to extract the year, month and day from a timestamp in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT EXTRACT(YEAR FROM order_date) AS yr,
       EXTRACT(MONTH FROM order_date) AS mo,
       EXTRACT(DAY FROM order_date) AS dy
FROM orders;
```

**Explanation:** `EXTRACT(field FROM source)` is the SQL-standard part extraction, returning a `numeric`. Cast to int if needed: `EXTRACT(YEAR FROM ...)::int`.
**Alt1:**
```sql
-- Oracle
SELECT EXTRACT(YEAR FROM order_date), EXTRACT(MONTH FROM order_date), EXTRACT(DAY FROM order_date) FROM orders;
```
## Q25: Write a query to get the hour, minute and second of a timestamp in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT DATEPART(HOUR, paid_at) AS hr,
       DATEPART(MINUTE, paid_at) AS mn,
       DATEPART(SECOND, paid_at) AS sc
FROM payments;
```

**Explanation:** `DATEPART(part, date)` returns the numeric component. SQL Server also offers `DATENAME()` for the string name of a part.
## Q26: Write a query to get the day of the week (0-6, Monday-based) for each order in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT order_date,
       EXTRACT(ISODOW FROM order_date) AS dow_mon_based
FROM orders;
```

**Explanation:** `ISODOW` returns 1=Monday ... 7=Sunday per ISO. `EXTRACT(DOW ...)` returns 0=Sunday ... 6=Saturday; both are in Postgres.

## Q27: Write a query to compare two dates ignoring the time portion in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT *
FROM events
WHERE CAST(event_ts AS DATE) = CAST('2026-01-05' AS DATE);
```

**Explanation:** Casting both sides to `DATE` strips the time so the comparison is day-level. Avoid casting a bare column to preserve index usage (see Q36).

## Q28: Write a query to compare dates ignoring the time portion in MySQL.

**Query:**
```sql
-- MySQL
SELECT *
FROM events
WHERE DATE(event_ts) = '2026-01-05';
```

**Explanation:** `DATE(datetime)` trims to midnight. Prefer `>= '2026-01-05 00:00:00' AND < '2026-01-06'` for index-friendly day filtering.
**Alt1:**
```sql
-- SQL Server
SELECT * FROM events WHERE CAST(event_ts AS DATE) = '2026-01-05';
```
## Q29: Write a query to compare dates ignoring the time portion in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT *
FROM events
WHERE event_ts::date = DATE '2026-01-05';
```

**Explanation:** `::date` casts the timestamp to date. For index-friendly equivalent use a range: `>= DATE '2026-01-05' AND < DATE '2026-01-06'`.

## Q30: Write a query to filter orders for the current day using an index-friendly range in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT *
FROM orders
WHERE order_ts >= CURRENT_DATE
  AND order_ts <  CURRENT_DATE + 1;
```

**Explanation:** The half-open range `[today, tomorrow)` keeps the column uncased so a b-tree index on `order_ts` can be used.

## Q31: Write a query to filter orders for the current day using an index-friendly range in MySQL.

**Query:**
```sql
-- MySQL
SELECT *
FROM orders
WHERE order_ts >= CURDATE()
  AND order_ts <  CURDATE() + INTERVAL 1 DAY;
```

**Explanation:** Same half-open range pattern. Avoiding `DATE(order_ts)` on the left side lets the optimizer seek into an index.

## Q32: Write a query to truncate a timestamp to the start of its day in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT order_ts, DATE_TRUNC('day', order_ts) AS day_start
FROM orders;
```

**Explanation:** `DATE_TRUNC('day', ts)` zeroes the time. Supported buckets include `hour`, `day`, `week`, `month`, `quarter`, `year`.

## Q33: Write a query to truncate a timestamp to the start of the month in PostgreSQL for a daily report.

**Query:**
```sql
-- PostgreSQL
SELECT DATE_TRUNC('month', order_ts) AS month_start, COUNT(*)
FROM orders
GROUP BY DATE_TRUNC('month', order_ts);
```

**Explanation:** Grouping by `DATE_TRUNC('month', ...)` buckets every order into its calendar month — the standard monthly grouping trick.

## Q34: Write a query to group sales into daily buckets in MySQL.

**Query:**
```sql
-- MySQL
SELECT DATE(sale_ts) AS sale_day, SUM(amount)
FROM sales
GROUP BY DATE(sale_ts);
```

**Explanation:** `DATE()` casts each timestamp to midnight so all sales on the same day collapse into one group.

## Q35: Write a query to group sales into weekly buckets in MySQL starting on Monday.

**Query:**
```sql
-- MySQL
SELECT DATE_ADD(DATE(sale_ts), INTERVAL (-(WEEKDAY(sale_ts))) DAY) AS week_start_mon,
       SUM(amount)
FROM sales
GROUP BY week_start_mon;
```

**Explanation:** `WEEKDAY()` returns 0 for Monday; subtracting that many days snaps each row back to the Monday of its week.
**Alt1:**
```sql
-- PostgreSQL
SELECT DATE_TRUNC('week', sale_ts) AS week_start_mon, SUM(amount) FROM sales GROUP BY 1;
```
## Q36: Explain why wrapping a column in a function breaks an index, and show the fix.

**Query:**
```sql
-- MySQL
-- Slow: function on column defeats the index
SELECT * FROM orders WHERE YEAR(order_ts) = 2026;
-- Fast: range preserves the index
SELECT * FROM orders WHERE order_ts >= '2026-01-01' AND order_ts < '2027-01-01';
```

**Explanation:** `YEAR(order_ts)` has to be computed for every row, forcing a scan. An uncased-column range lets the optimizer use a b-tree index.

## Q37: Write a query to find the first day of the current month in MySQL.

**Query:**
```sql
-- MySQL
SELECT DATE_FORMAT(CURDATE(), '%Y-%m-01') AS first_of_month;
```

**Explanation:** Re-formatting the date with the day hard-coded to `01` gives the month start without a function like `DATE_TRUNC`.

## Q38: Write a query to find the last day of the current month in MySQL.

**Query:**
```sql
-- MySQL
SELECT LAST_DAY(CURDATE()) AS last_of_month;
```

**Explanation:** `LAST_DAY(date)` returns the last day of the given date's month, correctly handling 28/29/30/31-day endings.
**Alt1:**
```sql
-- SQL Server
SELECT EOMONTH(GETDATE()) AS last_of_month;
```
## Q39: Write a query to find the last day of next month in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT EOMONTH(DATEADD(MONTH, 1, GETDATE())) AS last_of_next_month;
```

**Explanation:** `EOMONTH(date)` returns the month-end; pre-adding a month with `DATEADD` shifts the target month first.

## Q40: Write a query to get the first day of the current month in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT DATEADD(DAY, 1, EOMONTH(GETDATE(), -1)) AS first_of_month;
```

**Explanation:** `EOMONTH(date, -1)` gives the end of the previous month; adding one day lands on the first of the current month.
**Alt1:**
```sql
-- PostgreSQL
SELECT DATE_TRUNC('month', CURRENT_DATE) AS first_of_month;
```
## Q41: Write a query to get the first day and last day of the month for any date in Oracle.

**Query:**
```sql
-- Oracle
SELECT TRUNC(SYSDATE, 'MM') AS first_of_month,
       LAST_DAY(SYSDATE) AS last_of_month
FROM dual;
```

**Explanation:** `TRUNC(date, 'MM')` truncates to the first of the month; `LAST_DAY` returns the month-end.

## Q42: Write a query to get the number of days in the current month in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT EXTRACT(DAY FROM DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month - 1 day')::int AS days_in_month;
```

**Explanation:** The last day of the month, extracted as a `DAY` field, equals the count of days in that month.

## Q43: Write a query to format a date as 'YYYY-MM-DD' in MySQL.

**Query:**
```sql
-- MySQL
SELECT DATE_FORMAT(order_date, '%Y-%m-%d') AS formatted
FROM orders;
```

**Explanation:** `DATE_FORMAT` uses `%` specifiers (`%Y` 4-digit year, `%m` month, `%d` day) for total control over output.
**Alt1:**
```sql
-- SQL Server
SELECT CONVERT(VARCHAR(10), order_date, 23) FROM orders;
```
## Q44: Write a query to format a date as 'DD-MON-YYYY' and 'Month DD, YYYY' in Oracle.

**Query:**
```sql
-- Oracle
SELECT TO_CHAR(order_date, 'DD-MON-YYYY') AS short_fmt,
       TO_CHAR(order_date, 'Month DD, YYYY') AS long_fmt
FROM orders;
```

**Explanation:** `TO_CHAR(date, mask)` is Oracle's formatter. `MON` gives the abbreviated month name; `Month` the full name.
**Alt1:**
```sql
-- PostgreSQL
SELECT TO_CHAR(order_date, 'DD-MON-YYYY') FROM orders;
```
## Q45: Write a query to format a date as 'yyyy-MM-dd' in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT TO_CHAR(order_date, 'YYYY-MM-DD') AS formatted
FROM orders;
```

**Explanation:** Postgres's `TO_CHAR` uses a different mask vocabulary than MySQL: uppercase `YYYY`, `MM`, `DD`.

## Q46: Write a query to format a date as 'yyyy-MM-dd' in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT FORMAT(order_date, 'yyyy-MM-dd') AS formatted
FROM orders;
```

**Explanation:** `FORMAT` uses .NET format strings. It is handy but slow at scale; use `CONVERT`/`CAST` for large result sets.

## Q47: Write a query to convert the string '2026-01-15' into a date in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT TO_DATE('2026-01-15', 'YYYY-MM-DD') AS parsed_date;
```

**Explanation:** `TO_DATE(text, mask)` parses a string by format. With ISO strings you can also rely on `'2026-01-15'::date`.
**Alt1:**
```sql
-- MySQL
SELECT STR_TO_DATE('2026-01-15', '%Y-%m-%d') FROM dual;
```
## Q48: Write a query to parse the string '15/01/2026' (DD/MM/YYYY) into a date in MySQL.

**Query:**
```sql
-- MySQL
SELECT STR_TO_DATE('15/01/2026', '%d/%m/%Y') AS parsed_date;
```

**Explanation:** `STR_TO_DATE` is the inverse of `DATE_FORMAT`, mapping `%d/%m/%Y` to the day/month/year.

## Q49: Write a query to convert a string to a date in SQL Server expecting 'yyyy-MM-dd'.

**Query:**
```sql
-- SQL Server
SELECT CONVERT(DATE, '2026-01-15', 23) AS parsed_date;
```

**Explanation:** Style code `23` declares ISO `yyyy-MM-dd` input. `CAST('2026-01-15' AS DATE)` works when the format is unambiguous.

## Q50: Write a query to parse a free-text date like 'January 15, 2026' in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT TO_DATE('January 15, 2026', 'Month DD, YYYY') AS parsed_date;
```

**Explanation:** `Month` matches the full month name. Postgres can also auto-parse with `CAST('January 15, 2026' AS date)` due to flexible input parsing.
## Q51: Write a query to get the current timestamp in UTC in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT NOW() AT TIME ZONE 'UTC' AS utc_now;
```

**Explanation:** `AT TIME ZONE 'UTC'` converts a `timestamptz` value to a plain timestamp at the UTC offset. `CURRENT_TIMESTAMP` behaves like `NOW()`.
**Alt1:**
```sql
-- SQL Server
SELECT GETUTCDATE() AS utc_now;
```
## Q52: Write a query to get the current time in a named time zone in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT CURRENT_TIMESTAMP AT TIME ZONE 'America/New_York' AS ny_now;
```

**Explanation:** `AT TIME ZONE` accepts any IANA zone in pg_timezone_names, converting the instants to wall-clock time there.

## Q53: Write a query to shift a stored UTC timestamp to the user's local display time in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT event_ts AT TIME ZONE 'America/Los_Angeles' AS local_ts
FROM events;
```

**Explanation:** `timestamptz AT TIME ZONE 'zone'` reinterprets the instant in the given zone, respecting DST. Filter first, display last.
**Alt1:**
```sql
-- SQL Server
SELECT created_at AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific Standard Time' FROM events;
```
## Q54: Write a query to get the current time in SQL Server with time zone info.

**Query:**
```sql
-- SQL Server
SELECT SYSDATETIMEOFFSET() AS now_with_offset;
```

**Explanation:** `SYSDATETIMEOFFSET()` returns a datetimeoffset carrying the server's UTC offset. Prefer storing `datetimeoffset` to keep instants unambiguous.

## Q55: Write a query to convert a UTC datetimeoffset value to another time zone in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT created_at AT TIME ZONE 'UTC' AT TIME ZONE 'India Standard Time' AS ist_time
FROM records;
```

**Explanation:** `AT TIME ZONE` in SQL Server converts between zones. Failing to declare the source zone first is the classic bug.

## Q56: Write a query to get the current UTC timestamp in MySQL.

**Query:**
```sql
-- MySQL
SELECT UTC_TIMESTAMP() AS utc_now;
```

**Explanation:** `UTC_TIMESTAMP()` returns the current UTC date/time regardless of session `time_zone`. `NOW()` reflects the session zone instead.

## Q57: Write a query to compare NOW() and CURRENT_TIMESTAMP in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT NOW() AS a, CURRENT_TIMESTAMP AS b, NOW() = CURRENT_TIMESTAMP AS same;
```

**Explanation:** Both return the transaction start time and are effectively identical in PostgreSQL. `CLOCK_TIMESTAMP()` differs as it reflects real time.

## Q58: Write a query to find rows created on a specific date ignoring their timezone offset in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT *
FROM events
WHERE event_ts AT TIME ZONE 'UTC' >= '2026-03-15 00:00:00'
  AND event_ts AT TIME ZONE 'UTC' <  '2026-03-16 00:00:00';
```

**Explanation:** Normalizing to UTC first makes day boundaries consistent even though each row stores its original offset.

## Q59: Write a query to get the day of the week name for each order date in MySQL.

**Query:**
```sql
-- MySQL
SELECT order_date, DAYNAME(order_date) AS day_name
FROM orders;
```

**Explanation:** `DAYNAME()` returns 'Monday', 'Tuesday', etc. `WEEKDAY()` returns the 0-6 numeric Monday-based index.

## Q60: Write a query to get the full month name of a date in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT TO_CHAR(order_date, 'FMMonth') AS month_name
FROM orders;
```

**Explanation:** `Month` yields the padded name by default; the `FM` modifier strips trailing spaces. `Mon` gives the abbreviated form.

## Q61: Write a query to get the ISO week number and ISO year of a date in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT EXTRACT(ISOWEEK FROM order_date) AS iso_week,
       EXTRACT(ISOYEAR FROM order_date) AS iso_year
FROM orders;
```

**Explanation:** ISO weeks are Monday-based and can straddle calendar years, so the ISO year may differ from `EXTRACT(YEAR ...)` in early January.
**Alt1:**
```sql
-- SQL Server
SELECT DATEPART(ISO_WEEK, order_date) FROM orders;
```
## Q62: Write a query to get the week number of a date in MySQL with the week starting on Monday.

**Query:**
```sql
-- MySQL
SELECT WEEK(order_date, 1) AS monday_week
FROM orders;
```

**Explanation:** The mode argument `1` forces Monday start per ISO. `WEEK(order_date)` uses Sunday by default (mode 0).

## Q63: Write a query to find the Monday of the current week in PostgreSQL (ISO week).

**Query:**
```sql
-- PostgreSQL
SELECT DATE_TRUNC('week', CURRENT_DATE) AS monday_of_week;
```

**Explanation:** Postgres's `week` bucket always starts on Monday, matching ISO 8601. Sunday-start weeks require manual offset math.
**Alt1:**
```sql
-- MySQL
SELECT DATE_ADD(CURDATE(), INTERVAL -WEEKDAY(CURDATE()) DAY) AS monday_of_week;
```
## Q64: Write a query to find the Monday of the current week in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT DATEADD(DAY, 2 - DATEPART(WEEKDAY, GETDATE()), CAST(GETDATE() AS DATE)) AS week_start_mon;
```

**Explanation:** `DATEPART(WEEKDAY, ...)` returns 1=Sunday by default, so `2 - weekday` yields 0 on Monday and negative offsets earlier in the week.

## Q65: Write a query to determine if a date falls on a weekend in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT order_date,
       CASE WHEN EXTRACT(ISODOW FROM order_date) IN (6, 7)
            THEN 'weekend' ELSE 'weekday' END AS kind
FROM orders;
```

**Explanation:** `ISODOW` gives 1-7 with 6 and 7 being Saturday/Sunday, making weekend checks explicit and readable.

## Q66: Write a query to count business days (Monday-Friday) between two dates in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT COUNT(*) AS business_days
FROM generate_series(
       DATE '2026-01-05',
       DATE '2026-01-16',
       INTERVAL '1 day') AS d(day)
WHERE EXTRACT(ISODOW FROM day) IN (1, 2, 3, 4, 5);
```

**Explanation:** `generate_series` expands every day in range and the `ISODOW` filter counts only weekdays — a pure-SQL business-day counter.
**Alt1:**
```sql
-- SQL Server
SELECT COUNT(*) FROM (
  SELECT DATEADD(DAY, n.n-1, '2026-01-05') AS day
  FROM (SELECT TOP (12) ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) n FROM sys.all_objects) n
) g
WHERE DATEPART(WEEKDAY, g.day) BETWEEN 2 AND 6;
```
## Q67: Write a query to count business days between two dates without a series in MySQL (simplified).

**Query:**
```sql
-- MySQL
SELECT DATEDIFF('2026-01-16', '2026-01-05') + 1
     - 2 * (FLOOR(DATEDIFF('2026-01-16', '2026-01-05') / 7))
     - CASE WHEN DAYOFWEEK('2026-01-16') <= DAYOFWEEK('2026-01-05') THEN 2 ELSE 0 END
       AS approx_business_days;
```

**Explanation:** This formula subtracts whole weekend weeks and corrects for the remainder window. It ignores holidays; a calendar table is more robust.

## Q68: Write a query to count business days between two dates using a calendar table in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT COUNT(*)
FROM dbo.calendar
WHERE cal_date >= CAST('2026-01-05' AS DATE)
  AND cal_date <  CAST('2026-01-17' AS DATE)
  AND is_business_day = 1;
```

**Explanation:** A pre-computed calendar table (marking weekends and holidays) is the standard, index-friendly and holiday-aware approach.

## Q69: Write a query to generate a series of all days in January 2026 in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT generate_series(DATE '2026-01-01', DATE '2026-01-31', INTERVAL '1 day')::date AS day;
```

**Explanation:** `generate_series` produces one row per interval step across the range. It is the workhorse for date-bucket and gapping reports.
**Alt1:**
```sql
-- MySQL
WITH RECURSIVE jan AS (
  SELECT DATE('2026-01-01') d
  UNION ALL SELECT d + INTERVAL 1 DAY FROM jan WHERE d < '2026-01-31')
SELECT * FROM jan;
```
## Q70: Write a query to generate a month-by-month series for the last 12 months in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT DATE_TRUNC('month', generate_series(
         CURRENT_DATE - INTERVAL '11 months',
         CURRENT_DATE,
         INTERVAL '1 month')) AS month_start;
```

**Explanation:** Stepping the series by `1 month` yields one row per month, useful for zero-filling monthly dashboards.

## Q71: Write a query to fill missing days in a daily aggregate using generate_series in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT g.day, COALESCE(t.total, 0) AS total
FROM generate_series(CURRENT_DATE - 6, CURRENT_DATE, INTERVAL '1 day') AS g(day)
LEFT JOIN (SELECT sale_ts::date AS day, SUM(amount) AS total
           FROM sales GROUP BY sale_ts::date) t
       ON t.day = g.day;
```

**Explanation:** The series drives the outer join so days with no sales still appear with a zero — solving the classic "missing dates" gap problem.

## Q72: Write a query to generate a recursive date series in MySQL 8+.

**Query:**
```sql
-- MySQL
WITH RECURSIVE date_series AS (
  SELECT DATE('2026-01-01') AS d
  UNION ALL
  SELECT d + INTERVAL 1 DAY FROM date_series WHERE d < DATE('2026-01-31')
)
SELECT * FROM date_series;
```

**Explanation:** MySQL lacks `generate_series`, so a `WITH RECURSIVE` CTE builds each next day by adding `INTERVAL 1 DAY`. Works as of MySQL 8.0.

## Q73: Write a query to generate a year of dates using a numbers table in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT DATEADD(DAY, n.n - 1, '2026-01-01') AS day
FROM (SELECT TOP (365) ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n
      FROM sys.all_objects) AS n;
```

**Explanation:** A numbers/stack approach multiplies a row number into `DATEADD(DAY, ...)`. SQL Server 2022+ could use `GENERATE_SERIES`.

## Q74: Write a query to find all orders from the year-to-date in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT *
FROM orders
WHERE order_date >= DATE_TRUNC('year', CURRENT_DATE)
  AND order_date <  DATE_TRUNC('year', CURRENT_DATE) + INTERVAL '1 year';
```

**Explanation:** The YTD window is bounded by `[Jan 1 of this year, Jan 1 next year)`, keeping the range operator-based and index scan-free.

## Q75: Write a query to find orders from the last complete month in MySQL.

**Query:**
```sql
-- MySQL
SELECT *
FROM orders
WHERE order_date >= DATE_FORMAT(CURDATE() - INTERVAL 1 MONTH, '%Y-%m-01')
  AND order_date <  DATE_FORMAT(CURDATE(), '%Y-%m-01');
```

**Explanation:** Shifting back one month then formatting to `'01'` gives last month's first day; the current month's first day becomes the exclusive bound.
## Q76: Write a query to find records from the last complete month in PostgreSQL using date_trunc.

**Query:**
```sql
-- PostgreSQL
SELECT *
FROM orders
WHERE order_date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
  AND order_date <  DATE_TRUNC('month', CURRENT_DATE);
```

**Explanation:** Truncating the previous and current month gives a clean half-open interval for last month's data — immune to the current day of the month.

## Q77: Write a query to report monthly revenue for the last complete quarter in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT DATEPART(YEAR, order_date) AS yr,
       DATEPART(MONTH, order_date) AS mo,
       SUM(amount) AS revenue
FROM orders
WHERE order_date >= DATEFROMPARTS(YEAR(GETDATE()),
                   ((DATEPART(QUARTER, GETDATE()) - 2) * 3), 1)
  AND order_date <  DATEADD(QUARTER, DATEDIFF(QUARTER, 0, GETDATE()), 0);
```

**Explanation:** The bounds span the three months of the previous quarter. The upper edge resets to the start of the current quarter.

## Q78: Write a query to bucket sales into fiscal quarters in Oracle.

**Query:**
```sql
-- Oracle
SELECT TO_CHAR(sale_date, 'Q') AS fiscal_q,
       TO_CHAR(sale_date, 'YYYY') AS yr,
       SUM(amount) AS revenue
FROM sales
GROUP BY TO_CHAR(sale_date, 'YYYY'), TO_CHAR(sale_date, 'Q');
```

**Explanation:** Oracle's `Q` format masks the calendar quarter. A custom fiscal calendar (e.g. April start) needs a `CASE` offset or a fiscal date dimension.

## Q79: Write a query to bucket sales into fiscal quarters in PostgreSQL where the fiscal year starts in April.

**Query:**
```sql
-- PostgreSQL
SELECT EXTRACT(YEAR FROM sale_date - INTERVAL '3 months') AS fiscal_year,
       (EXTRACT(QUARTER FROM sale_date - INTERVAL '3 months'))::int AS fiscal_q,
       SUM(amount) AS revenue
FROM sales
GROUP BY 1, 2;
```

**Explanation:** Shifting the date back by three months aligns an April fiscal year onto the January calendar quarter, so April-June becomes Q1.
**Alt1:**
```sql
-- Oracle
SELECT fiscal_yr, fiscal_q, SUM(amount) FROM (
  SELECT amount, EXTRACT(YEAR FROM ADD_MONTHS(sale_date, -3)) fiscal_yr,
         TO_CHAR(ADD_MONTHS(sale_date, -3), 'Q') fiscal_q
  FROM sales) GROUP BY fiscal_yr, fiscal_q;
```
## Q80: Write a query to group events into 15-minute time buckets in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT date_trunc('hour', event_ts) + INTERVAL '15 min' *
       (EXTRACT(MINUTE FROM event_ts)::int / 15) AS bucket_start,
       COUNT(*)
FROM events
GROUP BY bucket_start;
```

**Explanation:** The floor of the minute divided by 15 yields the bucket index; multiplying back per-bucket start. `date_bin` in Postgres 14+ does this natively.

## Q81: Write a query to group events into 30-minute buckets in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT DATEADD(MINUTE, DATEDIFF(MINUTE, '2026-01-01', event_ts) / 30 * 30, '2026-01-01') AS bucket_start,
       COUNT(*)
FROM events
GROUP BY DATEADD(MINUTE, DATEDIFF(MINUTE, '2026-01-01', event_ts) / 30 * 30, '2026-01-01');
```

**Explanation:** Integer division of the minute-diff by 30 floors the bucket; multiplying by 30 and re-adding anchors to the epoch.

## Q82: Write a query to detect duplicate last 7 days records where only the time differs (same day) in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT user_id, order_ts::date AS day, COUNT(*)
FROM orders
WHERE order_ts >= CURRENT_DATE - 7
GROUP BY user_id, order_ts::date
HAVING COUNT(*) > 1;
```

**Explanation:** Casting to `date` collapses rows within the same day so time-of-day differences are ignored when counting duplicates.

## Q83: Write a query to find orders that shipped later than 3 days after ordering in Oracle.

**Query:**
```sql
-- Oracle
SELECT order_id
FROM orders
WHERE ship_date - order_date > 3;
```

**Explanation:** `DATE - DATE` returns days in Oracle, so a simple `> 3` gives a >3-day delay without extra function calls.

## Q84: Write a query to get the average order-to-ship time in hours in MySQL.

**Query:**
```sql
-- MySQL
SELECT AVG(TIMESTAMPDIFF(HOUR, order_date, ship_date)) AS avg_hours
FROM orders;
```

**Explanation:** `TIMESTAMPDIFF(HOUR, ...)` computes whole hours per row, then `AVG` aggregates them. For precision use `TIMESTAMPDIFF(SECOND, ...) / 3600`.

## Q85: Write a query to find the signup that has lasted the longest in months in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT TOP 1 account_id, DATEDIFF(MONTH, signup_date, COALESCE(churn_date, GETDATE())) AS months_lived
FROM accounts
ORDER BY months_lived DESC;
```

**Explanation:** `COALESCE` treats still-active accounts as ending today. `DATEDIFF(MONTH, ...)` counts month boundaries, which overstates partial months.

## Q86: Write a query to compute a person's exact age in years as an integer in SQL Server (birthday-aware).

**Query:**
```sql
-- SQL Server
SELECT name,
       DATEDIFF(YEAR, birth_date, GETDATE())
       - CASE WHEN DATEADD(YEAR, DATEDIFF(YEAR, birth_date, GETDATE()), birth_date) > CAST(GETDATE() AS DATE)
              THEN 1 ELSE 0 END AS age_years
FROM people;
```

**Explanation:** The naive `DATEDIFF(YEAR)` over-counts before the birthday; re-adding the years and comparing to today subtracts one when the birthday hasn't arrived.

## Q87: Write a query to find employees whose birthday is today in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT *
FROM employees
WHERE EXTRACT(MONTH FROM birth_date) = EXTRACT(MONTH FROM CURRENT_DATE)
  AND EXTRACT(DAY FROM birth_date) = EXTRACT(DAY FROM CURRENT_DATE);
```

**Explanation:** Comparing month and day parts independently sidesteps the year and works across leap-day birthdays (Feb 29 wraps to Feb 28 — handle with `OR`).

## Q88: Write a query to find people turning 18 this year (birthday-aware) in MySQL.

**Query:**
```sql
-- MySQL
SELECT *
FROM people
WHERE birth_date <= STR_TO_DATE(CONCAT(YEAR(CURDATE()), '-12-31'), '%Y-%m-%d')
  AND DATE_ADD(birth_date, INTERVAL 18 YEAR) >= DATE_FORMAT(CURDATE(), '%Y-01-01');
```

**Explanation:** A person turns 18 this year if their 18th birthday falls on or after Jan 1 and on or before Dec 31 of this year.

## Q89: Write a query to handle Feb 29 birthdays (next real celebration date) in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT name, birth_date,
       CASE WHEN EXTRACT(MONTH FROM birth_date) = 2 AND EXTRACT(DAY FROM birth_date) = 29
            THEN (CURRENT_DATE + INTERVAL '1 day')::date
            ELSE birth_date END AS next_real_birthday
FROM employees;
```

**Explanation:** Leap-day logic is inherently edge-case-driven. A robust approach joins to a calendar table that maps Feb 29 to Feb 28 in non-leap years.

## Q90: Write a query to find orders where the shipping took place across a leap year February in MySQL.

**Query:**
```sql
-- MySQL
SELECT order_id
FROM orders
WHERE (order_date <= '2028-02-28' OR order_date <= '2027-02-28')
  AND ship_date >= '2028-02-29'
  AND order_date < ship_date;
```

**Explanation:** The `2028-02-29` boundary only exists in leap years, so 2027's orders can never cross it. Interval math must respect actual calendar lengths.

## Q91: Write a query to list dates that are international holidays using a series plus a mapping in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT d,
       CASE WHEN EXTRACT(ISODOW FROM d) IN (6, 7) THEN 'Weekend'
            WHEN d = DATE '2026-12-25' THEN 'Christmas'
            ELSE 'Workday' END AS kind
FROM generate_series(DATE '2026-12-01', DATE '2026-12-31', INTERVAL '1 day') AS d;
```

**Explanation:** Combining generated dates with `CASE` labels shows how series and date-part logic build calendars without an external table.

## Q92: Write a query to compare month-over-month growth using month-first-day bucketing in MySQL.

**Query:**
```sql
-- MySQL
SELECT DATE_FORMAT(sale_date, '%Y-%m-01') AS month_start,
       SUM(amount) AS revenue,
       LAG(SUM(amount)) OVER (ORDER BY DATE_FORMAT(sale_date, '%Y-%m-01')) AS prev_revenue
FROM sales
GROUP BY DATE_FORMAT(sale_date, '%Y-%m-01');
```

**Explanation:** Bucketing by the formatted month start makes the `LAG` window compare adjacent months directly. MySQL 8+ supports window functions.

## Q93: Write a query to find the earliest order date per customer and the days since then in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT customer_id,
       MIN(order_date) AS first_order,
       (CURRENT_DATE - MIN(order_date)) AS days_since_first
FROM orders
GROUP BY customer_id;
```

**Explanation:** `CURRENT_DATE - MIN(order_date)` computes day counts inline because `DATE - DATE = integer` in Postgres.

## Q94: Write a query to report daily active users filtering only today's activity index-friendly in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT COUNT(DISTINCT user_id) AS dau
FROM activity
WHERE activity_ts >= CURRENT_DATE
  AND activity_ts <  CURRENT_DATE + 1;
```

**Explanation:** The range form stays on today's rows without wrapping `activity_ts`, so a composite index on `(activity_ts, user_id)` can serve the scan.

## Q95: Write a query to find the last 30 days average order value with time filters in Oracle.

**Query:**
```sql
-- Oracle
SELECT order_date_d, AVG(amount) OVER (ORDER BY order_date_d ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS avg_30d
FROM (SELECT TRUNC(order_date) AS order_date_d, SUM(amount) AS amount
      FROM orders GROUP BY TRUNC(order_date))
ORDER BY order_date_d;
```

**Explanation:** `TRUNC(order_date)` normalizes each order to a day; the analytic window then averages the trailing 30 daily buckets.

## Q96: Write a query to find customer first purchase month vs last purchase month (retention spread) in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT customer_id,
       FORMAT(MIN(order_date), 'yyyy-MM') AS first_month,
       FORMAT(MAX(order_date), 'yyyy-MM') AS last_month,
       DATEDIFF(MONTH, MIN(order_date), MAX(order_date)) AS months_span
FROM orders
GROUP BY customer_id;
```

**Explanation:** `FORMAT` pins each row's min/max to `yyyy-MM`; `DATEDIFF(MONTH, ...)` gives the boundary-count difference between the two.

## Q97: Write a query to find whether a date's month has 5 Sundays in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT d::date AS month,
       COUNT(*) FILTER (WHERE EXTRACT(ISODOW FROM d) = 7) AS sundays
FROM generate_series(
       DATE '2026-03-01',
       (DATE '2026-03-01' + INTERVAL '1 month - 1 day')::date,
       INTERVAL '1 day') AS d
WHERE EXTRACT(ISODOW FROM d) = 7
GROUP BY d::date;
```

**Explanation:** Only Sundays are generated (the `ISODOW = 7` filter), counted per month. Five Sundays appear when the month spans five distinct Sunday positions.

## Q98: Write a query to compute the last day of the previous quarter in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT DATE_TRUNC('quarter', CURRENT_DATE - INTERVAL '1 quarter')
         + INTERVAL '1 quarter - 1 day' AS last_day_prev_quarter;
```

**Explanation:** Truncating to the previous quarter start then adding `1 quarter - 1 day` lands exactly on its last day.

## Q99: Write a query to find records created exactly between noon and 1 PM on any date in MySQL (ignoring the date part of the comparison).

**Query:**
```sql
-- MySQL
SELECT *
FROM events
WHERE TIME(event_ts) BETWEEN '12:00:00' AND '12:59:59';
```

**Explanation:** `TIME()` extracts only the time-of-day portion, letting you compare across all days. For large tables, a generated column storing `TIME(event_ts)` keeps it indexable.

## Q100: Write a query to detect interval-arithmetic overflow: adding one month to Jan 31 in MySQL vs expected Feb 28.

**Query:**
```sql
-- MySQL
SELECT DATE('2026-01-31') + INTERVAL 1 MONTH AS mysql_result;          -- 2026-02-28
SELECT DATEADD(MONTH, 1, '2026-01-31');                                 -- SQL Server: 2026-02-28
-- PostgreSQL
SELECT DATE '2026-01-31' + INTERVAL '1 month';                          -- 2026-02-28 00:00:00
-- Oracle
SELECT ADD_MONTHS(DATE '2026-01-31', 1) FROM dual;                     -- 2026-02-28
```

**Explanation:** All major dialects clamp month-end overflow to the last day of the target month. Chain backward (e.g. add one month, then subtract one day) to safely land on month boundaries.
