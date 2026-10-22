# Failover, Replicas, and Unavailability (22.14–22.16)

> Part IX · Chapter 22 · Sections 22.14–22.16 · _Estimated reading time: 18 min_
> **Prerequisite:** [Conflicts, Locks, and Timeouts](./03-conflicts-locks-and-timeouts.md)

## In one sentence

Failover turns a healthy database into a **briefly unavailable** one, read replicas turn
**write-after-read** into a stale-read bug, and unavailability is a **transient state you must
ride out** — not a reason to return `500` while the standby is being promoted.

## Why this matters in production

Managed Postgres and MySQL fail over more often than teams expect: maintenance, AZ loss, a
storage hiccup, or a version upgrade can promote a standby in seconds to minutes. During that
window every pooled connection dies (`08006`), writes may hit the **old primary** and be
rejected as read-only (**`25006`**), and reads from replicas lag behind the write the user just
made. Code that treats these as permanent errors produces failed checkouts and "I saved it but
it's gone" tickets — for events that resolve themselves.

## Core concept

```text
                 ┌──────────────┐   async replication   ┌──────────────┐
   writes ─────▶ │   primary    │ ────────────────────▶ │  replica(s)  │ ◀───── reads
                 └──────┬───────┘                       └──────────────┘
                        │ failure
                        ▼
                 ┌──────────────┐
                 │ new primary  │  promotion: seconds–minutes
                 └──────────────┘  connections dropped → 08006 / 2013
                                   old primary now rejects writes → 25006
                                   app still points at old host? → 57P03 / ECONNREFUSED
```

| § | Situation | Signals | Correct posture |
| - | --------- | ------- | --------------- |
| 22.14 | **Failover** | `08006`, `57P03`, MySQL `2006`/`2013`, connection resets | transient → reconnect + backoff; never retry writes blindly (ambiguous) |
| 22.15 | **Read replica** | stale rows, replica lag, `25006` if a write lands on a read-only node | route reads deliberately; read-your-writes from primary |
| 22.16 | **Unavailable** | `08006`, `53300`, DNS failure, refused connection | `503` + `Retry-After`, bounded retry, shed load |

**Unavailability is a state, not an exception type.** The same SQLSTATE can mean "restarting"
(seconds), "failover in progress" (tens of seconds), or "the database is gone" (page). Only
duration and health checks distinguish them.

## How it works (mechanics)

### Failover (22.14)

1. Primary becomes unreachable; the client's open connections fail (`08006`/`2013`).
2. The orchestrator promotes a replica and repoints the **service** name (DNS/VIP) — but DNS
   TTLs and pooled connections mean your process may still hold dead sockets or the old address.
3. In-flight transactions: **aborted**; their outcome may be unknown if `COMMIT` was in flight
   (see [ambiguous outcomes](../../23-transaction-and-rollback-error-handling/02-deep-dive/01-ambiguous-commit-outcomes.md)).
4. New connections succeed once routing updates and the new primary accepts writes. Any write
   still sent to the *old* primary returns **`25006 read_only_sql_transaction`**.

### Read replicas (22.15)

Replication is typically **asynchronous**: the primary commits, then ships WAL/binlog. A read
on a replica can therefore miss a just-committed write. This is normal, not corruption.

| Read type | Source | Why |
| --------- | ------ | --- |
| Immediately after a user write (profile, order confirmation) | **primary** | read-your-writes |
| Dashboards, lists, search | replica | tolerate seconds of lag |
| Authorization / entitlement checks | **primary** (or cached with version) | a stale "not suspended" is a security bug |
| Idempotency lookups | **primary** | deciding "already processed" from a lagging replica duplicates work |

### Unavailability (22.16)

Distinguish three tiers before choosing a response:

| Duration / evidence | Response |
| ------------------- | -------- |
| Seconds, health check flapping, failover event | retry with backoff, hold requests briefly, `503` + `Retry-After` |
| Sustained > 30 s, pool failures, all nodes down | fail fast `503`, enable degraded mode, page |
| Partial (one replica down) | route around it, keep serving |

## Worked example

```go
// Classifying availability errors without guessing
func classifyDB(err error) Code {
    var pgErr *pgconn.PgError
    if errors.As(err, &pgErr) {
        switch pgErr.Code {
        case "08006", "08003", "57P03":
            return CodeDBUnavailable       // transient
        case "53300":
            return CodeDBAtCapacity        // transient + shed load
        case "25006":
            return CodeDBReadOnly          // write hit a read-only/failover node
        }
    }
    if errors.Is(err, context.DeadlineExceeded) {
        return CodeDBTimeout               // ambiguous for writes
    }
    return CodeDBUnknown
}

// Read-your-writes: the write response already has the row, so don't re-read a replica.
func (s *Service) CreateProject(ctx context.Context, in CreateProject) (*Project, error) {
    p, err := s.repo.InsertPrimary(ctx, in) // INSERT ... RETURNING *
    if err != nil { return nil, err }       // already translated
    return p, nil                            // no second read → no replica lag bug
}
```

```sql
-- Detecting replica lag before trusting a read (Postgres)
SELECT now() - pg_last_xact_replay_timestamp() AS replica_lag;
-- If lag > your tolerance, read from the primary instead.
```

## Key data / numbers

- Postgres SQLSTATE **`25006`** `read_only_sql_transaction` — a write reached a read-only node.
- **`57P03`** `cannot_connect_now` — server starting/shutting down; **`57P01`** `admin_shutdown`.
- MySQL **`2006`** server has gone away, **`2013`** lost connection during query, **`1290`**
  `--read-only` / super-read-only.
- Managed failover windows are commonly **10–60 s**; DNS TTL is often **5–60 s** — your
  connection pool may outlive the DNS change unless it re-resolves.
- Replica lag targets: **< 1 s** for same-region async replicas is typical; anything over your
  read-your-writes budget must route to primary.
- Retry budget during failover: **3–5 attempts over 10–30 s** with jitter; beyond that, `503`.

## Real-world use case — Acme SaaS

Acme read project lists from a replica to offload the primary. During a failover, three things
happened at once: open connections died (`08006`), the old primary rejected writes (`25006`),
and a user who had just renamed a project kept seeing the old name because the list read hit a
lagging replica. Support called it "data loss". The fix was not a bigger replica: the
**write response returns the updated entity** (no re-read), reads for the current user's own
writes go to the primary for 5 s after a write, and `25006`/`08006` are classified transient
with bounded retries. "Lost saves" disappeared, and failover became a blip instead of an
incident.

## Trade-offs

| Strategy | Pros | Cons | When to use |
|----------|------|------|-------------|
| All reads from primary | correct, simple | no read scaling | small apps, auth/billing paths |
| Replica reads + primary for read-your-writes | scales reads | routing complexity | most SaaS dashboards |
| Read from replica always | max scale | stale data, confusing UX | analytics, search indexes |
| Aggressive retry across failover | rides out short blips | retry storms during real outage | with capped budget + jitter |
| Fail fast `503` | protects resources | brief user-visible errors | sustained outage, overload |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify `08006`/`57P03` as transient | Return `500` for a failover blip |
| Route read-your-writes to the primary (or return the written row) | Re-read a lagging replica right after a write |
| Treat `25006` as a routing/retry signal | Retry `25006` forever on the same node |
| Cap retries during failover and then `503` | Retry writes with no ambiguity check |
| Monitor replica lag and pool re-resolution | Assume DNS/pool automatically follows promotion |

## Common mistakes

- **Re-reading a replica after a write** and concluding the write was lost.
- **Retrying a write after `08006` without an idempotency check** — it may have committed.
- **Pinning a pool to an IP** so failover never reaches the new primary.
- **Treating `53300` and `08006` identically** — capacity vs reachability need different actions.
- **Assuming `25006` means data corruption** — it means "you are talking to the wrong node".

## Checklist

- [ ] Failover signals (`08006`, `57P03`, `2006`, `2013`) are classified transient.
- [ ] Writes rejected with `25006` retry against the new primary, not the old one.
- [ ] Read-your-writes paths avoid replicas (or use `RETURNING`/session stickiness).
- [ ] Replica lag is measured and compared to a documented tolerance.
- [ ] Retry budget during failover is capped and jittered.

## Related

- [Connections and Pool Errors (22.1–22.2)](./01-connection-and-pool-errors.md)
- [Ambiguous Commit Outcomes](../../23-transaction-and-rollback-error-handling/02-deep-dive/01-ambiguous-commit-outcomes.md)
- [Read-After-Write and Consistency Guarantees](../../24-repository-and-data-access-error-handling/01-concepts/05-read-after-write-and-consistency-guarantees.md)
- [Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
