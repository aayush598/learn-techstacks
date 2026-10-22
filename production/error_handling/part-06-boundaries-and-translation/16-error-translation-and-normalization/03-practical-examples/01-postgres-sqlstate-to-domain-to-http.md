# Postgres SQLSTATE → Domain Error → HTTP Status

> Part VI · Chapter 16 · All sections · _Estimated reading time: 22 min_
> **Prerequisite:** [Translation Directions](../01-concepts/02-translation-directions.md)

## In one sentence

This is the definitive **two-hop translation map**: a Postgres `SQLSTATE` becomes a **domain error**
(carrying category and retry class), which then becomes an **HTTP status and error code** — with the
raw driver error preserved only as `cause`.

## Why this matters in production

This is the single most common translation in a DB-backed SaaS, and the one teams most often get
wrong: they either leak the `SQLSTATE`/constraint to the client or collapse every database failure
into a blind `500`. A correct table makes statuses right, retries safe, and client behavior
predictable — with no Postgres types escaping the repository.

## The two hops

```text
HOP 1  (repository boundary)          HOP 2  (request boundary)
SQLSTATE 23505                        DomainError ALREADY_EXISTS
+ constraint "users_email_key"  ──▶   category=CONFLICT, transient=false  ──▶  HTTP 409
cause: PgError (server-only)          details={field:"email"}                  body: Problem + JSON
```

Hop 1 owns **meaning**; hop 2 owns **transport**. Neither invents the other's responsibility.

## The full map

| SQLSTATE | Postgres meaning | Domain code | Category | Transient | HTTP | Client action |
| -------- | ---------------- | ----------- | -------- | --------- | ---- | ------------- |
| `23505` | unique_violation | `ALREADY_EXISTS` (+`details.field`) | CONFLICT | No | 409 | Fix input / treat as success if replay |
| `23503` | foreign_key_violation | `REFERENCE_MISSING` | VALIDATION/CONFLICT | No | 422 (or 404 for a missing parent) | Re-select valid parent |
| `23502` | not_null_violation | `REQUIRED_FIELD_MISSING` | VALIDATION | No | 422 | Fill the field (bug if pre-validated → alert) |
| `23514` | check_violation | `BUSINESS_RULE_VIOLATION` | VALIDATION | No | 422 | Correct the value |
| `40001` | serialization_failure | `RETRYABLE_CONFLICT` | DEPENDENCY | **Yes** | 409 (or 503) | Retry |
| `40P01` | deadlock_detected | `RETRYABLE_CONFLICT` | DEPENDENCY | **Yes** | 409 (or 503) | Retry |
| `57014` | query_canceled | `QUERY_TIMEOUT` | DEPENDENCY | Yes if deadline | 504 | Retry / reduce work |
| `53300` | too_many_connections | `DB_UNAVAILABLE` | DEPENDENCY | **Yes** | 503 + `Retry-After` | Retry with backoff |
| `08006` | connection_failure | `DB_UNAVAILABLE` | DEPENDENCY | **Yes** | 503 + `Retry-After` | Retry |
| `08003` | connection_does_not_exist | `DB_UNAVAILABLE` | DEPENDENCY | **Yes** | 503 | Retry |
| `42P01` | undefined_table | `SCHEMA_ERROR` | INTERNAL | No | 500 | Support (alert on-call) |
| `42703` | undefined_column | `SCHEMA_ERROR` | INTERNAL | No | 500 | Support (alert on-call) |
| `22001` | string_data_right_truncation | `VALUE_TOO_LONG` | VALIDATION | No | 422 | Shorten value |
| `22003` | numeric_value_out_of_range | `VALUE_OUT_OF_RANGE` | VALIDATION | No | 422 | Fix value |
| `23P01` | exclusion_violation | `RESOURCE_CONFLICT` | CONFLICT | No | 409 | Resolve overlap |
| `55000` | object_not_in_prerequisite_state | `INVALID_STATE` | CONFLICT | No | 409 | Refresh state |
| *(unknown)* | — | `DB_WRITE_FAILED` | INTERNAL/DEPENDENCY | `status≥500` rule | 500 | Support |

## Hop 1 — Repository: SQLSTATE → domain

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class DomainError(Exception):
    code: str
    category: str
    transient: bool
    http_status: int
    safe_message: str
    details: dict = field(default_factory=dict)
    cause: Optional[BaseException] = None

FIELD_BY_CONSTRAINT = {
    "users_email_key": "email",
    "projects_slug_key": "slug",
    "invitations_project_id_email_key": "email",
}

def translate_pg(err: BaseException, *, resource: str) -> DomainError:
    state = getattr(err, "pgcode", None)
    constraint = getattr(err, "diag", None) and getattr(err.diag, "constraint_name", None)

    if state == "23505":
        return DomainError("ALREADY_EXISTS", "CONFLICT", False, 409,
                           "That value already exists.",
                           details={"field": FIELD_BY_CONSTRAINT.get(constraint)}, cause=err)
    if state == "23503":
        return DomainError("REFERENCE_MISSING", "VALIDATION", False, 422,
                           "A referenced record does not exist.", cause=err)
    if state in ("23502",):
        return DomainError("REQUIRED_FIELD_MISSING", "VALIDATION", False, 422,
                           "A required field is missing.", cause=err)
    if state in ("23514",):
        return DomainError("BUSINESS_RULE_VIOLATION", "VALIDATION", False, 422,
                           "The value violates a business rule.", cause=err)
    if state in ("40001", "40P01"):
        return DomainError("RETRYABLE_CONFLICT", "DEPENDENCY", True, 409,
                           "A concurrent update occurred; retry.", cause=err)
    if state in ("53300", "08006", "08003"):
        return DomainError("DB_UNAVAILABLE", "DEPENDENCY", True, 503,
                           "The database is temporarily unavailable.", cause=err)
    if state in ("42P01", "42703"):
        return DomainError("SCHEMA_ERROR", "INTERNAL", False, 500,
                           "An unexpected error occurred.", cause=err)  # alert=True in meta
    if state in ("22001", "22003"):
        return DomainError("VALUE_OUT_OF_RANGE", "VALIDATION", False, 422,
                           "The value is out of the allowed range.", cause=err)
    # Unknown SQLSTATE: safe generic; transient only if clearly a connection-class failure.
    return DomainError("DB_WRITE_FAILED", "INTERNAL", False, 500,
                       "An unexpected error occurred.", cause=err)
```

**Preserved:** `cause` (the `PgError`), `transient` (explicit), `constraint` → `details.field`.
**Never emitted:** the `SQLSTATE` string, the constraint name as-is, any SQL text.

## Hop 2 — Request boundary: domain → HTTP

```ts
function toResponse(err: DomainError, instance: string) {
  const status = err.httpStatus; // decided in hop 1's classification, not here
  return {
    status,
    body: {
      type: `https://errors.acme.example/${err.category.toLowerCase()}`,
      title: err.code,                   // stable, machine-readable
      status,
      detail: err.safeMessage,           // curated, no internals
      ...(Object.keys(err.details).length ? { errors: err.details } : {}),
      instance,                          // correlation id
    },
  };
}
```

Hop 2 adds **transport concerns only**: problem-details shape, correlation id, and (for `503`) a
`Retry-After` header derived from the retry policy.

## Handling the transient hop in the service

Between hops, the **service (transaction) boundary** decides retry for `RETRYABLE_CONFLICT`:

```go
for attempt := 1; attempt <= 3; attempt++ {
    err := repo.Insert(ctx, inv)
    if errors.Is(err, ErrRetryableConflict) && attempt < 3 {
        time.Sleep(backoff(attempt)) // 20ms, 40ms (+ jitter)
        continue
    }
    return err // already-translated domain error, or success
}
```

`40P01`/`40001` never reach the client if a retry succeeds — the mapping still exists for the
exhausted case (then `409`/`503`).

## A concrete end-to-end trace

```text
Request: POST /projects/42/invitations { email: "a@b.com" }  (duplicate)

repository:  insert → PgError{ code:"23505", constraint:"invitations_project_id_email_key" }
hop 1:       DomainError{ code:"ALREADY_EXISTS", category:"CONFLICT", transient:false,
                          httpStatus:409, details:{field:"email"}, cause:PgError }
service:     not retryable → propagate
hop 2:       HTTP 409
             { "type":".../conflict", "title":"ALREADY_EXISTS", "status":409,
               "detail":"That value already exists.", "errors":{"field":"email"},
               "instance":"req_8f2c1a" }
log:         error with requestId=req_8f2c1a, cause=PgError (server-side only)
```

## Key data / numbers

- Class **23** integrity: `23505` unique, `23503` FK, `23502` not-null, `23514` check.
- Class **40** rollback: `40001` serialization, `40P01` deadlock → transient, HTTP `409`/`503`.
- Class **08** connection: `08006`, `08003` → transient, HTTP `503` + `Retry-After`.
- Class **42** syntax/access: `42P01`, `42703` → `SCHEMA_ERROR`, HTTP `500`, **alert**.
- `57014` query canceled → `504`; `53300` too many connections → `503`.
- Constraint identity is what selects `details.field` **without** exposing the index name.

## Real-world use case — Acme SaaS

Acme's invitation flow mapped every `IntegrityError` to `500`. Duplicate invitations looked like
outages and generated support tickets; a bad migration (`42P01`) also produced `500` but **without
an alert**, so it took 40 minutes to notice. Applying this map: duplicates became `409` with a
field hint, FK failures became `404/422`, and schema errors became alerting `500`s. Support load
dropped and deploy faults now page on-call within a minute.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Distinguish class 23/40/08/42 | Map all `IntegrityError` to `500` |
| Keep `SQLSTATE` and constraint server-side | Put constraint names in the response |
| Mark class-40/08 transient | Retry `23505`/`23503` |
| Use constraint identity for `details.field` | Expose the index name |
| Alert on class-42 schema errors | Show deploy faults as user `422` |

## Common mistakes

- **`23503` as `500`** — it usually means "referenced row missing" (`404`/`422`).
- **Retrying a unique violation**, amplifying an idempotency bug.
- **Losing `transient`**, so deadlocks fail the job permanently.
- **Not alerting on `SCHEMA_ERROR`**, so a bad migration is discovered by users.

## Checklist

- [ ] Hop 1 is the only layer that reads `SQLSTATE`/constraint.
- [ ] Hop 2 derives status from the domain classification, not a per-handler guess.
- [ ] Every code maps to a specific category and retry class.
- [ ] Constraint metadata selects `details.field` without leaking.
- [ ] Class-42 alerts; class-40/08 is retryable.

## Related

- [Postgres SQLSTATE at the Boundary](../../15-error-boundaries/03-practical-examples/02-postgres-sqlstate-boundary-map.md)
- [Normalization with the Recurring Cast](./02-normalization-with-recurring-cast.md)
- [Part IX — Database Error Classification](../../../part-09-database-and-transactions/22-database-error-classification/README.md)
