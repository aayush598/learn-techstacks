# Attempts, Delays, and Jitter

> Part XI · Chapter 27 · Sections 27.6–27.9 · _Estimated reading time: 18 min_
> **Prerequisite:** [Retry Classification and Eligibility](./02-retry-classification-and-eligibility.md)

## In one sentence

A retry policy is defined by **how many attempts**, **how long it waits between them**, and **how
much randomness it adds** — and the default should be a small attempt count with exponential backoff
plus jitter, capped by a deadline.

## Why this matters in production

The delay schedule decides whether a retry helps or hurts. Immediate retries hammer a dependency that
is already failing. Fixed delays synchronize every client, creating a thundering herd on each tick.
Exponential backoff without jitter is better but still aligns clients that started together. **Jitter
is the single cheapest change that prevents coordinated retry storms**, and a cap prevents a single
request from waiting minutes for a dependency that is clearly down.

## 27.6 — Max attempts

`maxAttempts` bounds the work per operation. It is not a measure of optimism; it is a capacity
decision.

| Attempts | Fits | Use for |
| -------- | ---- | ------- |
| 1 | No retry | Non-idempotent, strict latency |
| 2–3 | User-facing calls | Default for APIs and DB |
| 3–5 | Background jobs | Higher tolerance for latency |
| 5–10 | Recoverable async work | With checkpointing and DLQ |

Important distinction: **`maxAttempts` counts the first try**. Three attempts means one initial call
plus two retries. Define this in code (`attempt < maxAttempts`) so it cannot drift between services.

## 27.7 — Fixed delay

Every retry waits the same amount. Simple, predictable, and usually wrong for anything shared.

```text
attempt 1 ── 1s ──▶ attempt 2 ── 1s ──▶ attempt 3
```

It is acceptable for a single-client, low-volume job where the dependency recovers quickly. It is
bad for a fleet: all clients retry at the same instants.

## 27.8 — Exponential backoff

Delay grows with each attempt, giving a struggling dependency increasing room to recover:

```text
delay_n = min(cap, base × multiplier^n)      // n = 0 for the first retry
```

With `base = 200ms`, `multiplier = 2`, `cap = 10s`:

| Retry # | Raw delay | Used |
| ------- | --------- | ---- |
| 1 | 200ms | 200ms |
| 2 | 400ms | 400ms |
| 3 | 800ms | 800ms |
| 4 | 1.6s | 1.6s |
| 5 | 3.2s | 3.2s |
| 6 | 6.4s | 6.4s |
| 7 | 12.8s | 10s (cap) |

The cap matters: without it, attempt 10 waits over three minutes, long past any useful deadline.

## 27.9 — Backoff with jitter

Jitter randomizes the delay so independent clients spread out. There are four common strategies
(AWS Architecture Blog's "Exponential Backoff and Jitter"):

| Strategy | Formula | Behavior |
| -------- | ------- | -------- |
| **None** | `d` | Fully synchronized |
| **Full jitter** | `random(0, d)` | Maximum spread; lowest peak load |
| **Equal jitter** | `d/2 + random(0, d/2)` | Spread with a guaranteed minimum wait |
| **Decorrelated** | `random(base, prev × 3)` | Avoids clusters, tolerates long waits |

**Full jitter is the recommended default** for most services:

```text
sleep = random_between(0, min(cap, base × 2^attempt))
```

### Why jitter works

If 1,000 workers fail at the same moment and retry after exactly 1s, the dependency receives a
1,000-request spike at t=1s, t=3s, t=7s… With full jitter the same 1,000 requests spread across the
whole interval, and the peak collapses.

```text
No jitter:        │████████│          │████████│
Full jitter:      │▁▂▁▃▂▁▁▂▃▁▂▁▃▂▁▁▂▃│  (same count, spread out)
                  t=0      1s         3s
```

## Worked example

```ts
export interface BackoffOptions {
  baseMs?: number;
  capMs?: number;
  multiplier?: number;
  jitter?: "none" | "full" | "equal";
}

export function backoffDelay(attempt: number, opts: BackoffOptions = {}): number {
  const {
    baseMs = 200,
    capMs = 10_000,
    multiplier = 2,
    jitter = "full",
  } = opts;

  const raw = Math.min(capMs, baseMs * Math.pow(multiplier, attempt));

  switch (jitter) {
    case "none":
      return raw;
    case "equal": {
      const half = raw / 2;
      return half + Math.random() * half;
    }
    case "full":
    default:
      return Math.random() * raw;
  }
}
```

```python
import random

def backoff_delay(attempt: int, base: float = 0.2, cap: float = 10.0,
                  multiplier: float = 2.0, jitter: str = "full") -> float:
    raw = min(cap, base * (multiplier ** attempt))
    if jitter == "none":
        return raw
    if jitter == "equal":
        return raw / 2 + random.random() * (raw / 2)
    return random.random() * raw   # full jitter
```

## Key data / numbers

- AWS-recommended default: **full jitter**, `sleep = random(0, min(cap, base × 2^attempt))`.
- Common base: **100–500ms**; common cap: **10–30s**.
- Common multiplier: **2** (occasionally 1.5 for gentler growth).
- `Retry-After` overrides the computed delay when present.
- A 3-attempt policy with a 2s per-attempt timeout and capped backoff typically resolves in **under
  10s**; measure your own worst case.

## Real-world use case — ExportJob

`ExportJob` pulled 10,000 rows from a provider that rate-limited at 100 req/s. The worker pool hit
`429` in bursts, and the fixed 1s retry caused every worker to retry on the same second, producing a
second spike and a second wave of `429`s. Switching to exponential backoff with **full jitter**
(`base=250ms`, `cap=8s`) spread the retries across the window; `429` volume fell by roughly 70% and
the export completed within its SLA. No change was made to the provider or the request rate.

## Trade-offs

| Strategy | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Fixed delay | Predictable | Synchronizes fleet | Single low-volume client |
| Exponential, no jitter | Gives dependency room | Still clusters | One caller, no fleet |
| Full jitter | Best spread, simple | Some retries are very early | Default |
| Equal jitter | Guaranteed minimum wait | Less spread | Latency-sensitive |
| Decorrelated | Avoids long clusters | Harder to reason about | Long-running jobs |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Cap the backoff | Let delay grow unbounded |
| Use full jitter by default | Use fixed delays across a fleet |
| Honor `Retry-After` over computed delay | Ignore server guidance |
| Count the first try in `maxAttempts` | Define attempts differently per service |
| Include the delay in the deadline check | Sleep past the caller's deadline |

## Common mistakes

- **Jitter applied to the wrong term.** Jitter the final delay, not the attempt number.
- **No cap.** Attempt 8 waits minutes while the caller has already timed out.
- **Retry-After ignored.** The server said 120s; the client retried in 200ms.
- **Sleeping after the last attempt.** The loop sleeps, then exits without another call.
- **Randomness without a seed in tests.** Tests become flaky; inject the RNG.

## Checklist

- [ ] `maxAttempts` is explicit and counts the initial attempt.
- [ ] Delay is exponential and capped.
- [ ] Jitter is enabled by default.
- [ ] `Retry-After` overrides computed delay.
- [ ] No sleep occurs after the final attempt.
- [ ] Backoff is injected/mockable for tests.

## Related

- [Backoff and Jitter Math](../02-deep-dive/01-backoff-and-jitter-math.md)
- [Budgets, Deadlines, and Server Guidance](./04-budgets-deadlines-and-server-guidance.md)
- [Reusable Retry Utility with Jitter](../03-practical-examples/01-reusable-retry-utility-with-jitter.md)
- [Retry vs Fail Decision Guide](../05-reference/README.md)
