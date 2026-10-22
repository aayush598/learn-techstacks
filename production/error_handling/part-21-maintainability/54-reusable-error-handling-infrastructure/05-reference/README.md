# Chapter 54 — Reference

> Part XXI · Chapter 54 · _Cheat sheets, decision tables, and the infrastructure spec_

## 1. The package spec

| Item | Value |
| ---- | ----- |
| Package | `@acme/errors` |
| Version | `2.2.0` (previous majors: `2.0.0`, `1.4.2`, `1.0.0`) |
| Size | 1,240 lines, 10 modules, 16 exports |
| Configuration points | 0 |
| Vendor dependencies in the core | 0 |
| Consumers | 11 services (3 TypeScript, 4 Python, 2 Go, 2 mixed) |
| Categories | 15 |
| Context allowlist | 16 keys |
| Cause truncation | 4,000 characters |

## 2. Module map

| Module | Lines | Contains |
| ------ | ----- | -------- |
| `core/types.ts` | 165 | `AppError`, `ErrorCategory`, `ErrorMapper`, `RetryPolicy`, `RecoveryPolicy`, `BoundaryContext` |
| `core/factory.ts` | 115 | `createError`, `redact`, `serializeCause` |
| `core/registry.ts` | 90 | `defineRegistry`, `registryEntry`, duplicate guard |
| `core/category-policy.ts` | 65 | `CATEGORY_POLICY` |
| `core/retry.ts` | 95 | `RETRY_POLICIES`, `decideRetry`, `backoffDelay`, `withRetry` |
| `adapters/http.ts` | 160 | `toProblemDetails`, `toAppError` |
| `adapters/jobs.ts` | 135 | `toJobFailure`, `JobFailure` |
| `adapters/pg.ts` | 145 | `postgresMapper` (SQLSTATE) |
| `adapters/stripe.ts` | 160 | `stripeMapper` |
| `adapters/llm.ts` | 110 | `llmMapper` |

## 3. Interface signatures

```ts
export interface ErrorMapper<E = unknown> {
  readonly name: string;
  canMap(err: unknown): err is E;
  map(err: E): AppError;
}

export interface RetryPolicy {
  readonly maxAttempts: number;
  readonly baseDelayMs: number;
  readonly maxDelayMs: number;
  readonly jitter: boolean;
  readonly totalDeadlineMs: number;
  readonly honourRetryAfter: boolean;
}

export interface RecoveryPolicy {
  readonly action: "fail" | "retry" | "degrade" | "compensate" | "terminate" | "resolve_later";
  readonly maxAttempts?: number;
  readonly note?: string;
}

export interface ErrorBoundary<TRequest, TResponse> {
  handle(err: unknown, ctx: BoundaryContext<TRequest>): TResponse;
}
```

## 4. The category table

| Category | HTTP | Public code | Recovery | Retryable |
| -------- | ---- | ----------- | -------- | --------- |
| `validation` | 422 | `VALIDATION_FAILED` | fail | no |
| `business` | 422 | `BUSINESS_RULE_VIOLATION` | fail | no |
| `conflict` | 409 | `CONFLICT` | fail | no |
| `auth` | 401 | `UNAUTHENTICATED` | fail | no |
| `not_found` | 404 | `NOT_FOUND` | fail | no |
| `external_api_permanent` | 502 | `PROVIDER_REJECTED` | fail | no |
| `external_api_transient` | 503 | `DEPENDENCY_UNAVAILABLE` | retry | yes |
| `external_api_ambiguous` | 202 | `RESOLUTION_PENDING` | resolve_later | no |
| `database_transient` | 503 | `DATABASE_UNAVAILABLE` | retry | yes |
| `data_integrity` | 500 | `INTERNAL_ERROR` | terminate | no |
| `dependency_unavailable` | 503 | `DEPENDENCY_UNAVAILABLE` | degrade | yes |
| `resource_exhausted` | 503 | `RESOURCE_EXHAUSTED` | degrade | yes |
| `rate_limit` | 429 | `RATE_LIMITED` | fail | yes |
| `cancellation` | 499 | `CLIENT_CLOSED_REQUEST` | fail | no |
| `internal` | 500 | `INTERNAL_ERROR` | fail | no |

## 5. Retry table

| Category | Attempts | Base delay | Max delay | Deadline | Honours `Retry-After` |
| -------- | -------- | ---------- | --------- | -------- | --------------------- |
| `external_api_transient` | 3 | 250 ms | 4 s | 10 s | yes |
| `database_transient` | 3 | 100 ms | 1 s | 5 s | no |
| `dependency_unavailable` | 2 | 500 ms | 2 s | 6 s | yes |
| `rate_limit` | 2 | 1 s | 5 s | 15 s | yes |
| everything else | 1 | — | — | — | — |

## 6. Change classification

| Change | Bump | Examples |
| ------ | ---- | -------- |
| New code registered | MINOR | `checkout.CARD_DECLINED` added |
| New category with a new status | MAJOR | `external_api_ambiguous` added |
| New adapter | MINOR | `llmMapper` added |
| New optional argument | MINOR | `createError(..., { meta })` |
| Status of an existing category changes | MAJOR | `rate_limit` 429 → 503 |
| Public message changes | MAJOR | `VALIDATION_FAILED` wording |
| A code is removed | MAJOR | `checkout.LEGACY_CODE` removed |
| A code is deprecated (still works) | MINOR | `since: 2.0.0`, `deprecated: 3.0.0` |
| Typo in a comment, internal refactor | PATCH | — |

## 7. Deprecation rules

| Rule | Value |
| ---- | ----- |
| Minimum life before deprecation | 2 minor releases |
| Minimum life after deprecation | 2 minor releases |
| Removal version | The next MAJOR after the deprecation |
| Telemetry | Per-code usage counts published each release |
| Notice | A `console.warn` at use time, plus a CI check for new uses |
| Migration note | A before → after table in the release notes |

## 8. Decision table — what goes where

| You need to… | Put it in | Never in |
| ------------- | --------- | ------- |
| A new failure mode | Your registry | The package core |
| A new status | A proposed category | A local status literal |
| A vendor mapping | An adapter | The core |
| A retry policy for a category | The package (propose it) | A call site |
| A retry policy for one operation | Your service | The package |
| The user-facing wording | The registry row | The response builder |
| Extra non-sensitive fields | `meta` | The error's top level |
| A secret | Nowhere — redact it | The context |

## 9. Public body fields

| Field | Type | Present |
| ----- | ---- | ------- |
| `type` | URI | always |
| `title` | string | always |
| `status` | number | always |
| `detail` | string | always |
| `instance` | string | when a path is known |
| `code` | string | always |
| `request_id` | string | always at an HTTP boundary |

Never present: `stack`, `cause`, the internal `message`, table names, vendor payloads.

## 10. Job failure fields

| Field | Type | Notes |
| ----- | ---- | ----- |
| `status` | `failed` \| `retryable` \| `dead_lettered` | exactly one |
| `code` | string | the registered code |
| `category` | string | one of the 15 |
| `reason` | string | internal message, for the log |
| `attempts` / `maxAttempts` | number | the attempt budget |
| `retryAt` | ISO-8601 | only when `status: retryable` |
| `cause` | object | name, message, code, truncated |
| `occurredAt` | ISO-8601 | when the error was created |

## 11. Standards referenced

| Standard | Used for |
| -------- | -------- |
| RFC 9457 (Problem Details for HTTP APIs) | the public body shape |
| RFC 6585 | the `499` client-closed-request status |
| PostgreSQL SQLSTATE | the `pg` adapter's codes (`23505`, `40001`, `40P01`, `08006`, `57014`) |
| HTTP `Retry-After` | the rate-limit and transient backoff hint |
| gRPC status codes | the mapping target for the LLM adapter |
| Semantic Versioning 2.0.0 | the package's change classification |

## 12. Starter template spec

| Item | Value |
| ---- | ----- |
| Files | 11 (plus 2 config files) |
| Lines | ~430 |
| Adoption time | 2 h 40 m median, 4 h ceiling |
| Wiring | 3 lines in `src/platform/errors.ts` |
| Version | `templates/minimal-service@2.1.0` |
| Re-sync | annually, ~40-line diff per project |
| Customization rules | 7 (C1–C7) |

## 13. Review checklist

- [ ] Core imports no vendor SDK, no web framework.
- [ ] Export surface ≤ 25 symbols.
- [ ] Category table is total; every category has a status, code, recovery, retryability.
- [ ] Factory redacts by allowlist; cause is truncated at 4,000 characters.
- [ ] Unregistered codes throw at creation.
- [ ] Every adapter has a timeout, a retry policy, and a fallback.
- [ ] HTTP body has 7 fields and no stack trace.
- [ ] Job failure has a fixed field set and 3 statuses.
- [ ] The change is classified; breaking changes ship a migration table.
- [ ] Deprecated codes survive 2 minor releases; usage telemetry is published.

## Related

- [Chapter 54 — Reusable Error-Handling Infrastructure](../README.md)
- [Do / Don't](../04-dos-and-donts/README.md)
- [The `@acme/errors` Package Skeleton](../03-practical-examples/01-the-acme-errors-package-skeleton.md)
