# Undo, Redo, and Shadow Paging

> **TL;DR**: Undo reverses uncommitted work (before-images), redo re-applies committed work (after-images), and shadow paging was the no-log attempt to achieve atomicity by copy-on-write + pointer flip — which lost because logging is far cheaper.

## 1. Why Does This Exist?
A crash can leave the disk in three states for any transaction: (a) all its changes flushed, (b) none flushed, or (c) some flushed. To reconstruct a valid state you need two *directions*: **undo** (undo the effects of transactions that never committed — atomicity) and **redo** (re-apply the effects of committed transactions that never reached disk — durability). These two operations are the yin-and-yang of every recovery algorithm, and the log's before-images (undo) and after-images (redo) make both possible. **Shadow paging** exists as the historical counterproposal: achieve atomicity *without* a log by never overwriting pages (copy-on-write) and atomically swapping a page-table pointer at commit. Studying it explains *why* the industry converged on logging: shadow paging's elegance doesn't survive real workloads.

## 2. How Does It Work?
**Undo**: for each record of a failed transaction (scanning the log backward), write the before-image back to the page, restoring the pre-transaction state. When done, release locks; the transaction is "as if never ran."
**Redo**: for each record of a committed transaction (scanning forward), write the after-image to the page *if the page's current state predates the record* (LSN check) — idempotent re-application.
**Shadow paging**: maintain two page tables — the *current* table and a *shadow* table. Updates copy-on-write: a modified page goes to a new disk location; the current table is updated, the shadow table stays untouched. At commit: flush the current table to disk, then atomically flip a single "current = shadow" pointer in the root; the old shadow becomes the starting point of the next transaction. If the system crashes, the disk still points at the shadow table — the uncommitted changes are simply invisible; no undo needed, no log needed.

## 3. When Is It Used?
- **Undo**: every rollback and every crash-recovery undo pass. Postgres: undo via before-images and `CLR` records during ARIES-style recovery (and historically `UNDO` logs). InnoDB: undo is *the* mechanism for both rollback and MVCC snapshots (undo log serves both).
- **Redo**: every crash-recovery redo pass; every replication apply (standby replays = redo).
- **Shadow paging**: historically in some systems; its *descendants* survive — copy-on-write at the *file-system* level (ZFS, btrfs, CoW filesystems), and LSM/B-tree COW pages in some engines — but no major relational DBMS uses it for transaction recovery today.
- In interviews: "explain undo and redo", "why is shadow paging not used?", "what's the difference between logical and physical redo?"

## 4. Why Wasn't Another Approach Chosen?
- *Undo-only*: can't restore committed-but-lost work → violates durability.
- *Redo-only*: can't remove uncommitted-but-flushed work → violates atomicity.
- *Both, via a full page-image log*: correct but logs whole pages for every change — huge volume. Modern systems log *logical* changes (before/after images of the changed data) and full pages only after checkpoints (`full_page_writes`).
- *Shadow paging vs logging* — why logging won:
  1. **Commit cost**: shadow paging flushes *all* modified pages at commit (scattered writes) plus the page tables; logging flushes one small sequential log record. Logging's commit is far cheaper.
  2. **Data fragmentation**: every update moves the page (new location) → fragmentation and poor locality; logging keeps pages in place.
  3. **Garbage collection**: old shadow pages must be reclaimed (a second bookkeeping problem the log doesn't have).
  4. **Concurrency**: shadow paging needs the page-table root lock at commit — a global serialization point; logging's commit is per-transaction.
  5. **No incremental undo**: with shadow paging, a transaction that aborts mid-way has to either discard everything since the shadow or do expensive re-cloning; logs support partial/arbitrary rollback cleanly.
- *State-machine/redo-only journal (like some NoSQL, e.g., MongoDB journal in some modes)*: works when "committed = redo applied at replay," but doesn't handle undo of in-flight operations without extra structures.

## 5. Intuition
Undo is **un-typing**: you wrote words (before-images), so you can erase them back to the pre-word state. Redo is **re-typing**: you recorded the words you *intended* to write (after-images), so you can re-enter them if the page got lost. Shadow paging is a **whiteboard with a sheet on top**: you never erase the real board — you write on the overlay (COW pages); when you're happy (commit), you flip the board over (pointer swap) so the overlay becomes the visible one. If you're not happy, you just throw the overlay away — no erasing. Elegant! But flipping the whole board means *every* change rewrites the overlay stack (all dirty pages + tables) at commit — expensive, which is why real DBs chose typing (logging) over overlays.

## 6. Real-World Analogy
**Legal contracts**: Undo = crossing out clauses with white-out (before-image) — you can restore the original text. Redo = carbon copies (after-images) — if the final contract is lost, you reprint from the carbon. Shadow paging = a **notary with two notepads**: the "official" notepad is only ever updated by swapping in a new complete copy you built in secret. No white-out needed, but every notarization means recopying the entire book — and that's why notaries instead keep a log (recording each change) and a proper archive. Two notepads look safe but cost too much per page of work.

## 7. Formal Definition
- **Undo**: the recovery process that restores a data item to its state before a transaction began, using the before-image recorded in the log: `page = before_image`. Applied to transactions whose commit record is absent from the log.
- **Redo**: the recovery process that re-applies the after-image of a change to a data item whose on-disk state predates the change, using the LSN/pageLSN comparison to avoid double application: `page = after_image` if `pageLSN < record.LSN`. Applied to transactions whose commit record is present.
- **Shadow paging**: the database is represented by a page table (array of pointers to disk pages). A transaction copies pages on write (COW) and updates the *current* page table; at commit the current table is made durable and the root pointer is atomically switched so the current table becomes the new base (shadow). Crash ⇒ disk still references the old shadow table ⇒ uncommitted changes are simply absent — no undo log is required. Atomicity is achieved via the single root-pointer update.
- **Idempotency**: redo/undo must be repeatable (crash during recovery) — hence LSN comparisons and the recording of per-operation state, not just end-state.

## 8. Example
Transaction T: `UPDATE accounts SET balance=balance-50 WHERE id=1` (balance 100 → 50), then crash.
Log: `⟨T start⟩, ⟨T, A(1), before=100, after=50⟩, [crash]`.

**Redo path** (T had committed): recovery sees the commit record, replays after-image: writes `A(1)=50` to any page whose `pageLSN < record LSN`. If the page already has 50 (flushed), the LSN check skips it → idempotent. Final: balance=50. ✓
**Undo path** (T not committed): recovery sees no commit record, restores before-image: writes `A(1)=100`. Even if the page had 50 on disk, it's set back to 100. Final: balance=100. ✓

**Shadow paging**: the DB's root page table has pointers `[P1, P2]`. T updates page P1: allocates P1' (copy of P1), writes `balance=50` into P1', updates the *current* table to point at P1'. Commit: flush current table + root. Crash before the root flip: disk still references the shadow table with `[P1, P2]` → balance=100 (T invisible) — no undo needed. Crash after root flip: `[P1', P2]` → balance=50 — T committed. Same guarantee, but T's commit flushed a whole page + the table, and P1' is garbage to be reclaimed.

## 9. Internal Working
1. **Undo pass**: scan the log backward; for each record of an uncommitted transaction, restore the before-image; write a `CLR` (compensation log record) when redoing an undo so repeated undo is safe (ARIES, Section 04).
2. **Redo pass**: scan forward; for committed transactions, apply after-images with LSN checks; because of idempotency, recovery can crash again mid-recovery and simply re-run.
3. **Shadow paging internals**: (a) COW on each modified page; (b) in-memory current page table, shadow table on disk; (c) commit = fsync dirty pages + tables + root; (d) crash ⇒ shadow table used; (e) GC of abandoned pages (the "old shadow" pages are unreachable — collected lazily or at checkpoint).
4. Modern engines mostly implement undo/redo inside WAL (ARIES), using physical page changes (with logical undo for index/page splits in ARIES) — the "shadow" idea survives mainly in CoW filesystems and LSM-tree compaction.

## 10. Time Complexity
- Undo: O(records of failed transactions) — bounded by their write sets.
- Redo: O(log records since redo point) — bounded by the checkpoint.
- Both are idempotent; each record applied O(1) with an LSN check.
- Shadow paging commit: O(#dirty pages + #pages in page tables) *fsync'd at commit* — the fatal cost compared to logging's O(1) log record. Plus O(garbage pages) for reclamation.
- Logging total: O(1 log write per change + 1 fsync per commit group).

## 11. Advantages
- **Undo/redo (logging)**: cheap sequential commit; arbitrary partial rollback; supports concurrency without a global commit lock; WAL doubles as replication/PITR input; idempotent and crash-during-recovery-safe.
- **Shadow paging**: no log = no log replay; atomicity is a pointer flip; crash leaves a *valid* prior state instantly (fast, simple recovery); pages never half-updated in place.

## 12. Disadvantages
- **Undo/redo (logging)**: log I/O bottleneck at high TPS; log volume/bloat; recovery time depends on log length; WAL correctness complexity (ordering, torn records, full-page images).
- **Shadow paging**: expensive commits (all dirty pages + tables flushed); fragmentation/locality loss; garbage collection overhead; global page-table root contention at commit; no cheap incremental undo of sub-transactions; complex page-table persistence — the reasons it lost.

## 13. Interview Questions
1. **Q: What is undo and what does it use?** A: Undo restores data to its pre-transaction state using the before-image from the log. It's applied to transactions that never committed (their effects must vanish — atomicity). Done by scanning the log backward.
2. **Q: What is redo and what does it use?** A: Redo re-applies committed changes using the after-image from the log — for transactions whose commit record is present but whose data pages may not have reached disk (durability). Done scanning forward, with LSN checks for idempotency.
3. **Q: Why must recovery be idempotent?** A: The system can crash *during* recovery. If redo/undo isn't repeatable, a second recovery could double-apply or mis-apply changes. LSN/pageLSN checks and compensation records (CLRs) guarantee applying a record twice is harmless.
4. **Q: What is shadow paging?** A: A no-log atomicity technique: copy pages on write (COW), maintain a current page table and a shadow table; at commit, atomically flip the root pointer from shadow to current. A crash before the flip leaves the DB at the old shadow state — no undo needed.
5. **Q: Why isn't shadow paging used in production DBMSes?** A: Commit is expensive (flush all dirty pages + page tables + root), pages fragment and lose locality, abandoned pages need garbage collection, and commit needs a global root lock — versus logging's one small sequential record per commit. Logging wins on every axis that matters.
6. **Q: TRICKY: Does shadow paging eliminate the need for the WAL entirely?** A: For transaction atomicity — yes, in theory. But it still needs *some* durable ordering (the page tables and root), and it can't produce the cheap log that replication and PITR need. So even COW systems keep logs for other purposes.
7. **Q: What is a CLR (compensation log record)?** A: A record written when an undo action is performed, describing the *undo* of an undo. It makes recovery crash-safe during the undo pass (a crash mid-undo must not redo the original change). ARIES uses CLRs.
8. **Q: What's the difference between physical and logical redo?** A: Physical redo applies to the exact page/offset (fast, idempotent) but breaks if pages move. Logical redo (used by ARIES for some operations, e.g., page splits) re-executes an operation semantically — necessary when physical structure changed during the transaction. Most engines redo physically and undo logically where needed.
9. **Q: PR: In Postgres, how is undo performed during recovery?** A: Postgres uses a WAL-driven ARIES-style scheme: committed transactions are redone; uncommitted changes are undone using the log's before-images (and `CLOG`/hint bits for status). Long transactions have their undo done transaction-by-transaction at recovery, which is why long-running transactions slow crash recovery.
10. **Q: How does InnoDB use undo differently from Postgres?** A: InnoDB's undo log serves *both* rollback and MVCC: it stores before-images so old snapshots can reconstruct versions (not just crash recovery). Postgres stores versions in the table (MVCC) and uses WAL for crash recovery — the undo path differs because the versioning strategy differs.
11. **Q: TRICKY: Can redo be applied to a torn page?** A: Only safely with a full-page image: if the page is torn, incremental redo would be applied to garbage. That's exactly why `full_page_writes` logs the entire page after checkpoints — redo then starts from a known-good full image.
12. **Q: Why do we redo before undo (ARIES order)?** A: Redo (forward) restores all pages to their state *as of the last log record* (replaying committed work); undo (backward) then removes uncommitted work. Doing redo first means undo operates on the fully-redone (correct) page state. Also, redo is idempotent and cheap; undo needs the redo'd state to apply before-images meaningfully.
13. **Q: What is the difference between undo at abort and undo at crash?** A: At abort (transaction failure), undo is straightforward (walk the transaction's undo records; no concurrency issues because it's the only writer). At crash, multiple transactions' undo records interleave in the log — recovery must disentangle them by transaction and honor commit status (which is where ARIES's analysis phase comes in).
14. **Q: PRODUCTION: Why does a long-running transaction slow down crash recovery?** A: Recovery must undo its *entire* write set (all its before-images) and it may have dirtied pages late in the log; also it prevented checkpoints from being clean. Keeping transactions short is a recovery-time best practice.

## 14. Follow-Up Questions
1. **Q: What is "logical undo" vs "physical undo"?** A: Physical undo restores a page's bytes (fast, but structure-dependent); logical undo re-executes inverse operations (needed when a page split or index node moved). ARIES uses physical redo + logical undo for complex structures.
2. **Q: How do CoW filesystems relate to shadow paging?** A: ZFS/btrfs snapshot filesystems implement shadow-paging *at the filesystem layer* (COW blocks + atomic metadata update) — proving the idea works, but at a different layer with different cost model. Databases prefer the log.
3. **Q: What is the difference between shadow paging and MVCC?** A: Both keep old versions, but MVCC keeps them *for concurrent readers* (isolation), not for atomic commit; MVCC still relies on the WAL for durability/recovery. They solve different problems with similar-looking mechanisms.

## 15. Coding Example
```pseudocode
// Undo/redo skeleton with LSN idempotency
function redo(record r):
    if page(r.item).pageLSN < r.lsn:          // stale page → apply
        write_page(r.item, r.after_image)
        page(r.item).pageLSN = r.lsn

function undo(record r, txid):
    page(r.item).write(r.before_image)         // restore prior state
    append_log(CLR(txid, r.item, r.before_image, current_lsn))  // crash-safe undo
```
```sql
-- Postgres: observe recovery activity in the log
SELECT * FROM pg_stat_bgwriter;                -- checkpoint + background writer stats
-- A crash trigger and recovery are visible in the server log:
-- "database system was interrupted; last known up at ..."
-- "database system was not properly shut down; automatic recovery in progress"
-- "redo starts at 0/xxxxxx; redo done at ..."  (shows the redo pass)
```
```bash
pg_waldump -p $PGDATA/pg_wal/ | head -20   # see the actual log records (LSNs, before/after)
```

## 16. Industry Usage
- **PostgreSQL**: ARIES-style WAL recovery — redo committed, undo uncommitted, `CLOG` for status, `full_page_writes`, `pg_waldump` for inspection. Undo of uncommitted work is visible in crash-recovery logs.
- **MySQL InnoDB**: redo log for crash recovery (physical redo), undo log for rollback + MVCC (logical undo/reconstruction).
- **SQL Server**: transaction log + ARIES (SQL Server is a direct ARIES descendant); `RESTORE` with `STOPAT` (PITR).
- **Oracle**: redo + undo (rollback segments); `UNDO_MANAGEMENT=AUTO`; flashback uses undo.
- **Shadow-paging descendants**: CoW filesystems (ZFS/btrfs), some LSM engines' page COW, and file-level snapshot tools — but no major relational engine.

## 17. References
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 17.4 (undo/redo with deferred/immediate update) & 17.6 (shadow paging).
- Elmasri & Navathe, Ch. 22 (recovery).
- Mohan et al., "ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging", IBM 1992 — the definitive undo/redo treatment.
- Gray & Reuter, *Transaction Processing: Concepts and Techniques* (1993) — shadow paging analysis (Ch. 9).
- PostgreSQL docs, "Crash Recovery": https://www.postgresql.org/docs/current/wal-intro.html

## 18. Cheat Sheet
- Undo = before-images, backward, for uncommitted transactions (atomicity).
- Redo = after-images, forward, for committed transactions (durability).
- Idempotency via LSN/pageLSN checks + CLRs (crash-during-recovery safety).
- Redo before undo (ARIES order).
- Full-page writes make redo safe against torn pages.
- Shadow paging = COW pages + atomic root flip; no log, but expensive commit, fragmentation, GC, root contention → lost.
- InnoDB undo serves rollback *and* MVCC; Postgres versions in-table + WAL for recovery.
- Long transactions slow recovery (bigger undo).
- CoW filesystems are shadow-paging descendants at another layer.

## 19. Quiz
1. Undo uses: a) after-images b) before-images c) LSN only d) none → **b**
2. Redo uses: a) before-images b) after-images c) CLRs d) shadow → **b**
3. Undo applies to: a) committed transactions b) uncommitted transactions c) all d) none → **b**
4. Redo applies to: a) uncommitted b) committed c) all d) none → **b**
5. Shadow paging achieves atomicity via: a) log replay b) COW + root pointer flip c) fsync d) locks → **b**
6. Why did logging beat shadow paging? a) better atomicity b) cheaper commit c) less code d) faster reads → **b**
7. A CLR is written to make: a) redo idempotent b) undo crash-safe c) commits faster d) locks safer → **b**
8. Correct recovery order: a) undo then redo b) redo then undo c) arbitrary d) parallel → **b**

## 20. Flashcards
- **Q: Undo vs redo?** → **A:** Undo = before-images for uncommitted; redo = after-images for committed.
- **Q: Why idempotent recovery?** → **A:** The system can crash during recovery; re-applying must be harmless (LSN checks + CLRs).
- **Q: What is shadow paging?** → **A:** COW pages + atomic page-table root flip at commit — atomicity without a log.
- **Q: Why did shadow paging lose?** → **A:** Expensive commit (flush all dirty pages + tables), fragmentation, GC, global root lock.
- **Q: What is a CLR?** → **A:** Compensation log record — records an undo's action so a crash mid-undo is safe.
- **Q: Recovery order?** → **A:** Redo (forward) first, then undo (backward).
- **Q: When does redo need a full-page image?** → **A:** After a checkpoint (torn-page safety).
- **Q: What's special about InnoDB undo?** → **A:** Serves rollback AND MVCC (reconstructs old versions).

## 21. Revision
Undo (before-images, backward, uncommitted) restores atomicity; redo (after-images, forward, committed) restores durability. Recovery is idempotent (LSN checks, CLRs), ordered redo-then-undo, and safe against torn pages via full-page images. Shadow paging (COW + root flip) achieves atomicity without a log but lost on commit cost, fragmentation, GC, and root contention. InnoDB's undo doubles for MVCC; Postgres relies on WAL + in-table versions. This sets up ARIES (Section 04), which formalizes all of it.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Explain undo and redo." | 1, 2, 7 |
| "Why must recovery be idempotent?" | 7, 9, 13 |
| "What is shadow paging and why did it lose?" | 2, 7, 13 |
| "What is a CLR?" | 9, 13 |
| "Why redo before undo?" | 13, 18 |
| "Physical vs logical redo?" | 13, 14 |
| "Why do long transactions slow recovery?" | 13, 16 |
| "InnoDB undo vs Postgres undo?" | 13, 16 |
