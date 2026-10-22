# Chapter 10 — Do's and Don'ts

> Part IV · Chapter 10 · All sections 10.1–10.17

A condensed rule set for centralized and distributed error handling. Use it as a review checklist.

## Central vs local

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Centralize mechanics: serialize, correlate, redact, safety-net | Centralize business decisions (retry, compensate, degrade) |
| Recover locally where the context lives | Ask the global handler "what should we do?" |
| Keep the global handler under a ~30-line budget | Let it accumulate one `if` per incident |
| Answer unknown errors with `500` + correlation ID | Convert unknown errors into `200` "success" |

## Mechanisms

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give each mechanism one job (middleware preconditions, filter serialization, utilities) | Stack middleware, interceptor, filter, and decorator on the same error |
| Keep serializers/redaction as pure utilities | Bury them in a framework filter class |
| Check `headersSent` before writing | Write twice after headers left |
| Register preconditions outermost, the filter last | Register the error filter before routes |
| Make decorator wrap order an explicit review item | Stack decorators with no stated wrap order |

## Limits of the global handler

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Map registered codes → status in the center | Branch on `err.message` text |
| Put optional-feature fallbacks at the feature boundary | Return friendly defaults that hide outages |
| Audit central files for `retry|refund|compensate|tenant.plan` | Assume the handler stays pure by itself |
| Keep saga/compensation steps in the application layer | Refund inside the error filter |

## Coupling and module size

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep the error kernel free of feature imports | Import domain types into the kernel |
| Let features register their own codes | Maintain one giant code switch |
| Enforce dependency direction and unique codes in CI | Trust review alone |
| Deprecate codes through the registry | Ship `Foo2` to dodge review |

## Contracts across modules and services

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Publish one versioned contract artifact | Copy status tables into each repo |
| Classify unknown remote codes by status class | Crash or `200`-swallow on unknown codes |
| Propagate one correlation ID across all hops | Mint a new ID per service |
| Treat `retryable` as contract surface | Change retryability in an unversioned hotfix |
| Design for N/N-1/N-2 version skew | Assume lockstep deploys |

## Anti-patterns in the wild

1. **The Oracle Filter** — 400 lines of business logic in the global handler.
2. **The Silent Ack** — `200` returned for transient webhook failures; data vanishes.
3. **The Double Writer** — middleware and filter both serialize; clients see corrupt bodies.
4. **The God Module** — `core/errors.ts` imports half the app and blocks every PR.
5. **The Copied Table** — four services, four status maps, four drift timelines.
6. **The Version-Blind Consumer** — unknown code ⇒ crash or swallow, no status-class fallback.
7. **The Retry Decoration** — a decorator that retries outside the idempotency boundary.

## Chapter checklist

- [ ] Global handler has zero business branches (grep-verified).
- [ ] Exactly one layer writes each error response body.
- [ ] Streaming/mid-flight failures have documented abort semantics.
- [ ] Error kernel imports no feature modules (lint-enforced).
- [ ] Codes, statuses, and retryability come from one published artifact.
- [ ] Every consumer tolerates unknown codes by status class.
- [ ] Correlation IDs cross every hop unchanged.

## Related

- [Chapter 10 Reference](../05-reference/README.md)
- [Chapter 21 — API Boundary and Middleware](../../../part-08-http-and-api/21-api-boundary-and-middleware-error-handling/README.md)
- [Chapter 46 — Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
