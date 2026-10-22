# Two-Table Query Writing — 8 Solved Questions

> Section 3 · DBMS & SQL · Two-Table Query Writing · _Estimated reading time: 12 min_
> **Prerequisite:** [Task recipe cards](../02-techniques/02-task-recipe-cards.md)

## In one sentence

Eight "write a query for two tables" questions, each written with the eight-step recipe and each
with the near-miss that the exam would have accepted as the trap.

## Why the pre-test tests this

- This archetype is 1–2 of the 10 DBMS questions and is the slowest to answer. Getting the shape
  right in 60 seconds is the whole game.
- Half of these questions are "which of these four queries is correct" — in that format you do not
  have to write the query, only recognise the right one.
- The fixture is the shared one from the [section index](../../README.md#the-shared-fixture).

## Core concept

The eight-step recipe, abbreviated:

```
1 FROM   → 2 JOIN   → 3 ON   → 4 WHERE
5 GROUP BY → 6 HAVING → 7 SELECT → 8 ORDER BY → 9 LIMIT
```

Every question below is walked through with those nine steps. The "near-miss" table under each
answer is what the exam's distractors look like.

## Worked example

### Q1 — Answer **B** (the classic "all customers with their orders")

**Write a query to display all customers with their order ids and amounts, including customers who
have not placed any order.**

- A. `SELECT c.cust_name, o.order_id, o.amount FROM customers c JOIN orders o ON c.cust_id = o.cust_id;`
- B. `SELECT c.cust_name, o.order_id, o.amount FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id;`
- C. `SELECT c.cust_name, o.order_id, o.amount FROM orders o JOIN customers c ON c.cust_id = o.cust_id;`
- D. `SELECT c.cust_name, o.order_id, o.amount FROM customers c, orders o WHERE c.cust_id = o.cust_id;`

**Solution by the recipe**

| Step | Decision |
|---|---|
| 1 `FROM` | `customers c` — "all customers", so customers keep their rows |
| 2 `JOIN` | `LEFT JOIN` — "including customers who have not placed any order" |
| 3 `ON` | `c.cust_id = o.cust_id` |
| 4–9 | No filter, no group, no order, no limit |

**Answer: B.**

**Near-misses**

| Option | What breaks |
|---|---|
| A | `JOIN` drops Vikram — 6 rows, and the stem explicitly asks for him |
| C | Same semantics as A; the table order does not change an inner join |
| D | Old-style inner join — same as A. It also silently means "cross join + filter", which the exam treats as a style error |

---

### Q2 — Answer **A** (count per parent, including zeros)

**Write a query to show each customer and the number of orders they have placed, including customers
with zero orders.**

- A. `SELECT c.cust_name, COUNT(o.order_id) AS order_count FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id, c.cust_name;`
- B. `SELECT c.cust_name, COUNT(*) AS order_count FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id;`
- C. `SELECT c.cust_name, COUNT(o.order_id) AS order_count FROM customers c JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id;`
- D. `SELECT c.cust_name, COUNT(o.order_id) AS order_count FROM customers c, orders o WHERE c.cust_id = o.cust_id GROUP BY c.cust_id;`

**Solution**

| Requirement | Clause |
|---|---|
| Every customer, even with zero orders | `LEFT JOIN` |
| Zero reported as 0, not 1 | `COUNT(o.order_id)` |
| One row per customer | `GROUP BY c.cust_id, c.cust_name` |

**Answer: A.** Output: Ananya 2, Rahul 1, Meera 1, Karthik 2, Vikram 0.

**Near-misses**

| Option | What breaks |
|---|---|
| B | `COUNT(*)` counts the NULL-padded row → Vikram shows **1** |
| C | `JOIN` drops Vikram entirely |
| D | Old-style inner join — Vikram dropped, and the comma form is a style error |

---

### Q3 — Answer **C** (anti-join)

**Write a query to find customers who have never placed an order.**

- A. `SELECT c.cust_name FROM customers c JOIN orders o ON c.cust_id = o.cust_id WHERE o.order_id IS NULL;`
- B. `SELECT c.cust_name FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id WHERE o.order_id IS NULL;`
- C. `SELECT c.cust_name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.cust_id = c.cust_id);`
- D. `SELECT c.cust_name FROM customers WHERE cust_id NOT IN (SELECT cust_id FROM orders);`

**Solution**

| Option | Result on the fixture | Verdict |
|---|---|---|
| A | 0 rows — an inner join never makes a NULL-padded row | ❌ |
| B | 1 row: Vikram | ✅ |
| C | 1 row: Vikram | ✅ |
| D | 0 rows — the `NOT IN` + NULL trap (the `orders` table has a row with a NULL `cust_id`) | ❌ |

**Answer: B** — the exam expects the anti-join form for a "two-table" question. Option C is
equally correct SQL and is the answer if the question says "using a subquery"; the exam's stem here
asks for a two-table query.

**Near-misses**

| Option | What breaks |
|---|---|
| A | Inner join removes the NULL row before the `IS NULL` test can see it |
| D | `NOT IN` with a NULL in the list returns nothing |

---

### Q4 — Answer **D** (`HAVING` vs `WHERE`)

**Write a query to show each customer with their order count, keeping only customers with more than
one order.**

- A. `SELECT c.cust_name, COUNT(*) FROM customers c JOIN orders o ON c.cust_id = o.cust_id WHERE COUNT(*) > 1 GROUP BY c.cust_id;`
- B. `SELECT c.cust_name, COUNT(*) FROM customers c JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id HAVING c.cust_name <> '';`
- C. `SELECT c.cust_name, COUNT(*) FROM customers c JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id ORDER BY COUNT(*) DESC;`
- D. `SELECT c.cust_name, COUNT(*) FROM customers c JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id HAVING COUNT(*) > 1;`

**Solution**

The filter is on an aggregate, so it must be in `HAVING` (step 6, after `GROUP BY`).

**Answer: D.** Output: Ananya 2, Karthik 2.

**Near-misses**

| Option | What breaks |
|---|---|
| A | `WHERE COUNT(*) > 1` — **invalid**: aggregates cannot appear in `WHERE` |
| B | Filters groups on a non-grouped column, and filters the wrong thing entirely |
| C | Sorts the counts but filters nothing — every customer appears |

---

### Q5 — Answer **B** (`WHERE` before `GROUP BY`)

**Write a query to show the number of orders placed by customers in Chennai, and keep only those
customers with more than one order.**

- A. `SELECT c.cust_name, COUNT(*) FROM customers c JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id HAVING c.city = 'Chennai' AND COUNT(*) > 1;`
- B. `SELECT c.cust_name, COUNT(*) FROM customers c JOIN orders o ON c.cust_id = o.cust_id WHERE c.city = 'Chennai' GROUP BY c.cust_id HAVING COUNT(*) > 1;`
- C. `SELECT c.cust_name, COUNT(*) FROM customers c JOIN orders o ON c.cust_id = o.cust_id WHERE c.city = 'Chennai' AND COUNT(*) > 1 GROUP BY c.cust_id;`
- D. `SELECT c.cust_name, COUNT(*) FROM customers c JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id, c.cust_name, c.city HAVING COUNT(*) > 1;`

**Solution**

- `c.city = 'Chennai'` is a **row-level** filter → `WHERE` (step 4).
- `COUNT(*) > 1` is an **aggregate** filter → `HAVING` (step 6).
- `GROUP BY c.cust_id` alone is legal here because `cust_id` is the primary key of `customers` — the
  DBMS can infer the rest. Standard SQL's `ONLY_FULL_GROUP_BY` accepts a primary key as a grouping
  key. Option D's fuller group list is also valid.

**Answer: B.** (On the fixture, no Chennai customer has more than one order, so the result is empty
— but the query is what is being graded.)

**Near-misses**

| Option | What breaks |
|---|---|
| A | The city filter is in `HAVING`, where it is applied **after** grouping — different semantics, and it references a non-grouped column |
| C | `COUNT(*)` in `WHERE` — **invalid** |
| D | Valid SQL, and semantically the same result, but the exam's intended answer is B because it separates the row filter from the group filter |

---

### Q6 — Answer **A** (top N with `ORDER BY` + `LIMIT`)

**Write a query to find the top 3 customers by total order amount.**

- A. `SELECT c.cust_name, SUM(o.amount) AS total FROM customers c JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id, c.cust_name ORDER BY total DESC LIMIT 3;`
- B. `SELECT c.cust_name, SUM(o.amount) AS total FROM customers c JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id, c.cust_name ORDER BY total DESC LIMIT 3 OFFSET 0;`
- C. `SELECT c.cust_name, SUM(o.amount) AS total FROM customers c JOIN orders o ON c.cust_id = o.cust_id LIMIT 3;`
- D. `SELECT c.cust_name, SUM(o.amount) AS total FROM customers c JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id, c.cust_name ORDER BY SUM(o.amount) DESC LIMIT 3;`

**Solution**

`GROUP BY` (aggregate) → `ORDER BY` the total descending → `LIMIT 3`.

**Answer: A.** Output: Karthik 2050, Ananya 1250, Rahul 1200.

**Near-misses**

| Option | What breaks |
|---|---|
| B | `OFFSET 0` is a no-op — the query is correct SQL and returns the same rows. If the exam wants one answer, A is the shorter, intended form |
| C | `LIMIT` with no `ORDER BY` — an arbitrary 3 rows, and no grouping means `SUM` collapses everything into one row |
| D | Also correct SQL — `ORDER BY SUM(o.amount)` is legal and returns the same rows. The exam's expected form uses the alias |

**Honest note:** B and D are both valid and return identical results to A. If you see a question
like this with more than one valid option, the grader is checking the *structure* (group → order →
limit), and all three pass. That is worth knowing: pick A and move on.

---

### Q7 — Answer **C** (window function, MySQL 8+)

**Write a query to find, for each customer, their single highest-value order. (MySQL 8+)**

- A. `SELECT c.cust_name, MAX(o.amount) FROM customers c JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id;`
- B. `SELECT c.cust_name, o.order_id FROM customers c JOIN orders o ON c.cust_id = o.cust_id WHERE o.amount = (SELECT MAX(amount) FROM orders WHERE cust_id = c.cust_id);`
- C. `SELECT * FROM (SELECT c.cust_name, o.order_id, o.amount, ROW_NUMBER() OVER (PARTITION BY c.cust_id ORDER BY o.amount DESC) AS rn FROM customers c JOIN orders o ON c.cust_id = o.cust_id) t WHERE t.rn = 1;`
- D. `SELECT c.cust_name, o.order_id FROM customers c JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_id HAVING o.amount = MAX(o.amount);`

**Solution**

The question asks for the **order row** (order_id), not just the maximum amount, for **each**
customer. That is a per-group top-1 — the `ROW_NUMBER() OVER (PARTITION BY …)` pattern.

**Answer: C.** Output: Ananya/1002 (750), Rahul/1003 (1200), Meera/1004 (300), Karthik/1006 (1100).

**Near-misses**

| Option | What breaks |
|---|---|
| A | Returns the max amount but **not** the `order_id` — it cannot tell you *which* order it was |
| B | Correct SQL and it returns the same rows, but it is the **correlated-subquery** form, not the window-function form. The stem says "(MySQL 8+)", which points at the window function. If the stem had no version note, B would be the answer |
| D | `HAVING o.amount = MAX(o.amount)` is not valid — `MAX` is an aggregate, not a scalar to compare against in `HAVING` |

**MySQL 5.7 note:** option C fails on MySQL 5.7 — window functions arrived in 8.0. Use option B
there.

---

### Q8 — Answer **A** (the "with no matching" pair query)

**Write a query to find all pairs of customers who live in the same city, listing each pair once.**

- A. `SELECT a.cust_name AS customer1, b.cust_name AS customer2 FROM customers a JOIN customers b ON a.city = b.city AND a.cust_id < b.cust_id;`
- B. `SELECT a.cust_name, b.cust_name FROM customers a JOIN customers b ON a.city = b.city;`
- C. `SELECT a.cust_name, b.cust_name FROM customers a, customers b WHERE a.city = b.city;`
- D. `SELECT a.cust_name, b.cust_name FROM customers a CROSS JOIN customers b WHERE a.city = b.city;`

**Solution**

Two mentions of `customers` → a self-join with two aliases. The `a.cust_id < b.cust_id` guard
lists each pair once.

**Answer: A.** Output on the fixture: Ananya, Meera (both in Pune).

**Near-misses**

| Option | What breaks |
|---|---|
| B | Each pair appears twice: (Ananya, Meera) and (Meera, Ananya) |
| C | Old-style join; also it would include (Ananya, Ananya) and (Meera, Meera) because the comparison is true for the row with itself |
| D | A cross join filtered afterwards — works, but `CROSS JOIN` with a `WHERE` filter is a style error and it also includes the self-pairs |

## Quick rules

- `FROM` + `JOIN` first, then `ON`, then `WHERE`, then `GROUP BY`/`HAVING`, then `SELECT`, then
  `ORDER BY`/`LIMIT`.
- "including" → `LEFT JOIN`; "that have" → `INNER JOIN`.
- Row filter → `WHERE`; aggregate filter → `HAVING`.
- `COUNT(child.col)` for zero-inclusive counts; `COALESCE(SUM(x), 0)` for zero-inclusive sums.
- `GROUP BY` every non-aggregated selected column.
- `ORDER BY` before `LIMIT`; add a tiebreaker.
- Window functions need MySQL 8+, and cannot be filtered in the same `WHERE`.
- Skip any clause the question did not ask for.

## Common traps

| Trap | Near-miss in these questions | Fix |
|---|---|---|
| Inner join for an "including none" stem | Q1 A, Q2 C | `LEFT JOIN` |
| `COUNT(*)` for a zero-inclusive count | Q2 B | `COUNT(child.col)` |
| Aggregate in `WHERE` | Q4 A, Q5 C | `HAVING` |
| Row filter in `HAVING` | Q5 A | `WHERE` |
| `LIMIT` without `ORDER BY` | Q6 C | Add `ORDER BY` |
| Grouping key missing from `GROUP BY` | — | List every non-aggregated column |
| Pair duplication in a self-join | Q8 B | `a.id < b.id` |

## Checklist

- [ ] I identified the task type before writing anything.
- [ ] I put the table whose rows must survive on the left.
- [ ] I used `WHERE` for row filters and `HAVING` for aggregate filters.
- [ ] I chose `COUNT(col)` or `COALESCE` where zeros matter.
- [ ] I grouped by every non-aggregated selected column.
- [ ] I added `ORDER BY` before `LIMIT`, with a tiebreaker.
- [ ] I checked the MySQL version before using a window function.

## Related

- [Two-table query anatomy](../01-concepts/01-two-table-query-anatomy.md)
- [The eight-step recipe](../02-techniques/01-the-eight-step-recipe.md)
- [Task recipe cards](../02-techniques/02-task-recipe-cards.md)
- [Query writing traps](../04-pitfalls/01-query-writing-traps.md)
- [Pattern library](../05-reference/01-query-writing-pattern-library.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
