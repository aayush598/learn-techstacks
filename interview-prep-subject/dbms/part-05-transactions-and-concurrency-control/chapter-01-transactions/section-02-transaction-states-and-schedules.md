# Transaction States and Schedules

> **TL;DR**: Every transaction moves through a small set of states (active → partially committed → committed, or failed → aborted), and a *schedule* is just a way of interleaving the steps of several transactions — the object of study that lets us decide if concurrent execution is safe.

## 1. Why Does This Exist?
A transaction isn't a magic instant — it's a *process* that begins, does work, and finishes, and at any moment it may be interrupted by a crash, a timeout, or a deadlock. To reason about (and implement) recovery and concurrency control, we need (a) a precise model of a transaction's *lifecycle* (its states and transitions) and (b) a precise way to *write down an interleaved execution* (a schedule). Both exist so that "did this execution produce correct results?" becomes a formal, checkable question rather than a vibe. States drive *what recovery must do* (undo vs redo); schedules drive *what concurrency control must prevent*.

## 2. How Does It Work?
A transaction is modeled as a sequence of operations `read(X)`, `write(X)`, plus `commit`/`abort`. Its lifecycle: **Active** (working) → **Partially committed** (final statement executed, but not yet recorded as done) → **Committed** (the commit record is durably written) — or from Active → **Failed** (some error/crash) → **Aborted** (rolled back, changes undone, possibly restarted). A schedule is an ordering of the operations of N transactions, preserving each transaction's internal order. If the operations of different transactions are *not* interleaved, the schedule is **serial**; if they are interleaved but the result is still equivalent to a serial execution, it's **serializable** (details in Section 03).

## 3. When Is It Used?
- Whenever a DBMS must decide, after a crash, which transactions to *redo* (committed but not flushed) and which to *undo* (uncommitted) — this is the state model feeding ARIES/undo-redo recovery (Part 06).
- Whenever a concurrency control protocol must decide whether two transactions conflict — it looks at the schedule and the order of conflicting operations.
- In interviews: "draw the transaction state diagram", "which transactions survive a crash?", "what is a schedule?", "serial vs serializable".

## 4. Why Wasn't Another Approach Chosen?
- *Modeling a transaction as a black box (just "runs" or "doesn't")*: too coarse — can't reason about interleaving, can't recover a half-run transaction, can't schedule. The step-by-step operation model is the minimum granularity at which correctness is decidable.
- *Treating "partially committed" and "committed" as one state*: rejected because there is a real window — after the last statement runs but before the commit record is durable — where a crash must still roll the transaction back (it was not "committed" to the log). Recovery depends on distinguishing them.
- *Allowing arbitrary reordering in a schedule*: rejected because operations within one transaction have an order that *must* be preserved (a transaction reads before it writes its own result). Schedules only reorder *across* transactions.
- *Only studying serial execution*: trivially safe but zero concurrency; the whole point is that we want *some* interleaving — so we define equivalence to serial instead of requiring serial.

## 5. Intuition
Think of a transaction as a **legal contract being drafted**. It's *active* while you're writing clauses. When the final clause is written, you're "partially committed" — the document is complete but not yet notarized (signed and registered). If the notary (log) never records it, a fire (crash) means the contract never happened (aborted). Once notarized (commit record durable), it's *committed* — binding forever. A *schedule* is like a busy law firm: several lawyers each drafting their own contracts, and the timeline shows whose pen-strokes happened when. If the interleaving of their work could never produce a result that a "do them one at a time" run would, the firm's workflow is *serializable* — safe.

## 6. Real-World Analogy
A **recipe executed by multiple chefs on shared ingredients**. A transaction is one recipe (active → ready to plate → served/committed, or burnt/failed → discarded/aborted). A schedule is the kitchen's timeline showing interleaved steps of several recipes. If two chefs both need the same bowl of flour and one uses it *while* the other is measuring from it, the dishes come out wrong — that's a non-serializable schedule. The kitchen rule "only one chef touches a bowl at a time, and finish before handing over" is 2PL (Chapter 02); the timeline with that rule enforced is a serializable schedule.

## 7. Formal Definition
**States**: A transaction T is **active** while executing its operations. It is **partially committed** after its final operation has executed but before the commit record is written to stable storage. It is **committed** after the commit record is durably stored. If it cannot proceed (error, abort, system failure), it becomes **failed**, and after its effects are undone it is **aborted**; an aborted transaction may be restarted. (Silberschatz Ch. 15.)
**Schedule**: Given transactions T₁..Tₙ, a schedule S is an ordering of all operations of T₁..Tₙ (preserving the order of operations *within* each Tᵢ) with a commit/abort marker for each. A schedule is **serial** if the operations of each transaction appear consecutively (no interleaving). A schedule is **serializable** if it is equivalent (conflict- or view-equivalent) to some serial schedule. A **complete schedule** includes a commit/abort for every transaction.

## 8. Example
Two transactions:
- T₁: `read(A); A := A − 100; write(A); read(B); B := B + 100; write(B); commit`
- T₂: `read(A); temp := A*1.1; A := temp; write(A); commit`

**Serial schedule**: `T₁ then T₂` (or `T₂ then T₁`). In serial order, either T₁'s transfer fully happens before T₂'s interest accrual, or vice versa — both are "correct" outcomes, though different final states.
**Non-serial (interleaved) schedule**: `r₁(A); w₁(A); r₂(A); w₂(A); ...` — T₂ reads A *after* T₁ debited but *before* T₁ credited B. This interleaving may produce a different (wrong) final state than any serial run, e.g., the interest is computed on the wrong balance or a lost update occurs.

**State walkthrough**: T₁ executes its last `write(B)` → **active→partially committed**. System writes commit record to log and flushes → **committed**. If instead a crash occurs between "last operation" and "log flush" → **failed**, and recovery rolls back T₁ (undo) since no commit record exists.

## 9. Internal Working
1. `BEGIN` → DBMS allocates TXID, marks state **active**, associates a recovery-era identity (an undo/redo scope — the set of log records it will produce).
2. Each operation generates a log record tagged with the TXID; the concurrency control layer records conflicts (reads/writes + locks).
3. Last statement completes → state **partially committed**: the DBMS stops executing, must now persist the commit marker. If any constraint check fails at this point, it transitions to **failed** instead.
4. Commit record written to WAL + flushed (group commit can batch several) → state **committed**; locks released; the transaction's dirty pages can be written to disk lazily (no need to force data pages — the log has enough to redo).
5. On error/deadlock/system failure while active → **failed** → recovery performs undo (or the DBMS performs a local rollback): reads undo records, restores before-images, releases locks → **aborted** → optionally restart (new TXID).
6. Schedules are materialized by the *scheduler* component: it takes each transaction's operation requests and either grants them (letting them interleave), delays them (waiting for a lock), or rejects them (abort).

## 10. Time Complexity
- Tracking states: O(1) per transition — a descriptor field and a log record.
- Building/checking a schedule for serializability: conflict-graph check is O(N + E) for N transactions and E conflicting operations (topological sort); brute-force equivalence checks are exponential, which is why we use polynomial-time conflict tests (Section 03).
- Recovery state reconstruction: O(number of log records) to replay, but checkpointing bounds it (Part 06).

## 11. Advantages
- State model cleanly separates "should this be redone or undone" — the core of every recovery algorithm.
- Schedules give a formal, decidable notion of "safe interleaving" independent of any specific protocol.
- The model is engine-agnostic: the same states/schedules appear in textbooks and in the ARIES-based engines of Postgres, MySQL, and SQL Server.

## 12. Disadvantages
- The schedule model assumes each operation is a single read/write on a data item — real engines operate on pages and index nodes, so "data item" granularity must be defined (lock granularity, Section 02 Chapter 02).
- Serializability as a *global* property is NP-hard to test in general (though conflict serializability is polynomial).
- The state model abstracts away the messy reality of nested transactions, distributed transactions, and aborts mid-protocol (e.g., a transaction aborting inside a lock protocol).

## 13. Interview Questions
1. **Q: What are the states of a transaction?** A: Active (executing), Partially committed (final operation done, commit not yet durable), Committed (commit record on stable storage), Failed (couldn't proceed), Aborted (rolled back). Some models simplify to Active/Aborted/Committed; the distinction active→partially committed→committed matters for recovery.
2. **Q: What is the difference between a serial schedule and a serializable one?** A: Serial = no interleaving at all (transactions run back-to-back). Serializable = interleaved, but *equivalent* (conflict- or view-equivalent) to some serial schedule — i.e., produces the same result as running them one at a time. Serializability allows concurrency without sacrificing correctness.
3. **Q: Draw and explain the transaction state diagram.** A: Active → (execute final op) → Partially committed → (commit record flushed) → Committed; Active → (error/abort requested) → Failed → (rollback) → Aborted; also Active → (can't proceed) → Failed. The key: partial-commit is the moment between "last operation" and "log durable", where a crash still aborts.
4. **Q: Which transactions must be redone and which undone after a crash?** A: Redo: those whose commit record is in the log (committed, but their data pages may not have reached disk). Undo: those with no commit record (active or partially committed) whose changes may be on disk. This is the fundamental rule behind ARIES and WAL recovery.
5. **Q: What is a schedule, formally?** A: An interleaving of the operations (reads, writes, commits, aborts) of a set of transactions that preserves the order of operations within each transaction. A complete schedule includes each transaction's commit/abort.
6. **Q: TRICKY: If a crash happens when a transaction is partially committed, what happens?** A: It is treated as *failed* and rolled back, because no commit record reached stable storage. "Partially committed" is a fiction from the transaction's perspective — from recovery's perspective only the log matters.
7. **Q: What is the difference between a schedule and a serialization order?** A: The schedule is the actual interleaved execution; the serialization order is the serial order (e.g., the topological order of the conflict graph) that the schedule is equivalent to. A serializable schedule has at least one serialization order.
8. **Q: Can a non-serial schedule be correct?** A: Yes — that's the definition of serializable: it's non-serial (interleaved) but equivalent to a serial one. Non-serial is not inherently wrong; *non-serializable* is the problem.
9. **Q: What is an incomplete schedule?** A: One where some transactions haven't committed or aborted yet — the live prefix of an execution. Recovery and concurrency control must handle incomplete schedules; correctness is judged on *complete* schedules.
10. **Q: PRACTICAL: What happens to a transaction that hits a deadlock in a real DBMS?** A: The DBMS picks a victim, aborts it (transition active→failed→aborted), rolls back its changes, releases its locks, and the app retries. Deadlock is a *failure state* of the transaction, handled exactly like the state diagram's failed branch.
11. **Q: Why do we preserve intra-transaction order in a schedule?** A: Because a transaction's operations are causally dependent (it reads values it previously wrote; an update is read-modify-write). Reordering its own operations would change its semantics — the schedule is only free to reorder across transactions.
12. **Q: TRICKY: Is "committed but not durable" possible?** A: Yes, transiently — commit returns after the commit record is *in the log buffer*, but true durability needs the flush. With `synchronous_commit=off` (Postgres) or `innodb_flush_log_at_trx_commit=0/2` (MySQL), a commit can be acknowledged before the log is on disk, risking loss of *recently committed* transactions on crash — a deliberate durability/latency trade-off.
13. **Q: What does "restarted transaction" mean?** A: An aborted transaction can be started again as a *new* transaction (new TXID). Retry is done by the application; the DBMS doesn't auto-restart (except some deadlock retries). Restarting is how the system eventually completes work that transiently failed.
14. **Q: PRODUCTION: What does MySQL's `SHOW ENGINE INNODB STATUS` show about transaction states?** A: It lists transactions with their state (running/rolled back), lock waits, undo log growth, and history list length — a live view of the active/aborted/committed model at work in production.

## 14. Follow-Up Questions
1. **Q: How does a checkpoint interact with the state model?** A: A checkpoint ensures all data pages for certain transactions are on disk before it's recorded; recovery then only needs to examine log *after* the checkpoint (Part 06), reducing undo/redo work.
2. **Q: In distributed transactions, what replaces "commit record on stable storage"?** A: 2PC: the coordinator forces a *prepare* log record, then after all participants agree, forces a *commit* record. The partially-committed/committed distinction becomes a distributed agreement question.
3. **Q: What is the difference between serializability and linearizability?** A: Serializability is about *database* transaction interleaving (no real-time constraint); linearizability (distributed systems) requires the result to respect *real-time order* of operations. A serializable execution may be non-linearizable.

## 15. Coding Example
```pseudocode
// Minimal transaction lifecycle simulation
transaction T:
  state = ACTIVE
  while state == ACTIVE:
      op = next_operation()
      if op is None:                     # final statement executed
          state = PARTIALLY_COMMITTED
      elif op is an error or abort requested:
          state = FAILED
  if state == PARTIALLY_COMMITTED:
      append_log({txid: T.id, type: COMMIT})   # order matters!
      flush_log()                              # durable only after this
      state = COMMITTED
  elif state == FAILED:
      append_log({txid: T.id, type: ABORT})
      for rec in undo_records(T.id):           # restore before-images
          write_page(rec.page_id, rec.before_image)
      release_locks(T.id)
      state = ABORTED
```
```sql
-- Real engines: observe the state transitions via these
SHOW TRANSACTION ISOLATION LEVEL;
SELECT * FROM pg_stat_activity WHERE state <> 'idle';  -- Postgres transaction states
SHOW ENGINE INNODB STATUS;                            -- MySQL: transaction list + states
```

## 16. Industry Usage
- **ARIES recovery** (used by IBM DB2, and the conceptual base of Postgres/MySQL WAL) implements exactly the active/partially-committed/committed + undo/redo split. The state "partially committed" corresponds to "commit record written but not yet flushed / redo not complete."
- **PostgreSQL** exposes transaction state via `pg_stat_activity.state` ('active', 'idle in transaction', 'idle in transaction (aborted)', 'idle', 'fastpath function call', 'disabled') — a direct production mapping of the lifecycle.
- **MySQL InnoDB** transaction state lives in `information_schema.innodb_trx` (`trx_state` = RUNNING/LOCK WAIT/ROLLING BACK/COMMITTING).
- **SQL Server** and Oracle track the same lifecycle internally, and their recovery restarts mid-transaction exactly per the failed→aborted path.
- **Spanner/CockroachDB** extend the state model: a transaction is active → prepared (2PC) → committed/aborted across replicas; the "partially committed" window becomes a distributed *prepared* state.

## 17. References
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 15.1–15.2 (Transaction concept, states) — the classic state diagram (Fig. 15.4).
- Elmasri & Navathe, *Fundamentals of Database Systems*, Ch. 20.1.
- PostgreSQL docs: https://www.postgresql.org/docs/current/monitoring-stats.html (`pg_stat_activity.state`)
- MySQL 8.0 docs: https://dev.mysql.com/doc/refman/8.0/en/innodb-information-schema-transactions.html (`innodb_trx`)
- Mohan et al., "ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging" (1992).

## 18. Cheat Sheet
- States: Active → Partially committed → Committed | Failed → Aborted.
- Committed requires the commit record durable on stable storage — otherwise a crash → aborted.
- Failed transactions get undone (rolled back); committed ones get redone if their pages didn't reach disk.
- Schedule = interleaving preserving each transaction's internal order; serial = no interleaving; serializable = equivalent to serial.
- Aborts can be followed by restarts (new TXID).
- Recovery only trusts the log, not the data pages.

## 19. Quiz
1. Which state immediately precedes Committed? a) Active b) Failed c) Partially committed d) Aborted → **c**
2. A crash after the last statement but before the commit log flush → a) committed b) aborted c) restarted d) partial commit → **b**
3. A schedule where transactions run with no interleaving is: a) serializable b) serial c) conflict-free d) deadlock-free → **b**
4. Which property must a schedule preserve? a) alphabetical order b) intra-transaction operation order c) global order of writes d) none → **b**
5. After a crash, committed transactions are: a) undone b) redone if pages may be missing c) ignored d) all restarted → **b**
6. Serializable means: a) serial b) equivalent to a serial schedule c) conflict-free d) no interleaving → **b**
7. The DBMS trusts ____ for recovery decisions. a) buffer pool b) data pages c) the log d) the application → **c**
8. An aborted transaction can be: a) never re-run b) restarted as a new transaction c) committed anyway d) partially committed → **b**

## 20. Flashcards
- **Q: List transaction states in order.** → **A:** Active → Partially committed → Committed; and Active → Failed → Aborted.
- **Q: What's the difference between serial and serializable?** → **A:** Serial = no interleaving; serializable = interleaved but equivalent to a serial schedule.
- **Q: When does a crash abort a transaction?** → **A:** When no commit record is durable in the log (active/partially committed).
- **Q: Which transactions need redo after a crash?** → **A:** Committed ones whose data pages may not be on disk.
- **Q: What is a schedule?** → **A:** An interleaving of operations of several transactions preserving each one's internal order.
- **Q: What replaces "commit record" in distributed transactions?** → **A:** 2PC prepare + commit records with all participants.
- **Q: What state does a deadlock victim enter?** → **A:** Failed → Aborted, then app retries.

## 21. Revision
A transaction moves active → partially committed → committed (once the commit log record is durable) or active → failed → aborted. Recovery: redo committed, undo the rest — the log is the only source of truth. A schedule is the interleaving of several transactions' operations preserving intra-transaction order; serial = no interleaving; serializable = equivalent to a serial schedule. These definitions set up Section 03 (how to test serializability) and Chapter 02 (protocols that force schedules to be serializable). If asked about "what happens when my transaction crashes/deadlocks/rolls back," you're answering with this state model.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Draw the transaction state diagram." | 1, 2, 7 |
| "What transactions are redone vs undone after crash?" | 2, 13 |
| "What is a schedule?" | 2, 7, 13 |
| "Serial vs serializable?" | 5, 7, 13 |
| "What happens to a deadlock victim?" | 13, 16 |
| "When is a commit actually durable?" | 13, 18 |
| "How does Postgres expose transaction state?" | 16 |
| "What is a complete schedule?" | 7, 13 |
