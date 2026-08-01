# Clustered vs Non-clustered Organization

> **TL;DR**: A **clustered** organization keeps the table's data pages physically ordered by a key (at most **one** per table), making range scans and the PK lookup contiguous and fast. A **non-clustered** organization stores rows in a heap and references them from a separate index structure, so any key order is virtual. InnoDB clusters rows by the primary key; PostgreSQL keeps a heap and only re-orders with `CLUSTER`. The choice trades write cost and index duplication against read speed.

## 1. Why Does This Exist?
Sorted files proved that ordering rows by a key makes reads fast — but maintaining a strict sorted *file* is too expensive for OLTP (every insert shifts rows). The clustered-index idea is the compromise: keep the rows ordered by a **tree (B+ tree)** instead of a flat run, so inserts cause cheap page splits rather than massive shifts — and because the data pages themselves are ordered, the "index" and the "table" are the same structure. Since a set of pages can only be physically ordered one way, a table can have **at most one clustered index**; every other order must be a *secondary* index that references the rows. Non-clustered organization (heap + separate indexes) is the alternative: any number of "virtual orders" via indexes, none of them physical. Understanding the difference explains why PK lookups are fastest in InnoDB, why secondary-index lookups cost an extra hop, and why `CLUSTER` is a one-time maintenance op in PostgreSQL.

## 2. How Does It Work?
- **Clustered (InnoDB)**: the table *is* a B+ tree keyed on the primary key (the "clustered index"). Leaf pages hold whole rows, physically ordered by PK. A PK lookup = one B+ tree descent to the leaf = the row. Secondary indexes are separate B+ trees whose leaves store the PK value (not a RID) → a secondary lookup does *two* descents: the secondary tree, then the clustered tree (the "secondary lookup + PK probe").
- **Non-clustered / heap (PostgreSQL)**: the table is an unordered heap of pages. Every index (including one on the PK) is a separate structure whose leaves store **RIDs** (page, slot). A lookup = index descent → fetch page by RID (one random page read). No physical ordering; any number of indexes coexist.
- **Clustering (Postgres `CLUSTER`)**: a one-time physical rewrite of the heap into the order of an index; after that, inserts/updates break the order over time (heap behavior resumes), so you re-run `CLUSTER` or `VACUUM`-style maintenance to refresh locality.

## 3. When Is It Used?
- **Clustered**: when the *primary key* (or one hot range column) dominates reads — most OLTP. InnoDB uses it for everyone; Oracle/SQL Server let you choose the clustered key; choosing a non-PK clustering key (e.g., `user_id`) groups each user's rows together, speeding "all orders of a user."
- **Non-clustered/heap**: when inserts are the bottleneck, when you need many different orderings, when updates relocate rows (heap avoids row movement), and when full scans dominate.
- **`CLUSTER` (Postgres)**: periodic maintenance for range-heavy tables; re-running after writes restore locality.
- **Decision rule**: one order to rule them all? → clustered. Many orders / write-heavy? → heap + non-clustered indexes.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: sort the whole file and keep it sorted (flat sorted file).** Rejected for OLTP — every insert shifts rows O(N). The **B+ tree** absorbs inserts with page splits (O(log N)) and *is* the order: same benefit, manageable writes.
- **Alternative: cluster on more than one column set.** Physically impossible — one page order only; every other index must be non-clustered. The "at most one clustered index" rule is a physical law.
- **Alternative: non-clustered everywhere (heap).** Fast writes, any number of indexes — but each secondary lookup adds a random page fetch, and range scans on any key are not contiguous. Rejected where PK/range reads dominate.
- **Why InnoDB clusters on PK?** Because the vast majority of workloads read by PK; making the PK lookup a single-tree descent removes the extra hop and keeps the hottest reads contiguous. PostgreSQL chose heap for write/flexibility; the two engines are the two corners of the same trade.

## 5. Intuition
**Clustered = books on a shelf sorted by title.** Find "Moby Dick" → walk to the M section, pull the actual book — the shelf *is* the data, and "read all titles starting with M" is one contiguous shelf walk. Only one arrangement is possible (you can't sort by title *and* by author physically). **Non-clustered = a card catalog (index) + shelves in arbitrary order.** The catalog points you to shelf 14, slot 3; you then walk there and pull the book. You can have any number of catalogs (by title, by author, by year) — but every lookup is a catalog step *plus* a shelf step, and "all books by an author" means touching scattered shelves. The clustered shelf is fastest when you always read by the sorted order; the catalog wins when you need many orderings or frequent re-shelving.

## 6. Real-World Analogy
A **physical library** — books (rows), shelves (pages). **Clustered library**: shelves ordered by ISBN; finding ISBN 978-0-13 is a direct walk to the section, and "ISBNs 978-0-13-4…" is a contiguous shelf scan. Adding a book means sliding neighbors (page split). A second order (by author) exists only as a *card catalog* listing shelf positions — reading all of Tolstoy still means hopping between shelves. **Non-clustered library**: books shelved by arrival order (heap); a stack of card catalogs (title, author, subject) points to shelf+slot; any ordering is possible, every find requires the catalog step plus a shelf walk, and "shelving in order" never happens. Libraries pick one approach; databases pick the same way.

## 7. Formal Definition
(MySQL InnoDB docs; Elmasri & Navathe Ch. 17.2; Silberschatz Ch. 14.3; Oracle/SQL Server clustered index docs.)
- **Clustered index**: an index whose leaf level *contains the table's data rows*, ordered by the index key. A table can have at most one clustered index. Access to a row = descent to the leaf.
- **Non-clustered index**: a separate B+ tree whose leaf entries are (search-key, row locator). In a heap the locator is a **RID**; in InnoDB the locator is the **primary key value** (a secondary lookup therefore requires a second probe into the clustered tree).
- **Heap file**: an unordered collection of records; non-clustered indexes reference records by RID.
- **Clustering (as an operation)**: physically reordering a heap's records into an index key order (PostgreSQL `CLUSTER`); a *temporary* property that degrades as writes occur.

## 8. Example
Table `orders(order_id PK, user_id, amount)`; 1M rows; pages of 100 rows.
- **InnoDB (clustered on PK)**: PK lookup = descent ≈ log₂(1e4) ≈ 14 pages → 14 reads to the leaf, row in hand. Secondary index on user_id: leaf stores PK → descent (14) + PK descent (14) ≈ 28 reads per row. Range `order_id BETWEEN k AND k+500` = contiguous ~5 leaf pages.
- **PostgreSQL (heap + non-clustered)**: PK index leaves store RIDs. PK lookup ≈ 14 (index) + 1 (row page). Secondary lookup on user_id: 14 + 1. Range on order_id: index gives RIDs, but rows may be scattered → up to `result count` random page reads.
- **Clustered on user_id instead** (InnoDB, PK becomes a unique non-clustered index): "all orders of user U" = one contiguous run of data pages → single descent + sequential read; the "many rows of one user" pattern becomes cheap — the classic reason to choose a non-PK clustering key for user-centric schemas.

## 9. Internal Working
1. **InnoDB clustered table**: B+ tree over PK; data rows in leaves; inserts split leaves (O(log N)); secondary index entries = (secondary-key, PK). Unique secondary indexes add checks; updating PK relocates the row (row movement).
2. **Postgres heap**: rows appended/updated in place (updated rows are new versions via MVCC); every index is a separate B+ tree with (key → RID); a HOT (heap-only tuple) optimization avoids re-indexing when only non-indexed columns change.
3. **`CLUSTER`/`ALTER TABLE ... CLUSTER ON`**: physically sorts the table by the index key; locks the table; rewrites; provides locality until writes scatter it again (Postgres tracks clustering state in `pg_class.relclustered`).
4. **Choosing a clustering key**: the column with the most read amplification win — user-centric clustering groups child rows; time clustering groups recent rows for append-heavy analytics.

## 10. Time Complexity
- **Clustered PK lookup**: O(log N) to the leaf (row found) — no extra hop.
- **Clustered range on key**: O(log N + result pages), contiguous IO.
- **Non-clustered lookup (heap)**: O(log N) index descent + O(1) RID page fetch (random IO).
- **InnoDB secondary lookup**: O(log N) secondary + O(log N) clustered (≈ 2× PK lookup).
- **Insert (clustered)**: O(log N) page split amortized; may need reorganization.
- **Insert (heap)**: O(1) append + O(log N) index maintenance per index.
- **Clustering operation**: O(N) rewrite; only occasional.

## 11. Advantages
- **Clustered**: fastest PK/range reads (one descent, contiguous leaf runs); no double hop for the key reads; physical ordering matches hot access → great sequential IO.
- **Non-clustered/heap**: any number of orderings; cheap inserts (no row movement); updates that don't touch indexed columns are cheaper (Postgres HOT); full scans fine.
- **Secondary index on clustered table**: index-only queries can be *covering* (PK always available → some queries served entirely from the secondary tree without probing data).
- **Informed choice** between the two is exactly the OLTP schema-tuning skill interviewers probe.

## 12. Disadvantages
- **Clustered**: only one order; changing the clustering key (InnoDB PK update) relocates rows (expensive); inserts into the middle of a hot range cause page splits/lock contention (UUID PK problem); secondary lookups need two descents.
- **Non-clustered/heap**: point lookups always have a random page fetch; range scans on any key touch scattered pages; no physical locality for hot keys.
- **`CLUSTER`**: blocking rewrite; order degrades; maintenance burden.
- **Generally**: "clustering by the wrong key" (e.g., random UUID PK) is a classic InnoDB performance disaster — the choice is consequential.

## 13. Interview Questions
1. **Q: Difference between clustered and non-clustered?** A: Clustered = data pages physically ordered by the key (table and index are one structure, at most one per table). Non-clustered = a separate structure referencing rows (heap + index, any number).
2. **Q: How many clustered indexes per table?** A: Exactly one — the physical row order can only match one key.
3. **Q: What is an InnoDB clustered index?** A: The table itself: a B+ tree keyed on the PK whose leaves hold whole rows; secondary indexes store PK values and need a second probe.
4. **Q: How does PostgreSQL organize by default?** A: Heap; every index (incl. PK) is non-clustered, leaves store RIDs; `CLUSTER` can reorder temporarily.
5. **Q: Why is a secondary lookup in InnoDB 2× cost?** A: Secondary index descent → get PK → clustered descent for the row.
6. **Q (scenario): "all orders for a user" is hot.** A: Choose a clustered key on user_id (InnoDB: make user_id the PK or the clustered key) so one user's rows sit contiguously; or cluster on user_id.
7. **Q (tricky): UUID primary keys in InnoDB.** A: Random UUIDs insert into random positions → page splits + cache churn; prefer auto-increment PK (append at the end) or UUIDv7/time-ordered UUIDs.
8. **Q: What does CLUSTER (Postgres) do?** A: Physically rewrites the heap in an index's key order, one-time; subsequent writes degrade the order; re-run periodically.
9. **Q: When prefer heap/non-clustered?** A: Write-heavy workloads, many different query orderings, frequent updates that don't touch indexes, full-scan analytics.
10. **Q (production): covering index on a clustered table?** A: Because the PK is always in a secondary index, queries selecting only secondary-key + PK columns can be answered from the index alone (index-only scan) — an InnoDB trick.
11. **Q: What is a RID?** A: (page, slot); the row locator stored in Postgres index leaves; vs InnoDB's PK-as-locator.
12. **Q: How do inserts differ?** A: Clustered: page splits when inserting mid-range (O(log N), possible lock contention). Heap: O(1) append + per-index maintenance.
13. **Q (scenario): append-only time-series.** A: Cluster by time (or append-ordered heap): inserts land at the end (no splits); range scans read contiguous pages.
14. **Q: Is "clustered index" the same as "sorted file"?** A: Similar goal (physical order) but different mechanism — a B+ tree with page splits vs a flat run with shifting; the tree makes writes feasible.
15. **Q: What happens when you change the clustered key in InnoDB?** A: The row is relocated in the clustered tree (physical move) — expensive; choose the PK/clustering key carefully (surrogate stable keys).
16. **Q (tricky): index-only scans in PostgreSQL?** A: Postgres can answer a query from a non-clustered index alone (no heap fetch) when all needed columns are in the index — "covering index"; vs InnoDB where PK columns are implicitly covered.
17. **Q: Why does MySQL call the PK the "clustered index"?** A: Because InnoDB's B+ tree *is* the table, keyed on PK; there's no separate data file — the data is the index's leaves.
18. **Q (production): table has hot range reads + heavy inserts into that range.** A: Conflict — clustering helps reads, page splits hurt inserts. Mitigation: append-ordered keys, partition by range, or accept splits and measure.
19. **Q: How does MVCC interact with clustering?** A: Postgres: updates create new heap tuples (RID changes) — HOT keeps index entries valid if indexed columns unchanged. InnoDB: row updates in place; PK update = physical move.
20. **Q: How do you pick a clustering key in practice?** A: Identify the dominant access pattern (the query with highest read amplification); the key that groups its target rows into contiguous runs wins; validate with EXPLAIN + measured latency.

## 14. Follow-Up Questions
1. **Q: Can you have a clustered index on a non-PK column in InnoDB?** A: Only if you design the PK to be that column (or use a different PK and keep the hot column as the clustered order via a covering design) — InnoDB clusters specifically on the PK; other engines (SQL Server, Oracle IOT) allow choosing the clustered key.
2. **Q: What's a "covering" index and why does it matter?** A: An index containing all columns the query needs → no heap/data fetch at all (index-only scan); it's the biggest practical win on top of either organization.
3. **Q: How does row size affect clustering?** A: Clustered tables benefit from narrow rows (more rows/leaf page → fewer reads); wide rows dilute the locality benefit; the clustering key should be small (big PKs bloat every secondary index).
4. **Q: Does clustering help joins?** A: Indirectly — join inputs sorted/clustered on the join key enable merge joins and reduce sorts; but it's primarily a data-access (scan) optimization.
5. **Q: What about clustered columnar engines?** A: Columnar stores sort each *column* by a sort key (the "clustered" analog at column scale) — same locality idea, different unit (columns, not rows).

## 15. Coding Example
```sql
-- InnoDB (MySQL): PK = clustered index by default
CREATE TABLE orders (
  order_id BIGINT AUTO_INCREMENT PRIMARY KEY,   -- clustered: rows PK-ordered
  user_id  BIGINT NOT NULL,
  amount   DECIMAL(10,2),
  INDEX idx_user (user_id)                       -- secondary: leaves store PK
);
-- user-orders query: secondary probe (idx_user) + PK probe (clustered) per row
EXPLAIN SELECT * FROM orders WHERE user_id = 42;  -- note "Using index condition"

-- To cluster by user_id instead (hot pattern): make user_id the clustered key
CREATE TABLE orders2 (
  user_id  BIGINT NOT NULL,
  order_id BIGINT AUTO_INCREMENT,
  amount   DECIMAL(10,2),
  PRIMARY KEY (user_id, order_id)                -- clustered on user_id first
);

-- PostgreSQL: heap + non-clustered indexes; one-time physical reorder
CREATE INDEX idx_orders_ts ON orders(created_at);
CLUSTER orders USING idx_orders_ts;              -- rewrite heap in ts order
ANALYZE orders;
-- inserts after this slowly scatter the order; re-run CLUSTER periodically
```
```python
# Read-cost sketch
def clustered_pk_lookup_cost(n_pages):
    import math
    return math.log2(n_pages)                     # one tree descent -> row

def postgres_lookup_cost(n_pages):
    import math
    return math.log2(n_pages) + 1                 # index descent + RID fetch

def innodb_secondary_cost(n_pages):
    import math
    return 2 * math.log2(n_pages)                 # secondary + clustered probe
```

## 16. Industry Usage
- **MySQL/InnoDB**: every table is clustered on the PK; DBAs pick surrogate auto-increment PKs to keep inserts at the hot end and avoid UUID page-split storms.
- **PostgreSQL**: heaps + non-clustered indexes; `CLUSTER` for range locality; `pg_stat_user_tables`/`pg_class.relclustered` to monitor clustering state.
- **Oracle (IOT), SQL Server**: explicit clustered-key choice — "clustered index design" is a standard DBA skill and interview topic.
- **User-centric SaaS schemas**: clustering on `user_id`/`tenant_id` groups a tenant's rows contiguously — the dominant OLTP tuning move for multi-tenant apps.
- **Analytics**: columnar sort keys (Redshift, ClickHouse) extend the same locality principle to columns; range-pruned scans are the payoff.

## 17. References
- MySQL 8.0 Reference Manual, "InnoDB Clustered and Secondary Indexes".
- PostgreSQL docs: CLUSTER, CREATE INDEX (index-only scans), HOT updates.
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 17.2.
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 14.3.
- SQL Server docs: Clustered and Nonclustered Indexes.

## 18. Cheat Sheet
- Clustered: data ordered by key; at most one; leaves hold rows.
- Non-clustered: separate index → RID (heap) or PK (InnoDB).
- InnoDB: table = clustered B+ tree on PK; secondary = 2 probes.
- Postgres: heap + RID indexes; CLUSTER reorders temporarily.
- Hot user reads → cluster on user_id/tenant; hot ranges → time-ordered.
- UUID PK in InnoDB = page-split storm → use auto-inc / UUIDv7.
- Covering index ⇒ no data fetch at all.
- Choose by: dominant access pattern + write amplification.

## 19. Quiz
1. Max clustered indexes per table: a) 0 b) 1 c) 2 d) unlimited → **b**
2. InnoDB clusters on: a) first index b) primary key c) heap d) user choice → **b**
3. Postgres default layout: a) clustered b) heap c) hash d) sorted → **b**
4. Secondary lookup in InnoDB costs: a) 1 descent b) 2 descents c) O(N) d) 0 → **b**
5. Postgres index leaves store: a) PK b) RID c) hash d) data → **b**
6. CLUSTER (Postgres): a) permanent b) temporary reorder c) drops indexes d) partitions → **b**
7. UUID PK in InnoDB causes: a) compaction b) page splits c) covering d) nothing → **b**
8. Covering index enables: a) index-only scan b) full scan c) reorder d) hash join → **a**
9. Which is physically impossible: a) two clustered indexes b) many non-clustered c) RID storage d) PK index → **a**
10. Best clustering key for user-centric tables: a) random UUID b) user_id c) amount d) created_at only → **b**

## 20. Flashcards
- **Q: Clustered index?** → **A:** Data pages ordered by key; one per table; leaves = rows.
- **Q: Non-clustered?** → **A:** Separate index → RID or PK; any number.
- **Q: InnoDB layout?** → **A:** B+ tree on PK; secondary stores PK (2 probes).
- **Q: Postgres layout?** → **A:** Heap + RID indexes; CLUSTER reorders temporarily.
- **Q: Why UUID PK hurts?** → **A:** Random inserts → page splits / cache churn.
- **Q: Covering index?** → **A:** Index holds all query columns → no data fetch.
- **Q: When heap wins?** → **A:** Write-heavy, many orderings, full scans.
- **Q: Pick clustering key by?** → **A:** Dominant access pattern (group hot rows).

## 21. Revision
**Clustered** = table physically ordered by a key (a B+ tree whose leaves are the rows); **one per table**; PK/range reads are a single descent + contiguous leaf runs. **Non-clustered** = rows in a heap, referenced by separate indexes. Two canonical engines: **InnoDB** clusters on the PK (secondary index leaves store the PK → a secondary lookup does *two* descents), while **PostgreSQL** keeps a heap whose index leaves store **RIDs** (index descent + one random page fetch; `CLUSTER` gives a temporary physical reorder). Pick clustering to group the hot rows (user-centric → cluster on user_id; time-series → time order) and avoid random-UUID PKs in InnoDB (page-split storms). A **covering index** (all needed columns) removes the data fetch entirely. Interview script: contrast the two structures, give InnoDB vs Postgres behavior, explain the "one clustered index" law, and name a workload for each.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Clustered vs non-clustered?" | 2 / 13 Q1–Q2 |
| "How many clustered indexes?" | 13 Q2 |
| "InnoDB clustered PK / secondary cost?" | 13 Q3, Q5, Q17 |
| "Postgres heap + RID / CLUSTER?" | 13 Q4, Q8 |
| "UUID PK problem?" | 13 Q7 |
| "Pick a clustering key?" | 13 Q6, Q20 |
| "Covering / index-only scans?" | 13 Q10, Q16 |
| "When prefer heap?" | 13 Q9 |
