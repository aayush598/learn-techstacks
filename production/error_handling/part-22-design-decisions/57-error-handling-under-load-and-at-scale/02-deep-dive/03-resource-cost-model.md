# The Resource Cost Model: What One Error Costs and How to Budget for It

> Part XXII · Chapter 57 · Sections 57.6, 57.7 · _Estimated reading time: 18 min_
> **Prerequisite:** [The Resource Cost of Errors](../01-concepts/04-resource-cost-of-errors.md)

## In one sentence

Every error consumes **CPU, memory, log bytes, and downstream attempts**, and a system that
has not budgeted those four is one incident away from turning its own error path into the
outage.

## Why this matters in production

Capacity planning normally models the happy path. The failure path is invisible in the plan
and dominant in the incident. This deep dive turns the error path into numbers you can put
next to your normal capacity numbers — so that "the service is fine at 2,000 rps" becomes
"the service is fine at 2,000 rps **including 5% failures**".

## The cost model

### Per-error costs

| Cost | Model | Typical value | How to measure |
| ---- | ----- | ------------- | -------------- |
| **Stack capture** | `c_stack × frames` | 5–50 µs | Microbenchmark `new Error()` at depth 30 |
| **Object allocation** | `size(error) × retained_count` | 0.5–5 KB | Heap snapshot under load |
| **Serialization** | `c_ser × bytes` | 10–100 µs | Benchmark the serializer |
| **Log write** | `bytes + compression + transport` | 1–10 KB | Log agent throughput |
| **Retry attempt** | `cost(happy path)` | 100% | The same work, done again |
| **Held resources** | `timeout × concurrency` | seconds | Pool utilization curve |

### The aggregate formula

For an error rate `e` on a service handling `R` requests/second:

```text
  errors_per_second = R × e

  error_path_cpu = R × e × (c_stack + c_ser + c_log)
  error_memory   = R × e × size × retention_seconds
  log_bytes_per_second = R × e × bytes_per_error
  downstream_extra_load = R × e × (A − 1)
```

### A worked budget

Acme's API: `R = 2,000 rps`, `e = 2%` in normal operation, 8 vCPU, `max_connections = 500`.

```text
  errors_per_second = 2,000 × 0.02 = 40

  c_stack  = 40 µs (30 frames)
  c_ser    = 60 µs
  c_log    = 100 µs
  ⇒ error_path_cpu = 40 × 200 µs = 8 ms/s = 0.008 cores      ✅ negligible

  bytes_per_error = 4 KB
  ⇒ log throughput = 40 × 4 KB = 160 KB/s = 0.16 MB/s        ✅ fine

  size = 3 KB, retention = 30 s
  ⇒ error_memory = 40 × 3 KB × 30 = 3.6 MB                  ✅ fine
```

At the **normal** 2% error rate, the error path is free. Now the same model at a **10%**
error rate during an incident:

```text
  errors_per_second = 200

  error_path_cpu = 200 × 200 µs = 40 ms/s = 0.04 cores        still small
  log throughput = 200 × 4 KB = 800 KB/s = 0.8 MB/s           still OK
  error_memory   = 200 × 3 KB × 30 = 18 MB                    OK
  downstream_extra_load = 2,000 × 0.10 × (A − 1)
```

With `A = 3`: `2,000 × 0.10 × 2 = 400` extra downstream requests/second. With `A = 12`:
`2,000 × 0.10 × 11 = 2,200` — **more than doubling** the downstream load.

**And at 12,000 errors/second** (Acme's real incident):

```text
  error_path_cpu = 12,000 × 200 µs = 2.4 cores = 30% of 8 cores   ⚠️
  log throughput = 12,000 × 4 KB = 48 MB/s                        ⚠️⚠️
  error_memory   = 12,000 × 3 KB × 30 = 1.08 GB                   ⚠️
  downstream_extra_load (A = 12) = 2,000 × 0.10 × 11 ≈ 2,200/s   ⚠️⚠️
```

The log throughput is the number that broke first: 48 MB/s saturated the log agent, which
competed for disk and CPU, which slowed *successful* requests. The error path became the
outage.

### Finding the breaking point

For each resource, solve for the error rate at which the budget is exhausted:

```text
  e_max_cpu   = (cpu_budget / R) / (c_stack + c_ser + c_log)
  e_max_log   = (log_budget_bytes_per_second / R) / bytes_per_error
  e_max_mem   = (mem_budget / R) / (size × retention)
  e_max_down  = (downstream_headroom / R) / (A − 1)
```

The **smallest** `e_max` is your real breaking point. Acme's numbers:

| Resource | Budget | `e_max` |
| -------- | ------ | ------- |
| CPU | 0.4 cores (5% of 8) | 0.4/2,000/200µs = **1.00 (100%)** |
| Log | 5 MB/s | 5,000,000/2,000/4,096 = **0.61 (61%)** |
| Memory | 512 MB | 512MB/2,000/3KB/30 = **2.79 (279%)** |
| Downstream (A = 12) | 20% headroom | 0.20/0.10/11 = **0.018 (1.8%)** |

The binding constraint was **downstream amplification at 1.8%** — below Acme's 5% alert
threshold. That is the same finding the storm math produced, from a different direction.

> ⚠️ **Hazard.** The log throughput budget is usually the smallest and the most overlooked,
> because logging is "just" infrastructure. A single verbose log line (a full request body,
> a stack trace on every rejection) changes the byte size by 10× and moves the breaking point
> from 61% to 6%.

## How it works (mechanics)

### Measuring the per-error cost

```ts
// A microbenchmark you can run in CI.
function measureErrorCost(depth: number): { stackUs: number; serializeUs: number } {
  const N = 10_000;

  // stack capture
  let t0 = performance.now();
  for (let i = 0; i < N; i++) capture(depth);
  const stackUs = (performance.now() - t0) * 1000 / N;

  // serialization
  const err = capture(depth);
  t0 = performance.now();
  for (let i = 0; i < N; i++) JSON.stringify(serialize(err));
  const serializeUs = (performance.now() - t0) * 1000 / N;

  return { stackUs, serializeUs };
}

function capture(depth: number): Error {
  return depth > 0 ? capture(depth - 1) : new Error("x");
}
```

Run it at startup (or in a CI benchmark) and store the numbers in a config file. Then the
budget formula becomes a runtime check rather than a guess.

### Bounding the bytes

```ts
// ✅ A bounded error payload: the size is a property of the type, not of luck.
export function serializeError(err: AppError): Record<string, unknown> {
  return {
    code: err.code,
    category: err.category,
    message: err.message.slice(0, 200),        // hard cap
    correlationId: err.correlationId,
    retryable: err.retryable,
    riskTier: err.riskTier,
    // The stack is included only for unexpected errors, and only for T3/T4.
    ...(err.unexpected ? { stack: err.stack?.split("\n").slice(0, 30).join("\n") } : {}),
    // Never the cause chain, the request body, or context values.
  };
}
```

Rules for keeping the bytes bounded:

| Rule | Effect |
| ---- | ------ |
| Cap the message at 200 characters | Prevents a vendor's HTML error page from becoming a 40 KB log line |
| Cap the stack at 30 frames | A 120-frame stack is 12 KB |
| **Never** log the request body | The largest and most dangerous field |
| Never log the cause chain verbatim | Vendor payloads can be huge; take the code, not the body |
| Allowlist context fields | `tenantId`, `correlationId` — not arbitrary objects |

### The validation-rejection fast path

```ts
// ✅ A rejection that allocates almost nothing.
export type Rejection = {
  status: 422;
  code: "VALIDATION_FAILED";
  issues: FieldIssue[];       // ≤ 20
  fields: string[];           // names only — never values
};

export function reject(issues: FieldIssue[]): Rejection {
  return {
    status: 422,
    code: "VALIDATION_FAILED",
    issues: issues.slice(0, 20),
    fields: issues.map((i) => i.field),
  };
}
```

No `Error` object, no stack, no cause, no body. The cost is one small object and a JSON
serialization of a capped array.

## Worked example — `Acme SaaS` sizing the validation-rejection budget

Acme's API receives 2,000 rps. During a partner-integration bug, 15% of traffic (300 rps)
was invalid.

Without controls:

```text
  errors_per_second = 300
  error_path_cpu = 300 × 200 µs = 0.06 cores          ✅
  log throughput = 300 × 4 KB = 1.2 MB/s               ⚠️ (PII attached)
  downstream_extra_load = 0 (no retry on 4xx)          ✅
```

The CPU was fine. The problem was the **log payload**: the original code attached the
request body (2.5 KB average) to every rejection log, so the real throughput was
`300 × 6.5 KB = 1.95 MB/s`, and the body contained the customer's email address — a PII
leak in the log pipeline, at volume.

After the fix:

| Change | Effect |
| ------ | ------ |
| Rejections return a value, not an `Error` | No stack capture (−40 µs each) |
| Log only the failing **field names** | 4 KB → 120 bytes per line |
| Sample rejection logs at 1% above 20/s | 1.95 MB/s → 0.02 MB/s |
| Exact counter kept for the error-rate alert | The alert still fires accurately |
| Rate-limit invalid requests per API key at 20/s | Volume capped at the source |

Result: `300 rps` of invalid traffic now costs ~0.01 cores and 20 KB/s of logs, and no PII
reaches the log pipeline.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Log every error in full | Complete diagnostics | Log-storm; PII exposure | Below 100 errors/s, T3/T4 only |
| Sample above a threshold | Bounded cost | Some detail missing | **Default** |
| Cap the payload size | Bounded bytes | Loses detail | **Always** |
| Never log request bodies | No PII leak | Harder debugging | **Always** |
| Reject without an `Error` object | Cheapest rejection | No stack for rejections | Validation paths |
| Pre-validate before expensive work | Avoids downstream cost | Slightly slower rejection | **Always** |
| Rate-limit invalid requests | Stops the flood | Legitimate clients can be throttled | Per API key |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Measure the per-error cost | Assume it is free |
| Compute the breaking point per resource | Plan capacity only for the happy path |
| Cap messages at 200 chars and stacks at 30 frames | Log vendor HTML error pages verbatim |
| Never log request bodies or cause chains | Attach the body to a rejection log |
| Sample logs but keep exact counters | Sample the counters too |
| Return rejections as values | Throw for a `422` |
| Rate-limit invalid traffic per client | Let one client consume the error budget |

## Common mistakes

- **Planning only the happy path.** The error path is a workload that appears exactly when
  the system is already degraded.
- **Treating logs as free.** Log volume is the most common first resource to saturate.
- **Attaching context objects wholesale.** One `ctx` with a request body can be 10 KB.
- **Sampling without counters.** The dashboard shows the error rate dropping while it is
  actually climbing.
- **Thinking in averages.** Errors arrive in bursts; budget for the burst (the 1-second
  peak), not the 1-minute average.
- **Ignoring the cost of *successful* rejections.** A `422` is a success to your metrics
  system and therefore completely unbudgeted.

## Checklist

- [ ] The per-error CPU, memory, and byte cost is measured, not guessed.
- [ ] Each resource's breaking error rate (`e_max`) is computed; the smallest one is known.
- [ ] The error-path CPU budget is ≤ 5% of total CPU.
- [ ] The log throughput budget is ≤ 5 MB/s per service.
- [ ] Error payloads are capped (message ≤ 200 chars, stack ≤ 30 frames).
- [ ] Request bodies and cause chains are never logged.
- [ ] Log sampling kicks in above 100 errors/s, with exact counters preserved.
- [ ] Validation rejections allocate no `Error` and no stack.
- [ ] Invalid-request volume is rate-limited per client.

## Related

- [The Resource Cost of Errors](../01-concepts/04-resource-cost-of-errors.md)
- [Error-Storm Math](./01-error-storm-math.md)
- [Chapter 36 — Sensitive Data and Error Context](../../../part-13-security-aware/36-sensitive-data-and-error-context/README.md)
- [Chapter 34 — Security Principles for Error Handling](../../../part-13-security-aware/34-security-principles-for-error-handling/README.md)
