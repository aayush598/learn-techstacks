# DBMS Components and Architecture

> **TL;DR**: A DBMS is a pipeline of cooperating subsystems — query processor (parser/optimizer/executor), storage manager (buffer manager, file/access methods), and transaction manager (concurrency + recovery) — that converts a declarative SQL statement into safe, fast, durable reads and writes.

## 1. Why Does This Exist?
A DBMS must do many jobs — parse SQL, choose a fast plan, manage disk pages, keep concurrent transactions correct, and survive crashes — and no single monolithic blob can do all of them well. This section exists to explain the *decomposition*: each hard problem is isolated into a component with a clear interface. The architecture exists so that (a) each concern can be optimized independently (an index improvement shouldn't touch transaction logic), (b) correctness-critical parts (recovery, locking) are separated from performance parts (caching), and (c) the whole pipeline is explainable — which is exactly what interviewers want when they ask "trace a query through a DBMS."

## 2. How Does It Work?
The pipeline (top → bottom): **Client** sends SQL → **Query Processor**: *Parser* (syntax + catalog check), *Translator/Preprocessor* (views expanded), *Optimizer* (cost-based plan choice), *Execution Engine* (operators: scan, join, aggregate) → **Storage Manager**: *Buffer Manager* (page cache), *File Manager* (files/pages), *Access Methods* (heap, B+ tree, hash) → **Disk**. In parallel, the **Transaction Manager**: *Concurrency Controller* (locks/MVCC), *Recovery Manager* (WAL, checkpoints, undo/redo) → **Log + Data files** on disk. The **Catalog Manager** stores metadata that the parser and optimizer read. Every query crosses most of these boxes; every write additionally goes through the transaction manager.

## 3. When Is It Used?
- **Every query**: parser → optimizer → executor → buffer manager → disk, in every DBMS, every time.
- **Every write**: additionally acquires locks, appends WAL, updates pages, and at commit, flushes the log.
- **Crash recovery**: the recovery manager replays WAL at restart; checkpoints bound recovery time.
- **DDL**: catalog manager updates metadata tables; storage manager allocates new files.
- **Administration**: buffer pool sizing, `VACUUM`, `CHECKPOINT`, index creation all exercise these components — DBAs reason about this architecture daily.
- **Query debugging**: reading `EXPLAIN` output is reading the optimizer's plan — a direct interface to this architecture.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: single-process monolith where one module does everything.** Rejected because correctness modules (locking, recovery) and performance modules (caching, optimization) have opposing goals; separating them prevents, e.g., an optimizer bug from corrupting the WAL.
- **Alternative: no optimizer — user-provided access paths (navigational).** Rejected: data independence and declarative SQL *require* an optimizer that picks the plan. Users shouldn't know about indexes.
- **Alternative: pass raw file I/O to the app (no buffer manager).** Rejected: every app would reimplement caching, page buffering, and read-ahead; the DBMS owns the page cache to guarantee consistent snapshots and WAL ordering.
- **Alternative: a single global lock manager for everything.** Rejected for performance — granularity matters (row vs page vs table locks), so the concurrency controller must be separate and tunable.
- **Why this modular design?** It mirrors the OS's own layered design (which itself proved modularity works), and it lets DBMS vendors swap components (storage engine plugins, index types) without touching SQL semantics.

## 5. Intuition
Think of a **restaurant kitchen pipeline**. The *parser* is the hostess reading the order and checking it's valid (do we have that dish?). The *optimizer* is the chef deciding the fastest way to cook it (grill vs oven — which pan/heat is cheapest). The *executor* is the line cooks executing each step. The *buffer manager* is the pantry fridge — keep the most-used ingredients close so you don't run to the basement (disk) each time. The *transaction manager* is the billing + backup system: make sure orders paid together are recorded together, and if the kitchen catches fire, the receipt ledger lets you rebuild what was cooking. Every order (query) flows through the same stations.

## 6. Real-World Analogy
A **warehouse + order-fulfillment company** (Amazon's distribution model). The *parser* reads the customer's order and validates items exist. The *optimizer* picks which fulfillment center and which shelf layout to pull from (cheapest path). The *executor* sends pickers (access methods) to shelves. The *buffer manager* keeps fast-moving items near the loading dock (cache). The *concurrency controller* ensures two customers can't both take the last unit (locking). The *recovery manager* keeps a manifest (WAL) so if a truck crashes, the shipment can be reconstructed. The *catalog* is the master product/SKU list (metadata) every station consults. Remove any station and fulfillment breaks.

## 7. Formal Definition
A DBMS is logically divided into (Elmasri & Navathe Ch. 2; Silberschatz Ch. 1.3-1.4, 12-13):
- **Query processor**: DDL/DML compiler (parser + translator), query optimizer, execution engine.
- **Storage manager**: authorization & integrity manager, transaction manager, file manager, buffer manager, access methods (indexes), and the data structures/files (data files, data dictionary, indexes, WAL).
- **Transaction manager**: concurrency-control manager (locking/MVCC) + recovery manager (log, checkpoints).
- **System catalog**: the self-describing metadata repository the parser and optimizer consult.
A query is processed as: parse → validate against catalog → optimize (cost-based) → execute via operators over pages managed by the buffer manager; writes are serialized through the transaction manager which orders WAL writes before page writes.

## 8. Example
Trace `SELECT name FROM student WHERE gpa > 3.5` on a table with 1M rows and an index on `gpa`:
1. **Parser**: valid SQL; `student`, `name`, `gpa` exist in catalog.
2. **Optimizer**: compares two plans — (a) full heap scan (1M rows, read ~all pages) vs (b) index range scan on `gpa > 3.5` (reads only matching leaves) — picks (b), cost ~O(log n + matched).
3. **Executor**: opens the index, walks leaves, fetches matching row pointers, then pages from the heap.
4. **Buffer manager**: if those pages are cached in shared_buffers, no disk I/O (cache hit); else reads 8 KB pages from disk.
5. **Transaction manager** (read-only): takes no write locks, uses MVCC snapshot to avoid blocking.
6. Result rows stream to the client. On an `UPDATE`, step 5 changes: row lock + WAL append + commit log fsync.

## 9. Internal Working
1. **Parser**: tokenizes SQL → parse tree → semantic check against catalog (tables/columns exist, types OK, privileges OK).
2. **Preprocessor**: expands views into their defining queries; rewrites (flattening, predicate pushdown).
3. **Optimizer**: generates plans (join orders, access methods), estimates costs from statistics (row counts, distinct values, histograms), selects minimum-cost plan. May use dynamic programming over join orders (O(n!) worst → pruned).
4. **Executor**: volcano-style operator tree — each node (scan, filter, join, aggregate) pulls rows from below and pushes up; result streamed.
5. **Buffer manager**: LRU/CLOCK eviction; dirty pages written back at checkpoint; ensures a page is read *once per snapshot* (consistency).
6. **Access methods**: heap (unordered append), B+ tree (ordered, O(log n)), hash (O(1) equality). 
7. **Transaction manager**: acquires locks (2PL or MVCC snapshots); deadlock detection via wait-for graph; WAL (append `BEGIN/UPDATE/COMMIT` records) → fsync WAL at commit → lazily flush data pages → `CHECKPOINT` periodically.
8. **Recovery on crash**: analyze WAL → redo committed txns → undo uncommitted → database reaches a consistent committed state.

## 10. Time Complexity
- **Parsing**: O(len(SQL)) + O(catalog lookups) — effectively constant per query.
- **Optimization**: exponential in join count worst case (pruned heuristics: usually near-instant; complex queries may hit `join_collapse_limit`).
- **Execution**: index point lookup O(log_f n); index range O(log_f n + k) (k = matches); full scan O(n); hash join O(n+m); sort-merge join O(n log n + m log m); nested loop O(n·m).
- **Buffer hit**: ~0.1–1 µs (RAM); disk read: ~5–10 ms → the entire architecture is an optimization for that 10⁴× gap.

## 11. Advantages
- **Separation of concerns**: correctness vs performance modules isolated; bugs contained.
- **Data independence**: optimizer absorbs storage changes; apps stable.
- **Performance**: cost-based optimization + caching + access methods tailored per query.
- **Reliability**: WAL + checkpointing + recovery makes crashes cheap and correct.
- **Extensibility**: plugins (storage engines, index types, functions) without touching SQL.
- **Scalability of development**: big DBMSs (Postgres ~1M LOC) are maintained by many teams in parallel — modularity is what makes that possible.

## 12. Disadvantages
- **Overhead & complexity**: many layers add latency and memory; tuning knobs (buffer sizes, work_mem) require expertise.
- **Hard to reason about**: one bad optimizer estimate → 1000× slowdown; `EXPLAIN` literacy is mandatory.
- **Interference between components**: e.g., a long-running transaction blocks vacuum/checkpoints; buffer pressure can starve WAL writes.
- **Monolithic engines resist horizontal scale** — sharding is bolted on; that's partly why NoSQL architectures split storage/compute.
- **Failure modes are global**: a bug in the recovery manager can take the whole cluster down.

## 13. Interview Questions
1. **Q: Name the main components of a DBMS and their roles.** A: Query processor (parser, optimizer, executor), storage manager (buffer manager, file manager, access methods), transaction manager (concurrency control + recovery/WAL), and the system catalog. Parser validates; optimizer plans; executor runs; buffer manager caches pages; transaction manager guarantees ACID.
2. **Q: Trace the path of `SELECT ... WHERE ...` through a DBMS.** A: Parse → semantic check vs catalog → view expansion → optimize (pick index/scan/join) → execute via operator tree → buffer manager fetches pages → rows streamed out. For writes: + locks, WAL append, fsync at commit, page update, checkpoint.
3. **Q: What does the query optimizer do?** A: Takes the parsed query and generates the cheapest physical plan: choosing join order, join algorithm (hash/nested-loop/merge), and access method (index vs scan) using table statistics and estimated costs. It's the difference between a 1-second and 1-hour query.
4. **Q: What is the buffer manager and why is it needed?** A: It caches disk pages in RAM (shared_buffers) to avoid hitting the ~5-10 ms disk latency for hot data. It manages eviction (LRU/clock) and dirty-page write-back. Without it, every query would be disk-bound.
5. **Q (tricky): If the OS already caches files, why does the DBMS need its own buffer cache?** A: Control: consistent page snapshots per transaction, ordered write-back vs WAL, checksums, its own eviction policy, and avoiding double-copying. The OS cache is page-oriented and not transaction-aware; the DBMS must not read torn/half-updated pages.
6. **Q: What is the system catalog?** A: The metadata tables describing tables, columns, types, constraints, indexes, users, privileges, statistics. It's self-describing — the DBMS reads it to validate, optimize, and enforce. Postgres: `pg_catalog`; standard: `information_schema`.
7. **Q: What is the difference between parser and optimizer?** A: Parser checks *syntax and semantics* (is the SQL well-formed, do tables exist, types match) — it does not care about speed. Optimizer chooses *how to execute* (plan) — it's about speed/cost.
8. **Q (scenario): A query is slow. Which components would you suspect?** A: In order: missing/wrong index (access method/optimizer), stale statistics (optimizer picks bad plan), buffer cache thrashing (buffer manager), lock contention (concurrency control), bad join order (optimizer), disk I/O (storage). Use `EXPLAIN ANALYZE` to localize — it exposes the optimizer's plan and actual costs.
9. **Q: What is the transaction manager?** A: The component guaranteeing ACID: it acquires/releases locks (or uses MVCC), manages isolation levels, detects deadlocks, and coordinates with the recovery manager (WAL) so committed work survives crashes and aborted work is rolled back.
10. **Q: What is the WAL and what does the recovery manager do with it?** A: The write-ahead log records every change before data pages are updated; the recovery manager replays committed changes (redo) and rolls back uncommitted ones (undo) after a crash, restoring consistency. Checkpoints limit how much log must be replayed.
11. **Q (tricky): Which component decides between a hash join and a nested-loop join?** A: The optimizer, using estimated sizes (both inputs, available memory `work_mem`). Hash join wins on large unsorted inputs (O(n+m)); nested loop wins on small inputs with index lookups (O(n·log m)).
12. **Q: What is an access method / what does the storage manager include?** A: Access methods are the physical ways to fetch rows: heap scan, B+ tree index, hash index. The storage manager = file manager + buffer manager + access methods + (at lower level) raw blocks. It turns logical "scan relation" into physical "read pages".
13. **Q (production): Why is `work_mem` (or `sort_mem`) important?** A: It bounds memory for sorts/hashes. If a sort exceeds `work_mem`, the executor spills to disk (temp files), causing a 10-100× slowdown. Tuning this knob is a classic DBA act — and an optimizer-vs-executor interaction interviewers like.
14. **Q: What happens on a `CHECKPOINT`?** A: The DBMS flushes all dirty buffer pages up to the current WAL position and records the checkpoint in the log. This shortens crash recovery (less WAL to replay) at the cost of a burst of writes.
15. **Q: What is MVCC and which component implements it?** A: Multi-Version Concurrency Control — each transaction sees a consistent snapshot; readers don't block writers. Implemented by the transaction/storage layer (Postgres `xmin/xmax` tuple headers, old versions until `VACUUM`). It's why `SELECT` is nearly free of lock contention in Postgres.
16. **Q (tricky): Why does the optimizer sometimes choose a full scan over an index?** A: If the query touches a large fraction of rows (e.g., `WHERE status = 'active'` on 80% active rows), an index adds page-jumping overhead — sequential scan of the heap is cheaper. Statistics + selectivity drive this. The index isn't "bad"; the plan was right.
17. **Q: How does the executor stream results instead of loading everything?** A: Volcano/tuple-at-a-time iteration: operators pull one tuple from their child, process, push up; the client fetches in batches (cursor/fetch size). Memory stays O(pipeline depth), not O(result size).
18. **Q: What is a "plan operator"?** A: A physical node in the execution tree: `SeqScan`, `IndexScan`, `HashJoin`, `Sort`, `Aggregate`, `NestLoop`. `EXPLAIN` shows the operator tree; each has an estimated cost. Reading one is reading the optimizer's decisions.
19. **Q (production): A report query runs 10× slower after statistics were refreshed. Why?** A: The optimizer now estimates differently and chose a worse plan (e.g., switched from index to hash join, or a scan). This is the classic "optimizer is fragile to statistics" failure — fix with plan hints, better indexes, or `ANALYZE` at the right frequency.
20. **Q (hard): What is the difference between logical and physical optimization?** A: Logical: algebraic rewrites that are always correct (predicate pushdown, join reordering, subquery flattening, projection elimination). Physical: choosing implementation (join algorithm, access method, memory limits). Logical doesn't need statistics; physical does.

## 14. Follow-Up Questions
1. **Q: Why is the buffer manager "the" performance bottleneck in OLTP?** A: Because RAM hits are ~100 ns vs disk ~5-10 ms (10⁴×). A 99.9% cache-hit workload is 1000× faster than 50% hit. Every OLTP tuning goal reduces to keeping hot pages resident.
2. **Q: What is the difference between a DBMS "page" and an OS "block"?** A: DBMS page (4-16 KB) is the unit of DBMS I/O with headers/slots/checksums; OS block (typically 4 KB) is the unit of file-system I/O. The DBMS maps pages to blocks.
3. **Q: Why are modern DBMSs moving compute/storage apart (Snowflake)?** A: Because the buffer manager + WAL were designed for a fixed node; separating them (shared storage, elastic compute) decouples capacity and cost. The optimizer/executor remain, but page ownership moves to object storage.
4. **Q: What is a "hot" vs "cold" page?** A: Hot = frequently accessed (stays in cache); cold = rarely accessed (evicted). The buffer manager's eviction policy decides the boundary; an LRU/clock approximation.
5. **Q: Does the executor ever write to disk during a `SELECT`?** A: Yes — sorts/hash joins that exceed `work_mem` spill to temp files, and materialized intermediate results may be spilled. `EXPLAIN ANALYZE` shows "Disk:" usage when it happens.

## 15. Coding Example
```pseudocode
// Simplified DBMS pipeline for SELECT
function runQuery(sql):
    tree   = Parser.parse(sql)            # syntax + catalog check
    logical= Preprocess.expandViews(tree) # view → base query
    plan   = Optimizer.choosePlan(logical, stats)   # cost model
    for tuple in Executor.execute(plan):  # volcano streaming
        emit(tuple)

// Executor pulls tuples bottom-up
function IndexScan(op):
    for rowid in BTree.seek(op.index, op.range):
        page = BufferManager.fetchPage(heap, rowid.page)
        yield page.rows[rowid.slot]       # cache hit? no disk I/O

// Transaction side for UPDATE
function ExecuteUpdate(txn, sql):
    ConcurrencyControl.lockRows(txn, rows)     # row locks / MVCC
    Recovery.log(WAL, "UPDATE", rows, newvals) # before page writes
    Storage.apply(rows, newvals)               # to dirty pages
    txn.markCommitting()
    Recovery.fsyncWAL()                        # durability point
    txn.commit()                               # visible to others
```

## 16. Industry Usage
- **PostgreSQL** (relational): components map 1:1 — `postgres` backend (executor), `pg_planner` (optimizer), `shared_buffers` (buffer manager), `pg_stat_*` (catalog stats), WAL in `pg_wal`, MVCC via `xmin/xmax`. Reading Postgres docs is reading this architecture.
- **MySQL InnoDB** (OLTP): buffer pool (memory), change buffer, doublewrite buffer, redo log (WAL), undo log (MVCC) — the same components with different names.
- **Oracle** (enterprise): SGA/shared pool (buffer + library cache), cost-based optimizer, `DBMS_STATS` for statistics, redo/undo logs.
- **Snowflake** (warehouse): separates storage (shared object store) from compute (virtual warehouses) — the optimizer/executor per-warehouse, catalog shared. A production proof that the architecture can be physically split.
- **Every EXPLAIN / query plan / slow-query log** a DBA reads is output from this architecture. Interviewers asking "why is this query slow" are probing your model of these components.

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 2 (Database System Concepts and Architecture).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 1 (Introduction) & Ch. 12-13 (Physical Storage; Query Processing).
- PostgreSQL Documentation: https://www.postgresql.org/docs/current/ — `EXPLAIN`, WAL, shared buffers.
- MySQL Reference Manual, InnoDB: https://dev.mysql.com/doc/refman/8.0/en/innodb-introduction.html
- Graefe, G., "Query Evaluation Techniques for Large Databases", ACM Computing Surveys, 1993 (volcano model).

## 18. Cheat Sheet
- Query path: Parse → Catalog check → Optimize → Execute → Buffer → Disk.
- Write path adds: locks → WAL → fsync at commit → page write → checkpoint.
- 3 manager families: Query Processor, Storage Manager, Transaction Manager.
- Optimizer = the "why is my query slow?" answer point; read `EXPLAIN`.
- Buffer manager: page cache in RAM (shared_buffers); avoids 10⁴× disk latency.
- WAL = write-ahead log; recovery = redo committed, undo uncommitted.
- Access methods: heap (scan), B+ tree (range/point), hash (equality).
- MVCC: readers don't block writers; snapshot isolation.

## 19. Quiz
1. Which component validates SQL against the catalog? a) optimizer b) parser c) buffer manager d) recovery → **b**
2. Which picks the join algorithm? a) parser b) optimizer c) WAL d) checkpoint → **b**
3. shared_buffers is managed by: a) parser b) buffer manager c) catalog d) client → **b**
4. The WAL is written: a) after page updates b) before page updates c) never d) only at shutdown → **b**
5. Crash recovery does: a) delete data b) redo committed + undo uncommitted c) reinstall d) fsck → **b**
6. A full table scan of n rows costs: a) O(1) b) O(log n) c) O(n) d) O(n²) → **c**
7. Which is NOT a DBMS component? a) optimizer b) buffer manager c) compiler of the OS d) recovery manager → **c**
8. MVCC mainly helps: a) compression b) readers not blocking writers c) encryption d) backup → **b**
9. A checkpoint's purpose: a) shrink WAL replay time b) speed up SELECT c) add indexes d) compress data → **a**
10. `EXPLAIN` output shows: a) syntax errors b) the optimizer's plan c) user logins d) disk errors → **b**

## 20. Flashcards
- **Q: Query path through a DBMS?** → **A:** Parse → catalog check → optimize → execute → buffer manager → disk.
- **Q: What does the optimizer choose?** → **A:** Join order, join algorithm, access method — cheapest plan from statistics.
- **Q: What is the buffer manager?** → **A:** RAM cache of disk pages; eviction + write-back; hides disk latency.
- **Q: What is WAL?** → **A:** Log of changes written before data pages; basis of durability and recovery.
- **Q: What does recovery do on crash?** → **A:** Redo committed txns, undo uncommitted, reach consistent state.
- **Q: 3 access methods?** → **A:** Heap scan, B+ tree, hash index.
- **Q: What is MVCC?** → **A:** Snapshot-based concurrency; readers don't block writers.
- **Q: Where does EXPLAIN come from?** → **A:** The optimizer — it prints the chosen physical plan.

## 21. Revision
DBMS = pipeline of cooperating subsystems. **Query processor**: parse (syntax + catalog), optimize (cost-based plan), execute (operator tree, streaming). **Storage manager**: buffer manager (page cache), file manager, access methods (heap/B+tree/hash). **Transaction manager**: concurrency control (locks/MVCC) + recovery (WAL: write log before pages; on crash redo committed, undo uncommitted; checkpoints bound replay). The **catalog** holds metadata and statistics — what the parser and optimizer read. Interview moves: trace a SELECT and an UPDATE separately (the UPDATE adds locks + WAL + fsync); answer "slow query?" with the component-by-component checklist ending in `EXPLAIN ANALYZE`; explain why buffer cache exists (10⁴× RAM-vs-disk gap). Name Postgres/MySQL equivalents (shared_buffers/InnoDB buffer pool, pg_wal/redo log).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Name the DBMS components and their roles" | 2 / 13 Q1 |
| "Trace a query through the DBMS" | 8 / 13 Q2 |
| "What does the optimizer do?" | 13 Q3 |
| "Why does the DBMS need its own buffer cache?" | 13 Q5 |
| "What is the WAL / recovery manager?" | 13 Q10 |
| "Why is my query slow? Which component?" | 13 Q8 / 10 |
| "What is MVCC?" | 13 Q15 |
| "What does EXPLAIN show?" | 13 Q18 |
