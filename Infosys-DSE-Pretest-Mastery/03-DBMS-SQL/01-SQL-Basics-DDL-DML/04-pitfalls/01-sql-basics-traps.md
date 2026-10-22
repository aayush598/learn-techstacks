# SQL Basics Traps — What the Exam Sets for You

> Section 3 · DBMS & SQL · SQL Basics, DDL & DML · _Estimated reading time: 6 min_
> **Prerequisite:** [DDL, DML and SQL anatomy](../01-concepts/01-ddl-dml-anatomy.md)

## In one sentence

Every trap in this topic is a **near-miss statement** — real SQL that does the wrong thing, or the
right thing applied to the wrong scope.

## Why the pre-test tests this

- Option lists in DBMS MCQs are usually four *valid* SQL statements. You cannot answer by
  recognising "valid SQL" — you must recognise "valid SQL that solves this stem".
- Learning to see the trap in the option list is faster than reasoning carefully every time.
- These nine traps account for most of the marks lost in archetype (a).

## Core concept

### The nine traps and their signature options

| # | Trap | The wrong computation | Signature option |
|---|---|---|---|
| 1 | "delete the table" read as "delete the rows" | `DELETE FROM t` | The `DELETE` option when the stem says *table* |
| 2 | "remove all rows" read as "remove the table" | `DROP TABLE t` | The `DROP` option when the stem says *rows* |
| 3 | `= NULL` | treating NULL as a value | The option that counts the NULL rows |
| 4 | `COUNT(*)` vs `COUNT(col)` | counting NULLs | The option with equal counts |
| 5 | Aggregate in `WHERE` | `WHERE COUNT(*) > 1` | The option with `WHERE` before `GROUP BY` |
| 6 | `NOT IN` + NULL | assuming it works like `NOT EXISTS` | The option claiming "returns customers with no orders" |
| 7 | `UNION` vs `UNION ALL` | deduping when duplicates count | The smaller row count |
| 8 | `LIMIT` without `ORDER BY` | assuming a default order | Any specific "first row" claim |
| 9 | `UPDATE`/`DELETE` without `WHERE` | "it means all rows" | The no-`WHERE` option when the stem names one row |

**Meta-rule:** in a DBMS MCQ, the option that is *most dramatic* is usually the trap.
`DROP DATABASE`, `DELETE *`, `UPDATE` with no `WHERE` — the exam's wrong answers are the ones a
careless candidate writes.

## Worked example

**Q. Which statement removes the rows of the `orders` table but keeps the table itself, and can be
rolled back inside a transaction?**

- A. `DROP TABLE orders;`
- B. `TRUNCATE TABLE orders;`
- C. `DELETE FROM orders;`
- D. `DELETE * FROM orders;`

**Solution**

| Requirement | A | B | C | D |
|---|---|---|---|---|
| Removes the rows | Yes | Yes | Yes | **Syntax error** |
| Keeps the table | **No** | Yes | Yes | — |
| Rollbackable | No | No | **Yes** | — |

**Answer: C (`DELETE FROM orders;`).**

**The traps in this question**

| Trap | Where it shows up |
|---|---|
| Confusing "removes the rows" with "removes the table" | Option A |
| Ignoring the rollback requirement | Option B — `TRUNCATE` is DDL and auto-commits in MySQL |
| Sloppy syntax | Option D — `DELETE * FROM` is invalid; it is `DELETE FROM orders;` |

**Second example — the `NOT IN` + NULL trap.**

**Q. Which query returns the customers who have placed no order?**

- A. `... WHERE c.cust_id NOT IN (SELECT cust_id FROM orders WHERE cust_id IS NOT NULL);`
- B. `... WHERE c.cust_id NOT IN (SELECT cust_id FROM orders);`
- C. `... WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.cust_id = c.cust_id);`
- D. `... WHERE c.cust_id = NULL;`

The `orders` table contains one row with a NULL `cust_id`.

| Option | Result | Why |
|---|---|---|
| A | Correct | Filtering the NULL out of the list makes `NOT IN` safe — but it is a fragile fix |
| B | **Zero rows** | `cust_id <> NULL` is `UNKNOWN`, so nothing passes |
| C | Correct | NULL-safe, and it is the pattern the question is testing |
| D | Zero rows | `= NULL` never matches |

**Correct answer: C.** The exam wants `NOT EXISTS`; A also works but only because the NULL was
explicitly removed, and the standard is to use `EXISTS`/`NOT EXISTS` for existence questions.

**Third example — `COUNT` vs `COUNT(*)`.**

**Q. `employees` has 6 rows, `manager_id` NULL for 2. What does `SELECT COUNT(manager_id) FROM
employees;` return?**

| Answer | Verdict |
|---|---|
| 6 | Trap — this is `COUNT(*)` |
| 2 | Trap — this is the number of NULLs |
| 4 | **Correct** — 6 rows minus 2 NULLs |
| 1 | Trap — one aggregate row |

The option `4` next to `6` is the signature pair. If you see `6, 6` as an option, one of the two
columns is `COUNT(*)`.

## Quick rules

- "Remove the table" → `DROP`. "Remove all the rows" → `TRUNCATE`. "Remove some rows" → `DELETE`.
- Rollbackable = DML = `INSERT`/`UPDATE`/`DELETE`. Not rollbackable = DDL = `CREATE`/`ALTER`/
  `DROP`/`TRUNCATE`.
- `IS NULL`, never `= NULL`.
- `COUNT(*)` = rows. `COUNT(col)` = non-NULL values of `col`.
- `WHERE` = rows, `HAVING` = groups. An aggregate can only go in `HAVING`.
- `NOT IN` with a possibly-NULL list = empty result. Use `NOT EXISTS`.
- `UNION` dedups, `UNION ALL` does not.
- `ORDER BY` before `LIMIT`.
- A `WHERE` on `UPDATE`/`DELETE` is not decoration.

## Common traps

| Trap | How it shows up | Guard rail |
|---|---|---|
| `DROP` for "delete all rows" | `DROP TABLE t` offered | Read the noun: rows vs table |
| `TRUNCATE` for "delete some rows" | `TRUNCATE` offered next to `DELETE … WHERE` | `TRUNCATE` cannot take a `WHERE` |
| `= NULL` | Option counting the NULL rows | `IS NULL` / `IS NOT NULL` |
| `COUNT(*)` vs `COUNT(col)` | Equal counts offered | Ask "does the column have NULLs?" |
| Aggregate in `WHERE` | `WHERE COUNT(*) > 1` | `HAVING` |
| `NOT IN` + NULL | "Returns the right rows" | `NOT EXISTS` |
| `UNION` for `UNION ALL` | A row count one too small | Ask "duplicates counted?" |
| `LIMIT` without `ORDER BY` | A named first row | Order first, cut second |
| No `WHERE` on `UPDATE` | The all-rows option | Read "which rows" from the stem |

## Checklist

- [ ] I read the noun in the stem: **rows**, **table**, **column**, **records**.
- [ ] I checked whether the statement must be rollbackable.
- [ ] I checked every NULL-related option.
- [ ] I verified no aggregate sits in a `WHERE`.
- [ ] I chose `EXISTS`/`NOT EXISTS` for existence questions.
- [ ] I can name the trap behind every question I got wrong.

## Related

- [DDL, DML and SQL anatomy](../01-concepts/01-ddl-dml-anatomy.md)
- [Statement decision procedures](../02-techniques/01-statement-decision-procedures.md)
- [Solved SQL basics set](../03-worked-examples/01-solved-sql-basics-set.md)
- [SQL basics cheat sheet](../05-reference/01-sql-basics-cheat-sheet.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
