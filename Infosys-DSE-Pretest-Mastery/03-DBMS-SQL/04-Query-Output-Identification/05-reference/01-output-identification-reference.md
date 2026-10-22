# Output Identification Reference — The Trace Card

> Section 3 · DBMS & SQL · Query Output Identification · _Estimated reading time: 4 min_
> **Prerequisite:** [Trace procedures](../02-techniques/01-trace-procedures.md)

## In one sentence

One card: the five stages, the fixture in numbers, the aggregate table, and the NULL table —
everything you need to read any output query.

## Why the pre-test tests this

- Output questions are 2 of the 10 DBMS questions.
- This card plus 4 minutes of reading is the whole revision surface for the archetype.

## Core concept

### The trace card

```
STAGE 1  FROM + JOIN   →  working set     (rows multiply here)
STAGE 2  WHERE         →  filter rows
STAGE 3  GROUP BY      →  collapse to groups
STAGE 4  HAVING        →  filter groups
STAGE 5  SELECT / DISTINCT / ORDER BY / LIMIT
```

### The fixture in numbers

| Fact | Value |
|---|---|
| Customers | **5** |
| Orders | **6** |
| Total order value | **4800.00** |
| Customers with no order | 1 (105, Vikram) |
| Customers with 2 orders | 2 (101 Ananya, 104 Karthik) |
| Customers with 1 order | 2 (102 Rahul, 103 Meera) |
| Distinct cities | 4 (Pune ×2, Chennai, Delhi, Bengaluru) |
| `customers JOIN orders` | **6 rows** |
| `customers LEFT JOIN orders` | **7 rows** |
| `customers CROSS JOIN orders` | **30 rows** |
| `employees LEFT JOIN employees` (manager) | **6 rows** |

### Join row counts

| Join | Rows |
|---|---|
| `customers JOIN orders` | 6 |
| `customers LEFT JOIN orders` | 7 |
| `orders JOIN customers` | 6 |
| `orders LEFT JOIN customers` | 6 |
| `customers CROSS JOIN orders` | 30 |
| `employees e LEFT JOIN employees m` | 6 |

### Aggregate table

| Expression | Behaviour |
|---|---|
| `COUNT(*)` | Counts rows, **including** NULL-padded ones |
| `COUNT(col)` | Counts non-NULL values only |
| `COUNT(DISTINCT col)` | Counts distinct non-NULL values |
| `SUM(col)` | Skips NULLs; `NULL` if no non-NULL values |
| `AVG(col)` | Skips NULLs; denominator = non-NULL count |
| `MIN/MAX(col)` | Skips NULLs; `NULL` if all NULL |
| Any aggregate with no `GROUP BY` | Exactly **one** output row |

### NULL table

| Expression | For a NULL value | Row survives `WHERE`? |
|---|---|---|
| `col = 5` | `UNKNOWN` | ❌ |
| `col <> 5` | `UNKNOWN` | ❌ |
| `col > 5` | `UNKNOWN` | ❌ |
| `col IS NULL` | `TRUE` | ✅ |
| `col IS NOT NULL` | `FALSE` | ❌ |
| `SUM/AVG/MIN/MAX/COUNT(col)` | Skipped | — |
| `GROUP BY col` | One NULL group | ✅ |
| `ORDER BY col ASC` | NULLs first (MySQL) | ✅ |

### Shape predictor

| Query contains | Output is |
|---|---|
| Aggregate, no `GROUP BY` | 1 row |
| `GROUP BY` + aggregate | 1 row per group |
| Plain column list | 1 row per source row |
| `DISTINCT` | 1 row per distinct combination |
| `LIMIT n` | ≤ n rows |

### Time split

| Seconds | Activity |
|---|---|
| 0–15 | Read once, predict the shape |
| 15–40 | Stage 1: list the join rows |
| 40–55 | Stage 2: cross out the `WHERE` failures |
| 55–75 | Stage 3–4: groups, then `HAVING` |
| 75–90 | Stage 5: match the option, mark, move |

## Worked example

**Q. `SELECT c.cust_name, COUNT(o.order_id) FROM customers c LEFT JOIN orders o ON c.cust_id = o.cust_id GROUP BY c.cust_name;`**

| Stage | Result |
|---|---|
| 1 | 7 rows |
| 2 | 7 rows (no `WHERE`) |
| 3 | 5 groups: Ananya, Rahul, Meera, Karthik, Vikram |
| 4 | 5 groups |
| 5 | 5 output rows — counts 2, 1, 1, 2, **0** |

Vikram's count is 0 because `COUNT(o.order_id)` skips the NULL.

## Quick rules

- Five stages, always in order.
- Fixture numbers: 5, 6, 7, 30, 4800.
- After a join, count rows.
- NULL rows die in a `WHERE` unless the test is `IS NULL`.
- `COUNT(*)` vs `COUNT(col)` differ by the unmatched-row count.
- No `GROUP BY` + aggregate = one row.
- Predict the shape before reading the options.

## Common traps

| Trap | Correct |
|---|---|
| Entity count instead of row count | List the rows |
| `WHERE` kills the NULL row | Move to `ON` if needed |
| `COUNT(*)` after a `LEFT JOIN` | `COUNT(col)` |
| `DISTINCT` on one column | Whole row |
| `LIMIT` without `ORDER BY` | Add `ORDER BY` |

## Checklist

- [ ] I can recite the five stages.
- [ ] I know 5, 6, 7, 30 and 4800 for the fixture.
- [ ] I know the aggregate and NULL tables by heart.
- [ ] I can answer an output question in 60 seconds.

## Related

- [The five-step execution model](../01-concepts/01-five-step-execution-model.md)
- [Trace procedures](../02-techniques/01-trace-procedures.md)
- [Solved output identification set](../03-worked-examples/01-solved-output-identification-set.md)
- [Output identification traps](../04-pitfalls/01-output-identification-traps.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
