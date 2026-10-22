# Chapter 38 — Full-Stack Error Contracts

> Part XIV · _Estimated reading time: 60–80 min_
> **Prerequisite:** [Chapter 37 — Frontend Error Handling](../37-frontend-error-handling/README.md), [Part VIII — HTTP and API Error Handling](../../part-08-http-and-api/README.md)

## One-sentence summary

**One shared contract, two responsibilities:** align taxonomies and codes across backend and frontend, map API errors to UI states/fields, and keep user messages and diagnostics strictly separated across web and mobile.

## Why this chapter matters

When backend and frontend invent their own error vocabularies, every integration becomes guesswork. Field validation becomes "unknown error", auth expiry causes infinite redirects, unknown codes crash flows, and generated clients leak implementation details. For **Acme SaaS** (multi-tenant), **Checkout** (money), and **WebhookIngest** (integrations), a mismatched contract is not cosmetic — it's incorrect user action or lost recovery. A deliberate contract (Problem Details + shared `ErrorCode` + mapping layer) makes the full stack testable and safe.

## Chapter map

This chapter covers 38.1–38.14:

| File | Subsections | What you learn |
| ---- | ----------- | -------------- |
| [01-concepts/01-aligning-taxonomies-shared-codes.md](./01-concepts/01-aligning-taxonomies-shared-codes.md) | 38.1–38.2 | Align taxonomies, shared codes, ownership, stability |
| [01-concepts/02-mapping-api-to-ui-and-validation-to-fields.md](./01-concepts/02-mapping-api-to-ui-and-validation-to-fields.md) | 38.3–38.4 | API→UI mapping, validation→field mapping, defaults |
| [01-concepts/03-unknown-codes-version-incompatibility.md](./01-concepts/03-unknown-codes-version-incompatibility.md) | 38.5–38.6 | Unknown codes, API version incompatibility, safe fallbacks |
| [01-concepts/04-generated-clients-auth-expiry-redirects.md](./01-concepts/04-generated-clients-auth-expiry-redirects.md) | 38.7–38.9 | Generated clients, auth expiration/refresh, repeated redirects |
| [02-deep-dive/01-optimistic-update-failures-cross-platform.md](./02-deep-dive/01-optimistic-update-failures-cross-platform.md) | 38.10–38.11 | Optimistic update failures across full stack, web/mobile consistency |
| [02-deep-dive/02-localization-diagnostics-vs-user-messages.md](./02-deep-dive/02-localization-diagnostics-vs-user-messages.md) | 38.12–38.13 | Localization, diagnostics vs user messages, PII/safety |
| [02-deep-dive/03-end-to-end-contract-design.md](./02-deep-dive/03-end-to-end-contract-design.md) | 38.14 | End-to-end error contract: shape, versioning, extensibility |
| [03-practical-examples/01-shared-error-code-enum-typescript.md](./03-practical-examples/01-shared-error-code-enum-typescript.md) | 38.2 | Shared `ErrorCode` enum across frontend/backend (TS types) |
| [03-practical-examples/02-api-error-to-form-field-mapping-fullstack.md](./03-practical-examples/02-api-error-to-form-field-mapping-fullstack.md) | 38.3–38.4 | End-to-end mapping: Problem Details → form fields with tests |
| [03-practical-examples/03-auth-expiry-refresh-flow-end-to-end.md](./03-practical-examples/03-auth-expiry-refresh-flow-end-to-end.md) | 38.8–38.9 | HTTP 401 refresh flow: single-flight, queue, original intent, avoid loops |
| [04-dos-and-donts/README.md](./04-dos-and-donts/README.md) | all | Contract do/don't |
| [05-reference/README.md](./05-reference/README.md) | all | End-to-end error contract reference, mapping tables, checklist |

## Learning objectives

By the end you can:

- Define a shared taxonomy and stable `ErrorCode` enum with ownership and change policy.
- Map `application/problem+json` (RFC 9457) to UI states and field-level errors predictably.
- Handle unknown codes, version incompatibility, and generated client drift safely.
- Implement the **HTTP 401 refresh flow** correctly: single-flight refresh, request queue, original request replay, no redirect storms.
- Keep web/mobile behavior consistent, localize safely, and separate diagnostics from user messages.
- Design an end-to-end contract that is extensible without breaking clients.

## Key takeaways

1. **Contract is code.** Treat the error envelope and codes as a published contract; version when breaking.
2. **Map, don't guess.** Frontend must map codes→UI via a pure mapping layer (testable, no string-matching scattered).
3. **401 is a flow.** Refresh token rotation, single-flight, retry the original request once, and if refresh fails redirect to login preserving intent (38.8–38.9).
4. **Unknown ≠ crash.** Fallback to a safe generic message + log diagnostics with `errorId`/traceId (38.5).
5. **Generated clients need discipline.** Wrap generated types, validate at boundary, and map to internal UI models.
6. **Diagnostics separate.** `detail` may be for debugging; user copy comes from i18n keyed by code (38.13).

## Exercises

1. Create a shared `ErrorCode` enum in a `packages/errors` and use it in both API types and React code.
2. Given a Problem Details response with `invalid_params`, render field errors and a summary.
3. Implement 401 single-flight refresh with request queue and original intent preservation.
4. Simulate unknown code and API version incompatibility; verify safe fallbacks.
5. Draft an end-to-end contract doc (shape, version header, codes, deprecation policy).

## Related

- [Chapter 37 — Frontend Error Handling](../37-frontend-error-handling/README.md)
- [Part VIII — HTTP and API Error Handling](../../part-08-http-and-api/README.md)
- [Part XIII — Security-Aware Error Handling](../../part-13-security-aware-error-handling/README.md)
- [Glossary](../../GLOSSARY.md)
