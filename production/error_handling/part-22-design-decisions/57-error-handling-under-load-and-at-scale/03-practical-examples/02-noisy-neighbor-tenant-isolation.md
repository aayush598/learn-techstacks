# Noisy-Neighbour Tenant Isolation for Acme SaaS

> Part XXII · Chapter 57 · Sections 57.4, 57.9, 57.10, 57.11 (applied) · _Estimated reading time: 24 min_
> **Prerequisite:** [Isolation: Tenants, Features, and Dependencies](../01-concepts/02-isolation-tenants-features-dependencies.md)

## In one sentence

A complete **multi-tenant isolation layer** for Acme SaaS: per-tenant fairness, per-tenant
circuit breakers, per-tenant budgets, and the degraded mode that keeps one tenant's
outage from becoming everyone's.

## Why this matters in production

"Noisy neighbour" is the failure mode of every multi-tenant system, and it is invisible
until one customer writes 10× more data than the next ten. Then the expensive customer's
export job holds the shared Postgres pool for minutes, and 200 other tenants see
timeouts.

The reason it stays invisible is that **the resource is shared and the limits are not**.
The fix is not to give every tenant a dedicated database (it is a SaaS product; that is not
on the table). The fix is to make the sharing *fair and bounded*: every tenant gets a
guaranteed share, and excess demand is rejected or queued rather than allowed to consume
the common pool.

## The isolation model

Acme isolates at five levels:

| Level | Isolates | Mechanism | Limit |
| ----- | -------- | --------- | ----- |
| 1. Concurrency | In-flight work per tenant | Per-tenant semaphore | 10 (standard), 100 (enterprise) |
| 2. Rate | Request rate per tenant | Token bucket per tenant | 50 rps (standard), 500 rps (enterprise) |
| 3. Queue depth | Queued work per tenant | Per-tenant queue | 10 messages |
| 4. Circuit breaker | Fault domain per tenant→dependency | Per-tenant breaker | 50% failures / 20 requests |
| 5. Resource | CPU, memory, log volume | Per-tenant quotas and sampling | 1% CPU, 50 MB logs |

Levels 1–3 are **admission** (prevent excess from entering). Levels 4–5 are **containment**
(limit the damage once excess is inside).

> **The order matters.** The circuit breaker must be per-tenant, not global, or one tenant's
> broken integration opens the breaker for everybody. This was Acme's second incident.

## Implementation

### Level 1 + 2 — per-tenant concurrency and rate

```ts
export type TenantTier = "standard" | "enterprise";

export interface TenantQuota {
  concurrency: number;
  ratePerSecond: number;
  burst: number;
  queueDepth: number;
  cpuShare: number;          // fraction of the instance's CPU this tenant may use
  logBytesPerHour: number;
}

export const QUOTAS: Record<TenantTier, TenantQuota> = {
  standard: {
    concurrency: 10,
    ratePerSecond: 50,
    burst: 100,
    queueDepth: 10,
    cpuShare: 0.01,          // 1%
    logBytesPerHour: 10 * 1024 * 1024,
  },
  enterprise: {
    concurrency: 100,
    ratePerSecond: 500,
    burst: 1_000,
    queueDepth: 10,
    cpuShare: 0.10,          // 10%
    logBytesPerHour: 200 * 1024 * 1024,
  },
};

export class TenantGovernor {
  private readonly concurrency = new Map<string, Semaphore>();
  private readonly buckets = new Map<string, TokenBucket>();
  private readonly queues = new Map<string, number>();

  constructor(private readonly quotas: Record<TenantTier, TenantQuota>) {}

  async admit(tenantId: string, tier: TenantTier): Promise<Admission> {
    const quota = this.quotas[tier];

    // 1. Rate limit (cheap check, rejects bursts before any resource is taken).
    const bucket = this.bucket(tenantId, quota);
    if (!bucket.tryConsume(1)) {
      return { ok: false, code: "TENANT_RATE_LIMITED", status: 429, retryAfterSeconds: 2 };
    }

    // 2. Concurrency limit.
    const sem = this.semaphore(tenantId, quota.concurrency);
    if (!sem.tryAcquire()) {
      // 3. Queue the overflow, up to the tenant's queue depth.
      const depth = (this.queues.get(tenantId) ?? 0) + 1;
      if (depth > quota.queueDepth) {
        return { ok: false, code: "TENANT_QUEUE_FULL", status: 429, retryAfterSeconds: 5 };
      }
      this.queues.set(tenantId, depth);
      try {
        await sem.acquire();       // wait for a slot
      } finally {
        this.queues.set(tenantId, (this.queues.get(tenantId) ?? 1) - 1);
      }
    }

    let released = false;
    return {
      ok: true,
      release: () => {
        if (released) return;
        released = true;
        sem.release();
      },
    };
  }

  private semaphore(tenantId: string, limit: number): Semaphore {
    let sem = this.concurrency.get(tenantId);
    if (!sem) {
      sem = new Semaphore(limit);
      this.concurrency.set(tenantId, sem);
    }
    return sem;
  }

  private bucket(tenantId: string, quota: TenantQuota): TokenBucket {
    let b = this.buckets.get(tenantId);
    if (!b) {
      b = new TokenBucket(quota.ratePerSecond, quota.burst);
      this.buckets.set(tenantId, b);
    }
    return b;
  }
}
```

### Level 4 — per-tenant circuit breakers

This is the level that was wrong in Acme's original design (a single global breaker per
dependency) and the level that caused the second incident.

```ts
export class TenantBreaker {
  private readonly state = new Map<string, BreakerState>();   // key: tenantId|dependency

  constructor(
    private readonly thresholds: {
      failureRatio: number;    // 0.50
      minimumRequests: number;// 20
      cooldownMs: number;     // 30_000
      halfOpenProbes: number; // 3
    },
  ) {}

  private key(tenantId: string, dependency: string): string {
    return `${tenantId}|${dependency}`;
  }

  async call<T>(tenantId: string, dependency: string, fn: () => Promise<T>): Promise<T> {
    const key = this.key(tenantId, dependency);
    const s = this.state.get(key) ?? { failures: 0, total: 0, openedAt: 0, probes: 0 };

    // Open: refuse without calling the dependency.
    if (s.openedAt > 0) {
      if (Date.now() - s.openedAt < this.thresholds.cooldownMs) {
        throw new CircuitOpenError({ tenantId, dependency, retryAfterSeconds: 5 });
      }
      // Cooldown elapsed: allow limited probes.
      if (s.probes >= this.thresholds.halfOpenProbes) {
        throw new CircuitOpenError({ tenantId, dependency, retryAfterSeconds: 5 });
      }
      s.probes++;
    }

    s.total++;
    try {
      const result = await fn();
      this.state.set(key, { failures: 0, total: s.total, openedAt: 0, probes: 0 });
      return result;
    } catch (err) {
      s.failures++;
      const ratio = s.failures / Math.max(s.total, 1);
      if (s.total >= this.thresholds.minimumRequests && ratio >= this.thresholds.failureRatio) {
        s.openedAt = Date.now();
        s.probes = 0;
        metrics.gauge("breaker.open", 1, { tenant: tenantId, dependency });
      }
      this.state.set(key, s);
      throw err;
    }
  }
}
```

The key property: **the state key includes the tenant**, so tenant A's broken Stripe
account opens only tenant A's breaker. Tenant B's Stripe traffic is unaffected.

### Level 5 — resource containment

```ts
// ✅ Bound the log volume a tenant can consume, per hour.
export class TenantLogBudget {
  private readonly used = new Map<string, number>();

  constructor(private readonly maxBytesPerHour: number) {}

  allow(tenantId: string, bytes: number): boolean {
    const used = (this.used.get(tenantId) ?? 0) + bytes;
    if (used > this.maxBytesPerHour) return false;

    const hour = Math.floor(Date.now() / 3_600_000);
    this.used.set(tenantId, used);
    metrics.gauge("tenant.log_bytes_hour", used, { tenant: tenantId, hour });
    return true;
  }
}
```

When the budget is exhausted, the log line is dropped and a counter increments — the
tenant's errors become invisible in logs but the system stays healthy. This is a
deliberate trade: a noisy tenant loses observability before it loses capacity.

## Worked example — the `$12k/month` tenant

Acme has a customer, *Northwind*, on the enterprise tier: 5,000 users, 2,000 webhook
events/second, and a nightly export of 4 million rows.

**The incident (before isolation):**

| Time | Event |
| ---- | ----- |
| 02:00 | Northwind's nightly export starts: 4M rows, streamed in 500-row pages. |
| 02:00:05 | The export holds 20 of 20 Postgres connections for 18 minutes. |
| 02:00:05 | Every other tenant's requests wait for a connection; p99 hits 30 s. |
| 02:01 | Health checks fail; all instances restart. |
| 02:18 | The export finishes — the connection pool had recovered on its own. |
| 02:19 | The alert fires: "database connection pool exhausted". |
| — | 412 support tickets in 20 minutes. |

**The alert was 19 minutes late.** The pool saturation signal existed at 02:00:05; the
alert was configured on a 1-minute error-rate window, and the requests had not *errored* —
they were **waiting**. That is the lesson: **saturation must be alerted on directly, not
inferred from error rate.**

**After isolation:**

| Control | Effect on Northwind's export |
| ------- | ---------------------------- |
| Per-tenant concurrency (100 for enterprise) | The export uses at most 100 in-flight requests |
| Per-tenant queue depth (10) | Overflow is rejected with `429`, not queued forever |
| Per-tenant rate limit (500 rps) | The export is throttled to 500 rps |
| Export-specific bulkhead (5 workers) | Exports never exceed 5 concurrent jobs |
| Pool bulkhead (20) | The 20 connections are shared, but a tenant can hold at most 5 for exports |
| Chunky pagination (500 → 100 rows) | Fewer round trips, shorter lock holds |

Result: the export takes 4.2× longer (75 minutes instead of 18) but **no other tenant was
affected**. The p99 for other tenants stayed at 180 ms. Northwind received a proactive
email: "Your export is scheduled during off-peak hours; contact support to move it."

**The important part is the design change, not the tuning:** exports are a **P2 workload
with a dedicated bulkhead**. Before, an export could consume the entire pool. After, it
can consume at most 5 of 20 connections — a hard 25% ceiling.

## The degraded mode

When the system cannot serve a tenant at full fidelity, the choice is between rejecting and
degrading. Acme's rule:

| Situation | Response |
| --------- | -------- |
| Tenant exceeds its own quota | `429` + `Retry-After` — the tenant can fix it |
| Shared resource saturated | `503` + `Retry-After` — retry later |
| Optional feature (P3) unavailable | `200` with `degraded: true` |
| Read replica lagging | Serve from the replica anyway, mark `stale: true` |
| Analytics unavailable | Serve the cached page, mark `cachedAt` |

```ts
export function degradedPage<T>(payload: T, reason: string, stale = false): T & { degraded: boolean; degradedReason: string } {
  return { ...payload, degraded: true, degradedReason: reason, ...(stale ? { stale: true } : {}) };
}
```

The `stale` flag matters for read-after-write flows: a client that sees `stale: true` knows
to re-read before making a decision.

## Key data / numbers

| Item | Value | Notes |
| ---- | ----- | ----- |
| Per-tenant concurrency (standard) | 10 | Per instance |
| Per-tenant concurrency (enterprise) | 100 | Per instance |
| Per-tenant rate limit (standard) | 50 rps, burst 100 | |
| Per-tenant rate limit (enterprise) | 500 rps, burst 1,000 | |
| Per-tenant queue depth | 10 | Beyond this: `429` + `Retry-After: 5` |
| Breaker scope | Per `tenantId\|dependency` | Never global |
| Breaker open threshold | 50% failures over ≥ 20 requests | |
| Breaker cooldown | 30 s | |
| Half-open probes | 3 | |
| Tenant CPU share | 1% standard, 10% enterprise | |
| Tenant log budget | 10 MB/h standard, 200 MB/h enterprise | |
| Export bulkhead | 5 concurrent jobs | Hard ceiling, independent of tier |
| Tenant queue wait limit | 5 s | Then `429` — do not wait indefinitely |
| Isolation slack | N instances × per-tenant limit | Documented; 24 instances → 240 effective |
| Saturation alert | Direct, ≤ 10 s window | Not inferred from error rate |

## Real-world use case — `ExportJob` and `AgentRun` (Acme SaaS)

Two workloads sat on the same Postgres pool, and they had opposite requirements:

| Workload | Duration | Concurrency needed | Can be queued? |
| -------- | -------- | ------------------ | -------------- |
| `ExportJob` (Northwind) | 75 min | 1–5 | Yes — a queue is natural |
| `AgentRun` (per-user AI) | 30–90 s | Many (thousands) | Barely — users are waiting |
| `Checkout` | 200 ms | Many | No — must fail fast |

The naive design gave all three the same pool. The isolated design:

```text
  pool (20 connections)
    ├── export bulkhead (5)   → 25% of the pool, 1 tenant
    ├── agent bulkhead (5)    → 25% of the pool, LLM-limited anyway
    └── general traffic (10)  → 50% of the pool, everything else
```

With this split, Northwind's export cannot starve `Checkout` even at peak. Before, the
export consumed 100% of the pool for 18 minutes.

The `AgentRun` bulkhead of 5 also serves as the LLM bulkhead: 5 concurrent agent runs × 12
LLM calls each = 60 concurrent LLM requests, which is the provider's negotiated limit. The
two limits are the same number for the same reason.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Key the breaker by `tenantId\|dependency` | Use one global breaker per dependency |
| Alert on saturation directly, within 10 s | Wait for the error rate to rise |
| Give expensive workloads a dedicated bulkhead | Let them share the general pool |
| Reject a tenant that exceeds its own quota | Let it consume shared capacity |
| Bound the tenant queue wait (5 s) | Let requests wait indefinitely for a slot |
| Mark degraded responses explicitly | Serve stale data silently |
| Cap the log volume per tenant | Let one tenant's errors saturate the log pipeline |
| Document the isolation slack (N instances) | Assume the per-tenant limit is exact |

## Common mistakes

- **A global circuit breaker.** One tenant's broken integration then blocks every tenant.
- **Alerting on errors instead of saturation.** A pool that is 100% utilized produces
  *waiting*, not errors — the alert fires minutes after the incident starts.
- **The same quota for every tier.** A fair share is not the same as an equal share.
- **A tenant queue with no depth limit.** The queue just becomes the outage.
- **A tier-based limit that ignores the fleet size.** With 24 instances, a "10 concurrent"
  limit is 240 in practice.
- **Unbounded log volume per tenant.** A tenant with a broken integration can produce
  millions of error lines per minute.
- **Isolation without measurement.** Without per-tenant saturation metrics you cannot prove
  isolation works — and you will not believe it when it is under pressure.

## Checklist

- [ ] Every tenant has a tier with explicit concurrency, rate, queue-depth, CPU, and log quotas.
- [ ] The circuit-breaker state key includes the tenant.
- [ ] Saturation alerts fire directly, within 10 s, per resource.
- [ ] Expensive workloads have dedicated bulkheads with hard ceilings.
- [ ] Tenant queue waits are bounded (5 s) before rejection.
- [ ] Rejections for quota violations use `429` + `Retry-After`.
- [ ] Degraded responses carry `degraded: true` and, where relevant, `stale: true`.
- [ ] Per-tenant log volume is capped.
- [ ] The effective limit (per-instance × instance count) is documented.
- [ ] A per-tenant saturation dashboard exists.

## Related

- [Load Shedding and Admission Control](./01-load-shedding-and-admission-control-acme.md)
- [Isolation: Tenants, Features, and Dependencies](../01-concepts/02-isolation-tenants-features-dependencies.md)
- [Scaling and Instance Consistency](../01-concepts/05-scaling-and-instance-consistency.md)
- [Chapter 31 — Multi-Tenant Systems](../../../part-12-multi-tenant-and-saas/31-multi-tenant-systems/README.md)
