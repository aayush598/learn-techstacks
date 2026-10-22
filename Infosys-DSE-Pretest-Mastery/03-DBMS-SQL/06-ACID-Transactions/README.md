# ACID & Transactions — Topic Guide

> Section 3 · DBMS & SQL · ACID & Transactions · _Estimated reading time: 32 min for the full topic_

## What the pre-test asks in this topic

**Transactions and ACID is 1–2 of the 10 DBMS questions** and it is pure vocabulary — no SQL, no
fixture, no arithmetic. The exam asks one of these:

- "Which ACID property guarantees X?" → Atomicity / Consistency / Isolation / Durability.
- "What is this anomaly called?" → dirty / non-repeatable / phantom / lost update.
- "Which isolation level prevents X?" → the **weakest** level that blocks it.
- "Which mechanism is this?" → locking / MVCC / timestamp ordering / optimistic control.

## Learning objectives

After this topic you should be able to:

- State all four ACID properties in one line each **with the mechanism that implements it**.
- Define all four anomalies and identify each from the wording of a scenario.
- Recite the **four isolation levels** and, for each, exactly which anomalies it blocks.
- Always answer "which level prevents X" with the **weakest sufficient level**, not SERIALIZABLE.
- Explain that a **lost update** is a write-write conflict that no isolation level fixes by itself.
- Describe **two-phase locking** — growing then shrinking, no new locks after the first release —
  and what it does and does not guarantee.
- Name the three deadlock strategies: **prevention, detection, recovery**, and say how each works.
- Explain **MVCC** in one sentence and name what it replaces.
- Tell whether a schedule is **conflict-serializable** using the precedence graph.

## File index

| File | Lines | What it gives you |
|---|---|---|
| [01-concepts/01-acid-and-isolation-levels.md](01-concepts/01-acid-and-isolation-levels.md) | ~330 | ACID with mechanisms, atomicity machinery, consistency enforcement, the four levels, the four anomalies, 2PL, deadlock, serializability, 2PC, MVCC |
| [02-techniques/01-concurrency-control-procedures.md](02-techniques/01-concurrency-control-procedures.md) | ~270 | Property-matching table, anomaly decision tree, level selection, mechanism table, precedence-graph procedure, the "weakest sufficient" rule, 60-second split |
| [03-worked-examples/01-solved-acid-transactions-set.md](03-worked-examples/01-solved-acid-transactions-set.md) | ~330 | 8 solved questions with full reasoning and distractors explained |
| [04-pitfalls/01-acid-transaction-traps.md](04-pitfalls/01-acid-transaction-traps.md) | ~200 | 8 traps + 1 bonus, each with the tell in the option |
| [05-reference/01-acid-transactions-quick-check.md](05-reference/01-acid-transactions-quick-check.md) | ~160 | ACID table, anomaly table, level table, statement syntax, 2PL summary, deadlock strategies, cheat sheet |

## Quick procedure

1. **Identify the ask:** property, anomaly, level, or mechanism?
2. **Property:** match the phrase — all-or-nothing → Atomicity; rules hold → Consistency; no
   partial views → Isolation; survives crash → Durability.
3. **Anomaly:** *committed?* → non-repeatable. *Uncommitted?* → dirty. *Row count changed?* →
   phantom. *Write overwritten?* → lost update.
4. **Level:** pick the **weakest** that blocks it — dirty → READ COMMITTED; non-repeatable →
   REPEATABLE READ; phantom → SERIALIZABLE.
5. **Mechanism:** snapshots and no reader-writer blocking → MVCC. Lock phases → 2PL. Version check →
   optimistic.

## Key takeaways

- ✅ **Atomicity = all or nothing.** It applies to the *transaction*, not the statement.
- ✅ **Consistency = constraints hold.** PK, FK, CHECK, triggers, application rules.
- ✅ **Isolation = no partial views.** Locks or MVCC.
- ✅ **Durability = survives a crash.** Write-ahead log, checkpoints.
- ✅ **Dirty → READ COMMITTED, non-repeatable → REPEATABLE READ, phantom → SERIALIZABLE.**
- ✅ **Lost update is not a read anomaly** — it needs `SELECT ... FOR UPDATE` or a version column.
- ✅ **2PL guarantees serializability, not deadlock freedom.** After the first release, no new locks.
- ✅ **Deadlock:** prevent, detect (wait-for graph cycle), or recover (victim rollback).
- ⚠️ **Meera's note:** she knows ACID but answers "SERIALIZABLE" every time. The exam wants the
  weakest sufficient level.

## Related

- [DBMS & SQL section index](../README.md)
- [SQL Basics: DDL & DML](../01-SQL-Basics-DDL-DML/README.md) — `COMMIT`, `ROLLBACK`, constraint DDL
- [DBMS Theory, Keys, Indexes & Views](../07-DBMS-Theory-Keys-Indexes-Views/README.md) — keys and constraints that enforce consistency
- [Master README](../../README.md)
