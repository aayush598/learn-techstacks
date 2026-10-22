# Chapter 24 — Do's and Don'ts

> Part IX · Chapter 24 · _Estimated reading time: 12 min_
> **Prerequisite:** [Chapter 24 README](../README.md)

## The short version

> **Translate at the repository, preserve the cause, expose intent, and never let "no rows" mean
> "it worked".**

## Do's

### Boundary and responsibilities

- ✅ **Import the driver only in the adapter.** One directory, one owner.
- ✅ **Name methods by intent** (`findById`, `findByIdOrFail`, `updateIfVersion`) so callers see
  the semantics.
- ✅ **Accept the transaction from the service.** Compose multiple repository calls in one unit.
- ✅ **Return domain-shaped data**, not raw rows or lazy ORM entities.
- ✅ **Keep HTTP out of the repository.** Map codes to statuses in the controller.
- ✅ **Use one `translate()`** as the single constructor of repository errors.

### Error shape

- ✅ **Give every error a stable code, category, `transient`, and `retryScope`.**
- ✅ **Preserve `cause`** with the original driver error — server-side only.
- ✅ **Allowlist `field`** from constraint names; omit when unknown.
- ✅ **Write `safeMessage` yourself**; never reuse the driver's message.
- ✅ **Attach `op` and `resource`** for metrics and triage.
- ✅ **Serialize from an allowlist**, so `cause` is structurally unreachable.

### CRUD semantics

- ✅ **`null` for optional lookups; `NOT_FOUND` for required reads.**
- ✅ **Never turn a query failure into `null`/`404`.**
- ✅ **Use `RETURNING`** so the caller gets the written row without a second read.
- ✅ **Disambiguate 0-row updates** into `NOT_FOUND` vs `STALE_VERSION`.
- ✅ **Make delete idempotent**; use a separate `deleteOrFail` when required.
- ✅ **Map FK-on-delete (`23503`/`1451`) to `RESOURCE_IN_USE`.**
- ✅ **Let the service decide** whether a duplicate is `409` or a replayed success.

### Bulk operations

- ✅ **Return per-item outcomes** with item identity.
- ✅ **Distinguish `failed` from `skipped`** (not attempted).
- ✅ **Use savepoints or chunks** when partial success is required.
- ✅ **Use `ON CONFLICT` only for expected duplicates.**
- ✅ **Persist the report**; do not rely on the HTTP response alone.
- ✅ **Retry only failed lines/chunks.**

### Consistency

- ✅ **Return the written row** or read the primary after a write.
- ✅ **Emit a signed consistency token** (LSN/GTID) and honor it on reads.
- ✅ **Read the primary for auth, billing, and idempotency.**
- ✅ **Declare the read source per method.**
- ✅ **Measure replica lag in seconds** against a documented budget.

## Don'ts

### Boundary and responsibilities

- ❌ **Don't catch driver exceptions in services or controllers.** It re-couples the layers.
- ❌ **Don't return raw rows** — snake_case and DB types become your API.
- ❌ **Don't open transactions inside the repository** (unless it is a deliberate unit-of-work
  API).
- ❌ **Don't let ORM entities escape** and lazy-load after the transaction.
- ❌ **Don't decide HTTP status** in the adapter.

### Error shape

- ❌ **Don't throw a single `RepositoryError("database error")`.** It destroys every decision.
- ❌ **Don't echo `SQLSTATE`, constraint names, SQL, or `DETAIL`.**
- ❌ **Don't drop `cause`** "to keep it clean".
- ❌ **Don't `Object.assign`/spread the driver error** into the response.
- ❌ **Don't send unscrubbed errors to the tracker** — it is a second API.
- ❌ **Don't fall back to the constraint name** when the allowlist misses.

### CRUD semantics

- ❌ **Don't `catch { return null }`.** Outages become 404s.
- ❌ **Don't return `200` when `rowCount = 0`.**
- ❌ **Don't `404` on an already-deleted row** by default.
- ❌ **Don't turn FK-on-delete into a `500`.**
- ❌ **Don't make every duplicate a `409`** — webhook replays become incidents.
- ❌ **Don't leak existence across tenants** with distinct errors.

### Bulk operations

- ❌ **Don't return a boolean for a batch.**
- ❌ **Don't assume a multi-row insert is partially applied** — Postgres aborts the statement.
- ❌ **Don't use `INSERT IGNORE`** to silence all conflicts (it hides truncation too).
- ❌ **Don't mark unprocessed rows as failed.**
- ❌ **Don't restart a 100k-row import** for 7 bad lines.

### Consistency

- ❌ **Don't re-read a replica immediately after a write.**
- ❌ **Don't resolve ambiguous commits or idempotency keys from a replica.**
- ❌ **Don't check entitlements on a lagging replica.**
- ❌ **Don't trust unsigned consistency tokens.**
- ❌ **Don't compare LSNs across a failover** without a cluster/timeline id.
- ❌ **Don't assume replication is instant** because it usually is.

## Code review checks

| Check | Fail signal |
| ----- | ----------- |
| Driver imports | driver package imported outside the adapter |
| Error construction | `new RepositoryError` / `throw Error("db")` |
| Serialization | `...err`, `toJSON`, `cause` in payload |
| Absence handling | `catch { return null }`, `rows[0]` unguarded |
| Update result | `UPDATE` without `RETURNING` or `rowCount` check |
| Delete | delete throws when nothing matched |
| Bulk | returns `void`/`boolean` for N items |
| Consistency | write then read from `replica` in the same handler |
| Retry | repository retries internally, hiding attempts |

## Incident smells

| Symptom | Likely cause |
| ------- | ------------ |
| "My save disappeared" | write → replica read |
| Duplicate records after retry | duplicate treated as `500`, client retried create |
| `500` on second delete | delete not idempotent |
| PII in error tracker | unscrubbed `cause`/`DETAIL` |
| 404 during an outage | `catch { return null }` |
| Import re-runs from zero | no checkpoint / all-or-nothing batch |
| Stale rename in UI | read-after-write not routed to primary |

## The one-line rule

> If a caller cannot tell **retry** from **fix your input** from **page someone** using only your
> error, the repository has not finished its job.

## Related

- [Chapter 24 README](../README.md)
- [Mapping Persistence to Application Errors](../01-concepts/02-mapping-persistence-to-application-errors.md)
- [Leak Prevention and Metadata Preservation](../02-deep-dive/01-leak-prevention-and-metadata-preservation.md)
- [Chapter 24 Reference](../05-reference/README.md)
