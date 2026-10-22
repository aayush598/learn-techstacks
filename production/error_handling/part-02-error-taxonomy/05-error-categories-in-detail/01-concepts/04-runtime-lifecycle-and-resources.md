# Runtime, Resource, and Lifecycle Categories (5.22, 5.25–5.27, 5.31)

> Part II · Chapter 5 · Sections 5.22, 5.25–5.27, 5.31 · _Estimated reading time: 28 min_
> **Prerequisite:** [External, Network, and Config Categories](./03-external-network-and-config.md)

## In one sentence

This family covers failures **inside your own process** — **resource exhaustion, programming
bugs, unexpected runtime faults, cancellation, and shutdown/lifecycle** — where the correct
posture is usually fail-fast, isolate, and terminate safely.

## Why this matters in production

These are the failures that take down *processes*, not requests. An OOM kills the worker; an
uncaught exception at 3 a.m. restarts the container; a failed graceful shutdown drops in-flight
work. They are rarely retryable in place — the recovery is **isolation, restart, or load
shedding**, not a bigger `try/catch`.

## 5.22 Resource exhaustion

**Resource exhaustion** means a finite resource ran out: memory, file descriptors, sockets,
connection pool, threads, disk, queue capacity.

| Resource | Symptom | Signal |
| -------- | ------- | ------ |
| memory | OOM kill | `ENOMEM`, container OOMKilled |
| file descriptors | cannot open files | `EMFILE`, `ENFILE` |
| sockets | cannot connect | `EADDRINUSE`, ephemeral port exhaustion |
| DB pool | requests block | `53300 too_many_connections`, pool timeout |
| disk | writes fail | `ENOSPC` |
| queue | latency spikes | backlog / age metrics |

| Aspect | Value |
| ------ | ----- |
| HTTP | `503` (shed) |
| Retry | yes, but **bounded** — retries worsen exhaustion |
| Fix | bulkheads, backpressure, admission control (Chapter 57) |

> ⚠️ **Hazard.** Unbounded retry under exhaustion is a **retry storm** — it converts a degraded
> dependency into a full outage. Bound retries and shed load.

## 5.25 Internal programming

**Programming** errors are defects in our code: `TypeError`, `NullPointerException`, assertion
failures, impossible states, off-by-one on a boundary.

| Aspect | Value |
| ------ | ----- |
| HTTP | `500` (generic) |
| Retry | **never** — it will recur deterministically |
| Alert | yes (a bug on the path) |
| Disclosure | generic message; full detail to logs |

Programming errors should be **fixed**, not handled. A `NullPointerException` caught and converted
to a 400 hides a bug (Chapter 1). Treat these as alerts that demand a code change.

## 5.26 Unexpected runtime

**Unexpected runtime** errors are failures that are not "bugs" in our code yet are not
anticipated: an impossible branch, a library throwing something new, an OS-level fault.

| Aspect | Value |
| ------ | ----- |
| HTTP | `500` |
| Retry | depends on cause (usually no) |
| Alert | yes |
| Disclosure | generic |

The default handling is the **outermost catch-all**: log with full context, return a generic
`500`, never leak internals. This is the *only* category where "catch everything" is correct — and
only at the very top (Chapter 21.18).

## 5.27 Cancellation / interruption

The caller went away: client closed the connection, deadline elapsed, user navigated, worker got
`SIGTERM`. This is **not a failure of the operation** — it is a request to stop.

| Trigger | Signal |
| ------- | ------ |
| client disconnect | `499` (nginx convention), `context canceled` (Go) |
| gRPC cancel | `CANCELLED (1)` |
| user abort | DOM `AbortController` |
| worker shutdown | `SIGTERM` |

| Aspect | Value |
| ------ | ----- |
| Retry | no (the initiator left) |
| Log level | `info` (not `error`) |
| Must do | cancel downstream work, release resources, don't mark as failure |

> ⚠️ **Hazard.** Cancellation must **not** be turned into success *or* into a generic error. If a
> write is mid-flight, you have an **ambiguous outcome** (Chapter 58.13) and need idempotency.

## 5.31 Shutdown / lifecycle

**Shutdown** failures occur when a process is going down: in-flight requests dropped, jobs
abandoned, cleanup skipped, health still reporting "ok" while draining.

| Phase | Correct behavior |
| ----- | ---------------- |
| receive `SIGTERM` | stop accepting new work; mark unready |
| drain | finish or checkpoint in-flight work up to a grace period |
| cleanup | close pools, flush buffers, commit/rollback |
| force kill | after grace period, terminate without corruption |

Kubernetes sends `SIGTERM` then `SIGKILL` after `terminationGracePeriodSeconds` (default **30s**).
Shutdown errors are otherwise the "process terminated holding a lock / mid-transaction" class
(Chapter 41.14–41.15).

## Worked example — ExportJob worker under pressure

```text
Worker processes 1M-row exports on a queue:
  heap grows unbounded              → 5.22 resource_exhaustion → OOM kill; add streaming + bulkhead
  null deref in transform           → 5.25 internal_programming → fail job, alert, fix code
  unknown library throw             → 5.26 unexpected_runtime   → job fails, DLQ after attempts
  deploy sends SIGTERM mid-export   → 5.31 shutdown_lifecycle   → checkpoint + resume on next start
  operator cancels the run          → 5.27 cancellation         → stop, release, mark "canceled" not "failed"
```

Each category maps to a different response: bound, fix, quarantine, checkpoint, or stop.

## Key data / numbers

- Linux `EMFILE`/`ENFILE` = file descriptor exhaustion; `ENOMEM` = memory; `ENOSPC` = disk.
- Kubernetes default `terminationGracePeriodSeconds` is **30 s**; in-flight work must finish or
  checkpoint within it.
- `499` is the de-facto nginx "client closed request" code (not in RFC 9110).
- gRPC `CANCELLED (1)` and `DEADLINE_EXCEEDED (4)` are distinct from `INTERNAL (13)`.

## Real-world use case — Acme SaaS

Acme's export workers used to restart on deploy and **lose** in-flight exports, then retry from
scratch and duplicate S3 objects. Classification separated `shutdown_lifecycle` (checkpoint on
`SIGTERM`) from `cancellation` (operator stop → mark canceled) and `resource_exhaustion` (stream
instead of buffering). Deploy-time data loss and duplicate objects both went to zero.

## Trade-offs

| Category | Retry | Terminate? | Primary fix |
| -------- | ----- | ---------- | ----------- |
| resource_exhaustion | bounded | maybe | backpressure, bulkheads |
| internal_programming | no | fix code | code change + test |
| unexpected_runtime | no | catch-all | investigate |
| cancellation | no | cleanup only | cooperative cancel |
| shutdown_lifecycle | resume | graceful | drain + checkpoint |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Treat cancellation as a signal, log `info` | Record it as a failure/error |
| Bound retries under exhaustion | Retry-storm a saturated resource |
| Fail fast on programming errors | Catch NPE and return `400` |
| Checkpoint on `SIGTERM` | Drop in-flight work on shutdown |
| Use one outermost catch-all | Catch-all in the domain |

## Common mistakes

- **Logging cancellations at `error`**, creating alert noise.
- **Retrying during exhaustion**, deepening the outage.
- **Swallowing programming errors** and masking bugs.
- **Skipping graceful shutdown**, corrupting partial state.

## Checklist

- [ ] Are retries bounded during resource pressure?
- [ ] Do programming errors alert and fail fast?
- [ ] Is cancellation handled as a signal, not a failure?
- [ ] Does shutdown drain, checkpoint, and clean up?
- [ ] Is the single catch-all at the outermost boundary only?

## Related

- [External, Network, and Config Categories](./03-external-network-and-config.md)
- [Async Jobs, Partial Failure, and Specialized Categories](./05-async-jobs-partial-and-specialized.md)
- [Process, Runtime, and Resource Failures](../../../part-15-distributed-failures/41-process-runtime-and-resource-failures/README.md)
- [Error Handling Under Load and at Scale](../../../part-22-design-decisions/57-error-handling-under-load-and-at-scale/README.md)
