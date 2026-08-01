# NoSQL Overview & Types

> **TL;DR**: NoSQL is a family of non-relational data models (key-value, document, wide-column, graph) that relax ACID guarantees and general query capability to gain horizontal scalability, availability, and simpler operations for specialized workloads — understood through CAP (partition-tolerance forces a consistency/availability choice) and PACELC (the latency trade-off of that choice).

## 1. Why Does This Exist?
Relational databases excel at general queries, joins, and strong integrity (Parts 01-07), but they scale **up**: one node (or a modest replica set) owns the write path, and horizontal write scaling requires painful sharding plus distributed ACID. Around 2005-2010 the web grew workloads (session data, feeds, telemetry, catalogs) that were *not* relational in nature — mostly O(1) reads/writes by key, or append-heavy logs — where the relational features (joins, transactions, rigid schema) were overhead, not value. NoSQL exists to trade those features for: (a) **horizontal scaling** (partition across many nodes, no single-writer bottleneck), (b) **availability** (keep serving through node/network failures), and (c) **schema flexibility / specialized query shapes** (documents, graphs). The CAP theorem made the trade explicit: when a network partition happens, you choose consistency or availability — and the rest of the time (PACELC) you choose latency or consistency.

## 2. How Does It Work?
Four families, each with a data model and a sweet spot:
- **Key-Value** (Redis, DynamoDB, Memcached, etcd): a giant hash table. Get/put/delete by opaque key; value is a blob (Redis: rich value types; DynamoDB: items). Scales via partitioning (sharding/consistent hashing); DynamoDB is a "NoSQL-as-a-service" KV. Best for caches, sessions, config, counters.
- **Document** (MongoDB, CouchDB, DynamoDB's document API): values are structured documents (JSON/BSON); indexes on nested fields; rich queries but *no general joins* (aggregation pipelines emulate them). Best for content, catalogs, user profiles, flexible schemas.
- **Wide-Column / Columnar** (Cassandra/HBase/Scylla; ClickHouse/Vertica/Redshift for columnar): rows with dynamic column families, ordered by a partition key (Cassandra), or columnar storage for analytic scans (ClickHouse). Best for write-heavy, always-available, time-series/telemetry (Cassandra) and large analytical queries (columnar).
- **Graph** (Neo4j, Amazon Neptune, TigerGraph): nodes + edges as first-class; `MATCH`/`Cypher` for path queries. Best for social networks, fraud detection, recommendation/knowledge graphs.
Mechanism across all: partitioning (hash/consistent-hashing or range) + replication (sync/async) + eventual/strong consistency options + API rather than SQL.

## 3. When Is It Used?
- **KV/Redis**: caching layer in front of a relational DB; session store; rate limiting; leaderboards; distributed locks; queues.
- **DynamoDB**: serverless applications needing single-digit-ms key lookups with seamless horizontal scaling; sessions; event/metadata stores.
- **MongoDB**: content management, catalogs, real-time analytics dashboards, user profiles, IoT with variable schema, rapid-prototype products.
- **Cassandra**: time-series/telemetry (metrics, IoT), messaging, write-heavy logs, global applications needing multi-datacenter availability with "last-write-wins" semantics.
- **Columnar (ClickHouse/Vertica)**: analytics/OLAP — aggregation over billions of rows, time-series analytics dashboards.
- **Graph**: social/friend graphs, fraud ring detection, recommendation ("people who bought"), knowledge graphs, network/access-control.
- Interview: "why do NoSQL databases exist?", "name the families", "when would you NOT use SQL?", "explain CAP/PACELC", "eventual consistency".

## 4. Why Wasn't Another Approach Chosen?
- *Sharded relational DBs*: possible (Part 04 techniques) but operations-heavy (manual shard management, cross-shard joins/transactions, no natural global index) — the industry chose purpose-built systems over retrofit.
- *One-node relational for everything*: fine until write/scale needs outgrow it; NoSQL exists precisely where the relational engine's generality (joins, transactions) is unused but its single-writer/scale-up model is a bottleneck.
- *NewSQL (CockroachDB, TiDB, Spanner)*: keeps SQL + transactions + horizontal scale at the cost of complexity/consensus overhead — the "have it all" option, used when the app *needs* both (e.g., finance); NoSQL remains when the workload doesn't justify it.
- *Only strong consistency everywhere*: synchronous replication everywhere = high latency under partition (PACELC); most modern web apps tolerate eventual consistency for most data, so relaxing it is the *point*.
- *Schemaless-only (pure documents)*: loses structure for many workloads (counters, analytics) — hence separate families instead of one "NoSQL".
The families exist because each workload's *access pattern* (by-key, per-object, per-time-range, per-relationship) determines the optimal trade.

## 5. Intuition
Relational databases are a **spreadsheet with a set of rules**: every row must fit the columns, rows talk to each other through keys, and every change either all happens or none does. NoSQL is a **collection of specialized tools**: the address book (KV — look up by name, instant), the dossier binder (document — each file self-contained, messy but flexible), the logbook (wide-column — append the current reading, always record, don't stop), and the family tree (graph — follow connections). Each tool is worse at everything else, but *much* better at its job at scale. CAP/PACELC is the honest admission that you can't have the spreadsheet *and* the address book's uptime *and* zero wait: when the network hiccups, you pick "everyone sees the same data" or "everyone gets an answer," and the choice costs you latency in the other moments.

## 6. Real-World Analogy
A **city's systems**: the relational database is the *land registry* — one authoritative office, strict forms, every transfer must be notarized and coordinated (transactions), slow but utterly consistent. As the city grows, the registry becomes a bottleneck (single writer). NoSQL is the city *specializing*: the *courier service* (key-value) — hand over a parcel by tracking number, instant, no paperwork, if a courier is down another takes the route (availability over strict ordering); the *hospital patient files* (document) — every patient's file is self-contained and messy, some have allergies, some scans, no two alike, but a doctor needs the whole file at once; the *power-grid meter log* (wide-column/columnar) — thousands of meters write readings continuously, you almost never read a single one but you run weekly analytics over all of them; the *social graph of who-knows-whom* (graph) — "find friends of friends of A" is a *relationship* query the registry can't answer quickly. The registry still exists for property; the city simply added specialized systems for specialized jobs.

## 7. Formal Definition
**NoSQL**: "not only SQL" — a class of distributed database systems that relax one or more ACID guarantees (usually atomicity across multiple items, and/or strong consistency) and the relational data model in exchange for horizontal scalability, high availability, or specialized query semantics. **CAP theorem** (Brewer 2000, proven by Gilbert & Lynch 2002): during a network *partition*, a distributed system must choose between Consistency (every read sees the latest write) and Availability (every request gets a non-error response). **PACELC** (Abadi 2012): if a *Partition*, choose Availability or Consistency; Else (normal operation), choose Latency or Consistency. **BASE**: Basically Available, Soft state, Eventual consistency — the pragmatic inverse of ACID used by most NoSQL systems. The four data-model families (KV, document, wide-column, graph) instantiate these choices differently.

## 8. Example
Example 1 — **shopping cart (KV)**:
```
Redis:  SET cart:user42 {item: "laptop", qty: 1}
        GET cart:user42
```
No relational model needed; O(1) per key; partitioning across nodes; if the cart write races, last-write-wins (eventual) is fine.
Example 2 — **user profile (document, MongoDB)**:
```js
db.users.insertOne({ _id: 1, name: "Ana", email: "a@x.com",
  addresses: [{ city: "Pune" }, { city: "Berlin" }] })
db.users.find({ "addresses.city": "Pune" })
```
Flexible schema (addresses is an array; another user may omit it) — a relational design would force a join (users ⋈ addresses) or a fixed schema.
Example 3 — **CAP choice**: a distributed KV with replication — during a partition, a strict-serializable KV returns an error to the island it can't sync with (chooses C, drops A); an eventually-consistent KV returns the stale value (chooses A, drops C). DynamoDB (default) chooses availability + eventual consistency; Spanner chooses consistency.
Example 4 — **Cassandra write-heavy**: `INSERT INTO metrics (ts, node, value) VALUES (...) ;` — partitioned by node, written to any available replica, last-write-wins — designed so writes never block even during failures.

## 9. Internal Working
1. **Data model mapping**: KV = opaque bytes; document = self-describing JSON/BSON with queryable fields; wide-column = `(partition_key, clustering_key, ...columns)` rows, ordered within a partition; graph = adjacency model (nodes/edges stored with index on labels/properties).
2. **Partitioning**: consistent hashing (DynamoDB, Cassandra `murmur3(partition_key)`, Redis Cluster `CRC16` hash slots) → data spread across nodes; range partitioning (HBase, Cassandra clustering within partition) for ordered scans.
3. **Replication**: async multi-node (eventual: DynamoDB default, Cassandra quorum options); synchronous (RAFT/Paxos in etcd, Spanner, CockroachDB) for strong consistency. Replica factor configurable; `QUORUM`/`ONE`/`ALL` read/write consistency levels (Cassandra) and DynamoDB `ConsistentRead`.
4. **Queries**: KV = O(1) lookups (and scan for range keys); document = field indexes + aggregation pipeline (no cross-doc joins); wide-column = partition-key equality + clustering-range scans; graph = traversal/pattern matching (Cypher `MATCH`).
5. **Consistency engine**: vector clocks/versioning for last-write-wins or conflict resolution (DynamoDB/Cassandra); timestamps + quorum math for read-repair; the "replica catches up" path (hinted handoff, anti-entropy/gossip) restores consistency post-partition.

## 10. Time Complexity
- KV get/put by key: **O(1)** (hash lookup), plus network round trip (~sub-ms LAN, ms WAN) — the performance bet NoSQL makes.
- Document lookup by indexed field: **O(log n)** (B-tree) similar to relational; aggregate pipelines cost O(output) — but *no joins* → no cross-node join cost.
- Wide-column partition scan: O(rows in partition) for clustered range queries — great for time-series (read a device's last hour); full analytics = O(all rows).
- Columnar analytic scan: O(columns touched) — reading only needed columns avoids the row-store full-width cost.
- Graph traversal: BFS/DFS O(V+E) over explored subgraph — local, relationship-following queries are fast; *global* graph analytics are expensive.
- Write path (eventual KV/wide-column): O(1) log-structured/commit-log append + async replication — designed for high throughput.

## 11. Advantages
- **Horizontal scaling**: partition across commodity nodes; write throughput scales ~linearly (vs relational single-writer).
- **High availability**: replication + partition-tolerant design keep serving during failures (choose A under CAP).
- **Schema flexibility**: documents/dynamic columns accept evolving data without migrations; fast iteration.
- **Specialized performance**: O(1) key access; write-optimized log-structured storage; columnar scan efficiency; graph traversal expressiveness.
- **Simpler operations for narrow workloads**: no joins/transactions/planner to reason about for pure key-driven workloads.
- **Reduced latency (PACELC)**: eventual consistency → local/async replication → lower read/write latency at normal operation.

## 12. Disadvantages
- **No general joins/ACID**: multi-item atomicity must be designed by the application (denormalization, compensation); consistency is eventual or application-managed.
- **Application burden**: the programmer implements constraints, referential integrity, and consistency — bugs move to the app layer.
- **Query generality loss**: no arbitrary SQL; analytics/BI over KV/document data needs extra pipelines or a warehouse.
- **Operational complexity at scale**: consistent hashing, replica repair, tombstone/compaction management (Cassandra), vector clocks.
- **Eventual consistency pitfalls**: stale reads, lost updates (unless last-write-wins is acceptable), concurrent-write conflicts needing reconciliation.
- **Ecosystem maturity**: fewer relational-grade tools, less standardized SQL/querying, vendor-specific semantics.

## 13. Interview Questions
1. **Q: Why do NoSQL databases exist?** A: To serve workloads relational engines handle poorly at scale — horizontal write scaling, high availability through partitions, flexible/specialized data models, and latency under replication — by relaxing ACID/relational guarantees (the CAP/PACELC trade).
2. **Q: Name the four NoSQL families and a system for each.** A: Key-value (Redis, DynamoDB, Memcached), document (MongoDB, CouchDB), wide-column (Cassandra, HBase) and columnar analytics (ClickHouse, Vertica), graph (Neo4j, Neptune).
3. **Q: What is CAP?** A: During a network partition (P), a distributed system can guarantee Consistency (every read sees the latest write) or Availability (every request returns) but not both. It's about *behavior during a partition*, not a general pick-any-two.
4. **Q: TRICKY: "Consistency" in CAP vs ACID consistency?** A: Different words. CAP consistency = linearizability (all replicas see writes in the same order). ACID consistency = the DB maintains integrity constraints (transactions move a valid state to a valid state). They are orthogonal; a NoSQL system can be "CAP-consistent" per-key yet not support ACID transactions.
5. **Q: What is PACELC?** A: Abadi's extension: If there's a Partition, choose Availability or Consistency; Else (normal operation), choose Latency or Consistency. It captures the *always-on* cost: even without partitions, strong consistency requires synchronous replication → higher latency.
6. **Q: What is ACID vs BASE?** A: ACID = atomicity, consistency, isolation, durability — strong guarantees for multi-statement transactions. BASE = basically available, soft state, eventual consistency — the relaxed model: data may be briefly inconsistent but converges; availability and scale are prioritized.
7. **Q: What is eventual consistency?** A: A consistency model where replicas may temporarily disagree but, given no further writes and enough time, converge to the same value. Common in DynamoDB/Cassandra; implemented via async replication, vector clocks/versioning, read-repair.
8. **Q: TRICKY: When is eventual consistency acceptable?** A: When the *latest value is not required immediately* — e.g., social feeds, likes/views counters, session TTL, metrics — and a stale read (seconds old) is harmless. When a read must reflect the latest write (payment balance, inventory deduction), use strong/consistent reads or a transactional DB.
9. **Q: What is "schemaless" really?** A: Schema is enforced at *write time by the application* rather than by the DB at DDL time. The DB stores whatever JSON/BSON/document arrives; the app must handle variance (missing fields, type changes). It's flexibility, not "no design" — modeling moves to the code.
10. **Q: When would you choose NewSQL (CockroachDB, Spanner, TiDB) over NoSQL?** A: When you need SQL semantics *and* horizontal scaling — real transactions across nodes, joins, strong consistency (e.g., finance, e-commerce inventory) — and are willing to pay consensus overhead (multi-Paxos/Raft, synchronous replication) for it.
11. **Q: PR: Is "NoSQL" faster than SQL?** A: Misleading question — different trade-offs. NoSQL wins on *specific* patterns: O(1) key lookups, write-heavy append (Cassandra), columnar scans (ClickHouse), graph traversal. For general OLTP with joins and transactions, relational engines are competitive or better. "Faster" depends entirely on workload.
12. **Q: What does "last-write-wins" (LWW) mean?** A: When concurrent writes conflict, the write with the newest timestamp wins (DynamoDB/Cassandra default). Simple, available, but can *lose* updates (a stale writer can overwrite a newer value if its clock is ahead) — need clock discipline or versioned conflict handling for correctness.
13. **Q: What is read repair?** A: During a read with consistency level QUORUM (Cassandra) or when reading inconsistent replicas (DynamoDB), the system detects stale replicas and rewrites the latest value to them — a background mechanism that makes eventual convergence happen on the *read* path too.
14. **Q: TRICKY: A NoSQL system that is "CAP-consistent" — can it still lose data?** A: Consistency ≠ durability. A strictly-consistent system can still lose acknowledged writes if the replica acknowledged the write dies before replication (async replication); that's a *durability* concern (Part 06), orthogonal to CAP's consistency. Durability needs synchronous replication/quorum acks.
15. **Q: How do NoSQL systems handle partitioning?** A: Consistent hashing (DynamoDB, Cassandra, Redis Cluster) places each key on a node via hash; range partitioning (HBase) orders by key for range scans. Partition count and replication factor are configurable; rebalancing happens as nodes join/leave.
16. **Q: PRODUCTION: "Just use MongoDB" is bad advice for what workload?** A: High-write transactional workloads (payments, inventory), complex multi-entity analytics, or any workload needing joins/ACID across documents — a relational (or NewSQL) engine fits better. MongoDB shines for flexible-schema, per-document CRUD at scale.
17. **Q: What is the "join problem" in NoSQL?** A: Documents/items don't have arbitrary join ability; related data is *denormalized* (embedded) or looked up separately (application-side joins). This trades query power for scale and simplicity but pushes consistency of related data to the app.
18. **Q: TRICKY: Does schemaless mean faster migrations?** A: Yes, in the sense of *no blocking DDL* — adding a field is free. But it shifts the migration cost to read-time code (handle old and new shapes) and can hide schema drift until runtime errors. There's a trade; the "faster" claim is true only for certain kinds of change.

## 14. Follow-Up Questions
1. **Q: What is a vector clock and why do NoSQL systems use it?** A: A versioning structure tracking which replica incrementally modified a value; used to detect and reconcile concurrent writes (causality) instead of naively overwriting. DynamoDB/Cassandra use version metadata to let clients/apps resolve conflicts.
2. **Q: What is consistent hashing?** A: Keys hash into a circular key-space; each node owns an arc of the circle; adding/removing a node only remaps the arc's keys (O(N) rebalance → O(1/m) local). Reduces rebalancing compared to modulo hashing — why KV/wide-column stores use it.
3. **Q: What is the "hot key" problem?** A: A few keys get disproportionate traffic (a celebrity's profile), overloading the owning partition/node. Mitigations: replica reads, request splitting/caching, partition-by-fanout, or denormalization.

## 15. Coding Example
```python
# Redis (key-value): cache + session
import redis
r = redis.Redis(decode_responses=True)
r.setex("session:user42", 3600, '{"name": "Ana"}')   # TTL 1h
r.incr("views:article:7")                             # counter (O(1))
print(r.get("session:user42"))
```
```js
// MongoDB (document): flexible schema + query
db.products.insertOne({
  _id: ObjectId(), sku: "P100", price: 999,
  specs: { color: "black", weight: "1.2kg" },   // arbitrary nested doc
  tags: ["electronics", "new"]                   // array
});
db.products.find({ "specs.color": "black" });    // nested-field index
db.orders.aggregate([                             // aggregation (emulated join)
  { $match: { status: "paid" } },
  { $lookup: { from: "products", localField: "sku",
               foreignField: "sku", as: "product" } }
]);
```
```sql
-- Cassandra (wide-column): write-heavy time series
INSERT INTO metrics (device_id, ts, temp) VALUES ('dev-1', toTimestamp(now()), 21.4);
SELECT * FROM metrics WHERE device_id = 'dev-1'
  AND ts > '2026-08-01' AND ts <= '2026-08-02';   -- clustering range scan
-- consistency level choice
CONSISTENCY QUORUM;
```
```cypher
// Neo4j (graph): find friends-of-friends
MATCH (me:User {id: 'u1'})-[:FRIENDS_WITH]->()-[:FRIENDS_WITH]->(foaf:User)
WHERE NOT (me)-[:FRIENDS_WITH]->(foaf) AND foaf <> me
RETURN DISTINCT foaf.name;
```

## 16. Industry Usage
- **Redis**: cache, sessions, rate limiting, queues — used by nearly every large web company (its 2024 licensing shift to RSAL/AGPL for new versions sparked forks like Valkey).
- **DynamoDB**: AWS's flagship NoSQL — the paper behind it (2007) *invented* eventual-consistency-via-quorum and read repair; powers massive serverless backends.
- **MongoDB**: M2M/content/catalog workloads across startups and enterprises; the `$lookup` pipeline addresses its join gap.
- **Cassandra**: powering messaging/telemetry at Apple, Netflix (viewing metadata), Discord — write-heavy, multi-DC, LWW.
- **ClickHouse/Vertica/Redshift**: analytics/OLAP — columnar storage is the standard for big aggregations.
- **Neo4j/Neptune**: fraud, social, knowledge graphs — LinkedIn-style networks and financial-services fraud rings.
- **NewSQL (Spanner, CockroachDB, TiDB)**: "SQL + horizontal scale + strong consistency" — Spanner's TrueTime, Cockroach's Raft-based design.

## 17. References
- Brewer, "CAP Twelve Years Later" (2012): how the rule is misunderstood and how it actually applies.
- Abadi, "Consistency Tradeoffs in Modern Distributed Database System Design" (2012) — PACELC.
- Gilbert & Lynch, "Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services" (2002).
- DeCandia et al., "Dynamo: Amazon's Highly Available Key-value Store" (2007) — the origin paper.
- Lakshman & Malik, "Cassandra — A Decentralized Structured Storage System" (2010).
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 24 (NoSQL) & Ch. 25 (Big Data).
- MongoDB docs: https://www.mongodb.com/docs/ ; Cassandra docs: https://cassandra.apache.org/doc/latest/ ; Neo4j Cypher manual: https://neo4j.com/docs/cypher-manual/current/

## 18. Cheat Sheet
- 4 families: KV (Redis/DynamoDB), document (MongoDB), wide-column/columnar (Cassandra/ClickHouse), graph (Neo4j).
- CAP: during partition, pick C or A (not both). PACELC: else pick latency or consistency.
- ACID (relational) vs BASE (NoSQL): basically available, soft state, eventual consistency.
- KV = O(1) by key; document = flexible schema, no joins; wide-column = write-heavy, LWW, partition key + clustering range; columnar = big scans; graph = traversal/paths.
- Eventual consistency: replicas converge; stale reads OK for feeds/counters, not for balances.
- LWW = newest timestamp wins — simple, can lose updates.
- Consistent hashing → minimal rebalance; hot keys → partition imbalance.
- Read repair / quorum / hinted handoff = convergence mechanisms.
- NewSQL = SQL + scale + strong consistency (Spanner, CockroachDB, TiDB).
- "Faster" is workload-specific, not a family property.

## 19. Quiz
1. Which family is DynamoDB? a) graph b) key-value c) columnar d) document → **b**
2. CAP applies: a) always b) during partitions c) only to SQL d) never → **b**
3. ACID consistency vs CAP consistency are: a) same b) different concepts c) opposites d) synonyms → **b**
4. PACELC adds: a) the latency cost outside partitions b) availability c) sharding d) encryption → **a**
5. BASE stands for: a) Balanced, Atomic, Sync, Efficient b) Basically Available, Soft state, Eventual consistency c) Batch, Atomic, Serial, Eager d) none → **b**
6. Last-write-wins can: a) lose updates b) always be correct c) replace 2PC d) ensure integrity → **a**
7. Consistent hashing minimizes: a) reads b) rebalancing on node changes c) writes d) TTL → **b**
8. NewSQL gives you: a) SQL + scale b) scale only c) no consistency d) graphs → **a**

## 20. Flashcards
- **Q: 4 NoSQL families?** → **A:** KV, document, wide-column, graph.
- **Q: CAP says?** → **A:** During a partition, choose consistency or availability.
- **Q: PACELC adds?** → **A:** Else (no partition), choose latency or consistency.
- **Q: BASE?** → **A:** Basically available, soft state, eventual consistency.
- **Q: KV access complexity?** → **A:** O(1) by key.
- **Q: Document stores lack?** → **A:** General joins (denormalize or aggregate).
- **Q: Cassandra sweet spot?** → **A:** Write-heavy, always-available, LWW, time series.
- **Q: Graph stores make what first-class?** → **A:** Relationships (nodes + edges).
- **Q: Eventual consistency example?** → **A:** Feeds/counters tolerate stale reads.
- **Q: NewSQL?** → **A:** SQL + horizontal scale + strong consistency.

## 21. Revision
NoSQL = family of systems relaxing relational/ACID guarantees for scale, availability, and specialized models. Four families (KV/document/wide-column-columnar/graph) each optimize a specific access pattern. CAP governs partition behavior (C or A); PACELC governs the normal-operation latency/consistency cost. BASE vs ACID frames the guarantee spectrum. Practical read: key-driven O(1) workloads → KV; flexible objects, no joins → documents; write-heavy always-available telemetry → Cassandra; big scans → columnar; relationship-heavy → graph; need SQL+scale+ACID → NewSQL. This chapter sets up the family-by-family sections next.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Why do NoSQL DBs exist?" | 1, 2, 13 |
| "Name the families + examples." | 2, 13 |
| "Explain CAP / PACELC." | 2, 7, 13 |
| "ACID consistency vs CAP consistency." | 7, 13 |
| "What is eventual consistency?" | 7, 13 |
| "When is eventual consistency OK?" | 13 |
| "Is NoSQL faster than SQL?" | 13 |
| "What is last-write-wins?" | 13 |
| "When use NewSQL?" | 4, 13 |
| "What is schemaless really?" | 8, 13 |
