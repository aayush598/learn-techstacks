# Multipart Resume and Cleanup — Mechanics

> Part XVI · Chapter 43 · Sections 43.4, 43.5, 43.11 · _Estimated reading time: 24 min_
> **Prerequisite:** [Interrupted Uploads and Multipart](../01-concepts/02-interrupted-uploads-and-multipart.md)

## In one sentence

A multipart upload is a **three-state protocol** — initiated, completed, aborted — and it
is only safe if **every initiated upload eventually reaches one of the two terminal states**.

## Why this matters in production

Multipart is the only storage API most teams use where **you can lose money without losing
data**. The parts are stored, billed, and invisible: they have no object key, so they never
appear in a console listing, and `ListObjectsV2` will never show them. A customer who
abandons an upload leaves a bill you cannot reconcile by looking at your bucket. On top of
that, completion is **ambiguous** — it can succeed and time out at the same time — so a
naive retry reports failure for an object that exists.

## The protocol, formally

```text
        CreateMultipartUpload
                 │
                 ▼
        ┌─────────────────────┐
        │    IN PROGRESS       │   UploadId + Key define the session
        │  parts 1..N upload  │   ListParts returns {PartNumber, ETag, Size, Checksum}
        └──────┬──────────────┘
               │
     ┌─────────┼─────────────────────────────┐
     ▼         ▼                             ▼
 Complete   AbortMultipartUpload        (never called)
     │         │                             │
     ▼         ▼                             ▼
┌─────────┐ ┌─────────┐              ┌──────────────┐
│COMPLETED│ │ ABORTED │              │ ORPHANED     │
│object   │ │parts    │              │ billed but   │
│visible  │ │deleted  │              │ invisible;   │
└─────────┘ └─────────┘              │ lifecycle    │
                                     │ reaps it     │
                                     └──────────────┘
```

Four states, and **only two of them are terminal**. `ORPHANED` is the failure mode this
chapter keeps coming back to: the upload is neither completed nor aborted, so the parts sit
in the bucket consuming storage, request-count, and multipart-quota budget.

## Part identity and ETags

A part is identified by the pair `(UploadId, PartNumber)`. Two consequences fall straight
out of that:

1. **Re-uploading a part number replaces the part.** Part upload is idempotent — a retry
   with the same number overwrites, it does not append. This is why part-level retries are
   safe, and why the resume protocol can freely re-send a part it is unsure about.
2. **The `ETag` is the receipt.** It is what the completion call expects back, and it is
   what proves which bytes the store holds.

The ETag of a multipart object is *not* the MD5 of the object:

```text
multipart ETag = md5( concat(md5(part_1), md5(part_2), …) ) + "-" + partCount
example:        "9a0364b9e99bb480dd25e1f0284c8555-42"
```

Consequences:

- You **cannot** verify a multipart object's integrity with a single MD5 of the whole file.
- You must verify **per part**, using the per-part checksum the store returns
  (`ChecksumSHA256` / `x-amz-checksum-sha256`), and then optionally ask for an aggregated
  checksum at completion with `ChecksumMode: "ENABLED"`.
- A code that compares `ETag === md5(fileBytes)` will "fail" on every correctly-uploaded
  multipart object. This is a real bug in the wild.

```ts
type StoredPart = {
  partNumber: number;
  eTag: string;             // opaque receipt
  size: number;
  checksumSHA256?: string;  // base64; present only when ChecksumAlgorithm was requested
};

const res = await s3.uploadPart({ Bucket: BUCKET, Key: session.key, UploadId: session.uploadId,
  PartNumber: part.partNumber, Body: body, ChecksumAlgorithm: "SHA256" });
if (res.ChecksumSHA256 && res.ChecksumSHA256 !== base64(sha256(body))) {
  throw new PartChecksumMismatch({ partNumber: part.partNumber });   // terminal for this part
}
```

**Key data:** part numbers are **1–10,000**; re-upload by number **replaces**; the multipart
ETag is `<md5-of-part-md5s>-<partCount>`, so it is **not** a whole-file MD5; per-part
checksums need `ChecksumAlgorithm: "SHA256"` and `ChecksumMode: "ENABLED"`.

## Choosing part size

Part size is not a tuning knob — it is a **constraint solve**:

```ts
const MIN_PART = 5 * 1024 * 1024;   // 5 MiB, except the last part
const MAX_PARTS = 10_000;

function planParts(expectedBytes: number, maxPart = 64 * 1024 * 1024) {
  let partSize = Math.min(maxPart, Math.max(MIN_PART, expectedBytes));
  while (Math.ceil(expectedBytes / partSize) > MAX_PARTS) partSize *= 2;
  const count = Math.ceil(expectedBytes / partSize);
  if (count > MAX_PARTS) throw new UploadTooManyParts({ needed: count, max: MAX_PARTS });
  return { partSize, count };
}
```

| Rule | Value |
| ---- | ----- |
| Minimum part size | **5 MiB** (the final part may be smaller) |
| Maximum parts | **10,000** |
| Maximum part size | 5 GiB |
| Maximum object size | **5 TiB** |
| Part size for a 5 TiB object | ≈ **512 MiB** (5 TiB / 10,000 parts) |

A 5 TiB object forces roughly **512 MiB parts**, so a "just use 5 MB parts" default breaks
the largest tier of customers only at completion time.

> ⚠️ **Hazard.** The 10,000-part limit is enforced **at completion**. A client that used
> 5 MB parts for a 100 GB file uploads 20,000 parts successfully and then fails on
> `CompleteMultipartUpload`. Validate `ceil(size / partSize) ≤ 10,000` when the session is
> created, and reject with `UPLOAD_TOO_MANY_PARTS` before a single byte is transferred.

## Resume: `ListParts` is the source of truth

The client's claim about what it uploaded is a hint, not a fact. The store's list is the
fact. The resume protocol is therefore: **ask the store, then send only what is missing.**

```ts
async function resume(session: UploadSession): Promise<StoredPart[]> {
  const remote: StoredPart[] = [];
  for await (const page of s3.listPartsPaginator({
    Bucket: BUCKET, Key: session.key, UploadId: session.uploadId,
  })) {
    remote.push({ partNumber: page.PartNumber, eTag: page.ETag!, size: page.Size!,
                  checksumSHA256: page.ChecksumSHA256 });
  }
  // Parts whose stored size disagrees with the plan are stale/corrupt: re-send them.
  return remote.filter((p) => p.size === expectedSize(p.partNumber, session));
}
```

The filter is not optional. A part can be *present* and *wrong* — a retry that uploaded a
truncated body after the connection reset mid-write. Because part identity is
`(UploadId, PartNumber)`, re-uploading fixes it; comparing the stored size detects it.

Rules that make resume correct:

1. **Reconcile with the store before sending anything.** Never trust client progress state.
2. **Re-send by part number** — replacement semantics make it safe.
3. **Persist the session** (`uploadId`, `key`, `partSize`, `expectedSize`) server-side so a
   different device or process can resume; bind it to `tenantId` and `userId`, and key it on
   `(tenantId, contentSha256)` so a *different* file cannot resume into this upload.
4. **Expire sessions.** An upload nobody completes is aborted, not left to accrue.

## Completion is ambiguous

`CompleteMultipartUpload` assembles the object from the parts you list. The call can fail
in ways that look identical but mean different things:

| Response | Meaning | Action |
| -------- | ------- | ------ |
| 200 + `ETag` | Object created | Success |
| `NoSuchUpload` | Upload id unknown | **Ambiguous** — it may already be completed |
| `InvalidPart` | ETag/part mismatch | Re-`ListParts`, re-send the bad part |
| `InvalidPartOrder` | Parts not ascending | Sort and retry — a bug in *your* code |
| `EntityTooSmall` | A non-final part is < 5 MiB | Re-plan part size; cannot fix in place |
| `MalformedXML` | Malformed request body | Bug — never retry unchanged |
| 5xx / timeout | Store-side problem | **Ambiguous** — check before retrying |

The `NoSuchUpload` case is the one to internalize: **the first completion may have
succeeded**, and the retry sees a session that no longer exists. The only correct response
is *check, then decide*:

```ts
async function completeSafely(session: UploadSession, parts: StoredPart[]) {
  const sorted = [...parts].sort((a, b) => a.partNumber - b.partNumber);   // ascending
  try {
    const res = await s3.completeMultipartUpload({
      Bucket: BUCKET, Key: session.key, UploadId: session.uploadId,
      MultipartUpload: { Parts: sorted.map((p) => ({ PartNumber: p.partNumber, ETag: p.eTag })) },
      ChecksumMode: "ENABLED",
    });
    return { ok: true, eTag: res.ETag };
  } catch (err) {
    if (err.name === "NoSuchUpload") {
      // Either (a) a previous attempt already completed it, or (b) it was aborted/expired.
      const head = await s3.headObject({ Bucket: BUCKET, Key: session.key }).catch(() => null);
      if (head) return { ok: true, eTag: head.ETag, alreadyCompleted: true };
      throw new UploadSessionExpired({ uploadId: session.uploadId });        // terminal
    }
    if (err.name === "InvalidPart") throw new PartMismatch({ uploadId: session.uploadId });
    throw err;
  }
}
```

`InvalidPartOrder` can never happen if you sort, and `EntityTooSmall` cannot be fixed after
the fact — both are **pre-flight** checks that belong in session creation, not in the
completion error handler.

**Key data:** `NoSuchUpload` on completion means "already completed or gone" — always
`HeadObject` first. `InvalidPartOrder` ⇒ client bug. `EntityTooSmall` ⇒ part under 5 MiB.

## Abort and the cleanup obligation

Aborting is simple; the obligation is not. Every `CreateMultipartUpload` must end in
`Complete` or `Abort`. There are exactly four ways an upload dies without reaching either:

| Death | Detection | Cleanup |
| ----- | --------- | ------- |
| User cancels | Explicit | `AbortMultipartUpload` immediately |
| Session TTL expires | Sweeper job | `AbortMultipartUpload` |
| Process crash mid-upload | Sweeper job | `AbortMultipartUpload` |
| Never detected | Lifecycle rule | `AbortIncompleteMultipartUpload` |

The lifecycle rule is the backstop that covers the cases your code cannot see:

```json
{
  "Rules": [{
    "ID": "abort-incomplete-multipart-uploads",
    "Status": "Enabled",
    "Filter": { "Prefix": "uploads/" },
    "AbortIncompleteMultipartUpload": { "DaysAfterInitiation": 7 },
    "Expiration": { "Days": 30 }
  }]
}
```

`DaysAfterInitiation` is measured from the `CreateMultipartUpload` call, and the rule
aborts the whole session — parts included. Choose it as "longer than any legitimate upload
session, short enough that the bill is bounded". For a resumable-upload product with a 24 h
session TTL, **7 days** is the common choice; for a same-day product, 2–3 days is fine.

Layer your cleanup: **active abort** on cancel and TTL; a **session sweeper** for sessions
older than the TTL (needs the `uploadId` stored, which is why the session row must persist
it); and the **lifecycle rule**, the only layer that catches a crash between "create" and
"persist".

> ⚠️ **Hazard.** If your sweeper only knows `uploadId` values it stored, a crash between
> `CreateMultipartUpload` and the DB write leaks a session that no code will ever abort.
> Write the session row *before* creating the upload (and abort on create failure), or
> rely on the lifecycle rule as the only guaranteed backstop. Doing both is the answer.

### Cleanup ownership, artifact by artifact

| Artifact | Owner | TTL | Enforcement |
| -------- | ----- | --- | ----------- |
| Incomplete multipart parts | Upload session | 7 days | Lifecycle `AbortIncompleteMultipartUpload` |
| Presigned part URLs | Request handler | ≤ 15 min | Expiry, never persisted |
| Temp files on workers | Processing job | Job lifetime | `finally` cleanup + sweeper |
| Quarantine objects | Scan service | 30 days | Lifecycle `Expiration` |

Presigned URL expiry bounds how long a paused upload can stay paused — a 15-minute URL
forces the client to **re-request part URLs on resume**. URL lifetime and session lifetime
are different clocks.

**Key data:** presigned URL maximum validity is **7 days** (SigV4), but part URLs are
typically issued with **5–15 minutes**; `DaysAfterInitiation` is commonly **7**;
`AbortMultipartUpload` is idempotent — aborting an already-aborted or completed upload is a
no-op success.

## Worked example — the 2.1 TB of invisible parts

Acme's desktop client uploaded 4 GB exports in 5 MiB parts and kept resume state **in
browser memory only**. Every client restart began a *new* multipart upload, and the old one
kept its parts. Over a quarter the bucket accumulated **2.1 TB of incomplete uploads** —
roughly $50/month, invisible in the console, and the first item on the quarterly audit
findings list. Two fixes: (1) persist `{uploadId, key, partSize, completedParts}` keyed on
`(tenantId, contentSha256)` so a restart *resumes* instead of restarting; (2) an
`AbortIncompleteMultipartUpload` rule with `DaysAfterInitiation: 7`. Storage spend returned
to baseline and resume success went from 0% to ~98%.

## Real-world use case — the resumed export that kept restarting

Acme's `ExportJob` uploads a customer's media set to the object store in parts. On a
flaky connection the client resumed with `ListParts`, found every part it expected, and
called `CompleteMultipartUpload` — which failed with `InvalidPart` (HTTP `400`). The
client's error handling treated `InvalidPart` as "the upload is corrupt", threw away the
`uploadId`, and started over from part 1. On a 2.4 TB export that never finished: resume
success sat at 41%.

The root cause was a **part identity** mismatch. One part had been uploaded through a
different client path whose line endings differed, so its ETag did not match the one the
server had recorded, and `CompleteMultipartUpload` requires the exact ETag list. The
server had the correct ETag in `ListParts`; the client had overwritten its local copy
with the ETag from its own re-upload.

The fix moved the source of truth to the store. On resume, the server calls `ListParts`
and **rebuilds the ETag list from the store's response**, never from client state; the
client sends only the part numbers it believes are done, and the server verifies them
against `ListParts`. A mismatch on one part is now a targeted single-part repair, not a
restart — and a `CompleteMultipartUpload` that returns `InvalidPart` is classified as a
**retryable, targeted** failure rather than a terminal one.

Resume success rose from 41% to 99.4%, and the median completion time for the same
export fell from 6.2 hours to 51 minutes. The lesson: **the store's part list is the only
authority on what has been uploaded; your client's memory is a guess.**

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Multipart, no resume state | Faster than single PUT | Restarts on drop; orphan parts | Never for large files |
| Multipart + `ListParts` resume | Survives drops and restarts | Extra state and a round trip | ✅ Default > 100 MB |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Reconcile with `ListParts` before resuming | Trust the client's progress claim |
| `HeadObject` on `NoSuchUpload` before failing | Retry completion blindly |
| Validate `ceil(size / partSize) ≤ 10,000` at session creation | Discover the cap at completion time |
| Abort on cancel, on TTL, and via lifecycle rule | Leave orphaned parts to bill silently |

## Common mistakes

- **Retrying `CompleteMultipartUpload` after a timeout** — first call succeeded; the retry
  returns `NoSuchUpload` and the client reports failure for an object that exists.
- **Comparing the multipart ETag to a whole-file MD5** — always mismatches; every integrity
  check "fails" and someone disables the check.
- **5 MiB parts for a 100 GB file** — 20,000 parts; the upload dies at completion.
- **Resume keyed by filename** — one tenant resumes into another's upload.
- **Sweeper that only knows stored `uploadId`s** — the crash-before-persist leak.

## Checklist

- [ ] Part size chosen so `ceil(size / partSize) ≤ 10,000`, validated before transfer.
- [ ] Session row persists `uploadId`, `key`, `partSize`, and per-part ETags.
- [ ] Resume reconciles with `ListParts` and re-sends size/checksum mismatches.
- [ ] Completion sorts parts ascending and handles `NoSuchUpload` as check-then-decide.
- [ ] `AbortMultipartUpload` is called on cancel and on session TTL.
- [ ] An `AbortIncompleteMultipartUpload` lifecycle rule exists as the backstop.
- [ ] Per-part checksums requested and compared; part URLs expire in minutes.

## Related

- [Interrupted Uploads and Multipart](../01-concepts/02-interrupted-uploads-and-multipart.md)
- [Downloads, Cleanup, Duplicate Processing, and Batch](../01-concepts/04-downloads-cleanup-and-batch.md)
- [S3 Multipart Upload with Cleanup](../03-practical-examples/01-s3-multipart-upload-with-cleanup.ts)
- [Chapter 43 Reference](../05-reference/README.md)
