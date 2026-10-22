# Status Selection Walkthrough — Wire-Level Scenarios

> Part VIII · Chapter 19 · Sections 19.1–19.20 applied · _Estimated reading time: 20 min_
> **Prerequisite:** [Status Code Classes and Selection Table](../01-concepts/01-status-code-classes-and-selection-table.md)

## In one sentence

This file walks complete request/response pairs across the recurring cast — **`400` vs `422`,
`401` vs `403`, `404` vs `410`, `409`, `429` with `Retry-After`, and the 5xx family** — so the
selection drill becomes muscle memory.

## Why this matters in production

Reading rules is not the same as applying them under deadline. These scenarios are the ones
that actually appear in code review arguments: the expired token, the other tenant's ID, the
slug collision, the rate-limit burst, the dead provider. Each walkthrough shows the request,
the decision path, the exact response, and the client action the status enables — the loop
you want running automatically in your head.

## Core concept — the drill, applied

Every scenario below runs the same ordered questions from
[§19.1](../01-concepts/01-status-code-classes-and-selection-table.md):

```text
client-fixable? → credentials? → permission? → parseable? → semantic/state?
```

We show the decision path inline as `path:` lines. Trace them; they are the whole chapter in
one line each.

## Scenario 1 — `400` vs `422`: the Checkout form

**Bad JSON (encoder bug):**

```http
POST /api/v1/checkout HTTP/1.1
Content-Type: application/json
Authorization: Bearer <valid>

{"planId": "pro", "seats": 2,}
```

`path: parseable? NO → 400`

```http
HTTP/1.1 400 Bad Request
Content-Type: application/problem+json
X-Request-Id: req_s1

{
  "type": "/problems/malformed-request",
  "title": "Malformed Request",
  "status": 400,
  "code": "MALFORMED_JSON",
  "detail": "The request body is not valid JSON.",
  "instance": "/api/v1/checkout",
  "requestId": "req_s1"
}
```

Client action: **do not show field errors; log/fix the encoder.** No retry.

**Valid JSON, invalid domain value:**

```http
POST /api/v1/checkout HTTP/1.1
Content-Type: application/json
Authorization: Bearer <valid>

{"planId": "pro_monthly", "seats": -4, "paymentMethodId": "pm_1"}
```

`path: parseable? YES → schema? seats out of range → 422`

```http
HTTP/1.1 422 Unprocessable Content
Content-Type: application/problem+json
X-Request-Id: req_s2

{
  "type": "/problems/validation-error",
  "title": "Validation Failed",
  "status": 422,
  "code": "VALIDATION_FAILED",
  "detail": "One or more fields are invalid.",
  "instance": "/api/v1/checkout",
  "requestId": "req_s2",
  "errors": [
    { "field": "seats", "code": "out_of_range",
      "message": "seats must be between 1 and 500." }
  ]
}
```

Client action: **highlight `seats`, keep the form.** No retry.

## Scenario 2 — `401` vs `403`: AgentRun access

**Expired token (identity problem):**

```http
POST /api/v1/agent/runs HTTP/1.1
Authorization: Bearer <expired>

{"prompt": "Summarize sprint 12"}
```

`path: credentials valid? NO → 401`

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="acme", error="invalid_token"
Content-Type: application/problem+json
X-Request-Id: req_s3

{
  "type": "/problems/unauthenticated",
  "title": "Unauthenticated",
  "status": 401,
  "code": "TOKEN_EXPIRED",
  "detail": "The access token expired. Refresh and retry.",
  "requestId": "req_s3"
}
```

Client action: **refresh token, replay request once.**

**Valid token, insufficient role (permission problem):**

```http
POST /api/v1/agent/runs HTTP/1.1
Authorization: Bearer <valid, role: viewer>

{"prompt": "Summarize sprint 12"}
```

`path: credentials valid? YES → permission? NO → 403`

```http
HTTP/1.1 403 Forbidden
Content-Type: application/problem+json
X-Request-Id: req_s4

{
  "type": "/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "code": "INSUFFICIENT_ROLE",
  "detail": "Running agents requires the editor role.",
  "requestId": "req_s4"
}
```

Client action: **show "ask an admin for access"; do not refresh; do not retry.**

## Scenario 3 — `404` vs `410`: ExportJob results

**Never existed (or hidden from this tenant):**

```http
GET /api/v1/exports/exp_ghost HTTP/1.1
Authorization: Bearer <valid>
```

`path: credentials OK → permission OK → exists for principal? NO → 404`

```http
HTTP/1.1 404 Not Found
Content-Type: application/problem+json

{
  "type": "/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "code": "EXPORT_NOT_FOUND",
  "detail": "The requested export does not exist.",
  "requestId": "req_s5"
}
```

**Expired after the 7-day TTL (known, permanently gone):**

```http
GET /api/v1/exports/exp_9f2 HTTP/1.1
Authorization: Bearer <valid>
```

`path: existed and tombstoned? YES → 410`

```http
HTTP/1.1 410 Gone
Content-Type: application/problem+json

{
  "type": "/problems/gone",
  "title": "Gone",
  "status": 410,
  "code": "EXPORT_EXPIRED",
  "detail": "Export results expire after 7 days. Create a new export.",
  "requestId": "req_s6"
}
```

Client action: `404` → show not-found; `410` → **evict the cached ID, stop polling.**

## Scenario 4 — `409`: concurrent Checkout edit

```http
PATCH /api/v1/checkout/co_551 HTTP/1.1
Authorization: Bearer <valid>
If-Match: "7"
Content-Type: application/json

{"seats": 30}
```

Server state is version 9. `path: parseable OK → permission OK → state conflict? YES → 409`

```http
HTTP/1.1 409 Conflict
ETag: "9"
Content-Type: application/problem+json

{
  "type": "/problems/conflict",
  "title": "Conflict",
  "status": 409,
  "code": "VERSION_CONFLICT",
  "detail": "This checkout is now at version 9. Re-fetch and retry.",
  "instance": "/api/v1/checkout/co_551",
  "requestId": "req_s7",
  "currentVersion": 9
}
```

Client action: **GET fresh state, re-apply, PATCH with `If-Match: "9"`.** Never re-validate
the body — the fields were fine.

## Scenario 5 — `429` with `Retry-After`: the burst

```http
POST /api/v1/exports HTTP/1.1
Authorization: Bearer <key_live_42>

{"queryId": "q_17", "format": "csv"}
```

Sixth request in a 5/minute window. `path: under rate limit? NO → 429`

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 42
RateLimit-Limit: 5
RateLimit-Remaining: 0
RateLimit-Reset: 1772371320
Content-Type: application/problem+json

{
  "type": "/problems/rate-limited",
  "title": "Too Many Requests",
  "status": 429,
  "code": "RATE_LIMITED",
  "detail": "Export creation is limited to 5 per minute. Retry in 42 seconds.",
  "requestId": "req_s8",
  "retryAfterSeconds": 42
}
```

Client action: **sleep ≥ 42 s (plus jitter), replay with the same idempotency key.** SDKs that
honor `Retry-After` need no special casing; SDKs that guess cause herd spikes.

## Scenario 6 — the 5xx family: one request, honest outcomes

`POST /api/v1/checkout` with a valid body. Three different internal realities:

| Reality | Status | Body `code` | `Retry-After` | Who is paged |
| ------- | ------ | ----------- | ------------- | ------------ |
| Null invoice line throws (our bug) | `500` | `INTERNAL_ERROR` | — | Payments app on-call, immediately |
| Circuit open on Stripe | `503` | `PAYMENT_PROVIDER_UNAVAILABLE` | `10` | Integration on-call / incident |
| Stripe answers with garbage bytes | `502` | `UPSTREAM_INVALID_RESPONSE` | — | Integration on-call |
| Gateway 20 s deadline expires before app | `504` | (edge-generated) | — | Platform/edge on-call |

```http
HTTP/1.1 503 Service Unavailable
Retry-After: 10
Content-Type: application/problem+json

{
  "type": "/problems/service-unavailable",
  "title": "Service Unavailable",
  "status": 503,
  "code": "PAYMENT_PROVIDER_UNAVAILABLE",
  "detail": "The payment provider is temporarily unreachable. Retry in 10 seconds.",
  "requestId": "req_s9",
  "retryAfterSeconds": 10
}
```

Client action: `503` → retry after 10 s **with the same idempotency key**; `500` → show
"something went wrong," surface `requestId` for support, do not tight-loop.

## Key data / numbers

| Scenario | Status | Load-bearing header/field |
| -------- | ------ | ------------------------- |
| Broken JSON | `400` | — (single top-level problem) |
| Bad domain value | `422` | `errors[].field`, `errors[].code` |
| Expired token | `401` | `WWW-Authenticate` |
| Insufficient role | `403` | — |
| Unknown/hidden export | `404` | — |
| Expired export | `410` | — |
| Version clash | `409` | `ETag` of current state |
| Rate limited | `429` | `Retry-After: 42` |
| Dep outage | `503` | `Retry-After: 10` |
| Our bug | `500` | `requestId` correlates to trace |

## Real-world use case — Acme SaaS support playbook

Acme's support team previously needed five engineers' judgment to answer "what should this
response have been?" They adopted this walkthrough as the internal playbook: every escalated
ticket now includes the request, the registry code, and the expected status from this table.
Mean time to classify API tickets dropped from ~40 minutes to under 8 — most tickets became
"client ignored `410`" or "client retries `422`" one-liners, fixed in the client repo with a
link to this file's scenarios.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Replay `429`/`503` only after `Retry-After`, with idempotency keys | Tight-loop retry `429` |
| On `410`, evict and stop polling | Treat `410` like `404` and re-request forever |
| On `409`, re-fetch then re-apply | Re-send the identical stale write |
| Surface `requestId` on `500` for support | Show raw error text to end users |

## Common mistakes

- **Retrying `429` without jitter.** All clients resume at the same second; add ±20% jitter.
- **Refreshing tokens on `403`.** Wastes quota, loops, and masks the real permission fix.
- **Treating `410` as transient.** It is permanent by definition; polling it is a client bug.
- **Collapsing the 5xx family in the client.** A client that treats all `5xx` as
  equally-retryable will hammer a `500` bug. Branch on `code`/`status`.

## Checklist

- [ ] Your SDK/client handles each scenario's documented action.
- [ ] `Retry-After` is honored (seconds parsed; jitter added) for `429`/`503`.
- [ ] `401` triggers refresh; `403` never does.
- [ ] `409` triggers refetch-reapply, not blind retry.
- [ ] `410` removes the cached resource client-side.

## Related

- [The HTTP Status Selection Guide](../05-reference/README.md)
- [RFC 9110 and Consistent Selection](../02-deep-dive/01-rfc-9110-and-consistent-selection.md)
- [A Complete Middleware Chain (Ch. 21)](../../21-api-boundary-and-middleware-error-handling/03-practical-examples/01-a-complete-middleware-chain.md)
