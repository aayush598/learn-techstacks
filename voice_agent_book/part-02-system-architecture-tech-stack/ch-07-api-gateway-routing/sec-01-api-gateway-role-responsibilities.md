# Section 01: API Gateway Role & Responsibilities

## Gateway Architecture

The API Gateway serves as the **single entry point** for all external traffic to the platform. It handles authentication, rate limiting, request routing, transformation, and observability before forwarding requests to internal microservices.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    API GATEWAY ARCHITECTURE                         │
│                                                                     │
│  External Clients                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Dashboard│  │  Mobile  │  │ 3rd Party│  │ WebSocket Client │   │
│  │ (Browser)│  │   App    │  │   API    │  │                  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────────┬─────────┘   │
│       │              │              │                 │             │
│  ┌────┼──────────────┼──────────────┼─────────────────┼─────────┐   │
│  │    ▼              ▼              ▼                 ▼         │   │
│  │               API GATEWAY                                     │   │
│  │  ┌─────────────────────────────────────────────────────────┐  │   │
│  │  │              Next.js API Routes + Middleware             │  │   │
│  │  │                                                         │  │   │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │  │   │
│  │  │  │   TLS    │ │   Auth   │ │   Rate   │ │  Route   │  │  │   │
│  │  │  │ Term.    │ │  Proxy   │ │  Limiter │ │ Resolver │  │  │   │
│  │  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │  │   │
│  │  │                                                         │  │   │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │  │   │
│  │  │  │ Request  │ │ Response │ │  CORS    │ │   Log    │  │  │   │
│  │  │  │ Transform│ │ Transform│ │  Handler │ │ & Monitor │  │  │   │
│  │  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │  │   │
│  │  └─────────────────────────────────────────────────────────┘  │   │
│  └────────────────────────────────────────────────────────────────┘   │
│       │              │              │                 │             │
│       ▼              ▼              ▼                 ▼             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │  Agent   │  │   Call   │  │  Billing │  │   Microservices  │   │
│  │  Service │  │  Service │  │  Service │  │    (Internal)    │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Gateway Middleware Pipeline

```typescript
// Middleware chain executed for every request
interface GatewayMiddleware {
  name: string;
  order: number;
  handler: (req: NextRequest, ctx: GatewayContext) => Promise<NextResponse | null>;
  // Return null to continue chain, NextResponse to short-circuit
}

interface GatewayContext {
  tenantId?: string;
  userId?: string;
  apiKey?: string;
  rateLimit: {
    remaining: number;
    reset: number;
    total: number;
  };
  requestStart: number;
}

// Built-in middleware order
const MIDDLEWARE_PIPELINE: GatewayMiddleware[] = [
  { name: 'tls-termination', order: 1, handler: enforceTLS },
  { name: 'cors', order: 2, handler: handleCORS },
  { name: 'auth', order: 3, handler: authenticateRequest },
  { name: 'rate-limit', order: 4, handler: checkRateLimit },
  { name: 'tenant-resolution', order: 5, handler: resolveTenant },
  { name: 'request-transform', order: 6, handler: transformRequest },
  { name: 'route', order: 7, handler: routeToService },
  { name: 'response-transform', order: 8, handler: transformResponse },
  { name: 'logging', order: 9, handler: logRequest },
];
```

## Route Resolution

```typescript
interface RouteDefinition {
  method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE' | 'OPTIONS';
  path: string;
  version: string; // v1, v2
  service: string;
  handler: string; // Internal endpoint
  auth: 'required' | 'optional' | 'none';
  scopes: string[];
  rateLimit: {
    tier: string;
    limit: number;
    window: number; // seconds
  };
}

// Route table — maps incoming requests to services
const ROUTE_TABLE: RouteDefinition[] = [
  // Agent Configuration
  { method: 'GET', path: '/api/v1/agents', service: 'agent-service', handler: '/agents', auth: 'required', scopes: ['agents:read'], rateLimit: { tier: 'standard', limit: 60, window: 60 } },
  { method: 'POST', path: '/api/v1/agents', service: 'agent-service', handler: '/agents', auth: 'required', scopes: ['agents:write'], rateLimit: { tier: 'standard', limit: 30, window: 60 } },
  // Calls
  { method: 'POST', path: '/api/v1/calls', service: 'call-service', handler: '/calls/initiate', auth: 'required', scopes: ['calls:write'], rateLimit: { tier: 'burst', limit: 10, window: 1 } },
  { method: 'GET', path: '/api/v1/calls/:id', service: 'call-service', handler: '/calls/:id', auth: 'required', scopes: ['calls:read'], rateLimit: { tier: 'standard', limit: 60, window: 60 } },
];
```

## Request/Response Handling

```typescript
// Standard response envelope
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: Record<string, string[]>;
    requestId: string;
  };
  meta?: {
    page: number;
    pageSize: number;
    total: number;
    hasMore: boolean;
  };
}

// Gateway enforces envelope for all responses
function formatResponse<T>(data: T, meta?: ApiMeta): ApiResponse<T> {
  return {
    success: true,
    data,
    meta,
  };
}

function formatError(code: string, message: string, status: number, details?: Record<string, string[]>): NextResponse {
  return NextResponse.json({
    success: false,
    error: { code, message, details, requestId: crypto.randomUUID() },
  }, { status });
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Gateway implementation | Next.js API Routes + Middleware | Unified with application, no separate gateway service |
| TLS termination | Edge (Cloudflare/LB) | Offloads CPU, DDoS protection at edge |
| Routing strategy | Path-based + version prefix | Simple, cacheable, no header sniffing needed |
| Response format | Standard envelope | Consistent client handling, version-proof |
| Observability | OpenTelemetry auto-instrumentation | Distributed tracing across all services |

## Integration Points

- **Ch 02 (Next.js Architecture)** — Gateway uses Next.js middleware and route handlers
- **Ch 04 (Real-Time)** — WebSocket connections bypass REST gateway, use separate WebSocket server
- **Ch 07 (API Routing)** — Route table drives the documentation generator
- **Ch 10 (Security)** — Auth middleware integrates with JWT/API key validation

## Production Considerations

- **Latency Budget**: Gateway adds < 5ms per request (auth check + rate limit in Redis)
- **High Availability**: Deployed across 3+ availability zones, stateless design
- **Graceful Degradation**: Rate limit cache failure falls back to local in-memory counters
- **Monitoring**: Every request logged with duration, status, and route; alerts on p99 > 100ms
- **Backpressure**: When upstream services are slow, gateway responds with 503 and `Retry-After` header
