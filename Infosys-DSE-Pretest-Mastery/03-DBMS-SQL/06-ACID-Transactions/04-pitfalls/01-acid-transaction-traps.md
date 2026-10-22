# ACID and Transaction Traps — Where Candidates Lose the Mark

> Section 3 · DBMS & SQL · ACID & Transactions · _Estimated reading time: 5 min_
> **Prerequisite:** [ACID and isolation levels](../01-concepts/01-acid-and-isolation-levels.md)

## In one sentence

Eight traps, each one a specific confusion between the four properties, the four anomalies, and the
four isolation levels.

## Why the pre-test tests this

- Transaction questions are worth 1–2 marks and every option is a term.
- The traps below are the standard distractors. Recognising them is the whole game.

## Core concept

### Trap 1 — Isolation "prevents lost updates"

No isolation level prevents lost updates on its own. A lost update is a **write-write** conflict:
both transactions read a committed value, both write, one write is overwritten. READ COMMITTED,
REPEATABLE READ and SERIALIZABLE all allow it (SERIALIZABLE makes it *less likely* by serialising
the transactions, but the classic lost-update scenario is a write-skew style race that requires
explicit `SELECT ... FOR UPDATE` or a version column).

**Exam tell:** the option says "SERIALIZABLE prevents lost updates". Technically serial execution
cannot lose an update — but the exam's intended answer is that lost updates need **explicit**
concurrency control, not a higher level.

### Trap 2 — Dirty read vs non-repeatable read

The word **committed** decides it.

| Detail in the scenario | Anomaly |
|---|---|
| The other transaction **rolled back** — the value never existed | **Dirty read** |
| The other transaction **committed** — the value was real, but it changed | **Non-repeatable read** |

### Trap 3 — Non-repeatable read vs phantom read

| What changed | Anomaly |
|---|---|
| The **value of a row you already read** | Non-repeatable read |
| The **set of rows** matching your `WHERE` | Phantom read |

"Row changed" vs "rows appeared". The number of rows is the tell.

### Trap 4 — Treating SERIALIZABLE as the answer to every "prevent" question

The exam usually asks for the **weakest sufficient** level. If the question is "which level prevents
dirty reads?", the answer is READ COMMITTED, not SERIALIZABLE. SERIALIZABLE also prevents them, but
it is over-specified and is the wrong answer to the question as asked.

**Exam tell:** the option list includes several levels, and the question says "minimum" or "lowest"
— or the question is about the *specific* anomaly.

### Trap 5 — REPEATABLE READ prevents phantoms

It does not. REPEATABLE READ guarantees that **rows you have already read** keep their values. It
does not prevent **new rows** from satisfying a predicate. MySQL's InnoDB has a related setting
(`REPEATABLE READ` + gap locks) that can reduce phantom behaviour in range scans, but the textbook
answer is: only **SERIALIZABLE** blocks phantoms.

### Trap 6 — 2PL prevents deadlock

2PL guarantees **conflict serializability**. It does **not** guarantee deadlock freedom — in fact
the shrinking phase makes deadlock *more* likely than a strict 2PL schedule. Deadlock is handled by
**prevention** (wait-die, wound-wait, lock ordering), **detection** (wait-for graph, cycle) or
**recovery** (victim rollback).

### Trap 7 — Atomicity means "each statement is atomic"

Atomicity is a property of the **transaction**, not the statement. Every single SQL statement is
already atomic on its own. The guarantee that matters is: **a group of statements** either all take
effect or none do. The option "atomicity guarantees each statement runs fully or not at all" is
true but is not what the property means.

### Trap 8 — Consistency is enforced by the DBMS alone

Consistency comes from **constraints you declare** — `PRIMARY KEY`, `UNIQUE`, `FOREIGN KEY`,
`CHECK`, `NOT NULL`, `TRIGGER` — plus the application logic that the database cannot express.
"Isolation guarantees consistency" is false: serialisability is about the *schedule*, not about
whether the rules hold.

### Bonus trap — "Durability is implemented by locking"

Durability is implemented by the **write-ahead log**, **checkpoints**, and **forcing log/data to
disk** at commit. Locks have nothing to do with it.

## Worked example

**Q. A transaction reads a row's value, another transaction updates and commits that row, and then
the first transaction reads the same row again and sees the new value. Which isolation level
prevents this?**

- A. READ UNCOMMITTED
- B. READ COMMITTED
- C. REPEATABLE READ
- D. SERIALIZABLE

**Solution**

The scenario is a **non-repeatable read**: the same row returned a different value because another
transaction committed an update in between. The weakest level that prevents it is
**REPEATABLE READ**.

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Blocks everything, including this |
| B | READ COMMITTED allows a row to change between two reads within the same transaction — that is its defining weakness |
| D | SERIALIZABLE also prevents it, but REPEATABLE READ is the **minimum** level that does. The exam wants the weakest sufficient level |

## Quick rules

- The word **committed** separates dirty read from non-repeatable read.
- The word **rows** separates non-repeatable read from phantom read.
- Weakest sufficient level: dirty → RC; non-repeatable → RR; phantom → SERIALIZABLE.
- Lost update → explicit locking or a version check, not a higher level.
- 2PL → serializability, not deadlock freedom.
- Atomicity → the transaction, not the statement.
- Durability → WAL + checkpoints, not locks.

## Common traps

| Trap | The tell in the option |
|---|---|
| "Isolation prevents lost updates" | The scenario is a write-write conflict |
| "Dirty" used for a committed change | The scenario says the other transaction **committed** |
| "Phantom" used for a changed value | The scenario mentions a **row's value**, not row count |
| "SERIALIZABLE" for a weak-anomaly question | The question names one specific anomaly |
| "2PL prevents deadlock" | The scenario mentions waiting transactions |
| "Durability via locking" | The scenario mentions a crash or power failure |

## Checklist

- [ ] I can tell dirty from non-repeatable by the word *committed*.
- [ ] I can tell non-repeatable from phantom by *value* vs *row count*.
- [ ] I give the weakest sufficient isolation level.
- [ ] I know lost updates need explicit control.
- [ ] I know 2PL's guarantee is serializability, not deadlock freedom.
- [ ] I know durability comes from the WAL.

## Related

- [ACID and isolation levels](../01-concepts/01-acid-and-isolation-levels.md)
- [Concurrency control procedures](../02-techniques/01-concurrency-control-procedures.md)
- [Solved ACID and transactions set](../03-worked-examples/01-solved-acid-transactions-set.md)
- [ACID and transactions quick check](../05-reference/01-acid-transactions-quick-check.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
