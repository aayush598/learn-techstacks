# Chapter: Concurrency in Practice

## What you'll learn
- How **PostgreSQL** actually implements MVCC — tuple versions, `xmin`/`xmax`, snapshots, `VACUUM`, and the real behavior of READ COMMITTED vs REPEATABLE READ vs SERIALIZABLE.
- How **MySQL InnoDB** implements it differently — undo log, `DB_TRX_ID`/`DB_ROLL_PTR`, next-key locks, and the REPEATABLE READ default.
- The **optimistic vs pessimistic** concurrency spectrum — and how to *choose* for a given system design, including app-level optimistic locking with version columns.

## Prerequisites (linked)
- [Chapter 01 README](chapter-01-transactions/README.md) — transaction, ACID, isolation levels.
- [Chapter 02 README](chapter-02-concurrency-control-protocols/README.md) — 2PL, MVCC, timestamps, deadlock.

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [MVCC in Postgres and MySQL InnoDB](chapter-03-concurrency-in-practice/section-01-mvcc-in-postgres-and-mysql-innodb.md) | How do two real engines turn MVCC theory into production behavior? |
| 02 | [Optimistic vs Pessimistic Concurrency Control](chapter-03-concurrency-in-practice/section-02-optimistic-vs-pessimistic-concurrency-control.md) | When do you choose locking, versions, or app-level validation? |

## One-paragraph narrative connecting all sections
Chapter 02 gave you the protocol zoo (2PL, timestamps, validation, MVCC, deadlock). Chapter 03 is where theory meets the engines interviewers expect you to have *actually used*. Section 01 dissects MVCC in PostgreSQL — per-tuple versions, `xmin`/`xmax` visibility rules, the read snapshot, and `VACUUM` reclaiming dead versions — then contrasts it with InnoDB, where old versions live in an undo log reached via `DB_ROLL_PTR` and where next-key locks bolt phantom prevention onto the snapshot model. Seeing both side-by-side is the fastest way to internalize *why* "REPEATABLE READ" means different things in different engines. Section 02 steps back to the decision: pessimistic control (locks, `SELECT FOR UPDATE`) is right when conflicts are frequent and aborts are costly; optimistic control (app-level version columns, validation) is right when conflicts are rare — and it gives you the production recipe for choosing, plus the classic "distributed counter" and "inventory" scenarios where the choice decides whether your system scales.

## Common interview trap in this chapter
**Trap:** Believing "REPEATABLE READ" behaves identically in Postgres and MySQL — it doesn't (Postgres: pure snapshot, write-skew possible; InnoDB: snapshot + next-key locks, phantom-safe on writes, different write-conflict behavior). Also: thinking `SELECT FOR UPDATE` is "optimistic" — it's the most pessimistic primitive there is. And: believing optimistic concurrency is always better because "locks are slow" — under high contention it aborts so much work that pessimistic wins; the real question is the *conflict rate*. Finally, don't confuse Postgres `VACUUM` (dead-version reclamation) with MySQL's purge thread — different mechanisms, same goal.

## Checklist before moving on
- [ ] I can explain Postgres tuple visibility using `xmin`/`xmax` and a snapshot.
- [ ] I can explain InnoDB's undo-log-based old-version reconstruction and next-key locks.
- [ ] I can describe what `VACUUM`/autovacuum and the InnoDB purge thread actually do.
- [ ] I can state the real (different) semantics of REPEATABLE READ in Postgres vs MySQL.
- [ ] I can pick optimistic vs pessimistic for a given workload and defend it with conflict-rate reasoning.
- [ ] I can write an app-level optimistic-locking update and its retry loop.
