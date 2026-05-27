# Section 06: Action Execution Engine

## Overview

The Action Execution Engine is the component that translates automation connector action requests (e.g., "Send SMS", "Create Contact", "Get Analytics") into platform API operations and returns structured responses. When an automation workflow triggers an action, the execution engine authenticates the request, validates input parameters against the action schema, executes the corresponding platform operation, formats the response, and handles errors gracefully.

The engine serves as the bridge between the various automation platforms (Zapier, Make, n8n, Workato) and the platform's internal services. It normalizes the different action invocation patterns — Zapier sends action requests via its SDK, Make calls REST endpoints, n8n executes node methods, Workato runs Ruby lambdas — and maps them to a unified action execution pipeline. The engine also handles action discoverability (providing input/output schemas for the automation platform's editor UI), idempotency (preventing duplicate action execution), and rate limit management.

## Architecture

```
                Action Execution Engine

   Automation Connector → Action Engine → Platform API
                              |
   +----------------------------------------------------------+
   |             Action Execution Pipeline                    |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Auth Validator   |  | Schema Validator  |            |
   |  | • API key check  |  | • Input validation|            |
   |  | • OAuth token    |  | • Type coercion   |            |
   |  | • Scope check    |  | • Required fields |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Action Router    |  | Rate Limiter      |             |
   |  | • Action →       |  | • Per-connector   |            |
   |  |   handler map    |  | • Per-action      |            |
   |  | • Version        |  | • Token bucket    |            |
   |  |   resolution     |  +-------------------+            |
   |  +------------------+                                    |
   |  +------------------+  +-------------------+            |
   |  | Response         |  | Error Handler     |             |
   |  | Formatter        |  | • Error codes     |            |
   |  | • Platform-      |  | • Retry advice    |            |
   |  |   specific       |  | • Human-readable  |            |
   |  | • Field mapping  |  | • Fallback values |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **Schema-driven action registry over hard-coded dispatch:** Actions are registered in a schema-driven registry where each action defines its input schema (expected parameters, types, required/optional), output schema (response format), execution handler (a function reference), and rate limit parameters. New actions can be added by registering a new entry in the registry without modifying the engine code. The registry is loaded at startup and can be refreshed without restart. Trade-off: schema-driven registration requires maintaining action definitions separate from code but enables dynamic action discovery and auto-generation of connector manifests.

- **Platform-specific response formatting over one-size-fits-all response:** Each automation platform expects responses in a specific format. Zapier expects a plain object (or array of objects for list operations). Make expects the full envelope with status and data. n8n expects `{ json: data }` format. Workato expects the data object directly. The engine applies a response formatter based on the `X-Integration-Platform` header or URL prefix. Trade-off: multi-format responses increase code complexity but eliminate the need for platform-specific action endpoints.

- **Idempotency key-based deduplication over at-most-once execution:** Actions can be retried by automation platforms (e.g., on network failure). The engine supports idempotency keys — the caller includes an `X-Idempotency-Key` header, and the engine returns the cached response for duplicate keys within a 24-hour window. This is especially important for billing-related actions (Send SMS costs money) and data-creating actions (Create Contact should not create duplicates). Trade-off: idempotency caching adds storage overhead but prevents duplicate charges and data creation.

## Implementation Approach

```
interface ActionDefinition {
  name: string;
  description: string;
  inputSchema: z.ZodSchema;
  outputSchema: z.ZodSchema;
  handler: (params: any, context: ActionContext) => Promise<any>;
  rateLimit: { maxPerSecond: number; burstSize: number };
  idempotent: boolean;
  timeout: number; // ms
}

interface ActionContext {
  tenantId: string;
  apiKey: string;
  platform: 'zapier' | 'make' | 'n8n' | 'workato';
  requestId: string;
  idempotencyKey?: string;
}

class ActionExecutionEngine {
  private actions = new Map<string, ActionDefinition>();
  private idempotencyCache: IdempotencyCache;
  private rateLimiter: RateLimiter;

  registerAction(name: string, definition: ActionDefinition) {
    this.actions.set(name, definition);
  }

  async executeAction(
    actionName: string,
    params: Record<string, any>,
    context: ActionContext
  ): Promise<ActionResult> {
    const action = this.actions.get(actionName);
    if (!action) {
      return { success: false, statusCode: 404, error: { code: 'ACTION_NOT_FOUND', message: `Action ${actionName} not found` } };
    }

    // 1. Check idempotency
    if (action.idempotent && context.idempotencyKey) {
      const cached = await this.idempotencyCache.get(context.idempotencyKey);
      if (cached) {
        logger.info('Idempotent action, returning cached result', { actionName, key: context.idempotencyKey });
        return cached;
      }
    }

    // 2. Rate limit
    const allowed = await this.rateLimiter.check(`action:${actionName}:${context.tenantId}`, action.rateLimit);
    if (!allowed) {
      return {
        success: false,
        statusCode: 429,
        error: { code: 'RATE_LIMITED', message: 'Action rate limit exceeded. Retry after 1 second.' },
      };
    }

    // 3. Validate input
    const parsed = action.inputSchema.safeParse(params);
    if (!parsed.success) {
      return {
        success: false,
        statusCode: 400,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Input validation failed',
          details: parsed.error.issues.map(i => ({ field: i.path.join('.'), message: i.message })),
        },
      };
    }

    // 4. Execute with timeout
    const timeoutMs = action.timeout || 30000;
    try {
      const result = await withTimeout(
        action.handler(parsed.data, context),
        timeoutMs
      );

      const formatted = this.formatResponse(result, context.platform);
      const actionResult = { success: true, statusCode: 200, data: formatted };

      // Cache for idempotency
      if (action.idempotent && context.idempotencyKey) {
        await this.idempotencyCache.set(context.idempotencyKey, actionResult, 86400);
      }

      return actionResult;
    } catch (error: any) {
      logger.error('Action execution failed', { actionName, error: error.message, requestId: context.requestId });

      return {
        success: false,
        statusCode: error.statusCode || 500,
        error: {
          code: error.code || 'EXECUTION_ERROR',
          message: error.message || 'Action execution failed',
          retryable: error.retryable !== false,
        },
      };
    }
  }

  private formatResponse(data: any, platform: string): any {
    switch (platform) {
      case 'zapier':
        return Array.isArray(data) ? data : [data];
      case 'make':
        return { result: data };
      case 'n8n':
        return { json: data };
      case 'workato':
        return data;
      default:
        return data;
    }
  }
}

// Action registration example
const engine = new ActionExecutionEngine();

engine.registerAction('send_sms', {
  name: 'send_sms',
  description: 'Send an SMS message',
  inputSchema: z.object({
    to: z.string().regex(/^\+[1-9]\d{1,14}$/, 'Invalid phone number'),
    text: z.string().min(1).max(1600),
    from: z.string().regex(/^\+[1-9]\d{1,14}$/).optional(),
  }),
  outputSchema: z.object({
    id: z.string(),
    status: z.string(),
    to: z.string(),
    sent_at: z.string(),
  }),
  handler: async (params, ctx) => {
    const message = await messageService.sendSMS({
      to: params.to,
      text: params.text,
      from: params.from,
      tenantId: ctx.tenantId,
    });
    return {
      id: message.id,
      status: message.status,
      to: message.to,
      sent_at: message.sentAt.toISOString(),
    };
  },
  rateLimit: { maxPerSecond: 10, burstSize: 20 },
  idempotent: true,
  timeout: 15000,
});

engine.registerAction('create_contact', {
  name: 'create_contact',
  description: 'Create a new contact',
  inputSchema: z.object({
    name: z.string().min(1),
    email: z.string().email().optional(),
    phone: z.string().regex(/^\+[1-9]\d{1,14}$/).optional(),
    tags: z.array(z.string()).optional(),
    custom_fields: z.record(z.any()).optional(),
  }),
  outputSchema: z.object({
    id: z.string(),
    name: z.string(),
    created_at: z.string(),
  }),
  handler: async (params, ctx) => {
    const contact = await contactService.createContact({
      ...params,
      tenantId: ctx.tenantId,
    });
    return {
      id: contact.id,
      name: contact.name,
      created_at: contact.createdAt.toISOString(),
    };
  },
  rateLimit: { maxPerSecond: 30, burstSize: 50 },
  idempotent: true,
  timeout: 10000,
});
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Zod (MIT) | Validation | Input/output schema validation |
| ioredis (MIT) | Redis | Idempotency cache |
| Bottleneck (MIT) | Node.js | Rate limiting |

## Production Considerations

**Scaling:** Action execution is synchronous from the perspective of the automation platform (the platform waits for the HTTP response). Ensure action timeouts match the automation platform's timeout expectations (Zapier: 30s, Make: 40s, n8n: configurable, Workato: 60s). Use connection pooling and database query optimization to minimize action execution time. For long-running actions, implement the "async action" pattern: accept the request, return an immediate acknowledgment with a "check status" URL, and let the automation platform poll for completion.

**Security:** Validate that the caller's API key has permission to execute the requested action. Some actions (Send SMS) have cost implications — enforce spending limits and alert on unusual usage. Never expose internal identifiers or system states in action responses. Log all action executions with the caller identity and params (excluding sensitive fields).

**Monitoring:** Track action execution count by action type, execution latency (p50/p95/p99), success/failure rates, idempotency cache hit rate, rate limit hit count, and validation error distribution. Alert on action failure rates exceeding 5%, execution latency exceeding 75% of the timeout, and idempotency cache miss rate on retries.
