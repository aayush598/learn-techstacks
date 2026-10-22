# Joins — The Six Kinds, and the One Mental Model That Covers Them

> Section 3 · DBMS & SQL · Joins · _Estimated reading time: 9 min_
> **Prerequisite:** [SELECT, filter, sort and subqueries](../01-SQL-Basics-DDL-DML/01-concepts/02-select-filter-sort-and-subqueries.md)

## In one sentence

**A join is a filter over the cartesian product, and the join type decides which side of the
mismatch you keep** — INNER keeps neither, LEFT keeps the left, RIGHT keeps the right.

## Why the pre-test tests this

- "SQL fundamentals up to JOINs" is the single largest sub-archetype in this section: 2–3 of the 10
  questions.
- The pre-test asks two flavours: *"which join do I need?"* (a 30-second decision) and *"what is the
  output of this join?"* (a 60-second trace). Both come from the same mental model.
- The `WHERE`-after-`LEFT JOIN` trap is the single most common wrong answer in DBMS MCQs.

## Core concept

### 1. The one mental model: everything starts as a cartesian product

```
FROM customers, orders        → 5 × 6 = 30 rows (every customer × every order)
ON  c.cust_id = o.cust_id     → keep only the 6 matching pairs
```

| Join type | Keeps rows where | Unmatched left rows | Unmatched right rows | Result size on the shared fixture |
|---|---|---|---|---|
| `INNER` / `JOIN` | ON matches | Dropped | Dropped | **6** |
| `LEFT OUTER` | ON matches | **Kept, right side NULL** | Dropped | **7** (6 + Vikram) |
| `RIGHT OUTER` | ON matches | Dropped | **Kept, left side NULL** | **7** |
| `FULL OUTER` | ON matches | **Kept, NULLs** | **Kept, NULLs** | **7** |
| `CROSS` | everything | Kept | Kept | **30** |
| `SELF` (INNER or LEFT) | ON matches on the same table | per type | per type | depends |

The single most useful thing to memorise: **`LEFT JOIN` keeps unmatched left rows with NULLs on the
right.** Everything else is a variation on which side you keep.

### 2. `INNER JOIN`

```sql
SELECT c.cust_name, o.order_id, o.amount
FROM   customers c
INNER JOIN orders o ON c.cust_id = o.cust_id;
```

Only rows where the `ON` condition is true. Unmatched rows from **both** sides are discarded.

```
customers        orders         INNER JOIN result
101 Ananya  ─┬─ 1001 (101)
              └─ 1002 (101)
102 Rahul   ──── 1003 (102)
103 Meera   ──── 1004 (103)
104 Karthik ─┬─ 1005 (104)
              └─ 1006 (104)
105 Vikram ──── (no match → dropped)
                                       = 6 rows
```

Note the multiplicity: customer 101 appears **twice**, once per order. A join **multiplies rows**
when the key is not unique on the right. `COUNT(*)` after this join counts join rows, not customers.

### 3. `LEFT OUTER JOIN`

```sql
SELECT c.cust_name, o.order_id, o.amount
FROM   customers c
LEFT JOIN orders o ON c.cust_id = o.cust_id;
```

Every row of the **left** table survives. Rows with no match get `NULL` for every right-table
column.

```
101 Ananya   1001  500.00
101 Ananya   1002  750.00
102 Rahul    1003  1200.00
103 Meera    1004  300.00
104 Karthik  1005  950.00
104 Karthik  1006  1100.00
105 Vikram   NULL  NULL     ← unmatched left row, right side NULL
                                = 7 rows
```

Three rules that follow from this:

1. `WHERE o.order_id IS NULL` on a `LEFT JOIN` is an **anti-join**: "left rows with no match".
2. `COUNT(*)` = 7 but `COUNT(o.order_id)` = 6. The difference is exactly the number of unmatched
   left rows.
3. `SUM(o.amount)` ignores the NULL row, so it equals the inner-join sum.

### 4. `RIGHT OUTER JOIN`

The mirror image. Every row of the **right** table survives; unmatched right rows get NULLs on the
left.

**Rule of thumb:** `RIGHT JOIN` is almost never what you want — you can always rewrite it as a
`LEFT JOIN` with the tables swapped, which reads better. In the pre-test, if you see `RIGHT JOIN`,
check the option order: the exam usually writes the "right" table first, which is the confusing
case.

### 5. `FULL OUTER JOIN`

Keeps unmatched rows from **both** sides. MySQL does **not** support `FULL OUTER JOIN` — you emulate
it with a `LEFT JOIN UNION RIGHT JOIN`. The exam may still ask the concept.

### 6. `CROSS JOIN`

Every row of the left table × every row of the right table. `CROSS JOIN` with no `ON` = 30 rows on
the shared fixture. Use it for date/calendar grids, and never by accident.

### 7. `SELF JOIN`

Joining a table to itself. The classic use is the **manager hierarchy**: `manager_id` in
`employees` points to `emp_id` in `employees`.

```sql
SELECT e.emp_name AS employee,
       m.emp_name AS manager
FROM   employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id;
```

```
employee   manager
Ananya     Karthik
Rahul      Karthik
Meera      Vikram
Karthik    NULL      ← Karthik manages nobody
Vikram     NULL      ← Vikram manages nobody
Anjali     Vikram
```

A `LEFT JOIN` is used rather than an `INNER JOIN` so the top of the hierarchy (the people with no
manager) is not lost. You must give the two aliases **different names** (`e` and `m`) or the query
is ambiguous.

### 8. Many-to-many relationships need a junction table

There is no direct many-to-many join. You create a third table holding the two foreign keys.

```sql
CREATE TABLE enrollments (
  student_id INT,
  course_id  INT,
  grade      VARCHAR(2),
  PRIMARY KEY (student_id, course_id),
  FOREIGN KEY (student_id) REFERENCES students(student_id),
  FOREIGN KEY (course_id)  REFERENCES courses(course_id)
);
```

Joining `students → enrollments → courses` gives **one row per enrolment**, so a student taking 3
courses appears 3 times. `COUNT(DISTINCT s.student_id)` fixes that.

### 9. `ON` vs `WHERE` — the boundary

| | `ON` | `WHERE` |
|---|---|---|
| Part of | The join condition | The row filter |
| Evaluated | While matching rows | After the join produces rows |
| Can reference | Columns of the joined tables | Any column |
| With `LEFT JOIN` | Decides which left rows match | Filters the **joined result**, including the NULL-padded rows |

**The trap:** moving a right-table condition from `ON` to `WHERE` on a `LEFT JOIN` **silently turns
it into an INNER JOIN**, because the NULL-padded rows have `NULL` in the right table and
`NULL = 'Pune'` is `UNKNOWN`, so they are filtered out.

```sql
-- LEFT JOIN: all 5 customers, 7 rows
SELECT c.cust_name, o.amount
FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id;

-- The SAME query with WHERE: only 5 customers who HAVE orders, 6 rows
SELECT c.cust_name, o.amount
FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id
WHERE o.amount > 400;
```

The second query cannot return Vikram at all, because his `o.amount` is NULL and `NULL > 400` is
`UNKNOWN`.

### 10. `NATURAL JOIN`

```sql
SELECT * FROM customers NATURAL JOIN orders;
```

- Joins on **every column with the same name** in both tables (`cust_id` here).
- You **cannot specify the join condition**.
- If a new column with a matching name is added later, the join silently changes behaviour. This is
  why production code avoids it.
- It is an INNER join.
- `NATURAL LEFT JOIN` exists and keeps unmatched left rows.

The exam's favourite question: "how many columns does `SELECT *` return after `NATURAL JOIN`?" —
the shared columns appear **once**, not twice.

### 11. `USING` — the explicit version of `NATURAL`

```sql
SELECT * FROM customers JOIN orders USING (cust_id);
```

You name the join columns explicitly, and the joined column appears **once** in the output.

### 12. Table aliases — mandatory with two tables

```sql
SELECT c.cust_name, o.amount
FROM   customers AS c
JOIN   orders     AS o ON o.cust_id = c.cust_id;
```

- Both tables have a `cust_id` column, so `cust_id` alone is ambiguous.
- `c.cust_id` and `o.cust_id` disambiguate.
- Use the alias for the **table**, then the column: `c.cust_name`, not `cust_id.cust_name`.
- Alias names should not shadow column names — `FROM customers c` creates table alias `c`, and
  `c.cust_name` refers to the table.

### 13. The join fan-out problem

Joining two one-to-many chains multiplies rows:

```
customers 1---* orders 1---* order_items
1 order × 3 items  →  3 rows per order
2 orders × 3 items  →  6 rows
```

The fix when you want distinct entities:

```sql
SELECT c.cust_name, COUNT(DISTINCT o.order_id) AS orders,
       COUNT(i.item_id) AS items
FROM customers c
JOIN orders o ON o.cust_id = c.cust_id
JOIN order_items i ON i.order_id = o.order_id
GROUP BY c.cust_id, c.cust_name;
```

`COUNT(DISTINCT o.order_id)` counts orders even though each order was duplicated by the items
join.

## Worked example

**Q. Given the shared fixture, what does
`SELECT c.cust_name, o.order_id FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id;`
return?**

- A. 5 rows
- B. 6 rows
- C. 7 rows
- D. 11 rows

**Solution**

1. `FROM customers` → 5 rows.
2. `LEFT JOIN orders ON c.cust_id = o.cust_id` → for each customer, every matching order:
   - 101 → 2 rows, 102 → 1 row, 103 → 1 row, 104 → 2 rows, 105 → **1 row with NULLs**.
3. Total = 2 + 1 + 1 + 2 + 1 = **7 rows**.

**Answer: C (7 rows).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | 5 = the number of **customers**. This is `COUNT(DISTINCT c.cust_id)` or a `GROUP BY` on customers — it ignores that the join fans out |
| B | 6 = the **inner join** row count. A `LEFT JOIN` never drops the unmatched left row |
| D | 11 = 5 + 6, the "every customer plus every order" count. That would be a cartesian product of 5 × 6 = 30, and 11 comes from adding rows instead of matching them |

**The row set**

```
cust_name   order_id
Ananya      1001
Ananya      1002
Rahul       1003
Meera       1004
Karthik     1005
Karthik     1006
Vikram      NULL     ← the row a LEFT JOIN adds and an INNER JOIN drops
```

## Quick rules

- Cartesian product first, then filter by `ON`. The join type decides which mismatches survive.
- `LEFT JOIN` = **keep every left row**; unmatched right side is NULL.
- `COUNT(*)` counts join rows; `COUNT(right.col)` counts matched rows.
- `WHERE right.col = x` on a `LEFT JOIN` removes the NULL-padded rows → behaves like INNER.
- `ON` = match condition. `WHERE` = filter the result.
- `RIGHT JOIN` = `LEFT JOIN` with the tables swapped. Prefer the `LEFT` form.
- `NATURAL JOIN` matches on all same-named columns and cannot be customised.
- Many-to-many needs a junction table; the join then returns one row per junction row.
- Self-join: use two different aliases and usually a `LEFT JOIN` to keep the top of the hierarchy.

## Common traps

| Trap | What you get | What you should get |
|---|---|---|
| `WHERE` on the right table of a `LEFT JOIN` | Inner-join behaviour | Move the condition into `ON` |
| `COUNT(*)` after a one-to-many join | 7 (join rows) | `COUNT(DISTINCT c.cust_id)` = 5 |
| `LEFT JOIN` + `WHERE right IS NULL` thinking it filters matches | It filters to the *unmatched* rows | That is the anti-join — correct, but know why |
| `NATURAL JOIN` assumed to join on one named column | Joins on **all** matching column names | Use explicit `ON` or `USING` |
| `RIGHT JOIN` read left-to-right | Wrong side kept | The **right** table's rows always survive |
| Self-join without aliases | Ambiguous column error | `employees e JOIN employees m` |
| Forgetting the fan-out on a 3-table join | Inflated counts | `COUNT(DISTINCT ...)` |

## Checklist

- [ ] I can state what a `LEFT JOIN` keeps in one sentence.
- [ ] I checked whether a `WHERE` condition on the right table silently kills the `LEFT JOIN`.
- [ ] I used `COUNT(DISTINCT col)` when the join can fan out.
- [ ] I know that `NATURAL JOIN` matches on every same-named column.
- [ ] I used two different aliases for a self-join.
- [ ] I checked the row count of the join before answering an output question.

## Related

- [Join decision table](../02-techniques/01-join-decision-table.md)
- [Solved join set](../03-worked-examples/01-solved-join-set.md)
- [Join traps](../04-pitfalls/01-join-traps.md)
- [Join reference sheet](../05-reference/01-join-reference-sheet.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
