# Caching Strategies for Recommendation Systems

## 1. Cache Hierarchy

### 1.1 Multi-Level Cache Architecture
```
Level 1: Client Cache (Browser/App)
  ↓ Miss
Level 2: CDN Cache (Edge)
  ↓ Miss
Level 3: API Gateway Cache (Redis)
  ↓ Miss
Level 4: Application Cache (In-Process)
  ↓ Miss
Level 5: Feature Store Cache (Redis Cluster)
  ↓ Miss
Level 6: Model Prediction Cache
  ↓ Miss
Level 7: Origin (Compute from Model)
```

### 1.2 Cache Characteristics by Level

| Level | Latency | TTL | Scope | Hit Rate Target |
|---|---|---|---|---|
| Client Cache | 0ms | 5-60 min | Per user | 30-50% |
| CDN Cache | 1-5ms | 5-60 min | Global | 20-40% |
| Gateway Cache | 1-3ms | 5-15 min | Per user+context | 40-60% |
| Application Cache | <1ms | 1-5 min | Per instance | 10-20% |
| Feature Store | 1-3ms | 1-24 hr | Per entity | 80-95% |
| Model Prediction Cache | 1-3ms | 1-24 hr | Per user+item | 5-15% |

---

## 2. Cache Key Design

### 2.1 Recommendation Cache Keys
```
# Home page recommendations
rec:home:{user_id}:{context_hash}:{variant}

# Similar items
rec:similar:{item_id}:{user_segment}:{limit}

# Trending
rec:trending:{category}:{time_window}

# For you feed
rec:foryou:{user_id}:{page_cursor}:{filters_hash}

# Search results
rec:search:{user_id}:{query_hash}:{filters_hash}:{sort}
```

### 2.2 Feature Cache Keys
```
# User features
feat:user:{user_id}:{feature_group}:{version}

# Item features
feat:item:{item_id}:{feature_group}:{version}

# Interaction features
feat:interact:{user_id}:{item_id}:{feature_group}
```

### 2.3 Cache Key Best Practices
- Include version in key for schema evolution
- Use consistent hashing for key distribution
- Keep keys under 256 bytes
- Use meaningful prefixes for easy invalidation
- Include context for context-dependent recommendations

---

## 3. Cache Invalidation Strategies

### 3.1 TTL-Based Invalidation
- Set appropriate TTL for each cache type
- Personalized recs: 5-15 minutes
- Trending/popular: 5-30 minutes
- Item metadata: 1-24 hours
- User features: 1-6 hours
- Pros: Simple, automatic
- Cons: Stale data possible within TTL window

### 3.2 Event-Driven Invalidation
- Invalidate cache when underlying data changes
- New user interaction → invalidate user's recommendation cache
- New item added → invalidate trending cache
- Model update → invalidate all model-dependent caches
- Pros: Fresh data, no unnecessary invalidations
- Cons: Complexity, potential for missed invalidations

### 3.3 Invalidation Cascade
```
User clicks item
  → Publish UserInteractionEvent
  → Feature Store consumer: Update user features
  → Cache invalidator: Invalidate user's recommendation cache
  → Next request: Cache miss → Fresh recommendations generated
```

### 3.4 Selective Invalidation
- **User-specific**: Invalidate only affected user's cache
- **Item-specific**: Invalidate caches containing specific item
- **Category-specific**: Invalidate caches for affected category
- **Global**: Invalidate all caches (model update, emergency)

---

## 4. Model Prediction Caching

### 4.1 When to Cache Predictions
- Same user requesting similar items multiple times
- Popular items predicted for many users
- Expensive model inference that can be pre-computed
- Batch predictions that can be cached and served

### 4.2 Cache Strategy
```
# Before model inference
cache_key = f"pred:{model_version}:{user_id}:{item_id}"
cached_score = cache.get(cache_key)
if cached_score is not None:
    return cached_score

# Run model inference
score = model.predict(user_features, item_features)
cache.set(cache_key, score, ttl=3600)
return score
```

### 4.3 Prediction Cache Considerations
- **Freshness**: Predictions may become stale; TTL must be short enough
- **Coverage**: Only cache predictions for frequently requested user-item pairs
- **Memory**: Prediction vectors can be large; compress or quantize
- **Invalidation**: Invalidate on model update or feature update

---

## 5. Cache Warming

### 5.1 Proactive Cache Warming
- Pre-compute recommendations for active users during off-peak hours
- Pre-populate feature cache before expected traffic spikes
- Pre-load popular item features into cache
- Schedule warming jobs: daily, hourly, before campaigns

### 5.2 Reactive Cache Warming
- When cache miss detected, immediately compute and cache
- For cold-start users, generate default recommendations and cache
- Warm cache on first request after deployment

### 5.3 Cache Warming for New Deployments
- After model deployment, pre-compute recommendations for top N users
- After feature store update, pre-materialize hot features
- After code deployment, warm application-level caches

---

## 6. Cache Monitoring

### 6.1 Key Metrics
- **Hit Rate**: Percentage of requests served from cache (target: >80% for features)
- **Miss Rate**: Percentage of requests that miss cache
- **Eviction Rate**: How often entries are evicted (too low TTL?)
- **Memory Usage**: Cache memory utilization (should stay <80%)
- **Latency**: Cache read/write latency (should be <3ms)
- **Key Count**: Number of keys in cache
- **Bandwidth**: Cache network bandwidth usage

### 6.2 Cache Dashboards
- Real-time hit/miss rates per cache level
- Cache latency percentiles (P50, P95, P99)
- Memory utilization and eviction trends
- Cache size growth over time
- Per-endpoint cache performance

---

## 7. Cache Sizing

### 7.1 Memory Estimation
```
Number of active users: 1M
Average recommendation cache per user: 5KB (50 items × 100 bytes)
Total recommendation cache: 5GB

Feature cache per user: 2KB
Total feature cache: 2GB

Prediction cache: 10M common user-item pairs × 4 bytes = 40MB

Total cache memory: ~7GB
Safety margin (2x): 14GB
Redis cluster: 3 nodes × 8GB = 24GB
```

### 7.2 Eviction Policy
- **LRU (Least Recently Used)**: Default for most use cases
- **LFU (Least Frequently Used)**: Good for popular items that stay relevant
- **TTL-based**: Combined with LRU for automatic expiration
- **Random**: Simple, predictable performance
