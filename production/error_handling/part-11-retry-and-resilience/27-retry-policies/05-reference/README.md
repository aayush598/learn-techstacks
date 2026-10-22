# Chapter 27 — Reference

> Part XI · Chapter 27 · Retry decision guide, eligibility tables, policy defaults, and glossary.

## Cheat sheet — the retry contract

```text
RetryPolicy {
  maxAttempts        3        includes the first try
  deadline           absolute epoch ms derived from the caller
  perAttemptTimeout  min(config, deadline - now)
  baseDelay          200ms
  multiplier         2
  capDelay           10s
  jitter             full       sleep = random(0, min(cap, base × 2^n))
  budget             10-20% per dependency
  retryAfterMs       server hint, overrides computed delay
}
```

## Decision tree — retry or fail?

```text
An operation failed.
│
├─ Is the error classified retryable?
│   ├─ No → FAIL (or compensate / degrade)
│   └─ Yes → continue
│
├─ Is the operation safe to repeat (idempotent or keyed)?
│   ├─ No → RECONCILE first; do not retry blind
│   └─ Yes → continue
│
├─ Is this layer the designated retry owner?
│   ├─ No → PROPAGATE the classified error
│   └─ Yes → continue
│
├─ Are attempts left? ── No → FAIL with RetryExhaustedError
│
├─ Does the next delay + timeout fit the deadline? ── No → FAIL now
│
├─ Does the retry budget allow another attempt? ── No → FAIL now
│
└─ RETRY with backoff + jitter (same idempotency key)
```

## Decision table — retryable by error source

| Source | Retryable | Conditional | Terminal |
| ------ | --------- | ----------- | -------- |
| HTTP | `408`, `429`, `502`, `503`, `504` | `500` (provider) | `400`, `401`, `403`, `404`, `405`, `413`, `415`, `422` |
| Postgres | `40001`, `40P01`, `08xxx`, `53300` | `57014` (timeout only) | `23xxx`, `42xxx` |
| Network | `ECONNRESET`, `ECONNREFUSED`, `ETIMEDOUT` | — | TLS errors, `ENOENT`, `EACCES` |
| Provider | `429`, `5xx`, rate limits | `409` after refresh | `400`, `401`, `403`, `422`, business declines |
| Cancellation | — | — | Caller cancel / deadline exceeded |

## Defaults by context

| Context | Attempts | Base | Cap | Deadline |
| ------- | -------- | ---- | --- | -------- |
| User-facing API | 2–3 | 200–300ms | 2–5s | 5–10s |
| Internal RPC | 3 | 100–300ms | 5s | 2–5s |
| Provider call | 3 | 250–500ms | 3–10s | 5–15s |
| DB transaction | 2–3 | 10–50ms | 0.5–1s | Request budget |
| Background job | 3–5 | 30s | 10m | Job SLA |
| Rate-limited call | 3 | `Retry-After` | `Retry-After` | Caller budget |

## Backoff formulas

```text
raw(n)        = min(cap, base × multiplier^n)
full jitter   = random(0, raw(n))
equal jitter  = raw(n)/2 + random(0, raw(n)/2)
capped sum    = Σ raw(i) for i = 0..k-1
deadline ok   = now + delay + timeout < deadline
```

## Status and code quick reference

| Signal | Meaning | Action |
| ------ | ------- | ------ |
| `429` + `Retry-After` | Rate limited | Wait the hint, retry |
| `503` + `Retry-After` | Temporarily unavailable | Wait the hint, retry |
| `504` | Upstream timeout | Backoff + jitter, retry |
| `409` | Conflict | Refresh state, then maybe retry |
| `422` | Semantic validation | Do not retry |
| `40001` / `40P01` | Serialization/deadlock | Roll back, retry |
| `53300` | Too many connections | Backoff, do not open more |
| `42P01` | Undefined table | Do not retry; alert |

## Retry owner assignment

| Call | Owner | Others |
| ---- | ----- | ------ |
| Stripe charge | Payment service (holds key) | SDK/client retries off |
| Postgres transaction | Repository/service boundary | Driver retries off |
| Internal HTTP RPC | Caller service | Gateway retries off for writes |
| Job step | Worker | Inner client retries off |
| Browser fetch | UI (user-initiated only) | — |

## Exhaustion contract

```text
RetryExhaustedError {
  attempts      number of tries made
  elapsedMs     total wall-clock time
  lastError     the final classified error (cause)
  retryable     whether another attempt could ever help
  outcome       "failed" | "unknown" | "partial"
}
```

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Retryable | Transient error expected to succeed later |
| Conditional | Safe to retry only if idempotent/keyed/refreshed |
| Terminal | Will fail identically; do not retry |
| Attempt | One execution, including the first |
| Backoff | Increasing delay between attempts |
| Jitter | Randomness added to delay to spread retries |
| Retry budget | Cap on retries relative to successes |
| Deadline | Absolute time by which the operation must finish |
| Amplification | Product of attempts across nested layers |
| Retry owner | The one layer allowed to retry a dependency |
| `Retry-After` | Server hint (seconds or HTTP-date) for when to retry |
| Ambiguous outcome | The caller cannot tell whether the operation succeeded |

## Signposts

- Error classification → [Ch. 4](../../../part-02-error-taxonomy/04-designing-a-comprehensive-error-taxonomy/README.md)
- HTTP semantics (`429`, `503`) → [Ch. 19](../../../part-08-http-and-api/19-http-error-semantics/README.md)
- Idempotency → [Ch. 28](../../28-idempotency-and-duplicate-operation-safety/README.md)
- Breakers and deadlines → [Ch. 29](../../29-timeouts-circuit-breakers-and-bulkheads/README.md)
- Final retry-vs-fail guide → [Ch. 62](../../../part-24-repeatable-blueprint/62-final-reference-materials/README.md)

## Related

- [Chapter 27 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Reusable Retry Utility with Jitter](../03-practical-examples/01-reusable-retry-utility-with-jitter.md)
- [Backoff and Jitter Math](../02-deep-dive/01-backoff-and-jitter-math.md)
- [Chapter 28 — Idempotency and Duplicate-Operation Safety](../../28-idempotency-and-duplicate-operation-safety/README.md)
