# Section 03: Dashboard Layout System

## Shell Layout Architecture

The dashboard layout system uses a **shell layout** pattern with a persistent sidebar, top navigation bar, and dynamic content area. The layout is server-rendered with client-side interactivity for responsive behaviors.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DASHBOARD SHELL LAYOUT                           │
│                                                                     │
│  ┌─────────┐ ┌──────────────────────────────────────────────────┐   │
│  │         │ │  Top Bar                                         │   │
│  │         │ │  ┌──────────┐ ┌──────┐ ┌──────┐ ┌────────────┐  │   │
│  │         │ │  │  Search  │ │ Notif│ │ Docs │ │ Profile     │  │   │
│  │         │ │  └──────────┘ └──────┘ └──────┘ └────────────┘  │   │
│  │ Sidebar  │ ├──────────────────────────────────────────────────┤   │
│  │          │ │                                                  │   │
│  │ ┌──────┐ │ │  Content Area                                   │   │
│  │ │Logo  │ │ │  ┌────────────────────────────────────────────┐  │   │
│  │ └──────┘ │ │  │                                            │  │   │
│  │          │ │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐   │  │   │
│  │ Overview │ │  │  │ StatCard │ │ StatCard │ │ StatCard │   │  │   │
│  │ Agents   │ │  │  └──────────┘ └──────────┘ └──────────┘   │  │   │
│  │ Campaigns│ │  │                                            │  │   │
│  │ Calls    │ │  │  ┌──────────────────────────────────────┐  │  │   │
│  │ Analytics│ │  │  │         Data Visualization           │  │  │   │
│  │ Settings │ │  │  └──────────────────────────────────────┘  │  │   │
│  │          │ │  │                                            │  │   │
│  │ Billing  │ │  │  ┌──────────────────────────────────────┐  │  │   │
│  │          │ │  │  │         Recent Calls Table           │  │  │   │
│  │          │ │  │  └──────────────────────────────────────┘  │  │   │
│  │          │ │  └────────────────────────────────────────────┘  │   │
│  └─────────┘ └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Sidebar Navigation

```typescript
interface NavItem {
  id: string;
  label: string;
  href: string;
  icon: LucideIcon;
  badge?: { count: number; variant: 'info' | 'warning' | 'danger' };
  children?: NavItem[]; // Collapsible sub-groups
  isActive: (pathname: string) => boolean;
}

interface SidebarProps {
  items: NavItem[];
  isCollapsed: boolean;
  onToggleCollapse: () => void;
  tenantLogo?: string;
  tenantName: string;
}
```

The sidebar supports three states: **expanded** (240px, full labels), **collapsed** (64px, icons only), and **hidden** (0px, mobile). State is persisted in localStorage and synced across browser tabs via `storage` event listener.

## Breadcrumbs

```typescript
interface BreadcrumbItem {
  label: string;
  href?: string; // undefined = current page (non-interactive)
  icon?: LucideIcon;
}

// Auto-generated from route tree
const breadcrumbMap: Record<string, BreadcrumbItem[]> = {
  '/dashboard/agents': [
    { label: 'Dashboard', href: '/dashboard' },
    { label: 'Agents', href: '/dashboard/agents' },
  ],
  '/dashboard/agents/[id]/edit': [
    { label: 'Dashboard', href: '/dashboard' },
    { label: 'Agents', href: '/dashboard/agents' },
    { label: 'Edit Agent' },
  ],
};
```

## Page Headers

Every page follows a consistent header pattern with title, description, actions, and optional tabs:

```typescript
interface PageHeaderProps {
  title: string;
  description?: string;
  actions?: React.ReactNode[]; // Buttons rendered in header
  tabs?: Tab[]; // Sub-navigation tabs
  breadcrumb?: BreadcrumbItem[];
  status?: { label: string; variant: 'success' | 'warning' | 'error' };
}
```

## Responsive Breakpoints

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RESPONSIVE BREAKPOINTS                           │
│                                                                     │
│  Mobile     < 640px          Single column, bottom nav              │
│  ┌──────────────────────┐  ┌─────────────────────────────────┐     │
│  │        Header        │  │  Stacked layout, full-width      │     │
│  ├──────────────────────┤  │  Sidebar → Bottom tab bar        │     │
│  │                      │  │  Cards: 1 column                 │     │
│  │    Content           │  │  DataTable: horizontal scroll    │     │
│  │                      │  │  Modals → Full-screen drawers    │     │
│  ├──────────────────────┤  └─────────────────────────────────┘     │
│  │  Bottom Navigation   │                                           │
│  └──────────────────────┘                                           │
│                                                                     │
│  Tablet     640-1024px      Two column, collapsed sidebar           │
│  ┌────────┬────────────────┐  ┌─────────────────────────────────┐  │
│  │Collapse│                │  │  Sidebar → Icons only (64px)    │  │
│  │  d SB  │   Content      │  │  Cards: 2 columns               │  │
│  │ (64px) │                │  │  DataTable: responsive columns  │  │
│  └────────┴────────────────┘  └─────────────────────────────────┘  │
│                                                                     │
│  Desktop   > 1024px         Three+ column, expanded sidebar         │
│  ┌─────────┬────────────────┐  ┌─────────────────────────────────┐  │
│  │Expanded │                │  │  Sidebar → Full (240px)         │  │
│  │ Sidebar │   Content      │  │  Cards: 3-4 columns             │  │
│  │(240px)  │                │  │  DataTable: all columns         │  │
│  └─────────┴────────────────┘  │  Multi-panel layouts            │  │
│                                └─────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Layout strategy | CSS Grid with named areas | Clean semantic layout, no nested flex hacks |
| Sidebar behavior | Persistent on desktop, overlay on mobile | Maximum screen utilization on large screens |
| Navigation state | URL-driven (Next.js App Router) | SSR/SSG compatible, shareable URLs |
| Mobile nav | Bottom tab bar | Thumb-friendly, iOS/Android design conventions |
| Sidebar collapse | localStorage + URL param | Survives refresh, shareable collapsed state |

## Integration Points

- **Ch 04 (Real-Time)** — Sidebar shows live call count badge via WebSocket subscription
- **Ch 07 (API Gateway)** — Breadcrumb generation uses route definitions from API docs
- **Ch 09 (Data Flow)** — Layout state (sidebar, active tab) persisted in URL search params

## Production Considerations

- **Shell Layout**: Server Component wrapper with Client Component interactivity islands — zero layout shift on navigation
- **Mobile Navigation**: Bottom tab bar has `position: fixed` with `safe-area-inset-bottom` for notched devices
- **Sidebar Scroll**: Virtualized nav items when > 50 menu items using TanStack Virtual
- **Breadcrumb SEO**: BreadcrumbList structured data for Google search results
- **Performance**: Route-level code splitting — dashboard shell loads ~45KB gzipped initial bundle
