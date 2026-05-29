# Section 04: Middleware Architecture

## Edge Middleware Overview

Next.js Middleware runs at the **edge** (CDN level) before a request reaches the application server. This is the ideal place for high-performance, low-latency operations like tenant detection, authentication checks, URL rewriting, and rate limiting.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      MIDDLEWARE EXECUTION FLOW                          │
│                                                                         │
│  Request arrives                                                        │
│       │                                                                 │
│       ▼                                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    MIDDLEWARE CHAIN                             │    │
│  │                                                                  │    │
│  │  1. Tenant Detection                                             │    │
│  │     ├── Extract tenant slug from hostname or header              │    │
│  │     └── Set x-tenant-id header for downstream                    │    │
│  │                                                                  │    │
│  │  2. Authentication Check                                         │    │
│  │     ├── Check session cookie or Authorization header             │    │
│  │     ├── Validate JWT/API key                                     │    │
│  │     ├── Redirect to /login if unauthenticated                    │    │
│  │     └── Set x-user-id header                                     │    │
│  │                                                                  │    │
│  │  3. Rate Limiting (Edge)                                         │    │
│  │     ├── Check IP-based rate limit (KV store)                     │    │
│  │     └── Return 429 if exceeded                                   │    │
│  │                                                                  │    │
│  │  4. Route Protection                                             │    │
│  │     ├── Check role/permissions for admin routes                  │    │
│  │     └── Redirect unauthorized users                              │    │
│  │                                                                  │    │
│  │  5. Rewrite/Redirect                                             │    │
│  │     ├── Rewrite /dashboard to /(dashboard)                       │    │
│  │     ├── Handle i18n routing                                      │    │
│  │     └── Redirect old URLs to new                                 │    │
│  │                                                                  │    │
│  │  6. Header Manipulation                                          │    │
│  │     ├── Set security headers (CSP, HSTS, X-Frame-Options)        │    │
│  │     ├── Set cache headers                                        │    │
│  │     └── Add request ID                                           │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│       │                                                                 │
│       ▼                                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    APPLICATION SERVER                           │    │
│  │  (Request now has tenant/user context in headers)              │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Implementation

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { getTenantFromHost } from '@/lib/edge/tenant'
import { validateSession } from '@/lib/edge/auth'
import { checkRateLimit } from '@/lib/edge/rate-limit'

// Route configuration
export const config = {
  matcher: [
    // Match all routes except static files, images, and auth pages
    '/((?!_next/static|_next/image|favicon.ico|auth|api/webhooks).*)',
    // Also match API routes
    '/api/:path*'
  ]
}

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const startTime = Date.now()
  
  try {
    // ──────────────────────────────────────────────────────────
    // 1. Tenant Detection
    // ──────────────────────────────────────────────────────────
    const tenant = await getTenantFromHost(request)
    const requestHeaders = new Headers(request.headers)
    
    if (tenant) {
      requestHeaders.set('x-tenant-id', tenant.id)
      requestHeaders.set('x-tenant-slug', tenant.slug)
    }

    // ──────────────────────────────────────────────────────────
    // 2. Authentication Check
    // ──────────────────────────────────────────────────────────
    const isPublicPath = (
      pathname.startsWith('/auth/') ||
      pathname === '/' ||
      pathname.startsWith('/api/v1/auth/')
    )

    if (!isPublicPath) {
      const token = request.cookies.get('session_token')?.value
        ?? request.headers.get('authorization')?.replace('Bearer ', '')
        ?? request.headers.get('x-api-key')

      if (!token) {
        if (pathname.startsWith('/api/')) {
          return NextResponse.json(
            { error: { code: 'UNAUTHORIZED', message: 'Authentication required' } },
            { status: 401 }
          )
        }
        return NextResponse.redirect(new URL('/auth/login', request.url))
      }

      const session = await validateSession(token)
      if (!session.valid) {
        const loginUrl = new URL('/auth/login', request.url)
        loginUrl.searchParams.set('redirect', pathname)
        return NextResponse.redirect(loginUrl)
      }

      requestHeaders.set('x-user-id', session.userId)
      requestHeaders.set('x-user-role', session.role)
      
      // ──────────────────────────────────────────────────────────
      // 3. Role-Based Access Control (for admin routes)
      // ──────────────────────────────────────────────────────────
      if (pathname.startsWith('/admin') && session.role !== 'admin') {
        if (pathname.startsWith('/api/')) {
          return NextResponse.json(
            { error: { code: 'FORBIDDEN', message: 'Admin access required' } },
            { status: 403 }
          )
        }
        return NextResponse.redirect(new URL('/dashboard', request.url))
      }
    }

    // ──────────────────────────────────────────────────────────
    // 4. Rate Limiting (API routes only)
    // ──────────────────────────────────────────────────────────
    if (pathname.startsWith('/api/') && !isPublicPath) {
      const ip = request.ip ?? 'unknown'
      const tenantId = tenant?.id ?? ip
      const rateLimitResult = await checkRateLimit(tenantId)
      
      if (!rateLimitResult.allowed) {
        return new NextResponse(
          JSON.stringify({
            error: { code: 'RATE_LIMITED', message: 'Too many requests' }
          }),
          {
            status: 429,
            headers: {
              'Content-Type': 'application/json',
              'X-RateLimit-Limit': String(rateLimitResult.limit),
              'X-RateLimit-Remaining': '0',
              'X-RateLimit-Reset': String(rateLimitResult.resetAt),
              'Retry-After': String(rateLimitResult.retryAfter)
            }
          }
        )
      }

      requestHeaders.set('x-ratelimit-remaining', String(rateLimitResult.remaining))
    }

    // ──────────────────────────────────────────────────────────
    // 5. Security Headers
    // ──────────────────────────────────────────────────────────
    const response = NextResponse.next({
      request: { headers: requestHeaders }
    })

    response.headers.set('X-Content-Type-Options', 'nosniff')
    response.headers.set('X-Frame-Options', 'DENY')
    response.headers.set('X-XSS-Protection', '1; mode=block')
    response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')
    response.headers.set(
      'Content-Security-Policy',
      "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';"
    )
    
    // Only set HSTS in production
    if (process.env.NODE_ENV === 'production') {
      response.headers.set(
        'Strict-Transport-Security',
        'max-age=63072000; includeSubDomains; preload'
      )
    }

    // ──────────────────────────────────────────────────────────
    // 6. Performance Headers
    // ──────────────────────────────────────────────────────────
    response.headers.set('X-Response-Time', `${Date.now() - startTime}ms`)
    response.headers.set('X-Request-Id', crypto.randomUUID())

    return response

  } catch (error) {
    // Middleware should never crash — log and allow through
    console.error('Middleware error:', error)
    return NextResponse.next()
  }
}
```

## Edge-Compatible Tenant Detection

```typescript
// lib/edge/tenant.ts
import { NextRequest } from 'next/server'

interface TenantInfo {
  id: string
  slug: string
  config: Record<string, unknown>
}

// Cache tenants in edge KV store (Vercel KV / Upstash)
const TENANT_CACHE_TTL = 300 // 5 minutes

export async function getTenantFromHost(
  request: NextRequest
): Promise<TenantInfo | null> {
  const hostname = request.headers.get('host') ?? ''
  
  // Extract tenant slug from hostname
  // e.g., acme.voiceplatform.com → acme
  // e.g., localhost:3000 → check x-tenant header
  const slug = hostname.includes('localhost')
    ? request.headers.get('x-tenant') ?? 'default'
    : hostname.split('.')[0]

  if (!slug || slug === 'www') return null

  // Check edge cache first
  const cacheKey = `tenant:${slug}`
  const cached = await EDGE_KV.get(cacheKey)
  if (cached) {
    return JSON.parse(cached)
  }

  // Fetch from primary database via API
  const response = await fetch(
    `${process.env.INTERNAL_API_URL}/api/internal/tenants/resolve?slug=${slug}`,
    { headers: { 'Authorization': `Bearer ${process.env.INTERNAL_API_KEY}` } }
  )

  if (!response.ok) return null

  const tenant = await response.json()
  
  // Cache for future requests
  await EDGE_KV.set(cacheKey, JSON.stringify(tenant), { ex: TENANT_CACHE_TTL })

  return tenant
}
```

## Edge Rate Limiting

```typescript
// lib/edge/rate-limit.ts
import { EDGE_KV } from '@/lib/edge/kv'

interface RateLimitResult {
  allowed: boolean
  limit: number
  remaining: number
  resetAt: number
  retryAfter: number
}

const TIER_LIMITS: Record<string, number> = {
  free: 10,
  starter: 60,
  pro: 300,
  business: 1000,
  enterprise: 5000
}

export async function checkRateLimit(
  identifier: string,
  tier: string = 'free'
): Promise<RateLimitResult> {
  const limit = TIER_LIMITS[tier] ?? TIER_LIMITS.free
  const windowMs = 60_000 // 1 minute
  const now = Date.now()
  const windowKey = Math.floor(now / windowMs)
  
  const key = `ratelimit:${identifier}:${windowKey}`
  
  const count = await EDGE_KV.incr(key)
  if (count === 1) {
    await EDGE_KV.expire(key, 60)
  }

  const resetAt = (windowKey + 1) * windowMs
  const allowed = count <= limit

  return {
    allowed,
    limit,
    remaining: Math.max(0, limit - count),
    resetAt: Math.floor(resetAt / 1000),
    retryAfter: Math.max(0, Math.ceil((resetAt - now) / 1000))
  }
}
```

## Matcher Configuration

```typescript
// middleware.ts config
export const config = {
  matcher: [
    // Dashboard and app routes
    '/((?!_next/static|_next/image|favicon.ico|auth).*)',
    // API routes (v1)
    '/api/v1/:path*',
    // Public API docs
    '/docs/:path*',
    // Developer portal
    '/developer/:path*'
  ]
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Edge Runtime | Vercel Edge / Cloudflare Workers | Low-latency global execution |
| KV Store | Upstash Redis / Vercel KV | HTTP-based, edge-compatible |
| Auth Strategy | Session cookie + API key | Supports both browser and API clients |
| Tenant Resolution | Hostname-based | Clean URLs, SEO-friendly |
| Rate Limiting | Sliding window | Fair, accurate, edge-performant |

## Integration Points

- **Part 07 (API Gateway)** — Middleware is the first line of API gateway enforcement
- **Part 10 (Security)** — Security headers and auth checks enforced here
- **Part 16 (User Management)** — Session validation integrates with auth service

## Production Considerations

- **Middleware Latency**: Keep middleware execution under 10ms — it delays every request
- **Cold Starts**: Minimize dependencies; avoid heavy computation at the edge
- **Edge Memory**: Limit KV store sizes; avoid loading large datasets
- **Fallback Behavior**: Middleware should never throw — always return NextResponse.next() on error
- **Testing**: Middleware is critical path — test with edge runtime locally
- **Monitoring**: Track middleware execution time, auth failure rate, rate limit triggers
