# Chapter 43 — Do's and Don'ts

> Part XVI · Chapter 43 · All sections

A condensed rule set for file and media processing. Use it as a review checklist for any
change that touches uploads, storage objects, or processing workers.

## Upload validation

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Sniff **magic bytes** from the first bytes of the body | Trust the client's `Content-Type` header |
| Enforce an **allowlist** of types, matched by sniffed type | Accept "any type" and rely on a download header later |
| Enforce size limits on the **declared and the actual** byte count | Only check the declared size |
| Cap decompressed size when the format is compressed (zip, gzip) | Let a 10 KB zip expand to 10 GB |
| Reject a file whose extension and sniffed type disagree | Rename `.exe` to `.png` and pass |
| Run the validator in the API process, before any bytes are stored | Validate after the object is already in the bucket |
| Return **stable codes** (`UPLOAD_TYPE_NOT_ALLOWED`) | Return "file type not supported" strings to branch on |

## Storage-provider errors

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify provider errors once: transient vs permanent | `catch { retry() }` around every storage call |
| Retry `SlowDown`, `InternalError`, `RequestTimeout` with jittered backoff | Retry `AccessDenied` or `SignatureDoesNotMatch` |
| Cap the retry budget (typically 3–5 attempts) | Retry forever inside a request |
| Surface exhausted storage failures as **503** with a retry hint | Surface them as 500 or 400 |
| Treat a timeout **after** the request was sent as ambiguous | Assume a timeout means "nothing happened" |
| Reconcile ambiguous writes (head the object) before declaring failure | Re-send blindly and create duplicates |

## Multipart uploads

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Compute the part size **before** the first byte moves | Discover the 10,000-part limit at completion time |
| Keep every non-final part at **5 MiB or larger** | Use 1 MiB parts to "save time" |
| Send parts **in parallel but bounded** (4–8 concurrent) | Fire 1,000 concurrent `UploadPart` calls |
| Record the session (upload id, key, part size, expected bytes) **before** returning URLs | Hand out part URLs with no server-side record |
| `Complete` with parts sorted by part number and their exact ETags | Complete with stale or missing ETags |
| Abort the upload when the client cancels or validation fails | Leave the upload open "in case they come back" |
| Add an `AbortIncompleteMultipartUpload` lifecycle rule | Rely on your sweeper alone for sessions never persisted |

**Key data:** 5 MiB minimum part size (except the last), **10,000 parts maximum**, **5 TiB**
object maximum, presigned URL maximum **7 days** (issue 15 minutes).

## Resume and idempotency

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Resume from `ListParts`, not from client memory | Trust the client's list of what it uploaded |
| Re-send a part under the **same part number** to replace it | Append a new part for the same range |
| Verify part sizes against the plan and re-send mismatches | Assume a part of the right number is the right bytes |
| Treat `NoSuchUpload` at completion as **ambiguous**, then `HeadObject` | Retry completion blindly and report failure for an existing object |
| Derive derivative keys from content hash + transform version + params | Put a timestamp or UUID in the derivative key |
| Make the checkpoint record steps whose **output exists** | Checkpoint steps that were merely attempted |
| Verify checkpointed outputs exist on resume | Trust the checkpoint blindly |

## Processing and scanning

| ✅ Do | ❌ Don't |
| ----- | -------- |
| **Quarantine first** — objects land unreadable, then get promoted | Write user uploads straight into the serving prefix |
| Fail **closed** when the scanner is unavailable or errors | Serve unscanned files when the scan times out |
| Treat `INFECTED` as a **permanent, per-item** failure | Retry an infected file until the quota runs out |
| Treat a scanner **error** as retryable and keep the file quarantined | Mark a scan error as "clean" |
| Bound every step: time, bytes, pixels, memory | Run an unbounded decode on user-supplied bytes |
| Isolate the decoder in a sandboxed worker | Parse untrusted media in the API process |
| Keep the scanned definition version with the verdict | Re-scan against a silently updated definition set |
| Exclude archives and encrypted containers by default | Scan every byte of a 40 GB archive |

**Key data:** scan status vocabulary is `pending` → `clean` | `infected` | `error`; only
`clean` may be served; promotion order is **copy → mark clean → delete quarantine**.

## Downloads and signed URLs

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Issue **short-lived** signed URLs (minutes, not days) | Issue 7-day public URLs for private content |
| Generate the URL only after the clean gate passes | Sign any object in the bucket |
| Serve the **stored** content type, not the uploaded one | Echo the client's `Content-Type` on download |
| Set `Content-Disposition: attachment` for user uploads | Render user HTML inline in your origin |
| Send `X-Content-Type-Options: nosniff` | Assume the browser respects the extension |
| Support range requests with the stored ETag as `If-Range` | Regenerate a derivative on every range request |
| Let the **owner** delete the object, with the deletion recorded | Delete on a client-supplied key alone |

## Cleanup and lifecycle

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give every artifact an **owner and a TTL** | Create temp objects that nobody cleans up |
| Sweep expired sessions on a schedule and abort their uploads | Assume the lifecycle rule covers sessions you never persisted |
| Treat cleanup as a **failure path** with its own metrics | Run cleanup only on the happy path |
| Delete quarantine objects after promotion | Keep two copies forever |
| Expire stale derivatives when a transform version is retired | Leave old rendition versions serving traffic |
| Alert on the growth of stored quarantine bytes | Watch only the request error rate |

## Batches and duplicate processing

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return **per-item** success/failure for a batch | Fail a 10,000-item batch because one item is corrupt |
| Checkpoint the batch cursor after each item | Restart the whole batch after a worker crash |
| Bound concurrency per tenant and globally | Let one tenant saturate the worker pool |
| Dead-letter only the exhausted items, with replay context | Dead-letter the entire batch |
| Cap the attempt count per item | Retry a permanent failure forever |
| Report per-item **stable codes**, not raw messages | Return one message for a heterogeneous batch |

## Anti-patterns in the wild

1. **The Timestamped Derivative** — every retry writes a new key, so a re-run doubles the
   storage bill and the CDN serves the older rendition.
2. **The Invisible Upload** — a multipart upload with no abort and no lifecycle rule, billed
   forever for parts nobody can read.
3. **The Fail-Open Scanner** — a scan timeout marks the file clean and the CDN serves it.
4. **The All-Or-Nothing Import** — one corrupt JPEG in a 10,000-image ZIP fails the job.
5. **The Trusting Validator** — the extension is checked, the bytes are not.
6. **The Unbounded Decoder** — a user-supplied file drives the worker's memory to zero.
7. **The Client-Memory Resume** — the browser remembers what it uploaded; the server does not.

## Chapter checklist

- [ ] Uploads are validated by content at the trust boundary, with size and type limits.
- [ ] Storage errors are classified once, and permanent ones are never retried.
- [ ] Part size is planned before transfer; the 5 MiB / 10,000-part / 5 TiB limits are enforced.
- [ ] Every multipart session has a record, an owner, a TTL, and an abort path.
- [ ] Resume reads the store's part list and verifies sizes.
- [ ] Derivative keys are a pure function of content, version, and parameters.
- [ ] Scans fail closed; only `clean` objects are served.
- [ ] Downloads use short-lived signed URLs with the stored content type.
- [ ] Batches return per-item outcomes and checkpoint their cursor.
- [ ] Cleanup runs on a schedule and is monitored like a product feature.

## Related

- [Chapter 43 Reference](../05-reference/README.md)
- [Chapter 28 — Idempotency](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- [Part XVI Index](../../README.md)
