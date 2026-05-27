# Rate Limit per Key

## Overview

Per-key rate limiting prevents any single API key from consuming excessive resources. Rate limits are enforced using token bucket or sliding window algorithms with distributed Redis storage.

## Rate Limiter

```typescript
interface KeyRateLimit {
  keyId: string;
  requestsPerMinute: number;
  requestsPerHour: number;
  burstLimit: number;
  concurrentLimit: number;
}

class KeyRateLimiter {
  private redis: Redis;

  async checkRateLimit(keyId: string, limit: KeyRateLimit): Promise<RateLimitResult> {
    const now = Date.now();
    const minuteKey = `ratelimit:${keyId}:minute`;
    const hourKey = `ratelimit:${keyId}:hour`;

    // Sliding window minute counter
    const minuteCount = await this.redis.incr(minuteKey);
    if (minuteCount === 1) {
      await this.redis.pexpire(minuteKey, 60000);
    }

    // Sliding window hour counter
    const hourCount = await this.redis.incr(hourKey);
    if (hourCount === 1) {
      await this.redis.pexpire(hourKey, 3600000);
    }

    // Check concurrent requests
    const concurrentKey = `concurrent:${keyId}`;
    const concurrent = await this.redis.get(concurrentKey) || 0;

    const headers = {
      'X-RateLimit-Limit': limit.requestsPerMinute,
      'X-RateLimit-Remaining': Math.max(0, limit.requestsPerMinute - minuteCount),
      'X-RateLimit-Reset': Math.ceil((now + 60000) / 1000),
    };

    if (minuteCount > limit.requestsPerMinute) {
      return { allowed: false, status: 429, retryAfter: 60, headers };
    }

    if (hourCount > limit.requestsPerHour) {
      return { allowed: false, status: 429, retryAfter: 3600, headers };
    }

    if (Number(concurrent) >= limit.concurrentLimit) {
      return { allowed: false, status: 429, retryAfter: 5, headers };
    }

    return { allowed: true, headers };
  }
}
```

## Rate Limit Tiers

```typescript
const RATE_LIMIT_TIERS: Record<string, KeyRateLimit> = {
  free: { requestsPerMinute: 10, requestsPerHour: 100, burstLimit: 20, concurrentLimit: 2 },
  pro: { requestsPerMinute: 60, requestsPerHour: 1000, burstLimit: 120, concurrentLimit: 10 },
  enterprise: { requestsPerMinute: 300, requestsPerHour: 10000, burstLimit: 500, concurrentLimit: 50 },
};
```

## Open-Source Tools

- **express-rate-limit** (MIT) — Rate limiting middleware
- **rate-limiter-flexible** (MIT) — Distributed rate limiting with Redis

## Production Considerations

- Use Lua scripts for atomic rate limit operations
- Rate limit by key, by IP, and by tenant simultaneously
- Return rate limit headers on every response
- Queue bursts exceeding limit for delayed processing
- Allow tenants to configure custom rate limits
- Monitor rate limit hits per key to detect abuse
- Provide rate limit usage dashboard in developer portal
