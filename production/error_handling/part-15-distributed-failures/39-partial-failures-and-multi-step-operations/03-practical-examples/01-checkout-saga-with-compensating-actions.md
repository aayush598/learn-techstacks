# Checkout Saga with Compensating Actions

> Part XV · Chapter 39 · Sections 39.7, 39.8, 39.13–39.16 · _Estimated reading time: 30 min_
> **Prerequisite:** [Saga and Compensation Mechanics](../02-deep-dive/01-saga-and-compensation-mechanics.md)

## In one sentence

This file builds the **`Checkout` saga end to end** — durable steps, idempotent compensations, a
`blocked` escalation, and failure injection — so you can copy the shape into your own workflow.

## Why this matters in production

Most teams write the happy path first and add compensation "later." Later is after the first
double refund. The example below is deliberately boring: a table, a state machine, one runner, and
a compensations ledger. It is the minimum machinery that makes `Checkout` safe when Stripe is
slow, a pod dies mid-flight, or an operator cancels a half-finished order.

## The saga

```text
Checkout (orchestrated, 4 forward steps + compensations)

  T1 reserve_inventory   ── C1 release_inventory
  T2 charge_payment      ── C2 refund_payment          ← money: two safety layers
  T3 activate_subscription ── C3 cancel_subscription
  T4 send_receipt        ── (irreversible: never compensated, runs last)

  failure anywhere → persist state='compensating' → run Cn…C1 reverse order
  compensation exhausts retries → state='blocked' → page a human
```

## Step 1 — schema

```sql
CREATE TABLE sagas (
  id           uuid PRIMARY KEY,
  tenant_id    text        NOT NULL,
  kind         text        NOT NULL DEFAULT 'checkout',
  state        text        NOT NULL,   -- running|compensating|blocked|succeeded|...
  cause_code   text,
  lease_owner  text,
  lease_expires_at timestamptz,
  created_at   timestamptz NOT NULL DEFAULT now(),
  finished_at  timestamptz
);

CREATE TABLE saga_steps (
  saga_id   uuid NOT NULL REFERENCES sagas(id),
  step      text NOT NULL,             -- reserve_inventory | charge_payment | ...
  state     text NOT NULL DEFAULT 'pending', -- pending|running|done|failed|compensated
  attempt   int  NOT NULL DEFAULT 0,
  ref       text,                       -- stripe charge id, reservation id...
  error_code text,
  updated_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (saga_id, step)
);

CREATE TABLE compensations (
  step_key    text PRIMARY KEY,         -- '<saga_id>:<step>' → exactly one undo per step
  kind        text NOT NULL,
  state       text NOT NULL DEFAULT 'pending', -- pending|done|blocked
  attempt     int  NOT NULL DEFAULT 0,
  provider_ref text,
  last_error  text,
  updated_at  timestamptz NOT NULL DEFAULT now()
);
```

## Step 2 — forward execution with durable intent

```ts
const STEPS = ["reserve_inventory", "charge_payment", "activate_subscription", "send_receipt"] as const;
type Step = (typeof STEPS)[number];

export async function runCheckout(input: CheckoutInput): Promise<SagaView> {
  const id = await db.one(`INSERT INTO sagas (tenant_id, kind, state)
                           VALUES ($1,'checkout','running') RETURNING id`, [input.tenantId]);
  for (const step of STEPS) await advance(id, step, input);
  await db.query(`UPDATE sagas SET state='succeeded', finished_at=now()
                   WHERE id=$1 AND state='running'`, [id]);   // guarded, once
  return view(id);
}

async function advance(sagaId: string, step: Step, input: CheckoutInput) {
  await db.query(
    `INSERT INTO saga_steps (saga_id, step, state) VALUES ($1,$2,'pending')
     ON CONFLICT (saga_id, step) DO NOTHING`, [sagaId, step]);
  await db.query(
    `UPDATE saga_steps SET state='running', attempt=attempt+1
     WHERE saga_id=$1 AND step=$2 AND state IN ('pending','failed')`, [sagaId, step]);

  try {
    const ref = await executeStep(step, input);          // see Step 3
    await db.query(`UPDATE saga_steps SET state='done', ref=$3
                     WHERE saga_id=$1 AND step=$2`, [sagaId, step, ref]);
  } catch (err) {
    const e = classify(err);
    await db.query(`UPDATE saga_steps SET state='failed', error_code=$3
                     WHERE saga_id=$1 AND step=$2`, [sagaId, step, e.code]);

    if (e.ambiguous) {                                   // timeout / lost ack: never guess
      const known = await resolveStepByKey(step, input);
      if (known === "done") {
        await db.query(`UPDATE saga_steps SET state='done'
                         WHERE saga_id=$1 AND step=$2`, [sagaId, step]);
        return;
      }
      if (known === "unknown") {
        await db.query(`UPDATE sagas SET state='blocked', cause_code='AMBIGUOUS_STEP'
                         WHERE id=$1`, [sagaId]);
        await alert("saga.ambiguous", { sagaId, step });
        throw new SagaBlocked(sagaId, step);
      }
    }
    if (e.retryable && (await attempts(sagaId, step)) < 3) return advance(sagaId, step, input);

    // Durable decision FIRST, then undo.
    await db.query(`UPDATE sagas SET state='compensating', cause_code=$2
                     WHERE id=$1 AND state='running'`, [sagaId, e.code]);
    await compensate(sagaId);
    throw new SagaFailed(sagaId, e);                     // caller sees compensated outcome
  }
}
```

## Step 3 — step implementations with stable keys

```ts
async function executeStep(step: Step, input: CheckoutInput): Promise<string> {
  switch (step) {
    case "reserve_inventory": {
      // Guarded local update: 0 rows ⇒ sold out ⇒ a *permanent*, non-retryable domain error.
      const n = await db.query(
        `UPDATE inventory SET reserved = reserved + $2
          WHERE sku=$1 AND available - reserved >= $2`, [input.sku, input.qty]);
      if (n.rowCount === 0) throw new DomainError("INVENTORY_UNAVAILABLE", { http: 409 });
      return `res:${input.sku}`;
    }
    case "charge_payment": {
      const charge = await stripe.charges.create(
        { amount: input.amountCents, currency: "usd", customer: input.stripeCustomerId },
        { idempotencyKey: `charge:${input.orderId}` });   // ONE key per logical charge
      return charge.id;
    }
    case "activate_subscription": {
      const sub = await db.one(
        `INSERT INTO subscriptions (tenant_id, order_id, status, plan)
         VALUES ($1,$2,'active',$3)
         ON CONFLICT (tenant_id, order_id) DO UPDATE SET status='active'
         RETURNING id`, [input.tenantId, input.orderId, input.plan]);
      return String(sub.id);                             // insert is naturally idempotent
    }
    case "send_receipt": {
      // IRREVERSIBLE. Runs last, only after every other step is 'done'.
      await mailer.send({ to: input.email, template: "receipt", orderId: input.orderId });
      return "sent";
    }
  }
}
```

## Step 4 — compensation, reverse order, two safety layers

```ts
export async function compensate(sagaId: string) {
  const done = await db.any(
    `SELECT step, ref FROM saga_steps
      WHERE saga_id=$1 AND state='done'
      ORDER BY updated_at DESC`, [sagaId]);               // reverse execution order

  for (const { step, ref } of done) {
    if (step === "send_receipt") continue;                // irreversible: cannot undo
    const key = `${sagaId}:${step}`;
    await db.query(
      `INSERT INTO compensations (step_key, kind) VALUES ($1,$2)
       ON CONFLICT (step_key) DO NOTHING`, [key, step]);

    for (let attempt = 1; attempt <= 8; attempt++) {
      const row = await db.one(`SELECT state FROM compensations WHERE step_key=$1`, [key]);
      if (row.state === "done") break;                    // another runner finished it
      try {
        await db.query(`UPDATE compensations SET attempt=attempt+1 WHERE step_key=$1`, [key]);
        const providerRef = await performCompensation(step, sagaId, ref);   // idempotent
        await db.query(
          `UPDATE compensations SET state='done', provider_ref=$2, last_error=NULL
            WHERE step_key=$1 AND state <> 'done'`, [key, providerRef]);
        await db.query(`UPDATE saga_steps SET state='compensated'
                         WHERE saga_id=$1 AND step=$2`, [sagaId, step]);
        break;
      } catch (err) {
        const e = classify(err);
        await db.query(`UPDATE compensations SET last_error=$2 WHERE step_key=$1`,
          [key, e.code]);
        if (!e.retryable && e.http !== 409) return escalate(sagaId, key, err); // permanent
        if (attempt === 8) return escalate(sagaId, key, err);                  // exhausted
        await sleep(backoff(attempt));                     // 1s … 128s + jitter
      }
    }
  }
  await db.query(`UPDATE sagas SET state='compensated', finished_at=now()
                   WHERE id=$1 AND state='compensating'`, [sagaId]);
}

async function performCompensation(step: Step, sagaId: string, ref?: string) {
  if (step === "charge_payment") {
    const existing = await stripe.refunds.list({ charge: ref, limit: 10 });
    const mine = existing.data.find((r) => r.metadata?.saga === sagaId);
    if (mine) return mine.id;                             // read-back: already refunded
    const rf = await stripe.refunds.create(
      { charge: ref }, { idempotencyKey: `refund:${sagaId}` });  // one key per undo
    return rf.id;
  }
  if (step === "reserve_inventory") {
    await db.query(`UPDATE inventory SET reserved = reserved - $2 WHERE sku=$1`,
      [skuFor(sagaId), qtyFor(sagaId)]);
    return "released";
  }
  if (step === "activate_subscription") {
    await db.query(`UPDATE subscriptions SET status='cancelled'
                     WHERE order_id=$1 AND status='active'`, [orderIdFor(sagaId)]);
    return "cancelled";
  }
  throw new Error("uncompensable step");
}

async function escalate(sagaId: string, key: string, err: unknown) {
  await db.query(`UPDATE compensations SET state='blocked' WHERE step_key=$1`, [key]);
  await db.query(`UPDATE sagas SET state='blocked' WHERE id=$1 AND state='compensating'`, [sagaId]);
  await alert("compensation.blocked", { sagaId, key, err: classify(err) });  // page a human
}
```

## Step 5 — inject the failures and watch

```text
A) Kill the process after charge_payment, before activate_subscription (SIGKILL):
   sagas.state='running'; steps: reserve=done, charge=done, activate=pending
   boot → resumeAll() → claim lease → advance() → activate runs (idempotent insert)
   ⇒ succeeded, exactly one charge

B) Stripe times out on charge (outcome ambiguous):
   resolveStepByKey → charge id exists with key charge:ord_9f2 → 'done' → continue
   ⇒ no double charge, no false failure

C) Stripe refunds permanently rejected (card expired / refund window):
   8 attempts over ~4 min → compensations.state='blocked' → sagas.state='blocked'
   ⇒ Slack alert with saga id + ledger link; money held is now owned by a human

D) Operator cancels a running checkout:
   UPDATE sagas SET state='compensating' WHERE id=$1 AND state='running'  (guard wins)
   ⇒ the same compensate() path runs; no duplicate undo from the concurrent sweeper
```

## Key data / numbers

- Forward steps: **4**; compensations: **3** (`send_receipt` is irreversible and excluded).
- Charge idempotency key: `charge:<order_id>`; refund key: `refund:<saga_id>` — **one key per
  logical operation**, reused across every attempt.
- Step forward retries: **3**; compensation retries: **8 attempts over ~4–7 minutes**, then
  `blocked` + page.
- HTTP mapping: inventory conflict → **`409`**; saga already running for the same idempotency key
  → **`409`**; started but unfinished → **`202`**; blocked workflow exposed to the client →
  **`409`** with `code: SAGA_BLOCKED` (never a fake `500`).
- Ledger/compensation SQL goes through the retry wrapper for **`40001`/`40P01`** — the `sagas`
  row is hot when a sweeper and a request race.

## Real-world use case — Acme SaaS

Acme's `Checkout` shipped as four sequential service calls with a `try/catch` that logged. In one
month: 11 charges without subscriptions (deploy killed the process between T2 and T3), 2 double
refunds (failure path and cron both refunded), and one email sent for a payment that never
settled. This exact implementation replaced it. Within a quarter: **0 duplicate charges, 0 double
refunds**, ambiguous charges resolved in under 30 s by read-back, and the two genuinely stuck
refunds (permanently rejected by the PSP) showed up as `blocked` alerts the same minute they
happened — instead of being discovered by finance.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| This: DB-backed orchestrator + ledger | transparent, SQL-debuggable, no new infra | you own the runner/sweeper | one primary DB, few sagas |
| Temporal/Step Functions-style engine | timers, retries, UI, durability built in | new dependency, learning curve | many long-running workflows |
| Synchronous happy path + async repair | fast when things work | repair path rots because it is rarely run | only with heavy chaos testing |
| No ledger, compensate from logs | less schema | duplicates and strands under failure | never for money |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Persist `compensating` before the first undo | Decide to refund only in a `catch` block |
| Guard every state transition with `WHERE state=...` | Overwrite state unconditionally |
| List refunds (read-back) before creating one | Blind refund on retry |
| Exclude irreversible steps from compensation | Try to "unsend" the receipt |
| Page on `blocked`, not just on `failed` | Let a stuck refund sit unnoticed |
| Test with `SIGKILL`, timeout, and double-trigger | Test only the happy path |

## Common mistakes

- **Compensation triggered in the request handler** — the request dies, compensation never runs.
- **Refund key per attempt** (`refund:${Date.now()}`) — each retry is a new logical refund.
- **Resume without claiming a lease** — sweeper and runner both advance; guarded `UPDATE`s save
  you, but only if every write has the guard.
- **`send_receipt` before payment** — an irreversible effect on a path that can still fail.
- **Returning `500` for a `blocked` saga** — clients retry forever against a state that will not
  change; return `409` with a stable code.

## Checklist

- [ ] Schema has `sagas`, `saga_steps`, `compensations` with guarded transitions.
- [ ] Every forward step is idempotent by a stable business key.
- [ ] Ambiguous step outcomes are resolved by read-back before any retry.
- [ ] Compensations run in reverse order with two safety layers (ledger + provider key).
- [ ] `blocked` alerts a human within seconds of the final attempt.
- [ ] Resume claims a lease; sweeper handles `running`/`compensating` with expired leases.
- [ ] Failure injection (kill, timeout, double-trigger) is a CI test, not a hope.

## Related

- [Saga and Compensation Mechanics](../02-deep-dive/01-saga-and-compensation-mechanics.md)
- [States, Compensation Safety, and Irreversibility (39.13–39.16)](../01-concepts/05-states-compensation-safety-and-irreversibility.md)
- [Chapter 39 Reference — rollback/compensation guide](../05-reference/README.md)
- [Idempotency and Duplicate-Operation Safety (Ch. 28)](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
