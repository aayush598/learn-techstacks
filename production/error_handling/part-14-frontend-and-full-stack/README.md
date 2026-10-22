# Part XIV — Frontend and Full-Stack Error Handling

> **Chapters 37–38.** Errors don't stop at the backend boundary. On the frontend, failures must be translated into recoverable UI states; across the full stack, contracts must align so that what the backend classifies is what the UI can act on. This part makes that translation deliberate.

## Learning objectives

By the end of Part XIV you will be able to:

1. Distinguish **expected vs unexpected** frontend failures and route them to appropriate UI surfaces (forms, toasts, error boundaries, offline states).
2. Place error boundaries at the correct scope (**component/page/app**), know their mechanics and hard limits, and design recoverable vs unrecoverable UI.
3. Handle real browser concerns: **network failures, timeouts, AbortController cancellation/navigation**, **stale data/refresh**, **optimistic updates with rollback**, **uploads/downloads**, **infinite scroll/pagination**, **real-time connections**, and **render failures**.
4. Prevent UI corruption: deduplicate notifications, manage state transitions safely, and avoid leaking details or corrupting cached state.
5. Build a **shared error contract** across frontend and backend: shared codes, API→UI mapping, validation→field mapping, unknown code handling, auth expiration/refresh, API version incompatibility, generated clients, and end-to-end error contracts.
6. Keep **diagnostics vs user messages** separated, handle localization carefully, and maintain web/mobile consistency.

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 37 | [Frontend Error Handling](./37-frontend-error-handling/README.md) | Boundaries, expected vs unexpected, forms, network/timeouts, cancellation, optimistic rollback, pagination, uploads, real-time, retries, notifications, render failures |
| 38 | [Full-Stack Error Contracts](./38-full-stack-error-contracts/README.md) | Shared taxonomy/codes, mapping API→UI, validation→fields, auth expiry/refresh, versioning, generated clients, web/mobile, i18n, diagnostics, end-to-end contract |

## How to study this part

- **Read Chapter 37 first.** Treat the browser as a hostile, unreliable environment: offline is normal, not exceptional.
- **Practice boundaries.** Draw your app tree and decide per subtree what is recoverable and what must crash to a boundary.
- **Do Chapter 38 with real types.** Create a shared `ErrorCode` enum and trace a `Problem Details` response all the way to a field error.
- **Test the ugly paths.** Simulate `AbortController` on navigation, token expiry mid-request, slow uploads, and a render throw inside a memoized component.

## Key takeaways

- **Expected failures are UX.** Validation, 401/403, not-found, and rate limits are part of the contract — handle them inline, not as crashes.
- **Unexpected failures need boundaries.** Use React error boundaries for render failures; they do **not** catch async errors, event handlers, or errors in SSR/setup — plan for those separately.
- **Rollback is required for optimism.** Optimistic UI without rollback is a data-consistency bug; pair with idempotency keys and reconciliation.
- **One contract, two views.** Share codes and a mapping layer; keep user-facing copy and telemetry/diagnostics strictly separated.
- **Auth is a flow, not a modal.** 401 must trigger refresh with a single-flight, queue in-flight requests, avoid repeated redirects, and never lose the original intent.

## Related

- [Part VIII — HTTP and API Error Handling](../part-08-http-and-api/README.md)
- [Part VII — Validation and Business Errors](../part-07-validation-and-business-errors/README.md)
- [Part X — External Dependencies](../part-10-external-dependencies/README.md)
- [Part XI — Retry and Resilience](../part-11-retry-and-resilience/README.md)
- [Glossary](../GLOSSARY.md)
