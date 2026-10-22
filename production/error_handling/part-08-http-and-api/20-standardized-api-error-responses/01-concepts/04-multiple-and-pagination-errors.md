# Multiple Errors and Pagination Errors

> Part VIII · Chapter 20 · Sections 20.10, 20.11 · _Estimated reading time: 16 min_
> **Prerequisite:** [App Codes, IDs, and Field Details](./03-app-codes-ids-and-field-details.md)

## In one sentence

"Multiple errors" has two distinct shapes — **many field failures in one rejected request**
(keep the single problem envelope, add `errors[]`) and **many items each with their own
outcome** (per-item statuses in a success or multi-status response) — while paginated
endpoints must decide how a mid-page failure affects the page, the cursor, and the client's
merge logic.

## Why this matters in production

Bulk endpoints and list endpoints are where error contracts get sloppy fastest. A bulk import
that returns `500` because item 4,001 failed discards 4,000 successes — or worse, returns
`200` having silently dropped items. A paginated list that 500s on page 3 of an infinite
scroll leaves the client's merge state inconsistent: does it retry the page, restart the
query, or show a hole? These are contract decisions, not incidentals; they must be designed
with the same care as the base envelope.

## Core concept — two meanings of "multiple"

### 20.10a — Aggregated validation failures (one request, many fields)

One request, one verdict: **rejected**. This is still a single problem — `422` with
`errors[]` (previous file). Do **not** return `200` with per-field statuses; do **not** invent
`400`-with-array. The request failed as a unit; the fields explain why.

```json
{
  "type": "/problems/validation-error",
  "status": 422,
  "code": "VALIDATION_FAILED",
  "detail": "Three fields are invalid.",
  "requestId": "req_m1",
  "errors": [
    { "field": "name",  "code": "required",   "message": "name is required." },
    { "field": "seats", "code": "out_of_range","message": "seats must be 1–500." },
    { "field": "owner.email", "code": "format_invalid",
      "message": "owner.email must be a valid email." }
  ]
}
```

### 20.10b — Multi-item operations (many requests in one call)

A bulk endpoint processes N independent items. Per RFC 9110's spirit and common practice
(RFC 4918's `207 Multi-Status` is the formal cousin), the honest contract is:

- **`200` (or `207`) + a per-item result array**, each item carrying its own `status` and
  (on failure) its own problem-shaped entry — **when partial success is meaningful**.
- **`4xx`/`5xx` only when the whole call failed as a unit** — auth, rate limit, payload too
  large, unparseable envelope.

```json
{
  "type": "/problems/bulk-result",
  "title": "Bulk Operation Result",
  "status": 207,
  "requestId": "req_m2",
  "results": [
    { "index": 0, "id": "pr_1", "status": "ok" },
    { "index": 1, "status": "error",
      "problem": { "code": "SLUG_TAKEN", "status": 409,
                   "detail": "Slug 'apollo' already exists." } },
    { "index": 2, "id": "pr_3", "status": "ok" }
  ],
  "summary": { "total": 3, "succeeded": 2, "failed": 1 }
}
```

Decision rules:

- **All-or-nothing semantics** (a transaction across all items): on any failure return one
  `4xx`/`5xx` for the whole call; `results[]` is then unnecessary.
- **Independent items**: always per-item; the call itself "succeeded" in being processed.
- Document whether order is preserved, whether duplicates within the batch are per-item
  conflicts, and the max batch size.

### 20.11 — Errors inside paginated responses

A paginated `GET` returns a page plus cursor metadata. Failure modes:

| Failure | Response | Client action |
| ------- | -------- | ------------- |
| Auth/rate-limit/validation before any query | Normal single problem (`401`/`429`/`422`) | Standard handling |
| Query fails entirely (DB down) | `503` single problem | Retry same cursor after `Retry-After` |
| Page computed but enrichment of one row fails (e.g. per-row permission) | **Design choice, below** | — |
| Cursor invalid/expired | `400`-class problem (`INVALID_CURSOR`) | Restart from first page |

For row-level partial failures inside a page, pick one and document it:

1. **Omit-and-flag (recommended for lists):** drop the failing row, include
   `"partial": true` (or a top-level extension `incomplete: true`) so clients can show a
   placeholder or refetch. Keeps the page renderable.
2. **Placeholder row:** include the row with a per-item problem (mirrors bulk results).
3. **Fail the page:** only if the page is meaningless without every row — rare; prefer (1).

⚠️ **Hazard.** Silently omitting rows *without any signal* is the pagination equivalent of
`200`-for-failure: clients believe the data is complete, sorts and counts go wrong, and users
make decisions on truncated datasets. **Completeness must be explicit in the contract.**

## How it works — choosing the shape

```text
Is this one request with one verdict?
   YES (validation) ──▶ 422 + errors[]        (single problem)
   NO ↓
Is the top-level call itself failing (auth/limit/parse)?
   YES ──▶ single 4xx/5xx problem
   NO ↓
Are outcomes independent per item?
   YES ──▶ 2xx/207 + results[] (+ summary)    (bulk)
   NO (all-or-nothing) ──▶ single 4xx/5xx on any failure
```

## Worked example — ExportJob bulk create

`POST /api/v1/exports/bulk` creates up to 20 export jobs. Two of five queries reference
deleted dashboards:

```http
HTTP/1.1 207 Multi-Status
Content-Type: application/problem+json
X-Request-Id: req_m3

{
  "type": "/problems/bulk-result",
  "title": "Bulk Operation Result",
  "status": 207,
  "requestId": "req_m3",
  "summary": { "total": 5, "succeeded": 3, "failed": 2 },
  "results": [
    { "index": 0, "id": "exp_a", "status": "ok" },
    { "index": 1, "status": "error",
      "problem": { "code": "DASHBOARD_NOT_FOUND", "status": 404,
        "detail": "Dashboard db_77 no longer exists." } },
    { "index": 2, "id": "exp_c", "status": "ok" },
    { "index": 3, "id": "exp_d", "status": "ok" },
    { "index": 4, "status": "error",
      "problem": { "code": "DASHBOARD_NOT_FOUND", "status": 404,
        "detail": "Dashboard db_81 no longer exists." } }
  ]
}
```

The call was processed (so not a bare `4xx`); each failure is actionable and addressable by
index; the summary lets batch UIs render "3 of 5 queued."

## Key data / numbers

- **`207 Multi-Status`:** defined by RFC 4918 (WebDAV); widely used for bulk regardless of
  WebDAV heritage. Plain `200` + `results[]` is equally acceptable — pick one per API.
- **Validation aggregation stays `422`** — never `207` for form validation.
- **`INVALID_CURSOR`** is conventionally `400` (malformed) or `410`/`404` (expired, if you
  tombstone cursors) — choose and document; we recommend `400` with a distinct code and a
  documented "restart from first page" client action.
- **Batch-size limits:** enforce server-side (e.g. 100–1000 items) and return `413`/`422`
  with the limit in `detail` when exceeded.
- **Completeness flag:** `partial: true` (or `incomplete`) on any response where the server
  knowingly omitted items — the anti-silent-truncation guard.

## Real-world use case — WebhookIngest replay API

`WebhookIngest` exposed a bulk replay: `POST /api/v1/webhooks/replay` with up to 500 event
IDs. The first version replayed all-or-nothing in one transaction; one already-expired event
aborted all 500, and customers re-submitted repeatedly, each time re-failing on the same
expired ID. Switching to per-item results (`207` + `results[]`) let clients skip the two
expired events (`410`-flavored per-item problems) and confirm the other 498. Replay success
rate went from all-or-nothing churn to first-pass 99%+, and the support runbook became "show
the `results[]` entries with `status: error`."

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Per-item `207`/`200` + `results[]` | Honest partial success; actionable | Larger payloads; client iteration required | Independent-item bulk |
| All-or-nothing single status | Simple client logic | One bad item fails the batch | Small, transactional batches only |
| Omit failing rows + `partial: true` | Pages stay renderable | Client must handle incompleteness | Paginated lists |
| Fail whole page on row error | Simplest server | Unrenderable pages; retry loops | Rare; avoid |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep validation aggregation as one `422` + `errors[]` | Return `200` with per-field failure maps |
| Return per-item results for independent bulk items | Fail 999 successes because item 1,000 failed |
| Flag partial/incomplete pages explicitly | Silently drop rows from a page |
| Give per-item problems the same `code`/`detail` discipline | Invent ad-hoc per-item strings |
| Bound batch size; return a problem when exceeded | Accept unbounded arrays "for convenience" |

## Common mistakes

- **`results[]` without `summary`.** Clients must re-scan arrays; include counts.
- **Per-item `status: 500` for validation.** An invalid item is a per-item `4xx`-flavored
  problem (e.g. `409`/`404`/`422`-class code), not a server fault.
- **Bulk endpoints that return `200` when *everything* failed.** If all items failed from a
  call-level cause, return the call-level problem; reserve `2xx`+`results[]` for processed
  batches.
- **Cursor errors that look like empty results.** An invalid cursor must error, not return
  `[]` — empty-but-valid is a different, legitimate state.

## Checklist

- [ ] Bulk endpoints document partial-success semantics and max batch size.
- [ ] Validation stays one problem + `errors[]`.
- [ ] Paginated reads signal partial data explicitly.
- [ ] Invalid cursors error distinctly from empty pages.
- [ ] Per-item problems reuse the same envelope discipline (`code`, safe `detail`).

## Related

- [Consistency and Information Safety](./05-consistency-and-information-safety.md)
- [Error Shapes Across Scenarios](../03-practical-examples/02-error-shapes-across-scenarios.md)
- [The Error Envelope Spec](../05-reference/README.md)
