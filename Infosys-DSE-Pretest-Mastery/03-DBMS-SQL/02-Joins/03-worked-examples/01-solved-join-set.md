# Joins — 9 Solved Questions

> Section 3 · DBMS & SQL · Joins · _Estimated reading time: 12 min_
> **Prerequisite:** [Join decision table](../02-techniques/01-join-decision-table.md)

## In one sentence

Nine join questions — four "which join", five "what is the output" — every one traced on paper.

## Why the pre-test tests this

- Joins are 2–3 of the 10 DBMS questions, the largest block in the section.
- The "which join" questions are worth 30 seconds each if you scan the stem correctly.
- The "what is the output" questions are worth 60 seconds each if you write the intermediate rows
  down. Do not trace them in your head.

## Core concept

Before each question:

1. **Which entity must appear?** Put it on the left.
2. **Escape clause?** "including", "even if", "never" → `LEFT JOIN`.
3. **Row count.** Compute it on the fixture before you pick the option.

**The shared fixture** (from the [section index](../../README.md#the-shared-fixture)):

```
customers                       orders
101 Ananya  Pune                1001 cust 101  500.00
102 Rahul   Chennai             1002 cust 101  750.00
103 Meera   Pune                1003 cust 102 1200.00
104 Karthik Delhi               1004 cust 103  300.00
105 Vikram  Bengaluru           1005 cust 104  950.00
                                1006 cust 104 1100.00
```

## Worked example

### Q1 — Answer **C** (the `LEFT JOIN` + `WHERE` trap)

**What does
`SELECT c.cust_name, o.amount FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id WHERE o.amount > 400;`
return?**

- A. 4 rows
- B. 6 rows
- C. 5 rows
- D. 7 rows

**Solution**

1. `LEFT JOIN` builds 7 rows (6 matched + 1 NULL-padded row for Vikram).
2. `WHERE o.amount > 400` then keeps only rows with an amount above 400:
   - 1001 (500) ✅, 1002 (750) ✅, 1003 (1200) ✅, 1004 (300) ❌, 1005 (950) ✅, 1006 (1100) ✅
   - Vikram's row: `o.amount` is NULL, and `NULL > 400` is `UNKNOWN` → filtered out.
3. Rows left = **5**.

**Answer: C (5 rows).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Counts only the Pune customers' large orders (500 + 750 = 2 for Ananya, 1200 for Rahul = 3… plus Meera's 300 excluded) — a miscount of the filter |
| B | The **inner join** count after the same filter — the answer if the join were `INNER`. This is the trap: a `WHERE` on the right table of a `LEFT JOIN` silently converts it to an inner join |
| D | The full `LEFT JOIN` count before the `WHERE` — ignores the filter |

**The lesson:** move the condition into `ON` if you want the NULL-padded rows to survive:
`... LEFT JOIN orders o ON c.cust_id = o.cust_id AND o.amount > 400` → 7 rows, Vikram included,
and only his plus Ananya's 1002.

---

### Q2 — Answer **B** (the LEFT JOIN mental model)

**A manager asks for "all customers and the orders they placed". Which query is correct?**

- A. `SELECT c.cust_name, o.order_id FROM customers c JOIN orders o ON c.cust_id = o.cust_id;`
- B. `SELECT c.cust_name, o.order_id FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id;`
- C. `SELECT c.cust_name, o.order_id FROM orders o JOIN customers c ON c.cust_id = o.cust_id;`
- D. `SELECT c.cust_name, o.order_id FROM customers c CROSS JOIN orders o;`

**Solution**

"**All** customers" is the escape clause. The customers table goes on the left and unmatched
customers must survive → `LEFT JOIN`.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Drops Vikram. If the question had said "customers who have placed orders", A would be right |
| C | Same semantics as A — the table order does not change an inner join |
| D | 30 rows; every customer against every order |

---

### Q3 — Answer **A** (`COUNT(*)` vs `COUNT(col)` after a join)

**`SELECT COUNT(*), COUNT(o.order_id) FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id;`
returns what?**

- A. `7, 6`
- B. `5, 6`
- C. `6, 6`
- D. `7, 7`

**Solution**

- `COUNT(*)` counts every row of the join result: 6 matched + 1 NULL-padded = **7**.
- `COUNT(o.order_id)` skips NULLs: only the 6 matched rows have a non-NULL `order_id` → **6**.

**Answer: A (`7, 6`).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | `5` is the customer count — it ignores that the join fans out customers 101 and 104 into two rows each |
| C | `6` for both — this is the inner join result; a `LEFT JOIN` always adds the NULL-padded row |
| D | Assumes `COUNT(col)` counts NULLs |

---

### Q4 — Answer **D** (anti-join)

**Which query returns the customers who have never placed an order?**

- A. `SELECT c.cust_name FROM customers c JOIN orders o ON c.cust_id = o.cust_id WHERE o.order_id IS NULL;`
- B. `SELECT c.cust_name FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id WHERE o.order_id IS NULL;`
- C. `SELECT c.cust_name FROM customers WHERE cust_id NOT IN (SELECT cust_id FROM orders);`
- D. `SELECT c.cust_name FROM orders o LEFT JOIN customers c ON c.cust_id = o.cust_id WHERE c.cust_id IS NULL;`

**Solution**

- B works: the `LEFT JOIN` keeps Vikram with a NULL `order_id`, and `WHERE o.order_id IS NULL`
  selects exactly that row.
- A fails: an inner join never produces a row with a NULL `order_id`, so A returns **zero rows**.
- C fails on the NULL trap: the extended fixture has a row in `orders` with a NULL `cust_id`, so
  `NOT IN` returns zero rows. (Even without it, C is the fragile form.)
- D fails: it finds **orders without customers**, which is the other direction. On this fixture that
  is also zero rows.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | `JOIN` never yields NULL-padded rows, so `o.order_id IS NULL` matches nothing |
| C | The `NOT IN` + NULL trap, and the fragile form in general |
| D | Reverses the direction — finds orders with no customer |

---

### Q5 — Answer **B** (`NATURAL JOIN`)

**`SELECT * FROM customers NATURAL JOIN orders;` returns how many columns?**

- A. 7
- B. 6
- C. 5
- D. 8

**Solution**

`customers` has 3 columns (`cust_id`, `cust_name`, `city`); `orders` has 4 (`order_id`, `cust_id`,
`order_date`, `amount`). `NATURAL JOIN` joins on every same-named column — `cust_id` — and the
joined column appears **once** in the output.

3 + 4 − 1 = **6 columns**: `cust_id`, `cust_name`, `city`, `order_id`, `order_date`, `amount`.

**Answer: B (6).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | 3 + 4 = 7 — the count if `cust_id` appeared twice (which is what a plain `JOIN` with `SELECT *` gives) |
| C | Counts only the shared column plus something — wrong arithmetic |
| D | More columns than the two tables have in total |

**Bonus:** `NATURAL JOIN` is an inner join, so it returns 6 rows on this fixture.

---

### Q6 — Answer **A** (`RIGHT JOIN` direction)

**`SELECT c.cust_name, o.order_id FROM orders o RIGHT JOIN customers c ON o.cust_id = c.cust_id;`
returns how many rows?**

- A. 7
- B. 6
- C. 5
- D. 11

**Solution**

`RIGHT JOIN` keeps every row of the **right** table. The right table here is `customers` (5 rows).
The join matches 6 order rows to customers, and customer 105 has no order, so it appears once with
NULLs.

Row count = 6 matched + 1 unmatched customer = **7**.

**Answer: A (7).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | The inner join count — ignores that `RIGHT JOIN` keeps the customers table |
| C | The customer count — ignores the fan-out |
| D | 5 + 6 = 11, adding rows instead of matching them |

**Note:** `orders o RIGHT JOIN customers c` is exactly `customers c LEFT JOIN orders o`. Same
answer, but the second form is what you should write.

---

### Q7 — Answer **C** (`CROSS JOIN` size)

**`SELECT c.cust_name, o.order_id FROM customers c CROSS JOIN orders o;` returns how many rows?**

- A. 6
- B. 5
- C. 30
- D. 11

**Solution**

`CROSS JOIN` = every customer × every order = 5 × 6 = **30**.

**Answer: C (30).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | The inner join count |
| B | The customer count |
| D | 5 + 6 — the "add the tables" instinct |

---

### Q8 — Answer **B** (self-join)

**`SELECT e.emp_name AS employee, m.emp_name AS manager FROM employees e LEFT JOIN employees m ON e.manager_id = m.emp_id;`
— which pair appears in the output?**

- A. Karthik / Karthik
- B. Karthik / NULL
- C. Ananya / Ananya
- D. Karthik / Vikram

**Solution**

`manager_id` values: Ananya→4, Rahul→4, Meera→5, Karthik→NULL, Vikram→NULL, Anjali→5.

Employee 4 is **Karthik** and employee 5 is **Vikram**. So:

```
employee   manager
Ananya     Karthik
Rahul      Karthik
Meera      Vikram
Karthik    NULL      ← manager_id is NULL
Vikram     NULL      ← manager_id is NULL
Anjali     Vikram
```

**Answer: B (Karthik / NULL).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Karthik's `manager_id` is NULL, so he has no manager; he is not his own manager |
| C | Ananya's manager is employee 4 = Karthik, not Ananya |
| D | Vikram is employee 5, and Karthik's manager is NULL — the pair is reversed |

**Why `LEFT JOIN` and not `INNER JOIN`:** an inner join would drop Karthik and Vikram, losing the
top of the hierarchy — exactly the rows a "who is at the top" report needs.

---

### Q9 — Answer **D** (many-to-many via a junction table)

**`students`, `courses` and `enrollments` hold: Ananya→{DBMS, Java}, Rahul→{Java}, Meera→{SQL,
DBMS}. How many rows does
`SELECT s.student_name, c.course_name FROM students s JOIN enrollments e ON e.student_id = s.student_id JOIN courses c ON c.course_id = e.course_id;`
return?**

- A. 3
- B. 4
- C. 5
- D. 6

**Solution**

The result has **one row per enrolment**: Ananya 2 + Rahul 1 + Meera 2 = **5 rows**.

**Answer: C (5).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | The number of students |
| B | The number of distinct courses (DBMS, Java, SQL) + 1 |
| D | The number of students + courses − 1, a coincidence-style guess |

**Trap:** students do not join directly to courses. The junction table `enrollments` is what makes
the many-to-many possible, and the row count of the join equals the number of junction rows, not
the number of students or courses.

## Quick rules

- Trace on paper. Write the joined rows, then count.
- `LEFT JOIN` + `WHERE right IS NULL` = "left rows with no match".
- `WHERE right.col = x` on a `LEFT JOIN` = inner join.
- `COUNT(*)` counts join rows; `COUNT(right.col)` counts matches.
- `NATURAL JOIN` on the fixture → 6 columns, 6 rows.
- `CROSS JOIN` on the fixture → 30 rows.
- Self-join on `employees` → Karthik and Vikram have NULL managers.
- Many-to-many row count = number of junction rows.

## Common traps

| Trap | Wrong answer | Right answer | Option |
|---|---|---|---|
| `LEFT JOIN` + `WHERE` on the right table | 6 | 5 (the NULL row is filtered) | B vs C |
| "all customers" → INNER | A | `LEFT JOIN` | A vs B |
| `COUNT(*)` after join | 6 | 7 | C vs A |
| Anti-join with `JOIN` | A | `LEFT JOIN` + `IS NULL` | A vs B |
| `NATURAL JOIN` column count | 7 | 6 | A vs B |
| `RIGHT JOIN` direction | 6 | 7 | B vs A |
| `CROSS JOIN` size | 6 | 30 | A vs C |
| Many-to-many row count | 3 | 5 | A vs C |

## Checklist

- [ ] I wrote the intermediate joined rows before counting.
- [ ] I checked whether a `WHERE` condition nullified the `LEFT JOIN`.
- [ ] I used `COUNT(col)` when counting matches.
- [ ] I read the table order in `RIGHT JOIN`.
- [ ] I confirmed the join column count for `NATURAL JOIN`.
- [ ] I counted junction rows for many-to-many questions.

## Related

- [The six joins](../01-concepts/01-the-six-joins.md)
- [Join decision table](../02-techniques/01-join-decision-table.md)
- [Join traps](../04-pitfalls/01-join-traps.md)
- [Join reference sheet](../05-reference/01-join-reference-sheet.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
