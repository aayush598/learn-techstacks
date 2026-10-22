# Chapter 18 — Reference

> Part VII · Chapter 18 · The domain error contract, HTTP/gRPC mapping tables, and placement
> decision tables.

## The domain error contract

```text
DomainError (internal, transport-free)
{
  code       stable, registry-listed, context-namespaced   → clients, logs, registry
  category   VALIDATION|CONFLICT|FORBIDDEN|NOT_FOUND|PAYMENT|QUOTA|PRECONDITION|LIFECYCLE
  details    structured, typed per code (requested, limit, allowed, capability, …)
  cause      ORIGINAL (server-side only)                    → debugging
  transient  false by default for domain denials            → retry engine
}

Transport projection (adapter, per API version)
{
  HTTP status   from registry row (code + category → status)
  body          RFC 9457 problem: type/title/status/detail/instance + requestId
                + details spread (allowlisted keys)
  headers       Retry-After only when waiting genuinely helps
}
```

## HTTP and gRPC mapping tables

| Category / code pattern | HTTP | gRPC | Retry? |
| ----------------------- | ---- | ---- | ------ |
| `INVALID_TRANSITION`, `STATE_CONFLICT` | `409` | `FAILED_PRECONDITION` (9) | No — refresh |
| `CONCURRENT_MODIFICATION` | `409` | `ABORTED` (10) | Yes — with version bump |
| `ALREADY_EXISTS` (+ `details.field`) | `409` | `ALREADY_EXISTS` (6) | No (or idempotent replay) |
| `NOT_OWNER` (admit policy) | `403` | `PERMISSION_DENIED` (7) | No |
| Cross-tenant (hide policy) | `404` | `NOT_FOUND` (5) | No |
| `ENTITLEMENT_MISSING` | `403` | `PERMISSION_DENIED` (7) | No — upgrade |
| `INSUFFICIENT_FUNDS`, `PAYMENT_METHOD_REQUIRED` | `402` | `FAILED_PRECONDITION` (9) | No — human |
| `SEAT_QUOTA_EXCEEDED`, `STORAGE_QUOTA_EXCEEDED` | `402` (recommended) | `RESOURCE_EXHAUSTED` (8) | No — free capacity/upgrade |
| Rate limiting (temporal) | `429` + `Retry-After` | `RESOURCE_EXHAUSTED` (8) + `retry-info` | Yes — honor hint |
| `OPERATION_IN_PROGRESS`, `DEPENDENCY_PENDING` | `409` + `retryAfterMs` | `FAILED_PRECONDITION` (9) | Sometimes — honor hint |
| `VERIFICATION_REQUIRED`, `TRIAL_NOT_ENDED` | `409` (or `403`) | `FAILED_PRECONDITION` (9) | No — complete step |
| `RESOURCE_NOT_FOUND` | `404` | `NOT_FOUND` (5) | No |
| `VALIDATION`-class domain rules (`SEATS_OUT_OF_RANGE`) | `422` | `INVALID_ARGUMENT` (3) | No |
| Invariant breach (our bug) | `500` + alert | `INTERNAL` (13) | No — page us |

Pick **one** policy per family (e.g. quota → `402` everywhere) and snapshot-test it; mixing `402`
and `409` for the same code across endpoints is a contract bug.

## Placement decision table — where does the check live?

| Question about the rule | Lives in | Error style |
| ----------------------- | -------- | ----------- |
| Needs only the request payload? | DTO/validation (Ch. 17) | Field error, `422` |
| Needs only the entity's own fields? | Value object / aggregate root | Domain error (or invariant → `500`) |
| Needs sibling entities in one tx boundary? | Aggregate root method | Domain error |
| Needs other aggregates, clock, or ports? | Domain service | Result/error outcome |
| Needs a database round trip as *detection*? | Repository edge (translate `23505`→`409`) | Domain error + cause |
| Needs HTTP/framework context? | Adapter/controller only | Transport mapping |

## Rule family → code starter kit

| Family | Codes | Key details |
| ------ | ----- | ----------- |
| Lifecycle | `INVALID_TRANSITION`, `ALREADY_CANCELED`, `JOB_ALREADY_RUNNING` | `action`, `state`, `allowed`, `stateReason` |
| Precondition | `OPERATION_IN_PROGRESS`, `VERIFICATION_REQUIRED`, `GRACE_PERIOD_ACTIVE` | `blocking{}`, `retryAfterMs`, `endsAt` |
| Access | `NOT_OWNER`, `INSUFFICIENT_ROLE`, `TENANT_MISMATCH` | `resourceKind` (redacted id) |
| Duplicate | `ALREADY_EXISTS` | `field`, `resource` |
| Balance/quota | `INSUFFICIENT_FUNDS`, `SEAT_QUOTA_EXCEEDED`, `STORAGE_QUOTA_EXCEEDED` | `requested`, `limit`, `current`, `plan`, `upgradeRequired` |
| Entitlement | `ENTITLEMENT_MISSING` | `capability`, `plan`, `entitledPlans[]`, `reason` |
| Concurrency | `CONCURRENT_MODIFICATION` | `expectedVersion`, `actualVersion` |

## Multi-violation policy table

| Operation type | Policy | HTTP shape |
| -------------- | ------ | ---------- |
| Consumer single-action (upgrade, cancel) | Ordered first failure | One code + details |
| Admin/bulk workflow | Accumulate + cap | Primary code + `details.violations[]` |
| Validation-adjacent pure rules | Aggregate like Ch. 17 | `422` + field errors |

## Domain vs infrastructure quick test

| Signal | Domain | Infrastructure |
| ------ | ------ | -------------- |
| Healthy deps still produce it? | Yes | No |
| PM recognizes it as by-design? | Yes | No |
| Same-request retry helps? | No | Usually |
| Status family | 4xx | 5xx |
| Owner | Domain team | Platform/integration |

## Client branching cheat sheet

```text
on problem response:
  402 + upgradeRequired  → billing CTA
  403 + capability       → upsell (entitledPlans)
  409 + allowed          → refresh state; re-render actions
  409 + retryAfterMs     → wait, then retry
  409 (no hint)          → refresh; do NOT auto-retry identical call
  422 + errors[]         → field rendering (Ch. 17)
  429 + Retry-After      → backoff (Ch. 27)
  500                    → generic; report requestId
  unknown code/kind      → generic fallback + log code (18.20)
```

## Contract invariants (test these)

1. Every emitted domain code has a registry row with exactly one status per API version.
2. No HTTP status literal and no framework exception type exists in `domain/` (CI lint).
3. Every `409` transition denial includes `state`, `action`, `allowed`.
4. Every quota/balance denial includes numeric details (`requested`/`limit` or `due`).
5. Duplicate webhook deliveries produce zero additional domain effects (property test).
6. Invariant-breach paths alert and never render as user `422`s.

## Signposts

- Validation side of the line → [Ch. 17](../../17-input-validation-error-handling/README.md)
- SQLSTATE → domain → HTTP map → [Ch. 16 practical](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/03-practical-examples/01-postgres-sqlstate-to-domain-to-http.md)
- HTTP status semantics → [Ch. 19](../../../part-08-http-and-api/19-http-error-semantics/README.md)
- Registry governance → [Ch. 8](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
- Contract versioning → [Ch. 49](../../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)
- Billing workflows end-to-end → [Ch. 42](../../../part-16-specialized-saas-scenarios/42-auth-billing-and-subscription-workflows/README.md)

## Related

- [Chapter 18 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Entitlement, Lifecycle, and Webhook Examples](../03-practical-examples/02-entitlement-lifecycle-and-webhooks.md)
- [Chapter 17 Reference](../../17-input-validation-error-handling/05-reference/README.md)
