# Ambiguous Commit Outcomes

> Part IX · Chapter 23 · Sections 23.11, 23.12, 23.19 · _Estimated reading time: 25 min_
> **Prerequisite:** [Ambiguous Commits and Idempotent Retries](../01-concepts/04-ambiguous-commits-and-idempotent-retries.md)

## In one sentence

An **ambiguous outcome** is a durable `unknown`: the transaction may be committed, the client
cannot tell, and the only correct resolution is to **reconnect and read a marker that was written
inside the same transaction**.

## Why this matters in production

Every retry decision downstream depends on this one classification. Treat unknown as failure and
you retry committed writes (double charge). Treat it as success and you return a receipt for a
write that never happened. Both are silent data corruption. The good news: ambiguity is
**bounded and resolvable** if you planned a marker. The bad news: it is invisible in local tests
unless you deliberately kill the socket at the right moment.

## The exact failure window

```text
  app                       TCP                      postgres
   │  BEGIN ────────────────▶│──────────────────────▶│
   │  INSERT/UPDATE ────────▶│──────────────────────▶│
   │  COMMIT ───────────────▶│──────────────────────▶│ flush WAL, fsync, commit
   │                         │                      │
   │                    ✗ connection dies  ◀─────────│ send CommandComplete
   │                         │                      │
   │  "connection error"     │                      │  COMMITTED
   ▼                         ▼                      ▼
        client knowledge: UNKNOWN        server state: COMMITTED
```

Three distinct cases hide behind "connection error":

| Case | Server state | Client sees | Resolution |
| ---- | ------------ | ----------- | ---------- |
| died **before** commit record | not committed | `08006` | marker absent → safe to retry |
| died **after** commit, before ack | committed | `08006`/`08007` | marker present → return result |
| died **during** 2PC prepare | in-doubt / prepared | `08007` | query `pg_prepared_xacts`, resolve manually |

## The resolution algorithm

```text
on commit error:
  if error is a constraint / definite server rejection:
      → NOT_COMMITTED, translate, do not retry
  if error is connection loss / timeout / 08007:
      → UNKNOWN
         reconnect to PRIMARY
         SELECT ... WHERE idempotency_key = $1
           row exists, state=completed  → COMMITTED (return stored response)
           row exists, state=in_progress → IN_PROGRESS (409/202, retry later)
           row absent, within safety window → wait briefly, read again
           still absent → NOT_COMMITTED (retry once, idempotently)
           cannot read → stay UNKNOWN, alert + reconcile
```

**Never skip the read.** The marker is proof. Time-based guessing ("it's been 5 seconds") is a
heuristic, not a resolution.

## Designing the marker

The marker has to be durable **in the same transaction**, unique per logical operation, and
readable without side effects.

```sql
CREATE TABLE idempotency_keys (
  key           text PRIMARY KEY,              -- client/operation supplied
  request_hash  text NOT NULL,                 -- detect key reuse with a different payload
  state         text NOT NULL,                 -- 'in_progress' | 'completed' | 'failed'
  response      jsonb,                         -- serialized result for replay
  created_at    timestamptz NOT NULL DEFAULT now(),
  expires_at    timestamptz NOT NULL DEFAULT now() + interval '7 days'
);
```

Rules:

- The **primary key** on `key` makes the insert itself the dedupe (`23505` = already started).
- `state='completed'` is written **in the same transaction** as the business effect — so
  "row completed" and "effect applied" are one atomic fact.
- `request_hash` catches a reused key with a different body: return `409`, not the old response.
- `expires_at` prevents unbounded growth; purge expired rows offline.
- Read the marker from the **primary**. A replica can be seconds behind and tell you "no row"
  for a committed operation.

## Worked example (TypeScript, pg)

```ts
type Outcome<T> =
  | { status: "committed"; value: T }
  | { status: "not_committed"; error: DomainError }
  | { status: "in_progress" }
  | { status: "unknown"; error: DomainError };

async function commitOrder(pool: Pool, req: OrderRequest): Promise<Outcome<Order>> {
  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    await client.query(
      `INSERT INTO idempotency_keys (key, request_hash, state)
       VALUES ($1, $2, 'in_progress')`,
      [req.key, req.hash],
    );
    const { rows } = await client.query(
      `INSERT INTO orders (tenant_id, total_cents, status)
       VALUES ($1, $2, 'pending') RETURNING *`,
      [req.tenantId, req.totalCents],
    );
    await client.query(
      `UPDATE idempotency_keys SET state='completed', response=$1 WHERE key=$2`,
      [JSON.stringify(rows[0]), req.key],
    );
    await client.query("COMMIT");
    return { status: "committed", value: rows[0] };
  } catch (err) {
    const db = normalize(err);
    if (isDefiniteRejection(db)) {
      await safeRollback(client);
      return { status: "not_committed", error: classify(db, { resource: "orders:create" }) };
    }
    if (isAmbiguousCommit(db)) {                 // 08006, 08007, 2013, socket reset on COMMIT
      return resolve(pool, req);
    }
    await safeRollback(client);
    return { status: "not_committed", error: classify(db, { resource: "orders:create" }) };
  } finally {
    client.release();                            // discard if broken (see below)
  }
}

async function resolve(pool: Pool, req: OrderRequest): Promise<Outcome<Order>> {
  const { rows } = await pool.query(
    `SELECT state, response FROM idempotency_keys WHERE key = $1`,
    [req.key],
  );
  if (rows.length === 0) return { status: "not_committed", error: markerAbsent(req.key) };
  if (rows[0].state === "completed") {
    return { status: "committed", value: rows[0].response as Order };
  }
  if (rows[0].state === "in_progress") return { status: "in_progress" };
  return { status: "not_committed", error: markerFailed(req.key) };
}
```

> ⚠️ **Hazard.** `client.release()` on a connection whose socket died returns a dead connection
> to the pool. Call `client.release(true)` (node-pg: destroy) or close it, or the next request
> inherits the failure.

## External effects (`23.19`)

The same shape applies outside the database:

| Effect | Ambiguous signal | Resolution |
| ------ | ---------------- | ---------- |
| Stripe charge | timeout after request sent | reuse the **same** `Idempotency-Key`; provider returns the original result |
| S3 `PutObject` | connection reset | deterministic key + `HEAD`/`GET` to check existence |
| Queue publish | ack timeout | publish with `event_id`; consumer dedupe (or outbox) |
| Email provider | timeout | dedupe key + provider query, or accept at-least-once |

Store `external_state='unknown'` rather than inventing a boolean. A reconciliation job resolves
it later.

## Two-phase commit and prepared transactions

Postgres `PREPARE TRANSACTION` creates an **in-doubt** transaction that survives a crash and
holds locks until `COMMIT PREPARED` or `ROLLBACK PREPARED`. If the coordinator dies, you must
resolve it manually:

```sql
SELECT gid, prepared, owner, database FROM pg_prepared_xacts;
-- then, after verifying with the coordinator:
COMMIT PREPARED 'txn_9f2';   -- or ROLLBACK PREPARED
```

In-doubt transactions hold locks and block vacuum; alert if `pg_prepared_xacts` is non-empty.
Most SaaS apps should avoid 2PC and use outbox/saga instead.

## Key data / numbers

- `08007 transaction_resolution_unknown` — the standard code for "cannot determine".
- MySQL `2013` (lost connection during query) and `2006` (server gone away) are the analogous
  signals; treat as unknown **only when the lost statement was `COMMIT`**.
- Stripe idempotency replay window: **24 hours**; dedupe your own records longer if you reconcile.
- Stripe does not allow reusing an idempotency key with different parameters — a `409`-style
  error is returned.
- Safety window before declaring "not committed": at least one **read after reconnect plus a
  short delay** (e.g. 200–500 ms) to let a lagging commit land; never a single immediate read.
- Prepared transactions: monitor `pg_prepared_xacts`; any row older than minutes is an incident.

## Real-world use case — Acme SaaS

Acme's `Checkout` mapped every `08006` to `DB_UNAVAILABLE` and retried the whole request. After
a failover, three customers were charged twice because the first `COMMIT` had already succeeded.
Adding the idempotency marker, a dedicated `unknown` branch, and a primary read-back reduced
duplicate charges to **zero** across the next two failovers. The metric `checkout.commit_unknown`
now alerts the team, and the reconciliation job resolves any marker that stays `in_progress` for
more than 60 seconds.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Idempotency table | exact resolution, replay | extra write per operation | payments, orders |
| Unique business key | no extra table | needs a natural unique key | webhooks, imports |
| Deterministic external key | no read needed for provider | only works for supporting providers | Stripe/S3 |
| Heuristic time-based guess | no schema change | **wrong by construction** | never |
| Async reconciliation only | decouples request | user waits; needs a job | high volume, non-interactive |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Treat unknown as a first-class state | Map it to success or failure |
| Resolve by reading the primary | Read a replica to decide |
| Write the marker in the same transaction | Write it after commit |
| Reuse the same idempotency key on retry | Generate a fresh key per attempt |
| Destroy broken connections | Return them to the pool |
| Alert on `08007` | Ignore it as a network blip |

## Common mistakes

- **Conflating "commit returned an error" with "not committed."**
- **Using a new idempotency key per attempt** — resolution never matches.
- **Checking the marker on a replica** — false "not committed".
- **Leaving `in_progress` rows forever** — no reconciliation, locked business flows.
- **Ignoring `pg_prepared_xacts`** — locks and bloat accumulate silently.

## Checklist

- [ ] There is a named `unknown` outcome type in the code.
- [ ] The idempotency marker commits atomically with the effect.
- [ ] Resolution reads the primary and distinguishes completed/in-progress/absent.
- [ ] External effects use provider idempotency keys or deterministic keys.
- [ ] Broken connections are destroyed, not pooled.
- [ ] `unknown` and in-doubt/prepared transactions are alerted and reconciled.

## Related

- [Ambiguous Commits and Idempotent Retries](../01-concepts/04-ambiguous-commits-and-idempotent-retries.md)
- [Outbox Mechanics and Cross-Store Consistency](./02-outbox-mechanics-and-cross-store-consistency.md)
- [Idempotency and Duplicate-Operation Safety (Ch. 28)](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Lost Responses After Success (26.15)](../../../part-10-external-dependencies/26-network-and-distributed-communication-errors/README.md)
