# Postgres SQLSTATE at the Boundary

> Part VI · Chapter 15 · All sections · _Estimated reading time: 18 min_
> **Prerequisite:** [Code-Level Boundaries](../01-concepts/02-code-level-boundaries.md)

## In one sentence

The repository boundary is where **PostgreSQL `SQLSTATE` codes are classified, contained, and
translated** — and the single most common place where teams accidentally leak schema or collapse
distinct failures into one meaningless error.

## Why this matters in production

Every DB-backed SaaS sees `SQLSTATE` codes all day. If the repository does not own them, they
either reach the API (leak) or get flattened into `DB_ERROR` (lost meaning, wrong status). This
file gives the exact mapping a repository boundary should implement.

## What a `SQLSTATE` is

PostgreSQL reports errors with a 5-character `SQLSTATE`. Drivers expose it in different ways:

| Language | Where the state lives |
| -------- | --------------------- |
| Node `pg` | `err.code` (and structured `err.constraint`, `err.table`, `err.column`) |
| Python `psycopg2` | exception class (`errors.UniqueViolation`) + `e.pgcode` |
| Python `asyncpg` | exception class (`exceptions.UniqueViolationError`) + `e.sqlstate` |
| Go `pgx`/`lib/pq` | `*pgconn.PgError.Code` (via `errors.As`) |
| Java JDBC | `SQLException.getSQLState()` |
| SQLAlchemy | `exc.orig.pgcode` after `DBAPIError` |

The **repository boundary** is the only layer allowed to know this table.

## The core translation table

| SQLSTATE | Postgres meaning | Domain meaning | Retry? | HTTP |
| -------- | ---------------- | -------------- | ------ | ---- |
| `23505` | `unique_violation` | `ALREADY_EXISTS` (per resource) | No | 409 |
| `23503` | `foreign_key_violation` | `NOT_FOUND` (referenced row) / `INVALID_REFERENCE` | No | 404 / 422 |
| `23502` | `not_null_violation` | `REQUIRED_FIELD_MISSING` (bug if validated) | No | 422 / 500 |
| `23514` | `check_violation` | `BUSINESS_RULE_VIOLATION` | No | 422 |
| `40001` | `serialization_failure` | `RETRYABLE_CONFLICT` | **Yes** | 409 / 503 |
| `40P01` | `deadlock_detected` | `RETRYABLE_CONFLICT` | **Yes** | 409 / 503 |
| `57014` | `query_canceled` | `TIMEOUT` / `CANCELLED` | Yes (if deadline) | 504 |
| `53300` | `too_many_connections` | `DB_UNAVAILABLE` | **Yes** | 503 |
| `08006` | `connection_failure` | `DB_UNAVAILABLE` | **Yes** | 503 |
| `08003` | `connection_does_not_exist` | `DB_UNAVAILABLE` | Yes | 503 |
| `42P01` | `undefined_table` | `SCHEMA_ERROR` (deploy bug) | No | 500 |
| `22001` | `string_data_right_truncation` | `VALUE_TOO_LONG` | No | 422 |
| `22003` | `numeric_value_out_of_range` | `VALUE_OUT_OF_RANGE` | No | 422 |
| `42703` | `undefined_column` | `SCHEMA_ERROR` (deploy bug) | No | 500 |

> ⚠️ **Hazard.** `42P01` / `42703` are **deployment/programming faults**, not user errors. A
> migration gap should page a human and never be shown as a `422`. Classify them as
> `SCHEMA_ERROR` → `500` and alert.

## Implementing the boundary in three languages

### TypeScript (`pg`)

```ts
type PgError = { code?: string; constraint?: string; table?: string };

function translatePg(err: unknown, ctx: { resource: string }): AppError {
  const e = err as PgError;
  switch (e?.code) {
    case "23505":
      return new DomainError(`${ctx.resource.toUpperCase()}_ALREADY_EXISTS`, { cause: err });
    case "23503":
      return new DomainError(`${ctx.resource.toUpperCase()}_REFERENCE_MISSING`, { cause: err });
    case "23514":
      return new DomainError(`${ctx.resource.toUpperCase()}_RULE_VIOLATION`, { cause: err });
    case "40001":
    case "40P01":
      return new RetryableError("RETRYABLE_CONFLICT", { cause: err });
    case "53300":
    case "08006":
    case "08003":
      return new InfrastructureError("DB_UNAVAILABLE", { transient: true, cause: err });
    case "42P01":
    case "42703":
      return new InfrastructureError("SCHEMA_ERROR", { alert: true, cause: err });
    default:
      return new InfrastructureError("DB_WRITE_FAILED", { cause: err });
  }
}
```

### Python (`psycopg2`)

```python
def translate_pg(err: Exception, resource: str) -> AppError:
    state = getattr(err, "pgcode", None)
    if state == "23505":
        return DomainError(f"{resource.upper()}_ALREADY_EXISTS", cause=err)
    if state == "23503":
        return DomainError(f"{resource.upper()}_REFERENCE_MISSING", cause=err)
    if state in ("40001", "40P01"):
        return RetryableError("RETRYABLE_CONFLICT", cause=err)
    if state in ("53300", "08006", "08003"):
        return InfrastructureError("DB_UNAVAILABLE", transient=True, cause=err)
    if state in ("42P01", "42703"):
        return InfrastructureError("SCHEMA_ERROR", alert=True, cause=err)
    return InfrastructureError("DB_WRITE_FAILED", cause=err)
```

### Go (`pgx`)

```go
func translatePg(err error, resource string) error {
    var pgErr *pgconn.PgError
    if !errors.As(err, &pgErr) {
        return fmt.Errorf("%w: %v", ErrDBWriteFailed, err)
    }
    switch pgErr.Code {
    case "23505":
        return fmt.Errorf("%w: %v", ErrAlreadyExists, err)
    case "23503":
        return fmt.Errorf("%w: %v", ErrReferenceMissing, err)
    case "40001", "40P01":
        return fmt.Errorf("%w: %v", ErrRetryableConflict, err)
    case "53300", "08006", "08003":
        return fmt.Errorf("%w: %v", ErrDBUnavailable, err)
    case "42P01", "42703":
        return fmt.Errorf("%w: %v", ErrSchemaError, err)
    default:
        return fmt.Errorf("%w: %v", ErrDBWriteFailed, err)
    }
}
```

## What the boundary must preserve

1. **Cause.** Attach the raw driver error (`cause`, `%w` with care, `raise from`) for server logs.
2. **Constraint metadata (server-side only).** `err.constraint` tells you *which* unique index
   fired; use it to pick the domain code, but never expose it.
3. **Retry class.** `40001`/`40P01`/`53300`/`08006` are transient; the rest are not. Losing this
   turns a recoverable blip into a permanent failure.

```ts
// Use constraint metadata to choose the precise domain code — server-side only.
if (e.code === "23505" && e.constraint === "users_email_key") {
  throw new DomainError("EMAIL_ALREADY_USED", { cause: err });
}
```

## The leak checklist for this boundary

```ts
// ❌ Everything below leaks: schema, table, column, constraint, SQL.
throw err;
res.status(500).send(err.detail); // pg puts SQL-ish text in .detail / .where
// ✅ Only the domain code + safe message cross the boundary.
throw new DomainError("EMAIL_ALREADY_USED", { safeMessage: "That email is already in use.", cause: err });
```

## Key data / numbers

- Class 23 = integrity constraint violation (`23505`, `23503`, `23502`, `23514`).
- Class 40 = transaction rollback (`40001`, `40P01`) — the classic retryable class.
- Class 08 = connection exception (`08006`, `08003`) — retryable, often circuit-break on.
- Class 42 = syntax/access rule (`42P01`, `42703`) — deployment faults.
- `pg` exposes `err.constraint`, `err.table`, `err.column`, `err.detail`, `err.schema`.

## Real-world use case — ExportJob

`ExportJob` bulk-inserts rows. It hit `40P01` (deadlock) under concurrent exports older code
treated as fatal, failing the job. The repository boundary translated `40P01` → `RETRYABLE_CONFLICT`;
the job boundary (Ch. 32) retried with backoff and succeeded. Separately, a `42P01`
(`undefined_table`) after a bad deploy was classified as `SCHEMA_ERROR` and **paged on-call**
— exactly the right outcome for a migration fault.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Map each SQLSTATE class to a distinct domain meaning | Collapse every code into `DB_ERROR` |
| Mark `40001`/`40P01`/class-08 as transient | Retry `23505`/`23503` (permanent) |
| Keep `constraint`/`table` server-side | Put constraint names in the response |
| Classify class-42 as a deploy fault (alert) | Show schema errors as user `422` |

## Common mistakes

- **`23503` mapped to `500`** — usually means "referenced row missing" → `404`/`422`.
- **Not distinguishing unique from FK** by catching `IntegrityError` broadly.
- **Swallowing `57014`** (query canceled) — it may be a user timeout or a `statement_timeout`;
  decide deliberately.
- **Retrying a `23505`** in a loop, amplifying an idempotency bug.

## Checklist

- [ ] Repository is the only layer that references `SQLSTATE`.
- [ ] Each class-23 code maps to a specific domain meaning and HTTP status.
- [ ] Class-40 and class-08 map to transient errors.
- [ ] Class-42 maps to `SCHEMA_ERROR` and alerts.
- [ ] Constraint/table/column metadata never crosses the boundary.

## Related

- [A Full Boundary Map for an Acme SaaS Request](./01-acme-request-boundary-map.md)
- [SQLSTATE → Domain → HTTP map](../../16-error-translation-and-normalization/03-practical-examples/01-postgres-sqlstate-to-domain-to-http.md)
- [Part IX — Database Error Classification](../../../part-09-database-and-transactions/22-database-error-classification/README.md)
