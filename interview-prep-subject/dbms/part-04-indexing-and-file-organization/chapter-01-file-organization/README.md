# Chapter: File Organization

## What you'll learn
- **File organization methods**: how rows are physically placed on disk — heap (unordered), sorted, and hashed files — and how each supports record search, insert, and delete differently.
- **Clustered vs non-clustered organization**: when row order on disk *matches* a key order (clustered) versus when it doesn't (non-clustered); why clustered tables read ranges fast but pay on inserts, and how this maps to InnoDB and PostgreSQL storage.

## Prerequisites (linked)
- [Part 01 (DBMS Fundamentals)](../../part-01-dbms-fundamentals/README.md) — [Chapter 02 (DBMS Architecture)](../../part-01-dbms-fundamentals/chapter-02-dbms-architecture/README.md) for the storage manager and buffer pool context.
- Feeds into [Chapter 02 (Indexing)](../chapter-02-indexing/README.md) — indexes are data structures layered *on top of* these file organizations.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — File Organization Methods: Heap, Sorted, Hashed](section-01-file-organization-methods-heap-sorted-hashed.md) | Heap append-only; sorted by key for range scans; hashed for exact lookups; IO cost per operation |
| [Section 02 — Clustered vs Non-clustered Organization](section-02-clustered-vs-non-clustered-organization.md) | Physical row order vs index order; InnoDB clustered tables; PostgreSQL heap; trade-offs |

## One-paragraph narrative connecting all sections
How you *lay rows on disk* decides the IO cost of every query, so it's the first thing a storage engine gets right. **Heap files** (Section 01) append records and support fast inserts and full scans but force O(N) search; **sorted files** order records by a key so binary search makes equality and range lookups O(log N) — at the price of slow inserts that must shift or append+reorder; **hashed files** make exact-key lookups O(1) but kill range queries. Since no single layout wins everything, engines add a second layer — **clustered vs non-clustered** organization (Section 02) — where *one* ordering is physical (the clustered key, e.g., InnoDB's primary key or a table's only ordering) and everything else references it. That's why PostgreSQL stores rows in a heap and orders only via indexes, while MySQL/InnoDB physically orders rows by the primary key. Master this chapter and indexing (Chapter 02) becomes "a few more trees and hashes built on top of these files."

## Common interview trap in this chapter
Candidates claim a sorted file gives O(log N) *updates* — it doesn't: binary search finds the record in O(log N), but the file may still need shifting/reordering to stay sorted, making inserts/updates O(N). Second trap: confusing "clustered index" with "any index on a primary key" — a clustered index *physically orders rows* by that key, so a table can have **at most one** clustered index; PostgreSQL has no clustered index by default (rows live in a heap). Third: assuming a hash file is a hash *index* — hashing is a file-organization choice (rows placed by hash bucket), distinct from a hash index structure layered on a heap.

## Checklist before moving on
- [ ] I can compare heap vs sorted vs hashed files across insert/search(range)/search(exact)/delete with costs.
- [ ] I can explain why sorted files are bad for writes and hashed files are bad for ranges.
- [ ] I can explain the "at most one clustered index" rule and what physically clustering buys.
- [ ] I can contrast InnoDB's clustered-PK storage with PostgreSQL's heap + secondary indexes.
- [ ] I can describe how a B+ tree index (Chapter 02) would sit on top of each file organization.
- [ ] I can state when a heap file with a secondary index is preferable to a sorted file.
