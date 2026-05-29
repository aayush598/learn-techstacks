# Section 01: App Router Structure & Conventions

## Route Architecture

Next.js 14's App Router provides a file-system based routing paradigm with support for route groups, parallel routes, intercepting routes, and nested layouts. Our AI Voice Agent platform leverages these features to create a maintainable, scalable application structure.

```
app/
├── (dashboard)/                              # Route group — no URL prefix
│   ├── layout.tsx                            # Dashboard shell (sidebar, header)
│   ├── loading.tsx                           # Global dashboard loading state
│   ├── page.tsx                              # / — Dashboard home
│   ├── agents/
│   │   ├── page.tsx                          # /agents
│   │   ├── loading.tsx
│   │   ├── [id]/
│   │   │   ├── page.tsx                      # /agents/:id
│   │   │   ├── edit/
│   │   │   │   └── page.tsx                  # /agents/:id/edit
│   │   │   └── builder/
│   │   │       └── page.tsx                  # /agents/:id/builder
│   │   └── new/
│   │       └── page.tsx                      # /agents/new
│   ├── calls/
│   │   ├── page.tsx                          # /calls
│   │   ├── loading.tsx
│   │   ├── [id]/
│   │   │   ├── page.tsx                      # /calls/:id
│   │   │   └── transcript/
│   │   │       └── page.tsx                  # /calls/:id/transcript
│   │   └── active/
│   │       └── page.tsx                      # /calls/active
│   ├── campaigns/
│   │   ├── page.tsx                          # /campaigns
│   │   ├── [id]/
│   │   │   ├── page.tsx                      # /campaigns/:id
│   │   │   ├── analytics/
│   │   │   │   └── page.tsx                  # /campaigns/:id/analytics
│   │   │   └── contacts/
│   │   │       └── page.tsx                  # /campaigns/:id/contacts
│   │   └── new/
│   │       └── page.tsx                      # /campaigns/new
│   ├── analytics/
│   │   ├── page.tsx                          # /analytics
│   │   ├── calls/
│   │   │   └── page.tsx                      # /analytics/calls
│   │   ├── agents/
│   │   │   └── page.tsx                      # /analytics/agents
│   │   └── billing/
│   │       └── page.tsx                      # /analytics/billing
│   ├── recordings/
│   │   ├── page.tsx                          # /recordings
│   │   └── [id]/
│   │       └── page.tsx                      # /recordings/:id
│   └── settings/
│       ├── page.tsx                          # /settings
│       ├── profile/
│       │   └── page.tsx
│       ├── billing/
│       │   └── page.tsx                      # /settings/billing
│       ├── team/
│       │   └── page.tsx                      # /settings/team
│       └── notifications/
│           └── page.tsx                      # /settings/notifications
│
├── (admin)/                                  # Route group — admin portal
│   ├── layout.tsx
│   └── admin/
│       ├── page.tsx                          # /admin
│       ├── tenants/
│       │   ├── page.tsx                      # /admin/tenants
│       │   └── [id]/
│       │       └── page.tsx                  # /admin/tenants/:id
│       ├── users/
│       │   └── page.tsx                      # /admin/users
│       ├── audit-log/
│       │   └── page.tsx                      # /admin/audit-log
│       └── system/
│           ├── page.tsx                      # /admin/system
│           └── features/
│               └── page.tsx                  # /admin/system/features
│
├── (developer)/                              # Route group — developer portal
│   ├── layout.tsx
│   └── developer/
│       ├── page.tsx                          # /developer
│       ├── api-keys/
│       │   ├── page.tsx                      # /developer/api-keys
│       │   └── new/
│       │       └── page.tsx                  # /developer/api-keys/new
│       ├── webhooks/
│       │   ├── page.tsx                      # /developer/webhooks
│       │   └── [id]/
│       │       └── page.tsx                  # /developer/webhooks/:id
│       └── playground/
│           └── page.tsx                      # /developer/playground
│
├── (auth)/                                   # Route group — no layout needed
│   ├── login/
│   │   ├── page.tsx                          # /login
│   │   └── actions.ts                        # Server Actions
│   ├── signup/
│   │   └── page.tsx                          # /signup
│   ├── forgot-password/
│   │   └── page.tsx                          # /forgot-password
│   └── callback/
│       └── route.ts                          # OAuth callback handler
│
└── api/                                      # API routes (no App Router layouts)
    └── v1/
        ├── agents/
        │   ├── route.ts                      # GET / POST /api/v1/agents
        │   └── [id]/
        │       └── route.ts                  # GET / PATCH / DELETE /api/v1/agents/:id
        ├── calls/
        │   ├── route.ts
        │   └── [id]/
        │       └── route.ts
        ├── campaigns/...
        ├── voice/...
        ├── billing/...
        └── webhooks/...
```

## Route Groups & Layout Nesting

Route groups `(groupName)` organize routes without affecting URL paths:

```typescript
// app/(dashboard)/layout.tsx — Dashboard shell layout
export default function DashboardLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}

// app/(dashboard)/agents/layout.tsx — Agents sub-layout
export default function AgentsLayout({
  children,
  modal
}: {
  children: React.ReactNode
  modal: React.ReactNode
}) {
  return (
    <>
      <div className="space-y-4">
        <AgentsHeader />
        {children}
      </div>
      {modal}  {/* Parallel route for modals */}
    </>
  )
}
```

## Parallel Routes for Modals

Parallel routes enable rendering multiple pages in the same view, useful for modals without changing the URL:

```typescript
// app/(dashboard)/agents/layout.tsx
export default function AgentsLayout({
  children,
  modal
}: {
  children: React.ReactNode
  modal: React.ReactNode
}) {
  return (
    <>
      {children}
      {modal}  {/* @modal parallel route renders here */}
    </>
  )
}

// app/(dashboard)/agents/@modal/default.tsx
export default function DefaultModal() {
  return null  // No modal by default
}

// app/(dashboard)/agents/@modal/(.)new/page.tsx
// This intercepts /agents/new and renders as a modal
export default function NewAgentModal() {
  return (
    <Dialog open>
      <DialogContent>
        <AgentForm />
      </DialogContent>
    </Dialog>
  )
}
```

## Intercepting Routes

Intercepting routes allow the app to "intercept" a navigation and show a different view:

```typescript
// (.) matches same level
// (..) matches one level above
// (..)(..) matches two levels above
// (...) matches from root app directory

// app/(dashboard)/agents/@modal/(.)new/page.tsx
// Intercepts /agents/new — shows as modal when navigated from within dashboard
// Direct navigation to /agents/new shows the full page
```

## Loading & Error States

Each route segment can have its own loading and error boundaries:

```typescript
// app/(dashboard)/calls/loading.tsx
export default function CallsLoading() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-8 w-48" />          {/* Title */}
      <Skeleton className="h-10 w-full" />       {/* Search bar */}
      <div className="space-y-2">
        {Array.from({ length: 10 }).map((_, i) => (
          <Skeleton key={i} className="h-16 w-full" />
        ))}
      </div>
    </div>
  )
}

// app/(dashboard)/calls/error.tsx
'use client'

import { useEffect } from 'react'
import { Button } from '@/components/ui/button'

export default function CallsError({
  error,
  reset
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error('Calls page error:', error)
  }, [error])

  return (
    <div className="flex flex-col items-center justify-center py-12">
      <h2 className="text-xl font-semibold mb-2">Something went wrong</h2>
      <p className="text-muted-foreground mb-4">
        Failed to load calls. Please try again.
      </p>
      <Button onClick={reset}>Try Again</Button>
    </div>
  )
}
```

## File Conventions Summary

| Convention | Purpose |
|------------|---------|
| `page.tsx` | Route UI — must export default component |
| `layout.tsx` | Shared UI for segment and children |
| `loading.tsx` | Loading UI (React Suspense) |
| `error.tsx` | Error UI (React Error Boundary) |
| `not-found.tsx` | 404 UI |
| `route.ts` | API route handler |
| `template.tsx` | Re-rendered on each navigation (unlike layout) |
| `default.tsx` | Fallback for parallel routes |

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Route Groups | (dashboard), (admin), (developer) | Separate concerns without URL bloat |
| Parallel Routes | @modal for dialogs | Preserve URL state, shareable links |
| Intercepting Routes | (.) pattern | Smooth UX for deep-link navigations |
| Nested Layouts | Per-domain layouts | Each domain (agents, calls) has its own chrome |
| Shared Components | app/components | Co-located near routes but shared via import |

## Integration Points

- **Part 06 (Frontend Architecture)** — Design system components used within layouts
- **Part 07 (API Gateway)** — API routes under `/api/v1/` serve as the external API
- **Part 03 (Dev Setup)** — Local dev mirrors production App Router structure

## Production Considerations

- **Bundle Splitting**: Each route group is automatically code-split
- **Layout Caching**: Layouts are cached and reused across navigations
- **Static Rendering**: Dashboard pages with static content use static generation
- **Dynamic Rendering**: Call detail pages use dynamic rendering for real-time data
- **Middleware**: Edge middleware runs before route matching for auth/tenant detection
