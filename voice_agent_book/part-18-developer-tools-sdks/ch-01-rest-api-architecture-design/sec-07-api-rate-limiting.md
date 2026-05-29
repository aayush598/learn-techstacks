# Section 07: API Rate Limiting

## Overview

Rate limiting protects the Voice Agent API from abuse and ensures fair resource distribution across tenants. The system implements a distributed token bucket algorithm, enforced at the API gateway level. Each API key has a configurable rate limit per endpoint group, and clients receive clear rate limit headers to implement proper backoff.

## Architecture

```
Rate Limiting Architecture
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Token Bucket Algorithm:
  ┌──────────────────────────────────┐
  │   Token Bucket per API Key       │
  │                                  │
  │  Capacity: 100 tokens            │
  │  Refill Rate: 10 tokens/second   │
  │                                  │
  │  [● ● ● ● ● ○ ○ ○ ○ ○]          │
  │   ├── Available tokens           │
  │   └── Empty slots (refilling)    │
  └──────────────────────────────────┘

Request Flow:
  [Request] → [API Gateway] → [Redis Cluster]
                                  │
                    ┌─────────────┴─────────────┐
                    │  Token Bucket Check        │
                    │  Key: ratelimit:va_live_X  │
                    │                            │
                    │  Tokens > 0?               │
                    │   ├── Yes → Consume 1      │
                    │   │        → Forward       │
                    │   └── No  → 429 Response   │
                    └────────────────────────────┘

Rate Limit Headers:
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 42
  X-RateLimit-Reset: 1684512345
  Retry-After: 5
```

## Design Decisions

- **Token Bucket Over Fixed Window**: Token bucket allows bursts while maintaining average rate; fixed window can cause thundering herd at window boundaries
- **Distributed via Redis**: Redis cluster provides atomic token operations across multiple gateway instances
- **Per-Endpoint Tiers**: Different rate limits for different endpoint tiers — `/v1/calls` limits are stricter than `/v1/agents` reads
- **Redis Lua Scripts**: Atomic token consumption using Lua scripting prevents race conditions

## Implementation Approach

```typescript
// Rate limit configuration
interface RateLimitConfig {
  capacity: number;      // Burst capacity
  refillRate: number;    // Tokens per second
  refillInterval: number; // Milliseconds between refills
}

const DEFAULT_RATE_LIMITS: Record<string, RateLimitConfig> = {
  'agents:read':   { capacity: 1000, refillRate: 100, refillInterval: 1000 },
  'agents:write':  { capacity: 100,  refillRate: 10,  refillInterval: 1000 },
  'calls:read':    { capacity: 100,  refillRate: 20,  refillInterval: 1000 },
  'calls:write':   { capacity: 10,   refillRate: 2,   refillInterval: 1000 },
  'analytics':     { capacity: 50,   refillRate: 5,   refillInterval: 1000 },
};

// Token bucket implementation with Redis Lua
const CONSUME_TOKEN_SCRIPT = `
  local key = KEYS[1]
  local capacity = tonumber(ARGV[1])
  local refillRate = tonumber(ARGV[2])
  local now = tonumber(ARGV[3])
  local cost = tonumber(ARGV[4])

  local bucket = redis.call('HMGET', key, 'tokens', 'lastRefill')
  local tokens = tonumber(bucket[1]) or capacity
  local lastRefill = tonumber(bucket[2]) or now

  -- Refill tokens based on elapsed time
  local elapsed = now - lastRefill
  local refill = math.floor(elapsed * refillRate / 1000)
  if refill > 0 then
    tokens = math.min(capacity, tokens + refill)
  end

  if tokens >= cost then
    tokens = tokens - cost
    redis.call('HMSET', key, 'tokens', tokens, 'lastRefill', now)
    redis.call('EXPIRE', key, 60)
    return {1, tokens, capacity, math.ceil((capacity - tokens) / refillRate * 1000)}
  else
    local resetIn = math.ceil((capacity - tokens) / refillRate * 1000)
    return {0, tokens, capacity, resetIn}
  end
`;

class RateLimiter {
  constructor(private redis: Redis) {}

  async check(key: string, config: RateLimitConfig, cost = 1): Promise<RateLimitResult> {
    const now = Date.now();
    const result = await this.redis.eval(
      CONSUME_TOKEN_SCRIPT,
      1,
      `ratelimit:${key}`,
      config.capacity,
      config.refillRate,
      now,
      cost,
    ) as [number, number, number, number];

    const [allowed, remaining, limit, resetIn] = result;

    return {
      allowed: allowed === 1,
      remaining,
      limit,
      resetIn,
    };
  }
}

// Rate limit middleware
function rateLimit(config: RateLimitConfig) {
  return async (c: Context, next: Next) => {
    const apiKey = c.get('apiKey');
    const endpointGroup = c.get('endpointGroup');
    const key = `${apiKey}:${endpointGroup}`;

    const result = await rateLimiter.check(key, config);

    c.header('X-RateLimit-Limit', result.limit.toString());
    c.header('X-RateLimit-Remaining', result.remaining.toString());
    c.header('X-RateLimit-Reset', Math.ceil(Date.now() / 1000 + result.resetIn / 1000).toString());

    if (!result.allowed) {
      c.header('Retry-After', Math.ceil(result.resetIn / 1000).toString());
      throw new ApiErrorResponse(429, 'RATE_LIMITED',
        `Rate limit exceeded. Retry after ${Math.ceil(result.resetIn / 1000)} seconds`);
    }

    await next();
  };
}
```

## Integration Points

- **Redis Cluster**: Distributed token state across gateway instances
- **API Gateway**: Rate limiting enforced before authentication to reject early
- **SDK Backoff**: SDK reads Retry-After headers and implements automatic backoff

## Production Considerations

- **Key Space Management**: Each API key + endpoint group creates a Redis key; set TTL to auto-clean inactive keys
- **Graceful Degradation**: If Redis is unreachable, fall back to local in-memory rate limiting with reduced limits
- **Per-Tenant Overrides**: Enterprise tenants may negotiate higher limits via overrides store in database
- **Rate Limit Analytics**: Track rate limit hit rates to identify abusive patterns and adjust limits

## Open-Source Tools

- **Redis**: In-memory data store for distributed rate limiting
- **Upstash**: Serverless Redis compatible with edge runtimes
