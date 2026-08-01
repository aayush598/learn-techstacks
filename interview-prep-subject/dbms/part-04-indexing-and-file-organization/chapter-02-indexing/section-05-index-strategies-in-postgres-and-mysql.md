# Index Strategies in PostgreSQL and MySQL

> **TL;DR**: Real index tuning comes down to a few proven moves: choose composite index **column order** to match the workload (equality first, then range/order), prefer **covering indexes** for index-only scans, use **partial indexes** for hot subsets, understand **leftmost-prefix** limits, and read **EXPLAIN** to find out why an index is (or isn't) used. InnoDB and PostgreSQL differ in clustered-PK, index-only, and NULL handling — know both.

## 1. Why Does This Exist?
Creating an index is easy; making the *right* index is hard. The cost model punishes naive choices: too many indexes slow every write; the wrong column order makes a composite index useless for half your queries; an index the optimizer ignores is pure overhead. Index strategy exists to answer: *for this specific query workload, which keys, in which order, with which filters, and how do I prove it works?* It's the practical layer over index theory — the difference between a schema that crawls at 10M rows and one that stays fast at 1B. Both PostgreSQL and MySQL expose the same core ideas (B+ trees, covering, EXPLAIN) with engine-specific differences (clustered PK vs heap, index-only scans, NULL handling) that a production engineer must know to make correct choices.

## 2. How Does It Work?
- **Composite order rule**: `WHERE a = ? AND b = ?` → index (a, b), equality columns before range/order columns; the *leftmost prefix* of the index is always usable, nothing else.
- **Covering / index-only**: add the columns the query returns so the plan never touches the table (Postgres `Index Only Scan`; InnoDB implicitly covers the PK).
- **Partial / filtered**: index only the hot subset (`WHERE status='open'`) → smaller, cheaper writes, same read benefit for that subset.
- **EXPLAIN-driven tuning**: read the plan (Seq Scan vs Index Scan vs Index Only Scan vs Bitmap Scan), estimated vs actual rows, and confirm the predicate is a real `Index Cond` (not a filter).
- **Engine differences**: InnoDB clusters by PK (secondary lookups probe the clustered tree); Postgres heaps with RID indexes; NULLs not indexed in InnoDB; Postgres indexes NULLs.

## 3. When Is It Used?
- **New schema**: PK + FK indexes + indexes for every known hot query (from the query list, not guesses).
- **Production slowdown**: first step is `EXPLAIN ANALYZE` → find Seq Scans on big tables → design the index that converts them to Index Scans.
- **Covering queries**: dashboard/list queries selecting a few columns → covering composite.
- **Partial use cases**: queues (`WHERE status='pending'`), tenancy filters, active-only reports.
- **FKs & joins**: index every FK column (joins and cascades).
- **After data growth**: re-check with new stats; drop unused indexes (`pg_stat_user_indexes`, MySQL `performance_schema`).

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: index every column.** Rejected — write amplification, space, and cache pressure; the optimizer can't use most of them. Targeted indexes only.
- **Alternative: index nothing and rely on scans.** Rejected at scale — O(N) on 100M rows is seconds; indexes buy millisecond reads.
- **Alternative: follow generic "best practices" without EXPLAIN.** Rejected — every schema differs; the optimizer's decision (with your data + stats) is the only ground truth. Measure, don't guess.
- **Alternative: one wide composite "catch-all" index.** Rejected — leftmost-prefix means a catch-all only works for queries that share its prefix; multiple narrow indexes usually beat one wide.
- **Why EXPLAIN over intuition?** Because the cost model accounts for stats (cardinality, correlation), table size, and memory — the human can't; the plan is the answer.

## 5. Intuuition
An index is a **library of quick-reference books**, and strategy is choosing which quick-reference books to buy. Buying one book per topic (index every column) costs shelves and maintenance but no one reads most of them. The trick is knowing the *actual questions*: if readers always ask "which books by author, then year," buy an author→year composite (equality author first, range year second). A **covering** index is buying a reference that contains the *answer itself* (title + author on the card) so readers never open the shelf. A **partial** index is buying a tiny "active members only" directory — 1% of the entries, 1% of the maintenance. And when readers complain it's slow, you watch them (EXPLAIN) to see if they actually *used* your reference or wandered the aisles (Seq Scan) — then buy precisely what they need.

## 6. Real-World Analogy
A **stadium's "find my seat" kiosks**. The naive version has one kiosk listing every seat in every order (index everything) — huge, outdated, and nobody reads most of it. The well-designed stadium learns the questions: "find seat by section + row" → a composite directory ordered (section, row) — section first because that's the first question asked; "show me all accessible seats" → a partial directory of only wheelchair seats; "how many seats in section 12?" → a directory that *includes the count* so staff never open the seat records (covering). And when a line forms, the manager watches which kiosks are actually used (EXPLAIN) and rebuilds the ones nobody touches. Index strategy = building the right reference books for the questions people actually ask, then verifying they use them.

## 7. Formal Definition
(PostgreSQL docs: Index-Only Scans, Partial Indexes, EXPLAIN; MySQL docs: InnoDB indexes, index cardinality; use-the-plan.)
- **Leftmost prefix**: an index on (a, b, c) can satisfy predicates on (a), (a,b), (a,b,c) — never (b) or (c) alone.
- **Covering index**: contains every column the query references → index-only scan (no table access).
- **Partial index**: `CREATE INDEX ... WHERE predicate` — index only matching rows.
- **Index Cond vs Filter**: `Index Cond` = predicate evaluated during the index descent (good); `Filter` = rows rechecked after (often OK but less efficient).
- **InnoDB specifics**: clustered PK; secondary index leaves store PK values; NULLs not indexed (IS NULL can't use a non-covering index); PK included in every index.
- **Postgres specifics**: heaps + RID indexes; NULLs indexed (IS NULL usable); `Index Only Scan` via visibility map; `Bitmap` plans combine indexes.

## 8. Example
Query set for `orders(user_id, status, created_at, amount)`:
- Q1: `WHERE user_id = 42 AND status = 'open'` → composite **equality-first**: `(user_id, status)`.
- Q2: `WHERE user_id = 42 AND created_at > '2024-01-01'` → `(user_id, created_at)` (equality then range).
- Q3: `SELECT user_id, status, created_at FROM orders WHERE status = 'open'` → **covering** partial: `(status, created_at, user_id) WHERE status='open'` → index-only.
- Bad: `(status, user_id)` for Q1 if Q1 filters by user_id first (status is low-selectivity → index returns half the table).
- **Before/after**:
```
Seq Scan on orders (cost=1000..35000, rows=1M)      -- no index
Index Only Scan using idx_q3 (cost=... rows=5000)   -- covering partial index
```
- **InnoDB note**: the PK is implicit in every index, so `SELECT id, user_id FROM orders WHERE user_id=42` is index-only off `(user_id)` alone.

## 9. Internal Working
1. **Collect the workload**: top queries from logs/slow-query; note the equality/range/order columns.
2. **Design**: for each query — equality columns in index order, then range/order column; add returned columns if the query is hot (covering); add a WHERE to a partial index for the hot subset.
3. **Avoid**: overlapping indexes (`(a)` + `(a,b)` — drop the prefix-only one), low-selectivity leading columns (status first when it matches 90%), unindexed FK columns.
4. **EXPLAIN ANALYZE**: confirm `Index Scan`/`Index Only Scan`, check `Index Cond` (not `Filter` for the main predicate), compare estimated vs actual rows (stats stale?).
5. **Monitor**: `pg_stat_user_indexes.idx_scan` / `pg_indexes_size`; drop indexes with ~0 scans; refresh stats (`ANALYZE`) after big changes.
6. **Re-validate at scale**: what's fast at 1M may change at 100M — revisit with fresh stats.

## 10. Time Complexity
- **Point via B+ index**: O(log_f N) ≈ 3–4 reads (+ table fetch if not covering).
- **Range via index**: O(log_f N + k) where k = result pages.
- **Index-only scan**: O(log_f N) — no table access.
- **Scan without index**: O(N) pages.
- **Partial index**: O(log_f |subset|) — cheaper writes too (only subset maintained).
- **Write cost**: O(log_f N) per index per write (why *fewer, right* indexes beat many).

## 11. Advantages
- **Measured, targeted speedups**: each index maps to a real query; nothing wasted.
- **Index-only scans**: hot list queries skip the table entirely.
- **Partial indexes**: tiny + cheap to maintain while covering the hot subset.
- **Smaller maintenance surface**: fewer, right indexes beat many wrong ones.
- **Diagnosable**: EXPLAIN makes every decision verifiable; unused indexes are discoverable and droppable.

## 12. Disadvantages
- **Design cost**: needs the actual query workload (often undocumented).
- **Workload drift**: an index tuned for today's queries hurts tomorrow's writes.
- **Engine quirks**: NULL handling, clustered PK, index-only differences between PG/MySQL must be remembered or you'll mis-predict plans.
- **Stale stats**: without ANALYZE, the optimizer mis-estimates and ignores your index.
- **Still a trade**: every index taxes writes and cache; tuning is continuous, not one-time.

## 13. Interview Questions
1. **Q: How do you choose the columns for a composite index?** A: Match the query: equality predicates first (in any order), then the range/order column last; keep leftmost prefixes usable for other queries.
2. **Q: What is the leftmost-prefix rule?** A: An index on (a,b,c) serves (a), (a,b), (a,b,c) only — leading-column queries; (b) or (c) alone can't use it.
3. **Q: What is a covering index?** A: An index containing every column the query needs → index-only scan, no table access.
4. **Q: What is a partial index?** A: `CREATE INDEX ... WHERE predicate` — indexes only matching rows; smaller, cheaper, faster for the hot subset (e.g., status='open').
5. **Q (scenario): query `WHERE status='open' ORDER BY created_at`.** A: Partial index `(created_at) WHERE status='open'` — serves the filter and the order in one tiny structure.
6. **Q: How do you know an index is being used?** A: `EXPLAIN ANALYZE` — look for `Index Scan`/`Index Only Scan` and `Index Cond`; a `Seq Scan` or `Filter` on the main predicate means it isn't.
7. **Q (tricky): index on (user_id, created_at) — does `WHERE created_at > ...` use it?** A: No — created_at is not the leftmost column; only queries filtering on user_id (or user_id+created_at) can use it.
8. **Q: Why does InnoDB do index-only on `SELECT id, user_id ... WHERE user_id=?` with just a (user_id) index?** A: InnoDB's clustered PK is implicitly included in every secondary index — id (the PK) is always available without a table probe.
9. **Q (production): why is my index ignored?** A: Stale stats (run ANALYZE), low selectivity (scan cheaper), function/coercion on the column (need expression index), or a leading wildcard LIKE.
10. **Q: Equality vs range in composite order — why equality first?** A: Equality filters narrow to a point in the first column; a range first forces scanning a large interval before applying the rest — equality-first prunes earliest.
11. **Q: Postgres vs InnoDB: what's different about NULL indexing?** A: Postgres indexes NULLs (IS NULL can use an index); InnoDB does not (IS NULL on a non-covering index falls back to a scan).
12. **Q (tricky): two indexes (a) and (a,b) — redundant?** A: (a) is a leftmost prefix of (a,b) — keep only (a,b); the standalone (a) is duplicate maintenance.
13. **Q: When would you use a Bitmap plan?** A: When several indexes each match some rows and the planner ORs/ANDs their bitmaps (Bitmap Index Scan + Bitmap Heap Scan) — common for multi-column ORs.
14. **Q: How do you tune a slow ORDER BY?** A: An index matching the ORDER BY columns (with any WHERE equality columns first) gives sorted index order — no sort step (avoid `Sort` in the plan).
15. **Q (scenario): queue table with status='pending' hot.** A: Partial index on the pending subset + a small poll — the classic "index the hot subset" pattern; keep it tiny so writes are cheap.
16. **Q: What does ANALYZE do and why does it matter?** A: Refreshes statistics (histograms, cardinality) that the optimizer uses to estimate rows; stale stats → wrong plans → ignored indexes.
17. **Q (hard): covering index in Postgres needs what to skip the table?** A: A visibility map bit for the page — recently-updated pages force a heap visit for visibility checks; long-running transactions hurt index-only scans.
18. **Q: How do you find unused indexes?** A: `pg_stat_user_indexes` (idx_scan ≈ 0) / `pg_indexes_size` for the bloat; MySQL `performance_schema.table_io_waits_summary_by_index_usage`; drop with care after checking a real workload window.
19. **Q (tricky): should the FK column be indexed?** A: Yes — joins and ON DELETE CASCADE need the FK index in both engines; an unindexed FK makes cascades and child joins full scans.
20. **Q: What's your complete "slow query → fix" recipe?** A: (1) capture slow queries; (2) EXPLAIN ANALYZE each; (3) design indexes: equality cols → range/order → covering extras → partial for subsets; (4) verify Index Scan + Index Cond, re-measure; (5) monitor and drop the unused.

## 14. Follow-Up Questions
1. **Q: How does cardinality estimation drive index choice?** A: The optimizer multiplies estimated selectivity × table size; if the estimate says "most rows" it scans. High-quality stats (ANALYZE) make these estimates accurate.
2. **Q: What are "covering" trade-offs?** A: Adding return columns grows the index and its write cost; only cover the hot queries that actually avoid the table fetch — measure the gain.
3. **Q: How do generated/computed columns interact with indexes?** A: MySQL generated columns and Postgres expression indexes both index derived values — the fix for functions on columns.
4. **Q: What happens to indexes during partitioning?** A: Global indexes are unusual; most engines index per partition — queries prune partitions first, then use local indexes (Postgres per-partition indexes).
5. **Q: How do you handle a "hot column" that is also updated often?** A: Balance: the index helps reads but every update rewrites its entries; if updates dominate on that column, consider a narrower/partial index or accept the cost.

## 15. Coding Example
```sql
-- Workload-driven index design (PostgreSQL)
CREATE TABLE orders (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id BIGINT NOT NULL,
  status  TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  amount  NUMERIC
);

-- Q1: WHERE user_id = ? AND status = ?           -> equality-first composite
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Q2: WHERE user_id = ? AND created_at > ? ORDER BY created_at
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at);

-- Q3: SELECT status, created_at FROM orders WHERE status='open' (hot queue poll)
CREATE INDEX idx_orders_open_cover ON orders(status, created_at) WHERE status = 'open';

-- Q4: join on user (users.id) + ON DELETE CASCADE -> index the FK
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Prove it:
EXPLAIN (ANALYZE, BUFFERS)
SELECT status, created_at FROM orders WHERE status = 'open' ORDER BY created_at;
--   -> Index Only Scan using idx_orders_open_cover  (no Seq Scan, no Sort)

-- Find unused indexes
SELECT relname, indexrelname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes
WHERE idx_scan = 0 ORDER BY pg_relation_size(indexrelid) DESC;

-- MySQL equivalent check
EXPLAIN SELECT id, user_id FROM orders WHERE user_id = 42;  -- id covered by PK (InnoDB)
```

## 16. Industry Usage
- **PostgreSQL**: partial indexes for queue tables, BRIN for logs, index-only scans via visibility maps, `pg_stat_user_indexes` for index hygiene — standard production playbook.
- **MySQL/InnoDB**: PK = clustered (surrogate auto-increment preferred), secondary indexes implicitly cover the PK, NULL-not-indexed gotcha, `EXPLAIN` + `SHOW INDEX` tuning.
- **Every web stack** (Prisma, Rails, Django ORMs): generated FK indexes and query-driven composites are the difference between a schema that holds and one that collapses at 100M rows.
- **Data-intensive SaaS**: multi-tenant schemas index on tenant_id first (leftmost), partial-index hot subsets, and drop cold indexes — the operational norm.
- **Interview batteries** (Amazon/Google/Meta DB rounds): composite ordering, leftmost-prefix, covering, partial, EXPLAIN diagnosis are the exact skills probed.

## 17. References
- PostgreSQL docs: Index-Only Scans, Partial Indexes, CREATE INDEX, EXPLAIN, pg_stat_user_indexes.
- MySQL 8.0 Reference Manual: InnoDB Indexes, Optimizer Use of Indexes, EXPLAIN Output.
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 14 (query tuning / physical design).
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 18–19.
- Use the Index, Luke! (use-the-index-luke.com) — Markus Winand, the standard index-strategy reference.

## 18. Cheat Sheet
- Composite: equality columns first, then range/order; leftmost prefixes only.
- Covering: index all returned columns → index-only scan.
- Partial: `WHERE subset` → tiny index for the hot subset.
- Equality-before-range: prune earliest.
- EXPLAIN: Index Scan/Index Only Scan + Index Cond = good; Seq Scan/Filter = bad.
- InnoDB: clustered PK, PK implicitly in every index, NULLs not indexed.
- Postgres: heap+RID, NULLs indexed, visibility map for index-only.
- Redundant: (a) vs (a,b) → keep (a,b). Drop unused (idx_scan=0).

## 19. Quiz
1. Composite order for `WHERE a=? AND b > ?`: a) (b,a) b) (a,b) c) (b) d) (a) → **b**
2. Index (a,b,c) serves: a) (b) b) (a,b) c) (c) d) (b,c) → **b**
3. Covering index enables: a) Seq Scan b) Index Only Scan c) Bitmap d) Sort → **b**
4. Partial index filters: a) rows at query b) index membership c) columns d) nothing → **b**
5. InnoDB implicitly includes in every secondary index: a) RID b) PK c) status d) hash → **b**
6. Postgres vs InnoDB NULLs: a) both index b) PG indexes, InnoDB doesn't c) neither d) InnoDB only → **b**
7. A plan showing Seq Scan means: a) index used b) index not used c) covering d) sort → **b**
8. Stale stats cause: a) better plans b) optimizer ignores index c) crashes d) bloat → **b**
9. (a) and (a,b) both present → : a) keep both b) (a) redundant c) (a,b) redundant d) neither → **b**
10. Equality-before-range because: a) order is random b) prunes earliest c) smaller files d) sort → **b**

## 20. Flashcards
- **Q: Composite column order?** → **A:** Equality first, then range/order; leftmost prefixes usable.
- **Q: Covering index?** → **A:** Contains all query columns → index-only scan.
- **Q: Partial index?** → **A:** `WHERE subset` — index the hot subset only.
- **Q: When is an index ignored?** → **A:** Stale stats, low selectivity, function/coercion, leading wildcard.
- **Q: InnoDB implicit column?** → **A:** PK in every secondary index; NULLs not indexed.
- **Q: Postgres index-only need?** → **A:** Visibility map bit; heap check for recent updates.
- **Q: Redundant index pair?** → **A:** (a) and (a,b) → keep (a,b).
- **Q: How to prove an index helps?** → **A:** EXPLAIN ANALYZE → Index Scan + Index Cond, re-measure.

## 21. Revision
Index strategy = build the **right reference for the workload**, then prove it. The rules: **composite order** equality-first then range/order (leftmost prefixes only); **covering** indexes (all returned columns) for index-only scans; **partial** indexes for hot subsets (queue `status='open'`); equality-before-range to prune earliest. Diagnose with **EXPLAIN ANALYZE** — `Index Scan`/`Index Only Scan` + `Index Cond` = good; `Seq Scan`/`Filter` = the index isn't being used (check stats/selectivity/functions). Engine quirks: **InnoDB** clusters by PK (PK implicit in every index, NULLs not indexed), **Postgres** heaps with RIDs (NULLs indexed, visibility map gates index-only). Housekeeping: drop redundant (`(a)` vs `(a,b)`) and unused (`idx_scan = 0`) indexes; ANALYZE after changes. Interview script: given a query, write the index (equality→range→covering/partial), predict the EXPLAIN output, and state the engine-specific caveat.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Composite index column order?" | 2 / 13 Q1, Q10 |
| "Leftmost-prefix rule?" | 13 Q2 |
| "Covering / index-only scans?" | 13 Q3, Q17 |
| "Partial index / hot subset?" | 13 Q4–Q5, Q15 |
| "Why is my index ignored?" | 13 Q9 |
| "InnoDB vs Postgres differences?" | 13 Q8, Q11 |
| "Unused/redundant indexes?" | 13 Q12, Q18 |
| "Slow-query recipe?" | 13 Q20 |
