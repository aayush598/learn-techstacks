# Initialization, Startup, and Shutdown (41.10–41.18)

> Part XV · Chapter 41 · Sections 41.10–41.18 · _Estimated reading time: 28 min_
> **Prerequisite:** [Pool, Queue, and CPU Pressure (41.7–41.9)](./03-pool-queue-and-cpu-pressure.md)

## In one sentence

**Startup is where you should fail and shutdown is where you should succeed** — validate config
and dependencies *once at boot*, and treat `SIGTERM` as a **designed protocol with a deadline**.
The process that ignores it loses work on every deploy.

## Why this matters in production

Two failures account for a large share of "the deploy went wrong" incidents, and neither shows
up in an application log:

- **Startup failures** are *late* failures. A module that throws on first use, a config value
  that is `undefined` after a secret was rotated, a database briefly unreachable at boot — all
  produce a process that *starts*, passes readiness, and only fails when traffic arrives.
- **Shutdown failures** are *silent* failures. A pod that receives `SIGTERM` and exits before
  flushing, before closing the database pool, or before finishing the job it claimed, loses work
  without an error. The customer sees "my export disappeared"; you see nothing at all.

The asymmetry to internalize: **a failed startup is loud and harmless; a failed shutdown is
quiet and destructive.**

## Core concept

### 41.10 Runtime init failures

The process never became a running application. The runtime itself refused to cooperate:

| Failure | Signal | Typical cause |
|---------|--------|---------------|
| Syntax / parse error | `SyntaxError` at parse time, exit **1** | bad build artifact |
| Port already in use | `EADDRINUSE` (errno **98**) | two processes, or a lingering `TIME_WAIT` binding |
| DNS failure at boot | `EAI_AGAIN` / `ENOTFOUND` | resolver or service-discovery entry not ready |
| Out of memory at boot | `ENOMEM`, exit **134**/**137** | heap flag plus workload exceeds the container limit |

None are recoverable in-process: the process must exit and the orchestrator must retry. The work
is making the failure **diagnosable** and separating *"this deployment is broken"* (page) from
*"this dependency is briefly unavailable"* (retry with backoff).

### 41.11 Module loading

Module loading has a distinctive failure profile: **the error happens at import time, but the
*consequence* happens much later.** A lazily imported module fails on the first request to its
route — in production, under load.

The common traps:

- **Top-level side effects.** Code that reads a file or opens a socket at import time fails at
  *import* time (fine); the same code in a **lazily** imported module fails at first use.
- **Circular imports** produce `undefined` at module-evaluation time instead of an exception — the
  classic `Cannot read properties of undefined (reading 'Foo')` that is really an import cycle.

**Rule: every module must be loadable at boot.** Import *cost* is a startup-time concern; import
*failures* are a correctness concern.

### 41.12 Config loading

Config is the most common source of "the code is fine, the environment is wrong" incidents, and
config failures are **perfectly detectable at boot** — if you do the detection.

| Failure | Example | Detected when? |
|---------|---------|----------------|
| Missing required value | `DATABASE_URL` unset after a secret rotation | boot, if validated |
| Invalid value | `POOL_SIZE=abc`, `TIMEOUT=5s` (needs a number) | boot, if parsed |
| Out-of-range value | `POOL_SIZE=1000` against a 100-connection database | boot, if range-checked |
| Secret readable but wrong | a stale key that authenticates as nobody | request time — the worst time |

The pattern: read raw values → parse and validate against a schema (unknown keys rejected) →
freeze a typed, immutable config object → use `config.<field>` everywhere else, with **no
`process.env` reads below the bootstrap layer**.

### 41.13 Startup and dependency init

At boot a service connects to the database, the cache, and the queue consumer, warms caches, and
*maybe* runs migrations — each step has a different right answer.

| Step | Failure | Right answer |
|------|---------|--------------|
| Connect to the database | transient network error | **retry with backoff** for a bounded window, then fail the boot |
| Connect to the database | auth error / bad host | **fail immediately** — retrying will not help |
| Warm the cache | cache down | **degraded start** — serve without cache |
| Open the queue consumer | queue down | **fail the boot** — a worker that cannot consume should not be "ready" |
| Run migrations | lock held / conflicting migration | **fail the boot**; migrations belong in a separate job |

**Readiness vs liveness** makes startup safe: liveness asks *"is this process wedged?"*,
readiness *"can it serve traffic?"*. A process still initializing is **not ready** but **alive** —
one probe for both lets a slow database kill healthy pods.

### 41.14 Graceful shutdown failures

**Graceful shutdown** is the sequence you run when you learn you are going to stop: stop taking
new work, finish the work in hand, release resources, exit. Most implementations keep only the
last step:

```text
SIGTERM arrives
  → server.close()      ← stops accepting NEW connections
  → process.exit()      ← everything still in flight is now lost
```

The parts that usually break:

- **`server.close()` waits for keep-alive connections**, so the server stays "open" for as long
  as `keepAliveTimeout`. Node ≥ 18.2 adds `server.closeIdleConnections()` /
  `server.closeAllConnections()` for exactly this.
- **The drain has no deadline**, so the orchestrator sends `SIGKILL` and you lose the work
  anyway — now without a clean exit.
- **A shutdown step throws**, and the remaining steps never run unless each has its own `try/catch`.

### 41.15 Termination failures

Termination is the last resort and it has exactly two forms:

| Signal | Catchable? | Meaning |
|--------|-----------|---------|
| `SIGTERM` (15) | yes | "please stop" — the orchestrator's request |
| `SIGINT` (2) | yes | interactive interrupt (Ctrl-C) |
| `SIGKILL` (9) | **no** | "stop now" — nothing runs, no cleanup, no logs |

`SIGKILL` is what the orchestrator sends when the grace period expires. If your process needs
`SIGKILL` to stop, **every deploy loses in-flight work** — permanently and invisibly:

- **PID 1 does not forward signals** — a shell or supervisor without `exec` swallows `SIGTERM` —
  and **the shutdown path can outlast the grace period**; both end in an inevitable `SIGKILL`.

### 41.16 Limits of process recovery

Some states cannot be repaired from inside the running process:

| State | Why in-process recovery fails |
|-------|-------------------------------|
| **Descriptor table exhausted** | every subsequent `open`/`accept` fails (`EMFILE`); the leak's owner is unreachable |
| **Heap exhausted / OOM** | the runtime is aborting (`ENOMEM`, exit **137**); no memory to run recovery code in |
| **Corrupted native state** | a segfault or native-addon bug means the process's invariants are gone |
| **A poisoned global singleton** | a cache or registry that holds bad data for every caller |

In all of these, **restarting the process is not a workaround — it is the repair.** The work
moves from "recover the state" to "reconstruct the state from a durable source"; see the
[deep dive on recovery limits](../02-deep-dive/01-process-recovery-limits-and-termination.md).

### 41.17 When to terminate

The decision, stated as a rule:

```text
IF the failure is a bug in THIS process, its invariants are known-intact,
   AND restarting is cheap and idempotent
THEN terminate (and fix the bug)

IF the failure may have corrupted state, or the invariants are unknown,
   or the process cannot complete its own cleanup
THEN terminate immediately, without cleanup (fast crash > slow corruption)

IF the failure is an expected, bounded, per-request condition
THEN do NOT terminate — handle it at the boundary and return an error
```

The third branch is where teams get it wrong: a `404`, a validation failure, a declined card, a `503` from Stripe — **none of these are reasons to exit**.

### 41.18 Unsafe recovery from corrupted state

Restarting is safe only if state is rebuilt from a **durable, consistent** source. If the
corrupted state is *durable*, restarting reproduces it exactly: a half-written file is read again,
a corrupted WAL is replayed, a half-applied migration is not undone, a poisoned cache re-poisoned.

The rules:

1. **Every piece of state the process holds must be reconstructible** from durable storage, or explicitly disposable.
2. **Startup must validate what it loads** — refuse to start rather than serve corrupt durable state.
3. **After a crash, the replacement should verify its invariants first**, not accept new work.

⚠️ **Hazard.** The dangerous combination is **"retry forever"** on top of **corrupt durable state**:
the pod crashes at boot and the restart policy hides the original corruption behind restart noise.

## How it works (mechanics)

The shutdown sequence that does not lose work: **SIGTERM → mark "not ready" (leave the LB) → stop
claiming → close the listener → drain in-flight work (bounded) → flush → release → `exit(0)`; on
deadline overrun, log the work in flight, force-close, `exit(1)`.** Order: **readiness first,
listener second, in-flight third** (routing takes time to propagate) — `exit(1)` makes lost work visible.

## Worked example

```ts
// ✅ Ordered, bounded, idempotent shutdown.
// ❌ The naive version — close the server, flush nothing, exit — drops in-flight work.
const SHUTDOWN_DEADLINE_MS = 25_000;   // < the orchestrator grace period (30 s default)
let shuttingDown = false;

async function shutdown(signal: string, exitCode = 0): Promise<void> {
  if (shuttingDown) return;          // idempotent: a second SIGTERM must not restart the dance
  shuttingDown = true;
  const deadline = Date.now() + SHUTDOWN_DEADLINE_MS;
  log.info({ signal }, "shutdown started");

  // 1. Leave the load balancer first — routing changes take time to propagate.
  readiness.markNotReady();
  await sleep(2_000);                 // give the LB the propagation window

  // 2. Stop taking NEW work. Claims stop before the listener closes.
  queue.stopClaiming();               // in-flight jobs keep running
  httpServer.close();                 // stop accepting new connections
  httpServer.closeIdleConnections();  // Node >= 18.2: release idle keep-alive sockets

  // 3. Wait for in-flight work, bounded by the deadline.
  const drained = await waitForInFlight(deadline);
  if (!drained) {
    log.error({ inFlight }, "shutdown deadline exceeded with work in flight");
    httpServer.closeAllConnections();  // cut the rest loose; report it
    exitCode = 1;                      // non-zero: work was lost
  }

  // 4. Flush, then release, each step isolated so one failure does not skip the rest.
  await safe(() => metrics.flush(), "metrics flush");
  await safe(() => db.end(), "db pool close");
  await safe(() => queue.close(), "queue consumer close");
  await flushLogs();
  process.exit(exitCode);
}

async function safe(fn: () => Promise<void>, name: string): Promise<void> {
  try { await fn(); } catch (err) { log.error({ err, step: name }, "shutdown step failed"); }
}

process.on("SIGTERM", () => { void shutdown("SIGTERM", 0); });
process.on("SIGINT",  () => { void shutdown("SIGINT", 0); });
```

## Key data / numbers

- **Signals**: `SIGHUP` **1**, `SIGINT` **2**, `SIGQUIT` **3**, `SIGKILL` **9**, `SIGTERM` **15**,
  `SIGUSR1` **10**, `SIGUSR2` **12**. Only `SIGKILL` cannot be caught.
- **Exit codes**: `143` = `128 + 15` (SIGTERM, normal stop), `137` = `128 + 9` (SIGKILL / OOM-kill,
  never normal), `134` = `128 + 6` (SIGABRT), `139` = `128 + 11` (SIGSEGV), `1` = fatal error.
- **Grace periods**: Kubernetes `terminationGracePeriodSeconds` default **30 s** (plus a **2 s**
  `preStop` hook delay); Docker `docker stop` default **10 s**; systemd `TimeoutStopSec` **90 s**.
- **Node** `server.closeIdleConnections()` / `server.closeAllConnections()` — **v18.2+**;
  `keepAliveTimeout` **5000 ms**, `headersTimeout` **60000 ms**, `requestTimeout` **300000 ms**.
  `--unhandled-rejections=strict` makes an unhandled rejection **throw** (default since Node 15);
  `MaxListenersExceededWarning` fires at the 11th listener on one emitter (default **10**).
- **Go** `signal.Notify(ctx, syscall.SIGTERM, syscall.SIGINT)` + `http.Server.Shutdown(ctx)`.
- **Python** `signal.signal(signal.SIGTERM, handler)`; `SIGKILL` cannot be caught; `atexit`
  handlers do **not** run on `SIGTERM` unless your handler exits normally.
- **PID 1** must handle `SIGTERM` and **reap** its children; `exec` shell entrypoints so signals
  reach the real process. **Readiness window**: wait **1–5 s** for LB routing to converge.
- **Errno**: `EADDRINUSE` **98**, `EMFILE` **24**, `ENOMEM` **12**, `EAI_AGAIN`/`ENOTFOUND`;
  `ERR_DLOPEN_FAILED` (native ABI mismatch), `ERR_REQUIRE_ESM` (ESM/CJS mismatch).
- **Container memory limits**: cgroups v2 `memory.max`, Kubernetes `resources.limits.memory`;
  the OOM kill exits **137**; `ulimit -n` must be checked **inside the container**.

## Real-world use case — Acme SaaS

**Startup.** A secret rotation renamed `EXPORT_QUEUE_URL` to `EXPORT_QUEUE_URL_V2`. The old variable
was removed from the secret manager but the deployment template still set it, so the process booted
with an empty string, built a queue client with an empty endpoint, and **crashed on the first enqueue**
ten minutes into the deploy. The pod had passed a static `200` readiness probe, so traffic was routed
to it and every export request returned `500` while the rollout continued. The fix: a **boot-time
schema check** that exits **1** naming the missing key, plus a readiness probe that touches the queue —
the next rotation failed the pod in **200 ms**: `CONFIG_INVALID: EXPORT_QUEUE_URL_V2 is required`.

**Shutdown.** The same week, a deploy of the API pods dropped ~1% of requests with `502`s. The
`SIGTERM` handler closed the HTTP server and exited but never stopped the `ExportJob` consumer: for
~3 seconds the worker kept **claiming jobs from the queue** and then died holding them. They were not
lost — they were *claimed*, so the broker treated them as delivered and they only returned after the
visibility timeout expired. Users saw "my export started and vanished."

The fix was the ordered shutdown above: mark not ready → **stop claiming first** → close the
listener → drain against a deadline → flush → release → exit. Deploy-time `502`s went to zero and
the "claimed but never processed" count fell from ~40 per deploy to zero (budget **25 s** < **30 s**).

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| **Validate config at boot, exit on invalid** | one loud failure instead of many quiet ones | deploys fail fast | always |
| **Retry dependency init with backoff** | survives a brief dependency blip | delays readiness | transient dependency failures |
| **Graceful drain with a deadline** | preserves in-flight work | takes time; needs a hard cutoff | default for `SIGTERM` |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Validate and freeze config at boot | Read `process.env` per request |
| Fail the boot on missing/invalid required config | Fall back to a default for a required value |
| Import every module at boot so import errors surface early | Lazily `require()` a module that can throw |
| Distinguish readiness (not yet ready) from liveness (wedged) | Use one probe for both |
| Stop claiming work before closing the listener | Close the listener while the worker still claims |

## Common mistakes

- **Ready before ready** — the readiness probe returns `200` as soon as the HTTP server is up, so
  traffic arrives before the DB pool or queue consumer is connected.
- **Migrations in the startup path** — two pods race, one crashes, the deploy stalls, and the
  schema is now half-migrated.
- **Closing resources in the wrong order** — the workers' final writes hit a closed pool.
- **No deadline on the drain** — the orchestrator sends `SIGKILL` and you lose exactly what you
  were trying to save.
- **Trusting `SIGTERM` to arrive** — with a shell as PID 1 it never does.

## Checklist

- [ ] Config is parsed, validated, and frozen at boot; unknown keys are rejected.
- [ ] Dependency init retries transient failures with bounded backoff and fails fast on permanent ones.
- [ ] Readiness and liveness are separate probes; liveness never depends on a dependency.
- [ ] Migrations run as a separate job, not in the app's startup path.
- [ ] `SIGTERM` handling is ordered: not-ready → stop claiming → close listener → drain → flush
      → release → exit, with a deadline shorter than the grace period.
- [ ] The shutdown path is idempotent and each step is individually guarded.

## Related

- [Process Recovery Limits and When to Terminate (41.16–41.18) — deep dive](../02-deep-dive/01-process-recovery-limits-and-termination.md)
- [Graceful Shutdown Sequencing with SIGTERM — deep dive](../02-deep-dive/02-graceful-shutdown-sequencing.md)
- [Node.js: Uncaught Rejection Handling and Graceful Shutdown](../03-practical-examples/01-node-uncaught-rejection-and-graceful-shutdown.md)
- [Worker Failures, Timeouts, Shutdown, and Isolation](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/01-concepts/04-worker-failures-timeouts-and-isolation.md)
