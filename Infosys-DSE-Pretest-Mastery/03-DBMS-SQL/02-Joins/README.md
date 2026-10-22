# Joins — Topic Guide

> Section 3 · DBMS & SQL · Joins · _Estimated reading time: 70 min for the full topic_

## What the pre-test asks in this topic

**"SQL fundamentals up to JOINs" is the biggest block in this section: 2–3 of the 10 questions.**
It appears in two shapes:

1. **"Which join do I need?"** — "To list all customers along with their orders, including customers
   who have never ordered, which join?" Options: `INNER`, `LEFT`, `RIGHT`, `FULL OUTER`.
2. **"What is the output of this join?"** — the exam shows two small tables and a query, and asks
   how many rows or which rows come out.

Both are decided by the same thing: **the escape clause in the stem.** "including those with none"
is the difference between 6 rows and 7 rows.

## Learning objectives

After this topic you should be able to:

- State in one sentence what each of the six join types keeps, and which side's unmatched rows
  survive.
- Pick the correct join from the stem's wording in **under 30 seconds**.
- Explain why a `WHERE` clause on the right table of a `LEFT JOIN` silently converts it to an
  `INNER JOIN`, and fix it by moving the predicate into `ON`.
- Compute the row count of any join on a small fixture before you look at the options.
- Choose between `COUNT(*)`, `COUNT(col)` and `COUNT(DISTINCT col)` correctly for "how many
  customers/orders/matches".
- Write a many-to-many query through a junction table and predict its row count.
- Write a self-join for a manager hierarchy using two aliases and a `LEFT JOIN`.
- Say what `NATURAL JOIN` does, why it is risky, and how the output column count differs from an
  explicit join.

## File index

| File | Lines | What it gives you |
|---|---|---|
| [01-concepts/01-the-six-joins.md](01-concepts/01-the-six-joins.md) | ~250 | The cartesian-product mental model, all six joins, `ON` vs `WHERE`, `NATURAL JOIN`, fan-out |
| [02-techniques/01-join-decision-table.md](02-techniques/01-join-decision-table.md) | ~230 | The decision table, the keyword scanner, a 7-step procedure, the 3-row test |
| [03-worked-examples/01-solved-join-set.md](03-worked-examples/01-solved-join-set.md) | ~290 | 9 solved questions: 4 "which join", 5 "what is the output", all traced on paper |
| [04-pitfalls/01-join-traps.md](04-pitfalls/01-join-traps.md) | ~180 | 5 named traps + 1 bonus, each with the wrong answer, the right answer and the signature option |
| [05-reference/01-join-reference-sheet.md](05-reference/01-join-reference-sheet.md) | ~170 | Six joins, row counts on the fixture, the "which join" one-liner, count cheat, MySQL notes |
| [05-reference/02-join-cheat-sheet.md](05-reference/02-join-cheat-sheet.md) | ~100 | The 3-minute version: six joins, three sentences, four numbers, three traps |

## Quick 4-step join procedure

1. **Circle the entity that must appear.** It goes on the **left** — unless the question wants the
   other side's rows to survive.
2. **Scan for the escape clause.** "including", "even if", "or without", "who have never" → `LEFT
   JOIN`.
3. **Scan for the restriction clause.** "who have", "that have an order", "matching" → `INNER JOIN`.
4. **Count the rows before reading the options.** 6, 7, 30 and 5 are the four numbers that decide
   most of these questions.

## Key takeaways

- ✅ **A join is a filtered cartesian product.** INNER keeps matches only; LEFT keeps every left
  row; RIGHT keeps every right row.
- ✅ **"LEFT JOIN keeps unmatched left rows with NULLs on the right."** Say this sentence until it
  is automatic.
- ✅ **`ON` decides matching; `WHERE` filters the result.** Putting a right-table condition in
  `WHERE` on a `LEFT JOIN` turns it into an inner join.
- ✅ **The join can multiply rows.** `COUNT(*)` after a one-to-many join counts join rows, not
  entities — use `COUNT(DISTINCT col)`.
- ✅ **`NATURAL JOIN` matches every same-named column** and shows the joined column once.
- ✅ **Many-to-many always goes through a junction table**, and the result row count equals the
  junction row count.
- ✅ **Self-join needs two aliases** and usually a `LEFT JOIN` to keep the top of the hierarchy.
- ⚠️ **Meera's warning:** she knows the join is right but counts 5 customers instead of 7 rows.
  Write the rows out. Always.

## Related

- [DBMS & SQL section index](../README.md)
- [SQL Basics: DDL & DML](../01-SQL-Basics-DDL-DML/README.md) — the clauses every join sits inside
- [Two-Table Query Writing](../03-Two-Table-Query-Writing/README.md) — where joins get used for real
- [Query Output Identification](../04-Query-Output-Identification/README.md) — tracing join outputs
- [Master README](../../README.md)
