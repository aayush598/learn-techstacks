# Budgets, Deadlines, and Server Guidance

> Part XI · Chapter 27 · Sections 27.10–27.14 · _Estimated reading time: 17 min_
> **Prerequisite:** [Attempts, Delays, and Jitter](./03-attempts-delays-and-jitter.md)

## In one sentence

Attempts bound the *count*, but a **deadline** bounds the *time* and a **retry budget** bounds the
*aggregate load* — and when the server tells you when to come back (`Retry-After`), you obey it
instead of guessing.

## Why this matters in production

Without a deadline, a retry loop can outlive the request that triggered it. The user has already
received a `504`, but the server keeps retrying, holding connections and worker slots for a result
nobody will read. Without a budget, a small percentage of failing requests can multiply into a large
percentage of extra traffic, which is precisely what a saturated dependency cannot handle. Deadlines
and budgets are what keep retries *proportional* to the value of the request.

## 27.10 — Retry budgets

A retry budget caps retries as a fraction of successful (or total) requests. Instead of allowing
every failed request 3 retries independently, the system as a whole limits retry traffic.

```text
retry_budget = retries_allowed / total_requests
```

Common implementation (as popularized by Envoy and gRPC): maintain a token bucket where each
successful request earns a small number of retry tokens, and each retry costs one. During normal
operation the bucket is full and retries flow; during an outage, successes stop, tokens drain, and
retries are suppressed.

| Parameter | Typical starting value |
| --------- | ---------------------- |
| Budget ratio | 10–20% of requests |
| Token earn per success | 1 |
| Token cost per retry | 1 (or 5 for high-cost calls) |
| Minimum retries per window | A small floor so low-traffic services still retry |

Budgets are **per dependency and per caller**, not global. A global budget lets one noisy caller
consume everyone else's retry capacity.

## 27.11 — Retry deadlines

A deadline is an absolute point in time by which the operation must finish, derived from the caller's
remaining time. Every retry checks:

```text
now + next_backoff + per_attempt_timeout < deadline
```

If the next attempt cannot fit, **stop now** and return the last failure. Sleeping until the deadline
only to fail is strictly worse than failing immediately.

```ts
function canAttempt(now: number, deadline: number, nextDelay: number, attemptTimeout: number) {
  return now + nextDelay + attemptTimeout < deadline;
}
```

Deadlines propagate downstream (Chapter 29.3). If you have 4 seconds left, do not issue a call with
a 10-second timeout.

## 27.12 — Total vs per-attempt timeout

These are different budgets and must both exist:

| Timeout | Bounds | Set by |
| ------- | ------ | ------ |
| **Per-attempt timeout** | One network call | The caller's client |
| **Total operation timeout / deadline** | All attempts plus backoff | The request/job boundary |

Example: a 10s total deadline with a 2s per-attempt timeout and 3 attempts can spend at most 6s on
calls and ~2–3s on backoff. If the first call hangs for 9s, there is no room for a second attempt —
the policy must detect that rather than starting one.

> ⚠️ **Hazard.** A per-attempt timeout longer than the remaining deadline guarantees a retry that
> cannot complete. Compute the effective timeout as `min(perAttempt, deadline - now)`.

## 27.13 — Server instructions

Servers often know more than clients about when capacity will return. Prefer explicit signals:

| Signal | Meaning | Client action |
| ------ | ------- | ------------- |
| `Retry-After: 120` | Wait 120 seconds | Sleep at least that long |
| `Retry-After: Wed, 21 Oct 2026 07:28:00 GMT` | Wait until this HTTP date | Convert to a delay |
| gRPC `RESOURCE_EXHAUSTED` + retry info | Provider-specific backoff | Honor the hint |
| Provider error body (`retry_after`, `retry_after_ms`) | Vendor hint | Parse in the adapter, normalize |
| HTTP `503` without `Retry-After` | Temporary unavailability | Exponential backoff + jitter |

Rules:

1. **`Retry-After` wins** over your computed backoff for that attempt.
2. **Cap it against your deadline.** If the server says 300s and you have 5s, fail now.
3. **Normalize vendor hints** into one internal `retryAfterMs` at the adapter boundary.
4. **Do not retry before the hint.** Early retries are what the header exists to prevent.

## 27.14 — Retry-After in practice

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 30
Content-Type: application/problem+json

{ "type": "https://errors.acme.example/rate-limited", "status": 429 }
```

```ts
function parseRetryAfter(value: string | null, now = Date.now()): number | undefined {
  if (!value) return undefined;
  const seconds = Number(value);
  if (Number.isFinite(seconds)) return Math.max(0, seconds * 1000);
  const date = Date.parse(value);
  if (!Number.isNaN(date)) return Math.max(0, date - now);
  return undefined; // malformed: fall back to jittered backoff
}

function delayForAttempt(attempt: number, err: AppError): number {
  const hint = err.retryAfterMs;
  const computed = backoffDelay(attempt);
  if (hint === undefined) return computed;
  return Math.max(hint, computed * 0.5); // never earlier than the hint
}
```

## Worked example — deadline-aware loop

```ts
async function retryWithDeadline<T>(
  op: () => Promise<T>,
  opts: {
    maxAttempts: number;
    deadline: number;        // absolute epoch ms
    perAttemptMs: number;
    isRetryable: (e: unknown) => boolean;
    delay: (attempt: number, e: unknown) => number;
  },
): Promise<T> {
  let lastError: unknown;

  for (let attempt = 0; attempt < opts.maxAttempts; attempt++) {
    const remaining = opts.deadline - Date.now();
    if (remaining <= 0) break;

    try {
      return await withTimeout(op(), Math.min(opts.perAttemptMs, remaining));
    } catch (err) {
      lastError = err;
      if (!opts.isRetryable(err) || attempt === opts.maxAttempts - 1) break;

      const wait = opts.delay(attempt, err);
      if (Date.now() + wait >= opts.deadline) break; // no room left
      await sleep(wait);
    }
  }

  throw lastError;
}
```

## Key data / numbers

- Retry budget ratio: commonly **10–20%** of requests.
- `Retry-After` supports **delta-seconds** and **HTTP-date** formats (RFC 9110).
- `429` and `503` are the statuses most likely to carry `Retry-After`.
- Suggested default: 3 attempts, 2s per-attempt timeout, 10s total deadline.
- A deadline should be **less** than the caller's timeout, leaving time to serialize the error.

## Real-world use case — Acme SaaS

Acme's API gateway had a 30s client timeout, but the internal `EmailService` retried 5 times with a
10s per-attempt timeout. When the email provider degraded, each request could occupy a worker for
~50s; the gateway had already returned `504`, but workers stayed busy. Queue depth grew until the
whole API slowed. The fix: a 12s total deadline derived from the request budget, a 3s per-attempt
timeout, and a 15% retry budget per dependency. Worker occupancy during the next provider incident
stayed flat, and the API remained responsive.

## Trade-offs

| Mechanism | Protects against | Cost |
| --------- | ---------------- | ---- |
| Deadline | Wasted work after caller gives up | Needs propagation |
| Retry budget | Aggregate retry storms | Can suppress useful retries |
| `Retry-After` | Synchronized retries | Depends on server honesty |
| Per-attempt timeout | Hung connections | Too-short values cause false failures |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Derive the deadline from the caller | Invent a fresh 30s budget at each layer |
| Clamp per-attempt timeout to remaining time | Use a timeout longer than the deadline |
| Obey `Retry-After` when present | Retry earlier than the server asked |
| Budget retries per dependency | Share one global retry budget |
| Stop when the next attempt cannot fit | Sleep until the deadline, then fail |

## Common mistakes

- **Deadline measured from process start**, not request arrival.
- **`Retry-After` parsed as milliseconds** when it is seconds.
- **Budget without a floor**, so low-traffic services never retry.
- **Retrying `429` immediately** because the computed backoff is smaller than the hint.
- **No total timeout**, so attempts individually succeed but the operation exceeds SLA.

## Checklist

- [ ] Every retry loop accepts a deadline, not just an attempt count.
- [ ] Per-attempt timeout is clamped to remaining time.
- [ ] `Retry-After` overrides computed backoff.
- [ ] A retry budget exists per dependency.
- [ ] The policy stops before sleeping past the deadline.
- [ ] Deadlines propagate to downstream calls.

## Related

- [Retry Amplification and Budgets](../02-deep-dive/02-retry-amplification-and-budgets.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Chapter 19 — HTTP Error Semantics](../../../part-08-http-and-api/19-http-error-semantics/README.md)
- [Retry vs Fail Decision Guide](../05-reference/README.md)
