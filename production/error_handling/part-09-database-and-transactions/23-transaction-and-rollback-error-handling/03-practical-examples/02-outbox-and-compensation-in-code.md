# Outbox and Compensation in Code

> Part IX · Chapter 23 · Sections 23.15–23.17 · _Estimated reading time: 24 min_
> **Prerequisite:** [Outbox Mechanics and Cross-Store Consistency](../02-deep-dive/02-outbox-mechanics-and-cross-store-consistency.md)

## In one sentence

This is the `Checkout` implementation: **order + reservation + outbox commit atomically**, the
relay publishes, the consumer charges with an idempotency key, and a failed charge triggers
**idempotent compensation** instead of an impossible rollback.

## Why this matters in production

The naive version of this flow is five lines: insert order, charge card, update order, publish
event, send email. Every adjacent pair can fail independently, and the result is the three
classic billing bugs: charged but not fulfilled, fulfilled but not charged, and fulfilled twice.
The code below makes each transition explicit and each retry safe, so a crash at any line leaves
a recoverable state rather than a mystery.

## The state machine

```text
                 reserve + order(pending) + outbox
     ┌───────────────────────┐
     ▼                       │
  pending ──charge ok──▶ paid ──outbox('order.paid')──▶ fulfilled
     │
     ├──charge declined──▶ cancelled (compensate: release reservation)
     ├──ambiguous────────▶ payment_unknown (resolve with provider key)
     └──timeout──────────▶ pending (retry consumer)
```

**Every state is durable.** `payment_unknown` is a real state, not an error string. Nothing is
"rolled back" after commit; transitions and compensations move the state forward.

## Step 1 — schema

```sql
CREATE TABLE orders (
  id            bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  tenant_id     bigint NOT NULL,
  status        text   NOT NULL CHECK (status IN
                  ('pending','paid','cancelled','payment_unknown')),
  total_cents   bigint NOT NULL CHECK (total_cents > 0),
  created_at    timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE reservations (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id   bigint NOT NULL UNIQUE REFERENCES orders(id),
  sku        text   NOT NULL,
  qty        int    NOT NULL CHECK (qty > 0),
  released_at timestamptz
);

CREATE TABLE outbox (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  topic        text NOT NULL,
  aggregate_id text NOT NULL,
  payload      jsonb NOT NULL,
  created_at   timestamptz NOT NULL DEFAULT now(),
  published_at timestamptz
);
CREATE INDEX outbox_pending_idx ON outbox (created_at) WHERE published_at IS NULL;

CREATE TABLE idempotency_keys (
  key          text PRIMARY KEY,
  request_hash text NOT NULL,
  state        text NOT NULL,          -- in_progress | completed
  response     jsonb,
  expires_at   timestamptz NOT NULL
);
```

## Step 2 — the atomic write

```ts
import type { Pool } from "pg";

export async function createOrder(pool: Pool, req: CreateOrderRequest) {
  return pool.transaction(async (tx) => {
    // 1. Idempotency guard and the order in the SAME transaction.
    const key = await tx.query(
      `INSERT INTO idempotency_keys (key, request_hash, state, expires_at)
       VALUES ($1, $2, 'in_progress', now() + interval '7 days')
       ON CONFLICT (key) DO NOTHING`,
      [req.idempotencyKey, req.requestHash],
    );
    if (key.rowCount === 0) {
      const existing = await tx.one(
        `SELECT state, response FROM idempotency_keys WHERE key = $1`,
        [req.idempotencyKey],
      );
      if (existing.state === "completed") return existing.response as Order;
      throw new DomainError("REQUEST_IN_PROGRESS", { http: 409, transient: true });
    }

    // 2. Reserve inventory with the guard inside the statement.
    const reservation = await tx.one(
      `INSERT INTO reservations (order_id, sku, qty)
       SELECT $1, $2, $3
        WHERE (SELECT available - reserved FROM inventory WHERE sku = $2) >= $3
       RETURNING *`,
      [orderId, req.sku, req.qty],
    );
    if (!reservation) throw new DomainError("OUT_OF_STOCK", { http: 409 });

    // 3. Business row + event, atomically.
    const order = await tx.one(
      `INSERT INTO orders (tenant_id, status, total_cents)
       VALUES ($1, 'pending', $2) RETURNING *`,
      [req.tenantId, req.totalCents],
    );
    await tx.query(
      `INSERT INTO outbox (topic, aggregate_id, payload)
       VALUES ('order.created', $1, $2)`,
      [String(order.id), JSON.stringify({ orderId: order.id, sku: req.sku, qty: req.qty })],
    );
    await tx.query(
      `UPDATE idempotency_keys SET state='completed', response=$1 WHERE key=$2`,
      [JSON.stringify(order), req.idempotencyKey],
    );
    return order;
  });
}
```

## Step 3 — relay (at-least-once)

```ts
export async function relayOnce(db, broker, batch = 200) {
  await db.transaction(async (tx) => {
    const rows = await tx.any(
      `SELECT id, topic, aggregate_id, payload FROM outbox
        WHERE published_at IS NULL
        ORDER BY created_at
        LIMIT $1
        FOR UPDATE SKIP LOCKED`,
      [batch],
    );
    for (const row of rows) {
      await broker.publish(row.topic, row.payload, { eventId: row.id });
      await tx.query(`UPDATE outbox SET published_at = now() WHERE id = $1`, [row.id]);
    }
  });
}
```

Crash after `publish` and before `UPDATE` → duplicate event. The consumer dedupes on `eventId`.

## Step 4 — consumer charges idempotently

```ts
export async function onOrderCreated(event: OrderCreatedEvent) {
  const dedupe = await db.query(
    `INSERT INTO consumer_events (consumer, event_id)
     VALUES ('billing', $1) ON CONFLICT DO NOTHING`,
    [event.eventId],
  );
  if (dedupe.rowCount === 0) return;                  // already applied

  let result;
  try {
    result = await stripe.paymentIntents.create(
      { amount: event.totalCents, currency: "usd", metadata: { orderId: event.orderId } },
      { idempotencyKey: `order:${event.orderId}` },   // SAME key on every retry
    );
  } catch (err) {
    if (isDecline(err)) return compensate(event, "declined");
    throw err;                                        // timeout/5xx → retry consumer
  }

  await db.transaction(async (tx) => {
    await tx.query(`UPDATE orders SET status='paid' WHERE id=$1 AND status='pending'`,
                   [event.orderId]);
    await tx.query(
      `INSERT INTO outbox (topic, aggregate_id, payload)
       VALUES ('order.paid', $1, $2)`,
      [String(event.orderId), JSON.stringify({ orderId: event.orderId, paymentId: result.id })],
    );
  });
}
```

## Step 5 — compensation

```ts
export async function compensate(event: OrderCreatedEvent, reason: string) {
  await db.transaction(async (tx) => {
    const order = await tx.one(
      `UPDATE orders SET status='cancelled'
        WHERE id=$1 AND status='pending' RETURNING *`,
      [event.orderId],
    );
    if (!order) return;                               // already resolved — idempotent

    await tx.query(
      `UPDATE reservations SET released_at = now()
        WHERE order_id = $1 AND released_at IS NULL`,
      [event.orderId],
    );
    await tx.query(
      `INSERT INTO outbox (topic, aggregate_id, payload)
       VALUES ('order.cancelled', $1, $2)`,
      [String(event.orderId), JSON.stringify({ orderId: event.orderId, reason })],
    );
  });
}
```

Every compensation step is guarded (`status='pending'`, `released_at IS NULL`), so a retried
compensation cannot cancel twice or release inventory twice.

## Key data / numbers

- `FOR UPDATE SKIP LOCKED` for the relay; batch **200**; poll **200–500 ms**.
- Stripe `Idempotency-Key`: **one per logical order**, reused across attempts; replay window
  **24 h**.
- `orders.status` includes **`payment_unknown`** for provider timeouts — resolve by querying the
  payment intent, not by retrying the charge.
- Idempotency-key TTL: **7 days**; consumer dedupe rows retained **≥ the event retention**.
- Compensation must be callable **N times** with the same result.

## Real-world use case — Acme SaaS

Acme shipped the naive five-line checkout. Within a month: 14 customers charged for `cancelled`
orders (charge succeeded, update failed), 6 orders marked `paid` without a charge (update
succeeded, charge timed out and was never retried), and 3 duplicate charges from a retried
webhook. The state machine above, plus outbox and provider idempotency keys, removed all three:
`paid` now implies a charge recorded from the provider, `cancelled` always releases inventory
exactly once, and replays are no-ops. Refund volume from duplicate charges went to zero.

## Trade-offs

| Decision | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Synchronous charge in request | immediate result | slow request, ambiguous on timeout | low-risk payments |
| Async charge via outbox consumer | resilient, retriable | user waits for webhook/poll | default for scale |
| Compensation vs auto-refund | explicit audit | slower resolution | financial flows |
| Stripe idempotency + local key | double protection | two records to keep | payments |
| `payment_unknown` state | honest, resolvable | extra UI state | provider timeouts |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Commit order + reservation + outbox together | Charge the card inside the DB transaction |
| Reuse `order:{id}` on every charge attempt | Generate a new idempotency key per retry |
| Guard compensation with state predicates | Refund/release unconditionally |
| Put `payment_unknown` in the schema | Encode it as a generic `500` |
| Dedupe consumer events on `eventId` | Assume the relay delivers once |

## Common mistakes

- **Charging before the order is committed** — orphan charges.
- **Updating `paid` without checking `status='pending'`** — a late decline overwrites a paid
  order.
- **Compensation without a state guard** — duplicate refunds.
- **No `payment_unknown` state** — ambiguous outcomes become support tickets.
- **Publishing `order.paid` inline** — lost events on broker failure.

## Checklist

- [ ] Order, reservation, idempotency record, and outbox commit in one transaction.
- [ ] Charge happens after commit, with a stable provider idempotency key.
- [ ] Consumer dedupes on `eventId`.
- [ ] Compensation is state-guarded and idempotent.
- [ ] `payment_unknown` is a first-class state with a resolver.
- [ ] Inventory guard is inside the SQL statement.

## Related

- [After-Commit Failures, Outbox, and Cross-Store (23.15–23.20)](../01-concepts/05-after-commit-failures-outbox-and-cross-store.md)
- [Outbox Mechanics and Cross-Store Consistency](../02-deep-dive/02-outbox-mechanics-and-cross-store-consistency.md)
- [Ambiguous Commit Outcomes](../02-deep-dive/01-ambiguous-commit-outcomes.md)
- [Billing and Subscription Workflows (Ch. 42)](../../../part-16-specialized-saas-scenarios/42-auth-billing-and-subscription-workflows/README.md)
