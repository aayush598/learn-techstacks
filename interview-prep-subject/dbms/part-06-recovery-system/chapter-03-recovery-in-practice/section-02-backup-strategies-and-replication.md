# Backup Strategies and Replication

> **TL;DR**: Backups (physical/logical, full/incremental, with WAL archiving for **PITR**) protect against media and logical disasters, while replication (streaming, synchronous/asynchronous) protects against node failure — and you need *both* because they solve different failure classes.

## 1. Why Does This Exist?
Crash recovery (WAL/ARIES) covers system failures, but it can't help when the *data itself* is gone or corrupted: a dead disk (media failure), a `DROP TABLE` typo, a bad migration, a malicious delete, or an entire datacenter going dark. Backups and replication exist to cover exactly those classes. **Backups** are the durable, offline, point-in-time-recoverable copy — the last line of defense. **Replication** is the *online* copy — a standby that can take over instantly, minimizing downtime (RTO) and data loss (RPO). They exist as complementary layers because neither alone meets real SLAs: replication gives speed but shares the primary's corruption risks; backups give survivability but have restore time.

## 2. How Does It Work?
**Backup taxonomy**:
- **Physical** (file-level: copy of data files + WAL, e.g., `pg_basebackup`) — byte-exact, fast restore, replays WAL; required for PITR.
- **Logical** (schema/data dump, e.g., `pg_dump`) — portable, restores to a different version/engine, but slower and no WAL replay.
- **Full / incremental / differential** — full = everything; incremental = changes since the last *any* backup; differential = changes since the last *full*.
- **PITR**: base backup + WAL archiving (`archive_command`) → restore base + replay WAL to a target LSN/time/`txid`.
**Replication**:
- **Streaming replication** (WAL shipping): the primary streams WAL; the standby continuously applies it (`pg_stat_replication` tracks lag).
- **Synchronous vs asynchronous**: async — standby may lag (durability depends on primary fsync); sync — the primary waits for the standby (quorum configurable: `synchronous_standby_names`), so an acknowledged commit exists on both (RPO=0 for that standby) at the cost of commit latency.
- **Failover**: on primary loss, promote the standby (Patroni, repmgr, cloud services); with synchronous commit + slots, you can achieve RPO=0 failover.
- **Backup + replication together**: standby gives near-zero RTO; a WAL archive gives PITR back to any moment, including recovery from logical corruption that the standby also shares.

## 3. When Is It Used?
- **Scheduled backups**: nightly `pg_basebackup` (or snapshots) + continuous WAL archiving — the DR baseline.
- **PITR**: restore to just before a `DROP TABLE`, a bad batch job, or a botched migration.
- **Read replicas**: async standbys serving reads (offload); failover candidates.
- **Cross-region DR**: backups to S3 + archived WAL; synchronous replicas in another AZ/region.
- **Testing/staging**: logical dumps to create test environments, sanitized copies.
- In interviews: "design backup/DR for a database", "RPO/RTO", "synchronous vs asynchronous replication", "why both backup and replication?"

## 4. Why Wasn't Another Approach Chosen?
- *Backup-only*: restore time (RTO) can be hours; you lose all changes since the last backup unless you have WAL archiving (then it's PITR). Backups alone don't give availability.
- *Replication-only*: a standby protects against *node* failure but not *logical* corruption or *region*-wide loss — a `DROP TABLE` replays onto the standby too. No point-in-time backtracking. Hence backups (with archives) are still required.
- *Synchronous replication everywhere*: guarantees RPO=0 but adds commit latency and requires a quorum majority to avoid split-brain; async is chosen where latency matters and small loss is acceptable.
- *Copying the whole DB on every backup (no archiving)*: expensive and still loses the interval between backups; WAL archiving makes backups "continuous" for free.
- *Physical backups only / logical only*: physical is fastest and PITR-capable but not portable; logical is portable but slow and not point-in-time — production uses physical for DR + logical for portability/testing.

## 5. Intuition
**Backups are the vault; replication is the second cash register.** The vault copy (backup) sits safely off-site and can be rewound to any moment (PITR) — if the store burns down, you rebuild from the vault plus the day's receipts (WAL). The second register (replica) is wired in real time: if the main register dies, the second one keeps serving instantly (failover) — but it has the *same* books, so a bookkeeping error (logical corruption) appears in both. A well-run store keeps *both*: the wire keeps customers served, and the vault lets you undo mistakes that the wire faithfully repeated. Choosing one is choosing to lose either downtime (no wire) or your history (no vault).

## 6. Real-World Analogy
A **journalist's archive system**: every article draft is saved in a versioned archive (backup + PITR) and a mirror copy exists on a colleague's machine (replication). If the editor accidentally deletes the whole folder (logical error), the archive restores last night's state and you re-apply today's edits (PITR) — the mirror can't help because it mirrored the mistake. If the laptop is stolen (node failure), the colleague's machine takes over immediately (failover). The versioned archive costs disk; the mirror costs sync effort — a newsroom runs both because neither covers the other's failure mode.

## 7. Formal Definition
- **Backup**: a stored copy of the database state (full/incremental; physical or logical) used to restore the database after data loss or corruption.
- **PITR (Point-In-Time Recovery)**: restore a base backup and then apply archived WAL (or log) records to bring the database to a chosen point in time — effectively any committed state within the archive's retention.
- **RPO (Recovery Point Objective)**: the maximum acceptable data loss measured in time (e.g., "no more than 5 minutes lost"); **RTO (Recovery Time Objective)**: the maximum acceptable downtime (e.g., "back in 15 minutes").
- **Replication**: maintaining a second copy (standby) of the database by continuously applying the primary's WAL (or logical changes). **Asynchronous**: the standby may lag; commits don't wait. **Synchronous**: the primary waits until a quorum of listed standbys confirms receipt/apply before acknowledging the commit.
- **Streaming replication**: the standby connects to the primary and continuously receives and applies WAL records (recently also includes cascade / `pg_rewind` for fast rejoin).

## 8. Example
**Full backup + PITR** (Postgres):
- Nightly: `pg_basebackup -D /backup/base_$(date +%F)` → base backup at 02:00.
- Continuous: `archive_command = 'cp %p /backup/wal/%f'` captures every WAL segment.
- Tuesday 14:00: someone runs `DELETE FROM orders` (no WHERE). Recovery: restore the Monday 02:00 base backup, start Postgres in recovery with `recovery_target_time = '2026-08-04 13:59:59'`, replay archived WAL to just before the delete, resume. Lost data: ≤ 1 second (whatever was after the target). Without archiving: everything since 02:00 is lost.
**Replication with failover**:
- Primary + async standby, `synchronous_standby_names = 'standby1'`, `synchronous_commit = on`.
- Primary dies; standby1 has all acknowledged commits (sync). Ops (or Patroni) promotes standby1 → new primary; app fails over via DNS/connection pool. RPO=0 (for acknowledged commits), RTO=seconds-to-minutes.

## 9. Internal Working
1. **Backup**: `pg_basebackup` copies the cluster (or a snapshot does), recording a start LSN so WAL replay can begin coherently; archive_command ships segments. Restore = unpack + recovery config (`recovery_target_*` or `restore_command`/`recovery_end_command`) + replay.
2. **Streaming replication**: primary writes WAL → walwriter; the standby's walreceiver fetches via the streaming protocol → replays (startup process). Lag = how far behind (bytes/time); slots reserve WAL.
3. **Synchronous commit**: with `synchronous_standby_names`, the primary includes standbys in the commit wait quorum; a commit is acked only after the standby confirms (write/apply per the `synchronous_commit` level).
4. **Failover**: promotion (`pg_ctl promote` / `SELECT pg_promote()`) makes the standby a primary; `pg_rewind` lets an old primary rejoin the cluster safely afterward.
5. **Verification**: restore drills (actually test restoring backups!), `pg_checksums`, and replication-lag monitoring keep the safety nets trustworthy.

## 10. Time Complexity
- Base backup: O(data size) I/O; incremental: O(changes) — run nightly vs continuously.
- WAL archiving: O(WAL volume) — bandwidth-proportional, continuous.
- PITR restore: O(base restore) + O(WAL since backup) — RPO set by archive retention; RTO by base size + WAL volume.
- Streaming replication lag: bounded by network + apply speed; synchronous commit adds latency ≈ one RTT (network).
- Monitoring: O(1) queries (`pg_stat_replication`, `pg_is_in_recovery()`).

## 11. Advantages
- **Backups**: survive media/corruption/logical disasters; PITR rewinds to any committed state; portable (logical) or fast (physical); independent of the running system.
- **Replication**: near-zero RTO failover; read scaling (read replicas); synchronous mode gives RPO=0; continuous apply doubles as a rolling-upgrade/testing target.
- **Together**: an RPO/RTO story you can actually defend ("RPO≤5min via archives, RTO≈15min via standby + automated failover").

## 12. Disadvantages
- **Backups**: disk/bandwidth cost; restore is slow (a big base backup takes time); unverified backups are worthless; incremental chain complexity; archival retention management.
- **Replication**: async = data loss window; sync = commit latency + quorum complexity (must avoid split-brain); replicas replicate *mistakes*; storage/serving cost; failover automation is subtle (Promotion, `pg_rewind`, fencing).
- **Both**: operational burden (scheduling, monitoring, drills); failure of either layer is discovered exactly when it's needed.

## 13. Interview Questions
1. **Q: What is the difference between a physical and a logical backup?** A: Physical copies the data files + WAL (`pg_basebackup`) — byte-exact, fast, supports PITR. Logical dumps schema/data (`pg_dump`) — portable across versions/engines, but slower and no WAL replay for point-in-time restore.
2. **Q: What is PITR and how does it work?** A: Restore a base backup, then replay *archived WAL* to a chosen point (time, LSN, or transaction ID) — recovering the database to any committed state within the archive's retention, e.g., just before an accidental `DROP TABLE`.
3. **Q: What are RPO and RTO?** A: RPO = how much data you can afford to lose (time window); RTO = how long you can afford to be down. Backups give you PITR (low RPO if archiving, but high RTO); replication gives low RTO (failover) and, with sync commit, RPO=0.
4. **Q: Why do you need both backups and replication?** A: They cover different failure classes: replication protects against node failure (fast failover) but replicates logical corruption and can't rewind; backups protect against corruption/media/logical disasters and enable PITR but are slow to restore. Production runs both.
5. **Q: TRICKY: A `DROP TABLE` happens. Can the standby save you?** A: No — the standby will replay the DROP too (it has the same WAL). You restore from a backup + archived WAL to before the DROP (PITR). This is the classic "replication isn't a backup" argument.
6. **Q: What is the difference between synchronous and asynchronous replication?** A: Async — the primary doesn't wait; the standby may lag (data loss window on failover). Sync — the primary waits for a quorum of standbys to acknowledge the WAL before committing (RPO=0 for acknowledged commits), paying commit latency and requiring careful quorum config.
7. **Q: PR: What is a replication slot and why does it matter?** A: A slot reserves WAL on the primary for a specific standby/consumer, preventing needed segments from being recycled. Benefits: no lost WAL. Danger: an abandoned slot leaks WAL forever (disk full). Monitor `pg_replication_slots`.
8. **Q: How does failover work with streaming replication?** A: Promote the standby (`pg_ctl promote`/`SELECT pg_promote()`): it stops replaying, becomes a primary, and accepts writes. Tools like Patroni automate this with a quorum and fencing; `pg_rewind` safely rejoins the old primary afterward.
9. **Q: What sets RPO in a backup-only setup?** A: The interval between backups *unless* WAL archiving is on — then RPO is bounded by archive retention (continuous). Without archiving, an 02:00 backup loses everything after 02:00.
10. **Q: TRICKY: What is the "split-brain" risk in synchronous replication?** A: If the primary and standby both think they're the primary (partitioned network), both accept writes → divergent data. Prevention: quorum (only the majority side promotes), fencing, and heartbeat/lease mechanisms (Patroni uses a distributed consensus store like etcd/ZooKeeper).
11. **Q: What is a full vs incremental vs differential backup?** A: Full = everything. Incremental = changes since the last *any* backup (a chain). Differential = changes since the last *full* backup (cumulative). Chain complexity vs restore simplicity is the trade.
12. **Q: PR: What does a restore drill look like?** A: Periodically restore the base backup into a staging cluster, replay archived WAL to a recent point, run checks (row counts, `pg_checksums`, `amcheck`), and measure RTO. Unrestored backups rot — drills are how you know the safety net works.
13. **Q: How does WAL archiving interact with a standby?** A: Independently: the archive is durable PITR input; the standby streams live WAL. A standby can also be a source for archiving (`archive_mode=always`), and `restore_command` can backfill a lagging standby from the archive.
14. **Q: TRICKY: What does `synchronous_commit=remote_apply` buy vs `remote_write`?** A: `remote_write` = standby received WAL into the OS buffer (may not have applied); `remote_apply` = standby has applied it — so a failover after `remote_apply` has the change visible on the new primary. `remote_apply` is the strongest "no acknowledged transaction lost AND no visible change lost" setting, at the highest latency.
15. **Q: PRODUCTION: Design DR for a Postgres database. What do you say?** A: (1) Continuous WAL archiving to object storage + nightly `pg_basebackup` → PITR with RPO≈minutes. (2) A synchronous (or async) standby in another AZ → RTO≈seconds with automated promotion (Patroni). (3) Periodic restore drills + `pg_checksums`. (4) Document the RPO/RTO, backup retention, and the failover runbook. That's the full answer.

## 14. Follow-Up Questions
1. **Q: What is cascade replication and when is it useful?** A: A standby that itself serves standbys — reduces load on the primary's WAL streaming for fan-out (many replicas).
2. **Q: How do you measure replication lag?** A: `pg_stat_replication` (sent/received/replayed LSNs, time lag), `pg_wal_lsn_diff()`, or `pg_last_wal_receive_lsn()` vs `pg_last_wal_replay_lsn()` on the standby.
3. **Q: What is `pg_rewind`?** A: Fast recovery of an old primary after failover: it replays the divergent WAL from the new primary's timeline, so the old primary can rejoin without a full base backup.

## 15. Coding Example
```bash
# Base backup + WAL archiving for PITR
pg_basebackup -D /backup/base_$(date +%F) -h primary -p 5432 -U replicator -c fast -P
# archive_command (postgresql.conf):
archive_command = 'test ! -f /backup/wal/%f && cp %p /backup/wal/%f'
```
```bash
# Restore + PITR: unpack base, configure recovery, start
tar -xzf /backup/base_20260802.tar.gz -C /var/lib/postgresql/16/main
cat > /var/lib/postgresql/16/main/postgresql.conf <<EOF
restore_command = 'cp /backup/wal/%f %p'
recovery_target_time = '2026-08-04 13:59:59'
EOF
pg_ctl start    # replays archived WAL to the target, then is ready
```
```sql
-- Replication status & lag
SELECT client_addr, state, sync_state, write_lag, flush_lag, replay_lag
  FROM pg_stat_replication;
SELECT pg_is_in_recovery();                     -- true on a standby
SELECT pg_wal_lsn_diff(pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn());
```

## 16. Industry Usage
- **Every managed DB**: RDS/Aurora (automated snapshots + PITR via WAL; Aurora uses WAL as the distributed storage replication unit), GCP Cloud SQL, Azure Database for PostgreSQL.
- **Patroni + etcd**: standard HA setup — auto-promotion, synchronous standby, slot management.
- **Read scaling**: big read workloads use async read replicas (RDS Read Replicas) off the same WAL.
- **All engines analogize**: MySQL binary log for PITR + replication; SQL Server backup + log shipping/AGs; MongoDB oplog/journal for PITR; DynamoDB Global Tables for multi-region — same two layers (backup/archive vs replication), different names.

## 17. References
- PostgreSQL docs, "Continuous Archiving and Point-in-Time Recovery (PITR)": https://www.postgresql.org/docs/current/continuous-archiving.html
- PostgreSQL docs, "Streaming Replication": https://www.postgresql.org/docs/current/warm-standby.html
- PostgreSQL docs, "High Availability, Load Balancing, and Replication": https://www.postgresql.org/docs/current/high-availability.html
- PostgreSQL docs, `pg_basebackup`: https://www.postgresql.org/docs/current/app-pgbasebackup.html
- Patroni documentation: https://patroni.readthedocs.io/
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 11 (Replication) & Ch. 12 (Partitioning) — RPO/RTO framing.

## 18. Cheat Sheet
- Backup = offline restorable copy (media/logical disasters); Replication = online second copy (node failure).
- Physical (`pg_basebackup`) + WAL archiving = PITR; logical (`pg_dump`) = portability.
- RPO = max acceptable data loss; RTO = max acceptable downtime.
- PITR = base backup + archived WAL replay to a target time/LSN.
- Async replication = may lag (loss window); sync = wait for standby quorum (RPO=0, commit latency).
- Replication slots reserve WAL; abandoned slots leak WAL.
- `DROP TABLE` is *not* saved by a standby — only by backup + PITR.
- Split-brain → quorum + fencing (Patroni/etcd).
- Restore drills keep backups trustworthy; `pg_checksums`/`amcheck` validate.
- Every engine mirrors this: MySQL binlog, SQL Server log/AGs, Mongo journal/oplog.

## 19. Quiz
1. Which covers an accidental DROP TABLE? a) standby b) backup + PITR c) sync commit d) slots → **b**
2. RPO is: a) downtime b) max data loss c) backup size d) latency → **b**
3. PITR needs: a) base backup only b) base backup + archived WAL c) a standby d) logical dump → **b**
4. Synchronous replication provides: a) zero RTO always b) RPO=0 for acknowledged commits c) no latency cost d) no quorum → **b**
5. A replication slot: a) frees WAL b) reserves WAL c) archives WAL d) compresses WAL → **b**
6. A physical backup is: a) portable SQL dump b) byte copy of files + WAL c) a snapshot only d) config → **b**
7. Split-brain is prevented by: a) fsync b) quorum + fencing c) sync commit d) slots → **b**
8. Restore drills exist to: a) speed backups b) verify backups work c) reduce RPO d) save disk → **b**

## 20. Flashcards
- **Q: Backups vs replication?** → **A:** Backups = offline restorable copy; replication = online second copy.
- **Q: What is PITR?** → **A:** Base backup + replay archived WAL to a chosen point in time.
- **Q: RPO / RTO?** → **A:** Max data loss window / max downtime.
- **Q: Sync vs async replication?** → **A:** Sync waits for standby quorum (RPO=0, latency); async may lag.
- **Q: Why can't a standby fix a DROP TABLE?** → **A:** It replays the same WAL — the DROP hits both. PITR is the fix.
- **Q: What is a replication slot?** → **A:** Reserves WAL for a consumer; abandoned ones leak disk.
- **Q: What prevents split-brain?** → **A:** Quorum majority + fencing (Patroni + etcd).
- **Q: What's the safest sync setting?** → **A:** synchronous_commit=remote_apply (wait for standby apply).

## 21. Revision
Two safety layers: **backups** (physical + WAL archiving → PITR; covers media/corruption/logical errors; RPO≈archive retention, RTO=restore time) and **replication** (streaming WAL to a standby; async = availability, sync = RPO=0 with latency; failover via promotion + quorum). Remember: a standby mirrors mistakes — only backup + PITR rewinds time. RPO/RTO frame every DR answer. Monitor slots/lag; drill restores. All engines implement the same two layers.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Physical vs logical backup?" | 2, 7, 13 |
| "What is PITR / RPO / RTO?" | 2, 7, 13 |
| "Why both backup and replication?" | 1, 7, 13 |
| "Can a standby save a DROP TABLE?" | 13 |
| "Sync vs async replication?" | 2, 9, 13 |
| "What is a replication slot?" | 9, 13 |
| "How does failover work?" | 2, 9, 13 |
| "Design DR for a Postgres DB." | 13, 16 |
