# Chapter 37 — Frontend Error Handling

> Part XIV · _Estimated reading time: 70–90 min_
> **Prerequisite:** [Part VIII — HTTP and API Error Handling](../../part-08-http-and-api/README.md), [Part VII — Validation and Business Errors](../../part-07-validation-and-business-errors/README.md)

## One-sentence summary

**Treat the browser as an unreliable environment:** classify failures as *expected vs unexpected*, place error boundaries at the right scope, and translate every failure into a safe, recoverable UI state rather than leaking a stack trace to end users.

## Why this chapter matters

Frontend failures behave differently than backend: renders can throw, async rejections never reach a parent component, navigation cancels in-flight requests, networks drop, and optimistic updates mutate local state before the server confirms. The wrong split (crash the entire page for a field error, or silently swallow a render bug) creates churn, lost work, and corrupted state. With **Acme SaaS**, **Checkout**, **ExportJob**, **WebhookIngest**, and **AgentRun**, the cost is visible: a lost cart at Checkout, a broken export list in ExportJob, or a tool failure in AgentRun surfaced as "Unknown error" with no retry.

## Chapter map

This chapter covers 37.1–37.22. Grouped as specified:

| File | Subsections | What you learn |
| ---- | ----------- | -------------- |
| [01-concepts/01-expected-vs-unexpected.md](./01-concepts/01-expected-vs-unexpected.md) | 37.1 | Classify expected/unexpected; UX vs crash boundary |
| [01-concepts/02-boundaries-component-page-app.md](./01-concepts/02-boundaries-component-page-app.md) | 37.2–37.4 | Where to put boundaries, scope, blast radius |
| [01-concepts/03-recoverable-vs-unrecoverable-ui.md](./01-concepts/03-recoverable-vs-unrecoverable-ui.md) | 37.5–37.6 | Design recovery affordances per surface |
| [01-concepts/04-forms-api-validation-mapping.md](./01-concepts/04-forms-api-validation-mapping.md) | 37.7–37.8 | Form validation vs API errors, mapping errors→fields |
| [01-concepts/05-network-timeouts-cancellation.md](./01-concepts/05-network-timeouts-cancellation.md) | 37.9–37.11 | Network failures, timeouts, AbortController, navigation cancellation |
| [02-deep-dive/01-stale-data-refresh-optimistic-rollback.md](./02-deep-dive/01-stale-data-refresh-optimistic-rollback.md) | 37.12–37.13 | Stale data, refresh strategy, optimistic rollback mechanics and limits |
| [02-deep-dive/02-pagination-scroll-uploads-downloads-realtime.md](./02-deep-dive/02-pagination-scroll-uploads-downloads-realtime.md) | 37.14–37.16 | Infinite scroll/pagination, uploads/downloads, real-time connections (reconnect/backpressure) |
| [02-deep-dive/03-state-transitions-retry-notifications-corruption.md](./02-deep-dive/03-state-transitions-retry-notifications-corruption.md) | 37.17–37.20 | Safe state transitions, retry/recovery controls, dedupe notifications, preventing UI corruption |
| [02-deep-dive/04-render-failures-and-outside-boundaries.md](./02-deep-dive/04-render-failures-and-outside-boundaries.md) | 37.21–37.22 | React error boundary mechanics and limits; errors outside boundaries (async/events/SSR/setup) |
| [03-practical-examples/01-react-error-boundary-retry-tsx.md](./03-practical-examples/01-react-error-boundary-retry-tsx.md) | 37.21, 37.5, 37.18 | React error boundary + retry UI in TSX; recoverable surface |
| [03-practical-examples/02-api-error-to-form-field-mapping.md](./03-practical-examples/02-api-error-to-form-field-mapping.md) | 37.7–37.8 | API error → form field mapping with typed error envelope |
| [03-practical-examples/03-shared-error-code-enum-frontend-backend.md](./03-practical-examples/03-shared-error-code-enum-frontend-backend.md) | 37.8, 38.* cross-ref | Shared error-code enum across frontend/backend (typed contracts) |
| [04-dos-and-donts/README.md](./04-dos-and-donts/README.md) | all | Frontend-specific do/don't checklist |
| [05-reference/README.md](./05-reference/README.md) | all | Mapping API errors→UI states, boundary placement guide, recovery matrix |

## Learning objectives

By the end you can:

- Classify every frontend failure as expected/unexpected and pick the right surface.
- Place boundaries at component/page/app with correct blast radius and recovery.
- Implement safe optimistic updates with rollback, cancellation with AbortController, retry with backoff, and stale-data refresh.
- Map API errors to form fields and render safe user messages without leaking internals.
- Prevent duplicate toasts, corrupted caches, and infinite retry storms.
- Handle render failures and everything error boundaries do *not* catch.

## Key takeaways

1. **Expected ≠ trivial.** Expected failures belong in the flow (inline validation, empty/error states) — do not throw to break the tree.
2. **Boundaries have limits.** React error boundaries catch render/lifecycle errors in the tree below; they do **not** catch async callbacks, event handlers, SSR, or code outside render. Treat those separately (37.21–37.22).
3. **Cancellation is correctness.** Navigation aborts requests; you must ignore stale responses and avoid setting state after unmount/abort (AbortController + isMounted guard or cleanup).
4. **Optimism needs rollback.** Store previous state, revert on failure, reconcile with server (37.13). Never assume success.
5. **Notifications must be deduped.** One actionable message per root cause; avoid toast spam on retries (37.19).
6. **State transitions must be total.** Every request moves through `idle|loading|success|error` with explicit transitions and no partial, corrupted UI states (37.17, 37.20).

## Exercises

1. Map your app tree: mark one component boundary, one page boundary, one app boundary and justify recoverability for each.
2. Reproduce AbortController on route change in a list view (ignore stale responses).
3. Implement an optimistic toggle with rollback for Acme SaaS "favorite project".
4. Build a small form: API returns field-level errors → map to inputs; unknown codes → global toast.
5. Simulate a render throw and verify boundary retry clears local state safely.

## Related

- [Chapter 38 — Full-Stack Error Contracts](../38-full-stack-error-contracts/README.md)
- [Part VIII — HTTP and API](../../part-08-http-and-api/README.md)
- [Part XI — Retry and Resilience](../../part-11-retry-and-resilience/README.md)
- [Glossary](../../GLOSSARY.md)
