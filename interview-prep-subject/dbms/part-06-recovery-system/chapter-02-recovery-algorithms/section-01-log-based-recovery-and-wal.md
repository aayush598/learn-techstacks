# Log-Based Recovery and WAL

> **TL;DR**: The database log is an append-only, ordered, checksummed record of every change — and the Write-Ahead Logging rule ("log before data, flush the log at commit") is what lets recovery redo committed work and undo uncommitted work after any crash.

## 1. Why Does This Exist?
A crash loses the buffer pool but not the disk — and the disk's pages may be torn, out of order, or missing the latest committed changes. To reconstruct a consistent state, the DBMS needs a **single ordered source of truth about what happened**: the log. Log-based recovery exists because (a) data pages alone can't tell you which transactions committed and in what order, (b) you can't force every page to disk at commit time (too slow), and (c) you can't trust the physical order of disk writes. The log solves all three: it records *logical* changes in a *deterministic sequence* with sequence numbers, and it's the only structure written in a strictly ordered, crash-tolerant way. **WAL** is the ordering discipline that makes the log trustworthy: the log record for a change is written (and at commit, flushed) *before* the data page is modified.

## 2. How Does It Work?
A log is a sequence of records; each record typically holds: transaction ID, operation type (`BEGIN`, `UPDATE`, `INSERT`, `DELETE`, `COMMIT`, `ABORT`, `CHECKPOINT`, `PAGE_IMAGE`), the data item/page affected, a **before-image** (old value — for undo) and **after-image** (new value — for redo), and a sequence number (LSN). The two WAL rules:
1. **Log first**: before a data page is written to disk, the log record describing that change must be on stable storage (in practice: in the log buffer and eventually flushed).
2. **Flush at commit**: a transaction is committed only after its `COMMIT` record is flushed to stable storage.
Recovery then: **redo** every transaction whose commit record is in the log (re-apply after-images), **undo** every transaction without a commit record (restore before-images), using the LSN order to apply changes exactly once. This is safe *only* because WAL guarantees the log is always ahead of the data.

## 3. When Is It Used?
- **Every commit** in every serious engine: Postgres appends to `pg_wal`; InnoDB appends to the redo log; SQL Server to the transaction log; MongoDB's WiredTiger to its journal.
- **Crash recovery on startup**: replay the log per WAL ordering.
- **Replication**: the log is shipped to replicas/standbys (streaming replication is literally WAL replay).
- **PITR (point-in-time recovery)**: archives of WAL enable replaying a backup up to any timestamp.
- **Rollback**: a transaction abort uses the same before-images the log recorded — the log serves undo for both crash and explicit rollback.

## 4. Why Wasn't Another Approach Chosen?
- *Force all dirty pages to disk at commit (no log)*: correct but horrifically slow — every commit writes every page it touched (random I/O, multi-page). The log lets you write *one small sequential record* at commit and defer page flushes.
- *Trust data pages' own contents*: pages can be torn and out of order; you can't reconstruct "which transactions committed" from pages alone.
- *Log only after-images (redo-only log)*: works for committed transactions but can't *undo* uncommitted ones (no before-image); uncommitted-but-flushed pages would corrupt the DB. You need before-images too (or undo from a separate mechanism).
- *Log only before-images (undo-only log)*: can roll back but can't *redo* committed-but-unflushed changes. Hence both images (or a combination) are needed.
- *Shadow paging (no log at all)*: copy-on-write pages + atomic pointer flip — avoids the log but pays double I/O, makes commit a full-page write, and complicates recovery of the shadow structure itself (Section 03). WAL/logging won on every axis that matters.
- *In-memory journals / redo-in-RAM*: some systems buffer the log in RAM and flush lazily — that's the `synchronous_commit=off` trade (bounded loss), not a replacement for logging.

## 5. Intuition
WAL is the **"receipt before the work"** rule. You never start remodeling a room until the contract (receipt) describing the work is signed and filed. At commit, the signed receipt must be *in the filing cabinet* (flushed) before you tell the client "done." After any disaster, you consult the receipts: anything with a signed "done" (commit record) gets *completed* (redo); anything without one gets *reversed* (undo). The receipts are numbered in order (LSN), so even if the workers scribbled over pages out of order, you can redo/undo in the exact sequence that actually happened. If you let workers paint *before* filing the receipt, a disaster leaves painted walls with no record — unrecoverable.

## 6. Real-World Analogy
A **chef's prep station with an order pad**. Every dish change is written on the order pad *before* the ingredient is touched (log-first). When the waiter confirms the order (commit), the pad page is *handed to the manager to file* (flush). A kitchen fire (crash) loses the countertop (RAM) but not the filed order pad (stable log). After the fire: any order with a filed "confirmed" slip gets re-made (redo); any order still in the pad without confirmation gets cancelled (undo). Because every line is numbered, the kitchen can rebuild the evening's real sequence exactly — even though the actual cooking (data pages) was interrupted at random moments.

## 7. Formal Definition
**Log record** (Silberschatz): ⟨Tᵢ, X, V₁, V₂⟩ — transaction Tᵢ updated data item X from before-image V₁ to after-image V₂; plus log records for start (⟨Tᵢ start⟩), commit (⟨Tᵢ commit⟩), and abort (⟨Tᵢ abort⟩), and checkpoints. Records are appended in order; each has an LSN.
**Write-Ahead Logging (WAL) rule**: the before-images of a data change must be recorded in the log on stable storage *before* the data page is written to disk, and the log must be flushed to stable storage at commit *before* the transaction is acknowledged as committed. Equivalently: the record describing a page modification is written to the log before the page is written out.
**Deferred vs immediate update**: with immediate update, pages are changed in the buffer pool as operations execute and undo uses before-images; with deferred update, pages are changed only at commit. WAL + immediate update (with before-images) is the modern standard.

## 8. Example
Transaction T (transfer 100): suppose initial `A=100, B=50`.
Log (in order):
1. `⟨T start⟩`
2. `⟨T, A, 100, 0⟩` (before=100, after=0) — update A
3. `⟨T, B, 50, 150⟩` (before=50, after=150) — update B
4. `⟨T commit⟩`

Case 1 — crash after record 2, before commit: data page A may show 0 (flushed) or 100 (not flushed). Recovery sees `⟨T start⟩` and no `⟨T commit⟩` → **undo**: set A back to 100 (before-image), release locks. B untouched. Result: consistent, T rolled back.
Case 2 — crash after record 4 (commit flushed): T is **committed** → **redo**: re-apply after-images (A=0, B=150) to any page that didn't reach disk. Result: T's effect is complete.

## 9. Internal Working
1. Each operation in the buffer pool first writes its log record to the **log buffer** (in shared memory) with the current LSN.
2. The page being modified records the LSN of the last log record that changed it (pageLSN).
3. At commit: the `COMMIT` record is appended; the log buffer is **flushed** to stable storage (fsync / group commit); then the transaction is acknowledged and (strict 2PL) releases locks.
4. Dirty pages (with pageLSN) are written to disk lazily — at checkpoints or under cache pressure — *always* after their log records are already durable (WAL rule).
5. On crash: recovery scans the log backward (undo) and/or forward (redo) from the last checkpoint, honoring each record's LSN; a page is redo'd only if its pageLSN < record's LSN (so changes are applied exactly once).
6. **Group commit**: several transactions' flushes are batched into one fsync; the flush covers all their commit records.

## 10. Time Complexity
- Log append: O(1) per record (in-memory) + amortized O(1) fsync at commit (group commit).
- Redo: O(log records from redo point) — bounded by checkpoint distance.
- Undo: O(undo records of failed transactions) — bounded by the history list.
- Log volume: grows with write workload; checkpoints bound replay; archival (PITR) needs retention policy.
- The per-commit fsync latency (~1-5 ms) is the fundamental throughput limiter → why group commit and weaker-sync modes exist.

## 11. Advantages
- **Only small sequential I/O at commit** — order-of-magnitude cheaper than flushing pages.
- **Ordered, deterministic** — LSNs let recovery apply changes exactly once regardless of physical page order.
- **One structure serves many jobs**: durability, atomicity, rollback, replication, PITR, and even index rebuild.
- **Works with lazy page writes** — the buffer pool can flush dirty pages anytime after their log records are safe.
- **Standardized across engines** — knowledge transfers directly to Postgres/InnoDB/SQL Server/MongoDB.

## 12. Disadvantages
- **Log is single-writer critical path** — log I/O can bottleneck high-TPS workloads (mitigated by group commit, partitioning, and fast NVMe).
- **Log volume/bloat** — heavy updates generate huge WAL; needs archiving/retention management.
- **fsync latency** — each commit pays device flush latency unless weakened (risking loss).
- **Recovery time** — replaying a long log is slow (mitigated by checkpoints, Section 02).
- **Complexity** — WAL correctness (order, flushing, torn-page handling) is subtle; bugs are catastrophic.

## 13. Interview Questions
1. **Q: What is a log record and what does it contain?** A: A record of one database change: transaction ID, operation type (start/update/insert/delete/commit/abort/checkpoint), the item/page affected, before-image and after-image, and an LSN (sequence number). Records are appended in order.
2. **Q: What is the WAL rule?** A: (1) Before a data page is written to disk, the log records describing its changes must already be on stable storage. (2) A commit is acknowledged only after the COMMIT record is flushed to stable storage. In short: **log before data, flush the log at commit**.
3. **Q: Why is "log before data" necessary?** A: If a data page reached disk before its log record, and the log record was then lost in the crash, recovery would either redo a change it doesn't know about (inconsistent redo) or fail to undo one it must. Ordering the log first guarantees the log is always a *superset* of what's on disk — so recovery can always reconstruct.
4. **Q: What is the difference between redo and undo in log terms?** A: Redo uses **after-images** to re-apply committed transactions that didn't reach disk; undo uses **before-images** to roll back uncommitted transactions that did. Redo reads the log forward; undo reads backward.
5. **Q: Why do you need both before and after images?** A: After-images enable redo of committed-but-unflushed work; before-images enable undo of uncommitted-but-flushed work. A crash can leave either situation, so both directions must be possible.
6. **Q: TRICKY: Can a transaction be "committed" but its data not on disk?** A: Yes, by design. The COMMIT record is flushed (durability), but data pages can still be in the buffer pool. Recovery redoes them from the log. "Committed" means "its log record is durable," not "its pages are on disk."
7. **Q: What is the purpose of the LSN (log sequence number)?** A: A monotonic number per log record, used to order records, tag pages (pageLSN = last log record affecting them), and bound recovery: a page is only redo'd if its pageLSN is older than the record's LSN — ensuring each change applies exactly once.
8. **Q: What is group commit?** A: Batching multiple transactions' log flushes into a single fsync so per-commit I/O is amortized; the batch is durable once the flush completes. This is how high-TPS systems keep commits fast despite fsync latency.
9. **Q: PR: What is the difference between `synchronous_commit=on` and `off`?** A: On: fsync the WAL before acknowledging commit (durable). Off: acknowledge without waiting for the flush (log survives in the buffer pool / OS cache until a later flush) — power loss can lose the most recent commits. It's a durability-vs-latency trade, not a correctness feature.
10. **Q: What happens during crash recovery in log terms?** A: From the last checkpoint, read the log forward to find committed transactions (redo them) and identify uncommitted ones (undo them), honoring LSN/pageLSN to avoid double-applying. Order: typically redo then undo (ARIES — Section 04).
11. **Q: Why is an append-only log better than random page writes for durability?** A: Appends are sequential (fast), naturally ordered, and atomic at the tail (a torn tail = "not committed"); random page writes have no ordering guarantee and can be torn mid-page. That's why the log is the durability vehicle.
12. **Q: TRICKY: What is a "torn log tail" and how is it handled?** A: If power is lost mid-append, the last log record may be partial. Each record is checksummed with its length; recovery ignores the incomplete tail (records before the last valid checksum are authoritative). That's why log records are self-describing.
13. **Q: What is the deferred-update variant of logging?** A: Changes are *not* applied to the buffer pool during execution — they're recorded in the log and applied only at commit. Simpler undo (nothing to undo mid-flight), but worse performance and not what modern engines do for general OLTP (Postgres/InnoDB use immediate update with before-images).
14. **Q: PR: How does WAL enable replication?** A: A standby reads the primary's WAL (streaming replication) and replays the records into its own buffer pool — same log, second copy. This is exactly the redo path, run continuously rather than at crash time. PITR is the same idea: replay archived WAL onto a restored backup.

## 14. Follow-Up Questions
1. **Q: When exactly must the data page be flushed relative to the log?** A: Never before its log records are durable (WAL rule). After that, anytime — checkpoints and buffer pressure decide. The pageLSN check at recovery enforces this.
2. **Q: What is the difference between WAL and the redo log in MySQL?** A: Terminology: MySQL's "redo log" IS the WAL for durability/crash recovery; InnoDB's *undo log* is a separate structure for rollback/MVCC. Postgres's WAL serves both redo and undo (undo via before-images / ARIES CLRs). Don't confuse the two "logs."
3. **Q: Why can't you just fsync the data page at commit instead of the log?** A: Because a commit typically touches *many* pages (scattered, random I/O, possibly torn) while the log is one small sequential record. Durability via the log is 10-100x cheaper.

## 15. Coding Example
```pseudocode
// Minimal WAL-correct commit
function commit(T):
    record = {type: COMMIT, txid: T.id, lsn: next_lsn()}
    log_buffer.append(record)
    fsync(wal_file)                      // WAL rule 2: flush before ack
    release_locks(T)                     // strict 2PL
    return OK

function crash_recovery(last_checkpoint):
    records = read_log_forward_from(last_checkpoint.lsn)
    committed = {r.txid for r in records if r.type == COMMIT}
    // redo
    for r in records:
        if r.type in (UPDATE,) and r.txid in committed:
            if page(r.item).pageLSN < r.lsn:     // apply exactly once
                write_page(r.item, r.after_image); page(r.item).pageLSN = r.lsn
    // undo
    for r in reverse(records):
        if r.type in (UPDATE,) and r.txid not in committed:
            if page(r.item).pageLSN == r.lsn:
                write_page(r.item, r.before_image)
```
```sql
-- Production visibility into the log
SHOW wal_level;            -- replica / logical (Postgres: how much is logged)
SHOW max_wal_size;         -- checkpoint trigger threshold
SELECT * FROM pg_stat_archiver;   -- WAL archiving status (PITR)
SHOW VARIABLES LIKE 'innodb_redo_log_capacity';  -- MySQL 8.0.30+
```

## 16. Industry Usage
- **PostgreSQL**: WAL in `pg_wal`; `wal_level`, `max_wal_size`, `checkpoint_timeout`, `archive_command`; `pg_waldump` to inspect records; streaming replication = WAL replay.
- **MySQL InnoDB**: redo log (recently `innodb_redo_log_capacity`), undo tablespaces; `innodb_flush_log_at_trx_commit`; doublewrite buffer.
- **SQL Server**: transaction log with LSNs, `CHECKPOINT`, log shipping, Always-On AG replication via the log.
- **Oracle**: redo + archive logs; `ALTER DATABASE ARCHIVELOG`; Data Guard ships redo.
- **MongoDB (WiredTiger)**: journal with WAL semantics; `writeConcern: majority` maps to a durability quorum.
- **RocksDB/LevelDB**: per-memtable WAL, `WriteOptions.sync`.
- **Kafka**: producer acks + log flushing — the same log-first pattern in a message queue.

## 17. References
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 17.4 (log-based recovery) & 17.5 (recovery with concurrent transactions).
- Elmasri & Navathe, Ch. 22.
- PostgreSQL docs, WAL: https://www.postgresql.org/docs/current/wal-intro.html
- MySQL 8.0 docs, InnoDB Redo Log: https://dev.mysql.com/doc/refman/8.0/en/innodb-redo-log.html
- Mohan et al., "ARIES: A Transaction Recovery Method..." (1992) — the canonical WAL+undo/redo reference.
- Stonebraker, "The End of an Architectural Era (It's Time for a Complete Rewrite)" (2007).

## 18. Cheat Sheet
- Log record: ⟨txid, item, before, after⟩ + type + LSN; append-only, checksummed.
- WAL rule 1: log record before data page reaches disk.
- WAL rule 2: COMMIT record flushed before acknowledging the commit.
- Redo = after-images, forward; Undo = before-images, backward.
- LSN = monotonic sequence; pageLSN prevents double-application.
- Group commit batches fsyncs; per-commit fsync is the throughput limiter.
- `synchronous_commit=off` = acknowledge without flush = bounded loss on power failure.
- Torn log tail = partial append; ignored via per-record checksums.
- WAL is also the vehicle for replication and PITR.

## 19. Quiz
1. WAL rule 1: a) data before log b) log before data c) flush at abort d) none → **b**
2. WAL rule 2: a) flush at start b) flush COMMIT before ack c) flush pages d) no flush → **b**
3. Redo uses: a) before-images b) after-images c) both d) neither → **b**
4. Undo uses: a) after-images b) before-images c) LSNs only d) nothing → **b**
5. The LSN's purpose: a) encryption b) ordering + once-only application c) speed d) security → **b**
6. Group commit: a) batches transactions b) batches fsyncs c) batches pages d) batches tables → **b**
7. A committed-but-unflushed transaction is: a) lost b) redone c) undone d) archived → **b**
8. A transaction with a start but no commit record is: a) redone b) committed c) undone d) kept → **c**

## 20. Flashcards
- **Q: What's in a log record?** → **A:** txid, type, item, before-image, after-image, LSN.
- **Q: WAL rules?** → **A:** Log before data; flush COMMIT before acknowledging.
- **Q: Redo vs undo?** → **A:** Redo = after-images (forward); undo = before-images (backward).
- **Q: What does the LSN do?** → **A:** Orders records and ensures each change applies exactly once (pageLSN comparison).
- **Q: What is group commit?** → **A:** Batching multiple commits' log flushes into one fsync.
- **Q: What does synchronous_commit=off sacrifice?** → **A:** Per-commit flush → recent commits can be lost on power failure.
- **Q: How does the log enable replication?** → **A:** Standby replays the primary's WAL — the redo path, continuously.
- **Q: What's a torn log tail?** → **A:** Partial final append; ignored via per-record checksums.

## 21. Revision
WAL: every change is logged (⟨txid, item, before, after, LSN⟩) *before* the data page touches disk, and the COMMIT record is flushed before the commit is acknowledged. Recovery = redo committed transactions (after-images, forward) + undo uncommitted (before-images, backward), using LSNs to apply each change exactly once. Group commit amortizes fsync; `synchronous_commit=off` trades durability for latency; torn tails handled by checksums. The log is the vehicle for durability, rollback, replication, and PITR — everything in Chapters 02-03.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a log record?" | 2, 7, 8 |
| "WAL rules and why log-first?" | 2, 4, 13 |
| "Redo vs undo?" | 7, 13 |
| "Why both before and after images?" | 7, 13 |
| "What does the LSN do?" | 9, 13 |
| "Group commit / fsync bottleneck?" | 9, 13 |
| "synchronous_commit=off?" | 13, 16 |
| "How does WAL do replication/PITR?" | 13, 16 |
