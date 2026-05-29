# Section 02: Next.js Application Layer

## Role in the Architecture

The Next.js application serves as the **primary orchestration layer** for the AI Voice Agent platform. It handles the admin dashboard, developer portal, API routes, middleware, and server-side rendering. Unlike a traditional SPA setup, Next.js 14+ with the App Router enables server-side data fetching, streaming, and edge computing out of the box.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    NEXT.JS APPLICATION LAYER                        │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                      APP ROUTER                             │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │    │
│  │  │  Dashboard   │  │    Admin     │  │  Developer   │      │    │
│  │  │  (Route Grp) │  │  (Route Grp) │  │  (Route Grp) │      │    │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │    │
│  │         │                  │                  │             │    │
│  │  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐      │    │
│  │  │  Agents      │  │  Users       │  │  API Keys    │      │    │
│  │  │  Calls       │  │  Tenants     │  │  Webhooks    │      │    │
│  │  │  Campaigns   │  │  Billing     │  │  SDK Docs    │      │    │
│  │  │  Analytics   │  │  Audit       │  │  Playground  │      │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘      │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                      MIDDLEWARE                             │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │    │
│  │  │  Tenant  │  │   Auth   │  │  Rate    │  │ Redirect │    │    │
│  │  │  Detect  │  │  Check   │  │  Limit   │  │ /Rewrite │    │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                      API ROUTES                             │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │    │
│  │  │  Agent   │  │  Call    │  │  Voice   │  │  Billing │    │    │
│  │  │  /api/v1/│  │  /api/v1/│  │  /api/v1/│  │  /api/v1/│    │    │
│  │  │  agents  │  │  calls   │  │  /voice  │  │  /billing│    │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                 EDGE FUNCTIONS                              │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │    │
│  │  │   Auth   │  │   Geo    │  │   Cache  │                   │    │
│  │  │  Verify  │  │  Routing │  │  Invalidation                │    │
│  │  └──────────┘  └──────────┘  └──────────┘                   │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

## App Router Structure and Conventions

The application uses route groups to organize code by domain:

```
app/
├── (dashboard)/              # Route group — no path prefix
│   ├── dashboard/
│   ├── agents/
│   ├── calls/
│   ├── campaigns/
│   ├── analytics/
│   └── recordings/
├── (admin)/                  # Route group — admin portal
│   ├── admin/
│   │   ├── tenants/
│   │   ├── users/
│   │   ├── audit-log/
│   │   └── billing/
│   └── layout.tsx
├── (developer)/              # Route group — developer portal
│   ├── developer/
│   │   ├── api-keys/
│   │   ├── webhooks/
│   │   ├── docs/
│   │   └── playground/
└── api/                      # API routes
    └── v1/
        ├── agents/
        ├── calls/
        ├── campaigns/
        ├── voice/
        ├── billing/
        ├── auth/
        └── webhooks/
```

## Server vs Client Component Strategy

```typescript
// Server Component — data fetching, no interactivity
// app/agents/page.tsx
import { getServerSession } from '@/lib/auth'
import { prisma } from '@/lib/db'
import { AgentsList } from './agents-list'

export default async function AgentsPage() {
  const session = await getServerSession()
  const agents = await prisma.agent.findMany({
    where: { tenantId: session.tenantId },
    include: { version: true }
  })

  return <AgentsList agents={agents} />
}

// Client Component — interactive, uses "use client"
// app/agents/agents-list.tsx
'use client'

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { DataTable } from '@/components/ui/data-table'

export function AgentsList({ agents: initialData }: { agents: Agent[] }) {
  const [search, setSearch] = useState('')
  const { data } = useQuery({
    queryKey: ['agents', search],
    queryFn: () => fetch(`/api/v1/agents?search=${search}`).then(r => r.json()),
    initialData
  })

  return <DataTable data={data} />
}
```

## API Route Organization

API routes are organized by domain and follow RESTful conventions:

```typescript
// app/api/v1/agents/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from '@/lib/auth'
import { prisma } from '@/lib/db'
import { z } from 'zod'

const updateAgentSchema = z.object({
  name: z.string().min(1).max(100).optional(),
  voiceId: z.string().uuid().optional(),
  promptId: z.string().uuid().optional(),
  isActive: z.boolean().optional()
})

export async function PATCH(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  const session = await getServerSession()
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const body = await req.json()
  const parsed = updateAgentSchema.safeParse(body)
  if (!parsed.success) {
    return NextResponse.json(
      { error: 'Validation failed', details: parsed.error.flatten() },
      { status: 400 }
    )
  }

  const agent = await prisma.agent.update({
    where: { id: params.id, tenantId: session.tenantId },
    data: parsed.data
  })

  return NextResponse.json(agent)
}
```

## Middleware Chain

The middleware handles tenant resolution, authentication, and routing:

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // 1. Tenant detection from hostname or header
  const tenant = resolveTenant(request)
  if (!tenant && !isPublicPath(pathname)) {
    return NextResponse.redirect(new URL('/auth/login', request.url))
  }

  // 2. Authentication check
  const token = request.cookies.get('session_token')?.value
  if (!token && !isPublicPath(pathname)) {
    return NextResponse.redirect(new URL('/auth/login', request.url))
  }

  // 3. Rate limiting check (simplified)
  const ip = request.ip ?? 'unknown'
  const isRateLimited = checkRateLimit(ip)
  if (isRateLimited) {
    return new NextResponse('Too Many Requests', { status: 429 })
  }

  // 4. Attach tenant context to request headers
  const requestHeaders = new Headers(request.headers)
  if (tenant) {
    requestHeaders.set('x-tenant-id', tenant.id)
  }

  return NextResponse.next({
    request: { headers: requestHeaders }
  })
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|auth).*)']
}
```

## Data Fetching Patterns

The application uses a hybrid approach for data fetching:

| Pattern | Use Case | Example |
|---------|----------|---------|
| RSC (Server Component) | Initial page data | Agent list, dashboard metrics |
| React Query (Client) | Interactive data with refetching | Call logs, search results |
| Server Actions | Form mutations | Create agent, update settings |
| Streaming SSR | Long-loading pages | Analytics dashboards |

```typescript
// Server Action example
// app/agents/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { prisma } from '@/lib/db'
import { z } from 'zod'

const createAgentSchema = z.object({
  name: z.string().min(1),
  voiceId: z.string().uuid(),
  prompt: z.string(),
  language: z.string().default('en-US')
})

export async function createAgent(formData: FormData) {
  const session = await getServerSession()
  const parsed = createAgentSchema.parse(Object.fromEntries(formData))

  const agent = await prisma.agent.create({
    data: {
      ...parsed,
      tenantId: session.tenantId,
      createdBy: session.userId
    }
  })

  revalidatePath('/agents')
  return { success: true, agent }
}
```

## Integration Points

- **Part 01 (Platform Vision)** — Implements dashboard and admin features
- **Part 03 (Dev Setup)** — Local dev mirrors this structure
- **Part 06 (Frontend)** — Design system components render within this layer
- **Part 07 (API Gateway)** — API routes are the gateway implementation

## Production Considerations

- **Bundle Size**: Monitor via `@next/bundle-analyzer`, code-split heavy pages
- **Caching**: ISR for static pages, `stale-while-revalidate` for dynamic content
- **Error Handling**: Global error boundaries, error logging to Loki
- **Performance**: React Server Components minimize client-side JavaScript
- **Security**: Middleware prevents unauthorized access at the edge
