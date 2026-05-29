# Section 06: Request Validation

## Overview

Request validation is the first defense against malformed data entering the system. The Voice Agent API uses Zod schemas to define request shapes, validate inputs at the edge, and return detailed validation errors. Validation covers request bodies, query parameters, URL path parameters, and headers. Idempotency enforcement adds another layer, ensuring operations are processed exactly once.

## Architecture

```
Validation Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[HTTP Request] → [Body Parsing] → [Schema Validation] → [Type Coercion] → [Controller]
                                        │
                                   [Errors?] ──→ [ValidationError Response]
                                        │
                                   [Idempotency Check]
                                        │
                                   [Duplicate?] ──→ [Cached Response Returned]

Validation Layers:
  ┌──────────────────────────────┐
  │ Layer 1: Transport           │  → Content-Type check, JSON parse
  │ Layer 2: Schema              │  → Zod validation against schema
  │ Layer 3: Business            │  → Domain rules (e.g., agent limits)
  │ Layer 4: Idempotency         │  → Replay detection
  └──────────────────────────────┘
```

## Design Decisions

- **Zod Over Alternatives**: Zod provides TypeScript type inference from runtime schemas, eliminating type drift
- **Edge Validation**: Validation runs at the API gateway or middleware layer before business logic
- **Idempotency via Header**: Clients provide `Idempotency-Key` header for mutating requests; identical keys return cached responses
- **Coercion with Safety**: Query parameters are coerced to correct types; if coercion fails, a validation error is returned

## Implementation Approach

```typescript
import { z } from 'zod';

// Agent creation schema
const CreateAgentSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().max(500).optional(),
  voice: z.object({
    provider: z.enum(['elevenlabs', 'azure', 'google', 'amazon']),
    voiceId: z.string().min(1),
    speed: z.number().min(0.5).max(2.0).optional().default(1.0),
  }),
  model: z.object({
    provider: z.enum(['openai', 'anthropic', 'google']),
    model: z.string().min(1),
    temperature: z.number().min(0).max(2).optional().default(0.7),
    maxTokens: z.number().int().min(1).max(16384).optional().default(4096),
  }),
  greeting: z.string().max(1000).optional(),
  timezone: z.string().optional().default('UTC'),
});

type CreateAgentRequest = z.infer<typeof CreateAgentSchema>;

// Query parameter schema with coercion
const ListAgentsQuerySchema = z.object({
  cursor: z.string().optional(),
  limit: z.coerce.number().int().min(1).max(100).optional().default(20),
  status: z.enum(['active', 'paused', 'draft', 'archived']).optional(),
  query: z.string().max(200).optional(),
});

// Validation middleware factory
function validate(schema: z.ZodSchema, source: 'json' | 'query' | 'param' = 'json') {
  return async (c: Context, next: Next) => {
    let data: unknown;

    switch (source) {
      case 'json':
        data = await c.req.json();
        break;
      case 'query':
        data = c.req.query();
        break;
      case 'param':
        data = c.req.param();
        break;
    }

    const result = schema.safeParse(data);

    if (!result.success) {
      const details = result.error.issues.map(issue => ({
        field: issue.path.join('.'),
        code: issue.code.toUpperCase(),
        message: issue.message,
        constraints: issue.code === 'custom' ? { custom: issue.message } : undefined,
      }));

      throw new ValidationError(details);
    }

    c.set('validated', result.data);
    await next();
  };
}

// Idempotency middleware
async function idempotencyMiddleware(c: Context, next: Next) {
  const idempotencyKey = c.req.header('Idempotency-Key');

  if (c.req.method === 'POST' && !idempotencyKey) {
    throw new ApiErrorResponse(400, 'VALIDATION_ERROR',
      'Idempotency-Key header is required for POST requests');
  }

  if (idempotencyKey) {
    const existing = await idempotencyStore.get(idempotencyKey);

    if (existing) {
      // Replay detected — return cached response
      if (existing.requestBody !== await c.req.text()) {
        throw new ApiErrorResponse(422, 'IDEMPOTENCY_ERROR',
          'Idempotency key reused with different request body');
      }
      return c.json(existing.response, existing.statusCode);
    }

    // Store response after processing
    c.set('idempotencyKey', idempotencyKey);
    const originalJson = c.json.bind(c);
    c.json = async (body, status) => {
      await idempotencyStore.set(idempotencyKey, {
        requestBody: await c.req.text(),
        response: body,
        statusCode: status || 200,
      }, { ttl: 86400 }); // 24 hour TTL
      return originalJson(body, status);
    };
  }

  await next();
}

// Route usage
app.post('/v1/agents',
  validate(CreateAgentSchema),
  idempotencyMiddleware,
  agentsController.create
);
```

## Integration Points

- **SDK Validation**: SDKs perform client-side validation with identical Zod schemas for early feedback
- **API Gateway**: Schema validation at gateway rejects invalid requests before they reach services
- **Database Layer**: Validated data passes directly to ORM/query builder without additional sanitization

## Production Considerations

- **Schema Versioning**: Request schemas are versioned alongside API versions; breaking changes require a new API version
- **Validation Performance**: Zod is benchmarked at ~1μs per validation; for high-throughput endpoints, consider caching compiled schemas
- **Error Detail Size**: Validation details are truncated to prevent excessively large error responses (max 20 detail items)

## Open-Source Tools

- **Zod**: TypeScript-first schema validation with zero dependencies
- **Hono Zod OpenAPI**: OpenAPI schema generation from Zod schemas
