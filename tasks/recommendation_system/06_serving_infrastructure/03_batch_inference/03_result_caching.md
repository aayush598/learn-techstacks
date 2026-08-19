# Result Caching for Batch Inference

## Overview

Result caching stores pre-computed recommendations from batch inference jobs for fast retrieval at serving time. The cache serves as the bridge between batch computation and real-time serving, enabling sub-millisecond recommendation retrieval. This covers cache freshness, invalidation strategies, multi-tier caching, and cache warming.

---

## Pre-Computed Recommendations

### Storage Schema

```
cache_key: user:{user_id}:context:{context_hash}:model:{version}
cache_value: {
    recommendations: [
        {item_id: "i1", score: 0.95, metadata: {...}},
        {item_id: "i2", score: 0.93, metadata: {...}},
        ...
    ],
    computed_at: "2026-08-15T02:30:00Z",
    model_version: "v1.3.0",
    context: {
        time_bucket: "morning",
        device: "mobile",
        segment: "power_user"
    }
}
```

### Cache Dimensions

| Dimension | Values | Impact |
|-----------|--------|--------|
| User ID | Active user identifier | Personalization |
| Context | Time, device, location | Contextual relevance |
| Model version | Current serving model | Freshness |
| Recommendation type | Homepage, trending, similar | Different caches |
| Region | Geographic location | Local relevance |

---

## Cache Freshness

### Freshness Requirements by Surface

| Surface | Max Staleness | Rationale |
|---------|-------------|-----------|
| Homepage "For You" | 1-4 hours | High visibility, frequent visits |
| Search results | N/A (real-time) | Query-dependent |
| Email recommendations | 24 hours | Delivered once |
| Push notifications | 12 hours | Time-sensitive but not instant |
| "Continue watching" | 2 hours | Session-dependent |
| Social recommendations | 6 hours | Friend activity changes |

### Measuring Freshness

- Track `current_time - computed_at` for served recommendations
- Report freshness distribution (P50, P95, P99)
- Alert when average freshness exceeds threshold
- Compare freshness across user segments

### Freshness vs Quality Trade-off

- Older recommendations may have higher quality (more computation time)
- Newer recommendations reflect latest model and data
- Find optimal TTL per recommendation type through A/B testing
- Consider adaptive freshness based on user activity patterns

---

## Cache Invalidation Strategies

### Time-Based Invalidation (TTL)

```
TTL_Config:
  homepage_recs: 4 hours
  trending: 30 minutes
  similar_items: 7 days
  email_recs: 25 hours
  cold_start: 2 hours
```

**Pros**: Simple, predictable, no coordination needed
**Cons**: May serve stale data or expire useful data prematurely

### Event-Based Invalidation

| Event | Invalidation Action |
|-------|-------------------|
| User purchase | Invalidate user's recommendation cache |
| Item removed from catalog | Invalidate all caches referencing item |
| New model deployed | Invalidate all caches for that model version |
| Feature pipeline update | Invalidate affected feature-dependent caches |
| User preference change | Invalidate user's personalized cache |

### Version-Based Invalidation

- Include model version in cache key
- New model version → new cache key → old cache naturally unused
- Old cache entries expire via TTL
- No explicit invalidation needed (key mismatch)

### Selective Invalidation

- Invalidate only caches affected by the change
- Track dependency between cache entries and upstream data
- Minimize unnecessary cache invalidation
- Batch invalidation requests for efficiency

---

## Multi-Tier Caching

### Three-Tier Architecture

```
Request → L1 (In-Memory) → L2 (Redis Cluster) → L3 (Persistent Store) → Compute
```

### Tier Specifications

| Tier | Technology | Latency | Capacity | Consistency |
|------|-----------|---------|----------|-------------|
| L1 | In-process hash map | < 0.1 ms | 10-100K entries | Per-instance |
| L2 | Redis Cluster | 0.5-2 ms | 10M+ entries | Distributed |
| L3 | DynamoDB/PostgreSQL | 5-20 ms | Unlimited | Strong |
| L4 (compute) | Batch inference | Minutes-hours | Unlimited | Fresh |

### Cache Lookup Flow

1. Check L1 (in-memory) → if hit, return immediately
2. Check L2 (Redis) → if hit, populate L1 and return
3. Check L3 (persistent) → if hit, populate L2 and L1, return
4. Fall back to real-time inference or serve popularity-based

### L1 Cache Management

- Per-instance in-memory cache (no network overhead)
- LRU eviction when capacity reached
- Populate from L2 on L1 miss
- TTL-based expiration aligned with L2
- Consider warming L1 during instance startup

### L2 Cache Distribution

- Consistent hashing across Redis cluster
- Shard by user ID for even distribution
- Replicate each shard for high availability
- Monitor memory usage per shard
- Auto-resharding when approaching capacity limits

---

## Cache Warming for Batch Results

### Post-Batch Warming

After batch job completes:
1. Write results to L3 (persistent store)
2. Asynchronously push to L2 (Redis)
3. L1 populated on first access per instance

### Proactive Warming

- Predict which users will access cache soon (based on historical patterns)
- Pre-warm L2 for predicted active users
- Warm highest-traffic users first
- Complete warming before peak traffic hours

### Warming Strategies

| Strategy | Timing | Coverage | Cost |
|----------|--------|---------|------|
| Full warm | After batch completion | All active users | High |
| Priority warm | Before peak hours | Top 20% users | Medium |
| On-demand warm | First access per user | Individual users | Low |
| Predictive warm | Based on usage patterns | Predicted users | Medium |

### Warming Monitoring

- Track cache hit rate during warming period
- Measure time to full cache warm after batch completion
- Alert if warming is slower than expected
- Monitor cache memory usage during warming

---

## Cache Monitoring and Optimization

### Key Metrics

| Metric | Target | Alert |
|--------|--------|-------|
| L1 hit rate | > 50% | < 30% |
| L2 hit rate | > 90% | < 80% |
| Overall hit rate | > 95% | < 90% |
| Cache latency (P99) | < 5 ms | > 20 ms |
| Cache memory usage | < 80% | > 90% |
| Staleness (P95) | Within TTL | > 120% of TTL |

### Optimization Techniques

- **Request coalescing**: Multiple requests for same key → single fetch
- **Cache partitioning**: Separate caches by recommendation type
- **Compression**: Compress large recommendation lists in cache
- **Predictive prefetching**: Pre-fetch before user requests
- **Negative caching**: Cache "no recommendations" to avoid repeated computation

### Capacity Planning

- Estimate cache size per user (typically 1-10 KB)
- Multiply by active user count for total cache size
- Add 30-50% buffer for growth and fragmentation
- Plan Redis cluster size based on QPS and memory requirements
