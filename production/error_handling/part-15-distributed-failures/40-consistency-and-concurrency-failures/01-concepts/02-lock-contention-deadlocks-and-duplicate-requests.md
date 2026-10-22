# Lock Contention, Deadlocks, and Concurrent Duplicate Requests (40.4–40.7)

> Part XV · Chapter 40 · Sections 40.4–40.7 · _Estimated reading time: 24 min_
> **Prerequisite:** [Races, Optimistic Control, and Version Conflicts (40.1–40.3)](./01-races-optimistic-control-and-version-conflicts.md)

## In one sentence

**Lock contention** is waiting, **deadlock** is waiting in a circle (the database picks a victim
and returns `40P01`/`1213`), and **concurrent duplicates** are two requests both succeeding at
"create one" — a bug the unique constraint, not the code, must catch.

## Why this matters in production

Contention is not an error you can avoid; it is load. What separates a healthy system from an
outage is what happens under contention: a deadlock that retries cleanly is invisible, a deadlock
that surfaces as `500` pages someone at 3 a.m.; a duplicate subscription created by two concurrent
`POST /subscriptions` becomes a refund and a support thread; a lock wait that runs to the
database's 50-second default turns one slow request into a pool exhaustion cascade. These four
failure modes (40.4–40.7) are the ones that turn **normal load into incidents**.

## Core concept

### 40.4 Lock contention

| Signal | What it means | Typical source |
|--------|---------------|----------------|
| Requests queueing on one row | hot row (counter, tenant, quota) | bad data model, broadcast update |
| `55P03 lock_not_available` (Postgres) | your `lock_timeout` expired while waiting | long transactions, missing index |
| `1205 Lock wait timeout exceeded` (MySQL) | `innodb_lock_wait_timeout` (default **50 s**) expired | same |
| Rising `p99` with flat throughput | everyone is waiting, not working | lock convoy, too-long critical section |
| Pool exhaustion under load | waiters hold connections while waiting | **waiting while holding a connection** |

Rules that keep contention survivable:

1. **Keep transactions short** — no network calls, no HTTP, no LLM calls inside a transaction that
   holds locks.
2. **Always set `lock_timeout`** (`SET LOCAL lock_timeout = '2s'`) so a wait becomes a fast,
   retryable `55P03` instead of a 50-second hang.
3. **Lock in a consistent order** (by id, ascending) — the cheapest deadlock prevention there is.
4. **Separate the waiters from the holders**: a connection pool where every waiter holds a
   connection is a self-inflicted outage.

### 40.5 Deadlock detection and recovery

```text
T1: UPDATE orders SET ... WHERE id=10      T2: UPDATE orders SET ... WHERE id=11
T1: UPDATE orders SET ... WHERE id=11  ── waits ── T2: UPDATE orders SET ... WHERE id=10
        └──────────── circular wait ────────────────┘
DB detects (Postgres: after deadlock_timeout, default 1 s) → aborts ONE victim
victim receives: SQLSTATE 40P01 deadlock_detected (MySQL: error 1213)
```

The contract for deadlocks is fixed and simple:

- **`40P01` / `1213` are retryable** — always, because the abort left no partial state.
- **Retry the whole transaction**, re-reading all state (never just the failed statement).
- **Bump `lock_timeout`** so non-deadlock waits also become retryable instead of hanging.
- **Prevent structurally**: total lock order, small transactions, unique index instead of
  "check-then-insert."
- Deadlock **victim choice is the database's**, not yours; you can influence it (e.g.
  `deadlock_timeout`, statement priority) but you must handle being the victim either way.

Serialization conflicts at `READ COMMITTED`+`REPEATABLE READ`/`SERIALIZABLE` are the same story
with a different SQLSTATE: **`40001 serialization_failure`** — also retryable, also whole-
transaction.

### 40.6 Concurrent duplicate requests

Two identical requests arrive (client retry, double-click, two pods behind a load balancer, a
webhook redelivery). Both pass validation; both try to create. Three defenses, in order of
strength:

| Defense | Mechanism | Failure it prevents |
|---------|-----------|---------------------|
| **Idempotency key** | `Idempotency-Key` stored with the result; second request replays the stored response | double charge, double create across retries |
| **Unique constraint** | `UNIQUE(tenant_id, external_id)` / `UNIQUE(order_id)` → `23505` | duplicate rows even if keys were forgotten |
| **Guarded insert** | `INSERT ... ON CONFLICT DO NOTHING` + read-back | check-then-insert races |

⚠️ **Hazard.** `23505` is **not** a transient error and must never be retried as one — but it *is*
the correct detector for a concurrent duplicate. Translate it deliberately:
"unique violation because *my own* key already exists" → **replay the stored result**; "unique
violation on a natural key the client chose" → **`409`/`422`**.

### 40.7 Concurrent creation

"Create if not exists" is the race that unique constraints exist for:

```sql
-- WRONG: TOCTOU — two requests both see "not exists"
SELECT 1 FROM subscriptions WHERE tenant_id=$1 AND plan=$2;   -- both get NULL
INSERT INTO subscriptions (...) VALUES (...);                 -- both insert → 2 rows or 23505

-- RIGHT: the database decides, exactly once
INSERT INTO subscriptions (tenant_id, plan, status)
VALUES ($1, $2, 'active')
ON CONFLICT (tenant_id, plan) DO UPDATE SET updated_at = now()   -- or DO NOTHING + read
RETURNING *;
```

For creations that carry external effects (a payment, an email), the order matters:

```text
1. INSERT the row (unique + state='pending')      ← the linearization point
2. on 23505 → read the existing row:
     state='active'   → replay stored success (idempotent duplicate)
     state='pending'  → 409 REQUEST_IN_PROGRESS (another request is mid-flight)
     state='failed'   → decide: clean up then retry, or return the stored error
3. only after the insert wins → perform the external effect, keyed by the row id
```

## Worked example

```ts
// One flow handles deadlock retry AND duplicate-create correctly.
export async function createSubscription(input: SubInput): Promise<Sub> {
  const key = input.idempotencyKey;                      // client-supplied, per operation
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      return await withTransaction(async (tx) => {
        await tx.query(`SET LOCAL lock_timeout = '2s'`);
        const idem = await tx.query(
          `INSERT INTO idempotency_keys (key, request_hash, state)
           VALUES ($1,$2,'in_progress') ON CONFLICT (key) DO NOTHING RETURNING key`,
          [key, hash(input)]);
        if (idem.rowCount === 0) {                       // someone with this key got here first
          const row = await tx.one(`SELECT state, response FROM idempotency_keys WHERE key=$1`, [key]);
          if (row.state === "completed") return replay(row.response);
          throw new DomainError("REQUEST_IN_PROGRESS", { http: 409, transient: true });
        }
        const sub = await tx.one(
          `INSERT INTO subscriptions (tenant_id, plan, status)
           VALUES ($1,$2,'active') RETURNING *`, [input.tenantId, input.plan]);
        await tx.query(
          `UPDATE idempotency_keys SET state='completed', response=$2 WHERE key=$1`,
          [key, sub]);
        return sub;
      }, { label: "subscriptions:create" });             // wrapper retries 40001/40P01
    } catch (err) {
      const e = classify(err);
      if (e.code === "UNIQUE_VIOLATION_ON_NATURAL_KEY")  // 23505 on (tenant_id, plan)
        throw new DomainError("SUBSCRIPTION_EXISTS", { http: 409 });
      if (!e.retryable || attempt === 3) throw e;        // preserves the final failure
      await sleep(backoff(attempt));                     // 25 ms base, full jitter
    }
  }
  throw new Error("unreachable");
}
```

```text
Trace — two identical POSTs at the same millisecond:
  req A: INSERT idempotency_keys key='sub_7f1' → rowCount=1 → INSERT subscriptions → 200
  req B: INSERT idempotency_keys key='sub_7f1' → rowCount=0 → SELECT → state='in_progress'
          → 409 REQUEST_IN_PROGRESS (transient)
  req B retry (150 ms later) → state='completed' → replays A's response → 200 (same body)
  Net: one subscription, one charge, identical response bodies.
```

## Key data / numbers

- Retryable SQLSTATEs: **`40001`** serialization_failure, **`40P01`** deadlock_detected,
  **`55P03`** lock_not_available (when *you* set `lock_timeout`); MySQL **`1213`** deadlock,
  **`1205`** lock wait.
- Non-retryable but meaningful: **`23505`** unique_violation (duplicate detector), **`23503`**
  foreign_key_violation.
- Postgres `deadlock_timeout` default **1 s**; MySQL `innodb_lock_wait_timeout` default **50 s** —
  set your own `lock_timeout` of **1–2 s** and treat expiry as retryable.
- Deadlock/contention retry: **3 attempts**, base **25–50 ms**, full jitter, whole transaction.
- Duplicate-create protection: **both** an idempotency key and a unique constraint — keys can be
  forgotten, constraints cannot.
- `ON CONFLICT`/`UPSERT` is atomic; `SELECT`-then-`INSERT` is a race, always.

## Real-world use case — Acme SaaS

Acme's `POST /v1/projects` had a `SELECT ... if exists then error` check. Under a marketing
automation that created projects for 300 tenants in parallel, duplicate project rows appeared for
~0.7% of requests: two requests both saw "absent," both inserted. There was no unique constraint,
so the duplicates were legal forever — and one tenant ended up with two billing entities. The fix:
`UNIQUE(tenant_id, slug)` plus `INSERT ... ON CONFLICT DO NOTHING RETURNING`, mapping the conflict
to `409 SLUG_TAKEN`, and `lock_timeout='2s'` so the accompanying deadlock retries surfaced as
clean `40P01` retries instead of 50-second hangs. Duplicates: zero. p99 under the same load fell
because lock waits stopped running to the MySQL default.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Pessimistic locks (`FOR UPDATE`) | deterministic single winner | waits, deadlocks, connection pressure | short, high-contention critical sections |
| Optimistic + `409` | no waits, scales | wasted work under heavy contention | most APIs, human-paced writes |
| Unique constraint as the arbiter | correctness even under races | client must handle `23505`→`409`/replay | every "create" operation |
| Idempotency key + replay | exact-once semantics for clients | storage + TTL policy | payments, external-effect creates |
| Retry everything on `500` | simple | amplifies deadlocks into an outage | never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Set `lock_timeout` on every transaction | Wait 50 s by default and call it "reliable" |
| Lock rows in a consistent, documented order | Lock in whatever order the code happened to read |
| Retry `40001`/`40P01`/`1213` as whole transactions | Retry only the failed statement |
| Treat `23505` as a duplicate detector, not noise | Retry `23505` until the constraint gives up |
| Do network I/O outside transactions | Hold row locks across an HTTP call |
| Return `409` for concurrent create conflicts | Return `500` for a duplicate key |

## Common mistakes

- **"Check then insert" without a unique constraint** — a race you cannot win.
- **Retrying `23505` as transient** — it fails every time; classify it.
- **Retrying only the deadlocked statement** — the transaction is aborted (`25P02` in Postgres);
  you must re-`BEGIN`.
- **Two layers retrying deadlocks** (repository + service) — 3 × 3 attempts of amplification.
- **Holding a pooled connection while waiting on a lock** — every waiter starves everyone;
  shrink the transaction instead.
- **Auto-increment ids created inside the retried transaction** — harmless but wasteful; more
  importantly, *captured outside values* reused on retry re-create the original conflict.

## Checklist

- [ ] `lock_timeout` is set (1–2 s) and its expiry is classified retryable.
- [ ] Deadlock retries are owned by exactly one layer and re-run the whole transaction.
- [ ] Every create has a unique constraint **and** an idempotency key path.
- [ ] `23505` maps to replay-or-`409`, never to a blind retry or bare `500`.
- [ ] Lock order is documented and consistent across code paths.
- [ ] No external I/O happens while a transaction holds locks.
- [ ] Deadlock/conflict rates are monitored with attempt counts.

## Related

- [Optimistic Concurrency vs Deadlock — deep dive](../02-deep-dive/01-optimistic-concurrency-vs-deadlock.md)
- [Conflict Resolution, Retry Safety, and Corruption (40.13–40.15)](./05-conflict-resolution-retry-safety-and-corruption.md)
- [Retrying 40001 and 40P01 in Code](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/03-practical-examples/01-retrying-40001-and-40p01.md)
- [Idempotency Keys and Duplicate Detection](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/01-concepts/02-idempotency-keys-and-duplicate-detection.md)
