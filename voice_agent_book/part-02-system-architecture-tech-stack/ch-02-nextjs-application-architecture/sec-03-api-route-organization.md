# Section 03: API Route Organization

## Route Handler Architecture

Next.js API routes serve as the platform's REST API layer. They are organized by domain, versioned via URL paths, and follow consistent patterns for authentication, validation, error handling, and response formatting.

```
app/api/
├── v1/
│   ├── agents/
│   │   ├── route.ts              # GET (list), POST (create)
│   │   └── [id]/
│   │       ├── route.ts          # GET, PATCH, DELETE
│   │       ├── deploy/
│   │       │   └── route.ts      # POST /agents/:id/deploy
│   │       ├── versions/
│   │       │   ├── route.ts      # GET /agents/:id/versions
│   │       │   └── [versionId]/
│   │       │       └── route.ts  # GET /agents/:id/versions/:versionId
│   │       └── analytics/
│   │           └── route.ts      # GET /agents/:id/analytics
│   │
│   ├── calls/
│   │   ├── route.ts              # GET (list), POST (initiate)
│   │   └── [id]/
│   │       ├── route.ts          # GET, PATCH (update state)
│   │       ├── events/
│   │       │   └── route.ts      # GET /calls/:id/events
│   │       ├── transcript/
│   │       │   └── route.ts      # GET /calls/:id/transcript
│   │       └── recording/
│   │           └── route.ts      # GET /calls/:id/recording
│   │
│   ├── campaigns/
│   │   ├── route.ts
│   │   └── [id]/
│   │       ├── route.ts
│   │       ├── start/
│   │       │   └── route.ts
│   │       ├── pause/
│   │       │   └── route.ts
│   │       ├── contacts/
│   │       │   ├── route.ts
│   │       │   └── [contactId]/
│   │       │       └── route.ts
│   │       └── analytics/
│   │           └── route.ts
│   │
│   ├── voice/
│   │   ├── stt/
│   │   │   └── route.ts          # POST /voice/stt
│   │   ├── tts/
│   │   │   └── route.ts          # POST /voice/tts
│   │   └── voices/
│   │       └── route.ts          # GET /voice/voices (list available)
│   │
│   ├── billing/
│   │   ├── subscription/
│   │   │   └── route.ts          # GET, PATCH /billing/subscription
│   │   ├── usage/
│   │   │   └── route.ts          # GET /billing/usage
│   │   └── invoices/
│   │       ├── route.ts          # GET /billing/invoices
│   │       └── [id]/
│   │           └── route.ts      # GET /billing/invoices/:id
│   │
│   ├── auth/
│   │   ├── login/
│   │   │   └── route.ts          # POST /auth/login
│   │   ├── logout/
│   │   │   └── route.ts          # POST /auth/logout
│   │   ├── register/
│   │   │   └── route.ts          # POST /auth/register
│   │   ├── verify/
│   │   │   └── route.ts          # POST /auth/verify
│   │   └── password/
│   │       ├── forgot/
│   │       │   └── route.ts
│   │       └── reset/
│   │           └── route.ts
│   │
│   ├── webhooks/
│   │   ├── route.ts              # GET (list webhooks), POST (create)
│   │   └── [id]/
│   │       ├── route.ts          # GET, PATCH, DELETE
│   │       └── deliveries/
│   │           └── route.ts      # GET /webhooks/:id/deliveries
│   │
│   └── tenants/
│       └── [id]/
│           └── route.ts          # GET, PATCH /tenants/:id
│
└── webhooks/                      # External webhook receivers
    ├── stripe/
    │   └── route.ts              # POST /webhooks/stripe
    ├── twilio/
    │   └── route.ts              # POST /webhooks/twilio
    └── sendgrid/
        └── route.ts              # POST /webhooks/sendgrid
```

## Route Handler Pattern

Every API route follows a consistent pattern:

```typescript
// app/api/v1/agents/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from '@/lib/auth'
import { requireAuth } from '@/lib/api/require-auth'
import { validateRequest } from '@/lib/api/validate-request'
import { handleApiError } from '@/lib/api/handle-error'
import { apiResponse } from '@/lib/api/response'
import { prisma } from '@/lib/db'
import { z } from 'zod'

// -- Schemas --
const updateAgentSchema = z.object({
  name: z.string().min(1).max(100).optional(),
  description: z.string().max(500).optional(),
  voiceId: z.string().uuid().optional(),
  promptId: z.string().uuid().optional(),
  language: z.string().length(5).optional(),
  isActive: z.boolean().optional(),
  config: z.object({
    temperature: z.number().min(0).max(2).optional(),
    maxTokens: z.number().min(100).max(4096).optional(),
    bargeIn: z.boolean().optional(),
    endCallAfterSilence: z.number().min(1).max(60).optional()
  }).optional()
})

// -- GET /api/v1/agents/:id --
export async function GET(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const session = await requireAuth(req)

    const agent = await prisma.agent.findUnique({
      where: { id: params.id, tenantId: session.tenantId },
      include: {
        voice: true,
        prompt: true,
        version: {
          orderBy: { createdAt: 'desc' },
          take: 1
        }
      }
    })

    if (!agent) {
      return NextResponse.json(
        { error: { code: 'NOT_FOUND', message: 'Agent not found' } },
        { status: 404 }
      )
    }

    return apiResponse(agent)
  } catch (error) {
    return handleApiError(error)
  }
}

// -- PATCH /api/v1/agents/:id --
export async function PATCH(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const session = await requireAuth(req)

    const body = await req.json()
    const data = validateRequest(updateAgentSchema, body)

    // Check agent exists and belongs to tenant
    const existing = await prisma.agent.findUnique({
      where: { id: params.id, tenantId: session.tenantId }
    })
    if (!existing) {
      return NextResponse.json(
        { error: { code: 'NOT_FOUND', message: 'Agent not found' } },
        { status: 404 }
      )
    }

    const agent = await prisma.agent.update({
      where: { id: params.id },
      data: {
        ...data,
        updatedBy: session.userId
      }
    })

    return apiResponse(agent)
  } catch (error) {
    return handleApiError(error)
  }
}

// -- DELETE /api/v1/agents/:id --
export async function DELETE(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const session = await requireAuth(req)

    // Soft delete — update status instead of removing
    await prisma.agent.update({
      where: { id: params.id, tenantId: session.tenantId },
      data: {
        status: 'deleted',
        deletedAt: new Date(),
        deletedBy: session.userId
      }
    })

    return apiResponse({ success: true })
  } catch (error) {
    return handleApiError(error)
  }
}
```

## Shared Middleware for API Routes

```typescript
// lib/api/require-auth.ts
import { getServerSession } from '@/lib/auth'
import { NextResponse } from 'next/server'
import { ApiError } from '@/lib/api/errors'

export async function requireAuth(req: Request) {
  const session = await getServerSession()
  if (!session) {
    throw new ApiError('UNAUTHORIZED', 'Authentication required', 401)
  }
  return session
}

// lib/api/validate-request.ts
import { ZodSchema } from 'zod'
import { ApiError } from '@/lib/api/errors'

export function validateRequest<T>(schema: ZodSchema<T>, data: unknown): T {
  const result = schema.safeParse(data)
  if (!result.success) {
    throw new ApiError(
      'VALIDATION_ERROR',
      'Invalid request data',
      400,
      result.error.flatten().fieldErrors
    )
  }
  return result.data
}

// lib/api/handle-error.ts
import { NextResponse } from 'next/server'
import { ApiError } from '@/lib/api/errors'
import { logger } from '@/lib/logger'

export function handleApiError(error: unknown) {
  if (error instanceof ApiError) {
    return NextResponse.json(
      {
        error: {
          code: error.code,
          message: error.message,
          details: error.details
        }
      },
      { status: error.status }
    )
  }

  logger.error({ err: error }, 'Unhandled API error')

  return NextResponse.json(
    {
      error: {
        code: 'INTERNAL_ERROR',
        message: 'An unexpected error occurred'
      }
    },
    { status: 500 }
  )
}

// lib/api/response.ts
import { NextResponse } from 'next/server'

export function apiResponse<T>(data: T, meta?: Record<string, unknown>) {
  return NextResponse.json(
    meta ? { data, meta } : { data },
    {
      headers: {
        'X-Request-Id': crypto.randomUUID()
      }
    }
  )
}
```

## Rate Limiting Middleware for API Routes

```typescript
// lib/api/rate-limit.ts
import { redis } from '@/lib/redis'
import { NextResponse } from 'next/server'

interface RateLimitConfig {
  limit: number
  window: number  // seconds
}

const tierLimits: Record<string, RateLimitConfig> = {
  free: { limit: 10, window: 60 },
  starter: { limit: 60, window: 60 },
  pro: { limit: 300, window: 60 },
  business: { limit: 1000, window: 60 },
  enterprise: { limit: 5000, window: 60 }
}

export async function checkRateLimit(
  tenantId: string,
  tier: string
): Promise<{ allowed: boolean; remaining: number; resetAt: number }> {
  const config = tierLimits[tier] ?? tierLimits.free
  const key = `ratelimit:${tenantId}:${Math.floor(Date.now() / 1000 / config.window)}`
  
  const current = await redis.incr(key)
  if (current === 1) {
    await redis.expire(key, config.window)
  }

  return {
    allowed: current <= config.limit,
    remaining: Math.max(0, config.limit - current),
    resetAt: Math.floor(Date.now() / 1000) + config.window
  }
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Versioning | URL-based (/api/v1/) | Clear, cacheable, easy to route |
| Route nesting | Domain-based (agents, calls, ...) | Mirrors resource hierarchy |
| Validation | Zod schemas per route | TypeScript inference, composable |
| Error handling | Centralized ApiError class | Consistent error format |
| Auth per route | requireAuth wrapper | Explicit, testable middleware |
| Response format | { data, meta? } envelope | Consistent, extensible |

## Integration Points

- **Part 07 (API Gateway Routing)** — Deep dive into versioning and routing
- **Part 10 (Integrations & API)** — External API consumers use these routes
- **Part 18 (Developer Tools)** — SDK generated from route definitions

## Production Considerations

- **Response Compression**: Enable gzip/brotli for API responses larger than 1KB
- **Caching**: Add Cache-Control headers for GET endpoints
- **Pagination**: All list endpoints support cursor-based pagination
- **Request IDs**: Every response includes X-Request-Id for debugging
- **Audit Logging**: All mutations logged with before/after state
- **OpenAPI Generation**: Auto-generate OpenAPI 3.1 spec from route handlers
