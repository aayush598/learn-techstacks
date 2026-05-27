# Section 08: Multi-Tenant Isolation

## Overview

Multi-tenant notification architecture isolates tenant data, configurations, and delivery quotas. Each tenant has independent channel configurations, template sets, preference schemas, and delivery quotas. The notification bus filters events by tenant and enforces per-tenant rate limits and billing integration.

## Design Decisions

- **Database-Level Isolation**: Tenant ID on every notification record
- **Config Per Tenant**: Channel configs, templates, and preferences scoped to tenant
- **Quota Enforcement**: Delivery quotas tracked and enforced per tenant
- **Billing Integration**: Delivery counts feed into billing system

## Implementation Approach

```typescript
interface TenantNotificationConfig {
  tenantId: string;
  enabledChannels: string[];
  channelConfigs: Record<string, ChannelConfig>;
  quotas: NotificationQuotas;
  rateLimits: RateLimitConfig;
  billingPlan: string;
}

interface NotificationQuotas {
  monthlyLimit: number;
  currentMonthUsage: number;
  warningThreshold: number; // percentage
  hardLimit: boolean; // block when exceeded
}

class MultiTenantNotificationManager {
  async sendWithTenantIsolation(event: NotificationEvent): Promise<void> {
    const tenantConfig = await this.getTenantConfig(event.metadata.tenantId);
    if (!tenantConfig) throw new Error('Tenant not configured');

    // Check quota
    const quotaCheck = await this.checkQuota(tenantConfig);
    if (!quotaCheck.allowed) {
      await this.notifyQuotaExceeded(tenantConfig);
      throw new QuotaExceededError(quotaCheck);
    }

    // Filter enabled channels
    const enabledChannels = tenantConfig.enabledChannels;
    const channelSubscribers = this.getEnabledSubscribers(event.topic, enabledChannels);

    await Promise.all(channelSubscribers.map(async subscriber => {
      const channelConfig = tenantConfig.channelConfigs[subscriber.channel];
      if (!channelConfig?.enabled) return;

      // Per-channel rate limiting
      if (await this.isRateLimited(tenantConfig.rateLimits, subscriber.channel)) {
        await this.queueForLater(event, subscriber);
        return;
      }

      await this.deliver(event, subscriber);
      await this.incrementUsage(tenantConfig.tenantId, 1);
    }));
  }

  private async checkQuota(config: TenantNotificationConfig): Promise<QuotaResult> {
    return {
      allowed: config.quotas.hardLimit
        ? config.quotas.currentMonthUsage < config.quotas.monthlyLimit
        : true,
      usagePercent: (config.quotas.currentMonthUsage / config.quotas.monthlyLimit) * 100,
    };
  }

  async initializeTenant(tenantId: string, plan: string): Promise<void> {
    const config = this.getDefaultConfig(plan);
    await this.storage.save(`tenant_config:${tenantId}`, {
      ...config,
      tenantId,
      billingPlan: plan,
      quotas: { ...config.quotas, currentMonthUsage: 0 },
    });
  }
}
```

## Integration Points

- **Billing System**: Usage tracked and synced to billing
- **Admin UI**: Tenant configuration management
- **Onboarding Flow**: Tenant setup during onboarding

## Production Considerations

- **Quota Enforcement**: Hard limits prevent surprise bills
- **Usage Monitoring**: Alert when tenants approach limits
- **Self-Service**: Allow tenants to upgrade plans via billing integration
