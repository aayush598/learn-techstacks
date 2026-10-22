# Join Traps — The Five That Cost Marks

> Section 3 · DBMS & SQL · Joins · _Estimated reading time: 6 min_
> **Prerequisite:** [The six joins](../01-concepts/01-the-six-joins.md)

## In one sentence

The `LEFT JOIN` + `WHERE` trap is the highest-frequency wrong answer in the whole DBMS section, and
four other traps sit right behind it.

## Why the pre-test tests this

- Option lists are designed so that the "obvious" join and the "correct" join are both present. The
  only way to tell them apart is to read the stem's escape clause.
- These five traps account for most of the marks lost in the join archetype.

## Core concept

### Trap 1 — `WHERE` on the right table kills the `LEFT JOIN`

| | Query | Rows on the fixture |
|---|---|---|
| LEFT JOIN, no filter | `customers c LEFT JOIN orders o ON c.cust_id = o.cust_id` | **7** (Vikram present) |
| LEFT JOIN + `WHERE o.amount > 400` | same + filter | **5** (Vikram lost) |
| INNER JOIN + same filter | `customers c JOIN orders o ON ... WHERE o.amount > 400` | **5** (identical!) |

Why: the NULL-padded row has `o.amount = NULL`, and `NULL > 400` is `UNKNOWN`, not `TRUE`, so
`WHERE` discards it. The `LEFT JOIN` has become an `INNER JOIN`.

**Fix:** move the right-table predicate into `ON`:
`LEFT JOIN orders o ON c.cust_id = o.cust_id AND o.amount > 400` → 7 rows, Vikram included with
NULLs, and only orders over 400.

**Signature in the option list:** the `LEFT JOIN` option and the `INNER JOIN` option produce the
*same* row count, and the correct answer is the one that keeps the unmatched left row.

### Trap 2 — `COUNT(*)` after a join counts join rows

```sql
-- "How many customers have at least one order?"
SELECT COUNT(*) FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id;   -- 7, not 5
```

`COUNT(*)` counts **rows of the result**, and the join fanned 4 customers out to 6 rows plus the
NULL row. Correct forms:

```sql
SELECT COUNT(DISTINCT c.cust_id) FROM customers c LEFT JOIN orders o ON ...;  -- 5
SELECT COUNT(o.order_id) FROM customers c LEFT JOIN orders o ON ...;           -- 6
```

### Trap 3 — `NATURAL JOIN` joins on *every* same-named column

`NATURAL JOIN customers orders` joins on `cust_id` **and** on any other column the two tables share.
Add a `status` column to both and the join silently changes.

- `SELECT *` after a `NATURAL JOIN` shows the joined column **once** (6 columns on the fixture).
- `SELECT *` after an explicit `JOIN` shows it **twice** (7 columns).
- You cannot write a custom condition with `NATURAL JOIN`; use `USING (cust_id)` or `ON`.

### Trap 4 — `RIGHT JOIN` reads right-to-left

The keyword names the side that **survives**, not the side that is written first.

| Query | Rows | Who survives |
|---|---|---|
| `customers c LEFT JOIN orders o` | 7 | All customers |
| `customers c RIGHT JOIN orders o` | 6 | All orders (every order has a customer here) |
| `orders o RIGHT JOIN customers c` | 7 | All customers |
| `orders o LEFT JOIN customers c` | 6 | All orders |

The trap option is `orders RIGHT JOIN customers` presented as if "RIGHT" means "the table on the
right is the important one". It means the opposite.

### Trap 5 — many-to-many row count equals the junction count

```sql
-- 3 students, 3 courses, 5 enrollments
SELECT s.student_name, c.course_name
FROM students s JOIN enrollments e ON e.student_id = s.student_id
JOIN courses c ON c.course_id = e.course_id;   -- 5 rows
```

The join returns one row per **enrolment**. If the question asks for one row per student, add
`GROUP BY` or `DISTINCT`, and use `COUNT(DISTINCT c.course_id)`.

### Bonus trap — the self-join without aliases

```sql
SELECT emp_name FROM employees JOIN employees ON manager_id = emp_id;  -- error
```

Two copies of the same table need two names, and every column reference needs a prefix:
`employees e JOIN employees m ON e.manager_id = m.emp_id`.

## Worked example

**Q. `SELECT COUNT(*) FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id;` returns what?**

- A. 5
- B. 6
- C. 7
- D. 10

**Solution**

The `LEFT JOIN` produces 6 matched rows + 1 NULL-padded row for Vikram = **7 rows**.
`COUNT(*)` counts rows → 7.

**Answer: C (7).**

**The traps in this question**

| Trap | Where it shows up |
|---|---|
| Counting customers, not join rows | Option A |
| Forgetting that `LEFT JOIN` adds a row | Option B |
| Counting the cartesian product (5 × 6 = 30 → but here only "5 + 5"?) | Option D |

**Second example — the `WHERE` trap.**

**Q. Which query returns Vikram (the customer with no orders)?**

| Option | Query | Result |
|---|---|---|
| A | `... LEFT JOIN orders o ON c.cust_id = o.cust_id` | 7 rows, Vikram present with NULLs ✅ |
| B | `... LEFT JOIN orders o ON c.cust_id = o.cust_id WHERE o.amount IS NOT NULL` | 6 rows, Vikram dropped ❌ |
| C | `... JOIN orders o ON c.cust_id = o.cust_id` | 6 rows, Vikram dropped ❌ |
| D | `... CROSS JOIN orders o` | 30 rows, no NULL row ❌ |

**Answer: A.** Option B is the trap: adding `WHERE o.amount IS NOT NULL` to a `LEFT JOIN` deletes
exactly the rows the `LEFT JOIN` was there to preserve.

## Quick rules

- `LEFT JOIN` + a right-table `WHERE` = inner join. Put the right-table predicate in `ON`.
- `COUNT(*)` = result rows; `COUNT(col)` = non-NULL values of `col`; `COUNT(DISTINCT col)` = distinct
  values.
- `NATURAL JOIN` matches all same-named columns; `USING` or `ON` is safer.
- `RIGHT JOIN` keeps the **right** table's rows, whatever order the tables are written in.
- Many-to-many → one row per junction row.
- Self-join → two aliases, and prefix every column.

## Common traps

| Trap | Wrong answer | Right answer | Guard rail |
|---|---|---|---|
| `WHERE` kills the LEFT JOIN | Inner-join row count | Move to `ON` | Ask "do I still want the NULL row?" |
| `COUNT(*)` after a fan-out | Entity count | `COUNT(DISTINCT col)` | Count rows on paper |
| `NATURAL JOIN` column count | n + m | n + m − 1 shared | Count the shared columns |
| `RIGHT JOIN` direction | Wrong side kept | Rewrite as LEFT with tables swapped | Name the surviving table |
| Many-to-many count | Students or courses | Junction rows | Count the middle table |
| Self-join without aliases | Ambiguous column error | `e` and `m` | Always alias |

## Checklist

- [ ] I checked whether a `WHERE` condition nullified my `LEFT JOIN`.
- [ ] I used `COUNT(DISTINCT col)` where the join can fan out.
- [ ] I know that `NATURAL JOIN` shows the joined column once.
- [ ] I named the surviving table in any `RIGHT JOIN`.
- [ ] I counted junction rows for many-to-many questions.
- [ ] I aliased both copies in a self-join.
- [ ] I can name the trap behind every join question I got wrong.

## Related

- [The six joins](../01-concepts/01-the-six-joins.md)
- [Join decision table](../02-techniques/01-join-decision-table.md)
- [Solved join set](../03-worked-examples/01-solved-join-set.md)
- [Join reference sheet](../05-reference/01-join-reference-sheet.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
