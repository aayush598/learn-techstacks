# Checkpointing

> **TL;DR**: A checkpoint records "what's already on disk" so crash recovery doesn't replay the whole log — and fuzzy (non-quiescent) checkpoints take that snapshot *without stopping the database*.

## 1. Why Does This Exist?
After days of uptime, the WAL contains records for every change ever made — replaying all of it at recovery would take hours. Checkpointing exists to *bound recovery time*: periodically, the DBMS records which data pages have been flushed to disk and where the log "began" for recovery purposes, so crash recovery only replays the log *after* that point. Without checkpoints, recovery cost grows without bound; with them, recovery cost is proportional to the checkpoint interval's log volume. Checkpoints also free WAL space (segments before the checkpoint can be archived/removed) and are the hook for PITR and for `VACUUM`/statistics maintenance in Postgres.

## 2. How Does It Work?
Two flavors:
- **Consistent (quiescent) checkpoint**: stop all transactions, flush *every* dirty page, record "the database is fully on disk at LSN L," resume. Simple and fully consistent, but the database must pause — costly for 24/7 OLTP.
- **Fuzzy (non-quiescent) checkpoint** (used in practice): the database keeps running. The DBMS (1) records a checkpoint begin with the current LSN (the *redo point* / checkpoint LSN), (2) asynchronously flushes dirty pages whose `pageLSN < checkpoint LSN` (a snapshot of dirtiness taken at begin), (3) records the checkpoint end record with the list of *still-dirty* pages (the dirty page table / `FPI` list). Recovery starts from the checkpoint LSN and only handles pages/records after it. Because pages are flushed concurrently, the checkpoint end record is authoritative about what remained dirty.

## 3. When Is It Used?
- Postgres: `CHECKPOINT` command; automatic checkpoints driven by `checkpoint_timeout` (default 5 min) and `max_wal_size` (WAL volume trigger). `VACUUM` interacts: it can force checkpoints (Postgres docs recommend increasing `max_wal_size` before big vacuum).
- MySQL InnoDB: background checkpoints (`innodb_max_dirty_pages_pct` triggers flushing); `innodb_log_file_size`/`innodb_redo_log_capacity` sizing.
- SQL Server: automatic checkpoints (recovery interval target); `CHECKPOINT` manual.
- MongoDB (WiredTiger): checkpoints every 60s by default.
- Everywhere recovery-time matters: you trade a periodic burst of I/O (flush cost) for a bounded crash-recovery window.

## 4. Why Wasn't Another Approach Chosen?
- *No checkpoints*: recovery replays the whole log — unbounded, and log space can't be recycled. Unacceptable for production uptime.
- *Consistent checkpoints only*: correctness is trivially provable (the DB is fully consistent on disk), but the stop-the-world pause is brutal under load; fuzzy checkpoints give the same recovery bound without stopping work — a strictly better engineering trade, hence production uses them.
- *Checkpoint the whole database every time*: unnecessary — only *dirty* pages and the log position need recording; the dirty-page table is the minimal bookkeeping.
- *Checkpoint via replication to a mirror*: that's a different mechanism (standby); the checkpoint is the *local* cost-control, replication is the *remote* copy. Both are needed.
- *Recovery-time guarantees via more-frequent fsync instead*: forcing every page at commit kills throughput; checkpoints defer page flushes and bound replay instead — the right division of labor.

## 5. Intuition
A checkpoint is like **a tax accountant's "books balanced as of Dec 31" line**. At year end, you record "everything up to this date is fully posted (on disk) and the books agree" (checkpoint begin). During the year, transactions keep happening (fuzzy), so at the end you also list which accounts are still partially worked (dirty-page list). If the office burns mid-year, you only have to reconstruct from Jan 1 (the checkpoint), not from the company's founding. The checkpoint isn't a copy of the whole business — just a marker of "as of this log position, these pages are safe."

## 6. Real-World Analogy
**A lifeguard's rotation log at a pool**. At every shift change the guard writes "as of 2:00pm, here's what's done" (checkpoint) and notes which tasks are still unfinished (dirty list). If the pool's logbook is needed later, you only reconstruct from the last shift change, not from the pool's opening day. A *quiescent* checkpoint would mean closing the pool for a full audit each shift — safe but nobody swims; a *fuzzy* checkpoint lets swimmers keep going while the off-duty guard quietly catches up on paperwork.

## 7. Formal Definition
A **checkpoint** is a special log record (or pair of records) that records the log position `L` (the **checkpoint LSN / redo point**) at which the state of the database is known to be recoverable without scanning records before `L`. In a **consistent checkpoint**, at time `L` every transaction is complete and every dirty page has been flushed — the database on disk is a valid, complete state. In a **fuzzy checkpoint**, transaction activity continues; the checkpoint records `L`, and a **dirty page table (DPT)** snapshot listing pages with `pageLSN ≥ L` that were still dirty at checkpoint begin (plus their LSNs), and writes a **checkpoint end** record once those pages are flushed; recovery replays the log starting at `L` and uses the DPT to know which pages might need redo. Postgres additionally writes a **full-page image (FPI)** for each dirty page at checkpoint time so redo never needs an older image.

## 8. Example
Postgres at startup/flush:
- `max_wal_size = 1GB`, `checkpoint_timeout = 5min`.
- At 10:00 the autovacuum/checkpointer starts a checkpoint: records checkpoint begin at LSN `0/3000000`. Dirty pages: P1 (pageLSN 0/2E00000), P2 (0/2F00000), P7 (0/2A00000) — all `< 0/3000000`.
- The checkpointer flushes P7, P1, P2 to disk (asynchronously; new transactions keep writing).
- At 10:00:01 it writes checkpoint end (DPT empty — all flushed) at `0/3000002` and can recycle WAL segments before `0/3000000`.
- Crash at 10:00:02. Recovery reads the last checkpoint end (LSN `0/3000002`), replays the log from `0/3000000` forward (only ~2 minutes of records — not days), undoes uncommitted transactions.
Without the checkpoint, recovery would scan from the first WAL segment (possibly GBs).

## 9. Internal Working
1. **Trigger**: elapsed `checkpoint_timeout`, WAL volume ≥ `max_wal_size`, explicit `CHECKPOINT`, or (Postgres) certain operations (e.g., after `CREATE DATABASE`).
2. **Begin**: write a `CHECKPOINT` log record with the current LSN — the redo point. Take a snapshot of the dirty page table.
3. **Flush**: write dirty pages with `pageLSN < redo point` to disk (in batches, respecting `checkpoint_completion_target` — spread the burst over a fraction of the interval to smooth I/O).
4. **End**: write the checkpoint end record (including any pages still dirty from concurrent activity that must survive in the DPT). Update the control file (`pg_control`) with the checkpoint LSN — used at recovery to locate it.
5. **Post-checkpoint**: WAL segments older than the redo point can be recycled (archived/deleted); the DPT carries forward only pages dirtied after the redo point.
6. **Recovery use**: find the checkpoint via `pg_control`, start replay from its redo point, honor pageLSN checks, and — because of full-page images at checkpoint — never need pre-checkpoint pages for redo.

## 10. Time Complexity
- Checkpoint work: O(#dirty pages) flush + O(DPT) bookkeeping. Amortized over the interval: the flush burst is spread via `checkpoint_completion_target`.
- Recovery time: O(log records after redo point) + O(undo work). **Checkpoint frequency directly trades I/O burst for recovery time.**
- WAL space: recycling happens at checkpoint boundaries; `max_wal_size` bounds segments between checkpoints.
- Postgres `checkpoint_timeout` default 5 min → typical recovery is seconds to a couple minutes for normal workloads.

## 11. Advantages
- **Bounds recovery time** — recovery replays only post-checkpoint log.
- **Recycles WAL space** — pre-checkpoint segments can be archived/removed.
- **Fuzzy checkpoints don't stop the database** — 24/7 availability preserved.
- **Full-page images at checkpoint** make redo robust against torn/missing earlier pages.
- **Tunable**: frequency controls the I/O-vs-recovery trade per workload.

## 12. Disadvantages
- **Periodic I/O bursts** — checkpoint flushes can cause latency spikes under load (mitigated by `checkpoint_completion_target`).
- **Checkpointing costs CPU/IO** — too-frequent checkpoints waste throughput; too-rare ones blow up recovery time and WAL usage.
- **Interaction surprises** — big `VACUUM` or mass DDL can force a checkpoint mid-workload, causing stalls.
- **Recovery still O(log volume)** — an enormous `max_wal_size` still means a long replay; crash-recovery time isn't instantaneous.
- **Postgres-specific quirks** — checkpoints also interact with `full_page_writes` and archiving; misconfig can cause WAL bloat or slow crash recovery.

## 13. Interview Questions
1. **Q: What is a checkpoint and why is it needed?** A: A mechanism that records "as of log position L, pages up to this point are (mostly) on disk" — bounding crash recovery to the log *after* L instead of replaying the entire WAL. It also lets WAL segments be recycled.
2. **Q: What's the difference between a consistent and a fuzzy checkpoint?** A: A consistent checkpoint requires stopping all transactions and flushing every dirty page — the on-disk state is fully valid. A fuzzy checkpoint lets transactions continue; it records the redo point + a dirty-page list and flushes asynchronously. Production uses fuzzy.
3. **Q: What is the redo point (checkpoint LSN)?** A: The log position from which recovery must start replaying. Anything before it is guaranteed safe (pages flushed, or covered by full-page images); recovery ignores earlier records.
4. **Q: How does a fuzzy checkpoint stay correct if pages are flushed mid-transaction?** A: Because the checkpoint records (a) the redo point, (b) the dirty-page table snapshot at begin, and (c) a checkpoint-end record after flushing. Recovery replays from the redo point using pageLSN checks, and full-page images cover any page that was dirty at checkpoint begin — so concurrent activity is harmless.
5. **Q: What is the dirty page table (DPT)?** A: The set of pages that have been modified in the buffer pool but not yet flushed, with each page's LSN. Used by checkpoints (what to flush) and by recovery (which pages might need redo). In Postgres this is the `dirty_page` state tracked by the buffer manager; ARIES formalizes it.
6. **Q: TRICKY: Why is a checkpoint not a backup?** A: It's a *marker + flush*, not a *copy*. A backup captures data to be restored later (media failure); a checkpoint just advances the "safe to stop replaying here" line for *crash* recovery and frees WAL. Backups (Chapter 03) use WAL archiving, not checkpoints.
7. **Q: How do `checkpoint_timeout` and `max_wal_size` interact?** A: A checkpoint triggers when either the time elapsed since the last checkpoint reaches `checkpoint_timeout` (default 5 min) OR WAL written since then exceeds `max_wal_size` (default 1GB) — whichever comes first. Lower values = more frequent, smaller-burst checkpoints = faster recovery but more I/O overhead.
8. **Q: What is `checkpoint_completion_target`?** A: The fraction of the checkpoint interval over which the checkpointer spreads its flush burst (default 0.5). Higher = smoother I/O but risk of overlapping the next interval; it's how you tune away checkpoint latency spikes.
9. **Q: PR: Why did my query slow down right after a checkpoint?** A: Checkpoint flushing competes for I/O bandwidth (the burst), and if the buffer pool was large and dirty, the flush storm can stall normal traffic. Fixes: raise `checkpoint_completion_target`, tune `max_wal_size`/`checkpoint_timeout`, ensure enough I/O capacity.
10. **Q: What does a checkpoint have to do with full-page writes?** A: Immediately after a checkpoint, the next modification of each page must write the whole page to the log (`full_page_writes`) — because redo starting from the checkpoint might need to apply an incremental change to a page that was only partially flushed or torn at the checkpoint. So checkpoints and full-page writes are coupled.
11. **Q: TRICKY: What happens to WAL files before the last checkpoint?** A: They're eligible for recycling (deletion or archiving). Postgres recycles segments for reuse (avoids reallocating); with archiving on, they're shipped to the archive *first* (needed for PITR). You must not delete un-archived WAL.
12. **Q: How does recovery find the checkpoint?** A: The control file (`pg_control`) stores the location of the last valid checkpoint record (and a backup copy). Recovery reads it, validates, then replays from that redo point. If the primary control file is corrupted, the backup checkpoint is used.
13. **Q: PRODUCTION: Why would you lower or raise `max_wal_size`?** A: Lower → more frequent checkpoints, faster recovery, but more I/O bursts. Raise → longer intervals, bigger WAL, longer recovery. Choose based on your recovery-time SLA and I/O headroom — and raise it before large `VACUUM`/DDL operations that generate lots of WAL.
14. **Q: What is the difference between a checkpoint and `VACUUM`?** A: A checkpoint flushes dirty *pages* and advances the recovery point (I/O). `VACUUM` reclaims *dead tuple space* and updates visibility (also does some flushing/`UPDATE`-like work but is a different subsystem). They interact: vacuum generates WAL, which can trigger checkpoints.

## 14. Follow-Up Questions
1. **Q: What is `pg_control` and why does Postgres keep two copies?** A: The control file stores checkpoint locations, WAL settings, and system ID; two copies (primary + backup) guard against corruption during update — if one is bad, recovery uses the other.
2. **Q: What is the relationship between checkpoints and PITR?** A: PITR restores a base backup (a consistent snapshot taken with `pg_basebackup`) then replays *archived* WAL from that point. Checkpoints determine when base backups and WAL archives align, but PITR's replay isn't bounded by the checkpoint — it's bounded by the archive's retention.
3. **Q: What's "crash recovery" vs "archive recovery"?** A: Crash recovery replays the *local* WAL from the last checkpoint to bring the cluster up (seconds-minutes). Archive recovery restores a base backup + replays *archived* WAL to a target time — used for PITR, replicas, or after media failure (longer, deliberate).

## 15. Coding Example
```sql
-- Postgres: checkpoint control
SHOW checkpoint_timeout;              -- 5min
SHOW max_wal_size;                    -- 1GB
SHOW checkpoint_completion_target;    -- 0.5
CHECKPOINT;                           -- force one now (waits for completion)
SELECT checkpoints_timed, checkpoints_req, checkpoint_write_time, checkpoint_sync_time
  FROM pg_stat_bgwriter;              -- historical checkpoint stats
```
```bash
# Observe WAL recycling after a checkpoint
ls $PGDATA/pg_wal/ | head
# Control file inspection
pg_controldata $PGDATA | grep -i checkpoint
```
```pseudocode
// Fuzzy checkpoint algorithm (conceptual)
function fuzzy_checkpoint():
    redo_point = current_lsn()
    dpt = snapshot_dirty_page_table()          // pages dirty at this instant
    append_log_record(CHECKPOINT_BEGIN, redo_point)
    for page in dpt (batched, throttled):      // spread flush over completion_target
        if page.pageLSN < redo_point:
            flush(page)
    append_log_record(CHECKPOINT_END, still_dirty_pages())
    update_control_file(redo_point)
```

## 16. Industry Usage
- **PostgreSQL**: `CHECKPOINT`, autocheckpoint by `checkpoint_timeout`/`max_wal_size`, `checkpoint_completion_target`, `pg_control`, `pg_stat_bgwriter`. Recovery uses the control-file checkpoint to start replay.
- **MySQL InnoDB**: background flushes driven by `innodb_max_dirty_pages_pct_lwm`/`innodb_max_dirty_pages_pct`, adaptive flushing; checkpoint LSN in the redo log; `innodb_redo_log_capacity` sizing bounds recovery.
- **SQL Server**: automatic checkpoint targeting a recovery interval; `CHECKPOINT` manual; periodic checkpoint = "flush + mark in log."
- **MongoDB (WiredTiger)**: checkpoints every 60s; recovery replays the journal from the last checkpoint.
- **RocksDB**: memtable flush + `Flush`/compaction checkpoints; WAL is discarded once a memtable is flushed (analogous checkpointing).

## 17. References
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 17.5 (recovery with checkpoints).
- Elmasri & Navathe, Ch. 22.
- PostgreSQL docs, "WAL Configuration": https://www.postgresql.org/docs/current/wal-configuration.html
- PostgreSQL docs, `CHECKPOINT`: https://www.postgresql.org/docs/current/sql-checkpoint.html and `pg_controldata`: https://www.postgresql.org/docs/current/app-pgcontroldata.html
- MySQL 8.0 docs, InnoDB Redo Log / checkpointing: https://dev.mysql.com/doc/refman/8.0/en/innodb-redo-log.html
- Mohan et al., "ARIES" (1992) — checkpoints in the DPT/LSN framework.

## 18. Cheat Sheet
- Checkpoint = "recovery can start from log position L"; bounds replay to post-checkpoint log.
- Consistent = stop-the-world, full flush; fuzzy = keep running, DPT snapshot + async flush. Production = fuzzy.
- Redo point = LSN recovery starts replaying from.
- Dirty page table = pages dirtied-not-yet-flushed, with LSNs.
- Postgres: triggered by `checkpoint_timeout` (5min) or `max_wal_size` (1GB); control file (`pg_control`) stores the checkpoint LSN.
- `checkpoint_completion_target` spreads the flush burst (default 0.5).
- After a checkpoint, `full_page_writes` kicks in (whole-page log on first modification).
- Pre-checkpoint WAL → archive (if archiving) → recycle.
- Checkpoint ≠ backup; crash-recovery ≠ archive-recovery/PITR.

## 19. Quiz
1. The redo point is: a) the last commit b) the log position recovery starts replaying from c) the checkpoint end d) the first LSN → **b**
2. Production checkpoints are: a) consistent (stop-the-world) b) fuzzy c) never taken d) manual only → **b**
3. The dirty page table tracks: a) clean pages b) dirtied-but-unflushed pages c) indexes d) WAL → **b**
4. Postgres triggers a checkpoint on: a) timeout or WAL volume b) every commit c) every query d) never → **a**
5. A checkpoint is NOT: a) a recovery bound b) WAL recycling c) a backup d) a flush marker → **c**
6. `checkpoint_completion_target` spreads: a) WAL writes b) the flush burst c) commits d) vacuum → **b**
7. After a checkpoint, the next modification to each page needs: a) an LSN b) a full-page image c) a lock d) an index → **b**
8. Recovery finds the checkpoint via: a) the log scan b) the control file c) a backup d) the DPT → **b**

## 20. Flashcards
- **Q: What is a checkpoint for?** → **A:** Bounds crash recovery by marking a redo point so replay starts there, not at the log's beginning.
- **Q: Consistent vs fuzzy checkpoint?** → **A:** Consistent stops the DB and flushes all; fuzzy keeps running with a DPT snapshot + async flush. Fuzzy wins.
- **Q: What is the redo point?** → **A:** The LSN recovery starts replaying from.
- **Q: What's in the dirty page table?** → **A:** Pages modified in the buffer pool but not flushed, with their LSNs.
- **Q: When does Postgres checkpoint?** → **A:** `checkpoint_timeout` (5min) or `max_wal_size` (1GB), whichever first.
- **Q: Why full-page images after a checkpoint?** → **A:** So redo from the redo point never needs a pre-checkpoint page image (torn-page safety).
- **Q: What is `pg_control`?** → **A:** The control file storing the last valid checkpoint LSN, used by recovery.
- **Q: Checkpoint vs backup?** → **A:** Checkpoint = recovery point + flush; backup = restorable copy.

## 21. Revision
A checkpoint bounds recovery: record a redo point (LSN), flush dirty pages, record the checkpoint-end with remaining dirty pages. Consistent = stop-the-world; fuzzy = keep running (production). Postgres triggers on `checkpoint_timeout`/`max_wal_size`; `pg_control` stores the checkpoint; `checkpoint_completion_target` smooths I/O; `full_page_writes` resumes after each checkpoint. Checkpoint ≠ backup. This bounds crash-recovery replay — the input to ARIES's analysis phase (Section 04).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a checkpoint?" | 1, 2, 7 |
| "Consistent vs fuzzy checkpoint?" | 2, 7, 13 |
| "What is the redo point / DPT?" | 2, 7, 9, 13 |
| "checkpoint_timeout vs max_wal_size?" | 9, 13 |
| "Why full-page writes after a checkpoint?" | 13, 14 |
| "Why did my query slow after a checkpoint?" | 13, 16 |
| "How does recovery find the checkpoint?" | 9, 13 |
| "Checkpoint vs backup / VACUUM?" | 13, 14 |
