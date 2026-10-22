# Mapping Persistence to Application Errors (24.3, 24.12, 24.13)

> Part IX · Chapter 24 · Sections 24.3, 24.12, 24.13 · _Estimated reading time: 20 min_
> **Prerequisite:** [Repository Responsibilities and the Domain Boundary](./01-repository-responsibilities-and-domain-boundary.md)

## In one sentence

Translation is a **lossy-by-design** operation: keep the facts that drive decisions (`code`,
`category`, `transient`, `field`, `cause`) and **drop the dialect** (`SQLSTATE` text, constraint
names, SQL) — while avoiding one generic error that erases all of them.

## Why this matters in production

The mapping is where a `409` is chosen over a `500`, where a deadlock becomes an invisible retry
instead of an outage, and where a stale client learns which field collided. Get it wrong in the
"generic" direction and every failure looks the same; get it wrong in the "leaky" direction and
your API publishes your schema. Neither is recoverable later: clients build on whatever you
return, so the shape you choose now becomes a contract.

## Core concept

### 24.3 The mapping rules

| Persistence fact | Keep as | Drop |
| ---------------- | ------- | ---- |
| SQLSTATE / errno | a stable app `code` (derived) | the raw code |
| Constraint name | `field` (allowlist lookup) | the index name |
| SQL text / `DETAIL` | `cause` (server log only) | API body |
| Retry class | `transient`, `retryScope` | driver-specific retry hints |
| Transaction state | `retryScope` | raw `25P02` strings |
| Table/column | `resource`/`op` label | schema identifiers |
| Ambiguity | `unknown` outcome | "connection reset" |

Three rules:

1. **Every code maps to a category** (`CONFLICT`, `VALIDATION`, `DEPENDENCY`, `INTERNAL`).
2. **Every error carries `transient` and `retryScope`** so retry needs no driver knowledge.
3. **Every error carries `cause`** so logs retain the full server truth.

### 24.12 Why generic repository errors hurt

```ts
// The anti-pattern
class RepositoryError extends Error {}

async function save(x) {
  try { return await db.insert(x); }
  catch (e) { throw new RepositoryError("database error"); }
}
```

| Caller question | With `RepositoryError` | With a translated error |
| --------------- | ---------------------- | ----------------------- |
| Is this retryable? | unknown → probably not | `transient` says yes/no |
| Which HTTP status? | `500` for everything | `409`/`422`/`503` |
| Which field? | unknown | `field: "email"` |
| Should on-call page? | every time | only `INTERNAL`/`SCHEMA` |
| Duplicate or outage? | indistinguishable | distinct codes |

A generic error is not "abstract"; it is **information destruction**. The caller is forced to
either page on everything or retry everything.

### 24.13 Preserving failure metadata

Minimum metadata on every repository error:

```ts
type RepoError = {
  code: string;                 // stable app code, e.g. CONFLICT
  category: string;             // CONFLICT | VALIDATION | DEPENDENCY | INTERNAL
  transient: boolean;           // retry with backoff?
  retryScope: "none" | "statement" | "transaction";
  alert: boolean;               // page a human?
  safeMessage: string;          // user-safe, no internals
  field?: string;               // public field name, not constraint
  op: string;                   // "projects.insert"
  resource: string;             // "projects"
  cause: unknown;               // ORIGINAL driver error (server-side only)
};
```

`cause` is the single most valuable field: it turns a production error log from "CONFLICT" into
`23505 on projects_slug_key`, without exposing either to the client.

## How it works (mechanics)

```text
driver error
  → normalize()        code, class, constraint, table, column, cause
  → mapConstraint()    constraint → public field (allowlist)
  → classify()         class → category/transient/retryScope/alert
  → translate()        construct RepoError, attach cause + op
  → service            decides retry/translate-to-domain
  → controller         decides HTTP + body
```

The mapping table should be **declarative** so it can be tested row by row (see Chapter 22's
practical example). Avoid a `switch` that mixes mapping and business decisions.

## Worked example

```python
# Mapping a single insert, with metadata preserved end to end.
def insert_project(tx, project) -> Project:
    try:
        row = tx.execute(
            """INSERT INTO projects (tenant_id, slug, budget, owner_id)
               VALUES (%s, %s, %s, %s) RETURNING id, tenant_id, slug, budget""",
            (project.tenant_id, project.slug, project.budget, project.owner_id),
        ).fetchone()
        return Project(**row)
    except DriverError as exc:
        db = normalize(exc)
        if db.code == "23505":
            raise RepoError(
                code="CONFLICT",
                category="CONFLICT",
                transient=False,
                retry_scope="none",
                alert=False,
                safe_message="That value is already taken.",
                field=FIELD_BY_CONSTRAINT.get(db.constraint),   # "slug"
                op="projects.insert",
                resource="projects",
                cause=exc,                                      # preserved
            )
        if db.code == "23503":
            raise RepoError(code="REFERENCE_MISSING", category="VALIDATION",
                            transient=False, retry_scope="none", alert=False,
                            safe_message="A referenced record does not exist.",
                            field=FIELD_BY_CONSTRAINT.get(db.constraint),
                            op="projects.insert", resource="projects", cause=exc)
        raise translate(db, op="projects.insert", resource="projects")
```

```text
API response (safe):
  409 { "title": "CONFLICT", "detail": "That value is already taken.",
        "errors": { "field": "slug" } }
Server log (full):
  err.code=CONFLICT op=projects.insert cause=PgError(SQLSTATE=23505,
  constraint=projects_slug_key, detail="Key (slug)=(acme) already exists.")
```

## Key data / numbers

- Keep the public surface to **one shape**; every repository returns the same `RepoError` type.
- `field` comes from an **allowlist** — if a constraint is unknown, omit `field` rather than
  leaking the name.
- Preserve `cause` on **100%** of translated errors; it is the only link back to `SQLSTATE`.
- `op` labels should be stable (`resource.action`) so metrics can group by operation.
- Never include `detail`, `sql`, `table`, or `column` in `safeMessage`.

## Real-world use case — Acme SaaS

Acme's `InvitationRepository` threw `RepositoryError("database error")` for everything. The
service mapped it to `500`, so duplicate invitations (a `23505`) looked like outages; on-call
paged for user double-clicks, and the frontend could not highlight the email field. Replacing the
generic error with `CONFLICT { field: "email", transient: false }` changed the API to `409` with a
field hint, removed the pages, and let the invitation modal show "already invited" inline. The
same change preserved `cause`, so the next schema incident was still diagnosable from logs.

## Trade-offs

| Mapping style | Pros | Cons | When to use |
| ------------- | ---- | ---- | ----------- |
| One generic error | tiny code | destroys all decisions | prototypes |
| Domain errors directly from repo | fewer types | couples repo to domain | small DDD apps |
| Application error + metadata | stable, testable | one extra type | default |
| Raw driver passthrough | zero work | leaks + unstable | never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Map every code to a category | Throw one `RepositoryError` for all |
| Attach the original `cause` | Reconstruct an error without it |
| Use an allowlist for `field` | Echo the constraint name |
| Keep `safeMessage` free of internals | Include `DETAIL` or SQL |
| Keep `op`/`resource` on the error | Log without operation context |

## Common mistakes

- **Generic error with a nice message** — still loses retry/status decisions.
- **Including the raw message as `safeMessage`** — Postgres messages contain user data.
- **Mapping to HTTP inside the repository** — couples persistence to transport.
- **Dropping `cause` "to keep the error clean"** — makes incidents undebuggable.
- **Mapping unknown constraints to `field: constraint`** — leaks schema.

## Checklist

- [ ] One `RepoError` shape across all repositories.
- [ ] Every error has code, category, transient, retryScope, alert, message.
- [ ] `field` comes from an allowlist.
- [ ] `cause` is always attached and never serialized to clients.
- [ ] `op`/`resource` labels are stable and used in metrics.

## Related

- [CRUD Failure Semantics (24.4–24.8)](./03-crud-failure-semantics.md)
- [Leak Prevention and Metadata Preservation](../02-deep-dive/01-leak-prevention-and-metadata-preservation.md)
- [SQLSTATE → Domain Error Mapping (Ch. 22)](../../22-database-error-classification/03-practical-examples/01-sqlstate-to-domain-error-mapping.md)
- [Chapter 24 Do's and Don'ts](../04-dos-and-donts/README.md)
