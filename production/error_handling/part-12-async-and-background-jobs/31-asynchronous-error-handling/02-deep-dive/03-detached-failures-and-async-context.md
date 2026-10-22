# Detached Failures and Async Context — Mechanics

> Part XII · Chapter 31 · Sections 31.2, 31.15 (mechanics) · _Estimated reading time: 15 min_
> **Prerequisite:** [Async Cleanup, Detached Failures, and Conventions](../01-concepts/05-async-cleanup-and-detached-failures.md)

## In one sentence

A detached failure is **work whose rejection has no observer**, and the fix is twofold: give every
task an owner and carry **async context** (request, tenant, job, trace) across the boundary so the
eventual failure is attributable.

## Why this matters in production

Detached failures are invisible in the request's error rate because they happen after the response.
They surface later as "batch stopped processing," "emails stopped," or a growing goroutine count.
Context loss makes them worse: the error log says `TypeError: cannot read property 'id' of
undefined` with no tenant, no job, and no request id. You cannot page the right team or replay the
right work.

## Anatomy of a detached failure

```text
request ──▶ spawn(promise) ──▶ response sent (200)
                 │
                 ├─ promise rejects later
                 │       │
                 │       └─ no .catch  ──▶ unhandledRejection
                 │                           │
                 │                           └─ process-level handler
                 │                               (no business context)
                 └─ context lost at the spawn boundary
```

Three components:

1. **Spawn** — work starts without an `await`/return path.
2. **Loss of ownership** — no handler decides the terminal outcome.
3. **Loss of context** — tenant/request/job ids are not carried into the async continuation.

## Detection mechanisms per runtime

| Runtime | Event / symptom | Notes |
| ------- | --------------- | ----- |
| Node.js | `process.on("unhandledRejection")` | Node 15+ default exits on unhandled rejection |
| Browsers | `window.onunhandledrejection` | Does not crash the page; easy to miss |
| Python | "Task exception was never retrieved" | Logged at GC, often minutes later |
| Go | goroutine leak / blocked send | `runtime.NumGoroutine()` growth; `pprof` |
| Java | `CompletableFuture` never joined | No default handler; result silently dropped |
| Kotlin | uncaught `CoroutineExceptionHandler` | Only root coroutines invoke it |

### Node example with context

```ts
process.on("unhandledRejection", (reason) => {
  const ctx = requestContext.getStore(); // may be undefined at process level
  log.fatal({ reason, ctx }, "unhandled rejection — exiting");
  process.exitCode = 1;
  server.close(() => process.exit(1));
});
```

Exiting is deliberate: a process with an unknown detached failure may be in an inconsistent state.
Let the supervisor restart it and let the queue redeliver the message.

## Async context propagation

Context is the set of identifiers you want on every log/error: `requestId`, `tenantId`, `jobId`,
`traceId`, `attempt`. It must survive `await`, timers, and callbacks.

### Node — `AsyncLocalStorage`

```ts
import { AsyncLocalStorage } from "node:async_hooks";

type Ctx = { requestId: string; tenantId: string; jobId?: string };
export const ctxStore = new AsyncLocalStorage<Ctx>();

export function withContext<T>(ctx: Ctx, fn: () => Promise<T>): Promise<T> {
  return ctxStore.run(ctx, fn);
}

// Late failure still knows the tenant:
setTimeout(() => {
  try { risky(); }
  catch (err) { log.error({ err, ctx: ctxStore.getStore() }, "late failure"); }
}, 5_000);
```

### Python — `contextvars`

```python
import contextvars, asyncio

request_id = contextvars.ContextVar("request_id")

async def handle(req):
    token = request_id.set(req.id)
    try:
        await do_work()
    finally:
        request_id.reset(token)  # tasks copy context; reset in the owning task
```

Each `asyncio.Task` copies the current context at creation. Values set *inside* a task do not leak
back to the parent, which is usually what you want.

### Go — explicit `context.Context`

```go
type ctxKey string
const tenantKey ctxKey = "tenant"

func withTenant(ctx context.Context, id string) context.Context {
    return context.WithValue(ctx, tenantKey, id)
}

func worker(ctx context.Context) {
    tenant, _ := ctx.Value(tenantKey).(string)
    // tenant available for the whole call tree
}
```

Go prefers explicit passing over ambient storage; values should be request-scoped metadata, never
optional parameters.

## The owner wrapper

Standardize detached tasks through one function so no call site can forget:

```ts
export function spawn(
  name: string,
  fn: (ctx: Ctx) => Promise<void>,
  ctx: Ctx = ctxStore.getStore() ?? { requestId: "unknown", tenantId: "unknown" },
): void {
  void withContext(ctx, async () => {
    try {
      await fn(ctx);
    } catch (err) {
      await failureStore.record({
        scope: name,
        requestId: ctx.requestId,
        tenantId: ctx.tenantId,
        code: classify(err),
        error: serialize(err),
      });
      log.error({ err, ctx, scope: name }, "detached task failed");
    }
  });
}
```

The wrapper guarantees: context carried, failure recorded, error logged, and the promise observed.
It is still in-process, so use it only for non-critical work (cache warmup, telemetry). Critical
work belongs on a durable queue (Chapter 32).

## Shutdown and draining

Detached tasks must be awaited before exit:

```ts
const inflight = new Set<Promise<unknown>>();

export function track<T>(p: Promise<T>): Promise<T> {
  inflight.add(p);
  p.finally(() => inflight.delete(p));
  return p;
}

async function shutdown() {
  server.close();
  const grace = new Promise((r) => setTimeout(r, 25_000));
  await Promise.race([Promise.allSettled([...inflight]), grace]);
  process.exit(0);
}
```

Without tracking, `SIGTERM` kills the process and the promise disappears mid-write.

## Worked example — Acme notification fan-out

Acme fired welcome emails with `void mailer.send(...)`. When the provider returned `429`, the
rejection was unhandled; Node logged it, but the tenant id was absent because the promise had lost
the request context. Support could not tell which customers were affected.

```ts
// Before
void mailer.send(user.email, template); // no owner, no context

// After — durable job, not detached
await queue.enqueue("SendWelcome", {
  tenantId: user.tenantId,
  userId: user.id,
  requestId: ctxStore.getStore()?.requestId,
});
```

The job carries context in its payload and is retried by the queue. There is no detached promise
left to fail silently.

## Key data / numbers

- Node 15+ exits on unhandled rejection by default; Node 14 logged and continued.
- `AsyncLocalStorage` has small per-context overhead; it is stable since Node 16.
- Python tasks copy `contextvars` at creation; mutations inside a task do not propagate outward.
- Kubernetes `terminationGracePeriodSeconds` default 30 s; set drain shorter (e.g. 25 s).
- `runtime.NumGoroutine()` climbing under steady load is an early goroutine-leak signal.

## Real-world use case — ExportJob

Acme's export worker spawned a detached "cleanup old exports" promise on every job. Under load the
promises accumulated; a failure inside one left a temp object forever. Because the spawn happened
without context, the failure log had no job id. Replacing the detached promise with a scheduled job
(Chapter 32) made cleanup observable, retryable, and attributable.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Bare `void promise` | None | Unobservable, unbounded | Never |
| `spawn()` wrapper | Context + handler | Still in-process | Telemetry, cache |
| Durable queue job | Survives crashes, replayable | Infrastructure | Work that must happen |
| `AsyncLocalStorage` | Zero-arg context | Runtime-specific | Request-scoped metadata |
| Explicit context args | Clear, portable | Verbose | Go, cross-service APIs |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Route every detached task through an owner wrapper | `void promise` anywhere |
| Propagate tenant/request/job context | Log errors without identifiers |
| Track in-flight work and drain on shutdown | Let `SIGTERM` kill mid-write |
| Exit non-zero on unhandled rejection in workers | Continue in an unknown state |
| Prefer durable jobs for critical work | Rely on in-process promises |

## Common mistakes

- **Assuming `unhandledRejection` is error handling.** It is a last-resort alarm with no context.
- **Context set inside a child task leaking to the parent** — in Python it does not; in Node it is
  ambient per async resource, which can surprise you.
- **Draining without allSettled** — `Promise.all` rejects and skips waiting for the rest.
- **Spawn loops with no cap** — detach thousands of tasks and exhaust the pool.
- **Treating shutdown as instant** — no grace means partial writes.

## Checklist

- [ ] Is every detached task routed through a single owner wrapper?
- [ ] Does the wrapper record context and a terminal outcome?
- [ ] Is context propagated with `AsyncLocalStorage`/`contextvars`/`context.Context`?
- [ ] Are in-flight tasks tracked and drained on `SIGTERM`?
- [ ] Do workers exit non-zero on unhandled rejection?
- [ ] Is critical work on a durable queue rather than a detached promise?
- [ ] Is goroutine/task growth monitored?

## Related

- [Async Cleanup, Detached Failures, and Conventions](../01-concepts/05-async-cleanup-and-detached-failures.md)
- [Sync vs Async Error Semantics](../01-concepts/01-sync-vs-async-error-semantics.md)
- [Chapter 32 — Worker Failures, Timeouts, and Isolation](../../32-background-jobs-queues-and-scheduled-tasks/01-concepts/04-worker-failures-timeouts-and-isolation.md)
- [Chapter 32 — Background Jobs](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
