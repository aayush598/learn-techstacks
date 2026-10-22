# Transaction Boundaries and Atomicity (23.1, 23.2)

> Part IX · Chapter 23 · Sections 23.1, 23.2 · _Estimated reading time: 18 min_
> **Prerequisite:** [Database Error Classification](../../22-database-error-classification/README.md)

## In one sentence

A transaction boundary is a **deliberate architectural line** that says "these writes succeed or
fail together", and atomicity is only as strong as the **set of effects you put inside it** — one
external API call outside the boundary and the promise is already broken.

## Why this matters in production

Most "transaction bugs" are boundary bugs. Too small a boundary (order inserted, inventory
decremented in a second transaction) leaves a window where one succeeds and the other fails. Too
large a boundary holds locks across a Stripe call and turns a 300 ms payment into a 30 s lock,
starving every other checkout. And a boundary that includes an external side effect gives you
**atomicity you cannot roll back**. Choosing the boundary is a design decision, not a framework
setting.

## Core concept

```text
Request ─────────────────────────────────────────────────────────────▶
   │
   ├── BEGIN ────────────────────────────────────────────── COMMIT ──┐
   │     insert order                                                 │
   │     decrement inventory        ← inside: atomic, rollback-able   │
   │     write outbox row                                             │
   └──────────────────────────────────────────────────────────────────┘
         charge card  ← outside: NOT atomic, needs idempotency + compensation
         send email   ← outside: best-effort, retriable, may duplicate
         publish event← outside: use outbox, never publish inline
```

| Property | Guarantees | Does **not** guarantee |
| -------- | ---------- | ---------------------- |
| **Atomicity** | All statements in the txn apply or none do | Anything about external systems |
| **Consistency** | Constraints hold at commit | Cross-store consistency |
| **Isolation** | Concurrent txns see a defined snapshot | No lost updates (depends on level) |
| **Durability** | Committed data survives crash | That the client learned it committed |

### 23.1 Choosing boundaries

A boundary should contain **exactly one business invariant's worth of writes**. Practical rules:

| Rule | Why |
| ---- | --- |
| One request → one transaction per aggregate | Keeps locks short; avoids cross-aggregate contention |
| Never hold a transaction across a network call | Lock time grows with provider latency |
| Put "change + announce" in the same txn via **outbox** | Events cannot be lost or invented |
| Multi-aggregate workflows → **saga/compensation**, not one giant txn | Long locks, distributed failure |
| Read-only queries → no explicit txn (or a short one) | Snapshot consistency where needed |

### 23.2 Atomicity in practice

```sql
-- Acme Checkout: one atomic unit
BEGIN;
  INSERT INTO orders (id, tenant_id, status, total_cents)
  VALUES ($1, $2, 'pending', $3);

  UPDATE inventory
     SET reserved = reserved + $4
   WHERE sku = $5 AND available - reserved >= $4;   -- guard inside the txn
  -- rowCount = 0 → not enough stock → ROLLBACK

  INSERT INTO outbox (id, topic, payload)
  VALUES ($6, 'order.created', $7);                 -- same txn as the order
COMMIT;                                              -- one durable outcome
```

If the guard affects zero rows, you must **abort** — continuing would create an order with no
reservation. That is atomicity doing its job.

> ⚠️ **Hazard.** `SELECT ...; if (ok) UPDATE ...` inside `READ COMMITTED` is **not** atomic:
> another transaction can change the row between the read and the write. Put the condition in the
> `UPDATE`/`DELETE` predicate or lock the row (`FOR UPDATE`).

## How it works (mechanics)

1. `BEGIN` starts a transaction; the database assigns a snapshot (isolation-dependent).
2. Statements acquire locks; constraint checks may be deferred to `COMMIT`.
3. `COMMIT` writes the commit record (WAL/binlog). **Durability is achieved at this point**,
   not when the client receives the acknowledgment.
4. `ROLLBACK` discards the transaction's changes. Locks release.
5. If the process dies **before** `COMMIT`, the server rolls back on connection loss.
6. If the process dies **after** `COMMIT` but before responding, the data is committed and the
   caller does not know — the **ambiguous outcome** of §23.12.

## Worked example

```ts
// Boundary that is correct: DB writes + outbox in one txn, external call after commit.
async function placeOrder(input: OrderInput) {
  const order = await db.transaction(async (tx) => {
    const reserved = await tx.query(
      `UPDATE inventory SET reserved = reserved + $1
        WHERE sku = $2 AND available - reserved >= $1`,
      [input.qty, input.sku],
    );
    if (reserved.rowCount === 0) throw new DomainError("OUT_OF_STOCK", 409);

    const o = await tx.one(
      `INSERT INTO orders (tenant_id, status, total_cents)
       VALUES ($1, 'pending', $2) RETURNING *`,
      [input.tenantId, input.totalCents],
    );
    await tx.query(
      `INSERT INTO outbox (topic, payload) VALUES ('order.created', $1)`,
      [JSON.stringify({ orderId: o.id })],
    );
    return o;
  });

  // Outside the transaction: external effect with its own idempotency key.
  await payments.charge({ orderId: order.id, amount: order.totalCents,
                          idempotencyKey: `order:${order.id}` });
  return order;
}
```

The external charge is **not** rolled back if it fails after the order commits — instead the
order stays `pending` and a compensation/retry path resolves it (see `05-after-commit`).

## Key data / numbers

- Postgres default isolation is **`READ COMMITTED`**; `SERIALIZABLE` is opt-in per transaction.
- A commit is durable once the **WAL flush** completes; `synchronous_commit=on` (default) waits
  for it, `off` trades durability for latency.
- Practical transaction duration target: **< 100 ms**; anything over **1 s** on a hot path is a
  lock-contention incident waiting to happen.
- `idle_in_transaction_session_timeout` (Postgres) closes abandoned transactions — set it
  (commonly 30–60 s) so a leaked `BEGIN` cannot pin locks forever.

## Real-world use case — Acme SaaS

Acme's `Checkout` originally did: `INSERT order` → `COMMIT` → `charge card` → `UPDATE order SET
paid`. If the charge succeeded and the update failed, the customer was charged for a `pending`
order — the classic boundary bug. Moving the order state and an **outbox event** into one
transaction, then charging **after** commit with `idempotencyKey=order:{id}`, meant every
outcome became recoverable: no charge → retry; charge succeeded but update lost → the relay
replays `order.created` and reconciliation marks it paid. Duplicate charges went to zero.

## Trade-offs

| Boundary choice | Pros | Cons | When to use |
| --------------- | ---- | ---- | ----------- |
| One txn per aggregate | short locks, clear | needs saga across aggregates | default |
| One big txn across aggregates | simple atomicity | long locks, deadlocks | tiny/low-traffic flows |
| Txn + outbox | no lost events | relay lag, extra table | any event on commit |
| Txn + inline publish | lowest latency | lost events, phantom events | **never** |
| Txn per batch item | partial success possible | more round trips | imports/exports |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep external calls outside the transaction | Hold a txn open across Stripe/S3 |
| Put the invariant in the SQL predicate | `SELECT` then `UPDATE` without a lock |
| Write events to an outbox in the same txn | Publish to a queue before commit |
| Set `idle_in_transaction_session_timeout` | Leave `BEGIN` open waiting on user input |
| Use sagas for multi-aggregate work | One giant transaction across services |

## Common mistakes

- **Commit-then-side-effect** with no compensation — the standard double-charge bug.
- **`SELECT`-then-`UPDATE`** under `READ COMMITTED` — lost update.
- **Long transactions** caused by awaiting user input or an HTTP call.
- **Assuming rollback covers the external world** — it only covers the database.
- **Nested `BEGIN`** in a driver that silently ignores it, giving fake atomicity.

## Checklist

- [ ] Every write path has an explicit transaction boundary.
- [ ] No network call occurs inside a transaction.
- [ ] Invariants are enforced in SQL predicates or with locks, not read-then-write.
- [ ] Events are written to an outbox, not published inline.
- [ ] Transaction duration is measured and alerted.

## Related

- [Commit, Rollback, and Savepoints (23.3–23.6)](./02-commit-rollback-and-savepoints.md)
- [Outbox Mechanics and Cross-Store Consistency](../02-deep-dive/02-outbox-mechanics-and-cross-store-consistency.md)
- [Failure Domains and Fault Boundaries (1.16)](../../../part-01-foundations/01-understanding-errors-and-failures/02-deep-dive/01-failure-domains-and-fault-boundaries.md)
- [Chapter 23 Reference](../05-reference/README.md)
