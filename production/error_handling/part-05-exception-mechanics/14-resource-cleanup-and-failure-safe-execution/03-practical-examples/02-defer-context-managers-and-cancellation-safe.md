# defer, Context Managers, and Cancellation-Safe Cleanup

> Part V · Chapter 14 · Sections 14.10–14.18 (practical) · _Estimated reading time: 22 min_
> **Prerequisite:** [Cleanup Timeouts, Cancellation, and Idempotency](../01-concepts/05-cleanup-timeouts-cancellation-and-idempotency.md)

## In one sentence

This file shows cleanup that survives **panic, cancellation, and timeout** using Go `defer`,
Python `async with`, and detached cleanup contexts, with idempotent release.

## Why this matters in production

The hardest cleanups happen when the system is already unhealthy: a cancelled request, a panicking
worker, a shutdown. This is exactly when a naive cleanup is skipped. The patterns here guarantee
release under those conditions and keep the release itself bounded and idempotent.

## Scenario

**Acme SaaS `AgentRun`** acquires a semaphore permit, a temp workspace, and a distributed lock,
then calls an LLM provider that may time out or be cancelled by the user.

```text
acquire permit ─▶ acquire lock (lease+token) ─▶ create workspace
     └── call provider (ctx may cancel/timeout)
release all three on: success, error, panic, cancel, timeout
```

## Go — `defer` + detached cleanup context

```go
func (r *Runner) Run(ctx context.Context, req AgentRequest) (Result, error) {
    // 1. Semaphore permit, released on every path.
    if err := r.sem.Acquire(ctx, 1); err != nil {
        return Result{}, fmt.Errorf("acquire permit: %w", err)
    }
    defer r.sem.Release(1)                       // panic/cancel safe

    // 2. Distributed lock with lease + fencing token.
    lock, err := r.locks.Acquire(ctx, "agent:"+req.ID, 30*time.Second)
    if err != nil {
        return Result{}, fmt.Errorf("acquire lock: %w", err)
    }
    defer func() {
        // Detached, bounded release: the request ctx may already be cancelled.
        cctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
        defer cancel()
        if lerr := lock.Release(cctx); lerr != nil {
            log.Warn("lock release failed", "err", lerr, "run", req.ID)
        }
    }()

    // 3. Temp workspace, removed on every path.
    ws, err := os.MkdirTemp("", "agent-*")
    if err != nil {
        return Result{}, fmt.Errorf("workspace: %w", err)
    }
    defer func() {
        cctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
        defer cancel()
        if rerr := r.remove(cctx, ws); rerr != nil { // idempotent RemoveAll
            log.Warn("workspace cleanup failed", "err", rerr, "dir", ws)
        }
    }()

    // Panic safety: convert a panic in the provider call into an error + cleanup.
    defer func() {
        if p := recover(); p != nil {
            log.Error("provider panicked", "panic", p, "run", req.ID)
        }
    }()

    return r.callProvider(ctx, req, ws)          // ctx may time out / be cancelled here
}
```

Release order is LIFO: panic-recover, workspace removal, lock release, permit release. Every
release uses a **detached context** so cancellation of the request does not skip cleanup.

## Python — `async with` + `finally`

```python
async def run(req: AgentRequest) -> Result:
    async with semaphore:                          # __aexit__ releases on exception/cancel
        lock = await locks.acquire(f"agent:{req.id}", ttl=30)
        try:
            ws = tempfile.TemporaryDirectory(prefix="agent-")
            try:
                return await call_provider(req, ws.name)   # may raise CancelledError
            finally:
                # Runs even on asyncio.CancelledError.
                await asyncio.shield(sweep(ws.name))       # shield: not cancelled with the task
        finally:
            try:
                await asyncio.shield(lock.release())
            except Exception as e:
                logger.warning("lock release failed: %s", e)
```

`asyncio.shield(...)` protects the release coroutine from the surrounding cancellation — the async
analogue of a detached cleanup context.

## Idempotent release

```ts
class IdempotentLock {
  private released = false;
  async release(): Promise<void> {
    if (this.released) return;          // second call is a safe no-op
    this.released = true;
    await this.redis.eval(RELEASE_SCRIPT, [this.key], [this.token]); // only if token matches
  }
}
```

The Lua script releases only if the stored token equals ours, so a stale holder cannot delete a new
holder's lock.

## Handling shutdown

```go
func (w *Worker) Shutdown(ctx context.Context) error {
    // Bounded by the caller's grace period; each step gets a slice of the budget.
    ctx, cancel := context.WithTimeout(ctx, 20*time.Second)
    defer cancel()

    w.queue.StopAccepting()              // 1. stop new work
    if err := w.drain(ctx); err != nil { // 2. finish in-flight, bounded
        return fmt.Errorf("drain: %w", err)
    }
    var errs []error
    if err := w.db.Close(ctx); err != nil {
        errs = append(errs, fmt.Errorf("db close: %w", err))
    }
    if err := w.sweeper.Flush(ctx); err != nil {
        errs = append(errs, fmt.Errorf("sweep: %w", err))
    }
    return errors.Join(errs...)          // report all shutdown cleanup failures
}
```

## Key data / numbers

- **Go `defer`** runs on panic; register releases immediately after each acquire (LIFO).
- **`context.WithTimeout(context.Background(), d)`** creates a detached cleanup budget; 2–5s per
  release, 10–30s for shutdown.
- **`asyncio.shield`** prevents cleanup from being cancelled with the task.
- **Kubernetes `terminationGracePeriodSeconds`**: default 30s; shutdown cleanup must fit.
- **Redis lock release**: compare-and-delete via Lua; never `DEL` unconditionally.
- **Temp sweeper**: run every few minutes; delete artifacts older than a threshold as a backstop.

## Real-world use case — Acme SaaS

Acme's `AgentRun` released its distributed lock using the request context. When users cancelled
runs (client disconnect), the context was cancelled and the release call returned immediately
without deleting the lock — the lock then blocked new runs for that agent for its full TTL. They
switched to a detached context (Go) / `asyncio.shield` (Python) and made release compare-and-delete
by token. Cancellations stopped leaking locks, and throughput recovered.

## Trade-offs

| Mechanism | Protects against | Caveat |
| --------- | ---------------- | ------ |
| `defer` | panic, normal return | Not `os.Exit`/`SIGKILL` |
| Detached context | request cancellation | Small extra budget needed |
| `asyncio.shield` | task cancellation | Must be awaited, can still fail |
| Idempotent release | double release | Needs a flag/CAS |
| Sweeper | crashes, missed cleanup | Delayed |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Register `defer` right after acquire | Release manually at the end |
| Cleanup with a detached context | Reuse the cancelled request context |
| Use `asyncio.shield` for release | Await release unshielded after cancel |
| Make release idempotent (CAS/token) | `DEL` a lock unconditionally |
| Bound shutdown cleanup | Hang past the grace period |

## Common mistakes

- **Cleanup on the cancelled context** — release is skipped exactly when needed.
- **Releasing a lock without a token check** — deletes a newer holder's lock.
- **Unbounded shutdown** — the process is `SIGKILL`ed mid-cleanup.
- **Assuming `defer` runs on `os.Exit`** — it does not.
- **No sweeper** — crash residue accumulates.

## Checklist

- [ ] Releases registered immediately after acquire (LIFO).
- [ ] Cleanup uses a detached, bounded context (or `shield`).
- [ ] Release is idempotent and token-checked.
- [ ] Shutdown cleanup fits the grace period.
- [ ] A sweeper exists as a backstop.

## Related

- [try/finally and using Patterns](./01-try-finally-and-using-patterns.md)
- [Cleanup Timeouts, Cancellation, and Idempotency](../01-concepts/05-cleanup-timeouts-cancellation-and-idempotency.md)
- [Locks, Semaphores, and Temporary Resources](../01-concepts/03-locks-semaphores-and-temporary-resources.md)
- [Asynchronous Error Handling (Part XII)](../../../part-12-async-and-background-jobs/31-asynchronous-error-handling/README.md)
