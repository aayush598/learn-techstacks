# Read-After-Write and Consistency Mechanics (24.14, 24.15)

> Part IX · Chapter 24 · Sections 24.14, 24.15 · _Estimated reading time: 24 min_
> **Prerequisite:** [Read-After-Write and Consistency Guarantees](../01-concepts/05-read-after-write-and-consistency-guarantees.md)

## In one sentence

Make read-your-writes **provable** by carrying a **consistency token** (LSN, GTID, or version)
from the write to the read, and fail closed — fall back to the primary — when the replica has not
caught up.

## Why this matters in production

Heuristics like "read primary for 5 seconds" work until replication stalls for 30 seconds during a
backup or a network blip. A token-based check turns a guess into a guarantee: the read either sees
the write or goes to the primary. This is the difference between "we think it's fine" and "the
dashboard cannot show stale data after an edit." It also gives you a cheap, precise lag metric
instead of a vague "replication seems slow."

## Core concept

```text
        ┌──────────┐   commit at LSN L   ┌───────────┐
write ─▶│ PRIMARY  │────────────────────▶│  REPLICA  │
        └──────────┘   async stream      └───────────┘
             │                                 │
             │ token = L                       │ replay = R
             ▼                                 ▼
        client/session ────────────────▶ read: R >= L ? replica : primary
```

| Mechanism | Token | Check | Notes |
| --------- | ----- | ----- | ----- |
| **Postgres LSN** | `pg_current_wal_lsn()` | `pg_last_wal_replay_lsn() >= L` | precise, per-cluster |
| **MySQL GTID** | `@@global.gtid_executed` | `WAIT_FOR_EXECUTED_GTID_SET(gtid, timeout)` | blocks until applied |
| **Logical version** | row `version` / `updated_at` | compare in the read | app-level, per-row |
| **Session pin** | "wrote at" timestamp | `now - wroteAt < window` | heuristic, simple |
| **Sticky routing** | session → primary | none | coarse, expensive |

### 24.14 The write path

1. Execute the write on the primary, `RETURNING` the row **and** capturing the commit position.
2. Return the row to the caller (so the immediate response needs no read).
3. Put the position in a **consistency token** attached to the session/response (header or
   signed cookie, not a client-trusted value).
4. The next read presents the token; the router compares it to the replica's replay position.

```sql
-- Postgres: capture the position in the same transaction as the write
BEGIN;
UPDATE projects SET name = $1 WHERE id = $2 RETURNING id, name, version;
SELECT pg_current_wal_lsn();          -- L, valid after commit for this session
COMMIT;
```

> Capture **after** the write statement in the same transaction. `pg_current_wal_lsn()` is the
> insert/commit position; for strict guarantees compare against the commit LSN
> (`pg_current_wal_flush_lsn()` after commit, or use `pg_logical_emit_message`/a commit hook).

### 24.15 The read path

```ts
async function readWithToken<T>(
  token: ConsistencyToken | undefined,
  read: (db: Db) => Promise<T>,
): Promise<T> {
  if (!token) return read(this.replica);              // no recent write → replica
  const caughtUp = await this.replicaCaughtUp(token); // cached per replica, ~50 ms TTL
  return read(caughtUp ? this.replica : this.primary); // fail closed
}

async function replicaCaughtUp(token: ConsistencyToken): Promise<boolean> {
  const r = await this.replica.one(
    "SELECT pg_last_wal_replay_lsn() >= $1::pg_lsn AS ok", [token.lsn],
  );
  return r.ok;
}
```

For MySQL: `SELECT WAIT_FOR_EXECUTED_GTID_SET($1, $2)` blocks until the replica applies the set
(or times out). Cache the result briefly — checking per query doubles read latency.

## How it works (mechanics)

### Lag budget

Define per read class, then alert when exceeded:

| Read class | Max staleness | Action when exceeded |
| ---------- | ------------- | -------------------- |
| Auth / entitlement | **0** (primary) | never allow |
| Post-write edit view | **0** (token) | fall back to primary |
| User dashboard | 5 s | show "updated 4 s ago" |
| Search / analytics | 60 s | background reindex |
| Billing reconciliation | 0 | primary |

Measure lag as `primary_lsn - replica_replay_lsn` (bytes) and as **seconds behind** — bytes alone
hide a stuck replica.

### Failure modes

| Failure | Symptom | Handling |
| ------- | ------- | -------- |
| Replication stopped | `replay_lsn` frozen | exceed budget → primary + page |
| Replica promoted/demoted | token refers to old timeline | invalidate token on failover |
| Token from a different cluster | comparison meaningless | include cluster id in token |
| Clock-based token | skew → wrong window | prefer LSN/GTID/version |
| `WAIT_FOR_EXECUTED_GTID_SET` timeout | replica far behind | fall back to primary |
| Read on primary after failover | old primary stale | use the new primary's token |

### Monotonic reads

Without a token, a session can bounce between replicas at different positions and go **backwards**
in time. Pin a session to one replica (hash of session id) or keep a per-session high-water mark
and route to a replica that has reached it.

## Worked example

```python
# FastAPI middleware: issue and honor a consistency token.
def write_project(request, project_id, patch, db, session):
    row, lsn = db.primary.execute(
        """UPDATE projects SET name=%s WHERE id=%s
           RETURNING id, name, version""", (patch.name, project_id)
    ), None
    lsn = db.primary.scalar("SELECT pg_current_wal_lsn()::text")
    token = sign({"lsn": lsn, "cluster": CLUSTER_ID})
    response.headers["X-Consistency-Token"] = token
    return row


def read_project(request, project_id, db):
    token = verify(request.headers.get("X-Consistency-Token"))
    if token and token["cluster"] != CLUSTER_ID:
        token = None                                  # failover: ignore foreign token
    if token and not replica_has(token["lsn"], db.replica):
        return db.primary.fetch_one(...)              # fail closed
    return db.replica.fetch_one(...)


def replica_has(lsn, replica):
    return replica.scalar(
        "SELECT pg_last_wal_replay_lsn() >= %s::pg_lsn", (lsn,)
    )
```

```text
PATCH /projects/42 → 200 + X-Consistency-Token: lsn=0/1A2B3C
GET   /projects/42 (with token)  → replica caught up → replica read
GET   /projects/42 (replica 2 s behind) → primary read
GET   /projects/42 (no token)    → replica read (eventual)
```

## Key data / numbers

- Token check adds **one small query** per read unless cached; cache per replica for **50–100 ms**.
- Lag alert thresholds: **warn > 2 s**, **page > 10 s** for primary-backed paths; tune to SLA.
- Postgres: `pg_last_wal_receive_lsn()` vs `pg_last_wal_replay_lsn()` distinguishes "received but
  not applied" from "not received" — the latter means a network problem.
- MySQL `WAIT_FOR_EXECUTED_GTID_SET` timeout: keep **< 100 ms** on the request path; fall back
  after.
- Tokens must be **signed**; an unsigned LSN lets a client pin itself to the primary (DoS).

## Real-world use case — Acme SaaS

Acme's 5-second primary window failed during a nightly backup: replication lag hit 40 seconds,
and edits made during the window were read back stale, producing duplicate "rename" audit entries.
The team replaced the time window with an **LSN token** returned by every write and a cached
replica catch-up check. Reads with a token either hit a caught-up replica or the primary; dashboards
kept using eventual reads and showed a freshness indicator. Duplicate renames disappeared, and the
lag metric (from token checks) fed a new alert that fires before users notice.

## Trade-offs

| Approach | Correctness | Latency | Complexity |
| -------- | ----------- | ------- | ---------- |
| Always primary | strongest | higher | none |
| Time window | heuristic | low | low |
| LSN/GTID token | exact | +1 check (cacheable) | medium |
| Session pin | good-ish | low | low |
| Row version compare | per-row exact | low | app changes |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return the written row (`RETURNING`) | Immediately re-read a replica |
| Sign and scope consistency tokens | Trust a client-supplied LSN |
| Fail closed (primary) when unsure | Serve a possibly-stale read |
| Cache catch-up checks briefly | Query replica position per row |
| Include cluster/timeline in the token | Compare LSNs across failovers |
| Alert on lag seconds, not just bytes | Assume bytes equal staleness |

## Common mistakes

- **Token captured before the write commits** — the read can still miss it.
- **Comparing LSNs across clusters** — after failover they are unrelated.
- **`WAIT_FOR_EXECUTED_GTID_SET` on the primary** — wrong node; it must run on the replica.
- **Monotonicity ignored** — bouncing replicas makes UIs flicker backwards.
- **Unsigned tokens** — clients can force primary reads or forge freshness.

## Checklist

- [ ] Writes return the row and a signed consistency token.
- [ ] Reads with a token verify replica catch-up, cached briefly.
- [ ] Failover invalidates tokens (cluster/timeline id included).
- [ ] Auth/billing reads bypass replicas entirely.
- [ ] Lag is monitored in seconds with warn/page thresholds.
- [ ] Monotonic reads are guaranteed per session.
- [ ] Tests cover stalled replication and failover.

## Related

- [Read-After-Write and Consistency Guarantees (24.14, 24.15)](../01-concepts/05-read-after-write-and-consistency-guarantees.md)
- [Failover, Replicas, and Unavailability (22.14–22.16)](../../22-database-error-classification/01-concepts/04-failover-replicas-and-unavailability.md)
- [Partial Failures and Multi-Step Operations (Ch. 39)](../../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
- [Consistency and Concurrency Failures (Ch. 40)](../../../part-15-distributed-failures/40-consistency-and-concurrency-failures/README.md)
