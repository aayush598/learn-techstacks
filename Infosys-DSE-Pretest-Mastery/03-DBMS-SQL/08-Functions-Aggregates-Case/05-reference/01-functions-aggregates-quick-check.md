# Functions and Aggregates Quick Check — One Page

> Section 3 · DBMS & SQL · Functions, Aggregates & CASE · _Estimated reading time: 3 min_
> **Prerequisite:** [Function selection procedures](../02-techniques/01-function-selection-procedures.md)

## In one sentence

Verb → function, the three `COUNT`s, the `CASE` rule, the ranking trio, and the fixture numbers.

## Why the pre-test tests this

- The most frequent archetype in the section. Three minutes of revision closes it.
- Every wrong option in a function question is a **real function in the wrong place**.

## Core concept

### The four families

| Family | In → out | Key point |
|---|---|---|
| Scalar | 1 → 1 | Transforms one row |
| Aggregate | N → 1 | **Collapses** the rows |
| Window | N → N | Computes across a set, **never collapses** |
| Conditional | 1 → 1 | `CASE`, `COALESCE`, `NULLIF`, `IFNULL`, `IIF` |

### Verb → function

| Verb | Function |
|---|---|
| Count rows | `COUNT(*)` |
| Count non-NULL | `COUNT(col)` |
| Count different | `COUNT(DISTINCT col)` |
| Total | `SUM(col)` |
| Average | `AVG(col)` |
| Highest / lowest | `MAX` / `MIN` |
| Strip leading spaces | `LTRIM(s)` |
| Strip trailing spaces | `RTRIM(s)` |
| Strip both ends | `TRIM(s)` |
| Upper / lower | `UPPER` / `LOWER` |
| Character count | `LENGTH(s)` / `CHAR_LENGTH(s)` |
| Substring | `SUBSTRING(s, start, len)` / `LEFT` / `RIGHT` |
| Join strings | `CONCAT(a, b)` |
| Join with separator | `CONCAT_WS(sep, a, b)` |
| Replace text | `REPLACE(s, from, to)` |
| Pad | `LPAD(s, n, pad)` / `RPAD` |
| Find position | `LOCATE(sub, s)` / `POSITION` / `INSTR` |
| First non-NULL | `COALESCE(a, b, ...)` |
| NULL if equal | `NULLIF(a, b)` |
| Round | `ROUND(x, n)` |
| Truncate | `TRUNC(x, n)` |
| Round up / down | `CEIL(x)` / `FLOOR(x)` |
| Remainder | `MOD(a, b)` |

### Numeric functions on 2.7

| `ROUND` | `TRUNC` | `CEIL` | `FLOOR` |
|---|---|---|---|
| 3 | 2 | 3 | 2 |

### Aggregates

| Function | NULLs | Returns |
|---|---|---|
| `COUNT(*)` | Counts them | Rows |
| `COUNT(col)` | Skips | Non-NULL count |
| `COUNT(DISTINCT col)` | Skips | Distinct non-NULL count |
| `SUM(col)` | Skips | Total |
| `AVG(col)` | Skips | Mean of the **non-NULL** values |
| `MIN/MAX(col)` | Skips | Extreme value |

**Rules:** no `GROUP BY` + aggregate = **1 row**. Aggregate filter → **`HAVING`**. `WHERE` filters
rows before grouping.

### String aggregation

| DBMS | Function |
|---|---|
| MySQL | `GROUP_CONCAT(col SEPARATOR ', ')` |
| PostgreSQL / SQL Server | `STRING_AGG(col, ', ')` |
| Oracle | `LISTAGG(col, ', ')` |

### Window functions

```sql
func() OVER ( [PARTITION BY cols] [ORDER BY cols] [frame] )
```

| Function | Behaviour |
|---|---|
| `ROW_NUMBER()` | Consecutive, **never ties** |
| `RANK()` | Ties share a rank, **skips** (1, 2, 2, 4) |
| `DENSE_RANK()` | Ties share a rank, **no skip** (1, 2, 2, 3) |
| `NTILE(n)` | n buckets |
| `LAG(col, n)` / `LEAD(col, n)` | Previous / next row's value |
| `SUM(col) OVER (ORDER BY ...)` | Running total |

MySQL **8.0+** required.

### `CASE`

```sql
CASE [expr]
  WHEN v1 THEN r1
  WHEN v2 THEN r2
  ELSE r3
END
```

| Rule | Detail |
|---|---|
| Order | Top to bottom |
| Winner | The **first** matching `WHEN` |
| No match, with `ELSE` | The `ELSE` value |
| No match, no `ELSE` | **`NULL`** |

### NULL-handling functions

| Function | Behaviour |
|---|---|
| `COALESCE(a, b)` | First non-NULL |
| `NULLIF(a, b)` | `NULL` when `a = b` |
| `IFNULL(a, b)` | MySQL's two-arg `COALESCE` |
| `IIF(cond, a, b)` | SQL Server's two-branch `CASE` |

**`NULL` test = `IS NULL`. `= NULL` is never true.**

### Fixture numbers

| Fact | Value |
|---|---|
| `orders` rows | 6 |
| Total order value | 4800 |
| Distinct customers in `orders` | **4** |
| `GROUP BY cust_id` groups over `orders` | **4** |
| `customers` rows | 5 |
| `customers` with no order | 105 Vikram |
| `customers JOIN orders` | 6 rows |
| `customers LEFT JOIN orders` | 7 rows |

### `DISTINCT` vs `GROUP BY`

| | `DISTINCT` | `GROUP BY` |
|---|---|---|
| Removes duplicates | ✅ | ✅ |
| Aggregates | ❌ | ✅ |

## Worked example

**Q. `SELECT COUNT(*), COUNT(DISTINCT cust_id) FROM orders;` returns:**

- A. `6, 6`
- B. `6, 4`
- C. `5, 4`
- D. `6, 5`

**Answer: B.** `COUNT(*)` = 6 rows; `COUNT(DISTINCT cust_id)` = 4 (101, 102, 103, 104). Vikram
(105) has no order, so he is not counted.

## Quick rules

- Verb → function. Rows vs values vs distinct values.
- No `GROUP BY` + aggregate = 1 row.
- `HAVING` for aggregate filters.
- `IS NULL`.
- `CASE`: first match wins; no `ELSE` → `NULL`.
- `ROW_NUMBER` no ties, `RANK` skips, `DENSE_RANK` does not.
- `CONCAT` propagates NULL; `CONCAT_WS` skips it.
- `GROUP_CONCAT` is an aggregate; `CONCAT_WS` is scalar.
- MySQL 8.0+ for window functions.

## Common traps

| Trap | Fix |
|---|---|
| `COUNT(*)` for distinct values | Use `COUNT(DISTINCT col)` |
| Counting the wrong table | Count where the qualifying rows live |
| Aggregate filter in `WHERE` | Use `HAVING` |
| `= NULL` | `IS NULL` |
| `CASE` branches out of order | First match wins |
| `CONCAT_WS` for a group list | `GROUP_CONCAT` |
| `AVG` over `COUNT(*)` | Non-NULL denominator |

## Checklist

- [ ] I can map a verb to a function in 15 seconds.
- [ ] I know the fixture numbers 6, 4800, 4, 5, 7.
- [ ] I know `HAVING` vs `WHERE`.
- [ ] I can evaluate a `CASE` top to bottom.
- [ ] I know the ranking trio.
- [ ] I know `COALESCE` / `NULLIF` / `IFNULL`.
- [ ] I know the MySQL version requirement for window functions.

## Related

- [Functions, aggregates and CASE](../01-concepts/01-functions-aggregates-and-case.md)
- [Function selection procedures](../02-techniques/01-function-selection-procedures.md)
- [Solved functions and aggregates set](../03-worked-examples/01-solved-functions-aggregates-set.md)
- [Functions and aggregates traps](../04-pitfalls/01-functions-aggregates-traps.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
