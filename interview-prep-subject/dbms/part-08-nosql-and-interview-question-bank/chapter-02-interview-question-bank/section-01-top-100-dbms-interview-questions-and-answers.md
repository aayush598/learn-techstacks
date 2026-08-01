# Top 100 DBMS Interview Questions

> **TL;DR**: 100 must-know DBMS questions (fundamentals, relational model, normalization, indexing, transactions, recovery, query processing, NoSQL) with tight answer keys you can rehearse aloud — each marked with difficulty (E/M/H) and mapped to the source part; the "say-it-out-loud" rehearsal script for interview day.

## 1. Why Does This Exist?
A DBMS interview tests two things: *breadth* (do you know the whole syllabus?) and *depth* (can you explain *why*?). This file exists to give you a single rehearsal artifact covering the full surface of Parts 01-08 — the 100 questions that are actually asked, not a random sampling. It exists because interview prep fails when it's scattered: candidates deep-dive B-trees but freeze on "what is a covering index?" or "explain ACID vs BASE." By organizing 100 questions by part with difficulty tiers and mapping each to its source section, you can (a) audit your gaps part-by-part, (b) rehearse aloud (the answers are written to be spoken), and (c) cross-link to the detailed material when an answer feels thin.

## 2. How Does It Work?
- Questions are grouped by the 8 parts: Q1-14 fundamentals, Q15-28 relational model & SQL, Q29-42 normalization, Q43-56 indexing & file organization, Q57-70 transactions & concurrency, Q71-84 recovery, Q85-92 query processing & optimization, Q93-100 NoSQL.
- Each Q&A is tagged **[E]**asy, **[M]**edium, **[H]**ard, and has a `→ Part X §Y` back-reference to where the full explanation lives.
- The answers are written as you'd *say* them in an interview (2-4 sentences + a crisp mechanism), not textbook prose.
- Use it as: (1) a self-audit checklist (can I say the answer aloud?), (2) a warm-up the day before, (3) a targeting tool (only review the tiers you're aiming at).

## 3. When Is It Used?
- Daily 20-minute audio rehearsal blocks in the final two weeks.
- Gap detection: mark every question you can't answer cleanly → re-read the mapped section → retest.
- 24h before the interview: rapid pass over all 100.
- Live-interview practice with a peer: have them pick random numbers.
- The "stretch" set (H-tier) for senior/principal loops.

## 4. Why Wasn't Another Approach Chosen?
- *Just reading the full parts*: depth is great but interview *fluency* is a different skill — you must compress knowledge into spoken answers. The 100 Q&A are the compression.
- *Flashcards alone*: cards test recall, not articulation; these answers model *how* to phrase the explanation.
- *Random question banks*: miss the systematic coverage; this list is engineered to span every part so no gap goes undetected.
- *Memorized scripts verbatim*: interviewers dig with follow-ups (Section 14 in every part); these answers give the *core mechanism* so you can improvise the follow-up rather than recite.

## 5. Intuition
Think of this file as a **pilot's pre-flight checklist** — the same set every time, in the same order, designed so you *notice the gap* when you can't complete an item. You don't fly a plane by remembering one conversation; you fly it by walking a checklist. Interview fluency is the same: the *list* is the framework that keeps your knowledge ordered and complete under pressure. Each item (question) is paired with a "what I say out loud" — the spoken answer — so rehearsing is exactly the motion of the real event. And like a checklist, it's no substitute for the systems manual (the parts themselves) — it's the *operating procedure* built on top.

## 6. Real-World Analogy
A **fighter pilot's habit patterns** or a **sous-chef's station checklist**: the chef doesn't relearn knife skills at service — the checklist reminds them to taste the sauce, check the heat, verify plating order, every single service. The 100 questions are your *service checklist*: on the day, pressure is high and recall must be automatic. The checklist (Q1-100) tells you what's *expected at this station* (this part of the syllabus), the answer key is your *trained motion* (the phrasing you've practiced), and the back-reference is the *recipe* if you realize your motion is rusty. Practicing the checklist until it's boring is exactly what makes service (the interview) feel routine.

## 7. Formal Definition
A structured set of 100 canonical interview questions with model answers, organized by syllabus part and difficulty tier, each answer stating (a) the definition/mechanism, (b) the trade-off/why, (c) one concrete example — the minimal shape of a strong verbal answer. Difficulty: E (definition/recall), M (mechanism/trade-off), H (edge cases, production judgment, distributed interplay).

## 8. Example
See the full question set below (Section 13). A sample at the target shape:
**[M] Q61: What is the difference between dirty, non-repeatable, and phantom reads?** A: Dirty read — reading an uncommitted write (prevented by READ COMMITTED). Non-repeatable read — re-reading the same row in one transaction sees a *changed* value (another transaction committed between) (prevented by REPEATABLE READ). Phantom — re-running a query sees *new rows* inserted by another transaction (prevented by SERIALIZABLE). Each isolation level adds one prevention: RC fixes dirty, RR fixes non-repeatable (and in Postgres also phantoms via MVCC), Serializable fixes all. → Part 05 §Chapter 1 §3-4.

## 9. Internal Working
The set is built to *cover* the syllabus and *rehearse* the answer shape. Working rule for each entry: state it → show the mechanism → give the trade-off → land an example. The "trap" notes (e.g., "work_mem is per operation", "CAP applies during partitions", "LWW can lose updates") are seeded where candidates most commonly fail, so a rehearsal pass catches your own blind spots. The back-references guarantee that if an answer feels thin, the depth is one click away — the file is a *router*, not a replacement.

## 10. Time Complexity
- Full pass (say aloud): ~90-120 minutes at 45-60s/answer.
- Rapid pass (skim): ~25-35 minutes.
- Gap-fix loop: ~15 min/question of source re-reading.
- The value: 100 rehearsed answers ≈ a whole interview round's worth of fluent output; the list removes "what will they ask?" anxiety.

## 11. Advantages
- **Complete coverage** with no syllabus gap.
- **Spoken-ready answers** — the exact muscle interview day uses.
- **Difficulty-tagged** for level targeting.
- **Back-referenced** for instant depth when needed.
- **Gap-detecting** — the checklist exposes what you don't know.
- **Reusable** — the same file serves audit, warm-up, and rapid review.

## 12. Disadvantages
- **Answers are compressed** — not a substitute for the parts; weak spots need the source.
- **Model answers ≠ your voice** — adapt the phrasing to how you naturally explain.
- **Static list** — live interviews invent novel angles; the list trains the base, follow-up improv comes from mechanism understanding.
- **Recitation risk** — the trap of parroting; always be ready for the "why?" probe.

## 13. Interview Questions

### Part 01 — Fundamentals (Q1-14)
1. **[E] What is a database and a DBMS?** A: A database is an organized collection of data; a DBMS is software managing it — storage, retrieval, concurrency, integrity, recovery. Examples: PostgreSQL, MySQL, MongoDB. → Part 01 §1
2. **[E] What are the three-schema architecture and why?** A: External (user views) / conceptual (community schema) / internal (physical storage). It gives logical independence (change schema without views) and physical independence (change storage without schema). → Part 01 §2
3. **[E] What is data independence?** A: The ability to change one level without changing the next: logical independence (conceptual vs external) and physical independence (internal vs conceptual) — so storage changes don't break queries. → Part 01 §2
4. **[M] What is a data model? Name the main types.** A: A data model describes structure + constraints + operations. Types: relational, ER, network, hierarchical, object, and NoSQL models (KV/document/wide-column/graph). → Part 01 §3
5. **[M] What are the components of a DBMS architecture?** A: Query processor (parser, optimizer, executor), storage manager (buffer, file, indexing), transaction manager (concurrency control, recovery), and metadata (catalog). → Part 01 §4
6. **[E] What is a data dictionary / catalog?** A: The DBMS's metadata: schema, tables, indexes, constraints, privileges — used by the planner and DDL; stored in system tables (pg_catalog, information_schema). → Part 01 §4
7. **[M] What is the difference between a database and a data warehouse?** A: Database = OLTP, transactional, normalized, row-store, current data, many small writes. Warehouse = OLAP, analytical, denormalized, columnar, historical aggregates, bulk loads. → Part 01 §4
8. **[M] What is OLTP vs OLAP?** A: OLTP: online transaction processing — many short ACID transactions (orders, logins). OLAP: online analytical processing — complex read-only aggregations over history (reporting). Different engines/designs optimize each. → Part 01 §4
9. **[E] What is a transaction?** A: A logical unit of work (one or more statements) executed atomically with ACID guarantees — all-or-nothing, isolated from others, durable. → Part 05
10. **[M] What does ACID stand for and give an example of violation?** A: Atomicity (all-or-nothing — a transfer debits both accounts or neither), Consistency (constraints hold), Isolation (concurrent transactions don't see each other's partial work), Durability (committed survives crash via WAL). → Part 05 Ch1
11. **[M] What is a buffer pool and why does it exist?** A: The in-memory cache of pages managed by the storage manager — converts disk I/O into memory hits; managed with LRU/clock replacement; dirty pages flushed by the background writer. → Part 01 §4, Part 04
12. **[H] What is a dirty page and what happens if the system crashes while it's in memory?** A: A modified page not yet written to disk. On crash, in-memory dirty pages are lost — that's why WAL (write-ahead logging) writes the *log record* to disk *before* the page, so recovery replays/undoes. → Part 06
13. **[M] What are the file organization types?** A: Heap (unordered), sorted/sequential (by key), hashed (by hash key), clustered (related rows near each other, e.g., index-organized tables). Choice affects scan/point/range costs. → Part 04
14. **[H] What is the difference between physical and logical data independence, with a concrete case?** A: Physical: change storage layout (add an index) without changing schema/SQL. Logical: add a column or change schema without rewriting external views (views insulate). Both exist to decouple layers. → Part 01 §2

### Part 02 — Relational Model & SQL (Q15-28)
15. **[E] What is a relation?** A: A table with: unique name, attributes (columns) with domains, rows, and constraints (key, entity, referential). Rows unordered; each row unique by key. → Part 02
16. **[E] What is a superkey vs candidate key vs primary key vs foreign key?** A: Superkey — any set of attributes uniquely identifying a row. Candidate key — *minimal* superkey. Primary key — chosen candidate key. Foreign key — references a primary/unique key in another table to enforce referential integrity. → Part 02
17. **[M] What is the difference between a key and an index?** A: A key is a *constraint* (uniqueness/integrity, part of the data model). An index is a *physical access structure* (speeds queries). Keys are usually implemented with indexes, but an index needn't be a key (a non-unique index). → Part 02/04
18. **[E] What are the integrity constraints?** A: Domain (attribute values), key/entity (unique identifier), referential (FK validity), and general user-defined constraints (CHECK). They enforce the "C" in ACID. → Part 02
19. **[M] What is referential integrity and what are the FK action options?** A: Every FK value must exist (or be NULL) in the referenced table. Actions on parent delete/update: RESTRICT/NO ACTION, CASCADE, SET NULL, SET DEFAULT — choose by business semantics (cascade deleting a user's orders vs nulling them). → Part 02
20. **[M] What are the three SQL sublanguages?** A: DDL (CREATE/ALTER/DROP — schema), DML (INSERT/UPDATE/DELETE/SELECT — data), DCL (GRANT/REVOKE — permissions), plus TCL (COMMIT/ROLLBACK) for transactions. → Part 02
21. **[E] What is a view?** A: A named, stored query (virtual table) — a saved SELECT; insulates users from schema, restricts access, and can be updated under conditions. Materialized views persist results for performance. → Part 02
22. **[M] TRICKY: What is the difference between DELETE, TRUNCATE, and DROP?** A: DELETE — row-by-row DML, can be filtered, *can be rolled back*, fires triggers. TRUNCATE — removes all rows quickly (DDL-ish), resets storage, still rollbackable in most engines (minimal logging). DROP — removes the object itself (table/index) entirely. → Part 02
23. **[M] What is a join? Name the types.** A: A join combines rows from tables by a condition. Types: INNER, LEFT/RIGHT/FULL OUTER, CROSS, SELF, and NATURAL (by same-named columns). Execution via nested-loop/merge/hash (Part 07). → Part 02/07
24. **[M] TRICKY: LEFT JOIN vs INNER JOIN — when do they return different row counts?** A: When the right side has no match for a left row: INNER drops the left row, LEFT keeps it with NULLs on the right. If the right side is unique per left row and always matches, they're equal. → Part 02
25. **[M] What is GROUP BY and the HAVING clause?** A: GROUP BY groups rows by columns; aggregates (COUNT/SUM/AVG) apply per group. HAVING filters *groups* (after aggregation); WHERE filters *rows* (before). → Part 02
26. **[H] What is the difference between HAVING and WHERE, and why can't you use an aggregate in WHERE?** A: WHERE filters rows *before* grouping — aggregates aren't defined yet. HAVING filters groups *after* aggregation. ORDER: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY. → Part 02
27. **[M] What is a correlated subquery?** A: A subquery referencing an outer-query column — re-executed (or re-evaluated) per outer row. Expensive; optimizers may turn some into joins. `SELECT name FROM emp e WHERE salary > (SELECT AVG(salary) FROM emp WHERE dept_id = e.dept_id)`. → Part 02
28. **[H] What is the difference between ROW_NUMBER, RANK, and DENSE_RANK?** A: All assign an integer per ordering partition: ROW_NUMBER gives 1,2,3... ties broken arbitrarily; RANK gives 1,1,3 (gaps); DENSE_RANK gives 1,1,2 (no gaps). Choose by whether ties share a rank and whether ranks skip. → Part 02

### Part 03 — Normalization (Q29-42)
29. **[E] What is normalization and why?** A: Decomposing relations to reduce redundancy and update anomalies (insert/update/delete) by ensuring a "good" form via functional dependencies. → Part 03
30. **[E] What is a functional dependency?** A: `X → Y`: for any two rows with equal X, Y must be equal — X determines Y. The backbone of key/schema reasoning. → Part 03
31. **[M] What are the update anomalies?** A: Insert (can't add a fact without the whole row), update (redundant copies must change together), delete (removing a row destroys unrelated facts). Normalization eliminates them. → Part 03
32. **[E] What is 1NF?** A: Every attribute holds a single atomic value — no repeating groups/arrays/nested tables. (Trivially satisfied in modern SQL; violated by CSV-in-a-column.) → Part 03
33. **[E] What is 2NF?** A: 1NF + no *partial* dependency — every non-key attribute depends on the *whole* composite key (relevant only with composite keys). → Part 03
34. **[M] What is 3NF?** A: 2NF + no *transitive* dependency — non-key attributes depend only on the key (not on other non-key attributes). Eliminates "dept → city" style drift. → Part 03
35. **[H] What is BCNF and how does it differ from 3NF?** A: BCNF: every determinant must be a candidate key (3NF but stricter — handles the case where a non-key column determines part of a composite key, which 3NF permits). BCNF always preserves data but may sacrifice dependency preservation. → Part 03
36. **[M] What are the three properties of a good decomposition?** A: Lossless join (rejoin reproduces the original), dependency preservation (FDs checkable without a join), no redundancy/anomalies (normal form). Every join: lossless + dependency-preserving decomposition to BCNF isn't always possible — 3NF always is. → Part 03
37. **[H] What is the difference between lossless join and dependency preservation?** A: Lossless: the natural join of decomposed tables equals the original (no spurious rows). Dependency preservation: all FDs hold within a single decomposed table (no join needed to check them). A BCNF decomposition is always lossless but may lose dependencies; 3NF preserves both. → Part 03
38. **[M] What is 4NF?** A: 3NF/BCNF + no *multi-valued dependencies* (a non-trivial MVD not implied by a key). Handles independent one-to-many facts (employee → skills AND languages) that cause row multiplication. → Part 03
39. **[M] What is 5NF?** A: Join-projection form: no lossless decomposition into projections that can't be reassembled — handles cyclic 3-way relationships (join dependencies). Rare in practice. → Part 03
40. **[E] What is denormalization and when is it justified?** A: Intentionally re-adding redundancy for performance (avoid joins) — after profiling, when read-heavy queries dominate and you accept the update/consistency cost (or use materialized views). → Part 03
41. **[M] TRICKY: Is "always normalize to 3NF" correct?** A: No. Normalization reduces update anomalies but often adds joins to reads. Production schemas use a *judgment call*: normalize the transactional core, denormalize hot read paths (or use views/materialized views/columns), document the trade. → Part 03
42. **[H] How do you find a candidate key from a set of FDs?** A: Closure algorithm: start with attribute sets, apply FDs to compute closure (+=), a set whose closure covers all attributes is a superkey; remove extraneous attributes to get candidate keys. Minimal keys = those that lose coverage if any attr removed. → Part 03

### Part 04 — Indexing & File Organization (Q43-56)
43. **[E] What is an index?** A: A physical access structure (B-tree, hash, etc.) that speeds lookups/predicates/ordering by trading write overhead + storage. The planner chooses it when the estimated cost drops. → Part 04
44. **[M] What is a B+ tree and why is it the default index?** A: A balanced multi-way tree with internal nodes as routing keys and *all data in leaves*, leaves linked for range scans. Height O(log_d N) — a few disk reads even for billions of rows; great for equality *and* range/order. → Part 04
45. **[M] What is a clustered index?** A: The index whose order *defines* the physical row order (primary key in InnoDB — an index-organized table). One per table; range scans on it are sequential. Secondary indexes reference the clustered key. → Part 04
46. **[M] What is a covering index?** A: An index containing *all* columns a query needs (via INCLUDE/leaf columns) → "Index Only Scan" — no heap fetch. Often the cheapest read possible. → Part 04
47. **[M] What is the difference between a clustered and non-clustered (secondary) index?** A: Clustered determines physical order, one per table; secondary indexes are separate structures pointing to rows (or clustered keys), multiple allowed. Range on clustered is sequential I/O; secondary usually random. → Part 04
48. **[H] What is a composite index, and does column order matter?** A: An index over multiple columns; order matters for *range* (leftmost-prefix rule): an index on (a,b) serves `WHERE a=?`, `WHERE a=? AND b=?`, but *not* `WHERE b=?`. Equality-first ordering maximizes usefulness. → Part 04
49. **[M] What is the leftmost-prefix rule?** A: A composite index can only be used from its leftmost column(s): (a,b,c) serves predicates on a, (a,b), (a,b,c) — never starting at b or c. Order columns equality-first, then range/sort. → Part 04
50. **[M] What is a hash index and when is it right?** A: O(1) equality lookups on the key; useless for range/order. Right for exact-match lookups (in-memory workloads, Redis/Memcached philosophy); B-tree wins generally (also handles ranges). → Part 04
51. **[M] What is a bitmap index?** A: Each distinct value stores a bit per row; fast AND/OR on low-cardinality columns for analytics; expensive to maintain on high writes; used in warehouses (not OLTP B-trees). → Part 04
52. **[M] What is index bloat and how is it caused/fixed?** A: Dead entries/fragmentation from updates/deletes (page splits, dead tuples) make scans read extra pages. Fix: VACUUM/REINDEX (Postgres), OPTIMIZE TABLE (MySQL), fillfactor headroom for hot-update tables. → Part 04/07
53. **[H] Why is a B+ tree preferred over a binary search tree / hash for a disk index?** A: BST is tall (O(log2 N) disk reads — too many); hash has no range support; B+ tree has high fanout → height 3-4 for billions of rows → few disk reads, supports range/order via leaf links, and internal nodes can stay cached. → Part 04
54. **[H] What is a partial (filtered) index?** A: An index on a subset of rows (`WHERE` predicate) — smaller, faster, ideal for a hot selective predicate over mostly-old data (e.g., index only active orders). Planner uses it when the predicate matches. → Part 04
55. **[M] What is an expression index (functional index)?** A: An index on `LOWER(name)`, `(a+b)`, etc. — needed because plain indexes can't serve `WHERE LOWER(name)=...` (the planner won't know to reverse the function). Creates the transformed value as the key. → Part 04
56. **[H] TRICKY: A query uses `WHERE salary > 5000` on 90% of rows — should you index it?** A: Probably not — low selectivity means the index fetches most rows via random I/O, losing to a seq scan. Indexes pay when selectivity is high (few rows) or the index covers the query. Verify with EXPLAIN rather than guessing. → Part 04/07

### Part 05 — Transactions & Concurrency (Q57-70)
57. **[E] What is a schedule and what does it mean for it to be serial?** A: A schedule is an ordering of operations from concurrent transactions; serial means no interleaving (T1 fully before T2). Correctness compares a schedule to a serial one. → Part 05 Ch1
58. **[M] What is serializability and its two kinds?** A: A schedule is serializable if equivalent to *some* serial schedule. Conflict-serializable: swapping conflicting ops (same item, at least one write, different transactions) can't reach a serial order — the classic precedence-graph test. View-serializable is looser (same reads/final writes) — includes some non-conflict-serializable schedules. → Part 05 Ch1
59. **[M] What is the precedence graph and how do you test conflict serializability?** A: Nodes = transactions; edge Ti→Tj if they conflict (read-write/write-write on same item) with Ti's op first. Serializable iff acyclic (cycle = not conflict-serializable). → Part 05 Ch1
60. **[E] Name the isolation levels in order.** A: READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE — each adds prevention of dirty, then non-repeatable, then phantom reads (with engine-specific quirks, esp. MVCC). → Part 05 Ch1/2
61. **[M] TRICKY: Dirty vs non-repeatable vs phantom reads (with an example each)?** A: Dirty — read uncommitted data (rollback → you saw a ghost). Non-repeatable — re-read a row, its value changed (another txn committed). Phantom — re-run a query, new rows appear (another txn inserted within range). READ COMMITTED blocks dirty; REPEATABLE READ blocks non-repeatable; SERIALIZABLE blocks phantoms. → Part 05 Ch1
62. **[M] What is 2PL (two-phase locking)?** A: Every transaction does all its lock acquisitions (growing phase) before any release (shrinking phase). Guarantees conflict-serializable schedules; strict 2PL (hold locks until commit) also avoids cascading aborts and is what engines use. Deadlock possible. → Part 05 Ch2
63. **[M] What are the phases and types of locks?** A: Shared (S) — reads, compatible with other S; Exclusive (X) — writes, blocks everything. Growing phase (acquire only), shrinking phase (release only). Lock tables/rows/ranges depending on granularity. → Part 05 Ch2
64. **[H] What is deadlock, and how is it detected/resolved?** A: Two transactions each hold a lock the other needs → cycle. Detection: wait-for graph cycle check (Postgres: deadlock_timeout → check → abort one victim). Prevention: lock ordering, timeout, wait-die/wound-wait (timestamp priority). → Part 05 Ch2
65. **[M] What is timestamp-based concurrency control?** A: Each transaction gets a timestamp (order); reads/writes are rejected if they'd violate timestamp order (too-late read/write) — transaction restarts. Prevents deadlock (no waits/locks) at the cost of restarts; Thomas's Write Rule skips obsolete writes. → Part 05 Ch2
66. **[M] What is optimistic concurrency control (validation)?** A: Execute without locking, then *validate* at commit (timestamps ensure no conflicting writes happened); abort on conflict and retry. Best when conflicts are rare (read-heavy). Read/write phase + validation + write phase. → Part 05 Ch2
67. **[H] What is MVCC and how does Postgres implement it?** A: Readers never block writers: each version of a row gets a transaction id (xmin/xmax); a snapshot stores visible committed txns; a read builds its view from versions. Postgres stores old versions in the same page (or a TOAST/overflow), cleaned by VACUUM — allowing REPEATABLE READ without locks, giving snapshot isolation. → Part 05 Ch2/3
68. **[M] What is snapshot isolation and what's the anomaly it allows?** A: SI gives a transaction a consistent snapshot — no dirty/non-repeatable/phantom reads without locking. But *write skew* can occur: two transactions read overlapping data and each writes disjoint parts, violating a constraint neither saw change — prevented by Serializable SI (SSI), which detects dangerous structures. → Part 05 Ch2/3
69. **[H] What is write skew? Give an example.** A: T1 and T2 both read A and B (constraint: A+B ≥ 0); T1 writes A, T2 writes B; neither saw the other's write (SI), and together they violate A+B ≥ 0. Snapshot isolation permits it; SERIALIZABLE (SSI/true serializable) catches it via conflict detection. → Part 05 Ch2/3
70. **[M] How does MySQL InnoDB's REPEATABLE READ actually work?** A: MVCC snapshots (like Postgres) — so phantoms on plain SELECT are *also* prevented (unlike the SQL standard). But gaps: `SELECT ... FOR UPDATE`/`INSERT` still use gap locks/next-key locks, and the famous "phantom insert" can still be observed via `INSERT ... ON DUPLICATE KEY`. → Part 05 Ch3

### Part 06 — Recovery (Q71-84)
71. **[E] What types of failures can a database suffer?** A: Transaction failures (abort), system failures (crash: memory loss, disk OK), media failures (disk loss — needs backup). Recovery handles all three with logs + backups. → Part 06 Ch1
72. **[M] What is a WAL (write-ahead logging) rule?** A: The log record for a change must be flushed to stable storage *before* the data page is written. Recovery then knows every committed change is logged and every unlogged change was undone. → Part 06 Ch2
73. **[M] What is the ARIES recovery algorithm?** A: The industry-standard method: (1) *Analysis* — read log from last checkpoint to determine dirty pages and winners/losers; (2) *Redo* — replay all changes (even uncommitted) from the redo LSN using page LSNs to skip already-written pages; (3) *Undo* — roll back losers using the log, writing compensating log records (CLRs). Uses LSNs and dirty-page tables. → Part 06 Ch2
74. **[M] What is an LSN (log sequence number) and why does it matter?** A: A monotonically increasing pointer to a log record; pages store their last-updated LSN. During redo, a page whose pageLSN ≥ recordLSN was already flushed — skip it. Makes redo idempotent and fast. → Part 06 Ch2
75. **[M] What is a checkpoint?** A: A point where the DB forces buffered log/data to stable storage and records the state (dirty-page table + redo LSN). Recovery starts from the last checkpoint instead of the beginning of the log — bounds the recovery work. → Part 06 Ch2
76. **[M] What is UNDO vs REDO logging?** A: UNDO records let recovery *revert* uncommitted changes (on abort); REDO records let recovery *replay* committed-but-not-yet-flushed changes (on crash). ARIES logs both in one record and decides by analysis phase. → Part 06 Ch2
77. **[H] What is the difference between physical, logical, and physiological logging?** A: Physical logs record byte/page-level state (simple, replays exactly); logical logs record the *operation* (compact, but must be re-executable); physiological = page-level physical but operation-level within a page (ARIES compromise: redo physical-ish, undo logical-ish). → Part 06 Ch2
78. **[E] What is shadow paging?** A: Copy-on-write: keep two page tables (current + shadow); updates write new pages and switch the pointer on commit. No log needed for atomicity, but page copies are expensive and it doesn't do well with many transactions — mostly superseded by WAL. → Part 06 Ch2
79. **[M] How does PostgreSQL implement crash recovery?** A: WAL with LSNs: `INSERT`/`UPDATE` write xlog records before pages; on crash, replay WAL (redo) from the last checkpoint (redo phase), then undo is unnecessary for committed data because WAL already holds all changes; aborted transactions are cleaned by VACUUM rather than by undo at recovery. → Part 06 Ch3
80. **[M] What is a full vs incremental vs differential backup?** A: Full: complete copy (baseline). Incremental: changes since the *last backup of any kind* (small, but restore chains). Differential: changes since the *last full* (bigger but simpler restore). Strategy: periodic full + incremental/differential + archived WAL for point-in-time recovery. → Part 06 Ch3
81. **[H] What is point-in-time recovery (PITR)?** A: Restore a base backup then replay archived WAL up to a target time (e.g., just before a bad migration/delete). Requires continuous WAL archiving; Postgres: `archive_mode` + `pg_basebackup` + `recovery_target_time`. → Part 06 Ch3
82. **[M] What is replication and the main topologies?** A: Copying data to replicas: primary-replica async (replicas may lag — reads can be stale), synchronous (commit waits for acks — RPO=0, higher latency), and multi-master / consensus (Raft/Paxos — strong consistency). Used for HA, read scaling, and disaster recovery. → Part 06 Ch3
83. **[H] TRICKY: Async replica + primary crash = data loss. Explain.** A: The primary commits a write (durable locally) but the async replica never received it before the crash; failover to the replica loses those last writes (RPO > 0). Fix: synchronous replication or quorum-commit (consensus) for RPO=0 — at a latency cost. → Part 06 Ch3
84. **[H] What is the "durability" guarantee exactly in Postgres with `synchronous_commit=off`?** A: With off, a transaction can commit before the WAL is fsynced (or before sync replicas ack) — durability is weakened: on crash you may lose recent commits. It's a latency/durability trade-off for non-critical workloads; default is `on`. → Part 06 Ch2/3

### Part 07 — Query Processing & Optimization (Q85-92)
85. **[E] What are the main steps of query processing?** A: Parsing → rewriting/transformation → query optimization (logical + physical plan selection) → execution. Parser validates; optimizer chooses access paths/join orders/algorithms by cost. → Part 07 Ch1
86. **[M] What are the join algorithms and their trade-offs?** A: Nested-loop (for each outer row, probe inner — great with small outer + indexed inner), block nested-loop (block-level for small tables), merge join (both inputs sorted — good for pre-sorted/large equal-key joins), hash join (build hash on smaller side, probe — best for large equi-joins when unsorted). Cost: NLJ O(n·m) worst; merge O(n+m) sorted; hash O(n+m) build+probe. → Part 07 Ch1
87. **[M] How does hash join work, and why is it usually best for big equi-joins?** A: Build a hash table on the *smaller* input's join key, probe each row of the larger input — O(n+m) with good hashing, no sorting. Wins when inputs are large and unsorted; spills to disk when the build side exceeds memory (partition/grace hash join). → Part 07 Ch1
88. **[M] What are the cardinality estimation methods?** A: Table statistics (row counts), histograms on columns (selectivity of `col > x`), distinct-value counts (n_distinct), and correlation/independence assumptions. Wrong estimates → wrong join orders → slow queries. → Part 07 Ch1
89. **[H] What is the system-R cost model?** A: The classic cost formula: total cost = disk I/O (pages read/written) + CPU (tuple processing) + memory factors, computed per operator and summed up the tree; the optimizer picks the min-cost plan. Basis for modern cost-based optimizers. → Part 07 Ch1
90. **[M] What is predicate pushdown and why is it so valuable?** A: Moving `WHERE`/`JOIN` filters to the base scans (as early as possible) so each operator processes fewer rows — reduces I/O and intermediate sizes, enables index selection. One of the optimizer's highest-value transformations. → Part 07 Ch2
91. **[M] What is a covering index / index-only scan in the context of the optimizer?** A: When the index leaves contain every column the query needs, the plan skips heap fetches entirely — the cheapest scan; the optimizer picks it when available (Postgres `Index Only Scan`, MySQL `Using index`). → Part 07 Ch2
92. **[H] TRICKY: Why might the optimizer pick a Seq Scan on a 10M-row table?** A: Low selectivity (predicate matches most rows — index adds random I/O), covering whole-table needs, or stale statistics making estimates wrong. Diagnose with EXPLAIN: if estimated rows are way off actual, refresh stats (ANALYZE) before "fixing" the plan. → Part 07 Ch2

### Part 08 — NoSQL (Q93-100)
93. **[E] Name the four NoSQL families with an example each.** A: Key-value (Redis, DynamoDB), document (MongoDB, CouchDB), wide-column/columnar (Cassandra/ClickHouse), graph (Neo4j, Neptune). Each optimizes a different access pattern. → Part 08 Ch1
94. **[M] What is CAP and why is it often misunderstood?** A: During a network *partition*, you choose Consistency (all reads see latest writes) or Availability (every request answered). Misunderstood as "pick 2 of 3 always" — it's about partition *behavior*, and PACELC adds the always-on latency/consistency trade. → Part 08 Ch1
95. **[M] What is ACID vs BASE?** A: ACID: strong guarantees for transactional systems. BASE: basically available, soft state, eventual consistency — relaxed guarantees for scale/availability; data converges but may be stale/lost temporarily. → Part 08 Ch1
96. **[M] What is eventual consistency and when is it acceptable?** A: Replicas may disagree briefly but converge given no writes. Acceptable when stale reads are harmless (feeds, counters, caches, sessions) and LWW losses are OK; not for money/inventory/unique-constraint data. → Part 08 Ch1
97. **[M] Redis vs Memcached?** A: Memcached: pure in-memory cache (strings, eviction, no persistence). Redis: data structure server — typed values (lists, sets, sorted sets, hashes), RDB/AOF persistence, TTL, pub/sub, Lua — used as cache *and* beyond. → Part 08 Ch1 §2
98. **[M] Cassandra vs MongoDB — when each?** A: Cassandra: write-heavy, always-available, LSM, query-by-partition-key + time-range, LWW (telemetry/messaging). MongoDB: rich queries, flexible schemas, per-document CRUD, `$lookup` for limited joins — but single-writer-per-shard and index-maintenance write cost. → Part 08 Ch1 §2/3
99. **[M] What is LSM and why does it make writes fast?** A: Log-structured merge tree: writes go to a durable commit log + in-memory memtable, then flush to immutable sorted SSTables merged by compaction. No in-place updates/locks → O(1)-ish appends that scale horizontally. → Part 08 Ch1 §3
100. **[H] TRICKY: Design a system — "like button" counter that can handle 100M likes on one post. Where does it go?** A: A single hot counter breaks Cassandra's partitioning and Postgres's single-row write path. Options: Redis `INCR` (O(1), LWW-tolerant, TTL-less for the hot row) with async persistence to the DB; or partition the counter (fan-out by shard suffix, sum on read); or use a KV with hash-partitioned counter shards. Eventual consistency is fine for a like count. → Part 08 Ch1

## 14. Follow-Up Questions
1. **Q: "Why is hash join better for this big unsorted join?"** → Use Part 07 §2's algorithm comparison + the cost formula.
2. **Q: "What would break in your answer if the data were skewed?"** → Connect to histograms, selectivity, hot partitions (Part 07/08).
3. **Q: "How would you reproduce/verify this in production?"** → EXPLAIN ANALYZE + pg_stat_statements (Part 07 §2/3).
4. **Q: "Does your answer change at 10x the scale?"** → The scale-dial: partitioning, caching, NewSQL/consensus (Part 08).

## 15. Coding Example
```sql
-- Rehearse the "3 readings" example (Q61) in SQL
-- Dirty read: prevented by READ COMMITTED
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN;
SELECT balance FROM accounts WHERE id=1;   -- snapshot now
-- (another txn commits a change) → re-run → new value (non-repeatable at RC!)
SELECT balance FROM accounts WHERE id=1;   -- different value → non-repeatable read
COMMIT;

-- Non-repeatable vs phantom: check SERIALIZABLE
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
SELECT count(*) FROM accounts WHERE balance > 1000;  -- 3
-- (another txn inserts row with balance 5000)
SELECT count(*) FROM accounts WHERE balance > 1000;  -- still 3 (phantom prevented)
COMMIT;
```
```sql
-- The "covering index / index-only scan" demo (Q46/91)
CREATE INDEX idx_orders_cov ON orders (customer_id) INCLUDE (total);
EXPLAIN SELECT customer_id, total FROM orders WHERE customer_id = 42;
-- Index Only Scan (Postgres) / Using index (MySQL) — no heap fetch
```

## 16. Industry Usage
- The 100-question set mirrors the question banks used in top-tier loops (FAANG-adjacent), standard DBA/backend tracks, and university interview prep — it's the *intersection* of what actually gets asked.
- Structured oral practice (peer mock interviews) uses exactly this format: pick random Q numbers, answer aloud, receive "why?" probes.
- Companies that run written/technical screens reuse these patterns verbatim (index + isolation + normalization + SQL window functions are the perennial core).

## 17. References
- Every part's References section (all 22-block files) — the depth behind each answer.
- Silberschatz, *Database System Concepts*, 7th ed. (canonical).
- "Database Design" and "How to Answer Interview Questions" playbooks (System Design Interview by Alex Xu, parts on data).
- LeetCode-style SQL practice for Q-set challenges (Part 08 Ch2 §3).

## 18. Cheat Sheet
- Answer shape: define → mechanism → trade-off → example.
- Map Q → part: 1-14 fundamentals, 15-28 relational/SQL, 29-42 normalization, 43-56 indexing, 57-70 transactions, 71-84 recovery, 85-92 query processing, 93-100 NoSQL.
- Difficulty: E = recall, M = mechanism, H = edge/production.
- Core "why?" probes: dirty/non-repeatable/phantom (Q61), B+tree vs alternatives (Q53), hash vs merge vs NLJ (Q86), LWW/CAP (Q94/97), covering index (Q46), checkpoint/ARIES (Q73/75).
- Always have one example ready per topic — the example is what separates memorization from understanding.

## 19. Quiz
1. The covering index avoids: a) the sort b) the heap fetch c) the scan d) the log → **b**
2. HAVING filters: a) rows b) groups c) both d) neither → **b**
3. BCNF failure case: a) transitive dep b) determinant-not-a-key c) repeating groups d) MVD → **b**
4. Recovery redo applies: a) only committed b) all logged changes (then undo losers) c) nothing d) index pages → **b**
5. LSM writes are fast because: a) locking b) append-only + memtable c) B-tree d) compression → **b**
6. CAP's P means: a) always b) during partition c) never d) performance → **b**
7. Hash join build side should be: a) larger b) smaller c) sorted d) indexed → **b**
8. WORK_MEM is: a) global b) per-operation c) per-connection d) per-table → **b**

## 20. Flashcards
- **Q: 3-read anomaly ladder?** → **A:** Dirty (RC), non-repeatable (RR), phantom (Serializable).
- **Q: 2PL two phases?** → **A:** Growing (acquire only), shrinking (release only); strict = hold till commit.
- **Q: ARIES 3 phases?** → **A:** Analysis, redo, undo.
- **Q: Checkpoint purpose?** → **A:** Bound recovery scope (start redo at last checkpoint).
- **Q: Join algorithms?** → **A:** NLJ (small+indexed), merge (sorted), hash (big equi-join).
- **Q: Composite index leftmost rule?** → **A:** Use starts at the leftmost column.
- **Q: 4NF kills?** → **A:** Multi-valued dependencies.
- **Q: B+tree height for billions?** → **A:** ~3-4 disk reads.
- **Q: CAP during?** → **A:** Partitions.
- **Q: LSM write path?** → **A:** Commit log → memtable → SSTable → compaction.

## 21. Revision
100 questions = the full syllabus compressed into rehearsable answers: fundamentals → relational/SQL → normalization → indexing → transactions → recovery → query optimization → NoSQL. Answer shape everywhere: define → mechanism → trade-off → example. Use as checklist: mark gaps, re-read the mapped part, retest aloud. The "why?" probes (3-read ladder, B+tree choice, hash vs merge, CAP, LWW, covering index) are the differentiators — drill those hardest.

## 22. What Interview Questions Come From This Section?
This *is* the interview question set — the whole file. Use it directly as:
| Interview question | Source section |
|---|---|
| All 100 questions | Section 13 |
| Answer-shape guidance ("define→mechanism→trade-off→example") | 2, 9 |
| Gap-detection workflow | 2, 3 |
| "Why?" probe preparation | 13 (H-tier) |
| Day-before rapid pass | 3, 10 |
