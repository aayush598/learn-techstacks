# Graceful Shutdown Sequencing with SIGTERM (41.14–41.15)

> Part XV · Chapter 41 · Sections 41.14–41.15 (mechanics) · _Estimated reading time: 24 min_
> **Prerequisite:** [Initialization, Startup, and Shutdown (41.10–41.18)](../01-concepts/04-initialization-startup-and-shutdown.md)

## In one sentence

Graceful shutdown is a **phased protocol with a deadline**, not a single handler: *leave the load
balancer → stop intake → drain in-flight work → flush → release → exit*, in that order, every
step bounded, and every failure reported rather than skipped.

## Why this matters in production

Every deploy sends `SIGTERM` to every pod. If your shutdown path is a single `close()` call, then
**every deploy is a small, scheduled, self-inflicted outage** — and because it is scheduled and
uniform, it hides in the noise of "we deploy 30 times a day".

The failures are always in the same three places:

1. **Ordering.** Closing the server before the load balancer has stopped routing to it turns a
   graceful stop into a burst of `502`s; closing the database pool before the workers finished their
   in-flight writes turns it into lost work.
2. **Deadlines.** A drain without a deadline never ends, the orchestrator escalates to `SIGKILL`,
   and you lose everything the drain was protecting.
3. **Partial failure.** One shutdown step throwing skips the rest — including the flush and the
   release — because nobody wrapped them.

## Core concept

### Who sends `SIGTERM`, and when

| Sender | Grace before `SIGKILL` |
|--------|------------------------|
| Kubernetes (after the `preStop` hook) | `terminationGracePeriodSeconds`, default **30 s** |
| Docker (`docker stop`) | `--stop-timeout`, default **10 s** |
| systemd | `TimeoutStopSec`, default **90 s** |
| `supervisord`, CI, a human | whatever the caller decides |

Two deployment facts that break naive handlers:

- **PID 1 does not forward signals.** A shell entrypoint without `exec` receives `SIGTERM` and
  ignores it; the container is eventually `SIGKILL`ed. Use `exec node server.js` (or an init that
  forwards signals).
- **`SIGKILL` cannot be caught.** If your handler has not finished when the grace period expires,
  the process is removed instantly: no flush, no cleanup, no log line. Design the shutdown to fit
  *comfortably* inside the grace period, not to use it all.

### The five phases

```text
P0  QUIESCE ROUTING    mark not ready → wait for the LB to propagate (1–5 s)
P1  STOP INTAKE        close the listener; stop claiming jobs; stop accepting new work
P2  DRAIN              let in-flight work finish, bounded by a deadline
P3  FLUSH              metrics, logs, checkpoints, WAL
P4  RELEASE            close pools, sockets, files, consumers
P5  EXIT               exit(0) if clean, exit(1) if work was lost
```

**P0 before P1 is the rule people get wrong.** Marking the pod not-ready tells the load balancer to
stop sending new traffic, but the change propagates over seconds; closing the listener *immediately*
rejects requests the pod could still have served — the exact source of deploy-time `502`s.

**P2 before P4 is the other rule.** Closing the database pool while a worker is mid-export means the
worker's final checkpoint write fails against a closed pool, and the job is stuck in `running`.

### The in-flight inventory

"Drain" means something different for each kind of work. Know yours:

| In-flight thing | How to stop it | How to finish it |
|-----------------|----------------|------------------|
| HTTP request | close the listener (`server.close()`) | wait for the response to be written |
| Streaming response (SSE, export download) | stop accepting; mark the stream to finish | abort with a clean close, or let it complete |
| Queued job | stop claiming | finish the claimed job, or release the lease so another worker takes it |

**A claimed queue job is the dangerous one.** Stop the consumer while a job is claimed but not
finished and the job is *invisible* to the broker until the visibility timeout expires: delivered
from the broker's perspective, vanished from the user's.

### The time budget

Divide the orchestrator's grace period up front and make each phase's budget explicit:

```text
grace period (K8s default)                       30 s
├── P0 routing propagation                       2 s
├── P1 stop intake                            0.5 s
├── P2 drain (bounded)                          20 s
├── P3 flush                                     3 s
├── P4 release                                   2 s
└── margin                                      2.5 s   ← never plan to use 100% of the window
```

Record **shutdown duration** (p99) and **work lost on shutdown** as metrics. Both should be zero-ish;
if p99 approaches the grace period, you are one slow request from `SIGKILL` on every deploy.

### The escalation ladder

```text
SIGTERM received
  └─ phased shutdown with a hard deadline
       ├─ completed in time → exit(0)
       └─ deadline exceeded → log what was in flight, force-close, release leases, exit(1)
```

Outside your process: `exit(1)` or a deadline overrun → the orchestrator waits its backoff and
restarts the pod; a pod that never responds to `SIGTERM` → `SIGKILL` → **exit 137**.

## How it works (mechanics)

### The handler contract

```text
1. The handler MUST be re-entrancy-safe   (a second SIGTERM must not restart the sequence)
2. The handler MUST have a deadline        (no unbounded wait)
3. Each phase MUST be individually guarded (one failure must not skip the rest)
4. The handler MUST report what was lost   (exit code + a structured log)
5. The handler MUST be fast to start       (no long work before the first phase)
```

Point 5 matters in Python, where the handler runs in the main thread between bytecodes (a slow
handler blocks everything); point 1 matters because orchestrators often send `SIGTERM` twice and a
user can hit Ctrl-C during a deploy.

### The mechanics, per runtime

```ts
// Node: server.close() waits for idle keep-alives; close them yourself (v18.2+).
server.close(() => log.info("listener closed"));
server.closeIdleConnections();            // release idle keep-alives now
// server.closeAllConnections();          // last resort: force-close everything
process.exitCode = 0;                     // preferred: let the event loop drain
```

```go
// Go: Shutdown stops intake and waits for idle conns; a context deadline bounds it.
ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGTERM, syscall.SIGINT)
defer stop()
go func() {
    <-ctx.Done()
    drainCtx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
    defer cancel()
    if err := srv.Shutdown(drainCtx); err != nil { // deadline exceeded → conns still open
        log.Error("shutdown", "err", err)
        srv.Close()                                // force-close what is left
    }
}()
```

```python
import signal, threading

def on_sigterm(signum, frame):
    # Runs in the main thread between bytecodes: keep it tiny, hand off to a worker.
    threading.Thread(target=shutdown, daemon=True).start()

signal.signal(signal.SIGTERM, on_sigterm)
signal.signal(signal.SIGINT, on_sigterm)
```

responses. In Python, `atexit` handlers do **not** run on `SIGTERM` — handle the signal and exit
normally if you want that semantics.

### Ordering constraints, restated as rules

```text
mark not ready  BEFORE  close the listener        (else deploy-time 502s)
stop claiming    BEFORE  close the consumer        (else jobs vanish for a visibility timeout)
finish writes    BEFORE  close the pool            (else checkpoints fail)
close the transport LAST                           (a closed transport cannot flush)
```

## Worked example

```python
# ❌ The classic: one call, wrong order, no deadline. metrics.flush() never runs if
#    db_pool.close() raises, and the listener closes before the LB stops routing → 502s.
def shutdown(signum, frame):
    http_server.shutdown()
    db_pool.close()
    queue_consumer.stop()
    metrics.flush()
```

The corrected handler, with the phases explicit:

```python
SHUTDOWN_DEADLINE_S = 20.0
state = {"inflight": 0, "claimed_jobs": set(), "stopping": False}

def shutdown(signum, frame):
    if state["stopping"]: return            # re-entrancy: a second SIGTERM is a no-op
    state["stopping"] = True
    deadline = time.monotonic() + SHUTDOWN_DEADLINE_S

    readiness.mark_not_ready(); time.sleep(2.0)   # P0 — leave the LB, let it propagate
    queue_consumer.stop_claiming()               # P1 — stop intake first
    http_server.stop_accepting()

    while state["inflight"] > 0 and time.monotonic() < deadline:   # P2 — bounded drain
        time.sleep(0.1)
    lost = state["inflight"]
    if lost:
        log.error("shutdown.deadline", lost=lost, claimed=list(state["claimed_jobs"]))
        queue_consumer.release_leases(state["claimed_jobs"])   # another worker can take them
        http_server.close_all()

    for name, fn in (("metrics", metrics.flush), ("db", db_pool.close),   # P3/P4, isolated
                     ("queue", queue_consumer.close), ("logs", log.flush)):
        try: fn()
        except Exception as exc: log.error("shutdown.step_failed", step=name, err=exc)

    sys.exit(1 if lost else 0)
```

The two details that make the difference in production:

- **`queue_consumer.release_leases(...)`** hands claimed-but-unfinished jobs back explicitly
  instead of waiting for the broker's visibility timeout; without it every deploy leaves jobs
  invisible for minutes.
- **`sys.exit(1 if lost else 0)`** tells the orchestrator and dashboards that work was lost.

## Key data / numbers

- **Signals**: `SIGTERM` **15**, `SIGINT` **2**, `SIGQUIT` **3**, `SIGHUP` **1**, `SIGKILL` **9** —
  only `SIGKILL` is uncatchable.
- **Exit codes**: `0` clean, `1` fatal or work lost, `143` = `128 + 15` (SIGTERM),
  `137` = `128 + 9` (SIGKILL — OOM-kill *or* grace expiry), `134` `SIGABRT`, `139` `SIGSEGV`.
- **Grace periods**: Kubernetes `terminationGracePeriodSeconds` default **30 s** (plus a **2 s**
  delay after the `preStop` hook before `SIGTERM`); Docker `docker stop` default **10 s**; systemd
  `TimeoutStopSec` default **90 s**.
- **Node**: `server.closeIdleConnections()` / `server.closeAllConnections()` — **v18.2+**;
  `keepAliveTimeout` default **5000 ms**, `headersTimeout` default **60000 ms**,
  `requestTimeout` default **300000 ms**; `process.exitCode` vs `process.exit()`.
- **Queue visibility**: SQS `VisibilityTimeout` default **30 s**; Kafka `max.poll.interval.ms`
  default **300000 ms** — a consumer that stops polling longer is evicted from the group.
- **Typical phase budget**: routing **1–5 s**, drain **≤ 20 s**, flush **~3 s**, release **~2 s**,
  margin **≥ 20%** of the grace period. **Measure**: shutdown duration p99, work lost, and
  claims-after-close (should be **0**).

## Real-world use case — Acme SaaS

Acme's `ExportJob` worker writes a large CSV to object storage, then records a checkpoint row in
Postgres so the job can resume. Its `SIGTERM` handler was three lines — close the server, close the
pool, done. Two incidents followed.

**Lost checkpoints.** A deploy landed while a 90-second export was running. The handler closed the
database pool first; the export's final checkpoint write hit a closed pool and raised. The job stayed
in `running` — the lease expired and nothing restarted it (the reconciler meant to find such jobs had
been disabled for "noise" weeks earlier).

**Deploy-time 502s.** The API pods closed their listener first, so the ~2 seconds the load balancer
needed to deregister became ~2 seconds of connection refusals — ~1% of all requests.

The rewritten handler applies the phases and **releases its lease** when it cannot finish:

```text
SIGTERM
  P0  mark not ready         → 2 s deregistration propagation, no 502s
  P1  stop claiming new jobs → no job is claimed by a dying process
  P2  drain (≤ 20 s)         → in-flight export finishes if it can; else release the lease
  P3  flush metrics + checkpoints
  P4  close pool, close consumer, flush logs
  P5  exit(1 if work was lost else 0)
```

Results: deploy-time `502`s went to **zero**; stuck `running` jobs went to **zero** (the lease is
released, so the next worker resumes from the checkpoint); and the new `shutdown_work_lost_total`
metric showed **2** losses in the first month — both genuinely unable to finish in 20 s, both visible
and rescheduled. Re-enabling the reconciler was the other half of the fix.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| **Phased shutdown with a deadline** | preserves in-flight work, observable | more code; needs in-flight accounting | default |
| Close-and-exit | 3 lines | loses work; deploy-time 502s | stateless, no-queue processes only |
| Drain without a deadline | never loses work | gets `SIGKILL`ed; loses everything anyway | never |
| Release leases on shutdown | jobs resume immediately | needs lease/fencing support | queue consumers |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Mark not-ready **before** closing the listener | Close the listener first |
| Stop claiming jobs **before** closing the consumer | Close the consumer and keep claiming |
| Bound the drain with a deadline | Wait for in-flight work indefinitely |
| Guard each shutdown step individually | Let one failing step skip the rest |
| Exit non-zero when work was lost | Always exit `0` |
| Make the handler re-entrancy-safe | Restart the sequence on the second `SIGTERM` |
| `exec` the real process as PID 1 | Leave a shell swallowing `SIGTERM` |

## Common mistakes

- **Closing the listener before deregistering** — the source of nearly all deploy-time `502`s.
- **Closing the pool before the workers stop** — the final checkpoint write fails and the job orphans.
- **No deadline on the drain** — `SIGKILL` takes everything you were trying to save.
- **Stopping the consumer without releasing claims** — jobs invisible until the visibility timeout.
- **`process.exit()` before the log flush** — the last log line (explaining the shutdown) is truncated.
- **Always exiting `0`** — work loss becomes invisible and the restart policy treats it as normal.
- **Signals swallowed by a shell entrypoint** — the container is `SIGKILL`ed on every deploy.

## Checklist

- [ ] `SIGTERM` handler exists, is re-entrancy-safe, and starts fast.
- [ ] The shutdown runs in phases: not-ready → stop intake → drain → flush → release → exit.
- [ ] The drain deadline fits inside the grace period, with margin.
- [ ] In-flight work is tracked and logged when it is lost; claimed jobs are released or fenced.
- [ ] Every shutdown step is individually guarded and logged; exit code distinguishes clean (`0`) from lossy (`1`).
- [ ] The container entrypoint `exec`s the real process.
- [ ] Shutdown duration p99, work lost, and claims-after-close are monitored.
- [ ] A staging drill sends `SIGTERM` under load and asserts exit code, no lost jobs, no 502s.

## Related

- [Process Recovery Limits and When to Terminate (41.16–41.18)](./01-process-recovery-limits-and-termination.md)
- [Node.js: Uncaught Rejection Handling and Graceful Shutdown](../03-practical-examples/01-node-uncaught-rejection-and-graceful-shutdown.md)
- [Initialization, Startup, and Shutdown (41.10–41.18)](../01-concepts/04-initialization-startup-and-shutdown.md)
- [Scheduled Tasks and Graceful Shutdown](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/03-practical-examples/02-scheduled-tasks-and-graceful-shutdown.md)
- [Cleanup Timeouts, Cancellation, and Idempotency](../../../part-05-exception-mechanics/14-resource-cleanup-and-failure-safe-execution/01-concepts/05-cleanup-timeouts-cancellation-and-idempotency.md)
