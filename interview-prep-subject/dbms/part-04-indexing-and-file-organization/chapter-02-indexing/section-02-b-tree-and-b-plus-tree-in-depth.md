# B-tree and B+ tree in Depth

> **TL;DR**: B-trees are self-balancing, shallow, wide trees whose height is O(log_f N) with fan-out f in the hundreds — so a billion-row table is reached in **3–4 page reads**. The **B+ tree** (chosen by every major RDBMS) keeps all records in ordered, doubly-linked leaves with keys duplicated in the internal nodes, giving fast range scans and better page utilization than the B-tree. Insert/delete use splits and merges to stay balanced.

## 1. Why Does This Exist?
A sorted file gives O(log N) search but O(N) insert. A binary tree gives O(log N) for both — but nodes live on *disk*, and each node visit is a *page read*, thousands of times slower than a CPU operation. A binary tree of 1 billion keys has height ~30: **30 disk reads per lookup** — too slow. The B-tree exists to make the tree *wide*, not tall: each node holds hundreds of keys (as many as fit in one page), so height collapses to ~3–4 regardless of table size. It also keeps itself **balanced automatically** (all leaves at the same depth) via splits and merges, so worst-case behavior stays O(log_f N). The B+ tree is the refinement DBs actually use: only leaves hold data, leaves are linked for range scans, and internal nodes store *copies* of keys — packing more keys per page (higher fan-out) and making every operation faster. This is why "an index seek ≈ 3 page reads" is the mental model of every DBA.

## 2. How Does It Work?
- **Structure**: an M-way balanced tree. Each node holds up to M−1 keys and M child pointers; a node with k keys has k+1 children, and keys are ordered. All leaves are at the *same depth*.
- **B-tree**: records stored in *both* internal nodes and leaves. **B+ tree**: internal nodes store only keys (for routing); *all* records live in leaves, and leaves are linked left-to-right (and usually back).
- **Fan-out**: number of children per node ≈ page size / (key size + pointer size) — typically 100–1000.
- **Search**: start at root, at each node binary-search the keys to pick the child; descend. In B+ tree, descend to the leaf, then scan the leaf (or follow links for ranges).
- **Insert**: search down to the leaf; insert sorted; if the node overflows (> M−1 keys), **split** into two (promote the middle key in B-tree; in B+ tree, copy it up to the parent); recurse; if the root splits, height grows by one.
- **Delete**: remove; if a node underflows (< ⌈M/2⌉−1 keys), **merge** with a sibling (or borrow/redistribute); if the root empties, height shrinks.

## 3. When Is It Used?
- **Default index structure of every major RDBMS** (Postgres, MySQL/InnoDB, Oracle, SQL Server): for PK, unique, and most secondary indexes.
- **Ordered access**: `WHERE id = ...`, `BETWEEN`, `ORDER BY`, `GROUP BY`, prefix `LIKE 'abc%'`, and join keys.
- **Clustered tables** (InnoDB): the table itself is a B+ tree.
- **Filesystems & key-value stores** (Btrfs, RocksDB LSM emulations, MongoDB indexes): the same tree concept.
- **NOT for**: pure exact-match with no ordering need (hash wins), or low-selectivity queries (scan wins).

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: binary search tree.** Height ~log₂ N ≈ 30 for 1e9 → 30 disk reads; also needs explicit balancing (AVL/red-black) and has no page-oriented fan-out. B-tree's wide nodes cut height by ~10×.
- **Alternative: sorted array + binary search.** Search O(log N) but insert O(N) — deadly for OLTP. B-tree absorbs inserts with splits (O(log N)).
- **Alternative: B-tree (data in internal nodes).** Works, but (1) range scans need parent hops (leaves aren't linked), (2) internal nodes are fatter (holding data) → lower fan-out → taller tree. The **B+ tree** fixes both: linked leaves for ranges, key-only internal nodes for maximal fan-out.
- **Alternative: hash index.** O(1) exact but no ordering — ranges/ORDER BY impossible. B+ is the general default; hash is the specialization.
- **Why not an even wider tree?** Fan-out is bounded by page size; wider would need larger pages (worse for small lookups) — the engineering sweet spot is one page per node.

## 5. Intuition
A B+ tree is a **telephone directory built like a subway map with an express line**. The *internal nodes* are the station names (keys) used only to route: "go to this platform." The *leaves* are the actual platform list of all records, in order, and each platform links to the next — so walking "all names from A–Z" is one continuous stroll through linked leaves, never going back upstairs. The tree is *wide*: one platform signboard holds hundreds of names (fan-out), so even a city with a billion residents needs only ~3 floors of signs to reach any resident — and because the tree rebalances itself (splitting overflowing signboards, merging sparse ones), all platforms stay on the same floor. That's the whole design: wide, shallow, balanced, and the range-walk lives at the bottom.

## 6. Real-World Analogy
A **multi-story archive with index cards**. Each card (node) fits ~500 entries (fan-out). The top card says "A–M / N–Z" (internal node, keys only); next level refines; the bottom-level cards are the *actual files*, and each card has a note pointing to the next card in alphabetical order (leaf links). Finding "Smith" = read top card (1 read), second card (1 read), bottom card (1 read) = **3 card reads** for millions of records — vs a card-per-record system (binary search) needing 20+ card reads. Filing a new "Roberts" may split a bottom card in two, updating the parent pointers (the split). The archive's genius: the same 3-read path works whether there are 1,000 or 1,000,000,000 files, because only the fan-out grows. That's the B+ tree.

## 7. Formal Definition
(Knuth; Cormen CLRS Ch. 18; Silberschatz Ch. 14.4; Elmasri & Navathe Ch. 18.5.)
- **B-tree of order M**: every node has at most M children and at least ⌈M/2⌉ children (root excepted); a node with k children holds k−1 keys; all leaves at the same depth.
- **B+ tree**: all keys and records in leaves; internal nodes contain only routing keys (duplicates of leaf keys); leaves form an ordered, linked list.
- **Height**: O(log_f N) where f = fan-out ≈ page_size / entry_size.
- **Invariants**: every leaf at depth d; node occupancy between ⌈M/2⌉−1 and M−1 keys (50% minimum fill).
- **Properties for DBs**: point search = height page reads; range scan = height + result pages (via leaf links); inserts/deletes = O(height) splits/merges.

## 8. Example
Insert into a B+ tree of order M=4 (max 3 keys/node), keys: 1, 2, 3, 4.
```
Insert 1,2,3  ->  leaf [1,2,3]
Insert 4      ->  leaf [1,2,3] + 4 overflows -> split: [1,2] | [3,4], promote 3
                internal [3]
                    /        \
               [1,2]        [3,4]
Insert 5      ->  [3,4]+5 overflows -> split [3,4] -> [3] | [4,5], promote 4
                internal [3,4]
                   /   |   \
               [1,2] [3] [4,5]
```
Search 5: root [3,4] → right child [4,5] → found. All leaves depth 1. Insert 6,7,8,9 pushes splits further; height grows only when the root splits.

**Height vs N** (fan-out f = 100): N=10⁶ → height ≈ log₁₀₀(10⁶) ≈ 3; N=10¹² → height ≈ 6. Compare f=2 (binary): 10¹² → height 40.

## 9. Internal Working
1. **Page-sized nodes**: each node = one disk page (typically 8 KB default); a node visit = one page read. Fan-out = floor(page_size / (key + child_ptr)).
2. **Search**: root → per-node binary search → child pointer; descend; in B+ tree stop at the leaf; range = leaf scan + next-leaf links.
3. **Insert (B+ tree)**: find leaf; insert in order; if > M−1 keys, split (right half to new sibling; middle key *copied* to parent); parent may split recursively; root split creates a new root (height +1).
4. **Delete**: find leaf; remove; if < ⌈M/2⌉−1 keys: borrow from sibling (redistribute) or merge with sibling (parent loses a key; may cascade; root shrink → height −1).
5. **B-tree vs B+**: B-tree promotes the actual key (data moves up); B+ tree copies keys up and keeps data in leaves — leaves must link for ranges.
6. **Optimizer stats**: `pg_statistic`/InnoDB stats store histogram + index cardinality to estimate result sizes and choose index vs scan.

## 10. Time Complexity
- **Point lookup**: O(log_f N) page reads ≈ height (3–4 for 1e9).
- **Range [k1,k2]**: O(log_f N + k) — height descent + k result pages via leaf links.
- **Insert/Delete**: O(log_f N) amortized (splits/merges along one path).
- **Space**: nodes ≥ 50% full on average (~69% typical fill) → index size ≈ 1.5× data keys.
- **Build (bulk load)**: O(N) by filling leaves left-to-right.

## 11. Advantages
- **Tiny height**: ~3–4 page reads for any table — effectively constant in practice.
- **Balanced automatically**: splits/merges keep all leaves at equal depth; no rebalancing passes like AVL rotations.
- **Ordered + ranged**: leaves ordered + linked → ORDER BY, BETWEEN, GROUP BY adjacency, prefix LIKE all fast.
- **High fan-out**: B+ key-only internal nodes maximize keys/page → shortest tree.
- **Good page locality**: leaves packed; sequential scans read contiguous pages.
- **Proven at scale**: 50+ years as the RDBMS default.

## 12. Disadvantages
- **Write amplification**: each insert touches path nodes + possibly splits (vs heap append O(1)).
- **Cache/pessimistic fill**: ~69% average fill wastes ~30% of index pages.
- **Random-key inserts** (UUID): split/relocation + cache churn in clustered tables (InnoDB).
- **Not exact-match optimal**: hash beats B+ for pure point lookups.
- **Complexity**: split/merge invariants are the trickiest part to get right (vs simpler structures).

## 13. Interview Questions
1. **Q: Why B-tree instead of binary search tree for DBs?** A: BST height = log₂ N ≈ 30 for 1e9 (30 page reads). B-tree's page-sized nodes give fan-out ~100–1000 → height 3–4 page reads.
2. **Q: What is fan-out?** A: Max children per node ≈ page size / (key + pointer). Drives height: height = log_f N.
3. **Q: B-tree vs B+ tree?** A: B+ keeps all data in leaves (internal nodes = keys only), leaves are linked. Higher fan-out (shorter), and ranges scan linked leaves without parent hops.
4. **Q: Why do DBs pick B+ over B?** A: (1) range scans via leaf links, (2) higher fan-out (key-only internals → shorter tree), (3) leaves packed for sequential IO.
5. **Q (tricky): height of a B+ tree with 1e9 keys, fan-out 500?** A: height ≈ log₅₀₀(1e9) ≈ 3.3 → 4 levels (3 internal + leaf). "Index seek = 3–4 page reads."
6. **Q: What happens on insert overflow?** A: Split the node in two, copy the middle key to the parent; parent may split recursively; if root splits, height +1.
7. **Q: What happens on delete underflow?** A: Redistribute (borrow) from a sibling or merge two nodes; parent key removed; cascades; root shrink → height −1.
8. **Q (scenario): table with random UUID PK in InnoDB.** A: Random inserts split leaves at random positions + cache churn; use auto-increment or UUIDv7 (time-ordered) to keep inserts at the right edge.
9. **Q: Why does ORDER BY id come free with a B+ index?** A: Leaves are already ordered and linked; the planner reads leaves in order (no sort step).
10. **Q: Can a B+ index satisfy GROUP BY?** A: Often — grouping by an indexed prefix reads adjacent runs of equal keys, avoiding a sort/hash aggregate.
11. **Q (hard): what's the minimum fill, and why 50%?** A: Every non-root node keeps ≥ ⌈M/2⌉ children — guarantees splits/merges stay balanced and space usage bounded (≈69% typical).
12. **Q: B+ vs hash for point lookups?** A: Hash is O(1) expected but no order; B+ is O(log_f N) ≈ 3–4 reads but supports ranges — DBs default to B+.
13. **Q: What does "covering" mean for a B+ index?** A: The index's leaf entries contain all columns a query needs → index-only scan, never open the table.
14. **Q (production): why would EXPLAIN prefer a scan over your B+ index?** A: Low selectivity (estimates say scan cheaper), stale stats, functions on the column, or a range predicate spanning most rows.
15. **Q: How does bulk loading build a B+ tree fast?** A: Sort keys, fill leaves left-to-right, then build internal levels upward (O(N) instead of N individual inserts).
16. **Q (tricky): what does a split "promote" vs "copy" mean?** A: B-tree *moves* the actual record up (data in internal nodes). B+ tree *copies* the key up (routing only) and keeps the record in the leaf — that's why B+ leaves hold everything.
17. **Q: What is the effect of page size on fan-out?** A: Bigger pages → more keys per node → higher fan-out → shorter tree; but wasted reads on small lookups. 4–16 KB pages are the trade-off point.
18. **Q: How do range scans use leaf links?** A: Find the first matching leaf (descent), then walk the linked list of leaves reading contiguous results — no repeated root descents.
19. **Q (scenario): index on (a,b); does it help ORDER BY b?** A: No — ORDER BY b alone can't use (a,b) (leftmost prefix); ORDER BY a, b can. A separate index on b would help.
20. **Q: What makes B+ tree "self-balancing"?** A: All inserts/deletes run the same split/merge invariants along the path, so every leaf stays at the same depth — no external rebalancing step ever runs.

## 14. Follow-Up Questions
1. **Q: How do LSM trees compare to B+?** A: LSM (RocksDB, LevelDB, Cassandra) writes to in-memory memtables and flushes sorted runs, merging in background — faster writes, slower point reads; B+ is better for reads, worse for write-heavy workloads.
2. **Q: What is a "blind write" in a B+ tree?** A: Writing a value without first reading (upsert) — possible for inserts; DBs do it to save IO.
3. **Q: How do buffer-pool caches interact with the tree?** A: Root + upper levels stay cached (hot), so in steady state a lookup is ~1 leaf read; the "3–4 reads" is the cold-cache bound.
4. **Q: Why is 69% average fill typical?** A: Splits happen at 100% but leaves can shrink to 50% — average occupancy ≈ (100%+50%)/2 = 75%, slightly less with variance (≈69%).
5. **Q: Does deleting many rows shrink the tree?** A: Only when underflow merges cascade up; the tree is dense (values removed from leaves), but page count shrinks lazily via merges — not immediately per delete.

## 15. Coding Example
```sql
-- B+ trees are the engine's business; you just create indexes:
CREATE TABLE orders (id BIGINT, user_id BIGINT, amount NUMERIC);

-- PK -> clustered B+ tree (InnoDB) / unique index (Postgres)
ALTER TABLE orders ADD PRIMARY KEY (id);

-- secondary B+ index on the FK (join + filter)
CREATE INDEX idx_orders_user ON orders(user_id);

-- composite B+ index tuned for the hot query
CREATE INDEX idx_orders_user_amount ON orders(user_id, amount);

-- confirm the planner descends the tree (Index Scan, not Seq Scan)
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 42 AND amount > 100;
--   -> Index Scan using idx_orders_user_amount

-- index-only scan example (covering)
CREATE INDEX idx_orders_user_amount_cover ON orders(user_id, amount);
EXPLAIN ANALYZE SELECT user_id, amount FROM orders WHERE user_id = 42;
--   -> Index Only Scan (no table access)
```
```python
def b_plus_height(n, fan_out):
    import math
    return math.ceil(math.log(n, fan_out)) if n > 1 else 1

def pages_read(n, fan_out):
    return b_plus_height(n, fan_out)          # point lookup = one path

# For 1e9 keys, fan_out 500:
print(pages_read(10**9, 500))                  # 4 page reads
```

## 16. Industry Usage
- **All major RDBMS**: Postgres (`btree` access method), MySQL/InnoDB (clustered PK = B+), Oracle, SQL Server — the default index structure.
- **Index-only scans & covering indexes**: Postgres and InnoDB exploit B+ leaves holding all needed columns to skip the table entirely.
- **Filesystems & storage**: Btrfs, ext4, and MongoDB's default index use B-tree/B+ families; LSM-based engines (RocksDB, Cassandra) are the write-heavy alternative.
- **Range analytics**: time-series and reporting queries rely on B+ ordering for `BETWEEN`/`ORDER BY`/prefix scans over big tables.
- **Schema tuning**: DBAs measure index heights and fill factors (e.g., `FILLFACTOR` in Postgres) — the B+ internals directly influence production config.

## 17. References
- Cormen, Leiserson, Rivest & Stein, *Introduction to Algorithms*, 3rd ed., Ch. 18 (B-trees).
- Knuth, *The Art of Computer Programming*, Vol. 3, Sec. 6.2.4 (B-trees).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 14.4.
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 18.5.
- Bayer & McCreight, "Organization and Maintenance of Large Ordered Indexes", 1972 (original B-tree paper).
- PostgreSQL docs: Index Types (btree), FILLFACTOR.

## 18. Cheat Sheet
- B/B+ tree: wide, balanced, shallow; height = log_f N.
- Fan-out f ≈ page_size/(key+ptr) ≈ 100–1000 → height 3–4 for 1e9.
- B+ tree: data only in leaves; internal = routing keys; leaves linked.
- DBs choose B+ for: leaf-linked ranges, higher fan-out, sequential leaves.
- Insert → split (copy middle key up); Delete → borrow/merge.
- Order invariants keep every leaf at the same depth.
- "Index seek = 3 page reads"; covering ⇒ index-only scan.
- Random keys (UUID) → splits + cache churn; prefer ordered keys.

## 19. Quiz
1. Height of B+ tree with N keys, fan-out f: a) log₂ N b) log_f N c) N d) f → **b**
2. 1e9 keys, fan-out 500 ≈ height: a) 30 b) 4 c) 100 d) 10 → **b**
3. B+ vs B: data lives in a) internal nodes b) leaves c) both d) neither → **b**
4. Range scans use: a) parent hops b) leaf links c) root repeat d) hashing → **b**
5. On insert overflow, a node: a) merges b) splits c) rotates d) rebuilds → **b**
6. On underflow, a node: a) splits b) borrows/merges c) shrinks root only d) drops → **b**
7. B+ internal nodes hold: a) records b) keys only c) hashes d) bitmaps → **b**
8. BST of 1e9 keys ≈ height: a) 4 b) 30 c) 100 d) 10 → **b**
9. Fill factor of a B+ node is at least: a) 100% b) 50% c) 25% d) 0% → **b**
10. Random UUID PKs in InnoDB cause: a) left-edge inserts b) random splits/cache churn c) no effect d) merge storms → **b**

## 20. Flashcards
- **Q: B+ tree height?** → **A:** log_f N ≈ 3–4 for 1e9 (fan-out ~500).
- **Q: Why B+ over B-tree?** → **A:** Leaf links for ranges + higher fan-out (key-only internals).
- **Q: Insert overflow?** → **A:** Split node, copy middle key up; root split → height +1.
- **Q: Delete underflow?** → **A:** Borrow or merge with sibling; root shrink → height −1.
- **Q: What is fan-out?** → **A:** Children per node ≈ page_size/(key+ptr).
- **Q: Point lookup cost?** → **A:** Height page reads (one root-to-leaf path).
- **Q: Range lookup cost?** → **A:** Height + k result pages via leaf links.
- **Q: B+ tree in the DB?** → **A:** Default index; InnoDB clustered PK is a B+ tree.

## 21. Revision
B-trees solve **disk height**: page-sized nodes give fan-out ~100–1000, so height = log_f N ≈ **3–4 page reads** for billions of rows (vs ~30 for binary). The **B+ tree** refines it — all records in **leaves**, internal nodes hold **keys only**, leaves are **linked** — giving (1) cheap range scans along the leaf chain, (2) higher fan-out/shorter tree, (3) packed sequential leaves: the three reasons every RDBMS defaults to B+. Invariants: nodes keep between ⌈M/2⌉−1 and M−1 keys; **insert** overflows split (middle key copied up), root split grows height; **delete** underflows borrow/merge, root shrink drops height. Remember the working numbers: point = height reads, range = height + k, and "seek ≈ 3 page reads" is the DBA's mental model. Watch random keys (UUID) causing splits + cache churn, and use **covering** indexes for index-only scans.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Why B-tree not BST?" | 1 / 13 Q1 |
| "What is fan-out / height?" | 13 Q2, Q5 |
| "B vs B+ and why B+?" | 13 Q3–Q4 |
| "Split / merge mechanics?" | 13 Q6–Q7 |
| "UUID random-key problem?" | 13 Q8 |
| "Range scans / leaf links?" | 13 Q9, Q18 |
| "Covering / index-only scans?" | 13 Q13 |
| "When scan beats the index?" | 13 Q14 |
