# Classification Axes: HTTP Semantics through Compensation

> Part II · Chapter 4 · Sections 4.10–4.15 · _Estimated reading time: 28 min_
> **Prerequisite:** [Classification Axes: Origin through Retry](./02-classification-axes-origin-through-retry.md)

## In one sentence

The remaining axes — **HTTP semantics, domain/capability, security implications, transactional
consequences, dependency, and compensation requirement** — connect the taxonomy to the outside
contract, the business, and the data.

## Why this matters in production

These axes are where a good taxonomy earns its keep. HTTP semantics shape what clients can do;
domain/capability decides ownership; security implications decide what may be disclosed;
transactional consequences decide whether you roll back or compensate; the dependency axis drives
resilience; and the compensation axis is the only thing standing between a partial failure and
inconsistent data.

## 4.10 By HTTP semantics

Every category maps to an HTTP status **class** (Chapter 19). The mapping is derived, not
hand-picked per endpoint:

| Category family | Typical status | Why |
| --------------- | -------------- | --- |
| validation / parsing | `400`, `422` | Client can fix the request |
| authentication | `401` | Credentials missing/invalid |
| authorization | `403` | Authenticated but not permitted |
| not found | `404` | Resource does not exist |
| conflict / duplicate / state transition | `409` | Request conflicts with current state |
| rate limit / quota | `429` | Caller should slow / upgrade |
| dependency unavailable | `502`, `503`, `504` | Upstream problem |
| internal programming / unexpected | `500` | Our fault, no client action |

```http
HTTP/1.1 409 Conflict
Content-Type: application/problem+json

{ "type": "https://acme.example/errors/conflict", "title": "Version conflict",
  "status": 409, "code": "CONFLICT_VERSION_MISMATCH", "instance": "/exports/exp_123" }
```

> ⚠️ **Hazard.** Never return `200` with `{"success": false}` for a failure. It defeats caching,
> proxies, retries, monitoring, and SDKs. Failures use 4xx/5xx (Chapter 19.17).

## 4.11 By domain / capability

The domain axis maps an error to a **business capability**, which determines ownership and the
public code prefix:

```text
billing   → PAYMENT_*, SUBSCRIPTION_*, INVOICE_*
identity  → AUTH_*, SESSION_*, TENANT_*
exports   → EXPORT_*, FILE_*
agents    → AI_*, TOOL_*
webhooks  → WEBHOOK_*
```

This is the axis that lets a single global handler route a `billing` failure to the billing
playbook without parsing anything. It is also the natural boundary for versioning (Chapter 49).

## 4.12 By security implications

Some categories are **disclosure-sensitive** and must be redacted, normalized, or deliberately
vague:

| Category | Risk | Rule |
| -------- | ---- | ---- |
| authentication | user enumeration | Return the same response for unknown user and wrong password |
| authorization | existence disclosure | Return `404` instead of `403` when existence is itself sensitive |
| database | schema leakage | Never expose SQLSTATE or table names |
| configuration | infra leakage | Never expose hostnames, paths, or env values |
| validation | reflection | Do not echo raw input back unsanitized |

The security axis marks an error as `SENSITIVE` so the redaction layer (Chapter 36) knows to strip
context before serialization.

## 4.13 By transactional consequences

Classify what the failure means for **data state** (Chapters 22–23):

```text
no_state_change   → nothing written; safe to retry
rolled_back       → transaction aborted; consistent
partially_applied → some writes committed; needs compensation
unknown           → outcome ambiguous (timeout after commit?); needs idempotency + re-check
```

The `unknown` outcome is the hardest and demands an **idempotency key** before any retry.

## 4.14 By dependency

The dependency axis names **which external system** failed and its criticality:

| Dependency | Criticality | On failure |
| ---------- | ----------- | ---------- |
| Postgres primary | required | fail request / retry transient |
| Stripe | required for billing | no silent success; idempotent retry |
| Redis cache | optional | bypass, read from DB |
| LLM provider | optional per feature | degrade to cached/placeholder |
| email / analytics | best-effort | enqueue; drop after budget |

This axis feeds bulkheads, circuit breakers, and fallback selection (Chapters 29–30).

## 4.15 By whether compensation is required

Some failures leave **completed work** that must be logically undone:

```text
Charge succeeded → Provision failed → compensation = refund
Reserve inventory succeeded → Payment failed → compensation = release reservation
Upload part 1..N succeeded → part N+1 failed → compensation = abort multipart
```

Classifying `requires_compensation = true` is what triggers a saga/compensation path (Chapter 39)
rather than a naive retry.

## Worked example — Checkout, classified end to end

```text
Step: charge card via Stripe → succeeded
Step: create subscription row → failed (DB 500)
Classification:
  origin            = dependency (DB)
  permanence        = transient
  recoverable       = yes (retry the DB write)
  http              = 503 to caller
  domain            = billing
  security          = sensitive (no provider detail)
  transactional     = partially_applied
  dependency        = postgres (required)
  compensation      = NOT required (charge is idempotent on key; retry completes the saga)
Decision: retry the DB write with the SAME idempotency key; never re-charge; never mark paid.
```

Change one step — make the charge the *second* step — and the same failure now *requires*
compensation of anything done in step one.

## Key data / numbers

- RFC 9457 Problem Details defines the canonical HTTP error shape (`type`, `title`, `status`,
  `detail`, `instance`).
- `409 Conflict` is the standard status for version/state conflicts; combine with `ETag` +
  `If-Match` for optimistic locking (`412 Precondition Failed`).
- `429` should accompany `Retry-After` and often `RateLimit-Limit` / `RateLimit-Remaining`.

## Real-world use case — Acme SaaS (tenant billing)

Acme adds an `INVOICE_*` capability. A nightly invoice job partially applies: it marks an invoice
`issued` but fails before writing the line items. Classification: domain `billing`, transactional
`partially_applied`, compensation `required`. The job now writes line items first inside a single
transaction; on failure it rolls back and retries idempotently. Because the taxonomy flagged
compensation, the fix was one transaction boundary — not a new subsystem.

## Trade-offs

| Axis | Cheap to omit? | Cost of omitting |
| ---- | -------------- | ---------------- |
| HTTP semantics | No | Inconsistent contracts, broken clients |
| Domain | No | No ownership; cross-team chaos |
| Security | No | Leakage, enumeration, fines |
| Transactional | Only for reads | Silent corruption |
| Dependency | No | No resilience strategy |
| Compensation | For pure reads | Orphaned/double side effects |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Derive HTTP from category | Hand-pick status codes per endpoint |
| Tag security-sensitive errors | Echo raw DB/provider text |
| Classify transactional state explicitly | Assume every failure rolled back |
| Mark compensation requirement | Retry blindly after partial success |

## Common mistakes

- **`200` with an error body.** Breaks every generic client.
- **Leaking SQLSTATE** because it "is useful for debugging" — put it in logs, not the response.
- **Assuming a timeout means "nothing happened."** The commit may have succeeded.
- **Forgetting compensation** on multi-step flows, producing double charges.

## Checklist

- [ ] Does every category map to a status class?
- [ ] Do codes carry a domain prefix?
- [ ] Are security-sensitive errors flagged for redaction?
- [ ] Is transactional consequence recorded for every write path?
- [ ] Is compensation requirement explicit for multi-step flows?

## Related

- [Classification Axes: Origin → Retry](./02-classification-axes-origin-through-retry.md)
- [Mutual Exclusivity, Growth, and Governance](./04-mutual-exclusivity-growth-governance.md)
- [HTTP Error Semantics](../../../part-08-http-and-api/19-http-error-semantics/README.md)
- [Partial Failures and Multi-Step Operations](../../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
