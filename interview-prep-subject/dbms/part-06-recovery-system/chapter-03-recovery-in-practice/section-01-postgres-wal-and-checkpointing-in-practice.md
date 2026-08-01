# Postgres WAL and Checkpointing in Practice

> **TL;DR**: Postgres's crash-safety is a concrete WAL + checkpointing pipeline you configure — `wal_level`, `max_wal_size`, `checkpoint_timeout`, `archive_command`, `synchronous_commit` — and knowing how to read the recovery signals (`pg_controldata`, the startup log, `pg_stat_bgwriter`) is the production skill interviews probe.

## 1. Why Does This Exist?
Theory (WAL, checkpoints, ARIES) only matters if you can *operate* it: a Postgres cluster that crashes and comes back clean is the product of settings chosen years earlier. This section exists to translate ARIES-style recovery into the actual knobs, commands, and log lines an engineer must know: which settings control durability vs latency, how a checkpoint is triggered and smoothed, what archiving does, and how to diagnose a crash or predict recovery time. Interviewers at Postgres-heavy shops (and every cloud DB job) ask "what does `wal_level` mean?", "why is my WAL huge?", "what do these log lines mean?" — the answer is this operational layer, not just the algorithm.

## 2. How Does It Work?
Postgres writes every change to the WAL (in `PGDATA/pg_wal`, 16MB segments). Key settings:
- `wal_level` — `minimal` (no WAL for many bulk ops — no PITR/replication), `replica` (default; enables standby + archive), `logical` (adds logical decoding).
- `fsync` / `wal_sync_method` / `synchronous_commit` — how durably the log is flushed before a commit is acknowledged.
- `max_wal_size` / `checkpoint_timeout` / `checkpoint_completion_target` — checkpoint frequency and smoothing; `min_wal_size` for segment recycling.
- `archive_mode` / `archive_command` — copy completed WAL segments to an archive (the input to PITR and to failover).
At startup, crash recovery reads `pg_control`, locates the last checkpoint, and replays WAL (Analysis/Redo/Undo — Section 04), logging progress lines. `pg_stat_bgwriter` shows checkpoint counts and write/sync times.

## 3. When Is It Used?
- **Every commit** — WAL append + optional fsync.
- **Every checkpoint** — background checkpointer flushes dirty pages (every `checkpoint_timeout` or `max_wal_size`).
- **Crash recovery** — every unclean shutdown runs it automatically.
- **PITR / restore** — archive_command + `pg_basebackup` restore.
- **Replication** — standbys stream/replay WAL.
- **Tuning** — when WAL grows fast, checkpoints spike I/O, or recovery is slow.

## 4. Why Wasn't Another Approach Chosen?
- *`wal_level=minimal` for everything*: saves WAL but forbids PITR and replication — unacceptable for production durability requirements. The default `replica` is the correct baseline.
- *Always `synchronous_commit=on`*: safest but adds per-commit fsync latency; the `off`/`remote_*` variants exist because some workloads (metrics, cache, batch) can trade bounded loss for speed — a *product* decision, not a technical accident.
- *Frequent, tiny checkpoints*: fast recovery but constant I/O overhead; *rare, huge checkpoints*: minimal overhead but long recovery + big WAL. `max_wal_size`/`checkpoint_timeout`/`completion_target` are the tuning surface; there's no single right answer, only per-workload trade-offs.
- *No archiving*: you get crash recovery but not media recovery or PITR — the failure taxonomy (Chapter 01) says you need both. `archive_mode` is the deliberate second layer.
- *fsync=off*: available (test workloads) but documented as "you will lose data" — the WAL is the durability line; disabling it is the extreme of the trade.

## 5. Intuition
Think of Postgres as a **restaurant that writes every order into a numbered receipt book (WAL)**. Settings decide: *how detailed* the receipts are (`wal_level`: minimal=cheap notes, replica=full copies for the manager's backup, logical=also machine-readable), *how fast the bookkeeper stamps "paid"* (`synchronous_commit`), *how often the day's books are closed* (`checkpoint_timeout`/`max_wal_size` — closing balances the ledger and trims the receipt stack), and *whether used receipt books are sent to the corporate archive* (`archive_command` — for rebuilding after the restaurant burns down). After any fire, the manager (recovery) reopens the books from the last close (checkpoint) and re-records every receipt since — the log lines you see on startup.

## 6. Real-World Analogy
**A shipping company's manifest system**: every parcel's label is written to the manifest (WAL) before the truck (page) leaves; "committed" means the manifest page is filed (fsync) before the customer is told "sent." Every Friday the dispatcher closes the week's manifest (checkpoint) and ships the old manifest to the records vault (archive). If the office floods, you restore the Friday close + every manifest shipped since (PITR), and the parcel ledgers come back consistent. The settings aren't exotic — they're just *how carefully* the manifest is kept, *when* it's filed, and *where* the copies go.

## 7. Formal Definition
- **wal_level**: the level of detail logged. `minimal` — WAL omits most information needed to reconstruct from a backup (no PITR/standby; bulk operations can be under-logged); `replica` — full WAL supporting read replicas and PITR (default); `logical` — `replica` + logical decoding of row changes.
- **synchronous_commit**: whether the commit waits for the WAL flush: `on` (wait for local flush), `remote_write` (wait for standby to receive), `remote_apply` (wait for standby to *apply*), `off` (no wait; acknowledge immediately).
- **max_wal_size / checkpoint_timeout**: checkpoint is triggered when either the WAL volume since the last checkpoint reaches `max_wal_size` (default 1GB) or `checkpoint_timeout` (default 5min) elapses.
- **checkpoint_completion_target**: fraction of the checkpoint interval over which the checkpointer spreads its flush (default 0.5).
- **archive_mode / archive_command**: archive_mode enables WAL archiving; archive_command is a shell command executed for each completed WAL segment (e.g., `test ! -f ... && cp ...`). Required for PITR and for a standby that may fall far behind.
- **pg_control**: the control file with the last valid checkpoint location, WAL state, and system ID — read at startup to begin recovery.

## 8. Example
Production config (`postgresql.conf`):
```
wal_level = replica
fsync = on
wal_sync_method = fdatasync
synchronous_commit = on
checkpoint_timeout = 5min
max_wal_size = 2GB
min_wal_size = 80MB
checkpoint_completion_target = 0.9
archive_mode = on
archive_command = 'test ! -f /backup/wal/%f && cp %p /backup/wal/%f'
```
After a `kill -9` of the server:
```
$ pg_ctl start
LOG:  database system was interrupted; last known up at 2026-08-02 10:32:04
LOG:  database system was not properly shut down; automatic recovery in progress
LOG:  redo starts at 0/2E000000          # Analysis found the redo point
LOG:  redo done at 0/2F4A2B80            # Redo phase complete
LOG:  invalid record length ...          # (torn tail ignored via checksum)
LOG:  checkpoint complete
LOG:  database system is ready to accept connections
```
Diagnosis with tools: `pg_controldata $PGDATA | grep checkpoint` shows the checkpoint LSN; `pg_waldump -p $PGDATA/pg_wal | head` shows records; `SELECT * FROM pg_stat_bgwriter;` shows `checkpoints_timed`/`checkpoints_req` and write times.

## 9. Internal Working
1. Every change writes a WAL record with an LSN; the page gets `pageLSN`; at commit the record is flushed per `synchronous_commit`.
2. The **checkpointer** runs continuously: when `checkpoint_timeout` elapses or WAL since last checkpoint ≥ `max_wal_size`, it begins a checkpoint — writes a `CHECKPOINT` record (redo point), flushes dirty pages (spread over `checkpoint_completion_target` of the interval), writes the checkpoint end + updates `pg_control`, and recycles WAL segments older than the redo point.
3. **Archiver** copies each completed segment via `archive_command`; failures retry (`pg_stat_archiver.failed_count`); archiving must succeed or WAL accumulates (`archive_mode` semantics).
4. On crash: startup reads `pg_control`, loads the last checkpoint, and runs Analysis/Redo/Undo (Section 04). Recovery replays from the redo point using pageLSN checks; CLOG/hint bits provide commit status; uncommitted transactions are undone.
5. Monitoring: `pg_stat_bgwriter` (checkpoint counts, write time), `pg_stat_archiver` (archiving success/failure), `pg_ls_waldir()` (WAL volume), `pg_stat_replication` (standby lag).

## 10. Time Complexity
- Checkpoint cost: O(#dirty pages) flushed + O(DPT) bookkeeping per interval.
- Recovery: O(log records after redo point) + O(undo of active txns) — minutes for typical clusters; grows with `max_wal_size` distance.
- WAL write: O(1) per record + amortized fsync (group commit).
- Archiving: O(segment) per completed segment, I/O-bound.
- The `synchronous_commit=on` → `off` switch changes per-commit latency by roughly the fsync cost (up to ~10x).

## 11. Advantages
- **Durability you can tune**: each `synchronous_commit` level is a documented durability/latency point.
- **Bounded recovery**: `max_wal_size` bounds replay distance; recovery is typically seconds-to-minutes.
- **PITR/DR**: archiving + `pg_basebackup` give point-in-time restore and streaming-replication feed.
- **Observable**: log lines, `pg_stat_bgwriter`, `pg_controldata`, `pg_waldump` make the recovery machinery transparent.
- **Zero-DBA defaults**: out-of-the-box settings (1GB / 5min / 0.5) work for most workloads.

## 12. Disadvantages
- **Misconfiguration is silent** — wrong `archive_command`, `fsync=off`, or `synchronous_commit=off` degrade durability without an error until the wrong moment.
- **Checkpoint I/O spikes** — big dirty-buffer flushes can stall traffic (tunable, not eliminated).
- **WAL bloat** — heavy DDL/VACUUM or a lagging archive grows `pg_wal` (filling disk is a classic incident).
- **Recovery isn't instant** — failover to a standby is the only way to get near-zero RTO; local crash recovery always has a gap.
- **Many knobs** — `wal_level`, sync modes, archive, checkpoints interact; knowing the matrix is a real skill.

## 13. Interview Questions
1. **Q: What does `wal_level` do and what values exist?** A: Controls what's written to the WAL. `minimal` (under-logged, no PITR/replica), `replica` (default; full WAL for PITR + streaming standby), `logical` (adds logical decoding for change capture). You need `replica`+ for any serious durability/replication setup.
2. **Q: What is the difference between `synchronous_commit=on`, `off`, `remote_write`, and `remote_apply`?** A: `on` — wait for the local WAL flush before ack. `off` — ack without flushing (recent commits may be lost on power failure). `remote_write` — wait until the standby received (OS write) but not necessarily applied. `remote_apply` — wait until the standby *applied* the change. Each trades latency for a stronger durability/availability point.
3. **Q: What triggers a checkpoint in Postgres?** A: Elapsed `checkpoint_timeout` (default 5min) or WAL written since the last checkpoint reaching `max_wal_size` (default 1GB) — whichever comes first. Also explicit `CHECKPOINT` and some DDL paths.
4. **Q: What does `checkpoint_completion_target` do?** A: Spreads the checkpoint flush over a fraction (default 0.5) of the checkpoint interval to smooth I/O instead of bursting — raising it reduces latency spikes but risks overlapping the next interval.
5. **Q: PR: Why did my `pg_wal` directory fill the disk?** A: WAL accumulates when (a) `max_wal_size` is reached but checkpoints are slow, (b) archiving is failing so segments can't be recycled (they're not archived), (c) a standby is disconnected and `wal_keep_size` is large, or (d) massive writes from VACUUM/DDL. Check `pg_stat_archiver` and `pg_stat_replication`.
6. **Q: What does `archive_command` do and why is it required for PITR?** A: It copies each completed WAL segment to a safe location. PITR restores a base backup then replays these archived segments — without them, you can only restore to the backup moment. A failing archive command is a silent PITR-risk.
7. **Q: What do the "redo starts at / redo done at" log lines mean?** A: Crash recovery ran its Analysis (found the redo point) and Redo (replayed WAL from it). "Invalid record length" later in the log is normal — it's the torn tail, safely ignored via checksums. Seeing these lines at startup = the cluster was uncleanly stopped and recovered.
8. **Q: PR: How do you make crash recovery faster?** A: Reduce the log distance to the last checkpoint (lower `max_wal_size` or `checkpoint_timeout`), keep transactions short (smaller undo), enable checksums (faster validation), and consider a standby for near-zero RTO instead of local recovery. Recovery time ≈ log after the redo point + undo of active transactions.
9. **Q: What is `pg_controldata` used for?** A: Inspects the control file: checkpoint locations, `wal_level`, system ID, and the database's shutdown state. It tells you whether the cluster is clean, crashed, or in recovery — the first diagnostic on an unclean shutdown.
10. **Q: TRICKY: What happens if `pg_control` is corrupted?** A: Postgres keeps a backup control file; recovery can fall back to it. If both are gone, you can use `pg_resetwal` (dangerous — forgets WAL consistency, may lose data; used only for emergency restart) — the honest answer is "you may have to accept data loss or restore from backup."
11. **Q: Why is `fsync=off` a footgun?** A: Postgres trusts the OS flush; without fsync, "durable" writes may be lost on power failure. It's documented as data-losing — only for testing/benchmarks. Interviews love "what could go wrong with fsync=off?" → answer: committed transactions lost on crash.
12. **Q: What is the difference between `min_wal_size` and `max_wal_size`?** A: `min_wal_size` is the target for *recycling* WAL segments during checkpoints (how much old WAL to keep around); `max_wal_size` triggers a checkpoint when WAL exceeds it. They bound disk usage vs checkpoint frequency.
13. **Q: PRODUCTION: A standby can't connect; the primary's WAL is growing. What's happening?** A: The primary keeps WAL the standby hasn't consumed (replication slots / `wal_keep_size`). If the standby is far behind, you may need to re-provision it (pg_basebackup) or the primary will recycle needed segments. Monitor `pg_replication_slots` and lag.
14. **Q: What is the difference between WAL archiving and streaming replication?** A: Archiving copies *completed* segments to durable storage (for PITR/media recovery) asynchronously. Streaming replication sends *live* WAL to standbys for continuous replay (availability/failover). They're complementary: archiving = durability/DR, streaming = availability/RTO.
15. **Q: TRICKY: You see "checkpoint starting: time" — what's happening?** A: The checkpointer was triggered (time or size) and is beginning its flush phase. Combined with `checkpoint_completion_target`, this is the I/O burst you watch for latency impacts — the log equivalent of `pg_stat_bgwriter.checkpoint_write_time` spiking.

## 14. Follow-Up Questions
1. **Q: How does `synchronous_commit=remote_apply` protect you?** A: A commit isn't acknowledged until a synchronous standby has *applied* it — so if the primary dies instantly, no acknowledged transaction is lost on the standby (RPO=0 for acknowledged commits, at the cost of added commit latency).
2. **Q: What is a replication slot and why does it affect WAL?** A: A slot reserves WAL (and in logical mode, state) for a consumer; it prevents the primary from recycling WAL the consumer still needs — but an abandoned slot leaks WAL forever. Monitor and remove dead slots.
3. **Q: How does `pg_stat_archiver` reveal trouble?** A: `failed_count`/`last_failed_time` rising = archiving failing (PITR at risk); `archived_count` not increasing = archiving stalled; these are the first checks on "WAL is huge" incidents.

## 15. Coding Example
```bash
# Diagnose a crash / recovery
pg_controldata $PGDATA | grep -E "state|checkpoint"     # shutdown state + checkpoint LSN
# Read the actual WAL records
pg_waldump -p $PGDATA/pg_wal/ | head -30
# Monitor checkpoints and archiving
psql -c "SELECT checkpoints_timed, checkpoints_req, checkpoint_write_time FROM pg_stat_bgwriter;"
psql -c "SELECT * FROM pg_stat_archiver;"
psql -c "SELECT * FROM pg_stat_replication;"
```
```sql
-- Set/observe the durability knobs
ALTER SYSTEM SET wal_level = 'replica';        -- requires restart
ALTER SYSTEM SET synchronous_commit = 'on';
ALTER SYSTEM SET max_wal_size = '2GB';
ALTER SYSTEM SET checkpoint_timeout = '5min';
ALTER SYSTEM SET archive_mode = 'on';
ALTER SYSTEM SET archive_command = 'test ! -f /backup/wal/%f && cp %p /backup/wal/%f';
SELECT pg_reload_conf();
```
```pseudocode
// Postgres crash recovery, as the server does it
on startup():
    pg_control = read_control_file()          // find last valid checkpoint
    if shutdown_state != clean:
        redo_point, dpt = analysis(pg_control) // "redo starts at ..."
        redo(redo_point)                       // "redo done at ..."
        undo(active_transactions())
    checkpoint()
    ready_for_connections()
```

## 16. Industry Usage
- **PostgreSQL**: this section is the daily reality for every Postgres DBA/engineer — RDS/Aurora/GCP Cloud SQL all expose `wal_level`, `synchronous_commit`, checkpoint tuning, and archive settings.
- **RDS/Aurora Postgres**: automated backups use WAL archiving; Aurora adds a distributed storage layer where WAL is the replication unit — the same ideas at cloud scale.
- **Patroni / failover automation**: uses replication slots + synchronous_commit to guarantee RPO=0 on failover.
- **All engines mirror these knobs**: MySQL `innodb_flush_log_at_trx_commit`, `innodb_redo_log_capacity`; SQL Server `DELAYED_DURABILITY`, `CHECKPOINT`, log shipping — knowing Postgres's set transfers.

## 17. References
- PostgreSQL docs, "Write-Ahead Logging (WAL)": https://www.postgresql.org/docs/current/wal-intro.html
- PostgreSQL docs, "WAL Configuration": https://www.postgresql.org/docs/current/wal-configuration.html
- PostgreSQL docs, "Reliability": https://www.postgresql.org/docs/current/wal-reliability.html
- PostgreSQL docs, `pg_controldata`: https://www.postgresql.org/docs/current/app-pgcontroldata.html
- PostgreSQL docs, `pg_waldump`: https://www.postgresql.org/docs/current/app-pgwaldump.html
- PostgreSQL docs, "Continuous Archiving and PITR": https://www.postgresql.org/docs/current/continuous-archiving.html

## 18. Cheat Sheet
- `wal_level`: minimal | replica (default) | logical.
- `synchronous_commit`: on | remote_write | remote_apply | off.
- Checkpoint trigger: `checkpoint_timeout` (5min) OR `max_wal_size` (1GB).
- `checkpoint_completion_target` (0.5) spreads flush I/O.
- `archive_mode`/`archive_command` → PITR + media recovery.
- Recovery log lines: "redo starts at ..." → "redo done at ..." (torn tail = "invalid record length", normal).
- `pg_controldata` = checkpoint + state diagnostic; `pg_waldump` = read WAL.
- `pg_stat_bgwriter`, `pg_stat_archiver`, `pg_stat_replication`, `pg_ls_waldir()` = monitoring.
- `fsync=off` loses data; abandoned replication slots leak WAL.
- Streaming replication = availability; archiving = durability/DR. Both needed.

## 19. Quiz
1. Which `wal_level` enables PITR? a) minimal b) replica c) logical d) none → **b**
2. `synchronous_commit=remote_apply` waits for: a) local fsync b) standby apply c) standby receive d) nothing → **b**
3. A checkpoint triggers when: a) timeout or max_wal_size b) every commit c) every query d) manual only → **a**
4. `archive_command` failure causes: a) WAL growth b) data loss c) crash d) nothing → **a**
5. "redo starts at 0/x" means: a) WAL full b) recovery replaying c) checkpoint done d) archive done → **b**
6. Which is the fastest way to near-zero RTO? a) larger max_wal_size b) standby + failover c) fsync=off d) more checkpoints → **b**
7. An abandoned replication slot: a) is harmless b) leaks WAL c) speeds recovery d) archives automatically → **b**
8. `pg_controldata` shows: a) query plans b) checkpoint LSN + shutdown state c) backups d) queries → **b**

## 20. Flashcards
- **Q: wal_level values?** → **A:** minimal, replica (default), logical.
- **Q: synchronous_commit values?** → **A:** on, remote_write, remote_apply, off.
- **Q: What triggers a checkpoint?** → **A:** checkpoint_timeout (5min) or max_wal_size (1GB).
- **Q: What does archive_command do?** → **A:** Copies completed WAL segments for PITR/media recovery.
- **Q: What do the redo log lines mean?** → **A:** Crash recovery replaying WAL from the redo point.
- **Q: Why did pg_wal fill the disk?** → **A:** Failed archiving, slow checkpoints, or a stale replication slot.
- **Q: fsync=off?** → **A:** Postgres skips the durability flush — data loss on crash (test only).
- **Q: Streaming vs archiving?** → **A:** Streaming = live replay to standby (availability); archiving = durable copies (DR/PITR).

## 21. Revision
Postgres crash safety = tunable WAL: `wal_level` (replica for PITR/standby), `synchronous_commit` (on = fsync before ack), checkpoints on `checkpoint_timeout`/`max_wal_size` with `checkpoint_completion_target` smoothing, and `archive_command` for PITR. Crash recovery = "redo starts/done at" log lines replaying WAL from the redo point. Monitor `pg_stat_bgwriter`, `pg_stat_archiver`, `pg_stat_replication`, `pg_ls_waldir()`. Footguns: fsync=off, abandoned slots, failing archiving. Streaming = availability; archiving = durability — both required.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What does wal_level do?" | 2, 7, 13 |
| "synchronous_commit levels?" | 2, 7, 13 |
| "What triggers a checkpoint?" | 9, 13 |
| "Why is pg_wal huge?" | 13, 14 |
| "What do the redo log lines mean?" | 8, 13 |
| "How does archiving enable PITR?" | 9, 13 |
| "fsync=off danger?" | 13 |
| "Streaming vs archiving?" | 13, 16 |
