# Isolation Levels in Depth

> **TL;DR**: Isolation levels are the pragmatic dial between "perfect but slow" (SERIALIZABLE) and "fast but risky" (READ UNCOMMITTED) — each level defines exactly which concurrency anomalies (dirty read, non-repeatable read, phantom) the database will and won't prevent.

## 1. Why Does This Exist?
SERIALIZABLE isolation is the "correct" default — but it's expensive: it forces locks that serialize transactions and blocks phantoms via range locks, killing concurrency. Most applications don't need full serializability; they need *some* protection at a cost they can afford. Isolation levels exist to give applications a *documented, standardized* set of trade-off points: "I accept anomaly X in exchange for throughput Y." The SQL standard (and the 1995 "Critique of ANSI SQL Isolation Levels" paper) codified four levels and three anomalies so that a DBMS's behavior is predictable and portable across vendors.

## 2. How Does It Work?
The four ANSI levels, weakest→strongest:
1. **READ UNCOMMITTED** — no isolation at all for reads: a transaction can see other transactions' uncommitted writes (dirty reads). Engines typically *do not* permit uncommitted writes to be read by others safely, so it's often implemented "as read committed" in practice (Postgres ignores it).
2. **READ COMMITTED** — each *statement* sees a snapshot of data committed *before the statement started*. No dirty reads, but two statements in one transaction can see different snapshots → **non-repeatable reads** and phantoms possible.
3. **REPEATABLE READ** — each *transaction* sees a single snapshot taken at its first read. No dirty/non-repeatable reads; **phantoms** possible (rows can appear/disappear in range queries) unless range/next-key locks are used.
4. **SERIALIZABLE** — equivalent to serial execution: no dirty reads, no non-repeatable reads, no phantoms, no write skew. Implemented via strict 2PL + range locks (MySQL) or SSI (Postgres).

The anomalies: **dirty read** (read an uncommitted write later rolled back), **non-repeatable read** (re-read a row and get a different committed value), **phantom** (a range query returns different rows across executions because another transaction inserted/deleted a matching row).

## 3. When Is It Used?
- **READ COMMITTED** — the overwhelming production default (Postgres default, Oracle default, SQL Server default). Good for most OLTP: each query sees consistent committed data.
- **REPEATABLE READ** — MySQL InnoDB default; used when a *transaction* must see a stable view (reporting, multi-statement reads that must agree). Note Postgres maps it to snapshot isolation (no phantoms in the snapshot *reads*, but write-skew possible).
- **SERIALIZABLE** — money, inventory, seats, idempotency-critical logic, when the cost of a rare anomaly exceeds the cost of slower writes.
- **READ UNCOMMITTED** — almost never; used for dashboards/analytics where a slightly stale/garbage value is tolerable and read latency dominates.

## 4. Why Wasn't Another Approach Chosen?
- *Always serializable:* correct but pays for it in lock contention and reduced concurrency — unacceptable as the default for read-heavy OLTP.
- *Always read uncommitted:* fastest but corrupts business logic; nobody wants to read half-applied transfers.
- *A continuum of anomaly-latency points rather than discrete levels:* conceptually cleaner, but the SQL standard chose discrete levels for *portability* and *testability*; vendors add knobs *on top* (e.g., `synchronous_commit`, `innodb_flush_log_at_trx_commit`).
- *Relying only on MVCC snapshots:* snapshot isolation is great but is *not* serializable (write skew) — so DBMSes add extra machinery (next-key locks, SSI) where the standard requires serializable behavior, showing that "just use MVCC" wasn't enough.
- The Berenson et al. critique showed ANSI's original definitions were even ambiguous (they described *implementation* artifacts like locks, not observable anomalies) — subsequent systems define levels by *anomalies prevented*, the model used here.

## 5. Intuition
Picture a **room of people reading and editing a shared whiteboard**. READ UNCOMMITTED: you glance at the board mid-edit, seeing scribbles that may be erased. READ COMMITTED: you see a consistent snapshot *each time you look* — but someone may erase and rewrite between looks, so your notes go stale. REPEATABLE READ: you take a photo of the whole board when you start; you always see that photo — but new rows can be added that your photo doesn't include (phantom). SERIALIZABLE: only one person works on the board at a time — nobody ever sees anyone else's work-in-progress or partial timeline. Each step up costs more waiting, prevents more surprises.

## 6. Real-World Analogy
**Ordering food from a menu while the kitchen inventory changes**: Dirty read = the waiter quotes you a dish that another table just ordered the last of (and that order gets cancelled). Non-repeatable read = the waiter quotes a price, you call back, price changed. Phantom = the "vegetarian options" page lists 3 dishes now and 4 the next time you look, because the kitchen added a new dish mid-conversation. SERIALIZABLE = the kitchen freezes the entire menu for your whole call — slow, but what you saw is what you got.

## 7. Formal Definition
An isolation level is a specification of which anomalies a DBMS may exhibit while executing transactions at that level. Per the ANSI/ISO SQL standard (as refined by Berenson et al.):
- **READ UNCOMMITTED**: transactions may read data written by uncommitted transactions (dirty read) — but the standard *requires* writes to be no-worse than READ COMMITTED; anomalies: dirty, non-repeatable, phantom all possible.
- **READ COMMITTED**: dirty reads prevented (a read sees only committed data at statement start); non-repeatable reads and phantoms possible.
- **REPEATABLE READ**: dirty and non-repeatable reads prevented; phantoms possible (a transaction's own writes are always visible).
- **SERIALIZABLE**: no dirty, no non-repeatable, no phantoms; the execution is serializable (equivalent to serial) — includes write-skew prevention.

## 8. Example
Scenario — row `A=100`:
- **T1**: `UPDATE A SET A=A-100 WHERE id=1;` (A→0, uncommitted)
- **T2** at READ UNCOMMITTED: `SELECT A` → **0** (dirty). T1 rolls back → T2 saw a value that never existed.
- **T2** at READ COMMITTED: `SELECT A` → **100** (blocked from the uncommitted 0). But later `SELECT A` in the same T2 after T1 commits sees 0 → non-repeatable read across statements.
- **T2** at REPEATABLE READ: `SELECT A` twice → **100, 100** even after T1 commits (snapshot). If T3 inserts a new row matching T2's `WHERE A>50` filter, T2's second range scan sees the new row → **phantom**.
- **T2** at SERIALIZABLE: same guarantees as REPEATABLE READ plus phantoms prevented (range locks / SSI). Also prevents T1 and T2 both reading then writing disjoint data inconsistently (write skew).

## 9. Internal Working
1. The application sets `SET TRANSACTION ISOLATION LEVEL X` (session- or transaction-scoped).
2. The DBMS instantiates the mechanism:
   - **READ COMMITTED (MVCC engines)**: at each statement start, create a snapshot of committed versions (Postgres `xmin`/`xmax` visibility rules); row versions newer than the snapshot are invisible. This makes it *statement*-consistent.
   - **REPEATABLE READ (MVCC)**: take the snapshot once, at the transaction's first read (Postgres); MySQL InnoDB instead combines the snapshot with **next-key locks** (record + gap locks) on reads under certain conditions.
   - **SERIALIZABLE (Postgres)**: SSI — same snapshot as REPEATABLE READ, plus track read/write dependencies to detect "dangerous structures" and abort one transaction. **SERIALIZABLE (MySQL)**: convert plain `SELECT`s to `SELECT ... LOCK IN SHARE MODE` and `SELECT ... FOR UPDATE`-style locking plus next-key locks, giving serializability by blocking.
   - **READ UNCOMMITTED**: engines either skip the snapshot entirely (see in-flight buffers) or *ignore it* and behave as READ COMMITTED (Postgres: "READ UNCOMMITTED is treated like READ COMMITTED").
3. Each anomaly class maps to a mechanism gap: dirty → snapshot too old/absent; non-repeatable → per-statement snapshot; phantom → no range/next-key lock.

## 10. Time Complexity
- READ COMMITTED: snapshot cost O(1) per statement (plus version-chasing on read if not visible directly — worst case O(version chain length)).
- REPEATABLE READ: same per-read cost, but snapshot taken once; lock costs only where next-key locking applies.
- SERIALIZABLE: adds either lock wait time (2PL — blocking) or SSI bookkeeping (tracking r/w sets, checking for dangerous structures) — worst-case extra O(active transactions) per read/write, plus aborts.
- Concurrency (throughput) roughly falls as isolation rises because blocking/waiting increases; the exact trade-off depends on the workload (read:write ratio, contention on hot rows).

## 11. Advantages
- **Predictable, standard semantics**: apps can state their needs in portable SQL.
- **Performance control**: most apps run at READ COMMITTED/REPEATABLE READ and get high concurrency with bounded anomalies.
- **Fine-grained tuning**: the level can vary per session (reports at SERIALIZABLE, hot-path writes at READ COMMITTED).
- **Anomaly documentation**: knowing *which* anomaly each level allows lets developers design compensating logic or add locks only where needed.

## 12. Disadvantages
- **Weak levels allow real bugs**: lost updates, non-repeatable reads, phantoms, write skew silently corrupt results for apps that assume stronger isolation.
- **Vendor divergence**: "REPEATABLE READ" in MySQL ≠ "REPEATABLE READ" in Postgres ≠ Oracle's (Postgres = snapshot; MySQL = snapshot + next-key; Oracle's REPEATABLE READ is not even exposed the same way; Oracle's SERIALIZABLE is snapshot-based with write-skew risk!). Portability is a trap.
- **Over-locking**: developers who don't understand levels often "fix" anomalies by overusing SERIALIZABLE or `SELECT FOR UPDATE`, destroying concurrency.
- **Defaults hide semantics**: an app tested only at default isolation may break silently in another engine whose default differs.

## 13. Interview Questions
1. **Q: Name the four isolation levels from weakest to strongest.** A: READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE — plus the anomalies each prevents (dirty read, non-repeatable read, phantom).
2. **Q: What is a dirty read?** A: Reading a row modified by a transaction that hasn't committed (and may roll back) — you've seen data that may never have existed.
3. **Q: What is a non-repeatable read?** A: Within one transaction, re-reading the same row returns a *different* (newly committed) value — the row "changed under you" between statements.
4. **Q: What is a phantom read?** A: Re-running a range query within a transaction returns *different sets of rows* because another transaction inserted (or deleted) a matching row in between. Row locks can't prevent it — you need range/gap locks or a snapshot.
5. **Q: Which anomaly does READ COMMITTED allow that REPEATABLE READ doesn't?** A: Non-repeatable reads (and phantoms) — READ COMMITTED sees a new snapshot per statement; REPEATABLE READ per transaction.
6. **Q: TRICKY: Is REPEATABLE READ in MySQL the same as in Postgres?** A: No. Postgres REPEATABLE READ = pure snapshot isolation (phantoms can't appear in *reads*, but write skew can happen, and nothing blocks insert conflicts). MySQL REPEATABLE READ = snapshot + next-key (gap) locks that also *prevent phantoms by locking ranges*, and even blocks some write conflicts. The names match the standard's letter, not each other's behavior.
7. **Q: What is a lost update and at which levels can it occur?** A: T1 reads A=100, T2 reads A=100, T1 writes A=90, T2 writes A=90 — final 90 instead of 80. Possible at READ UNCOMMITTED and READ COMMITTED (both can read then write over each other); prevented by `SELECT FOR UPDATE` or REPEATABLE READ+lock or SERIALIZABLE (via serialization).
8. **Q: How does Postgres handle `SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED`?** A: It accepts it but treats it as READ COMMITTED — Postgres refuses to let you read dirty data; the level exists for standard compatibility only.
9. **Q: PRODUCTION: Which level should an e-commerce cart's "add item" use?** A: The *write path* needs SERIALIZABLE or explicit `SELECT ... FOR UPDATE` on the cart row to avoid lost updates; the *read path* (displaying the cart) can be READ COMMITTED. Mixing levels per operation is the normal production pattern.
10. **Q: What is a write skew and why does it break REPEATABLE READ?** A: Two transactions both read overlapping data, then each writes a *different* portion — neither violates a constraint alone, but together they do. Snapshot isolation allows it (e.g., both doctors decide a patient can leave, each unaware of the other). Only SERIALIZABLE prevents it. (Fekete's famous example.)
11. **Q: Does READ COMMITTED guarantee no dirty writes?** A: Yes — dirty *writes* (overwriting another transaction's uncommitted change) are prevented at every level by row-write locking, even READ UNCOMMITTED. The level concerns what you *read*, and the standard requires writes be atomic.
12. **Q: TRICKY: Why does the ANSI standard define levels by *prevented anomalies* rather than by locks?** A: Because the original standard described *implementation* (locking) not *behavior*; Berenson et al. (1995) showed the definitions were incomplete (e.g., snapshot isolation and write skew fall outside the original three anomalies). Defining by observable anomalies makes the contract precise and testable across engines.
13. **Q: What is the "P" in P0/P1/P2/P3 anomalies?** A: Berenson et al.'s notation: P0 = dirty write, P1 = dirty read, P2 = fuzzy/non-repeatable read, P3 = phantom. (Some add P4 = lost update.) Knowing P0-P3 lets you precisely classify "which anomaly does this schedule exhibit?"
14. **Q: PRODUCTION: When do you raise a transaction from READ COMMITTED to SERIALIZABLE in production?** A: For money movement (transfer, payout idempotency), inventory decrement with a "can't oversell" invariant, seat/room booking, and any operation where a race produces a *financial or integrity* bug worse than the performance cost. Teams typically start at default and *escalate only the few transactions that need it*.
15. **Q: What is the difference between isolation level and locking?** A: Isolation level is the *contract* (which anomalies are prevented); locking/MVCC is the *mechanism*. One level can be implemented by different mechanisms (MySQL REPEATABLE READ via next-key locks vs Postgres via snapshots), and the same mechanism (MVCC) can serve multiple levels (read committed = per-statement snapshots; repeatable read = one snapshot).
16. **Q: Does lowering isolation ever improve write performance, not just read concurrency?** A: Yes — less locking means fewer lock waits and less deadlock risk, and MVCC engines avoid version churn. READ COMMITTED has lower overhead per transaction than SERIALIZABLE, so *throughput* rises even for writes when contention is low.

## 14. Follow-Up Questions
1. **Q: What is "snapshot isolation" and how does it relate to the standard levels?** A: A mechanism (read from a versioned snapshot, write-conflict detection) that *typically* implements REPEATABLE READ (Postgres) but is also the basis of Oracle's SERIALIZABLE. It guarantees no dirty/non-repeatable reads/phantoms-in-reads but permits write skew — it is *not* serializable without SSI.
2. **Q: What is SSI (Serializable Snapshot Isolation)?** A: Snapshot isolation plus runtime detection of "dangerous structures" (read-write dependencies between transactions); when detected, one transaction is aborted, restoring serializability (Postgres `REPEATABLE READ`→`SERIALIZABLE` upgrade).
3. **Q: How do next-key locks prevent phantoms in MySQL?** A: They lock the record *and the gap before it*, so a concurrent `INSERT` into the gap blocks until the lock holder commits — range stability across statements.
4. **Q: What is "read your own writes" and which level guarantees it?** A: A transaction always sees its own writes at every level (even READ UNCOMMITTED) — the guarantee is about *other* transactions, never self.

## 15. Coding Example
```sql
-- Set a level (MySQL)
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
SELECT * FROM accounts WHERE id = 1;      -- snapshot taken here (first read)
-- other sessions commit changes to id=1...
SELECT * FROM accounts WHERE id = 1;      -- still sees snapshot → repeatable read
COMMIT;
```
```python
# Anomaly walkthrough: non-repeatable read at READ COMMITTED in Postgres
import psycopg, threading

def reader(dsn):
    with psycopg.connect(dsn) as c:
        c.execute("SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL READ COMMITTED")
        with c.transaction():
            print("T2 first read:", c.execute("SELECT balance FROM accounts WHERE id=1").fetchone())
            time.sleep(2)                       # writer commits in the gap
            print("T2 second read:", c.execute("SELECT balance FROM accounts WHERE id=1").fetchone())

def writer(dsn):
    time.sleep(1)
    with psycopg.connect(dsn) as c:
        with c.transaction():
            c.execute("UPDATE accounts SET balance = balance - 100 WHERE id=1")
# Output: "T2 first read: (1000,)  T2 second read: (900,)"  → non-repeatable read
```
```sql
-- Preventing the lost update at any level
START TRANSACTION;
SELECT balance FROM accounts WHERE id=1 FOR UPDATE;   -- pessimistic lock
-- compute new_balance in app
UPDATE accounts SET balance = new_balance WHERE id=1;
COMMIT;
```

## 16. Industry Usage
- **PostgreSQL**: default READ COMMITTED; REPEATABLE READ = snapshot isolation; SERIALIZABLE = SSI. Docs explicitly state the anomaly each level permits — the reference for "which level does what."
- **MySQL InnoDB**: default REPEATABLE READ with next-key locks (stronger phantom prevention than the standard requires).
- **Oracle**: default READ COMMITTED with undo-based read consistency; "SERIALIZABLE" is snapshot-based — so Oracle's SERIALIZABLE allows write skew. Different vendors = different semantics.
- **SQL Server**: READ COMMITTED default; supports SNAPSHOT isolation and `READ_COMMITTED_SNAPSHOT ON`; SERIALIZABLE via locks.
- **Spanner**: provides *external consistency* (linearizable serializable) — stronger than any ANSI level, via TrueTime + 2PC. CockroachDB: serializable by default with non-blocking reads.

## 17. References
- ANSI/ISO SQL standard, isolation level definitions (ISO/IEC 9075-2).
- Berenson, Bernstein, Gray, Melton, O'Neil, O'Neil, "A Critique of ANSI SQL Isolation Levels", SIGMOD 1995 — the anomalies P0–P3 and the incompleteness argument.
- PostgreSQL docs, "Transaction Isolation": https://www.postgresql.org/docs/current/transaction-iso.html
- MySQL 8.0 docs, InnoDB isolation levels: https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html
- Fekete et al., "Making Snapshot Isolation Serializable" (2005) — write-skew examples.
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 15.6.

## 18. Cheat Sheet
- 4 levels: RU → RC → RR → SERIALIZABLE (weakest→strongest).
- Anomalies: dirty read (P1), non-repeatable (P2), phantom (P3); dirty write (P0) is prevented everywhere.
- READ COMMITTED: no dirty reads; per-statement snapshot. (Postgres/Oracle/SQL Server default.)
- REPEATABLE READ: no dirty/non-repeatable; one snapshot per transaction (Postgres = snapshot; MySQL = snapshot + next-key locks).
- SERIALIZABLE: serial equivalence; Postgres = SSI, MySQL = 2PL + gap locks.
- Lost updates/write skew are prevented only at SERIALIZABLE (or by explicit locks at weaker levels).
- Vendor semantics differ despite identical names — always check the docs.
- Level is per-session; escalate only critical transactions.

## 19. Quiz
1. Which anomaly does READ COMMITTED allow? a) dirty read b) non-repeatable read c) none d) all → **b**
2. Which anomaly does REPEATABLE READ allow by the standard? a) phantom b) dirty read c) non-repeatable d) none → **a**
3. Postgres default isolation level: a) READ UNCOMMITTED b) READ COMMITTED c) REPEATABLE READ d) SERIALIZABLE → **b**
4. MySQL InnoDB default: a) READ COMMITTED b) REPEATABLE READ c) SERIALIZABLE d) READ UNCOMMITTED → **b**
5. Reading a value that was later rolled back is: a) non-repeatable read b) phantom c) dirty read d) lost update → **c**
6. Write skew is prevented only at: a) READ COMMITTED b) REPEATABLE READ c) SERIALIZABLE d) READ UNCOMMITTED → **c**
7. What mechanism prevents phantoms in MySQL REPEATABLE READ? a) row locks b) next-key (gap) locks c) timestamps d) serialization order → **b**
8. Which is the correct weakest→strongest order? a) RR, RU, RC, S b) RU, RC, RR, S c) RU, RR, RC, S d) RC, RU, S, RR → **b**

## 20. Flashcards
- **Q: Four isolation levels weakest→strongest.** → **A:** READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE.
- **Q: Dirty read?** → **A:** Reading an uncommitted write that may roll back.
- **Q: Non-repeatable read?** → **A:** Same row, different value across statements in one transaction.
- **Q: Phantom read?** → **A:** A range query returns different rows because another txn inserted/deleted a match.
- **Q: Which levels prevent dirty reads?** → **A:** READ COMMITTED and above.
- **Q: Which levels prevent non-repeatable reads?** → **A:** REPEATABLE READ and above.
- **Q: Which levels prevent phantoms?** → **A:** Only SERIALIZABLE by the standard (MySQL RR also does via gap locks).
- **Q: Postgres default vs MySQL default?** → **A:** Postgres READ COMMITTED; MySQL InnoDB REPEATABLE READ.

## 21. Revision
Isolation levels trade safety for concurrency: RU (dirty reads allowed — Postgres ignores it), RC (per-statement snapshot; no dirty reads; non-repeatable + phantom possible; default in Postgres/Oracle/SQL Server), RR (per-transaction snapshot; no non-repeatable; phantoms per standard, though MySQL's next-key locks prevent them too; MySQL default), SERIALIZABLE (serial equivalence; Postgres via SSI, MySQL via 2PL+gap locks; also stops write skew/lost updates). Remember vendor divergence: identical names ≠ identical behavior. Anomaly mnemonic: P0 dirty write (never allowed), P1 dirty read, P2 non-repeatable, P3 phantom.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Explain the four isolation levels." | 2, 7 |
| "What is a dirty/non-repeatable/phantom read?" | 2, 8, 13 |
| "Which anomaly does each level allow?" | 2, 13 |
| "Is REPEATABLE READ the same in MySQL and Postgres?" | 6, 13 |
| "What is a lost update / write skew?" | 13, 14 |
| "What are the defaults in Postgres/MySQL?" | 13, 16, 21 |
| "How does SSI work?" | 13, 14, 16 |
| "What does `SELECT ... FOR UPDATE` change?" | 13, 15 |
