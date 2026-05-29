# Section 08: Optimizations & Performance Patterns

## Performance Architecture

This section covers the performance optimization patterns used throughout the Next.js application, focusing on bundle size, image optimization, font loading, dynamic imports, streaming, and caching strategies.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PERFORMANCE OPTIMIZATION MAP                         │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    BUILD-TIME OPTIMIZATIONS                     │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │    │
│  │  │  Bundle      │  │  Image       │  │  Font        │           │    │
│  │  │  Analysis    │  │  Optimization│  │  Loading     │           │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘           │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │    │
│  │  │  Code        │  │  Tree        │  │  Static      │           │    │
│  │  │  Splitting   │  │  Shaking     │  │  Generation  │           │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘           │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                   RUNTIME OPTIMIZATIONS                          │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │    │
│  │  │  Streaming   │  │  Dynamic     │  │  Lazy        │           │    │
│  │  │  SSR         │  │  Imports     │  │  Loading     │           │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘           │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │    │
│  │  │  React       │  │  Memoization │  │  Debouncing  │           │    │
│  │  │  Server      │  │  (useMemo)   │  │  (Inputs)    │           │    │
│  │  │  Components  │  │              │  │               │           │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘           │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                   CACHING STRATEGIES                             │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │    │
│  │  │  Data Cache  │  │  Full Route  │  │  React Query │           │    │
│  │  │  (Redis)     │  │  Cache (CDN) │  │  Cache       │           │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘           │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐                              │    │
│  │  │  ISR Cache   │  │  Router      │                              │    │
│  │  │  (On-demand) │  │  Cache (SWR) │                              │    │
│  │  └──────────────┘  └──────────────┘                              │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Bundle Analysis

Configure bundle analysis to identify large dependencies:

```typescript
// next.config.js / next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // Production optimizations
  productionBrowserSourceMaps: false,
  swcMinify: true,
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production'
  },

  // Image optimization
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 1080, 1920],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    minimumCacheTTL: 60 * 60 * 24 * 30, // 30 days
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.minio.voiceplatform.com'
      }
    ]
  },

  // Experimental features
  experimental: {
    optimizePackageImports: [
      'lucide-react',
      'recharts',
      '@radix-ui/react-icons',
      '@tanstack/react-table'
    ],
    serverActions: {
      bodySizeLimit: '4mb'
    }
  }
}

export default nextConfig
```

Run bundle analysis:

```bash
# Package.json scripts
{
  "analyze": "ANALYZE=true next build",
  "analyze:server": "ANALYZE_SERVER=true next build",
  "analyze:browser": "ANALYZE_BROWSER=true next build"
}
```

## Dynamic Imports

Split large components and libraries into separate chunks:

```typescript
// Dynamic import of heavy component
import dynamic from 'next/dynamic'
import { Skeleton } from '@/components/ui/skeleton'

// Analytics chart — large library (Recharts)
const CallVolumeChart = dynamic(
  () => import('@/components/analytics/call-volume-chart'),
  {
    loading: () => <Skeleton className="h-[400px]" />,
    ssr: false  // Chart is client-only
  }
)

// Code editor — heavy dependency (Monaco)
const PromptEditor = dynamic(
  () => import('@/components/agents/prompt-editor'),
  {
    loading: () => <Skeleton className="h-[600px]" />,
    ssr: false
  }
)

// Data table — conditionally loaded
const DataTable = dynamic(
  () => import('@/components/ui/data-table'),
  { ssr: false }
)

// Audio player — only when needed
const CallPlayer = dynamic(
  () => import('@/components/calls/call-player'),
  { ssr: false }
)

// Usage in page
export default function AgentDetailPage() {
  const [showEditor, setShowEditor] = useState(false)

  return (
    <div>
      <Button onClick={() => setShowEditor(true)}>
        Edit Prompt
      </Button>

      {showEditor && (
        <Suspense fallback={<Skeleton className="h-[600px]" />}>
          <PromptEditor />
        </Suspense>
      )}

      <Suspense fallback={<Skeleton className="h-[400px]" />}>
        <CallVolumeChart />
      </Suspense>
    </div>
  )
}
```

## Image Optimization

```typescript
// Next.js Image component with optimization
import Image from 'next/image'

// Avatar with optimization
<Image
  src={user.avatarUrl}
  alt={user.name}
  width={40}
  height={40}
  className="rounded-full"
  priority={false}
  loading="lazy"
  placeholder="blur"
  blurDataURL="data:image/webp;base64,..."
/>

// Hero image with priority
<Image
  src="/images/dashboard-hero.webp"
  alt="Dashboard overview"
  width={1200}
  height={600}
  priority
  className="rounded-lg"
/>

// Remote image with configuration
<Image
  src={`https://cdn.voiceplatform.com/tenants/${tenantId}/logo.png`}
  alt="Tenant logo"
  width={200}
  height={50}
  unoptimized={false}
/>
```

## Font Loading

```typescript
// app/layout.tsx — Optimized font loading
import { Inter, JetBrains_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
  preload: true,
  fallback: ['system-ui', 'sans-serif']
})

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-mono',
  preload: false,  // Only preload primary font
  fallback: ['monospace']
})

export default function RootLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable}`}>
      <body className={inter.className}>
        {children}
      </body>
    </html>
  )
}
```

## Streaming & Progressive Rendering

```typescript
// app/dashboard/page.tsx — Streaming with Suspense
import { Suspense } from 'react'
import { Skeleton } from '@/components/ui/skeleton'
import { CallVolumeCard } from './call-volume-card'
import { AgentStatusCard } from './agent-status-card'
import { RecentCallsTable } from './recent-calls-table'
import { CostBreakdown } from './cost-breakdown'
import { AlertBanner } from './alert-banner'

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Instant — no async needed */}
      <AlertBanner />

      {/* Stream in as data arrives */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Suspense fallback={<Skeleton className="h-32" />}>
          <CallVolumeCard />
        </Suspense>
        <Suspense fallback={<Skeleton className="h-32" />}>
          <AgentStatusCard />
        </Suspense>
        <Suspense fallback={<Skeleton className="h-32" />}>
          <CostBreakdown />
        </Suspense>
      </div>

      {/* Slowest component streams in last */}
      <Suspense fallback={<Skeleton className="h-96" />}>
        <RecentCallsTable />
      </Suspense>
    </div>
  )
}

// Each component fetches its own data
async function CallVolumeCard() {
  const data = await fetchCallVolume() // ~200ms
  return <MetricCard title="Call Volume" value={data.total} />
}

async function AgentStatusCard() {
  const data = await fetchAgentStatus() // ~300ms
  return <MetricCard title="Active Agents" value={data.active} />
}

async function RecentCallsTable() {
  const data = await fetchRecentCalls() // ~800ms — slow
  return <CallsTable calls={data} />
}
```

## Caching Strategy

```typescript
// lib/cache.ts — Multi-level caching
import { redis } from '@/lib/redis'

export async function getCachedOrFetch<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttlSeconds: number = 60
): Promise<T> {
  // Level 1: In-memory cache (per request)
  const cached = globalThis.__CACHE__?.[key]
  if (cached && cached.expiresAt > Date.now()) {
    return cached.data as T
  }

  // Level 2: Redis cache
  const redisCached = await redis.get(key)
  if (redisCached) {
    // Store in memory for this request
    if (globalThis.__CACHE__) {
      globalThis.__CACHE__[key] = { data: redisCached, expiresAt: Date.now() + 5000 }
    }
    return JSON.parse(redisCached as string) as T
  }

  // Level 3: Fetch from source
  const data = await fetcher()
  await redis.set(key, JSON.stringify(data), { ex: ttlSeconds })

  return data
}
```

## Performance Metrics

```typescript
// Performance monitoring setup
export const performanceConfig = {
  // Core Web Vitals thresholds
  LCP: { good: 2500, poor: 4000 },     // Largest Contentful Paint (ms)
  FID: { good: 100, poor: 300 },        // First Input Delay (ms)
  CLS: { good: 0.1, poor: 0.25 },       // Cumulative Layout Shift

  // Custom metrics
  TTFB: { good: 200, poor: 600 },       // Time to First Byte (ms)
  FCP: { good: 1500, poor: 3000 },      // First Contentful Paint (ms)
  INP: { good: 200, poor: 500 },        // Interaction to Next Paint (ms)

  // Application metrics
  API_LATENCY: { good: 100, poor: 500 },
  PAGE_LOAD: { good: 2000, poor: 5000 },
  ROUTE_CHANGE: { good: 300, poor: 1000 }
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Image Format | AVIF + WebP fallback | Best compression (AVIF 50% smaller than WebP) |
| Font Strategy | Next.js font (self-hosted) | Zero layout shift, no external requests |
| Code Splitting | Dynamic imports + route groups | Automatic per-page chunks |
| Streaming | React Suspense boundaries | Progressive rendering, perceived performance |
| Caching | 3-level (memory → Redis → source) | Optimal trade-off of speed vs freshness |

## Integration Points

- **Part 06 (Frontend)** — Design system components use these patterns
- **Part 23 (DevOps)** — Build configuration for optimal bundles
- **Part 24 (Scaling)** — Performance metrics drive scaling decisions

## Production Considerations

- **Bundle Budget**: Set max bundle size warning at 200KB JS, 50KB CSS
- **Lighthouse Targets**: Maintain 90+ on all Core Web Vitals
- **Real User Monitoring (RUM)**: Track actual user performance via Web Vitals API
- **Error Budget**: Performance regression = 10% degradation triggers rollback
- **A/B Testing**: Test performance impact of new features before rollout
- **Performance Budget in CI**: Fail builds that exceed bundle size budgets
