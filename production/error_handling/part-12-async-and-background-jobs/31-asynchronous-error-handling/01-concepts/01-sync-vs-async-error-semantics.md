# Sync vs Async Error Semantics

> Part XII · Chapter 31 · Sections 31.1–31.3 · _Estimated reading time: 16 min_
> **Prerequisite:** [Error, Fault, Failure, and Exception](../../../part-01-foundations/01-understanding-errors-and-failures/01-concepts/01-error-fault-failure-exception.md)

## In one sentence

In synchronous code an error **unwinds the stack** to a `catch`; in asynchronous code an error is a
**value delivered later to a handler**, and if no handler is attached it becomes an unhandled
rejection that the call site never sees.

## Why this matters in production

A payment API that returns `202 Accepted` and enqueues work has already told the client "success."
If the asynchronous half then fails and nobody attached a handler, the customer believes they are
paid up while the invoice never generates. The failure is **detached from the request that caused
it**, so it does not appear in the request's logs, its trace, or its error rate. Detached failures
are the most expensive class of async bug because they are invisible until a user complains.

## Sync vs async: the same error, two contracts

```text
SYNC                                  ASYNC (promise)
─────                                 ───────────────
call()                                const p = call()
  │                                     │ returns immediately
  ├─ work ──▶ throws ──▶ unwind         │ work continues later
  │                     to catch        ├─ resolves ──▶ .then(handler)
  ▼                                     └─ rejects  ──▶ .catch(handler)
caller is blocked until done                    caller already moved on
error cannot be ignored                         error is ignored unless handled
```

| Property | Synchronous | Asynchronous (promise/future) |
| -------- | ----------- | ----------------------------- |
| Who observes the error | The caller, immediately | Whoever holds the promise |
| Default if unhandled | Process-level uncaught exception | **Unhandled rejection** (may or may not crash) |
| Ordering | Deterministic, in-stack | Event-loop / scheduler dependent |
| Context | Stack trace includes the caller | Stack trace often starts at the async boundary |
| Cancellation | Not a concept (except signals) | First-class (abort, cancel, timeout) |

**The key shift:** a promise is a *value* representing a future outcome. Throwing inside a `.then`
handler does not throw to the function that created the promise; it rejects the *next* promise in
the chain. The error travels along the promise graph, not the call stack.

## 31.1 — Sync vs async semantics in practice

```ts
function syncCharge(): void {
  throw new Error("card declined"); // caller MUST catch or crash
}

function asyncCharge(): Promise<void> {
  return gateway.charge();          // returns a promise; nothing thrown yet
}

try {
  asyncCharge();                    // ❌ try/catch does NOT catch the rejection
} catch (err) {
  // never runs
}
```

To observe the failure you must await it or attach a handler:

```ts
try {
  await asyncCharge();              // ✅ rejection is re-thrown here
} catch (err) {
  log.warn({ err }, "charge failed");
}
```

> ⚠️ **Hazard.** `try { asyncCharge() } catch {}` is a silent-failure generator. The synchronous
> part of `asyncCharge` may throw before the first `await`, but any rejection after an `await` is
> not caught. Always `await` or return the promise.

Languages encode this differently, but the rule is identical:

| Language | Async value | Error arrives via | Unhandled default |
| -------- | ----------- | ----------------- | ----------------- |
| JavaScript/TypeScript | `Promise<T>` | rejection → `.catch` / `await` | `unhandledRejection` event |
| Python | `Coroutine` / `Task` | exception raised at `await` | "Task exception was never retrieved" |
| Go | goroutine + `chan error` | explicit channel / `errgroup` | silent unless you read it |
| Kotlin | `Deferred<T>` | exception on `await` | propagates to parent scope |
| Rust | `Future<Output = Result<T,E>>` | the `Result` itself | must be polled; `#[must_use]` |

## 31.2 — Unhandled rejections

An **unhandled rejection** is a rejected promise whose rejection has not been handled by the end of
the microtask turn. What happens next is runtime-specific and this is where teams get burned:

- **Node.js ≥ 15** defaults to `--unhandled-rejections=throw`, which raises an uncaught exception
  and **terminates the process** unless a handler is installed.
- **Browsers** fire an `unhandledrejection` event and continue; the failure is easy to miss.
- **Python asyncio** logs "Task exception was never retrieved" when the task is garbage-collected,
  which can be much later, with a mangled traceback.

```ts
// A detached promise: created, never awaited, never caught.
function sendReceipt(orderId: string): void {
  mailer.send(orderId); // returns a promise; rejection is unowned
}

// Detection at the process boundary (last resort, not a strategy).
process.on("unhandledRejection", (reason, promise) => {
  log.error({ reason, promise }, "unhandled rejection — investigate");
  // Do NOT swallow: exit non-zero in a worker so the supervisor restarts cleanly.
});
```

Process-level handlers are an **alarm**, not error handling. They tell you a promise escaped your
design; they cannot tell you which business operation was lost.

## 31.3 — Propagation across async boundaries

Every `await`, `.then`, callback handoff, queue boundary, or worker hop is a place where the error
must be *carried explicitly*. The three patterns:

### Pattern A — await through the chain (preserves cause)

```ts
async function exportRows(job: ExportJob): Promise<void> {
  const rows = await db.streamRows(job.query); // rejection propagates up
  await s3.putObject(job.key, rows);           // rejection propagates up
}
```

This is the **default** and the correct choice whenever the caller can act on the failure.

### Pattern B — wrap with context at the boundary

```ts
try {
  await exportRows(job);
} catch (err) {
  throw new ExportFailed(job.id, job.tenantId, { cause: err });
}
```

Preserve the original as `cause`; never replace it with a string.

### Pattern C — cross a process boundary (serialize, do not throw)

```ts
type JobFailure = {
  code: string;          // stable machine-readable code
  message: string;       // safe, human-readable
  retryable: boolean;    // the receiver needs this decision
  attempt: number;
  context: Record<string, unknown>;
};

// The worker cannot "throw" across SQS. It writes a failure record and
// decides ack/nack based on `retryable`.
await storeJobFailure(job.id, toJobFailure(err));
```

Once work crosses a queue, an event bus, or a webhook, **the error must become data**. Exceptions
do not survive serialization; codes and metadata do.

## Worked example — Acme SaaS export request

Acme's API accepts `POST /exports` and returns `202` with a job id. If the worker fails, the API
request's trace has long ended.

```ts
// API boundary — cannot observe worker failure
app.post("/exports", async (req, res) => {
  const job = await queue.enqueue("ExportJob", { tenantId: req.tenant.id });
  res.status(202).json({ jobId: job.id });
});

// Worker boundary — owns the failure
worker.process("ExportJob", async (job) => {
  try {
    await exportRows(job.data);
  } catch (err) {
    await job.recordFailure({
      code: classifyExportError(err),
      retryable: isRetryable(err),
      attempt: job.attempts,
      context: { tenantId: job.data.tenantId, objectKey: job.data.key },
    });
    throw err; // let the queue decide retry vs DLQ
  }
});
```

The fix is not to "catch and log." The fix is to make the worker the **owner** of the failure and
to persist enough data that the client can poll `GET /exports/:id` and see `failed`.

## Key data / numbers

- Node.js 15+ default: unhandled rejection → **process exit** (`--unhandled-rejections=throw`).
- Python: `Task exception was never retrieved` is emitted at task GC, not at failure time.
- Go: an error written to an unbuffered channel with no reader blocks the goroutine forever.
- Typical queue visibility timeout starts at **30 s** (SQS default); async work must fit or extend it.
- Microtask vs macrotask: promise callbacks run before timers, so ordering bugs compound failures.

## Real-world use case — Checkout

Checkout captures payment synchronously but emails the receipt asynchronously. The email call was
fired with `void sendReceipt()` and no `.catch`. When the mail provider returned `429`, the
rejection was unhandled; the process logged a warning and continued. Customers paid but received no
receipt for two days. The fix: enqueue a `SendReceipt` job with retries instead of detaching a
promise, and make "receipt sent" a visible job state.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| `await` and propagate | Simple, preserves cause | Caller must handle | Caller can act |
| Fire-and-forget with `.catch` | Non-blocking | No durability; lost on crash | Truly optional telemetry only |
| Enqueue a job | Durable, retryable, observable | Adds infrastructure | Any work that must happen |
| Process-level handler only | Catches everything | Too late; no business context | Last-resort alarm |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| `await` or return every promise you create | Wrap an async call in `try/catch` without `await` |
| Attach `.catch` to intentionally detached work | Use `void promise` to silence the linter |
| Convert errors to data at queue/event boundaries | Throw across serialization boundaries |
| Preserve the original `cause` when wrapping | Replace an error with a log line |
| Exit non-zero on unhandled rejection in workers | Swallow it and keep the process alive |

## Common mistakes

- **`try/catch` around a promise call.** The rejection happens after the `try` block exits; only
  `await` re-enters the catch.
- **`.then(fn)` without `.catch`.** A rejection in `fn` is silently forwarded to an unobserved
  promise.
- **`forEach(async …)`.** The callbacks are detached; the surrounding function returns before they
  finish. Use `for…of` with `await` or `Promise.all`.
- **Losing the stack across an async boundary.** Node truncates async stacks; attach the causal
  error (`{ cause }`) at the boundary.
- **Assuming a 202 means success.** It means *accepted*; the job can still fail later.

## Checklist

- [ ] Is every promise either awaited, returned, or given an explicit `.catch` owner?
- [ ] Do worker processes exit non-zero on unhandled rejection?
- [ ] Is there a process-level handler that alerts (not swallows)?
- [ ] Are failures converted to serializable records before crossing a queue/event boundary?
- [ ] Does the API expose a job status endpoint for work that outlives the request?
- [ ] Are `forEach(async …)` and bare `void promise` banned by lint rule?

## Related

- [Concurrent Failures and Aggregation](./02-concurrent-failures-and-aggregation.md)
- [Detached Failures and Async Context](../02-deep-dive/03-detached-failures-and-async-context.md)
- [Chapter 12 — Exception Propagation and Control Flow](../../../part-05-exception-mechanics/12-exception-propagation-and-control-flow/README.md)
- [Chapter 32 — Background Jobs](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
