# Load Shedding and Admission Control for Acme SaaS

> Part XXII · Chapter 57 · Sections 57.12, 57.13, 57.14 (applied) · _Estimated reading time: 25 min_
> **Prerequisite:** [Chapter 57 README](../README.md), [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)

## In one sentence

A complete, working **load-shedding and admission-control layer** for Acme SaaS: a system
that protects the core by rejecting the right requests, in the right order, with a complete
client contract.

## Why this matters in production

Every service eventually hits a point where it cannot serve its full offered load. What
happens next is a design decision, and the default — "let the queue grow, let latency
climb, let everything time out" — is the worst one: it converts a capacity shortfall into a
total outage with **no useful error messages**.

A shedding layer is the difference between:

- "We are busy; try again in 5 seconds" (429/503 + `Retry-After`), and
- "Your request timed out after 30 seconds" (504), which the client cannot act on.

The second is what happens without admission control, and it costs you every retrying
client's patience.

## The design

```text
   client
     │
     ▼
 ┌──────────────────────────────────────────────────────────┐
 │  EDGE / MIDDLEWARE                                       │
 │  1. Hard gates (circuit breaker open → 503 + Retry-After) │
 │  2. Global concurrency limit (semaphore)                  │
 │  3. Tenant concurrency limit (per-tenant semaphore)       │
 │  4. Endpoint class → shedding priority                    │
 │  5. Feature flag: optional features → shed first          │
 └───────────────┬──────────────────────────────────────────┘
                 ▼
 ┌──────────────────────────────────────────────────────────┐
 │  APPLICATION                                             │
 │  6. Dependency bulkheads (per dependency)                 │
 │  7. Per-dependency retry budget                           │
 │  8. Degraded-mode fallbacks (local only)                  │
 └──────────────────────────────────────────────────────────┘
```

Each layer has one job, and each produces a **distinct error code**, so the reason for a
rejection is always visible.

## Endpoint classification

The shedding order requires knowing what each endpoint is worth. Acme classified every
endpoint into four classes:

| Class | Examples | Shedding order | Response when shed |
| ----- | -------- | -------------- | ------------------ |
| **P0 — Critical** | `POST /checkout`, `POST /webhooks/stripe`, `POST /auth/token` | Never shed | Served or `503` on hard failure |
| **P1 — Essential** | `GET /projects`, `GET /tasks`, `POST /tasks` | Shed last | `503` + `Retry-After` |
| **P2 — Valuable** | `GET /reports`, `POST /exports` | Shed before P1 | `503` + `Retry-After` |
| **P3 — Optional** | `GET /ai/summary`, `GET /avatars`, `GET /previews` | Shed first | `200` with a degraded body |

The P3 class is special: it **does not reject**. It returns a successful, degraded response,
because the feature is optional and the page still works without it.

```ts
export type EndpointClass = "P0" | "P1" | "P2" | "P3";

// Ordered by shedding priority: P3 first.
const SHED_ORDER: EndpointClass[] = ["P3", "P2", "P1", "P0"];
```

## Implementation

### Step 1 — the shedding controller

```ts
export type SheddingState = "normal" | "shedding" | "critical";

export class SheddingController {
  private state: SheddingState = "normal";
  private lastTransition = Date.now();

  constructor(
    private readonly saturation: SaturationSignal,   // pool utilization, CPU, latency
    private readonly thresholds: {
      sheddingAt: number;    // e.g. 0.75
      criticalAt: number;    // e.g. 0.90
    },
  ) {}

  get current(): SheddingState {
    this.evaluate();
    return this.state;
  }

  private evaluate(): void {
    const s = this.saturation.value();          // 0..1
    const next: SheddingState =
      s >= this.thresholds.criticalAt ? "critical"
      : s >= this.thresholds.sheddingAt ? "shedding"
      : "normal";

    if (next !== this.state) {
      this.state = next;
      this.lastTransition = Date.now();
      metrics.gauge("shedding.state", SHED_ORDER.indexOf(next) === -1 ? 0 : next === "normal" ? 0 : next === "shedding" ? 1 : 2);
    }
  }

  /** How aggressively to shed, per class: 0 = never, 1 = always. */
  shouldShed(cls: EndpointClass): boolean {
    this.evaluate();
    if (this.state === "normal") return false;
    if (cls === "P0") return false;

    const rank = SHED_ORDER.indexOf(cls);              // P3 = 0, P1 = 2
    if (this.state === "critical") return cls !== "P0";

    // In "shedding" state, shed the lowest-value classes first.
    return rank <= (this.state === "critical" ? 2 : 0);
  }
}
```

The saturation signal is a blend, because no single metric is reliable:

```ts
export class SaturationSignal {
  value(): number {
    const pool = gauge("db.pool.utilization");        // 0..1
    const cpu = gauge("process.cpu.utilization");      // 0..1
    const latencyRatio = gauge("http.p99") / gauge("http.p50");
    // Latency inflation is the earliest signal of saturation.
    return Math.max(pool, cpu, Math.min(1, (latencyRatio - 2) / 4));
  }
}
```

### Step 2 — admission control

```ts
export class AdmissionController {
  private readonly global: Semaphore;
  private readonly perTenant = new Map<string, Semaphore>();
  private readonly perDependency = new Map<string, Semaphore>();

  constructor(
    private readonly limits: {
      globalConcurrency: number;        // 200 for the whole instance
      perTenantConcurrency: number;     // 10 standard, 100 enterprise
      perDependencyConcurrency: Record<string, number>;  // postgres 20, stripe 10, llm 5
      tenantQueueDepth: number;         // 10
    },
  ) {
    this.global = new Semaphore(this.limits.globalConcurrency);
  }

  admit(tenantId: string, dependency: string): Admission {
    if (!this.global.tryAcquire()) {
      return { ok: false, code: "SERVER_OVERLOADED", retryAfterSeconds: 2 };
    }

    const tenant = this.tenantSemaphore(tenantId);
    if (!tenant.tryAcquire()) {
      this.global.release();
      return { ok: false, code: "TENANT_CONCURRENCY_LIMIT", retryAfterSeconds: 5 };
    }

    const dep = this.dependencySemaphore(dependency);
    if (!dep.tryAcquire()) {
      tenant.release();
      this.global.release();
      return { ok: false, code: "DEPENDENCY_OVERLOADED", retryAfterSeconds: 1 };
    }

    let released = false;
    return {
      ok: true,
      release: () => {
        if (released) return;
        released = true;
        dep.release();
        tenant.release();
        this.global.release();
      },
    };
  }

  private tenantSemaphore(tenantId: string): Semaphore {
    const limit = this.limits.perTenantConcurrency;
    let sem = this.perTenant.get(tenantId);
    if (!sem) {
      sem = new Semaphore(limit);
      this.perTenant.set(tenantId, sem);
    }
    return sem;
  }

  private dependencySemaphore(dependency: string): Semaphore {
    let sem = this.perDependency.get(dependency);
    if (!sem) {
      sem = new Semaphore(this.limits.perDependencyConcurrency[dependency] ?? 10);
      this.perDependency.set(dependency, sem);
    }
    return sem;
  }
}
```

> The per-tenant map is per instance. With 24 instances, the effective tenant limit is
> 24 × 10 = 240. Acme accepted that slack deliberately and documented it; for enterprise
> tenants with hard isolation requirements, the limit moved to a shared store.

### Step 3 — the middleware

```ts
export function admissionMiddleware(controller: AdmissionController, shedder: SheddingController) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const cls = classifyEndpoint(req.route);
    const tenantId = req.tenantId;

    // 1. Optional features: degrade rather than reject.
    if (cls === "P3" && shedder.shouldShed("P3")) {
      res.status(200).json(degradedBody(req.route));
      res.setHeader("Warning", '199 acme "feature-degraded"');
      return;
    }

    // 2. Hard gates.
    if (killSwitch.isOpen(primaryDependency(req.route))) {
      return sendRejected(res, "DEPENDENCY_DISABLED", 503, 5);
    }

    // 3. Admission control.
    const admission = controller.admit(tenantId, primaryDependency(req.route));
    if (!admission.ok) {
      return sendRejected(res, admission.code, admission.code === "TENANT_CONCURRENCY_LIMIT" ? 429 : 503,
                          admission.retryAfterSeconds);
    }

    try {
      await next();
    } finally {
      admission.release();
    }
  };
}

function sendRejected(res: Response, code: string, status: number, retryAfter: number): void {
  res.setHeader("Retry-After", String(retryAfter));
  res.status(status).json({
    type: `https://acme.example/problems/${code.toLowerCase().replace(/_/g, "-")}`,
    title: titleFor(code),
    status,
    detail: `The request was rejected (${code}). Retry in ${retryAfter} seconds.`,
    code,
    correlationId: res.locals.correlationId,
  });
}
```

### Step 4 — the degraded body for optional features

```ts
function degradedBody(route: string): unknown {
  switch (route) {
    case "ai.summary":
      return { summary: null, degraded: true, degradedReason: "SERVICE_SATURATED" };
    case "project.avatar":
      return { url: "/static/avatar-placeholder.svg", degraded: true };
    default:
      return { degraded: true, degradedReason: "SERVICE_SATURATED" };
  }
}
```

Note the `degraded: true` marker and the `Warning` header. A degraded response that looks
like a normal response is a silent failure.

## Worked example — the Saturday incident

Acme's API normally serves 400 rps and peaks at 2,000 rps on weekday mornings. On a
Saturday, a partner integration entered a retry loop against `POST /projects/sync` and drove
sustained 6,000 rps of requests — 3× the normal peak.

**Before the shedding layer**, the sequence was:

1. 09:14 — arrival rate rises to 6,000 rps. The DB pool (20 connections) fills; requests wait.
2. 09:14:30 — `connectionTimeoutMillis = 0` meant requests waited indefinitely. Latency
   climbed past 30 s; the load balancer's health checks started failing.
3. 09:16 — the load balancer removed all instances because the health check timed out.
   Full outage.
4. The partner's retry loop continued against a dead service.

**After the shedding layer:**

1. 09:14 — arrival rate rises to 6,000 rps. Saturation signal (pool utilization) crosses
   0.75 → state `shedding`.
2. P3 endpoints (AI summaries, avatars) return degraded `200` responses immediately.
   Latency for those endpoints: 4 ms.
3. The global concurrency limit (200) is reached; excess requests are rejected with
   `503` + `Retry-After: 2`. P1 endpoints are served up to the limit.
4. The partner's requests are rejected fast; its retry loop backs off (it honors
   `Retry-After`).
5. 09:19 — the partner fixes its loop. Arrival rate returns to 400 rps. Saturation drops
   below 0.75 → state returns to `normal`.
6. Health checks never failed. **Zero minutes of full outage.**

Measured comparison:

| Metric | Before | After |
| ------ | ------ | ----- |
| Full-outage duration | 22 min | 0 |
| Requests served successfully | 41% | 88% |
| P99 latency (healthy tenants) | 31,000 ms | 420 ms |
| Health-check failures | 14 (all instances removed) | 0 |
| Partner retry volume during the incident | 6,000 rps sustained | 200 rps (capped by `Retry-After`) |
| Error-path CPU share | 22% | 3% |

The 12% of requests that were rejected were all from the misbehaving partner, and each
rejection told the partner exactly when to come back.

## Key data / numbers

| Item | Value | Notes |
| ---- | ----- | ----- |
| Global concurrency limit (per instance) | 200 | Sized to the dependency pools × 10 |
| Per-tenant concurrency | 10 standard, 100 enterprise | Per instance; document the N× slack |
| Per-dependency concurrency | Postgres 20, Stripe 10, LLM 5 | One bulkhead per dependency |
| Tenant queue depth | 10 | Beyond this: `429` + `Retry-After: 5` |
| Shedding threshold (`shedding` state) | 0.75 saturation | Pool utilization or CPU or latency ratio |
| Shedding threshold (`critical` state) | 0.90 saturation | |
| Latency ratio signal | p99 / p50 > 3 | The earliest saturation signal |
| Shedding order | P3 → P2 → P1; P0 never | |
| Rejection status (server) | `503` + `Retry-After` | |
| Rejection status (tenant) | `429` + `Retry-After` | |
| `Retry-After` values | 1 s (dependency), 2 s (global), 5 s (tenant) | |
| Degraded response | `200` + `degraded: true` + `Warning` header | Never a silent fallback |
| Circuit breaker open | ≥ 50% failures over ≥ 20 requests | 30 s cooldown, 3 probes |
| Error-path CPU budget | ≤ 5% of total | |
| Log sampling threshold | 100 errors/s | |
| Recovery check after an incident | state returns to `normal` within 60 s of the load dropping | |

## Real-world use case — `Checkout` (Acme SaaS) during the partner incident

The shedding layer had to protect one thing above all: **payments**. `POST /checkout` is
P0 and is never shed. But P0 does not mean "always succeeds" — it means "always gets a
definitive, actionable answer".

Under the 6,000 rps flood, a checkout attempt that could not get a DB connection within
250 ms received:

```http
HTTP/1.1 503 Service Unavailable
Retry-After: 2
Content-Type: application/problem+json

{
  "type": "https://acme.example/problems/server-overloaded",
  "title": "Service temporarily overloaded",
  "status": 503,
  "detail": "We could not accept your payment right now. Your card was not charged. Retry in 2 seconds.",
  "code": "SERVER_OVERLOADED",
  "correlationId": "req-7c11a9"
}
```

Two details were deliberate and are worth copying:

1. **"Your card was not charged."** The rejection happens at admission control, *before* the
   Stripe call, so no side effect occurred. Stating it removes the customer's fear and
   removes support load.
2. **The correlation ID.** The customer can quote it; support can find the exact rejection
   in the log.

The alternative — letting the checkout wait for a connection and then timing out at 30 s —
produced abandoned carts, Stripe sessions left open, and "did my card get charged?"
support tickets. The rejection is strictly better for the customer even though it is
"less service".

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify every endpoint by value before shedding | Shed uniformly |
| Never shed P0 (payments, auth, webhooks) | Shed the payment endpoint to protect the rest |
| Reject before any side effect occurs | Reject after the card was charged |
| Return `Retry-After` on every rejection | Return `500` and let clients guess |
| Use `429` for tenant limits and `503` for server saturation | Use the same code for both |
| Degrade P3 features instead of rejecting them | Reject an optional feature |
| Mark degraded responses with `degraded: true` | Serve a plausible empty body silently |
| Derive the saturation signal from several metrics | Trigger shedding on a single noisy metric |

## Common mistakes

- **Shedding by endpoint uniformly.** Every customer loses 10% of their requests instead of
  the optional features being dropped first.
- **Shedding after a side effect.** A rejected request that already charged a card is a
  duplicate-charge incident.
- **Rejecting with `500`.** Clients treat `500` as unretryable and give up.
- **No `Retry-After`.** The client retries immediately, and you are back to the storm.
- **A single-metric trigger.** CPU alone misses I/O saturation; pool utilization alone
  misses a downstream slowdown. Use a blend, with latency ratio as the early signal.
- **Shedding P0 endpoints.** If the payment path is shed, revenue stops — and the traffic
  you shed was very likely to be legitimate.
- **No recovery path.** A controller that never returns to `normal` is an outage with extra
  steps.

## Checklist

- [ ] Every endpoint has a shedding class (P0–P3).
- [ ] The shedding order is documented and encoded.
- [ ] P0 is never shed.
- [ ] Rejections happen before any side effect.
- [ ] Every rejection carries a status, a stable code, a `Retry-After`, and a correlation ID.
- [ ] `429` is used for tenant limits; `503` for server saturation.
- [ ] Degraded responses carry `degraded: true` and a `Warning` header.
- [ ] The saturation signal blends pool utilization, CPU, and the p99/p50 ratio.
- [ ] The controller returns to `normal` automatically when the load drops.
- [ ] `shedding.state` and the per-class rejection counts are on a dashboard.

## Related

- [Noisy-Neighbour Tenant Isolation](./02-noisy-neighbor-tenant-isolation.md)
- [Bounding Queues, Retries, and Backpressure](../01-concepts/03-bounding-queues-retries-and-backpressure.md)
- [Retry Budget and Queue Bounding](../02-deep-dive/02-retry-budget-and-queue-bounding.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
