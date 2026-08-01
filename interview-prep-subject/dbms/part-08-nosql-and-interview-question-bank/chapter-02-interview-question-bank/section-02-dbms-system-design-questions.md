# DBMS System Design Questions

> **TL;DR**: The database half of design interviews — a reusable structure (requirements → access patterns → consistency → schema/model → partitioning → caching → replication → failover) that answers "design the data layer of X" for ridesharing, e-commerce, social feeds, chat, URL shorteners, and analytics platforms, using the vocabulary from Parts 04-08.

## 1. Why Does This Exist?
A large fraction of system-design interviews are *data design* interviews wearing a disguise: "design Twitter" is really "design the timeline read/write data path"; "design a checkout" is really "how do you keep inventory consistent under concurrency?"; "design a rideshare app" is really "how do you store driver locations and match trips?" This file exists to give you a *reusable skeleton* for the DBMS portion of any design question — the vocabulary (Part 04 indexing, Part 05 isolation, Part 07 EXPLAIN thinking, Part 08 CAP/NoSQL) converted into a step-by-step response that interviewers recognize as senior-level. Without the skeleton, candidates ramble about features; with it, they systematically derive the data model, the consistency story, the shard key, the cache, and the failure modes — which is what actually earns the "design" credit.

## 2. How Does It Work?
A fixed structure that works for (almost) every DBMS design question:
1. **Requirements**: clarify scale (users, QPS, writes/sec, data size, growth), functional reads/writes, latency/availability/consistency requirements.
2. **Identify access patterns**: name the top queries (by-key? by-range? aggregates? traversals?) and top writes (transactional? append? counter?).
3. **Consistency & isolation requirements**: which data is money/inventory/unique (strong/transactional — Part 05), which is eventual-OK (feeds/counters — Part 08).
4. **Choose the engine per data class** (SQL default + NoSQL where a pattern dominates — Part 08 §5).
5. **Schema/model design**: relational schema or document/wide-column model; indexes to serve the hot queries (Part 04); denormalization for read paths.
6. **Partitioning/sharding**: shard key selection, consistent hashing vs range, hot-key handling (Part 04/08).
7. **Caching**: what's cached (cache-aside/Redis), TTLs, invalidation, stampede protection (Part 08 §2).
8. **Replication & HA**: async/sync/consensus, failover, RPO/RTO (Part 06).
9. **Monitoring + failure modes**: how you'd catch and fix the slow path (Part 07 §3).

## 3. When Is It Used?
- The "design X" interview round (backend/generalist) where the data layer is 40-60% of the grade.
- The "how would you store/query this at scale?" variant questions ("100M likes", "1B events/day").
- Practicing with a peer: run the skeleton on a new problem every session.
- Real architecture work: the same skeleton produces the ADR (decision record) for production data design.
- Interviews: "design Twitter timeline", "design an e-commerce checkout", "design a ride-hailing platform", "design a chat app", "design a URL shortener", "design a metrics/analytics pipeline", "design a social graph/feed".

## 4. Why Wasn't Another Approach Chosen?
- *Memorized answers per product* ("here's the Twitter answer"): breaks on any novel twist; interviewers reword the same question to detect memorization. The *skeleton* generalizes; the product is just the instantiation.
- *Jumping to schema/ERD immediately*: candidates who draw tables without stating scale/consistency get exposed at the "why?" follow-up. Requirements-first anchors everything.
- *Jumping straight to "use Cassandra"*: NoSQL-as-default signals hype, not reasoning; the skeleton forces the SQL-default + evidence-based deviation stance (Part 08 §5).
- *Only OLTP designs*: warehouses/analytics are their own design questions; the skeleton branches to columnar/streaming where scans dominate.
- *No failure/monitoring discussion*: senior signals are "what breaks and how do you find it" — the last two steps make the answer production-grade.

## 5. Intuition
Treat the design interview like **architecting a building**: you don't start with the lobby décor (schema). You start with *who uses it and how many* (requirements), *what traffic does each entrance get* (access patterns), *which floors need fireproofing* (consistency-critical data), *which materials* (engine choice), *the load-bearing layout* (schema + indexes), *how the building scales when the block grows* (sharding), *where the vaults and quick-access lockers are* (caching), and *how it survives a fire* (replication/failover) — then, only at the end, *how you'd inspect the building's health* (monitoring). The interviewer's real question is never "what does a checkout look like?" — it's "do you know *which decisions matter* and *which order* to make them in?" The skeleton is that ordering: it front-loads the decisions that, if wrong, make everything else collapse (shard key, consistency, engine), and defers the detail that can be fixed later (exact columns).

## 6. Real-World Analogy
**Designing a city's transit + freight system is the "design a ride-hailing platform" question.** Step 1: how many passengers/day, how many cars, peak-hour bursts (requirements). Step 2: the hot operations are "find cars near me" (spatial query) and "assign a rider to a car" (match + state change) — everything else is secondary (access patterns). Step 3: *billing* and *trip state* must be airtight (transactions, money), while *driver location pings* tolerate staleness (eventual — a 5-second-old ping is fine) (consistency). Step 4: the *trip ledger* lives in Postgres (money + joins), *locations* in a fast keyed/geo store (Redis/Geo or a KV with TTL), *analytics* in a warehouse (columnar) (engine per data class). Step 5: schema for trips/riders/drivers with indexes on the hot queries (driver_id, rider_id), denormalized location cache. Step 6: shard trips by driver_id or rider_id (both query paths!), locations by consistent hashing (partitioning). Step 7: cache hot profiles/areas; single-flight the match computation (caching). Step 8: Postgres primary + sync/async replica for read scaling; location store replicated for availability (replication). Step 9: slow-query dashboards + EXPLAIN on the match query (monitoring). Delivered as one coherent walk, the interviewer hears: "I know which data is sacred, which can lag, where the scale pressure is, and how I'd verify it works."

## 7. Formal Definition
A structured design method for the data layer: given a product P, derive (R) requirements (scale, QPS, write rate, size, growth, latency, availability, consistency); (AP) dominant access patterns (by-key / range / aggregate / traversal; transactional vs append vs counter writes); (C) per-data-class consistency/isolation (strong vs causal vs eventual, per Part 05/08); (E) engine mapping (relational default; KV/document/wide-column/columnar/graph by pattern dominance, Part 08 §5); (S) schema + indexes (Part 04) + denormalization; (H) partitioning/shard-key design (Part 04/08) incl. hot-key handling; (K) cache strategy (cache-aside, TTL, invalidation, stampede guard); (R2) replication + failover (async/sync/consensus; RPO/RTO; Part 06); (M) monitoring + failure modes (Part 07 §3). Output: a defensible data architecture with explicitly stated trade-offs.

## 8. Example
**"Design the data layer for an e-commerce checkout."**
- **Requirements**: 10k checkouts/min peak; inventory is globally consistent-critical; order records append-ish; read: order history, product pages; p99 < 300ms.
- **Access patterns**: W: create order (transactional: decrement stock + create order + charge), read: order by id, orders by user (range), product page by sku.
- **Consistency**: *inventory decrement must be transactional* (money/stock) — READ COMMITTED+or SERIALIZABLE on Postgres; *order history* is eventual-OK; *product page* is cache-able.
- **Engine**: Postgres = orders + stock (transactions/joins); Redis = product-page cache + session; warehouse = daily sales analytics. No NoSQL needed for the transactional core.
- **Schema**: `orders(order_id, user_id, created_at, total)`, `order_items(order_id, sku, qty, price)`, `inventory(sku, stock)`, `products(sku, price, ...)`. Indexes: `orders(user_id, created_at)`, `inventory(sku)`, FK constraints. Denormalize `orders.total` (don't recompute).
- **Partitioning** (if needed): order by `user_id` (both query paths hit the same shard); inventory is *global state* — keep in one Postgres or use NewSQL if it must shard; hot skus need optimistic concurrency (row version) not just locking.
- **Caching**: product pages (Redis, TTL), order-history reads via cache-aside; *never cache inventory* — correctness first.
- **Replication**: Postgres primary + async replica for read load; RPO≈small; failover via managed service.
- **Monitoring**: track checkout latency, EXPLAIN the checkout write path, alert on lock waits/deadlocks (Part 05 §deadlock).
Key senior beats: inventory as *global transactional state* (not sharded casually), the distinction between eventual (history/pages) and strong (stock/charge), and "never cache inventory."

## 9. Internal Working
The skeleton works because each step *depends on* the previous: consistency requirements (3) determine engine (4); access patterns (2) determine indexes/schema (5); scale (1) determines whether partitioning (6) is needed and its key; latency/availability (1) determine caching (7) and replication (8). Interviewers probe by *pushing on a dependency* — "what if writes double?" (⇒ partitioning/caching), "what if you lose a node?" (⇒ replication), "why not Cassandra for orders?" (⇒ consistency argument). Practicing the skeleton means being able to re-derive any later step from earlier givens, out loud, with a concrete example per step (Part 05's isolation levels, Part 08's CAP/PACELC, Part 07's EXPLAIN, Part 04's index rules). The "trap" moments are when a candidate treats a *dependency* as a *free choice* (e.g., sharding inventory because "sharding is scalable") — the skeleton makes the dependency explicit.

## 10. Time Complexity
- A full design walk: 30-45 minutes (the interview slot); the DBMS portion ~15-20 min of it.
- The skeleton's value: it turns an open-ended "design X" into a *sequence of small decisions* — each cheap to state, cheap to defend, and collectively covering the whole data layer.
- Practice loop: one new problem + review per session (~1 hour); after 8-10 problems the skeleton becomes automatic.

## 11. Advantages
- **Complete coverage**: no interviewer surprise left unaddressed (schema, consistency, scale, cache, HA, monitoring all in one pass).
- **Defensible**: every choice is *derived* from requirements — the "why not Cassandra?" follow-ups have built-in answers.
- **Senior signals**: stating RPO/RTO, global-state inventory, LWW-vs-strong, and EXPLAIN verification reads as production experience.
- **Portable**: the same skeleton handles social, commerce, chat, analytics, geo.
- **Interview-efficient**: structure keeps you from wandering; interviewers reward the organized walk.

## 12. Disadvantages
- **Can feel formulaic** — interviewers know the script; you must still *reason*, not recite (name the actual scale, the actual query).
- **Requires breadth**: weak Part 05/08 knowledge shows immediately under probes.
- **Over-design risk**: candidates add sharding/NewSQL when the stated scale doesn't need it — the skeleton must include a "do we actually need this?" gate.
- **Not every design question is DBMS-heavy**: routing/queueing/API portions also matter; this skeleton is the *data* part, not the whole answer.

## 13. Interview Questions
1. **Q: Design the database for a ride-hailing app.** A: (1) Requirements: 100k drivers, 1M riders, 500 rps. (2) Access: find cars near a point (spatial), assign trip (transactional state change), trip history. (3) Consistency: billing/trip state strong (Postgres), locations eventual-OK (Redis/geo, TTL). (4) Engine: Postgres (trips, wallets, riders) + Redis/geo (locations) + warehouse (analytics). (5) Schema: trips(trip_id, driver_id, rider_id, status, amount, created_at) with indexes on driver_id, rider_id; wallet table with row version for optimistic updates. (6) Shard trips by driver_id (or rider_id — pick one, both query paths hit one shard). (7) Cache hot areas/leaderboard; single-flight match. (8) Postgres primary + async replica; geo store replicated. (9) Monitor match-latency EXPLAIN + lock waits. → Part 04-08
2. **Q: Design Twitter's timeline read path.** A: Fan-out on write: when a user posts, push the post into followers' timelines (write-heavy fan-out, eventual-OK). Reads: home timeline = cached KV read (Redis/DynamoDB) by user_id; social graph = graph DB or friends table. Consistency: timeline can be eventual (5s staleness fine); likes are counters (LWW-OK, Redis INCR). Shard timelines by user_id (consistent hashing); hot celebrities get fan-out special-casing (only push to active followers / read-time merge). → Part 08 §2/4
3. **Q: Design a URL shortener's storage.** A: KV fits: short-code → URL. But need: collision-free (unique codes — use a base62 counter or hash + uniqueness constraint), expiry (TTL), click analytics (append events → columnar/warehouse). Engine: Postgres or DynamoDB for the mapping (PK = code); Redis for hot lookups; analytics in warehouse. Scale: the lookup is by-key O(1); shard by code (hash). Consistency: mapping is append-ish; analytics eventual. → Part 08 §2
4. **Q: Design the data layer for a chat app (1-1 and groups).** A: Per-conversation ordering is the core. Model: messages(conv_id, msg_id(ts+seq), sender, body); query by conv_id + range on seq — this is *exactly* Cassandra's partition-key + clustering pattern (or Postgres with `(conv_id, id)` primary key + range). Index on conv_id; shard by conv_id. Reads: last-N messages via range scan; presence via Redis (TTL). Consistency: message order must be total per conversation (strong per conv — sequence numbers), but cross-conv is irrelevant. → Part 08 §3
5. **Q: Design an inventory system for 100M SKUs.** A: Inventory is *global transactional state*: decrement stock atomically with order creation → Postgres row version/optimistic locking or SELECT FOR UPDATE, in READ COMMITTED+; keep inventory in *one* logical store (don't shard casually — a hot SKU becomes a hot partition; use optimistic concurrency + retries). Read-side (available count) can be cached with very short TTL or served by replica; never cache the authoritative decrement. If write throughput truly demands sharding, go NewSQL (CockroachDB) for distributed transactions, or partition by a *location* dimension. → Part 05/08
6. **Q: TRICKY: 100M likes on one post — how do you count it?** A: A single hot counter is the classic hot-key problem. Options: (1) Redis INCR on a per-post key — O(1), LWW-tolerant, but one Redis key hot; (2) *counter sharding*: fan out by suffix (post:42:0..post:42:15), INCR a random shard, SUM on read — spreads the write; (3) batch/async: buffer likes and flush in batches to the DB; read the cache, lazily persist. Like-count is eventual-OK; correctness concern is only "don't lose too many on crash" — accept some loss or use Redis AOF. → Part 08 §2
7. **Q: Design a metrics/analytics pipeline ingesting 1B events/day.** A: Writes dominate and are append-only → Kafka → columnar warehouse (ClickHouse/BigQuery) with batch inserts; partition by time (month) for pruning. Reads are scans/aggregations (columnar). Don't put this in the OLTP DB. Dashboards hit pre-aggregated rollups (hourly/daily) materialized by scheduled jobs. Consistency: eventual, fine. Retries/at-least-once with deduplication (event_id unique) → idempotent ingestion. → Part 08 §3
8. **Q: How do you choose the shard key for an e-commerce orders table?** A: The shard key must match the *dominant query path*. If the app reads "orders for a user," shard by user_id so both write and read hit one shard (no scatter-gather). If it reads "orders by merchant," shard by merchant_id. Compromise: shard by user_id + keep a denormalized merchant index (or a secondary lookup table with its own shard). Avoid monotonic keys (auto-increment ids → hot last shard) — use hash-based sharding (consistent hashing or hash of user_id). → Part 04/08
9. **Q: When would you *not* shard?** A: When a single node serves the load (most OLTP: a few 1000s QPS is fine), when the data is inherently *global state* (inventory, wallet balances, unique counters) where sharding breaks transactional integrity, or when joins across shards would dominate. Scale *up* (bigger node, replicas, cache) before sharding *out* — sharding is a last resort, not a default. → Part 08 §5
10. **Q: How do you keep a cache consistent with the database?** A: Cache-aside with *delete-on-write* (invalidate, not just update, to avoid races): read → miss → DB → populate; write → DB first → delete cache. Add short TTLs as a safety net. For strong read-after-write, read-through/read-your-writes with a short-TTL cache or bypass cache for the critical read. Handle stampede with single-flight locks + jittered TTL. → Part 08 §2
11. **Q: TRICKY: Your order service just lost its Redis cache. What happens?** A: With cache-aside, the DB is the source of truth — reads miss and hit the DB (thundering herd) until cache repopulates. That's a *performance* incident, not data loss, *provided* nothing relied on Redis for correctness (never cache inventory/balances authoritatively). Mitigation: cache warming, single-flight, DB replicas to absorb the read spike. The design answer: "Redis is a derived cache; its loss costs performance, not correctness." → Part 08 §2
12. **Q: Design the data layer for a social network's friends graph.** A: Two classes: (1) profile data → document/relational (users table, flexible profile fields — Postgres JSONB or Mongo); (2) the *graph* → graph DB (Neo4j) for "friends of friends", "mutual friends", "feed permission traversal" — or a `friends(user_a, user_b, since)` table if depth is small and fixed. Traversal at variable depth is the graph DB's home (Part 08 §4). Consistency: friendship edges can be eventually consistent; sync graph from the relational source via CDC. → Part 08 §4
13. **Q: How do you handle read-your-writes in an eventually-consistent system?** A: Route the user's own writes to the primary (session-stickiness / read-your-writes affinity), or read from primary for that key, or use strong reads (DynamoDB ConsistentRead). Accept eventual for *others'* writes. This is a concrete PACELC/consistency design decision. → Part 05/08
14. **Q: Design the database for a leaderboard with 10M users.** A: Redis sorted sets are the natural fit: `ZADD lb:global score user`, `ZREVRANGE lb:global 0 99` (top-100), rank lookups O(log n). Scores are counters (LWW/incremental-OK). Persist the final scores to a relational/warehouse store asynchronously for history/analytics. Shard by leaderboard scope (global vs per-game); per-scope hotness bounded. → Part 08 §2
15. **Q: TRICKY: "Use PostgreSQL" was your answer for checkout. What breaks at 10x scale and how do you fix it?** A: Postgres itself scales: bigger node, read replicas, connection pooling, partitioning (declarative) for the orders table, better caching. The *real* pressure is (1) the checkout write path (contention on inventory rows → row-lock waits; fix: optimistic concurrency + retries, or serialize stock ops) and (2) analytics growth → move reporting to the warehouse. Only after those are exhausted consider NewSQL (distributed transactions) or microservice-owned stores. The senior answer is: *identify the actual bottleneck, not the fashionable scale-out.* → Part 07 §3/08 §5

## 14. Follow-Up Questions
1. **Q: "What's the RPO/RTO of your design?"** → Connect to replication: async replica RPO>0, sync/consensus RPO=0, restore-from-backup RTO minutes-to-hours (Part 06).
2. **Q: "How would you debug a sudden latency spike?"** → Monitoring loop: pg_stat_statements → EXPLAIN → stats/index/memory fix (Part 07 §3).
3. **Q: "Your shard is hot (one user has 50M followers). Fix?"** → Supernode/fan-out special-casing, read-time merge, sub-partitioning by suffix (Part 08 §2/3/4).
4. **Q: "Could this be done without any NoSQL?"** → Yes for most: Postgres + JSONB + replicas + partitioning covers 80% (Part 08 §5); name when a family truly wins.

## 15. Coding Example
```sql
-- Checkout: transactional inventory decrement with optimistic concurrency
BEGIN;
SELECT stock, version FROM inventory WHERE sku = 'P42' FOR UPDATE;
-- check stock >= qty; else rollback
UPDATE inventory SET stock = stock - 5, version = version + 1
 WHERE sku = 'P42' AND version = 7;
-- if 0 rows updated → conflict → retry/abort (optimistic path)
INSERT INTO orders (user_id, total, status) VALUES (42, 4500, 'paid');
INSERT INTO order_items (order_id, sku, qty, price) VALUES (lastval(), 'P42', 5, 900);
COMMIT;
```
```python
# Fan-out-on-write timeline (eventual-OK) with counter sharding for hot posts
def post_message(author_id, text):
    post = insert_post(author_id, text)                      # relational source of truth
    for follower in get_followers(author_id):
        timeline.add(follower, post.id)                      # KV append (async, batched)

def like_post(post_id):
    shard = random.randint(0, 15)
    redis.incr(f"likes:{post_id}:{shard}")                   # counter sharding

def total_likes(post_id):
    return sum(redis.get(f"likes:{post_id}:{s}") for s in range(16))
```
```sql
-- Chat ordering: Cassandra-style partition+clustering, or Postgres composite PK
CREATE TABLE messages (
  conv_id  bigint,
  seq      bigint,          -- per-conversation sequence
  sender   bigint,
  body     text,
  PRIMARY KEY (conv_id, seq)   -- partition by conv, ordered by seq
);
SELECT * FROM messages WHERE conv_id = 7 AND seq > 1000 ORDER BY seq LIMIT 50;
```

## 16. Industry Usage
- The skeleton is the *standard* answer shape in backend/cloud architecture interviews (System Design Interview series, Alex Xu; Grokking-style courses) — every design problem decomposes into the same data steps.
- Production ADRs use the identical flow: requirements → pattern → consistency → engine → schema → shard → cache → HA → monitoring — because it produces a *decision record* with rationale.
- Real distributed systems (e.g., Amazon order pipeline, Twitter timeline, Uber matching) follow exactly these trade-offs: transactional core (Postgres/NewSQL) + derived cache/geo (Redis) + analytics (warehouse) + specialized graph for relationships.

## 17. References
- Xu, *System Design Interview* (Vol 1/2) — the data portions of every chapter.
- Kleppmann, *Designing Data-Intensive Applications* — replication, partitioning, consistency (Ch. 5-7).
- Part 04 (indexing/sharding), Part 05 (isolation), Part 06 (replication/recovery), Part 07 (EXPLAIN), Part 08 (CAP/NoSQL families) — the depth behind the skeleton.
- Fowler, "Polyglot Persistence": https://martinfowler.com/bliki/PolyglotPersistence.html

## 18. Cheat Sheet
- Order: requirements → access patterns → consistency → engine → schema+indexes → sharding → caching → replication/HA → monitoring.
- SQL default; NoSQL only on pattern evidence (Part 08 §5).
- Global state (inventory, balances, unique codes) stays transactional & unsharded (or NewSQL).
- Hot-key fixes: counter sharding, fan-out special-casing, read-time merge.
- Shard key = dominant query path; avoid monotonic keys; hash-based.
- Eventual-OK: feeds, counters, presence, analytics; Strong: money, stock, unique constraints.
- Cache-aside + delete-on-write + TTL + single-flight; never cache authoritative stock.
- Async replica = RPO>0; sync/consensus = RPO≈0; state both in the answer.
- Monitoring: EXPLAIN + slow-query stats; the design must include "how do I verify it."
- Failure beat: "what happens if X dies?" must have an answer (cache loss = perf, DB loss = failover, both tested).

## 19. Quiz
1. First step of any design? a) schema b) requirements c) Cassandra d) cache → **b**
2. Inventory should be: a) sharded b) transactional/global c) in Redis d) LWW → **b**
3. Timeline reads are: a) strong b) eventual-OK c) never cached d) graph → **b**
4. Shard key should match: a) smallest table b) dominant query path c) random d) monotonic id → **b**
5. Cache loss causes: a) data loss b) perf incident only c) corruption d) nothing → **b**
6. Hot-key counter fix? a) single node b) counter sharding/fan-out c) remove TTL d) index → **b**
7. Async replica RPO: a) 0 b) >0 c) infinite d) undefined → **b**
8. When not to shard? a) small load b) global state c) joins dominate d) all of the above → **d**

## 20. Flashcards
- **Q: Design skeleton order?** → **A:** Req → patterns → consistency → engine → schema → shard → cache → HA → monitor.
- **Q: Inventory at scale?** → **A:** Keep global & transactional; optimistic concurrency + retries (or NewSQL).
- **Q: Hot-key like counter?** → **A:** Counter sharding (sum on read) + Redis INCR.
- **Q: Timeline consistency?** → **A:** Eventual; fan-out on write, cached KV.
- **Q: Shard key rule?** → **A:** Dominant query path; hash-based, avoid monotonic.
- **Q: Cache failure impact?** → **A:** Performance, not correctness (never cache authoritative state).
- **Q: Async replica RPO?** → **A:** >0 (lose recent writes on failover); sync = 0.
- **Q: When not to shard?** → **A:** Load fits one node, or global-state integrity matters.

## 21. Revision
DBMS design interviews = one skeleton, any product. Requirements → access patterns → consistency (strong vs eventual, Part 05/08) → engine (SQL default, Part 08 §5) → schema + indexes (Part 04) → sharding (dominant query path, hot keys) → caching (cache-aside, never-cache-authoritative) → replication/HA (RPO/RTO, Part 06) → monitoring (EXPLAIN, Part 07). The differentiators: state consistency per data class, protect global state, handle hot keys, and always include the failure + verification beats. Practice 8-10 problems with the skeleton and it becomes automatic.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Design the data layer of X" (any product) | 2, 8, 13 |
| "How do you pick a shard key?" | 2, 8, 13 |
| "How do you count 100M likes?" | 8, 13 |
| "Cache consistency / cache loss?" | 7, 13 |
| "Read-your-writes under eventual consistency?" | 13 |
| "When not to shard / use NoSQL?" | 4, 13 |
| "RPO/RTO of your design?" | 7, 13 |
| "Debug a latency spike?" | 2, 9, 13 |
