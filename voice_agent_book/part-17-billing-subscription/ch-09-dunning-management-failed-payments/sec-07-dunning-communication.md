# Section 07: Dunning Communication

## Email Templates Per Stage

Each dunning stage has tailored email templates that escalate in urgency and actionability.

```
[Dunning Stage → Email Template]
    ├── Soft Reminder
    │   ├── Subject: "Payment update needed"
    │   ├── Tone: Helpful, low urgency
    │   └── CTA: Update payment method
    ├── Active Recovery
    │   ├── Subject: "Action required: payment failed"
    │   ├── Tone: Urgent, direct
    │   ├── CTA: Pay now or update card
    │   └── Includes: Payment link
    ├── Grace Period
    │   ├── Subject: "Service will be restricted soon"
    │   ├── Tone: Warning, serious
    │   ├── CTA: Resolve immediately
    │   └── Includes: Days remaining
    └── Suspension Notice
        ├── Subject: "Service has been suspended"
        ├── Tone: Informational, solution-oriented
        ├── CTA: Reactivate account
        └── Includes: Data retention period
```

```typescript
interface DunningEmailTemplate {
  id: string;
  stage: DunningStage;
  subject: string;
  previewText: string;
  bodyTemplate: string;          // Handlebars template
  ctaText: string;
  ctaUrl: string;                // Template with {{paymentLink}} placeholder
  variables: string[];
  urgency: 'low' | 'medium' | 'high' | 'critical';
}

const DUNNING_EMAIL_TEMPLATES: DunningEmailTemplate[] = [
  {
    id: 'soft_reminder_day1',
    stage: DunningStage.SOFT_REMINDER,
    subject: 'Quick reminder: update your payment method',
    previewText: 'We had trouble processing your latest payment',
    bodyTemplate: `Hi {{customerName}},

We noticed a recent payment attempt for your {{planName}} subscription was unsuccessful.

This is likely a temporary issue — most payment failures are resolved by updating your payment method.

Update your payment method here: {{paymentLink}}

If you have any questions, our support team is here to help.

Best,
The {{appName}} Team`,
    ctaText: 'Update Payment Method',
    ctaUrl: '{{paymentLink}}',
    variables: ['customerName', 'planName', 'paymentLink', 'appName'],
    urgency: 'low',
  },
  {
    id: 'active_recovery_day3',
    stage: DunningStage.ACTIVE_RECOVERY,
    subject: 'Action required: payment failed — service at risk',
    previewText: 'Your service may be restricted if payment is not updated',
    bodyTemplate: `Hi {{customerName}},

We've made multiple attempts to process your payment of {{amount}} for {{planName}}, but each attempt has failed.

To avoid service interruption, please update your payment method within {{daysRemaining}} days.

Click here to pay now: {{paymentLink}}

If you need assistance, contact our support team.

Best,
The {{appName}} Team`,
    ctaText: 'Resolve Payment Now',
    ctaUrl: '{{paymentLink}}',
    variables: ['customerName', 'planName', 'amount', 'daysRemaining', 'paymentLink', 'appName'],
    urgency: 'medium',
  },
  {
    id: 'grace_period_day7',
    stage: DunningStage.GRACE_PERIOD,
    subject: 'Final notice: your service will be restricted',
    previewText: 'Your account will be restricted in {{daysRemaining}} days',
    bodyTemplate: `Hi {{customerName}},

This is your final notice. Your {{planName}} subscription payment of {{amount}} remains unpaid.

On {{restrictionDate}}, your service will be restricted. You will lose access to:
- API access
- Voice agent deployments
- Team collaboration features
- New analytics data

Your data will be retained for {{dataRetentionDays}} days after restriction.

Prevent this by updating your payment method now: {{paymentLink}}

Need more time? Contact our support team to discuss options.

Best,
The {{appName}} Team`,
    ctaText: 'Update Payment — Keep Service Active',
    ctaUrl: '{{paymentLink}}',
    variables: ['customerName', 'planName', 'amount', 'daysRemaining', 'restrictionDate', 'dataRetentionDays', 'paymentLink', 'appName'],
    urgency: 'high',
  },
  {
    id: 'suspension_notice',
    stage: DunningStage.SUSPENSION,
    subject: 'Your service has been suspended',
    previewText: 'Your account is suspended due to non-payment',
    bodyTemplate: `Hi {{customerName}},

Your {{planName}} subscription has been suspended due to non-payment of {{amount}}.

What happens next:
- Your data will be retained for {{dataRetentionDays}} days
- After that period, your data will be permanently deleted
- You can export your data at any time: {{exportLink}}

To reactivate your account, simply update your payment method and your service will be restored immediately: {{reactivationLink}}

If you'd like to discuss payment options, please reply to this email.

Best,
The {{appName}} Team`,
    ctaText: 'Reactivate Your Account',
    ctaUrl: '{{reactivationLink}}',
    variables: ['customerName', 'planName', 'amount', 'dataRetentionDays', 'exportLink', 'reactivationLink', 'appName'],
    urgency: 'critical',
  },
];
```

## SMS Notifications

SMS notifications are used for high-urgency dunning stages where email may not be sufficient.

```typescript
interface SMSTemplate {
  id: string;
  stage: DunningStage;
  template: string;
  maxLength: number;             // SMS character limit
  includesLink: boolean;
  requiresOptIn: boolean;
}

const SMS_TEMPLATES: SMSTemplate[] = [
  {
    id: 'sms_active_recovery',
    stage: DunningStage.ACTIVE_RECOVERY,
    template: '{{appName}}: Payment for {{planName}} ({{currency}}{{amount}}) failed. Update payment to continue service: {{shortLink}}',
    maxLength: 160,
    includesLink: true,
    requiresOptIn: true,
  },
  {
    id: 'sms_grace_warning',
    stage: DunningStage.GRACE_PERIOD,
    template: '{{appName}}: Service will be restricted in {{daysRemaining}}d. Update payment now: {{shortLink}}',
    maxLength: 160,
    includesLink: true,
    requiresOptIn: true,
  },
  {
    id: 'sms_suspension',
    stage: DunningStage.SUSPENSION,
    template: '{{appName}}: Service suspended. Reactivate: {{shortLink}}',
    maxLength: 160,
    includesLink: true,
    requiresOptIn: true,
  },
];

class SMSDunningService {
  async sendSMS(
    customerId: string,
    stage: DunningStage,
    context: SMSTemplateContext
  ): Promise<void> {
    const consent = await this.checkSMSConsent(customerId);
    if (!consent) return; // Skip if no consent

    const template = SMS_TEMPLATES.find(t => t.stage === stage);
    if (!template) return;

    // Check rate limits (max 3 SMS per 7 days per customer)
    const recentCount = await this.getRecentSMSCount(customerId, 7);
    if (recentCount >= 3) return;

    const shortLink = await this.shortenUrl(context.paymentLink);
    const message = template.template
      .replace('{{appName}}', context.appName)
      .replace('{{planName}}', context.planName)
      .replace('{{currency}}', context.currency)
      .replace('{{amount}}', context.amount.toString())
      .replace('{{daysRemaining}}', context.daysRemaining?.toString() || '')
      .replace('{{shortLink}}', shortLink);

    await this.smsProvider.send(context.phoneNumber, message);
    await this.logSentSMS(customerId, template.id, message);
  }
}
```

## In-App Banners

In-app notifications provide real-time dunning status to logged-in users.

```typescript
interface InAppBanner {
  id: string;
  stage: DunningStage;
  title: string;
  message: string;
  variant: 'info' | 'warning' | 'error' | 'critical';
  dismissable: boolean;
  actions: InAppBannerAction[];
  showOnPages: string[];         // Route patterns
  autoHideAfterDays?: number;
}

const IN_APP_BANNERS: InAppBanner[] = [
  {
    id: 'banner_soft_reminder',
    stage: DunningStage.SOFT_REMINDER,
    title: 'Payment Update Needed',
    message: 'We had trouble processing your latest payment. Please update your payment method to continue uninterrupted.',
    variant: 'warning',
    dismissable: true,
    actions: [
      { label: 'Update Payment', url: '/billing/payment', primary: true },
      { label: 'Learn More', url: '/help/billing', primary: false },
    ],
    showOnPages: ['/', '/dashboard', '/settings/*'],
    autoHideAfterDays: 2,
  },
  {
    id: 'banner_grace_period',
    stage: DunningStage.GRACE_PERIOD,
    title: 'Service Will Be Restricted',
    message: 'Your payment is {{daysOverdue}} days overdue. Update your payment method within {{daysRemaining}} days to avoid service restriction.',
    variant: 'error',
    dismissable: false,
    actions: [
      { label: 'Resolve Now', url: '/billing/payment', primary: true },
      { label: 'Contact Support', url: '/support', primary: false },
    ],
    showOnPages: ['/', '/dashboard', '/settings/*', '/agents/*'],
  },
  {
    id: 'banner_suspended',
    stage: DunningStage.SUSPENSION,
    title: 'Service Suspended',
    message: 'Your subscription has been suspended due to non-payment. Update your payment method to reactivate your service.',
    variant: 'critical',
    dismissable: false,
    actions: [
      { label: 'Reactivate', url: '/billing/reactivate', primary: true },
      { label: 'Export Data', url: '/settings/export', primary: false },
    ],
    showOnPages: ['*'],          // Show on all pages
  },
];

class InAppBannerService {
  async getActiveBanners(customerId: string): Promise<InAppBanner[]> {
    const dunningState = await this.getDunningState(customerId);
    if (!dunningState) return [];

    const banners = IN_APP_BANNERS.filter(b => b.stage === dunningState.currentStage);
    const daysRemaining = this.getDaysRemaining(dunningState);

    return banners.map(banner => ({
      ...banner,
      message: this.interpolateMessage(banner.message, {
        daysRemaining: daysRemaining.toString(),
        daysOverdue: this.getDaysOverdue(dunningState).toString(),
      }),
    }));
  }
}
```

## Push Notifications

```typescript
interface PushNotificationTemplate {
  id: string;
  stage: DunningStage;
  title: string;
  body: string;
  deepLink: string;
  urgency: 'default' | 'timeSensitive' | 'critical';
}

const PUSH_TEMPLATES: PushNotificationTemplate[] = [
  {
    id: 'push_soft_reminder',
    stage: DunningStage.SOFT_REMINDER,
    title: 'Payment Update Needed',
    body: 'Tap to update your payment method and keep your service active.',
    deepLink: 'yourapp://billing/payment',
    urgency: 'default',
  },
  {
    id: 'push_grace_expiring',
    stage: DunningStage.GRACE_PERIOD,
    title: 'Service Expiring Soon',
    body: 'Your service will be restricted in 3 days. Update payment now.',
    deepLink: 'yourapp://billing/payment',
    urgency: 'timeSensitive',
  },
];
```

## Open-Source Tools

- **Handlebars** (MIT) — Email template rendering
- **BullMQ** — Communication scheduling and delivery
- **PostgreSQL** — Communication logs and preferences
- **Redis** — Rate limiting for SMS and email
- **Inbucket** (MIT) — Email preview and testing
- **Nodemailer** (MIT) — Email transport

## Integration Points

Dunning communication integrates with the dunning workflow (triggers per stage), customer preferences (channel opt-in), template engine (rendering), delivery service (sending), and analytics (open/click tracking).

## Production Considerations

- Respect customer communication preferences and timezone
- Implement rate limiting per channel per customer
- Track email open rates and SMS delivery rates per stage
- A/B test subject lines and CTAs to optimize recovery
- Include unsubscribe link in all emails
- Use short links for SMS due to character limits
- Fall back to email if push notification delivery fails
- Log all communications for compliance and audit

## Open-Source First Philosophy

Handlebars renders all dunning email templates with dynamic variables from the dunning state. BullMQ schedules communications with timezone-aware delivery. Nodemailer handles email delivery through any SMTP provider. PostgreSQL logs every communication for audit. This stack replaces proprietary communication platforms while maintaining full control over messaging and customer data.
