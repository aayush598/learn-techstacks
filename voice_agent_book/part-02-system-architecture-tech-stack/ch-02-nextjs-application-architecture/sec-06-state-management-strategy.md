# Section 06: State Management Strategy

## Multi-Layer State Architecture

The platform employs a layered state management approach where each type of state is handled by the most appropriate tool. This avoids the common pitfalls of putting everything in a global store or over-engineering simple component state.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      STATE MANAGEMENT LAYERS                           │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Layer 1: SERVER STATE (TanStack Query / React Query)           │    │
│  │                                                                  │    │
│  │  What it manages:                                               │    │
│  │  • Data from API endpoints                                      │    │
│  │  • Server-side data that needs refetching                       │    │
│  │  • Cache, pagination, optimistic updates                        │    │
│  │                                                                  │    │
│  │  Examples:                                                      │    │
│  │  • Agent list, call history, campaign data                       │    │
│  │  • User profile, tenant settings                                │    │
│  │  • Analytics data, usage metrics                                │    │
│  │                                                                  │    │
│  │  Tools: useQuery, useMutation, useInfiniteQuery                 │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                               │                                         │
│  ┌───────────────────────────┼─────────────────────────────────────┐    │
│  │  Layer 2: CLIENT STATE (Zustand)                               │    │
│  │                           │                                      │    │
│  │  What it manages:         │                                      │    │
│  │  • Global UI state        │                                      │    │
│  │  • Cross-component state  │                                      │    │
│  │  • Complex state that requires middleware                       │    │
│  │                                                                  │    │
│  │  Examples:                                                      │    │
│  │  • Sidebar open/closed, active theme                             │    │
│  │  • Selected filters, current view mode                          │    │
│  │  • WebSocket connection state                                   │    │
│  │  • Call player state (playback position, volume)                │    │
│  │                                                                  │    │
│  │  Tools: create store, store slices, middleware                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Layer 3: URL STATE (Search Params / Next.js Navigation)        │    │
│  │                                                                  │    │
│  │  What it manages:                                               │    │
│  │  • Shareable/persistable UI state                                │    │
│  │  • Pagination, filters, search queries                           │    │
│  │  • Selected tabs, sort order                                     │    │
│  │                                                                  │    │
│  │  Approach: useSearchParams, useRouter, shallow routing          │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Layer 4: COMPONENT STATE (React useState / useReducer)         │    │
│  │                                                                  │    │
│  │  What it manages:                                               │    │
│  │  • Local UI state not needed elsewhere                           │    │
│  │  • Form input state, toggle states                               │    │
│  │  • Ephemeral animation state                                     │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Zustand Store Architecture

Zustand is used for global client state. Stores are organized by domain:

```typescript
// stores/ui-store.ts — Global UI state
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface UIState {
  sidebarOpen: boolean
  theme: 'light' | 'dark' | 'system'
  activeCallId: string | null
  notifications: Notification[]

  // Actions
  toggleSidebar: () => void
  setTheme: (theme: 'light' | 'dark' | 'system') => void
  setActiveCall: (callId: string | null) => void
  addNotification: (notification: Notification) => void
  dismissNotification: (id: string) => void
}

export const useUIStore = create<UIState>()(
  persist(
    (set) => ({
      sidebarOpen: true,
      theme: 'system',
      activeCallId: null,
      notifications: [],

      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
      setTheme: (theme) => set({ theme }),
      setActiveCall: (callId) => set({ activeCallId: callId }),
      addNotification: (notification) =>
        set((state) => ({
          notifications: [...state.notifications, notification]
        })),
      dismissNotification: (id) =>
        set((state) => ({
          notifications: state.notifications.filter((n) => n.id !== id)
        }))
    }),
    {
      name: 'ui-storage',
      partialize: (state) => ({ theme: state.theme, sidebarOpen: state.sidebarOpen })
    }
  )
)
```

```typescript
// stores/call-player-store.ts — Complex state with middleware
import { create } from 'zustand'
import { subscribeWithSelector } from 'zustand/middleware'

interface CallPlayerState {
  isPlaying: boolean
  currentTime: number
  duration: number
  volume: number
  speed: number
  currentSegment: string | null
  audioUrl: string | null

  // Actions
  play: () => void
  pause: () => void
  seek: (time: number) => void
  setVolume: (volume: number) => void
  setSpeed: (speed: number) => void
  loadRecording: (url: string) => void
  unload: () => void
}

export const useCallPlayerStore = create<CallPlayerState>()(
  subscribeWithSelector((set, get) => ({
    isPlaying: false,
    currentTime: 0,
    duration: 0,
    volume: 1,
    speed: 1,
    currentSegment: null,
    audioUrl: null,

    play: () => set({ isPlaying: true }),
    pause: () => set({ isPlaying: false }),
    seek: (time) => set({ currentTime: time }),
    setVolume: (volume) => set({ volume: Math.max(0, Math.min(1, volume)) }),
    setSpeed: (speed) => set({ speed }),
    loadRecording: (url) => set({ audioUrl: url, currentTime: 0, isPlaying: false }),
    unload: () => set({
      isPlaying: false,
      currentTime: 0,
      duration: 0,
      audioUrl: null,
      currentSegment: null
    })
  }))
)
```

## URL State Management

URL state is used for shareable/persistable UI state:

```typescript
// hooks/use-call-filters.ts
'use client'

import { useSearchParams, useRouter, usePathname } from 'next/navigation'
import { useCallback, useMemo } from 'react'

interface CallFilters {
  status?: string
  agentId?: string
  dateFrom?: string
  dateTo?: string
  search?: string
  page: number
  limit: number
  sortBy: string
  sortOrder: 'asc' | 'desc'
}

export function useCallFilters(): {
  filters: CallFilters
  setFilter: (key: string, value: string | undefined) => void
  setPage: (page: number) => void
  resetFilters: () => void
} {
  const searchParams = useSearchParams()
  const router = useRouter()
  const pathname = usePathname()

  const filters = useMemo<CallFilters>(() => ({
    status: searchParams.get('status') ?? undefined,
    agentId: searchParams.get('agentId') ?? undefined,
    dateFrom: searchParams.get('dateFrom') ?? undefined,
    dateTo: searchParams.get('dateTo') ?? undefined,
    search: searchParams.get('search') ?? undefined,
    page: parseInt(searchParams.get('page') ?? '1'),
    limit: parseInt(searchParams.get('limit') ?? '20'),
    sortBy: searchParams.get('sortBy') ?? 'createdAt',
    sortOrder: (searchParams.get('sortOrder') as 'asc' | 'desc') ?? 'desc'
  }), [searchParams])

  const setFilter = useCallback((key: string, value: string | undefined) => {
    const params = new URLSearchParams(searchParams.toString())
    if (value) {
      params.set(key, value)
    } else {
      params.delete(key)
    }
    // Reset to page 1 when filter changes
    params.set('page', '1')
    router.push(`${pathname}?${params.toString()}`, { scroll: false })
  }, [searchParams, router, pathname])

  const setPage = useCallback((page: number) => {
    const params = new URLSearchParams(searchParams.toString())
    params.set('page', String(page))
    router.push(`${pathname}?${params.toString()}`, { scroll: false })
  }, [searchParams, router, pathname])

  const resetFilters = useCallback(() => {
    router.push(pathname, { scroll: false })
  }, [router, pathname])

  return { filters, setFilter, setPage, resetFilters }
}
```

## Context for Global Providers

React Context is reserved for truly global concerns:

```typescript
// providers/tenant-provider.tsx
'use client'

import { createContext, useContext, type ReactNode } from 'react'

interface TenantContextValue {
  tenantId: string
  slug: string
  name: string
  config: TenantConfig
}

const TenantContext = createContext<TenantContextValue | null>(null)

export function TenantProvider({
  children,
  tenant
}: {
  children: ReactNode
  tenant: TenantContextValue
}) {
  return (
    <TenantContext.Provider value={tenant}>
      {children}
    </TenantContext.Provider>
  )
}

export function useTenant(): TenantContextValue {
  const context = useContext(TenantContext)
  if (!context) {
    throw new Error('useTenant must be used within TenantProvider')
  }
  return context
}
```

## State Decision Matrix

| Type of State | Tool | Example | Rationale |
|---------------|------|---------|-----------|
| Server data (list) | React Query | Agent list, call list | Caching, refetching, pagination |
| Server data (detail) | React Query | Call detail, agent detail | Cache invalidation on mutation |
| Global UI state | Zustand | Sidebar, theme, active call | Simple, fast, no boilerplate |
| Complex client state | Zustand + middleware | Call player, drag-and-drop | Subscribe, select, persist |
| URL-persisted state | Search Params | Filters, page, sort | Shareable URLs, back button |
| Form state | React Hook Form | Agent form, campaign config | Form-specific: validation, dirty tracking |
| Ephemeral state | useState | Dropdown open, tooltip | Local only, no global needed |
| Global config | Context | Tenant info, user session | Read-heavy, rarely changes |

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Server state | React Query (not SWR) | Devtools, mutation helpers, broader ecosystem |
| Client state | Zustand (not Redux) | Minimal boilerplate, TypeScript-native, middleware |
| URL state | Search Params (not Zustand) | Shareable, bookmarkable, back-button compatible |
| Form state | React Hook Form (not Formik) | Performance (isolated re-renders), smaller bundle |
| Persistence | Zustand persist middleware | Theme, sidebar preference survives refresh |

## Integration Points

- **Part 06 (Frontend)** — Zustand stores consumed by design system components
- **Part 09 (Data Flow)** — Event-driven updates flow into Zustand and React Query
- **Part 04 (Real-Time)** — WebSocket events update Zustand stores directly

## Production Considerations

- **Bundle Size**: Zustand is ~1KB gzipped vs Redux ~12KB
- **Performance**: Zustand subscriptions are fine-grained — components only re-render when their selected state changes
- **Persistence Limits**: Only persist essential UI state (theme, sidebar); never persist server data
- **Devtools**: Use Zustand devtools middleware in development
- **Testing**: Zustand stores can be tested in isolation without React components
