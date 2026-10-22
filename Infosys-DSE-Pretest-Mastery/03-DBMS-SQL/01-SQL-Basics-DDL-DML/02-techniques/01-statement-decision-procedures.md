# Statement Decision Procedures — Nine Recipes for SQL Questions

> Section 3 · DBMS & SQL · SQL Basics, DDL & DML · _Estimated reading time: 7 min_
> **Prerequisite:** [DDL, DML and SQL anatomy](../01-concepts/01-ddl-dml-anatomy.md)

## In one sentence

**Every SQL question in the pre-test is one of nine decisions** — identify which one, apply the
matching procedure, and you never need to remember syntax under pressure.

## Why the pre-test tests this

- "Which statement…?", "What is the output…?" and "Write the query…" are all the *same* question
  wearing different clothes: which operation am I performing?
- The procedures below are deliberately mechanical so that they survive the 108-second box.

## Core concept

### Procedure 1 — "Which statement…?" (name the family)

1. Underline the **verb** in the stem: creates, alters, removes, inserts, updates, deletes, reads,
   commits, rolls back, grants.
2. Map it:

| Stem verb | Family | Answer |
|---|---|---|
| create / define / declare | DDL | `CREATE` |
| change the structure / add a column | DDL | `ALTER` |
| remove the table / remove the database | DDL | `DROP` |
| remove all rows but keep the table | DDL | `TRUNCATE` |
| add a record | DML | `INSERT` |
| change existing records | DML | `UPDATE` |
| remove some records | DML | `DELETE` |
| show / list / find | DQL | `SELECT` |
| make permanent | TCL | `COMMIT` |
| undo | TCL | `ROLLBACK` |
| allow / deny access | DCL | `GRANT` / `REVOKE` |

3. If two options are in the same family, use the **scope discriminator**: rows vs structure vs
   identity counter vs rollback.

### Procedure 2 — "Delete all rows / delete some rows / delete the table"

```
Does the table survive?  ── no  ──→ DROP TABLE
        │ yes
Does it reset AUTO_INCREMENT and skip row logging? ── yes ──→ TRUNCATE TABLE
        │ no
Does it accept a WHERE clause and roll back? ── yes ──→ DELETE FROM t WHERE ...
```

### Procedure 3 — "Insert a row"

```sql
INSERT INTO table_name (col1, col2) VALUES (val1, val2);
```

Checklist: column list present? value count equals column count? single quotes around text? `NULL`
written unquoted? `AUTO_INCREMENT` column left out of the list?

### Procedure 4 — "Update every row where…"

```sql
UPDATE table_name
SET    col = new_value
WHERE  condition;
```

- The `WHERE` clause is **not optional** in your answer if the stem says "where".
- `SET` uses `=`, not `==`.
- Multiple columns: `SET city = 'Pune', status = 'Active'`.
- String comparisons need single quotes: `WHERE city = 'Pune'`.

### Procedure 5 — "Which filter goes in WHERE and which in HAVING?"

```
Does the condition reference an aggregate (COUNT, SUM, AVG, MAX, MIN)? ── yes ──→ HAVING
        │ no
Does it reference a column not in GROUP BY, or a row-level condition? ── yes ──→ WHERE
```

### Procedure 6 — "Match a value against a set / range / pattern / existence"

| The stem says | Use | Example |
|---|---|---|
| "one of these values" | `IN` | `city IN ('Pune','Delhi')` |
| "between X and Y", "from X to Y" | `BETWEEN` | `amount BETWEEN 300 AND 1000` |
| "starts with", "contains", "ends with" | `LIKE` | `cust_name LIKE 'A%'` |
| "has at least one matching…" | `EXISTS` | `WHERE EXISTS (SELECT 1 ...)` |
| "has no matching…" | `NOT EXISTS` | `WHERE NOT EXISTS (SELECT 1 ...)` |
| "is missing / not filled in" | `IS NULL` | `WHERE manager_id IS NULL` |

**`NOT IN` is never the answer** when the values come from a subquery that might contain NULL.

### Procedure 7 — "Combine two result sets"

| The stem says | Use |
|---|---|
| "all records from both, ignoring repeats" | `UNION` |
| "all records from both, keep repeats" | `UNION ALL` |
| "records present in both" | `INTERSECT` |
| "records in the first but not the second" | `EXCEPT` (MySQL: `NOT IN` / `NOT EXISTS`) |

### Procedure 8 — "Show the top N"

```sql
SELECT ...
FROM   ...
ORDER BY <key> DESC          -- 1. always sort
LIMIT  N;                    -- 2. then cut
```

If ties are possible at the cut line, add a deterministic tiebreaker:
`ORDER BY amount DESC, cust_id ASC LIMIT 3`. If the question says "the top 3 customers by total
spend", the sort key is `SUM(amount)`, so `GROUP BY` comes first:

```sql
SELECT c.cust_name, SUM(o.amount) AS total
FROM   customers c JOIN orders o ON c.cust_id = o.cust_id
GROUP  BY c.cust_id, c.cust_name
ORDER  BY total DESC
LIMIT  3;
```

### Procedure 9 — "Write a query for two tables" (the master recipe)

1. **Name the two tables** and the join key (`customers.cust_id = orders.cust_id`).
2. **Decide the join type** — use the [join decision table](../../02-Joins/05-reference/01-join-reference-sheet.md).
3. **Write `FROM` + `JOIN … ON`** first. Nothing else.
4. **Add `WHERE`** for the row filter.
5. **Add `GROUP BY` / `HAVING`** only if the question mentions counts, totals, averages or "more than
   n".
6. **Write the `SELECT` list** — only the columns asked for.
7. **`ORDER BY`** only if the question asks for an order.
8. **`LIMIT`** only if the question asks for top/bottom n.

Full version with diagrams: [Two-Table Query Writing](../03-Two-Table-Query-Writing/README.md).

## Worked example

**Q. A table `audit_log` has columns `id INT`, `action VARCHAR(20)`, `created_at DATE`. Which statement
removes every row from it but keeps the table and its column definitions, and cannot be rolled back
inside a transaction?**

- A. `DELETE FROM audit_log;`
- B. `DROP TABLE audit_log;`
- C. `TRUNCATE TABLE audit_log;`
- D. `TRUNCATE DATABASE audit_log;`

**Apply Procedure 2:**

1. Does the table survive? Yes → eliminate **B** and **D**.
2. Does it reset the identity counter and skip row logging? Yes → `TRUNCATE`.
3. `DELETE` can be rolled back → eliminate **A**.

**Answer: C (`TRUNCATE TABLE audit_log;`).**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| A | `DELETE` is DML: it is row-by-row, logged, and **rollbackable** inside a transaction |
| B | `DROP` removes the table structure — the question says "keeps the table" |
| D | `TRUNCATE DATABASE` is not a statement; `TRUNCATE` operates on a table |

**Faster route:** the discriminating requirement is "cannot be rolled back". Only `TRUNCATE` and
`DROP` qualify, and "keeps the table" removes `DROP`.

## Quick rules

- Identify the **verb** first; the family follows.
- Use the **discriminating requirement** to break ties inside a family.
- `WHERE` = row filter, `HAVING` = group filter.
- `IN` for lists, `BETWEEN` for ranges, `LIKE` for patterns, `EXISTS` for existence, `IS NULL` for
  missing.
- `UNION` dedups, `UNION ALL` keeps duplicates.
- Always `ORDER BY` before `LIMIT`; add a tiebreaker.
- Two-table query: `FROM`+`JOIN` → `WHERE` → `GROUP BY`/`HAVING` → `SELECT` → `ORDER BY` → `LIMIT`.

## Common traps

| Trap | The wrong option | The right pick |
|---|---|---|
| "delete the table" → `DELETE` | `DELETE FROM t` | `DROP TABLE t` |
| "remove all rows" → `DROP` | `DROP TABLE t` | `TRUNCATE TABLE t` |
| Aggregate in `WHERE` | `WHERE COUNT(*) > 1` | `HAVING COUNT(*) > 1` |
| `NOT IN` for "no matching" | `NOT IN (subquery)` | `NOT EXISTS (subquery)` |
| `=` for missing values | `WHERE mgr = NULL` | `WHERE mgr IS NULL` |
| `UNION` when duplicates matter | `UNION` | `UNION ALL` |
| `LIMIT` with no order | `LIMIT 3` alone | `ORDER BY … LIMIT 3` |
| `BETWEEN` for exclusive range | `BETWEEN 1 AND 10` | `> 1 AND < 10` |

## Checklist

- [ ] I can name the family of every SQL verb on sight.
- [ ] I used the discriminating-requirement method when two options were in the same family.
- [ ] I put aggregates in `HAVING`, never in `WHERE`.
- [ ] I chose `EXISTS`/`NOT EXISTS` for subqueries.
- [ ] I added `ORDER BY` before `LIMIT`.
- [ ] I wrote the two-table query in clause order without reordering it.

## Related

- [DDL, DML and SQL anatomy](../01-concepts/01-ddl-dml-anatomy.md)
- [SELECT, filter, sort and subqueries](../01-concepts/02-select-filter-sort-and-subqueries.md)
- [Solved SQL basics set](../03-worked-examples/01-solved-sql-basics-set.md)
- [SQL basics traps](../04-pitfalls/01-sql-basics-traps.md)
- [Command family table](../05-reference/02-command-family-table.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
