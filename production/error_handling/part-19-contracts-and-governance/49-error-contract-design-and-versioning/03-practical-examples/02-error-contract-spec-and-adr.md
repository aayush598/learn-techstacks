# The Error Contract Spec and the ADR That Adopted It

> Part XIX · Chapter 49 · Sections 49.5–49.6, 49.14–49.15 · _Estimated reading time: 20 min_
> **Prerequisite:** [Ownership, Documentation, and Message Independence](../01-concepts/03-ownership-documentation-and-message-independence.md)

## In one sentence

A published error contract is a **versioned artifact with its own catalogue, compatibility
policy, and deprecation process**, and adopting one is an **architecture decision** worth
recording — because the alternative is accidental compatibility forever.

## Why this matters in production

An error contract that lives in a wiki tab has no version, no owner, and no change process. It
describes what the API *used* to do. Meanwhile the registry in code describes what it does
*now*, and the two disagree — which is worse than having no contract at all, because consumers
trust the document.

Two artifacts fix this:

1. **The contract specification** — the published, versioned promise to consumers.
2. **The ADR** — the internal record of *why* the organisation accepted that promise, what it
   costs, and what it explicitly does not cover.

The ADR matters more than teams expect. Six months later, when a new team wants to "just return
a 400 with a string", the ADR is what makes the answer "no, and here is what we decided and
why" instead of a debate.

## Part 1 — Contract specification (excerpt)

```text
Acme SaaS — Public API Error Contract
Contract version: 1.4.0     Contract owner: api-platform
Effective: 2026-02-01       Supersedes: 1.3.x
```

### 1. Scope and stability

```text
This contract covers the error body of every 4xx and 5xx response from the Acme public
API (api.acme.example). It does not cover the webhook delivery contract, which is
specified separately in the Webhook Error Contract.

Stability tier: T3 (public).

Guaranteed:
  G1  Every error response is application/problem+json and contains the fields in §2.
  G2  The `code` field is present on every error response and identifies the condition.
  G3  Within contract version 1.x, new codes MAY be added and new optional fields MAY
      appear. Consumers MUST tolerate codes and fields they do not recognise.
  G4  The meaning of a code, its HTTP status, and its retry semantics are FIXED for the
      lifetime of a code. A change of meaning requires a new code.
  G5  A code, once published, is never re-used for a different condition.

Not guaranteed:
  N1  The `title` and `detail` strings. They are human-readable and MAY change at any time,
      including between two responses in the same minute.
  N2  The order of fields in `errors[]`.
  N3  The presence of vendor-specific metadata in the extensions object.
```

### 2. Response shape

```json
{
  "type": "/problems/validation-error",
  "title": "Validation Failed",
  "status": 422,
  "detail": "The request contained 2 invalid fields.",
  "instance": "/projects/req_01H8/fields",
  "code": "VALIDATION_FAILED",
  "requestId": "req_01H8XZ9K2M",
  "errors": [
    { "field": "seats", "code": "VALIDATION_OUT_OF_RANGE", "detail": "seats must be between 1 and 500" }
  ]
}
```

| Field | Type | Required | Guaranteed |
| ----- | ---- | -------- | ---------- |
| `type` | string (URI reference) | Yes | Yes — stable per problem class |
| `title` | string | Yes | No (structure yes, wording no) |
| `status` | integer | Yes | Yes — matches the HTTP status |
| `detail` | string | Yes | No |
| `instance` | string | Yes | No |
| `code` | string | Yes | Yes — append-only within 1.x |
| `requestId` | string | Yes | Yes — format, not value |
| `errors[]` | array | No | Yes — additive only |

### 3. `type` URI convention

```text
/problems/{problem-class}          root-relative, version-independent, one per class
/problems/{domain}-{condition}     kebab-case, ASCII, ≤ 64 characters
about:blank                       only for genuinely untyped problems (deprecated in 2.x)

Rules:
  - One `type` per problem class. A class whose meaning changes gets a NEW `type`.
  - `type` is NOT versioned. /problems/validation-error is valid in 1.x and 2.x.
  - `type` never contains a host, a query string, or an API version.
```

### 4. Catalogue (excerpt)

| Code | `type` | Status | Retryable | Idempotent | `clientAction` | Since | Owner |
| ---- | ------ | ------ | --------- | ---------- | -------------- | ----- | ----- |
| `VALIDATION_FAILED` | `/problems/validation-error` | 422 | No | Yes | `fix_input` | 1.0.0 | api-platform |
| `AUTH_REQUIRED` | `/problems/unauthenticated` | 401 | No | Yes | `reauthenticate` | 1.0.0 | api-platform |
| `AUTH_FORBIDDEN` | `/problems/forbidden` | 403 | No | Yes | `contact_support` | 1.0.0 | api-platform |
| `RESOURCE_NOT_FOUND` | `/problems/not-found` | 404 | No | Yes | `none` | 1.0.0 | api-platform |
| `PLAN_SEAT_LIMIT_EXCEEDED` | `/problems/plan-seat-limit-exceeded` | 409 | No | Yes | `choose_alternative` | 1.2.0 | billing-team |
| `RATE_LIMITED` | `/problems/rate-limited` | 429 | Yes | Yes | `retry` | 1.0.0 | api-platform |
| `PAYMENT_CARD_DECLINED` | `/problems/payment-declined` | 402 | No | Yes | `choose_alternative` | 1.0.0 | billing-team |
| `EXPORT_STORAGE_UNAVAILABLE` | `/problems/service-unavailable` | 503 | Yes | Yes | `retry` | 1.1.0 | data-team |
| `INTERNAL_ERROR` | `/problems/internal-error` | 500 | No | Yes | `contact_support` | 1.0.0 | api-platform |

### 5. Compatibility policy

```text
SAFE (no contract version bump required):
  - a new code is added
  - an optional field is added
  - a title or detail string is reworded
  - a new problem class (new `type`) is added

BREAKING (requires a MAJOR contract version):
  - a code is removed, renamed, or re-used
  - a code's HTTP status changes
  - a code's meaning or retry semantics change
  - a required field is added, or a field is removed or retyped
  - a clientAction value set gains or loses a member
```

### 6. The unknown-code obligation

```text
Consumers MUST:
  - treat an unrecognised `code` as a generic internal error
  - never throw, crash, or render an empty state because of an unknown code
  - prefer the `clientAction` value over the `code` when deciding what to offer the user

Producers MUST:
  - never emit a code that is absent from the published catalogue
  - never reuse a removed code
```

### 7. Deprecation and sunset

```text
Window:  90 days from announcement for T3 surfaces.
Signal:  `Deprecation` and `Sunset` response headers, and a changelog entry.
Removal: only after 30 consecutive days of zero measured consumption.
Retired: codes keep their mapping and their alias until removed.
```

### 8. Version history

```text
1.0.0  2025-03-03  Initial public error contract.
1.1.0  2025-07-14  Added EXPORT_STORAGE_UNAVAILABLE; added clientAction field.
1.2.0  2025-11-02  Added PLAN_SEAT_LIMIT_EXCEEDED (409).
1.3.0  2026-01-20  Added `errors[]` field details (additive).
1.4.0  2026-02-01  Documentation corrections; added requestId to the guaranteed field list.
```

## Part 2 — ADR-014

```text
ADR-014: Adopt a versioned public error contract
Status:     Accepted
Date:       2026-02-01
Deciders:   api-platform, billing-team, product, support
Owners:     api-platform (contract), team stewards (code families)
```

### Context

Acme's public API returned bare `{"error": "..."}` strings until 2025. Error behaviour was
implicit, undocumented, and changed whenever a handler changed. Two partner incidents in one
quarter traced to the same root cause: partners could not distinguish a permanent failure from
a transient one because there were no codes, only prose and status codes.

The API was also about to be versioned (v2 → v3). We had to decide whether error behaviour
would be versioned along with the API or governed separately.

### Decision

1. **Adopt RFC 9457 Problem Details** as the error body shape for the public API, with the
   Acme extensions `code`, `requestId`, and `errors[]`.
2. **Publish an error contract** as a versioned artifact, separate from the API version, with
   its own semver, catalogue, compatibility policy, and deprecation process.
3. **Every public code is owned** by a steward team, registered in a single registry, and
   generated into the catalogue — the catalogue is never hand-edited.
4. **Codes are append-only within a contract version.** Meaning changes require a new code.
5. **Consumers are obligated to tolerate unknown codes.** The contract states this explicitly so
   it is enforceable by the consumer, not just good manners.
6. **The error contract version is returned on every error response**
   (`Error-Contract-Version`), so consumers can detect drift.
7. **The webhook error contract is a separate artifact** with its own owner and schedule.

### Consequences

**Good**

- Partner escalations now start with a code, and the runbook is indexed by code.
- The contract is testable: a CI suite replays the published guarantees against the current
  implementation and fails on drift.
- New error codes are cheap to add (MINOR), so teams no longer avoid them and stuff conditions
  into `detail` prose.
- The contract made the "which failure is which" question answerable during incidents.

**Bad / accepted costs**

- Every error response carries a header and a code; payload grew by ~40 bytes on errors.
- A MAJOR contract version is a coordinated event: it requires a deprecation window, partner
  communication, and a second release.
- The catalogue and SDK types are generated, so the build must run before a contract change
  ships — a small friction added to every change.
- Two contracts (API and webhook) mean two sets of reviews for teams that touch both.

**Neutral**

- Error contract version and API version are independent. API v3 currently ships error
  contract 1.x.

### Alternatives considered

| Alternative | Why not |
| ----------- | ------- |
| Fold error behaviour into API versions | An error-only fix would force an API migration for consumers who never see the change; in practice teams would stop versioning the errors |
| Keep bare `{ "error": "..." }` strings | No machine-readable condition; partners must parse prose |
| Publish a catalogue but no compatibility policy | A catalogue without a policy is a snapshot; the next change breaks consumers the same way |
| One contract for API and webhooks | Different consumers, different owners, different change cadence; one artifact would always be wrong for one of them |

### Compliance

```text
CI checks:
  [x] every code in the registry has a catalogue row and a `type` URI
  [x] catalogue and registry are generated from the same source (no drift possible)
  [x] published guarantees (status, retryability, clientAction) are replayed in tests
  [x] responses carry Error-Contract-Version matching the registry version
  [x] no public response contains a stack trace, SQL text, or internal hostname

Review checks (owner approval required):
  [x] any removal or meaning change to a public code
  [x] any MAJOR contract version
  [x] any change to the deprecation window or the sunset process
```

## Key data / numbers

- **Contract versions published:** 1.0.0 (2025-03-03) → 1.4.0 (2026-02-01) — four MINOR
  bumps, zero MAJOR, because every change was additive.
- **Guarantees in the spec:** 5 (`G1`–`G5`); explicit non-guarantees: 3 (`N1`–`N3`).
- **Catalogue fields per code:** code · `type` · status · retryable · idempotent ·
  `clientAction` · since · owner.
- **Deprecation window:** 90 days from announcement; removal after 30 days at zero consumption.
- **Contract header:** `Error-Contract-Version` on every error response.
- **Payload cost:** ~40 bytes added per error response (code + requestId + errors[]).
- **CI checks:** 5 automated, 3 requiring owner approval.
- **Contract owner:** 1 team per surface; code stewards: 1 team per code family.

## Real-world use case — WebhookIngest

Acme's `WebhookIngest` accepts Stripe webhooks and returns errors to Stripe's servers, but
Stripe does not read error bodies — it reads the **HTTP status** and retries on 5xx. That
made the webhook "error contract" a strange one: the body was invisible to the consumer, and
the real contract was "which failures are permanent (2xx, no retry) versus transient (5xx,
retry)".

Acme's first webhook implementation returned `400` for a bad signature, which told Stripe the
event was poison and should not be retried. The result: a transient signing-key rotation
failed on 11% of real payment events, and those payments were **lost**.

The webhook error contract, written separately from the API contract, made the semantics
explicit:

```text
Webhook Error Contract (v1.1.0, owner: billing-team)

  SIGNATURE_INVALID          → 401  permanent  (do not retry; the event is untrustworthy)
  PAYLOAD_MALFORMED          → 400  permanent
  EVENT_UNPROCESSABLE        → 422  permanent
  DEPENDENCY_TEMPORARILY_DOWN→ 503  transient  (Stripe retries)
  INTERNAL_ERROR             → 500  transient  (Stripe retries)
```

And the operational rule that came with it: **a signing-key rotation is a deployment, not a
config flip** — the rotation is done by having both keys active, and a `SIGNATURE_INVALID`
during rotation is treated as an incident, not as noise.

Because this contract was written separately from the API contract, the billing team could
change webhook semantics without touching the API's 1.x compatibility promises, and the API
team could keep its deprecation window untouched.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| State guarantees AND explicit non-guarantees | Leave readers to infer what is promised |
| Generate the catalogue from the registry | Maintain the catalogue by hand |
| Publish the contract version on every error response | Keep the version only in the document |
| Record the decision, the costs, and the alternatives | Skip the ADR for "small" contract changes |
| Give the webhook/API surfaces separate contracts | Force one artifact on consumers with different needs |
| Test published guarantees in CI | Assume the implementation matches the spec |
| Name stewards per code family | Leave the catalogue ownerless |

## Common mistakes

- **The snapshot contract.** Published once, never updated, describing the past.
- **The hand-edited catalogue.** Diverges from the registry within weeks.
- **The unversioned contract.** "Which guarantees were live?" is unanswerable.
- **The ADR-free adoption.** The standard is quietly rolled back the first time it is
  inconvenient.
- **The over-broad contract.** One document for the API, the webhooks, the SDKs, and the
  internal queues — nobody can find their part.
- **The guarantees-without-non-guarantees spec.** Readers assume prose is promised.

## Checklist

- [ ] The contract has a version, an owner, and an effective date.
- [ ] It states guarantees and explicit non-guarantees.
- [ ] Every public code row carries `type`, status, retryability, `clientAction`, since, owner.
- [ ] The compatibility policy lists safe and breaking changes.
- [ ] The unknown-code obligation is stated for consumers and producers.
- [ ] The deprecation window, sunset signal, and removal gate are documented.
- [ ] The catalogue is generated, and CI replays the published guarantees.
- [ ] An ADR records the decision, the costs, and the rejected alternatives.

## Related

- [Ownership, Documentation, and Message Independence](../01-concepts/03-ownership-documentation-and-message-independence.md)
- [The Deprecation Workflow: Introduce → Dual-Emit → Sunset](./01-deprecation-workflow-introduce-dual-emit-sunset.md)
- [Versioning Error Contracts](../02-deep-dive/02-versioning-error-contracts.md)
- [Chapter 20 — Standardized API Error Responses](../../../part-08-http-and-api/20-standardized-api-error-responses/README.md)
