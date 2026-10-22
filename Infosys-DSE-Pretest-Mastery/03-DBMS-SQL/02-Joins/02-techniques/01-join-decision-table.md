# Join Decision Table — Which Join Do I Need?

> Section 3 · DBMS & SQL · Joins · _Estimated reading time: 7 min_
> **Prerequisite:** [The six joins](../01-concepts/01-the-six-joins.md)

## In one sentence

**Read the stem for the shape of the answer — "all customers including those with no orders" is a
`LEFT JOIN`, "customers who have ordered" is an `INNER JOIN`** — and the join type writes itself.

## Why the pre-test tests this

- "Which join do I need?" is a 30-second question and it recurs. Getting it wrong costs the whole
  question, not a mark.
- The wording of the stem is the only signal you get. Learning to read it is cheaper than memorising
  syntax.
- The same table answers "which join?" and "what is the output?", so this file serves both.

## Core concept

### 1. The master decision table

Read the stem, find the row:

| What the question asks for | Join to write | Why |
|---|---|---|
| Rows where **both** sides match | `INNER JOIN` (or `JOIN`) | The default |
| **All** of the left table, plus matches from the right | `LEFT JOIN` | "including those with none" |
| **All** of the right table, plus matches from the left | `RIGHT JOIN` | Rarely the intent |
| Everything from both, matched or not | `FULL OUTER JOIN` | Not in MySQL |
| Every combination | `CROSS JOIN` | Grids, calendars |
| The same table twice | `SELF JOIN` | Hierarchy, same-day pairs |
| Left rows that have **no** match | `LEFT JOIN` + `WHERE right.col IS NULL` | Anti-join |
| A many-to-many relationship | Join through a **junction table** | Two joins |
| Join on one specific column | `ON a.id = b.id` | Explicit |
| Join on every same-named column | `NATURAL JOIN` | Avoid it |

### 2. The keyword scanner

Underline these words in the stem — they pick the join:

| Stem wording | Join |
|---|---|
| "only those that have", "matched", "common", "in both" | `INNER` |
| "all", "including those with no", "even if", "or without", "including customers who have never ordered" | `LEFT` |
| "every X, and if any" | `LEFT JOIN` on X |
| "all X **and** all Y" | `FULL OUTER` |
| "each X with each Y", "all combinations" | `CROSS` |
| "each employee with their manager" | `SELF JOIN` |
| "who have never", "with no matching" | `LEFT JOIN` + `IS NULL` |

### 3. Procedure — pick the join in 30 seconds

1. **Circle the entity that must appear.** If the stem says "list all customers…", the customer
   table is on the **left**. If it says "list all orders…", orders are on the left.
2. **Look for the escape clause** — "even if", "including those with no", "if any", "or without".
   If it is there → `LEFT JOIN`.
3. **Look for the restriction clause** — "who have", "that have an order", "where a matching order
   exists". If it is there → `INNER JOIN`.
4. **Check for a "never / no matching" clause.** → `LEFT JOIN` + `WHERE right.col IS NULL`.
5. **Check for "all combinations"** → `CROSS JOIN`.
6. **Check for two mentions of the same table** → `SELF JOIN`.
7. **Check for three tables** → there is a junction table somewhere.

### 4. Procedure — choose the LEFT table

The `LEFT` table is the one whose rows you cannot afford to lose.

| Stem | Left table | Join |
|---|---|---|
| "all customers and their orders" | `customers` | `customers LEFT JOIN orders` |
| "all orders and the customer who placed them" | `orders` | `orders LEFT JOIN customers` |
| "employees and their manager" | `employees e` | `employees e LEFT JOIN employees m` |
| "departments and their employees" | `departments` | `departments LEFT JOIN employees` |

Rule: **the entity named first in the stem is usually the left table**, but the real test is "which
side must keep its unmatched rows".

### 5. The three classic task shapes

| Task | Shape | Query skeleton |
|---|---|---|
| **Count per parent, including zeros** | LEFT JOIN + `GROUP BY` | `SELECT p.id, COUNT(ch.id) FROM parent p LEFT JOIN child ch ON ch.pid = p.id GROUP BY p.id` |
| **Find the ones with no children** | Anti-join | `... LEFT JOIN child ch ON ch.pid = p.id WHERE ch.id IS NULL` |
| **Sum per parent including zeros** | LEFT JOIN + `COALESCE` | `SELECT p.id, COALESCE(SUM(ch.amount),0) FROM parent p LEFT JOIN child ch ON ... GROUP BY p.id` |

**Why `COUNT(ch.id)` and not `COUNT(*)`:** in the first shape, `COUNT(*)` counts the NULL-padded row
as 1 and every parent appears to have at least one child. `COUNT(ch.id)` skips NULLs and correctly
reports 0.

### 6. Many-to-many — the two-step path

```sql
-- students → enrollments → courses
SELECT s.student_name, c.course_name, e.grade
FROM   students s
JOIN   enrollments e ON e.student_id = s.student_id
JOIN   courses     c ON c.course_id  = e.course_id;
```

If the question is "how many courses has each student taken, including students with none", the
first join must be a `LEFT JOIN`:

```sql
SELECT s.student_name, COUNT(c.course_id) AS courses
FROM   students s
LEFT JOIN enrollments e ON e.student_id = s.student_id
LEFT JOIN courses     c ON c.course_id  = e.course_id
GROUP BY s.student_id, s.student_name;
```

### 7. Self-join — the two alias rules

```sql
-- Rule 1: two aliases, one for each role
SELECT e.emp_name AS employee, m.emp_name AS manager
FROM   employees e
LEFT JOIN employees m ON m.emp_id = e.manager_id;

-- Rule 2: column prefixes follow the alias, not the table
-- e.emp_name  ✔    employees.emp_name as e  ✘
```

Rule 3: use `LEFT JOIN` when the top of the hierarchy must survive (rows where `manager_id IS NULL`).

### 8. When to use `INNER` vs `LEFT` — the 3-row test

Write the two candidate queries and count the rows on the fixture. The one that matches the row
count implied by the stem is right.

| Stem | Implied count on the fixture | Right join |
|---|---|---|
| "list customers who placed an order" | 4 customers (101, 102, 103, 104) | `INNER` |
| "list all customers and their order details" | 7 rows (5 customers, 101 and 104 twice) | `LEFT` |
| "list customers who have never ordered" | 1 customer (105) | `LEFT` + `IS NULL` |
| "list all customers with the number of orders" | 5 rows | `LEFT` + `GROUP BY` |

This test alone answers most pre-test join questions.

## Worked example

**Q. Which query lists all customers with their order amounts, including customers who have never
placed an order?**

- A. `SELECT c.cust_name, o.amount FROM customers c JOIN orders o ON c.cust_id = o.cust_id;`
- B. `SELECT c.cust_name, o.amount FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id;`
- C. `SELECT c.cust_name, o.amount FROM orders o RIGHT JOIN customers c ON c.cust_id = o.cust_id;`
- D. `SELECT c.cust_name, o.amount FROM customers c CROSS JOIN orders o;`

**Solution**

Apply Procedure 3:

1. Entity that must appear → **customers** ("all customers"). Customers go on the left.
2. Escape clause → **"including customers who have never placed an order"**. That is the
   `LEFT JOIN` signature.
3. The result must contain Vikram (customer 105), who has no orders. Only a `LEFT JOIN` (from
   `customers`) does that.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | `INNER JOIN` drops Vikram — 6 rows instead of 7. This is the most common wrong answer |
| C | `RIGHT JOIN` keeps unmatched **right** rows. Here the right table is `orders`, and every order has a customer, so the row set is identical to `INNER JOIN` — 6 rows, and Vikram is missing. The join type is right but the **table order** is wrong for this intent |
| D | `CROSS JOIN` gives 30 rows — every customer against every order. It has no match condition at all |

**Note on C:** it is the classic "right join written backwards" trap. `orders RIGHT JOIN customers`
is exactly `customers LEFT JOIN orders`, so if C had been written `customers RIGHT JOIN orders` it
would have been correct. Read the table order, not the keyword.

## Quick rules

- "All X **including** those without Y" → `X LEFT JOIN Y`.
- "X that have Y" → `INNER JOIN`.
- "X with no Y" → `LEFT JOIN` + `WHERE Y.id IS NULL`.
- "All combinations" → `CROSS JOIN`.
- The left table is the one whose rows must survive.
- `COUNT(child.id)` counts matches; `COUNT(*)` counts rows including the NULL-padded one.
- Two tables with a shared column name need aliases.
- Many-to-many always goes through a junction table.

## Common traps

| Trap | Wrong answer | Right answer |
|---|---|---|
| "including those with none" → INNER | A | B |
| `RIGHT JOIN` with the tables reversed | C | Swap so the kept table is on the left |
| `COUNT(*)` for "how many children" | Counts the NULL row | `COUNT(child.id)` |
| `CROSS JOIN` for "all customers with all orders" | 30 rows | Not a join type question |
| `NATURAL JOIN` for "join on id" | Joins on all same-named columns | Explicit `ON` |

## Checklist

- [ ] I circled the entity that must appear and put it on the left.
- [ ] I scanned for "including / even if / never" before choosing `INNER`.
- [ ] I applied the 3-row test on the fixture to confirm my choice.
- [ ] I used `COUNT(child.id)` for "count of children, including zero".
- [ ] I checked the table order in a `RIGHT JOIN`.
- [ ] I added aliases whenever two tables share a column name.

## Related

- [The six joins](../01-concepts/01-the-six-joins.md)
- [Solved join set](../03-worked-examples/01-solved-join-set.md)
- [Join traps](../04-pitfalls/01-join-traps.md)
- [Join reference sheet](../05-reference/01-join-reference-sheet.md)
- [Join cheat sheet](../05-reference/02-join-cheat-sheet.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
