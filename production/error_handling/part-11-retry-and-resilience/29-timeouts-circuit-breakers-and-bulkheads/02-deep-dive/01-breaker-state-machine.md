# Breaker State Machine

> Part XI · Chapter 29 · Sections 29.5–29.9, 29.14 · _Estimated reading time: 21 min_
> **Prerequisite:** [Circuit Breaker States and Conditions](../01-concepts/02-circuit-breaker-states-and-conditions.md)

## In one sentence

The breaker's correctness lives in its **transitions and counters**: a sliding window decides when to
open, a jittered cooldown decides when to probe, and a small set of consecutive successes decides when
to close — with hysteresis to stop it flapping.

## Why this matters in production

Two breakers can share the same three state names and behave completely differently. One opens on a
single `500`; another opens only when 50% of 30+ requests fail. One lets all traffic through on
half-open; another serializes a single probe. One closes after one success and immediately reopens.
The differences are all in the transition rules, and those rules determine whether the breaker
protects the dependency or becomes a second source of instability.

## The full state machine

```text
                 ┌─────────────────────────────────────────┐
                 │                 CLOSED                  │
                 │  allow all; record outcomes in window   │
                 └───────┬─────────────────────────┬───────┘
                         │                         │
      window: rate >= threshold              success in window
      and requests >= minRequests             (no transition)
                         │
                         ▼
                 ┌─────────────────────────────────────────┐
                 │                  OPEN                   │
                 │  reject fast; schedule cooldown         │
                 │  cooldown = base × 2^(opens-1), capped  │
                 └───────────────────┬─────────────────────┘
                                     │ cooldown elapsed (+ jitter)
                                     ▼
                 ┌─────────────────────────────────────────┐
                 │               HALF_OPEN                 │
                 │  allow up to probeLimit concurrent      │
                 │  probes; count successes/failures       │
                 └───────┬─────────────────────────┬───────┘
                         │                         │
              successes >= closeThreshold     any failure
                         │                         │
                         ▼                         ▼
                      CLOSED                     OPEN
                                      (cooldown grows, then resets
                                       after a stable close)
```

## Counters and windows

### Sliding window vs rolling window

| Window | Behavior | Use |
| ------ | -------- | --- |
| **Rolling/tumbling** | Reset every N seconds | Simple, coarse |
| **Sliding (count)** | Last N requests | Stable under variable rate |
| **Sliding (time)** | Requests in last N seconds | Matches "recent health" |

A sliding window avoids the boundary artifact where a burst of failures at the end of one window is
forgotten at the start of the next.

```ts
interface Sample { at: number; ok: boolean; }

class SlidingWindow {
  private samples: Sample[] = [];
  constructor(private windowMs: number, private maxSamples = 1000) {}

  record(ok: boolean, now = Date.now()) {
    this.samples.push({ at: now, ok });
    this.evict(now);
  }

  private evict(now: number) {
    const cutoff = now - this.windowMs;
    while (this.samples.length && this.samples[0].at < cutoff) this.samples.shift();
    if (this.samples.length > this.maxSamples) {
      this.samples.splice(0, this.samples.length - this.maxSamples);
    }
  }

  stats(now = Date.now()) {
    this.evict(now);
    const total = this.samples.length;
    const failures = this.samples.filter((s) => !s.ok).length;
    return { total, failures, rate: total ? failures / total : 0 };
  }
}
```

### The opening predicate

```text
shouldOpen =
    total >= minRequests
    AND failureRate >= failureThreshold
```

Both conditions matter. Without `minRequests`, a single failure at 1 req/s opens the breaker. Without
`failureThreshold`, any failure opens it.

## Cooldown and backoff

An open breaker should not retry the dependency at a fixed interval forever. Grow the cooldown on
repeated failures so a persistently broken dependency is probed less often:

```text
cooldown(n) = min(cap, base × 2^(n-1)) × jitter(0.8..1.2)
```

| Consecutive opens | Cooldown (base 10s, cap 5min) |
| ----------------- | ----------------------------- |
| 1 | 10s |
| 2 | 20s |
| 3 | 40s |
| 4 | 80s |
| 5 | 160s |
| 6+ | 300s (cap) |

Reset the exponent after the breaker stays closed for a stable period (e.g. 60s), not immediately on
the first success — otherwise a flapping dependency probes at the base interval forever.

## Half-open probe policy

### Concurrent probes

| Policy | Behavior | Risk |
| ------ | -------- | ---- |
| **Serial** (1 at a time) | Safest | Slow recovery |
| **Limited** (2–5) | Balanced | Slightly more load |
| **All** | Fastest | Recovery stampede |

Recommended: **serial probes** for critical dependencies, limited concurrency for high-throughput
ones.

### Close threshold

Require `closeThreshold` **consecutive** successes (3–5) before closing. A single success may be
luck; consecutive successes indicate recovery.

```text
probe 1 ok  → remain HALF_OPEN (1/3)
probe 2 ok  → remain HALF_OPEN (2/3)
probe 3 ok  → CLOSED, reset window
probe 2 fail → OPEN, cooldown grows
```

### Probe timeouts

A probe must have its own timeout, shorter than or equal to the normal request timeout. A probe that
hangs blocks the state machine.

## Hysteresis

Hysteresis prevents flapping by making "open" and "close" thresholds different:

| Direction | Threshold |
| --------- | --------- |
| Open when | failure rate ≥ 50% |
| Close when | 3 consecutive successes |
| Stay open | any probe failure |

You can also require a **minimum dwell time** in each state (e.g. 5s) so transitions cannot happen
faster than the system can react.

## Metrics and observability

Emit at least:

```text
breaker_state{dependency="stripe"} 0|1|2        (closed|half_open|open)
breaker_transitions_total{dependency,from,to}
breaker_rejected_total{dependency}
breaker_failures_total{dependency}
breaker_probe_success_total{dependency}
```

Alert on `state=open` for longer than an expected recovery window, and on frequent transitions
(flapping).

## Worked example — trace

```text
t=0     CLOSED, window empty
t=1..40 40 requests, 2 failures (5%) → stays CLOSED
t=41..60 20 requests, 12 failures (60%) → total 60, rate 14/60=23% → stays CLOSED
t=61..80 20 requests, 15 failures → total 80, rate 29/80=36%
t=81..90 10 requests, 8 failures → total 90, rate 37/90=41%
t=91..100 10 requests, 9 failures → total 100, rate 46/100=46%
t=101..105 5 requests, 4 failures → total 105, rate 50/105=48%
t=106..110 5 requests, 4 failures → total 110, rate 54/110=49%
t=111..115 5 requests, 5 failures → total 115, rate 59/115=51% → OPEN
```

Note how the rate lags a sudden outage: the window still contains healthy history. For critical
dependencies, use a **shorter window** or a **consecutive-failure** secondary trigger.

## Key data / numbers

- Window: **10–60s** sliding; shorter for critical paths.
- Min requests: **20–50**.
- Failure threshold: **50%** (20–30% for critical).
- Cooldown: **5–30s**, exponential up to **5min**.
- Half-open probes: **1–5**, close after **3–5 consecutive** successes.
- Probe timeout: ≤ normal request timeout.
- Alert on open > **2× expected recovery**.

## Real-world use case — Acme SaaS

Acme's breaker used a 60s tumbling window and counted all non-2xx responses. A brief provider
incident produced 40 failures in 10s, but the window's healthy start kept the rate below 50%, so the
breaker never opened; retries hammered the provider for the full minute. After switching to a 15s
sliding window, excluding `4xx`, and adding a secondary "10 consecutive failures" trigger, the
breaker opened within ~2s of a real outage and stopped the retry storm. False opens stayed near zero
because validation errors no longer counted.

## Trade-offs

| Parameter | Lower | Higher |
| --------- | ----- | ------ |
| Window | Faster reaction, more noise | Stable, slower |
| Threshold | Protects early, flaps | Stable, slower |
| Min requests | Sensitive | Insensitive at low traffic |
| Cooldown | Fast recovery | Less probing load |
| Close threshold | Fast recovery | Safer, slower |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use a sliding window | Use a tumbling window for critical paths |
| Require a minimum sample | Open on one failure |
| Grow cooldown on repeated opens | Probe at a fixed interval forever |
| Serialize half-open probes | Send full traffic on probe |
| Require consecutive successes | Close after one success |
| Emit state-transition metrics | Only log open/close |

## Common mistakes

- **Threshold checked before the minimum sample**, opening on low traffic.
- **Cooldown reset on every open**, causing frequent probes.
- **Closing on a single success**, flapping during partial recovery.
- **No probe timeout**, so half-open hangs.
- **Counting validation errors**, opening on bad clients.

## Checklist

- [ ] Window type and size are documented.
- [ ] `minRequests` and `failureThreshold` are both enforced.
- [ ] Critical paths have a secondary consecutive-failure trigger.
- [ ] Cooldown grows with repeated opens and is capped.
- [ ] Half-open probes are limited and have timeouts.
- [ ] Close requires consecutive successes.
- [ ] State and transitions are exported as metrics.

## Related

- [Circuit Breaker States and Conditions](../01-concepts/02-circuit-breaker-states-and-conditions.md)
- [Circuit Breaker Implementation](../03-practical-examples/01-circuit-breaker-implementation.md)
- [Admission Control and Combining Mechanisms](../01-concepts/04-admission-control-and-combining-mechanisms.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../30-graceful-degradation-and-fallbacks/README.md)
