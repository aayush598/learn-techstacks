# Chapter 17 — Reference

> Part VII · Chapter 17 · The validation error contract, status decision tables, code catalogue,
> and pointer conventions.

## The validation error contract

```http
HTTP/1.1 422 Unprocessable Content
content-type: application/problem+json
```

```text
Problem (RFC 9457) + extensions
{
  type          URI identifier of the problem type      → branchable, stable
  title         short human summary ("VALIDATION_FAILED")→ not for branching
  status        number (422), repeated in-body
  detail        one human sentence, replaceable
  instance      request path / URI reference
  requestId     correlation id                           → extension
  errors[]      field entries                             → extension
  errorsTruncated bool, present only when capped          → extension
}

Field entry
{
  pointer   required  RFC 6901 path from payload root ("/" or "" for whole body)
  code      required  registry-listed, rule-level, stable
  message   optional  human/localized sentence; never a contract key
  params    optional  interpolation values: min, max, format, when, other, key…
}
```

JSON:API alternative (equivalent, pick one and stay with it):
`errors[].source.pointer` + `errors[].code` + `errors[].detail`.

## Status decision table

| Situation | Status | Body | Note |
| --------- | ------ | ---- | ---- |
| Wrong method for route | `405` | problem, no fields | Include `Allow` header |
| Body over route cap | `413` | problem, no fields | Abort during read |
| Wrong/missing media type | `415` | problem, no fields | Don't sniff on writes |
| Headers over cap | `431` | problem | Server-level |
| Missing/invalid auth (guard) | `401` / `403` | problem | Ch. 35 owns semantics |
| Unparseable JSON | `400` | problem, **zero** field errors | Never `422` |
| Complexity bomb (depth/keys) | `400` | `PAYLOAD_TOO_COMPLEX` | Before schema walk |
| Wrong top-level container type | `400` (recommended) | no field pointers | Pick one policy |
| Unknown field / structure | `422` | `unknown_field` etc. | Strict writes |
| Required/type/range/format | `422` | field entries | ≥1 entry guaranteed |
| Cross-field / conditional | `422` | field entry with `rule`/`when` | Gated on clean inputs |
| Bulk invalid rows (no writes) | `422` | entries + `summary` | `rejected: true` |
| Bulk partial written | `200` + results | per-row outcomes | Never `422` after writes |
| Uniqueness vs existing data | `409` | problem | L3 — Ch. 18 |
| State/entitlement/quota | `409`/`403`/`402`/`429` | problem | L3 — Ch. 18 |
| Verified-but-unactionable webhook payload | `400` | bare problem | Detail in logs |

## Rule class → code catalogue (start here; register before use)

| Rule class | Code | Typical `params` | Section |
| ---------- | ---- | ---------------- | ------- |
| Unknown key | `unknown_field` | `key` | 17.2 |
| Unexpected container shape | `unexpected_shape` | `expected` | 17.2 |
| Missing/null/empty required | `required` | — | 17.3 |
| Wrong type / non-integer | `type_mismatch` | `expected`, `received` | 17.4 |
| Outside numeric/temporal bound | `out_of_range` | `min`, `max`, `inclusive` | 17.5 |
| String pattern failure | `format_invalid` | `format` | 17.6 |
| Too long / too short | `too_long` / `too_short` | `max` / `min` | 17.5 |
| Multi-field rule failure | `cross_field_invalid` | `rule`, `other` | 17.7 |
| Conditional rule failure | `conditional_rule_failed` | `when`, `rule` | 17.8 |
| Collection too large/small | `too_many_items` / `too_few_items` | `max` / `min` | 17.10 |
| Duplicate within payload | `duplicate_item` | `firstIndex` | 17.10 |
| Payload too complex | `PAYLOAD_TOO_COMPLEX` | `maxDepth`, `maxKeys` | 17.19 |
| Body unparseable | `MALFORMED_BODY` | — | 17.19 |
| Top-level validation (envelope) | `VALIDATION_FAILED` | — | all |

## Aggregation decision table

| Stage | Strategy | Cap |
| ----- | -------- | --- |
| Method/size/media-type guards | Fail fast | n/a |
| Parse | Fail fast | n/a |
| Complexity guard | Fail fast | n/a |
| Per-field rules | Aggregate | issues ≤ 100 (rec.) |
| Cross-field/conditional | Aggregate, gated | per above |
| Bulk rows | Aggregate per row, then policy | rows ≤ 1,000 (rec.) |
| Domain checks (L3) | First conflict or grouped | n/a |

## Pointer conventions

```text
/                      whole payload (structure-level); some stacks use "" — pick one
/name                  top-level field
/billing/street        nested object
/items/2/sku           nested array, zero-based
/columns/1             bulk list item
/filters/1/field       nested field inside bulk item
```

Escaping (RFC 6901): `~` → `~0`, `/` → `~1` in key segments. Use a library.

## Where the check lives

| Check | Layer | Owner |
| ----- | ----- | ----- |
| Bytes/media-type/parse | transport middleware | platform team |
| Field/structure rules | DTO/schema module | endpoint owner |
| Cross-field/conditional | DTO/schema module (same pass) | endpoint owner |
| Uniqueness, entitlement, state | domain service | domain owner |
| DB constraints (`NOT NULL`, `CHECK`, unique) | persistence backstop | translates via Ch. 16 map |

## Client-side rendering algorithm

```text
on 422:
  for e in body.errors:
    template = dict[e.messageKey ?? "validation." + e.code] ?? e.message ?? e.code
    field[e.pointer].show(interpolate(template, e.params))
  if body.errorsTruncated: show "more errors not shown" note
```

## Contract invariants (test these)

1. Every `422` has ≥ 1 entry; every entry has `pointer` + registry `code`.
2. Every `400` has 0 field entries.
3. No response contains SQLSTATE, column names, stack frames, or regex source.
4. One primary `(pointer, code)` pair; no duplicate pairs.
5. `errors.length == errorsTruncated ? cap : < cap` semantics hold.
6. Golden snapshot per endpoint family matches in CI.

## Signposts

- Domain side of the line → [Ch. 18](../../18-domain-and-business-logic-errors/README.md)
- HTTP status semantics → [Ch. 19](../../../part-08-http-and-api/19-http-error-semantics/README.md)
- Envelope standards (RFC 9457) → [Ch. 20](../../../part-08-http-and-api/20-standardized-api-error-responses/README.md)
- Middleware placement → [Ch. 21](../../../part-08-http-and-api/21-api-boundary-and-middleware-error-handling/README.md)
- Code registry governance → [Ch. 8](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)

## Related

- [Chapter 17 Do's and Don'ts](../04-dos-and-donts/README.md)
- [CreateProject DTO → 422 Envelope](../03-practical-examples/01-create-project-dto-to-422-envelope.md)
- [Chapter 18 Reference](../../18-domain-and-business-logic-errors/05-reference/README.md)
