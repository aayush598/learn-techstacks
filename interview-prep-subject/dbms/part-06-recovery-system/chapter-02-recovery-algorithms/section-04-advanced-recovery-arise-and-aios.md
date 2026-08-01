# Advanced Recovery: ARIES and AIOS

> **TL;DR**: ARIES (Algorithm for Recovery and Isolation Exploiting Semantics) is the industry-standard recovery algorithm — built on WAL, LSNs, a dirty-page table, and a three-phase recovery (Analysis → Redo → Undo) — and its ideas (sometimes labeled the "AIOS"-family of ARIES-style algorithms) power Postgres, MySQL, SQL Server, and most modern engines.

## 1. Why Does This Exist?
Before ARIES, recovery algorithms made blunt simplifying assumptions: redo-then-undo, or undo-then-redo, with no way to handle *partial* rollbacks, *long* transactions that span checkpoints, *pages split during a transaction*, or *recovery that crashes mid-recovery*. ARIES exists to make recovery (a) **fast**: recovery work is proportional to the *transactions that were active*, not to the whole log; (b) **correct**: works with fine-grained locking, partial rollbacks, and logical operations on indexes; (c) **idempotent**: recovery can crash repeatedly and still converge. It's the resolution of the undo/redo tangle (Section 03) into one rigorous, provable algorithm — and it's what "production-grade recovery" means.

## 2. How Does It Work?
Core structures: each log record has an **LSN**; each page stores its **pageLSN** (last LSN applied to it); the **Dirty Page Table (DPT)** records every dirty page and the LSN of the first record that dirtied it (its `RecLSN`); each transaction's last log record is tracked (a **transaction table** maps txid → last LSN). Key log records: normal change records, `COMMIT`/`ABORT`, **compensation log records (CLR)** for undo, and **checkpoints** (which store the DPT + transaction table).
Recovery = three phases:
1. **Analysis** (forward from the last checkpoint): reconstruct the transaction table (which transactions were active) and the DPT (which pages may be dirty). Determines the **redo start point** = minimum `RecLSN` in the DPT.
2. **Redo** (forward from the redo start): re-apply every change whose LSN > the page's pageLSN — restoring all pages to the state of the last log record, exactly once (idempotent).
3. **Undo** (backward from the end): roll back all *active* transactions (those that never committed), in LSN order; write a **CLR** before each undo so a crash mid-undo resumes correctly instead of redoing.

## 3. When Is It Used?
- **Every major engine**: Postgres's WAL-based crash recovery, InnoDB's redo/undo, SQL Server (a direct ARIES descendant — the docs literally cite ARIES), Oracle's redo-based recovery — all implement the ARIES architecture.
- **Partial rollback**: ARIES supports `ROLLBACK TO SAVEPOINT` and aborting a sub-operation while keeping the transaction — via CLRs and the LSN chain.
- **Recovery during recovery**: the idempotency guarantees that a crash in the middle of the Analysis/Redo/Undo phases just restarts cleanly.
- In interviews: "explain ARIES's three phases", "what is an LSN?", "what is the dirty page table?", "what is a CLR?", "how does Postgres do crash recovery?"

## 4. Why Wasn't Another Approach Chosen?
- *Undo-then-redo*: requires redo to start from the very beginning (undoing may clobber committed work), making recovery slow and wrong for long logs. ARIES redo-first restores the log-tail state, then undoes only *active* transactions.
- *Redo everything, undo everything (no filtering)*: wastes work replaying committed transactions that are already on disk; the DPT + transaction table make recovery proportional to *active* work.
- *Ignore partial rollbacks (assume all-or-nothing per transaction)*: incompatible with savepoints and with aborting part of a complex operation; ARIES's CLR machinery handles arbitrary rollback scope.
- *Physical-only undo*: can't handle index pages that split/moved during a transaction — ARIES uses *logical* undo for such operations (undo the *operation*, not the byte), and physical redo for idempotency.
- *Shadow paging (Section 03)*: no log, but commit cost, fragmentation, GC, and no incremental rollback — ARIES + WAL is the strict improvement.
- *No recovery (MyISAM-era)*: corrupted tables after crashes — universally rejected for production.

## 5. Intuition
ARIES is a **forensic accountant reconstructing a ledger after a fire**. Phase 1 (Analysis) = "figure out what books were open when the fire started" (transaction table) and "which pages might have been half-worked" (dirty page table) — so you know where to start. Phase 2 (Redo) = "re-write every entry that a completed (committed) book says happened, but only if the page doesn't already have it" (LSN comparison) — the books get their true final state. Phase 3 (Undo) = "tear out the entries of books that were never closed (uncommitted)" — and before each tear-out you *note it in a memo* (CLR) so if the building catches fire again mid-cleanup, you don't redo a torn-out entry. The result is provably the state "all committed, none uncommitted" — no matter how many times the fire interrupts.

## 6. Real-World Analogy
**A GPS navigation system re-plotting after you miss a turn** (log = your route; recovery = re-route): Analysis = "where am I and which segments were I driving on?" (active state + dirty roads); Redo = "advance along every confirmed (committed) stretch I haven't yet traversed, skipping already-passed ones" (LSN check); Undo = "cancel the waypoints of routes I never confirmed," and the route recorder logs each cancellation so re-plotting after another detour doesn't resurrect them. GPS systems are *designed to be interrupted and re-planned* — exactly ARIES's design goal.

## 7. Formal Definition
**ARIES** (Mohan, Haderle, Lindsay, Pirahesh, Schwarz, 1992): a recovery method using **Write-Ahead Logging** with **redo/undo based on LSNs**, supporting **fine-grained locking**, **partial rollbacks**, and **logical undo of structure-modifying operations**. Principles:
1. **WAL**: log records (with LSNs) are written before pages are written to disk; commit requires the commit record flushed.
2. **Repeating history during redo**: redo re-applies *all* log records from the redo start point, re-creating the exact state of the database at the end of the log.
3. **Logging changes during undo**: every undo action is itself logged (CLR), making undo resumable/idempotent.
Recovery phases:
- **Analysis**: scan forward from the checkpoint, rebuilding the transaction table (active transactions, lastLSN) and DPT (page → RecLSN). Redo point = min(RecLSN in DPT).
- **Redo**: scan forward from the redo point; apply record r to page P if `r.LSN > P.pageLSN` (i.e., P hasn't seen it yet). Set `P.pageLSN = r.LSN`.
- **Undo**: process active transactions backward by lastLSN; for each change record, undo it and write a CLR (with an `UndoNextLSN` pointing to the next record to undo). Continue via CLR chains until every active transaction is rolled back; write `ABORT`/end records.

## 8. Example
Log (LSNs in order): `[10: <T1 begin>], [20: <T1 update P5, before=100, after=50>], [30: <T2 begin>], [40: <T2 update P9, before=7, after=8>], [50: <T1 commit>], [60: <T2 update P5, before=50, after=0>]`. Crash.
Checkpoint at LSN 10 (DPT empty, both transactions active? no — checkpoint taken at 10, T1 just began; assume checkpoint DPT tracks nothing). Recovery:
1. **Analysis** from 10: transaction table = {T1 active, lastLSN=20; T2 active, lastLSN=60}. DPT = {P5 → RecLSN 20; P9 → RecLSN 40}. Redo point = min(20,40) = 20.
2. **Redo** from 20: apply LSN 20 to P5 (if P5.pageLSN < 20); apply 40 to P9; apply 60 to P5 (pageLSN now ≥ 60). End state: P5 = 0, P9 = 8 — exactly the log tail.
3. **Undo** (active = T2 only — T1 committed at 50): backward from T2.lastLSN=60: undo record 60 (P5 = 50, CLR written with UndoNextLSN=40); then record 40 (P9 = 7, CLR). T2 rolled back. T1's committed state (P5=50) — wait: undo of 60 restored P5 to 50, which is T1's committed after-image — correct! Final: P5=50 (T1 committed), P9=7 (T2 undone). ✓ (Note how redo-then-undo makes this trivially correct: undo restores to the *last committed* state.)

## 9. Internal Working
1. **Normal operation**: every change writes a log record (with LSN, txid, page id, before/after images) and updates pageLSN; checkpoints periodically write DPT + transaction table.
2. **Analysis**: re-read the checkpoint, then scan forward applying the *effects on metadata*: BEGIN → add to transaction table; COMMIT/ABORT → mark/remove; each change → add page to DPT with RecLSN (first occurrence). End: active set + redo point.
3. **Redo**: forward scan; the DPT tells you which pages might be dirty (others skipped); pageLSN comparison makes re-application idempotent (crash-safe).
4. **Undo**: build the undo list from active transactions' lastLSN chains; process records in descending LSN; before each undo, write a CLR {txid, page, before-image, UndoNextLSN}; after the CLR, apply the before-image. On a second recovery, the CLR's UndoNextLSN resumes where it left off (no redo of undone changes).
5. **Commit record handling**: the commit record is the durability line; redo only applies to committed transactions (commit record present or inferred via CLR/ABORT status).

## 10. Time Complexity
- **Analysis**: O(log records since last checkpoint) + O(DPT rebuild).
- **Redo**: O(records from redo point) — typically O(active window), *not* O(total log).
- **Undo**: O(records of active transactions) — proportional to *uncommitted* work.
- Total recovery ≈ O(active transaction work + log since last checkpoint). With checkpoints every 5 minutes, typical crash recovery is seconds-to-minutes even for huge databases.
- Per-record overhead: O(1) LSN compare/apply; DPT in memory O(dirty pages).

## 11. Advantages
- **Fast**: recovery proportional to active work, not total log (DPT + transaction table filtering).
- **Correct under concurrency**: works with fine-grained locking, savepoints, partial rollbacks.
- **Idempotent**: safe against crashes *during recovery* (pageLSN + CLRs).
- **Logical undo**: handles structure changes (B-tree splits) that physical undo can't.
- **Proven, standard**: the architecture behind Postgres/MySQL/SQL Server/Oracle — a transferable answer.
- **Replay serves replication/PITR**: the same redo machinery runs standbys and archive recovery.

## 12. Disadvantages
- **Complex**: LSN/pageLSN/CLR/DPT/transaction-table bookkeeping is intricate; bugs are catastrophic.
- **Log volume**: logical redo + full-page images inflate the log (mitigated by compression, `full_page_writes` controls).
- **Recovery still needs the log**: ARIES assumes WAL; a lost/corrupt log means you fall back to backup (media-failure class).
- **Undo of long transactions is slow**: recovery undoes all active work; a long transaction's write set costs recovery time.
- **Not "instant"**: recovery time is bounded but not zero; high-availability systems mitigate with replicas/failover rather than faster local recovery.

## 13. Interview Questions
1. **Q: What is ARIES?** A: The industry-standard recovery algorithm (Mohan et al., 1992): WAL + LSNs + a dirty-page table + a transaction table, with recovery in three phases — Analysis, Redo, Undo. It supports fine-grained locking, partial rollbacks, and logical undo.
2. **Q: What are the three phases of ARIES recovery?** A: **Analysis** (reconstruct active transactions + dirty pages from the checkpoint; find the redo point = min RecLSN), **Redo** (re-apply all changes from the redo point using LSN comparisons, restoring the log-tail state), **Undo** (roll back all uncommitted transactions backward, logging a CLR before each undo).
3. **Q: What is an LSN and how is it used?** A: A monotonic log sequence number on every record and page (pageLSN). It orders records, detects "has this page already seen this change?" (apply if r.LSN > page.pageLSN), and defines the redo point.
4. **Q: What is the Dirty Page Table (DPT)?** A: The set of pages modified in the buffer pool but not yet flushed, each with its **RecLSN** (the LSN of the first record that dirtied it). Recovery uses it to (a) compute the redo start point (min RecLSN) and (b) skip redo for pages known clean.
5. **Q: What is a CLR and why is it needed?** A: A Compensation Log Record written before each undo action, containing the before-image and an `UndoNextLSN` (where undo resumes). If recovery crashes mid-undo, the CLR ensures the undone change is not redone and undo resumes correctly — making undo idempotent.
6. **Q: Why does ARIES redo before undo?** A: Redo restores every page to its state at the end of the log (including committed work); undo then removes only *uncommitted* work from that correct state. Undoing first could clobber committed changes that redo would need.
7. **Q: TRICKY: How does ARIES handle a transaction that did 3 writes and aborted, then the system crashed?** A: Normal abort already rolled it back (with CLRs). If it aborted *because of* the crash, it's an active transaction at recovery: Analysis puts it in the transaction table, Redo may re-apply its (uncommitted) writes — that's fine — and Undo rolls them back using before-images + CLRs.
8. **Q: What is the difference between ARIES's redo and a simple "replay all committed transactions"?** A: ARIES redoes *every* change from the redo point (even uncommitted ones) to faithfully reproduce the log-tail state, then undoes uncommitted work. Filtering redo to only-committed would leave pages inconsistent because a committed transaction might depend on earlier structure the log captured only as uncommitted changes.
9. **Q: How does ARIES support savepoints/partial rollback?** A: Rollback to a savepoint undoes only the records after the savepoint's LSN; each undo writes a CLR, so the transaction continues with correct state (the CLR chain is the "logical tail" of the transaction). This is why apps can `SAVEPOINT`/`ROLLBACK TO` reliably.
10. **Q: PR: How does Postgres's crash recovery map to ARIES?** A: Postgres implements a WAL-based ARIES-style recovery: startup reads the control-file checkpoint (Analysis-like: loads DPT/transaction info), replays `pg_wal` from the redo point (Redo, using pageLSN comparisons), then undoes uncommitted transactions using the log's before-images; `CLOG`/hint bits track commit status. The server log shows "redo starts at ..." / "redo done at ...".
11. **Q: How does InnoDB map to ARIES?** A: Redo log = physical redo; undo log = logical undo; recovery scans redo forward, then rolls back via undo; checkpoint LSNs bound it. Same ARIES skeleton with a different physical layout (doublewrite, redo groups).
12. **Q: What is "repeating history"?** A: ARIES's principle that redo must reproduce the exact sequence of changes (the log's history), including uncommitted ones, so the subsequent undo has a well-defined, correct base state — rather than trying to skip uncommitted work during redo.
13. **Q: TRICKY: What happens if the DPT/transaction table at the checkpoint is lost?** A: ARIES handles it: if no valid checkpoint exists, Analysis treats the whole log as the window (DPT empty, so redo point = start of log). Recovery still converges — just slower. That's why "checkpoint lost" degrades performance, not correctness.
14. **Q: Why can't you use physical undo for B-tree operations?** A: A B-tree page may have split or its contents moved during the transaction — the bytes you'd restore no longer correspond to a valid tree. Logical undo re-executes the *inverse operation* (e.g., merge/unsplit) on the current structure. ARIES therefore uses physical redo + logical undo where structures change.
15. **Q: PR: How does "crash during recovery" stay safe?** A: Idempotency: redo re-checks pageLSN, undo re-checks CLRs. If the DB crashes mid-recovery, the next recovery re-runs Analysis from the same checkpoint, redo skips already-applied records (pageLSN), and undo resumes from the last CLR's UndoNextLSN. Every phase is restartable.
16. **Q: What is the difference between ARIES and "ARIES-style" algorithms used elsewhere?** A: ARIES is the original 1992 algorithm; "ARIES-family" (sometimes abbreviated in practice as the "AIOS"/ARIES-like class of algorithms — *Algorithms for Recovery and Isolation Exploiting Semantics*) share its core: WAL + LSNs + DPT + CLRs + three-phase recovery. Engines implement variants tuned to their storage (Postgres, InnoDB, SQL Server all differ in detail, all ARIES in spirit).

## 14. Follow-Up Questions
1. **Q: What is the relationship between ARIES and checkpoints?** A: Checkpoints in ARIES store the DPT + transaction table so Analysis starts there; the redo point comes from the DPT's min RecLSN. ARIES checkpoints are *fuzzy* (don't stop the system).
2. **Q: How does ARIES interact with strict 2PL?** A: Strict 2PL ensures a transaction's writes aren't visible until commit — so redo/undo decisions align cleanly with commit status; ARIES was designed to work *with* locking (fine-grained) and is safe under any scheduler that produces recoverable schedules.
3. **Q: What's the difference between ARIES and the log-structured storage in LSM trees?** A: LSM stores are *write-optimized* (logs become the data); ARIES is a *recovery* algorithm layered on any storage. They coexist: RocksDB uses WAL (ARIES-like semantics) on top of an LSM layout.

## 15. Coding Example
```pseudocode
// ARIES recovery skeleton
function recover():
    checkpoint = read_last_checkpoint()
    tx_table, dpt = {}, {}
    // Phase 1: Analysis (forward from checkpoint)
    for rec in log_from(checkpoint.lsn):
        if rec.type == BEGIN:  tx_table[rec.txid] = {lastLSN: rec.lsn, active: True}
        if rec.type in (COMMIT, ABORT): tx_table[rec.txid].active = False
        if rec.type == UPDATE: dpt.setdefault(rec.page, rec.lsn)   # RecLSN = first
    redo_point = min(dpt.values()) or checkpoint.lsn
    // Phase 2: Redo (forward from redo_point)
    for rec in log_from(redo_point):
        if rec.type == UPDATE and page(rec.page).pageLSN < rec.lsn:
            page(rec.page).write(rec.after_image); page(rec.page).pageLSN = rec.lsn
    // Phase 3: Undo (backward over active transactions)
    undo_stack = [t.lastLSN for t in tx_table if t.active]
    while undo_stack:
        lsn = pop_max(undo_stack); rec = log(lsn)
        if rec.type == UPDATE:
            write_log(CLR(txid=rec.txid, page=rec.page, before=rec.before, UndoNextLSN=prev(rec)))
            page(rec.page).write(rec.before_image)
        if rec.has_prev(): undo_stack.push(rec.prev_lsn)
```
```sql
-- Postgres: see recovery phases in action (server log excerpts)
-- "redo starts at 0/2E00000"        ← Analysis found the redo point
-- "redo done at 0/2F01234"          ← Redo phase completed
-- "database system is ready to accept connections"
```
```bash
pg_controldata $PGDATA | grep -i -E "checkpoint|state"   # checkpoint LSNs + shutdown state
```

## 16. Industry Usage
- **SQL Server**: directly documented as ARIES-based recovery; LSNs, dirty-page tracking, and CLR-style compensation are core.
- **PostgreSQL**: ARIES-inspired WAL recovery (redo-then-undo, LSN/pageLSN, CLOG for commit status, fuzzy checkpoints).
- **MySQL InnoDB**: ARIES-style with physical redo + logical undo; doublewrite buffer for torn pages.
- **Oracle**: redo-based recovery with SCN (a system change number — the Oracle equivalent of LSN) + undo segments.
- **CockroachDB/TiDB**: ARIES ideas extended to distributed logs (Raft) — each replica recovers via the replicated log.
- **NoSQL (RocksDB, MongoDB WiredTiger)**: WAL with LSN/journal replay — ARIES principles in LSM/store form.

## 17. References
- Mohan, Haderle, Lindsay, Pirahesh, Schwarz, "ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging", IBM Research Report RJ 6649, 1992.
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 17.5 (recovery) & 17.8 (additional recovery techniques).
- Elmasri & Navathe, Ch. 22.
- PostgreSQL docs, "Crash Recovery": https://www.postgresql.org/docs/current/wal-intro.html
- SQL Server docs on ARIES: https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-log-architecture-and-management-guide
- Gray & Reuter, *Transaction Processing: Concepts and Techniques* (1993).

## 18. Cheat Sheet
- ARIES = WAL + LSNs + DPT + transaction table + CLRs + 3-phase recovery.
- Phases: Analysis (rebuild active txns + DPT; find redo point) → Redo (apply forward, LSN-checked, idempotent) → Undo (roll back active txns backward, CLR-logged).
- LSN: sequence number on records & pages (pageLSN); apply only if record.LSN > page.pageLSN.
- DPT: dirty pages with RecLSN; min RecLSN = redo point.
- CLR: logged undo action (before-image + UndoNextLSN) → crash-safe, resumable undo.
- "Repeating history": redo all changes (even uncommitted) so undo starts from a correct state.
- Redo-first then undo; physical redo + logical undo for structure changes.
- Fuzzy checkpoints store DPT + tx table; lost checkpoint → slower but still correct.
- Powers: SQL Server (direct), Postgres, InnoDB, Oracle (SCN), RocksDB/MongoDB (WAL).

## 19. Quiz
1. ARIES's three phases in order: a) Undo, Redo, Analysis b) Analysis, Redo, Undo c) Redo, Analysis, Undo d) Analysis, Undo, Redo → **b**
2. The redo point comes from: a) the oldest log record b) min RecLSN in the DPT c) the commit record d) the CLR → **b**
3. A CLR records: a) the redo action b) an undo action with UndoNextLSN c) a checkpoint d) a commit → **b**
4. Redo applies a record if: a) r.LSN > page.pageLSN b) r.LSN < page.pageLSN c) equal d) always → **a**
5. "Repeating history" means redo applies: a) only committed changes b) all changes from redo point c) only uncommitted d) none → **b**
6. ARIES is used by: a) SQL Server b) Postgres c) InnoDB d) all of these → **d**
7. If a checkpoint is lost: a) recovery fails b) recovery is slower but correct c) data lost d) must restore → **b**
8. Partial rollback uses: a) DPT b) CLR chains c) shadow pages d) WAL only → **b**

## 20. Flashcards
- **Q: ARIES three phases?** → **A:** Analysis (rebuild tx table + DPT) → Redo (apply forward) → Undo (roll back active, CLR-logged).
- **Q: What is an LSN / pageLSN?** → **A:** Monotonic sequence on log records and pages; apply redo only when record.LSN > page.pageLSN.
- **Q: What is the DPT?** → **A:** Dirty pages with RecLSN (first LSN that dirtied them); min RecLSN = redo point.
- **Q: What is a CLR?** → **A:** Compensation log record: logs an undo (before-image + UndoNextLSN) so recovery is crash-safe/resumable.
- **Q: Why redo before undo?** → **A:** Redo restores the true log-tail state (incl. uncommitted); undo then cleanly removes uncommitted work.
- **Q: What does "repeating history" mean?** → **A:** Redo all changes from the redo point, even uncommitted ones — giving undo a correct base.
- **Q: Why logical undo for B-trees?** → **A:** Pages split/move; byte-restore is invalid — undo the *operation*, not bytes.
- **Q: Which engines use ARIES?** → **A:** SQL Server (direct), Postgres, InnoDB, Oracle (SCN), RocksDB/MongoDB (WAL variants).

## 21. Revision
ARIES = the production recovery algorithm: WAL + LSNs + DPT + transaction table + CLRs. Recovery runs Analysis (rebuild active txns + dirty pages; redo point = min RecLSN) → Redo (re-apply all changes from redo point, LSN-checked, idempotent) → Undo (roll back uncommitted transactions backward, logging CLRs so a crash mid-recovery resumes safely). Redo restores the log tail; undo removes uncommitted work; logical undo handles structure ops. Postgres, InnoDB, SQL Server, Oracle all implement ARIES-family recovery.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is ARIES?" | 1, 2, 7 |
| "Three phases of ARIES?" | 2, 8, 13 |
| "What is an LSN / pageLSN?" | 2, 9, 13 |
| "What is the dirty page table?" | 2, 9, 13 |
| "What is a CLR?" | 2, 9, 13 |
| "Why redo before undo / repeating history?" | 4, 13 |
| "Why logical undo for B-trees?" | 4, 13 |
| "How does Postgres do crash recovery?" | 13, 16 |
