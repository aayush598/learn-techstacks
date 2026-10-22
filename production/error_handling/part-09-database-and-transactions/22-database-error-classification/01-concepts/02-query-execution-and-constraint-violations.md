# Query Execution and Constraint Violations (22.3–22.8)

> Part IX · Chapter 22 · Sections 22.3–22.8 · _Estimated reading time: 22 min_
> **Prerequisite:** [Connection and Pool Errors](./01-connection-and-pool-errors.md)

## In one sentence

A constraint violation is **the database enforcing your own declared rules** — `23505` unique,
`23503` foreign key, `23502` not-null, `23514` check — so it is a **permanent, meaningful answer**
about the data, not a transient system failure.

## Why this matters in production

Constraint errors are the highest-volume database errors in a SaaS product and the ones most
often mis-handled. Mapping all of `IntegrityError` to `500` tells a user "something broke" when
they simply double-submitted a form; retrying `23505` creates duplicate invoices; treating
`23503` as a crash hides a stale UI that referenced a deleted project. Because class **`23`**
errors carry **business meaning**, your handler must extract that meaning — which column, which
constraint, which rule — and translate it, not suppress it.

## Core concept

### 22.3 Query execution

"Query execution" is the broad bucket: anything raised while running a statement. Split it by
what actually happened:

| Sub-class | Example | SQLSTATE / errno | Outcome |
| --------- | ------- | ---------------- | ------- |
| Syntax / reference | table or column renamed | `42601`, `42703`, `42P01`; MySQL `1064`, `1054`, `1146` | permanent, **alert** (deploy fault) |
| Data type / value | `"abc"` into an integer, value too long | `22002`, `22003`, `22001`, `22P02`; MySQL `1265`, `1406` | permanent, usually **validation** |
| Constraint | see below | class **`23`**; MySQL `1062`, `1452`, `1048`, `3819` | permanent, **translate** |
| Permission | role lost a grant | `42501`; MySQL `1142` | permanent, **alert** (config) |
| Timeout | statement ran too long | `57014`; MySQL `3024` | transient-ish, retry selectively |

### 22.4–22.8 The class `23` family

```sql
-- Acme SaaS schema: the four violations in one place
CREATE TABLE projects (
  id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  tenant_id   bigint NOT NULL,                              -- 23502 if NULL
  slug        text   NOT NULL UNIQUE,                       -- 23505 on duplicate
  budget      numeric CHECK (budget >= 0),                  -- 23514 on negative
  owner_id    bigint REFERENCES users(id)                   -- 23503 on missing user
);
```

| § | Violation | Postgres SQLSTATE | MySQL errno / SQLSTATE | What it usually means |
| - | --------- | ----------------- | ---------------------- | ---------------------- |
| 22.5 | **unique** | `23505` | `1062` / `23000` | duplicate submission, replayed webhook, idempotency hit |
| 22.6 | **foreign key** | `23503` | `1452` / `23000` | parent missing (stale read, deleted row, wrong tenant id) |
| 22.7 | **not-null** | `23502` | `1048` / `23000` | skipped required field — usually a **bug** if you pre-validated |
| 22.8 | **check** | `23514` | `3819` (MySQL 8.0.16+) / `23000` | business rule at the storage layer |

Reverse FK errors matter too: MySQL **`1451`** ("cannot delete a parent row") fires when you
delete something other rows still reference.

## How it works (mechanics)

1. The statement runs; the **first** violated row aborts the whole statement in Postgres
   (`CURRENT_QUERY` stops; the transaction enters **failed state** — `25P02`
   `in_failed_sql_transaction` if you keep issuing statements).
2. The driver raises an exception carrying **`SQLSTATE` + constraint identity**:
   - Postgres reports `Constraint: projects_slug_key`, `DETAIL: Key (slug)=(acme) already
     exists.`, and `COLUMN`/`TABLE` in the error fields.
   - MySQL reports `errno=1062`, `sqlState=23000`, and a message containing the index name.
3. Your **only** layer that reads those fields (the repository) maps them to a domain error,
   including `details.field` derived from the constraint — **without emitting the index name**.
4. Because class `23` is permanent, the retry policy must be **no** — except the deliberate
   idempotent-replay case for `23505` (see worked example).

> ⚠️ **Hazard.** In Postgres, after a class-`23` error inside a transaction, **every following
> statement fails with `25P02`** until you `ROLLBACK` (or issue a `SAVEPOINT`-based recovery).
> Code that catches and continues issuing queries produces baffling "`25P02` in failed
> transaction" errors that look like a second bug.

## Worked example

```python
# psycopg2: extracting meaning, never the raw message
FIELD_BY_CONSTRAINT = {
    "projects_slug_key": "slug",
    "projects_owner_id_fkey": "ownerId",
}

def translate_integrity(exc, *, resource: str):
    state = getattr(exc, "pgcode", None)
    diag = getattr(exc, "diag", None)
    constraint = getattr(diag, "constraint_name", None) if diag else None
    field = FIELD_BY_CONSTRAINT.get(constraint)

    if state == "23505":
        # Deliberate idempotency: WebhookIngest replays are SUCCESS, not 409.
        return DomainError("ALREADY_EXISTS", field=field, transient=False, http=409, cause=exc)
    if state == "23503":
        return DomainError("REFERENCE_MISSING", field=field, transient=False, http=422, cause=exc)
    if state == "23502":
        # Pre-validated input hitting NOT NULL = programming fault → alert.
        return DomainError("REQUIRED_FIELD_MISSING", field=field, transient=False,
                           http=422, alert=(resource != "internal_job"), cause=exc)
    if state == "23514":
        return DomainError("BUSINESS_RULE_VIOLATION", field=field, transient=False,
                           http=422, cause=exc)
    return DomainError("DATA_INTEGRITY", transient=False, http=500, alert=True, cause=exc)
```

```text
Duplicate invitation POST /projects/42/invitations {email:"a@b.com"}
  → 23505, constraint invitations_project_id_email_key
  → DomainError ALREADY_EXISTS {field:"email"}, transient=false
  → HTTP 409 + field detail          (NOT 500, NOT retried)
Deleted project while a job references it
  → 23503, constraint export_jobs_project_id_fkey
  → REFERENCE_MISSING → HTTP 404/422 for users; for ExportJob → skip item, record reason
```

## Key data / numbers

- Class **`23505`** unique, **`23503`** FK, **`23502`** not-null, **`23514`** check — all
  **permanent, not retryable**.
- MySQL: **`1062`** duplicate entry, **`1452`** no referenced row (insert), **`1451`** referenced
  row (delete), **`1048`** column cannot be null, **`3819`** check violated (8.0.16+),
  **`1265`/`1406`** data truncated / data too long.
- Prisma (if you use it): **`P2002`** unique, **`P2003`** FK, **`P2011`** null constraint,
  **`P2004`** check, **`P2025`** record not found.
- Postgres aborts the **entire statement** on the first violating row — multi-row inserts are
  all-or-nothing unless you use savepoints (Chapter 23).
- `ON CONFLICT DO NOTHING/DO UPDATE` (Postgres) and `INSERT IGNORE` (MySQL) turn the unique
  race into a normal path — but `INSERT IGNORE` swallows *more* than duplicates; prefer
  `ON CONFLICT` or upsert semantics you can see.

## Real-world use case — Acme SaaS

`WebhookIngest` processes Stripe webhooks. Stripe delivers `invoice.paid` at-least-once, so the
first design recorded each event id in a `webhook_events` table — and any duplicate raised
`23505`, which the generic handler turned into a `500`. Stripe retried on every `500`, so one
duplicate became **dozens of retries**, each `500`ing, until the endpoint risked being disabled.
After classification, `23505` on the **idempotency table** is recognized as *already processed*
and returns `200` with the stored outcome; `23505` on business tables is `409`. Duplicate
processing dropped to zero, and the retry budget stopped burning on events that were already
applied.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Fail with `409`/`422` | honest, safe | client must react | default for constraint errors |
| Upsert (`ON CONFLICT`) | race becomes routine | hides intent; needs a payload-equality check | creation flows with idempotency |
| Treat `23505` as success | perfect for replays | wrong if payload differs | **only** when the row is the idempotency record |
| Validate before insert | better messages | duplicate work; race still possible | UX-critical fields |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Map `23505`→conflict, `23503`→reference, `23502`/`23514`→validation | Raise one `IntegrityError` → `500` |
| Mark all class `23` non-retryable | Retry a unique violation |
| Use constraint identity to pick `details.field` | Put the index name in the response |
| Roll back (or savepoint) after a class-`23` error | Keep issuing statements in the failed transaction |
| Alert when pre-validated input hits `23502` | Assume not-null always means user error |

## Common mistakes

- **`500` for every `IntegrityError`** — converts routine duplicates into fake outages.
- **Retrying `23505` "because inserts are idempotent"** — they are not; you get duplicates or a
  permanent loop.
- **Exposing `DETAIL: Key (slug)=(acme) already exists.`** — leaks schema and user data.
- **Ignoring `25P02`** — the secondary error masks the real one.
- **Treating `23503` as an internal crash** — it usually means stale UI or a deleted parent.

## Checklist

- [ ] Each class-`23` code maps to its own application error code.
- [ ] Constraint names/`DETAIL` never leave the persistence layer.
- [ ] Retry policy explicitly marks class `23` as permanent.
- [ ] Replayed webhooks use `23505` (or a dedicated table) as their duplicate detector.
- [ ] Post-`23` transactions roll back before anything else runs.

## Related

- [Conflicts, Locks, and Timeouts (22.9–22.13)](./03-conflicts-locks-and-timeouts.md)
- [SQLSTATE → Domain Error Mapping](../03-practical-examples/01-sqlstate-to-domain-error-mapping.md)
- [Repository CRUD Failure Semantics](../../24-repository-and-data-access-error-handling/01-concepts/03-crud-failure-semantics.md)
- [Chapter 22 Do's and Don'ts](../04-dos-and-donts/README.md)
