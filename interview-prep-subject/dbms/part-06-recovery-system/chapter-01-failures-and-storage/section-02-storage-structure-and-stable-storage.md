# Storage Structure and Stable Storage

> **TL;DR**: Data lives in a memory hierarchy — registers → cache → RAM → page cache → disk — and "durability" means reaching **stable storage** (storage that survives power loss), which requires understanding `fsync`, torn pages, checksums, and RAID.

## 1. Why Does This Exist?
ACID durability says "committed data survives crashes" — but *where* does data physically live? The answer shapes every recovery algorithm. Most data at any instant is in **volatile storage** (CPU registers, L1-L3 cache, RAM, OS page cache): fast but wiped by power loss. Only **non-volatile storage** (SSD, HDD) survives, and even that can be *partially written* (torn pages) or *corrupted* (bad sectors). The concept of **stable storage** exists to name the subset of non-volatile storage that is *trustworthy*: redundant, checksummed, and written atomically enough that a crash leaves either the old or new state — never garbage. Every WAL rule ("log first, fsync the log") is a direct consequence of this storage reality: you must put the commit marker somewhere stable before you can claim durability.

## 2. How Does It Work?
- **Hierarchy**: registers → cache → RAM → disk. The DBMS's **buffer pool** (RAM) caches pages; the OS adds its **page cache** on top. A "write" lands in these caches immediately and reaches disk only via a flush.
- **`fsync`/`fdatasync`**: the syscall that forces dirty pages (or the file range) out of the page cache to disk; it returns only when the write is *durable*. Without it, a power failure loses cached data.
- **Stable storage primitives**: (a) **redundancy** — store two copies (dual write) or parity (RAID-1/5), so a single bad sector doesn't destroy data; (b) **atomic write** — never expose a partially written block (write-ahead at the storage layer, or full-page images in the DB log); (c) **verification** — checksums on every page so torn/corrupted reads are detected.
- **Write ordering**: the OS can write pages *out of order* and *partially*; the DBMS can't control that — so it orders *its* writes (log record before data page) and adds checksums to detect the residue.

## 3. When Is It Used?
- Every commit: the DBMS forces the commit log record to disk (`fsync` the WAL), which is the durability line.
- Every checkpoint: flushing dirty pages to disk (Chapter 02) so recovery has less to replay.
- Buffer management: LRU-ish replacement of the buffer pool; dirty vs clean page tracking (needed to know what must be flushed).
- Torn-page protection: checksums (Postgres `data_checksums`, InnoDB) + `full_page_writes` (write the whole page to the log on first modification after checkpoint).
- Durable deployments: RAID arrays, EBS volumes, hardware write-cache batteries, and `fdatasync`-friendly filesystems — all to make the storage "stable enough."

## 4. Why Wasn't Another Approach Chosen?
- *Assume RAM is durable* (no flush discipline): in-memory DBs (memcached, some Redis modes) — fast but data lost on crash; rejected for durable workloads.
- *Assume every write() is durable* (trust the OS): the page cache breaks this; data silently lost on power loss. Hence `fsync` is non-negotiable for commit records.
- *Single copy on disk (no redundancy)*: a bad sector corrupts a page with no recourse. RAID/dual-write adds cost but buys survival.
- *Write data pages directly to disk in commit order*: you'd need to know physical ordering and atomicity — the OS can't give you that. The **log** (append-only, checksummed, fsync'd) is the chosen mechanism because appends are naturally ordered and easy to make atomic.
- *Verify-by-rereading everything* (no checksums): too slow; checksums on read are the cheap, correct detection mechanism.
- *Shadow paging instead of logging*: makes each page copy-on-write so commits are atomic without a log — but doubles I/O and complicates garbage collection (Chapter 02 section on shadow paging explains why logging won).

## 5. Intuition
Think of the storage hierarchy as **sticky notes vs a filing cabinet**. You work on sticky notes (RAM) because they're fast, but a gust of wind (power loss) scatters them. When you want something saved, you must *file it in the cabinet* (disk) — and only when you've physically filed it can you claim "saved." The filing itself has hazards: the drawer can jam mid-push (torn page), and the cabinet can have a broken drawer (bad sector). Stable storage = a fireproof cabinet with double copies (RAID) and a checklist you consult on every read (checksums). The WAL is the "receipt book" you keep in the cabinet: you write the receipt *before* you change any working notes, so after any windstorm you can reconstruct what was really saved.

## 6. Real-World Analogy
A **photographer with memory cards and an album**. Shooting = writes to RAM card (fast, volatile). "Saved" means the *album* (stable storage): you print the photo (fsync) — only when the print is in the album is the shot safe. A power outage loses the card, not the album. If the printer jams mid-print (torn page), you print again from the negative (checksums/full-page images catch it). A flood in the studio (media failure) is why you keep *two* albums (RAID/backups). And the "receipt book" (WAL) records which photos you *intended* to print, so after any disaster you know exactly what needs re-printing — that's why you log before you print.

## 7. Formal Definition
**Volatile storage**: storage whose contents are lost when the system loses power (registers, cache, RAM, and, arguably, the OS page cache). **Non-volatile storage**: storage that survives power loss but may suffer *torn* (partial) writes and *media* failures (bad sectors, head crashes). **Stable storage**: non-volatile storage that is *trustworthy* — implemented via redundancy (e.g., keeping two copies of each block, or RAID with parity), atomic write protocols (a block write is either fully committed or leaves the old copy), and checksum/verification on every read. Writes to stable storage are treated as atomic; reads verify integrity. The DBMS's **Write-Ahead Log (WAL)** is kept on stable storage; the commit record is flushed there before a transaction is acknowledged.

## 8. Example
Postgres commit path in concrete steps:
1. App: `COMMIT;`
2. Postgres writes the commit record to the WAL buffer (in shared memory, volatile).
3. Postgres calls `fsync()` (via `wal_sync_method`) on the WAL file to force the record to disk — **this is the durability point**.
4. Only after the flush succeeds does `COMMIT` return "success" to the app.
5. Meanwhile, the data page (balance changed) may still be only in the buffer pool — it will be flushed later at a checkpoint. If the machine dies right after step 4, crash recovery **redoes** the change from the WAL.
If instead the WAL file is on a filesystem whose `fsync` is a no-op (some old/tuned filesystems, `sync_method=open_datasync` misconfig), step 3 is a lie and committed data can be lost — a classic durability footgun.

## 9. Internal Working
1. **Page lifecycle**: a page is read into the buffer pool; modifications mark it *dirty* (tracked in a dirty-page table with its LSN).
2. **WAL flush discipline**: on commit, the log record (containing the changes + LSN) is appended to the WAL buffer and `fsync`'d to stable storage *before* the commit is acknowledged. The data page may be written later, *in any order*, because the log has the authoritative record.
3. **fsync semantics**: the filesystem flush guarantees the bytes are on the device (with battery-backed caches, that's effectively stable); `fdatasync` flushes data only (skips metadata).
4. **Checksums**: Postgres computes a CRC on each page (if `data_checksums` enabled) and verifies on read; InnoDB stores per-page checksums in the page header. A mismatch ⇒ torn/corrupt page detected.
5. **Full-page images**: after a checkpoint, the first write to a page also writes the *entire page* to the WAL (`full_page_writes`), so that a later crash cannot replay an incremental change onto a torn page.
6. **RAID/storage layer**: RAID-1 mirrors blocks; RAID-5 stripes with parity — surviving a single drive loss. The DBMS doesn't see it; it just sees "storage that doesn't lie."

## 10. Time Complexity
- Reading/writing a page in the buffer pool: O(1) + I/O if missing.
- `fsync` of the log: O(1) per flush (or batched — **group commit** batches several commits into one fsync, amortizing cost).
- Checksum compute/verify: O(page size) per page.
- The durability flush is the dominant *latency* cost (≈1-5 ms), which is why every engine exposes a "weaken the flush for speed" knob (`synchronous_commit=off`, `innodb_flush_log_at_trx_commit=0/2`).

## 11. Advantages
- **Durability by construction**: commit = log record on stable storage; the rest can be lazy.
- **Performance**: the buffer pool keeps hot pages in RAM; only the log forces I/O per commit (and group commit batches it).
- **Correctness under torn writes**: checksums + full-page images make the OS's unreliable write behavior *detectable* and *recoverable*.
- **Portability**: `fsync`/checksums work on any filesystem; the DBMS doesn't depend on filesystem-level atomicity guarantees.

## 12. Disadvantages
- **fsync latency**: one random I/O per commit (mitigated by group commit).
- **Full-page writes bloat the log** (`full_page_writes`), increasing WAL volume.
- **Checksums cost CPU** on every read.
- **RAID is not a backup**: RAID survives one bad sector, not `DROP TABLE` or a fire — the taxonomy (Chapter 01) still applies.
- **fsync can be silently broken** by misconfigured filesystems/volumes, causing data loss that's discovered only on failure — "fsyncgate" class incidents.

## 13. Interview Questions
1. **Q: What is the storage hierarchy and why does it matter for durability?** A: Registers → cache → RAM → OS page cache → disk. Everything above disk is volatile (lost on power failure) or buffered (lost without flush). Durability therefore means forcing the *commit marker* down to disk (stable storage) via fsync, not just writing to RAM.
2. **Q: What does `fsync` guarantee?** A: That the file's dirty pages have been written to the storage device and the write survives a power failure (assuming honest hardware). It's the syscall that converts "written to cache" into "durable."
3. **Q: Why can't you trust `write()` alone?** A: The write lands in the OS page cache and can be lost when the machine loses power before the cache is flushed. `fsync` forces it out. Any "durability" claim without a flush is fiction.
4. **Q: What is stable storage?** A: Non-volatile storage made trustworthy via redundancy (two copies / RAID), atomic-write handling, and checksums — a block write is all-or-nothing and verified on read. The WAL lives on stable storage.
5. **Q: What is a torn page and how is it handled?** A: A page partially written to disk (power lost mid-write) — neither old nor new content. Handled with page checksums (detect) and `full_page_writes` (log a complete page image so incremental redo can be applied to a known-good state).
6. **Q: TRICKY: When is the commit actually durable?** A: Exactly when the commit record is *fsync'd to the WAL on stable storage*. Data pages can still be in the buffer pool — recovery will redo them. Anything earlier than the fsync is not durable; hence `synchronous_commit=off` knowingly gives up this line.
7. **Q: What is the buffer pool and how does it relate to durability?** A: The in-memory cache of database pages. It's what makes hot reads fast; its dirty pages are written to disk lazily (checkpoints). Because it's volatile, committed changes that are only in the buffer pool need the WAL to be redone after a crash.
8. **Q: What is group commit?** A: Batching several transactions' log flushes into one `fsync` so the per-commit I/O cost is amortized. This is why modern engines can commit thousands of transactions/sec despite fsync costing ~1-5 ms.
9. **Q: PR: `synchronous_commit=off` or `innodb_flush_log_at_trx_commit=0` — what are you trading?** A: Skipping the per-commit fsync for ~10x lower latency, accepting that the most recent commits may be lost on a power failure (the WAL data survives in memory and is flushed later; a *system crash* that loses RAM loses those records). Fine for non-critical workloads, never for money.
10. **Q: Why does the WAL need to be on the same storage as... no, why does it need stable storage?** A: Because the log is the source of truth after a crash: it must survive the crash that recovery is responding to. If the log were volatile, recovery would have nothing to replay. If it's corrupt, recovery is garbage.
11. **Q: What is `full_page_writes` and when would you disable it?** A: It writes the whole page to the WAL the first time it's modified after a checkpoint, so redo can't be applied to a torn page. Disable it only when the underlying storage guarantees atomic page writes (e.g., some filesystems with checksummed COW like ZFS/btrfs, or certain SANs) — otherwise crash recovery can corrupt data.
12. **Q: TRICKY: Does RAID make the database crash-safe by itself?** A: No. RAID survives a *drive* failure (media class), but doesn't protect against torn pages, silent corruption (unless checksummed), logical corruption (`DROP TABLE`), or anything the application does. RAID + DB-level checksums + backups + WAL are all separate layers.
13. **Q: PR: Why does adding `fsync` make my commits slow?** A: Each fsync is a forced write to physical storage (a few ms, and on spinning disks a cache-flush). With synchronous commits, every commit waits for it. Fixes: group commit (already on by default), lowering `synchronous_commit`, using a battery-backed controller cache (makes the flush fast and safe), or `fsync=off` when durability isn't needed.
14. **Q: What is the difference between `fsync` and `fdatasync`?** A: `fsync` flushes data *and* file metadata (size, timestamps); `fdatasync` flushes data only. Postgres lets you choose (`wal_sync_method`). `fdatasync` can be cheaper when metadata doesn't matter.

## 14. Follow-Up Questions
1. **Q: What happens if the OS loses its page cache and the DBMS thinks a page is clean?** A: That's exactly why commit flushes the *log*, not data pages — the DBMS never trusts clean-page state for durability; the log record is the authority.
2. **Q: Why is an append-only log easier to make durable than a random-write data page?** A: Appends are sequential (fast), naturally ordered, and can be made atomic with a single checksummed record and a write pointer — a torn tail is just "not committed." Random page writes have no such ordering.
3. **Q: What is a "dirty page" and a "clean page"?** A: A dirty page has been modified in the buffer pool and not yet written to disk; a clean page matches disk. The dirty-page table (with each page's LSN) is what checkpoints and recovery use.

## 15. Coding Example
```bash
# Observe fsync settings and log location
psql -c "SHOW wal_sync_method; SHOW synchronous_commit; SHOW full_page_writes;"
ls -la $PGDATA/pg_wal/            # the WAL segment files (16MB each)
```
```c
// What the DBMS does at commit (conceptually — Postgres CommitTransaction path)
append_log_record(commit_record, lsn);      // in-memory WAL buffer
if (synchronous_commit == ON)
    fsync(wal_fd);                          // durability line
acknowledge_commit();
// data page flush is deferred to checkpoints
```
```pseudocode
// Torn-page-safe pattern: log the full image before modifying
on_first_page_modification_after_checkpoint(page):
    write_wal_record(type=FULL_PAGE_IMAGE, page_data=page)
    write_wal_record(type=CHANGE, ...)
on_read(page):
    if checksum(page) != stored_checksum(page): raise TornPage(page)
```

## 16. Industry Usage
- **PostgreSQL**: WAL in `pg_wal`; `wal_sync_method`, `synchronous_commit`, `full_page_writes`, `data_checksums` (initdb), group commit; `fsync=off` exists but warns.
- **MySQL InnoDB**: redo log (`innodb_log_file_size`, `#innodb_redo`), `innodb_flush_log_at_trx_commit` (1/0/2), doublewrite buffer (writes pages twice for torn-page safety on some storage).
- **SQL Server**: transaction log with sequential I/O; `synchronous_commit`-equivalent (`... DELAYED_DURABILITY`), snapshot/buffer pool.
- **Oracle**: redo logs + `ARCHIVELOG`; log buffer; `COMMIT WRITE NOWAIT` as the weaker-durability dial.
- **RocksDB / LevelDB**: WAL + memtable; `WriteOptions::sync` maps to fsync-on-write.
- **MongoDB WiredTiger**: journal (WAL), `writeConcern` levels including `majority` for durability across replicas.

## 17. References
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 17.2 (storage structure) & 17.3 (stable storage).
- PostgreSQL docs: "Write-Ahead Logging (WAL)": https://www.postgresql.org/docs/current/wal-intro.html and "Reliability": https://www.postgresql.org/docs/current/wal-reliability.html
- MySQL 8.0 docs, InnoDB Redo Log: https://dev.mysql.com/doc/refman/8.0/en/innodb-redo-log.html
- Michael Stonebraker et al., "The End of an Architectural Era" (2007) — buffer-pool/fsync trade-offs.
- Linux man pages: fsync(2), fdatasync(2).

## 18. Cheat Sheet
- Hierarchy: registers → cache → RAM → page cache → disk; only disk survives power loss (and it can tear/corrupt).
- Stable storage = redundancy + atomic writes + checksums.
- Durability line = commit record fsync'd to WAL.
- write() ≠ durable; fsync() = durable.
- Torn pages: detect via checksums, fix via full_page_writes.
- Dirty pages → checkpoint flush; buffer pool is volatile.
- Group commit batches fsyncs; weakening it = bounded data-loss risk.
- RAID ≠ backup; checksums ≠ encryption; layers are complementary.

## 19. Quiz
1. Which is volatile? a) disk b) RAM c) RAID d) SSD → **b**
2. fsync guarantees: a) cache write b) durable disk write c) faster reads d) nothing → **b**
3. Stable storage needs: a) RAM b) redundancy + atomicity + checksums c) SSD only d) fsync only → **b**
4. A torn page is detected by: a) fsync b) checksums c) RAID d) vacuum → **b**
5. The durability line for a commit is: a) buffer pool write b) WAL fsync c) data page flush d) checkpoint → **b**
6. Group commit: a) groups transactions b) batches log fsyncs c) groups tables d) batches pages → **b**
7. `full_page_writes` protects against: a) lost updates b) torn pages c) deadlocks d) phantoms → **b**
8. RAID protects against: a) torn pages b) drive loss c) logical errors d) fsync lies → **b**

## 20. Flashcards
- **Q: Storage hierarchy top→bottom?** → **A:** Registers → cache → RAM → page cache → disk.
- **Q: What is stable storage?** → **A:** Non-volatile storage made trustworthy: redundancy + atomic writes + checksums.
- **Q: write() vs fsync()?** → **A:** write = page cache (volatile); fsync = forced to disk (durable).
- **Q: When is a commit durable?** → **A:** When its WAL record is fsync'd to stable storage.
- **Q: Torn page?** → **A:** Partially written page; detect with checksums, repair-safe with full-page images.
- **Q: What is group commit?** → **A:** Batching multiple transactions' log flushes into one fsync.
- **Q: Why is the log on stable storage?** → **A:** It's the source of truth recovery replays after a crash.
- **Q: RAID vs backup?** → **A:** RAID survives drive loss; backups survive logical/media disasters.

## 21. Revision
Data lives in volatile (RAM/caches) and non-volatile (disk) storage; durability means reaching stable storage — redundancy + atomic writes + checksums. `write()` hits the page cache; only `fsync` makes it durable. The commit record fsync'd to the WAL is the durability line; data pages flush lazily at checkpoints. Torn pages need checksums + full-page images. Group commit amortizes fsync cost. This storage model is *why* the WAL rules in Chapter 02 exist.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Why is write() not durable?" | 2, 3, 13 |
| "What is stable storage?" | 2, 7, 13 |
| "What is a torn page and how is it fixed?" | 9, 13 |
| "When is a commit durable?" | 8, 13 |
| "What is the buffer pool / dirty pages?" | 9, 14 |
| "Group commit / synchronous_commit?" | 9, 13, 16 |
| "RAID vs backup?" | 13, 16 |
| "full_page_writes?" | 9, 13 |
