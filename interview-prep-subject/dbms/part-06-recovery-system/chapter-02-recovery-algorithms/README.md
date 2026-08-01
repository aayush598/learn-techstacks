# Chapter: Recovery Algorithms

## What you'll learn
- **Log-based recovery** and the WAL rule: what a log record contains, and why *log-before-data* plus *flush-the-log-before-commit* makes undo and redo possible.
- **Checkpointing**: how consistent vs fuzzy (non-quiescent) checkpoints bound recovery time without stopping the database.
- **Undo, redo, and shadow paging**: the classic algorithms — and why shadow paging (the only no-log option) lost the battle.
- **ARIES** and its cousin AIOS (Arithmetic / Index / Other Structure... no — **Algorithms for Recovery and Isolation Exploiting Semantics** is the real abbreviation — here meaning the *algorithmic core*: Analysis, Redo, Undo): LSNs, dirty-page tables, and the 3-phase recovery that every major engine implements.

## Prerequisites (linked)
- [Chapter 01 README](chapter-01-failures-and-storage/README.md) — failure taxonomy and storage/stable-storage model.
- [Part 05](../part-05-transactions-and-concurrency-control/README.md) — commit semantics, strict 2PL, isolation (recovery relies on "committed = visible" being well-defined).

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Log-Based Recovery and WAL](section-01-log-based-recovery-and-wal.md) | What goes in the log, and which order rules make recovery correct? |
| 02 | [Checkpointing](section-02-checkpointing.md) | How do you bound how much log recovery must replay? |
| 03 | [Undo, Redo, and Shadow Paging](section-03-undo-and-redo-and-shadow-paging.md) | How do the two classic recovery directions work, and why did the no-log alternative fail? |
| 04 | [Advanced Recovery: ARIES and AIOS](section-04-advanced-recovery-arise-and-aios.md) | What is the industry-standard algorithm, exactly? |

## One-paragraph narrative connecting all sections
Chapter 01 established that crashes lose RAM but not disk, and that only stable storage can be trusted. Chapter 02 builds the algorithms on that bedrock. Section 01 defines the log itself — a sequence of ordered, checksummed records (with the transaction ID, before-image, after-image, and a sequence number) — and states the two WAL rules that make recovery correct: **log first**, and **flush the log at commit before acknowledging**. Section 02 solves the performance problem — after weeks of uptime the log is huge and replaying it is slow — with **checkpoints**: periodic snapshots of "what's on disk" that let recovery start from a recent point; fuzzy checkpoints let the DB keep running while they're taken. Section 03 then names the two recovery *directions*: **undo** (reverse uncommitted transactions using before-images) and **redo** (re-apply committed transactions using after-images), and examines **shadow paging**, the only serious no-log alternative, and why it lost (commit latency, page-pair overhead, no cheap incremental log). Finally, Section 04 assembles everything into **ARIES**: LSNs stamp every page and log record, the dirty-page table tracks what may be on disk, and recovery runs three phases — **analysis** (figure out where to start and what's dirty), **redo** (reapply committed changes from the redo LSN), and **undo** (roll back uncommitted work using a history list) — the algorithm Postgres, MySQL, SQL Server, and most others implement in some form.

## Common interview trap in this chapter
**Trap:** Saying "redo applies only committed transactions and undo only uncommitted ones" *before* explaining that this is only safe because of strict 2PL / WAL ordering — the log's record order, not the transaction's commit status at scan time, is what decides. Also: thinking a *consistent* checkpoint (stop-the-world) is what databases use — production uses *fuzzy* checkpoints that record "pages dirtied up to LSN X" without stopping writes. And confusing LSN (log sequence number, monotonic) with the transaction's commit timestamp.

## Checklist before moving on
- [ ] I can state the two WAL rules and prove why "log before data" is necessary.
- [ ] I can write a minimal log record (txid, before-image, after-image, LSN, type).
- [ ] I can contrast consistent vs fuzzy checkpoints and say which production uses.
- [ ] I can explain undo vs redo, with the direction each reads.
- [ ] I can explain shadow paging and 2-3 reasons it lost.
- [ ] I can trace ARIES: analysis → redo → undo, and define LSN, dirty page table, history list.
