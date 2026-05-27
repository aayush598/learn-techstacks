# Section 04: Rate Limiting Strategies

## Overview

Rate limiting strategies protect both the voice platform from external API throttling and external APIs from being overwhelmed by the platform. External APIs enforce rate limits to protect their infrastructure — exceeding these limits results in HTTP 429 (Too Many Requests) responses, temporary or permanent blocking, and degraded integration reliability. The rate limiting layer ensures the platform stays within allowed limits while maximizing throughput.

Rate limiting operates at multiple levels: per-integration (total calls to a specific external API), per-endpoint (calls to specific API endpoints), per-tenant (fair distribution across tenants sharing an integration), and per-adapter-instance (across horizontally scaled instances). The system supports multiple rate limiting algorithms — token bucket (for bursty traffic with average rate enforcement), leaky bucket (for perfectly smooth traffic), sliding window (for precise time-window enforcement matching external API limits), and adaptive rate limiting (dynamically adjusting based on API response headers and error rates).

## Architecture

```
                  Rate Limiting Architecture

   +------------------------------------------------------+
   |              Rate Limiting Manager                    |
   |                                                      |
   |  +------------------+  +-------------------------+   |
   |  | Algorithm        |  | Limit Configuration     |   |
   |  | Selector         |  | (Per integration)       |   |
   |  | • Token bucket   |  | • Max requests          |   |
   |  | • Leaky bucket   |  | • Time window           |   |
   |  | • Sliding window |  | • Burst capacity        |   |
   |  | • Adaptive       |  | • Concurrency max       |   |
   |  +------------------+  +-------------------------+   |
   |  +------------------+  +-------------------------+   |
   |  | Distributed      |  | Adaptive Adjuster      |   |
   |  | Counter Store    |  | • 429 response parsing  |   |
   |  | (Redis)          |  | • Retry-After header    |   |
   |  | • Atomic incr    |  | • Dynamic limit adj     |   |
   |  | • TTL-based      |  | • Backoff calculation  |   |
   |  |   expiry         |  |                         |   |
   |  +------------------+  +-------------------------+   |
   +------------------------------------------------------+
```

## Design Decisions

- **Distributed token bucket with Redis atomic operations over local counters:** Token buckets are stored in Redis using atomic Lua scripts for counter operations. This ensures consistent rate limiting across all application instances without the clock skew issues of distributed local counters. Token refill rates are calculated based on elapsed time since last request rather than periodic timer ticks. Trade-off: Redis dependency adds latency (1-3ms per rate limit check) and operational overhead.

- **Adaptive rate limiting with dynamic limit discovery over static configuration:** Many APIs return rate limit information in response headers (X-RateLimit-Remaining, X-RateLimit-Reset, Retry-After). The adaptive rate limiter reads these headers and dynamically adjusts the internal limit to match the API's current allocation. When 429 responses are received, the limiter backs off according to the Retry-After header. This handles APIs with dynamic or user-specific rate limits. Trade-off: adaptive limiting may be too conservative if the API returns conservative header values.

- **Per-tenant rate limit allocation with guaranteed minimum:** Rate limits are allocated across tenants with a guaranteed minimum (each tenant gets at least N requests per minute) and a shared burst pool (unused capacity is available to any tenant). This prevents one noisy tenant from starving others while ensuring each tenant has a minimum throughput guarantee. Trade-off: shared burst pools require accurate tracking of "borrowed" capacity to prevent overallocation.

## Implementation Approach

```
interface RateLimitConfig {
  algorithm: 'token_bucket' | 'sliding_window' | 'adaptive';
  maxRequests: number;
  windowMs: number;           // Time window in ms
  burstCapacity?: number;      // For token bucket
  concurrency?: number;        // Max concurrent requests
  adaptive?: {
    headerLimit?: string;      // Header for limit (default: X-RateLimit-Limit)
    headerRemaining?: string;  // Header for remaining (default: X-RateLimit-Remaining)
    headerReset?: string;      // Header for reset (default: X-RateLimit-Reset)
    minLimit: number;          // Minimum limit regardless of API response
  };
}

class DistributedRateLimiter {
  constructor(private redis: Redis, private config: RateLimitConfig) {}

  async acquire(key: string, count: number = 1): Promise<boolean> {
    const result = await this.redis.eval(this.tokenBucketScript(), 1, key, {
      count,
      capacity: this.config.burstCapacity || this.config.maxRequests,
      refillRate: this.config.maxRequests / (this.config.windowMs / 1000),
      now: Date.now()
    });
    return result === 1;
  }

  private tokenBucketScript(): string {
    return `
      local key = KEYS[1]
      local count = tonumber(ARGV[1])
      local capacity = tonumber(ARGV[2])
      local refillRate = tonumber(ARGV[3])
      local now = tonumber(ARGV[4])

      local bucket = redis.call('hmget', key, 'tokens', 'lastRefill')
      local tokens = tonumber(bucket[1]) or capacity
      local lastRefill = tonumber(bucket[2]) or now

      local elapsed = math.max(0, now - lastRefill)
      local newTokens = math.min(capacity, tokens + elapsed * refillRate / 1000)

      if newTokens >= count then
        redis.call('hmset', key, 'tokens', newTokens - count, 'lastRefill', now)
        redis.call('expire', key, math.ceil(capacity / refillRate) + 10)
        return 1
      else
        return 0
      end
    `;
  }

  async getWaitTime(key: string): Promise<number> {
    const bucket = await this.redis.hmget(key, 'tokens', 'lastRefill');
    const tokens = parseFloat(bucket[0]) || 0;
    const tokensNeeded = 1 - tokens;
    const refillRate = this.config.maxRequests / (this.config.windowMs / 1000);
    return tokensNeeded > 0 ? Math.ceil(tokensNeeded / refillRate * 1000) : 0;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Bottleneck** (MIT) | Node.js | Rate limiting library |
| **Rate Limiter Flexible** (MIT) | Node.js | Flexible rate limiting |
| **Redis** (BSD) | Data store | Distributed counters |
| **ioredis** (MIT) | Node.js | Redis client |

## Production Considerations

**Scaling:** Rate limit state in Redis must be partitioned by integration key to avoid hot keys. Use Redis Cluster with key hashing to distribute load. For extreme throughput scenarios (1000+ requests/second per integration), consider local rate limiting with periodic sync to Redis for cross-instance coordination. Monitor Redis command latency for rate limit operations.

**Security:** Rate limit bypass attempts (intentional request flooding) should be detected and blocked. Implement admission control at the integration gateway level before requests reach the rate limiter. Rate limit configurations should be immutable by tenant users — only platform administrators should adjust limits.

**Monitoring:** Track rate limit utilization (% of limit consumed), rate limit hit rate (% of requests delayed or rejected), wait time distribution, 429 responses from external APIs, and adaptive limit adjustments. Alert on rate limit utilization > 80% for sustained periods, 429 responses increasing (indicates limit may be set too high), and adaptive limits dropping below 50% of configured limit.
