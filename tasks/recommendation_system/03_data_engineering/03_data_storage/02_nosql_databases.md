# NoSQL Databases — Recommendation System Data Storage

## 1. When to Choose NoSQL Over SQL

### 1.1 Decision Matrix

| Requirement | SQL (PostgreSQL) | NoSQL (Cassandra/MongoDB/DynamoDB) |
|------------|------------------|------------------------------------|
| Data Structure | Fixed schema, relational | Flexible schema, document/columnar |
| Write Throughput | Moderate (< 10K writes/s per node) | High (100K+ writes/s per node) |
| Read Pattern | Complex joins, aggregations | Simple key-value lookups, known query patterns |
| Consistency | Strong (ACID) | Tunable (eventual to strong) |
| Horizontal Scaling | Limited (Citus adds sharding) | Native (add nodes linearly) |
| Transaction Support | Full multi-row transactions | Limited (single-partition transactions) |
| Query Flexibility | Ad-hoc queries | Known query patterns only |
| Best For | User profiles, model metadata, experiment configs | Interaction logs, session data, feature store |

### 1.2 The Polyglot Persistence Pattern

Production recommendation systems use multiple database types:

| Data Type | Database Choice | Rationale |
|-----------|----------------|-----------|
| User profiles | PostgreSQL | Relational integrity, complex queries |
| User preferences | PostgreSQL (JSONB) | Flexible schema, queryable |
| Interaction events | Cassandra / ScyllaDB | High write throughput, time-series access |
| Session state | Redis | Sub-millisecond reads, TTL-based expiry |
| Item catalog | PostgreSQL + MongoDB | Structured fields in SQL, unstructured metadata in Mongo |
| Feature vectors | Redis / DynamoDB | Low-latency key-value lookups |
| Knowledge graph | Neo4j | Graph traversal queries |
| Search index | Elasticsearch | Full-text search, faceted filtering |

---

## 2. Cassandra for High Write Throughput

### 2.1 Why Cassandra for Recommendation Systems

- **Write-Optimized**: Cassandra's LSM-tree storage engine is optimized for write-heavy workloads. Interaction event logging (millions of events per second) is a natural fit.
- **Linear Horizontal Scaling**: Add nodes to increase throughput proportionally. No rebalancing or resharding required.
- **Tunable Consistency**: Configure consistency per query — ONE for low-latency reads, QUORUM for balanced, ALL for strong consistency.
- **No Single Point of Failure**: Every node in a Cassandra cluster is equal; no master node. Automatic failover with no downtime.

### 2.2 Data Modeling for Recommendation Interactions

Cassandra data modeling is query-driven — design tables for specific query patterns:

```sql
-- Query: Get user's recent interactions (most common query)
CREATE TABLE user_interactions (
    user_id     UUID,
    event_time  TIMESTAMP,
    item_id     UUID,
    event_type  TEXT,
    event_value FLOAT,
    session_id  TEXT,
    device_type TEXT,
    PRIMARY KEY (user_id, event_time)
) WITH CLUSTERING ORDER BY (event_time DESC)
  AND default_time_to_live = 7776000  -- 90-day TTL
  AND gc_grace_seconds = 864000;

-- Query: Get item's recent interactions (for item-based CF)
CREATE TABLE item_interactions (
    item_id     UUID,
    event_time  TIMESTAMP,
    user_id     UUID,
    event_type  TEXT,
    event_value FLOAT,
    PRIMARY KEY (item_id, event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);

-- Query: Get daily interaction counts (for popularity computation)
CREATE TABLE daily_item_stats (
    item_id     UUID,
    stat_date   DATE,
    view_count  COUNTER,
    click_count COUNTER,
    purchase_count COUNTER,
    PRIMARY KEY (item_id, stat_date)
);
```

### 2.3 Cassandra Operational Considerations

| Aspect | Recommendation | Rationale |
|--------|---------------|-----------|
| Replication Factor | 3 (production) | Tolerates 1 node failure without data loss |
| Consistency Level (writes) | LOCAL_QUORUM | Strong consistency within a data center |
| Consistency Level (reads) | LOCAL_ONE | Low latency; acceptable for non-critical reads |
| Compaction Strategy | TimeWindowCompactionStrategy | Optimal for time-series data with TTL |
| Partition Size | < 100 MB per partition | Prevents hotspots and OOM during compaction |
| Data Retention | TTL-based (90 days for raw events) | Automatic expiry reduces storage costs |

---

## 3. MongoDB for Flexible Schemas

### 3.1 Why MongoDB for Recommendation Systems

- **Flexible Schema**: Item catalogs with diverse attribute types (different product categories have different attributes) are a natural fit for MongoDB's document model.
- **Rich Query Language**: MongoDB supports ad-hoc queries, aggregations, text search, and geospatial queries — useful for item discovery and exploration.
- **Change Streams**: Real-time change streams enable event-driven architectures where downstream services react to data changes.
- **Horizontal Scaling**: MongoDB Atlas or sharded clusters provide native horizontal scaling with automatic sharding.

### 3.2 Document Design for Item Catalog

```javascript
// Product document
{
  "_id": ObjectId("..."),
  "external_id": "itm_12345",
  "title": "Sony WH-1000XM5 Wireless Headphones",
  "description": "Industry-leading noise cancellation...",
  "category_path": ["Electronics", "Audio", "Headphones", "Over-Ear"],
  "brand": "Sony",
  "price": {
    "amount": 349.99,
    "currency": "USD",
    "history": [
      {"date": "2026-01-01", "amount": 399.99},
      {"date": "2026-03-15", "amount": 349.99}
    ]
  },
  "attributes": {
    "color": "Black",
    "weight_grams": 250,
    "battery_life_hours": 30,
    "noise_cancellation": true,
    "wireless": true,
    "connectivity": ["Bluetooth 5.2", "3.5mm jack"]
  },
  "images": [
    {"url": "...", "type": "main", "width": 800, "height": 800},
    {"url": "...", "type": "detail", "width": 1200, "height": 800}
  ],
  "embeddings": {
    "content_embedding": [0.12, -0.45, ...],  // 256-dim
    "image_embedding": [0.33, 0.78, ...]      // 128-dim
  },
  "stats": {
    "view_count": 125000,
    "purchase_count": 8500,
    "avg_rating": 4.6,
    "review_count": 3200
  },
  "status": "active",
  "created_at": ISODate("2025-06-15"),
  "updated_at": ISODate("2026-08-10")
}
```

### 3.3 MongoDB Query Patterns for Recommendations

```javascript
// Find similar items by category and price range
db.items.find({
  "category_path": { $all: ["Electronics", "Audio"] },
  "price.amount": { $gte: 200, $lte: 500 },
  "status": "active",
  "_id": { $ne: current_item_id }
}).sort({ "stats.view_count": -1 }).limit(50);

// Text search on item descriptions
db.items.find(
  { $text: { $search: "wireless noise cancelling" } },
  { score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } }).limit(20);

// Aggregation pipeline for category popularity
db.items.aggregate([
  { $match: { "status": "active", "created_at": { $gte: ISODate("2026-07-01") } } },
  { $group: {
    _id: { $arrayElemAt: ["$category_path", 1] },
    total_views: { $sum: "$stats.view_count" },
    total_purchases: { $sum: "$stats.purchase_count" },
    item_count: { $sum: 1 }
  }},
  { $sort: { total_views: -1 } },
  { $limit: 20 }
]);
```

---

## 4. Redis for Caching and Real-Time Features

### 4.1 Redis Data Structures for Recommendations

| Use Case | Redis Data Structure | Key Pattern | TTL |
|----------|---------------------|-------------|-----|
| User Feature Cache | Hash | `user_features:{user_id}` | 15 min |
| Item Feature Cache | Hash | `item_features:{item_id}` | 1 hour |
| Recommendation Cache | List | `recs:{user_id}:{page_type}` | 30 min |
| Session State | Hash | `session:{session_id}` | 30 min |
| Real-Time Popularity | Sorted Set | `popularity:{category}:{window}` | 24 hour |
| User Interaction History | Sorted Set | `user_history:{user_id}` | 90 days |
| Feature Store (Online) | String (serialized) | `feature:{entity}:{feature_name}` | Varies |

### 4.2 Redis Patterns for Recommendation Serving

**Pattern 1: Recommendation Cache with Stampede Prevention**
```python
def get_recommendations(user_id, page_type):
    cache_key = f"recs:{user_id}:{page_type}"
    
    # Try cache first
    cached = redis.get(cache_key)
    if cached:
        return deserialize(cached)
    
    # Cache miss: use distributed lock to prevent stampede
    lock_key = f"lock:recs:{user_id}:{page_type}"
    if redis.set(lock_key, "1", nx=True, ex=5):  # Lock with 5s TTL
        try:
            # Generate fresh recommendations
            recs = generate_recommendations(user_id, page_type)
            redis.setex(cache_key, 1800, serialize(recs))  # 30 min TTL
            return recs
        finally:
            redis.delete(lock_key)
    else:
        # Another process is generating; wait and retry cache
        time.sleep(0.1)
        cached = redis.get(cache_key)
        return deserialize(cached) if cached else fallback_recommendations()
```

**Pattern 2: Real-Time Feature Updates**
```python
def record_interaction(user_id, item_id, event_type, event_value):
    # Update user history (sorted set by timestamp)
    event_score = time.time()
    redis.zadd(f"user_history:{user_id}", {item_id: event_score})
    redis.zremrangebyrank(f"user_history:{user_id}", 0, -501)  # Keep last 500
    
    # Update item popularity counters
    redis.zincrby(f"popularity:all:1h", 1, item_id)
    redis.zincrby(f"popularity:all:24h", 1, item_id)
    
    # Invalidate user recommendation cache
    redis.delete(f"recs:{user_id}:home")
    redis.delete(f"recs:{user_id}:for_you")
```

### 4.3 Redis Cluster for Production

- **Sharding**: Use Redis Cluster (16,384 hash slots distributed across nodes) for horizontal scaling beyond a single node's memory.
- **Memory Management**: Set maxmemory-policy to allkeys-lru (evict least-recently-used keys when memory is full) for caching use cases.
- **Persistence**: Use RDB snapshots for disaster recovery; AOF for durability if storing critical feature data.
- **Replication**: Each primary has at least one replica for failover. Use Redis Sentinel for automatic failover.

---

## 5. DynamoDB Patterns

### 5.1 DynamoDB Table Design for Recommendations

**Single-Table Design Pattern**:

| PK | SK | Attributes | Access Pattern |
|----|----|-----------|----------------|
| USER#123 | PROFILE | name, email, age_bucket | Get user profile |
| USER#123 | PREF#color | value: "red" | Get user preference |
| USER#123 | HISTORY#2026-08-19T10:00 | item_id, event_type | Get user history |
| ITEM#456 | PROFILE | title, price, category | Get item details |
| ITEM#456 | STATS | views, purchases, rating | Get item statistics |
| ITEM#456 | SIMILAR#001 | similarity: 0.85 | Get similar items |

### 5.2 DynamoDB Capacity Planning

| Workload Type | Provisioned Throughput | Cost Optimization |
|--------------|----------------------|-------------------|
| Steady reads (user profiles) | On-demand or provisioned with auto-scaling | Reserved capacity for predictable workloads |
| Bursty writes (event logging) | On-demand capacity | Pay-per-request for unpredictable spikes |
| Hot partition (popular items) | DAX (DynamoDB Accelerator) for caching | Reduce read capacity with DAX layer |

### 5.3 DynamoDB + DAX for Sub-Millisecond Reads

DAX (DynamoDB Accelerator) is an in-memory cache for DynamoDB that provides:
- **Microsecond reads** for frequently accessed items (popular items, active users).
- **Write-through caching** — writes update both DAX and DynamoDB simultaneously.
- **Multi-layer cache** — item cache (single item lookups) and query cache (query results).

---

## 6. NoSQL vs SQL Decision Framework

### 6.1 Choose SQL When:

- Data has clear relational structure (users, items, interactions).
- ACID transactions are required (financial transactions, profile updates).
- Complex joins and aggregations are needed (co-occurrence analysis, cohort analysis).
- Ad-hoc queries are required (analytics, debugging, data exploration).
- Data volume is moderate (< 1TB).

### 6.2 Choose NoSQL When:

- Write throughput exceeds 10K writes/second per table (interaction logging).
- Horizontal scaling is required without complex sharding logic.
- Schema flexibility is needed (diverse item types, evolving attributes).
- Low-latency key-value lookups are the primary access pattern (feature serving, caching).
- Data volume is very large (> 1TB) and growing rapidly.
- Time-to-live (TTL) based data expiry is a core requirement (session data, event retention).

### 6.3 Hybrid Architecture

Most production recommendation systems use both SQL and NoSQL:

```
PostgreSQL:
├── User profiles (complex queries, transactions)
├── Item catalog (relational integrity, joins)
├── Model registry (metadata, audit)
└── Experiment configurations (ACID)

Cassandra/ScyllaDB:
├── Interaction events (high write throughput)
├── User interaction history (time-series access)
└── Aggregated statistics (daily/hourly rollups)

Redis:
├── User feature cache (sub-ms reads)
├── Recommendation cache (precomputed results)
├── Session state (ephemeral data)
└── Real-time counters (popularity, trending)

MongoDB:
├── Item metadata (flexible schema per item type)
├── Content embeddings (document storage)
└── Semi-structured enrichment data
```
