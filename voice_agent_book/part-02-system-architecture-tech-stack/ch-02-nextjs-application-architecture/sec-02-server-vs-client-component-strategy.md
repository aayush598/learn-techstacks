# Section 02: Server vs Client Component Strategy

## Component Split Decision Framework

One of the most important architectural decisions in Next.js 14+ is determining which components should be Server Components (default) and which need to be Client Components (with `'use client'` directive). This decision directly impacts performance, bundle size, and user experience.

```
┌─────────────────────────────────────────────────────────────────────────┐
│              SERVER VS CLIENT COMPONENT DECISION TREE                   │
│                                                                         │
│  ┌─────────────────────────────────────────────┐                        │
│  │         Start: New Component                │                        │
│  └─────────────────────┬───────────────────────┘                        │
│                        ▼                                               │
│  ┌─────────────────────────────────────────────┐                        │
│  │ Does it need interactivity?                 │                        │
│  │ (onClick, onChange, useState, useEffect)    │                        │
│  └──────┬──────────────────────────┬───────────┘                        │
│         │ No                       │ Yes                               │
│         ▼                          ▼                                   │
│  ┌──────────────────┐   ┌─────────────────────────┐                    │
│  │ Can it be a      │   │ Does it need browser    │                    │
│  │ Server Component │   │ APIs or event handlers?  │                   │
│  └────────┬─────────┘   └──────┬──────────────────┘                    │
│           │                    │ Yes                                   │
│           ▼                    ▼                                       │
│  ┌─────────────────────────────────────────────┐                       │
│  │              SERVER COMPONENT               │                       │
│  │                                             │                       │
│  │  Benefits:                                  │                       │
│  │  ✓ Zero client JS                           │                       │
│  │  ✓ Direct database access                   │                       │
│  │  ✓ Access to secrets/tokens                 │                       │
│  │  ✓ Automatic code splitting                 │                       │
│  │  ✓ Stream from server                       │                       │
│  │                                             │                       │
│  │  Examples:                                  │                       │
│  │  • AgentListPage (fetch agents)             │                       │
│  │  • CallMetricsCard (aggregate data)         │                       │
│  │  • CampaignAnalytics (computed data)        │                       │
│  └─────────────────────────────────────────────┘                       │
│                       │                                                │
│                       ▼                                                │
│  ┌─────────────────────────────────────────────┐                       │
│  │         CLIENT COMPONENT                    │                       │
│  │                                             │                       │
│  │  Rules:                                     │                       │
│  │  ✓ Add 'use client' directive               │                       │
│  │  ✓ Minimize the component tree              │                       │
│  │  ✓ Push data fetching to server boundary    │                       │
│  │  ✓ Use server actions for mutations         │                       │
│  │                                             │                       │
│  │  When needed:                               │                       │
│  │  • User interactions (clicks, drags)        │                       │
│  │  • Browser APIs (localStorage, clipboard)   │                       │
│  │  • Real-time subscriptions (WebSocket)      │                       │
│  │  • Animations (Framer Motion)               │                       │
│  │  • State management (Zustand)               │                       │
│  └─────────────────────────────────────────────┘                       │
└─────────────────────────────────────────────────────────────────────────┘
```

## Server Component Pattern

Server Components are the default and should be used whenever possible:

```typescript
// ✅ Server Component — no 'use client' needed
// app/(dashboard)/agents/page.tsx
import { getServerSession } from '@/lib/auth'
import { prisma } from '@/lib/db'
import { AgentsTable } from './agents-table'  // Client component boundary
import { AgentStatsCards } from './agent-stats-cards'  // Can be server or client

export default async function AgentsPage() {
  // Direct database access — never sent to client
  const session = await getServerSession()
  const agents = await prisma.agent.findMany({
    where: { tenantId: session.tenantId },
    select: {
      id: true,
      name: true,
      voice: { select: { name: true } },
      version: { select: { version: true } },
      _count: { select: { calls: true } },
      createdAt: true,
      status: true
    },
    orderBy: { createdAt: 'desc' }
  })

  const metrics = await prisma.call.aggregate({
    where: { tenantId: session.tenantId },
    _count: true,
    _avg: { duration: true }
  })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">AI Agents</h1>
        <CreateAgentButton />  {/* Client component — just the button */}
      </div>

      <AgentStatsCards
        totalAgents={agents.length}
        totalCalls={metrics._count}
        avgDuration={metrics._avg.duration}
      />

      <AgentsTable agents={agents} />
    </div>
  )
}
```

## Client Component Pattern

Client Components are used only when interactivity is required:

```typescript
// ✅ Client Component — minimal, pushed to leaf
// app/(dashboard)/agents/agents-table.tsx
'use client'

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
  getSortedRowModel,
  getFilteredRowModel,
  getPaginationRowModel
} from '@tanstack/react-table'
import { Input } from '@/components/ui/input'
import { DataTable } from '@/components/ui/data-table'

interface AgentRow {
  id: string
  name: string
  voice: string
  version: number
  totalCalls: number
  createdAt: Date
  status: 'active' | 'inactive' | 'draft'
}

// Receives initial data from server component
export function AgentsTable({ agents: initialData }: { agents: AgentRow[] }) {
  const [search, setSearch] = useState('')

  // React Query for client-side filtering + refetching
  const { data, isLoading } = useQuery({
    queryKey: ['agents', search],
    queryFn: async () => {
      const res = await fetch(`/api/v1/agents?search=${search}`)
      return res.json()
    },
    initialData: { data: initialData }
  })

  const columns: ColumnDef<AgentRow>[] = [
    { accessorKey: 'name', header: 'Name' },
    { accessorKey: 'voice', header: 'Voice' },
    { accessorKey: 'version', header: 'Version' },
    { accessorKey: 'totalCalls', header: 'Total Calls' },
    { accessorKey: 'status', header: 'Status' },
    {
      id: 'actions',
      cell: ({ row }) => (
        <div className="flex gap-2">
          <AgentActionsDropdown agentId={row.original.id} />
        </div>
      )
    }
  ]

  return (
    <DataTable
      columns={columns}
      data={data?.data ?? []}
      searchPlaceholder="Search agents..."
      onSearch={setSearch}
    />
  )
}
```

## Composing Server + Client Components

The key pattern is to keep server components at the page level and push client boundaries down:

```typescript
// PAGE (Server Component) — fetches data
// CALL RECORD (Server Component) — pure display
// BUTTON (Client Component) — minimal interactivity

// app/calls/[id]/page.tsx — Server Component
export default async function CallDetailPage({ params }: { params: { id: string } }) {
  const session = await getServerSession()
  const call = await prisma.call.findUnique({
    where: { id: params.id, tenantId: session.tenantId },
    include: {
      transcript: true,
      recording: true,
      agent: true
    }
  })

  if (!call) notFound()

  return (
    <div className="space-y-6">
      <CallHeader call={call} />              {/* Server component */}
      <CallTranscript segments={call.transcript} />  {/* Could be server */}
      <CallControls callId={call.id}>         {/* Server wrapper */}
        <EndCallButton callId={call.id} />     {/* Client leaf */}
        <TransferButton callId={call.id} />    {/* Client leaf */}
      </CallControls>
    </div>
  )
}
```

## Data Flow Patterns

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     DATA FLOW BETWEEN COMPONENTS                       │
│                                                                         │
│  Server Component                                                       │
│  ┌─────────────────────────────┐                                        │
│  │  export default async fn    │                                        │
│  │  const data = await db()    │                                        │
│  │  return <ClientComp data/>  │─── Props (serializable) ────►         │
│  └─────────────────────────────┘                                        │
│                                                                         │
│  Client Component                                                       │
│  ┌─────────────────────────────┐                                        │
│  │  'use client'               │                                        │
│  │  export function ClientComp │                                        │
│  │  const [state, setState]    │                                        │
│  │  const { data } = useQuery  │─── Fetch /api/v1/... ────► API        │
│  │  return <div>...</div>      │                                        │
│  └─────────────────────────────┘                                        │
│                                                                         │
│  Server Action                                                          │
│  ┌─────────────────────────────┐                                        │
│  │  'use server'               │                                        │
│  │  export async function act  │─── Mutate DB ────► revalidatePath()   │
│  └─────────────────────────────┘                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

## When to Use Each Pattern

| Scenario | Component Type | Rationale |
|----------|---------------|-----------|
| Fetching data for page | Server Component | Direct DB access, no waterfall |
| Initial page load | Server Component | Send HTML, not JS |
| Search/Filter results | Client Component | Interactive, real-time |
| Form submission | Server Action + Client Form | Progressive enhancement |
| Real-time updates | Client Component | WebSocket subscription |
| Static content | Server Component | Zero JS, fast render |
| Map/Drawing canvas | Client Component | Browser API needed |
| Audio player | Client Component | Web Audio API needed |

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Default choice | Server Component | Smaller bundle, faster page loads |
| Client boundary | Leaf components | Minimize client JS scope |
| Data fetching | Server Component → Client via props | No waterfall, pre-filled cache |
| Mutations | Server Actions | Progressive enhancement, secure |
| Real-time data | Client + React Query + WebSocket | Subscription-based updates |

## Integration Points

- **Part 06 (Frontend)** — Design system components designed for both server/client
- **Part 07 (API Gateway)** — API routes called from client components
- **Part 09 (State Management)** — Zustand stores used in client components only

## Production Considerations

- **Bundle Size**: Server components contribute zero JS to client bundle
- **Waterfall Prevention**: Fetch data in server components, pass to client
- **Serialization**: Server → Client props must be serializable (no functions, no Date objects without serialization)
- **Error Handling**: Error boundaries at both server and client levels
- **Loading States**: Suspense boundaries around async server components
- **Streaming**: Use `loading.tsx` for streaming server components
