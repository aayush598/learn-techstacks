# Chapter 41 — Reference

> Part XV · Chapter 41 · Cheat sheets, decision tables, and process-failure reference.

## Decision table — what do I do with this failure?

| Signal | Meaning | Recover in-process? | Correct action |
|--------|---------|--------------------|----------------|
| Uncaught exception (Node) | an error escaped every handler | ❌ | log → flush → `exit(1)` |
| Unhandled rejection (Node ≥ 15) | a promise failed with no observer | ❌ | log → flush → `exit(1)`; fix the detached promise |
| Unhandled rejection (Python `asyncio`) | a task failed; logged at GC time | ❌ | log at task level, never fire-and-forget |
| Unrecovered `panic` (Go) | a goroutine panicked | ❌ | process exits **2**; `recover()` in that goroutine's frame |
| Dropped `err` from `go func()` | a compile error, not a runtime one | n/a | fix the code — the compiler is the only detector you get |
| `ENOMEM` on one allocation | transient pressure | ⚠️ maybe | one failed operation; exit if it repeats |
| Heap OOM (V8) | the runtime is aborting | ❌ | exit **134**; fix the allocation |
| `137` / `OOMKilled` | the cgroup limit was hit | ❌ | exit; fix the workload or the limit; **page** |
| `RangeError: Maximum call stack size exceeded` | recursion bug | ⚠️ maybe | treat the operation as failed; fix the recursion |
| `RecursionError` (Python) | depth limit reached | ⚠️ maybe | fail the operation fast; do not keep serving at the ceiling |
| Goroutine stack overflow (Go) | fatal runtime error | ❌ | exits **2**; bound the recursion |
| `EMFILE` (errno 24) | this process is out of fds | ❌ | exit; find the leak |
| `ENFILE` (errno 23) | the host is out of fds | ❌ | exit; escalate to the host owner |
| Pool acquire timeout | saturation | ✅ | `503` + `Retry-After` + shed load |
| `SQLSTATE 53300` | too many connections | ❌ | fix the pool budget; this is fatal for the connection |
| `SQLSTATE 53200` | out of memory on the DB | ❌ | reduce the query's memory use; add a limit |
| Queue depth over the watermark | saturation | ✅ | reject `429`/`503`; shed |
| Event-loop lag above the SLO | CPU saturation | ✅ | shed load, move work off the request path |
| Bad config at boot | deployment error | n/a | exit **1** with the key named; do not start |
| `EADDRINUSE` | another process owns the port | ❌ | exit **1**; do not retry in a loop |
| `SIGTERM` received | someone wants you to stop | ✅ | phased, bounded shutdown; exit `0` |
| Shutdown deadline exceeded | work could not finish | ✅ | abort, log the loss, exit **1** |
| `SIGKILL` received | the grace period expired | ❌ | nothing ran; find why the shutdown was too slow |

## Decision table — when to terminate?

| Condition | Terminate? | Notes |
|-----------|-----------|-------|
| Expected, bounded, per-request error | ❌ no | handle at the boundary and return it |
| One dependency down, the rest healthy | ❌ no | degrade, shed, or fail that path only |
| One pooled connection broken | ❌ no | discard it, retry once |
| One worker or thread wedged | ❌ no | abort and replace that worker |
| Heap exhausted / OOM | ✅ yes | no memory to run recovery code in |
| Descriptor table exhausted | ✅ yes | the leak's owner is unreachable |
| Native crash (`SIGSEGV`, `SIGABRT`) | ✅ yes | collect a core dump first |
| State may be corrupted | ✅ yes | fast crash beats slow corruption |
| Durable state is corrupt | ✅ yes | exit with a code that blocks auto-restart |
| Event loop wedged | ✅ yes | `SIGKILL` from outside |
| The process is correct but slow | ❌ no | shed load, scale out |

## Signal and exit-code reference

| Signal | Number | Catchable | Meaning |
|--------|--------|-----------|---------|
| `SIGHUP` | 1 | yes | terminal hangup / config reload |
| `SIGINT` | 2 | yes | interactive interrupt (Ctrl-C) |
| `SIGQUIT` | 3 | yes | quit + core dump |
| `SIGKILL` | 9 | **no** | stop now — no cleanup, no logs |
| `SIGUSR1` | 10 | yes | user-defined |
| `SIGUSR2` | 12 | yes | user-defined |
| `SIGTERM` | 15 | yes | please stop (the orchestrator's request) |

| Exit code | Meaning | Orchestrator reaction |
|-----------|---------|----------------------|
| `0` | clean shutdown, no work lost | normal |
| `1` | fatal error, or a shutdown that lost work | restart, alert |
| `2` | Go fatal runtime error / unrecovered panic | restart, alert |
| `134` | `128 + 6` — `SIGABRT` (V8 heap OOM abort) | restart, alert |
| `137` | `128 + 9` — `SIGKILL` (OOM-kill **or** grace expiry) | restart, **page** |
| `139` | `128 + 11` — `SIGSEGV` | restart, alert |
| `143` | `128 + 15` — `SIGTERM` | expected |

## Errno reference (Linux)

| Errno | Value | Meaning | Response |
|-------|-------|---------|----------|
| `EINTR` | 4 | interrupted by a signal | retry the syscall |
| `ENOMEM` | 12 | cannot allocate | exit if it persists |
| `EAGAIN` | 11 | resource temporarily unavailable | back off; treat as saturation |
| `ENFILE` | 23 | **host-wide** fd table full | exit; escalate to the host owner |
| `EMFILE` | 24 | **per-process** fd limit reached | exit; find the leak |
| `EPIPE` | 32 | write on a closed socket | close and stop writing |
| `ETIMEDOUT` | 110 | connection timed out | retry (bounded) |
| `ECONNRESET` | 104 | peer reset the connection | retry (bounded), check conntrack |
| `ECONNREFUSED` | 111 | nothing listening | check the dependency; do not hot-retry |
| `EADDRINUSE` | 98 | port already bound | exit at boot; do not retry in a loop |
| `EADDRNOTAVAIL` | 99 | ephemeral ports exhausted | reuse connections; check the port range |
| `ENOBUFS` | 105 | socket buffer memory unavailable | memory pressure; shed load |

## Shutdown checklist

| # | Step | Verified how |
|---|------|---------------|
| 1 | `SIGTERM` (and `SIGINT`) handlers exist and are re-entrancy-safe | send two signals; the sequence runs once |
| 2 | Handlers are installed before bootstrap | a bootstrap throw still exits `1` |
| 3 | Readiness is marked not-ready **first** | no `502`s in the deploy window |
| 4 | The routing-propagation pause is respected (1–5 s) | load-balancer deregistration observed |
| 5 | Intake stops: listener closed, queue claims stopped | no job claimed after the shutdown started |
| 6 | In-flight work is tracked and awaited | the drain waits for the real count |
| 7 | The drain has a deadline shorter than the grace period | `shutdown_duration_p99` ≪ grace period |
| 8 | Unfinished jobs are released (lease/fencing) | no job invisible after the drain |
| 9 | Telemetry and logs are flushed | the final log line is present in the log store |
| 10 | Pools, sockets, and consumers are released, each step guarded | one failing step does not skip the rest |
| 11 | The exit code is `1` when work was lost | the orchestrator and dashboards see the loss |
| 12 | The container entrypoint `exec`s the real process | `SIGTERM` reaches the app, not a shell |
| 13 | `SIGKILL` during shutdown is impossible in practice | `shutdown_duration_p99` has margin |

## Key numbers

| Item | Value |
|------|-------|
| Kubernetes `terminationGracePeriodSeconds` | **30 s** default (+ ~2 s `preStop` delay) |
| Docker `docker stop` timeout | **10 s** default |
| systemd `TimeoutStopSec` | **90 s** default |
| Recommended shutdown budget | **≤ 25 s** of work inside a 30 s window (≥ 20% margin) |
| Routing-propagation pause | **1–5 s** before closing the listener |
| V8 `--max-old-space-size` vs container limit | **~70–75%** of the container limit |
| Node `--unhandled-rejections` | `strict` (recommended), `throw` (default since v15), `warn`, `warn-with-error-code`, `none` |
| Node `maxListeners` | **10** → `MaxListenersExceededWarning` at the 11th listener |
| Node `keepAliveTimeout` / `headersTimeout` / `requestTimeout` | **5000 ms** / **60000 ms** / **300000 ms** |
| Node `closeIdleConnections()` / `closeAllConnections()` | **v18.2+** |
| Python recursion limit | **1000** default; raise only with a bigger thread stack |
| Go `GOMEMLIMIT` / `GOGC` / `GOMAXPROCS` | soft limit (**1.19+**) / **100** default / CPU count default |
| Go fatal runtime error exit code | **2** |
| Linux `ulimit -n` | verify **inside** the container; runtime often sets **1024** |
| Linux `fs.nr_open` / `fs.file-max` | **1048576** / host-wide |
| Ephemeral ports / `tcp_fin_timeout` | `32768 60999` (**~28,231**) / **60 s** |
| `nf_conntrack_max` | commonly **262144**; overflow drops packets silently → timeouts |
| Postgres `max_connections` / reserved | **100** / **3** |
| cgroup CPU period (CFS) | **100 ms**; excess work is *paused*, not slowed |
| Kubernetes restart backoff | **10 s → 20 s → 40 s …**, capped at **5 min**; alert at ~5 restarts / 10 min |

## Chapter glossary

| Term | Meaning |
|------|---------|
| Uncaught exception | An error that escaped every handler and reached the runtime's top level |
| Unhandled rejection | A promise rejected with no handler attached by the end of the turn |
| Last-resort handler | The `uncaughtException` / `unhandledRejection` hook: log, flush, exit |
| Post-mortem hook | A handler whose purpose is diagnosis, not continued execution |
| Heap OOM | The runtime aborting because the managed heap is exhausted |
| OOM kill | The kernel killing a process that exceeded its cgroup memory limit |
| EMFILE / ENFILE | Per-process vs host-wide file-descriptor exhaustion |
| Ephemeral port exhaustion | The outbound port space is full; connections stall or fail to bind |
| Pool exhaustion | Every connection in the pool is in use and waiters queue |
| Admission control | Rejecting work up front rather than queueing it without bound |
| Backpressure | Making the producer slow down because the consumer cannot keep up |
| Event-loop lag | The delay between a timer firing and the loop being free — Node's saturation signal |
| CPU throttling | The container being *paused* for the unused part of its CFS period |
| Graceful shutdown | The phased protocol that stops intake, drains, flushes, releases, exits |
| Drain | The bounded wait for in-flight work to finish |
| Grace period | The orchestrator's window between `SIGTERM` and `SIGKILL` |
| PreStop hook | A Kubernetes lifecycle hook that runs before `SIGTERM` is sent |
| Readiness / liveness | "Can I serve?" vs "am I wedged?" — two different questions |
| PID 1 signal semantics | PID 1 must handle `SIGTERM` explicitly and reap children; shells do not forward |
| Restart safety | The property that a fresh process rebuilds correct state with no duplicate effects |
| Lease | A time-bounded claim on work; releasing it hands the work back |
| Crash loop | Repeated restarts of a deterministic failure; a symptom, not a recovery |
| Corrupted state | Data that is internally inconsistent and survives a restart |

## Signposts

- Unhandled rejections in async code → [Ch. 12 deep dive](../../../part-05-exception-mechanics/12-exception-propagation-and-control-flow/02-deep-dive/02-async-propagation-and-unhandled-rejections.md)
- Cleanup and timeouts → [Ch. 14](../../../part-05-exception-mechanics/14-resource-cleanup-and-failure-safe-execution/README.md)
- Pool and connection errors → [Ch. 22](../../../part-09-database-and-transactions/22-database-error-classification/01-concepts/01-connection-and-pool-errors.md)
- Bulkheads and admission control → [Ch. 29](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/01-concepts/03-bulkheads-and-concurrency-limits.md)
- Worker shutdown in a queue → [Ch. 32](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/01-concepts/04-worker-failures-timeouts-and-isolation.md)

## Related

- [Chapter 41 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 41 Index](../README.md)
- [Part XV Index](../../README.md)
