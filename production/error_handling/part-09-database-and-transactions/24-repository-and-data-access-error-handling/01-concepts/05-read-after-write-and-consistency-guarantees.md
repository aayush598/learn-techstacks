# Read-After-Write and Consistency Guarantees (24.14, 24.15)

> Part IX · Chapter 24 · Sections 24.14, 24.15 · _Estimated reading time: 18 min_
> **Prerequisite:** [Bulk Operations and Partial Success](./04-bulk-operations-and-partial-success.md)

## In one sentence

Read-after-write is a **routing guarantee**, not a hope: after a write, either **return the
written row**, read the **primary**, or **stick the session** until replication catches up — and
document the consistency each query actually provides.

## Why this matters in production

The most common "data loss" report in a read-replica architecture is not loss at all: the write
committed on the primary, and the next read hit a replica that was 200 ms behind. Users see their
edit vanish, re-save, and create duplicates. Authorization checks are worse: a user whose
suspension was just committed still reads `active` from a lagging replica. Repositories must make
the read source explicit per operation, because "the database" is no longer one thing.

## Core concept

```text
 write ──▶ PRIMARY ──(async replication)──▶ REPLICA ──▶ read
              │                                  ▲
              │        replication lag: ms–s     │
              └──────────── read-your-writes ────┘
                        must avoid this path
```

| Guarantee | Meaning | Mechanism |
| --------- | ------- | --------- |
| **Read-your-writes** | a client sees its own committed write | read primary / return written row / sticky session |
| **Monotonic reads** | a client never goes back in time | stick to one replica per session |
| **Consistent prefix** | reads see writes in order | ordered replication / primary reads |
| **Eventual** | replicas converge "soon" | async replication + lag budget |

### 24.14 Read-after-write

Three safe implementations, in order of preference:

1. **Return the written row** — `INSERT/UPDATE ... RETURNING *`, so no second read happens.
2. **Route the next read to the primary** — for a short window (e.g. 5 s) after a write, or for
   the specific query that needs it.
3. **Session stickiness** — pin the session to the primary until the replica's LSN/GTID catches
   up with the write's position.

```sql
-- Postgres: return the row instead of re-reading a replica.
UPDATE projects SET name = $1 WHERE id = $2
RETURNING id, name, version, updated_at;

-- Checking replica catch-up before trusting a read:
SELECT pg_current_wal_lsn() AS primary_lsn;      -- capture after commit
SELECT pg_last_wal_replay_lsn() AS replica_lsn;  -- on the replica
-- replica is caught up when replica_lsn >= primary_lsn
```

### 24.15 Consistency guarantees

Declare the guarantee **per repository method**, not per application:

| Method | Source | Guarantee | Rationale |
| ------ | ------ | --------- | --------- |
| `createProject` | primary | read-your-writes via `RETURNING` | user must see it |
| `getProjectForEdit` | primary | strong | editing stale data loses work |
| `listProjects` | replica | eventual (lag budget) | dashboards tolerate lag |
| `isTenantSuspended` | primary or versioned cache | strong | security decision |
| `searchProjects` | replica/search index | eventual | index lag acceptable |
| `findIdempotencyKey` | **primary** | strong | resolving ambiguity |

The repository should make the source visible in the method name or an option
(`{ readFrom: "primary" }`), so a reviewer can see the guarantee without tracing config.

## How it works (mechanics)

1. Write goes to the primary and commits at LSN `L`.
2. The application records `L` (or a timestamp, or an idempotency marker) for the session.
3. The next read either:
   - uses the primary, or
   - checks the replica's replay position and falls back to the primary if `replica < L`.
4. For list/dashboard reads, accept eventual consistency and **show a "last updated" time** if
   freshness matters to the user.
5. Never resolve an **ambiguous commit** from a replica — absence there proves nothing.

## Worked example

```ts
type ReadSource = "primary" | "replica";

class ProjectRepository {
  constructor(private primary: Db, private replica: Db) {}

  async update(tx: Tx, id: ProjectId, patch: ProjectPatch): Promise<Project> {
    // Primary + RETURNING: the caller never needs a follow-up read.
    const row = await tx.one(
      `UPDATE projects SET name=$1, version=version+1
        WHERE id=$2 RETURNING id, name, version, updated_at`,
      [patch.name, id],
    );
    return toProject(row);
  }

  async findForEdit(id: ProjectId, session: Session): Promise<Project | null> {
    // Read-your-writes window: stay on the primary briefly after a write.
    const db = session.wroteRecentlyWithin(5_000) ? this.primary : this.replica;
    const row = await db.maybeOne(`SELECT ... FROM projects WHERE id=$1`, [id]);
    return row ? toProject(row) : null;
  }

  async list(tenantId: TenantId): Promise<ProjectSummary[]> {
    // Explicitly eventual: dashboards can be a little stale.
    return this.replica.any(`SELECT ... FROM projects WHERE tenant_id=$1`, [tenantId]);
  }
}
```

```text
Acme dashboard, 200 ms replica lag:
  PATCH /projects/42  → 200 with the updated project (RETURNING)
  GET   /projects/42  → primary for 5 s after the write → correct
  GET   /projects     → replica → may be 200 ms stale, acceptable
  GET   /billing/entitlement → primary → never stale
```

## Key data / numbers

- Async replica lag: commonly **10 ms–1 s** same-region; cross-region **100 ms–2 s**.
- Read-your-writes window: **5 s** is a common heuristic; a proper LSN/GTID check is exact.
- `synchronous_commit=on` (Postgres default) protects durability, **not** replica freshness.
- `synchronous_standby_names` can make commit wait for a replica — higher latency, stronger
  freshness.
- MySQL: compare `@@global.gtid_executed` / `WAIT_FOR_EXECUTED_GTID_SET` for catch-up.
- Resolving ambiguity or idempotency **must** use the primary.

## Real-world use case — Acme SaaS

Acme moved project lists to a read replica. Immediately after a rename, the redirect to the
project page read from the replica and showed the old name; some users renamed twice. Support
logged it as "saves are lost". The fix was three lines of routing: `update()` returns
`RETURNING`, `findForEdit()` reads the primary inside a 5 s post-write window, and list views stay
on the replica with a visible "updated just now" indicator. "Lost saves" dropped to zero, and read
traffic stayed off the primary.

## Trade-offs

| Strategy | Correctness | Cost | When to use |
| -------- | ----------- | ---- | ----------- |
| Always read primary | strongest | no read scaling | auth, billing, edits |
| `RETURNING` written row | strong for that caller | none | write responses |
| Sticky session (5 s) | read-your-writes | slightly more primary load | user-facing edits |
| LSN/GTID catch-up check | exact | extra query/complexity | strict SLAs |
| Replica always | eventual | stale reads | dashboards, search |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return the written row with `RETURNING` | Re-read a replica immediately after a write |
| Declare the read source per method | Hide primary/replica choice in global config |
| Use the primary for auth and idempotency | Trust a lagging replica for security decisions |
| Measure replica lag | Assume async replication is instant |
| Show freshness when it matters | Silently serve stale data as current |

## Common mistakes

- **Write → commit → read replica** in the same request (classic "lost save").
- **Resolving an ambiguous commit from a replica** — false "not committed".
- **Entitlement checks on replicas** — suspended tenants keep access briefly.
- **No lag metric** — you cannot tune a budget you do not measure.
- **Session stickiness forever** — defeats the purpose of replicas; bound the window.

## Checklist

- [ ] Write responses use `RETURNING` or read the primary.
- [ ] Each repository method declares primary vs replica.
- [ ] Auth, billing, and idempotency always read the primary.
- [ ] Replica lag is measured against a documented budget.
- [ ] Read-your-writes windows are bounded and tested.

## Related

- [Failover, Replicas, and Unavailability (22.14–22.16)](../../22-database-error-classification/01-concepts/04-failover-replicas-and-unavailability.md)
- [Read-After-Write Consistency Mechanics](../02-deep-dive/02-read-after-write-and-consistency-mechanics.md)
- [Ambiguous Commit Outcomes](../../23-transaction-and-rollback-error-handling/02-deep-dive/01-ambiguous-commit-outcomes.md)
- [Consistency and Concurrency Failures (Ch. 40)](../../../part-15-distributed-failures/40-consistency-and-concurrency-failures/README.md)
