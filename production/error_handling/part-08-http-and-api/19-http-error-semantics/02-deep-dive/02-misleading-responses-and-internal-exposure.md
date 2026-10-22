# Misleading Responses and Internal Exposure

> Part VIII · Chapter 19 · Sections 19.17, 19.18, 19.20 · _Estimated reading time: 18 min_
> **Prerequisite:** [RFC 9110 and Consistent Selection](./01-rfc-9110-and-consistent-selection.md)

## In one sentence

Two failure modes corrupt the API contract from opposite directions — **lying about failure**
(`200` for an error, wrong class) and **telling the truth about the wrong thing** (stack
traces, SQL, internal IDs leaking through `4xx`) — and production APIs must design explicitly
against both.

## Why this matters in production

A `200` that hides a failure is invisible to every automated defender: uptime monitors see
green, SDK error handlers never fire, caches store the error as success, and the first
noticeable symptom is corrupted client state — a checkout that "succeeded" without charging,
an export list showing jobs that never ran. At the other extreme, an over-detailed `400`
hands attackers a free reconnaissance tool: schema names, framework versions, internal
resource IDs, tenant boundaries. Both problems feel like conveniences in the moment
("clients find 200 easier"; "detail helps debugging") and both are liabilities in production.

## Core concept — the two directions of contract corruption

```text
        HONEST CONTRACT
        status = truth about the class of outcome
        body   = safe, actionable detail
              ▲
              │ corruption points
     ┌────────┴─────────┐        ┌──────────────────┐
     │ DOWNPLAYING      │        │ OVER-DISCLOSING  │
     │ failure          │        │ internals        │
     ├──────────────────┤        ├──────────────────┤
     │ 200 + error body │        │ stack traces     │
     │ 201 for failed   │        │ SQL / ORM errors │
     │   creation       │        │ hostnames, IPs   │
     │ 302 redirect to  │        │ internal IDs,    │
     │   error page     │        │   tenant IDs     │
     │ wrong 4xx class  │        │ file paths       │
     │  (§19.20)        │        │ dependency names │
     └──────────────────┘        └──────────────────┘
```

### 19.17 — when not to return `200` for failures

`2xx` means the action succeeded. Returning `200` (or `201`) for a failure breaks clients at
the protocol level: proxies may cache it, monitors won't page, and SDKs skip error handling.
The exceptions are narrow and must be **documented protocol features**, not habits:

| Situation | Verdict | Why |
| --------- | ------- | --- |
| Regular error for a create/update | ❌ Use the 4xx/5xx that fits | The operation failed; say so |
| Bulk endpoint with per-item outcomes | ⚠️ `200`/`207` with per-item statuses is legitimate | Document the per-item status field as the real contract |
| "Operation result" polling endpoint (`GET /operations/{id}`) | ✅ `200` + status field | The *lookup* succeeded; the operation's outcome is domain data (`status: "failed"`) — model it explicitly (Chapter 39) |
| Business outcome that is not a failure (`EXPORT_EMPTY`) | ✅ `200` | An empty export is a successful export — model as outcome code, not error |
| Deliberate webhook fast-ack to stop sender retries on poison events | ⚠️ debatable; often `200` after DLQ | Document; ensure the failure was durably recorded first |

The bright line: **if the client's SDK should enter an error path, the status must be an
error status.** If the outcome is *domain state* the client will render (empty list, failed
operation record), `200` with an explicit state field is honest — as long as that state is
part of the documented success schema.

### 19.18 — what `4xx` must never expose

`4xx` bodies are attacker-visible and client-visible at the same time. Never include:

- **Stack traces, exception class names, file paths** — reveals framework, versions, layout.
- **SQL text, constraint names, ORM messages** — reveals schema; `duplicate key value violates
  unique constraint "projects_slug_key"` is a schema dump.
- **Internal resource identifiers** that cross tenant boundaries (raw UUIDs of other tenants,
  internal auto-increment IDs) — existence and enumeration aid.
- **Hostnames, IPs, pod names, cluster details** — topology reconnaissance.
- **Dependency vendor names and versions** ("Stripe SDK 14.2 failed") — target selection.
- **Raw echoed request bytes** — reflection surface; at minimum truncate and escape.

What `4xx` *should* include: a stable `code`, a safe human-readable `detail`, field-level
errors the client can act on, and a `requestId` for support. The full envelope is Ch. 20's
subject; the disclosure boundary here.

### 19.20 — avoiding misleading responses

Misleading responses are subtler than outright lies. The recurring patterns:

1. **Wrong class for the truth** — a validation bug as `500` (clients retry) or a dependency
   outage as `400` (clients stop and blame their users). Every registry row is a chance to
   mislead; test them (deep-dive 01).
2. **Wrong `detail` for the status** — `404` whose detail says "permission denied" (or vice
   versa) undoes the status selection. Detail and status must tell one story.
3. **Misleading headers** — `Location` pointing at a resource that wasn't created because
   creation failed halfway; `Retry-After` on a `500` that will never heal; `Allow` listing
   methods that 403 for everyone.
4. **Success-shaped empty payloads** — `200` with `null` where an object was promised, so
   clients crash on `result.id`. Either return the object or an explicit error/empty state.
5. **Redirect-as-error** — `302` to an HTML error page from a JSON API: every non-JSON client
   breaks, and the status lies (it's not a redirection).

> ⚠️ **Hazard.** The most expensive misleading response is a **`200` after a partial commit**
> — e.g. `Checkout` charges the card, then the write of the order row fails, and the handler
> still returns `200`. The client believes the order exists; the database disagrees. Return a
> coded failure (often `500`/`503` with an idempotency-safe retry path) and let reconciliation
> fix the charge — never paper over it with success (Chapter 28).

## How it works — the disclosure funnel

```text
internal error object (full: code, message, cause, stack, sql, tenant, ...)
        │
        │  map via registry: pick public code + status
        ▼
public projection (code, status, title, safe detail, field errors, requestId)
        │
        │  serializer: NO serializer hooks may add err.stack or err.sql
        ▼
wire response (application/problem+json)  ──▶ client + logs (full version stays internal)
```

The rule that makes this mechanical: **the serializer consumes the public projection type,
not `Error`.** If a serializer can only accept `PublicProblem`, it cannot leak `err.stack` by
forgetting to redact — the field does not exist on the type.

## Worked example — the good and the bad

❌ Misleading and leaky:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "ok": false,
  "error": "QueryFailedError: duplicate key value violates unique constraint \"projects_slug_key\" in projects.ts:142"
}
```

Problems: `200` for a failure (§19.17); schema and file path leaked (§19.18); non-standard
shape; no status for SDKs to branch on; caches may store it as success.

✅ Honest and safe:

```http
HTTP/1.1 409 Conflict
Content-Type: application/problem+json

{
  "type": "/problems/conflict",
  "title": "Conflict",
  "status": 409,
  "code": "SLUG_TAKEN",
  "detail": "A project with this slug already exists in your organization.",
  "instance": "/api/v1/projects",
  "requestId": "req_bb10"
}
```

Status tells the truth; `code` is stable and documented; the DB constraint name, table, and
file path live only in the server log keyed by `requestId`.

## Key data / numbers

- **Never-on-the-wire list (minimum):** stack traces, SQL/ORM messages, constraint names,
  hostnames/pods, file paths, internal UUIDs of other tenants, dependency vendor/version
  strings.
- **Safe-on-the-wire list:** stable public `code`, RFC 9110 status, safe `detail` (≤ ~200
  chars), per-field errors with their own stable codes, `requestId`.
- **Legit `2xx`-with-outcome patterns:** bulk (`200`/`207` + per-item array), operation
  polling (`200` + `status` field), empty-success business outcomes (`200` + documented empty
  representation).
- **Reflection hygiene:** if you echo client input into `detail`, escape it and truncate
  (e.g. 256 chars); never reflect raw bytes into an HTML error page from a JSON API.
- **`207 Multi-Status`** exists (WebDAV, RFC 4918) for per-part statuses; many SaaS APIs
  prefer plain `200` + array for simplicity — either is fine, document the choice.

## Real-world use case — WebhookIngest

`WebhookIngest` processed Stripe events; signature-verification failures were logged and the
handler returned `200` "to stop Stripe retrying." Two poison event types repeated for weeks,
invisible to monitoring because every delivery was "successful" (§19.17), while the events
were silently dropped — customers were never billed for upgrades. The fix: verification
failure → `400` (Stripe retries a few times, then surfaces the endpoint as failing — the
correct signal); unknown-but-valid events → `200` after durable enqueue (ack is honest: we
took responsibility); processing failures post-ack → recorded to DLQ with alerting. Within one
billing cycle, two stuck upgrade flows were caught by the newly-visible failure signal and
fixed. The lesson: **the status code is not for your convenience — it is the sender's
control loop.**

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| `200` + envelope `{ok:false}` | Client "simplicity" | Invisible to monitors/caches/SDKs | Never for public APIs |
| Proper 4xx/5xx + Problem Details | Honest to every consumer | Client must handle errors | Default |
| `200` + per-item statuses for bulk | Partial success expressible | Client must iterate items | Bulk endpoints |
| `207` for bulk | Explicit multi-status | Rarer; some tooling ignores it | If you standardize on it |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return an error status whenever the SDK should enter an error path | Wrap failures in `200` + `ok: false` |
| Project internal errors through the registry before serialization | Serialize `Error` objects directly to clients |
| Keep status and `detail` telling one story | Return `404` whose detail says "forbidden" |
| Return `410`/`409` truthfully even when inconvenient | Redirect JSON clients to HTML error pages |

## Common mistakes

- **`Retry-After` on a `500`.** Promises healing that a bug won't deliver; clients hammer a
  broken deploy.
- **`Location` after failed creation.** Half-committed creates returning `201` + `Location`
  are worse than `500`: the client believes the resource exists.
- **Debug headers in production.** `X-Debug-Stack`, `X-Exception` "temporarily" left on.
  Strip at the boundary, always.
- **Trusting the framework's error page.** Unhandled errors outside your boundary render
  HTML with a stack in dev mode; ensure production mode renders your problem JSON (Ch. 21).

## Checklist

- [ ] No production path returns `2xx` for a failure except documented bulk/polling patterns.
- [ ] The serializer accepts only the public problem type — leaks are type-impossible.
- [ ] Status and `detail` are tested to agree (no "404/permission" hybrids).
- [ ] `Location`, `Retry-After`, and `Allow` are emitted only when truthful.
- [ ] Raw client input is escaped/truncated when echoed into messages.

## Related

- [RFC 9110 and Consistent Selection](./01-rfc-9110-and-consistent-selection.md)
- [Consistency and Information Safety (Ch. 20)](../../20-standardized-api-error-responses/01-concepts/05-consistency-and-information-safety.md)
- [The Response-Already-Started Problem (Ch. 21)](../../21-api-boundary-and-middleware-error-handling/02-deep-dive/02-response-already-started.md)
