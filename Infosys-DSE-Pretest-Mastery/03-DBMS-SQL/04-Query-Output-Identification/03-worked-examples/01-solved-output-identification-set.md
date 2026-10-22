# Query Output Identification — 8 Solved Questions

> Section 3 · DBMS & SQL · Query Output Identification · _Estimated reading time: 13 min_
> **Prerequisite:** [Trace procedures](../02-techniques/01-trace-procedures.md)

## In one sentence

Eight output questions, each traced on paper through the five stages, with the option that each
wrong reading produces.

## Why the pre-test tests this

- "Identify the output of the given SQL query" is 2 of the 10 DBMS questions.
- Every question below is deterministic: the fixture is stated in full, so you can reproduce it on
  any SQL engine.
- The whole point is that the answer is decided by the **trace**, not by how the SQL "feels".

## Core concept

### The fixture — run this before you start

```sql
CREATE TABLE customers (
  cust_id   INT PRIMARY KEY,
  cust_name VARCHAR(30),
  city      VARCHAR(20)
);
INSERT INTO customers VALUES
  (101, 'Ananya',  'Pune'),
  (102, 'Rahul',   'Chennai'),
  (103, 'Meera',   'Pune'),
  (104, 'Karthik', 'Delhi'),
  (105, 'Vikram',  'Bengaluru');

CREATE TABLE orders (
  order_id   INT PRIMARY KEY,
  cust_id    INT,
  order_date DATE,
  amount     DECIMAL(10,2)
);
INSERT INTO orders VALUES
  (1001, 101, '2026-01-05', 500.00),
  (1002, 101, '2026-01-09', 750.00),
  (1003, 102, '2026-02-11', 1200.00),
  (1004, 103, '2026-02-14', 300.00),
  (1005, 104, '2026-03-02', 950.00),
  (1006, 104, '2026-03-03', 1100.00);
```

**Facts to hold in your head:** 5 customers, 6 orders, total order value **4800.00**, customer 105
has no orders, customers 101 and 104 have two orders each, cities are Pune ×2, Chennai, Delhi,
Bengaluru.

### The scratch pad

```
STAGE 1  FROM+JOIN  →  rows: ____
STAGE 2  WHERE      →  rows: ____
STAGE 3  GROUP BY   →  groups: ____
STAGE 4  HAVING     →  groups: ____
STAGE 5  SELECT     →  output: ____
```

## Worked example

### Q1 — Answer **B** (join row count)

**What does `SELECT COUNT(*) FROM customers c JOIN orders o ON c.cust_id = o.cust_id;` return?**

- A. 5
- B. 6
- C. 7
- D. 30

**Trace**

| Stage | Result |
|---|---|
| 1 `FROM` + inner join | Each order matches exactly one customer → **6 rows** |
| 2–4 | No `WHERE`, no `GROUP BY`, no `HAVING` |
| 5 `COUNT(*)` | One aggregate row, no `GROUP BY` → **1 row** containing 6 |

**Answer: B (6).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | 5 = the number of **customers**. `COUNT(*)` counts join rows, not entities. Customer 105 has no order and customers 101 and 104 each contribute 2 rows, so 5 ≠ 6 |
| C | 7 = the `LEFT JOIN` row count. The join is an inner join, so Vikram is dropped |
| D | 30 = the cartesian product 5 × 6. The `ON` clause filters it down to 6 |

---

### Q2 — Answer **A** (`LEFT JOIN` + `WHERE`)

**What does
`SELECT c.cust_name, o.amount FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id WHERE o.amount > 400;`
return?**

- A. 5 rows
- B. 6 rows
- C. 7 rows
- D. 30 rows

**Trace**

| Stage | Result |
|---|---|
| 1 `LEFT JOIN` | 7 rows (6 matched + Vikram with NULLs) |
| 2 `WHERE o.amount > 400` | Keeps 500, 750, 1200, 950, 1100 → **5 rows**. Meera's 300 is out; **Vikram is out** because `NULL > 400` is `UNKNOWN` |
| 3–5 | No group, no aggregate → 5 output rows |

**Answer: A (5 rows).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | 6 = the inner-join count. The `WHERE` deleted the NULL-padded row, so the `LEFT JOIN` behaved like an inner join |
| C | 7 = the `LEFT JOIN` count **before** the `WHERE`. The exam's favourite trap |
| D | 30 = the cartesian product |

---

### Q3 — Answer **A** (`GROUP BY` collapses)

**What does
`SELECT c.cust_name, COUNT(*) FROM customers c JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_name;`
return?**

- A. 4 rows
- B. 5 rows
- C. 6 rows
- D. 7 rows

**Trace**

| Stage | Result |
|---|---|
| 1 inner join | 6 rows |
| 2 | No `WHERE` → 6 rows |
| 3 `GROUP BY c.cust_name` | Distinct names among the 6 rows: Ananya, Rahul, Meera, Karthik → **4 groups** (Ananya has 2 orders, Karthik has 2) |
| 4 | No `HAVING` |
| 5 | 4 output rows: Ananya 2, Rahul 1, Meera 1, Karthik 2 |

**Answer: A (4 rows).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | 5 = the customer count including Vikram — but Vikram has no order, so no inner-join row mentions him |
| C | 6 = the join row count before grouping |
| D | 7 = the `LEFT JOIN` row count |

---

### Q4 — Answer **B** (`HAVING` on an aggregate)

**What does
`SELECT c.cust_name, COUNT(*) AS n FROM customers c JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_name HAVING COUNT(*) > 1;`
return?**

- A. 1 row
- B. 2 rows
- C. 3 rows
- D. 4 rows

**Trace**

| Stage | Result |
|---|---|
| 1 inner join | 6 rows |
| 3 `GROUP BY c.cust_name` | 4 groups: Ananya(2), Rahul(1), Meera(1), Karthik(2) |
| 4 `HAVING COUNT(*) > 1` | Drops Rahul(1) and Meera(1) → **2 groups**: Ananya, Karthik |
| 5 | 2 output rows |

**Answer: B (2 rows).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | 1 = the number of groups with exactly one order if the comparison were `= 1`. The `> 1` filter keeps the groups with **two** orders, which is the opposite end of the distribution |
| C | 3 = the number of groups before the `HAVING` filter (Ananya, Rahul, Karthik) |
| D | 4 = the number of groups before `HAVING`, if you had grouped on `cust_id` including Vikram |

---

### Q5 — Answer **A** (`SUM` over a `LEFT JOIN`)

**What does `SELECT SUM(o.amount) FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id;`
return?**

- A. 4800.00
- B. 4500.00
- C. 3600.00
- D. NULL

**Trace**

| Stage | Result |
|---|---|
| 1 `LEFT JOIN` | 7 rows (6 with amounts, 1 with NULL) |
| 5 `SUM(o.amount)` | `SUM` skips NULLs → 500 + 750 + 1200 + 300 + 950 + 1100 = **4800.00** |

**Answer: A (4800.00).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | 4500 = 4800 − 300, i.e. dropping Meera's order of 300.00 |
| C | 3600 = 4800 − 1200, i.e. dropping Rahul's order of 1200.00 |
| D | `SUM` over a group with no non-NULL values is `NULL`, but this group has 6 non-NULL amounts |

---

### Q6 — Answer **B** (`DISTINCT` applies to the whole row)

**What does `SELECT DISTINCT c.city FROM customers c JOIN orders o ON c.cust_id = o.cust_id;`
return?**

- A. 3 rows
- B. 4 rows
- C. 5 rows
- D. 6 rows

**Trace**

| Stage | Result |
|---|---|
| 1 inner join | 6 rows with cities: Pune, Pune, Chennai, Pune, Delhi, Delhi |
| 5 `DISTINCT` | Unique cities: Pune, Chennai, Delhi → **3 rows** |

**Answer: A (3 rows).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | 4 = the number of distinct cities in the **customers** table (Bengaluru included) — but Bengaluru has no orders, so it never reaches the output |
| C | 5 = the customer count |
| D | 6 = the join row count — `DISTINCT` removed the duplicate Pune and Delhi rows |

---

### Q7 — Answer **D** (`ORDER BY` + `LIMIT`)

**What does
`SELECT c.cust_name FROM customers c JOIN orders o ON c.cust_id = o.cust_id ORDER BY o.amount DESC LIMIT 2;`
return?**

- A. Ananya, Karthik
- B. Rahul, Ananya
- C. Rahul, Karthik
- D. Karthik, Rahul

**Trace**

| Stage | Result |
|---|---|
| 1 inner join | 6 rows: Ananya 500, Ananya 750, Rahul 1200, Meera 300, Karthik 950, Karthik 1100 |
| 5 `ORDER BY o.amount DESC` | 1200 (Rahul), 1100 (Karthik), 950 (Karthik), 750 (Ananya), 500 (Ananya), 300 (Meera) |
| 5 `LIMIT 2` | Rahul, Karthik |

**Answer: C (Rahul, Karthik).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Ananya's orders are 500 and 750 — she is not in the top 2. The trap for candidates who total per customer |
| B | Ananya is 4th and 5th by individual order amount. The trap for candidates who think in totals (Ananya's total is 1250, second) but then mis-order |
| D | The right pair in the **wrong order** — 1200 > 1100, so Rahul comes first |

---

### Q8 — Answer **A** (`WHERE` + `GROUP BY` + `HAVING` together)

**What does
`SELECT c.cust_name FROM customers c JOIN orders o ON c.cust_id = o.cust_id WHERE o.amount > 400 GROUP BY c.cust_name HAVING COUNT(*) > 1;`
return?**

- A. Ananya, Karthik
- B. Ananya, Rahul, Karthik
- C. Ananya, Meera, Karthik
- D. Ananya, Karthik, Rahul

**Trace**

| Stage | Result |
|---|---|
| 1 inner join | 6 rows |
| 2 `WHERE o.amount > 400` | Ananya 500, Ananya 750, Rahul 1200, Karthik 950, Karthik 1100 → **5 rows** (Meera 300 out) |
| 3 `GROUP BY c.cust_name` | Ananya(2), Rahul(1), Karthik(2) → **3 groups** |
| 4 `HAVING COUNT(*) > 1` | Drops Rahul(1) → **2 groups** |
| 5 | Ananya, Karthik |

**Answer: A (Ananya, Karthik).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | Rahul has only **one** order, so `COUNT(*) > 1` excludes him |
| C | Meera's order (300) was removed by the `WHERE` — she is not in the result at all |
| D | Same rows as B in a different order — still includes Rahul |

**The key insight:** `WHERE` decides which *orders* count; `HAVING` decides which *customers*
survive. Move the `WHERE` into the `HAVING` (`HAVING COUNT(*) > 1 AND SUM(o.amount) > 400`) and you
get a different question with a different answer.

---

### Q9 — Answer **B** (self-join, `LEFT JOIN` keeps the top)

**What does
`SELECT e.emp_name, m.emp_name FROM employees e LEFT JOIN employees m ON e.manager_id = m.emp_id;`
return, and how many rows?**

The `employees` table: (1, Ananya, dept 10, 60000, mgr 4), (2, Rahul, 10, 45000, mgr 4),
(3, Meera, 20, 90000, mgr 5), (4, Karthik, 10, 120000, mgr NULL), (5, Vikram, 20, 110000, mgr NULL),
(6, Anjali, 30, 50000, mgr 5).

- A. 4 rows
- B. 6 rows
- C. 8 rows
- D. 12 rows

**Trace**

| Stage | Result |
|---|---|
| 1 `LEFT JOIN` | Every employee row survives: 6 rows. Manager 4 = Karthik, manager 5 = Vikram; employees 4 and 5 have no manager → NULL |
| 5 | Ananya/Karthik, Rahul/Karthik, Meera/Vikram, Karthik/NULL, Vikram/NULL, Anjali/Vikram |

**Answer: B (6 rows).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | 4 = the rows where a manager exists. An inner join would give 4 (Ananya, Rahul, Meera, Anjali) |
| C | 8 = double-counting: every employee matched to both managers |
| D | 12 = the cartesian product of 6 × 2 possible managers |

## Quick rules

- Trace stage 1 and write the rows down.
- After a join, count rows — 6 for an inner join on this fixture, 7 for a left join from
  `customers`.
- `WHERE` kills the NULL-padded row of a `LEFT JOIN`.
- `GROUP BY` collapses to the number of distinct group keys; `HAVING` then cuts groups.
- `SUM`/`COUNT` skip NULLs; `COUNT(*)` does not.
- `DISTINCT` applies to the whole row.
- `ORDER BY` + `LIMIT`: sort first, and check for ties.
- At 70 seconds with no clean trace: guess and move.

## Common traps

| Trap | Wrong option here | Right answer |
|---|---|---|
| Counting entities, not join rows | A in Q1 | B (6) |
| `WHERE` kills the `LEFT JOIN` | C in Q2 | A (5) |
| Forgetting `GROUP BY` collapses rows | C in Q3 | A (4) |
| Ignoring `HAVING` | D in Q4 | B (2) |
| `DISTINCT` on one column | B in Q6 | A (3) |
| `LIMIT` before sorting | D in Q7 | C |
| `WHERE` instead of `HAVING` | B in Q8 | A |

## Checklist

- [ ] I wrote the stage-1 rows on paper before reading the options.
- [ ] I predicted the answer shape.
- [ ] I marked the NULL rows and applied the `WHERE` to them explicitly.
- [ ] I applied `HAVING` to groups, not rows.
- [ ] I checked `COUNT(*)` vs `COUNT(col)` and `DISTINCT` semantics.
- [ ] I checked whether `ORDER BY` ties make the order undefined.
- [ ] I marked and moved if I passed 70 seconds.

## Related

- [The five-step execution model](../01-concepts/01-five-step-execution-model.md)
- [Trace procedures](../02-techniques/01-trace-procedures.md)
- [Output identification traps](../04-pitfalls/01-output-identification-traps.md)
- [Output identification reference](../05-reference/01-output-identification-reference.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
