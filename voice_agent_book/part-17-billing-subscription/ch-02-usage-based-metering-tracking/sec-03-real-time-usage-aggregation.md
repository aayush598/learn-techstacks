# Section 03: Real-Time Usage Aggregation

## Redis Counters

Redis is the foundation of real-time usage aggregation. Its atomic increment operations, high throughput, and low latency make it ideal for maintaining counters that are updated on every usage event. Each counter tracks a specific meter for a specific tenant.

Counter keys follow a hierarchical pattern: `usage:{tenantId}:{meter}:{period}`. This allows efficient scanning and expiration at period boundaries.

```typescript
class RealtimeCounter {
  private redis: Redis;
  private readonly KEY_TTL = 90 * 24 * 60 * 60; // 90 days

  async increment(
    tenantId: string,
    meter: string,
    quantity: number,
    period: string // '2025-06'
  ): Promise<number> {
    const key = `usage:${tenantId}:${meter}:${period}`;
    const newTotal = await this.redis.incrByFloat(key, quantity);
    await this.redis.expire(key, this.KEY_TTL);
    return newTotal;
  }

  async getCurrentUsage(
    tenantId: string,
    meter: string,
    period: string
  ): Promise<number> {
    const key = `usage:${tenantId}:${meter}:${period}`;
    const value = await this.redis.get(key);
    return parseFloat(value || '0');
  }

  async getBulkUsage(
    tenantIds: string[],
    meter: string,
    period: string
  ): Promise<Map<string, number>> {
    const pipeline = this.redis.pipeline();
    for (const tenantId of tenantIds) {
      pipeline.get(`usage:${tenantId}:${meter}:${period}`);
    }
    const results = await pipeline.exec();
    const usage = new Map<string, number>();
    results.forEach(([err, val], i) => {
      usage.set(tenantIds[i], parseFloat((val as string) || '0'));
    });
    return usage;
  }
}
```

## Sliding Window Aggregation

For rate limits and concurrent usage tracking, sliding window aggregation provides a rolling view of usage within a configurable time window. This is distinct from the fixed-period counters used for billing.

```typescript
class SlidingWindowCounter {
  private redis: Redis;

  async incrementSlidingWindow(
    tenantId: string,
    meter: string,
    quantity: number,
    windowMs: number
  ): Promise<number> {
    const now = Date.now();
    const windowKey = `sliding:${tenantId}:${meter}`;

    // Add current count with timestamp
    await this.redis.zadd(windowKey, now, `${now}:${Math.random()}`);
    await this.redis.incrByFloat(`${windowKey}:total`, quantity);

    // Remove entries outside window
    const cutoff = now - windowMs;
    const removed = await this.redis.zremrangebyscore(windowKey, 0, cutoff);

    if (removed > 0) {
      // Recalculate total (simplified — production would use accurate tracking)
      const count = await this.redis.zcard(windowKey);
      if (count === 0) {
        await this.redis.del(`${windowKey}:total`);
        return quantity;
      }
    }

    const total = await this.redis.get(`${windowKey}:total`);
    return parseFloat(total || '0');
  }
}
```

```
Sliding Window vs Fixed Window:
┌─────────────────────────────────────────────────────────────────┐
│ Fixed Window (Billing):                                         │
│                                                                  │
│  June 1 ────────────────────────────────────────────── June 30  │
│  │      │      │      │      │      │      │      │            │
│  ├──────┴──────┴──────┴──────┴──────┴──────┴──────┴────────────┤
│  │                       15,432 min                             │
│  └──────────────────────────────────────────────────────────────┘
│                                                                  │
│ Sliding Window (Rate Limits):                                    │
│                                                                  │
│  [─────── 1 hour window ───────]                                │
│       ↑ now                                                     │
│  [─────────── 1 hour window ───────────]                        │
│            ↑ earlier                                             │
└─────────────────────────────────────────────────────────────────┘
```

## Pre-Aggregated Rollups

For efficient querying, raw usage events are periodically rolled up into pre-aggregated summary tables. Rollups run on a schedule (every 5 minutes for billing, hourly for analytics) and aggregate events by tenant, meter, and time bucket.

```typescript
interface UsageRollup {
  tenantId: string;
  meterId: string;
  bucketStart: string;  // ISO timestamp for bucket start
  bucketEnd: string;
  total: number;
  count: number;        // Number of raw events
  min: number;
  max: number;
  lastValue: number;
}

async function rollupUsage(bucketMinutes: number = 5): Promise<void> {
  const now = new Date();
  const bucketStart = new Date(now.getTime() - bucketMinutes * 60 * 1000);

  const rawEvents = await db.usageRecords.find({
    eventTimestamp: {
      $gte: bucketStart,
      $lt: now,
    },
    rollupStatus: 'pending',
  });

  // Group and aggregate
  const grouped = groupBy(rawEvents, ['tenantId', 'meterId']);
  const rollups: UsageRollup[] = [];

  for (const [key, events] of Object.entries(grouped)) {
    const [tenantId, meterId] = key.split(':');
    const quantities = events.map(e => e.quantity);

    rollups.push({
      tenantId,
      meterId,
      bucketStart: bucketStart.toISOString(),
      bucketEnd: now.toISOString(),
      total: quantities.reduce((a, b) => a + b, 0),
      count: quantities.length,
      min: Math.min(...quantities),
      max: Math.max(...quantities),
      lastValue: quantities[quantities.length - 1],
    });
  }

  // Batch insert rollups
  await db.usageRollups.bulkCreate(rollups);

  // Mark events as rolled up
  await db.usageRecords.updateMany(
    { _id: { $in: rawEvents.map(e => e._id) } },
    { rollupStatus: 'completed' }
  );
}
```

## Eventual Consistency Trade-offs

Redis counters are eventually consistent — there's a small window where the counter hasn't been updated after a crash. For billing purposes, we rely on the PostgreSQL-stored aggregated data rather than Redis. Redis provides approximate real-time visibility for dashboards and alerts.

```
Consistency Model:
┌──────────────────────────────────────────────────────────────────┐
│ Layer            │ Consistency  │ Latency  │ Source of Truth     │
├──────────────────┼──────────────┼──────────┼─────────────────────┤
│ Redis Counter    │ Eventual     │ <1ms     │ Approximate (alerts)│
│ Rollup Tables    │ Strong       │ <5 min   │ Billing (Stripe)    │
│ Raw Events       │ Strong       │ <10s     │ Audit & Reconcil.   │
│ Stripe Records   │ Strong       │ <5 min   │ Final Invoice       │
└──────────────────────────────────────────────────────────────────┘
```

The rule: Redis is fast but fuzzy, PostgreSQL is accurate but slower, Stripe is the ultimate source of truth for billing.

## Open-Source Tools

- **Redis** (BSD-3) — Real-time counters and sliding window tracking
- **Redis Stack** (Redis Source Available) — RedisTimeSeries for time-series counter data
- **BullMQ** (MIT) — Scheduled rollup jobs
- **ClickHouse** (Apache 2.0) — Rollup storage and analytics queries

## Integration Points

Real-time aggregation feeds the quota checking middleware (Part 8), the usage alert system (Chapter 7 Section 3), the dashboard analytics (Part 12), and the billing engine's Stripe usage record submission.

## Production Considerations

- Use Redis Cluster for horizontal scaling of counters
- Monitor Redis memory usage per tenant pattern
- Implement counter persistence with Redis AOF
- Handle Redis failover gracefully (degrade to PostgreSQL reads)
- Roll up counters to PostgreSQL periodically for durability
- Alert on counter drift between Redis and PostgreSQL

## Open-Source First Philosophy

Redis (BSD-3) handles tens of millions of increments per second on a single node, making it the go-to real-time counter for usage-based billing. Combined with BullMQ for rollup scheduling and ClickHouse for analytical aggregation, this all-open-source stack replaces proprietary solutions from Stripe (Metering API premium tier) and AWS (CloudWatch usage metrics).
