# Translation, Adapters, and Outages

> Part X · Chapter 25 · Sections 25.14, 25.15, 25.16, 25.17, 25.18, 25.19, 25.20 · _Estimated reading time: 18 min_

## In one sentence

**Translate every upstream failure to a stable internal error at a replaceable adapter boundary** — avoid vendor coupling, don't mislead with status codes, degrade intentionally for optional deps, fail safely for critical deps, and have a plan for vendor outages.

## Why this matters in production

If domain services see `StripeCardError` directly, swapping providers or adding fallbacks becomes invasive. **Checkout** must not know Stripe's field names. **WebhookIngest** must normalize all provider callbacks. When a vendor has an outage, **Acme SaaS** needs predictable behavior (queue, degrade, or fail closed) — not ad-hoc retries that amplify load.

## Core concept

| Area | Goal | Notes |
| ---- | ---- | -----|
| **Translation** | Map vendor → internal codes + metadata | Preserve retryability, `retryAfterSec`, `cause`, safe context. |
| **Avoid vendor coupling** | Adapters isolate vendors | Domain depends on internal interfaces/errors only. |
| **Misleading status codes** | Don't propagate provider status as-is | Translate to correct internal category; map to appropriate API status later (Part VIII). |
| **Fallback for optional deps** | Degrade safely | Use cached/defaults only if non-critical and doesn't corrupt state. |
| **Fail safely when critical dep unavailable** | Fail closed with explicit error | Don't guess; don't bypass checks; return safe error to caller. |
| **Vendor outages** | Plan for regional/outages | Timeouts, circuit breakers, feature flags, queued retries with budgets. |
| **Replaceable adapters** | Swappable implementations | Interface-based; translation tables per vendor; tests against contracts. |

## How it works (mechanics)

### Translation
1. **Classify** (http/payload/network) as before.
2. **Normalize** using vendor-specific mapper → internal error code + severity + retryable + metadata.
3. **Enrich** with safe context (request id, operation, vendor name redacted or internal label).
4. **Preserve cause** (`Error.cause` / chained error) without leaking sensitive payloads.

### Adapters
- **Interface**: `PaymentProvider.charge()`, `StorageProvider.put()`, etc. Returns internal `Result` or throws internal errors.
- **Per-vendor impl**: Stripe adapter, etc., contains all vendor SDK types and mappers.
- **Translation tables**: Map `provider.error.code` → `AcmeErrorCode`.
- **No leakage**: Never export vendor types from adapter interface.

### Outages and fallbacks
- **Optional** (e.g. address validation): On failure → skip validation with warning, log, don't block checkout if policy allows.
- **Critical** (e.g. payment capture for **Checkout**): On failure → fail the operation with `DEPENDENCY_UNAVAILABLE`, don't create order in "paid" state, use idempotency and don't guess.
- **Circuit breaker**: Open after threshold; return fallback or fail fast.
- **Retry budgets**: Prevent retry storms across fleet.

## Worked example — Translation

```ts
// Internal stable error codes (example)
enum AcmeErr {
  UPSTREAM_AUTH_INVALID = "UPSTREAM_AUTH_INVALID",
  UPSTREAM_RATE_LIMITED = "UPSTREAM_RATE_LIMITED",
  UPSTREAM_DECLINED = "UPSTREAM_DECLINED",
  UPSTREAM_UNAVAILABLE = "UPSTREAM_UNAVAILABLE",
  UPSTREAM_TIMEOUT = "UPSTREAM_TIMEOUT",
  UPSTREAM_MALFORMED = "UPSTREAM_MALFORMED",
  UPSTREAM_UNEXPECTED_FORMAT = "UPSTREAM_UNEXPECTED_FORMAT",
}

// Stripe adapter maps to internal
function mapStripe(e: StripeErr): InternalErr {
  if (e.type === "StripeCardError") {
    return new InternalErr(AcmeErr.UPSTREAM_DECLINED, { retryable: false, vendorCode: e.code });
  }
  if (e.type === "StripeRateLimitError") {
    return new InternalErr(AcmeErr.UPSTREAM_RATE_LIMITED, { retryable: true, retryAfterSec: e.retryAfter });
  }
  if (e.type === "StripeConnectionError") {
    return new InternalErr(AcmeErr.UPSTREAM_UNAVAILABLE, { retryable: true });
  }
  if (e.type === "StripeAuthenticationError") {
    return new InternalErr(AcmeErr.UPSTREAM_AUTH_INVALID, { retryable: false });
  }
  // ...
}
```

**Key data:**
- **Stable codes:** Internal codes never change due to vendor renames.
- **Metadata:** `retryable`, `retryAfterSec`, `cause` (chained), `vendor` (internal label only).
- **Never leak:** Don't put full provider JSON in user-facing messages.

## Real-world use case

**Acme SaaS — Swappable payment provider:** Initially using Stripe. Business needs to support another provider. With replaceable adapters and internal error codes, **Checkout** service code doesn't change. The new provider adapter implements the same interface and maps its errors to the same internal codes. Fallback logic for "provider unavailable" works for either provider.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **Pass-through vendor errors** | No translation code | Tight coupling, leaks details, inconsistent policy | **Never** for domain/external APIs |
| **Central translation in one god mapper** | Easy to find | Becomes huge, hard to version per vendor | Avoid; prefer per-vendor mappers in adapters |
| **Per-adapter mappers + stable internal codes** | Clean separation, swappable | More files | **Recommended** |
| **Translate at API boundary only** | Less work | Internal layers still see vendor errors | Insufficient |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Translate at integration boundary (adapter) | Let `StripeError` escape to controllers/domain |
| Use stable internal error codes | Propagate vendor error codes/types as your API |
| Define critical vs optional per dependency | Treat all dependencies the same |
| Fail closed for critical operations on ambiguity | Guess and proceed with side effects |
| Plan for vendor outages (timeouts, breakers, budgets) | Retry forever on provider outage |

## Common mistakes

- **Leaking vendor details:** Returning Stripe's `decline_code` directly to end users without mapping.
- **Misleading status codes:** Converting `429` to internal but returning wrong HTTP status later.
- **Optional→critical creep:** Treating non-critical as critical and blocking entire flows unnecessarily.
- **No replaceability:** Hardcoding vendor logic throughout codebase.
- **Retrying critical ops on outage:** Amplifying load during provider incident.

## Checklist

- [ ] Every third-party call goes through an adapter with translation.
- [ ] Internal error model is vendor-agnostic.
- [ ] Critical vs optional dependencies documented and enforced.
- [ ] Fallback behavior tested; fails closed when unsafe.
- [ ] Outage playbook exists (timeouts, circuit breaker, feature flags).
- [ ] Adapter interface allows swapping vendors without domain changes.

## Related

- [Provider Error Translation Mechanics](../02-deep-dive/01-provider-error-translation-mechanics.md)
- [Adapters, Vendor Outages, and Replaceability](../02-deep-dive/03-adapters-vendor-outages-and-replaceability.md)
- [Stripe Error Mapping Adapter (Example)](../03-practical-examples/01-stripe-error-mapping-adapter.md)
- [Glossary](../../../GLOSSARY.md)
