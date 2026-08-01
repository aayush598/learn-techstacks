# Join Algorithms: Nested Loop, Merge, Hash

> **TL;DR**: Joins are physically executed by one of three strategies — Nested Loop (O(n·m), great with an index), Merge Join (O(n+m) on sorted inputs), or Hash Join (O(n+m), the big-unindexed-workhorse) — and picking the right one is the optimizer's most consequential decision.

## 1. Why Does This Exist?
"JOIN orders ON customers" is logical — but the engine must *physically combine* two sets of rows, and the naive "compare every row with every row" is O(n·m), catastrophic for big tables. Join algorithms exist to combine relations *fast* using the tools we have: indexes (nested loop can exploit a B-tree), sorted order (merge join), or hashing (hash join builds a lookup). Choosing between them is the difference between a 10ms query and a 10-minute query. This is also the most popular "explain your EXPLAIN" topic in interviews — because joins are where most slow queries live.

## 2. How Does It Work?
1. **Nested Loop Join (NLJ)**: for each row of the *outer* relation, scan the *inner* relation for matches. If the inner has an index on the join key → **Index Nested Loop** (O(n · log m) per-match lookups). Cost O(n·m) worst case; ideal when the outer is tiny (or the inner is indexed and small).
2. **Merge Join**: sort both relations by the join key (if not already sorted — e.g., from an index scan), then walk both in lockstep, advancing the pointer of the smaller value. O(n log n + m log m) for sorts, O(n+m) for the merge itself; requires a sortable (comparison) join key; great for range/equality on already-sorted inputs.
3. **Hash Join**: build a hash table on the join key of the *build* side (usually the smaller relation); then for each row of the *probe* side, look it up. O(n+m) with one pass (no sorting); ideal for equality joins of large unindexed relations; uses memory (`work_mem`), spills to disk if the build side is too big.

## 3. When Is It Used?
- **NLJ**: `WHERE c.id = o.customer_id` with an index on `o.customer_id` and `customers` small (common in OLTP: look up a handful of orders per customer).
- **Merge Join**: join keys that come out of index scans already sorted (or a `ORDER BY` / window that needs order anyway); range joins (`a.x BETWEEN b.y AND b.z`); no good hash key.
- **Hash Join**: big equi-joins without indexes (analytics, ETL, reporting) — the workhorse of data-warehouse queries.
- The optimizer picks by estimated cost, not by what you write — you *influence* it with indexes, statistics, and `work_mem`.

## 4. Why Wasn't Another Approach Chosen?
- *Always nested loop*: simple but O(n·m) — unacceptable for big joins; only fine with an index + tiny outer.
- *Always sort-merge*: great when sorted, but sorting costs O(n log n) and it can't use a hash key's randomness — wasteful when no order is needed.
- *Always hash*: fastest for big equi-joins but (a) doesn't preserve order, (b) needs equality keys, (c) memory-heavy (spills hurt), and (d) overkill for tiny tables where NLJ wins.
- *Exotic joins (bitmap join, sort-merge variants, distributed joins)*: exist (e.g., bitmap for several OR conditions, semi/anti-join variants), but the three classics cover ~99% of real plans — hence the interview focus.
- *Physical join at the storage layer (join pushdown)*: some engines (StarRocks, some columnar) push joins into scans; but the three algorithms remain the semantic core.

## 5. Intuition
**NLJ** = a slow dance: for each of your dance partners (outer rows), you look through the crowd (inner) for matches. Fine for a small party; terrible for a stadium. **Merge** = two sorted lines merging into one: both lines are already in order (perhaps from index scans), so you compare heads and advance the smaller — one clean pass. **Hash** = a coat-check: toss every coat (build side) into labeled racks by name hash (O(1) lookup); each guest (probe side) checks their coat instantly. You'd never use a coat-check for 5 coats (overhead), but for 10,000 coats it beats scanning the whole rack for each person.

## 6. Real-World Analogy
**Matching resumes to job postings**: NLJ = for each resume, read every posting (fine for 10 postings, madness for 10,000). Merge = sort both piles by "required skill" and walk them side-by-side, ticking matches (one pass, but you paid to sort). Hash = file every posting into a box per skill keyword (build), then look up each resume's skills in the boxes instantly (probe) — by far the fastest for big piles, as long as matching is by exact keyword. HR systems use the "hash" approach; that's why job search feels instant.

## 7. Formal Definition
For relations R (size n) and S (size m), join key K:
- **Nested Loop Join**: for each r ∈ R, for each s ∈ S, emit if r.K = s.K. **Cost**: n·m block accesses (naive); with an index on S.K: n·(c + c_index_lookup) where c = cost per probe — **O(n·log m)** typical.
- **Merge Join**: sort R and S on K (cost O(n log n + m log m)), then merge: advance the side with the smaller current key; emit equal pairs. **Cost**: O(n log n + m log m) sorting + **O(n + m)** merge. If inputs are already sorted (index scans), the merge alone costs O(n+m).
- **Hash Join**: build a hash table H on S.K (smaller relation — the *build* side), scanning S once (O(m)); probe H for each r ∈ R (O(n)). **Cost**: O(n+m) expected, plus memory for H (spill to disk if it exceeds `work_mem`, turning it into a grace/partitioned hash join with extra passes).

## 8. Example
Join `orders (10M rows)` ⋈ `customers (100K rows)` on `customer_id`.
- **NLJ (customers outer, index on orders.customer_id)**: for each of 100K customers, one B-tree probe on orders (~3-4 page reads each) → ~300-400K page reads, ~seconds. Great when "customers" is the small side.
- **NLJ (orders outer, no index)**: 10M × 100K = 10¹² comparisons — hours. Never.
- **Merge Join**: sort both by customer_id (already sorted if indexes are used): O(10M + 100K) merge — one pass over each; excellent if the inputs come from index scans.
- **Hash Join (typical winner)**: build hash on customers (100K rows, fits memory), probe orders (10M rows): ~10M hash probes ≈ a few seconds, no sort. The optimizer usually picks this when neither side is tiny and there's no sorted input.

## 9. Internal Working
1. The optimizer estimates each candidate join (Section 03) using relation sizes, indexes, and join selectivity; it picks the cheapest.
2. **Hash join execution**: (a) choose build side (smaller after filtering); (b) scan build side, insert into hash table (key = join column, value = row pointer); (c) scan probe side, look up each key, emit matches; (d) if the table exceeds `work_mem`, *partition* (grace hash join: split both sides by hash, recursively) and spill partitions to temp files; (e) hash joins are naturally *right-deep* tolerant and preserve no order (probe output unordered).
3. **Merge join execution**: (a) get both inputs sorted on the key (explicit sort node, or index scans already in order); (b) two pointers; compare keys; advance the smaller; when equal, emit and handle duplicates carefully (group by same key); O(n+m).
4. **NLJ execution**: outer = the driving side (usually filtered small relation); inner = the looked-up side (indexed). For each outer row, probe the inner index; correlated/parameterized plans push the outer value into the inner scan.
5. Parallel joins: hash joins can be parallelized by partitioning the probe side across workers; NLJ parallelizes trivially (split outer).

## 10. Time Complexity
- NLJ: O(n·m) worst; O(n · h(m)) with an index (h = B-tree height, ~3-4).
- Merge: O(n log n + m log m) including sorts; **O(n+m)** if both pre-sorted.
- Hash: O(n+m) expected (one build + one probe); O((n+m) log) with spills.
- Block-transfer versions: NLJ block-nested-loop O(n·m/B); hash typically the winner for large equal-join workloads.
- Memory: hash needs O(m) (build side); merge needs O(n+m) for sorts (or in-memory runs); NLJ O(1).

## 11. Advantages
- **NLJ**: minimal memory; great when outer is tiny or inner is indexed; preserves outer order; supports non-equi joins (range) trivially; the OLTP default.
- **Merge**: no random access (sequential scans on both sides after sort); preserves sorted order for downstream operations (ORDER BY, window, group); handles range joins.
- **Hash**: fastest for large equi-joins without indexes; single pass per side (no sorting); robust to data skew on the key (hash spreads).
- Having all three lets the optimizer cover every shape.

## 12. Disadvantages
- **NLJ**: O(n·m) without an index — the classic "slow join" failure mode (nested loop over big unindexed relations).
- **Merge**: sorting is expensive (O(n log n)); duplicates in keys complicate the merge; needs a comparison-ordered key.
- **Hash**: memory-hungry (build side in RAM; spills slow it down 10-100x); equality-only keys (no range joins); no output ordering; skew on the probe key degrades lookups.

## 13. Interview Questions
1. **Q: What are the three main join algorithms?** A: Nested Loop Join (for each outer row, find matching inner rows — O(n·m) worst, O(n·log m) with an index), Merge Join (sort both sides by the join key, then one linear pass — O(n+m) if pre-sorted), Hash Join (build a hash table on the smaller side, probe with the larger — O(n+m)).
2. **Q: When would you use a hash join?** A: Equality joins of large relations with no useful index and no need for sorted output — the analytics/ETL workhorse. It does one build pass + one probe pass with no sorting.
3. **Q: When would you use a nested loop join?** A: When the outer relation is small and the inner has an index on the join key (each outer row → cheap indexed lookup), or when the join is not on equality (range joins) where hash doesn't apply. Classic OLTP pattern.
4. **Q: When would you use a merge join?** A: When both inputs are already sorted on the join key (e.g., from index scans or an explicit sort that's needed anyway) — the merge is a single linear pass over each. It also handles range joins.
5. **Q: TRICKY: Is nested loop always worse than hash?** A: No. With a tiny outer (say 100 rows) and an indexed inner, NLJ does ~400 page reads — far cheaper than building a hash table over a 10M-row relation. The optimizer compares *estimated costs*, not algorithm fame.
6. **Q: What's the cost formula for a hash join?** A: O(n + m) page/CPU operations (build m, probe n) plus memory for the hash table (build side); if the build side exceeds `work_mem`, partitioning/spill adds passes — typically 2×-3× the base cost.
7. **Q: What is the build side and why does it matter?** A: The relation whose rows go into the hash table (ideally the smaller/filtered one) — it determines memory use; the other side is probed. Choosing the wrong build side can cause spills and order-of-magnitude slowdowns.
8. **Q: What happens when the hash table doesn't fit in memory?** A: The hash join *partitions* both sides by hash (grace hash join): each partition is processed separately, spilled to temp files; matching partitions are re-read. Spilling slows the join 10-100x — which is why raising `work_mem` can dramatically speed up big joins.
9. **Q: What is the difference between block-nested-loop and index-nested-loop?** A: Block NLJ processes the inner relation in page-size chunks (fewer block transfers, O(n·m/B)); index NLJ uses an index on the inner join key for O(log) lookups per outer row. The optimizer picks whichever the index/statistics support.
10. **Q: Why does a merge join need sorted input?** A: The merge is a two-pointer walk that relies on both keys being non-decreasing — if unsorted, the "advance the smaller" logic breaks. Hence the sort node (or an index scan that provides order). Sorting costs O(n log n).
11. **Q: TRICKY: Can a hash join produce sorted output?** A: No — hash buckets destroy order. If the query needs `ORDER BY`, the executor adds a Sort after the hash join (or the optimizer prefers a merge join that preserves order). That's a hidden cost to remember in plans.
12. **Q: What does "parameterized/correlated nested loop" mean?** A: The inner scan takes the outer row's join value as a parameter (a "parameterized path"), turning the inner into a per-row index probe — the classic "small table × indexed big table" join. EXPLAIN shows `Index Scan ... using o_customer_idx (customer_id=$1)`.
13. **Q: PR: My join is a nested loop over two 10M-row tables. What happened?** A: The optimizer found no usable index and estimated it cheapest (bad stats?) or the join is non-equi (range) where hash doesn't apply. Fixes: add an index on the join key (enables index NLJ/merge), `ANALYZE` to refresh stats, or `work_mem`/`enable_hashjoin` hints to steer it.
14. **Q: What's the difference between equi-join and theta/range join for algorithms?** A: Hash join requires equality (an equi-join). Range joins (`a.x < b.y`) need NLJ or merge — hash can't look up a range. This is why merge joins exist for analytic range joins.
15. **Q: PRODUCTION: How do you choose join order yourself for a report?** A: Smallest/filtered relation as the build side (hash) or outer (NLJ); use indexes on join keys; ensure statistics are fresh; read `EXPLAIN ANALYZE` to confirm actual rows match estimates — then fix the estimates/indexes rather than brute-forcing hints.
16. **Q: What is a semi join / anti join and which algorithms apply?** A. Semi join: emit rows from one side that have a match (`IN`/`EXISTS`); anti join: rows with no match (`NOT IN`/`NOT EXISTS`). All three algorithms have semi/anti variants (hash semi join, merge anti join) — the executor can stop early on the first match.

## 14. Follow-Up Questions
1. **Q: What is the "grace" hash join and when is it used?** A: The partitioned variant for build sides too big for memory: partition both sides by hash into buckets, recursively join matching buckets; each bucket fits memory. It trades extra passes for bounded memory.
2. **Q: What is a "merge join without sort" (when is it possible)?** A: When both inputs are index scans on the same key (already in order) — the sort nodes vanish, and the merge is O(n+m) with no extra cost. This is why covering indexes that match the join key are so valuable.
3. **Q: How do parallel joins work?** A: Hash join: parallel workers build the hash table, then probe disjoint partitions of the probe side. NLJ: split the outer across workers. Merge: parallel sort then a merged merge. Costs change; `max_parallel_workers_per_gather` controls it.

## 15. Coding Example
```sql
-- Force/observe join algorithms (Postgres)
SET enable_nestloop = off;   -- optimizer will avoid nested loop (debugging only)
SET enable_hashjoin = off;
SET enable_mergejoin = off;

EXPLAIN (ANALYZE, BUFFERS)
SELECT c.name, o.amount
  FROM customers c JOIN orders o ON o.customer_id = c.id
 WHERE c.city = 'Berlin';
-- Typical output:
--   Hash Join  (cost=...)
--     Hash Cond: (o.customer_id = c.id)
--     ->  Seq Scan on orders ...
--     ->  Hash
--         ->  Seq Scan on customers ...
```
```python
# Simulate the three algorithms' behavior on join keys
def nested_loop(R, S, key):
    return [(r, s) for r in R for s in S if r[key] == s[key]]

def merge_join(R, S, key):
    R, S = sorted(R, key=lambda x: x[key]), sorted(S, key=lambda x: x[key])
    i = j = 0; out = []
    while i < len(R) and j < len(S):
        if R[i][key] < S[j][key]: i += 1
        elif R[i][key] > S[j][key]: j += 1
        else:
            out.append((R[i], S[j]))
            j += 1                       # handle duplicates by re-checking same R
            if j == len(S): j = 0; i += 1
    return out

def hash_join(R, S, key):                 # build on S, probe with R
    table = {}
    for s in S: table.setdefault(s[key], []).append(s)
    return [(r, s) for r in R for s in table.get(r[key], [])]
```

## 16. Industry Usage
- **PostgreSQL**: hash join is the default for large equi-joins; merge join with index-ordered inputs; index NLJ for OLTP. `work_mem`, `enable_*join` flags, `hash_mem_multiplier`.
- **MySQL InnoDB**: NLJ (with index) historically; hash join added in 8.0.18 (for `>=` join types); `join_buffer_size`.
- **SQL Server**: all three + `MERGE`/`HASH`/`LOOP` join hints; adaptive joins (hash↔loop switch at runtime).
- **Oracle**: all three with nested-loop/hash/sort-merge hints; `USE_HASH`, `USE_NL`, `USE_MERGE`.
- **Columnar/MPP (Redshift, Snowflake, BigQuery, ClickHouse)**: hash joins dominate (built for big equi-joins); merge for ordered data; broadcast vs shuffle (distributed) join variants.
- Every slow-query war story is, at its core, "the optimizer chose the wrong join / a scan instead of a seek."

## 17. References
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 13.3 (join operations) — cost formulas for nested-loop/merge/hash.
- Elmasri & Navathe, Ch. 18.3.
- PostgreSQL docs, "Planner/Optimizer": https://www.postgresql.org/docs/current/planner-optimizer.html and `work_mem`: https://www.postgresql.org/docs/current/runtime-config-resource.html
- MySQL 8.0 docs, "Nested-Loop Join Algorithms" & "Hash Join": https://dev.mysql.com/doc/refman/8.0/en/nested-loop-joins.html
- Graefe, "Query Evaluation Techniques for Large Databases" (1993).

## 18. Cheat Sheet
- NLJ: outer×inner; O(n·m) naive, O(n·log m) with inner index; tiny outer + index = OLTP king.
- Merge: sort both by key (O(n log n + m log m)), merge O(n+m); needs pre-sorted inputs to shine; handles ranges.
- Hash: build smaller side + probe larger; O(n+m); equality-only, no order, memory O(m).
- Build side = smaller relation; spills to disk when > `work_mem` (10-100x slower).
- No optimizer rule beats cost estimates: 100-row outer × indexed 10M inner → NLJ wins.
- Hash destroys order; merge preserves it; parameterized NLJ = per-row index probe.
- Range joins → NLJ or merge only.
- `EXPLAIN` shows the chosen join; `enable_*` flags/hints are debug tools.

## 19. Quiz
1. Worst-case cost of naive nested loop: a) O(n+m) b) O(n·m) c) O(n log n) d) O(1) → **b**
2. Hash join requires: a) sorted input b) equality join key c) an index d) two passes → **b**
3. Merge join shines when: a) both inputs sorted b) no index c) tiny outer d) any time → **a**
4. The build side of a hash join should be: a) the bigger side b) the smaller side c) random d) sorted → **b**
5. Hash tables too big for memory cause: a) sorts b) spills (10-100x slower) c) aborts d) merge → **b**
6. Which join can preserve output order? a) hash b) merge c) both d) neither → **b**
7. Range join (`a.x < b.y`) can use: a) hash b) NLJ/merge c) only merge d) nothing → **b**
8. A parameterized NLJ is: a) a per-row index probe b) a sort c) a hash lookup d) a bitmap → **a**

## 20. Flashcards
- **Q: Three join algorithms?** → **A:** Nested Loop, Merge, Hash.
- **Q: NLJ cost?** → **A:** O(n·m) naive; O(n·log m) with an index on the inner key.
- **Q: Merge join cost?** → **A:** O(n log n + m log m) with sorts; O(n+m) merge if pre-sorted.
- **Q: Hash join cost?** → **A:** O(n+m) expected (build smaller, probe larger); spills if > work_mem.
- **Q: When NLJ?** → **A:** Tiny outer + indexed inner (OLTP); range joins.
- **Q: When merge?** → **A:** Both inputs already sorted on the key.
- **Q: When hash?** → **A:** Large equi-joins, no index, order not needed.
- **Q: Hash join output order?** → **A:** None — unordered (adds a Sort if ORDER BY needed).

## 21. Revision
Joins: NLJ = per-outer-row inner probe (indexed → fast; naive O(n·m)); Merge = sort both then one linear walk (needs sorted input / index order; O(n+m)); Hash = build small side + probe big (O(n+m), equality only, no order, memory-bound). The optimizer picks by *estimated cost*: tiny outer + index ⇒ NLJ, sorted inputs ⇒ merge, big unindexed equi ⇒ hash. Spills = 10-100x slower. `work_mem`, stats freshness, and indexes steer the choice. Range joins → NLJ/merge only.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Explain the three join algorithms." | 1, 2, 7 |
| "When is each join used?" | 3, 13 |
| "Cost formulas for each?" | 7, 8 |
| "Is NLJ always bad?" | 13 |
| "What is a build side / spill?" | 8, 9, 13 |
| "Does hash join preserve order?" | 13, 14 |
| "Range joins with which algorithms?" | 13 |
| "Why is my join slow / nested loop over huge tables?" | 13, 16 |
