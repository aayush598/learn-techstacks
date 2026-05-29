# Section 07: Edge Functions & CDN Strategy

## Edge Computing Architecture

Edge functions bring computation closer to users, reducing latency for geographic-sensitive operations. The platform uses edge functions for authentication checks, URL rewrites, header manipulation, and serving static assets via CDN.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                  EDGE FUNCTIONS & CDN STRATEGY                         │
│                                                                         │
│                          ┌──────────────────┐                          │
│                          │   Global CDN     │                          │
│                          │  (Cloudflare/    │                          │
│                          │   Vercel Edge)   │                          │
│                          └────────┬─────────┘                          │
│                                   │                                     │
│          ┌────────────────────────┼────────────────────────┐            │
│          │                        │                        │            │
│          ▼                        ▼                        ▼            │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐     │
│  │   Edge Region 1  │    │   Edge Region 2  │    │   Edge Region 3  │    │
│  │   (US East)      │    │   (EU West)      │    │   (Asia Pacific)  │   │
│  │                   │    │                   │    │                   │   │
│  │  ┌─────────────┐ │    │  ┌─────────────┐ │    │  ┌─────────────┐ │   │
│  │  │ Edge Middle- │ │    │  │ Edge Middle- │ │    │  │ Edge Middle- │ │   │
│  │  │ ware        │ │    │  │ ware        │ │    │  │ ware        │ │   │
│  │  │ (Auth,      │ │    │  │ (Auth,      │ │    │  │ (Auth,      │ │   │
│  │  │ Geo-route)  │ │    │  │ Geo-route)  │ │    │  │ Geo-route)  │ │   │
│  │  └──────┬──────┘ │    │  └──────┬──────┘ │    │  └──────┬──────┘ │   │
│  └─────────┼─────────┘    └─────────┼─────────┘    └─────────┼─────────┘   │
│            │                        │                        │            │
│            └────────────┬───────────┴───────────┬────────────┘            │
│                         │                        │                        │
│                         ▼                        ▼                        │
│              ┌─────────────────────┐  ┌─────────────────────┐            │
│              │  Static Assets (CDN) │  │  API / Dynamic      │            │
│              │  • JS bundles       │  │  • Edge API routes  │            │
│              │  • CSS / fonts      │  │  • ISR pages        │            │
│              │  • Images           │  │  • Server Actions   │            │
│              │  • Recorded audio   │  │  • WebSocket        │            │
│              │  (static version)   │  │                     │            │
│              └─────────────────────┘  └─────────────────────┘            │
└─────────────────────────────────────────────────────────────────────────┘
```

## Edge Middleware Use Cases

### 1. Geographic Routing

```typescript
// middleware.ts — Geographic routing
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const EDGE_REGIONS: Record<string, string> = {
  'US': 'us-east',
  'CA': 'us-east',
  'GB': 'eu-west',
  'DE': 'eu-west',
  'FR': 'eu-west',
  'JP': 'ap-northeast',
  'AU': 'ap-southeast',
  'IN': 'ap-south',
  'SG': 'ap-southeast',
  'BR': 'sa-east'
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Skip for static assets
  if (pathname.startsWith('/_next/')) {
    return NextResponse.next()
  }

  // Get geolocation from edge request
  const country = request.geo?.country ?? 'US'
  const region = EDGE_REGIONS[country] ?? 'us-east'

  // For API calls, route to nearest region
  if (pathname.startsWith('/api/')) {
    const response = NextResponse.next()
    response.headers.set('x-edge-region', region)
    response.headers.set('x-user-country', country)
    return response
  }

  // For dashboard, serve from nearest edge
  const response = NextResponse.next()
  response.headers.set('x-edge-region', region)
  return response
}
```

### 2. Edge API Rate Limiting with KV Store

```typescript
// lib/edge-rate-limit.ts
// Uses Vercel KV or Upstash Redis for distributed rate limiting at the edge

interface EdgeRateLimitConfig {
  maxRequests: number
  windowSeconds: number
  blockDurationSeconds?: number
}

const DEFAULT_CONFIG: EdgeRateLimitConfig = {
  maxRequests: 100,
  windowSeconds: 60
}

export async function edgeRateLimit(
  identifier: string,
  config: Partial<EdgeRateLimitConfig> = {}
): Promise<{ success: boolean; remaining: number }> {
  const { maxRequests, windowSeconds } = { ...DEFAULT_CONFIG, ...config }
  const now = Math.floor(Date.now() / 1000)
  const window = Math.floor(now / windowSeconds)
  const key = `ratelimit:${identifier}:${window}`

  // Atomic increment at edge
  const count = await EDGE_KV.incr(key)
  if (count === 1) {
    await EDGE_KV.expire(key, windowSeconds)
  }

  return {
    success: count <= maxRequests,
    remaining: Math.max(0, maxRequests - count)
  }
}
```

### 3. Edge Feature Flags

```typescript
// lib/edge-features.ts
// Edge-compatible feature flag evaluation

interface FeatureFlags {
  newDashboard: boolean
  advancedAnalytics: boolean
  betaVoiceCloning: boolean
  webhookV2: boolean
}

const FEATURE_FLAGS_KEY = 'edge:feature-flags'

export async function getFeatureFlags(tenantId: string): Promise<FeatureFlags> {
  // Check edge cache first
  const cached = await EDGE_KV.get(`${FEATURE_FLAGS_KEY}:${tenantId}`)
  if (cached) {
    return JSON.parse(cached)
  }

  // Fallback to defaults
  return {
    newDashboard: false,
    advancedAnalytics: false,
    betaVoiceCloning: false,
    webhookV2: false
  }
}
```

## Incremental Static Regeneration (ISR)

ISR combines static generation with dynamic updates for pages that don't change frequently:

```typescript
// app/(dashboard)/analytics/reports/[id]/page.tsx
// ISR — regenerated on demand or every 5 minutes

interface ReportPageProps {
  params: { id: string }
}

export default async function ReportPage({ params }: ReportPageProps) {
  const report = await fetchReport(params.id)

  return (
    <div>
      <h1>{report.name}</h1>
      <ReportContent data={report.data} />
    </div>
  )
}

// Revalidate every 5 minutes
export const revalidate = 300

// On-demand revalidation via API route
// POST /api/revalidate?secret=TOKEN&path=/analytics/reports/123
export async function revalidateReport(reportId: string) {
  'use server'
  revalidatePath(`/analytics/reports/${reportId}`)
}
```

## CDN Caching Strategy

```typescript
// CDN cache configuration

interface CacheRules {
  'static assets': {
    pattern: '/_next/static/*'
    ttl: 31536000  // 1 year
    staleWhileRevalidate: true
  }
  'images': {
    pattern: '/images/*'
    ttl: 86400    // 1 day
    staleWhileRevalidate: true
  }
  'recorded audio': {
    pattern: '/audio/*'
    ttl: 604800   // 1 week
    immutable: true
  }
  'API responses': {
    pattern: '/api/v1/*'
    ttl: 0        // No CDN cache
    vary: 'Authorization'
  }
  'public pages': {
    pattern: '/(dashboard|agents|calls)'
    ttl: 60       // 1 minute
    staleWhileRevalidate: 300
  }
  'analytics': {
    pattern: '/analytics/*'
    ttl: 300      // 5 minutes
  }
}
```

## Edge API Routes

Some API routes can run at the edge for lower latency:

```typescript
// app/api/edge/auth/route.ts
// Runs on edge runtime — faster JWT validation

export const runtime = 'edge'

export async function POST(request: Request) {
  const { token } = await request.json()

  try {
    // Edge-compatible JWT verification
    const payload = await verifyJWT(token, process.env.JWT_SECRET!)
    const session = await getSessionFromPayload(payload)

    return Response.json({ valid: true, session })
  } catch {
    return Response.json({ valid: false }, { status: 401 })
  }
}
```

## Edge-Compatible Dependencies

| Library | Edge Compatible | Notes |
|---------|----------------|-------|
| jose | ✓ | JWT verification at edge |
| @upstash/redis | ✓ | HTTP-based Redis for edge |
| nanoid | ✓ | Edge-safe ID generation |
| zod | ✓ | Validation at edge |
| next-intl | ✓ | i18n routing at edge |
| next-auth/middleware | ✓ | Auth checks at edge |

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Edge Runtime | Vercel Edge / Cloudflare | Wide geographic distribution |
| Static Generation | ISR for docs, analytics reports | Fast loads with periodic updates |
| CDN | Built-in (Vercel) / Cloudflare | Zero-config, global edge network |
| Edge KV | Upstash Redis / Vercel KV | Distributed rate limiting, cache |
| Edge Analytics | Real User Monitoring (RUM) | Performance insights from edge |

## Integration Points

- **Part 23 (DevOps)** — CDN and edge deployment configuration
- **Part 24 (Scaling)** — Edge distribution improves global performance
- **Part 07 (API Gateway)** — Edge middleware is the first gateway layer

## Production Considerations

- **Edge Limits**: 50ms CPU time per request, 1MB response body, 4MB request body
- **Cold Starts**: Edge functions have minimal cold start (~5ms)
- **KV Limitations**: 256KB per value, 10 reads/sec per key on free tier
- **Cache Invalidation**: Use on-demand revalidation (webhook) for ISR pages
- **Monitoring**: Track edge function execution time, cache hit rate, regional latency
- **Cost**: Edge functions are typically cheaper than serverless functions for high-volume auth/redirect workloads
