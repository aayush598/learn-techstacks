# Concurrency Control Procedures — Answering Transaction Questions in 60 Seconds

> Section 3 · DBMS & SQL · ACID & Transactions · _Estimated reading time: 7 min_
> **Prerequisite:** [ACID and isolation levels](../01-concepts/01-acid-and-isolation-levels.md)

## In one sentence

**Identify the property, identify the anomaly, then read the isolation level off a four-row table —
that is the whole archetype.**

## Why the pre-test tests this

- 1–2 questions, and every option in them is a term you either know or do not.
- There is no arithmetic. Knowing the vocabulary *is* the skill.
- Meera can get these right, but only if she has the anomaly table in her head before she reads the
  question.

## Core concept

### Procedure 1 — "Which ACID property does X guarantee?"

| The question mentions | The answer |
|---|---|
| "all or nothing", "rolled back", "half-updated" | **Atomicity** |
| "constraints still hold", "no invalid state", "rules enforced" | **Consistency** |
| "other transactions do not see partial results", "concurrent access" | **Isolation** |
| "committed data survives a crash", "power failure", "recovery" | **Durability** |

**Tie-breakers**

| Ambiguous phrase | Lean |
|---|---|
| "referential integrity maintained" | Consistency (enforced by FK constraints) |
| "no dirty read" | Isolation |
| "undo log / rollback" | Atomicity |
| "write-ahead log / checkpoint / fsync" | Durability |
| "locking or MVCC" | Isolation |
| "constraint, trigger, key" | Consistency |

### Procedure 2 — "What is this anomaly called?"

Read the scenario and look for the tell:

| Tell in the scenario | Anomaly |
|---|---|
| "read a value that was **never committed** / was rolled back" | **Dirty read** |
| "read the **same row** twice, got a **different value**, the other transaction **committed**" | **Non-repeatable read** |
| "re-ran a **query**, got **extra rows** / **missing rows**" | **Phantom read** |
| "both **wrote**, one update **disappeared**" | **Lost update** |

**Decision order**

```
Was the data COMMITTED?  ──no──▶ Dirty read
        │ yes
Did the ROW's VALUE change between two reads? ──yes──▶ Non-repeatable read
        │ no
Did the SET OF ROWS change between two reads? ──yes──▶ Phantom read
        │ no
Did one WRITE get overwritten? ──yes──▶ Lost update
```

### Procedure 3 — "Which isolation level?"

Build the answer from the anomaly: the **weakest** level that blocks it.

| Requirement | Answer |
|---|---|
| Block dirty reads | **READ COMMITTED** |
| Block dirty + non-repeatable reads | **REPEATABLE READ** |
| Block all three | **SERIALIZABLE** |
| Block nothing | READ UNCOMMITTED |

**The four-row table to memorise**

| Level | Dirty | Non-repeatable | Phantom |
|---|---|---|---|
| READ UNCOMMITTED | allowed | allowed | allowed |
| READ COMMITTED | blocked | allowed | allowed |
| REPEATABLE READ | blocked | blocked | allowed |
| SERIALIZABLE | blocked | blocked | blocked |

**Default levels to remember**

| DBMS | Default |
|---|---|
| MySQL InnoDB | REPEATABLE READ |
| PostgreSQL | READ COMMITTED |
| Oracle | READ COMMITTED |
| SQL Server | READ COMMITTED (locking) |

### Procedure 4 — "Which concurrency control mechanism?"

| The question mentions | The answer |
|---|---|
| "readers do not block writers", "snapshots", "multiple versions" | **MVCC** |
| "shared / exclusive locks", "two phases", "grow then shrink" | **2PL** |
| "check the version before writing", "retry on conflict" | **Optimistic concurrency control** |
| "timestamps decide who wins" | **Timestamp ordering** |
| "each transaction waits or is preempted based on age" | **Wait-die / wound-wait** |
| "graph of waits, cycle" | **Deadlock detection** |

### Procedure 5 — "Is it serializable / conflict-serializable?"

1. List the transactions and their operations on each item.
2. Find the **conflicts**: same item, at least one operation is a write.
3. Draw the **precedence graph**: edge `Ti → Tj` if `Ti` conflicts with `Ti` **and comes first**.
4. **Cycle in the graph → NOT conflict-serializable.**
5. **No cycle → conflict-serializable** (and equivalent to some serial order).

**Time budget**

| Seconds | Activity |
|---|---|
| 0–15 | Find the ACID property or the anomaly |
| 15–35 | Match to the table |
| 35–50 | Check the distractors |
| 50–60 | Mark and move |

### Procedure 6 — the 6-option trap

Transaction questions often offer "SERIALIZABLE" as the answer to everything. It is the strongest
isolation level, so it always **blocks** the anomaly — but the exam usually wants the **weakest
level that blocks it**, or it wants the level that **permits** it.

| Question type | What to pick |
|---|---|
| "Which level prevents X?" | The **weakest** level that blocks X |
| "Which level allows X?" | The **strongest** level that still allows X |
| "Which level is used for financial transfers?" | SERIALIZABLE |
| "Which level is the default in MySQL?" | REPEATABLE READ |

## Worked example

**Q. Under which isolation level can a transaction read another transaction's uncommitted changes?**

- A. READ COMMITTED
- B. SERIALIZABLE
- C. READ UNCOMMITTED
- D. REPEATABLE READ

**Solution**

Reading another transaction's **uncommitted** changes is a **dirty read**. By definition only
**READ UNCOMMITTED** permits it — every higher level blocks uncommitted reads.

**Answer: C (READ UNCOMMITTED).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | READ COMMITTED's entire purpose is to block dirty reads |
| B | SERIALIZABLE blocks every anomaly |
| D | REPEATABLE READ blocks dirty reads too |

---

**Q2. Which isolation level is required to prevent phantom reads?**

- A. READ UNCOMMITTED
- B. READ COMMITTED
- C. REPEATABLE READ
- D. SERIALIZABLE

**Solution**

A phantom is a **row** appearing or disappearing between two executions of the same `WHERE` query.
REPEATABLE READ guarantees that the rows you already read stay the same, but it does not stop new
rows from matching your predicate. Only **SERIALIZABLE** blocks that.

**Answer: D (SERIALIZABLE).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Blocks nothing |
| B | Blocks only dirty reads |
| C | Blocks dirty and non-repeatable reads, but not phantoms |

---

**Q3. Two transactions read `balance = 1000`, both compute a new value, and both write it back.
One transaction's write vanishes. What is this, and what fixes it?**

- A. Dirty read — use READ COMMITTED
- B. Non-repeatable read — use REPEATABLE READ
- C. Lost update — use `SELECT ... FOR UPDATE` or an optimistic version check
- D. Phantom read — use SERIALIZABLE

**Solution**

Both transactions **wrote** the same row and one write was overwritten. No isolation level fixes
this by itself — you need **explicit** concurrency control: `SELECT ... FOR UPDATE` (pessimistic) or
a version column checked in the `WHERE` clause (optimistic).

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Nothing was read that was uncommitted. The problem is a write-write conflict |
| B | The row did not change value between reads — both read 1000 |
| D | No rows appeared or disappeared |

## Quick rules

- Property first: all-or-nothing → Atomicity; rules hold → Consistency; no partial views →
  Isolation; survives crash → Durability.
- Anomaly tells: uncommitted → dirty; same row different value → non-repeatable; extra rows →
  phantom; write overwritten → lost update.
- Weakest level that blocks: dirty → RC; non-repeatable → RR; phantom → SERIALIZABLE.
- Lost update needs explicit locking or a version check.
- 2PL = grow, then shrink; no new locks after the first release.
- Cycle in the precedence graph → not conflict-serializable.

## Common traps

| Trap | Why the option is wrong |
|---|---|
| "SERIALIZABLE" for every "prevent" question | The exam usually wants the weakest sufficient level |
| Isolation "prevents lost updates" | It does not; no level does on its own |
| Confusing non-repeatable with phantom | Row value vs row count |
| 2PL prevents deadlock | It does not |
| REPEATABLE READ prevents phantoms | It does not |

## Checklist

- [ ] I can name the property from the phrase.
- [ ] I can name the anomaly from the tell.
- [ ] I can recite the four-row isolation table.
- [ ] I know the default level in MySQL and PostgreSQL.
- [ ] I know the four deadlock strategies.
- [ ] I can draw a precedence graph and spot a cycle.

## Related

- [ACID and isolation levels](../01-concepts/01-acid-and-isolation-levels.md)
- [Solved ACID and transactions set](../03-worked-examples/01-solved-acid-transactions-set.md)
- [ACID and transaction traps](../04-pitfalls/01-acid-transaction-traps.md)
- [ACID and transactions quick check](../05-reference/01-acid-transactions-quick-check.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
