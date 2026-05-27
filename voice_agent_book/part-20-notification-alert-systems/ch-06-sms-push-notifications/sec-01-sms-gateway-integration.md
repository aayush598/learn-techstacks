# Section 01: SMS Gateway Integration

## Overview

The SMS gateway integration sends text messages through providers like Twilio. The system provides provider abstraction, message formatting, delivery receipts, and number pooling. Multiple provider support enables failover and regional optimization.

## Implementation Approach

```typescript
interface SMSConfig {
  provider: 'twilio' | 'vonage' | 'aws_sns' | 'plivo';
  accountSid: string;
  authToken: string;
  fromNumber: string;
  messagingServiceSid?: string;
  statusCallback: string;
}

interface SMSMessage {
  to: string;
  body: string;
  from?: string;
  mediaUrl?: string[];
  statusCallback?: string;
  validityPeriod?: number;
}

class SMSGateway {
  private provider: SMSProvider;

  async send(message: SMSMessage): Promise<SMSResult> {
    const normalized = this.normalizeNumber(message.to);
    return this.provider.send({ ...message, to: normalized });
  }

  async handleStatusCallback(webhook: SMSStatusWebhook): Promise<void> {
    await this.deliveryStore.update(webhook.messageSid, {
      status: webhook.SmsStatus,
      timestamp: new Date().toISOString(),
      errorCode: webhook.ErrorCode,
    });

    if (webhook.SmsStatus === 'delivered') {
      await this.analyticsService.trackDelivery('sms', true);
    } else if (webhook.SmsStatus === 'failed' || webhook.SmsStatus === 'undelivered') {
      await this.analyticsService.trackDelivery('sms', false);
      await this.handleFailedDelivery(webhook);
    }
  }

  private normalizeNumber(number: string): string {
    // Remove non-digit characters and ensure E.164 format
    const cleaned = number.replace(/\D/g, '');
    if (!cleaned.startsWith('+')) {
      return `+${cleaned}`;
    }
    return cleaned;
  }

  private async handleFailedDelivery(webhook: SMSStatusWebhook): Promise<void> {
    const message = await this.deliveryStore.get(webhook.messageSid);
    if (message.retryCount < this.config.maxRetries) {
      await this.deliveryStore.updateRetry(webhook.messageSid, message.retryCount + 1);
      await this.send({ to: message.to, body: message.body });
    }
  }
}

class TwilioProvider implements SMSProvider {
  private client: Twilio;

  constructor(config: SMSConfig) {
    this.client = twilio(config.accountSid, config.authToken);
  }

  async send(message: SMSMessage): Promise<SMSResult> {
    const result = await this.client.messages.create({
      to: message.to,
      from: message.from || this.fromNumber,
      body: message.body,
      statusCallback: message.statusCallback,
      validityPeriod: message.validityPeriod || 28800, // 8 hours
    });
    return { messageSid: result.sid, status: 'queued', provider: 'twilio' };
  }

  async getMessageStatus(sid: string): Promise<DeliveryStatus> {
    const message = await this.client.messages(sid).fetch();
    return { status: message.status, errorCode: message.errorCode, errorMessage: message.errorMessage };
  }
}
```

## Integration Points

- **Status Callbacks**: Webhook endpoints for delivery status
- **Number Pool**: Manage and rotate sender numbers
- **Provider Fallback**: Switch providers on failure

## Production Considerations

- **10DLC Compliance**: Register for 10DLC in US
- **Number Pooling**: Multiple numbers to avoid rate limits
- **Cost Tracking**: Monitor SMS costs per message
