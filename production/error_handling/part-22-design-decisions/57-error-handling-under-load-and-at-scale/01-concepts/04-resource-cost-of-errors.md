# The Resource Cost of Errors, Validation Failures, and Degraded Mode

> Part XXII · Chapter 57 · Sections 57.6, 57.7, 57.8 · _Estimated reading time: 20 min_
> **Prerequisite:** [Chapter 34 — Security Principles for Error Handling](../../../part-13-security-aware/34-security-principles-for-error-handling/README.md)

## In one sentence

**Errors are not free exceptions to normal operation — they are a workload** with CPU, memory,
and bandwidth costs that must be budgeted, and the systems that fail *well* (degraded mode,
validation rejection) are exactly the ones that consume the most resources.

## Why this matters in production

Most capacity plans are written for the happy path: X requests/second, Y ms each, Z CPU. They
do not include the failure path, and the failure path is not cheap:

- **Stack capture** costs CPU proportional to stack depth. At 10,000 errors/second with a
  30-frame stack, you are paying for 300,000 frame captures per second.
- **Error objects** allocate. A wrapped error with a cause chain, a stack, and a context object
  is typically 2–5 KB of retained memory. At 10,000 errors/second held for 30 s in a retry
  buffer, that is 300 MB of garbage pressure.
- **Log volume** explodes. One error logged at 500 bytes across 20 fields is 10 KB per
  error; at 10,000 errors/second that is **100 MB/second** of log pipeline — which will
  backpressure into your application, because the logging agent competes for the same CPU
  and file descriptors.

The counter-intuitive case is worse: **degraded mode** (57.8) and **validation failures**
(57.7) are *successful* responses from the application's point of view, and therefore
typically **not sampled, not rate-limited, and not budgeted** — yet they are the most
resource-hungry responses in the system, because they do the most work.

## Core concept

### 57.6 — The cost of an error

| Cost | What it is | Typical magnitude | Scales with |
| ---- | ---------- | ----------------- | ------------ |
| **Stack capture** | Walking the call stack and formatting frames | 5–50 µs | Stack depth × error rate |
| **Allocation** | Error object, cause chain, context, sanitized copy | 0.5–5 KB per error | Error rate × retention |
| **Logging** | Serialization + write + compression + transport | 1–10 KB per error | Error rate × verbosity |
| **Retry attempts** | The whole call again | 100% of the operation cost | Attempts × error rate |
| **Held resources** | Connection, worker slot, memory for the duration | The timeout window | Concurrency × timeout |
| **Alert fatigue** | Human attention | The scarcest resource of all | Alert volume |

The **error path cost** is what makes an error storm a *capacity* event rather than an
availability one.

```text
  Cost of one failed request (5 s timeout, 3 attempts, 30-frame stack, 4 KB log line)

  CPU      3 × (call + 30-frame capture) + serialization   ≈ 0.8 ms
  Memory   3 KB retained × concurrency                      ≈ 30 KB at 10 concurrent
  Log      4 KB                                            ≈ 4 KB
  Downstream 3 attempts                                    ≈ 3 × the happy-path cost
```

At 500 errors/second, the downstream cost alone is **1,500 requests/second of extra load** —
on a system that was presumably sized for 500.

### The five responses to an error-rate spike

| Response | Effect on error-path cost | Effect on downstream load |
| -------- | ------------------------ | ------------------------- |
| **Sample the logs** | ↓↓ (log volume) | — |
| **Shorten the timeout** | ↓ (held resources) | — |
| **Reduce retry attempts** | ↓ | ↓↓ |
| **Open the circuit breaker** | ↓ | ↓↓↓ |
| **Shed load** | ↓↓ | ↓↓ (the request never happens) |

Note that the two cheapest responses (sampling, shorter timeout) are the ones teams skip,
because they "reduce observability" or "make failures faster". They should be your first
lever, not your last.

### 57.7 — High-volume validation failures

A validation failure is a *rejection*, and rejection is supposed to be cheap. But at volume it
is not:

```text
  1,000 rps of invalid requests
      → 1,000 × (schema validation + 422 body construction + error object + log line)
      → maybe 3 ms each = 3 CPU-seconds per second = 3 cores burned on rejecting bad input
      → plus 1,000 log lines/second = 4 MB/s of logs
```

Worse, validation failures often come from a **single misbehaving client** (a broken
integration, a bot, a stale SDK) sending the same invalid payload thousands of times.

Controls:

| Control | Effect |
| ------- | ------ |
| **Reject early** — validate before expensive work (auth, DB) | Avoids the downstream cost entirely |
| **Rate-limit invalid requests per client** | Stops the volume at the source |
| **Sample validation-failure logs** (they are usually identical) | Cuts log volume |
| **Aggregate** the field errors (≤ 20) | Reduces the response size |
| **Cache the "known-bad" fingerprint** | Reject a repeated payload without re-validating |
| **Return `422`, not `400`/`500`** | Clients can distinguish it from a server fault |

```ts
// ✅ Reject a repeated bad payload cheaply.
const fingerprint = sha256(canonicalJson(body));
if (knownBadPayloads.has(fingerprint)) {
  return reject422(knownBadPayloads.get(fingerprint));   // no re-validation, no re-parse
}
```

### 57.8 — Errors during degradation

Degraded mode is where error handling and capacity management collide. When a dependency is
down and the feature degrades, **every request takes the degraded path** — and the degraded
path is often the *expensive* one:

| Degradation strategy | Cost per request | Notes |
| -------------------- | ---------------- | ----- |
| Serve a cached value | Cheap (a cache read) | The cheapest good answer |
| Serve a stale value from the DB | Moderate (a DB read) | Must be labeled stale |
| Call a fallback service | **Expensive** (a remote call under stress) | Prefer only with its own budget |
| Compute locally | Expensive (CPU) | Only if the CPU headroom exists |
| Return an empty/minimal response | Cheap | Can be misleading |

The failure mode is a **degradation cascade**: the fallback is a *live* dependency, it is
also slow or down, and now every request makes two failing calls instead of one.

```text
  Normal:      request → primary (fast)         → response
  Degraded:    request → primary (timeout 2 s)   → fallback (timeout 2 s) → response
               └──────────── 4 s of latency, 2× the load ────────────┘
```

Rules that keep degraded mode affordable:

1. **Prefer local fallbacks** (cache, last-known value) over remote ones.
2. **Give every remote fallback its own timeout, breaker, and budget** — it is a dependency
   now, and it must be treated as one.
3. **Bound the degraded path's concurrency** — if 100% of traffic degrades, the fallback's
   capacity must handle 100% of traffic, not the occasional request.
4. **Mark every degraded response** so the load is visible and countable.
5. **Shed before you degrade** — if the system is saturated, rejecting is cheaper than
   degrading.

## How it works (mechanics)

### Error logging with sampling and tier-aware verbosity

```ts
export function logError(err: AppError, ctx: RequestContext): void {
  // T3/T4 errors are never sampled: they are the ones that matter.
  if (err.riskTier === "T3" || err.riskTier === "T4") {
    logger.error({ err: serialize(err), correlationId: ctx.correlationId }, err.code);
    return;
  }

  // Below a threshold, log everything.
  const rate = errorCounter.rate("all", 1_000);
  if (rate < 100) {
    logger.warn({ err: serialize(err), correlationId: ctx.correlationId }, err.code);
    return;
  }

  // Above it, sample, but keep a count so nothing is invisible.
  if (Math.random() < 0.1) {
    logger.warn({ err: serialize(err), correlationId: ctx.correlationId }, err.code);
  }
  metrics.increment("error.logged.sampled");
}
```

The counter keeps the *count* exact even when the *log* is sampled — so an alert on error
rate still fires.

### Cheap failure construction

Building an error object with a stack trace is expensive; building the *representation* for a
rejection does not need one.

```ts
// ❌ A 422 response allocates a full Error with a stack trace.
throw new ValidationError(issues);        // captured stack, never used

// ✅ The rejection path returns a value; no stack, no throw.
export type RequestOutcome<T> =
  | { ok: true; value: T }
  | { ok: false; rejection: { code: string; issues: FieldIssue[]; status: number } };
```

For a path that *must* throw (e.g. an unexpected bug), capture the stack once, at the
boundary, rather than at every layer.

### Budgeting the error path

```text
  error_path_cpu_budget = 0.05 × total_cpu

  ⇒ allowed_errors_per_second = error_path_cpu_budget / cpu_cost_per_error
  ⇒ with cpu_cost_per_error = 0.4 ms and 8 cores:
       0.05 × 8 = 0.4 cores → 0.4 s / 0.0004 s = 1,000 errors/second
```

At 1,000 errors/second the error path is at its ceiling. Above that, either the sampling
threshold must drop or the incident is already happening.

## Worked example — `Acme SaaS` log-storm incident

During a database incident, Acme's API produced ~12,000 errors/second. The symptoms were
confusing: the API was slow, the dashboards were slow, and the *successful* requests were
also slow — even though the database was failing anyway.

The root cause was not the database. It was the error path.

| Cost | Per second | Notes |
| ---- | ---------- | ----- |
| Stack capture (30 frames) | 12,000 × 40 µs | 0.48 cores |
| Error allocation + cause chain | 12,000 × 3 KB | 36 MB/s of garbage |
| Log serialization + write | 12,000 × 4 KB | **48 MB/s to the log pipeline** |
| Retry attempts (3×) | 36,000 DB queries/s | 3× the load on a struggling database |

The 48 MB/s of logs was the decisive number: the logging agent saturated the disk and the
CPU, which slowed *every* request, including the ones that did not touch the database. The
incident's blast radius was the whole service, not the database.

The fix:

1. **Sample above 100 errors/second** — but keep the exact count in a metric. Log volume
   dropped from 48 MB/s to ~5 MB/s.
2. **Cap the error context** — no stack traces for known `AppError`s (the class already
   carries the code); stack traces only for genuinely unexpected exceptions.
3. **Shorten the DB timeout** from 5 s to 1 s for read queries during saturation, reducing
   held connections by 5×.
4. **Open the breaker** on the failing dependency after 20 requests, cutting downstream
   attempts to zero.
5. **Reduce retry attempts to 1** while the breaker is open.

Outcome: the same database incident now produced ~2,000 errors/second of log volume
(5 MB/s), the API's p99 for unaffected endpoints rose only 12%, and the incident was
contained to the database-dependent endpoints.

The generalizable lesson: **during an incident, the error path competes with the request
path for the same resources.** If you do not bound the error path, the error path becomes
the outage.

## Key data / numbers

| Item | Value | Notes |
| ---- | ----- | ----- |
| Stack capture cost | 5–50 µs | Proportional to stack depth (typical 20–40 frames) |
| Error object size | 0.5–5 KB | With cause chain and context |
| Log line size | 1–10 KB | Structured logs are large; trim the payload |
| Error-path CPU ceiling | 5% of total CPU | Above this, sample |
| Log sampling threshold | 100 errors/second per service | Keep 100% of T3/T4 |
| Log sampling ratio above the threshold | 10% (1 in 10) | Keep the counter exact |
| Max log throughput | 5 MB/s per service | Beyond this, the agent becomes a bottleneck |
| Max validation issues per response | 20 | Cap the array |
| Validation rejection cost target | < 1 ms | Validate before auth/DB |
| Error rate that triggers a shedding decision | > 20% over 1 min | Or pool > 90% |
| Error budget burn rate that freezes deploys | 14.4× over 1 h **and** 6× over 6 h | Multi-window burn-rate alert |
| Degraded-path timeout | ≤ 500 ms for local fallbacks | A degraded answer must arrive quickly |
| Fallback concurrency | Same as the primary it replaces | It now serves 100% of traffic |

## Real-world use case — `Checkout` (Acme SaaS) validation flood

A partner integration of a large tenant began sending malformed `Checkout` requests: 400
rps, each with `amountMinor` as a string. Acme's validation rejected every one with a `422`,
correctly — but at 400 rps the rejections were:

- building 400 error objects with stack traces per second,
- writing 400 log lines per second with the full request body attached (including a PII
  risk — the body contained the customer's email),
- and **counting as a 4xx**, which meant Acme's dashboards showed "no errors" while the
  endpoint was burning 2 cores.

Two problems: a resource problem (400 rejections/second) and a **security problem** (the
request body, including PII, was attached to the log line).

The fixes:

| Problem | Fix |
| ------- | --- |
| PII in logs | The validation rejection carries only the *field names* that failed, never the values |
| Cost of rejection | Validation failures return a value; no `Error` object, no stack |
| Volume | Rate-limited per API key: 20 invalid requests/second, then `429` + `Retry-After: 60` |
| Log volume | Invalid-request logs sampled at 1%, with an exact counter |
| Repeat offender | A fingerprint of the invalid payload was cached for 60 s, so repeats were rejected without re-validating |

Result: the partner's flood cost Acme ~0.05 cores instead of 2, no PII reached the logs, and
the partner received a clear `429` with `Retry-After: 60` instead of 400 `422`s per second.
The partner fixed their SDK the same day, because the response told them exactly which field
was wrong.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Log every error | Complete visibility | Log-storm and CPU cost | Below 100 errors/s |
| Sample errors above a threshold | Bounded cost | Some detail missing (the count is kept) | **Default above 100 errors/s** |
| Capture stacks always | Best diagnostics | 5–50 µs and allocation per error | Unexpected errors only |
| Reject invalid input late | Catches more errors | Wastes downstream work | Never for validation |
| Local fallback (cache) | Cheap, fast | May be stale | **Default for degradation** |
| Remote fallback service | Fresher data | Doubles the failure surface | Only with its own budget/breaker |
| Throttle invalid requests | Stops the flood | A legitimate client can be throttled | Per API key, with `Retry-After` |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Budget the error path as a real workload | Assume errors are free |
| Sample logs above 100 errors/s but keep exact counts | Log every error at 12,000/s |
| Capture stack traces only for unexpected errors | Capture a stack for every rejection |
| Validate before auth and database work | Validate after the expensive work |
| Rate-limit invalid requests per client | Let one client consume the error budget |
| Use local fallbacks under degradation | Chain live fallbacks under stress |
| Mark degraded responses and count them | Serve wrong data silently |
| Never log request bodies on validation failures | Attach PII-bearing payloads to log lines |

## Common mistakes

- **Logging the full request body on validation failure.** It is the easiest PII leak in a
  SaaS product, and it happens exactly when volume is high.
- **Sampling without a counter.** Sampled logs look like the error rate dropped. Keep the
  count exact.
- **Throwing for rejections.** A `422` does not need a stack trace.
- **Remote fallbacks without budgets.** The fallback doubles the failure surface.
- **Ignoring the error path in capacity planning.** The plan says 4,000 rps; the error path
  adds 3,000 rps of downstream load during the incident you planned for.
- **Treating degraded mode as free.** It serves 100% of traffic through the *expensive* path.

## Checklist

- [ ] The error path has a CPU budget (≤ 5% of total) and a log-throughput budget (≤ 5 MB/s).
- [ ] Logs are sampled above 100 errors/second, with exact counters preserved.
- [ ] Stack traces are captured only for unexpected errors.
- [ ] Validation rejections carry field names only — never values.
- [ ] Invalid-request volume is rate-limited per client with `Retry-After`.
- [ ] Validation runs before auth and database work.
- [ ] Degraded-mode fallbacks are local, or have their own timeout/breaker/budget.
- [ ] Degraded responses are marked and counted.
- [ ] The alert set includes an error-budget burn-rate alert (14.4×/1 h and 6×/6 h).

## Related

- [Failure Amplification and Error Storms](./01-failure-amplification-and-error-storms.md)
- [The Resource Cost Model](../02-deep-dive/03-resource-cost-model.md)
- [Chapter 34 — Security Principles for Error Handling](../../../part-13-security-aware/34-security-principles-for-error-handling/README.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)
