# Chapter 25 — Third-Party API Error Handling

> Part X · _Estimated reading time: 50–60 min_  
> **Prerequisite:** [Part VI — Error Boundaries and Translation](../../part-06-boundaries-and-translation/README.md), [Part VIII — HTTP and API Error Handling](../../part-08-http-and-api/README.md)

## One-sentence summary

**Translate provider-specific failures into a stable internal error model at the integration boundary** so that **Acme SaaS** can call **Stripe** (or swap vendors) without leaking vendor coupling into **Checkout**, **WebhookIngest**, or domain logic.

## Why this chapter matters

Third-party APIs fail in ways your own code does not: they return vendor-shaped error JSON, use different status semantics, throttle with `Retry-After`, may return 200 with an "error" body, or behave differently across versions. If you propagate raw vendor errors, you cannot enforce a consistent retry policy, you risk leaking sensitive details, and swapping providers becomes a rewrite.

## Learning objectives

By the end of this chapter you can:

- **Classify** upstream failures (HTTP errors, auth, rate limits/quotas, timeouts, connectivity, malformed/unexpected responses, degradation, version incompatibility).
- **Translate** provider payloads to internal codes with preserved retry/recoverability metadata.
- **Avoid** vendor coupling by isolating mapping in adapters.
- **Decide** fallback behavior for optional vs critical dependencies.
- **Handle** vendor outages deliberately with replaceable adapters and safe failure paths.

## Chapter map (files and coverage)

| File | Subsections (from TOC) | What you learn |
| ---- | ----------------------- | -------------- |
| [`01-concepts/01-classifying-upstream-failures.md`](./01-concepts/01-classifying-upstream-failures.md) | 25.1, 25.2, 25.3, 25.8, 25.9 | Classify by origin: HTTP, provider payload shape, timeouts, connection failures. |
| [`01-concepts/02-auth-rate-limits-quotas-and-billing.md`](./01-concepts/02-auth-rate-limits-quotas-and-billing.md) | 25.4, 25.5, 25.6, 25.7 | Invalid/expired credentials, `429` + `Retry-After`, quota/billing failures and their semantics. |
| [`01-concepts/03-malformed-responses-versioning-degradation.md`](./01-concepts/03-malformed-responses-versioning-degradation.md) | 25.10, 25.11, 25.12, 25.13 | Malformed/unexpected formats, version incompatibility, and graceful degradation. |
| [`01-concepts/04-translation-adapters-and-outages.md`](./01-concepts/04-translation-adapters-and-outages.md) | 25.14, 25.15, 25.16, 25.17, 25.18, 25.19, 25.20 | Translate to internal codes, avoid vendor coupling, misleading status codes, fallbacks, critical dep failure, vendor outages, replaceable adapters. |
| [`02-deep-dive/01-provider-error-translation-mechanics.md`](./02-deep-dive/01-provider-error-translation-mechanics.md) | 25.3, 25.14, 25.15 | Mapping tables, normalization, preserving `cause`, and avoiding info loss. |
| [`02-deep-dive/02-misleading-status-codes-and-200-errors.md`](./02-deep-dive/02-misleading-status-codes-and-200-errors.md) | 25.2, 25.16 | When providers return 200 with error bodies; correct internal classification. |
| [`02-deep-dive/03-adapters-vendor-outages-and-replaceability.md`](./02-deep-dive/03-adapters-vendor-outages-and-replaceability.md) | 25.17, 25.18, 25.19, 25.20 | Fallback strategies, failing safely, outage playbooks, adapter interfaces. |
| [`03-practical-examples/01-stripe-error-mapping-adapter.md`](./03-practical-examples/01-stripe-error-mapping-adapter.md) | 25.2, 25.3, 25.6, 25.14, 25.15 | Worked example: translate Stripe errors to `AcmeError` codes with retry metadata. |
| [`03-practical-examples/02-fallbacks-for-optional-vs-critical-dependencies.md`](./03-practical-examples/02-fallbacks-for-optional-vs-critical-dependencies.md) | 25.17, 25.18 | Optional (e.g. address verification) vs critical (Checkout payment capture) with concrete code. |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all 25.1–25.20 | Rules and anti-patterns. |
| [`05-reference/README.md`](./05-reference/README.md) | all 25.1–25.20 | External API failure handling guide, translation checklist, adapter checklist. |

## Key takeaways

1. **Boundary translation is mandatory.** Map provider shapes to internal codes at the adapter; domain sees only stable errors.
2. **Auth/quotas differ.** `401`/`403` may be misconfigured keys vs permission; `429` needs `Retry-After` and respects retry budgets.
3. **Not all errors are retryable.** `400` validation from provider is usually not; `503`/`504`/`ECONNRESET` often are — but only if idempotent.
4. **200 can be an error.** Some providers return success status with an error body — detect and translate.
5. **Plan for outages.** Critical deps require explicit "fail safely" behavior; optional deps must degrade without corrupting state.

## Exercises

1. **Map Stripe:** For `card_declined`, `expired_card`, `rate_limit`, `api_connection_error`, classify retryability and internal code.
2. **Adapter design:** Write an adapter interface that can swap two providers with no domain changes.
3. **Outage drill:** For **Checkout** payment capture, define fail-safe behavior if Stripe is unavailable for 60s.
4. **Webhook translation:** Translate **WebhookIngest** signature verification failures and malformed provider webhooks.

## Related

- [Chapter 26 — Network and Distributed Communication Errors](../26-network-and-distributed-communication-errors/README.md)
- [Part VI — Error Boundaries and Translation](../../part-06-boundaries-and-translation/README.md)
- [Part XI — Retry Logic and Resilience](../../part-11-retry-and-resilience/README.md)
- [Glossary](../../../GLOSSARY.md)
