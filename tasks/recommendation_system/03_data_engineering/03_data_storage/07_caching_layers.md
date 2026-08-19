# Caching Layers — Redis vs Memcached for Recommendation Systems

## 1. Why Caching is Critical for Recommendation Systems

### 1.1 The Latency Imperative

Recommendation systems must serve responses within tight latency budgets (P95 < 200ms). Without caching, every recommendation request would require:
1. Feature store lookup (5–10ms)
2. Candidate retrieval from index (10–30ms)
3. Model inference (5–20ms)
4. Re-ranking and filtering (3–10ms)

Total: 23–70ms without network overhead. With inter-service network hops, this can easily exceed 200ms. Caching eliminates redundant computation and I/O, reducing latency to sub-5ms for cache hits.

### 1.2 Caching Impact at Scale

| Metric | Without Cache | With Cache (70% hit rate) | Savings |
|--------|-------------|--------------------------|---------|
| P50 Latency | 50ms | 15ms | 70% reduction |
| P95 Latency | 180ms | 80ms | 56% reduction |
| Feature Store QPS | 100K/s | 30K/s | 70% reduction |
| Model Inference QPS | 100K/s | 30K/s | 70% reduction |
| Infrastructure Cost | $100K/month | $45K/month | 55% reduction |

---

## 2. Redis vs Memcached Comparison

### 2.1 Feature Comparison

| Feature | Redis | Memcached |
|---------|-------|-----------|
| **Data Structures** | Strings, Lists, Sets, Sorted Sets, Hashes, HyperLogLog, Bitmaps, Streams | Strings only (key-value) |
| **Persistence** | RDB snapshots + AOF log | None (purely in-memory) |
| **Replication** | Master-replica with automatic failover | Client-side replication only |
| **Clustering** | Redis Cluster (hash slot sharding) | Client-side consistent hashing |
| **Pub/Sub** | Built-in pub/sub + Streams | Not supported |
| **TTL Support** | Per-key TTL with EXPIRE/PEXPIRE | Per-key TTL at set time |
| **Memory Efficiency** | Higher overhead per key (~50 bytes) | Lower overhead per key (~10 bytes) |
| **Multi-Threaded** | I/O threading (Redis 6+); single-threaded command execution | Fully multi-threaded |
| **Max Dataset Size** | Limited by RAM; recommended < 50GB per instance | Limited by RAM; recommended < 10GB per instance |
| **License** | Redis Source Available License (formerly BSD) | BSD |

### 2.2 Performance Comparison

| Benchmark | Redis | Memcached |
|-----------|-------|-----------|
| Get Operations/sec (single node) | 100K–200K | 200K–400K |
| Set Operations/sec (single node) | 80K–150K | 150K–300K |
| Latency (P99, local) | < 1ms | < 0.5ms |
| Throughput with 100-byte values | ~120K ops/sec | ~200K ops/sec |
| Throughput with 1KB values | ~90K ops/sec | ~150K ops/sec |
| Throughput with 10KB values | ~40K ops/sec | ~60K ops/sec |

**Key Insight**: Memcached is faster for simple get/set operations due to its simpler architecture and multi-threaded design. Redis is more versatile due to its data structures and persistence, making it the better choice for most recommendation system use cases.

### 2.3 When to Choose Redis

- **Complex Data Structures**: User interaction histories (sorted sets), session state (hashes), real-time counters (hyperloglog).
- **Persistence Required**: Feature cache that must survive restarts without cold-start penalty.
- **Pub/Sub Needed**: Real-time event propagation between services (e.g., cache invalidation events).
- **Clustering Needed**: Large datasets (> 10GB) that require horizontal sharding.
- **Atomic Operations**: Increment/decrement counters, list pushes, set operations without application-level locking.

### 2.4 When to Choose Memcached

- **Pure Caching**: Simple key-value caching with no persistence requirement (e.g., model prediction cache).
- **Multi-Threaded Workload**: High-concurrency workloads that benefit from multi-threaded request handling.
- **Memory Efficiency**: When memory overhead per key matters (millions of small keys).
- **Simplicity**: When the team needs minimal operational complexity.

---

## 3. Cache Strategies for Recommendation Systems

### 3.1 Cache-Aside (Lazy Loading)

The application manages the cache directly — checks cache first, loads from DB on miss.

```
Request → Check Cache → [Hit] → Return cached result
                       → [Miss] → Query DB → Store in Cache → Return result
```

**Implementation for Recommendations**:
```python
def get_recommendations(user_id, page_type):
    cache_key = f"recs:{user_id}:{page_type}"
    
    # Check cache
    cached = redis.get(cache_key)
    if cached:
        return deserialize(cached)
    
    # Cache miss: generate recommendations
    recommendations = recommendation_engine.generate(user_id, page_type)
    
    # Store in cache with TTL
    redis.setex(cache_key, CACHE_TTL, serialize(recommendations))
    
    return recommendations
```

**Pros**: Simple to implement; cache only stores what is actually requested; no stale data in cache (TTL-based expiry).
**Cons**: Cache miss penalty (cold start); first request always hits the backend; thundering herd on popular items.

### 3.2 Write-Through Cache

Writes update both the cache and the database synchronously.

```
Write → Update Cache AND DB simultaneously
Read → Check Cache → [Hit] → Return; [Miss] → NOT POSSIBLE (always in cache after write)
```

**When to Use**: For user feature data that is updated on every interaction and read frequently. The write-through pattern ensures the cache is always fresh.

**Cons**: Write latency increases (must write to both cache and DB); data in cache may be stale if DB is updated externally.

### 3.3 Write-Behind (Write-Back) Cache

Writes update the cache immediately and asynchronously flush to the database.

```
Write → Update Cache → Return immediately → Async flush to DB
Read → Check Cache → [Hit] → Return; [Miss] → Load from DB
```

**When to Use**: For high-throughput event logging where write latency is critical (interaction events, analytics events).

**Cons**: Risk of data loss if cache crashes before flushing to DB; data may be temporarily inconsistent.

### 3.4 Pre-Computation + Cache

Generate recommendations offline (batch job), store results in cache, serve from cache.

```
Batch Job (every 30 min) → Generate recommendations for all active users → Store in cache
Request → Check Cache → [Hit] → Return pre-computed result
```

**When to Use**: For home page recommendations, "For You" feed, and email recommendations where slight staleness (up to 30 minutes) is acceptable.

**Pros**: Zero latency for serving; no backend load during request time; predictable performance.
**Cons**: Stale recommendations; high memory usage (must store recommendations for all active users); batch job complexity.

---

## 4. Cache Invalidation Strategies

### 4.1 TTL-Based Invalidation

Set a time-to-live on each cached item. After TTL expires, the next request triggers a cache miss and refresh.

| Cache Type | Recommended TTL | Rationale |
|-----------|----------------|-----------|
| User Recommendations (home) | 15–30 min | Balance freshness vs. computation cost |
| User Recommendations (for-you) | 5–15 min | Higher freshness requirement |
| Item Features | 1–24 hours | Item features change infrequently |
| User Features | 5–15 min | User features updated on every interaction |
| Model Predictions | 1–5 min | Model scores become stale quickly |
| Search Results | 5–10 min | Query results should be relatively fresh |
| Session State | 30 min | Match session inactivity timeout |

### 4.2 Event-Driven Invalidation

Invalidate cache entries when underlying data changes.

```python
# When a user interacts with an item, invalidate their recommendation cache
def on_interaction(user_id, item_id, event_type):
    # Update the interaction store
    interaction_store.save(user_id, item_id, event_type)
    
    # Invalidate recommendation caches
    redis.delete(f"recs:{user_id}:home")
    redis.delete(f"recs:{user_id}:for_you")
    redis.delete(f"recs:{user_id}:similar_{item_id}")
    
    # Publish invalidation event for other services
    redis.publish("cache_invalidation", json.dumps({
        "type": "user_recommendations",
        "user_id": user_id,
        "timestamp": time.time()
    }))
```

### 4.3 Stampede Prevention

When a popular cache entry expires, many concurrent requests may simultaneously try to regenerate it — the "cache stampede" or "thundering herd" problem.

**Strategy 1: Distributed Locking**
```python
def get_recommendations_with_lock(user_id):
    cache_key = f"recs:{user_id}:home"
    lock_key = f"lock:recs:{user_id}:home"
    
    cached = redis.get(cache_key)
    if cached:
        return deserialize(cached)
    
    # Acquire lock (NX = only if not exists, EX = expiry)
    if redis.set(lock_key, "1", nx=True, ex=5):
        try:
            recs = generate_recommendations(user_id)
            redis.setex(cache_key, 1800, serialize(recs))
            return recs
        finally:
            redis.delete(lock_key)
    else:
        # Another process is generating; wait and retry
        time.sleep(0.05 + random.uniform(0, 0.05))
        cached = redis.get(cache_key)
        return deserialize(cached) if cached else fallback()
```

**Strategy 2: Probabilistic Early Expiration**
```python
def get_recommendations_probabilistic(user_id):
    cache_key = f"recs:{user_id}:home"
    cached = redis.getWithExpiry(cache_key)
    
    if cached:
        value, ttl = cached
        # As TTL approaches zero, probability of refresh increases
        if ttl < 300 and random.random() < (300 - ttl) / 300:
            # Trigger async refresh
            refresh_queue.enqueue(user_id)
        return deserialize(value)
    
    return generate_and_cache(user_id)
```

### 4.4 Cascading Cache Invalidation

When an item's data changes, invalidate all caches that reference that item:

```python
def invalidate_item_caches(item_id):
    # Direct item cache
    redis.delete(f"item:{item_id}")
    
    # Invalidate similarity caches for this item
    similar_items = redis.smembers(f"similar:{item_id}")
    for similar_id in similar_items:
        redis.delete(f"item:{similar_id}")
    
    # Invalidate recommendation caches for users who recently interacted
    recent_users = get_recent_interactors(item_id, hours=24)
    pipe = redis.pipeline()
    for user_id in recent_users:
        pipe.delete(f"recs:{user_id}:home")
        pipe.delete(f"recs:{user_id}:for_you")
    pipe.execute()
```

---

## 5. Distributed Caching Architecture

### 5.1 Cache Hierarchy

```
Request → L1: Application-Level In-Process Cache (ConcurrentHashMap, LRU, 100ms TTL)
        → L2: Redis/Memcached Cluster (shared across instances, 5–30 min TTL)
        → L3: Feature Store / Database (authoritative data source)
```

### 5.2 Multi-Region Cache

| Region | Cache Layer | Replication | Staleness |
|--------|------------|-------------|-----------|
| US-East | Redis Cluster (primary) | Master for US region | Real-time |
| US-West | Redis Cluster (replica) | Cross-region replication | < 30 seconds |
| EU-West | Redis Cluster (replica) | Cross-region replication | < 30 seconds |
| APAC | Redis Cluster (replica) | Cross-region replication | < 30 seconds |

### 5.3 Cache Sizing

**Estimation Formula**:
```
Cache Size = (Active Users × Recommendations per User × Bytes per Recommendation)
           + (Hot Items × Item Feature Size)
           + (Session Store × Active Sessions × Session Size)

Example:
- 10M active users × 100 recommendations × 50 bytes = 50 GB (recommendation cache)
- 1M hot items × 2 KB = 2 GB (item feature cache)
- 500K active sessions × 1 KB = 0.5 GB (session cache)
Total: ~53 GB → Deploy 3-node Redis cluster with 64 GB each (with replication)
```

### 5.4 Monitoring Cache Health

| Metric | Alert Threshold | Investigation Action |
|--------|----------------|---------------------|
| Cache Hit Ratio | < 60% for 5 min | Check TTL settings, key distribution |
| Memory Usage | > 80% of allocated | Scale up or evict less-used keys |
| Eviction Rate | > 100 evictions/sec | Increase memory or reduce cache TTL |
| Connection Count | > 80% of max connections | Scale connection pool or add nodes |
| Replication Lag | > 5 seconds | Check network, disk I/O on replicas |
| Command Latency | P99 > 5ms | Check for slow commands, large keys, blocked operations |

### 5.5 Anti-Patterns to Avoid

- **Caching Everything**: Not all data benefits from caching. Cache data that is read frequently and expensive to compute. Don't cache data that is already fast to retrieve.
- **Ignoring Cache Warming**: After a deployment or cache flush, proactively warm the cache for the most active users before they experience cold-start latency.
- **Using KEYS Command**: The Redis `KEYS` command scans the entire keyspace and blocks the server. Use `SCAN` for production operations.
- **Storing Large Objects**: Objects > 100KB in Redis degrade performance. Use object storage (S3) for large artifacts and cache only references.
- **No Monitoring**: Deploying a cache without hit-ratio, latency, and memory monitoring is flying blind. Always monitor cache health.
