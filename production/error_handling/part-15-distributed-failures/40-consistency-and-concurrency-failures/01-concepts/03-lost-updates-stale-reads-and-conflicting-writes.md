# Lost Updates, Stale Reads, and Conflicting Writes (40.8–40.9)

> Part XV · Chapter 40 · Sections 40.8–40.9 · _Estimated reading time: 20 min_
> **Prerequisite:** [Races, Optimistic Control, and Version Conflicts (40.1–40.3)](./01-races-optimistic-control-and-version-conflicts.md)

## In one sentence

A **lost update** happens when a write based on an older read silently overwrites a newer one, and
a **stale read** happens when that older read comes from a cache or replica — both corrupt data
*without raising a single exception* unless you compare versions or preconditions at commit.

## Why this matters in production

This is the failure class that makes engineers say "the database said everything was fine." A
`last_updated_at`-based merge, a read from a read replica followed by a write to the primary, a
cart edited in two tabs — each produces plausible-looking wrong data, and each is invisible to
monitoring because every query *succeeded*. The cost shows up later as billing disputes,
configuration that "reverted," and edits that evaporate. Lost updates are exactly what OCC
(40.2) exists to detect; this file is about recognizing all the shapes they come in.

## Core concept

### 40.8 Lost updates

Four classic shapes:

```text
A. Read-modify-write (read 10 → write 11)          two of these, one increment vanishes
B. Last-writer-wins  (A sets x=1, B sets x=2)      A's intent is gone; no error anywhere
C. Blind overwrite    (PUT whole object from a     fields updated by a background job in
                       snapshot taken 30 s ago)     between are reverted
D. Copy-on-write merge (PATCH built from a stale    patch applies cleanly to the wrong base
                        client cache)
```

| Shape | Detector | Correct response |
|-------|----------|------------------|
| A — arithmetic increment | `WHERE version=$1`, or make it `SET n=n+1` | `409` or conflict-free atomic update |
| B — last-writer-wins | version / `If-Match` | `409` (or `412`) with current state |
| C — blind overwrite of a full object | `If-Match` on the ETag the client read | `412`; client refetches and re-applies |
| D — PATCH built stale | version precondition in the request | `409` + `currentVersion` for a merge |

The universal rule: **a write must be validated against the state it was derived from.** If you
cannot name that state (a version, an ETag, a timestamp with guaranteed precision), you cannot
detect the loss — and it will happen under load.

### 40.9 Stale reads and conflicting writes

Staleness has three common sources:

```text
client cache ──▶ stale UI ──▶ PUT with old payload          (D above)
read replica ──▶ read-your-write gap ──▶ verify against it  (write-after-read divergence)
in-process memo ──▶ background worker uses cached config ──▶ overwrites fresh value
```

**The read-replica trap**, in detail:

```text
1. Client creates a row → committed on PRIMARY
2. Client immediately GETs it → served by REPLICA (lag 5–500 ms) → 404
3. Client concludes failure and POSTs again → duplicate (or 409 if unique key exists)
   — or —
4. Worker reads config from replica (stale), computes, writes to primary → overwrites
   a newer config value with a decision made from the old one
```

Rules:

1. **Read-your-writes:** after a write, read from the primary (or from your own write result) for
   a bounded window. Session/"sticky" routing to a replica is a weaker version of the same idea.
2. **Never derive a write from a replica read.** Verify preconditions (version, `If-Match`,
   existence) **on the primary, inside the writing transaction**.
3. **Conflicting writes are not just two humans.** The second writer is often a background job, a
   webhook, or your own retry — audit *those* paths first; they have no UI to show a conflict.
4. **Merge explicitly when you can.** For genuinely concurrent *different* fields, a merge policy
   (`PATCH` semantics with field-level ownership) beats whole-object `PUT`.

## How it works (mechanics)

Detect a lost update with a precondition evaluated at write time:

```sql
-- Intent-derived update with precondition (the safe form)
UPDATE settings
   SET theme = COALESCE($2, theme),            -- only the fields the client owns
       locale = COALESCE($3, locale),
       version = version + 1
 WHERE tenant_id = $1
   AND version = $4;                            -- precondition: what the client read
-- rowCount = 0 → either not found or (more likely) someone wrote in between → 409/412
```

```python
def update_setting(tx, tenant_id, payload, expected_version):
    row = tx.execute("""
        UPDATE settings
           SET theme = COALESCE(%(theme)s, theme),
               locale = COALESCE(%(locale)s, locale),
               version = version + 1
         WHERE tenant_id = %(tid)s AND version = %(ver)s
         RETURNING version, theme, locale
    """, {"theme": payload.get("theme"), "locale": payload.get("locale"),
          "tid": tenant_id, "ver": expected_version}).fetchone()
    if row is None:
        cur = tx.execute("SELECT version FROM settings WHERE tenant_id=%s",
                         (tenant_id,)).fetchone()
        if cur is None:
            raise DomainError("SETTINGS_NOT_FOUND", http=404)
        raise DomainError("VERSION_CONFLICT", http=409,
                          details={"currentVersion": cur["version"]})
    return row
```

And the ETag/`If-Match` variant, which moves the precondition into HTTP:

```http
GET /v1/tenants/t_9/settings
→ 200
ETag: "v7"

PUT /v1/tenants/t_9/settings
If-Match: "v7"
→ 412 Precondition Failed          (someone else wrote since v7)
```

## Worked example

```text
Incident: "the integration config reverted"

  10:00:00.000  Admin saves webhook URL (settings.version 7 → 8)
  10:00:00.100  Support tool (background) had read settings at 09:59:58 (version 7)
                and writes back a full object with theme/locale/url from its snapshot
                → UPDATE settings SET url=..., theme=..., locale=... WHERE tenant_id=...
                → url reverted to the OLD value; version bumped 8 → 9
  10:00:01      No error, no log line, no 4xx/5xx anywhere.

Fix:
  - support tool must write only fields it owns (theme/locale), OR
  - full-object writes carry If-Match / version and get 412 → refetch → re-apply → 200
  - metric: count 409/412 by caller; the support tool's conflict rate went to 100% for a day
    (because it was always stale), which made the bug obvious instead of invisible.
```

```python
# Two concurrent increments — the safe version needs no conflict at all.
def bump_counter(tx, key):
    tx.execute("UPDATE counters SET n = n + 1, version = version + 1 WHERE key=%s", (key,))
    # atomic read-modify-write inside the DB: commutative, never loses an update
```

```text
Read-replica verification — WRONG vs RIGHT

WRONG:   v = read replica;   write to primary WHERE version = v     (v may be older than primary)
RIGHT:   write to primary WHERE version = (SELECT version FROM primary row FOR UPDATE)
         or: read on primary inside the same transaction as the write
```

## Key data / numbers

- **`409 Conflict`** for a stale version in the body; **`412 Precondition Failed`** for `If-Match`;
  **`404`** when the row genuinely does not exist — do not report `409` for missing rows.
- Replica lag is commonly **tens of ms** and routinely **hundreds of ms** under load (and seconds
  after a failover) — that window is wide enough for a duplicate-create or a "resend" button.
- ETag comparison for concurrency must be **strong** (`"v7"`); `W/"..."` weak validators are for
  cache freshness only.
- Timestamp-based preconditions need precision ≥ the write rate: with `updated_at` at **second**
  precision, two writes in the same second are undetectable — use an integer version.
- Read-your-writes windows: simplest correct rule is **"read from primary for the rest of the
  session/request"**; sticky routing is an optimization, not a guarantee.

## Real-world use case — Acme SaaS

Acme's project settings page autosaved the whole settings object every 5 seconds. A tenant's admin
changed a webhook URL while a billing job updated `plan_features` on the same row; the autosave's
full-object `PUT` silently reverted the billing job's update — and vice versa. Two weeks of
"settings randomly revert" reports produced no errors in logs because **every query succeeded**.
The fix was threefold: field-ownership (`PATCH` only your own fields), a `version` column with
`409` + `currentVersion`, and `If-Match` on the settings endpoint returning `412`. Conflicts
surfaced at ~4/minute during editing sessions (previously invisible), the client began merging on
`412`, and "revert" reports stopped. Replica reads were also excluded from any write's input.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Integer version + `409` | precise, simple, merge-friendly | clients must handle `409` | default for any editable row |
| `If-Match` ETag + `412` | HTTP-native, caching-friendly | ETag plumbing on every GET | public/HTTP-first APIs |
| Field-ownership `PATCH` | concurrent different-field edits just work | cannot express whole-object replace | multi-writer settings objects |
| Last-writer-wins | zero code | silent data loss | never for money/config/entitlements |
| `SELECT FOR UPDATE` around read-modify-write | no conflicts | lock waits, deadlocks | tiny, very hot rows |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Validate a write against the state it derived from | Blindly `UPDATE ... SET` the whole row |
| Read from the primary before writing | Derive writes from a replica or cache |
| Give background jobs the same preconditions as humans | Assume jobs cannot race the UI |
| Distinguish `404` from `409` | Return `409` when the row simply is gone |
| Merge on conflict, field by field | Overwrite the whole object from a stale snapshot |

## Common mistakes

- **Version check on the wrong row** (checking `project.version` while writing `settings`).
- **Prefetch version, then use a different connection** for the write — the check is not atomic
  with the write.
- **`COALESCE`-free PATCH** that writes `null` over fields the client never intended to clear.
- **Assuming the UI always reads immediately before writing** — mobile clients write minutes
  later.
- **Trusting a cached config read in a worker** — the classic background-job lost update.
- **`SELECT ... FOR UPDATE` forgotten** on a read-modify-write you deemed "too simple."

## Checklist

- [ ] Every editable row used by >1 writer has a version or ETag precondition.
- [ ] `rowCount` is checked; `0` maps to `409`/`412`/`404` deliberately.
- [ ] No write is derived from a replica/cached read.
- [ ] Background jobs and webhooks carry preconditions too.
- [ ] Field ownership is defined where multiple writers touch one row.
- [ ] Reproduce the race in a test with two real sessions before shipping.

## Related

- [Optimistic Locking with a Version Column — worked example](../03-practical-examples/01-optimistic-locking-with-version-column.md)
- [Conflict Resolution, Retry Safety, and Corruption (40.13–40.15)](./05-conflict-resolution-retry-safety-and-corruption.md)
- [Replica Consistency (40.12)](./04-distributed-locks-fencing-and-replicas.md)
- [Repository and Data Access Error Handling (Ch. 24)](../../../part-09-database-and-transactions/24-repository-and-data-access-error-handling/README.md)
