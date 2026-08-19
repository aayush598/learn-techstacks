# Relational Databases — PostgreSQL for Recommendation Systems

## 1. Why PostgreSQL for Recommendation Systems

### 1.1 Core Strengths

- **ACID Compliance**: Transactional integrity is critical for user profile updates, interaction logging, and model metadata management where partial writes can corrupt downstream pipelines.
- **JSON/JSONB Support**: PostgreSQL's JSONB column type provides schema flexibility for semi-structured data (item metadata, user preferences, experiment configurations) without sacrificing queryability.
- **Full-Text Search**: Built-in tsvector/tsquery support enables keyword search over item descriptions and user-generated content without a separate search engine for small-to-medium catalogs.
- **Extensibility**: Extensions like PostGIS (geospatial), pg_trgm (fuzzy text matching), and pgvector (vector similarity) extend PostgreSQL's capabilities for recommendation-specific use cases.
- **Mature Ecosystem**: Extensive tooling for monitoring (pg_stat_statements, pgBadger), backup (pg_dump, pgBackRest), replication (streaming, logical), and connection pooling (PgBouncer, PgPool-II).

### 1.2 Limitations to Acknowledge

- **Write Throughput**: PostgreSQL's MVCC architecture creates write amplification; high write throughput (>10K writes/second) requires careful tuning or offloading to a write-optimized system.
- **Horizontal Scaling**: Native PostgreSQL does not support horizontal sharding; read replicas handle read scaling but not write scaling. Citus extension adds sharding capability.
- **Real-Time Feature Serving**: PostgreSQL's query latency is typically 1–10ms for indexed lookups, which is adequate but not optimal for sub-5ms feature serving at high QPS.
- **Vector Similarity**: pgvector is functional but significantly slower than purpose-built vector databases (FAISS, Milvus) for high-dimensional similarity search at scale.

---

## 2. Schema Design for Recommendation Systems

### 2.1 Core Entity Tables

```sql
-- Users table: Core user profile and metadata
CREATE TABLE users (
    user_id         BIGSERIAL PRIMARY KEY,
    external_id     VARCHAR(64) UNIQUE NOT NULL,  -- External auth provider ID
    email           VARCHAR(255),
    display_name    VARCHAR(128),
    country_code    CHAR(2) NOT NULL,
    language_code   CHAR(5) DEFAULT 'en',
    age_bucket      SMALLINT,                     -- 0: unknown, 1: 13-17, 2: 18-24, ...
    gender          VARCHAR(16),
    signup_date     DATE NOT NULL,
    last_active_at  TIMESTAMPTZ,
    user_segment    VARCHAR(32),                  -- 'power_user', 'casual', 'dormant'
    is_bot          BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Items table: Product/content catalog
CREATE TABLE items (
    item_id         BIGSERIAL PRIMARY KEY,
    external_id     VARCHAR(128) UNIQUE NOT NULL,
    title           VARCHAR(512) NOT NULL,
    description     TEXT,
    category_id     INTEGER REFERENCES categories(category_id),
    brand           VARCHAR(128),
    price           NUMERIC(12,2),
    currency_code   CHAR(3) DEFAULT 'USD',
    image_url       TEXT,
    item_type       VARCHAR(32) NOT NULL,          -- 'product', 'video', 'article', 'podcast'
    status          VARCHAR(16) DEFAULT 'active',  -- 'active', 'discontinued', 'out_of_stock'
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- User-Item Interactions: Core recommendation data
CREATE TABLE interactions (
    interaction_id  BIGSERIAL PRIMARY KEY,
    user_id         BIGINT NOT NULL REFERENCES users(user_id),
    item_id         BIGINT NOT NULL REFERENCES items(item_id),
    event_type      VARCHAR(32) NOT NULL,          -- 'view', 'click', 'purchase', 'rate', 'save'
    event_value     REAL,                          -- rating value, or interaction strength
    session_id      VARCHAR(64),
    device_type     VARCHAR(16),
    country_code    CHAR(2),
    referrer        VARCHAR(512),
    created_at      TIMESTAMPTZ NOT NULL
);

-- User Preferences: Explicit user preferences
CREATE TABLE user_preferences (
    user_id         BIGINT REFERENCES users(user_id),
    preference_key  VARCHAR(64) NOT NULL,
    preference_value VARCHAR(256) NOT NULL,
    source          VARCHAR(32) DEFAULT 'explicit', -- 'explicit', 'inferred'
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, preference_key)
);
```

### 2.2 Model Management Tables

```sql
-- Model registry: Track all model versions
CREATE TABLE models (
    model_id        SERIAL PRIMARY KEY,
    model_name      VARCHAR(128) NOT NULL,
    model_version   VARCHAR(32) NOT NULL,
    model_type      VARCHAR(64) NOT NULL,          -- 'cf', 'content_based', 'deep_ranking'
    training_data_snapshot VARCHAR(128),           -- Reference to training data version
    hyperparameters JSONB,
    metrics         JSONB,                         -- {'auc': 0.85, 'ndcg@10': 0.72, ...}
    artifact_path   TEXT NOT NULL,                 -- S3/GCS path to model artifact
    status          VARCHAR(16) DEFAULT 'staging', -- 'staging', 'canary', 'production', 'archived'
    deployed_at     TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- A/B experiments
CREATE TABLE experiments (
    experiment_id   SERIAL PRIMARY KEY,
    experiment_name VARCHAR(128) NOT NULL,
    description     TEXT,
    traffic_allocation JSONB,                     -- {'control': 50, 'treatment_a': 25, 'treatment_b': 25}
    primary_metric  VARCHAR(64) NOT NULL,
    status          VARCHAR(16) DEFAULT 'draft',
    start_date      TIMESTAMPTZ,
    end_date        TIMESTAMPTZ,
    created_by      VARCHAR(64),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 3. Indexing Strategies

### 3.1 B-Tree Indexes

Standard B-tree indexes for equality and range queries:

```sql
-- User lookup by external ID (authentication)
CREATE INDEX idx_users_external_id ON users(external_id);

-- Item lookup by external ID (catalog sync)
CREATE INDEX idx_items_external_id ON items(external_id);

-- Interaction queries by user and time range
CREATE INDEX idx_interactions_user_time ON interactions(user_id, created_at DESC);

-- Interaction queries by item (for item-based CF)
CREATE INDEX idx_interactions_item_time ON interactions(item_id, created_at DESC);

-- Active items for candidate generation
CREATE INDEX idx_items_status ON items(status) WHERE status = 'active';
```

### 3.2 Composite Indexes

Covering indexes that satisfy query patterns without table lookups:

```sql
-- Covering index for user interaction history retrieval
CREATE INDEX idx_interactions_user_covering ON interactions(user_id, created_at DESC)
    INCLUDE (item_id, event_type, event_value);

-- Covering index for item interaction summary
CREATE INDEX idx_interactions_item_covering ON interactions(item_id, created_at DESC)
    INCLUDE (user_id, event_type, event_value);

-- Partial index for recent interactions only (hot data)
CREATE INDEX idx_interactions_recent ON interactions(user_id, created_at DESC)
    WHERE created_at > NOW() - INTERVAL '90 days';
```

### 3.3 Index Selection Guidelines

| Query Pattern | Recommended Index | Expected Latency |
|--------------|-------------------|------------------|
| User by external_id | B-tree on external_id | < 1ms |
| User's interaction history (last N) | B-tree on (user_id, created_at DESC) | < 5ms |
| Item's interaction history | B-tree on (item_id, created_at DESC) | < 5ms |
| Interactions in time range | B-tree on created_at + filter | < 10ms |
| User preferences | B-tree on (user_id, preference_key) | < 1ms |
| Active items by category | Partial index on status + category_id | < 5ms |

---

## 4. Partitioning Strategies

### 4.1 Table Partitioning for Interactions

The interactions table is the largest table in a recommendation system and benefits significantly from partitioning:

```sql
-- Range partitioning by time (monthly partitions)
CREATE TABLE interactions (
    interaction_id  BIGSERIAL,
    user_id         BIGINT NOT NULL,
    item_id         BIGINT NOT NULL,
    event_type      VARCHAR(32) NOT NULL,
    event_value     REAL,
    session_id      VARCHAR(64),
    created_at      TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE interactions_2026_01 PARTITION OF interactions
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE interactions_2026_02 PARTITION OF interactions
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
-- ... auto-create future partitions with pg_partman
```

### 4.2 Partitioning Benefits

| Benefit | Explanation | Impact |
|---------|-------------|--------|
| **Query Pruning** | Queries with time filters only scan relevant partitions | 5–10× faster range queries |
| **Maintenance** | Drop old partitions instead of DELETE (no VACUUM needed) | 100× faster data lifecycle management |
| **Index Efficiency** | Smaller indexes per partition fit in memory better | Improved cache hit ratio |
| **Parallel Queries** | Each partition can be scanned in parallel | Better multi-core utilization |

### 4.3 Partition Management

- **Automated Creation**: Use pg_partman or a custom script to create future partitions monthly.
- **Automated Retention**: Drop partitions older than the retention period (e.g., 2 years for detailed interactions, indefinite for aggregated data).
- **Partition Pruning**: Ensure queries always include the partition key (created_at) to enable partition pruning. Use EXPLAIN ANALYZE to verify.

---

## 5. Replication and High Availability

### 5.1 Replication Topologies

| Topology | Description | Use Case |
|----------|-------------|----------|
| **Single Primary + Read Replicas** | One primary handles writes; replicas handle reads | Most common; read-heavy workloads |
| **Synchronous Replication** | Primary waits for replica acknowledgment before committing | Zero data loss; higher write latency |
| **Asynchronous Replication** | Primary commits immediately; replicas lag behind | Lower write latency; possible data loss |
| **Cascading Replicas** | Replicas replicate from other replicas | Reduces primary load; increases replication lag |
| **Logical Replication** | Selective table-level replication | Replicate specific tables to different systems |

### 5.2 Read Replica Strategy for Recommendation Systems

- **User Profile Reads**: Route all user profile reads to read replicas; write updates to the primary.
- **Interaction Writes**: Write interaction events to the primary; read replicas serve historical interaction queries.
- **Feature Computation**: Read replicas serve the data for batch feature computation jobs, offloading the primary.
- **Connection Pooling**: Use PgBouncer in front of each read replica to manage connection pools efficiently.

### 5.3 Failover and Recovery

- **Automatic Failover**: Use Patroni or pg_auto_failover for automatic primary failover with health checks.
- **Failover Time Target**: < 30 seconds for automatic failover; < 5 minutes for manual intervention.
- **Data Loss Tolerance**: With synchronous replication, RPO = 0. With asynchronous replication, RPO = replication lag (typically seconds to minutes).

---

## 6. Connection Pooling

### 6.1 Why Connection Pooling Matters

PostgreSQL uses a process-per-connection model — each connection spawns a new OS process. With thousands of concurrent connections, this creates excessive memory usage and context switching overhead.

### 6.2 Connection Pool Architecture

```
Application Servers → PgBouncer (Connection Pooler) → PostgreSQL Primary/Replicas
                     ├── Pool Mode: Transaction (recommended)
                     ├── Default Pool Size: 20–50 connections per database
                     ├── Max Client Connections: 1000+
                     └── Server Idle Timeout: 300 seconds
```

### 6.3 Pool Mode Comparison

| Mode | Description | Pros | Cons |
|------|-------------|------|------|
| **Session** | Connection assigned for entire client session | Simple; supports SET commands | Wastes connections during idle periods |
| **Transaction** | Connection assigned per transaction | Better utilization; connection reuse | Cannot use PREPARE statements or LISTEN/NOTIFY |
| **Statement** | Connection assigned per statement | Maximum utilization | Very restrictive; no multi-statement transactions |

**Recommendation**: Use Transaction mode for recommendation workloads — most queries are simple lookups within single transactions.

---

## 7. Query Optimization

### 7.1 Common Recommendation Queries and Optimization

**User Interaction History (Last N Interactions)**:
```sql
-- Optimized: Uses covering index, returns immediately
SELECT item_id, event_type, event_value, created_at
FROM interactions
WHERE user_id = $1
ORDER BY created_at DESC
LIMIT 50;
```

**Item Popularity (Last 30 Days)**:
```sql
-- Optimized: Uses partial index for recent data
SELECT item_id, COUNT(*) as view_count,
       COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) as purchase_count
FROM interactions
WHERE created_at > NOW() - INTERVAL '30 days'
  AND event_type IN ('view', 'purchase')
GROUP BY item_id
HAVING COUNT(*) >= 10
ORDER BY view_count DESC
LIMIT 1000;
```

**Co-Occurrence Matrix (Item-to-Item CF)**:
```sql
-- Optimized: Using window functions and self-join
SELECT i1.item_id AS item_a, i2.item_id AS item_b, COUNT(*) AS co_occurrence
FROM interactions i1
JOIN interactions i2 ON i1.user_id = i2.user_id
    AND i1.item_id < i2.item_id
    AND i1.created_at BETWEEN i2.created_at - INTERVAL '7 days' AND i2.created_at + INTERVAL '7 days'
WHERE i1.event_type = 'purchase' AND i2.event_type = 'purchase'
GROUP BY i1.item_id, i2.item_id
HAVING COUNT(*) >= 5;
```

### 7.2 Query Performance Monitoring

- **pg_stat_statements**: Track query execution statistics — total time, calls, mean time, rows.
- **EXPLAIN ANALYZE**: Use for query plan analysis; look for sequential scans on large tables, nested loops with high row counts, and sort operations on large result sets.
- **Index Hit Ratio**: Target > 99% index hit ratio for frequently queried tables. Low hit ratio indicates insufficient memory for index caching.

---

## 8. JSONB for Flexible Schemas

### 8.1 When to Use JSONB

- **Item Metadata**: Different item types (products, videos, articles) have different attribute sets. JSONB allows storing type-specific attributes without schema changes.
- **Experiment Configurations**: A/B test parameters change frequently and have varied structures.
- **User Feature Snapshots**: Snapshots of computed user features for debugging and audit.
- **Model Hyperparameters**: Variable structure depending on model type.

### 8.2 JSONB Query Patterns

```sql
-- Query items by nested JSONB attribute
SELECT * FROM items
WHERE metadata->>'color' = 'red'
  AND (metadata->'dimensions'->>'weight')::numeric < 2.5;

-- Index JSONB columns for query performance
CREATE INDEX idx_items_metadata_color ON items USING GIN ((metadata->>'color'));
CREATE INDEX idx_items_metadata ON items USING GIN (metadata);

-- Aggregate JSONB data
SELECT metadata->>'brand' AS brand, COUNT(*)
FROM items
WHERE metadata ? 'brand'
GROUP BY metadata->>'brand'
ORDER BY COUNT(*) DESC;
```

### 8.3 JSONB Best Practices

- **Validate at Application Layer**: JSONB does not enforce schema; use application-level validation (Pydantic, JSON Schema) to ensure data integrity.
- **Index Strategically**: GIN indexes on JSONB are effective for containment queries (? and @> operators) but not for scalar comparisons. Use expression indexes for frequently queried paths.
- **Avoid Deep Nesting**: Flatten deeply nested JSONB structures into separate columns for frequently queried fields. Use JSONB for truly variable or sparse attributes.
- **Storage Awareness**: JSONB is stored as a compressed binary format (more efficient than raw JSON text) but is still larger than typed columns for equivalent data.
