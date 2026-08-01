# File Organization Methods: Heap, Sorted, Hashed

> **TL;DR**: A file organization decides how rows are physically laid out on disk, which fixes the cost of each operation. **Heap files** append rows and win on inserts/full scans but pay O(N) for point lookups. **Sorted files** order rows by a search key so equality and range queries become O(log N) via binary search, but inserts/updates cost O(N) to maintain order. **Hashed files** place rows by a hash of the key for O(1) exact lookups while destroying range scans. Real engines mix them: the heap (PostgreSQL) plus indexes, or the clustered key (InnoDB).

## 1. Why Does This Exist?
Data lives on disk in pages, and reading is thousands of times slower than computing. If rows are scattered, every query becomes a full scan; if they're ordered, lookups get cheap; if they're hashed, exact hits are instant. A **file organization** is the deliberate choice of how to place records so the *dominant workload* reads as few pages as possible. There is no free lunch: the choice is a triangle among fast inserts (heap), fast range scans (sorted), and fast exact lookups (hash). Storage engines exist to pick the layout that matches real workloads — and every later optimization (indexes, clustering) is built on top of this raw layer. Understanding heap/sorted/hashed is understanding the *baseline* costs that indexes are measured against.

## 2. How Does It Work?
- **Heap (unordered)**: new records appended at the end of the file (or a free slot found via a free-list). Search = sequential scan, O(N). Full scans benefit from sequential IO. Delete marks a slot free; update often becomes delete+insert.
- **Sorted file**: records stored in ascending order of a *search key*; new records inserted in sorted position (with shifting or by appending and periodically re-sorting). Lookups use **binary search**, O(log N) comparisons, but still O(log N) page reads in the best case. Range scans read a contiguous run. Inserts/deletes cost O(N) in the worst case because of shifting.
- **Hashed file**: choose M buckets; bucket = `hash(key) mod M`; records with the same bucket stored together (each bucket may be a page or a chain). Point lookup: compute hash, read the bucket, scan it — O(1) expected. Range scans are impossible (order is destroyed); the file must be rehashed when buckets overflow (extendible/linear hashing).
- **Record addressing**: heap/sorted use a **record identifier (RID)** = (page, slot); hash files address by bucket. A RID is what an index ultimately stores.

## 3. When Is It Used?
- **Heap**: default for most OLTP row stores (PostgreSQL heap; MySQL/InnoDB also heap-like before clustering, and secondary indexes over heaps). Great when writes dominate and queries are point lookups *through an index*.
- **Sorted**: pre-relational and batch systems, read-mostly tables with range-heavy scans (e.g., append-only log tables clustered by time), columnar engines' sort orders (SORT BY in ClickHouse/Redshift).
- **Hashed**: exact-match workloads — key-value caches, lookups by primary key, partitioning by hash (Postgres declarative hash partitioning; Oracle/MySQL partition by HASH). Not for range/order queries.
- **Decision rule**: count your inserts vs range queries vs point lookups; the dominant one picks the layout.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: heap everywhere.** Fast writes, but O(N) point lookups → every equality query scans the whole file. Rejected for lookup-heavy workloads.
- **Alternative: sorted everywhere.** Great reads, but every insert rewrites/shifts rows (O(N)) → write-heavy OLTP would collapse. Rejected for write-heavy workloads.
- **Alternative: hash everywhere.** O(1) exact lookups but no ranges, no ordering, and rehashing pain. Rejected wherever ORDER BY / BETWEEN / joins-by-range matter.
- **Why not one universal layout?** Because the access pattern *differs per query*; the real answer is **a heap (or clustered key) plus secondary indexes** — the file is laid out for the dominant path, and indexes emulate the other two organizations on top. That hybrid is what all modern engines do.

## 5. Intuition
Think of **a phone book (sorted), a stack of unread mail (heap), and a coat-check room (hash)**.
- The **sorted phone book**: finding "Zulu" is fast (binary search), reading everyone in the "M" block is fast — but publishing a new edition (insert) means re-doing everything.
- The **mail pile**: adding a letter is O(1) (drop it on top), finding a specific bill is a frantic full search.
- The **coat-check room**: the attendant hands you the coat for ticket #23 instantly (hash of the ticket) — but you can't ask for "all blue coats" (no ordering).
The designer's job is deciding whether this workload needs searching (sorted), piling (heap), or ticket-lookup (hash) — and modern engines cheat by doing a heap for storage and putting "phone books" (indexes) on top.

## 6. Real-World Analogy
A **warehouse** deciding how to shelve 100k boxes. Option 1 — **heap**: forklift drops each box wherever there's room; receiving is instant, but finding "the red shoe box" means walking every aisle (O(N)). Option 2 — **sorted**: shelves ordered by SKU; the picker binary-searches to the exact aisle and grabs all "A-1000" range in one walk — but every new SKU insertion means reshuffling shelves (O(N)). Option 3 — **hash**: a sign at the door says "SKU → lane 37"; the picker goes straight to lane 37 (O(1)) — but the "show me everything below $10" request is impossible, and when lane 37 overflows you must re-sign the whole building. The warehouse manager picks based on what workers do most; DBAs pick file organization the same way.

## 7. Formal Definition
(Elmasri & Navathe Ch. 16–17; Silberschatz Ch. 13; Garcia-Molina, Ullman, Widom Ch. 13.)
- **Heap file**: records appended unordered; free slots tracked (free list). Search O(N) page reads.
- **Sorted file**: records ordered by a search key; search via binary search O(log₂ N); range scans O(span); insertion requires relocating/shifting (amortized O(N) worst).
- **Hashed file**: bucket address = h(K) for a hash function h; M primary buckets; collisions handled by chaining or open addressing; expected point lookup O(1); rehashing on overflow via extendible/linear hashing.
- **RID (tuple identifier)**: (page_id, slot_number) locates a record regardless of organization; secondary indexes store RIDs, not data.

## 8. Example
File of records with key `id`, N = 1,000,000 records, page holds ~100 records.
- **Heap**: insert = 1 page write (append). Point lookup by id = full scan ≈ 10,000 page reads (O(N)). Range scan = whole file.
- **Sorted by id**: point lookup = binary search ≈ log₂(1e4) ≈ 14 page reads. Range id∈[k,k+500] ≈ 5–10 page reads. Insert = find position (14 reads) + shift rest (≈ O(N) worst).
- **Hashed (M buckets)**: point lookup = 1 bucket read ≈ 1–2 page reads (O(1) expected). Insert = 1 bucket write. Range query = scan every bucket (impossible in practice).

| Operation | Heap | Sorted | Hashed |
|---|---|---|---|
| Point lookup | O(N) scan | O(log N) | O(1) expected |
| Range lookup | O(N) | O(span) fast | O(N) |
| Insert | O(1) append | O(N) shift worst | O(1) amortized |
| Delete | O(N)+mark | O(N) | O(1) amortized |
| Full scan | O(N) sequential | O(N) sequential | O(N) random |

## 9. Internal Working
1. **Heap**: maintain a header page pointing to first free page + free-list of empty slots; append or reuse a free slot; a slot directory keeps pages stable under splits.
2. **Sorted**: keep the file ordered on the search key; maintain an *overflow area* for new records, periodically merging the overflow into the main file (batching inserts to amortize cost — the classic "sorted file + overflow" trick).
3. **Hash**: choose M buckets sized to fit a page; bucket pages chained on overflow; when buckets saturate, either rehash the whole file (M → 2M) or use **extendible hashing** (directory doubling, split one bucket at a time) / **linear hashing** (incremental splits). Expected bucket length ≈ records/M.
4. **RIDs**: every record keeps an address (page, slot); the buffer pool caches pages; IO is counted in pages, so "O(log N)" means *page* reads, the real unit.

## 10. Time Complexity
- **Heap**: insert O(1); point search O(N) pages; full scan O(N) sequential; delete O(N)+O(1) mark.
- **Sorted**: search O(log N); range O(log N + result pages); insert/update O(N) worst (shift), O(1) amortized with overflow batching; delete O(N).
- **Hashed**: point O(1) expected, O(N) worst (all keys collide); insert O(1) amortized; range O(N); delete O(1) amortized.
- **Rehash**: O(N) when it happens; extendible/linear hashing amortize to O(1) per insert.
- Note: N is in *records*; page reads ≈ records/page.

## 11. Advantages
- **Heap**: simplest layout; fastest inserts; perfect sequential scans; no reordering; secondary indexes find RIDs cheaply.
- **Sorted**: excellent point and range reads; no index needed for the sort key; predictable IO; great for append-only + time-range analytics.
- **Hashed**: unbeatable exact lookups (O(1)); perfect for key-value and PK lookups; simple write path.
- **All three**: the *baseline* against which every index is justified; knowing them shows you understand physical storage.

## 12. Disadvantages
- **Heap**: O(N) point lookups without an index; updates fragment; no ordering.
- **Sorted**: O(N) inserts/updates; overhead to maintain order; the file must be fully rewritten on re-sort.
- **Hashed**: no ranges, no ORDER BY; collisions degrade to O(N); rehashing complexity; wasted space in sparse buckets.
- **General**: a single organization can't serve mixed workloads — which is precisely why indexes exist (Chapter 02).

## 13. Interview Questions
1. **Q: What are the three basic file organizations?** A: Heap (unordered append), sorted (ordered by a key), and hashed (rows placed by hash bucket).
2. **Q: Compare costs for point lookup.** A: Heap O(N) scan; sorted O(log N) binary search; hashed O(1) expected.
3. **Q: Compare costs for range lookup.** A: Heap O(N); sorted O(log N + result pages) — contiguous run; hashed O(N) (order destroyed).
4. **Q: Compare insert costs.** A: Heap O(1) append; sorted O(N) worst (shifting) but O(1) amortized with overflow batching; hashed O(1) amortized.
5. **Q (scenario): append-only log table, range-by-timestamp queries.** A: Sorted-by-timestamp (or clustered by time) — inserts are time-ordered (cheap append at the end), range scans read contiguous pages.
6. **Q (scenario): key-value lookup store.** A: Hashed file (O(1) exact lookups); ranges aren't needed.
7. **Q: What is a RID?** A: Record identifier (page number, slot number); indexes store RIDs to locate records without moving them.
8. **Q: How do modern engines actually organize rows?** A: A heap (PostgreSQL) or clustered key (InnoDB orders by PK); secondary indexes reference records via RID/PK. File organization + indexes = the real layout.
9. **Q (tricky): is a "sorted file" the same as a "clustered index"?** A: Conceptually related — both keep records ordered by a key — but clustered index is a *tree structure* with pages and pointers (Chapter 02/File Ch. 2), while a sorted file is a flat ordered run; a clustered index is a *dynamic* sorted file.
10. **Q: What is extendible hashing?** A: A hash scheme that doubles a directory (2^d buckets) and splits one bucket at a time on overflow, keeping most lookups at 2 page reads — amortized O(1).
11. **Q: What is linear hashing?** A: Incremental bucket splits without a full rehash; grows M by one as load crosses a threshold; amortized O(1).
12. **Q (scenario): table with frequent inserts AND frequent exact-PK lookups.** A: Heap + a hash or B+ tree PK index — heap absorbs writes, index serves lookups; don't use sorted (writes would shift rows).
13. **Q: Why is IO measured in pages, not records?** A: Disk transfers whole pages (typically 4–16 KB); a page holds many records, so "reading one record" costs reading its page. Cost = pages touched.
14. **Q: What are the consequences of a full scan on a heap vs sorted?** A: Both read every page; heap pages are contiguous (fast sequential IO), sorted also sequential — hash files scatter records (random IO, slower scans).
15. **Q (tricky): can a heap file have good point lookups?** A: Only with a secondary index — the index holds (key → RID) and turns the lookup into index-search + 1 page read. The *file* itself is still O(N) to scan.
16. **Q: When would you store rows sorted by a column that isn't unique?** A: When range/grouping queries dominate on that column (e.g., timestamp); duplicates are fine — binary search finds the first occurrence, then read the run.
17. **Q: What is bucket overflow handling?** A: Chaining (overflow buckets linked) or open addressing; beyond that, extendible/linear hashing rehash incrementally. Overflow degrades lookups toward O(N).
18. **Q (production): Postgres vs MySQL/InnoDB physical layout?** A: PostgreSQL: heap + RIDs, indexes point to RIDs (unclustered by default). InnoDB: clustered by primary key — rows are physically ordered by PK, secondary indexes store PK values (a "covering" property).
19. **Q: Why is a sorted file bad for OLTP?** A: Every insert/update may require shifting records (O(N)); OLTP does millions of tiny writes — a heap (or clustered tree) absorbs them.
20. **Q: How do columnar engines use sorted files?** A: They keep *column* data sorted by a chosen sort key (Redshift SORTKEY, ClickHouse ORDER BY) — the sorted-file idea applied per-column for compression and range pruning.

## 14. Follow-Up Questions
1. **Q: How does a buffer pool change these costs?** A: Frequently-read pages stay cached (LRU), so repeated lookups hit memory; but cold-cache costs are still governed by the organization — the O() analysis is the cold-case bound.
2. **Q: Heap + index vs sorted file — which wins?** A: Heap+index wins on writes; sorted wins on pure range scans of the whole key; the optimizer chooses via cost estimation. InnoDB's clustered PK is the hybrid: tree keeps order, inserts are page splits not shifts.
3. **Q: What does "clustered" mean physically?** A: The *data pages* are kept in key order, so a range scan on the key is contiguous IO; only one such order can exist per table.
4. **Q: How do hash partitioning (Postgres) relate to hashed files?** A: Partitioning routes each row to a partition by hash — a file-organization decision at the table level; each partition then has its own layout.
5. **Q: Where do sorted files shine in analytics?** A: Time-series: ORDER BY timestamp ⇒ range scans read contiguous pages and compression improves (runs of similar values) — the reason log/event tables cluster by time.

## 15. Coding Example
```sql
-- No SQL directly controls file organization, but the design choices show up:
-- 1) HEAP-ish default: Postgres stores rows in a heap; an index makes lookups fast:
CREATE INDEX idx_users_email ON users(email);   -- (email -> RID) over the heap

-- 2) SORTED-ish design: order matters; cluster by a sort key for range reads
--    (Postgres: physical reorder, one-time):
CLUSTER users USING idx_users_created_at;        -- rewrite table in index order

-- 3) HASH-partitioned layout (rows distributed by hash of a key):
CREATE TABLE events (
  id BIGINT, ts TIMESTAMPTZ, payload JSONB
) PARTITION BY HASH (id);
CREATE TABLE events_p0 PARTITION OF events FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE events_p1 PARTITION OF events FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE events_p2 PARTITION OF events FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE events_p3 PARTITION OF events FOR VALUES WITH (MODULUS 4, REMAINDER 3);
-- exact id lookup -> one partition (≈ O(1) bucketing)
```
```python
# Cost model sketch: pages touched per operation
def heap_search_cost(n_records, records_per_page):
    return n_records / records_per_page          # full scan, all pages

def sorted_search_cost(n_records, records_per_page):
    pages = n_records / records_per_page
    import math
    return math.log2(pages)                       # binary search on pages

def hashed_lookup_cost():
    return 1.5                                    # ~1-2 pages expected
```

## 16. Industry Usage
- **PostgreSQL**: heap file for rows, index entries → RID; `CLUSTER` as the one-time sorted-file emulation.
- **MySQL/InnoDB**: clustered by primary key (rows physically PK-ordered); secondary indexes store PK values → exactly the "sorted-file" idea managed by a tree.
- **Oracle/SQL Server**: heap or clustered (IOT in Oracle) choice per table — DBAs pick by workload, the way this chapter teaches.
- **Analytics (Redshift, ClickHouse, Snowflake)**: sort keys / ORDER BY per column — the sorted-file concept at columnar scale, driving compression + range pruning.
- **Key-value stores** (Redis, DynamoDB partitions): hashed placement for O(1) exact access — hashed-file thinking in production.

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 16 (disk storage), Ch. 17 (file organizations).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 13.1–13.3.
- Garcia-Molina, Ullman & Widom, *Database Systems: The Complete Book*, 2nd ed., Ch. 13.1–13.3.
- PostgreSQL docs: CLUSTER; CREATE TABLE ... PARTITION BY HASH.
- MySQL InnoDB docs: Clustered and Secondary Indexes.

## 18. Cheat Sheet
- Heap: append rows; O(1) insert; O(N) point search; great scans.
- Sorted: order by key; O(log N) search/range; O(N) insert.
- Hashed: bucket by h(key); O(1) point; no ranges; rehash on overflow.
- RID = (page, slot); indexes store RIDs/PKs.
- Real engines: Postgres heap + RID indexes; InnoDB clustered by PK.
- Hash file ≠ hash index; sorted file ≈ static clustered idea.
- Choose by dominant workload: writes→heap, ranges→sorted, exact→hash.

## 19. Quiz
1. Point lookup cost on a heap file: a) O(1) b) O(log N) c) O(N) d) O(N²) → **c**
2. Best organization for range queries: a) heap b) sorted c) hash d) none → **b**
3. Best for exact-key lookups: a) heap b) sorted c) hashed d) random → **c**
4. Insert cost into a sorted file (worst): a) O(1) b) O(log N) c) O(N) d) O(1) amortized → **c**
5. A RID is: a) a hash b) (page, slot) c) a key d) a bitmap → **b**
6. PostgreSQL default row layout: a) clustered b) heap c) hash d) sorted → **b**
7. InnoDB organizes rows by: a) heap b) primary key (clustered) c) hash d) creation order → **b**
8. Hashed files fail at: a) exact lookups b) range queries c) inserts d) all → **b**
9. Extendible hashing splits: a) whole file b) one bucket at a time c) nothing d) all pages → **b**
10. IO cost is measured in: a) bytes b) pages c) records d) buckets → **b**

## 20. Flashcards
- **Q: Three file organizations?** → **A:** Heap, sorted, hashed.
- **Q: Heap point lookup?** → **A:** O(N) scan; insert O(1).
- **Q: Sorted point lookup?** → **A:** O(log N); insert O(N) worst.
- **Q: Hashed point lookup?** → **A:** O(1) expected; no ranges.
- **Q: What is a RID?** → **A:** (page, slot) — where a record lives.
- **Q: Postgres layout?** → **A:** Heap + indexes→RID.
- **Q: InnoDB layout?** → **A:** Clustered by primary key.
- **Q: Choose organization by?** → **A:** Dominant workload (writes/ranges/exact).

## 21. Revision
Three raw file organizations, three cost profiles: **heap** = append (O(1) insert, O(N) point search, great sequential scan), **sorted** = ordered by key (O(log N) point/range, O(N) insert), **hashed** = bucket by `h(key)` (O(1) point, no ranges, rehash on overflow). The **RID** (page, slot) is how records are addressed, and indexes store RIDs (or PKs). No single layout wins — that's why **PostgreSQL** uses a heap with indexes→RID while **InnoDB** clusters rows by primary key, and analytics engines keep columns sorted by a sort key. Interview script: name the three; give the cost table (point/range/insert); map them to workloads (writes→heap, ranges→sorted, exact→hash); and state the modern reality (heap/cluster + indexes). This is the baseline — Chapter 02's indexes are built on top of it.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Three file organizations / costs" | 2 / 13 Q1–Q4 |
| "Which for my workload?" | 13 Q5–Q6, Q12 |
| "What is a RID?" | 13 Q7 |
| "Postgres vs InnoDB layout?" | 13 Q18 |
| "Extendible / linear hashing?" | 13 Q10–Q11 |
| "Heap + index vs sorted?" | 13 Q15 / 14 Q2 |
| "Why pages not records?" | 13 Q13 |
| "Clustered vs clustered index?" | 13 Q9 |
