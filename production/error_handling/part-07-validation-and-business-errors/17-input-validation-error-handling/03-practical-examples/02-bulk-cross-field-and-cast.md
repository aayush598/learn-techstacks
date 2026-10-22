# Bulk Row Failures, Cross-Field Rules, and Untrusted Payloads

> Part VII · Chapter 17 · All sections · _Estimated reading time: 22 min_
> **Prerequisite:** [CreateProject DTO → 422 Envelope](./01-create-project-dto-to-422-envelope.md)

## In one sentence

Three production shapes of the same contract: **bulk row validation** with per-row pointers and a
summary (`ExportJob`), **cross-field rules** that fire once on clean inputs (`Checkout`), and
**payload validation behind a signature** where the honest answer to anything unverified is a bare
`400` (`WebhookIngest`).

## Why this matters in production

Single-object `422`s are the easy case. The pressure appears at the edges: 1,200-row imports,
scheduled upgrades with dates, and webhooks that anyone on the internet can POST to. Each edge has
one trap that generic advice misses — partial writes after `422`, derivative duplicate errors, and
validation oracles — and each trap is cheap to design out if you have seen it once.

## Shape 1 — Bulk rows (`ExportJob`)

`POST /v1/exports` with `{ range, columns[], filters[] }`, all-or-nothing policy.

```json
{
  "range": { "from": "2026-01-01", "to": "2026-01-31" },
  "columns": ["id", "nam", "seats"],
  "filters": [
    { "field": "status",   "op": "eq",  "value": "active" },
    { "field": "nmae",     "op": "eq",  "value": "x" },
    { "field": "seats",    "op": "gt",  "value": 10 }
  ]
}
```

```json
{
  "type": "https://errors.acme.example/validation",
  "title": "VALIDATION_FAILED",
  "status": 422,
  "detail": "The request contains 2 invalid field(s).",
  "instance": "/v1/exports",
  "requestId": "req_b40e77",
  "errors": [
    { "pointer": "/columns/1",   "code": "unknown_field", "params": { "key": "nam" } },
    { "pointer": "/filters/1/field", "code": "unknown_field", "params": { "key": "nmae" } }
  ],
  "summary": { "total": 3, "invalid": 2, "valid": 1, "rejected": true }
}
```

Mechanics that made this correct:

- **Container size guards first** (`/columns` `too_many_items` at 100, `/filters` at 20) —
  otherwise item work is unbounded (17.10).
- **Indexed pointers** `/columns/1`, `/filters/1/field` — zero-based, so bulk UIs highlight the
  exact cell.
- **`summary.invalid` counts distinct rows/items with errors (2), not issues (2 here, but 5 if a
  row had three bad cells)** — clients loop rows, not issues.
- **Nothing is enqueued on `422`.** The job does not start, does not partially exist. If the
  product later opts into partial mode, the response becomes `200` with per-row outcomes and a
  result id — never a `422` after work happened (17.11 hazard).

```ts
// All-or-nothing: validate completely, then enqueue — no interleaving.
const issues = validateExportSpec(body);
if (issues.length) return toValidationProblem(issues, ctx);   // 422, zero side effects
const job = await exportQueue.enqueue({ spec: toSpec(body), tenantId });  // only now
return res.status(202).json({ jobId: job.id });
```

## Shape 2 — Cross-field (`Checkout`)

Scheduled plan change: `{ plan, seats, startDate, endDate, billing }`.

```json
{
  "pointer": "/endAt",
  "code": "cross_field_invalid",
  "message": "End date must not be before the start date.",
  "params": { "rule": "end_after_start", "other": "/startAt" }
}
```

The three correctness properties (each one is a past bug somewhere):

| Property | Bad version | Good version |
| -------- | ----------- | ------------ |
| Fires once | `startDate too early` **and** `endDate too late` | One entry, pointer `/endAt` |
| Suppressed when input failed | `required` on `/startAt` + `cross_field_invalid` on `/endAt` | Cross-field skipped — one error total |
| Points at the canonical field | pointer `/` or `/startDate` | `/endAt` + `params.other=/startAt` |

Conditional cousin for the same flow:

```json
{ "pointer": "/seats", "code": "conditional_rule_failed",
  "params": { "when": "plan=enterprise", "rule": "seats_required" } }
```

— so the free-plan user is never told "seats is required" with no context.

## Shape 3 — Untrusted ingress (`WebhookIngest`)

```python
# Order: signature → parse → complexity → schema. Field errors never leak pre-auth.
def handle_webhook(request):
    raw = request.body()
    if len(raw) > MAX_WEBHOOK_BYTES:                 # 256 KB
        return Response(413)
    if not hmac.compare_digest(signing_secret, compute_sig(raw, request.headers)):
        return Response(400)                         # single non-informative answer
    try:
        event = json.loads(raw)
    except ValueError:
        return Response(400)                         # verified-but-malformed: still no details
    issues = validate_event(event)                   # registered schema, versioned
    if issues:
        log.warning("webhook_schema_mismatch", code=issues[0].code,
                    event_type=event.get("type"), requestId=request.id)
        return Response(400)                         # Stripe-style: fail → provider retries/logs
    dispatch(event)
    return Response(200)
```

Why no `422` here: the caller is a **provider retry loop**, not a human. It cannot fix fields;
it needs only `2xx` (accepted) vs `4xx` (reject). Field-level detail belongs in **logs** with the
`requestId`, not in the response. This is the general rule: *the audience decides whether field
errors are contract or telemetry*.

| Ingress | `422` field errors? | Why |
| ------- | ------------------- | --- |
| Human/agent API client | ✅ Yes | Can fix and resubmit |
| Bulk import UI | ✅ Yes (row pointers) | Same |
| Provider webhook | ❌ No — `400` + logs | Cannot fix; retry semantics |
| Queue consumer | ❌ No — DLQ with context | No requester exists |

## Key data / numbers

- Bulk summary keys: `total`, `invalid`, `valid`, `rejected` — always all four.
- Pointers: zero-based `/columns/1`, `/filters/1/field`.
- Cross-field: **one issue per rule**, gated on clean inputs, pointer at the canonical field.
- Webhook: signature first; caps (recommended **256 KB**); any pre-auth failure → uniform `400`;
  no field errors before verification.
- All-or-nothing bulk: `422` ⇒ **zero side effects**; partial mode ⇒ `200` + per-row results.

## Real-world use case — Checkout + ExportJob at Acme

Two incidents, one root cause (contract ambiguity). (1) `Checkout`'s scheduled-upgrade endpoint
emitted `end_after_start` even when `startDate` was missing; a support macro told a customer to
"fix the end date" three times. (2) `ExportJob`'s importer wrote the valid 1,197 rows and returned
`422` — a client retry **duplicated 1,197 rows** in the export log because it treated `422` as
"nothing happened". Fixes: dependency-gated cross-field evaluation, `summary` with explicit
`rejected: true`, and partial mode moved to `200` + `results[]` with an idempotency key. The
duplicate-write class of ticket has not recurred since.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| All-or-nothing bulk | Simple client semantics | One bad row blocks 1,999 | ✅ Default |
| Partial bulk + result id | High throughput on messy data | Needs idempotency + result API | Large imports, ETL |
| Webhook `422` detail | Debuggable | Oracle risk, useless to retry loops | Only for first-party internal webhooks |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Validate the whole batch before any write | Enqueue rows one-by-one, discovering errors after writes |
| Index every bulk pointer from zero | Point all row errors at `/rows` |
| Log field codes on webhook reject; return bare `400` | Return validation detail to unsigned callers |
| Gate cross-field rules on clean inputs | Emit derivative errors from one root cause |

## Common mistakes

- **`summary.invalid` counting issues instead of rows** — UI loops show "3 invalid" when 1 row
  has 3 cells.
- **Client-side-only dedup of bulk rows** — server receives duplicates anyway; validate
  uniqueness server-side (`duplicate_item`).
- **Webhook 4xx retry storms** — if you return `500` to a provider for a bad payload, it retries
  forever; bad payloads are `400`.
- **Mixed audiences on one endpoint** — humans want field errors, machines want logs; split the
  endpoints or pick the dominant audience.

## Checklist

- [ ] Bulk: size guards → per-item pointers → summary → policy before any write.
- [ ] Cross-field: single canonical pointer, one fire, dependency-gated.
- [ ] Ingress: signature → parse → complexity → schema; `422` only post-verification if at all.
- [ ] `422` never coexists with side effects on the same request.
- [ ] Audience (human vs retry loop) decides field-error exposure.

## Related

- [CreateProject DTO → 422 Envelope](./01-create-project-dto-to-422-envelope.md)
- [Aggregation Mechanics](../02-deep-dive/01-aggregation-mechanics.md)
- [Chapter 33 — Events, Webhooks, and Message Processing](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
- [Validation Reference](../05-reference/README.md)
