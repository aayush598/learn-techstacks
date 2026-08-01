# DBMS Crash-Course Revision

> **TL;DR**: The entire DBMS syllabus (Parts 01-08) distilled into one dense, high-signal revision sheet — definitions, mechanisms, trade-offs, and the canonical answers for each of the 8 parts, organized for a 90-minute to 2-hour rapid review in the 24-48 hours before an interview, ending with a final checklist.

## 1. Why Does This Exist?
By interview day, knowledge must be *indexed for recall*, not just understood in the moment. This crash course exists to compress the 8 parts into a single revisable artifact — the "one pass to re-wire everything" sheet. It exists because: (a) re-reading 8 parts of detailed material takes days, but a well-structured summary re-activates the same neural network in ~90 minutes; (b) interviewers reward *organized* recall — the ability to jump from "isolation levels" to "MVCC" to "ARIES" to "EXPLAIN" to "CAP" fluently — which is exactly what a cross-linked revision sheet trains; (c) it's the final confidence artifact: "I've reviewed everything, on one page-set, today." Without it, candidates either over-review (last-minute cramming scattered notes) or under-review (fading on the fundamentals under pressure).

## 2. How Does It Work?
The sheet is organized by the 8 parts, each condensed to four fixed slots:
1. **Core definitions** — the 3-5 terms that anchor the part.
2. **Key mechanisms** — how it actually works (the "how" that answers "why?").
3. **Trade-offs** — what you give up for what.
4. **Canonical interview answers** — the 2-3 sentences you'd say for the part's signature question.
Then a **cross-part connection map** (how the parts interlock) and a **final checklist**. Review protocol: (1) read a part block, (2) close the sheet and *say* the canonical answers aloud, (3) mark weak spots and jump to the source part's Section 13 for depth, (4) finish with the connection map to rehearse the "big picture" narrative.

## 3. When Is It Used?
- 24-48 hours before the interview: two full passes (today: parts 1-4; tomorrow: parts 5-8 + connections).
- The morning of: one rapid pass of the canonical answers + checklist.
- Gap detection during prep: mark any block you can't speak → re-read the source part section.
- Peer-review sessions: have a friend call part numbers, you recite the canonical answers.
- Before mocks: a 10-minute warm-up pass so the mocks test recall, not lookup.

## 4. Why Wasn't Another Approach Chosen?
- *Full re-read of all parts*: depth is where understanding lives, but days-before-cramming re-reading is the wrong motion — the crash course *reactivates* what the parts built; re-reading is for first-time learning.
- *Only flashcards*: cards train recall of facts, not the *spoken answer shape* the interview rewards; this sheet includes the canonical answers as you'd say them.
- *Only the 100-question bank*: that's the rehearsal script (Part 08 Ch2 §1); this is the *structure* underneath it — the map that lets you navigate any question to its part.
- *Scattered summaries*: a single coherent sheet beats fragmented notes because the *connections* (Part 04's index → Part 07's EXPLAIN → Part 08's hot-key fix) are the actual interview asset.
- *Skipping review entirely*: fluency needs reactivation; even a strong candidate benefits from a same-day pass (recency wins recall).

## 5. Intuion
The crash course is the **index at the back of a textbook** — it doesn't teach, it *locates*. On interview day, when a question lands ("what's the difference between a clustered and non-clustered index?"), your mind needs to navigate: *indexing → clustered vs secondary → mechanism (physical order vs pointer) → trade-off (one vs many, sequential vs random) → example (InnoDB PK)* — in under 10 seconds. The index-style structure trains exactly that navigation: each part block is a node, the canonical answers are the edges that lead to the right node fast. And like a good index, it's *hierarchical*: part → key concept → mechanism → answer. Under pressure, that hierarchy is what converts panic into a structured, fluent response.

## 6. Real-World Analogy
A **pilot's quick-reference checklist (QRC)**. The pilot doesn't re-read the full flight manual at the gate; she runs the QRC — one dense page-set that condenses every normal and emergency procedure into its critical steps and triggers. The QRC exists *because* the manual exists: it reactivates trained procedures in the seconds available, when recall must be fast and structured. The DBMS crash course is your QRC: it condenses the 8-part "manual" into the critical recall blocks (definitions, mechanisms, trade-offs, answers) so that under interview pressure — the equivalent of an engine indication at 3,000 feet — you don't fumble through the manual; you execute the checklist. It cannot make you a pilot; it makes the trained pilot *fast*.

## 7. Formal Definition
A compressed, cross-linked revision artifact covering Parts 01-08, structured per part as (definitions → mechanisms → trade-offs → canonical spoken answers), plus a connection map and final checklist. Designed for rapid reactivation (90-120 min full pass), gap detection (self-recitation), and the "big picture" narrative interviewers test when they ask "how do all the pieces fit together?" It is a *router* to the source parts, not a replacement for them.

## 8. Example
**Part 05 block (condensed):**
- **Definitions**: transaction, ACID, schedule, serializability (conflict/view), isolation levels, 2PL, timestamp protocol, MVCC, deadlock.
- **Mechanisms**: 2PL = growing/shrinking phases → conflict-serializable; strict 2PL holds locks to commit (no cascading abort). Timestamp = order + reject/restart. MVCC = xmin/xmax versions + snapshot → readers never block writers. Postgres = MVCC (snapshot isolation); SERIALIZABLE = SSI (write-skew detection). InnoDB RR = MVCC + gap/next-key locks.
- **Trade-offs**: locks (deadlock risk, blocking) vs timestamps (restart cost) vs MVCC (bloat, vacuum, write-skew) vs optimistic (retry cost); isolation strength vs concurrency/latency.
- **Canonical answers**: (1) "The three read anomalies are dirty, non-repeatable, and phantom; READ COMMITTED, REPEATABLE READ, and SERIALIZABLE each add prevention. Postgres's MVCC actually prevents phantoms at REPEATABLE READ too." (2) "MVCC gives each reader a consistent snapshot so readers never block writers; old versions are cleaned by VACUUM; its residual anomaly is write skew, caught by SERIALIZABLE/SSI."
→ Part 05 Ch1-3 for depth.

## 9. Internal Working
The revision protocol's mechanism is *retrieval practice*: reading a compressed block is weak encoding; *reciting it aloud* from memory (closing the sheet) is what builds the retrieval path interview day uses. The connection map works by cross-linking (Part 04 index feeds Part 07's EXPLAIN scan choice; Part 05 isolation feeds Part 08's consistency vocabulary; Part 06 WAL feeds Part 07's durability reasoning and Part 08's "never cache authoritative state"). The checklist operationalizes readiness: if every canonical answer comes out clean and every connection is named, the prep is done — further review has diminishing returns, and the advice is to stop and rest rather than cram new material.

## 10. Time Complexity
- Full pass (recite everything): 90-120 min.
- Targeted pass (only weak blocks, marked in prep): 30-45 min.
- Morning-of rapid pass (canonical answers + checklist only): 15-20 min.
- The *value*: hours of scattered review compressed into one structured hour — retrieval practice is provably more effective than re-reading for retention, and this sheet makes that practice structured.

## 11. Advantages
- **One artifact for the whole syllabus** — no scattered notes.
- **Spoken-answer training** — the canonical answers are the interview motion.
- **Gap detection built-in** — self-recitation reveals weak blocks.
- **Cross-linked** — trains the "big picture" narrative interviews test.
- **Time-boxed** — a complete review fits in ~2 hours; no cramming spiral.
- **Router to depth** — each block back-references the full source part for fixes.

## 12. Disadvantages
- **Compression loses nuance** — the source parts hold the edge cases (follow-up probes need them).
- **Reactivation ≠ learning** — it cannot substitute for the first-time learning in the parts.
- **Can encourage shallow recitation** — must pair with the "why?" practice from the parts, not just the canonical answer.
- **Static view** — real questions reword the canonical ones; the connection map is what generalizes, so it must be *used*, not skimmed.

## 13. Interview Questions
(The crash course itself is the answer sheet; the blocks below are the condensed content. In interview terms: every question in the Top-100 (§1) routes to exactly one block here.)

**Part 01 — Fundamentals.**
- Definitions: DBMS, three-schema, data independence, OLTP vs OLAP, ACID, buffer pool.
- Mechanisms: storage manager + buffer pool (LRU) → query processor (parser→optimizer→executor) → transaction manager (CC + recovery).
- Trade-offs: row vs column (OLTP vs OLAP); generality vs specialization.
- Canonical: "A DBMS is software that manages storage, retrieval, concurrency, integrity, and recovery. The three-schema architecture gives logical and physical data independence."
→ Part 01

**Part 02 — Relational Model & SQL.**
- Definitions: relation, keys (super/candidate/primary/foreign), integrity constraints, view, joins, GROUP BY/HAVING.
- Mechanisms: FK enforces referential integrity; view = stored query; HAVING filters groups post-aggregation.
- Trade-offs: normalization purity vs read joins; view flexibility vs performance.
- Canonical: "A relation is a table with a key and constraints. Foreign keys enforce referential integrity. WHERE filters rows before grouping; HAVING filters groups after."
→ Part 02

**Part 03 — Normalization.**
- Definitions: FD, 1NF-5NF, BCNF, lossless join, dependency preservation, denormalization.
- Mechanisms: decompose via FDs; 2NF kills partial, 3NF kills transitive, BCNF requires every determinant a key, 4NF kills MVDs.
- Trade-offs: less redundancy/update anomalies ↔ more joins; BCNF vs 3NF (dependency preservation).
- Canonical: "Normalization removes redundancy and update anomalies via functional dependencies. 3NF is the practical target; BCNF is stricter but may sacrifice dependency preservation. Denormalization re-adds redundancy deliberately, after profiling."
→ Part 03

**Part 04 — Indexing & File Organization.**
- Definitions: B+ tree, clustered vs secondary, covering, composite (leftmost prefix), hash/bitmap, bloat.
- Mechanisms: B+ tree = high fanout, height 3-4, leaves linked → equality + range; clustered = physical order (one); covering = index-only scan.
- Trade-offs: read speed ↔ write/storage cost; clustered vs secondary; selectivity decides index worth.
- Canonical: "The B+ tree is the default index — high fanout keeps height ~3-4 for billions of rows, and leaf links give range scans. A covering index holds all needed columns so we skip the heap. Composite indexes follow the leftmost-prefix rule."
→ Part 04

**Part 05 — Transactions & Concurrency.**
- Definitions: ACID, schedule, serializability, isolation levels, 2PL, timestamp, MVCC, deadlock, write skew.
- Mechanisms: 2PL (growing/shrinking; strict = hold to commit); timestamp (order + reject/restart); MVCC (versions + snapshot; readers don't block); InnoDB RR = MVCC + gap locks.
- Trade-offs: locks (deadlock/blocking) vs timestamps (restarts) vs MVCC (bloat/write-skew) vs optimistic (retries); isolation vs concurrency/latency.
- Canonical: "The three anomalies are dirty, non-repeatable, and phantom reads; READ COMMITTED, REPEATABLE READ, SERIALIZABLE add prevention in turn. MVCC gives snapshots so readers never block writers; Postgres's REPEATABLE READ also stops phantoms, and SERIALIZABLE (SSI) catches write skew."
→ Part 05

**Part 06 — Recovery.**
- Definitions: failure types, WAL, ARIES (analysis/redo/undo), LSN, checkpoint, shadow paging, backup types, PITR, replication.
- Mechanisms: WAL = log record flushed before page; ARIES replays from last checkpoint (redo) then undoes losers (CLRs); LSN skips already-flushed pages; PITR = base backup + archived WAL.
- Trade-offs: durability (fsync/sync replication) ↔ latency; async replica RPO>0 vs sync/consensus RPO≈0.
- Canonical: "Write-ahead logging flushes the log before the page, so recovery knows committed work is logged. ARIES does analysis, redo, then undo with LSNs to skip flushed pages. Point-in-time recovery restores a backup and replays archived WAL to a target time."
→ Part 06

**Part 07 — Query Processing & Optimization.**
- Definitions: pipeline, join algorithms (NLJ/merge/hash), cost estimation, EXPLAIN, transformations, tuning loop.
- Mechanisms: hash join builds the smaller side, probes the larger — best for big equi-joins; optimizer transforms (pushdown, unnest) then costs physical plans; EXPLAIN ANALYZE compares estimates vs actuals.
- Trade-offs: NLJ (small+indexed) vs merge (sorted) vs hash (big unsorted); planning cost vs execution; index vs seq scan by selectivity.
- Canonical: "Join algorithms: nested-loop for small outer with indexed inner, merge for sorted inputs, hash for large equi-joins — hash usually wins. The optimizer transforms the query (predicate pushdown, subquery unnesting) then picks the cheapest physical plan. EXPLAIN ANALYZE compares estimated and actual rows to find where plans go wrong."
→ Part 07

**Part 08 — NoSQL & Decision Guide.**
- Definitions: 4 families, CAP/PACELC, ACID vs BASE, eventual consistency, LSM/LWW, cache patterns.
- Mechanisms: KV = O(1) by-key; document = flexible schema, no joins; wide-column = write-heavy LSM, partition+clustering; columnar = scan-optimized; graph = adjacency traversal; CAP during partitions; PACELC elsewhere.
- Trade-offs: scale/availability ↔ consistency/query generality; strong vs eventual; cache freshness vs correctness.
- Canonical: "NoSQL trades ACID/general queries for scale and availability. Four families fit four patterns: by-key → KV, flexible objects → document, write-heavy + availability → wide-column, scans → columnar, traversal → graph. CAP governs behavior during partitions; PACELC adds the latency cost otherwise. Default to SQL; deviate only when a pattern dominates."
→ Part 08

## 14. Follow-Up Questions
1. **Q: "Connect these topics" (isolation, indexes, EXPLAIN, CAP).** → Use the connection map: an index (04) is *chosen by the optimizer* (07) which *needs fresh stats* (07 §3); isolation (05) is the *vocabulary* for consistency (08); WAL durability (06) underlies "never cache authoritative state" (08 §2).
2. **Q: "Why did this production query degrade?"** → Stale stats → bad plan → EXPLAIN shows it → ANALYZE/index/memory fix → verify (Part 07 §3).
3. **Q: "Explain the same idea to a non-engineer."** → Use the part analogies (airport transfer map for graph, kitchen checklist for tuning, recipe prep-list for EXPLAIN).

## 15. Coding Example
```sql
-- The 4 commands that close the whole loop (index → plan → verify)
ANALYZE orders;                                   -- refresh stats (Part 07 §3)
CREATE INDEX idx_orders_cov ON orders (customer_id) INCLUDE (total);  -- Part 04
EXPLAIN (ANALYZE, BUFFERS)                        -- Part 07 §2
SELECT customer_id, total FROM orders WHERE customer_id = 42;
-- expect: Index Only Scan, estimates ≈ actuals
```
```sql
-- The isolation → consistency → NoSQL bridge
BEGIN ISOLATION LEVEL REPEATABLE READ;           -- Part 05: snapshot
SELECT * FROM accounts WHERE id = 1;
COMMIT;
-- the same "snapshot" idea, relaxed, is what eventual consistency is NOT
-- (Part 08: LWW/counters are eventual-OK; balances are not)
```

## 16. Industry Usage
- The crash-course format mirrors the "last-minute review" sheets used across interview-prep programs (DataLemur, StrataScratch, interview-prep repos): one dense, cross-linked artifact run right before the interview.
- It doubles as the *knowledge map* for mocks — peers call parts, you recite; the same format senior engineers use when refreshing for a new role.
- The connection map is the "how does it all fit?" answer — a common final-round prompt.

## 17. References
- All 8 parts' files (the depth behind each block) — routed via the Section 13 blocks.
- The Top-100 Q&A (§1 of this chapter) for rehearsal; the System-Design skeleton (§2) for the design layer; the SQL challenges (§3) for the coding round.

## 18. Cheat Sheet
- 8 blocks: Fundamentals / Relational+SQL / Normalization / Indexing / Transactions / Recovery / Optimization / NoSQL.
- Per block: definitions → mechanisms → trade-offs → canonical answer (say it aloud).
- Connection map: index(04) → optimizer(07) → stats(07§3); isolation(05) → consistency vocab(08); WAL(06) → "no cache of authoritative state"; EXPLAIN(07§2) verifies everything.
- The canonical answers are the interview motion — recite, don't skim.
- Final checklist (below) operationalizes "done".

## 19. Quiz
1. The crash course is best used: a) for first learning b) for reactivation before interview c) instead of the parts d) never → **b**
2. Retrieval practice means: a) re-reading b) reciting from memory c) highlighting d) copying → **b**
3. BCNF stricter than 3NF by: a) keys only b) every determinant a key c) MVDs d) repeating groups → **b**
4. MVCC's residual anomaly: a) dirty read b) write skew c) phantom d) lost update → **b**
5. PITR replays: a) redo only b) archived WAL to a time c) cache d) nothing → **b**
6. Hash join builds the: a) larger side b) smaller side c) both d) sorted side → **b**
7. CAP governs: a) always b) during partitions c) never d) performance → **b**
8. Default engine per the guide: a) Mongo b) relational c) Cassandra d) Redis → **b**

## 20. Flashcards
- **Q: 8 part blocks?** → **A:** Fund, Relational/SQL, Normalization, Indexing, Transactions, Recovery, Optimization, NoSQL.
- **Q: Per-block structure?** → **A:** Definitions → mechanisms → trade-offs → canonical answer.
- **Q: Why recite aloud?** → **A:** Retrieval practice builds the interview recall path.
- **Q: Index → optimizer link?** → **A:** Optimizer picks access paths; needs fresh stats (ANALYZE).
- **Q: Isolation → NoSQL link?** → **A:** Isolation vocabulary = consistency vocabulary (strong vs eventual).
- **Q: WAL → caching link?** → **A:** Durability is why you never cache authoritative state.
- **Q: Best time to run?** → **A:** 24-48h before + morning-of rapid pass.

## 21. Revision
Eight blocks — Fundamentals, Relational/SQL, Normalization, Indexing, Transactions, Recovery, Optimization, NoSQL — each condensed to definitions, mechanisms, trade-offs, and the canonical spoken answer. Recite aloud (retrieval practice), mark weak blocks, route to the source parts for fixes, and finish with the connection map (index→optimizer→stats; isolation→consistency; WAL→no-cache-authoritative; EXPLAIN verifies). Two passes (24-48h + morning-of) convert six weeks of study into interview-day fluency.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| Any part's signature question (all 8 blocks) | 13 |
| "How do all the DBMS pieces fit together?" | 2, 9, 13 |
| "Explain X to a non-engineer" | 14 |
| "Why did this query degrade?" | 14, 13 (Part 07 block) |
| Final self-check (canonical answers) | 13, 18, 21 |
