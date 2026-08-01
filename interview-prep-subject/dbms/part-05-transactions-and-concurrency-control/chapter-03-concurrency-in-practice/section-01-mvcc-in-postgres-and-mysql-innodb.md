# MVCC in Postgres and MySQL InnoDB

> **TL;DR**: Both Postgres and MySQL InnoDB are MVCC engines, but they implement it differently — Postgres keeps old versions *in the table* and cleans them with VACUUM, while InnoDB keeps old versions in an *undo log* and rebuilds them on demand with a purge thread — which is why their "REPEATABLE READ" semantics differ.

## 1. Why Does This Exist?
Theory says "readers should read old versions" (MVCC), but the theory doesn't say *where the old versions live*. Two production answers emerged. PostgreSQL chose **in-table versioning**: each update creates a new tuple version; the old tuple stays put, tagged with visibility metadata, until VACUUM reclaims it. MySQL InnoDB chose **undo-log versioning**: the row keeps its newest value plus a rollback pointer; reading an old snapshot walks the undo log to reconstruct the old value. These two designs exist to answer the same practical question — "how do I serve many concurrent readers a consistent view without blocking?" — under different constraints: Postgres optimizes for *no extra storage layer* and snapshot reads (versions are directly in the page), InnoDB optimizes for *row locality* and write amplification (only the current value lives in the index; old values live compactly in the undo log).

## 2. How Does It Work?
**PostgreSQL**:
- Every tuple carries `xmin` (XID that created it) and `xmax` (XID that deleted/superseded it) plus `cmin`/`cmax` (command counters) and hint bits (`HEAP_XMIN_COMMITTED` etc.).
- A transaction's snapshot is a structure with `xmin` (oldest active), `xmax` (next XID to be assigned), and `xip_list` (in-flight XIDs). Visibility: a tuple version is visible to snapshot S if `xmin` is committed and ≤ S.xmax and not in S's in-flight list, and `xmax` is 0 or not committed (or the deleting XID is not visible to S).
- `UPDATE` = insert a new tuple version + mark old one deleted (a "chain" via `ctid`). `VACUUM` (and autovacuum) removes tuples no snapshot can see.

**MySQL InnoDB**:
- Each row in the clustered index carries `DB_TRX_ID` (last writer's transaction ID) and `DB_ROLL_PTR` (pointer into the undo log).
- A `READ VIEW` is a snapshot of active transaction IDs. Visibility: a row version is visible if `DB_TRX_ID` is committed and < read-view's minimum active ID (or is in the view's committed set).
- `UPDATE` writes the new value + an *undo record* describing the before-image. An old snapshot reading the row finds `DB_TRX_ID` too new, then follows `DB_ROLL_PTR` through undo records to reconstruct the older value.
- A purge thread deletes undo records (and marks row versions) once no read view needs them.

## 3. When Is It Used?
- Postgres MVCC runs on *every* SELECT/UPDATE/INSERT/DELETE — it's not optional; isolation levels merely pick the snapshot policy (READ COMMITTED = new snapshot per statement; REPEATABLE READ = one per transaction).
- InnoDB MVCC runs on every DML under READ COMMITTED/REPEATABLE READ (its defaults); SERIALIZABLE switches plain SELECTs to locking reads (locking disables the snapshot path).
- Used for: OLTP with mixed reads/writes, long reporting transactions (must not be disturbed by writes), online upgrades/schema changes with low lock impact.
- In interviews: "how does Postgres implement MVCC?", "xmin/xmax", "why does your table grow after many updates?", "undo log vs vacuum".

## 4. Why Wasn't Another Approach Chosen?
- *Postgres: separate undo log (like InnoDB)* — rejected for Postgres's design because (a) it adds a write to a second structure per update (higher write amplification), (b) it needs a purge/compact subsystem, (c) visibility must then reconstruct old tuples on demand (CPU cost per read of old versions). Postgres traded that for "old versions are free to read (they're in the page), at the cost of table bloat + vacuum."
- *InnoDB: in-table versions (like Postgres)* — rejected because (a) each update rewrites the page and leaves dead tuples bloating the clustered index, hurting scan locality, (b) InnoDB's page structure is optimized around a *current* row; (c) undo log is also reused for rollback (abort needs the before-image anyway), so the mechanism is "free" for MVCC. InnoDB trades that for write-amplification on undo + read-amplification when reconstructing old versions.
- *Pure locking without versions* — rejected: readers would block writers; both engines chose non-blocking reads.
- *A single global snapshot + COW whole database* (shadow paging) — too expensive; per-row versioning is the fine-grained alternative.

## 5. Intuition
**Postgres** is like a **whiteboard that keeps every draft**: when you update, you draw the new value and leave the old one underneath with a "retired on <date>" note. Readers glance at the current draft but can "read backwards" by peeling layers. Every so often a janitor (VACUUM) erases drafts nobody can still be reading — but if a long meeting (long transaction) is reading an old draft, the janitor must wait, and the board grows.
**InnoDB** is like a **notebook that only keeps the latest line, plus a margin note "to restore the previous line, see page 200 of the archive"** (undo log). To read an old value you visit the archive and re-derive it. An archivist (purge thread) destroys archive pages nobody needs anymore.

## 6. Real-World Analogy
A **wiki with revision history**: Postgres keeps the full revision *inline* (every version is a click away in the same page list) but the page list grows and must be archived (vacuum). InnoDB keeps the current revision on the page and stores the diffs/old revisions in a separate archive box (undo), reconstructing older views by "undoing" the newest edits — efficient for the page, but reading history costs an archive lookup. Same feature ("view the page as of 3pm"), different cost profile — exactly why the two engines chose different storage layouts.

## 7. Formal Definition
**PostgreSQL MVCC visibility** (simplified rule set used by `HeapTupleSatisfiesSnapshot`): a tuple version with creating XID `xmin`, deleting XID `xmax` is visible to snapshot `{xmin_s, xmax_s, xip_list}` iff:
- `xmin` is committed and not aborted and `xmin < xmax_s` and `xmin ∉ xip_list`, AND
- `xmax = 0` OR (`xmax` not committed) OR (`xmax ≥ xmax_s`) OR (`xmax ∈ xip_list` — the deleting transaction is itself in-flight, so it hasn't "taken effect").
**InnoDB visibility** (`row_vers_build_for_read` + `ReadView`): a row version is visible if `DB_TRX_ID < view->m_low_limit_id` and (`DB_TRX_ID < view->m_up_limit_id` OR `DB_TRX_ID ∈ committed-IDs set`); otherwise the undo log (`DB_ROLL_PTR`) is followed to build the older version and the check repeats.

## 8. Example
`accounts(id=1, balance=100)`. Timeline with transaction IDs:
- XID 100: `INSERT (id=1, balance=100)` → tuple v1, xmin=100. Committed.
- XID 110: `BEGIN; UPDATE accounts SET balance=70 WHERE id=1;` → new tuple v2 (xmin=110, balance=70), old v1 gets xmax=110. (Postgres) / InnoDB: row's DB_TRX_ID=110, DB_ROLL_PTR → undo rec (balance=100).
- XID 111: `SELECT` (snapshot S, in-flight=[110], xmax_s=112) → sees v1 (xmin=100 committed, 100 < 112, 100∉in-flight; xmax=110 is in-flight) → **balance=100** — the uncommitted write by 110 is invisible.
- XID 110 commits. XID 112: `SELECT` → sees v2 (xmin=110 committed) → balance=70. InnoDB: DB_TRX_ID=110 committed < 112's view → visible → 70.
- XID 113: `SELECT` with snapshot started *before* 110 committed → still 100 (snapshot isolation). Postgres: v1's xmax=110 is committed → is 110 "visible"? v1 is invisible if xmax committed AND 110 < 113's horizon. Since 110 committed and ≤ horizon, v1 is dead → invisible → reader gets v2 (70). Wait — but the reader's snapshot predates 110's commit: Postgres *does* handle this — the snapshot in READ COMMITTED is per-statement, so by XID 113's statement 110 is committed and v2 is read. The "before 110 committed" case only applies if the snapshot was taken while 110 was in-flight.

## 9. Internal Working
**Postgres**:
1. `BEGIN` → assign XID lazily (on first write). First statement/read → build snapshot (READ COMMITTED: per statement; RR/SERIALIZABLE: first read of transaction).
2. Every tuple read is tested via `HeapTupleSatisfiesXxx` using the snapshot — no locks for MVCC reads.
3. `UPDATE` → `heap_update`: new tuple inserted with xmin=self, old tuple's xmax=self (points via `ctid`). Indexes updated (index entries may be updated, hence index bloat).
4. Commit → mark tuple `HEAP_XMIN_COMMITTED` (hint bit) via `SetHintBits`; aborts get `HEAP_XMIN_INVALID`/CLOG lookup fallback.
5. `VACUUM`/`autovacuum`: scans tables, removes tuples whose `xmax` is committed and old enough (below `vacuum_defer_cleanup_age` / `OldestXmin`), updates visibility maps, freezes tuples older than `freeze_min_age` (sets hint bits so `xmin` needn't be consulted), so wrap-around of XIDs is safe.
6. Old XID wrap-around: `VACUUM FREEZE` and `max_wal_size`-controlled anti-wraparound vacuum (transaction ID wraparound prevention).

**InnoDB**:
1. `START TRANSACTION` → transaction object in `trx_sys`.
2. First read builds a `ReadView` (list of active trx IDs). Consistency: rows with `DB_TRX_ID` not visible → follow `DB_ROLL_PTR` through undo log to build the old version (`row_vers_build_for_read`) — undo records are linked in reverse-chronological order.
3. `UPDATE` → create undo record with before-image; set row `DB_TRX_ID`/`DB_ROLL_PTR`; the record enters the current transaction's undo log (rollback needs it too).
4. Commit → purge thread later removes undo records once `ReadView` no longer needs them; marks the row version as garbage (or retains for historical/`READ VIEW`).
5. Locking: InnoDB combines MVCC *reads* with **record/gap/next-key locks** on DML and `SELECT ... FOR UPDATE` — so write-write conflicts are lock-based (2PL), and phantoms are prevented at REPEATABLE READ via next-key locks (unlike Postgres's pure-snapshot RR).

## 10. Time Complexity
- **Postgres read of current version**: O(1) (tuple in page, hint bits set). Read of *old* version: O(1) too — old versions are physically in the page/table (no reconstruction); the cost is table bloat (scan I/O) and vacuum.
- **InnoDB read of current version**: O(1). Read of *old* version: O(undo-chain length) to reconstruct — can degrade with long chains (a known "old reads slow down" phenomenon).
- **Postgres write**: O(1) new tuple + index maintenance; **bloat growth** O(updates) without vacuum.
- **InnoDB write**: O(1) row update + O(1) undo append; purge is amortized.
- **Vacuum/purge**: Postgres O(pages with dead tuples) per vacuum; InnoDB O(undo records) per purge.

## 11. Advantages
- **Postgres**: old versions cost *nothing to read* (no reconstruction); snapshots are cheap; no separate undo storage to manage; vacuum is tunable and observable; full visibility control via hints.
- **InnoDB**: clustered index stays "lean" (one current value per row → good scan locality); undo log is also used for rollback (two jobs, one structure); purge is a background thread, non-blocking; next-key locks give phantom-safe REPEATABLE READ.
- Both: lock-free reads (no reader-writer blocking), snapshot consistency, high OLTP concurrency.

## 12. Disadvantages
- **Postgres**: table & index **bloat** (updates leave dead tuples — a full-rewrite cycle is often needed); vacuum cost and autovacuum tuning; long transactions stall vacuum and can cause catastrophic bloat; REPEATABLE READ does NOT prevent phantom/insert conflicts the way InnoDB does (write skew + SI gaps remain).
- **InnoDB**: **undo log growth** under heavy update workloads (history list length); reconstructing old versions is CPU/undo-chain work; purge lag; REPEATABLE READ's next-key locks *reduce insert concurrency* and can cause confusing deadlocks.
- Both: MVCC complexity — subtle visibility bugs, wraparound issues (Postgres XID wraparound; InnoDB trx ID reuse), and semantics differ per engine (portability trap).

## 13. Interview Questions
1. **Q: How does Postgres implement MVCC?** A: In-table tuple versioning. Each tuple carries `xmin`/`xmax` (creating/deleting XID) + hint bits; an UPDATE inserts a new version and marks the old one deleted. A transaction's snapshot (list of in-flight XIDs + horizon) decides which version is visible. VACUUM reclaims dead versions no snapshot can see.
2. **Q: How does InnoDB implement MVCC?** A: The clustered-index row keeps the *current* value plus `DB_TRX_ID` (last writer) and `DB_ROLL_PTR` (undo-log pointer). A `ReadView` of active transaction IDs determines visibility; an invisible newer row is reconstructed by following undo records (`row_vers_build_for_read`). The purge thread reclaims undo when no view needs it.
3. **Q: What is the difference between the two engines' MVCC storage?** A: Postgres stores old versions *in the table* (no reconstruction on read; vacuum removes them); InnoDB stores old versions *in the undo log* and reconstructs them on demand (purge thread removes them). Postgres pays table bloat; InnoDB pays undo growth + reconstruction cost.
4. **Q: What are `xmin` and `xmax`?** A: `xmin` = the XID that created the tuple version; `xmax` = the XID that deleted/superseded it (0 if not deleted). Combined with hint bits (committed flags), they answer "is this version visible to this snapshot?"
5. **Q: What is a snapshot in Postgres and how is it built?** A: A `Snapshot` holds `xmin` (oldest active XID), `xmax` (next XID to allocate), and `xip` (in-flight XIDs). It's built at the start of each statement (READ COMMITTED) or at the transaction's first read (REPEATABLE READ/SERIALIZABLE). Visibility: `xmin` committed, < xmax, not in-flight, and `xmax` not committed (or invisible).
6. **Q: TRICKY: Why does my Postgres table keep growing even though I only UPDATE rows?** A: MVCC leaves the old tuple versions in place — every update adds a new version. Until VACUUM (autovacuum) reclaims them (only safe once no active snapshot is older), the table grows. Long transactions and heavy update rates are the usual culprits; monitor bloat and tune autovacuum.
7. **Q: What is the "history list length" in InnoDB?** A: The number of un-purged undo records (via `SHOW ENGINE INNODB STATUS` / `information_schema.innodb_metrics`). A high value means purge is lagging — usually caused by long-running transactions holding read views open — and results in undo log growth and possibly slower inserts.
8. **Q: What is a read view in InnoDB?** A: A structure capturing the set of active transaction IDs at snapshot time plus low/up limit IDs; used to decide whether a row's `DB_TRX_ID` version is visible. It's InnoDB's analog of the Postgres `Snapshot`.
9. **Q: Why does Postgres REPEATABLE READ not prevent phantoms the way MySQL does?** A: Postgres REPEATABLE READ is pure snapshot isolation — reads can't see new rows, but a concurrent INSERT that *conflicts with your snapshot's assumption* (e.g., duplicate key, or a predicate you read) is allowed unless a constraint fires; write skew and insert-conflict anomalies remain. InnoDB REPEATABLE READ additionally takes next-key locks on the scanned ranges, so a conflicting INSERT *blocks* until your transaction commits — phantom-safe on the write path.
10. **Q: PRODUCTION: A long-running report is causing a "snapshot too old" error in Oracle or bloating Postgres — what's happening?** A: The report's snapshot pins old versions; in Postgres, autovacuum can't reclaim them (table bloat); in Oracle it raises ORA-01555 (undo overwritten). Mitigations: shorten the report, use READ COMMITTED per-statement snapshots, increase undo retention/vacuum aggressiveness, or snapshot the data into a temp table first.
11. **Q: What is a "tuple chain" and when does Postgres use it?** A: Each new version's `ctid` points to the next version, forming an update chain. Under normal visibility it's followed once; HOT updates (no index columns changed) reuse the same index entry, reducing index churn — the chain walk is also used to find the latest version of a row.
12. **Q: What are hint bits and why do they matter?** A: Bits on the tuple (e.g., `HEAP_XMIN_COMMITTED`, `HEAP_XMIN_INVALID`, `HEAP_XMAX_COMMITTED`) caching the committed/aborted status of `xmin`/`xmax` so the hot path avoids consulting the CLOG. They're set lazily (during reads/writes) and are a famous Postgres performance optimization.
13. **Q: TRICKY: Can two different snapshots in Postgres return different rows for the same table at the same time?** A: Yes — READ COMMITTED builds a new snapshot per statement, so two statements in the same transaction can see different committed states; and two concurrent transactions with different snapshot times see different versions. That's the *definition* of MVCC's consistency model, and the reason non-repeatable reads happen at READ COMMITTED.
14. **Q: How does InnoDB use locks alongside MVCC?** A: MVCC serves *consistent reads* (snapshots); but DML and `SELECT ... FOR UPDATE` take real locks: record locks, gap locks, next-key locks. So InnoDB = MVCC for reads + 2PL-style locks for write-write conflicts and phantom prevention — "locking reads" override the snapshot.
15. **Q: PRODUCTION: Which engine's REPEATABLE READ would you trust for "my transaction must lock the rows it reads"?** A: InnoDB — its next-key locking at REPEATABLE READ genuinely blocks conflicting inserts and makes `SELECT ... FOR UPDATE` range locks. Postgres REPEATABLE READ is snapshot-only; you'd need `FOR UPDATE`/`FOR SHARE` to lock rows and SERIALIZABLE to get SSI for write-skew protection. Pick based on the anomaly you're defending against, not the level name.

## 14. Follow-Up Questions
1. **Q: What is the transaction ID wraparound problem in Postgres?** A: XIDs are 32-bit (≈4 billion); after wraparound, old transactions could look "in the future." `VACUUM FREEZE` marks tuples as frozen (never needs re-check), and anti-wraparound autovacuum enforces it automatically — a production must-watch.
2. **Q: How does `SELECT` at SERIALIZABLE differ from REPEATABLE READ in Postgres?** A: Same snapshot mechanics, but SSI additionally tracks read/write dependencies and aborts transactions forming "dangerous structures" — closing write skew and achieving true serializability.
3. **Q: What is `DECLARE CURSOR WITH HOLD` and how does it interact with MVCC?** A: A held cursor keeps its snapshot alive across commits/transactions — which can pin old versions (bloat) for as long as it's open. A classic "why is my table growing" answer.

## 15. Coding Example
```sql
-- Postgres: observe MVCC state
SELECT age(xmin), xmin, xmax, ctid, balance
  FROM accounts WHERE id = 1;          -- age(xmin) tells you version age

BEGIN;
SELECT pg_current_xact_id();           -- my XID
UPDATE accounts SET balance = 90 WHERE id = 1;   -- creates new version
-- In another session: the old value is still readable (snapshot)
COMMIT;

-- Watch vacuum reclaim dead versions
SELECT n_dead_tup FROM pg_stat_user_tables WHERE relname='accounts';
VACUUM VERBOSE accounts;               -- prints how many dead tuples removed
```
```sql
-- MySQL: observe InnoDB MVCC metadata (8.0)
SELECT trx_id, trx_state, trx_rows_modified
  FROM information_schema.innodb_trx;
SELECT index_name, lock_type, lock_mode, lock_data
  FROM performance_schema.data_locks;      -- record/gap/next-key locks you hold

SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
SELECT * FROM accounts WHERE id = 1;       -- consistent read (snapshot)
-- In another session update id=1 ... here you still see the old snapshot
```
```python
# Snapshot vs current read in MySQL: consistent read vs locking read
import pymysql
conn = pymysql.connect(...)
with conn:
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE id=1")        # snapshot (MVCC)
    cur.execute("SELECT balance FROM accounts WHERE id=1 FOR UPDATE")  # locking read
```

## 16. Industry Usage
- **PostgreSQL**: MVCC is the foundation of all its isolation semantics; used by Meta (at massive scale), Uber, Reddit, Instacart, and every Postgres-heavy stack. `pg_stat_user_tables.n_dead_tup`, autovacuum tuning, and bloat reports are daily ops concerns.
- **MySQL InnoDB**: MVCC + undo log + next-key locks; powers Meta's social graph, many e-commerce systems; `history list length` monitoring is standard.
- **Amazon Aurora** (Postgres & MySQL compatible): inherits these MVCC designs; storage is distributed but versioning semantics match the engines.
- **TiDB / CockroachDB**: MVCC with per-key versions + timestamp/clock coordination — extending the same ideas geo-distributed.
- Every DB candidate should be able to describe *both* engines' MVCC and the production signals (dead tuples, history list, wraparound).

## 17. References
- PostgreSQL docs, MVCC: https://www.postgresql.org/docs/current/mvcc.html and internals: https://www.postgresql.org/docs/current/storage-page-layout.html
- PostgreSQL source: `src/backend/access/heap/heapam_visibility.c` (`HeapTupleSatisfiesSnapshot`).
- MySQL 8.0 docs, InnoDB Multi-Versioning: https://dev.mysql.com/doc/refman/8.0/en/innodb-multi-versioning.html
- MySQL 8.0 docs, InnoDB Locking (record/gap/next-key): https://dev.mysql.com/doc/refman/8.0/en/innodb-locking.html
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 16.6 (MVCC).
- "PostgreSQL: The Ultimate Guide" / PostgreSQL 9.x internals references (Tom Lane talks) for vacuum internals.

## 18. Cheat Sheet
- Postgres MVCC: versions live *in the table*; `xmin`/`xmax` + hint bits; snapshot = in-flight list; VACUUM reclaims; bloat = dead tuples.
- InnoDB MVCC: current value in clustered index + `DB_TRX_ID`/`DB_ROLL_PTR` → undo log holds old versions; ReadView decides; purge thread reclaims.
- READ COMMITTED: new snapshot per statement. REPEATABLE READ: one per transaction. SERIALIZABLE (PG): SSI.
- InnoDB REPEATABLE READ adds next-key locks → phantom-safe writes; Postgres RR is pure SI → write skew possible.
- `SELECT FOR UPDATE` = locking read (overrides MVCC snapshot for those rows).
- Postgres XID wraparound: `VACUUM FREEZE` / anti-wraparound autovacuum.
- Monitor: `n_dead_tup` (PG), `history list length` (InnoDB).
- Both engines: lock-free reads, write-write conflicts still locked.

## 19. Quiz
1. Postgres old tuple versions live: a) in undo log b) in the table c) in WAL d) in tempdb → **b**
2. InnoDB old row versions live: a) in the table b) in the undo log c) in WAL d) nowhere → **b**
3. `xmax` records: a) the XID that created the tuple b) the XID that deleted it c) the transaction's end time d) nothing → **b**
4. A ReadView in InnoDB is: a) a snapshot of active trx IDs b) a lock list c) an undo record d) a page → **a**
5. What reclaims Postgres dead versions? a) purge thread b) VACUUM c) undo log d) WAL replay → **b**
6. What reclaims InnoDB undo records? a) VACUUM b) purge thread c) fsync d) checkpoint → **b**
7. InnoDB REPEATABLE READ prevents phantoms via: a) snapshots only b) next-key locks c) timestamps d) SSI → **b**
8. Postgres READ COMMITTED snapshots are built: a) once per transaction b) per statement c) per commit d) never → **b**

## 20. Flashcards
- **Q: Where do Postgres store old versions?** → **A:** In the table (dead tuple versions) until VACUUM reclaims them.
- **Q: Where do InnoDB store old versions?** → **A:** In the undo log, reconstructed via `DB_ROLL_PTR`.
- **Q: What do xmin/xmax mean?** → **A:** XID that created / XID that deleted the tuple version.
- **Q: Postgres snapshot = ?** → **A:** In-flight XID list + horizon (`xmin`/`xmax`).
- **Q: What causes Postgres bloat?** → **A:** Dead tuple versions from UPDATEs, kept alive by long snapshots, until VACUUM.
- **Q: What is history list length?** → **A:** InnoDB's un-purged undo count; high = purge lag / long transactions.
- **Q: When does a SELECT lock in InnoDB?** → **A:** Only locking reads (`FOR UPDATE`, `LOCK IN SHARE MODE`) and DML; plain SELECTs are snapshot reads.
- **Q: Postgres vs InnoDB REPEATABLE READ?** → **A:** PG = pure SI (write skew possible); InnoDB = SI + next-key locks (phantom-safe writes).

## 21. Revision
Postgres MVCC: versions in-table (`xmin`/`xmax`, hint bits), snapshot = in-flight XIDs, VACUUM cleans dead tuples → bloat risk; READ COMMITTED per-statement snapshots, RR per-transaction, SERIALIZABLE = SSI. InnoDB MVCC: current value + `DB_TRX_ID`/`DB_ROLL_PTR` in clustered index, undo log reconstructs old versions, purge thread cleans; REPEATABLE READ adds next-key locks (phantom-safe, more insert blocking). Same theory, different storage trade-offs: PG = free old reads, bloat; InnoDB = lean index, undo+reconstruction. `SELECT FOR UPDATE` = locking read in both.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "How does Postgres implement MVCC?" | 2, 9, 13 |
| "How does InnoDB implement MVCC?" | 2, 9, 13 |
| "What are xmin/xmax?" | 2, 9, 13 |
| "Why is my table bloating?" | 9, 13, 14 |
| "What is history list length?" | 13, 14 |
| "Postgres vs MySQL REPEATABLE READ?" | 4, 13 |
| "What does SELECT FOR UPDATE do in MVCC?" | 13, 15 |
| "What is XID wraparound?" | 14 |
