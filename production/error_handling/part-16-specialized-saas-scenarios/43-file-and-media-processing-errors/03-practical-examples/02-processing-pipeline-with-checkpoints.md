# Processing Pipeline with Checkpoints

> Part XVI · Chapter 43 · Sections 43.6, 43.13, 43.14 · _Estimated reading time: 24 min_
> **Prerequisite:** [Downloads, Cleanup, Duplicate Processing, and Batch](../01-concepts/04-downloads-cleanup-and-batch.md)

## In one sentence

A media pipeline is a **sequence of bounded steps with a durable checkpoint after each one**,
so a failure costs one step instead of the whole file, and a batch reports **per-item
outcomes** instead of a single verdict.

## Why this matters in production

Processing is where the cost is: a 2 GB video can take twenty minutes of CPU and forty cents
of storage to transcode. Restarting it from zero after a transient worker restart is expensive
and user-visible. But restarting *carelessly* is worse: a second pass writing to a timestamped
key produces two renditions, the CDN serves the older one, and the customer complains their
"new" edit shows the old video. The design must make the retry **free** and the resume
**exact**.

## The pipeline

```text
  probe ──▶ scan ──▶ transcode ──▶ thumbnails ──▶ publish
     │         │          │             │             │
     └─────────┴──────────┴─────────────┴─────────────┘
                    checkpoint after every step
```

Each step has three properties you must decide up front:

| Property | Rule | Why |
| -------- | ---- | --- |
| **Bounded** | Time, bytes, pixels, and memory are capped | An attacker-chosen file must not be able to stall a worker |
| **Deterministic** | Same input + same version ⇒ same output bytes | Makes a retry a no-op instead of a duplicate |
| **Isolated** | Runs in a sandboxed worker, not the API process | A malformed file must not take down the service |

"Deterministic" is the one people skip. It is also the one that makes checkpointing work:
if step 3's output depends on a timestamp, a resumed run produces a *different* file, and
the publish step now has two candidates.

## Checkpoint schema

```sql
CREATE TABLE media_job (
  job_id        TEXT PRIMARY KEY,
  tenant_id     TEXT NOT NULL,
  source_key    TEXT NOT NULL,
  source_sha256 TEXT NOT NULL,        -- the content identity of the input
  status        TEXT NOT NULL,        -- pending|running|done|failed
  current_step  TEXT NOT NULL,        -- probe|scan|transcode|thumbnails|publish
  completed     TEXT[] NOT NULL DEFAULT '{}',   -- steps whose output is durable
  cursor        TEXT,                 -- resume point INSIDE the current step
  attempt       INTEGER NOT NULL DEFAULT 0,
  error_code    TEXT,
  error_detail  TEXT,
  created_at    TIMESTAMPTZ NOT NULL,
  updated_at    TIMESTAMPTZ NOT NULL
);
```

Two details make this table work:

1. **`completed` lists steps whose *output exists*, not steps that were attempted.** The
   distinction matters: a step that ran and crashed halfway has produced a partial file.
2. **`source_sha256` is part of the job identity.** The same bytes processed twice produce
   the same job; different bytes produce a different one. Without it, a re-upload of a
   changed file reuses stale derivatives.

## Derivative keys: the identity that makes retries free

```ts
/**
 * The derivative key is a pure function of (content, transform, version, params).
 * Nothing time-based, nothing random. A retry writes the SAME key.
 */
function derivativeKey(src: SourceRef, t: Transform): string {
  const paramHash = hashParamsCanonical(t.params);      // stable key ordering
  return `derived/${t.name}/v${t.version}/${src.sha256}-${paramHash}`;
}
```

```text
derived/transcode/v3/9f2c…-a71b        # 1080p, CRF 23
derived/thumbnails/v1/9f2c…-e04c       # sprite sheet, 512 px wide
derived/thumbnails/v1/9f2c…-e04c       # identical request → identical key
```

Because the key is identical, the write is **idempotent by construction** — a retry
overwrites the same object with the same bytes. Add a conditional write to make the race
explicit rather than last-write-wins:

```ts
await s3.putObject({
  Bucket: MEDIA_BUCKET,
  Key: derivativeKey(src, transform),
  Body: output,
  IfNoneMatch: "*",                    // someone else already produced it
}).catch((err) => {
  if (err.name === "PreconditionFailed") return;   // identical output — success
  throw err;
});
```

> ⚠️ **Hazard.** Include the **transform version** in the key. When you fix a rendering bug
> you want *new* outputs, not silent reuse of the broken derivative. But also include every
> parameter that affects bytes (dimensions, quality, crop, codec) — otherwise two different
> renders collide on one key and users see the wrong one.

**Key data:** transform version in the key (`v3`), parameter hash over a **canonicalised**
JSON object (sorted keys, stable number formatting), content hash from `sha256` of the
source bytes. Never a timestamp, never a UUID.

## Resume, verified

A checkpoint can outlive the file it points at. Someone can delete a derivative, or a
lifecycle rule can expire it, and a naive resume will happily skip a missing step. So
resume **verifies** before it trusts:

```ts
async function resume(job: MediaJob): Promise<void> {
  for (const step of PIPELINE) {
    if (!job.completed.includes(step.name)) {
      await runStep(job, step);                       // may itself checkpoint internally
      await checkpoint(job, { completed: [...job.completed, step.name] });
      continue;
    }
    // Already marked complete — verify the artifact still exists before skipping.
    const key = derivativeKey(job.source, step);
    const exists = await s3.headObject({ Bucket: MEDIA_BUCKET, Key: key })
      .then(() => true).catch(() => false);
    if (!exists) {
      // The checkpoint lied (or the artifact expired). Re-run this step only.
      await checkpoint(job, { completed: job.completed.filter((s) => s !== step.name) });
      await runStep(job, step);
      await checkpoint(job, { completed: [...job.completed, step.name] });
    }
  }
}
```

That "the checkpoint lied" branch is the difference between a cheap resume and a customer
who downloads a 404.

## Per-step failure classification

Every step's error must land in one of three buckets, and the bucket determines what the
job does next:

| Bucket | Examples | Job action |
| ------ | -------- | ---------- |
| **Retryable** | Storage `SlowDown`, worker crash, dependency `503`, timeout | Retry the step with backoff; job stays `running` |
| **Permanent (this file)** | `MALFORMED_MEDIA`, `UNSUPPORTED_FORMAT`, `INFECTED`, `UNSCANNABLE` | Mark the **item** failed, do not retry, move on to the next item |
| **Fatal (this job)** | Quota exhausted, plan limit reached, source missing | Mark the **job** failed, do not retry, surface the reason |

The mistake that costs the most is treating permanent failures as retryable. A corrupt
file retried ten times burns ten times the CPU, delays every other file behind it in the
batch, and ends in the same place.

```ts
type StepOutcome =
  | { ok: true; output: { key: string; sha256: string } }
  | { ok: false; class: "retryable"; code: string; detail: string }
  | { ok: false; class: "permanent"; code: string; detail: string }
  | { ok: false; class: "fatal"; code: string; detail: string };

async function runStep(job: MediaJob, step: Step): Promise<StepOutcome> {
  try {
    const out = await step.execute(job.source, { timeoutMs: step.timeoutMs });
    return { ok: true, output: out };
  } catch (err) {
    if (err instanceof MalformedMedia) return { ok: false, class: "permanent", code: "MALFORMED_MEDIA", detail: err.safeMessage };
    if (err instanceof UnsupportedFormat) return { ok: false, class: "permanent", code: "UNSUPPORTED_FORMAT", detail: err.format };
    if (err instanceof ScanVerdict) return { ok: false, class: "permanent", code: "INFECTED", detail: err.ruleName };
    if (err instanceof StorageError && err.retryable) return { ok: false, class: "retryable", code: err.code, detail: err.safeMessage };
    return { ok: false, class: "fatal", code: "INTERNAL", detail: "unexpected failure" };
  }
}
```

**Key data:** a scan verdict of `INFECTED` is a **permanent, per-item** failure — never a
job-level retry. A scan `error` (scanner down) is **retryable** and keeps the file
quarantined, never served (see the malware deep dive).

## Batches: per-item results, always

`ExportJob` runs a media batch over hundreds of items. The contract with the caller is
per-item:

```ts
type BatchItemResult = {
  id: string;
  status: "succeeded" | "failed" | "skipped";
  code?: string;          // stable error code, never a raw message
  detail?: string;        // safe, user-presentable
  retryable?: boolean;
};

type BatchResult = {
  total: number;
  succeeded: number;
  failed: number;
  items: BatchItemResult[];
  artifactKey?: string;   // the assembled manifest / zip
};
```

The rules that make a batch safe to re-run:

1. **Per-item idempotency.** Every item's work is keyed by `(sourceSha256, transform)`, so
   re-running the batch re-does nothing.
2. **Cursor checkpoint.** The batch records its position; a crash resumes near the crash.
3. **Bounded concurrency.** A per-tenant and global cap (bulkhead): one tenant with 10,000
   videos must not starve everyone else, and the provider's rate limits are shared.
4. **Partial success is a success.** The job completes with `succeeded: 9_987, failed: 13`,
   not failed, because three items were corrupt.
5. **Dead-letter only the exhausted items**, with enough context to replay *just those*.

```ts
async function runBatch(job: ExportJob): Promise<BatchResult> {
  const items = await db.items(job.id);
  const out: BatchItemResult[] = [];
  for (const item of items) {
    if (item.status === "done") { out.push(item.result); continue; }   // resume: skip done
    const res = await processOne(item);                              // idempotent per item
    out.push(res);
    await checkpoint(job, { cursor: item.id });                      // cursor after each item
  }
  return { total: items.length,
           succeeded: out.filter((r) => r.status === "succeeded").length,
           failed: out.filter((r) => r.status === "failed").length,
           items: out };
}
```

**Key data:** for a 10,000-item batch, report `{ total: 10000, succeeded: 9987, failed: 13 }`
with per-item codes. Concurrency caps are commonly **4–8 per tenant** and **32–64 global**
for CPU-bound transcodes; the storage provider's request rate is the other limit.

## Worked example — the 10,000-image import

Acme's importer accepted a ZIP of product images and processed it as one job with a single
`try/catch`. One corrupt JPEG aborted the job at item 412; the user retried, and the first
411 were processed **again**, producing duplicate renditions because the old code appended
a timestamp to the key. The rebuild: unzip with per-entry results; hash each image; derive
rendition keys from `sha256 + transformVersion + paramHash`; checkpoint the entry index
after every item; and return `{ succeeded: 9_987, failed: 13 }` with per-file codes.
Re-running the import became a no-op for the 9,987 good images — which is what let
support tell the customer "just retry, we will only touch the 13". The next corrupt-file
incident was handled in four minutes instead of a migration.

## Real-world use case — the customer who downloaded a half-built archive

Acme's `ExportJob` produces a customer's media archive as a ZIP. One export of 40,000
images failed at 61% — a worker was OOM-killed while transcoding — and the customer still
received a download link, because the job's status was written to `ready` before the
archive was finalized. The link served a **partial ZIP** with a valid manifest and a
plausible file count, and support could not prove what should have been inside it.

Three changes fixed the class of bug: **finalize, then publish** (the status becomes
`ready` only after the manifest and its checksum are written, so a partial archive is
`failed`, never `ready`); **deterministic derivative keys** derived from the source ETag
and the derivative spec, so a resumed job overwrites nothing and skips nothing; and
**checkpointed resume** from the last completed step per item, with the per-item outcome
table making completeness provable.

Since the change, no partial archive has been served, and a failed export resumes in ~22
minutes instead of restarting from zero. The lesson: **a job's status is a promise — never
make it before the work is done.**

## Trade-offs

| Choice | Pros | Cons | When to use |
| ------ | ---- | ---- | ----------- |
| Checkpoint per step | Cheap resume | More writes | Multi-minute jobs |
| Checkpoint per item | Fine-grained resume | Many writes | Batches |
| Timestamp-free keys | Retry is a no-op | Cache invalidation needs versioning | ✅ Always |
| Resume without verifying outputs | Cheap | Serves missing artifacts | Never |
| All-or-nothing batch | Simple status | One fault kills everything | Small, homogeneous batches |
| Per-item batch results | Accurate, replayable | More payload/state | ✅ Default at scale |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Derive derivative keys from content + version + params | Put a timestamp or UUID in the key |
| Checkpoint after each durable unit | Checkpoint only at the end |
| Verify checkpointed outputs exist on resume | Trust the checkpoint blindly |
| Classify malformed as permanent, dependency errors as retryable | Retry a corrupt file ten times |
| Report per-item batch outcomes | Fail a 10,000-item batch for one item |
| Bound concurrency per tenant and globally | Let one tenant monopolise the workers |
| Keep a dead-letter queue for exhausted items only | Dead-letter the whole batch |

## Common mistakes

- **Timestamp-based derivative keys** — every retry creates a new object, forever.
- **Checkpoint without output verification** — resume points at a deleted file.
- **Retrying permanent failures** — corrupt files burn the queue and delay good work.
- **All-or-nothing batches** — one bad file kills 9,999 good ones and the user starts over.
- **Unbounded concurrency** — one tenant's import saturates the transcoder pool.
- **Sharing a job row across two sources** — the `sourceSha256` must be part of the identity.
- **Treating a timeout as success** — a partial derivative must never be published.
- **Publishing before finalizing** — a half-built archive is served as complete.

## Checklist

- [ ] Every step is bounded (time, bytes, memory) and runs in an isolated worker.
- [ ] Derivative keys are a pure function of content, transform, version, and params.
- [ ] Checkpoints are written after each durable unit, not at the end.
- [ ] Resume verifies that checkpointed outputs still exist.
- [ ] Failures are classified retryable / permanent-per-item / fatal-per-job.
- [ ] Batches return per-item results and checkpoint their cursor.
- [ ] Concurrency is bounded per tenant and globally.
- [ ] Exhausted items land in a dead-letter queue with replay context.

## Related

- [Malware Scanning and Quarantine Flow — Mechanics](../02-deep-dive/02-malware-scanning-and-quarantine-flow.md)
- [Processing, Malformed Files, Malware Scanning, and Temp URLs](../01-concepts/03-processing-scanning-and-temp-urls.md)
- [S3 Multipart Upload with Cleanup](./01-s3-multipart-upload-with-cleanup.ts)
