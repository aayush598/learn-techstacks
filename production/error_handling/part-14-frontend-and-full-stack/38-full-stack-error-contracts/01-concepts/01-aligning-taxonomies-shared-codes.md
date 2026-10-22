# Aligning Taxonomies and Shared Codes

> Part XIV · Chapter 38 · Sections 38.1–38.2 · _Estimated reading time: 17 min_
> **Prerequisite:** [Frontend Error Handling (Ch37)](../../37-frontend-error-handling/README.md), [HTTP and API Error Handling (Part VIII)](../../../part-08-http-and-api/README.md)

## In one sentence

**Align the backend's failure taxonomy with the frontend's UI taxonomy** by sharing stable machine-readable `error.code` values and a single error envelope (RFC 9457 Problem Details), with explicit ownership and a change policy.

## Why this matters in production

For **Acme SaaS** (multi-tenant), **Checkout** (payments), and **WebhookIngest** (integrations), mismatched taxonomies create "unknown error" and lost recovery paths. Sharing codes means the UI maps deterministically (field/summary/action) instead of guessing from HTTP status or English messages.

## Aligning taxonomies (38.1)

| Concern | Backend taxonomy | Frontend taxonomy | Alignment |
| ------- | ---------------- | ----------------- | --------- |
| **Validation** | Domain/business rules | Form field vs summary | Use `invalid_params` with per-field codes |
| **AuthN/AuthZ** | 401/403 with reasons | Login flow vs permission banner | Share codes (`UNAUTHENTICATED`, `SESSION_EXPIRED`, `UNAUTHORIZED`) |
| **Conflicts** | State conflicts | Actionable UI (resolve/retry) | Code (`CONFLICT`) + context |
| **Rate limits** | `429` + `Retry-After` | Countdown/retry | `RATE_LIMITED` + headers |
| **Infrastructure** | 5xx/transients | Recoverable/fallback | Distinguish transient vs permanent via codes if needed |
| **Business failures** | Quota/entitlement | CTA (upgrade) | Codes like `SEAT_LIMIT_EXCEEDED` |

> **Principle:** The error contract is the boundary translation layer. Backend classifies causes; frontend classifies UI responses — both use the same code set.

## Shared codes (38.2)

**Stability rules:**
- Codes are machine-stable: `UPPER_SNAKE_CASE`, never change meaning.
- Additive by default. Deprecate, don't silently rename.
- Namespace by domain if large (`BILLING_*`, `ORG_*`), but keep flat for core set when practical.
- Versioned when breaking the envelope (see 38.6, 38.14).

## Envelope (RFC 9457)

```json
{
  "type": "https://api.acme.com/errors/validation-failed",
  "title": "Validation failed",
  "status": 422,
  "detail": "One or more fields are invalid",
  "instance": "/orgs",
  "error_id": "err_01HXYZK0VWJNBT6RZ4A7W1ZQ84",
  "code": "VALIDATION_FAILED",
  "invalid_params": [
    {"field": "slug", "code": "SLUG_TAKEN", "message": "This slug is already taken."}
  ]
}
```

**Notes:** `code` is the shared machine code; `error_id` is for support/correlation (separate from PII). `detail` may be developer-oriented or safe; user-facing text must come from frontend i18n keyed by `code` (38.13).

## Ownership & change policy

| Item | Policy |
| ---- | ------ |
| **Code set ownership** | Platform/Errors WG or backend owning the domain |
| **Adding codes** | Reviewed PR; documented (meaning, status, UI action, retryable?) |
| **Deprecation** | Mark in docs, keep for N releases, log usage, no hard removal without API version |
| **Versioning** | Envelope changes require version header or new `/vN` |
| **Unknown codes** | FE must treat as fallback with `error_id` (38.5) |

## Real-world use case — Acme SaaS

Signup returns `code: "EMAIL_TAKEN"` with `field: "email"`. Frontend maps to field error in any client (web/mobile) using the same mapping. No guessing from English strings.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| HTTP-only | Simple | Insufficient for UI actions | Never for complex flows |
| Shared codes + envelope | Deterministic mapping | Requires governance | **Recommended default** |
| Service-specific codes | Decentralized | Drift across services | Only with clear namespaces + contract tests |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Treat error codes as published contract | Rename/change meaning arbitrarily |
| Use additive changes + deprecation | Break clients silently |
| Keep `error_id` separate from user messages | Leak internal details in `detail` to end users |
| Align via contract tests | Rely on string equality of human messages |

## Checklist

- [ ] Single envelope shape (RFC 9457) adopted
- [ ] Shared `ErrorCode` enum/types (monorepo/shared package)
- [ ] Governance documented (owner, review, deprecation)
- [ ] Contract tests cover emitted codes
- [ ] Unknown code fallback defined (38.5)

## Related

- [Mapping API→UI and Validation→Fields](./02-mapping-api-to-ui-and-validation-to-fields.md)
- [Unknown Codes, Version Incompatibility](./03-unknown-codes-version-incompatibility.md)
- [Shared Error Code Enum (Practical)](../../37-frontend-error-handling/03-practical-examples/03-shared-error-code-enum-frontend-backend.md)
- [End-to-End Error Contract (Reference)](../05-reference/README.md)
