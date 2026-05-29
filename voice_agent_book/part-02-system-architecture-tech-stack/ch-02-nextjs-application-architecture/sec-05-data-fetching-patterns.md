# Section 05: Data Fetching Patterns

## Hybrid Data Fetching Strategy

The platform uses a **hybrid data fetching approach** that combines React Server Components (RSC) for initial page data, TanStack Query (React Query) for client-side data management, and Server Actions for mutations. This provides fast initial loads with interactive, real-time updates.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DATA FETCHING STRATEGY MAP                           │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    PAGE LOAD                                     │    │
│  │                                                                  │    │
│  │  Server Component (RSC)                                         │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │  await prisma.agent.findMany()                           │    │    │
│  │  │  await fetch(API_URL + '/calls')                         │    │    │
│  │  │  return <ClientComponent initialData={data} />          │    │    │
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  │                            │                                     │    │
│  │                            ▼                                     │    │
│  │  Client Component (React Query)                                 │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │  const { data } = useQuery({                            │    │    │
│  │  │    queryKey: ['agents'],                                │    │    │
│  │  │    queryFn: () => fetch('/api/v1/agents'),              │    │    │
│  │  │    initialData: props.initialData                       │    │    │
│  │  │  })                                                      │    │    │
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                  USER INTERACTION                               │    │
│  │                                                                  │    │
│  │  Mutation (Server Action)                                       │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │  'use server'                                            │    │    │
│  │  │  export async function createAgent(data) {               │    │    │
│  │  │    await prisma.agent.create({ data })                   │    │    │
│  │  │    revalidatePath('/agents')                             │    │    │
│  │  │  }                                                        │    │    │
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  │                            │                                     │    │
│  │                            ▼                                     │    │
│  │  React Query Invalidation                                      │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │  queryClient.invalidateQueries({ queryKey: ['agents'] })│    │    │
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                  REAL-TIME UPDATES                              │    │
│  │                                                                  │    │
│  │  WebSocket Event → React Query Cache Update                    │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │  socket.on('call.updated', (call) => {                  │    │    │
│  │  │    queryClient.setQueryData(['calls', call.id], call)   │    │    │
│  │  │  })                                                      │    │    │
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Server Component Data Fetching

Fetch data directly in Server Components for immediate page renders:

```typescript
// app/(dashboard)/calls/page.tsx — Server Component
import { getServerSession } from '@/lib/auth'
import { prisma } from '@/lib/db'
import { CallList } from './call-list'  // Client component
import { CallMetricsBar } from './call-metrics-bar'

export default async function CallsPage({
  searchParams
}: {
  searchParams: { status?: string; page?: string }
}) {
  const session = await getServerSession()
  const page = parseInt(searchParams.page ?? '1')
  const status = searchParams.status
  const limit = 20

  // Parallel data fetching
  const [calls, total, metrics] = await Promise.all([
    prisma.call.findMany({
      where: {
        tenantId: session.tenantId,
        ...(status ? { status } : {})
      },
      include: {
        agent: { select: { name: true } },
        recording: { select: { duration: true } }
      },
      orderBy: { createdAt: 'desc' },
      skip: (page - 1) * limit,
      take: limit
    }),
    prisma.call.count({
      where: {
        tenantId: session.tenantId,
        ...(status ? { status } : {})
      }
    }),
    prisma.call.aggregate({
      where: { tenantId: session.tenantId },
      _count: true,
      _avg: { duration: true },
      _sum: { cost: true }
    })
  ])

  return (
    <div className="space-y-6">
      <CallMetricsBar {...metrics} />
      <CallList
        calls={calls}
        total={total}
        page={page}
        limit={limit}
      />
    </div>
  )
}
```

## React Query for Client-Side Data

Use React Query for interactive data that needs refetching:

```typescript
// app/(dashboard)/calls/call-list.tsx
'use client'

import { useState, useCallback } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { DataTable } from '@/components/ui/data-table'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { useWebSocket } from '@/hooks/use-websocket'
import type { Call } from '@/types/call'

interface CallListProps {
  calls: Call[]
  total: number
  page: number
  limit: number
}

export function CallList({ calls: initialData, total, page: initialPage, limit }: CallListProps) {
  const [page, setPage] = useState(initialPage)
  const [statusFilter, setStatusFilter] = useState<string | undefined>()
  const queryClient = useQueryClient()

  // React Query with initial data from server
  const { data, isLoading } = useQuery({
    queryKey: ['calls', page, statusFilter],
    queryFn: async () => {
      const params = new URLSearchParams({
        page: String(page),
        limit: String(limit),
        ...(statusFilter ? { status: statusFilter } : {})
      })
      const res = await fetch(`/api/v1/calls?${params}`)
      return res.json()
    },
    initialData: { data: initialData, meta: { total, page, limit } }
  })

  // Real-time updates via WebSocket
  const handleCallUpdate = useCallback((call: Call) => {
    queryClient.setQueryData(['calls', call.id], call)
    // Also invalidate list if call in current view
    queryClient.invalidateQueries({ queryKey: ['calls', page, statusFilter] })
  }, [queryClient, page, statusFilter])

  useWebSocket('call.updated', handleCallUpdate)
  useWebSocket('call.created', () => {
    queryClient.invalidateQueries({ queryKey: ['calls'] })
  })

  const columns = [
    { accessorKey: 'callerNumber', header: 'Caller' },
    { accessorKey: 'agent.name', header: 'Agent' },
    {
      accessorKey: 'status',
      header: 'Status',
      cell: ({ row }) => {
        const status = row.original.status
        const variant = status === 'completed' ? 'success'
          : status === 'active' ? 'warning'
          : status === 'failed' ? 'destructive'
          : 'default'
        return <Badge variant={variant}>{status}</Badge>
      }
    },
    {
      accessorKey: 'duration',
      header: 'Duration',
      cell: ({ row }) => formatDuration(row.original.duration)
    },
    { accessorKey: 'createdAt', header: 'Time', cell: ({ row }) => formatTime(row.original.createdAt) }
  ]

  return (
    <DataTable
      columns={columns}
      data={data?.data ?? []}
      isLoading={isLoading}
      pagination={{
        page,
        totalPages: Math.ceil((data?.meta?.total ?? total) / limit),
        onPageChange: setPage
      }}
      filters={[
        {
          key: 'status',
          value: statusFilter,
          onChange: setStatusFilter,
          options: [
            { label: 'All', value: undefined },
            { label: 'Active', value: 'active' },
            { label: 'Completed', value: 'completed' },
            { label: 'Failed', value: 'failed' }
          ]
        }
      ]}
    />
  )
}
```

## Server Actions for Mutations

Server Actions handle mutations with progressive enhancement:

```typescript
// app/(dashboard)/agents/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { z } from 'zod'
import { prisma } from '@/lib/db'
import { getServerSession } from '@/lib/auth'
import { createAuditLog } from '@/lib/audit'
import { kafka } from '@/lib/kafka'

const createAgentSchema = z.object({
  name: z.string().min(1, 'Name is required').max(100),
  description: z.string().max(500).optional(),
  voiceId: z.string().uuid('Invalid voice'),
  promptId: z.string().uuid('Invalid prompt'),
  language: z.string().length(5).default('en-US'),
  config: z.object({
    temperature: z.number().min(0).max(2).default(0.7),
    maxTokens: z.number().min(100).max(4096).default(1024),
    bargeIn: z.boolean().default(true),
    endCallAfterSilence: z.number().min(1).max(60).default(10)
  }).default({})
})

export async function createAgent(formData: FormData) {
  const session = await getServerSession()
  if (!session) {
    throw new Error('Unauthorized')
  }

  // Parse and validate
  const raw = Object.fromEntries(formData)
  const parsed = createAgentSchema.safeParse({
    ...raw,
    config: raw.config ? JSON.parse(raw.config as string) : undefined
  })

  if (!parsed.success) {
    return {
      error: 'Validation failed',
      details: parsed.error.flatten().fieldErrors
    }
  }

  // Create agent
  const agent = await prisma.agent.create({
    data: {
      ...parsed.data,
      tenantId: session.tenantId,
      createdBy: session.userId,
      status: 'draft'
    }
  })

  // Create initial version
  await prisma.agentVersion.create({
    data: {
      agentId: agent.id,
      version: 1,
      config: parsed.data.config,
      createdBy: session.userId
    }
  })

  // Audit log
  await createAuditLog({
    tenantId: session.tenantId,
    userId: session.userId,
    action: 'agent.created',
    resourceType: 'agent',
    resourceId: agent.id,
    metadata: { name: parsed.data.name }
  })

  // Emit event
  await kafka.produce('agent.created', {
    agentId: agent.id,
    tenantId: session.tenantId,
    timestamp: new Date().toISOString()
  })

  revalidatePath('/agents')
  return { success: true, agent }
}
```

## Streaming SSR

Use streaming for slower pages:

```typescript
// app/(dashboard)/analytics/page.tsx
import { Suspense } from 'react'
import { CallVolumeChart } from './call-volume-chart'
import { AgentPerformanceTable } from './agent-performance-table'
import { CostAnalytics } from './cost-analytics'
import { Skeleton } from '@/components/ui/skeleton'

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Analytics</h1>

      {/* These stream in as they complete */}
      <Suspense fallback={<Skeleton className="h-[400px]" />}>
        <CallVolumeChart />
      </Suspense>

      <div className="grid grid-cols-2 gap-6">
        <Suspense fallback={<Skeleton className="h-[300px]" />}>
          <AgentPerformanceTable />
        </Suspense>
        <Suspense fallback={<Skeleton className="h-[300px]" />}>
          <CostAnalytics />
        </Suspense>
      </div>
    </div>
  )
}

// Each component fetches its own data independently
async function CallVolumeChart() {
  const data = await fetchCallVolume() /  / / This can be slow
  return <ChartComponent data={data} />
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Initial data | Server Component fetch | No loading state, better SEO, smaller bundle |
| Refetching | React Query | Caching, deduplication, background refresh |
| Mutations | Server Actions | Progressive enhancement, no API route needed |
| Real-time | WebSocket + Query invalidation | Immediate updates, consistent cache |
| Slow pages | Streaming SSR | Progressive rendering, perceived performance |

## Integration Points

- **Part 06 (Frontend)** — React Query hooks used in design system components
- **Part 09 (State Management)** — React Query handles server state, Zustand handles client state
- **Part 04 (Real-Time)** — WebSocket integration for live data updates

## Production Considerations

- **Caching**: React Query `staleTime: 30000` for most queries, `staleTime: 0` for real-time
- **Deduplication**: React Query deduplicates identical concurrent requests
- **Error Handling**: Global query error handler with toast notifications
- **Optimistic Updates**: For mutations that affect UI immediately
- **Prefetching**: Prefetch data for likely next pages on hover
- **Waterfall Prevention**: Use Promise.all() in Server Components for parallel fetches
