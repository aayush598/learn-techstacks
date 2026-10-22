# Driver and Vendor Error Shapes

> Part IX · Chapter 22 · Sections 22.1–22.6, 22.20 · _Estimated reading time: 22 min_
> **Prerequisite:** [The SQLSTATE Classification Table](./01-sqlstate-classification-table.md)

## In one sentence

Every driver exposes the same facts under **different field names** — so write **one adapter per
driver** that normalizes `(code, class, constraint, table, column, detail)` into a single shape,
instead of scattering `err.code` / `e.pgcode` / `pgErr.Code` across the codebase.

## Why this matters in production

A team standardizes on Postgres, then adds a MySQL-backed analytics store, then a Prisma-based
admin service. Now three shapes exist: node-pg puts the SQLSTATE in `err.code`, psycopg2 in
`e.pgcode`, Go's `pq` in `*pq.Error.Code`, pgx in `*pgconn.PgError.Code`, and Prisma hides all
of it behind `P2002`. If the classifier is written against one driver, the others silently fall
through to `DB_UNKNOWN` → `500` + alert. Normalizing at the adapter boundary is the difference
between one mapping and five.

## Core concept

```text
        ┌──────────── driver-specific exception ────────────┐
        │ node-pg  err.code, err.constraint, err.detail     │
        │ psycopg2 e.pgcode, e.diag.constraint_name         │
        │ pq       *pq.Error{Code, Constraint, Detail}      │
        │ pgx      *pgconn.PgError{Code, ConstraintName}    │
        │ mysql2   err.errno, err.sqlState, err.sqlMessage  │
        │ Prisma   err.code = P2002 | P2003 | P2011 …       │
        └───────────────────────────┬───────────────────────┘
                                    ▼
                    DbFailure { code, class, constraint,
                                table, column, detail, cause }
                                    ▼
                     one classifier → application error
```

## How it works (mechanics)

### Postgres / node-pg (TypeScript)

The `pg` driver copies server error fields onto the `DatabaseError`: `code` (SQLSTATE),
`severity`, `detail`, `hint`, `position`, `internalPosition`, `internalQuery`, `where`,
`schema`, `table`, `column`, `dataType`, `constraint`, `file`, `line`, `routine`.

```ts
import type { DatabaseError } from "pg";

function fromPg(err: DatabaseError) {
  return {
    code: err.code,                 // "23505"
    cls: err.code?.slice(0, 2),     // "23"
    constraint: err.constraint,     // "projects_slug_key" (server-side only)
    table: err.table,
    column: err.column,
    detail: err.detail,             // may contain user data → never expose
    cause: err,
  };
}
```

> ⚠️ **Hazard.** `err.detail` often contains the actual conflicting value
> (`Key (email)=(a@b.com) already exists.`). It is PII. Log a hash or the constraint name, never
> the detail, and never put it in an API response.

### Postgres / Python (psycopg2)

psycopg2 puts the SQLSTATE in `pgcode` and structured fields in `diag`:
`diag.constraint_name`, `diag.table_name`, `diag.column_name`, `diag.message_primary`,
`diag.message_detail`. Subclasses in `psycopg2.errors` (e.g. `UniqueViolation`) are convenient
but **version- and import-sensitive**; `pgcode` is the stable key.

```python
import psycopg2
from psycopg2 import errors

def from_psycopg(exc: BaseException):
    state = getattr(exc, "pgcode", None)
    diag = getattr(exc, "diag", None)
    return {
        "code": state,
        "cls": state[:2] if state else None,
        "constraint": getattr(diag, "constraint_name", None),
        "table": getattr(diag, "table_name", None),
        "column": getattr(diag, "column_name", None),
        "is_unique": isinstance(exc, errors.UniqueViolation),  # optional refinement
        "cause": exc,
    }
```

### Postgres / Go (`pq` and `pgx`)

```go
// lib/pq
var pqErr *pq.Error
if errors.As(err, &pqErr) {
    _ = pqErr.Code      // pq.ErrorCode, a string like "23505"
    _ = pqErr.Constraint
    _ = pqErr.Table
    _ = pqErr.Column
}

// jackc/pgx v5
var pgErr *pgconn.PgError
if errors.As(err, &pgErr) {
    _ = pgErr.Code            // SQLSTATE
    _ = pgErr.ConstraintName
    _ = pgErr.TableName
    _ = pgErr.ColumnName
    _ = pgErr.Detail
}
```

Always use `errors.As` (not a type assertion) so wrapped errors still match.

### MySQL (`mysql2`, Connector/Python, go-sql-driver)

MySQL exposes **both** `sqlState` and a numeric `errno`; the `errno` is the discriminating one.

| errno | SQLSTATE | Symbol | Meaning |
| ----- | -------- | ------ | ------- |
| `1062` | `23000` | `ER_DUP_ENTRY` | duplicate key |
| `1451` | `23000` | `ER_ROW_IS_REFERENCED_2` | delete/update blocked by child row |
| `1452` | `23000` | `ER_NO_REFERENCED_ROW_2` | insert/update missing parent |
| `1048` | `23000` | `ER_BAD_NULL_ERROR` | column cannot be null |
| `3819` | `HY000` | `ER_CHECK_CONSTRAINT_VIOLATED` | check constraint (8.0.16+) |
| `1213` | `40001` | `ER_LOCK_DEADLOCK` | deadlock; **whole txn rolled back** |
| `1205` | `HY000` | `ER_LOCK_WAIT_TIMEOUT` | lock wait timeout; statement rolled back |
| `1040` | `08004` | `ER_CON_COUNT_ERROR` | too many connections |
| `2006` | `HY000` | `CR_SERVER_GONE_ERROR` | server gone away |
| `2013` | `HY000` | `CR_SERVER_LOST` | lost connection during query |
| `1146` | `42S02` | `ER_NO_SUCH_TABLE` | table missing |
| `1054` | `42S22` | `ER_BAD_FIELD_ERROR` | unknown column |
| `3024` | `HY000` | `ER_QUERY_TIMEOUT` | `max_execution_time` exceeded |

```ts
// mysql2
import type { QueryError } from "mysql2";

function fromMySQL(err: QueryError) {
  return {
    code: String(err.errno),        // "1062" — key on this, not the message
    sqlState: err.sqlState,         // "23000" — class is coarse
    cls: err.sqlState?.slice(0, 2),
    constraint: undefined,          // parse from err.sqlMessage if you must
    cause: err,
  };
}
```

### ORM codes (Prisma and friends)

ORMs collapse vendor detail into their own codes. That is convenient but **lossy** — you lose
the constraint name and sometimes the retry class.

| Prisma | Meaning | Maps to |
| ------ | ------- | ------- |
| `P2002` | unique constraint failed | `ALREADY_EXISTS` |
| `P2003` | foreign key constraint failed | `REFERENCE_MISSING` |
| `P2004` | check constraint failed | `BUSINESS_RULE_VIOLATION` |
| `P2011` | null constraint violation | `REQUIRED_FIELD_MISSING` |
| `P2025` | record to update/delete not found | `NOT_FOUND` / stale write |
| `P1001` | cannot reach database server | `DB_UNAVAILABLE` (transient) |
| `P1008` | operations timed out | `DB_TIMEOUT` (ambiguous for writes) |
| `P2024` | timed out fetching a connection from pool | `POOL_EXHAUSTED` |

## Worked example

```python
# One normalization entry point used by every repository.
from dataclasses import dataclass

@dataclass(frozen=True)
class DbFailure:
    code: str | None
    cls: str | None
    constraint: str | None
    table: str | None
    column: str | None
    cause: BaseException

def normalize(exc: BaseException) -> DbFailure:
    if hasattr(exc, "pgcode"):                        # psycopg2
        d = getattr(exc, "diag", None)
        return DbFailure(exc.pgcode, (exc.pgcode or "")[:2],
                         getattr(d, "constraint_name", None),
                         getattr(d, "table_name", None),
                         getattr(d, "column_name", None), exc)
    if hasattr(exc, "errno"):                         # mysql-connector
        return DbFailure(str(exc.errno), exc.sqlstate[:2] if exc.sqlstate else None,
                         None, None, None, exc)
    if hasattr(exc, "code"):                          # Prisma-ish / node-pg
        return DbFailure(exc.code, str(exc.code)[:2],
                         getattr(exc, "constraint", None),
                         getattr(exc, "table", None),
                         getattr(exc, "column", None), exc)
    return DbFailure(None, None, None, None, None, exc)
```

`normalize()` is the **only** function that names a driver field. Everything above it consumes
`DbFailure`.

## Key data / numbers

- node-pg: `code`, `constraint`, `table`, `column`, `detail`, `schema`, `routine`.
- psycopg2: `pgcode`, `diag.constraint_name`, `diag.table_name`, `diag.column_name`.
- `pq`: `*pq.Error{Code, Constraint, Table, Column}`; pgx: `*pgconn.PgError{Code,
  ConstraintName, TableName, ColumnName}`.
- MySQL `1062` duplicate, `1452` missing parent, `1213` deadlock, `1205` lock wait, `1040`
  too many connections, `2006`/`2013` connection loss.
- Prisma `P2002` unique, `P2003` FK, `P2011` null, `P2025` not found, `P1001` unreachable.
- **`error.code` is overloaded**: in node-pg it is `SQLSTATE`; in Node's `fs` it is `ENOENT`;
  in Prisma it is `P2002`. Always check the driver/type before reading it.

## Real-world use case — Acme SaaS

Acme standardized on node-pg, then added a Prisma service for internal admin tooling. The shared
`translate()` function read `err.code.slice(0, 2)` — fine for `23505`, but Prisma's `P2002`
became class **`P2`**, fell through to `DB_UNKNOWN`, and returned `500` for every duplicate
admin action. Introducing `normalize()` with a Prisma branch (`P2002` → `ALREADY_EXISTS`) fixed
admin tooling without touching the API service. The lesson: **normalize per driver, classify
once.**

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Raw driver checks in each repository | no abstraction | duplicated, drifts | one driver, two queries |
| Shared `normalize()` per driver | one place to fix, testable | small adapter layer | default for multi-driver apps |
| ORM codes only | portable, simple | lossy, vendor detail gone | ORM-only, no raw SQL |
| Parse `sqlMessage` text | works when no field exists | brittle, locale-sensitive | last resort, with tests |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Normalize into one `DbFailure` shape | Let `err.code` mean five things across modules |
| Use `errors.As` / `isinstance` for wrapping | Type-assert and drop wrapped errors |
| Read MySQL `errno` before `sqlState` | Treat all `23000` as duplicates |
| Treat ORM `P1001`/`P2024` as transient | Retry `P2002` |
| Keep `detail`/`sqlMessage` server-side | Return them to clients |

## Common mistakes

- **Keying on the exception class name** (`UniqueViolation`) — renamed/moved between versions.
- **Assuming `err.code` is a SQLSTATE everywhere** — Prisma and Node core also use `code`.
- **Losing the cause** when wrapping into `DbFailure` — always carry `cause`.
- **Parsing constraint names out of MySQL messages** without a fallback — messages vary.
- **Treating ORM `P2025` as success** — a missing row on update is usually a stale write.

## Checklist

- [ ] One `normalize()` per driver, one classifier above it.
- [ ] `DbFailure` carries code, class, constraint, table, column, and cause.
- [ ] MySQL classification keys on `errno`, not `sqlState` alone.
- [ ] ORM codes have their own branch with documented mappings.
- [ ] No driver type escapes the persistence adapter.

## Related

- [The SQLSTATE Classification Table](./01-sqlstate-classification-table.md)
- [SQLSTATE → Domain Error Mapping](../03-practical-examples/01-sqlstate-to-domain-error-mapping.md)
- [Repository Translating Persistence Errors](../../24-repository-and-data-access-error-handling/03-practical-examples/01-repository-translating-persistence-errors.md)
- [Framework and Runtime Integration (48.6 ORM mapping)](../../../part-18-languages-and-frameworks/48-framework-and-runtime-integration/README.md)
