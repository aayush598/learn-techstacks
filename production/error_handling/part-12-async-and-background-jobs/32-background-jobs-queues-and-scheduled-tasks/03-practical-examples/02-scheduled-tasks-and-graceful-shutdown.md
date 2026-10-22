# Practical — Scheduled Tasks and Graceful Shutdown

> Part XII · Chapter 32 · Sections 32.12, 32.18, 32.19 · _Estimated reading time: 17 min_
> **Prerequisite:** [Worker Failures, Timeouts, Shutdown, and Isolation](../01-concepts/04-worker-failures-timeouts-and-isolation.md)

## Scenario

Acme runs a nightly per-tenant export at 02:00 UTC and a weekly usage rollup at 03:00 UTC on Sunday.
Both run on the same worker fleet that processes ad-hoc `ExportJob`s. Deploys happen during the day,
and the nightly job occasionally runs past the next deploy window. The current implementation has
produced: overlapping nightly runs for large tenants, a failed deploy that left `running` jobs with
no result, and one tenant's rollup delaying all other tenants by 40 minutes.

## Goals

- **No overlapping runs** for the same tenant and schedule window.
- **Missed runs are detectable and recoverable.**
- **`SIGTERM` stops new claims and drains in-flight work** within the platform grace period.
- **Scheduled work is isolated** from interactive work.

## Step 1 — Idempotency keyed by the schedule window

```ts
function nightlyKey(tenantId: string, dayUtc: string): string {
  return `nightly-export:${tenantId}:${dayUtc}`; // dayUtc = YYYY-MM-DD
}

async function enqueueNightly(tenantId: string) {
  const dayUtc = new Date().toISOString().slice(0, 10);
  await jobs.enqueueOnce(
    "ExportJob",
    { jobId: nightlyKey(tenantId, dayUtc), tenantId, query: { from: dayUtc, to: dayUtc } },
    { key: nightlyKey(tenantId, dayUtc) },
  );
}
```

Keying on `Date.now()` or the scheduler's fire time guarantees duplicates when a retry or a second
scheduler instance fires. Keying on the **window** makes re-delivery a no-op.

## Step 2 — Overlap protection with a lease

```ts
const SCHEDULE_LEASE_MS = 90 * 60_000; // longer than the p99 nightly run

async function runNightly(tenantId: string) {
  const key = `lock:nightly:${tenantId}`;
  const lease = await locks.acquire(key, { ttlMs: SCHEDULE_LEASE_MS, wait: false });

  if (!lease) {
    metrics.increment("nightly_skipped_overlap", { tenantId });
    return; // previous run still active
  }

  try {
    await exports.runNightly(tenantId);
  } finally {
    await lease.release().catch((e) => log.error({ e, tenantId }, "lease release failed"));
  }
}
```

The lock TTL must exceed the longest expected run. A short TTL re-introduces overlap; a very long TTL
delays recovery after a crash. Renew the lease if runs can exceed it.

## Step 3 — Detect missed runs

Overlap protection and catch-up are complementary. Track the last successful window:

```ts
async function checkMissedWindows(tenantId: string) {
  const last = await schedules.lastSuccess("nightly-export", tenantId);
  const yesterday = utcDateDaysAgo(1);

  if (!last || last < yesterday) {
    metrics.increment("nightly_missed", { tenantId, last: last ?? "never" });
    await enqueueNightly(tenantId); // idempotent catch-up for yesterday
  }
}
```

```yaml
alarm:
  metric: nightly_export_success_age_hours
  threshold: 26
  description: "No successful nightly export for a tenant in 26h"
```

A cron that silently stops firing is the most common scheduled-task incident. Alarm on **success
recency**, not just on failure logs.

## Step 4 — Isolate scheduled work

```yaml
queues:
  interactive-jobs:      # password resets, webhook projections
    concurrency: 12
  scheduled-jobs:        # nightly exports, rollups
    concurrency: 4
  bulk-exports:          # ad-hoc large exports
    concurrency: 2
```

Scheduled and interactive jobs share code but not capacity. A nightly export must not delay a
password reset, and an ad-hoc 5 GB export must not block the nightly run.

Within the scheduled queue, cap per-tenant concurrency:

```ts
await withTenantSlot(tenantId, 1, () => exports.runNightly(tenantId));
```

## Step 5 — Graceful shutdown protocol

```ts
class Worker {
  private shuttingDown = false;
  private inflight = new Set<Promise<unknown>>();

  async start() {
    process.on("SIGTERM", () => void this.shutdown("SIGTERM"));
    process.on("SIGINT", () => void this.shutdown("SIGINT"));

    while (!this.shuttingDown) {
      const messages = await this.consumer.receive({ max: 10, waitSeconds: 20 });
      for (const m of messages) this.track(this.handle(m));
    }
  }

  private track(p: Promise<unknown>) {
    this.inflight.add(p);
    p.finally(() => this.inflight.delete(p));
  }

  private async shutdown(signal: string) {
    if (this.shuttingDown) return;
    this.shuttingDown = true;
    log.info({ signal }, "shutdown started");

    await this.consumer.pause();                       // stop new claims

    const drained = await Promise.race([
      Promise.allSettled([...this.inflight]),           // wait for in-flight
      sleep(25_000).then(() => "timeout" as const),     // below 30s grace
    ]);

    if (drained === "timeout") {
      await this.consumer.requeueAll();                 // explicit nack
      log.warn("shutdown grace exceeded; requeued in-flight jobs");
    }

    await this.consumer.close();
    await telemetry.flush();
    process.exit(0);
  }
}
```

Key points:

1. **Pause before draining** — otherwise new messages keep arriving.
2. **25 s drain < 30 s grace** — leaves time to close and flush.
3. **Explicit requeue on timeout** — an unacked message redelivers anyway, but requeue makes the
   intent explicit and lets you record the reason.
4. **`allSettled`** — one failing job must not skip waiting for the rest.

## Step 6 — Shutdown-aware job handler

```ts
async function handleExport(msg: SQSMessage, signal: AbortSignal) {
  if (signal.aborted) return;                 // do not start new work
  const payload = parse<ExportPayload>(msg.Body);

  await exports.run(payload, { signal });     // cooperative cancellation
  await jobs.markSucceeded(payload.jobId);
}
```

The worker passes a per-job abort signal tied to both the job deadline and shutdown. When shutdown
fires, long exports stop at the next checkpoint, persist progress, and exit cleanly. The
checkpointed resume (Chapter 32.15) makes the redelivered message cheap.

## Failure-mode review

| Event | Behavior | Result |
| ----- | -------- | ------ |
| Two schedulers fire | Lease + window key | One run |
| Previous run still active | Lease not acquired | Skip + metric |
| Scheduler misses a day | Missed-window check | Catch-up with same key |
| Deploy at 02:10 | Pause + drain ≤25 s | In-flight finishes or requeues |
| `SIGKILL` during run | Lease expires; message redelivers | Resume from checkpoint |
| Nightly run > lease TTL | Renew lease | No overlap |
| Large tenant export | Per-tenant slot | Other tenants unaffected |

## Real-world use case — Acme SaaS

Acme's nightly job ran on two scheduler replicas without a lock. For 3 weeks, every tenant's export
ran twice; duplicate CSVs were uploaded and duplicate "your export is ready" emails sent (providers
did not dedupe). The team added a per-tenant lease keyed by schedule window, window-based job ids,
and a "missed run" alarm. Duplicate emails went to zero. Separately, deploys were killing in-flight
jobs; the graceful shutdown above reduced orphaned `running` records from ~30 per deploy to zero.

## Key data / numbers

- Nightly schedule: **02:00 UTC**; weekly rollup: **03:00 UTC Sunday**.
- Schedule lease TTL: **90 min**, renewed if a run exceeds 60 min.
- Shutdown drain: **25 s** inside Kubernetes' **30 s** grace.
- Missed-run alarm: no success for **26 h**.
- Per-tenant scheduled concurrency: **1**; scheduled queue concurrency: **4**.
- Catch-up window: **1 day** (larger gaps need explicit backfill approval).

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Key idempotency on the schedule window | Key on wall-clock time |
| Acquire a per-tenant lease | Allow overlapping runs |
| Alarm on success recency | Only alarm on errors |
| Isolate scheduled/bulk queues | Share one pool with interactive jobs |
| Pause the consumer before draining | Keep claiming during shutdown |
| Requeue on drain timeout | Kill in-flight work silently |
| Resume from a checkpoint after requeue | Restart long exports from zero |

## Checklist

- [ ] Is the schedule idempotency key derived from the window?
- [ ] Is there a per-tenant lease with a TTL > p99 runtime?
- [ ] Is there an alarm for missed successful runs?
- [ ] Is scheduled work isolated from interactive work?
- [ ] Does `SIGTERM` pause polling before draining?
- [ ] Is the drain budget below the platform grace period?
- [ ] Are in-flight jobs requeued explicitly on timeout?
- [ ] Do handlers respect cancellation and checkpoint progress?

## Related

- [Job Lifecycle and Failure States](../01-concepts/01-job-lifecycle-and-failure-states.md)
- [Worker Failures, Timeouts, Shutdown, and Isolation](../01-concepts/04-worker-failures-timeouts-and-isolation.md)
- [ExportJob Worker with DLQ and Backoff](./01-exportjob-worker-with-dlq-and-backoff.md)
- [Worker Failures, Timeouts, and Isolation](../01-concepts/04-worker-failures-timeouts-and-isolation.md)
