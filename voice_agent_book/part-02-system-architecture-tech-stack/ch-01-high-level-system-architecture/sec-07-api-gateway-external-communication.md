# Section 07: API Gateway & External Communication

## Gateway Architecture

The API Gateway acts as the **single entry point** for all external traffic — REST API calls from third-party developers, WebSocket connections for real-time events, and webhook deliveries for async notifications. It handles cross-cutting concerns so individual services don't have to.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     API GATEWAY & EXTERNAL COMMUNICATION                │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐     │
│  │                     EXTERNAL CLIENTS                            │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │     │
│  │  │  SDK     │  │  API     │  │  Webhook │  │  Dashboard │      │     │
│  │  │  Client  │  │  Direct  │  │  Receiver│  │  (Browser)│      │     │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │     │
│  └───────┼──────────────┼──────────────┼──────────────┼───────────┘     │
│          │              │              │              │                 │
│  ┌───────┴──────────────┴──────────────┴──────────────┴───────────┐     │
│  │                     API GATEWAY (Next.js Edge/Middleware)        │     │
│  │                                                                  │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │     │
│  │  │   TLS    │  │   Auth   │  │   Rate   │  │   Route  │        │     │
│  │  │  Term.   │  │  Verify  │  │  Limiter │  │  Resolver│        │     │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │     │
│  │                                                                  │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │     │
│  │  │  Request │  │  API     │  │  CORS    │  │  Logging │        │     │
│  │  │  Transf. │  │  Version │  │  Handler │  │  Audit   │        │     │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │     │
│  └─────────────────────────────────────────────────────────────────┘     │
│          │              │              │                                 │
│  ┌───────┼──────────────┼──────────────┼───────────────────────────┐     │
│  │       │              │              │                           │     │
│  │  ┌────┴────┐   ┌────┴────┐   ┌─────┴─────┐                    │     │
│  │  │  REST   │   │WebSocket│   │  Webhook  │                    │     │
│  │  │  Routes │   │  Server │   │  Dispatcher│                   │     │
│  │  └────┬────┘   └────┬────┘   └─────┬─────┘                    │     │
│  │       │              │              │                           │     │
│  │  ┌────┴──────────────┴──────────────┴─────────────────────┐    │     │
│  │  │                 MICROSERVICES                          │    │     │
│  │  │  Agent │ Call │ Voice │ AI │ Campaign│ Billing │ Auth  │    │     │
│  │  └────────────────────────────────────────────────────────┘    │     │
│  └────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
```

## REST API Gateway

The REST API gateway (implemented via Next.js API routes) handles all synchronous HTTP requests:

```typescript
// API Route Handler — app/api/v1/calls/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { rateLimiter } from '@/lib/rate-limiter'
import { authenticate } from '@/lib/auth'
import { validateSchema } from '@/lib/validation'
import { callService } from '@/services/call-service'
import { z } from 'zod'

const listCallsSchema = z.object({
  status: z.enum(['active', 'completed', 'failed']).optional(),
  agentId: z.string().uuid().optional(),
  limit: z.coerce.number().min(1).max(100).default(20),
  offset: z.coerce.number().min(0).default(0),
  from: z.string().datetime().optional(),
  to: z.string().datetime().optional()
})

export async function GET(request: NextRequest) {
  // 1. Authentication
  const auth = await authenticate(request)
  if (!auth.authenticated) {
    return NextResponse.json(
      { error: { code: 'UNAUTHORIZED', message: 'Invalid API key' } },
      { status: 401 }
    )
  }

  // 2. Rate limiting
  const rateLimitResult = await rateLimiter.check(auth.tenantId, 'calls:read')
  if (!rateLimitResult.allowed) {
    return NextResponse.json(
      { error: { code: 'RATE_LIMITED', message: 'Too many requests' } },
      { 
        status: 429,
        headers: {
          'X-RateLimit-Limit': String(rateLimitResult.limit),
          'X-RateLimit-Remaining': '0',
          'X-RateLimit-Reset': String(rateLimitResult.resetAt)
        }
      }
    )
  }

  // 3. Input validation
  const params = Object.fromEntries(request.nextUrl.searchParams)
  const parsed = listCallsSchema.safeParse(params)
  if (!parsed.success) {
    return NextResponse.json(
      { 
        error: { 
          code: 'VALIDATION_ERROR', 
          message: 'Invalid parameters',
          details: parsed.error.flatten().fieldErrors
        }
      },
      { status: 400 }
    )
  }

  // 4. Service call
  const result = await callService.listCalls({
    tenantId: auth.tenantId,
    ...parsed.data
  })

  // 5. Response with envelope
  return NextResponse.json({
    data: result.calls,
    meta: {
      total: result.total,
      limit: parsed.data.limit,
      offset: parsed.data.offset,
      hasMore: result.offset + result.limit < result.total
    }
  })
}
```

## WebSocket Server

The WebSocket server provides real-time communication between the platform and client applications:

```typescript
// WebSocket server setup (Socket.IO)
import { Server as HTTPServer } from 'http'
import { Server as SocketIOServer } from 'socket.io'
import { authenticate as authMiddleware } from '@/lib/auth'
import { rateLimiter } from '@/lib/rate-limiter'

export function createWebSocketServer(httpServer: HTTPServer) {
  const io = new SocketIOServer(httpServer, {
    cors: {
      origin: process.env.CORS_ORIGINS?.split(',') ?? '*',
      methods: ['GET', 'POST']
    },
    // Redis adapter for horizontal scaling
    adapter: createRedisAdapter(redisClient),
    // Connection options
    pingInterval: 25000,
    pingTimeout: 20000,
    transports: ['websocket', 'polling']
  })

  // Authentication middleware
  io.use(async (socket, next) => {
    try {
      const token = socket.handshake.auth.token
        ?? socket.handshake.query.token
      const auth = await authMiddleware(token as string)
      if (!auth.authenticated) {
        return next(new Error('Authentication failed'))
      }
      socket.data.tenantId = auth.tenantId
      socket.data.userId = auth.userId
      next()
    } catch (err) {
      next(new Error('Authentication failed'))
    }
  })

  // Connection handler
  io.on('connection', (socket) => {
    const { tenantId, userId } = socket.data
    logger.info({ tenantId, userId, id: socket.id }, 'WebSocket connected')

    // Join tenant room for scoped events
    socket.join(`tenant:${tenantId}`)

    // Subscribe to specific resources
    socket.on('subscribe:calls', (callIds: string[]) => {
      callIds.forEach(id => socket.join(`call:${id}`))
    })

    socket.on('subscribe:agent', (agentId: string) => {
      socket.join(`agent:${agentId}`)
    })

    socket.on('disconnect', () => {
      logger.info({ tenantId, userId, id: socket.id }, 'WebSocket disconnected')
    })
  })

  return io
}
```

## Webhook Dispatcher

Webhook delivery for event notifications to third-party services:

```typescript
interface WebhookEndpoint {
  id: string
  tenantId: string
  url: string
  secret: string
  events: string[]           // Which events to subscribe to
  retryConfig: {
    maxRetries: number       // Default: 3
    backoffMs: number        // Exponential backoff base
  }
  headers?: Record<string, string>
  status: 'active' | 'paused' | 'disabled'
}

interface WebhookDelivery {
  id: string
  endpointId: string
  event: string
  payload: unknown
  status: 'pending' | 'delivered' | 'failed' | 'retrying'
  attempts: Array<{
    timestamp: Date
    statusCode: number
    responseBody: string
    duration: number
  }>
  createdAt: Date
}

// Webhook dispatch via BullMQ
import { Queue, Worker } from 'bullmq'

const webhookQueue = new Queue('webhook-delivery', {
  connection: redisClient
})

async function dispatchWebhook(
  endpoint: WebhookEndpoint,
  event: string,
  payload: unknown
): Promise<void> {
  const signature = crypto
    .createHmac('sha256', endpoint.secret)
    .update(JSON.stringify(payload))
    .digest('hex')

  await webhookQueue.add(
    'deliver',
    {
      endpointId: endpoint.id,
      url: endpoint.url,
      event,
      payload,
      headers: {
        'Content-Type': 'application/json',
        'X-Webhook-Signature': signature,
        'X-Webhook-Event': event,
        'X-Webhook-Timestamp': Date.now().toString(),
        ...endpoint.headers
      }
    },
    {
      attempts: endpoint.retryConfig.maxRetries,
      backoff: {
        type: 'exponential',
        delay: endpoint.retryConfig.backoffMs
      }
    }
  )
}

// Webhook worker
const webhookWorker = new Worker('webhook-delivery', async (job) => {
  const { url, payload, headers } = job.data
  const response = await fetch(url, {
    method: 'POST',
    headers,
    body: JSON.stringify(payload),
    // Timeout after 10 seconds
    signal: AbortSignal.timeout(10000)
  })

  if (!response.ok) {
    throw new Error(`Webhook delivery failed: ${response.status}`)
  }
}, { connection: redisClient })
```

## API Response Envelope

All API responses follow a consistent envelope:

```typescript
interface APIResponse<T> {
  data: T
  meta?: {
    total?: number
    limit?: number
    offset?: number
    hasMore?: boolean
  }
}

interface APIError {
  error: {
    code: string           // Machine-readable code
    message: string        // Human-readable message
    details?: unknown      // Validation errors, etc.
    requestId?: string     // For debugging
  }
}

// Standard error codes
const ErrorCodes = {
  UNAUTHORIZED: 'UNAUTHORIZED',
  FORBIDDEN: 'FORBIDDEN',
  NOT_FOUND: 'NOT_FOUND',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  RATE_LIMITED: 'RATE_LIMITED',
  CONFLICT: 'CONFLICT',
  INTERNAL_ERROR: 'INTERNAL_ERROR',
  SERVICE_UNAVAILABLE: 'SERVICE_UNAVAILABLE',
  QUOTA_EXCEEDED: 'QUOTA_EXCEEDED'
} as const
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Gateway Implementation | Next.js API Routes + Middleware | Unified codebase, edge deployment |
| WebSocket Library | Socket.IO | Rooms, auto-reconnect, fallback transports |
| Webhook Queue | BullMQ (Redis) | Persistence, retries, rate limiting |
| API Versioning | URL-based (v1, v2) | Clear, cacheable, easy to route |
| Rate Limiting | Sliding window (Redis) | Fair, accurate, per-key tracking |

## Integration Points

- **Part 07 (API Gateway Routing)** — Deep dive into routing strategy
- **Part 10 (Integrations & API)** — External API design for developers
- **Part 18 (Developer Tools)** — SDK generation from OpenAPI specs
- **Part 20 (Notifications)** — Webhook delivery for notification events

## Production Considerations

- **Gateway Latency**: Gateway adds <5ms overhead per request; monitor and optimize
- **Webhook Guarantees**: At-least-once delivery with idempotency keys; deduplication window of 5 minutes
- **WebSocket Scaling**: Redis adapter for multi-instance deployment; connection draining on shutdown
- **Rate Limit Headers**: Always return `X-RateLimit-*` headers for client-side backoff
- **Audit Logging**: All API requests logged with request ID, tenant, endpoint, status, duration
- **DDoS Protection**: Rate limiting at the edge + WAF (Cloudflare/AWS Shield)
