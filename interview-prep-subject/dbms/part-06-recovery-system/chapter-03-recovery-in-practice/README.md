# Chapter: Recovery in Practice

## What you'll learn
- How **PostgreSQL** actually configures and runs WAL + checkpointing in production: `wal_level`, `max_wal_size`, `checkpoint_timeout`, `archive_command`, `pg_ctl` crash recovery, and how to read the recovery story from the server log.
- **Backup strategies and replication**: full/incremental/differential/logical backups, `pg_basebackup`, **PITR** via WAL archiving, and streaming/synchronous/asynchronous replication — the real-world durability+availability machinery.

## Prerequisites (linked)
- [Chapter 01 README](chapter-01-failures-and-storage/README.md) — failure taxonomy and stable storage.
- [Chapter 02 README](chapter-02-recovery-algorithms/README.md) — WAL, checkpoints, undo/redo, ARIES.

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Postgres WAL and Checkpointing in Practice](section-01-postgres-wal-and-checkpointing-in-practice.md) | What knobs do you turn, and what does recovery actually look like? |
| 02 | [Backup Strategies and Replication](section-02-backup-strategies-and-replication.md) | How do you survive media failure, and how do you get zero-downtime failover? |

## One-paragraph narrative connecting all sections
Chapter 02 gave you the algorithms; this chapter is the ops manual. Section 01 walks through Postgres's production WAL configuration — the settings that matter (`wal_level=replica`, `max_wal_size`, `checkpoint_timeout`, `checkpoint_completion_target`, `archive_mode`/`archive_command`, `synchronous_commit`), what each one changes, and how to read the crash-recovery story (`pg_controldata`, the startup log's "redo starts at..." lines, `pg_waldump`). It closes with the operational playbook: when recovery runs, how long it takes, and the monitoring signals that predict it. Section 02 then scales the story up: backups (physical vs logical, full vs incremental, `pg_basebackup`, consistency and how WAL archiving enables **PITR** with `recovery_target_time`), and replication (streaming replication, synchronous vs asynchronous, the synchronous-quorum trade, and how replication + backups give you an RTO/RPO story you can defend in a design interview). Together they answer the two questions every ops-heavy interviewer asks: "how do you restore after a disaster?" and "how do you fail over without losing data?"

## Common interview trap in this chapter
**Trap:** Treating a *base backup* as the whole recovery story — without WAL archiving, a backup restores only to the moment of the backup. And treating *replication* as a substitute for backups: replicas protect against node failure, not against logical corruption (`DROP TABLE`, a bad migration) or region-wide loss — you still need archives. Also: `synchronous_commit=remote_apply` gives you durability but adds commit latency; "synchronous replication" does *not* mean zero RPO on its own — it means the commit isn't acknowledged until the standby has it.

## Checklist before moving on
- [ ] I can list the Postgres WAL settings and what each controls.
- [ ] I can explain what `wal_level` values mean and when to use `logical`.
- [ ] I can describe crash recovery start→end and what the server log lines mean.
- [ ] I can build a backup strategy: base backup + WAL archiving → PITR, with RPO/RTO estimates.
- [ ] I can contrast synchronous vs asynchronous replication and their durability/availability trade-offs.
- [ ] I can explain why backups and replication are both needed (not either/or).
