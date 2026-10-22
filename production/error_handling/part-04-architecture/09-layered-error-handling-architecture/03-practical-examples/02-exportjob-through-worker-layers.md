# `ExportJob` Through the Worker Layers

> Part IV · Chapter 9 · Sections 9.6–9.10 · _Estimated reading time: 20 min_
> **Prerequisite:** [Async Layers: Workers, Scheduled Tasks, Bootstrap](../02-deep-dive/02-async-layers-workers-and-scheduled-tasks.md)

## In one sentence

A queued `ExportJob` travels the **same** repository, domain, and application layers as an HTTP
request, with the **worker and queue owning only job-shaped decisions**: attempt counts, backoff,
terminal classification, and the DLQ.

## Why this matters in production

Background paths rot quietly. The HTTP endpoint gets the careful `409`/`503` mapping; the worker
gets `catch (e) { fail(e) }`. The consequences: permanent errors burn all retries before failing,
transient errors kill jobs on the first blip, and the *same underlying fault* produces two
different codes depending on whether a user or a cron triggered it — which breaks alerting,
dashboards, and every runbook that says "if you see `X`, do `Y`."

## The job and its layer path

```text
 queue ──▶ BACKGROUND WORKER 9.9 ──▶ APPLICATION 9.4 ──▶ DOMAIN 9.5 ──▶ REPOSITORY 9.6 ──▶ INFRA 9.7
 (attempt,        (classify,          (runExport:        (export         (rows,             (pool,
  backoff,         ack/retry/fail)      one decision)      rules)          checkpoints)       S3 SDK)
  DLQ)
```

**Message envelope** (the worker's contract with the queue):

```json
{
  "jobType": "export.create",
  "jobId": "job_9f21c",
  "tenantId": "tnt_8412",
  "attempt": 1,
  "maxAttempts": 5,
  "enqueuedAt": "2026-10-14T09:12:03Z",
  "correlationId": "corr_5b8e0d"
}
```

## Step 1 — Worker receives the attempt (layer 9.9)

```ts
// workers/export-handler.ts
export async function onExportJob(msg: ExportMessage) {
  const attempt = { n: msg.attempt, max: msg.maxAttempts };
  try {
    const outcome = await runExport(msg);        // application service — the ONE decision point
    if (outcome.status === "failed") {
      await queue.fail(msg, { code: outcome.code, dlq: true });   // business-terminal
      return;
    }
    await queue.ack(msg);
  } catch (err) {
    const e = normalize(err);                    // same normalizer as the HTTP path
    const record = { code: e.code, correlationId: msg.correlationId, cause: e };

    if (!isRetryable(e)) {
      await queue.fail(msg, { ...record, dlq: true });            // permanent → DLQ now
    } else if (attempt.n >= attempt.max) {
      await queue.fail(msg, { ...record, dlq: true, reason: "retries_exhausted" });
    } else {
      await queue.retry(msg, { delayMs: backoff(attempt.n), ...record });
    }
  }
}
```

The worker performs **only** job decisions: *ack / retry / fail-to-DLQ*. It does not inspect
Stripe payloads, does not map HTTP statuses, and does not contain business rules.

## Step 2 — Application service runs the use case (layer 9.4)

```ts
// app/run-export.ts — identical whether called from HTTP "export now" or from the queue
export async function runExport(msg: ExportMessage): Promise<ExportOutcome> {
  const exportRec = await exportsRepo.get(msg.jobId);      // RECORD_NOT_FOUND → terminal
  const scope = await tenants.dataScope(msg.tenantId);      // FORBIDDEN_SCOPE → terminal
  await exporters[exportRec.format].run(exportRec, scope); // domain + integration errors propagate
  await exportsRepo.markSucceeded(msg.jobId);
  return { status: "ok" };
}
```

Decisions live here: a `FORBIDDEN_SCOPE` (tenant downgraded mid-export) is terminal — no amount
of retrying re-grants access; a `DB_UNAVAILABLE` is allowed to propagate retryable so the worker
can schedule attempts.

## Step 3 — Repository and infrastructure translate (layers 9.6–9.7)

```ts
// repo/export-repo.ts — checkpoint writes are the resume point
async function saveCheckpoint(id: string, offset: number) {
  try {
    await this.db.none("UPDATE exports SET offset = $2 WHERE id = $1", [id, offset]);
  } catch (err) {
    if (isSqlState(err, "40001") || isSqlState(err, "40P01"))
      throw { code: "DB_UNAVAILABLE", retryable: true, cause: err };
    throw { code: "DB_WRITE_FAILED", retryable: false, cause: err };
  }
}
```

```ts
// infra/s3.ts — storage failures keep their retryability honest
try { await s3.upload(params).promise(); }
catch (err) {
  if (isSlowDown(err) || isTimeout(err)) throw { code: "STORAGE_UNAVAILABLE", retryable: true, cause: err };
  if (isAccessDenied(err))               throw { code: "STORAGE_ACCESS_DENIED", retryable: false, cause: err };
  throw { code: "STORAGE_UPLOAD_FAILED", retryable: false, cause: err };
}
```

**Checkpoints make retries safe**: on attempt N the export resumes from `offset`, so a retried
job does not duplicate rows in the S3 object (the classic `ExportJob` duplicate-rows bug from
Chapter 1).

## Step 4 — Domain enforces export rules (layer 9.5)

```ts
// domain/export-rules.ts — pure, no imports from queue or storage
if (exportRec.expiresAt < now()) throw new DomainError("EXPORT_EXPIRED");       // terminal
if (rowsPlanned(exportRec) > MAX_ROWS) throw new DomainError("EXPORT_TOO_LARGE"); // terminal
```

Both are non-retryable: the worker's `isRetryable(e)` consults the registry, not the exception
text.

## Step 5 — Scheduled sibling (layer 9.10)

The nightly CSV rollup uses the same layers with run semantics:

| Event | Outcome recorded |
| ----- | ---------------- |
| previous run still active | `SKIPPED_OVERLAP` (run lock rejected; not success, not failure) |
| run succeeds | `succeeded` |
| run throws `EXPORT_EXPIRED` | `failed`, code recorded, **no** retry |
| run throws `DB_UNAVAILABLE` | `failed`, retryable → next tick re-runs idempotently |

## The classification table this job relies on

| Code (stable) | Retryable | Job action | Attempt limit |
| ------------- | --------- | ---------- | ------------- |
| `DB_UNAVAILABLE` | ✅ | delayed retry, backoff | 5 |
| `STORAGE_UNAVAILABLE` | ✅ | delayed retry, backoff | 5 |
| `UPSTREAM_RATE_LIMITED` | ✅ | retry honoring `Retry-After` | 5 |
| `DB_WRITE_FAILED` | ❌ | fail → DLQ immediately | 1 |
| `STORAGE_ACCESS_DENIED` | ❌ | fail → DLQ immediately, alert | 1 |
| `EXPORT_EXPIRED` | ❌ | fail (business terminal, no DLQ alert) | 1 |
| `EXPORT_TOO_LARGE` | ❌ | fail + notify requestor | 1 |
| unknown / unclassified | ⚠️ | retry once, then DLQ | 2 |

## Key data / numbers

- Recommended policy: **max 5 attempts**, exponential backoff base **~2 s** (factor 2, full
  jitter); terminal codes skip retries entirely.
- DLQ record minimum: stable `code`, `jobId`, `tenantId`, `correlationId`, `attempt`, last
  `cause` message (sanitized), `enqueuedAt`.
- Checkpoint granularity recommendation: every **1 000–10 000 rows** (or ~30 s of work) so a
  retry re-does bounded work.
- Duplicate-row hazard without checkpoints + idempotent object keys: observed multipliers of
  **2×** rows on naive retries (see Chapter 1).

## Real-world use case — Acme SaaS

Acme's worker originally did `catch (e) { await queue.retry(msg); }` — every failure retried 5
times. Two incidents followed: a `STORAGE_ACCESS_DENIED` (rotated IAM key) hammered S3 for 11
minutes across hundreds of jobs, and a poison row with a corrupt tenant reference produced
duplicate CSV rows in customer exports because attempts restarted from offset 0.

After the layering above: access-denied failed on attempt 1 to the DLQ with an alert, transient
storage errors retried with jittered backoff, and checkpoints + deterministic object keys made
retries row-exact. The customer-facing duplicate-row report rate went to zero.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Shared application service + job-shaped shell (shown) | One decision point, consistent codes | Requires outcome type discipline | Default for all jobs |
| Worker re-implements flow | Independent evolution | Drifts from HTTP behavior; double policies | Never |
| Infinite retries "until green" | Simple | Poison jobs stall the queue forever | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify by stable code before counting attempts | Classify by `e.message` text |
| Checkpoint long jobs so retries are cheap | Restart exports from offset 0 on retry |
| DLQ terminal failures immediately | Burn 5 attempts on a permanent error |
| Record the same code on every attempt | Use different codes per attempt |

## Common mistakes

- **Business terminal ≠ technical terminal** — `EXPORT_EXPIRED` must not alert on-call; a DLQ
  entry without a page, unlike `STORAGE_ACCESS_DENIED`.
- **Worker-side normalization duplicating the repository's** — call the shared normalizer; two
  translators = two vocabularies.
- **Retrying without idempotency** — before any retry, the operation needs a checkpoint, an
  idempotency key, or a deterministic result (Chapter 28).

## Checklist

- [ ] The worker contains no HTTP mapping and no business rules.
- [ ] Every code has a retryable/terminal verdict in the registry.
- [ ] Long jobs checkpoint; retries resume rather than restart.
- [ ] DLQ entries carry code + correlation ID + attempt.
- [ ] The same code appears for a fault raised via HTTP and via the queue.

## Related

- [Async Layers: Workers, Scheduled Tasks, Bootstrap](../02-deep-dive/02-async-layers-workers-and-scheduled-tasks.md)
- [A `Checkout` Request Through Every Layer](./01-checkout-request-through-every-layer.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- [Chapter 9 Reference — layer matrix](../05-reference/README.md)
