# ACID and Transactions — 8 Solved Questions

> Section 3 · DBMS & SQL · ACID & Transactions · _Estimated reading time: 11 min_
> **Prerequisite:** [Concurrency control procedures](../02-techniques/01-concurrency-control-procedures.md)

## In one sentence

Eight transaction questions — properties, anomalies, isolation levels, locking and deadlock — each
solved by matching the phrase to the table.

## Why the pre-test tests this

- Transactions/ACID is 1–2 of the 10 DBMS questions and is pure vocabulary.
- The distractors are always the same: the wrong isolation level, the wrong anomaly, or the wrong
  property.

## Core concept

### The phrase → answer map

```
all or nothing / rollback                 → Atomicity
constraints hold / valid state             → Consistency
don't see partial work / concurrent        → Isolation
survives crash / committed work persists   → Durability
```

```
uncommitted data read                      → Dirty read
same row, new value, committed             → Non-repeatable read
same query, new rows                       → Phantom read
both wrote, one vanished                   → Lost update
```

```
block dirty        → READ COMMITTED
block non-repeat.  → REPEATABLE READ
block phantom      → SERIALIZABLE
```

## Worked example

### Q1 — Answer **C** (Isolation)

**Two transactions update the same row at the same time. A transaction must not see another
transaction's uncommitted changes. Which ACID property guarantees this?**

- A. Atomicity
- B. Consistency
- C. Isolation
- D. Durability

**Solution**

The requirement is that a transaction does not observe other transactions' **partial, uncommitted**
work. That is exactly the definition of **Isolation**.

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Atomicity is about a transaction either completing fully or not at all |
| B | Consistency is about constraints and rules remaining valid |
| D | Durability is about committed data surviving a crash |

---

### Q2 — Answer **D** (SERIALIZABLE)

**Which isolation level is required to prevent phantom reads?**

- A. READ UNCOMMITTED
- B. READ COMMITTED
- C. REPEATABLE READ
- D. SERIALIZABLE

**Solution**

A phantom is **new or missing rows** appearing when the same `WHERE` query is re-run. REPEATABLE
READ pins the rows you already read but does not stop new rows from matching the predicate. Only
SERIALIZABLE blocks that.

**Answer: D.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Blocks nothing |
| B | Blocks only dirty reads |
| C | Blocks dirty and non-repeatable reads, but new rows can still appear |

---

### Q3 — Answer **B** (Non-repeatable read)

**A transaction reads `EMP_NAME = 'Ananya'` from a row, then later reads the same row and gets
`'Ananya Rao'`. The other transaction committed its update in between. What is this anomaly?**

- A. Dirty read
- B. Non-repeatable read
- C. Phantom read
- D. Lost update

**Solution**

The **same row** returned a **different value** on a second read, and the change was
**committed**. That is a non-repeatable read.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | A dirty read involves data that was **never committed** — here the change was committed |
| C | A phantom is about the **number of rows** matching a query changing, not one row's value |
| D | No write was lost. Both values existed at different times |

---

### Q4 — Answer **A** (Atomicity)

**A transaction transfers money between two accounts. After the debit succeeds, the credit fails
because of a constraint violation. What guarantee ensures the debit is undone?**

- A. Atomicity
- B. Consistency
- C. Isolation
- D. Durability

**Solution**

"Everything happened, or nothing happened" is the definition of **Atomicity**. The failed credit
must not leave the debit in place, so the transaction is rolled back as a unit.

**Answer: A.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | Consistency says the final state obeys the rules — it is the **constraint** that failed, not the mechanism that undoes the debit |
| C | Isolation concerns concurrent transactions, not intra-transaction failure |
| D | Durability is about surviving a crash after a successful commit |

---

### Q5 — Answer **C** (Lost update)

**T1 and T2 both read `stock = 10`. Both compute `stock = 9` and both write it back. The store
actually sold only one item, but the counter dropped by one instead of two. What is this?**

- A. Dirty read
- B. Non-repeatable read
- C. Lost update
- D. Phantom read

**Solution**

Both transactions **wrote** the same row and one write was overwritten. The value written by T2
(or T1) was lost. That is a **lost update**.

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Both transactions read the **committed** value 10. Nothing uncommitted was read |
| B | The value did not change between the two reads — both saw 10 |
| D | No rows were inserted or deleted; one row's value was overwritten |

**The fix** (not asked, but know it): `SELECT ... FOR UPDATE`, or an optimistic version column
checked in the `WHERE` clause.

---

### Q6 — Answer **B** (MVCC)

**A database is configured so that readers never block writers and writers never block readers, and
each reader sees the data as it was at the start of its transaction. Which concurrency control
mechanism is this?**

- A. Two-phase locking
- B. Multi-version concurrency control (MVCC)
- C. Optimistic concurrency control
- D. Timestamp ordering with abort

**Solution**

"Multiple versions" plus "a snapshot as of the transaction start" is the definition of **MVCC**.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | 2PL uses shared/exclusive locks; readers and writers do block each other |
| C | Optimistic control does not block, but it has no snapshot — it detects the conflict at write time and asks the transaction to retry |
| D | Timestamp ordering aborts one of the conflicting transactions rather than letting both proceed |

---

### Q7 — Answer **A** (Two-phase locking, growing then shrinking)

**A transaction acquires shared and exclusive locks, and then releases only its exclusive locks.
Later it tries to acquire a new shared lock and is refused. Which concurrency protocol describes
this?**

- A. Two-phase locking
- B. Strict two-phase locking
- C. Timestamp ordering
- D. Optimistic concurrency control

**Solution**

The transaction took locks (growing phase) and then began releasing them (shrinking phase). Once
the shrinking phase starts, **no new locks** may be acquired — which is precisely 2PL.

**Answer: A.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | Strict 2PL (rigorous 2PL) additionally requires **all exclusive locks to be held until commit**. Here the exclusive lock was released before the end |
| C | Timestamp ordering does not use lock phases at all |
| D | Optimistic control uses no locks |

---

### Q8 — Answer **D** (victim rollback)

**Two transactions each hold a row lock the other needs, and both are waiting. The DBMS detects the
cycle and recovers. What is the standard recovery action?**

- A. Increase the isolation level
- B. Commit both transactions
- C. Kill the entire database and restart
- D. Roll back one transaction (the victim) and let it retry

**Solution**

Deadlock recovery **breaks the cycle** by choosing a **victim**, rolling it back to release its
locks, and allowing it (or the survivor) to proceed. Committing both is not possible — one of them
is blocked by the other.

**Answer: D.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Raising the isolation level does not release locks; it usually takes more of them |
| B | The victim cannot commit — it is blocked by a lock the other transaction holds |
| C | A deadlock does not corrupt data. Restarting the whole DB is not the standard recovery |

## Quick rules

- Property: all-or-nothing → Atomicity; rules hold → Consistency; no partial views → Isolation;
  survives crash → Durability.
- Anomaly: uncommitted → dirty; same row new value → non-repeatable; new rows → phantom;
  write overwritten → lost update.
- Weakest blocking level: dirty → RC; non-repeatable → RR; phantom → SERIALIZABLE.
- Lost update → `SELECT ... FOR UPDATE` or an optimistic version check.
- 2PL → grow then shrink, no new locks after the first release.
- Deadlock → victim rollback.

## Common traps

| Trap | Wrong answer | Right answer |
|---|---|---|
| Pick the strongest level, not the weakest sufficient | D in Q2 | The exam wants the weakest level that blocks the anomaly |
| Miss the "committed" detail | A in Q3 | A dirty read requires uncommitted data |
| Call a write-write conflict a dirty read | A in Q5 | It is a lost update |

## Checklist

- [ ] I can name the property from the phrase.
- [ ] I can name the anomaly from the tell.
- [ ] I can recite the four-row isolation table.
- [ ] I know lost updates need explicit control.
- [ ] I know 2PL vs strict 2PL.
- [ ] I know the deadlock recovery action.

## Related

- [ACID and isolation levels](../01-concepts/01-acid-and-isolation-levels.md)
- [Concurrency control procedures](../02-techniques/01-concurrency-control-procedures.md)
- [ACID and transaction traps](../04-pitfalls/01-acid-transaction-traps.md)
- [ACID and transactions quick check](../05-reference/01-acid-transactions-quick-check.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
