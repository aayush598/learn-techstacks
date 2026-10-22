# Requirements by Product Stage — MVP, Startup, Enterprise

> Part I · Chapter 3 · Sections 3.1, 3.2, 3.3 · _Estimated reading time: 22 min_

## In one sentence

Error-handling requirements **grow with the cost of failure**: an MVP needs explicit errors and one
clean boundary, a growing startup adds consistency and recovery, and enterprise SaaS adds
contracts, compliance, isolation, and resilience.

## Why this matters in production

Building enterprise-grade handling into an MVP wastes months and slows learning. Skipping the MVP
basics once real customers arrive produces silent data loss at the worst moment — right when growth
makes each incident public. The stage tells you *which* requirements are load-bearing now and which
can wait.

## Core concept — a stage ladder

```text
  MVP                Growing startup            Enterprise SaaS
  ───                ───────────────            ───────────────
  learn fast         keep customers             never lose data,
  minimal users      consistent behavior        never breach trust,
  low cost of failure medium cost               audited & contracted

  must:              adds:                      adds:
  • explicit errors  • one error envelope       • versioned public contracts
  • one boundary     • registry + codes         • SLA/SLO + error budgets
  • no silent loss   • retries w/ backoff       • audit trails
  • correlation id   • idempotency (writes)     • tenant isolation + residency
  • fail loud in dev • basic observability      • DR, compliance, on-call
```

### 3.1 MVP

**Goal:** learn fast with the least ceremony. But a few things are *not* optional even at MVP
because they are cheap now and catastrophic later.

| Non-negotiable at MVP | Why |
| --------------------- | --- |
| Explicit errors (no `200 {"error":...}`) | Clients cannot act on ambiguous shapes later |
| One catch-all boundary | Prevents crashes from leaking to users |
| Never fake success | Silent data loss is discovered by customers |
| Correlation/request IDs | Without them, every bug is uninvestigable |
| Fail loudly in non-prod | Fast feedback for developers |

Deferrable at MVP: retries with backoff, code registries, circuit breakers, DLQs, sagas.

### 3.2 Growing startup

**Goal:** survive the first real load and the first paying customers. Requirements shift from
*individual* correctness to *consistent* behavior and *basic recovery*.

Adds:

- **A standard error envelope** so every client parses errors one way.
- **A code registry** so the same condition is classified identically everywhere.
- **Retries with backoff** for transient dependency failures, with a cap.
- **Idempotency** for any write a client might retry (at least payment-adjacent).
- **Basic observability** — error rates by code, alerting on 5xx.

### 3.3 Enterprise SaaS

**Goal:** never lose data, never breach trust, prove it. Requirements become *contractual*.

Adds:

- **Versioned public error contracts** (Chapters 49, 20) with deprecation windows.
- **SLA/SLO and error budgets** that govern how aggressively to fail vs degrade.
- **Audit trails** — who did what, when, and whether it succeeded.
- **Tenant isolation and data residency** (Section 3.4).
- **DR/failover, on-call, and runbooks** for the failure classes you now must not lose.

## How it works (mechanics) — deriving requirements

```text
  1. Stage?           MVP | Startup | Enterprise
  2. Architecture?    single | modular | microservices | serverless
  3. Risk profile?    multi-tenant? money? real-time? AI? background?
  4. Cost of failure? $ per hour, per record, per breach
        │
        ▼
  Requirements = max( stage baseline , profile obligations , cost-of-failure floor )
```

The **cost-of-failure floor** is the key insight: a stage does not cap requirements. An MVP handling
*payments* inherits the financial obligation (Section 3.6) immediately, regardless of stage.

## Worked example

An MVP of **Acme SaaS** exposes `POST /invoices`. The minimal correct implementation:

```ts
// ✅ MVP-correct: explicit outcome, one boundary, no fake success, correlation id.
app.post("/invoices", async (req, res) => {
  const requestId = req.header("x-request-id") ?? randomUUID();
  try {
    const parsed = CreateInvoiceSchema.parse(req.body);      // explicit validation
    const invoice = await invoices.create(parsed);
    res.status(201).json({ id: invoice.id, requestId });
  } catch (err) {
    if (err instanceof ZodError) {
      return res.status(422).json({ code: "VALIDATION_FAILED", requestId,
                                    fields: err.issues.map(i => ({ path: i.path, message: i.message })) });
    }
    log.error({ err, requestId }, "invoice create failed");
    res.status(500).json({ code: "INTERNAL", requestId });    // fail loud, not fake success
  }
});
```

An MVP that returns `200 {"ok":false}` here would need a breaking change to fix later.

## Key data / numbers

| Item | Value | Stage relevance |
| ---- | ----- | --------------- |
| Request ID header | `X-Request-Id` (common convention) | MVP onward |
| Validation status | `422` | MVP onward |
| Retry attempts | 3–5 + exponential backoff + jitter | Startup onward |
| Error budget | e.g. 99.9% → ~43m/month | Enterprise |
| Stripe idempotency TTL | 24h | Startup (payments) |
| SLO target (typical SaaS) | 99.9% API availability | Enterprise |
| Audit retention | commonly 1–7 years | Enterprise (varies by regime) |

## Real-world use case — Acme SaaS

Acme's MVP returned `{ "success": false }` with HTTP `200` for validation errors, because it was
"fastest." By the time they had enterprise customers, mobile and partner clients had coded against
that shape, and a compliance review required machine-readable codes for its audit log. The
migration to proper `4xx` responses + codes took a quarter of coordinated client work — work that
would have cost an afternoon at MVP. The lesson: **the cheap non-negotiables are cheap only early**.

## Trade-offs

| Stage | Reliable | Fast to build | Complexity |
| ----- | -------- | ------------- | ---------- |
| MVP | Explicit errors, one boundary | High | Low |
| Startup | + consistency, retries, idempotency | Medium | Medium |
| Enterprise | + contracts, isolation, DR, audit | Low | High |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Build the cheap non-negotiables at MVP | Defer explicit errors and request IDs |
| Add consistency at first real load | Let every endpoint invent a shape |
| Version contracts before enterprise clients | Break clients without deprecation |
| Let cost-of-failure set the floor | Let "we're an MVP" excuse payment bugs |

## Common mistakes

- **`200` for errors** at MVP — the most expensive shortcut.
- **Stage as an excuse** for skipping payment idempotency.
- **Enterprise tooling at MVP** — sagas and registries before customers.
- **No request IDs** — every future debug is blind.

## Checklist

- [ ] Are errors explicit at every stage, including MVP?
- [ ] Is there exactly one catch-all boundary from day one?
- [ ] Do writes that clients retry have idempotency before real customers?
- [ ] Are public contracts versioned before enterprise commitments?
- [ ] Has cost-of-failure set a floor above the stage baseline?

## Related

- [Requirements by Architecture and Risk Profile](./02-requirements-by-architecture-and-risk-profile.md)
- [Choosing a Maturity Level](./03-balancing-and-choosing-your-maturity-level.md)
- [Chapter 61 — Maturity Model](../../../part-24-repeatable-blueprint/61-error-handling-maturity-model/README.md)
- [Glossary: error budget](../../../GLOSSARY.md)
