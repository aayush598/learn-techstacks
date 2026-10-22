# Chapter 31 — Do's and Don'ts

> Part XII · Chapter 31 · all sections · _Estimated reading time: 8 min_

## In one sentence

Async error handling fails when failures are **unowned** and succeeds when every promise, task, and
stream has a handler, a terminal state, and a deadline.

## The rules

| # | ✅ Do | ❌ Don't |
| - | ----- | -------- |
| 1 | `await` or `return` every promise you create | Wrap an async call in `try/catch` without `await` |
| 2 | Give detached work an owner (`spawn()` with `.catch`) | `void promise` to silence the linter |
| 3 | Route critical detached work to a durable queue | Rely on in-process fire-and-forget |
| 4 | Exit non-zero on unhandled rejection in workers | Swallow it and keep running |
| 5 | Choose fail-fast vs collect-all per operation | Use `Promise.all` everywhere out of habit |
| 6 | Abort siblings when failing fast | Assume `Promise.all` cancels the others |
| 7 | Return typed partial success | Return `200` with silently missing data |
| 8 | Classify per-branch failures with stable codes | Throw one "some items failed" error |
| 9 | Propagate `AbortSignal` / `Context` to every I/O call | Accept the signal and drop it |
| 10 | Compute one deadline at the boundary | Give every hop the full timeout |
| 11 | Keep `cancelled` and `timed_out` distinct from `failed` | Report cancellation as `500` |
| 12 | Use `pipeline()` / `for await` for streams | Use bare `.pipe()` and ignore stage errors |
| 13 | Isolate per-item errors in reactive/stream pipelines | Let one item terminate the shared stream |
| 14 | Run cleanup in `finally` on every exit path | Rely on the happy path |
| 15 | Give cleanup a fresh, short timeout | Pass the aborted signal to cleanup |
| 16 | Track in-flight work and drain on `SIGTERM` | Let shutdown kill mid-write work |
| 17 | Propagate request/tenant/job context | Log late failures without identifiers |
| 18 | Enforce conventions with lint rules | Document "be careful with promises" |

## Anti-patterns with symptoms

### ❌ The floating promise

```ts
mailer.send(email); // promise dropped
```

**Symptom:** emails silently stop; `unhandledRejection` with no request context.
**Fix:** `await`, `return`, or `spawn("send-email", () => mailer.send(email))`.

### ❌ `forEach(async …)`

```ts
items.forEach(async (i) => await process(i)); // returns immediately
```

**Symptom:** handler responds before processing finishes; errors unowned.
**Fix:** `for (const i of items) await process(i)` or `await Promise.all(items.map(process))`.

### ❌ `Promise.race` as a timeout

```ts
await Promise.race([charge(), sleep(5000).then(() => { throw new TimeoutError(); })]);
```

**Symptom:** duplicate charges after retry; provider keeps billing.
**Fix:** `AbortSignal.timeout()` passed into `charge()`.

### ❌ `catchError(() => of(null))`

```ts
source$.pipe(catchError(() => of(null))); // failure becomes success
```

**Symptom:** required data renders as empty; no error metric.
**Fix:** recover only for optional paths; otherwise rethrow after logging.

### ❌ Orphaned stream stages

```ts
readable.pipe(transform).pipe(writable); // errors not forwarded
```

**Symptom:** truncated output marked as success.
**Fix:** `await pipeline(readable, transform, writable)`; commit only after completion.

### ❌ Cleanup on the cancelled signal

```ts
finally { await releaseLock(signal); } // aborts instantly
```

**Symptom:** distributed locks held for their full TTL; next run no-ops.
**Fix:** cleanup with a fresh 2 s timeout signal.

## Code-review questions

1. Where is the `.catch` for this promise, and who owns the terminal outcome?
2. If this fails, do the sibling tasks stop?
3. Is this fan-out fail-fast or collect-all, and why?
4. Does cancellation reach the provider call or only this `await`?
5. What is the total deadline, and does each hop get the remaining budget?
6. Is successful work persisted before a partial-success response?
7. Does cleanup run on abort, and with which signal?
8. Does the error carry tenant/job/request context?

## Minimal lint configuration

```json
{
  "rules": {
    "no-floating-promises": "error",
    "no-misused-promises": "error",
    "await-thenable": "error",
    "require-await": "warn"
  }
}
```

For Python, enable `asyncio` checks in your linter and ban bare `except Exception` around awaited
calls. For Go, require `defer cancel()` after every `context.WithTimeout`.

## Related

- [Sync vs Async Error Semantics](./../01-concepts/01-sync-vs-async-error-semantics.md)
- [Async Cleanup, Detached Failures, and Conventions](./../01-concepts/05-async-cleanup-and-detached-failures.md)
- [Chapter 31 Reference](../05-reference/README.md)
- [Chapter 33 — Event Do's and Don'ts](../../33-events-webhooks-and-message-processing/04-dos-and-donts/README.md)
