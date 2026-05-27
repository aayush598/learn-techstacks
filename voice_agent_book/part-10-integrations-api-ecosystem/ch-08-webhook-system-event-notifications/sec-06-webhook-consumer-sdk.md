# Section 06: Webhook Consumer SDK

## Overview

The Webhook Consumer SDK provides client libraries that make it easy for external developers and partners to consume webhook events from the voice agent platform. The SDK handles signature verification, retry processing, event deserialization, and type-safe event handlers. It supports multiple programming languages (JavaScript/TypeScript, Python, Java, Go) and provides best-practice defaults for webhook consumption.

The SDK is published as open-source packages on npm, PyPI, Maven Central, and Go modules. It includes comprehensive documentation, example applications, and integration guides. The SDK reduces the barrier to entry for platform integrations — consumers do not need to implement HMAC verification, timestamp tolerance, or idempotency from scratch. They simply register event handlers and the SDK handles the infrastructure.

## Architecture

```
                 Webhook Consumer SDK

   Platform → HTTPS → Consumer App → SDK Handlers
                            |
   +----------------------------------------------------------+
   |              Consumer SDK Internals                      |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | HTTP Middleware  |  | Signature         |            |
   |  | • Express/Fastify|  | Verifier          |            |
   |  | • Flask/Django   |  | • HMAC-SHA256     |            |
   |  | • Spring Boot    |  | • Timestamp check |            |
   |  | • net/http       |  | • Replay protect  |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Event Router     |  | Payload Deserializ|            |
   |  | • Type routing   |  | • JSON parse      |            |
   |  | • Wildcard       |  | • Schema validate |            |
   |  | • Pattern match  |  | • TypeScript types|            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Idempotency      |  | Error Handling    |             |
   |  | • In-memory cache|  | • Structured      |            |
   |  | • Redis backend  |  | • Response codes  |            |
   |  | • 24h window     |  | • Retry advice    |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **Framework middleware over standalone server:** The SDK is designed as middleware for popular web frameworks (Express, Fastify, Flask, Spring), not as a standalone web server. This allows consumers to integrate webhook handling into their existing application server without provisioning additional infrastructure. The middleware captures the raw request body, verifies the signature, deserializes the event, and routes to the appropriate handler. Trade-off: middleware ties consumers to specific frameworks but avoids the operational overhead of a separate webhook server.

- **TypeScript-first with auto-generated type definitions:** The TypeScript SDK is the primary SDK from which type definitions for other languages are generated. Event schemas in the schema registry are used to auto-generate TypeScript interfaces, Python dataclasses, Java POJOs, and Go structs via code generation. This ensures type safety across all supported languages. Trade-off: code generation adds a build step and requires maintaining code generators but guarantees type consistency across languages.

- **Opt-in idempotency cache over mandatory dedup:** The SDK provides built-in idempotency handling through an optional in-memory cache (default TTL: 24 hours). When enabled, the SDK tracks processed event IDs and returns HTTP 200 OK for duplicate deliveries without invoking the handler. The cache can be backed by Redis for distributed deployments. Idempotency is optional because consumers may prefer to implement their own deduplication logic. Trade-off: optional idempotency means some consumers may process duplicates but provides flexibility for custom dedup strategies.

## Implementation Approach

```
// TypeScript SDK: Core Types
interface WebhookEvent<T = any> {
  id: string;
  type: string;
  version: string;
  tenantId: string;
  timestamp: string;
  idempotencyKey: string;
  data: T;
}

type EventHandler<T = any> = (event: WebhookEvent<T>) => Promise<void> | void;

interface WebhookHandlerConfig {
  secret: string;
  toleranceMs?: number;
  idempotency?: {
    backend: 'memory' | 'redis';
    ttlMs?: number;
    redisUrl?: string;
  };
  onError?: (error: WebhookError) => void;
}

// Express middleware
function createWebhookMiddleware(config: WebhookHandlerConfig) {
  const verifier = new SignatureVerifier({ secret: config.secret, toleranceMs: config.toleranceMs });
  const idempotencyCache = config.idempotency?.backend === 'redis'
    ? new RedisIdempotencyCache(config.idempotency.redisUrl!, config.idempotency.ttlMs)
    : new InMemoryIdempotencyCache(config.idempotency?.ttlMs);

  const handlers = new Map<string, EventHandler[]>();
  const wildcardHandlers: EventHandler[] = [];

  return {
    middleware: (req: Request, res: Response, next: NextFunction) => {
      const rawBody = (req as any).rawBody;
      if (!rawBody) {
        res.status(400).json({ error: 'Raw body required' });
        return;
      }

      // 1. Verify signature
      const signatureHeader = req.headers['x-webhook-signature'] as string;
      const verification = verifier.verify(rawBody.toString(), signatureHeader);
      if (!verification.valid) {
        res.status(401).json({ error: 'Verification failed', detail: verification.reason });
        return;
      }

      // 2. Parse event
      let event: WebhookEvent;
      try {
        event = JSON.parse(rawBody.toString());
      } catch {
        res.status(400).json({ error: 'Invalid JSON payload' });
        return;
      }

      // 3. Check idempotency
      if (config.idempotency) {
        const alreadyProcessed = idempotencyCache.check(event.idempotencyKey);
        if (alreadyProcessed) {
          res.status(200).json({ status: 'duplicate', eventId: event.id });
          return;
        }
        idempotencyCache.mark(event.idempotencyKey, event.id);
      }

      // 4. Route to handlers
      const matchedHandlers = [
        ...(handlers.get(event.type) || []),
        ...(handlers.get('*') || []),
        ...wildcardHandlers,
      ];

      if (matchedHandlers.length === 0) {
        res.status(200).json({ status: 'unhandled', eventType: event.type });
        return;
      }

      // 5. Execute handlers
      Promise.all(matchedHandlers.map(h => h(event)))
        .then(() => res.status(200).json({ status: 'ok', eventId: event.id }))
        .catch((err) => {
          if (config.onError) config.onError({ eventId: event.id, error: err, handler: 'unknown' });
          res.status(500).json({ status: 'error', message: 'Handler error' });
        });
    },

    on: (eventType: string, handler: EventHandler) => {
      const existing = handlers.get(eventType) || [];
      existing.push(handler);
      handlers.set(eventType, existing);
    },

    onAny: (handler: EventHandler) => {
      wildcardHandlers.push(handler);
    },
  };
}

// Python SDK example (for reference)
class WebhookConsumer:
    def __init__(self, secret: str, tolerance_ms: int = 300000):
        self.secret = secret
        self.tolerance_ms = tolerance_ms
        self.handlers: dict[str, list[Callable]] = {}

    def on(self, event_type: str):
        def decorator(func):
            if event_type not in self.handlers:
                self.handlers[event_type] = []
            self.handlers[event_type].append(func)
            return func
        return decorator

    def verify_and_route(self, body: bytes, headers: dict) -> tuple[int, dict]:
        # Verify HMAC signature
        signature = headers.get('X-Webhook-Signature', '')
        expected_sig = hmac.new(
            self.secret.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(expected_sig, signature.split('=')[-1]):
            return (401, {'error': 'Invalid signature'})

        event = json.loads(body)
        handlers = self.handlers.get(event['type'], [])
        for handler in handlers:
            handler(event)
        return (200, {'status': 'ok'})

// Usage example (TypeScript consumer app)
import { createWebhookMiddleware } from '@voiceagent/webhook-sdk';

const webhook = createWebhookMiddleware({
  secret: process.env.WEBHOOK_SECRET!,
  idempotency: { backend: 'memory' },
});

webhook.on('call.completed', async (event) => {
  console.log(`Call ${event.data.callSid} completed`);
  await updateCRM(event.data);
});

webhook.on('payment.succeeded', async (event) => {
  console.log(`Payment ${event.data.transactionId} succeeded`);
  await fulfillOrder(event.data);
});

app.post('/webhooks', webhook.middleware);
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Express (MIT) | Node.js | Reference middleware |
| Zod (MIT) | Validation | Event payload validation |
| TypeScript (Apache 2.0) | Language | Primary SDK language |

## Production Considerations

**Scaling:** The SDK is lightweight — middleware adds ~1ms overhead per request. The in-memory idempotency cache is bounded (default 10,000 entries, LRU eviction). For production deployments, consumers should configure a Redis-backed idempotency cache when running multiple application instances. The SDK does not manage webhook endpoint health — consumers should implement their own health check endpoints and monitoring.

**Security:** The SDK verifies signatures before deserializing events, preventing malformed payload attacks. Consumers should configure CORS if their webhook endpoint is publicly accessible. The SDK logs verification failures as warnings but never logs the secret or full signature. Consumers should rotate their webhook secrets periodically using the SDK's dual-key rotation support.

**Monitoring:** The SDK emits metric events (webhook.received, webhook.verified, webhook.processed, webhook.duplicate, webhook.failed) that consumers can instrument with their preferred monitoring system. Track event processing latency (enqueue to handler completion), handler error rate, duplicate event rate, and unhandled event types. Alert on high handler error rates and unexpected event types that no handler processes.
