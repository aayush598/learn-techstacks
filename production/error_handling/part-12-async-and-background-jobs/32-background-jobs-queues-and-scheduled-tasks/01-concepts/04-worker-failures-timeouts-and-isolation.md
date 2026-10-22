# Worker Failures, Timeouts, Shutdown, and Isolation

> Part XII · Chapter 32 · Sections 32.10–32.13, 32.19 · _Estimated reading time: 18 min_
> **Prerequisite:** [Job Lifecycle and Failure States](./01-job-lifecycle-and-failure-states.md)

## In one sentence

Workers are **mortal and duplicated**: they time out, crash, get killed during deploys, and receive
the same message twice — so every job must be time-bounded, cancellation-aware, idempotent, and
isolated from other jobs.

## Why this matters in production

The most common background-job incident is not a bug in the business logic; it is a **deploy** or a
**slow job**. A rolling deploy sends `SIGTERM` while an export is writing to S3; the worker is killed,
the message redelivers, and the job runs twice. A job that ignores its lease timeout keeps running
after the queue has already reassigned it, causing concurrent writes to the same record. This section
is about surviving the infrastructure realities that make jobs fail.

## 32.10 — Timeout and cancellation

Every job needs a **maximum runtime** that is shorter than the queue's lease/visibility timeout.
Otherwise the queue redelivers the message while the first worker is still working.

```text
visibilityTimeout = 300 s
jobDeadline       = 240 s   ← leaves 60 s for cleanup + ack
```

```ts
async function runWithBudget(job: Job, handler: (s: AbortSignal) => Promise<void>) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(new DOMException("job deadline", "TimeoutError")), job.deadlineMs);

  try {
    await handler(controller.signal);
  } finally {
    clearTimeout(timer);
  }
}
```

Cancellation sources for a job:

| Source | Meaning | Terminal state |
| ------ | ------- | -------------- |
| Deadline exceeded | Job ran too long | `failed` (timeout, retryable) |
| `SIGTERM` | Worker is shutting down | Requeue / redeliver |
| Operator cancel | Deliberate stop | `cancelled` |
| Tenant deleted | Work no longer needed | `cancelled` |

Long jobs should **renew their lease** (heartbeat) or split into smaller jobs. A 3-hour export with a
5-minute visibility timeout will be redelivered six times unless you extend the lease.

## 32.11 — Worker crashes

A crash (OOM, `SIGKILL`, node failure) leaves no chance to ack or clean up. The queue detects the
expired lease and redelivers. Consequences:

- **At-least-once** means the job may already have partially or fully run.
- **In-memory state is gone** — checkpoints must be durable (32.15).
- **Locks may persist** until their TTL expires — use short TTLs with renewal.

```text
worker A: claim → work → 💥 crash (no ack)
queue:    lease expires → message visible again
worker B: claim → work (possibly duplicate side effect)
```

The correct response is not to prevent crashes (you cannot) but to make re-execution safe:

1. **Idempotent writes** keyed by job id / business key.
2. **Durable checkpoints** so B resumes instead of restarting.
3. **Short lock TTLs** so a dead worker's lock does not block the tenant.
4. **Crash-loop detection** — if a job crashes the worker (e.g., OOM), count it as a poison candidate.

> ⚠️ **Hazard.** A job that OOMs the process on every attempt looks like "worker instability," not
> "bad job," unless you correlate crashes with the message being processed.

## 32.12 — Shutdown during processing

Graceful shutdown is a **protocol**, not a flag:

```ts
let shuttingDown = false;

process.on("SIGTERM", async () => {
  shuttingDown = true;          // 1. stop accepting new work
  await consumer.pause();       // 2. stop polling the queue
  await Promise.race([          // 3. drain in-flight jobs
    currentJobs.allSettled(),
    sleep(GRACE_MS),            //     bounded by the platform grace period
  ]);
  await consumer.close();       // 4. ack/nack finished, release leases
  process.exit(0);
});
```

Rules:

1. **Stop polling first**, then drain. Otherwise new jobs keep arriving during shutdown.
2. **Finish or explicitly nack in-flight jobs.** An unacked job redelivers (safe if idempotent) but
   may duplicate work.
3. **Keep the grace period shorter than the platform's.** Kubernetes defaults to 30 s; finish
   within ~25 s.
4. **Do not start a new long job after `shuttingDown` is set.**
5. **Flush telemetry and release locks** before exit.

## 32.13 — Duplicate delivery

Queues deliver **at-least-once**. Duplicates come from:

- Worker crash after the side effect but before ack.
- Visibility timeout expiring during a long job.
- Client/queue network errors causing a redelivery.
- DLQ replay.
- FIFO "exactly-once" only within a dedupe window; it is not absolute.

The only robust defense is **idempotency at the effect boundary**:

```ts
// Deterministic key: same job -> same row/key/charge.
const key = `export:${job.id}`;

await db.transaction(async (tx) => {
  const existing = await tx.exports.findByKey(key);
  if (existing) return existing;             // replay: return prior result
  return tx.exports.create({ key, ...job.data });
});
```

For external effects (payments, emails), pass the job id as the provider idempotency key
(e.g., `Idempotency-Key`). Deduplicate *before* the side effect where possible, and make the check
and the write atomic.

## 32.19 — Isolation between jobs

One misbehaving job class must not starve every other job:

| Isolation axis | Mechanism | Protects against |
| -------------- | --------- | ---------------- |
| Queue per job type | Separate queues | Head-of-line blocking |
| Worker pool per queue | Dedicated consumers | Noisy neighbor |
| Per-tenant concurrency | Semaphore / token bucket | One tenant monopolizing |
| Bulkhead per dependency | Separate pools/limits | Dependency exhaustion |
| CPU/memory limits | Container limits | OOM killing the whole host |
| Timeouts per job type | Distinct deadlines | Long jobs holding slots |

```ts
const tenantSem = new Map<string, Semaphore>();

async function withTenantSlot(tenantId: string, fn: () => Promise<void>) {
  const sem = tenantSem.get(tenantId) ?? new Semaphore(2); // max 2 concurrent per tenant
  tenantSem.set(tenantId, sem);
  await sem.acquire();
  try {
    await fn();
  } finally {
    sem.release();
  }
}
```

A single queue for `ExportJob`, `SendEmail`, and `AgentRun` means a 10-minute export delays every
password-reset email. Split queues by latency class and cost.

## Worked example — ExportJob shutdown

Acme deploys workers with `SIGTERM` and a 30 s grace period. The old worker did not pause the
consumer; new exports were claimed during shutdown and then killed, leaving `running` records with
no result.

```ts
process.on("SIGTERM", async () => {
  await consumer.pause();                              // no new claims
  const drained = await Promise.race([
    inFlight.allSettled(),
    sleep(25_000).then(() => "timeout" as const),
  ]);
  if (drained === "timeout") {
    for (const job of inFlight.pending()) await jobs.requeue(job.id); // explicit nack
  }
  await consumer.close();
  process.exit(0);
});
```

After the change, deploys stopped producing orphaned `running` jobs; duplicates dropped to zero for
jobs that completed within the grace period.

## Key data / numbers

- Kubernetes default `terminationGracePeriodSeconds`: **30 s**.
- SQS visibility timeout default **30 s**, max **12 h**; extend with `ChangeMessageVisibility`.
- SQS max long-poll wait: **20 s**.
- Typical job deadline = visibility timeout − (cleanup + ack margin), often **80–90%**.
- FIFO dedupe window: **5 minutes** (SQS FIFO); duplicates outside the window are possible.
- Recommended per-tenant concurrency: **2–10** depending on cost.

## Real-world use case — Acme SaaS

Acme ran all jobs in one worker pool. A tenant created a 5 GB export; the job consumed all 8 workers
for 40 minutes, delaying invoice generation and password-reset emails across the platform. They split
queues by latency class (`interactive`, `bulk`), capped bulk workers at 3, added a per-tenant
semaphore, and set a 20-minute deadline with checkpoint/resume. Interactive job p95 latency returned
to under 2 s during bulk exports.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One shared queue | Simple | Head-of-line blocking | Tiny systems |
| Queue per job type | Isolation | More infra | Default for mixed workloads |
| Long lease + heartbeat | Fewer redeliveries | Complexity | Long jobs |
| Short lease, short jobs | Simple recovery | Duplicate work | Small units |
| Forced kill on shutdown | Fast deploys | Orphaned work | Stateless, idempotent jobs |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Set job deadline below the lease | Let jobs outlive the visibility timeout |
| Pause polling on `SIGTERM` | Keep claiming during shutdown |
| Drain in-flight work with a bound | Kill mid-write |
| Make effects idempotent | Assume exactly-once delivery |
| Isolate queues by latency/cost | Mix exports and password resets |
| Cap per-tenant concurrency | Let one tenant consume all workers |

## Common mistakes

- **Deadline > visibility timeout** — the job runs twice concurrently.
- **No heartbeat for long jobs** — constant redelivery.
- **Acking after shutdown begins** — duplicates or lost work.
- **Retrying a crash-looping job forever** — one OOM job takes down every worker.
- **One pool for all queues** — noisy neighbor starves interactive work.

## Checklist

- [ ] Is every job deadline shorter than its lease/visibility timeout?
- [ ] Do long jobs renew their lease or checkpoint?
- [ ] Does `SIGTERM` pause polling and drain with a bound?
- [ ] Are in-flight jobs finished or explicitly requeued?
- [ ] Is every side effect idempotent under duplicate delivery?
- [ ] Are queues split by latency class and cost?
- [ ] Is per-tenant concurrency capped?
- [ ] Are crash-looping jobs detected as poison candidates?

## Related

- [Partial Completion and Failure Contracts](./05-partial-completion-and-failure-contracts.md)
- [At-least-once vs Exactly-once](../02-deep-dive/02-at-least-once-vs-exactly-once.md)
- [Scheduled Tasks and Graceful Shutdown](../03-practical-examples/02-scheduled-tasks-and-graceful-shutdown.md)
- [Scheduled Tasks and Graceful Shutdown](../03-practical-examples/02-scheduled-tasks-and-graceful-shutdown.md)
