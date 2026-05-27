# Section 05: Trial Expiry Notifications

## Countdown Emails

Trial expiry notifications are sent at strategic intervals to encourage conversion. The email sequence starts 7 days before expiry and increases in urgency as the deadline approaches.

```typescript
interface TrialNotificationSchedule {
  daysBeforeExpiry: number;
  channel: 'email' | 'in_app' | 'push' | 'sms';
  template: string;
  urgency: 'low' | 'medium' | 'high' | 'critical';
  action: string;
}

const TRIAL_EXPIRY_SCHEDULE: TrialNotificationSchedule[] = [
  {
    daysBeforeExpiry: 7,
    channel: 'email',
    template: 'trial_7_days',
    urgency: 'low',
    action: 'Explore upgrade benefits',
  },
  {
    daysBeforeExpiry: 3,
    channel: 'email',
    template: 'trial_3_days',
    urgency: 'medium',
    action: 'Add payment method',
  },
  {
    daysBeforeExpiry: 1,
    channel: 'email',
    template: 'trial_1_day',
    urgency: 'high',
    action: 'Confirm upgrade',
  },
  {
    daysBeforeExpiry: 0,
    channel: 'email',
    template: 'trial_expired',
    urgency: 'critical',
    action: 'Reactivate account',
  },
];

class TrialNotificationService {
  async sendTrialExpiryReminders(): Promise<void> {
    const now = new Date();

    for (const schedule of TRIAL_EXPIRY_SCHEDULE) {
      const targetDate = new Date(
        now.getTime() + schedule.daysBeforeExpiry * 86400000
      );

      const expiringTrials = await this.db.trials.find({
        status: 'active',
        endsAt: {
          $gte: targetDate.toISOString(),
          $lt: new Date(targetDate.getTime() + 86400000).toISOString(),
        },
        lastNotificationDay: { $ne: schedule.daysBeforeExpiry },
      }).toArray();

      for (const trial of expiringTrials) {
        await this.sendNotification(trial, schedule);
      }
    }
  }

  private async sendNotification(
    trial: TrialSession,
    schedule: TrialNotificationSchedule
  ): Promise<void> {
    const tenant = await this.tenantService.getTenant(trial.tenantId);
    const plan = await this.planCatalog.getPlan(trial.planId);

    const daysRemaining = Math.ceil(
      (Date.parse(trial.endsAt) - Date.now()) / 86400000
    );

    const templateData = {
      tenantName: tenant.companyName,
      planName: plan.name,
      daysRemaining: Math.max(0, daysRemaining),
      expiryDate: formatDate(trial.endsAt),
      upgradeUrl: `${APP_URL}/upgrade?trial=${trial.id}`,
      features: plan.features.filter(f => !f.enabled).slice(0, 3),
      usageSummary: await this.getUsageSummary(trial.tenantId, trial.planId),
    };

    // Send via appropriate channel
    switch (schedule.channel) {
      case 'email':
        await this.emailService.send({
          to: tenant.email,
          subject: this.getEmailSubject(schedule, templateData),
          template: schedule.template,
          data: templateData,
        });
        break;
      case 'in_app':
        await this.inAppNotificationService.show({
          tenantId: trial.tenantId,
          message: this.getInAppMessage(schedule, templateData),
          urgency: schedule.urgency,
          action: { label: schedule.action, url: templateData.upgradeUrl },
        });
        break;
      case 'sms':
        if (tenant.phone) {
          await this.smsService.send({
            to: tenant.phone,
            message: `Your ${plan.name} trial ends in ${daysRemaining} days. Upgrade to keep your agents running: ${templateData.upgradeUrl}`,
          });
        }
        break;
    }

    // Track notification
    await this.db.trialNotifications.create({
      trialId: trial.id,
      daysBeforeExpiry: schedule.daysBeforeExpiry,
      channel: schedule.channel,
      sentAt: new Date().toISOString(),
    });

    // Update last notification
    await this.db.trials.updateOne(
      { id: trial.id },
      { $set: { lastNotificationDay: schedule.daysBeforeExpiry } }
    );
  }

  private getEmailSubject(
    schedule: TrialNotificationSchedule,
    data: any
  ): string {
    const subjects: Record<string, string> = {
      trial_7_days: `${data.daysRemaining} days left in your ${data.planName} trial`,
      trial_3_days: `Your trial ends in ${data.daysRemaining} days — don't lose your setup`,
      trial_1_day: `Final day! Your trial ends tomorrow`,
      trial_expired: 'Your trial has ended — reactivate now',
    };
    return subjects[schedule.template] || 'Trial update';
  }
}
```

## In-App Banners

In-app banners provide persistent but non-intrusive reminders of trial status. They appear at the top of the dashboard and can be dismissed.

```typescript
interface TrialBanner {
  id: string;
  tenantId: string;
  message: string;
  urgency: 'info' | 'warning' | 'critical';
  action?: {
    label: string;
    url: string;
  };
  dismissible: boolean;
  expiresAt?: string;
}

class TrialBannerService {
  async getActiveBanners(tenantId: string): Promise<TrialBanner[]> {
    const trial = await this.db.trials.findOne({
      tenantId,
      status: 'active',
    });

    if (!trial) return [];

    const daysRemaining = Math.ceil(
      (Date.parse(trial.endsAt) - Date.now()) / 86400000
    );

    const banners: TrialBanner[] = [];

    if (daysRemaining <= 3 && daysRemaining > 0) {
      banners.push({
        id: 'trial_expiring',
        tenantId,
        message: `Your trial ends in ${daysRemaining} days. Upgrade to keep your account active.`,
        urgency: daysRemaining <= 1 ? 'critical' : 'warning',
        action: { label: 'Upgrade Now', url: `${APP_URL}/upgrade` },
        dismissible: daysRemaining > 1,
      });
    }

    if (daysRemaining <= 0) {
      banners.push({
        id: 'trial_expired',
        tenantId,
        message: 'Your trial has ended. Upgrade to reactivate your voice agents.',
        urgency: 'critical',
        action: { label: 'Reactivate', url: `${APP_URL}/upgrade` },
        dismissible: false,
      });
    }

    return banners;
  }
}
```

## Expiry Day Handling

When the trial expires, the system gracefully restricts access rather than immediately blocking the user. Data is preserved for a grace period, and the user can upgrade to restore full access.

```typescript
async function handleTrialExpiry(trialId: string): Promise<void> {
  const trial = await db.trials.findOne({ id: trialId });

  // Update trial status
  await db.trials.updateOne(
    { id: trialId },
    { $set: { status: 'expired', expiredAt: new Date().toISOString() } }
  );

  // Restrict feature access (but don't delete data)
  await featureGateService.applyExpiryRestrictions(trial.tenantId);

  // Send expiry notification
  await notificationService.sendTrialExpired(trial.tenantId, trial.planId);
}
```

## Post-Expiry Data Retention

After trial expiry, customer data is preserved for 30 days (retention period). During this period, the customer can upgrade and regain full access. After 30 days, data is archived and eventually deleted.

```typescript
const DATA_RETENTION_DAYS = 30;

async function scheduleDataCleanup(trial: TrialSession): Promise<void> {
  const cleanupDate = new Date(
    Date.parse(trial.endsAt) + DATA_RETENTION_DAYS * 86400000
  );

  await bullQueue.add('trialDataCleanup', {
    trialId: trial.id,
    tenantId: trial.tenantId,
  }, {
    delay: DATA_RETENTION_DAYS * 86400000,
  });
}

async function postExpiryDataRetention(tenantId: string): Promise<void> {
  // Archive data to cold storage
  await archiveService.archiveTenantData(tenantId);

  // Send final notification
  await notificationService.sendDataRetentionExpiring(tenantId);

  // Schedule deletion
  await bullQueue.add('deleteArchivedData', {
    tenantId,
  }, {
    delay: 7 * 86400000, // 7 days after archival
  });
}
```

## Open-Source Tools

- **BullMQ** (MIT) — Schedule trial expiry notifications
- **Nodemailer** (MIT) — Email delivery for reminders
- **PostgreSQL** — Trial notification tracking
- **Redis** — Banner state caching

## Integration Points

Trial expiry notifications connect to the email service, the in-app notification system, the feature gate service (for access restriction), and the data archival service.

## Production Considerations

- A/B test reminder timing and messaging
- Monitor email open rates and click-through rates
- Track conversion from reminder emails
- Handle timezone differences for global customers
- Respect user communication preferences

## Open-Source First Philosophy

BullMQ schedules all trial notifications reliably without proprietary marketing automation. Nodemailer delivers emails through any SMTP provider. PostgreSQL tracks notification history for analytics. This open-source stack provides trial communication capabilities equivalent to expensive marketing automation platforms.
