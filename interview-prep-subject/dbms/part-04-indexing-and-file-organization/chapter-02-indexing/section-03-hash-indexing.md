# Hash Indexing

> **TL;DR**: A hash index maps keys to buckets via a hash function, giving **O(1) expected** exact-match lookups — but only exact matches: no ranges, no ORDER BY, no prefix scans. Static hashing fixes the bucket count once (overflow chains degrade it); dynamic schemes (**extendible** and **linear hashing**) grow the bucket count incrementally. PostgreSQL ships a dynamic hash access method; MySQL's MEMORY engine and most NoSQL stores (DynamoDB, Cassandra) rely on hash/partition thinking for primary-key access.

## 1. Why Does This Exist?
A B+ tree finds a key in ~3–4 page reads. A hash index finds it in **~1–2** — compute h(key), read one bucket. When the workload is pure exact-match (get row by primary key, key-value lookups, `user_id = 42`), hashing is provably faster and simpler than any tree. That's why hash indexing exists: for point lookups it's the O(1) alternative to the tree's O(log N), and for *equality joins* it eliminates the ordering overhead entirely. But hashing throws away order — a hash index can't answer `BETWEEN`, `ORDER BY`, or `LIKE 'ab%'` — so DBs keep it as the *specialized* access method while B+ trees remain the general default. Understanding hash indexing also explains how key-value stores and partitioned tables work under the hood.

## 2. How Does It Work?
- **Static hashing**: choose M buckets; bucket = h(K) mod M; store (key, locator) in the bucket (a page, with overflow pages chained). Point lookup: hash → bucket → scan (usually 1 page). Insert: same bucket append. **Problem**: fixed M — growth → many overflow chains (lookups degrade toward O(N)); shrinking → wasted space.
- **Extendible hashing**: maintain a *directory* of 2^d entries pointing to buckets. On overflow, **split one bucket** (rehash its entries with a +1-bit hash), double the directory only when needed. Most lookups stay 2 page reads (directory + bucket).
- **Linear hashing**: no directory; split buckets **round-robin** (bucket pointer advances one per split) as load crosses a threshold; grows M incrementally. Amortized O(1).
- **Hash joins / hash partitioning** reuse the same idea: partitioning by hash routes each row to one partition; hash joins bucket both inputs then match within buckets.

## 3. When Is It Used?
- **Exact-match point lookups**: `WHERE pk = ...`, key-value get, dedup checks.
- **Equality joins on a key**: hash joins bucket by join key (no ordering needed).
- **NoSQL/key-value engines**: DynamoDB partition keys, Cassandra/Couchbase, Redis tables — hash placement for O(1) access.
- **PostgreSQL**: hash index access method (`USING hash`); improved since PG10 (WAL-logged, crash-safe).
- **MySQL**: MEMORY storage engine supports hash indexes; InnoDB doesn't (clustered B+).
- **NOT for**: ranges, ORDER BY, GROUP BY adjacency, prefix LIKE, sorting, or low-selectivity filters.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: B+ tree for everything.** Works, but 3–4 page reads vs hash's ~1–2 for exact lookups; when order is never needed, the tree's ordering machinery is pure overhead. Chosen when ranges matter; rejected for pure point workloads.
- **Alternative: static hash only.** Fixed M works for stable sizes; real tables grow, so overflow chains balloon (O(N) degradation) — dynamic schemes exist precisely for this.
- **Alternative: directory-less growth.** Full rehash on every size change is O(N) and blocks the table; extendible (directory doubling) and linear (round-robin splits) amortize growth to O(1).
- **Why don't DBs default to hash?** Because most SQL touches order (ORDER BY, BETWEEN, joins by range, group adjacency); the B+ tree covers both point and range. Hash is the performance specialization when the workload is exact-match.

## 5. Intuition
A hash index is the **coat-check room**: you hand over your ticket (key), the attendant computes your number (hash) and returns your coat (record) — **one trip, no searching**. A B+ tree is the *alphabetized directory*: you flip to the letter, then page, then line — fast but several steps. The coat room wins when you always come with a ticket (exact key) and never ask "all blue coats" (no ranges). Static hashing = a fixed-number-of-hooks coat room: fine until the gala arrives and 3 coats share a hook (overflow chain → you now sift through a pile). Extendible/linear hashing = a room that *adds hooks one section at a time* when a section gets crowded, so the crowd never grows faster than the hooks. The price: coats are stored in arrival order, not color order — you can't find "all blue coats," and "coats 10–20" means checking every hook.

## 6. Real-World Analogy
A **hospital's medical-record filing system**. The reception desk keeps a **hash** of patient number → locker number: hand over a patient ID, the clerk computes the locker, retrieves the folder in one trip. New patients get lockers by hashing their ID — when one locker overflows with files, the clerk adds a second locker just for that range (extendible split) or adds a new locker at the end and re-distributes (linear). But the system is useless for "all files from last week" (no date order) or "files 1000–2000" (no sequencing) — for those you'd want folders sorted by date (B+ tree). The hospital chose the hash because 95% of requests are "patient #X's file" — a pure exact-match workload, exactly when hash indexing shines.

## 7. Formal Definition
(Silberschatz Ch. 14.6; Elmasri & Navathe Ch. 18.7; Cormen Ch. 11 for hash functions.)
- **Hash function**: h: K → {0,…,M−1}; bucket address for key K.
- **Static hashing**: M fixed; bucket = h(K) mod M; overflow pages chain beyond bucket capacity.
- **Extendible hashing**: directory of 2^d pointers; global depth d, local depth d_i per bucket; split a full bucket (rehash by d+1 bits) and double the directory when d exceeds local depths.
- **Linear hashing**: M grows incrementally (round-robin splits) with overflow chains handled by split pointers; no directory.
- **Hash index**: stores (key → RID/PK) in buckets for exact-match lookup; does not preserve order.
- **Expected costs**: point lookup O(1) expected (1–2 page reads); range O(N); insert/delete O(1) amortized; rehash O(N) amortized O(1).

## 8. Example
Keys with h(K) = K mod 4, M = 4 buckets:
```
Bucket 0: [0, 4, 8]    Bucket 1: [1, 5]
Bucket 2: [2, 6, 10]   Bucket 3: [3, 7]
```
- Lookup 10: h(10)=2 → read bucket 2 → scan 3 entries → found. **1 page read**.
- Range 2..7: must scan all 4 buckets — no ordering.
- Insert 12: h=0 → append to bucket 0 (may overflow → chain).
- **Extendible fix on bucket 2 overflow** (say capacity 3): split bucket 2 by bit: h bit-1: keys with K mod 8 ∈ {2,6} → bucket 2a, {10,...} → 2b; directory doubles (2^2 → 2^3 pointers); lookups still ≤ 2 reads.
- **Compare B+**: point = 3–4 reads; range = cheap. Hash point = 1–2; range = impossible. The exact trade.

## 9. Internal Working
1. **Static**: allocate M bucket pages; h(K) mod M routes; overflow pages chained; periodic rehash (M → new M) when load factor gets high — an O(N) stop-the-world op.
2. **Extendible**: directory (index by first d bits); each bucket has local depth; on overflow, if local < global, split bucket in two (d+1 bits) and point directory entries accordingly; if local == global, double directory first. Reads: directory page + bucket page (≈ 2 reads).
3. **Linear**: a *split pointer* advances one bucket per insert once load exceeds a threshold; new buckets appended; each key rehashed lazily as its bucket is passed; amortized O(1), no blocking rehash.
4. **Postgres hash index**: persistent, WAL-logged (since PG10), crash-safe; leaf buckets = hash page + overflow pages; exact equality (`=`) operator only.
5. **Optimizer**: hash indexes appear in plans as `Bitmap Index Scan`/`Index Scan` for `=` predicates; cardinality estimates still come from stats.

## 10. Time Complexity
- **Point lookup**: O(1) expected (≈1–2 page reads; worst O(N) with pathological collisions).
- **Insert/Delete**: O(1) expected (bucket append/delete; amortized with dynamic growth).
- **Range query**: O(N) — unsupported in practice (must scan all buckets).
- **Rehash (static)**: O(N) blocking; **extendible/linear**: amortized O(1) per operation.
- **Space**: buckets ≥ ~70–80% full typical; directory overhead small for extendible.

## 11. Advantages
- **Fastest exact lookups**: 1–2 page reads — beats B+ tree's 3–4.
- **Fast equality joins**: no ordering needed; hash join buckets directly.
- **Simple writes**: append to a bucket; amortized O(1).
- **Graceful growth**: extendible/linear hashing avoid full rehashes.
- **Great for key-value and PK workloads**: the pattern under DynamoDB/Cassandra partition keys.

## 12. Disadvantages
- **No order**: ranges, ORDER BY, GROUP BY adjacency, prefix LIKE all impossible.
- **Collision degradation**: bad hash or overloaded buckets → chains → O(N) lookups.
- **Rehash complexity**: static rehash is blocking; dynamic schemes add directory/split-pointer machinery.
- **Space overhead**: sparse buckets waste pages; directory (extendible) is extra.
- **Less general**: SQL optimizers rarely choose hash for non-exact predicates; most DBs prefer B+ by default.

## 13. Interview Questions
1. **Q: What is a hash index?** A: A structure mapping keys to buckets via a hash function, storing (key → locator); exact-match lookups in O(1) expected.
2. **Q: When is a hash index the right choice?** A: Pure exact-match point lookups / equality joins with no ordering needs — e.g., key-value and PK get paths.
3. **Q: When is it wrong?** A: Any range/order work: BETWEEN, ORDER BY, GROUP BY adjacency, prefix LIKE — the hash destroys order.
4. **Q: Static vs dynamic hashing?** A: Static = fixed bucket count (overflow chains degrade); dynamic = grows incrementally (extendible: directory doubling + bucket splits; linear: round-robin splits).
5. **Q: What is extendible hashing?** A: A directory of 2^d pointers; on overflow, split one bucket (rehash with d+1 bits), doubling the directory when needed; ≈2 page reads per lookup.
6. **Q: What is linear hashing?** A: Grows bucket count one at a time (split pointer) without a directory; amortized O(1), no blocking rehash.
7. **Q (tricky): hash vs B+ for `WHERE id = 42`?** A: Hash: ~1–2 reads, no order overhead. B+: ~3–4 reads but also serves ranges. For a pure point workload, hash wins; DBs still default to B+ for generality.
8. **Q (scenario): key-value store, "get by key" only.** A: Hash indexing/partitioning — DynamoDB-style partition keys; O(1) access, no range requirement.
9. **Q: What happens when a bucket overflows (static)?** A: Overflow pages chain off the bucket; lookups in that bucket degrade toward O(N); fix = rehash to more buckets.
10. **Q: Does PostgreSQL have a hash index?** A: Yes — `USING hash`, crash-safe and WAL-logged since PG10, for `=` predicates; historically B+ was preferred, but hash is a valid exact-match option.
11. **Q (production): why is InnoDB using B+ not hash?** A: InnoDB clusters by PK and needs ranges/ORDER BY for its workload; MySQL's MEMORY engine supports hash indexes for exact-match caching tables.
12. **Q: What is a hash join?** A: Both inputs bucketed by join key hash, matched within buckets — O(N+M) expected, no sorting; the exact-match cousin of hash indexing.
13. **Q (hard): why can't a hash index answer ORDER BY?** A: Buckets have no order; keys are scattered by h(K) — collecting them sorted means hashing every bucket and sorting, i.e., no better than a scan.
14. **Q: What are the worst-case implications of a poor hash function?** A: All keys → one bucket → O(N) lookups (chain), and even dynamic hashing can't fix a biased function; DBs use strong mixers (Postgres uses lookup-based hashing).
15. **Q: How does hash partitioning relate to hash indexing?** A: Partitioning routes rows to partitions by hash (data placement); a hash index routes lookups to buckets (search structure) — same hashing idea at two levels.
16. **Q (tricky): can hash indexes be covering?** A: Yes — a hash index can store extra columns in buckets and serve exact-match queries without the table (like a covering B+ index), though DBs rarely expose this.
17. **Q: What does "mod M" do in bucket addressing?** A: Reduces the hash to the bucket range; M = number of buckets; collisions (same bucket) are handled by scan/chaining.
18. **Q: Why is rehash O(N) and why do dynamic schemes avoid it?** A: Rehash re-hashes every key to new buckets — O(N). Extendible splits one bucket at a time; linear splits incrementally — each insert pays O(1) amortized.
19. **Q (production): DynamoDB/Cassandra — how do they hash?** A: Partition key hashed to a partition node (DynamoDB consistent hashing; Cassandra murmur3 → token range) — the linear/consistent-hash family for distributed exact lookups.
20. **Q: When would you choose hash over B+ for a column?** A: Column used only in equality predicates (`=`, `IN`), high-selectivity, and never in ORDER BY/GROUP BY/ranges — then hash's 1–2 reads beat B+ and ordering is unused.

## 14. Follow-Up Questions
1. **Q: How do you size M for static hashing?** A: Load factor ≈ records/M; target 0.7–0.8 (buckets ~70–80% full) to bound chains; rehash when exceeded.
2. **Q: Consistent hashing?** A: Hashes both keys and nodes on a ring; keys assigned to the next node — minimizes re-hashing when nodes join/leave (DynamoDB, Cassandra, distributed caches).
3. **Q: Can hash indexes be used with NULL?** A: Postgres hash index can store NULL keys (one bucket); equality `IS NULL` may or may not use it — check the plan.
4. **Q: How does hash indexing interact with the buffer pool?** A: Small bucket count + hot keys → buckets cached → lookups become in-memory O(1); the 1–2 read cost is the cold bound.
5. **Q: Hash vs B+ for dedup (UNIQUE)?** A: B+ is the default because uniqueness + range + scan all matter; a hash unique index works but no order support — rare.

## 15. Coding Example
```sql
-- PostgreSQL hash index (exact-match only)
CREATE INDEX idx_orders_user_hash ON orders USING hash (user_id);

EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 42;
--   -> Index Scan using idx_orders_user_hash on orders  (Bitmap/Index, = predicate)

-- PostgreSQL dynamic hashing is automatic: buckets grow on demand,
-- no sizing knobs (unlike static schemes).

-- MySQL MEMORY engine hash index (exact-match cache table)
CREATE TABLE session_cache (
  session_id CHAR(32) PRIMARY KEY,
  user_id    INT,
  data       BLOB
) ENGINE=MEMORY;
CREATE INDEX idx_sess_hash ON session_cache (user_id) USING HASH;
-- exact lookups by user_id: O(1); no ranges on the hash column.

-- Hashing in partitioning (rows routed by hash, exact-lookup locality):
CREATE TABLE events (id BIGINT, payload JSONB)
  PARTITION BY HASH (id);            -- buckets = partitions
```
```python
import hashlib
def bucket_for(key, m):
    return int(hashlib.sha256(key.encode()).hexdigest(), 16) % m

def static_hash_search(key, m, buckets):
    b = bucket_for(key, m)
    return f"read bucket {b}: {buckets[b]}"   # ~1 page read, scan bucket
```

## 16. Industry Usage
- **PostgreSQL**: `USING hash` access method — a real dynamic hash index, WAL-logged and crash-safe, used for exact-match hot paths.
- **MySQL**: MEMORY engine hash indexes for fast in-memory exact lookups; InnoDB remains B+.
- **DynamoDB / Cassandra**: partition-key hashing (consistent/murmur3) for distributed O(1) primary access — hash indexing at cluster scale.
- **Hash joins everywhere**: PostgreSQL/MySQL use hash joins for equality joins without ordering — the query-level use of hashing.
- **Partitioned tables**: hash partitioning (Postgres/Oracle) spreads writes evenly and localizes exact-key access.

## 17. References
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 14.6 (Hash-Based Indexing).
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 18.7.
- Cormen, Leiserson, Rivest & Stein, *Introduction to Algorithms*, 3rd ed., Ch. 11 (Hash Tables).
- Fagin et al., "Extendible Hashing — A Fast Access Method for Dynamic Files", TODS 1979.
- Litwin, "Linear Hashing: A New Tool for File and Table Addressing", 1980.
- PostgreSQL docs: Index Types (hash); MySQL docs: MEMORY Storage Engine.

## 18. Cheat Sheet
- Hash index: (key → locator) in buckets; exact lookup O(1) expected (~1–2 reads).
- NO ranges / ORDER BY / prefix — order destroyed.
- Static: fixed M; overflow chains degrade → rehash O(N).
- Extendible: directory 2^d; split one bucket; ≈2 reads.
- Linear: round-robin splits; no directory; amortized O(1).
- Use for: pure `=` / IN / key-value / equality joins.
- Postgres `USING hash`; MySQL MEMORY; DynamoDB/Cassandra partition keys.
- Hash join = hashing at query level (no sort).

## 19. Quiz
1. Hash index point lookup: a) O(log N) b) O(1) expected c) O(N) d) O(N²) → **b**
2. Hash index range query: a) O(log N) b) fast c) unsupported O(N) d) O(1) → **c**
3. Static hashing's growth problem: a) too many buckets b) overflow chains c) ordering d) none → **b**
4. Extendible hashing doubles: a) buckets only b) a directory c) page size d) keys → **b**
5. Linear hashing splits: a) all at once b) round-robin c) never d) by depth → **b**
6. Which workload fits hash indexing: a) BETWEEN b) exact PK get c) ORDER BY d) LIKE → **b**
7. Postgres hash index: a) not crash-safe b) WAL-logged since PG10 c) default d) no `=` → **b**
8. Hash join avoids: a) hashing b) sorting c) indexes d) memory → **b**
9. A biased hash function causes: a) taller tree b) collisions → O(N) chains c) more buckets d) nothing → **b**
10. DynamoDB/Cassandra use hashing for: a) ranges b) distributed exact access c) ORDER BY d) bitmaps → **b**

## 20. Flashcards
- **Q: Hash index lookup cost?** → **A:** O(1) expected (~1–2 page reads).
- **Q: What can't hash do?** → **A:** Ranges, ORDER BY, prefix scans.
- **Q: Static vs dynamic?** → **A:** Fixed M vs incremental growth (extendible/linear).
- **Q: Extendible hashing?** → **A:** Directory doubling + one-bucket splits; ~2 reads.
- **Q: Linear hashing?** → **A:** Round-robin bucket splits, no directory, amortized O(1).
- **Q: When use hash?** → **A:** Pure equality/key-value/exact-match workloads.
- **Q: Postgres?** → **A:** `USING hash`, crash-safe since PG10.
- **Q: Hash join?** → **A:** Buckets both inputs, matches within buckets, no sort.

## 21. Revision
A **hash index** gives **O(1) expected** exact-match lookups (~1–2 page reads) by mapping keys to buckets — but it **cannot** do ranges, ORDER BY, or prefix scans, so it's the specialization for pure equality/key-value workloads while B+ trees stay the general default. **Static hashing** (fixed M) degrades via overflow chains and needs O(N) rehash; **extendible** hashing doubles a directory and splits one bucket at a time (~2 reads); **linear** hashing grows buckets round-robin (amortized O(1), no blocking rehash). Where it's used: PostgreSQL `USING hash` (crash-safe since PG10), MySQL MEMORY engine, and **DynamoDB/Cassandra partition-key hashing** for distributed exact access; **hash joins** are the query-level cousin (no sort needed). Interview script: state O(1) exact + "no ranges" in the same breath; contrast static vs extendible vs linear; and name where production actually uses it.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a hash index / when to use?" | 2 / 13 Q1–Q3 |
| "Static vs dynamic hashing?" | 13 Q4 |
| "Extendible / linear hashing?" | 13 Q5–Q6, Q18 |
| "Hash vs B+ for point lookups?" | 13 Q7 |
| "Overflow behavior?" | 13 Q9, Q14 |
| "Postgres / MySQL support?" | 13 Q10–Q11 |
| "Hash joins?" | 13 Q12 |
| "DynamoDB/Cassandra hashing?" | 13 Q19 |
