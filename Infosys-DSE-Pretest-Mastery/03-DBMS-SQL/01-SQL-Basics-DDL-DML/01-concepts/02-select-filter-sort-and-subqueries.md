# SELECT, Filter, Sort and Subqueries — The Rules

> Section 3 · DBMS & SQL · SQL Basics, DDL & DML · _Estimated reading time: 8 min_
> **Prerequisite:** [DDL, DML and SQL anatomy](01-ddl-dml-anatomy.md)

## In one sentence

**A `SELECT` statement is a pipeline with a fixed clause order** — `FROM` → `WHERE` → `GROUP BY` →
`HAVING` → `SELECT` → `DISTINCT` → `ORDER BY` → `LIMIT` — and getting the order wrong is the same
as getting the answer wrong.

## Why the pre-test tests this

- Archetype (b) asks you to *write* a query for two tables. The grader is checking clause order and
  join keys.
- Archetype (c) asks you to *read* the output of a query. You cannot read it without knowing the
  execution order.
- "Which option is the correct query?" questions are decided by clause order and by the
  `WHERE`/`HAVING` split.

## Core concept

### 1. The canonical `SELECT` skeleton

```sql
SELECT [DISTINCT] column_list
FROM   table1
[INNER | LEFT | RIGHT | FULL OUTER] JOIN table2 ON join_condition
[WHERE row_condition]
[GROUP BY grouping_columns]
[HAVING group_condition]
[ORDER BY sort_columns [ASC|DESC]]
[LIMIT n [OFFSET m]];
```

Logical execution order — **this is the order the DBMS runs them, not the order you type them**:

```
1. FROM + JOIN       → build the working set (rows can multiply)
2. WHERE             → drop individual rows
3. GROUP BY          → collapse rows into groups
4. HAVING            → drop groups
5. SELECT            → compute the output columns
6. DISTINCT          → remove duplicate output rows
7. ORDER BY          → sort
8. LIMIT             → cut
```

Two consequences you will be asked about:

- You may use an **aggregate in `SELECT`** (step 5) because grouping already happened.
- You may **not** use an aggregate in `WHERE` (step 2) because grouping has not happened yet.
- `ORDER BY` may reference an **alias** from `SELECT` (step 7 is after step 5), but `GROUP BY` may
  **not** in standard SQL (step 3 is before step 5). MySQL is lenient; the exam uses the standard
  rule.

### 2. Column selection and aliases

```sql
SELECT cust_name                    AS customer,
       amount * 1.18               AS amount_with_gst,
       UPPER(city)                  AS city_upper
FROM   customers c
JOIN   orders o ON c.cust_id = o.cust_id;
```

| Feature | Rule |
|---|---|
| `AS` keyword | Optional but recommended; accepted for table and column aliases in MySQL/PostgreSQL |
| Table alias | `FROM customers c` then use `c.cust_name` everywhere — required once you join two tables with a same-named column |
| `*` | Selects every column of every table in the `FROM` — including duplicated join columns |
| `table.*` | `SELECT c.*` = every column of `customers` only |
| String literal | Single quotes: `'Pune'`. Double quotes are identifiers in standard SQL |
| Arithmetic | `+`, `-`, `*`, `/`; `NULL` propagates through all of them |

**Duplicate column names are the reason aliases exist.** `SELECT cust_id FROM customers c JOIN orders
o ON c.cust_id = o.cust_id` produces two `cust_id` columns and is ambiguous in every engine. Write
`SELECT c.cust_id, o.cust_id AS order_cust_id ...`.

### 3. `DISTINCT`

```sql
SELECT DISTINCT city FROM customers;
```

- Removes **duplicate rows** from the output, not duplicate values inside a row.
- Applies to the **whole selected row**, not to one column. `SELECT DISTINCT city, cust_name` only
  removes rows where *both* are identical.
- Costs a sort/hash — it is not free.
- `NULL` counts as one distinct value: `DISTINCT` over `{Pune, NULL, Pune}` gives 2 rows.
- `DISTINCT` + `ORDER BY`: in MySQL, the `ORDER BY` column must appear in the `SELECT` list.

### 4. `ORDER BY`

```sql
SELECT cust_name, amount
FROM   orders
ORDER BY amount DESC, cust_name ASC;
```

- **Multiple keys** are applied left to right; each key gets its own direction.
- **Default direction is ASC** (ascending).
- `NULL` placement: MySQL puts NULLs **first** on `ASC` and **last** on `DESC`. PostgreSQL and
  Oracle put NULLs **last** on `ASC` and **first** on `DESC`.
- `ORDER BY 2` = order by the second column in the `SELECT` list (MySQL/PostgreSQL).
- `ORDER BY` is **not guaranteed** without it. If a question asks "the top 3 by amount", the query
  needs `ORDER BY amount DESC LIMIT 3`.
- **Ties make `LIMIT` non-deterministic.** Two customers tied at the top with `LIMIT 1` gives one of
  two rows, and the engine may return either. Add a tiebreaker: `ORDER BY amount DESC, cust_id ASC`.

### 5. `LIMIT`

| Syntax | Meaning | Engine |
|---|---|---|
| `LIMIT n` | First `n` rows | MySQL, PostgreSQL, SQLite |
| `LIMIT m, n` | `n` rows starting at row `m+1` | MySQL only |
| `LIMIT n OFFSET m` | Skip `m`, then take `n` | MySQL, PostgreSQL |
| `OFFSET m ROWS FETCH NEXT n ROWS ONLY` | Standard SQL | SQL:2008+, PostgreSQL, Oracle 12c+ |
| `TOP n` | First `n` rows | SQL Server / T-SQL |

Always pair `LIMIT` with `ORDER BY`. `LIMIT 3` alone has **no defined order**.

### 6. `WHERE` — the row filter

| Operator | Meaning | Example |
|---|---|---|
| `=`, `<>`, `<`, `>`, `<=`, `>=` | Comparison | `amount >= 500` |
| `AND`, `OR`, `NOT` | Logic | `city = 'Pune' AND amount > 500` |
| `BETWEEN a AND b` | Inclusive range | `amount BETWEEN 300 AND 1000` |
| `IN (list)` | Membership | `city IN ('Pune','Delhi')` |
| `LIKE 'pat'` | Pattern | `cust_name LIKE 'A%'` |
| `IS NULL`, `IS NOT NULL` | Null test | `manager_id IS NULL` |
| `EXISTS (subquery)` | Existence test | see below |

`AND` binds tighter than `OR`. `WHERE a = 1 OR b = 2 AND c = 3` means
`a = 1 OR (b = 2 AND c = 3)`. **Always bracket when in doubt.**

### 7. `HAVING` — the group filter

```sql
SELECT cust_id, COUNT(*) AS order_count
FROM   orders
GROUP BY cust_id
HAVING COUNT(*) > 1;
```

- `HAVING` can reference aggregates and column aliases.
- `HAVING` without `GROUP BY` treats the whole table as one group (valid in MySQL; in standard SQL
  the result has one row).
- `WHERE` and `HAVING` can both appear; `WHERE` runs first and reduces the rows that are grouped.

### 8. `GROUP BY` rules

- Every non-aggregated column in `SELECT` must appear in `GROUP BY` (standard SQL). MySQL's
  "ONLY_FULL_GROUP_BY" mode enforces it and is the default since MySQL 5.7.
- `GROUP BY` treats NULLs as **one group** (unlike `WHERE` where `NULL = NULL` is unknown).
- `GROUP BY` on two columns groups by the **combination**.
- `GROUP BY` does not guarantee output order. Add `ORDER BY`.

### 9. Subqueries

```sql
-- Scalar: returns one value
SELECT cust_name FROM customers
WHERE cust_id = (SELECT MAX(cust_id) FROM orders);

-- IN: membership in a set
SELECT cust_name FROM customers
WHERE cust_id IN (SELECT cust_id FROM orders WHERE amount > 1000);

-- EXISTS: does a matching row exist?
SELECT c.cust_name
FROM   customers c
WHERE  EXISTS (SELECT 1 FROM orders o WHERE o.cust_id = c.cust_id);

-- NOT EXISTS: NULL-safe complement
SELECT c.cust_name
FROM   customers c
WHERE  NOT EXISTS (SELECT 1 FROM orders o WHERE o.cust_id = c.cust_id);
```

| Question | Use | Why |
|---|---|---|
| "the maximum / average / name" | Scalar subquery | One value |
| "customers who placed an order" | `EXISTS` | Fast, NULL-safe, stops at first hit |
| "customers who placed an order" | `IN` | Fine, but breaks on NULL |
| "customers who placed **no** order" | `NOT EXISTS` | `NOT IN` returns nothing if the list has NULL |

Correlated subquery: the inner `SELECT` references the outer row, so it runs **once per outer row**.
That is why `EXISTS` with a correlated condition is usually cheap (it short-circuits) and why a
correlated `IN` can be slow.

### 10. `UNION` / `UNION ALL` / `INTERSECT` / `EXCEPT` — set semantics

```sql
SELECT city FROM customers WHERE cust_id IN (101,103)   -- Pune, Pune
UNION ALL
SELECT city FROM customers WHERE cust_id IN (101,104)   -- Pune, Delhi
```

| Operation | Duplicates | Sort needed? | MySQL? |
|---|---|---|---|
| `UNION` | Removed | Yes (implicit) | Yes |
| `UNION ALL` | Kept | No | Yes |
| `INTERSECT` | Removed | Yes | **No** (MySQL 8.0.31+ only) |
| `EXCEPT` | Removed | Yes | **No** (MySQL 8.0.31+ only) |

MySQL note: use `IN` / `EXISTS` instead of `INTERSECT` / `EXCEPT` unless you are on 8.0.31+.

### 11. `LIKE` and pattern matching

| Pattern | Matches | Example result |
|---|---|---|
| `'A%'` | starts with A | Ananya, Anjali |
| `'%a'` | ends with a | Meera, Ananya, Anjali |
| `'%an%'` | contains "an" | Ananya, Vikram? no → Ananya only |
| `'A_anya'` | exactly one char in the `_` slot | Ananya |
| `'%a_ya'` | fixed-width ends | Ananya, Meera? no → Ananya |

`%` = zero or more characters. `_` = exactly one character. `ESCAPE` changes the escape char if you
need to match a literal `%`.

### 12. Comments

```sql
-- single-line comment (SQL standard and MySQL)
# single-line comment (MySQL only)
/* multi-line
   comment */
```

The exam sometimes shows a statement with a `--` comment and asks whether it is valid. `--` is the
portable form. MySQL additionally accepts `#`.

### 13. Identifier rules

| Rule | Detail |
|---|---|
| Length | Up to 63 characters in PostgreSQL, 64 in MySQL |
| Start | A letter, or `_` (MySQL allows `$`) |
| Continue | Letters, digits, `_`, `$` |
| Case | Unquoted identifiers are case-insensitive in SQL; **table names are case-sensitive on Linux** in MySQL |
| Reserved words | Quote them: `` `order` `` (MySQL), `"order"` (standard SQL) |
| Schema qualifier | `schema.table.column` |

`order` is a reserved word. `SELECT * FROM order;` is a syntax error; `SELECT * FROM \`order\`;` works
in MySQL.

## Worked example

**Q. Given the `orders` table, which query returns the number of orders per customer, keeping only
customers with more than one order, sorted by the count descending, showing at most 2 customers?**

- A.
  ```sql
  SELECT cust_id, COUNT(*) FROM orders
  GROUP BY cust_id HAVING COUNT(*) > 1
  ORDER BY COUNT(*) DESC LIMIT 2;
  ```
- B.
  ```sql
  SELECT cust_id, COUNT(*) FROM orders
  WHERE COUNT(*) > 1
  GROUP BY cust_id
  ORDER BY COUNT(*) DESC LIMIT 2;
  ```
- C.
  ```sql
  SELECT cust_id, COUNT(*) FROM orders
  GROUP BY cust_id HAVING COUNT(*) > 1
  ORDER BY COUNT(*) DESC LIMIT 2;
  ```
- D.
  ```sql
  SELECT cust_id, COUNT(order_id) FROM orders
  GROUP BY cust_id HAVING COUNT(order_id) > 1
  ORDER BY COUNT(order_id) DESC LIMIT 2;
  ```

**Solution**

| Option | Verdict | Reason |
|---|---|---|
| A | Valid SQL | Missing `AS` alias is fine; but `COUNT(*)` vs `COUNT(order_id)` matters — see below |
| B | **Error** | `WHERE` cannot contain an aggregate: grouping has not happened yet |
| C | **Correct** | Clauses in the right order, aggregate only in `HAVING`/`SELECT`/`ORDER BY` |
| D | Correct on this data, different in general | `COUNT(order_id)` skips NULL `order_id`s; `order_id` is the PRIMARY KEY so it is never NULL — same result here |

The exam accepts C as the intended answer: it is the option that is valid **and** uses the standard
`COUNT(*)`.

**Answer: C.**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| A | Not wrong, but it reads as incomplete — no alias for the count column. The exam wants a labelled output column. If the question asks "which is the *best* form", A loses on style; if it asks "which is *valid*", A is also valid. In a single-answer MCQ, the exam will not write two identical-valid options; treat A as "missing the output alias" |
| B | `WHERE COUNT(*) > 1` is invalid in every standard engine — the aggregate is evaluated after grouping, and `WHERE` is applied before |
| D | Valid but fragile: if `order_id` were nullable, `COUNT(order_id)` would undercount. `COUNT(*)` counts rows unconditionally |

**Note on the data:** customers 101 and 104 each have 2 orders, so the output is two rows, count 2
each, order between them unspecified unless a tiebreaker is added. A question that expects a
deterministic order must include one.

## Quick rules

- Clause order: `FROM/JOIN` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `DISTINCT` → `ORDER BY` →
  `LIMIT`.
- `WHERE` filters rows, `HAVING` filters groups. Aggregates belong in `HAVING`.
- Every non-aggregated `SELECT` column must be in `GROUP BY`.
- `DISTINCT` applies to the whole selected row, not one column.
- `ORDER BY` must exist before `LIMIT`; add a tiebreaker when values tie.
- `NULL` sorts first ascending in MySQL, last in PostgreSQL/Oracle.
- `EXISTS` is NULL-safe; `NOT IN` is not. Use `NOT EXISTS`.
- `UNION` dedups, `UNION ALL` does not; `INTERSECT`/`EXCEPT` are not in MySQL < 8.0.31.
- Always alias tables when you join — `c.cust_id`, `o.cust_id`.
- `BETWEEN` includes both ends; `LIKE` uses `%` and `_`; `IN` takes an explicit list.

## Common traps

| Trap | What you get | What you should get |
|---|---|---|
| Aggregate in `WHERE` | Query error | Aggregate in `HAVING` |
| `WHERE` after `GROUP BY` | Query error | `WHERE` first, `GROUP BY` after |
| `LIMIT` without `ORDER BY` | Arbitrary rows | Add `ORDER BY` |
| `COUNT(col)` on a nullable column | Undercount | `COUNT(*)` to count rows |
| `DISTINCT city, cust_name` | Only exact row duplicates removed | — |
| `NOT IN` with a NULL-producing subquery | Zero rows | `NOT EXISTS` |
| `AND`/`OR` without brackets | Wrong filter set | `WHERE (a OR b) AND c` |
| `SELECT *` on a join | Duplicate key columns | Select named columns |
| `=` NULL | Never matches | `IS NULL` |
| `ORDER BY` an alias in `GROUP BY` | Non-portable | Use real column names in `GROUP BY` |

## Checklist

- [ ] I can write the execution order of a `SELECT` from memory.
- [ ] I checked that every aggregate in my query is in `SELECT`/`HAVING`/`ORDER BY`, never in `WHERE`.
- [ ] I added `ORDER BY` before every `LIMIT`.
- [ ] I added a tiebreaker where the sort key can tie.
- [ ] I chose `EXISTS`/`NOT EXISTS` over `IN`/`NOT IN` for subqueries.
- [ ] I aliased every table in a join.
- [ ] I used `IS NULL`, never `= NULL`.

## Related

- [DDL, DML and SQL anatomy](01-ddl-dml-anatomy.md)
- [Statement decision procedures](../02-techniques/01-statement-decision-procedures.md)
- [Solved SQL basics set](../03-worked-examples/01-solved-sql-basics-set.md)
- [SQL basics traps](../04-pitfalls/01-sql-basics-traps.md)
- [SQL basics cheat sheet](../05-reference/01-sql-basics-cheat-sheet.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
