# Chapter 37 — Reference (Frontend Error Handling)

> Part XIV · Chapter 37 · Section 05 · _Estimated reading time: 14 min_

## Mapping API Errors → UI States

| HTTP/status/code | Classification | UI Surface | Action |
| ----------------- | --------------- | ----------- | ------ |
| **400** | Expected (malformed) | Summary banner / form | Show safe message; validate client-side |
| **401** | Expected (auth) | Auth flow/modal | Trigger refresh (single-flight) or redirect to login preserving intent (see Ch38) |
| **403** | Expected (forbidden) | Page/state message | Explain permission; link to upgrade/contact |
| **404** | Expected (not found) | Empty/error state | Friendly message, navigation back/home |
| **409** | Expected (conflict) | Field or summary | Map to conflicting field or show resolution options |
| **422 + invalid_params** | Expected (validation) | Field errors + summary | Map to fields by path; preserve input |
| **429 + Retry-After** | Expected (rate limited) | Inline countdown + disabled action | Honor `Retry-After`; retry after time |
| **408/timeout** | Expected/recoverable | Retry card | Scoped retry with backoff |
| **5xx/503** | Often unexpected/recoverable | Fallback/retry or boundary | Retry with jitter; escalate if repeated |
| **NetworkError/offline** | Recoverable | Offline banner | Retry when online; queue if safe/idempotent |

## Boundary Placement Guide

| Subtree | Boundary | Reset keys | Notes |
| ------- | -------- | ---------- | ----- |
| **Critical widget (optional)** | Component | Route/id/filters | Preserve surrounding context (**ExportJob** chart) |
| **Route view** | Page | `pathname`/route params | Keep app shell/nav alive |
| **Global bootstrap** | App | Rare (manual) | Last resort; report `errorId`; offer reload |
| **Third-party embed** | Component | External id | Isolate completely |

## React Error Boundary Limits (Quick)

| Error type | Caught? | Fix |
| ---------- | ------- | --- |
| Render/lifecycle/constructor | **Yes** | Boundary |
| Event handlers | **No** | `try/catch` |
| Async (`useEffect`, promises) | **No** | `try/catch` + state→throw or classify |
| `setTimeout/setInterval` | **No** | `try/catch` |
| SSR | **Framework dependent** | Framework handlers |
| Outside React tree | **No** | `window.onerror` / `onunhandledrejection` |

## Recovery Matrix

| Failure | Recoverable? | Action | State |
| ------- | ------------ | ------ | ----- |
| **Field validation** | Yes | Inline mapping | Preserve inputs |
| **Offline/network** | Yes | Retry when online | Preserve work |
| **429** | Yes | Wait for Retry-After | Disable action temporarily |
| **Widget render throw** | Yes (scoped) | Boundary retry | Preserve rest of page |
| **Optimistic mutation fail** | Yes if reversible | **Rollback** | Restore previous state |
| **Non-idempotent charge fail** | No auto-retry | Show error, don't retry blindly | Correct state |
| **Cache corruption/invariant** | No | Clear affected keys/reload | Safe fallback + errorId |
| **Repeated boundary crashes** | No | Escalate | Unrecoverable fallback |

## Cheat Sheet

- **Expected vs unexpected:** contract-driven
- **Boundaries:** smallest scope that can recover
- **Cancellation:** abort + ignore `AbortError`
- **Optimism:** snapshot + rollback + idempotency
- **Forms:** server is source of truth, map to fields
- **Safety:** diagnostics separate, no PII, errorId for support

## Related

- [Chapter 37 README](../README.md)
- [Chapter 38 — Full-Stack Error Contracts](../../38-full-stack-error-contracts/README.md)
- [Part XI — Retry and Resilience](../../../part-11-retry-and-resilience/README.md)
