# Section 04: Credit-Free Testing Mode

## Overview

Sandbox testing does not consume billing credits or count toward usage quotas. All API operations in the sandbox environment are free, with higher rate limits to accommodate development workloads. Usage quotas in the sandbox are separate from production and designed to prevent abuse rather than generate revenue.

## Architecture

```
Credit-Free Testing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Billing Decision Flow:
  [API Request] → [Environment Detection]
                      │
          ┌───────────┴───────────┐
          │ Sandbox               │ Production
          ▼                       ▼
  [No Billing Check]      [Check Credits]
  [Skip Usage Recording]  [Deduct Credits]
  [Allow All Features]    [Check Limits]
          │                       │
          ▼                       ▼
  [Process Request]       [Process or Reject]

Sandbox Quotas:
  Resource               Sandbox Limit        Production Limit
  ──────────────────────────────────────────────────────────────
  API Requests/min       300 RPM              100 RPM
  Agents per tenant      100                  50
  Concurrent calls       25                   10
  Test numbers           10                   0
  Storage                1 GB                 10 GB
  Data retention         7 days               365 days

Sandbox Key Features:
  ✓ No credit card required
  ✓ All premium features available
  ✓ Higher rate limits
  ✓ Full request logging
  ✓ Data reset on demand
  ✗ Real phone calls (test numbers only)
  ✗ Production SLA (best effort)
```

## Design Decisions

- **Separate Rate Limits**: Sandbox has higher limits for development iteration
- **No Payment Required**: Sign up for sandbox with email only — no credit card
- **Feature Parity**: All premium API features available in sandbox (no feature gating)
- **Usage Tracking**: Sandbox usage tracked for abuse detection, not billing

## Implementation Approach

```typescript
// Sandbox quota manager
interface SandboxQuota {
  tenantId: string;
  apiRequestsMinute: number;
  totalAgents: number;
  concurrentCalls: number;
  storageBytes: number;
  lastResetAt: Date;
}

class SandboxQuotaManager {
  private readonly DEFAULTS = {
    apiRequestsMinute: 300,
    totalAgents: 100,
    concurrentCalls: 25,
    storageBytes: 1_073_741_824, // 1 GB
  };

  async checkQuota(tenantId: string, resource: keyof SandboxQuota): Promise<boolean> {
    const usage = await this.getUsage(tenantId);
    const limit = this.DEFAULTS[resource];

    return usage[resource] < limit;
  }

  async trackUsage(tenantId: string, resource: keyof SandboxQuota, amount = 1): Promise<void> {
    const key = `sandbox:usage:${tenantId}:${resource}`;
    await this.redis.incrby(key, amount);
    await this.redis.expire(key, 60); // Reset per-minute counters
  }

  async getUsage(tenantId: string): Promise<SandboxQuota> {
    const [requests, agents, calls, storage] = await Promise.all([
      this.redis.get(`sandbox:usage:${tenantId}:apiRequestsMinute`),
      this.db.count('agents', { tenantId }),
      this.redis.get(`sandbox:usage:${tenantId}:concurrentCalls`),
      this.getStorageUsage(tenantId),
    ]);

    return {
      tenantId,
      apiRequestsMinute: parseInt(requests || '0'),
      totalAgents: agents,
      concurrentCalls: parseInt(calls || '0'),
      storageBytes: storage,
      lastResetAt: new Date(),
    };
  }
}

// Billing middleware — no-op for sandbox
function billingMiddleware(environment: string) {
  return async (c: Context, next: Next) => {
    if (environment === 'sandbox') {
      // Skip all billing checks
      await next();
      return;
    }

    // Production billing logic
    const tenantId = c.get('tenantId');
    const credits = await billingService.getCredits(tenantId);

    if (credits.remaining <= 0) {
      throw new ApiErrorResponse(402, 'INSUFFICIENT_CREDITS', 'Insufficient credits');
    }

    await next();

    // Deduct credits after successful response
    if (c.res.statusCode < 400) {
      await billingService.deductCredits(tenantId, 1);
    }
  };
}

// Sandbox onboarding — no payment required
class SandboxOnboarding {
  async createSandboxTenant(email: string): Promise<SandboxAccount> {
    const tenant = await this.db.insert('tenants', {
      email,
      environment: 'sandbox',
      createdAt: new Date(),
      sandboxQuota: {
        apiRequestsMinute: 0,
        totalAgents: 0,
        concurrentCalls: 0,
        storageBytes: 0,
      },
    });

    const apiKey = await this.apiKeyService.generateKey('sandbox');

    return {
      tenantId: tenant.id,
      apiKey: apiKey.rawKey,
      environment: 'sandbox',
      quota: DEFAULTS,
    };
  }
}

// Usage dashboard — display remaining quota
async function getSandboxUsageDashboard(tenantId: string): Promise<Record<string, unknown>> {
  const quota = await sandboxQuotaManager.getUsage(tenantId);

  return {
    environment: 'sandbox',
    usage: {
      apiRequestsMinute: {
        used: quota.apiRequestsMinute,
        limit: 300,
        remaining: 300 - quota.apiRequestsMinute,
      },
      agents: {
        used: quota.totalAgents,
        limit: 100,
        remaining: 100 - quota.totalAgents,
      },
      concurrentCalls: {
        used: quota.concurrentCalls,
        limit: 25,
        remaining: 25 - quota.concurrentCalls,
      },
      storage: {
        used: quota.storageBytes,
        limit: 1_073_741_824,
        remaining: 1_073_741_824 - quota.storageBytes,
        usedFormatted: formatBytes(quota.storageBytes),
      },
    },
    resetsAt: quota.lastResetAt,
  };
}
```

## Integration Points

- **Developer Portal**: Usage dashboard shows sandbox quota consumption
- **API Keys**: Key prefix determines environment and billing behavior
- **Onboarding Flow**: Sandbox signup skips payment collection

## Production Considerations

- **Abuse Prevention**: Rate limits and quotas prevent sandbox abuse
- **Storage Limits**: 7-day data retention with automatic cleanup
- **Feature Gating**: New features available in sandbox immediately for beta testing
- **Promotion Path**: Seamless upgrade from sandbox to production with config export

## Open-Source Tools

- **Stripe**: Payment processing for production billing (disabled in sandbox)
