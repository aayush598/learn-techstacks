# Chapter 03: Caching Strategy (Multi-Layer)

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [HTTP Caching (CDN/SW)](sec-01-http-caching-cdn-sw.md) | Cache-Control headers, ETags, CDN caching, service worker cache, stale-while-revalidate |
| 02 | [Redis Caching Layer](sec-02-redis-caching-layer.md) | Redis cache patterns, serialization, TTL strategies, eviction policies, cluster mode |
| 03 | [In-Memory Cache](sec-03-in-memory-cache.md) | Local cache (node-cache/lru-cache), cache size limits, invalidation, TTL |
| 04 | [Cache Invalidation Strategies](sec-04-cache-invalidation-strategies.md) | Write-through, write-behind, cache-aside, publish/invalidate, TTL-based |
| 05 | [Cache Warming](sec-05-cache-warming.md) | Pre-warming strategies, scheduled warming, on-demand warming, gradual warming |
| 06 | [Distributed Caching](sec-06-distributed-caching.md) | Redis Cluster, consistency hashing, cache replication, failover |
| 07 | [Application-Level Caching](sec-07-application-level-caching.md) | Response caching, computed value caching, database query caching, partial caching |
| 08 | [Cache Monitoring & Tuning](sec-08-cache-monitoring-tuning.md) | Hit rate monitoring, latency impact, cache size optimization, eviction analysis |
