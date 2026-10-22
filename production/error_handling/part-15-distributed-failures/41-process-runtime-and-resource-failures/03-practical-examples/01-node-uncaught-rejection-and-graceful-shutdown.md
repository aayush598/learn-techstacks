# Node.js — Uncaught Rejection Handling and Graceful Shutdown

> Part XV · Chapter 41 · Sections 41.1, 41.2, 41.14, 41.15 · _Estimated reading time: 26 min_
> **Prerequisite:** [Uncaught Exceptions and Unhandled Async Failures (41.1–41.2)](../01-concepts/01-uncaught-and-unhandled-failures.md)

## In one sentence

A production Node service has exactly **two** last-resort behaviours — **log-and-exit** for
anything uncaught, and a **phased, bounded `SIGTERM` drain** for anything voluntary — and both
end in an **explicit exit code** so the orchestrator and the dashboards can tell a clean stop from
a crash.

## Why this matters in production

Node's default behaviour is already close to correct: an unhandled rejection raises as an uncaught
exception and the process exits with code 1. Almost every real deployment breaks it the same way —
someone adds `process.on('uncaughtException', log.error)` to "stop the errors from killing the
server", and the process now survives errors it has no business surviving.

The other half is the shutdown path. Node is unusually good at this (the event loop makes a clean
exit natural) and unusually easy to get wrong (one `process.exit()` at the end of the handler throws
away everything the process was doing).

## The service, end to end

```ts
// src/bootstrap.ts
import { config } from "./config";
import { server } from "./http";
import { queue } from "./queue";
import { db } from "./db";
import { logger } from "./logger";

export async function main(): Promise<void> {
  // 1. Config is validated ONCE, before anything else can use it.
  //    A missing key exits 1 here — not 200 requests later.
  config.validate();

  // 2. Every module is imported at boot, so import-time failures are boot failures.
  await db.connect();                    // fails fast on a permanent error
  await queue.connect();
  await warmCache();                    // best-effort: a cold cache is not a reason to refuse traffic

  // 3. Start listening only after the dependencies are usable.
  server.listen(config.port);
  logger.info({ port: config.port, version: config.version }, "started");
}
```

```ts
// src/config.ts — validate, parse, freeze. No process.env reads below this file.
import { z } from "zod";

const schema = z.object({
  PORT: z.coerce.number().int().min(1).max(65535).default(8080),
  DATABASE_URL: z.string().url(),
  EXPORT_QUEUE_URL: z.string().url(),
  POOL_SIZE: z.coerce.number().int().min(1).max(50).default(10),
  SHUTDOWN_DEADLINE_MS: z.coerce.number().int().min(1_000).max(120_000).default(25_000),
}).strict();   // .strict() → an unknown key is an error, not a shrug

export const config = Object.freeze(schema.parse(process.env));
```

A missing `EXPORT_QUEUE_URL` now fails at boot with a message naming the key, instead of failing
on the first export ten minutes into the deploy.

### The last-resort handlers

```ts
// src/fatal.ts
import { logger } from "./logger";
import { flush } from "./telemetry";
import { countOpenFds } from "./fd";

let exiting = false;

export function installFatalHandlers(): void {
  // Monitor: fires BEFORE the fatal handler. Logging only — process.exit() here is a no-op.
  process.on("uncaughtExceptionMonitor", (err, origin) => {
    logger.error({ err, origin, pid: process.pid }, "uncaught exception (monitor)");
  });

  process.on("uncaughtException", (err, origin) => {
    void fatal("uncaughtException", err, origin);
  });

  process.on("unhandledRejection", (reason) => {
    void fatal("unhandledRejection", reason, "promise");
  });
}

async function fatal(kind: string, reason: unknown, origin: string): Promise<void> {
  if (exiting) return;                 // idempotent: never run twice
  exiting = true;

  // The reason may not be an Error. Normalize BEFORE logging, or the handler throws in the handler.
  const err = reason instanceof Error ? reason : new Error(`non-Error reason: ${safeString(reason)}`);

  logger.error(
    {
      err,
      kind, origin, pid: process.pid,
      uptime_s: Math.round(process.uptime()),
      rss_mb: Math.round(process.memoryUsage().rss / 1024 / 1024),
      open_fds: countOpenFds(), in_flight: inFlight(), version: process.env.APP_VERSION,
    },
    "fatal: terminating process",
  );

  await flush().catch(() => {});       // flush BEFORE exiting: process.exit() truncates stdout
  process.exit(1);                     // non-zero: the orchestrator must restart us
}
```

Install these **first**, before anything else in `main()` — if bootstrap itself throws, the
handlers must already be there:

```ts
// src/index.ts
import { installFatalHandlers } from "./fatal";
import { main } from "./bootstrap";
import { shutdown } from "./lifecycle";

installFatalHandlers();
process.on("SIGTERM", () => { void shutdown("SIGTERM", 0); });
process.on("SIGINT",  () => { void shutdown("SIGINT", 0); });

main().catch((err) => { console.error("startup failed", err); process.exit(1); });
```

Run it with the strict rejection mode in **both** CI and production:

```bash
node --unhandled-rejections=strict --max-old-space-size=1536 dist/index.js
```

`--unhandled-rejections=strict` makes an unhandled rejection fatal (the default since Node 15 is
nearly the same, but explicit documents the intent). `--max-old-space-size=1536` is deliberately
**below** the container limit, so a memory problem produces a JS heap OOM abort (exit **134**) with a
stack trace instead of a cgroup kill (exit **137**) with nothing.

### The graceful shutdown

```ts
// src/lifecycle.ts
import { server } from "./http";
import { queue } from "./queue";
import { db } from "./db";
import { logger } from "./logger";
import { flush } from "./telemetry";

let shuttingDown = false;

export async function shutdown(signal: string, exitCode = 0): Promise<void> {
  if (shuttingDown) return;            // a second SIGTERM must not restart the sequence
  shuttingDown = true;

  const deadline = Date.now() + Number(process.env.SHUTDOWN_DEADLINE_MS ?? 25_000);
  logger.info({ signal, in_flight: inFlight() }, "shutdown.started");

  // P0 — leave the load balancer FIRST; the change takes seconds to propagate.
  readiness.markNotReady();
  await sleep(2_000);

  // P1 — stop intake: no new connections, no new claims. In-flight jobs keep running.
  queue.stopClaiming();
  server.close();
  server.closeIdleConnections();        // Node >= 18.2: release idle keep-alive sockets now

  // P2 — drain, bounded.
  while (inFlight() > 0 && Date.now() < deadline) {
    await sleep(100);
  }
  let code = exitCode;
  if (inFlight() > 0) {
    logger.error({ in_flight: inFlight() }, "shutdown.deadline_exceeded");
    server.closeAllConnections();      // Node >= 18.2: force the rest off
    code = 1;                          // work was lost — say so in the exit code
  }

  // P3/P4 — flush and release, each step isolated so one failure does not skip the rest.
  await step("telemetry", () => flush());
  await step("queue",      () => queue.close());
  await step("db",         () => db.end());
  await step("logs",       async () => { /* logger.flush() */ });

  logger.info({ signal, exit_code: code }, "shutdown.finished");
  process.exit(code);
}

async function step(name: string, fn: () => Promise<unknown>): Promise<void> {
  try { await fn(); }
  catch (err) { logger.error({ err, step: name }, "shutdown.step_failed"); }
}
```

### Tracking in-flight work

```ts
// src/inflight.ts — count in-flight work so the drain knows when it is safe to exit.
let count = 0;
export function inFlight(): number { return count; }
export function track<T>(promise: Promise<T>): Promise<T> {
  count++;
  return promise.finally(() => { count--; });
}

// src/http.ts — every request is tracked.
server = http.createServer((req, res) => { track(handle(req, res)); });
```

## Testing it

```ts
// test/fatal.spec.ts
import { spawn } from "node:child_process";

it("exits with code 1 on an unhandled rejection", async () => {
  const child = spawn(process.execPath, ["--unhandled-rejections=strict", "dist/throw.js"]);
  const code = await new Promise<number>((resolve) => child.on("exit", resolve));
  expect(code).toBe(1);
});
```

```bash
# The shutdown drill: send SIGTERM under load, then assert exit code 0, no 502, no orphaned job.
kill -TERM $PID; wait $PID; echo "exit=$?"
```

## Key data / numbers

- `--unhandled-rejections=strict` (also `throw`, `warn`, `warn-with-error-code`, `none`); Node's
  default since v15 is to **raise** an unhandled rejection as an uncaught exception → **exit 1**.
- `process.on("uncaughtExceptionMonitor", ...)` (Node **v12.17+**) fires *before* `uncaughtException`,
  where `process.exit()` is a no-op; `rejectionHandled` fires when a handler attaches late.
- `server.closeIdleConnections()` and `server.closeAllConnections()` — Node **v18.2+**.
- `server.keepAliveTimeout` **5000 ms**, `headersTimeout` **60000 ms**, `requestTimeout` **300000 ms**.
- Exit codes: `0` clean, `1` fatal or lossy shutdown, `134` `SIGABRT` (V8 heap OOM abort),
  `137` `SIGKILL` (cgroup OOM-kill or grace expiry), `143` `SIGTERM`.
- Kubernetes `terminationGracePeriodSeconds` **30 s**; the shutdown budget must be **below** it with
  margin (commonly **25 s** of work in a 30 s window). `--max-old-space-size` should be **~70–75%**
  of the container memory limit.
- `EventEmitter` default `maxListeners` = **10** → **`MaxListenersExceededWarning`** at the 11th listener.

## Real-world use case — Acme SaaS

Acme's API pod had `process.on("uncaughtException", (e) => logger.error(e))` added by a developer
during an incident six months earlier. It "fixed" the alerts and created a worse problem: the process
kept running after errors that left its state inconsistent.

The incident that exposed it was a `WebhookIngest` bug that threw **after** writing to the `events`
table but **before** updating the `webhook_deliveries` row. The handler logged and continued; Stripe's
retries kept arriving; the same event was inserted again and again. The duplicate rate reached **100%**,
and reconciliation flagged **every** downstream invoice — a billing incident generated by a handler
that "prevented the crash".

The fix was two commits: (1) the `uncaughtException` handler now **logs, flushes, and exits 1**, so the
duplicate rate dropped to **0%** and the crash became a **pager** instead of a swallowed log line; and
(2) the webhook handler writes the delivery row and the event in **one transaction**, with a unique
constraint on `(provider, event_id)` turning the duplicate into a clean `23505` → `409`/`200` replay.

The lesson is uncomfortable: **the "safety net" was the vulnerability.** Node's crash was protecting
the system from a handler that hid a data-corruption bug.

## Trade-offs

| Choice | Pros | Cons | When to use |
|--------|------|------|-------------|
| Log + flush + `exit(1)` on uncaught | clean death, visible, safe | restarts the pod | always |
| Log and continue | no downtime | undefined state, silent corruption | never |
| `process.exit(1)` directly after logging | simple | truncates buffered logs | only after an explicit flush |
| `close()` + `closeIdleConnections()` | prompt | needs Node ≥ 18.2 | default on Node ≥ 18.2 |
| Phased shutdown with a deadline | preserves in-flight work | more code | default |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Install the fatal handlers before anything else runs | Bootstrap first and hope the handlers are not needed |
| Normalize a non-`Error` reason before logging | Assume `reason.stack` exists |
| Flush telemetry before `process.exit()` | `process.exit()` right after `logger.error` |
| Exit non-zero so the orchestrator restarts you | Exit `0` after a fatal error |
| Run with `--unhandled-rejections=strict` | Rely on an undocumented default |
| Track in-flight requests so the drain can wait | Close the server and hope |
| Release idle keep-alive sockets explicitly | Let `close()` wait for them |
| Test the shutdown with a real `SIGTERM` under load | Only test the happy path |

## Common mistakes

- **Installing a "keep the server alive" `uncaughtException` handler** — the single most damaging
  line of code in this chapter.
- **`process.exit()` inside the fatal handler without flushing** — the log line explaining the crash
  is the one that gets lost.
- **A `try/catch` that swallows and returns `200`** — converts a failure into success-shaped output.
- **Closing the server before marking not-ready** — deploy-time `502`s.
- **Never counting in-flight work** — the drain cannot know when it is safe to exit.
- **Forgetting `closeIdleConnections()`** — the shutdown hangs until the orchestrator sends `SIGKILL`.

## Checklist

- [ ] Fatal handlers are installed before bootstrap and exit with code 1.
- [ ] The reason is normalized to an `Error` before logging.
- [ ] Telemetry and logs are flushed before exiting.
- [ ] `--unhandled-rejections=strict` is in the start command (CI and production).
- [ ] `--max-old-space-size` is ~70–75% of the container memory limit.
- [ ] Config is validated at boot with a strict schema; unknown keys fail.
- [ ] In-flight requests are tracked and awaited during the drain.
- [ ] The shutdown runs: not-ready → stop claiming → close → drain → flush → release → exit.
- [ ] `server.closeIdleConnections()` is called; `closeAllConnections()` is the escalation.
- [ ] The exit code is `1` when work was lost.
- [ ] A test asserts the exit code for an unhandled rejection, and a drill asserts the shutdown.

## Related

- [Graceful Shutdown Sequencing with SIGTERM — deep dive](../02-deep-dive/02-graceful-shutdown-sequencing.md)
- [Process Recovery Limits and When to Terminate — deep dive](../02-deep-dive/01-process-recovery-limits-and-termination.md)
- [Uncaught Exceptions and Unhandled Async Failures (41.1–41.2)](../01-concepts/01-uncaught-and-unhandled-failures.md)
- [Async Propagation and Unhandled Rejections](../../../part-05-exception-mechanics/12-exception-propagation-and-control-flow/02-deep-dive/02-async-propagation-and-unhandled-rejections.md)
- [Scheduled Tasks and Graceful Shutdown](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/03-practical-examples/02-scheduled-tasks-and-graceful-shutdown.md)
