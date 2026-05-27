# Section 04: Priority Levels & Urgency

## Overview

Notification priority levels determine delivery urgency and channel selection. High-priority notifications use interruptive channels (SMS, push), while low-priority ones use non-interruptive channels (in-app, email digest). The system maps notification types to priority tiers and selects appropriate channels.

## Implementation Approach

```typescript
type PriorityTier = 'critical' | 'high' | 'normal' | 'low';

interface PriorityConfig {
  tier: PriorityTier;
  channels: string[];
  deliveryTimeout: number; // seconds
  interruptionLevel: 'immediate' | 'alert' | 'passive' | 'silent';
  persistent: boolean;
  sound: boolean;
  vibration: boolean;
}

class PriorityRouter {
  private priorityConfigs: Record<PriorityTier, PriorityConfig> = {
    critical: {
      tier: 'critical',
      channels: ['sms', 'phone', 'push', 'in_app'],
      deliveryTimeout: 60,
      interruptionLevel: 'immediate',
      persistent: true,
      sound: true,
      vibration: true,
    },
    high: {
      tier: 'high',
      channels: ['push', 'in_app', 'email'],
      deliveryTimeout: 300,
      interruptionLevel: 'alert',
      persistent: true,
      sound: true,
      vibration: true,
    },
    normal: {
      tier: 'normal',
      channels: ['in_app', 'email'],
      deliveryTimeout: 3600,
      interruptionLevel: 'passive',
      persistent: false,
      sound: false,
      vibration: false,
    },
    low: {
      tier: 'low',
      channels: ['in_app'],
      deliveryTimeout: 86400,
      interruptionLevel: 'silent',
      persistent: false,
      sound: false,
      vibration: false,
    },
  };

  async route(notification: InAppNotification, userPrefs: UserPreferences): Promise<DeliveryPlan> {
    const config = this.priorityConfigs[notification.priority];
    const availableChannels = config.channels.filter(ch => this.isChannelAvailable(ch, userPrefs));
    const channelOrder = this.prioritizeChannels(availableChannels, userPrefs);

    return {
      notificationId: notification.id,
      priority: notification.priority,
      channels: channelOrder,
      interruptionLevel: config.interruptionLevel,
      deliveryStrategy: this.getDeliveryStrategy(notification.priority),
      timeout: config.deliveryTimeout,
    };
  }

  private prioritizeChannels(channels: string[], prefs: UserPreferences): ChannelTarget[] {
    const order: string[] = [];
    if (channels.includes('sms')) order.push('sms');
    if (channels.includes('push') && prefs.push.enabled) order.push('push');
    if (channels.includes('phone')) order.push('phone');
    if (channels.includes('in_app')) order.push('in_app');
    if (channels.includes('email') && prefs.email.frequency !== 'off') order.push('email');
    return order.map(ch => ({ channel: ch }));
  }

  private isChannelAvailable(channel: string, prefs: UserPreferences): boolean {
    switch (channel) {
      case 'sms': return prefs.sms.enabled;
      case 'push': return prefs.push.enabled;
      case 'phone': return prefs.phone?.enabled || false;
      case 'in_app': return true;
      case 'email': return prefs.email.enabled && prefs.email.frequency !== 'off';
      default: return false;
    }
  }

  private getDeliveryStrategy(priority: PriorityTier): DeliveryStrategy {
    switch (priority) {
      case 'critical':
        return { type: 'escalating', escalateAfter: 60, escalateChannel: 'phone' };
      case 'high':
        return { type: 'all_at_once' };
      case 'normal':
        return { type: 'sequential', order: ['push', 'email'] };
      case 'low':
        return { type: 'digest' };
    }
  }

  async escalateIfNotDelivered(notificationId: string, plan: DeliveryPlan): Promise<void> {
    if (plan.deliveryStrategy.type !== 'escalating') return;

    const deliveryStatus = await this.deliveryTracker.getStatus(notificationId);
    const elapsed = Date.now() - new Date(deliveryStatus.sentAt).getTime();

    if (elapsed > plan.deliveryStrategy.escalateAfter * 1000 && !deliveryStatus.acknowledged) {
      await this.notificationService.send(notificationId, {
        channels: [plan.deliveryStrategy.escalateChannel],
      });
    }
  }
}
```

## Integration Points

- **User Preferences**: Channel availability based on user settings
- **Delivery Tracker**: Track delivery and acknowledgment status
- **Escalation Engine**: Escalate if critical notifications unacknowledged

## Production Considerations

- **Notification Fatigue**: Respect quiet hours for non-critical notifications
- **Channel Velocity**: Limit high-priority notification frequency
- **User Control**: Allow users to customize priority mappings
