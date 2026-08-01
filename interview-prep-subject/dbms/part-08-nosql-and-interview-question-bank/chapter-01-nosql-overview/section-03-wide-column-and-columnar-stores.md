# Wide-Column & Columnar Stores

> **TL;DR**: Wide-column stores (Cassandra, HBase, Scylla) model rows with dynamic column families partitioned and ordered by a composite key, trading general queries for write throughput, always-on availability, and tunable (often LWW) consistency — best for telemetry, messaging, and time-series; columnar stores (ClickHouse, Vertica, Redshift) store data column-by-column to scan billions of rows for analytics — best for OLAP aggregation.

## 1. Why Does This Exist?
Two different workloads break the relational model at scale, and both are served by "column-oriented" designs:
- **Write-heavy, always-available workloads** (telemetry ingestion, messaging logs, IoT sensors, feed/event streams): millions of inserts/second that *must not block* on coordination, must survive node failures, and are read by key/time-range later. Cassandra/HBase exist for this: log-structured, LWW, no locks on the write path, partition across many nodes.
- **Analytical scans** (data warehouses, BI dashboards, "sum sales by region over 2 years"): relational row stores read whole rows — including columns you don't need — making billion-row scans slow and I/O-bound. Columnar stores (ClickHouse/Vertica) keep each column in its own file/segment, so a query touches only the columns it needs, and columnar compression + vectorized execution make scans order-of-magnitude faster.
The two are often confused because both are called "columnar" — but wide-column (Cassandra) is a *row-ordered, column-family* write store, while pure columnar (ClickHouse) is a *column-oriented* read store. This section separates them precisely.

## 2. How Does It Work?
**Wide-column (Cassandra, HBase, Scylla)**:
- Data model: `(partition_key, clustering_columns, ...non-key columns)`; rows grouped into partitions (by partition key hash) and ordered within a partition by clustering columns.
- Write path: append-only commit log + in-memory memtable → periodic flush to immutable SSTables (log-structured merge tree); compactions merge SSTables in the background. No in-place updates, no row locks → concurrent writes don't block.
- Replication/consistency: token range partitioning (consistent hashing); configurable replication factor and per-query consistency level (`ONE`, `QUORUM`, `LOCAL_QUORUM`, `ALL`); LWW on conflict; read repair + hinted handoff for convergence.
- Query language: CQL (SQL-like, but *only* equality on partition key + range on clustering columns — no joins, no arbitrary filters without an index).
**Columnar (ClickHouse, Vertica, Redshift)**:
- Storage: each column stored in separate compressed files/segments (not rows); "late materialization" reads only needed columns.
- Query: vectorized (SIMD) execution over column chunks; projections/min-max indexes per block; `GROUP BY`/aggregation optimized; part/partition pruning by date.
- Scale: massively parallel across nodes (MPP); `MERGE`/compaction of immutable parts.

## 3. When Is It Used?
**Cassandra/HBase (wide-column, write-heavy)**:
- Telemetry/metrics ingestion (IoT, APM) — millions of writes/sec, read by device+time window.
- Messaging systems (chat/notification inboxes) — partition by user.
- Event sourcing / audit logs / activity feeds.
- Time-series (sensor data, network monitoring) — partition by device, cluster by timestamp.
- Global multi-datacenter apps needing availability + LWW (e.g., counters, "last seen").
**ClickHouse/Vertica/Redshift (columnar, OLAP)**:
- Data warehouses and BI dashboards (aggregations over billions of rows).
- Log analytics (query engine on top of collected logs).
- Financial/operational reporting, ad-hoc analytics on large fact tables.
- Time-series analytics (rollups) as opposed to per-sensor point reads.
- Interviews: "Cassandra vs MongoDB?", "columnar vs row store?", "why is ClickHouse fast at aggregations?", "write path in Cassandra".

## 4. Why Wasn't Another Approach Chosen?
- *Relational (OLTP) for telemetry writes*: single-writer bottleneck + row locks + index maintenance per insert make high-throughput ingestion painful; relational is read/transaction-oriented. Cassandra's log-structured append + LWW removes coordination from the write path.
- *Document store (MongoDB) for wide-column*: Mongo shards documents but maintains B-tree indexes and per-document overhead; Cassandra's partition/clustering model *guarantees* ordered access within a partition and a lock-free write path — better for time-series/telemetry. Mongo is better when you need rich queries and flexible schemas.
- *Row-store for analytics*: reading `SUM(sales)` over 10^9 rows forces a row store to read every row fully (all columns) — columnar reads one column. The I/O gap is 10-100x; that's why warehouses went columnar.
- *In-memory analytics only*: doesn't scale past RAM for historical scans; columnar balances disk + compression + vectorization for disk-resident analytics.
- *NewSQL for everything*: brings SQL+transactions but the consensus overhead (Raft) slows the write path — defeats the "write everything, fast, no locks" use case; NewSQL is for transactional workloads that also need scale.

## 5. Intuition
**Wide-column** is like a **warehouse with a perfect filing rule**: everything for one customer (partition key) goes in one drawer, sorted by date (clustering), and the drawers are distributed across many warehouses by hashing the customer name. When a new order arrives, a clerk just *drops the slip on top of the drawer's pile* (append to memtable/SSTable) — no re-typing the whole ledger, no locks, no waiting; occasionally a janitor merges the pile (compaction). If the power blips and two clerks recorded the same order with different timestamps, the newest one wins (LWW). **Columnar** is a **reference library that filed each fact-type in its own hallway**: "all the dates" in Hall A, "all the amounts" in Hall B, "all the region codes" in Hall C — compressed dictionaries per hall. To compute "total amount by region," you only walk Halls B and C, ignoring everything else, and you read them in parallel, taking huge leaps (vectorized). The row-store library filed each book with all its facts bound together (row-by-row), so you'd flip every page of every book to find the amounts.

## 6. Real-World Analogy
A **power-grid's smart meters (wide-column)**: every meter (partition key) streams a reading every minute, forever — write volume is enormous and must never stop (availability), each meter's readings must be retrievable in time order ("last hour of meter 7"), and if two data-centers record a reading, the newest wins (LWW). The relational approach (one massive table with a `meter_id, ts` index, transactions on every insert) would drown in index maintenance and lock contention at this write rate; Cassandra's append-only, partition-then-order model is literally shaped for it. Now the **utility's monthly billing analytics (columnar)**: "total consumption by tariff across all meters, by month" — you need *only* the consumption and tariff columns of 2 billion readings. The row store reads every reading's full row (voltage, phase, timestamp, quality, consumption, tariff) — columnar reads exactly two columns, compressed, and answers in seconds. Same data, two different physical layouts — one for the write storm, one for the analytic scan.

## 7. Formal Definition
**Wide-column store**: row-oriented (per partition) log-structured database where rows are identified by `(partition_key, clustering_key)`; columns may vary per row ("column families"); writes append to a commit log + memtable and flush to immutable SSTables (LSM tree), merged by compaction; consistency tunable per query (ONE/QUORUM/ALL); conflicts resolved by LWW (timestamped) or user conflict resolution. Queries restricted to partition-key equality + clustering range.
**Columnar store**: storage organized per column (each column's values stored contiguously in compressed, min/max-indexed blocks); query execution is vectorized (SIMD) and prunes blocks by column min/max; optimized for scan-heavy aggregations (`GROUP BY`, `SUM`, `COUNT`) over large fact tables; MPP distribution across nodes.
**Key contrast**: wide-column optimizes the **write** path + point/range reads; columnar optimizes **scan/aggregation** reads. They are not interchangeable — Cassandra is not fast at ad-hoc analytics; ClickHouse is not a write-anytime, LWW, single-row-update store.

## 8. Example
**Wide-column — Cassandra schema (time series):**
```sql
CREATE TABLE metrics (
  device_id  text,
  ts         timestamp,
  temp       float,
  humidity   float,
  PRIMARY KEY (device_id, ts)          -- partition by device, order by ts
) WITH CLUSTERING ORDER BY (ts DESC);
-- Write: millions/sec, no locks, LWW
INSERT INTO metrics (device_id, ts, temp) VALUES ('dev-7', toTimestamp(now()), 21.4);
-- Read: within one partition, range on clustering key
SELECT temp, humidity FROM metrics
 WHERE device_id = 'dev-7' AND ts > '2026-08-01' AND ts <= '2026-08-02';
-- Index for non-key queries (a "secondary index" — use sparingly)
CREATE INDEX ON metrics (temp);
```
**Columnar — ClickHouse (analytics):**
```sql
CREATE TABLE events (ts DateTime, region LowCardinality(String), amount UInt32)
ENGINE = MergeTree PARTITION BY toYYYYMM(ts) ORDER BY (region, ts);
-- Scan only 2 columns; partition pruning skips old months
SELECT region, sum(amount) FROM events
 WHERE ts >= '2026-01-01' GROUP BY region ORDER BY region;
-- Vectorized, compressed: seconds over billions of rows
```

## 9. Internal Working
1. **Cassandra write path**: append to commit log (durable) → write to in-memory memtable → memtable flushes to SSTable when full (sorted, immutable) → background compaction merges SSTables and reclaims tombstones. Deletes are tombstones (marks), not physical removals until compaction.
2. **Cassandra partitioning**: `murmur3(partition_key)` → token ring; each node owns a token range; replication factor N places copies on the next N nodes; coordinator sends write to all replicas (or QUORUM); hinted handoff stores a missed write to replay later; read repair fixes stale replicas on read.
3. **Consistency math**: with RF=3, `QUORUM` = 2 nodes. Write QUORUM + Read QUORUM ⇒ overlap ≥1 ⇒ strong read (if both are quorum). `LOCAL_QUORUM` bounds to one DC; `ONE` = eventual (fast).
4. **ClickHouse**: MergeTree stores immutable parts per partition; each part stores columns as compressed blocks with min/max index; `ORDER BY` defines the primary key → sparse primary index (blocks, not rows); queries use vectorized evaluation (`AVX`), move-to-front/generic compression, and prune parts by partition + min/max. `SELECT` aggregates directly on compressed columnar data without materializing rows.
5. **MVCC/logs**: neither is ACID-transactional across rows; Cassandra has no multi-row transactions (use batch with LWT for conditional ops); columnar stores append-only/immutable parts + `ALTER`/merge — no row-level concurrency.

## 10. Time Complexity
- **Cassandra write**: O(1) amortized (commit-log append + memtable insert; no random I/O); LSM flush/compaction amortized O(1). Write throughput scales ~linearly with nodes.
- **Cassandra read (partition + range)**: O(log(#SSTables) + k) with a merge across SSTables; expensive if many SSTables (compaction lag). Point read by partition key ≈ O(log n) hashing + merge.
- **Cassandra query *without* partition key**: full cluster scan (scatter) — O(all data) — the #1 mistake.
- **Columnar scan**: O(bytes of *needed* columns) — with compression, ~10-100x less I/O than row store; aggregation cost O(rows × needed cols). Min/max + partition pruning skip blocks/parts.
- **Vectorized execution**: ~GB/s to tens of GB/s per node on wide servers.

## 11. Advantages
**Wide-column (Cassandra)**:
- **Write throughput at scale**: lock-free append path, linear horizontal scaling.
- **High availability**: no single writer; partition-tolerant; multi-DC replication.
- **Ordered access within partition**: time-series reads in O(range) without a sort.
- **Tunable consistency**: ONE→QUORUM→ALL per query (PACELC dial).
- **Survives node failures**: hinted handoff, read repair, gossip-based failure detection.
**Columnar (ClickHouse/Vertica)**:
- **Dramatically faster analytic scans**: only needed columns read; compression; SIMD.
- **Partition/min-max pruning**: skip whole months/blocks.
- **Massively parallel aggregation**: MPP across nodes; sub-second BI over billions of rows.
- **Compression ratios** 5-50x on repetitive columns (dates, enums, region codes).

## 12. Disadvantages
**Wide-column (Cassandra)**:
- **No joins, no arbitrary queries**: any non-partition-key filter = full scan or secondary index; no SQL generality.
- **LWW data loss**: concurrent conflicting writes can silently lose the older one; counters/updates need care.
- **No multi-row transactions**: atomicity must be designed (batches + LWT for limited cases).
- **Operational complexity**: compaction/GC pressure, tombstone buildup, tuning (memtable/SSTable sizes, repair), hot partitions on skewed keys.
- **Schema-ish rigidity**: column families are dynamic but modeling mistakes (bad partition keys) are expensive to fix.
**Columnar (ClickHouse)**:
- **Not a general OLTP/CRUD store**: no point-updates, limited transactions, not for application backends.
- **High write amplification on frequent small writes** (batch is the norm; real-time single-row ingest is costly).
- **Sub-second single-row lookups poor** (optimized for scans, not point gets).
- **Memory-heavy for some operations**; tuning for workloads beyond simple analytics.

## 13. Interview Questions
1. **Q: Cassandra vs MongoDB — when each?** A: Cassandra: write-heavy, ordered-time-range, always-available, LWW, no rich queries needed (telemetry/messaging). MongoDB: rich queries (nested/array/`$lookup`), flexible schemas, per-document CRUD, but single-writer-per-shard and index-maintenance write overhead. Cassandra is a *write* store; Mongo is a *document query* store.
2. **Q: What is a partition key vs clustering key?** A: Partition key decides *which node(s)* hold the row (hashing); clustering key decides *order within the partition*. A point read needs the full partition key; range scans use clustering columns. Both make up the primary key.
3. **Q: TRICKY: What happens if you query Cassandra by a non-key column?** A: Without a secondary index or a `ALLOW FILTERING`, the query is rejected; with one, it's a cluster-wide scan (slow). Design your model so queries *always* start from the partition key — the "query-driven" modeling rule.
4. **Q: How does Cassandra achieve high write throughput?** A: Log-structured: commit-log append + memtable (in-memory) → batched immutable SSTable flushes; no in-place updates, no locks, no B-tree index maintenance per insert; LSM compaction merges in the background. Writes are O(1)-ish appends that scale horizontally.
5. **Q: What is LSM (log-structured merge tree)?** A: The storage structure: a durable commit log, in-memory memtable(s), and immutable sorted SSTables with background compaction. Optimizes writes (sequential appends) at the cost of read cost across multiple SSTables — the write-heavy design behind Cassandra/HBase/Scylla.
6. **Q: What are the consistency levels in Cassandra?** A: `ONE` (fast, eventual — one replica acked), `QUORUM` (majority — strong when read+write both QUORUM with overlapping nodes), `ALL` (strongest, slowest, least available), `LOCAL_*` variants (single DC). It's the PACELC dial: pick per-query.
7. **Q: How does LWW (last-write-wins) work and what's the risk?** A: Conflicting writes to the same key are resolved by the newest timestamp (client-supplied). Risk: clock skew — a stale writer with a *newer* clock can overwrite a fresher value; and concurrent increments lose updates. Mitigations: use counters/atomic ops, or reconcile via versions at the app.
8. **Q: TRICKY: Cassandra "delete" is not a delete?** A: Deletes write *tombstones* (markers with TTL) that suppress the old value until compaction physically removes them. Sudden mass deletes create tombstone storms → wide reads/slow queries. Keep tombstones small and time-bounded (TTL them).
9. **Q: What is a hot partition and how do you fix it?** A: A partition key with disproportionate traffic (a celebrity user, a heavily-used device) overloads its node. Fixes: add a hash/random suffix to the partition key (fan-out), split the data by sub-key, or use secondary indexes/replicas — but you can't "shard" a single hot key further without model changes.
10. **Q: Columnar vs row store — the core difference?** A: Row store keeps all columns of a row together (good for point CRUD, one row's full tuple at once); columnar keeps each column's values together (good for scans: read only needed columns, compress repetitive columns, vectorize). Pick by workload: OLTP → row, OLAP → columnar.
11. **Q: Why is ClickHouse fast at `GROUP BY` over billions of rows?** A: Only needed columns are read (I/O cut), columns are compressed (dictionaries, delta) reducing bytes, min/max + partition pruning skip blocks, and execution is vectorized (SIMD) over column chunks — plus MPP across nodes.
12. **Q: TRICKY: Is Cassandra a "columnar" database?** A: No — that's the naming trap. Cassandra is *row-ordered* (a row is grouped by partition, columns stored per-row) and optimized for *writes* and point/range reads; "columnar" refers to column-oriented *scan* stores like ClickHouse. Same prefix, opposite workloads.
13. **Q: When would you pick Cassandra over a relational time-series design?** A: When insert rate exceeds a single-writer node, when you need 24x7 availability across datacenters, when reads are per-key + time-range (no ad-hoc joins), and when LWW/eventual consistency is acceptable. For SQL + transactions + ad-hoc analytics, relational (or NewSQL) stays the right call.
14. **Q: What is `ALLOW FILTERING` and why is it dangerous?** A: A Cassandra flag forcing an arbitrary query as a cluster-wide scan; it works but can hammer the cluster — a warning sign your data model doesn't match the query. Design the model so it's unnecessary.
15. **Q: How does ClickHouse handle real-time single-row inserts?** A: Poorly at high frequency — each insert creates a part (flush + merge); batch inserts (`INSERT INTO ... SELECT` / `INSERT ... VALUES` in bulk) amortize the cost. ClickHouse is a batch/analytics engine, not an OLTP row writer.
16. **Q: PR: Cassandra read latency crept up. Possible causes?** A: (1) Too many SSTables per partition (compaction lag) → tune compaction strategy; (2) tombstone buildup → tombstone storms; (3) hot partitions/skew; (4) `CL.ONE` reads fetching stale then read-repair; (5) network/gossip or node imbalance. Diagnose with `nodetool` (tpstats, cfstats) before tuning.

## 14. Follow-Up Questions
1. **Q: What is hinted handoff?** A: When a replica is down during a write, the coordinator stores the write locally ("hint") and replays it when the replica returns — raising write availability without sacrificing much consistency.
2. **Q: What are the compaction strategies?** A: SizeTiered (merge similar-sized SSTables — high throughput, more read amplification), Leveled (maintain level tiers — lower read amplification, more writes), TimeWindow (time-series: compact per time window). Pick by read/write balance and data shape.
3. **Q: What is Scylla?** A: A C++ rewrite of Cassandra's protocol with a shard-per-core design (no CPU contention on a JVM), claiming 10x throughput per node while staying wire-compatible with CQL.

## 15. Coding Example
```sql
-- Cassandra: modeling a messaging inbox (partition per user, order by ts)
CREATE TABLE inbox (
  user_id  text,
  msg_ts   timestamp,
  from_id  text,
  body     text,
  PRIMARY KEY (user_id, msg_ts)
) WITH CLUSTERING ORDER BY (msg_ts DESC);

INSERT INTO inbox (user_id, msg_ts, from_id, body)
VALUES ('u42', toTimestamp(now()), 'u7', 'hi');

-- Query-driven: always start with partition key
SELECT * FROM inbox WHERE user_id = 'u42'
  AND msg_ts > toTimestamp(now() - 86400);

-- Conditional write (LWT) for uniqueness — limited transactions
INSERT INTO users (user_id, email) VALUES ('u42', 'a@x.com')
  IF NOT EXISTS;
```
```sql
-- ClickHouse: analytics over telemetry
CREATE TABLE metrics_daily (
  device_id  String,
  day        Date,
  value      Float64
) ENGINE = MergeTree
PARTITION BY toYYYYMM(day)              -- prune months
ORDER BY (device_id, day);              -- primary key

-- Batch ingest: 100k rows/insert
INSERT INTO metrics_daily SELECT ... FROM staging;

-- Columnar aggregation: reads only device_id, day, value
SELECT device_id, round(avg(value), 2)
FROM metrics_daily
WHERE day >= '2026-07-01'
GROUP BY device_id
ORDER BY device_id;
```

## 16. Industry Usage
- **Cassandra**: Netflix (viewing metadata, event bus), Discord (messages), Apple (iCloud), Uber — write-heavy, multi-DC, availability-first; the Cassandra paper (Lakshman & Malik 2010) standardized LSM/LWW.
- **HBase**: Bigtable clone powering Facebook messenger (historically), Hadoop ecosystem scans.
- **Scylla**: Dropbox, Zillow — C++ shard-per-core for latency/throughput.
- **ClickHouse**: Cloudflare (analytics/logs), Uber, eBay — the go-to open-source OLAP engine.
- **Vertica/Redshift**: traditional enterprise + cloud warehouses; Redshift columnar on S3-backed MPP.
- **Snowflake/BigQuery**: managed columnar warehouses — same columnar principle behind the SQL facade.
- **TimescaleDB (time-series relational)**: PostgreSQL extension that competes on the time-series *query* side when you also want SQL/joins.

## 17. References
- Lakshman & Malik, "Cassandra — A Decentralized Structured Storage System" (2010).
- Chang et al., "Bigtable: A Distributed Storage System for Structured Data" (2006) — HBase's model.
- O'Neil et al., "The Log-Structured Merge-Tree (LSM-tree)" (1996).
- ClickHouse docs: https://clickhouse.com/docs (MergeTree, vectorized execution).
- Cassandra docs: https://cassandra.apache.org/doc/latest/ (data modeling, consistency).
- Abadi et al., "Column-Stores vs. Row-Stores" (2008) — the analytical I/O gap.

## 18. Cheat Sheet
- Wide-column = Cassandra/HBase/Scylla: write-heavy, availability, LWW, LSM; row-ordered by partition key, clustering for order.
- Columnar = ClickHouse/Vertica/Redshift/Snowflake: analytic scans, column-only reads, compression, vectorization, pruning.
- Cassandra write path: commit log → memtable → SSTable → compaction (LSM). No locks.
- Model by query: always start with partition key; non-key filters = scan (avoid `ALLOW FILTERING`).
- Consistency levels: ONE (eventual) / QUORUM (strong if W+R overlap) / ALL (strong+slow). LOCAL_* per DC.
- LWW: newest timestamp wins — clock skew + lost updates risk.
- Tombstones: deletes are markers; avoid delete storms.
- Hot partition: skewed key → fan-out with hash suffix.
- Columnar: only needed columns read; min/max pruning; batch inserts; not for point CRUD.
- Time-series: Cassandra for per-sensor writes; ClickHouse for rollup analytics.

## 19. Quiz
1. Cassandra's storage is: a) columnar b) LSM/row-ordered c) B-tree d) in-memory → **b**
2. A point read requires: a) clustering key only b) full partition key c) ALLOW FILTERING d) secondary index → **b**
3. LWW risk: a) nothing b) clock-skew lost updates c) faster reads d) no writes → **b**
4. Tombstones represent: a) deletes b) inserts c) reads d) compactions → **a**
5. Quorum with RF=3 needs: a) 3 nodes b) 2 nodes c) 1 node d) all nodes → **b**
6. Columnar stores win on: a) point CRUD b) analytic scans c) single-row updates d) joins → **b**
7. ClickHouse inserts should be: a) single-row b) batched c) random d) via UPDATE → **b**
8. "Columnar" describing Cassandra is: a) correct b) the naming trap c) irrelevant d) standard → **b**

## 20. Flashcards
- **Q: Cassandra storage engine?** → **A:** LSM (commit log + memtable + SSTables).
- **Q: Partition vs clustering key?** → **A:** Hash-location vs in-partition order.
- **Q: Consistency dial?** → **A:** ONE/QUORUM/ALL per query (LOCAL_* per DC).
- **Q: Deletes in Cassandra?** → **A:** Tombstones until compaction.
- **Q: Non-key query?** → **A:** Cluster scan / ALLOW FILTERING (avoid).
- **Q: Hot partition fix?** → **A:** Fan-out / hash suffix on partition key.
- **Q: Columnar wins on?** → **A:** Scan-heavy analytics (fewer bytes, SIMD, pruning).
- **Q: ClickHouse inserts?** → **A:** Batch (parts flush); not for point CRUD.
- **Q: Row vs column storage?** → **A:** OLTP point access vs OLAP scans.

## 21. Revision
Two "column" names, two workloads: Cassandra/HBase = write-heavy, always-available, LWW, LSM, query-by-partition-key+clustering-range — for telemetry/messaging/time-series *writes*. ClickHouse/Vertica = column-oriented analytic scans — fewer bytes, compression, vectorization, pruning — for OLAP *reads*. Model Cassandra queries around the partition key (non-key queries are scans); dial consistency with ONE/QUORUM/ALL; respect tombstones and hot partitions. Pick the row store for general OLTP with joins/transactions, and these for their specific strengths.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Cassandra vs MongoDB?" | 4, 13 |
| "Partition vs clustering key?" | 7, 13 |
| "How does Cassandra write so fast?" | 9, 13 |
| "What is LSM?" | 9, 13 |
| "Consistency levels?" | 9, 13 |
| "What is LWW and its risks?" | 7, 13 |
| "Tombstones / deletes?" | 13 |
| "Columnar vs row store?" | 1, 13 |
| "Why is ClickHouse fast?" | 9, 13 |
| "Is Cassandra columnar?" | 13 |
