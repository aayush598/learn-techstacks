# Multi-Tenancy, Isolation, and High Availability — Requirements in Depth

> Part I · Chapter 3 · Sections 3.4, 3.5 · _Estimated reading time: 22 min_

## In one sentence

Multi-tenancy requires that **one tenant's failures, load, and data can never affect another**, and
high availability requires that **one component's failure cannot take down the whole** — both are
blast-radius problems solved by isolation and bounded failure domains.

## Why this matters in production

In a single-tenant system, a bug affects one customer. In a multi-tenant system, the same bug — an
unscoped query, an unbounded job, a shared pool — affects *every* customer at once and may cross a
data boundary, turning an outage into a breach. This deep dive turns the two obligations from
Chapter 3 into concrete isolation mechanics and the failure domains they protect.

## Core concept — tenant as a failure domain

A tenant is both a **security boundary** (data) and a **failure domain** (load and blast radius).

```text
┌──────────────────── Shared infrastructure (shared fate) ───────────────────┐
│                                                                            │
│  ┌─ Tenant A pool ──┐  ┌─ Tenant B pool ──┐  ┌─ Tenant C pool ──┐          │
│  │ quota: 10 jobs   │  │ quota: 10 jobs   │  │ quota: 10 jobs   │          │
│  │ data: A only     │  │ data: B only     │  │ data: C only     │          │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘          │
│                                                                            │
│  Shared: DB cluster, Redis, HTTP client? ← if unbounded, shared fate       │
└────────────────────────────────────────────────────────────────────────────┘
```

Isolation is layered: **query scoping** (correctness), **per-tenant limits** (fairness), and
**per-tenant pools/partitions** (blast radius).

## How it works (mechanics)

### Layer 1 — Query and response scoping (prevents leakage)

Every read/write carries the tenant from the authenticated principal. Never trust a client-supplied
tenant ID.

```sql
-- ✅ Tenant scoping is structural, not optional.
SELECT id, title FROM documents
WHERE tenant_id = $1 AND id = $2;   -- $1 comes from the session, never the request body
```

A missing row returns `404`, **not** `403`, so existence of another tenant's resource is not
revealed (Chapter 35).

### Layer 2 — Fair-share limits (prevents noisy neighbors)

| Limit | Protects against |
| ----- | ------------------ |
| Requests/sec per tenant | API saturation |
| Concurrent jobs per tenant | Worker pool starvation |
| Rows/bytes per export | Storage/compute hogging |
| LLM tokens/day per tenant | Cost runaway |

Limits return `429 Too Many Requests` with `Retry-After`, scoped to the offending tenant only.

### Layer 3 — Partitioning/bulkheads (bounds blast radius)

- **Separate connection pools** or schemas per tier (enterprise vs free).
- **Separate queues/priority classes** for large jobs.
- **Cell-based deployment** for the largest customers (Chapter 57).

### High availability — bounding component failure

```text
  Request path (must stay up)            Optional path (may degrade)
  ─────────────────────────              ───────────────────────────
  auth        → fail-safe (deny)         recommendations → degrade
  primary DB  → fail-fast (503)          LLM summary     → degrade
  payments    → fail-fast (503)          activity feed   → cached/degrade
```

HA requirements in practice:

1. **Timeouts on every external call**, shorter than the caller's budget.
2. **Circuit breakers** to stop hammering a failing dependency.
3. **Redundancy** (replicas, multi-AZ) with **failover** on the critical path.
4. **SLOs and error budgets** to decide fail-fast vs degrade under load.
5. **Load shedding** (reject early with `503`) instead of collapsing under saturation.

## Edge cases

| Situation | Risk | Handling |
| --------- | ---- | -------- |
| Tenant ID from request body | Cross-tenant write | Ignore it; use the session's tenant |
| Shared cache key without tenant | Data leak | Prefix cache keys with tenant ID |
| Shared HTTP client to a tenant-specific endpoint | Credential mixups | Per-tenant clients/credentials |
| One tenant's huge export | Pool starvation | Per-tenant concurrency cap + priority queue |
| Retry storm across tenants | Cascading failure | Retry budget + jitter (Chapter 27) |
| Failover during a tenant's txn | Ambiguous outcome | Idempotency before retry (Chapter 23) |

## Worked example — a scoped, isolated, available endpoint

```ts
async function getReport(principal: Principal, reportId: string) {
  await rateLimit.check(principal.tenantId, "reports:read");     // 3.4 fair share
  const report = await reports.find({ id: reportId, tenantId: principal.tenantId }); // scoped
  if (!report) throw new NotFoundError({ resource: "report" });  // no existence leak
  return report;
}

async function renderDashboard(principal: Principal) {
  const report = await getReport(principal, principal.defaultReportId); // critical
  let widgets: Widget[] = [];
  try {
    widgets = await widgetService.list(principal);               // optional
  } catch (err) {
    log.warn({ err, tenantId: principal.tenantId }, "widgets degraded"); // 3.5 degrade
  }
  return { report, widgets, degraded: widgets.length === 0 };
}
```

## Key data / numbers

| Item | Value | Purpose |
| ---- | ----- | ------- |
| Cross-tenant access | `404` (not `403`) | Avoid existence disclosure |
| Rate limit response | `429` + `Retry-After` | Fair share |
| Per-tenant job concurrency | commonly 5–20 workers | Stop noisy neighbor |
| Timeout | less than caller's deadline | Prevent cascade |
| Circuit breaker | open after ~5 failures, half-open probe | Protect dependency |
| Load shed | `503` early | Survive saturation |
| HA target | 99.9% ≈ 43 min/month | Error budget |

## Real-world use case — Acme SaaS

Acme's `WebhookIngest` stored raw Stripe events in a shared Redis key `event:{id}` without a tenant
prefix. Two tenants happened to receive events with overlapping provider IDs during a Stripe retry
window; tenant B's worker read tenant A's cached payload and updated the wrong account — a
**cross-tenant correctness breach** caused by a shared cache key (Layer 3 isolation missing). The fix
was mechanical: prefix all cache and queue keys with `tenantId`, add a per-tenant webhook worker
quota, and return `404` rather than `403` on scoped misses. The same architecture, made
tenant-aware, closed the breach.

## Trade-offs

| Isolation level | Leak safety | Blast radius | Complexity |
| --------------- | ----------- | ------------ | ---------- |
| Scoped queries only | High | Shared pools | Low |
| + per-tenant limits | High | Bounded per tenant | Medium |
| + per-tenant pools/queues | High | Isolated | High |
| + cells per tenant | Highest | Minimal | Highest (large tenants only) |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Derive tenant from the principal | Accept tenant ID from the body |
| Prefix cache/queue keys with tenant | Share scoped keys |
| Cap per-tenant concurrency | Let one job monopolize the pool |
| Set timeouts below caller budgets | Leave external calls unbounded |
| Return `404` on scoped miss | Return `403` and reveal existence |

## Common mistakes

- **Unscoped queries** that pass tests because every test uses one tenant.
- **Shared pools without limits** — noisy neighbor by design.
- **No timeouts** — one slow dependency stalls everything.
- **Cache key collisions** across tenants.
- **Failover without idempotency** — ambiguous outcomes on retry.

## Checklist

- [ ] Is tenant context derived from the session, not the request?
- [ ] Are all queries, caches, and queues tenant-scoped?
- [ ] Does every tenant have fair-share limits?
- [ ] Do all external calls have timeouts below their caller's budget?
- [ ] Are critical and optional paths assigned distinct postures?
- [ ] Are scoped misses returned as `404`?

## Related

- [Requirements by Architecture and Risk Profile](../01-concepts/02-requirements-by-architecture-and-risk-profile.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Chapter 35 — Auth, Authz, and Tenant Isolation Errors](../../../part-13-security-aware/35-auth-authorization-and-tenant-isolation-errors/README.md)
- [Chapter 57 — Error Handling Under Load and at Scale](../../../part-22-design-decisions/57-error-handling-under-load-and-at-scale/README.md)
