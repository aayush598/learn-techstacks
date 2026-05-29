# Section 01: Frontend Stack

## Technology Overview

The frontend stack is built around **Next.js 14+** with the App Router, **React 18**, **TypeScript 5**, and **Tailwind CSS**. Component libraries include **Radix UI** for accessible primitives and **TanStack Query** for server state management.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FRONTEND TECHNOLOGY STACK                        │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Framework: Next.js 14+ (App Router)                        │   │
│  │  Language: TypeScript 5 (strict mode)                       │   │
│  │                                                              │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │   │
│  │  │    React     │ │   Tailwind   │ │   Radix UI +     │    │   │
│  │  │    18.x      │ │  CSS 3.x     │ │   shadcn/ui      │    │   │
│  │  │  (Server +   │ │  (Utility-   │ │   (Headless      │    │   │
│  │  │  Client      │ │   first)     │ │    Components)   │    │   │
│  │  │  Components) │ │              │ │                  │    │   │
│  │  └──────────────┘ └──────────────┘ └──────────────────┘    │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │   │
│  │  │   TanStack   │ │   Zustand    │ │    Framer        │    │   │
│  │  │   Query 5.x  │ │  (Client     │ │    Motion 11.x   │    │   │
│  │  │  (Server     │ │   State)     │ │   (Animations)   │    │   │
│  │  │   State)     │ │              │ │                  │    │   │
│  │  └──────────────┘ └──────────────┘ └──────────────────┘    │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │   │
│  │  │   React      │ │   Zod 3.x    │ │   Lucide React   │    │   │
│  │  │   Hook Form  │ │  (Schema     │ │   (Icons)        │    │   │
│  │  │   7.x        │ │   Validation)│ │                  │    │   │
│  │  └──────────────┘ └──────────────┘ └──────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Bundle Size Budget:                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Library              Version   Size (gzip)   Lazy Load?   │   │
│  │  ───────────────────────────────────────────────────────    │   │
│  │  React + ReactDOM     18.x       42KB          No           │   │
│  │  Next.js              14.x       25KB          No           │   │
│  │  Tailwind CSS         3.x        8KB           No           │   │
│  │  Radix UI (all)       2.x        15KB          Per-need     │   │
│  │  TanStack Query       5.x        12KB          No           │   │
│  │  Zustand              4.x        3KB           No           │   │
│  │  Framer Motion        11.x       35KB          Per-page     │   │
│  │  React Hook Form      7.x        9KB           No           │   │
│  │  Zod                  3.x        15KB          No           │   │
│  │  Lucide React         latest     4KB           Tree-shaken  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Next.js Configuration

```typescript
// next.config.ts
import type { NextConfig } from 'next';

const config: NextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@radix-ui/react-select', '@radix-ui/react-dialog'],
  experimental: {
    optimizePackageImports: [
      'lucide-react',
      '@radix-ui/react-select',
      '@radix-ui/react-dialog',
      'recharts',
      'date-fns',
    ],
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 768, 1024, 1280, 1536],
    remotePatterns: [
      { protocol: 'https', hostname: 'cdn.voiceagent.dev' },
      { protocol: 'https', hostname: 'storage.googleapis.com' },
    ],
  },
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },
};

export default config;
```

## TypeScript Configuration

```typescript
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "esnext"],
    "module": "esnext",
    "moduleResolution": "bundler",
    "jsx": "preserve",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": false,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"]
}
```

## TanStack Query Integration

```typescript
// Query client setup with prefetching support
import { QueryClient } from '@tanstack/react-query';
import { cache } from 'react';

export const getQueryClient = cache(() => new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,        // 30 seconds
      gcTime: 5 * 60_000,       // 5 minutes
      retry: 2,
      refetchOnWindowFocus: false,
    },
  },
}));

// Server component data fetching pattern
async function AgentsList() {
  const queryClient = getQueryClient();
  await queryClient.prefetchQuery({
    queryKey: ['agents'],
    queryFn: () => agentService.listAgents(),
  });

  return (
    <HydrationBoundary>
      <AgentsListClient />
    </HydrationBoundary>
  );
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| UI framework | Next.js 14+ App Router | RSC, streaming, server actions, ISR |
| CSS solution | Tailwind CSS | Zero-runtime, design-token-friendly, small bundle |
| Component library | Radix UI (headless) | Accessible, unstyled, full design control |
| Server state | TanStack Query | Caching, prefetching, optimistic updates |
| Client state | Zustand | Minimal boilerplate, no context providers |
| Icons | Lucide React | Tree-shakeable, consistent style, MIT license |

## Integration Points

- **Ch 02 (Next.js Architecture)** — App Router patterns, server/client component strategy
- **Ch 06 (Design System)** — Radix UI + Tailwind consume design tokens
- **Ch 08 (Backend Stack)** — TanStack Query consumes API routes

## Production Considerations

- **Bundle Budget**: Initial load < 100KB gzipped; each route adds < 30KB gzipped
- **Code Splitting**: Automatic via Next.js App Router; manual dynamic imports for heavy components
- **Type Safety**: Strict TypeScript with `noUncheckedIndexedAccess` prevents runtime array/object access errors
- **Polyfills**: No IE11 support; modern browser targets reduce polyfill overhead
- **Error Tracking**: Sentry integration with source maps for production error debugging
