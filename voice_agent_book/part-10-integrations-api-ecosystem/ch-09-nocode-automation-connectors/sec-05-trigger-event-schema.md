# Section 05: Trigger Event Schema

## Overview

The Trigger Event Schema defines the standardized event data structure that the voice agent platform exposes to no-code automation connectors (Zapier, Make, n8n, Workato). When an event occurs in the platform (call completed, message sent, payment received, customer created), the automation connector receives a normalized event payload that contains all the data needed to drive automation workflows. The schema is designed to be consistent across all supported automation platforms while accommodating each platform's specific requirements.

The trigger schema covers the full set of platform events that are useful for automation: call lifecycle events (incoming, ringing, answered, completed, failed), messaging events (SMS received, SMS delivered, WhatsApp message), customer events (created, updated, tagged), payment events (succeeded, failed, refunded), and analytics events (daily summary, threshold breached). Each event type has a defined schema that is versioned and guaranteed backward-compatible within a major version.

## Architecture

```
                Trigger Event Schema Structure

   Event Sources → Event Normalizer → Automation Connector
                        |
   +----------------------------------------------------------+
   |              Event Schema Components                     |
   |                                                          |
   |  +----------------------------------------------------+ |
   |  |  Event Envelope (Common to all events)             | |
   |  |  - event_id (string, unique)                       | |
   |  |  - event_type (string, dotted notation)            | |
   |  |  - event_version (string, semver)                  | |
   |  |  - timestamp (ISO 8601)                            | |
   |  |  - tenant_id (string)                              | |
   |  |  - account_subdomain (string)                      | |
   |  |  - environment (production/sandbox)                | |
   |  +----------------------------------------------------+ |
   |              |                                           |
   |              v                                           |
   |  +----------------------------------------------------+ |
   |  |  Event Payload (Specific to event type)            | |
   |  |  Call: call_sid, duration, status, customer_phone  | |
   |  |  Payment: transaction_id, amount, currency, status | |
   |  |  Customer: customer_id, name, email, phone         | |
   |  |  Message: message_id, to, channel, status          | |
   |  +----------------------------------------------------+ |
   |              |                                           |
   |              v                                           |
   |  +----------------------------------------------------+ |
   |  |  Platform-Specific Wrapper (Zapier/Make/n8n/Workato)| |
   |  |  - Platform-specific fields                         | |
   |  |  - Authentication context                           | |
   |  |  - Rate limit headers                               | |
   |  +----------------------------------------------------+ |
   +----------------------------------------------------------+
```

## Design Decisions

- **Dotted event type notation over flat strings:** Event types use a hierarchical dotted notation: `call.completed`, `call.incoming`, `payment.succeeded`, `customer.created`, `message.sms.received`. This enables consumers to subscribe to event hierarchies using wildcards (e.g., `call.*` for all call events, `*.completed` for all completed events). The hierarchy is extensible without breaking existing subscriptions. Trade-off: dotted notation requires careful namespace management but provides powerful subscription filtering and self-documenting event type names.

- **Timestamps in ISO 8601 with timezone offset over Unix epoch:** All timestamps include timezone offset (e.g., `2026-05-27T14:30:00-04:00`). This allows consumers in different timezones to display events in local time without conversion logic. The timestamp represents the time the event occurred (not when it was emitted — they may differ due to queue processing). Trade-off: ISO 8601 strings are larger than Unix epoch integers but are human-readable and timezone-aware.

- **PII field handling via explicit inclusion over automatic filtering:** PII fields (phone numbers, email addresses, names) are included in the event payload by default but can be filtered based on the automation connector's data handling policy. The platform provides a configuration option on the webhook endpoint to mask PII fields (replace with `***`). This allows compliance with data protection regulations (GDPR, CCPA) while maintaining event utility. Trade-off: PII masking reduces event payload usefulness for some automation scenarios but provides compliance with data protection regulations.

## Implementation Approach

```
// Event type registry
const EVENT_TYPES = {
  call: {
    incoming: 'call.incoming',
    answered: 'call.answered',
    completed: 'call.completed',
    failed: 'call.failed',
    recording_ready: 'call.recording_ready',
    transcription_ready: 'call.transcription_ready',
  },
  message: {
    sms: {
      received: 'message.sms.received',
      sent: 'message.sms.sent',
      delivered: 'message.sms.delivered',
      failed: 'message.sms.failed',
    },
    whatsapp: {
      received: 'message.whatsapp.received',
      sent: 'message.whatsapp.sent',
      delivered: 'message.whatsapp.delivered',
    },
  },
  payment: {
    succeeded: 'payment.succeeded',
    failed: 'payment.failed',
    refunded: 'payment.refunded',
    dispute_opened: 'payment.dispute_opened',
  },
  customer: {
    created: 'customer.created',
    updated: 'customer.updated',
    tagged: 'customer.tagged',
    merged: 'customer.merged',
  },
  analytics: {
    daily_summary: 'analytics.daily_summary',
    threshold_breached: 'analytics.threshold_breached',
  },
} as const;

// Generic event envelope
interface AutomationEventEnvelope {
  event_id: string;
  event_type: string;
  event_version: string;
  timestamp: string;           // ISO 8601 with offset
  tenant_id: string;
  account_subdomain: string;
  environment: 'production' | 'sandbox';
  data: Record<string, any>;
}

// Specific event payloads
interface CallCompletedPayload {
  call_sid: string;
  duration: number;
  status: 'completed' | 'failed' | 'busy' | 'no_answer' | 'canceled';
  customer_phone: string;       // May be masked
  agent_id?: string;
  campaign_id?: string;
  recording_url?: string;
  transcription?: string;
  completed_at: string;
  metadata?: Record<string, string>;
}

interface PaymentSucceededPayload {
  transaction_id: string;
  amount: number;
  currency: string;
  customer_id: string;
  payment_method: string;
  subscription_id?: string;
  invoice_id?: string;
  succeeded_at: string;
}

interface CustomerCreatedPayload {
  customer_id: string;
  name: string;
  email: string;
  phone: string;
  tags: string[];
  source: 'phone' | 'web' | 'api' | 'import';
  custom_fields: Record<string, any>;
  created_at: string;
}

// Event factory: builds platform-specific event payloads
class AutomationEventFactory {
  private piiMasking: boolean;

  constructor(piiMasking: boolean = false) {
    this.piiMasking = piiMasking;
  }

  buildCallCompleted(raw: CallCompletedData, tenant: TenantInfo): AutomationEventEnvelope {
    const payload: CallCompletedPayload = {
      call_sid: raw.callSid,
      duration: raw.duration,
      status: raw.status,
      customer_phone: this.piiMasking ? this.maskPhone(raw.customerPhone) : raw.customerPhone,
      agent_id: raw.agentId,
      campaign_id: raw.campaignId,
      recording_url: raw.recordingUrl,
      transcription: raw.transcription,
      completed_at: raw.completedAt.toISOString(),
      metadata: raw.metadata,
    };

    return {
      event_id: generateId('evt'),
      event_type: 'call.completed',
      event_version: '1.0.0',
      timestamp: new Date().toISOString(),
      tenant_id: tenant.id,
      account_subdomain: tenant.subdomain,
      environment: tenant.environment,
      data: payload,
    };
  }

  buildPaymentSucceeded(raw: PaymentData, tenant: TenantInfo): AutomationEventEnvelope {
    return {
      event_id: generateId('evt'),
      event_type: 'payment.succeeded',
      event_version: '1.0.0',
      timestamp: new Date().toISOString(),
      tenant_id: tenant.id,
      account_subdomain: tenant.subdomain,
      environment: tenant.environment,
      data: {
        transaction_id: raw.transactionId,
        amount: raw.amount,
        currency: raw.currency,
        customer_id: raw.customerId,
        payment_method: raw.paymentMethod,
        subscription_id: raw.subscriptionId,
        invoice_id: raw.invoiceId,
        succeeded_at: raw.processedAt.toISOString(),
      } as PaymentSucceededPayload,
    };
  }

  // Format for Zapier (requires array of items)
  toZapierFormat(event: AutomationEventEnvelope): any[] {
    return [event.data]; // Zapier expects just the data in an array
  }

  // Format for Make (uses full envelope)
  toMakeFormat(event: AutomationEventEnvelope): any {
    return event; // Make can use the full envelope
  }

  // Format for n8n (uses full envelope)
  toN8nFormat(event: AutomationEventEnvelope): any {
    return { json: event };
  }

  // Format for Workato (specific field mapping)
  toWorkatoFormat(event: AutomationEventEnvelope): any {
    return event.data; // Workato maps fields automatically
  }

  private maskPhone(phone: string): string {
    if (!phone || phone.length < 6) return phone;
    const last4 = phone.slice(-4);
    return `${phone.slice(0, -6)}******${last4}`;
  }

  private maskEmail(email: string): string {
    const [local, domain] = email.split('@');
    if (!domain) return email;
    return `${local[0]}***@${domain}`;
  }
}

// Schema validation (using Zod)
const callCompletedSchema = z.object({
  call_sid: z.string(),
  duration: z.number().int().min(0),
  status: z.enum(['completed', 'failed', 'busy', 'no_answer', 'canceled']),
  customer_phone: z.string(),
  agent_id: z.string().optional(),
  campaign_id: z.string().optional(),
  recording_url: z.string().url().optional(),
  transcription: z.string().optional(),
  completed_at: z.string().datetime(),
  metadata: z.record(z.string()).optional(),
});

const paymentSucceededSchema = z.object({
  transaction_id: z.string(),
  amount: z.number().positive(),
  currency: z.string().length(3),
  customer_id: z.string(),
  payment_method: z.string(),
  subscription_id: z.string().optional(),
  invoice_id: z.string().optional(),
  succeeded_at: z.string().datetime(),
});
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Zod (MIT) | Validation | Event payload validation |
| Date-fns-tz (MIT) | Dates | ISO 8601 with timezone |

## Production Considerations

**Scaling:** Event payload schemas must be performance-optimized — avoid large nested objects that increase serialization time. The maximum recommended payload size is 100KB. For payloads exceeding this (e.g., full transcription text), include a URL reference to fetch the data separately. Use a schema registry to manage schema evolution and ensure all automation connectors receive valid payloads.

**Security:** PII field masking should be the default for Sandbox environments and optional for Production. Document PII field handling in the automation connector documentation. Include data classification tags (`sensitive: true`) in schema metadata for fields containing PII. The automation event factory should never include API keys, credentials, or internal system identifiers in event payloads.

**Monitoring:** Track event schema validation failure rates (events that don't match their schema — indicates a bug), PII masking toggle usage (how many connectors enable vs. disable masking), event payload size distribution, and payload serialization/deserialization time. Alert on schema validation failures and payload sizes exceeding 100KB.
