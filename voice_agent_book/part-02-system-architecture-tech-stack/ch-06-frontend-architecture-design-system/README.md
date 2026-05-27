# Chapter 06: Frontend Architecture & Design System

> **Part:** 02 - System Architecture & Technology Stack

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Design System Foundation](sec-01-design-system-foundation.md) | Tokens (colors, typography, spacing), component primitives, accessibility (WCAG 2.1 AA) |
| 02 | [Component Architecture](sec-02-component-architecture.md) | Atomic design, compound components, controlled/uncontrolled patterns, polymorphism |
| 03 | [Dashboard Layout System](sec-03-dashboard-layout-system.md) | Shell layout, sidebar navigation, breadcrumbs, page headers, responsive breakpoints |
| 04 | [Real-Time Data Views](sec-04-real-time-data-views.md) | WebSocket subscriptions, optimistic updates, skeleton loading, live indicators |
| 05 | [Form & Builder Components](sec-05-form-builder-components.md) | React Hook Form + Zod, dynamic forms, drag-and-drop (React DnD), Monaco editor |
| 06 | [Data Visualization](sec-06-data-visualization.md) | Chart components (Recharts/Nivo), dashboards, real-time charts, data tables (TanStack Table) |
| 07 | [Theme & White-Label Support](sec-07-theme-white-label-support.md) | CSS variables for theming, dark mode, tenant branding overrides, custom CSS injection |
| 08 | [Performance & Bundle Optimization](sec-08-performance-bundle-optimization.md) | Code splitting, dynamic imports, bundle analysis, image optimization, font loading |

---

## Key Open-Source Tools

- **Radix UI** (MIT) — Accessible headless components
- **shadcn/ui** (MIT) — Component collection
- **Tailwind CSS** (MIT) — Utility CSS framework
- **TanStack Table** (MIT) — Data tables
- **React Hook Form** (MIT) — Form management
- **Zod** (MIT) — Schema validation
- **Framer Motion** (MIT) — Animations
- **Monaco Editor** (MIT) — Code/prompt editor

---

## Key Takeaways

- Radix UI + shadcn/ui for accessible, customizable components
- CSS variables enable white-label theming per tenant
- Real-time data via WebSocket subscriptions with optimistic updates
- React Hook Form + Zod for type-safe form handling
- Dynamic imports and code splitting for bundle optimization
- Atomic design for scalable component architecture
