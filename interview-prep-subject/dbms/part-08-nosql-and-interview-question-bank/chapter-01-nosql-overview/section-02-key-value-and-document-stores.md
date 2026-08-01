# Key-Value & Document Stores

> **TL;DR**: Key-value stores (Redis, DynamoDB, Memcached, etcd) give O(1) get/put by an opaque key with nothing else — the right tool for caches, sessions, and counters; document stores (MongoDB, CouchDB) keep self-contained JSON/BSON objects with flexible schema and indexed field queries but no general joins — the right tool for content, catalogs, and user profiles.

## 1. Why Does This Exist?
Both families exist because the most common web access pattern is **"give me this one thing by this identifier, fast, at any scale"** — a session, a profile, a product, a shopping cart. A relational engine answers that with a point query (fine) but couples it to joins, transactions, and schema rigidity the app doesn't use, and — more importantly — its write path scales up (single writer) rather than out. Key-value stores strip everything to an O(1) lookup across a partitioned cluster. Document stores add the next requirement: the value is a *structured object* with nested fields you want to query and index (profiles with addresses, products with specs) — but you still want per-object reads at scale and the freedom to evolve the shape without migrations. Together they cover "data you fetch by id, at web scale."

## 2. How Does It Work?
**Key-value**: an API of `GET(key)`, `SET(key, value)`, `DELETE(key)` (+ TTL). Value is opaque to the store (Redis actually has typed values: strings, hashes, lists, sets, sorted sets, streams — enabling counters, leaderboards, pub/sub; DynamoDB has typed *items* with attributes and secondary indexes). Partitioning via consistent hashing; replication configurable; TTL/eviction for caches.
**Document**: values are JSON/BSON documents; the store indexes chosen fields (including nested/array fields) so `find` on any indexed field is fast; queries support equality, range, and an aggregation pipeline (`$match`, `$group`, `$lookup` for a *limited* join). Sharding by a shard key distributes documents; replica sets provide availability/durability. Both favor reads-by-key with denormalized data (embed related data in the document) rather than normalized joins.

## 3. When Is It Used?
**Key-value**:
- Caching layer (Redis/Memcached in front of relational DBs — the #1 use).
- Session storage (DynamoDB TTL sessions, Redis `SETEX`).
- Rate limiting / counters / leaderboards (Redis `INCR`, sorted sets).
- Distributed locks, queues (Redis `SETNX`, streams; etcd for coordination/config).
- Feature flags, config (etcd/Redis).
**Document**:
- Content/CMS, product catalogs (variable specs per product).
- User profiles with nested structures; activity feeds; event/cart data.
- Rapid prototyping where schema evolves weekly.
- IoT/telemetry with heterogeneous readings.
- Interviews: "design a cache", "why Redis vs DynamoDB", "document vs relational modeling", "how to model a one-to-many in Mongo".

## 4. Why Wasn't Another Approach Chosen?
- *Relational for caching/sessions*: sessions/caches are ephemeral, key-driven, high-write — relational gives ACID overhead and single-writer bottlenecks for no benefit; TTL/eviction is native to KV, awkward in SQL.
- *Document store only (no KV)*: documents are heavier (serialization, indexes); for pure byte-blob caching a KV is cheaper and faster. They solve adjacent problems; hence both exist.
- *KV with rigid schema (treating KV as a poor-man's SQL)*: loses the ability to query by fields — that's what document indexes give. KV without indexes can't answer "all products with color=black."
- *Normalized relational for document-like data*: profiles/catalogs are naturally one-document aggregates; normalizing them into 3NF tables means join-heavy reads for what is one object read. Document stores mirror the object shape.
- *Single-node document DB*: can't scale writes/availability; the *distributed* partitioning + replication is the point (MongoDB sharding, DynamoDB tables).

## 5. Intuition
A **key-value store is a giant, shared, super-fast locker room**: you rent lockers by number, put anything in, grab it instantly, and set how long it stays (TTL). No questions about what's inside, no cross-referencing lockers — which is exactly why it's instant and scales to millions of lockers. A **document store is a filing cabinet of dossier folders**: each folder (document) is self-contained and can look totally different from the next (flexible schema); you can put tabs on the outside (indexed fields) and find every folder whose tab says "color: black", but you can't automatically weave two folders together (no joins) — if a dossier needs info from another folder, you staple a copy inside (denormalize). Relational is the spreadsheet that cross-references everything and insists every row have the same columns — powerful, but heavier than either for these specific jobs.

## 6. Real-World Analogy
**Key-value = the coat-check at a stadium**: you hand over your coat (SET), get a number (key), retrieve it in seconds (GET), and if nobody claims it in 90 minutes the staff discards it (TTL/eviction). Nobody cares what's in the coat; the operation is number → coat, always fast, and the stadium can run dozens of coat-check booths (partitioning) with a couple of booths holding duplicates for safety (replication). **Document = a hospital's patient charts**: every patient has a chart folder (document) containing anything relevant — some charts have allergy pages, some have MRI reports, none are identical (schemaless). A nurse pulls the *whole folder* by patient id and reads nested sections; the chart is a single self-contained record, and while it may cite another department's records, nobody is *joining* them — they're stapled copies. Trying to run the ER on spreadsheets (relational) would collapse under variance; the folder system scales because each folder stands alone.

## 7. Formal Definition
**Key-value store**: a distributed hash map with API `PUT(k,v)`, `GET(k)`, `DELETE(k)`, optional `TTL`. Values opaque or typed. Consistency: LWW or configurable (DynamoDB eventual/strong reads). Partitioning: consistent hashing. Use case: O(1) access, cache/session/counter patterns.
**Document store**: values are semi-structured documents (JSON/BSON/XML) with an internal schema enforced by the application; storage engine indexes user-declared fields (including nested); query language supports equality/range over indexed fields plus an aggregation pipeline; no general multi-document joins (denormalization or `$lookup` instead). Partitioning: shard key → range/hash; replication: replica set with a primary. Trade: flexible schema + per-document reads at scale, at the cost of relational integrity/join generality.

## 8. Example
**Key-value — Redis cache:**
```
> SETEX product:42 600 '{"name":"laptop","price":999}'
> GET product:42
> INCR views:day:20260802
> ZADD leaderboard 999 user42        -- sorted set
> EXPIRE session:7 3600
```
**Key-value — DynamoDB (typed item + secondary index):**
```
aws dynamodb put-item --table-name sessions \
  --item '{ "user_id": {"S": "u42"}, "ttl": {"N": "1754..."} }'
```
**Document — MongoDB (flexible schema, nested + array queries):**
```js
db.users.insertOne({ _id: 1, name: "Ana",
  emails: ["a@x.com", "work@x.com"],
  address: { city: "Pune", country: "IN" } });
db.users.find({ "address.city": "Pune" });            // nested index
db.users.find({ emails: "a@x.com" });                  // array index
db.products.aggregate([                                // emulated join
  { $match: { category: "electronics" } },
  { $lookup: { from: "reviews", localField: "sku",
               foreignField: "sku", as: "reviews" } }
]);
```

## 9. Internal Working
1. **Key-value core**: hash(key) → owning partition (consistent hashing); local data structure (Redis: in-memory dict + RDB/AOF persistence; DynamoDB: LSM/SSD). TTL via per-key expiry metadata; eviction (Redis LRU/LFU/allkeys-random) for bounded caches.
2. **Replication (KV)**: Redis master-replica (async, failover); DynamoDB multi-AZ synchronous replication of writes to quorum. Read consistency: eventual (default) vs `ConsistentRead` (strong) in DynamoDB.
3. **Document indexing**: MongoDB uses WiredTiger B-tree indexes on fields; a query on indexed field = index probe → doc fetch; compound indexes serve multi-field; `$lookup` pushes a correlated sub-lookup per document (like a nested-loop join, but application-visible).
4. **Sharding (MongoDB)**: shard key → chunks (range or hashed); mongos router routes queries to shards; a query without the shard key = scatter-gather across shards.
5. **Durability (Part 06 ideas)**: Redis AOF (append-only file) + RDB snapshots; MongoDB WiredTiger journal (WAL) — crash recovery replays the journal. Durability ≠ CAP consistency.

## 10. Time Complexity
- KV `GET`/`SET`: **O(1)** amortized + network RTT (LAN sub-ms, WAN 10-100ms). Redis is in-memory → tens of µs; DynamoDB SSD-backed → ms.
- Document indexed lookup: **O(log n)** (B-tree probe) + fetch; without index: collection scan O(n).
- Aggregation `$lookup`: O(per-doc × target) — effectively a nested-loop join; costs rise with volume (denormalize to avoid).
- TTL/eviction: O(1) amortized (lazy deletion + active scans).
- Sharded query with shard key: O(1) partition target; without: O(#shards).

## 11. Advantages
- **Predictable sub-ms latency** for key access; linear write scale via partitioning.
- **Cache semantics native**: TTL, eviction, counters (Redis atomic ops) — features relational engines lack.
- **Flexible schema** (document): no blocking migrations; heterogeneous records coexist.
- **Self-contained objects** (document): one fetch returns the whole aggregate (no join fan-out).
- **Simple operations**: KV has no planner/joins to tune; document stores have a small tuning surface (indexes, shard key).
- **High availability**: replication + partition tolerance (DynamoDB 3-AZ, Redis Sentinel/Cluster).

## 12. Disadvantages
- **No joins / referential integrity**: denormalization and app-side consistency; `$lookup` is a band-aid, not general joins.
- **Eventual consistency**: stale reads, LWW lost updates for concurrent writers without careful versioning.
- **Query limitation**: KV is lookup-only; document range/aggregation is far weaker than SQL (no window functions, arbitrary JOIN, set operations).
- **Application correctness burden**: schema, constraints, multi-document atomicity, and conflict resolution all live in app code.
- **Denormalization drift**: embedded copies of data go stale; update must fan out to every copy.
- **Operational sharp edges**: Redis persistence tuning (AOF/RDB trade-offs), Mongo shard-key selection (a bad shard key = hot partitions or unbalanced data).

## 13. Interview Questions
1. **Q: Difference between Redis and Memcached?** A: Memcached is a pure in-memory cache (eviction, no persistence, strings only, multithreaded). Redis is in-memory *with* persistence (RDB/AOF), rich value types (lists, sets, hashes, sorted sets, streams), TTL, pub/sub, and Lua scripting — a data structure server that's often used *as* a cache plus more.
2. **Q: When is a key-value store the wrong choice?** A: When queries need range/multi-key/join/analytics or transactional integrity across keys — then relational, document (for structure), or analytics stores fit better. KV is for *by-key access only*.
3. **Q: TRICKY: How do you scale a relational DB with a Redis cache?** A: Cache-aside: read from cache, on miss read DB + populate; write-through/back on writes; TTL to bound staleness; handle cache invalidation (delete on write) and stampede (single-flight). The cache absorbs read load; the DB keeps source of truth.
4. **Q: MongoDB vs relational for a catalog?** A: Mongo wins when products have variable/spec-heavy schemas and reads are per-product aggregates; relational wins if you need complex joins, strict integrity, or arbitrary reporting SQL. "Catalog" with stable attributes → relational; heterogenous specs → Mongo.
5. **Q: What is a shard key and why is it important in MongoDB?** A: The field(s) by which documents are distributed across shards. Bad choice (low cardinality, monotonic like auto-increment, or not in most queries) → hot shards or scatter-gather. Design it around the dominant access pattern.
6. **Q: What is DynamoDB's consistency model?** A: Default eventually-consistent reads (cheaper, faster); optional `ConsistentRead` for strong read-after-write within a moment; writes replicate to quorum across AZs. This is the CAP/PACELC trade in practice — strong reads cost latency.
7. **Q: TRICKY: Redis says "cache" but it also has AOF persistence — isn't that a database?** A: Redis is a *data structure server with optional durability*. Persistence (AOF/RDB) makes it survive restarts, but it's still typically a cache/transient layer: bounded memory, eviction, LWW, no multi-key ACID — you'd never treat it as the system of record for critical data. It blurs the line on purpose.
8. **Q: How do you model a one-to-many in a document store?** A: Embed the many as an array when the set is small and read together (addresses, tags); reference by id when the set is large (posts) or independently updated — then denormalize frequently-read fields (author name) and update copies on change.
9. **Q: What is the difference between `$lookup` and a relational join?** A: `$lookup` is a per-document correlated lookup (nested-loop-like), limited to equality on one field, no arbitrary conditions — and it's *visible to the application*. A relational join is optimizer-chosen, arbitrary, and can use hash/merge algorithms.
10. **Q: PR: My MongoDB query is slow. What do you check?** A: (1) `explain()` — is it scanning (`COLLSCAN`) or using an index? (2) Index coverage: create the compound index matching the query + sort. (3) Shard key: is the query routed to one shard or scatter-gather? (4) Data drift: are documents huge/denormalized? (5) Read preference/secondary lag.
11. **Q: TRICKY: Cache stampede (thundering herd) — how do you prevent it?** A: When a hot key expires and many requests miss simultaneously, all hit the DB. Fix: single-flight (one request rebuilds, others wait — Redis lock/`SETNX`), jittered TTLs, background refresh before expiry, or always-refresh popular keys.
12. **Q: What is write-through vs write-back vs write-around caching?** A: Write-through: write cache + DB synchronously (consistent, slower writes). Write-back: write cache first, flush to DB later (fast, risk of loss). Write-around: write DB only, invalidate cache (avoids pollution). Cache-aside is a variant combining read-populate + delete-on-write.
13. **Q: How do you implement a distributed lock with Redis?** A: `SET key uuid NX PX 5000` (atomic set-if-not-exists with TTL); owner releases with a Lua script checking the uuid (don't delete someone else's lock); renewal/watchdog for long operations. Caveats: clock/GC pause → Redlock debate; for correctness-critical locks prefer etcd/ZooKeeper (consensus).
14. **Q: What is a sorted set and why is it powerful?** A: A set with a score; ops: add, `ZRANGE`, `ZREVRANGE`, `ZINCRBY`, rank queries — O(log n) each. Powering leaderboards, rate-limiting windows, delayed queues, and top-N features without a DB query.
15. **Q: TRICKY: DynamoDB vs Cassandra — both KV-ish wide-column?** A: DynamoDB is managed (you don't run nodes; cost by RCU/WCU), eventual/strong reads, LWW, 400KB item limit, no local joins. Cassandra is self-managed, tunable consistency (ONE/QUORUM/ALL), richer CQL queries, but more ops. Choose by managed-vs-self-hosted and consistency control needs.
16. **Q: What happens to a Redis key with TTL when the server restarts?** A: If persisted (RDB/AOF), TTL is preserved and re-enforced on load; unpersisted keys simply vanish on restart. Evicted keys (LRU/LFU) also vanish — hence never rely on cache contents.
17. **Q: PRODUCTION: Should sessions live in a cache or a DB?** A: Both are common: Redis/DynamoDB-with-TTL for web sessions (fast, auto-expire). If sessions must survive node/cache loss and be auditably durable (SSO compliance), use a DB with short TTL. The TTL is the key feature either way.

## 14. Follow-Up Questions
1. **Q: What is a Bloom filter and where would you use one in a KV/cache?** A: A probabilistic set membership structure (O(1), space-efficient, may false-positive). Use before the cache to avoid cache-penetration DB hits for non-existent keys (e.g., filter out queries for deleted product ids).
2. **Q: What is cache penetration and how do you handle it?** A: Requests for non-existent keys always miss the cache → hammer the DB. Fix: cache negative results (short TTL), Bloom filter, or validate keys upstream.
3. **Q: How does Redis Cluster partition data?** A: 16384 hash slots (`CRC16(key) % 16384`) distributed across nodes; each node owns a range; keys are routed by slot; MOVED/ASK redirects guide clients; scaling adds/removes slots with minimal data movement.

## 15. Coding Example
```python
# Redis: cache-aside + stampede guard + leaderboard
import redis, json
r = redis.Redis(decode_responses=True)

def get_product(pid: str):
    cached = r.get(f"p:{pid}")
    if cached is not None:
        return json.loads(cached)
    # single-flight guard against stampede
    with r.lock(f"lock:{pid}", timeout=5):
        cached = r.get(f"p:{pid}")          # re-check after acquiring
        if cached is not None:
            return json.loads(cached)
        row = db_query("SELECT ... FROM products WHERE id=%s", pid)
        r.setex(f"p:{pid}", 300, json.dumps(row))   # TTL 5 min
        return row
```
```python
# Redis: atomic counter + sorted-set leaderboard
r.incr(f"views:{article}")                          # counter
r.zadd("lb:aug", {user: score})                     # leaderboard
top = r.zrevrange("lb:aug", 0, 9, withscores=True)  # top-10
```
```js
// MongoDB: model one-to-many (embed) vs reference
// Embed (small, read-together):
db.users.insertOne({ _id: 1, name: "Ana", addresses: [
  { city: "Pune" }, { city: "Berlin" } ] });
// Reference + $lookup (large, independently updated):
db.orders.insertOne({ _id: 100, user: 1, items: [{ sku: "P42", qty: 2 }] });
db.orders.aggregate([
  { $match: { _id: 100 } },
  { $lookup: { from: "users", localField: "user",
               foreignField: "_id", as: "customer" } }
]);
```
```javascript
// DynamoDB: TTL + strong read (AWS SDK v3)
await dynamo.putItem({ TableName: "sessions",
  Item: { user_id: { S: "u42" }, ttl: { N: "1754400000" } } });
await dynamo.getItem({ TableName: "sessions",
  Key: { user_id: { S: "u42" } }, ConsistentRead: true });
```

## 16. Industry Usage
- **Redis**: cache/session/queue at essentially every large web company; the 2024 license change (RSAL/AGPLv3) forked Valkey (Linux Foundation). Used for rate limiting, leaderboards (gaming), pub/sub.
- **DynamoDB**: AWS serverless flagship; TTL sessions, metadata (Amazon's own scale), gaming leaderboards, event sourcing tables — the "Dynamo paper" (2007) shaped all LWW/eventual-consistency design.
- **MongoDB**: catalogs/content at countless startups; used by Atlassian, Coinbase (self-managed), SEGA (sharded games); `$lookup` and sharding maturity growing.
- **CouchDB/Couchbase**: mobile sync (PouchDB) and memory-first KV+doc hybrid (Couchbase) niches.
- **etcd**: the coordination KV (Raft) at the heart of Kubernetes — a *correctness-critical* KV, unlike cache Redis.
- **Memcached**: still the ultra-simple cache in many CDN/edge stacks.

## 17. References
- DeCandia et al., "Dynamo: Amazon's Highly Available Key-value Store" (2007).
- Redis docs: https://redis.io/docs/ (data types, persistence, cluster).
- MongoDB docs: https://www.mongodb.com/docs/ (data modeling, sharding, aggregation).
- Memcached: https://memcached.org/
- Use The Index, Luke — cache/DB interplay: https://use-the-index-luke.com/
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 24.3-24.4 (key-value & document).

## 18. Cheat Sheet
- KV: O(1) get/put/delete, TTL, eviction, counters (INCR), sorted sets (leaderboards), locks (SETNX+TTL), streams/queues.
- Cache patterns: cache-aside (populate on miss, delete on write), write-through, write-back, single-flight vs stampede, jittered TTL, cache negative results / Bloom filter vs penetration.
- Redis vs Memcached: persistence + types + scripting vs pure cache + multithreaded.
- Redis Cluster: 16384 slots via CRC16; MOVED redirects.
- DynamoDB: eventual default, ConsistentRead for strong, RCU/WCU, TTL, LWW.
- Document: embed (small/read-together) vs reference (large/independent) + $lookup; compound indexes; shard key design (cardinality + access pattern); COLLSCAN is the enemy.
- One-to-many: embed small; reference + denormalize hot fields large.
- Distribution: consistent hashing → minimal rebalance; hot keys → load skew.

## 19. Quiz
1. Redis persistence options: a) RDB/AOF b) only RDB c) none d) SQL → **a**
2. `SETEX` does: a) set with TTL b) delete c) list d) rank → **a**
3. Best cache pattern for read-heavy data? a) write-back b) cache-aside c) write-through d) none → **b**
4. Mongo COLLSCAN means: a) indexed b) full scan (bad) c) sharded d) capped → **b**
5. Shard key should have: a) low cardinality b) high cardinality + used in queries c) monotonic d) none → **b**
6. DynamoDB strong read: a) ConsistentRead b) always c) never d) QUORUM → **a**
7. Cache stampede fix? a) no TTL b) single-flight/jitter c) more caches d) restart → **b**
8. Redis Cluster slot count: a) 1024 b) 16384 c) 256 d) unlimited → **b**

## 20. Flashcards
- **Q: KV access complexity?** → **A:** O(1) get/put by key.
- **Q: Redis persistence?** → **A:** RDB snapshots + AOF log (optional).
- **Q: Cache-aside?** → **A:** Read cache, miss → DB → populate; delete cache on write.
- **Q: Stampede guard?** → **A:** Single-flight lock + jittered TTL.
- **Q: Cache penetration fix?** → **A:** Cache negatives / Bloom filter.
- **Q: Embed vs reference?** → **A:** Embed small read-together; reference large/independent.
- **Q: Mongo $lookup is?** → **A:** A per-doc correlated lookup, not a real join.
- **Q: COLLSCAN?** → **A:** Full collection scan — the classic Mongo perf problem.
- **Q: DynamoDB default reads?** → **A:** Eventually consistent (ConsistentRead = strong).
- **Q: Redis Cluster hashing?** → **A:** CRC16(key) % 16384 slots.

## 21. Revision
KV = O(1) by-key for caches/sessions/counters with TTL and eviction; Redis is the Swiss-army version (types, persistence, cluster), DynamoDB the managed LWW service. Document = self-contained JSON objects with flexible schema and field indexes; model one-to-many by embedding (small) or referencing + denormalizing (large); use compound indexes and design the shard key around the dominant access pattern. Cache correctly (cache-aside, single-flight, jitter, negatives). No joins anywhere — that's the contract you accept for scale and flexibility.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Redis vs Memcached?" | 2, 13 |
| "When is KV the wrong choice?" | 13 |
| "Cache-aside + stampede?" | 8, 13 |
| "MongoDB vs relational for catalogs?" | 4, 13 |
| "Shard key design?" | 9, 13 |
| "DynamoDB consistency model?" | 9, 13 |
| "Embed vs reference modeling?" | 13 |
| "$lookup vs join?" | 9, 13 |
| "Distributed lock with Redis?" | 13 |
| "Cache penetration/bloom filter?" | 14 |
