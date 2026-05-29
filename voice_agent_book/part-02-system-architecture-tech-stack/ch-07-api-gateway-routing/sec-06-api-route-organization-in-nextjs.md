# Section 06: API Route Organization in Next.js

## Route Group Structure

API routes in Next.js are organized by **domain** using route groups, with shared middleware, error boundaries, and validation applied at the group level.

```
┌─────────────────────────────────────────────────────────────────────┐
│               NEXT.JS API ROUTE ORGANIZATION                        │
│                                                                     │
│  src/app/api/                                                       │
│  ├── (api-layout)/                   ← Shared API layout            │
│  │   ├── _middleware.ts              ← Global API middleware        │
│  │   ├── _error-boundary.ts          ← Global error handler         │
│  │   └── _rate-limit.ts             ← Global rate limit config     │
│  │                                                                   │
│  ├── (api-layout)/v1/               ← API Version 1                │
│  │   ├── agents/                    ← Agent domain                  │
│  │   │   ├── route.ts               ← GET, POST /api/v1/agents     │
│  │   │   ├── [id]/                                                  │
│  │   │   │   ├── route.ts           ← GET, PUT, DELETE /api/v1/... │
│  │   │   │   └── versions/                                          │
│  │   │   │       └── route.ts       ← GET /api/v1/agents/:id/vers  │
│  │   │   └── _validators.ts         ← Agent-specific Zod schemas   │
│  │   │                                                              │
│  │   ├── calls/                     ← Call domain                   │
│  │   │   ├── route.ts               ← GET, POST /api/v1/calls      │
│  │   │   ├── [id]/                                                  │
│  │   │   │   ├── route.ts           ← GET /api/v1/calls/:id        │
│  │   │   │   ├── status                                               │
│  │   │   │   │   └── route.ts       ← PATCH /api/v1/calls/:id/stat │
│  │   │   │   └── transcript                                         │
│  │   │   │       └── route.ts       ← GET /api/v1/calls/:id/trans  │
│  │   │   └── _validators.ts                                         │
│  │   │                                                              │
│  │   ├── campaigns/                 ← Campaign domain               │
│  │   ├── analytics/                 ← Analytics domain              │
│  │   ├── billing/                   ← Billing domain                │
│  │   └── tenants/                   ← Tenant configuration          │
│  │                                                                   │
│  ├── (api-layout)/v2/               ← API Version 2 (beta)         │
│  │   └── ...                        ← Same structure, evolved      │
│  │                                                                   │
│  └── webhooks/                      ← External webhooks (no auth)  │
│      ├── stripe/                                                     │
│      │   └── route.ts               ← POST /api/webhooks/stripe    │
│      └── twilio/                                                     │
│          └── route.ts               ← POST /api/webhooks/twilio    │
└─────────────────────────────────────────────────────────────────────┘
```

## Route Handler Pattern

```typescript
// src/app/api/(api-layout)/v1/agents/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { agentService } from '@/lib/services/agent-service';
import { requireAuth } from '@/lib/api/middleware/auth';
import { validate } from '@/lib/api/middleware/validate';
import { apiHandler } from '@/lib/api/api-handler';

const CreateAgentSchema = z.object({
  name: z.string().min(1).max(100),
  voice: z.enum(['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']),
  temperature: z.number().min(0).max(2).default(0.7),
  promptTemplate: z.string().min(10).max(10000),
});

// apiHandler wraps error handling, logging, and response formatting
export const GET = apiHandler(async (request: NextRequest) => {
  const { tenantId } = await requireAuth(request);
  const agents = await agentService.listAgents(tenantId);
  return NextResponse.json(agents);
});

export const POST = apiHandler(async (request: NextRequest) => {
  const { tenantId, userId } = await requireAuth(request);
  const body = await validate(request, CreateAgentSchema);
  const agent = await agentService.createAgent({ ...body, tenantId, createdBy: userId });
  return NextResponse.json(agent, { status: 201 });
});
```

## Shared Middleware

```typescript
// src/app/api/(api-layout)/_middleware.ts
export async function middleware(request: NextRequest) {
  // 1. CORS preflight
  if (request.method === 'OPTIONS') {
    return handleCORS();
  }

  // 2. Rate limiting
  const rateLimitResult = await checkRateLimit(request);
  if (!rateLimitResult.allowed) {
    return rateLimitExceeded(rateLimitResult);
  }

  // 3. Authentication
  const authResult = await authenticateRequest(request);
  if (!authResult.authenticated && requiresAuth(request.nextUrl.pathname)) {
    return formatError('unauthorized', 'Authentication required', 401);
  }

  // 4. Attach context to request
  const requestWithContext = attachContext(request, authResult);

  return NextResponse.next({ request: requestWithContext });
}

export const config = {
  matcher: '/api/:path*',
};
```

## Error Boundaries

```typescript
// src/app/api/(api-layout)/_error-boundary.ts
// Wraps every route handler to catch and format errors consistently

export async function apiHandler<T>(
  handler: (request: NextRequest, context: { params: Record<string, string> }) => Promise<NextResponse<T>>
) {
  return async (request: NextRequest, { params }: { params: Record<string, string> }) => {
    const requestId = crypto.randomUUID();
    const startTime = Date.now();

    try {
      const response = await handler(request, { params });
      response.headers.set('X-Request-Id', requestId);

      // Log request
      logApiRequest({
        method: request.method,
        path: request.nextUrl.pathname,
        status: response.status,
        duration: Date.now() - startTime,
        requestId,
      });

      return response;
    } catch (error) {
      // Log error
      logApiError({ error, requestId, path: request.nextUrl.pathname });

      if (error instanceof ZodError) {
        return formatValidationError(error, requestId);
      }

      if (error instanceof NotFoundError) {
        return formatError('not_found', error.message, 404, { requestId });
      }

      // Unknown error — return 500 in production
      return formatError('internal_error', 'An unexpected error occurred', 500, { requestId });
    }
  };
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Route organization | Domain-based route groups | Clear ownership, parallel development |
| Middleware scope | Route group level via (_middleware.ts) | Shared logic without duplication |
| Version segregation | Route groups per version | Clean separation, independent deployment |
| Handler pattern | Wrapper function (apiHandler) | DRY error handling, consistent response format |
| Validation location | In route handler | Close to usage, explicit per-endpoint |

## Integration Points

- **Ch 02 (Next.js Architecture)** — Route groups align with App Router conventions
- **Ch 05 (Microservices)** — API routes delegate to microservice clients
- **Ch 07 (API Gateway)** — Route organization mirrors gateway route table

## Production Considerations

- **File Naming**: `route.ts` for route handlers, `_*` prefix for private modules (middleware, validators)
- **Code Splitting**: Each route group is independently deployable
- **Testing**: Route handlers tested via `nextTestUtils` with mocked service layer
- **Rate Limiting by Route**: Expensive routes (voice synthesis, batch processing) have stricter limits
- **Documentation**: Route structure drives automatic OpenAPI spec generation
