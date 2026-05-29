# Section 05: Idempotency Keys

## Overview

Idempotency keys ensure that API requests can be safely retried without causing duplicate side effects. Clients include an `Idempotency-Key` header with a unique UUID for each mutating request. The API stores the response for completed requests keyed by the idempotency key, returning the cached response for identical keys. If the same key is used with a different request body, the API rejects the request.

## Architecture

```
Idempotency Flow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Client]                           [API Gateway]                    [Storage]
   │                                    │                              │
   │── POST /v1/agents                │                              │
   │   Idempotency-Key: uuid-123     │                              │
   │── ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ →│                              │
   │                                    │── Check idempotency:key:uuid-123 ─→│
   │                                    │←── Not found ──────────────────────│
   │                                    │                              │
   │                                    │── [Process Request] ─────→  │
   │                                    │                              │
   │                                    │── Store Response (ttl: 24h)──→│
   │                                    │←── Acknowledged ─────────────│
   │←── 201 Created ──────────────────│                              │
   │                                    │                              │
   │── [NETWORK ERROR — Retry]        │                              │
   │                                    │                              │
   │── POST /v1/agents                │                              │
   │   Idempotency-Key: uuid-123     │                              │
   │── ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ →│                              │
   │                                    │── Check idempotency:key:uuid-123 ─→│
   │                                    │←── Cached Response ───────────────│
   │←── 201 Created (cached) ────────│                              │

Error: Same key, different body:
  → 422 IDEMPOTENCY_ERROR: Idempotency key reused with different request body
```

## Design Decisions

- **Client-Generated Keys**: Clients generate unique UUIDs for each operation — the server never assigns idempotency keys
- **24-Hour Storage TTL**: Keys expire after 24 hours, allowing ample time for retry while bounding storage costs
- **Response Caching**: Entire response (status code, headers, body) is cached and returned verbatim on replay
- **Body Comparison**: Full request body comparison prevents accidental key reuse with different operations

## Implementation Approach

```typescript
// Idempotency storage interface
interface IdempotencyRecord {
  key: string;
  requestBody: string;
  requestMethod: string;
  requestPath: string;
  responseBody: string;
  responseStatus: number;
  responseHeaders: Record<string, string>;
  createdAt: Date;
}

interface IdempotencyStore {
  get(key: string): Promise<IdempotencyRecord | null>;
  set(key: string, record: IdempotencyRecord, ttl: number): Promise<void>;
}

// Redis implementation
class RedisIdempotencyStore implements IdempotencyStore {
  constructor(private redis: Redis) {}

  async get(key: string): Promise<IdempotencyRecord | null> {
    const data = await this.redis.get(`idempotency:${key}`);
    return data ? JSON.parse(data) : null;
  }

  async set(key: string, record: IdempotencyRecord, ttl: number): Promise<void> {
    await this.redis.setex(`idempotency:${key}`, ttl, JSON.stringify(record));
  }
}

// Idempotency middleware
interface IdempotencyConfig {
  store: IdempotencyStore;
  ttl: number; // seconds
  methods: string[]; // Methods that require idempotency keys
}

function idempotencyMiddleware(config: IdempotencyConfig) {
  return async (c: Context, next: Next) => {
    const method = c.req.method;

    // Only apply to configured methods
    if (!config.methods.includes(method)) {
      return next();
    }

    const idempotencyKey = c.req.header('Idempotency-Key');

    if (!idempotencyKey) {
      throw new ApiErrorResponse(400, 'VALIDATION_ERROR',
        `Idempotency-Key header is required for ${method} requests`);
    }

    // Validate UUID format
    if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(idempotencyKey)) {
      throw new ApiErrorResponse(400, 'VALIDATION_ERROR',
        'Idempotency-Key must be a valid UUID v4');
    }

    const existing = await config.store.get(idempotencyKey);

    if (existing) {
      // Verify same request body
      const requestBody = await c.req.text();

      if (requestBody !== existing.requestBody) {
        throw new ApiErrorResponse(422, 'IDEMPOTENCY_ERROR',
          'Idempotency key reused with different request body');
      }

      // Return cached response
      Object.entries(existing.responseHeaders).forEach(([k, v]) => c.header(k, v));
      c.status(existing.responseStatus);
      return c.body(existing.responseBody);
    }

    // Store the request body for later comparison
    const requestBody = await c.req.text();
    c.set('idempotencyKey', idempotencyKey);
    c.set('idempotencyStore', config.store);
    c.set('idempotencyTTL', config.ttl);
    c.set('idempotencyRequestBody', requestBody);

    // Intercept response to cache it
    const originalSend = c.body.bind(c);
    c.body = async (body, status?, headers?) => {
      const record: IdempotencyRecord = {
        key: idempotencyKey,
        requestBody: c.get('idempotencyRequestBody'),
        requestMethod: c.req.method,
        requestPath: c.req.path,
        responseBody: typeof body === 'string' ? body : JSON.stringify(body),
        responseStatus: status || 200,
        responseHeaders: Object.fromEntries(
          Object.entries(c.res.headers).filter(([k]) => k !== 'set-cookie')
        ),
        createdAt: new Date(),
      };

      await config.store.set(idempotencyKey, record, config.ttl);

      return originalSend(body, status, headers);
    };

    await next();
  };
}
```

## Integration Points

- **SDK**: Idempotency key generation built into all mutating SDK methods
- **Retry Logic**: SDK retry automatically regenerates idempotency keys for new attempts
- **Webhook Idempotency**: Webhook events include idempotency keys for receiver deduplication

## Production Considerations

- **Storage Bounds**: 24-hour TTL limits key storage to at most (requests/sec * 86400) keys; with 1M keys at ~1KB each = ~1GB
- **Persistence**: Idempotency store should be backed by Redis with persistence for crash recovery
- **Key Collision Risk**: UUID v4 provides 122 bits of entropy — collision probability is negligible
- **Monitoring**: Track idempotency key hit rate to detect retry patterns and potential replay attacks

## Open-Source Tools

- **Redis**: Fast key-value store for idempotency records with built-in TTL support
- **BullMQ**: Background job processing with idempotency support
