# Part: Recovery System

> **TL;DR**: Recovery is the DBMS's guarantee that a crash never loses committed work or leaves half-applied transactions — powered by Write-Ahead Logging (WAL), checkpoints, and undo/redo algorithms like ARIES.

## What this part covers
Part 05 told you concurrency control keeps interleaved transactions *correct*; Part 06 answers what happens when the machine **dies mid-transaction**. It covers the taxonomy of failures (transaction → system → media), the storage hierarchy that forces us to design for loss (volatile RAM vs stable storage), and the three pillars of recovery: **Write-Ahead Logging** (log the change before touching data), **checkpointing** (bound how much log recovery must replay), and **undo/redo** (restore aborted transactions and committed-but-not-flushed transactions). It ends with ARIES — the industry-standard algorithm (LSNs, dirty-page tables, redo-then-undo) — and how Postgres actually implements WAL and checkpoints in production, plus backup/replication strategies.

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| **Chapter 01: Failures and Storage** | types of DB failures; storage structure & stable storage | Classify failures (transaction/system/media) and choose the right recovery strategy; explain why RAM isn't enough and how stable storage (fsync, RAID) works |
| **Chapter 02: Recovery Algorithms** | log-based recovery & WAL; checkpointing; undo/redo & shadow paging; ARIES & AIOS | Write and replay log records; take consistent/non-quiescent checkpoints; apply undo/redo and understand why shadow paging lost; run ARIES's 3 phases |
| **Chapter 03: Recovery in Practice** | Postgres WAL & checkpointing; backups & replication | Configure `wal_level`, `checkpoint_timeout`, `archive_command`; build backup/restore + PITR + streaming replication |

## Study order
1. **Chapter 01** — know the *failure types* first (each determines which recovery algorithm applies).
2. **Chapter 02** — the theory: WAL rules, checkpoints, undo/redo, ARIES. This is the interview core.
3. **Chapter 03** — map theory to Postgres (`pg_wal`, `CHECKPOINT`, `pg_ctl` recovery) and to production backup/DR (PITR, replication).

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ★★★★☆ (4/5)** — a top-4 DBMS topic. Every serious DB round asks "what is WAL?", "how does recovery work?", "what's the difference between undo and redo?"
- **Emphasized by**: all database-focused roles — Amazon Aurora/DynamoDB teams, Google (Spanner, F1), PostgreSQL core contributors, CockroachDB, MongoDB (WiredTiger), and every infra/data engineer at Meta/Stripe/Uber. Crash-consistency questions also appear in distributed-systems rounds (Kafka, Zookeeper, etc.).
- Typical asked: "WAL rule (log before data)", "undo vs redo", "what is a checkpoint?", "how does ARIES work?", "fsync and durability", "PITR", "why can't you lose committed data?".

## How the parts connect (roadmap)
- **Part 05 (Transactions)** defined durability & atomicity as ACID promises; this part delivers them. Strict 2PL (Part 05) gives recovery the "only committed transactions are visible" property it relies on.
- **Part 04 (Indexing/File Organization)** gave you pages and B-trees; recovery operates on those pages via LSNs.
- **Part 07 (Query Processing)** is orthogonal (performance); **Part 08 (NoSQL)** contrasts "durability vs availability" (CAP/PACELC) — this part is the durability side of that trade.
- Real systems: Postgres `pg_wal`, MySQL `ib_logfile`/redo log, InnoDB undo tablespace, SQL Server transaction log, MongoDB journal, RocksDB WAL — all implement the ARIES/WAL ideas here.
