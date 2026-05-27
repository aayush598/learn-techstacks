# Section 01: Transactional Email Architecture

## Overview

The transactional email system sends automated emails triggered by events. It provides a provider-agnostic abstraction layer supporting Resend, SendGrid, and SES. The system handles email queuing, delivery tracking, bounce handling, and template rendering. Providers are interchangeable via adapter pattern.

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  App Events  │────▶│  Email Queue  │────▶│  Provider     │
│              │     │  (BullMQ)     │     │  Adapter      │
│  Alert       │     │              │     │              │
│  Digest      │────▶│  Templates   │────▶│  Resend      │
│  Welcome     │     │  Renderer    │     │  SendGrid    │
│  Invoice     │────▶│              │────▶│  SES         │
│              │     │  Bounce      │     │              │
│              │     │  Handler     │     │  Webhook     │
└──────────────┘     └──────────────┘     └──────────────┘
```

## Implementation Approach

```typescript
interface EmailPayload {
  to: string[];
  subject: string;
  html?: string;
  text?: string;
  templateId?: string;
  templateData?: Record<string, unknown>;
  attachments?: Attachment[];
  headers?: Record<string, string>;
  tags?: Record<string, string>;
}

interface EmailProvider {
  send(email: EmailPayload): Promise<EmailResult>;
  validate(email: EmailPayload): Promise<ValidationResult>;
  getDeliveryStatus(messageId: string): Promise<DeliveryStatus>;
}

class EmailService {
  private provider: EmailProvider;
  private queue: EmailQueue;

  async send(email: EmailPayload, options?: SendOptions): Promise<EmailResult> {
    const validated = await this.provider.validate(email);
    if (!validated.valid) throw new EmailValidationError(validated.errors);

    if (options?.priority === 'high') {
      return this.provider.send(email);
    }

    // Queue for async delivery
    return this.queue.enqueue({
      ...email,
      scheduledAt: options?.scheduledAt,
      priority: options?.priority || 'normal',
    });
  }

  async handleDeliveryWebhook(webhook: DeliveryWebhook): Promise<void> {
    const status = await this.provider.getDeliveryStatus(webhook.messageId);
    await this.deliveryStore.update(webhook.messageId, {
      status: webhook.event,
      timestamp: new Date().toISOString(),
      details: webhook,
    });

    if (webhook.event === 'bounce') {
      await this.handleBounce(webhook);
    }
  }

  private async handleBounce(webhook: DeliveryWebhook): Promise<void> {
    // Mark email as bounced
    await this.userService.markEmailBounced(webhook.to);

    // Remove from active list
    if (webhook.bounceType === 'permanent') {
      await this.userService.removeEmail(webhook.to);
    }

    // Update analytics
    await this.analyticsService.trackBounce(webhook);
  }
}

class ResendProvider implements EmailProvider {
  async send(email: EmailPayload): Promise<EmailResult> {
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: this.fromAddress,
        to: email.to,
        subject: email.subject,
        html: email.html,
        text: email.text,
        attachments: email.attachments,
        headers: email.headers,
        tags: email.tags,
      }),
    });
    const data = await response.json();
    return { messageId: data.id, status: 'sent', provider: 'resend' };
  }

  async validate(email: EmailPayload): Promise<ValidationResult> {
    const errors: string[] = [];
    if (!email.to.length) errors.push('No recipients');
    if (!email.subject) errors.push('No subject');
    if (!email.html && !email.text) errors.push('No content');
    return { valid: errors.length === 0, errors };
  }

  async getDeliveryStatus(messageId: string): Promise<DeliveryStatus> {
    const response = await fetch(`https://api.resend.com/emails/${messageId}`, {
      headers: { 'Authorization': `Bearer ${this.apiKey}` },
    });
    return response.json();
  }
}
```

## Integration Points

- **Provider Switching**: Swap providers via config change
- **Webhook Endpoints**: Provider delivery webhooks
- **Email Queue**: Async processing for non-critical emails

## Production Considerations

- **Sending Reputation**: Warm up sending domains gradually
- **Delivery Monitoring**: Track bounce rates, spam complaints
- **Provider Fallback**: Fallback to secondary provider on failure
