# Backoff and Jitter Math

> Part XI · Chapter 27 · Sections 27.6–27.9, 27.11 · _Estimated reading time: 20 min_
> **Prerequisite:** [Attempts, Delays, and Jitter](../01-concepts/03-attempts-delays-and-jitter.md)

## In one sentence

Backoff math is how you answer two questions before shipping a policy: **what is the worst-case
elapsed time?** and **what load does this create when everyone retries at once?**

## Why this matters in production

A retry policy is a latency and capacity contract. If you cannot compute its worst case, you cannot
promise an SLA or size a worker pool. The most common production surprises are not exotic: an
uncapped exponential that waits four minutes on attempt 8, a jitter strategy that leaves the
expected wait far below what the team assumed, or a deadline that the backoff schedule can never fit
inside.

## The base schedule

For attempt index `n` starting at `0` for the first retry:

```text
raw(n) = min(cap, base × multiplier^n)
```

With `base = 200ms`, `multiplier = 2`, `cap = 10,000ms`:

| n | `base × 2^n` | `raw(n)` |
| - | ------------ | -------- |
| 0 | 200 | 200 |
| 1 | 400 | 400 |
| 2 | 800 | 800 |
| 3 | 1,600 | 1,600 |
| 4 | 3,200 | 3,200 |
| 5 | 6,400 | 6,400 |
| 6 | 12,800 | 10,000 |
| 7 | 25,600 | 10,000 |

The **uncapped** sum for `k` retries is geometric:

```text
sum = base × (multiplier^k − 1) / (multiplier − 1)
```

For `base=200`, `multiplier=2`, `k=7`: `200 × (128 − 1) = 25,400ms` (25.4s). The cap reduces this to
`200+400+800+1600+3200+6400+10000 = 22,600ms`. Still far beyond most request deadlines — which is why
attempt count alone is not a policy.

## Jitter strategies, formally

Let `d = raw(n)` and `U(a,b)` be a uniform random value.

| Strategy | Delay | Expected delay | Variance |
| -------- | ----- | -------------- | -------- |
| None | `d` | `d` | 0 |
| Full jitter | `U(0, d)` | `d/2` | High |
| Equal jitter | `d/2 + U(0, d/2)` | `0.75d` | Medium |
| Decorrelated | `U(base, prev×3)` | varies | High, anti-cluster |

### Expected total wait

Because expectation is linear, the expected wait for a sequence is the sum of expected delays:

```text
E[total] = Σ E[delay_i]
```

For full jitter: `E[total] = 0.5 × Σ raw(i)`.
For equal jitter: `E[total] = 0.75 × Σ raw(i)`.

This is the number to use for capacity planning; the worst case (`Σ raw`) is the number to use for
deadlines.

## Worked example — a 4-attempt policy

Policy: `base=250ms`, `multiplier=2`, `cap=4s`, `maxAttempts=4` (3 retries), per-attempt timeout
`1.5s`.

| Attempt | Call timeout | Delay before next (raw) | Cumulative worst case |
| ------- | ------------ | ----------------------- | --------------------- |
| 1 | 1.5s | 250ms | 1.75s |
| 2 | 1.5s | 500ms | 3.75s |
| 3 | 1.5s | 1,000ms | 6.25s |
| 4 | 1.5s | — | 7.75s |

Worst case ≈ **7.75s**. With full jitter the expected wait is `0.5 × (250+500+1000) = 875ms`, so
expected total ≈ `6 × 1.5s? no` — careful: only four calls, `4 × 1.5 = 6s` plus expected `0.875s`
≈ **6.9s**. Worst case is close enough that an **8s deadline** is the right envelope; a **5s
deadline** would make the last attempt impossible and the policy misleading.

## Choosing the cap

The cap controls how long a single request is willing to wait for a dependency that is clearly down.

| Context | Suggested cap | Reason |
| ------- | ------------- | ------ |
| User-facing API | 2–5s | Beyond that the user has left |
| Internal RPC | 5–10s | Tight request budgets |
| Provider call | 10–30s | Providers often recover in seconds |
| Background job | 5–15 min | Long outages are survivable |
| Rate-limit wait | Honor `Retry-After` | Server knows better |

Set the cap below the total deadline minus the call time; otherwise the cap is decorative.

## Choosing the base

`base` should be larger than the dependency's typical recovery time and smaller than the user's
patience.

- Too small (10ms): retries pile onto the same failure window.
- Too large (5s): a single blip costs seconds of latency.
- A common starting point is **200–500ms** for APIs, **1–5s** for jobs.

## Jitter and the thundering herd

Suppose `N` clients fail simultaneously and retry with delay `d`. Without jitter, the arrival rate at
each retry instant is `N`. With full jitter over `[0,d]`, the expected rate is `N/d` per unit time —
spread across the window. The peak drops by roughly a factor of `d` (in the same units).

```text
N = 1000, d = 1s
no jitter:  1000 req at t=1.0s
full jitter: ~1000 req spread over 0–1.0s  → ~1000/s average, no synchronized spike
```

The total work is identical. Only the *shape* changes, and the shape is what a saturated dependency
feels.

## Deadline interaction

A deadline check must include the **next** delay and the **next** call timeout:

```text
attempt_allowed(now) =
    now + delay(n) + min(perAttempt, deadline − now) < deadline
```

If the check fails, stop. Sleeping first and checking later wastes the very time you were trying to
protect.

```ts
function plan(deadline: number, now: number, n: number, perAttempt: number) {
  const delay = backoffDelay(n);
  const remaining = deadline - now;
  if (remaining <= 0) return { action: "fail" as const };
  if (delay + Math.min(perAttempt, remaining) >= remaining) {
    return { action: "fail" as const };
  }
  return { action: "retry" as const, delay, timeout: Math.min(perAttempt, remaining - delay) };
}
```

## Key data / numbers

- AWS full-jitter formula: `sleep = random_between(0, min(cap, base × 2^attempt))`.
- Expected full-jitter wait is **half** the raw delay; equal jitter is **75%**.
- Uncapped geometric sum: `base × (multiplier^k − 1) / (multiplier − 1)`.
- Common caps: 2–5s (API), 10–30s (provider), 5–15 min (jobs).
- Common bases: 200–500ms (API), 1–5s (jobs).
- Always compute the worst case including **all** per-attempt timeouts.

## Real-world use case — Acme SaaS

Acme's `ExportJob` used `base=1s`, `multiplier=2`, no cap, `maxAttempts=8`. The team assumed "a few
seconds." The real worst case was `1+2+4+8+16+32+64 = 127s` of backoff alone, plus eight 30s call
timeouts — over **6 minutes** per page, while the job SLA was 5 minutes. Adding `cap=15s` and
`maxAttempts=5` brought the worst case to `1+2+4+8 = 15s` of backoff plus 150s of calls, and full
jitter spread retries across worker restarts. Pages that previously timed out now completed, and the
SLA held during a provider slowdown.

## Trade-offs

| Choice | Pros | Cons |
| ------ | ---- | ---- |
| Larger base | Fewer synchronized retries | Higher latency |
| Smaller cap | Predictable deadlines | Less recovery room |
| Full jitter | Best spread | Early retries may fail again |
| Equal jitter | Guaranteed minimum | Less spread |
| Decorrelated | Handles clustered failures | Harder to bound |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Compute worst-case elapsed time | Assume "3 retries is fast" |
| Cap below the deadline | Use an uncapped exponential |
| Jitter the final delay | Jitter the attempt counter |
| Use expectation for capacity planning | Use it for deadlines |
| Recompute delay after `Retry-After` | Ignore the server hint |

## Common mistakes

- **Forgetting call time in the worst case.** Backoff is only part of elapsed time.
- **Jittering `base` instead of the result.** The schedule still synchronizes.
- **Cap larger than the deadline.** The cap never takes effect.
- **Using the mean as the deadline.** Half of requests exceed it.
- **Sharing RNG state** across concurrent retries, correlating delays.

## Checklist

- [ ] Worst-case elapsed time is documented.
- [ ] Expected wait is used for capacity planning.
- [ ] Cap is below the deadline.
- [ ] Delay is jittered, not the attempt index.
- [ ] Deadline check includes the next delay and timeout.
- [ ] Tests inject a deterministic RNG.

## Related

- [Attempts, Delays, and Jitter](../01-concepts/03-attempts-delays-and-jitter.md)
- [Budgets, Deadlines, and Server Guidance](../01-concepts/04-budgets-deadlines-and-server-guidance.md)
- [Retry Amplification and Budgets](./02-retry-amplification-and-budgets.md)
- [Reusable Retry Utility with Jitter](../03-practical-examples/01-reusable-retry-utility-with-jitter.md)
