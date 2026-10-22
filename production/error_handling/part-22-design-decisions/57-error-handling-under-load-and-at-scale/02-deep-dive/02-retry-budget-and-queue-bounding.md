# Retry Budget and Queue Bounding: The Calculations

> Part XXII · Chapter 57 · Sections 57.3, 57.5, 57.13, 57.14 · _Estimated reading time: 22 min_
> **Prerequisite:** [Bounding Queues, Retries, and Backpressure](../01-concepts/03-bounding-queues-retries-and-backpressure.md)

## In one sentence

A **retry budget** caps retries as a fraction of traffic and a **queue bound** caps waiting
work; together they determine whether a degradation recovers in minutes or becomes an
outage.

## Why this matters in production

Retries without a budget and queues without a bound are the two mechanisms that turn a
dependency's bad day into your bad week. Both are easy to fix *after* the fact and nearly
impossible to fix *during* the incident, because the fix requires a deploy.

The arithmetic matters because the two controls are usually chosen by intuition
("let's retry 3 times", "let's allow 100,000 messages"), and intuition does not know your
traffic shape. The formulas below size them from three numbers you already have: arrival
rate, service rate, and error rate.

## Core concept

### The retry budget formula

A budget expressed as a ratio of retries to total requests:

```text
  budget_ratio = max_retries_allowed / total_requests
```

The subtlety: the denominator is **total traffic**, not error traffic. If 10% of requests
fail and the budget is 10%, then *every* failed request may be retried once and no more —
so the budget is exhausted exactly when the error rate reaches the budget ratio. Above that,
retries are refused.

Setting the ratio from your alert threshold `t` and your amplification factor `A`:

```text
  budget_ratio ≤ t × (A − 1) / (1 + t × (A − 1))
```

With `t = 0.05`, `A = 3`: `0.05 × 2 / 1.1 = 0.0909` → **9%**, so a 10% budget is right.
With `t = 0.05`, `A = 12`: `0.05 × 11 / 1.55 = 0.355` → 35% — which is not a sensible
budget, and the correct conclusion is **reduce `A`**, not raise the budget.

### Queue depth and drain time

```text
  λ = arrival rate (messages/second)
  μ = service rate = workers / average_job_duration_seconds
  ρ = λ / μ                              (must be < 1)

  drain_time = depth / (μ − λ)
  time_to_capacity = (max_depth − depth) / (μ − λ)
  time_to_overflow   = (max_depth − depth) / (λ − μ)     (when λ > μ)
```

Three derived quantities you should be able to state for every queue:

| Quantity | Meaning | Target |
| -------- | ------- | ------ |
| **Headroom time** | How long before the queue reaches its limit | ≥ 15 min |
| **Drain time** | How long to clear the current backlog | < 15 min |
| **Overflow time** | How long until the queue overflows (if `λ > μ`) | Alert well before it |

### Backpressure arithmetic

A bounded queue with a bounded producer queue needs a **rejection rate** that is
proportionate. When a queue is at capacity:

```text
  rejection_rate = arrivals_beyond_capacity / (μ − λ)
```

If arrivals exceed capacity by 20% and the service rate is 8/s, you must reject
`0.2 × 8 = 1.6/s` of arrivals — about 12% of traffic at a 13/s arrival rate. That
rejection rate is a **deliberate, communicated** outcome, not an accident.

### Holding resources: the timeout budget

Every retry attempt holds a connection for up to the timeout:

```text
  connection_hold_time = attempts × timeout_ms
  pool_requirement = peak_rps × connection_hold_time_seconds / (1 − target_utilization)
```

With 200 peak rps, 3 attempts, a 2 s timeout, and a target utilization of 0.7:

```text
  hold = 3 × 2 = 6 s
  pool = 200 × 6 / 0.7 = 1,714 connections   ← absurd; the design is wrong
```

The absurdity is the point. The formula says: **you cannot retry 3× with a 2 s timeout at
200 rps on a 20-connection pool.** Fixing it means one of:

- Reduce the retry count to 1 → hold = 2 s → pool = 571. Still too many.
- Shorten the timeout to 250 ms → hold = 750 ms → pool = 214. Still too many.
- **Cap concurrency at the pool size** (admission control) → the pool is the limit, and
  excess requests are rejected rather than queued.

The conclusion that a pool of 20 with a 2 s timeout can serve 200 rps only if requests
complete in ~70 ms (20 / 200 = 100 ms per slot). So a 2 s timeout on a 200 rps workload
means the pool can absorb a 2-second slowdown — anything longer is exhaustion. **Your
timeout should be a small multiple of the healthy p99, not of the worst case you fear.**

## How it works (mechanics)

### A budget that counts against total traffic

```ts
export class RetryBudget {
  private windowStart = Date.now();
  private total = 0;
  private retried = 0;

  constructor(
    private readonly ratio: number,       // e.g. 0.10
    private readonly windowMs: number,    // e.g. 10_000
  ) {}

  private roll(now: number): void {
    if (now - this.windowStart >= this.windowMs) {
      this.windowStart = now;
      this.total = 0;
      this.retried = 0;
    }
  }

  recordAttempt(): void {
    this.roll(Date.now());
    this.total++;
  }

  tryReserveRetry(): boolean {
    this.roll(Date.now());
    if (this.retried >= this.ratio * Math.max(this.total, 1)) return false;
    this.retried++;
    return true;
  }

  get used(): number {
    return this.total === 0 ? 0 : this.retried / this.total;
  }
}
```

The subtlety in `tryReserveRetry`: the check uses `this.total`, which counts **attempts**,
not original requests. When 10% of requests fail and each gets one retry, `total` grows by
the retries as well — so the ratio is retries / (requests + retries). That is the standard
definition and it is self-correcting: as the ratio approaches the limit, fewer retries are
allowed.

### Sizing a queue from the traffic shape

```ts
export function sizeQueue(opts: {
  arrivalRatePerSec: number;     // λ, measured at peak
  avgJobDurationSec: number;     // measured
  workers: number;               // current worker count
  headroomMinutes: number;       // target time before overflow
}): { workers: number; maxDepth: number; drainSecondsAtLimit: number } {
  const mu = opts.workers / opts.avgJobDurationSec;
  if (mu <= opts.arrivalRatePerSec) {
    throw new Error(`queue is unstable: λ=${opts.arrivalRatePerSec} ≥ μ=${mu}`);
  }
  const serviceRate = mu - opts.arrivalRatePerSec;       // messages/second of drain capacity
  const headroomSeconds = opts.headroomMinutes * 60;
  const maxDepth = Math.ceil(serviceRate * headroomSeconds);
  const drainSecondsAtLimit = maxDepth / serviceRate;    // = headroomSeconds by construction
  return { workers: opts.workers, maxDepth, drainSecondsAtLimit };
}
```

The `maxDepth` formula is worth pausing on: **the depth limit is the product of your drain
capacity and the time you are willing to be full.** It is not an arbitrary number.

Worked example — Acme's export queue:

```text
  λ = 3 exports/second (peak)
  avg job duration = 60 s
  workers = 4   →  μ = 4/60 = 0.0667/s
```

`μ = 0.0667/s` is **far below** `λ = 3/s`. The queue as configured was unstable by a factor
of 45 — the backlog would grow at 2.93 messages/second. Acme's actual peak export rate was
0.08/second (not 3), which gives `μ = 0.0667` vs `λ = 0.08` — still unstable. They added
workers (4 → 10) giving `μ = 0.167/s`, which is 2× `λ`. With a 30-minute headroom target:

```text
  service_rate = 0.167 − 0.08 = 0.087/s
  max_depth = 0.087 × 1800 = 156 messages
```

156 messages, not 10,000. The depth limit is small because the service rate is small — which
is exactly the point. A queue that can only drain 0.087 messages/second must not be allowed
to hold thousands.

### Admission control at the pool boundary

```ts
// ✅ Cap concurrency at the resource, reject the excess.
export async function withDb<T>(fn: (client: PoolClient) => Promise<T>): Promise<T> {
  const slot = dbLimiter.tryAcquire();
  if (!slot.ok) {
    // 503 + Retry-After: the server is saturated, not the client's fault.
    throw new ServerOverloadedError({ retryAfterSeconds: 2, reason: "db_pool_saturated" });
  }
  try {
    return await fn(await pool.connect());
  } finally {
    slot.release();
  }
}
```

The limiter's limit is set to the pool size (20), and the pool's own
`connectionTimeoutMillis` is 250 ms — so the second line of defence never waits long.

### Backpressure on the producer with a `Retry-After`

```ts
export function rejectOverloaded(res: Response): void {
  res.setHeader("Retry-After", "5");
  res.status(503).json({
    type: "https://acme.example/problems/server-overloaded",
    title: "Service temporarily overloaded",
    status: 503,
    detail: "The request was rejected to protect service stability. Retry in 5 seconds.",
    code: "SERVER_OVERLOADED",
    correlationId: res.locals.correlationId,
  });
}
```

`503` (not `429`) is correct when the *server* is saturated: the client did nothing wrong.
`429` is for a client-specific limit (a tenant's quota). Choosing the wrong one makes
clients back off for the wrong reason.

## Worked example — `Acme SaaS` sizing three queues

| Queue | λ (peak/s) | Avg duration | Workers | μ | Service rate | Headroom | Max depth | Drain at limit |
| ----- | ---------- | ------------ | ------- | - | ------------ | -------- | --------- | -------------- |
| `exports` | 0.08 | 60 s | 10 | 0.167/s | 0.087/s | 30 min | 156 | 30 min |
| `webhooks` | 25 | 0.4 s | 8 | 20/s | −5/s → **unstable** | — | — | — |

The webhook row is unstable: 8 workers at 0.4 s each serve 20/s, but arrivals are 25/s.
Acme's options were (a) more workers, (b) shorter job duration, (c) accept the backlog and
bound the depth.

They chose (c) with a twist: the webhook queue's depth limit is 50,000 (a much larger
number because the service rate is 20/s, so 50,000 messages = 2,500 s of work), and
consumers have a **per-event idempotency key** so replays are safe. The depth limit exists
to prevent unbounded memory growth, not to prevent backlog — because for webhooks, the
backlog *is* the correct behavior (the producer cannot be slowed down).

The export row shows the opposite conclusion: with a slow service rate, a small depth limit
is correct, and exceeding it should **reject** the customer with `429` + `Retry-After`,
because the export is a user-initiated, recomputable operation.

> The lesson: **the depth limit is a function of the service rate and of whether the
> producer can be slowed down.** Exports can be rejected; webhooks cannot.

## Key data / numbers

| Item | Value | Formula / note |
| ---- | ----- | -------------- |
| Retry budget ratio | 5–10% | `t(A−1) / (1 + t(A−1))` |
| Retry budget window | 10 s | |
| Max attempts | 3 | |
| Queue headroom target | 15–30 min | Time to capacity from empty |
| Drain time target | < 15 min | Time to clear the backlog |
| `μ` (service rate) | workers / avg duration | Must exceed `λ` by ≥ 50% |
| Max depth (slow queue) | `service_rate × headroom_seconds` | e.g. 156 for exports |
| Max depth (fast queue) | 50,000 | Webhooks: producer cannot be slowed |
| Pool sizing | `peak_rps × hold_time / (1 − utilization)` | Often absurd — that is the finding |
| Pool utilization target | 70% | |
| `connectionTimeoutMillis` | 250 ms | |
| Admission-control limit | = pool size | Reject beyond it |
| Rejection status (server saturated) | `503` + `Retry-After` | |
| Rejection status (tenant limit) | `429` + `Retry-After` | |
| `Retry-After` value | 1–30 s | Integer seconds |
| Overflow alert | 80% of max depth | Before it matters |

## Real-world use case — `WebhookIngest` (Acme SaaS) budget sizing

Acme's webhook endpoint receives bursts from Stripe (up to 300 events/second during a
retry wave). The original code had no budget, so during a 6-minute incident the handler
issued:

```text
  300 events/s × 3 attempts = 900 requests/s against a dependency serving 200/s
```

The dependency collapsed. With the fix:

```text
  t = 0.05 (alert threshold)
  A = 3 (one owner, 3 attempts)
  budget = 0.05 × 2 / 1.1 = 0.09 → 10%
  retry allowance = 300 × 0.09 ≈ 27 retries/second
```

Under the 300/s burst, only 27 requests/second may be retried; the rest fail immediately
with `503` + `Retry-After: 5`. Stripe then backs off on its own schedule.

The measured result during the next incident: the dependency saw **327 requests/second**
instead of 900, recovered in 4 minutes instead of 22, and Stripe's delivery success was
99.9% (against 96.2% before) — because the 503s with `Retry-After` told Stripe exactly when
to come back.

The second half of the fix was a **kill switch**: when the local breaker opened, the
handler returned `503` in under 2 ms with no downstream call at all, so the dependency
received only the 300 original requests.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Size the budget from the alert threshold and `A` | Pick 10% because it is a round number |
| Use total traffic as the budget denominator | Budget against error traffic only |
| Compute `max_depth` from the drain rate | Set max depth to "a big number" |
| Reject with `503` when the server is saturated | Return `500` on rejection |
| Set `Retry-After` on every rejection | Leave the client to guess |
| Cap concurrency at the pool size | Let requests queue on the pool |
| Check the queue at 80% depth and alert | Alert only when it overflows |

## Common mistakes

- **A budget that counts retries but not requests.** The ratio then drifts upward as the
  error rate rises — exactly when you need it to fall.
- **Sizing `max_depth` for a slow queue at 10,000.** A queue that drains 0.087 messages per
  second holding 10,000 messages means 32 hours of stale work.
- **Rejecting with `500`.** Clients treat `500` as "your fault, do not retry" and give up.
- **A pool timeout of 0.** Waiting forever turns a slow dependency into an unbounded queue.
- **Budgeting per instance.** The fleet budget grows with the fleet (Chapter 57, 57.17).
- **Alerting only on overflow.** By then, work has already been lost or delayed.

## Checklist

- [ ] A retry budget exists per dependency, with a 10 s window.
- [ ] The budget ratio is derived from the alert threshold and `A`.
- [ ] The budget counts against **total** traffic.
- [ ] Every queue has a documented `λ`, `μ`, and headroom target.
- [ ] `max_depth = service_rate × headroom_seconds` is computed, not guessed.
- [ ] Queues whose producer cannot be slowed down use a DLQ, not a rejection.
- [ ] Rejections use `429`/`503` with `Retry-After` and a stable code.
- [ ] The pool has a bounded `connectionTimeoutMillis` and an admission-control limit.
- [ ] Queue-depth alerts fire at 80% of the limit.

## Related

- [Error-Storm Math](./01-error-storm-math.md)
- [Bounding Queues, Retries, and Backpressure](../01-concepts/03-bounding-queues-retries-and-backpressure.md)
- [Load Shedding and Admission Control (worked example)](../03-practical-examples/01-load-shedding-and-admission-control-acme.md)
- [Chapter 27 — Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
