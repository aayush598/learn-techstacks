# Processing, Malformed Files, Malware Scanning, and Temp URLs

> Part XVI · Chapter 43 · Sections 43.6–43.9 · _Estimated reading time: 20 min_
> **Prerequisite:** [Upload Validation and Storage Failures](./01-upload-validation-and-storage-failures.md)

## In one sentence

Once bytes are stored, every downstream step — decode, transform, scan, serve — can fail on
**attacker-chosen input**, so processing must be bounded, scanning must **fail closed**, and
temporary URLs must be short-lived, single-purpose capabilities.

## Why this matters in production

A malformed PDF crashes the renderer; a crafted image exhausts worker memory; a 4 GB zip
expands to 400 GB; a scan that times out and lets the file through serves malware under your
brand. Then there is the delivery side: a signed URL with a 7-day expiry forwarded in a Slack
channel is a public download link, and a URL that signs only the path lets a user swap the
`Content-Type` on the way out. Each of these is a different failure with a different fix, and
all of them are silent unless you design the failure path explicitly.

## 43.6 — Processing and transformation failures

Processing is a pipeline of bounded steps. Each step can fail in three ways:

| Failure | Example | Class | Handling |
| ------- | ------- | ----- | -------- |
| Unsupported input | Codec not available for a `.mov` variant | Permanent | `422 UNSUPPORTED_FORMAT`, itemized |
| Corrupt input | Truncated JPEG, bad PDF xref table | Permanent (for this file) | `422 MALFORMED_MEDIA`; do not retry |
| Resource exhaustion | Image claims huge dimensions; OOM | Permanent-ish | Cap work; retry once with lower limits |
| Worker crash | Segfault in native decoder | Transient infra | Retry on a fresh worker, then quarantine |
| Timeout | Transcode exceeds budget | Config-dependent | Extend budget or mark `PROCESSING_TIMEOUT` |
| Dependency down | OCR service 503 | Transient | Retry with backoff, then leave `pending` |

The design rule: **separate "this file cannot be processed" from "we could not process it
right now."** The first is terminal for the file and must not be retried forever; the second
is a job failure that retries and eventually dead-letters.

```ts
type ProcessResult =
  | { ok: true; derivatives: Derivative[] }
  | { ok: false; retryable: false; code: "MALFORMED_MEDIA" | "UNSUPPORTED_FORMAT"; detail: string }
  | { ok: false; retryable: true; code: "DEPENDENCY_UNAVAILABLE" | "TIMEOUT" };

async function transform(input: StoredObject): Promise<ProcessResult> {
  try {
    const decoded = await decodeBounded(input, { maxPixels: 40_000_000, timeoutMs: 30_000 });
    return { ok: true, derivatives: await renderDerivatives(decoded) };
  } catch (err) {
    if (err instanceof DecodeError) return { ok: false, retryable: false, code: "MALFORMED_MEDIA", detail: err.message };
    if (err instanceof UnsupportedFormat) return { ok: false, retryable: false, code: "UNSUPPORTED_FORMAT", detail: err.format };
    return { ok: false, retryable: true, code: "DEPENDENCY_UNAVAILABLE" };
  }
}
```

**Key data:** bound every transform — pixel count, duration, decompressed bytes, CPU seconds,
wall-clock timeout. A worker timeout is a **failure**, not a slow success; a partial derivative
must never be published as complete.

## 43.7 — Malformed files

Malformed input is expected, not exceptional. The safe posture:

1. **Parse in an isolated, resource-capped process** (a subprocess or sandbox), never in the
   API process.
2. **Treat parser exceptions as data errors**, not crashes — catch them at the worker boundary
   and record `MALFORMED_MEDIA` with a safe excerpt of the parser message.
3. **Quarantine, don't delete silently.** Store the original with `status: rejected` so support
   can answer "why did my file fail?" without the bytes being servable.
4. **Never echo raw parser output to users** — it can contain memory addresses, paths, or
   attacker-controlled strings (see Chapter 34).

Polyglot files deserve a mention: a file that is a valid JPEG *and* a valid ZIP (or HTML) is a
classic bypass. If you accept images, re-encode them rather than serving the original bytes;
re-encoding destroys the second interpretation.

## 43.8 — Malware scanning

Scanning is a **gate**, and gates fail closed:

```text
upload ──▶ stored as quarantine/<id> ──▶ scan
                                            │
              ┌─────────────────────────────┼──────────────────────────┐
              ▼                             ▼                          ▼
          clean                        infected                    scan failed
   promote to media/<id>        keep quarantined, alert,     keep quarantined, retry
   serve via signed URL         notify tenant, never serve   (bounded); after N ⇒
                                                             fail closed + alert
```

| Outcome | User sees | Serving |
| ------- | --------- | ------- |
| `clean` | File available | Signed URL allowed |
| `infected` | "File rejected by security scan" | Never; optionally allow quarantine download for admins |
| `scan_error` / timeout | "File is being checked" | **No** — fail closed |
| `scan_unavailable` (provider down) | "Uploads are temporarily delayed" | No; queue and scan when back |

> ⚠️ **Hazard.** Failing **open** on scan errors is how malware gets served with your domain
> in the `Content-Disposition`. If the scanner is down, the correct behavior is to wait, not
> to serve unverified bytes.

**Key data:** scanning timeouts are common on large archives; set a scan budget and treat
exceeding it as `scan_error`, not `clean`. Keep the quarantine bucket private and separate
from the serving bucket. Scan **after** upload completes but **before** any URL is issued —
never scan asynchronously after the file is already downloadable.

## 43.9 — Temporary URLs

Signed URLs are bearer capabilities. Treat them like passwords:

| Property | Rule |
| -------- | ---- |
| TTL | As short as the use case allows — seconds to minutes for reads |
| Maximum (SigV4) | **7 days** for presigned URLs; temporary credentials cannot outlive their session |
| Scope | One object, one method (GET), signed content type where possible |
| Binding | Include `Content-Disposition` and `Content-Type` in the signature |
| Revocation | Not possible for a signed URL — shorten TTL instead; rotate keys for emergencies |
| Logging | Never log the full URL (it is a credential) |

```ts
// Sign the response headers too, so the browser cannot be tricked into rendering HTML.
const url = await getSignedUrl(s3, new GetObjectCommand({
  Bucket: MEDIA_BUCKET,
  Key: objectKey,
  ResponseContentType: "application/octet-stream",
  ResponseContentDisposition: `attachment; filename="${safeFilename}"`,
}), { expiresIn: 300 });                       // 5 minutes
```

Two delivery rules complete the picture:

1. **Serve from a separate origin/domain** (e.g. `files.example-cdn.com`) so a content-type
   mistake cannot execute script in your app's origin.
2. **Never put tenant-identifying or sequential IDs in the path without authorization** —
   signing happens after an authorization check, not instead of one.

**Key data:** SigV4 presigned URL maximum **7 days**; recommended read TTL **≤ 5 minutes** for
private files and **≤ 1 hour** for share links, with revocation implemented as "short TTL +
re-issue," since individual URLs cannot be revoked.

## Worked example — Acme's invoice PDF queue

Acme generated invoice PDFs through a renderer that accepted uploaded logos. One logo was a
polyglot: valid PNG header, embedded JavaScript in a trailing chunk. The renderer was fine, but
the app served the original logo from the app origin with `Content-Type: image/png` derived
from the extension — and a browser that sniffed the trailing bytes executed the script. The
fix had four parts: magic-byte validation **plus** re-encode through the image library (which
dropped the trailing chunk), a malware scan gate that failed closed, serving from a separate
origin with `X-Content-Type-Options: nosniff` and signed `Content-Disposition: attachment`, and
logging that excluded the signed URL. No single fix would have been sufficient.

## Real-world use case — the scanner that silently skipped 9% of uploads

Acme's pipeline scanned every upload — except those over 2 GB, which took a "fast path"
that promoted the object straight to the serving prefix. The fast path existed for
legitimate large video files and was never revisited. For nine months, 9% of uploads
bypassed malware scanning entirely, and no metric showed it, because the only counter
counted *scan verdicts* and the fast path produced none.

The fix was to make the **absence** of a verdict detectable. Every upload now writes a
`scan_verdict` row — including `skipped_large` — and promotion requires a verdict row
that is not `pending`. A daily reconciliation compares `count(uploads)` against
`count(scan_verdict)` and alerts below 99.5%, which is how the 2.1% gap that remained
was traced to uploads that arrived while the scanner queue was drained.

Unscanned-and-promoted uploads went from 9% to 0, and the reconciliation alert now fires
within a day instead of never. The lesson: **a skip is a decision, and every decision
needs a record that something can check.**

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Synchronous scan before response | Simple flow | Slow uploads | Small files |
| Quarantine + async scan | Fast upload | File not immediately available | ✅ Default |
| Scan and fail open on error | Availability | Serves unverified bytes | Never |
| Long-lived public URLs | Cache-friendly | Permanent leak | Public assets only |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Re-encode untrusted media | Serve original bytes after a shallow check |
| Fail closed when scanning fails | Treat scan timeout as clean |
| Keep quarantine separate from serving | Serve from the upload bucket |
| Sign response content type/disposition | Sign only the object path |
| Use short TTLs for private files | Hand out 7-day URLs by default |
| Log a URL fingerprint, not the URL | Log full signed URLs |

## Common mistakes

- **Parsing in the request process** — a malformed file takes down the API.
- **Scan-after-publish** — the file is downloadable before the scan result arrives.
- **Retrying malformed files** — permanent failures burn the queue and delay good work.
- **Extension-derived content type on download** — sniffing and inline rendering.
- **Assuming signed URLs are revocable** — they are not; shorten the TTL.

## Checklist

- [ ] Processing runs in an isolated, resource-capped worker.
- [ ] Malformed input maps to a permanent `422`-class code, not retries.
- [ ] Files are quarantined until scanned clean.
- [ ] Scan failure/timeout blocks serving (fail closed).
- [ ] Signed URLs are short-lived and sign content type/disposition.
- [ ] Downloads come from a separate origin with `nosniff`.

## Related

- [Downloads, Cleanup, Duplicate Processing, and Batch](./04-downloads-cleanup-and-batch.md)
- [Malware Scanning and Quarantine Flow — Mechanics](../02-deep-dive/02-malware-scanning-and-quarantine-flow.md)
- [Chapter 34 — Security Principles for Error Handling](../../../part-13-security-aware/34-security-principles-for-error-handling/README.md)
- [Chapter 43 Reference](../05-reference/README.md)
