# SQL Basics Cheat Sheet — Print This Page

> Section 3 · DBMS & SQL · SQL Basics, DDL & DML · _Estimated reading time: 5 min_
> **Prerequisite:** [DDL, DML and SQL anatomy](../01-concepts/01-ddl-dml-anatomy.md)

## In one sentence

One page: every SQL clause, every NULL rule, and every operator choice you need for archetype (a)
— enough to answer a SQL-foundation question without hesitating.

## Why the pre-test tests this

- SQL fundamentals are 1–2 of the 10 DBMS questions. This sheet is the whole revision surface.
- If you can read the answer off this page, the archetype costs 55 seconds, not 108.

## Core concept

### Clause order — typed vs executed

```
Typed:    SELECT  FROM  JOIN  WHERE  GROUP BY  HAVING  ORDER BY  LIMIT
Executed: FROM→JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT
```

### Statement family table

| Family | Statements | Auto-commit (MySQL) |
|---|---|---|
| DDL | `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME` | Yes |
| DML | `INSERT`, `UPDATE`, `DELETE`, `MERGE` | No |
| DQL | `SELECT` | n/a |
| TCL | `COMMIT`, `ROLLBACK`, `SAVEPOINT`, `SET TRANSACTION` | — |
| DCL | `GRANT`, `REVOKE` | Yes |

### DELETE vs TRUNCATE vs DROP

| | `DELETE` | `TRUNCATE` | `DROP` |
|---|---|---|---|
| Rows | Removed | Removed | Removed |
| Structure | Kept | Kept | **Removed** |
| `WHERE` | Yes | No | No |
| Rollback | **Yes** | No | No |
| `AUTO_INCREMENT` reset | No | **Yes** | Yes |
| Triggers fire | Yes | No | No |
| Class | DML | DDL | DDL |

### NULL behaviour table

| Expression / function | Result |
|---|---|
| `NULL = NULL`, `NULL <> NULL` | `UNKNOWN` — never `TRUE` |
| `NULL > 5`, `NULL + 10` | `UNKNOWN` / `NULL` |
| `NULL IS NULL` | `TRUE` |
| `COUNT(*)` | Counts **all rows** |
| `COUNT(col)` | Counts **non-NULL** values |
| `SUM/AVG/MIN/MAX(col)` | Ignore NULLs; `SUM` of all-NULL = `NULL` |
| `AVG(col)` | Denominator = count of non-NULL values |
| `GROUP BY col` | NULLs form **one** group |
| `DISTINCT` | One NULL counted once |
| `ORDER BY col ASC` | NULLs first (MySQL); last (PostgreSQL/Oracle) |
| `NOT IN (list with NULL)` | **Zero rows** |

### Operator chooser

| Need | Keyword | Example |
|---|---|---|
| One of these values | `IN` | `city IN ('Pune','Delhi')` |
| Inclusive range | `BETWEEN` | `amount BETWEEN 300 AND 1000` |
| Pattern | `LIKE` | `cust_name LIKE 'A%'` |
| At least one match | `EXISTS` | `WHERE EXISTS (SELECT 1 ...)` |
| No match | `NOT EXISTS` | `WHERE NOT EXISTS (SELECT 1 ...)` |
| Missing value | `IS NULL` | `WHERE manager_id IS NULL` |
| Combine | `AND`, `OR`, `NOT` | Bracket when mixing `AND` and `OR` |

### `LIKE` patterns

| Pattern | Meaning |
|---|---|
| `%` | zero or more characters |
| `_` | exactly one character |
| `'A%'` | starts with A |
| `'%a'` | ends with a |
| `'%an%'` | contains "an" |
| `'a_'` | a + exactly one more character |

### Set operations

| Operation | Duplicates | MySQL support |
|---|---|---|
| `UNION` | Removed | All versions |
| `UNION ALL` | Kept | All versions |
| `INTERSECT` | Removed | 8.0.31+ only |
| `EXCEPT` | Removed | 8.0.31+ only |

Same number of columns required; column names come from the first `SELECT`.

### `LIMIT` spellings

| Engine | Syntax |
|---|---|
| MySQL / PostgreSQL / SQLite | `LIMIT n` · `LIMIT n OFFSET m` |
| MySQL only | `LIMIT m, n` |
| SQL Server | `TOP n` |
| Oracle 12c+ / standard SQL | `FETCH NEXT n ROWS ONLY` |

### Data types cheat

| Need | Type | Note |
|---|---|---|
| Whole number | `INT` | `BIGINT` for large ids |
| Money | `DECIMAL(10,2)` | Never `FLOAT` |
| Fixed text | `CHAR(n)` | Pads with spaces |
| Variable text | `VARCHAR(n)` | Up to `n`, no padding |
| Date only | `DATE` | `YYYY-MM-DD` |
| Date + time | `DATETIME` / `TIMESTAMP` | |
| Yes/No | `BOOLEAN` | MySQL stores 0/1 |

### Constraint names

| Constraint | Ensures | Also implies |
|---|---|---|
| `PRIMARY KEY` | Unique, non-null per row | Index, `NOT NULL` |
| `UNIQUE` | No duplicate values | Index; multiple NULLs allowed in most engines |
| `FOREIGN KEY` | Value exists in the parent table | Referential integrity |
| `NOT NULL` | Column must have a value | |
| `CHECK` | Column/row rule | e.g. `CHECK (amount >= 0)` |
| `DEFAULT` | Fallback value | Not the same as `NULL` |

## Worked example

**Q. Which statement deletes all rows of `orders`, keeps the table, resets the identity counter, and
is not rollbackable?**

```sql
TRUNCATE TABLE orders;
```

Four requirements → one statement. Check each against the table above: rows ✅, structure kept ✅,
identity reset ✅, rollback ❌ (DDL auto-commit in MySQL).

## Quick rules

- Verb → family. Rows → DML. Structure → DDL. Read → DQL. Undo → TCL. Permissions → DCL.
- `DELETE` rows · `TRUNCATE` empty table · `DROP` remove table.
- `IS NULL`, never `= NULL`.
- `COUNT(*)` = rows; `COUNT(col)` = non-NULL values.
- `WHERE` = rows, `HAVING` = groups.
- `NOT EXISTS` beats `NOT IN`.
- `UNION` dedups, `UNION ALL` keeps.
- `ORDER BY` then `LIMIT`; add a tiebreaker.

## Common traps

| Trap | Correct |
|---|---|
| `DELETE` for "delete the table" | `DROP TABLE` |
| `DROP` for "remove all rows" | `TRUNCATE TABLE` |
| `= NULL` | `IS NULL` |
| `COUNT(*)` = `COUNT(col)` | Not equal when the column has NULLs |
| Aggregate in `WHERE` | `HAVING` |
| `NOT IN` with NULL | `NOT EXISTS` |
| `UNION` when duplicates count | `UNION ALL` |
| `LIMIT` without `ORDER BY` | Add `ORDER BY` |

## Checklist

- [ ] I can recite the clause execution order.
- [ ] I know the four `DELETE`/`TRUNCATE`/`DROP` differences.
- [ ] I know the NULL behaviour of all eight common functions/expressions.
- [ ] I pick the right operator for lists, ranges, patterns and existence.
- [ ] I know the `LIMIT` spelling for MySQL, PostgreSQL, Oracle and SQL Server.
- [ ] I can answer any SQL-foundation MCQ in under 60 seconds.

## Related

- [DDL, DML and SQL anatomy](../01-concepts/01-ddl-dml-anatomy.md)
- [SELECT, filter, sort and subqueries](../01-concepts/02-select-filter-sort-and-subqueries.md)
- [Statement decision procedures](../02-techniques/01-statement-decision-procedures.md)
- [Solved SQL basics set](../03-worked-examples/01-solved-sql-basics-set.md)
- [SQL basics traps](../04-pitfalls/01-sql-basics-traps.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
