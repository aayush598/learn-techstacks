# Section 08: Webhook Testing Tools

## Overview

Webhook testing tools enable developers to validate their webhook integration without triggering real events. Tools include test event generation, endpoint simulation, delivery inspection, and signature verification utilities. Testing is available through both the developer portal UI and programmatic CLI/SDK interfaces.

## Architecture

```
Webhook Testing Tools
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test Event Generator:
  ┌────────────────────────────────────────────────────┐
  │ Test Event Types:                                   │
  │                                                     │
  │  ○ call.started      ─ Standard call initiation    │
  │  ○ call.completed    ─ Standard call completion    │
  │  ○ call.failed       ─ Call failure scenario       │
  │  ○ agent.deployed    ─ Agent deployment event      │
  │  ● webhook.test      ─ Generic test event          │
  │  ○ Custom Payload    ─ JSON editor                 │
  └────────────────────────────────────────────────────┘

Delivery Simulation:
  [Developer] → Select Test Event → [Simulation Engine]
                                         │
                ┌─────────────────────────┼────────────────────────┐
                │                         │                        │
            [Real Endpoint]         [Test URL (no auth)]     [Webhook.site/RequestBin]
                │                         │                        │
            See delivery             Inspect payload          Capture raw request
            in dashboard             without real server       with public URL

CLI Testing:
  $ voiceagent webhook test \
      --endpoint wh_abc_123 \
      --event call.completed \
      --payload '{"call_id":"test_123"}'

  $ voiceagent webhook inspect \
      --id delivery_xyz_789

  $ voiceagent webhook verify \
      --payload payload.json \
      --signature "sha256=..." \
      --timestamp 1684512345 \
      --secret whsec_abc123
```

## Design Decisions

- **Test Event vs Real Event**: Test events are tagged with `test_` prefix in event ID; dashboard filters them separately
- **No Side Effects**: Test events don't trigger downstream processing (no actual calls, no billing)
- **Delivery Simulation**: Test delivery goes through the same pipeline as real events but without side effects
- **CLI Integration**: Full testing capability from command line for CI/CD pipelines

## Implementation Approach

```typescript
// Test event types
interface TestEventGenerator {
  eventTypes: Record<string, () => WebhookEventEnvelope>;
}

class WebhookTestEventGenerator {
  private generators: Record<string, () => WebhookEventEnvelope> = {
    'webhook.test': () => ({
      type: 'webhook.test',
      version: 1,
      id: `test_${crypto.randomUUID()}`,
      timestamp: new Date().toISOString(),
      topic: 'webhook',
      data: { message: 'This is a test webhook delivery', timestamp: new Date().toISOString() },
    }),

    'call.started': () => ({
      type: 'call.started',
      version: 1,
      id: `test_${crypto.randomUUID()}`,
      timestamp: new Date().toISOString(),
      topic: 'calls',
      data: {
        call_id: 'test_call_started',
        agent_id: 'test_agent',
        from_number: '+15551234567',
        to_number: '+15557654321',
        direction: 'inbound',
      },
    }),

    'call.completed': () => ({
      type: 'call.completed',
      version: 1,
      id: `test_${crypto.randomUUID()}`,
      timestamp: new Date().toISOString(),
      topic: 'calls',
      data: {
        call_id: 'test_call_completed',
        agent_id: 'test_agent',
        duration_seconds: 120,
        status: 'completed',
        transcript_summary: 'Test call completed successfully',
        sentiment: 'positive',
      },
    }),

    'call.failed': () => ({
      type: 'call.failed',
      version: 1,
      id: `test_${crypto.randomUUID()}`,
      timestamp: new Date().toISOString(),
      topic: 'calls',
      data: {
        call_id: 'test_call_failed',
        agent_id: 'test_agent',
        duration_seconds: 0,
        status: 'failed',
        failure_reason: 'No answer',
      },
    }),

    'agent.deployed': () => ({
      type: 'agent.deployed',
      version: 1,
      id: `test_${crypto.randomUUID()}`,
      timestamp: new Date().toISOString(),
      topic: 'agents',
      data: {
        agent_id: 'test_agent',
        agent_name: 'Test Agent',
        deployed_at: new Date().toISOString(),
        version: '1.0.0-test',
      },
    }),
  };

  generate(eventType: string, customPayload?: Record<string, unknown>): WebhookEventEnvelope {
    if (customPayload) {
      return {
        type: eventType,
        version: 1,
        id: `test_${crypto.randomUUID()}`,
        timestamp: new Date().toISOString(),
        topic: 'custom',
        data: customPayload,
      };
    }

    const generator = this.generators[eventType];
    if (!generator) {
      throw new Error(`Unknown test event type: ${eventType}`);
    }

    return generator();
  }

  getAvailableEventTypes(): string[] {
    return Object.keys(this.generators);
  }
}

// Test delivery service
class WebhookTestService {
  constructor(
    private eventGenerator: WebhookTestEventGenerator,
    private deliveryService: WebhookDeliveryService,
    private signer: WebhookSigner,
  ) {}

  async sendTestDelivery(
    endpointId: string,
    eventType: string,
    customPayload?: Record<string, unknown>,
  ): Promise<TestDeliveryResult> {
    const event = this.eventGenerator.generate(eventType, customPayload);
    const endpoint = await this.endpointRepository.findById(endpointId);

    // Sign the event
    const { signature, timestamp } = this.signer.sign(
      JSON.stringify(event),
      endpoint.secret,
    );

    // Deliver
    const startTime = Date.now();
    try {
      const response = await fetch(endpoint.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'VoiceAgent-Webhook/1.0 (test)',
          'X-VoiceAgent-Signature': `sha256=${signature}`,
          'X-VoiceAgent-Timestamp': timestamp.toString(),
          'X-VoiceAgent-Event-Id': event.id,
          'X-VoiceAgent-Delivery-Attempt': '1',
          'X-VoiceAgent-Idempotency-Key': event.id,
        },
        body: JSON.stringify(event),
        timeout: 30_000,
      });

      return {
        success: response.ok,
        eventId: event.id,
        statusCode: response.status,
        statusText: response.statusText,
        latencyMs: Date.now() - startTime,
        responseBody: await response.text(),
        responseHeaders: Object.fromEntries(response.headers),
      };
    } catch (error) {
      return {
        success: false,
        eventId: event.id,
        statusCode: 0,
        latencyMs: Date.now() - startTime,
        error: (error as Error).message,
      };
    }
  }

  // Verify signature (for receiver testing)
  verifySignature(
    payload: string,
    signatureHeader: string,
    timestampHeader: string,
    secret: string,
  ): { valid: boolean; details: string } {
    const signature = signatureHeader.replace('sha256=', '');
    const timestamp = parseInt(timestampHeader, 10);

    const isValid = this.signer.verify(payload, signature, timestamp, secret);

    return {
      valid: isValid,
      details: isValid
        ? 'Signature verification passed — webhook is authentic'
        : 'Signature verification failed — webhook may be forged or payload was tampered',
    };
  }
}

// CLI testing commands
const webhookTestCommand = {
  name: 'webhook test',
  description: 'Send a test webhook delivery',
  options: [
    { flag: '--endpoint <id>', description: 'Endpoint ID' },
    { flag: '--event <type>', description: 'Event type' },
    { flag: '--payload <json>', description: 'Custom payload (JSON)' },
  ],
  async run(args: Record<string, string>): Promise<void> {
    const service = new WebhookTestService(/* deps */);
    const result = await service.sendTestDelivery(
      args.endpoint,
      args.event,
      args.payload ? JSON.parse(args.payload) : undefined,
    );
    console.table(result);
  },
};
```

## Integration Points

- **Developer Portal**: Test webhook UI with event type selector and payload editor
- **CLI Tool**: `voiceagent webhook test` command for CI testing
- **SDK**: `client.webhooks.test()` method for programmatic testing

## Production Considerations

- **Test Event Quota**: Limit test events to 100 per hour per tenant to prevent abuse
- **Test Endpoint Verification**: Test deliveries respect same rate limits as real deliveries
- **No Billing Impact**: Test events are not billed and don't count toward usage quotas
- **Webhook.site Integration**: Quick test endpoint using public request inspection services

## Open-Source Tools

- **Webhook.site**: Public endpoint for inspecting webhook deliveries
- **RequestBin**: Temporary URL for capturing and inspecting webhook requests
