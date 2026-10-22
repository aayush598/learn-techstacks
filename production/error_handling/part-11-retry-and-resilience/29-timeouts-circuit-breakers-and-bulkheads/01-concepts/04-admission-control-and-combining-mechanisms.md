# Admission Control and Combining Mechanisms

> Part XI · Chapter 29 · Sections 29.13–29.16 · _Estimated reading time: 19 min_
> **Prerequisite:** [Bulkheads and Concurrency Limits](./03-bulkheads-and-concurrency-limits.md)

## In one sentence

**Admission control** decides whether to accept work *before* the system is full, and the resilience
mechanisms only work when composed in a fixed order — deadline, breaker, bulkhead, retry, fallback —
so each one sees the state the previous one left.

## Why this matters in production

A system at 100% utilization has no capacity to serve the next request, run recovery, or even emit
metrics reliably. Admission control keeps utilization below the cliff by rejecting or shedding load
early. Composition matters because the same four mechanisms in the wrong order can amplify the very
failure they were meant to contain — for example, retrying *before* checking the breaker, or applying
a fallback *before* the retry budget is exhausted.

## 29.13 — Admission control

Admission control is the gate at the edge of a service or dependency. It asks: *should this request
be allowed to consume resources right now?*

### Strategies

| Strategy | Decision | Use |
| -------- | -------- | --- |
| **Concurrency limit** | Reject if in-flight ≥ limit | Protect pools |
| **Queue bound** | Reject if queue ≥ max | Bound latency |
| **Rate limit** | Reject if rate > allowance | Fairness, quotas |
| **Load shedding** | Drop low-priority work | Survive overload |
| **Deadline check** | Reject if remaining time < minimum | Avoid doomed work |
| **Priority admission** | Admit critical, defer batch | Protect checkout |

### The early deadline check

A cheap and effective form of admission control: if the request cannot possibly finish in the time
remaining, reject it now.

```ts
function admit(req: Request, minUsefulMs = 50): boolean {
  const remaining = req.deadline - Date.now();
  if (remaining < minUsefulMs) return false;      // too late to be useful
  if (pool.inFlight >= pool.limit) return false;  // no capacity
  if (pool.queue >= pool.maxQueue) return false;  // queue saturated
  return true;
}
```

### Load shedding by priority

```text
Priority 1 (checkout, auth)   → always admit if capacity exists
Priority 2 (dashboard reads)  → shed when utilization > 85%
Priority 3 (exports, backfill)→ shed when utilization > 70%
```

Shedding priority 3 first keeps the critical path alive through a spike.

## 29.14 — Combining mechanisms

### The fixed order

```text
request
  │
  ├─ 1. DEADLINE check ──── no time left? ──▶ fail fast
  │
  ├─ 2. CIRCUIT BREAKER ─── open? ──────────▶ fail fast / fallback
  │
  ├─ 3. BULKHEAD ────────── no slot? ───────▶ queue or reject
  │
  ├─ 4. CALL (with per-attempt timeout)
  │       │
  │       └─ failure? ──▶ 5. RETRY if eligible, budget, deadline allow
  │
  └─ 6. FALLBACK / DEGRADE if all attempts fail (Chapter 30)
```

Why this order:

- **Deadline first** avoids starting work that cannot finish.
- **Breaker before bulkhead** avoids taking a slot for a call that will be rejected.
- **Bulkhead before call** prevents exceeding capacity.
- **Retry after the call** respects the per-attempt result and the budget.
- **Fallback last** so it is not used while a legitimate retry is still possible.

### What not to do

| Anti-pattern | Consequence |
| ------------ | ----------- |
| Retry before breaker check | Retries a dead dependency |
| Fallback before retry | Hides recoverable errors |
| Bulkhead acquired per retry | Holds slots across backoff |
| Deadline checked after sleep | Wastes the remaining budget |
| Breaker per attempt | Never accumulates failures |

## 29.15 — Preventing amplification

Combining mechanisms can multiply work if each layer adds attempts. Keep the product bounded:

```text
gateway: 1 attempt (no retry)
service: 3 attempts (sole owner)
breaker: rejects when open (no calls)
bulkhead: cap 20 concurrent
→ worst case calls = 3, regardless of retries
```

### Amplification controls

| Control | Effect |
| ------- | ------ |
| One retry owner | Prevents `Π attempts` growth |
| Breaker open rejects | Stops retries during outage |
| Bulkhead cap | Bounds concurrent load |
| Retry budget | Bounds aggregate retries |
| Deadline | Bounds total time/attempts |
| Admission control | Bounds accepted work |

> ⚠️ **Hazard.** A breaker that opens *after* the retry loop has already issued three calls does not
> prevent the first burst. Check the breaker **before each attempt**, and let the retry policy stop
> as soon as it opens.

## 29.16 — Dependency resilience policy

Write one policy per dependency and keep it in code/config, not in a wiki.

```yaml
dependency: stripe
  timeout:
    connect: 1s
    request: 3s
  deadline: 8s
  retry:
    owner: payment-service
    maxAttempts: 3
    baseDelay: 250ms
    jitter: full
    retryOn: [timeout, 429, 5xx, connection]
    honorRetryAfter: true
  breaker:
    failureRate: 0.5
    minRequests: 30
    window: 30s
    cooldown: 15s
    halfOpenProbes: 3
  bulkhead:
    maxConcurrent: 20
    maxQueue: 40
  fallback:
    mode: fail-closed
    response: 503
    retryAfter: 5s
  idempotency:
    required: true
    key: "tenant:order:charge"
    ttl: 24h
```

### Policy review questions

1. What is the worst-case latency, including retries and backoff?
2. What happens to requests while the breaker is open?
3. What is the maximum concurrent load this dependency can receive?
4. Is every retried operation idempotent or keyed?
5. Does the fallback preserve correctness (not just availability)?

## Worked example — one slow provider

```text
t=0    1000 requests arrive
       admission control admits 20 (bulkhead), queues 40, rejects rest with 503
t=0.1  calls time out at 3s
t=3.2  retries begin (attempt 2), breaker records failures
t=6.0  failure rate > 50% over 30s → breaker opens
t=6.1  new requests fail fast with 503 + Retry-After, no provider calls
t=21   cooldown ends → half-open, 1 probe
t=21.1 probe succeeds → 2 more probes → closed
```

Without composition, the 1,000 requests would have produced 3,000 calls, filled the pool, and
delayed recovery.

## Key data / numbers

- Admission: reject below **50ms** remaining (adjust to your minimum useful work).
- Load-shed thresholds: 70% for batch, 85% for interactive, 95% for critical-only.
- Bulkhead cap: derived from Little's Law (throughput × latency).
- Breaker: 50% over 30s, min 30 requests, 15s cooldown, 3 probes.
- Worst-case calls = attempts of the single owner (e.g. 3).
- `Retry-After` on rejection: **1–10s** depending on expected recovery.

## Real-world use case — Acme SaaS

Acme's checkout path had retries but no admission control. During a sale, traffic tripled; the
payment service queued every request, latency grew past the 10s deadline, and retries tripled the
load. The team added a per-dependency semaphore (20), a bounded queue (40), an early deadline check,
and a breaker checked before each attempt. Under the next spike, checkout admitted what it could
serve, rejected the rest with `503 + Retry-After`, and kept p99 under 3s. Successful checkouts
actually increased because fewer requests timed out after doing partial work.

## Trade-offs

| Control | Protects | Cost |
| ------- | -------- | ---- |
| Admission control | Utilization, latency | Some requests rejected |
| Priority shedding | Critical path | Batch work delayed |
| Breaker before bulkhead | Wasted slots | Slightly more checks |
| One retry owner | Amplification | Cross-team coordination |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Check the deadline before starting work | Start work that cannot finish |
| Check the breaker before each attempt | Retry into an open breaker |
| Acquire a bulkhead slot once per attempt | Hold slots across backoff |
| Shed low-priority work first | Treat all traffic equally |
| Keep one retry owner | Let each layer retry |
| Write the policy down per dependency | Rely on tribal knowledge |

## Common mistakes

- **Admission control after the queue**, which is just a slower overflow.
- **Breaker checked once outside the retry loop**, so retries bypass it.
- **Fallback before retry**, hiding transient recoverability.
- **Bulkhead slot held during backoff**, reducing capacity for no reason.
- **No priority classes**, so exports starve checkout.

## Checklist

- [ ] Admission control rejects doomed and excess work early.
- [ ] Low-priority work is shed before critical work.
- [ ] Mechanisms run in the fixed order.
- [ ] Breaker is checked before every attempt.
- [ ] Bulkhead slot is held only during the call.
- [ ] One retry owner keeps amplification bounded.
- [ ] Every dependency has a written resilience policy.
- [ ] Worst-case latency and load are documented.

## Related

- [Breaker State Machine](../02-deep-dive/01-breaker-state-machine.md)
- [Timeouts and Bulkheads for Acme](../03-practical-examples/02-timeouts-and-bulkheads-for-acme.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../30-graceful-degradation-and-fallbacks/README.md)
- [Chapter 57 — Error Handling Under Load and at Scale](../../../part-22-design-decisions/57-error-handling-under-load-and-at-scale/README.md)
