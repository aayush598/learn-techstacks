# Chapter 41 — Do's and Don'ts

> Part XV · Chapter 41 · All sections

A condensed rule set distilled from the chapter. Use it as a pre-deploy checklist for any service
that can crash, exhaust a resource, or be asked to stop.

## Uncaught errors and unhandled async (41.1–41.2)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Log, flush, then exit non-zero on `uncaughtException` | Install a handler "so the server stays up" |
| Log, flush, then exit non-zero on `unhandledRejection` | Ignore the rejection and keep serving |
| Normalize a non-`Error` reason before logging | Assume `reason.stack` exists |
| Await or `.catch()` every promise you start | Start detached promises with `void` |
| Run with `--unhandled-rejections=strict` | Rely on an undocumented default |
| Translate expected failures at the boundary | Let a domain error reach the runtime |
| Treat `MaxListenersExceededWarning` as a leak | Raise `maxListeners` to silence it |

## Memory, stack, and descriptors (41.3–41.6)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Stream or page large results | Buffer a whole export in memory |
| Set `--max-old-space-size` to ~70–75% of the container limit | Set it equal to the container limit |
| Alert on RSS growth *shape* and fd headroom | Wait for `EMFILE` or an OOM kill |
| Close streams and sockets on success, error, and abort | Close only on the success path |
| Check `ulimit -n` inside the container | Assume the host's limit applies |
| Exit on `EMFILE` / `MemoryError` | Catch it and keep serving |
| Bound recursion with an explicit depth limit | Catch `RecursionError` and continue |
| Treat `137` as a page | Treat `137` as noise |

## Pool, queue, and CPU pressure (41.7–41.9)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Set an acquire timeout on every pool | Wait for a connection forever |
| Size pools from the server's connection budget | Size pools from the app's core count |
| Use separate pools per workload class | Share one pool across tenants and workloads |
| Set `statement_timeout` on every session | Let one query hold a session indefinitely |
| Bound queue depth and reject past the watermark | Accept work you cannot start |
| Alert on queue **age**, not only depth | Alert only on depth |
| Probe liveness process-locally | Probe liveness through a saturated dependency |
| Cap outbound connections (`MaxConnsPerHost`) | Let an outbound client consume your fds |

## Startup and initialization (41.10–41.13)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Validate and freeze config at boot | Read `process.env` per request |
| Reject unknown config keys | Fall back to a default for a required value |
| Import every module at boot | Lazily `require()` a module that can throw |
| Retry transient dependency failures with bounded backoff | Retry a permanent error forever |
| Fail the boot on a permanent dependency error | Start "ready" with a broken dependency |
| Separate readiness from liveness | Use one probe for both |
| Run migrations as a separate job | Run migrations in the app's startup path |

## Graceful shutdown and termination (41.14–41.15)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Mark not-ready **before** closing the listener | Close the listener first |
| Stop claiming jobs **before** closing the consumer | Keep claiming while shutting down |
| Finish writes **before** closing the pool | Close the pool while work is in flight |
| Bound the drain with a deadline | Wait for in-flight work indefinitely |
| Release leases for unfinished jobs | Let the visibility timeout hide them |
| Guard each shutdown step individually | Let one failing step skip the rest |
| Exit non-zero when work was lost | Always exit `0` |
| Make the handler re-entrancy-safe | Restart the sequence on the second `SIGTERM` |
| `exec` the real process as PID 1 | Leave a shell swallowing `SIGTERM` |
| Keep the shutdown budget under the grace period | Plan to use 100% of the window |

## Recovery, termination, and corruption (41.16–41.18)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Ask "is the process still a valid executor?" | Ask "can I catch this?" |
| Discard suspect in-memory state when you catch an error | Continue with a half-built context |
| Make restart-safety a property of every durable effect | Assume "restart" means "no duplicate effects" |
| Alert on restart counts and crash loops | Let the backoff hide a deterministic bug |
| Verify invariants at startup after a crash | Serve whatever the durable store contains |
| Isolate crash-prone components in their own process | Run a native parser in the request path |
| Collect a core dump for native crashes | Lose the evidence to a bare stack trace |

## Anti-patterns in the wild

1. **The Lifeboat** — `process.on('uncaughtException', log)` added to stop alerts, leaving a
   process with undefined state to keep serving traffic.
2. **The Detached Promise** — `void doWork()` with no `.catch()`; the rejection is found by the
   runtime, not by the code review.
3. **The Ceiling** — catching `MemoryError` and returning a `503`, so the process keeps serving at
   its memory ceiling until the cgroup kills it.
4. **The Quiet Queue** — a pool acquire with no timeout, turning a full pool into an unbounded
   request queue and a restart storm.
5. **The Warm Restart** — restarting a process whose durable state is corrupt, reproducing the
   corruption on every attempt.
6. **The Late Close** — closing the database pool before the workers finish, so the last
   checkpoint write fails and the job is orphaned.
7. **The Phantom Claim** — stopping the queue consumer without releasing claims, so jobs vanish
   until the visibility timeout expires.
8. **The Gracious 0** — a shutdown that always exits `0`, so every lost job is invisible.
9. **The Shell PID 1** — a container entrypoint without `exec`, so `SIGTERM` never reaches the
   app and every deploy ends in `SIGKILL`.
10. **The Heap Limit Lie** — `--max-old-space-size` set equal to the container limit, so V8 never
    reports an OOM and the cgroup kills the pod with no diagnostics.

## Chapter checklist

- [ ] Uncaught errors and unhandled rejections log, flush, and exit non-zero.
- [ ] No detached promises; expected failures are translated at the boundary.
- [ ] Memory, fd, and stack usage are bounded in code, not merely limited by configuration.
- [ ] Container limits are read at boot; V8's heap flag is below the container memory limit.
- [ ] Streams and sockets are released on success, error, and abort paths.
- [ ] Every pool has a size, an acquire timeout, and a statement timeout.
- [ ] Queues are bounded, reject past the watermark, and alert on age.
- [ ] Config is validated and frozen at boot; modules are imported at boot.
- [ ] Readiness and liveness are separate; liveness never depends on a dependency.
- [ ] Shutdown is phased, bounded, idempotent, and reports losses in the exit code.
- [ ] Restart-safety is guaranteed for every durable side effect (idempotency, lease, checkpoint).
- [ ] Exit codes are meaningful and monitored (`0`, `1`, `137`, `143`).

## Related

- [Chapter 41 Reference](../05-reference/README.md)
- [Chapter 41 Index](../README.md)
- [Part XV Index](../../README.md)
- [Part XI — Retry Logic and Resilience](../../../part-11-retry-and-resilience/README.md)
