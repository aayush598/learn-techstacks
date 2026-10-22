# ACID and Transactions Quick Check — One Page

> Section 3 · DBMS & SQL · ACID & Transactions · _Estimated reading time: 3 min_
> **Prerequisite:** [Concurrency control procedures](../02-techniques/01-concurrency-control-procedures.md)

## In one sentence

ACID in four rows, the four anomalies in four rows, the four isolation levels in four rows, and the
lock protocol in five lines.

## Why the pre-test tests this

- 1–2 marks. Three minutes of revision converts the archetype into free marks.
- Every distractor in this topic comes from one of the tables on this page.

## Core concept

### ACID

| | Property | Mechanism | Failure looks like |
|---|---|---|---|
| **A** | Atomicity | Transaction log, undo, `ROLLBACK`, `SAVEPOINT` | Half a transfer applied |
| **C** | Consistency | PK, FK, CHECK, NOT NULL, triggers | A rule is violated |
| **I** | Isolation | Locks, MVCC, isolation levels | Dirty read, lost update |
| **D** | Durability | Write-ahead log, checkpoints, fsync | Committed work disappears after a crash |

### The four anomalies

| Anomaly | The tell | First level that fixes it |
|---|---|---|
| **Dirty read** | Read data that was **never committed** | READ COMMITTED |
| **Non-repeatable read** | Same **row**, different **value**, change was **committed** | REPEATABLE READ |
| **Phantom read** | Same **query**, extra/missing **rows** | SERIALIZABLE |
| **Lost update** | Both **wrote**, one **disappeared** | Explicit lock / version check |

### The four isolation levels

| Level | Dirty | Non-repeatable | Phantom | Use it for |
|---|---|---|---|---|
| READ UNCOMMITTED | allowed | allowed | allowed | Nothing |
| READ COMMITTED | blocked | allowed | allowed | Default in Postgres, Oracle, SQL Server |
| REPEATABLE READ | blocked | blocked | allowed | Default in MySQL InnoDB; reporting |
| SERIALIZABLE | blocked | blocked | blocked | Financial transfers |

### Statement syntax

```sql
START TRANSACTION;   -- or BEGIN
SAVEPOINT sp1;
ROLLBACK TO SAVEPOINT sp1;   -- partial undo
COMMIT;    -- make it permanent
ROLLBACK;  -- undo everything
```

### 2PL

```
GROWING   →  take S and X locks, hold many
SHRINKING →  release X then S, take NOTHING new
```

| Property | 2PL |
|---|---|
| Conflict serializability | ✅ |
| Cascading locks | ⚠️ possible |
| Deadlock freedom | ❌ |
| Recoverability | ❌ (needs strict 2PL) |

### Deadlock

| Strategy | Detail |
|---|---|
| Prevention | Consistent lock order; wait-die; wound-wait; timeout |
| Detection | Wait-for graph — a **cycle** means deadlock |
| Recovery | Roll back the **victim**, release locks, retry |

### MVCC in one line

Keep **multiple row versions**; readers take a **snapshot**; writers create a new version; readers
never block writers and vice versa.

### Anomalies → level cheat sheet

| Question asks | Answer |
|---|---|
| Prevent dirty reads | READ COMMITTED |
| Prevent dirty + non-repeatable | REPEATABLE READ |
| Prevent all three | SERIALIZABLE |
| Allow dirty reads | READ UNCOMMITTED |
| Prevent lost updates | `SELECT ... FOR UPDATE` / version column |

### Serializability

| Term | Meaning |
|---|---|
| Conflict | Same item, at least one write |
| Precedence graph | Edge `Ti → Tj` when `Ti` conflicts before `Tj` |
| Conflict-serializable | Graph has **no cycle** |
| Recoverable | No transaction reads uncommitted data |

## Worked example

**Q. Which mechanism provides "readers never block writers, and each reader sees a consistent
snapshot as of its transaction start"?**

- A. Two-phase locking
- B. Multi-version concurrency control
- C. Timestamp ordering with abort
- D. Strict 2PL

**Answer: B.** Multiple row versions + a start-time snapshot is the definition of MVCC.

## Quick rules

- Atomicity = all or nothing. Consistency = rules hold. Isolation = no partial views. Durability =
  survives crash.
- Committed → non-repeatable. Uncommitted → dirty. Row count → phantom. Write overwritten → lost
  update.
- Weakest sufficient level: RC / RR / SERIALIZABLE.
- 2PL grows then shrinks; deadlock still possible.
- Cycle in the wait-for graph → deadlock.

## Common traps

| Trap | Fix |
|---|---|
| Isolation fixes lost updates | No — explicit locking or version check |
| REPEATABLE READ blocks phantoms | No — SERIALIZABLE does |
| 2PL prevents deadlock | No |
| SERIALIZABLE for every "prevent" question | Give the weakest sufficient level |

## Checklist

- [ ] I can recite ACID and the mechanism for each.
- [ ] I can recite the anomaly tells.
- [ ] I can recite the isolation table.
- [ ] I know MySQL's default level and PostgreSQL's.
- [ ] I can describe 2PL and deadlock recovery.
- [ ] I know what MVCC buys.

## Related

- [ACID and isolation levels](../01-concepts/01-acid-and-isolation-levels.md)
- [Concurrency control procedures](../02-techniques/01-concurrency-control-procedures.md)
- [Solved ACID and transactions set](../03-worked-examples/01-solved-acid-transactions-set.md)
- [ACID and transaction traps](../04-pitfalls/01-acid-transaction-traps.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
