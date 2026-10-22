# Async Cleanup, Detached Failures, and Conventions

> Part XII · Chapter 31 · Sections 31.14–31.16 · _Estimated reading time: 16 min_
> **Prerequisite:** [Cancellation, Timeouts, and Event-Driven Errors](./03-cancellation-timeouts-and-events.md)

## In one sentence

**Cleanup must run on every exit path** — success, failure, timeout, and cancellation — and a
**detached failure** is a promise or task you started but no longer own; eliminate it or attach an
owner, then codify the rules so the next engineer cannot reintroduce it.

## Why this matters in production

Cleanup bugs leak file handles, temp objects, DB connections, and distributed locks. They rarely
fail loudly; they show up hours later as pool exhaustion or a tenant whose export never runs because
a lock was never released. Detached failures are worse: they silently drop work. Both are
*conventions* problems — the language will not stop you, so your team's standard must.

## 31.14 — Async cleanup

Use `try/finally` (or the language equivalent) so cleanup runs on rejection too:

```ts
const lock = await locks.acquire(`export:${job.tenantId}`, { ttlMs: 60_000 });
try {
  await exportRows(job);
} finally {
  await lock.release(); // runs on success, throw, timeout, and abort
}
```

### Cleanup rules

1. **Idempotent cleanup.** Releasing an already-released lock or deleting a missing temp file must
   be a no-op, because cleanup can itself be retried.
2. **Cleanup must not mask the primary error.** If cleanup throws, log it; do not replace the
   original failure.
3. **Bound cleanup time.** Cleanup can hang too; give it its own short timeout.
4. **Cancellation-safe cleanup.** Do not pass the cancelled signal to the cleanup call, or it will
   abort immediately. Use a fresh short signal.
5. **Order matters.** Release locks *after* the state that they protect is durably written, but
   *before* you leave the process.

```ts
try {
  await doWork(signal);
} finally {
  await withTimeout(cleanup(), 2_000).catch((err) =>
    log.error({ err }, "cleanup failed"),   // never throw from cleanup
  );
}
```

### Multi-resource cleanup

When several resources are acquired, release in reverse order and attempt **all** of them:

```ts
const releases: Array<() => Promise<void>> = [];

try {
  releases.push(await openFile());
  releases.push(await beginTransaction());
  await work();
} finally {
  for (const release of releases.reverse()) {
    await release().catch((err) => log.error({ err }, "release failed"));
  }
}
```

Languages with scoped cleanup (`defer` in Go, `with` in Python, `using` in C#, Kotlin's `use`) are
preferred because they cannot be forgotten.

## 31.15 — Preventing detached failures

A **detached failure** is work whose outcome nobody observes: a fire-and-forget promise, a goroutine
whose error channel is never read, a Python task whose exception is never retrieved, a callback
invoked after the request ended.

### How to detect them

| Signal | Likely cause |
| ------ | ------------ |
| `unhandledRejection` / "task exception was never retrieved" | Missing `.catch` / unread task |
| Response returns before side effect completes | `void promise` / un-awaited call |
| Work continues after client disconnect | No cancellation propagation |
| Errors appear only in process logs, not request traces | Async context not propagated |
| Goroutine count grows without bound | Blocked send on an unread channel |

### How to prevent them

**Rule 1 — Every spawned task has an owner.** If it cannot be awaited, it must have a `.catch` that
records a terminal outcome:

```ts
function spawn(name: string, fn: () => Promise<void>): void {
  fn().catch(async (err) => {
    await failureStore.record({ scope: name, error: serialize(err) });
    log.error({ err, scope: name }, "background task failed");
  });
}
```

**Rule 2 — Prefer durable queues over in-process detachment.** A promise dies with the process; an
enqueued job survives it.

**Rule 3 — Propagate async context.** Use `AsyncLocalStorage` (Node), `contextvars` (Python), or
`context.Context` (Go) so late failures still carry tenant/request/tenant IDs.

```ts
import { AsyncLocalStorage } from "node:async_hooks";
const requestContext = new AsyncLocalStorage<{ requestId: string; tenantId: string }>();

requestContext.run({ requestId: req.id, tenantId: req.tenant.id }, () => handle(req));
```

**Rule 4 — Shut down the process correctly.** On `SIGTERM`, stop accepting work, await in-flight
tasks up to a grace period, then exit. Do not let detached tasks die mid-write.

## 31.16 — Conventions

Write these down once and enforce them with lint/review. A sample standard:

| Convention | Rule |
| ---------- | ---- |
| Promise handling | Every promise is `await`ed, `return`ed, or passed to `spawn()` with a handler |
| Fire-and-forget | Banned except via `spawn()`; `void promise` is a lint error |
| `forEach(async …)` | Banned; use `for…of` + `await` or `Promise.all` |
| Cancellation | Every I/O function accepts `signal`/`ctx` as its last parameter |
| Timeouts | Every external call takes a deadline from the boundary; no bare constant timeouts deep in code |
| Aggregation | `Promise.all` only when all results are required; otherwise `allSettled` + typed result |
| Cleanup | `try/finally` or scoped resource; cleanup is idempotent and time-bounded |
| Error conversion | Convert to a serializable `JobFailure`/`EventFailure` at queue/event boundaries |
| Terminal states | Every async operation ends in `succeeded`, `failed`, `cancelled`, or `timed_out` |

Conventions only work if they are **mechanical**:

```json
{
  "rules": {
    "no-floating-promises": "error",
    "no-misused-promises": "error",
    "require-await": "warn"
  }
}
```

> ⚠️ **Hazard.** "Be careful with promises" is not a convention. If the linter cannot detect it and
> the reviewer cannot point to a rule, it will regress within a quarter.

## Worked example — Acme export cleanup and spawn

Acme's `ExportJob` acquired a distributed lock and wrote to a temp S3 key. A timeout path skipped
`finally`, leaking the lock for 24 hours; the next scheduled export found the lock held and exited
**successfully without exporting anything**.

```ts
const lock = await locks.acquire(`export:${tenantId}`, { ttlMs: 60_000 });
const tempKey = `tmp/${job.id}.csv`;

try {
  await pipeline(queryRows(signal), toCsv(), s3.write(tempKey, { signal }));
  await s3.copy(tempKey, finalKey);
} catch (err) {
  await s3.delete(tempKey).catch(() => {});
  throw err;
} finally {
  await lock.release().catch((e) => log.error({ e }, "lock release failed"));
}
```

The lock is now released on every path; a failed export is marked `failed` rather than a false
`succeeded`.

## Key data / numbers

- Node `AsyncLocalStorage` (stable since v16) propagates context across promises and timers.
- `SIGTERM` → Kubernetes default `terminationGracePeriodSeconds` is **30 s**; your in-flight grace
  must be shorter.
- Typical distributed lock TTLs: 30–60 s with renewal; a leaked lock can block a tenant for the full
  TTL.
- `unhandledRejection` listeners should **exit non-zero** in workers so the supervisor restarts a
  clean process.
- Cleanup budget recommendation: reserve **10–20%** of the operation deadline for teardown.

## Real-world use case — Acme SaaS

Acme's notification service used `events.on("user.created", async () => sendWelcome())`. A provider
outage caused rejections that terminated listeners silently; welcome emails stopped for a week with
no alert. The fix: replace the in-process emitter with a durable `SendWelcome` job, add `spawn()`
with an `unhandledRejection` alarm, and add a lint rule banning async emitter listeners without a
wrapper. Detached failures became a tracked metric (`background_task_failed_total`).

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| `try/finally` | Works everywhere | Verbose with many resources | Most code |
| Scoped helpers (`defer`, `using`) | Cannot forget | Language-specific | Preferred where available |
| `spawn()` wrapper | Handler guaranteed | Still in-process, not durable | Telemetry, cache warmup |
| Durable queue | Survives crashes | Infrastructure cost | Work that must happen |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Put cleanup in `finally`/scope guards | Rely on the happy path |
| Make cleanup idempotent and time-bounded | Let cleanup throw or hang |
| Give every spawned task an owner | `void promise` to silence lint |
| Propagate async context | Lose tenant/request IDs at the boundary |
| Enforce rules with lint | Rely on memory and good intentions |

## Common mistakes

- **Cleanup using the cancelled signal** — it aborts instantly, so nothing is released.
- **Cleanup throwing over the primary error** — the real cause disappears from logs.
- **Fire-and-forget writes** — the process exits before the write flushes.
- **Async `EventEmitter` listeners** — rejections bypass the emitter's error handling.
- **No shutdown drain** — in-flight tasks are killed mid-transaction.

## Checklist

- [ ] Does cleanup run on success, failure, timeout, and cancellation?
- [ ] Is cleanup idempotent, error-isolated, and time-bounded?
- [ ] Are resources released in reverse acquisition order?
- [ ] Does every detached task go through a wrapper with a terminal handler?
- [ ] Is async context (request/tenant/job id) propagated to late failures?
- [ ] Are the async conventions documented and lint-enforced?
- [ ] Does shutdown drain in-flight work within a grace period?

## Related

- [Callbacks, Streams, and Reactive Pipelines](./04-callbacks-streams-and-reactive-pipelines.md)
- [Detached Failures and Async Context — Mechanics](../02-deep-dive/03-detached-failures-and-async-context.md)
- [Chapter 14 — Resource Cleanup and Failure-Safe Execution](../../../part-05-exception-mechanics/14-resource-cleanup-and-failure-safe-execution/README.md)
- [Chapter 32 — Worker Failures, Timeouts, and Isolation](../../32-background-jobs-queues-and-scheduled-tasks/01-concepts/04-worker-failures-timeouts-and-isolation.md)
