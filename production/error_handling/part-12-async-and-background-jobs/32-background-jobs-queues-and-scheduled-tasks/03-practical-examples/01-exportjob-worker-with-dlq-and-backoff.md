# Practical — ExportJob Worker with DLQ and Backoff

> Part XII · Chapter 32 · Sections 32.4–32.8, 32.22 · _Estimated reading time: 20 min_
> **Prerequisite:** [Retries, Backoff, and Exhaustion](../01-concepts/02-retries-backoff-and-exhaustion.md)

## Scenario

`ExportJob` generates a CSV for a tenant and uploads it to S3. Exports take 30 s to 20 min, call
Postgres and S3, and must survive worker crashes and deploys. The job must:

- retry only transient failures with exponential backoff and jitter,
- stop after 6 attempts or 6 hours,
- send poison/permanent failures to a DLQ with context,
- be idempotent under at-least-once delivery,
- expose a clear failure contract to the API.

## Architecture

```text
producer ──▶ export-jobs (SQS, visibility 900s, maxReceiveCount 6)
                    │
                    ▼
             ExportWorker (this example)
                    │  success → delete message
                    │  transient → throw (redeliver via visibility)
                    │  permanent/exhausted → export-dlq + delete
                    ▼
             export-dlq (14d retention, alarm)
```

## Step 1 — Define the payload and failure contract

```ts
type ExportPayload = {
  jobId: string;
  tenantId: string;
  query: { from: string; to: string; format: "csv" | "json" };
  idempotencyKey: string;    // usually `${jobId}`
};

type JobFailure = {
  jobId: string;
  jobType: "ExportJob";
  tenantId: string;
  attempt: number;
  maxAttempts: number;
  code: string;
  class: "transient" | "input" | "config" | "business" | "programming";
  retryable: boolean;
  terminalReason: "permanent" | "exhausted" | "cancelled" | null;
  message: string;
  checkpoint?: Record<string, unknown>;
  occurredAt: string;
};
```

## Step 2 — Classify errors

```ts
function classify(err: unknown): JobFailure["class"] {
  if (isSqlState(err, "40001") || isSqlState(err, "40P01")) return "transient";
  if (isHttpStatus(err, [429, 500, 502, 503, 504])) return "transient";
  if (isTimeout(err) || isConnectionReset(err)) return "transient";
  if (isS3AccessDenied(err)) return "config";
  if (isSchemaError(err) || isInvalidQuery(err)) return "input";
  if (isQuotaExceeded(err) || isTenantSuspended(err)) return "business";
  return "programming";
}

const RETRYABLE: JobFailure["class"][] = ["transient"];
```

## Step 3 — Backoff policy

```ts
const POLICY = {
  baseMs: 500,
  capMs: 60_000,
  maxAttempts: 6,
  maxAgeMs: 6 * 60 * 60 * 1_000,
};

function backoffMs(attempt: number): number {
  const exp = Math.min(POLICY.capMs, POLICY.baseMs * 2 ** (attempt - 1));
  return Math.floor(Math.random() * exp); // full jitter
}
```

| Attempt | Max delay |
| ------- | --------- |
| 1 | 0.5 s |
| 2 | 1 s |
| 3 | 2 s |
| 4 | 4 s |
| 5 | 8 s |
| 6 | 16 s (cap allows 60 s; 6 attempts rarely reach it) |

## Step 4 — Idempotent export with a checkpoint

```ts
async function exportRows(payload: ExportPayload, signal: AbortSignal) {
  const cp = await checkpoints.getOrCreate(payload.jobId, {
    queryHash: sha256(JSON.stringify(payload.query)),
    lastRowId: null,
    rowsWritten: 0,
  });

  const tempKey = `tmp/${payload.tenantId}/${payload.jobId}.csv`;

  for await (const batch of batches(db.streamAfter(payload.query, cp.lastRowId, { signal }), 1_000)) {
    await s3.appendIdempotent(tempKey, toCsv(batch), { dedupeKey: `${payload.jobId}:${batch[0].id}` });
    cp.lastRowId = batch.at(-1)!.id;
    cp.rowsWritten += batch.length;
    await checkpoints.save(cp);        // after the write, never before
    signal.throwIfAborted();
  }

  await s3.commit(tempKey, `exports/${payload.tenantId}/${payload.jobId}.csv`);
  return { rows: cp.rowsWritten };
}
```

## Step 5 — The worker loop

```ts
import { SQSClient, ReceiveMessageCommand, DeleteMessageCommand } from "@aws-sdk/client-sqs";

const sqs = new SQSClient({});
const QUEUE_URL = process.env.EXPORT_QUEUE_URL!;
const DLQ_URL = process.env.EXPORT_DLQ_URL!;

async function handleMessage(msg: SQSMessage) {
  const attempt = Number(msg.Attributes?.ApproximateReceiveCount ?? "1");
  const payload = parse<ExportPayload>(msg.Body); // may throw -> input class

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(new DOMException("job deadline", "TimeoutError")), 12 * 60_000);

  try {
    const result = await exportRows(payload, controller.signal);

    await jobs.markSucceeded(payload.jobId, result);
    await sqs.send(new DeleteMessageCommand({ QueueUrl: QUEUE_URL, ReceiptHandle: msg.ReceiptHandle }));
  } catch (err) {
    const cls = classify(err);
    const retryable = RETRYABLE.includes(cls) && attempt < POLICY.maxAttempts;

    if (!retryable) {
      const terminalReason = RETRYABLE.includes(cls) ? "exhausted" : "permanent";
      const failure: JobFailure = {
        jobId: payload?.jobId ?? "unknown",
        jobType: "ExportJob",
        tenantId: payload?.tenantId ?? "unknown",
        attempt,
        maxAttempts: POLICY.maxAttempts,
        code: toCode(err),
        class: cls,
        retryable: RETRYABLE.includes(cls),
        terminalReason,
        message: safeMessage(err),
        checkpoint: await checkpoints.get(payload?.jobId),
        occurredAt: new Date().toISOString(),
      };

      await jobs.markFailed(failure);
      await sqs.send(new SendMessageCommand({
        QueueUrl: DLQ_URL,
        MessageBody: JSON.stringify({ failure, originalBody: msg.Body }),
      }));
      await sqs.send(new DeleteMessageCommand({ QueueUrl: QUEUE_URL, ReceiptHandle: msg.ReceiptHandle }));
      metrics.increment("export_job_dlq", { code: failure.code, class: cls });
    } else {
      // Do not delete: leave the message for redelivery.
      await jobs.markRetrying(payload.jobId, { attempt, delayMs: backoffMs(attempt), code: toCode(err) });
      metrics.increment("export_job_retry", { code: toCode(err) });
    }
  } finally {
    clearTimeout(timer);
  }
}
```

Two important details:

- **Transient errors are not deleted.** The queue's visibility timeout redelivers the message after
  the lease; the receive count increments. (If your queue supports per-message delay, send a copy
  with `DelaySeconds` and delete the original for exact backoff control.)
- **Permanent errors go straight to the DLQ**, even on attempt 1, so a schema bug does not burn six
  attempts.

## Step 6 — Visibility timeout and heartbeat

For exports longer than the 900 s visibility timeout, renew the lease:

```ts
const heartbeat = setInterval(() => {
  sqs.send(new ChangeMessageVisibilityCommand({
    QueueUrl: QUEUE_URL,
    ReceiptHandle: msg.ReceiptHandle,
    VisibilityTimeout: 900,
  })).catch((e) => log.warn({ e }, "heartbeat failed"));
}, 5 * 60_000);

try { await handleMessage(msg); } finally { clearInterval(heartbeat); }
```

Without the heartbeat, a 20-minute export is redelivered at minute 15 while still running.

## Step 7 — DLQ record and replay

The DLQ message contains `{ failure, originalBody }`. Replay:

```ts
async function replayOne(dlqMessage: SQSMessage, approve: boolean) {
  if (!approve) throw new Error("replay requires explicit approval");
  const { originalBody, failure } = JSON.parse(dlqMessage.Body);
  if (failure.class === "input" && !(await inputWasFixed(failure))) {
    return archive(dlqMessage, "cause not fixed");
  }
  await sqs.send(new SendMessageCommand({
    QueueUrl: QUEUE_URL,
    MessageBody: originalBody,
    MessageAttributes: { ReplayOf: { DataType: "String", StringValue: failure.jobId } },
  }));
  await sqs.send(new DeleteMessageCommand({ QueueUrl: DLQ_URL, ReceiptHandle: dlqMessage.ReceiptHandle }));
}
```

The original body still carries the same `jobId` and `idempotencyKey`, so the replay cannot create a
second export.

## Metrics and alarms

| Metric | Alarm |
| ------ | ----- |
| `export_job_success_total` | Drop below baseline for 15 min |
| `export_job_retry_total{code}` | Spike > 3× baseline |
| `export_job_dlq_total` | Any increase |
| `export_dlq_visible_messages` | > 0 for 5 min |
| `export_job_duration_seconds` p95 | > 10 min |

## Real-world use case — Acme SaaS

Acme's export worker previously caught every error, logged it, and deleted the message. Transient S3
`503`s lost exports silently. After implementing this worker, a 40-minute S3 incident produced 312
retries, all of which succeeded after the outage; 4 exports with an invalid date range went to the
DLQ with `EXPORT_INVALID_QUERY` and were replayed after the producer fix. No customer export was
lost, and on-call had one dashboard for retry and DLQ volume.

## Key data / numbers

- Visibility timeout **900 s**; job deadline **720 s**; heartbeat every **300 s**.
- `maxReceiveCount` **6**; `maxAttempts` **6**; max age **6 h**.
- Backoff base **500 ms**, cap **60 s**, full jitter.
- DLQ retention **14 days**; alarm at any message for 5 min.
- Batch size **1,000 rows**; checkpoint after every batch.
- DLQ replay rate: **5 msg/s** initially.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify before retrying | Delete the message on any error |
| Send permanent errors to the DLQ immediately | Burn all attempts on bad input |
| Renew visibility for long jobs | Let a long export be redelivered |
| Checkpoint after the write | Save the cursor before the effect |
| Reuse `jobId` on replay | Generate a new id |
| Alarm on DLQ depth | Wait for a customer report |

## Checklist

- [ ] Is every error classified before deciding retry vs DLQ?
- [ ] Is backoff exponential with full jitter?
- [ ] Are permanent errors routed to the DLQ on the first attempt?
- [ ] Is the job deadline below the visibility timeout?
- [ ] Is there a heartbeat for long-running exports?
- [ ] Is the export idempotent and checkpointed?
- [ ] Does the DLQ record include the full failure contract?
- [ ] Is replay rate-limited and approval-gated?

## Related

- [Poison Message Handling — Mechanics](../02-deep-dive/01-poison-message-handling.md)
- [Retries, Backoff, and Exhaustion](../01-concepts/02-retries-backoff-and-exhaustion.md)
- [Scheduled Tasks and Graceful Shutdown](./02-scheduled-tasks-and-graceful-shutdown.md)
- [Chapter 28 — Idempotency](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
