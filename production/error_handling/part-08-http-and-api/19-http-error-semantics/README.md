# Chapter 19 — HTTP Error Semantics

> Part VIII · _Estimated reading time: 70–95 min_
> **Prerequisite:** [Error Codes and Error Registries](../../part-03-error-models/08-error-codes-and-error-registries/README.md)

## One-sentence summary

An HTTP status code is a **machine-readable contract** about what kind of thing went wrong —
and choosing it from a documented table (`400` vs `422`, `401` vs `403`, `409` vs `410`) is
the difference between an API clients can build on and an API they must reverse-engineer.

## Why this chapter matters

Status codes drive client behavior at every layer: SDK retry logic branches on `429`/`503`,
caches key on `404`/`410`, browsers distinguish `401` (redirect to login) from `403` (show
"access denied"), and proxies treat `5xx` differently from `4xx` for health and circuit-breaking.
A wrong code is not a cosmetic bug — it triggers the **wrong machine response**: a retry loop
against permanent failures, cache poisoning, silent success on failure, or a login redirect for
a permission error. This chapter gives you the selection rules so the choice is never ad hoc.

## Chapter map

The chapter has 20 sections. They are grouped into nine files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-status-code-classes-and-selection-table.md`](./01-concepts/01-status-code-classes-and-selection-table.md) | 19.1 | The five status classes, what each promises the client, and the full selection table for this chapter |
| [`01-concepts/02-request-content-errors-400-413-415-422.md`](./01-concepts/02-request-content-errors-400-413-415-422.md) | 19.2, 19.9, 19.10, 19.11 | Parsing vs semantic failures: the `400` vs `422` boundary, oversized payloads, unsupported media types |
| [`01-concepts/03-access-errors-401-403-404-405.md`](./01-concepts/03-access-errors-401-403-404-405.md) | 19.3, 19.4, 19.5, 19.6 | Authentication vs authorization, existence disclosure, wrong-method responses and the `Allow` header |
| [`01-concepts/04-state-and-limit-errors-409-410-429.md`](./01-concepts/04-state-and-limit-errors-409-410-429.md) | 19.7, 19.8, 19.12 | Conflicts, permanent removal, rate limiting and `Retry-After` |
| [`01-concepts/05-server-errors-500-502-503-504.md`](./01-concepts/05-server-errors-500-502-503-504.md) | 19.13, 19.14, 19.15, 19.16 | Which server error is honest: our bug, bad upstream, unavailable dependency, upstream timeout |
| [`02-deep-dive/01-rfc-9110-and-consistent-selection.md`](./02-deep-dive/01-rfc-9110-and-consistent-selection.md) | 19.2, 19.11, 19.19 | RFC 9110 semantics, decision procedure for consistent selection, registry-driven mapping |
| [`02-deep-dive/02-misleading-responses-and-internal-exposure.md`](./02-deep-dive/02-misleading-responses-and-internal-exposure.md) | 19.17, 19.18, 19.20 | Why `200`-for-failure breaks machines, what 4xx must never reveal, avoiding misleading signals |
| [`03-practical-examples/01-status-selection-walkthrough.md`](./03-practical-examples/01-status-selection-walkthrough.md) | 19.1–19.20 applied | Wire-level request/response walkthroughs across the recurring cast |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Status-selection rules of thumb and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | The HTTP status selection guide, decision tree, and chapter glossary |

## Learning objectives

By the end you can:

- Select the correct status code for any 4xx/5xx scenario in under a minute, using one
  documented decision procedure.
- Explain to a teammate why a validation failure is `422` and not `400`, why missing credentials
  are `401` and not `403`, and why a deleted resource is `410` and not `404`.
- Attach the headers each status requires (`Retry-After`, `Allow`, `WWW-Authenticate`) so
  clients and proxies can act automatically.
- Detect and eliminate the two systemic lies: `200` responses that hide failures, and `4xx`
  responses that expose internals.
- Drive status selection from your error registry instead of scattering literal numbers through
  handlers.

## Key takeaways

1. **`4xx` means "the client can fix this by changing the request"; `5xx` means "we broke the
   promise."** Misclassifying one as the other trains clients into wrong retry/UX behavior.
2. **Syntax vs semantics is the `400`/`422` line.** Unparseable JSON is `400`; parseable JSON
   with a negative seat count is `422`. Both are permanent; only the first indicates a broken
   encoder.
3. **`401` is about identity, `403` is about permission.** An expired token is `401` with
   `WWW-Authenticate`; a valid user touching another tenant's project is `403`.
4. **`429` and `503` are the retry-eligible statuses** — and they are the only ones where
   `Retry-After` is load-bearing. Everything else in 4xx is permanent.
5. **`200` for a failure is an API defect**, not a convenience. Machines branch on status;
   giving them a lie to parse creates silent failures in SDKs, caches, and monitors.

## Exercises

1. Take your ten most-returned error responses today. Map each to a row of the selection table
   in `05-reference/README.md`; list every mismatch.
2. For `POST /api/v1/checkout` with a valid token but another tenant's `cartId`, write the exact
   status line, headers, and body you would return — then justify `403` vs `404` in one sentence.
3. A Stripe webhook arrives with a bad signature. Which status? Which status if the body is
   valid but the event type is unknown? Write both responses.
4. Sketch the retry-class column of your error registry: which of your codes map to `429` or
   `503` today, and is each mapping defensible?

## Related

- [Standardized API Error Responses (Ch. 20)](../20-standardized-api-error-responses/README.md)
- [API Boundary and Middleware Error Handling (Ch. 21)](../21-api-boundary-and-middleware-error-handling/README.md)
- [Error Codes and Error Registries](../../part-03-error-models/08-error-codes-and-error-registries/README.md)
- [Glossary](../../GLOSSARY.md)
