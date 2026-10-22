# Async Layers: Workers, Scheduled Tasks, Bootstrap, and the Process Boundary

> Part IV · Chapter 9 · Sections 9.9–9.13 · _Estimated reading time: 20 min_
> **Prerequisite:** [The Layers of an Error-Handling Architecture](../01-concepts/01-layered-architecture-overview.md)

## In one sentence

**Background workers, scheduled tasks, bootstrap, and the process itself are layers with the same
discipline as HTTP handlers** — each owns a distinct failure class, and getting their contracts
wrong is how queues stall, crons double-charge, and half-wired services accept traffic.

## Why this matters in production

The HTTP path gets all the architecture attention; the async path gets `try/catch` and hope. The
resulting incidents are among the nastiest:

- A **poison job** fails forever, its retries clog the queue, and every other tenant's exports
  stop — no DLQ, no terminal state.
- A **nightly billing rollup** overlaps itself (the previous run is still going), producing
  double invoices — no run guard, no idempotency.
- A service **starts with an empty `DATABASE_URL`**, accepts traffic, and fails every request for
  six minutes — bootstrap did not fail fast.
- A process swallows `uncaughtException`, keeps serving with corrupted state, and leaks
  connections until the orchestrator kills it without a graceful drain.

Each of these is a *layer contract* failure, not a coding accident.

## Core concept — four layers, four jobs

| Layer | Failure class it owns | Its contract |
| ----- | --------------------- | ------------ |
| **Background worker** (9.9) | per-attempt job failure | classify retryable vs terminal; apply backoff; route exhausted jobs to DLQ; never decide business policy |
| **Scheduled task** (9.10) | per-*run* failure + overlap | prevent concurrent runs; make re-runs idempotent; record run outcome; never assume the last run succeeded |
| **Bootstrap** (9.11) | startup/init failure | validate config and dependencies **before** serving; fail fast with a clear cause; exit non-zero |
| **Process boundary** (9.12) | runtime failure of last resort | log safely, flush, terminate so a supervisor restarts clean; never attempt in-process recovery |

### 9.9 — Background worker

The worker wraps the same application service the HTTP path uses (Chapter 9's consistency rule),
and adds the job-specific decisions:

```ts
// workers/export-handler.ts — the worker's OWN jobs: classify, schedule, DLQ
export async function handleExport(msg: JobMessage, attempt: Attempt) {
  try {
    await runExport(msg.cmd);              // shared application service (handle-once owner)
    await attempt.ack();
  } catch (err) {
    const e = normalize(err);
    if (!isRetryable(e) || attempt.n >= MAX_ATTEMPTS) {
      await attempt.fail({ code: e.code, dlq: true, cause: e });  // terminal → DLQ
      return;
    }
    await attempt.retry({ delayMs: backoff(attempt.n), code: e.code });
  }
}
```

Key data: a recommended job contract is **max 5 attempts**, exponential backoff (base ~2 s,
factor 2, full jitter), terminal failures routed to a **DLQ** immediately, retryable failures
recorded with the same stable code on every attempt (Chapter 32 has the full policy).

### 9.10 — Scheduled task

Scheduled runs fail differently: the unit is the *run*, and the hazards are **overlap** and
**non-idempotent re-execution**.

- Guard with a run lock or an `runs` row unique on `(job_name, scheduled_for)` — a duplicate tick
  must fail as a duplicate, not run twice.
- Make each run idempotent (upsert by natural key), because schedulers redeliver after crashes.
- Record `succeeded | failed | skipped_overlap` with the error code — a silent skipped run is an
  undefined outcome, which this book forbids.

### 9.11 — Bootstrap

Bootstrap's error job is **halt**. Validate configuration and dependency reachability during
startup, before the listener opens:

```ts
// bootstrap.ts — fail fast, one clear cause, non-zero exit
const cfg = ConfigSchema.safeParse(process.env);
if (!cfg.success) {
  logger.fatal({ issues: cfg.error.issues }, "invalid configuration");
  process.exit(1);                       // terminal by design — no half-wired service
}
await db.ping();                         // or fail with DB_UNAVAILABLE at boot
app.listen(cfg.data.PORT);
```

Rules: **no request-serving before wiring completes**; startup failures are terminal (Chapters 41
and 58 cover the edge cases); the exit code and fatal log are the contract with the orchestrator.

### 9.12 — Process boundary

The process boundary owns what no layer above can handle: `uncaughtException`,
`unhandledRejection`, OOM, `SIGTERM`. Its contract is *terminate safely*, not *recover*:

```ts
process.on("uncaughtException", (err) => {
  logger.fatal({ err }, "uncaught exception — shutting down");
  flushLogsAndExit(1);                   // supervisor restarts a clean process
});
process.on("SIGTERM", () => drainAndExit(0)); // stop intake, finish in-flight, then exit
```

Key data: Kubernetes' default `terminationGracePeriodSeconds` is **30**; drain must finish within
it or in-flight requests die to `SIGKILL`. `SIGKILL` cannot be handled — the only defense is
finishing before it. Never "log and continue" after `uncaughtException`: in-process state
(pools, counters, locks) may already be corrupt.

## How the async layers connect to the request path

```text
 queue ──▶ WORKER 9.9 ──┐                        boot ──▶ BOOTSTRAP 9.11 (terminal on failure)
 cron  ──▶ SCHED  9.10 ─┼─▶ APPLICATION 9.4 ──▶ DOMAIN 9.5 ──▶ REPOSITORY 9.6 ──▶ INFRA 9.7
                        │              ▲
                        │              └── same handle-once decision as HTTP
                        └── renders job/run outcomes (attempt records), not HTTP
                 any layer escaping all of the above ──▶ PROCESS 9.12 (terminate)
```

## Key data / numbers

- Recommended job policy: **max 5 attempts**, backoff base **~2 s** (factor 2, jitter), DLQ on
  terminal or exhausted; poison messages are detected by *terminal classification*, not by
  attempt count alone.
- Scheduler overlap: unique run key `(job, scheduled_for)`; a second overlapping start is
  `SKIPPED_OVERLAP`, not success.
- Bootstrap: exit code **1** on config/init failure; readiness probe fails while booting so no
  traffic arrives early (Kubernetes: `readinessProbe` distinct from `livenessProbe`).
- Process: `SIGTERM` grace default **30 s** (Kubernetes), `SIGKILL` unhandleable, Node events
  `uncaughtException` / `unhandledRejection`.

## Real-world use case — Acme SaaS `ExportJob`

Acme's export worker had no DLQ and classified *every* error as retryable. One row with a
corrupt tenant ID made `ExportJob` fail forever; retries (3 layers deep — client, worker, queue
defaults) flooded Postgres, and exports for all tenants stalled for **47 minutes** until an
engineer spotted the growing queue.

The fix was purely contractual: the repository classified `DATA_INTEGRITY` as terminal, the worker
honored it (immediate `failed` + DLQ entry with the stable code), retries were capped at 5 with
jittered backoff, and the run record carried the code. The same poison row now fails in under a
second, alone, with a replayable DLQ entry.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Async layers with explicit contracts (recommended) | No stalled queues/crons; testable | More scaffolding (attempt records, run guards) | Any production queue or cron |
| `try/catch` + `console.error` in the worker | Tiny | Poison jobs, undefined outcomes, silent skips | Never beyond a demo |
| Bootstrap validates lazily on first request | Fast boot | Half-wired service takes traffic; confusing 5xx storm | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Reuse the application service inside workers | Re-implement business logic in the worker |
| Give every job attempt a max + DLQ path | Retry indefinitely "until it works" |
| Guard scheduled runs against overlap | Assume the previous run finished |
| Fail fast at bootstrap with exit code 1 | Serve traffic with invalid config |
| Terminate on `uncaughtException` | Continue after an uncaught exception |

## Common mistakes

- **Worker-as-second-handler** — the worker catches domain errors and invents its own policy,
  diverging from HTTP behavior (see `05-avoiding-duplicate-handling-and-consistent-flow.md`).
- **Classifying by attempt count only** — a permanent error retried 5 times is still permanent;
  classify by code first, attempts second.
- **Liveness probe as readiness** — restarting on boot validation failures causes crash loops;
  fail readiness, exit only on genuinely unrecoverable init.

## Checklist

- [ ] Workers call the same application service as HTTP entry points.
- [ ] Every job type has a terminal classification and a DLQ destination.
- [ ] Scheduled runs have an overlap guard and an idempotent body.
- [ ] Config and dependencies are validated before the listener opens.
- [ ] `uncaughtException`/`SIGTERM` handlers exist and terminate, not continue.

## Related

- [The Layers of an Error-Handling Architecture](../01-concepts/01-layered-architecture-overview.md)
- [ExportJob Through the Worker Layers](../03-practical-examples/02-exportjob-through-worker-layers.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- [Chapter 41 — Process, Runtime, and Resource Failures](../../../part-15-distributed-failures/41-process-runtime-and-resource-failures/README.md)
