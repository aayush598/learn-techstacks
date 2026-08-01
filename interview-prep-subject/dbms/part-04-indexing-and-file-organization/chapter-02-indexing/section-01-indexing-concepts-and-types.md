# Indexing Concepts and Types

> **TL;DR**: An index is a redundant data structure that accelerates reads by trading space and write cost. The core vocabulary: **clustered** (data ordered by the key, at most one) vs **secondary**; **dense** (entry per record) vs **sparse** (entry per page); **single-column** vs **composite**; **unique** vs **non-unique**. Every index decision is the same trade: faster lookups/range scans in exchange for slower writes and more disk.

## 1. Why Does This Exist?
Without indexes, every equality query is a full scan (O(N) pages) — unacceptable at table sizes of millions to billions. An index is a *side structure* mapping search keys to row locations (or PKs), so a lookup becomes "descend a tree / probe a hash → fetch one page" instead of scanning everything. It is **redundant by design**: the data already exists in the table; the index duplicates keys to make them searchable fast. Because it duplicates, it costs disk and slows every write (each insert/update/delete must maintain the index). Indexing exists to make the *read workload* fast while paying a *write/space* price — and choosing *which* keys to index, and *how* (which structure, which type), is the craft. It's the single highest-leverage physical-design decision in databases.

## 2. How Does It Work?
- **Index entry** = (search key, locator). Locator: **RID** (Postgres heap) or **primary key** (InnoDB secondary).
- **Clustered vs secondary**: clustered index = data physically ordered by key (one per table); secondary indexes are separate structures referencing the clustered/heap.
- **Dense vs sparse**: dense = one entry per *record*; sparse = one entry per *page* (points to the page, records searched within). Sparse saves space but needs ordered data; dense is general.
- **Primary vs secondary index**: primary index = on the sorted/ordering key (unique, typically dense); secondary = any other key, allows duplicates.
- **Composite**: index on multiple columns; only *leftmost prefixes* of the column list are usable.
- **Unique**: enforces uniqueness and lets the optimizer know at most one row matches.
- **Structures**: B+ tree (default, ordered), hash (exact match), bitmap, GIN/GiST/BRIN (specialized). Chosen by access pattern.

## 3. When Is It Used?
- **Point lookups** (`WHERE id = 5`): unique index on the key.
- **Range/order** (`BETWEEN`, `ORDER BY`, `GROUP BY`): B+ tree (ordered).
- **Equality on a foreign key** (join columns): secondary index on the FK.
- **Composite filters** (`WHERE a = 1 AND b = 2`): composite index on (a, b) with the right column order.
- **Covering** (all needed columns): covering index → no table fetch.
- **NOT for**: low-selectivity columns (WHERE status='active' with 90% match — scan is cheaper), columns written constantly with no read benefit, or tiny tables.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: sort the data and do binary search.** Works for one key, but a table has many query keys and writes shift rows; indexes give *many* orderings without moving data, maintained incrementally.
- **Alternative: no index (always scan).** Correct but O(N) — the baseline; indexes exist because scans don't scale.
- **Alternative: one universal index.** Impossible — different queries need different keys; and each index adds write cost, so the answer is *few, targeted* indexes.
- **Why B+ tree over hash as default?** Because most DB queries need *ordering* (ranges, ORDER BY, group-by adjacency); B+ trees support both point and range, so they're the general default; hash is the specialized exact-match optimizer. (Details in Sections 02–03.)
- **Why dense over sparse generally?** Sparse requires the data to be ordered on the index key (only the clustered case); dense works on any heap and still gives O(log N) — generality wins.

## 5. Intuition
An index is **the index of a textbook**: the pages (records) are in some physical order, and the index at the back maps every key (or topic) to page numbers. You never scan the whole book to find "Huffman coding" — you flip to the index, find the page, jump there. The textbook index is *redundant* (the topics are already in the text), it *costs pages* (space), and adding a page to the book means updating the index (write cost) — but searching becomes near-instant. A **composite index** is a combined index like "Author → Page" — it only helps if you search by author first (leftmost prefix). And a **covering index** is a mini-encyclopedia entry that contains the answer itself, so you don't even flip to the page.

## 6. Real-World Analogy
A **phone directory's back-of-book quick reference**. The full book is sorted by name (the clustered order — one physical order). The quick reference is a *secondary* index: "plumbers → see category 37" — an extra lookup step. A **sparse** index = the tabs on the letter pages ("P starts here") — one pointer per letter/page, fast to the section, then scan within. A **dense** index = every single name listed with its page — instant to the exact row, but a thick section (space). A **composite** index = "Name → Address → Phone" sorted by name first; looking up by *phone* alone is useless (leftmost rule). Maintaining any of these when people change address costs effort — that's the write tax. The directory publisher picks which references to print based on how readers search: exactly how a DBA picks indexes.

## 7. Formal Definition
(Elmasri & Navathe Ch. 18; Silberschatz Ch. 14; PostgreSQL & MySQL index docs.)
- **Index**: a structure storing (search-key, locator) pairs that supports the find/range operations of the key faster than a scan.
- **Clustered index**: data file ordered by the index key; at most one.
- **Dense index**: one entry per record. **Sparse index**: one entry per page (requires data ordered by the key).
- **Primary index**: on the ordered key; typically unique and dense. **Secondary index**: on any other key; may be non-unique.
- **Composite (multi-column) index**: key = ordered tuple (a₁, a₂, …, aₙ); usable only for *leftmost prefixes* (a₁), (a₁,a₂), … .
- **Unique index**: enforces at most one row per key; optimizer uses it for cardinality estimates.
- **Covering index**: contains every column a query needs → no table access (index-only scan).

## 8. Example
Table `employees(id, dept, name, city)`, 1M rows, 100 rows/page.
- **No index**: `WHERE id = 900000` → full scan ≈ 10,000 page reads.
- **Clustered B+ on id** (InnoDB PK): descent, fan-out ~500, height ≈ log₅₀₀(1e4) ≈ 2 → **2–3 page reads** for the row.
- **Secondary on city**: `WHERE city='Pune'` → index descent (2) + RID/page fetch per match.
- **Composite on (dept, city)**: helps `WHERE dept='Eng' AND city='Pune'`, `WHERE dept='Eng'` — but NOT `WHERE city='Pune'` (leftmost prefix).
- **Covering index (dept, city)**: `SELECT dept, city WHERE city='Pune'`? No — city isn't leftmost. A covering index for `SELECT city, name WHERE city='Pune'` needs (city, name) so all columns come from the index.

| Index type | Locator | Read cost | Write cost | Notes |
|---|---|---|---|---|
| None | — | O(N) scan | O(1) | baseline |
| Dense B+ | RID/PK | O(log_f N) | O(log_f N) | general |
| Sparse | page | O(log N)+scan page | smaller | needs ordered data |
| Hash | bucket | O(1) exact | O(1) | no ranges |
| Bitmap | bit array | O(bits AND/OR) | O(update) | low cardinality |

## 9. Internal Working
1. **Choose the key(s)**: the columns in the WHERE/ORDER BY/GROUP BY of hot queries.
2. **Choose structure**: B+ tree if order/range matters; hash if exact-only; GIN/GiST/BRIN/bitmap for specialized types.
3. **Choose type**: clustered (only one) for the hottest ordering; secondary for others; unique if keys are unique; composite with careful column order; covering to add needed columns.
4. **Maintain**: each insert/update/delete updates every index (O(log N) per index); the optimizer reads index stats (cardinality, selectivity) to decide usage.
5. **Verify**: `EXPLAIN ANALYZE` — confirm the plan uses the index (Index Scan / Index Only Scan) and measure latency; drop unused indexes (monitor `pg_stat_user_indexes` / MySQL index usage stats).

## 10. Time Complexity
- **B+ lookup**: O(log_f N) where f = fan-out (hundreds) — for N = 1e9, height ≈ 4 → **4 page reads**.
- **Range**: O(log_f N + k) pages, k = result pages (leaf-linked).
- **Insert/delete**: O(log_f N) per index (tree maintenance).
- **Hash point**: O(1) expected; **hash range**: O(N) (not supported).
- **Full scan (no index)**: O(N) pages.
- **Covering index**: O(log_f N), zero table fetches.

## 11. Advantages
- **Massive read speedup**: point/range lookups drop from O(N) to O(log N) or O(1).
- **Multiple orderings**: secondary indexes provide many virtual orders without moving rows.
- **Constraint support**: unique/PK indexes enforce integrity and serve lookups simultaneously.
- **Covering/index-only scans**: some queries never touch the table.
- **Fine-grained control**: composite, partial, expression, and filtered indexes tune per-query performance.

## 12. Disadvantages
- **Write amplification**: every insert/update/delete maintains each index (O(log N) each).
- **Disk/space cost**: duplicate keys; huge indexes on wide/long columns.
- **Cache pressure**: more index pages compete for buffer pool memory.
- **Index-maintenance & stats**: need monitoring; stale stats mislead the optimizer.
- **Bad indexes hurt**: unused indexes slow writes and waste space; over-indexing is a classic production mistake.

## 13. Interview Questions
1. **Q: What is an index?** A: A redundant structure mapping search keys to row locations (or PKs) to speed reads, at the cost of space and write maintenance.
2. **Q: Dense vs sparse index?** A: Dense = one entry per record; sparse = one per page. Sparse is smaller but needs data ordered by the key; dense is general.
3. **Q: Clustered vs secondary?** A: Clustered = data physically ordered by the key (one per table); secondary = separate structure referencing rows (any number).
4. **Q: Primary vs secondary index?** A: Primary = on the ordering key, usually unique; secondary = any other key (may allow duplicates).
5. **Q: Why do writes get slower with indexes?** A: Each insert/update/delete must update every index structure (O(log N) per index) — write amplification.
6. **Q (tricky): index on (a, b) — does it help `WHERE b = 5`?** A: No — only leftmost prefixes (a) and (a, b) are usable; b alone can't be used (unless the DB can skip-scan, a partial exception).
7. **Q: What is a covering index?** A: An index containing all columns the query needs → index-only scan, no table fetch.
8. **Q (scenario): table with WHERE dept AND city; which composite order?** A: More selective first, or match the most-common query's equality filters; e.g., (dept, city) if dept filters more / (city, dept) otherwise — measure with EXPLAIN.
9. **Q: When does an index hurt more than help?** A: Low-selectivity columns (matches most rows → optimizer prefers scan), write-heavy tables with unused indexes, or tiny tables where scan is faster.
10. **Q: Unique vs non-unique index?** A: Unique enforces at-most-one and helps the optimizer (cardinality = 1 → stop-at-match); non-unique allows duplicates.
11. **Q (hard): sparse index on a heap?** A: Not possible in the classic sense — sparse requires records physically ordered by the key (clustered); heaps use dense indexes.
12. **Q: What does a B+ tree give that a hash doesn't?** A: Ordering — ranges, ORDER BY, GROUP BY adjacency, prefix scans. Hash gives O(1) exact only.
13. **Q: How does the optimizer decide to use an index?** A: Cost model: estimated selectivity (from stats/analyze), expected page reads vs full scan; low selectivity → index looks more expensive than scan.
14. **Q (production): you added an index but EXPLAIN ignores it.** A: Check: stats stale (ANALYZE), low selectivity, `%pattern%` LIKE, functions on the column (no expression index), or type coercion preventing index usage.
15. **Q: Composite index column order rule?** A: Equality columns first (exact filters), then the range/order column; the most selective first helps narrow fastest — but equality-vs-range trumps pure selectivity.
16. **Q: What is an index-only scan?** A: The index contains every needed column (covering), so the planner reads only index pages — no heap/clustered probe.
17. **Q (tricky): can a secondary index avoid the second probe?** A: Yes when covering (Postgres index-only scan; InnoDB: PK is always in the secondary index, so queries selecting PK+index columns avoid the clustered probe).
18. **Q: Partial/filtered index?** A: Index on a WHERE subset, e.g., `WHERE status='open'` — smaller, cheaper to maintain, targeted at the hot subset.
19. **Q: Expression/function index?** A: `CREATE INDEX ON t (lower(email))` — indexes the *expression*; required when queries use functions/coercions on columns.
20. **Q: How many indexes is too many?** A: When write amplification + maintenance cost exceeds read benefit — monitor usage (`pg_stat_user_indexes.idx_scan`); drop cold indexes. There's no fixed number; it's a measured trade.

## 14. Follow-Up Questions
1. **Q: How do NULLs index?** A: Postgres indexes NULLs (usable for IS NULL); InnoDB does not index NULL values by default (IS NULL can't use a non-covering index — a classic gotcha).
2. **Q: What is selectivity and why does it matter?** A: The fraction of rows a predicate matches; high selectivity (few rows) → index wins; low selectivity (many rows) → scan. Optimizers estimate it from histogram stats.
3. **Q: How do indexes interact with joins?** A: Indexed join keys enable nested-loop joins with an index probe per outer row (O(outer × log N)); without, the planner picks hash/merge joins instead.
4. **Q: What is the difference between an index and a constraint?** A: A unique/PK *constraint* is backed by an index but is semantically about integrity; an index alone is only a performance structure (no integrity guarantee).
5. **Q: How does MVCC interact with indexes?** A: Old row versions must remain reachable — Postgres updates index entries for changed keys, and HOT avoids re-indexing when only non-indexed columns change; bloat is a maintenance concern.

## 15. Coding Example
```sql
-- Basic index types (PostgreSQL syntax)
CREATE TABLE employees (id BIGINT, dept TEXT, city TEXT, name TEXT);

-- 1) unique index (also backs a UNIQUE constraint)
CREATE UNIQUE INDEX idx_emp_id ON employees(id);

-- 2) composite index: order matters (leftmost prefix)
CREATE INDEX idx_emp_dept_city ON employees(dept, city);
-- helps: WHERE dept='Eng' / WHERE dept='Eng' AND city='Pune'
-- NOT:  WHERE city='Pune'

-- 3) covering index -> index-only scan
CREATE INDEX idx_emp_city_name ON employees(city, name);
-- SELECT city, name WHERE city='Pune'  => index-only, no table fetch

-- 4) partial index (hot subset)
CREATE INDEX idx_emp_open ON employees(id) WHERE status = 'open';

-- 5) expression index
CREATE INDEX idx_emp_lower_email ON employees(lower(email));

-- Verify what the optimizer actually does
EXPLAIN ANALYZE SELECT id FROM employees WHERE city = 'Pune';
--   Index Only Scan using idx_emp_city_name  (if covering)
--   Seq Scan                                (if it ignores the index)
```
```python
# Selectivity & read-cost reasoning
def estimate_index_cost(selectivity, n_records, height=3):
    rows_matched = n_records * selectivity
    return height + rows_matched   # height reads + per-row fetches

def estimate_scan_cost(n_records):
    return n_records               # every page scanned
# Index wins when height + rows_matched < n_records, i.e., selectivity low enough.
```

## 16. Industry Usage
- **Every RDBMS**: B+ tree is the default; PK/unique constraints auto-create indexes.
- **Postgres**: rich index family — partial, expression, covering, GIN/GiST/BRIN; `pg_stat_user_indexes` for usage monitoring.
- **MySQL/InnoDB**: clustered PK; secondary indexes store PK; MEMORY engine uses hash indexes; `SHOW INDEX` + `EXPLAIN` for tuning.
- **OLTP schema design**: FK columns get indexes (join + cascade speed); hot query filters get composite indexes tuned with EXPLAIN.
- **Caches/key-value** (Redis, DynamoDB): hash/partition structures — the same trade at engine scale; over-indexing is a top operational anti-pattern everywhere.

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 18 (Indexing).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 14.
- Garcia-Molina, Ullman & Widom, *Database Systems: The Complete Book*, 2nd ed., Ch. 14.
- PostgreSQL docs: CREATE INDEX, Index-Only Scans, Partial Indexes.
- MySQL 8.0 docs: InnoDB Indexes, MEMORY Storage Engine.

## 18. Cheat Sheet
- Index = redundant (key → locator) structure: read speed for write+space.
- Clustered (1/table, data ordered) vs secondary (many, references).
- Dense (per record) vs sparse (per page, needs order).
- Composite: leftmost prefixes only.
- Unique ⇒ at-most-one + optimizer cardinality.
- Covering ⇒ index-only scan (no table fetch).
- B+ tree: point + range; hash: point only.
- Monitor: unused indexes slow writes — drop them.

## 19. Quiz
1. An index trades for: a) writes for reads b) reads for writes c) disk for cpu d) nothing → **a**
2. Sparse index needs: a) any data b) data ordered by key c) hashing d) covering → **b**
3. Max clustered indexes per table: a) 0 b) 1 c) 2 d) many → **b**
4. Index on (a,b) helps: a) b only b) a only & (a,b) c) nothing d) all → **b**
5. Covering index enables: a) seq scan b) index-only scan c) hash join d) full table → **b**
6. Unique index tells the optimizer: a) count b) cardinality 1 → stop c) nothing d) sorts → **b**
7. A query matching 95% of rows prefers: a) index b) seq scan c) hash d) bitmap → **b**
8. Which structure supports ranges? a) hash b) B+ tree c) both d) neither → **b**
9. Insert cost per index: a) O(1) b) O(log N) c) O(N) d) O(N²) → **b**
10. Over-indexing causes: a) faster reads b) write amplification c) less disk d) nothing → **b**

## 20. Flashcards
- **Q: What is an index?** → **A:** Redundant (key → locator) structure; read speed for write+space.
- **Q: Clustered vs secondary?** → **A:** Clustered orders data (1/table); secondary references rows.
- **Q: Dense vs sparse?** → **A:** Per-record vs per-page; sparse needs order.
- **Q: Composite leftmost rule?** → **A:** Only prefixes (a), (a,b) usable.
- **Q: Covering index?** → **A:** Contains all needed columns → index-only scan.
- **Q: When to NOT index?** → **A:** Low selectivity, tiny tables, unused indexes.
- **Q: Why do writes slow?** → **A:** Every index maintained per write (O(log N)).
- **Q: Default structure?** → **A:** B+ tree (point + range).

## 21. Revision
An index is **redundant (key → locator)**: it buys read speed at write + space cost. Master the type matrix: **clustered** (one per table, data ordered) vs **secondary** (any number, references); **dense** (per record) vs **sparse** (per page, needs ordering); **single vs composite** (only leftmost prefixes work); **unique** (at-most-one + optimizer boost); **covering** (index-only scan, no table fetch). The **B+ tree** is the default because it serves point + range (height ≈ log_f N ≈ 3–4 for 1e9 rows); **hash** is O(1) exact only. Decide by **selectivity**: high-selectivity predicates → index; low-selectivity/95%-match → scan. Watch write amplification and drop unused indexes (`pg_stat_user_indexes`). Interview script: define the trade, run the type matrix, apply the leftmost rule to a composite example, and state when an index is a bad idea.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is an index?" | 2 / 13 Q1 |
| "Dense vs sparse / clustered vs secondary?" | 13 Q2–Q4 |
| "Why slower writes?" | 13 Q5 |
| "Composite leftmost rule?" | 13 Q6 |
| "Covering index?" | 13 Q7, Q16 |
| "When does an index hurt?" | 13 Q9 |
| "Why does EXPLAIN ignore my index?" | 13 Q14 |
| "Index type / structure choice?" | 13 Q12, Q18–Q19 |
