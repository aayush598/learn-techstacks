# Section 05: Welcome Flow & Email Automation

## Overview

The welcome flow transforms a newly provisioned tenant into an engaged, active user. It combines automated email sequences, in-app messaging, and guided onboarding to accelerate time-to-first-call and increase activation rates. A well-crafted welcome sequence educates users about platform capabilities, demonstrates value, and builds momentum toward the "aha moment" where the user experiences the core value proposition for the first time.

The welcome flow is triggered when provisioning completes and tenant status changes to `active`. It includes a welcome email (immediate), a getting-started email sequence (days 1-7), in-app banners and tooltips, educational content (docs, videos, webinars), and milestone-triggered communications (first call made, first campaign launched). Each communication should be personalized with the tenant's name, industry, use case, and configuration choices.

For a voice agent platform, the critical "aha moment" is the first successful inbound or outbound call handled by the AI agent. The welcome flow should aggressively guide users toward this outcome, removing friction and providing hand-holding through the first call setup.

## Design Decisions

- **React Flow over Custom**: Battle-tested node/edge rendering. Saves 6+ months custom development.
- **Local-First State**: Zustand + debounced saves (2s). Instant UI response without waiting for API.
- **Function-as-Edge**: Edges carry conditions and transforms. Flow evaluates conditions at each step.
## Implementation Approach

```typescript
interface WelcomeStep {
  trigger: WelcomeTrigger;
  channel: 'email' | 'in_app' | 'sms' | 'slack';
  delay?: Duration; // for time-based
  template: string;
  data: (tenant: Tenant) => Record<string, any>;
}

class WelcomeAutomation {
  private steps: WelcomeStep[];

  constructor(
    private emailService: EmailService,
    private notificationService: NotificationService,
    private analytics: AnalyticsService
  ) {
    this.steps = [
      {
        trigger: { type: 'provisioning_complete' },
        channel: 'email',
        delay: { minutes: 0 },
        template: 'welcome-email',
        data: (t) => ({ name: t.name, dashboardUrl: `https://app.voiceagent.com/dashboard?tenant=${t.id}` }),
      },
      {
        trigger: { type: 'provisioning_complete' },
        channel: 'in_app',
        delay: { minutes: 0 },
        template: 'welcome-banner',
        data: (t) => ({ steps: ['Setup phone number', 'Create your first agent', 'Make a test call'] }),
      },
      {
        trigger: { type: 'step_completed', step: 'phone_number' },
        channel: 'email',
        delay: { minutes: 0 },
        template: 'phone-setup-complete',
        data: (t) => ({ phoneNumber: t.phoneNumber }),
      },
      {
        trigger: { type: 'step_completed', step: 'agent_created' },
        channel: 'email',
        delay: { minutes: 0 },
        template: 'agent-created',
        data: (t) => ({ agentName: t.agentName, testCallUrl: `...` }),
      },
      {
        trigger: { type: 'first_call_completed' },
        channel: 'email',
        delay: { minutes: 5 },
        template: 'first-call-celebration',
        data: (t) => ({ duration: t.callDuration, transcriptUrl: `...` }),
      },
      {
        trigger: { type: 'no_activity' },
        condition: { daysSinceProvisioning: 3 },
        channel: 'email',
        template: 'check-in',
        data: (t) => ({ supportUrl: '...' }),
      },
    ];
  }

  async handleEvent(event: WelcomeEvent): Promise<void> {
    const matchingSteps = this.steps.filter(s => 
      this.matchesTrigger(s.trigger, event)
    );

    for (const step of matchingSteps) {
      await this.sendCommunication(step, event.tenant);
      await this.analytics.track('welcome.step_sent', {
        tenantId: event.tenant.id,
        step: step.template,
        channel: step.channel,
      });
    }
  }

  private async sendCommunication(step: WelcomeStep, tenant: Tenant): Promise<void> {
    const data = step.data(tenant);
    
    switch (step.channel) {
      case 'email':
        await this.emailService.send({
          to: tenant.adminEmail,
          template: step.template,
          data,
        });
        break;
      case 'in_app':
        await this.notificationService.sendInApp({
          tenantId: tenant.id,
          template: step.template,
          data,
        });
        break;
      case 'sms':
        await this.notificationService.sendSms({
          to: tenant.adminPhone,
          template: step.template,
          data,
        });
        break;
    }
  }
}

// Email template example
const WELCOME_EMAIL_TEMPLATE = `
Subject: Welcome to VoiceAgent, {{name}}!

Hi {{name}},

Welcome to VoiceAgent! Your AI voice agent platform is ready.

Here's what to do next:
1. **Set up your phone number** — Get a local number or bring your own
2. **Create your first agent** — Use our templates or build from scratch
3. **Make a test call** — Hear your AI agent in action

👉 [Start Setup]({{dashboardUrl}})

Need help? Reply to this email or check our [documentation](https://docs.voiceagent.com).

Best,
The VoiceAgent Team
`;

// Onboarding checklist component
function OnboardingChecklist({ tenantId, progress }: Props) {
  const steps = [
    { id: 'phone', label: 'Set up phone number', completed: progress.hasPhone },
    { id: 'agent', label: 'Create your first agent', completed: progress.hasAgent },
    { id: 'call', label: 'Make a test call', completed: progress.hasTestCall },
    { id: 'team', label: 'Invite team members', completed: progress.hasTeam, optional: true },
    { id: 'integrations', label: 'Connect integrations', completed: progress.hasIntegrations, optional: true },
  ];

  return (
    <div className="onboarding-checklist">
      <h3>Getting Started ({steps.filter(s => s.completed).length}/{steps.length})</h3>
      <ul>
        {steps.map(step => (
          <li key={step.id} className={step.completed ? 'completed' : 'pending'}>
            <span className="status-icon">{step.completed ? '✓' : '○'}</span>
            {step.label}
            {step.optional && <span className="badge">Optional</span>}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## Integration Points

- **Email Service (Part 20):** Transactional email delivery with SendGrid/Resend
- **In-App Notifications:** Real-time notification delivery via WebSocket
- **Analytics (Part 11):** Welcome funnel tracking and conversion metrics
- **Support System:** In-app chat integration for help during onboarding
- **Onboarding Checklist:** Dashboard component showing completion progress

## Open-Source Tools

- **React Flow** (MIT): Node-based UI
- **Zustand** (MIT): State management
- **Immer** (MIT): Immutable updates
## Production Considerations

- **Email Deliverability:** Monitor welcome email deliverability rates. A welcome email landing in spam kills the onboarding experience. Use dedicated sending domains and warm IP addresses.
- **Opt-Out Management:** Include unsubscribe links in all marketing emails. Transactional emails (related to account activity) should have notification preference links instead.
- **Multi-Language Welcome:** If the tenant set a non-English language during signup, send welcome emails in their language. This requires translated email templates for all supported languages.
- **Welcome Flow Testing:** Regularly test the complete welcome flow from signup to first call. Record a new tenant weekly and verify all emails arrive, links work, and in-app messages display.
- **Segmentation:** Different welcome flows for different segments: self-service signup vs sales-assisted enterprise, different industries, different use cases. A/B test variations.
- **Re-engagement:** Users who sign up but never complete setup get a re-engagement sequence (day 3, 7, 14, 30). Offer help (book a call) or simplified setup path.
