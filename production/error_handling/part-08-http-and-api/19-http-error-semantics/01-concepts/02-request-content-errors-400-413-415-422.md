# Request Content Errors — 400, 413, 415, 422

> Part VIII · Chapter 19 · Sections 19.2, 19.9, 19.10, 19.11 · _Estimated reading time: 18 min_
> **Prerequisite:** [Status Code Classes and Selection Table](./01-status-code-classes-and-selection-table.md)

## In one sentence

`400` means the request **cannot be parsed**, `415` means the media type is **not supported**,
`413` means the payload is **too large**, and `422` means the request parsed fine but is
**semantically invalid** — the syntax/semantics line between `400` and `422` is the single most
misunderstood boundary in HTTP APIs.

## Why this matters in production

Clients behave differently depending on which of these four they receive. A `400` tells a
client "your encoder is broken — inspect how you build requests." A `422` tells it "your data
is wrong — show field errors to the user." A `413` tells it "chunk or compress the upload." A
`415` tells it "negotiate a different content type." Collapse them all into `400` (a very
common shortcut) and every client must string-match on error bodies to recover — the exact
anti-pattern RFC 9457 exists to eliminate. Get the distinction right and **the status code
alone drives the correct recovery path**.

## Core concept — the syntax/semantics split

RFC 9110 frames `400 Bad Request` around a request the server **cannot process because of its
syntax**. `422 Unprocessable Content` (RFC 9110; formerly "Unprocessable Entity," popularized
by WebDAV) covers content that is **syntactically correct and semantically wrong**.

```text
            ┌──────────────────── HTTP request body ────────────────────┐
            │                                                            │
   bytes ──▶│  Can the parser produce a structure?                       │
            │     NO  ──────────────▶  400 Bad Request                    │
            │     YES                                                      │
            │       └▶ Does Content-Type match a supported type?          │
            │            NO  ─────────▶  415 Unsupported Media Type       │
            │            YES                                               │
            │              └▶ Within size limit?  NO ─▶ 413 Content Too Large
            │                 YES                                           │
            │                   └▶ Do values satisfy schema + rules?       │
            │                        NO ──────────────▶  422 Unprocessable │
            │                        YES ──▶ proceed to handler           │
            └──────────────────────────────────────────────────────────────┘
```

Key consequences:

- **Both `400` and `422` are permanent.** Retrying the identical request fails identically.
  Neither is retry-eligible.
- **`422` owns field-level detail.** Validation errors are the canonical `422` payload:
  per-field codes, messages, and paths (see Ch. 20 for the envelope).
- **`400` should stay thin.** When JSON fails to parse you usually cannot know *which* field
  is wrong — the structure does not exist. Return a single top-level problem, not invented
  field errors.
- **Ordering matters:** check `415` and `413` at the middleware layer *before* attempting to
  parse, and parse (`400`) *before* semantic validation (`422`). Chapter 21 maps these to
  middleware positions.

## How it works — classifying each failure

| Failure | Status | Why |
| ------- | ------ | --- |
| Body is not valid JSON (`{"name": }`) | `400` | Parser cannot produce a structure |
| Query string is malformed (`?cursor=%zz`) | `400` | Syntax cannot be decoded |
| JSON parses, `seats: "many"` where integer required | `422` | Structure exists; type/semantics fail (some teams use `400` for type mismatches inside schema — pick one; we recommend `422`) |
| JSON parses, `seats: -3` | `422` | Business-rule violation |
| JSON parses, email already registered | `409` or `422` | Conflict-with-existing-state (`409`) vs field invalidity (`422`); adopt one convention per API |
| Body is 200 MB, limit is 10 MB | `413` | Size limit, checked before parse |
| `Content-Type: text/xml` to a JSON route | `415` | Unsupported media type |
| Chunked body with invalid chunk framing | `400` | Transport-level syntax failure |

> ⚠️ **Hazard.** Some frameworks surface parse failures as `500` because the JSON library
> *throws*. If your error middleware does not classify parser exceptions, every malformed body
> pages on-call as a server error. Classify them explicitly (Chapter 21, §21.2).

## Worked example — Checkout payload vs validation

`Checkout` accepts `POST /api/v1/checkout`. Three requests, three different statuses:

```http
POST /api/v1/checkout HTTP/1.1
Content-Type: application/json
Authorization: Bearer <valid>

{"planId": "pro_monthly", "paymentMethodId": "pm_123",
```

```http
HTTP/1.1 400 Bad Request
Content-Type: application/problem+json

{
  "type": "/problems/malformed-request",
  "title": "Malformed Request",
  "status": 400,
  "detail": "The request body is not valid JSON.",
  "instance": "/api/v1/checkout",
  "code": "MALFORMED_JSON",
  "requestId": "req_7c1a9f2e"
}
```

```http
POST /api/v1/checkout HTTP/1.1
Content-Type: application/json
Authorization: Bearer <valid>

{"planId": "pro_monthly", "paymentMethodId": "pm_123", "seats": 0}
```

```http
HTTP/1.1 422 Unprocessable Content
Content-Type: application/problem+json

{
  "type": "/problems/validation-error",
  "title": "Validation Failed",
  "status": 422,
  "detail": "One or more fields are invalid.",
  "instance": "/api/v1/checkout",
  "code": "VALIDATION_FAILED",
  "requestId": "req_9b44c0d1",
  "errors": [
    { "field": "seats", "code": "out_of_range",
      "message": "seats must be between 1 and 500." }
  ]
}
```

```http
POST /api/v1/checkout HTTP/1.1
Content-Type: application/xml
Authorization: Bearer <valid>

<checkout><planId>pro_monthly</planId></checkout>
```

→ `415 Unsupported Media Type` with an `Accept: application/json` hint. The body may never be
parsed; the media type check happens first.

## Key data / numbers

- **`400` RFC 9110 name:** Bad Request. **`413`:** Content Too Large. **`415`:** Unsupported
  Media Type. **`422`:** Unprocessable Content.
- **`422` origin:** RFC 4918 (WebDAV); retained in RFC 9110. **`413`/`415`** also carried
  into RFC 9110 with updated reason phrases.
- **All four are permanent for identical retries** — never map them to a retryable class in
  the registry.
- **Size limits are configuration, not protocol:** pick explicit limits (e.g. 1 MB JSON, 25 MB
  upload) and return `413` with the limit documented. Common practice is a top-level
  `maxBytes` member in the problem body.
- **Field-error budget:** cap the number of returned field errors (e.g. first 20) to keep
  responses bounded under hostile input.

## Real-world use case — Acme SaaS uploads

Acme's `POST /api/v1/projects/{id}/attachments` accepted files up to 25 MB. The upload
middleware parsed multipart *before* checking size, so a 2 GB body was streamed into memory,
spiking the pod, and the resulting OOM surfaced as `500` — three failures in one (no `413`,
resource exhaustion, wrong class). Fix: enforce `413` at the very front of the chain from
`Content-Length` and a streaming counter, reject `415` for non-whitelisted media types next,
and only then parse. `500`s from uploads vanished; the mobile client got a clean "file too
large" path keyed on `413` alone.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Strict `400` parse / `422` semantic split | Machine-actionable; SDKs branch cleanly | Slightly more mapping code | Default; recommended |
| Everything malformed → `400` | Simple | Clients can't show field errors without string matching | Internal APIs only |
| Type mismatches → `400` | Matches some validators' defaults | Blurs the line; inconsistent with rule violations | Only if documented and consistent |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return `422` with per-field `errors[]` for validation | Return `400` for business-rule violations |
| Return a single top-level problem for `400` parse failures | Fabricate field errors from an unparseable body |
| Check `413`/`415` before parsing | Parse first and let the size blow up the process |
| Classify JSON-parser exceptions as `400` in middleware | Let parser exceptions become `500` |

## Common mistakes

- **`400` for everything invalid.** Clients lose the parse-vs-validate distinction; support
  loses the ability to tell broken encoders from bad data.
- **`422` with no `errors[]`.** A `422` that does not localize the failure forces the client
  to re-validate on its own — you shipped the work back to them.
- **`500` from the parser.** Uncaught `SyntaxError` → catch-all → `500`. Classify explicitly.
- **Revealing parser internals in `400`.** `detail: "Unexpected token } at position 47"` is
  tolerable for your own API; keep it generic (`"The request body is not valid JSON."`) for
  public consumers, and never echo the raw body.

## Checklist

- [ ] Parse failures produce `400`, never `500`.
- [ ] Every `422` includes machine-readable field details.
- [ ] `413` is enforced before the body is buffered.
- [ ] `415` is checked before parsing and names the supported types.
- [ ] The registry maps `MALFORMED_JSON→400`, `VALIDATION_FAILED→422`, `PAYLOAD_TOO_LARGE→413`,
      `UNSUPPORTED_MEDIA_TYPE→415` — no handler-local deviations.

## Related

- [Access Errors: 401, 403, 404, 405](./03-access-errors-401-403-404-405.md)
- [RFC 9110 and Consistent Selection](../02-deep-dive/01-rfc-9110-and-consistent-selection.md)
- [Parsing and Malformed Requests (Ch. 21)](../../21-api-boundary-and-middleware-error-handling/01-concepts/02-parsing-and-malformed-requests.md)
