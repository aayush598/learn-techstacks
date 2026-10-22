# Requirements by Architecture and Risk Profile

> Part I · Chapter 3 · Sections 3.4, 3.5, 3.6, 3.7, 3.8, 3.9 · _Estimated reading time: 26 min_

## In one sentence

Beyond product stage, each architecture and risk profile adds **specific, non-optional
obligations** — isolation for multi-tenant, idempotency for financial, deadlines for real-time,
provider abstraction for AI, bounded retries for background processing.

## Why this matters in production

Two products can be the same stage but have different requirements because of *what they are*. A
multi-tenant tool that leaks tenant A's data into tenant B's error message has a breach, not a bug.
A financial flow that double-charges during a retry loses money and trust. Recognizing the profile
is how you pull in the safeguard *before* the incident, not after.

## Core concept — six profiles, six obligations

### 3.4 Multi-tenant

**Obligation: strict isolation and noisy-neighbor control.**

- Every error, log, and response is scoped to the **tenant**; no cross-tenant leakage (Chapter 34/35).
- **Per-tenant fair-share** — one tenant's failure cannot starve others (bulkheads, quotas).
- Tenant context is validated at the boundary and carried through (correlation + tenant ID).

```ts
// ✅ Tenant derived from the authenticated principal, never from client input.
const tenantId = principal.tenantId;      // from token/session
const doc = await docs.find({ id, tenantId }); // scoped query
if (!doc) throw new NotFoundError({ resource: "document" }); // never reveals cross-tenant existence
```

### 3.5 High-availability

**Obligation: bounded blast radius, graceful degradation, and fast recovery.**

- **No single point of failure** on the critical path; redundant dependencies.
- **Timeouts and circuit breakers** everywhere (Chapter 29).
- **Degrade optional features**, fail-fast critical ones (Chapter 30).
- **SLOs and error budgets** drive how aggressively to fail vs degrade.

### 3.6 Financial / transactional

**Obligation: idempotency, exactly-once side effects, auditability.**

- **Idempotency keys** on every money-moving call (Chapter 28).
- **No duplicate charges** across retries; ambiguous outcomes resolved by lookup, not guess.
- **Compensation** for partial multi-step workflows (sagas, Chapter 39).
- **Immutable audit trail** of attempts and outcomes.

### 3.7 AI-powered

**Obligation: provider abstraction, bounded spend, safe failure.**

- Distinguish **provider errors** (`429`, quota, timeout) from **app errors** (bad prompt, schema).
- **Fallback models** and honest degraded output; never present fabricated content as fact.
- **Token/cost limits** and cancellation; retries must be idempotent or side-effect-free.

### 3.8 Real-time

**Obligation: deadlines, backpressure, ordering, and reconnect.**

- **Deadline propagation** end-to-end; a late result is a failure (Chapter 29).
- **Backpressure** instead of unbounded queues; drop/coalesce rather than stall.
- **Reconnect and resume** with sequence numbers; handle duplicate and out-of-order delivery.

### 3.9 Background processing

**Obligation: durable retries, DLQ, checkpointing, at-least-once safety.**

- **Retryable vs terminal** classification; **max attempts** + backoff (Chapter 32).
- **Dead-letter queue** with preserved context for poison messages.
- **Checkpointing/resume** for long jobs; idempotent processing for duplicate delivery.

## How it works (mechanics) — profile → safeguard

```text
  Profile              Primary failure risk          Required safeguard
  ───────              ────────────────────          ──────────────────
  multi-tenant         cross-tenant leakage          tenant-scoped everything
  high-availability    cascading outage              timeouts + breakers + degrade
  financial            duplicate/lost money          idempotency + compensation + audit
  AI                    runaway cost, bad output     provider abstraction + limits + fallback
  real-time            stale/late results            deadlines + backpressure + resume
  background           poison message, lost job      DLQ + checkpoint + bounded retry
```

A product can hold several profiles at once — and then must satisfy **the union** of obligations.

## Worked example — Acme SaaS satisfies three profiles at once

Acme is multi-tenant, has background exports, and includes an AI summary.

```ts
// Multi-tenant + AI profile in one call: tenant isolation and honest AI failure.
async function summarizeForTenant(principal: Principal, docId: string) {
  const doc = await docs.find({ id: docId, tenantId: principal.tenantId }); // 3.4 isolation
  if (!doc) throw new NotFoundError({ resource: "document" });              // no cross-tenant hint
  try {
    return await llm.summarize(doc.text, {
      maxTokens: 1024,                 // 3.7 bounded spend
      timeoutMs: 8_000,                // 3.5/3.8 deadline
      fallbackModel: "small-fast",     // 3.7 fallback
    });
  } catch (err) {
    if (err instanceof LLMQuotaError) return { summary: null, degraded: "quota" }; // honest degrade
    throw new SummarizationUnavailable({ cause: err });                            // preserve cause
  }
}
```

The export path (`ExportJob`) adds the background obligations: checkpoint + DLQ + idempotent writes.

## Key data / numbers

| Profile | Key value | Meaning |
| ------- | --------- | ------- |
| Multi-tenant | `tenant_id` in every query | Prevents cross-tenant access |
| High-availability | timeout < caller's deadline | No cascade (e.g. 2s call under 5s budget) |
| Financial | idempotency key TTL 24h (Stripe) | Collapses duplicate charges |
| Financial | SQLSTATE `40001` retryable | Serialization retry, never re-charge |
| AI | provider `429` + `Retry-After` | Retry vs fallback decision |
| Real-time | max end-to-end deadline | A late result is discarded |
| Background | max attempts (commonly 5), then DLQ | Bounded retries, poison handling |

## Real-world use case — Acme SaaS

Acme's `ExportJob` processed tenant exports on a shared worker pool with no per-tenant limit. One
enterprise tenant queued a 40-million-row export, exhausting the pool and starving every other
tenant's jobs — a textbook noisy neighbor (3.4) manifesting as a background-processing outage (3.9).
The fix combined two profiles: **per-tenant concurrency limits** (isolation) and a **separate
priority queue with checkpoints** (background). Small tenants' exports returned to normal latency,
and the giant export completed with resume without blocking anyone. Requirements came from the
*profiles*, not from the stage.

## Trade-offs

| Profile | Adds reliability | Adds complexity | Skip only if… |
| ------- | ---------------- | --------------- | ------------- |
| Multi-tenant | Isolation | Scoping everywhere | Single-tenant forever |
| High-availability | Uptime | Redundancy + breakers | Internal, low-stakes tool |
| Financial | Correctness | Idempotency + saga | No money/data movement |
| AI | Cost/output safety | Provider layer + limits | No LLM in product |
| Real-time | Freshness | Deadlines + backpressure | Batch-only UI |
| Background | Durability | DLQ + checkpoints | Fully synchronous |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Derive safeguards from profiles, not stage | Assume small stage means no obligations |
| Scope every query/error/log by tenant | Derive tenant from client input |
| Make money operations idempotent | Retry a charge without a key |
| Bound AI cost and time | Let an LLM call run unbounded |
| Set deadlines shorter than the caller's | Propagate without a budget |

## Common mistakes

- **Leaking other tenants' data** through error messages or existence hints.
- **Shared pools with no per-tenant limits** — noisy neighbor.
- **Retrying payments without idempotency** — double charges.
- **Unbounded background retries** — poison message blocks the queue.
- **Late real-time results treated as success.**

## Checklist

- [ ] Is every query, log, and error tenant-scoped?
- [ ] Do optional and critical dependencies have different postures?
- [ ] Are all money operations idempotent and audited?
- [ ] Are AI calls bounded in tokens, time, and cost?
- [ ] Do real-time paths set and propagate deadlines?
- [ ] Do background jobs retry boundedly, checkpoint, and DLQ?

## Related

- [Requirements by Product Stage](./01-requirements-by-product-stage.md)
- [Multi-Tenancy, Isolation, and High Availability — Deep Dive](../02-deep-dive/01-multi-tenancy-isolation-and-high-availability.md)
- [Chapter 28 — Idempotency](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Chapter 44 — AI, LLM, and Tool-Calling Errors](../../../part-16-specialized-saas-scenarios/44-ai-llm-and-tool-calling-application-errors/README.md)
