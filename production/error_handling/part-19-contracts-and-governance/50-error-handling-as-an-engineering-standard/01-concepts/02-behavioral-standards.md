# Behavioral Standards: Propagation, Retry, Response, Recovery

> Part XIX · Chapter 50 · Sections 50.4–50.7 · _Estimated reading time: 20 min_
> **Prerequisite:** [What an Error-Handling Standard Contains](./01-what-a-standard-contains.md)

## In one sentence

The behavioural half of a standard fixes **four decisions**: where an error stops travelling
(propagation), when trying again is allowed (retry), what the outside world sees (response),
and what the system does instead of failing (recovery).

## Why this matters in production

Naming rules are visible; behavioural rules are where systems actually differ. Two teams can
follow the identical code standard and still behave completely differently under failure:

- One team's service swallows a `NotFound` and returns an empty list; the other propagates it.
  The first looks resilient and silently loses data.
- One team retries every `5xx` three times; another retries nothing. Under a provider outage,
  the first team's traffic triples and takes down the provider's other customers.
- One team returns a raw exception message to the client; the other returns a problem document.
  The first leaks a table name.
- One team's background job retries forever on a poison payload; another gives up after three
  attempts. The first burns money on a job that can never succeed.

These are all standardisable, and all of them are invisible in code review unless someone asks.

## 50.4 — Propagation conventions

The standard's propagation rules answer: **where does an error stop travelling, and who
changes its shape?**

```text
R-PROP-1  An error is either handled or propagated. It is never neither.
R-PROP-2  Swallowing is forbidden: catching and continuing without changing behaviour is
          a bug, not a recovery.
R-PROP-3  Errors are translated exactly once, at a boundary. The boundary converts an
          internal error into the surface's contract shape.
R-PROP-4  Translation preserves the cause and the correlation id.
R-PROP-5  The domain layer never sees transport types; the transport layer never sees
          domain internals.
R-PROP-6  A catch block must state which error kinds it handles and what it does with
          them. A catch-all must rethrow or convert to a generic internal error.
```

R-PROP-2 deserves emphasis, because "swallowing" is rarely intentional. It usually arrives as:

```ts
try {
  await syncBillingCache();
} catch (e) {
  log.warn("cache sync failed");   // swallowed: the caller believes it succeeded
}
```

The standard's requirement is not "never catch" — it is **"a catch must change the
program's outcome"**: rethrow, translate, degrade, compensate, or record-and-escalate. A catch
that only logs and continues is prohibited because the caller cannot distinguish success from
failure.

### The layer responsibility table

A standard should publish this table, because "where do I translate?" is asked in every review:

| Layer | Owns | Never does |
| ----- | ---- | ---------- |
| Domain | Raising errors; invariants; no transport types | Throwing HTTP exceptions |
| Application / service | Orchestration; transaction boundaries; compensation | Returning raw provider errors |
| Infrastructure / adapter | Translating provider/DB errors into domain errors | Deciding user-facing behaviour |
| Transport | Mapping domain errors to the wire contract | Inventing new error meanings |
| Boundary (handler) | Serializing; logging; correlation id; final safety net | Recovering business logic |

## 50.5 — Retry and timeout conventions

Retries are the most dangerous convention to leave open, because a wrong retry policy converts
a small outage into a large one.

```text
R-RETRY-1  Retrying is permitted only for errors explicitly marked retryable.
R-RETRY-2  Retrying is permitted only for idempotent operations. A non-idempotent operation
           requires an idempotency key before it may be retried.
R-RETRY-3  Every retry policy declares: max attempts · base delay · backoff · jitter ·
           total deadline · and which errors qualify.
R-RETRY-4  Retries are owned by exactly one layer. Nested retry policies are forbidden.
R-RETRY-5  Every outbound call has a timeout. Every operation has a deadline that is
           propagated to its callees.
R-RETRY-6  A retry budget exists per dependency: retries may not exceed a small
           percentage of total requests to that dependency.
```

R-RETRY-4 is the one most often violated. Three layers — service, HTTP client, SDK — each
with their own retry policy multiply: 3 × 3 × 3 = 27 attempts. The standard fixes one owner:

```text
WHO OWNS THE RETRY?
  application service  → owns retries for business operations (idempotency-aware)
  infrastructure client → owns retries for single transport calls (connect/read only)
  the SDK/provider     → owns its own internal retries, which you MUST account for
```

R-RETRY-5's two halves are different problems. A **timeout** bounds a single call; a
**deadline** bounds the whole operation and shrinks as it descends:

```text
client request deadline: 30s
  ├─ db query          deadline: 3s
  ├─ billing provider  deadline: 10s   (remaining: 27s, capped at 10s)
  └─ export job enqueue deadline: 2s
```

### A recommended default policy table

```text
DEPENDENCY CLASS          TIMEOUT   MAX ATTEMPTS   BACKOFF            RETRYABLE
same-region database       3s       3              100ms + jitter     deadlock/serialization only
read replica               2s       2              100ms + jitter     connection errors
external HTTP provider    10s       3              1s + jitter        5xx, 429, timeouts
queue / broker             5s       5              1s + jitter        connection errors
LLM provider              60s       2              5s + jitter        rate limit, 5xx
```

These are **recommendations with a stated origin** — they are defaults to start from, not laws.
A standard should say so; pretending a timeout of 3 s is universally correct is the kind of
rigidity Chapter 50 §50.12 warns against.

## 50.6 — Response format conventions

If the standard fixes only one thing about responses, it should be the shape.

```text
R-RESP-1  Error responses use the media type application/problem+json (RFC 9457).
R-RESP-2  The body contains at least: type · title · status · detail · code · requestId.
R-RESP-3  `code` is the machine-readable identifier; it is the only field clients branch on.
R-RESP-4  `detail` is human-readable prose and may change without notice.
R-RESP-5  The HTTP status matches the code's registered mapping. Handlers do not
          override the status per call site.
R-RESP-6  Public responses never contain stack traces, SQL, internal hostnames, or
          credentials. (See §50.8.)
R-RESP-7  Validation failures list field-level details in `errors[]`, each with a field
          path and a stable sub-code.
R-RESP-8  The response carries the error contract version.
```

R-RESP-5 is the subtle one. When a handler chooses a status, you get `402` in one place and
`409` in another for the same condition, and every client has to cope with both. The
registered mapping is the single source of truth; a call site that needs a different status
needs a different code.

## 50.7 — Recovery conventions

Recovery is what the system does *instead of* failing, and it has to be chosen deliberately:

```text
R-RECOV-1  Every fallback states its trigger, its scope (what degrades), and its
           observability (how you know it is active).
R-RECOV-2  A fallback never masks a permanent failure: it must not convert "this will
           never work" into a retry loop.
R-RECOV-3  Degraded mode is observable: it emits a signal and appears in the response
           when it affects the user.
R-RECOV-4  Security-critical paths fail closed by default; availability-critical paths
           may fail open only with a recorded decision.
R-RECOV-5  Multi-step operations define compensation for every irreversible step.
R-RECOV-6  A recovery path is itself bounded: it has a deadline and a maximum number of
           attempts, so a fallback cannot loop forever.
```

R-RECOV-4 is where an organisation's standard earns its keep, because "fail open or closed"
is a **security decision** that must be consistent across teams, and it is exactly the kind of
decision that gets made ad hoc by whoever is on call.

### The recovery decision table

| Situation | Standard default |
| --------- | ---------------- |
| Optional dependency down (recommendations, avatar) | Degrade; empty result; observable |
| Payment provider down at checkout | Fail closed; `503` + `retry` action |
| Analytics sink down | Degrade silently (drop samples), never fail the request |
| Cache down | Fail open to the database; observable; reduced latency |
| Auth provider down | Fail closed; `503`; never fail open on authorisation |
| Export worker queue saturated | Reject with `429`/`503` + `Retry-After`; never queue unbounded |
| LLM provider down (summary feature) | Degrade the card, not the page |
| Third-party webhook delivery fails | Retry with backoff, then dead-letter; never 500 to the sender |

## Worked example — one dependency, four recovery postures

Acme's `AgentRun` calls an LLM provider. The standard's recovery table was applied to decide
what happens when the provider is down, and the answers differ by call site:

```text
Call site                Fallback                      Why
──────────────────────────────────────────────────────────────────────────────────
Dashboard summary card   cached summary + "stale" badge  optional, degraded UI is fine
Chat first token         fail with 503, client retries   the user is waiting on it
Background summarisation skip this batch, record it      nobody is waiting; cost is a delay
Billing plan lookup      cached plan, max 5 min stale    a stale plan beats no plan
```

Each line cites the standard's rules (R-RECOV-1, -2, -3) rather than restating them, and the
**deviation is documented in the rule's exception register** — the billing lookup is the one
place Acme allows fail-open, because it has a recorded security decision.

## Key data / numbers

- **Propagation:** 5 layers with a fixed responsibility table; translation happens exactly
  once, at a boundary.
- **Retry:** max attempts 2–5 by dependency class; backoff with **jitter**; **one** retry owner
  per call path; a retry budget of roughly **10%** of total requests to a dependency.
- **Timeouts (recommended defaults):** database 3 s · replica 2 s · external HTTP 10 s ·
  queue 5 s · LLM 60 s. **Start here, then measure.**
- **Response fields (required):** `type` · `title` · `status` · `detail` · `code` ·
  `requestId` — plus the contract version header.
- **Recovery:** every fallback states trigger, scope, and observability; degraded mode must be
  observable; recovery paths are bounded.
- **Fail-closed default:** authentication, authorisation, and payment paths.

## Real-world use case — ExportJob

Acme's `ExportJob` worker had no standard for retries, so each job type grew its own policy.
The export job retried provider errors **forever** (a background job has no user waiting, so
"retry until it works" seemed free); the invoice job retried nothing (someone had been paged
once and told to stop).

Both were wrong in the same direction: **neither distinguished retryable from permanent**.
A malformed column mapping (`EXPORT_COLUMN_MAPPING_INVALID`, permanent) was retried 200 times
over two days, each attempt re-reading 500 000 rows from Postgres. One poison export consumed
about 6% of the worker's database capacity for a day.

Acme's standard fixed it with four lines:

```text
R-RETRY-1  retry only codes marked retryable
R-RETRY-2  retry only idempotent operations
R-RETRY-3  every policy declares max attempts, backoff, and a total deadline
R-RETRY-4  exactly one layer owns the retry
```

The export job's policy became `maxAttempts 5 · base 30s · exponential with jitter · total
deadline 15 min · retryable: {EXPORT_STORAGE_UNAVAILABLE, EXPORT_QUEUE_TIMEOUT}`. The poison
job failed in 90 seconds, went to the dead-letter queue, and surfaced in the support dashboard
with a code — instead of quietly consuming a tenth of the database for two days.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One org-wide policy with defaults | Consistent; fast to adopt | Defaults are wrong for edge dependencies | Most dependencies |
| Per-dependency policies | Accurate | Many decisions; drift | Critical dependencies only |
| No policy (per team) | Local fit | Inconsistent; outage amplification | Never |
| Standard says "declare a policy", not which one | Flexible; still checkable | Requires discipline | Mature organisations |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| State which layer owns each decision | Leave "who retries?" implicit |
| Require a total deadline, not just per-attempt timeouts | Rely on per-attempt timeouts alone |
| Reject retries of permanent codes | Retry everything that fails |
| Derive the HTTP status from the registry | Choose the status at the call site |
| Bound every recovery path | Let a fallback loop indefinitely |
| Fail closed on auth, authz, and payments | Fail open on security checks |
| Make degraded mode observable | Degrade silently and invisibly |

## Common mistakes

- **The catch-and-log-only.** The caller cannot tell success from failure.
- **The nested retry.** 3 × 3 × 3 attempts against a struggling provider.
- **The endless job retry.** A poison payload burns capacity for days.
- **The hand-picked status.** One condition, three statuses across three modules.
- **The silent degradation.** Nobody knows the feature has been broken for a week.
- **The open authorization gate.** Availability pressure turned into a security hole.

## Checklist

- [ ] Every catch block changes the outcome (rethrow, translate, degrade, compensate).
- [ ] Translation happens exactly once, at a boundary, and preserves the cause.
- [ ] Every retry policy declares attempts, backoff, jitter, deadline, and eligible codes.
- [ ] Exactly one layer owns retries for a given call path.
- [ ] Every outbound call has a timeout; every operation has a propagated deadline.
- [ ] HTTP statuses come from the registry, never from the call site.
- [ ] Every fallback states trigger, scope, and observability.
- [ ] Auth, authz, and payment paths fail closed.

## Related

- [What an Error-Handling Standard Contains](./01-what-a-standard-contains.md)
- [Security Requirements and Exceptions to the Standard](./03-security-and-exceptions.md)
- [Durable Rules, Exceptions, and Change Management](../02-deep-dive/01-durable-vs-ceremonial-rules.md)
- [Chapter 27 — Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)
