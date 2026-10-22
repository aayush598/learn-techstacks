# State and Limit Errors — 409, 410, 429

> Part VIII · Chapter 19 · Sections 19.7, 19.8, 19.12 · _Estimated reading time: 17 min_
> **Prerequisite:** [Access Errors: 401, 403, 404, 405](./03-access-errors-401-403-404-405.md)

## In one sentence

`409` says "valid request, wrong current state," `410` says "this is permanently gone," and
`429` says "slow down" — the only status in this set that carries an explicit **retry
instruction** via `Retry-After`.

## Why this matters in production

These three statuses sit on paths where business meaning is dense: concurrent edits, deleted
resources, and quota enforcement. Misclassifying them has measurable downstream effects. A
`409` returned as `422` tells clients "fix your fields" when the fields are fine — the state
moved underneath them, and the correct client behavior is to re-fetch and re-apply, not to
re-validate. A `410` returned as `404` keeps clients and crawlers polling a tombstone forever.
A `429` without `Retry-After` turns a well-behaved client into a blind retry loop — exactly
the amplification that turns a small overload into an outage (Chapter 57).

## Core concept — three distinct meanings

### `409 Conflict` — the world changed under you

`409` is for requests that are **well-formed and well-formed-authorized, but inconsistent with
the current state of the target resource**. Canonical cases:

- **Optimistic concurrency:** `If-Match`/version mismatch on `PATCH /projects/{id}` — the
  resource was modified since the client's `ETag`.
- **Concurrent lifecycle actions:** cancelling a `Checkout` that has already captured payment.
- **Duplicate with different payload:** same idempotency key, different body (Chapter 28).
- **Uniqueness conflicts** you model as state conflicts: `POST /projects` with an existing
  slug. (Teams also model uniqueness as `422`; whichever you choose, apply it uniformly.)

`409` tells the client: *re-read the resource, then decide.* It is permanent for the
identical request but resolvable by a new request against fresh state.

### `410 Gone` — stronger than `404`

`410` means the resource **existed and has been deliberately, permanently removed**. The
client should evict its copy and stop asking. Acme's `ExportJob` result objects expire after
7 days: after that, `GET /api/v1/exports/{id}` returns `410`, not `404` — the difference
between "you guessed an ID" and "you had this and it is over."

### `429 Too Many Requests` — the retry-eligible 4xx

`429` means the client **exceeded a rate or quota**. It is the one client-error class where
retrying is the expected recovery — but only after the advertised delay:

- `Retry-After: 30` (delta-seconds) or an HTTP-date — RFC 9110 formats, both valid.
- Optionally paired with `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset` (the
  IETF `RateLimit` header fields, commonly seen in the `X-RateLimit-*` variant).

⚠️ **Hazard.** `429` must be **per-identity** wherever possible (API key, token, tenant,
falling back to IP). A global `429` lets one noisy tenant lock out everyone — a self-inflicted
denial of service.

## How it works — the mechanics

```text
PATCH /projects/pr_1  If-Match: "v3"
  │
  ├─ current version is v3 ──▶ apply, return 200 + new ETag "v4"
  └─ current version is v5 ──▶ 409 Conflict
                               detail: "The project was modified by someone else."
                               errors?: [{ code: "version_conflict", currentVersion: 5 }]
                               (client re-GETs, re-applies, retries with v5's ETag)

POST /exports  (per-tenant budget: 10/min)
  │
  ├─ under budget ──▶ 202 Accepted + Location: /exports/{id}
  └─ over budget ──▶ 429 + Retry-After: 12
                     (client sleeps 12s; SDK schedules automatic retry)

GET /exports/exp_9f2  (created 2026-03-01, now 2026-03-20, TTL 7 days)
  │
  ├─ exists ──▶ 200
  └─ expired ─▶ 410 Gone  (client deletes local reference)
```

Retry semantics by status:

| Status | Retry the identical request? | Correct client behavior |
| ------ | ---------------------------- | ----------------------- |
| `409` | No | Re-fetch state, re-decide, possibly new request |
| `410` | No | Evict; never poll again |
| `429` | Yes, after `Retry-After` | Sleep or schedule; add jitter (Chapter 27) |

## Worked example — Checkout concurrency

Two tabs edit the same subscription. Tab A saves first; Tab B's stale write:

```http
PATCH /api/v1/checkout/co_551 HTTP/1.1
Authorization: Bearer <valid>
If-Match: "7"
Content-Type: application/json

{"seats": 25}
```

```http
HTTP/1.1 409 Conflict
ETag: "9"
Content-Type: application/problem+json

{
  "type": "/problems/conflict",
  "title": "Conflict",
  "status": 409,
  "code": "VERSION_CONFLICT",
  "detail": "This checkout was modified (now version 9). Re-fetch and retry.",
  "instance": "/api/v1/checkout/co_551",
  "requestId": "req_c7",
  "currentVersion": 9
}
```

And the quota path on the same flow:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 30
RateLimit-Limit: 100
RateLimit-Remaining: 0
RateLimit-Reset: 1772371200
Content-Type: application/problem+json

{
  "type": "/problems/rate-limited",
  "title": "Too Many Requests",
  "status": 429,
  "code": "RATE_LIMITED",
  "detail": "Request limit exceeded. Retry after 30 seconds.",
  "requestId": "req_c8"
}
```

## Key data / numbers

- **`409` RFC 9110 name:** Conflict. **`410`:** Gone. **`429`:** Too Many Requests (defined
  in RFC 6585, carried into RFC 9110).
- **`Retry-After` formats:** delta-seconds (`Retry-After: 30`) or HTTP-date
  (`Retry-After: Wed, 21 Oct 2026 07:28:00 GMT`). Delta-seconds is simpler for clients; use it
  unless you have a reason not to.
- **`429` is permanent for the identical immediate retry** but **retry-eligible after the
  delay** — the registry should mark `RATE_LIMITED` retryable with a delay hint.
- **`410` vs `404` retention:** keep tombstones at least as long as clients could hold
  references (Acme: 7 days for exports; tombstone retained 30 days).
- **ETag/`If-Match` flow:** `412 Precondition Failed` is the alternative for `If-Match`
  failures; many APIs prefer `409` because it reads as a state conflict. Choose one and
  document it — both are defensible under RFC 9110.

## Real-world use case — Acme SaaS ExportJob

`ExportJob` results were served from S3 with a 7-day lifecycle rule. The mobile client cached
export IDs and polled them on app open. After expiry the API returned `404`, so the client
treated every expired export as a bug, retried with backoff, and filed telemetry events that
drowned the real error stream. Two fixes: `410` for expired-but-known exports (with the
tombstone retained 30 days), and a `DELETE`-free client contract — on `410`, drop the cached
ID and stop polling. Poll volume fell ~70% for users with large historical lists, and the
telemetry signal became trustworthy again.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Uniqueness → `409` | Signals "re-read and retry" | Clients may over-retry | Slug/name collisions, stateful duplicates |
| Uniqueness → `422` | Frames it as a field problem | Misses the "state changed" nuance | Pure field constraints (email taken) — still common |
| `If-Match` → `409` | Natural conflict reading | Slightly less precise vs `412` | Recommended default |
| `If-Match` → `412` | RFC-classic | Confusing to some client authors | Fine if documented |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return `409` when concurrent state invalidates an otherwise-valid request | Return `422` for version conflicts |
| Return `410` for known-permanent removals | Return `404` for expired resources clients once held |
| Attach `Retry-After` to every `429` | Return bare `429` and hope the client guesses |
| Rate-limit per identity | Apply one global limit that one tenant can exhaust |

## Common mistakes

- **`429` without `Retry-After`.** Clients back off with their own guesses; the thundering
  herd you feared arrives anyway.
- **`409` with no hint about current state.** Include enough context (current version, who
  touched it if safe) for the client to act, without leaking PII.
- **`410` for anything "old."** Age is not removal. Old-but-present resources serve `200`;
  only deliberate deletion earns `410`.
- **Limiting on unauthenticated IP alone for keyed APIs.** Attackers rotate IPs; key-based
  limits are the primary axis, IP is the fallback for the unauthenticated surface.

## Checklist

- [ ] Every `429` carries `Retry-After`.
- [ ] Rate limits are scoped per tenant/key before any global fallback.
- [ ] `410` is used only with a retained tombstone.
- [ ] Optimistic-concurrency failures are one status (`409` or `412`), uniformly.
- [ ] Registry marks `429` retryable-with-delay; all other 4xx non-retryable.

## Related

- [Server Errors: 500, 502, 503, 504](./05-server-errors-500-502-503-504.md)
- [Glossary](../../../GLOSSARY.md)
- [The HTTP Status Selection Guide](../05-reference/README.md)
