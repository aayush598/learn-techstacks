# SQL Basics — 8 Solved Questions

> Section 3 · DBMS & SQL · SQL Basics, DDL & DML · _Estimated reading time: 10 min_
> **Prerequisite:** [Statement decision procedures](../02-techniques/01-statement-decision-procedures.md)

## In one sentence

Eight SQL-foundation questions, each built around one specific error — statement family, NULL
semantics, `WHERE` vs `HAVING`, `NOT IN`, set operations and `LIMIT` ties.

## Why the pre-test tests this

- This is archetype (a): "SQL fundamentals up to JOINs". The questions are quick if you know the
  differences, and slow if you try to reason from first principles.
- Every question below has a definite answer and a distractor set built from the *most likely wrong
  reading* of the stem.
- The fixture is the shared one from the [section index](../../README.md#the-shared-fixture).

## Core concept

Before each question, answer three questions in under 10 seconds:

1. **Which family?** DDL, DML, DQL, TCL or DCL.
2. **What is the discriminating requirement?** Rows, structure, rollback, identity counter, NULL
   semantics, duplicates?
3. **What is the fixture?** The shared `customers` / `orders` tables, with customer 105 having no
   orders and customers 101 and 104 having two each.

## Worked example

### Q1 — Answer **C** (statement family: DDL removes structure)

**Which SQL command removes a table along with all of its data and its definition?**

- A. `DELETE FROM orders;`
- B. `TRUNCATE TABLE orders;`
- C. `DROP TABLE orders;`
- D. `REMOVE TABLE orders;`

**Solution**

| Option | What it actually does | Removes the table? |
|---|---|---|
| A | Deletes rows; DML; rollbackable | No |
| B | Empties the table, resets identity; DDL-ish | No — the table survives |
| C | Removes the table and its definition | **Yes** |
| D | Not a SQL statement | n/a |

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Deletes data only. The table still exists and can be queried |
| B | Empties the table but keeps it. "Removes the table" is not the same as "removes the rows" |
| D | `REMOVE` is not an SQL keyword. `DELETE` and `DROP` are the two real candidates |

---

### Q2 — Answer **A** (`TRUNCATE` vs `DELETE` vs `DROP`)

**Which statement removes all rows from `orders`, keeps the table, resets the `AUTO_INCREMENT`
counter, and cannot be rolled back?**

- A. `TRUNCATE TABLE orders;`
- B. `DELETE FROM orders;`
- C. `DROP TABLE orders;`
- D. `DELETE * FROM orders;`

**Solution**

| Requirement | `DELETE` | `TRUNCATE` | `DROP` |
|---|---|---|---|
| Keeps the table | Yes | Yes | **No** |
| Resets `AUTO_INCREMENT` | No | **Yes** | Yes |
| Rollbackable | **Yes** | No | No |

Only `TRUNCATE` satisfies all four requirements.

**Answer: A.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | Rollbackable, and it does not reset the identity counter |
| C | The table no longer exists — "keeps the table" fails |
| D | `DELETE * FROM` is a syntax error in every engine. `DELETE FROM orders;` |

---

### Q3 — Answer **B** (NULL comparison)

**Given `employees` with `manager_id` values `4, 4, 5, NULL, NULL, 5`, how many rows does
`SELECT emp_name FROM employees WHERE manager_id = NULL;` return?**

- A. 0
- B. 5
- C. 2
- D. 6

**Solution**

`manager_id = NULL` is evaluated as `UNKNOWN` for every row — the comparison against NULL is never
`TRUE`. `WHERE` keeps only rows where the predicate is `TRUE`. `UNKNOWN` is not `TRUE`, so **no row
qualifies**.

**Answer: A (0 rows).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | The answer for `manager_id IS NULL` (employees 4 and 5). The exam pairs these two options deliberately |
| C | The answer for `manager_id IS NOT NULL` (employees 1, 2, 3, 6) — 4 rows, not 2. The count of NULLs (2) is the trap |
| D | Every row, i.e. `WHERE TRUE` — the "no filter means all" misreading |

**Guard:** always write `IS NULL` / `IS NOT NULL`.

---

### Q4 — Answer **C** (`COUNT(*)` vs `COUNT(col)`)

**Table `employees` has 6 rows; `manager_id` is NULL for 2 of them. What does
`SELECT COUNT(*), COUNT(manager_id) FROM employees;` return?**

- A. `6, 6`
- B. `2, 6`
- C. `6, 4`
- D. `4, 2`

**Solution**

- `COUNT(*)` counts **rows**: 6.
- `COUNT(manager_id)` counts **non-NULL values** of that column: 6 − 2 = 4.

**Answer: C (`6, 4`).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Assumes `COUNT(col)` counts rows |
| B | Swapped, and the second number is wrong |
| D | Counts the NULLs instead of the non-NULLs — the exact inversion |

---

### Q5 — Answer **B** (`WHERE` before `HAVING`)

**Which query returns customers having more than one order?**

- A. `SELECT cust_id FROM orders GROUP BY cust_id WHERE COUNT(*) > 1;`
- B. `SELECT cust_id FROM orders GROUP BY cust_id HAVING COUNT(*) > 1;`
- C. `SELECT cust_id FROM orders WHERE cust_id IN (SELECT cust_id FROM orders GROUP BY cust_id HAVING COUNT(*) > 1);`
- D. `SELECT cust_id FROM orders GROUP BY cust_id ORDER BY COUNT(*) > 1;`

**Solution**

The condition references an aggregate. Aggregation happens at `GROUP BY`; the filter on the
aggregate must be `HAVING`, which runs after grouping.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | `WHERE` is applied before grouping; `COUNT(*)` does not exist yet. **Error in every standard engine** |
| C | Logically correct, but it is a needless nested subquery for a one-group filter — the exam wants the direct form. (It does return the same rows: customers 101 and 104) |
| D | `ORDER BY` needs a sort key; a boolean is not one, and it never filters |

---

### Q6 — Answer **A** (`NOT IN` + NULL)

**`orders` contains `cust_id` values 101, 101, 102, 103, 104, 104 — and one row where `cust_id` is
NULL. Which query returns customer 105 (who has no orders)?**

- A. `SELECT cust_name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.cust_id = c.cust_id);`
- B. `SELECT cust_name FROM customers c WHERE c.cust_id NOT IN (SELECT cust_id FROM orders);`
- C. `SELECT cust_name FROM customers WHERE cust_id NOT IN (101, 102, 103, 104);`
- D. `SELECT cust_name FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id WHERE o.order_id IS NULL;`

**Solution**

The subquery in B returns `{101, 101, 102, 103, 104, 104, NULL}`. `NOT IN` expands to
`cust_id <> 101 AND … AND cust_id <> NULL`. The last comparison is `UNKNOWN`, and
`TRUE AND UNKNOWN = UNKNOWN`, so **no row is returned**. B returns the empty set.

`NOT EXISTS` (A) is NULL-safe: for customer 105 no matching order row exists, so the correlated
subquery is empty and `NOT EXISTS` is `TRUE`.

**Answer: A.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | The `NOT IN` + NULL trap. It returns **zero rows**, not the customers without orders |
| C | Correct on this data — the literal list has no NULL, so it returns customer 105. But the exam's point is the NULL trap: with a literal list you must type every excluded id, and it silently breaks if the data changes. A is the robust form the exam wants when the question says "who has no orders" |
| D | Also correct (a `LEFT JOIN … IS NULL` anti-join) and returns customer 105. Exam accepts A as intended because it does not need the extra join; D is the alternative form |

**Learning point:** two options can both be *correct* SQL with the same result. When that happens,
the exam's intended answer is the one that states the pattern the question is testing. If you see
two correct options, re-read the stem for a hint like "using a subquery".

---

### Q7 — Answer **B** (`UNION` vs `UNION ALL`)

**`SELECT city FROM customers WHERE cust_id IN (101,103)` returns Pune, Pune.
`SELECT city FROM customers WHERE cust_id IN (101,104)` returns Pune, Delhi.
What does `SELECT city FROM customers WHERE cust_id IN (101,103) UNION ALL SELECT city FROM customers
WHERE cust_id IN (101,104);` return?**

- A. 2 rows: Pune, Delhi
- B. 4 rows: Pune, Pune, Pune, Delhi
- C. 3 rows: Pune, Pune, Delhi
- D. 5 rows

**Solution**

`UNION ALL` keeps duplicates. 2 rows from the first branch + 2 rows from the second = 4 rows.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | This is `UNION` (which dedups to Pune, Delhi) |
| C | Assumes the duplicate Pune is removed once but keeps both of the second branch |
| D | Off-by-one; nothing removes a row |

---

### Q8 — Answer **A** (`LIMIT` with ties)

**`customers` holds: 101 Ananya (Pune), 102 Rahul (Chennai), 103 Meera (Pune), 104 Karthik (Delhi),
105 Vikram (Bengaluru). What does `SELECT cust_name FROM customers ORDER BY city DESC LIMIT 2;`
return?**

- A. Two rows — Ananya and Meera — in an undefined order between them
- B. Two rows — Karthik and Rahul
- C. Two rows — Vikram and Rahul
- D. Two rows — Ananya and Meera, with Ananya first

**Solution**

`ORDER BY city DESC` sorts the city string descending. Alphabetically:
Pune > Delhi > Chennai > Bengaluru.

| Position | City | Customer |
|---|---|---|
| 1 | Pune | Ananya **or** Meera |
| 2 | Pune | Meera **or** Ananya |
| 3 | Delhi | Karthik |
| 4 | Chennai | Rahul |
| 5 | Bengaluru | Vikram |

Both top rows come from Pune. The two Pune rows **tie** on the sort key, so the engine may return
them in either order.

**Answer: A.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | Delhi and Chennai are positions 3 and 4 in the descending order, not the top 2 |
| C | Bengaluru is the **lowest** city alphabetically, so it is last in a descending sort |
| D | The pair is right, but the order inside the tie is **not guaranteed**. A query that needs a fixed answer must add a tiebreaker: `ORDER BY city DESC, cust_id ASC LIMIT 2` → Ananya (101), Meera (103) |

**The trap this question tests:** `ORDER BY` on a column with ties leaves the order between the tied
rows undefined. If the exam asks "which row is first", the query must have a deterministic
tiebreaker or the question is unfair.

---

### Q9 — Answer **D** (`BETWEEN` is inclusive)

**Which query returns orders with `amount` from 300 to 1000 inclusive?**

- A. `WHERE amount > 300 AND amount < 1000`
- B. `WHERE amount >= 300 OR amount <= 1000`
- C. `WHERE amount BETWEEN 300 AND 1000`
- D. `WHERE amount IN (300, 1000)`

**Solution**

`BETWEEN` is inclusive on both ends — 300 and 1000 are included.

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Exclusive at both ends — it drops the boundary values 300 and 1000 |
| B | `OR` makes it true for every row (any number is either ≥300 or ≤1000) |
| D | Matches only the two boundary values, not the range |

---

### Q10 — Answer **A** (`UPDATE` needs a `WHERE`)

**Which statement changes the city of customer 101 to 'Mumbai' and leaves every other row
untouched?**

- A. `UPDATE customers SET city = 'Mumbai' WHERE cust_id = 101;`
- B. `UPDATE customers SET city = 'Mumbai';`
- C. `UPDATE customers SET cust_id = 101, city = 'Mumbai';`
- D. `UPDATE customers SET city = 'Mumbai' WHERE city = 'Pune';`

**Solution**

`UPDATE` changes rows. Without a `WHERE` it changes **every** row. The stem says "customer 101 and
leaves every other row untouched", so a `WHERE` on `cust_id` is required.

**Answer: A.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | Changes the city of all 5 customers |
| C | Also rewrites the primary key of every row — and it has no `WHERE`, so it corrupts the table |
| D | Changes both Ananya (101) and Meera (103) — Meera was not mentioned |

---

### Q11 — Answer **B** (subquery type)

**Which query finds the customer with the highest single order amount?**

- A. `SELECT cust_name FROM customers WHERE cust_id IN (SELECT MAX(amount) FROM orders);`
- B. `SELECT cust_name FROM customers WHERE cust_id = (SELECT cust_id FROM orders ORDER BY amount DESC LIMIT 1);`
- C. `SELECT cust_name FROM customers WHERE cust_id IN (SELECT cust_id FROM orders GROUP BY cust_id HAVING MAX(amount));`
- D. `SELECT cust_name FROM customers WHERE cust_id > (SELECT MAX(amount) FROM orders);`

**Solution**

The question asks for the **row** with the maximum amount, so you need the `cust_id` of that row.
That requires a scalar subquery returning exactly one value, or `ORDER BY … LIMIT 1` inside a
subquery.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | `MAX(amount)` is `1200.00`; comparing it to a `cust_id` (101–105) matches nothing |
| C | `HAVING MAX(amount)` is not a valid predicate — `MAX(amount)` is a value, not a boolean. Also, a group's max is not the row-level max |
| D | Compares a `cust_id` against an amount (`1200`), so no row matches |

---

### Q12 — Answer **C** (`DROP` beats `TRUNCATE` for the table)

**An intern runs `TRUNCATE TABLE orders;` and then the DBA says the table itself is gone and must
be recreated. Which statement would have produced that result?**

- A. `DELETE FROM orders;`
- B. `TRUNCATE TABLE orders;`
- C. `DROP TABLE orders;`
- D. `ALTER TABLE orders DROP COLUMN amount;`

**Solution**

Only `DROP TABLE` removes the table. `TRUNCATE` empties it; `ALTER … DROP COLUMN` removes one
column.

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Removes rows only; the table survives |
| B | Empties the table and resets the identity counter; the table survives |
| D | Drops the `amount` column; the table and its other columns survive |

---

### Q13 — Answer **D** (`DISTINCT` applies to the whole row)

**`SELECT DISTINCT city, cust_name FROM customers;` on the shared fixture returns how many rows?**

- A. 5
- B. 2
- C. 3
- D. 4

**Solution**

Rows: (Pune, Ananya), (Chennai, Rahul), (Pune, Meera), (Delhi, Karthik), (Bengaluru, Vikram).
No two rows are identical in **both** columns, so `DISTINCT` removes nothing → 5 rows.

**Answer: A (5).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | The count of distinct **cities** (Pune, Chennai, Delhi, Bengaluru) — ignores that `DISTINCT` applies to the whole row |
| C | A partial count of distinct cities that appear more than once |
| D | A guess based on "Pune appears twice so one row is removed" — but Ananya and Meera are different people, so both rows survive |

**Learning point:** `DISTINCT` removes duplicate *rows*, not rows sharing one value.

## Quick rules

- `DELETE` = rows (with `WHERE`, rollbackable) · `TRUNCATE` = empty table, resets identity ·
  `DROP` = delete the table.
- `NULL` never equals anything, not even itself. Use `IS NULL`.
- `COUNT(*)` counts rows; `COUNT(col)` counts non-NULL values.
- Aggregates in `HAVING`, never in `WHERE`.
- `NOT IN` + a NULL in the list = zero rows. `NOT EXISTS` is NULL-safe.
- `UNION` dedups; `UNION ALL` keeps duplicates.
- `BETWEEN` includes both ends.
- `UPDATE`/`DELETE` without `WHERE` hits every row.
- `ORDER BY` before `LIMIT`; add a tiebreaker when values tie.

## Common traps

| Trap | Wrong answer | Right answer | Option |
|---|---|---|---|
| `= NULL` | Counts the NULL rows | 0 rows | B vs A |
| `COUNT(*)` = `COUNT(col)` | 6, 6 | 6, 4 | A vs C |
| Aggregate in `WHERE` | B | `HAVING` | B |
| `NOT IN` with NULL | Returns customers | Returns nothing | B |
| `UNION` used where duplicates count | 2 rows | 4 rows | A vs B |
| `LIMIT` with tied sort key | A specific order | Undefined order | B |
| `UPDATE` without `WHERE` | B | A | B |
| `BETWEEN` exclusive | A | C | A |

## Checklist

- [ ] I named the statement family before answering.
- [ ] I checked the discriminating requirement (rows vs structure vs rollback).
- [ ] I checked every NULL-related option.
- [ ] I confirmed that any aggregate sits in `SELECT`/`HAVING`, not `WHERE`.
- [ ] I checked whether `UNION` or `UNION ALL` was asked for.
- [ ] I added a tiebreaker to any `ORDER BY … LIMIT` I wrote.
- [ ] I logged the archetype of every question I got wrong.

## Related

- [DDL, DML and SQL anatomy](../01-concepts/01-ddl-dml-anatomy.md)
- [SELECT, filter, sort and subqueries](../01-concepts/02-select-filter-sort-and-subqueries.md)
- [Statement decision procedures](../02-techniques/01-statement-decision-procedures.md)
- [SQL basics traps](../04-pitfalls/01-sql-basics-traps.md)
- [SQL basics cheat sheet](../05-reference/01-sql-basics-cheat-sheet.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
