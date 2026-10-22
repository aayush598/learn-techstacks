# Chapter 19 — Reference

> Part VIII · Chapter 19 · Cheat sheets, decision tree, and glossary.

## Cheat sheet — the five-question drill

```text
1. Client-fixable?  NO ──▶ 5xx drill: bug→500 · bad upstream→502 · known-down→503 · upstream timeout→504
2. Credentials missing/invalid?        YES ──▶ 401 + WWW-Authenticate
3. Principal known but not allowed?    YES ──▶ 403   (or 404 if hiding by policy)
4. Unparseable syntax?                 YES ──▶ 400   (too large→413 · wrong type→415 · wrong method→405+Allow)
5. Semantic/state problem?   invalid→422 · conflict→409 · gone→410 · rate→429+Retry-After
```

## HTTP status selection guide (full table)

| Status | One-line trigger | Required/expected headers | Retry class |
| ------ | ---------------- | ------------------------- | ----------- |
| `400` | Cannot parse the request syntax | — | Permanent |
| `401` | No/invalid/expired credentials | `WWW-Authenticate` | Permanent (refresh, don't replay) |
| `403` | Authenticated, not permitted | — | Permanent |
| `404` | Not present (or hidden) for this principal | — | Permanent (negative-cache OK) |
| `405` | Path exists, method unsupported | `Allow` | Permanent |
| `409` | Conflicts with current resource state | `ETag` (if ETag-based) | Re-fetch then new request |
| `410` | Permanently removed; stop asking | — | Terminal — evict |
| `413` | Body/headers exceed limit | — | Permanent (smaller request) |
| `415` | Content-Type unsupported | `Accept`/`Accept-Post` hints | Permanent (renegotiate) |
| `422` | Parseable but semantically invalid | `errors[]` (recommended) | Permanent (fix fields) |
| `429` | Rate/quota exceeded | `Retry-After` | Retry after delay (+jitter) |
| `500` | Unexpected server condition (bug) | `requestId` | Do not hot-retry |
| `502` | Gateway received invalid upstream response | — | Edge-level retryable |
| `503` | Temporarily unavailable (overload/maintenance/breaker) | `Retry-After` | Retry after delay, idempotent |
| `504` | Gateway did not get upstream response in time | — | Edge-level retryable |

## Decision tree — the historically ambiguous pairs

| Question | Yes | No |
| -------- | --- | -- |
| Is the body unparseable? | `400` | ↓ |
| Is Content-Type unsupported? | `415` | ↓ |
| Is the body over the size limit? | `413` | ↓ |
| Are credentials missing/invalid? | `401` | ↓ |
| Is the principal authenticated-but-forbidden? | `403` (or `404` by hiding policy) | ↓ |
| Is the path unroutable? | `404` | ↓ |
| Is the method unsupported on this path? | `405` + `Allow` | ↓ |
| Does it violate a field/business rule? | `422` | ↓ |
| Does it conflict with current state? | `409` | ↓ |
| Is it a known-permanent removal? | `410` | ↓ |
| Is it a rate/quota limit? | `429` + `Retry-After` | ↓ |
| Did we hit an unexpected condition? | `500` | ↓ |
| Is a dependency knowingly down? | `503` + `Retry-After` | proceed / investigate |

## Cheat sheet — registry mapping skeleton

```ts
// One code → one status → one retry class. Handlers never pick statuses.
const HTTP = {
  MALFORMED_JSON: 400, TOKEN_EXPIRED: 401, INSUFFICIENT_ROLE: 403,
  PROJECT_NOT_FOUND: 404, METHOD_NOT_ALLOWED: 405, VERSION_CONFLICT: 409,
  EXPORT_EXPIRED: 410, PAYLOAD_TOO_LARGE: 413, UNSUPPORTED_MEDIA_TYPE: 415,
  VALIDATION_FAILED: 422, RATE_LIMITED: 429, INTERNAL_ERROR: 500,
  UPSTREAM_INVALID_RESPONSE: 502, SERVICE_UNAVAILABLE: 503,
} as const;
```

## Cheat sheet — retry classification

| Class | Statuses | Client behavior |
| ----- | -------- | --------------- |
| Permanent | `400`, `401`, `403`, `404`, `405`, `409*`, `410`, `413`, `415`, `422` | Do not replay identically; `409` → refetch; `401` → refresh |
| Retry-after-delay | `429`, `503` | Sleep `Retry-After` + jitter; idempotent replay |
| Edge-retryable | `502`, `504` | Retry per SDK policy; these are usually edge-generated |
| Report | `500` | Surface to user/support; no hot retry (amplifies bugs) |

\* `409` is "permanent for the identical stale request" but resolvable via re-fetch.

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Status class | First digit of the code; the generic contract (2xx success, 4xx client, 5xx server) |
| Syntax failure | Request cannot be parsed → `400` |
| Semantic failure | Parses fine, violates rules → `422` |
| Existence hiding | Returning `404` (not `403`) to avoid confirming a resource exists |
| `Retry-After` | Header advertising safe retry delay (delta-seconds or HTTP-date) |
| Retry class | Registry-derived property: permanent / retry-after-delay / report |
| Misleading response | Status, detail, or headers that contradict the actual outcome |
| Internal exposure | Stack/SQL/topology details leaking into client-visible responses |

## Signposts

- Full wire-level scenarios → [Status Selection Walkthrough](../03-practical-examples/01-status-selection-walkthrough.md)
- Envelope/body design → [Chapter 20](../../20-standardized-api-error-responses/README.md)
- Where selection is enforced in code → [Chapter 21](../../21-api-boundary-and-middleware-error-handling/README.md)

## Related

- [Chapter 19 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Part VIII Index](../../README.md)
