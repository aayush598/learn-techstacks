# Isolation: Tenants, Features, and Dependencies

> Part XXII · Chapter 57 · Sections 57.4, 57.9, 57.10, 57.11 · _Estimated reading time: 22 min_
> **Prerequisite:** [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)

## In one sentence

**Isolation means one workload's failure cannot consume another's capacity** — and it is
implemented with *separate pools and per-tenant limits*, not with hopes about traffic
shaping.

## Why this matters in production

Acme SaaS is multi-tenant: 4,000 customers, one deployment, one Postgres, one Redis, one
worker pool. In a shared-everything architecture, a single tenant's mistake becomes everyone's
outage:

- A tenant uploads a 2 GB file in 40,000 pieces, each triggering 3 storage calls. Their
  traffic consumes 70% of the connection pool; every other tenant now sees "too many
  clients".
- A tenant starts a bulk export every minute. The export queue's backlog grows, workers
  spend their time on exports, and interactive webhooks (which share the worker pool) fall
  behind.
- A tenant's malformed payloads cause a validation failure storm that saturates the CPU with
  error handling, and the *valid* requests of other tenants get slower.

None of these is a "bug" in the application logic. They are **shared fate** — the failure
domain of Chapter 1 — and the cure is to break the sharing.

## Core concept

### 57.4 — Pool exhaustion

Pool exhaustion is the most common way a *healthy* dependency is taken down.

```text
  Normal:   20 in-flight   ████░░░░░░░░░░░░░░░░  pool 20
  Storm:    20 in-flight   ████████████████████  pool 20  → new callers wait
  Deadlock: 20 in-flight   ████████████████████  pool 20  → new callers wait
                                   │
                                   ▼
              waiters accumulate → request latency grows
              → callers time out → callers retry → pool waits longer
              → MORE waiters                                     ← feedback loop
```

The mechanism: **a slow dependency does not fail fast by default**. If your timeout is 30 s
and the dependency takes 29 s, you hold a connection for 29 s. At 1 rps of arrivals with 20
connections, the pool is exhausted after 20 seconds — and the system is now failing with
"too many clients" even though the database is perfectly healthy.

Three things must be true for a pool to survive a slow dependency:

| Requirement | Value | Why |
| ----------- | ----- | --- |
| The timeout is **shorter** than the dependency's healthy p99 | timeout ≤ p99 | Otherwise slow-but-alive requests consume the pool |
| The pool has **headroom** for retries | max ≥ 1.5 × peak RPS × p95 latency | Retries must not be able to empty it |
| Queued waiters are **bounded** | `acquireTimeoutMs` ≤ 250 ms | Waiting is a failure, not patience |

```ts
// ✅ A pool that fails fast instead of queueing forever.
const pool = new Pool({
  max: 20,
  connectionTimeoutMillis: 250,   // wait at most 250 ms for a connection
  idleTimeoutMillis: 30_000,
  statement_timeout: 5_000,       // server-side kill switch
});
```

The fourth line is the one teams miss: a **server-side `statement_timeout`** is the only way
to guarantee that a query that ignores client-side cancellation cannot hold a connection
indefinitely.

### 57.9 — Tenant isolation

Three levels of tenant isolation, cheapest first:

| Level | Mechanism | Cost | Protects against |
| ----- | --------- | ---- | ---------------- |
| **L1 — Quota** | Per-tenant request rate limit | Very low | One tenant's request volume |
| **L2 — Concurrency** | Per-tenant in-flight limit | Low | One tenant's *long* requests |
| **L3 — Resource** | Dedicated pool/queue/instance per tenant tier | High | One tenant's *shape* of load |

Most SaaS products need **L1 + L2** for every tenant and **L3** only for enterprise tiers
that have contracted isolation.

```text
  Per-tenant concurrency limit (L2)

  tenant A (enterprise, limit 100):  ██████████░░░░░░░░░░  10/100
  tenant B (standard,   limit 20):  ████████████████████  20/20  ← saturated
  tenant C (standard,   limit 20):  ░░░░░░░░░░░░░░░░░░░░   0/20  ← unaffected ✅
```

The key property: **tenant B saturating does not reduce tenant C's capacity**. That only
holds if the limit is checked *before* the shared resource is acquired, and the limit is
per-tenant rather than global.

Concurrency limits also need a **queue**: without one, the 21st request of tenant B either
fails immediately (harsh) or waits (unbounded). A short bounded queue (say 10 per tenant)
absorbs bursts; beyond that, reject with `429` and a `Retry-After`.

### 57.10 — Feature isolation

Feature isolation is about **blast radius between capabilities of the same product**:

| Isolation unit | Example | Why |
| -------------- | ------- | --- |
| Separate **connection pool** per dependency | 20 for Postgres, 10 for Stripe, 5 for the LLM | A slow LLM call cannot empty the Postgres pool |
| Separate **worker pool** per job class | 4 export workers, 8 webhook workers | A poison export cannot starve webhook processing |
| Separate **queue** per job class | `exports`, `webhooks`, `notifications` | Backlog in one queue does not delay another |
| Separate **thread pool** per feature | AI summarization gets 4 threads | AI work cannot starve the request path |
| **Feature flag** to disable a feature | Turn off AI summaries | An optional feature can be removed from the request path |

The classic failure is a **shared HTTP client**. One client, one pool, three dependencies.
When the LLM provider starts responding in 30 s instead of 300 ms, all 20 sockets are held
by LLM calls, and the Stripe calls — which would have succeeded — cannot get a socket.

```ts
// ❌ One client for everything.
const http = new HttpClient({ maxSockets: 20 });

// ✅ One client per dependency: independent pools, independent breakers, independent budgets.
const clients = {
  stripe: new HttpClient({ maxSockets: 10, timeoutMs: 5_000 }),
  llm:    new HttpClient({ maxSockets: 5,  timeoutMs: 30_000 }),
  s3:     new HttpClient({ maxSockets: 10, timeoutMs: 10_000 }),
};
```

### 57.11 — One dependency exhausting shared resources

Even with per-dependency pools, one dependency can exhaust a **truly shared** resource:
the database, the Redis instance, the CPU, the file-descriptor table, the queue broker.

```text
                 ┌──────────────────────────────┐
   Stripe ──────►│                              │
   LLM ─────────►│   Postgres (pool of 20)      │  ← LLM calls write audit rows
   Exports ─────►│                              │     and hold connections
   Webhooks ────►│                              │
                 └──────────────────────────────┘
        The LLM's audit writes take 4 of the 20
        connections for the whole request duration.
```

Mitigations, in order of effectiveness:

1. **Separate pools per workload** — a dedicated pool for exports and analytics, separate
   from the request path.
2. **Shorten the dependency's hold time** — the LLM call should not hold a DB connection
   while it waits for the provider. Write the audit row *after* the provider responds, or
   use an outbox.
3. **Bound the concurrent dependency calls** — the LLM bulkhead is 5 concurrent; a
   background audit writer is 2 concurrent.
4. **Use a separate read replica** for analytics/export queries so they do not consume the
   primary's connections or its CPU.

> ⚠️ **Hazard.** **Holding a connection across a remote call** is the single most common way
> a slow dependency exhausts a healthy database pool. The rule: acquire the connection, do
> the database work, release it, *then* make the remote call — unless the two must be
> atomic, in which case use a transactional outbox.

## How it works (mechanics)

### Per-tenant concurrency limit with a bounded queue

```ts
export class TenantLimiter {
  private inFlight = new Map<string, number>();
  private queued = new Map<string, number>();

  constructor(
    private readonly limitPerTenant: number,
    private readonly queuePerTenant: number,
  ) {}

  tryAcquire(tenantId: string): { ok: true; release: () => void } | { ok: false; retryAfterSeconds: number } {
    const inFlight = this.inFlight.get(tenantId) ?? 0;
    const queued = this.queued.get(tenantId) ?? 0;

    if (inFlight < this.limitPerTenant) {
      this.inFlight.set(tenantId, inFlight + 1);
      let released = false;
      return {
        ok: true,
        release: () => {
          if (released) return;
          released = true;
          const n = (this.inFlight.get(tenantId) ?? 1) - 1;
          if (n <= 0) this.inFlight.delete(tenantId); else this.inFlight.set(tenantId, n);
        },
      };
    }

    if (queued < this.queuePerTenant) {
      this.queued.set(tenantId, queued + 1);
      return { ok: true, release: () => this.dequeue(tenantId) };
    }

    // Saturated: reject immediately with a bounded backoff.
    return { ok: false, retryAfterSeconds: 5 };
  }

  private dequeue(tenantId: string): void {
    const q = (this.queued.get(tenantId) ?? 1) - 1;
    if (q <= 0) this.queued.delete(tenantId); else this.queued.set(tenantId, q);
  }
}
```

> The in-flight map is **per instance**. With N instances, the effective limit is N ×
> `limitPerTenant`. That is usually acceptable — but it must be a conscious decision, not an
> accident (see 57.17).

### Bulkheads: one pool per dependency

```ts
const bulkheads = {
  postgres: new Bulkhead({ maxConcurrent: 20, queueMax: 40, acquireTimeoutMs: 250 }),
  stripe:   new Bulkhead({ maxConcurrent: 10, queueMax: 20, acquireTimeoutMs: 200 }),
  llm:      new Bulkhead({ maxConcurrent: 5,  queueMax: 10, acquireTimeoutMs: 100 }),
};
```

When a bulkhead is exhausted, it fails **immediately** with its own error code
(`DEPENDENCY_OVERLOADED`, mapped to `503` + `Retry-After`), rather than letting the request
wait for a slot that will never come.

### Releasing the connection before the remote call

```ts
// ❌ Holds a DB connection for the whole LLM call (up to 30 s).
async function summarizeAndStore(taskId: string) {
  const client = await pool.connect();
  try {
    const task = await client.query("SELECT * FROM tasks WHERE id=$1", [taskId]);
    const summary = await llm.summarize(task.rows[0].text);   // ← 30 s with the connection held
    await client.query("UPDATE tasks SET summary=$1 WHERE id=$2", [summary, taskId]);
  } finally {
    client.release();
  }
}

// ✅ Release the connection before the remote call; use an outbox for atomicity.
async function summarizeAndStore(taskId: string) {
  const task = await db.tasks.find(taskId);                    // short-lived query
  const summary = await llm.summarize(task.text);              // no connection held
  await db.outbox.enqueue("task.summary", { taskId, summary }); // durable, async write
}
```

## Worked example — `Acme SaaS` noisy-neighbour incident

One enterprise tenant (a 4,000-seat company) had a scheduled bulk import that issued 200
concurrent export queries, each running for 40 s. Acme's architecture at the time:

- One Postgres pool: `max = 20`.
- One worker pool: 12 workers shared by exports and webhooks.
- One HTTP client pool for all outbound calls: `maxSockets = 20`.

**The incident.** At 09:05 UTC the import started. Its 200 concurrent queries consumed all
20 database connections for 40 seconds. Every interactive request in Acme — including the
Stripe webhook endpoint — waited on the pool. The pool's default `connectionTimeoutMillis`
was 0 (wait forever), so requests queued rather than failing.

At 09:05:40 the import released its connections. The queue of 3,200 waiting requests drained
in 22 seconds, but each had already been waiting long enough that the HTTP clients' 5-second
timeouts fired, so those requests failed anyway. Meanwhile, the worker pool was saturated by
export jobs, and Stripe's webhook deliveries started timing out — which caused Stripe to
retry, which increased the queue depth further.

**Total damage**: 38 minutes of degraded service for *all* tenants, 61% error rate at peak,
and 412 duplicate webhook deliveries (retried by Stripe because Acme was slow).

**The fix, layer by layer:**

| Layer | Change | Effect |
| ----- | ------ | ------ |
| Pool | `max = 20` → `max = 60`, `connectionTimeoutMillis = 250` | Failing fast instead of queueing |
| Pool | Dedicated pool of 10 for exports/analytics | Imports cannot consume the request path's pool |
| Query | Export queries rewritten to use the read replica | Removes them from the primary entirely |
| Tenant limit | L2 concurrency limit: 10 in-flight per tenant | One tenant ≤ 17% of the request path |
| Worker pool | Export workers (4) split from webhook workers (8) | A poison export cannot starve webhooks |
| HTTP client | One client per dependency (Stripe 10, LLM 5, S3 10) | Slow LLM calls cannot hold Stripe sockets |
| Queue | Depth limit 10,000; messages older than 1 h go to the DLQ | The queue cannot grow without bound |
| Shedding | Optional features shed before writes | Interactive traffic survives |

**After**: the same import runs with 10 concurrent queries against the replica. The request
path's pool utilization stays at 62% during the import. No duplicate webhook deliveries. The
tenant's import takes 4× longer, which the tenant was told was expected — and which was a
better outcome than a 38-minute outage for 4,000 other tenants.

## Key data / numbers

| Item | Value | Notes |
| ---- | ----- | ----- |
| Pool `connectionTimeoutMillis` | 250 ms | Never 0; waiting is a failure |
| Pool headroom for retries | max ≥ 1.5 × peak RPS × p95 latency | |
| Pool utilization ceiling at peak | 70% | Above this, retries have no headroom |
| Postgres `statement_timeout` | 5 s (queries), 30 s (migrations) | Server-side kill switch |
| Per-tenant concurrency (standard tier) | 10 in-flight | ~10% of the fair share |
| Per-tenant concurrency (enterprise tier) | 100 in-flight | Contracted |
| Per-tenant queue | 10 | Beyond this: `429` + `Retry-After: 5` |
| Per-dependency bulkhead | Stripe 10, LLM 5, S3 10 | One pool per dependency |
| Bulkhead acquire timeout | 100–250 ms | Fail fast, do not wait |
| Worker pools | exports 4, webhooks 8, notifications 4 | Separate per job class |
| Queue depth limit | 10,000 messages | Beyond this: shed or DLQ |
| Queue max age | 1 hour | Older items are usually worthless |
| Read replica usage | exports, analytics, reporting | Never the request path |
| DB connections per instance | ≤ 100 total | Watch the server's `max_connections` |
| Dedicated pool for exports | 10 | Separate from the request path |
| Fair-share guarantee | ≥ 80% of capacity reserved for standard tenants | Enforced by limits, not by hope |

## Real-world use case — `AgentRun` (Acme SaaS)

`AgentRun` is the feature most likely to exhaust shared resources, because each run makes
up to 12 provider calls, each of which can take 30 seconds.

Before isolation, `AgentRun` shared the API's outbound HTTP pool. During an LLM provider
degradation (p99 rising from 800 ms to 25 s), Acme's runs held 5 sockets each; at 20
concurrent runs, all 20 sockets were held by LLM calls, and Stripe calls in the same process
could not get a socket. Checkout failures — which need exactly one Stripe call — were
collateral damage.

After isolation:

| Resource | Before | After |
| -------- | ------ | ----- |
| LLM client pool | shared (20) | dedicated (5) |
| Stripe client pool | shared (20) | dedicated (10) |
| Postgres pool | shared (20) | shared, but AI audit writes go through an outbox |
| Per-tenant run concurrency | none | 2 for standard, 10 for enterprise |
| Circuit breaker per dependency | none | LLM opens at 50% failures over 20 requests |

Result during the same degradation: LLM calls failed fast via the breaker, **checkout
success rate was unaffected**, and the LLM feature degraded to "summary unavailable"
instead of taking down payments. The AI feature was the thing that broke — which is the
correct blast radius.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Shared pools + global limits | Simple; maximum utilization | One tenant can starve everyone | Small, trusted, single-tenant workloads |
| Per-tenant quota (L1) | Very cheap | Does not bound *long* requests | Every multi-tenant system |
| Per-tenant concurrency (L2) | Bounds in-flight work | Needs per-tenant state | **Default for multi-tenant** |
| Per-dependency bulkheads | Isolates failure domains | Some idle capacity | Every system with ≥ 2 dependencies |
| Per-tier dedicated resources (L3) | Strong isolation | Expensive; operational complexity | Contracted enterprise tiers |
| Read replica for heavy reads | Protects the primary | Replication lag | Exports, analytics, reports |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Set a bounded `connectionTimeoutMillis` on every pool | Let callers wait forever for a connection |
| Set a server-side `statement_timeout` | Rely on client-side cancellation alone |
| Give each dependency its own client pool and bulkhead | Share one HTTP client across dependencies |
| Release the DB connection before a slow remote call | Hold a connection across a 30 s LLM call |
| Limit per-tenant concurrency, not just rate | Rate-limit only; long requests still pile up |
| Use the read replica for exports and analytics | Run analytics on the primary |
| Give each job class its own worker pool | Share one worker pool across job classes |

## Common mistakes

- **Unbounded pool waiting.** `connectionTimeoutMillis = 0` means a slow dependency converts
  into an unbounded queue and a latency collapse.
- **One pool for everything.** Postgres, Stripe, and the LLM sharing 20 sockets means the
  slowest dependency sets the latency for all of them.
- **Rate limit without concurrency limit.** A tenant sending 5 rps of 60-second requests
  passes the rate limit and occupies 300 slots.
- **The "fair share" that is not enforced.** Without per-tenant limits, fairness is a
  hypothesis.
- **Analytics on the primary.** A `GROUP BY` over 40M rows holds a connection and a CPU for
  minutes.
- **Increasing the pool size instead of isolating.** Doubling the pool doubles the
  concurrent damage to the database.

## Checklist

- [ ] Every pool has a bounded `connectionTimeoutMillis` (≤ 250 ms).
- [ ] Every query path has a server-side `statement_timeout`.
- [ ] Each dependency has its own HTTP client, pool, breaker, and retry budget.
- [ ] Per-tenant concurrency limits exist for every tenant tier.
- [ ] Per-tenant queues are bounded, and overflow returns `429` + `Retry-After`.
- [ ] No connection is held across a remote call.
- [ ] Exports and analytics use the read replica.
- [ ] Each job class has its own worker pool and queue.
- [ ] Pool utilization stays ≤ 70% at peak, verified by a load test.

## Related

- [Failure Amplification and Error Storms](./01-failure-amplification-and-error-storms.md)
- [Bounding Queues, Retries, and Backpressure](./03-bounding-queues-retries-and-backpressure.md)
- [Noisy-Neighbour Tenant Isolation (worked example)](../03-practical-examples/02-noisy-neighbor-tenant-isolation.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
