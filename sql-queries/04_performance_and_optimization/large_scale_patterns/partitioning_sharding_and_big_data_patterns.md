# Partitioning, Sharding and Large-Scale SQL Patterns — 100 SQL Interview Q&A

## Q1: What is table partitioning and how do you create a range-partitioned table in PostgreSQL?

**Query:**
```sql
CREATE TABLE orders (
    order_id   BIGSERIAL,
    customer_id BIGINT NOT NULL,
    order_date DATE NOT NULL,
    total      NUMERIC(10,2)
) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2024 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE orders_2025 PARTITION OF orders
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
```
**Explanation:** Partitioning splits one logical table into multiple physical segments (partitions) by a key. Each partition holds a slice of the rows; the parent table is empty and routes every query.

**Alt1:**
```sql
CREATE TABLE orders (
    ...
) PARTITION BY HASH (customer_id);   -- rows spread by bucket(customer_id) % n
```

## Q2: How do you create a LIST partition in PostgreSQL?

**Query:**
```sql
CREATE TABLE events (
    id BIGSERIAL,
    region TEXT NOT NULL,
    payload JSONB
) PARTITION BY LIST (region);

CREATE TABLE events_na PARTITION OF events FOR VALUES IN ('us', 'ca', 'mx');
CREATE TABLE events_eu PARTITION OF events FOR VALUES IN ('de', 'fr', 'es');
CREATE TABLE events_other PARTITION OF events DEFAULT;
```
**Explanation:** LIST partitions hold rows whose key value matches one of an explicit set of values. A DEFAULT partition catches anything not listed.

## Q3: What does PARTITION BY HASH accomplish and when would you choose it over RANGE?

**Query:**
```sql
CREATE TABLE users (
    id BIGINT NOT NULL,
    email TEXT NOT NULL
) PARTITION BY HASH (id);

CREATE TABLE users_p0 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE users_p1 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE users_p2 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE users_p3 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```
**Explanation:** Hash partitioning distributes rows uniformly across a fixed number of partitions, which evens out writes. Use it when there is no natural range (e.g. user IDs) and equal distribution beats ordered scans.

## Q4: How does partition pruning speed up a query in PostgreSQL?

**Query:**
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT sum(total) FROM orders WHERE order_date >= '2024-01-01' AND order_date < '2024-02-01';
```
**Explanation:** The planner compares the WHERE predicate against each partition's bounds and scans only the matching partition(s); the plan shows exactly one partition scanned instead of all of them. Pruning avoids touching irrelevant data.

**Alt1:**
```sql
SET enable_partition_pruning = on;   -- pruning is on by default in modern PG
SELECT count(*) FROM orders WHERE order_date = '2025-06-15';
```

## Q5: What is a common partition key pitfall that defeats pruning?

**Query:**
```sql
-- Wrong: the check is wrapped so the key isn't seen as immutable/plannable
SELECT * FROM orders WHERE date_trunc('month', order_date) = '2024-05-01';

-- Right: sargable predicate
SELECT * FROM orders
WHERE order_date >= '2024-05-01' AND order_date < '2024-06-01';
```
**Explanation:** Predicates must be on the raw partition column. If the `WHERE` filters a function of the partition key (or casts it), the planner cannot prune and scans every partition.

## Q6: How does MySQL create a RANGE-partitioned table?

**Query:**
```sql
CREATE TABLE orders (
    order_id BIGINT NOT NULL,
    order_date DATE NOT NULL,
    total DECIMAL(10,2)
) PARTITION BY RANGE (YEAR(order_date)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```
**Explanation:** MySQL's Oracle-style `VALUES LESS THAN` syntax stores each row in the first partition whose upper bound exceeds the key. `MAXVALUE` catches everything that doesn't fit earlier partitions.

## Q7: What are MySQL HASH and KEY partitioning and how do they differ?

**Query:**
```sql
CREATE TABLE sessions (
    session_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL
) PARTITION BY HASH (user_id) PARTITIONS 8;

CREATE TABLE sessions_key (
    session_id CHAR(36) NOT NULL,
    user_id BIGINT NOT NULL
) PARTITION BY KEY (session_id) PARTITIONS 8;
```
**Explanation:** HASH uses a user-specified column with an integer hash; KEY uses MySQL's own hashing (MD5-based) and is the only option for columns that aren't integers (e.g. CHAR/text). KEY is generally preferred in MySQL because any data type and index type works.

## Q8: How does SQL Server implement partitioning?

**Query:**
```sql
CREATE PARTITION FUNCTION pf_orders (DATE)
    AS RANGE RIGHT FOR VALUES ('2024-01-01', '2025-01-01');

CREATE PARTITION SCHEME ps_orders
    AS PARTITION pf_orders ALL TO ([PRIMARY]);

CREATE TABLE orders (
    order_id BIGINT NOT NULL,
    order_date DATE NOT NULL
) ON ps_orders (order_date);
```
**Explanation:** SQL Server uses a two-object model: a partition function (how rows map to partitions) plus a partition scheme (which filegroup backs each partition). Alignment requires the unique index to include the partition column.

## Q9: How is partitioning declared in Oracle (range, list, hash, composite)?

**Query:**
```sql
CREATE TABLE orders (
    order_id NUMBER,
    order_date DATE
) PARTITION BY RANGE (order_date)
  PARTITIONS 12 (PARTITION p1 VALUES LESS THAN (DATE '2024-01-01'));

CREATE TABLE regs (
    id NUMBER, region VARCHAR2(10), yr NUMBER
) PARTITION BY RANGE (yr) SUBPARTITION BY LIST (region)
  (PARTITION y2024 VALUES LESS THAN (2025)
      (SUBPARTITION y2024_na VALUES ('US','CA'),
       SUBPARTITION y2024_eu VALUES ('DE','FR')));
```
**Explanation:** Oracle supports the same core strategies plus composite (sub-partitioning): a range partition host with list or hash sub-partitions inside it. That gives range pruning for time plus a list/hash spread for locality.

## Q10: Can you create an index on a partitioned table and what types exist (global vs local)?

**Query:**
```sql
-- PostgreSQL: index is created per partition automatically
CREATE INDEX idx_orders_customer ON orders (customer_id);

-- Oracle: local index (one segment per partition)
CREATE INDEX idx_orders_cust_local ON orders (customer_id) LOCAL;

-- Oracle / SQL Server: global index spans partitions
CREATE INDEX idx_orders_cust_global ON orders (customer_id) GLOBAL;
```
**Explanation:** PostgreSQL and MySQL build a partitioned index that is per-partition under the hood (local-style). Oracle lets you explicitly pick LOCAL (cheaper, partition-aligns, dropped with partition) vs GLOBAL (single B-tree, stays useful when partitions are swapped).

**Alt1:**
```sql
-- SQL Server: index aligned via the partitioned scheme, include partition column
CREATE CLUSTERED INDEX cix_orders ON orders (order_date) ON ps_orders (order_date);
```

## Q11: How do you attach a new partition for incoming time-series data?

**Query:**
```sql
-- prepare the table, then attach
CREATE TABLE orders_2026 (LIKE orders INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
ALTER TABLE orders_2026 ADD CONSTRAINT orders_2026_chk
    CHECK (order_date >= '2026-01-01' AND order_date < '2027-01-01');

ALTER TABLE orders ATTACH PARTITION orders_2026
    FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
```
**Explanation:** Instead of inserting into an existing partition, you create a standalone table, validate its data with a CHECK, then attach it. Attach is a fast metadata operation that validates constraints without rewriting the base table.

## Q12: How do you drop or detach an old partition (retention)?

**Query:**
```sql
-- PostgreSQL: detach keeps the table around
ALTER TABLE orders DETACH PARTITION orders_2020;

-- drop the partition + its data instantly
DROP TABLE orders_2020;
DROP TABLE orders_2019;

-- Oracle: drop a partition
ALTER TABLE orders DROP PARTITION p2019;
```
**Explanation:** Dropping an entire partition is O(1) metadata work — it deletes millions of rows without a `DELETE` scan. This is the standard mechanism for time-series retention: delete whole months instead of row by row.

**Alt1:**
```sql
-- MySQL: drop partition by value bounds
ALTER TABLE orders DROP PARTITION p2019;

-- SQL Server: switch out then drop
ALTER TABLE orders SWITCH PARTITION 1 TO orders_archive_2019;
DROP TABLE orders_archive_2019;
```

## Q13: How do you convert a non-partitioned table into a partitioned one?

**Query:**
```sql
-- PostgreSQL: create partitioned parent + migrate
CREATE TABLE orders_new (LIKE orders) PARTITION BY RANGE (order_date);
ALTER TABLE orders RENAME TO orders_old;
ALTER TABLE orders_new RENAME TO orders;

CREATE TABLE orders_2024 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
INSERT INTO orders SELECT * FROM orders_old;
DROP TABLE orders_old;

-- Oracle: single ALTER that reorganizes data into partitions
ALTER TABLE orders MODIFY PARTITION BY RANGE (order_date) ONLINE;
```
**Explanation:** PostgreSQL migrates via create-copy-swap (the ATTACH/validated-constraint path can do it without a full scan). Oracle 12.2+ can repartition in place with `MODIFY PARTITION BY`. Expect a one-time write amplification.

## Q14: When does partitioning help and when does it hurt?

**Query:**
```sql
-- Good: predicates always filter the partition key
SELECT * FROM orders WHERE order_date BETWEEN '2025-01-01' AND '2025-03-31';

-- Bad: no partition-key filter -> every partition scanned + merged
SELECT * FROM orders WHERE customer_id = 42 ORDER BY order_date DESC;
```
**Explanation:** Partitioning helps large tables where queries filter on the partition key, enabling pruning and fast drop-by-partition. It hurts on small tables and when the key never appears in WHERE — you add overhead (keep partitions, per-partition indexes, "append" plans) for no pruning.

**Alt1:**
```sql
-- before partitioning: full scan reads the whole heap
-- after: scan touches ~2/12 monthly partitions
-- benchmark the same query with/without the filter to decide
```

## Q15: How does partition count affect performance and planning?

**Query:**
```sql
-- a handful of large partitions: pruning is trivial
CREATE TABLE events PARTITION BY RANGE (ts);
-- thousands of tiny partitions: planner cost explodes
CREATE TABLE log PARTITION BY RANGE (ts);  -- per-second partitions = bad idea
```
**Explanation:** Each partition adds per-partition statistics, entry in the plan, and index overhead. A few dozen to a few hundred partitions is sweet territory; tens of thousands cause hundreds of sub-plans and worse planning/slow stats collection.

## Q16: What is sharding and how does it differ from partitioning?

**Query:**
```sql
-- Partitioning: one server, table chopped internally
CREATE TABLE orders PARTITION BY RANGE (order_date);

-- Sharding: the same table physically lives on N different database servers
--   shard_db[0..3].orders  -> shard key = customer_id % 4
SELECT * FROM shard_{customer_id % 4}.orders
WHERE customer_id = :cid;
```
**Explanation:** Partitioning splits a table within a single database instance; sharding distributes whole tables (or key-ranges) across separate database servers. Sharding scales out writes and raw storage across machines; partitioning does not.

## Q17: What is horizontal vs vertical sharding?

**Query:**
```sql
-- Horizontal sharding: rows of one table spread by key
--   orders for customer 1..10 on db0, 11..20 on db1, ...
SELECT * FROM db_{customer_id / 10}.orders WHERE customer_id = :cid;

-- Vertical sharding: different tables (or columns) on different servers
--   db_users:  users, profiles
--   db_orders: orders, order_lines
SELECT * FROM db_users.users WHERE id = :uid;
```
**Explanation:** Horizontal sharding partitions rows of the same table by a shard key; vertical sharding splits by table or by column group (hot columns on one server, large blobs on another). Retroarch apps combine both: vertical split first, then shard the widest tables.

**Alt1:**
```sql
-- vertical: move rarely-read wide columns off the hot path
CREATE TABLE users_primary   (id, login, email, created_at);
CREATE TABLE users_profile   (id, avatar_blob, bio, preferences JSONB);
```

## Q18: What makes a good shard key?

**Query:**
```sql
-- high cardinality + high selectivity + even distribution + stable
-- customer_id / tenant_id are classic choices; country codes are poor
CREATE TABLE orders (
    order_id  BIGINT,
    customer_id BIGINT NOT NULL,   -- shard key
    ...
);
-- routing uses the key on every query
SELECT * FROM orders WHERE customer_id = :cid AND order_date >= '2025-01-01';
```
**Explanation:** A good shard key must appear in most queries (so they route to one shard), have high cardinality (no hotspots), distribute evenly, and never change. customer_id/tenant_id win because every business query already filters on them.

## Q19: What is consistent hashing and how does it improve on modulo sharding?

**Query:**
```sql
-- modulo: adding a 5th shard rehashes ~80% of rows
-- consistent hashing: keys map onto a ring of slots; adding a node moves
--   only the keys owned by the nearest successor slot (~1/n fraction)
-- (illustrative hash-ring key ownership, no DDL)
INSERT INTO ring(k, owner) VALUES
  (hash('customer_7')  , 'shard_2'),
  (hash('customer_823'), 'shard_4');
```
**Explanation:** Consistent hashing: keys map onto a hash ring of slots; adding a node only re-owns the keys of its nearest successors, so ~1/n of keys move instead of (n-1)/n. It is why Dynamo-style datastores and Vitess reshards stay cheap during topology changes.

**Alt1:**
```sql
-- vs. modulo: the ring lookup replaces "key % shard_count"
SELECT shard_owner(hash('customer_823'));   -- lookup in the ring table
```

## Q20: What is a hotspot shard key and how do you avoid it?

**Query:**
```sql
-- Bad: low cardinality or skewed -> one shard takes all the writes
--   (e.g. shard on country where 90% of users are US)
-- Mitigation: use a high-cardinality composite or add salt buckets
INSERT INTO users (id, country) VALUES
  (1, 'US'), (2, 'US');   -- both would land on the same US shard

CREATE TABLE users (
    user_id BIGINT,
    bucket  SMALLINT GENERATED ALWAYS AS (user_id % 64) STORED
) PARTITION BY HASH (bucket);   -- salt spreads a hot key across 64 slices
```
**Explanation:** Hotspot keys concentrate reads/writes on one shard (celebrity accounts, a dominant country). Fixes: choose a higher-cardinality key, append a salt/tenant-suffix, or distribute the hot logical entity across buckets and re-merge on read.

**Alt1:**
```sql
-- read side: SELECT ... FROM users WHERE country='US'     -- fans to 64 salted buckets
-- then merge in the coordinator; only the hottest key is salted
INSERT INTO tweets (id, author_id, salt) VALUES ( , 1, (1%64));
```

## Q21: What is a cross-shard query and why is it expensive?

**Query:**
```sql
-- Query that needs data from every shard -> fan-out + gather
-- db0: SELECT customer_id, sum(total) AS t FROM orders WHERE ... GROUP BY customer_id;
-- db1: SELECT customer_id, sum(total) AS t FROM orders WHERE ... GROUP BY customer_id;
-- coordinator: merge/aggregate the per-shard partial rows
SELECT customer_id, sum(t) FROM
   (results_from_all_shards_union_all) GROUP BY customer_id;
```
**Explanation:** A cross-shard query fans out to N shards, each returning partial results, then the coordinator merges/aggregates. Latency is bounded by the slowest shard and any JOIN/GROUP BY across shards moves data over the network.

## Q22: What problems do distributed joins face across shards?

**Query:**
```sql
-- join two sharded tables on the same key = co-located, cheap
SELECT o.id, u.name
FROM orders o JOIN users u USING (customer_id)   -- both sharded by customer_id
WHERE o.customer_id = 42;

-- joining on a different key = must scatter rows across the network
SELECT o.id, p.name
FROM orders o JOIN products p ON o.product_id = p.id;  -- products not sharded by product_id
```
**Explanation:** Joins on the shard key are co-located (rows with the same key live on the same shard) and cheap. Joins on non-shard keys require shuffling — duplicate/route rows between machines — which is why sharded schemas denormalize instead of joining.

## Q23: How do you denormalize to avoid distributed joins?

**Query:**
```sql
-- instead of joining orders->products on every read, store the product
-- name/snapshot on the order row (eventually consistent denormalization)
CREATE TABLE orders (
    order_id     BIGINT,
    customer_id  BIGINT NOT NULL,
    product_id   BIGINT,
    product_name TEXT,          -- copied at write time
    product_price NUMERIC(10,2)
) PARTITION BY HASH (customer_id);
```
**Explanation:** Copy frequently-joined columns into the child record at write time so reads are single-shard. You trade write-time duplication + drift risk for eliminating cross-shard joins — the standard tradeoff in sharded systems.

**Alt1:**
```sql
-- fan-out writes: update the denormalized copy on every shard
-- db0/app code broadcasts: UPDATE orders SET product_name='X' WHERE product_id=7;
```

## Q24: What is the MySQL application-level sharding pattern and its downsides?

**Query:**
```sql
-- app/router picks shard by key; no DB-layer magic
$shard = "db" . (customer_id % 4);
$sql = "SELECT * FROM orders WHERE customer_id = ? AND id = ?";
-- execute($shard, $sql, [$cid, $order_id]);

-- all shards usually have the same schema DDL applied by the deploy pipeline
-- CREATE TABLE orders (...) ;  -- run against db0..db3
```
**Explanation:** The application embeds shard-selection logic and connects to many connections, so schema changes must be pushed to every shard and cross-shard queries must be coded by hand. It's simple, but you maintain routing, migrations, and backup fan-out yourself.

**Alt1:**
```sql
-- router side table: customer_id % 4 -> host, max connections, schema
UPDATE shard_map SET host='db3' WHERE bucket=2;  -- manual failover/rebalance
```

## Q25: How do Vitess and ProxySQL change the MySQL scaling story?

**Query:**
```sql
-- Vitess: transparent sharding on top of MySQL; app talks to vtgate
VSchema:
{
  "tables": {
    "orders": {
      "column_vindexes": [ {"column":"customer_id", "name":"hash"} ]
    }
  }
}
-- app: SELECT * FROM orders WHERE customer_id = 42;  (vtgate routes the shard)

-- ProxySQL: connection-level pool/router / query routing & caching, not a sharder
mysql> SELECT hostgroup_id, comment FROM mysql_replication_hostgroups;
```
**Explanation:** Vitess replaces hand-rolled routing with a vtgate serving layer that does sharding, resharding, and cross-shard scatter automatically. ProxySQL mostly handles pooling, replication-aware routing, and caching in front of MySQL- no data splitting.

**Alt1:**
```sql
-- ProxySQL query cache keeps hot global reads off the replicas
mysql> INSERT INTO mysql_query_rules (match_pattern, cache_ttl) VALUES ('^SELECT region', 300);
LOAD MYSQL QUERY RULES TO RUNTIME;
```

## Q26: How do read replicas help scale reads and what queries go to them?

**Query:**
```sql
-- route read-only traffic to replicas, writes to the primary
--   primary:  INSERT INTO orders ...; UPDATE ...
--   replica1: SELECT * FROM orders_detail_view WHERE account_id = ...;
--   replica2: analytics / reporting batch workloads

-- app-level two-pool config (illustration)
rw:   host=primary,  pool_size=50
ro:   host=replica1, host=replica2, load_balance=round_robin, pool_size=200
```
**Explanation:** Replicas absorb read load (SELECTs, reports, dashboard queries) so the primary spends its capacity on writes. Every write to the primary is replayed on replicas, giving horizontal read scale with near-zero code change.

**Alt1:**
```sql
-- workload split at the SQL level: mark read-only transactions
SET TRANSACTION READ ONLY;      -- routed by pool to a replica
-- heavy analytics: SELECT ... /* ANALYTICS */ ... -- ProxySQL routes to replica
```

## Q27: Why don't read replicas solve write scaling?

**Query:**
```sql
-- all writes still hit the single primary
INSERT INTO orders (...) VALUES (...) ON PRIMARY;   -- serialized by the primary
-- replicas only multiply read capacity; the primary is still one writer
```
**Explanation:** Write scaling needs multiple writers (shards/multi-primary), which is precisely what single-primary replication cannot supply. Partitioning inside one node also does not scale write IOPS — only sharding spreads the write lock/WAL/flush across machines.

**Alt1:**
```sql
-- three primaries each own a key range; replicas attach under each
--   shard_a (pk < 1M), shard_b (1M-2M), shard_c (>2M) --> 3x write throughput
```

## Q28: What is read-after-write consistency and how do you fix it with replicas?

**Query:**
```sql
-- Problem: user posts, then immediately reads -> replica may lag
INSERT INTO posts ... (primary);
SELECT * FROM posts WHERE user_id = :uid;   -- hits stale replica, post missing!

-- Fix 1 (session pinning / single-row): keep that user's reads on primary
if (session.user_id == writer.user_id) route("primary");

-- Fix 2: sticky cookie / updated_at guard
if (last_write_time - replica_lag_estimate < threshold) route("primary");
```
**Explanation:** Replication delay means a query routed to a replica can miss data just written. Pinning the writing user to the primary, using session affinity, or guarding reads with a timestamp are the common mitigations at the cost of load imbalance.

## Q29: What is eventual vs strong consistency at the database layer?

**Query:**
```sql
-- Strong: every read sees the latest committed write
-- (single-node Postgres SERIALIZABLE, after synchronous_commit)
--   SELECT * FROM balance WHERE account=5;  -- always current

-- Eventual: replicas converge over time; may serve stale data during lag
--   (async replication, multi-primary sync)
INSERT INTO balance(account, amount) VALUES (5, -100);  -- primary
SELECT amount FROM balance WHERE account=5;             -- replica: maybe -100, maybe old
```
**Explanation:** Strong consistency guarantees a linearizable/causal view the moment a write acknowledges; eventual consistency accepts brief staleness for lower commit latency and availability. The choice drives replica routing, retries, and conflict handling.

## Q30: What is a read-after-write pattern called read-your-writes, and how do you implement it in app code?

**Query:**
```sql
-- user writes -> must see own write
UPDATE profile SET name = :name WHERE user_id = :uid;   -- hit primary
-- app remembers the write timestamp & forces primary for the same user
SELECT name FROM profile WHERE user_id = :uid AND session_pin = 'primary';
```
**Explanation:** Read-your-writes (read-after-write) means a user always observes their own recent writes. Store `last_write_ts` per user and, when a read for that user arrives faster than the replication lag budget, serve it from the primary (or a quorum-read replica).

**Alt1:**
```sql
-- strong-consistency path for the rare "just wrote" read
if (replica_lag_for(user_id) > 0) {   -- pg_stat / SHOW SLAVE STATUS
   route_to_primary(user_id);
}
```

## Q31: What are denormalized reporting tables / data marts in an OLTP schema?

**Query:**
```sql
-- Build a flattened sales mart from transaction tables each night
CREATE TABLE mart_daily_sales AS
SELECT o.order_date,
       o.customer_id,
       c.name                                     AS customer_name,
       SUM(ol.qty * ol.unit_price)                AS revenue,
       COUNT(DISTINCT o.order_id)                 AS orders
FROM orders o
JOIN order_lines ol ON ol.order_id = o.order_id
JOIN customers  c  ON c.id = o.customer_id
GROUP BY o.order_date, o.customer_id, c.name;

CREATE INDEX idx_mart_date ON mart_daily_sales (order_date, customer_id);
```
**Explanation:** A data mart is a purpose-built, pre-joined, pre-aggregated table for reporting. OLTP stays normalized and fast; the mart trades storage for instant dashboard queries instead of expensive joins over hot tables.

## Q32: Name the OLTP vs OLAP differences and a column store fit.

**Query:**
```sql
-- OLTP: many small row-level ops, indexed lookups, heavy concurrent writes
-- OLAP: huge scans over many rows, few aggregations, big reads

-- Columnar / warehouse: store per column, scan only touched columns
--   Snowflake/Redshift/BigQuery example (illustrative)
CREATE TABLE sales (
  order_id BIGINT   ENCODE AZ64,
  state    VARCHAR  ENCODE LZO
)
DISTSTYLE KEY DISTKEY (customer_id)
SORTKEY (order_date);
```
**Explanation:** OLTP favors row stores with indexes and point writes; OLAP favors columnar storage at high compression where analytics only read needed columns. Exporting/loading a columnar warehouse is the classic "big data" SQL pattern.

## Q33: How do you export an OLTP database to a columnar warehouse (Redshift/Snowflake/BigQuery)?

**Query:**
```sql
-- export from source (Postgres example)
COPY orders TO '/tmp/orders_2025.tsv' WITH (FORMAT 'csv', HEADER true);
-- copy into the warehouse
--   Redshift: COPY orders FROM 's3://bucket/orders_2025' IAM_ROLE 'arn:...' CSV;
--   Snowflake: COPY INTO orders FROM @stage/orders_2025 FILE_FORMAT=(TYPE=CSV);
--   BigQuery: LOAD DATA ... FROM FILES (format='CSV', uris=['gs://...']);
```
**Explanation:** The pattern is extract-to-files, then a parallel bulk load (`COPY`/`LOAD DATA`). Warehouse `COPY` commands parallelize file reads across nodes — far faster than inserting row-by-row from the app.

## Q34: How do you batch-optimize bulk inserts (batch transactions)?

**Query:**
```sql
-- Bad: 100k single-row autocommit inserts (a commit roundtrip each)
INSERT INTO events(ts, msg) VALUES(%s, %s);

-- Good: batch into multi-row statement / one transaction
INSERT INTO events(ts, msg) VALUES (:1,:a), (:2,:b), (:3,:c), ...;  -- ~1-2k rows each

BEGIN;
INSERT INTO events(ts, msg) VALUES ...;
INSERT INTO events(ts, msg) VALUES ...;   -- 100 of these
COMMIT;
```
**Explanation:** Each commit is a fsync + roundtrip; batching amortizes it over thousands of rows. One transaction per 1k-10k rows (dozens to hundreds of multi-row INSERTs per commit) gives a 10-100x write speedup.

**Alt1:**
```sql
-- PostgreSQL: COPY is the fastest path to bulk-load
COPY events(ts, msg) FROM '/tmp/events.tsv' WITH (FORMAT 'csv');
```

## Q35: How do temporal tables support time-series data?

**Query:**
```sql
-- SQL Server system-versioned temporal table
CREATE TABLE sensor_readings (
    sensor_id  INT NOT NULL,
    reading    FLOAT,
    valid_from DATETIME2 GENERATED ALWAYS AS ROW START,
    valid_to   DATETIME2 GENERATED ALWAYS AS ROW END,
    PERIOD FOR SYSTEM_TIME (valid_from, valid_to)
) WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.sensor_history));

-- time-series = as-of query
SELECT * FROM sensor_readings
  FOR SYSTEM_TIME BETWEEN '2025-01-01' AND '2025-01-02'
  WHERE sensor_id = 7;
```
**Explanation:** Temporal tables automatically keep every version of a row in a history table. Time-series queries can scan a full point-in-time window (as-of / between), giving auditing and range analytics without building your own versioning.

**Alt1:**
```sql
-- PostgreSQL: event-table time series, partial indexes per period
CREATE TABLE readings (sensor_id INT, ts TIMESTAMPTZ, value FLOAT)
  PARTITION BY RANGE (ts);
SELECT sensor_id, avg(value) FROM readings WHERE ts >= '2025-06-01' GROUP BY sensor_id;
```

## Q36: What are event tables / append-only streams for large-scale ingestion?

**Query:**
```sql
CREATE TABLE events (
    id      BIGSERIAL,
    ts      TIMESTAMPTZ NOT NULL DEFAULT now(),
    type    TEXT NOT NULL,
    user_id BIGINT,
    payload JSONB
) PARTITION BY RANGE (ts);

CREATE TABLE events_2025_07 PARTITION OF events
    FOR VALUES FROM ('2025-07-01') TO ('2025-08-01');
-- appends only: INSERT + PK (id) via sequence, no UPDATE/DELETE of old rows
```
**Explanation:** Event tables are append-only logs of what happened (clicks, telemetry, orders). They use narrow rows, JSONB payload, and partition-by-time so old segments drop instantly and analytics only scan recent windows.

**Alt1:**
```sql
-- index only the query path; JSONB payload stays unindexed
CREATE INDEX idx_events_type ON events (type, ts) WHERE type IN ('click','view');
```

## Q37: How do you keep hot vs cold data separate (partition by month + archiving)?

**Query:**
```sql
-- hot: last 3 months in an indexed, online partitions range
CREATE TABLE metrics PARTITION BY RANGE (dt);
CREATE TABLE metrics_p2025_08 PARTITION OF metrics
    FOR VALUES FROM ('2025-08-01') TO ('2025-09-01');

-- cold: detach older partitions to a read-only archive / warehouse
ALTER TABLE metrics DETACH PARTITION metrics_p2024_12;
ALTER TABLE metrics_p2024_12 SET (fillfactor=100);  -- read-only after detach
-- optionally move archive to cheaper storage (tablespace)
ALTER TABLE metrics_p2024_12 SET TABLESPACE archive_ts;
```
**Explanation:** Keep the last N months as hot partitions (indexed, online); detach anything older into a read-only archive or export it to the warehouse. Hot queries stay on a tiny dataset while the full history remains safely out of the way.

## Q38: How do you implement pagination across shards without skipping rows?

**Query:**
```sql
-- Naive LIMIT/OFFSET per shard is wrong: (offset * shard_count) needed then worst-case shuffle
--   shard each: SELECT ... ORDER BY id LIMIT 5 OFFSET 10   (gives wrong page)

-- Better: keyset (seek) pagination on a global sort column; fetch N from each shard
--   SELECT ... FROM orders WHERE (customer_id, id) > (:last_cid, :last_id)
--   ORDER BY customer_id, id LIMIT 25  -- run on each shard, merge top-25
SELECT * FROM orders
WHERE (customer_id, id) > (:prev_cid, :prev_id)
ORDER BY customer_id, id
LIMIT 25;
```
**Explanation:** With `LIMIT/OFFSET` each shard pages independently, so page two is not "the overall page two." Keyset pagination passes the last-seen key, every shard returns only what follows it, and the coordinator merges — deterministic and no dropped rows.

**Alt1:**
```sql
-- stable page token: base64(last customer_id, last id) survives re-sharding
SELECT * FROM orders WHERE customer_id > :tok_cid AND id > :tok_id
ORDER BY customer_id, id LIMIT 25;
```

**Alt1:**
```sql
-- Query cache in coordinator: stable page_token = base64(last_cid,last_id)
SELECT * FROM orders
WHERE customer_id > :tok_cid AND id > :tok_id
ORDER BY customer_id, id LIMIT 25;
```

## Q39: Why are UUID keys attractive for sharding and what is the cost?

**Query:**
```sql
-- UUID: globally unique, no coordinator to mint IDs, generated at any shard
INSERT INTO orders (id, customer_id, ...) VALUES (uuid(), 42, ...);
-- costs: 16 bytes, random -> B-tree index bloat, no ordering/locality
--   -> random insert pages = slower reads on that index
-- fix: UUIDv7 (time-ordered) keeps rough chronological locality
SELECT uuid_generate_v7();   -- Postgres pg_uuidv7 / manual v7
```
**Explanation:** UUIDs let any node create collision-free IDs without a central sequence (great for multi-shard inserts). The downside is random order = poor index locality; ordered variants (UUIDv7, snowflake-style, or `id | shard_id` packing) restore it.

**Alt1:**
```sql
-- time-ordered UUIDv7 keeps index locality AND global uniqueness
CREATE TABLE orders (id BYTEA PRIMARY KEY);
INSERT INTO orders (id) VALUES (uuid_generate_v7());
```

## Q40: Sequence vs UUID for sharded primary keys — what would you pick?

**Query:**
```sql
-- Sequence (1,2,3...) : compact 8-byte B-tree, but needs a coordinator or high-low per shard
--   shard_i: id = (i << 48) | (shard_local_seq++)
-- UUID(4): no coordinator, random-locality
-- UUID(7)/snowflake: no coordinator, time-ordered, ~decodable
CREATE TABLE orders (
    id BIGINT DEFAULT (set_sequence_bits(shard, nextval('orders_seq'))),
    customer_id BIGINT
) PARTITION BY HASH (customer_id);
```
**Explanation:** Use sequence+shard-bit embedding when index shape/compactness matters; use UUIDv7/snowflake when you need decentralized ID creation with orderability. Pure random UUIDv4 is usually the wrong trade unless global uniqueness trumps everything.

## Q41: What is the outbox pattern and how does it guarantee reliable async side effects?

**Query:**
```sql
CREATE TABLE outbox (
    id           BIGSERIAL PRIMARY KEY,
    aggregate_id BIGINT NOT NULL,
    event_type   TEXT NOT NULL,
    payload      JSONB NOT NULL,
    created_at   TIMESTAMPTZ DEFAULT now(),
    published_at TIMESTAMPTZ
);

-- write business state + outbox row in the SAME local transaction
BEGIN;
  INSERT INTO orders (id, customer_id, total) VALUES (1, 42, 5.00);
  INSERT INTO outbox (aggregate_id, event_type, payload)
      VALUES (1, 'order_created', jsonb_build_object('order_id',1,'total',5.00));
COMMIT;

-- relay: SELECT not-yet-published rows, publish to broker, mark published
SELECT * FROM outbox WHERE published_at IS NULL ORDER BY id LIMIT 100;
```
**Explanation:** The outbox pattern writes the event inside the business transaction, then a relay publishes it to a queue/Broker. Because the DB commit and the event are atomic, you never lose events — the core fix for dual-write problems between DB and message queue.

**Alt1:**
```sql
-- publish on transaction commit hook instead of manual relay
COMMIT AND CHAIN;  -- then read via LOGICAL REPLICATION (pgoutput) -> broker
```

## Q42: What is the saga pattern and how does it replace two-phase commit?

**Query:**
```sql
-- Distributed transaction split into local, compensatable steps
-- T1: create_order   (order svc DB)      compens_atable: cancel_order
-- T2: charge_card    (payment svc)       compensatable: refund
-- T3: reserve_inventory (inv svc)        compensatable: release
BEGIN; -- order svc
  INSERT INTO orders(id, status) VALUES(1,'pending');
COMMIT;
-- if T3 fails -> run compensations in reverse: T2 refund, T1 cancel
UPDATE orders SET status='cancelled' WHERE id=1;  -- compensation
```
**Explanation:** Sagas split a cross-service transaction into normal steps and compensating steps; on failure you undo completed steps. This preserves ACID locally but only eventual consistency globally, avoiding long-held locks across services.

## Q43: Why avoid two-phase commit (2PC) in large distributed SQL systems?

**Query:**
```sql
-- 2PC: coordinator PREPARE all participants, then COMMIT
--   PREPARE on db1, db2, db3 ... if coordinator dies mid-COMMIT:
--   participants hold prepared locks => unexplained stalls / coordinator recovery needed
PREPARE TRANSACTION 'txn-1' ;
-- ... if crash: SELECT * FROM pg_prepared_xacts; COMMIT PREPARED 'txn-1';
```
**Explanation:** 2PC provides atomicity but holds resources from PREPARE until a coordinator finishes, and an unavailable coordinator blocks everything. Across microservices and shards, plans crash-recovery and lock-holding make outbox/saga patterns more practical.

## Q44: What is change data capture (CDC) at a light level?

**Query:**
```sql
-- Debezium-style: read the DB transaction log as a stream of changes
--   source:
CREATE PUBLICATION dbz_publication FOR TABLE orders;
--   connector: binlog (MySQL) / WAL (PG) -> Kafka -> warehouse/replica
-- downstream applies each INSERT/UPDATE/DELETE row event
INSERT INTO warehouse_orders (...) VALUES (new_after);   -- replay
```
**Explanation:** CDC captures committed row changes from the transaction log without touching application tables or app polling. You stream those events to caches, search, aggregations, or the warehouse — enabling denormalized copies that eventually match the source.

## Q45: Combine partitioning + date pruning for a retention-friendly query.

**Query:**
```sql
CREATE TABLE audit_log (
    id        BIGSERIAL,
    actor     TEXT NOT NULL,
    action    TEXT NOT NULL,
    at        TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (at);

CREATE TABLE audit_log_2025_07 PARTITION OF audit_log
    FOR VALUES FROM ('2025-07-01') TO ('2025-08-01');

-- which one partition is hit by a 30-day audit lookback ?
SELECT actor, count(*) FROM audit_log
WHERE at BETWEEN '2025-06-01' AND '2025-07-01'
GROUP BY actor;
```
**Explanation:** With a weekly/monthly partition per time bucket, a date-bounded query prunes to one or two partitions and scans only that slice. Retention = dropping whole partitions and never running an unbounded DELETE.

## Q46: What is fan-out and when does one write touch many shards?

**Query:**
```sql
-- User "likes" a post -> record must exist on EVERY follower's feed =
--   write fan-out to N shards (one per follower) at serve time
-- implementation: one event row per follower-shard
INSERT INTO feed_events (follower_shard, user_id, post_id)
SELECT s, :userid, :postid FROM unnest(:follower_shards) s;   -- multi-shard write
```
**Explanation:** Operations that need to replicate a change into many users' data (news feeds, notifications) fan writes out to every concerned shard. That's one logical action but many physical writes — the reason feeds systems use eager vs lazy fan-out tradeoffs.

## Q47: When is partitioning the answer vs sharding the answer?

**Query:**
```sql
-- One beefy server suffices -> partition (pruning, retention, maintenance wins)
CREATE TABLE big_events PARTITION BY RANGE (ts);   -- 2 TB, fits on one host

-- Data/writes exceed what one server can do -> shard (multi-host scale-out)
--   orders.orders.hashed(customer_id) -> 8 MySQL hosts via Vitess
```
**Explanation:** If the dataset fits on one machine and only scan/heap size is the problem, partitioning suffices. If writes, storage, or backup exceed single-node capacity, you shard — partitioning stays within a node, sharding spans nodes.

## Q48: How do you choose partition count and interval for a time-series table?

**Query:**
```sql
-- Rule of thumb: aim for low hundreds of partitions, e.g. monthly for 5y = 60
--   chunk pages + stats per partition; too many = costly autovacuum/planning
-- Adapt interval to write volume: high-volume log -> hourly; audit -> monthly
CREATE TABLE rides PARTITION BY RANGE (started_at);
CREATE TABLE rides_p2025_07 PARTITION OF rides
    FOR VALUES FROM ('2025-07-01') TO ('2025-08-01');
-- set template for new partitions
CREATE TABLE rides PARTITION BY RANGE (started_at);
ALTER TABLE rides SET PARTITION TEMPLATE (PARTITION BY RANGE (started_at));
```
**Explanation:** The partition interval is a cache/index/storage size decision: enough rows per partition to amortize per-partition overhead, but not so many partitions that planning, vacuum and split operations explode. Monthly works for most; go hourly for very hot logs and quarterly for pure archives.

## Q49: What does `PRIMARY KEY` / `UNIQUE` require on a partitioned table?

**Query:**
```sql
-- PostgreSQL requires the partition key INSIDE every unique index
CREATE TABLE orders (
    order_id BIGINT,
    customer_id BIGINT NOT NULL,
    order_date DATE NOT NULL,
    PRIMARY KEY (order_id, order_date)   -- partition key included
) PARTITION BY RANGE (order_date);

-- unique code: must include partition key or it isn't global (MySQL: same rule)
CREATE TABLE orders (
    order_no VARCHAR(20),
    order_date DATE NOT NULL,
    UNIQUE KEY uq_order (order_no, order_date)
) PARTITION BY RANGE (YEAR(order_date));
```
**Explanation:** Uniqueness can only be enforced per-partition without a global index, so the partition column must be a prefix of every unique/primary key. PostgreSQL/MySQL reject a PK that omits the partition key — a classic "can't add NATURAL order_id PK" gotcha.

## Q50: Detach doesn't validate? Show a fast integrity-safe archive swap.

**Query:**
```sql
-- attach with constraint ensures data is confined BEFORE production traffic sees it
CREATE TABLE orders_2024 (LIKE orders INCLUDING ALL);
ALTER TABLE orders_2024 ADD CONSTRAINT orders_2024_bounds CHECK
    (order_date >= DATE '2024-01-01' AND order_date < DATE '2025-01-01');
INSERT INTO orders_2024 SELECT * FROM orders WHERE order_date < DATE '2024-01-01';  -- offline

ALTER TABLE orders ATTACH PARTITION orders_2024
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');  -- validates constraint in one scan
```
**Explanation:** Pre-loading a standalone table then ATTACHing (validated by the CHECK during attach) moves data into partition land without a full-table rewrite on the live table, keeping the swap atomic and integrity-safe.

## Q51: How does MySQL LIST/HASH partitioning compare with PostgreSQL for ad-hoc partition counts?

**Query:**
```sql
-- MySQL: partition count baked into the table at creation
CREATE TABLE log_h (
    id BIGINT, ts TIMESTAMP
) PARTITION BY HASH (id) PARTITIONS 16;

-- PostgreSQL: partitions are separate children; count = number you create
CREATE TABLE log_h2 (id BIGINT, ts TIMESTAMP) PARTITION BY HASH (id);
CREATE TABLE log_h2_0 PARTITION OF log_h2 FOR VALUES WITH (MODULUS 16, REMAINDER 0);
CREATE TABLE log_h2_1 PARTITION OF log_h2 FOR VALUES WITH (MODULUS 16, REMAINDER 1);
```
**Explanation:** MySQL declares partitions inside `CREATE TABLE` (count is fixed; resizing requires `ALTER ... REORGANIZE/COALESCE`). PostgreSQL partitions are independent tables attached by DDL, so scaling out is just add/drop ATTACHed children.

## Q52: What are the risks of an unbounded `MAXVALUE` partition for ranges?

**Query:**
```sql
-- MySQL: catch-all partition silently eats "impossible" values
CREATE TABLE t (ts DATE) PARTITION BY RANGE (YEAR(ts))
( PARTITION p0 VALUES LESS THAN (2024),
  PARTITION p_future VALUES LESS THAN MAXVALUE );
-- INSERT 2100.. silently accepted; p_future grows forever, never prunes
INSERT INTO t VALUES('2100-01-01');
```
**Explanation:** A MAXVALUE/DEFAULT catch-all protects inserts from "no partition for value" errors but hides data-quality issues, prevents pruning on that tail partition, and turns it into the table's unbounded hotspot. Prefer explicit partitions plus a monitoring query that flags the default.

## Q53: How do you make a time-series partition automatically on time (PostgreSQL).

**Query:**
```sql
CREATE OR REPLACE FUNCTION create_next_partition()
RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  EXECUTE format('CREATE TABLE IF NOT EXISTS metrics_%s PARTITION OF metrics
                  FOR VALUES FROM (%L) TO (%L)',
                 to_char(current_date + interval '2 months', 'YYYY_MM'),
                 date_trunc('month', current_date + interval '2 months'),
                 date_trunc('month', current_date + interval '2 months') + interval '1 month');
END $$;

SELECT create_next_partition();  -- cron / pg_cron each day, a month ahead
```
**Explanation:** A scheduled function creates the next month's partition in advance so inserts never hit a missing-partition error. Pre-create two or three months out to cover clock skew and spikes.

## Q54: Trigger-based vs declarative partitioning for maintenance.

**Query:**
```sql
-- Legacy trigger-sharding: every INSERT routed by IF/ELSE in a BEFORE trigger
CREATE TRIGGER route_orders BEFORE INSERT ON orders
FOR EACH ROW EXECUTE FUNCTION route_order();  -- pain to maintain

-- Declarative: planner routes rows by partition bounds; no trigger overhead
CREATE TABLE orders_part PARTITION BY RANGE (order_date);  -- preferred
```
**Explanation:** Trigger-based partitioning routes rows by hand (slow, error-prone, breaks bulk COPY and cross-partition updates). Declarative partitioning builds routing into the planner/storage and is the modern choice everywhere (PG10+, MySQL 8, Oracle).

## Q55: What is index alignment and why does partition-drop need local indexes?

**Query:**
```sql
-- Local index: index segment exists per partition, dropped WITH the partition
CREATE INDEX idx_orders_local ON orders (order_date) LOCAL;          -- Oracle
-- Global index: spans all partitions; dropping a partition must touch it
CREATE INDEX idx_orders_global ON orders (order_date) GLOBAL;        -- DROP PARTITION updates it
```
**Explanation:** Local (partition-local) indexes align 1:1 with partitions, so `DROP PARTITION` is a metadata delete of both data and index pieces. Global indexes span partitions — dropping a partition invalidates/index-maintains them, which is fast with `UPDATE GLOBAL INDEXES` but still costlier on retention-heavy systems.

## Q56: How do you know if a query actually prunes? (PostgreSQL example)

**Query:**
```sql
EXPLAIN (COSTS OFF)
SELECT count(*) FROM events WHERE ts >= '2025-07-01' AND ts < '2025-08-01';
-- Seq Scan on events_p2025_07  (good: exactly one partition)
--   vs
-- Append  (bad: iterates all partitions, each had a Bitmap/Seq Scan)
```
**Explanation:** Read the plan: a single child name in `EXPLAIN` means pruning worked; an `Append` node with every partition child means it didn't. This is the fastest way to catch a mis-placed cast or non-deterministic function.

## Q57: What is a "partition-wise join" and when does it help?

**Query:**
```sql
-- Both tables partitioned identically on the SAME key -> join slices pair up
--   orders by (customer_id), customers by (customer_id) -> join on one node
SELECT o.id, c.name
FROM orders o JOIN customers c ON o.customer_id = c.customer_id
WHERE c.region = 'us';
-- PG: enable_partitionwise_join = on
```
**Explanation:** If two tables use identical partition definitions, the optimizer can join partition i of A to partition i of B independently (partition-wise join), avoiding one big hash join and reducing memory/shuffle. It shines for large co-partitioned fact tables.

## Q58: What is a generated column for a composite shard key (salt)?

**Query:**
```sql
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    country TEXT NOT NULL,
    shard_bucket SMALLINT GENERATED ALWAYS AS (user_id % 64) STORED
) PARTITION BY HASH (shard_bucket);

SELECT * FROM users WHERE user_id = 42 AND shard_bucket = 42 % 64;  -- prune to 1 partition
```
**Explanation:** A stored generated column computes the salt/bucket from the natural key, so queries can target the exact bucket and the planner prunes. It also lets you keep the logical key while distributing evenly — avoiding a country-code hotspot.

## Q59: Write the query for an as-of join against a temporal/history table.

**Query:**
```sql
-- Get each order's product price as it was WHEN the order happened
SELECT o.order_id, o.product_id, h.price
FROM orders o
JOIN price_history h
  ON h.product_id = o.product_id
 AND o.created_at >= h.valid_from
 AND o.created_at <  h.valid_to;
```
**Explanation:** This bitemporal as-of join matches each order to the price version active at its timestamp. It needs an index on `(product_id, valid_from, valid_to)` to avoid a full history scan.

## Q60: What is a materialized view vs. a data mart for reporting scale?

**Query:**
```sql
-- Materialized view: refresh in place, base-table copy of the aggregate
CREATE MATERIALIZED VIEW mv_daily_sales AS
SELECT order_date, customer_id, sum(total) revenue
FROM orders GROUP BY order_date, customer_id
WITH NO DATA;
REFRESH MATERIALIZED VIEW mv_daily_sales;

-- Data mart: dedicated table/DB, extra custom columns, denormalized to the report
CREATE TABLE mart_daily_sales (...);   -- rebuilt/loaded from warehouse each batch
```
**Explanation:** Materialized views keep queries fast by precomputing aggregates and refreshing on schedule; data marts are purpose-built reporting tables possibly in a separate store (reporting database) — both are "compute once, read many."

## Q61: When do you put the partition key on the LEFT of an index?

**Query:**
```sql
-- Partition key first if queries always filter it,
-- especially on a global-ish index so pruning + index seek combine
CREATE INDEX idx_orders_modal
  ON orders (order_date, customer_id, status);   -- prune month, then customer
-- If the key is always filtered everywhere, omit it: already implicit in the partition slice
CREATE INDEX idx_orders_cistatus ON orders (customer_id, status);  -- per-partition, smaller index
```
**Explanation:** With local indexes, every partition already carries its partition-value slice, so repeating the key is redundant — index only non-partition columns. With global indexes (Oracle/SQL Server), leading with the partition key lets the server prune and seek in one step.

## Q62: What happens to transactions and locks with retention DROP PARTITION?

**Query:**
```sql
-- DROP PARTITION only needs a lock on that partition's structure,
-- not row locks on other partitions — concurrent appINSERT continues
ALTER TABLE orders DROP PARTITION p2019;
-- (In-flight ISOLATION-level operations on p2019 must finish first.)
```
**Explanation:** Dropping a partition takes an exclusive lock on the dropped piece and briefly on the table metadata, but does not row-lock or scan retained data. This makes partition-drop the O(1) retention primitive under live traffic — vs `DELETE WHERE date < x` which locks and logs every row.

## Q63: What is list-partition by constraint overlap and how is it detected?

**Query:**
```sql
-- Postgres checks partition bounds at ATTACH time
CREATE TABLE e PARTITION BY LIST (kind);
CREATE TABLE e_a PARTITION OF e FOR VALUES IN ('a');
CREATE TABLE e_b PARTITION OF e FOR VALUES IN ('b');
-- ATTACH e_dup FOR VALUES IN ('a') -> ERROR: partition bounds must not overlap
ALTER TABLE e ATTACH PARTITION e_dup FOR VALUES IN ('a');
```
**Explanation:** The database validates that each new partition's bound range is disjoint from existing ones and from the parent's constraint. Overlapping bounds are rejected eagerly (attach error) — a safety net that hand-rolled partition logic lacks.

## Q64: How do global indexes behave when you swap partitions (partition exchange)?

**Query:**
```sql
-- Exchange: promote a staging table to the live partitioned table instantly
-- (Oracle)
ALTER TABLE sales EXCHANGE PARTITION p2024_05 WITH TABLE sales_stage_2024_05;
-- (SQL Server)
ALTER TABLE sales SWITCH PARTITION 5 TO sales_archive_2024_05;
-- Global indexes on the target must be updated:
ALTER TABLE sales REBUILD PARTITION p2024_05 (global index) ...;
```
**Explanation:** Partition exchange swaps data files/segments in metadata time — instantly loading overnight bulk files or offloading old data. Global indexes then need maintenance/rebuild because their pointers changed; local indexes are unaffected. This is the signature trick for data-warehouse-style partition loads.

## Q65: What is Hard partition vs soft partitioning (schema-per-tenant)?

**Query:**
```sql
-- Soft/schema partitioning: one server, one schema per tenant
CREATE SCHEMA tenant_42; CREATE SCHEMA tenant_87;
CREATE TABLE tenant_87.orders (...);   -- app prefixes queries with schema

-- Hard partitioning: rows within one table by key
CREATE TABLE orders PARTITION BY HASH (customer_id);
```
**Explanation:** Schema-per-tenant isolates each tenant with separate metadata, sequences, and privileges, but multiplies maintenance (backup, provisioning, monitoring). Hard partitioning shares the query path, indexing and backup story, at the cost of weaker isolation. Both count as "partitioning" but answer different isolation-vs-efficiency tradeoffs.

## Q66: Prove a range query benefits from pruning with EXPLAIN (generic).

**Query:**
```sql
EXPLAIN
SELECT * FROM audit PARTITION = 3;      -- Oracle: force one partition
EXPLAIN PARTITIONS
SELECT * FROM audit WHERE at >= '2025-01-01' AND at < '2025-02-01';
-- PostgreSQL: EXPLAIN shows Append over one child only
```
**Explanation:** `EXPLAIN (PARTITIONS)` (MySQL), `PARTITION =` hint (Oracle), and Append-children inspection (PG) display exactly which physical partitions each query reads — demonstrating pruning instead of scanning the whole partitioned parent.

## Q67: What is a "missing partition"/data-not-there failure and how to avoid it?

**Query:**
```sql
-- Insert outside any bound -> error
INSERT INTO events (ts) VALUES ('2027-01-01');  -- no such partition
-- ERROR: no partition of relation "events" found for row
-- Fix: pre-create partitions ahead, or deploy the plannedcheduler
SELECT create_next_partition();               -- called daily by pg_cron
-- monitor for the "no partition found" error class
```
**Explanation:** If data arrives for a time window with no partition, PostgreSQL/MySQL reject the insert. Forward-creating partitions (scheduler) or adding a partitioned-default fallback make ingestion immune to clock skew and late data.

## Q68: How do you reshard with Vitess-style tools vs manual double-writes?

**Query:**
```sql
-- Vitess: MoveTables/Reshard handles split without app changes
--   vtctlclient Reshard ks.workflow '0' '-80'
-- Manual: dual-write into old + new shards, backfill, flip, drop
app => write(old_shard_k); write(new_shard);            -- every transaction x2
backfill = SELECT ... FROM old WHERE key IN (...) → COPY into new;    -- catch-up
-- flip reads to new once lag = 0; keep old in read-only; drop old
```
**Explanation:** Vitess automates the split (MoveTables, Reshard, VReplication) by streaming row changes so the app needs no code change. Manual resharding requires dual-writes, backfill of existing data, a flip point, and careful rollback — exactly what the tooling replaces.

## Q69: What is the difference between a distributed database vs a sharded monolith?

**Query:**
```sql
-- Sharded monolith: N independent postgres/MySQL instances, app joins/scatters
SELECT * FROM db_{shard(cid)}.orders WHERE customer_id = :cid;
-- Distributed SQL DB (CockroachDB/TiDB/Yugabyte): one protocol, SQL across nodes
SELECT * FROM orders WHERE customer_id = :cid;   -- transparent distributed execution
```
**Explanation:** A sharded normal DB gives you horizontal scale but the app owns routing, joins, and migrations. Distributed SQL databases keep one logical schema while spreading data/replicas across nodes, so cross-shard queries and consistency come built-in, at some coordination cost.

## Q70: What is query coalescing/fan-in at the coordinator for reporting?

**Query:**
```sql
-- Each shard computes its partial aggregation, coordinator merges
-- db0: SELECT date(dt), count(*) FROM events WHERE dt>=? GROUP BY 1
-- db1: (same); coordinator: SELECT date, sum(cnt) FROM parts GROUP BY date
-- (this "two-phase aggregation" is classic Map-Reduce-ish / streaming GROUP BY)
```
**Explanation:** Instead of shipping raw rows to be aggregated centrally, each shard pre-aggregates locally and only small partials travel. That is how OLAP over sharded OLTP stays fast — push down as much work to each shard as possible, then merge.

## Q71: How do you maintain counters (e.g. likes) correctly in a sharded system?

**Query:**
```sql
-- Anti-pattern: SELECT count(*) FROM likes WHERE post_id=? ON EVERY read  (scatter)
-- Better: denormalized counter column updated with delta transactions
BEGIN; INSERT INTO likes(post_id,user_id) VALUES(9,42);
      UPDATE posts SET like_count = like_count + 1 WHERE id=9; COMMIT;
-- Consistency trick: read like_count, but for exactness re-check the delta
-- or keep event-stream and materialize counter asynchronously
```
**Explanation:** Keeping a hot counter column updated in the same transaction as the "like" row gives strong consistency and cheap reads. When the counter is written by many app hosts concurrently, use atomic `+= 1` and periodic reconciliation against the event source.

## Q72: When would you use SQL Server partition switching over an ALTER?

**Query:**
```sql
-- Bulk-import into staging then switch = near-instant partition load
CREATE TABLE sales_stage(...);      -- same columns, same aligned PK
BULK INSERT sales_stage FROM 'daily.ctl';   -- fast, minimally logged
ALTER TABLE sales SWITCH TO sales_stage
  WITH ( PARTITION 5 ); -- now sales has the packed partition
```
**Explanation:** `SWITCH` swaps a whole partition's data between two identically-aligned tables in milliseconds, so you bulk-load a spare table offline then swap it in — the fastest way to land a daily warehouse load without locking the live table.

## Q73: Why do hot partitions need their own tuning (AutoVacuum, stats)?

**Query:**
```sql
-- Current-month partition gets all writes -> bloat + tuples, needs baby autovacuum
ALTER TABLE events_p2025_07 SET (autovacuum_vacuum_scale_factor = 0.05);
ANALYZE events_p2025_07;           -- hit once tables change a lot
-- read-only historical partitions: skip vacuum cost
ALTER TABLE events_p2024_06 SET (autovacuum_enabled = false);
```
**Explanation:** The newest partition absorbs inserts/updates; older ones are immutable. Different per-partition storage settings avoid thrash: aggressive autovacuum on the hot slice, none on archives. Statistics per partition also keep the planner's estimates honest after load.

## Q74: Rename the storage: table space/tablespace for hot vs cold.

**Query:**
```sql
-- PostgreSQL: split partitions across storage classes
CREATE TABLESPACE archive_ts LOCATION '/mnt/archive';
ALTER TABLE metrics_2024_01 SET TABLESPACE archive_ts;
-- Oracle: partition in a different tablespace
ALTER TABLE metrics MOVE PARTITION p2024_01 TABLESPACE cold_ts;
```
**Explanation:** Moving a whole partition to a slower/cheaper tablespace (spinning disk, object storage mount) relocates its data with a single DDL while keeping the query path. Hot partitions stay on NVMe; retired months migrate to archive tiers without application changes.

## Q75: Summarize the mental model: partitioning, sharding, replicas.

**Query:**
```sql
-- One decision axis: reads vs writes vs storage vs disaster recovery
-- Partitioning : within one node — pruning, retention, maintenance
-- Sharding     : across nodes  — write scale-out, geo, multi-terabyte
-- Replication  : copies for reads + failover, NOT write scale
-- (trade-offs summary) OLTP strong-consistency needs mono-writer; eventual lets replicas serve reads
```
**Explanation:** Use partitioning for large-but-vertical datasets, sharding when one node's writes/storage run out, and replicas for read capacity and HA. Sharding+partitioning often combine (partition inside each shard by time), while replication is always underneath for durability.

## Q76: How you implement archive/rollup automatically with partitioned tables.

**Query:**
```sql
-- Attach rolls the month in; the rollup job then collapses daily granularity
CREATE TABLE metrics_2025_07 PARTITION OF metrics
  FOR VALUES FROM ('2025-07-01') TO ('2025-08-01');

INSERT INTO rollup_monthly (year_month, metric, total)
SELECT date_trunc('month', dt), metric, sum(value)
FROM metrics WHERE dt < '2025-06-30' GROUP BY 1,2;   -- daily data -> monthly grain
```
**Explanation:** Old months transition from hot detail partitions to a coarse rollup table, and the detail partition is dropped. Retention + aggregation therefore happen on whole partitions, keeping both the raw tier and the summary tier tidy.

## Q77: How do Snowflake/BigQuery style micro-partitions relate to pruning?

**Query:**
```sql
-- Snowflake: tables auto-cluster into micro-partitions (~50-500MB) + metadata
CREATE TABLE orders (order_date DATE, total NUMBER)
CLUSTER BY (order_date);
SELECT sum(total) FROM orders WHERE order_date BETWEEN '2025-01-01' AND '2025-03-01';
-- only micro-partitions whose min/max covers range are scanned
-- BigQuery: automatic partitioning
CREATE TABLE `proj.dataset.orders`
PARTITION BY DATE_TRUNC(order_ts, MONTH)
OPTIONS( require_partition_filter = true );
```
**Explanation:** Columnar warehouses prune the same way but automatically: each micro-partition stores min/max bounds, so range queries skip whole chunks at scan time. `CLUSTER BY` (Snowflake) and declare partitioning (BigQuery) improve that pruning without any manual partition DDL.

## Q78: How does automatic vs manual partition management in Cloud warehouses differ?

**Query:**
```sql
-- BigQuery: partitions auto-created by ingestion; expire by time
CREATE TABLE log PARTITION BY DAY(ts)
PARTITION_EXPIRATION_DAYS = 30;   -- server drops old partitions for you
-- Redshift: manual distribution/sort keys instead
CREATE TABLE sales ( ... ) DISTSTYLE KEY
DISTKEY (customer_id) SORTKEY (sales_date);
```
**Explanation:** Modern warehouses manage partitioning invisibly (column-oriented micro-partitions, time-based expiry, automatic clustering), whereas classic DBs need you to write the ALTER/DROP DDL. On-prem SQL servers (Postgres/MySQL) keep the explicit model; on the managed side, you mostly declare intent and let the engine run it.

## Q79: In sharded OLTP, what is a "shared-nothing" join and when is it impossible?

**Query:**
```sql
-- co-located join: possible because rows already live together
SELECT ... FROM orders o JOIN customers c USING (customer_id);   -- key = shard key

-- non-key join: needs a broadcast/hash join over the network
--   e.g. join orders (sharded by customer) to ref.products (small, replicated)
SELECT * FROM orders o JOIN products p ON o.product_id = p.id;
-- small "reference" tables get replicated to every shard to enable it
```
**Explanation:** Shared-nothing means each shard holds only its slice; joins work only if the join key equals the shard key (co-located) or one input is replicated everywhere. Otherwise the coordinator must shuffle, which is what you design around with fan-out or denormalization.

## Q80: How do you approximate COUNT / analytics on huge partitioned data?

**Query:**
```sql
-- Exact count on 50B rows is expensive; use an approximation
SELECT count(*) FROM orders WHERE order_date = '2025-06-01';  -- exact, slow on huge tables

-- faster heuristics:
--  1) read the partition row estimate from stats: reltuples (PG)
SELECT reltuples::bigint AS approx_rows FROM pg_class WHERE relname='orders_p2025_06';
--  2) use the warehouse's APPROX_COUNT_DISTINCT (BigQuery / HLL)
SELECT APPROX_COUNT_DISTINCT(customer_id) FROM orders WHERE ds > 20250601;
--  3) HLL sketch: count distinct but not rows
```
**Explanation:** For exact row counts you must scan; for bounded memory "about N" answers, use planner statistics, approximate aggregate functions, or hyperlog-log sketches. On business dashboards approximate counts from partitioned stats are cheap and plenty.

## Q81: What is the two-phase outbox + CDC combo for rebuilding denormalized views?

**Query:**
```sql
-- Step 1: write event in the same tx as the domain row (outbox)
BEGIN;
  INSERT INTO orders (...) VALUES (...);
  INSERT INTO outbox(event_type,payload) VALUES ('order_created',
    jsonb_build_object('id', :id, 'customer', :cid));
COMMIT;
-- Step 2: CDC/debezium streams outbox rows to the search/cache/warehouse
--   which replays them into a denormalized serving table
INSERT INTO search_orders (id,customer_id,status) VALUES (new.id,new.customer_id,'new');
```
**Explanation:** The outbox guarantees the event exists; CDC delivers it reliably to downstream stores. That rebuild path is how a sharded system keeps read-side denormalized projections (search, feeds, counters) consistent without distributed transactions.

## Q82: Why is running analytics on the OLTP primary a bad idea, and what's the fix?

**Query:**
```sql
-- Bad: report query locks/vacuum-thrashes the hot DB
SELECT ... big JOIN ... GROUP BY ... FROM orders WHERE total_reads > x;  -- primary

-- Fix: route to a replica / build a columnar export via COPY
COPY (SELECT ... ) TO '/tmp/report.csv';
-- and load into warehouse for columnar scans
COPY report FROM '/tmp/report.csv';   -- on the warehouse
```
**Explanation:** A long analytic scan competes for buffers, locks and CPU with OLTP writes, risking row-index/page-lock stalls. Analytics belong on a replica (replication lag tolerated) or a separate columnar store that handles scans natively.

## Q83: What is a "scatter-gather" pattern and when is the coordinator the bottleneck?

**Query:**
```sql
-- Every shard returns its partial result in a scatter-gather query
--   fan-out: S shards * latency; gather: coordinator merges S partial sets
-- Bottleneck: coordinator memory/CPU when S is large and partials are big, or when
--   one shard is slow -> total latency = slowest shard
SELECT * FROM orders WHERE customer_id IN (...many...) AND status='open'
   <- executed per shard, merged in clockwise-latency order
```
**Explanation:** Scatter-gather binds coordinator capacity and awaits the slowest shard. Mitigations: cap fan-out (partitioned sub-keys), push heavy work down (partial aggregate), pre-sort/broadcast, or serve the hot read from a prebuilt aggregation.

## Q84: How do UUIDv7 and snowflake keys keep write locality in sharded tables?

**Query:**
```sql
-- v7 UUID: timestamp in the high bits -> close rows have close sort keys
SELECT uuid_generate_v7();   -- e8b81a11-a9c7-7c6?-...
-- snowflake ID: (ms timestamp, machine/worker bits, per-worker counter)
CREATE TABLE orders ( id BIGINT PRIMARY KEY, created_at TIMESTAMPTZ DEFAULT now() );
-- insert around same time -> same page range, good for RANGE index scans/geo-semi
```
**Explanation:** Both encode time in the leading bits, so new rows cluster near each other in the index instead of scattering across the whole B-tree (the UUIDv4 problem). That preserves CRUD locality even when inserters are distributed across many app servers and shards.

## Q85: What is the "friendly fire" of SQL Server partition alignment (unique index)?

**Query:**
```sql
-- unique/primary key must include the partition column
CREATE TABLE orders (
  order_id  BIGINT NOT NULL,
  order_date DATE NOT NULL,
  PRIMARY KEY (order_id, order_date)          -- must lead with partition col
) ON ps_orders (order_date);
-- UNIQUE (order_id) alone is impossible over a partitioned table:
--   error : the partition column must be part of the unique key
```
**Explanation:** Any globally unique index over a partitioned SQL Server table must incorporate the partition key, because uniqueness is enforced per partition. That forces surrogate-key designs to denormalize (order_id, partition_date) or accept per-partition uniqueness — a deliberate, surprising-by-design limitation.

## Q86: Why does a sharded system need idempotency keys for writes?

**Query:**
```sql
-- Retry over uncertain network -> duplicated write unless you dedupe
-- Solution: idempotency key column + unique constraint on it
CREATE TABLE payments (
    txn_id      BIGINT PRIMARY KEY,
    idem_key    UUID NOT NULL UNIQUE,     -- client-generated, retried as-is
    amount      NUMERIC(10,2), status TEXT
);
INSERT INTO payments (idem_key, amount, status)
VALUES (:key, :amt, 'new') ON CONFLICT (idem_key) DO NOTHING;
-- When client retries with same idem_key, second attempt is a no-op
```
**Explanation:** Sharded systems retry a lot (timeouts beyond one shard fail before commit-known). An idempotency key with a unique constraint turns an at-least-once delivery into exactly-once application semantics; without it, retried transactions double-charge.

## Q87: What is grid/horizontal sharding vs. split by tenant (isolated heap)?

**Query:**
```sql
-- Grid sharding: every table divided by customer_id across hot nodes
CREATE TABLE orders_shard_0 AS SELECT * FROM orders WHERE customer_id % 8 = 0;  -- etc
-- Tenant-home: each tenant owns its cluster/schema with private schema DDL
--  (tenant_87 owns orders WHERE customer_id IN (...)) — but cross-tenant join is local
```
**Explanation:** Grid (data keyed) shares global DDL and indexes; tenant-home gives isolation in billing, capacity, and DDL blast radius — with harder cost of cross-tenant analytics. Choose grid for shared-schema microservices; tenant-home for billing isolation and noisy neighbors.

## Q88: When to use SQL Server/MySQL/Postgres partitioning vs. a partitioned engine like ClickHouse?

**Query:**
```sql
-- PG/MySQL: row-store partitions for OLTP pruning/retention — few hundred
CREATE TABLE events PARTITION BY RANGE (ts);   -- ~200 partitions, point queries

-- ClickHouse: column-store, per-part merge-tree at scale — thousands of parts
CREATE TABLE events_ck (ts DateTime, msg String)
ENGINE = MergeTree PARTITION BY toYYYYMM(ts) ORDER BY ts;
SELECT ... WHERE ts >= '2025-06-01' GROUP BY ...;   -- scan-complete analytics on 1B rows
```
**Explanation:** Classic DB partitioning helps when queries still do index/point access. For scan-heavy analytics on billions of rows you're better off with a column oriented, merge-tree engine whose "partition parts" are designed for many hundreds of them: different storage, different access pattern.

## Q89: Read-after-write in a multi-primary or active-active setup.

**Query:**
```sql
-- Two primaries asynchronously replicating -> conflicts & lag
--   update account 'A' on dc1; read on dc2 may see old value until async sync
-- Fix options:
--  1) same user -> same primary (session affinity / LWW by timestamp)
--  2) read-your-writes by routing the read to the primary that served the write
--  3) CDC/epoch guard: reject read if last_write_ts > replicated_ts (client-supplied ts)
SELECT value FROM account WHERE id=:a AND replication_epoch >= :my_write_epoch;
```
**Explanation:** Active-active with async replication trades strong read-your-writes for availability. Route per-user writes to a single DC (affinity), or version-read gates — LWW timestamps alone can drop updates from a lagging DC, so add collision detection.

## Q90: Denormalized projection + CDC = the canonical read-path for sharded apps.

**Query:**
```sql
-- source shard: orders/order_lines bring in the outbox event
-- CDC/debezium delivers order_created to:
--    user-orders (per user)  + order-search (per status)  + metrics (per day)
-- downstream table (search projection):
CREATE TABLE order_search (
   order_id BIGINT, customer_id BIGINT, customer_name TEXT,
   status TEXT, items JSONB, created_at TIMESTAMPTZ
) PARTITION BY HASH (customer_id);
SELECT * FROM order_search WHERE customer_id=:cid AND status='paid';  -- one shard
```
**Explanation:** Instead of joins at read time, sharded apps maintain specialized read models fed by CDC/outbox events. Because each read model is keyed to its access pattern, every serving query lands on one shard — the entire trick of sharded e-commerce/search products.

## Q91: What is "shard key change" hell and how do you support it?

**Query:**
```sql
-- Customer changes email/login; if email is the shard key, its row must move….
-- Better: immutable tenant_id is the key; mutable fields stay columnar
CREATE TABLE customers (
   id BIGINT NOT NULL,          -- shard key; never edited
   email TEXT,                  -- mutable, lives with the row
   PRIMARY KEY(id)
);
-- IF you must rekey: active-row dual-write + altenative index until the move ends
```
**Explanation:** If the shard key can change, updating it means relocating a row to another shard — rewriting indexes and risking lost reads mid-move. Prefer an immutable surrogate key (id/tenant_id) for routing and keep business-mutable identifiers as plain columns.

## Q92: When is partition shrink / REORG needed and how do you run it offline?

**Query:**
```sql
-- heavily-updated partition gets bloat; reorganize just that piece
-- Oracle / SQL Server
ALTER TABLE orders MOVE PARTITION p2025_01 TABLESPACE fast_ts;   -- offline move
ALTER INDEX idx_orders REBUILD PARTITION p2025_01;
-- PostgreSQL
VACUUM (FULL) orders_p2025_01;    -- blocks writers on that partition only
-- MySQL: ALTER TABLE orders REORGANIZE PARTITION ...
```
**Explanation:** Per-partition maintenance confines bloat to the slice that changed. Dropping indexes, `MOVE PARTITION` or `VACUUM FULL` of an old/low-activity partition recompacts storage with a bounded lock — a known time window instead of a multi-hour table-wide operation.

## Q93: How would you rate-limit and back-pressure events going to a warehouse?

**Query:**
```sql
-- gate the COPY/load from the broker rather than blasting the warehouse
-- 1) round-robin huge file copies: COPY table FROM s3://bucket/part_0001..
-- 2) retry with exponential backoff on throttle
-- 3) monitor cursor lag; if the WAL/outbox departs the load, break up the batch
COPY events FROM 's3://events/load_group_00037/' IAM_ROLE '...' CSV;
```
**Explanation:** Bulk loaders move big chunks fast, but a warehouse will throttle or you can hit quota. Chunked/staged COPYs with backoff, and lag-based backpressure (don't let the WAL/outbox run ahead) keep the pipe steady — the classic broker-to-warehouse engineering pattern.

## Q94: Demonstrate a UNIQUE across a partitioned PK that PostgreSQL still permits.

**Query:**
```sql
-- unique constraint confined per-partition is allowed only if the key
-- contains the partition column; otherwise rejected
CREATE TABLE note (
  id BIGINT, customer_id BIGINT, seq BIGINT,
  PRIMARY KEY (customer_id, seq)          -- OK: leads with partition col
) PARTITION BY HASH (customer_id);

CREATE TABLE bump (
  id BIGINT, ref BIGINT UNIQUE             -- ERROR: ref not in partition key
) PARTITION BY HASH (id);
```
**Explanation:** Because uniqueness is enforced per partition, a unique index must include the partition column as a prefix. This is the biggest schema-design gotcha on partitioned tables: convert global unique keys into `(partition_col, natural_unique)` composites when you partition.

## Q95: What is "metadata-only" vs "data-moving" DDL when adding a partition?

**Query:**
```sql
-- Metadata-only (attach/list/rag period): no data rewrite
CREATE TABLE orders_new ... ; ALTER TABLE orders ATTACH PARTITION orders_new...; -- instant

-- Data-moving (ALTER ... PARTITION BY RANGE in Oracle, PostgreSQL repartition): rewrites rows
ALTER TABLE orders ALTER PARTITION SET;  -- / CREATE new + INSERT ... SELECT
```
**Explanation:** Adding an empty partition (or swapping aligned tables) only updates catalog metadata. Repartitioning an existing table's data, or rebalancing hash counts on MySQL (`REORGANIZE`), physically rewrites rows — plan a maintenance window and watch disk.

## Q96: What are the two PLANNING pitfalls with many partitions?

**Query:**
```sql
-- 1) per-partition row estimates add up but stats are stale -> wrong choice pruner
ANALYZE events_p2025_06;   -- spec per partition; parent uses child stats
-- 2) recursive Append over thousands of partitions -> planning time sky-rockets
EXPLAIN SELECT * FROM events WHERE ts='2025-07-01T10:00:00Z';
-- plan shows Append on 1237 children: ~separation cost, consider partition pruning
SELECT count(*) FROM events WHERE ts < '2024-01-01' ; -- 1000s of children scanned
```
**Explanation:** The planner budgets a pruning/generation pass per partition; with tens of thousands of them, planning goes sublinear-to-linear and stats drift. Keep partitions bounded (hundreds–low thousands), ANALYZE hot slices, and make sure filters are sargable against the key.

## Q97: What does sharding do to backup and point-in-time recovery?

**Query:**
```sql
-- each shard has its own snapshot: restore must be coordinated
--   shard0 pg_dump, shard1 pg_dump,... — no global transaction boundary
-- consensus: WAL-archives per shard restored to a common LSN/epoch, then reconcile
--  point-in-time (PITR) across shards: restore each to time T; overlapping
--  cross-shard txn may exist in shard A but not shard B -> inconsistent slice
```
**Explanation:** Without replication-consistent snapshots per shard, cross-shard consistency at restore time isn't guaranteed — a two-shard write may survive on one and vanish on the other. Producers solve it with consistent snapshots, restore ordering, or app-level reconciliation/idempotency at that LSN/epoch.

## Q98: When do you NOT partition or shard at all?

**Query:**
```sql
-- <few million rows single node, uniform access => partitions add overhead
CREATE TABLE small_lookup (...);   -- no partition clause. fine as-is.
-- reads/writes fit one node, analytics run on the replica => sharding is needless
--  instead: add a covering index, materialized view, archive the old data
```
**Explanation:** Partitioning pays off above a few million rows or when you need retention-by-drop; sharding pays off when node capacity (storage/write IO) is the wall. If indexes fix it, use indexes; premature partitioning/sharding just adds operational weight.

## Q99: Write an end-to-end retention + archive solution with partitions (all platforms syntax).

**Query:**
```sql
-- PostgreSQL
CREATE TABLE logs PARTITION BY RANGE (ts);
CREATE TABLE logs_2025_06 PARTITION OF logs FOR VALUES FROM ('2025-06-01') TO ('2025-07-01');
ALTER TABLE logs DETACH PARTITION logs_2024_06;  -- archive 12 months out
-- MySQL
ALTER TABLE logs PARTITION BY RANGE (YEAR(ts)) (... p_2024 BEFORE, p_now ...);
ALTER TABLE logs DROP PARTITION p_2022;          -- purge O(1)
-- Oracle
ALTER TABLE logs DROP PARTITION p_2023 UPDATE GLOBAL INDEXES;
ALTER TABLE logs MOVE PARTITION p_2024 TABLESPACE archive_ts;
-- SQL Server
ALTER TABLE logs SWITCH PARTITION 3 TO logs_archive;
```
**Explanation:** All four engines express the same policy: keep rolling windows, drop whole old partitions (metadata-op), and optionally move the oldest live slice to a cheaper tablespace. Retention becomes a cron job of attach/drop/move — not `DELETE FROM logs WHERE ts<...`.

## Q100: Summarize the 10 laws of partitioning/sharding at scale.

**Query:**
```sql
-- 1. Partition key must be in every hot WHERE / unique
-- 2. Sargable predicates only; let pruning work
-- 3. Bounded partition count; hot slice tuned separately
-- 4. Keep hot data recent, archive by whole partition
-- 5. Shard key = high-cardinality, immutable, in every query
-- 6. Fake a low-cardinality/country key or you get hotspots
-- 7. Cross-shard work is a last resort: denormalize or fan-out
-- 8. Replicas scale reads, never writes; read-after-write pins known writers
-- 9. Outbox+CDC keeps projections eventually consistent
-- 10. Startup normal until partitioned; evolve it only when it pays
```
**Explanation:** The discipline is all upstream of the query: pick keys that prune, shape access to be single-shard, and keep write/retention cheap. Everything else — engines, Vitess, warehouses — is just the machinery around those decisions.
