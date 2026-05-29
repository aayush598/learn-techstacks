# Section 07: Rate Limiting per Tenant

Per-tenant rate limiting ensures fair resource distribution by capping the request volume each tenant can send to the API. Unlike the API key rate limiting (per-key), tenant rate limiting is per-tenant regardless of how many keys or users they have. This prevents a single tenant with many keys from overwhelming the system.

Rate limit architecture: token bucket algorithm per tenant, limits defined in tenant plan (requests per second, burst capacity), Redis-backed counters (sorted sets for sliding window), distributed lock-free decrement via Lua scripts for atomicity. Limits are checked at the API gateway before any business logic.

Rate limit response uses standard 429 status with headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset. The response body includes the reset time in ISO 8601. Retry-After header indicates seconds until quota replenishes. Rate limit metrics are exposed for monitoring and alerting.
