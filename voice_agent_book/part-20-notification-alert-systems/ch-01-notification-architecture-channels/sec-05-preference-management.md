# Section 05: Preference Management

## Overview

The preference management system lets users control how and when they receive notifications. Preferences include channel opt-in/out, notification category subscriptions, frequency controls (immediate, digest, off), quiet hours, and per-channel settings. A preference center UI exposes these controls, and the notification bus checks preferences before delivering.

## Architecture

```
┌─────────────────────────────────────────┐
│         Preference Management            │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   User Preference Profile        │   │
│  │                                  │   │
│  │  • Channel Opt-In/Out            │   │
│  │  • Category Subscriptions        │   │
│  │  • Frequency Controls            │   │
│  │  • Quiet Hours                   │   │
│  │  • Global Pause                  │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────┐  ┌─────────────────┐  │
│  │ Preference   │  │ Enforcement     │  │
│  │ API          │  │ Engine          │  │
│  │             │  │                │  │
│  │ CRUD/GET    │  │ Filter events  │  │
│  │ Batch update│  │ Route channels │  │
│  │ Validation  │  │ Apply rules    │  │
│  └─────────────┘  └─────────────────┘  │
└─────────────────────────────────────────┘
```

## Implementation Approach

```typescript
interface UserPreferences {
  userId: string;
  tenantId: string;
  globalPaused: boolean;
  quietHours: QuietHours;
  channels: ChannelPreferences;
  categories: CategoryPreferences;
}

interface ChannelPreferences {
  email: { enabled: boolean; frequency: 'immediate' | 'digest' | 'off' };
  sms: { enabled: boolean; dailyLimit: number };
  push: { enabled: boolean; quietHoursEnabled: boolean };
  slack: { enabled: boolean; channelIds: string[] };
}

interface CategoryPreferences {
  billing: { subscribed: boolean; channel: string };
  security: { subscribed: boolean; channel: string };
  product: { subscribed: boolean; channel: string };
  system: { subscribed: boolean; channel: string };
}

class PreferenceEnforcementEngine {
  async shouldDeliver(event: NotificationEvent, userId: string): Promise<DeliveryDecision> {
    const prefs = await this.preferenceService.getPreferences(userId);
    if (prefs.globalPaused) return { allow: false, reason: 'global_pause' };

    const category = event.metadata.category;
    const categoryPref = prefs.categories[category];
    if (!categoryPref?.subscribed) return { allow: false, reason: 'category_unsubscribed' };

    const channelPref = prefs.channels[categoryPref.channel];
    if (!channelPref?.enabled) return { allow: false, reason: 'channel_disabled' };

    if (this.isInQuietHours(prefs.quietHours)) return { allow: false, reason: 'quiet_hours' };

    return { allow: true, channel: categoryPref.channel };
  }

  private isInQuietHours(quietHours: QuietHours): boolean {
    const now = new Date();
    const currentMinutes = now.getHours() * 60 + now.getMinutes();
    const startMinutes = quietHours.start.hours * 60 + quietHours.start.minutes;
    const endMinutes = quietHours.end.hours * 60 + quietHours.end.minutes;
    return currentMinutes >= startMinutes && currentMinutes <= endMinutes;
  }
}
```

## Integration Points

- **Preference Center UI**: User-facing settings page
- **Preference API**: REST endpoints for preference CRUD
- **Enforcement Hook**: Called before notification delivery

## Production Considerations

- **Default Preferences**: Sensible defaults for new users
- **Preference Caching**: Cache preferences aggressively
- **Audit Trail**: Log preference changes for compliance
