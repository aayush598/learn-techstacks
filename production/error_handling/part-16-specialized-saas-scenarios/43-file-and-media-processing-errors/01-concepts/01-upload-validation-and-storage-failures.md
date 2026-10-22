# Upload Validation and Storage Failures

> Part XVI · Chapter 43 · Sections 43.1–43.3 · _Estimated reading time: 20 min_
> **Prerequisite:** [Chapter 17 — Input Validation Error Handling](../../../part-07-validation-and-business-errors/17-input-validation-error-handling/README.md)

## In one sentence

An upload is **untrusted input at a security boundary**: validate by content and size before
it reaches storage, and treat the storage provider as a remote dependency whose failures must
map to explicit, retryable-or-terminal outcomes.

## Why this matters in production

Users upload executables renamed to `.png`, zip bombs that expand to 100 GB, 8 GB "images" that
exhaust worker memory, and files with a `Content-Type` they chose themselves. Meanwhile the
storage provider returns `503 SlowDown`, expired credentials, or a `403` that actually means
"your signing key is wrong." Without a validation stage you serve malware and pay for it;
without a storage-error map you retry permanent failures forever or give up on transient ones.

## 43.1 — Upload validation at the trust boundary

Validate in this order — cheapest and most decisive first:

```text
1. Declared size        (reject before reading the body)
2. Declared content type (allowlist; a hint only)
3. Actual bytes         (magic-number sniffing)
4. Decodability         (can the parser open it without error? bounded work)
5. Policy               (virus scan state, tenant quota, filename safety)
```

| Check | Trust level | Failure code |
| ----- | ----------- | ------------ |
| `Content-Length` ≤ limit | Client-declared; enforce again while streaming | `UPLOAD_TOO_LARGE` (413) |
| Extension allowlist | Weak; users rename | `UPLOAD_TYPE_NOT_ALLOWED` (415) |
| `Content-Type` header | Weak; user-controlled | `UPLOAD_TYPE_NOT_ALLOWED` (415) |
| Magic bytes / signature | Strong for known formats | `UPLOAD_TYPE_MISMATCH` (415) |
| Parser can decode | Strong but expensive — bound it | `UPLOAD_MALFORMED` (422) |
| Filename safety | Prevent path traversal / header injection | `UPLOAD_INVALID_FILENAME` (400) |

```ts
// Validate on the stream, before writing a single byte to durable storage.
async function validateUpload(stream: Readable, declared: DeclaredFile) {
  if (declared.size > MAX_BYTES) throw new UploadTooLarge({ limit: MAX_BYTES }); // 413
  if (!ALLOWED_MIME.has(declared.mime)) throw new UploadTypeNotAllowed({ mime: declared.mime });

  const head = await readExactly(stream, 32);           // magic-number window
  const sniffed = sniffMime(head);                      // image/png, application/pdf, ...
  if (!sniffed || sniffed !== declared.mime) {
    throw new UploadTypeMismatch({ declared: declared.mime, sniffed });        // 415
  }
  if (!isSafeFilename(declared.name)) throw new UploadInvalidFilename({ name: declared.name });

  return { sniffed, head, rest: prepend(head, stream) }; // stream continues to storage
}
```

> ⚠️ **Hazard.** Never trust the extension or the browser-supplied MIME type for anything
> security-relevant. `.jpg` is a naming convention; the bytes decide.

**Key data:** choose limits deliberately — e.g. avatars 5 MB, documents 50 MB, video 2 GB.
Enforce the limit **while streaming**; `Content-Length` can lie or be absent with chunked
encoding. Reject `text/html`, `image/svg+xml` (scriptable), and executables unless you have a
specific, isolated use case. A decompression-bomb defense caps the *expanded* size, not just
the upload.

## 43.2 — Size and type

Size and type are not a single check; they are a matrix of limits per plan and per use case:

| Dimension | Typical limit | Where enforced |
| --------- | ------------- | -------------- |
| Request body | e.g. 100 MB | Reverse proxy / API gateway (413) |
| Object | Plan-dependent (e.g. 2 GB) | App validation + provider policy |
| Multipart part | 5 MB min (except last), 10,000 parts | Client + provider |
| Image dimensions | e.g. 12,000 × 12,000 px | Decoder, before full decode |
| Decompressed archive | e.g. 1 GB / 1,000 entries | Archive reader, streaming |
| Tenant storage quota | Plan-dependent | Quota service (see Ch. 42) |

Type enforcement has two layers with different jobs:

1. **Allowlist by sniffed type** — reject anything not explicitly supported. Deny-by-default.
2. **Processor compatibility** — a valid TIFF may not be supported by your image pipeline;
   that is a `422 UPLOAD_UNSUPPORTED_FORMAT`, distinct from a security rejection.

Separating "not allowed" (415) from "allowed but we cannot process it" (422) matters: the
first is user-correctable by choosing another file, the second often is not.

**Key data:** HTTP **413** for too large, **415** for unsupported media type, **422** for
structurally invalid/unsupported content. Return the actual limit in the error detail
(`maxBytes: 52428800`) so clients can pre-check and show a useful message.

## 43.3 — Storage provider failures

S3-compatible storage is a remote dependency. Map its failures explicitly:

| Failure | Typical cause | Class | Handling |
| ------- | ------------- | ----- | -------- |
| `503 SlowDown` | Request rate too high | Transient | Backoff + retry (same key / same part) |
| `500 InternalError` | Provider blip | Transient | Retry with backoff |
| `RequestTimeout` / socket reset | Network | Ambiguous | Retry same part (uploads are idempotent per part) |
| `403 AccessDenied` | Wrong bucket policy / key | Permanent config | Fail fast, alert; do not retry |
| `403 SignatureDoesNotMatch` | Clock skew, bad secret | Permanent config | Fail fast, fix credentials |
| `ExpiredToken` | Temporary credentials expired | Recoverable | Refresh credentials, retry once |
| `404 NoSuchBucket` | Misconfiguration | Permanent | Fail fast, alert |
| `412 PreconditionFailed` | Conditional write lost a race | Business outcome | Re-read and decide |

```ts
async function putWithRetry(key: string, body: Buffer) {
  return retry(
    () => s3.putObject({ Bucket: BUCKET, Key: key, Body: body,
                         ContentType: sniffMime(body), ChecksumSHA256: sha256b64(body) }),
    {
      attempts: 5,
      retryOn: (err) => ["SlowDown", "InternalError", "RequestTimeout", "ExpiredToken"]
        .includes(err.name),
      backoff: "exponential-jitter",
    },
  );
}
```

Two provider-specific habits worth adopting:

- **Send a checksum** (`ChecksumSHA256`) so silent corruption is detected at write time, not
  when a user opens the file.
- **Use conditional writes** (`If-None-Match: *`) when the object key is derived from content
  hash — a concurrent duplicate upload then becomes a `412`, not a race.

## Worked example — Acme's "profile picture" incident

Acme accepted avatars with `Content-Type: image/*` and stored them under the user's filename.
Two problems surfaced: (1) a user uploaded a 40 MB SVG with embedded script, which the app
served inline from the app's own domain — stored XSS; (2) a mobile client retried a failed
upload five times with `retry`, multiplying storage writes during an S3 `SlowDown` window.
Fixes: sniff magic bytes and allow only JPEG/PNG/WebP; re-encode every image server-side to
strip metadata and normalize format; serve from a separate origin via signed URL with
`Content-Disposition: attachment`; and map `SlowDown` to a bounded backoff with a jittered
cap. Storage writes dropped ~70% during the next provider blip, and the XSS class disappeared
because SVG was no longer accepted.

## Real-world use case — the storage outage that became 4,000 tickets

Acme's attachment upload sat directly on the provider's SDK. During a regional provider
incident every provider error surfaced as a `500 Internal Server Error` with the XML body
echoed to the customer, and the mobile client treated `500` as fatal — so a ten-second
provider blip produced ten *separate* uploads per user, each writing its own row in
`uploads`. Support received 4,000 tickets for 400 logical uploads.

The fix was a boundary translation, not a retry loop. The app now classifies the provider
error once and returns its own contract: `STORAGE_UNAVAILABLE` → `503` with
`Retry-After`, `STORAGE_TRANSIENT` → `502`, `STORAGE_QUOTA_EXCEEDED` → `429`,
`STORAGE_INVALID` → `422`. Provider bodies never leave the adapter. Upload attempts
carried an idempotency key derived from `(userId, clientUploadId)`, so a retry updated
the existing row instead of inserting a new one, and the response always returned the
`uploadId` so the client could **resume** rather than restart.

Attempts per logical upload fell from 10 to 1.2, and "upload failed" tickets dropped by
roughly 80%. The lesson: **a provider outage becomes an incident of your own the moment
you let its error shape through.**

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Validate in app memory | Simple | Memory pressure on big files | Small files only |
| Validate while streaming | Bounded memory | More code | ✅ Default |
| Re-encode all media | Strips payloads, normalizes | CPU cost, quality loss | Images/documents |
| Store original + scan | Keeps fidelity | Must gate serving | Video/archives |
| Provider policy only | No app code | No user-friendly errors | Never alone |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Sniff magic bytes and compare to the declared type | Trust extension or `Content-Type` |
| Enforce size limits while streaming | Buffer the whole body to check its size |
| Deny-by-default with an explicit allowlist | Blocklist "known bad" extensions |
| Distinguish 415 (type) from 422 (malformed) | Return 400 for everything |
| Retry `SlowDown`/`5xx` with backoff | Retry `AccessDenied` or `NoSuchBucket` |
| Send a content checksum on write | Assume storage writes are correct |

## Common mistakes

- **Extension-only validation** — a `.png` that is a PHP webshell.
- **Trusting `Content-Length`** — chunked uploads and lying clients bypass it.
- **Serving user content from the app origin** — stored XSS and cookie exposure.
- **Retrying permanent S3 errors** — retry storms on a misconfigured bucket.
- **Unbounded decode** — an image "header" that claims 60,000 × 60,000 pixels.

## Checklist

- [ ] Upload limit enforced while streaming, not just from `Content-Length`.
- [ ] Magic bytes checked against an allowlist.
- [ ] Decompressed size/entry count bounded for archives.
- [ ] Storage errors classified transient vs permanent vs config.
- [ ] Checksums sent on write.
- [ ] User content served from a separate origin, never inline from the app.

## Related

- [Interrupted Uploads and Multipart](./02-interrupted-uploads-and-multipart.md)
- [Chapter 17 — Input Validation Error Handling](../../../part-07-validation-and-business-errors/17-input-validation-error-handling/README.md)
- [Chapter 25 — Third-Party API Error Handling](../../../part-10-external-dependencies/25-third-party-api-error-handling/README.md)
- [Chapter 43 Reference](../05-reference/README.md)
