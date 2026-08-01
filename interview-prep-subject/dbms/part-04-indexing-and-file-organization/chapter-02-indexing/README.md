# Chapter: Indexing

## What you'll learn
- **Indexing concepts & types**: what an index is, clustered vs secondary, dense vs sparse, primary vs secondary, single vs composite, and the read/write/space trade.
- **B-tree & B+ tree in depth**: the structure, fan-out, why height is tiny (log_{f} N), why B+ trees beat B-trees for DBs, leaf-level linked lists, and insert/delete/split/merge mechanics.
- **Hash indexing**: static vs dynamic (extendible/linear), O(1) exact lookups, why ranges fail, and where DBs use hash indexes (Postgres, MySQL MEMORY, NoSQL).
- **Bitmap & other index types**: bitmap indexes for low-cardinality columns, GIN/GiST/BRIN for JSON/full-text/ranges, and when each wins.
- **Index strategies in Postgres & MySQL**: composite index column order, covering indexes, index-only scans, partial indexes, and the classic "why is my index not used" diagnostics (EXPLAIN).

## Prerequisites (linked)
- [Part 04 Chapter 01 (File Organization)](../chapter-01-file-organization/README.md) — indexes sit on top of heap/sorted/hashed files; RIDs and clustering are the vocabulary used here.
- [Part 01 (DBMS Fundamentals)](../../part-01-dbms-fundamentals/README.md) — storage manager context from [Chapter 02](../../part-01-dbms-fundamentals/chapter-02-dbms-architecture/README.md).
- Feeds into Part 05+ (transactions/query processing) — index selection is how query optimizers make joins and scans fast.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Indexing Concepts and Types](section-01-indexing-concepts-and-types.md) | What an index is; dense/sparse; primary/secondary; composite; the read/write/space trade |
| [Section 02 — B-tree and B+ tree in Depth](section-02-b-tree-and-b-plus-tree-in-depth.md) | Structure, fan-out, height ~log_f(N), leaf links, splits/merges; why DBs prefer B+ trees |
| [Section 03 — Hash Indexing](section-03-hash-indexing.md) | Static/dynamic hashing, extendible & linear, O(1) point lookups, no ranges |
| [Section 04 — Bitmap and Other Index Types](section-04-bitmap-and-other-index-types.md) | Bitmaps for low cardinality; GIN/GiST/BRIN for JSON/full-text/range; full-text indexes |
| [Section 05 — Index Strategies in PostgreSQL and MySQL](section-05-index-strategies-in-postgres-and-mysql.md) | Composite order, covering/index-only scans, partial indexes, EXPLAIN diagnostics, real tuning |

## One-paragraph narrative connecting all sections
An index is a *redundant structure* that trades space and write cost for read speed — the layered payoff of Chapter 01's file organizations. **Concepts and types** (Section 01) fix the vocabulary: clustered vs secondary, dense vs sparse, single vs composite, and the fundamental read/write/space trade every index decision starts from. The workhorse structure is the **B+ tree** (Section 02) — a shallow, wide, balanced tree whose fan-out keeps height at 3–4 levels even for billions of rows, with all data in ordered leaves linked for range scans; it's why "seek ≈ 3 page reads" is the mental model of every DBA. For exact-match workloads, **hash indexing** (Section 03) is the O(1) alternative — extendible/linear hashing grow gracefully — but it abandons ordering, so ranges need the tree. **Bitmap and specialized indexes** (Section 04) cover the exotic but important cases: bitmap AND/OR for low-cardinality filters, GIN for JSON arrays and full text, GiST for geometry/ranges, BRIN for huge sorted tables. Finally, **strategies in Postgres & MySQL** (Section 05) turn theory into practice: composite key ordering, covering indexes, partial indexes, and reading EXPLAIN to diagnose why an index isn't used. Master the chapter and you can both design indexes and defend them.

## Common interview trap in this chapter
Candidates quote "O(log N) index lookup" and stop — but the *constant matters*: a B+ tree of height 3 with a fan-out of hundreds means **3 page reads**, not 3 comparisons; the "log" is on *fan-out* (block size), not base 2, and that's the whole point of the wide tree. Second trap: assuming an index on `(a, b)` helps queries on `b` alone — it does not (leftmost prefix rule), yet candidates keep claiming it. Third: confusing hash indexes with hash *files* and believing hashes support `BETWEEN`/`ORDER BY` — they never do. Fourth: "add an index and everything gets faster" — writes get *slower* (every insert updates every index), and the trade must be stated.

## Checklist before moving on
- [ ] I can draw a B+ tree, compute height from fan-out and N, and explain why leaf links make ranges cheap.
- [ ] I can compare B-tree vs B+ tree and state the three reasons DBs choose B+.
- [ ] I can contrast B+ tree vs hash index across point/range/insert/space.
- [ ] I can explain dense vs sparse, clustered vs secondary, composite leftmost-prefix.
- [ ] I can read an `EXPLAIN` output and tell why an index is or isn't used.
- [ ] I can design a composite index for a given query set and justify the column order.
- [ ] I can name GIN/GiST/BRIN/bitmap and one use case each.
