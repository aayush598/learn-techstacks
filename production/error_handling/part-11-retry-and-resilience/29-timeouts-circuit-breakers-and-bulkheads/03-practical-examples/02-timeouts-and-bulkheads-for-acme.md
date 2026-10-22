# Timeouts and Bulkheads for Acme

> Part XI · Chapter 29 · Sections 29.1–29.16 · _Estimated reading time: 25 min_
> **Prerequisite:** [Circuit Breaker Implementation](./01-circuit-breaker-implementation.md)

## In one sentence

This is Acme's **end-to-end resilience policy**: a deadline, per-attempt timeout, breaker, bulkhead,
and admission rule for each dependency, wired so checkout, exports, webhooks, and agent runs each fail
within a known budget.

## Why this matters in production

Individual mechanisms are easy to add and easy to misconfigure. The failure mode is almost always at
the seams: a 30s gateway timeout over a 3s provider timeout, a shared pool between checkout and
exports, a breaker that opens but is bypassed by the retry loop. This walkthrough shows the whole
configuration as one system and what happens during a real incident.

## Acme's dependency inventory

| Dependency | Caller | Criticality | Typical p99 | Provider limit |
| ---------- | ------ | ----------- | ----------- | -------------- |
| Stripe | Checkout | Critical | 900ms | 100 req/s |
| S3-compatible storage | `ExportJob` | Important | 2.5s | 50 req/s |
| Email API | Notifications | Optional | 600ms | 20 req/s |
| LLM provider | `AgentRun` | Optional | 6s | 30 req/s |
| Internal auth | All | Critical | 80ms | — |

## Layer budgets

```text
Client           65s absolute ceiling (interactive 10s)
  API gateway    10s deadline, 1 attempt
    Checkout     8s operation deadline
      Stripe     1s connect, 3s request, 3 attempts, 8s total
    Export       60s job deadline (async)
      Storage    2s connect, 10s request, 3 attempts per part
    Agent        20s deadline
      LLM        2s connect, 8s request, 2 attempts, 20s total
```

Rule: **each downstream budget is smaller than its caller's remaining time**, and the sum of retries
plus backoff cannot exceed the deadline.

## Configuration

```yaml
resilience:
  gateway:
    default_deadline_ms: 10000
    max_inflight: 2000
    reject_below_remaining_ms: 50

  dependencies:
    stripe:
      timeout: { connect_ms: 1000, request_ms: 3000 }
      deadline_ms: 8000
      retry: { owner: checkout, max_attempts: 3, base_ms: 250, jitter: full }
      breaker: { threshold: 0.5, min_requests: 30, window_ms: 30000, cooldown_ms: 15000 }
      bulkhead: { max_concurrent: 20, max_queue: 40 }
      fallback: { mode: fail_closed, status: 503, retry_after_s: 5 }

    storage:
      timeout: { connect_ms: 2000, request_ms: 10000 }
      deadline_ms: 60000
      retry: { owner: export_worker, max_attempts: 3, base_ms: 500, jitter: full }
      breaker: { threshold: 0.6, min_requests: 20, window_ms: 60000, cooldown_ms: 30000 }
      bulkhead: { max_concurrent: 30, max_queue: 60, per_tenant: 5 }
      fallback: { mode: fail_open, action: mark_export_retry_later }

    email:
      timeout: { connect_ms: 1000, request_ms: 3000 }
      deadline_ms: 5000
      retry: { owner: notification_worker, max_attempts: 2, base_ms: 1000 }
      breaker: { threshold: 0.5, min_requests: 10, window_ms: 30000, cooldown_ms: 60000 }
      bulkhead: { max_concurrent: 10, max_queue: 20 }
      fallback: { mode: fail_open, action: queue_for_later }

    llm:
      timeout: { connect_ms: 2000, request_ms: 8000 }
      deadline_ms: 20000
      retry: { owner: agent_run, max_attempts: 2, base_ms: 1000, jitter: full }
      breaker: { threshold: 0.4, min_requests: 20, window_ms: 20000, cooldown_ms: 20000 }
      bulkhead: { max_concurrent: 8, max_queue: 16, per_tenant: 2 }
      fallback: { mode: fail_open, action: cached_or_template }

    auth:
      timeout: { connect_ms: 200, request_ms: 500 }
      deadline_ms: 2000
      retry: { owner: gateway, max_attempts: 2, base_ms: 50 }
      breaker: { threshold: 0.3, min_requests: 20, window_ms: 10000, cooldown_ms: 5000 }
      bulkhead: { max_concurrent: 100, max_queue: 200 }
      fallback: { mode: fail_closed, status: 503 }
```

## Wiring the checkout path

```ts
const stripeBreaker = new CircuitBreaker("stripe", metrics, {
  failureThreshold: 0.5, minRequests: 30, windowMs: 30_000, baseCooldownMs: 15_000,
});
const stripeSlots = new Semaphore(20);

async function chargeOrder(order: Order, req: Request) {
  const deadline = Date.now() + remainingFrom(req); // gateway propagated ≤10s

  return retry(
    async (attempt) => {
      if (Date.now() >= deadline) throw new DeadlineExceeded();
      if (stripeBreaker.isOpen()) throw new CircuitOpenError(stripeBreaker.retryAfterMs());

      const release = await stripeSlots.acquire();
      try {
        return await stripeBreaker.exec(() =>
          withTimeout(
            (signal) => stripe.charges.create(
              { amount: order.total, idempotencyKey: `order:${order.id}:charge` },
              { signal },
            ),
            Math.min(3_000, deadline - Date.now()),
          ),
        );
      } finally {
        release();
      }
    },
    {
      maxAttempts: 3,
      deadline,
      baseDelayMs: 250,
      jitter: "full",
      retryOn: (e) => isRetryable(e) || e.code === "CIRCUIT_OPEN",
    },
  );
}
```

Key properties:

- The gateway deadline is the **outer bound**; each attempt is clamped to the remaining time.
- The bulkhead slot is held only during the call, **not during backoff**.
- The breaker is checked **before each attempt**, so an opening breaker stops retries.
- The idempotency key is stable across attempts (Chapter 28).

## Wiring exports

Exports are asynchronous, so the deadline lives on the job:

```ts
async function runExport(job: ExportJob) {
  if (Date.now() > job.deadlineMs) {
    return markExpired(job.id);           // do not start stale work
  }

  const tenantSlots = slotsFor(job.tenantId); // max 5 concurrent per tenant

  for (const part of job.parts) {
    const release = await tenantSlots.acquire();
    const storageRelease = await storageSlots.acquire();
    try {
      await retry(
        () => storageBreaker.exec(() =>
          withTimeout(
            (signal) => storage.putPart(part, { signal }),
            Math.min(10_000, job.deadlineMs - Date.now()),
          ),
        ),
        {
          maxAttempts: 3,
          deadline: job.deadlineMs,
          baseDelayMs: 500,
          jitter: "full",
          retryOn: isRetryable,
        },
      );
    } finally {
      storageRelease();
      release();
    }
  }
  job.status = "completed";
}
```

On failure after exhaustion, the job is marked `retry_later` rather than failed permanently; the
scheduler re-enqueues it with a fresh deadline. Per-tenant limits prevent one large export from
starving checkout's storage reads.

## Failure scenarios

### Provider outage (Stripe)

| Time | Event |
| ---- | ----- |
| 0s | Failures begin; requests fail in 3s |
| 5s | 30+ requests, failure rate > 50% → breaker opens |
| 5s+ | New checkouts fail fast with `503 + Retry-After: 5` |
| 20s | Cooldown ends; one probe admitted |
| 20.9s | Probe succeeds; two more probes succeed → closed |
| 21s | Normal traffic resumes |

During the open window, **no Stripe calls** are made, protecting the provider and freeing pool
capacity for healthy paths.

### Queue saturation

At 3× traffic, gateway admission admits 2,000 in-flight and rejects beyond with `503`. Checkout gets
priority; exports are shed above 70% utilization. p99 stays under 3s instead of growing unbounded.

### Slow storage

Storage p99 rises to 15s. The 10s per-attempt timeout fires; retries get 3 attempts within the 60s job
deadline; the breaker opens after 60s of >60% failures. Exports move to `retry_later`; the UI says
"Export delayed" instead of spinning forever.

## Health and alerting

```text
alert: breaker_open{dependency="stripe"} for 2m
alert: queue_depth{dependency="storage"} > 50 for 5m
alert: p99_latency{dependency="llm"} > 10s for 10m
alert: rejected_total{reason="admission"} > 5% for 5m
alert: bulkhead_wait_p99 > 1s for 10m
```

## Key data / numbers

- Gateway deadline **10s**; job deadline **60s**.
- Stripe: 20 concurrent, 3 attempts, 3s per attempt, breaker 50%/30/30s.
- Storage: 30 concurrent, 5 per tenant, 3 attempts, 10s per attempt.
- LLM: 8 concurrent, 2 per tenant, 2 attempts, 8s per attempt, breaker 40%/20/20s.
- Auth: fail-closed, 2 attempts, 500ms per attempt.
- Admission rejects below **50ms** remaining.

## Real-world use case — Acme SaaS

The policies above were introduced after a Black Friday incident where a storage slowdown caused
checkout timeouts. Before: one shared 100-connection pool, no per-tenant limits, retries at gateway
and service, and a 30s gateway timeout. After: separated pools, admission control, one retry owner per
path, and propagated deadlines. The next spike produced **0 checkout failures**, exports delayed by
minutes instead of failing, and no provider rate-limit incident.

## Trade-offs

| Decision | Benefit | Cost |
| -------- | ------- | ---- |
| Fail-closed auth/payments | Correctness | Availability during outage |
| Fail-open email/LLM | Availability | Missing notifications, template responses |
| Per-tenant export cap | Fairness | Large tenants slower |
| 60s export deadline | Bounds work | Very large exports must chunk |
| Short breaker windows | Fast reaction | More false opens |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give every dependency its own policy | Copy one policy everywhere |
| Keep downstream timeouts below the caller's | Let hops exceed the budget |
| Check the breaker before each attempt | Retry past an open breaker |
| Release bulkhead slots during backoff | Hold capacity while sleeping |
| Make fallbacks explicit per dependency | Return empty data silently |
| Alert on open breakers and queue depth | Only alert on error rate |

## Common mistakes

- **Same deadline for interactive and async paths**, forcing exports to fail early or requests to wait.
- **Per-tenant limits without eviction**, leaking memory under many tenants.
- **Fallback returning `200` with empty data**, hiding the outage (see Chapter 30).
- **Gateway retries**, duplicating service retries.
- **Breaker counting `4xx`**, opening on bad requests.

## Checklist

- [ ] Each dependency has its own timeout, retry, breaker, bulkhead, and fallback.
- [ ] Budgets nest: downstream < upstream remaining.
- [ ] One retry owner per path.
- [ ] Interactive and async deadlines are separate.
- [ ] Per-tenant limits exist for heavy workloads.
- [ ] Fallback modes are explicit (fail-open vs fail-closed).
- [ ] Open breakers and queue depth are alerted.
- [ ] Every retried operation is idempotent or keyed.

## Related

- [Admission Control and Combining Mechanisms](../01-concepts/04-admission-control-and-combining-mechanisms.md)
- [Circuit Breaker Implementation](./01-circuit-breaker-implementation.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../30-graceful-degradation-and-fallbacks/README.md)
- [Chapter 28 — Idempotency and Duplicate-Operation Safety](../../28-idempotency-and-duplicate-operation-safety/README.md)
