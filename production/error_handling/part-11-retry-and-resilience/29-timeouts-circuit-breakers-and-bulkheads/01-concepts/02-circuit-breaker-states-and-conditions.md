# Circuit Breaker States and Conditions

> Part XI · Chapter 29 · Sections 29.5–29.9 · _Estimated reading time: 20 min_
> **Prerequisite:** [Why Timeouts and Deadlines](./01-why-timeouts-and-deadlines.md)

## In one sentence

A circuit breaker is a **three-state feedback controller** — closed, open, half-open — that stops
calling a dependency when its failure rate crosses a threshold, then probes cautiously before
restoring traffic.

## Why this matters in production

Retries help when failures are rare; they hurt when a dependency is down. Without a breaker, every
request keeps retrying a dead service, consuming workers, connections, and budget, and delaying the
user's error. With a breaker, the system fails fast during an outage, gives the dependency breathing
room, and automatically recovers when it comes back. The hard part is not the state machine; it is
choosing thresholds that open on *real* failure and do not flap on normal noise.

## 29.5 — The states

```text
                 failures >= threshold
     ┌────────┐  in the window        ┌────────┐
     │ CLOSED │ ────────────────────▶ │  OPEN  │
     └────┬───┘                        └───┬────┘
          │                                │ cooldown elapses
          │ success resets                 ▼
          │ counter                  ┌────────────┐
          │                          │ HALF_OPEN  │
          │      probe succeeds      └─────┬──────┘
          └────────────────────────────────┘
                                    probe fails
                                          │
                                          ▼
                                       OPEN
```

| State | Behavior | Purpose |
| ----- | -------- | ------- |
| **Closed** | Calls pass through; outcomes recorded | Normal operation |
| **Open** | Calls fail immediately (or fallback) | Stop hammering a failing dependency |
| **Half-open** | A limited number of probes allowed | Test recovery without a stampede |

The breaker does not retry; it **rejects**. Retry (Chapter 27) is a separate policy that must respect
the open state.

## 29.6 — Opening conditions

A breaker should open on a **rate** of failures over a **window**, not on a single error.

### Typical configuration

| Parameter | Common starting value |
| --------- | --------------------- |
| Failure-rate threshold | 50% (sometimes 20–30% for critical paths) |
| Minimum requests | 20–50 in the window |
| Window | 10–60s (sliding or rolling) |
| Open cooldown | 5–30s (with jitter) |
| Half-open probes | 1–5 sequential requests |

### What counts as a failure

Define this explicitly. Usually:

| Outcome | Counts as failure? |
| ------- | ------------------ |
| Timeout | Yes |
| Connection error | Yes |
| `5xx` | Yes |
| `429` | Yes (dependency is overloaded) |
| `4xx` (validation/auth) | **No** — the caller is wrong, not the dependency |
| Business decline | No |
| Cancellation | No |

Counting `4xx` as failures is a classic bug: a burst of bad client requests opens the breaker and
takes down the dependency for everyone.

### Why a minimum request count

At low traffic, one failure is 100% of a tiny sample. A minimum (e.g. 20 requests) prevents opening
on a single unlucky call.

## 29.7 — Half-open

Open does not mean "never call again." After a cooldown, the breaker moves to half-open and allows a
small number of probes.

Rules for half-open:

1. **Serialize probes.** Allow one at a time, or a small fixed number.
2. **Success threshold.** Require `N` consecutive successes (commonly 3–5) before closing.
3. **Any failure reopens immediately** (reset the cooldown, optionally with exponential growth).
4. **Do not send full traffic** during probing; that is just reopening the floodgates.
5. **Add jitter to the cooldown** so many instances do not probe simultaneously.

```text
OPEN (cooldown 10s ± jitter)
  → HALF_OPEN: allow 1 probe
      → success: allow 1 more (up to 3)
          → 3 successes: CLOSED
      → failure: OPEN (cooldown × 1.5, capped)
```

## 29.8 — Fallback errors

When the breaker is open, the call fails fast. That failure still needs a representation:

| Outcome | Status/code | Retryable? |
| ------- | ----------- | ---------- |
| Dependency temporarily unavailable | `503` + `Retry-After` | Yes, after cooldown |
| Feature optional | Degraded response (Ch. 30) | N/A |
| Circuit open, no fallback | `503 CIRCUIT_OPEN` | Yes |
| Half-open probe failed | `503` | Yes |

Do **not** return `500` for an open breaker: `503` with `Retry-After` tells clients the dependency is
temporarily unavailable and when to try again. Preserve the last real failure as the cause for logs.

## 29.9 — Misuse

| Misuse | Consequence | Fix |
| ------ | ----------- | --- |
| Counting all errors, including `4xx` | Opens on client mistakes | Count only dependency failures |
| No minimum request count | Opens on one failure | Require a sample |
| Single-attempt threshold | Flaps constantly | Use a window and rate |
| Half-open sends full traffic | Stampede on recovery | Limit probes |
| No jitter on cooldown | Synchronized probes | Add jitter |
| Breaker around non-idempotent writes with no fallback | Data loss | Fallback must be safe |
| Breaker as a retry mechanism | No recovery logic | Combine with retry, not replace |
| Per-request breaker instance | Never accumulates state | One per dependency per process |

> ⚠️ **Hazard.** A breaker with no fallback turns a dependency outage into an immediate user-facing
> error. That may be correct for critical paths, but it must be a decision — see Chapter 30.

## Worked example — thresholds

Suppose a dependency handles 100 req/s. You want to open when the failure rate exceeds 50% over 30s,
with at least 30 requests:

```text
window:            30s
min requests:      30
failure threshold: 0.5
cooldown:          15s ± 30% jitter
half-open probes:  3 consecutive successes
```

At 100 req/s, the window sees ~3,000 requests, so noise is smoothed. At 0.2 req/s, the minimum of 30
takes 150s to accumulate — acceptable for a low-traffic dependency, but consider a longer window and
lower minimum if you need faster reaction.

## Key data / numbers

- Failure-rate threshold: **50%** typical; 20–30% for critical paths.
- Minimum requests: **20–50**.
- Window: **10–60s** sliding/rolling.
- Cooldown: **5–30s**, jittered.
- Half-open probes: **1–5**, with 3–5 consecutive successes to close.
- Count `5xx`, timeouts, connection errors, `429`; do **not** count `4xx`.
- Open response: `503` + `Retry-After`.

## Real-world use case — Acme SaaS

Acme wrapped its Stripe client in a breaker that counted *all* errors. A marketing campaign sent
thousands of requests with expired cards, producing `402` declines; the breaker saw >50% "failures"
and opened, blocking legitimate charges for 30s at a time. The team changed the failure predicate to
count only timeouts, connection errors, `429`, and `5xx`, added a 30-request minimum, and required 3
half-open successes. Breaker opens during real Stripe incidents still happened, but false opens from
customer declines dropped to zero.

## Trade-offs

| Threshold | Pros | Cons |
| --------- | ---- | ---- |
| Low (20%) | Fast protection | Flaps on noise |
| High (50%) | Stable | Slow to protect |
| Short window | Reactive | Noisy |
| Long window | Stable | Slow to react |
| Aggressive probes | Fast recovery | Risk of reopening flood |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Open on failure *rate* over a window | Open on one error |
| Exclude `4xx` and business declines | Count every non-2xx |
| Use a minimum request count | Trust tiny samples |
| Limit half-open probes | Send full traffic on probe |
| Jitter the cooldown | Synchronize instances |
| Keep one breaker per dependency | Create one per request |

## Common mistakes

- **Breaker instance created per call**, so it never accumulates state.
- **Half-open with no probe limit**, causing a recovery stampede.
- **No fallback**, turning a short outage into a hard failure.
- **Never closing**, because the success threshold is effectively unreachable.
- **Counting client errors**, opening on bad input.

## Checklist

- [ ] Breaker is one instance per dependency per process.
- [ ] Failure predicate excludes `4xx`.
- [ ] Threshold is a rate over a window with a minimum sample.
- [ ] Cooldown is jittered.
- [ ] Half-open probes are limited and require consecutive successes.
- [ ] Open state returns `503` + `Retry-After` or a safe fallback.
- [ ] Breaker metrics expose state and transitions.

## Related

- [Breaker State Machine](../02-deep-dive/01-breaker-state-machine.md)
- [Circuit Breaker Implementation](../03-practical-examples/01-circuit-breaker-implementation.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../30-graceful-degradation-and-fallbacks/README.md)
- [Chapter 27 — Retry Policies](../../27-retry-policies/README.md)
