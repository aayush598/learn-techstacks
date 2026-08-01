# Types of Database Failures

> **TL;DR**: Database failures split into three classes — transaction (one transaction fails), system (the process/machine dies), and media (the disk dies) — and each class dictates a different recovery strategy: local rollback, log-based undo+redo, and backup-plus-log-replay.

## 1. Why Does This Exist?
"Recovery" is not one problem — it's three, with different causes, different data losses, and different costs to fix. A single transaction timing out and a hard disk dying have nothing in common except that both are "failures." A DBMS needs a precise taxonomy so it can (a) choose the right recovery mechanism at runtime, (b) allocate the right resources (log for transaction/system failures; backup archive for media failures), and (c) guarantee the correct ACID outcome after each class. Without the taxonomy, you'd either under-protect (lose committed data after a media failure) or over-pay (replay the whole backup for a single rolled-back transaction).

## 2. How Does It Work?
Three classes, plus the strategy each triggers:
1. **Transaction failure** — the transaction cannot complete (logical error, deadlock victim, constraint violation, app abort). Recovery = **undo** its effects (or, for MVCC, discard its versions), release locks; the DBMS remains up.
2. **System failure** (crash/power loss/OS panic) — volatile memory (buffer pool, caches) is lost; disk survives intact, but data pages may be *partially written* and the buffer pool's unflushed committed changes are gone. Recovery = **redo** committed transactions whose pages didn't reach disk + **undo** uncommitted transactions whose changes did reach disk. Achieved by replaying the WAL log (ARIES, Chapter 02).
3. **Media failure** (disk head crash, corruption, accidental deletion) — the data file itself is gone or corrupted. Recovery = **restore the last backup** + **replay the log** from the backup point (PITR), or failover to a replica.

## 3. When Is It Used?
- **Transaction failures**: every rollback, every deadlock-victim abort, every failed constraint — constantly, in normal operation.
- **System failures**: any crash — an outage, `kill -9`, power loss, OOM-killed postgres, a datacenter blip. Every restart runs crash recovery.
- **Media failures**: rare but catastrophic — disk replacement, EBS failure, corruption detected by checksums, `rm` of a data file. Requires a backup strategy that existed *before* the failure (Part 06 Chapter 03).
- Also relevant: the failure *detection* machinery — crash detection (heartbeats, watchdog), torn-page detection (checksums), and automated failover in replicas.

## 4. Why Wasn't Another Approach Chosen?
- *Treat every failure as a full restart from backup*: obviously wasteful — a deadlock victim shouldn't replay a terabyte backup. Recovery must be proportional: transaction failures need only local rollback; system failures need log replay; only media failures justify full restore.
- *Treat every failure as just "rollback"*: would silently *lose committed work* after a crash — the cardinal sin. Committed transactions must be *redone*, not rolled back. Hence undo alone is insufficient.
- *Treat every failure as just "redo"*: would resurrect *uncommitted* transactions after a crash — violating atomicity. Hence both undo and redo are needed.
- *Ignore failures entirely (no recovery)*: MyISAM-style — no rollback, no crash safety; tables get corrupted and manual repair is needed. Rejected by every serious engine because committed-data loss and corruption are unacceptable for production.
- *In-memory / NoSQL "durability-free" stores*: some systems consciously trade durability for speed (memcached) or accept bounded loss (Redis AOF with `always`/`everysec`); that's a *product decision*, not an alternative recovery algorithm — and even they add journaling when durability matters.

## 5. Intuition
Think of the database as a **legal archive with three disaster scenarios**: (1) a *single clerk* (transaction) realizes they made an arithmetic mistake — you just strike out their one entry (rollback); (2) the *whole office* loses power and the janitor (recovery) must re-copy the day's work from the logbook (redo) and erase the half-finished entries (undo); (3) the *archive itself* burns down — you must rebuild from the off-site safety copy (backup) and then re-enter everything recorded since the copy was made (log replay). Each disaster needs its own playbook, and the playbooks differ in *scope* (one entry vs the whole log) and *direction* (undo vs redo vs rebuild).

## 6. Real-World Analogy
A **checkbook**: Transaction failure = you tear out one bad check and void it (rollback). System failure = the bank's ledger computer crashes at night; in the morning the bank re-applies every transaction that was logged but not yet posted (redo) and discards transactions that never completed (undo) — the log is the source of truth, not the ledger. Media failure = the bank building floods; the bank restores the last backup from the vault (backup) and replays every check image scanned since then (log replay). Same bank, three very different recovery plans.

## 7. Formal Definition
- **Transaction failure**: a transaction is unable to proceed or chooses to abort — caused by logical errors (division by zero, constraint violation), concurrency issues (deadlock victim), or explicit `ROLLBACK`. Recovery requirement: undo the transaction's partial effects; other transactions unaffected; the DBMS continues running.
- **System failure**: the computer system crashes (OS failure, power loss) while transactions are in flight; volatile storage is lost, non-volatile storage survives (though pages may be torn or written out of order). Recovery requirement: redo all committed transactions (whose effects may not have reached disk) and undo all uncommitted transactions (whose effects may have reached disk), restoring a consistent state that respects every commit.
- **Media failure**: a portion of the non-volatile storage (data files, log files, or both) is damaged or lost. Recovery requirement: restore from backup and replay the log (or failover to a replica), losing at most the data between the last backup and the failure (bounded by `wal_keep_size`/`archive_command` design).

## 8. Example
**Transaction failure**: T7 does `UPDATE accounts SET balance=balance-500` but also violates a `CHECK (balance >= 0)`. The DBMS aborts T7: undo its update, release its locks, return an error to the app. Other transactions keep running; the DBMS stays up. (Everyday occurrence.)
**System failure**: at 14:00, T8 committed (commit record flushed to WAL), but its data page is still in the buffer pool. T9 is active (no commit record). Power dies. On restart: recovery reads the WAL, **redoes** T8's changes (they weren't on disk), and **undoes** T9's changes (T9 never committed). Result: exactly as if T8 had completed and T9 never ran.
**Media failure**: the `accounts` data file is corrupted (bad sector). Ops restores last night's full backup (state at 02:00) and replays the WAL from 02:00 onward — re-applying every committed transaction since the backup (PITR). Data is restored to the last committed point the log knows.

## 9. Internal Working
1. **Detection**: the DBMS or operator notices the failure class — transaction abort (in-process), system crash (next startup runs crash recovery), media failure (checksum mismatch on read, I/O error, or hardware alert).
2. **Transaction failure path**: the abort handler walks the transaction's undo records (or its MVCC version list), restores before-images, releases locks, and reports.
3. **System failure path (crash recovery)**: startup runs the recovery algorithm (Chapter 02): read the last checkpoint → scan the WAL → redo committed changes (via LSNs) → undo uncommitted ones → bring the DB to a consistent, crash-consistent state → open for business.
4. **Media failure path**: halt affected reads/writes → restore backup (full + incremental) → replay archived WAL → verify checksums → resume; often implemented via failover to a synchronous replica to minimize downtime.
5. The failure taxonomy also drives **operational decisions**: log location, backup frequency, archive retention, and replica count are chosen per the mix of risks a deployment cares about.

## 10. Time Complexity
- Transaction failure: O(undo work of that transaction) — proportional to its writes.
- System failure: O(log records since last checkpoint) for redo + O(undo work) — the checkpoint bounds it (Chapter 02).
- Media failure: O(backup size) + O(log volume since backup) — the *worst* and slowest recovery class, hence the emphasis on backups and replicas.
- Detecting corruption (checksums): O(page size) per page read.

## 11. Advantages
- **Proportional response**: each failure class gets a recovery mechanism sized to it — cheap for common cases, expensive only for rare ones.
- **Correct ACID outcomes**: committed work survives crashes (redo), uncommitted work never does (undo), and media loss is bounded by backup design.
- **Clean engineering separation**: the taxonomy maps cleanly to code (abort handler, crash recovery, restore pipeline) and to ops (backup/DR policy).

## 12. Disadvantages
- **The taxonomy assumes disk survives system crashes** — true for real failures, but "torn pages" (partially written pages) still need checksums and careful handling (WAL + full-page images).
- **Media failure recovery depends on pre-existing backups** — if you skipped backups, no algorithm saves you.
- **Replication doesn't replace recovery**: replicas are only as good as their lag; and failover itself can expose torn/unapplied state.
- **Failure detection is imperfect**: an undetected corrupted page can silently propagate (hence checksums + periodic validation like `pg_checksums`/`amcheck`).

## 13. Interview Questions
1. **Q: What are the three classes of database failures?** A: Transaction failure (one transaction aborts — logical error, deadlock, constraint), system failure (process/machine crash — RAM lost, disk intact), media failure (disk/storage lost or corrupted). Each needs a different recovery: rollback, log-based undo+redo, backup+log replay.
2. **Q: Why can't a single algorithm handle all three?** A: Because the failure's *scope* and *data loss* differ. A transaction failure must not disturb other transactions; a system failure requires replaying the log to recover committed work; a media failure requires data restoration. One size would either over-do (replay backups for every rollback) or under-do (lose committed work).
3. **Q: What does crash recovery do after a system failure?** A: Redo committed transactions whose effects never reached disk (their commit records are in the log), and undo uncommitted transactions whose effects did reach disk (they never committed). The log is the source of truth — data pages alone are not trustworthy.
4. **Q: What data survives a system crash?** A: Whatever is on non-volatile storage — committed log records (if flushed) and data pages that happened to be written out (possibly out of order or torn). Volatile state (buffer pool, caches, unflushed log) is lost.
5. **Q: TRICKY: Can a system failure cause loss of committed data?** A: Only if the commit record itself wasn't durably flushed — which is exactly what `synchronous_commit`/`innodb_flush_log_at_trx_commit` control. With proper flushing, no: committed transactions are redone from the log after crash. Weakening the flush weakens this guarantee (bounded loss of the most recent commits).
6. **Q: What is a media failure and how is it different from a system failure?** A: Media failure damages the *storage* (disk death, corruption); system failure only loses volatile memory. Recovery differs: media needs backup + log replay (or replica failover); system needs log replay only. A system crash doesn't corrupt your backup; a media failure may.
7. **Q: What is a torn page?** A: A page half-written to disk (e.g., 16KB page written in 512-byte sectors, power lost mid-write) — the disk has neither the old nor the new content. Without checksums and full-page images (or double-write buffers), replaying the log over a torn page can corrupt the DB.
8. **Q: PR: How do you detect a torn page / corruption?** A: Page-level checksums (Postgres `data_checksums`, InnoDB checksums) validate on read; `pg_checksums` and `amcheck` validate the heap/index; replication/backup health checks catch silent corruption early.
9. **Q: Why doesn't an OS `write()` guarantee durability?** A: `write()` copies into the OS page cache; the data can sit there and be lost on power failure. `fsync()` forces the cache out to disk and returns only when the data is durable. This is the crux of "log before data, fsync the log."
10. **Q: What is the difference between transaction and system failure handling?** A: Transaction failure = *undo only* (other transactions unaffected, DBMS stays up). System failure = *redo + undo* (replay the log). Transaction failure never requires redo because nothing committed-and-not-flushed happened; system failure always considers both.
11. **Q: TRICKY: If a transaction's changes all reached disk but it never committed, what happens on crash?** A: It is **undone** — recovery sees no commit record and rolls back its effects. This is atomicity in action: uncommitted work is never visible, even if it physically hit disk.
12. **Q: What recovery does a deadlock victim require?** A: Transaction-level rollback (undo its partial work, release locks) — no log replay, no backup. The app typically retries. This is the *most common* failure class in production.
13. **Q: PRODUCTION: How does a checksum failure during read behave?** A: The page read fails with an error (Postgres logs "invalid page" and may mark the relation corrupted); reads on that block fail until repaired. Monitoring + backups + `amcheck` are how you find and fix it before it propagates.
14. **Q: What does "crash-consistent" mean?** A: After recovery, the database reflects exactly the set of committed transactions — no committed transaction is lost (subject to flush settings) and no uncommitted transaction's effects remain. "Consistent" here is a transaction-level property, not a page-level one (pages can be torn mid-recovery; the log fixes it).
15. **Q: TRICKY: Why can't you just write data pages to disk before commit?** A: Because pages can be written *out of order* (page 5 before page 3) and *torn*, and the commit might then reference data not yet written — you'd need to know exactly which pages belong to the commit. The log solves this by recording *logical* changes with sequence numbers, so redo/undo don't depend on physical page order.

## 14. Follow-Up Questions
1. **Q: Which failure class does a replica failover belong to?** A: It's a system-failure (or media-failure) *response*: the standby takes over via its own WAL replay — effectively recovery done continuously, before the failure.
2. **Q: How does backup/recovery relate to the taxonomy?** A: Backups exist for the *media* class; but PITR (replaying WAL after a backup) is also used for *logical* disasters (accidental `DROP TABLE`) and for system-crash testing.
3. **Q: What's the difference between a physical and logical backup for media recovery?** A: Physical (copy of data files + WAL) restores byte-exact and replays WAL fast; logical (`pg_dump`) restores schema/data but requires re-applying changes via SQL — slower, no WAL replay. Physical backups are the standard for PITR.

## 15. Coding Example
```sql
-- Check the durability/fsync settings that define your failure profile
SHOW synchronous_commit;                        -- on | remote_write | remote_apply | off
SHOW fsync;                                     -- on
SHOW wal_sync_method;                           -- fdatasync | fsync | ... (Postgres)
SHOW VARIABLES LIKE 'innodb_flush_log_at_trx_commit';  -- 1 (durable) | 0 | 2 (bounded loss)
```
```pseudocode
// Crash recovery dispatch by failure class (conceptual)
on_failure(failure):
    if failure is TransactionFailure(t):        // e.g., deadlock, constraint
        undo(t); release_locks(t); report_error(t)
    elif failure is SystemFailure:              // crash/power loss
        cp = load_last_checkpoint()
        log_records = read_wal_from(cp.lsn)
        redo_committed(log_records)             // committed, not on disk
        undo_uncommitted(log_records)           // uncommitted, reached disk
        open_for_business()
    elif failure is MediaFailure(segment):
        restore_last_backup()
        replay_archive_wal(until = last_committed_lsn)
        verify_checksums()
```
```bash
# Detect corruption (media class) in Postgres
pg_checksums -c $PGDATA             # verify page checksums across the cluster
psql -c "SELECT * FROM amcheck..."  # or run amcheckbtree() for index validation
```

## 16. Industry Usage
- **PostgreSQL**: crash recovery on startup reads the last checkpoint, replays `pg_wal`, undoes with the startup process; `synchronous_commit` levels; checksums optional (`initdb -k`).
- **MySQL InnoDB**: redo log (`ib_logfile0/1` or `#innodb_redo`), undo tablespaces; crash recovery replays redo and uses undo for rollback; `innodb_flush_log_at_trx_commit=1` default for durability.
- **MongoDB**: WiredTiger journal (WAL) + checkpoints; `writeConcern: majority` maps to "flush log at commit."
- **RocksDB / LSM stores**: WAL per memtable; recovery replays WAL and rebuilds memtables. Kafka's `log.flush.interval` is the same durability dial.
- **CockroachDB/TiDB**: WAL/Raft log replay across replicas — recovery extended to a distributed system (Chapter 03).

## 17. References
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 17.1 (failure classification).
- Elmasri & Navathe, Ch. 22.
- PostgreSQL docs, "Reliability": https://www.postgresql.org/docs/current/wal-reliability.html
- MySQL 8.0 docs, InnoDB Redo Log / crash recovery: https://dev.mysql.com/doc/refman/8.0/en/innodb-redo-log.html
- Mohan et al., "ARIES: A Transaction Recovery Method..." (1992) — the systematic treatment of undo+redo.
- O'Neil, "Recovery" in *Principles of Database Systems* texts.

## 18. Cheat Sheet
- 3 failure classes: transaction (undo), system (redo+undo via log), media (backup+log replay).
- Committed ⇒ must survive (redo); uncommitted ⇒ must vanish (undo).
- The log, not the data pages, is the source of truth after a crash.
- OS page cache + missing fsync = lost "writes" = why durability needs log flushing.
- Torn pages need checksums + full-page images.
- Deadlock victims are transaction failures (most common class).
- Crash recovery = read checkpoint → redo committed → undo uncommitted → serve.
- Backups only matter if they existed before the media failure.

## 19. Quiz
1. A deadlock victim abort is a: a) system failure b) transaction failure c) media failure d) none → **b**
2. A power outage is a: a) transaction failure b) media failure c) system failure d) logical error → **c**
3. A disk with a bad sector is a: a) system failure b) transaction failure c) media failure d) crash → **c**
4. Committed-but-unflushed transactions on crash are: a) undone b) redone c) ignored d) deleted → **b**
5. Uncommitted transactions whose pages reached disk are: a) redone b) undone c) committed d) restored → **b**
6. Which failure class needs a backup? a) transaction b) system c) media d) none → **c**
7. `fsync()` guarantees: a) data in cache b) data on disk c) data committed d) nothing → **b**
8. A torn page is: a) a deleted row b) a half-written page c) a corrupted index d) a bad LSN → **b**

## 20. Flashcards
- **Q: Name the 3 failure classes and their recovery.** → **A:** Transaction→undo; System→redo+undo (log); Media→backup+log replay.
- **Q: What is redone after a crash?** → **A:** Committed transactions whose pages didn't reach disk.
- **Q: What is undone after a crash?** → **A:** Uncommitted transactions whose changes reached disk.
- **Q: Why does a write() not guarantee durability?** → **A:** OS page cache — need fsync to force to disk.
- **Q: What is a torn page?** → **A:** A page half-written to disk; needs checksums + full-page images.
- **Q: Which failure class is most common?** → **A:** Transaction failures (aborts, deadlocks) — constant in production.
- **Q: What is the source of truth during recovery?** → **A:** The WAL log, not the data pages.
- **Q: Media failure recovery = ?** → **A:** Restore backup + replay WAL (PITR) or failover to replica.

## 21. Revision
Three failure classes: transaction (undo only), system (redo committed + undo uncommitted from the log), media (backup + log replay / failover). The log is the source of truth; `fsync` of the commit record is the durability line; OS caching and torn pages are why "write to disk" isn't enough. Crash recovery = load checkpoint → scan log → redo → undo → serve. This taxonomy drives Chapter 02 (algorithms) and Chapter 03 (Postgres/backup practice).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Classify database failures." | 1, 2, 7 |
| "What happens to committed/uncommitted after crash?" | 2, 9, 13 |
| "Why is write() not durable?" | 9, 13 |
| "What is a torn page?" | 9, 13 |
| "Transaction vs system failure?" | 13, 14 |
| "Why can't pages be written before commit?" | 13 |
| "How do you detect corruption?" | 9, 13 |
| "Media failure recovery?" | 2, 8, 13 |
