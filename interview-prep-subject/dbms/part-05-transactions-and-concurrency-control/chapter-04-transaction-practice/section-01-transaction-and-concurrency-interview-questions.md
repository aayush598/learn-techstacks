# Transaction and Concurrency Interview Questions

> **TL;DR**: The complete Part 05 question bank — 28 questions spanning easy→hard, with crisp answers designed to be said out loud, plus the follow-ups interviewers actually ask next.

## 1. Why Does This Exist?
Every DBMS interview devotes 30-60% of its time to transactions and concurrency, and the questions repeat with remarkable consistency — ACID, isolation levels, 2PL, MVCC, deadlock. This section exists to turn your Part 05 knowledge (Chapters 01-03) into *answerable* form: the exact phrasing, the exact examples, and the exact follow-ups, so you can recognize the question, say the answer confidently, and survive the "why?" that follows. It also exists because the *scenario* questions (anomaly detection, system design, debugging) are where candidates with textbook knowledge fail — so those get extra depth.

## 2. How Does It Work?
Each question is a real interview question with a complete answer you can speak in 30-90 seconds. The questions are grouped by difficulty: definitional (warm-up), mechanism (medium), and scenario/debugging (hard). For every answer, the underlying *reason* is included so you can derive it live. Use it as follows: cover the answer, try to answer aloud, compare, and repeat until every answer is fluent. Then do the follow-ups at the bottom as a second pass.

## 3. When Is It Used?
- The week before an interview: read aloud, one section per day.
- In mock interviews: have a friend ask the questions in random order.
- During system-design practice: reuse the "which isolation level / optimistic or pessimistic / how does MVCC help here?" reasoning for database-heavy designs (booking, inventory, payments, chat).

## 4. Why Wasn't Another Approach Chosen?
- *Fifty-page answer keys*: too much to memorize; interview answers must be *spoken*, not *written*. Each answer here is a tight 3-5 sentence core you can expand.
- *Only trivia questions*: FAANG interviews are scenario-heavy; trivia-only prep fails on "detect the anomaly in this schedule." Hence the scenario block.
- *Only scenario questions*: you still need the crisp definitional answers for warm-ups. Balance is the point.
- *Abstract theory dump*: every answer is tied to a real engine (Postgres/MySQL) or a production pattern, because interviewers reward "how does this work in real life."

## 5. Intuition
Think of this section as **flashcards with the answers already in interview voice**. The goal isn't to know the answer — it's to know the answer *the way you'd say it in a room with an interviewer staring at you*: first the definition, then the mechanism, then (for hard questions) a concrete example and a production caveat. That three-beat structure is what "crisp full answer" means in practice.

## 6. Real-World Analogy
A **stand-up comedian's set list**: you don't improvise the jokes on stage; you rehearse the beats. But the best sets leave room for audience interaction (follow-ups). This section is your rehearsed set list for the transaction/concurrency part of the interview — rehearse it cold, and you'll have headroom to handle the curveballs.

## 7. Formal Definition
An interview answer to a transaction question should contain: (1) a one-line formal definition, (2) the mechanism (how it's implemented), (3) a concrete example, (4) the trade-offs/caveats. This section provides those four parts for each of the 28 canonical questions in the domain of transactions, schedules, serializability, isolation, and concurrency control.

## 8. Example
Question: "What is a deadlock?" A model answer: "A deadlock is a state where two or more transactions each hold a lock the others need and are waiting for locks the others hold — a cycle in the wait-for graph. It's the classic Coffman conditions: mutual exclusion, hold-and-wait, no preemption, circular wait. The DBMS handles it by detection (Postgres waits `deadlock_timeout`=1s then scans the graph; InnoDB detects at block time) and by aborting a victim, which the app must retry. You can reduce deadlocks by acquiring locks in a consistent global order and keeping transactions short." That's the exact structure this section instills.

## 9. Internal Working
1. Group 1 — definitions (Q1-Q6): the vocabulary you must own cold.
2. Group 2 — isolation and anomalies (Q7-Q13): level → anomaly mapping, defaults, write skew.
3. Group 3 — protocols (Q14-Q21): 2PL, timestamps, MVCC, validation, deadlock.
4. Group 4 — scenarios & debugging (Q22-Q28): production incidents and system-design answers.
5. Follow-ups: the "and why?" probes interviewers attach to each.

## 10. Time Complexity
- Time to review all 28: ~45-60 minutes aloud on first pass; ~15 minutes on review.
- Time per answer: 30-90 seconds spoken. Follow-up answers: 10-30 seconds.
- Interview coverage: ~40-60% of a typical DBMS round.

## 11. Advantages
- Complete coverage of the part's interviewable surface.
- Answers are spoken-sized, not essay-sized.
- Scenario/debugging questions go deeper than typical prep.
- Each answer stands alone — you can study in any order.

## 12. Disadvantages
- Answers are compressed; a genuinely unusual interviewer question may need deeper theory (go to the section files).
- Memorization risk — must practice *deriving*, not just recalling.

## 13. Interview Questions

### Group 1 — Definitions (easy)
1. **Q: What is a transaction?** A: A sequence of database operations that forms a single logical unit of work, executed atomically — either all its effects are applied or none — and isolated from other concurrent transactions. In SQL, bracketed by `BEGIN ... COMMIT/ROLLBACK`. (Section: transaction concept.)
2. **Q: Define ACID with one violation example each.** A: Atomicity — crash mid-transfer leaves money in limbo; undone via the undo log. Consistency — an update breaks "balance ≥ 0"; enforced by constraints + app logic. Isolation — a concurrent read sees half-applied work; prevented by locking/MVCC. Durability — committed data lost after power cut; prevented by the redo log + fsync.
3. **Q: Can the DBMS fully enforce consistency?** A: No. It enforces declared constraints (PK, FK, CHECK), but application invariants (sum of balances constant) need triggers or app code. ACID guarantees that if you start consistent and obey invariants, the DB won't corrupt them.
4. **Q: Difference between atomicity and durability?** A: Atomicity = all-or-nothing across *partial execution* (even on abort); Durability = persists *after* COMMIT returns. A system can be atomic but not durable (in-memory DB), or durable but not atomic (no logging).
5. **Q: What are the transaction states?** A: Active → Partially committed (last op done, commit not durable) → Committed (commit record on stable storage); or Active → Failed → Aborted. Recovery redos committed transactions and undoes the rest.
6. **Q: What is a schedule, and when is it serializable?** A: A schedule is an interleaving of transactions' operations preserving intra-transaction order. It's serializable if equivalent (conflict or view) to some serial schedule. Conflict serializable ⇔ acyclic precedence graph.

### Group 2 — Isolation and anomalies (easy→medium)
7. **Q: Name the four isolation levels and the anomaly each allows.** A: READ UNCOMMITTED (dirty reads), READ COMMITTED (non-repeatable + phantom), REPEATABLE READ (phantom), SERIALIZABLE (none). Dirty = reading uncommitted data; non-repeatable = same row different value across statements; phantom = range query returns different rows.
8. **Q: What is the default isolation in Postgres and MySQL?** A: Postgres READ COMMITTED (per-statement snapshot); MySQL InnoDB REPEATABLE READ (snapshot + next-key locks).
9. **Q: Is REPEATABLE READ the same in both?** A: No. Postgres = pure snapshot isolation (write skew possible, no phantom-preventing locks on reads). MySQL = snapshot + next-key locks, so concurrent inserts into a scanned range block — phantom-safe on writes. The names match the standard, not each other.
10. **Q: What is a lost update and how do you prevent it?** A: Two transactions read the same value, both modify, second overwrites the first. Prevented by `SELECT ... FOR UPDATE` (pessimistic) or by version-column optimistic locking, or by SERIALIZABLE.
11. **Q: What is write skew?** A: Two transactions read overlapping data but write *disjoint* rows; each alone preserves the invariant, together they violate it (two doctors both going off-duty after both saw "1 on duty"). Snapshot isolation allows it; only SERIALIZABLE (SSI) or explicit locks prevent it.
12. **Q: TRICKY: Can dirty writes happen at READ UNCOMMITTED?** A: No — dirty *writes* (overwriting another transaction's uncommitted write) are prevented at every level by write-locking. Isolation levels govern *reads*; the standard requires writes to be atomic.
13. **Q: What does `SELECT ... FOR UPDATE` do and when do you use it?** A: It acquires exclusive locks on the returned rows, held until commit — a pessimistic lock turning a plain read into a locked read-modify-write. Use it for counters, inventory decrements, booking, anywhere a read-then-write race must be closed.

### Group 3 — Protocols (medium→hard)
14. **Q: Explain two-phase locking.** A: Acquire all locks in a growing phase, release in a shrinking phase; never acquire after the first release. It guarantees conflict serializability. Strict 2PL (release at commit) additionally gives recoverability and is what engines implement. It does NOT prevent deadlock.
15. **Q: Why does 2PL give serializability?** A: Conflicting operations are ordered by lock acquisition; if the conflict graph had a cycle, some transaction would need to acquire a lock after releasing one — violating the two-phase rule. So the graph is acyclic.
16. **Q: Strict vs rigorous 2PL?** A: Strict holds X-locks until commit/abort (S-locks may be released early); rigorous holds *all* locks until commit. Strict is the production norm; rigorous appears in distributed settings.
17. **Q: What is the Thomas Write Rule?** A: Under timestamp ordering, if a write arrives with TS(T) < W-ts(item), the older write is *ignored* instead of aborting the transaction — the write is obsolete. It reduces aborts; schedules stay view-serializable.
18. **Q: What is MVCC and why is it used?** A: Multiple versions of each row, tagged with commit info; readers read a consistent snapshot and never block; write-write conflicts still lock/abort. Used because read-heavy OLTP shouldn't serialize readers behind writers.
19. **Q: What is snapshot isolation and its limitation?** A: Each transaction sees a snapshot at first read; own writes visible; write-write → abort second. Prevents dirty/non-repeatable/phantom-in-reads but allows write skew — NOT serializable. Postgres SERIALIZABLE adds SSI to fix it.
20. **Q: How does Postgres vs InnoDB implement MVCC?** A: Postgres keeps old tuple versions in the table (`xmin`/`xmax`, hint bits), snapshot = in-flight XID list, VACUUM reclaims → bloat risk. InnoDB keeps the current value + `DB_TRX_ID`/`DB_ROLL_PTR` in the clustered index, reconstructs old versions from the undo log, purge thread cleans.
21. **Q: How is deadlock handled?** A: Detection (wait-for graph cycle → abort a victim; InnoDB at block time, Postgres after `deadlock_timeout`), prevention (wait-die/wound-wait by timestamp), or timeouts. The app must retry the victim (SQLSTATE 40001).

### Group 4 — Scenarios & debugging (hard)
22. **Q: PR: Why is my Postgres table bloating after an update-heavy batch?** A: MVCC keeps old tuple versions in the table; VACUUM can't remove them while any snapshot is older than them (long transactions hold the horizon). Fix: monitor `n_dead_tup`, tune autovacuum, avoid long transactions, `VACUUM FULL` as a last resort.
23. **Q: PR: A query deployed in production started deadlocking. What do you investigate?** A: The new query's lock acquisition order vs existing queries (gap/next-key locks, FK locks), whether it scans instead of seeks (locks many rows), transaction length, and index usage. Fixes: consistent access order, indexes, shorter transactions, retries.
24. **Q: Design: inventory decrement for a flash sale (high contention).** A: Use atomic conditional update: `UPDATE inventory SET qty=qty-1 WHERE sku=? AND qty>=1`, check `ROW_COUNT()`, roll back if 0. Keep the transaction tiny; consider batching/sharding the stock across rows to reduce contention. Do NOT use optimistic read-then-write.
25. **Q: Design: which isolation for a payment ledger?** A: SERIALIZABLE (or READ COMMITTED + explicit `FOR UPDATE` on account rows) — money movement must prevent lost updates and write skew; auditability requires atomicity/durability. Report reads can use READ COMMITTED/snapshots.
26. **Q: TRICKY: Detect the anomaly in: T1 reads A=100; T2 updates A=50 (uncommitted); T1 reads A=50; T2 aborts.** A: Dirty read — T1 read T2's uncommitted (and later rolled-back) write. Allowed only at READ UNCOMMITTED; prevented by READ COMMITTED's per-statement snapshot.
27. **Q: TRICKY: Can MVCC databases still deadlock?** A: Yes — writers deadlock on write-write conflicts, lock upgrades (S→X), gap locks (InnoDB), and FK checks. MVCC eliminates *reader* deadlocks only; write paths are still 2PL-style.
28. **Q: PRODUCTION: When would you use `synchronous_commit=off` or `innodb_flush_log_at_trx_commit=0`?** A: To cut commit latency by skipping the log fsync per commit, accepting that the *most recent* commits may be lost on a power failure. Valid when the app tolerates losing the last few transactions (metrics, caches, logs) — never for financial data.

## 14. Follow-Up Questions
1. **Q (on 2PL): Does 2PL prevent deadlock?** A: No — it prevents non-serializable schedules. Deadlock is a separate problem handled by detection/prevention (see Q21).
2. **Q (on MVCC): Why isn't snapshot isolation serializable?** A: Because it allows write skew — two transactions can both commit having written *different* rows based on overlapping reads; no serial execution produces that outcome.
3. **Q (on isolation): What's the difference between a phantom and a non-repeatable read?** A: Non-repeatable = an *existing* row changes value; phantom = a *new* row appears (or disappears) in a range query — different rows, not different values.
4. **Q (on timestamps): Why restart with a newer timestamp?** A: An older timestamp would fail the same conflict forever; a newer one makes the transaction the winner of future disputes, guaranteeing progress.
5. **Q (on OCC): When does optimistic beat pessimistic?** A: When the conflict rate is low and retries are cheap — the common case is fast and you rarely pay the abort cost. Under high contention, pessimistic's blocking beats optimistic's abort-and-redo.
6. **Q (on recovery): What happens to uncommitted transactions after a crash?** A: They're undone (no commit record in the log); committed ones are redone if their pages didn't reach disk. That's Part 06's job.

## 15. Coding Example
```sql
-- The "inventory decrement" answer, done right (atomic + pessimistic on write)
BEGIN;
UPDATE inventory SET qty = qty - 1
 WHERE sku = 'A100' AND qty >= 1;        -- atomic, guarded
SELECT ROW_COUNT();                       -- 1 = sold; 0 = out of stock
COMMIT;
```
```sql
-- Detecting the dirty read (READ UNCOMMITTED, MySQL)
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
BEGIN;
-- (concurrently) T2: UPDATE accounts SET balance=50 WHERE id=1;  -- uncommitted
SELECT balance FROM accounts WHERE id=1;   -- returns 50 → DIRTY READ
ROLLBACK;
```
```python
# Retry wrapper used for all concurrency errors
import time, psycopg
def run_with_retry(fn, attempts=4):
    for i in range(attempts):
        try:
            with psycopg.connect("dbname=x") as conn:
                with conn.transaction():
                    return fn(conn)
        except psycopg.errors.SerializationFailure:
            time.sleep(0.05 * 2 ** i)      # backoff
    raise RuntimeError("concurrency retry budget exhausted")
```

## 16. Industry Usage
These questions mirror real screening: Google and Meta ask anomaly-detection and isolation-level questions verbatim; Amazon's SDE rounds ask "design an inventory system" (Q24); Stripe/Adyen ask ledger durability (Q25); every Postgres-based company has a "bloat or deadlock" war story (Q22/Q23). Practicing them aloud is practicing the actual interview.

## 17. References
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 15-16.
- PostgreSQL docs, "Transaction Isolation": https://www.postgresql.org/docs/current/transaction-iso.html
- MySQL 8.0 docs, InnoDB isolation & locking: https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html
- Berenson et al., "A Critique of ANSI SQL Isolation Levels" (1995).
- MySQL error reference 1213/1205; SQLSTATE 40001.

## 18. Cheat Sheet
- Answer structure: define → mechanism → example → caveat.
- ACID mechanisms: atomicity←undo, isolation←locking/MVCC, durability←redo+fsync, consistency←constraints.
- Levels → anomalies: RU=dirty, RC=non-repeatable, RR=phantom, S=none.
- 2PL: grow/release; strict=release at commit; serializable guaranteed, deadlock not.
- MVCC: versions; snapshot; write-skew = not serializable; SSI fixes.
- Deadlock: WFG cycle → victim → retry 40001.
- Postgres RR=SI, MySQL RR=SI+next-key locks.
- Inventory → atomic conditional update; ledger → SERIALIZABLE; bloat → vacuum.

## 19. Quiz
1. Which answer best explains isolation? a) all-or-nothing b) serial equivalence c) survives crash d) constraints → **b**
2. At which level is a dirty read possible? a) RC b) RU c) RR d) S → **b**
3. `SELECT FOR UPDATE` in MVCC engines: a) snapshot read b) locking read c) no lock d) view → **b**
4. Snapshot isolation does NOT prevent: a) dirty reads b) non-repeatable reads c) write skew d) phantoms-in-read → **c**
5. Deadlock victim is chosen by (InnoDB): a) age b) rollback work c) priority d) name → **b**
6. Postgres detects deadlock: a) instantly b) after 1s timeout c) never d) at commit → **b**
7. The "bloat" problem is caused by: a) undo log b) old tuple versions c) WAL d) indexes → **b**
8. A dirty read is reading: a) a committed value b) an uncommitted, possibly rolled-back value c) a snapshot d) a phantom → **b**

## 20. Flashcards
- **Q: Name ACID + mechanisms.** → **A:** Atomicity←undo; Consistency←constraints; Isolation←locking/MVCC; Durability←redo+fsync.
- **Q: Level→anomaly map.** → **A:** RU dirty; RC non-repeatable; RR phantom; S none.
- **Q: Why is 2PL serializable but not deadlock-free?** → **A:** Locks order conflicts (acyclic graph) but still allow circular waits.
- **Q: Postgres vs MySQL RR.** → **A:** PG pure SI; MySQL SI + next-key locks.
- **Q: Inventory decrement idiom?** → **A:** `UPDATE ... SET qty=qty-1 WHERE ... AND qty>=1` + rowcount check.
- **Q: What to do on 40001?** → **A:** Retry the whole transaction (with backoff).
- **Q: What does VACUUM do?** → **A:** Reclaims dead tuple versions no snapshot can see.
- **Q: When is optimistic better?** → **A:** Low conflict rate / cheap retries.

## 21. Revision
Every transaction question reduces to: definition → mechanism → example → caveat. Own the level→anomaly table, the 2PL phases, MVCC's snapshot + write-skew gap, and the Postgres-vs-MySQL defaults. Scenario answers use three idioms: inventory (atomic conditional UPDATE), ledger (SERIALIZABLE/FOR UPDATE), debugging (check lock order, scans, transaction length). Practice speaking all 28 answers aloud before interview day.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "ACID / transaction basics" | Q1-Q6 |
| "Isolation levels and anomalies" | Q7-Q13 |
| "2PL, MVCC, timestamps, deadlock" | Q14-Q21 |
| "Detect anomaly in a schedule" | Q26 |
| "Design inventory / ledger / booking" | Q24-Q25 |
| "Debugging bloat / deadlock storms" | Q22-Q23 |
| "Optimistic vs pessimistic choice" | Q17, Q24 |
| "When to weaken durability" | Q28 |
