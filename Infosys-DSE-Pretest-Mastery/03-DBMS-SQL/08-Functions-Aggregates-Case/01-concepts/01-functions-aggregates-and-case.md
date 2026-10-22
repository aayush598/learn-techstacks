# Functions, Aggregates and CASE — The Complete Toolkit

> Section 3 · DBMS & SQL · Functions, Aggregates & CASE · _Estimated reading time: 12 min_
> **Prerequisite:** [SQL Basics: DDL & DML](../01-SQL-Basics-DDL-DML/01-concepts/02-select-filter-sort-and-subqueries.md)

## In one sentence

**Scalar functions transform one row, aggregates collapse many rows into one, `CASE` picks a value
by condition, and window functions compute across a set without collapsing it.**

## Why the pre-test tests this

- This is the topic the exam loves, because each question is small and the options are function
  names.
- Typical questions: "Which function removes trailing spaces?", "What does `COUNT(DISTINCT
  cust_id)` return?", "What is the value of this `CASE` expression?", "Which clause filters
  groups?"
- There is no computation to get wrong — you either know the function or you do not.

## Core concept

### 1. The four families

| Family | Rows in → rows out | Used in | Examples |
|---|---|---|---|
| **Scalar** | 1 → 1 | `SELECT` list, `WHERE`, `ORDER BY` | `UPPER`, `ROUND`, `LENGTH`, `NOW()` |
| **Aggregate** | N → 1 | `SELECT` list with `GROUP BY` | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` |
| **Window** | N → N | `SELECT` list with `OVER ()` | `ROW_NUMBER`, `RANK`, `LAG`, `SUM OVER` |
| **Conditional** | 1 → 1 | Anywhere a value is allowed | `CASE`, `COALESCE`, `NULLIF`, `IFNULL`, `IIF` |

**The single most useful distinction:** an **aggregate collapses** the rows; a **window function
does not**.

### 2. String functions

| Function | Returns | Example |
|---|---|---|
| `UPPER(s)` | Uppercase | `UPPER('ananya')` → `ANANYA` |
| `LOWER(s)` | Lowercase | `LOWER('ANANYA')` → `ananya` |
| `LENGTH(s)` / `CHAR_LENGTH(s)` | Number of characters | `LENGTH('Ananya')` → 6 |
| `TRIM(s)` | Both ends stripped | `TRIM('  Ananya  ')` → `Ananya` |
| `LTRIM(s)` / `RTRIM(s)` | Left / right only | `RTRIM('Ananya  ')` → `Ananya` |
| `SUBSTRING(s, start, len)` / `SUBSTR` | Part of the string | `SUBSTRING('Ananya', 1, 3)` → `Ana` |
| `LEFT(s, n)` / `RIGHT(s, n)` | From the start / end | `RIGHT('Ananya', 3)` → `nya` |
| `CONCAT(a, b, ...)` | Joined, `NULL` if any arg is `NULL` | `CONCAT('Ananya', ' ', 'Rao')` |
| `CONCAT_WS(sep, a, b, ...)` | Joined with a separator; skips `NULL`s | `CONCAT_WS('-', 'Ananya', 'Rao')` |
| `REPLACE(s, from, to)` | Replace all occurrences | `REPLACE('Pune Pune', 'Pune', 'Mumbai')` |
| `LPAD(s, n, pad)` / `RPAD` | Pad to length `n` | `LPAD('7', 3, '0')` → `007` |
| `REVERSE(s)` | Reversed | `REVERSE('abc')` → `cba` |
| `REPEAT(s, n)` | Repeated | `REPEAT('-', 5)` → `-----` |
| `LOCATE(sub, s)` / `POSITION` / `INSTR` | 1-based position, 0 if not found | `LOCATE('n', 'Ananya')` → 2 |
| `COALESCE(a, b, ...)` | First non-NULL argument | `COALESCE(NULL, 'N/A')` → `N/A` |
| `NULLIF(a, b)` | `NULL` if `a = b`, else `a` | `NULLIF(10, 10)` → `NULL` |

**`CONCAT` vs `CONCAT_WS`:** `CONCAT` returns `NULL` if **any** argument is `NULL`. `CONCAT_WS`
skips `NULL`s and uses the separator. This is a classic exam question.

**`COALESCE` vs `CASE`:** `COALESCE(a, b)` is exactly `CASE WHEN a IS NOT NULL THEN a ELSE b END`.
Use `COALESCE` when there is one fallback; use `CASE` when the rule is conditional.

### 3. Numeric functions

| Function | Returns | Note |
|---|---|---|
| `ROUND(x, d)` | Rounded to `d` decimals | `ROUND(4800.567, 1)` → `4800.6` |
| `TRUNC(x, d)` | Truncated, not rounded | `TRUNC(4800.567, 1)` → `4800.5` |
| `CEIL(x)` / `CEILING` | Round up | `CEIL(10.1)` → 11 |
| `FLOOR(x)` | Round down | `FLOOR(10.9)` → 10 |
| `ABS(x)` | Absolute value | `ABS(-5)` → 5 |
| `MOD(a, b)` | Remainder | `MOD(10, 3)` → 1 |
| `POWER(a, b)` | `a` raised to `b` | `POWER(2, 10)` → 1024 |
| `SQRT(x)` | Square root | `SQRT(16)` → 4 |
| `SIGN(x)` | -1, 0 or 1 | `SIGN(-5)` → -1 |
| `RAND()` | Random number 0 ≤ x < 1 | Non-deterministic |

**`ROUND` vs `TRUNC`:** `ROUND(2.5)` → 3, `TRUNC(2.5)` → 2. This is a favourite exam pair.

### 4. Date and time functions

| Function | Returns |
|---|---|
| `CURRENT_DATE` | Today's date |
| `CURRENT_TIME` | Current time |
| `CURRENT_TIMESTAMP` | Both |
| `NOW()` | Both (MySQL) |
| `EXTRACT(YEAR FROM d)` | The year as a number |
| `YEAR(d)` / `MONTH(d)` / `DAY(d)` | The parts |
| `DATE_ADD(d, INTERVAL n unit)` | Shift forward |
| `DATE_SUB(d, INTERVAL n unit)` | Shift back |
| `DATEDIFF(d1, d2)` | Days between (MySQL: `d1 - d2`) |
| `LAST_DAY(d)` | Last day of the month |
| `DATE_FORMAT(d, fmt)` | Formatted string |

**Standard SQL note:** `EXTRACT(field FROM date)` is the portable form; `YEAR()`, `NOW()` and
`DATE_FORMAT()` are MySQL-specific. PostgreSQL uses `date_part('year', d)` and `to_char(d, fmt)`.

### 5. Aggregate functions

| Function | Ignores NULL? | Returns |
|---|---|---|
| `COUNT(*)` | n/a — counts rows including NULL-padded ones | Number of rows |
| `COUNT(col)` | ✅ | Number of non-NULL values |
| `COUNT(DISTINCT col)` | ✅ | Number of distinct non-NULL values |
| `SUM(col)` | ✅ | Total; `NULL` if no non-NULL values |
| `AVG(col)` | ✅ | Mean of the non-NULL values |
| `MIN(col)` / `MAX(col)` | ✅ | Smallest / largest |
| `STDDEV(col)` / `VARIANCE(col)` | ✅ | Spread (not in all DBMS) |

**Aggregate + string concatenation**

| Function | DBMS |
|---|---|
| `GROUP_CONCAT(col SEPARATOR ', ')` | MySQL |
| `STRING_AGG(col, ', ')` | PostgreSQL, SQL Server |
| `LISTAGG(col, ', ')` | Oracle |

```sql
SELECT cust_id, GROUP_CONCAT(proj_name ORDER BY proj_name SEPARATOR ', ')
FROM enrollments JOIN projects USING (proj_id)
GROUP BY cust_id;
```

**The rules that matter**

1. An aggregate with **no `GROUP BY`** returns **exactly one row**.
2. Aggregates in the `SELECT` list require every non-aggregated column to be in the `GROUP BY`.
3. `HAVING` filters **groups**; `WHERE` filters **rows before grouping**.
4. `COUNT(*)` and `COUNT(col)` differ by the number of NULLs — this changes the answer to a
   `LEFT JOIN` question.
5. `AVG(col)` divides by the **count of non-NULL values**, not by `COUNT(*)`.

### 6. Window functions

A window function computes across a set of rows but **does not collapse them** — every row stays in
the output.

```sql
SELECT
  cust_id,
  cust_name,
  SUM(order_amt) OVER (PARTITION BY cust_id) AS cust_total,
  ROW_NUMBER() OVER (PARTITION BY cust_id ORDER BY order_amt DESC) AS rn,
  RANK()       OVER (ORDER BY order_amt DESC)                    AS rnk
FROM orders;
```

| Function | Returns |
|---|---|
| `ROW_NUMBER()` | 1, 2, 3… with **no ties** — always distinct |
| `RANK()` | 1, 2, 2, 4 — ties share a rank and **skip** the next value |
| `DENSE_RANK()` | 1, 2, 2, 3 — ties share a rank and **do not skip** |
| `NTILE(n)` | Distribute rows into `n` buckets |
| `LAG(col, n)` | Value from `n` rows **before** the current row |
| `LEAD(col, n)` | Value from `n` rows **after** the current row |
| `FIRST_VALUE(col)` / `LAST_VALUE(col)` | First / last value in the window |
| `SUM/AVG/COUNT(col) OVER (...)` | A running or partitioned aggregate |

**`ROW_NUMBER` vs `RANK` vs `DENSE_RANK`** — the classic exam trio:

| Values | `ROW_NUMBER` | `RANK` | `DENSE_RANK` |
|---|---|---|---|
| 100, 90, 90, 80 | 1, 2, 3, 4 | 1, 2, 2, 4 | 1, 2, 2, 3 |

**`RANK` skips; `DENSE_RANK` does not.** `ROW_NUMBER` never ties at all.

**The `OVER` clause**

```sql
OVER ( [PARTITION BY cols] [ORDER BY cols] [frame] )
```

| Part | Meaning |
|---|---|
| `PARTITION BY` | Restart the calculation for each group — like a `GROUP BY` that does not collapse |
| `ORDER BY` | The order inside the window — required for `ROW_NUMBER`, `RANK`, `LAG`, `LEAD` |
| `ROWS BETWEEN ...` | The frame — which rows the aggregate sees. `UNBOUNDED PRECEDING` to `CURRENT ROW` gives a running total |

**Standard SQL note:** window functions require **MySQL 8.0+** (or PostgreSQL, Oracle, SQL Server).
MySQL 5.7 and earlier do not have them.

### 7. `CASE` expressions

**Simple `CASE`** — compares a single expression to a list of values.

```sql
CASE status
  WHEN 'NEW'     THEN 'Pending'
  WHEN 'PAID'    THEN 'Complete'
  WHEN 'CANCEL'  THEN 'Closed'
  ELSE 'Unknown'
END
```

**Searched `CASE`** — evaluates a list of conditions in order, and takes the **first** that is true.

```sql
CASE
  WHEN order_amt >= 1000 THEN 'High'
  WHEN order_amt >= 500  THEN 'Medium'
  ELSE 'Low'
END
```

**The rules**

| Rule | Detail |
|---|---|
| Evaluation order | `CASE` takes the **first** matching `WHEN` and ignores the rest |
| No match | The `ELSE` branch runs. **Without `ELSE` the result is `NULL`** |
| `END` | Required |
| Nesting | `CASE` inside `CASE` is allowed and common |
| Type | All `THEN`/`ELSE` results should be of a compatible type |
| Where it goes | Anywhere a value is allowed — `SELECT` list, `WHERE`, `ORDER BY`, `GROUP BY` |

**`CASE` in a `WHERE` clause** — remember the `WHERE` filters rows **before** grouping, so you
cannot reference an aggregate there. Use `HAVING` for aggregate conditions.

### 8. `COALESCE`, `NULLIF`, `IFNULL`, `IIF`

| Function | Returns | Equivalent |
|---|---|---|
| `COALESCE(a, b, c)` | First non-NULL argument | `CASE WHEN a IS NOT NULL THEN a WHEN b IS NOT NULL THEN b ELSE c END` |
| `NULLIF(a, b)` | `NULL` if `a = b`, otherwise `a` | — |
| `IFNULL(a, b)` (MySQL) | `b` if `a` is NULL, else `a` | `COALESCE(a, b)` for two args |
| `IIF(cond, a, b)` (SQL Server) | `a` if condition true, else `b` | `CASE WHEN cond THEN a ELSE b END` |

**`NULLIF` is used to avoid a division-by-zero error:**

```sql
SELECT SUM(amount) / NULLIF(COUNT(*), 0) AS avg_amount
FROM orders;
```

### 9. `WHERE` vs `GROUP BY` vs `HAVING`

| Clause | Filters | When it runs | Can it use aggregates? |
|---|---|---|---|
| `WHERE` | **Rows** | **Before** grouping | ❌ No |
| `GROUP BY` | Groups rows into buckets | After `WHERE` | — |
| `HAVING` | **Groups** | **After** grouping | ✅ Yes |

**The rule that trips people up:** a condition on an aggregate goes in `HAVING`, never in `WHERE`.

```sql
SELECT cust_id, SUM(order_amt) AS total
FROM orders
WHERE order_amt > 400          -- filters individual rows first
GROUP BY cust_id
HAVING SUM(order_amt) > 1000;  -- filters the groups
```

### 10. `DISTINCT` vs `GROUP BY`

| | `DISTINCT` | `GROUP BY` |
|---|---|---|
| Removes duplicate rows | ✅ | ✅ (implicitly) |
| Can compute aggregates | ❌ | ✅ |
| Needs an aggregate in the select list | ❌ | Often |
| Use it when | You want unique values of the selected columns | You want a summary per group |

`SELECT DISTINCT cust_name FROM orders` and `SELECT cust_name FROM orders GROUP BY cust_name`
return the same set of names — but only the `GROUP BY` version can also show `COUNT(*)`.

### 11. CTEs — `WITH`

```sql
WITH big_orders AS (
  SELECT cust_id, SUM(order_amt) AS total
  FROM orders
  GROUP BY cust_id
  HAVING SUM(order_amt) > 1000
)
SELECT c.cust_name, b.total
FROM big_orders b
JOIN customers c ON c.cust_id = b.cust_id;
```

A **CTE** names an intermediate result set. It reads like a query, can be referenced more than
once, and in MySQL 8.0+ can even recurse (`WITH RECURSIVE`).

### 12. Functions vs procedures vs triggers

| | Function | Procedure | Trigger |
|---|---|---|---|
| Returns a value | ✅ exactly one | Optional `OUT` params | ❌ |
| Used in an expression | ✅ | ❌ | ❌ |
| Modifies data | ❌ (MySQL/Postgres) | ✅ | ✅ |
| Called automatically | ❌ | ❌ | ✅ |
| Called from | `SELECT` expression | Application call | The DBMS, on an event |

## Worked example

**Q. Given the `orders` table (6 rows, `cust_id` values 101, 101, 102, 103, 104, 104), what does
`SELECT COUNT(*), COUNT(DISTINCT cust_id), COUNT(cust_id) FROM orders;` return?**

- A. `6, 5, 6`
- B. `5, 5, 5`
- C. `6, 4, 6`
- D. `6, 6, 6`

**Solution**

| Expression | What it does | Result |
|---|---|---|
| `COUNT(*)` | Counts **rows**. All 6 rows exist and none is NULL-padded | **6** |
| `COUNT(DISTINCT cust_id)` | Distinct customers in the orders: 101, 102, 103, 104 → 4 | **4** |
| `COUNT(cust_id)` | Counts non-NULL `cust_id` values — all 6 are non-NULL | **6** |

**Answer: C (`6, 4, 6`).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | `COUNT(DISTINCT cust_id)` is **4**, not 5. The fifth customer (105, Vikram) placed no order, so he is not in the `orders` table at all |
| B | `COUNT(*)` counts rows, not distinct customers. It is 6, and Vikram's absence does not reduce it |
| D | `COUNT(DISTINCT cust_id)` is 4, not 6. There are only 4 distinct customers in `orders` |

**Note:** `COUNT(*)` = 6 and `COUNT(cust_id)` = 6 agree here because no `cust_id` is NULL in
`orders`. Add a row with a `NULL` `cust_id` and they diverge: `COUNT(*)` = 7, `COUNT(cust_id)` = 6.
That divergence is exactly what a `LEFT JOIN` question tests.

---

**Q2. What does this expression return for `order_amt = 900`?**

```sql
CASE
  WHEN order_amt >= 1000 THEN 'High'
  WHEN order_amt >= 500  THEN 'Medium'
  ELSE 'Low'
END
```

- A. `High`
- B. `Medium`
- C. `Low`
- D. `NULL`

**Solution**

`CASE` evaluates the `WHEN` conditions **in order** and takes the **first** that is true. `900 >= 1000`
is false. `900 >= 500` is true → `'Medium'`.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | `900 >= 1000` is false, so the first branch is skipped |
| C | The `ELSE` branch only runs when **no** `WHEN` matches. The second `WHEN` matched |
| D | `ELSE` supplies a value, so the result is never `NULL` here. `NULL` would only appear if the `ELSE` branch were missing and nothing matched |

## Quick rules

- **Scalar** = 1 row in, 1 row out. **Aggregate** = many rows in, 1 row out. **Window** = many in,
  many out.
- `COUNT(*)` counts rows; `COUNT(col)` counts non-NULL values; `COUNT(DISTINCT col)` counts
  distinct non-NULL values.
- No `GROUP BY` + an aggregate = **exactly one row**.
- `WHERE` filters rows, `HAVING` filters groups. Aggregates belong in `HAVING`.
- `CONCAT` returns `NULL` if any argument is `NULL`; `CONCAT_WS` skips `NULL`s.
- `ROUND` rounds, `TRUNC` truncates.
- `ROW_NUMBER` never ties. `RANK` skips after ties. `DENSE_RANK` does not skip.
- `CASE` takes the **first** matching `WHEN`; without `ELSE` the result is `NULL`.
- `COALESCE` = first non-NULL; `NULLIF(a,b)` = `NULL` when `a = b`.
- Window functions need **MySQL 8.0+**.

## Common traps

| Trap | What you get | What you should get |
|---|---|---|
| `COUNT(DISTINCT col)` counting customers not in the table | 5 in the example | 4 — Vikram has no order |
| `COUNT(*)` after a `LEFT JOIN` | Same as `COUNT(col)` | `COUNT(*)` includes the NULL-padded row |
| Aggregate filter in `WHERE` | Error or wrong result | Put it in `HAVING` |
| `CASE` without `ELSE` | A default value | `NULL` |
| `RANK` and `DENSE_RANK` treated the same | — | `RANK` skips, `DENSE_RANK` does not |
| `ROUND` and `TRUNC` treated the same | — | `ROUND(2.5)` = 3, `TRUNC(2.5)` = 2 |
| `CONCAT` with a NULL argument | `'Ananya'` | `NULL` |
| `AVG` dividing by `COUNT(*)` | Wrong average | Divide by the non-NULL count |
| Window function assumed to collapse rows | Fewer output rows | Same number of rows as the input |

## Checklist

- [ ] I can sort a function into scalar / aggregate / window / conditional.
- [ ] I know the difference between `COUNT(*)`, `COUNT(col)` and `COUNT(DISTINCT col)`.
- [ ] I know an aggregate without `GROUP BY` returns one row.
- [ ] I know `WHERE` vs `HAVING` and why the aggregate goes in `HAVING`.
- [ ] I can write a `CASE` with `ELSE` and predict its result.
- [ ] I know `CONCAT` vs `CONCAT_WS` and `COALESCE` vs `NULLIF`.
- [ ] I can write a `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)` query.
- [ ] I know the MySQL 8.0+ requirement for window functions.

## Related

- [Function selection procedures](../02-techniques/01-function-selection-procedures.md)
- [Solved functions and aggregates set](../03-worked-examples/01-solved-functions-aggregates-set.md)
- [Functions and aggregates traps](../04-pitfalls/01-functions-aggregates-traps.md)
- [Functions and aggregates quick check](../05-reference/01-functions-aggregates-quick-check.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
