# Failure Amplification and Error Storms

> Part XXII · Chapter 57 · Sections 57.1, 57.2, 57.3, 57.12, 57.15 · _Estimated reading time: 24 min_
> **Prerequisite:** [Chapter 27 — Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md), [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)

## In one sentence

An **error storm** is a feedback loop where each failure produces extra load, which produces
more failures — and the only defence is to **bound the amplification**: one retry owner, a
retry budget, and a cap on what a failure is allowed to cost.

## Why this matters in production

The defining property of a storm is that **the system is busier because it is failing**. A
dependency returns `503`; each caller retries three times; the dependency now receives 3× the
traffic; it slows further; more callers time out and retry; the retry calls hold connections;
the connection pool empties; unrelated endpoints start failing with "too many clients".

Nothing in that chain is a bug in the classic sense. Every component behaved as configured.
The failure came from **composition**: policies that are individually reasonable and jointly
lethal.

This chapter names the amplification factors and gives you the controls.

## Core concept

### 57.1 — What an error storm is

```text
                 ┌─────────────────────────────────────┐
                 │  Dependency returns 503              │
                 └──────────────┬──────────────────────┘
                                ▼
                 ┌─────────────────────────────────────┐
                 │  Caller retries (3 attempts)         │  ← AMPLIFICATION 1 (retry)
                 └──────────────┬──────────────────────┘
                                ▼
                 ┌─────────────────────────────────────┐
                 │  Caller above also retries (3)       │  ← AMPLIFICATION 2 (nested retry)
                 └──────────────┬──────────────────────┘
                                ▼
                 ┌─────────────────────────────────────┐
                 │  Dependency now sees 9× the traffic │  ← the dependency collapses
                 └──────────────┬──────────────────────┘
                                ▼
                 ┌─────────────────────────────────────┐
                 │  Timeouts accumulate → pool empty    │  ← AMPLIFICATION 3 (held resources)
                 └──────────────┬──────────────────────┘
                                ▼
                 ┌─────────────────────────────────────┐
                 │  Unrelated endpoints fail too       │  ← COLLATERAL DAMAGE
                 └─────────────────────────────────────┘
```

The storm is not the `503`. The storm is the **amplification** around it.

### 57.2 — The five amplification factors

| # | Amplifier | Multiplier | Control |
| - | --------- | ---------- | ------- |
| 1 | **Retries** | up to `attempts` | Retry budget; one owner |
| 2 | **Nested retries** (layer × layer) | `∏ attempts` per layer | Single retry owner per dependency |
| 3 | **Timeouts** (held resources) | `timeout × attempts` per worker | Deadline propagation; bounded timeouts |
| 4 | **Fan-out** (one request → N calls) | `N` | Circuit breaker; bulkhead per dependency |
| 5 | **Retries of retries** in queues and clients | `queue × client` | Client-side budget; server-side `Retry-After` |

The **total amplification factor** is the product of the factors in play:

```text
  A = attempts × nested_layers × fan_out
```

With 3 retry attempts at 2 layers and a fan-out of 3 (one request calls three services):

```text
  A = 3 × 2 × 3 = 18
```

A 10% error rate at the leaf dependency becomes a **190% load increase** at that dependency.
The formula is worked through in
[`02-deep-dive/01-error-storm-math.md`](../02-deep-dive/01-error-storm-math.md).

### 57.3 — Retry storms

A retry storm is the specific case where retries dominate the traffic.

| Symptom | Meaning |
| ------- | ------- |
| `retry_ratio` (retries / total requests) > 20% | Retries are no longer a minority of traffic |
| Dependency request count > 2× the caller's request count | Every caller is retrying |
| Retry attempts correlate with the error rate | Retries are not budgeted |
| The dependency recovers *after* the clients stop | The clients were keeping it down |

**The rule that prevents them:** a **retry budget** — retries may not exceed a stated
fraction (commonly 5–10%) of the total request volume, per dependency. When the budget is
exhausted, the next transient failure is **not** retried; it fails immediately.

```ts
// ✅ A retry budget: the tenth request may not add retries beyond 10% of traffic.
const budget = new RetryBudget({ ratio: 0.10, windowMs: 10_000 });

if (budget.allow()) {
  await sleep(backoffWithJitter(attempt));
  return attemptAgain();
}
throw err;    // budget exhausted → fail fast, do not amplify
```

Retries must also be **owned by exactly one layer**. The layer closest to the failing
dependency retries; layers above it propagate. When both the service and its HTTP client
retry, you get 3 × 3 = 9 attempts.

### 57.12 — Overload without added overload

The defining property of a *good* failure is that **the system's total load goes down when
it fails**.

| Mechanism | Effect on load | Notes |
| --------- | -------------- | ----- |
| Fail fast | Load ↓ (request ends) | Best for permanent errors |
| Circuit breaker | Load ↓ (calls stop) | Best for a dead dependency |
| Load shedding | Load ↓ (requests rejected early) | Best for total overload |
| Bulkhead | Load ↔ (other tenants unaffected) | Isolation, not reduction |
| Retry | Load ↑ | Only safe with a budget |
| Fallback chain | Load ↑ | A fallback that calls another service adds load |
| Logging every error | Load ↑ | At scale, logging is a load event |

> ⚠️ **Hazard.** **Fallback chains are a hidden amplifier.** "If Stripe is down, use the
> cached price" is fine; "if Stripe is down, call the backup processor, and if that is down,
> call the queue" is three new dependencies invoked precisely when the system is least able to
> serve them. Every fallback must be **local** (a value you already have) or **budgeted**
> (a call with its own retry policy and timeout).

### 57.15 — Resource-aware recovery

"Recovery" is not a boolean. The right recovery depends on the **resource state** of the
system at the moment of failure.

```text
  Is the system saturated?          No  → normal recovery (retry within budget)
        │
        Yes → Which resource?
                ├─ Threads/connections exhausted → shed load first, then recover
                ├─ Memory exhausted            → shed load, terminate the worker if needed
                ├─ CPU exhausted               → shed load, reduce work per request
                └─ Downstream saturated         → shed load, do NOT retry downstream
```

The practical rule:

> **When the local system is saturated, shedding is the recovery.** Retrying while your own
> pool is empty turns a local saturation into a downstream outage.

### 57.1 / 57.2 — The storm lifecycle

```text
  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
  │  Trigger  │→  │ Amplify  │→  │ Saturate │→  │ Collapse │
  │ 1 fault  │   │ retries  │   │ pools,   │   │ healthy  │
  │          │   │ timeouts │   │ queues   │   │ features │
  └──────────┘   └──────────┘   └──────────┘   │   fail    │
                                            └──────────┘
                                                 │
                                                 ▼
                                      ┌──────────────────────┐
                                      │  Recovery requires   │
                                      │  REMOVING the fault, │
                                      │  not adding capacity │
                                      └──────────────────────┘
```

The recovery phase of a storm is where teams make it worse: "let us add more retries" or
"let us add more instances" while the amplification continues. Recovery starts with
**stopping the amplification**.

## How it works (mechanics)

### A retry budget that actually bounds traffic

```ts
export class RetryBudget {
  private total = 0;
  private retried = 0;
  private windowStart = 0;

  constructor(private readonly ratio: number, private readonly windowMs: number) {}

  recordRequest(): void {
    const now = Date.now();
    if (now - this.windowStart >= this.windowMs) {
      this.windowStart = now;
      this.total = 0;
      this.retried = 0;
    }
    this.total++;
  }

  allow(): boolean {
    // Ratio check against *total* traffic, not against a fixed count.
    return this.retried < this.ratio * Math.max(this.total, 1);
  }

  recordRetry(): void {
    this.retried++;
  }

  get ratio(): number {
    return this.total === 0 ? 0 : this.retried / this.total;
  }
}
```

The ratio check uses `total` traffic, so the budget scales with load: at 1,000 rps, a 10%
budget allows 100 retries/second; at 10 rps, it allows 1.

### One retry owner per dependency

```ts
// ✅ Retry lives in the adapter, closest to the dependency.
export class StripeAdapter {
  constructor(private readonly http: HttpClient, private readonly budget: RetryBudget) {}

  async charge(input: ChargeInput): Promise<ChargeOutcome> {
    for (let attempt = 1; attempt <= 3; attempt++) {
      this.budget.recordRequest();
      try {
        const res = await this.http.post("/v1/charges", input, {
          timeoutMs: 5_000,
          idempotencyKey: input.idempotencyKey,
        });
        return { ok: true, chargeId: res.id };
      } catch (err) {
        const normalized = classify(err);
        if (!normalized.retryable || attempt === 3) throw err;
        if (!this.budget.allow()) throw err;            // budget exhausted → fail now
        this.budget.recordRetry();
        await sleep(backoffWithJitter(attempt, normalized.retryAfterSeconds));
      }
    }
    throw new Error("unreachable");
  }
}
```

Note what the *caller* of `charge` does: nothing. It does not retry a `503` from Stripe; it
propagates. One owner, one amplification factor of 3.

### Circuit breaker: removing load, not adding it

```text
        failure rate
             │
   50% ─ ─ ─┤─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  OPEN  (calls fail immediately, 0 downstream load)
             │                     ╱
             │                    ╱  30 s cooldown
   25% ─ ─ ─ ┤─ ─ ─ ─ ─ ─ ─ ─ ─╱ ─ ─ ─  HALF_OPEN (3 probes allowed)
             │        ╱
   0%  ─ ─ ─ ┤─ ─ ─╱ ─ ─ ─ ─ ─ ─ ─ ─ ─  CLOSED  (normal traffic)
             └──────────────────────────────────────────► time
```

The breaker's job is precisely to **break the storm's feedback loop**: it stops sending
traffic to a dependency that cannot serve it, so the dependency can recover instead of
dying under the amplified load.

### Detecting the storm in metrics

| Metric | Healthy | Storm | Formula |
| ------ | ------- | ----- | ------- |
| `retry_ratio` | < 0.05 | > 0.20 | retried / total |
| `dependency_amplification` | ~1.0 | > 2.0 | downstream requests / upstream requests |
| `pool_utilization` | < 0.70 | > 0.95 | in-use / max |
| `error_rate` vs `retry_ratio` correlation | low | high | — |
| `queue_age_oldest` | < 60 s | > 600 s | now − oldest item timestamp |
| `error_path_cpu_share` | < 0.05 | > 0.15 | error CPU / total CPU |

## Worked example — `WebhookIngest` (Acme SaaS)

Acme's Stripe webhook endpoint receives bursts when Stripe retries a batch of events. The
original handler had three amplification problems:

1. The HTTP client retried `5xx` responses automatically (3 attempts).
2. The handler's own `catch` block retried by returning `500`, which made Stripe retry too.
3. Stripe's retry of a *duplicate* event (because Acme answered slowly) produced a fresh
   database error, which produced another Acme retry.

The multiplication: 1 event → 3 client attempts → 3 responses of `500` → 3 Stripe deliveries
→ 9 client attempts. `A = 3 × 3 = 9`.

The fix applied the concepts above:

- **One retry owner** (57.3): the handler never retries; the adapter owns the retry, and only
  for `429`/`503` from *Acme's own* dependencies, with a budget.
- **A retry budget** (57.3): 10% of webhook requests may be retries.
- **A circuit breaker** on the internal task-lookup dependency (57.15): during a database
  incident, the breaker opens and `WebhookIngest` returns `503` in < 5 ms instead of waiting
  2 s for a timeout — so Stripe's own backoff, not Acme's, decides the retry cadence.
- **Fast acknowledgement for duplicates** (57.12): a duplicate event is acknowledged in
  ~8 ms, which removes the load that produced the duplicates.
- **Idempotency** (Chapter 28): every event write is keyed by `Stripe-Event-Id`, so the
  retries that do happen cannot duplicate work.

Measured outcome during a simulated 30-minute database degradation:

| Metric | Before | After |
| ------ | ------ | ----- |
| Downstream DB requests per webhook | 9 | 1 (breaker open) |
| `retry_ratio` | 0.62 | 0.03 |
| Webhook handler p99 latency | 4,200 ms | 12 ms (breaker) / 380 ms (closed) |
| Duplicate events processed | 1,840 | 0 |
| Stripe delivery success (24 h) | 97.1% | 99.94% |

## Key data / numbers

| Item | Value | Notes |
| ---- | ----- | ----- |
| Retry budget (recommended) | 5–10% of total requests | Per dependency, per window |
| Retry budget window | 10 s | Long enough to smooth bursts |
| Max retry attempts | 3 | 5+ rarely helps; it amplifies |
| Max amplification factor `A` | ≤ 3 | Per dependency path |
| Nested retry layers | 1 | One owner per dependency |
| Circuit breaker opens | ≥ 50% failures over ≥ 20 requests | Minimum 10 requests to open |
| Circuit breaker cooldown | 30 s | Then 3 half-open probes |
| Circuit breaker half-open | 3 probes, 2 successes to close | |
| Pool utilization ceiling | 70% at peak | Above that, retries have no headroom |
| Retry hold time | `attempts × timeout` | This is the connection-time budget |
| Queue depth limit | 10,000 messages per queue | Start shedding / DLQ beyond |
| Queue max age | 1 hour | Older work is usually worthless |
| Error-path CPU ceiling | 5% of total CPU | Above this, sample logs |
| Error log sampling threshold | 100 errors/s per service | Keep 100% of T3/T4 errors |

## Real-world use case — `Checkout` (Acme SaaS) under a provider outage

During a Stripe incident, Acme's checkout error rate rose to 35%. The team expected a
recoverable blip and got a 20-minute outage instead. The postmortem traced it to four
compounding factors:

1. **Nested retries**: the Stripe SDK retried 2× internally; Acme's adapter retried 3×; the
   API client's transport retried 2× again. `A = 2 × 3 × 2 = 12`.
2. **No retry budget**: every one of those attempts was allowed.
3. **Held connections**: `12 × 5 s timeout` meant a single checkout request could hold its
   HTTP client socket for up to 60 s — long enough to exhaust the 100-connection client pool
   at ~2 rps of arrivals.
4. **No breaker**: Acme kept calling a provider that was returning `503` for 20 minutes.

The fix, in order of effect:

| Change | Effect on `A` |
| ------ | ------------- |
| Disable the SDK's internal retries (configure `maxNetworkRetries: 0`) | 12 → 6 |
| One retry owner (the adapter only) | 6 → 3 |
| Add a retry budget of 10% | caps retries regardless of the above |
| Add a circuit breaker (opens after 50% failures over 20 requests) | dependency load → 0 during the outage |
| Reduce the client timeout from 5 s to 2 s | connection-hold time 12 s → 6 s |
| Return `503` + `Retry-After: 5` to the client | clients back off instead of retrying hard |

After the change, during the next provider incident: checkout `A` stayed at 3, the retry
ratio peaked at 0.08, Stripe connection usage stayed under 40%, and checkout failures became
visible as `503` with a clear `Retry-After` instead of 20-minute hangs.

The lesson generalizes: **the storm was not Stripe's fault; it was the multiplication of
six individually reasonable policies.**

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Aggressive retries | Masks short blips | Amplifies storms; duplicates side effects | Never on a non-idempotent path |
| Retry budget | Bounded traffic | Some requests fail unnecessarily | **Default** |
| Circuit breaker | Removes load from a dead dependency | Fails fast when the dependency is fine | Slow, frequently-failing dependencies |
| Fail fast | Lowest load | More user-visible errors | Permanent errors |
| Load shedding | Protects the core | Rejects paying customers if mis-ordered | Total overload |
| Fallback chain | Keeps some traffic served | Adds dependencies under stress | Only with local (cached) fallbacks |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give each dependency exactly one retry owner | Retry at the client, the service, and the SDK |
| Cap retries with a budget (5–10% of traffic) | Retry every transient failure |
| Propagate `Retry-After` to your own callers | Swallow it and use your own schedule |
| Open the breaker when a dependency is clearly down | Keep probing a dead dependency |
| Shed load before retrying when locally saturated | Retry while your own pool is empty |
| Use cached/local fallbacks only | Chain live fallbacks under stress |
| Measure `retry_ratio` and `dependency_amplification` | Assume your retries are bounded |

## Common mistakes

- **Nested retries at multiple layers.** The most common storm cause, and the hardest to
  see because each layer looks reasonable in isolation.
- **Retrying with the SDK's defaults left on.** Many SDKs retry by default, silently.
- **A breaker that never opens.** Configured with a 1,000-request minimum window, so it
  opens long after the damage.
- **Retrying inside a timeout-less call.** The hold time becomes unbounded.
- **Shedding uniformly.** Rejecting the same percentage of every customer's traffic
  instead of shedding optional features first.
- **Adding instances to fix a storm.** More instances mean more retries, which means more
  load on the failing dependency.

## Checklist

- [ ] Each dependency has exactly one retry owner; the SDK's own retries are disabled.
- [ ] A retry budget of 5–10% is implemented and its ratio is monitored.
- [ ] The amplification factor `A` per dependency path is ≤ 3 and documented.
- [ ] Circuit breakers have thresholds matched to the dependency's traffic (min 10 requests).
- [ ] `Retry-After` from a dependency is propagated to callers.
- [ ] Fallbacks are local (cached) or independently budgeted.
- [ ] Shedding is ordered by request value and implemented.
- [ ] `retry_ratio`, `dependency_amplification`, and `pool_utilization` are on a dashboard.

## Related

- [Isolation: Tenants, Features, and Dependencies](./02-isolation-tenants-features-dependencies.md)
- [Bounding Queues, Retries, and Backpressure](./03-bounding-queues-retries-and-backpressure.md)
- [The Error-Storm Math](../02-deep-dive/01-error-storm-math.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
