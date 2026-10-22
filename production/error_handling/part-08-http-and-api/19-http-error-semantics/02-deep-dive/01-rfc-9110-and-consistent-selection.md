# RFC 9110 and Consistent Status Selection

> Part VIII · Chapter 19 · Sections 19.2, 19.11, 19.19 · _Estimated reading time: 18 min_
> **Prerequisite:** [Request Content Errors: 400, 413, 415, 422](../01-concepts/02-request-content-errors-400-413-415-422.md)

## In one sentence

Consistent selection is not taste — it is the mechanical result of (a) reading RFC 9110's
definitions literally, (b) fixing a **decision order** for overlapping statuses, and (c)
enforcing the outcome through the **error registry** so no handler can freelance.

## Why this matters in production

Two engineers looking at the same failure will pick different statuses unless a rule settles
it: `400` or `422` for a wrong type? `409` or `422` for a uniqueness violation? `404` or `403`
for another tenant's row? Without written answers, the API drifts until clients write
defensive `switch` statements covering all plausible codes — the exact cost standardization is
meant to prevent. Consistency is also a **testing** property: a registry-driven mapping means
one test table verifies the whole surface instead of per-handler guesses.

## Core concept — RFC 9110's actual definitions

RFC 9110 (HTTP Semantics) supersedes the older RFC 7231 family and is the current authority.
The definitions that settle the overlaps:

| Code | RFC 9110 definition (paraphrased) | Settles |
| ---- | --------------------------------- | ------- |
| `400` | The server **cannot process the request because of its perceived syntax error** | Syntax failures only — not semantics |
| `401` | Request lacks **valid authentication credentials** for the target resource | Identity, not permission |
| `403` | Server **understood but refuses** to authorize; applicable even if authentication would help | Permission refusal even post-auth |
| `404` | Server **did not find a current representation** for the target resource | "Not here (for you)" |
| `405` | Method **known to the resource but not supported**; requires `Allow` | Method vs path distinction |
| `409` | Request **conflicts with the current state** of the server | State conflicts, not field invalidity |
| `410` | Target **is no longer available and the condition is likely permanent** | Permanent removal vs absence |
| `413` | Content **larger than the server is willing or able to process** | Size, before parse |
| `415` | **Media type not supported** by the target resource | Type negotiation, before parse |
| `422` | Content syntactically correct but **semantically erroneous** (e.g. value-level errors) | The semantic half of validation |
| `429` | User has **exceeded request rate/quota** (RFC 6585; in RFC 9110's registry) | Rate limiting vs authz |
| `500` | Server hit an **unexpected condition** preventing fulfillment | Bugs vs known conditions |
| `502` | Gateway received an **invalid response** from an inbound server | Upstream protocol breakage |
| `503` | Server is **temporarily unable to handle** (overloaded/maintenance) | Known temporary unavailability |
| `504` | Gateway did **not receive a timely response** from an upstream | Upstream silence |

RFC 9110 also states the meta-rule: clients parse the **class** (first digit) for generic
behavior and the **specific code** for specialized behavior. That is why putting a `422`-class
condition into a `5xx` code breaks generic client logic, not just pedantic correctness.

## How it works — the overlapping-status decision procedure

For each historically ambiguous pair, fix the axis of difference:

### 19.2 / 19.11 — `400` vs `422`

```text
Axis: CAN the payload be parsed into a structure at all?
  NO  → 400           (broken encoder; no field semantics exist yet)
  YES → 422           (structure exists; schema/values/business rules fail)
```

Edge cases, fixed by policy:

| Edge | Policy | Rationale |
| ---- | ------ | --------- |
| JSON parses but a field's *type* is wrong (`"seats": "ten"`) | `422` (recommended) | Structure exists; value is semantically wrong. Some validators default to `400` — acceptable if uniform |
| Query/path parameter invalid (bad UUID format) | `400` | The request line fails to decode; common convention |
| Body valid JSON but not the expected *schema* (missing required field) | `422` | Schema is a semantic contract; field details belong in `errors[]` |
| `400` detail containing parse position | Allowed internally; genericize for public APIs | Avoid echoing attacker-supplied bytes (§19.18) |

### `409` vs `422` (uniqueness and lifecycle)

```text
Axis: does the failure depend on the CURRENT STATE of an existing resource?
  NO  (pure input rule: password too weak)                → 422
  YES (a row exists / resource moved / already captured)  → 409
```

`email already registered` is the classic fight. Recommended: `409` — because the client's
correct action is "this exists; sign in or reset," not "fix the format." Either is defensible;
**document the choice in the registry and never vary it per endpoint**.

### `404` vs `403` (existence hiding)

```text
Axis: may the caller learn the resource exists?
  NO (cross-tenant, unauthorized by policy) → 404   [recommended for multi-tenant SaaS]
  YES (known but forbidden to this role)     → 403
```

### `404` vs `405` vs `405`-adjacent routing

```text
Axis: does the ROUTE exist at all?
  NO                         → 404
  YES, wrong method          → 405 + Allow
  YES, right method          → proceed (then resource lookup → 404/200)
```

## Enforcing consistency — registry, not reviewers

The procedure only survives if it is executable. The registry column is the enforcement
point (Chapter 8):

```ts
// The registry is the single place a status is chosen. Handlers never call res.status(4xx).
const HTTP: Record<ErrorCode, number> = {
  MALFORMED_JSON:            400,
  INVALID_QUERY_PARAMETER:   400,
  UNAUTHENTICATED:           401,
  TOKEN_EXPIRED:             401,
  INSUFFICIENT_ROLE:         403,
  ACCOUNT_SUSPENDED:         403,
  PROJECT_NOT_FOUND:         404,
  METHOD_NOT_ALLOWED:        405,
  VERSION_CONFLICT:          409,
  EMAIL_ALREADY_REGISTERED:  409,
  RESOURCE_GONE:             410,
  PAYLOAD_TOO_LARGE:         413,
  UNSUPPORTED_MEDIA_TYPE:    415,
  VALIDATION_FAILED:         422,
  RATE_LIMITED:              429,
  UNHANDLED_EXCEPTION:       500,
  SERVICE_UNAVAILABLE:       503,
} as const;
```

Contract tests then iterate the table and assert each mapped status is produced by the
corresponding scenario — drift fails CI, not a customer.

## Worked example — one code, one status, forever

Acme once had `slug taken` return `409` on `POST /projects` and `422` on `PATCH
/projects/{id}/slug`. SDK code handled both; the public docs listed one. The fix was one
registry row (`SLUG_TAKEN → 409`, visibility public, clientAction `choose_alternative`) and a
contract test per endpoint family. Client-side `switch` statements shrank, docs matched
reality, and the on-call runbook needed one entry instead of two.

## Key data / numbers

- **RFC 9110** is the current HTTP semantics spec (obsoletes RFC 7230–7235 family).
  **RFC 9457** defines Problem Details (Ch. 20). **RFC 6585** originally defined `428`,
  `429`, `431`, `511` — `429` remains the rate-limit code.
- **Required headers:** `401` → `WWW-Authenticate`; `405` → `Allow`. RFC 9110 §15.5.59
  (`Retry-After`) applies to `503` and (via RFC 6585) `429`.
- **Decision axes that resolve every pair in this chapter:** parseability (400/422),
  identity (401), permission (403), existence (404/410), route (404/405), state (409),
  size (413), media type (415), rate (429), fault ownership (5xx family).
- **Registry-driven APIs** typically show a near-flat distribution across 4xx codes;
  a spike in one code (e.g. `400` = 90% of errors) usually means misclassification, not a
  client pandemic.

## Real-world use case — Acme SaaS contract tests

Acme's API review checklist required a human to eyeball status codes on every new endpoint.
Drift persisted (three endpoints returned `500` for validation). The team moved selection into
the registry and added a contract test that, for each error code, drives a synthetic request
through the full middleware chain and asserts exact status + headers + envelope `code`. A
"new endpoint" PR that invents a status now fails CI with "code X not in registry." Escape
hatch: adding a registry row (with owner + review) is a one-line diff — the right amount of
friction: easy to extend, impossible to freelance.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Registry-enforced selection | Consistent, testable, auditable | Central bottleneck for new codes | Default |
| Per-endpoint documented tables | Local clarity | Drift across endpoints | Tiny internal APIs |
| Framework defaults untouched | Zero effort | `500`-sprawl, no taxonomy | Prototypes only |

## Common mistakes

- **Classifying from the exception type alone.** `NotFoundException → 404` sounds fine until
  a cache-miss exception reuses the same type. Classify from the *error code*, not the class
  name.
- **Letting middleware override handler-mapped statuses.** A catch-all that rewrites all
  errors to `500` undoes careful mapping. The catch-all must pass through already-mapped
  application errors (Ch. 21).
- **"We'll fix it in the client."** Baking drift into SDK fallback lists cements every past
  mistake as contract.
- **Resolving overlaps differently per endpoint family "because resources differ."** Rarely
  justified; usually just unexamined habit. Document true exceptions with a reason.

## Checklist

- [ ] The overlapping pairs above have written, one-line policies in your API standard.
- [ ] No HTTP literal for a 4xx/5xx exists outside the registry/mapping module.
- [ ] Contract tests assert status per error code.
- [ ] RFC-required headers (`WWW-Authenticate`, `Allow`, `Retry-After` where applicable) are
      part of the tested contract, not best-effort extras.
- [ ] New codes require a registry PR with owner + rationale.

## Related

- [Status Code Classes and Selection Table](../01-concepts/01-status-code-classes-and-selection-table.md)
- [Misleading Responses and Internal Exposure](./02-misleading-responses-and-internal-exposure.md)
- [Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
