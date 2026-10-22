# Chapter 31 — Reference

> Part XII · Chapter 31 · all sections · _Estimated reading time: 10 min_

## Aggregation decision table

| Need | Primitive | Settles on | Failure visibility | Notes |
| ---- | --------- | ---------- | ------------------ | ----- |
| All results required | `Promise.all` | First rejection | One error | Abort siblings manually |
| Partial results useful | `Promise.allSettled` | All settle | Every outcome | Map statuses to codes |
| Any one source suffices | `Promise.any` | First fulfillment | Only if all fail | `AggregateError` |
| Bound concurrency | Pool / `for await` | All workers done | Depends on loop | Protects pools/sockets |
| First error + cancel rest | `errgroup.WithContext` (Go) | First error | One error | True cancellation |

## Timeout and cancellation cheatsheet

| Runtime | Cancel | Timeout | "Cancelled" signal | Notes |
| ------- | ------ | ------- | ------------------ | ----- |
| JS/TS | `AbortController.abort()` | `AbortSignal.timeout(ms)` | `AbortError` | `AbortSignal.any` to compose |
| Node HTTP | — | `server.requestTimeout` | — | Set below proxy timeout |
| Python | `Task.cancel()` | `asyncio.timeout(ms)` | `CancelledError` | Inherits `BaseException` |
| Go | `context.WithCancel` | `context.WithTimeout` | `context.Canceled` | `defer cancel()` |
| Kotlin | `Job.cancel()` | `withTimeout(ms)` | `CancellationException` | `coroutineScope` propagates |
| Java | `Future.cancel(true)` | `orTimeout(ms)` | `CancellationException` | Check interruption |

## Terminal state vocabulary

| State | Meaning | Retry? | Counts as error? |
| ----- | ------- | ------ | ---------------- |
| `succeeded` | Completed fully | No | No |
| `partial` | Some branches failed | Per branch | Yes (branch-level) |
| `failed` | Did not complete | Per classification | Yes |
| `cancelled` | Caller stopped it | No | No |
| `timed_out` | Deadline exceeded | Usually | Yes (as timeout) |

> Never collapse these five into "success" and "error." Retry, alerting, and billing all depend on
> the distinction.

## Detached-failure detection matrix

| Runtime | Detector | What it misses |
| ------- | -------- | -------------- |
| Node.js | `unhandledRejection` | Failures in already-exited work |
| Browsers | `window.onunhandledrejection` | Errors ignored by the user |
| Python | Task GC warning | Tasks kept alive by references |
| Go | Goroutine count / `pprof` | Blocked sends with no growth alarm |
| JVM | Unjoined `CompletableFuture` | Silent dropped results |

## Backoff / delay formula (for async retries)

```text
exponential:  delay = min(cap, base * 2^attempt)
full jitter:  delay = random(0, min(cap, base * 2^attempt))
equal jitter: delay = half + random(0, half), half = min(cap, base*2^attempt)/2
```

Typical: `base = 200 ms`, `cap = 30 s`, **full jitter**, max 5–8 attempts. (Full policy in
[Chapter 27](../../../part-11-retry-and-resilience/27-retry-policies/README.md).)

## Concurrency sizing rule of thumb

| Work type | Suggested in-flight cap |
| --------- | ----------------------- |
| External HTTP calls | 10–50 per worker |
| Database queries | ≤ pool size (often 10–20) |
| LLM/tool calls | 2–8 (cost + rate limits) |
| CPU-bound tasks | ≈ number of cores |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| **Detached failure** | A rejection/task whose outcome no one observes |
| **Unhandled rejection** | A rejected promise with no handler at the end of the microtask turn |
| **Fail-fast** | Aggregate settles on first failure; siblings should be aborted |
| **Collect-all** | Wait for every branch and report each outcome |
| **Partial success** | Some branches succeeded; result must say which |
| **Deadline** | Absolute time by which the operation must finish |
| **Cancellation** | Cooperative signal to stop work; not a failure |
| **Async context** | Request/tenant/job identifiers carried across async boundaries |
| **Backpressure** | Slowing producers when consumers cannot keep up |

## Related

- [Chapter 31 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 27 — Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
- [Chapter 32 — Background Jobs](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- [Glossary](../../../GLOSSARY.md)
