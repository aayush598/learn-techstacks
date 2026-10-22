# Contracts, Fallback, Recursion, Transformation, and Predictability (51.10–51.12, 51.17–51.18)

> Part XX · Chapter 51 · Sections 51.10–51.12, 51.17–51.18 · _Estimated reading time: 26 min_
> **Prerequisite:** [Chapter 16 — Error Translation and Normalization](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md), [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)

## In one sentence

Five properties govern what the outside world sees and how the system behaves when the world
misbehaves: **contracts are honoured, unknown failures fail safe, recursion is bounded,
translation is lossless, and behaviour under dependency failure is predictable.**

## Why this matters in production

- **Contract violations** (51.10) break clients. A `200` with `{"success": false}` teaches the
  frontend to check the body instead of the status — then a *real* `500` slips through. One
  inconsistent error shape undoes months of SDK work.
- **Unsafe fallbacks** (51.11) hide outages. If an unknown exception maps to an empty list, the
  dashboard shows "no data" instead of "broken", and nobody is paged for three days.
- **Unbounded recursion** (51.12) appears in places you would not think to look: a fallback chain
  that falls back to the thing that failed, a token refresh that re-triggers the call that returned
  401, a translator that translates its own output.
- **Lossy translation** (51.17) turns a precise vendor code into "upstream error", destroying the
  information the whole system depends on.
- **Unpredictable behaviour** (51.18) means the same outage produces a 2-second 503 for some
  customers and a 30-second hang for others, depending on when their request arrived.

## Core concept

### 51.10 — Responses follow contracts

Every error that crosses a boundary must satisfy the **declared contract of that boundary**:

| Boundary | Contract requirements |
| -------- | --------------------- |
| HTTP | Registered error code, correct status code, documented body shape, `Content-Type: application/problem+json` for RFC 9457 shapes |
| Queue / job | Registered failure code, terminal state, attempt count, dead-letter eligibility |
| Internal module | A stable error type or a closed union member |
| Third-party webhook | Vendor-correct status and semantics (e.g. `2xx` only for "handled", `4xx` for "will never work", `5xx` for "try later") |

The test: **validate the emitted error against the schema**, on every path, in a test. A schema
that is never validated is a wish.

### 51.11 — Safe fallback for unknown

The `default` branch of every classifier and every policy table needs a defined, safe behaviour.
"Safe" depends on what the failure protects:

```text
   UNKNOWN ERROR
        │
        ├── authentication / authorization  → FAIL CLOSED (deny, 401/403)
        ├── payments / money movement       → FAIL CLOSED (do not guess)
        ├── write of user-visible data      → FAIL CLOSED (do not half-write)
        ├── read of optional, non-critical  → FAIL OPEN (degraded: cached/stale/empty, flagged)
        └── everything else                 → 500 + generic code + correlation ID + alert
```

Three absolute prohibitions for the unknown branch:

1. **Never map unknown → success** (no `200`, no `null` presented as "no data").
2. **Never map unknown → retryable by default.** You do not know if the effect happened.
3. **Never map unknown → an empty result that looks like a valid empty.** "The list is empty" and
   "the list could not be loaded" must be different states in the response.

### 51.12 — No unbounded recursion

Error handling recurses in five common shapes:

| Shape | Example | Bound |
| ----- | ------- | ----- |
| Retry recursion | `withRetry(withRetry(withRetry(x)))` | One owner; attempts ≤ 5 |
| Fallback chain | primary → cache → default → primary | Chain depth ≤ 3, acyclic |
| Translation recursion | `translate()` produces an error that `translate()` maps again | Depth ≤ 5, cycle-detected |
| Auth refresh recursion | 401 → refresh → retry → 401 → refresh | One refresh per operation, then surface |
| Cause chain recursion | error A wraps error B wraps error A | Cause depth ≤ 10, cycle-detected |

```ts
// ✅ Bounded fallback chain: explicit, finite, acyclic.
const FALLBACKS: ReadonlyArray<(ctx: Ctx) => Promise<Response>> = [
  tryPrimary,   // 1
  tryCache,     // 2
  tryStale,     // 3 — last resort, always flagged as stale
];             // no more than 3, and nothing points back to tryPrimary
```

### 51.17 — Transformations preserve metadata

A **transformation** converts an error from one representation into another. It must be **lossless
with respect to a defined field set**. That set is the contract between layers:

| Field | Must survive? | Consequence if lost |
| ----- | ------------- | -------------------- |
| `code` | Yes | Routing, alerting, and client behaviour break |
| `category` | Yes | Retry decisions become guesswork |
| `retryable` | Yes | Retries either never happen or happen wrongly |
| `cause` | Yes | Root cause is unreachable (51.4) |
| `correlationId` | Yes | The trace is broken across the boundary |
| `dependency` / `vendorCode` / `vendorRequestId` | Yes | Provider support tickets become untraceable |
| `retryAfter` / `httpStatus` | Yes when present | Rate limits become 500s |
| `attempt` | Yes | Retry storms hide inside a single call |
| Internal detail (stack, SQL, PII) | No — must be **dropped** | Security leak (51.5) |

Note the asymmetry: **preservation is mandatory for metadata; removal is mandatory for sensitive
detail.** A transformation that keeps everything is as wrong as one that keeps nothing.

### 51.18 — Predictable during dependency failures

Predictability means: **given the dependency's state, the behaviour is the same every time.** Not
"the first request behaves differently from the rest". Not "it depends on which pod you hit".

The mechanism is an explicit **dependency policy** plus **deadline propagation**:

```yaml
# One policy per dependency. Behaviour under failure is written down, not emergent.
dependencies:
  stripe:
    criticality: critical
    connect_timeout_ms: 1000
    request_timeout_ms: 8000
    max_attempts: 3
    breaker:
      error_rate_threshold: 0.5      # 50% errors
      window_requests: 20
      half_open_probes: 5
    fallback: fail_closed             # never guess a payment outcome
    degrade: disable_subscription_upgrade_ui
  redis:
    criticality: optional
    connect_timeout_ms: 200
    request_timeout_ms: 500
    max_attempts: 1
    fallback: fail_open_to_postgres   # reads bypass the cache
    degrade: stale_cache_reads
```

With that policy, "Stripe is down" produces the same outcome for every customer: a fast 503 with
`PAYMENT_PROVIDER_UNAVAILABLE` inside ~2 s (breaker open) or a bounded ~8 s retry sequence
(breaker closed, first requests) — never a 30 s hang.

## Worked example — `AgentRun` (Acme SaaS)

`AgentRun` is an LLM tool-calling agent. Its tool `sendEmail` is a side effect; the LLM provider
is a dependency; token limits are a quota error.

```ts
// BEFORE — violates 51.10, 51.11, 51.17 and 51.18 at once.
try {
  const result = await agent.run(input);
  return res.json({ ok: true, result });
} catch (err) {
  return res.json({ ok: false, error: err.message });   // 200 + ad-hoc shape (51.10)
  // unknown error → "error" field only; client cannot tell provider from tool (51.11)
  // vendor error code and provider request id dropped (51.17)
  // provider timeout surfaced after the full client timeout (51.18)
}
```

After:

```ts
try {
  const result = await agent.run(input, { deadline: ctx.remaining });
  return res.json({ ok: true, result });
} catch (err) {
  const appErr = toAppError(err, { operation: "agentRun", correlationId: ctx.correlationId });
  // 51.17: provider code, provider request id, tool name survive translation
  // 51.10: the body matches the published error contract, status matches the code
  // 51.11: unknown → 500 + generic code; provider rate limit → 429 + Retry-After
  // 51.18: the provider call had a 8 s timeout and a breaker; failure is fast and uniform
  throw appErr;   // the global handler owns the response shape (51.10)
}
```

The tool-call case is where 51.9 and 51.16 meet: if the provider times out **after** the agent
already called `sendEmail`, retrying the whole run risks a second email. The recovery precondition
is "the tool has no recorded side effect for this run"; otherwise the run is marked `unknown` and
reconciled, not retried.

## Key data / numbers

- **Public error body: 4–6 fields**; anything more is a contract you have to version.
- **RFC 9457** `application/problem+json` — the standard shape for HTTP error bodies.
- **Fallback chain depth: ≤ 3.** Depth 2 is usually enough; 3 is the last honest try.
- **Translation depth: ≤ 5**, cause chain depth: **≤ 10** (both with cycle detection).
- **Token refresh: exactly once per operation.** A second 401 after a refresh is surfaced, not
  retried.
- **Dependency timeouts**: connect **200 ms–1 s**, request **1–10 s** — always a fraction of the
  caller's deadline.
- **Circuit breaker**: open at **≥ 50% errors over 20 requests**, **5** half-open probes.
- **HTTP status for unknown errors: 500**, never 200, never 204.
- **Rate-limit passthrough**: vendor `429` keeps its `Retry-After` header (seconds or HTTP-date).

## Real-world use case — Acme SaaS `WebhookIngest`

Stripe's webhook endpoint began returning `500` for a payload shape Acme did not recognise. The
global handler caught it and returned `200 {"ok": false}` — because the body had to satisfy an
old client contract.

Consequences, all traceable to properties:

- **51.10 violated**: clients could no longer distinguish "handled" from "failed" and started
  retrying internally, tripling webhook volume.
- **51.11 violated**: an *unknown* payload type produced `ok: false` inside a `200`, so the
  webhook pipeline looked healthy. Acme's "webhook success rate" metric read 99.9% while 4% of
  events were being dropped.
- **51.17 violated**: the Stripe error code was replaced by a generic string, so no one could search
  Stripe's logs for the affected event IDs.
- **51.18 violated**: the retry to fetch the event from Stripe's API had no breaker, so a Stripe
  incident produced a self-inflicted load amplifier.

The fix was a small registry change plus a policy: unknown event types are **acknowledged and
recorded** (`2xx` + `UNKNOWN_EVENT_TYPE` recorded for later processing, because Stripe retries
non-2xx for up to **3 days**), genuine failures return `5xx`, and the Stripe API client got a
breaker with a **20-request / 50%** threshold. The "silent drop" metric went from 4% to 0 because
unknown events are now *counted*, not swallowed.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Always fail closed on unknown | Safe by default | Availability loss on benign failures | Money, auth, writes |
| Always fail open | Never blocks users | Hides real failures | Optional, non-critical reads only |
| Per-category fallback policy | Explicit, reviewable | Needs a complete category list | Mature systems with a registry |
| Global single fallback | Simple | One-size-fits-none | Small services with one dependency |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Validate emitted error bodies against a schema | Trust that every handler formats alike |
| Have an explicit, reviewed default policy | Let the `default` branch return `200` |
| Distinguish "empty" from "could not load" | Map unknown to an empty list |
| Bound fallback and translation depth explicitly | Let fallback A fall back to B which falls back to A |
| Preserve code, cause, retryability, context in translation | Wrap with a generic "upstream error" |
| Give every dependency a written failure policy | Let timeout behaviour emerge from library defaults |

## Common mistakes

- **The `ok: false` envelope.** A `200` with a boolean inside teaches every client to ignore the
  status code. Reserve `2xx` for success.
- **A fallback that returns the primary's default value.** A fallback for a failed cache read
  should return *stale or missing*, not a plausible-looking zero.
- **Generic translations at the HTTP layer.** `catch { throw new Error("Internal Server Error") }`
  at the boundary destroys the entire internal error model.
- **Retrying an unknown failure.** If you cannot classify it, you do not know whether the effect
  happened. Resolve by read-back; do not guess.
- **No breaker on a dependency that is not in the request path.** The worst retries happen in the
  background while the user request already timed out.

## Checklist

- [ ] Every error response is validated against a schema in a test.
- [ ] The default branch of the classifier has a reviewed, safe policy.
- [ ] Unknown never maps to success, to retry, or to a valid-looking empty result.
- [ ] Fallback chains are finite, acyclic, and depth-limited.
- [ ] Translation preserves code, category, retryability, cause, correlation ID, vendor context.
- [ ] Every dependency has a written policy: timeouts, attempts, breaker, fallback, degraded mode.
- [ ] Behaviour during a dependency outage is uniform across instances and customers.

## Related

- [Determinism and Completeness (51.1–51.4)](./01-determinism-and-completeness.md)
- [Concurrency, Cancellation, and Partial Failures (51.13–51.16)](./04-concurrency-cancellation-and-partial-properties.md)
- [Chapter 20 — Standardized API Error Responses](../../../part-08-http-and-api/20-standardized-api-error-responses/README.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)
- [Chapter 44 — AI, LLM, and Tool-Calling Application Errors](../../../part-16-specialized-saas-scenarios/44-ai-llm-and-tool-calling-application-errors/README.md)
