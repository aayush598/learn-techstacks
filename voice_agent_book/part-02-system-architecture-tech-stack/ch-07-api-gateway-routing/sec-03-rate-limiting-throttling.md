# Section 03: Rate Limiting & Throttling

## Rate Limit Architecture

Rate limiting uses a **token bucket algorithm** implemented in Redis, with per-key counters for API keys, IP addresses, and user IDs. Limits are tiered and burst allowance provides short-term flexibility.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RATE LIMITING ARCHITECTURE                       │
│                                                                     │
│  ┌──────────┐     ┌────────────────────┐    ┌──────────────────┐   │
│  │  Client  │────→│   API Gateway      │───→│   Rate Limiter   │   │
│  │  Request │     │   Middleware        │    │   Middleware     │   │
│  └──────────┘     └────────────────────┘    └────────┬─────────┘   │
│                                                      │              │
│                                                      ▼              │
│                                           ┌────────────────────┐   │
│                                           │   Redis Cluster    │   │
│                                           │                    │   │
│                                           │  ┌──────────────┐  │   │
│                                           │  │  Token Bucket │  │   │
│                                           │  │  rate_limit:  │  │   │
│                                           │  │  {api_key}:{  │  │   │
│                                           │  │  window_tokens│  │   │
│                                           │  │  }            │  │   │
│                                           │  └──────────────┘  │   │
│                                           │  ┌──────────────┐  │   │
│                                           │  │  Tier Config │  │   │
│                                           │  │  {tier}:{    │  │   │
│                                           │  │  max_tokens  │  │   │
│                                           │  │  refill_rate │  │   │
│                                           │  │  burst_limit │  │   │
│                                           │  │  }           │  │   │
│                                           │  └──────────────┘  │   │
│                                           └────────────────────┘   │
│                                                      │              │
│                                                      ▼              │
│                                           ┌────────────────────┐   │
│                                           │   Decision         │   │
│                                           │   ┌──────────────┐ │   │
│                                           │   │ Under Limit  │ │   │
│                                           │   │  → Proceed   │ │   │
│                                           │   └──────────────┘ │   │
│                                           │   ┌──────────────┐ │   │
│                                           │   │ Over Limit   │ │   │
│                                           │   │  → 429 +     │ │   │
│                                           │   │  Retry-After │ │   │
│                                           │   └──────────────┘ │   │
│                                           └────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Tier-Based Rate Limits

```typescript
interface RateLimitTier {
  name: string;
  requestsPerWindow: number;
  windowSeconds: number;
  burstLimit: number;         // Max tokens in bucket
  refillRate: number;         // Tokens per second
  concurrentLimit: number;    // Max concurrent requests
  costPerRequest: number;     // Token cost (1 for standard, >1 for expensive ops)
}

const RATE_LIMIT_TIERS: Record<string, RateLimitTier> = {
  free: {
    name: 'Free',
    requestsPerWindow: 10,
    windowSeconds: 60,
    burstLimit: 20,
    refillRate: 0.17,   // 10/60 tokens per second
    concurrentLimit: 2,
    costPerRequest: 1,
  },
  starter: {
    name: 'Starter',
    requestsPerWindow: 60,
    windowSeconds: 60,
    burstLimit: 100,
    refillRate: 1,
    concurrentLimit: 5,
    costPerRequest: 1,
  },
  pro: {
    name: 'Pro',
    requestsPerWindow: 300,
    windowSeconds: 60,
    burstLimit: 500,
    refillRate: 5,
    concurrentLimit: 20,
    costPerRequest: 1,
  },
  business: {
    name: 'Business',
    requestsPerWindow: 1000,
    windowSeconds: 60,
    burstLimit: 2000,
    refillRate: 16.7,
    concurrentLimit: 50,
    costPerRequest: 1,
  },
  enterprise: {
    name: 'Enterprise',
    requestsPerWindow: -1,    // Custom
    windowSeconds: 60,
    burstLimit: -1,
    refillRate: -1,
    concurrentLimit: -1,
    costPerRequest: 1,
  },
};
```

## Token Bucket Implementation

```typescript
interface TokenBucket {
  key: string;
  tokens: number;
  lastRefill: number; // Unix timestamp
  maxTokens: number;
  refillRate: number; // Tokens per second
}

async function checkRateLimit(key: string, tier: RateLimitTier): Promise<RateLimitResult> {
  const bucket = await redis.get<TokenBucket>(`rate_limit:${key}`);

  if (!bucket) {
    // Initialize new bucket
    const newBucket: TokenBucket = {
      key,
      tokens: tier.burstLimit,
      lastRefill: Date.now(),
      maxTokens: tier.burstLimit,
      refillRate: tier.refillRate,
    };
    await redis.set(`rate_limit:${key}`, newBucket, { EX: tier.windowSeconds });
    return { allowed: true, remaining: tier.burstLimit - 1, reset: Date.now() + tier.windowSeconds * 1000 };
  }

  // Refill tokens based on elapsed time
  const now = Date.now();
  const elapsed = (now - bucket.lastRefill) / 1000;
  const refillAmount = elapsed * bucket.refillRate;
  bucket.tokens = Math.min(bucket.maxTokens, bucket.tokens + refillAmount);
  bucket.lastRefill = now;

  if (bucket.tokens < tier.costPerRequest) {
    const waitTime = Math.ceil((tier.costPerRequest - bucket.tokens) / tier.refillRate);
    return {
      allowed: false,
      remaining: 0,
      reset: now + waitTime * 1000,
      retryAfter: waitTime,
    };
  }

  bucket.tokens -= tier.costPerRequest;
  await redis.set(`rate_limit:${key}`, bucket, { EX: tier.windowSeconds });

  return {
    allowed: true,
    remaining: Math.floor(bucket.tokens),
    reset: now + tier.windowSeconds * 1000,
  };
}
```

## Rate Limit Headers

```typescript
function setRateLimitHeaders(response: NextResponse, result: RateLimitResult, tier: RateLimitTier): void {
  response.headers.set('X-RateLimit-Limit', String(tier.requestsPerWindow));
  response.headers.set('X-RateLimit-Remaining', String(result.remaining));
  response.headers.set('X-RateLimit-Reset', String(Math.ceil(result.reset / 1000)));
  response.headers.set('X-RateLimit-Burst', String(tier.burstLimit));

  if (!result.allowed) {
    response.headers.set('Retry-After', String(result.retryAfter));
  }
}

// 429 response for rate-limited requests
function rateLimitExceeded(result: RateLimitResult): NextResponse {
  return NextResponse.json({
    success: false,
    error: {
      code: 'rate_limit_exceeded',
      message: `Rate limit exceeded. Retry after ${result.retryAfter} seconds.`,
      details: {
        retryAfter: result.retryAfter,
        resetAt: new Date(result.reset).toISOString(),
      },
    },
  }, {
    status: 429,
    headers: {
      'Retry-After': String(result.retryAfter),
      'X-RateLimit-Remaining': '0',
    },
  });
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Algorithm | Token bucket | Supports bursts, smooth refill, cost-weighted requests |
| Storage | Redis | Sub-millisecond reads, atomic operations, TTL auto-cleanup |
| Key strategy | API key primary, IP fallback | Authenticated users get tier-based limits, anonymous get IP limits |
| Window | Sliding window via token refill | No wall-clock window boundaries, fairer than fixed window |
| Concurrency | Separate counter | Prevents request pileup on slow endpoints |

## Integration Points

- **Ch 03 (Database)** — Rate limit tier stored in tenant billing plan
- **Ch 05 (Microservices)** — Service-level rate limiting for inter-service calls
- **Ch 10 (Security)** — DDoS protection via aggressive rate limiting at edge

## Production Considerations

- **Redis Failure Mode**: If Redis is unreachable, rate limiter falls back to in-memory approximate counters
- **Distributed Consistency**: Token bucket state is eventually consistent — small overages possible during failover
- **Cost-Weighted Endpoints**: POST /api/v1/calls costs 5 tokens (expensive), GET costs 1 token
- **Monitoring**: Rate limit hit rate tracked per tier; alerts on > 50% hit rate for paid tiers
- **Dashboard**: Tenants see their rate limit usage in real-time on the API dashboard
