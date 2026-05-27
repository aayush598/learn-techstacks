# Section 07: Rate Limiting and Throttling

## Overview

Rate limiting and throttling protect both the webhook delivery engine and the consumer endpoints from overload. On the delivery side, rate limits prevent the platform from overwhelming consumer infrastructure during event bursts (e.g., campaign completion, simultaneous call endings). On the consumer side, the rate limiter ensures fair resource allocation across all webhook endpoints, preventing one noisy consumer from consuming all delivery worker capacity.

The rate limiting system implements a two-tier architecture: a global rate limiter (platform-wide outbound HTTP throughput) and per-endpoint rate limiters (individual consumer capacity). Both tiers use the token bucket algorithm for its ability to handle bursts within limits. The system also supports consumer-declared rate limits — endpoints can specify their capacity during registration, and the system respects those limits through adaptive throttling.

## Architecture

```
                Rate Limiting & Throttling

   Webhook Engine → Global Limiter → Per-Endpoint Limiter → Consumer
                          |
   +----------------------------------------------------------+
   |              Rate Limiting Architecture                  |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Global Rate      |  | Per-Endpoint      |            |
   |  | Limiter          |  | Rate Limiter      |            |
   |  | • Platform-wide  |  | • Token bucket    |            |
   |  | • 1000 req/s     |  | • Configurable    |            |
   |  | • Circuit breaker|  | • Adaptive based  |            |
   |  |   on 5xx spike   |  |   on response     |            |
   |  +------------------+  |   times           |            |
   |  +------------------+  +-------------------+            |
   |  | Token Bucket     |  +-------------------+            |
   |  | Algorithm        |  | Leaky Bucket      |            |
   |  | • Burst capacity |  | Fallback          |             |
   |  | • Steady refill  |  | • For strict      |            |
   |  | • Redis-backed   |  |   ordering        |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **Token bucket over fixed-window or sliding-window counters:** The token bucket algorithm allows bursts of up to the bucket capacity (e.g., 100 tokens) while enforcing a steady-state rate (e.g., 100 tokens/second refill). This is ideal for webhook delivery because event bursts are natural (call completion spikes) and should be delivered quickly up to the consumer's declared capacity. Fixed-window counters would introduce sharp cutoffs at window boundaries. Trade-off: token bucket permits short bursts that may exceed the average rate but provides better UX for bursty event patterns.

- **Consumer-declared rate limits with adaptive reduction over hard-coded limits:** Each endpoint can declare its preferred rate limit during registration (`maxRequestsPerSecond`). The system respects this declaration but adaptively reduces the effective rate if the endpoint responds with 429 (rate limited), 5xx errors, or high latency. The adaptive algorithm uses a sliding window of the last 100 responses to calculate an effective capacity. If error rate exceeds 10%, the effective rate is reduced by 50%. Trade-off: adaptive reduction can be overly conservative if the consumer has transient issues but protects consumer infrastructure from cascading failures.

- **Redis-backed distributed rate limiter over in-memory:** Rate limit state is stored in Redis, enabling consistent rate limiting across multiple webhook worker instances. The Lua scripting approach ensures atomic token operations (check + consume). In-memory rate limiting is used as a local optimization cache (synced every second) to reduce Redis round trips. Trade-off: Redis-backed adds ~1ms latency per rate check but ensures consistent limits in horizontally-scaled deployments.

## Implementation Approach

```
interface RateLimitConfig {
  maxRequestsPerSecond: number;
  burstCapacity: number;
  adaptive: boolean;
}

class TokenBucket {
  private capacity: number;
  private refillRate: number;  // tokens per second
  private tokens: number;
  private lastRefill: number;

  constructor(capacity: number, refillRate: number) {
    this.capacity = capacity;
    this.refillRate = refillRate;
    this.tokens = capacity;
    this.lastRefill = Date.now();
  }

  tryConsume(count: number = 1): boolean {
    this.refill();
    if (this.tokens >= count) {
      this.tokens -= count;
      return true;
    }
    return false;
  }

  private refill(): void {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000;
    this.tokens = Math.min(this.capacity, this.tokens + elapsed * this.refillRate);
    this.lastRefill = now;
  }
}

class RedisTokenBucket {
  private redis: Redis;
  private scriptSha: string;

  constructor(redis: Redis) {
    this.redis = redis;
    // Load Lua script for atomic token bucket
    this.scriptSha = 'TOKEN_BUCKET_SHA';
  }

  async tryConsume(key: string, capacity: number, refillRate: number, count: number = 1): Promise<boolean> {
    const result = await this.redis.eval(
      `
      local key = KEYS[1]
      local capacity = tonumber(ARGV[1])
      local refillRate = tonumber(ARGV[2])
      local count = tonumber(ARGV[3])
      local now = tonumber(ARGV[4])

      local bucket = redis.call('HMGET', key, 'tokens', 'lastRefill')
      local tokens = tonumber(bucket[1]) or capacity
      local lastRefill = tonumber(bucket[2]) or now

      local elapsed = math.max(0, (now - lastRefill) / 1000)
      tokens = math.min(capacity, tokens + elapsed * refillRate)

      if tokens >= count then
        tokens = tokens - count
        redis.call('HMSET', key, 'tokens', tokens, 'lastRefill', now)
        redis.call('EXPIRE', key, 3600)
        return 1
      else
        redis.call('HMSET', key, 'tokens', tokens, 'lastRefill', now)
        redis.call('EXPIRE', key, 3600)
        return 0
      end
      `,
      1, key, capacity, refillRate, count, Date.now()
    );
    return result === 1;
  }
}

class AdaptiveRateLimiter {
  private errorWindow: Map<string, number[]> = new Map(); // endpointId → [timestamps]
  private effectiveRates: Map<string, number> = new Map();

  getEffectiveRate(endpointId: string, declaredRate: number): number {
    const effective = this.effectiveRates.get(endpointId);
    if (effective === undefined) return declaredRate;
    return Math.max(1, effective); // Minimum 1 req/s
  }

  recordResponse(endpointId: string, statusCode: number): void {
    const now = Date.now();
    let errors = this.errorWindow.get(endpointId) || [];
    errors = errors.filter(t => now - t < 60000); // 60-second window
    if (statusCode >= 500 || statusCode === 429) {
      errors.push(now);
    }
    this.errorWindow.set(endpointId, errors);

    // Recalculate effective rate every 10 responses
    const currentRate = this.effectiveRates.get(endpointId);
    if (currentRate === undefined || errors.length % 10 === 0) {
      const errorRate = errors.length / 60; // errors per second
      const declaredRate = currentRate || 100;
      if (errorRate > 0.1) { // >10% error rate
        this.effectiveRates.set(endpointId, Math.floor(declaredRate * 0.5));
      } else if (errorRate < 0.01 && errors.length > 10) {
        // Recover: gradually increase rate
        this.effectiveRates.set(endpointId, Math.min(declaredRate, Math.floor((currentRate || 0) * 1.1)));
      }
    }
  }
}

class WebhookRateLimiter {
  private globalBucket: TokenBucket;
  private endpointBuckets: Map<string, RedisTokenBucket>;
  private adaptive: AdaptiveRateLimiter;
  private redis: Redis;

  constructor() {
    this.globalBucket = new TokenBucket(1000, 1000); // 1000 req/s burst, 1000/s steady
    this.endpointBuckets = new Map();
    this.adaptive = new AdaptiveRateLimiter();
  }

  async canDeliver(endpoint: WebhookEndpoint): Promise<boolean> {
    // Global check first
    if (!this.globalBucket.tryConsume()) {
      logger.warn('Global rate limit reached, throttling');
      return false;
    }

    // Per-endpoint check
    const declaredRate = endpoint.rateLimit?.maxRequestsPerSecond || 100;
    const effectiveRate = this.adaptive.getEffectiveRate(endpoint.id, declaredRate);
    const burstCapacity = endpoint.rateLimit?.burstCapacity || Math.ceil(effectiveRate * 2);

    const endpointBucket = this.getEndpointBucket(endpoint.id);
    const allowed = await endpointBucket.tryConsume(
      `ratelimit:endpoint:${endpoint.id}`,
      burstCapacity,
      effectiveRate
    );

    if (!allowed) {
      logger.warn('Endpoint rate limit reached', {
        endpointId: endpoint.id,
        effectiveRate,
        declaredRate,
      });
    }

    return allowed;
  }

  private getEndpointBucket(endpointId: string): RedisTokenBucket {
    if (!this.endpointBuckets.has(endpointId)) {
      this.endpointBuckets.set(endpointId, new RedisTokenBucket(this.redis));
    }
    return this.endpointBuckets.get(endpointId)!;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ioredis (MIT) | Node.js | Redis rate limit storage |
| Bottleneck (MIT) | Node.js | Token bucket implementation |

## Production Considerations

**Scaling:** Rate limiter state in Redis must be highly available — use Redis Sentinel or Cluster. If Redis is unavailable, the rate limiter should fail-open (allow delivery) rather than fail-closed (block all delivery), to prevent a Redis outage from causing a webhook delivery outage. The global rate limit should be set based on platform capacity testing (start at 500 req/s and increase based on consumer feedback).

**Security:** Rate limit keys include endpoint IDs and tenant IDs — ensure keys do not contain sensitive data. The adaptive rate limiter should not penalize endpoints for transient errors (maintain a minimum effective rate of 1 req/s even for failing endpoints). Monitor for rate limit bypass attempts (attackers consuming rate limit capacity to cause denial of service to legitimate endpoints).

**Monitoring:** Track global rate limiter utilization (current throughput vs. capacity), per-endpoint effective rates vs. declared rates, rate limit hit counts, adaptive reduction events, and Redis rate limit operation latency. Alert on global throughput approaching 80% of capacity, any endpoint with effective rate reduced to minimum, and Redis rate limit operation latency exceeding 10ms.
