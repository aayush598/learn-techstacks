# Inference Caching for Recommendation Systems

## Overview

Inference caching stores prediction results, intermediate computations, and features to reduce latency and compute costs. At scale, caching is not optional—it's essential for serving millions of requests efficiently. This covers prediction caching, feature caching, result caching, cache warming, and invalidation strategies.

---

## Prediction Caching

### What to Cache

| Cache Type | Content | TTL | Hit Rate Target |
|-----------|---------|-----|----------------|
| User recommendation cache | Top-K items per user | 1-24 hours | > 80% |
| Similar item cache | "Similar items" for each item | 1-7 days | > 90% |
| Trending cache | Top trending items overall/category | 5-60 minutes | > 95% |
| Personalized ranking cache | Re-ranked candidates per user | 1-6 hours | > 70% |

### Cache Key Design

**User-Level Cache Keys**:
```
rec:{user_id}:{context_hash}:{model_version}
```

Where context_hash encodes time-of-day bucket, device type, and location granularity.

**Item-Level Cache Keys**:
```
similar:{item_id}:{model_version}:{top_k}
```

### Cache Granularity Trade-offs

| Granularity | Hit Rate | Freshness | Storage |
|------------|---------|-----------|---------|
| Per-user-per-context | Low | High | High |
| Per-user | High | Medium | Medium |
| Per-user-segment | Very High | Low | Low |
| Per-popularity-tier | Highest | Lowest | Lowest |

---

## Feature Caching

### Feature Categories and Caching

| Feature Type | Update Frequency | Cache Strategy |
|-------------|-----------------|----------------|
| User demographics | Rarely (days-months) | Long TTL, high priority |
| User behavior aggregates | Hourly | Medium TTL |
| Item attributes | Rarely | Long TTL |
| Item popularity | Minutes-hours | Short TTL |
| Real-time session features | Per-event | No cache (compute on-demand) |
| Cross-feature interactions | Depends on inputs | Cache with input-based key |

### Feature Cache Architecture

```
Request → Feature Cache (Redis) → [Miss] → Feature Pipeline → Cache Write
                                  [Hit] → Return cached features
```

### Multi-Level Feature Caching

**L1 Cache (In-Process)**:
- In-memory hash map within inference service
- Sub-microsecond access
- Limited size (10-100K entries)
- Per-instance, not shared

**L2 Cache (Distributed)**:
- Redis or Memcached cluster
- Sub-millisecond access
- Shared across instances
- 10M+ entries

**L3 Cache (Persistent)**:
- Database or disk-based cache
- Millisecond access
- Survives restarts
- Very large capacity

---

## Result Caching

### Caching Full Recommendations

Store complete recommendation lists for fast retrieval:

**Pre-computed Recommendations**:
- Generate recommendations offline (batch job)
- Store in fast-access cache (Redis, DynamoDB)
- Serve from cache on request (< 5ms latency)
- Refresh periodically based on freshness requirements

**Cache Structure**:
```
user_id → {
    recommendations: [item_1, item_2, ..., item_100],
    scores: [0.95, 0.93, ..., 0.45],
    computed_at: timestamp,
    model_version: "v1.3.0",
    context: "homepage"
}
```

### Hybrid Cache + Real-Time

1. Serve pre-computed recommendations from cache (base layer)
2. Apply real-time re-ranking on top (freshness layer)
3. Filter out recently seen/purchased items (dedup layer)
4. Add trending boosts (trending layer)

### Cache Consistency

- Model version changes require cache invalidation
- Feature pipeline changes may invalidate cached features
- New items need cache entries created
- User preference changes need cache refresh

---

## Cache Warming

### Warming Strategies

| Strategy | When | Coverage | Cost |
|----------|------|---------|------|
| Batch pre-warming | After model update | All active users | High |
| Predictive warming | Before peak traffic | Likely-active users | Medium |
| On-demand warming | First request per user | One user at a time | Low |
| Progressive warming | During idle periods | Priority users first | Medium |

### Warming Priority

1. **High-traffic users** (top 10% by request frequency)
2. **New users** (cold-start recommendations are expensive)
3. **Recent active users** (likely to return soon)
4. **All remaining active users** (within last 30 days)
5. **Dormant users** (warm on re-engagement)

### Warming for Model Updates

When a new model is deployed:
1. Immediately invalidate affected cache entries
2. Pre-warm cache for highest-traffic users first
3. Serve stale cache entries with fallback for users not yet warmed
4. Complete warming within SLA (typically < 1 hour for top users)

---

## Cache Invalidation for Model Updates

### Invalidation Strategies

| Strategy | Implementation | Latency Impact | Complexity |
|----------|---------------|----------------|-----------|
| TTL expiration | Wait for natural expiry | Delayed staleness | Low |
| Version-based key | New model version = new cache key | No staleness | Low |
| Explicit invalidation | Event-driven cache clear | Immediate | Medium |
| Progressive invalidation | Invalidate per-user as they request | Gradual | Medium |

### Model Update Cache Flow

```
New model deployed → 
  1. Invalidate all cache entries for old model version
  2. Start background cache warming for top users
  3. Serve fallback (popularity/old model) during warming gap
  4. Cache hit rate recovers as warming completes
  5. Monitor cache hit rate and latency during transition
```

### Stale Cache Handling

- Allow serving stale cache during warming period
- Add staleness indicator to cached responses
- Client can decide whether to accept stale recommendations
- Maximum staleness threshold: reject cache entries older than TTL + grace period

---

## TTL Strategies

### TTL by Content Type

| Content Type | Recommended TTL | Rationale |
|-------------|----------------|-----------|
| Personalized recs | 1-6 hours | Balance freshness vs cost |
| Trending items | 5-30 minutes | Rapidly changing popularity |
| Similar items | 1-7 days | Item relationships stable |
| User segment recs | 6-24 hours | Segment membership changes slowly |
| Cold-start recs | 1-2 hours | Limited personalization |

### Adaptive TTL

- Increase TTL for users with stable preferences
- Decrease TTL for users with volatile behavior
- Adjust TTL based on traffic patterns (shorter during peak hours)
- Use ML model to predict optimal TTL per user

### TTL + Grace Period

```
effective_cache = {
    entry: cached_data,
    valid_until: created_at + TTL,
    stale_until: valid_until + grace_period,
    state: VALID | STALE | EXPIRED
}
```

- **VALID**: Serve from cache, no computation needed
- **STALE**: Serve from cache, trigger background refresh
- **EXPIRED**: Must recompute before serving

---

## Monitoring and Optimization

### Cache Metrics

| Metric | Target | Alert Threshold |
|--------|--------|----------------|
| Hit rate | > 80% | < 70% |
| Miss latency | < 50ms (P99) | > 100ms |
| Cache memory usage | < 80% capacity | > 90% |
| Eviction rate | < 5% per hour | > 15% per hour |
| Staleness rate | < 10% of served | > 20% of served |

### Cache Optimization

- Analyze access patterns to optimize key design
- Monitor hot keys and ensure even distribution across cache shards
- Implement request coalescing: if multiple requests for same key, fetch once
- Use Bloom filters for quick negative lookups (avoid cache penetration for non-existent users)
- Monitor and alert on cache stampedes (thundering herd after TTL expiration)
