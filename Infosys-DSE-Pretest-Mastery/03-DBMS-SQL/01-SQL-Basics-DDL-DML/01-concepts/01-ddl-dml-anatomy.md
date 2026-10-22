# DDL, DML and SQL Anatomy — The Rules

> Section 3 · DBMS & SQL · SQL Basics, DDL & DML · _Estimated reading time: 8 min_
> **Prerequisite:** [SQL basics cheat sheet](../05-reference/01-sql-basics-cheat-sheet.md)

## In one sentence

**Every SQL statement belongs to one of five families, and the family decides what it touches** —
DDL changes structure, DML changes rows, TCL controls transactions, DCL controls permissions.

## Why the pre-test tests this

- "Which SQL command does X?" is a recurring option-based question, and the options are all real SQL
  verbs — so you need the *difference*, not the syntax.
- `DELETE` / `TRUNCATE` / `DROP` and `UPDATE` / `DELETE` / `INSERT` are the two highest-yield
  comparison sets in this topic.
- A single "which statement is wrong?" question can test `NULL` handling, constraints and
  identifiers at the same time.

## Core concept

### 1. The five statement families

| Family | Full name | What it does | Statements | Auto-commit? |
|---|---|---|---|---|
| **DDL** | Data Definition Language | Changes the **structure** | `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME`, `COMMENT` | Yes (MySQL) |
| **DML** | Data Manipulation Language | Changes the **rows** | `INSERT`, `UPDATE`, `DELETE`, `MERGE` | No — you must `COMMIT` |
| **DQL** | Data Query Language | Reads rows | `SELECT` | n/a |
| **TCL** | Transaction Control Language | Controls transactions | `COMMIT`, `ROLLBACK`, `SAVEPOINT`, `SET TRANSACTION` | — |
| **DCL** | Data Control Language | Controls permissions | `GRANT`, `REVOKE` | Yes |

Two boundaries the exam loves:

- **`TRUNCATE` is DDL in the textbook classification** (it is a DDL-like statement in MySQL; MySQL
  classifies it under DDL). It empties the table and resets the auto-increment counter.
- **`SELECT` is DQL**, and the question "which is DML?" must not be answered `SELECT`.

### 2. `CREATE TABLE` — the anatomy

```sql
CREATE TABLE orders (
  order_id   INT           NOT NULL AUTO_INCREMENT,
  cust_id    INT           NOT NULL,
  order_date DATE,
  amount     DECIMAL(10,2) DEFAULT 0.00,
  status     VARCHAR(20)   DEFAULT 'NEW',
  CONSTRAINT pk_orders PRIMARY KEY (order_id),
  CONSTRAINT fk_orders_cust FOREIGN KEY (cust_id) REFERENCES customers(cust_id)
);
```

| Element | Meaning | Exam-relevant detail |
|---|---|---|
| `NOT NULL` | Column cannot be empty | A `NULL` in a `NOT NULL` column is rejected |
| `AUTO_INCREMENT` | DBMS generates the next value | 1, 2, 3… by default; `TRUNCATE` resets it |
| `DEFAULT x` | Value used when the column is omitted from `INSERT` | Different from `NULL` |
| `PRIMARY KEY` | Uniquely identifies each row | Implies `NOT NULL` + unique + indexed |
| `FOREIGN KEY` | Links to another table's key | Enforces referential integrity |
| `CHECK` | Row-level rule | e.g. `CHECK (amount >= 0)` |
| `UNIQUE` | No two rows share the value | Can be NULL in most engines (multiple NULLs allowed) |

### 3. Data types you must recognise

| Category | Types | Notes |
|---|---|---|
| Exact numeric | `INT`/`INTEGER`, `SMALLINT`, `BIGINT`, `DECIMAL(p,s)`, `NUMERIC` | `DECIMAL(10,2)` = max 10 digits, 2 after the point → up to 99,999,999.99 |
| Approximate numeric | `FLOAT`, `REAL`, `DOUBLE` | Rounding errors; never use for money |
| Character | `CHAR(n)`, `VARCHAR(n)`, `TEXT` | `CHAR` pads with spaces to `n`; `VARCHAR` does not |
| Date/time | `DATE`, `TIME`, `DATETIME`, `TIMESTAMP` | `DATE` = `YYYY-MM-DD` |
| Boolean | `BOOLEAN` (= `TINYINT(1)` in MySQL) | Stores 0/1, not TRUE/FALSE text |
| Other | `BLOB`, `JSON`, `ENUM`, `SET` | Engine-specific |

`CHAR` vs `VARCHAR` is a real question: `CHAR(10)` always stores 10 characters, padding with spaces;
`VARCHAR(10)` stores up to 10 and does not pad. Trailing-space comparison differences are the reason
the exam mentions it.

### 4. `INSERT`, `UPDATE`, `DELETE`

```sql
-- INSERT one row
INSERT INTO customers (cust_id, cust_name, city) VALUES (106, 'Sneha', 'Pune');

-- INSERT from another table (standard SQL)
INSERT INTO customers (cust_id, cust_name, city)
SELECT 200, s.name, 'Pune' FROM students s;

-- UPDATE with a filter
UPDATE customers SET city = 'Mumbai' WHERE cust_id = 101;

-- UPDATE every row
UPDATE customers SET city = 'Mumbai';

-- DELETE with a filter
DELETE FROM orders WHERE order_id = 1006;

-- DELETE every row
DELETE FROM orders;
```

- `UPDATE` and `DELETE` **without `WHERE` affect every row**. This is the single most common trap in
  the archetype.
- `UPDATE` and `DELETE` are **DML**: they can be rolled back (inside a transaction) until committed.
- `INSERT INTO t VALUES (...)` without a column list depends on the physical column order — the exam
  prefers the explicit form.

### 5. `ALTER` vs `DROP` vs `TRUNCATE` vs `DELETE`

| | `DELETE FROM t` | `TRUNCATE TABLE t` | `DROP TABLE t` |
|---|---|---|---|
| Removes rows | Yes | Yes | Yes (all data) |
| Removes structure | No | No | **Yes** |
| Can have `WHERE` | **Yes** | No | No |
| Rollback | **Yes** (DML) | Usually **No** (DDL, MySQL) | No (DDL) |
| Resets `AUTO_INCREMENT` | No | **Yes** | Yes |
| Fires row triggers | Yes | No | No |
| Logs every row | Yes | No (faster) | No |
| Table still usable | Yes | Yes | **No** |
| DDL/DML class | DML | DDL | DDL |

**The one-sentence version:** `DELETE` = remove *some rows*; `TRUNCATE` = empty the table *quickly*;
`DROP` = delete the *table*.

### 6. `ALTER TABLE` — what it can do

| Operation | Syntax | Note |
|---|---|---|
| Add a column | `ALTER TABLE t ADD COLUMN c INT;` | Existing rows get `NULL` unless a `DEFAULT` is given |
| Drop a column | `ALTER TABLE t DROP COLUMN c;` | Data in that column is gone |
| Change a column type | `ALTER TABLE t MODIFY COLUMN c DECIMAL(10,2);` (MySQL) / `ALTER COLUMN` (standard) | May fail if existing data does not fit |
| Add a constraint | `ALTER TABLE t ADD CONSTRAINT pk_t PRIMARY KEY (id);` | |
| Drop a constraint | `ALTER TABLE t DROP CONSTRAINT pk_t;` | MySQL: `DROP FOREIGN KEY fk_name;` |
| Rename a table | `ALTER TABLE t RENAME TO t2;` (MySQL) / `RENAME TO` (standard) | |
| Rename a column | `ALTER TABLE t RENAME COLUMN a TO b;` (MySQL 8+) / `RENAME COLUMN` (standard) | |

`ALTER TABLE` **cannot** change the primary key to a column that has duplicate or NULL values. It
also cannot rename a column in older MySQL versions — the exam says "MySQL 8+" when it matters.

### 7. NULL semantics — the part that loses marks

`NULL` means **unknown / missing**. It is not `0`, not `''`, and not `FALSE`.

| Expression | Result | Why |
|---|---|---|
| `NULL = NULL` | `UNKNOWN` | You cannot know that two unknowns are equal |
| `NULL <> NULL` | `UNKNOWN` | Same reason |
| `NULL > 5` | `UNKNOWN` | Cannot order a missing value |
| `10 + NULL` | `NULL` | Arithmetic with unknown is unknown |
| `NULL IS NULL` | `TRUE` | The only way to test for missing |
| `NULL IS NOT NULL` | `TRUE` for non-null rows | |
| `COUNT(col)` | Ignores NULLs | Counts non-null values only |
| `COUNT(*)` | Counts **all rows** | `*` is not a column |
| `SUM(col)` | Ignores NULLs | If all values are NULL, `SUM` returns `NULL` |
| `AVG(col)` | Ignores NULLs | Denominator = count of **non-null** values only |
| `MAX(col)` | Ignores NULLs | |
| `ORDER BY col ASC` | NULLs first (MySQL) | NULLs last in PostgreSQL/Oracle |
| `GROUP BY col` | NULLs form **one** group | NULL ≠ NULL, but `GROUP BY` treats them as equal |
| `DISTINCT` | NULL counted once | One NULL in the output |

**Never write `WHERE col = NULL`.** Write `WHERE col IS NULL` or `WHERE col IS NOT NULL`.

### 8. `NULL` and `NOT IN` — the classic killer

```sql
-- Suppose the subquery returns {10, 20, NULL}
SELECT cust_name FROM customers WHERE cust_id NOT IN (10, 20, NULL);
```

Result: **zero rows**. SQL rewrites it as `cust_id <> 10 AND cust_id <> 20 AND cust_id <> NULL`.
The last comparison is `UNKNOWN`, and `TRUE AND UNKNOWN` is `UNKNOWN`, so no row qualifies. This is
the trap the exam uses to punish `NOT IN` with subqueries.

`NOT EXISTS` is NULL-safe and returns the correct rows.

### 9. `WHERE` vs `HAVING` — the boundary

| | `WHERE` | `HAVING` |
|---|---|---|
| Operates on | Individual **rows** | **Groups** of rows |
| Runs | Before `GROUP BY` | After `GROUP BY` |
| Can use aggregates | **No** | Yes |
| Can use column aliases | No | Yes (MySQL allows in `HAVING`) |
| Applied to | Every row of the source | Only to groups that exist |
| With `DISTINCT` | Filters before dedup | — |

```sql
-- Correct: filter rows, then group, then filter groups
SELECT city, COUNT(*) AS orders
FROM customers c JOIN orders o ON c.cust_id = o.cust_id
WHERE o.amount > 400
GROUP BY city
HAVING COUNT(*) >= 2;
```

`WHERE o.amount > 400` cannot be replaced by `HAVING SUM(o.amount) > 400` — that changes the
meaning from "count orders over 400" to "sum of all orders per city over 400". Different question,
different answer.

### 10. Subquery types

| Type | Form | Returns | NULL-safe? |
|---|---|---|---|
| **Scalar** | `WHERE salary = (SELECT MAX(salary) FROM employees)` | One value | One row, one column |
| **IN** | `WHERE cust_id IN (SELECT cust_id FROM orders)` | A set | **No** if the set contains NULL |
| **EXISTS` | `WHERE EXISTS (SELECT 1 FROM orders o WHERE o.cust_id = c.cust_id)` | True/False | **Yes** |
| **Correlated** | Inner `SELECT` refers to the outer row | Per outer row | — |

`EXISTS` stops at the first matching row — it answers "does at least one match exist?", not "how
many match?". `IN` compares a value against the whole set.

### 11. Set operations

| Operation | Keeps | Duplicates | Notes |
|---|---|---|---|
| `UNION` | Rows in both | **Removes** duplicates | Result is sorted; costs a sort |
| `UNION ALL` | Rows in both | **Keeps** duplicates | Faster |
| `INTERSECT` | Rows in both | Removes duplicates | Not supported by MySQL (use `IN`/`EXISTS`) |
| `EXCEPT` | Rows in first but not second | Removes duplicates | Not supported by MySQL (use `NOT IN`/`NOT EXISTS`) |

Column rules: every `SELECT` in a set operation must have the **same number of columns**, and the
data types must be compatible. Column names come from the **first** `SELECT`.

```sql
-- Same rows, different counts: UNION dedups, UNION ALL does not
SELECT city FROM customers WHERE cust_id IN (101, 103)   -- Pune, Pune
UNION ALL
SELECT city FROM customers WHERE cust_id IN (101, 104)   -- Pune, Delhi
-- UNION ALL      → Pune, Pune, Pune, Delhi  (4 rows)
-- UNION         → Pune, Delhi                (2 rows)
```

### 12. `LIKE` patterns

| Pattern | Matches | Example |
|---|---|---|
| `%` | Zero or more characters | `'A%'` → Ananya, Anjali |
| `_` | Exactly one character | `'_nanya'` → Ananya |
| `LIKE 'A%'` | Starts with A | |
| `LIKE '%a'` | Ends with a | |
| `LIKE '%an%'` | Contains an | |
| `LIKE 'a_'` | 'a' + one char | |

MySQL default collation is case-insensitive, so `LIKE 'a%'` also matches `Ananya`. Standard SQL
`LIKE` is case-sensitive; `ILIKE` (PostgreSQL) is the case-insensitive variant. The exam usually
ignores case.

### 13. `IN` vs `BETWEEN` vs `LIKE` vs `EXISTS`

| Need | Use | Example |
|---|---|---|
| Match a set of known values | `IN` | `city IN ('Pune','Delhi')` |
| Match a contiguous range | `BETWEEN` | `amount BETWEEN 300 AND 1000` |
| Match a pattern | `LIKE` | `cust_name LIKE 'A%'` |
| Test existence of matching rows | `EXISTS` | `WHERE EXISTS (SELECT 1 ...)` |

`BETWEEN` is **inclusive** on both ends. `NOT BETWEEN` includes values outside the range.

### 14. `ORDER BY` and `LIMIT`

```sql
SELECT cust_name, city
FROM customers
ORDER BY city DESC, cust_name ASC     -- multiple keys, each with its own direction
LIMIT 10;                              -- MySQL / PostgreSQL / SQLite

SELECT cust_name
FROM customers
ORDER BY cust_name
LIMIT 10 OFFSET 20;                   -- rows 21–30
```

- `ORDER BY 2` sorts by the second selected column (ordinal). Legal in MySQL and PostgreSQL; not
  portable to Oracle.
- `ORDER BY` on a column not in the `SELECT` list is fine in standard SQL.
- `LIMIT` without `ORDER BY` returns an **arbitrary** 10 rows. If a question asks "the top 3
  customers" you need `ORDER BY` first, and ties make the answer non-deterministic unless you add a
  tiebreaker.
- `TOP n` is the T-SQL / SQL Server spelling; `ROWNUM` is Oracle's (and behaves differently).

## Worked example

**Q. Which statement removes all rows from the `orders` table, keeps the table structure, resets the
`AUTO_INCREMENT` counter, and cannot be rolled back?**

- A. `DELETE FROM orders;`
- B. `TRUNCATE TABLE orders;`
- C. `DROP TABLE orders;`
- D. `DROP DATABASE orders;`

**Solution**

| Requirement | Statement that satisfies it |
|---|---|
| Removes all rows | `DELETE` / `TRUNCATE` / `DROP` all do |
| Keeps the table | `TRUNCATE` only (`DROP` destroys it) |
| Resets `AUTO_INCREMENT` | `TRUNCATE` only |
| Cannot be rolled back | `TRUNCATE` (DDL) — `DELETE` is DML and can be |

**Answer: B (`TRUNCATE TABLE orders;`).**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| A `DELETE FROM orders;` | Keeps the structure and the identity counter, and **can** be rolled back inside a transaction |
| C `DROP TABLE orders;` | Destroys the structure — the table no longer exists |
| D `DROP DATABASE orders;` | Destroys the whole database, not one table; and `orders` is a table name, not a database name |

**Faster route:** the answer is the only one of the four that keeps the table. Find the
*requirement that discriminates*, not the closest definition.

## Quick rules

- **Verb first**: structure → DDL; rows → DML; reading → DQL; transaction control → TCL;
  permissions → DCL.
- `DELETE` = rows (with `WHERE`, rollbackable); `TRUNCATE` = empty table fast, resets identity;
  `DROP` = delete the table.
- `UPDATE`/`DELETE` without `WHERE` = **every row**.
- `NULL = NULL` is `UNKNOWN`. Use `IS NULL` / `IS NOT NULL`. Never `= NULL`.
- `COUNT(*)` counts rows; `COUNT(col)` counts non-null values.
- `WHERE` filters rows before grouping; `HAVING` filters groups after grouping.
- `NOT IN` + a NULL in the subquery = zero rows. Use `NOT EXISTS`.
- `UNION` removes duplicates; `UNION ALL` keeps them and is faster.
- `BETWEEN` is inclusive; `LIKE` uses `%` and `_`; `IN` takes an explicit list.

## Common traps

| Trap | Wrong answer you would pick | Correct |
|---|---|---|
| "Delete the table" → `DELETE` | `DELETE FROM t;` | `DROP TABLE t;` |
| "Remove all rows" → `DROP` | `DROP TABLE t;` | `TRUNCATE TABLE t;` |
| `WHERE col = NULL` | Rows where the value is 0 | Nothing matches |
| `COUNT(*)` vs `COUNT(col)` | Counting NULLs | `COUNT(*)` counts all rows |
| `NOT IN` with NULL in list | Correct complement rows | **Zero rows** |
| `WHERE` with an aggregate | `WHERE COUNT(*) > 1` | `HAVING COUNT(*) > 1` |
| `UNION` vs `UNION ALL` on duplicates | 4 rows | `UNION` gives 2 |
| `BETWEEN` exclusive | Excludes the boundary | Inclusive on both ends |
| `SELECT` is DML | Picking `SELECT` | `SELECT` is DQL |

## Checklist

- [ ] I can name the family (DDL/DML/DQL/TCL/DCL) of any SQL verb on sight.
- [ ] I know the four differences between `DELETE`, `TRUNCATE` and `DROP`.
- [ ] I never write `= NULL`; I use `IS NULL`.
- [ ] I checked whether the question is about rows or about groups before choosing `WHERE`/`HAVING`.
- [ ] I used `NOT EXISTS` instead of `NOT IN` when a subquery might return NULLs.
- [ ] I know whether `UNION` or `UNION ALL` was asked for.
- [ ] I checked that my `ORDER BY` exists before trusting a `LIMIT` result.

## Related

- [SELECT, filter, sort and subqueries](../01-concepts/02-select-filter-sort-and-subqueries.md)
- [Statement decision procedures](../02-techniques/01-statement-decision-procedures.md)
- [Solved SQL basics set](../03-worked-examples/01-solved-sql-basics-set.md)
- [SQL basics traps](../04-pitfalls/01-sql-basics-traps.md)
- [SQL basics cheat sheet](../05-reference/01-sql-basics-cheat-sheet.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
