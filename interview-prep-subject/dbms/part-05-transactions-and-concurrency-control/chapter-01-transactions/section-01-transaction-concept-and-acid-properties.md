# Transaction Concept and ACID Properties

> **TL;DR**: A transaction is a group of database operations that must succeed or fail as one unit, and ACID (Atomicity, Consistency, Isolation, Durability) is the contract that makes that "as one unit" actually true even under concurrency and crashes.

## 1. Why Does This Exist?
Consider a bank transfer: `balance[Alice] -= 100; balance[Bob] += 100`. If the system crashes between the two statements, or if another transaction reads the balance mid-transfer, money literally appears or disappears. A single SQL statement can't express this — it's *two* updates that must be an indivisible unit. Transactions exist because real-world operations are multi-step and must be atomic (all-or-nothing), isolated (invisible mid-flight), consistent (preserve invariants), and durable (survive crashes). Without a transaction abstraction, application programmers would have to hand-write crash and concurrency handling for every business rule — a correctness nightmare. The transaction + ACID model moves that burden into the database engine where it can be done once, correctly.

## 2. How Does It Work?
The application brackets operations with `BEGIN TRANSACTION` ... `COMMIT` (make permanent) or `ROLLBACK` (undo everything). The DBMS tracks every page the transaction touches. On `COMMIT`, the changes are forced to durable storage (or the commit record is written to a log first — Part 06). On failure or `ROLLBACK`, the DBMS undoes every change. For concurrency, the DBMS's concurrency control protocol (Chapter 02) controls how transactions' read/write steps interleave so each transaction sees a consistent view. In short: atomicity+durability come from recovery (Part 06), isolation comes from concurrency control (this chapter's protocols), and consistency is the application contract the DBMS helps enforce.

## 3. When Is It Used?
- Money movement, order placement, inventory decrement, any "multiple writes must all happen" logic.
- Any time a read must not observe a half-finished update from another session (reporting, analytics over live data).
- Long-running ETL batches that must not expose partial results; schema migrations that must roll back cleanly.
- Distributed systems that want the same guarantee across nodes (Spanner, CockroachDB) — they extend single-node transactions with replication/commit protocols (2PC/Paxos).
- Nearly every production system: e-commerce carts, ride-hailing trip lifecycle, booking engines, ledger systems (double-entry bookkeeping is a transaction by construction).

## 4. Why Wasn't Another Approach Chosen?
- *No atomicity at all (plain writes):* rejected because a crash mid-operation corrupts data; application-level compensation is error-prone.
- *Application-managed atomicity (manual undo logs in app code):* rejected because the app can't see disk-level partial writes, can't be crash-safe without cooperation from the DB, and every developer would re-implement it differently. Centralizing in the DB engine gives one correct implementation.
- *Optimistic "just retry on failure":* retries fix transient errors but not the fundamental need to *hide* partial states from other readers; a reader needs isolation even if the writer eventually succeeds.
- *Full serial execution (a global lock on everything):* gives perfect correctness but zero concurrency — rejected on performance; that's exactly why we need the elaborate machinery of schedules and serializability rather than just "one at a time."
- *Write-ahead-log + undo/redo (recovery) vs shadow paging:* both give durability/atomicity; shadow paging avoids logs but is slow on commit and poor for large DBs, so logging won (details in Part 06).

## 5. Intuition
Think of a transaction as a **single bullet point on a checklist**: "transfer 100 from A to B" is one item, even though it physically requires erasing a digit in two places. The database's job is to make the whole checklist item visible as either *completely done* or *never started* — never "half-done." If a teammate (another transaction) looks at the checklist while you're working, they must see either the old state (before you started) or the new state (after you finished), never your in-progress scribbles. And once you check the box (COMMIT), a flood (crash) must not wash the ink away.

## 6. Real-World Analogy
A **restaurant table order**: a waiter takes your order, the kitchen must prepare *all* courses, and either the full meal arrives at your table or — if the grill catches fire mid-way — the whole order is written off and you're asked to order again. You never receive "half the meal." Other diners (concurrent transactions) sitting nearby never see the half-cooked dishes; the kitchen's pass window (isolation) only shows finished plates. The order book (transaction log) records every order so that after the fire is put out, the kitchen can re-cook (redo) or cancel (undo) correctly. If the manager wrote the order in pencil and water spilled, that's a durability failure — which is why the book (WAL) is written in pen *before* the kitchen starts cooking.

## 7. Formal Definition
A transaction is a sequence of database operations (reads and writes on data items) that constitutes a single logical unit of work, defined to be atomic, consistent, isolated, and durable. **Atomicity**: either all operations are reflected in the database or none. **Consistency**: a transaction, executed alone on a consistent database, must leave the database in a consistent state (it preserves application invariants). **Isolation**: to each transaction, all others appear to execute either entirely before or entirely after it — the execution must be equivalent to some serial execution. **Durability**: after a transaction commits, its effects must persist despite subsequent failures. (Silberschatz, Database System Concepts, Ch. 15.)

## 8. Example
Transfer ₹500 from Alice's account (A=1000) to Bob's (B=200):
```
BEGIN TRANSACTION;
  UPDATE accounts SET balance = balance - 500 WHERE name='Alice';  -- A: 1000 → 500
  UPDATE accounts SET balance = balance + 500 WHERE name='Bob';    -- B: 200 → 700
COMMIT;
```
- If a crash happens between the two UPDATEs, the transaction never commits; recovery undoes the first UPDATE, leaving A=1000, B=200. Atomicity ✓.
- If a concurrent transaction reads A while this one is mid-flight, isolation says it must read 1000 (old) or 500 (new) — never a torn state.
- If Alice had an invariant "balance ≥ 0", the DBMS refuses to commit if the transaction would make A negative. Consistency ✓.
- After COMMIT returns, even a power cut must not lose the transfer. Durability ✓.

## 9. Internal Working
1. Application issues `BEGIN` → DBMS allocates a transaction descriptor (TXID, state=ACTIVE), starts a private view of the database.
2. Each `SELECT`/`UPDATE`/`INSERT` touches pages. For atomicity+durability the DBMS writes *log records* describing the change to the Write-Ahead Log *before* modifying the data page (WAL rule, Part 06). For isolation, the concurrency-control protocol records the transaction's read/write sets (locks, version snapshots, or timestamps — Chapter 02).
3. Application issues `COMMIT` → the DBMS writes a commit log record, then (with `synchronous_commit`) flushes log to stable storage; only then does it return "committed" to the app.
4. Application issues `ROLLBACK` or the system aborts → the DBMS uses the log (undo records) to restore every page the transaction changed to its pre-transaction value, then releases the transaction's locks and marks it ABORTED.
5. Cleanup: MVCC engines reclaim dead versions; the transaction descriptor is freed; counters update.

## 10. Time Complexity
- Per-transaction overhead: the transaction descriptor and log writes are O(1) amortized per operation, but the *durability* flush (fsync) is the expensive part — typically 1–5 ms per commit on spinning disk / SSD, and it's a random-latency cost, not a CPU cost.
- Commit protocol: O(1) log writes locally; O(N) message round-trips for N participants in distributed 2PC (not used in single-node).
- Abort cost: proportional to the number of changed pages that must be undone (O(changes)); MVCC makes aborts cheap by discarding versions (O(1) per version).
- Recovery replay is O(log size) in a crash (Part 06).

## 11. Advantages
- **Atomicity**: no partial writes — the highest-value correctness guarantee in databases.
- **Isolation**: concurrent apps written as if they ran alone; massive simplification of application logic.
- **Durability**: committed data survives crashes; enables trusting the DB with money, orders, state.
- **Standardized**: ACID is vendor-neutral (ANSI/ISO SQL), so skills transfer between Oracle, Postgres, MySQL, SQL Server.
- **Enables higher abstractions**: stored procedures, triggers, and ORM transactions all rely on it.

## 12. Disadvantages
- **Performance**: durability flushes cost latency; isolation machinery (locks/versions) adds overhead to every operation.
- **Lock contention**: pessimistic concurrency can serialize hot rows (the classic "one counter row" bottleneck).
- **NOT the default everywhere**: MySQL/MyISAM had no transactions; many NoSQL stores drop ACID for scale (Part 08), forcing app-level compensation.
- **Consistency is not free**: the DB only enforces declared constraints; business invariants still require app discipline — a "consistent" transaction can encode a bug.
- **Distributed ACID is expensive**: cross-node transactions cost many round-trips (Spanner uses atomic clocks; classic 2PC can block on failures).

## 13. Interview Questions
1. **Q: What is a transaction?** A: A logical unit of work consisting of one or more database operations that must be executed atomically — either all of its effects are applied or none are — and in isolation from other concurrent transactions.
2. **Q: Define each ACID property with a concrete violation.** A: Atomicity — crash mid-transfer leaves money in limbo; Consistency — a transfer that creates negative balance breaks an invariant; Isolation — a concurrent read sees a half-applied transfer; Durability — committed data is lost after power cut. The DBMS mechanisms: atomicity→undo log; isolation→locking/MVCC; durability→redo log + fsync; consistency→constraints (app-level).
3. **Q: Can consistency be fully enforced by the DBMS?** A: No. The DBMS enforces declared constraints (PK, FK, CHECK, NOT NULL), but application invariants like "sum of all balances = constant" or "no overdraft" need triggers or app logic. The transaction model guarantees that *if* you start consistent and obey your invariants, the DB won't corrupt them — it doesn't check them for you.
4. **Q: What's the difference between atomicity and durability?** A: Atomicity is about *partial execution* (all-or-nothing even on abort/crash mid-way); durability is about *time* (once COMMIT returns, effects survive any subsequent failure). A system could be atomic but not durable (in-memory DB that aborts cleanly but loses everything on power loss) or durable but not atomic (without logging, a partial update could be persisted).
5. **Q: Why is a single SQL statement not automatically a transaction you can COMMIT/ROLLBACK?** A: Because many real units of work span multiple statements (transfer = two updates). But note: in most engines a single statement IS atomic on its own (statement-level atomicity is required even in autocommit), while the *transaction* is the group the app declares. Autocommit mode makes each statement its own transaction — fine for single-statement writes, wrong for multi-step ones.
6. **Q: TRICKY: If a transaction does `INSERT` then `SELECT COUNT(*)` on the same table, can it see its own insert before COMMIT?** A: Yes — read-your-own-writes is *required* for correctness within a transaction (a DBMS that hid its own uncommitted writes would break even simple programs). Isolation governs what a transaction sees of *other* transactions, never of itself.
7. **Q: What happens if you run `ROLLBACK` after `COMMIT`?** A: Nothing — the transaction is over; the commit is permanent. ROLLBACK after COMMIT is a no-op (or an error depending on driver). DDL in some engines (MySQL) causes an implicit commit and cannot be rolled back.
8. **Q: Which engines/table types historically had no transactions?** A: MyISAM (MySQL) and early SQLite (off) lacked transactional guarantees (MyISAM: no rollback, table-level locking only). This is why `InnoDB` became MySQL's default in 5.5 — transactions and crash recovery were the differentiator.
9. **Q: What is a "distributed transaction"?** A: A transaction that spans multiple database nodes. It needs a coordinator to decide a single commit/abort outcome (2PC or a consensus protocol). The challenge: "commit" is now a coordination problem, not just a local log flush — network partitions can block or force rollback.
10. **Q: Why do NoSQL systems frequently sacrifice ACID?** A: Because enforcing isolation/atomicity across distributed, partitioned data requires coordination that hurts availability and latency (CAP/PACELC — Part 08). They trade strong isolation for horizontal scale and choose eventual consistency, pushing the "fix it later" logic into the application.
11. **Q: What is a phantom write / "lost update"?** A: Two transactions both read a value, both modify it, and both write — the second write clobbers the first (lost update). ACID isolation at READ COMMITTED may allow it (it's not prevented by row-level locking in a plain engine); SERIALIZABLE or explicit `SELECT FOR UPDATE` prevents it.
12. **Q: PRACTICAL: Should you put business logic in a transaction or a stored procedure?** A: Transactions are a *scope* concept — put the transaction boundary around the unit of work, wherever the logic lives. Stored procedures reduce round-trips and can be transactional; but the transaction should be as short as possible (long transactions hold locks/versions and starve others). Never hold a transaction open across user interaction/network calls.
13. **Q: What is autocommit and when is it dangerous?** A: Autocommit (default in MySQL, psql) commits each statement immediately. Dangerous when a multi-statement workflow "works" because each statement happens to be independent, then a mid-flow failure leaves partial state — which is exactly what explicit transactions prevent.
14. **Q: PRODUCTION: How does an airline booking system use transactions for seat selection?** A: `BEGIN; SELECT * FROM seats WHERE id=? FOR UPDATE; UPDATE seats SET status='booked' ...; COMMIT;`. The `FOR UPDATE` (or an update with a guard) prevents two users from booking the same seat — the classic "lost update" prevented via pessimistic locking.
15. **Q: TRICKY: A transaction writes data, another reads it. If the writer ROLLBACKs, what should the reader have seen?** A: Because of isolation, the reader must *not* have seen the writer's uncommitted data (no dirty read). At a proper isolation level, the reader saw the old committed value. If the reader *did* see the dirty value and the writer rolled back, that's a dirty-read anomaly — only allowed at READ UNCOMMITTED.
16. **Q: Can a transaction be both atomic and partially visible?** A: No — atomicity means the effects are all-or-nothing *as seen by other transactions*. However, internally a DBMS can have partially applied changes (pages in the buffer pool) as long as isolation hides them. Atomicity is about *observability*, not physical simultaneity.
17. **Q: What is the difference between COMMIT and a plain write reaching disk?** A: A plain write can be in the OS page cache (not durable). A COMMIT forces the commit log record (and in some modes the data) to stable storage so that a crash can't lose the committed work. The OS can "lose" dirty pages; the log cannot lie after fsync.
18. **Q: PRODUCTION: What trade-off is `synchronous_commit=off` making in Postgres?** A: It skips the fsync on COMMIT, trading a small chance of losing the *most recent* commits (which still survive as WAL that's flushed later) for up to ~10x lower commit latency. It's a durability-vs-latency knob, valid for workloads where losing the last few transactions on a power failure is acceptable.

## 14. Follow-Up Questions
1. **Q: If isolation is guaranteed, why do we still need `SELECT FOR UPDATE`?** A: Because READ COMMITTED (the default in most engines) allows lost updates and non-repeatable reads. `FOR UPDATE` locks rows so the read-modify-write cycle is atomic — isolation at a *coarser* level is not enough for read-modify-write sequences.
2. **Q: Can atomicity be achieved without a log?** A: Yes — via shadow paging (make a copy-on-write of pages; atomically flip the page table pointer at commit). It avoids logging but doubles page writes and complicates garbage collection, which is why WAL logging won.
3. **Q: Why is "durability" not just "write to disk"?** A: Because OS caching means "write()" doesn't reach the platter; you need fsync/fsync-able flush, and you need the *log* (not just data) on disk because data pages can be written out of order.
4. **Q: What happens to locks when a transaction aborts?** A: All locks held by the transaction are released immediately, and other transactions waiting on them proceed — this is why abort processing must release locks even while undo runs.

## 15. Coding Example
```sql
-- Bank transfer with proper transaction semantics
BEGIN;

UPDATE accounts
   SET balance = balance - 500
 WHERE account_id = 1001
   AND balance >= 500;          -- guard: enforce "no overdraft" (consistency)

-- check the guard succeeded
SELECT ROW_COUNT();             -- if 0 rows updated, abort instead of partial transfer

UPDATE accounts
   SET balance = balance + 500
 WHERE account_id = 2002;

COMMIT;
```
```python
# Pythonic pattern using the 'psycopg' driver
import psycopg
from psycopg import sql

with psycopg.connect("dbname=bank") as conn:
    with conn.transaction():
        cur = conn.cursor()
        cur.execute(
            "UPDATE accounts SET balance = balance - %s "
            "WHERE account_id = %s AND balance >= %s",
            (500, 1001, 500),
        )
        if cur.rowcount != 1:
            raise RuntimeError("insufficient funds")   # triggers ROLLBACK on exit
        cur.execute(
            "UPDATE accounts SET balance = balance + %s WHERE account_id = %s",
            (500, 2002),
        )
    # leaving the with-block commits automatically; exceptions roll back
```

## 16. Industry Usage
- **PostgreSQL**: MVCC-based isolation, `BEGIN/COMMIT/ROLLBACK`, `synchronous_commit` levels, `DECLARE ... FOR UPDATE`.
- **MySQL/InnoDB**: transactions with undo/redo log, `autocommit` on by default, `SET SESSION TRANSACTION ISOLATION LEVEL`.
- **Oracle**: read-consistent multi-versioning, undo tablespace, `COMMIT WRITE`.
- **SQL Server**: snapshot isolation, `MARS` (multiple active result sets) affecting transaction handling.
- **Distributed**: Spanner (true ACID across data centers via TrueTime + Paxos), CockroachDB (serializable, MVCC), FoundationDB (ACID with strict serializability). Every payment ledger (Stripe, Adyen) and financial system is transactional by regulation — auditability *requires* atomicity/durability.

## 17. References
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 15 (Transactions) & Ch. 16 (Concurrency Control).
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 20.
- PostgreSQL docs: https://www.postgresql.org/docs/current/mvcc.html and https://www.postgresql.org/docs/current/sql-begin.html
- MySQL 8.0 docs, InnoDB transactions: https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-model.html
- ISO/IEC 9075 (SQL standard), transaction & isolation level definitions.

## 18. Cheat Sheet
- Transaction = one logical unit of work; `BEGIN ... COMMIT/ROLLBACK`.
- ACID: Atomicity (all-or-nothing), Consistency (invariants hold), Isolation (serial equivalence), Durability (survives crash).
- Mechanisms: Atomicity ← undo log; Durability ← redo log + fsync; Isolation ← locking/MVCC; Consistency ← constraints.
- Single statement in autocommit = one transaction; multi-statement logic needs explicit BEGIN/COMMIT.
- Commit is only durable after the commit record hits stable storage.
- Rollback undoes all changes via log; MVCC can make aborts nearly free.
- Read-your-own-writes always holds; dirty reads never do (except READ UNCOMMITTED).

## 19. Quiz
1. Which property prevents a concurrent transaction from seeing your half-done work? a) Atomicity b) Consistency c) Isolation d) Durability → **c**
2. Which property is the DBMS *least* able to fully enforce? a) Atomicity b) Consistency c) Isolation d) Durability → **b** (app invariants can't be checked by the engine)
3. After COMMIT returns, what guarantee exists? a) Data is in the buffer pool b) Data is on disk/log such that it survives crash c) Data is visible to all other sessions immediately d) None → **b**
4. ROLLBACK after COMMIT: a) undoes the commit b) is a no-op c) crashes d) auto-commits again → **b**
5. Which is NOT an ACID property? a) Atomicity b) Consistency c) Concurrency d) Durability → **c**
6. A transaction that only reads data: a) never needs ROLLBACK b) can still be aborted by the DBMS c) never holds locks d) is not a transaction → **b** (read-only transactions can still be aborted, e.g. deadlock victim, and still use snapshots)
7. MyISAM vs InnoDB: which supports transactions? a) MyISAM only b) InnoDB only c) both d) neither → **b**
8. What does `SELECT ... FOR UPDATE` do? a) waits for the table to be free b) locks returned rows against concurrent update c) prevents other readers d) none → **b**

## 20. Flashcards
- **Q: What is a transaction?** → **A:** A sequence of DB operations executed as one atomic, isolated unit of work.
- **Q: Name the ACID properties and their mechanisms.** → **A:** Atomicity←undo log; Consistency←constraints; Isolation←locking/MVCC; Durability←redo log+fsync.
- **Q: What's the difference between atomicity and durability?** → **A:** Atomicity = all-or-nothing even on abort; Durability = survives after COMMIT returns.
- **Q: Can the DBMS fully enforce consistency?** → **A:** No — only declared constraints; app invariants need app/trigger logic.
- **Q: When is a commit actually durable?** → **A:** When the commit log record is flushed to stable storage.
- **Q: Why is a single SQL statement not enough for a transfer?** → **A:** The unit of work is multi-statement; autocommit would make the two UPDATEs separate transactions.
- **Q: Does a transaction see its own writes?** → **A:** Yes — read-your-own-writes always holds within a transaction.

## 21. Revision
A transaction groups operations into one atomic unit bracketed by BEGIN/COMMIT/ROLLBACK. ACID = Atomicity (all-or-nothing, via undo log), Consistency (invariants preserved; only partially enforceable by the DB), Isolation (behaves as if serial, via locking/MVCC), Durability (survives crashes, via redo log + fsync). Atomicity is about partial execution; durability is about time-after-commit. Every ACID mechanism will be revisited in Part 06 (recovery/log) and Chapter 02 of this part (concurrency protocols). For interviews: define each property, give a violation example, and name the mechanism — that's the full "ACID" answer.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a transaction?" | 1, 7 |
| "Define ACID with examples." | 1, 2, 8 |
| "Can the DBMS enforce consistency?" | 4, 9 |
| "Atomicity vs durability?" | 2, 13 |
| "Why does the DB need a log for atomicity/durability?" | 9, 14 |
| "What does `SELECT FOR UPDATE` do?" | 13, 19 |
| "Transactions in MyISAM vs InnoDB?" | 13 |
| "Why do NoSQL systems drop ACID?" | 13, 16 |
| "When is a commit durable?" | 9, 18 |
