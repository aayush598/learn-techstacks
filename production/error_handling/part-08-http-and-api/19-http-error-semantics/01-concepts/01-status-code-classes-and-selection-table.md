# Status Code Classes and What They Promise

> Part VIII · Chapter 19 · Section 19.1 · _Estimated reading time: 16 min_
> **Prerequisite:** [Chapter 19 README](../README.md)

## In one sentence

Every HTTP status code belongs to a **class that makes a promise to the client** — `2xx` "your
request worked," `4xx` "change the request and try again," `5xx` "we broke our promise" — and
choosing the class correctly is the first and most consequential error-handling decision at the
API boundary.

## Why this matters in production

Clients are machines before they are UIs. An SDK sees `503` and schedules a retry with backoff;
it sees `409` and surfaces a conflict dialog; it sees `404` and caches the negative result. If
you return `500` for what is really a validation failure (`422`), every compliant client
retries — against a bug that will never heal — turning one bad request into a retry storm. If
you return `200` with an error body (§19.17), monitoring, caching, and SDK error paths all go
blind. **The class is the contract; the body is the detail.**

## Core concept — the five classes (RFC 9110)

RFC 9110 defines the status-code taxonomy. The first digit is the contract:

```text
┌───────┬──────────────────────────┬─────────────────────────────────────────────┐
│ Class │ RFC 9110 meaning          │ What the client should do                    │
├───────┼──────────────────────────┼─────────────────────────────────────────────┤
│ 1xx   │ Informational            │ Wait; the request is in progress             │
│ 2xx   │ Success                  │ Request accepted/complete; parse the body    │
│ 3xx   │ Redirection              │ Follow (or stop); rarely used for errors     │
│ 4xx   │ Client error             │ The request is wrong; do NOT retry as-is     │
│ 5xx   │ Server error             │ Our fault; retry only if idempotent + policy  │
└───────┴──────────────────────────┴─────────────────────────────────────────────┘
```

- **`2xx`** — the action *succeeded*. A `202 Accepted` is still success: the contract changed
  from "done" to "accepted for processing," and the client should poll or wait on a result
  resource (Acme's `ExportJob` returns `202` + `Location`).
- **`3xx`** — rarely an error path. `304 Not Modified` is a caching optimization, not a
  failure.
- **`4xx`** — **the client can fix this by changing the request.** The server understood the
  request (or refused to understand it) and the fault is in authentication, permissions,
  syntax, semantics, state conflict, or limits. Retrying the identical request must fail
  identically. Exceptions where a retry may help: `408`, `429`, and occasionally `425`.
- **`5xx`** — **the server failed to perform a valid request.** The request itself is fine;
  we broke the promise. This includes our bugs (`500`), a broken upstream (`502`), deliberate
  unavailability (`503`), and upstream timeouts (`504`).

> ⚠️ **Hazard.** "It's an error, so it's a 500" is the most expensive default in API
> development. It converts every user mistake into a server-fault signal: alerts fire, retries
> amplify, and the client learns nothing actionable.

## The full status selection table for this chapter

This is the master table. Every scenario below is expanded in the files that follow; use this
as the index and the quick answer.

| Status | Name (RFC 9110) | Use when | Never use for | Required/expected headers |
| ------ | --------------- | -------- | ------------- | ------------------------- |
| `400` | Bad Request | The request **cannot be parsed**: malformed JSON, broken query syntax, invalid URL encoding, wrong header syntax | Semantic rule violations (use `422`); auth (`401`/`403`) | — |
| `401` | Unauthorized | The request lacks **valid credentials**: no token, expired token, bad signature, revoked key | Missing permissions for an authenticated principal (use `403`) | `WWW-Authenticate` (RFC 9110 requires it for `401`) |
| `403` | Forbidden | The principal is authenticated but **not allowed**: wrong role, other tenant's resource, suspended account, fail-closed policy | Absent/invalid credentials (use `401`); a nonexistent resource (see §19.5 on existence hiding) | — |
| `404` | Not Found | The resource **does not exist** for this principal, or the route itself is unknown and you choose not to disclose | A resource that exists but was deleted (use `410`); an existing resource the user may not see (decide `403`/`404` deliberately) | — |
| `405` | Method Not Allowed | The path exists but **this HTTP method is not supported** (`DELETE` on a read-only collection) | An unknown path (use `404`) | `Allow` (RFC 9110 requires it for `405`) |
| `409` | Conflict | The request is valid but **conflicts with the current state** of the resource: optimistic-lock mismatch, concurrent edit, duplicate with a different payload | Unique-constraint failures you model as `422` (pick one convention and keep it) | — |
| `410` | Gone | The resource **existed and is permanently removed**; clients should stop asking | Temporarily unavailable resources (use `503`); resources never known (use `404`) | — |
| `413` | Content Too Large | The request body/headers **exceed a configured limit** (upload cap, header cap) | A body that is merely invalid (use `400`/`422`) | — |
| `415` | Unsupported Media Type | The `Content-Type` is **not supported** for this route (`text/xml` to a JSON-only endpoint) | A supported media type carrying invalid data (use `400`/`422`) | `Accept-Post`/`Accept` hints are good practice |
| `422` | Unprocessable Content | The request is **syntactically valid but semantically invalid**: schema-valid input breaking a business rule, field-level validation failures, well-formed but wrong types downstream | Unparseable payloads (use `400`) | — |
| `429` | Too Many Requests | The client **exceeded a rate or quota limit** (per-key, per-IP, per-tenant) | Permanent quota exhaustion you model as billing (`402`) or entitlement (`403`) — pick deliberately | `Retry-After` (strongly expected); `RateLimit-*` headers common |
| `500` | Internal Server Error | An **unexpected condition** prevented us from fulfilling: uncaught exception, broken invariant, our bug | Expected business outcomes (use `4xx`); known dependency outages (use `503`) | — |
| `502` | Bad Gateway | An **upstream gateway/proxy received an invalid response** from the origin | Our own code failing (use `500`); our own timeout of an upstream (use `504`) | — |
| `503` | Service Unavailable | **Deliberate or detected unavailability**: overload, maintenance window, open circuit, dependency down | A single request's validation failure (use `4xx`); an unexpected bug (use `500`) | `Retry-After` (RFC 9110 allows it; strongly expected) |
| `504` | Gateway Timeout | An **upstream did not respond in time** to our gateway/proxy | An internal operation timing out inside our own service (use `500`, or `503` if it implies unavailability) | — |

## How it works — the selection mechanics

Selection is a **five-question drill**, asked in order. Stop at the first "yes":

```text
1. Could the CLIENT fix this by sending a different request?
      NO  → 5xx drill (500/502/503/504)  — our fault
      YES ↓
2. Are the CREDENTIALS missing or invalid?          → 401
3. Is the principal KNOWN but not ALLOWED?          → 403
4. Is the request UNPARSEABLE (syntax)?             → 400
      (body too large → 413; wrong content type → 415; wrong method → 405 + Allow)
5. Is it parseable but semantically INVALID or in CONFLICT with state?
      invalid per rules → 422   ·   conflict with current state → 409
      gone → 410   ·   rate limited → 429
```

The drill is deliberately ordered **auth before validation**. A caller with no valid token
should not learn which fields exist; returning `422` first would leak schema information to
unauthenticated callers (see §19.18 and Chapter 35).

## Worked example

Acme's `POST /api/v1/projects` accepts JSON. Each of these produces a different status:

```http
POST /api/v1/projects HTTP/1.1
Content-Type: application/json
Authorization: Bearer <expired-token>

{"name": "Apollo"}
```

→ `401 Unauthorized` + `WWW-Authenticate: Bearer error="invalid_token"` — credentials first.

```http
POST /api/v1/projects HTTP/1.1
Content-Type: application/json
Authorization: Bearer <valid-token>

{"name": "Apollo", "seats": -3}
```

→ `422 Unprocessable Content` — parseable, but `seats` violates a business rule.

```http
POST /api/v1/projects HTTP/1.1
Content-Type: application/json
Authorization: Bearer <valid-token>

{"name": "Apollo", "seats":
```

→ `400 Bad Request` — the JSON does not parse. The client's encoder is broken.

```http
POST /api/v1/projects HTTP/1.1
Content-Type: application/xml
Authorization: Bearer <valid-token>

<project><name>Apollo</name></project>
```

→ `415 Unsupported Media Type` — the route speaks JSON only.

## Key data / numbers

- **Class boundaries (RFC 9110):** `1xx` informational, `2xx` successful, `3xx` redirection,
  `4xx` client error, `5xx` server error.
- **Retry-eligible statuses in this chapter:** `429` and `503` (with `Retry-After`); `408` is
  defined for client request timeouts but rarely returned by API servers. Everything else in
  `4xx` is permanent for an identical retry.
- **Header-mandatory statuses:** `401` → `WWW-Authenticate`; `405` → `Allow`. Both are RFC 9110
  requirements, not conventions.
- **`422` RFC 9110 name:** "Unprocessable Content" (formerly "Unprocessable Entity").
  **`413` RFC 9110 name:** "Content Too Large" (formerly "Payload Too Large"). Older clients
  know the old reason phrases; the codes are what matter.

## Real-world use case — Acme SaaS

Acme's first API returned `500` for every failure: validation, auth, you name it. Consequences
measured over one quarter: on-call was paged for user typos (~40% of pages), and the mobile SDK
— which retries `5xx` with backoff — turned each invalid form into 4 attempts, quadrupling
load during a bad-release week. The fix was not a framework; it was adopting the selection
drill above and driving status codes from the error registry's `http` column. `5xx` volume
dropped by an order of magnitude, paging for client errors stopped entirely, and SDK retry
behavior became correct without a client release.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Registry-driven mapping (`code → http`) | Consistent, testable, auditable | Requires discipline adding codes | Default for any real API |
| Handler-local literals (`res.status(404)`) | Fast to write | Drift, 500-sprawl, untestable | Prototypes only |
| Coarse mapping (all validation → `400`) | Fewer decisions | Clients can't distinguish parse vs semantic failures | Never for public APIs |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Pick status from a documented table | Invent codes per handler |
| Keep `4xx` for anything the client can fix | Default to `500` "to be safe" |
| Attach `WWW-Authenticate` on `401`, `Allow` on `405` | Return bare status lines with required headers missing |
| Treat `429`/`503` as the only routine retry-eligible statuses | Let clients retry `400`/`422`/`404` |

## Common mistakes

- **`404` for everything unknown.** Method not supported is `405` + `Allow`; a deleted
  resource is `410`; a parse failure is `400`. `404` is only "not here."
- **`403` for missing tokens.** An absent token is `401` — `403` assumes an authenticated
  principal the server does not have.
- **`503` for bugs.** `503` promises "try later and it may work"; a `500`-class bug does not
  heal on a timer. Reserve `503` for genuine unavailability.
- **Mixing classes in one code.** One error code maps to exactly one status (registry column),
  never a "usually 404, sometimes 403" waffle.

## Checklist

- [ ] Every 4xx/5xx your API can return appears in the selection table above.
- [ ] Status codes come from the registry, not from handler literals.
- [ ] `401` responses carry `WWW-Authenticate`; `405` responses carry `Allow`.
- [ ] Team members can recite the five-question drill.
- [ ] No expected business outcome maps to `5xx`.

## Related

- [Request Content Errors: 400, 413, 415, 422](./02-request-content-errors-400-413-415-422.md)
- [RFC 9110 and Consistent Selection](../02-deep-dive/01-rfc-9110-and-consistent-selection.md)
- [The HTTP Status Selection Guide](../05-reference/README.md)
