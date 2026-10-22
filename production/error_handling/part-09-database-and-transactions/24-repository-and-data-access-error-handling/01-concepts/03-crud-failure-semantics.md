# CRUD Failure Semantics (24.4–24.8)

> Part IX · Chapter 24 · Sections 24.4–24.8 · _Estimated reading time: 22 min_
> **Prerequisite:** [Mapping Persistence to Application Errors](./02-mapping-persistence-to-application-errors.md)

## In one sentence

A **zero-row result is data, not an exception**, and "missing" means different things per
operation: `null` for a lookup, a `404` for a required read, a conflict for an update that
matched no version, and a success for an idempotent delete.

## Why this matters in production

Most repository APIs conflate four outcomes: found, absent, failed, and conflicted. The result
is bugs like "deleting a already-deleted project returns `500`", "an update that matched zero
rows silently reports success", and "a query timeout is translated to `404`". Each of these is a
one-line distinction in the repository — and an incident if it is missing. This file fixes the
semantics for each CRUD operation.

## Core concept

| § | Operation | Outcome | Repository returns | Caller sees |
| - | --------- | ------- | ------------------ | ----------- |
| 24.4 | **Read (lookup)** | row absent | `null` | `404` only if the use case requires it |
| 24.4 | **Read (required)** | row absent | throw `NOT_FOUND` | `404` |
| 24.5 | **Missing vs failed** | no row | `null` | not an error |
| 24.5 | **Missing vs failed** | driver error | throw translated error | `500`/`503` |
| 24.6 | **Insert** | duplicate | throw `CONFLICT` | `409` (or replay-success) |
| 24.7 | **Update** | 0 rows matched | throw `CONFLICT`/`NOT_FOUND` | `409`/`404` |
| 24.7 | **Update** | version mismatch | throw `CONFLICT` | `409`/`412` |
| 24.8 | **Delete** | 0 rows | `false` (idempotent) | `204` |
| 24.8 | **Delete (required)** | 0 rows | throw `NOT_FOUND` | `404` |

The key design decision is **who declares absence an error**: the repository exposes the fact,
the **use case** declares the requirement.

### 24.4 Missing records

Two method shapes, deliberately:

```ts
findById(tx, id): Promise<Project | null>          // absence is a value
getById(tx, id): Promise<Project>                  // absence is NOT_FOUND
```

Do not make every `find` throw — that forces callers to catch for normal control flow. Do not
make every `find` return `null` — that pushes a null-check into every caller. Provide both names;
let the use case pick.

### 24.5 Missing vs failed query

```ts
// ❌ Conflates the three outcomes
async function find(id) {
  try {
    return (await db.query("... WHERE id=$1", [id])).rows[0];
  } catch {
    return null;                    // a timeout now looks like "not found"
  }
}
```

```ts
// ✅ Absent is null; failure throws
async function find(tx, id) {
  try {
    const row = await tx.maybeOne("... WHERE id=$1", [id]);
    return row ? toProject(row) : null;
  } catch (err) {
    throw translate(normalize(err), { op: "projects.find", resource: "projects" });
  }
}
```

This distinction is a **security** issue too: turning a database failure into `404` can hide
outages and leak existence semantics (see Chapter 35).

### 24.6 Duplicate inserts

| Situation | Correct outcome |
| --------- | --------------- |
| User submits the same create twice | `CONFLICT` (`409`) with `field` |
| Webhook replays an event | **success** (`200`) if the row is the dedupe record |
| Import contains duplicate rows | per-row rejection, not whole-batch failure |
| Idempotent create with a client key | return the existing row |

The repository should not decide which of these applies — it returns `CONFLICT` with the
constraint-derived `field` (and optionally the existing row for `ON CONFLICT` paths). The service
maps replay to success.

### 24.7 Failed updates

`UPDATE ... WHERE id=$1` returning `rowCount = 0` is **ambiguous**: the row may not exist, or it
may exist but not match the predicate (wrong version, wrong tenant, wrong state). Resolve it:

```sql
-- Return enough to distinguish the outcomes in one round trip.
UPDATE projects
   SET name = $1, version = version + 1
 WHERE id = $2 AND tenant_id = $3 AND version = $4
RETURNING id, version;
-- 0 rows: either absent, wrong tenant, or stale version → follow-up SELECT decides
```

| `rowCount` | Follow-up | Conclusion |
| ---------- | --------- | ---------- |
| 1 | — | updated |
| 0 | row exists, version differs | `CONFLICT` (`409`/`412`) |
| 0 | row exists, state disallows | `INVALID_STATE` (`409`) |
| 0 | row absent | `NOT_FOUND` (`404`) |
| 0 | wrong tenant | `NOT_FOUND` (do not leak existence) |

Never report `200 OK` for an update that matched nothing. That is the **silent lost update**.

### 24.8 Failed deletes

Deletes should be **idempotent by default**: deleting a row that is already gone is the desired
end state, not an error. Return `boolean` (or the deleted row):

```ts
deleteById(tx, id): Promise<boolean>          // false = nothing to delete, still success
deleteByIdOrFail(tx, id): Promise<void>       // NOT_FOUND if absent
```

Beware the reverse FK error (`23503` / MySQL `1451`): the delete failed because **another row
still references it**. That is a `409 RESOURCE_IN_USE`, not a `500` and not "not found".

## How it works (mechanics)

1. Repository issues the statement with **`RETURNING`** where supported (Postgres) so the
   outcome is known without a second query.
2. `rowCount`/`rows.length` is inspected and mapped to `absent` / `updated` / `conflict`.
3. Any driver exception is translated (Chapter 22) and thrown.
4. For deletes, a `23503`/`1451` is translated to `RESOURCE_IN_USE`.
5. The service decides whether absence is `404`, success, or a domain outcome.

## Worked example

```python
def update_project(tx, project_id, tenant_id, name, expected_version):
    row = tx.execute(
        """UPDATE projects
              SET name = %s, version = version + 1
            WHERE id = %s AND tenant_id = %s AND version = %s
        RETURNING id, version""",
        (name, project_id, tenant_id, expected_version),
    ).fetchone()
    if row:
        return row

    exists = tx.execute(
        "SELECT version FROM projects WHERE id = %s AND tenant_id = %s",
        (project_id, tenant_id),
    ).fetchone()
    if exists is None:
        raise NotFound("projects", project_id)          # 404, no existence leak
    raise Conflict("STALE_VERSION", field="version",
                   current_version=exists.version)      # 409 / 412


def delete_project(tx, project_id, tenant_id):
    try:
        deleted = tx.execute(
            "DELETE FROM projects WHERE id = %s AND tenant_id = %s RETURNING id",
            (project_id, tenant_id),
        ).rowcount
        return deleted > 0                              # idempotent: false is still success
    except DriverError as exc:
        db = normalize(exc)
        if db.code == "23503":                          # MySQL 1451
            raise Conflict("RESOURCE_IN_USE", resource="projects")
        raise translate(db, op="projects.delete", resource="projects")
```

```text
DELETE /projects/42 twice:
  first  → 204 No Content
  second → 204 No Content        (idempotent, not 404)
DELETE /projects/42 with live child rows:
  → 409 { "title": "RESOURCE_IN_USE" }
```

## Key data / numbers

- Postgres `UPDATE`/`DELETE ... RETURNING` gives outcome + data in **one round trip**; prefer it
  over `rowCount` + follow-up.
- `rowCount = 0` on `UPDATE` is **ambiguous** — never map it directly to `404`.
- MySQL `1451` (referenced row) and Postgres `23503` on delete → `409 RESOURCE_IN_USE`.
- Delete idempotency: `DELETE` twice returns success twice; HTTP `204` both times.
- ORMs: SQLAlchemy `NoResultFound`, Django `DoesNotExist`, Prisma `P2025` — all mean "required
  read/update matched nothing"; map them to `NOT_FOUND`/`CONFLICT`, not `500`.

## Real-world use case — Acme SaaS

Acme's `updateProject` returned `200` whenever the SQL executed, even if `rowCount` was `0`. Two
users editing the same project silently overwrote each other because the stale write "succeeded"
with no change. Adding `version` to the predicate, `RETURNING`, and an explicit `STALE_VERSION`
conflict turned the silent loss into a `409` the UI could resolve by reloading. In the same
sprint, `deleteProject` stopped returning `500` for an already-deleted project (now `204`) and
started returning `409 RESOURCE_IN_USE` when tasks still referenced it.

## Trade-offs

| Semantics | Pros | Cons | When to use |
| --------- | ---- | ---- | ----------- |
| `find` returns `null` | no exceptions for normal flow | null checks everywhere | optional lookups |
| `get` throws `NOT_FOUND` | caller intent clear | exceptions as control flow | required reads |
| Idempotent delete (`204`) | retry-safe | cannot tell "never existed" | default |
| `404` on second delete | strict | breaks retries | only if required |
| `UPDATE ... RETURNING` | one round trip | Postgres/MySQL 8 only | default |
| 0-row update as `404` | simple | hides stale writes | never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return `null` for absent lookups; throw for required reads | Throw `NOT_FOUND` from every `find` |
| Translate query failure to `5xx`, not `404` | Catch all errors and return `null` |
| Distinguish stale version from absent row | Map 0-row update to `404` |
| Make delete idempotent | `500` when the row is already gone |
| Map `23503` on delete to `RESOURCE_IN_USE` | Treat FK-on-delete as internal error |
| Return the existing row for idempotent create | Insert a duplicate and dedupe later |

## Common mistakes

- **`catch { return null }`** — outages become `404`s.
- **Ignoring `rowCount`** — silent lost updates.
- **`404` on idempotent replay** — clients retry deletes and see errors.
- **Duplicates always `409`** — webhook replays then generate noise and retries.
- **Revealing existence via different errors** — cross-tenant probes learn what exists.

## Checklist

- [ ] `find` vs `get` semantics are explicit and named.
- [ ] Query failure never becomes `null`/`404`.
- [ ] Updates use `RETURNING` or a follow-up to disambiguate 0 rows.
- [ ] Deletes are idempotent by default; required deletes use a separate method.
- [ ] FK-on-delete maps to `409 RESOURCE_IN_USE`.
- [ ] Duplicate-insert policy is decided by the service, not the repository.

## Related

- [Bulk Operations and Partial Success (24.9–24.10)](./04-bulk-operations-and-partial-success.md)
- [Repository Translating Persistence Errors](../03-practical-examples/01-repository-translating-persistence-errors.md)
- [Domain and Business Logic Errors (Ch. 18)](../../../part-07-validation-and-business-errors/18-domain-and-business-logic-errors/README.md)
- [Chapter 24 Reference](../05-reference/README.md)
