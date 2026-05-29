# Section 05: Consumer SDK

## Overview

The webhook consumer SDK simplifies webhook integration for consumers. It provides signature verification helpers, retry handling, event type parsing, and type-safe payload deserialization. The SDK is distributed as an npm package for Node.js consumers.

## Architecture

```
Consumer SDK Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[SDK Package] → [Consumer Application]
       │                    │
  @voiceagent/webhooks   Express/Fastify
       │                handler integration
  ├── WebhookVerifier    │
  │   - verify()         │
  │   - middleware()     req → verify → parse → handle
  │   - middlewareAsync()│
  ├── EventParser        [Consumer Code]
  │   - parse()          app.post('/webhooks', (req, res) => {
  │   - typed events       const verified = verifier.verify(req);
  │   - type guards        const event = parser.parse(req.body);
  ├── RetryHandler         handler.handle(event);
  │   - shouldRetry()      res.status(200).send({ ok: true });
  │   - computeDelay()   });
  └── Types
      - TypeScript types
      - Event interfaces

SDK Usage:
  import { createWebhookHandler } from '@voiceagent/webhooks';

  const handler = createWebhookHandler({
    secret: process.env.WEBHOOK_SECRET,
    toleranceMs: 300000,
  });

  app.post('/webhooks/voiceagent', handler.middleware());
```

## Design Decisions

- **Express/Fastify Middleware**: First-class framework support
- **TypeScript-First**: Full type definitions for all event types
- **Framework-Agnostic Core**: Core verifier works with any HTTP framework
- **Minimal Dependencies**: Zero external runtime dependencies

## Implementation Approach

```typescript
// SDK types
interface WebhookSDKConfig {
  secret: string;
  toleranceMs?: number;
  onError?: (error: WebhookError) => void;
}

interface WebhookEventPayload<T = unknown> {
  id: string;
  type: WebhookEventType;
  payload: T;
  idempotencyKey: string;
  timestamp: string;
  tenantId: string;
}

type WebhookEventType =
  | 'agent.created'
  | 'agent.updated'
  | 'agent.deleted'
  | 'call.completed'
  | 'call.failed'
  | 'call.recording.ready'
  | 'alert.fired'
  | 'alert.resolved';

interface CallCompletedPayload {
  callId: string;
  duration: number;
  status: 'completed' | 'failed' | 'timeout';
  recordingUrl?: string;
  transcriptUrl?: string;
  sentiment: string;
}

// Core SDK
class WebhookVerifier {
  private signer: WebhookSigner;

  constructor(private config: WebhookSDKConfig) {
    this.signer = new WebhookSigner();
  }

  verify(
    body: Record<string, unknown>,
    headers: Record<string, string | string[] | undefined>,
  ): boolean {
    const signature = this.getHeader(headers, 'x-webhook-signature');
    const timestamp = this.getHeader(headers, 'x-webhook-timestamp');
    const webhookId = this.getHeader(headers, 'x-webhook-id');
    const version = this.getHeader(headers, 'x-webhook-version') || 'v1';

    if (!signature || !timestamp || !webhookId) {
      throw new WebhookError('Missing required webhook headers');
    }

    return this.signer.verify(
      body as Record<string, unknown>,
      { signature, timestamp, webhookId, version },
      this.config.secret,
      this.config.toleranceMs || 300000,
    );
  }

  middleware(): (req: any, res: any, next: Function) => void {
    return (req, res, next) => {
      if (!this.verify(req.body, req.headers)) {
        return res.status(401).json({
          error: 'Invalid webhook signature',
          code: 'SIGNATURE_MISMATCH',
        });
      }
      next();
    };
  }

  middlewareAsync(): (req: any, res: any) => Promise<void> {
    return async (req, res) => {
      if (!this.verify(req.body, req.headers)) {
        res.status(401).json({
          error: 'Invalid webhook signature',
          code: 'SIGNATURE_MISMATCH',
        });
        return;
      }
    };
  }

  private getHeader(
    headers: Record<string, string | string[] | undefined>,
    name: string,
  ): string | undefined {
    const value = headers[name] || headers[name.toLowerCase()];
    return Array.isArray(value) ? value[0] : value;
  }
}

class WebhookEventParser {
  parse<T>(body: Record<string, unknown>): WebhookEventPayload<T> {
    this.validateSchema(body);

    return {
      id: body.id as string,
      type: body.type as WebhookEventType,
      payload: body.payload as T,
      idempotencyKey: body.idempotencyKey as string,
      timestamp: body.timestamp as string,
      tenantId: body.tenantId as string,
    };
  }

  parseCallCompleted(body: Record<string, unknown>): WebhookEventPayload<CallCompletedPayload> {
    return this.parse<CallCompletedPayload>(body);
  }

  isCallCompletedEvent(event: WebhookEventPayload): event is WebhookEventPayload<CallCompletedPayload> {
    return event.type === 'call.completed';
  }

  private validateSchema(body: Record<string, unknown>): void {
    const required = ['id', 'type', 'payload', 'idempotencyKey', 'timestamp', 'tenantId'];
    for (const field of required) {
      if (!body[field]) {
        throw new WebhookError(`Missing required field: ${field}`);
      }
    }
  }
}

class WebhookError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'WebhookError';
  }
}

// Convenience factory
function createWebhookHandler(config: WebhookSDKConfig) {
  return {
    verifier: new WebhookVerifier(config),
    parser: new WebhookEventParser(),
    retry: new RetryHandler(),
  };
}

// Example consumer usage
/*
import { createWebhookHandler, CallCompletedPayload } from '@voiceagent/webhooks';
import express from 'express';

const app = express();
const webhook = createWebhookHandler({
  secret: process.env.WEBHOOK_SECRET!,
});

app.post('/webhooks/voiceagent', express.json(), (req, res) => {
  try {
    // Verify signature
    webhook.verifier.verify(req.body, req.headers);

    // Parse event
    const event = webhook.parser.parse<CallCompletedPayload>(req.body);

    // Handle by type
    switch (event.type) {
      case 'call.completed':
        console.log(`Call ${event.payload.callId} completed in ${event.payload.duration}s`);
        break;
      case 'agent.created':
        console.log(`Agent created: ${event.payload}`);
        break;
    }

    // Acknowledge immediately
    res.status(200).json({ received: true });
  } catch (error) {
    if (error instanceof WebhookError) {
      res.status(401).json({ error: error.message });
    } else {
      res.status(500).json({ error: 'Internal server error' });
    }
  }
});
*/
```

## Integration Points

- **npm Registry**: Published as @voiceagent/webhooks
- **Documentation**: SDK usage examples in developer portal
- **TypeScript Definitions**: Auto-generated from event schemas

## Production Considerations

- **Versioning**: SDK major version matches webhook API version
- **Error Handling**: SDK throws typed errors with actionable messages
- **Bundle Size**: Keep under 10KB gzipped — tree-shakeable
- **Backward Compatibility**: Type changes additive only, no breaking changes

## Open-Source Tools

- **tsup**: TypeScript bundling for npm publishing
- **JSDoc**: Inline documentation generation
