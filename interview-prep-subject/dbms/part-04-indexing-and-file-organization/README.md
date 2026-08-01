# Part: Indexing & File Organization

## What this part covers
The **physical layer** — how rows physically live on disk and how the database finds them fast. It covers file organization methods (heap, sorted, hashed) and why clustered vs non-clustered is the single highest-leverage storage decision, then goes deep on the data structures that make databases fast: B-trees and B+-trees (the default index in Postgres, MySQL, Oracle, SQL Server), hash indexes (including Postgres hash partitions and MySQL adaptive hash index), bitmap indexes (OLAP/analytics), and the index *strategies* real systems use (covering, partial, composite, unique, INCLUDE). This is where "why is this query slow?" interview answers come from.

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| ch-01 File Organization | File organization methods (heap/sorted/hashed), clustered vs non-clustered | Pick the right physical layout for a workload, explain exactly what clustering does to both the table and secondary indexes |
| ch-02 Indexing | Indexing concepts & types, B-tree & B+-tree in depth, hash indexing, bitmap & other index types, index strategies in Postgres & MySQL | Describe B+-tree insert/delete with a worked example, compute fan-out and tree height, compare B+ tree vs hash vs bitmap, design composite/covering/partial indexes for real queries, read `EXPLAIN` index usage |

## Study order
1. **ch-01** first — indexing is meaningless without knowing what the heap vs clustered layout stores.
2. **ch-02** second — B+ tree is the star; spend the most time there. Then hash, bitmap, then strategies to tie it all to real SQL.
Read every section in numbered order within a chapter; each section assumes the previous one.

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ⭐⭐⭐⭐ (4/5)** — high frequency in *every* DB round as "how does an index work?" and in *every* SQL round as "why is this query slow / what index would you add?".
- **Emphasized by**: **backend SWE at Amazon, Google, Meta, Microsoft** (index design in system design), **DB core teams** (Postgres, MySQL, Oracle, SQLite, MongoDB — B+ tree internals are a must), and **data platform teams** (Snowflake micro-partitions, ClickHouse). Any interviewer who mentions `EXPLAIN` is probing this part.
- Typical asked: "B+ tree vs B-tree", "clustered vs non-clustered", "what index for `WHERE a=1 AND b>2`?", "why does my write slow down with many indexes?", "hash index vs B+ tree".

## How the parts connect (roadmap)
- Built on **Part 01's** internal-schema layer and **Part 02's** SQL — every index exists to serve a specific SQL predicate.
- **Part 03's** denormalization chapter pairs with indexing: both serve read-heavy workloads.
- Later **transaction/concurrency** parts explain how indexes and lock granularity interact (page vs record locks), and **query optimization** parts explain cost-based selection of the indexes you design here.
