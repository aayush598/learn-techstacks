# Section 08: Usage Notification Preferences

## Per-User Notification Settings

Each user on a tenant account can configure their notification preferences independently. Notifications include usage alerts, overage warnings, billing reminders, and promotional offers.

```typescript
interface NotificationPreference {
  userId: string;
  tenantId: string;
  channels: {
    email: boolean;
    inApp: boolean;
    sms: boolean;
    webhook: boolean;
  };
  alertCategories: {
    usageAlerts: AlertCategoryConfig;
    billingAlerts: AlertCategoryConfig;
    overageAlerts: AlertCategoryConfig;
    promotionalAlerts: AlertCategoryConfig;
  };
  quietHours?: {
    enabled: boolean;
    start: string;       // HH:mm format
    end: string;         // HH:mm format
    timezone: string;
  };
  digest: {
    enabled: boolean;
    frequency: 'never' | 'daily' | 'weekly' | 'monthly';
    lastSent?: string;
  };
}

interface AlertCategoryConfig {
  enabled: boolean;
  channels: AlertChannel[];
  minSeverity: 'info' | 'warning' | 'critical';
  thresholds?: number[];      // Custom thresholds (percentages)
}

class NotificationPreferenceService {
  async getPreferences(
    userId: string,
    tenantId: string
  ): Promise<NotificationPreference> {
    let prefs = await this.db.notificationPreferences.findOne({
      userId,
      tenantId,
    });

    if (!prefs) {
      // Create default preferences
      prefs = this.getDefaultPreferences(userId, tenantId);
      await this.db.notificationPreferences.create(prefs);
    }

    return prefs;
  }

  async updatePreferences(
    userId: string,
    tenantId: string,
    updates: Partial<NotificationPreference>
  ): Promise<NotificationPreference> {
    await this.db.notificationPreferences.updateOne(
      { userId, tenantId },
      { $set: { ...updates, updatedAt: new Date().toISOString() } }
    );

    return this.getPreferences(userId, tenantId);
  }

  async shouldNotify(
    userId: string,
    tenantId: string,
    alertType: string,
    severity: 'info' | 'warning' | 'critical'
  ): Promise<{ shouldSend: boolean; channels: AlertChannel[] }> {
    const prefs = await this.getPreferences(userId, tenantId);

    // Check if category is enabled
    const categoryKey = this.getCategoryKey(alertType);
    const category = prefs.alertCategories[categoryKey];

    if (!category || !category.enabled) {
      return { shouldSend: false, channels: [] };
    }

    // Check severity level
    const severityLevels = { info: 0, warning: 1, critical: 2 };
    const minLevel = severityLevels[category.minSeverity];
    const currentLevel = severityLevels[severity];

    if (currentLevel < minLevel) {
      return { shouldSend: false, channels: [] };
    }

    // Check quiet hours
    if (prefs.quietHours?.enabled) {
      const now = new Date();
      const quietStart = this.parseTime(prefs.quietHours.start);
      const quietEnd = this.parseTime(prefs.quietHours.end);

      if (this.isInQuietHours(now, quietStart, quietEnd)) {
        // Queue for digest instead
        await this.queueForDigest(userId, tenantId, alertType);
        return { shouldSend: false, channels: [] };
      }
    }

    // Determine channels
    const channels = category.channels.filter(ch => {
      switch (ch) {
        case AlertChannel.EMAIL: return prefs.channels.email;
        case AlertChannel.IN_APP: return prefs.channels.inApp;
        case AlertChannel.SMS: return prefs.channels.sms;
        case AlertChannel.WEBHOOK: return prefs.channels.webhook;
        default: return false;
      }
    });

    return { shouldSend: channels.length > 0, channels };
  }

  private getDefaultPreferences(
    userId: string,
    tenantId: string
  ): NotificationPreference {
    return {
      userId,
      tenantId,
      channels: { email: true, inApp: true, sms: false, webhook: false },
      alertCategories: {
        usageAlerts: { enabled: true, channels: [AlertChannel.EMAIL, AlertChannel.IN_APP], minSeverity: 'warning', thresholds: [80, 90, 100] },
        billingAlerts: { enabled: true, channels: [AlertChannel.EMAIL], minSeverity: 'info' },
        overageAlerts: { enabled: true, channels: [AlertChannel.EMAIL, AlertChannel.IN_APP, AlertChannel.SMS], minSeverity: 'warning' },
        promotionalAlerts: { enabled: false, channels: [AlertChannel.EMAIL], minSeverity: 'info' },
      },
      quietHours: { enabled: false, start: '22:00', end: '08:00', timezone: 'UTC' },
      digest: { enabled: false, frequency: 'weekly' },
    };
  }
}
```

## Channel Preferences

Channel preferences determine which notification channels each alert category uses. Channels include email, in-app notifications, SMS, and webhooks.

```typescript
interface ChannelPreference {
  email: {
    enabled: boolean;
    emailAddress: string;       // Override email (default: account email)
    digestOnly: boolean;        // Only send in digest, not real-time
  };
  inApp: {
    enabled: boolean;
    showBanners: boolean;
    showBadge: boolean;
  };
  sms: {
    enabled: boolean;
    phoneNumber: string;
    criticalOnly: boolean;      // Only critical alerts via SMS
  };
  webhook: {
    enabled: boolean;
    endpointUrl: string;
    secret: string;             // HMAC secret for webhook verification
    retryOnFailure: boolean;
  };
}
```

## Digest Frequency

For non-critical alerts, notifications can be batched into digests. Digest frequency is configurable (never, daily, weekly, monthly).

```typescript
interface NotificationDigest {
  id: string;
  userId: string;
  tenantId: string;
  period: 'daily' | 'weekly' | 'monthly';
  periodStart: string;
  periodEnd: string;
  items: DigestItem[];
  sentAt?: string;
}

interface DigestItem {
  type: string;
  severity: string;
  title: string;
  message: string;
  timestamp: string;
  actionUrl?: string;
}

class DigestService {
  async generateDigest(
    userId: string,
    tenantId: string,
    frequency: 'daily' | 'weekly' | 'monthly'
  ): Promise<NotificationDigest> {
    const periodStart = this.getPeriodStart(frequency);

    const queuedItems = await this.db.notificationQueue.find({
      userId,
      tenantId,
      queuedForDigest: true,
      createdAt: { $gte: periodStart },
    }).toArray();

    const digest: NotificationDigest = {
      id: `digest_${nanoid(16)}`,
      userId,
      tenantId,
      period: frequency,
      periodStart: periodStart.toISOString(),
      periodEnd: new Date().toISOString(),
      items: queuedItems.map(q => ({
        type: q.type,
        severity: q.severity,
        title: q.title,
        message: q.message,
        timestamp: q.createdAt,
        actionUrl: q.actionUrl,
      })),
    };

    return digest;
  }

  async sendDigest(digest: NotificationDigest): Promise<void> {
    const user = await this.userService.getUser(digest.userId);

    if (digest.items.length === 0) return;

    await this.emailService.send({
      to: user.email,
      subject: `Your ${digest.period} digest — ${digest.items.length} notifications`,
      template: 'notification_digest',
      data: {
        userName: user.name,
        period: digest.period,
        itemCount: digest.items.length,
        items: digest.items,
        settingsUrl: `${APP_URL}/settings/notifications`,
      },
    });

    // Clear queued items
    await this.db.notificationQueue.deleteMany({
      userId: digest.userId,
      tenantId: digest.tenantId,
      queuedForDigest: true,
    });

    // Record digest sent
    await this.db.notificationDigests.create({
      ...digest,
      sentAt: new Date().toISOString(),
    });
  }
}
```

## Open-Source Tools

- **PostgreSQL** — Notification preference storage
- **Redis** — Cache preferences for fast access
- **BullMQ** (MIT) — Schedule digest generation
- **Nodemailer** (MIT) — Email delivery for digests

## Integration Points

Notification preferences connect to the usage alert system (Section 3), the billing alert system, the in-app notification service, and the user management system.

## Production Considerations

- Provide a unified notification settings UI
- Default notifications to sensible values
- Allow admin to set tenant-wide defaults
- Respect customer opt-out for marketing communications
- Monitor notification delivery success by channel

## Open-Source First Philosophy

PostgreSQL stores notification preferences, Redis caches them for fast checks, and BullMQ manages digest scheduling. Nodemailer delivers emails through any SMTP provider. This open-source stack provides enterprise-grade notification preference management without proprietary marketing automation platforms.
