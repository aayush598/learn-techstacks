# Component, Page, and App Boundaries

> Part XIV · Chapter 37 · Sections 37.2–37.4 · _Estimated reading time: 18 min_
> **Prerequisite:** [Expected vs Unexpected](./01-expected-vs-unexpected.md)

## In one sentence

**Scope boundaries by blast radius and recoverability:** a **component boundary** isolates a widget, a **page boundary** isolates a route context, and an **app boundary** is the last safe fallback before a hard reload.

## Why this matters in production

The wrong scope turns one widget crash into losing an entire form or route state. For **ExportJob** list, a broken chart should not destroy filters and pagination; for **Checkout**, a shipping estimate failure must remain recoverable without losing the cart. Blast radius must match what the user can reasonably recover.

## Core concept

| Boundary | Scope | When to use | What to catch | Recovery | Blast radius |
| ------- | ----- | ----------- | ------------- | -------- | ------------ |
| **Component** (37.2) | Small subtree (card, widget, embed) | Isolated, optional, may retry independently | Render/lifecycle errors of that widget | Inline fallback + "Retry" scoped to widget | Minimal |
| **Page** (37.3) | Route-level subtree | Route data fetch/render failure; preserve nav shell | Errors affecting the whole view but not global chrome | Page-level error state + retry; keep header/nav alive if possible | Route |
| **App** (37.4) | Root of app tree | Global, unrecoverable at page level, bootstrap failures | Last-resort for unexpected render errors | "Something went wrong", "Reload", report diagnostics; consider safe redirect | Global |

> **Key:** React error boundaries only catch render, lifecycle, and constructor errors in the tree below them. They **do not** catch async, event handlers, SSR, or code outside React render (see 37.21–37.22).

## How it works (mechanics)

1. **Fail small first.** Default to component boundaries for non-critical visual blocks.
2. **Preserve context.** Keep navigation, layout, and user input when the error is scoped below page.
3. **Avoid nesting traps.** Too many boundaries add complexity; too few create large blast radius.
4. **Reset on route change.** Boundaries should reset when key props/route change so a fixed bug doesn't permanently lock a route.

## Placement examples

```tsx
<AppErrorBoundary>
  <Router>
    <AppShell />
    <Routes>
      <Route path="/export-jobs" element={
        <PageErrorBoundary>
          <ExportJobList /> {/* may have <WidgetErrorBoundary> for charts */}
        </PageErrorBoundary>
      }/>
      <Route path="/checkout/*" element={
        <PageErrorBoundary>
          <CheckoutFlow />
        </PageErrorBoundary>
      }/>
    </Routes>
  </Router>
</AppErrorBoundary>
```

## Key data / numbers

| Item | Guidance | Notes |
| --- | -------- | ----- |
| **Component boundary** | Widgets that can be skipped/replaced | Prefer for third-party embeds, heavy visualizations. |
| **Page boundary** | Per route | Keeps app chrome alive; good for route-level data failures. |
| **App boundary** | Exactly once near root | Last resort; offer reload and safe diagnostics. |
| **Reset keys** | Use `location.pathname`/route id | Prevents "stuck" fallback after fix/navigation. |

## Real-world use case — Acme SaaS (ExportJob)

**Context:** **ExportJob** has a list, filters, and a cost/size chart. 

**Failure:** The chart library throws a render error due to unexpected API shape. 

**Fix:** Place a **component boundary** around the chart. When it crashes, show "Chart unavailable — retry" and keep filters, pagination, and selected job visible. If the entire list fetch fails, a **page boundary** shows a route-level retry without losing global nav.

**Result:** Partial failure degrades gracefully instead of destroying work context.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One big app boundary | Simple | Loses all local state/context on widget failure | Small apps only |
| Boundary per widget | Small blast radius | Boilerplate, can mask root causes | Feature-heavy UIs |
| Page-only boundaries | Good middle ground | Widget failures still affect whole page | Common default with targeted component boundaries |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Scope to recoverability (what user can retry without losing work) | Scope by file size |
| Reset boundaries on navigation/route id | Leave a boundary in permanent fallback after successful retry |
| Keep app chrome alive at page boundary when possible | Crash global shell for a subview error |
| Document boundary placement per feature | Nest boundaries unnecessarily without reason |

## Common mistakes

- **Crashing checkout flow.** Shipping estimate widget throws → component boundary, not page/app.
- **Stuck fallback.** Forgetting `resetKeys` means fixed code still shows fallback on same route.
- **Treating async as boundary-caught.** Data fetch throws in `useEffect` async → must be handled in state, not by render boundary alone.

## Checklist

- [ ] Each independent widget with third-party deps has a component boundary if it can degrade.
- [ ] Critical flows (**Checkout**) have page-level boundaries with safe recovery.
- [ ] Exactly one app boundary exists near root with diagnostics capture.
- [ ] Boundaries reset on route change/key changes.

## Related

- [Recoverable vs Unrecoverable UI](./03-recoverable-vs-unrecoverable-ui.md)
- [Render Failures and Outside Boundaries](../02-deep-dive/04-render-failures-and-outside-boundaries.md)
- [React Error Boundary + Retry UI (Practical)](../03-practical-examples/01-react-error-boundary-retry-tsx.md)
