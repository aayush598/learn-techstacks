# DBMS Theory — 9 Solved Questions

> Section 3 · DBMS & SQL · DBMS Theory, Keys, Indexes & Views · _Estimated reading time: 12 min_
> **Prerequisite:** [DBMS concept procedures](../02-techniques/01-dbms-concept-procedures.md)

## In one sentence

Nine theory questions — schema levels, data independence, keys, cardinality, indexes, views,
programmable objects — each solved by matching the stem to the concept table.

## Why the pre-test tests this

- 1–2 of the 10 DBMS questions, and it is the widest archetype: any of twenty definitions.
- The distractors are always **a different concept's correct definition**. Knowing the exact
  wording of each definition is the whole skill.

## Core concept

### The concept → tell map

```
external / conceptual / internal   → three-level schema
"without changing"                  → data independence
DDL / DML / GRANT / COMMIT           → data languages
candidate / primary / alternate      → keys
ON DELETE / orphan                  → referential integrity
one-to-many / participation         → ER model
B-tree / clustered / selectivity    → indexes
view / updatable / materialized     → views
procedure / function / trigger      → programmable objects
2-tier / DBA / flat files           → architecture
```

## Worked example

### Q1 — Answer **B** (Conceptual)

**In the ANSI/SPARC three-level schema architecture, which level describes the tables, keys,
constraints and relationships of the entire database?**

- A. External level
- B. Conceptual level
- C. Internal level
- D. Metadata level

**Solution**

The **conceptual level** (also called the **logical level**) holds the global logical structure of
the whole database — every table, key, constraint and relationship. The external level holds
user-specific views; the internal level holds the physical storage.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | The external level holds the views and user programs — what each user sees |
| C | The internal level holds files, pages, indexes and access paths |
| D | There is no "metadata level" in the three-level architecture. The **data dictionary** stores metadata, but it is not one of the three schema levels |

---

### Q2 — Answer **A** (Logical data independence)

**A DBA splits `customers` into `customers` and `customer_addresses`, and re-points an existing view
so that user programs are not changed. Which independence is demonstrated?**

- A. Logical data independence
- B. Physical data independence
- C. Referential integrity
- D. Transaction isolation

**Solution**

The **conceptual** schema changed (a table was split) while the **external** schema (the views and
user programs) stayed the same. That is exactly logical data independence.

**Answer: A.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | Physical data independence is about changing indexes and file layout with no conceptual change |
| C | Referential integrity is about foreign keys matching parent keys — nothing about schema changes |
| D | Transaction isolation is about concurrent transactions — unrelated |

---

### Q3 — Answer **C** (DCL)

**Which SQL category includes `GRANT` and `REVOKE`?**

- A. DDL
- B. DML
- C. DCL
- D. TCL

**Solution**

`GRANT` and `REVOKE` manage **privileges**, which is the **Data Control Language**.

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | DDL is `CREATE`, `ALTER`, `DROP`, `TRUNCATE` — it changes the schema |
| B | DML is `INSERT`, `UPDATE`, `DELETE` — it changes rows |
| D | TCL is `COMMIT`, `ROLLBACK`, `SAVEPOINT` — it controls transactions |

---

### Q4 — Answer **B** (Candidate key)

**Which of the following is the correct definition of a candidate key?**

- A. An attribute set that determines all attributes of a relation
- B. A minimal attribute set that determines all attributes of a relation
- C. The candidate key chosen by the database administrator as the primary key
- D. An attribute in a relation that uniquely identifies another relation

**Solution**

A candidate key is a **minimal** superkey — the smallest set of attributes that still determines
everything.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | That is the definition of a **superkey**. A superkey need not be minimal — `{cust_id, cust_name}` is a superkey but not a candidate key |
| C | That is the **primary key** |
| D | That is a **foreign key** |

---

### Q5 — Answer **D** (Foreign key on the many side)

**The `orders` table must record, for every order, the customer who placed it. A customer may place
many orders, and every order must have exactly one customer. Which design is correct?**

- A. `customers.cust_id` as a foreign key referencing `orders.order_id`
- B. `orders.cust_id` as a foreign key referencing `customers.cust_id`
- C. A `customer_orders` junction table with a composite key
- D. A `customer_orders` junction table with a composite key, because the relationship is M:N

**Solution**

This is a **one-to-many** relationship: many orders, one customer each. A **1:N** relationship
needs **no junction table** — the foreign key goes on the many side.

**Correct design:**

```sql
CREATE TABLE orders (
  order_id   INT PRIMARY KEY,
  cust_id    INT,
  FOREIGN KEY (cust_id) REFERENCES customers(cust_id)
);
```

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | It puts the FK on the wrong side and creates a circular reference between the two tables |
| C | A junction table is for **M:N**. Here one customer has many orders but one order has exactly one customer — a junction table would allow an order to have several customers, which the requirement forbids |
| D | Same reason as C, and it also misstates the relationship as M:N |

---

### Q6 — Answer **A** (B-tree)

**Which index structure is the default choice for a large table that will be queried with
`WHERE amount BETWEEN 100 AND 500` and `ORDER BY order_date`?**

- A. B-tree index
- B. Hash index
- C. Bitmap index
- D. No index is needed

**Solution**

A B-tree stores keys **in sorted order**, so it supports range predicates, `BETWEEN`, `ORDER BY`
and prefix searches — all in one structure. A hash index supports **equality only** and cannot
satisfy a range or an `ORDER BY`.

**Answer: A.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | A hash index cannot do range scans or return rows in sorted order |
| C | Bitmap indexes suit **low-cardinality** columns with many rows, e.g. a `status` flag. `amount` is high-cardinality |
| D | A large table queried by range and sort is exactly the case an index is for |

---

### Q7 — Answer **C** (Not usable — leftmost prefix rule)

**An index exists on `orders(cust_id, order_date)`. Which query will **NOT** be able to use that
index for its lookup?**

- A. `SELECT * FROM orders WHERE cust_id = 101;`
- B. `SELECT * FROM orders WHERE cust_id = 101 AND order_date = '2026-01-05';`
- C. `SELECT * FROM orders WHERE order_date = '2026-01-05';`
- D. `SELECT * FROM orders WHERE cust_id > 100 ORDER BY order_date;`

**Solution**

The **leftmost prefix rule**: a composite index on `(cust_id, order_date)` can be used only if the
leftmost column `cust_id` is in the predicate. Option C filters on `order_date` alone, so the index
cannot be used for the lookup.

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Uses the leftmost column → the index is usable |
| B | Uses the leftmost column plus the second → the index is usable and covers the full key |
| D | Uses the leftmost column with a range, and `ORDER BY` on the second column of the same index is also usable |

---

### Q8 — Answer **B** (Trigger)

**A requirement says: "whenever a row is deleted from `orders`, the corresponding row must be
deleted from `order_audit`." Which database object implements this?**

- A. A stored procedure
- B. A trigger
- C. A function
- D. A view

**Solution**

The behaviour must happen **automatically** when the event occurs. Only a **trigger** fires
automatically on an event.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | A stored procedure must be **called explicitly**. It will not fire by itself on a `DELETE` |
| C | A function returns a single value and is called from an expression. It cannot fire on an event |
| D | A view is a stored query. It cannot perform a `DELETE` on another table |

---

### Q9 — Answer **D** (3-tier)

**A web application runs in a browser, calls an application server written in Java, which connects
to a MySQL database over the network. How many tiers is this?**

- A. One tier
- B. Two tiers
- C. Two-and-a-half tiers
- D. Three tiers

**Solution**

| Tier | Component here |
|---|---|
| 1 | The browser (presentation) |
| 2 | The Java application server (business logic) |
| 3 | MySQL (data) |

Three distinct layers with the business logic in its own server → **3-tier**.

**Answer: D.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | One tier means the app and the data are on the same machine with no network separation |
| B | Two tiers is a client talking **directly** to the DBMS, with no middle server |
| C | Not a real architecture term. Do not invent one when the options run out |

## Quick rules

- Conceptual = logical. Internal = physical. External = view.
- Logical independence = conceptual changes; physical = internal changes.
- DDL / DML / DQL / DCL / TCL.
- Superkey = any, candidate = minimal, primary = chosen, alternate = not chosen.
- FK on the many side; 1:N needs no junction table; M:N does.
- B-tree for ranges and sorts, hash for equality, bitmap for low cardinality.
- Leftmost prefix rule; covering index.
- Trigger = automatic. Procedure = called. Function = returns one value.

## Common traps

| Trap | Wrong answer | Right answer |
|---|---|---|
| Superkey definition for candidate key | A in Q4 | Candidate key = minimal superkey |
| Foreign key on the wrong side | A in Q5 | FK on the many side |
| Junction table for a 1:N relationship | C in Q5 | 1:N needs no junction table |
| Hash index for a range query | B in Q6 | B-tree |
| Composite index without the leftmost column | — | Cannot be used |
| Trigger confused with procedure | A in Q8 | Only a trigger fires automatically |

## Checklist

- [ ] I can define all ten key types.
- [ ] I can distinguish the three schema levels by their contents.
- [ ] I know the five data language categories.
- [ ] I can read cardinality and participation off a scenario.
- [ ] I know when an index is usable and when it is not.
- [ ] I can tell a trigger from a procedure from a function.
- [ ] I can count tiers in an architecture diagram.

## Related

- [Schema, keys and indexes](../01-concepts/01-schema-keys-and-indexes.md)
- [DBMS concept procedures](../02-techniques/01-dbms-concept-procedures.md)
- [DBMS theory traps](../04-pitfalls/01-dbms-theory-traps.md)
- [DBMS theory quick check](../05-reference/01-dbms-theory-quick-check.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
