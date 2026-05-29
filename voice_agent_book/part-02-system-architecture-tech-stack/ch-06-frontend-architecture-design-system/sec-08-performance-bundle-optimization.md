# Section 08: Performance & Bundle Optimization

## Optimization Strategy

Performance optimization follows a **layered approach**: code splitting at the route level, dynamic imports for heavy components, image optimization via Next.js Image, font loading with `next/font`, and bundle analysis in CI.

```
┌─────────────────────────────────────────────────────────────────────┐
│                 PERFORMANCE OPTIMIZATION LAYERS                     │
│                                                                     │
│  Layer 1: Route-Level Code Splitting                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  /dashboard          → dashboard.chunk.js    (45KB)        │   │
│  │  /dashboard/agents   → agents.chunk.js       (35KB)        │   │
│  │  /dashboard/calls    → calls.chunk.js         (28KB)        │   │
│  │  /dashboard/settings → settings.chunk.js      (22KB)        │   │
│  │  /dashboard/analytics→ analytics.chunk.js     (85KB)        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Layer 2: Dynamic Component Imports                                 │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Monaco Editor     → loaded on demand   (450KB gzipped)    │   │
│  │  Chart Libraries   → loaded on demand   (45-60KB gzipped)  │   │
│  │  React DnD         → loaded on demand   (15KB gzipped)     │   │
│  │  Date picker       → loaded on demand   (12KB gzipped)     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Layer 3: Asset Optimization                                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Images → Next.js Image (WebP/AVIF, lazy load, blur)       │   │
│  │  Fonts  → next/font (self-hosted, subset, swap)             │   │
│  │  Icons  → Lucide (tree-shakeable, dynamic import)           │   │
│  │  CSS    → Tailwind JIT (purged, < 10KB final)              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Layer 4: Runtime Optimizations                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  React Server Components → Zero JS for static content       │   │
│  │  Streaming SSR           → Progressive HTML delivery        │   │
│  │  ISR/SSG                 → Pre-rendered static pages         │   │
│  │  Edge Middleware         → Fast geo-routing, A/B testing    │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Dynamic Imports Pattern

```typescript
import dynamic from 'next/dynamic';

// Chart components — loaded only when used
const LineChart = dynamic(() => import('@/components/charts/line-chart'), {
  loading: () => <ChartSkeleton />,
  ssr: false,
});

// Monaco Editor — massive bundle, loaded only for agent builder
const MonacoEditor = dynamic(() => import('@monaco-editor/react'), {
  loading: () => <div className="h-96 animate-pulse bg-muted rounded" />,
  ssr: false,
});

// React DnD — only on builder pages
const DndProvider = dynamic(() => import('./dnd-provider'), {
  ssr: false,
});
```

## Bundle Analysis Configuration

```typescript
// next.config.js bundle analysis
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // Production optimizations
  swcMinify: true,
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },
  experimental: {
    optimizePackageImports: [
      'lucide-react',
      '@radix-ui/react-select',
      '@radix-ui/react-dialog',
      'recharts',
    ],
  },
});
```

## Image Optimization

```typescript
import Image from 'next/image';

// Automatic WebP/AVIF conversion, lazy loading, responsive sizes
function TenantLogo({ src, alt }: { src: string; alt: string }) {
  return (
    <Image
      src={src}
      alt={alt}
      width={120}
      height={40}
      priority={false}
      placeholder="blur"
      blurDataURL="data:image/webp;base64,..."
      sizes="(max-width: 768px) 80px, 120px"
      className="object-contain"
    />
  );
}
```

## Font Loading

```typescript
import { Inter, JetBrains_Mono } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
  // Preload only required weights
  weight: ['400', '500', '600', '700'],
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-mono',
  weight: ['400', '500'],
});
```

## Performance Budgets

```typescript
const PERFORMANCE_BUDGETS = {
  initialLoad: {
    jsBundle: { maxSize: 100_000, unit: 'bytes' }, // 100KB gzipped
    cssBundle: { maxSize: 10_000, unit: 'bytes' },
    lcp: { maxMs: 2500 },
    fid: { maxMs: 100 },
    cls: { maxScore: 0.1 },
  },
  routeSpecific: {
    dashboard: { jsBundle: 120_000 },
    analytics: { jsBundle: 180_000 },
    agentBuilder: { jsBundle: 600_000 }, // Includes Monaco
  },
};
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Framework | Next.js App Router | Automatic code splitting, RSC, streaming |
| CSS approach | Tailwind JIT | Zero runtime, purged unused styles |
| Image component | next/image | WebP/AVIF, lazy load, responsive, CDN |
| Font strategy | next/font | Self-hosted, subset, no layout shift |
| Bundle analysis | @next/bundle-analyzer | Visual treemap, CI integration |

## Integration Points

- **Ch 02 (Next.js Architecture)** — Route groups and layouts enable code splitting boundaries
- **Ch 08 (Tech Stack)** — Webpack/Rspack configuration for advanced optimizations
- **Ch 09 (Data Flow)** — RSC streaming for progressive data loading

## Production Considerations

- **Monitoring**: Real User Monitoring (RUM) via Web Vitals API — LCP, FID, CLS tracked to Grafana
- **CI Gates**: Lighthouse CI score < 90 blocks deployment; bundle size regressions flagged in PR
- **CDN Strategy**: Static assets served via CDN with immutable cache headers (1 year)
- **Preload Critical Assets**: Font CSS preloaded, above-the-fold images preloaded with `priority`
- **Graceful Degradation**: No JS fallback for static content, form submission works without JS via `<form action>`
- **Target Metrics**: Lighthouse score > 95, LCP < 2s, TBT < 200ms, CLS < 0.05
