# Usage Tracking & Quotas

## Overview

Usage tracking records every API call made with a key, enabling quota enforcement, billing, and analytics. Quotas can be daily or monthly with configurable overage handling.

## Usage Recording

```typescript
interface ApiKeyUsage {
  id: string;
  keyId: string;
  timestamp: Date;
  endpoint: string;
  method: string;
  statusCode: number;
  latencyMs: number;
  bytesOut: number;
  requestId: string;
}

interface ApiKeyQuota {
  keyId: string;
  dailyLimit: number;
  monthlyLimit: number;
  dailyUsed: number;
  monthlyUsed: number;
  resetAtDaily: Date;
  resetAtMonthly: Date;
}

class UsageTrackingService {
  async recordUsage(usage: Omit<ApiKeyUsage, 'id'>): Promise<void> {
    await this.db.insert('api_key_usage', {
      ...usage,
      id: generateId('usage'),
    });

    // Update counters
    const today = new Date().toISOString().slice(0, 10);
    await this.redis.incr(`usage:daily:${usage.keyId}:${today}`);
    await this.redis.incr(`usage:monthly:${usage.keyId}:${new Date().getMonth()}`);
  }

  async checkQuota(keyId: string): Promise<QuotaStatus> {
    const today = new Date().toISOString().slice(0, 10);
    const daily = Number(await this.redis.get(`usage:daily:${keyId}:${today}`) || 0);
    const monthly = Number(await this.redis.get(`usage:monthly:${keyId}:${new Date().getMonth()}`) || 0);

    const quota = await this.db.findOne('api_key_quotas', { keyId });
    if (!quota) return { withinQuota: true, daily, monthly };

    return {
      withinQuota: daily <= quota.dailyLimit && monthly <= quota.monthlyLimit,
      daily,
      dailyLimit: quota.dailyLimit,
      monthly,
      monthlyLimit: quota.monthlyLimit,
      overage: daily > quota.dailyLimit || monthly > quota.monthlyLimit,
    };
  }
}
```

## Overage Handling

```typescript
async function handleOverage(keyId: string, quota: QuotaStatus): Promise<void> {
  if (!quota.overage) return;

  const config = await getKeyConfig(keyId);
  if (config.overageAllowed) {
    await billingService.chargeOverage(keyId, quota);
    await notificationService.warn({
      type: 'quota_overage',
      keyId,
      usage: `${quota.daily}/${quota.dailyLimit} daily`,
    });
  } else {
    await revokeKeyForBilling(keyId);
  }
}
```

## Open-Source Tools

- **Redis** — Atomic counters for usage tracking
- **ClickHouse** (Apache 2.0) — Time-series usage analytics

## Production Considerations

- Use Redis atomic counters for real-time quota checks
- Persist usage to database in batches for historical analysis
- Reset daily counters at midnight UTC
- Provide usage analytics dashboard per key
- Support usage alerts at 50%, 80%, 90%, 100% thresholds
- Allow overage with auto-charge or block on quota exceeded
- Retain usage data for 13 months for billing cycles
