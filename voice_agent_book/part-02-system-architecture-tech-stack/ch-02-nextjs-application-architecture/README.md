# Chapter 02: Next.js Application Architecture

> **Part:** 02 - System Architecture & Technology Stack

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [App Router Structure & Conventions](sec-01-app-router-structure-conventions.md) | Route groups, parallel routes, intercepting routes, loading/error layouts |
| 02 | [Server vs Client Component Strategy](sec-02-server-vs-client-component-strategy.md) | Component split decision tree, server component benefits, "use client" boundaries |
| 03 | [API Route Organization](sec-03-api-route-organization.md) | Route handlers, route grouping by domain, middleware chain, rate limiting |
| 04 | [Middleware Architecture](sec-04-middleware-architecture.md) | Tenant resolution, authentication check, redirect/rewrite, header manipulation |
| 05 | [Data Fetching Patterns](sec-05-data-fetching-patterns.md) | RSC data fetching, React Query for client, server actions, streaming SSR |
| 06 | [State Management Strategy](sec-06-state-management-strategy.md) | Zustand for client state, React Query for server state, URL state, context for global |
| 07 | [Edge Functions & CDN Strategy](sec-07-edge-functions-cdn-strategy.md) | Edge middleware, edge API routes, ISR for static pages, CDN caching strategy |
| 08 | [Optimizations & Performance Patterns](sec-08-optimizations-performance-patterns.md) | Image optimization, font loading, bundle analysis, dynamic imports, streaming |

---

## Key Takeaways

- App Router with route groups for tenant/admin/developer portal sections
- Server components by default, client components only when interactivity needed
- API route handlers organized by domain (agents, calls, campaigns, billing)
- Middleware handles tenant detection, auth, and rate limiting
- Server actions for mutations, React Query for data fetching, Zustand for client state
- Edge functions for low-latency geographic distribution of auth and redirects
