# ACID and Isolation Levels — The Full Picture

> Section 3 · DBMS & SQL · ACID & Transactions · _Estimated reading time: 10 min_
> **Prerequisite:** [SQL Basics: DDL & DML](../01-SQL-Basics-DDL-DML/01-concepts/01-ddl-dml-anatomy.md)

## In one sentence

**ACID = Atomic, Consistent, Isolated, Durable** — four guarantees a transaction gives you, and
**isolation level = how much of that isolation you trade away for concurrency**.

## Why the pre-test tests this

- Transactions/ACID is 1–2 of the 10 DBMS questions and is mostly vocabulary.
- The exam asks: "Which property does X guarantee?", "Which isolation level prevents dirty reads?",
  "What is the name of this anomaly?".
- These are free marks once the vocabulary is locked in. Ananya scores them all; she just never
  studies this topic.

## Core concept

### 1. The four properties

| Property | Guarantees | Mechanism | If it fails you get |
|---|---|---|---|
| **A**tomicity | All operations succeed, or **none** do | Transaction log, undo/rollback, `ROLLBACK` | A half-done transfer: money out, money not in |
| **C**onsistency | Constraints and rules hold before and after | Keys, FKs, CHECK, triggers | A row that violates a business rule |
| **I**solation | Concurrent transactions do not see each other's partial work | Locks, MVCC, isolation levels | Dirty reads, lost updates |
| **D**urability | Committed changes survive a crash | Write-ahead log, checkpoints, fsync | Lost committed work |

**Memory hook:** *All Changes In Transactions Are Done* — or just A-C-I-D in order.

**The transaction boundary is explicit.** A transaction runs from the first statement (or an
explicit `BEGIN`/`START TRANSACTION`) to a `COMMIT` or `ROLLBACK`.

```sql
START TRANSACTION;
UPDATE accounts SET balance = balance - 500 WHERE acct_id = 1;  -- debit
UPDATE accounts SET balance = balance + 500 WHERE acct_id = 2;  -- credit
COMMIT;   -- both happen, or neither
-- any error before COMMIT → ROLLBACK undoes both
```

### 2. Atomicity — the machinery

| Mechanism | What it does |
|---|---|
| **Transaction log** | Every change is written to a log before the data page is changed |
| **Undo / rollback** | The log is read backwards to reverse uncommitted changes |
| **Redo / recovery** | After a crash, the log is read forwards to reapply committed changes |
| **`ROLLBACK`** | Explicit undo of the current transaction |
| **`SAVEPOINT`** | Partial undo — roll back to a named point, keep the rest |

**Atomicity is about the transaction, not the statement.** A `DELETE` that removes 500 rows in one
statement is atomic by itself. A transfer across two `UPDATE`s needs an explicit transaction to be
atomic.

### 3. Consistency — who enforces it

Consistency is enforced by **constraints**, and the constraints live in the schema:

| Constraint | Enforces |
|---|---|
| `PRIMARY KEY` / `UNIQUE` | No duplicate keys |
| `FOREIGN KEY` | Referential integrity |
| `CHECK` | Column and row-level rules |
| `NOT NULL` | Presence |
| `TRIGGER` | Complex business rules |

Consistency is also a **property of the whole database**, not of one row: total balances conserved,
no negative stock, audit trail complete.

### 4. Isolation — the interesting one

Isolation says a transaction should behave as if it were running **alone**. Real systems run many
transactions at once, so they approximate it via an **isolation level**.

| Level | Dirty read | Non-repeatable read | Phantom read | Typical use |
|---|---|---|---|---|
| **READ UNCOMMITTED** | ✅ possible | ✅ possible | ✅ possible | Nothing useful. Row-level reporting you will redo |
| **READ COMMITTED** | ❌ blocked | ✅ possible | ✅ possible | Default in MySQL, PostgreSQL, Oracle, SQL Server |
| **REPEATABLE READ** | ❌ blocked | ❌ blocked | ✅ possible | MySQL InnoDB default; reporting |
| **SERIALIZABLE** | ❌ blocked | ❌ blocked | ❌ blocked | Financial transfers, anything you cannot redo |

**Stronger level = more locks held longer = fewer concurrent transactions = lower throughput.** That
trade is the whole point of isolation levels.

### 5. The four anomalies

| Anomaly | Definition | Fixed by |
|---|---|---|
| **Dirty read** | You read data another transaction wrote but has **not committed** — and it gets rolled back. Your value was never real | READ COMMITTED and above |
| **Non-repeatable read** | You read a row twice in the same transaction and get **different values**, because another transaction updated and committed in between | REPEATABLE READ and above |
| **Phantom read** | You re-run a `WHERE` query and get **extra rows**, because another transaction inserted and committed matching rows | SERIALIZABLE |
| **Lost update** | Two transactions read the same value and both write back; one update is **silently overwritten** | Explicit locking, `SELECT ... FOR UPDATE`, or optimistic version columns |

**Mnemonic for the anomalies:**
- **Dirty** = read uncommitted.
- **Non-repeatable** = the *row changed*.
- **Phantom** = *new rows appeared*.
- **Lost update** = *both wrote, one vanished*.

**Lost update is not a "read anomaly"** — it is a write-write conflict, and no isolation level
prevents it by itself. You need `SELECT ... FOR UPDATE`, `SELECT ... FOR UPDATE NOWAIT`, or an
optimistic concurrency check (`WHERE version = ?`).

### 6. Concurrency control mechanisms

| Mechanism | How it works | Cost |
|---|---|---|
| **Locking (2PL)** | Transactions take S/X locks; 2PL prevents conflict serializability problems | Blocking, deadlocks |
| **MVCC** | Readers take a snapshot of the data as of a timestamp; writers create new row versions | Storage for old versions, no read locks |
| **Timestamp ordering** | Each transaction gets a timestamp; conflicts are resolved by comparing timestamps | Aborts transactions |
| **Optimistic concurrency** | Read, verify the version is unchanged, then write | Retries under contention |

### 7. Two-Phase Locking (2PL)

Every transaction locks in **two phases**:

```
GROWING PHASE      →  may take shared (S) and exclusive (X) locks
                    →  may hold many locks
                    ↓
SHRINKING PHASE    →  may release locks (X then S)
                    →  may NOT acquire any new lock
```

**The rule that matters:** once you release a lock, you can never take another. A transaction is in
the growing phase until its first release, then in the shrinking phase forever.

| Property | 2PL gives you |
|---|---|
| Conflict serializability | ✅ Yes — the guarantee 2PL is famous for |
| Cascading locks | ⚠️ Yes — a released S lock may be taken by another txn, so a later release can block |
| Deadlock freedom | ❌ No — deadlock is still possible, and more likely than with strict 2PL |
| Recoverability | ⚠️ Not by itself — needs strict 2PL (all X locks held until commit) |

**Rigorous 2PL** (all exclusive locks held until commit) prevents cascading locks and gives
recoverability.

### 8. Deadlocks

**Definition:** two or more transactions each hold a resource the other needs, so each waits for the
other forever.

```
T1: locks A              T2: locks B
T1: wants B  ─┐         T2: wants A  ─┐
             └─ deadlock ─┘
```

| Strategy | How |
|---|---|
| **Prevention** | Consistent lock ordering; **wait-die** (older txn waits); **wound-wait** (older txn preempts); lock timeouts |
| **Detection** | Build a **wait-for graph**; a **cycle** means deadlock |
| **Recovery** | Pick a **victim**, roll it back, release its locks, let it retry |

**Deadlock is a liveness problem, not a safety problem.** The database stays consistent; it just
stops making progress until the deadlock is broken.

### 9. Schedules and serializability

| Term | Meaning |
|---|---|
| **Serial schedule** | Transactions run one after another, no interleaving |
| **Concurrent schedule** | Transactions interleave their operations |
| **Conflict** | Two operations on the **same item**, at least one a **write** |
| **Conflict equivalence** | Two schedules have the same conflict order on every item |
| **Conflict serializability** | A schedule is conflict-serializable if it is conflict-equivalent to some serial schedule |
| **View serializability** | Equivalent to some serial schedule **as seen by a particular query** — weaker |
| **Recoverable schedule** | No transaction reads uncommitted data (no dirty reads) |

**Rule of thumb:** if a schedule has a **cycle** in its precedence graph, it is **not**
conflict-serializable.

### 10. Distributed transactions — 2PC

| Phase | What happens |
|---|---|
| **Prepare** | Every participant says "I can commit" and flushes its log to disk |
| **Commit** | The coordinator tells everyone to commit — decision is **unanimous** |

**The problem:** if the coordinator dies between prepare and commit, participants are stuck in an
**in-doubt** state. 2PC is **blocking** for this reason.

### 11. MVCC — one paragraph

Multi-Version Concurrency Control keeps **multiple versions** of each row. A reader takes a
**snapshot** at its transaction start and sees the version that was current then. Writers do not
block readers; they create a new version. Old versions are reclaimed later (by a **vacuum** in
PostgreSQL, or the **purge** thread in InnoDB). MVCC gives **snapshot isolation** — which in
PostgreSQL still allows serialization failures, so Postgres adds `SERIALIZABLE` on top.

## Worked example

**Q. Transaction T1 and T2 run concurrently. T1 reads `balance` from a row that T2 has updated but
not committed. T2 then rolls back. What is the anomaly, and which isolation level prevents it?**

- A. Phantom read — REPEATABLE READ
- B. Dirty read — READ COMMITTED
- C. Lost update — REPEATABLE READ
- D. Non-repeatable read — READ UNCOMMITTED

**Solution**

T1 read data that was **never committed** and was subsequently rolled back. The value T1 held was
phantom — it did not exist in any committed state. That is the definition of a **dirty read**.

A dirty read requires **READ UNCOMMITTED**. Any level at or above **READ COMMITTED** blocks it.

**Answer: B (Dirty read — READ COMMITTED).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | A phantom read is **extra or missing rows** appearing on a re-run of a `WHERE` query, not a row read before commit |
| C | A lost update happens when two transactions **write** the same row and one write is overwritten. Here the transaction only read |
| D | A non-repeatable read is the **same row** returning a **different value** because it was updated **and committed**. Here the value was never committed, and no update happened between two reads |

**Quick check on the other levels**

| Level | Dirty read? |
|---|---|
| READ UNCOMMITTED | ✅ allowed |
| READ COMMITTED | ❌ blocked |
| REPEATABLE READ | ❌ blocked |
| SERIALIZABLE | ❌ blocked |

## Quick rules

- **Atomicity** = all or nothing → rollback, transaction log.
- **Consistency** = constraints hold → keys, FKs, CHECK, triggers.
- **Isolation** = transactions do not see partial work → locks or MVCC.
- **Durability** = committed work survives → write-ahead log, checkpoints.
- Dirty read → needs READ COMMITTED. Non-repeatable → REPEATABLE READ. Phantom → SERIALIZABLE.
- **Lost update is a write conflict** — no isolation level fixes it by itself.
- 2PL = grow then shrink; after the first release, **no new locks**.
- Deadlock → prevention, detection (wait-for graph cycle), or victim rollback.

## Common traps

| Trap | What you get | What you should get |
|---|---|---|
| "Isolation prevents lost updates" | ✅ | ❌ Lost update needs explicit locking or a version check |
| "Dirty read = non-repeatable read" | — | Dirty = uncommitted; non-repeatable = changed and committed |
| "Phantom = extra column" | — | Phantom = extra **rows** |
| "2PL prevents deadlock" | ✅ | ❌ Deadlock is still possible |
| "Serializable is the fastest level" | — | It is the most restrictive and usually the slowest |
| "Atomicity means each statement is atomic" | — | It means the **whole transaction** is all-or-nothing |

## Checklist

- [ ] I can spell ACID and name the mechanism behind each property.
- [ ] I know which isolation level blocks which anomaly.
- [ ] I can define all four anomalies in one line each.
- [ ] I know lost updates need explicit concurrency control.
- [ ] I can describe the two phases of 2PL and its guarantee.
- [ ] I know the three deadlock strategies and the wait-for graph test.

## Related

- [Concurrency control procedures](../02-techniques/01-concurrency-control-procedures.md)
- [Solved ACID and transactions set](../03-worked-examples/01-solved-acid-transactions-set.md)
- [ACID and transaction traps](../04-pitfalls/01-acid-transaction-traps.md)
- [ACID and transactions quick check](../05-reference/01-acid-transactions-quick-check.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
