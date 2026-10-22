# Acme SaaS Requirements Across Three Stages

> Part I · Chapter 3 · Sections 3.1–3.3 · _Estimated reading time: 24 min_

## In one sentence

Following one product — **Acme SaaS** — from MVP to startup to enterprise shows how the *same*
feature (`POST /invoices`) accumulates requirements without ever being rebuilt from scratch.

## Why this matters in production

Requirements are easier to internalize as an *evolution* than as a checklist. Seeing what changed,
what stayed, and what was deliberately deferred at each stage lets you place your own product
correctly and avoid both short-cutting and over-building.

## Stage 1 — MVP (Section 3.1)

**Context:** 50 beta users, no revenue, one engineer, single Postgres, no queue.

**Requirements:** explicit errors, one catch-all boundary, no fake success, request IDs.

```ts
// MVP implementation — minimal but not dishonest.
app.post("/invoices", async (req, res) => {
  const requestId = req.header("x-request-id") ?? randomUUID();
  try {
    const dto = validateInvoice(req.body);            // throws on bad input
    const invoice = await db.invoices.insert(dto);
    res.status(201).json({ id: invoice.id, requestId });
  } catch (err) {
    if (err instanceof ValidationError) {
      return res.status(422).json({ code: "VALIDATION_FAILED", requestId, fields: err.fields });
    }
    log.error({ err, requestId }, "invoice create failed");
    res.status(500).json({ code: "INTERNAL", requestId });
  }
});
```

| Requirement | Present at MVP | Deferred |
| ----------- | -------------- | -------- |
| Explicit errors | ✅ | |
| One boundary | ✅ | |
| Request IDs | ✅ | |
| Consistent envelope | partial | full envelope later |
| Code registry | ❌ | later |
| Idempotency | ❌ (no money yet) | when billing added |
| Retries/backoff | ❌ | later |

## Stage 2 — Growing startup (Section 3.2)

**Context:** 2,000 paying customers, Stripe billing, first background export, mobile clients.

**New pressures:** clients need to *act* on errors; drift appears across endpoints; transient
dependency failures reach users as 500s.

```ts
// Startup implementation — registry-driven envelope + idempotency where money moves.
// errors/registry.ts
export const ERRORS = {
  VALIDATION_FAILED:   { http: 422, retryable: false },
  DUPLICATE_RESOURCE:  { http: 409, retryable: false },
  RESOURCE_NOT_FOUND:  { http: 404, retryable: false },
  UPSTREAM_TIMEOUT:    { http: 504, retryable: true },
} as const;

// checkout.ts — idempotent charge (financial obligation arrives with billing)
async function charge(order: Order, idempotencyKey: string) {
  return withRetry(
    () => stripe.charge(order.amount, { idempotencyKey }),
    { attempts: 4, retryable: (e) => e.status === 429 || e.status >= 500 },
  );
}
```

| Requirement | Added | Why |
| ----------- | ----- | --- |
| Standard envelope | ✅ | Clients parse errors consistently |
| Code registry | ✅ | Same condition classified once |
| Idempotency (billing) | ✅ | Financial obligation |
| Retries + backoff | ✅ | Transient dependency failures |
| Basic 5xx alerting | ✅ | Detect systemic issues |

## Stage 3 — Enterprise SaaS (Section 3.3)

**Context:** 40 enterprise tenants, SLAs, a compliance review, multi-region, partner API.

```yaml
# Public error contract (versioned) + SLI/SLO definitions.
error_contract:
  version: "2026-01"
  envelope: "application/problem+json"      # RFC 9457
  deprecation_window_days: 180
slos:
  api_availability: "99.9%"                 # ~43 min/month error budget
  api_latency_p95_ms: 300
audit:
  invoice_events: "append-only, 7-year retention"
tenancy:
  isolation: "row-scoped; enterprise tier gets dedicated pool"
```

| Requirement | Added | Why |
| ----------- | ----- | --- |
| Versioned public contract | ✅ | Partner/enterprise clients, deprecation |
| SLA/SLO + error budget | ✅ | Govern fail vs degrade |
| Audit trail | ✅ | Compliance |
| Tenant isolation tiers | ✅ | Enterprise obligations |
| DR/failover + runbooks | ✅ | Contractual uptime |

## What never changed

Across all three stages, the **cheap non-negotiables** stayed: explicit errors, one boundary, no
fake success, request IDs. Nothing was rebuilt — each stage *added* to the previous contract.

## Key data / numbers

| Item | MVP | Startup | Enterprise |
| ---- | --- | ------- | ---------- |
| Error shape | ad hoc JSON | standard envelope | RFC 9457 contract |
| Validation status | `422` | `422` | `422` |
| Idempotency | none | Stripe keys (24h) | keys + audit |
| Retry attempts | none | 3–5, backoff | 3–5, budget-governed |
| Availability target | best-effort | informal 99% | SLA 99.9% (~43 min/mo) |
| Contract versioning | none | internal | public, 180-day deprecation |

## Real-world use case — Acme SaaS

When Acme launched billing, they could have kept the MVP shape and simply "tried harder." Instead
they recognized that **adding money moved Acme into the financial profile (3.6)** and immediately
added idempotency keys and retry classification at the `Checkout` boundary. The first Stripe timeout
during a retry window collapsed to a single charge because the key was there — a requirement the
MVP correctly deferred and the startup correctly added, at exactly the right moment.

## Trade-offs

| Stage | Build cost | Reliability | Debt if skipped |
| ----- | ---------- | ----------- | --------------- |
| MVP | Low | Basic | Ambiguous errors get coded in |
| Startup | Medium | Solid | Drift, double charges |
| Enterprise | High | Contractual | Compliance failure, churn |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep the cheap non-negotiables at every stage | Defer explicit errors "for later" |
| Add idempotency when money arrives | Retry charges without keys |
| Version the contract before enterprise clients | Break partners silently |
| Let profiles raise the floor | Let "MVP" excuse financial bugs |

## Common mistakes

- **Rebuilding error handling** at each stage instead of extending it.
- **Adding billing without idempotency** because stage said "startup."
- **Deferring request IDs** — makes every later stage harder to operate.
- **Adopting enterprise tooling** at MVP.

## Checklist

- [ ] Does each stage keep the MVP non-negotiables?
- [ ] Did adding money trigger idempotency immediately?
- [ ] Is the public contract versioned before enterprise commitments?
- [ ] Is each added safeguard mapped to a stage pressure?
- [ ] Did you extend rather than rebuild?

## Related

- [Requirements by Product Stage](../01-concepts/01-requirements-by-product-stage.md)
- [Specialized SaaS Requirements in Code](./02-specialized-saas-requirements-in-code.md)
- [Chapter 42 — Auth, Billing, and Subscription Workflows](../../../part-16-specialized-saas-scenarios/42-auth-billing-and-subscription-workflows/README.md)
- [Chapter 49 — Error Contract Design and Versioning](../../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)
