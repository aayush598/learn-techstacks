# Bitmap and Other Index Types

> **TL;DR**: Beyond B+ and hash, databases offer specialized indexes: **bitmap** indexes (bit per row per distinct value) for low-cardinality AND/OR filters in warehouses; **GIN** (inverted lists) for arrays, JSONB, and full text; **GiST** (generalized search trees) for geometry and ranges; **BRIN** (block ranges) for huge naturally-ordered tables; and **full-text** indexes for language-aware search. Each trades generality for a specific access pattern.

## 1. Why Does This Exist?
B+ trees and hash indexes cover equality and range on scalar keys — but real data has patterns they handle badly. A column like `gender` or `status` has a few distinct values (low cardinality): a B+ index on it returns 50% of rows (useless — scan is cheaper), yet warehouses *combine* many such filters (`WHERE region='NA' AND gender='F' AND status='active'`). **Bitmap indexes** turn each value into a bit array and answer such predicates by cheap bitwise AND/OR — built for that. Other types answer *non-scalar* questions: **GIN** finds "which rows contain this array element / JSON key / word"; **GiST** finds "which rows overlap this range/geometry"; **BRIN** exploits physical order to skip whole page ranges; **full-text** indexes handle word variants and ranking. These specialized structures exist because "generic sorted tree" isn't optimal for every access pattern — each type is the right tool for a specific job.

## 2. How Does It Work?
- **Bitmap index**: for each distinct value v, a bit vector with bit i = 1 iff row i has v (compressed run-length). `WHERE c=v` → fetch the vector; `AND`/`OR` → bitwise ops; results → RIDs. Row updates rewrite bits (costly → read-mostly warehouses).
- **GIN (Generalized Inverted Index)**: inverted list — each key (array element, JSONB key/entry, token) maps to the list of rows containing it. Postgres GIN for `@>`, `?`, `?|`, `?&` on arrays/JSONB, and `tsvector` full text.
- **GiST (Generalized Search Tree)**: balanced search tree generalizing the B-tree to arbitrary data types via user-defined keys/penalties — ranges (`int4range`, `tsrange`), geometry (`&&`, `<@`), exclusion constraints, and nearest-neighbor (`<->`).
- **BRIN (Block Range Index)**: stores per-page-range min/max summaries; for a naturally-ordered table, a predicate skips entire ranges whose min/max exclude it. Tiny, fits in cache.
- **Full-text**: tokens → posting lists with positions; supports stemming, ranking (ts_rank), phrase search; GIN/`tsvector` behind the scenes in Postgres.

## 3. When Is It Used?
- **Bitmap**: data warehouses, low-cardinality columns combined with AND/OR (Oracle, PostgreSQL `Bitmap Heap Scan` + `Bitmap Index Scan` combine B+ bitmaps; true bitmap *indexes* are Oracle/PG-extension territory).
- **GIN**: JSONB/array containment (`@>`, `?`), full-text search, trigram `ILIKE` (`pg_trgm`).
- **GiST**: geometry overlaps, range types (concurrency/overlap checks), exclusion constraints, KNN (`ORDER BY ... <->`).
- **BRIN**: huge append-only tables ordered by a column (log/event tables by timestamp) where a full index is too big.
- **Full-text**: search over documents/descriptions with ranking (Postgres `to_tsvector`/`@@`, MySQL FULLTEXT).

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: B+ tree on low-cardinality columns.** Returns most rows → optimizer ignores it (scan cheaper); combining multiple such predicates still needs per-row checks. Bitmap's bitwise AND/OR collapses the cost — the whole point.
- **Alternative: B+ tree for array/JSON containment.** A B+ index can only look up a whole value; "contains this element" needs an *inverted* structure mapping element → rows — that's GIN.
- **Alternative: B+ tree for geometry/ranges.** B+ ordering assumes a total order; overlap/intersection needs a spatial structure — GiST generalizes the tree with domain-specific keys.
- **Alternative: a full B+ index on a huge ordered table.** Space and maintenance cost scale with N; BRIN trades exact entries for block-range summaries, staying tiny while enabling page-range pruning.
- **Why not one universal index?** Because "what the query needs" varies (bit tests, containment, overlap, word match); each specialized index optimizes its pattern and is the default-free structure for it.

## 5. Intuition
- **Bitmap** = a **light-up seating chart** per attribute value: "show rows where status='active'" lights up a subset of seats; "AND gender='F'" = keep only seats lit by *both* charts. Comparing two charts (bitwise) is instant; comparing a list of row numbers is not.
- **GIN** = a **book's back-of-book index** for words: "find every page mentioning 'hashing'" → the index (inverted list) lists the pages; you never scan the book. GIN is that — but for array elements and JSON keys.
- **GiST** = a **map with grid references**: "show parks overlapping this area" → the tree narrows to the relevant grid cells, no need to check every park against the rectangle.
- **BRIN** = **shelf labels**: a warehouse shelves goods in date order and labels each aisle "March 1–7"; a request for "March 3" skips all other aisles without opening a single box.

## 6. Real-World Analogy
A **department store's floor-plan app**. The **bitmap** approach: every product has a tag per attribute (color=red, size=M) and each tag lights up a subset of shelves on the map; shoppers filter by combining tags — the app compares lit-shelf lists by AND/OR, near-instantly (bitmap). The **GIN** approach: "find all stores carrying the 'Nike' brand" uses a catalog that lists each brand with all its stores (inverted list) — no walking every aisle. **GiST**: "find a pharmacy within 2 km" uses a city grid map — only the nearby grid cells are checked. **BRIN**: "find receipts from July" uses the shelving order and aisle labels — the July aisle only. Each specialty answers its own question type the way the general B+ tree (an alphabetized list of *everything*) can't do efficiently.

## 7. Formal Definition
(Oracle & PostgreSQL docs; Elmasri & Navathe Ch. 18.8; Silberschatz Ch. 14.8.)
- **Bitmap index**: for each distinct key value v, a compressed bit vector B_v with B_v[i]=1 iff tuple i has v. Supports efficient AND/OR/NOT and aggregation (COUNT).
- **GIN**: inverted index mapping each indexed key (element/token/JSON entry) to a posting list of TIDs; supports containment, existence, and full-text operators.
- **GiST**: balanced tree with generalized keys (predicate operators user-supplied); supports range overlap, geometry, and KNN ordering.
- **BRIN**: stores per-block-range (e.g., 128 pages) min/max summaries; planner prunes ranges outside the query's bounds.
- **Full-text index**: token→posting lists with positions/language-specific stemming; supports ranked and phrase queries.

## 8. Example
Rows 1–8, column `status ∈ {open, closed}`:
```
open:   1 1 0 1 0 0 1 0
closed: 0 0 1 0 1 1 0 1
```
- `WHERE status='open'` → fetch the `open` bitmap (8 bits) → rows {1,2,4,7}.
- `WHERE status='open' AND region='NA'` → AND the two bitmaps → instant.
- `COUNT(*) WHERE status='open'` → popcount — no row scan.
- **GIN example**: JSONB `tags @> '["red"]'` → GIN maps token 'red' → posting list → rows.
- **GiST**: `tsrange && '[2024-01-01, 2024-02-01)'` on a reservations table → tree prunes non-overlapping ranges.
- **BRIN**: table ordered by `created_at`; BRIN stores min/max per 128-page block; a July query skips all non-July blocks.

| Index | Best for | Cost | Used by |
|---|---|---|---|
| B+ tree | scalar eq/range | O(log N) | default everywhere |
| Hash | exact eq | O(1) | PG/MySQL MEMORY |
| Bitmap | low-card AND/OR | bitwise ops | Oracle, PG (bitmap heap scans) |
| GIN | containment/full-text | inverted lists | Postgres arrays/JSONB/fts |
| GiST | geometry/ranges | tree w/ ops | Postgres geo/range |
| BRIN | huge ordered tables | block min/max | Postgres append-only |

## 9. Internal Working
1. **Bitmap**: build one bit vector per distinct value (run-length/word-aligned compression); queries bitwise-AND/OR/NOT vectors; convert result bits → RIDs (row order by bitmap order); updates rewrite affected bits (write-heavy tables suffer — warehouses only).
2. **GIN**: tokenize keys (arrays → elements; JSONB → key/entry pairs; text → tsvector lexemes); maintain posting lists per token; on query, union/intersect postings; can be *lossy* (fast path) with recheck.
3. **GiST**: each node holds a key that summarizes its subtree (e.g., bounding box); query descends only subtrees whose key *can* satisfy the operator; supports KNN by ordering subtrees by distance.
4. **BRIN**: compute per-range min/max (and optionally nulls); planner uses the summaries to skip ranges; `CREATE INDEX ... USING brin (...) WITH (pages_per_range = n)`.
5. **Full-text**: `to_tsvector` parses/lexes with a dictionary (english etc.); GIN/`@@` query; `ts_rank`/`ts_headline` for ranking; combined with `pg_trgm` for ILIKE/substring search.

## 10. Time Complexity
- **Bitmap AND/OR of two vectors**: O(#pages) bitwise — near-constant per vector; **COUNT**: O(popcount) ≈ O(N/word).
- **GIN lookup**: O(log + posting list length) — proportional to matches, not table size.
- **GiST**: O(log N) descents to matching subtrees (worst O(N) pathological overlap).
- **BRIN scan**: O(#block_ranges) to filter + O(scanned pages) for matching ranges.
- **Full-text**: O(log + hits) for term queries; ranking O(hits).
- **B+ baseline**: O(log N) per point; O(N) for low-selectivity predicates (why bitmap wins there).

## 11. Advantages
- **Bitmap**: sub-linear multi-predicate AND/OR; fast COUNT; tiny per-value storage (compressed); ideal for warehouse analytics.
- **GIN**: answers "contains" questions a B+ tree can't; efficient for arrays/JSONB/full text; scalable posting lists.
- **GiST**: one structure for many datatypes (geo, ranges, exclusion); supports KNN; user-extensible operators.
- **BRIN**: tiny index on enormous tables; fits in cache; near-zero maintenance for append-only data.
- **Full-text**: language-aware search + ranking the B+ tree can't provide.

## 12. Disadvantages
- **Bitmap**: update/insert cost (bit rewriting) → read-mostly only; row counts shift invalidate vectors (bitmap indexes are append-immutable-friendly).
- **GIN**: build/maintenance cost; lossy entry with recheck; memory use on updates.
- **GiST**: complexity; operator-dependent performance; can degenerate on overlapping data.
- **BRIN**: useless unless data is physically ordered by the indexed column; coarse (block-range) selectivity.
- **Full-text**: language/dictionary tuning; not a substitute for a real search engine at huge scale.

## 13. Interview Questions
1. **Q: What is a bitmap index?** A: One bit vector per distinct value (bit i = row i has the value); predicates answered with bitwise AND/OR/NOT; best for low-cardinality columns in read-mostly warehouses.
2. **Q: Why not a B+ tree for low-cardinality columns?** A: A B+ index on 'gender' returns ~50% of rows (scan is cheaper) and can't cheaply combine several such predicates — bitmap's bitwise ops collapse the cost.
3. **Q (tricky): when do you NOT use a bitmap index?** A: High-cardinality columns (vector per value ≈ table size) and write-heavy OLTP (every update rewrites bits); bitmaps belong in append-heavy warehouses.
4. **Q: What is GIN?** A: Generalized Inverted Index — maps each indexed key (array element, JSONB key/entry, text token) to a posting list of rows; used for containment and full-text.
5. **Q: JSONB containment query without GIN?** A: `tags @> '["red"]'` scans every row; a GIN index on `tags` maps 'red' → rows → instant. That's the classic JSONB-index story.
6. **Q: What is GiST?** A: Generalized Search Tree — a balanced tree with user-defined keys; serves range overlap (`&&`), geometry (`<@`), exclusion constraints, and KNN (`<->`).
7. **Q: What is BRIN and when does it shine?** A: Block-Range Index — stores per-page-range min/max; shines on huge append-only tables ordered by the indexed column (e.g., logs by timestamp) where a full B+ index is too big.
8. **Q (scenario): events table, 500 GB, queried by created_at range.** A: BRIN on created_at (naturally ordered, append-only) — tiny index, prunes blocks; a full B+ index would be huge and slow to maintain.
9. **Q: Postgres full-text search mechanics?** A: `to_tsvector` tokenizes with a dictionary; GIN on the tsvector; `@@` for matching; `ts_rank` for ranking; `pg_trgm` for ILIKE/substring.
10. **Q: Bitmap Heap Scan vs bitmap index?** A: Postgres builds per-index *bitmaps* during planning and combines them (Bitmap Index Scan → Bitmap Heap Scan) even with B+ indexes — a query-level bitmap; true persistent bitmap *indexes* are Oracle's.
11. **Q (hard): how does a bitmap COUNT avoid a scan?** A: popcount over the value's bit vector counts matches directly — O(N/word) without touching rows.
12. **Q: What is an exclusion constraint and GiST?** A: A constraint like "no overlapping booking ranges" enforced via GiST (`EXCLUDE USING gist (range WITH &&)`) — uniqueness generalized to "no overlaps."
13. **Q (tricky): GIN lossy index?** A: GIN can store a *fastpath* (partial) entry pointing to a page; the query then rechecks rows in that page — trading precision for speed; `gin_fuzzy_search_limit` guards worst cases.
14. **Q: When would you use GIN vs GiST for ranges?** A: GIN for *set containment* (arrays/JSONB/full text); GiST for *overlap/order* (geometric/range types). Different operator families, different structures.
15. **Q (production): arrays column `tags`, query `WHERE 'x' = ANY(tags)`?** A: Create a GIN index on tags; the `= ANY` becomes a GIN lookup — without it, a full scan per row.
16. **Q: What is pg_trgm?** A: A GIN/GiST trigram index for fuzzy/substring matching (`ILIKE '%pattern%'`, similarity) that a plain B+ tree can't support.
17. **Q (hard): why is a bitmap index bad for a column with 1M distinct values?** A: One vector per value → 1M vectors, nearly every bit set for large tables — storage and AND/OR blow up; high cardinality wants B+/hash.
18. **Q: What does "low cardinality" mean for index choice?** A: Few distinct values (gender, status, month) — few bitmaps, each dense → bitmap wins; high-cardinality (id, email) → B+/hash.
19. **Q (scenario): search "documents containing both words" with full-text.** A: `tsvector` GIN index; query `@@ to_tsquery('foo & bar')` intersects posting lists; ranking via ts_rank — a mini search engine inside Postgres.
20. **Q: How do you decide between BRIN and B+ for a big table?** A: If data is physically sorted on the query column and queries are ranges → BRIN (tiny, fast, skip-heavy); if point lookups or arbitrary order → B+.

## 14. Follow-Up Questions
1. **Q: Can bitmap indexes be combined with join operations?** A: Bitmaps produce RID sets that feed nested-loop or bitmap-join plans; warehouses use them as the filter stage before joins.
2. **Q: What's the build cost of a GIN index on a huge table?** A: O(N × avg tokens) tokenization + posting build; `maintenance_work_mem`-tuned; can be significant — build off-peak.
3. **Q: How does BRIN interact with partitioning?** A: Partitioning by time + BRIN per partition gives doubly-prunable scans — the standard event-table architecture.
4. **Q: GIN vs a separate full-text engine (Elasticsearch)?** A: Postgres full-text scales to ~millions of docs fine; Elasticsearch wins at huge scale/distributed ranking — know the threshold (size, query load, ranking sophistication).
5. **Q: Does Oracle use bitmap indexes in production?** A: Yes — Oracle bitmap indexes on low-cardinality dimension columns in star schemas are a textbook warehouse pattern; PostgreSQL's bitmaps are primarily plan-level.

## 15. Coding Example
```sql
-- GIN: JSONB containment
CREATE TABLE docs (id BIGINT, tags JSONB);
CREATE INDEX idx_docs_tags ON docs USING gin (tags);
SELECT * FROM docs WHERE tags @> '["red", "urgent"]';   -- GIN lookup

-- GIN: arrays
CREATE INDEX idx_orders_skus ON orders USING gin (skus);
SELECT * FROM orders WHERE skus @> ARRAY['A-100'];

-- GIN: full-text (tsvector)
CREATE INDEX idx_docs_fts ON docs USING gin (to_tsvector('english', body));
SELECT id, ts_rank(to_tsvector('english', body), query) AS rank
FROM docs, to_tsquery('english', 'hashing & index') query
WHERE to_tsvector('english', body) @@ query ORDER BY rank DESC;

-- GiST: range overlap
CREATE TABLE reservations (id INT, during tsrange);
CREATE INDEX idx_res_during ON reservations USING gist (during);
SELECT * FROM reservations WHERE during && '[2024-06-01, 2024-07-01)';

-- BRIN: huge ordered log table
CREATE INDEX idx_logs_ts ON logs USING brin (created_at) WITH (pages_per_range = 64);
SELECT * FROM logs WHERE created_at BETWEEN '2024-06-01' AND '2024-06-02';
-- planner skips non-June block ranges

-- Verify chosen plans
EXPLAIN (ANALYZE) SELECT * FROM docs WHERE tags @> '["red"]';
--   -> Bitmap Index Scan on idx_docs_tags  /  Bitmap Heap Scan
```

## 16. Industry Usage
- **PostgreSQL**: GIN/GiST/BRIN are first-class access methods — JSONB `@>`, arrays, full text (`to_tsvector`), ranges, geometry (PostGIS uses GiST), and massive append-only tables (BRIN) are all production patterns.
- **Oracle**: bitmap indexes on low-cardinality warehouse dimension columns (star schema filters); optimizer combines them for multi-predicate analytics.
- **MySQL**: FULLTEXT indexes for language search; no GIN/GiST/BRIN equivalents (different design) — but generated columns + JSON in MySQL 8 cover some cases.
- **PostGIS**: GiST spatial indexes power geospatial querying at scale — the canonical GiST deployment.
- **Log/event pipelines**: BRIN + time partitioning is the standard cheap-index recipe for click-stream and audit tables.

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 18.8 (other indexes).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 14.8.
- O'Neil & Quass, "Improved Query Performance with Variant Indexes" (bitmap), SIGMOD 1997.
- PostgreSQL docs: Index Types (GIN, GiST, BRIN), Full Text Search, pg_trgm.
- Oracle Database Concepts: Bitmap Indexes.

## 18. Cheat Sheet
- Bitmap: bit per value; AND/OR/COUNT via bitwise; low-cardinality, read-only.
- GIN: inverted lists; arrays/JSONB `@>`; full text tsvector.
- GiST: generalized tree; geometry/range overlap; exclusion; KNN.
- BRIN: block min/max; huge append-only ordered tables; tiny.
- Full-text: tsvector + GIN + ts_rank; pg_trgm for ILIKE.
- High cardinality → B+/hash; low → bitmap; containment → GIN; geo/range → GiST; huge ordered → BRIN.
- Postgres plans: Bitmap Index Scan + Bitmap Heap Scan combine B+ indexes.

## 19. Quiz
1. Bitmap index best for: a) high cardinality b) low cardinality c) write-heavy d) ranges → **b**
2. Bitmap AND of two predicates: a) sort b) bitwise AND c) scan d) hash → **b**
3. GIN stands for: a) General Index b) Generalized Inverted Index c) Global Index d) Gist → **b**
4. JSONB `tags @> '["red"]'` best served by: a) B+ b) GIN c) BRIN d) bitmap → **b**
5. GiST is for: a) scalars b) geometry/ranges c) text d) bitmaps → **b**
6. BRIN stores: a) per-row keys b) block-range min/max c) hashes d) postings → **b**
7. BRIN requires data: a) hashed b) physically ordered on the column c) unique d) small → **b**
8. COUNT via bitmap uses: a) scan b) popcount c) index dive d) hash → **b**
9. Full-text ranking in Postgres: a) ts_rank b) ts_pop c) rank_n d) score() → **a**
10. Bitmap indexes are unsuitable for: a) warehouses b) OLTP writes c) low-card d) analytics → **b**

## 20. Flashcards
- **Q: Bitmap index?** → **A:** Bit per value per row; AND/OR/COUNT bitwise; low-cardinality warehouses.
- **Q: GIN?** → **A:** Inverted lists; arrays/JSONB containment; full text.
- **Q: GiST?** → **A:** Generalized tree; geometry/range overlap; KNN.
- **Q: BRIN?** → **A:** Block-range min/max; huge append-only ordered tables.
- **Q: When bitmap fails?** → **A:** High cardinality or write-heavy OLTP.
- **Q: JSONB containment without GIN?** → **A:** Full table scan per row.
- **Q: pg_trgm?** → **A:** Trigram GIN/GiST for ILIKE/fuzzy search.
- **Q: Exclusion constraint?** → **A:** GiST "no overlaps" (e.g., bookings ranges).

## 21. Revision
Four specialized index families beyond B+/hash. **Bitmap**: one bit vector per distinct value; predicates become bitwise AND/OR, COUNT becomes popcount — for **low-cardinality, read-mostly** warehouse columns; deadly on write-heavy/high-cardinality. **GIN**: inverted lists (element/token → posting list) powering arrays and JSONB `@>` and full text. **GiST**: a generalized balanced tree for **overlap** questions — geometry (`<@`), range types (`&&`), exclusion constraints, KNN. **BRIN**: block-range min/max summaries that let planners skip ranges — ideal for **huge, physically-ordered, append-only** tables (logs by timestamp). Full-text adds stemming + ranking (`ts_rank`); `pg_trgm` handles ILIKE. Choosing: low-card → bitmap; containment → GIN; geo/range → GiST; huge ordered → BRIN; scalar eq/range → B+/hash. Mention Postgres's plan-level bitmaps (Bitmap Index Scan + Bitmap Heap Scan) as the query-level cousin.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a bitmap index / when to use?" | 2 / 13 Q1–Q3 |
| "Why not B+ for low cardinality?" | 13 Q2 |
| "What is GIN / JSONB containment?" | 13 Q4–Q5 |
| "What is GiST / exclusion?" | 13 Q6, Q12 |
| "What is BRIN / when does it shine?" | 13 Q7–Q8 |
| "Postgres full-text mechanics?" | 13 Q9, Q19 |
| "GIN vs GiST?" | 13 Q14 |
| "Choosing between index types?" | 13 Q17, Q20 |
