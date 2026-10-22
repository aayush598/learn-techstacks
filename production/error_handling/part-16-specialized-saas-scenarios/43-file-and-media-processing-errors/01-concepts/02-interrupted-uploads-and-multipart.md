# Interrupted Uploads and Multipart Semantics

> Part XVI · Chapter 43 · Sections 43.4–43.5 · _Estimated reading time: 18 min_
> **Prerequisite:** [Upload Validation and Storage Failures](./01-upload-validation-and-storage-failures.md)

## In one sentence

Large uploads **will** be interrupted, so the only question is whether resuming costs one part
or the whole file — which means multipart upload is a **resumable protocol with a cleanup
obligation**, not a performance tweak.

## Why this matters in production

A 1 GB upload on a mobile network drops often. Without multipart, every drop restarts at byte
zero: wasted bandwidth, angry users, and retry storms against your own API. With multipart but
without cleanup, every abandoned upload leaves parts in the bucket — and S3 bills for them
even though they are invisible in the console and unreachable by any object key. With
multipart but without resume state, the browser still restarts from part 1. The failure you
are designing for is **partial progress**, and it has two halves: resume what succeeded, and
delete what will never finish.

## 43.4 — Interrupted uploads

Interruptions come in four shapes, and they are not equivalent:

| Interruption | What happened | Safe response |
| ------------ | ------------- | ------------- |
| Network drop mid-part | Part not acknowledged | Re-upload **that part** (part upload is idempotent) |
| Client crash / tab closed | Upload session abandoned | Resume from `ListParts` state, or expire |
| Server crash after part stored | Client did not get the ETag | `ListParts` to reconcile, then continue |
| Timeout on `CompleteMultipartUpload` | **Ambiguous** — completion may have succeeded | Check `HeadObject` / `ListParts` before retrying |

The ambiguous completion case is the one teams miss. `CompleteMultipartUpload` is not
idempotent in the "retry freely" sense: a retry after a timeout can return `NoSuchUpload`
because the first call already succeeded. The safe procedure is **check, then decide**:

```ts
async function completeSafely(uploadId: string, key: string, parts: CompletedPart[]) {
  try {
    return await s3.completeMultipartUpload({ Bucket: BUCKET, Key: key, UploadId: uploadId,
      MultipartUpload: { Parts: parts } });
  } catch (err) {
    if (err.name === "NoSuchUpload") {
      // Either already completed by a prior attempt, or aborted/expired.
      const head = await s3.headObject({ Bucket: BUCKET, Key: key }).catch(() => null);
      if (head) return { alreadyCompleted: true, etag: head.ETag };  // success-shaped
      throw new UploadSessionExpired({ uploadId });                   // terminal
    }
    throw err;
  }
}
```

**Key data:** uploads should be **resumable at part granularity**; persist `uploadId`, `key`,
part size, and completed `{PartNumber, ETag}` tuples server-side (or in the client with a
server-issued session token). A resume must never restart from zero if parts already exist.

## 43.5 — Multipart mechanics and limits

The S3 multipart contract — memorize these numbers, they shape your client design:

| Rule | Value |
| ---- | ----- |
| Minimum part size | **5 MB** (except the last part, which may be smaller) |
| Maximum parts | **10,000** |
| Part numbers | **1–10,000** (inclusive) |
| Maximum object size | **5 TB** |
| Maximum single `UploadPart` | 5 GB |
| Part identity | `(UploadId, PartNumber)`; re-uploading a number replaces it |
| Completion requirement | Parts in ascending order, each with its `ETag` |
| Multipart ETag form | `<md5-of-part-md5s>-<partCount>` (not a plain MD5) |

Two consequences fall out of the 10,000-part cap:

- For a 5 TB object you must use **~500 MB parts** (5 TB / 10,000), not 5 MB parts.
- Choose part size as `max(5 MB, ceil(expectedSize / 10_000))` and round up, with headroom
  for the object growing.

```ts
function choosePartSize(expectedBytes: number): number {
  const MIN = 5 * 1024 * 1024;
  const needed = Math.ceil(expectedBytes / 10_000);
  // Round up to a power-of-two-ish MB boundary for cache-friendly transfers.
  return Math.max(MIN, Math.ceil(needed / (1024 * 1024)) * 1024 * 1024);
}
```

### The resume protocol

```text
Client                          Your API                        Storage
  │  POST /uploads/init           │                                │
  │  {name,size,type}  ──────────▶│ validate, CreateMultipart ────▶│
  │  ◀── {uploadId, partSize, signedUrls[]}
  │                                                               │
  │  PUT part 1 ──────────────────────────────────────────────────▶│  ETag1
  │  PUT part 2 ──────────────────────────────────────────────────▶│  ETag2
  │  ✖ connection lost                                            │
  │  GET /uploads/{id}/parts ─────▶│ ListParts ────────────────────▶│
  │  ◀── [{1,ETag1},{2,ETag2}]                                    │
  │  PUT part 3..N (from part 3) ─────────────────────────────────▶│
  │  POST /uploads/{id}/complete  │ CompleteMultipart ────────────▶│
  │  ◀── {key}                    │                                │
```

Rules that make this protocol correct:

1. **`ListParts` is the source of truth** on resume — never trust a client's claim about what
   it uploaded.
2. **Part re-upload replaces** the previous part with the same number; retries are safe.
3. **Persist the session** (upload id + key + expected size) so a new browser/device can
   resume; bind it to the tenant and user.
4. **Expire sessions.** An upload nobody completes must be aborted, not left to accrue parts.
5. **Verify checksums per part** where supported; a corrupted part that is "present" is worse
   than a missing one.

**Key data:** some clients (browser SDKs) use 5 MB parts by default; at that size a 100 GB
file needs 20,000 parts and **exceeds the 10,000 limit** — the upload fails only at completion
time. Validate `ceil(size / partSize) ≤ 10_000` at session creation and reject early with a
clear `UPLOAD_TOO_MANY_PARTS` error.

## Worked example — the 90% upload that never finished

Acme's desktop client uploaded 4 GB video exports with 5 MB parts — 819 parts, fine — but
stored resume state only in memory. Every client restart re-created a multipart upload,
leaving the previous one with hundreds of parts. Over a quarter, the bucket accumulated
**2.1 TB of invisible incomplete uploads** (about $50/month, plus a scary audit finding). Two
fixes: (1) persist `uploadId` + completed parts keyed by `(tenantId, fileHash)` so a restart
resumes instead of restarting; (2) an `AbortIncompleteMultipartUpload` lifecycle rule with
`DaysAfterInitiation: 7` as the backstop. Storage cost returned to baseline, and resume success
went from 0% (client restart) to ~98%.

## Real-world use case — the abandoned uploads that cost $3,100 a month

Acme's browser client started multipart uploads for anything over 100 MB and abandoned
them whenever the tab closed. Nothing aborted the session, and no lifecycle rule existed,
so incomplete uploads accumulated in the bucket for months. The bill showed it: ~40% of
Acme's storage spend was **multipart parts belonging to nobody**, invisible to the object
list because no object had been completed.

Two fixes, at two levels. The **session** now gets an owner and an expiry the moment
`CreateMultipartUpload` returns, and the client registers a `beforeunload` handler that
aborts it. The **bucket** got the backstop — a lifecycle rule with
`AbortIncompleteMultipartUpload` and `DaysAfterInitiation: 7` — so even a client that
crashes entirely cannot leak a session past a week. A daily sweeper calls
`ListMultipartUploads` and aborts sessions whose owner has not checked in.

Storage spend on orphaned parts fell by 71% in the first full month, and the bucket's
`IncompleteMultipartUpload` count went from a steady 1,800 to under 40. The lesson:
**the client is not a reliable janitor; the lifecycle rule is.**

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Single PUT | Simplest | No resume; size ceiling | < 100 MB, stable networks |
| Multipart, no resume state | Faster than single | Restarts on drop; orphan parts | Never for large files |
| Multipart + resume + lifecycle | Resilient, cheap | More state, more code | ✅ Default for > 100 MB |
| Resumable upload via provider SDK | Handles protocol | Vendor lock-in | If the SDK is well supported |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Persist `uploadId` and completed parts | Keep resume state only in browser memory |
| Call `ListParts` before resuming | Trust the client's progress claim |
| Choose part size so parts ≤ 10,000 | Default to 5 MB parts for any size |
| Handle `NoSuchUpload` on completion as check-then-decide | Retry completion blindly |
| Abort sessions on user cancel and on TTL | Leave orphaned parts to bill silently |
| Verify part checksums | Assume "uploaded" means "intact" |

## Common mistakes

- **Completion retried after a timeout** — first call succeeded; retry returns `NoSuchUpload`
  and the client reports failure for a file that exists.
- **Part size too small** — 10,000-part cap hit only at the end.
- **No lifecycle rule** — orphaned parts accumulate for years.
- **Resume keyed by filename only** — two users, same name, cross-tenant resume.
- **No abort on cancel** — user cancels, parts stay billable.

## Checklist

- [ ] Client computes part size with the 10,000-part cap at session creation.
- [ ] `uploadId` and completed part ETags persist across client restarts.
- [ ] Resume always reconciles with `ListParts`.
- [ ] `CompleteMultipartUpload` failures distinguish "already completed" from "expired."
- [ ] `AbortMultipartUpload` is called on cancel and on TTL.
- [ ] `AbortIncompleteMultipartUpload` lifecycle rule exists as a backstop.

## Related

- [Multipart Upload Resume and Cleanup — Mechanics](../02-deep-dive/01-multipart-resume-and-cleanup-mechanics.md)
- [S3 Multipart Upload with Cleanup](../03-practical-examples/01-s3-multipart-upload-with-cleanup.ts)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- [Chapter 43 Reference](../05-reference/README.md)
