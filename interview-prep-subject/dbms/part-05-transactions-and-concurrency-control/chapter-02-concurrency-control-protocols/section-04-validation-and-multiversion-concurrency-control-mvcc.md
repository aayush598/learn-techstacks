# Validation and Multiversion Concurrency Control (MVCC)

> **TL;DR**: Validation (optimistic) concurrency control lets transactions run without locking and checks conflicts only at commit; MVCC goes further — readers never wait by reading old versions — and together they're the backbone of every modern OLTP engine (Postgres, MySQL InnoDB, Oracle).

## 1. Why Does This Exist?
2PL and timestamp ordering make decisions *up front* (locks/timestamps at each operation), which costs either waiting (locks) or aborting work (timestamps). Validation asks: what if we let transactions run freely — optimistically — and only *check* at commit whether anyone conflicted? And MVCC answers a different pain: the *readers* under 2PL are the ones who wait (a reader must wait for a writer's commit to take the lock). MVCC's core insight: **readers should never block, and never be blocked** — they read a consistent *snapshot* built from old versions. Both exist to squeeze out the waiting that plagues 2PL: validation eliminates *premature* waiting, MVCC eliminates *reader* waiting. They're the reason modern DBMSes get thousands of concurrent reads while a write is in flight.

## 2. How Does It Work?
**Validation (Optimistic Concurrency Control, OCC)**: each transaction runs in three phases — **read** (read data, record its read set), **validate** (at commit, check whether any transaction it read from has since committed a conflicting write, or whether overlapping write sets conflict), **write** (apply writes). A transaction is *validated* (allowed to commit) if, for each item it wrote, no transaction that read it (or a transaction it read) committed a conflicting write during the transaction's lifetime. Otherwise abort.
**MVCC**: each write creates a *new version* of the row tagged with the writer's timestamp (commit number). A reader selects the version whose timestamp is ≤ its snapshot timestamp and invisible if the version is uncommitted (or belongs to a transaction that will abort). Version chains (in-row or in a separate undo log) let old snapshots read "the past." Write-write conflicts: first writer wins, the second blocks (locks) or aborts. **Snapshot Isolation (SI)**: the specific MVCC policy that gives every transaction a snapshot at first read; it prevents dirty/non-repeatable reads and phantoms-in-reads but is *not serializable* (write skew).

## 3. When Is It Used?
- **MVCC**: every major OLTP engine — Postgres (default; undo-free, versions in table), MySQL InnoDB (undo log), Oracle (undo segments), SQL Server (SNAPSHOT isolation), and many NoSQL stores (HBase, TiDB, CockroachDB). Used when read/write mixes dominate OLTP and readers must never block.
- **Validation/OCC**: main-memory databases (VoltDB-style single-threaded partitions), low-contention OLTP, some distributed transaction systems (Calvin, FoundationDB conflict detection), and app-level patterns (optimistic locking via version columns). Used when writes rarely conflict.
- In interviews: "what is optimistic vs pessimistic concurrency?", "how does MVCC work?", "what is snapshot isolation?", "write skew", "why are Postgres reads lock-free?"

## 4. Why Wasn't Another Approach Chosen?
- *2PL for everything (pessimistic)*: guarantees safety by blocking, but under read-heavy OLTP readers block on writers — the exact problem MVCC removes. Pessimistic control is right when conflicts are frequent or the cost of abort is catastrophic (e.g., a seat you must hold).
- *Validation vs 2PL*: validation avoids locking overhead when conflicts are *rare* (most transactions succeed, no wait); but under high contention it aborts far more work than locking, and a long read transaction can be invalidated by a single late write. That's why OCC is chosen for low-contention and in-memory systems.
- *Basic timestamp ordering for reads*: TO makes reads abort too often; MVCC *never aborts reads* — a read just picks a compatible version. MVCC beats TO on read-heavy workloads decisively.
- *Shadow paging / copy-on-write at the DB level*: an alternative to per-row versions, but writing whole pages is too expensive — MVCC versioning is per-row (or per-index-entry), much finer.
- *Predicate locking to fix phantoms*: MVCC with SI avoids phantoms in *reads* cheaply (snapshot); fixing it *fully* (write skew, serializable) needed SSI — the "add serializability to MVCC" approach rather than going back to locks.

## 5. Intuition
MVCC is a **time-traveling library**. Every book (row) has multiple editions (versions) with a publication date (commit timestamp). A reader entering the library at a given moment gets a snapshot of the catalog "as of then" and reads only editions published by then — even if a new edition is being printed right now (uncommitted), the reader never sees it, and never waits for the printer. Writers: if two people try to publish a *new* edition of the same book, only the first succeeds; the second must wait or withdraw (write-write conflict). The validation protocol is like a **homework-review meeting**: everyone does their work independently (read phase), then at the meeting (validate) the teacher checks nobody's answers contradict a classmate's *committed* work; if they do, you redo (abort).

## 6. Real-World Analogy
**Wikipedia editing**: readers see whatever version is "live" — but consider a wiki that keeps every revision. A viewer who opened the page at 3:00pm continues to see the 3:00pm revision even as others save new edits (MVCC snapshot). Two editors simultaneously editing the same article: the platform either blocks the second (pessimistic edit lock) or warns "this article was edited since you loaded it — merge or overwrite" (optimistic validation). And a researcher who wants the full *history* (all versions) reads the old revisions — exactly what a long MVCC snapshot does.

## 7. Formal Definition
**Validation (OCC)** — each transaction T has a start time and a validation time. Phases: read (collect read set RS(T) and write set WS(T)), validate, write. T is allowed to commit iff, for every transaction T' that committed *after* T started, the following holds: WS(T) ∩ RS(T') = ∅ and WS(T) ∩ WS(T') = ∅ (no read/write or write/write overlap with later-committed transactions that could see T's values). Otherwise abort.
**Snapshot Isolation (MVCC policy)**: a transaction's reads see the snapshot as of its **snapshot time** (first read or transaction start); its own writes become visible to itself immediately; a write-write conflict (two transactions modifying the same row) causes one to abort. **SI prevents**: dirty reads, non-repeatable reads, phantoms (within the snapshot). **SI does NOT prevent**: write skew (two transactions writing disjoint rows based on overlapping reads that combine to violate an invariant). SI is **not serializable**.
**Version chain**: each row has old→new versions linked (or reconstructed from an undo log); a version is visible to snapshot S if its commit-timestamp ≤ S and its transaction committed.

## 8. Example
Table `accounts`:
```
Row(id=1, balance=100)  v0: committed, ts=10
Row(id=2, balance=50)   v0: committed, ts=10
```
- T1 (snapshot ts=20): reads id=1 → sees balance=100 (v0).
- T2 (snapshot ts=21): `UPDATE accounts SET balance=balance-20 WHERE id=1` → creates v1 (balance=80), commit ts=22. T1's *next* read of id=1 still sees 100 (v0 ≤ 20) → **repeatable read**.
- T3 (snapshot ts=23): reads id=1 → sees 80 (v1, since 22 ≤ 23).
- Write-write: T4 (ts=24) updates id=2 to 40 (v1). T5 (ts=25) updates id=2 to 30 → conflict with T4's v1 on id=2 → T5 waits; if T4 commits, T5 must re-evaluate (InnoDB deadlock/dup) or aborts.
- **Write skew example**: two doctors: T1: `if SELECT count(patients on duty) = 1 then UPDATE (doc A sets off-duty)`. T2 likewise for doc B. Both read "1 doctor on duty", both write their own row (disjoint), both commit → now 0 doctors on duty, invariant broken. Both succeeded under SI — only SERIALIZABLE (SSI) catches it.

## 9. Internal Working
1. Transaction begins → DBMS assigns a snapshot/transaction ID (Postgres XID; InnoDB transaction id; read view structure).
2. On first read, the snapshot's "visible up to" boundary is fixed: committed transactions with ID ≤ boundary are visible; anything later or in-flight is invisible.
3. A write creates a new version (InnoDB: writes to the row + undo record in undo log; Postgres: new tuple version, old one left for concurrent snapshots). The row gains commit info (XID, status).
4. Visibility check per row: compare the row version's commit timestamp/status against the snapshot. Postgres: `xmin`/`xmax`/`cmin`/`cmax` + hint bits; InnoDB: `DB_TRX_ID`/`DB_ROLL_PTR` in the clustered index.
5. Read-write conflicts: MVCC readers never lock. Write-write conflicts: the second writer blocks on the row's write lock (or aborts) — this is where 2PL still applies (for writers).
6. Old versions get reclaimed: Postgres `VACUUM` (removes versions older than all active snapshots); InnoDB purge thread (via undo log); MySQL "history list length" tracks pending purges.
7. **SSI** (Postgres SERIALIZABLE): on top of SI, track read/write *dependencies* between concurrent transactions; when a "dangerous structure" appears (a write-write or read-write cycle pattern), abort one transaction.

## 10. Time Complexity
- Read with MVCC: O(1) visibility check + O(version-chain length) worst case if old versions must be chased; indexes + vacuum keep it ~O(1) amortized.
- Write: O(1) version create + log record.
- Validation (OCC): O(|RS| + |WS|) per commit for conflict checks vs concurrent transactions; often kept in-memory O(1)-ish in main-memory DBs.
- Vacuum/purge: amortized O(dead versions); a long-running read holds old versions alive → table bloat (a real production cost).

## 11. Advantages
- **Readers never block and never are blocked** — the #1 reason MVCC dominates OLTP.
- **Writers rarely block readers or other writers of *different* rows** — high concurrency.
- **SI prevents the "standard" anomalies** (dirty, non-repeatable, phantom-in-read) cheaply with no locks on reads.
- **OCC avoids lock overhead entirely when conflicts are rare** — best-case throughput, no deadlock, no lock manager.
- **Snapshot reads are consistent** — a transaction's whole view is one instant, ideal for reporting.

## 12. Disadvantages
- **Write skew is not prevented** by SI — apps that need serializability must use SERIALIZABLE (SSI) or explicit locks.
- **Write-write conflicts still serialize/abort** — two writers to the same row can't both succeed.
- **Storage bloat**: old versions accumulate; vacuum/purge lag causes table growth and index bloat (Postgres tables grow, InnoDB undo grows).
- **OCC's validation phase can abort long transactions unfairly** under contention; retry storms.
- **More complex internals**: version chains, visibility logic, vacuum — bugs here corrupt reads (e.g., Postgres's infamous bloat/visibility edge cases).
- **Not directly portable**: each engine's MVCC has different semantics (Postgres vs MySQL vs Oracle differ subtly) — a source of interview traps.

## 13. Interview Questions
1. **Q: What is MVCC?** A: Multiversion Concurrency Control: instead of locking reads, the DBMS keeps multiple versions of each row (tagged with commit info); each transaction reads a consistent snapshot of versions, so readers never block writers and vice versa. Write-write conflicts are resolved by blocking or aborting the second writer.
2. **Q: What is snapshot isolation?** A: An MVCC policy: every transaction sees the committed database state as of its snapshot time; it sees its own writes; write-write conflicts cause an abort. It prevents dirty reads, non-repeatable reads, and phantoms (in reads) but allows write skew — so it is NOT serializable.
3. **Q: Why are MVCC reads lock-free?** A: Because the reader reads a *version* consistent with its snapshot; it never needs to wait for a writer's commit, since the writer's uncommitted version is invisible to it. The reader doesn't hold a lock that would block anyone.
4. **Q: What is a write skew and why does SI allow it?** A: Two transactions read overlapping data but write *disjoint* rows; each individually maintains invariants, but together they violate one (e.g., two doctors both see "1 doctor on duty" and both go off-duty). Since each wrote a *different* row, no write-write conflict fires — so SI lets both commit. Only serializable (SSI) or explicit locks prevent it.
5. **Q: TRICKY: What's the difference between a dirty read and reading an uncommitted version under MVCC?** A: MVCC never *exposes* uncommitted versions to other transactions — an in-flight write is invisible (the reader sees the older committed version). A dirty read is precisely the failure to hide in-flight writes; MVCC+snapshot prevents it by construction.
6. **Q: How does OCC (validation) differ from MVCC?** A: OCC lets transactions run with no versioning/blocking at all and validates at commit (checking read/write set overlaps), aborting on conflict. MVCC keeps versions and serves reads from snapshots; it blocks only on write-write conflicts. OCC has no "reader history" (readers see live data); MVCC has snapshots.
7. **Q: When would you choose OCC over locking/MVCC?** A: When conflicts are rare and abort cost is low (low write contention, e.g., app-level optimistic locking with a version column), or in main-memory DBs where validation is cheap. Under heavy contention OCC aborts too much work — pessimistic wins there.
8. **Q: PRODUCTION: How does Postgres implement MVCC?** A: Each row version carries `xmin`/`xmax` (inserting/deleting XID) plus status bits; a transaction's snapshot is a list of in-flight XIDs + horizon. Visibility: version is visible if `xmin` committed & ≤ horizon, `xmax` not committed or ≥ horizon. Old versions are removed by `VACUUM`. No undo log — version garbage is handled by vacuum.
9. **Q: PRODUCTION: How does MySQL InnoDB implement MVCC?** A: Row carries `DB_TRX_ID` (last writer) and `DB_ROLL_PTR` (undo record). The undo log reconstructs old versions; `READ VIEW` stores the set of active transactions at snapshot time. Purge thread cleans up. This differs from Postgres's in-table versioning — and from Oracle (undo in separate tablespaces).
10. **Q: TRICKY: Does MVCC prevent phantoms at REPEATABLE READ?** A: In *reads* — yes: the snapshot is fixed, so a range query can't see newly inserted rows. In *writes* — the classic SI phantom (a "write skew on predicates", e.g., inserting a duplicate in a range another transaction read) can occur. MySQL's REPEATABLE READ adds next-key locks on write paths to close the insert conflict; Postgres's RR (pure SI) does not — a known semantic gap.
11. **Q: What causes MVCC bloat and how is it cleaned?** A: Every update leaves the old version alive until no snapshot can see it. Long-running transactions extend the horizon, so garbage piles up (table/index bloat, undo growth). Postgres: `VACUUM` (autovacuum); InnoDB: purge threads; Oracle: undo retention. Bloat degrades scan performance and bloats storage.
12. **Q: What is the difference between SI and SERIALIZABLE in Postgres?** A: REPEATABLE READ = SI (write skew allowed). SERIALIZABLE = SSI (Serializable Snapshot Isolation): tracks r/w dependencies and aborts transactions that form dangerous structures, achieving serializable while keeping snapshot-based non-blocking reads.
13. **Q: How do you implement optimistic locking in an application?** A: Add a `version` column; `UPDATE ... SET version=version+1 WHERE id=? AND version=?`; check `ROW_COUNT()==1`, else retry or report conflict. This is app-level validation on top of a plain engine.
14. **Q: TRICKY: Can MVCC and 2PL coexist?** A: Yes — and they do: MVCC handles *read* isolation (lock-free snapshots) while a 2PL-style lock system handles *write-write* conflicts (the second writer blocks on the row's write lock until the first commits/aborts). That's exactly Postgres and InnoDB: MVCC for reads, locking for writes.

## 14. Follow-Up Questions
1. **Q: What is the "history list length" in InnoDB and why does it matter?** A: The number of un-purged undo records; a long value means bloat — long transactions or a lagging purge thread. Monitoring it catches runaway transactions.
2. **Q: Why is OCC not used as the default in most DBMSes?** A: Because production OLTP has enough contention that validation aborts too often, and the engines can't know conflict rates in advance; MVCC's "readers free, writers lock" fits the 80% read / 20% write profile better. OCC shines in specialized in-memory/low-contention systems.
3. **Q: What is `xmin`/`xmax` in Postgres?** A: `xmin` = the XID that created the tuple version; `xmax` = the XID that deleted/updated it (or 0 = not deleted). Combined with hint bits (inserted/committed flags), they determine a version's visibility to a snapshot.

## 15. Coding Example
```sql
-- MVCC snapshot visibility walkthrough (Postgres semantics)
CREATE TABLE accounts (id int PRIMARY KEY, balance int);
INSERT INTO accounts VALUES (1, 100);
-- Session A (long transaction):
BEGIN; SELECT balance FROM accounts WHERE id=1;   -- snapshot taken, sees 100
-- Session B:
UPDATE accounts SET balance = 50 WHERE id=1; COMMIT;
-- Session A (still in same transaction):
SELECT balance FROM accounts WHERE id=1;          -- STILL 100 → repeatable read / MVCC
```
```python
# App-level optimistic locking (validation OCC pattern)
def transfer(conn, account_id, amount, max_retries=5):
    for _ in range(max_retries):
        cur = conn.execute(
            "SELECT balance, version FROM accounts WHERE id = %s", (account_id,))
        balance, version = cur.fetchone()
        if balance < amount:
            raise InsufficientFunds()
        updated = conn.execute(
            "UPDATE accounts SET balance=%s, version=version+1 "
            "WHERE id=%s AND version=%s",
            (balance - amount, account_id, version))
        if updated.rowcount == 1:
            return                       # validation passed, committed
        # else: someone else changed it → retry (validate-and-abort loop)
```
```sql
-- Prevent write skew at SI: use SSI or explicit locking
BEGIN ISOLATION LEVEL SERIALIZABLE;       -- Postgres: SSI
UPDATE doctors SET on_duty=false WHERE id=1;
-- SSI will abort one of two concurrent such transactions if it detects the skew
COMMIT;
```

## 16. Industry Usage
- **PostgreSQL**: MVCC with in-table versions, `VACUUM`, SSI for SERIALIZABLE; the flagship of MVCC-visible semantics.
- **MySQL InnoDB**: MVCC + undo log + next-key locks; REPEATABLE READ default; purge threads.
- **Oracle**: undo tablespace-based MVCC ("read consistency"); SERIALIZABLE is snapshot-based (write skew possible — a famous divergence).
- **SQL Server**: SNAPSHOT isolation via version store in tempdb; READ COMMITTED SNAPSHOT option.
- **Distributed MVCC**: CockroachDB (MVCC + hybrid clocks + serializable), TiDB, HBase (versioned cells), Spanner (MVCC + TrueTime). MVCC is *the* standard for cloud OLTP and many NoSQL stores.

## 17. References
- Berenson et al., "A Critique of ANSI SQL Isolation Levels", SIGMOD 1995 — places SI in the anomaly framework.
- Cahill, Röhm, Fekete, "Serializable Isolation for Snapshot Databases", SIGMOD 2009 — SSI.
- Fekete et al., "Making Snapshot Isolation Serializable" (2005) — write-skew analysis.
- PostgreSQL docs, MVCC: https://www.postgresql.org/docs/current/mvcc.html
- MySQL 8.0 InnoDB multi-versioning: https://dev.mysql.com/doc/refman/8.0/en/innodb-multi-versioning.html
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 16.5 (validation) & 16.6 (MVCC).
- Elmasri & Navathe, Ch. 21.

## 18. Cheat Sheet
- MVCC = keep versions; reads use snapshots → readers never block.
- Snapshot Isolation: snapshot at first read; own writes visible; write-write → abort/block second.
- SI prevents dirty/non-repeatable/phantom-in-reads; allows write skew → NOT serializable.
- OCC/validation: read→validate→write; abort on read/write set overlap at commit. Best when conflicts rare.
- MVCC internals: Postgres `xmin`/`xmax`+vacuum; InnoDB `DB_TRX_ID`/`DB_ROLL_PTR`+undo+purge.
- Write-write conflicts still use locks (MVCC + 2PL coexist).
- Bloat = old versions piling up; fix with VACUUM/purge; long transactions worsen it.
- SSI makes MVCC serializable (Postgres SERIALIZABLE).

## 19. Quiz
1. Under MVCC, a reader: a) blocks on writers b) reads an old version c) takes X-locks d) aborts → **b**
2. Snapshot isolation prevents: a) write skew b) dirty reads c) lost-update-only d) nothing → **b**
3. Which anomaly does SI allow? a) dirty read b) non-repeatable read c) write skew d) phantom-in-read → **c**
4. MVCC write-write conflict is resolved by: a) aborting both b) the second blocks/aborts c) versioning d) timestamps → **b**
5. OCC's validate phase checks: a) locks b) read/write set overlaps c) timestamps d) gap locks → **b**
6. Postgres removes old versions via: a) purge thread b) VACUUM c) undo log d) shadow pages → **b**
7. SSI is used to make MVCC: a) faster b) serializable c) lock-free writes d) durable → **b**
8. OCC is best suited to: a) high contention b) low contention c) read-heavy always d) never → **b**

## 20. Flashcards
- **Q: Core MVCC idea?** → **A:** Multiple row versions; readers use snapshots and never block writers (or each other).
- **Q: What is snapshot isolation?** → **A:** Each transaction sees a snapshot as of its first read; own writes visible; write-write conflict → abort/block.
- **Q: What does SI prevent and not prevent?** → **A:** Prevents dirty/non-repeatable/phantom-in-reads; NOT write skew (not serializable).
- **Q: How do MVCC and 2PL coexist?** → **A:** MVCC serves lock-free reads; 2PL-style locks handle write-write conflicts.
- **Q: Postgres MVCC internals?** → **A:** `xmin`/`xmax` + hint bits on versions; VACUUM reclaims garbage.
- **Q: InnoDB MVCC internals?** → **A:** `DB_TRX_ID`/`DB_ROLL_PTR` + undo log; purge thread reclaims.
- **Q: What is OCC's three phases?** → **A:** Read → Validate → Write (abort on conflict at validate).
- **Q: When choose OCC?** → **A:** Low write contention / cheap aborts (in-memory, app version columns).

## 21. Revision
MVCC: readers read snapshots of old versions → never block, never blocked; writers still 2PL-lock write-write conflicts. Snapshot isolation prevents dirty/non-repeatable/phantom-in-read but allows write skew → not serializable; Postgres SERIALIZABLE = SSI fixes it. OCC/validation: run free, validate at commit (read/write set overlap), abort on conflict; great for low contention. Internals: Postgres `xmin/xmax`+VACUUM; InnoDB `DB_TRX_ID/DB_ROLL_PTR`+undo+purge. Watch for: bloat from long transactions, "SI is not serializable," "MVCC readers don't take shared locks."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is MVCC and why is it used?" | 1, 2, 13 |
| "What is snapshot isolation?" | 2, 7, 13 |
| "What is write skew?" | 8, 13 |
| "Why are MVCC reads lock-free?" | 1, 9, 13 |
| "OCC vs MVCC vs 2PL?" | 4, 13 |
| "How does Postgres/InnoDB implement MVCC?" | 9, 13, 16 |
| "MVCC bloat / vacuum?" | 13, 14, 16 |
| "What is SSI?" | 9, 13 |
