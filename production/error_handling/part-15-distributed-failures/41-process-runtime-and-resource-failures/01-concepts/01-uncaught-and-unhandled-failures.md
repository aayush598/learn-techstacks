# Uncaught Exceptions and Unhandled Async Failures (41.1–41.2)

> Part XV · Chapter 41 · Sections 41.1–41.2 · _Estimated reading time: 19 min_
> **Prerequisite:** [Async Propagation and Unhandled Rejections](../../../part-05-exception-mechanics/12-exception-propagation-and-control-flow/02-deep-dive/02-async-propagation-and-unhandled-rejections.md)

## In one sentence

An **uncaught exception** is an error that escaped every handler on the stack, and an **unhandled
rejection** is a promise that failed with nobody watching — both are **signals about the state of
the process**, so the correct response is **log, flush, exit non-zero**, never "catch it and keep
serving".

## Why this matters in production

A handled error is a `500` and a log line. An *uncaught* error is the runtime deciding the process
can no longer be trusted: Node prints the stack and exits, taking every in-flight request, every
open Postgres transaction, and every pending timer with it. The uncomfortable part is that the
"safe" recovery — installing a handler that logs and continues — is the one thing that turns a
clean crash into a **zombie**: a process serving traffic whose invariants are already broken. The
whole point of a last-resort handler is to make the *death* clean and diagnosable, not to
prevent it.

## Core concept

### 41.1 Uncaught exceptions

An uncaught exception is any error that reaches the top of the stack with no handler in the chain.
The runtime's default behavior is to print the error and terminate the process.

```text
request handler ──throws──▶ route layer ──no try/catch──▶ process boundary
                                                          ↓
                                            runtime default: print + exit(1)
```

Common sources, in rough order of how often they appear in production:

| Source | Typical example |
|--------|-----------------|
| Throw in a callback | `setTimeout(() => { throw err }, 0)` — the `try/catch` around the *scheduler* does not cover the callback |
| Throw in an event handler | `emitter.on('data', () => { throw err })` |
| Throw inside a promise chain | `.then(a).then(b)` where `b` throws and no `.catch` is attached |
| Throw in a `Promise` executor | `new Promise(() => { throw err })` |
| Runtime-level faults | `TypeError: Cannot read properties of undefined` — a real bug, not an expected error |
| Throw in `process.nextTick` / `setImmediate` | escapes the current turn entirely |

The **contract** of a last-resort handler is short and non-negotiable:

```text
1. LOG the error with correlation id, request id, and what the process was doing
2. FLUSH logs and telemetry (stdout is async in Node — a bare process.exit() can truncate it)
3. EXIT with a non-zero code so the orchestrator restarts you
```

Why step 3 is not optional: a process that continues after an uncaught exception has **undefined
state**. Node's own documentation says the process "is not in a safe state" — an in-flight
transaction may be half-applied, a mutex may still be held, a file may be half-written, a library's
internal cache may be inconsistent. Continuing is not recovery; it is *unbounded uncertainty*.

> ⚠️ **Hazard.** `process.exit()` in a `uncaughtException` handler truncates buffered stdout/stderr
> in Node, so the log line you just wrote may never reach your log shipper. Flush explicitly, or
> exit via `process.exitCode = 1` and let the event loop drain.

### 41.2 Unhandled async failures

An **unhandled rejection** is a promise that was rejected and still had no rejection handler by
the end of the current turn of the event loop. It is the async twin of the uncaught exception, and
it is the single most common way a Node service dies in 2026.

```text
async function handler() { ... }

handler();                       // ← no .catch(), no await, no try/catch
   └─ promise rejects
        └─ no handler attached by the end of the turn
             └─ runtime raises: unhandledRejection
                  └─ default (Node ≥ 15): raised as uncaughtException → exit(1)
```

The important structural point: **the rejection has no stack trace of its own.** It carries the
stack from the point it was thrown, but the *absence* of a handler is invisible in code review.
That is why the failure mode is so common — `void doAsyncWork()` looks correct.

| Runtime | Unhandled async failure behavior |
|---------|-----------------------------------|
| **Node.js** | `unhandledRejection` event; default since v15 is to raise it as an uncaught exception → **exit 1** |
| **Python `asyncio`** | "Task exception was never retrieved" logged at garbage-collection time — **the process does not exit**; the failure is silent until GC runs |
| **Go** | A `panic` in a goroutine that nobody `recover()`s **kills the whole process**; a dropped `err` from `go func()` is a *compile-time* error, not a runtime one |
| **Rust** | A `JoinHandle` whose `Err` is never read is **silently dropped** — no warning by default |

Note the asymmetry: **Python hides it, Go is loud, Node is loud by default.** The runtimes differ
so much that "our error handling" cannot be a runtime-agnostic habit — it must be a per-runtime
mechanism.

## How it works (mechanics)

### The Node rejection lifecycle

```text
t0  promise rejects
t1  end of microtask checkpoint → runtime checks: is a rejection handler attached?
t2  no handler → emit 'unhandledRejection' (reason, promise)
      └─ default mode 'throw' → raised as an uncaught exception
           └─ emit 'uncaughtExceptionMonitor'  (Node ≥ 12.17: logging-only, cannot exit)
                └─ emit 'uncaughtException'     → your handler: log, flush, exit
t3  if a handler is attached LATER → 'rejectionHandled' fires (the error was already reported)
```

Two consequences worth internalizing:

1. **The reason may not be an `Error`.** `Promise.reject("string")`, `Promise.reject(undefined)`,
   and `throw "string"` all produce a non-Error reason. A handler that does `reason.stack` will
   itself throw inside the handler — inside the handler for an uncaught exception. Always
   normalize the reason before logging it.
2. **`rejectionHandled` means someone attached a handler late.** That is a code smell worth
   logging separately: the failure was already reported, and the late handler may now run cleanup
   logic against an operation the runtime already flagged as fatal.

### The "detect then exit" pattern

```ts
// Fatal paths only: log → flush → exit. Never `return` and keep serving.
function fatal(reason: unknown, kind: "uncaughtException" | "unhandledRejection") {
  const err = reason instanceof Error ? reason : new Error(String(reason));
  log.error({ err, kind, pid: process.pid, uptime: process.uptime() }, "fatal process error");
  flushLogsAndTelemetry()
    .catch(() => {})
    .finally(() => process.exit(1));
}

process.on("uncaughtExceptionMonitor", (err) => {
  log.error({ err, origin: "uncaughtExceptionMonitor" }, "uncaught exception (monitor)");
});
process.on("uncaughtException", (err, origin) => fatal(err, "uncaughtException"));
process.on("unhandledRejection", (reason) => fatal(reason, "unhandledRejection"));
```

`uncaughtExceptionMonitor` is the right place for "something is very wrong" telemetry: it fires
*before* the fatal handler, and `process.exit()` inside it is a no-op — so it must never be your
only handler.

## Worked example

The failure this chapter is about, in the shape it actually appears:

```ts
// ❌ The bug: a detached promise. Looks fine. Kills the process under load.
export async function enqueueExport(tenantId: string, query: ExportQuery): Promise<void> {
  void jobs.enqueue("ExportJob", { tenantId, query });   // nothing observes the rejection
}
```

```text
timeline
  t0  enqueueExport() called; `jobs.enqueue` returns a promise
  t1  the job queue is momentarily unavailable → promise rejects with QueueUnavailable
  t2  nobody attached a handler → 'unhandledRejection'
  t3  Node (default 'throw') raises it as an uncaught exception
  t4  process exits with code 1 — mid-request, with an open DB transaction
  t5  orchestrator restarts the pod → crash loop while the queue is down
```

The fix is not a bigger `try/catch` — it is to make the promise **observed** at the boundary where
the work is started, and to treat a failure to enqueue as a failure of the caller's request:

```ts
export async function enqueueExport(tenantId: string, query: ExportQuery): Promise<JobRef> {
  try {
    return await jobs.enqueue("ExportJob", { tenantId, query });
  } catch (err) {
    throw new DomainError("EXPORT_QUEUE_UNAVAILABLE", {
      http: 503,
      retryable: true,
      cause: err,
      details: { tenantId },
    });
  }
}
```

Now the caller sees a `503` with a stable code and can retry; nothing escapes to the runtime.

## Key data / numbers

- **Node default `--unhandled-rejections` mode is `throw`** (since Node v15): the rejection is
  raised as an uncaught exception and the process exits with **code 1**.
- `--unhandled-rejections=strict` makes the raise unconditional (the recommended CI setting);
  `warn` and `warn-with-error-code` downgrade it to a warning; `none` silences it.
- `process.on("uncaughtExceptionMonitor", ...)` — Node **v12.17+**; fires before
  `uncaughtException`; `process.exit()` inside it is a no-op.
- `process.on("rejectionHandled", ...)` — fires when a handler is attached *after* the rejection
  was already reported.
- Uncaught exception → **exit code 1**; `SIGTERM` → **143**; `SIGKILL` → **137**;
  `SIGSEGV` → **139**; `SIGABRT` (V8 heap OOM abort) → **134**.
- Node's `EventEmitter` default `maxListeners` is **10** — the 11th listener on one emitter emits
  **`MaxListenersExceededWarning`**. It is a leak detector, not a crash; see
  [Pool, Queue, and CPU Pressure](./03-pool-queue-and-cpu-pressure.md).
- Python's `asyncio` logs "Task exception was never retrieved" only when the task object is
  **garbage-collected** — an unbounded delay between the failure and the log.
- Go: an unrecovered `panic` in any goroutine exits the process with **status 2**; `recover()`
  only works in a deferred function of the panicking goroutine's own frame.

## Real-world use case — Acme SaaS

`ExportJob` enqueueing used a detached promise inside the request handler. On a Tuesday morning
the job queue's Redis node was briefly unreachable; every export request produced one unhandled
rejection, and because Node's default raises them as uncaught exceptions, the API pod exited
with code 1 **mid-request** — with an open Postgres transaction and a half-written audit row. The
orchestrator restarted the pod, the pod enqueued another export attempt on boot-path retry, and
the pod crashed again: a **crash loop that produced no error page**, only a 503 from the load
balancer.

The fix had two parts. First, `enqueueExport` now awaits and translates the failure into a
`503 EXPORT_QUEUE_UNAVAILABLE` with a stable code, so the queue outage became a *client-visible
degradation* instead of a process death. Second, the worker — not the API — owns queue
availability: exports that cannot be queued are written to a durable `export_requests` table and
enqueued by a reconciler. Crash loops went to zero, and the number of exports delayed by a queue
outage became a metric (`export_enqueue_deferred_total`) instead of a mystery.

The lesson: the unhandled rejection was never the bug. **The bug was an unobserved promise on a
path the system needed to survive.**

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| **Log + flush + exit(1)** on uncaught/unhandled | clean, diagnosable death; orchestrator restarts you | loses in-flight work | default, always |
| Log and continue serving | "no downtime" | undefined state; silent corruption; masks the bug | never in production |
| Install a handler only to add context, then rethrow | keeps default crash semantics, adds metadata | none | when you need a fatal-event hook |
| Crash only on unknown errors, recover known ones | availability for expected failures | requires a strict error taxonomy | with a real taxonomy in place |
| Suppress unhandled rejections (`--unhandled-rejections=none`) | quiet logs | hides real bugs | never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Log, flush, then exit non-zero | Log and keep serving |
| Normalize a non-`Error` rejection reason before logging | Assume `reason.stack` exists |
| Await/observe every promise you start | Start detached promises with `void` |
| Translate expected failures into domain errors at the boundary | Let expected errors reach the runtime |
| Test that a deliberate throw exits the process with code 1 | Assume your CI catches unhandled rejections |
| Use `--unhandled-rejections=strict` in CI | Run CI with `none` or `warn` |

## Common mistakes

- **Installing `process.on('uncaughtException')` to "keep the server up"** — this is the single
  most common way teams convert a crash into silent data corruption.
- **`process.exit(1)` immediately after logging** — Node's stdout is asynchronous; the log line
  can be truncated before it is written. Flush first.
- **Leaving the default `unhandledRejection` behavior undocumented** — a team that later adds
  `--unhandled-rejections=warn` silently converts crashes into log noise.
- **Catching the error and returning `200` with an empty body** — converts a failure into
  success-shaped output, the worst outcome of all.
- **Relying on `uncaughtException` for cleanup** — cleanup that runs after an uncaught exception
  runs on a corrupted process; make cleanup part of *graceful shutdown*, not of the crash path.
- **Forgetting `Promise.all` rejections** — `Promise.all` rejects on the first failure while the
  other promises keep running; their later rejections become unhandled. Use `allSettled`.

## Checklist

- [ ] `uncaughtException` and `unhandledRejection` handlers log, flush, and exit non-zero.
- [ ] The handler normalizes non-`Error` reasons before logging.
- [ ] `--unhandled-rejections=strict` in CI and in production start-up flags.
- [ ] No detached promises (`void asyncFn()`) without an explicit `.catch`.
- [ ] Expected failures are translated to domain errors at the boundary, never left to the runtime.
- [ ] A test asserts a deliberate uncaught error exits with code 1.
- [ ] Exit codes are documented per failure class (`1` uncaught, `137` OOM-killed, `143` SIGTERM).

## Related

- [Memory, Stack, and Descriptor Exhaustion (41.3–41.6)](./02-memory-stack-and-descriptor-exhaustion.md)
- [Node.js: Uncaught Rejection Handling and Graceful Shutdown](../03-practical-examples/01-node-uncaught-rejection-and-graceful-shutdown.md)
- [Async Propagation and Unhandled Rejections](../../../part-05-exception-mechanics/12-exception-propagation-and-control-flow/02-deep-dive/02-async-propagation-and-unhandled-rejections.md)
- [Async Cleanup and Detached Failures](../../../part-12-async-and-background-jobs/31-asynchronous-error-handling/01-concepts/05-async-cleanup-and-detached-failures.md)
