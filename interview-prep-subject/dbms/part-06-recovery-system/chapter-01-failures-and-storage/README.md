# Chapter: Failures and Storage

## What you'll learn
- The **taxonomy of failures** — transaction failures, system failures, media failures — and why each one needs a *different* recovery strategy (undo only, redo only, or backup+log replay).
- The **storage hierarchy** (cache/RAM → disk → tape) and exactly why "just write to disk" is not durable — the role of the OS page cache, `fsync`, and **stable storage** (double-write, RAID, checksums).
- Why the *order* of writes (log-first) and the *moment* of flushing are the real crux of durability.

## Prerequisites (linked)
- [Part 06 README](../README.md) — the roadmap.
- [Part 05](../part-05-transactions-and-concurrency-control/README.md) — transactions, ACID durability/atomicity, commit semantics.

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Types of Database Failures](section-01-types-of-database-failures.md) | What can go wrong, and which recovery technique does each failure need? |
| 02 | [Storage Structure and Stable Storage](section-02-storage-structure-and-stable-storage.md) | Where does data physically live, and what makes a write actually survive a crash? |

## One-paragraph narrative connecting all sections
Recovery starts with a taxonomy: **transaction failures** (the app aborts, or the DBMS kills the transaction) need *undo* only; **system failures** (crash/power loss — volatile memory lost, disk intact) need *redo* of committed work and *undo* of uncommitted work; **media failures** (disk dies) need *backup + log replay*. Section 01 defines these three classes and maps each to its recovery prescription — the organizing skeleton for the whole part. Section 02 then explains the physical reality that forces the design: data lives in a hierarchy from CPU cache through the OS page cache down to disk, and "durable" means *somewhere a power cut can't erase*, i.e., **stable storage**. Because the OS buffers writes, a "successful" write isn't on disk until `fsync`; because disks fail and lie, stable storage needs redundancy (RAID, dual writes) and verification (checksums). Knowing *why writes are lost* is what makes the WAL rules in Chapter 02 feel inevitable rather than arbitrary.

## Common interview trap in this chapter
**Trap:** Saying "a crash loses the data" without distinguishing *what* is lost — RAM (loses everything since the last flush) vs disk (nothing lost, but pages may be torn/out-of-order). Also: confusing *system failure* with *media failure* — a system crash leaves your disk intact, so no backup replay is needed; a media failure does. And the biggest one: "the data was committed" ≠ "the data was on disk" — the commit only guarantees the *log record* was flushed, which is exactly why recovery replays the log.

## Checklist before moving on
- [ ] I can classify any failure into transaction/system/media and say which recovery mechanism applies.
- [ ] I can explain why the OS page cache breaks the "write = durable" assumption.
- [ ] I can explain what `fsync` guarantees and what a torn page is.
- [ ] I can describe stable storage (RAID + checksums + dual-write) and its trade-offs.
- [ ] I can say what a "flush of the log at commit" means and why it's the durability line.
