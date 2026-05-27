# Chapter 07: API Performance & Rate Limiting

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [API Response Caching](sec-01-api-response-caching.md) | Response cache headers, CDN caching for API, stale-while-revalidate, cache invalidation |
| 02 | [Connection Keepalive](sec-02-connection-keepalive.md) | HTTP keepalive configuration, connection pooling, TCP tuning, batch HTTP requests |
| 03 | [Response Compression](sec-03-response-compression.md) | Gzip/brotli compression, compression levels, per-content-type compression, streaming compression |
| 04 | [Pagination Strategies](sec-04-pagination-strategies.md) | Cursor-based vs offset pagination, keyset pagination, page size optimization, infinite scroll |
| 05 | [Rate Limit Tiers](sec-05-rate-limit-tiers.md) | Per-tenant rate limits, tier-based limits (free/pro/enterprise), burst limits, rate limit headers |
| 06 | [Rate Limiting Implementation](sec-06-rate-limiting-implementation.md) | Token bucket, sliding window, Redis-based rate limiting, distributed rate limiting |
| 07 | [API Response Payload Optimization](sec-07-api-response-payload-optimization.md) | Field selection (GraphQL/JSON:API), sparse fieldsets, partial responses, compression |
| 08 | [API Gateway Configuration](sec-08-api-gateway-configuration.md) | Gateway caching, request throttling, request validation, API versioning, aggregation |
