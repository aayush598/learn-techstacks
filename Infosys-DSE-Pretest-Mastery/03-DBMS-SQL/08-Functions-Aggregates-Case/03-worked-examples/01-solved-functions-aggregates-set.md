# Functions and Aggregates — 9 Solved Questions

> Section 3 · DBMS & SQL · Functions, Aggregates & CASE · _Estimated reading time: 12 min_
> **Prerequisite:** [Function selection procedures](../02-techniques/01-function-selection-procedures.md)

## In one sentence

Nine function questions — counts, trimming, rounding, `CASE`, window functions, string aggregation —
each solved by matching the verb.

## Why the pre-test tests this

- Functions are the most common single-archetype question in DBMS sections, because the answer is
  always a name.
- The distractors are real functions used in the wrong place. Precision is the skill.

## Core concept

### The fixture used in this set

```
customers(cust_id, cust_name, city)
  101 Ananya  Pune
  102 Rahul   Chennai
  103 Meera   Pune
  104 Karthik Delhi
  105 Vikram  Bengaluru

orders(order_id, cust_id, order_amt)
  1001 101 500
  1002 101 750
  1003 102 1200
  1004 103 300
  1005 104 950
  1006 104 1100
```

Total order value = **4800**. Distinct customers in `orders` = **4**.

## Worked example

### Q1 — Answer **C** (`COUNT(DISTINCT cust_id)`)

**How many distinct customers have placed at least one order?**

- A. `COUNT(*)` over `orders`
- B. `COUNT(cust_id)` over `orders`
- C. `COUNT(DISTINCT cust_id)` over `orders`
- D. `COUNT(cust_id)` over `customers`

**Solution**

"Distinct customers who have placed an order" — you need the distinct count of `cust_id` within
`orders`. The `cust_id` values are 101, 101, 102, 103, 104, 104 → distinct = **4**.

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | `COUNT(*)` counts **rows** — 6, not distinct customers |
| B | `COUNT(cust_id)` counts non-NULL values — also 6. It ignores duplicates |
| D | Counting over `customers` gives 5, and it includes Vikram, who has **no** orders. The question asks for customers who have placed an order |

---

### Q2 — Answer **B** (6 rows)

**`SELECT COUNT(*) FROM orders;` returns:**

- A. 4
- B. 6
- C. 5
- D. 7

**Solution**

`COUNT(*)` counts **rows**. The `orders` table has 6 rows. It does not count customers, and it does
not care whether any column is NULL.

**Answer: B (6).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | 4 is the number of **distinct customers** in `orders` |
| C | 5 is the number of rows in `customers` |
| D | 7 is the number of rows you get from `customers LEFT JOIN orders` |

---

### Q3 — Answer **C** (`COALESCE`)

**You want to display `city`, but show `'Unknown'` when `city` is NULL. Which expression is
correct?**

- A. `COALESCE(city, 'Unknown')`
- B. `NULLIF(city, 'Unknown')`
- C. `IFNULL(city, 'Unknown')`
- D. `CASE WHEN city = NULL THEN 'Unknown' ELSE city END`

**Solution**

`COALESCE` returns the **first non-NULL** argument, so `COALESCE(city, 'Unknown')` gives exactly
the required result.

**Answer: A.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | `NULLIF(a, b)` returns `NULL` when `a = b`, otherwise `a`. It does **not** replace a NULL with a value |
| C | `IFNULL` is MySQL's two-argument `COALESCE` and also works — but the **portable standard SQL** answer is `COALESCE`. If the question names MySQL explicitly, `IFNULL` is acceptable too |
| D | `city = NULL` is never true. The correct NULL test is `city IS NULL`. As written, the `CASE` always takes the `ELSE` branch and never shows `'Unknown'` |

---

### Q4 — Answer **A** (`TRUNC`)

**Which function returns `2` for the input `2.7`?**

- A. `TRUNC(2.7)`
- B. `ROUND(2.7)`
- C. `CEIL(2.7)`
- D. `FLOOR(2.7)`

**Solution**

| Function | Result on 2.7 |
|---|---|
| `TRUNC(2.7)` | **2** — cuts off the decimal part |
| `ROUND(2.7)` | 3 — rounds to the nearest integer |
| `CEIL(2.7)` | 3 — rounds up |
| `FLOOR(2.7)` | 2 — rounds down |

**Answer: A.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | `ROUND` rounds to the nearest integer, giving 3 |
| C | `CEIL` rounds up, giving 3 |
| D | `FLOOR` also gives 2 — but `FLOOR` rounds down to the nearest integer, which is not the same rule as `TRUNC` for negatives (`FLOOR(-2.7)` = -3, `TRUNC(-2.7)` = -2). The precise answer is `TRUNC` |

---

### Q5 — Answer **B** (`HAVING`)

**Which clause filters groups whose total order value exceeds 1000?**

- A. `WHERE`
- B. `HAVING`
- C. `GROUP BY`
- D. `ORDER BY`

**Solution**

Filtering on a **group total** means filtering after grouping. Only `HAVING` runs after grouping.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | `WHERE` runs **before** grouping, so it cannot see `SUM(order_amt)` |
| C | `GROUP BY` defines the buckets, it does not filter them |
| D | `ORDER BY` sorts |

---

### Q6 — Answer **D** (5 rows, one group per customer)

**`SELECT cust_id, COUNT(*) FROM orders GROUP BY cust_id;` returns how many rows?**

- A. 6
- B. 4
- C. 1
- D. 5

**Solution**

`GROUP BY cust_id` creates one group per **distinct** `cust_id` present in `orders`. The customers
who have orders are 101, 102, 103 and 104 — that is **4** distinct values, so 4 output rows.

**Answer: B (4 rows).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | 6 is the number of **orders**, before grouping |
| C | 1 row is what you get with an aggregate and **no** `GROUP BY` |
| D | 5 is the number of customers in the `customers` table, including Vikram who has no order. He never appears in `orders`, so he is not a group |

---

### Q7 — Answer **C** (`ROW_NUMBER`)

**Which window function numbers rows 1, 2, 3, 4 with no ties and no gaps, even when two rows have
identical ordering values?**

- A. `RANK()`
- B. `DENSE_RANK()`
- C. `ROW_NUMBER()`
- D. `LAG()`

**Solution**

`ROW_NUMBER()` produces consecutive integers and **never ties**. `RANK()` and `DENSE_RANK()` both
give tied rows the same number, and `RANK()` skips after a tie. `LAG()` returns a value from a
previous row — it does not number rows.

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | `RANK()` produces 1, 2, 2, 4 on ties — gaps appear |
| B | `DENSE_RANK()` produces 1, 2, 2, 3 — no gaps, but ties still share a number |
| D | `LAG()` returns the value from `n` rows earlier, not a row number |

---

### Q8 — Answer **A** (`GROUP_CONCAT`)

**In MySQL, which function returns the order ids of a customer as a single comma-separated
string?**

- A. `GROUP_CONCAT(order_id)`
- B. `STRING_AGG(order_id, ',')`
- C. `LISTAGG(order_id, ',')`
- D. `CONCAT_WS(',', order_id)`

**Solution**

**MySQL** provides `GROUP_CONCAT`. `STRING_AGG` is PostgreSQL/SQL Server and `LISTAGG` is Oracle.
`CONCAT_WS` joins **separate rows/columns** — it is not an aggregate and does not collapse a group
into one string.

**Answer: A.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | `STRING_AGG` is not a MySQL function. It is the PostgreSQL / SQL Server equivalent |
| C | `LISTAGG` is the Oracle equivalent |
| D | `CONCAT_WS` is a scalar function. It joins its arguments in one row; it does not gather values across the rows of a group |

---

### Q9 — Answer **C** (`CASE` first match wins)

**What does `CASE WHEN order_amt >= 1000 THEN 'High' WHEN order_amt >= 750 THEN 'Medium' ELSE
'Low' END` return for `order_amt = 1200`?**

- A. `Medium`
- B. `Low`
- C. `High`
- D. `NULL`

**Solution**

`CASE` evaluates the `WHEN` conditions **top to bottom** and stops at the **first** one that is
true. `1200 >= 1000` is true → `'High'`. The second `WHEN` is never evaluated.

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | The first matching branch wins. `1200 >= 750` is true, but it is never reached |
| B | `ELSE` only runs when **no** `WHEN` matched |
| D | `ELSE` supplies a value, so the result is never `NULL` here |

## Quick rules

- `COUNT(*)` rows, `COUNT(col)` non-NULL, `COUNT(DISTINCT col)` distinct.
- No `GROUP BY` + aggregate = 1 row.
- `GROUP BY` on the fixture's `orders` gives **4** groups.
- Aggregate filter → `HAVING`.
- `CASE` first match wins; no `ELSE` → `NULL`.
- `NULL` test → `IS NULL`, never `= NULL`.
- `ROUND` rounds, `TRUNC` truncates, `CEIL` goes up, `FLOOR` goes down.
- `ROW_NUMBER` no ties, `RANK` skips, `DENSE_RANK` does not.
- `GROUP_CONCAT` = MySQL, `STRING_AGG` = PostgreSQL, `LISTAGG` = Oracle.

## Common traps

| Trap | Wrong answer | Right answer |
|---|---|---|
| Counting customers over the `orders` table | A in Q1 | Only customers **with** orders count |
| Confusing row count with group count | A in Q6 | `GROUP BY` gives 4 groups, not 6 |
| `= NULL` instead of `IS NULL` | D in Q3 | `= NULL` is never true |
| Reading `CASE` branches out of order | A in Q9 | First match wins |
| `FLOOR` offered for "truncate" | D in Q4 | `TRUNC` truncates toward zero |

## Checklist

- [ ] I can map a verb to a function name.
- [ ] I know the three `COUNT` variants and their answers on this fixture.
- [ ] I know `GROUP BY` on `orders` gives 4 groups.
- [ ] I know the aggregate goes in `HAVING`.
- [ ] I can evaluate a `CASE` top to bottom.
- [ ] I know `IS NULL` vs `= NULL`.
- [ ] I can tell `ROW_NUMBER`, `RANK`, `DENSE_RANK` apart.
- [ ] I know the string-aggregation function per DBMS.

## Related

- [Functions, aggregates and CASE](../01-concepts/01-functions-aggregates-and-case.md)
- [Function selection procedures](../02-techniques/01-function-selection-procedures.md)
- [Functions and aggregates traps](../04-pitfalls/01-functions-aggregates-traps.md)
- [Functions and aggregates quick check](../05-reference/01-functions-aggregates-quick-check.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
