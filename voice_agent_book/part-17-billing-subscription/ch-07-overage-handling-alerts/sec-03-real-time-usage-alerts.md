# Section 03: Real-Time Usage Alerts

## Usage Threshold Alerts

Usage alerts notify customers when they approach or exceed their plan allowances. Alerts are configurable at multiple thresholds and deliverable through multiple channels.

```typescript
interface UsageAlertThreshold {
  meter: string;
  thresholds: AlertThreshold[];
}

interface AlertThreshold {
  percentOfAllowance: number;    // 50, 75, 80, 90, 100, 120, 150
  direction: 'above' | 'below';
  channels: AlertChannel[];
  message: string;
  action?: AlertAction;
}

enum AlertChannel {
  EMAIL = 'email',
  IN_APP = 'in_app',
  SMS = 'sms',
  WEBHOOK = 'webhook',
}

interface AlertAction {
  type: 'none' | 'upgrade_prompt' | 'auto_topup' | 'block';
  url?: string;
}

const DEFAULT_ALERT_THRESHOLDS: UsageAlertThreshold[] = [
  {
    meter: 'monthly_minutes',
    thresholds: [
      { percentOfAllowance: 50, direction: 'above', channels: [AlertChannel.IN_APP], message: 'You\'ve used 50% of your monthly minutes' },
      { percentOfAllowance: 80, direction: 'above', channels: [AlertChannel.EMAIL, AlertChannel.IN_APP], message: 'You\'ve used 80% of your monthly minutes' },
      { percentOfAllowance: 90, direction: 'above', channels: [AlertChannel.EMAIL, AlertChannel.IN_APP], message: 'You\'ve used 90% of your monthly minutes — overage rates will apply soon' },
      { percentOfAllowance: 100, direction: 'above', channels: [AlertChannel.EMAIL, AlertChannel.IN_APP, AlertChannel.SMS], message: 'You\'ve exhausted your monthly allowance. Overage rates now apply.', action: { type: 'auto_topup' } },
      { percentOfAllowance: 120, direction: 'above', channels: [AlertChannel.EMAIL], message: 'Your overage is $X. Consider upgrading to save.', action: { type: 'upgrade_prompt', url: '/upgrade' } },
      { percentOfAllowance: 150, direction: 'above', channels: [AlertChannel.EMAIL, AlertChannel.SMS], message: 'High usage alert: You\'ve used 150% of your allowance.' },
    ],
  },
];

class UsageAlertService {
  async evaluateThresholds(
    tenantId: string,
    meter: string,
    currentUsage: number,
    allowance: number
  ): Promise<void> {
    const config = await this.getAlertConfig(tenantId);
    const thresholds = config.find(t => t.meter === meter)?.thresholds
      || DEFAULT_ALERT_THRESHOLDS.find(t => t.meter === meter)?.thresholds;

    if (!thresholds) return;

    const usagePercent = allowance > 0 ? (currentUsage / allowance) * 100 : 0;

    for (const threshold of thresholds) {
      // Check if we've crossed this threshold
      const crossed = usagePercent >= threshold.percentOfAllowance;
      if (!crossed) continue;

      // Check if already notified at this threshold
      const alreadyNotified = await this.wasNotified(tenantId, meter, threshold.percentOfAllowance);
      if (alreadyNotified) continue;

      // Send notification
      await this.sendAlert(tenantId, meter, threshold, currentUsage, allowance);

      // Perform action
      if (threshold.action) {
        await this.executeAction(tenantId, threshold.action);
      }

      // Mark as notified
      await this.markNotified(tenantId, meter, threshold.percentOfAllowance);
    }
  }

  private async sendAlert(
    tenantId: string,
    meter: string,
    threshold: AlertThreshold,
    currentUsage: number,
    allowance: number
  ): Promise<void> {
    const tenant = await this.tenantService.getTenant(tenantId);
    const overage = Math.max(0, currentUsage - allowance);
    const message = threshold.message
      .replace('$X', `$${(overage * 0.025).toFixed(2)}`);

    for (const channel of threshold.channels) {
      switch (channel) {
        case AlertChannel.EMAIL:
          await this.emailService.send({
            to: tenant.email,
            subject: `Usage Alert: ${meter}`,
            text: message,
            html: `<p>${message}</p><p><a href="${APP_URL}/billing/usage">View Usage</a></p>`,
          });
          break;
        case AlertChannel.IN_APP:
          await this.inAppNotificationService.show({
            tenantId,
            message,
            type: 'warning',
            action: threshold.action
              ? { label: 'View', url: threshold.action.url || '/billing/usage' }
              : undefined,
          });
          break;
        case AlertChannel.SMS:
          if (tenant.phone) {
            await this.smsService.send({
              to: tenant.phone,
              message: `[Voice Agent] ${message}`,
            });
          }
          break;
        case AlertChannel.WEBHOOK:
          await this.webhookService.send(tenantId, {
            type: 'usage.alert',
            data: { meter, currentUsage, allowance, threshold: threshold.percentOfAllowance },
          });
          break;
      }
    }
  }
}
```

## Progress Notifications

Progress notifications show real-time usage as a percentage of allowance in the dashboard and via periodic check-ins.

```
Usage Progress Display (Dashboard):
┌──────────────────────────────────────────────────────────────────┐
│ Monthly Minutes Usage                                            │
│                                                                  │
│ [████████████████████████████░░░░░░░░░░░░░░░] 8,450 / 10,000   │
│                                                                  │
│ Usage: 84.5% of Growth Plan allowance                            │
│ Remaining: 1,550 minutes                                         │
│ Projected end-of-period: 11,200 minutes (12% overage)            │
└──────────────────────────────────────────────────────────────────┘
```

## In-App Banners

In-app banners provide persistent but non-intrusive usage warnings. They appear at the top of relevant pages and can be dismissed after viewing.

```typescript
function getUsageWarningBanner(
  usagePercent: number,
  meter: string
): { message: string; severity: 'info' | 'warning' | 'danger' } | null {
  if (usagePercent < 80) return null;

  if (usagePercent >= 100) {
    return {
      message: `You've used all your ${meter} for this period. Overage charges apply.`,
      severity: 'danger',
    };
  }

  if (usagePercent >= 90) {
    return {
      message: `You've used ${Math.round(usagePercent)}% of your ${meter}. Upgrade to avoid overage.`,
      severity: 'warning',
    };
  }

  return {
    message: `You've used ${Math.round(usagePercent)}% of your ${meter}.`,
    severity: 'info',
  };
}
```

## Email/SMS Alerts

Email and SMS alerts are sent at critical thresholds. The message content is personalized with exact usage numbers and cost estimates.

```typescript
function buildAlertEmailContent(
  tenant: Tenant,
  meter: string,
  usage: number,
  allowance: number,
  overageCost: number
): EmailContent {
  const percentUsed = Math.round((usage / allowance) * 100);

  return {
    subject: `⚠️ Usage Alert: ${percentUsed}% of ${meter} used`,
    body: `
Hi ${tenant.name},

You've used ${usage.toLocaleString()} of your ${allowance.toLocaleString()} ${meter} (${percentUsed}%).

${usage >= allowance
  ? `You've exceeded your allowance by ${(usage - allowance).toLocaleString()} ${meter}. Estimated overage cost: $${overageCost.toFixed(2)}.`
  : `You have ${(allowance - usage).toLocaleString()} ${meter} remaining this period.`}

View your detailed usage: ${APP_URL}/billing/usage
Upgrade your plan: ${APP_URL}/upgrade

— Voice Agent Platform
    `,
  };
}
```

## Open-Source Tools

- **BullMQ** — Schedule periodic threshold evaluations
- **Redis** — Track notified thresholds per tenant
- **Nodemailer** (MIT) — Email alert delivery
- **Twilio** (Proprietary, pay-as-you-go) — SMS alert delivery
- **PostgreSQL** — Alert configuration and history

## Integration Points

Usage alerts connect to the usage metering pipeline (real-time counters), the notification preference service (Section 8), the overage calculation engine (Section 1), and the customer dashboard.

## Production Considerations

- Allow customers to configure custom thresholds
- Rate-limit alerts to prevent notification fatigue
- Respect customer notification preferences (opt-in/opt-out)
- Test alert delivery across all channels
- Monitor alert delivery success rates

## Open-Source First Philosophy

BullMQ schedules alert evaluations reliably. Redis tracks notification deduplication. PostgreSQL stores alert configurations. This open-source stack provides real-time usage alerting without proprietary monitoring platforms, with Twilio as the only paid service (for SMS delivery).
