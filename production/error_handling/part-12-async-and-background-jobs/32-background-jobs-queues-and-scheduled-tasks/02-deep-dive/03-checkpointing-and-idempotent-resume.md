# Checkpointing and Idempotent Resume — Mechanics

> Part XII · Chapter 32 · Sections 32.14–32.15 (mechanics) · _Estimated reading time: 15 min_
> **Prerequisite:** [Partial Completion, Checkpointing, and Failure Contracts](../01-concepts/05-partial-completion-and-failure-contracts.md)

## In one sentence

A checkpoint is a **durable cursor plus the evidence that the work behind it is committed**, and a
resume is safe only when replaying from the checkpoint is **idempotent** — because the checkpoint and
the effect can never be updated atomically across systems.

## Why this matters in production

The naive checkpoint is "save `lastRowId` after each batch." If the batch write succeeds and the
checkpoint write fails, a resume redoes the batch — duplicates. If the checkpoint write succeeds and
the batch write fails, a resume skips the batch — data loss. This is the classic **dual-write
problem**, and it is the reason resumable jobs need idempotent units and an ordering that makes one
failure mode safe.

## The dual-write problem

```text
             ┌──────────────┐
  batch ────▶│ effect store │  (S3 object, DB rows, email)
             └──────────────┘
             ┌──────────────┐
  cursor ───▶│ checkpoint   │  (separate table/object)
             └──────────────┘
        two writes, no shared transaction → one can fail
```

Three resolutions:

| Strategy | How | Residual risk |
| -------- | --- | ------------- |
| **Idempotent replay** | Re-running a batch is harmless | Requires dedupe/keys |
| **Atomic commit** | Checkpoint in the same DB transaction as rows | Not possible for S3/email |
| **Effect-derived cursor** | Derive the cursor from the data itself | Requires a monotonic key |

The pragmatic default is **idempotent replay + checkpoint after commit**, accepting that the last
batch may run twice.

## Cursor design

A good cursor is:

- **Monotonic** (e.g., auto-increment id, `(created_at, id)` tuple, Kafka offset).
- **Stable** (not affected by concurrent inserts before it).
- **Indexed** so `WHERE id > $cursor ORDER BY id LIMIT n` is cheap.
- **Serializable** into the job record.

```sql
SELECT id, payload
FROM export_rows
WHERE tenant_id = $1 AND id > $2
ORDER BY id
LIMIT 1000;
```

Avoid offset/`LIMIT OFFSET` pagination for resumable work: concurrent inserts and deletes shift the
window, causing skipped or duplicated rows.

## Checkpoint ordering

```ts
for await (const batch of batches(stream, 1_000)) {
  await writeBatchIdempotent(batch);      // 1. effect first
  await checkpoints.save({                // 2. cursor second
    jobId,
    lastRowId: batch.at(-1)!.id,
    rowsWritten: (cp.rowsWritten += batch.length),
  });
}
```

If the process dies between (1) and (2): the batch is redone, and idempotency makes it a no-op.
If it dies during (2): the checkpoint is either fully written or not; a partial DB write is atomic
per row/transaction.

Never reverse the order: a cursor saved before the effect silently skips data.

## Atomic DB example

When the effect and checkpoint live in the same database, commit them together:

```sql
BEGIN;

INSERT INTO export_rows_exported (job_id, row_id, payload)
SELECT $1, id, payload
FROM export_rows
WHERE id > $2 AND tenant_id = $3
ORDER BY id
LIMIT 1000
ON CONFLICT (job_id, row_id) DO NOTHING;

UPDATE export_checkpoints
SET last_row_id = (
  SELECT max(row_id) FROM export_rows_exported WHERE job_id = $1
), updated_at = now()
WHERE job_id = $1;

COMMIT;
```

One transaction makes the cursor and the rows consistent. Re-running the same batch is a no-op
thanks to `ON CONFLICT`.

## Idempotent batch writes

| Sink | Idempotent technique |
| ---- | -------------------- |
| Postgres rows | `INSERT … ON CONFLICT (job_id, row_id) DO NOTHING` |
| S3 object | Write part file named by offset; overwrite same key on retry |
| S3 append (not atomic) | Multipart upload with deterministic part numbers |
| Kafka | Key by `(jobId, rowId)` + consumer dedupe, or transactional producer |
| Email | `dedupe.claim(jobId:recipient)` before send |
| Search index | `_id = jobId:rowId` upsert |

Multipart upload is a common checkpoint: use a deterministic part number per batch, so re-uploading
a part replaces it instead of appending a duplicate.

```ts
await s3.uploadPart({
  Bucket, Key: tempKey, UploadId,
  PartNumber: batchIndex + 1,
  Body: csv,
});
await checkpoints.save({ lastRowId, partNumber: batchIndex + 1 });
```

## Resume with changed input

A checkpoint is only valid for the input that produced it. Store a hash:

```ts
if (cp.queryHash !== sha256(job.data.query)) {
  throw new NonRetryableJobError("EXPORT_INPUT_CHANGED");
}
```

If the input changed, do not resume the old cursor; start a new job (or a new checkpoint namespace).
Resuming a stale cursor against a new query is how exports silently miss or duplicate rows.

## Crash-consistency matrix

| Crash point | Effect committed? | Cursor committed? | Resume behavior | Safe? |
| ----------- | ----------------- | ----------------- | --------------- | ----- |
| Before effect | No | No | Redo batch | ✅ |
| After effect, before cursor | Yes | No | Redo batch (idempotent) | ✅ if idempotent |
| During cursor write | Yes | Partial/atomic | Redo or skip last batch | ✅ if idempotent |
| After cursor | Yes | Yes | Next batch | ✅ |
| After final publish, before complete | Yes | Yes | Job re-runs from cursor | ✅ if final publish idempotent |

The only unsafe row is "effect committed, cursor committed, final publish not idempotent." Make the
publish a deterministic key that can be overwritten.

## Worked example — ExportJob to S3

```ts
async function exportWithResume(job: Job<ExportPayload>) {
  const cp = await checkpoints.getOrCreate(job.id, {
    queryHash: sha256(job.data.query),
    lastRowId: null,
    partNumber: 0,
  });

  if (cp.queryHash !== sha256(job.data.query)) {
    throw new NonRetryableJobError("EXPORT_INPUT_CHANGED");
  }

  const uploadId = await s3.startMultipart(finalKey(job));

  for await (const batch of batches(db.streamAfter(job.data.query, cp.lastRowId), 1_000)) {
    const partNumber = cp.partNumber + 1;
    await s3.uploadPart({ uploadId, partNumber, body: toCsv(batch) });
    cp.lastRowId = batch.at(-1)!.id;
    cp.partNumber = partNumber;
    await checkpoints.save(cp);              // after the part is durable
  }

  await s3.completeMultipart(uploadId);      // deterministic key, overwrite-safe
  await jobs.markSucceeded(job.id);
}
```

Resuming re-uploads the last part number (replacing it) and continues from the cursor. The final key
is deterministic, so a retry after completion overwrites rather than creating a second object.

## Key data / numbers

- Batch size: **500–5,000** rows; smaller = more durable, more overhead.
- S3 multipart: minimum part **5 MiB** (except the last), max **10,000** parts.
- Postgres `ON CONFLICT` requires a unique index on the dedupe key.
- Checkpoint write cost should be <1% of batch processing cost; measure before shrinking batches.
- Resume rework is bounded by one batch when checkpointing after each commit.

## Real-world use case — Acme SaaS

Acme used `LIMIT/OFFSET` pagination with a checkpoint on the offset. During a large export, new rows
were inserted by the application, shifting the window; the export skipped ~2,000 rows and duplicated
others. Switching to a keyset cursor (`id > lastRowId`), writing each 1,000-row batch with
`ON CONFLICT DO NOTHING`, and storing the cursor after the commit eliminated both. A resume after a
mid-export deploy re-uploaded only the last multipart part.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| No checkpoint | Simple | Full restart, duplicates | Jobs < 1 min |
| Cursor after effect | Safe, simple | Last batch redone | Default |
| Same-transaction cursor | Exactly consistent | DB-only | DB-to-DB jobs |
| Effect-derived cursor | No separate checkpoint | Requires monotonic data | Append-only tables |
| Checkpoint every N batches | Less overhead | Larger replay window | Very high throughput |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Commit the effect, then the cursor | Save the cursor before writing |
| Use keyset pagination | Use `OFFSET` for resumable work |
| Make each batch idempotent | Append blindly on resume |
| Store the input hash | Resume a stale plan silently |
| Use deterministic keys/part numbers | Random object names per attempt |
| Bound rework to one batch | Checkpoint only at the end |

## Common mistakes

- **Cursor-before-effect** — silent data loss on crash.
- **Offset pagination** — shifted windows with concurrent writes.
- **Non-idempotent append** — duplicate rows on resume.
- **Checkpoint without input hash** — stale resume after a config change.
- **Random output keys** — orphaned partial objects on retry.

## Checklist

- [ ] Is the cursor monotonic and indexed?
- [ ] Is the effect committed before the cursor?
- [ ] Is re-running a batch idempotent?
- [ ] Does the checkpoint include an input hash?
- [ ] Are output keys/part numbers deterministic?
- [ ] Is the replay window bounded to one batch?
- [ ] Is the final publish overwrite-safe?

## Related

- [Partial Completion, Checkpointing, and Failure Contracts](../01-concepts/05-partial-completion-and-failure-contracts.md)
- [At-least-once vs Exactly-once](./02-at-least-once-vs-exactly-once.md)
- [ExportJob Worker with DLQ and Backoff](../03-practical-examples/01-exportjob-worker-with-dlq-and-backoff.md)
- [Chapter 23 — Transaction and Rollback Error Handling](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
