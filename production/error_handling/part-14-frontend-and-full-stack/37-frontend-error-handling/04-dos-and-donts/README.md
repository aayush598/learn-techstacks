# Chapter 37 — Do's and Don'ts (Frontend Error Handling)

> Part XIV · Chapter 37 · Section 04 · _Estimated reading time: 12 min_

## Classification & Boundaries

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify as **expected vs unexpected** by API contract (status + `error.code`) | Treat every `Error` instance as "crash the app" |
| Put boundaries at **component/page/app** matching blast radius and recoverability | Wrap entire app in one boundary or over-nest without reason |
| Reset boundaries on route/filter change via `resetKeys` | Leave boundary in permanent fallback after navigation/fix |
| Know React boundary limits: catch render/lifecycle/constructor only | Assume boundaries catch async, event handlers, SSR, or timeouts |

## Forms, API, Network

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Map `422` with `invalid_params` to fields; use summary for cross-field | Clear form inputs on validation errors |
| Preserve user input/state on recoverable failures (**Checkout**, forms) | Reload page for a widget timeout |
| Use **AbortController**; abort on unmount/route change; ignore `AbortError` | Call `setState` after abort/unmount or retry cancellation |
| Set timeouts per flow; honor `Retry-After` for `429` | Let requests hang forever or hammer rate-limited endpoints |
| Treat network/offline/503 as **recoverable** with backoff | Toast "Request failed" with no retry for transient network errors |

## Optimistic UI, State, Notifications

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Snapshot before optimistic mutation; **rollback** on error; reconcile on settle | Optimistically charge cards or do non-reversible ops optimistically |
| Use **idempotency keys** for state-changing POSTs | Retry non-idempotent actions blindly |
| Manage state as `idle\|loading\|success\|error` with explicit transitions | Create partial/corrupted UI states |
| Deduplicate notifications (one actionable message per root cause) | Spam toasts on every retry attempt |
| Cancel related queries on mutation to avoid stale overwrites | Let old GET responses overwrite optimistic state |

## Rendering & Safety

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Handle async/event errors with `try/catch`; route to boundary via state→throw if needed | Let promises reject unhandled |
| Show scoped fallbacks for optional widgets (**ExportJob** chart) | Crash global chrome for non-critical widgets |
| Report with `errorId`, route, component stack; keep user messages safe | Leak stack traces, SQL, URLs, or PII to users |
| Escalate repeated recoverable failures to unrecoverable with support id | Retry forever on corrupted cache/invariants |
| Keep diagnostics and user copy separated | Show raw exception messages verbatim |

## Quick Checklist

- [ ] Every critical flow has recoverable/unrecoverable classification
- [ ] Boundaries scoped correctly with reset strategy
- [ ] All fetches abortable; cancellation non-fatal
- [ ] Optimistic updates have rollback + idempotency where needed
- [ ] Forms map server errors correctly and preserve input
- [ ] Async/event errors explicitly handled
- [ ] Notifications deduplicated
- [ ] Safe telemetry with no PII

## Related

- [Chapter 37 README](../README.md)
- [Chapter 38 — Full-Stack Error Contracts](../../38-full-stack-error-contracts/README.md)
- [Part XI — Retry and Resilience](../../../part-11-retry-and-resilience/README.md)
