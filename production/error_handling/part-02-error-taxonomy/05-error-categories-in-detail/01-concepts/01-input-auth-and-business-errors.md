# Input, Auth, and Business Categories (5.1–5.9)

> Part II · Chapter 5 · Sections 5.1–5.9 · _Estimated reading time: 30 min_
> **Prerequisite:** [Chapter 4 — Designing a Comprehensive Error Taxonomy](../README.md)

## In one sentence

The first family covers the failures a well-behaved client is *supposed* to be able to fix —
**validation, parsing, authentication, authorization, business rules, not found, conflict,
duplicate operations, and invalid state transitions** — all permanent, all non-retryable, all
typically `4xx`.

## Why this matters in production

These categories are the **public contract** of your API. Getting them wrong produces the classic
SaaS complaints: `500` for a bad field, `401` where `403` was expected, retried `409`s that create
duplicates, and `403`s that leak the existence of other tenants' data. They are also the highest-
volume errors you will ever see, so their cost-per-error matters.

## 5.1 Validation

**Validation** means the request is well-formed but violates a rule: required field missing, type
wrong, out of range, bad format, cross-field inconsistency.

| Aspect | Value |
| ------ | ----- |
| HTTP | `422` (or `400` for some groups) |
| Retry | **never** — same input fails forever |
| Alert | none (business/expected) |
| Disclosure | safe field details; never echo raw input unsanitized |

```json
{
  "type": "https://acme.example/errors/validation",
  "title": "Validation failed",
  "status": 422,
  "code": "VALIDATION_REQUIRED_FIELD",
  "errors": [{ "field": "dateFrom", "code": "VALIDATION_REQUIRED_FIELD" }]
}
```

Validation is *syntactic vs semantic* (Chapter 17). Keep the code stable and field-scoped; the
human message is a presentation concern.

## 5.2 Request parsing

**Parsing** failures happen *before* validation: malformed JSON, wrong `Content-Type`, wrong
encoding, oversized body, duplicate headers.

| Trigger | Status | Code |
| ------- | ------ | ---- |
| malformed JSON | `400` | `REQUEST_MALFORMED_JSON` |
| unsupported media type | `415` | `REQUEST_UNSUPPORTED_MEDIA_TYPE` |
| payload too large | `413` | `REQUEST_PAYLOAD_TOO_LARGE` |

Parsing errors are **produced by the transport layer**, not the domain. They must not reach
business code; the framework/edge maps them (Chapter 21).

## 5.3 Authentication

**Authentication** establishes *who* the caller is: missing credentials, invalid token, expired
session, revoked key.

| Trigger | Status | Header |
| ------- | ------ | ------ |
| no credentials | `401` | `WWW-Authenticate: Bearer` |
| invalid/expired token | `401` | `WWW-Authenticate: Bearer error="invalid_token"` |
| revoked session | `401` | same |

> ⚠️ **Never distinguish "unknown user" from "wrong password."** Return one code
> (`AUTH_INVALID_CREDENTIALS`) to prevent **user enumeration** (Chapter 35).

Authentication errors are `SENSITIVE`: log the reason internally, but the public body must be
uniform.

## 5.4 Authorization / permission

**Authorization** is about *what* an authenticated caller may do: missing scope, wrong role,
wrong tenant, ownership violation.

| Trigger | Status | Code |
| ------- | ------ | ---- |
| insufficient scope | `403` | `AUTHZ_INSUFFICIENT_SCOPE` |
| not the owner | `403` / `404` | `AUTHZ_NOT_OWNER` |
| cross-tenant access | `404` | `RESOURCE_NOT_FOUND` (deliberate) |

Choose `404` over `403` when **existence itself is sensitive** — leaking "this tenant's project
exists" is a real disclosure. Record the true category internally; return a normalized code.

## 5.5 Business rule

A **business rule** failure is a legitimate domain outcome, not a bug: card declined, seat taken,
trial expired, insufficient balance, plan does not allow the feature.

| Example | Status | Code |
| ------- | ------ | ---- |
| card declined | `422` | `BUSINESS_CARD_DECLINED` |
| insufficient balance | `422` | `BUSINESS_INSUFFICIENT_FUNDS` |
| plan limit | `402`/`403` | `BUSINESS_PLAN_REQUIRED` |

Business errors are **not alerts**. They are expected, often high-volume, and should log at
`info`/`warn` (Chapter 57 covers validation/business at scale).

## 5.6 Not found

A resource does not exist (or the caller cannot see it).

| Aspect | Value |
| ------ | ----- |
| HTTP | `404` |
| Retry | never |
| Code | `RESOURCE_NOT_FOUND`, `RESOURCE_GONE` (`410`) |

Distinguish **not found** (`404`, may exist later) from **gone** (`410`, permanently removed).
Never return `200` with `null` for a missing singular resource — it confuses clients and caching.

## 5.7 Conflict

The request conflicts with the **current state** of a resource: version mismatch, already exists,
concurrent edit, illegal removal.

| Trigger | Status | Code |
| ------- | ------ | ---- |
| version mismatch | `409` | `CONFLICT_VERSION_MISMATCH` |
| resource already exists | `409` | `CONFLICT_ALREADY_EXISTS` |
| dependency prevents delete | `409` | `CONFLICT_HAS_DEPENDENTS` |

Conflict is **permanent** and non-retryable without new information (a fresh version). Optimistic
locking uses `ETag` + `If-Match` and can return `412 Precondition Failed`.

## 5.8 Duplicate operation

A **duplicate** is the same operation submitted twice: a retried payment, a replayed webhook, a
double-submitted form.

| Situation | Correct behavior |
| --------- | ---------------- |
| same idempotency key, same payload | return the **original** result (`2xx`) |
| same idempotency key, different payload | `409` `DUPLICATE_KEY_REUSED` |
| no key, unique constraint hit | `409` `DUPLICATE_RESOURCE` (or `23505` translated) |

This category is the bridge to **idempotency** (Chapter 28). The dangerous anti-pattern is
creating a *new* operation when an old one already succeeded — double billing.

## 5.9 State transition

An operation is **invalid for the current state** of the entity: cancel an already-shipped order,
refund a refunded charge, resume a completed export.

| Trigger | Status | Code |
| ------- | ------ | ---- |
| cancel shipped order | `409` | `STATE_INVALID_TRANSITION` |
| refund refunded charge | `409` | `STATE_INVALID_TRANSITION` |
| start running export | `409` | `CONFLICT_OPERATION_IN_PROGRESS` |

State machines belong in the domain; the error names the transition, not the implementation. This
category is where "exceptions as business flow" most often goes wrong (Chapter 18).

## Worked example — `POST /v1/exports`

```text
missing dateFrom            → 5.1 validation              → 422 VALIDATION_REQUIRED_FIELD
dateFrom > dateTo           → 5.1 validation              → 422 VALIDATION_RANGE_INVERTED
tenant already at limit     → 5.5 business rule           → 402 BUSINESS_PLAN_REQUIRED
export already running      → 5.9 state transition        → 409 CONFLICT_OPERATION_IN_PROGRESS
retried request w/ same key → 5.8 duplicate operation     → 200 (replay original)
```

Five outcomes, one endpoint, five different categories and codes — all `4xx`, all non-retryable.

## Key data / numbers

- `400` vs `422`: syntactic failure uses `400`; semantically valid but rule-violating uses `422`.
- `401` requires `WWW-Authenticate`; `403` means authenticated but not permitted.
- PostgreSQL `23505` `unique_violation` maps to **duplicate operation**; `23503`
  `foreign_key_violation` on delete maps to **conflict** (`CONFLICT_HAS_DEPENDENTS`).
- `410 Gone` marks permanent removal; `404` may reappear.

## Real-world use case — Acme SaaS (login + exports)

Acme's login returned "user not found" vs "wrong password", enabling enumeration. Mapped to a
single `AUTH_INVALID_CREDENTIALS` `401`. Separately, a retried `POST /exports` created duplicate
CSVs; Acme adopted idempotency keys so the second request **replays** the first (`200`) instead of
hitting `409`. Both fixes were classification fixes, not new endpoints.

## Trade-offs

| Choice | Pros | Cons |
| ------ | ---- | ---- |
| Distinct `401`/`403`/`404` | Precise clients | May leak existence |
| Uniform `404` for hidden resources | No disclosure | Loses client precision |
| `409` for conflicts | Correct semantics | Clients must handle it |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use `422` for rule violations | Return `500` for bad input |
| Normalize auth failures | Reveal user existence |
| Replay idempotent duplicates | Re-execute a completed payment |
| Model state transitions explicitly | Throw a generic error on bad state |

## Common mistakes

- **Retrying a `409`/`422`/`401`.** All are permanent.
- **`403` where existence is secret.** Prefer `404`.
- **Treating duplicates as errors** when replay is correct.
- **Encoding state rules in the transport**, not the domain.

## Checklist

- [ ] Are validation details field-scoped and stable?
- [ ] Are parsing failures handled by the transport layer?
- [ ] Is authentication uniform to prevent enumeration?
- [ ] Are duplicates collapsed via idempotency?
- [ ] Are state transitions domain-owned?

## Related

- [Limits, Concurrency, and Data Categories](./02-limits-concurrency-and-data.md)
- [Category Interactions and Overlaps](../02-deep-dive/01-category-interactions-and-overlaps.md)
- [Input Validation Error Handling](../../../part-07-validation-and-business-errors/17-input-validation-error-handling/README.md)
- [HTTP Error Semantics](../../../part-08-http-and-api/19-http-error-semantics/README.md)
