# Section 04: Channel Subscription Management

## Overview

Channel subscription management maps notification types to specific Slack channels or Teams channels. Users can subscribe channels to receive specific alert categories, and filtering rules determine which notifications appear in each channel. The system supports one-to-many and many-to-one channel mappings.

## Implementation Approach

```typescript
interface ChannelSubscription {
  id: string;
  workspaceId: string;
  channelId: string;
  channelName: string;
  tenantId: string;
  filters: SubscriptionFilter[];
  enabled: boolean;
  createdAt: string;
}

interface SubscriptionFilter {
  type: 'severity' | 'source' | 'ruleId' | 'tag' | 'custom';
  values: string[];
  operator: 'include' | 'exclude';
}

class ChannelSubscriptionManager {
  async subscribe(subscription: CreateSubscriptionRequest): Promise<ChannelSubscription> {
    const existing = await this.findSubscription(subscription.workspaceId, subscription.channelId);
    if (existing) throw new Error('Channel already subscribed');

    const sub: ChannelSubscription = {
      id: generateId(),
      ...subscription,
      enabled: true,
      createdAt: new Date().toISOString(),
    };

    await this.storage.save(sub);
    await this.sendWelcomeMessage(sub);
    return sub;
  }

  async unsubscribe(id: string): Promise<void> {
    await this.storage.delete(id);
  }

  async updateFilters(id: string, filters: SubscriptionFilter[]): Promise<ChannelSubscription> {
    const sub = await this.storage.get(id);
    sub.filters = filters;
    await this.storage.update(sub);
    return sub;
  }

  async getSubscribedChannels(tenantId: string): Promise<ChannelSubscription[]> {
    return this.storage.query({ tenantId, enabled: true });
  }

  async shouldDeliverToChannel(subscription: ChannelSubscription, alert: Alert): Promise<boolean> {
    if (!subscription.enabled) return false;

    for (const filter of subscription.filters) {
      const matches = this.evaluateFilter(filter, alert);
      if (filter.operator === 'include' && !matches) return false;
      if (filter.operator === 'exclude' && matches) return false;
    }

    return true;
  }

  private evaluateFilter(filter: SubscriptionFilter, alert: Alert): boolean {
    switch (filter.type) {
      case 'severity':
        return filter.values.includes(alert.severity);
      case 'source':
        return filter.values.includes(alert.metadata.source);
      case 'ruleId':
        return filter.values.includes(alert.ruleId);
      case 'tag': {
        const alertTags = alert.metadata.tags || [];
        return filter.values.some(v => alertTags.includes(v));
      }
      default:
        return true;
    }
  }

  private async sendWelcomeMessage(subscription: ChannelSubscription): Promise<void> {
    const message = {
      text: `🔔 *Notification Channel Active*\nThis channel will receive notifications for: ${subscription.filters.map(f => `${f.type}: ${f.values.join(', ')}`).join(' | ')}`,
    };
    await this.slackService.sendMessage(subscription.workspaceId, subscription.channelId, message);
  }

  async validateChannel(workspaceId: string, channelId: string): Promise<boolean> {
    try {
      await this.slackService.getChannelInfo(workspaceId, channelId);
      return true;
    } catch {
      return false;
    }
  }
}
```

## Integration Points

- **Slack/Teams API**: Channel validation and message sending
- **Alert Engine**: Evaluates subscriptions for each alert
- **Subscription UI**: Manage subscriptions from settings page

## Production Considerations

- **Channel Validation**: Verify channel exists before subscribing
- **Duplicate Prevention**: Prevent duplicate channel subscriptions
- **Bulk Operations**: Support batch subscription updates
