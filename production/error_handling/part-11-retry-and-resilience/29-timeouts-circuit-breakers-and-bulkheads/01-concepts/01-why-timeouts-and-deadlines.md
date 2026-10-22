# Why Timeouts and Deadlines

> Part XI · Chapter 29 · Sections 29.1–29.4 · _Estimated reading time: 18 min_
> **Prerequisite:** [Chapter 26 — Network and Distributed Communication Errors](../../../part-10-external-dependencies/26-network-and-distributed-communication-errors/README.md)

## In one sentence

A timeout is a **promise to stop waiting**; a deadline is the **absolute time by which the whole
operation must finish**, and only deadlines propagated across hops prevent a slow dependency from
consuming capacity indefinitely.

## Why this matters in production

A network call without a timeout can hang until the OS gives up — minutes or hours. Every hung call
holds a connection, a thread or task, and possibly a database transaction. A few thousand of those and
the pool is exhausted, the queue is full, and a single slow dependency has taken down the whole
service. Timeouts are the cheapest reliability control you have, and they are the one most often
forgotten on internal calls because "it's fast."

## 29.1 — Why timeouts

Timeouts protect three resources:

| Resource | Without a timeout | With a timeout |
| -------- | ----------------- | -------------- |
| Connection | Held until TCP gives up | Released, returned to pool |
| Worker/thread | Blocked indefinitely | Freed for other work |
| Transaction | Open, holding locks | Rolled back, locks released |

They also bound **latency**: a caller can reason about worst-case response time only if every
downstream call is bounded.

> ⚠️ **Hazard.** A timeout is not optional because a dependency is "internal." Internal services
> fail, deploy, and get saturated exactly like external ones.

## 29.2 — Connection, request, and operation deadlines

These are different layers of the same problem:

| Timeout | Bounds | Configured on |
| ------- | ------ | ------------- |
| **Connect timeout** | TCP/TLS handshake | HTTP client / socket |
| **Request timeout** | One request/response exchange | HTTP client |
| **Per-attempt timeout** | One attempt in a retry loop | Retry policy |
| **Operation deadline** | Entire operation including retries and fallbacks | Request/job boundary |

A robust client sets all four. Example:

```text
connectTimeout       = 1s
requestTimeout       = 3s
perAttemptTimeout    = 3s
operationDeadline    = 10s   (allows up to 3 attempts with backoff)
```

### The layered relationship

```text
operation deadline (10s)
  ├─ attempt 1: request timeout 3s + backoff 200ms
  ├─ attempt 2: request timeout 3s + backoff 400ms
  └─ attempt 3: request timeout 3s
total worst case ≈ 9.6s  ✅ fits
```

If the per-attempt timeout were 5s, three attempts could not fit in 10s; the policy must clamp the
last attempt or stop earlier.

## 29.3 — Propagation

A deadline must travel with the request. Resetting it at each hop is how a 30s client timeout becomes
a 90s server operation.

### How deadlines propagate

| Transport | Mechanism |
| --------- | --------- |
| gRPC | `grpc-timeout` header / `context.WithDeadline` |
| HTTP | `X-Request-Deadline` / `X-Request-Timeout-Ms` (convention, not standard) |
| Message queue | Deadline stored in message metadata |
| In-process | Pass a context with a deadline |

```go
func (s *Service) GetUser(ctx context.Context, id string) (*User, error) {
    // Do not create a fresh 5s timeout; respect the caller's budget.
    ctx, cancel := context.WithTimeout(ctx, 2*time.Second)
    defer cancel()

    if deadline, ok := ctx.Deadline(); ok && time.Until(deadline) < 100*time.Millisecond {
        return nil, ErrDeadlineExceeded
    }
    return s.repo.Find(ctx, id)
}
```

The inner timeout is a **cap**, not a reset: `WithTimeout` takes the earlier of the parent deadline
and the new one. In languages without context propagation, pass the absolute deadline explicitly.

### Budget allocation

Split the remaining budget across sequential and parallel steps:

```text
remaining = 10s
  ├─ auth check      0.5s
  ├─ DB read         2s
  ├─ provider call   5s
  └─ serialize       0.5s  (reserve)
```

Reserve time for serialization, logging, and cleanup — a deadline that leaves zero slack turns a
successful call into a client-side timeout.

## 29.4 — Timeout vs cancellation

| Concept | Meaning | Trigger |
| ------- | ------- | ------- |
| **Timeout** | Local limit on how long to wait | `deadline exceeded` |
| **Cancellation** | Caller explicitly aborts | Client disconnect, shutdown, user action |

They are related but not identical:

- A timeout should **cancel** the underlying work (abort the HTTP request, cancel the query).
- A cancellation is not a failure to retry; it means the result is no longer needed.
- Cleanup must run in both cases (Chapter 14).

```ts
const controller = new AbortController();
const timer = setTimeout(() => controller.abort(new TimeoutError()), 3_000);

try {
  return await fetch(url, { signal: controller.signal });
} catch (err) {
  if (controller.signal.aborted) throw new TimeoutError("request timed out");
  throw err;
} finally {
  clearTimeout(timer); // always release the timer
}
```

> **Rule:** if you time out, you must also **stop the work**. Otherwise the timeout frees the caller
> but the dependency keeps working, consuming capacity for a result nobody will read.

## Worked example — an unbounded internal call

```ts
// Before: hangs for the OS default (often minutes).
const res = await fetch("http://recommendations/recommend");

// After: connect + request + operation deadline, cancellation on timeout.
const controller = new AbortController();
const timer = setTimeout(() => controller.abort(), 2_000);
try {
  const res = await fetch("http://recommendations/recommend", {
    signal: controller.signal,
    // Node's undici supports connect timeout via dispatcher; set at client level.
  });
  return await res.json();
} finally {
  clearTimeout(timer);
}
```

## Key data / numbers

- Common connect timeout: **500ms–1s** (internal), 1–3s (external).
- Common request timeout: **2–5s** for APIs, 10–30s for providers.
- Client defaults often **infinite** (Node `fetch`, Python `requests` without `timeout`).
- Go: `http.Client{Timeout: ...}` sets the whole request; `DialContext` sets connect.
- gRPC: `grpc-timeout` is in the request headers; deadlines are absolute in-process.
- Reserve **10–20%** of the operation budget for serialization/cleanup.

## Real-world use case — Acme SaaS

Acme's dashboard called a recommendations service with no timeout. The service's own dependency
became slow, so each recommendation call took 60–120s. Dashboard workers exhausted their pool, and
the entire dashboard — including pages that did not use recommendations — became unresponsive. Adding
a 1.5s request timeout and a 3s operation deadline freed workers, and the dashboard degraded to "no
recommendations" instead of failing. Latency for the affected page dropped from ~90s to ~1.6s.

## Trade-offs

| Timeout | Too short | Too long |
| ------- | --------- | -------- |
| Connect | False failures on slow networks | Slow handshakes hold workers |
| Request | Failed calls that would have succeeded | Hung workers |
| Operation | Premature cancellation | Exceeds caller SLA |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Set connect, request, and operation bounds | Rely on OS defaults |
| Propagate the remaining deadline | Reset a fresh timeout per hop |
| Cancel work on timeout | Leave the request running |
| Reserve slack for cleanup | Use the entire budget for calls |
| Treat cancellation as non-retryable | Retry after the caller gave up |

## Common mistakes

- **No timeout on internal calls.** "It's fast" is not a bound.
- **Timeout without cancellation.** The dependency keeps working.
- **Deadline reset at each service.** Total latency grows with depth.
- **Timeout longer than the caller's remaining budget.** Guaranteed wasted work.
- **Catching `AbortError` and retrying**, defeating cancellation.

## Checklist

- [ ] Every outbound call has a connect and request timeout.
- [ ] Every operation has an absolute deadline.
- [ ] Deadlines propagate across services and queues.
- [ ] Timeout cancels the underlying work.
- [ ] Cancellation is not retried.
- [ ] Cleanup time is reserved in the budget.

## Related

- [Deadline Propagation](../02-deep-dive/02-deadline-propagation.md)
- [Circuit Breaker States and Conditions](./02-circuit-breaker-states-and-conditions.md)
- [Chapter 27 — Retry Policies](../../27-retry-policies/README.md)
- [Chapter 26 — Network and Distributed Communication Errors](../../../part-10-external-dependencies/26-network-and-distributed-communication-errors/README.md)
