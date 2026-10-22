# Chapter 38 — Do's and Don'ts (Full-Stack Error Contracts)

> Part XIV · Chapter 38 · Section 04 · _Estimated reading time: 12 min_

## Contract & Codes

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use RFC 9457 Problem Details + shared `ErrorCode` enum | Invent per-service error vocabularies |
| Treat codes as published contract; additive + deprecate | Rename/change code meaning without versioning |
| Share types via internal package/monorepo | Duplicate enum definitions |
| Use contract tests to prevent drift | Rely on English message equality |

## Mapping & UX

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Map via pure function `(ProblemDetails) -> UiAction[]` | Scatter `if (err.code)` across components |
| Map `invalid_params` to fields, cross-field to summary | Put every error on arbitrary field or only summary |
| Localize by code with safe fallbacks | Render `detail` verbatim to users |
| Handle unknown codes safely with `error_id` | Crash on unknown code/field |
| Separate diagnostics from user messages | Leak stacks/PII to UI |

## Auth, Clients, Versioning

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Wrap generated clients at boundary; normalize errors | Let generated types leak everywhere |
| Single-flight refresh + queue + replay once on 401 | Parallel refreshes or infinite retry loops |
| Preserve intent with `return_to` on redirect | Redirect to login without preserving path/cart |
| Guard redirects (flag + pathname check) | Create redirect storms |
| Version on breaking envelope changes | Break old clients silently |

## Cross-Platform & Safety

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Consistent mapping for web/mobile | Different semantics per platform |
| Idempotency keys for state-changing ops | Optimistic charge without rollback/idempotency |
| Reconcile on optimistic failure | Leave optimistic state after final failure |
| Forward-compatible parsing (ignore unknown fields) | Fail on extra fields |

## Quick Checklist

- [ ] Shared envelope + codes adopted
- [ ] Central mapper with i18n
- [ ] 401 refresh flow correct (single-flight/queue/replay-once)
- [ ] Unknown/version incompatibility handled safely
- [ ] Diagnostics correlated with `error_id`/traceId
- [ ] Contract tests in CI

## Related

- [Chapter 38 README](../README.md)
- [Chapter 37 — Frontend Error Handling](../../37-frontend-error-handling/README.md)
- [Part VIII — HTTP and API](../../../part-08-http-and-api/README.md)
