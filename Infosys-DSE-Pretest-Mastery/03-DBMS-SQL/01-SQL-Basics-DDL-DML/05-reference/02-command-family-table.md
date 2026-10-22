# Command Family Table — Every SQL Verb, One Line Each

> Section 3 · DBMS & SQL · SQL Basics, DDL & DML · _Estimated reading time: 4 min_
> **Prerequisite:** [DDL, DML and SQL anatomy](../01-concepts/01-ddl-dml-anatomy.md)

## In one sentence

Every SQL command the pre-test can ask about, with its family, its effect, and the one fact you
must not get wrong about it.

## Why the pre-test tests this

- "Which statement…?" questions only need you to recall the right row of this table.
- Print it. Read it once before the exam and the archetype is closed.

## Core concept

### Master command table

| Command | Family | Effect | Key fact |
|---|---|---|---|
| `CREATE TABLE` | DDL | Creates a table | Add constraints at creation: `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `CHECK` |
| `CREATE INDEX` | DDL | Creates an index | Speeds reads, slows writes |
| `CREATE VIEW` | DDL | Creates a virtual table | Stored as a query, not as data |
| `CREATE PROCEDURE` / `CREATE FUNCTION` | DDL / DML | Creates stored code | Procedure may `RETURN` void; function must return a value |
| `CREATE TRIGGER` | DDL | Creates automatic code on an event | Fires on INSERT/UPDATE/DELETE |
| `ALTER TABLE` | DDL | Changes structure | Can add/drop columns, add/drop constraints, rename |
| `RENAME TABLE` | DDL | Renames | `ALTER TABLE t RENAME TO t2;` |
| `DROP TABLE` | DDL | Removes the table and data | Irreversible |
| `DROP DATABASE` | DDL | Removes the whole database | — |
| `DROP INDEX` | DDL | Removes an index | Query plans may change |
| `TRUNCATE TABLE` | DDL | Empties a table, resets identity | No `WHERE`, not rollbackable in MySQL |
| `INSERT INTO` | DML | Adds rows | Can insert from a `SELECT` |
| `UPDATE` | DML | Changes existing rows | Without `WHERE` → all rows |
| `DELETE FROM` | DML | Removes rows | With `WHERE`; rollbackable |
| `MERGE` | DML | Insert-or-update in one statement | Upsert |
| `SELECT` | DQL | Reads rows | Not DML — a classic trap |
| `COMMIT` | TCL | Makes changes permanent | Ends the transaction |
| `ROLLBACK` | TCL | Undoes uncommitted changes | Only uncommitted work is undone |
| `SAVEPOINT` | TCL | Partial rollback point | `ROLLBACK TO SAVEPOINT sp1;` |
| `SET TRANSACTION` | TCL | Sets isolation level | Must run before the transaction starts |
| `GRANT` | DCL | Gives a privilege | `GRANT SELECT ON orders TO analyst;` |
| `REVOKE` | DCL | Takes a privilege back | — |

### Object model table

| Object | Is it stored? | Contains | Notes |
|---|---|---|---|
| **Table** | Yes | Rows and columns | The base relation |
| **View** | No (definition only) | A stored `SELECT` | Recomputed on every query; can be updatable if it maps to one table |
| **Materialised view** | **Yes** | Physically stored results | Refreshed on a schedule; fast reads; costs storage |
| **Index** | Yes | B-tree / hash structures | A separate structure pointing at rows |
| **Stored procedure** | Yes | Code | May return no value; supports `OUT` parameters |
| **Function** | Yes | Code | Must return exactly one value; usable inside `SELECT` |
| **Trigger** | Yes | Code | Fires automatically; no parameters; `INSTEAD OF` triggers exist for views |
| **Temporary table** | Yes, until session ends | Rows | `CREATE TEMPORARY TABLE` |
| **Cursor** | No | A pointer over a result set | Row-by-row processing |

### DDL vs DML — the five-second version

| | DDL | DML |
|---|---|---|
| Changes | Structure | Rows |
| Examples | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` | `INSERT`, `UPDATE`, `DELETE` |
| Rollback (MySQL) | **No** (auto-commits) | **Yes** |
| Triggers | Not fired | **Fired** |
| Typical question | "which command modifies the schema?" | "which command modifies the data?" |

### Stored procedure vs function vs trigger

| | Procedure | Function | Trigger |
|---|---|---|---|
| Called by | `CALL p();` | Inside an expression | Automatically, by the DBMS |
| Returns | May return none / `OUT` params | **Must** return one value | None |
| Takes input | Yes | Yes | No (uses row context) |
| Used in `SELECT` | No | **Yes** | No |
| Example use | Batch of DML statements | `fn_total(101)` | Audit-log every DELETE |

## Worked example

**Q. Which statement is a DML statement?**

- A. `CREATE TABLE`
- B. `ALTER TABLE`
- C. `UPDATE`
- D. `DROP TABLE`

**Answer: C (`UPDATE`).** DML = `INSERT`, `UPDATE`, `DELETE`, `MERGE`. A, B and D are all DDL.

---

**Q. Which command can be rolled back inside a transaction in MySQL?**

- A. `TRUNCATE TABLE orders;`
- B. `DELETE FROM orders;`
- C. `DROP TABLE orders;`
- D. `ALTER TABLE orders ADD COLUMN note VARCHAR(50);`

**Answer: B.** `DELETE` is DML. `TRUNCATE`, `DROP` and `ALTER` are DDL and implicitly commit in
MySQL.

---

**Q. Which object is physically stored with its results?**

- A. View
- B. Materialised view
- C. Index
- D. Cursor

**Answer: B.** A plain view stores only the query definition; a materialised view stores the result
set on disk and must be refreshed.

## Quick rules

- DDL = structure, DML = rows, DQL = read, TCL = transaction control, DCL = permissions.
- `SELECT` is DQL, never DML.
- `TRUNCATE` is DDL in the textbook classification.
- A view stores a definition; a materialised view stores data.
- A function must return one value; a procedure need not.
- A trigger has no parameters and fires automatically.
- `ROLLBACK` only undoes **uncommitted** work.

## Common traps

| Trap | Correct |
|---|---|
| `SELECT` is DML | It is DQL |
| `TRUNCATE` is DML | It is DDL |
| `DROP` and `TRUNCATE` are rollbackable | Neither is, in MySQL |
| A view stores data | It stores a definition |
| A function can return nothing | It must return one value |
| A trigger is called manually | It fires automatically |

## Checklist

- [ ] I can name the family of every verb in the master table.
- [ ] I know which commands are rollbackable in MySQL.
- [ ] I know the one distinguishing fact about views, materialised views, procedures, functions and
      triggers.
- [ ] I can answer any "which command…" question in under 30 seconds.

## Related

- [DDL, DML and SQL anatomy](../01-concepts/01-ddl-dml-anatomy.md)
- [Statement decision procedures](../02-techniques/01-statement-decision-procedures.md)
- [Solved SQL basics set](../03-worked-examples/01-solved-sql-basics-set.md)
- [SQL basics cheat sheet](01-sql-basics-cheat-sheet.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
