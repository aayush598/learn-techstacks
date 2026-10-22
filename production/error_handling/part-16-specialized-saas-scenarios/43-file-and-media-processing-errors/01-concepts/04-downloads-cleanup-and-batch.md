# Downloads, Cleanup, Duplicate Processing, and Batch

> Part XVI · Chapter 43 · Sections 43.10–43.14 · _Estimated reading time: 22 min_
> **Prerequisite:** [Processing, Malformed Files, Malware Scanning, and Temp URLs](./03-processing-scanning-and-temp-urls.md)

## In one sentence

The back half of the file lifecycle is about **repeatability**: downloads must survive aborted
clients, cleanup must be owned by something, reprocessing must be a no-op, and long batches
must report **per-item** outcomes instead of all-or-nothing.

## Why this matters in production

Downloads look trivial until a mobile client reconnects mid-video and your handler buffers the
whole object in memory. Cleanup looks like housekeeping until the storage bill arrives.
Reprocessing looks safe until a webhook replay creates two renditions of the same video and a
customer sees the wrong one. Batch jobs look fine until one corrupt file fails the entire
10,000-item export and no one can tell which item was bad. Each subsection names the failure
and the safe default.

## 43.10 — Download and streaming

The failure surface is on both ends of the socket:

| Failure | Cause | Correct outcome |
| ------- | ----- | --------------- |
| Client disconnects mid-stream | Navigation, flaky network | Stop reading upstream; release the file handle; **no error alert** |
| Range request unsatisfiable | `Range: bytes=...` beyond EOF | `416` with `Content-Range: bytes */<size>` |
| Range partially served | Client resumes | `206 Partial Content` with correct `Content-Range` |
| Upstream storage throttles | `503 SlowDown` on read | Backoff; propagate `503` if the stream has not started |
| Error mid-stream | Storage reset after headers sent | Terminate the connection; cannot change the status code |
| Slow client | Backpressure | Honor flow control; bound the buffer; never buffer the whole object |

The rule that prevents the worst bugs: **stream, never buffer.** Pipe the storage body to the
response with backpressure, and abort the upstream read when the client goes away.

```ts
app.get("/files/:id", async (req, res) => {
  const range = parseRange(req.headers.range);          // undefined ⇒ full object
  const file = await authorizeAndStat(req.params.id, req.user);  // 404/403 before streaming

  if (range && range.start >= file.size) {
    res.status(416).set("Content-Range", `bytes */${file.size}`).end();
    return;
  }

  const upstream = await s3.getObject({
    Bucket: MEDIA_BUCKET, Key: file.key,
    Range: range ? `bytes=${range.start}-${range.end}` : undefined,
  });

  res.status(range ? 206 : 200);
  res.set("Content-Length", String(range ? range.length : file.size));
  res.set("Accept-Ranges", "bytes");
  if (range) res.set("Content-Range", `bytes ${range.start}-${range.end}/${file.size}`);
  res.set("Content-Type", "application/octet-stream");
  res.set("Content-Disposition", `attachment; filename="${file.safeName}"`);

  const body = upstream.Body as NodeJS.ReadableStream;
  body.pipe(res);
  res.on("close", () => body.destroy());                // client gone ⇒ stop reading
});
```

> ⚠️ **Hazard.** After the first byte of the body is sent, you can no longer change the status
> code. Any upstream failure at that point is a **truncated response** — the only honest signal
> is closing the connection. Clients must verify `Content-Length`/checksums for critical
> downloads.

**Key data:** `Accept-Ranges: bytes`, `206` with `Content-Range`, `416` for invalid ranges,
`Content-Length` for both full and partial responses. Range requests are what make resumable
downloads and video seeking work.

## 43.11 — Temporary cleanup

Everything created on the failure path needs an owner and a TTL:

| Artifact | Created by | Cleanup |
| -------- | ---------- | ------- |
| Incomplete multipart parts | Interrupted upload | `AbortMultipartUpload` + lifecycle backstop |
| Quarantine objects | Scan gate | Delete after terminal rejection (retain metadata) |
| Temp files on workers | Processing | `finally`-style cleanup; per-job temp dirs |
| Partial derivatives | Failed transforms | Deterministic keys ⇒ overwrite on retry; sweep orphans |
| Upload sessions | Never completed | TTL on the session row; abort storage |
| Signed URLs | Issued | Expire by TTL; never persist them |

```ts
async function withTempDir<T>(jobId: string, fn: (dir: string) => Promise<T>): Promise<T> {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), `job-${jobId}-`));
  try {
    return await fn(dir);
  } finally {
    await fs.rm(dir, { recursive: true, force: true }).catch((err) => {
      // Cleanup failure must be loud but must not mask the primary error.
      log.error({ err, jobId, dir }, "temp cleanup failed");
    });
  }
}
```

**Key data:** set the S3 lifecycle rule `AbortIncompleteMultipartUpload` with
`DaysAfterInitiation` (commonly **7 days**; shorter if uploads are short-lived). Cleanup code
must be **idempotent** (deleting a missing object is success) and must never throw over the
primary failure.

## 43.12 — Duplicate processing

Duplicates arise from retries, webhook replays, and double-submits. The defense is a
**content-derived identity**:

```text
derivative key = sha256( sourceBytesHash + transformName + transformVersion + params )
```

| Duplicate source | Defense |
| ---------------- | ------- |
| Job retried after timeout | Same derivative key ⇒ deterministic write, overwrite |
| Webhook `object.created` delivered twice | Dedupe on event id, plus deterministic key |
| User clicks "regenerate" twice | Idempotency key per request; or accept and overwrite |
| Two workers pick up the same job | Lease/visibility timeout + conditional write |

```ts
function derivativeKey(src: SourceRef, t: Transform): string {
  return `derived/${t.name}/v${t.version}/${src.sha256}-${hashParams(t.params)}`;
}

// Conditional write makes the race explicit instead of last-write-wins.
await s3.putObject({ Bucket: MEDIA_BUCKET, Key: derivativeKey(src, t), Body: out,
  IfNoneMatch: "*" }).catch((err) => {
    if (err.name === "PreconditionFailed") return;   // someone else produced it identically
    throw err;
  });
```

**Key data:** include the **transform version** in the key — when you fix a rendering bug you
want new outputs, not to silently reuse the old derivative. Include all parameters that affect
bytes (dimensions, quality, crop) or two different transforms will collide.

## 43.13 — Partial processing and resume

Long media jobs (transcode, OCR, thumbnail sprites) should be **checkpointed** per unit of
work, exactly like `ExportJob`:

```ts
type MediaCheckpoint = { step: "probe" | "transcode" | "thumbnails" | "scan";
                         completed: string[]; cursor?: string };

async function processMedia(job: MediaJob, cp: MediaCheckpoint) {
  if (!cp.completed.includes("probe")) {
    const meta = await probe(job.source);
    await saveCheckpoint(job.id, { ...cp, step: "transcode", probe: meta });
  }
  // Transcode is itself resumable only if the encoder supports segments; otherwise
  // checkpoint completed segment ranges and concatenate deterministically.
  for (const segment of segments(job, cp.cursor)) {
    if (cp.completed.includes(segment.id)) continue;
    await transcodeSegment(job, segment);
    await saveCheckpoint(job.id, { ...cp, completed: [...cp.completed, segment.id],
                                   cursor: segment.next });
  }
}
```

**Key data:** checkpoint after each durable unit, not at the end; on restart, re-verify the
checkpoint's outputs exist (a checkpoint can outlive a deleted derivative). Partial output must
be marked `partial` in the API — never served as the final rendition.

## 43.14 — Large-scale batch

Batch processing fails in the aggregate: one bad item must not fail the batch, and the caller
must learn **which** items failed and why. Adopt per-item results:

```ts
type BatchResult = {
  total: number;
  succeeded: string[];
  failed: { id: string; code: string; retryable: boolean; detail: string }[];
};

async function processBatch(ids: string[]): Promise<BatchResult> {
  const out: BatchResult = { total: ids.length, succeeded: [], failed: [] };
  for (const id of ids) {
    try {
      await processOne(id);                      // idempotent per item
      out.succeeded.push(id);
    } catch (err) {
      out.failed.push(toItemFailure(id, err));   // classify, don't stringify
    }
  }
  return out;                                    // partial success is a valid outcome
}
```

Rules for large batches:

1. **Per-item idempotency** so a retried batch does not double-process the successes.
2. **Checkpoint the batch cursor** so a crash resumes mid-batch.
3. **Bound concurrency** per tenant and globally (bulkhead), and respect provider rate limits.
4. **Return partial success** with itemized errors; HTTP `207 Multi-Status` or a job resource
   with per-item states — never a single `500` for 3 bad items out of 10,000.
5. **Dead-letter only exhausted items**, with enough context to replay just those.

## Worked example — Acme's 10,000-image import

Acme's importer accepted a ZIP of product images and processed it as one job with a single
`try/catch`. One corrupt JPEG aborted the job at item 412; the user retried, and the first 411
were processed **again**, producing duplicate renditions (different keys because the old code
included a timestamp). The rebuild: unzip with per-entry results, hash each image, derive
rendition keys from `sha256 + transformVersion`, checkpoint the entry index, and return
`{ succeeded: 9_987, failed: 13 }` with per-file codes. Re-running the import became a no-op
for the 9,987 good images — which is exactly what let support tell the customer "just retry,
we will only touch the 13."

## Real-world use case — the $4,200 month of orphan media

Acme generated temp objects — thumbnails, previews, converted PDF pages — and never
deleted them. The objects had no owner and no expiry, and the presigned URLs handed to
clients were valid for **7 days**, so a URL that leaked in a shared doc still served
customer data a week later.

The fix made ownership mandatory. Every temp object is written with an `expires_at` and
an `owner_kind`/`owner_id`; the sweeper deletes anything past `expires_at` and reports an
`orphaned_temp_objects` gauge that must be zero; presigned URLs are issued for **15
minutes** instead of 7 days; and downloads of temp objects go through an app endpoint
that re-checks the expiry on every request rather than trusting the URL.

Temp storage fell 71%, the storage bill fell by about $2,900 a month, and the leaked-URL
exposure window shrank from 7 days to 15 minutes. The lesson: **an object with no owner
and no expiry is a liability with a storage bill attached.**

## Trade-offs

| Choice | Pros | Cons | When to use |
| ------ | ---- | ---- | ----------- |
| Buffer then send | Simple | Memory blowup, no seek | Tiny files |
| Stream + range | Constant memory, resumable | More code | ✅ Default |
| TTL-only cleanup | Simple | Orphans until TTL | Acceptable with lifecycle |
| Active abort + TTL | Fast, cheap | More moving parts | ✅ Large uploads |
| Atomic batch | Simple status | One fault kills all | Small, homogeneous batches |
| Per-item results | Accurate, replayable | More payload/state | ✅ Default at scale |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Stream downloads with backpressure | `readFile` before responding |
| Support `Range`/`206`/`416` | Ignore `Range` and send the whole file |
| Abort upstream reads on client disconnect | Keep reading after the socket closes |
| Derive derivative keys from content + version | Key derivatives by timestamp |
| Checkpoint long jobs per unit | Restart from zero after a crash |
| Return per-item batch results | Fail the whole batch for one item |

## Common mistakes

- **Cleanup that throws over the primary error** — the job is marked failed for the wrong
  reason.
- **Orphan sweeps without metrics** — nobody notices a leak until finance does.
- **Timestamp-based derivative keys** — every retry creates a new object.
- **Checkpoints without output verification** — resume points at a missing file.
- **Batch retries without item idempotency** — successes are processed twice.

## Checklist

- [ ] Downloads stream with backpressure and abort on client disconnect.
- [ ] Range requests return `206`/`416` correctly.
- [ ] Every temp artifact (parts, quarantine, temp dirs, sessions) has a TTL and an owner.
- [ ] Derivative keys include source hash, transform name, version, and params.
- [ ] Long jobs checkpoint per unit and verify outputs on resume.
- [ ] Batch endpoints return per-item success/failure and are safe to re-run.

## Related

- [Multipart Resume and Cleanup — Mechanics](../02-deep-dive/01-multipart-resume-and-cleanup-mechanics.md)
- [Processing Pipeline with Checkpoints](../03-practical-examples/02-processing-pipeline-with-checkpoints.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- [Chapter 43 Reference](../05-reference/README.md)
