# Chapter 43 — Reference

> Part XVI · Chapter 43 · S3 multipart limits, upload/download status map, storage error
> classes, scan states, cleanup ownership, and glossary.

## S3 multipart limits and facts

| Fact | Value | Consequence |
| ---- | ----- | ----------- |
| Minimum part size | **5 MiB** (last part may be smaller) | Smaller parts ⇒ `EntityTooSmall` |
| Maximum parts per upload | **10,000** | Plan the part size *before* transfer |
| Maximum object size | **5 TiB** | Single `PutObject` cap is 5 GiB |
| `PutObject` single-request cap | 5 GiB | Above it, multipart is mandatory |
| Presigned URL maximum expiry | **7 days** | Issue minutes, not days |
| Part URL practical expiry | 5–15 min | Bounds a leaked URL's damage |
| Part numbering | 1 → 10,000, ascending | `Complete` needs ascending part numbers |
| ETag | MD5 of the part (not the object) for non-multipart part ETags | The object's ETag is `md5-N` for multipart |
| `CompleteMultipartUpload` parts | Exactly the parts you list | Omitting a part silently drops it |
| `AbortMultipartUpload` | Idempotent-ish; `NoSuchUpload` afterwards | Treat `NoSuchUpload` as success |
| Lifecycle rule | `AbortIncompleteMultipartUpload`, `DaysAfterInitiation` | Backstop for unpersisted sessions |

**Part planning.** Pick the largest part size that keeps the count under 10,000:

```text
partSize = max(8 MiB, ceil(expectedBytes / 10_000))
partCount = ceil(expectedBytes / partSize)
```

| Object size | Part size | Parts |
| ----------- | --------- | ----- |
| 50 MiB | 8 MiB | 7 |
| 1 GiB | 64 MiB | 16 |
| 500 GiB | 64 MiB | 8,000 |
| 1 TiB | 128 MiB | 8,192 |
| 5 TiB | 512 MiB | 10,000 |

**Key data:** the last part is the only one allowed below 5 MiB. A 5 TiB object needs at
least 512 MiB parts to stay inside the 10,000-part limit.

## Upload endpoint status map

| Condition | HTTP | Stable code | Retryable |
| --------- | ---- | ----------- | --------- |
| Type not on the allowlist / sniff failed | 415 | `UPLOAD_TYPE_NOT_ALLOWED` | ❌ |
| Declared or actual size over the limit | 413 | `UPLOAD_TOO_LARGE` | ❌ |
| Part count would exceed 10,000 | 400 | `UPLOAD_TOO_MANY_PARTS` | ❌ |
| Part bytes differ from the plan | 502 | `UPLOAD_PART_MISMATCH` | ✅ |
| Multipart upload gone (aborted/expired) | 410 | `UPLOAD_SESSION_EXPIRED` | ❌ |
| Scan has not cleared the file | 409 | `UPLOAD_NOT_CLEARED` | ✅ (wait) |
| Storage unreachable after retries | 503 | `STORAGE_UNAVAILABLE` | ✅ |
| Session not found (unknown id) | 404 | `UPLOAD_SESSION_NOT_FOUND` | ❌ |
| Tenant mismatch on the session | 403 | `UPLOAD_FORBIDDEN` | ❌ |
| Part URL expired | 403 | `UPLOAD_URL_EXPIRED` | ✅ (re-issue) |

## Storage-provider error classes

| Provider error name | Class | Action |
| ------------------ | ----- | ------ |
| `SlowDown` | Transient | Retry with jittered backoff; honor `Retry-After` |
| `InternalError` | Transient | Retry with backoff |
| `RequestTimeout` | Transient | Retry the same part number |
| `ServiceUnavailable` | Transient | Retry with backoff |
| `ExpiredToken` | Transient | Refresh credentials, then retry |
| `ECONNRESET` / `ETIMEDOUT` | Transient | Retry the same part number |
| `AccessDenied` | Permanent | Config/permission bug — never retry |
| `SignatureDoesNotMatch` | Permanent | Signing bug — never retry |
| `NoSuchBucket` | Permanent | Config bug |
| `EntityTooSmall` | Permanent | Part-size bug |
| `InvalidPart` | Permanent | Part-number/ETag bookkeeping bug |
| `InvalidPartOrder` | Permanent | Sort parts ascending before completing |
| `NoSuchUpload` | Terminal (ambiguous) | `HeadObject` to check whether it completed |
| `PreconditionFailed` | Success-shaped | Another writer produced the same content |

## Scan status table

| Status | Meaning | Servable? | Retriable? |
| ------ | ------- | --------- | ---------- |
| `pending` | Uploaded, not yet scanned | ❌ | — |
| `scanning` | A scanner is working on it | ❌ | — |
| `clean` | No threat found at definition version *v* | ✅ | — |
| `infected` | Threat found (rule name recorded) | ❌ | ❌ permanent |
| `error` | Scanner unavailable / unreadable file | ❌ | ✅ retryable |
| `quarantined` | Held for manual review (false positive appeal) | ❌ | ❌ human |

**Key data:** only `clean` is servable. `infected` is a per-item permanent failure; `error`
is retryable and must keep the object in quarantine. Re-scan when the scanner definition
version changes.

## Download and range-request facts

| Fact | Value |
| ---- | ----- |
| `Range` header | `bytes=0-1048575` (inclusive, 0-based) |
| `206 Partial Content` | Success for a range request |
| `416 Range Not Satisfiable` | Offset beyond the object size |
| `Content-Range` | `bytes 0-1048575/52428800` (total size last) |
| `ETag` / `If-Range` | Use the stored ETag; a mismatch ⇒ full 200 response |
| `Accept-Ranges` | `bytes` |
| Signed URL TTL | 5–15 min |
| `Content-Disposition` | `attachment; filename="..."` for user uploads |
| `X-Content-Type-Options` | `nosniff` |
| `Cache-Control` | `private, max-age=0, no-store` for signed responses |

## Cleanup ownership table

| Artifact | Owner | TTL / trigger | Reaper |
| -------- | ----- | ------------- | ------ |
| Incomplete multipart upload | `upload_session` row | 24 h | Scheduler + lifecycle rule (7 days) |
| Quarantined object | `file` row | 30 days | Scheduler |
| Temp derivative (preview, watermark) | `derivative` row | 1 h | Scheduler |
| Superseded rendition version | Transform version | On version retire | Scheduler |
| Expired signed URL | — | Minutes | n/a (stateless) |
| Stale processing job | `media_job` row | 24 h in `running` | Scheduler |
| Dead-lettered batch item | `batch_item` row | 30 days | Manual replay |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| **Trust boundary** | Where untrusted bytes enter the system and must be validated |
| **Magic bytes** | The leading bytes of a file that reveal its real format |
| **Multipart upload** | Chunked object upload: `Create` → `UploadPart`×N → `Complete`/`Abort` |
| **Part number** | 1-based index of a chunk in a multipart upload |
| **ETag** | Provider entity tag; part-level MD5, composite for the completed object |
| **Resume** | Continuing an interrupted upload from the store's part list |
| **Ambiguous completion** | `Complete` returns `NoSuchUpload`; the object may or may not exist |
| **Quarantine** | Prefix where uploads land and remain unreadable until scanned |
| **Promotion** | Copying a scanned-clean object from quarantine into the served prefix |
| **Derivative key** | Deterministic key of a transformed output; content-derived |
| **Checkpoint** | Durable record of completed units of work |
| **Content filter** | Provider-side refusal of unsafe content (`finish_reason: content_filter`) |
| **Fail closed** | Deny access when a check cannot be completed |
| **Range request** | Partial download of bytes via the `Range` header |

## Signposts

- Multipart and resume mechanics → [Multipart Resume and Cleanup Mechanics](../02-deep-dive/01-multipart-resume-and-cleanup-mechanics.md)
- Scanning and quarantine → [Malware Scanning and Quarantine Flow](../02-deep-dive/02-malware-scanning-and-quarantine-flow.md)
- Idempotent processing → [Processing Pipeline with Checkpoints](../03-practical-examples/02-processing-pipeline-with-checkpoints.md)
- Retry budget → [Chapter 29 Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
- Async workers → [Chapter 32 Background Jobs](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)

## Related

- [Chapter 43 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 43 Overview](../README.md)
- [Part XVI Index](../../README.md)
