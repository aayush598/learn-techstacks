# Error Shapes Across Scenarios

> Part VIII · Chapter 20 · Sections 20.1–20.20 applied · _Estimated reading time: 19 min_
> **Prerequisite:** [The Problem Details Envelope in Code](./01-problem-details-envelope-in-code.md)

## In one sentence

Every common scenario — `400`, `401`, `403`, `404`, `409`, `415`, `422` with fields,
`429` with `Retry-After`, `500`/`503` — plus **bulk** and **pagination** errors, all use the
**same envelope** with the correct `code`, headers, and extensions.

## Why this matters in production

This is the "golden set" for contract tests. If you can match every one of these JSON bodies
exactly (minus `requestId` values), your error surface is consistent. If your API produces
anything else, you know exactly what's missing. Copy this into your API docs as the public
error reference; generate it from the registry to keep it in sync.

## Core concept — the complete set

All examples use `Content-Type: application/problem+json`. `X-Request-Id` is echoed; `Retry-After`
appears on `429`/`503`.

### 1. `400 Bad Request` — malformed JSON

```http
HTTP/1.1 400 Bad Request
Content-Type: application/problem+json
X-Request-Id: req_e1

{
  "type": "/problems/malformed-request",
  "title": "Malformed Request",
  "status": 400,
  "detail": "The request body is not valid JSON.",
  "instance": "/api/v1/checkout",
  "code": "MALFORMED_JSON",
  "requestId": "req_e1"
}
```

### 2. `401 Unauthorized` — expired token

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="acme", error="invalid_token"
Content-Type: application/problem+json
X-Request-Id: req_e2

{
  "type": "/problems/unauthenticated",
  "title": "Unauthenticated",
  "status": 401,
  "detail": "The access token expired. Refresh and retry.",
  "instance": "/api/v1/agent/runs",
  "code": "TOKEN_EXPIRED",
  "requestId": "req_e2"
}
```

### 3. `403 Forbidden` — insufficient role

```http
HTTP/1.1 403 Forbidden
Content-Type: application/problem+json
X-Request-Id: req_e3

{
  "type": "/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Running agents requires the editor role.",
  "instance": "/api/v1/agent/runs",
  "code": "INSUFFICIENT_ROLE",
  "requestId": "req_e3"
}
```

### 4. `404 Not Found` — hidden/unknown resource

```http
HTTP/1.1 404 Not Found
Content-Type: application/problem+json
X-Request-Id: req_e4

{
  "type": "/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The requested project does not exist.",
  "instance": "/api/v/v1/projects/pr_ghost",
  "code": "PROJECT_NOT_FOUND",
  "requestId": "req_e4"
}
```

### 5. `409 Conflict` — version clash

```http
HTTP/1.1 409 Conflict
ETag: "9"
Content-Type: application/problem+json
X-Request-Id: req_e5

{
  "type": "/problems/conflict",
  "title": "Conflict",
  "status": 409,
  "detail": "This checkout is now at version 9. Re-fetch and retry.",
  "instance": "/api/v1/checkout/co_551",
  "code": "VERSION_CONFLICT",
  "requestId": "req_e5",
  "currentVersion": 9
}
```

### 6. `415 Unsupported Media Type`

```http
HTTP/1.1 415 Unsupported Media Type
Content-Type: application/problem+json
X-Request-Id: req_e6

{
  "type": "/problems/unsupported-media-type",
  "title": "Unsupported Media Type",
  "status": 415,
  "detail": "This endpoint supports only application/json.",
  "instance": "/api/v1/projects",
  "code": "UNSUPPORTED_MEDIA_TYPE",
  "requestId": "req_e6"
}
```

### 7. `422 Unprocessable Content` — field errors

```http
HTTP/1.1 422 Unprocessable Content
Content-Type: application/problem+json
X-Request-Id: req_e7

{
  "type": "/problems/validation-error",
  "title": "Validation Failed",
  "status": 422,
  "detail": "Two fields are invalid.",
  "instance": "/api/v1/projects",
  "code": "VALIDATION_FAILED",
  "requestId": "req_e7",
  "errors": [
    { "field": "name", "code": "required", "message": "name is required." },
    { "field": "owner.email", "code": "format_invalid",
      "message": "owner.email must be a valid email address." }
  ]
}
```

### 8. `429 Too Many Requests` — with `Retry-After`

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 42
Content-Type: application/problem+json
X-Request-Id: req_e8

{
  "type": "/problems/rate-limited",
  "title": "Too Many Requests",
  "status": 429,
  "detail": "Export creation is limited to 5 per minute. Retry in 42 seconds.",
  "instance": "/api/v1/exports",
  "code": "RATE_LIMITED",
  "requestId": "req_e8",
  "retryAfterSeconds": 42
}
```

### 9. `500 Internal Server Error` — generic, safe

```http
HTTP/1.1 500 Internal Server Error
Content-Type: application/problem+json
X-Request-Id: req_e9

{
  "type": "/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred. Provide the requestId to support.",
  "instance": "/api/v1/checkout",
  "code": "INTERNAL_ERROR",
  "requestId": "req_e9"
}
```

### 10. `503 Service Unavailable` — dependency down

```http
HTTP/1.1 503 Service Unavailable
Retry-After: 10
Content-Type: application/problem+json
X-Request-Id: req_e10

{
  "type": "/problems/service-unavailable",
  "title": "Service Unavailable",
  "status": 503,
  "detail": "The payment provider is temporarily unreachable. Retry in 10 seconds.",
  "instance": "/api/v1/checkout",
  "code": "PAYMENT_PROVIDER_UNAVAILABLE",
  "requestId": "req_e10",
  "retryAfterSeconds": 10
}
```

## Bulk and pagination examples

### 11. Bulk with partial success — `207 Multi-Status`

```http
HTTP/1.1 207 Multi-Status
Content-Type: application/problem+json
X-Request-Id: req_b1

{
  "type": "/problems/bulk-result",
  "title": "Bulk Operation Result",
  "status": 207,
  "detail": "3 succeeded, 2 failed.",
  "instance": "/api/v1/exports/bulk",
  "code": "BULK_PARTIAL_SUCCESS",
  "requestId": "req_b1",
  "summary": { "total": 5, "succeeded": 3, "failed": 2 },
  "results": [
    { "index": 0, "id": "exp_a", "status": "ok" },
    { "index": 1, "status": "error",
      "problem": {
        "code": "DASHBOARD_NOT_FOUND",
        "status": 404,
        "detail": "Dashboard db_77 no longer exists."
      }
    },
    { "index": 2, "id": "exp_c", "status": "ok" },
    { "index": 3, "id": "exp_d", "status": "ok" },
    { "index": 4, "status": "error",
      "problem": {
        "code": "DASHBOARD_NOT_FOUND",
        "status": 404,
        "detail": "Dashboard db_81 no longer exists."
      }
    }
  ]
}
```

### 12. Paginated list with partial data — `200 OK` with incompleteness signal

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Request-Id: req_p1

{
  "data": [
    { "id": "pr_1", "name": "Apollo" },
    { "id": "pr_2", "name": "Orion" }
  ],
  "pagination": { "cursor": "c_2b",
                   "hasMore": true },
  "partial": true,
  "incompleteReason": "one_or_more_rows_unavailable"
}
```

Note: this is a **success response** (the page request succeeded) — the incompleteness is a
data signal on a success body, not a problem document. Only in rare cases would a page
failure be a problem document (e.g. DB down → `503`). Keep success and error envelopes
distinct (they're different *shapes* by design here).

### 13. Invalid cursor — problem document

```http
HTTP/1.1 400 Bad Request
Content-Type: application/problem+json
X-Request-Id: req_p2

{
  "type": "/problems/invalid-cursor",
  "title": "Invalid Cursor",
  "status": 400,
  "detail": "The pagination cursor is invalid or has expired. Restart from the first page.",
  "instance": "/api/v1/projects",
  "code": "INVALID_CURSOR",
  "requestId": "req_p2"
}
```

## Key data / numbers

| Scenario | Status | Required extensions | Headers |
| -------- | ------ | ------------------- | ------- |
| Malformed JSON | `400` | `code` | — |
| Expired token | `401` | `code` | `WWW-Authenticate` |
| Insufficient role | `403` | `code` | — |
| Not found/hidden | `404` | `code` | — |
| Version conflict | `409` | `code`, `currentVersion` | `ETag` (if used) |
| Unsupported media type | `415` | `code` | — |
| Validation | `422` | `code`, `errors[]` | — |
| Rate limited | `429` | `code`, `retryAfterSeconds` | `Retry-After` |
| Internal error | `500` | `code` (generic) | — |
| Dep unavailable | `503` | `code`, `retryAfterSeconds` | `Retry-After` |
| Bulk partial | `207`/`200` | `summary`, `results[]` | — |
| Invalid cursor | `400` | `code` | — |

## Real-world use case — Acme SaaS

Acme's public API docs previously showed three different "error" sections; developers
consistently opened tickets asking which shape to expect. Replacing them with this golden
set — and generating it from the contract tests — cut API-onboarding questions by over half.
More importantly, every example here passed the CI denylist (no stacks, no SQL, no internal
hosts) and every one used the documented extensions. When a new endpoint shipped, its errors
just worked with the existing SDKs because nothing new had to be learned.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use these shapes verbatim for their scenarios | Deviate by adding extra top-level keys ad hoc |
| Mirror status into the body and headers consistently | Return HTML for API error paths |
| Keep 500 generic; log details with `requestId` | Dump traces into `detail` |
| Signal pagination incompleteness explicitly | Silently truncate lists |
| Use per-item problems for bulk failures | Fail the whole batch on one bad item (unless transactional) |

## Checklist

- [ ] All 13 scenarios exist as contract-test fixtures.
- [ ] Every problem body uses `application/problem+json`.
- [ ] `Retry-After` header + `retryAfterSeconds` body match for `429`/`503`.
- [ ] `errors[]` capped and field paths are request-shape paths.
- [ ] Pagination success vs error are clearly distinguished in docs.

## Related

- [The Error Envelope Spec](../05-reference/README.md)
- [The Problem Details Envelope in Code](./01-problem-details-envelope-in-code.md)
- [A Complete Middleware Chain (Ch. 21)](../../21-api-boundary-and-middleware-error-handling/03-practical-examples/01-a-complete-middleware-chain.md)
