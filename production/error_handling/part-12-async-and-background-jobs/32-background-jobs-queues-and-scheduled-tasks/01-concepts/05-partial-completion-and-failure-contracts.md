# Partial Completion, Checkpointing, and Failure Contracts

> Part XII · Chapter 32 · Sections 32.14–32.16, 32.20, 32.22 · _Estimated reading time: 18 min_
> **Prerequisite:** [Worker Failures, Timeouts, Shutdown, and Isolation](./04-worker-failures-timeouts-and-isolation.md)

## In one sentence

Long jobs **finish partway** and then fail, so you need durable **checkpoints** to resume, explicit
**compensation** for irreversible steps, and a **standard error contract** that tells the next
attempt (or the operator) exactly where the job stopped.

## Why this matters in production

A 2-hour export that fails at 90% and restarts from zero multiplies cost and latency by ten. Worse, if
the first 90% already published rows or sent emails, restarting duplicates them. Partial completion
without checkpointing is either expensive (full restart) or corrupting (duplicate effects).
Checkpointing makes progress durable; compensation makes already-completed side effects reversible;
the error contract makes both decisions reconstructable after a crash.

## 32.14 — Partial completion

A job can complete some units of work before failing:

| Partial shape | Example | Safe strategy |
| ------------- | ------- | ------------- |
| Idempotent rows | Export writes keyed by `(jobId, rowId)` | Resume from last committed row |
| External side effects | Emails sent per recipient | Track sent set; skip on resume |
| Multi-step workflow | Reserve → charge → provision | Compensation for completed steps |
| Batch items | 10k records, 300 invalid | Report per-item; continue valid ones |

Rules:

1. **Persist progress before acknowledging the unit.** The checkpoint and the effect should be
   committed together (same transaction where possible).
2. **Report partial results** rather than discarding them.
3. **Never mark a partial job `succeeded`** unless the contract says partial is success.
4. **Make each unit idempotent** so a resume that redoes the last unit is harmless.

## 32.15 — Checkpointing and resume

A **checkpoint** is durable progress: `lastProcessedOffset`, `lastCommittedRowId`, `stage`,
`completedItems`. On restart, the job resumes from it.

```ts
type ExportCheckpoint = {
  jobId: string;
  queryHash: string;       // detect input changes between attempts
  lastRowId: string | null;
  rowsWritten: number;
  tempObjectKey: string;
  updatedAt: string;
};
```

```ts
async function exportWithResume(job: Job<ExportPayload>) {
  const cp = (await checkpoints.get(job.id)) ?? {
    jobId: job.id,
    queryHash: hash(job.data.query),
    lastRowId: null,
    rowsWritten: 0,
    tempObjectKey: `tmp/${job.id}.csv`,
  };

  if (cp.queryHash !== hash(job.data.query)) {
    throw new NonRetryableJobError("EXPORT_INPUT_CHANGED"); // checkpoint is stale
  }

  const stream = db.streamRowsAfter(job.data.query, cp.lastRowId);

  for await (const batch of batches(stream, 1_000)) {
    await s3.append(cp.tempObjectKey, toCsv(batch));       // durable append
    cp.lastRowId = batch.at(-1)!.id;
    cp.rowsWritten += batch.length;
    await checkpoints.save(cp);                            // commit progress
  }

  await s3.commit(cp.tempObjectKey, finalKey(job));        // atomic publish
  await checkpoints.complete(job.id);
}
```

### Resume is at-least-once

The checkpoint may lag the effect by one batch. On resume you may **reprocess the last batch**, so
the write must be idempotent:

- Use deterministic object keys / row keys.
- Append with a dedupe key, or write batches to separate part files named by offset.
- Verify the checkpoint's `queryHash` so a changed input does not silently resume a stale plan.

### When not to checkpoint

- Jobs under a few seconds: the overhead exceeds the benefit.
- Jobs with no natural ordering key: resuming requires a stable cursor.
- Jobs whose units are not idempotent: restart-and-compensate may be safer.

## 32.16 — Compensation

Compensation is the **business-level undo** of a completed step. It is not a database rollback; the
effect already left the transaction.

| Completed step | Compensation |
| -------------- | ------------ |
| Charged a card | Refund / void authorization |
| Reserved inventory | Release reservation |
| Sent an email | Send correction (cannot unsend) |
| Created a tenant resource | Deprovision / mark deleted |
| Wrote a published object | Delete or supersede with a tombstone |

```ts
type Step = { name: string; run: () => Promise<void>; undo: () => Promise<void> };

async function saga(steps: Step[]) {
  const done: Step[] = [];
  try {
    for (const step of steps) {
      await step.run();
      done.push(step);
    }
  } catch (err) {
    for (const step of done.reverse()) {
      // Compensation must be idempotent and must not mask the original error.
      await step.undo().catch((e) => log.error({ e, step: step.name }, "compensation failed"));
    }
    throw err;
  }
}
```

Compensation rules:

1. **Only compensate completed steps**, in reverse order.
2. **Compensation is itself retryable and idempotent.**
3. **A failed compensation is an incident** — it can leave inconsistent state; alert.
4. **Some effects are irreversible** (email sent); prefer a corrective action plus a support path.
5. **Record compensation in the job record** so replay does not compensate twice.

> ⚠️ **Hazard.** A job that retries after a *successful* compensation can re-charge the customer.
> Gate the retry on a terminal state transition, not just on the exception.

## 32.20 — Preserving failure context

When a job fails, the next actor is a human or a replay script. Both need context:

| Field | Why |
| ----- | --- |
| `jobId`, `tenantId`, `jobType` | Identify and scope |
| `attempt`, `maxAttempts` | Explain exhaustion |
| `errorCode` (stable) | Group and alert |
| `errorClass` (retryable/terminal) | Decide replay |
| `lastSuccessfulCheckpoint` | Resume point |
| `input` (or a safe reference) | Reproduce |
| `startedAt`, `finishedAt` | Duration/overlap analysis |
| `workerId`, `region` | Infrastructure correlation |

Do **not** dump raw stack traces or provider payloads that may contain secrets or PII
(Chapter 36). Store a safe summary plus a reference to redacted diagnostics.

## 32.22 — Standard job error contract

Every job type should emit the same failure shape:

```ts
type JobFailure = {
  jobId: string;
  jobType: string;
  tenantId: string;
  attempt: number;
  maxAttempts: number;
  code: string;                  // stable, e.g. EXPORT_S3_UNAVAILABLE
  class: "transient" | "input" | "config" | "business" | "programming";
  retryable: boolean;
  terminalReason: "permanent" | "exhausted" | "cancelled" | null;
  message: string;               // safe for operators
  checkpoint?: Record<string, unknown>;
  occurredAt: string;            // ISO 8601 UTC
};
```

Contract rules:

1. **`code` is stable**; `message` may change. Consumers branch on `code`.
2. **`class` drives retry**, not the HTTP status of the underlying error.
3. **`retryable` and `terminalReason` are consistent** (`terminalReason` is set only when terminal).
4. **`checkpoint` is safe to persist** and sufficient to resume.
5. **No secrets, tokens, or PII** in `message` or `checkpoint`.
6. **Version the contract** if fields are added/removed (Chapter 49).

```json
{
  "jobId": "job_01HX...",
  "jobType": "ExportJob",
  "tenantId": "ten_42",
  "attempt": 5,
  "maxAttempts": 6,
  "code": "EXPORT_S3_UNAVAILABLE",
  "class": "transient",
  "retryable": true,
  "terminalReason": "exhausted",
  "message": "S3 returned 503 while appending batch",
  "checkpoint": { "lastRowId": "row_88213", "rowsWritten": 88213 },
  "occurredAt": "2026-10-21T09:22:10Z"
}
```

## Worked example — ExportJob resume and compensation

```ts
async function runExport(job: Job<ExportPayload>) {
  try {
    await exportWithResume(job);                 // checkpointed, idempotent
  } catch (err) {
    // If we published a partial object under a public key, remove it.
    await s3.delete(`public/${job.id}.csv`).catch((e) => log.error({ e }, "cleanup failed"));
    throw new JobError({
      jobId: job.id,
      jobType: "ExportJob",
      tenantId: job.data.tenantId,
      attempt: job.attempt,
      maxAttempts: job.maxAttempts,
      code: toCode(err),
      class: classifyJobError(err),
      retryable: classifyJobError(err) === "transient",
      terminalReason: terminalReason(err, job.attempt, job.maxAttempts),
      message: safeMessage(err),
      checkpoint: await checkpoints.get(job.id),
      occurredAt: new Date().toISOString(),
    }, { cause: err });
  }
}
```

The failure record now carries the checkpoint, so the replay resumes at `row_88213` rather than
starting over, and support can see exactly how far the job got.

## Key data / numbers

- Batch size for checkpointed work typically **500–5,000 rows** (balance durability vs overhead).
- Checkpoint write frequency should be proportional to reprocessing cost; a 1k-row batch bound.
- S3 multipart upload part size: **5 MiB minimum**, up to 10,000 parts (use part offsets as
  checkpoints).
- `checkpoint` and the side effect should share a transaction store where possible; if not, accept
  at-least-once resume.
- Standard failure-contract fields: 8–12; more becomes unmaintainable.

## Real-world use case — Acme SaaS

Acme's export restarted from row zero after any failure. A 4-hour export that hit a transient DB
blip at hour 3 would run again for another 4 hours, and it appended duplicate rows because the S3
object was opened in append mode without dedupe. After adding row-level checkpoints, per-part object
keys, and a `JobFailure.checkpoint`, the same failure resumed in seconds and produced exactly the
expected row count. A separate saga compensated an already-created "export complete" notification
when the final commit failed.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Restart from zero | Simple, no stale state | Expensive, duplicates | Short jobs |
| Checkpoint + resume | Cheap recovery | Idempotency required | Long/batch jobs |
| Compensate then retry | Clean slate | Complex, may be irreversible | Multi-step workflows |
| Continue past item failures | Maximizes progress | Partial contract needed | Bulk validation |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Checkpoint after each durable batch | Keep progress only in memory |
| Include `queryHash`/input hash | Resume a stale plan silently |
| Make resumed units idempotent | Append duplicates on retry |
| Compensate completed steps in reverse | Roll back in arbitrary order |
| Emit a standard `JobFailure` | Throw an ad-hoc string |
| Keep secrets out of failure context | Store raw provider payloads |

## Common mistakes

- **Checkpoint written before the effect commits** — resume skips lost work.
- **No input hash** — a changed query resumes with the old cursor.
- **Compensating before the state is terminal** — retry re-does the effect.
- **Ignoring a failed compensation** — silent inconsistent state.
- **Failure contract per job type** — operators cannot write one runbook.

## Checklist

- [ ] Does the job persist progress before acking each unit?
- [ ] Is resume at-least-once safe (idempotent units)?
- [ ] Is the checkpoint invalidated when the input changes?
- [ ] Are completed steps compensated in reverse on failure?
- [ ] Is compensation idempotent and alerting on failure?
- [ ] Does every job emit the same failure-contract shape?
- [ ] Is the failure context free of secrets/PII?
- [ ] Can support resume the job from the recorded checkpoint?

## Related

- [Checkpointing and Idempotent Resume — Mechanics](../02-deep-dive/03-checkpointing-and-idempotent-resume.md)
- [Poison Messages, DLQ, and Replay](./03-poison-messages-dlq-and-replay.md)
- [Checkpointing and Idempotent Resume](../02-deep-dive/03-checkpointing-and-idempotent-resume.md)
- [Chapter 32 Reference](../05-reference/README.md)
