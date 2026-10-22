# SQLSTATE → Domain Error Mapping

> Part IX · Chapter 22 · Sections 22.4–22.6, 22.9, 22.20 · _Estimated reading time: 25 min_
> **Prerequisite:** [The SQLSTATE Classification Table](../02-deep-dive/01-sqlstate-classification-table.md)

## In one sentence

This is a **complete, testable mapping module**: raw driver error → normalized `DbFailure` →
domain error with `code`, `category`, `transient`, `retryScope`, `http`, `alert`, and a
constraint-to-field table — the only code in the service that knows `SQLSTATE`.

## Why this matters in production

A mapping table is not documentation; it is **executable policy**. When it lives in one module
with tests, a new status code or a new SQLSTATE is a one-line change reviewed once. When it is
scattered across handlers, the same error gets a `409` in one endpoint and a `500` in another,
retry behavior diverges between `Checkout` and `ExportJob`, and nobody can answer "what happens
when `23503` fires?" without grepping.

## The pipeline

```text
driver error
  │  normalize per driver (node-pg / psycopg2 / pq / mysql2)
  ▼
DbFailure { code, class, constraint, table, column, cause }
  │  classify (class-first, subclass overrides)
  ▼
DomainError { code, category, transient, retryScope, http, alert, field, cause }
  │  map to transport at the request boundary
  ▼
HTTP response (Problem-style) + server-side log with cause
```

Only **hop 1** reads driver fields. Only **hop 2** reads `SQLSTATE`. Only **hop 4** decides
status text. See [Chapter 16](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/03-practical-examples/01-postgres-sqlstate-to-domain-to-http.md)
for the transport half.

## The table

| SQLSTATE / errno | Domain code | Category | Transient | Retry scope | HTTP | Alert |
| ---------------- | ----------- | -------- | --------- | ----------- | ---- | ----- |
| `23505` / `1062` | `ALREADY_EXISTS` | CONFLICT | no | none | `409` | no |
| `23503` / `1452` | `REFERENCE_MISSING` | VALIDATION | no | none | `422` | no |
| `23503` / `1451` (delete) | `RESOURCE_IN_USE` | CONFLICT | no | none | `409` | no |
| `23502` / `1048` | `REQUIRED_FIELD_MISSING` | VALIDATION | no | none | `422` | pre-validated? yes |
| `23514` / `3819` | `BUSINESS_RULE_VIOLATION` | VALIDATION | no | none | `422` | no |
| `40001` | `RETRYABLE_CONFLICT` | CONCURRENCY | yes | **transaction** | `409` after exhaustion | no |
| `40P01` / `1213` | `RETRYABLE_CONFLICT` | CONCURRENCY | yes | **transaction** | `409` after exhaustion | no |
| `55P03` / `1205` | `LOCK_TIMEOUT` | CONCURRENCY | yes | transaction | `409`/`503` | no |
| `57014` / `3024` | `QUERY_TIMEOUT` | DEPENDENCY | yes* | statement | `504` | no |
| `08006` / `2013` | `DB_UNAVAILABLE` | DEPENDENCY | yes | transaction | `503` | sustained |
| `53300` / `1040` | `DB_AT_CAPACITY` | CAPACITY | yes | transaction | `503` | sustained |
| `57P03` / `57P01` | `DB_UNAVAILABLE` | DEPENDENCY | yes | transaction | `503` | no |
| `25006` / `1290` | `DB_READ_ONLY` | ROUTING | yes | transaction | `503` | no |
| `42P01` / `1146` | `SCHEMA_MISMATCH` | INTERNAL | no | none | `500` | **yes** |
| `42703` / `1054` | `SCHEMA_MISMATCH` | INTERNAL | no | none | `500` | **yes** |
| `42601` / `1064` | `SCHEMA_MISMATCH` | INTERNAL | no | none | `500` | **yes** |
| `42501` / `1142` | `DB_PERMISSION` | CONFIG | no | none | `500` | **yes** |
| `28P01` / `1045` | `DB_AUTH_FAILED` | CONFIG | no | none | `500` | **yes** |
| `XX001`, `XX002`, `58P01` | `DATA_CORRUPTION` | CORRUPTION | no | none | `503` | **yes** |
| unknown | `DB_UNKNOWN` | INTERNAL | no | none | `500` | **yes** |

\* `57014` is retryable only if the deadline was short; retrying a genuinely expensive query
repeats the timeout. Treat it as transient for the *request*, permanent for the *query shape*.

## Worked example (Python, psycopg2)

### Step 1 — normalize + classify

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class DomainError(Exception):
    code: str
    category: str
    http: int
    transient: bool
    retry_scope: str          # "none" | "statement" | "transaction"
    safe_message: str
    alert: bool = False
    field: Optional[str] = None
    cause: Optional[BaseException] = None
    metadata: dict = field(default_factory=dict)


FIELD_BY_CONSTRAINT = {
    # constraint identity → public field name. Never expose the index name.
    "users_email_key": "email",
    "projects_slug_key": "slug",
    "invitations_project_id_email_key": "email",
    "export_jobs_project_id_fkey": "projectId",
}

# (code, action) where action is one of the four outcomes below.
FOUR_OH_NINE = lambda field, msg: ("ALREADY_EXISTS", "CONFLICT", 409, False, "none", msg, False, field)
VALIDATION  = lambda field, msg: ("VALIDATION", "VALIDATION", 422, False, "none", msg, False, field)


def classify(db, *, resource: str) -> DomainError:
    state = db.code
    field_name = FIELD_BY_CONSTRAINT.get(db.constraint or "")

    if state == "23505":
        code, cat, http, trans, scope, msg, alert, f = FOUR_OH_NINE(
            field_name, "That value already exists.")
    elif state == "23503":
        deleting = resource.endswith(":delete")
        code, cat, http, trans, scope, msg, alert, f = (
            ("RESOURCE_IN_USE", "CONFLICT", 409, False, "none",
             "This record is still referenced.", False, None) if deleting else
            ("REFERENCE_MISSING", "VALIDATION", 422, False, "none",
             "A referenced record does not exist.", False, field_name))
    elif state == "23502":
        code, cat, http, trans, scope, msg, alert, f = (
            "REQUIRED_FIELD_MISSING", "VALIDATION", 422, False, "none",
            "A required field is missing.", resource.startswith("internal:"), field_name)
    elif state == "23514":
        code, cat, http, trans, scope, msg, alert, f = (
            "BUSINESS_RULE_VIOLATION", "VALIDATION", 422, False, "none",
            "The value violates a business rule.", False, field_name)
    elif state in ("40001", "40P01"):
        code, cat, http, trans, scope, msg, alert, f = (
            "RETRYABLE_CONFLICT", "CONCURRENCY", 409, True, "transaction",
            "A concurrent update occurred; retry.", False, None)
    elif state == "55P03":
        code, cat, http, trans, scope, msg, alert, f = (
            "LOCK_TIMEOUT", "CONCURRENCY", 409, True, "transaction",
            "The record is busy; retry.", False, None)
    elif state in ("08006", "08003", "57P03", "57P01"):
        code, cat, http, trans, scope, msg, alert, f = (
            "DB_UNAVAILABLE", "DEPENDENCY", 503, True, "transaction",
            "The database is temporarily unavailable.", False, None)
    elif state == "53300":
        code, cat, http, trans, scope, msg, alert, f = (
            "DB_AT_CAPACITY", "CAPACITY", 503, True, "transaction",
            "The database is at capacity.", False, None)
    elif state in ("42P01", "42703", "42601", "42501"):
        code, cat, http, trans, scope, msg, alert, f = (
            "SCHEMA_MISMATCH", "INTERNAL", 500, False, "none",
            "An unexpected error occurred.", True, None)
    elif state in ("XX001", "XX002", "58P01"):
        code, cat, http, trans, scope, msg, alert, f = (
            "DATA_CORRUPTION", "CORRUPTION", 503, False, "none",
            "The data store is unavailable.", True, None)
    else:
        code, cat, http, trans, scope, msg, alert, f = (
            "DB_UNKNOWN", "INTERNAL", 500, False, "none",
            "An unexpected error occurred.", True, None)

    return DomainError(code=code, category=cat, http=http, transient=trans,
                       retry_scope=scope, safe_message=msg, alert=alert,
                       field=f, cause=db.cause,
                       metadata={"resource": resource})
```

### Step 2 — call sites stay boring

```python
def insert_project(repo, project, resource="projects:create"):
    try:
        return repo.insert(project)
    except DriverError as exc:
        raise classify(normalize(exc), resource=resource)
```

### Step 3 — SQL that produces each row (for tests)

```sql
-- 23505
INSERT INTO projects (tenant_id, slug, budget, owner_id)
VALUES (1, 'acme', 100, 7), (1, 'acme', 100, 7);
-- 23503
INSERT INTO projects (tenant_id, slug, budget, owner_id)
VALUES (1, 'beta', 100, 999999);
-- 23514
INSERT INTO projects (tenant_id, slug, budget, owner_id)
VALUES (1, 'gamma', -1, 7);
-- 23502 (omit tenant_id)
INSERT INTO projects (slug, budget, owner_id) VALUES ('delta', 100, 7);
```

## MySQL variant

```ts
const MYSQL: Record<number, [string, string, number, boolean, string]> = {
  1062: ["ALREADY_EXISTS", "CONFLICT", 409, false, "none"],
  1452: ["REFERENCE_MISSING", "VALIDATION", 422, false, "none"],
  1451: ["RESOURCE_IN_USE", "CONFLICT", 409, false, "none"],
  1048: ["REQUIRED_FIELD_MISSING", "VALIDATION", 422, false, "none"],
  3819: ["BUSINESS_RULE_VIOLATION", "VALIDATION", 422, false, "none"],
  1213: ["RETRYABLE_CONFLICT", "CONCURRENCY", 409, true, "transaction"],
  1205: ["LOCK_TIMEOUT", "CONCURRENCY", 409, true, "transaction"],
  1040: ["DB_AT_CAPACITY", "CAPACITY", 503, true, "transaction"],
};
```

## Key data / numbers

- The mapping covers **20 rows**; production usually needs 12–15 of them.
- `retryScope` values: `none`, `statement`, **`transaction`** — only `40001`/`40P01`/`1213`
  require the whole transaction.
- Constraint→field map is **schema-owned**: update it in the same PR as the migration.
- `alert=true` only on `42xxx`, `XXxxx`, `58P01`, auth/permission, and unknown codes.
- Test matrix: **one test per row**, asserting `code`, `transient`, `http`, and `alert`.

## Real-world use case — Acme SaaS

Acme's `Checkout` and `ExportJob` each had their own `except IntegrityError` handler.
`Checkout` returned `409`, `ExportJob` retried, and the admin API returned `500` for identical
`23505`s. Consolidating on this module made the three paths agree: duplicates are
`ALREADY_EXISTS`/`409` everywhere, the export job stops retrying them, and the admin API stopped
paging on-call for a user double-click. The test suite now asserts the whole table, so adding a
new constraint forces a deliberate field mapping.

## Trade-offs

| Choice | Pros | Cons | When to use |
| ------ | ---- | ---- | ----------- |
| Data-driven table | testable, reviewable | less flexible per call | default |
| `if/elif` classifier | easy to add context | grows into a monster | small, <10 codes |
| Per-repository mapping | close to the query | duplicated policy | throwaway scripts |
| Map to HTTP directly | fewer hops | leaks transport into persistence | never in layered apps |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Map constraint → public field name | Return the constraint/index name |
| Keep the raw driver error as `cause` | Reconstruct a new error and drop the cause |
| Test every row with real SQL | Trust the table by inspection |
| Mark `23502` on pre-validated input as `alert` | Treat every not-null as user error |
| Return `409` after conflict retries exhaust | Return `500` for a deadlock |

## Common mistakes

- **Two classifiers** (API vs worker) that drift apart.
- **Mapping class `42` to `422`** because it "looks like validation".
- **Forgetting `retryScope`** and retrying a single statement inside an aborted transaction.
- **Exposing `detail`** from Postgres, which contains user-supplied values.
- **Not testing the unknown branch** — it is the one that alerts.

## Checklist

- [ ] One module owns the entire `SQLSTATE` → domain mapping.
- [ ] Every row has code, category, http, transient, retryScope, alert.
- [ ] Constraint→field table is updated with migrations.
- [ ] Tests execute real SQL for `23505`, `23503`, `23502`, `23514`, and `40001`.
- [ ] Unknown codes are permanent + alert + generic message.

## Related

- [Classifying Real Failures with the Cast](./02-classifying-real-failures-with-the-cast.md)
- [Driver and Vendor Error Shapes](../02-deep-dive/02-driver-and-vendor-error-shapes.md)
- [Retrying 40001 and 40P01 in Code](../../23-transaction-and-rollback-error-handling/03-practical-examples/01-retrying-40001-and-40p01.md)
- [Chapter 22 Reference](../05-reference/README.md)
