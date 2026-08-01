# Chapter: The Relational Model

## What you'll learn
- **The relational model & schema**: tables, rows, columns, domains; what a relation *is* mathematically; why SQL's tables ≈ but aren't exactly relations.
- **Keys, in depth**: superkeys, candidate keys, primary keys, foreign keys, and surrogate keys — how each is *found* from data semantics, and the traps (NULLs, composite keys).
- **Relational integrity constraints**: entity integrity, referential integrity, and domain integrity — and how RDBMS enforce them (PRIMARY KEY, UNIQUE, NOT NULL, FOREIGN KEY).
- **Relational algebra, for real**: SELECT, PROJECT, JOIN (theta/natural), UNION, DIFFERENCE, RENAME — the algebra that proves SQL's expressiveness and underlies every query optimizer.

## Prerequisites (linked)
- [Part 01 (DBMS Fundamentals)](../../part-01-dbms-fundamentals/README.md) — especially [Chapter 01 (Introduction to Databases)](../../part-01-dbms-fundamentals/chapter-01-introduction-to-databases/README.md) for the relational data model and [Chapter 02 (DBMS Architecture)](../../part-01-dbms-fundamentals/chapter-02-dbms-architecture/README.md) for the data dictionary.
- Feeds into [Chapter 02 (SQL)](../chapter-02-sql/README.md) — SQL is the algebra with a sugar coating — and into [Part 03 (Normalization)](../../part-03-normalization/README.md), which is entirely expressed in key/FD vocabulary.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Relational Model and Relational Schema](section-01-relational-model-and-relational-schema.md) | Relations, domains, tuples; schema vs instance; the "SQL table ≠ math relation" differences |
| [Section 02 — Keys in Databases (Super, Candidate, Primary, Foreign)](section-02-keys-in-databases-super-candidate-primary-foreign.md) | How keys are identified; minimality; FK semantics; surrogate keys |
| [Section 03 — Relational Integrity Constraints](section-03-relational-integrity-constraints.md) | Entity / referential / domain integrity; enforcement in PostgreSQL & MySQL |
| [Section 04 — Relational Algebra Operations](section-04-relational-algebra-operations.md) | SELECT/PROJECT/JOIN/UNION/DIFFERENCE/RENAME; algebra → SQL translation; optimizer use |

## One-paragraph narrative connecting all sections
The relational model is the mathematical foundation under every SQL database: a **relation** is a set of tuples over **domains** (Section 01), and its *schema* fixes column names and types while its *instance* is the current rows. Order is irrelevant, duplicates are impossible — properties SQL then bends. To actually use a relation you must **identify rows by keys** (Section 02): superkeys, the minimal candidate keys, the chosen primary key, and the foreign keys that wire relations together — this is the vocabulary normalization will later reuse word-for-word. Those keys plus the three **integrity constraints** (Section 03) are what make a database trustworthy: the RDBMS refuses entity-integrity breaks (NULL keys), referential-integrity breaks (dangling FKs), and domain violations. Finally, **relational algebra** (Section 04) is the precise, set-based calculus of queries — SELECT, PROJECT, JOIN, UNION, DIFFERENCE — that both defines what SQL means and is exactly what PostgreSQL/MySQL optimizers execute internally. Understand these four pieces and every SQL query you write is just algebra in disguise.

## Common interview trap in this chapter
Candidates confuse the *relation* (a set — no duplicates, no order) with the *SQL table* (a bag — duplicates allowed, order irrelevant). That single confusion misleads answers about `SELECT DISTINCT`, join results, and "why does the optimizer care?" Second trap: calling any column that identifies a row a "primary key" — a primary key is a *minimal* superkey, and many such sets exist (all are candidate keys); you must *choose* one. Third: forgetting that a NULL foreign key is **not** a referential-integrity violation (it's an unset reference), while a NULL primary key always is.

## Checklist before moving on
- [ ] I can state the three differences between a mathematical relation and a SQL table.
- [ ] I can compute candidate keys from functional dependencies (closure) and pick a primary key.
- [ ] I can explain why a foreign key may be NULL but a primary key never may be.
- [ ] I can name all three integrity constraints and how each is enforced in SQL.
- [ ] I can translate a SQL query (join + where + distinct) into relational algebra step by step.
- [ ] I can explain how relational algebra connects to query optimization.
- [ ] I can define superkey, candidate key, primary key, foreign key, surrogate key without hesitation.
