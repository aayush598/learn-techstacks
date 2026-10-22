# Races, Optimistic Control, and Version Conflicts (40.1–40.3)

> Part XV · Chapter 40 · Sections 40.1–40.3 · _Estimated reading time: 22 min_
> **Prerequisite:** [Conflicts, Locks, and Timeouts (22.9–22.13)](../../../part-09-database-and-transactions/22-database-error-classification/01-concepts/03-conflicts-locks-and-timeouts.md)

## In one sentence

A **race condition** is a decision made from state that changed underneath you, and **optimistic
concurrency control** turns that silent corruption into a loud, retryable **`HTTP 409`** by
checking a **version** at commit time.

## Why this matters in production

The nastiest data bugs do not crash. `WebhookIngest` processes the same `invoice.paid` twice in
two pods; a tenant's seat count goes 10 → 11 → 10 instead of 12; two support agents edit a ticket
and the second save erases the first. No exception is thrown, no log line is red — the numbers are
just wrong, sometimes for weeks, until a customer audits. Race conditions are the class of failure
that **error handling cannot see unless you build the detector**, and the detector is a version
check.

## Core concept

### 40.1 Races

```text
T1: read seats = 10                    T2: read seats = 10
T1: seats := 10 + 1 = 11               T2: seats := 10 + 1 = 11
T1: WRITE 11 ✓                         T2: WRITE 11 ✓      ← T1's increment vanished
result: 11, expected 12                 (lost update, 40.8)
```

A race condition exists when:

1. Two or more agents (processes, pods, threads, retries, cron) act on the **same item**,
2. their operations **interleave**, and
3. the outcome depends on the interleaving **and nobody checked**.

The key insight: **retries and background jobs make you concurrent even if users are not.** A
deploy that starts two pods is concurrency. A queue redelivery is concurrency. Optimistic locking
is not a feature for "big systems"; it is the default for *any* system with more than one runner.

### 40.2 Optimistic concurrency control (OCC)

OCC assumes conflicts are rare, so it **does not lock while working**; it **verifies at commit**
that nothing else changed:

```text
1. READ the row (including version)
2. COMPUTE the new values locally
3. UPDATE ... SET ..., version = version + 1
    WHERE id = $1 AND version = $expected
4. If rowCount = 1 → committed. If rowCount = 0 → CONFLICT (someone else won)
```

| Mechanism | Detected how | Client sees |
|-----------|--------------|-------------|
| **Version column** (integer, +1 per write) | `WHERE version = $1` matched 0 rows | `409 Conflict` |
| **`If-Match` / ETag** (HTTP-native) | precondition fails | `412 Precondition Failed` |
| **`last_updated_at`** timestamp compare | `WHERE updated_at = $expected_ts` | `409` (⚠️ clock/precision hazards) |
| **CAS in Redis** (`WATCH`/`MULTI` or `SET ... XX GET`) | transaction aborts | retry or `409` |

### 40.3 Version conflicts

A version conflict means *"your input was based on a state that no longer exists."* The correct
response depends on what the client sent:

| Client sent | Response | Why |
|-------------|----------|-----|
| The whole object, built from a stale read | **`409 Conflict`** + current version/ETag | merging is the client's job; it has fresher data now |
| A partial delta, still valid on the new state | **re-apply** to the new row, then re-check | e.g. `increment by 1` is commutative |
| A precondition (`If-Match`) | **`412 Precondition Failed`** | HTTP-native, semantics are exactly "your ETag is stale" |
| Unconditional write (`UPDATE ... SET x=1`) | succeeded, but **possibly a lost update** | this is the bug OCC prevents |

⚠️ **Hazard.** A conflict retried with the *original* `version` fails forever. The retry must
**re-read** and re-apply the user's *intent* ("set status to approved", "add 1 seat"), not replay
the stale payload.

## How it works (mechanics)

### The guarded update is the whole detector

```sql
-- The conflict detector: no rowCount check, no detection.
UPDATE tickets
   SET body = $2,
       version = version + 1,
       updated_by = $3
 WHERE id = $1
   AND version = $4;             -- ← $4 came from the client's read (If-Match / body)
```

```ts
const res = await db.query(
  `UPDATE tickets SET body=$2, version=version+1 WHERE id=$1 AND version=$3`,
  [id, body, expectedVersion]);
if (res.rowCount === 0) {
  const current = await db.oneOrNone(`SELECT version, body FROM tickets WHERE id=$1`, [id]);
  if (!current) throw new DomainError("TICKET_NOT_FOUND", { http: 404 });
  throw new DomainError("VERSION_CONFLICT", {        // stable code, maps to 409
    http: 409,
    details: { currentVersion: current.version },     // lets the client refetch and merge
  });
}
```

### Retry shape for a conflict

```text
attempt: read (v=7) → compute → guarded update (WHERE version=7)
  ├─ rowCount=1 → 200
  └─ rowCount=0 → 409 → client: refetch (v=8) → re-apply intent → update (WHERE version=8)
```

- **Who retries:** the *writer with intent*, usually the client or the service layer — never a
  blind middleware retry that re-sends the stale payload.
- **How many:** conflicts are contention; if every attempt conflicts, the retry storm is the
  symptom — back off with jitter, cap attempts (commonly 3), and measure conflict rate as a
  signal that the row is too hot (consider read-modify-write in one SQL statement instead).

## Worked example

```python
def add_seat(tenant_id: str, expected_version: int) -> Tenant:
    """Re-apply INTENT (+1 seat) rather than a stale snapshot."""
    with transaction() as tx:
        row = tx.execute(
            """UPDATE tenants
                  SET seats = seats + 1, version = version + 1
                WHERE id = %s AND version = %s AND seats < seat_limit
                RETURNING id, seats, version""",
            (tenant_id, expected_version),
        ).fetchone()
        if row is None:
            cur = tx.execute("SELECT seats, seat_limit, version FROM tenants WHERE id=%s",
                             (tenant_id,)).fetchone()
            if cur is None:
                raise DomainError("TENANT_NOT_FOUND", http=404)
            if cur["seats"] >= cur["seat_limit"]:
                raise DomainError("SEAT_LIMIT_REACHED", http=409)   # business conflict, not a race
            raise DomainError("VERSION_CONFLICT", http=409,         # race: caller's version is stale
                              details={"currentVersion": cur["version"]})
        return row
```

```text
Two admins click "Add seat" simultaneously, both read version=7:
  A: UPDATE ... WHERE version=7 → rowCount=1 → seats=11, version=8 → 200
  B: UPDATE ... WHERE version=7 → rowCount=0 → SELECT → version=8 → 409 + currentVersion
  B's client refetches (seats=11, v=8) → retries WHERE version=8 → seats=12 → 200
  net effect: 12 seats, zero lost increments, zero locks held.
```

## Key data / numbers

- **`HTTP 409 Conflict`** for version/state conflicts; **`412 Precondition Failed`** when the
  client used `If-Match`/`If-Unmodified-Since`; **`404`** if the row vanished underneath.
- gRPC convention for the same condition: **`ABORTED` (status code 10)** — the standard
  "transient conflict, retry with fresh state" signal.
- Version columns: `bigint NOT NULL DEFAULT 0`, incremented on **every** write (trigger or
  application). Timestamp versions are vulnerable to clock skew and precision — prefer an integer.
- Contention guidance: if a single row's conflict rate exceeds a few percent of writes, it is a
  **hot row** — batch the increments (`UPDATE ... SET n = n + k`) or shard the counter.
- ETags: strong validators are what `If-Match` expects; a weak `W/` ETag is not valid for
  concurrency control.

## Real-world use case — Acme SaaS

`WebhookIngest` applied Stripe events with `UPDATE invoices SET status=... ` and no version check.
During a Stripe retry burst, two pods processed `invoice.paid` concurrently; both read
`status='open'` and wrote `status='paid'` — harmless — but a concurrent `payment_method.updated`
write in between was overwritten, leaving an invoice pointing at a detached payment method. After
adding `version = version + 1 ... WHERE version = $1`, the race surfaced as `409`s at a rate of
~0.3% during retry bursts; ingest retried with a fresh read and a **stable event-derived idempotent
payload**. The corrupted-invoice rate went to zero, and conflict rate became a useful metric
instead of a hidden one.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| **Optimistic (version/ETag)** | no lock holding, scales, great under low contention | conflicts waste work; needs client retry logic | default; human-paced edits, most APIs |
| **Pessimistic (`SELECT FOR UPDATE`)** | no wasted work, one winner | lock waits, deadlocks, pool pressure | high contention, short critical sections |
| **Atomic single-statement update** (`SET n=n+1`) | conflict-free by construction | only works when the operation is commutative | counters, quotas, append-only fields |
| **No control at all** | zero code | silent lost updates | never once two writers exist |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Check `rowCount` after every guarded update | Assume the `UPDATE` matched |
| Return `409` + current version | Return `500` for a stale write |
| Retry by re-reading and re-applying intent | Retry the stale payload with the old version |
| Use integer versions, not timestamps | Rely on `updated_at` with second precision |
| Give every hot row a conflict metric | Treat contention as an embarrassing secret |

## Common mistakes

- **Omitting the `WHERE version = ...`** — you wrote a version column for nothing; both writers
  "win."
- **Reading the version in a different transaction/connection than the write** — the whole point
  is that the check is atomic with the write.
- **Retrying `409` in middleware** — a generic retry re-sends the identical stale body and fails
  `maxAttempts` times before surfacing a worse error.
- **Confusing business `409` with race `409`** — "seat limit reached" and "your version is stale"
  are both `409` but need different client actions; keep them different **codes**.
- **Version bumps only on "edits"** — a background job that writes without bumping invalidates
  every client's `If-Match`.

## Checklist

- [ ] Every table with human or multi-service writers has a version (or `If-Match` ETag).
- [ ] Every guarded `UPDATE` checks `rowCount`.
- [ ] Conflict maps to `409`/`412` with a stable code and the current version.
- [ ] Retries re-read and re-apply intent; generic middleware never retries `409` blindly.
- [ ] Business conflicts and race conflicts share a status but not a code.
- [ ] Conflict rate is a monitored metric; hot rows are identified.

## Related

- [Optimistic Locking with a Version Column — worked example](../03-practical-examples/01-optimistic-locking-with-version-column.md)
- [Optimistic Concurrency vs Deadlock — deep dive](../02-deep-dive/01-optimistic-concurrency-vs-deadlock.md)
- [Lost Updates, Stale Reads, and Conflicting Writes (40.8–40.9)](./03-lost-updates-stale-reads-and-conflicting-writes.md)
- [HTTP Error Semantics: 409 (19.7)](../../../part-08-http-and-api/19-http-error-semantics/README.md)
