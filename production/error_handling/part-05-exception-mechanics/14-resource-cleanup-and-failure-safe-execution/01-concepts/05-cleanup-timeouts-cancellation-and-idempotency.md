# Cleanup Timeouts, Cancellation, and Idempotency

> Part V · Chapter 14 · Sections 14.14, 14.15, 14.16, 14.17, 14.18 · _Estimated reading time: 17 min_
> **Prerequisite:** [Multiple Errors and Primary Preservation](./04-multiple-errors-and-primary-preservation.md)

## In one sentence

Cleanup is itself an operation with a **deadline**, must be **safe under cancellation**, must be
**idempotent** (safe to run twice), must **prevent leaks** at the design level, and should follow
one **universal policy** across the codebase.

## Why this matters in production

A cleanup that hangs is as bad as no cleanup: it holds a request slot, blocks a shutdown, or
delays a deploy. A cleanup that only runs when not cancelled leaves resources behind precisely when
the system is under stress. A cleanup that assumes it runs once breaks under retry or duplicate
delivery. Treating cleanup as a first-class operation with a budget is what makes "always release"
actually true.

## Core concept

| Requirement | Why | Mechanism |
| ----------- | --- | --------- |
| **Cleanup timeout** (14.14) | A hung cleanup blocks shutdown/request | Separate short deadline |
| **Cancellation-safe** (14.15) | Cleanup must run after cancel/timeout | Detached context / `finally` |
| **Idempotent cleanup** (14.16) | May run twice (retry, double close) | No-op if already released |
| **Prevent leaks by design** (14.17) | Habitual cleanup forgets | Scoped ownership |
| **Universal policy** (14.18) | Consistency | One rule for all resources |

### Cleanup timeouts (14.14)

Cleanup gets its own **short deadline**, independent of the request deadline that already expired.
If the request timed out, the cleanup deadline is *not* already exhausted — otherwise cleanup is
cancelled before it starts. Use a fresh context with a small budget (e.g. 2–5s).

### Cancellation-safe cleanup (14.15)

When the caller cancels (client disconnect, shutdown, timeout), the request's context is cancelled.
If cleanup uses that same context, it is cancelled too and the resource leaks. Cleanup must use a
**detached context** (or synchronous release) so it runs regardless.

### Idempotent cleanup (14.16)

Cleanup may be invoked twice: once inline and once by a deferred/sweeper path, or after a retry.
Make it a no-op when already released (`if alreadyClosed return`, `defer` after a `sync.Once`,
`ON CONFLICT DO NOTHING` for temp records).

### Preventing leaks (14.17)

Design-level leak prevention beats cleanup discipline:
- **Pooled + scoped** resources (request-scoped connection from a pool).
- **Ownership rules**: the acquirer releases.
- **Sweepers** for unavoidable cases (crashes).
- **Bounded timeouts** so a stuck holder cannot block forever.

### Universal cleanup policy (14.18)

Write it once: *"Every acquired resource is released by its acquirer, in the same scope, with a
bounded independent deadline, idempotently, on every exit path, and cleanup failures are attached
as suppressed."* Apply to every project.

## How it works (mechanics)

### Detached cleanup context

```go
func handler(ctx context.Context) error {
    conn, err := pool.Acquire(ctx)
    if err != nil {
        return err
    }
    defer func() {
        // Fresh context with a short budget, NOT the (possibly cancelled) request ctx.
        cctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
        defer cancel()
        if cerr := conn.Release(cctx); cerr != nil {
            log.Warn("release failed", "err", cerr)
        }
    }()
    return doWork(ctx, conn)
}
```

```ts
// TS: use a fresh AbortController for cleanup, not the request signal.
try {
  return await work(req.signal);
} finally {
  const cleanupCtrl = new AbortController();
  const t = setTimeout(() => cleanupCtrl.abort(), 3000);
  try {
    await resource.release(cleanupCtrl.signal);
  } finally {
    clearTimeout(t);
  }
}
```

### Idempotent release

```java
final class OnceConnection implements AutoCloseable {
    private final AtomicBoolean closed = new AtomicBoolean();
    private final Connection conn;
    OnceConnection(Connection c) { this.conn = c; }
    public void close() {
        if (closed.compareAndSet(false, true)) {   // only the first caller closes
            conn.close();
        }
    }
}
```

### Bounded cleanup during shutdown

```text
shutdown signal
  └─ stop accepting new work
  └─ wait up to D for in-flight work
  └─ run cleanup with its own short deadline
  └─ if cleanup exceeds deadline: log, exit (do not hang forever)
```

## Worked example

Acme's worker on SIGTERM:

```go
func (w *Worker) Run(ctx context.Context) error {
    ctx, stop := signal.NotifyContext(ctx, syscall.SIGTERM, syscall.SIGINT)
    defer stop()

    for {
        select {
        case <-ctx.Done():
            return w.shutdown()           // bounded cleanup below
        case job := <-w.queue:
            if err := w.process(ctx, job); err != nil {
                w.recordFailure(job, err) // job errors are attached, not fatal to the loop
            }
        }
    }
}

func (w *Worker) shutdown() error {
    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()
    var errs []error
    if err := w.db.Close(ctx); err != nil {      // idempotent close
        errs = append(errs, fmt.Errorf("db close: %w", err))
    }
    if err := w.tmpSweeper.Flush(ctx); err != nil { // best-effort
        errs = append(errs, fmt.Errorf("sweep: %w", err))
    }
    return errors.Join(errs...)
}
```

## Key data / numbers

- **Kubernetes**: default `terminationGracePeriodSeconds: 30`; cleanup must fit inside it or the pod
  is `SIGKILL`ed.
- **Cleanup deadline**: commonly 2–5s per request-level release; 10–30s for shutdown.
- **`context.WithTimeout(context.Background(), …)`** is the standard detached-cleanup pattern in Go.
- **HTTP client close**: ensure `resp.Body.Close()` runs regardless of status; not closing leaks the
  connection from the pool.

## Real-world use case — Acme SaaS

Acme's API released its DB connection using the request context. On any request timeout, that
context was already cancelled, so the release call returned immediately with `context canceled` and
the connection was never returned. Under a wave of slow requests, the pool drained and the API
went fully down. Switching cleanup to a detached 3-second context fixed the leak; timeouts now
recover instead of cascading.

## Trade-offs

| Choice | Pros | Cons | When |
| ------ | ---- | ---- | ---- |
| Request context for cleanup | Simple | Cancelled means no cleanup | ❌ |
| Detached short deadline | Always runs; bounded | Slightly more code | Default |
| Synchronous cleanup | Deterministic | Can block the caller | Fast releases |
| Sweeper-only cleanup | Robust to crashes | Delayed; more infra | Backstop always |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give cleanup its own short deadline | Reuse the expired request deadline |
| Use a detached context for cleanup | Let cancellation skip cleanup |
| Make release idempotent | Assume release runs exactly once |
| Bound shutdown cleanup | Hang forever on a stuck close |
| Write one cleanup policy | Improvise per resource |

## Common mistakes

- **Cleanup on the cancelled request context** — the most common leak-on-timeout bug.
- **Unbounded cleanup** — a hung close blocks shutdown past `terminationGracePeriod`.
- **Non-idempotent close** — a second close throws and (if inline) hides the primary.
- **No sweeper** — a crash leaves resources forever.
- **Assuming exactly-once cleanup** — duplicate delivery/retry calls it twice.

## Checklist

- [ ] Cleanup uses a detached, bounded context.
- [ ] Release is idempotent.
- [ ] Shutdown cleanup fits inside the grace period.
- [ ] A sweeper exists for crash residue.
- [ ] One written universal cleanup policy is applied everywhere.

## Related

- [Acquire/Release and Guaranteed Cleanup](./01-acquire-release-and-guaranteed-cleanup.md)
- [Locks, Semaphores, and Temporary Resources](./03-locks-semaphores-and-temporary-resources.md)
- [Timeouts, Circuit Breakers, and Bulkheads (Part XI)](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Process, Runtime, and Resource Failures (Part XV)](../../../part-15-distributed-failures/41-process-runtime-and-resource-failures/README.md)
